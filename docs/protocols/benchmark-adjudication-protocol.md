# Benchmark and Adjudication Protocol + Statistical Analysis Plan

**Protocol ID:** P-BENCH-01
**Author:** Fahmi Alshahabi (benchmark · statistics · adjudication · reference interpreter)
**Independent reviewer:** Wesley Ng
**Freeze gate:** Benchmark freeze (must be committed and reviewed before H1)
**Status:** SKELETON — not frozen. Open decisions are listed in §12 and every one of them blocks the freeze.
**Version:** v0.1
**Date:** 2026-07-19

---

## 1. Purpose and standing

This protocol specifies the London Discovery Benchmark, the statistical analysis plan applied to
it, and the human adjudication procedure used to estimate semantic-classification error. It is one
of the three operational protocols required by decision request 4 of the final supervisor proposal.

Standing rules inherited from the team governance document:

- Methodological choices enter the decision log before they enter code. Where this protocol and
  the decision log disagree, the decision log wins.
- No number enters a report or document without a generating script and a row in the metrics
  manifest (D-016).
- A protocol that exists only outside the private repository does not exist.
- Load-bearing work is not self-approved. This protocol is not frozen until Wesley has recorded a
  review against the checklist in §13.

**Dependency warning.** This protocol can be written, reviewed and frozen independently of the
corpus, but it cannot be *executed* until the S0/S1/S1b reconstruction ladder materialises records.
Sections 8 and 9 are therefore specified so that they can be dry-run against synthetic corpora
with planted mechanisms before any real corpus exists. Nothing in this document may be re-tuned
after the corpus arrives.

## 2. Claim boundary

The unit of claim is an observed listing at a named snapshot, not London provision.

- "No observed listed match" never means "no activity exists."
- Answerability is a property of the data, not of Londoners. This benchmark measures data-side
  answerability of prespecified searches (R3). It does not measure observed user behaviour, reach,
  engagement or lived access.
- Deprivation-stratified results describe the catalogue's answerability across origins drawn from
  different deprivation strata. Whether these are reported as descriptive or estimative is
  **OPEN — see §12, item O-4.**
- Capacity, bookability and cancellation status are never inferred from recurrence.

## 3. Query families and required evidence

Six families. A query is *answerable at stage s* when the frozen evidence engine returns at least
one supported match — that is, every required atomic predicate evaluates to T.

| # | Family | Frozen task | Required evidence | Absence semantics |
|---|---|---|---|---|
| F1 | Activity + geography | Named activity within a frozen distance of the origin | Mapped activity term; validated London/distance evidence | Unmapped vocabulary → `U_vocabulary`; unresolvable geography → scope-indeterminate, not non-match |
| F2 | Time / Schedule | Evening or weekend opportunity within the frozen horizon | Explicit occurrence, or a valid full `Schedule` expanded over the horizon | `PartialSchedule` is never expanded → `U_source_absence` |
| F3 | Price visibility | Free, or at or below a frozen price | Structured offer/price | Absent price is unknown, never free. `U_source_absence` |
| F4 | Age information | Includes a stated age | Structured age range | Absent age range is unknown, never universal |
| F5 | Accessibility information | Publishes a requested access feature | Structured accessibility evidence | Absence is a publication finding, not an absence of provision |
| F6 | Compound referral | Time AND price AND accessibility constraints jointly | All component evidence, plus the acquisition-coverage qualifier | Any component unknown propagates to indeterminate for the conjunction |

**Evidence grading.** Occurrences derived by `Schedule` expansion are reported as
*determinate-schedule-derived*, never pooled with *determinate-explicit*. F2 and F6 results are
reported separately by grade. **Rationale:** the S0→S1b contrast is the primary estimand, and
schedule-derived evidence is the dominant mechanism by which S1b gains answerability; pooling the
grades would make the headline effect uninterpretable.

**Barrier grounding.** Each family maps to a documented participation barrier (cost, time, age
eligibility, accessibility information, travel). The literature citations supporting each mapping
are **OPEN — see §12, item O-1.** Families are not justified by data availability.

## 4. Origins and sampling frame

- At least **30** prespecified population-weighted LSOA origins.
- At least **10 per London-specific deprivation tertile**.
- Final origin count is chosen jointly with query and pair-sample size by the sizing simulation
  (§8), not asserted here.

Required registrations, all **OPEN — see §12:**

| Item | Status |
|---|---|
| Deprivation index and vintage (English IoD year; London-specific tertiling method) | OPEN — O-2 |
| Population-weighting source and vintage | OPEN — O-2 |
| LSOA boundary vintage and its consistency with the deprivation vintage | OPEN — O-2 |
| Distance threshold(s) for F1 | OPEN — O-3 |
| Price threshold for F3 | OPEN — O-3 |
| Requested access feature(s) for F5 | OPEN — O-3 |
| Geocoding cascade and dual-route disagreement audit rule | OPEN — O-5 |

Reuse note: point-in-polygon borough assignment and the geographic stratification fields in
`src/export_ws3_inputs.py` are reusable for origin placement. The gap-index and quadrant payload
in that module is **not** used by this protocol.

