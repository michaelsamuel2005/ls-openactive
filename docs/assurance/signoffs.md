# Sign-off ledger

Canonical, **append-only** record of human sign-offs behind the assurance case. Format and rules per
Fahmi Alshahabi's evaluation-stream template. One entry per claim, appended, never edited after
signing. If a claim changes, add a new dated entry rather than amending the old one.

A claim is flipped to AUTHORISED in `assurance-case.json` **only** when a completed, signed entry
appears below with a real commit SHA, a real date, and an outcome of APPROVED / APPROVED WITH
CONDITIONS. `REVIEWED`-only or entries with open blocking findings do **not** flip a claim.

---

## Template

```
## SIGN-OFF — [claim or gate name]
- Claim ID:
- Claim wording (as seen):
- Artefacts checked: [file paths] — branch `[branch]`, commit `[SHA]`
- Method: [what you read, what you ran, what output you saw]
- Outcome: REVIEWED / APPROVED / APPROVED WITH CONDITIONS
- Conditions: [if any]
- Not covered by this sign-off: [findings still open, and anything outside scope]
- Reference: RATIFY-XX-XX
- Signed: [name] · [YYYY-MM-DD]
```

## Rules (Fahmi Alshahabi)
1. **Commit SHA, not branch name.** A sign-off is against a state, not a moving branch.
2. **Method must be reproducible.** "Reviewed" is not a method; "read X against my 18 Aug review; ran
   `Y.py`, exit 0" is. This is the field the oral defence draws on.
3. **Always fill "not covered".** An unscoped sign-off reads as covering everything.
4. **Never sign on someone's description of their own work.** Check the artefact.
5. **Never sign a claim you have not seen the wording of.**
6. Sign findings **individually**, not "the review is addressed".

---

# Signed entries

## SIGN-OFF — evaluation-parity gate (condition manifest)
- **Claim ID:** CL-7
- **Artefacts checked:** packages/evaluation/condition-manifest.json,
  packages/evaluation/fahmi-review-response.md, packages/evaluation/validate_conditions.py,
  packages/evaluation/event-schema.json — branch clarence/c-block-05, commit ea8f5bd
- **Method:** read fahmi-review-response.md against my F-12 review of 18 August 2026; ran
  `python packages/evaluation/validate_conditions.py` (exit 0); inspected event-schema.json directly
  for the opening-query digest field and version
- **Outcome:** REVIEWED — M-1 (task count), M-3 (repair minting), M-4 (origin/publisher keys) and
  M-5 (vintage binding) accepted as addressed on this commit. This does NOT authorise CL-7.
- **Conditions:** CL-7 remains unauthorised until M-6 is closed and M-2's referent is verified against
  the evidence engine.
- **Not covered by this sign-off:**
  - M-6 — STILL OPEN on ea8f5bd. `envelope_digest` is present in event-schema.json but is not in
    `required`, and the schema version remains 0.1.0-PROPOSED. Until it is required and versioned, the
    F-BLOCK-09 mechanical repair screen cannot run and the opening-query digest is not recoverable
    after the fact.
  - M-2 — OPEN. Shared terminal referent must be produced and verified by the evidence engine rather
    than true by construction. Not closable from the manifest; recorded as a locked-run precondition.
  - Any HCI, usability, actionability or application-effectiveness claim.
- **Reference:** RATIFY-14-07/08
- **Signed:** Fahmi Alshahabi · 2026-08-23

_Recorded in `assurance-case.json`: CL-7 reviewer = done (Fahmi Alshahabi, 2026-08-23, REVIEWED);
authority = pending (RATIFY-14-07/08 withheld pending M-6 + M-2). **CL-7 remains BLOCKED.**_

## SIGN-OFF — M-6 closure (event-schema opening-query digest)
- **Claim ID:** CL-7 (follow-up to entry of 2026-08-23)
- **Artefacts checked:** packages/evaluation/event-schema.json,
  packages/evaluation/validate_conditions.py — branch clarence/c-block-05, commit 21c788b
- **Method:** inspected event-schema.json directly — `envelope_digest` present in `required`, version
  0.2.0-PROPOSED; ran validate_conditions.py (exit 0)
- **Outcome:** REVIEWED — M-6 closed on this commit
- **Conditions:** CL-7 remains unauthorised. M-2 stays open.
- **Not covered by this sign-off:**
  - M-2 — shared terminal referent produced and verified by the evidence engine. Open until the engine runs.
  - Any HCI, usability, actionability or application-effectiveness claim.
