> **DRAFT — pending supervisor sign-off.** This is a working proposal, not an agreed plan. Method choices are candidates to be confirmed against the data-quality audit (see `decisions.md`). Do not treat as final until our supervisor has approved the direction and the team has agreed. Last updated 2026-06-16.

# Closing the Activity Gap
### An equity-led visual-analytics study of physical-activity provision in London using OpenActive data

**Project partner:** London Sport (problem owners: Josef Baines, Insight Manager; Muhammad Bilal Alam, Data & Analytics Lead)
**Unit:** MSc Data Science — Data Science Group Project (`SEMTM0044`, 60 credits, capstone), School of Engineering Mathematics and Technology, University of Bristol
**Academic supervisor:** Dalila O'Grady · **Teaching assistant:** Alex
**Team:** Michael, Clarence, Wesley, Fahmi
**Status:** Draft proposal for supervisor and partner sign-off
**Target hand-in:** 4 September 2026

> **Note on this draft.** The unit specification we are working from is the published `2026/27` version. Before this plan is finalised we will confirm with our supervisor that the `2025/26` assessment structure (20% group presentation, 60% group report, 20% individual reflective account) and the 4 September hand-in are unchanged. Method choices below are stated as *candidates to be confirmed against the data-quality audit* — the audit deliberately precedes any commitment to specific models. All dates assume a project start in the week of 16 June 2026.

---

## 1. Executive summary

London has one of the densest physical-activity ecosystems in Europe, yet roughly a quarter of adults are inactive, and inactivity concentrates in deprived communities — the populations London Sport exists to serve. The OpenActive standard now publishes more than two million activity opportunities nationally, but for London this is a *passive catalogue*: rich in supply-side detail, weak as a means of reaching the people who would benefit most.

This project asks a single, sharply-focused question: **where, and for whom, is London's activity provision failing to reach those who would benefit most, and how can data-driven discovery help close that gap?** It does so in two complementary parts. First, an analytical core builds a rigorous, reproducible picture of how activity provision is distributed *relative to need* — joining OpenActive supply data to deprivation, demographics, and Sport England Active Lives inactivity data to locate the areas where provision is thinnest precisely where need is highest. Second, it delivers a working proof-of-concept discovery prototype that is *equity-aware*, surfacing affordable, accessible, and locally reachable opportunities for underserved profiles, alongside an interactive decision-support dashboard for London Sport.

The headline analytical claims are validated against real external datasets, so they do not rest on fabricated ground truth, and the project treats data quality and honest uncertainty as first-class contributions rather than afterthoughts. The approach is deliberately disciplined: methods are included only where they are justified for this data and this question. Together the two parts address every required output in the brief and map cleanly onto all five unit learning outcomes.

---

## 2. Background and context

**The problem.** Physical inactivity is a major public-health issue whose burden falls most heavily on deprived communities. A well-evidenced barrier to activity is *discovery*: information about local sessions is fragmented across providers, formats, and platforms, and what little is consolidated tends to serve the already-active rather than those hardest to reach.

**OpenActive.** OpenActive is the national open-data standard for the sport and physical-activity sector. Providers publish "opportunity data" — sessions, schedules, locations, prices, availability — in a common format, harvested as live feeds. London Sport is a major publisher through its free Open Sessions tool, whose data is openly licensed and can be harvested now; the wider national catalogue additionally carries many London venues operated by large leisure providers.

**London Sport's intent.** London Sport wants to strengthen its use of innovative data and digital approaches to raise activity levels across the capital, improve audience engagement, and embed digital pathways into the everyday experience of finding and taking part in activity. Its strategy spans Active Environment, Community Sport, and Health, and its stated reasons for existing centre on inactivity, life expectancy, and deprived communities.

**The gap this project addresses.** Most existing OpenActive work treats the data as a supply catalogue to be surfaced through a finder. Far less asks *who that supply actually reaches*, *where it is missing relative to need*, and *how discovery could be designed for equity rather than for the already-active*. That is the space this project occupies, and it is precisely the space the brief flags through its explicit requirement to improve reach, engagement, and equity of access.

---

## 3. Aim and objectives

