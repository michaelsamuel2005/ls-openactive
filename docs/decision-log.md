# Decision log — Closing the Activity Gap (SEMTM0044)

Canonical, single-source record of the project's settled methodological
decisions. **This file wins over any other document** (CLAUDE.md, the project
instructions, the proposal): if they disagree, fix them to match this log.

Convention: one dated entry per decision (D-0NN), with rationale and the
alternatives considered.

> **Consolidation status (updated 2026-07-06).** D-011 and D-012 are captured in
> full (see `docs/D-011_decision_log.md`, `docs/D-012_decision_log.md`,
> summarised below). D-007–D-010 are summarised from verified cross-references.
> **The founding decision log (16 June 2026, eleven entries) has been recovered
> from PR #3's branch and preserved verbatim in `docs/decisions-founding.md`** —
> consolidation is now complete; nothing remains scattered.

## Founding decisions (2026-06-16) — status map
The founding log used unpadded IDs (D1–D11); the post-audit series below
restarted at zero-padded D-007, so the two series are distinct labels (founding
"D7" ≠ "D-007"). Full founding texts: `docs/decisions-founding.md`.

| Founding | Decision | Current status |
|---|---|---|
| D1 | Equity-led visual-analytics direction | Adopted (the framework) |
| D2 | Small-area (LSOA/MSOA) granularity | **Superseded by D-008** (borough, audit-forced) |
| D3 | Two projections + one validated clustering | **Superseded by D-010** (quadrants primary; PCA descriptive-only) |
| D4 | Bayesian imputation | **Superseded by D-010** (no imputation; missingness is a finding) |
| D5 | Honest evaluation, no accuracy claims | Adopted — standing, unbroken |
| D6 | Data sources & access strategy | Refined by **D-009/D-011** (Open Sessions primary; layers never merged) |
| D7 | Audit-first sequencing | Adopted — executed (the audit produced D-008/D-010) |
| D8 | Deliverables aligned to assessment | Adopted — confirmed by the 2025/26 handbook (`docs/unit-rules.md`) |
| D9 | Theory-grounded dashboard first-class | Adopted — WS4, build pending |
| D10 | Branch → PR → review, protected `main` | Adopted — CI + protection now mechanical |
| D11 | Forecasting = need-side stretch only | Standing (stretch tier) |

---

## D-007 · Deprivation source = IoD2025 *(summary — migrate full text)*
- **Decision:** Use the **English Indices of Deprivation 2025** (MHCLG) as the
  deprivation input, specifically **File 10 v2** (lower-tier LAD summaries, the
  17 Nov 2025 reissue). Not IoD2019.
- **Status:** Adopted; source verified against gov.uk on 2026-07-01 (File 10 v2,
  33/33 London boroughs, `IMD - Average score`).

## D-008 · Unit of analysis = London borough (LAD), n=33 *(summary — migrate full text)*
- **Decision:** The unit of analysis is the **borough / local authority
  district** (32 boroughs + City of London = 33). Settled by the WS1 audit:
  ~95.5% of LSOAs and ~81.2% of MSOAs carry zero sessions *(as measured at the
  time; superseded → 95.6% / 81.4% on the frozen 06-30 snapshot — see the
  correction record below)*, so neighbourhood-level
  analysis is not viable.
- **Status:** Decided (not a candidate). The whole pipeline is borough-keyed.

## D-009 · Provision-layer separation *(summary — migrate full text)*
- **Decision:** OpenActive **Open Sessions** is the primary community-provision
  feed; the wider national catalogue is **not merged** into it. (Extended by
  D-011 into a two-layer architecture: sessions and facilities analysed
  separately.)
- **Status:** Adopted.

## D-010 · Methods right-sized for n≈33 *(summary — migrate full text)*
- **Decision:** For n≈33, **imputation is dropped** (including MICE);
  **t-SNE/UMAP are dropped**; **PCA is descriptive-only**; the **need×provision
  quadrant typology is the PRIMARY structure**; the gap index is hardened; and
  **E2SFCA is a conditional** accessibility extension.
- **Status:** Adopted (changes methods, not data).

## D-011 · Tiered, validated external-data architecture *(full text: `docs/D-011_decision_log.md`)*
- **Decision:** Adopt Tier 1 + Tier 2 of the data plan: **two-layer provision**
  (community sessions primary; Active Places facilities independent, never
  merged); a **need composite** from IoD2025 + Census demographics + (originally)
  inactivity, reported under ≥2 weightings; **PTAL-weighted E2SFCA** accessibility
  as a conditional extension; and **validation by triangulation** with the
  facility layer as corroboration. Tier 3 held as documented candidates only.
- **Status:** Proposed → adopted for WS1; contingencies (Active Places licence,
  PTAL London-only, Active Lives CIs, supervisor sign-off) tracked in the full log.
- **Note:** the validation clause is **tightened by D-012** below.

## D-012 · Held-out validation — hold inactivity out of need *(full text: `docs/D-012_decision_log.md`)*
- **Decision:** Hold **adult inactivity (Active Lives) OUT of the need composite**
  and use it as the **independent, held-out validation target**. Restrict
  validation anchors to held-out signals only — deprivation and demographics are
  need **inputs** and are **never** used as validators (that was circular).
  Need = deprivation (IoD2025) + Census demographic risk; provision = community
  sessions; corroboration = Active Places facilities.
- **Status:** Adopted and implemented 2026-07-01 (`src/pipeline/gap_index.py`;
  `tests/test_analysis.py` enforces it, incl. a perturbation "held-out proof").
- **Result:** held-out validation runs at **Spearman(gap, inactivity) = +0.459**
  (non-City, n=32), proven non-circular. Refines D-011's validation clause and
  updates Proposal §§6–8 (v4). Next step: the incremental-validity check
  (`docs/incremental-validity-spec.md`).

## D-013 · Incremental validity — the gap is "more than deprivation relabelled" (rank-based) *(finding, 2026-07-01)*
- **Question:** does the *provision* layer add predictive signal for held-out adult
  inactivity **beyond need alone**? (The sharpest examiner challenge to the gap index.)
- **Method:** on the 32 non-City boroughs — partial Spearman (provision & gap vs
  inactivity, controlling need); nested OLS (need vs need+provision); Moran's I on the
  residuals. Stats implemented in `src/incremental_validity.py`, verified against
  scikit-learn + statsmodels. Spec: `docs/incremental-validity-spec.md`.
- **Result:**
  - **Rank-based (primary, robust at n=32):** partial ρ(provision, inactivity | need) =
    **−0.498 (p=0.004)**; partial ρ(gap, inactivity | need) = **+0.363 (p=0.045)**;
    provision ⟂ need (ρ=−0.05); gap·ι (+0.46) > need·ι (+0.30); R²(gap)=0.24 > R²(need)=0.18.
  - **Parametric (linear OLS):** ΔR² = **+0.070**, nested-F **p=0.110** (marginal); provision
    coefficient 95% CI includes 0. The Spearman≫Pearson gap for provision (−0.49 vs −0.31)
    indicates a **monotonic-but-nonlinear** provision–inactivity relationship that linear
    OLS under-captures.
  - **Spatial:** Moran's I on residuals = +0.08 (z=+0.94, p=0.35) → little residual spatial
    autocorrelation; the finding is not a spatial artefact.
- **Verdict (honest, calibrated):** provision carries **independent, significant signal**
  by the rank-based test — the gap is more than deprivation relabelled — **but** the
  linear-parametric test is only marginal at n=32. Report both; lead with effect sizes and
  the nonlinearity, not a single p-value. **No causal / individual-level claim** (borough-
  level, observational).
- **Follow-ups (not blocking):** a nonlinearity-aware model (e.g. rank/spline on provision);
  a spatial-error model if a larger indicator set inflates residual autocorrelation.
- **Precision note (2026-07-03):** code-traceable inference added
  (`spearman_inference()`, audit M1): gap–inactivity ρ=0.459, **95% CI [0.131, 0.696]**,
  t=2.83, p=0.0083, n=32. Orthogonality: the "ρ=−0.05" above is the **Spearman** (−0.047);
  the **Pearson is −0.111** — an informal "Pearson −0.05" that circulated in the hand-off
  was incorrect and is superseded.

## D-014 · Two-lens provision — REFRAMED (2026-07-03) *(supersedes the gated proposal)*
- **Original proposal:** measure provision as availability (`sessions_per_10k`, primary)
  AND intensity (`events_per_10k`), gated on Wesley reconciling event-harvest
  inconsistencies.
- **What the audit found** (`docs/event_harvest_audit.md`): the event harvest covers only
  the 37 ScheduledSession feeds — **Open Sessions publishes none**, so the event data is a
  **different provider universe** (commercial/institutional operators), not an intensity
  view of Open Sessions. All §11 contradictions resolved as scope/definition artefacts
  (527 venues = UK; 128 = London; 1.02% free = all-rows denominator over a 55%-price-unknown
  population; 2.30% on price-known rows).
- **Decision:** `events_per_10k` from that harvest is **not** an Open Sessions intensity
  lens and is never presented as one. Options going forward: (a) treat the event harvest as
  a third, commercial-universe provision layer under D-011 separation discipline (after the
  §3 defect fixes and a controlled re-harvest); (b) harvest Open Sessions' own events feed
  (`opensessions.io/api/rpde/events`) for a true same-universe intensity lens.
- **Status:** reframed; supervisor sign-off pending (with D-009/D-010/D-011).

## D-015 · Phase-gate: WS2 frozen at the validated milestone (2026-07-03)
- **Decision:** the analytical core is frozen as validated (gap index + held-out
  validation + incremental validity). Permitted bounded extensions only: bootstrap CIs,
  a second *distinct* held-out outcome, Active Places corroboration when acquired,
  conditional E2SFCA. Effort pivots to the deployment layer (LO4) and the report (60%).