- **Reference:** RATIFY-14-07/08
- **Signed:** Fahmi Alshahabi · 2026-08-23

_Recorded in `assurance-case.json`: M-6 CLOSED; CL-7 authority still pending — sole remaining blocker
is M-2 (evidence engine). **CL-7 remains BLOCKED.**_

## SIGN-OFF — application-facing evidence contract, checker & conversation route
- **Claim ID:** CL-1, CL-3, CL-6, CL-14
- **Artefacts checked:** `packages/application-contracts/c-block-05/`, `packages/certificate-checker/`,
  `apps/public-discovery/` (conversation route) — branch clarence/c-block-05, commit `9b0807d`
- **Method:** ran the application-contract invariant battery, `test_certificate_checker.py` (golden +
  13 negative + 8 mutation) and `test_conversation.py` — all supplied tests pass; then additional
  adversarial review
- **Outcome:** REVIEWED WITH BLOCKING CONDITIONS — **NOT approved.**
- **Conditions:** findings MS-1…MS-10 (see `docs/assurance/michael-review-findings.md`) must be fixed,
  each with the adversarial test that would have caught it, then re-reviewed at the successor commit.
- **Not covered by this sign-off:**
  - `RATIFY-09-04` (production/reference/checker ownership + independence) and `RATIFY-09-05` (claim
    vocabulary + rendering obligations) — **not recorded** (register fields blank).
  - Section 09 spec is proposed, not ratified (SHA-256 `48828408b1e93d6284022fec4618e52128363d35951a9d656613941c68d2133e`).
  - Any HCI/accessibility, evaluation or effectiveness claim.
- **CA-2 position:** claim-contract author may also author the production interpreter only if the
  contract is jointly frozen and independently reviewed; the reference interpreter has a different
  owner; the checker remains independently authored and reviewed.
- **Reference:** RATIFY-09-04, RATIFY-09-05 (both blank)
- **Signed:** Michael Samuel · 2026-08-23

_Recorded in `assurance-case.json`: CL-1, CL-3, CL-6, CL-14 reviewer = `conditions` (Michael Samuel,
2026-08-23, REVIEWED WITH BLOCKING CONDITIONS); authority pending. **All four remain BLOCKED** — and
these are open defects, not just missing signatures._

## SIGN-OFF — transport/versioning, server-side disclosure enforcement & the IAM path
- **Claim ID:** CL-5 (primary); CL-1 (transport/versioning half)
- **Claim wording (as seen):** CL-5 — "Restricted staff information cannot leak to the public plane;
  staff access is role-gated." CL-1 — "Public and staff surfaces never disagree on the retained
  decision, and restricted staff values cannot change public output."
- **Artefacts checked:** `packages/application-contracts/c-block-05/` (schemas,
  `disclosure-classes.json`, `projection_and_invariants.py`, fixtures),
  `packages/certificate-checker/certificate_checker.py`, `packages/security/`,
  `apps/public-discovery/server/{main,render}.py`, `apps/staff-assurance/server/{main,render}.py`,
  `packages/staff-ia/action-card-state-machine.json` — branch `clarence/c-block-05`, commit `e390072`
- **Method:** ran `projection_and_invariants.py` (8/8 expectations met);
  `test_certificate_checker.py` (fails in the `requirements.txt` environment — 24 failures, 10
  surviving mutants, no `jsonschema`; ALL PASS once `jsonschema` is installed);
  `apps/public-discovery/test_slice.py`, `apps/staff-assurance/test_staff.py`,
  `packages/security/validate_security.py` (all pass). Then adversarial testing beyond the supplied
  suites, via `fastapi.testclient` against both apps and direct calls into the checker:
  (a) injected three undeclared fields at three depths into `supported.json` and read
  `/api/envelope` — all dropped, all 13 declared staff/research fields absent;
  (b) set a candidate `provider_link` to `javascript:alert(document.domain)` and read the rendered
  `href` — served live;
  (c) requested unmodelled `(frm,to)` pairs on `/action-card/perform` as `analyst`;
  (d) ran the checker with `allowed_versions: {}` and with individual pins removed;
  (e) placed regex-dodging staff text in a `PUBLIC_SAFE` field and re-ran `INV-DISCLOSURE`;
  (f) wrote and ran the schema-annotation/class-map agreement check the README describes;
  (g) swept every file with no extension filter, plus the last 40 commits, for credentials.
  Full detail and reproductions: `docs/reviews/wesley-review-c-block-05.md`.
