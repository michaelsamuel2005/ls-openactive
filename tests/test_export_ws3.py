"""
test_export_ws3.py — synthetic-fixture test for the WS3 input exporter.

Two square boroughs; three sessions with known coordinates; a hand-built gap
table. Asserts the borough assignment, the equity-signal join, and the
priority flag — all against hand-computed expectations.

Run:  python -m tests.test_export_ws3
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import box

from src.export_ws3_inputs import build_ws3_inputs


def main():
    boundaries = gpd.GeoDataFrame(
        {"lad_code": ["E09000002", "E09000003"]},
        geometry=[box(0.0, 51.0, 0.1, 51.1), box(0.1, 51.0, 0.2, 51.1)],
        crs="EPSG:4326",
    )
    sessions = pd.DataFrame({
        "id": [1, 2, 3],
        "activity_type": ["Yoga", "Football", "Swim"],
        "longitude": [0.05, 0.15, 0.15],   # borough A, B, B
        "latitude": [51.05, 51.05, 51.05],
        "price": [0.0, 5.0, 12.0],
        "location_name": ["V1", "V2", "V3"],
        "has_access_info": [True, False, False],
    })
    gap = pd.DataFrame({
        "lad_code": ["E09000002", "E09000003"],
        "lad_name": ["A", "B"],
        "need_score_z": [1.0, -1.0],
        "provision_score_z": [-0.5, 0.5],
        "gap_index_z": [1.5, -1.5],
        "gap_index_rank": [1, 2],
        "gap_quadrant": ["priority", "well_served"],
    })

    out = build_ws3_inputs(sessions, boundaries, gap).set_index("id")

    assert len(out) == 3, f"expected 3 rows, got {len(out)}"
    assert out.loc[1, "lad_code"] == "E09000002"
    assert out.loc[2, "lad_code"] == "E09000003"
    assert out.loc[3, "lad_code"] == "E09000003"
    # equity signals joined correctly
    assert abs(out.loc[1, "gap_index_z"] - 1.5) < 1e-9
    assert abs(out.loc[2, "gap_index_z"] + 1.5) < 1e-9
    # priority flag follows the quadrant
    assert bool(out.loc[1, "is_priority_borough"]) is True
    assert bool(out.loc[2, "is_priority_borough"]) is False
    # original session fields survive the enrichment
    assert out.loc[1, "price"] == 0.0 and out.loc[3, "price"] == 12.0
    assert out.loc[1, "activity_type"] == "Yoga"

    print("ALL ASSERTIONS PASSED ✓")


if __name__ == "__main__":
    main()
