"""
ws2_metrics.py — single owner of every `ws2.*` row in results/metrics.csv.

Closes examiner findings B4-2 (WS2 validation statistics had no manifest rows,
violating D-016 the moment §5 cites them), D3-2 (the bootstrap CI circulated
from an audit session without a committed script), and B2-3 (the quadrant
typology's median thresholds had no sensitivity evidence).

What it computes, all from the committed artefacts (never from memory):
  1. Primary validation  — Spearman ρ of gap vs held-out adult inactivity,
     with exact p, Fisher-z 95% CI (via the tested `spearman_inference`) AND a
     seeded pairs bootstrap CI (B=5,000, seed = config.RANDOM_SEED).
  2. Incremental validity — partial Spearman ρ(provision, inactivity | need),
     ΔR² and nested-F p, Moran's I on residuals (via `incremental_validity`).
  3. Facilities corroboration — Spearman ρ of gap vs facilities_per_10k with
     its p and n (directional support; report the p, never bare ρ — D3-1).
  4. Weighting sensitivity — min Spearman of each alternative weighting's
     ranking vs the base (from `gap_index.run`).
  5. Quadrant threshold sensitivity — membership stability when both median
     thresholds shift by ±0.10·SD and ±0.25·SD (B2-3); per-borough margins to
     `results/quadrant_sensitivity.csv`.

Manifest discipline (D-016): this script REPLACES exactly the rows whose
metric_id starts with `ws2.` and touches nothing else.

Run AFTER the pipeline and analysis:
    python -m src.run_pipeline && python -m src.run_analysis
    python -m src.ws2_metrics
"""
from __future__ import annotations

import csv
import subprocess
import warnings
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

from src.incremental_validity import partial_spearman, spearman_inference
from src.incremental_validity import run as iv_run
from src.pipeline import config as C

RESULTS_DIR = C.ROOT / "results"
MANIFEST = RESULTS_DIR / "metrics.csv"
SENS_OUT = RESULTS_DIR / "quadrant_sensitivity.csv"
WS2_PREFIX = "ws2."
BOOT_B = 5_000

MANIFEST_COLS = [
    "metric_id", "value", "population", "unit", "vintage", "source_dataset",
    "definition", "script", "results_file", "commit", "timestamp",
    "corroboration", "verified_by",
]
VINTAGE = "sessions 2026-06-30 · IoD2025 · Census 2021 · Active Lives 2024/25"


def _git_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=C.ROOT,
                             capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or "unknown"
    except Exception:                                   # noqa: BLE001
        return "unknown"


