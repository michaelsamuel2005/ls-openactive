#!/usr/bin/env python3
"""
DEF-M0-4 — governed data manifest + clone-reproduction command.  v2.1

OWNERSHIP: originated by Wesley (provenance_m04_v2.py, 26 Aug 2026), who withdrew it
after the role clarification — formal data provenance sits in Michael's stream. Adopted
by Michael as the DEF-M0-4 working artefact. v2.1 changes (26 Aug, AI-assisted, PROPOSED):
  1. build_manifest now actually APPENDS each artefact (v2 wrote an empty manifest, so
     its AT-DATA-1/2 "PASS" lines were vacuous — demonstrated before fixing);
  2. corpus resolver prefixes tightened to ("census2_", "census_") so the census2021/
     demographic directory can never be mistaken for the OpenActive corpus;
  3. census2 provenance fields filled by their owner (Michael) instead of REQUESTED.
Naming: file renamed def_m0_4 to stop the DEF-M0-4 (defect) / M-04 (identity contract
deliverable) collision. Nothing here closes DEF-M0-4: retention + bundle_route fill-ins
and a real verified run against the incoming acquisition delivery remain.

Extended to meet Michael's acceptance tests AT-DATA-1/2/3:

  AT-DATA-1: one command re-materialises the declared inputs from the authorised
             bundle route AND verifies every hash, failing (typed non-zero) on any
             missing or mismatched artefact.
  AT-DATA-2: every artefact has licence + attribution + retention.
  AT-DATA-3: the manifest's research-vintage identifier matches downstream result
             manifests that consume the bundle.

Key design point (Michael's "required boundary"):
  * The MANIFEST lives under `manifests/` — version-controlled, in the repo.
  * The DATA lives in the authorised private bundle route (a shared drive / bucket /
    partner store) — never in the repo.
  * The command fetches from the bundle route, then verifies hashes.

FILL-IN markers are values only the data's owner can supply. For any artefact you
did NOT produce (e.g. a corpus from someone else's commit), do not invent
provenance — mark owner and route and request the values from that owner.
"""

import json
import hashlib
import sys
import shutil
from pathlib import Path
from datetime import datetime, timezone


# =====================================================================
#  Typed failures (AT-DATA-1 requires a *typed* non-zero failure, not a
#  bare sys.exit — so the caller can distinguish WHY reproduction failed)
# =====================================================================
class ReproError(Exception):
    exit_code = 10
class MissingArtefact(ReproError):
    exit_code = 11
class HashMismatch(ReproError):
    exit_code = 12
class UnresolvedProvenance(ReproError):
    exit_code = 13
class BundleRouteUnavailable(ReproError):
    exit_code = 14


# =====================================================================
#  MANIFEST location — in the repo, NOT in ignored data/
# =====================================================================
MANIFEST_DIR = Path("manifests")


