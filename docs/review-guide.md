# Review & analyse — complete walkthrough

The detailed companion to `docs/review-checklist.md`. Follow it top to bottom to **understand,
verify, and take ownership** of your stream before reviewers and the viva. It is written so you never
have to guess: every step gives the exact command, the output you should see, what each line means,
the precise pass/fail criteria, common problems, and where to record findings.

**Total time:** ~4–6 hours for a thorough first pass (1-hour fast path at the very end).

---

## 0. Before you start — conventions, repo map, glossary

### Conventions
- **Where to run commands:** a terminal opened at the **repo root** (the folder containing `apps/`,
  `packages/`, `docs/`). On Windows: `cd D:\files\Desktop\ls-openactive-clarence-c-block-05`. On Mac:
  `cd ~/Documents/ls-openactive`.
- **Python:** use `python` on Windows, `python3` on Mac/Linux. If `python` isn't found on Windows, try
  `py`.
- **Opening files:** use VS Code (`code .` opens the whole repo) or any text editor. Markdown (`.md`)
  is easiest to read rendered (VS Code: Ctrl/Cmd+Shift+V).
- **Recording findings:** keep `NOTES.md` open, or add comments directly in the file you're reviewing.

### Repo map (where everything lives)
```
apps/
  public-discovery/     the public app (P1): server/ (FastAPI+Jinja), client/ (React/TS), test_*.py
  staff-assurance/      the staff app (W1): role-gated workbench, test_staff.py
packages/
  application-contracts/c-block-05/   the CONTRACT: schemas, disclosure classes, invariants
  certificate-checker/  C-09 independent checker + tests
  accessible-design-system/content/   C-11 evidence-language lexicon + linter
  public-ia/            C-04 public IA state machine + validator
  staff-ia/             C-06 action-card workflow + validator
  evaluation/           C-17 condition manifests + telemetry schema + validator
  privacy/  security/  ethics/         C-13 / C-14 / C-15 models + validators
docs/
  applications/         one C-XX.md decision doc per deliverable + ADR + WCAG plan
  assurance/            C-01 register, C-16 assurance case (json + validator + rendered md),
                        ethics outline, this guide, review-checklist
  PULL_REQUEST.md, session-handoff.md, viva-evidence-map.md
```

### Glossary (so the docs read fluently)
- **Evidence states `T / F / U / B`** — supported / refuted / unknown-by-mechanism / conflict. The
  four-valued core; `U` and `B` are first-class outcomes, never "no".
- **Terminal decision** — `supported_match` / `bounded_non_match` / `evidence_indeterminate`.
- **Scope qualifier** — `scope_complete` / `scope_indeterminate` (orthogonal to the decision).
- **Recommendation action** — `authorised_slate` / `model_abstained` / `deterministic_fallback` /
  `browse_only` (separate from the evidence decision).
- **Disclosure classes** — `PUBLIC_SAFE` / `STAFF_AGGREGATE` / `STAFF_EVIDENCE` / `RESEARCH_RESTRICTED`.
  A field's class decides which surface (public/staff/research) may ever see it.
- **`C-XX`** — your work-package deliverable IDs. **`C-BLOCK-nn`** — the pre-code reconciliation
  blockers. **`CL-n`** — the assurance-case claims. **`CA-n`** — your work package's review amendments.

---

## Step 1 — Prove the ground truth (≈15 min)

**Why:** so you're analysing something that demonstrably works, not a description.

