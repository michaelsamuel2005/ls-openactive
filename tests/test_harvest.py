"""
test_harvest.py — synthetic-fixture tests for the scripted Open Sessions
harvester (src/harvest_open_sessions.py), covering the RPDE walk (updated /
deleted tombstones, dedup by id), the extraction/cleaning rules, and the
London boundary filter — all against hand-computed expectations.

The end-to-end proof lives elsewhere: the offline rebuild of the frozen raw
JSON reproduces london_sessions_2026-06-30.csv byte-identically (recorded in
docs/ws1_assessment_2026-07-04.md).

Run:  python -m tests.test_harvest
"""
import pathlib
import tempfile

import geopandas as gpd
from shapely.geometry import box

from src.harvest_open_sessions import clean, extract, harvest_feed, to_london


def _item(iid, lat=51.5, lon=-0.1, price=5.0, state="updated", access=None, modified=1):
    data = {
        "@id": f"https://example.org/{iid}",
        "name": f"S{iid}",
        "activity": [{"prefLabel": "Yoga"}],
        "organizer": {"name": "Org"},
        "location": {"name": f"V{iid}", "geo": {"latitude": lat, "longitude": lon},
                     "address": {"postalCode": None, "addressRegion": None}},
        "offers": [{"price": price, "priceCurrency": "GBP"}],
    }
    if access is not None:
        data["accessibilitySupport"] = access
    return {"id": iid, "state": state, "modified": modified, "data": data}


class _StubSession:
    """Canned RPDE pages: page1 (adds 1,2), page2 (tombstones 1, re-updates 2,
    adds 3), page3 (empty = live edge)."""

    def __init__(self):
        self.pages = {
            "u1": {"items": [_item(1), _item(2, price=0.0)], "next": "u2"},
            "u2": {"items": [{"id": 1, "state": "deleted", "modified": 2},
                             _item(2, price=0.0, modified=3),
                             _item(3, lat=0.0, lon=0.0)], "next": "u3"},
            "u3": {"items": [], "next": "u3"},
        }

    def get(self, url, timeout=None):
        payload = self.pages[url.split("/")[-1] if "/" in url else url]

        class R:
            def raise_for_status(self):
                pass

            def json(self, _p=payload):
                return _p

        return R()


def main():
    # ---- RPDE walk: tombstone removes 1; 2 and 3 survive ----
    live, stats = harvest_feed("u1", _StubSession(), sleep=0)
    assert set(live) == {2, 3}, live.keys()
    assert stats["seen_deleted"] == 1 and stats["seen_updated"] == 4, stats
    assert live[2]["modified"] == 3, "later update must win"

    # ---- extraction fields ----
    e = extract(_item(9, access=["wheelchair"]))
    assert e["name"] == "S9" and e["activity_type"] == "Yoga"
    assert e["organizer"] == "Org" and e["location_name"] == "V9"
    assert e["price"] == 5.0 and e["currency"] == "GBP"
    assert e["has_access_info"] is True
    assert extract(_item(9))["has_access_info"] is False

    # ---- cleaning: dedup, coord_valid, is_free ----
    recs = [
        _item(1, price=0.0),                       # free, valid coords
        _item(1, price=0.0),                       # duplicate id -> dropped
        _item(2, lat=0.0, lon=0.0),                # (0,0) -> coord_valid False
        _item(3, lat=70.0),                        # outside GB box -> False
        _item(4, price=None),                      # missing price -> NOT free
    ]
    df = clean(recs)
    assert len(df) == 4, f"dedup failed: {len(df)}"
    by = df.set_index("id")
    assert bool(by.loc[1, "coord_valid"]) and bool(by.loc[1, "is_free"])
    assert not by.loc[2, "coord_valid"] and not by.loc[3, "coord_valid"]
    assert not by.loc[4, "is_free"], "missing price must count as NOT free"

    # ---- London filter: point-in-polygon keeps only in-boundary sessions ----
    with tempfile.TemporaryDirectory() as tmp:
        bpath = pathlib.Path(tmp) / "b.geojson"
        gpd.GeoDataFrame({"LAD21CD": ["E09000002"]},
                         geometry=[box(-0.2, 51.4, 0.0, 51.6)],
                         crs="EPSG:4326").to_file(bpath, driver="GeoJSON")
        recs = [_item(1, lat=51.5, lon=-0.1),      # inside
                _item(2, lat=53.5, lon=-2.2)]      # Manchester-ish: outside
        lon = to_london(clean(recs), boundary_path=bpath)
        assert list(lon["id"]) == [1], list(lon["id"])
        assert "coord_valid" in lon.columns and "is_free" in lon.columns

    # ---- offline reproduction contract: frozen raw -> frozen CSV (documented) ----
    # (Executed as a run-level check, not a unit test: see ws1 assessment doc —
    #  byte-identical on 2026-06-30. Here we only assert clean() is deterministic.)
    d1, d2 = clean([_item(1), _item(2)]), clean([_item(1), _item(2)])
    assert d1.equals(d2)

    print("ALL ASSERTIONS PASSED ✓")


if __name__ == "__main__":
    main()
