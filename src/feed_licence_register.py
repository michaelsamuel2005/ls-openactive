"""Per-FEED licence register, built from retained raw. Adopted from Wesley's v2 (D-028).

WHY THIS EXISTS
---------------
`src/verify_licences.py` reads the licence each **dataset site** declares. That left a real
defect (D-026 item 2): publisher `Halo` returned **HTTP 403 on its site** — licence unknown —
yet its feed data was harvested and **14 derived rows were published in this public repo**.
Site-level attribution cannot govern feed-level redistribution.

Wesley's v2 proposal specifies the correct instrument:

    "A per-feed licence register governs use: all feeds are used for analysis, but
     redistribution or republication is limited to feeds whose licences permit it, and
     per-feed attribution is carried on published outputs."

That is exactly right, and it is buildable **with no new network traffic**: every RPDE page
envelope carries its own `license` alongside `items` and `next`, and we retained the raw.
A question nobody asked at harvest time is answerable months later **only because the raw was
kept** — which is the argument D-021 makes for retiring a corpus that kept none.

NOTE ON SCOPE (honest): this reads the RETAINED ARCHIVE, so it can only speak for feeds whose
pages we actually kept. The `census` archive is 44 pages short (D-026 item 4); prefer the
`census2` archive once it exists.

WHAT IT WRITES
--------------
results/feed_licence_register.csv   one row per (publisher, kind, licence): pages, items

Run:  python -m src.feed_licence_register
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


def latest_archive() -> Path | None:
    """Prefer the collision-fixed census2 archive; fall back to census."""
    for pattern in ("census2_*", "census_*", "pilot_*"):
        dirs = sorted(Path("data/raw").glob(pattern))
        if dirs:
            return dirs[-1]
    return None


def main() -> None:
    """Extract each retained page's envelope licence and aggregate per feed."""
    raw_dir = latest_archive()
    if raw_dir is None:
        print("no retained archive found — run src.harvest_pilot first")
        return
    print(f"feed licence register | raw -> {raw_dir}")

    # (publisher, kind, licence) -> [pages, items]
    reg: dict[tuple[str, str, str], list[int]] = defaultdict(lambda: [0, 0])
    no_licence: list[str] = []

    for f in sorted(raw_dir.glob("*.json")):
        try:
            page = json.loads(f.read_text())
        except (ValueError, OSError):
            continue
        stem = f.stem
        # filenames are "<publisher>_<kind>_<digest>_p<n>[_dupN]"
        parts = stem.split("_")
        kind = next((p for p in parts if p in
                     ("SessionSeries", "ScheduledSession", "FacilityUse", "Slot",
                      "CourseInstance")), "UNKNOWN")
        publisher = stem.split(f"_{kind}_")[0] if f"_{kind}_" in stem else stem
        licence = page.get("license")
        n_items = len(page.get("items", []))
        if not licence:
            no_licence.append(f.name)
            licence = "(NONE DECLARED ON ENVELOPE)"
        entry = reg[(publisher, kind, str(licence))]
        entry[0] += 1
        entry[1] += n_items

    Path("results").mkdir(exist_ok=True)
    with open("results/feed_licence_register.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["publisher", "kind", "licence", "pages", "items"])
        w.writeheader()
        for (pub, kind, lic), (pages, items) in sorted(reg.items()):
            w.writerow({"publisher": pub, "kind": kind, "licence": lic,
                        "pages": pages, "items": items})

    lic_totals: dict[str, int] = defaultdict(int)
    for (_p, _k, lic), (_pages, items) in reg.items():
        lic_totals[lic] += items
    publishers = {p for (p, _k, _l) in reg}

    print("\n" + "=" * 74)
    print("PER-FEED LICENCE REGISTER  (from retained raw envelopes — no new requests)")
    print(f"  feeds registered : {len(reg)}  across {len(publishers)} publishers")
    print(f"  pages with NO envelope licence : {len(no_licence)}")
    for lic, items in sorted(lic_totals.items(), key=lambda x: -x[1]):
        print(f"    {items:8,d} items  {lic}")
    print("\n  REDISTRIBUTION RULE (Wesley v2, adopted): publish derived rows ONLY for feeds")
    print("  whose envelope licence permits it; carry per-feed attribution on every output.")
    print("=" * 74)
    print("  -> results/feed_licence_register.csv")


if __name__ == "__main__":
    main()