### 1a. Run the assurance case
```
python docs/assurance/validate_assurance.py
```
**Expected output (annotated):**
```
== linked tests ==
[OK ] T-contracts     ← C-BLOCK-05 schemas + 8 invariants (non-interference, replay, no-collapse…)
[OK ] T-checker       ← C-09 checker: 13 negatives + branch mutation, 0 survivors
[OK ] T-register      ← C-01 reconciliation register completeness
[OK ] T-wording       ← C-11 evidence-language linter
[OK ] T-ia            ← C-04 public IA covers every contract enum
[OK ] T-actioncard    ← §8.5 action-card gates (no skip of review/approval)
[OK ] T-conditions    ← C-17 shared-backend guarantee + confound detection
[OK ] T-publicslice   ← public app: no-JS core, a11y, disclosure, render-lint, compare, conditions
[OK ] T-staffslice    ← staff app: role gate, symmetry, authority-asymmetry, replay, workspaces
[OK ] T-privacy       ← C-13 telemetry dictionary ↔ event schema parity, transient-by-default
[OK ] T-ethics        ← C-15 activity matrix gated + no-study fallback
[OK ] T-security      ← C-14 threat register + sanitisers + secret scan
[OK ] T-conversation  ← C-08 chat↔guided convergence, confirmation, no unverified token
[OK ] T-reading       ← CA-5 K7 foundation matrix structurally sound + attestation gate active
== claims ==
[OK ] CL-1 … CL-15    each: "graph sound & evidence green; verdict=BLOCKED (…review/authority pending)"
Graph: SOUND — all linked evidence green
Maturity: 0 authorised, 15 awaiting human review/authority (expected at this stage)
```
**Pass criteria:** `Graph: SOUND`, **14 `[OK]` tests, 15 `[OK]` claims**. Every claim reading
`BLOCKED pending non-author review + authority` is **correct** — the human gates are open by design;
that is the honest state, not a failure. Note `CL-15` (K7 reading) shows green *evidence* only because
the register and gate exist; the reading itself is still 0/28 — `python
docs/assurance/validate_foundation_matrix.py` shows the live count.

**If a test is `[BAD]`:** read the one line under it.
- `No such file or directory` → the file wasn't committed. Run `git status` (untracked shows `??`),
  then `git add <folder> && git commit && git push`, and `git pull` on the other machine.
- A real assertion failure → copy the block and send it to me; it points at the exact file.

### 1b. Start both apps
Two terminals, two ports (each `uvicorn` takes over its window while running):
```
# Terminal 1 — public app
python -m uvicorn server.main:app --app-dir apps/public-discovery --port 8000
# Terminal 2 — staff app
python -m uvicorn server.main:app --app-dir apps/staff-assurance --port 8001
```
Wait for `Application startup complete`, then open `http://127.0.0.1:8000` and
`http://127.0.0.1:8001/?role=analyst`. Stop with **Ctrl+C** in each window.

