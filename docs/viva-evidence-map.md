# Viva evidence-map — the ten explanation points (structure + evidence, not answers)

**Purpose:** for each of your work package's §22 explanation points, where the evidence lives on the
branch, the key facts to anchor from, and the honest limit to volunteer. **The spoken answers are
yours** — this is a rehearsal scaffold and evidence index, not a script (WP §10 hard rule; §21).

> Run `python docs/assurance/validate_assurance.py` before the viva: it re-proves every claim below
> live, so you can say "and it's green as of this morning" truthfully.

## 1. Why two applications but one evidence truth
- **Evidence:** `packages/application-contracts/c-block-05/` (one `DecisionEnvelope`, two projections); `INV-NONINTERFERENCE`, `INV-SYMMETRY`; staff `test_staff.py` (evidence-symmetry + authority-asymmetry).
- **Key facts:** public and staff are *projections* of the same decision; evidence-symmetric, authority-asymmetric; the public view is derived (fail-closed), never a second document.
- **Limit:** it's a research demonstration; the contribution is the *evaluated integration*, pending the §17 incumbent audit.

## 2. Evidence decision vs scope limitation vs model abstention vs service failure
- **Evidence:** `§4.2` vocabulary in the schema (`terminal_decision`, `scope_qualifier`, `recommendation_action`, `action_kind`); `INV-NO-COLLAPSE`, `INV-COVERAGE`; public app renders each as a **distinct screen** (`test_slice.py`).
- **Key facts:** four orthogonal axes; `bounded_non_match` ≠ `evidence_indeterminate` ≠ `model_abstained` ≠ `service_failure`; unknown (`U`) never rendered as "no".
- **Limit:** the taxonomy is enforced in the interface; upstream truth is Michael's.

## 3. Why the chatbot cannot be allowed to authorise facts
- **Evidence:** C-08 (`intent.py`, `/chat`, `test_conversation.py`); C-BLOCK-10; `INV-NO-UNVERIFIED`.
- **Key facts:** the model interprets/communicates; a deterministic verifier authorises every rendered claim; chat and guided **converge on the same DecisionEnvelope**; unclear input clarifies rather than fabricates; safe degradation when the model is off.
- **Limit:** the current parser is deterministic; a real LLM plugs in *behind* the same contract, and the injection battery still has to be run.

## 4. How staff replays a public output without leaking staff-only information
- **Evidence:** staff app `/replay` (`render.replay`); `INV-REPLAY`; disclosure classes; `test_staff.py` (authority-asymmetry, no research-identity leak).
- **Key facts:** staff recompute the digest of the *retained public payload* (semantic replay, C-BLOCK-09); the projection is fail-closed so `internal_score`/receipts/lineage never reach the public plane.
- **Limit:** person-level review of projections is still pending (non-author reviewer).

## 5. Why WCAG scanning alone is insufficient
- **Evidence:** `docs/applications/accessibility-wcag22-plan.md` (C-12); `a11y_check.py` (explicitly "one input"); ADR-0001 no-JS core.
- **Key facts:** automated checks catch structure only; contrast, screen-reader output and focus behaviour are manual; one examiner-found failure falsifies a blanket claim — hence "evaluated **toward** WCAG 2.2 AA within a tested matrix" (grounded in GOV.UK → WCAG 2.2 AA).
- **Limit:** manual/AT testing + a non-author HCI review (C-BLOCK-03) are outstanding.

## 6. What Section 15 evidence you coordinate vs decisions you cannot make
- **Evidence:** C-13 (`packages/privacy/`), C-14 (`packages/security/`), C-15 (`packages/ethics/`); `docs/assurance/ethics-application-outline.md`.
- **Key facts:** you *maintain the evidence pack*; you **cannot** issue the controller/processor or lawful-basis determination, the ethics approval, security certification, residual-risk acceptance or deployment authority — those are named authorities (§2.4).
- **Limit:** all three packages are green on their own checks but every maturity gate is `pending` a human authority.

## 7. How the certificate checker differs from a second interpreter
- **Evidence:** C-09 (`packages/certificate-checker/`), `§10.4` independence rules; `test_certificate_checker.py` (13 negatives + branch mutation, 0 survivors); `discrepancy-register.md`.
- **Key facts:** *limited technical independence* — no production import, never calls production to decide expected output, implements only the frozen contract, fails closed; disagreements are triaged, never patched to make production pass.
- **Limit:** it's not external independence; you cannot certify your own checker — needs a non-author code review + `RATIFY-09-04`.

## 8. How P0/P1/P2 and W0/W1/W1-NA isolate application effects
- **Evidence:** C-17 (`packages/evaluation/condition-manifest.json`, `validate_conditions.py`); public app `?condition=`.
- **Key facts:** every condition in a family resolves the **identical DecisionEnvelope per task** (proven by digest equality; a confound is detected) — so an interface effect can't be confounded with a backend difference (C-BLOCK-06). CA-1: `L_reliance` binds to that shared decision, so a system can't score "safer by showing less".
- **Limit:** you build the conditions; Fahmi owns the estimands; `P2−P1` is not cosmetic if conversation changes the interpreted query.

## 9. What result would falsify the candidate contribution
- **Evidence:** `docs/applications/C-BLOCK-05.md` §falsification; the assurance case claims CL-1…CL-14.
- **Key facts:** it narrows or fails if public/staff disagree on retained semantics; restricted staff info leaks; the interface bypasses abstention/order; unsupported model text reaches users; explanations increase *unsafe* reliance; the staff workbench doesn't improve diagnosis vs a comparator; accessibility barriers block tested routes; or the §17 audit shows the integration already exists.
- **Limit:** null/adverse results are reportable — the question is not redesigned after seeing them.

## 10. Which artefacts and review records prove your intellectual ownership
- **Evidence:** the branch commit history (atomic, per-deliverable); each decision doc's dated rationale + rejected alternatives; `docs/assurance/assurance-case.json` (per-claim reviewer/authority slots); the PR (`docs/PULL_REQUEST.md`).
- **Key facts:** every artefact links claim → control → **passing test** → the review still required; contribution is shown by reasoning and tests, never commit-count or hours.
- **Limit — the big one:** these are **AI-assisted scaffolds**; ownership is only real once you've corrected them in your own words, done your K7 primary-source reading, and the non-author reviews are recorded. Say this plainly; it is itself evidence of the discipline the project is about.

---

*Rehearse from the evidence, in your own words. Do not memorise phrasing from this file — an examiner
rewards reasoning you can defend, and the honest "here is the limit" lands better than a polished
over-claim.*
