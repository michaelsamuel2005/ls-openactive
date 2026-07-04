"""
verify_event_harvest.py — independent recompute of Wesley's event-harvest numbers
(hand-off §11 items 4-6; see docs/event_harvest_audit.md for the full audit).

PHASE 1  REPRODUCE: recompute every number printed in load_subevents.ipynb from
         Wesley's saved CSV, using HIS exact definitions (London-32 list without
         City of London; free = adultPrice==0 OR juniorPrice==0). Exact-match
         checks prove the file is the same run the notebook printed.
PHASE 2  CORRECT: recompute with project-standard definitions — London-33
         (City included), free share on the price-known denominator, paid-only
         price statistics, duration.
PHASE 3  RECORD: write event_harvest.* rows to results/metrics.csv (this script
         owns that prefix) + full log to results/event_harvest_recompute.txt.

INPUT: data/external/wesley/output.csv   (ask Wesley for output.csv + the
       harvest run date; do NOT re-run his notebooks — a live re-harvest
       cannot reproduce point-in-time numbers).
RUN:   python -m src.verify_event_harvest [optional_csv_path] [harvest_date]
DEPS:  pandas + stdlib.

CONTEXT CAVEAT (carry into any use of these numbers): this harvest covers the
37 ScheduledSession feeds only — Open Sessions publishes none, so this is the
COMMERCIAL/institutional operator universe, disjoint from the project's primary
Open Sessions layer. It is NOT an intensity lens on Open Sessions (D-014
reframe). Known defects biasing the free share DOWN: offer-name-restricted
price extraction; survivorship filter requiring booking-system fields.
"""
from __future__ import annotations

import csv
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "external" / "wesley" / "output.csv"
RESULTS_DIR = ROOT / "results"
MANIFEST = RESULTS_DIR / "metrics.csv"
AUDIT_LOG = RESULTS_DIR / "event_harvest_recompute.txt"

MANIFEST_COLS = [
    "metric_id", "value", "population", "unit", "vintage", "source_dataset",
    "definition", "script", "results_file", "commit", "timestamp",
    "corroboration", "verified_by",
]

# Wesley's hand-typed London list (32 — City of London ABSENT), verbatim:
LONDON_32 = [
    "Barking and Dagenham", "Barnet", "Bexley", "Brent", "Bromley", "Camden",
    "Croydon", "Ealing", "Enfield", "Greenwich", "Hackney",
    "Hammersmith and Fulham", "Haringey", "Harrow", "Havering", "Hillingdon",
    "Hounslow", "Islington", "Kensington and Chelsea", "Kingston upon Thames",
    "Lambeth", "Lewisham", "Merton", "Newham", "Redbridge",
    "Richmond upon Thames", "Southwark", "Sutton", "Tower Hamlets",
    "Waltham Forest", "Wandsworth", "Westminster",
]
LONDON_33 = LONDON_32 + ["City of London"]

# Expected values printed in the sent notebook (load_subevents (1).ipynb):
EXPECTED = {
    "uk_events": 464_392, "london32_events": 136_520,
    "uk_free": 8_646, "london32_free": 1_395,
    "uk_venues": 527, "london32_venues": 128,
    "uk_unique_locations_exact": 523, "uk_unique_names": 17_110,
    "borough_mean": 4_266.25, "borough_std": 4_603.650431,
    "borough_q25": 1_165.0, "borough_median": 3_211.5,
    "borough_q75": 5_594.25, "borough_max": 20_644,
    "locations_per_borough_mean": 4.266667, "locations_per_borough_n": 30,
    "top5": ["Hackney", "Camden", "Newham", "Enfield", "Hillingdon"],
}

_log: list[str] = []


def log(msg: str = "") -> None:
    print(msg)
    _log.append(msg)


def check(name: str, got, want, tol: float = 0.0) -> bool:
    ok = (abs(got - want) <= tol) if isinstance(want, (int, float)) else (got == want)
    log(f"  {'OK ' if ok else 'MISMATCH'}  {name}: got {got!r}  expected {want!r}")
    return ok