**Aim.** To analyse the equity of physical-activity provision across London using OpenActive and complementary open data, and to design, build, and evaluate visual-analytics tools — an interactive decision-support dashboard and an equity-aware discovery prototype — that demonstrate how this data can help reach London's least-active communities.

**Objectives.**

1. Characterise the current OpenActive ecosystem for London and rigorously assess the completeness, consistency, and suitability of the data for analysis and modelling.
2. Build an integrated, analysis-ready dataset combining OpenActive provision data with deprivation, demographic, and inactivity data, with documented, principled handling of missing and inconsistent values.
3. Map and statistically analyse the distribution of provision relative to population need, identifying priority "activity-gap" areas and underserved groups, and validating findings against real external data.
4. Design, build, and honestly evaluate an equity-aware discovery prototype and an interactive, theory-grounded visual-analytics dashboard.
5. Translate findings into practical, embeddable recommendations for London Sport, and package all work as reproducible handover material.

---

## 4. Research questions

These map one-to-one onto the five required outputs in the brief (see §12).

- **RQ1 — Ecosystem and data.** What does the current OpenActive ecosystem look like for London, and how complete, consistent, and usable is the data across providers?
- **RQ2 — Equity of provision.** How is the supply of activity opportunities distributed across London's small areas, and how does it relate to deprivation, demographic composition, and inactivity? Where are the largest gaps between provision and need?
- **RQ3 — Discovery and intervention.** Can an equity-aware, constraint- and content-based discovery prototype surface relevant, affordable, and accessible opportunities for underserved profiles — and what does evaluating it reveal about the limits of OpenActive data for personalised discovery?
- **RQ4 — Communication and embedding.** How can these insights be communicated through an interactive, theory-grounded dashboard, and embedded into London Sport's insight work, place-based targeting, and partner conversations?

---

## 5. Novelty, contribution, and method philosophy

The contribution is deliberately not "another activity finder" or "a benchmark of standard recommender algorithms," both of which are well-trodden. It is:

1. **An equity-of-provision analysis for London** that treats *need* — deprivation and inactivity — as the reference point, rather than treating the catalogue as an end in itself, and validates its central findings against real external datasets.
2. **A first-class data-quality and suitability assessment of OpenActive for London**, valuable to London Sport in its own right and explicitly requested in the brief.
3. **An equity-aware discovery prototype** that operationalises the analysis and is evaluated *honestly*, acknowledging the absence of behavioural data rather than overclaiming accuracy.
4. **A theory-grounded visual-analytics layer** — an interactive dashboard whose every encoding is justified against the principles of information visualisation and human perception.

**A note on discipline.** Top-band work is not the project with the most techniques in it; it is the one in which every method is the *right* method for the question and is justified as such. We therefore treat advanced methods (multiple projections, mixture models, forecasting) as a *menu of capabilities*, and let the data-quality audit determine which genuinely belong. We would rather run two complementary projections well and validate them than stack four for display. Method-stacking that is not driven by the question is avoided by design.

---

## 6. Data sources

All datasets are open and, with the partial exception of any historical export London Sport may share, can be accessed immediately.

**Primary — OpenActive.** London Sport's own Open Sessions feed (openly licensed, near real-time) is the principal source, complemented by London venues drawn from the wider national OpenActive catalogue. *Realistic caveat:* field population varies substantially by publisher — price, precise geocoordinates, and capacity are inconsistently present. Live availability via the Open Booking API requires authentication and is out of scope; we use published scheduled-session data. The data-quality assessment (WS1) gates how far the modelling can go and is therefore an early, not a late, task.

**Complementary — external open data.**

- The latest English Indices of Deprivation (Index of Multiple Deprivation) at small-area level (we will confirm the most recent release at the start of the project).
- ONS Census 2021 demographics and population estimates (age, ethnicity, disability, socio-economic indicators) at small-area and borough level.
- ONS boundary files for London's small areas and boroughs, for spatial joins and choropleth mapping.
- Sport England Active Lives Survey at borough level (proportion meeting 150+ minutes per week; inactivity), giving the "need" signal London Sport prioritises.
- *Stretch:* public-transport accessibility (e.g. PTAL) for a "reachability" dimension.