## 5. Query construction and freezing

- Families × origins yields at least **180 locked queries**.
- **Development queries are permanently excluded from the locked set.** The development pool is
  fixed and recorded before any locked query is generated; membership is checked by an automated
  test, not by inspection.
- Frozen in a single tagged commit: query text, thresholds, required fields, origins, geocoding
  cascade, codebook, random seeds, prior-sight declaration, and the analysis code.
- Seeds follow the existing single-seed rule (`config.RANDOM_SEED`).
- The entire benchmark must regenerate byte-identically from the frozen inputs on a clean
  checkout. This is an acceptance criterion, not an aspiration (§13).

**Candidate universe.** All stable identities in the frozen London-serving corpus form the
auditable candidate universe. There is no ranking and no hidden top-k. Each query answer carries
an independent acquisition-coverage qualifier; coverage failure is never folded into the
record-level evidence state.

## 6. Estimands

For query *q* and stage *s*, define **A(q,s) = 1** when the frozen evidence engine returns at
least one supported match, else 0.

**Primary estimand**

> Δ = mean[ A(q, S1b) − A(q, S0) ]

reported with exact paired transition counts (0→0, 0→1, 1→0, 1→1) and a 95% interval.

The 1→0 cell is reported even if empty; a non-empty 1→0 cell is a finding about reconstruction,
not a nuisance.

**Structural decomposition**

- S0 → S1 : answerability carried by inheritance.
- S1 → S1b : answerability carried by `Schedule` expansion.

These decompose Δ; they are not independent estimands and are not tested separately for
significance.

**Pre-enumerated secondary outcomes** (estimation-led, no hypothesis testing unless declared here):

1. Explicit vs schedule-derived evidence share, by family.
2. Family-level effects.
3. Result depth (count of supported matches per answerable query).
4. Distribution of unresolved mechanisms (`U_m` / `B_m` labels) among indeterminate answers.
5. Consumer-projection effects (S2a, and S2b as stress test only).
6. Deprivation-stratified description of answerability.

**Policy comparison.** Closed-world, permissive and explicit three-state policies are compared on
false-suppression and false-assurance rates against the weighted adjudicated reference labels,
plus a cost-ratio threshold curve. No unmeasured practitioner or resident cost is asserted; the
curve is presented as a sensitivity surface over an unknown cost ratio, not as a recommendation at
a chosen point.

**Equivalence testing** is used only if a workflow-derived margin and adequate precision are frozen
in advance. Absent that, no equivalence claim is made. Currently **not frozen** — see §12, O-6.

**Diagnostic positive and negative controls are excluded from the primary score.**

## 7. Interval estimation and dependence

Queries are clustered by origin and, through the corpus, by publisher/platform. The resampling
method is **selected by simulated coverage** under the declared query-generation design, not chosen
by convention. Candidate methods to be compared in §8: cluster bootstrap over origins, two-way
cluster-robust intervals, and exact paired methods for the marginal transition table.

Selection rule: the method with acceptable simulated coverage (nominal 95%, tolerance band
**OPEN — O-7**) and the narrowest expected width under the declared dependence scenarios. Ties
resolved in favour of the simpler method. The comparison table is committed.

## 8. Development-only sizing simulation

Purpose: jointly choose origin count, final query count, adjudicated pair-sample size,
confidence-width target and interval method, under a frozen assessor-hours cap.

Constraints and rules:

- Uses the **actual paired estimator** defined in §6.
- Uses **dependence scenarios**, never locked effects. No quantity from the locked corpus enters
  this simulation.
- The assessor-hours cap is frozen before the simulation runs. Value **OPEN — O-8.**
- Inputs: plausible marginal answerability rates, plausible transition structures, cluster sizes,
  intra-origin correlation range, and assessor throughput (pairs/hour, from development-example
  training).
- Outputs: a committed grid of (origins, queries, pair-sample size) against expected confidence
  width and required assessor hours, plus the selected operating point and the reason it was
  selected.
- Runs against synthetic corpora with planted mechanisms. This is the dry run that de-risks the
  whole plan before the corpus exists.

## 9. Adjudication

**Sample.** A probability sample of query–record pairs, over-representing stage/policy
disagreements while retaining **non-zero inclusion probability for agreements**. Inclusion
probabilities are recorded per pair and carried into analysis weights. Weighted reference labels
estimate semantic-classification error and support the policy comparison; they do **not** silently
redefine the unsampled engine outputs.

**Roles.**

| Role | Member | Note |
|---|---|---|
| Masked assessor | Clarence Zhen Jin Tan | Trained on development examples only |
| Masked assessor | Wesley Ng | Trained on development examples only |
| Arbitrator and analyst | Fahmi Alshahabi | Concentration declared in limitations (§11) |
| Excluded | Michael Chellam Sebastian | Owns the evidence engine; may not resolve locked semantic labels |

**Masking.** Assessors reconstruct predicate evidence from source lineage using the frozen
codebook. Stage and policy are masked. The arbitrator resolves disagreements **without examining
headline effects**; arbitration is completed and committed before any Δ is computed.

