# CLAUDE.md — Closing the Activity Gap (SEMTM0044)

Equity analysis of physical-activity provision in London using OpenActive and
complementary open data, for partner London Sport. MSc Data Science group
project (60 credits), University of Bristol. Hand-in: 4 September 2026.
Assessed as: group report + code repository (60%), group presentation (20%),
individual reflective accounts (20%).

> RECONCILED to the post-WS1-audit state (supersedes the pre-audit version).
> Reflects decisions D-007–D-012. Any future methodological change goes in the
> decision log FIRST, then this file is updated to match. If this file and the
> decision log ever disagree, the decision log wins — and fix this file.
> Repo-specific sections (layout, commands) were verified against the working
> tree on 2026-07-01.

## Rule zero — overrides everything
NEVER invent facts, numbers, statistics, file paths, column names, dataset
fields, API behaviour, or references. If it has not been verified against this
repo's code, data, or `docs/`, label it **UNVERIFIED** and stop to ask.
A confident wrong answer is the worst possible outcome on this project.
Saying "I don't know, let's check" is always acceptable.

## Settled decisions (quick reference — do not re-litigate; see docs/decision-log.md)
- **D-007** Deprivation source is **IoD2025** (File 10 v2, lower-tier LAD
  summaries). NOT IoD2019.
- **D-008** Unit of analysis is the **London borough / LAD** (33 = 32 boroughs
  + City of London). The WS1 audit settled this (LSOA ~95% empty, MSOA ~81%
  empty). This is DECIDED, not a candidate.
- **D-009** OpenActive **Open Sessions** is the primary provision feed; the
  national catalogue is **not merged** into it.
- **D-010** Methods revised for n≈33: **imputation dropped** (incl. MICE);
  **t-SNE/UMAP dropped**; **PCA is descriptive-only**; the **need×provision
  quadrant typology is the PRIMARY structure**; gap index hardened; E2SFCA
  added as a **conditional** accessibility extension.
- **D-011** Two-layer provision — **sessions and facilities are analysed
  separately and never merged**; tiered, triangulated validation; any E2SFCA
  is PTAL-weighted and conditional.
- **D-012** **Held-out validation**: adult inactivity is held OUT of the need
  composite and used as the **independent validation target**. Deprivation and
  demographics are need INPUTS and are **never** used as validators.

## Project state (keep current — update via PR when a decision changes)
- WS1 data acquisition is essentially complete: real London sessions (494 at
  33 boroughs), Census 2021 shares, IoD2025, and Active Lives inactivity are
  wired and verified. Active Places (facilities) and PTAL remain to acquire.
- WS2 analytical core has reached a validated milestone: the activity-gap
  index is deprivation-anchored and validated against held-out inactivity
  (Spearman ≈ +0.46, n=32, non-circular by construction). [DATA — current run]
- The discovery prototype (WS3) and dashboard (WS4) are the next build focus.
- Decision log lives at `docs/decision-log.md`. Every methodological choice
  (thresholds, weightings, catchment sizes, decay weights, unit of analysis)
  gets a dated entry with rationale and alternatives. Notable AI-assisted
  contributions are logged there too, per the unit's AI-use rules.

## Data sources (the only permitted sources — do not add others silently)
- OpenActive **Open Sessions** SessionSeries feed (CC-BY 4.0). London venues
  from the national OpenActive catalogue are used for context only, not merged
  (D-009).
- **English Indices of Deprivation 2025** (MHCLG), File 10 v2 lower-tier LAD
  summaries (D-007).
- ONS **Census 2021** demographics; ONS official boundaries (2021 LAD).
- Sport England **Active Lives** adult inactivity, **borough level** — used as
  the held-out validation target (D-012), not as a need input.
- Sport England **Active Places** facilities — a second, independent provision
  layer for corroboration, analysed separately (D-011). [to acquire]
CC-BY attribution must appear on every published output.

