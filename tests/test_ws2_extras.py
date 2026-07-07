"""
test_ws2_extras.py — tests for src/ws2_metrics.py (bootstrap CI, quadrant
threshold sensitivity, manifest replace-own-prefix discipline).

Run:  python -m tests.test_ws2_extras
"""
from __future__ import annotations

import pathlib
import tempfile

import numpy as np
import pandas as pd

from src.ws2_metrics import (MANIFEST_COLS, boot_ci, quadrant_sensitivity,
                             replace_ws2_rows)


def test_bootstrap() -> None:
    rng = np.random.default_rng(0)
    x = np.arange(40, dtype=float)
    y = x + rng.normal(0, 6, 40)          # strongly monotone + noise

    a = boot_ci(x, y, n_boot=800, seed=7)
    b = boot_ci(x, y, n_boot=800, seed=7)
    assert a == b, "same seed must give identical bounds (determinism)"

    c = boot_ci(x, y, n_boot=800, seed=8)
    assert c != a, "different seed should not give byte-identical bounds"

    assert a["ci_low"] <= a["point"] <= a["ci_high"], "CI must bracket the point estimate"
    assert a["ci_low"] > 0, "clearly positive association: lower bound above zero"
    assert a["n_dropped"] == 0, "no degenerate resamples expected on continuous data"
    print(f"  boot: point={a['point']:.3f} CI=[{a['ci_low']:.3f},{a['ci_high']:.3f}] ✓")


def test_quadrant_sensitivity() -> None:
    # Symmetric fixture: medians land exactly at (0, 0) BETWEEN data points.
    # Four corners at ±2 (never switch; max tested shift is ±0.25·SD ≈ ±0.41);
    # two near-median rows at need ±0.05 (must switch under ±0.10·SD ≈ ±0.16);
    # one City-style unscored row (excluded).
    g = pd.DataFrame({
        "lad_code": [f"E0900000{i}" for i in range(1, 8)],
        "lad_name": ["A", "B", "C", "D", "Edge", "Anti", "City"],
        "need_score_z":      [ 2.0, 2.0, -2.0, -2.0,  0.05, -0.05, 0.5],
        "provision_score_z": [-2.0, 2.0, -2.0,  2.0, -2.0,   2.0,  None],
        "gap_quadrant": ["priority", "high_need_served", "low_low",
                         "well_served", "priority", "well_served", None],
        "is_city_of_london": [False] * 6 + [True],
    })
    table, summary = quadrant_sensitivity(g)
    assert summary["n_scored"] == 6
    assert summary["n_combos"] == 24, "5x5 shift grid minus the (0,0) base"
    edge = table.loc[table.lad_name.eq("Edge")].iloc[0]
    anti = table.loc[table.lad_name.eq("Anti")].iloc[0]
    assert edge["n_switches"] > 0 and "low_low" in edge["alternate_quadrants"]
    assert anti["n_switches"] > 0 and "high_need_served" in anti["alternate_quadrants"]
    stable = table[table.lad_name.isin(["A", "B", "C", "D"])]
    assert (stable["n_switches"] == 0).all(), "clean corners must never switch"
    assert abs(summary["stable_share"] - 4 / 6) < 1e-9
    assert pd.isna(table.loc[table.lad_name.eq("City"), "gap_quadrant"].iloc[0])
    print(f"  quadrants: stable_share={summary['stable_share']:.2f}, "
          f"switchers={summary['switchers']} ✓")

    # base-reproduction guard: a wrong committed column must raise
    bad = g.assign(gap_quadrant=["low_low"] * 6 + [None])
    try:
        quadrant_sensitivity(bad)
        raise AssertionError("mismatched committed quadrants should raise")
    except AssertionError as e:
        assert "does not reproduce" in str(e)
    print("  base-reproduction guard raises on mismatch ✓")


def test_manifest_replace() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        p = pathlib.Path(tmp) / "metrics.csv"
        seed_rows = pd.DataFrame([
            {c: "x" for c in MANIFEST_COLS} | {"metric_id": "ws1.keep_me", "value": "1"},
            {c: "x" for c in MANIFEST_COLS} | {"metric_id": "ws2.stale", "value": "999"},
        ])
        seed_rows.to_csv(p, index=False)

        new = [{c: "y" for c in MANIFEST_COLS} | {"metric_id": "ws2.fresh", "value": "42"}]
        n = replace_ws2_rows(new, manifest_path=p)
        out = pd.read_csv(p, dtype=str)

        assert n == 1
        assert "ws1.keep_me" in set(out.metric_id), "other prefixes untouched"
        assert "ws2.stale" not in set(out.metric_id), "old ws2 rows replaced"
        assert "ws2.fresh" in set(out.metric_id)
        assert list(out.columns) == MANIFEST_COLS, "column contract preserved"

        # ownership guard: refuse to write a row outside the ws2. prefix
        try:
            replace_ws2_rows([{c: "z" for c in MANIFEST_COLS}
                              | {"metric_id": "ws1.hijack"}], manifest_path=p)
            raise AssertionError("non-ws2 row should be refused")
        except ValueError:
            pass
    print("  manifest: replace-own-prefix + ownership guard ✓")


def main() -> int:
    print("test_ws2_extras:")
    test_bootstrap()
    test_quadrant_sensitivity()
    test_manifest_replace()
    print("\nALL ASSERTIONS PASSED ✓")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
