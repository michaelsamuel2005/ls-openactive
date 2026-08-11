# Step 3 — the assurance case as your map

**Done:** 2026-08-12 · source: `docs/assurance/assurance-case.md` (regenerate: `python3
docs/assurance/validate_assurance.py`). This is the navigable index for Steps 4–9: find a claim →
jump to the file that proves it → see who still has to sign. Verified live today: **14/14 tests
green, 15 claims, graph SOUND**.

## Every claim → what it protects → backing test → file to open → who signs

| Claim | Protects (one line) | Test(s) | Open this file first | Sign-off still needed |
|---|---|---|---|---|
| CL-1 | public/staff never disagree; restricted values can't move public output | T-contracts, T-staffslice, T-publicslice | `packages/application-contracts/c-block-05/projection_and_invariants.py` (`INV-NONINTERFERENCE`, `project()`) | Michael + Wesley |
| CL-2 | unknown never shown as "no"/"free" | T-wording, T-contracts | `packages/accessible-design-system/content/evidence-language.json` + `INV-NO-COLLAPSE` | content / HCI |
| CL-3 | no unverified factual token reaches a user | T-contracts, T-checker | `packages/certificate-checker/certificate_checker.py` + `INV-NO-UNVERIFIED` | Michael (Section 09) |
| CL-4 | certified slate + order preserved; no bypass of abstention | T-contracts, T-ia | `INV-SLATE-ORDER` + `packages/public-ia/public-state-machine.json` | HCI / eval parity |
| CL-5 | staff-only info can't reach public; role-gated | T-contracts, T-staffslice | `packages/application-contracts/c-block-05/disclosure-classes.json` + staff `server/main.py` (`_role`, `ROLE_CAPABILITIES`) | security / IAM (Wesley) |
| CL-6 | forged/stale/swapped/escalated evidence rejected | T-checker | `certificate_checker.py` (`_c_escalation`, `FAIL_*`) + `test_certificate_checker.py` | non-author code review + Michael (`RATIFY-09-04`) |
| CL-7 | interface effect not confounded with backend | T-conditions | `packages/evaluation/condition-manifest.json` + `validate_conditions.py` | Fahmi |
| CL-8 | actions can't skip review/approval; send needs a role | T-actioncard, T-staffslice | `packages/staff-ia/action-card-state-machine.json` + `validate_action_cards.py` | Section 18 owner |
| CL-9 | every pre-code blocker dispositioned | T-register | `docs/assurance/reconciliation-register.json` + `validate_register.py` | team (`RATIFY-19-04`) |
| CL-10 | evaluated *toward* WCAG 2.2 AA (not blanket conformance) | T-publicslice, T-staffslice | `docs/applications/accessibility-wcag22-plan.md` + `apps/public-discovery/a11y_check.py` | non-author HCI reviewer (`C-BLOCK-03`) |
| CL-11 | telemetry transient; no raw utterance/exact location | T-privacy | `packages/privacy/telemetry-dictionary.json` + `validate_privacy.py` | governance / DPIA |
| CL-12 | every human-facing activity ethically gated + fallback | T-ethics | `packages/ethics/ethics-activity-matrix.json` + `validate_ethics.py` | Bristol PGT ethics |
| CL-13 | app-facing injection/output controls; no committed secret | T-security, T-checker | `packages/security/sanitize.py` + `threat-register.json` | security reviewer (`RATIFY-15-07`) |
| CL-14 | chat converges on the certified decision; never decides truth | T-conversation, T-contracts | `apps/public-discovery/server/intent.py` + `test_conversation.py` | Section 08 owner + Michael |
| CL-15 | every load-bearing source read + version-verified (K7) | T-reading | `docs/assurance/foundation-matrix.json` + `reading-log.md` | non-author reading check + your §26 record |

## Who you still need (the agenda this map produces)

