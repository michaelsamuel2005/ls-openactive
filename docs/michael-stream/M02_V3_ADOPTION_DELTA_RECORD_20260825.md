# M-02 OA-1..3 v3 adoption — lane and programme-manifest delta record

**Date:** 25 August 2026 (evening)
**Trigger:** Michael's hash-bound approval of the three OA-1..3 v3 attestation proposals (receipt `OA-1_TO_OA-3_ATTESTATION_APPROVAL_RECEIPT_20260825.md`, SHA-256 `9547dfa4…b001`, approval line received 2026-08-25T10:41:07+01:00), followed by Michael's execution of the K7 v3 freezes on his machine (terminal outputs of 25 Aug, ~21:24–21:25 BST).
**Executor of this delta:** AI assistant (cloud session) as mechanical successor work from independently verified bytes. The human acts were Michael's alone: the approval line, the inspection confirmation, and the freeze commands. This record closes no challenge gate.

## 1. Freeze facts (independently verified from staged bytes)

| Block | v3 card | SHA-256 | Frozen at | Lock receipt |
|---|---|---|---|---|
| OA-1 | `work/blocks/OA-1/frozen/v3/card.md` | `d92c8531dc2eb7f8964d5636517c8b6878c500213bb4f3cb259f9015ead5873d` | 2026-08-25T21:24:36+01:00 | `work/receipts/OA-1_v3_LOCK_RECEIPT.json` |
| OA-2 | `work/blocks/OA-2/frozen/v3/card.md` | `b98f5c57a6c19f540f81b20406bc730315bd9bc25cda9992dea55057b5713018` | 2026-08-25T21:24:47+01:00 | `work/receipts/OA-2_v3_LOCK_RECEIPT.json` |
| OA-3 | `work/blocks/OA-3/frozen/v3/card.md` | `732ff7b14d44d6a95656924471dcadfa54b88b906c1a659f1949359f98b7f249` | 2026-08-25T21:25:12+01:00 | `work/receipts/OA-3_v3_LOCK_RECEIPT.json` |

Verified independently in the cloud from staged bytes: each card hash matches the harness's printed value; each v3 card equals its exact v2 card (`69bdaea9…` / `ef7bc22e…` / `60f5f584…`, the same hashes named in the approval receipt) plus one appended "Stage D — Michael's personal attestation" section and nothing else (47 lines added, 0 removed, per block); each preserved attestation input is byte-identical to the approved input (`26716f0b…` / `96af9958…` / `b664b725…`); the authorised timestamp `2026-08-25T10:41:07+01:00` appears exactly once per card; all three `state.json` files report `PERSONAL_ATTESTATION_RECORDED`; `work/receipts/VERSION_MANIFEST.tsv` carries the three new v3 rows with matching hashes.

Also for the record: during execution two duplicate commands were issued in error (a second `freeze-v3 OA-2`, a second `record-attestation OA-3`). The harness refused both (`CHECK_FAIL: v3 requires Michael's separately captured attestation`; `CHECK_FAIL: refusing to overwrite existing frozen artefact`) with no side effects — fail-closed behaviour working as designed. No artefact was altered by the duplicates.

## 2. Files changed by this delta (old → new SHA-256)

| File | Old | New |
|---|---|---|
| `michael-foundations-m01-m08-20260824/m02/OA-1_TO_OA-3_ATTESTATION_PROPOSAL_MANIFEST.tsv` | `ba8f970bdb19cc501d860ab7de0024a9c908c72f70c7c316e4c639567303113d` | `456e233823d48b433dddfc90381c35117fccdffea2afd6201244bed71704150f` (statuses: review → `MICHAEL_APPROVAL_RECORDED_20260825`; three proposals → `ADOPTED_V3_FROZEN_20260825`; hashes/bytes unchanged) |
| `…/m02/M02_EVIDENCE_STATUS.tsv` | `7f3bfeb35447ff2a567aa17f6a2e7e39de1d6b9cf5ca3ed8fd89e6bcd02d57a1` | `5815cf8e236a00829163df1528534835ecdd13cda74ca882189108e86557e499` (OA-1..3 rows → `PERSONAL_ATTESTATION_RECORDED` with the v3 card hashes; OA-4 and TH rows untouched) |
| `…/m02/SHA256SUMS` | `5b4f759241b3063212a1238397eb3fbf883d2e726df8f429fb3efe193ac6d5f2` | `652c69c55eb07acefd816315836524808b3191d43a1d11cdfba9415f466ac4a7` (regenerated: nine entries, sorted, duplicate rows of the prior version removed; verified by simulated `sha256sum -c` over the exact final directory contents) |
| `…/PROGRAMME_MANIFEST.tsv` | `a87b73acaf9c0eb27b0e0a5d6c4e40b788959885ed4df841841c6aea989fabcd` | `b330c6945062d6bcb947bb5e5312738ac229abf5a8e06c7c64e8e125a2ead250` (single cell updated: the `m02/SHA256SUMS` lane-manifest hash) |
| `…/PROGRAMME_MANIFEST.tsv.sha256` | (bound old value) | rewritten to bind the new manifest |

Old values remain durably recorded in `M01_M08_HANDOFF_VERIFICATION_RECEIPT_20260824.json`, the 24 Aug handoff set, and the assistant's verification memos. `integration/HANDOFF_DOCUMENT_INDEX_20260824.tsv` (row: `../m02/SHA256SUMS`, old hash) is deliberately left untouched as dated 24 August evidence; this record supersedes that row's value.

## 3. Register effect

Gate `M02-OA123-ATT-01` ("Michael reviews and approves the exact three proposals") is now satisfied by: the approval receipt + the three frozen v3 cards + this delta. OA-1..3 join OA-4 in state `PERSONAL_ATTESTATION_RECORDED`, `usable=false` — attested, **not** challenged. Still open on these blocks: eligible challenger appointment (`M02-OA-ELIG-01`), export/send (`M02-OA-SEND-01`), return, and Michael's dispositions. Nothing in this delta claims completion of M-02.

## 4. Outstanding manual step (Michael, ~1 minute)

Move `m02/OA-1_TO_OA-3_ATTESTATION_VERIFICATION_AND_DECISION_SHEET_20260825.md` out of `m02/` to the workspace root (it is a working document, deliberately not listed in the regenerated lane manifest; the lane inventory reads as closed only once it leaves the directory). The three misdated `…_20260824` filing files at the workspace root also still await deletion.
