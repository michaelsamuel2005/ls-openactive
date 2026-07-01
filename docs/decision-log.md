# Decision log — Closing the Activity Gap (SEMTM0044)

Canonical, single-source record of the project's settled methodological
decisions. **This file wins over any other document** (CLAUDE.md, the project
instructions, the proposal): if they disagree, fix them to match this log.

Convention: one dated entry per decision (D-0NN), with rationale and the
alternatives considered. Notable AI-assisted contributions are noted here too,
per the unit's AI-use rules.

> **Consolidation status (2026-07-01).** D-011 and D-012 are captured in full
> (see `docs/D-011_decision_log.md`, `docs/D-012_decision_log.md`, reproduced in
> summary below). **D-007–D-010 are summarised here from verified cross-
> references** (the proposal §§6–7, D-011's relationships block, and the settled
> state observed in code) — their **original full logs still need migrating into
> this file**; until then, treat the summaries as authoritative on the *decision*
> but incomplete on rationale/alternatives. This consolidation closes the
> version-drift that arose from the logs living scattered in Downloads.

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
  ~95.5% of LSOAs and ~81.2% of MSOAs carry zero sessions, so neighbourhood-level
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
