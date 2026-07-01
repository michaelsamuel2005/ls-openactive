"""
test_run.py — generate tiny synthetic versions of every source, point config at
them, run the pipeline, and assert it produces a sane borough_features table.

This is what lets us trust the *logic* without the real (large, private) data.
Run from repo root:  python -m tests.test_run
"""
import tempfile
import pathlib
import pandas as pd
import geopandas as gpd
from shapely.geometry import box

from src.pipeline import config as C

# three fake boroughs incl. City of London; squares in lon/lat
BOROUGHS = [("E09000001", "City of London", 0.00, 0.10),
        ("E09000002", "Barking",        0.10, 0.20),
        ("E09000003", "Barnet",         0.20, 0.30)]
LAT0, LAT1 = 51.50, 51.60


def _pt(i):  # a point safely inside borough i's square
    x0 = BOROUGHS[i][2]
    return (x0 + 0.05, 51.55)


def make_fixtures(d: pathlib.Path):
    d.mkdir(parents=True, exist_ok=True)

    # boundaries
    gdf = gpd.GeoDataFrame(
        {"LAD21CD": [b[0] for b in BOROUGHS], "LAD21NM": [b[1] for b in BOROUGHS]},
        geometry=[box(b[2], LAT0, b[3], LAT1) for b in BOROUGHS], crs="EPSG:4326")
    gdf.to_file(d / "bnd.geojson", driver="GeoJSON")

    # lookup (only used in the no-boundaries fallback)
    pd.DataFrame({"LSOA21CD": ["E01000001"], "LAD22CD": ["E09000001"],
                  "LAD22NM": ["City of London"]}).to_csv(d / "lookup.csv", index=False)

    codes = [b[0] for b in BOROUGHS]
    head = {"date": 2021, "geography": [b[1] for b in BOROUGHS], "geography code": codes}

    # census tables (borough-level 'ltla' shape)
    pd.DataFrame({**head, "Residence type: Total": [10000, 20000, 30000]}
                 ).to_csv(d / "ts001.csv", index=False)
    pd.DataFrame({**head, "Age: Total": [10000, 20000, 30000],
                  "Aged 15 years and under": [2000, 4000, 6000],
                  "Aged 16 to 19 years": [1000, 2000, 3000],
                  "Aged 20 to 64 years": [5000, 10000, 15000],
                  "Aged 65 to 69 years": [800, 1600, 2400],
                  "Aged 85 years and over": [200, 400, 600]}
                 ).to_csv(d / "ts007a.csv", index=False)
    pd.DataFrame({**head, "Disability: Total": [10000, 20000, 30000],
                  "Disabled under the Equality Act: Limited a lot": [800, 1600, 2400],
                  "Disabled under the Equality Act: Limited a little": [1200, 2400, 3600],
                  "Not disabled under the Equality Act": [8000, 16000, 24000]}
                 ).to_csv(d / "ts038.csv", index=False)
    pd.DataFrame({**head, "General health: Total": [10000, 20000, 30000],
                  "Very good health": [5000, 10000, 15000], "Good health": [3000, 6000, 9000],
                  "Fair health": [1000, 2000, 3000], "Bad health": [800, 1600, 2400],
                  "Very bad health": [200, 400, 600]}).to_csv(d / "ts037.csv", index=False)
    pd.DataFrame({**head,
                  "Economic activity status: Total: All usual residents aged 16 years and over": [10000, 20000, 30000],
                  "Economic activity status: Economically active (excluding full-time students)": [6000, 12000, 18000],
                  "Economic activity status: Economically inactive": [4000, 8000, 12000],
                  "Economic activity status: Economically inactive: Retired": [2000, 4000, 6000],
                  "Economic activity status: Economically inactive: Student": [1000, 2000, 3000],
                  "Economic activity status: Economically inactive: Other": [1000, 2000, 3000],
                  }).to_csv(d / "ts066.csv", index=False)
    pd.DataFrame({**head,
                  "Ethnic group: Total: All usual residents": [10000, 20000, 30000],
                  "Ethnic group: Asian, Asian British or Asian Welsh": [2000, 4000, 6000],
                  "Ethnic group: Asian, Asian British or Asian Welsh: Indian": [1200, 2400, 3600],
                  "Ethnic group: Asian, Asian British or Asian Welsh: Other Asian": [800, 1600, 2400],
                  "Ethnic group: Black, Black British, Black Welsh, Caribbean or African": [1000, 2000, 3000],
                  "Ethnic group: Mixed or Multiple ethnic groups": [600, 1200, 1800],
                  "Ethnic group: Mixed or Multiple ethnic groups: White and Asian": [300, 600, 900],
                  "Ethnic group: White": [6000, 12000, 18000],
                  "Ethnic group: Other ethnic group": [400, 800, 1200],
                  }).to_csv(d / "ts021.csv", index=False)

    # IoD File 10 look-alike: a multi-sheet .xlsx. 'Notes' has title rows above data;
    # 'IMD' carries the 2025-style headers plus decoy 'average rank' columns to prove
    # the reader selects 'average score' (not 'average rank') and the right rank column.
    iod_path = d / "iod.xlsx"
    with pd.ExcelWriter(iod_path, engine="openpyxl") as xl:
        pd.DataFrame({"English indices of deprivation 2025": ["Notes", "Contact: …"]}
                     ).to_excel(xl, sheet_name="Notes", index=False)
        imd = pd.DataFrame({
            "Local Authority District code (2024)": codes,
            "Local Authority District name (2024)": ["A", "B", "C"],
            "IMD - Average rank": [9000.0, 3000.0, 6000.0],           # decoy (contains 'average')
            "IMD - Rank of average rank": [260, 45, 130],             # decoy (contains 'rank of average')
            "IMD - Average score": [12.0, 30.0, 22.0],                # TARGET score
            "IMD - Rank of average score": [250, 40, 120],            # TARGET rank
        })
        # give the IMD sheet two title rows above the header, like the real workbook
        imd.to_excel(xl, sheet_name="IMD", index=False, startrow=2)
        ws = xl.book["IMD"]
        ws["A1"] = "Index of Multiple Deprivation (IMD) 2025 — Local Authority District summaries"
        ws["A2"] = "Lower-tier local authority districts"

    # Open Sessions points
    rows = []
    for i, n in enumerate([3, 10, 6]):              # sessions per borough
        x, y = _pt(i)
        for j in range(n):
            rows.append({"longitude": x, "latitude": y,
                         "price": 0 if j % 2 == 0 else 5.0,
                         "activity_type": ["Yoga", "Football", "Swim"][j % 3],
                         "location_name": f"V{i}{j%2}", "has_access_info": j % 2 == 0})
    pd.DataFrame(rows).to_csv(d / "sessions.csv", index=False)

    # Active Places facilities
    frows = []
    for i, n in enumerate([2, 5, 3]):
        x, y = _pt(i)
        for j in range(n):
            frows.append({"SiteID": f"S{i}{j//2}", "Lon": x, "Lat": y,
                          "FacilityType": ["Sports Hall", "Swimming Pool", "Grass Pitch"][j % 3],
                          "CommunityUse": j % 2 == 0})
    pd.DataFrame(frows).to_csv(d / "fac.csv", index=False)
    pd.DataFrame([{"SiteID": "S00", "Lon": 0.05, "Lat": 51.55}]).to_csv(d / "sites.csv", index=False)

    # inactivity: OHID Fingertips look-alike — spaced headers, three Sex breakdowns,
    # two time periods. Reader must keep Sex='Persons' and the LATEST period.
    # Borough 1 (E09000001): Persons 2022/23 = 22.0 (target); 2021/22 = 25.0 (older decoy).
    ft = []
    persons_latest = {codes[0]: 22.0, codes[1]: 35.0, codes[2]: 28.0}
    persons_older  = {codes[0]: 25.0, codes[1]: 37.0, codes[2]: 30.0}
    for c in codes:
        for sex, per, val in [
            ("Persons", "2021/22", persons_older[c]),
            ("Persons", "2022/23", persons_latest[c]),   # latest → chosen
            ("Male",    "2022/23", persons_latest[c] - 3),
            ("Female",  "2022/23", persons_latest[c] + 3),
        ]:
            ft.append({"Indicator Name": "Percentage of physically inactive adults",
                       "Area Code": c, "Area Name": "X", "Area Type": "Districts & UAs",
                       "Sex": sex, "Time period": per, "Value": val,
                       "Lower CI 95.0 limit": val - 4, "Upper CI 95.0 limit": val + 4})
    pd.DataFrame(ft).to_csv(d / "inact.csv", index=False)

    # PTAL points (grades as bands)
    prows = []
    for i, grade in enumerate(["6b", "3", "4"]):
        x, y = _pt(i)
        prows.append({"x": x, "y": y, "PTAL": grade})
    pd.DataFrame(prows).to_csv(d / "ptal.csv", index=False)


