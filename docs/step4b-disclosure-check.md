# Step 4b — disclosure spot-check (the single highest-risk review)

**Done:** 2026-08-12 · source: `packages/application-contracts/c-block-05/disclosure-classes.json`
(52 classified fields) · method: audited every field against the rule *only `PUBLIC_SAFE` may ever
reach the public plane*, cross-checked the two schemas' `x-release-class` annotations, and traced the
two riskiest into the running app. `INV-DISCLOSURE`/`INV-NONINTERFERENCE` enforce the projection
*given* these classes — they cannot tell you a class is **mis-assigned**, which is what this review is for.

## Headline

The canonical high-risk checklist **passes 100%** — no receipts, lineage, scores, verifier outcomes,
versions or research identity are exposed. But a full field-by-field scan found **one live over-share
to fix (`failed_stage`)** and **three items to confirm with Michael/Wesley before freeze.** The
fail-closed default (`default_unlisted_field: DROP`) means the only way to leak is to *actively* mark
a field `PUBLIC_SAFE`, so the review concentrates on the ~30 fields that are.

## Canonical checklist — all correct

**Must NOT be `PUBLIC_SAFE` (verified restricted):**

| Field | Class in file | ✓ |
|---|---|---|
| `candidates[].internal_score` | STAFF_AGGREGATE | ✓ |
| `predicates[]/attributes[].receipts[].receipt_id`,`content_digest` | STAFF_EVIDENCE | ✓ |
| `predicates[]/attributes[].lineage_note` | STAFF_EVIDENCE | ✓ |
| `why_not[].predicate_id`,`blocking_state` | STAFF_EVIDENCE | ✓ |
| `versions.model_version`,`policy_version` | STAFF_AGGREGATE | ✓ |
| `claims[].verification`,`receipt_ids[]` | STAFF_EVIDENCE | ✓ |
| `episode_id`,`trace_id` (header + identity) | RESEARCH_RESTRICTED | ✓ |
| `coarsened_origin` | STAFF_AGGREGATE | ✓ |

**Must BE `PUBLIC_SAFE` (verified present):** `terminal_decision`, `scope_qualifier`,
`recommendation_action`, `coverage_qualifier.statement`, candidate `candidate_id`/`rank`/`pool`,
predicate `evidence_state`/`mechanism`/`grade`, `digest`, `vintage` — all ✓. Nice touches worth
keeping: `coarsened_origin` is *both* coarsened and staff-only; `coverage_qualifier` shows the *fact*
of incompleteness publicly but keeps `unevaluated_feeds` staff; `why_not.relaxation_suggestion` is
public while the internal `predicate_id`/`blocking_state` are staff.

## Findings from the full scan

### F1 — `payload.failed_stage` = PUBLIC_SAFE → **CHANGE (live over-share)**
- **Evidence:** `disclosure-classes.json:56` classes it PUBLIC_SAFE; `server/render.py:59` copies it into
  the public view; `templates/service_failure.html:6` renders *"A component ({{ v.failed_stage }})
  didn't respond"* — with the fixture that prints **"A component (retrieval) didn't respond."**
- **Issue:** the public plane names an internal pipeline stage (`retrieval`, `verifier`, …). That's
  architecture detail the public interface should not reveal, and it contradicts the intended honest-
  but-opaque failure message ("something went wrong; we won't show a stale result").
- **Recommend:** reclass `failed_stage` → **STAFF_AGGREGATE**; public template shows only the generic
  message + `safe_next`. Owner: Clarence (template is my UI); the class change is joint at the workshop.
- **Status (2026-08-12): FIXED in code** — reclassed to `STAFF_AGGREGATE` in `disclosure-classes.json`
  + the schema annotation; `service_failure.html` no longer names the stage; `render.py` stops copying
  it; regression guard added (`failed_stage` in `test_slice.py` `LEAK_KEYS`). Invariants + slice test
  re-run green. The *class* flip still needs joint ratification with Michael/Wesley at the freeze.

### F2 — `payload.budget_state.budget` (and `.asked`) = PUBLIC_SAFE → **CHANGE / confirm**
- **Evidence:** `application-envelope.schema.json:132-139` — `budget_state{asked,budget}` under the
  clarification envelope; `barrier_floor` description says "regardless of **EVOI**"; sibling
  `policy_id` is STAFF_AGGREGATE.
- **Issue:** `budget` is the **EVOI question-budget** (a policy parameter), not the user's price
  budget — so exposing it publicly leaks a policy internal, inconsistent with `policy_id` being staff.
- **Recommend:** `budget` → **STAFF_AGGREGATE**; keep `asked` public only if the UI needs "question 1
  of N", else also STAFF_AGGREGATE. Confirm the field's meaning with Michael.

### F3 — `predicate_id` public in `predicates[]`/`attributes[]` but STAFF_EVIDENCE in `why_not[]` → **confirm intent**
- **Evidence:** lines 80, 90 (PUBLIC_SAFE) vs line 99 (STAFF_EVIDENCE).
- **Issue:** same field name, opposite class. It's *likely* deliberate — a predicate shown *as
  evidence to the user* is public; the same id used *to justify an exclusion* is internal — but a
  reviewer must confirm, not assume. If the id strings themselves are internal vocabulary, even the
  evidence-facing ones may need a public label distinct from the raw id.
- **Recommend:** confirm the split with Michael; if kept, document why in the schema.

### F4 — provenance versions PUBLIC_SAFE while `model`/`policy` restricted → **confirm intent**
- **Evidence:** `corpus_version`, `interpretation_version`, `search_horizon_version`,
  `verifier_version`, `vintage` are PUBLIC_SAFE (lines 67-73); `model_version`/`policy_version` staff.
- **Issue:** exposing data/interpretation/verifier versions supports reproducibility, but also reveals
  internal versioning cadence. Defensible either way — needs an explicit decision.
- **Recommend:** confirm with Michael (semantics) + Wesley (what transport should expose).

## Record for the C-BLOCK-05 workshop (feeds 4c)

**Confirm with Michael (evidence semantics):** F2 (is `budget` the EVOI budget?), F3 (`predicate_id`
context split), F4 (which provenance versions are public).
**Confirm with Wesley (transport/exposure):** F4 (version exposure), and that the role gate enforces
these classes server-side.
**Done in code (2026-08-12):** F1 — `failed_stage` reclassed to STAFF_AGGREGATE and the public failure
page no longer names the stage (class flip still needs joint ratification at the freeze).

## Bottom line

The disclosure matrix is **sound on everything that would be a serious leak** (receipts, scores,
lineage, verifier outcomes, identity). The gap is at the *edges* — a failure-page string that names an
internal stage (fix it) and three intentional-looking asymmetries that must be confirmed, not assumed,
before you freeze the contract with Michael and Wesley. That's exactly what 4b is meant to surface.
