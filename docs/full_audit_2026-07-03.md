# Full end-to-end audit — repository, analysis, and outputs
**Date:** 3 July 2026 · **Scope:** all completed work (WS1 acquisition, WS2 analytical core, verification scripts, manifest, docs) · **Method:** line-by-line code review + cross-artefact reconciliation + independent hand recomputation where feasible. The sandbox was unavailable, so nothing was *executed* in this audit; execution checks are listed in §5.

**Verdict (calibrated, not a certification):** no critical defects found. The analytical core reproduces every headline claim from committed artefacts, the D-012 non-circularity design is correctly engineered and test-proven, and the statistics are correct by inspection and by known-answer tests. Findings: **3 Major, 5 Moderate, 7 Minor** — all fixable cheaply; none undermines a reported result.

---

## 1. What was VERIFIED (and how)

| Claim | How verified | Result |
|---|---|---|
| Priority top-10 (Enfield → Hillingdon) | `borough_gap_index.csv` read directly | Matches hand-off exactly |
| Weight sensitivity 0.976 / 0.952 | **Hand-recomputed** Spearman from the published rank columns (Σd² formula, n=32) | 0.97617 / 0.95161 — exact |
| gap = need − provision | Row-level identity on multiple boroughs | Holds (<1e-9) |
| D-013 statistics (partial ρ −0.498 p=0.0044; +0.363 p=0.0447; ΔR²=0.0704; F p=0.1096; Moran I=0.0807 z=0.937 p=0.349) | `reports/incremental_validity.csv` vs hand-off | All match |
| Held-out validation ρ=+0.459 | `spearman_gap_vs_inact = 0.4586` in the same file | Matches (rounding) |
| D-012 non-circularity | `gap_index.py` structure (inactivity absent from NEED_GROUPS) + `test_analysis.py` reversal proof (gap bit-identical) + validator guard (imd forbidden as anchor) | Correctly engineered AND tested |
| D-008 (33 boroughs) | features table has 33 rows; `run_pipeline` enforces count | Holds |
| IMD range 9.53–31.80; Hackney most deprived (avg score) | features table | 9.532–31.795; ordering Hackney > Newham > Haringey > TH > B&D — matches |
| Inactivity range 13.9–30.8; extremes | features table (proportions ×100) | Hillingdon .3081, B&D .3072, City .2964, Newham .2921, Brent .2837; Richmond/Kingston .139 — all match |
| Sessions per borough | features `n_sessions` vs `reports/sessions_per_borough_2026-06-30.csv` (independent joins) | Identical; sum = 494 |
| Statistical implementations (OLS, partial Spearman df=n−3, nested F, Moran variance) | Formula review + known-answer tests vs scikit-learn and hand-computed SE | Correct |
| Hard rules: no imputation, no t-SNE/UMAP, no seeds needed (fully deterministic), econ-vs-physical inactivity kept distinct, CRS reprojection before area/joins | Code inspection across all modules | Compliant |
| Open Sessions + event-harvest corrections (this week) | Dual-method recomputation (pandas + grep), identity checks, external corroboration | All numbers in `results/metrics.csv` (26 rows) verified |

## 2. MAJOR findings (fix before the report cites the affected numbers)

