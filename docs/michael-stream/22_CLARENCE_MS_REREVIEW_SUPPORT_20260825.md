# MS-1..MS-9 re-review support — Clarence's fixes at `7cf65ca`

**Date:** 25 August 2026 · **Prepared for:** Michael's re-review (the signoff entries are yours to complete)
**Object:** worktree `.review/clarence-7cf65ca` (branch `clarence/c-block-05`; commit `7cf65ca`, message "fix WY-1/WY-2/WY-3/WY-11 (Wesley review) with adversarial tests")
**Provenance:** AI-assisted mechanical verification; PROPOSED; signs nothing.

## 0. Orientation — three facts that frame the re-review

1. **The findings register at `7cf65ca` (`docs/assurance/michael-review-findings.md`) matches Clarence's email exactly:** six findings marked "FIXED — pending Michael re-review" (MS-1, 3, 6, 7, 8, 9), four OPEN as joint §09 work (MS-2, 4, 5, and MS-10 explicitly "reclassified — deferred to the joint session"). Your original review commit is recorded there as **`9b0807d`** — that is the pre-fix baseline for the negative leg.
2. **`7cf65ca` itself is a Wesley-fixes commit** (WY-1/2/3/11); the MS fixes are in its ancestry. Clarence cited the branch state, which is fine — the re-review binds to the tree at `7cf65ca` as he asked. Note the branch tip has since moved on (`fe982e5 → 2b92cd5` in your fetch); anything after `7cf65ca` is outside this re-review.
3. **Cross-team texture worth 10 seconds:** Wesley reviewed Clarence's block too (WY findings; `docs/reviews/wesley-review-c-block-05.md`), his WY-11 finding is the same environment-pinning lesson as our lock-file defect family (requirements.txt now pins jsonschema/fastapi with a note that without them "the certificate checker fails closed indiscriminately"), and Clarence's repo carries a draft `team-ratification-agenda.md` and LaTeX report-section drafts — useful inputs for the meeting and the group report.

## 1. Positive leg — executed in a clean cloud environment (this session)

| Suite | Result | Covers |
|---|---|---|
| `packages/certificate-checker/test_certificate_checker.py` | **PASS** (umbrella test: golden + negative battery incl. `_schema_extra_field` MS-3, `_bad_transition` MS-6, `_incompatible_decision` + `_caller_asserted_checker` MS-7, `_empty_allowed_versions` WY-3) | MS-3, 6, 7, 8 |
| `apps/public-discovery/test_slice.py` | **PASS** (incl. the MS-1 case: a claim with `verification:"failed"` and value `SECRET-UNVERIFIED` planted, then asserted absent from the public projection) | MS-1 |
| `apps/public-discovery/test_conversation.py` | **PASS** (umbrella `run()==0` over the four MS-9 cases) | MS-9 |
| `apps/staff-assurance/test_staff.py` | **PASS** | context |

Environment note: reproducing this required staging the full dependency closure (packages/security, accessible-design-system content, evaluation manifest, app templates) — the suites are runnable but the repo has no conftest; tests self-hack `sys.path`. Harmless, worth one tidy-up line to Clarence eventually.

## 2. Hostile read — fix by fix (verdicts are PROPOSED, within AI scope)

**MS-1 (projection drops non-verified claim tuples) — holds.** `render._drop_unverified_claims` removes every claim whose `verification != "verified"` *before* `proj.project` runs; a claim with a **missing** verification field is also dropped (fail-closed), and `load_public` returns `{}` when the projector says DROP. The remaining attribute-side question is exactly MS-10 and is correctly left OPEN for §09.

**MS-3 (runtime schema enforcement) — holds, and does double duty.** `_c_schema` is the *first* check in the ordered list: Draft 2020-12 validation of the certificate against `certificate.schema.json` (root `additionalProperties:false`), plus structural validation of the context (receipt store, manifest keys, expected query/digest). If jsonschema is missing or the schema file is unreadable it refuses to certify rather than skipping. One design interlock worth stating in your entry: **the soundness of the MS-7 version check depends on this schema running first** — `versions` requires all five keys (`corpus/interpretation/schema/verifier/checker_version`, no extras), which is what prevents a certificate from *omitting* a version key to dodge `_c_version`'s pin loop. The interlock is correct as built; suggest Clarence add a one-line comment in `_c_version` noting the dependency so a future schema edit can't silently break it.

**MS-6 (state transitions) — holds.** `_c_transition` fails closed when the manifest declares no `allowed_transitions`, and requires an exact from/to pair match; the schema also makes `state_transition` mandatory with both fields.

