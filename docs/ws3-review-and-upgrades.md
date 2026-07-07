# WS3 build — review record & upgrade pack
> **ROUND 3 (2026-07-07): REVIEW CLOSED — zero findings.** The decisive gate passed: full suite (43/43) under `python -W error::DeprecationWarning` on **pyproj 3.7.1** — the exact environment that failed round 2. The geo rewrite transforms origin+points in one array call (no scalar ever reaches the transformer — version-independent by construction) and is proven **value-neutral**: the golden trace is byte-identical to round 2's and regenerates exactly on the reviewer's stack. E5 is implemented end-to-end: pool policy recorded with the panel decision date, `'Tai Chi'`/`'Swimming'` verified verbatim against the catalogue (thin pools are provision findings, not string artefacts), transparent degradation noted in results and **asserted by test** (including the negative case). Ruff clean, vocabulary clean. Remaining items are process, not code: the five PRs from Clarence's machine, Fahmi's §5 sign-off gating PR 4, then harness → `ws3.*` manifest rows → report §6.
**Status:** adversarial review PASSED (2026-07-07) · **Reviewer artefact** — this document is the review record (committed by the reviewer); **every change below is applied and committed by Clarence, on his machine, in his branches**, per spec §6 ("these commits are Clarence's assessed contribution evidence").
**Review evidence:** 20/20 tests pass · ruff clean · banned-vocabulary scan clean · real-artefact run clean (494 rows, 79 activity types, 0 contract violations) · four unclaimed properties verified externally: input-order invariance, P2 monotone traversal on real data, equity isolation under filtering (≤1e-12), borough-vs-row gap bounds numerically identical today.

---

## A. Required fixes (fold into PR 1)

**A1 — `geo.py` future-breaking deprecation (the one real bug).**
```python
x0, y0 = _TRANSFORMER.transform(float(origin_lon), float(origin_lat))
xs, ys = _TRANSFORMER.transform(
    np.atleast_1d(np.asarray(lons, dtype=float)),
    np.atleast_1d(np.asarray(lats, dtype=float)),
)
```
Done means: `python -W error::DeprecationWarning -m pytest tests/ -q` passes (it currently fails under the flag).

**A2 — `relevance.profile_vector`: replace the `assert` with an explicit raise** (asserts vanish under `-O`):
```python
if profile.preferred_price_gbp is None:
    raise ValueError("include_price=True requires preferred_price_gbp on the profile.")
```

**A3 (optional tidy) — `ranking.recommend`:** the `positions` dict is an identity mapping; use `idx` directly.

## B. Ratifications (land with PR 3)

**B1 — Explicit borough-level gap bounds** (letter-compliance with spec §3.3; numerically identical today, verified):
```python
gap = pd.read_csv("data/processed/borough_gap_index.csv")
prepared = prepare_catalogue(df, gap_bounds=(gap.gap_index_z.min(), gap.gap_index_z.max()))
```

**B2 — Decision-log entry (paste, adjust number):**
> **D-0NN — WS3 implementation choices (Clarence).** Price encoded as a complementary pair (1−p, p): under cosine a single scaled dimension makes cheap-preference invisible. Proximity decay exp(−d/τ), τ = 5 km default. Affordability threshold £5 **placeholder pending Fahmi** (it also defines affordable-share@k). Underserved component scaled with explicit borough-level gap bounds (§3.3). Endpoint lexicographic tie-breaks per spec P1. cosine implemented in numpy (hand-checkable) — scikit-learn permitted but unnecessary.

**B3 — E1/Enfield preview note:** whatever behaviour was previewed against expectation E1, write it into the PR 3 description, dated, BEFORE the harness exists. Deviations are findings (spec §5c); the timestamp is what keeps the pre-registration honest.

## C. Upgrade set — the remaining headroom (hardening + evidence, not features)

