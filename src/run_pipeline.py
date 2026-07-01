"""
run_pipeline.py — build the borough feature table and write it to data/processed/.

Usage (from repo root, env active):
    python -m src.run_pipeline
"""
import sys
from src.pipeline import config as C
from src.pipeline.pipeline import build_features


def main() -> int:
    df = build_features()

    C.PATHS["output"].parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(C.PATHS["output"], index=False)

    # ---- verification printout (sanity-check before you trust it) ----
    print(f"\nWrote {C.PATHS['output']}")
    print(f"rows: {len(df)}  (expected 33: 32 boroughs + City of London)")
    print(f"cols: {len(df.columns)}")
    missing = df.isna().mean().sort_values(ascending=False)
    worst = missing[missing > 0].head(10)
    if len(worst):
        print("\nmost-incomplete columns (fraction missing):")
        for k, v in worst.items():
            print(f"  {v:5.1%}  {k}")
    else:
        print("no missing values.")

    ok = len(df) == 33
    print("\nstatus:", "OK" if ok else "CHECK — row count is not 33")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