def git_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def main() -> int:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    harvest_date = sys.argv[2] if len(sys.argv) > 2 else "TBC (ask Wesley)"
    if not csv_path.exists():
        print(f"Input not found: {csv_path}\n"
              "Ask Wesley for output.csv (+ harvest run date) and place it at "
              "data/external/wesley/output.csv — do not re-run his notebooks.")
        return 1

    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sha = git_commit()
    log(f"verify_event_harvest | {ts} | commit {sha} | input {csv_path.name} | "
        f"harvest date: {harvest_date}")

    df = pd.read_csv(csv_path, dtype={"id": str}, low_memory=False)
    log(f"rows: {len(df)}  columns: {list(df.columns)}")

    adult = pd.to_numeric(df["adultPrice"], errors="coerce")
    junior = pd.to_numeric(df["juniorPrice"], errors="coerce")
    free_wesley = (adult == 0) | (junior == 0)          # his definition, exactly
    lon32 = df["borough"].isin(LONDON_32)
    lon33 = df["borough"].isin(LONDON_33)
    city = df["borough"] == "City of London"

    # ---------------- PHASE 1: reproduce the notebook's printed numbers
    log("\n===== PHASE 1 — reproduce Wesley's printed numbers (his definitions)")
    all_ok = True
    all_ok &= check("UK events", len(df), EXPECTED["uk_events"])
    all_ok &= check("London-32 events", int(lon32.sum()), EXPECTED["london32_events"])
    all_ok &= check("UK free (his defn)", int(free_wesley.sum()), EXPECTED["uk_free"])
    all_ok &= check("London-32 free", int((free_wesley & lon32).sum()),
                    EXPECTED["london32_free"])
    all_ok &= check("UK venues", int(df["venue"].nunique()), EXPECTED["uk_venues"])
    all_ok &= check("London-32 venues", int(df.loc[lon32, "venue"].nunique()),
                    EXPECTED["london32_venues"])
    all_ok &= check("UK unique names", int(df["name"].nunique()),
                    EXPECTED["uk_unique_names"])

    coords = df.dropna(subset=["longitude", "latitude"])
    all_ok &= check("UK unique exact coord positions",
                    int(coords.groupby(["longitude", "latitude"]).ngroups),
                    EXPECTED["uk_unique_locations_exact"])

    bc = df.loc[lon32, "borough"].value_counts().reindex(LONDON_32, fill_value=0)
    all_ok &= check("borough mean", float(bc.mean()), EXPECTED["borough_mean"], 0.01)
    all_ok &= check("borough std", float(bc.std()), EXPECTED["borough_std"], 0.01)
    all_ok &= check("borough q25", float(bc.quantile(.25)), EXPECTED["borough_q25"], 0.01)
    all_ok &= check("borough median", float(bc.median()), EXPECTED["borough_median"], 0.01)
    all_ok &= check("borough q75", float(bc.quantile(.75)), EXPECTED["borough_q75"], 0.01)
    all_ok &= check("borough max", int(bc.max()), EXPECTED["borough_max"])
    all_ok &= check("top5 boroughs", list(bc.nlargest(5).index), EXPECTED["top5"])

    lc = coords[coords["borough"].isin(LONDON_32)].copy()
    lc["lat_r"] = lc["latitude"].round(5)
    lc["lon_r"] = lc["longitude"].round(5)
    lpb = lc.groupby("borough")[["lat_r", "lon_r"]].apply(
        lambda x: x.drop_duplicates().shape[0])
    all_ok &= check("locations/borough mean", float(lpb.mean()),
                    EXPECTED["locations_per_borough_mean"], 0.001)
    all_ok &= check("boroughs with coords (n)", int(lpb.shape[0]),
                    EXPECTED["locations_per_borough_n"])

    verdict = ("FILE MATCHES the sent notebook run — Wesley's arithmetic verified."
               if all_ok else
               "FILE DOES NOT fully match the sent notebook run (different "
               "harvest?). Corrected stats below still stand for THIS file, "
               "but do not attribute them to the notebook's run.")
    log(f"\nPHASE 1 VERDICT: {verdict}")

    # ---------------- PHASE 2: corrected, project-standard statistics
    log("\n===== PHASE 2 — corrected statistics (project definitions)")
    n_city = int(city.sum())
    log(f"City of London events (excluded by Wesley's list): {n_city}")
    n_l33 = int(lon33.sum())
    log(f"London-33 events (City included): {n_l33}")

    price_known = adult.notna() | junior.notna()
    for scope, mask in [("UK", pd.Series(True, index=df.index)),
                        ("London-33", lon33)]:
        n = int(mask.sum())
        known = int((price_known & mask).sum())
        free = int((free_wesley & mask).sum())
        minp = pd.concat([adult[mask], junior[mask]], axis=1).min(axis=1)
        paid = minp[minp > 0]
        log(f"\n[{scope}] n={n}  price-known={known} ({known/n*100:.1f}%)  "
            f"free={free}")
        log(f"[{scope}] free share: all-rows {free/n*100:.2f}%  |  "
            f"price-known {free/known*100:.2f}%" if known else f"[{scope}] no prices")
        log(f"[{scope}] paid min-price: median £{paid.median():.2f}  "
            f"mean £{paid.mean():.2f}  (n={len(paid)})")
        ad_paid = adult[mask & (adult > 0)]
        log(f"[{scope}] paid ADULT price: median £{ad_paid.median():.2f}  "
            f"mean £{ad_paid.mean():.2f}  (n={len(ad_paid)})")

    dur = pd.to_numeric(df["duration"], errors="coerce")
    if dur.isna().all():
        dur = pd.to_timedelta(df["duration"], errors="coerce").dt.total_seconds() / 60
    log(f"\nduration (minutes): mean {dur.mean():.1f}  median {dur.median():.1f}  "
        f"(n={int(dur.notna().sum())})")

    bc33 = df.loc[lon33, "borough"].value_counts().reindex(LONDON_33, fill_value=0)
    log(f"London-33 events/borough: mean {bc33.mean():.1f}  median {bc33.median():.1f}"
        f"  zero-event boroughs: {list(bc33[bc33 == 0].index)}")

    # ---------------- PHASE 3: manifest
    RESULTS_DIR.mkdir(exist_ok=True)
    script = "src/verify_event_harvest.py"
    src = str(csv_path.relative_to(ROOT)) if csv_path.is_relative_to(ROOT) else str(csv_path)
    vintage = f"Wesley event harvest ({harvest_date})"
    rf = "results/event_harvest_recompute.txt"
    caveat = ("Commercial-universe layer (37 ScheduledSession feeds; Open Sessions "
              "absent). Offer-name-restricted price extraction biases free share "
              "down. See docs/event_harvest_audit.md.")

    def fmt(v):
        if isinstance(v, float):
            return str(int(v)) if v.is_integer() else f"{v:.4f}".rstrip("0").rstrip(".")
        return str(v)

    def row(metric_id, value, population, unit, definition, corroboration=""):
        return {"metric_id": metric_id, "value": fmt(value), "population": population,
                "unit": unit, "vintage": vintage, "source_dataset": src,
                "definition": f"{definition} {caveat}", "script": script,
                "results_file": rf, "commit": sha, "timestamp": ts,
                "corroboration": corroboration,
                "verified_by": "Michael (independent recompute of Wesley's file)"}

    known33 = int((price_known & lon33).sum())
    free33 = int((free_wesley & lon33).sum())
    minp33 = pd.concat([adult[lon33], junior[lon33]], axis=1).min(axis=1)
    paid33 = minp33[minp33 > 0]
    rows = [
        row("event_harvest.uk.n_events", len(df), "UK", "events",
            "Event rows passing Wesley's required-fields filter.",
            f"Notebook printed 464,392 — reproduction {'OK' if all_ok else 'PARTIAL'}."),
        row("event_harvest.london32.n_events", int(lon32.sum()),
            "London-32 (no City; Wesley list)", "events",
            "Events in Wesley's 32-borough list.", "Notebook printed 136,520."),
        row("event_harvest.london33.n_events", n_l33, "London-33", "events",
            "Events in all 33 LADs incl. City of London (project standard, D-008)."),
        row("event_harvest.london33.n_city_events", n_city, "City of London",
            "events", "Events Wesley's hand-typed list silently excluded."),
        row("event_harvest.london33.pct_free_all", free33 / n_l33 if n_l33 else 0,
            "London-33", "proportion",
            "Free = adultPrice==0 OR juniorPrice==0; denominator all rows."),
        row("event_harvest.london33.pct_free_price_known",
            free33 / known33 if known33 else 0, "London-33", "proportion",
            "Free share among rows with any extracted price."),
        row("event_harvest.london33.paid_minprice_median",
            float(paid33.median()) if len(paid33) else 0, "London-33", "GBP",
            f"Median of per-row min(adult, junior) among >0 (n={len(paid33)})."),
        row("event_harvest.uk.n_venues", int(df["venue"].nunique()), "UK", "venues",
            "Distinct venue-name strings. The '527' figure — UK, NOT London."),
        row("event_harvest.london32.n_venues", int(df.loc[lon32, "venue"].nunique()),
            "London-32 (no City; Wesley list)", "venues",
            "Distinct venue-name strings. Resolves §11 item 4: London is ~128, "
            "not 527; '~137' was 4.27 x 32 (wrong multiplier — mean is over 30)."),
    ]

    if MANIFEST.exists():
        existing = pd.read_csv(MANIFEST, dtype=str)
        existing = existing[~existing["metric_id"].str.startswith("event_harvest.")]
        merged = pd.concat([existing, pd.DataFrame(rows).astype(str)],
                           ignore_index=True)
    else:
        merged = pd.DataFrame(rows)
    merged = merged[MANIFEST_COLS]
    merged.to_csv(MANIFEST, index=False, quoting=csv.QUOTE_ALL)
    log(f"\nWrote {len(rows)} event_harvest rows -> {MANIFEST.relative_to(ROOT)}")

    AUDIT_LOG.write_text("\n".join(_log) + "\n")
    print(f"Audit log -> {AUDIT_LOG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
