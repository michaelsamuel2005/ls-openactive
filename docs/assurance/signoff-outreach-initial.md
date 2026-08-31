# Sign-off outreach — ready-to-send messages

**Purpose.** Each message below asks one person (or the team, or an institution) for the *real*
review or decision that unblocks specific assurance claims. A claim flips BLOCKED → AUTHORISED only
when a genuine disposition comes back — **a name, a date, and a reference** — which is then recorded
in `docs/assurance/assurance-case.json` and confirmed by re-running `validate_assurance.py`.

**Ask everyone to reply in this one format:**
> `<name>, <date> — approved / approved-with-conditions / not-yet — <reference or decision-log ID>`
> (plus a short list of any findings to fix)

**Branch under review:** `clarence/c-block-05` · **Repo:** `ls-openactive`

---

## Tracker

| # | To | Unblocks | Kind | Status |
|---|----|----------|------|--------|
| 1 | Michael | CL-1, CL-3, CL-6, CL-14 | in-team review + ratification | not sent |
| 2 | Wesley | CL-1, CL-5, CL-13 | in-team review + ratification | not sent |
| 3 | Fahmi | CL-7 (+ CL-4 parity) | in-team review + ratification | not sent |
| 4 | Non-author HCI/accessibility reviewer *(to be named — not Clarence)* | CL-2, CL-4, CL-10 | in-team review | not sent |
| 5 | Team meeting | CL-9, CL-8, + demo/§08/§18 authorities on CL-1, CL-4, CL-14 | ratification | not sent |
| 6 | Data-governance / DPIA authority | CL-11 | institutional determination | not sent |
| 7 | Bristol PGT research-ethics route | CL-12 (+ ethics part of CL-7) | institutional determination | not sent |
| 8 | You (Clarence) + a non-author spot-check | CL-15 | own work + check | not sent |

---

## 1 → Michael  (evidence semantics / Section 09) — unblocks CL-1, CL-3, CL-6, CL-14

**Subject:** Review request — evidence-contract & checker on `clarence/c-block-05` (CL-1/3/6/14)

Hi Michael,

Could you do a non-author review of the application-facing use of the evidence contract on
`clarence/c-block-05`? Specifically:

- `packages/application-contracts/c-block-05/` — does every application-facing state map to a valid,
  distinguishable typed decision, and can any claim resolve to a receipt and a compatible release?
- `packages/certificate-checker/` — is the certificate/witness shape and the checker contract
  sufficient, versioned and fail-closed from a consumer's view? (run `python test_certificate_checker.py`)
- the conversation route (`apps/public-discovery/test_conversation.py`) — does the interface ever
  strengthen, suppress or confuse a state?
- `RATIFY-09-04` (CA-2): is it acceptable for the claim-contract author to also author the production
  interpreter, or must that pair be split?

Please send back, in the format above: your review outcome + name + date; the **Section 09 vocabulary
ratification** reference; and the `RATIFY-09-04` and `RATIFY-09-05` decision-log IDs. Aim for [date]?

Thanks,
Clarence

---

## 2 → Wesley  (transport, versioning, IAM / Section 16) — unblocks CL-1, CL-5, CL-13

**Subject:** Review request — versioning, disclosure enforcement & security (CL-1/5/13)

Hi Wesley,

Could you review, on `clarence/c-block-05`:

- version/compatibility rules and fail-closed behaviour on stale/incompatible releases
  (`packages/application-contracts/c-block-05/`);
- whether the field-level disclosure classes are enforceable **server-side**
  (`disclosure-classes.json`, `projection_and_invariants.py`);
- the plan to replace the demonstration role-gate stub with real authentication/IAM;
- application-facing security controls (`packages/security/`: sanitisers, threat register, secret scan).

Please send back: outcome + name + date; the `RATIFY-15-06` (IAM) reference; and the `RATIFY-15-07`
(security review) reference. If a separate security reviewer owns `RATIFY-15-07`, let me know and I'll
route that part to them. Aim for [date]?

Thanks,
Clarence

---

## 3 → Fahmi  (evaluation) — unblocks CL-7 (and the CL-4 parity check)

**Subject:** Confirm evaluation-parity sign-off + book the benchmark session (CL-7)

Hi Fahmi,

Following your review of `condition-manifest.json`, the four points (task count, origin/publisher,
repair minting, vintage) are actioned and validator-enforced — see
`packages/evaluation/fahmi-review-response.md` and `python packages/evaluation/validate_conditions.py`.