**Spatial granularity — a deliberate decision.** The equity analysis, projections, and clustering will be conducted at **small-area level (LSOA or MSOA)** — London has roughly 4,800 LSOAs and around 980 MSOAs — rather than at borough level. London's 33 boroughs are too few for neighbour-based projection and clustering methods to reveal meaningful structure; small areas provide the resolution those methods require, and align with the native granularity of deprivation data. We note openly that the Active Lives inactivity signal is published only at borough level, so it is coarser than the provision and deprivation signals; this granularity mismatch is handled explicitly (analysing the affected relationships at borough level, or treating borough inactivity as an area-level attribute with stated caveats) rather than concealed. Licensing for every source (predominantly the Open Government Licence and OpenActive's open terms) will be recorded in the handover material.

---

## 7. Methodology

The work is organised into five workstreams. Methods demonstrate a genuine *variety* of data-modelling techniques (LO3) while each step is justified by the research question it serves (LO5). Specific models are **candidates, confirmed or revised against the WS1 audit**.

**WS0 — Set-up and governance (Weeks 1–2).** Repository and environment set-up; agreed ways of working and a branch-and-pull-request version-control workflow; Community and Integrity training (a mandatory prerequisite for unit credit); literature and national-landscape review; data-access confirmation; the rough project plan for the first supervisor meeting and the full plan to share with London Sport.

**WS1 — Data engineering and quality assessment (Weeks 2–4).** Harvesting the Open Sessions feed and relevant national feeds (handling paged real-time exchange and incremental updates); schema normalisation into a single analysis-ready model; de-duplication of sessions appearing across feeds; geocoordinate validation and filtering to London by official boundaries (a spatial join, more accurate than a rectangular bounding box); and feature engineering. The deliverable is a documented data-quality and suitability assessment: per-provider field completeness, missingness patterns and quantities, granularity issues, staleness, and explicit limitations for modelling. This workstream gates the rest.

**WS2 — Equity and gap analysis (Weeks 3–7).** For each small area, construct provision measures (opportunity density per capita, diversity of activity types, share free or low-cost, share with accessibility information) and join them to deprivation, demographics, and inactivity. Then:

- **Missing-data handling:** Bayesian iterative imputation, modelling each incomplete field from the others so that missing values carry explicit uncertainty rather than being naively mean-filled; missingness is quantified and reported.
- **Structure discovery:** standardise features, then apply **two complementary projections** — Principal Component Analysis for interpretable variance and feature loadings, plus one neighbour-based method (t-SNE or UMAP) for cluster structure — and **one clustering method** (k-means or a Gaussian mixture) to identify area typologies, including an "underserved-and-inactive" priority cluster.
- **Validation:** silhouette analysis and cross-method agreement (e.g. rank correlation between projections) to test that the structure is real rather than an artefact of one method.
- **Gap index:** combine standardised need (inactivity, deprivation, population) against standardised provision into a transparent, interpretable activity-gap index, presented as a choropleth, with sensitivity analysis and the explicit caveat that absence of data is not absence of activity.

**WS3 — Discovery prototype and evaluation (Weeks 4–9).** A constraint- and content-based discovery engine: hard constraints applied first (price ceiling, travel distance, time window, accessibility requirements), then ranking by similarity to a user profile, with an **equity-aware re-ranking** mode that favours affordable, accessible, and underserved-area opportunities. Evaluation is deliberately honest (see §8).

**WS4 — Visual analytics, synthesis, and handover (Weeks 6–12).** An interactive, theory-grounded dashboard (see §9) that lets London Sport explore provision, need, and the gap index; synthesis into embeddable recommendations (insight work, place-based targeting, digital discovery, partner conversations, data-quality improvements); and reproducible handover material.

**Forecasting (stretch only).** If London Sport wants it and the data supports it, a probabilistic forecast with credible intervals may be added — but only on the *need* side (census or Active Lives trends), because OpenActive provision data has no meaningful history. It is not a core commitment.

