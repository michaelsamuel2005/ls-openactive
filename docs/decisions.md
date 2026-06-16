# Project Decision Log

**Project:** Closing the Activity Gap — London Sport × OpenActive
**Unit:** `SEMTM0044` — MSc Data Science Group Project, University of Bristol
**Maintained by:** Michael, Clarence, Wesley, Fahmi

---

## Purpose

This is a living record of the significant decisions taken on the project and the reasoning behind each one. We keep it for three reasons:

1. It makes our design choices **auditable and reversible** — anyone (including a marker) can see not just *what* we did but *why*.
2. It directly supports the unit's requirement to **document and justify design decisions** (Learning Outcome 5).
3. It gives each of us **source material for the individual reflective account**.

## How to use this log

- Add a new entry for any significant decision: direction, scope, method, tooling, or data.
- **One decision per entry.** Do not rewrite the rationale of a past decision after the fact. If we change our minds, add a *new* entry that supersedes the old one, and set the old entry's status to **Superseded**.
- Add entries through the normal **branch → pull request → review** workflow, so every change is reviewed by a teammate.
- **Statuses:** *Proposed* (awaiting supervisor sign-off) · *Adopted* (in effect) · *Superseded* (replaced by a later entry) · *Revisit* (conditionally adopted, to be re-checked against a stated trigger).

---

## Summary

| ID | Decision | Status | Date |
|----|----------|--------|------|
| D1 | Equity-led visual-analytics direction | Proposed | 2026-06-16 |
| D2 | Small-area (LSOA/MSOA) spatial granularity | Proposed | 2026-06-16 |
| D3 | Disciplined method set — two projections + one validated clustering | Proposed | 2026-06-16 |
| D4 | Bayesian imputation for missing fields | Proposed | 2026-06-16 |
| D5 | Honest evaluation — no accuracy claims without behavioural data | Adopted | 2026-06-16 |
| D6 | Data sources and access strategy | Proposed | 2026-06-16 |
| D7 | Audit-first sequencing | Adopted | 2026-06-16 |
| D8 | Deliverables aligned to the group-assessment structure | Adopted | 2026-06-16 |
| D9 | Theory-grounded dashboard as a first-class output | Proposed | 2026-06-16 |
| D10 | Branch-and-pull-request version control with protected `main` | Adopted | 2026-06-16 |
| D11 | Forecasting treated as a stretch goal, need-side only | Proposed | 2026-06-16 |

---

## D1 — Equity-led visual-analytics direction
**Status:** Proposed · **Date:** 2026-06-16

**Context.** The brief invites innovative use of OpenActive data to increase physical activity in London. Several directions were viable, and we needed one that serves the brief, the client's mission, and the unit's marking criteria together.

**Decision.** Frame the project as an equity-led study of physical-activity provision *relative to need*, delivered as an interactive decision-support dashboard plus an equity-aware discovery prototype.

**Alternatives considered.**
- *A pure recommender-systems comparison.* Rejected: it cannot validate accuracy without behavioural data, and it barely addresses equity, ecosystem understanding, or embedding — all explicit requirements of the brief.
- *A pure data-quality / ecosystem audit.* Useful and required, but too narrow to carry a 60-credit capstone on its own.
- *A pure dashboard.* Plays to our visual-analytics strengths but risks under-serving the learning outcome that requires a working proof-of-concept system.

**Rationale.** Only the equity-led direction satisfies all five required outputs in the brief, sits squarely on London Sport's reason for existing (inactivity, deprived communities, equity), provides both a system (LO4) and a genuine variety of modelling techniques (LO3), and grounds its headline claims in real external data rather than synthetic ground truth.

**Consequences.** Two parallel strands (analysis, and prototype/dashboard) require clear ownership and active scope control.

**Revisit if** the supervisor or partner steers toward a materially different emphasis.

---

## D2 — Small-area (LSOA/MSOA) spatial granularity
**Status:** Proposed · **Date:** 2026-06-16

**Context.** The equity analysis relies on dimensionality reduction and clustering to reveal area typologies. The choice of spatial unit determines whether those methods are meaningful.

