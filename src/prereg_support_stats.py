"""Pre-registration support statistics (v5.3 revision; D-020 evidence base).

Three numbers the condensed proposal v5.3 quotes, each computed here so the
D-016 rule holds (no document number without a generating script and a
manifest row):

1. `harvest0626.top100_name_volume_pct` — June-extraction top-100 exact-name
   coverage, the like-for-like counterpart of `harvest0707.top100_name_volume_pct`
   (the earlier 93.9% figure included four family rules and is NOT comparable).
2. `prereg.validator_morans_i_covered30` — Active Lives inactivity Moran's I
   over the queen adjacency of the 30 June-covered boroughs. The validator is
   already seen (prior-sight inventory), so computing its autocorrelation is
   not a new peek; it converts the assumed effective-n band into a partly
   computed one. The full Clifford-Richardson n_eff completes at the freeze,
   when the gap side exists.
3. `harvest0707.bbox_clip_sliver_rows` — snapshot rows in lon 0.30-0.34E,
   lat 51.28-51.70N: the territory the stated bbox clips from Havering
   (boundary reaches 0.334E). Zero rows = the bbox is a costless descriptive
   frame on this snapshot; it is never a point-in-polygon pre-filter.

Run:  python -m src.prereg_support_stats
"""

from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import geopandas as gpd
import pandas as pd

from src.incremental_validity import morans_i, queen_weights

METRICS = Path("results/metrics.csv")
NO_COVERAGE = {"Bexley", "City of London", "Haringey"}


def june_top100_pct() -> float:
    """Top-100 exact normalised-name coverage on the June London name-match."""
    a = pd.read_csv("data/external/wesley/output.csv", low_memory=False)
    feat = pd.read_csv("data/processed/borough_features.csv")
    lon = a[a["borough"].isin(feat["lad_name"])]
    names = lon["name"].astype(str).str.lower().str.strip().str.replace(r"\s+", " ", regex=True)
    return round(names.value_counts().head(100).sum() / len(lon) * 100, 1)


def validator_morans_i_covered() -> float:
    """Moran's I of pct_inactive_adults over queen adjacency, covered-30 only."""
    g = gpd.read_file("data/raw/boundaries/lad_2021_bgc.geojson")
    name_col = [c for c in g.columns if "NM" in c.upper()][0]
    f = pd.read_csv("data/processed/borough_features.csv")
    gl = g[g[name_col].isin(f["lad_name"])].merge(
        f[["lad_name", "pct_inactive_adults"]], left_on=name_col, right_on="lad_name"
    )
    gc = gl[~gl["lad_name"].isin(NO_COVERAGE)].reset_index(drop=True)
    assert len(gc) == 30, f"covered subgraph size changed: {len(gc)}"
    return round(morans_i(gc["pct_inactive_adults"].to_numpy(), queen_weights(gc.geometry))["I"], 3)


def bbox_clip_sliver_rows() -> float:
    """Snapshot rows inside the Havering sliver the stated bbox excludes."""
    b = pd.read_csv("data/raw/dataset_2026-07-07.csv", low_memory=False)
    return float(((b["latitude"].between(51.28, 51.70)) & (b["longitude"].between(0.30, 0.34))).sum())


def main() -> None:
    rows = {
        "harvest0626.top100_name_volume_pct": (
            june_top100_pct(), "London-33 name-match (June extraction, harvest date TBC - F2)", "%",
            "event harvest June extraction",
            "top-100 exact normalised name clusters, share of event volume; like-for-like counterpart of harvest0707.top100_name_volume_pct",
        ),
        "prereg.validator_morans_i_covered30": (
            validator_morans_i_covered(), "30 June-covered boroughs, queen adjacency", "Moran's I",
            "Active Lives 2024/25",
            "validator spatial autocorrelation for the effective-n bound; validator already seen (prior-sight inventory) so this is not a new peek",
        ),
        "harvest0707.bbox_clip_sliver_rows": (
            bbox_clip_sliver_rows(), "lon 0.30-0.34E, lat 51.28-51.70N (Havering sliver)", "events",
            "event harvest snapshot 2026-07-07",
            "rows the stated bbox clips from Havering territory (boundary reaches 0.334E); bbox is descriptive only, never a PIP pre-filter",
        ),
    }
    print("prereg_support_stats")
    for k, (v, pop, unit, vint, defn) in rows.items():
        print(f"  {k} = {v} {unit}  ({defn[:80]}...)")

    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with METRICS.open() as f:
        existing = {row[0] for row in csv.reader(f)}
    appended = 0
    with METRICS.open("a", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        for k, (v, pop, unit, vint, defn) in rows.items():
            if k in existing:
                continue
            w.writerow([k, v, pop, unit, vint,
                        "output.csv / borough_features.csv / lad_2021_bgc.geojson / dataset_2026-07-07.csv",
                        defn, "src/prereg_support_stats.py", "results/metrics.csv",
                        commit, ts, "", "pending four-eyes"])
            appended += 1
    print(f"manifest rows appended: {appended}")


if __name__ == "__main__":
    main()
