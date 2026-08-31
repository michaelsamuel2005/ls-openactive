# Response to Wesley's C-BLOCK-05 review

**Reviewer:** Wesley (2026-08-24, commit `e390072`) · **Disposition by:** Clarence
**Full review:** `docs/reviews/wesley-review-c-block-05.md`

Wesley's "fix first" set (WY-1, WY-2, WY-3, WY-11) is done, each with the adversarial test that would
have caught it. All suites green; nothing flips to AUTHORISED — CL-1/CL-5/CL-13 stay BLOCKED pending
Wesley's re-review and the outstanding items.

| # | Finding | Disposition | What changed | Test |
|---|---------|-------------|--------------|------|
| WY-1 | action-card capability gate fails open (`_cap_for` defaults to `view`; endpoint doesn't check the pair) | **FIXED — pending re-review** | `_cap_for` defaults to a `__deny__` sentinel no role holds; `/action-card/perform` rejects any `(frm,to)` not in `TRANSITION_CAPABILITY` | `test_staff.py`: analyst `observed→sent_by_authorised_role` = 403 |
| WY-2 | sanitisers never called; `javascript:` provider link renders live | **FIXED — pending re-review** | `safe_url()` wired into `render.build_view` on `provider_link` | `test_slice.py`: `javascript:` link sanitised to empty |
| WY-3 | empty/partial `allowed_versions` waives version pinning (2019 corpus PASSes) | **FIXED — pending re-review** | `_c_version` fails closed on an empty map and on any unpinned declared version key | `test_certificate_checker.py`: `empty_allowed_versions`, `unpinned_version_key` |
| WY-11 | `jsonschema` (and app deps) missing from `requirements.txt`; checker fails closed indiscriminately | **FIXED — pending re-review** | pinned `jsonschema`, `fastapi`, `jinja2`, `uvicorn`, `httpx` | reproduction: the Phase-B suites now import + pass from a clean install |
| WY-4 | no staleness bound anywhere; compatibility is exact-match only | **OPEN — design decision (joint)** | add a freshness bound (`max_vintage_age_days`/`not_after`) to the release manifest, or record staleness as out of contract scope | at the §09/§16 session |
| WY-5 | the applications run no version gate before rendering | **OPEN — design** | supported-version check at envelope load → existing `service_failure` page; natural home for WY-4's bound | with WY-4 |
| WY-6 | a documented schema/class-map agreement check does not exist | **OPEN — scheduled** | add the agreement check to the contract battery (~15 lines) or correct the README | — |
| WY-7 | secret scan skips extensionless files, misses realistic formats | **ROUTED to the security reviewer (#8)** — not Clarence's to close | recommend `gitleaks`/`detect-secrets` over history in CI | belongs to `RATIFY-15-07` |
| WY-8 | field classes protect *where* a value sits, not *what* is written into a correctly-classified field | **RESIDUAL RISK (CL-1/CL-5)** — not fixable by projection | recorded as a named residual risk | — |
| WY-9 | no security headers; role in URL; state-change over GET | **OPEN — split** | headers/egress are Wesley's §16 infra; the GET→POST for `/action-card/perform` is app-side and scheduled | — |
| WY-10 | empty containers dropped, not preserved | **OPEN — minor, scheduled** | decide preserve-vs-drop for empty arrays/objects in projection | — |

## Authority
- `RATIFY-15-06` (CL-5) — **not issued** and correctly so: the IAM stub is not real IAM. To be
  drafted against C-BLOCK-04 and ratified at the team meeting alongside naming the Section 15
  authorities. WY-1 is fixed in the stub so the real IAM won't inherit a fail-open table.
- `RATIFY-15-07` (CL-13) — the institutional security reviewer's to issue (request #8); WY-7 and the
  threat-register corrections in §5 of the review are handed to them, not closed here.

## Evidence
`clarence/c-block-05` — WY-1..WY-3 + WY-11 fixed with tests; `python docs/assurance/validate_assurance.py`
still reports graph SOUND, all linked evidence green, 0/15 (the fixes are pending re-review, not
authorised). Recorded so the disposition is not "silence" (WP §3).
