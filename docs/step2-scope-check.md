# Step 2 — scope check record (2a ownership map · 2b CA amendments)

**Done:** 2026-08-11 · against `CLARENCE_ZHEN_JIN_TAN_SPECIALISED_WORK_PACKAGE.md` §2.1 and its review
(CA-1…CA-7), verified file-by-file on branch `clarence/c-block-05`. Paste rows below as PR comments /
supervisor-agenda items. **Legend:** ✓ artefact present & covers the responsibility · ◑ present but
partial/bounded · ✗ missing.

## 2a — §2.1 "accountable for" → artefact (all 10 rows)

| # | §2.1 responsibility | Branch artefact | Status |
|---|---|---|---|
| 1 | Public application | `apps/public-discovery/` + `docs/applications/public-information-architecture.md` | ✓ |
| 2 | Staff application | `apps/staff-assurance/` + `staff-information-architecture.md` | ✓ |
| 3 | Conversational UX | `server/intent.py` + `/chat` route + `C-08-conversational-integration.md` | ✓ |
| 4 | Accessibility & inclusion | `accessibility-wcag22-plan.md` + `a11y_check.py` | ◑ plan + 1 automated check; **manual/AT testing evidence pending** (C-BLOCK-03/11 reviewer) |
| 5 | Application contracts | `packages/application-contracts/c-block-05/` + `C-BLOCK-05.md` | ✓ |
| 6 | Section 15 control requirements | `packages/privacy/`, `packages/security/`, `packages/ethics/` + `C-13/14/15-…md` + `ethics-application-outline.md` | ✓ (requirements only; authorities decide) |
| 7 | Certificate checker | `packages/certificate-checker/` + `C-09-certificate-checker.md` | ✓ |
| 8 | Evaluation instruments | `packages/evaluation/` + `evaluation-conditions.md` | ✓ |
| 9 | Partner-facing application pathway | `packages/staff-ia/action-card-state-machine.json` + staff `action_card.html`/`performed.html` | ◑ **action-card integration only**; wider partner pathway deliberately bounded to stretch (C-BLOCK-13) |
| 10 | Reproducible application evidence | per-package `README.md` + `docs/assurance/assurance-case.*` + test suites | ◑ present; **build manifest / runbook / contribution ledger (C-22) still thin** |

**Scope gaps (real, actionable):**
1. **Reproducible-evidence pack (row 10)** — no clean-room build manifest, no runbook, no C-22
   contribution ledger yet. Backlog item; needed for C-BLOCK-12 "functioning" claim.
2. **Accessibility evidence (row 4)** — only the plan + one automated pass exist; the manual keyboard/
   screen-reader/AT matrix is blocked on the non-author reviewer (C-BLOCK-03). Bounded, not forgotten.
3. **Partner pathway (row 9)** — only the action-card slice is built; the rest is stretch by design
   (C-BLOCK-13). Consistent with the WP; record as scope-bounded, not a miss.

*No §2.1 row has zero artefact.* Rows 4/9/10 are partial and each partial is either institutionally
blocked or explicitly stretch — none is an oversight.

## 2b — CA-1…CA-7 amendments: reflected?

| CA | Requires | Where verified | Status |
|---|---|---|---|
| **CA-1** | `L_reliance` referent = terminal `DecisionEnvelope` (identical across conditions) | `C-BLOCK-05.md` §6 + `C-BLOCK-15` row (priority 2) in the register; enforced by `INV-NONINTERFERENCE` | **Reflected.** Referent correctly bound; **open action = single named owner shared with Fahmi + joint decision-log entry (F-BLOCK-09)** — a team step, not Clarence's to self-assign |
| **CA-2** | State whether claim-contract author may also author the production interpreter | `C-09-…md` §2 (explicit open question) + §5 item 5, bound to `RATIFY-09-04` | **Reflected** — raised for the workshop; resolution is a team ratify |
| **CA-3** | C-BLOCK-05 is the keystone, carries the first date | Priority **1** in the register + `C-BLOCK-05.md` §1 "Why this is the keystone (CA-3)" | **Mostly reflected** — prioritised ✓; **the concrete first *date* is still `PENDING`** (set at the contract workshop) |
| **CA-4** | Bind C-BLOCK-01 to a real decision-log ID; no invented `RATIFY-08-*` | `C-BLOCK-01` row: decision-log ref = "create canonical ID (do NOT invent RATIFY-08-*)"; WP §2.2 also refuses it | **Reflected** — discipline honoured; **binding to a real ID is the pending team action** |
| **CA-5** | Cite by version-of-record + DOI (per-claim K7 foundation-matrix rows) | *No `reading-log.md` / foundation-matrix on the branch* | **NOT yet reflected — pending.** This is your Step-7 job and the **single biggest outstanding personal task** |
| **CA-6** | Mark deliverables core vs stretch | Register has a **Tier** column (14 core / 1 stretch); C-BLOCK-13 = stretch | **Reflected** for blockers; a per-C-XX-deliverable core/stretch tag would fully close it |
| **CA-7** | Keep authorship notice + blank §26 acceptance record | Authorship notice present in every scaffold (≈27 files); WP §26 record genuinely **blank** (not backfilled) | **Reflected** |

**CA verdict:** all seven are visibly addressed in the right files. The four that read "pending"
(CA-1 owner, CA-2 split, CA-3 date, CA-4 decision-log ID) are pending **because they are team/
institutional decisions you cannot self-make** — correct and honest. **CA-5 is the one genuine
to-do that is yours alone.**
