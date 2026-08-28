# Receiving Wesley's full-scale dataset — receipt protocol, and the DEF-M0-4 handover

**Date:** 27 August 2026 · **Prepared by:** AI assistant (cloud session) · **Provenance:** AI-assisted; PROPOSED; closes no gate.
**Context:** Wesley's overnight harvest is done; he is sending a **~40–50 GB zip via a Google Drive link**. He has withdrawn `provenance_m04_v2.py` ("provenance is your role"), so the formal-provenance half of DEF-M0-4 is now Michael's. This is the project's first **real, full-scale S0 delivery** — receive it like one.

## 1. Register corrections from the WhatsApp round (small, keep the record exact)

1. Wesley's recap says DEF-M0-3 "pointed at your harvest_pilot but applied to mine". For the record it was the reverse: **DEF-M0-3 was filed against his `harvest_open_sessions.py`** (`if not items: break`); `harvest_pilot.py` carries the *sibling* defect (compares `next` to the original feed URL). Same outcome — his `acquire_feed` terminal taxonomy fixes it and his AT-RPDE tests pass — but the disposition record should name the right artefact.
2. Everywhere "m04" appears in this thread it means the defect **DEF-M0-4**, never deliverable **M-04** (identity contract). The adopted script is renamed `provenance_def_m0_4_v2.1.py` partly to kill this ambiguity for good.
3. Ownership timeline for the file: originated Wesley 26 Aug → withdrawn same day → adopted into Michael's stream as v2.1. Recorded in the script header; no silent re-attribution.

## 2. The adopted artefact: `provenance_def_m0_4_v2.1.py` (on the workspace root)

Three changes from Wesley's v2, all verified by execution in a scratch corpus:
- **The false-green bug is fixed.** v2's `build_manifest` never appended artefacts, so it wrote `"artefacts": []` and both "AT-DATA-1 PASS" and AT-DATA-2 passed over **zero** files. v2.1 records all 8, and the tamper test now fails typed (`HashMismatch, exit 12`) instead of passing vacuously.
- **Resolver guard:** corpus prefixes are now `("census2_", "census_")` — bare `"census2"` also matched the `census2021/` demographic directory.
- **census2 provenance filled by its owner** (you): pilot harvest, 138 publishers, 2 pages/feed, 15 July 14:56–15:22Z, per-feed envelope licences via `feed_licence_register.csv` (Halo = known 403 gap). Retention is deliberately left `FILL-IN` — that is a decision, not a fact I can supply.

**Still open on DEF-M0-4 (yours):** set retention for each artefact class; set `bundle_route` values (the Google Drive link *is* the bundle route for the new delivery); rebuild the manifest against Wesley's real snapshot once received; run `verify`; then record the disposition.

## 3. Receipt protocol for the 40–50 GB delivery (do these in order)

**Before downloading anything:**
1. `df -h /` — you need roughly **2× the zip** free (download + extraction). If the Mac can't hold it, use an external drive; do not silently skip verification because of space.
2. **Keep it out of `~/Documents`** (iCloud-synced — eviction has burned this project three times; a 50 GB archive in iCloud is asking for dataless placeholders). `~/Projects/` or an external volume.
3. Ask Wesley for two things (draft in §4): the **zip's SHA-256** (`shasum -a 256 <file>.zip` on his side), and — this is the practical unlock — a **second, small bundle** containing just the derived files: `manifest.json`, `pages.csv`, `feeds_ledger.csv`, `walk_terminals.csv`, `records.jsonl`, `tombstones.jsonl`, `geo.csv`. That is what your S0/S1 work actually consumes day-to-day (likely 1–3 GB); the 50 GB raw-bytes zip is the **auditable archive**, and it can legitimately stay in Drive as the declared `bundle_route` with its hash recorded — you don't need it resident to govern it.

**On receipt:**
4. Hash the zip and record a **delivery receipt** (one small file at the workspace root): Drive link, zip SHA-256, byte size, received-at timestamp, sender. Ask Wesley to keep his original until your hash matches his.
5. Extract (or open the small bundle) and check `manifest.json`'s self-description: `feeds_complete` vs `feeds_incomplete`, the terminals histogram, `records_s0`, collection start/end. These are his pipeline's own honesty numbers — they are the headline facts for the report's data chapter.
6. **Spot-verify integrity end-to-end:** his `pages.csv` records a SHA-256 for *every raw page*. Sample ~20 random rows, hash the corresponding `page_*.bytes` files, compare. Bytes matching page-level hashes recorded at harvest time is exactly the immutability evidence DEF-M0-2's fix promised — now demonstrated on the real corpus.
7. Point `provenance_def_m0_4_v2.1.py` at the snapshot (`build <vintage> <git-sha>`, fill retention + bundle_route, then `verify`) — first real run of the governed-inputs manifest.
8. Hand me (or local Codex) the small bundle + a sample of raw pages via the connected folder, and I'll do the independent verification pass and the delivery-receipt write-up. **Honest boundary:** this receipt protocol is *scoped* S0 acceptance — integrity, provenance, completeness accounting. It is **not** the full `S0-AT-01..09` battery, which still needs the co-designed contract (M03-DESIGN-01) — the session Wesley is now warm for.

## 4. Drafts to send Wesley (short)

> **Ask (send now):** Before I pull the big zip — can you run `shasum -a 256 <zipfile>` and send me the hash + exact byte size? And could you also zip up just the small derived files (manifest.json, pages.csv, feeds_ledger, walk_terminals, records.jsonl, tombstones.jsonl, geo.csv) as a separate download? That's what my stream consumes directly — the big raw archive can stay in Drive as the declared bundle route, hash on record. Keep your original until my hash matches. Also: provenance script adopted, thanks — I fixed one real bug in it before first use (the manifest was built empty, so its PASS lines checked nothing; one missing `artefacts.append`), filled in the census2 provenance you asked for, and it now fail-closes correctly on tampering. DEF-M0-4's rest is on me.

## 5. On sharing this Claude session's link with Wesley

Technically possible, and his instinct ("easier than relaying") is fair — but I'd keep this particular session yours. It is your stream's working record: it contains your acceptance deliberations, candid review assessments of teammates' work, and the direction-of-instruction trail that your AI-use disclosure and M-26 authorship evidence depend on. Mixing a second instructor into it muddies exactly the who-directed-what line the project has kept clean all month. The pattern that has worked all week — artefacts + hashes travelling between sessions, each member directing their own — *is* the collaboration, with a clean audit trail as a side effect. If a genuinely joint surface would help, the right tool is a **fresh shared session** (or the team repo/issue thread) scoped to the joint object — the M03-DESIGN-01 S0-contract co-design is the perfect candidate — started clean, with both of you in it, and nothing of either private stream inside. Your call; that's the trade.

## 6. Standing queue (unchanged, and now genuinely time-sensitive)

The **team-asks email is still unsent** — the §09 session with Clarence and the ratification meeting are both waiting on it, and with real data landing, the M-05 defaults/horizon decisions (Fahmi) are about to become load-bearing. Also still open: the `verify --all` tail, and exporting the WhatsApp threads (now including this one — it contains Wesley's defect recap and the delivery announcement) into the evidence folder.
