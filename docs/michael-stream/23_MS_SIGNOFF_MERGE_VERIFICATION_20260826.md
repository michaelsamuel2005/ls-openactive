# Merge verification — MS-1/3/6/7/8/9 sign-offs at `5491bb9`

**Date:** 26 August 2026 · **Verifier:** AI assistant (cloud session), read-only from staged bytes
**Object:** merge commit `5491bb9` on `origin/clarence/c-block-05` ("Merge PR 12 Michael re-review sign-offs")
**Provenance:** AI-assisted mechanical verification; PROPOSED; signs nothing, closes no gate.

## 1. Result — the loop is closed, and the merged bytes are correct

| Check | Result |
|---|---|
| Six entries present in `docs/assurance/signoffs.md`, one per finding | **Yes** — `Re-review — MS-1/3/6/7/8/9` at lines 262–320, appended after the existing CL-7 material, no existing entry disturbed |
| Entry text matches the prepared drafts | **Verbatim** — every Finding, Artefacts, Method, Conditions and Not-covered field identical to `MS_SIGNOFF_ENTRIES_READY_FOR_MICHAEL_20260826.md` |
| Michael's decisions recorded | **Yes** — MS-1 / MS-6 / MS-8 `APPROVED`; MS-3 / MS-7 / MS-9 `APPROVED WITH CONDITIONS`; all six `Signed: Michael Samuel · 2026-08-26`; no `RECOMMENDED:` or `[Michael: confirm or amend]` placeholder survives |
| Authorship | Michael's own commit `74e0b62` in the merge history (branch `michael/ms-rereview-signoffs-20260826`), merged via PR #12 — contribution evidence is Michael's, not transcribed by another author |
| Both conditions actually applied by Clarence | **Yes**, in `1a9aae8`: `intent.py` `NEG_ACCESS_RE` now begins `\binaccessible\b|…`; `_c_version` carries the ordering comment naming the `_c_schema`↔`_c_version` interlock and warning against reordering `CHECKS` |
| Suites at the merged tip | **All pass** — checker, `test_slice.py`, `test_conversation.py` re-run in a clean container |
| Exploits at the merged tip | **All still killed** — `schema_extra_field`, `bad_transition`, `incompatible_decision` → `FAIL_MALFORMED`; unmutated golden → `PASS`; public signature is `check(cert, ctx)` and `checks=[]` raises `TypeError`. No regression was introduced by the condition edits |
| MS-9 condition behaviourally confirmed | "swimming in croydon but **inaccessible** venues" → `access=None`, `unsupported=['negated accessibility constraint']`, `scenario=None`, `confident=False` — surfaced, never reversed; unaffected queries behave as before |

## 2. What this closes, and what it does not

**Closes:** the MS re-review loop end to end — findings raised (23 Aug, `9b0807d`), fixed with adversarial tests (`7cf65ca`), independently re-verified in two separate environments, approved by Michael with two conditions, conditions applied by Clarence, sign-offs merged under Michael's own authorship.

**Does not close:** MS-2, MS-4, MS-5, MS-10 remain OPEN joint §09 work; `RATIFY-09-04` / `RATIFY-09-05` remain unrecorded; therefore CL-1, CL-3 and CL-6 remain blocked, and CL-14's finding side is clear but its claim still awaits RATIFY-09-05. The assurance validator reporting **0/15 claims authorised** after this merge is the correct and expected result — a completed reviewer gate is not claim authorisation.

**Independence boundary, stated exactly:** this merge records **one** eligible non-author human review (Michael's, of Clarence's work). The three mechanical replays (Clarence's, and two AI sessions) strengthen the factual base but are not additional human reviews.

## 3. Register effect

- Michael's non-author review duty (work package §5.1.7 — "acquisition/bitemporal and application artefacts at the Michael boundary") is now **evidenced** for the C-BLOCK-05 objects, with a durable, hash-addressable record in the team repository rather than a private note.
- Contributes to `M-26` (contribution/review/handover dossier): a complete raise → fix → verify → approve → merge cycle in Michael's own commits, with the negative-leg reproduction that distinguishes a real defect from a cosmetic one.
- Nothing in `M-01`–`M-08` changes state; `PROGRAMME_COMPLETE=false` stands.

## 4. One optional tidy (non-blocking)

MS-9's *Not covered* field reads "…the complete-decision-digest comparison requirement in **your** condition 6…" — second person reads oddly in Michael's own signed entry. If a future successor edit touches the ledger, change to "my condition 6". Not worth a commit on its own; the record is unambiguous as it stands.