**Decision.** Conduct the projection and clustering analysis at small-area level — LSOA (~4,800 in London) or MSOA (~980) — rather than at the 33-borough level.

**Rationale.** Neighbour-based projections (t-SNE, UMAP) and clustering need enough data points to form meaningful structure; 33 boroughs is far too few and would produce noise. Small areas provide the necessary resolution and align with the native granularity of the deprivation data.

**Consequences / known trade-off.** The Active Lives inactivity signal is published only at borough level, so it is coarser than the provision and deprivation signals. This **granularity mismatch is handled explicitly** — analysing the affected relationships at borough level, or treating borough inactivity as an area-level attribute with stated caveats — rather than concealed.

**Revisit if** geocoordinate quality in the OpenActive data proves too poor to place sessions reliably into small areas; fall back to borough level.

---

## D3 — Disciplined method set (two projections + one validated clustering)
**Status:** Proposed · **Date:** 2026-06-16

**Context.** The team can implement many advanced methods, and there is a temptation to include all of them.

**Decision.** Use a deliberately restrained method set: two complementary projections (PCA for interpretable variance and loadings, plus one neighbour-based method), one clustering method, and explicit validation (silhouette analysis and cross-method agreement).

**Rationale.** Top-band work is judged on whether each method is the *right* choice for the question, not on the number of methods. Method-stacking that is not driven by the research question reads as display rather than reasoning and tends to lose marks. Two projections done well and validated is stronger than four included for show.

**Consequences.** Additional methods (a third projection, mixture models) are held as documented stretch options, to be added only if justified.

**Revisit if** the data reveals structure that a single neighbour-based method demonstrably fails to capture.

---

## D4 — Bayesian imputation for missing fields
**Status:** Proposed · **Date:** 2026-06-16

**Context.** OpenActive fields such as price, capacity, and precise location are expected to be incomplete and inconsistently populated.

**Decision.** Handle missing values with Bayesian iterative imputation — modelling each incomplete field from the others — rather than naive mean or mode filling, and quantify missingness explicitly before imputing.

**Rationale.** Probabilistic imputation preserves relationships between variables and carries explicit uncertainty, which is more defensible than mean-filling and consistent with the project's commitment to honest treatment of data limitations.

**Consequences.** Imputation introduces modelled values that must be flagged; downstream results affected by imputation are reported with appropriate caution.

**Revisit if** the audit shows a field is so sparse that imputation would fabricate rather than estimate — in which case that field is dropped or reported as unusable.

---

## D5 — Honest evaluation; no accuracy claims without behavioural data
**Status:** Adopted · **Date:** 2026-06-16

**Context.** OpenActive contains no bookings, clicks, or ratings, so there is no behavioural ground truth for "relevance."

**Decision.** Make no claim of validated predictive recommendation accuracy. Validate the equity analysis against *real* external datasets (deprivation, demographics, Active Lives). Evaluate the prototype only with ground-truth-free metrics (coverage, diversity, accessibility/affordability share, geographic spread). Use synthetic personas transparently for illustration and stress-testing — never as an accuracy benchmark. Evaluate the dashboard using recognised visualisation-validation levels.

**Rationale.** Defining synthetic users and then scoring models against rule-derived labels would largely measure agreement with our own rules, not real-world utility. Calibrated, honest claims are rewarded; overclaiming is penalised.

**Consequences.** Conclusions about the prototype are framed as demonstrations of method and design, not as proven performance.

**Revisit if** a genuine source of interaction data becomes available (e.g. from London Sport).

---

## D6 — Data sources and access strategy
**Status:** Proposed · **Date:** 2026-06-16

**Context.** "The data" was not initially specified precisely, and OpenActive is published as live feeds rather than a single file.

**Decision.** Use London Sport's Open Sessions feed as the principal OpenActive source, complemented by London venues from the wider national OpenActive catalogue, and join to external open data: the latest Indices of Deprivation, ONS Census 2021, ONS boundaries, and the Active Lives Survey. Confirm with the data lead which feeds count as "the data" and whether a historical export is available.