**MS-7 (decision combos + checker identity) — holds.** `_ALLOWED_DECISION_ACTIONS` is a closed table (e.g. `authorised_slate` only under `supported_match`); unknown terminals get an empty allowed-set and fail. `CHECKER_VERSION = "chk-1.0"` is compared by hard equality against the certificate's declared `checker_version` — a caller-asserted different checker fails, and WY-3's addition also fails empty or partial `allowed_versions` maps.

**MS-8 (no empty-checks bypass) — holds.** Public `check(cert, ctx)` takes no checks parameter; `_run_checks` with an empty list returns `FAIL_MALFORMED` ("refusing to certify"), and any exception inside a check returns `FAIL_MALFORMED` instead of an accidental PASS. Residual observation, not a defect: `_run_checks` remains importable and could be called directly with a reduced list — unavoidable in Python, documented as internal-only, and outside the finding as written.

**MS-9 (conversation constraints) — holds.** Negations ("not/no/without/non … step-free/wheelchair/accessible", up to two intervening words) set access to None and are surfaced as `unsupported` — never reversed. Price ceilings are detected (£N / "under £N" / "N pounds") and surfaced as `unsupported`, never dropped. `confident` requires zero unsupported items, so both route to clarification. The injection case is closed structurally: scenarios resolve **only** when the user actually asked for step-free, so "climbing in Havering" now yields a clarification question rather than an answer to a step-free query the user never posed. Residual nit (safe): the single word "inaccessible" isn't matched by the negation pattern — it falls through to access=None and a clarification, which is a safe outcome, but Clarence could add it to the pattern for completeness.

## 3. Negative leg — COMPLETE (executed 25 Aug, cloud replay of the `9b0807d` worktree)

Three results, together closing the "would have caught it" question for all six findings:

1. **The pre-fix suites at `9b0807d` are green-but-blind:** the old checker, slice and conversation suites all pass as-is — exactly what your original review recorded ("supplied tests all pass; adversarial review nevertheless exposed release-blocking gaps").
2. **The exploits reproduce against the pre-fix checker.** Feeding the old checker (public signature `check(cert, ctx, checks=None)`) the new adversarial mutations returns **PASS** in every case: schema-extra-field (MS-3) → PASS; bad state transition (MS-6) → PASS; incompatible decision combination (MS-7) → PASS; caller-asserted checker version (MS-7) → PASS; and the literal bypass `check(cert, ctx, checks=[])` → **PASS** (MS-8). Every one of these returns a FAIL code or is impossible at `7cf65ca`.
3. **The new tests fail loudly on the old code.** Transplanting the `7cf65ca` test files onto the `9b0807d` implementations: the checker suite fails (it probes the removed `_run_checks`/no-override contract), the slice suite fails (`render._drop_unverified_claims` absent — MS-1 fix missing), and the conversation suite fails (`KeyError: 'unsupported'` — the old parser has no unsupported-constraint surface at all, MS-9 fix missing).

Positive leg (§1) + hostile read (§2) + this negative leg = the full evidence base for your six signoff entries. Within AI-verification scope, all six fixes stand; the APPROVED/RETURNED decision on each is yours.

## 4. Draft signoff entries (paste into `docs/assurance/signoffs.md` after the negative leg; sign only what you accept)

The file's own format is Claim/artefacts/method/outcome/conditions/not-covered/signed. One entry per finding, per your rule. Template per finding — fill MS-3/6/7/8 with the checker paths and MS-1/9 with the app paths:

> - **Finding:** MS-<n> — <finding wording from michael-review-findings.md>
> - **Artefacts checked:** <implementation file + function>, <test file :: case name> — branch `clarence/c-block-05`, commit `7cf65ca`
> - **Method:** re-ran the suite at `7cf65ca` (pass) and at the reviewed baseline `9b0807d` (adversarial case fails/absent); hostile read of the fix for bypasses (record: none found / plus the observation below)
> - **Outcome:** _[Michael — APPROVED / APPROVED WITH CONDITIONS / RETURNED]_
> - **Conditions / observations:** _[e.g. MS-3↔MS-7 schema-interlock comment; MS-9 "inaccessible" pattern nit — non-blocking]_
> - **Not covered:** MS-2/4/5/10 (joint §09 work), RATIFY-09-04/05 (authority), anything after `7cf65ca`
> - **Signed:** _Michael Samuel · [date]_

## 5. What this does NOT do

No signoff entry is made by this memo; no finding flips to APPROVED; RATIFY-09-04/05 remain blank; MS-2/4/5/10 remain OPEN for the joint session (your CA-2 position on the author/validator split is already recorded in the findings file and should become the text of RATIFY-09-04). The re-review outcome is yours after the negative leg completes.
