"""Check 2 — field lineage: separate EXTRACTION LOSS from SOURCE ABSENCE.

WHY THIS EXISTS
---------------
This is the check the whole project turns on. D-021 retired the legacy corpus because it
**could not distinguish an ecosystem defect from an extraction defect** — a field missing
from the CSV might never have been published (publication-side) or might have been thrown
away by our own pipeline (instrument-side), and with no raw retained the two were
indistinguishable forever.

The census retained raw. So the distinction is now decidable, per record, per field.

For each `ScheduledSession` child we resolve its `superEvent` pointer to the
`SessionSeries` parent captured in the same snapshot, then classify every field:

  ON_CHILD       the child itself carries the field.
  INHERITABLE    absent on the child, PRESENT on the resolved parent.
                 -> a child-only extraction DESTROYS this. INSTRUMENT-SIDE loss.
                    This is precisely what our legacy pipeline did.
  SOURCE_ABSENT  absent on child AND on parent. The ecosystem genuinely does not
                 publish it here. PUBLICATION-SIDE absence. Not our fault, and not
                 repairable by better extraction.
  UNRESOLVED     the child's superEvent target was not captured in this snapshot, so
                 nothing can be concluded. Reported, never silently folded into absence.

The blueprint's binding attribution rule: no field may be reported as "missing" without
naming which of these it is. UNRESOLVED is not evidence of absence.

CAVEAT (stated, not hidden)
---------------------------
The census captured 2 RPDE pages per feed. Parent and child pages are NOT aligned — a
child on page 1 may point at a parent on page 40, which was never fetched. So UNRESOLVED
is expected and is a property of the *snapshot*, not of the ecosystem. The INHERITABLE and
SOURCE_ABSENT rates below are therefore computed over RESOLVED children only, and that
denominator is reported everywhere. A full harvest (Deliverable 1) removes this limit.

WHAT IT WRITES
--------------
results/lineage_trace.csv    one row per (publisher, field, verdict): counts + rate
results/lineage_sample.csv   50 individual traces, so a second team member can
                             reproduce any single one by hand from data/raw/

Run:  python -m src.trace_lineage
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

# The descriptive fields a discovery query needs. `superEvent` is excluded: it is the
# join key itself, not a payload field.
FIELDS = [
    "name", "category", "activity", "offers", "organizer", "location",
    "eventSchedule", "url", "description", "ageRange", "genderRestriction",
    "level", "attendeeInstructions",
]

ON_CHILD = "ON_CHILD"
INHERITABLE = "INHERITABLE"
SOURCE_ABSENT = "SOURCE_ABSENT"
UNRESOLVED = "UNRESOLVED"


def target_of(super_event: object) -> str | None:
    """Extract the parent @id a child's superEvent points at."""
    if isinstance(super_event, str):
        return super_event
    if isinstance(super_event, dict):
        return super_event.get("@id")
    return None


def index_parents(raw_dir: Path) -> dict[str, dict]:
    """Map every captured SessionSeries parent @id -> its data payload."""
    parents: dict[str, dict] = {}
    for f in raw_dir.glob("*SessionSeries*.json"):
        try:
            page = json.loads(f.read_text())
        except (ValueError, OSError):
            continue
        for item in page.get("items", []):
            data = item.get("data")
            if isinstance(data, dict) and data.get("@id"):
                parents[data["@id"]] = data
    return parents


def classify(child: dict, parent: dict | None, field: str) -> str:
    """Decide the lineage verdict for one field of one child record."""
    if child.get(field) is not None:
        return ON_CHILD
    if parent is None:
        return UNRESOLVED
    if parent.get(field) is not None:
        return INHERITABLE
    return SOURCE_ABSENT


def main() -> None:
    """Trace field lineage across every captured ScheduledSession child."""
    dirs = sorted(Path("data/raw").glob("census_*"))
    if not dirs:
        print("no census raw directory found — run src.harvest_pilot --tag census first")
        return
    raw_dir = dirs[-1]
    print(f"lineage trace | raw -> {raw_dir}")

    parents = index_parents(raw_dir)
    print(f"  parents captured (SessionSeries with @id): {len(parents):,}")

    counts: dict[tuple[str, str, str], int] = defaultdict(int)
    samples: list[dict] = []
    n_children = 0
    n_resolved = 0

    for f in sorted(raw_dir.glob("*ScheduledSession*.json")):
        try:
            page = json.loads(f.read_text())
        except (ValueError, OSError):
            continue
        publisher = f.name.split("_ScheduledSession_")[0]
        for item in page.get("items", []):
            child = item.get("data")
            if not isinstance(child, dict):
                continue
            n_children += 1
            tgt = target_of(child.get("superEvent"))
            parent = parents.get(tgt) if tgt else None
            if parent is not None:
                n_resolved += 1
            for field in FIELDS:
                verdict = classify(child, parent, field)
                counts[(publisher, field, verdict)] += 1
            if parent is not None and len(samples) < 50:
                samples.append({
                    "publisher": publisher,
                    "child_id": child.get("@id"),
                    "parent_id": tgt,
                    "child_fields": "|".join(sorted(k for k in child if not k.startswith("@"))),
                    "parent_fields": "|".join(sorted(k for k in parent if not k.startswith("@"))),
                    "inheritable": "|".join(
                        f for f in FIELDS
                        if child.get(f) is None and parent.get(f) is not None),
                    "source_absent": "|".join(
                        f for f in FIELDS
                        if child.get(f) is None and parent.get(f) is None),
                })

    Path("results").mkdir(exist_ok=True)
    with open("results/lineage_trace.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["publisher", "field", "verdict", "n"])
        w.writeheader()
        for (pub, field, verdict), n in sorted(counts.items()):
            w.writerow({"publisher": pub, "field": field, "verdict": verdict, "n": n})
    with open("results/lineage_sample.csv", "w", newline="") as fh:
        if samples:
            w2 = csv.DictWriter(fh, fieldnames=list(samples[0].keys()))
            w2.writeheader()
            w2.writerows(samples)

    # Roll up over RESOLVED children only — the honest denominator.
    roll: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for (_pub, field, verdict), n in counts.items():
        roll[field][verdict] += n

    print(f"  children traced : {n_children:,}")
    print(f"  resolved to a captured parent : {n_resolved:,} "
          f"= {n_resolved/max(1,n_children):.1%}  (unresolved = snapshot paging, not absence)")
    print("\n" + "=" * 78)
    print("CHECK 2 — FIELD LINEAGE  (rates over RESOLVED children only)")
    print(f"{'field':22s} {'ON_CHILD':>9s} {'INHERITABLE':>12s} {'SOURCE_ABSENT':>14s}   verdict")
    print("-" * 78)
    for field in FIELDS:
        v = roll[field]
        res = v[ON_CHILD] + v[INHERITABLE] + v[SOURCE_ABSENT]
        if not res:
            continue
        inh = v[INHERITABLE] / res
        note = ""
        if inh > 0.5:
            note = "<- child-only extraction DESTROYS this (instrument-side)"
        elif v[SOURCE_ABSENT] / res > 0.5:
            note = "<- not published here (publication-side)"
        print(f"{field:22s} {v[ON_CHILD]:9,d} {v[INHERITABLE]:12,d} {v[SOURCE_ABSENT]:14,d}   {note}")
    print("=" * 78)
    print("  -> results/lineage_trace.csv (per publisher/field) "
          "· results/lineage_sample.csv (50 hand-checkable traces)")


if __name__ == "__main__":
    main()
