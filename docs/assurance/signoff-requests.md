# Sign-off request pack — closing the 15 assurance claims

**How to use:** send each block below to the named person (email / Slack). Each asks for a specific
review or decision and tells them exactly what to send back. A claim flips to AUTHORISED only when a
**real, referenceable disposition** comes back — a name, a date, and (for institutional gates) a
document reference. Paste any reply here and I'll record it in `assurance-case.json` and re-run the
validator so the claim flips, with the evidence attached.

**Reply format to ask everyone for:** *"<name>, <date> — <approved / approved-with-conditions /
not-yet> — <reference or decision-log ID if applicable>"*, or a short list of findings to fix.

---

## 1 → Michael (evidence semantics / Section 09) — unlocks CL-1, CL-3, CL-6, CL-14
Please review the application-facing use of your evidence contract on `clarence/c-block-05`
(`packages/application-contracts/c-block-05/`, `packages/certificate-checker/`). Specifically:
1. Does every application-facing state map to a valid, distinguishable typed decision, and can any
   claim resolve to a receipt and a compatible release?
2. Can the interface accidentally strengthen, suppress or confuse a state?
3. Are the certificate/witness shape and the checker contract sufficient, versioned and fail-closed
   from a consumer's view?
4. `RATIFY-09-04` (CA-2): is it acceptable for the claim-contract author to also author the production
   interpreter, or must that pair be split?
Send back: reviewed / findings, your name + date; and the Section 09 ratification reference for (4).

## 2 → Wesley (transport, versioning, IAM / Section 16) — unlocks CL-1, CL-5, CL-13
Please review: version/compatibility rules and fail-closed behaviour on stale/incompatible releases;
whether the field-level disclosure classes are enforceable server-side; and the plan to replace the
demonstration role-gate stub with real authentication/IAM. Send back: reviewed / findings + name +
date; and the `RATIFY-15-06` reference once the IAM path is agreed.

## 3 → Fahmi (evaluation) — unlocks CL-7
You've already reviewed `condition-manifest.json`; the four points (task count, origin/publisher,
repair minting, vintage) are actioned and validator-enforced (see `fahmi-review-response.md`). Please
confirm the fixes address your review and sign the evaluation-parity gate, and let's book the session
to mint the ≥20-task benchmark set against your power target. Send back: confirmed / remaining points
+ name + date (`RATIFY-14-07/08`).

## 4 → [name the non-author HCI / accessibility reviewer] (C-BLOCK-03) — unlocks CL-2, CL-4, CL-10
**First: the team names an eligible non-author reviewer** (it cannot be me — I built the interfaces).
That person: runs manual keyboard, screen-reader and AT testing on the declared browser × AT matrix;
confirms the wording never over-claims and that each evidence state is distinguishable; and confirms
map/list/compare preserve the certified order. Send back: the tested matrix + findings + name + date
(`RATIFY-14-02` + accessibility statement).

## 5 → The team (at the next meeting) — unlocks CL-9 (+ enables CL-8, CL-14)
Three ratifications, bound to real decision-log IDs:
- Ratify the reconciliation register (`RATIFY-19-04`) → CL-9.
- Name the accountable Section 08 owner (`C-BLOCK-01`, a real ID, not an invented `RATIFY-08-*`) →
  enables CL-8, CL-14.
- Name the public/staff product lead (`RATIFY-19-06`, `C-BLOCK-02`).
Send back: the decision-log IDs + date.

## 6 → Data-governance / DPIA authority — unlocks CL-11
This is a **formal determination**, not a verbal sign-off. Please issue (or point me to) the
controller/processor determination, the lawful-basis finding, and the DPIA outcome for the telemetry
and dialogue-log data path. Send back: the DPIA reference / decision (`RATIFY-15-02/04`). Until that
reference exists, CL-11 stays blocked.

## 7 → Bristol PGT research-ethics route — unlocks CL-12
Also a **formal determination**. The ethics application, participant materials and data plan are
drafted (`docs/assurance/ethics-application-outline.md`); please confirm submission and, when issued,
the approval reference (`RATIFY-15-03`). Until the approval reference exists, CL-12 stays blocked and
the project runs under the no-study fallback.

## 8 → Security / assurance reviewer — unlocks CL-13
Please review the application-facing controls (`packages/security/`: sanitisers, threat register,
secret scan) and issue the security review outcome (`RATIFY-15-07`). Send back: reviewed / findings +
name + date + reference.

## 9 → You (Clarence) — unlocks CL-15
Finish the K7 reading and record your own verdicts (`foundation-matrix.json` → `reading-log.md` reaches
28/28), then a **non-author** spot-checks that the attested records match the sources. That closes
CL-15 without needing anyone external.

---

## How it proceeds (per claim, once a real disposition is in)
1. You paste the reply here (name, date, decision, reference).
2. In `docs/assurance/assurance-case.json` the relevant claim's blocks are set, e.g.:
   `"reviewer": { …, "status": "done", "name": "Michael S." }` and/or
   `"authority": { …, "status": "done", "holder": "PGT Ethics (ref 2026-xxxx)" }`.
3. `python docs/assurance/validate_assurance.py` re-runs → that claim flips **BLOCKED → AUTHORISED**,
   and the evidence (name/date/ref) is on record.
4. When all fifteen carry a real disposition, the run reports **15 authorised** — and every one is true.

**Realistic order:** the teammate reviews (Michael, Wesley, Fahmi, the named HCI reviewer) can land in
days; the team ratifications at the next meeting; the three institutional determinations (ethics, DPIA,
security) on their own formal timelines. The honest interim state stays 0/15 — with these requests out,
it's 0/15 *in motion*, which is exactly what a marker wants to see.