**M1 — Untraceable inferential statistics in circulation. [FIXED 2026-07-03]** `spearman_inference()` (Fisher-z CI + t/p, scipy-matched in tests) and the two missing Pearsons added to `incremental_validity.py`; regenerated. Outcomes: CI = **[0.131, 0.696]**, t=2.83, p=0.0083 (code-traceable; supersedes the hand-off's approximate "[0.12, 0.70]"); Pearson provision-vs-inactivity = **−0.311** (confirms the circulating figure exactly); **Pearson provision-vs-need = −0.111, NOT the −0.05 the hand-off quoted** — the near-orthogonality conclusion stands, but any document citing −0.05 must be corrected. Original finding: The hand-off/dossier quote **CI ≈ [0.12, 0.70], t≈2.83, p≈0.008** for ρ=0.459, a **Pearson −0.311** for provision-vs-inactivity, and **Pearson −0.05** for orthogonality. None of these is computed anywhere in the repo (`incremental_validity.py` computes Pearson only for need and gap; nothing computes a CI for the bivariate ρ). They are formula-plausible (Fisher-z reproduces the CI) but violate Rule Zero as they stand. *Fix:* add a small `validation_ci` step (Fisher-z + the planned bootstrap) and the two missing Pearsons to `incremental_validity.py`; regenerate; add manifest rows. Until then these specific numbers must not appear in any deliverable.

**M2 — The decision log still does not exist in the repo.** `docs/decision-log.md` is referenced by CLAUDE.md and multiple docs but is absent; D-001–D-006 live only in the old project knowledge, D-007+ only in the hand-off. This week proved mislabelled numbers thrive exactly where provenance is scattered. *Fix:* consolidate into `docs/decision-log.md` (needs the old `decisions.md` content from the Claude project), add D-015/D-016 and the D-014 reframe.

**M3 — Reproducibility/process gaps.** Requirements are unpinned; no `environment.yml`; no CI; branch protection not enabled; and all of this week's work (2 verification scripts, 3 docs, manifest, gap-index outputs) is **uncommitted**. CLAUDE.md's environment section is also stale (says "anaconda base, env not yet created" — the `ls-openactive` env exists and is in use). *Fix:* pin versions, commit via PR, enable protection + minimal CI (run the three test modules).

## 3. MODERATE findings

**Mo1 — City of London gets a spurious quadrant. [FIXED 2026-07-03]** `quadrant()` now returns `<NA>` for undefined scores (medians on fully-scored rows — also closes Mo4); NaN-provision test added; regenerated artefact verified (City row now NA). Original finding: With provision undefined (NaN), `quadrant()` still assigns City `low_low` (NaN comparisons collapse to False). Visible in `borough_gap_index.csv`; would mislead a dashboard choropleth. *Fix:* assign `pd.NA` where provision or need is NaN + a fixture with NaN provision (the current test's City has non-NaN provision, so this path is untested).

**Mo2 — `median_price` in the feature table includes free sessions** (B&D shows £0.00) — the same zeros-contamination this project just corrected in two other datasets. Unused downstream, but misleadingly named. *Fix:* compute paid-only median (and rename), or drop the column.

**Mo3 — `gap_pct_based` mixes denominators: [FIXED 2026-07-03]** both percentiles now rank the same fully-scored 32; hand-verified on Hillingdon (14/32 − 1/32 = 0.40625). Original finding: need percentiles rank 33 values (City included), provision percentiles rank 32. Ordering unaffected in current data; still inconsistent. *Fix:* mask City from both.

**Mo4 — [FIXED with Mo1] Quadrant medians include City on the need side** (median over 33 vs z-params over 32). Hand-checked: no borough's quadrant flips in current data (need median 0.110 vs 0.144 City-excluded; no borough sits between). Fix alongside Mo1/Mo3 for principle.

**Mo5 — `.gitignore` blanket `data/` line** (last line) makes the earlier `!.gitkeep` negations dead letters and silently ignores `data/external/` — including `SOURCES.md`, documentation that should arguably be versioned. *Fix:* remove the blanket line (the specific `data/raw/*`, `data/processed/*` rules suffice) and decide the status of `data/external/` docs.

## 4. MINOR findings

1. `config.py` comment calls the 06-30 sessions file "(latest)" — it is the **frozen** snapshot (a 2026-07-03 harvest exists). Reword to prevent an accidental "update".
2. CLAUDE.md drift nits: commands omit `tests.test_incremental_validity`; says `test_run.py` "asserts 33 boroughs" (it asserts 3 on fixtures; the 33-check is `run_pipeline`'s runtime status); `results/` now exists.
3. `run_pipeline` sanity block prints rows/cols/missingness but not value ranges or duplicate counts (CLAUDE.md's definition-of-done promises both).
4. `zscore` uses ddof=0 — fine and deterministic, but undocumented; state it (ranks unaffected).
5. `load_geography`'s filename-independent fallback globs `*.geojson` alphabetically — a stray non-LAD file in `data/raw/boundaries/` would be picked up (the 33-count check downstream would catch it).
6. Notebook filename `data_audit().ipynb` contains `()` — awkward for shells/tools; rename.
7. Outputs split between `reports/` and `results/` — pick one convention (suggest: `results/` for machine-readable metrics, `reports/` for figures/rendered tables) and document it.

## 5. Execution checks (cannot be done by inspection — run these)

```bash
conda activate ls-openactive
python -m tests.test_run
python -m tests.test_analysis
python -m tests.test_incremental_validity
python -m src.run_pipeline      # regeneration stability: diff borough_features.csv after
python -m src.run_analysis      # diff borough_gap_index.csv after
```
Expected: all assertions pass; regenerated outputs identical to the committed ones (the pipeline is deterministic). Any diff = a finding.

**Execution results (2026-07-03, Michael, env `ls-openactive`):**
- `test_analysis` PASS (incl. the D-012 reversal proof); `test_incremental_validity` PASS.
- `run_analysis` regenerated `borough_gap_index.csv` with values identical to the audited file (top-10, 0.976/0.952, ρ=0.459) — **WS2 regeneration determinism confirmed by execution**.
- `test_run` and `run_pipeline` initially FAILED: `ModuleNotFoundError: openpyxl` — the dedicated env was missing a dependency listed in requirements.txt (M3 evidenced: earlier pipeline runs used the base env). Remediated: openpyxl 3.1.5 installed via conda-forge; **both then PASSED** (33 rows; fixture assertions green).
- **Regeneration diff:** all analytical columns byte-identical; the ONLY drift is `area_km2` at the 4th–5th significant figure (~10⁻⁵ relative) on every row — a **cross-environment geodesy-stack effect** (committed file built in the base env, rerun in `ls-openactive`; different PROJ/GEOS versions reproject EPSG:27700 microscopically differently). `area_km2` is used by nothing downstream; the gap index, validation and all reported numbers are unaffected (confirmed: `run_analysis` reproduced ρ=0.459 and the full ranking exactly). Consequence: M3 upgraded from "risk" to "observed" — pin the environment (`environment.yml` from `ls-openactive`) and regenerate all artefacts from that single env; within-env double-run determinism check added to the execution list.
- **Within-env double run: IDENTICAL** (byte-level) — pipeline determinism confirmed by execution. `run_analysis` re-reproduced ρ=0.459 and the full ranking from the refreshed features. `environment.yml` exported from `ls-openactive` (commit it; regenerate everything from this env from now on). Execution section: **CLOSED** — 3/3 test suites pass, determinism proven, drift quarantined.

## 6. Not yet built (roadmap items, not defects)
PCA (descriptive-only), bootstrap CIs (subsumes M1), Active Places + PTAL acquisition, E2SFCA (conditional), WS3 recommender + honest evaluation, WS4 dashboard, report skeleton, literature review, CI/branch protection, four-eyes re-derivation of manifest numbers (Fahmi).

---
*Audit performed under the project's integrity rules: findings over reassurance; verified/unverified separated; no certification of perfection — the verdict is "no critical defects found in what exists", which is not a statement about what is still to be built.*