def sha256_of(path: Path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


# ---------------------------------------------------------------------
#  DECLARE the governed input/output set for a vintage.
#  Each artefact binds the six fields Michael requires.
# ---------------------------------------------------------------------
def declare_artefacts(vintage: str):
    snap = Path("snapshots") / vintage
    artefacts = []

    # --- artefacts YOU produced (acquisition outputs) — you can fully bind these ---
    for name, licence, source in [
        ("records.jsonl",     "CC-BY-4.0", "OpenActive RPDE feeds — current-state S0 (this pipeline)"),
        ("tombstones.jsonl",  "CC-BY-4.0", "OpenActive RPDE feeds — deletions (this pipeline)"),
        ("pages.csv",         "CC-BY-4.0", "acquisition log (this pipeline)"),
        ("feeds_ledger.csv",  "CC-BY-4.0", "feed discovery ledger (this pipeline)"),
        ("geo.csv",           "CC-BY-4.0", "London borough classification (this pipeline)"),
        ("walk_terminals.csv","CC-BY-4.0", "RPDE walk terminals (this pipeline)"),
    ]:
        artefacts.append({
            "logical_name": name,
            "path_pattern": f"snapshots/{vintage}/{name}",
            "owner": "Wesley",
            "source": source,
            "licence": licence,
            "attribution": "OpenActive data © respective publishers, CC-BY-4.0",
            "retention": "FILL-IN",                 # FILL-IN: your retention rule
            "research_vintage": vintage,
            "bundle_route": "FILL-IN",              # FILL-IN: shared-drive/bucket path for this file
        })

    # --- external INPUT you consumed: the ONS boundary (you can bind this) ---
    artefacts.append({
        "logical_name": "london_boroughs.geojson",
        "path_pattern": "boundaries/london_boroughs.geojson",
        "owner": "Wesley",
        "source": "ONS Open Geography Portal — Local Authority Districts (Dec 2025) BFC",
        "licence": "OGL v3",
        "attribution": "Contains ONS & OS data © Crown copyright and database right 2025",
        "retention": "FILL-IN",
        "research_vintage": "2025-12",
        "bundle_route": "FILL-IN",
    })

    # --- artefact you did NOT produce: the census2 corpus (Michael's commit) ---
    # Do NOT invent its provenance. Declare it as owner=Michael and request values.
    # Resolve by prefix + newest, fixing the census_* vs census2_ glob defect.
    corpus = _resolve_newest("data/raw", prefixes=("census2_", "census_"))  # v2.1 FIX: bare "census2" also matched census2021/
    if corpus:
        artefacts.append({
            "logical_name": corpus.name,
            "path_pattern": f"data/raw/{corpus.name}",
            "owner": "Michael",
            # Owner-supplied values (Michael, 2026-08-26; see 24_CENSUS2_PROVENANCE_...md):
            "source": "harvest_pilot.py --tag census2 (diagnostic pilot, superseded by "
                      "data_acquisition.ipynb): 138 publishers nationally, 2 RPDE pages/feed, "
                      "run 2026-07-15T14:56-15:22Z",
            "licence": "per-feed RPDE envelope licences; register: results/feed_licence_register.csv "
                       "(known gap: publisher Halo, HTTP 403 at dataset site)",
            "attribution": "OpenActive data (c) respective publishers, per-feed licences",
            "retention": "FILL-IN",                 # Michael: local-only so far; set the rule
            "research_vintage": _vintage_from_name(corpus.name),
            "bundle_route": "REQUESTED-FROM-OWNER",
            "note": "OpenActive parent/child corpus from commit 286da75; provenance "
                    "must be supplied by its originator, not authored here.",
        })

    return artefacts


# ---------------------------------------------------------------------
#  Robust resolver — fixes the census_* glob that missed census2_...
# ---------------------------------------------------------------------
def _resolve_newest(root, prefixes):
    root = Path(root)
    if not root.exists():
        return None
    matches = [p for p in root.iterdir() if any(p.name.startswith(pre) for pre in prefixes)]
    if not matches:
        return None
    return max(matches, key=lambda p: (_vintage_from_name(p.name) or "", p.stat().st_mtime))


def _vintage_from_name(name):
    import re
    m = re.search(r"(\d{4})[-_T]?(\d{2})[-_]?(\d{2})", name)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None


# ---------------------------------------------------------------------
#  BUILD the manifest (writes to manifests/, in the repo)
# ---------------------------------------------------------------------
def build_manifest(vintage: str, git_sha: str = None):
    artefacts = []
    for a in declare_artefacts(vintage):
        p = Path(a["path_pattern"])
        if p.exists() and p.is_file():
            a["sha256"] = sha256_of(p)
            a["bytes"] = p.stat().st_size
        elif p.exists() and p.is_dir():
            # directory corpus: hash a manifest of its files' hashes
            files = sorted(f for f in p.rglob("*") if f.is_file())
            digest = hashlib.sha256()
            total = 0
            for f in files:
                digest.update(sha256_of(f).encode())
                total += f.stat().st_size
            a["sha256"] = digest.hexdigest()        # content identity of the whole dir
            a["bytes"] = total
            a["file_count"] = len(files)
        else:
            a["sha256"] = None
            a["bytes"] = None
            a["missing_at_build"] = True
        artefacts.append(a)   # v2.1 FIX: without this the manifest was empty and both PASSes were vacuous

    # AT-DATA-2 check: flag artefacts lacking licence/attribution/retention
    incomplete = [a["logical_name"] for a in artefacts
                  if "FILL-IN" in (a.get("licence"), a.get("retention"), a.get("attribution"))
                  or "REQUESTED-FROM-OWNER" in (a.get("licence"), a.get("retention"))]

    manifest = {
        "manifest_type": "governed-input-bundle",
        "research_vintage": vintage,               # AT-DATA-3 anchor
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_sha": git_sha,
        "artefacts": artefacts,
        "incomplete_governance": incomplete,       # AT-DATA-2: must be empty to pass
    }

    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    out = MANIFEST_DIR / f"inputs_{vintage}.json"
    out.write_text(json.dumps(manifest, indent=2))
    print(f"wrote {out}")
    if incomplete:
        print(f"\n⚠️  AT-DATA-2 NOT YET MET — {len(incomplete)} artefact(s) lack "
              f"licence/attribution/retention: {incomplete}")
        print("   For your own artefacts: fill in retention.")
        print("   For census2 (owner=Michael): request source/licence/retention from him.")
    return manifest


# ---------------------------------------------------------------------
#  MATERIALISE + VERIFY — the single clone-reproduction command (AT-DATA-1)
#  Fetches each artefact from its bundle_route into place, then verifies hash.
# ---------------------------------------------------------------------
def materialise_and_verify(vintage: str):
    man_path = MANIFEST_DIR / f"inputs_{vintage}.json"
    if not man_path.exists():
        raise MissingArtefact(f"manifest not found: {man_path}")
    manifest = json.loads(man_path.read_text())

    for a in manifest["artefacts"]:
        dest = Path(a["path_pattern"])
        route = a.get("bundle_route")

        # 1. materialise if absent
        if not dest.exists():
            if not route or route in ("FILL-IN", "REQUESTED-FROM-OWNER"):
                raise BundleRouteUnavailable(
                    f"{a['logical_name']}: no bundle route declared — cannot materialise")
            src = Path(route)                       # local/mounted bundle; swap for S3/HTTP fetch
            if not src.exists():
                raise BundleRouteUnavailable(
                    f"{a['logical_name']}: bundle route {route} not reachable")
            dest.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, dest)
            else:
                shutil.copy2(src, dest)

        # 2. verify hash
        if a.get("sha256") is None:
            raise UnresolvedProvenance(f"{a['logical_name']}: no expected hash in manifest")
        actual = (sha256_of(dest) if dest.is_file()
                  else _dir_digest(dest))
        if actual != a["sha256"]:
            raise HashMismatch(
                f"{a['logical_name']}: expected {a['sha256'][:12]} got {actual[:12]}")

    print(f"AT-DATA-1 PASS — all {len(manifest['artefacts'])} artefacts materialised "
          f"and hashes verified for vintage {vintage}.")


def _dir_digest(d: Path):
    files = sorted(f for f in Path(d).rglob("*") if f.is_file())
    h = hashlib.sha256()
    for f in files:
        h.update(sha256_of(f).encode())
    return h.hexdigest()


# ---------------------------------------------------------------------
#  CLI  (typed exit codes so failures are diagnosable — AT-DATA-1)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    vintage = sys.argv[2] if len(sys.argv) > 2 else "2026-08-18"
    try:
        if cmd == "build":
            git_sha = sys.argv[3] if len(sys.argv) > 3 else None
            build_manifest(vintage, git_sha)
        elif cmd == "verify":
            materialise_and_verify(vintage)
        else:
            print(f"unknown command: {cmd}"); sys.exit(2)
    except ReproError as e:
        print(f"REPRODUCTION FAILED [{type(e).__name__}, exit {e.exit_code}]: {e}")
        sys.exit(e.exit_code)