## Repo layout (verified against the working tree, 2026-07-01)
```
src/
  __init__.py
  pipeline/
    config.py        ALL constants: paths, column maps, per-capita base, geography
    pipeline.py      build_features() — geography, census, IoD, sessions, inactivity, …
    gap_index.py     need / provision / gap index / quadrants / held-out validation
  run_pipeline.py    builds data/processed/borough_features.csv
  run_analysis.py    builds the gap index + validation from the feature table
tests/
  test_run.py        pipeline test on synthetic fixtures (asserts 33 boroughs)
  test_analysis.py   gap-index test incl. the D-012 held-out proof
data/raw/            immutable inputs (gitignored)
data/processed/      pipeline outputs (gitignored)
notebooks/           exploratory work (e.g. data_audit().ipynb)
reports/             WS1 audit outputs + figures/tables/metrics that feed the report
docs/                team.md now; decision-log.md, data-quality-audit.md, references.bib [to add]
dashboard/           discovery prototype + dashboard app [planned, WS3/WS4]
```
> Note: the pipeline code above lives in the working tree but is not yet fully
> git-committed (only the scaffold is tracked). Commit it on a branch before
> relying on versioned history.

## Commands (verified this session)
- Environment: currently anaconda **base** (Python 3.13) with pandas, geopandas,
  shapely, openpyxl present (geospatial/Excel deps installed via conda-forge;
  listed in `requirements.txt`). A dedicated `ls-openactive` conda env + a pinned
  `environment.yml` is a recommended next step — **not yet created**. Never
  upgrade deps silently.
- Pipeline: `python -m src.run_pipeline`  ·  Analysis: `python -m src.run_analysis`
- Tests: `python -m tests.test_run` and `python -m tests.test_analysis`
  (add `pytest -q` / `ruff check .` once wired into CI).

## Hard rules

### Data handling
- `data/raw/` is immutable. Never edit, "fix", or hand-patch raw data.
  All transformations happen in pipeline code, reproducibly.
- Never fabricate, extend, interpolate, or **impute** data values to make an
  analysis work. Missingness is a finding, not an obstacle (D-010).
- Print and eyeball a sanity block for every artefact (row counts, value
  ranges, CRS, % missing per key field, duplicate count). Current tests are
  **assertion-based** (`tests/test_run.py`, `tests/test_analysis.py`);
  schema-enforced validation (e.g. pandera) is a target, not yet in place — do
  not claim an artefact is schema-validated.
- Absence of data is not absence of activity — carry this caveat into any
  output that maps or ranks provision. OpenActive under-captures private/
  commercial provision, which can make well-provided areas look under-served;
  state this limitation wherever provision is ranked.

### Geospatial
- Store coordinates in WGS84 (EPSG:4326). ALWAYS reproject to British
  National Grid (EPSG:27700) before any distance, area, buffer, or catchment
  computation. Never compute distances in degrees.
- London filter = official ONS boundaries; **33 local authorities**
  (32 boroughs + City of London, E09000001). Assert this count in tests.
- Every GeoDataFrame operation must be CRS-explicit; assert CRS in code.

### Statistics and modelling (per the decision log — do not deviate)
- Determinism: the pipeline is currently deterministic (no stochastic step).
  If any randomness is introduced (e.g. future clustering or sampling), its seed
  MUST come from a single constant in `src/pipeline/config.py`, so results are
  stable across reruns.
- Price (and similar structurally-missing fields) are **MNAR**: represent with
  a present/absent indicator (`is_free`). NEVER impute price values.
- **No imputation** of missing values (D-010, n≈33). Characterise the
  missingness mechanism (MCAR/MAR/MNAR) and report it; do not fill it.
- **Structure discovery**: the **need×provision quadrant typology**
  (priority / high-need-served / low-low / well-served) is the PRIMARY lens.
  **PCA is descriptive-only** (report retained variance). **t-SNE/UMAP are not
  used** (dropped, D-010). If any clustering is added it is secondary, done in
  standardised/PCA space with silhouette + cross-method agreement, and never
  on a 2-D embedding.
