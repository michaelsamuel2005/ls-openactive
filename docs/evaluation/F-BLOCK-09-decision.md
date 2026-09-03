# F-BLOCK-09 Decision Record

**Decision ID:** F-BLOCK-09 (joint with C-BLOCK-15)
**Status:** DRAFT — authored fields complete; institutional approval pending ratification.
**Authored:** 18 August 2026

> **Authorship notice.** The structure of this record derives from an AI-assisted coordination
> scaffold prepared from the current project artefacts. It is not evidence that Fahmi authored,
> read, accepted or completed the work.
> Decisions, rationale and authored fields in this record are mine.

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

## 2. Rationale

Reliance is a human action taken in response to a rendered decision rather than a
system emission, so it does not belong inside `L_decision`. Introducing `L_reliance`
is an explicit amendment recorded in this decision record instead of silent protocol
drift, preserving the frozen loss vocabulary through documented governance.
`L_reliance` never enters H-P, H-E, H-G or CAL-RISK, and every reliance quantity is
treated as estimative rather than confirmatory.

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

### Operational test

Use digest inequality as the mechanical screen: if the opening-query digest and the
terminal digest differ, the episode is automatically classified as repaired. Only the
digest-equal residual proceeds to blinded human adjudication to determine whether the
interpreted query genuinely changed or whether both queries resolve to the same
terminal DecisionEnvelope. Digest equality is evidence for that decision, not the
definition, because different interpreted queries may legitimately produce the same
terminal envelope.

**Dependency:** the opening-query digest is not yet present in `event-schema.json`;
until that contract is implemented, stage-one screening is not operational. Raised
with Clarence for the C-BLOCK-05 contract workshop.

### Inference boundary

Excluding repaired episodes means the P2 contrast under-tests conversational repair.
This exclusion is a declared inference boundary rather than a hidden confound, and the
repair rate is reported separately with uncertainty. With additional assessor
resources, the preferred design is two estimands: one for unrepaired same-envelope
episodes and one analysing repaired episodes independently.

------------------------------------------------------------------------

## 4. Ethics status

**Decision:** DEFINED BUT UNMEASURED without an approved participant
route.

If no ethics-approved human study exists, the reliance claim is withheld
entirely.

------------------------------------------------------------------------

## 5. Ownership

| Responsibility | Owner |
|---|---|
| Loss definition | Fahmi Alshahabi |
| Estimand | Fahmi Alshahabi |
| Sampling & adjudication | Fahmi Alshahabi |
| Analysis | Fahmi Alshahabi |
| Schema & invariant implementation | Clarence |

### Independence basis

Under the work package independence rule (§2.4), a component owner cannot judge
outputs where ownership defeats blinding. Clarence owns the application
implementation, so the loss definition, estimand and adjudicated scoring remain under
my ownership while implementation remains separate.

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

Reliance loss rate over unrepaired episodes within the declared task universe, at the
stated acquisition vintage, under the frozen design weights. Between-condition
contrasts are estimative and conditional on the shared terminal DecisionEnvelope
referent. No claim extends beyond the episodes adjudicated in this benchmark.

## 5c. Reading disposition

My definition uses the same failure conditions as misuse/disuse, but it does not adopt
the Lee & See (2004) or Parasuraman & Riley (1997) framing as a load-bearing
theoretical construct. Those sources are therefore not load-bearing for F-BLOCK-09.
Recorded as a decision, not an omission.

Date: 18 August 2026

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
-   Exclusion-order gate: fails if any episode's repair status carries an
    adjudication timestamp later than its reliance adjudication timestamp, or if
    repair status is absent for any P2 episode entering the estimand.

------------------------------------------------------------------------

## Fallback

If unresolved or ethics approval is unavailable, **report no reliance
result**.
