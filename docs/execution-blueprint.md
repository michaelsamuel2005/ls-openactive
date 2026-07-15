> **REPO STATUS (2026-07-15).** This file is the **(2)** revision, installed verbatim.
> It **supersedes the (1) copy** previously committed here, and supersedes the five local
> fixes applied to that copy — **(2) already carries all five, and carries them better**
> (see D-027). Two of (2)'s corrections land against this repository's own claims and are
> accepted: **Check 5** rules that the `bytes/item × 7.9M` extrapolation is *"a pilot
> estimate, not a capacity decision"* — retiring D-021's "capacity is not a constraint";
> and **§16** rules *"stop treating missing fields as publisher faults until parent lineage
> is checked"* — which D-025 did, and which D-026 corrects.
> **Only measured status annotations have been added below.** Nothing in (2)'s text is altered.

# Execution blueprint: maximally aligned, academically exceptional London Sport 1 project

> **Evidence update — 15 July 2026:** the 7 July CSV has now been inspected directly. Its lineage/current-state gate has failed. A fresh, raw-retaining catalogue harvest is Deliverable 1, not an optional feasibility exercise. All existing ecosystem-level diagnostics are suspended pending that harvest.

## 1. The decision

Adopt the **determinable discovery coverage** pivot and freeze it only after the five
corpus, lineage, current-state, mechanism-eligibility and capacity checks below.

Recommended title:

> **Determinable Discovery in London's OpenActive Ecosystem: Separating source publication, standards-aware reconstruction and consumer-processing effects**

This title is deliberately outcome-neutral. The pilot proves that information can be
lost during consumer extraction, but it does not establish that all remaining
indeterminacy is instrument-side or that publication-side limitations are absent.

Use this claim about alignment:

> The project is maximally and transparently aligned to the supplied London Sport overview through a documented task-derivation process. No claim is made that the selected task was separately validated or prioritised by the partner.

Do not claim “100% partner alignment.” Without further partner elicitation, that is unknowable. What the team can make complete is **brief traceability**: every brief clause must control a research choice, deliverable and evaluation.

## 2. Freeze the scientific core

### Research problem

OpenActive enables digital discovery, but record volume and field presence do not show whether a catalogue can determine that a listed opportunity satisfies a searcher's constraints. Feed acquisition, parent-child inheritance, current-state processing, publication horizons, semantic ambiguity and missing values can make search results indeterminate or misleading.

### Aim

> To determine which constraint-based searches are supported determinately by a reconciled London OpenActive corpus, attribute indeterminate results to source publication, standards-aware reconstruction or consumer processing, and quantify which validated changes most improve query-level discovery coverage.

### Research questions

1. **Corpus validity:** Which feeds, entity types, parent-child structures and semantic fields are actually represented, and what acquisition or extraction losses constrain discovery?
2. **Discovery determinability:** Across a prespecified benchmark of London searches, what proportion return enough determinate matches, only indeterminate candidates, or no observed listed match?
3. **Mechanism and repair:** How much do standards-aware reconstruction and consumer projection change determinable discovery coverage, for which search constraints, and at what coverage/error cost?

Do not add a fourth independent research programme. The prototype is an experimental surface for RQ3, not another RQ.

### Falsifiable central proposition

> Source state, standards-aware reconstruction and consumer projection do not preserve the same determinability for prespecified London discovery queries.

This can be falsified. If the three stages produce no material difference, report that
bounded null result and withdraw the information-loss claim. If a difference exists,
attribute it to the stage where the same-vintage paired comparison changes, rather than
assigning blame from field presence alone.

## 3. Formalise the construct without overclaiming

For query `q`, let `C(q)` be its hard constraints. For record `o`, evaluate each constraint as:

`T` = explicitly supported; `F` = explicitly contradicted; `U` = not determinable from the reconciled record.

Classify each record:

- **Determinate match:** every hard constraint is `T`.
- **Indeterminate candidate:** no constraint is `F`, and at least one is `U`.
- **Known non-match:** at least one hard constraint is `F`.