Could you confirm the fixes address your review and **sign the evaluation-parity gate**, and let's
book the session to mint the ≥20-task benchmark set against your power target? Please also confirm the
HCI/evaluation-parity view for CL-4.

Send back: confirmed / remaining points + name + date, and the `RATIFY-14-07/08` reference. (The
ethics-route part of CL-7 is tracked separately under the PGT ethics submission.) Aim for [date]?

Thanks,
Clarence

---

## 4 → [NAME the non-author HCI / accessibility reviewer] — unblocks CL-2, CL-4, CL-10

> **First action for the team:** name an eligible non-author reviewer for this — it **cannot be
> Clarence**, who built the interfaces (`RATIFY-14-02` / C-BLOCK-03).

**Subject:** Accessibility & content review request — public/staff apps (CL-2/4/10)

Hi [name],

Could you do an independent (non-author) review of the two applications on `clarence/c-block-05`?

- Run manual keyboard, focus and screen-reader testing on the declared browser × assistive-technology
  matrix (`apps/public-discovery/`, `apps/staff-assurance/`; `a11y_check.py` is only a partial input).
- Confirm the wording never over-claims and that each evidence state (supported / bounded non-match /
  unknown / conflicting) is distinguishable and never rendered as a negative fact.
- Confirm map/list/compare/browse routes preserve the certified slate and order.

Please send back: the tested matrix + findings + name + date; the **content sign-off**; and the
**accessibility statement** text + `RATIFY-14-02`. Aim for [date]?

Thanks,
Clarence

---

## 5 → Team meeting agenda item — unblocks CL-9 (and the authorities on CL-1, CL-4, CL-8, CL-14)

**Agenda: assurance ratifications (5 min).** Please minute these with real decision-log IDs:

1. Ratify the reconciliation register (`RATIFY-19-04`) → **CL-9**.
2. Name the accountable **Section 08 owner** (bind to a real canonical decision-log ID, *not* an
   invented `RATIFY-08-*`; C-BLOCK-01) → enables **CL-14**.
3. Name the public/staff **product / demonstration lead** and issue the `public_safe_demonstration`
   gate → authorities on **CL-1** and **CL-4**.
4. **Section 18 partner-route owner** to sign the governed-action route → **CL-8**.

Please send back the decision-log IDs + date for each.

---

## 6 → Data-governance / DPIA authority — unblocks CL-11

**Subject:** DPIA / controller-processor determination — telemetry & dialogue-log path

This is a **formal determination**, not a verbal sign-off. Please issue (or point me to) the
controller/processor determination, the lawful-basis finding, and the DPIA outcome for the telemetry
and dialogue-log data path (`packages/evaluation/event-schema.json` is transient-by-default by
construction; the privacy/telemetry write-up is in `docs/applications/C-13-privacy-telemetry.md`).

Send back: the DPIA reference / decision (`RATIFY-15-02/04`). Until that reference exists, CL-11 stays
blocked — which is correct.

---

## 7 → Bristol PGT research-ethics route — unblocks CL-12 (and the ethics part of CL-7)

**Subject:** PGT research-ethics submission — status & approval reference

Also a **formal determination**. The ethics application, participant materials and data plan are
drafted (`docs/assurance/ethics-application-outline.md`). Please confirm submission and, when issued,
the approval reference (`RATIFY-15-03`). Until that reference exists, CL-12 stays blocked and the
project runs under the no-study fallback (which yields real technical/accessibility/replay evidence
with no participant claim).

Send back: submission confirmation + the approval reference when issued.

---

## 8 → You (Clarence) + a non-author spot-check — unblocks CL-15

Not an outreach message — your own work:

1. Finish the K7 reading: complete every load-bearing row in `docs/assurance/foundation-matrix.json`
   (personally read, version-of-record DOI verified, your own verdict recorded) until
   `reading-log.md` reaches 28/28.
2. Record your §26 acceptance.
3. Ask **one non-author** to spot-check that the attested records match the primary sources, and to
   reply with name + date.

That closes CL-15 without needing anyone external.

---

## When a reply comes back

Paste it here (or into this file). I will set that claim's `reviewer` and/or `authority` block in
`assurance-case.json` — `status: "done"`, plus the name, date and reference — and re-run
`python docs/assurance/validate_assurance.py` so the claim flips **BLOCKED → AUTHORISED**, with the
evidence on record. When all fifteen carry a real disposition, the run reports **15 authorised** — and
every one is true.
