"""
run_analysis.py — WS2 entry point.

Reads data/processed/borough_features.csv (built by the pipeline), computes the
activity-gap index, writes data/processed/borough_gap_index.csv, and prints a
readable summary: the priority boroughs, the sensitivity of the ranking, and the
validation correlations.

Usage (repo root, env active):  python -m src.run_analysis
"""
import sys
import pandas as pd
from src.pipeline import config as C
from src.pipeline.gap_index import run


def main() -> int:
    features = C.PATHS["output"]                      # borough_features.csv
    if not features.exists():
        print(f"ERROR: {features} not found. Run `python -m src.run_pipeline` first.")
        return 1

    df = pd.read_csv(features)
    out, report = run(df)

    from src.pipeline.schema import GAP_INDEX, validate
    validate(out, GAP_INDEX, "borough_gap_index")        # raises on violation

    dest = C.PROCESSED / "borough_gap_index.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(dest, index=False)

    pd.set_option("display.width", 200, "display.max_columns", 30)
    print(f"\nWrote {dest}   ({report['n_boroughs']} boroughs)")

    print("\n— Widest gaps (priority boroughs by the base weighting) —")
    cols = ["lad_code", "lad_name", "need_score_z", "provision_score_z",
            "gap_index_z", "gap_index_rank", "gap_quadrant"]
    cols = [c for c in cols if c in out.columns]
    print(out.head(10)[cols].to_string(index=False))

    print("\n— Sensitivity (Spearman of each weighting's ranking vs the base) —")
    for w, r in report["sensitivity_spearman_vs_base"].items():
        print(f"  {w:16s} {r}")
    print(f"  stable priority set (top under EVERY weighting): {report['stable_priority_boroughs']}")

    print("\n— Validation by triangulation (Spearman of gap vs independent signals) —")
    if report["validation_spearman"]:
        for s, r in report["validation_spearman"].items():
            print(f"  gap vs {s:24s} {r}   (expect positive: bigger gaps where need is higher)")
    else:
        print("  (no validation signals present in the feature table yet)")
    if report["facility_corroboration"]:
        r = report["facility_corroboration"]["spearman_gap_vs_facilities"]
        print(f"  gap vs facilities_per_10k     {r}   (expect negative: thin sessions AND thin facilities)")

    print("\nNote: z-scores standardised on non-City boroughs"
          if report["city_excluded_from_scaling"] else "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