- **Activity-gap index**: standardised need minus standardised provision per
  borough. Log/rank-transform skewed indicators (e.g. sessions per 10k) BEFORE
  standardising; report BOTH a z-based and a rank/percentile-based
  construction; run weight-sensitivity across need weightings and report
  Spearman vs the base. City of London (zero sessions → undefined provision)
  is excluded from standardisation parameters.
- **Validation (D-012, strict)**: validate the gap ONLY against **held-out
  signals** — Active Lives adult inactivity is the primary independent target;
  a *distinct* health outcome (e.g. obesity, NOT republished inactivity) and
  the facilities layer provide corroboration. **NEVER validate against
  deprivation or demographics** — they are need inputs, and using them re-
  introduces the circularity D-012 removed. Report the validation coefficient
  with its uncertainty (CI, n) and note spatial autocorrelation as a caveat.
- **Levels**: all core analysis is at borough level (D-008); inactivity is at
  the same borough level and is therefore the validation target, not
  "contextual" evidence. Do not disaggregate any borough metric to sub-borough.
- **Need vs inactivity naming**: Census **economic inactivity**
  (`pct_econ_inactive`, a need input) is a different variable from Active Lives
  **physical inactivity** (`pct_inactive_adults`, the validator). Never
  conflate them in code or prose.
- The discovery prototype is deterministic filtering + content-based
  similarity + fairness re-ranking (score = α·relevance + (1−α)·equity). It is
  NOT a learned model and makes **NO accuracy claims** — there is no
  interaction ground truth. Evaluate only with beyond-accuracy metrics
  (coverage, intra-list diversity, affordable/accessible share, geographic
  spread), reported across α. Never evaluate against synthetic labels as if
  they were accuracy.

### Reporting and citations
- Any number in a report, README, or notebook markdown must be computed by
  code in this repo and traceable to a script + results file. Cite the
  generating path in a comment. No remembered or estimated statistics.
- References come from `docs/references.bib` (the proposal's list) only.
  Anything new is inserted as `TODO-VERIFY` until a team member has read the
  actual paper. NEVER invent a citation, DOI, page number, or URL.
- British English. Harvard referencing. Formal academic register.
- No content, text, figures, code, or analysis reused from the (AI-prohibited)
  VISA coursework — only transferable skills.
- State data vintages explicitly (IoD 2025 · Census 2021 · Active Lives
  2024/25) — triangulating across vintages is fine, but the examiner will
  check that you noticed.

### Code and git
- Workflow: branch → PR → peer review → squash-merge. `main` is protected.
  NEVER commit or push directly to main. (Enforce mechanically via branch
  protection + CI, not just this rule.)
- Never run: `git push --force`, `git reset --hard` on shared branches,
  history rewrites, or `rm -rf` outside `/tmp`.
- One concern per PR. Small diffs. Do not refactor unrelated code, delete
  others' code, or rename things without being asked.
- Every new/changed function: type hints, docstring, and a test. Spatial
  methods (e.g. E2SFCA, if built) get toy-grid fixtures with hand-computed
  expected values.
- No new dependencies without asking first; if approved, pin the version.
- Run the tests (and `ruff` once wired) before declaring any task complete.

## Ask before acting when…
- a task is ambiguous, or you would need to assume something about the data
  you have not actually checked;
- it touches schemas, thresholds/weightings, dependencies, the validation
  design, or deletes/moves files;
- two reasonable approaches exist — present both with trade-offs instead of
  silently choosing.
One clarifying question beats a plausible guess, every time.

## Definition of done (every task)
1. Plan stated and approved before non-trivial work (plan mode).
2. Code + tests written; tests pass; lint clean.
3. Sanity block printed and eyeballed: row counts, value ranges, CRS,
   % missing per key field, duplicate count.
4. Decision-log entry written if a methodological choice was made.
5. Closing summary states: what changed, what was verified and how, and
   anything that remains UNVERIFIED.

## Out of scope for Claude
- Drafting any part of the individual reflective accounts (personal,
  assessed individually — humans only; structure advice at most).
- Making claims about recommendation accuracy, causal effects, or
  individual-level behaviour from area-level data.
- Adding data sources, scraping non-listed sites, or calling external APIs
  beyond the listed feeds.