def point_config(d: pathlib.Path):
    C.PATHS.update({
        "lookup": d / "lookup.csv", "boundaries": d / "bnd.geojson",
        "iod_la": d / "iod.xlsx", "sessions": d / "sessions.csv",
        "ap_sites": d / "sites.csv", "ap_facilities": d / "fac.csv",
        "inactivity": d / "inact.csv", "ptal": d / "ptal.csv",
        "output": d / "out.csv",
    })
    # census_dir + flat filenames: pipeline accepts census2021-tsXXX-ltla.csv flat in census_dir
    cdir = d / "census"
    cdir.mkdir(exist_ok=True)
    for t in ["ts001", "ts007a", "ts038", "ts037", "ts066", "ts021"]:
        (cdir / f"census2021-{t}-ltla.csv").write_text((d / f"{t}.csv").read_text())
    C.PATHS["census_dir"] = cdir
    C.PTAL_CRS = "EPSG:4326"          # fixtures use lon/lat for PTAL too


def main():
    from src.pipeline.pipeline import build_features
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        make_fixtures(d)
        point_config(d)
        df = build_features()

        pd.set_option("display.width", 200, "display.max_columns", 40)
        cols = ["lad_code", "lad_name", "population", "pct_aged_65_plus", "pct_disabled",
                "pct_bad_health", "pct_econ_inactive", "pct_ethnic_minority", "imd_avg_score",
                "n_sessions", "n_venues", "pct_sessions_free", "sessions_per_10k",
                "n_facilities", "facilities_per_10k", "n_fac_sports_halls",
                "pct_inactive_adults", "mean_ptal", "is_city_of_london"]
        print(df[cols].to_string(index=False))

        # ---- assertions ----
        assert len(df) == 3, f"expected 3 boroughs, got {len(df)}"
        assert df["population"].tolist() == [10000, 20000, 30000]
        # 65+ = (800+200)/10000 = 0.10 for borough 1
        assert abs(df.loc[0, "pct_aged_65_plus"] - 0.10) < 1e-9
        # disabled = (800+1200)/10000 = 0.20
        assert abs(df.loc[0, "pct_disabled"] - 0.20) < 1e-9
        # bad+very bad health = (800+200)/10000 = 0.10
        assert abs(df.loc[0, "pct_bad_health"] - 0.10) < 1e-9
        # econ inactive = 4000/10000 = 0.40
        assert abs(df.loc[0, "pct_econ_inactive"] - 0.40) < 1e-9
        # ethnic minority = (2000+1000+600+400)/10000 = 0.40
        assert abs(df.loc[0, "pct_ethnic_minority"] - 0.40) < 1e-9
        # IoD from .xlsx: must pick 'IMD - Average score' (12.0), NOT the decoy
        # 'IMD - Average rank' (9000.0); and the matching rank-of-average-score (250).
        assert abs(df.loc[0, "imd_avg_score"] - 12.0) < 1e-9, df.loc[0, "imd_avg_score"]
        assert int(df.loc[0, "imd_rank_of_avg"]) == 250, df.loc[0, "imd_rank_of_avg"]
        # sessions assigned by point-in-polygon: 3 / 10 / 6
        assert df["n_sessions"].tolist() == [3, 10, 6]
        # free share borough 2 (10 sessions, j%2==0 -> 5 free) = 0.5
        assert abs(df.loc[1, "pct_sessions_free"] - 0.5) < 1e-9
        # per-capita: 3/10000*10000 = 3.0
        assert abs(df.loc[0, "sessions_per_10k"] - 3.0) < 1e-9
        # facilities 2/5/3
        assert df["n_facilities"].tolist() == [2, 5, 3]
        # inactivity converted to proportion
        assert abs(df.loc[0, "pct_inactive_adults"] - 0.22) < 1e-9
        # PTAL: '6b'->8, '3'->4, '4'->5
        assert df["mean_ptal"].tolist() == [8.0, 4.0, 5.0]
        assert df.loc[0, "is_city_of_london"]
        print("\nALL ASSERTIONS PASSED ✓")


if __name__ == "__main__":
    main()
