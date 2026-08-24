# Wesley — review of C-BLOCK-05: versioning, disclosure enforcement, IAM stub, app security

**Reviewer:** Wesley · **Date:** 2026-08-24
**Commit reviewed:** `e390072` (branch `clarence/c-block-05`)
**Scope requested:** transport/versioning, server-side disclosure enforcement, the IAM path
(`RATIFY-15-06`), and the application-facing security controls in `packages/security/`.
**Outcome: REVIEWED WITH BLOCKING CONDITIONS — not approved. `RATIFY-15-06` not issued.**

Every supplied test passes on this commit (contract invariant battery 8/8; certificate checker
golden + negatives + mutation; public slice; staff slice; security validator). Adversarial testing
nevertheless found four release-blocking defects the supplied tests do not reach — three of them
**fail-open defaults inside controls the assurance case relies on**, and one control that exists as a
library but is never called by either application.

> **On the security sign-off:** `RATIFY-15-07` is **not mine to issue** and this document does not
> issue it. See [§6](#6-sign-off-routing).

---

## 1. Verdict per question

| # | Question | Verdict |
|---|---|---|
| 1 | Version/compatibility rules and fail-closed behaviour on stale or incompatible releases | **Partly. Incompatible is caught; stale is not caught at all, and two fail-open paths exist.** WY-3, WY-4, WY-5 |
| 2 | Are the field-level disclosure classes enforceable server-side? | **Yes — and they are actually enforced.** The strongest part of this block. Caveat WY-8 |
| 3 | Plan to replace the role-gate stub with real auth/IAM | **Not yet a plan — an owner and a placeholder.** The stub also fails open today. WY-1 |
| 4 | Application-facing security controls | **Register and validator are honest; the sanitisers are not wired in.** WY-2, WY-7 |

---

## 2. What is genuinely solid

Stated plainly, because it should carry into the report:

- **Server-side projection is real, not aspirational.** Both apps import the reference projector
  (`apps/*/server/render.py` → `projection_and_invariants.project`) and build every view from its
  output. `load_public()` returns the public projection and nothing else; `/api/envelope` serves that
  same projection. There is no path in either app that renders a raw envelope.
- **Fail-closed default-drop works under adversarial input.** I injected three undeclared fields at
  three different depths (`payload.decision.operator_private_note`, `header.undeclared_debug_blob`,
  `candidates[].undeclared_internal_flag`) into `supported.json` and served the app: all three were
  dropped, and all thirteen declared `STAFF_*`/`RESEARCH_RESTRICTED` fields I checked for were absent
  from the public output.
- **The MS-1 fix is right.** Dropping the whole claim tuple rather than the `verification` field is
  the correct reading — field-class projection alone would have left the unverified subject/predicate
  /value visible.
- **The certificate checker is well built.** `check()` has no caller override, an empty check set
  refuses to certify, any exception becomes `FAIL_MALFORMED`, `checker_version` is not
  caller-assertable, and the mutation harness kills every branch. With `jsonschema` present the whole
  suite passes.
- **The role gate is applied consistently.** All eleven staff endpoints call `_role()` and return 403
  on a missing/invalid role; the six *modelled* transitions enforce separation of duties correctly
  (analyst cannot review, assurance cannot send).
- **The threat register is honest** where it matters most — `dos_cost_abuse`, `deletion_withdrawal_
  failure` are `planned`, not oversold. That is rarer than it sounds.

---

## 3. Findings

Severity is against the claims in the assurance case, not against the live demo — the demo persists
nothing, so none of these is currently exploitable for real harm. They are blocking because **CL-1,
CL-5 and CL-13 assert properties that do not currently hold.**

### WY-1 — BLOCKING — the action-card capability gate fails open (CL-5, CL-13)

`apps/staff-assurance/server/main.py:56` — `_cap_for()` returns `"view"` for any `(from, to)` pair not
in `TRANSITION_CAPABILITY`, and **every role holds `view`**. `/action-card/perform` also never checks
that the requested pair is a transition the state machine permits: it takes `frm` and `to` straight
from the query string.

Reproduced on `e390072`:

```
role=analyst  observed        -> sent_by_authorised_role  cap=view  200  "Transition permitted"
role=analyst  drafted         -> approved_for_route       cap=view  200  "Transition permitted"
role=analyst  anything_at_all -> sent_by_authorised_role  cap=view  200  "Transition permitted"
```

An `analyst` is told it may send. This contradicts, in terms:

- `docs/applications/staff-information-architecture.md` §5 — "The `/action-card/perform` route
  enforces this (403 when the role lacks the capability)" and "Actions never bypass the action-card
  gates";
- the passing staff check *"action-card no-skip (review+approval+authorised-role enforced)"*, which
  only inspects the transitions `render.action_card(state)` **offers**, never the ones the endpoint
  **accepts**;
- threat `malicious_staff_action`, whose control is this gate.

The route mutates nothing today, so there is no live impact — but the demonstration is the artefact
under review, and it currently renders "Transition permitted" for a straight jump to send.

**Fix (small):** default-deny in `_cap_for` (return a capability no role holds), and reject any
`(frm, to)` absent from `packages/staff-ia/action-card-state-machine.json` with 403. Add a test that
asserts an *unmodelled* pair is refused — the current test suite cannot fail on this.

### WY-2 — BLOCKING — the sanitisers are never called (CL-13)

`safe_url()`, `csv_field()` and `escape_html()` have **zero call sites outside `packages/security/`**.
`render.build_view` passes `provider_link` through untouched (`apps/public-discovery/server/render.py:97`)
and both templates interpolate it directly into `href`:

```jinja
<a class="button" href="{{ c.provider_link }}" rel="nofollow noopener">Go to provider</a>
```

Jinja autoescaping does not stop a `javascript:` URI — it escapes the quotes, not the scheme. I set
one candidate's `provider_link` to `javascript:alert(document.domain)` and the app rendered it as a
live link:

```
hrefs rendered by /discover: 'javascript:alert(document.domain)'
                             'https://example.org/sessions/102'
safe_url() on the same value: '' (blocked)
```

`provider_link_scan()` in `validate_security.py` *did* catch it — but that is a **build-time scan of
the four committed demo fixtures**, not a control on the request path. Once links come from real
OpenActive publisher feeds, as planned, it protects nothing. The threat register nonetheless records
`unsafe_html_url` as `mitigated` with "template autoescaping + `safe_url()` scheme allow-list" as the
control.

**Fix (small):** call `safe_url()` in `build_view` (or register it as a Jinja filter and use it in
both templates); keep the fixture scan as defence in depth. Then `mitigated` is true.

### WY-3 — BLOCKING — `allowed_versions: {}` fails open in the release gate (CL-1)

`packages/certificate-checker/certificate_checker.py:136` — `_c_version` iterates
`manifest["allowed_versions"]`. `_c_schema` requires the key to be *present*, not non-empty, so an
empty map means no version is pinned and the certificate **passes**:

```
manifest allowed_versions = {}
cert versions = corpus_version 'H1-2019-01-01', interpretation_version 'interp-0.0.1-broken'
-> ('PASS', 'certificate verified against witness, receipts, versions and scope')
```

Omitting a single key has the same effect for that key: deleting `corpus_version` from the manifest
made a 2019 corpus pass. The control case is the giveaway — `certifiable_fragment: []` fails **closed**
(`FAIL_UNSUPPORTED_FRAGMENT`). The two empty-collection cases behave in opposite directions.

**Fix (small):** in `_c_schema`, require `allowed_versions` to be a non-empty object covering every key
present in `cert["versions"]`; treat a missing pin as `FAIL_VERSION_MISMATCH`, not as a waiver.

### WY-4 — BLOCKING — nothing in the block expires (CL-1)

Compatibility is exact-string identity throughout. There is no freshness bound anywhere in
`packages/application-contracts/c-block-05/` or the checker: no `not_after`, no max-age, no
comparison of `versions.vintage` against anything. `frozen_vintage: 2026-06-30` binds evaluation
tasks to one vintage (`validate_conditions.py`), which is a *consistency* control, not a *staleness*
one — it would equally happily pin everything to a vintage two years old.

So the honest answer to the question as asked is: **incompatible releases are rejected; stale
releases are not a concept the contracts can express.** `staleness` exists as a per-predicate
`mechanism` label, and `stale_content_reused` is a structural `const: false` on the failure path —
neither bounds the age of a release.

**Fix:** add an explicit freshness bound to the release manifest (`max_vintage_age_days` or
`not_after`) and a `FAIL_STALE_RELEASE` outcome, or state in the C-BLOCK-05 record that staleness is
deliberately out of contract scope and carried operationally. Either is defensible; silence is not.

### WY-5 — the applications run no version gate at all

Neither app reads `header.schema_version` or `header.compatible_release_version` before rendering.
`load_public()` projects and renders whatever envelope it is handed. The contract declares the
fields, `disclosure-classes.json` classifies them `PUBLIC_SAFE`, and no code on the request path ever
compares them to a supported range. Fail-closed behaviour on an incompatible envelope exists only in
the checker, which the apps do not call.

**Fix:** a supported-version check at envelope load, returning the existing `service_failure` page on
mismatch. That is also the natural place for WY-4's freshness bound.

### WY-6 — a documented agreement check does not exist

`packages/application-contracts/c-block-05/README.md` states that the schemas' `x-release-class`
annotations "mirror it and are checked for agreement by `projection_and_invariants.py`". There is no
such check in that file — nothing prevents the schemas and the class map drifting apart.

I wrote the check and ran it: **93 annotations against 83 mapped fields, 0 disagreements.** The
deltas are container nodes (objects/arrays), which the projector classifies structurally rather than
by leaf class, so they are not leaks. So this is drift risk, not a live defect — but the README
currently claims a guarantee the code does not provide.

**Fix:** add the agreement check to the battery (~15 lines), or correct the README.

### WY-7 — the secret scan is much weaker than it reads (CL-13)

`validate_security.py` reports `secret scan (clean)`. That conclusion is correct — but I would not
rely on the instrument:

- **`SCAN_EXT` is an extension allow-list, so every extensionless file is skipped.**
  `os.path.splitext(".env")` → `('.env', '')`, so `.env` is never opened. Nor are `Dockerfile`,
  `id_rsa`, `credentials`, `.npmrc`, `.pypirc`.
- **The patterns miss most real credential formats.** Of eleven realistic samples placed in a
  *scanned* file, three were caught (AWS `AKIA`, quoted `password = "…"`, PEM header) and eight were
  missed: GitHub PAT `ghp_…`, Slack `xoxb-…`, Google `AIza…`, OpenAI-style `sk-…`, a JWT, unquoted
  `key=value`, a credential-bearing `postgres://user:pass@host` URL, and any quoted value containing
  a `.` (the charset excludes it).
- **Working tree only** — a secret committed and later removed stays in history, unseen.

Mitigating: `.gitignore` covers `.env` and `*.key`. And the repository really is clean — I ran an
independent sweep over **every** file with no extension filter, plus the last 40 commits of this
branch, using a much broader pattern set: **0 hits.**

**Fix:** run `gitleaks` or `detect-secrets` in CI (or enable GitHub secret scanning) against history,
not the working tree, and keep this script as the fast local smoke test — describing it as such.

### WY-8 — field classes protect fields, not content (residual risk, CL-1/CL-5)

The disclosure model classifies *where* a value sits, so staff information written into a
`PUBLIC_SAFE` field is published. `INV-DISCLOSURE` is the only content-level check, and it is a
known-bad regex (`lineage|receipt|superEvent|STAFF:|`postcode). Text that dodges it passes:

```
claims[].value = "internal ref 8931; provenance chain r-a1; escalate to ops"
served to the public: True
INV-DISCLOSURE verdict:  (True, 'public plane clean')
```

`INV-DISCLOSURE` also runs only in the battery — not on the request path — so at runtime nothing
checks content at all.

I do not think projection can fix this, and I am not asking for it to. **Record it as a named
residual risk on CL-1/CL-5** ("field-level classes do not constrain content placed in a correctly
classified field; mitigated by contract discipline upstream, not by the projector"), so the assurance
case does not read as claiming more than it delivers.

### WY-9 — no security headers; role in the URL; state-change over GET

Neither app sets `Content-Security-Policy`, `Referrer-Policy`, `X-Frame-Options` or HSTS. The demo
`?role=` parameter puts the privilege in the URL, so it reaches browser history, server logs, and the
`Referer` header on any outbound `provider_link` click. `/action-card/perform` is a `GET` with no CSRF
token.

All are harmless in a stateless local demo and all are correctly flagged as mine (Section 16). Listing
them so they are on the record before anything is hosted: **none of these may survive contact with a
real deployment**, and `?role=` must not outlive the stub.

### WY-10 — empty containers are dropped, not preserved

`project()` returns `DROP` for an empty dict/list, so `claims: []` — "we evaluated and found none" —
becomes indistinguishable from "not evaluated" in the public projection, and changes the sealed
digest. Minor, but it interacts with the coverage/abstention semantics this block is built on.

### WY-11 — `jsonschema` is missing from `requirements.txt`

`requirements.txt` lists pandas, numpy, scikit-learn, matplotlib, jupyter, requests. `jsonschema` —
which `_c_schema` needs — appears only in a parenthesis in `docs/RUN-apps.md`. In the environment
`requirements.txt` describes, the checker fails **closed**, which is correct, but *indiscriminately*:
every negative case collapses to `FAIL_MALFORMED`, so the WP §10.3 outcome vocabulary is unusable and
the mutation evidence does not run. The suite reports **24 failures and 10 surviving mutants** in a
clean environment, and **ALL CHECKER TESTS PASS** once `jsonschema` is installed.

**Fix:** pin `jsonschema` (and `fastapi`, `jinja2`, `uvicorn`, `httpx`) in `requirements.txt`, or add
`requirements-apps.txt`. The Phase B exit evidence should not depend on an undeclared dependency.

---

## 4. The IAM question (`RATIFY-15-06`)

**There is not yet a plan to review — there is an owner and a placeholder.** Everything I can find
resolves to "real IAM is Wesley's (Section 16, C-BLOCK-04)". `C-BLOCK-04` — *who holds the Section 15
operational authorities* — is itself still `PROPOSED` in the reconciliation register, so the security
authority has not been named either.

What exists is the role→capability matrix, which is the **authorisation** half and is a reasonable
starting shape: three roles, capability-per-transition, no single role able to draft, approve and send.
Keep it. What `RATIFY-15-06` needs before it can be issued:

1. **Authentication and identity binding.** The role is currently caller-asserted in a header or query
   parameter with no identity behind it. Until a request carries an authenticated principal, "role"
   is a rendering hint, not access control.
2. **Person-level independence (reviewer ≠ author).** Capabilities cannot express this — two people
   both holding `assurance` is not the same as the reviewer not being the author. This is already
   flagged as outstanding in the staff IA and it is the substantive half of WP §8.5.
3. **An audit log.** Nothing records who performed a transition. Separation of duties that cannot be
   evidenced after the fact is not evidence.
4. **Session management, break-glass and revocation**, with break-glass use itself audited.
5. **Purpose binding** — the register's own framing that access is not granted "merely because the
   user is staff".
6. **WY-1 fixed in the stub first.** The real IAM will inherit `TRANSITION_CAPABILITY`; a fail-open
   default must not be what it inherits.

Given (1)–(6), `RATIFY-15-06` cannot be issued on this commit, and `docs/step9-signoff-tracker.md`
already says so: CL-5 unlocks on "security/IAM review (**real IAM replaces the stub**)". The stub has
not been replaced. Marking it now would be exactly the backfill that document forbids.

I would rather agree the target design first (I will draft it against `C-BLOCK-04`), because
`RATIFY-15-06` should ratify a design, not a promise.

---

## 5. Suggested threat-register corrections

| id | now | should be | why |
|---|---|---|---|
| `authorization` | `mitigated` | `partial` | no authentication behind the role; capability gate fails open (WY-1) |
| `unsafe_html_url` | `mitigated` | `partial` | `safe_url()` is never called on the render path (WY-2) |
| `spreadsheet_formula_injection` | `mitigated` | `partial` | `csv_field()` has no call site; there is no export surface yet |
| `receipt_forgery_version` | `mitigated` | `partial` | version pinning is waivable by an empty manifest map (WY-3); no staleness bound (WY-4) |
| `malicious_staff_action` | `partial` | `partial` (unchanged) | correct already — but its control is the gate WY-1 bypasses |

`validate_security.py` accepts any of `mitigated`/`partial`/`planned`, so these are one-word edits.

---

## 6. Sign-off routing

**`RATIFY-15-07` is not mine.** The repository's own governance says so in three places:

- `docs/step9-signoff-tracker.md` — CL-13's eligible signer is "security reviewer (`RATIFY-15-07`)",
  distinct from CL-5's "Wesley (`RATIFY-15-06`)"; and its closing note: *"Everything else is an
  institutional authority (ethics, DPIA, **security**, Section 08 owner) … you cannot self-sign them."*
- `docs/step3-assurance-map.md` — "Security reviewer (`RATIFY-15-07`) | CL-13 | **institutional**".
- `docs/assurance/signoff-requests.md` — request **#2** to Wesley covers versioning, disclosure and
  IAM; request **#8**, to a separate "Security / assurance reviewer", covers `packages/security/`
  and `RATIFY-15-07`.

The message I received merged #2 and #8. I have reviewed all four areas — the findings above stand
either way and should go to whoever holds #8 — but the `RATIFY-15-07` *outcome* has to be issued by
that reviewer, and `C-BLOCK-04` needs to name them first.

**What this document is:** a `REVIEWED` entry with open blocking findings on CL-1 and CL-5. Per the
ledger's own rule, that does **not** flip a claim to AUTHORISED. Recorded in
`docs/assurance/signoffs.md`; `assurance-case.json` updated to `reviewer.status = conditions` for
CL-5, authority still `pending`. CL-13 left untouched — not mine to move.

---

## 7. What I would fix first

WY-1, WY-2 and WY-3 are each a few lines and each turns a currently-false assurance claim into a true
one. WY-11 is a one-line dependency pin that makes the Phase B evidence reproducible. Those four are
worth doing before the report freeze; WY-4/WY-5 need a short design conversation; the rest can be
recorded and scheduled. Happy to patch WY-1/WY-2/WY-3/WY-11 myself if that is faster — say the word.