- **Outcome:** **REVIEWED WITH BLOCKING CONDITIONS — not approved.** Server-side disclosure
  enforcement is confirmed and holds under adversarial input (question 2: yes). Four release-blocking
  defects found that the supplied tests do not reach — WY-1 (action-card capability gate fails open:
  an `analyst` is granted `observed -> sent_by_authorised_role`), WY-2 (`safe_url()`/`csv_field()`/
  `escape_html()` have no call sites; a `javascript:` provider link renders live), WY-3
  (`allowed_versions: {}` waives version pinning and returns PASS on a 2019 corpus), WY-4 (no
  staleness bound exists anywhere in the block). These are open defects, not missing signatures.
- **Conditions:** CL-5 and CL-1 remain unauthorised. WY-1, WY-2 and WY-3 fixed and re-reviewed;
  WY-4/WY-5 resolved by design decision (bound release freshness, or record staleness as out of
  contract scope); WY-11 dependency pin so the Phase B evidence reproduces.
- **Not covered by this sign-off:**
  - **`RATIFY-15-06` — NOT ISSUED.** CL-5 unlocks on "real IAM replaces the stub"; the stub has not
    been replaced. Authentication, identity binding, person-level independence (reviewer ≠ author),
    audit, session/break-glass/revocation and purpose binding are all still absent — see §4 of the
    review. `C-BLOCK-04` (who holds the Section 15 authorities) is itself still PROPOSED.
  - **`RATIFY-15-07` / CL-13 — NOT MINE TO ISSUE** and not issued here. The security review outcome
    belongs to the institutional security/assurance reviewer (`step9-signoff-tracker.md`,
    `step3-assurance-map.md`, `signoff-requests.md` #8). My `packages/security/` findings (WY-2, WY-7,
    WY-9 and the register corrections in §5) are supplied *to* that reviewer, not in place of them.
  - Infrastructure controls (rate limits, security headers, egress, SBOM, deletion) — mine under
    Section 16, none of them built yet; recorded as WY-9.
  - WY-8 — field classes constrain *where* a value sits, not *what* is written into a correctly
    classified field. Named as a residual risk on CL-1/CL-5; not fixable by projection.
  - Any evidence-semantics, HCI/accessibility, evaluation or effectiveness claim. MS-2, MS-4 and MS-5
    from Michael's review remain open and are unaffected by this entry.
- **Reference:** RATIFY-15-06 — **not issued** (IAM path not yet agreed; design to be drafted against
  C-BLOCK-04). RATIFY-15-07 — routed to the security/assurance reviewer, unassigned pending C-BLOCK-04.
- **Signed:** Wesley · 2026-08-24

_Recorded in `assurance-case.json`: CL-5 reviewer = `conditions` (Wesley, 2026-08-24, REVIEWED WITH
BLOCKING CONDITIONS); authority = pending (RATIFY-15-06 withheld — real IAM does not yet exist).
CL-1 reviewer note extended with the transport/versioning half. CL-13 untouched — not mine to move.
**CL-1, CL-5 and CL-13 all remain BLOCKED**, and WY-1..WY-4 are open defects, not missing signatures._

## SIGN-OFF — WY-1/WY-2/WY-3/WY-11 closure (re-review)
- **Claim ID:** CL-5 (primary); CL-1 (transport/versioning half) — follow-up to entry of 2026-08-24
- **Artefacts checked:** `apps/staff-assurance/server/main.py`,
  `apps/public-discovery/server/render.py`, `packages/certificate-checker/certificate_checker.py`,
  `requirements.txt`, `packages/staff-ia/action-card-state-machine.json`,
  `packages/certificate-checker/certificate.schema.json`,
  `apps/public-discovery/client/src/{enhance.ts,compare.tsx,types.ts}`,
  `packages/security/threat-register.json`, `docs/reviews/wesley-review-response.md` — branch
  `clarence/c-block-05`, commit `7cf65ca` (branch head `ca74024` is docs-only, so this is the head's
  code state)
