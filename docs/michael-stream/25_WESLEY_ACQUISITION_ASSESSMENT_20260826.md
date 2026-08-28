# Wesley's `data_acquisition.ipynb` vs the four M0 defects — assessment

**Date:** 26 August 2026 · **Prepared by:** AI assistant (cloud session)
**Object:** Wesley's `data_acquisition.ipynb` (64 cells, kernel `openactive-env`), sent to Michael 26 Aug
**What I did:** read every cell; **executed Wesley's own AT-RPDE acceptance tests** (`run_at_rpde()`, cell 32) in an isolated container — they need no network (mock feed). I did **not** run the full harvest (no network to the feeds, no `snapshots/` staged) and did **not** inspect the boundary GeoJSON's CRS (not staged). Claims below are marked FACT (read or executed) vs ASSUMPTION.
**Provenance:** AI-assisted; PROPOSED. This does not disposition any defect — that is Wesley's owner act — and closes no gate.

## 0. First, the question Wesley actually asked ("why are those files there — that's my territory")

He is right, and the answer is clean: **`harvest_pilot.py` + `census2_…` are a diagnostic pilot, not acquisition.** Its own docstring says it exists to answer one question — "does the source data carry what the legacy CSV lost?" — and D-021/D-026 record it as a deliberate stopgap built when no real acquisition existed. It pulls a **sample** (2 pages/feed). Wesley's notebook is the **real acquisition**: full per-feed walks to the live edge, content-addressed raw, S0 reconstruction, a provenance manifest, and H1/H2 snapshots with drift analysis. So the correct move is **not** "fix the pilot" — it is **supersede** the pilot with Wesley's acquisition and disposition the pilot-side defects as *resolved by supersession*. His Claude's read ("it thinks we have no data and is writing code off Michael's pilot snippet") is exactly the confusion, and it resolves the moment both sides see the pilot as retired.

## 1. Defect scorecard (honest)

| Defect | Status against this notebook | Evidence |
|---|---|---|
| **DEF-M0-2** — "immutable raw" was a re-serialised derivative | **RESOLVED** | `acquire_feed` writes the **served bytes**: `raw = resp.content` → `sha = sha256(raw)` → `byte_path.write_bytes(raw)`. The hash is of the actual bytes, page-addressed as `page_00000.bytes`. No `json.dumps` round-trip. This is precisely the pilot's sin, done correctly. |
| **DEF-M0-3** — walker stops on any empty page | **RESOLVED, and I ran the tests** | Terminal is one of `live_edge_reached \| page_cap_cut \| http_error \| parse_error \| repeated_cursor_anomaly \| harvest_crash`. Live edge requires **empty items AND `next == url`**; an empty page with a *different* `next` keeps walking; the cap is distinct and retains a resume cursor; `delivery = COMPLETE` iff `live_edge_reached`. **`run_at_rpde()` → ALL PASS** (AT-RPDE-1/3 empty-intermediate, AT-RPDE-2 page-cap-distinct, AT-RPDE-5 self-next anomaly, one-terminal invariant). The fixture is literally "Michael's four-page fixture" — the two sides' contracts already align. |
| **DEF-M0-1** — result changes with PROJ network setting; undeclared environment | **Root cause sidestepped for this pipeline; governance half still open** | The notebook does borough assignment with **no reprojection at all**: it loads LAD-2025 boundaries, builds a shapely `STRtree`, and tests `Point(lng, lat).covers` **in degrees**. No `pyproj`, no `EPSG:27700`, no PROJ network grids — so the specific "Helmert-vs-OSTN15 / network-on-vs-off" divergence cannot arise here. **BUT** two things remain: (a) this correctness depends on the boundary GeoJSON being WGS84 lat/lng — **verify** (see §3); and (b) the deeper governance point — *declare one canonical environment* — is not closed; the notebook runs under a **new** kernel `openactive-env` (a 4th environment alongside Wesley's, the repo `environment.yml`, and Michael's base) and ships no environment file. |
| **DEF-M0-4** — no licence/retention/vintage binding; lineage glob misses the corpus; clean clone can't reproduce | **Vintage/provenance: RESOLVED. Licence: NOT yet.** | Cell 48 writes `manifest.json` with `git_sha`, `python`, `collection_start`/`collection_end` (vintage), completeness accounting (`feeds_complete`/`incomplete`, terminals histogram), `records_s0`, geography classes, and **reconciliation `assert`s** that the numbers add up. Strong. **Gap:** the RPDE envelope **`license` field is never captured** into the manifest or the ledger — the pilot's `feed_licence_register.py` did read `page.get("license")`; this notebook does not. The "glob misses the corpus" issue was specific to the old `trace_lineage.py`; the new `snapshots/<id>/` layout is clean and self-describing, but Michael's S1 code will need to point at it. |

