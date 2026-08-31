# Sign-off request messages — C-BLOCK-05

Record of the re-review requests sent to each reviewer after the C-BLOCK-05 fixes landed.
Kept here so that every request is auditable against the commit it was pinned to, and so
that `signoffs.md` entries can be traced back to the request that prompted them.

| | |
|---|---|
| Branch | `clarence/c-block-05` |
| Commit pinned in all three messages | `7cf65ca` |
| Sent by | Clarence |
| Recipients | Michael, Wesley, Fahmi |
| Recorded | 2026-08-24 |

> Every message below is pinned to `7cf65ca`. If the branch moves, do **not** edit these
> messages — send a new request against the new tip and add it as a new section. Sign-off
> is against a commit, not against a branch name.

---

## Status at time of sending

| Message | Reviewer | Claims | Findings sent for re-review | Asked for | Still open after re-review |
|---|---|---|---|---|---|
| 1 | Michael | CL-1, CL-3, CL-6, CL-14 | MS-1, MS-3, MS-6, MS-7, MS-8, MS-9 | Re-review at `7cf65ca`; one follow-up `signoffs.md` entry per finding | MS-2, MS-4, MS-5 (receipt semantics + crypto-binding); MS-10 (attribute↔claim binding) → `RATIFY-09-04`, `RATIFY-09-05` |
| 2 | Wesley | CL-1, CL-5, CL-13 | WY-1, WY-2, WY-3, WY-11 | Re-review at `7cf65ca`; follow-up `signoffs.md` entries | CL-5 real IAM (`RATIFY-15-06` withheld); WY-4, WY-5 design conversation; CL-13 with institutional security reviewer (`RATIFY-15-07`) |
| 3 | Fahmi | CL-7 | M-1, M-3, M-4, M-5, M-6 all closed | Final pass once M-2 lands, then upgrade to **APPROVED** and issue `RATIFY-14-07/08` | M-2 — terminal referent produced and verified by the evidence engine (owner not yet assigned) |

---

## 1. → Michael — re-review (CL-1, CL-3, CL-6, CL-14)

**Subject:** All six of my fixes are in at `7cf65ca` — re-review?

Hi Michael,

Every finding of yours that was mine to fix is done and pushed, at branch `clarence/c-block-05`, commit **`7cf65ca`**, each with the adversarial test that would have caught it:

- **MS-1** — public projection drops non-verified claim tuples entirely (`test_slice.py`).
- **MS-3** — checker enforces `certificate.schema.json` + context at runtime (`schema_extra_field`).
- **MS-6** — state-transition check against the manifest (`bad_transition`).
- **MS-7** — incompatible decision combos rejected + checker's own version enforced (`incompatible_decision`, `caller_asserted_checker`).
- **MS-8** — the `check(checks=[])` bypass is gone (`_run_checks([])` fails closed).
- **MS-9** — conversation no longer drops/reverses constraints or injects step-free (4 tests).

Could you re-review at `7cf65ca` and, for each you're satisfied with, add a follow-up entry to `docs/assurance/signoffs.md` (per your one-entry-per-finding rule)? To fully close CL-1/3/6/14 we still need the two joint pieces — **MS-2, MS-4, MS-5** (receipt semantics + crypto-binding to the `DecisionEnvelope`) and **MS-10** (the attribute↔claim binding that defines "verifier-approved"). Can we book a short session to freeze that part of the §09 contract and record `RATIFY-09-04`/`RATIFY-09-05`?

Thanks, Clarence

---

## 2. → Wesley — re-review (CL-1, CL-5, CL-13)

**Subject:** WY-1/2/3/11 fixed at `7cf65ca` — re-review?

Hi Wesley,

Your "fix first" four are done and pushed at commit **`7cf65ca`**, each with its test:

- **WY-1** — `_cap_for` default-denies; `/action-card/perform` rejects any unmodelled `(frm,to)` (analyst `observed→sent_by_authorised_role` = 403).
- **WY-2** — `safe_url()` wired into `build_view`; a `javascript:` provider link renders empty.
- **WY-3** — `_c_version` fails closed on empty/partial `allowed_versions` (the 2019-corpus PASS is gone).
- **WY-11** — `jsonschema` + `fastapi/jinja2/uvicorn/httpx` pinned in `requirements.txt`.

Could you re-review at `7cf65ca` and add your follow-up entries to `signoffs.md`? To fully close: **CL-5** still needs real IAM to replace the stub (so `RATIFY-15-06` stays withheld — let's draft that against C-BLOCK-04 and take it at the team meeting); **WY-4/WY-5** (staleness bound + app-side version gate) need the short design conversation you offered; and **CL-13** I've routed to the institutional security reviewer with WY-7 and your threat-register corrections, since `RATIFY-15-07` isn't yours to issue. Full disposition is in `docs/reviews/wesley-review-response.md`.

Thanks, Clarence

---

## 3. → Fahmi — close-out (CL-7)

**Subject:** CL-7 — M-6 closed; only M-2 (evidence engine) remains

Hi Fahmi,

Thanks for the M-6 re-verification. Your review side of CL-7 is effectively complete — the manifest findings (M-1/3/4/5) and M-6 are all closed and logged in `signoffs.md`. The single remaining blocker, **M-2**, is the shared terminal referent being *produced and verified by the evidence engine*, which is out of my stream.

So there's nothing further for you on the manifest. Once the evidence-engine owner produces the verified referent, could you do a final pass and, if satisfied, upgrade your entry to **APPROVED** and issue `RATIFY-14-07/08`? I'll hand M-2 to whoever owns the engine and copy you when the referent lands.

Thanks, Clarence

---

## What re-review can and cannot close

Re-review lets each reviewer upgrade REVIEWED-WITH-CONDITIONS → APPROVED on the findings
that were fixed at `7cf65ca`. It does **not** by itself authorise the underlying claims,
because for each of these claims something remains that is not the reviewer's to give:

| Claim(s) | Remaining blocker | Owner | Gate |
|---|---|---|---|
| CL-1, CL-3, CL-6, CL-14 | §09 contract freeze — MS-2/4/5 (receipt semantics + crypto-binding to `DecisionEnvelope`), MS-10 (attribute↔claim binding) | Clarence + Michael, jointly | `RATIFY-09-04`, `RATIFY-09-05` |
| CL-5 | Real IAM replacing the stub, designed against C-BLOCK-04 | Clarence + Wesley | `RATIFY-15-06` (withheld) |
| CL-7 | M-2 — terminal referent produced *and verified* by the evidence engine | Evidence-engine owner — **unassigned** | `RATIFY-14-07/08` (Fahmi, after final pass) |
| CL-13 | Institutional security review of WY-7 + threat-register corrections | Institutional security reviewer | `RATIFY-15-07` (not Wesley's to issue) |

Separately, the authority gates — ratifications, institutional security, and the
demonstration gate — sit outside the code review stream entirely and are not affected by
anything at `7cf65ca`.

**Realistic outcome of these three messages:** the fixed findings get signed off, four
claims move close to clearing, and what remains is joint work plus authority items. Not
15/15 — but the movement is real, and the remainder is now named and owned rather than
diffuse.

> This record covers only the claims named above (CL-1, CL-3, CL-5, CL-6, CL-7, CL-13,
> CL-14). It makes no statement about the other claims in the set.
