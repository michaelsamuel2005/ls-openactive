"""
export_ws3_inputs.py — build the WS3 data-contract artefact (docs/ws3-recommender-spec.md §2).

Joins the frozen London SessionSeries snapshot to its borough (the same verified
point-in-polygon assignment the pipeline uses) and to the WS2 equity signals
(gap index, quadrant), producing ONE self-contained input file for the
recommender:  data/processed/ws3_sessions_enriched.csv

Run:   python -m src.export_ws3_inputs
Needs: data/processed/london_sessions_2026-06-30.csv (frozen snapshot),
       data/processed/borough_gap_index.csv (from src.run_analysis),
       boundary file per config. Shared with the team via OneDrive (data/ is
       git-ignored — never commit the artefact).
"""
from __future__ import annotations

import sys

import pandas as pd

from .pipeline import config as C
from .pipeline.pipeline import _assign_to_borough, load_geography

GAP_COLS = ["lad_code", "lad_name", "need_score_z", "provision_score_z",
            "gap_index_z", "gap_index_rank", "gap_quadrant"]
OUT = C.PROCESSED / "ws3_sessions_enriched.csv"


def build_ws3_inputs(sessions: pd.DataFrame, boundaries, gap: pd.DataFrame) -> pd.DataFrame:
    """Enrich session rows with borough assignment and WS2 equity signals.

    sessions:   raw London SessionSeries rows (lon/lat in WGS84).
    boundaries: GeoDataFrame[lad_code, geometry] (any CRS; reprojected inside).
    gap:        borough_gap_index table (GAP_COLS subset used).
    Returns one row per input session; sessions failing the spatial join are
    dropped (counted by the caller's sanity block).
    """
    s = C.SESSIONS_COLS
    df = _assign_to_borough(sessions, s["lon"], s["lat"], C.SESSIONS_CRS, boundaries)
    df = df.dropna(subset=["lad_code"]).drop(columns=["geometry"], errors="ignore")
    g = gap[[c for c in GAP_COLS if c in gap.columns]].copy()
    out = df.merge(g, on="lad_code", how="left", suffixes=("", "_gap"))
    out["is_priority_borough"] = out["gap_quadrant"].eq("priority")
    return pd.DataFrame(out)


def main() -> int:
    sessions_path = C.PATHS["sessions"]
    gap_path = C.PROCESSED / "borough_gap_index.csv"
    for p in (sessions_path, gap_path):
        if not p.exists():
            print(f"ERROR: {p} not found. Run the pipeline/analysis first.")
            return 1

    sessions = pd.read_csv(sessions_path)
    gap = pd.read_csv(gap_path)
    _, boundaries = load_geography()
    out = build_ws3_inputs(sessions, boundaries, gap)

    from .pipeline.schema import LONDON_SESSIONS, WS3_ENRICHED, validate
    validate(sessions, LONDON_SESSIONS, "london_sessions (input)")
    validate(out, WS3_ENRICHED, "ws3_sessions_enriched")

    out.to_csv(OUT, index=False)

    # ---- sanity block (eyeball before trusting) ----
    n_in, n_out = len(sessions), len(out)
    print(f"Wrote {OUT}")
    print(f"rows in/out: {n_in} -> {n_out}  (dropped by spatial join: {n_in - n_out})")
    print(f"boroughs represented: {out['lad_code'].nunique()}  "
          f"priority-borough sessions: {int(out['is_priority_borough'].sum())}")
    print(f"gap join complete: {out['gap_index_z'].notna().mean()*100:.1f}% "
          f"(City sessions would be NaN — expected 0 of them)")
    print(f"free share: {pd.to_numeric(out['price'], errors='coerce').eq(0).mean()*100:.1f}%  "
          f"(expect 43.9)")
    ok = n_out == n_in and out["lad_code"].notna().all()
    print("status:", "OK" if ok else "CHECK — row loss or unassigned boroughs")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
