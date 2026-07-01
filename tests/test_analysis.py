"""
test_analysis.py — verify the WS2 gap-index analysis on a synthetic feature table
with a known need/provision gradient.

Construction: boroughs B2..B8 have steadily INCREASING need (deprivation + demographics:
disability, bad health, age, economic inactivity) and steadily DECREASING community-session
provision. So the gap must rise monotonically and the worst borough must be 'priority'.
Adult inactivity ALSO rises across B2..B8, but under D-012 it is HELD OUT of the need
composite: it is the independent validation outcome, so the gap must correlate positively
with it WITHOUT it ever entering the need score (proven below by a perturbation check).
City of London is added as a low-need / inflated-provision outlier.

Run:  python -m tests.test_analysis
"""
import pandas as pd
from src.pipeline.gap_index import run


def make_features() -> pd.DataFrame:
    rows = [dict(lad_code="E09000001", lad_name="City of London", population=10_000,
                 imd_avg_score=12.0, pct_inactive_adults=0.18, pct_disabled=0.10,
                 pct_bad_health=0.08, pct_aged_65_plus=0.10, pct_econ_inactive=0.30,
                 sessions_per_10k=20.0, facilities_per_10k=10.0, is_city_of_london=True)]
    for i in range(7):                       # B2..B8
        rows.append(dict(
            lad_code=f"E0900000{i+2}", lad_name=f"Borough{i+2}", population=200_000,
            imd_avg_score=10 + i * 5,
            pct_inactive_adults=0.20 + i * 0.03,
            pct_disabled=0.10 + i * 0.02,
            pct_bad_health=0.06 + i * 0.015,
            pct_aged_65_plus=0.10 + i * 0.015,
            pct_econ_inactive=0.30 + i * 0.02,
            sessions_per_10k=6.0 - i * 0.8,          # provision falls as need rises
            facilities_per_10k=5.0 - i * 0.6,        # compounded
            is_city_of_london=False))
    return pd.DataFrame(rows)


def main():
    out, report = run(make_features())

    pd.set_option("display.width", 200, "display.max_columns", 30)
    show = ["lad_code", "need_score_z", "provision_score_z", "gap_index_z",
            "gap_index_rank", "gap_quadrant", "is_city_of_london"]
    print(out[show].to_string(index=False))
    print("\nreport:")
    for k, v in report.items():
        print(f"  {k}: {v}")

    by_code = out.set_index("lad_code")

    # ---- assertions ----
    assert len(out) == 8
    # worst borough (highest need, lowest provision) is B8 and is the widest gap
    assert by_code.loc["E09000008", "gap_index_rank"] == 1
    assert by_code.loc["E09000008", "gap_quadrant"] == "priority"
    # the low-need / high-provision end is well served
    assert by_code.loc["E09000002", "gap_quadrant"] == "well_served"
    # gap == need - provision (identity check on one row)
    r = by_code.loc["E09000005"]
    assert abs(r["gap_index_z"] - (r["need_score_z"] - r["provision_score_z"])) < 1e-9
    # validation by HELD-OUT signals only (D-012): inactivity is held out of need, so it is a
    # legitimate independent anchor; deprivation is a need INPUT and must not appear here.
    v = report["validation_spearman"]
    assert "imd_avg_score" not in v, f"deprivation is a need input; it must not be a validation anchor: {v}"
    assert v["pct_inactive_adults"] > 0.8, v
    # facility corroboration: thin sessions coincide with thin facilities (negative)
    assert report["facility_corroboration"]["spearman_gap_vs_facilities"] < 0
    # sensitivity: alternative weightings barely move the ranking here
    assert all(s > 0.8 for s in report["sensitivity_spearman_vs_base"].values())
    # City of London handled as a flagged outlier, not a priority borough
    assert by_code.loc["E09000001", "is_city_of_london"]
    assert by_code.loc["E09000001", "gap_quadrant"] != "priority"

    # ---- D-012 held-out proof: inactivity must NOT influence the need score or the gap ----
    # Reverse the inactivity column and re-run. If inactivity had leaked into need, the gap
    # index would move; held out, it must be numerically identical — it can only validate.
    perturbed = make_features()
    perturbed["pct_inactive_adults"] = list(reversed(perturbed["pct_inactive_adults"].tolist()))
    out_p, _ = run(perturbed)
    base_gap = by_code["gap_index_z"].sort_index()
    pert_gap = out_p.set_index("lad_code")["gap_index_z"].sort_index()
    assert ((base_gap - pert_gap).abs() < 1e-9).all(), \
        "reversing inactivity changed the gap index — it is leaking into need (D-012 violated)"

    print("\nALL ASSERTIONS PASSED ✓")


if __name__ == "__main__":
    main()
