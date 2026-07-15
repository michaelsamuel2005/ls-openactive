"""Verify the licence every OpenActive dataset site declares.

WHY THIS EXISTS
---------------
D-021 and PR #6 both assert "all CC-BY 4.0" of the harvested feeds. That claim was
**not traceable to any artefact**: `src/harvest_pilot.py` reads each dataset site's
`license` field in `site_feeds()` and then discards it — `results/*_endpoint_log.csv`
has no licence column. Under this project's rules a claim in a decision entry must be
computed by code here and traceable to a results file, so the assertion was unsupported.

It also matters legally, not just bibliographically. This repository is **public** and
distributes derivatives of these feeds (`results/census_*.csv`, `reports/*.csv`).
CC-BY 4.0 permits that **only with attribution**. To attribute correctly we must first
know, per publisher, what licence was actually declared — not assume one.

WHAT IT WRITES
--------------
results/licence_audit.csv   one row per declared dataset site:
                            catalogue, site, publisher, licence URL, status

Run:  python -m src.verify_licences
"""

from __future__ import annotations

import csv
import json
import re
import sys
import time
from pathlib import Path

import requests

CATALOGUE_COLLECTION = "https://openactive.io/data-catalogs/data-catalog-collection.jsonld"
UA = {"User-Agent": "UoB-SEMTM0044-research-pilot/0.1 (academic; MSc group project)"}
TIMEOUT = 45
PAUSE_S = 1.0


def fetch(url: str) -> tuple[object, str]:
    """Fetch a URL, returning (parsed-or-text, status)."""
    try:
        r = requests.get(url, headers=UA, timeout=TIMEOUT)
        if r.status_code != 200:
            return None, f"ERROR_HTTP_{r.status_code}"
        try:
            return r.json(), "COMPLETE"
        except ValueError:
            return r.text, "COMPLETE_HTML"
    except requests.Timeout:
        return None, "TIMEOUT"
    except requests.RequestException as e:
        return None, f"ERROR_{type(e).__name__}"


def site_licence(site_url: str) -> tuple[str | None, str | None, str]:
    """Return (publisher_name, licence_url, status) for one dataset site."""
    body, status = fetch(site_url)
    if status not in ("COMPLETE", "COMPLETE_HTML"):
        return None, None, status
    if isinstance(body, str):
        m = re.search(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', body, re.S)
        if not m:
            return None, None, "ERROR_NO_JSONLD"
        try:
            body = json.loads(m.group(1))
        except ValueError:
            return None, None, "ERROR_BAD_JSONLD"
    publisher = (body.get("publisher") or {}).get("name")
    return publisher, body.get("license"), "COMPLETE"


def main() -> None:
    """Walk the canonical collection and record each site's declared licence."""
    col, status = fetch(CATALOGUE_COLLECTION)
    if status != "COMPLETE":
        print(f"collection unreachable: {status}")
        sys.exit(1)

    rows: list[dict] = []
    for cat_url in col.get("hasPart", []):
        cat, status = fetch(cat_url)
        sites = cat.get("dataset", []) if status == "COMPLETE" else []
        print(f"{cat_url.split('/')[2]:52s} declared={len(sites)}")
        time.sleep(PAUSE_S)
        for site in sites:
            publisher, licence, st = site_licence(site)
            rows.append({"catalogue": cat_url.split("/")[2], "site": site,
                         "publisher": publisher, "licence": licence, "status": st})
            time.sleep(PAUSE_S)

    Path("results").mkdir(exist_ok=True)
    with open("results/licence_audit.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["catalogue", "site", "publisher", "licence", "status"])
        w.writeheader()
        w.writerows(rows)

    ok = [r for r in rows if r["status"] == "COMPLETE"]
    declared = [r for r in ok if r["licence"]]
    counts: dict[str, int] = {}
    for r in declared:
        counts[str(r["licence"])] = counts.get(str(r["licence"]), 0) + 1

    print("\n" + "=" * 72)
    print("LICENCE AUDIT")
    print(f"  sites declared/read : {len(rows)} / {len(ok)}")
    print(f"  sites declaring a licence : {len(declared)}/{len(ok)}"
          f"  ({len(ok) - len(declared)} readable sites declare NONE)")
    for lic, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"    {n:4d}  {lic}")
    print("=" * 72)


if __name__ == "__main__":
    sys.exit(main())
