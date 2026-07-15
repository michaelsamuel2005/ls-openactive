"""Snapshot verification for the 2026-07-07 event harvest (D-020 evidence base).

Computes every snapshot-side statistic quoted in the condensed proposal v5.2
on data/raw/dataset_2026-07-07.csv under a STATED London bounding box, prints
a sanity block, and appends `harvest0707.*` rows to results/metrics.csv
(idempotent: existing metric_ids are never duplicated).

Vintage discipline (revision brief FIX 1): these rows are the snapshot-side
counterparts of the June-extraction figures verified by
src/verify_event_harvest.py (whose harvest date remains open finding F2).

Run:  python -m src.verify_snapshot_0707
"""

from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

SNAPSHOT = Path("data/raw/dataset_2026-07-07.csv")
METRICS = Path("results/metrics.csv")
# Stated bounds (revision brief FIX 1d): every bbox figure cites these.
BBOX = {"lat_min": 51.28, "lat_max": 51.70, "lon_min": -0.55, "lon_max": 0.30}
POPULATION = "London bbox 51.28-51.70N, -0.55-0.30E (2026-07-07 snapshot)"
VINTAGE = "event harvest snapshot 2026-07-07"


def london_subset(df: pd.DataFrame) -> pd.DataFrame:
    """Rows inside the stated London bounding box."""
    m = df["latitude"].between(BBOX["lat_min"], BBOX["lat_max"]) & df[
        "longitude"
    ].between(BBOX["lon_min"], BBOX["lon_max"])
    return df[m].copy()


def compute_metrics(sub: pd.DataFrame) -> dict[str, tuple[float, str, str]]:
    """metric_id -> (value, unit, definition) for the bbox subset."""
    names = (
        sub["name"].astype(str).str.lower().str.strip().str.replace(r"\s+", " ", regex=True)
    )
    vc = names.value_counts()
    dur_min = pd.to_timedelta(sub["duration"], errors="coerce").dt.total_seconds() / 60
    sd = pd.to_datetime(sub["startDate"], errors="coerce", utc=True)
    dow_ok = (
        sub["dayOfWeek"].astype(str).str.lower().str[:3] == sd.dt.day_name().str.lower().str[:3]
    )
    lat4, lon4 = sub["latitude"].round(4), sub["longitude"].round(4)
    coords_per_venue = sub.assign(a=lat4, o=lon4).groupby("venue")[["a", "o"]].nunique().max().max()
    venues_per_coord = sub.assign(a=lat4, o=lon4).groupby(["a", "o"])["venue"].nunique().max()
    pk = sub["adultPrice"].notna()
    free = sub["adultPrice"] == 0

    return {
        "harvest0707.london_bbox_rows": (float(len(sub)), "events", "rows inside stated bbox"),
        "harvest0707.london_bbox_venues": (float(sub["venue"].nunique()), "venues", "distinct venue names inside stated bbox"),
        "harvest0707.adultprice_present_pct": (round(pk.mean() * 100, 2), "%", "adultPrice non-null share (MNAR; never imputed)"),
        "harvest0707.free_share_all_pct": (round(free.mean() * 100, 2), "%", "adultPrice==0 share of ALL rows (dual-denominator rule)"),
        "harvest0707.free_share_priceknown_pct": (round(free.sum() / pk.sum() * 100, 2), "%", "adultPrice==0 share of price-known rows"),
        "harvest0707.remaining_eq_max_pct": (round((sub["remainingCapacity"] == sub["maximumCapacity"]).mean() * 100, 2), "%", "capacity inertness on the snapshot (no harvest timestamp)"),
        "harvest0707.top100_name_volume_pct": (round(vc.head(100).sum() / len(sub) * 100, 1), "%", "top-100 normalised name clusters, share of event volume"),
        "harvest0707.top200_name_volume_pct": (round(vc.head(200).sum() / len(sub) * 100, 1), "%", "top-200 normalised name clusters, share of event volume"),
        "harvest0707.distinct_name_clusters": (float(len(vc)), "clusters", "lower/strip/collapse-whitespace normalised names"),
        "harvest0707.duration_median_min": (round(float(dur_min.median()), 1), "minutes", "ISO-8601 durations parsed; p95 equals median (hour slots)"),
        "harvest0707.duration_parseable_pct": (round(dur_min.notna().mean() * 100, 2), "%", "ISO-8601 duration parse rate"),
        "harvest0707.startdate_timeofday_pct": (round(((sd.dt.hour + sd.dt.minute) > 0).mean() * 100, 1), "%", "startDate rows carrying a non-midnight time (temporal surfaces feasibility)"),
        "harvest0707.dayofweek_agreement_pct": (round(dow_ok.mean() * 100, 2), "%", "dayOfWeek field vs parsed startDate weekday (publisher-QA positive)"),
        "harvest0707.duplicate_ids": (float(sub["id"].duplicated().sum()), "rows", "duplicate id values inside bbox subset"),
        "harvest0707.venue_coord_conflicts": (float(max(coords_per_venue, venues_per_coord) - 1), "conflicts", "0 = every venue has one coordinate and vice versa (4 d.p.)"),
        "harvest0707.impossible_capacity_rows": (float((sub["remainingCapacity"] > sub["maximumCapacity"]).sum()), "rows", "remaining>maximum or negative capacities"),
        "harvest0707.adult_age_restriction_present_pct": (round(sub["adultAgeRestriction"].notna().mean() * 100, 2), "%", "near-empty: scorecard finding, not a product feature"),
        "harvest0707.junior_age_restriction_present_pct": (round(sub["juniorAgeRestriction"].notna().mean() * 100, 2), "%", "near-empty: scorecard finding, not a product feature"),
        "harvest0707.juniorprice_present_pct": (round(sub["juniorPrice"].notna().mean() * 100, 2), "%", "junior-price affordability reported on this subset only"),
    }


def main() -> None:
    df = pd.read_csv(SNAPSHOT, low_memory=False)
    assert len(df) == 549_169, f"snapshot row count changed: {len(df)}"
    assert "endDate" not in df.columns, "schema changed: endDate present (June-file schema?)"
    sub = london_subset(df)
    metrics = compute_metrics(sub)

    print(f"verify_snapshot_0707 | {SNAPSHOT} | {len(df)} rows | bbox rows {len(sub)}")
    for k, (v, unit, defn) in metrics.items():
        print(f"  {k} = {v} {unit}  ({defn})")

    commit = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    existing = set()
    with METRICS.open() as f:
        existing = {row[0] for row in csv.reader(f)}
    appended = 0
    with METRICS.open("a", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        for k, (v, unit, defn) in metrics.items():
            if k in existing:
                continue
            w.writerow([k, v, POPULATION, unit, VINTAGE, str(SNAPSHOT), defn,
                        "src/verify_snapshot_0707.py", "results/metrics.csv",
                        commit, ts, "June-extraction counterpart: event_harvest.* rows",
                        "pending four-eyes"])
            appended += 1
    print(f"manifest rows appended: {appended} (existing skipped: {len(metrics) - appended})")


if __name__ == "__main__":
    main()