- **Rationale:** further WS2 deepening = low marginal marks + scope-creep risk (the
  exemplar's failure mode was polishing a strong component while the heavy one lagged).
- **Status:** PROPOSED (panel recommendation; operative in practice) — confirm with team
  and supervisor.

## D-016 · Metrics-manifest verification protocol (2026-07-03)
- **Decision:** every headline number lives as a row in **`results/metrics.csv`**
  (metric_id, value, **population**, unit, vintage, source, definition, script,
  results file, commit, timestamp, corroboration, verified-by). Scripts own metric-id
  prefixes and replace only their own rows. **No number enters a deliverable unless it
  traces to a manifest row.** Non-trivial statistics get dual-method verification.
- **Rationale:** the 41.6%/£4.80 episode — numbers circulating without population labels
  or provenance — was the project's demonstrated failure mode.
- **Status:** ADOPTED and implemented (`src/verify_open_sessions.py`,
  `src/verify_event_harvest.py`; 26 manifest rows, all dual-verified 2026-07-03).
  **Extended 2026-07-07:** WS2 inferential statistics now have manifest rows —
  `src/ws2_metrics.py` owns the `ws2.*` prefix (validation ρ/p/n, Fisher CI,
  **seeded bootstrap CI [0.112, 0.696]** (B=5,000, seed=config.RANDOM_SEED —
  the citable bootstrap; the unscripted audit figure [0.097, 0.705] is
  superseded and must not be cited), D-013 set, facilities corroboration with
  its p, weighting sensitivity, quadrant threshold stability per B2-3).

## D-017 · Process documentation follows supervisor guidance (2026-07-06)
- **Decision:** the repository and report carry **no AI-use statement**, per the
  supervisor's direct guidance at the team meeting of 6 July 2026: no such
  disclosure is required for this unit, and individual working practices are
  covered by each member's individual reflective account. This supersedes the
  4 July email exchange about commit-trailer handling (that question is now
  moot: development-tool commit trailers are absent from `main` in the normal
  course of the squash-merge workflow).
- **Housekeeping under the same guidance:** internal tooling working documents
  removed from the tracked tree as non-deliverables
  (`claude-project-instructions.md`, `prompt-playbook.md`); their substantive
  engineering content migrated to `docs/engineering-rules.md`.
- **Record:** supervisor guidance received verbally; written confirmation
  requested by email (filed with the team's meeting notes when received).

## D-018 · Active Places ingest rules (2026-07-07)
- **Context:** Sport England Active Places acquired 2026-07-07 (registered
  download; extract version 2026-07-07 03:30; closes WS1 examiner finding F3).
  Real headers/encodings differ from the pre-acquisition assumptions in
  `config.py`, which was adapted; three choices in that adaptation are
  methodological and are fixed here.
- **Decision 1 — operational-only counting.** `Operational Status` arrives as a
  numeric code; only **code 3 = Operational** counts as provision
  (`AP_OPERATIONAL_KEEP`). Decode verified by exact count-match (124,839 rows)
  against the text-labelled ArcGIS Hub export of the same vintage:
  1 Planned · 2 Under Construction · 3 Operational · 4 Temporarily Closed ·
  5 Closed · 7 No Grass Pitches Currently Marked Out · 8 Not Known. Excluded
  codes are ~21% of the national file; counting them would inflate provision.
  *Alternative rejected:* including 4 (temporarily closed, n=659 national) —
  not currently usable, and no reopen-date field to bound the closure.
- **Decision 2 — community use = 'Public Access'.** The assumed `CommunityUse`
  boolean does not exist; the export's `Accessibility Type Group (Text)` is
  {Public Access, Private, Not Known}. `pct_community_use` = share with
  **Public Access** (`AP_COMMUNITY_TRUE`). 'Not Known' counts as not-community
  (conservative; 100 rows nationally, immaterial).
- **Decision 3 — type decode + exact-safe needles.** `Facility Type` is coded;
  decoded via the lookup **shipped inside the extract** (`facilitytype.csv`),
  not a hand-maintained map. Needle changed 'Grass Pitch' → **'Grass Pitches'**:
  the singular substring also matches 'Artificial Grass Pitch' (a distinct
  type, ID 8) — hazard verified and now asserted in `tests/test_run.py`.
- **Verification:** borough assignment cross-checked by two independent routes —
  pipeline point-in-polygon vs the sites file's `Local Authority Code` — giving
  **identical** London results: 10,070 operational facilities · 3,553 sites ·
  grass 3,235 · halls 1,505 · health&fitness 1,160 · pools 534. Face validity:
  Bromley/Barnet/Hillingdon lead; City of London 96. Schema green (27 checks);
  synthetic fixtures now mirror the real coded shape incl. status decoys.
- **Caveat carried forward:** City of London `facilities_per_10k` (111.8) is a
  resident-denominator artefact — exclude from any standardisation exactly as
  its session rate is (D-012 practice). And per D-011, facilities remain a
  separate corroboration layer: never merged with sessions.

## D-019 · Event-layer snapshot succession (2026-07-07) — **PROPOSED, pending team + verification rework**
- **Proposal:** adopt Wesley's **2026-07-07 harvest** (`data/raw/dataset_2026-07-07.csv`,
  549,169 events, sha `7542ed60329c9c06`, `notebooks/load_dataset.ipynb`) as the
  canonical event layer, superseding `data/external/wesley/output.csv` (464,392
  events, harvest date **TBC** — the last open WS1 finding, F2, which this
  succession closes by replacement: the successor has full provenance).
- **Why:** known harvest date; structured adult/junior offers; richer schema;
  the audit's offer-parsing defect fixed at source. Same borough-robust /
  sub-borough-fragile shape (30/33 boroughs, 87.6% MSOA / 97.5% LSOA empty) —
  which **corroborates and does not re-open D-008** (different population:
  events, not the Open Sessions provision series).
- **Known defects carried, documented in the notebook:** harvest-time
  completeness filtering (retained-subset completeness only); no provider
  column → 128 cross-feed id collisions (next harvest: feed column + composite
  key); 2023-02→2027-04 window.
- **Adoption gate:** (1) team sign-off; (2) `verify_event_harvest.py`
  re-pointed at the new file with freshly derived dual-method expectations and
  regenerated `event_harvest.*` manifest rows (current rows describe the old
  file and stay labelled as such until then); (3) Fahmi four-eyes on the new
  numbers. Until all three: old file remains the cited artefact, new file is
  documented but not quoted in deliverables.
- **Attribution:** harvest & notebook Wesley; review, defect fixes (boundary
  column vintage, frozen-snapshot path, dual-denominator free share,
  events-vs-series labelling) and integration Michael.

## Correction record (2026-07-03) — superseded figures *(full detail: `docs/open_sessions_data_note.md`, `docs/event_harvest_audit.md`)*
| Old figure | Correct, labelled figure |
|---|---|
| "41.6% free" (implied London) | London **43.9%** (217/494); national 41.6% (659/1,585) |
| "£4.80 typical paid price" | London paid median **£10.00** (n=277); national £8.00 |
| "~254–264 venues" | **264** distinct London venue names (252 mapped positions) |
| "~1,605 national series" | **1,585** (2026-06-30 snapshot) |
| "527 venues" in London context | 527 = **UK**; London = **128** (event harvest) |
| "1.02% events free" | **2.30%** of price-known London events (44.5% price-known) |
| "Pearson −0.05" (orthogonality) | **−0.111** (Spearman −0.047) |
| Field-completeness block as London | national-scoped; London: price 100%, coords 100%, access-info 22.7%, capacity 1.4% |

## D-020 · Harvest-primary architecture (2026-07-14) — **PROPOSED**, pending two gates

- **Decision (proposed).** The OpenActive **event harvest** becomes the single PRIMARY
  dataset. Canonical vintage: `data/raw/dataset_2026-07-07.csv` (549,169 events,
  15-column schema — no `endDate`, ISO-8601 durations), adopted under D-019's gate;
  the predecessor June extraction (`data/external/wesley/output.csv`, harvest date
  unrecorded — open finding **F2**, register item 2.3) is retained as the exploratory
  evidence base, with every June-derived figure vintage-tagged. Every methodology,
  measure and product surface stems from the harvest; externals are confined to
  complementary roles (IoD2025 + Census 2021 = need inputs; Active Lives 2024/25 =
  the single held-out validator per D-012; Active Places = corroborant + separate
  accessibility display; Open Sessions = one pre-banded corroboration row; PTAL +
  ONS boundaries = context/backbone). All two-universe machinery is removed.
- **Pre-registration (binding before the point-in-polygon rebuild).** Endpoint
  selection after exploration is acknowledged: the run's product is a
  **frozen-specification estimate on corrected geometry**; the out-of-sample tier is
  cross-snapshot agreement (committed via the weekly cadence), with national
  LAD replication as gated stretch. Primary endpoint: Spearman
  ρ(harvest-native gap — the z-based (log1p) construction, covered-only — and
  Active Lives inactivity 2024/25, Fingertips extract retrieved 2026-07-01,
  exact table and version pinned at the freeze) > 0, with both variables
  rank-transformed, Clifford–Richardson effective *n* computed on the ranks
  over the covered-borough adjacency, and a Fisher-z CI at n_eff. The
  rank-percentile gap dual and the hours companion live in the specification
  curve only (no promotion rule; the headline venues measure is the sole
  endpoint input);
  pre-declared secondary: partial ρ(provision, inactivity | need) < 0; interpretation
  pre-committed for all four primary×secondary outcomes; falsification clause;
  three-tier coverage protocol defined on venues (threshold ratified with this entry) with a venue-based recovery rule; new-rows-only sensitivity;
  minimum detectable effect stated across the effective-n band (80% power:
  ρ ≈ 0.49 / 0.54 / 0.59 at n_eff 30 / 25 / 20; validator-side Moran's I =
  0.274 on the covered adjacency, `prereg.validator_morans_i_covered30`, so
  n_eff materially below 30 is expected and the falsification branch is live);
  pre-committed expectation: the middle cell — primary passes, secondary
  inconclusive — a modest validated targeting layer; specification-curve list
  enumerated at freeze.
- **Alternatives considered.** (i) *Open Sessions remains primary* (D-009 status
  quo) — rejected: 494 London series cannot carry the project's weight, and the
  brief names the national platform whose bulk the harvest carries. (ii) *Dual-feed
  split-role* (the unratified v4 draft: 494-series = catalogue, harvest = breadth
  layer) — rejected by team directive; two-universe machinery removed. (iii) *Hybrid
  retaining the validated session-layer analysis as evidential spine* — not chosen
  as headline (its −0.49 partial belongs to a demoted feed); retained only as a
  single pre-banded corroboration row.
- **Gates.** (1) Supervisor's written confirmation; (2) team ratification of this
  entry. **On ratification only:** D-009 gains a dated supersession pointer
  (annotated, never rewritten — the D-008 convention); CLAUDE.md's settled-decisions
  block is reconciled; the binding sequence engages (written confirmation →
  D-020 → reference verification, Clifford–Richardson first → pre-registration
  freeze → point-in-polygon rebuild → the single frozen-spec run).
- **Evidence base.** June-extraction exploratory statistics (`event_harvest.*`
  rows; vintage-tagged); snapshot verification rows `harvest0707.*` in
  `results/metrics.csv` (script `src/verify_snapshot_0707.py`, stated bbox
  51.28–51.70°N / −0.55–0.30°E). Prior-sight inventory: point-in-polygon
  event-density surfaces exist in `notebooks/load_dataset.ipynb` (192,032 London
  events, 30/33 boroughs); **never computed by anyone:** venue counts under
  point-in-polygon, the harvest-native gap, or any correlation with the validator —
  the pre-registered endpoint remains unseen.
- **Status: PROPOSED 2026-07-14.** No other document claims adoption.

## D-021 · Legacy event corpus retired; instrument-side branch opened on evidence (2026-07-15) — **PROPOSED**

- **Decision (proposed).** The legacy event corpus — `data/raw/dataset_2026-07-07.csv`
  (549,169 rows, 15 columns) and its predecessor `data/external/wesley/output.csv`
  (464,392 rows, 16 columns, harvest date unrecorded — open finding **F2**) — is
  **retired as the analysis corpus** and reclassified as **historical/motivating
  evidence only**. **Every diagnostic derived from it is suspended**: publication
  horizon, semantic duplication, price/capacity missingness, taxonomy coverage,
  venue counts, borough coverage, and the exploratory gap/validation figures. None
  may be cited in the report except as superseded history with this entry attached.

  - **SCOPE CORRECTION (2026-07-15).** This clause was initially actioned as if it
    affected only the `harvest0707.*` manifest prefix. **It does not.** Tracing every
    row in `results/metrics.csv` back to its `source_dataset` field, **31 of 72 rows**
    derive from a file this entry retires, across **four** prefixes:

    | Prefix | Rows | Retired source |
    |---|---|---|
    | `harvest0707.*` | 20 | `data/raw/dataset_2026-07-07.csv` |
    | `event_harvest.*` | 9 | `data/external/wesley/output.csv` |
    | `harvest0626.*` | 1 | `output.csv` |
    | `prereg.*` | 1 | `output.csv` |

    Naming only `harvest0707.*` would have left **11 rows live** that this entry
    suspends — including every `event_harvest.london33.*` figure. The suspension is
    **all 31 rows**. Reproduce with: trace `source_dataset` for each row against
    `dataset_2026-07-07.csv` / `output.csv`.
  - **Labelling is deferred until ratification, deliberately.** The manifest is the
    project's canonical evidence record, and this entry is **PROPOSED**. Mutating 31 rows
    of it to reflect an unratified decision would assert an outcome the team has not
    agreed. The status column lands **after** ratification, not before. Until then this
    entry is the register of what is suspended.

- **Why (verified 2026-07-15, not inferred).** Direct column inspection: **both files
  lack** `@id`, `superEvent`, `organizer`, activity/`category` vocabulary,
  publisher/feed identity, RPDE `modified`/`state`, and any retained raw JSON-LD.
  No raw was kept for this corpus (the only `session_series_raw_*.json` files belong
  to the separate, audited Open Sessions harvester). Consequently the corpus cannot
  distinguish an ecosystem defect from an extraction defect, and — because no raw
  was retained — **that ambiguity is not resolvable retrospectively**.

- **The evidence that settles it (`src/harvest_pilot.py`, 2026-07-15).** A direct,
  plain-HTTP read of the canonical catalogue → dataset sites → RPDE feeds, deliberately
  **not** using the `openactive` client (see F-DEP), found on a first sample of six
  LeisureCloud-platform publishers (7,624 items, 41 endpoints, all CC-BY 4.0):
  - **`category` present on 100% of `SessionSeries` parents at 6/6 publishers**;
    `offers` present as structured `Offer` objects (identifier/name/description/
    acceptedPaymentMethod) at 5/6 — **both absent from our CSV**, which retained only
    a flattened `adultPrice` number and no activity field at all.
  - **`superEvent` present on 100% of `ScheduledSession` children**; children carry
    *only* dates, capacity and the parent pointer. All descriptive fields live on the
    parent. Our extraction kept children and discarded the pointer.
  - `eventSchedule`, `attendeeInstructions`, RPDE `state` — published, and absent from
    our CSV.
  - Capacity: ~2,090 bytes/item raw → **~16.5 GB to retain all 7.9M items**; not a
    constraint.
  - A real publication defect was logged in passing: **Wigan's declared
    `ScheduledSession` feed returns HTTP 404**.
  - **Confound identified and corrected in the same session:** those six publishers all
    run on **one booking platform (LeisureCloud)**, because first-N sampling of a
    concatenated catalogue list is platform-biased. The pilot now **stratifies across
    all four catalogues**. **The stratified rates below supersede the figures above;
    the six-publisher figures must not be cited.**

- **Stratified evidence (supersedes the above; run 2026-07-15, 20 sites across all four
  catalogues, `attempted ÷ declared` = 20/173 = 11.6%, 77 endpoints, 12,890 items;
  `results/pilot_field_presence.csv`, `results/pilot_endpoint_log.csv`).**
  **Field availability is a property of the booking platform, not of the publisher** —
  near-deterministic between platforms, near-zero variance within them:

  | Platform (catalogue) | `category` on parents | `activity` (Activity List URI) |
  |---|---|---|
  | LeisureCloud (5 publishers) | **100%** (all five) | **0%** (all five) |
  | singular (Better; Bookwhen) | 0%; 53% | **100%** (both) |
  | Legend (BwD Leisure) | 0% | **100%** |
  | Bookteq (3 publishers) | 0% | 0% |

  - `superEvent` on `ScheduledSession`: **1,533/1,533 = 100.0%** — the primary ablation
    exists universally. (`Slot`: 0/4,106 — a different child type; the 27.2% all-kinds
    aggregate is a trap and the per-kind denominator is the honest one.)
  - Capacity: **~1,772 bytes/item → ~14.0 GB** to retain all 7.9M items raw.
  - **Endpoint failures: 8 of 77** — Wigan `ScheduledSession` HTTP 404; three Legend
    HTTP 500 (SessionSeries, FacilityUse, Slot); three HTTP 403 (Legend sites incl.
    Halo, Serco Leisure); one Bookteq site 404. ~~**Legend is the least reliable platform
    in this sample.**~~ **WITHDRAWN (D-029):** census2 showed **all five recovering sites were
    Legend 403s that cleared on retry** — that is **rate-limiting, i.e. a measurement of our own
    request pattern**, not Legend's reliability. Single-attempt endpoint logs cannot separate
    transient from structural failure; the persistent rate is **9/174 (5.2%)**, not 14/173
    (8.1%). Retry-and-classify is now a harvest requirement.
    The remaining failures are publication-process defects, logged with status.

- **CENSUS EVIDENCE — supersedes the 20-site stratified figures above (run 2026-07-15,
  `--per-catalogue 88 --pages 2 --tag census`; `results/census_field_presence.csv`,
  `results/census_endpoint_log.csv`).** Full coverage of the declared frame:
  **`attempted ÷ declared` = 173/173 = 100.0%**, 4 catalogues, **124 distinct publishers**,
  969 endpoints, **217,743 items**, 6,622 field-presence rows.

  - **The primary ablation is confirmed at scale.** `superEvent` on `ScheduledSession`:
    **18,935/18,935 = 100.0%** — a 12× larger denominator than the pilot's 1,533, still
    exactly universal. (`Slot`: **0/92,359 = 0.0%**. The 17.0% all-kinds aggregate is the
    same trap as the pilot's 27.2%; **the per-kind denominator is the only honest one.**)
  - Join integrity: **15,512/18,935 = 81.9%** of sampled `superEvent` targets resolve to a
    parent harvested on the same pages (page-1/2 alignment is not guaranteed, so this is a
    floor, not a rate).
  - **Capacity revised DOWN: 1,329 bytes/item → ~10.5 GB** to retain all 7.9M items raw
    (pilot estimated ~14.0 GB from a smaller, session-heavier sample). Not a constraint.
  - **Endpoint failures: 52 of 969 = 5.4%** — 30× HTTP 403, 13× HTTP 500, 7× HTTP 404,
    1 timeout, 1 dataset site serving no parseable JSON-LD. **14 of 173 declared sites
    (8.1%) could not be read at all.** A declared-but-unreadable site is a publication
    defect and must never silently become "zero opportunities".

- **AMENDMENT — the headline claim above is TOO STRONG and is corrected here.**
  The pilot's framing, *"field availability is a property of the booking platform, not of
  the publisher"*, does not survive the census in that form. **Field availability is a
  property of `platform × feed kind`.** Three corrections, all material:

  1. **Bookteq was mischaracterised.** Its **79 publishers serve `FacilityUse`/`Slot`
     only — no session feeds at all.** The pilot's "Bookteq publishes neither `category`
     nor `activity`" was not publisher negligence and not even a platform vocabulary
     choice: `category` and `activity` are **session** concepts, and Bookteq is a
     **facility-booking** platform. Reading that as a data-quality defect was an error of
     denominator, and it would have produced a repair recommendation aimed at a
     non-existent problem.
  2. **`offers` inverts between the two models.** For sessions it sits on the
     `SessionSeries` **parent**; for facilities it sits on the **`Slot` child** —
     **77/77 Bookteq, 25/25 LeisureCloud, 2/2 Legend, 1/1 singular: unanimous.** The same
     field has an opposite structural home depending on the model. Any consumer that
     assumes "descriptive fields live on the parent" silently loses all facility pricing.
  3. **Per-kind, the platform signal is strong but not total.** On `SessionSeries`
     (publishers with the field present / publishers serving the kind):

     | Platform | `category` | `activity` | `offers` | `organizer` | `location` |
     |---|---|---|---|---|---|
     | LeisureCloud | **28/28** | **0/28** | 27/28 | 25/28 | 28/28 |
     | singular | 2/6 | **6/6** | 5/6 | 6/6 | 6/6 |
     | Legend | **0/3** | **0/3** | 3/3 | 3/3 | 0/3 |
     | Bookteq | *serves no session feeds* | — | — | — | — |

     **The pilot's core dichotomy holds and strengthens**: LeisureCloud is `category`
     28/28 and `activity` **0/28** (pilot: 5/5 and 0/5); singular is `activity` 6/6.
     A publisher's `category`/`activity` vocabulary is fully predicted by its platform on
     LeisureCloud and Legend. But `offers` and `organizer` **split within** LeisureCloud
     (27/28, 25/28), and `category` splits within singular (2/6) — so the platform sets
     what is **possible**, and publisher behaviour still varies inside that envelope.
     Legend's `activity` is **8/8 on `FacilityUse` but 0/3 on `SessionSeries`** — the
     clearest single proof that platform alone is not the unit of explanation.

  **Corrected framing (supersedes the "Consequence" paragraph below):** *the booking
  platform determines which fields a publisher **can** expose for a **given feed kind**,
  and that ceiling — not publisher diligence — is the first-order determinant of which
  discovery questions are answerable where. Within the ceiling, publisher variation is
  real and second-order.* This is weaker than the pilot's claim and better evidenced.
  The four-vocabulary-regimes finding survives **for session feeds**; it must not be
  asserted across feed kinds.

- **Consequence — the branch this opens, and it is not the binary first assumed.**
  *(Written on the pilot evidence; read subject to the AMENDMENT above, which narrows
  claim 2 from "platform" to "platform × feed kind" and withdraws the Bookteq example.)*
  The stratified evidence shows **both** mechanisms operating, and they compose:
  1. **Instrument-side (confirmed).** Our extraction discarded `category`, `superEvent`
     and structured `offers` **where the platform published them on every record**
     (LeisureCloud). For that platform the "missingness" was self-inflicted.
  2. **Publication-side (confirmed, and this is the stronger finding).** The ecosystem
     is **not one vocabulary regime but four**. A consumer joining these feeds receives
     `category` from one platform, Activity List URIs from another, and neither from a
     third — so **any cross-platform activity analysis compares incommensurable fields**.
     The deployed Intelligence Platform reports "785 activities" across exactly this
     heterogeneity.
  The defensible framing is therefore neither "publishers are negligent" nor "our
  pipeline was bad", but: **field availability in OpenActive is determined by
  booking-platform software, and that determines which discovery questions can be
  answered where.** This is mechanistically explanatory, evidenced, brief-aligned, and
  not occupied by any incumbent tool. The title, aim and RQ framing change accordingly;
  pre-declared here rather than discovered later.
  - **Specifically retired:** the taxonomy contribution's motivation. The "free-text
    naming chaos" (5,636 London clusters; 86.1% top-100 dictionary coverage;
    "standardisation degrading as the feed grows") was measured on a projection that
    **discarded a `category` field LeisureCloud publishes on every record**. The
    coverage figures stand as arithmetic; their interpretation does not.
  - **Not retired — reframed and strengthened:** the vocabulary question is real, and
    it is a *platform* question. `activity` (the controlled Activity List URI) is
    published by singular and Legend at 100% and by LeisureCloud and Bookteq at 0%;
    `category` is the mirror image. Whether that dichotomy holds beyond 11 publishers
    is the first thing the full harvest must measure.

- **Alternatives considered.** (i) *Repair the legacy corpus retrospectively* —
  impossible: RPDE is a change feed; the 7 July parent state is unrecoverable and no
  raw was kept. (ii) *Proceed on the legacy corpus with caveats* — rejected: every
  headline would be uninterpretable between two causes. (iii) *Re-harvest* — adopted;
  a fresh, raw-retaining, paired-feed observation vintage is now **Deliverable 1**.

- **Consequences for the plan.** The frozen observation date **moves** (the new vintage
  is the analysis corpus; 7 July becomes history). The primary ablation
  (child-only vs parent-resolved) must draw **both arms from the same new vintage**.
  Wesley's harvest design changes: paired feeds, raw JSON-LD retained, per-endpoint
  status, `attempted ÷ declared` at catalogue/site/feed level, platform stratification.
  D-019's snapshot-succession question is **moot** for analysis (both candidate
  snapshots are retired) but F2 remains open for citing the legacy figures as history.

