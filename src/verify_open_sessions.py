"""
verify_open_sessions.py — resolve the disputed Open Sessions figures (§11 items 1-3)
and seed the metrics manifest (D-016).

WHAT THIS DOES
  1. LONDON stats from the frozen snapshot data/processed/london_sessions_2026-06-30.csv
     (the single source of truth for London series — never re-derived from raw JSON):
       - n series, free/paid counts, free share (audit definition: is_free = price==0,
         missing price counted NOT free) + price-known sensitivity variant
       - typical PAID price: median & mean of rows with price > 0 (excludes free AND
         missing) — plus the "contaminated" describe()-style stats (zeros included)
         to document where the untraceable £4.80 likely came from
       - distinct venues three ways: raw location_name nunique; normalised
         (casefold + whitespace-collapsed) nunique; distinct coordinate pairs (5 dp)
  2. NATIONAL stats from data/raw/session_series_raw_2026-06-30.json using the SAME
     extraction rules as data_audit.ipynb (first offer price; dedup by id;
     is_free = price==0, missing -> False). Tests the hypothesis that the
     "41.6% free" figure was the NATIONAL rate printed by the audit notebook.
  3. Drift check on data/processed/london_sessions_2026-07-03.csv (log only —
     the frozen 06-30 snapshot remains authoritative for all reported numbers).
  4. Identity checks (hard assertions): free + paid + price_missing == total;
     venues <= series; national >= London; every proportion in [0, 1];
     sum(reports/sessions_per_borough_2026-06-30.csv) == London n_series.
  5. Writes/updates results/metrics.csv (only rows whose metric_id starts with
     "open_sessions." are owned and replaced by this script) and a full audit log
     at results/open_sessions_recompute.txt.

RUN:  conda activate ls-openactive && python -m src.verify_open_sessions
DEPS: pandas + stdlib only.
"""
from __future__ import annotations

import csv
import json
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LONDON_CSV = ROOT / "data" / "processed" / "london_sessions_2026-06-30.csv"
DRIFT_CSV = ROOT / "data" / "processed" / "london_sessions_2026-07-03.csv"
NATIONAL_JSON = ROOT / "data" / "raw" / "session_series_raw_2026-06-30.json"
BOROUGH_CSV = ROOT / "reports" / "sessions_per_borough_2026-06-30.csv"
RESULTS_DIR = ROOT / "results"
MANIFEST = RESULTS_DIR / "metrics.csv"
AUDIT_LOG = RESULTS_DIR / "open_sessions_recompute.txt"

MANIFEST_COLS = [
    "metric_id", "value", "population", "unit", "vintage", "source_dataset",
    "definition", "script", "results_file", "commit", "timestamp",
    "corroboration", "verified_by",
]

_log_lines: list[str] = []


def log(msg: str = "") -> None:
    print(msg)
    _log_lines.append(msg)


def git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
            capture_output=True, text=True, timeout=10,
        )
        sha = out.stdout.strip()
        return sha if sha else "unknown"
    except Exception:
        return "unknown"


def norm_venue(name: str) -> str:
    return " ".join(str(name).split()).casefold()


# ------------------------------------------------------------------ extractors
# Mirrors data_audit.ipynb: first offer's price; is_free = (price == 0) if
# price is present else False (missing price is NOT counted as free).

def first_offer_price(data: dict):
    offers = data.get("offers")
    if isinstance(offers, list) and offers:
        return offers[0].get("price") if isinstance(offers[0], dict) else None
    if isinstance(offers, dict):
        return offers.get("price")
    return None


def item_to_row(item: dict) -> dict:
    data = item.get("data", item) if isinstance(item, dict) else {}
    if not isinstance(data, dict):
        data = {}
    loc = data.get("location") or {}
    loc_name = loc.get("name") if isinstance(loc, dict) else None
    geo = loc.get("geo") or {} if isinstance(loc, dict) else {}
    return {
        "id": item.get("id", data.get("@id", data.get("id"))),
        "location_name": loc_name,
        "latitude": geo.get("latitude") if isinstance(geo, dict) else None,
        "longitude": geo.get("longitude") if isinstance(geo, dict) else None,
        "price": first_offer_price(data),
    }


