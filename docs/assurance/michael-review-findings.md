# Michael Samuel — independent review findings (CL-1, CL-3, CL-6, CL-14)

**Reviewer:** Michael Samuel · **Date:** 2026-08-23 · **Commit reviewed:** `9b0807d`
**Outcome:** REVIEWED WITH BLOCKING CONDITIONS — **not approved.**

Supplied tests all pass (contract invariant battery; certificate checker golden + 13 negative + 8
mutation; conversation route). Adversarial review nevertheless exposed release-blocking gaps the
supplied tests do not cover. **These are real defects — the affected claims are not merely awaiting a
signature; they are currently unproven or false until the findings are fixed and re-reviewed.**

Section 09 spec (`09_semantics_verification_risk_control_spec.md`, 2026-08-04) is **proposed, not
ratified**; SHA-256 `48828408b1e93d6284022fec4618e52128363d35951a9d656613941c68d2133e`.
`RATIFY-09-04` (production/reference/checker ownership + independence) and `RATIFY-09-05` (claim
vocabulary + rendering obligations) remain blank — Michael has **not** recorded these.

## Findings

| ID | Finding | Affects | Owner | Status |
|----|---------|---------|-------|--------|
| MS-1 | Unverified claims survive public projection: failed verification status is removed while the claim content remains | CL-3 | Clarence (projection/render) | OPEN |
| MS-2 | Receipt IDs are arbitrary strings; the contract does not prove a receipt exists, supports that specific claim, or belongs to a compatible release | CL-6, CL-3 | Joint (Michael §09 contract + Clarence consumer) | OPEN |
| MS-3 | The checker does not enforce its own JSON Schema — schema-invalid certificates can return `PASS` | CL-6 | Clarence (checker) | OPEN |
| MS-4 | A valid receipt can be moved from one predicate to another and still pass (semantic receipt swap) | CL-6 | Joint (receipt↔predicate binding) | OPEN |
| MS-5 | Candidate identity, witness content and claimed decision are not cryptographically bound to the `DecisionEnvelope` | CL-1, CL-6 | Joint (contract) | OPEN |
| MS-6 | State transitions are not checked | CL-6 | Clarence (checker) | OPEN |
| MS-7 | The checker accepts incompatible decision combinations and caller-asserted checker versions | CL-6 | Clarence (checker) | OPEN |
| MS-8 | `check(..., checks=[])` bypasses every check and returns `PASS` | CL-6 | Clarence (checker) | OPEN |
| MS-9 | Conversation route silently ignores or reverses constraints (e.g. "under £10" ignored; "climbing in Havering" adds unrequested step-free; "not wheelchair accessible" interpreted as requiring step-free) | CL-14 | Clarence (conversation) | OPEN |
| MS-10 | Candidate attributes are rendered directly without requiring corresponding verifier-approved claim tuples | CL-3 | Clarence (render) | OPEN |

## Michael's "before approval" conditions (verbatim intent)
1. Claims must resolve to semantically compatible receipts and a verified release root.
2. Public projection must reject/remove entire failed/unresolvable claim tuples, not merely hide the verification field.
3. The checker must enforce its complete certificate and context schemas at runtime.
4. The checker must bind the exact query, `DecisionEnvelope`, candidate slate, claim/predicate, receipt content, versions and permitted transition.
5. Remove the public `checks=[]` bypass; add adversarial tests for semantic receipt swaps, candidate substitution and invalid decision combinations.
6. Conversation parsing must preserve every confirmed constraint, reject unsupported/negated constraints safely, and compare the complete decision digest — not merely candidate order.
7. Rendering must originate only from verifier-authorised claim tuples.
8. Record named, dated decisions for `RATIFY-09-04` and `RATIFY-09-05`.

## CA-2 position (Michael)
The claim-contract author may also author the production interpreter **only if** the contract is
jointly frozen and independently reviewed; the **reference** interpreter has a different owner; and the
certificate checker remains independently authored and code-reviewed. Michael must not be both sole
rule author and sole validator.

## Triage — what closes each
- **Clarence can fix in-stream now:** MS-8 (remove empty-checks bypass), MS-3 (enforce schema at
  runtime), MS-6 (check state transitions), MS-7 (reject incompatible decisions + caller-asserted
  versions), MS-9 (conversation constraint/negation handling), MS-1 & MS-10 (projection/render reject
  unverified/unauthorised tuples). Each needs a new adversarial test and Michael's re-review
  (independence preserved: Clarence authors, Michael reviews).
- **Joint with Michael (needs §09 contract change + freeze):** MS-2 (receipt semantics: existence +
  supports-this-claim + compatible-release), MS-4 (receipt↔predicate binding), MS-5 (cryptographic
  binding of candidate/witness/decision to the `DecisionEnvelope`).
- **Ratifications (authority):** `RATIFY-09-04`, `RATIFY-09-05` — recorded by the Section 09 owner once
  the above are addressed and the contract is frozen.

## Re-review protocol
Fix → add the adversarial test that would have caught it → return the **exact successor commit** to
Michael for re-review. A claim flips only when Michael's outcome becomes APPROVED and the authority
(ratification) is recorded.