**Troubleshooting:**
| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: fastapi` | deps not installed | `pip install fastapi jinja2 uvicorn` |
| `No module named render` | wrong app string | use exactly `server.main:app --app-dir apps/<app>` |
| `address already in use` | port taken | change `--port` (8002, 8003…) |
| `uvicorn: command not found` | not on PATH | use `python -m uvicorn …` (as above) |
| staff shows "Access restricted" | no role | add `?role=analyst` (that 403 is correct) |

**Record:** the date you last saw it green ("green as of <date>" is a good viva line).

---

## Step 2 — Re-read your two authority docs (scope check) (≈30 min)

**Why:** confirm the branch matches what you're *supposed* to own and that the review's binding
corrections are actually reflected.

**Open** (from your Claude project knowledge):
`CLARENCE_ZHEN_JIN_TAN_SPECIALISED_WORK_PACKAGE.md` and `review-clarence-work-package-2026-08-07.md`.

### 2a. Ownership map (§2.1) → artefact on the branch
Read the §2.1 "accountable for" table (it has **10 rows**) and tick that each has a real artefact.
Verified 2026-08-11 — full record in `docs/step2-scope-check.md`. **✓** present · **◑** partial/bounded:
| # | You own (§2.1) | On the branch | |
|---|---|---|---|
| 1 | Public application | `apps/public-discovery/` + `public-information-architecture.md` | ✓ |
| 2 | Staff application | `apps/staff-assurance/` + `staff-information-architecture.md` | ✓ |
| 3 | Conversational UX | `server/intent.py` + `/chat` + `C-08-…md` | ✓ |
| 4 | Accessibility & inclusion | `accessibility-wcag22-plan.md` + `a11y_check.py` | ◑ manual/AT testing pending (C-BLOCK-03/11) |
| 5 | Application contracts | `packages/application-contracts/c-block-05/` + `C-BLOCK-05.md` | ✓ |
| 6 | Section 15 requirements | `packages/privacy/`,`security/`,`ethics/` + `C-13/14/15-…md` | ✓ |
| 7 | Certificate checker | `packages/certificate-checker/` + `C-09-…md` | ✓ |
| 8 | Evaluation instruments | `packages/evaluation/` + `evaluation-conditions.md` | ✓ |
| 9 | Partner-facing pathway | `packages/staff-ia/` action-card machine + staff `action_card.html` | ◑ action-card only; rest is stretch (C-BLOCK-13) |
| 10 | Reproducible evidence | per-package `README.md` + `assurance-case.*` + test suites | ◑ build manifest / runbook / C-22 ledger thin |

Flag any row with **no** artefact (none is zero; rows 4/9/10 are partial by design — see the record).

### 2b. Review amendments CA-1…CA-7 — is each reflected?
| CA | What it requires | Where to verify | "Not reflected" looks like |
|---|---|---|---|
| **CA-1** | `L_reliance` referent = terminal `DecisionEnvelope` (identical across conditions) | `C-BLOCK-05.md` §6 + `C-BLOCK-15` row in `C-01-reconciliation-register.md` | referent defined against *displayed* evidence |
| **CA-2** | say whether the claim-contract author may also be the production author | `C-09-…md` §2 (open `RATIFY-09-04` question) | no mention of the split |
| **CA-3** | C-BLOCK-05 is the keystone, first date | it's **priority 1** in the register | not prioritised |
| **CA-4** | Section 08 has no RATIFY register — bind C-BLOCK-01 to a real ID | `C-BLOCK-01` row says "bind to a canonical decision-log ID" | an invented `RATIFY-08-*` |
| **CA-5** | cite by version-of-record + DOI (per-claim K7) | **your Step 7 job** — still pending | bare surnames only |
| **CA-6** | mark deliverables core vs stretch | `tier` column in the register | no core/stretch tag |
| **CA-7** | keep the authorship notice + blank §26 acceptance record | every scaffold carries the notice | a scaffold claiming to be authored |

**Record:** a "scope gaps" list (anything missing) and a "CA status" list (done vs pending). These
become PR comments and agenda items.

---

## Step 3 — Open the assurance case as your map (≈10 min)

**Why:** one index linking every claim to its evidence and its outstanding human gate.

**Open** `docs/assurance/assurance-case.md` (regenerate any time with
`python docs/assurance/validate_assurance.py`).

**How to read it:** the first table is the **live test results** (which script backs what). The
second is the **15 claims**; each shows *controls → evidence (tests) → reviewer → authority →
residual → verdict*. To analyse any deliverable, find its claim, then jump to the file/test named.
`BLOCKED` = evidence green but a human still has to sign; that is expected now.

**Machine source:** `docs/assurance/assurance-case.json` (this is what you'll edit in Step 9).

---

## Step 4 — Scrutinise the keystone hardest: C-BLOCK-05 (≈60–90 min)

**Why:** every other artefact consumes this contract. Get it right *before* freezing it with Michael
(evidence semantics) and Wesley (transport/IAM).

**Open, in order:**
1. `docs/applications/C-BLOCK-05.md` — read especially §7 (the §3 decision-table row) and **§8 "what
   to agree with Michael and Wesley"**.
2. `packages/application-contracts/c-block-05/decision-envelope.schema.json`
3. `…/application-envelope.schema.json`
4. `…/disclosure-classes.json`

### 4a. Confirm the vocabulary you'd freeze with Michael (Section 09)
These `enum`s are **proposals** until Michael confirms. For each, decide "freeze as-is" or "change":
- `evidence_state`: `T, F, U, B`
- `grade`: `explicit, schedule_derived, specification_default`
- `terminal_decision`: `supported_match, bounded_non_match, evidence_indeterminate`
- `scope_qualifier`: `scope_complete, scope_indeterminate`
- `recommendation_action`: `authorised_slate, model_abstained, deterministic_fallback, browse_only`
- `mechanism` (for U/B): `source_absence, linked_source_failure, unresolved_inheritance,
  invalid_or_ambiguous_value, conflicting_value, vocabulary_failure, projection_loss, staleness,
  spatial_uncertainty`
- `claim_type`: `listing_attribute, match_cardinality, bounded_non_match, uncertainty, process`
- checker outcomes (in `packages/certificate-checker/certificate.schema.json` + C-09): `PASS,
  FAIL_MALFORMED, FAIL_MISSING_WITNESS, FAIL_UNRESOLVED_RECEIPT, FAIL_DIGEST_MISMATCH,
  FAIL_VERSION_MISMATCH, FAIL_ILLEGAL_ESCALATION, FAIL_SCOPE_INCONSISTENCY, FAIL_UNSUPPORTED_FRAGMENT`

### 4b. Disclosure spot-check — the single highest-risk review
Open `disclosure-classes.json`. The rule: only `PUBLIC_SAFE` fields may ever reach the public surface.
**Verify these high-risk fields are NOT `PUBLIC_SAFE`:**
| Field | Must be | Why (harm if leaked) |
|---|---|---|
| `internal_score` | STAFF_AGGREGATE | ranking utility → looks like a public "best for you" |
| `receipts` / `content_digest` | STAFF_EVIDENCE | raw provenance |
| `lineage_note` | STAFF_EVIDENCE | source lineage prose |
| `why_not[].predicate_id/blocking_state` | STAFF_EVIDENCE | internal gate reasoning |
| `model_version` / `policy_version` | STAFF_AGGREGATE | operational internals |
| `claims[].verification` | STAFF_EVIDENCE | verifier outcome |
| `episode_id` / `trace_id` | RESEARCH_RESTRICTED | session identity |
| `coarsened_origin` | STAFF_AGGREGATE | even coarsened, not public |
If any of those reads `PUBLIC_SAFE`, that's a leak — flag it. Conversely confirm the fields users
*need* are `PUBLIC_SAFE`: `terminal_decision`, `scope_qualifier`, `recommendation_action`,
`coverage_qualifier.statement`, candidate `id/rank/pool`, predicate `evidence_state/mechanism/grade`,
`digest`, `vintage`.

### 4c. Run the invariants and read what they prove
```
python packages/application-contracts/c-block-05/projection_and_invariants.py
```
Expected: valid fixtures **PASS** all 8 invariants; each adversarial fixture is **DETECTED** by its
targeted gate (e.g. `unknown_rendered_as_no → INV-NO-COLLAPSE`, `staff_note_in_public →
INV-DISCLOSURE`, `tampered_public_digest → INV-REPLAY`). This is the executable proof that the
disclosure/collapse/replay rules hold.

**Record:** two lists — **"confirm with Michael (Section 09)"** (enums/wording) and **"confirm with
Wesley (transport/IAM/layout)"** — plus any disclosure class to change. These are the C-BLOCK-05
contract-workshop agenda.

---

## Step 5 — Walk the rest in dependency order (≈90 min)

For **each** artefact: read the doc, run the check (annotated below), and apply the three acid tests
— **(a) over-claim?** (banned words: safe, secure, best for you, fully accessible, compliant, first,
production-ready — should read "evaluated toward / candidate / PROPOSED"); **(b) independence
blurred?**; **(c) honest status (PROPOSED, not "done")?**

### C-09 — certificate checker
Doc: `docs/applications/C-09-certificate-checker.md`. Run:
`python packages/certificate-checker/test_certificate_checker.py`
Expect: golden `PASS`; **13 negatives each hit their exact `FAIL_*` code**; **all 8 branches killed
under mutation (0 survivors)**. Check §10.4 independence still reads: no production import, "do not
call production to determine expected output", "cannot certify your own checker".

### C-01 — reconciliation register
Doc: `docs/assurance/C-01-reconciliation-register.md`. Run:
`python docs/assurance/validate_register.py`
Expect: `REGISTER OK: 15 blockers … no blank cells`. Read the 15 rows; confirm the institutional cells
(approver/date/decision_log_ref) say **PENDING** (not fabricated). Confirm `C-BLOCK-15` (CA-1) exists.

### C-11 — evidence language
Doc: `docs/applications/content-and-evidence-language.md`. Run:
`python packages/accessible-design-system/content/render_lint.py`
Expect: completeness OK; a compliant render passes; an over-claiming render + the `unknown_rendered_as_no`
fixture are **flagged**. Read the banned/approved wording tables — this is where you'll do a lot of
Step-7 rewriting in your own voice.

### C-02 / C-04 — actors & public IA
Docs: `actors-and-jobs.md` (actors all HYPOTHETICAL until partner-validated), `public-information-architecture.md`.
Run: `python packages/public-ia/validate_ia.py`
Expect: `IA OK` + a coverage map showing **every** `action_kind`, terminal decision, recommendation
action and `scope_indeterminate` has a distinct screen, plus non-chat/non-map/no-JS fallbacks.

### C-06 — staff IA + action cards
Doc: `staff-information-architecture.md`. Run: `python packages/staff-ia/validate_action_cards.py`
Expect: `ACTION-CARD WORKFLOW OK` — no transition skips independent review/approval; send needs an
authorised role; a correction token can only create `observed`.

### The apps (deep-dive is Step 6)
Run: `python apps/public-discovery/test_slice.py` and `python apps/staff-assurance/test_staff.py`
Expect: `ALL SLICE CHECKS PASS` / `ALL STAFF SLICE CHECKS PASS`.

### C-17 — evaluation conditions
Doc: `evaluation-conditions.md`. Run: `python packages/evaluation/validate_conditions.py`
Expect: capability ladder OK; **each family's decision identical per task** (shared backend); a
confounded binding **detected**; event schema validates and rejects a `raw_utterance` field.

### C-13 / C-14 / C-15 — Section 15 trio
Docs: `C-13-privacy-telemetry.md`, `C-14-security-abuse.md`, `C-15-ethics-responsible-ai.md`. Run:
`python packages/privacy/validate_privacy.py`, `…/security/validate_security.py`,
`…/ethics/validate_ethics.py`. Expect each `… MODEL OK`. Confirm the honest "coordinate, not decide"
framing: you maintain the pack; the governance/ethics **authority** decides.

### C-08 — conversation
Doc: `C-08-conversational-integration.md`. Run: `python apps/public-discovery/test_conversation.py`
Expect: `ALL CONVERSATION CHECKS PASS` — convergence, confirmation gate, clarify-not-fabricate, no
unverified token, safe degradation, a11y.

### C-16 — assurance case
Doc: `C-16-assurance-case.md`. Already run in Step 1; confirm orphan detection is described and the
verdicts are honestly BLOCKED.

**Record:** per artefact, a one-line verdict + any wording to soften in Step 7.

---

## Step 6 — Experience the apps as a user (≈30 min)

**Public** (`http://127.0.0.1:8000`) — click each and confirm the expected behaviour:
| Do | URL | Expect |
|---|---|---|
| Supported | `/discover?scenario=supported` | "Matches your confirmed needs"; two options; **price "not published"** (never "free") |
| No match | `/discover?scenario=no_match` | "No listed match…" **plus a coverage line**; not "nothing exists" |
| Can't answer | `/discover?scenario=indeterminate` | "We can't tell…"; **scope notice shown** even though it's a non-result |
| Service failure | `/discover?scenario=service_failure` | "Something went wrong"; **no stale result reused** |
| Vague chat | `/chat?q=find me something fun` | **clarifies** (asks), does **not** invent a result |
| Access chat | `/chat?q=swimming in Croydon with step-free access` | **confirmation** step before any result |
| Compare | `/compare?scenario=supported` | evidence per option; **no "winner"** |
| Conditions | `/discover?scenario=supported&condition=P0` vs `…&condition=P1` | same options/order; P0 hides evidence detail, P1 shows it |