| Person / authority | Claims they unlock | Priority |
|---|---|---|
| **Michael** (evidence semantics, `RATIFY-09-04/05`) | CL-1, CL-3, CL-6, CL-14 | **highest — 4 claims; same workshop as Step 4** |
| **Wesley** (transport + real IAM) | CL-1, CL-5, CL-13 | high |
| **Non-author HCI/accessibility reviewer** (`C-BLOCK-03`) | CL-2, CL-4, CL-10 | high |
| **Fahmi** (evaluation parity) | CL-7 | medium |
| Governance / DPIA (`RATIFY-15-02/04`) | CL-11 | institutional |
| Bristol PGT ethics (`RATIFY-15-03`) | CL-12 | institutional |
| Security reviewer (`RATIFY-15-07`) | CL-13 | institutional |
| Section 08 owner (`C-BLOCK-01`) | CL-8, CL-14 | team |
| Team ratification (`RATIFY-19-04`) | CL-9 | team |
| You (K7 reading + §26) | CL-15 | **yours** |

## Three core claims traced (defend these cold before Step 4)

These map to your falsification conditions (WP §19.4); if any breaks, the contribution narrows.

**CL-1 — value-level non-interference.** Open `projection_and_invariants.py`. `project(node, fields,
allowed, path)` builds the public view by *dropping* any field whose class isn't `PUBLIC_SAFE`
(fail-closed). `INV-NONINTERFERENCE` mutates only non-public leaves and asserts the public projection
is byte-identical. *Bug would look like:* changing `internal_score` or a receipt shifts the public
output. The adversarial fixture `staff_note_in_public.json` is caught by `INV-DISCLOSURE` — proof the
gate can fail.

**CL-3 — verify-before-render.** Open `certificate_checker.py`. `check()` returns `PASS` only when the
certificate verifies against witness, receipts, versions and scope; `_c_escalation` rejects a
`supported_match` sitting over a `U`/`B`/`F` predicate (`FAIL_ILLEGAL_ESCALATION`). Paired with
`INV-NO-UNVERIFIED` (no claim with `verification ≠ verified` is renderable). *Bug would look like:* a
fluent sentence rendered before the verifier signs off.

**CL-5 — one-way disclosure + role gate.** Open `disclosure-classes.json` (field → class) and staff
`server/main.py`: `_role` reads the `x-staff-role` header (or `?role=` dev param), and
`ROLE_CAPABILITIES` gates each action server-side. *Bug would look like:* a `STAFF_EVIDENCE` field
reaching the public plane, or "send" available to an analyst.

## What the map reveals (worth saying at viva)

- **All 15 are BLOCKED for the same honest reason** — a human hasn't signed — not because any
  evidence is red. The branch is finished to the point a reviewer can start.
- **`T-contracts` backs six claims** (CL-1, 2, 3, 4, 5, 14). That concentration is *why* C-BLOCK-05 is
  the keystone and why Step 4 is the highest-leverage review: fix the contract and six claims move
  together.
- **The four most examiner-exposed residuals** (be ready to volunteer these): CL-14 (LLM not yet
  integrated; Section 08 owner unresolved — `C-BLOCK-01`), CL-10 (manual/AT accessibility testing
  outstanding — the reason it's "evaluated *toward* AA"), CL-5 (role gate is a stub until Wesley's
  real IAM), CL-15 (reading 0/28).
- **Michael is your highest-value sign-off** (4 claims) and it's the *same* conversation as the
  C-BLOCK-05 contract workshop — so Step 4 and unblocking CL-1/3/6/14 are one meeting, not two.
- **Claims you own end-to-end** (control owner = Clarence alone: CL-2, 4, 6, 8, 9, 10) you can defend
  now without waiting on anyone; the rest are shared and need a partner's sign-off.

## Done with Step 3 when

You can point at any claim and name its control, its proving file, and the person who must sign —
without hunting. You edit nothing here; the only file you ever change is `assurance-case.json`, in
Step 9, as sign-offs land.
