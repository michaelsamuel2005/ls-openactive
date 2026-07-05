"""
harvest_open_sessions.py — scripted, parameterised Open Sessions harvester
(WS1 gap 2: the harvest logic previously lived only in notebooks/data_audit.ipynb;
this is a faithful port of that notebook's cells, so the frozen artefacts are
reproducible by script).

Modes
  LIVE     python -m src.harvest_open_sessions                 # walk the RPDE feed (network)
  OFFLINE  python -m src.harvest_open_sessions --from-raw data/raw/session_series_raw_2026-06-30.json
           # rebuild the processed London CSV + reports from a saved raw harvest —
           # used to PROVE the frozen CSV regenerates from the frozen raw JSON.

The frozen 2026-06-30 snapshot remains the authoritative analysis input (D-015);
a live run creates a NEW dated snapshot and never overwrites an old one.
Licence: feed is CC-BY 4.0 — attribution required on published outputs.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW, PROCESSED = ROOT / "data" / "raw", ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
LONDON_BOUNDARY = ROOT / "data" / "external" / "london_lad_2021.geojson"
SESSION_SERIES_URL = "https://opensessions.io/api/rpde/session-series"
WORKING_CRS = "EPSG:27700"

# ------------------------------------------------------------------ extraction
# Faithful port of data_audit.ipynb cells 10/12 — do not "improve" silently:
# any change alters the frozen artefact's definition (log a decision first).

def g(obj, *keys, default=None):
    """Safely walk nested dicts (and lists by int index)."""
    cur = obj
    for k in keys:
        if isinstance(cur, dict):
            cur = cur.get(k)
        elif isinstance(cur, list) and isinstance(k, int) and -len(cur) <= k < len(cur):
            cur = cur[k]
        else:
            return default
        if cur is None:
            return default
    return cur


def first_activity(data):
    acts = g(data, "activity", default=[])
    if isinstance(acts, list) and acts:
        return g(acts[0], "prefLabel") or g(acts[0], "name")
    if isinstance(acts, dict):
        return g(acts, "prefLabel") or g(acts, "name")
    return None


def first_offer_price(data):
    offers = g(data, "offers", default=[])
    if isinstance(offers, list) and offers:
        return g(offers[0], "price"), g(offers[0], "priceCurrency")
    if isinstance(offers, dict):
        return g(offers, "price"), g(offers, "priceCurrency")
    return None, None


def extract(item: dict) -> dict:
    data = item.get("data", {}) or {}
    price, currency = first_offer_price(data)
    acc = g(data, "accessibilitySupport") or g(data, "accessibilityInformation")
    return {
        "id": item.get("id"),
        "oa_id": g(data, "@id"),
        "name": g(data, "name"),
        "activity_type": first_activity(data),
        "organizer": (g(data, "organizer", "name") or g(data, "organiser", "name")
                      or g(data, "provider", "name")),
        "location_name": g(data, "location", "name"),
        "latitude": g(data, "location", "geo", "latitude"),
        "longitude": g(data, "location", "geo", "longitude"),
        "postcode": g(data, "location", "address", "postalCode"),
        "region": g(data, "location", "address", "addressRegion"),
        "price": price,
        "currency": currency,
        "max_capacity": g(data, "maximumAttendeeCapacity"),
        "has_access_info": acc is not None,
        "modified": item.get("modified"),
    }


def clean(records: list[dict]) -> pd.DataFrame:
    """Extraction + numeric coercion + id de-dup + coord validity + is_free."""
    df = pd.DataFrame([extract(it) for it in records])
    for col in ["latitude", "longitude", "price", "max_capacity"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.drop_duplicates(subset="id").reset_index(drop=True)
    not_null = df["latitude"].notna() & df["longitude"].notna()
    not_zero = ~((df["latitude"].abs() < 1e-6) & (df["longitude"].abs() < 1e-6))
    in_gb = df["latitude"].between(49.0, 61.0) & df["longitude"].between(-8.5, 2.0)
    df["coord_valid"] = not_null & not_zero & in_gb
    df["is_free"] = df["price"].apply(lambda x: bool(x == 0) if pd.notna(x) else False)
    return df


def to_london(df: pd.DataFrame, boundary_path: Path = LONDON_BOUNDARY) -> pd.DataFrame:
    """Boundary filter: valid-coord sessions within any London LAD (EPSG:27700 join)."""
    boroughs = gpd.read_file(boundary_path).to_crs(WORKING_CRS)
    sv = df[df["coord_valid"]].copy()
    pts = gpd.GeoDataFrame(sv, geometry=gpd.points_from_xy(sv["longitude"], sv["latitude"]),
                           crs="EPSG:4326").to_crs(WORKING_CRS)
    joined = gpd.sjoin(pts, boroughs, how="inner", predicate="within")
    keep = [c for c in joined.columns if c in df.columns]
    return pd.DataFrame(joined[keep]).reset_index(drop=True)


# ------------------------------------------------------------------ live harvest
def harvest_feed(start_url: str, session, max_pages=20000, sleep=0.25) -> tuple[dict, dict]:
    """RPDE walk to the live edge: apply 'updated', drop 'deleted' tombstones."""
    current: dict = {}
    seen_updated = seen_deleted = pages = 0
    url, last_url = start_url, None
    while url and url != last_url and pages < max_pages:
        resp = session.get(url, timeout=60)
        resp.raise_for_status()
        payload = resp.json()
        items = payload.get("items", [])
        if not items:
            break
        for item in items:
            iid = item.get("id")
            if iid is None:
                continue
            if item.get("state") == "updated":
                current[iid] = item
                seen_updated += 1
            elif item.get("state") == "deleted":
                current.pop(iid, None)
                seen_deleted += 1
        nxt = payload.get("next")
        last_url, url = url, (urljoin(url, nxt) if nxt else None)
        pages += 1
        if sleep:
            time.sleep(sleep)
    return current, {"pages": pages, "seen_updated": seen_updated,
                     "seen_deleted": seen_deleted, "live_count": len(current)}


def _reports(df: pd.DataFrame, tag: str) -> None:
    key = ["name", "activity_type", "organizer", "location_name", "latitude",
           "longitude", "postcode", "price", "max_capacity", "has_access_info"]
    comp = pd.DataFrame({
        "field": key,
        "pct_present": [df[c].mean() * 100 if c == "has_access_info"
                        else df[c].notna().mean() * 100 for c in key],
    }).sort_values("pct_present", ascending=False)
    REPORTS.mkdir(exist_ok=True)
    comp.to_csv(REPORTS / f"field_completeness_{tag}.csv", index=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-raw", type=Path, default=None,
                    help="rebuild from a saved raw JSON instead of the network")
    ap.add_argument("--tag", default=None, help="date tag for outputs (default: raw file's/today)")
    ap.add_argument("--force", action="store_true",
                    help="allow overwriting an existing processed output (default: refuse — "
                         "frozen snapshots must never be silently regenerated in place)")
    args = ap.parse_args()

    if args.from_raw:
        records = json.load(open(args.from_raw))
        tag = args.tag or "".join(ch for ch in args.from_raw.stem if ch.isdigit() or ch == "-")[-10:]
        print(f"OFFLINE rebuild from {args.from_raw} ({len(records)} live records), tag={tag}")
    else:
        import requests
        from requests.adapters import HTTPAdapter
        try:
            from urllib3.util import Retry
        except Exception:  # pragma: no cover
            from urllib3.util.retry import Retry
        s = requests.Session()
        s.headers.update({"User-Agent": "ls-openactive-ws1/0.2 (UoB MSc group project)"})
        s.mount("https://", HTTPAdapter(max_retries=Retry(
            total=5, backoff_factor=1.0, status_forcelist=[429, 500, 502, 503, 504])))
        live, stats = harvest_feed(SESSION_SERIES_URL, s)
        records = list(live.values())
        tag = args.tag or date.today().isoformat()
        RAW.mkdir(parents=True, exist_ok=True)
        raw_path = RAW / f"session_series_raw_{tag}.json"
        json.dump(records, open(raw_path, "w"))
        print(f"LIVE harvest: {stats} -> {raw_path}")

    df = clean(records)
    london = to_london(df)
    out = PROCESSED / f"london_sessions_{tag}.csv"
    if out.exists() and not args.force:
        print(f"REFUSING to overwrite existing {out} — frozen snapshots are never "
              f"regenerated in place. Use a different --tag (or --force deliberately).")
        return 1
    PROCESSED.mkdir(parents=True, exist_ok=True)
    london.to_csv(out, index=False)
    _reports(df, tag)

    print(f"national live={len(df)}  london={len(london)}  free(L)={int(london['is_free'].sum())}"
          f"  venues(L)={london['location_name'].nunique()}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