**Net:** two defects (M0-2, M0-3) are resolved by supersession; M0-1 is architecturally sidestepped for the geocoding path but the "one declared environment" governance item stands; M0-4 is half-closed — vintage yes, **licence binding still to add**.

## 2. Bugs I found (small, worth a line to Wesley)

1. **FACT — missing `import tempfile`.** Cell 32's `run_at_rpde()` uses `tempfile.TemporaryDirectory()`/`mkdtemp()` but `tempfile` is imported nowhere in the notebook. As shipped, the acceptance cell raises `NameError`. Adding `import tempfile` (which I did) makes all four tests pass. One-line fix.
2. **FACT — `is_live_edge` column referenced but never written.** Debug cells 54 and 56 read `row["is_live_edge"]` / `row.get("is_live_edge")`, but `acquire_feed` writes `next_url`, `item_count`, `failure` … and **no** `is_live_edge`. Those debug prints will KeyError (54) or always show `None` (56). Leftover from an earlier page-row schema; either add the column in `acquire_feed` or drop the reference.
3. **OBSERVATION — licence capture** (the M0-4 gap above): add `"license": payload.get("license")` to each page row, and carry a per-feed licence into `manifest.json`, to close M0-4's licence half.

## 3. The one thing to verify before relying on the geography (FACT-check needed)

The borough counts depend entirely on the boundary GeoJSON being in **WGS84 (EPSG:4326, degrees)**, because the code compares degree points against the polygons with no CRS transform. ONS "BFC" boundary files are often distributed in **British National Grid (EPSG:27700, metres)**, in which case every `covers` test would silently fail and everything would read `known-outside`. Wesley evidently got a per-borough breakdown (Haringey/Redbridge appear), so it is **probably** already WGS84 — but confirm once:

```python
import json
gj = json.load(open("boundaries/london_boroughs.geojson"))
print(gj["features"][0]["geometry"]["coordinates"][0][0][:2])  # expect ~[-0.1, 51.5], NOT [530000, 180000]
```

If those look like longitudes/latitudes, the geography is sound and DEF-M0-1 truly does not bite this pipeline.

## 4. Why this matters far beyond the defects (the real headline)

The project's dominant open risk has been **data sufficiency** — whether enough live London sessions exist to support small-area analysis. Wesley's notebook shows that risk is being retired in the best possible way: **two full snapshots (H1, H2) already exist**, with per-feed completeness terminals, S0 records + tombstones reconstructed, London-borough assignment done, and **drift analysis between snapshots**. That is a real, longitudinal, provenance-carrying S0 corpus — exactly what M-03/M-04 need to stop being synthetic and what M-07 needs for real fixture derivation. It is a materially stronger position than "we have a 2-page pilot."

**But keep the boundary crisp:** this is Wesley's acquisition *converging on* Michael's S0 contract, not the contract satisfied. The real gates remain: **M03-DESIGN-01** (co-design the S0 input contract, owner + Michael) and the **S0-AT-01..09** acceptance against one immutable delivery. The encouraging fact is that Wesley's terminal vocabulary and Michael's AT-RPDE fixtures already match — the co-design is half-done in practice.

## 5. Suggested disposition (for the register, Wesley's act not mine)

1. **DEF-M0-2, DEF-M0-3 → RESOLVED_BY_SUPERSESSION**, correction = `data_acquisition.ipynb` `acquire_feed`; attach the `run_at_rpde()` ALL-PASS output as the M0-3 acceptance evidence.
2. **DEF-M0-1 → PARTIALLY_RESOLVED**: geocoding path no longer uses PROJ; **open item** = declare one canonical environment (ship an `environment.yml`/lock for `openactive-env`; retire Michael's stale June export).
3. **DEF-M0-4 → PARTIALLY_RESOLVED**: provenance manifest present; **open item** = capture per-feed `license` into the manifest/ledger.
4. Retire `harvest_pilot.py` + `trace_lineage.py`'s census globs as **superseded**; Michael's S1 lineage re-points at `snapshots/<id>/records.jsonl`.
5. Record against **D-031** and the DEF packet as owner dispositions — this is the `M01-DISP-01` evidence, and it is exactly the "issues/branches/dispositions" acknowledgement the filing anticipated.
