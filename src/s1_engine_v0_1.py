#!/usr/bin/env python3
"""
S1/S1b reconstruction engine — v0.1 PROPOSED  (M-09 / M-10 first executable)

Provenance: Michael's stream, 27 Aug 2026, AI-assisted build for the Item-1 commitment
to Fahmi (S1/S1b deterministic outputs). Status: PROPOSED, development run on
DEVELOPMENT-EXPOSED vintages only. This engine binds every inherited value to a rule id
from the M-06 inheritance-policy CANDIDATE table v0.2 (UNRATIFIED — recorded as such in
every lineage row; ratification flips the label, not the code).

Hard rules encoded:
  * H3 / sealed vintages are REFUSED by name (Fahmi §4): dev corpora must be allowlisted.
  * No generic deep merge (M-06): inheritance is whole-value, per-property, or nothing.
  * PartialSchedule is NEVER expanded (OA-1); only READY full Schedules expand.
  * Parent-not-found is classified as PARENT_NOT_IN_SAMPLE (a corpus-boundary fact),
    never as feed absence — scope qualifiers stay honest.
  * Determinism: no randomness, no wall-clock in outputs (fixed horizon anchor).

Outputs (out_dir): s1_records.jsonl (child records + field lineage), s1_summary.json,
s1b_occurrences.jsonl, s1b_summary.json, RUN_RECEIPT.json.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from collections import Counter, defaultdict
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ENGINE_VERSION = "s1-engine-0.1.0-PROPOSED"
POLICY_ID = "M06-INHERITANCE-v0.2-UNRATIFIED"
INTERP_ID = "M05-REGISTER-v0.2-UNRATIFIED"
SEALED_VINTAGE_PATTERNS = (re.compile(r"(^|[/_-])H3([/_-]|$)", re.I),)

# Properties classified for SessionSeries -> ScheduledSession (M-06 candidate rows).
# INHERITABLE_WHOLE: absent-on-child may take parent's whole value (no merge).
# CHILD_ONLY: never inherited (temporal/identity — M-06 child-only family).
INHERITABLE_WHOLE = ["name", "location", "organizer", "activity", "category",
                     "offers", "url", "attendeeInstructions", "level", "ageRange"]
CHILD_ONLY = ["startDate", "endDate", "duration", "maximumAttendeeCapacity",
              "remainingAttendeeCapacity", "@id", "identifier"]
DAY_MAP = {"https://schema.org/" + d: i for i, d in enumerate(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])}
for d, i in list(DAY_MAP.items()):
    DAY_MAP[d.rsplit("/", 1)[1]] = i  # tolerate bare day names

sha = lambda b: hashlib.sha256(b).hexdigest()


def refuse_sealed(paths):
    for p in paths:
        for pat in SEALED_VINTAGE_PATTERNS:
            if pat.search(str(p)):
                sys.exit(f"REFUSED: '{p}' matches a sealed-vintage pattern (H3). "
                         f"Development runs use exposed vintages only (Fahmi §4).")


# ---------------- Stage A: S0 fold (RPDE current state, provenance-carrying) --------
def fold_pages(files):
    state, tomb, prov = {}, set(), {}
    page_meta, order_violations = [], 0
    for f in sorted(files, key=lambda p: p.name):
        body = json.loads(Path(f).read_bytes())
        lic = body.get("license")
        page_meta.append({"file": f.name, "sha256": sha(Path(f).read_bytes()),
                          "items": len(body.get("items", [])), "license": lic})
        last_mod = None
        for it in body.get("items", []):
            iid = it.get("id")
            if iid is None:
                continue
            m = it.get("modified")
            if last_mod is not None and m is not None and m < last_mod:
                order_violations += 1          # recorded, not fatal: cross-page folds re-sort by scan order
            last_mod = m if m is not None else last_mod
            if it.get("state") == "deleted":
                state.pop(iid, None); tomb.add(iid)
            else:
                state[iid] = it
                prov[iid] = {"source_file": f.name, "rpde_id": iid,
                             "modified": it.get("modified"), "kind": it.get("kind"),
                             "page_license": lic}
    return state, tomb, prov, page_meta, order_violations


# ---------------- Stage B: S1 inheritance with field lineage ------------------------
def super_id(v):
    if isinstance(v, str): return v
    if isinstance(v, dict): return v.get("@id")
    return None


def reconstruct(children, parents_by_atid, prov):
    out, res_counter, field_counter = [], Counter(), Counter()
    for iid, it in children.items():
        d = it.get("data") or {}
        rec = {"item_id": iid, "@id": d.get("@id"), "type": d.get("@type"),
               "provenance": prov.get(iid), "fields": {}, "lineage": {}}
        sid = super_id(d.get("superEvent"))
        parent = parents_by_atid.get(sid) if sid else None
        if sid is None:
            rec["parent_resolution"] = "NO_SUPEREVENT"
        elif parent is None:
            rec["parent_resolution"] = "PARENT_NOT_IN_SAMPLE"   # corpus-boundary, NOT feed absence
        else:
            rec["parent_resolution"] = "RESOLVED"
            rec["parent_@id"] = sid
        res_counter[rec["parent_resolution"]] += 1
        pd = (parent.get("data") if parent else None) or {}
        for f in CHILD_ONLY:
            if f in d:
                rec["fields"][f] = d[f]
                rec["lineage"][f] = {"class": "ON_CHILD", "rule": "M06:child-only"}
        for f in INHERITABLE_WHOLE:
            c_has, p_has = f in d and d[f] is not None, f in pd and pd[f] is not None
            if c_has and p_has:
                cls = "BOTH_EQUAL" if d[f] == pd[f] else "CHILD_OVERRIDES"
                rec["fields"][f] = d[f]
            elif c_has:
                cls = "ON_CHILD"; rec["fields"][f] = d[f]
            elif p_has and rec["parent_resolution"] == "RESOLVED":
                cls = "INHERITED"; rec["fields"][f] = pd[f]
            elif rec["parent_resolution"] == "RESOLVED":
                cls = "SOURCE_ABSENT"
            else:
                cls = "UNRESOLVABLE_PARENT_UNAVAILABLE"
            rec["lineage"][f] = {"class": cls,
                                 "rule": f"{POLICY_ID}:SessionSeries->ScheduledSession:{f}",
                                 **({"parent_@id": sid, "parent_source":
                                     prov.get(parent["id"], {}).get("source_file")}
                                    if cls == "INHERITED" else {})}
            field_counter[(f, cls)] += 1
        out.append(rec)
    return out, res_counter, field_counter


# ---------------- Stage C: S1b schedule expansion (full Schedules only) -------------
READY_REQ = ("startDate", "endDate", "startTime", "endTime", "byDay", "scheduleTimezone")


def readiness(s):
    if not isinstance(s, dict): return ["not-an-object"]
    if (s.get("@type") or "").lower() == "partialschedule":
        return ["PartialSchedule-never-expanded(OA-1)"]
    return [k for k in READY_REQ if not s.get(k)]


def expand(series_id, s, horizon_days=28):
    tz = ZoneInfo(s["scheduleTimezone"])
    d0 = date.fromisoformat(s["startDate"])
    d1 = min(date.fromisoformat(s["endDate"]), d0 + timedelta(days=horizon_days))
    hh, mm = map(int, s["startTime"].split(":")[:2])
    days = {DAY_MAP[d] for d in s.get("byDay", []) if d in DAY_MAP}
    occ, day = [], d0
    while day <= d1:
        if day.weekday() in days:
            local = datetime.combine(day, time(hh, mm), tzinfo=tz)
            utc = local.astimezone(ZoneInfo("UTC"))
            occ.append({"series": series_id,
                        "start_local": local.isoformat(),
                        "start_utc": utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "grade": "schedule_derived",
                        "rule": f"{INTERP_ID}:expand-full-schedule"})
        day += timedelta(days=1)
    return occ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parents", nargs="+", required=True)
    ap.add_argument("--children", nargs="+", required=True)
    ap.add_argument("--out", default="s1_out")
    ap.add_argument("--horizon-days", type=int, default=28)
    a = ap.parse_args()
    refuse_sealed(a.parents + a.children)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    p_state, p_tomb, p_prov, p_pages, p_viol = fold_pages([Path(x) for x in a.parents])
    c_state, c_tomb, c_prov, c_pages, c_viol = fold_pages([Path(x) for x in a.children])
    parents_by_atid = {v["data"]["@id"]: v for v in p_state.values()
                       if isinstance(v.get("data"), dict) and v["data"].get("@id")}
    prov = {**p_prov, **c_prov}

    recs, res_c, fld_c = reconstruct(c_state, parents_by_atid, prov)
    with open(out / "s1_records.jsonl", "w") as f:
        for r in recs: f.write(json.dumps(r, ensure_ascii=False) + "\n")

    ready, not_ready, occs, suppressed = 0, Counter(), [], 0
    explicit_starts = defaultdict(set)
    for r in recs:                                    # explicit children index (collision check)
        if r.get("parent_@id") and r["fields"].get("startDate"):
            explicit_starts[r["parent_@id"]].add(str(r["fields"]["startDate"])[:16])
    for atid, p in parents_by_atid.items():
        s = p["data"].get("eventSchedule")
        for sch in (s if isinstance(s, list) else [s] if s else []):
            miss = readiness(sch)
            if miss: not_ready[tuple(sorted(miss))] += 1; continue
            ready += 1
            for o in expand(atid, sch, a.horizon_days):
                if o["start_local"][:16] in explicit_starts.get(atid, ()):  # heuristic (no idTemplate in feed) — flagged
                    o["suppressed_by_explicit"] = True; suppressed += 1
                occs.append(o)
    with open(out / "s1b_occurrences.jsonl", "w") as f:
        for o in occs: f.write(json.dumps(o) + "\n")

    s1_sum = {"engine": ENGINE_VERSION, "policy": POLICY_ID, "interpretation": INTERP_ID,
              "parents_s0": len(p_state), "children_s0": len(c_state),
              "tombstones": len(p_tomb) + len(c_tomb),
              "rpde_order_violations": p_viol + c_viol,
              "parent_resolution": dict(res_c),
              "field_lineage": {f"{f}:{c}": n for (f, c), n in sorted(fld_c.items())},
              "input_pages": p_pages + c_pages}
    (out / "s1_summary.json").write_text(json.dumps(s1_sum, indent=2))
    s1b_sum = {"schedules_ready": ready, "schedules_not_ready": {" ,".join(k): v for k, v in not_ready.items()},
               "occurrences": len(occs), "suppressed_by_explicit_heuristic": suppressed,
               "horizon_days": a.horizon_days,
               "note": "explicit-collision match is (series,start-minute) heuristic — feed publishes no idTemplate; flagged per occurrence"}
    (out / "s1b_summary.json").write_text(json.dumps(s1b_sum, indent=2))
    receipt = {"engine_sha256": sha(Path(__file__).read_bytes()),
               "engine": ENGINE_VERSION, "policy": POLICY_ID,
               "inputs": [{"file": Path(x).name, "sha256": sha(Path(x).read_bytes())}
                          for x in a.parents + a.children],
               "outputs": {n: sha((out / n).read_bytes())
                           for n in ("s1_records.jsonl", "s1_summary.json",
                                     "s1b_occurrences.jsonl", "s1b_summary.json")},
               "deterministic": True, "seed": None}
    (out / "RUN_RECEIPT.json").write_text(json.dumps(receipt, indent=2))
    print(json.dumps({"s1": s1_sum["parent_resolution"], "s1b": {"ready": ready,
          "occurrences": len(occs), "suppressed": suppressed}}, indent=1))


if __name__ == "__main__":
    main()