For a frozen query set `Q` and predeclared minimum useful count `k`:

`DDC@k(Q) = mean[ number of determinate matches for q >= k ]`.

Because this scalar is controlled by the composition of `Q`, the **primary result must be the prespecified stratum profile and a curve over constraint count**. Report the scalar only beside the complete query-composition manifest and sensitivity to `k`; never present it as an intrinsic property of London or OpenActive.

Companion outcomes:

- indeterminate-query rate;
- no-observed-listed-match rate;
- determinate and indeterminate result counts;
- uncertainty attribution by field/mechanism;
- distance to nearest determinate match;
- change in DDC after each validated repair;
- false-suppression and false-assurance rates against an adjudicated sample.

Never translate “no observed listed match” into “no activity exists.” Never translate DDC into participation, physical-activity provision or health outcome.

The database literature establishes query completeness and certain/possible answers over incomplete databases; do not claim invention of those concepts. The contribution is the domain-specific operationalisation, empirical mechanism analysis and reusable OpenActive benchmark. Candidate anchor: [Razniewski and Nutt, *Completeness of Queries over Incomplete Databases*](https://www.vldb.org/pvldb/vol4/p749-razniewski.pdf). **Reference status: primary source verified 15 July 2026** (title, authors, PVLDB volume 4 number 11, 2011, and relevance to query completeness/certain and possible answers). Final reference formatting and fit within the critical literature argument still require team review.

If the team wants to use the formal labels **certain** and **possible**, it must specify a possible-world model and permissible value domains. Otherwise retain the operational labels above.

## 4. Make every brief clause load-bearing

| Supplied overview clause | Research response | Deliverable | Acceptance evidence |
|---|---|---|---|
| Review OpenActive and approaches from elsewhere | Current incumbent/standards review plus systematic prior-art search | Dated capability and novelty matrix | Search protocol, inclusion rules, primary-source citations, surviving contribution |
| Analyse OpenActive data | Reconciled corpus and query-level determinability analysis | Versioned corpus ledger, metric outputs and uncertainty analysis | Full provenance, tests, non-author reproduction |
| Innovate using data/digital approaches | Three-state uncertainty-aware retrieval and repair-value evaluation | Reusable benchmark and thin prototype | Beats or meaningfully qualifies both closed-world and permissive baselines, or yields an informative null |
| Help audiences find activities | Test whether constrained searches receive determinable listed matches | Query benchmark and error analysis | Prespecified task outcomes; no behavioural overclaim |
| Embed digital pathways | Model a referral/finder-style discovery step | Workflow diagram and demonstrator | Clearly compatible with existing Get Active/Haringey-style flow; no claim of deployed integration |
| Tailor to London's diverse communities | Barrier-informed constraint combinations and spatially distributed search origins | Constraint-provenance table and stratified results | Every constraint sourced; scenarios described as searches, not representative personas |
| Develop new models, prototypes **or** recommendations | Formal DDC construct, optional thin interface and quantified repair recommendations | Model/benchmark, interface, evidence-ranked recommendations | Each recommendation has measured effect, uncertainty and implementation boundary |
| Increase physical activity | State a bounded theory of change from better discovery information | Logic model | Clearly labelled as potential pathway, not measured impact |

OpenActive's own quality guidance says data users report end-user search issues and that current quality work initially focuses on “what”, “where” and “when” for discovery and booking. This supports the problem while also proving that generic field-quality analysis is not novel. [OpenActive data-quality guidance](https://developer.openactive.io/publishing-data/data-quality)

The Haringey referral workflow is relevant as a public use context because healthcare professionals send patients links to local activity sessions found through OpenActive-compliant sources. It is not evidence that London Sport commissioned this exact evaluation. [London Sport Haringey pathway](https://londonsport.org/focus-area/london-sport-and-haringey-nhs-pioneer-open-data-digital-patient-referrals/)

## 5. Deliver the new corpus, then pass its five gates

The legacy corpus cannot pass these gates. Its columns are:

`id, name, startDate, duration, dayOfWeek, remainingCapacity, maximumCapacity, amenities, adultPrice, adultAgeRestriction, juniorPrice, juniorAgeRestriction, venue, latitude, longitude`.

It has 549,169 data rows. It contains no source `@id`, `superEvent`, organiser, activity vocabulary, feed/publisher identity, RPDE `modified`/`state` or retained raw JSON-LD. The projected `id` column exists, but its stability and source semantics cannot be established from the CSV. The 7 July file is therefore historical/motivating evidence only.

Deliverable 1 is a **fresh observation vintage** harvested from the canonical production catalogue, retaining raw responses, feed and request status, RPDE identity/state and the parent feeds required by observed references. It cannot retrospectively repair the 7 July state.

### Check 1 — corpus scope

Produce a table for every catalogue/dataset/feed declared by the canonical production collection:

`catalogue → dataset → publisher → feed → entity type → request status → record count → time coverage → parent feed → inclusion/exclusion`.

Pass only when `attempted ÷ declared` is reported at catalogue, dataset-site and feed level; 100% of selected endpoints have a recorded status; the selection rule is explicit; and failed/unattempted endpoints remain visible. “100% of three feeds attempted” is not full-ecosystem coverage.

### Check 2 — field lineage

> **STATUS: PASSED-PENDING-REPRODUCTION (D-025).** `src/trace_lineage.py` →
> `results/lineage_trace.csv`, `results/lineage_sample.csv`. Extraction loss **is** separated
> from source absence: over 14,790 resolved children, `location` is 100.0% *inheritable* and
> `level` is 100.0% *source-absent*. **Two caveats bind:** the counts were computed on a raw
> archive **44 pages short** (filename-collision defect, D-026 item 4), and the gate's second
> condition — *"a second team member can reproduce every sampled trace"* — **is not ours to
> close**. `results/lineage_sample.csv` emits 50 hand-checkable traces; a teammate must
> actually check them. **Not passed until both are done.**

For a stratified sample, trace activity, name, organiser, location, time, price, age and accessibility from raw JSON-LD through parent inheritance to analytical record.

Pass only on the new raw-retaining corpus, when extraction loss is separated from source absence and a second team member can reproduce every sampled trace.

### Check 3 — current-state pipeline

Demonstrate updates, deletions, feed-pair joins, partial read/error handling, recurrence/schedule semantics, London geography and common observation horizon.

Pass only when counts reconcile from harvest to final entity and failure/partial states cannot silently become “zero opportunities.” Publication-window sensitivity is part of the primary result because date-constrained discovery counts are defined by the chosen observation and future windows.

If any check fails, the first contribution becomes pipeline/corpus reconstruction and all ecosystem-wide claims are suspended.

### Check 4 — mechanism eligibility and prevalence

> **STATUS: PARTIAL — prevalence measured, ELIGIBILITY NOT.** Per-kind (the only honest
> denominator): `superEvent` on `ScheduledSession` **18,935/18,935 = 100.0%**; on `Slot`
> **0/92,359 = 0.0%** ⇒ **the primary mechanism is scoped to session feeds only**.
> **This check's own warning applies to us and is conceded:** *"Do not use the exploratory
> one-page pilot to claim ecosystem prevalence."* Our census read **pages 0–1 of each feed —
> the oldest end of a `modified`-ordered change feed** — so `173/173 = 100.0%` is coverage of
> **sites, never of records**. **Not yet done:** independent-cluster counts, the
> required-paired-record calculation, and the London paired-record count after geography/time
> rules. Note **31.5% of `ScheduledSession` items are `deleted` tombstones** (8,372 of
> 26,585), so current-state reconstruction materially changes any prevalence figure.

The pilot must report, by entity type and independent dataset/publisher cluster:

- the proportion of current children carrying a relevant parent reference;
- the proportion of those references resolved from the selected current-state corpus;
- the number of independent clusters contributing paired records;
- the number of paired London records after the final geography/time rules;
- field-level change from source child to reconstructed entity and from reconstructed
  entity to consumer projection.

Do not use the exploratory one-page pilot to claim ecosystem prevalence. Before the
confirmatory freeze, calculate the required paired-record count using the pilot's
cluster structure and the target interval precision, and record that calculation. The
primary mechanism is eligible only if there are enough paired London records and
independent clusters to estimate its effect without one publisher dominating it.

If the eligibility gate fails, do not manufacture a trivial null. Use the ranked
fallback: (1) consumer-projection loss on all reconstructable records; (2) unresolved
parent/reference failure as the primary mechanism; (3) a bounded corpus/pipeline study
with no London-wide query-effect claim. The observed prevalence remains a result.

### Check 5 — capacity and resumability

> **STATUS: MEASUREMENT ONLY — NOT a capacity decision, per this check's own rule.**
> Measured: **~1,329 raw bytes/item** over 217,743 items (`results/census_summary.csv`);
> ~25 min wall-clock for 969 endpoints at 1 req/sec. The `× 7.9M ≈ 10.5 GB` extrapolation is
> **a pilot estimate and is hereby demoted from D-021's claim that "capacity is not a
> constraint"** — it excludes database, index, log, duplicate-response, temporary and backup
> costs, exactly as this check states. **Not done:** 3× working-space verification, backup
> destination and owner, resume/restart procedure and recovery test, scope-reduction rule.

The pilot must measure raw feed-page bytes per observed RPDE item, items per page,
request time, retry behaviour, SQLite growth and temporary-file growth. Before a full
run, record:

- selected feeds and estimated item/page counts;
- estimated raw, database and temporary storage;
- at least three times the estimated local working space available;
- a separate backup destination and owner;
- expected wall-clock range under the declared request rate;
- the resume/restart procedure and a small recovery test;
- the scope-reduction rule if storage or time is insufficient.

The earlier approximate `bytes/item × 7.9m` calculation is a pilot estimate, not a
capacity decision. It excludes some database, index, log, duplicate-response,
temporary and backup costs. “An external drive” is not a plan until space, ownership,
backup and recovery have been verified.

## 6. Build one exceptional mechanism study

### Primary mechanism

Use three deterministic stages from the **same new observation vintage**:

- **S0 — source/current-state stage:** the current entity as published, before parent
  inheritance;
- **S1 — standards-aware stage:** recursively parent-resolved current entities with
  property provenance and unresolved references retained;
- **S2 — consumer-projection stage:** the deliberately specified flattened consumer
  view used by the discovery experiment.

Compare S1−S0 to measure the information made available by standards-aware
reconstruction and S2−S1 to measure information lost by the consumer projection.
Remaining indeterminacy at S1 is a source/corpus limitation only after unresolved feed
coverage and parent references have been accounted for. The legacy CSV cannot form one
arm of this comparison because it is a different vintage with irrecoverable provenance.

Predeclare:

- raw-retaining harvest identity and the three deterministic stages being compared;
- affected fields and expected direction;
- primary prespecified stratum profiles and constraint-count curves, with DDC as a
  secondary summary;
- `k`, radius, observation date and a primary future window plus a prespecified window-sensitivity grid;
- practically meaningful effect rule;
- clustering/uncertainty method;
- kill rule.

Do not choose the materiality threshold after seeing the result. If no partner threshold exists, justify it through task consequences and show the full sensitivity curve instead of hiding behind one cutoff.

### Predeclared outcome branches

The same experiment supports four honest outcomes:

1. **Source-limited:** S1 remains substantially indeterminate after complete,
   standards-aware reconstruction.
2. **Reconstruction-limited:** S1 materially improves on S0 because required fields
   are available through linked records.
3. **Projection-limited:** S2 materially degrades S1 because consumer flattening or
   filtering discards usable information.
4. **Mixed:** the dominant stage differs by constraint, entity type, publisher or
   technical system.

The report title, abstract and recommendations must follow the observed branch. The
instrument-side result is plausible and already motivated, but it is not pre-declared
as the answer.

### Secondary mechanisms

Only retain mechanisms that survive validation:

1. validated semantic deduplication;
2. controlled-vocabulary resolution after inheritance;
3. provider/publisher composition decomposition.

Publication horizon is not merely secondary: it is a constitutive sensitivity dimension of every date-constrained DDC result and must be reported with the primary profile.

Use paired query results and feed/publisher-clustered uncertainty. Do not treat millions of recurring rows as independent observations. If mechanisms interact, report a small factorial ablation or order-sensitivity analysis rather than an arbitrary additive “correction waterfall.”

## 7. Create a benchmark, not invented personas

Create a versioned YAML/CSV query specification. Every query component must have provenance:

- location sampling rule;
- activity category and controlled-vocabulary URI;
- date/time rule;
- travel radius;
- budget threshold;
- age constraint;
- requirement for accessibility information.

Derive the dimensions from the supplied overview, public London Sport workflows, OpenActive use-case/data requirements and peer-reviewed/public-health evidence. OpenActive's own framework recommends analysing what data exists versus what is needed for a defined objective and prioritising the gaps. [OpenActive data-requirements framework](https://usecaseframework.openactive.io/appendix-four-data-requirements-framework/data-requirements-framework)

Use **search scenarios**, not named demographic personas. Say “queries with a junior and low-budget constraint,” not “a representative low-income parent.”

Recommended design:

- a computational benchmark large enough to cover every prespecified combination and London location stratum;
- a smaller stratified adjudication set for semantic correctness;
- a frozen benchmark commit before the confirmatory run;
- explicit prior-sight disclosure because the team has already examined the data.

Avoid calling this “preregistration” if the hypotheses or data have already been seen. Call it a **time-stamped confirmatory freeze with prior-sight disclosure**.

## 8. Compare against fair baselines

Use at least:

1. **Closed-world filter:** unknown treated as non-match. This risks false suppression.
2. **Permissive filter:** unknown permitted without explicit warning. This risks false assurance.
3. **Proposed three-state presentation:** determinate match and indeterminate candidate separated with reasons.

The prototype should not be judged on polish. It should expose the scientific difference between these policies.

Primary prototype evaluation:

- hard-constraint judgement accuracy;
- false assurance;
- false suppression;
- task success at `k`;
- result coverage;
- latency and failure behaviour;
- explanation correctness.

If human participants are not covered by an approved ethics route, use deterministic test cases and non-author expert adjudication. Do not force a user study merely to appear exceptional.

## 9. Validate every semantic rule

Create an annotation guide and stratified gold standard for:

- parent/child field inheritance;
- activity mapping;
- price interpretation;
- age suitability;
- accessibility-information support;
- duplicate identity;
- online/location handling.

Use two independent annotators, adjudicate disagreement and report raw agreement plus an appropriate chance-corrected measure. Do not use Cohen's kappa mechanically when class imbalance makes it misleading.

No transformation enters the primary pipeline unless it meets a predeclared precision/recall or error bound. Failed repairs remain documented negative results.

Distinguish:

- **validated repair:** information correctly recovered or standardised from existing evidence;
- **presentation policy:** unknown shown or filtered differently;
- **oracle simulation:** hypothetical source information supplied for an upper bound;
- **imputation:** modelled value with uncertainty.

Never report an oracle simulation or imputation as actual repaired catalogue truth.

## 10. Engineer for reproducibility

The online repository should contain:

```text
README.md
LICENSE
environment lockfile
data/README.md
config/feed_manifest.yaml
config/metric_manifest.yaml
config/query_benchmark.yaml
schemas/
src/harvest/
src/reconstruct/
src/query/
src/evaluate/
tests/unit/
tests/integration/
tests/fixtures/
analysis/
app/                  # only the thin experiment surface
docs/brief_traceability.md
docs/decision_log.md
docs/claim_ledger.md
docs/prior_art.md
docs/model_card.md
results/manifest.json
```

Required controls:

- immutable hashes for external inputs and result tables;
- pinned environment and one-command pipeline;
- schema validation and contract tests;
- fixture tests for true/false/unknown logic;
- property tests for monotonicity, such as adding a hard constraint cannot increase determinate matches;
- failure-injection tests for feed errors and missing parents;
- no silent partial success;
- deterministic seeds where randomness exists;
- machine-readable result manifest linking claim to script/input/output;
- clean-environment reproduction by a non-author team member.

## 11. Make the academic contribution explicit

The contribution is not “we made an app.” It is the combination of:

1. a reconciled, auditable OpenActive discovery corpus;
2. a formally bounded query-determinability construct;
3. a versioned, provenance-backed London query benchmark;
4. a paired ablation account of which source, reconstruction and consumer-processing stages change discovery outcomes;
5. a fair comparison of closed, permissive and uncertainty-aware retrieval;
6. quantified repair value and failure boundaries;
7. reusable fixtures, annotation rules and tests;
8. a useful positive, mixed or null result.

Novelty wording:

> Existing research formalises completeness and querying under incomplete information, while OpenActive tools assess feed- and field-level quality for discovery. This project operationalises task-conditioned determinability for physical-activity opportunity searches and empirically tests how publication and extraction processes alter determinate, indeterminate and unsupported catalogue results across London search scenarios.

Support that statement with a documented prior-art search. “We could not find…” is acceptable when the search protocol is shown; “nobody has done…” is not.

## 12. Map execution to SEMTM0044

The supplied unit document has learning outcomes, not mark bands. Build the evidence case directly:

| Learning outcome | Required project evidence |
|---|---|
| LO1 team/stakeholder/software practice | Shared issues, decisions, branches/PRs, tests, versioned releases and honest documentation of the partner-access constraint |
| LO2 communication | Brief traceability, concise architecture, meeting/action records, clear presentation of unknowns and limitations |
| LO3 subtasks/modelling | Harvesting, reconstruction, formal query logic, ablation, uncertainty and evaluation integrated around one proposition |
| LO4 workable proof of concept | One-command corpus-to-result pipeline plus thin three-state discovery demonstrator addressing the supplied overview |
| LO5 design decisions/testing/monitoring | Decision records, rejected alternatives, baselines, test suite, failure monitoring, kill rules and reproducibility record |

No one can guarantee an “exceptional” band until the actual rubric is obtained. The defensible aim is to produce unusually strong evidence against every published learning outcome.

## 13. Your personal remit

Assuming the v6.1 allocation still makes you the analysis/visualisation lead, own the project's **evidence spine**, not a generic dashboard.

Complete personally:

1. `brief_traceability.md` with every supplied-overview clause mapped to method, output, evaluation and limitation.
2. A one-page v7 architecture containing the title, aim, three RQs, central proposition and kill rules.
3. `metric_manifest.yaml` defining DDC, denominators, `k`, windows, radii, units, missing-value semantics and sensitivity grid.
4. `query_benchmark.yaml` plus a provenance table for every scenario dimension.
5. Baseline and proposed-policy analysis: closed-world, permissive and three-state.
6. Paired raw-versus-reconstructed result analysis with feed/publisher-clustered uncertainty.
7. A single visual chain: source/feed → reconstructed entity → consumer projection → constraint states → prespecified stratum profiles/constraint-count curves → secondary DDC summary → practical consequence.
8. `claim_ledger.md`: every planned claim marked proposed, exploratory, confirmatory, supported, falsified or withdrawn.
9. `decision_log.md`: answerability pivot, rejected alternatives, lack of partner elicitation, threshold rationale and all kill decisions.
10. Cross-review of the data pipeline and a clean-environment reproduction of someone else's component.

Do **not** spend your time building a large borough dashboard. Build only the visual interface necessary to test and communicate the three-state discovery policy.

## 14. Non-negotiable gates

| Gate | Pass condition | Failure action |
|---|---|---|
| Alignment | Complete brief traceability; task derivation; no false partner claim | Rewrite scope/claims |
| Corpus scope | Attempted ÷ declared reported at catalogue, dataset and feed levels; every selected endpoint has a status; failures and unattempted endpoints remain visible | Restrict claims to the fully described selected corpus |
| Lineage/current state | Same-vintage identity, updates, tombstones, recursive relationships and field provenance reconcile | Restrict to pipeline/corpus study |
| Mechanism eligibility | Paired-record and independent-cluster requirement calculated before final outcomes; prevalence and dominance reported | Use ranked fallback; do not report a null by construction |
| Capacity/recovery | Measured estimate, ≥3× local headroom, separate backup, wall-clock range and tested resume/restart path | Reduce scope before launch |
| Construct | Constraint semantics and DDC pass fixtures and adjudication | Redefine or remove affected constraints |
| Primary effect | Predeclared parent-resolution contrast executed with uncertainty | Report null; remove improvement claim |
| Benchmark | Frozen, provenance-backed, no data-driven cherry-picking | Label exploratory only |
| Prototype | Fair baselines; bounded error/coverage/latency trade-off | Demote to demonstrator |
| Reproducibility | Non-author clean run reproduces headline table/figure | No exceptional claim |
| Integrity | Accurate AI/data/prior-sight/ethics disclosure under current rules | Stop submission claim until corrected |

## 15. Immediate sequence

### Next 24 hours

- Ratify the v7 title, aim, three RQs and central proposition with the team.
- Record that no further partner elicitation is available.
- Record the legacy-corpus gate failure and suspend every diagnostic derived from it.
- Finish the brief-traceability matrix.
- Freeze the rejected alternatives and novelty wording.
- Assign named owners and reviewers for each gate.
- Record the four outcome branches and the ranked fallback before final analysis.

### Next 48–72 hours

- Run a bounded catalogue/harvest pilot and inspect failure/status evidence.
- Produce the machine-readable prevalence/capacity audit; do not promote one-page
  observations to population rates.
- Launch the complete selected raw-retaining observation only after the pilot passes.
- Report attempted-versus-declared catalogue, dataset and feed coverage.
- Complete scope, lineage and current-state gates on the new observation.
- Write the metric manifest and query-specification schema.
- Decide whether parent resolution produces a valid corpus; do not start the final benchmark before this.

### Days 4–7

- Build fixtures and adjudication material.
- Run an exploratory end-to-end pilot on a small frozen slice.
- Fix rules, then time-stamp the confirmatory benchmark and analysis plan with prior-sight disclosure.

### Days 8–14

- Run the primary ablation and secondary analyses.
- Apply kill rules.
- Build the thin three-state demonstrator.
- Complete cross-role reproduction.
- Freeze claims only after the evidence manifest reconciles.

## 16. Stop doing these things

- Stop revising the central question after the five feasibility checks pass.
- Stop calling record counts provision, access or availability.
- Stop building deprivation indices, fairness rerankers and generic publisher dashboards.
- Stop treating missing fields as publisher faults until parent lineage is checked.
- Stop treating unknown as false without measuring false suppression.
- Stop claiming “certain/possible answers” without formal semantics.
- Stop presenting literature-derived scenarios as representative people.
- Stop using dynamic platform figures without timestamped evidence.
- Stop calling late analysis freezing preregistration.
- Stop equating technical search performance with activity participation.
- Stop using AI-generated review text as external validation.

The exceptional route is disciplined subtraction: one important discovery uncertainty, one verified corpus, one primary mechanism, fair baselines, explicit failure conditions and a result that remains useful even when the hypothesis fails.
