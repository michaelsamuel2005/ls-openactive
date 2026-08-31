# Team meeting — agenda

**Purpose:** clear the four blockers that re-review at `7cf65ca` cannot clear on its own —
the §09 contract freeze, the C-BLOCK-04 IAM design, the unowned M-2, and the ratification
round-up.

| | |
|---|---|
| Date / time | _TBC_ |
| Duration | 60 min |
| Chair | Clarence |
| Required | Clarence, Michael, Wesley |
| Required for item 3 | Whoever owns (or will own) the evidence engine |
| Optional / for item 4 | Institutional security reviewer |
| Baseline | `clarence/c-block-05` @ `7cf65ca` |

**Pre-reads**
- `docs/assurance/signoff-messages.md` — the three re-review requests and what each leaves open
- `docs/assurance/signoffs.md` — current entry state per finding
- `docs/reviews/wesley-review-response.md` — full disposition of Wesley's findings
- `certificate.schema.json` and the §09 contract text as it currently stands

**Ground rule:** this meeting produces *decisions and owners*, not designs. Anything that
needs more than ~10 minutes of design discussion gets an owner and a follow-up slot rather
than eating the hour.

---

## 1. §09 contract freeze — 20 min
**Leads:** Clarence + Michael · **Unblocks:** CL-1, CL-3, CL-6, CL-14 · **Produces:** `RATIFY-09-04`, `RATIFY-09-05`

The six fixed findings (MS-1/3/6/7/8/9) are Michael's to re-review at `7cf65ca` and need no
meeting time. What needs the room is the part neither of us can settle alone.

**MS-2 / MS-4 / MS-5 — receipt semantics and crypto-binding**
- What does a receipt attest to, precisely — and what is it explicitly *not* evidence of?
- How is a receipt bound to its `DecisionEnvelope`: what is signed, over what canonical form, and by whom?
- What must a verifier do to check that binding, and what does it do when the binding fails?

**MS-10 — the attribute↔claim binding**
- What exactly makes a claim "verifier-approved"? Which attributes must be present, and bound to what?
- Does the definition live in the schema, the manifest, or the contract text — and which one is normative if they disagree?

**Decisions required**
1. Freeze the above as §09 contract text, or name the smallest open question blocking a freeze.
2. Confirm `RATIFY-09-04` / `RATIFY-09-05` are the right two ratification points for it, and who issues each.
3. Set the date by which the frozen text and its tests land on the branch.

---

## 2. C-BLOCK-04 — IAM design, and Wesley's two design items — 15 min
**Leads:** Clarence + Wesley · **Unblocks:** CL-5 · **Gate:** `RATIFY-15-06` (currently withheld)

**IAM (CL-5).** The stub has to be replaced with real IAM before `RATIFY-15-06` can be
issued. Draft the design against C-BLOCK-04 and agree the shape here:
- Identity source and trust boundary — what is authoritative, and what is merely asserted by the caller?
- How this composes with `_cap_for`'s default-deny, so that WY-1's fix isn't quietly widened by the real implementation.
- Failure mode: what happens when IAM is unreachable? (Fail-closed, consistent with WY-3.)

**WY-4 — staleness bound.** Wesley offered a short design conversation. What is the maximum
tolerated staleness, measured from what event, and what is the behaviour at the bound?

**WY-5 — app-side version gate.** Where does the gate sit relative to `_c_version`, and does
it duplicate or defer to the checker's own version enforcement (MS-7)?

**Decisions required**
1. Agreed IAM design shape, an owner, and a target commit.
2. Whether WY-4/WY-5 are in scope for C-BLOCK-04 or tracked separately.
3. Confirm `RATIFY-15-06` stays withheld until real IAM lands — no provisional issue.

---

## 3. M-2 — assign the evidence-engine owner — 5 min
**Unblocks:** CL-7 · **Gate:** `RATIFY-14-07/08`

Fahmi's review side of CL-7 is complete: M-1/3/4/5 and M-6 are all closed and logged. The
one remaining blocker is M-2 — the shared terminal referent being **produced and verified by
the evidence engine** — and it is out of Clarence's stream with **no named owner**. That is
the whole item.

**Decisions required**
1. Name the evidence-engine owner.
2. Agree a date for the verified referent to land.
3. Confirm the sequence: referent lands → Fahmi does a final pass → upgrades to **APPROVED** → issues `RATIFY-14-07/08`.

---

## 4. CL-13 — institutional security route — 5 min
**Gate:** `RATIFY-15-07` (not Wesley's to issue)

CL-13 has been routed to the institutional security reviewer along with WY-7 and Wesley's
threat-register corrections.

**Decisions required**
1. Confirm the reviewer has it and knows `RATIFY-15-07` is theirs to issue.
2. Agree an expected turnaround, or escalate if none can be given.
3. Confirm nothing in the code stream is waiting on this — i.e. it runs in parallel, not in series.

---

## 5. Ratification round-up — 10 min

Walk the gates and mark each as *issuable now*, *blocked on a named item*, or *not ours*.

| Ratification | Blocked on | Issuer | Status to confirm |
|---|---|---|---|
| `RATIFY-09-04` | §09 freeze (item 1) | _confirm_ | Blocked |
| `RATIFY-09-05` | §09 freeze (item 1) | _confirm_ | Blocked |
| `RATIFY-14-07` | M-2 (item 3), then Fahmi's final pass | Fahmi | Blocked |
| `RATIFY-14-08` | M-2 (item 3), then Fahmi's final pass | Fahmi | Blocked |
| `RATIFY-15-06` | Real IAM (item 2) | _confirm_ | Withheld — deliberately |
| `RATIFY-15-07` | Institutional security review (item 4) | Institutional security reviewer | Not ours |

**Decisions required**
1. Confirm the issuer for each row that is currently unconfirmed.
2. Confirm that no ratification is issued ahead of its blocker — including under schedule pressure.
3. Agree who tracks these and where the tracking lives.

---

## 6. Close — 5 min

- Read back every decision and owner.
- Confirm the demonstration gate and any other authority gates are tracked elsewhere and are **not** in scope for this meeting.
- Next checkpoint date.

---

## Appendix — where things actually stand

Re-review at `7cf65ca` moves the *fixed findings* to APPROVED. It does not authorise the
claims. After a fully successful round of re-review, the remaining blockers are exactly:

- **CL-1 / CL-3 / CL-6 / CL-14** — joint §09 contract freeze (MS-2/4/5, MS-10)
- **CL-5** — real IAM replacing the stub
- **CL-7** — evidence engine produces and verifies the terminal referent (M-2)
- **CL-13** — institutional security review
- **All claims** — the authority gates: ratifications, security, demonstration gate

None of these is closed by writing more code on this branch, which is why they are on this
agenda. This appendix covers only the claims named in the three re-review messages
(CL-1, CL-3, CL-5, CL-6, CL-7, CL-13, CL-14) and makes no statement about the others.
