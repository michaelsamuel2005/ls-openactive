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
    Halo, Serco Leisure); one Bookteq site 404. **Legend is the least reliable platform
    in this sample.** These are publication-process defects, logged with status.

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

- **Open risk (blocks reliance).** **Neither primary is in this repository.** P1 sits in one
  member's `~/Downloads`; P2 exists only inside a zip. No one cloning this repo can check a
  single quotation against its source — the same bus-factor defect recorded against
  `src/recommender/`, and a direct failure against output type **O8** ("Instructions needed
  to reproduce the analysis"). **Action:** obtain permission to commit P1, or record a
  citable reference to it.

- **Status: PROPOSED 2026-07-15.**

---

## D-023 · Answerability pivot — rejected alternatives and thresholds (2026-07-15) — **PROPOSED**

- **Decision (proposed).** Reframe the project's central question from *"where is provision
  unequal?"* to *"which discovery questions are answerable, where, and why not?"* Read
  against P1, this is not a departure from the brief: the output framework (P1 p.22) names
  **"DATA QUALITY AND SUITABILITY ASSESSMENT"** as a required output type, itemising
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
