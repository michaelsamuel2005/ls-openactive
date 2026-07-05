# Engineering rules — Closing the Activity Gap
Working rules for everyone (and every tool) contributing to this repository.
The decision log (`docs/decision-log.md`) wins over this file if they disagree.
Unit-level compliance rules live in `docs/unit-rules.md`.

## Rule zero — overrides everything
Never state facts, numbers, statistics, file paths, column names, dataset
fields, API behaviour, or references that have not been verified against this
repository's code, data, or docs. Unverified claims are labelled **UNVERIFIED**
and resolved before use. A confident wrong answer is the worst outcome;
"I don't know, let's check" is always acceptable.

## Numbers and reporting
- Every number in any deliverable traces to a row in `results/metrics.csv`
  (D-016) or a committed results file, with an explicit **population label**
  (national / London / borough), unit, definition, and vintage.
- Non-trivial statistics get dual-method verification before publication.
- State data vintages wherever data is cited (IoD 2025 · Census 2021 ·
  Active Lives 2024/25 · Open Sessions 2026-06-30 frozen snapshot).
- References come from `docs/references.bib` only; new entries are
  `TODO-VERIFY` until a team member has read the source. Never invent a
  citation, DOI, page number, or URL.
- British English; formal academic register in deliverables.

## Data handling
- `data/raw/` is immutable — never edit, "fix", or hand-patch raw data; all
  transformations happen in pipeline code, reproducibly.
- **No imputation** (D-010). Missingness is characterised (MCAR/MAR/MNAR) and
  reported as a finding, never filled. Structurally-missing price → the
  `is_free` indicator; never impute price values.
- Absence of data is not absence of activity: OpenActive under-captures
  private/commercial provision, so provision measures are lower bounds — carry
  this caveat into every output that maps or ranks provision.
- Print and eyeball a sanity block for every artefact: row counts, value
  ranges, CRS, % missing per key field, duplicate count.
- `data/` is git-ignored and never committed; keep an off-GitHub backup of
  `data/raw/` current (data loss is not an exceptional circumstance).

## Geospatial
- Store coordinates in WGS84 (EPSG:4326); always reproject to British National
  Grid (EPSG:27700) before any distance, area, buffer, or catchment
  computation. Never compute distances in degrees.
- London = official ONS 2021 boundaries; **33 local authorities** (32 boroughs
  + City of London, E09000001). Assert the count in code and tests.
- Every geospatial operation is CRS-explicit.

## Statistics and modelling (per the decision log — do not deviate)
- Deterministic pipeline. Any randomness takes its seed from a single constant
  in `src/pipeline/config.py`.
- Unit of analysis: borough (D-008). Never disaggregate borough metrics.
- The need×provision **quadrant typology is the primary structural lens**;
  PCA is descriptive-only; t-SNE/UMAP are not used (D-010).
- **Activity-gap index:** standardised need minus standardised provision;
  log/rank-transform skewed indicators before standardising; report z-based and
  rank-based constructions; run weight sensitivity; City of London is excluded
  from standardisation parameters and receives no quadrant (undefined
  provision → `<NA>`).
- **Validation (D-012, strict):** validate only against held-out signals
  (Active Lives adult physical inactivity is the target). NEVER validate
  against deprivation or demographics — they are need inputs; using them is
  circular. Report coefficients with CI and n; note spatial autocorrelation.
- `pct_econ_inactive` (Census, need input) ≠ `pct_inactive_adults`
  (Active Lives, validation target). Never conflate them.
- The discovery prototype is deterministic filtering + content-based similarity
  + fairness re-ranking. It makes **no accuracy claims** (no interaction ground
  truth); evaluate only with beyond-accuracy metrics across the α sweep.

## Git and code
- Branch → PR → peer review → **squash-merge**; `main` is protected. Never
  push directly to main; never force-push; never rewrite shared history.
- One concern per PR; small diffs; no unrelated refactors.
- Every new or changed function: type hints, docstring, and a test. Spatial
  methods get toy-grid fixtures with hand-computed expected values.
- No new dependencies without team agreement; pin approved versions
  (`environment.yml` is the environment source of truth — regenerate all
  artefacts from the pinned `ls-openactive` environment).
- Run the test modules (and ruff) before declaring any task complete; CI
  enforces both on every PR.

## Tool-output discipline
- Numbers, code, and citations produced by any tool are never trusted
  unverified: dual-method checks for statistics, tests for code, human reading
  of every cited source before it leaves TODO-VERIFY status.
- Individual reflective accounts are written by their authors alone —
  structure advice at most, never drafting.
- No content is reused from any prior assessment (self-plagiarism).

## Ask before acting when…
a task is ambiguous; it touches schemas, thresholds, weightings, the validation
design, or deletes/moves files; or two reasonable approaches exist — present
both with trade-offs. One clarifying question beats a plausible guess.

## Definition of done (every task)
1. Plan stated and agreed before non-trivial work.
2. Code + tests written; tests pass; lint clean.
3. Sanity block printed and eyeballed.
4. Decision-log entry written if a methodological choice was made.
5. Closing summary: what changed, what was verified and how, and anything
   that remains UNVERIFIED.