**Staff** (`http://127.0.0.1:8001`):
| Do | URL | Expect |
|---|---|---|
| No role | `/` | **403 "Access restricted"** (correct — no staff content) |
| Workbench | `/?role=analyst` | list of workspaces |
| Replay | `/replay?scenario=supported&role=analyst` | **PASS — identical** (digest replays) |
| Failure chain | `/failure-chain?scenario=indeterminate&role=analyst` | acquisition→evidence→gate→interface |
| Per-role send | `/action-card?state=approved_for_route&role=analyst` vs `…&role=authoriser` | "send" is **not permitted** for analyst, **permitted** for authoriser |
| Equity audit | `/equity-audit?scenario=indeterminate&role=analyst` | contextual (area/scope); **no league table** |

**Record:** honest UX notes — anything confusing, any wording you'd change.

---

## Step 7 — Correct into your own words + record K7 (your individual mark) (≈ ongoing)

**Why:** this converts "AI-assisted scaffold" into *your authored work*. **I cannot do this** — the
words under your name must be yours (WP §10 hard rule). It also directly serves LO5 and your
reflective account.

### 7a. Rewrite in your voice
For each doc you keep: read it, then **rewrite the prose in your own words** (edit the file). Don't
just paraphrase mechanically — say why the choice is right as *you* understand it. Keep the
authorship-notice line until a doc is genuinely yours, then update it to reflect that you authored it.