**Agreement reporting.** Raw agreement, class-specific agreement, and a chance-adjusted statistic
are all reported. Chance-adjusted agreement alone is not reported, because base rates across the
four evidence states are expected to be highly skewed and a single kappa would be misleading.
A third-party audit of **10%** of agreements is performed by the arbitrator.

**Codebook.** Frozen before assessor training. Written so that a competent stranger with the
lineage view can apply it without asking the author a question — this is the operative mitigation
for the role concentration, and it is tested by having Wesley apply the draft codebook cold to a
development sample before it is frozen.

## 10. Sensitivity, robustness and later vintages

1. **Leave-one-publisher-out** and **leave-one-platform-out** re-estimation of Δ.
2. **Later-vintage persistence** at H2 and H3. Per the frozen team rule, if H3 cannot be acquired
   with sufficient evaluation time, it remains a clearly labelled sensitivity analysis and is not
   required for the primary conclusion.
3. **Schedule-horizon sensitivity.** Δ is re-estimated across a declared range of horizons.
   *This is load-bearing:* a longer horizon mechanically raises F2 and F6 answerability at S1b and
   therefore inflates Δ for structural rather than informational reasons. The horizon is proposed
   by Michael, evaluated here, and frozen by the full team before H1. The sensitivity range must be
   frozen at the same time as the horizon itself.
4. **Conditional H2/H3 schedule-override audit.** Compare H1 schedule-derived occurrences with
   later explicit overrides. Report checkable-case denominators, censoring, and matching-rule
   sensitivity. Explicit occurrences are selectively materialised, so this is **never** reported as
   a general reliability rate for schedule-derived evidence.
5. **Consumer-projection sensitivity** via S2a (bounded real-consumer case) and S2b (synthetic
   lossy projection, stress test only, never a headline).

## 11. Results-blind drafting and declared limitations

Before unblinding, three results-section shells are pre-drafted with placeholder values from
synthetic corpora:

- **Positive reading** — reconstruction materially raises answerability.
- **Null reading** — reconstruction does not materially change answerability.
- **Indeterminacy-dominated reading** — most queries resolve to indeterminate under all stages,
  and the informative result is the mechanism distribution rather than Δ.

All three are committed before the locked evaluation runs. The third is not a failure case.

**Declared limitations of this protocol, to appear in the report:**

- The arbitrator is also the analyst and the author of both this protocol and the reference
  interpreter. Mitigation is the cold-application codebook test (§9) and Wesley's independent check
  of inter-assessor agreement, not the declaration itself.
- Answerability is a catalogue property. No claim about Londoners' actual discovery experience
  follows from it.
- Adjudication is a sample; unsampled engine outputs retain their engine labels.

## 12. Open decisions — every item blocks the freeze

| ID | Decision | Owner | Needed by |
|---|---|---|---|
| O-1 | Literature grounding for each barrier→family mapping | Fahmi | Protocol freeze |
| O-2 | Deprivation index + vintage, population-weighting source, LSOA boundary vintage | Fahmi proposes, team approves | Before origin generation |
| O-3 | Distance, price and access-feature thresholds | Fahmi proposes, team approves | Before query generation |
| O-4 | Deprivation comparisons: descriptive or estimative | Team | Analysis plan freeze |
| O-5 | Geocoding cascade + dual-route disagreement audit rule | Wesley proposes, Fahmi evaluates | Before origin generation |
| O-6 | Whether any equivalence margin is workflow-derivable | Fahmi + Clarence | Analysis plan freeze |
| O-7 | Simulated-coverage tolerance band for interval-method selection | Fahmi | Before sizing simulation |
| O-8 | Assessor-hours cap | Team | Before sizing simulation |
| O-9 | Schedule-expansion horizon and its sensitivity range | Michael proposes, Fahmi evaluates, team freezes | Before H1 |
| O-10 | Confirmed submission date (18 Sep vs handbook's 4 Sep) — determines the latest possible locked-evaluation date | Clarence (supervisor confirmation) | Immediately |

O-10 is upstream of the entire schedule in this protocol. Dates elsewhere in this document are
provisional pending it.

## 13. Acceptance checklist — Wesley checks

This protocol is not frozen until every box is recorded as checked in the pull request.

- [ ] Benchmark regenerates from frozen inputs; seeds and origins reproduce byte-identically on a
      clean checkout.
- [ ] Development queries are provably excluded from the locked set by an automated test.
- [ ] Sampling inclusion probabilities and analysis weights are correct and recorded per pair.
- [ ] Headline tables regenerate cleanly from a clean checkout.
- [ ] Every number in the protocol and its outputs has a generating script and a metrics-manifest
      row (D-016).
- [ ] No quantity derived from the locked corpus appears anywhere in the sizing simulation.
- [ ] The three results shells were committed before the locked evaluation ran (checked by commit
      timestamp, not by assertion).

## 14. Change control

After the benchmark freeze, no change to this protocol is permitted without a recorded deviation
in the decision log, a stated reason, and a full audit rerun. Deviations are reported in the final
report regardless of whether they changed a conclusion.

---

**Review record**

| Date | Reviewer | Outcome |
|---|---|---|
| | Wesley Ng | pending |