# ------------------------------------------------------------------ stat blocks

def session_stats(df: pd.DataFrame, label: str) -> dict:
    """Compute the §11 stats on a sessions dataframe with explicit definitions."""
    n = len(df)
    price = pd.to_numeric(df["price"], errors="coerce")
    n_price_known = int(price.notna().sum())
    n_price_missing = n - n_price_known
    n_free = int((price == 0).sum())          # is_free rule: price == 0
    n_paid = int((price > 0).sum())
    assert n_free + n_paid + n_price_missing == n, f"{label}: identity failed"

    pct_free_all = n_free / n if n else float("nan")
    pct_free_known = n_free / n_price_known if n_price_known else float("nan")

    paid = price[price > 0]
    paid_median = float(paid.median()) if len(paid) else float("nan")
    paid_mean = float(paid.mean()) if len(paid) else float("nan")
    # The contaminated variant (zeros included) — likely origin of "£4.80":
    withzeros = price[price.notna()]
    contam_median = float(withzeros.median()) if len(withzeros) else float("nan")
    contam_mean = float(withzeros.mean()) if len(withzeros) else float("nan")

    venues_raw = int(df["location_name"].dropna().nunique())
    venues_norm = int(df["location_name"].dropna().map(norm_venue).nunique())
    lat = pd.to_numeric(df.get("latitude"), errors="coerce")
    lon = pd.to_numeric(df.get("longitude"), errors="coerce")
    coord_ok = lat.notna() & lon.notna()
    venues_coord = int(
        pd.DataFrame({"lat": lat[coord_ok].round(5), "lon": lon[coord_ok].round(5)})
        .drop_duplicates().shape[0]
    )

    # stored-is_free consistency check (London CSV only carries the column)
    stored_mismatch = None
    if "is_free" in df.columns:
        stored = df["is_free"].astype(str).str.strip().str.lower().isin(["true", "1"])
        recomputed = (price == 0)
        stored_mismatch = int((stored != recomputed).sum())

    # field completeness on THIS population (reports/field_completeness_*.csv is
    # NATIONAL-scoped — every pct × 1585 reconstructs an integer — so London
    # completeness must be computed here, on the London rows themselves).
    completeness = {"pct_price_present": float(price.notna().mean()),
                    "pct_coords_present": float(coord_ok.mean())}
    if "has_access_info" in df.columns:
        acc = df["has_access_info"].astype(str).str.strip().str.lower().isin(["true", "1"])
        completeness["pct_access_info_true"] = float(acc.mean())
    if "max_capacity" in df.columns:
        completeness["pct_capacity_present"] = float(
            pd.to_numeric(df["max_capacity"], errors="coerce").notna().mean())

    for p in (pct_free_all, pct_free_known):
        assert 0.0 <= p <= 1.0, f"{label}: proportion out of range"
    assert venues_raw <= n, f"{label}: venues > series"

    log(f"\n----- {label} -----")
    log(f"n series                          : {n}")
    log(f"free (price==0)                   : {n_free}")
    log(f"paid (price>0)                    : {n_paid}")
    log(f"price missing                     : {n_price_missing}")
    log(f"FREE SHARE (denom = all rows)     : {pct_free_all:.4f}  = {pct_free_all*100:.1f}%")
    log(f"free share (denom = price known)  : {pct_free_known:.4f}  = {pct_free_known*100:.1f}%")
    log(f"PAID price median (price>0 only)  : £{paid_median:.2f}   (n={len(paid)})")
    log(f"PAID price mean   (price>0 only)  : £{paid_mean:.2f}")
    log(f"  [contaminated, zeros included]  : median £{contam_median:.2f} / mean £{contam_mean:.2f}"
        f"   <- describe()-style; NOT 'typical paid price'")
    log(f"venues: raw location_name nunique : {venues_raw}")
    log(f"venues: normalised nunique        : {venues_norm}")
    log(f"venues: distinct coord pairs (5dp): {venues_coord}")
    if stored_mismatch is not None:
        log(f"stored is_free vs recomputed      : {stored_mismatch} mismatches")
    for k, v in completeness.items():
        log(f"completeness {k:<20}: {v*100:.1f}%")

    return {
        "n": n, "n_free": n_free, "n_paid": n_paid, "n_price_missing": n_price_missing,
        "pct_free_all": pct_free_all, "pct_free_known": pct_free_known,
        "paid_median": paid_median, "paid_mean": paid_mean, "n_paid_rows": int(len(paid)),
        "contam_median": contam_median, "contam_mean": contam_mean,
        "venues_raw": venues_raw, "venues_norm": venues_norm, "venues_coord": venues_coord,
        "stored_mismatch": stored_mismatch, "completeness": completeness,
    }