# ------------------------------------------------------------------ bootstrap
def boot_ci(x, y, n_boot: int = BOOT_B, seed: int = C.RANDOM_SEED,
            alpha: float = 0.05) -> dict:
    """Pairs-bootstrap percentile CI for the Spearman correlation of (x, y).

    Resamples borough PAIRS with replacement (keeps the x–y linkage), computes
    ρ per resample, and returns the percentile interval. Degenerate resamples
    (a constant vector, ρ undefined) are dropped and counted. Deterministic
    for a given seed — the seed lives in config (project rule).
    """
    from scipy import stats

    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if len(x) != len(y) or len(x) < 4:
        raise ValueError("boot_ci needs paired vectors of length >= 4")
    rng = np.random.default_rng(seed)
    n = len(x)
    rhos = np.empty(n_boot)
    dropped = 0
    for b in range(n_boot):
        idx = rng.integers(0, n, n)
        xs, ys = x[idx], y[idx]
        if np.all(xs == xs[0]) or np.all(ys == ys[0]):
            rhos[b] = np.nan
            dropped += 1
            continue
        rhos[b] = stats.spearmanr(xs, ys).statistic
    good = rhos[~np.isnan(rhos)]
    lo, hi = np.percentile(good, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {"ci_low": float(lo), "ci_high": float(hi), "n_boot": int(n_boot),
            "n_dropped": int(dropped), "seed": int(seed),
            "point": float(stats.spearmanr(x, y).statistic)}


# ------------------------------------------------ quadrant threshold stability
def quadrant_sensitivity(gap_df: pd.DataFrame,
                         deltas: tuple = (-0.25, -0.10, 0.10, 0.25)
                         ) -> tuple[pd.DataFrame, dict]:
    """Quadrant membership stability under threshold perturbation (B2-3).

    The typology cuts at the MEDIANS of need_z / provision_z over fully-scored
    rows (gap_index.quadrant). Here both thresholds are shifted by every
    combination of {0, ±0.10, ±0.25}·SD of the respective axis and membership
    is recomputed. Returns (per-borough table, summary). A borough is STABLE
    if its quadrant never changes across all shift combinations.
    """
    need = pd.to_numeric(gap_df["need_score_z"], errors="coerce")
    prov = pd.to_numeric(gap_df["provision_score_z"], errors="coerce")
    valid = need.notna() & prov.notna()
    med_n, med_p = need[valid].median(), prov[valid].median()
    sd_n, sd_p = need[valid].std(ddof=0), prov[valid].std(ddof=0)

    def assign(mn: float, mp: float) -> pd.Series:
        nh, ph = need > mn, prov > mp
        q = pd.Series(pd.NA, index=gap_df.index, dtype="object")
        q[valid & nh & ~ph] = "priority"
        q[valid & nh & ph] = "high_need_served"
        q[valid & ~nh & ~ph] = "low_low"
        q[valid & ~nh & ph] = "well_served"
        return q

    base = assign(med_n, med_p)
    # belt-and-braces: the base assignment must reproduce the committed column
    if "gap_quadrant" in gap_df.columns:
        committed = gap_df["gap_quadrant"].where(gap_df["gap_quadrant"].notna(), pd.NA)
        if not base[valid].astype(str).equals(committed[valid].astype(str)):
            raise AssertionError("base quadrant assignment does not reproduce "
                                 "the committed gap_quadrant column")

    shifts = [d for d in deltas] + [0.0]
    switch_count = pd.Series(0, index=gap_df.index)
    alternates: dict[int, set] = {i: set() for i in gap_df.index}
    n_combos = 0
    for dn, dp in product(shifts, shifts):
        if dn == 0.0 and dp == 0.0:
            continue
        n_combos += 1
        q = assign(med_n + dn * sd_n, med_p + dp * sd_p)
        changed = valid & (q.astype(str) != base.astype(str))
        switch_count[changed] += 1
        for i in gap_df.index[changed]:
            alternates[i].add(str(q[i]))

    table = pd.DataFrame({
        "lad_code": gap_df["lad_code"],
        "lad_name": gap_df.get("lad_name", pd.Series(index=gap_df.index)),
        "gap_quadrant": base,
        "need_margin_z": (need - med_n).round(4),
        "provision_margin_z": (prov - med_p).round(4),
        "n_switches": switch_count,
        "n_combos": n_combos,
        "alternate_quadrants": [";".join(sorted(alternates[i])) for i in gap_df.index],
    })
    scored = table[valid]
    summary = {
        "n_scored": int(valid.sum()),
        "n_combos": n_combos,
        "stable_share": float((scored["n_switches"] == 0).mean()),
        "n_switchers": int((scored["n_switches"] > 0).sum()),
        "switchers": scored.loc[scored["n_switches"] > 0, "lad_name"].tolist(),
    }
    return table, summary


# ------------------------------------------------------------------ manifest
def replace_ws2_rows(rows: list[dict], manifest_path: Path = MANIFEST) -> int:
    """Replace exactly the ws2.* rows in the manifest; leave every other row
    untouched (D-016 script-owned-prefix discipline). Returns rows written."""
    for r in rows:
        missing = set(MANIFEST_COLS) - set(r)
        if missing:
            raise ValueError(f"manifest row missing columns: {missing}")
        if not str(r["metric_id"]).startswith(WS2_PREFIX):
            raise ValueError(f"refusing to write non-ws2 row: {r['metric_id']}")
    if manifest_path.exists():
        existing = pd.read_csv(manifest_path, dtype=str)
        keep = existing[~existing["metric_id"].str.startswith(WS2_PREFIX)]
    else:
        keep = pd.DataFrame(columns=MANIFEST_COLS)
    out = pd.concat([keep, pd.DataFrame(rows)[MANIFEST_COLS].astype(str)],
                    ignore_index=True)
    out.to_csv(manifest_path, index=False, quoting=csv.QUOTE_ALL)
    return len(rows)


def main() -> int:
    feats_path = C.PATHS["output"]
    gap_path = C.PROCESSED / "borough_gap_index.csv"
    if not feats_path.exists() or not gap_path.exists():
        print("ERROR: run `python -m src.run_pipeline` then `python -m src.run_analysis` first.")
        return 1
    features = pd.read_csv(feats_path)
    gap = pd.read_csv(gap_path)
    d = gap.merge(features[["lad_code", "pct_inactive_adults", "facilities_per_10k"]],
                  on="lad_code", validate="one_to_one")
    d32 = d[~d["is_city_of_london"].astype(bool)].dropna(
        subset=["gap_index_z", "pct_inactive_adults"])

    # 1. primary validation: exact + Fisher CI + seeded bootstrap
    inf = spearman_inference(d32["gap_index_z"], d32["pct_inactive_adults"])
    boot = boot_ci(d32["gap_index_z"], d32["pct_inactive_adults"])

    # 2. incremental validity + Moran (reuse the tested module end-to-end)
    boundaries = None
    try:
        from src.pipeline.pipeline import load_geography
        _, boundaries = load_geography()
    except Exception as e:                              # noqa: BLE001
        warnings.warn(f"boundaries unavailable; Moran's I row skipped: {e}")
    res = iv_run(features, gap, boundaries)
    part = partial_spearman(d32["provision_score_z"], d32["pct_inactive_adults"],
                            d32["need_score_z"])

    # 3. facilities corroboration (with p and n — D3-1)
    dfac = d32.dropna(subset=["facilities_per_10k"])
    fac = spearman_inference(dfac["gap_index_z"], dfac["facilities_per_10k"])

    # 4. weighting sensitivity (recompute via gap_index.run — deterministic)
    from src.pipeline.gap_index import run as gap_run
    _, report = gap_run(features)
    sens = report["sensitivity_spearman_vs_base"]
    sens_min = min(sens.values())

    # 5. quadrant threshold sensitivity (B2-3) — full grid for the results
    #    file; gentle ±0.10·SD grid reported alongside, so the report can
    #    grade the claim rather than hide behind one number.
    qtable, qsum = quadrant_sensitivity(gap)
    _, qsum10 = quadrant_sensitivity(gap, deltas=(-0.10, 0.10))
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    qtable.to_csv(SENS_OUT, index=False)

    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    sha = _git_commit()
    pop32 = "London boroughs excl. City of London (n=32)"

    def row(mid: str, value, unit: str, definition: str, population: str = pop32,
            source: str = "borough_gap_index.csv + borough_features.csv",
            results_file: str = "results/metrics.csv", corroboration: str = "") -> dict:
        return {"metric_id": mid, "value": value, "population": population,
                "unit": unit, "vintage": VINTAGE, "source_dataset": source,
                "definition": definition, "script": "src/ws2_metrics.py",
                "results_file": results_file, "commit": sha, "timestamp": ts,
                "corroboration": corroboration, "verified_by": "pending four-eyes"}

    rows = [
        row("ws2.validation_rho", round(inf["r"], 4), "Spearman rho",
            "gap_index_z vs pct_inactive_adults (held-out validator, D-012)",
            corroboration="Fisher CI + seeded bootstrap agree; see companion rows"),
        row("ws2.validation_p", round(inf["p"], 4), "p (t approx, df=n-2)",
            "two-sided; matches scipy.spearmanr (asserted in tests)"),
        row("ws2.validation_n", inf["n"], "boroughs", "non-City, validator present"),
        row("ws2.validation_fisher_ci_low", round(inf["ci_low"], 3), "rho",
            "Fisher-z 95% CI lower bound"),
        row("ws2.validation_fisher_ci_high", round(inf["ci_high"], 3), "rho",
            "Fisher-z 95% CI upper bound"),
        row("ws2.validation_boot_ci_low", round(boot["ci_low"], 3), "rho",
            f"pairs bootstrap percentile 2.5%, B={boot['n_boot']}, "
            f"seed={boot['seed']} (config.RANDOM_SEED), dropped={boot['n_dropped']}"),
        row("ws2.validation_boot_ci_high", round(boot["ci_high"], 3), "rho",
            f"pairs bootstrap percentile 97.5%, B={boot['n_boot']}, "
            f"seed={boot['seed']} (config.RANDOM_SEED)"),
        row("ws2.partial_rho_provision_inactivity_given_need", round(part["r"], 4),
            "partial Spearman rho", "rank-based partial corr (D-013)"),
        row("ws2.partial_p", round(part["p"], 4), "p", "two-sided, df=n-3"),
        row("ws2.delta_r2", round(res["models"]["delta_r2"], 4), "R² increment",
            "R²(inactivity~need+provision) − R²(inactivity~need)"),
        row("ws2.nested_f_p", round(res["models"]["nested_F"]["p"], 4), "p",
            "nested-F for provision's increment (parametric; weaker of the two lenses)"),
        row("ws2.facilities_rho", round(fac["r"], 4), "Spearman rho",
            "gap_index_z vs facilities_per_10k (Active Places layer, D-011)",
            corroboration=f"DIRECTIONAL support only: p={fac['p']:.3f} at n={fac['n']} "
                          "— short of alpha=0.05; never cite the rho without this p"),
        row("ws2.facilities_p", round(fac["p"], 4), "p", "two-sided (t approx)"),
        row("ws2.sensitivity_min_spearman_vs_base", round(sens_min, 3), "Spearman rho",
            f"min rank agreement across weightings {sorted(sens)} vs base"),
        row("ws2.quadrant_stable_share", round(qsum["stable_share"], 4), "share",
            f"quadrant unchanged under all {qsum['n_combos']} threshold shifts "
            "of ±0.10/±0.25·SD on both axes (B2-3)",
            population=f"scored boroughs (n={qsum['n_scored']})",
            results_file="results/quadrant_sensitivity.csv"),
        row("ws2.quadrant_stable_share_pm10", round(qsum10["stable_share"], 4), "share",
            f"quadrant unchanged under the gentle grid (±0.10·SD only, "
            f"{qsum10['n_combos']} shifts) — cite beside the full-grid share",
            population=f"scored boroughs (n={qsum10['n_scored']})",
            results_file="results/quadrant_sensitivity.csv"),
        row("ws2.quadrant_n_switchers", qsum["n_switchers"], "boroughs",
            "boroughs whose quadrant changes under any tested shift; "
            "named with margins in the results file",
            population=f"scored boroughs (n={qsum['n_scored']})",
            results_file="results/quadrant_sensitivity.csv"),
    ]
    if res.get("moran"):
        rows += [
            row("ws2.morans_i_residuals", round(res["moran"]["I"], 4), "Moran's I",
                "residuals of inactivity ~ need + provision, queen contiguity"),
            row("ws2.morans_p", round(res["moran"]["p"], 4), "p", "normal approximation"),
        ]

    n = replace_ws2_rows(rows)

    # ---- sanity block ----
    print(f"[ws2_metrics] wrote {n} ws2.* rows -> {MANIFEST}")
    print(f"  validation: rho={inf['r']:+.4f} p={inf['p']:.4f} n={inf['n']} "
          f"Fisher[{inf['ci_low']:.3f},{inf['ci_high']:.3f}] "
          f"boot[{boot['ci_low']:.3f},{boot['ci_high']:.3f}] (B={boot['n_boot']}, seed={boot['seed']})")
    print(f"  partial rho={part['r']:+.4f} (p={part['p']:.4f}) | dR2={res['models']['delta_r2']:+.4f} "
          f"(F p={res['models']['nested_F']['p']:.4f})")
    print(f"  facilities: rho={fac['r']:+.4f} p={fac['p']:.4f} n={fac['n']} — directional only")
    print(f"  quadrants: {qsum10['stable_share']:.0%} stable at ±0.10·SD; "
          f"{qsum['stable_share']:.0%} stable over the full ±0.25·SD grid "
          f"({qsum['n_switchers']} switchers, margins in {SENS_OUT})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