**Rationale.** Open Sessions is the partner's own openly-licensed data; the national catalogue adds London coverage from large operators; the external datasets provide the validated "need" signals the equity question requires.

**Consequences.** The live feed is a current snapshot with shallow history; longitudinal depth depends on a partner export. All sources and licences are recorded in handover material.

**Revisit if** the partner provides a different or richer dataset, or restricts scope.

---

## D7 — Audit-first sequencing
**Status:** Adopted · **Date:** 2026-06-16

**Context.** The feasibility of the whole analysis depends on fields (price, location, capacity) whose completeness is unknown until inspected.

**Decision.** Complete a data-quality and suitability assessment **before** committing to specific models. Method choices in the proposal are explicitly labelled as candidates pending this audit.

**Rationale.** Building modelling around assumed-present fields is the classic way these projects fail. Auditing first de-risks every downstream step and is itself a required output and evidence of mature practice.

**Consequences.** The project plan front-loads the audit (WS1) and gates later work on it.

---

## D8 — Deliverables aligned to the group-assessment structure
**Status:** Adopted · **Date:** 2026-06-16

**Context.** `SEMTM0044` is assessed as a group project, not as an individual dissertation.

**Decision.** Plan all deliverables around the unit's three assessed components: a group written report including a code repository (60%), a group oral presentation (20%), and an individual reflective account per member (20%). The dashboard, prototype, dataset, and handover pack are evidence inside the report.

**Rationale.** Aligning deliverables to the actual marking scheme avoids producing artefacts that are not assessed and ensures the 40% carried by the presentation and the reflective accounts is not neglected.

**Consequences.** Each member keeps a contribution log from day one to evidence individual engagement.

**Revisit if** the supervisor confirms a different assessment structure for the 2025/26 cohort (the specification we hold is the 2026/27 version).

---

## D9 — Theory-grounded dashboard as a first-class output
**Status:** Proposed · **Date:** 2026-06-16

**Context.** The project is framed as visual analytics, and the supervisor has asked us to apply visual-analytics methods.

**Decision.** Treat the interactive dashboard as a first-class, theory-grounded contribution: tasks articulated with an established task taxonomy; encodings justified against channel-effectiveness and perception principles; an absolute-versus-proportion toggle; projection views that disclose the variables used and provide informative tooltips; and interactions for exploration and drill-down.

**Rationale.** Justification of visualisation choices is an explicit, heavily-weighted assessment criterion, and a well-designed dashboard is the natural vehicle for the brief's "embedding" requirement.

**Consequences.** Visualisation rationale is documented (here and in the report), not left implicit.

**Revisit if** scope pressure forces a reduction; the dashboard's analytical core is protected as MVP.

---

## D10 — Branch-and-pull-request version control with protected `main`
**Status:** Adopted · **Date:** 2026-06-16

**Context.** Learning Outcome 1 explicitly requires good software-development practice and collaborative version control.

**Decision.** All work goes through short-lived branches and reviewed pull requests; nobody pushes directly to `main`, which is protected to require a pull request before merging. Branch naming follows `feature/`, `fix/`, `docs/`, `chore/`.

**Rationale.** A reviewed history is the direct evidence the unit assesses, and protecting `main` enforces the practice rather than relying on memory.

**Consequences.** Slightly more process per change, offset by a clean, reviewable history that also supports peer moderation.

---

## D11 — Forecasting treated as a stretch goal, need-side only
**Status:** Proposed · **Date:** 2026-06-16

**Context.** London Sport has expressed interest in forecasting participation, and the team can implement probabilistic forecasting with credible intervals.

**Decision.** Treat forecasting as a stretch goal, not a core commitment, and only on the *need* side (census or Active Lives trends) — never on OpenActive provision.

**Rationale.** The OpenActive live feed has no meaningful history, so forecasting provision would be unfounded. Need-side forecasting is defensible and aligns with the partner's interest, but it must not crowd out the core equity analysis.

**Consequences.** Forecasting is scoped in the stretch tier and added only if time and partner appetite allow.

**Revisit if** a historical OpenActive export materially changes what can be forecast.