### 7b. Keep a K7 reading log — scaffold already built
The register exists: `docs/assurance/foundation-matrix.json` (28 §18.1 sources, empty §18.3
attestation columns) → `python docs/assurance/validate_foundation_matrix.py` renders
`docs/assurance/reading-log.md` and reports `K7 attestation: n/28`. **To complete a row:** read the
primary source, then in the JSON set its `personally_read=true`, fill `version_of_record.doi` + set
`verified=true`, and complete `date_accessed`, `sections_pages_read`, `claim_supported`,
`exact_limit_or_non_claim` and — in your own words — `clarence_independent_verdict`; re-run and the
row flips to ✅. The validator enforces CA-5/§18.3: it FAILs if you mark a source read without a
verified DOI + your verdict, and rejects a load-bearing preprint where a version of record exists.
Start with the high-priority set the log lists first (the reliance, explanation, uncertainty,
accessibility and verification clusters). Verify each `full_citation_proposed` against the record —
they're a scaffold, not gospel.

### 7c. The load-bearing reading (WP §18.1) mapped to what it supports
| Theme | Read | Supports |
|---|---|---|
| Human–AI reliance | Lee & See 2004; Parasuraman & Riley 1997; Buçinca 2021; Bansal 2021 | CL-1 reliance framing; §13 `L_reliance` |
| Explanation why/why-not | Tintarev & Masthoff 2012; Nunes & Jannach 2017; Lim 2009 | evidence cards / why-not |
| Conversational rec. | Jannach 2021/2023 | C-08 scope + evaluation limits |
| HCI interaction | Amershi 2019; Ashktorab 2019 | expectation-setting, failure recovery |
| Visual analytics eval | Munzner 2009; Lam 2012; Sarikaya 2019 | staff dashboards / a11y-of-charts |
| Uncertainty communication | van der Bles 2019/2020; MacEachren 2005; Kinkeldey 2017 | rendering U/B without false precision |
| Accessibility | Power 2012; Petrie & Kheir 2007; **WCAG 2.2**; **GOV.UK** | C-12 (scanning ≠ accessibility) |
| Privacy by design | Hoepman 2014; LINDDUN | C-13 |
| RAG / verification / constrained gen | Lewis 2020; Thorne 2018; Scholak 2021; Rashkin 2023; Niu 2024 | C-08 / C-BLOCK-10 |
| Prompt-injection / security | archival USENIX/CCS sources | C-14 |
Operational (current, not peer-reviewed proof): OpenActive docs; ICO/NCSC/NIST; Bristol ethics/DP
procedures; exact model-provider terms.

