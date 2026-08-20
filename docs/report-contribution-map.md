# Report contribution map — what your stream lets you write (Group 41 report)

**How to use:** for each report subsection below, this lists the points to make and the *exact evidence
to cite from your branch*. Write the prose in your own words — this is a scaffold, not paragraphs to
paste. Everything here is expressible inside the claim boundary (research demonstration, "evaluated
toward", PROPOSED). Sections 3.2–3.7 are yours; 3.1 (data) and the recommender/elicitation are
teammates'. Figures/tables marked ★ I can generate from your real data.

## 1.4 Scope and Claims Boundary (you can supply the applications' half)
- State plainly what the applications *do* and *do not* claim: a **research demonstration**, not a
  deployment; **"evaluated toward WCAG 2.2 AA within a tested matrix"**, not conformance; no
  human-effect, booking, or fairness claims.
- Cite the executable enforcement: the evidence-language linter that flags over-claiming terms
  ("best for you", "guaranteed", "fully accessible", "free" over unknown).
- Evidence: `packages/accessible-design-system/content/render_lint.py`; maturity label
  `research_demonstration`.

## 1.6 Contributions (your bullet or two)
- An **evidence-symmetric but authority-asymmetric** pair of applications over one certified contract;
  an **independent certificate checker**; **fail-closed disclosure-class projection** with executable
  invariants; a **conversational surface that never authorises facts**; accessibility **evaluated
  toward WCAG 2.2 AA**; and an **executable assurance case**.

## 3.2 Evidence Certification and the Independent Checker  (your C-09)
- Points: production emits a certificate/witness; a **deliberately small checker with limited
  technical independence** verifies it — imports no production code, never calls production to decide
  the expected answer, implements only the frozen contract, and **fails closed**.
- Evidence to cite: **13 negative cases each rejected with its exact `FAIL_*` code**; **branch-mutation
  testing kills all 8 decision branches (0 survivors)**; independence rules (WP §10.4).
- ★ **Table:** negative case → `FAIL_*` code (13 rows) from `test_certificate_checker.py`.
- Honest limit: *limited technical* (not external) independence; you cannot certify your own checker —
  needs a non-author code review + `RATIFY-09-04`.

## 3.3 Conversational Discovery Surface  (your C-08)
- Points: deterministic typed-intent parse; **chat and guided search converge on the same certified
  DecisionEnvelope**; a **confirmation gate** for high-consequence constraints; **clarify, don't
  fabricate** on unclear input; **verify-before-render** (no unverified token reaches the user); safe
  degradation when the model is off.
- Evidence: `test_conversation.py` (11 checks); `C-BLOCK-10`; `INV-NO-UNVERIFIED`.
- Honest limit: the current parser is deterministic; a real LLM plugs in *behind the same contract*;
  the prompt-injection battery is still to be run.

## 3.4 Public Discovery Dashboard  (your public app)
- Points: **FastAPI SSR + React/TS progressive enhancement with a no-JavaScript core** (ADR-0001); the
  four honest outcome states rendered as **distinct screens** (supported / no listed match /
  can't-answer / service problem); missing price shown as **"not published", never "free"**; a scope
  notice on can't-answer; compare with **no "winner"**; the evaluation conditions P0/P1/P2.
- Evidence: `test_slice.py` (19 checks); the IA validator covers **every contract enum**; 4 fixed
  scenarios.
- ★ **Figure:** the four public states (screenshots) — the clearest single illustration of the thesis.
- Honest limit: fixed demonstration scenarios; no live data, booking, or payment.

## 3.5 Internal Staff Assurance Dashboard  (your staff app)
- Points: a **role-gated workbench** (403 without a role, server-side); **eight workspaces** (replay,
  failure-chain, collection-health, action-card, bounded-scenario, recommender-assurance,
  equity-audit, release-incident); a **per-role capability ladder** (analyst / assurance / authoriser)
  where review, approval and send are separated (§8.5); **provenance on every panel**; no league
  tables, no productivity monitoring.
- Evidence: `test_staff.py` (40 checks) — including **evidence-symmetry**, **authority-asymmetry**
  (`internal_score`/`model_version` staff-only), replay, non-interference, and the role send-ladder
  (analyst cannot send; only an authoriser can).
- ★ **Table:** role → capability matrix. ★ **Figure:** the workbench card dashboard (screenshot).
- Honest limit: the role gate is a demonstration **stub**; real IAM is Wesley's (Section 16).

## 3.6 Disclosure Separation and Assurance Controls  (your C-BLOCK-05 + C-16)
- Points: **one staff-complete `DecisionEnvelope`** with a **fail-closed, class-driven projection** —
  the public view is *derived*, never a second document; **field-level disclosure classes**; **eight
  executable release invariants** (disclosure, non-interference, symmetry, replay, no-unverified,
  no-collapse, coverage, slate-order); **value-level non-interference**; **semantic replay via a
  digest**; and an **executable assurance case** (15 claims, live checks, orphan detection).
- Evidence: `projection_and_invariants.py` — 2 valid fixtures pass all gates, **6 adversarial fixtures
  each caught by their targeted gate**; the **F1 finding** (a real disclosure leak — the failure page
  named an internal stage — found in review and fixed); the assurance case is **graph-SOUND, evidence
  green, 15 claims BLOCKED pending human sign-off** (the honest state).
- ★ **Table:** disclosure classes (field → class). ★ **Table:** the 8 invariants → what each guards.
- Honest limit: the contract is **PROPOSED, not frozen** — needs the Michael/Wesley contract workshop.

## 3.7 Accessibility  (your C-12)
- Points: target **WCAG 2.2 AA and evaluate *toward* it within a declared matrix** (not conformance
  from a scan); no-JS core; a static automated subset **plus** a planned manual keyboard/screen-reader/
  AT matrix; automatic light/dark; visible focus; 44px targets; **redundant coding** (colour is never
  the only signal — every evidence state carries text).
- Evidence: `a11y_check.py` (explicitly "one input, not conformance"); `accessibility-wcag22-plan.md`.
- Honest limit: manual/AT testing is **outstanding** and needs a **non-author HCI reviewer**
  (`C-BLOCK-03`); hence "evaluated toward AA", not "accessible".

## 3.8 (template placeholder — replace)
The "Example Section" and the "example figure/table/algorithm" entries are LaTeX boilerplate — swap
them for the real figures/tables above.

## 4 Critical Evaluation (your honest limits — a strength here, not a weakness)
- The stream is a **research demonstration of PROPOSED scaffolds**: tests are green but **0/15
  assurance claims are AUTHORISED** — all correctly BLOCKED pending non-author review and named
  authorities. Say this plainly; the discipline *is* the contribution.
- Name the **falsification conditions** (WP §19.4): the contribution narrows if public/staff disagree
  on retained semantics, restricted values leak, the interface bypasses abstention/order, unsupported
  model text reaches users, or the incumbent audit shows the integration already exists.
- Use the **F1 leak** as evidence the discipline works: a review found a real over-share and a
  regression test now prevents it.

## Appendix A — reproducibility (you can own this)
- One-command verification: `python docs/assurance/validate_assurance.py` (14 suites live). The run
  guide `docs/RUN-apps.md`. The branch `clarence/c-block-05` and the open PR.

---
*Write these in your own words. Send me any subsection draft and I'll check it covers the substance,
stays inside the claim boundary, and reads like you — and I'll generate any of the ★ figures/tables.*
