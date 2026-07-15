"""Harvest pilot — does the source data carry what the legacy CSV lost?

WHY THIS EXISTS
---------------
The legacy event corpus (`data/raw/dataset_2026-07-07.csv`, 15 flat columns) has no
`@id`, `superEvent`, organiser, activity/category vocabulary, publisher/feed identity,
RPDE `modified`/`state`, and no retained raw JSON-LD. Every diagnostic computed on it
(horizon, duplication, price/capacity missingness, taxonomy coverage) is therefore
ambiguous: the defect may belong to the OpenActive ecosystem (a *publication-process*
effect) or to our own extraction (an *instrument-side* effect). This pilot walks the
canonical catalogue and reads the raw RPDE feeds directly to find out which.

It deliberately does NOT use the `openactive` PyPI client. That client is the prime
suspect for the field loss and self-describes as "experimental" and not for use "for
critical pipelines"; inspecting the feeds through it would be asking the suspect to
testify. Plain HTTP answers "what does the ecosystem actually publish?" uncontaminated.
(The client remains an *undeclared* dependency of the legacy corpus — see F-DEP.)

WHAT IT ANSWERS
---------------
Q1 joins        Do `superEvent` pointers on children resolve to parents we harvested?
Q2 prevalence   What share of children carry `superEvent`? (Does the primary ablation exist?)
Q3 capacity     Bytes per raw item -> can a full raw-retaining harvest fit on disk?
Q4 THE BIG ONE  Do parents carry the fields the CSV lacks (category/activity, offers,
                organizer, location, eventSchedule)? Publication-side or instrument-side?

WHAT IT WRITES
--------------
data/raw/<tag>_<UTC>/             raw JSON pages, exactly as served (immutable)
results/<tag>_endpoint_log.csv    one row per endpoint: attempted/declared, status, timing
results/<tag>_field_presence.csv  one row per (publisher, kind, field): presence rate

`--tag` keeps each run's evidence separate. It defaults to "pilot", which is the
20-site stratified run D-021 cites; a wider run MUST pass a different tag rather than
overwrite that record, because a decision entry whose evidence has been clobbered is
an unresolvable citation.

Run:  python -m src.harvest_pilot --per-catalogue 5 --pages 1
      python -m src.harvest_pilot --per-catalogue 88 --pages 2 --tag census   # all 173 sites
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

CATALOGUE_COLLECTION = "https://openactive.io/data-catalogs/data-catalog-collection.jsonld"
UA = {"User-Agent": "UoB-SEMTM0044-research-pilot/0.1 (academic; MSc group project)"}
TIMEOUT = 45
PAUSE_S = 1.0  # be a polite consumer: one request per second per host

# The fields the legacy CSV lost. Presence of these on the *parent* is the headline test.
LOST_FIELDS = [
    "activity", "category", "organizer", "offers", "location",
    "name", "description", "eventSchedule", "ageRange", "genderRestriction",
    "level", "url", "attendeeInstructions", "superEvent",
]
PARENT_KINDS = {"SessionSeries", "CourseInstance", "FacilityUse"}
CHILD_KINDS = {"ScheduledSession", "Slot"}


def get(url: str) -> tuple[object, str, float]:
    """Fetch a URL. Returns (parsed-or-text, status, elapsed_seconds).

    Status mirrors the OpenActive client's vocabulary so the two are comparable:
    COMPLETE (200 + parsed), ERROR (bad status / unparseable), TIMEOUT.
    """
    t0 = time.time()
    try:
        r = requests.get(url, headers=UA, timeout=TIMEOUT)
        dt = time.time() - t0
        if r.status_code != 200:
            return None, f"ERROR_HTTP_{r.status_code}", dt
        try:
            return r.json(), "COMPLETE", dt
        except ValueError:
            return r.text, "COMPLETE_HTML", dt
    except requests.Timeout:
        return None, "TIMEOUT", time.time() - t0
    except requests.RequestException as e:
        return None, f"ERROR_{type(e).__name__}", time.time() - t0


def discover_sites() -> tuple[dict[str, list[str]], list[dict]]:
    """Walk collection -> catalogues -> dataset sites.

    Returns sites grouped BY CATALOGUE, not a flat list. This matters: each catalogue
    is a different booking platform (LeisureCloud, Legend, Bookteq, singular), and
    field-publishing behaviour is plausibly a property of the *platform's software*
    rather than of the ecosystem. Sampling the first N of a concatenated list would
    confound the two. Callers must stratify.
    """
    log: list[dict] = []
    col, status, dt = get(CATALOGUE_COLLECTION)
    log.append({"level": "collection", "url": CATALOGUE_COLLECTION, "status": status, "seconds": round(dt, 2)})
    if status != "COMPLETE":
        return {}, log

    catalogues = col.get("hasPart", [])
    by_cat: dict[str, list[str]] = {}
    for cat_url in catalogues:
        cat, status, dt = get(cat_url)
        found = cat.get("dataset", []) if status == "COMPLETE" else []
        log.append({"level": "catalogue", "url": cat_url, "status": status,
                    "seconds": round(dt, 2), "declared": len(found)})
        by_cat[cat_url] = found
        time.sleep(PAUSE_S)
    return by_cat, log


def site_feeds(site_url: str) -> tuple[dict, list[dict], str]:
    """Extract publisher metadata and feed distributions from a dataset site."""
    body, status, _ = get(site_url)
    if status not in ("COMPLETE", "COMPLETE_HTML"):
        return {}, [], status
    if isinstance(body, str):  # HTML page with embedded JSON-LD
        m = re.search(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', body, re.S)
        if not m:
            return {}, [], "ERROR_NO_JSONLD"
        try:
            body = json.loads(m.group(1))
        except ValueError:
            return {}, [], "ERROR_BAD_JSONLD"
    meta = {
        "publisher": (body.get("publisher") or {}).get("name"),
        "license": body.get("license"),
        "dataset_name": body.get("name"),
    }
    return meta, body.get("distribution", []), "COMPLETE"


def field_presence(items: list[dict]) -> tuple[dict, int]:
    """Presence rate of each lost field across the `data` payloads on one page.

    Returns (rates, n_payloads). `n_payloads` is the DENOMINATOR the rates are over, and
    it is returned rather than inferred because it is NOT `len(items)`: an RPDE page also
    carries `state: deleted` tombstones, which have no `data` and cannot be scored. Writing
    `len(items)` beside a rate computed over `len(payloads)` makes the rate unreconcilable
    from the artefact — the defect corrected in D-026.
    """
    payloads = [i["data"] for i in items if isinstance(i.get("data"), dict)]
    if not payloads:
        return {}, 0
    rates = {f: sum(1 for d in payloads if d.get(f) is not None) / len(payloads)
             for f in LOST_FIELDS}
    return rates, len(payloads)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-catalogue", type=int, default=5,
                    help="dataset sites sampled PER CATALOGUE (stratified, not first-N)")
    ap.add_argument("--pages", type=int, default=1, help="RPDE pages per feed")
    ap.add_argument("--tag", default="pilot",
                    help="names this run's artefacts; use a fresh tag to avoid "
                         "overwriting a run an adopted decision entry cites")
    args = ap.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw_dir = Path(f"data/raw/{args.tag}_{stamp}")
    raw_dir.mkdir(parents=True, exist_ok=True)
    Path("results").mkdir(exist_ok=True)

    print(f"harvest_pilot | UTC {stamp} | tag={args.tag} | raw -> {raw_dir}")
    by_cat, endpoint_log = discover_sites()
    declared_sites = sum(len(v) for v in by_cat.values())

    # STRATIFIED selection: N per catalogue/platform, so the platform is not confounded
    # with the ecosystem. Deterministic (first N per catalogue) for reproducibility.
    selected: list[tuple[str, str]] = []
    print(f"  catalogues declared: {len(by_cat)} | dataset sites declared: {declared_sites}")
    for cat_url, site_list in by_cat.items():
        take = site_list[: args.per_catalogue]
        selected.extend((cat_url, s) for s in take)
        print(f"    {cat_url.split('/')[2]:52s} declared={len(site_list):4d} selected={len(take)}")
    print(f"  attempted/declared = {len(selected)}/{declared_sites} = "
          f"{len(selected)/max(1,declared_sites):.1%}  (stratified across catalogues)")

    presence_rows: list[dict] = []
    collisions: list[dict] = []
    child_super, child_total, raw_bytes, raw_items = 0, 0, 0, 0
    parent_ids: set[str] = set()
    child_super_targets: list[str] = []
    by_kind_total: dict[str, int] = {}
    by_kind_super: dict[str, int] = {}

    for cat_url, site in selected:
        platform = cat_url.split("/")[2]
        meta, dists, status = site_feeds(site)
        endpoint_log.append({"level": "site", "url": site, "status": status, "platform": platform,
                             "publisher": meta.get("publisher"), "declared": len(dists)})
        print(f"\n  [{platform.split('.')[0][:18]:18s}] {meta.get('publisher') or site}  "
              f"[{status}]  feeds={len(dists)}")
        time.sleep(PAUSE_S)
        if status != "COMPLETE":
            continue

        for dist in dists:
            kind = dist.get("name") or dist.get("additionalType", "").split("/")[-1]
            url = dist.get("contentUrl")
            if not url or kind not in (PARENT_KINDS | CHILD_KINDS):
                # NEVER skip a declared feed silently. Wesley's v2 puts `Event` (one-off) in
                # scope; this filter would have dropped it without trace, and the feed-level
                # `attempted ÷ declared` ledger Check 1 demands would have been quietly wrong.
                # Undisclosed harvest-time loss is the defect that retired the legacy corpus
                # (D-021) — a skip is a decision and must appear in the ledger. (D-028)
                endpoint_log.append({"level": "feed", "url": url or "(no contentUrl)",
                                     "status": f"SKIPPED_KIND_{kind or 'UNDECLARED'}",
                                     "platform": platform, "publisher": meta.get("publisher"),
                                     "kind": kind})
                print(f"      {str(kind):16s} [SKIPPED — kind not in scope]")
                continue
            page_url = url
            for pg in range(args.pages):
                body, status, dt = get(page_url)
                endpoint_log.append({"level": "feed", "url": page_url, "status": status, "platform": platform,
                                     "seconds": round(dt, 2), "publisher": meta.get("publisher"), "kind": kind})
                if status != "COMPLETE":
                    print(f"      {kind:16s} [{status}]")
                    break

                items = body.get("items", [])
                blob = json.dumps(body)
                # The filename MUST be unique per (feed, page), not per (publisher, kind, page):
                # a publisher can declare several feeds of one kind, and some dataset sites
                # publish no `publisher.name` at all — both collide, and a collision silently
                # OVERWRITES retained raw. That is the same undisclosed harvest-time data loss
                # that retired the legacy corpus (D-021), so it cannot be tolerated in the
                # replacement instrument. The URL digest disambiguates. See D-026.
                page_key = hashlib.sha1(page_url.encode()).hexdigest()[:8]
                stem = re.sub(r"[^A-Za-z0-9]+", "_",
                              f"{meta.get('publisher') or 'UNNAMED'}_{kind}")[:100]
                out = raw_dir / f"{stem}_{page_key}_p{pg}.json"
                # Belt and braces: RPDE `next` cursors make page URLs unique in practice, but
                # a site CAN declare the same contentUrl in two distributions (observed:
                # Chelmsford City Sports). Never overwrite; suffix and record it instead.
                dup = 0
                while out.exists():
                    dup += 1
                    out = raw_dir / f"{stem}_{page_key}_p{pg}_dup{dup}.json"
                if dup:
                    collisions.append({"file": out.name, "feed_url": url, "page_url": page_url})
                out.write_text(blob)  # immutable raw, exactly as served
                raw_bytes += len(blob.encode())
                raw_items += len(items)

                pres, n_payloads = field_presence(items)
                for f, rate in pres.items():
                    presence_rows.append({"platform": platform, "publisher": meta.get("publisher"),
                                          "kind": kind, "field": f, "presence_rate": round(rate, 4),
                                          "n_payloads": n_payloads, "n_items": len(items),
                                          "feed_url": url, "page": pg})
                if kind in PARENT_KINDS:
                    for i in items:
                        if isinstance(i.get("data"), dict) and i["data"].get("@id"):
                            parent_ids.add(i["data"]["@id"])
                if kind in CHILD_KINDS:
                    for i in items:
                        d = i.get("data")
                        if isinstance(d, dict):
                            child_total += 1
                            by_kind_total[kind] = by_kind_total.get(kind, 0) + 1
                            se = d.get("superEvent")
                            if se:
                                child_super += 1
                                by_kind_super[kind] = by_kind_super.get(kind, 0) + 1
                                child_super_targets.append(se if isinstance(se, str) else se.get("@id", ""))
                key = {f: f"{pres.get(f,0):.0%}" for f in ("category", "activity", "offers", "organizer", "superEvent")}
                print(f"      {kind:16s} [{status}] items={len(items):4d}  {key}")

                page_url = body.get("next")
                if not page_url or page_url == url:
                    break
                time.sleep(PAUSE_S)

    with open(f"results/{args.tag}_endpoint_log.csv", "w", newline="") as f:
        cols = ["level", "url", "status", "seconds", "platform", "publisher", "kind", "declared"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(endpoint_log)
    with open(f"results/{args.tag}_field_presence.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["platform", "publisher", "kind", "field",
                                          "presence_rate", "n_payloads", "n_items",
                                          "feed_url", "page"])
        w.writeheader()
        w.writerows(presence_rows)

    resolvable = sum(1 for t in child_super_targets if t in parent_ids)
    print("\n" + "=" * 72)
    print("PILOT FINDINGS")
    print(f"  Q1 joins       : {resolvable}/{len(child_super_targets)} sampled superEvent targets resolve "
          f"to parents harvested on page 1 (low is expected: page 1 of each feed is not aligned)")
    print(f"  Q2 prevalence  : {child_super}/{child_total} child records carry superEvent "
          f"= {child_super/max(1,child_total):.1%} (all child kinds)")
    for k in sorted(by_kind_total):
        print(f"                   {k:18s} {by_kind_super.get(k,0):5d}/{by_kind_total[k]:5d} "
              f"= {by_kind_super.get(k,0)/max(1,by_kind_total[k]):6.1%}  <- per-kind is the honest denominator")
    print(f"  Q3 capacity    : {raw_bytes/max(1,raw_items):,.0f} bytes/item raw; "
          f"{raw_bytes/1e6:.1f} MB for {raw_items:,} items "
          f"-> ~{raw_bytes/max(1,raw_items)*7.9e6/1e9:.1f} GB to retain 7.9M items")
    print(f"  Q4 fields      : see results/{args.tag}_field_presence.csv "
          "(parent presence of category/activity/offers/organizer = the headline)")
    print(f"  raw retained   : {raw_items:,} items across "
          f"{len(list(raw_dir.glob('*.json')))} files; filename collisions handled: {len(collisions)} "
          f"(0 pages lost — collisions are suffixed, never overwritten)")
    print(f"  endpoints      : {len(endpoint_log)} logged; statuses "
          f"{ {s: sum(1 for e in endpoint_log if e['status']==s) for s in {e['status'] for e in endpoint_log}} }")
    print("=" * 72)

    # Every headline figure MUST be a committed artefact, not stdout. K6 fired (D-026)
    # precisely because these numbers lived only in a terminal and `*.log` is gitignored,
    # leaving them unreconcilable from any committed file. One row per metric, so a
    # non-author can check any claim without re-running a live change feed.
    summary = [
        {"metric": "sites.declared", "value": declared_sites, "denominator": "",
         "note": "dataset sites declared by the 4 catalogues"},
        {"metric": "sites.attempted", "value": len(selected), "denominator": declared_sites,
         "note": "attempted/declared — coverage of SITES, never of records"},
        {"metric": "endpoints.logged", "value": len(endpoint_log), "denominator": "",
         "note": "every endpoint carries a status"},
        {"metric": "endpoints.failed", "value": sum(1 for e in endpoint_log
                                                    if e["status"] not in ("COMPLETE", "COMPLETE_HTML")),
         "denominator": len(endpoint_log), "note": "failed reads never become zeroes"},
        {"metric": "raw.items", "value": raw_items, "denominator": "",
         "note": "items across all retained pages (INCLUDES deleted tombstones)"},
        {"metric": "raw.files", "value": len(list(raw_dir.glob("*.json"))), "denominator": "",
         "note": "retained raw pages on disk"},
        {"metric": "raw.collisions_suffixed", "value": len(collisions), "denominator": "",
         "note": "filename collisions suffixed, never overwritten (0 pages lost)"},
        {"metric": "raw.bytes_per_item", "value": round(raw_bytes / max(1, raw_items)),
         "denominator": "", "note": "for the capacity plan"},
        {"metric": "capacity.gb_for_7.9m_items",
         "value": round(raw_bytes / max(1, raw_items) * 7.9e6 / 1e9, 1), "denominator": "",
         "note": "extrapolated; 7.9M is the DIP's published opportunity count"},
        {"metric": "joins.superEvent_resolvable", "value": resolvable,
         "denominator": len(child_super_targets),
         "note": "floor, not a rate: parent/child pages are not aligned in this snapshot"},
    ]
    for k in sorted(by_kind_total):
        summary.append({"metric": f"superEvent.prevalence.{k}", "value": by_kind_super.get(k, 0),
                        "denominator": by_kind_total[k],
                        "note": "PER-KIND is the only honest denominator; never pool across kinds"})
    with open(f"results/{args.tag}_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["metric", "value", "denominator", "note"])
        w.writeheader()
        w.writerows(summary)
    print(f"  -> results/{args.tag}_summary.csv  (every headline figure, as an artefact)")


if __name__ == "__main__":
    sys.exit(main())