**Tooling.** Python with pandas, geopandas, scikit-learn, scipy, and appropriate projection and spatial libraries; Tableau for the interactive dashboard; a lightweight interface for the prototype (command line minimum, simple web app as a stretch); Git and GitHub for version control with a branch-and-review workflow; an environment specification, tests for the data pipeline, data-validation checks, and feed-freshness monitoring to satisfy the documentation and monitoring expectations of LO5.

---

## 8. Evaluation strategy (and what we will *not* claim)

This is the methodological backbone of the project and a deliberate point of integrity.

OpenActive contains **no behavioural interaction data** — no bookings, clicks, or ratings. We therefore make **no claim to validated predictive recommendation accuracy**, because no real ground truth for "relevance" exists; we will not present any agreement-with-our-own-rules figure as an accuracy result. Instead:

- The **equity analysis (WS2)** is validated against *real* external datasets — deprivation, demographics, Active Lives — which is where genuine ground truth exists and where our strongest claims sit. Clustering and projection structure is validated with silhouette analysis and cross-method agreement.
- The **prototype (WS3)** is evaluated with **ground-truth-free metrics** meaningful without behavioural data: catalogue coverage, intra-list diversity, the share of accessible and affordable results, and geographic spread across priority areas. Synthetic personas are used transparently to illustrate and stress-test behaviour, documented as a reusable benchmark, and explicitly *not* treated as an accuracy ground truth.
- The **dashboard (WS4)** is assessed using recognised visualisation-validation levels, including, if feasible, a small user-based task evaluation with peers to check that intended insights are actually recovered.

Limitations and the conditions under which results should be treated with caution are stated prominently throughout.

---

## 9. Visualisation approach and justification

Because the project is framed as *visual analytics*, the visualisation layer is treated as a first-class, theory-grounded contribution rather than decoration, and its design choices are explicitly justified — a key assessment emphasis.

The dashboard is designed around well-defined analytical tasks (locate gaps; compare areas; relate provision to need; identify outliers and typologies), articulated using an established task taxonomy. Encoding choices are justified against channel-effectiveness principles and human perception: choropleths for spatial distribution of provision, need, and the gap index; projection scatterplots for area typologies; and ranked views for the prototype's output. The dashboard offers a toggle between **absolute values and population-adjusted proportions** (essential when comparing areas of different size); projection plots **disclose which original variables were used** and provide informative tooltips identifying each point, so that reduced-dimension views remain interpretable; and interactions (highlighting, filtering, drill-down to an area profile) support fluent exploration. The intended users — London Sport's insight and commissioning staff, and partners — are kept explicit, so the design serves real decision-making and the brief's "embedding" requirement.

---

## 10. Ethics, responsible innovation, and data governance

The project uses only open, non-personal, aggregate data, so individual-privacy risk is low. The substantive responsible-innovation considerations are: the risk that an equity tool *reinforces* inequity if provision data is itself biased (better-resourced providers publish more, so absence of data is not absence of activity); the danger of presenting a gap index as fact when it rests on incomplete supply data; and fair, non-stigmatising representation of deprived communities. We will document these explicitly, caveat the gap index accordingly with sensitivity analysis, and recommend that London Sport treat outputs as decision-support rather than ground truth. All data sources and licences will be recorded.

---

## 11. Deliverables mapped to the unit assessment

The unit is assessed entirely by coursework, in three components. Every deliverable is planned around that structure — not around a traditional individual dissertation.

| Deliverable | Unit assessment component | Weight | Learning outcomes |
|---|---|---|---|
| Group written report, including code viewable in an online repository (executive summary, analytical report, data-quality assessment, methodology, model/visualisation performance and limitations, practical implications, reproducible handover) | Group written report | **60%** | LO1–LO5 |
| Conference-style group oral presentation | Group oral presentation | **20%** | LO2, LO5 |
| Individual reflective account of the project experience and teamwork (collaborative-tool use, version control, peer review, individual contribution) — written separately by **each** team member | Individual reflective account | **20%** | LO1, LO2, LO5 |

Supporting artefacts inside the report and repository: the integrated clean dataset with documentation; the interactive dashboard; the discovery prototype with documented synthetic personas; and the reproducible handover pack (code/notebooks, method notes, data-source notes, assumptions, and reproduction instructions).

