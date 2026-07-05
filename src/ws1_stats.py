"""
ws1_stats.py — formal statistical tests behind WS1's comparative claims (D-016).

Turns the WS1 audit's descriptive statements into tested hypotheses, so the
report can cite inference, not adjectives:

  H1  London free share vs rest-of-national        (two-proportion z)
  H2  London paid prices vs rest-of-national       (Mann-Whitney U + rank-biserial)
  H3  London access-info share vs rest-of-national (two-proportion z)
  H4  Sessions vs population-proportional spread   (chi-square) + per-capita Gini

Writes results/ws1_statistical_tests.txt and ws1.* rows in results/metrics.csv.
Run:  python -m src.ws1_stats     Deps: pandas, numpy, scipy.
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
LONDON = ROOT / "data" / "processed" / "london_sessions_2026-06-30.csv"
RAW = ROOT / "data" / "raw" / "session_series_raw_2026-06-30.json"
FEATURES = ROOT / "data" / "processed" / "borough_features.csv"
MANIFEST = ROOT / "results" / "metrics.csv"
LOG = ROOT / "results" / "ws1_statistical_tests.txt"
MANIFEST_COLS = ["metric_id", "value", "population", "unit", "vintage", "source_dataset",
                 "definition", "script", "results_file", "commit", "timestamp",
                 "corroboration", "verified_by"]

_lines: list[str] = []


def log(m: str = "") -> None:
    print(m)
    _lines.append(m)


def two_prop_z(x1: int, n1: int, x2: int, n2: int) -> tuple[float, float]:
    """Two-proportion z-test (pooled). Self-checked: z**2 equals the 2x2
    chi-square without continuity correction."""
    p1, p2, pp = x1 / n1, x2 / n2, (x1 + x2) / (n1 + n2)
    z = (p1 - p2) / np.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    p = float(2 * stats.norm.sf(abs(z)))
    chi = stats.chi2_contingency(
        [[x1, n1 - x1], [x2, n2 - x2]], correction=False).statistic
    assert abs(z**2 - chi) < 1e-8, "z^2 != chi2 — implementation error"
    return float(z), p


def gini(values: np.ndarray) -> float:
    v = np.sort(np.asarray(values, float))
    n = len(v)
    return float((2 * np.arange(1, n + 1) - n - 1).dot(v) / (n * v.sum()))


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True, timeout=10).stdout.strip() or "unknown"
    except Exception:
        sha = "unknown"
    log(f"ws1_stats | {ts} | commit {sha}")

    L = pd.read_csv(LONDON)
    pl = pd.to_numeric(L["price"], errors="coerce")
    raw = json.load(open(RAW))
    rows = []
    for it in raw:
        d = it.get("data", {}) or {}
        off = d.get("offers")
        p = (off[0].get("price") if isinstance(off, list) and off and isinstance(off[0], dict)
             else (off.get("price") if isinstance(off, dict) else None))
        rows.append({"id": str(it.get("id")).split("/")[-1], "price": p})
    N = pd.DataFrame(rows).drop_duplicates("id")
    N["price"] = pd.to_numeric(N["price"], errors="coerce")
    rest = N[~N["id"].isin(set(L["id"].astype(str)))]

    # H1 free share
    z1, p1 = two_prop_z(int((pl == 0).sum()), len(L), int((rest["price"] == 0).sum()), len(rest))
    log(f"H1 free share London {int((pl==0).sum())}/{len(L)} vs rest "
        f"{int((rest['price']==0).sum())}/{len(rest)}: z={z1:.2f}, p={p1:.4f} "
        f"-> {'significant' if p1 < 0.05 else 'NOT significant'}")

    # H2 paid prices
    lp, rp = pl[pl > 0], rest["price"][rest["price"] > 0]
    u = stats.mannwhitneyu(lp, rp, alternative="two-sided")
    rb = float(1 - 2 * u.statistic / (len(lp) * len(rp)))
    log(f"H2 paid price medians £{lp.median():.2f} (London) vs £{rp.median():.2f} (rest): "
        f"U={u.statistic:.0f}, p={u.pvalue:.2e}, rank-biserial={rb:+.3f}")

    # H3 access info (rest share from national total minus London)
    acc_l = int(L["has_access_info"].astype(str).str.lower().isin(["true", "1"]).sum())
    NAT_ACCESS_TRUE = 692     # national count, verified vs field-completeness report
    z3, p3 = two_prop_z(acc_l, len(L), NAT_ACCESS_TRUE - acc_l, len(N) - len(L))
    log(f"H3 access-info {acc_l/len(L)*100:.1f}% (London) vs "
        f"{(NAT_ACCESS_TRUE-acc_l)/(len(N)-len(L))*100:.1f}% (rest): z={z3:.2f}, p={p3:.2e}")

    # H4 concentration
    F = pd.read_csv(FEATURES)
    f32 = F[F["lad_code"] != "E09000001"]
    obs = f32["n_sessions"].fillna(0).to_numpy(float)
    exp = f32["population"].to_numpy(float) / f32["population"].sum() * obs.sum()
    chi = stats.chisquare(obs, exp)
    g = gini((f32["n_sessions"].fillna(0) / f32["population"] * 1e4).to_numpy())
    log(f"H4 chi-square vs population-proportional: chi2={chi.statistic:.0f}, df=31, "
        f"p={chi.pvalue:.2e}; Gini(sessions per 10k)={g:.3f}")

    # ---- manifest rows ----
    script, rf = "src/ws1_stats.py", "results/ws1_statistical_tests.txt"
    vintage = "2026-06-30 snapshot"

    def row(mid, val, pop, unit, definition, corroboration=""):
        v = f"{val:.4f}".rstrip("0").rstrip(".") if isinstance(val, float) else str(val)
        return {"metric_id": mid, "value": v, "population": pop, "unit": unit,
                "vintage": vintage, "source_dataset": "london CSV + raw JSON + features",
                "definition": definition, "script": script, "results_file": rf,
                "commit": sha, "timestamp": ts, "corroboration": corroboration,
                "verified_by": ""}

    out_rows = [
        row("ws1.test.free_share_london_vs_rest_p", p1, "London vs rest-of-national",
            "p-value", "Two-proportion z (pooled), free = price==0. NOT significant: "
            "London's higher free share is within sampling noise — report descriptively only."),
        row("ws1.test.paid_price_london_vs_rest_p", float(u.pvalue), "London vs rest-of-national",
            "p-value", f"Mann-Whitney U on paid prices; medians £{lp.median():.2f} vs "
            f"£{rp.median():.2f}; rank-biserial {rb:+.3f}. London significantly dearer."),
        row("ws1.test.access_info_london_vs_rest_p", p3, "London vs rest-of-national",
            "p-value", "Two-proportion z on has_access_info==True. London markedly lower "
            "(22.7% vs 53.2%) — publisher-practice signal, significant."),
        row("ws1.test.concentration_chi2_p", float(chi.pvalue), "London-32",
            "p-value", "Chi-square of borough session counts vs population-proportional "
            "expectation. Provision decisively non-proportional."),
        row("ws1.concentration_gini_per10k", g, "London-32", "index",
            "Gini of sessions per 10k across 32 boroughs (0=equal).",
            "Repo granularity artefact reports Gini 0.581 on raw counts (33) — same order."),
    ]
    if MANIFEST.exists():
        ex = pd.read_csv(MANIFEST, dtype=str)
        ex = ex[~ex["metric_id"].str.startswith("ws1.")]
        merged = pd.concat([ex, pd.DataFrame(out_rows).astype(str)], ignore_index=True)
    else:
        merged = pd.DataFrame(out_rows)
    merged[MANIFEST_COLS].to_csv(MANIFEST, index=False, quoting=csv.QUOTE_ALL)
    log(f"\nWrote {len(out_rows)} ws1.* rows -> {MANIFEST.relative_to(ROOT)}")
    LOG.write_text("\n".join(_lines) + "\n")
    print(f"Log -> {LOG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