**U1 — Metamorphic invariant suite (the flagship; PR 3, no new dependencies).**
WS3's defining condition — no ground truth — is the classic *test-oracle problem*; metamorphic relations are the literature's answer to exactly that (Chen et al. 2018, ACM CSUR — TODO-VERIFY). You cannot test "are recommendations right?", but you CAN test necessary relations that must hold for ANY input. Implement as parameterised loops over a deterministic grid of synthetic catalogues × personas × α (hand-rolled; Hypothesis would be a new dep — don't, unless the team agrees):
- **MR1 input-order invariance:** shuffled catalogue (fixed seeds from config) ⇒ identical ranked id lists.
- **MR2 filter monotonicity:** adding any active filter never enlarges the candidate set.
- **MR3 equity isolation:** for surviving ids, equity values identical pre/post any filter.
- **MR4 monotone traversal (P2, executable):** Σrelevance non-decreasing and Σequity non-increasing in α, every grid point.
- **MR5 endpoint dominance (P1, executable):** at α=1 no excluded candidate has strictly higher relevance than any included one (with the lexicographic tie-break honoured); mirrored at α=0 for equity.
- **MR6 clone insertion:** duplicating a session under a fresh id never changes the relative order of other items, and the clone ranks adjacent to its original (total-order tie-break check).
- **MR7 irrelevant-field perturbation:** changing `name`/`organizer` strings changes nothing in scores or order.
Report line this buys: *"beyond example-based tests, the ranker satisfies seven metamorphic invariants across a systematic input grid — the appropriate testing standard for a system whose outputs have no oracle."* That sentence is rare in MSc work.

**U2 — Golden-trace regression artefact (PR 3).** Commit the canonical worked example: `python -m src.recommender.demo --csv … > results/ws3_demo_trace.txt`; add a test asserting byte-equality against the committed file. Protects the report's §3.5 exhibit from silent drift, and makes the trace itself regenerable (D-016 spirit).

**U3 — Edge-behaviour table (PR 3 docstring + report §6).** Four rows, already implemented and tested — make them visible: empty candidate set → empty result + note; all-tie relevance → 0.5 + note; missing gap score → zero underserved contribution, counted; price == threshold → affordable (boundary inclusive). Defensive code becomes examinable rigour only when documented.

**U4 — Micro-benchmark + complexity paragraph (PR 3).** One timed run (494 rows, per-query cost), one sentence: per-query work is O(n·(|V|+3)) — linear in catalogue size; extrapolate to the ~1,600-series national platform trivially. Pre-empts the "would this scale?" viva question with a measured number.

**U5 — API freeze for the harness (PR 3 → unblocks PR 4).** Declare `__all__` and a ten-line interface contract (what `prepare_catalogue`/`recommend`/`sweep` promise) so Fahmi's harness builds against a stable surface.

**U6 — Persona-pool sanity report (with sign-off).** One command printing candidate counts per draft persona: catches near-empty pools before evaluation (P3's 5 km around Havering is a real risk — outer-borough provision is thin). Feeds the Clarence+Fahmi sign-off checklist.

**U7 — Forward notes for Fahmi's harness (PR 4, his design):** report candidate-pool sizes (denominators) beside every metric; bootstrap-over-personas intervals for ablation deltas; expect steppy metric-vs-α curves (α=0 and 0.25 produced identical lists on a real query — plateaus are normal with scaled components, not bugs).

## D. Do NOT do
No rewrite (the build is verified; rewrites trade evidence for fresh bugs). No learned components, no α optimisation, no user study (spec §1 refusals). No new dependencies without team agreement — including test libraries; the grid approach above needs none. No edits to spec §5c expectations, especially E1, now that behaviour has been previewed.

## E. PR mapping
PR 1: A1 + A2 (+A3) with the deprecation-flag test · PR 2: as sliced (relevance tests) · PR 3: B1–B3, U1–U5 · PR 4 (after Fahmi's §5 sign-off + threshold): harness + U6/U7 · PR 5: results tables/figures + `ws3.*` manifest rows per D-016.

## F. References for the report (TODO-VERIFY until a team member has read them)
Chen, T.Y. et al. (2018) 'Metamorphic testing: a review of challenges and opportunities', *ACM Computing Surveys*, 51(1) · Claessen, K. & Hughes, J. (2000) 'QuickCheck: a lightweight tool for random testing of Haskell programs', *ICFP* (property-based testing origin) · plus the §5 anchors already logged (Kaminskas & Bridge 2016; Herlocker et al. 2004; Burke 2017; Liu & Burke 2018).
