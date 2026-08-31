# C-20 — Clarence's independent review of Fahmi's evaluation stream

> **This is Clarence's review to write.** The findings below must be his own, formed from reading the
> artefacts, in his own words. A review that cannot fail is not evidence (WP §17.3) — record *real*
> findings. Clarence must **not** review anything he co-authored (WP §2.3 independence). This template
> is structure only — every "Finding" cell is yours to fill.

**Reviewer:** Clarence Zhen Jin Tan  ·  **Independence check:** confirm you did not author the
artefacts below → ☐ confirmed
**Date of review:** ______

## Artefacts under review (get the latest first)

```
git fetch origin
git show origin/fahmi/proposal-v2-sections-6-7:docs/evaluation/estimand-registry.yaml
git show origin/fahmi/proposal-v2-sections-6-7:docs/evaluation/codebook-v0.3.md
git show origin/fahmi/proposal-v2-sections-6-7:docs/evaluation/eligibility-matrix-feasibility.md
git show origin/fahmi/proposal-v2-sections-6-7:docs/evaluation/source-reading-matrix.md
```
Or on GitHub: `…/tree/fahmi/proposal-v2-sections-6-7/docs/evaluation/`

| Artefact | Version / commit reviewed |
|---|---|
| `estimand-registry.yaml` (the estimands, incl. `L_reliance` referent — CA-1 seam) | ______ |
| `codebook-v0.3.md` (labels / annotation) | ______ |
| `eligibility-matrix-feasibility.md` (assessor eligibility / blinding) | ______ |
| `source-reading-matrix.md` | ______ |

## Method (how you actually reviewed — fill in)

Scope: ______ · Techniques used (checked a task case maps to a real app state / traced `L_reliance`
back to the terminal `DecisionEnvelope` / looked for personal data in telemetry / …): ______

## The §17.2 questions — your finding + severity for each

Severity scale: **blocker / major / minor / nit**. Write what you found, not a yes/no.

1. Do task cases correspond to real application states/actions? — **Finding:** ______  **Severity:** ___
2. Are P0/P1/P2 and W0/W1/W1-NA differences accurately described? — **Finding:** ______  **Severity:** ___
3. Are application failures retained in denominators (not silently dropped)? — **Finding:** ______  **Severity:** ___
4. Do labels measure comprehension / action / usefulness, not preference alone? — **Finding:** ______  **Severity:** ___
5. Can assessors stay blind / eligible given you own the interface? — **Finding:** ______  **Severity:** ___
6. Do telemetry events answer the estimands without unnecessary personal data? — **Finding:** ______  **Severity:** ___
7. Are accessibility modes represented without using disability proxies as identities? — **Finding:** ______  **Severity:** ___
8. Do staff metrics retain denominators / vintages / weighting / uncertainty? — **Finding:** ______  **Severity:** ___

> **Watch the CA-1 seam especially (question 1–2):** confirm `L_reliance` in Fahmi's
> `estimand-registry.yaml` binds to the terminal `DecisionEnvelope` evidence state (identical across
> P0/P1/P2), not to *displayed* evidence — that's the shared blocker (C-BLOCK-15 / F-BLOCK-09) you both
> own. If it still reads against displayed evidence, that's a **blocker** finding.

## Findings register (WP §17.1 schema — one row per real finding)

| review_id | artefact_and_version | scope | finding | severity | evidence_ref | owner_response | disposition | retest_evidence | remaining_limitation |
|---|---|---|---|---|---|---|---|---|---|
| C-20-01 | | | | | | (Fahmi) | | | |

## Summary (your words)

Overall assessment: ______  ·  Blockers raised: ___  ·  What you could **not** assess and why: ______
