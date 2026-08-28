# `census2_20260715T145612Z` — provenance record, and a defect-ownership correction

**Date:** 26 August 2026 · **Prepared by:** AI assistant (cloud session), from read-only inspection of Michael's working copy `~/Projects/ls-openactive-local`
**Why this exists:** Wesley asked what `census2_20260715T145612Z` is (it is not in the repository, so it is invisible to him), and observed that several DEF-M0 findings appear to target `src/harvest_pilot.py` rather than his data-acquisition code. Both points are addressed below from the files themselves.
**Provenance:** AI-assisted; PROPOSED; states facts and marks assumptions; closes no gate and assigns no authorship.

## 1. What `census2_20260715T145612Z` is — FACTS (verified from disk and code)

| Property | Value |
|---|---|
| Location | `data/raw/census2_20260715T145612Z/` in the working copy — **local only** |
| Contents | **767** JSON files, **~292.5 MB** |
| Written | 2026-07-15 **14:56:19Z → 15:22:03Z** (a ~26-minute run; the directory name carries the run start, 14:56:12Z) |
| Coverage | **138 distinct publishers**, **national** (e.g. Active Hartlepool, Active Leeds, Active Luton, Bangor City Stadium) — *not* London-scoped |
| Feed kinds | FacilityUse 263, Slot 259, SessionSeries 106, ScheduledSession 67, CourseInstance 64 pages (plus a few pages from publishers that declare no `publisher.name`, filed as `UNNAMED`) |
| Producer | `src/harvest_pilot.py`, run with `--tag census2`. The module docstring states it writes `data/raw/<tag>_<UTC>/` and gives `--per-catalogue 88 --pages 2 --tag census` as the all-sites form. Two pages per feed. |
| Why `census2` and not `census` | `src/feed_licence_register.py` records that the first `census` archive is **44 pages short** because of filename collisions (D-026 item 4) and instructs "prefer the `census2` archive once it exists"; `harvest_pilot.py` now disambiguates filenames by a SHA-1 digest of the page URL and never overwrites (D-026). `census2` is therefore the **collision-fixed re-run**. |
| Why it is not in git | `.gitignore` excludes `data/` outright (`data/raw/*`, `data/processed/*`, `data/`). Deliberate: data is never committed, and the repository was **public until 15 July 2026** (D-032). |
| Licence provenance | Each retained page keeps the RPDE envelope `license` field; `src/feed_licence_register.py` aggregates one row per (publisher, kind, licence) from the retained raw. Known gap: publisher `Halo` returned HTTP 403 at its dataset site, so its licence is unknown (D-026 item 2). |
| Vintage / completeness | A **single snapshot** of 15 July 2026 at **2 pages per feed**. It is a breadth sample of what publishers expose, **not** a complete feed capture and **not** a certified-complete collection under the M-03 S0 contract. |

**ASSUMPTION (for Michael to confirm, one line):** that this run was executed by Michael on 15 July 2026. The bytes and code establish *what* and *when*; only the person who ran it can attest *who*.

## 2. Wesley's second point — he is substantially right, and the packet should say so

Checked against the actual code in the working copy:

| Defect | What the code shows | Whose artefact |
|---|---|---|
| **DEF-M0-1** — result changes with PROJ network setting; three declared environments | Real, and not about the pilot: `to_london` in `src/harvest_open_sessions.py` calls `.to_crs("EPSG:27700")` with defaults (no PROJ_NETWORK, no grid policy anywhere); the three environments are Wesley's, the repo's `environment.yml` (**confirmed to be Michael's own June export** — `prefix: /opt/anaconda3/envs/ls-openactive`, versions match Michael's local env exactly), and Michael's base Anaconda where the red replay ran | **Repo-wide environment governance.** Declaring the supported environment is the owner's act; the stale `environment.yml` is Michael's to retire |
| **DEF-M0-2** — "immutable raw, exactly as served" but the checksum is of a derivative | **Confirmed in `src/harvest_pilot.py`**: `blob = json.dumps(body)` then `out.write_text(blob)  # immutable raw, exactly as served`. The retained bytes are Python's re-serialisation of the parsed body, not the served bytes | **`harvest_pilot.py` — not Wesley's acquisition code** |
| **DEF-M0-3** — walker stops on any empty items page | **Confirmed in `src/harvest_open_sessions.py`** (`items = payload.get("items", [])` → `if not items: break`), which is the acquisition harvester. MOD/RPDE requires the last-page test to be empty items **and** `next` equal to the current page URL; an empty page alone is legal mid-feed | **Acquisition code — correctly filed** |
| **DEF-M0-4** — nothing binds inputs to licence/retention/vintage; the lineage glob misses the corpus in use | **Confirmed**: `src/trace_lineage.py` globs `data/raw/census_*`, which does **not** match `census2_20260715T145612Z`; `src/feed_licence_register.py` does it correctly (`census2_*` first, then `census_*`, then `pilot_*`) | **`trace_lineage.py` — not Wesley's acquisition code.** The licence/retention/vintage binding itself is a shared governance item |

**Separate observation, Michael's side, not currently filed:** `harvest_pilot.py` terminates paging with `page_url = body.get("next"); if not page_url or page_url == url: break`, comparing `next` against the **original feed URL** rather than the **current page URL**. The RPDE last-page rule is `next == current page URL`. On a two-page run this is unlikely to bite, but it is the same class of defect as DEF-M0-3 and should be recorded rather than discovered later.

**Net:** of the four filed defects, one (DEF-M0-3) is squarely against acquisition code, one (DEF-M0-1) is repo-wide environment governance in which Michael's own stale export is implicated, and two (DEF-M0-2, and the glob half of DEF-M0-4) are against `harvest_pilot.py` / `trace_lineage.py` — pilot and lineage tooling, not Wesley's data acquisition.

**AUTHORSHIP — not established here.** These files live in the shared `src/` tree; this memo does not attribute them. `git log --follow --format='%an  %ad  %s' -- src/harvest_pilot.py src/trace_lineage.py` settles it in seconds and should be run before any re-assignment is recorded.

## 3. What follows

1. Answer Wesley's factual question now (§1) — it is the input `DEF-M0-4` needs.
2. Record a **successor** to the filing register that re-assigns DEF-M0-2 and the DEF-M0-4 glob item to their actual artefacts, keeping the sealed original packet untouched. Do not quietly re-scope the sealed bytes; supersede them in the open.
3. Add the `harvest_pilot.py` next-cursor observation to the same successor.
4. The defects remain valid regardless of ownership — a defect filed against the wrong owner is a filing error, not a false finding. Correcting it promptly is the strongest available evidence that the process is honest rather than adversarial.

## 4. Strategic note (worth more than the correction)

A retained-raw corpus of **767 pages / 292.5 MB / 138 publishers with envelope licences preserved** already exists on disk. It is **not** an S0 delivery under the M-03 contract — no collection certificate, no completeness proof, 2 pages per feed, national rather than London-scoped, July vintage — but it is real OpenActive data with retained provenance, and it is the obvious seed for the first real S0 delivery and for M-07 fixture derivation. Worth raising at the ratification meeting: what would need to be added to a re-run for it to satisfy `S0-AT-01..09`.
