# Clarence's stream — twin applications, conversational UX, accessibility & Section 15 assurance (PROPOSED)

**Branch:** `clarence/c-block-05` · **Status:** PROPOSED for review + ratification · **Maturity:** `research_demonstration` (C-BLOCK-12)

> **Authorship & status notice.** These artefacts are **AI-assisted scaffolds** prepared from the
> canonical protocols and my work package. They are **not** evidence that I authored, read, accepted
> or completed the work in my own words yet, and nothing here is ratified. Every file carries this
> notice. I am opening this PR to (a) commit the stream into the private repo (it must live here, not
> outside it) and (b) request the specific non-author reviews and team decisions listed below.

## What this adds

My stream (public + staff applications, conversational UX, accessibility, the Section 15 assurance
requirements, the independent certificate checker, and the frozen evaluation instruments), built as
interlocking artefacts over **one** certified evidence contract. 13 commits; 15 decision docs; 12
executable validators/test-suites; two runnable FastAPI apps.

## How to verify in one command

```bash
python docs/assurance/validate_assurance.py
```

This **executable assurance case** runs all 14 linked checks live and prints the graph. Expected:
`Graph: SOUND — all linked evidence green`, with all **15 claims BLOCKED pending non-author review +
authority** (the honest state). Individual suites can be run directly (see each package README).

## Deliverables

| Area | Deliverables | Evidence |
|------|--------------|----------|
| Contracts | C-BLOCK-05 `ApplicationEnvelope`/`DecisionEnvelope` + disclosure classes; CA-1 `L_reliance` binding | schema validation + 8 invariants |
| Assurance | C-09 independent certificate checker; C-10 projection suite; C-16 executable assurance case | negatives + mutation; non-interference/replay; orphan detection + live runs |
| Governance | C-01 reconciliation register (15 C-BLOCKs) | completeness validator |
| UX foundations | C-02 actors/jobs; C-04 public IA; C-06 staff IA + action-card workflow; C-11 evidence-language + linter | IA coverage; §8.5 gates; wording linter |
| Applications | Public discovery app (P1) incl. guided/list/**chat (C-08)**/detail/**compare**/handoff; Staff assurance app (W1) incl. replay, failure-chain, collection-health, action-card, **4 more workspaces**, per-role matrix | `test_slice.py`, `test_conversation.py`, `test_staff.py` |
| Evaluation | C-17 conditions P0/P1/P2 & W0/W1/W1-NA (shared-backend, C-BLOCK-06) + telemetry event schema | condition validator + confound detection |
| Section 15 | C-13 privacy/telemetry; C-14 security/abuse; C-15 ethics/responsible-AI | 3 validators |
| Accessibility | ADR-0001 (SSR + progressive enhancement, no-JS core); WCAG 2.2 AA plan (C-12) | static a11y subset (one input only) |

## Non-author reviews requested (you cannot approve your own — WP §2.6)

- **Michael** — evidence semantics + claim vocabulary (C-BLOCK-05 enums; C-09 checker contract, `RATIFY-09-04`; C-BLOCK-10 render obligation).
- **Wesley** — transport/versioning + **real IAM** replacing the staff role stub (C-BLOCK-04, `RATIFY-15-06`); repo layout for `apps/`/`packages/`.
- **Fahmi** — evaluation parity (P0/P1/P2, W0/W1/W1-NA map to real builds; `RATIFY-14-07/08`).
- **Non-author HCI/accessibility reviewer** — manual keyboard/screen-reader/AT/contrast testing (C-BLOCK-03, `RATIFY-14-02`); the automated check is only one input.

## Team decisions requested

- `RATIFY-19-04` (stream ownership) and `RATIFY-19-06` (feasible reviewer/assessor matrix).
- **Section 08** accountable owner + component split (C-BLOCK-01/CA-4) — bind to a real decision-log ID.
- **Section 15** authorities + Bristol **PGT ethics** determination (`RATIFY-15-*`) and the **DPIA** sign-off.
- Partner validation of the actors (`RATIFY-14-03`); Section 18 owner (C-BLOCK-13).

## Explicitly NOT claimed

No conformance ("evaluated *toward* WCAG 2.2 AA within a tested matrix" only); no human-effect /
usability / lived-equity claims (no ethics approval yet — operating under the no-study fallback); no
public deployment (local/authorised-staging only); no "chatbot owner" title until Section 08 is
ratified. `data/` is not committed; `node_modules` is git-ignored.

## Notes for reviewers

- Run the apps locally: `uvicorn server.main:app --app-dir apps/public-discovery` and
  `… --app-dir apps/staff-assurance` (staff routes need `?role=analyst|assurance|authoriser` or the
  `x-staff-role` header). Maturity is a research demonstration.
- The assurance case is the map: each claim links to the exact test(s) that evidence it and names the
  reviewer + authority still required. Populating `reviewer.name`/`status` and `authority.holder`/
  `status` in `docs/assurance/assurance-case.json` — only after the real reviews — moves a claim to
  AUTHORISED.
