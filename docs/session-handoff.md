# Session handoff — Clarence's stream build (portable record)

**Branch:** `clarence/c-block-05` · **Repo:** github.com/michaelsamuel2005/ls-openactive · **PR:** open
**Purpose of this file:** a portable record of what this working session produced and how to resume it on any machine (local Cowork chats don't sync across devices; this file + the branch do).

> Everything below is committed to `clarence/c-block-05`. On another laptop: `git clone` / `git pull`
> the branch and you have all of it. These are **AI-assisted scaffolds (PROPOSED)** — correct them
> into your own words and obtain the non-author reviews before they count as authored.

## What this session did

1. Cloned `michaelsamuel2005/ls-openactive` to `~/Documents` and connected it.
2. Oriented the repo: found it's a stratigraphy of two pivots — "Closing the Activity Gap" (equity
   re-ranker) → "Evidence-Bounded Activity Discovery" (main's proposal) → "Evidence-Bounded
   **Conversational** Activity Discovery" (your work-package world, on `fahmi/proposal-v2-...`).
3. Built your entire specialised stream as interlocking, executably-tested drafts on one contract.

## Deliverables (all on the branch)

| ID | Deliverable | Location |
|----|-------------|----------|
| C-BLOCK-05 | Application/Decision envelope schemas + disclosure classes + invariants | `packages/application-contracts/c-block-05/` · `docs/applications/C-BLOCK-05.md` |
| C-09 | Independent certificate checker (+ negatives + mutation) | `packages/certificate-checker/` · `docs/applications/C-09-…md` |
| C-01 | Reconciliation register (15 C-BLOCKs) | `docs/assurance/reconciliation-register.json` + validator |
| C-11 | Evidence-language lexicon + wording linter | `packages/accessible-design-system/content/` |
| C-02 / C-04 | Actors/jobs + public IA state machine + validator | `docs/applications/…` · `packages/public-ia/` |
| C-06 | Staff IA + action-card workflow + validator | `docs/applications/staff-…md` · `packages/staff-ia/` |
| Public app (P1) | FastAPI SSR + React/TS PE, no-JS core; guided/list/**chat**/detail/**compare**/handoff | `apps/public-discovery/` |
| Staff app (W1) | Role-gated workbench: replay, failure-chain, collection-health, action-card, bounded-scenario, recommender-assurance, equity-audit, release-incident; per-role matrix | `apps/staff-assurance/` |
| C-08 | Conversational integration (deterministic; chat↔guided convergence; C-BLOCK-10) | `apps/public-discovery/server/intent.py` + `/chat` |
| C-17 | Evaluation conditions P0/P1/P2, W0/W1/W1-NA + telemetry schema + shared-backend validator | `packages/evaluation/` |
| C-13 | Privacy/telemetry dictionary + validator | `packages/privacy/` |
| C-14 | Security/abuse register + sanitisers + validator | `packages/security/` |
| C-15 | Ethics activity matrix + validator; ethics application outline | `packages/ethics/` · `docs/assurance/ethics-application-outline.md` |
| C-16 | Executable assurance case (runs all checks live; orphan detection) | `docs/assurance/assurance-case.json` + `validate_assurance.py` |
| — | ADR-0001 (stack), WCAG 2.2 AA plan, PR description | `docs/applications/` · `docs/PULL_REQUEST.md` |

## Verify on any machine (one command)

```bash
python docs/assurance/validate_assurance.py
```

Runs all 13 linked checks live. Expected: **Graph SOUND — all evidence green**; **14 claims BLOCKED
pending non-author review + authority** (the honest state). Needs Python 3.10+; the two app tests
need `pip install fastapi jinja2 httpx`.

## Run the apps

```bash
pip install fastapi jinja2 uvicorn --break-system-packages
uvicorn server.main:app --app-dir apps/public-discovery --reload --reload-dir apps/public-discovery
# public: http://127.0.0.1:8000  (try /chat, /compare, the outcome radios)
uvicorn server.main:app --app-dir apps/staff-assurance --reload --reload-dir apps/staff-assurance
# staff (role required): add ?role=analyst|assurance|authoriser  e.g. http://127.0.0.1:8000/?role=analyst
```

## Current state

- **PR is open** on `clarence/c-block-05` (body = `docs/PULL_REQUEST.md`).
- Assurance case: **14 claims, evidence green, all BLOCKED pending human sign-off.**
- Maturity: `research_demonstration` only. No conformance / no human-effect / no deployment claims.

## What's left (not code)

- **Non-author reviews:** Michael (evidence/checker), Wesley (transport/**IAM** — replaces the role
  stub), Fahmi (evaluation parity), a non-author **HCI/accessibility** reviewer (manual/AT testing).
- **Team/institutional decisions:** `RATIFY-19-04/06`; Section 08 owner (C-BLOCK-01); Section 15
  authorities + **Bristol PGT ethics** + **DPIA**; partner validation of actors (`RATIFY-14-03`).
- **Yours personally:** correct scaffolds into your own words + K7 primary-source reading; C-19/C-20
  cross-reviews of Michael & Fahmi; C-22 contribution ledger + reflective account.
- **Optional code left:** public map view (needs a tiles/library decision with Wesley).

## To resume the chat's momentum elsewhere

There's no verbatim chat export (local Cowork sessions store history on this machine only). Use this
file as the resume point: on the other laptop, pull the branch, run the verify command, and pick up
from "What's left". As reviews land, set `reviewer.name`/`status` + `authority.holder`/`status` in
`docs/assurance/assurance-case.json` and re-run `validate_assurance.py` — claims flip to AUTHORISED.