> **Two assessment points the team must not overlook.** The group presentation and the individual reflective account together carry **40%** of the marks. The reflective account is individual and is where peer moderation and personal engagement in supervised meetings are evidenced — keep a contribution log from day one.

---

## 12. Mapping to the brief's required outputs

| Brief required output | Where addressed |
|---|---|
| Demonstrate a clear understanding of the current OpenActive ecosystem | RQ1 / WS0–WS1 |
| Highlight various approaches used across the country | National-landscape review (WS0), report |
| Identify challenges and opportunities in how Londoners search for and engage with local activities | RQ1, RQ2 / WS1–WS2 |
| Propose innovative digital or data-driven interventions improving reach, engagement, and equity | RQ3, RQ4 / WS3–WS4 |
| Highlight how these approaches could be embedded into London's system | RQ4 / WS4 |

---

## 13. Mapping to learning outcomes

| LO | How the project evidences it |
|---|---|
| LO1 — Teamwork with good software practice and version control | GitHub repository with a branch-and-review workflow, shared environment, documented in handover and reflective accounts |
| LO2 — Communicate within the team and with stakeholders | Weekly supervised meetings, partner updates routed through supervisors, non-technical executive summary, the dashboard, and the final presentation |
| LO3 — Multiple sub-tasks and a variety of modelling techniques | Data engineering, Bayesian imputation, dimensionality reduction, clustering with validation, a gap index, and similarity-based discovery |
| LO4 — A workable proof-of-concept system addressing client needs | The equity-aware discovery prototype and the interactive dashboard, addressing London Sport's reach-the-least-active need |
| LO5 — Document design decisions (tools, environments, testing, monitoring) | Methodology and design-decision log, theory-grounded visualisation justification, pipeline tests and data-validation checks, feed-freshness monitoring, handover pack |

---

## 14. Project plan and timeline

Weeks run from 16 June to 4 September 2026. The formative review-panel presentation falls roughly four weeks in, per the unit specification; a buffer week is built in deliberately.

| Week | Dates | Phase | Key activities | Milestone |
|---|---|---|---|---|
| 1 | 16–22 Jun | Set-up | Ways of working, repo/environment, Community & Integrity training, landscape review begins, data-access confirmation | **Rough plan for first supervisor meeting** |
| 2 | 23–29 Jun | Set-up / data | First feed harvest; initial data-quality probe (gating); full plan drafted | **Full plan shared with London Sport** |
| 3 | 30 Jun–6 Jul | Data | Schema normalisation, de-duplication, London filtering, small-area aggregation, feature engineering | Integrated dataset v1 |
| 4 | 7–13 Jul | Data / analysis | Data-quality assessment finalised; exploratory analysis; begin equity joins | **Formative review-panel presentation; optional report skeleton** |
| 5 | 14–20 Jul | Analysis / build | Bayesian imputation; provision measures; projections; prototype engine scaffold | — |
| 6 | 21–27 Jul | Analysis / build | Clustering and validation; constraint logic and ranking; dashboard scaffold | Mid-project progress review |
| 7 | 28 Jul–3 Aug | Analysis / build | Gap index; equity-aware re-ranking; dashboard build; begin drafting report | Analysis feature-complete |
| 8 | 4–10 Aug | Evaluation | Ground-truth-free prototype evaluation; dashboard validation; integration | Prototype & dashboard feature-complete |
| 9 | 11–17 Aug | Writing | First full report draft; reproducibility packaging | **Full draft report** |
| 10 | 18–24 Aug | Polish | Report editing; presentation build; code clean-up; handover; reflective-account drafts | Presentation v1 |
| 11 | 25–31 Aug | Buffer / QA | Dry-run presentation; claim and citation check; reproducibility test; finalise reflective accounts | Submission-ready |
| 12 | 1–4 Sep | Submit | Final proofing and submission | **Hand-in 4 Sep** |
| Oct | — | (Optional) | Present to London Sport as an organisation | — |

---

## 15. Team and roles

Everyone contributes across the project, but clear lead ownership protects both delivery and the individual peer-moderation marks. Assign to strengths, agree explicitly at the first meeting, and record in `docs/`. A suggested allocation, to refine as a team:

- **Project lead and stakeholder coordination** — owns the schedule, minutes, action tracking, and the single channel to the supervisors.
- **Data-engineering lead** — owns harvesting, the pipeline, and the data-quality assessment (WS1).
- **Analysis and modelling lead** — owns the equity analysis, projections, clustering, and validation (WS2).
- **Prototype and evaluation lead** — owns the discovery engine and its honest evaluation (WS3).
- **Visualisation lead** — owns the dashboard, the theory-grounded visualisation justification, and report integration (WS4).

With four members, the visualisation and analysis leads (or prototype and data-engineering leads) may pair on adjacent workstreams. Cross-cutting expectations for all: disciplined version control, pair review of each other's code, ownership of the relevant report sections, and an individually written reflective account.

---

## 16. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| OpenActive data sparser than hoped (missing price, geocoordinates, capacity) | High | High | Front-load the data-quality audit; Bayesian imputation with uncertainty; fall back to coarser geography; report sparsity as a finding |
| Small-area work infeasible if geocoding is poor | Medium | High | Validate geocoordinates early; fall back from LSOA/MSOA to borough level |
| Scope creep across analysis, prototype, and dashboard | Medium | High | Locked scope; supervisor sign-off; MVP/stretch split (§17); disciplined method selection |
| Over-reliance on synthetic personas for evaluation | Medium | High | Honest framing (§8); anchor headline claims to real external datasets |
| Granularity mismatch (borough-level Active Lives vs small-area provision) | High | Medium | Handle explicitly; analyse affected relationships at borough level; state as a limitation |
| Uneven team contribution | Medium | Medium | Git history, weekly minutes, peer review, contribution log |
| Assessment structure/dates differ for the 25/26 cohort | Low | Medium | Confirm with supervisor before locking the plan |
| Late or partial partner data share | Medium | Low | Start with open feeds immediately; do not block on the partner share |

---

## 17. Minimum viable project vs stretch

**Minimum viable (must deliver):** a defined set of harvested London feeds; the data-quality and suitability assessment; small-area provision mapping and exploratory analysis; an equity/gap analysis joining deprivation, demographics, and inactivity, with Bayesian imputation, two projections, one validated clustering, and a gap index; a working equity-aware discovery prototype with ground-truth-free evaluation; a theory-grounded interactive dashboard; and the report, presentation, and reflective accounts.

**Stretch (if time allows):** transport-reachability features; a third projection or mixture-model comparison; need-side probabilistic forecasting with credible intervals; a user-based dashboard evaluation; and a lightweight web interface for the prototype.

---

## 18. Immediate next actions

1. Agree this direction as a team, then confirm it with the supervisor at next week's meeting; bring the rough plan.
2. **Route all partner communication through the supervisors**, not directly to London Sport.
3. Complete the Community and Integrity training (a hard prerequisite for unit credit).
4. Confirm roles and record them; maintain the branch-and-pull-request workflow already in place.
5. Begin the OpenActive data audit now — the data is open, so do not wait for the partner share.
6. Through the supervisors, ask the data lead which feeds count as "the data," and whether a historical export beyond the live feed is available.

**Questions to confirm with the supervisor / partner:**

- Which exact OpenActive feeds or sources count as "the data," and is a historical export available beyond the live feed?
- Does the `2025/26` assessment structure match the `2026/27` specification, and is the hand-in 4 September 2026?
- Is any individual dissertation also required, or is the group report the sole written output for this unit?
- Does London Sport prefer emphasis on insight/analysis, on the tools, or on both, and are there priority boroughs or populations?

---

## 19. What "top band" looks like for this unit

A distinction-level outcome is driven less by algorithmic volume than by a genuinely useful result for the client; calibrated, well-evidenced claims with honest limitations; theory-grounded, justified visualisation; a clean, reproducible engineering trail; evident teamwork and version-control discipline; and communication pitched correctly for both technical and non-technical audiences. This plan is built around those criteria, and around methods the team can execute. The mark will ultimately follow execution — disciplined delivery against this plan — but the plan puts the team in clear contention for the top band.
