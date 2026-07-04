# Group report skeleton — Closing the Activity Gap
**Purpose:** the load-bearing scaffold for the 60% group written report. The logical thread is designed in from the start so results flow into a structure rather than being assembled in an August panic (the exemplar's merit-capping failure was precisely a missing thread). Every section states its job in the thread, what feeds it, its owner, and its status.
**Rules of use:** no number enters this report unless it traces to `results/metrics.csv` or a committed results file · British English · referencing from `docs/references.bib` only, style **[CONFIRM: Harvard per decision log vs IEEE per handbook example/LaTeX template — must be flawless either way]** · terminology per the glossary · team always alphabetical: Clarence, Fahmi, Michael, Wesley · every chapter opens with a 2–3 line intro and closes with a summary (handbook convention).
**CONFIRMED by the handbook (see `docs/unit-rules.md` — binding):** submission **1pm Friday 4 September 2026 via Blackboard** · report **max 30 pages** (first chapter → last chapter; appendices/references excluded) · **5 marks deducted per page over** · **LaTeX template provided, LaTeX recommended — obtain before drafting** · presentation 15 min live on Teams, late-Aug window, all members contribute · **Dalila reviews exactly ONE full draft, needs ≥14 days and a pre-agreed date → target draft to her ~10–14 August**.

**Page budget (30 total — enforced, adjust only by trading between sections):**
Intro 2 · Literature 4 · Data & data quality 4.5 · Methodology 4 · Results (equity) 6 · Prototype 3.5 · Dashboard 2.5 · Discussion 2 · Limitations 1.5 · Conclusions 1.5 ≈ 31.5 → trim ~1.5 by moving detail tables to appendices (excluded from the count — the engineering/reproducibility material lives there at zero page cost).

---

## THE LOGICAL THREAD (one paragraph — every section serves it)

> London's physical inactivity concentrates in its most deprived communities. OpenActive publishes tens of thousands of activity opportunities, but as a passive catalogue it says nothing about whether supply reaches need. We build the first equity-reasoned account of that data for London: a gating data-quality audit shows openly-published community provision is thin and spatially concentrated (itself a finding), forcing a defensible borough-level design; on that basis we construct a transparent activity-gap index, validate it non-circularly against held-out inactivity (ρ=0.459, CI [0.13, 0.70]), and show the gap is more than deprivation relabelled (provision adds independent signal). We then operationalise the analysis: an equity-aware discovery prototype that re-ranks toward affordable, accessible, underserved-area opportunities (evaluated honestly, with no accuracy claims), and a theory-grounded dashboard for London Sport's insight work. The report closes with what this means for closing London's activity gap — and for improving the data that must underpin any attempt to do so.

**The sentence-length version:** *Openly-published community provision in London is thin, uneven, and misaligned with need; we measure that misalignment credibly and build the tools to act on it.*

---

## SECTION PLAN

### 0. Abstract / Executive summary — write LAST
Thread in miniature: problem → data reality → gap index + validation → tools → recommendations. One paragraph for the examiner, one for London Sport. **Owner:** all (drafted by Michael, reviewed by all). **Status:** not started (deliberately).

### 1. Introduction and problem context
**Job in thread:** establish the activity gap as a real, quantified public-health equity problem and *discovery* as a tractable lever; state RQ1–RQ4; preview the thread explicitly ("this report shows…").
**Feeds:** proposal §2 (sourced inactivity figures: England ~25% inactive; London 26.4% 2020/21; 15 of 32 boroughs below national average — re-verify vintages before use); brief's five required outputs (map them in a footnote or table here).
**Marks note:** the "discovery as a barrier" premise still needs a citation (audit M5 → lit review).
**Owner:** Michael (draft), all review. **Status:** not started. **LO2.**

### 2. Background and literature review — **the largest remaining writing gap**
**Job in thread:** position the work in four literatures so the contribution is legible: (a) physical inactivity and health inequality; (b) equity of access to sport/leisure provision (incl. 2SFCA/E2SFCA accessibility tradition); (c) recommender systems for leisure discovery + the limits of offline evaluation (Herlocker et al. 2004 anchor); (d) visual analytics for spatial decision support (Munzner anchor). Close with the gap this project fills (equity-reasoned use of open opportunity data).
**Feeds:** `docs/references.bib` (to be built; proposal's list is the seed; new entries enter as TODO-VERIFY until a member reads the paper).
**Depth rule (exemplar lesson):** 4–6 papers deep per strand beats 9 shallow.
**Owner:** all four, one strand each (Clarence: recommenders; Fahmi: evaluation validity; Michael: visual analytics + equity-of-provision; Wesley: inactivity/public health + open data). **Status:** not started. **LO3 grounding.**

### 3. Data and data quality (WS1)
**Job in thread:** what the data IS, and the audit that gates everything above it. This section carries the "thin, concentrated, under-published" finding and the borough decision — the report's first substantive result, not a chores list.
**Content:** sources table with vintages and licences (Open Sessions 2026-06-30 frozen snapshot · IoD2025 File 10 v2 · Census 2021 · Active Lives 2024/25 via Fingertips 93015 · boundaries LAD 2021; CC-BY attribution) · Open Sessions correctly described (nationwide platform; London subset: 494 series, 264 venues, 43.9% free, paid median £10.00) · granularity audit (LSOA 95.5% / MSOA 81.2% empty → D-008 borough) · missingness stances (no imputation, D-010; `is_free` for MNAR price) · coverage bias as the defining limitation · the event-harvest universe finding (commercial feeds ≈99% paid; 2.30% free of price-known) with its audit story · the number-verification protocol (metrics manifest, D-016) presented as methodology.
**Feeds:** `docs/open_sessions_data_note.md`, `docs/event_harvest_audit.md`, `results/metrics.csv`, granularity/completeness reports, WS1 audit outputs.
**Owner:** Wesley (draft), Michael (verification narrative). **Status:** ~70% of content exists in repo docs — needs assembly and prose. **LO3, LO5; brief outputs 1–2.**

### 4. Methodology (WS2 design)
**Job in thread:** the gap index and its validation design, defensible under viva pressure.
**Content:** need composite (deprivation + demographics; **inactivity held out — D-012 stated as a design principle with the reversal proof**) · provision (log1p sessions per 10k; City excluded from scaling) · gap = need_z − provision_z with rank-based twin · quadrant typology as the primary structural lens (D-010) · weight-sensitivity design · validation-by-triangulation design · incremental-validity design (partial Spearman primary at n=32 — justify rank-based as primary BEFORE results appear) · what we deliberately did NOT do and why (no imputation, no t-SNE/UMAP, PCA descriptive-only — subtraction as judgement, D-010) · decision-log convention as method.
**Feeds:** `gap_index.py` docstrings, decision log, hand-off §6.1.
**Owner:** Michael. **Status:** design settled and implemented; prose not started. **LO3, LO5.**

### 5. Results — the equity of provision (WS2)
**Job in thread:** answer RQ2. Order the results as the thread demands:
1. Provision is thin/clustered (borough distribution; City zero; median 7 series).
2. The gap ranking (priority top-10: Enfield, Barking & Dagenham, Hackney, Tower Hamlets, Newham…) + quadrant map.
3. Robustness: weight sensitivity 0.976/0.952; z vs rank construction agreement.
4. **Held-out validation:** ρ=0.459, CI [0.131, 0.696], t=2.83, p=0.0083, n=32 — with the non-circularity proof cited.
5. **Incremental validity (D-013):** partial ρ −0.498 (p=0.004); ΔR²=0.070, nested-F p=0.110 — reported with the honest framing (monotonic-but-non-linear; rank test primary; parametric marginal).
6. The geography narrative: gap over-calls deprived-but-active inner boroughs, under-calls car-dependent outer ones; Hillingdon as genuine corroboration — *why ρ is 0.46, not 0.9, and why that is more informative*.
7. Affordability/universe finding (free provision lives in the community layer).
Every figure regenerated from committed code; caption cites script + results file.
**Feeds:** `borough_gap_index.csv`, `reports/incremental_validity.csv`, `results/metrics.csv`, hand-off §7 narrative (now verified).
**Owner:** Michael (draft), Fahmi (four-eyes re-derivation of every number before submission). **Status:** analysis DONE and frozen (WS2); prose not started. **LO3; brief output 2.**

### 6. Deployment I — the equity-aware discovery prototype (WS3)
**Job in thread:** operationalise the analysis (RQ3): deterministic hard-constraint filtering → content-based similarity → equity re-ranking (score = α·relevance + (1−α)·equity, where the equity term rewards affordable, accessible, underserved-area options — the underserved weight comes FROM the gap index, tying the layers together).
**Non-negotiables:** no learned model; NO accuracy claims (no interaction ground truth); beyond-accuracy evaluation only — coverage, intra-list diversity, affordable/accessible share, geographic spread into priority boroughs — across the α sweep; synthetic personas transparently illustrative.
**Feeds:** to be built — the report's largest outstanding dependency (LO4).
**Owner:** Clarence (build), Fahmi (evaluation design — design it BEFORE the build fixes behaviour). **Status:** designed, not built. **LO4; brief output 3.**

### 7. Deployment II — the dashboard (WS4)
**Job in thread:** communication and embedding (RQ4). Each view justified by the decision it supports (Munzner task framing); vintage + absence-of-data caveat on every provision view; no number computed in the dashboard that is not already a pipeline artefact; code-based/reproducible (Tableau rejected — CR-6).
**Owner:** Michael. **Status:** not started. **LO2, LO4; brief output 4.**

### 8. Discussion — what this means for closing the activity gap
**Job in thread:** synthesis for London Sport: where to target (priority quadrant), what discovery can and cannot fix, what the data itself needs (publish prices, accessibility info — London series carry access info at 22.7% vs 43.7% nationally; publish to standard). Compare findings against the literature from §2. Embedding routes: insight work, place-based targeting, partner conversations.
**Owner:** all four (workshop the recommendations together). **Status:** raw material exists across docs; not started. **LO2; brief output 5.**

### 9. Limitations and responsible use
**Job in thread:** the honesty that earns marks. Coverage bias (provision = lower bound; "under-served" may be "under-published") · n=32 (CIs lead, not p-values) · ecological inference held at bay by design but named · vintage heterogeneity (2021 Census demographics the weakest link) · no causal claims · no accuracy claims · gap index is decision-support, not ground truth · equity tools can reinforce inequity if data bias is ignored.
**Feeds:** audit docs; hand-off §15 viva-question list (pre-empt each in one sentence).
**Owner:** Fahmi (draft), all review. **Status:** content fully exists; needs assembly.

### 10. Conclusion + recommendations to London Sport
Answer each RQ in one paragraph; five brief outputs explicitly checked off; three-to-five concrete, prioritised recommendations (target priority boroughs; data-quality improvements to Open Sessions publishing; embed dashboard in insight workflow; discovery-layer pilot).
**Owner:** all. **Status:** not started.

### 11. Reproducibility and engineering appendix (LO1/LO5 evidence)
Repo structure · branch→PR→review→squash workflow (with evidence: PR history) · pinned `environment.yml` · deterministic pipeline (within-env byte-identical regeneration, documented cross-env caveat) · test suite incl. the D-012 reversal proof and known-answer statistics tests · metrics manifest protocol (D-016) · decision log · AI-use disclosure per unit rules (assisted contributions logged; verification always human+dual-method).
**Feeds:** `docs/full_audit_2026-07-03.md` §1 and §5 — much of this section is already written.
**Owner:** Wesley (repo/workflow), Michael (verification protocol). **Status:** ~60% exists.

### 12. References — Harvard, from `docs/references.bib` only. **Free-marks rule:** zero formatting errors (the exemplar lost real marks here).

### 13. Appendices: A decision log (D-001–D-016) · B data-quality audit detail · C metrics manifest snapshot · D glossary (canonical terms) · E additional figures/tables.

---

## LO COVERAGE CHECK (every LO must be *visibly* evidenced)
- **LO1** teamwork/version control → §11 + PR history + contribution statements.
- **LO2** communication → §1, §7, §8, presentation; plain-English framing throughout.
- **LO3** variety of techniques → §3–§5 (geospatial, composite indices, rank statistics, partial correlation, spatial autocorrelation) + §6 (similarity/re-ranking) — *variety through appropriateness, not stacking (D-010)*.
- **LO4** working proof-of-concept → §6 + §7. **Currently the report's biggest dependency: unbuilt.**
- **LO5** documented design decisions → decision log woven through §3–§7 + §11.

## BUILD ORDER (so writing never blocks on building)
1. §3 + §5 assembly can start NOW (all content verified and frozen).
2. §2 literature runs in parallel now (no data dependency; four strands, one per member).
3. §4 + §9 + §11 largely exist — assembly passes.
4. §6/§7 prose follows the WS3/WS4 builds — the builds are the critical path, start immediately.
5. §1, §8, §10, §0 last, once the thread's endpoints are fixed.

## HARD DATES (handbook-derived — the spine of the calendar)
- **~10–14 Aug:** full draft to Dalila (agree the exact date with her NOW; ≥14 days before feedback is needed; one draft only).
- **Week of 24 Aug onward:** final-presentation window (15 min, Teams) — book the slot early; prep overlaps the polish phase.
- **1pm Fri 4 Sep:** portfolio submission via Blackboard (report + reflective accounts).
- Working backwards: WS3/WS4 feature-complete by ~early August, or the draft goes to Dalila with placeholders in its LO4 sections — plan to avoid that.

## STANDING RISKS FOR THE REPORT
- LO4 unbuilt (highest marks-risk — mitigate by starting WS3 spec this week; team availability reduced by reassessments is a compounding factor, raise with Dalila).
- **30-page ceiling with a 5-marks-per-page penalty** — the budget above is enforced at every draft build; appendices are the pressure valve.
- Referencing style unresolved (Harvard vs IEEE/template) — zero-error requirement either way.
- Supervisor sign-off still pending on D-009/D-010/D-011 + D-014 reframe — take this skeleton, the audit, and `docs/unit-rules.md` queries to Dalila.
- Four-eyes pass (Fahmi) required before any §5 number is typeset.
- **Reflective-account inputs are accruing NOW:** every member needs a weekly log and visible repo activity (handbook mandates a GitHub-activity visualisation per member — a member without commits has nothing to show).