- **F-DEP (new finding, logged here).** The `openactive` PyPI client produced the entire
  legacy corpus (`notebooks/load_dataset.ipynb` does `import openactive`) but is
  **declared in neither `requirements.txt` nor `environment.yml`** and is not installed
  in the shared environment. The corpus is therefore not rebuildable by anyone cloning
  this repository. The client also self-describes as *"experimental"* and advises against
  use *"for critical pipelines"*. Any future use must be pinned, declared, and its
  join/delete/pagination behaviour independently verified against the raw feeds.

  - **F-DEP RE-EXAMINED (2026-07-15) — it is worse than stated above, and that CLOSES it
    rather than opening work.** Verified directly:

    | Layer | Result |
    |---|---|
    | `openactive` in `requirements.txt`? | **No** (13 lines; verified line-by-line, not by substring — `name: ls-openactive` in `environment.yml` is a false-positive trap) |
    | `openactive` in `environment.yml`? | **No** |
    | Installed in the environment? | **No** — `import openactive` raises `ModuleNotFoundError` |
    | `notebooks/load_dataset.ipynb` committed? | **NO — never, on any branch.** `git log --all -- notebooks/load_dataset.ipynb` is empty; the file is untracked. Only `notebooks/data_audit.ipynb` is tracked. |

    So the original statement — "undeclared, therefore unrebuildable" — **understates it**.
    **The corpus-building code is not in the repository at all.** Even a correctly pinned
    dependency would not make the corpus rebuildable, because there is nothing to run.
    The legacy corpus is **permanently unrebuildable by three independent failures**.

  - **Consequence: F-DEP is not an open task. It is evidence FOR D-021.** This entry retires
    the corpus; F-DEP explains why retirement is the only available option rather than a
    preference — the corpus cannot be reconstructed, audited, or defended by anyone but its
    original author, and no raw was retained to check it against. **No action is required and
    none should be taken:** there is **no forward dependency** on `openactive`
    (`src/harvest_pilot.py` and `src/verify_licences.py` use plain HTTP; their only
    third-party import is `requests`, which **is** declared).

  - **Correction to a claim made against this project (K6).** `docs/v7-one-pager.md` reported
    kill rule **K6** (*"a non-author cannot reproduce the headline table/figure from a clean
    clone"*) as **firing**, on F-DEP's authority. **That was wrong and is withdrawn.** K6
    tests the *current* headline, not the retired corpus. Every current headline figure comes
    from `harvest_pilot.py` / `verify_licences.py` → `results/census_*.csv`,
    `results/licence_audit.csv`, whose sole third-party dependency is declared. **A clean
    clone reproduces the current evidence chain; K6 does not fire.** The error was conflating
    two different reproducibility questions — the dead corpus and the live evidence.

- **Status: PROPOSED 2026-07-15.** Supersedes nothing yet; D-020 remains PROPOSED and
  its corpus premise is amended by this entry. No document may claim adoption.

---

## D-022 · Brief provenance established; no further partner elicitation (2026-07-15) — **PROPOSED**

- **Decision (proposed).** The London Sport 1 requirement set is **fixed and enumerable**,
  and consists of exactly two primary artefacts. All alignment claims must cite them
  directly. `docs/brief-traceability.md` is the mapping of record.

- **The primary sources (verified 2026-07-15 by direct extraction, not transcription).**
  - **P1 —** `LS machine learning projects_29-05-2026.pdf`, pp.16–19 (brief) and pp.22–24
    (output framework). London Sport's own "Let's Move London" deck. Verified
    partner-authored: PDF metadata `author: Josef Baines` — named in this project's records
    as **J. Baines, Insight Manager, London Sport** — `creator: Microsoft PowerPoint for
    Microsoft 365`, `creationDate: 2026-06-03`, 25 pages, real embedded text layer.
  - **P2 —** the numbered challenge listing headed **"1. London Sport 1"**, read directly
    as an image. **Sole source of the label "London Sport 1"; the deck never uses it.**
  - **P1 and P2 are NOT interchangeable.** They differ in wording (e.g. P1 p.18 "New
    solutions **required to** improve…" vs P2 "the system **requires** new solutions
    **that** improve…"). Every quotation must name which one it quotes.

- **Why this entry exists.** Until today the project's alignment rested on an **AI
  paraphrase** — `CODEX_FINAL_ADVERSARIAL_HANDOFF.md` §2.1, headed *"Brief as supplied in
  the conversation"*. Prior text searches missed P1 because the deck renders the brief as
  slide bullets while searches used the listing's prose, so **absence of grep hits was
  mistaken for absence of the artefact**. Recorded as a method lesson: a failed search
  licenses no conclusion about existence.

- **Finding — the partner is misquoted inside quotation marks.** P1 p.19 and P2 both read
  "…recommendations tailored **specifically** to London's diverse communities."
  `Closing_the_Activity_Gap_Project_Proposal.pdf` p.1 and `Updatedprojectproposal.pdf` p.3
  render it, **within quote marks**, as "tailored to London's diverse communities". The
  dropped word is the one that makes targeting — and therefore the equity lens — a
  requirement. **Fix required in every proposal artefact before submission.**

- **Constraint of record: no further partner elicitation is available.** P1 and P2 are the
  complete statement of requirements. There will be no clarification of ambiguous clauses,
  no scope negotiation, and no acceptance criteria beyond the brief's own words.
  **Consequences:** (1) every ambiguity is closed by *documented interpretation*, marked
  **[INTERPRETATION]** in `docs/brief-traceability.md`, and defended in the report — never
  by assumption presented as fact; (2) "the partner didn't specify" is **not available** as
  a defence for an unmet clause, because the clauses are fixed and enumerated; (3) the
  traceability matrix is the **alignment ceiling** — quote, interpret, deliver, evidence,
  limit — and is fully within the team's control.
  > **UNVERIFIED — team must supply before ratification.** The *reason* elicitation is
  > unavailable (unit rule / partner availability / team decision) and its *date* are not
  > recorded anywhere. This entry asserts the constraint as stated by the team. **Do not
  > ratify this bullet until the reason and date are written down.**

- **Open risk, and a correction to the obvious fix.** Neither primary is in this repository.
  The obvious remedy — commit them — is **wrong and must not be done**: **this repository is
  PUBLIC and has no licence file**, so committing P1 would **republish London Sport's
  unpublished internal deck, authored by a named employee, to the open internet** without
  their permission. No confidentiality marking appears on it, but absence of a marking is
  not a licence; copyright subsists automatically. **Decision: do not commit P1 or P2.**
  Quoting clauses for academic criticism is a different, defensible act; republishing the
  artefact is not.

- **Substitute adopted — identity by digest, not by distribution.** `docs/brief-traceability.md`
  §0.1 records SHA-256 digests, byte sizes and metadata for both primaries, so any member
  holding the deck can prove they hold the **same** artefact the quotations came from and
  check every row, without anything being published:
  - **P1** `5afccb820391fc4dad999e4fdc0cc04f31da49efd11410a942603a4d0959bb9f` (1,992,626 bytes,
    25 pp, `author: Josef Baines`, created 2026-06-03).
  - **P2** `8bc9b29747c95ca4fc1f1d6042ac476c9108ab901151933760d2ac4969dd6707` (580,032 bytes).
  A digest mismatch means a different artefact and the quotations must not be relied upon.

- **Residual gap — recorded, not closed.** Members who do **not** hold the deck still cannot
  verify a quotation, so this remains a partial failure against output type **O8**
  ("Instructions needed to reproduce the analysis"). **Team to decide:** (a) ask London Sport
  whether the deck may be committed or whether a citable public reference exists, and/or
  (b) circulate P1 by the team's own private channel — **not** this repo.

- **Status: PROPOSED 2026-07-15.**

---

## D-023 · Answerability pivot — rejected alternatives and thresholds (2026-07-15) — **PROPOSED**

- **Decision (proposed).** Reframe the project's central question from *"where is provision
  unequal?"* to *"which discovery questions are answerable, where, and why not?"* Read
  against P1, this is not a departure from the brief: the output framework (P1 p.22) names
  **"DATA QUALITY AND SUITABILITY ASSESSMENT"** as an output type under
  **"SUGGESTED OUTPUTS"** — *suggested*, **not** required (see the correction at D-026) — itemising
  "Completeness of the data", "Missing or inconsistent fields", "Issues with data
  granularity", "Any assumptions made", "Limitations in using the data for modelling or
  forecasting", and "Areas where findings should be treated with caution". **D-021 is that
  output.** **[INTERPRETATION]** — this is the team's reading of O3's scope, not a partner
  statement of intent.

- **What forced it (evidence, not preference).** D-021: the legacy corpus discarded the
  fields the analysis needed, and the census established that the ecosystem publishes them
  — 173/173 declared sites, 124 publishers, `superEvent` 18,935/18,935 = 100.0% on
  `ScheduledSession`. The original question was **unanswerable with the instrument in hand**,
  and the instrument's defects were themselves the more interesting finding.

- **Alternatives considered and rejected** (required by P1 p.22, output type
  **"METHODOLOGY EXPLANATION" → "What alternatives were considered"**):

  | Alternative | Rejected because |
  |---|---|
  | **Continue the equity-of-provision study on the 7-07 corpus** | The corpus cannot distinguish ecosystem defect from extraction defect, and no raw was retained, so the ambiguity is unresolvable retrospectively (D-021). Any finding would be uninterpretable. |
  | **Re-harvest and resume the original equity study unchanged** | Possible, but the deployed OpenActive Data Intelligence Platform (verified live 14–15 Jul 2026: 7.9M opportunities, 175 publishers, 74% of LAs, ODI-stewarded, daily refresh) already provides borough choropleths and per-publisher quality reporting. A borough per-capita/deprivation dashboard is **occupied**, so it is not a defensible novelty claim. |
  | **Build another activity finder / recommender** | London Sport already operates **Get Active** (an OpenActive-powered finder) and **Open Sessions** (a publishing product). Occupied. |
  | **Generic publisher quality scorecard** | Occupied by the deployed DIP's per-publisher data-quality section, which already separates core-detail completeness from extra-detail content quality. |
  | **Taxonomy / free-text naming standardisation** | Motivation retired by D-021: the "naming chaos" was measured on a projection that had discarded a `category` field LeisureCloud publishes on 28/28 `SessionSeries` publishers. The coverage arithmetic stands; its interpretation does not. |
  | **Equity re-ranker (α·relevance + (1−α)·equity)** | No interaction ground truth exists, so no accuracy claim is possible and the α-sweep evaluates nothing external. Retired in favour of the three-state demonstrator, whose outcomes (false suppression / false assurance) are measurable against an adjudicated sample. |
  | **Keep both the equity study and the answerability study ("two universes")** | Overruled by team direction: one primary dataset (OpenActive), one architecture. Splitting the evidence base halves the depth available to each within a 60-credit envelope. |

- **Thresholds and their rationale.** Recorded to satisfy P1 p.22 ("Any assumptions made"):
  - **Per-kind denominators are mandatory.** Any field-presence or prevalence rate must be
    reported per `kind`, never pooled. Rationale: two pooling errors have already produced
    false headlines — `superEvent` at 17.0% all-kinds vs the true 100.0% on
    `ScheduledSession` / 0.0% on `Slot`; and pooling `FacilityUse` with `SessionSeries`
    parents, which made Bookteq's **facility-only** catalogue (79 publishers, no session
    feeds) look like a publisher quality defect. **Both were caught internally and are
    recorded rather than hidden.**
  - **A field counts as "available" for a publisher at `presence_rate > 0`** on a parent
    feed of the relevant kind. Rationale: this is a *capability* test (does the platform
    ever expose this field for this publisher?), deliberately generous, because the claim
    being tested is about **ceilings**, not diligence. A stricter threshold would conflate
    capability with completeness.
  - **`attempted ÷ declared` must be reported at catalogue, site and feed level.** "100% of
    the feeds we tried" is not coverage. The census reports **173/173 = 100.0% of declared**
    — which is *not* 100% of existing: publishers outside the four catalogues are invisible
    by construction.
  - **Failed reads never become zeroes.** 52/969 endpoints (5.4%) and 14/173 sites (8.1%)
    failed; each carries a status.
  > **UNVERIFIED / to establish.** The thresholds for the three-state demonstrator — what
  > counts as a *determinate match* vs *indeterminate candidate*, and the adjudication rule
  > for the sample — are **not yet set** and must be pre-registered **before** the corpus is
  > examined for them, or the result is unfalsifiable. Do not ratify this bullet as complete.

- **Status: PROPOSED 2026-07-15.** Depends on D-021 and D-022. If D-021 is rejected, this
  entry falls with it.

---

## D-024 · Licensing, attribution and the public-repository correction (2026-07-15) — **PROPOSED**

- **Trigger — three live defects found together, all consequences of one unnoticed fact.**
  **The repository is PUBLIC** (`gh repo view` → `visibility: PUBLIC`), and had been
  throughout. It was not treated as such:
  1. **No `LICENSE`, no `NOTICE`, no attribution anywhere**, while publishing derivatives of
     CC-BY 4.0 OpenActive feeds (`results/census_*.csv`, `reports/*.csv`) to the open
     internet. **CC-BY 4.0 permits redistribution only with attribution**, so the
     redistribution was unlicensed. `docs/data-sources.md` line 3 already stated the
     obligation — *"Every published output must carry CC-BY 4.0 attribution … and OGL v3.0
     acknowledgement"* — so this was a known rule, unmet.
  2. **The README asserted the opposite of the truth.** A badge read
     *"access: private & confidential"* and a `## Confidentiality` section read *"This is a
     private academic project repository… Please do not share repository contents outside the
     project team"*. Both **false**. Internal decision logs, team notes naming individuals,
     and verbatim quotation of the partner's unpublished deck were world-readable while the
     README said they were not.
  3. **"All CC-BY 4.0" was asserted with no artefact behind it** (D-021, PR #6).
     `src/harvest_pilot.py` reads each dataset site's `license` in `site_feeds()` and
     **discards it** — no licence column exists in any endpoint log. A claim in a decision
     entry was untraceable, contrary to this project's traceability rule.

- **Decision (proposed).**
  1. **Remain public**, and correct the README to say so. *(Team decision, 2026-07-15.)*
  2. **Code (`src/`, `tests/`, config): MIT.** **Docs and analytical outputs (`docs/`,
     `results/`, `reports/`): CC-BY-4.0.**
  3. **Add `ATTRIBUTION.md`** carrying every upstream acknowledgement in its required form,
     and link it from the README. These are **licence conditions, not courtesies**.
  4. **Never commit the partner's brief (P1/P2)** — see D-022. Verification is by SHA-256
     digest, not distribution.

- **Why this split, and what was rejected** (P1 p.22 requires "What alternatives were considered"):

  | Option | Verdict |
  |---|---|
  | **MIT (code) + CC-BY-4.0 (docs/results)** | **CHOSEN.** Two different kinds of work get their natural licence. MIT means **London Sport — a not-for-profit — can use, embed and modify the code with no legal review**, which is exactly what brief output **O8** ("Reproducible handover material… Instructions needed to reproduce the analysis") is for. CC-BY-4.0 on prose and results **matches the upstream OpenActive licence**, so derivatives return to the ecosystem on the ecosystem's own terms and the team is attributed. |
  | Apache-2.0 | Rejected. Its patent grant and contribution terms are irrelevant to a 60-credit student analytics project and add legal-review burden for a small charity — friction against O8 with no compensating benefit. |
  | MIT for everything | Rejected. MIT is a software licence; applying it to prose and datasets is a category error and would not match the CC-BY-4.0 ecosystem the outputs derive from. |
  | CC-BY-4.0 for everything | Rejected. CC licences are **not recommended for source code** (Creative Commons' own guidance); it would leave the code's reuse terms ambiguous, defeating O8. |
  | No licence (status quo) | Rejected. Defaults to **all rights reserved** — so London Sport could not lawfully reuse the deliverable they commissioned, and the CC-BY redistribution stays unlicensed. This is the current state and it is a defect. |
  | Make the repo private instead | **Considered and rejected by the team, 2026-07-15.** It would have dissolved the CC-BY redistribution obligation and the exposure of internal notes. The team chose public; the obligations are therefore **live and must be met**, not deferred. |

- **Evidence — the CC-BY claim is now measured (`src/verify_licences.py` → `results/licence_audit.csv`).**
  Walking the canonical collection and reading the `license` each dataset site declares:
  - **162/162 readable sites declare `https://creativecommons.org/licenses/by/4.0/` = 100.0%, unanimous.**
  - **11 of 173 declared sites were unreadable**; their licences are **unknown, not assumed**,
    and no data from them is redistributed.
  - **Precision correction:** the honest claim is *"all readable sites"* (162/162), **not**
    "all 173". D-021 and PR #6 said "all CC-BY 4.0" without that denominator.
  - This **discharges the open ask** at `docs/data-sources.md` — *"verify per-feed licences
    before publishing derived outputs"*.

- **Verified upstream licences (from `docs/data-sources.md`; not assumed here).** OpenActive /
  Open Sessions **CC-BY 4.0** · IoD2025, ONS Census 2021, ONS boundaries, Active Lives
  **OGL v3.0** · TfL PTAL 2015 **OGL v2** *(v2, not v3)* · Active Places **Sport England's own
  licence**, requiring the verbatim acknowledgement *"Contains data Copyright Sport England"*
  — **not OGL**, a distinction `docs/data-sources.md` records the pre-acquisition runbook
  having got wrong.

- **Open — team must resolve before submission.** `LICENSE` names the copyright holders as
  *"Clarence, Fahmi, Michael Samuel, Wesley"*: `docs/team.md` records **only first names** for
  three of four. **Full legal names are required and must not be invented.** Marked TODO in
  the file.

- **Status: PROPOSED 2026-07-15.** The visibility correction and attribution are **compliance,
  not preference** — if the repo stays public they are required regardless of ratification.
  The licence *choice* (MIT + CC-BY-4.0) is the part open to team amendment.

---

## D-025 · Check 2 PASSED — instrument-side loss and publication-side absence separated and quantified (2026-07-15) — **PROPOSED**

- **What this settles.** D-021 retired the legacy corpus because it **could not distinguish an
  ecosystem defect from an extraction defect**, and — no raw retained — never would. The
  census retained raw, so the distinction is now **decidable per record, per field**. This is
  the blueprint's **Check 2 (field lineage)**, and it passes. It is also the evidential core
  of the whole pivot: the instrument/publication decomposition stops being an argument and
  becomes a measurement.

- **Method (`src/trace_lineage.py`, ruff clean).** For every captured `ScheduledSession`
  child, resolve `superEvent` to the `SessionSeries` parent captured in the same snapshot,
  then classify each field: **ON_CHILD** · **INHERITABLE** (absent on child, present on
  parent → *a child-only extraction destroys it — **instrument-side***) · **SOURCE_ABSENT**
  (absent on both → *the ecosystem does not publish it — **publication-side***) ·
  **UNRESOLVED** (parent not in snapshot → **nothing concluded**).

- **Scale.** 21,152 parents indexed · 18,213 children traced · **14,790 resolved = 81.2%**.

  > ⚠️ **DENOMINATOR CAVEAT (D-026).** These counts are computed over the **raw archive on
  > disk (708 files)**, which the filename-collision defect left **44 pages short** of the 752
  > actually fetched. That is why this entry says **18,213** children where D-021's census
  > says **18,935**: the missing **722** children are on the overwritten pages. **The rates
  > below are therefore measured on an incomplete archive** and must be recomputed after the
  > re-harvest with the fixed code. The *structural* findings are unlikely to move — but they
  > are not yet measured on the full retained record, and this entry must not be cited as if
  > they were.

- **RPDE tombstones are real and material (bearing on Check 3).** The archive carries
  **8,372 `state: deleted` tombstones** beside 18,213 `updated` items — **31.5% of all
  `ScheduledSession` items are deletions**. Current-state reconstruction is therefore not a
  formality: a consumer that ignores tombstones over-counts sessions by roughly a third on
  this sample. This also **confirms the `n_items` defect** (D-026 item 3): `n_items` counted
  all 26,585 items while `presence_rate` was computed over the 18,213 payloads.
  All rates below are over **resolved children only** — the honest denominator. **UNRESOLVED
  is never folded into absence**; it is a property of *our snapshot* (2 RPDE pages/feed, and
  parent/child pages are not aligned), not of the ecosystem. Folding it in would manufacture
  precisely the false missingness that retired the legacy corpus.

- **INSTRUMENT-SIDE — fields a child-only extraction destroys, that the ecosystem publishes:**

  | Field | Inheritable | Rate |
  |---|---|---|
  | `location` | 14,790/14,790 | **100.0%** |
  | `name` | 14,788/14,790 | **100.0%** |
  | `eventSchedule` | 14,759/14,790 | 99.8% |
  | `category` | 14,345/14,790 | 97.0% |
  | `url` | 12,872/14,790 | 87.0% |
  | `offers` | 11,915/14,790 | 80.6% |
  | `attendeeInstructions` | 10,105/14,790 | 68.3% |
  | `organizer` | 7,852/14,790 | 53.1% |
  | `genderRestriction` | 7,716/14,790 | 52.2% |

  **`location` is 100.0% inheritable with 0 source-absent.** Not one child carries the
  standard `location` field; every one is on the parent.

  > ⚠️ **CORRECTION (D-026, second pass).** An earlier version of this bullet continued:
  > *"A child-only pipeline loses **all** geography."* **That is false, and this entry
  > refuted it four bullets below its own claim:** 97.0% of children carry
  > **`beta:sportsActivityLocation`**, and the legacy CSV's `venue`/`latitude`/`longitude`
  > came from exactly that. A child-only pipeline loses the **standard** `location` field;
  > it does **not** lose geography. **This was the "assume instrument-side loss is the
  > answer" error** — presupposing the instrument story instead of attributing it, which the
  > answerability-pivot draft explicitly rejects as an alternative. The honest claim: geography
  > survives child-only extraction **only via a `beta:`-namespaced, explicitly provisional
  > field**, which is a fragility finding, not an absence finding.

- **PUBLICATION-SIDE — fields the ecosystem genuinely does not publish here:**

  | Field | Source-absent | Rate |
  |---|---|---|
  | `level` | 14,790/14,790 | **100.0%** |
  | `ageRange` | 14,644/14,790 | 99.0% |
  | `description` | 14,353/14,790 | 97.0% |
  | `activity` | 14,345/14,790 | 97.0% |

  **`level` is absent on every single resolved record — 14,790/14,790.** No better pipeline
  recovers it. A searcher asking *"is this suitable for a beginner?"* is **unanswerable in
  100% of cases**, and `ageRange` nearly so at 99.0%. These are not data-quality defects to
  be repaired; they are **hard limits on which discovery questions can be asked at all**, and
  they are the direct empirical warrant for the three-state design: *indeterminate* is the
  only honest verdict, and both a closed-world filter (false suppression) and a permissive one
  (false assurance) would lie.

- **Both mechanisms are real, and now quantified rather than asserted.** `category` is 97.0%
  **instrument-side** while `activity` is 97.0% **publication-side** — near-perfect
  complements, exactly as the census's platform×kind finding predicts (LeisureCloud dominates
  the sample and publishes `category`, not `activity`). The corrected D-021 framing survives
  an independent test at record level.

- **New finding — the legacy corpus's geography came from a `beta:` field.** The legacy CSV
  carried `venue`/`latitude`/`longitude` despite `location` being 0% on children. The route
  was **`beta:sportsActivityLocation`, present on 14,345/14,790 = 97.0% of children** — a
  **beta-namespaced, explicitly provisional** field. The retired corpus's only geography, on
  which every borough assignment and the entire gap index rested, depended on a field the
  specification marks as unstable. **This is independent of, and additional to, the reasons in
  D-021**, and strengthens rather than softens the retirement.

- **Reproducibility (the blueprint's actual pass condition).** Check 2 passes *"only when
  extraction loss is separated from source absence **and a second team member can reproduce
  every sampled trace**"*. The first is done. For the second, `results/lineage_sample.csv`
  emits **50 individual traces** (child `@id`, parent `@id`, fields on each, and the
  inheritable/source-absent verdict), each hand-checkable against `data/raw/census_*/` **with
  no code**. **The second half of this gate is not ours to close — a teammate must actually do
  it.** Until then Check 2 is **PASSED-PENDING-REPRODUCTION**, not passed.

- **Verification.** Every figure above was recomputed by a second, independent traversal of
  the raw pages and matched exactly (`location` 0/14,790/0 · `level` 0/0/14,790 · `category`
  0/14,345/445 · `activity` 0/445/14,345).

- **Status: PROPOSED 2026-07-15.** Gate status: **Check 1 PASSED · Check 2
  PASSED-PENDING-REPRODUCTION · Check 3 NOT STARTED** (no `state: deleted` handling exists;
  current-state reconstruction is unbuilt).

---

## D-026 · Adversarial audit — six defects found in today's own work, corrected here (2026-07-15) — **PROPOSED**

- **Why this entry exists.** An adversarial audit was run against everything produced on
  2026-07-15, explicitly tasked to attack this project's own reasoning. It found **six real
  defects**, every one verified independently before correction. They are recorded here in
  full rather than quietly fixed, because the pattern matters more than any single item:
  **the honesty was real but unevenly applied, and it thinned at exactly the points where the
  project's reputation was at stake.**

- **1. THE BRIEF WAS MISQUOTED — "required" is not the partner's word.** ❗
  - **Verified against P1:** p.19 reads "**Required outputs:**" and lists **five** — none about
    data quality. pp.22–24 are headed "**OUTPUT FRAMEWORK**", columns "**OUTPUT TYPE /
    SUGGESTED OUTPUTS**". The word *required* appears **nowhere** on pp.22–24.
  - **The error:** D-023, D-024, `docs/v7-one-pager.md` and `docs/brief-traceability.md` all
    called the nine output types **"required"**, and built on it the claim that *"the pivot is
    the brief's own required output"*. **O3 is SUGGESTED, not required.**
  - **Why it is serious, not a typo.** The word is load-bearing twice — for the pivot's
    central alignment argument and for D-024's licensing rationale — and it was inserted **in
    the self-serving direction**, by the very document (`brief-traceability.md` §0.2) that
    convicts the project's proposals of dropping "specifically" from partner text. **The same
    offence, committed while prosecuting it.**
  - **Corrected** in all four locations to "suggested". **The pivot's real defence does not
    need the inflation**: it was forced by instrument failure, it is honestly evidenced, and it
    maps closely onto O3's *suggested* contents. That argument stands on its own.

- **2. A FALSE LICENCE CLAIM, IN THE PUBLIC REPO.** ❗
  `ATTRIBUTION.md` §2.1 asserted *"No data from unreadable sites is redistributed here."*
  **False, and falsified by an artefact in the same commit (b584451):** publisher **`Halo`**
  returned **HTTP 403** on its dataset site — licence unknown — yet contributes **14 derived
  rows** to `results/census_field_presence.csv`, published publicly. Cause:
  `verify_licences.py` reads the *dataset site*; `harvest_pilot.py` reads the *feed
  endpoints*; a site can 403 on one and serve on the other. **This was the single assertion in
  that file with external legal consequence, in the document written to fix exactly this
  defect.** Corrected to disclose it; **resolution deferred to the team** (drop the rows /
  re-read the site / use the RPDE envelope's own `license`).

- **3. THE HEADLINE FIGURES WERE NOT TRACEABLE (K6 fires after all).** ❗
  `217,743 items`, `18,935/18,935`, `0/92,359`, `17.0%`, `1,329 bytes/item`, `~10.5 GB` exist
  in **no committed artefact** — they were printed to stdout, and `*.log` is gitignored
  (`.gitignore:23`), so no run log was kept. Worse, they are **not derivable** from the CSVs
  cited as their source: summing `n_items` over the `ScheduledSession`/`superEvent` rows gives
  **27,484, not 18,935**. Cause (benign, now fixed): `harvest_pilot.py` wrote
  `n_items = len(items)` — **including RPDE tombstones** — beside a `presence_rate` computed
  over `len(payloads)`. **An examiner reconciling the project's strongest number gets 27,484,
  concludes it is inflated, and stops reading.**
  - **Fixed:** `field_presence()` now returns its denominator; the CSV carries
    **`n_payloads`** (the true denominator) **and** `n_items`, plus `feed_url` and `page`.
  - **K6 status corrected AGAIN — it FIRES.** It was withdrawn earlier today on the grounds
    that the scripts' only third-party import is declared. **That reasoning was sound but
    answered the wrong question**: K6 asks whether a non-author can reproduce the *headline
    figures*, not whether the code imports cleanly. They could not. **The withdrawal is itself
    withdrawn.**

- **4. THE REPLACEMENT INSTRUMENT WAS SILENTLY LOSING RAW.** ❗
  **752 COMPLETE feed pages were fetched; 708 `.json` files exist on disk. 44 pages were
  silently overwritten** — under a code comment reading *"immutable raw, exactly as served"*.
  Cause: the filename was `{publisher}_{kind}_{page}`, which collides when a publisher
  declares several feeds of one kind, and **catastrophically when a dataset site publishes no
  `publisher.name` at all** (32 pages from unnamed publishers all collided into
  `_<kind>_<pg>.json`).
  **This is the same defect class — undisclosed harvest-time data loss — that D-021 retired an
  entire corpus over, reproduced in the instrument built to replace it, and disclosed nowhere.**
  - **Fixed:** filenames are now keyed by a **page-URL digest**; collisions get a `_dup`
    suffix, are counted, and are reported in the run output. **Pages lost: 0 (was 44.)**
    Re-simulated against the census endpoint log: 752 pages → 742 distinct names + 10 suffixed
    = **752 retained**. (Real collision observed: **Chelmsford City Sports declares the same
    feed URL twice.**)
  - **The census artefacts already committed were produced by the OLD code and are therefore
    missing 44 raw pages.** The CSVs are unaffected (they were written from the in-memory
    pages, not re-read from disk), but **the raw archive is incomplete and must be
    re-harvested before it is treated as the retained-raw record.** Disclosed, not hidden.

- **5. A KILL RULE BROKE ITS OWN RULE.** `docs/v7-one-pager.md` K1 cited *"census, 173/173
  declared sites, 124 publishers"* against a **`ScheduledSession`-only** measurement — which
  only **30 publishers on 2 platforms** (LeisureCloud, singular) serve at all. **That is the
  exact pooling error the D-021 amendment was written to catch, committed inside the rule that
  forbids pooling.** Corrected.

- **6. A DOCUMENT INSTRUCTED THE ONE ACT FOUR OTHERS FORBID.**
  `brief-traceability.md` §6 said *"get P1 into the repo"* — contradicting D-022, D-024,
  `ATTRIBUTION.md` §3 and its own §0.1. Aggravating: `.gitignore` had **no `*.pdf` rule**,
  `README.md:112` recommends `git add .`, and **an untracked PDF sits at the repo root right
  now**. Corrected, and **`*.pdf` added to `.gitignore` as a mechanical safety rail** — the
  rule must not depend on remembering it.

- **Findings the audit raised that were themselves FALSE, and are rejected** (recorded so they
  are not re-litigated): that `src/verify_licences.py`, `results/licence_audit.csv`, `LICENSE`
  and `ATTRIBUTION.md` were never committed — **all four are at HEAD in b584451**; the lenses
  read the tree before that commit landed. The K6 conclusion survives, but on **entirely
  different grounds** (item 3), not on that premise.

- **The scoping error nobody had flagged.** **D-022 treats the partner brief as the sole
  acceptance authority. It is not — the examiner is, and the examiner is not London Sport.**
  Nothing in any document produced today traces to the **SEMTM0044 marking criteria** or to
  **4 September**, seven weeks out, with the analysis corpus just retired and WS3/WS4 unbuilt.
  Declared in July by the team, that is a defensible scoping position; discovered in September
  by the examiner, it is not. **Open — the team must resolve.**

- **Status: PROPOSED 2026-07-15.** Corrections 1, 2, 5 and 6 are applied to the documents;
  3 and 4 are applied to `src/harvest_pilot.py` but **the committed census raw remains
  incomplete until re-harvested**.

---

## D-027 · Reconciling the external drafts: blueprint (2) supersedes; three-stage attribution adopted (2026-07-15) — **PROPOSED**

Three externally-produced drafts (all timestamped 12:59, 2026-07-15) were assessed against the
repository's own work: `determinable_discovery_execution_blueprint (2).md`,
`answerability_pivot_decision_draft.md`, `brief_traceability.md`. **They are better than what
this repository holds in several specific ways, and two of their criticisms land.**

- **1. Blueprint (2) SUPERSEDES the (1) committed at `docs/execution-blueprint.md`.** The `(1)`
  copy was the newest available at 09:57; `(2)` was written at 12:59 and changes the
  architecture. **`docs/execution-blueprint.md` currently holds a superseded design.**
  The substantive changes, all adopted:
  - **Three-stage attribution replaces the binary.** **S0** current source entity before
    inheritance → **S1** recursively reconstructed current entity → **S2** declared consumer
    projection. Evaluate the same frozen queries at every stage; permit *source-limited*,
    *reconstruction-limited*, *projection-limited*, *mixed* and *null* outcomes.
    **This is strictly better than D-021/D-025's instrument-vs-publication binary**, which
    collapses S1 and S2 — conflating *"we never did the RPDE join"* with *"we did the join,
    then flattened the fields"*. Different failures, different repairs, one bucket.
  - **The title becomes outcome-neutral:** *"…Separating source publication, standards-aware
    reconstruction and consumer-processing effects"*, on the stated grounds that the pilot
    *"does not establish that all remaining indeterminacy is instrument-side"*. Correct.
  - **Five gates, not three** (scope, lineage, current-state, mechanism-eligibility, capacity).
  - **K7 IS CLOSED.** Razniewski & Nutt now carries *"Reference status: primary source verified
    15 July 2026"* — PVLDB vol. 4 no. 11, 2011, verified against the primary source. The kill
    rule that was firing this morning no longer fires. Formatting and its fit in the critical
    literature argument remain open; **the TODO-VERIFY may be lifted.**

- **2. The pivot draft's rejected-alternative list contains one this repository should have
  written and did not:** *"**Assume instrument-side loss is the answer** — rejected because the
  final same-vintage comparison must attribute rather than presuppose the dominant cause."*
  **D-025 committed exactly that error** and it is corrected above: the "child-only extraction
  loses all geography" claim was refuted by D-025's own `beta:sportsActivityLocation` finding,
  four bullets later. The draft also warns *"top-level field presence missed some embedded
  parent information"* — **tested and REJECTED for this corpus**: `superEvent` is a bare string
  in **18,213/18,213** cases, zero embedded objects, so the `INHERITABLE` classification is not
  contaminated by that route. **But the warning was right in spirit and caught a real instance
  by a different path** (`beta:sportsActivityLocation` is exactly "field information the
  top-level key check misses").

- **3. `brief_traceability.md` (external) vs `docs/brief-traceability.md` (repo) — MERGE, do not
  replace.**
  - **The repo version is stronger where it matters most:** its left column is **verbatim
    partner text, page-cited and machine-checked against the deck**. The external version heads
    its column *"Supplied brief meaning"* — **paraphrase, honestly labelled but not citable**.
    An examiner asking *"where does this clause come from?"* gets a page number from one and a
    characterisation from the other.
  - **The external version is stronger in three respects, all adopted:**
    (a) an **alignment acceptance test** — five conditions, incl. *"London is present in the
    final query evidence, not merely the introduction"* and *"no claim that the partner
    commissioned, approved or prioritised this exact task"*;
    (b) a far better **R2** row — *"'No prior work found' is bounded by the search, never
    'nobody has done this'"*;
    (c) it **fixes the London-scope problem this repo only flagged**: *"use wider feeds only to
    validate mechanisms"*, *"National mechanism evidence cannot support London-wide consequence
    claims alone"*, and *"London-wide language is prohibited unless the selection and coverage
    support it."* The census is **national** (Wigan, BwD Leisure); the analysis is London. That
    gap was named here and left open — the drafts close it with a rule.

- **4. A sampling criticism this repository has NOT yet tested.** The pivot draft rejects
  *"treat the pilot as the final result"* because *"one-page modified-history samples are not
  representative current-state prevalence measurements"*. **RPDE is a change feed ordered by
  `modified`; `next` walks forward in time.** The census took **pages 0–1 of each feed — the
  START of each change history, i.e. the OLDEST records** — not current state and not a random
  sample. **`attempted ÷ declared = 173/173 = 100.0%` is honest coverage of SITES and must
  never be read as coverage of records.** Structural findings (`superEvent` universality,
  parent/child shape) are robust to this; **prevalence rates may not be.** UNTESTED — carry as
  a live threat to validity until measured.

- **5. CORRECTION — `(2)` carries ALL FIVE local fixes, and carries them better.** An earlier
  draft of this entry said `(2)` "does not carry" them and ordered them re-applied. **Wrong** —
  that conclusion came from grepping for *this repo's own wording* rather than reading `(2)`.
  It has **Check 4 "mechanism eligibility and prevalence"**, **Check 5 "capacity and
  resumability"**, **§6 "Predeclared outcome branches"**, a corrected **§14** corpus gate, and
  **Razniewski verified** (better than a TODO-VERIFY). **Nothing was re-applied; `(2)` is
  installed verbatim** with measured status annotations only, and `diff` confirms **nothing
  removed**.

  **Two of `(2)`'s rulings land against this repository and are accepted:**
  - **Check 5:** *"The earlier approximate `bytes/item × 7.9m` calculation is a pilot estimate,
    not a capacity decision. It excludes some database, index, log, duplicate-response,
    temporary and backup costs."* → **D-021's "capacity is not a constraint and must stop being
    cited as a risk" is RETIRED.** It was an overclaim from one extrapolation.
  - **§16:** *"Stop treating missing fields as publisher faults until parent lineage is
    checked."* → this is **exactly the D-025 error** (D-026), written down in the blueprint
    before the repo made it.
  - **§12 partially closes the examiner gap** this repo flagged: it maps evidence to **LO1–LO5**
    and states honestly that *"No one can guarantee an 'exceptional' band until the actual rubric
    is obtained."* The **mark-band/4-September gap remains open.**

- **Adopted and APPLIED (2026-07-15):** the S0/S1/S2 model; the outcome-neutral title; the five
  gates; lifting the Razniewski & Nutt TODO-VERIFY (**K7 closed**). `docs/execution-blueprint.md`
  now holds `(2)` verbatim + status annotations. **Merged into `docs/brief-traceability.md`:**
  the **alignment acceptance test** (§5b — *two of five conditions currently pass; alignment does
  not pass*), the **London-scope prohibition** (§5a), and the **R2 boundary rule** (*"no prior
  work found" is bounded by the search, never "nobody has done this"*).

- **What the acceptance test immediately exposes.** Condition 3 — *"London is present in the
  final query evidence, not merely the introduction"* — **FAILS**, and no amount of harvesting
  closes it. Every figure this project holds is **national**; there is no London query benchmark.
  The census sampled Wigan, BwD Leisure and Chelmsford. **This is the sharpest open gap in the
  project and it was invisible until the external draft supplied the rule.**

- **Status: PROPOSED 2026-07-15.**

---

## D-028 · Wesley's v2 assessed: what is adopted, what conflicts, and the architecture question the team must settle (2026-07-15) — **PROPOSED**

`Closing_the_Activity_Gap_Proposal_v2.docx` (Wesley, 2026-07-15 16:06) was assessed against
this repository's evidence and its adopted decisions. **It is substantial work containing
material this repository lacks.** It also proposes an architecture the pivot would retire.
**Both are PROPOSED. Neither is decided. This entry does not settle it.**

### 1. ADOPTED from Wesley — implemented today

- **Per-feed licence register (`src/feed_licence_register.py`).** His rule — *"redistribution
  or republication is limited to feeds whose licences permit it, and per-feed attribution is
  carried on published outputs"* — is **correct and fixes a live defect of ours**.
  `src/verify_licences.py` reads the **dataset site**; that is why `Halo` could return HTTP 403
  on its licence while **14 of its derived rows were published in this public repo**
  (D-026 item 2). Site-level attribution cannot govern feed-level redistribution.
  **Implemented with zero new network requests**: every RPDE page envelope carries its own
  `license`, and the raw was retained. *A question nobody asked at harvest time, answerable
  now, **only because the raw was kept** — D-021's argument, demonstrated rather than asserted.*
- **Declared feeds may never be skipped silently (`src/harvest_pilot.py`).** His scope includes
  **`Event` (one-off)**, which our kind filter would have dropped **without a log line** —
  making the feed-level `attempted ÷ declared` that Check 1 demands quietly wrong. Skips now
  emit `SKIPPED_KIND_<kind>` to the endpoint log. **A skip is a decision and belongs in the
  ledger** — the same principle as the filename-collision defect (D-026 item 4).
- **London-scoping discipline** — already adopted at `docs/brief-traceability.md` §5a via the
  external draft. Wesley's formulation is the *operational* one and is better: *"the
  out-of-London remainder is a by-product of the same harvest, costs nothing extra to retain,
  and is used for one purpose only — the LAD-level robustness check."*

### 2. ADOPTED IN PRINCIPLE — Wesley's to build, and the only Check 3 material in existence

**Check 3 (current-state pipeline) has no implementation anywhere in this repo.** Wesley's v2
is the only specification of it, and it is more detailed than anything we hold:

> RPDE paged chronological exchange · **updated and deleted records** · **parent–child
> reconciliation** (`SessionSeries`↔`ScheduledSession`, `FacilityUse`↔`Slot`) · **64-bit
> modified timestamps** · rate-limit etiquette: **sleep on empty pages, weekly resync cap,
> 429 handling, 404-purge** · normalise to one schema · map activity names to the **OpenActive
> Activity List (SKOS)** · validate coordinates · **de-duplicate across providers by entity
> resolution** on (activity, venue/coordinates, time, organiser), since aggregators and
> multi-route publishing create cross-feed duplicates.

**This is not optional**: D-025 measured **8,372 `state: deleted` tombstones against 18,213
`updated` items — 31.5% of all `ScheduledSession` items are deletions.** A consumer ignoring
them over-counts sessions by roughly a third.

- **Continuous harvesting from week one**, to *"accrue a longitudinal record the live feeds do
  not otherwise provide"*. **Adopted, and it answers a threat we logged and could not close**
  (D-027 item 4): RPDE is ordered by `modified` and `next` walks forward, so our two-page
  census read the **oldest end** of every feed. Continuous capture is the only way to obtain a
  current-state series; no single snapshot fixes it.
- **Active Places as an independent coverage benchmark** — *"used to estimate publishing
  coverage independently of OpenActive itself."* Strong: it measures the ecosystem's own
  selectivity against a source outside it, turning our coverage caveat into a measurable
  quantity. D-011/D-018 already have the facilities layer; this gives it a second purpose.

### 3. CONFLICTS WITH ALREADY-ADOPTED DECISIONS — must be fixed whichever architecture wins

These are **not** architecture questions. They contradict decisions already adopted:

| Wesley v2 | Conflict |
|---|---|
| *"English Indices of Deprivation **2019**"* | **D-007 (adopted)** mandates **IoD2025**, File 10 v2, and says explicitly *"Not IoD2019."* |
| *"Analysis is intended at small-area level (~4,800 LSOAs / ~980 MSOAs)… the WS1 audit fixes the feasible unit"* | **D-008 (adopted)** already settled this at **borough level**. The audit **has run**: LSOA **~95.6%** and MSOA **~81.4%** carry zero sessions. It is not pending. |
| *"Bayesian small-area estimation… models provision with uncertainty rather than forcing a coarser unit"* | Modelling around the emptiness D-008 measured. **D-010** right-sized methods for n≈33 and dropped this class. |
| *"All work is the team's own under the unit's **AI-use rules**"* | **D-017 (adopted)**: the repository and report carry **no AI-use statement**, per the supervisor's direct guidance. |

### 4. FIGURES REFUTED BY MEASUREMENT — fix regardless

| Wesley v2 | Measured |
|---|---|
| *"roughly seventy publishers"* | **123** publishers with data; **144** named across **173** declared sites (`results/census_field_presence.csv`, `results/licence_audit.csv`) |
| *"over two million structured activity opportunities"* | **7.9 million** — the deployed OpenActive Data Intelligence Platform, verified live 14–15 Jul 2026 |
| *"CC-BY 4.0 is common; some CC0 / OGL"* | **162/162 readable dataset sites declare CC-BY 4.0 — unanimous. Zero CC0. Zero OGL.** (`results/licence_audit.csv`) The per-feed register is still right; **this premise for it is not.** |
| *"Events (one-off)"* in scope | No `Event` distribution observed on any sampled site; the census saw five kinds only. **Not disproven ecosystem-wide — but not in evidence.** His scope nonetheless exposed our silent-skip bug. |

### 5. WHERE WESLEY IS RIGHT AND THIS REPOSITORY IS NOT

- He reached the **publication-side mechanism independently, by reasoning**: *"what OpenActive
  publishes about a place is not a neutral census of provision but a patchwork shaped by who
  chooses, and is equipped, to publish."* The census measured the same thing.
- He **fixed the v1 scoping error** — one publisher's feed (Open Sessions) standing in for the
  ecosystem — before we did.
- His **London discipline is better than ours.** `brief-traceability.md` §5b condition 3
  (*"London is present in the final query evidence, not merely the introduction"*) **FAILS** for
  this repository: every figure we hold is national (Wigan, BwD Leisure, Chelmsford). Wesley's
  v2 does not have that defect.

### 6. THE DECISION THE TEAM MUST MAKE — this entry does NOT make it

**Two architectures are on the table and nobody has arbitrated:**
- **Wesley v2:** whole-ecosystem equity-of-provision — gap index, E2SFCA, small-area estimation,
  equity-aware discovery.
- **The pivot (D-020/D-021/D-023):** determinable discovery — corpus retired on evidence,
  three-stage S0/S1/S2 attribution, thin three-state demonstrator.

**Status of record:** every pivot entry is **PROPOSED**. **PR #6 has been open since 09:45 UTC
2026-07-15 with zero reviews and zero comments**, with Wesley, Clarence and Fahmi all requested
as reviewers. **Wesley is not working against a decision — there is no decision.** His v2 is a
competing proposal made in good faith and in parallel.

> **Governance finding, recorded because it is uncomfortable and true.** `git log --all` returns
> **one author**. In a single day this repository retired a 549,169-row corpus, changed the
> title, rewrote the research questions, adopted an external architecture and set the licence —
> on one member's judgement, with every entry honestly marked PROPOSED but none ratified. The
> team notes record a bus-factor finding against `src/recommender/`. **The same finding points
> harder at this branch.** Ratification is not administrative here; it is the difference between
> a documented method and one person's opinion.

**A straight "the pivot wins" would discard real work** — the London rule, the per-feed licence
register and the entire Check 3 specification all come from Wesley's v2 and survive either way.

- **Status: PROPOSED 2026-07-15.** Items in §1 are implemented; §2 is adopted in principle and
  unbuilt; §3 and §4 require correction **whichever architecture the team ratifies**; §6 is for
  the team, not for this entry.

---

## D-029 · Census2: the platform dichotomy REPLICATES exactly; three claims corrected (2026-07-15) — **PROPOSED**

A second full census (`--tag census2`, 14:56 UTC) was run with the D-026-fixed code, five hours
after the first (09:53 UTC). It is an **independent replication at a different vintage**, and it
is the strongest evidence this project has produced — **and it retracts three of our claims.**

### 1. REPLICATION — every rate identical, on grown denominators

| `SessionSeries` | census 09:53 | census2 14:56 | |
|---|---|---|---|
| LeisureCloud · `category` | 28/28 = **100.0%** | 29/29 = **100.0%** | identical |
| LeisureCloud · `activity` | 0/28 = **0.0%** | 0/29 = **0.0%** | identical |
| singular · `category` | 2/6 = **33.3%** | 2/6 = **33.3%** | identical |
| singular · `activity` | 6/6 = **100.0%** | 6/6 = **100.0%** | identical |
| Legend · `category` | 0/3 = **0.0%** | 0/6 = **0.0%** | identical |
| Legend · `activity` | 0/3 = **0.0%** | 0/6 = **0.0%** | identical |

**Every rate is identical to one decimal place.** The denominators *grew* — new publishers
appeared, and three more Legend publishers served `SessionSeries` — and **the rates did not
move**. `superEvent` on `ScheduledSession` replicated at **18,690/18,690 = 100.0%**
(census: 18,935/18,935); `Slot` at **0/94,028 = 0.0%**. Capacity replicated: **1,347 bytes/item
→ ~10.6 GB** (census: 1,329 → ~10.5).

**This is what the pilot's 11-publisher hypothesis needed and never had: a rate that survives an
independent harvest.** It is no longer a hypothesis.

### 2. CORRECTION — "173/173 = 100% of declared" was true at 09:53 and is ALREADY FALSE

**The declared frame is dynamic. It grew from 173 to 174 sites in five hours** (LeisureCloud
31 → 32); publishers with data went 123 → 125. **Any coverage claim is a claim about an
instant and must carry a timestamp.** "100% of declared" without one is false by the time it
is read. This also *strengthens* Wesley's continuous-harvesting proposal (D-028): a frame that
moves hourly cannot be characterised by any single snapshot.

### 3. RETRACTION — "Legend is the least reliable platform in this sample" (D-021) is WITHDRAWN

D-021 concluded that from 8 endpoint failures. Census2 refutes it:

- **Sites failing: 14 (census) → 16 (census2). But only 9 are PERSISTENT.** Five recovered;
  seven are new.
- **All five recovered sites are Legend, and all five were HTTP 403s that cleared on retry.**
- **A 403 that clears on retry is rate-limiting, not a publication defect.** We were measuring
  **our own request pattern against Legend's rate limiter**, and reporting it as Legend's
  reliability.

**Consequences:** (a) the D-021 sentence is withdrawn; (b) the honest structural rate is **9 of
174 sites (5.2%) persistently unreadable**, not 14 of 173 (8.1%) — that figure conflated
transient and structural failure; (c) **any endpoint-failure claim requires ≥2 attempts at
different times**, and the harvester's single-attempt design cannot distinguish the two.
**Retry-and-classify is now a harvest requirement**, and it aligns with Wesley's specified
rate-limit etiquette (D-028 §2: sleep on empty pages, weekly resync cap, 429 handling).

### 4. The D-026 fixes are verified in production

- **Filename collisions: 0 pages lost.** 767 files retained, **8 collisions suffixed** and
  reported. The census archive lost **44 pages silently**; census2 lost none.
- **K6 CLOSED.** `results/census2_summary.csv` carries **every headline figure as a committed
  artefact**, each with its denominator and a note — including the trap that `raw.items`
  *includes tombstones* while `presence_rate` does not. The figures no longer live in stdout,
  and an examiner reconciling them now gets the right answer. *(K6 was: "a non-author cannot
  reproduce the headline table/figure from a clean clone.")*

### 5. What census2 does NOT fix

- It is still **2 pages per feed, from the `modified`-ascending end** of every change feed —
  the oldest records (D-027 item 4). Structural claims replicate; **prevalence over the full
  corpus remains unmeasured.** Only continuous capture (D-028) addresses this.
- **`level` / `ageRange` / `activity` source-absence and the lineage rates (D-025) were computed
  on the LOSSY census archive** and have **not** been recomputed on census2. They should be.
- **174 sites is 100% of *declared*, never of *existing*** — publishers outside the four
  catalogues remain invisible by construction.

- **Status: PROPOSED 2026-07-15.** Supersedes D-021's endpoint-reliability claim and its
  "173/173" framing; the platform×kind finding is **confirmed by replication** and strengthened.

---

## D-030 · PROPOSED scientific architecture: determinable discovery, London-first (2026-07-15) — **PROPOSED**

> **Status: PROPOSED. NOT ratified, NOT adopted.** This entry becomes operational only when
> **all four members explicitly accept the architecture and a named deliverable**. Until then it
> is one member's proposal. **It is not a defect record** — historical corrections are listed
> once, at the end, as bounded support tasks.

### 1. The decision

**Determinable discovery is the primary scientific and technical architecture. Equity of
discoverability is its evaluation lens. The existing Open Sessions gap-index association is
retained as prior-sighted, source-specific exploratory motivation only.**

**Title**

> **Determinable Discovery in London's OpenActive Ecosystem: Separating Source Publication,
> Standards-Aware Reconstruction and Consumer-Processing Effects**

**Plain-English purpose.** Build a reliable London OpenActive catalogue, test whether realistic
activity searches can be answered honestly, identify why some searches remain uncertain, and
measure which improvements help most.

**Aim.** To determine which prespecified London referral- and finder-style searches are supported
determinately by a correctly reconstructed OpenActive corpus, attribute indeterminate results to
**source publication (S0)**, **standards-aware reconstruction (S1)** or **consumer processing
(S2)**, and quantify which validated changes most improve discovery coverage.

**Research questions — three. No fourth.**
1. **Corpus validity.** Which relevant London feeds, records, parent–child relationships and
   search fields can be reconstructed reliably, and what acquisition or processing failures remain?
2. **Discovery determinability.** Which prespecified London searches return sufficient determinate
   matches, only uncertain candidates, or no observed listed match?
3. **Mechanisms and improvements.** How do standards-aware reconstruction and consumer projection
   alter those results, and which feasible repairs produce the greatest measured improvement?

Equity does **not** get a fourth RQ. It controls **query construction, stratification and
interpretation**.

**Primary estimand.** For each prespecified query, estimate **how its classification and result set
change between S0, S1 and S2**, and **attribute each change to a documented mechanism**.

Four distinct comparisons, not one:
- **S0 → S1** — *descriptive reconstruction experiment.* **Not a hypothesis test:** reconstruction is
  *designed* to recover inherited fields, and `location` is 100% inheritable, so a difference is
  guaranteed **by construction**. Report the magnitude and mechanism; claim no discovery from it.
- **S1 → S2** — *information-preservation experiment.* This one **can fail.**
- **Retrieval policies** — *decision-consequence comparison.*
- **Repairs** — *measured scenario effects.*

**Falsifiable proposition (S1 → S2):**
> For at least one prespecified London query family, **consumer projection materially changes
> determinate discovery relative to standards-aware reconstructed records.**

**"Material" is defined after the development pilot and before locked evaluation**, from a
use-case consequence — never an invented number. **A null is a result**: if projection preserves
determinability, report it and withdraw the information-loss claim.

> *An earlier draft proposed "the three stages do not preserve the same determinability". That is
> near-trivially true by construction and could not fail — it was not a falsifiable proposition.*

### 2. Claims boundary — binding

| We may claim | We may NOT claim |
|---|---|
| Which prespecified searches are determinate / indeterminate / no-observed-listed-match, for this corpus at a stated observation time | That any borough has more or less **physical-activity provision** |
| That indeterminacy attributes to S0, S1 or S2, evidenced by same-vintage paired comparison | That listing counts measure provision, participation or health |
| That discoverability differs across distributed London origins and barrier-relevant constraints | That **provision** is unequal, or that publication inequality **causes** inactivity |
| Information sufficiency for **referral-style discovery** | **Clinical safety** or safe signposting |
| Repair value, measured | Causal or behavioural effect |

**The contribution is task-conditioned London discovery determinability and mechanism
attribution** — not raw-byte forensics, not generic data quality, not another provision dashboard.

**The Open Sessions association** (partial Spearman ρ = −0.498, p = 0.0044; linear incremental
model inconclusive: ΔR² = 0.070, nested p = 0.110, CI includes zero; `reports/incremental_validity.csv`)
is **prior-sighted, source-specific exploratory motivation**. It does not distinguish actual
provision from publication coverage. **It remains prior-sighted secondary motivation.**
Multi-publisher replication may be reported as a **listing/discoverability association** — it does
**not** identify provision, publication inequality or causality, and **cannot promote listing
density into a provision claim.** A listing corpus, however reconciled, still cannot separate
real-world provision from whether provision is published from whether we acquired it.

**Haringey** is a **public workflow exemplar** only. London Sport did not commission this
evaluation. Beginner-suitability is **not** a Haringey finding until the London lineage analysis
supports it.

### 3. Status — built / partially built / planned (verified 2026-07-15)

| Component | Status |
|---|---|
| Catalogue → site → feed walker, per-endpoint status, stratified | **BUILT** (`src/harvest_pilot.py`) |
| Licence audit + per-feed register | **BUILT** (`src/verify_licences.py`, `src/feed_licence_register.py`) |
| Field-lineage tracer (parent/child provenance) | **BUILT** (`src/trace_lineage.py`) — rates computed on the lossy archive; recompute |
| WS1/WS2 borough pipeline + gap index | **BUILT, TESTED** — reclassified to motivation by §2 |
| Exact-byte raw capture | **PLANNED** — current harvester retains parsed-and-reserialised JSON |
| RPDE current-state walk — live edge, apply `updated`, drop `deleted`, latest-by-id | **BUILT AND TESTED** — `src/harvest_open_sessions.py:125` (`harvest_feed`); `tests/test_harvest.py` exercises tombstones and the live edge with a canned stub. **Reuse it; do not rebuild.** |
| *Generic* resumable multi-feed store (exact bytes, cursors, retry/failure history, incomplete-feed flags) | **PLANNED — NOT STARTED.** This — not current-state logic — is the actual gap. |
| Parent–child reconstruction with property provenance | **PARTIALLY BUILT** — `src/trace_lineage.py` indexes parents, resolves `superEvent`, classifies child-held / inheritable / source-absent / unresolved, and emits hand-checkable samples. **Missing:** reconstruction over a complete current-state corpus, materialised **S1** records, provenance carried into retrieval, recursive/standard-complete inheritance. |
| S0 / S1 / S2 records | **PLANNED — NOT STARTED** |
| Frozen London query benchmark | **PLANNED — NOT STARTED** |
| Three retrieval policies (closed-world / permissive / three-state) | **PLANNED — NOT STARTED** |
| Thin referral/finder demonstrator | **PLANNED — NOT STARTED.** No retrieval, three-state or scoring logic exists anywhere in `src/`. `src/recommender/` has never been committed by anyone. |
| *(consequence)* `src/export_ws3_inputs.py` | **BUILT, TESTED — SUPERSEDED as the primary WS3 data contract; PARTIALLY REUSABLE.** Reusable: point-in-polygon borough assignment, spatial join, geographic stratification fields, its test. Superseded: the equity-signal (gap index / quadrant) payload, which §5 demotes to secondary. **Do not delete now** — retire or re-point after the vertical slice establishes the new data contract. |
| R2 national approaches + prior-art matrix | **PLANNED — NOT STARTED** |
| Offline reproduction bundle | **PLANNED — NOT STARTED** |

**S0/S1/S2 materialisation, the London benchmark, three-state retrieval, the prototype, the R2
matrix and the reproduction bundle do not exist.** Current-state walking and lineage tracing **do**
(see the table) and must be reused.

**Contribution record — dated, not standing:** as at **2026-07-15T16:13Z**, this branch carries
**37 commits** (40 across all branches), **one author identity**, and **PR #6 had 0 reviews** with
az25352, wy25780 and fahmi-alshahabi still requested. **Re-check before citing.**

### 4. Immediate priority — one complete London vertical slice

Not more analysis of the two-page census. **A slice that proves the architecture works end to end:**

1. Select a **small heterogeneous group of London session feeds**.
2. Harvest **to live edge** (not two pages).
3. **Reconstruct current state** — apply updates and deletions.
4. **Resolve parent–child** fields, retaining property provenance.
5. Generate **S0 / S1 / S2** records.
6. Run **5–10 draft London queries**.
7. Compare **closed-world / permissive / uncertainty-aware** outputs.
8. **Capped verification** — not unbounded: **3–5 heterogeneous London session feeds**, **5
   development queries**, **max top-10 candidates per query per policy**; **inspect every
   disagreement between policies**, plus a **stratified sample of agreements**; trace every
   inspected field to child / parent / missing-at-source / acquisition failure.
9. Demonstrate **one query end-to-end** in the prototype.

**In parallel:** begin R2's reproducible national approaches and literature matrix — search
protocol, inclusion/exclusion rules, primary-source verification, and a final column stating what
contribution survives. *"No prior work found"* always means *"none found within this documented
search."*

### 5. Proposed must-have / stretch boundary

**Must have.** Current-state London session corpus · S0/S1/S2 · frozen London query benchmark ·
three retrieval baselines · small two-assessor adjudicated sample · thin working prototype · R2
matrix · measured repair recommendations · non-author reproduction · brief/LO traceability.

**Cut or stretch — do not build.** E2SFCA · Bayesian small-area modelling · full facilities/Slot
architecture · causal or health-effect interpretation · large polished dashboard · fairness
reranking · whole-UK longitudinal analysis · additional health validators · full Active Places
entity linkage.

**Do not add methods to satisfy LO3.** The must-have set already spans data engineering, semantic
reconstruction, geospatial processing, information retrieval, three-valued reasoning, evaluation,
sensitivity analysis and human adjudication — **once built**.

### 6. Deliverables and owners — REQUIRED FOR RATIFICATION

| # | Deliverable | Owner | Date |
|---|---|---|---|
| 1 | Current-state store + exact-byte capture + tombstones | *(unassigned)* | *(tbd)* |
| 2 | Parent–child reconstruction + S0/S1/S2 + provenance | *(unassigned)* | *(tbd)* |
| 3 | Frozen London query benchmark + constraint-provenance table | *(unassigned)* | *(tbd)* |
| 4 | Three retrieval policies + adjudicated sample + sensitivity | *(unassigned)* | *(tbd)* |
| 5 | Thin referral/finder demonstrator | *(unassigned)* | *(tbd)* |
| 6 | R2 national approaches + prior-art matrix | *(unassigned)* | *(tbd)* |
| 7 | Offline reproduction bundle + non-author verification | *(unassigned)* | *(tbd)* |

**Every owner cell is empty. That is the ratification blocker, and it is not a documentation
problem.**

### 7. Ratification — four questions, four answers required

1. Do we accept **determinable discovery** as the primary project?
2. Do we accept **equity of discoverability** as the evaluation lens?
3. Do we accept the **must-have / stretch** boundary in §5?
4. **Does each member accept a named deliverable and date in §6?**

**If any member does not answer, this entry stays PROPOSED and the architecture is not frozen.**

### 8. Bounded support corrections — not the dissertation

Recorded once. These are engineering and documentation tasks; **none is a research contribution**,
and **none justifies re-running census2**.

- **Exact-byte capture.** The harvester retains `json.dumps(response.json())` — parsed and
  re-serialised, **not** bytes as served (duplicate keys collapse; formatting is lost). Fix before
  the **final** collection: retain `response.content`, URL, status, headers, retrieval timestamp,
  SHA-256, retry attempt, feed identity. **Delete the false "exactly as served" comment.** Census2
  remains usable as **structural pilot evidence**; do not re-run it for byte fidelity.
- **Offline reproduction (replaces K6 rhetoric).** One acceptance test: *a named teammate obtains
  the private frozen raw bundle, verifies its checksum, runs the documented offline pipeline and
  reproduces the primary tables within declared tolerances.* Needs: snapshot location, SHA-256
  manifest, access instructions, environment lock, one command, signed non-author verification.
  **Stop adjudicating whether K6 "fires".**
- **Prior-sight terminology — split, not global replace.** **Code/tests:** *"adult inactivity
  excluded from index construction"* (true — `tests/test_analysis.py` proves it by perturbation).
  **Report/decision log:** *"prior-sighted external criterion"*. **Never:** *"confirmatory
  held-out validation"*. Hours, not another decision cycle.
- **Bristol Level 7 descriptors** are general, not the SEMTM0044 rubric. **Obtaining the
  unit-specific rubric remains open.**

### 9. Supersession

Supersedes D-020's architecture and the equity-primary reading of D-011/D-012/D-013 **as the
project's central claim** — those entries stand as executed work and motivation. D-021 (corpus
retirement), D-025 (lineage method), D-027 (S0/S1/S2), D-028 (Wesley's adoptions) are **inputs to
this decision**, not superseded.

- **Status: PROPOSED 2026-07-15. Not ratified. Owners unassigned.**