- **Method:** re-ran the exact reproductions from my 2026-08-24 review against `7cf65ca`, not the
  diff. (a) the four unmodelled `(frm,to)` pairs on `/action-card/perform` as `analyst`, plus seven
  modelled transitions across all three roles as controls, plus a set-comparison of
  `TRANSITION_CAPABILITY` against the state machine's declared transitions; (b) `provider_link` set
  to `javascript:alert(document.domain)` read back from `/discover`, the detail page **and**
  `/api/envelope`, and traced whether the enhancement client renders it; (c) the empty and partial
  `allowed_versions` cases, plus golden/genuine-mismatch/null/omitted-key controls, plus a check of
  whether the manifest-pins-an-absent-key path is reachable given `_c_schema` ordering; (d) built a
  clean virtualenv from the new `requirements.txt` block alone and ran all five suites in it, and
  simulated a `jsonschema` ImportError to confirm the degradation path is unchanged. All supplied
  suites and all eight validators green at `7cf65ca`.
- **Outcome:** **REVIEWED — WY-1, WY-3 and WY-11 CLOSED on this commit; WY-2 closed on the reported
  path.** All four unmodelled transitions now 403 with no over-correction (capability table and state
  machine are in exact 15/15 bijection); both `allowed_versions` cases now `FAIL_VERSION_MISMATCH`
  with genuine mismatches still detected; the Phase B evidence reproduces from a clean install
  (checker suite ALL PASS, previously 24 failures / 10 surviving mutants). This does **not** authorise
  CL-5 or CL-1.
- **Conditions:** CL-1 and CL-5 remain unauthorised. WY-2a (below) folded into the WY-4/WY-5 design
  session; WY-4, WY-5, WY-6, WY-9, WY-10 open as dispositioned in `wesley-review-response.md`.
- **Not covered by this sign-off:**
  - **WY-2a — NEW, open.** `safe_url()` is wired into `render.build_view` (the SSR path) but
    `/api/envelope` returns `render.load_public(...)`, which does not pass through it — the JSON
    contract boundary still emits `javascript:alert(document.domain)`. Not exploitable today
    (`compare.tsx` never renders `provider_link`), but `client/src/types.ts` declares that field as
    part of the public contract boundary, so the next consumer inherits an unsanitised URL. One line:
    sanitise in `load_public()` so both exits inherit it.
  - **WY-3a — NEW, open (very low).** `_c_version` skips `checker_version` in the manifest loop.
    Correct as far as MS-7 goes, but a manifest pinning a *different* checker version (or omitting it)
    is silently tolerated and `PASS`es — a release/tooling mismatch that goes unreported.
  - **`RATIFY-15-06` — STILL NOT ISSUED.** The fixes improve the stub; they do not make it real IAM.
    CL-5's unlock condition ("real IAM replaces the stub") is unchanged, and authentication, identity
    binding, reviewer≠author, audit, session/break-glass/revocation and purpose binding are all still
    absent. To be drafted against C-BLOCK-04 and ratified at the team meeting.
  - **`RATIFY-15-07` / CL-13 — still not mine to issue.** WY-7 and the threat-register corrections —
    restated against `7cf65ca` in the re-review section of `wesley-review-c-block-05.md`, since two of
    my original reasons have changed — travel to the institutional security reviewer. The register was
    not modified by `7cf65ca`; `authorization`, `unsafe_html_url`, `spreadsheet_formula_injection` and
    `receipt_forgery_version` all still read `mitigated` and in my view should read `partial`.
  - WY-8 residual risk unchanged; infrastructure controls (Section 16) unchanged and unbuilt.
  - Any evidence-semantics, HCI/accessibility, evaluation or effectiveness claim. MS-2, MS-4 and MS-5
    from Michael's review are unaffected by this entry.
- **Reference:** RATIFY-15-06 — **not issued**. RATIFY-15-07 — routed, not mine.
- **Signed:** Wesley · 2026-08-24

_Recorded in `assurance-case.json`: CL-5 reviewer stays `conditions` (Wesley, 2026-08-24), outcome
updated to note WY-1/WY-2/WY-3/WY-11 closed at `7cf65ca` with WY-2a/WY-3a opened; authority still
`pending`. **CL-1, CL-5 and CL-13 all remain BLOCKED** — WY-4/WY-5 need the design decision and CL-5
needs real IAM._

---

# Pending entries (prepared for the signer — NOT yet signed, NOT yet recorded)

> The judgment fields (Method output, Outcome, Conditions, Signed/date) are the signer's to complete.
> Only the objectively-checkable scaffolding is pre-filled, pinned to commit `ea8f5bd`.

