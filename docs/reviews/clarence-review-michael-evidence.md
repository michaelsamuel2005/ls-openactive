# C-19 — Clarence's independent review of Michael's evidence stream

> **This is Clarence's review to write.** The findings below must be his own, formed from reading the
> artefacts, in his own words. A review that cannot fail is not evidence (WP §17.3) — record *real*
> findings; "no issue found" is only valid where you genuinely looked and can say how. Clarence must
> **not** review anything he co-authored (WP §2.3 independence). This template is structure only —
> every "Finding" cell is yours to fill.

**Reviewer:** Clarence Zhen Jin Tan  ·  **Independence check:** confirm you did not author the
artefacts below → ☐ confirmed
**Date of review:** ______

## Artefacts under review (get the latest first)

```
git fetch origin
# read a file without switching branch:
git show origin/fahmi/proposal-v2-sections-6-7:docs/proposal-v2/section-6-recommender-architecture.md
git show origin/fahmi/proposal-v2-sections-6-7:docs/proposal-v2/section-8-evidence-contract-chatbot.md
```
Or on GitHub: `…/tree/fahmi/proposal-v2-sections-6-7/docs/proposal-v2/`

| Artefact | Version / commit reviewed |
|---|---|
| `section-6-recommender-architecture.md` (evidence/recommender semantics) | ______ |
| `section-8-evidence-contract-chatbot.md` (claim contract / evidence vocabulary) | ______ |
| Michael's certificate/witness spec (when on a branch) | ______ |

## Method (how you actually reviewed — fill in)

Scope: ______ · Techniques used (read-through / traced a claim to a receipt / checked an enum against
C-BLOCK-05 / tried to construct a confusable state / …): ______

## The §17.1 questions — your finding + severity for each

Severity scale: **blocker / major / minor / nit**. Write what you found, not a yes/no.

1. Is every application-facing state mutually distinguishable and schema-valid? — **Finding:** ______  **Severity:** ___
2. Can every factual claim resolve to a receipt and a compatible release? — **Finding:** ______  **Severity:** ___
3. Do spec-default / schedule-derived grades have accurate user wording? — **Finding:** ______  **Severity:** ___
4. Can unknown / conflict / scope / service-failure be confused? — **Finding:** ______  **Severity:** ___
5. Are high-consequence fields prevented from silent defaulting? — **Finding:** ______  **Severity:** ___
6. Are checker witnesses sufficient but minimal? — **Finding:** ______  **Severity:** ___
7. Do renderers preserve match and bounded-non-match soundness? — **Finding:** ______  **Severity:** ___
8. Are correction and version-mismatch behaviours defined? — **Finding:** ______  **Severity:** ___

## Findings register (WP §17.1 schema — one row per real finding)

| review_id | artefact_and_version | scope | finding | severity | evidence_ref | owner_response | disposition | retest_evidence | remaining_limitation |
|---|---|---|---|---|---|---|---|---|---|
| C-19-01 | | | | | | (Michael) | | | |

## Summary (your words)

Overall assessment: ______  ·  Blockers raised: ___  ·  What you could **not** assess and why: ______