**Record:** the reading log itself is the evidence.

---

## Step 8 — Your two cross-reviews (C-19, C-20) (≈2–3 h across the project)

**Why:** a deliverable *and* proof of your independence. Write in your own words. You may need their
latest work: `git fetch origin`, then read `origin/fahmi/proposal-v2-sections-6-7` (Fahmi) and
Michael's evidence files, or read on GitHub.

**Where to write:** `docs/reviews/clarence-review-michael-evidence.md` and
`…-fahmi-evaluation.md`. Use the WP §17.1 **review-record schema**: `review_id | artefact_and_version
| scope | methods | findings_by_severity | evidence_refs | owner_response | disposition |
retest_evidence | remaining_limitations`. Severity: blocker / major / minor / nit. **A review that
cannot fail is not evidence — record real findings.**

**C-19 — Michael's evidence stream (§17.1 questions):**
1. Is every application-facing state mutually distinguishable and schema-valid?
2. Can every factual claim resolve to a receipt and a compatible release?
3. Do spec-default / schedule-derived grades have accurate user wording?
4. Can unknown / conflict / scope / service-failure be confused?
5. Are high-consequence fields prevented from silent defaulting?
6. Are checker witnesses sufficient but minimal?
7. Do renderers preserve match and bounded-non-match soundness?
8. Are correction and version-mismatch behaviours defined?

