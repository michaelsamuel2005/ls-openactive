# F-BLOCK-09 Decision Record

**Decision ID:** F-BLOCK-09 (joint with C-BLOCK-15)
**Status:** DRAFT — not committable while any `AUTHOR` field remains unwritten.

> **Authorship notice.** The structure of this record derives from an AI-assisted coordination
> scaffold prepared from the current project artefacts. It is not evidence that Fahmi authored,
> read, accepted or completed the work.
> <<AUTHOR: one sentence naming which parts are yours — at minimum the option rejections in §1, the
> rationale in §2, the operational test and inference boundary in §3, the ethics disposition in §4
> and the independence basis in §5. Delete this bracket once written.>>

## Status

-   **Owner:** Fahmi Alshahabi
-   **Joint reviewer:** Clarence (PENDING)
-   **Date:** PENDING
-   **Decision log:** PENDING

> This is the decision record derived from the structural scaffold.
> Institutional approval fields remain pending until ratification.

------------------------------------------------------------------------

## 1. Decision

### Question

What is the referent of `L_reliance`, where does it sit within the
frozen loss vocabulary, and how are P2 query-repair episodes handled?

### Referent

**Decision:** ACCEPT.

`L_reliance` is judged against the **terminal DecisionEnvelope evidence
state**, identical across P0, P1, P2, W0, W1 and W1-NA by design and
enforced through `INV-NONINTERFERENCE`.

### Chosen option

**(a) Third distinct application-layer loss**

Rejected options:

-   **(b)** Rejected because a human reliance action is not a system
    emission, so it should not be folded into `L_decision`.
-   **(c)** Rejected because treating reliance only as an outcome
    removes any bounded application-layer construct for unsafe reliance.

------------------------------------------------------------------------

## 2. Rationale (AUTHOR IN YOUR OWN WORDS)

> **TODO --- replace this section with your own wording before
> committing.**

Points that must be covered:

1.  Why reliance is a human action rather than a system emission.
2.  Why introducing `L_reliance` is an explicit amendment instead of
    protocol drift.
3.  The statement that `L_reliance` never enters **H-P, H-E, H-G or
    CAL-RISK**.

------------------------------------------------------------------------

## 3. P2 query-repair rule

**Decision:** Repaired episodes are excluded from the reliance
estimand.

Rule:

-   Episodes where conversational repair changes the interpreted query
    resolve a different terminal DecisionEnvelope.
-   Those episodes are excluded from the reliance estimand.
-   Their frequency is reported separately with uncertainty.
-   The exclusion is declared before outcome adjudication and is never
    outcome-dependent.

### Operational test (AUTHOR)

> **TODO:** Define the exact deterministic test (e.g. DecisionEnvelope
> digest inequality).

### Inference boundary (AUTHOR)

> **TODO:** State that this under-tests conversational repair and that a
> two-estimand design would be preferred with additional assessor
> resources.

------------------------------------------------------------------------

## 4. Ethics status

**Decision:** DEFINED BUT UNMEASURED without an approved participant
route.

If no ethics-approved human study exists, the reliance claim is withheld
entirely.

> **TODO:** Confirm this wording or replace it with an approved
> non-participant surrogate.

------------------------------------------------------------------------

## 5. Ownership

| Responsibility | Owner |
|---|---|
| Loss definition | Fahmi Alshahabi |
| Estimand | Fahmi Alshahabi |
| Sampling & adjudication | Fahmi Alshahabi |
| Analysis | Fahmi Alshahabi |
| Schema & invariant implementation | Clarence |

### Independence basis (AUTHOR)

> **TODO:** Cite the §2.4 non-self-judgment clause in your own words.

------------------------------------------------------------------------

## 5b. Permitted and prohibited claims

**Prohibited (candidates compiled from work package §22 and C-17 §5 — accept, strike or extend):**

- No human-effectiveness, usability or actionability claim absent an approved participant route.
- No deployment, adoption or organisational-effectiveness claim.
- No inference about Londoner behaviour, attendance or health outcomes.
- No demographic-fairness claim.
- No confirmatory wording of any kind — `L_reliance` is estimative by construction.
- No claim that a condition is safer on the basis of displaying less; the shared referent exists
  precisely to make that unstatable.

**Permitted:**

> **AUTHOR:** the permitted list is a judgment about what your design actually licenses. Write it.
> It should be narrower than the prohibited list implies, and it should name the universe, the
> conditioning on unrepaired episodes, and the vintage.

## 5c. Reading disposition

> **AUTHOR:** Lee & See 2004 and Parasuraman & Riley 1997 sit against this construct in Clarence's
> reading log, unread on his side. State one of the following and date it:
> (i) your definition relies on the misuse/disuse framing → both become load-bearing, F-20 rows and
> attestations required before this record closes; or
> (ii) your definition does not rely on them → say so explicitly, so the omission is a recorded
> decision rather than a gap.

------------------------------------------------------------------------

## 6. Affected artefacts

-   `docs/evaluation/estimand-registry.yaml`
-   `docs/evaluation/F-BLOCK-09-decision.md`
-   **CA-02** (recommended new amendment)
-   `F-13` application evaluation
-   `C-BLOCK-15`

------------------------------------------------------------------------

## 7. Required tests

-   `INV-NONINTERFERENCE`
-   Paired identical-digest fixture across P0/P1/P2
-   **TODO:** Add the pre-declared exclusion gate that fails if repair
    status is assigned after outcomes are observed.

------------------------------------------------------------------------

## Fallback

If unresolved or ethics approval is unavailable, **report no reliance
result**.