## (SUPERSEDED — signed 2026-08-23, see "Signed entries" above) evaluation-parity gate — CL-7 scaffold
- **Claim ID:** CL-7
- **Claim wording (as seen):** "Application effects are not confounded with retrieval, ranking or
  content differences."
- **Artefacts checked:** `packages/evaluation/condition-manifest.json`,
  `packages/evaluation/fahmi-review-response.md`, `packages/evaluation/validate_conditions.py`,
  `packages/evaluation/event-schema.json` — branch `clarence/c-block-05`, commit `ea8f5bd`
- **Method:** _[Fahmi to complete]_ — suggested: read `fahmi-review-response.md` against the F-12
  review of 18 Aug 2026; run `python packages/evaluation/validate_conditions.py` and record the exit
  code you observe; inspect `event-schema.json` for the opening-query envelope-digest field.
- **Outcome:** _[Fahmi — REVIEWED / APPROVED / APPROVED WITH CONDITIONS]_
- **Conditions:** _[Fahmi]_
- **Not covered by this sign-off:**
  - **M-6** — opening-query envelope digest in `event-schema.json`. **Current factual state on
    `ea8f5bd`:** field `envelope_digest` is present but **NOT in `required`**, and
    `event_schema_version` is `0.1.0-PROPOSED` (not bumped). Appears **OPEN** — Fahmi to verify.
  - **M-2** — shared terminal referent produced and verified rather than true by construction. Not
    closable from the manifest; a locked-run precondition pending the evidence engine. **OPEN.**
  - Any HCI, usability, actionability or application-effectiveness claim.
- **Reference:** RATIFY-14-07/08
- **Signed:** _Fahmi Alshahabi · [YYYY-MM-DD]_

**Recording note:** because M-6 and M-2 are open, a completed sign-off here would most likely read
`REVIEWED` (findings M-1/M-3/M-4/M-5 addressed), which does **not** flip CL-7 to AUTHORISED. CL-7
clears only when M-6 is closed (make `envelope_digest` `required` and bump the schema version) and
M-2's shared referent is produced and verified by the evidence engine.

### Re-review — MS-1 (CL-3)

- **Finding:** MS-1 — Unverified claims survive public projection: failed verification status is removed while the claim content remains.
- **Artefacts checked:** `apps/public-discovery/server/render.py` (`_drop_unverified_claims`, called in `load_public` before projection); adversarial case in `apps/public-discovery/test_slice.py` — branch `clarence/c-block-05`, commit `7cf65ca`.
- **Method:** suite re-run at `7cf65ca` in a clean environment (pass; the planted `verification:"failed"` claim carrying `SECRET-UNVERIFIED` does not survive projection). At the reviewed baseline `9b0807d` the fix is absent (`render._drop_unverified_claims` does not exist; the transplanted test fails). Hostile read: a claim with a *missing* verification field is also dropped (fail-closed); the remaining attribute-side question is MS-10, correctly left open.
- **Outcome:** APPROVED
- **Conditions:** none.
- **Not covered:** MS-10 (attribute↔claim binding — joint §09); any commit after `7cf65ca`.
- **Signed:** Michael Samuel · 2026-08-26

### Re-review — MS-3 (CL-6)

- **Finding:** MS-3 — The checker does not enforce its own JSON Schema — schema-invalid certificates can return PASS.
- **Artefacts checked:** `packages/certificate-checker/certificate_checker.py` (`_c_schema`, first in the ordered `CHECKS`); `certificate.schema.json` (root `additionalProperties:false`; `versions` requires all five keys); negative case `_schema_extra_field` in `test_certificate_checker.py` — commit `7cf65ca`.
- **Method:** suite re-run at `7cf65ca` (pass). Exploit reproduced at `9b0807d`: a certificate with an extra field returns **PASS** on the pre-fix checker; returns FAIL_MALFORMED at `7cf65ca`. Hostile read: fail-closed when jsonschema is missing or the schema file is unreadable; context structure also validated.
- **Outcome:** APPROVED WITH CONDITIONS
- **Conditions:** add a one-line comment in `_c_version` noting that its per-key pin loop is sound because `_c_schema` runs first and the schema requires the complete `versions` key set — so a future schema edit cannot silently reopen the omit-a-version-key path.
- **Not covered:** MS-2/4/5 (joint §09); RATIFY-09-04/05.
- **Signed:** Michael Samuel · 2026-08-26