**C-20 — Fahmi's evaluation stream (§17.2 questions):**
1. Do task cases correspond to real application states/actions?
2. Are P0/P1/P2 and W0/W1/W1-NA differences accurately described?
3. Are application failures retained in denominators?
4. Do labels measure comprehension/action/usefulness, not preference alone?
5. Can assessors stay blind/eligible given interface ownership?
6. Do telemetry events answer the estimands without unnecessary personal data?
7. Are accessibility modes represented without disability proxies as identities?
8. Do staff metrics retain denominators/vintages/weighting/uncertainty?

---

## Step 9 — Act on the PR (close the human gates) (≈ ongoing)

**Why:** turn green-but-pending claims into AUTHORISED as reviews and decisions land.

### 9a. Which reviewer/authority unlocks which claim
| When this signs… | …these claims can flip |
|---|---|
| Michael (evidence semantics, `RATIFY-09-04`) | CL-1, CL-3, CL-6 |
| Wesley (transport + real IAM) | CL-1, CL-5 |
| Fahmi (evaluation parity) | CL-4, CL-7 |
| Non-author HCI/accessibility reviewer (C-BLOCK-03) | CL-2, CL-10 |
| Governance / DPIA (`RATIFY-15-02/04`) | CL-11 |
| Bristol PGT ethics (`RATIFY-15-03`) | CL-12 |
| Security/assurance reviewer (`RATIFY-15-07`) | CL-13 |
| Section 08 owner (C-BLOCK-01) | CL-14 |
| Section 18 owner | CL-8 |
| Team ratification (`RATIFY-19-04/06`) | CL-9 |

### 9b. Flip a claim (worked example)
In `docs/assurance/assurance-case.json`, for the claim, change the reviewer and/or authority blocks:
```json
"reviewer":  { "scope": "…", "eligible_non_author": true, "status": "done", "name": "A. Reviewer" },
"authority": { "decision": "…", "holder": "Dr X (role)", "status": "done" }
```
Then re-run `python docs/assurance/validate_assurance.py`. That claim's verdict flips
**BLOCKED → AUTHORISED**.

**Done means:** all 15 claims read **AUTHORISED** *and* your Step-7 authorship pass is complete. That
is the difference between "green and drafted" and "genuinely finished".

---

## Appendix A — run-everything cheat-sheet
```
python docs/assurance/validate_assurance.py                                   # the lot, live
python packages/application-contracts/c-block-05/projection_and_invariants.py # contract invariants
python packages/certificate-checker/test_certificate_checker.py              # checker
python docs/assurance/validate_register.py                                    # reconciliation
python packages/accessible-design-system/content/render_lint.py              # wording
python packages/public-ia/validate_ia.py                                      # public IA
python packages/staff-ia/validate_action_cards.py                            # action cards
python packages/evaluation/validate_conditions.py                            # conditions
python packages/privacy/validate_privacy.py                                   # privacy
python packages/security/validate_security.py                                 # security
python packages/ethics/validate_ethics.py                                     # ethics
python apps/public-discovery/test_slice.py                                     # public app
python apps/public-discovery/test_conversation.py                             # conversation
python apps/staff-assurance/test_staff.py                                      # staff app
python docs/assurance/validate_foundation_matrix.py                            # K7 reading log (CA-5)
```

## Appendix B — the 1-hour fast path
Step 1 (run it) → Step 4 (the contract) → Step 6 (click the apps). Enough to trust it and spot the
one or two things you'd change before reviewers see it.

## Appendix C — honesty guardrails (say these plainly)
- "Evaluated **toward** WCAG 2.2 AA within a tested matrix" — never "fully accessible".
- "**Candidate** contribution, pending the §17 incumbent audit" — never "novel/first".
- "**Research demonstration**" — never "deployed/production".
- "**Limited technical independence**" checker — never "independent" without the qualifier.
- Every artefact is a **PROPOSED scaffold** until you've authored it in your words and a non-author
  has reviewed it. Volunteering the limit is itself evidence of the discipline the project rewards.