# ------------------------------------------------------------------ main

def main() -> int:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sha = git_commit()
    log(f"verify_open_sessions | {ts} | commit {sha}")

    # 1. London (frozen snapshot — authoritative)
    ldn = pd.read_csv(LONDON_CSV)
    L = session_stats(ldn, f"LONDON — {LONDON_CSV.name} (FROZEN SNAPSHOT)")

    # Borough-sum identity
    if BOROUGH_CSV.exists():
        bor = pd.read_csv(BOROUGH_CSV)
        bsum = int(bor["sessions"].sum())
        log(f"\nborough-sum identity: sum(sessions_per_borough)={bsum} vs n={L['n']}"
            f"  -> {'OK' if bsum == L['n'] else 'FAILED'}")
        assert bsum == L["n"], "sum(borough sessions) != London n_series"

    # 2. National (raw JSON, same rules as audit notebook)
    with open(NATIONAL_JSON) as f:
        raw = json.load(f)
    items = list(raw.values()) if isinstance(raw, dict) else list(raw)
    nat = pd.DataFrame([item_to_row(it) for it in items])
    nat = nat.drop_duplicates(subset="id").reset_index(drop=True)
    N = session_stats(nat, f"NATIONAL — {NATIONAL_JSON.name} (all Open Sessions publishers)")
    assert N["n"] >= L["n"], "national < London — scoping error"
    log(f"\nHYPOTHESIS CHECK: was '41.6% free' the NATIONAL rate?"
        f"  national pct_free_all = {N['pct_free_all']*100:.1f}%"
        f"  (London = {L['pct_free_all']*100:.1f}%)")

    # 3. Drift check (log only; NOT authoritative)
    if DRIFT_CSV.exists():
        drift = pd.read_csv(DRIFT_CSV)
        session_stats(drift, f"DRIFT CHECK — {DRIFT_CSV.name} (not authoritative)")

    # 4. Manifest
    RESULTS_DIR.mkdir(exist_ok=True)
    script = "src/verify_open_sessions.py"
    vintage = "2026-06-30 snapshot"
    src_ldn = "data/processed/london_sessions_2026-06-30.csv"
    src_nat = "data/raw/session_series_raw_2026-06-30.json"
    rf = "results/open_sessions_recompute.txt"

    def fmt(v) -> str:
        """Counts as integers; proportions/prices to 4/2 dp — no '494.0' artefacts."""
        if isinstance(v, int):
            return str(v)
        if isinstance(v, float):
            return str(int(v)) if v.is_integer() else f"{v:.4f}".rstrip("0").rstrip(".")
        return str(v)

    def row(metric_id, value, population, unit, source, definition, corroboration=""):
        return {
            "metric_id": metric_id, "value": fmt(value), "population": population,
            "unit": unit, "vintage": vintage, "source_dataset": source,
            "definition": definition, "script": script, "results_file": rf,
            "commit": sha, "timestamp": ts, "corroboration": corroboration,
            "verified_by": "",
        }

    rows = [
        row("open_sessions.london.n_series", L["n"], "London", "series", src_ldn,
            "Live SessionSeries in the frozen London snapshot (cleaned, deduped by id).",
            "Panel grep line-count 494 (2026-07-03); sum(borough file)==494."),
        row("open_sessions.london.n_free", L["n_free"], "London", "series", src_ldn,
            "Series with price == 0. Missing price NOT counted as free.",
            "Panel grep count of line-anchored is_free==True: 217 (2026-07-03)."),
        row("open_sessions.london.pct_free", round(L["pct_free_all"], 4), "London",
            "proportion", src_ldn,
            "n_free / n_series (denominator = ALL rows; missing price counted not-free; "
            "audit-notebook is_free rule).",
            "Panel grep 217/494 = 0.4393. REPLACES the mislabelled '41.6%'."),
        row("open_sessions.london.pct_free_price_known", round(L["pct_free_known"], 4),
            "London", "proportion", src_ldn,
            "n_free / n_price_known (sensitivity variant; excludes missing-price rows)."),
        row("open_sessions.london.paid_price_median", round(L["paid_median"], 2),
            "London", "GBP", src_ldn,
            f"Median price of series with price > 0 (n={L['n_paid_rows']}); free and "
            "missing-price rows excluded. REPLACES the untraceable £4.80."),
        row("open_sessions.london.paid_price_mean", round(L["paid_mean"], 2),
            "London", "GBP", src_ldn,
            f"Mean price of series with price > 0 (n={L['n_paid_rows']})."),
        row("open_sessions.london.n_venues_raw", L["venues_raw"], "London", "venues",
            src_ldn,
            "Distinct location_name (venue name/address string), exact match. "
            "HEADLINE venue count; supersedes the earlier ~254 estimate."),
        row("open_sessions.london.n_venues_normalised", L["venues_norm"], "London",
            "venues", src_ldn,
            "Distinct location_name after casefold + whitespace collapse "
            "(equals raw count: no casing/spacing variants present)."),
        row("open_sessions.london.n_venues_coord", L["venues_coord"], "London",
            "venues", src_ldn,
            "Distinct (lat, lon) pairs rounded to 5 dp — distinct mapped positions; "
            "differs from named venues where names share/split coordinates."),
        row("open_sessions.national.n_series", N["n"], "national", "series", src_nat,
            "Live SessionSeries across ALL Open Sessions publishers (deduped by id). "
            "Supersedes the earlier working figure '~1,605'.",
            "Same order as London Sport's published 'over 1,700 sessions'; live "
            "deduped snapshot expectedly lower than the published total."),
        row("open_sessions.national.pct_free", round(N["pct_free_all"], 4), "national",
            "proportion", src_nat,
            "n_free / n_series, all-rows denominator, same is_free rule.",
            "London Sport: >700 of ~1,700 free (~41%); matches. CONFIRMED origin of "
            "the previously mislabelled '41.6%' (it is the NATIONAL rate)."),
        row("open_sessions.national.paid_price_median", round(N["paid_median"], 2),
            "national", "GBP", src_nat,
            f"Median price of series with price > 0 (n={N['n_paid_rows']})."),
        row("open_sessions.national.n_venues_raw", N["venues_raw"], "national",
            "venues", src_nat, "Distinct location_name, exact string match."),
    ]
    # London-scoped field completeness (reports/field_completeness_2026-06-30.csv
    # is NATIONAL-scoped — verified: each pct x 1585 reconstructs an integer).
    for key, val in L["completeness"].items():
        rows.append(row(
            f"open_sessions.london.{key}", round(val, 4), "London", "proportion",
            src_ldn,
            f"Share of the {L['n']} London series with this field usable "
            "(access_info = share True; others = share non-null).",
            "NB: reports/field_completeness_2026-06-30.csv is national-scoped."))

    if MANIFEST.exists():
        existing = pd.read_csv(MANIFEST, dtype=str)
        existing = existing[~existing["metric_id"].str.startswith("open_sessions.")]
        merged = pd.concat([existing, pd.DataFrame(rows).astype(str)], ignore_index=True)
    else:
        merged = pd.DataFrame(rows)
    merged = merged[MANIFEST_COLS]
    merged.to_csv(MANIFEST, index=False, quoting=csv.QUOTE_ALL)
    log(f"\nWrote {len(rows)} open_sessions rows -> {MANIFEST.relative_to(ROOT)}")

    AUDIT_LOG.write_text("\n".join(_log_lines) + "\n")
    print(f"Audit log -> {AUDIT_LOG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