### Re-review — MS-6 (CL-6)

- **Finding:** MS-6 — State transitions are not checked.
- **Artefacts checked:** `certificate_checker.py` (`_c_transition` against manifest `allowed_transitions`); negative case `_bad_transition` — commit `7cf65ca`.
- **Method:** suite re-run at `7cf65ca` (pass). Exploit reproduced at `9b0807d`: a forbidden transition (`…→ results_leak`) returns **PASS** on the pre-fix checker; fails at `7cf65ca`. Hostile read: a manifest that omits `allowed_transitions` refuses to certify (fail-closed); the schema makes `state_transition` mandatory with both fields.
- **Outcome:** APPROVED
- **Conditions:** none.
- **Not covered:** as MS-3.
- **Signed:** Michael Samuel · 2026-08-26

### Re-review — MS-7 (CL-6)

- **Finding:** MS-7 — The checker accepts incompatible decision combinations and caller-asserted checker versions.
- **Artefacts checked:** `certificate_checker.py` (`_ALLOWED_DECISION_ACTIONS` closed table; `_c_decision_consistency`; `_c_version` hard-equality against this checker's own `CHECKER_VERSION = "chk-1.0"`); negative cases `_incompatible_decision`, `_caller_asserted_checker` — commit `7cf65ca`.
- **Method:** suite re-run at `7cf65ca` (pass). Both exploits reproduced at `9b0807d`: an `authorised_slate` under `evidence_indeterminate`, and a caller-asserted `checker_version` matching a doctored manifest, each return **PASS** on the pre-fix checker; both fail at `7cf65ca`. Hostile read: unknown terminal decisions yield an empty allowed-set and fail; WY-3's addition also rejects empty or partial `allowed_versions` maps.
- **Outcome:** APPROVED WITH CONDITIONS
- **Conditions:** shares the single MS-3 condition (the `_c_schema`↔`_c_version` interlock comment); no separate action.
- **Not covered:** as MS-3.
- **Signed:** Michael Samuel · 2026-08-26

### Re-review — MS-8 (CL-6)

- **Finding:** MS-8 — `check(..., checks=[])` bypasses every check and returns PASS.
- **Artefacts checked:** `certificate_checker.py` (public `check(cert, ctx)` with no override parameter; `_run_checks` fail-closed on an empty list and on exceptions) — commit `7cf65ca`.
- **Method:** bypass reproduced at `9b0807d`: the pre-fix public signature is `check(cert, ctx, checks=None)` and `check(cert, ctx, checks=[])` returns **PASS**. At `7cf65ca` the public API has no such parameter, `_run_checks([])` returns FAIL_MALFORMED ("refusing to certify"), and any in-check exception returns FAIL_MALFORMED rather than an accidental PASS.
- **Outcome:** APPROVED
- **Conditions:** none. Observation for the record, no action: `_run_checks` remains importable as a private function (unavoidable in Python); it is documented internal-only and outside the finding as written.
- **Not covered:** as MS-3.
- **Signed:** Michael Samuel · 2026-08-26

### Re-review — MS-9 (CL-14)

- **Finding:** MS-9 — Conversation route silently ignores or reverses constraints (price ignored; unrequested step-free added; negated accessibility read as requiring step-free).
- **Artefacts checked:** `apps/public-discovery/server/intent.py` (`NEG_ACCESS_RE`, `PRICE_RE`, `unsupported` surface, scenario resolution only when step-free was actually requested); four adversarial cases in `test_conversation.py` — commit `7cf65ca`.
- **Method:** suite re-run at `7cf65ca` (pass). At `9b0807d` the fix is provably absent: the pre-fix parser has no `unsupported` surface at all (transplanted suite fails on `KeyError: 'unsupported'`). Hostile read: negations set access to None and are surfaced, never reversed; prices surface as unsupported, never dropped; `confident` requires zero unsupported items, so both route to clarification; the injection case is closed structurally (scenarios resolve only when step-free was requested).
- **Outcome:** APPROVED WITH CONDITIONS
- **Conditions:** add the single word "inaccessible" to the negation pattern (currently it falls through to a safe clarification rather than a reversal — fail-safe, but incomplete).
- **Not covered:** RATIFY-09-05 (claim vocabulary and rendering obligations); the complete-decision-digest comparison requirement in your condition 6 remains part of the §09 joint work.
- **Signed:** Michael Samuel · 2026-08-26

