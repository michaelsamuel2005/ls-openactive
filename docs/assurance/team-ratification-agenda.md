# Team meeting — assurance ratifications (agenda + minutes template)

Purpose: capture the four group decisions that unblock the ratification-gated claims. Each needs a
**real decision, a named owner/holder, a decision-log ID, and a date** — that is what lets the claim
flip legitimately. Fill the "MINUTES" blocks live in the meeting; paste them back afterwards and they
get recorded in `assurance-case.json`.

Branch under review: `clarence/c-block-05` · current commit at time of writing: `21c788b`

---

## Item 1 — Ratify the reconciliation register  → unblocks CL-9
**Decide:** is the pre-code reconciliation register (all C-BLOCK items dispositioned with owner, tests,
fallback) ratified?
**MINUTES:**
- Decision: [ratified / not yet]
- Decision-log ID: `RATIFY-19-04`
- Decided by: [name(s)] · Date: [YYYY-MM-DD]

## Item 2 — Name the accountable Section 08 owner  → enables CL-14 (with Michael's §09 review)
**Decide:** who is the accountable owner for Section 08? Bind it to a **real** canonical decision-log
ID (not an invented `RATIFY-08-*`; this resolves C-BLOCK-01).
**MINUTES:**
- Section 08 owner: [name]
- Decision-log ID: [real ID]
- Decided by: [name(s)] · Date: [YYYY-MM-DD]

## Item 3 — Product / demonstration lead + `public_safe_demonstration` gate  → authority on CL-1, CL-4
**Decide:** who is the public/staff product (demonstration) lead, and do they issue the
`public_safe_demonstration` gate for the research demonstration?
**MINUTES:**
- Demonstration lead / holder: [name]
- `public_safe_demonstration` gate: [issued / not yet]
- Decision-log ID: [ID, e.g. RATIFY-19-06]
- Decided by: [name(s)] · Date: [YYYY-MM-DD]

## Item 4 — Section 18 partner-route owner  → unblocks CL-8
**Decide:** who owns the §18 partner/governed-action route and signs that governed actions cannot skip
review/approval and that send is authoriser-only?
**MINUTES:**
- §18 owner / holder: [name]
- Governed-action route: [signed / not yet]
- Decision-log ID: [ID]
- Decided by: [name(s)] · Date: [YYYY-MM-DD]

---

## What each unblocks (for reference)
| Item | Claim(s) | Gate it fills |
|------|----------|---------------|
| 1 | CL-9 | reviewer + authority (team ratification `RATIFY-19-04`) |
| 2 | CL-14 | authority (Section 08 ownership) — also needs Michael's §09 review |
| 3 | CL-1, CL-4 | authority (`public_safe_demonstration` gate) — CL-1 also needs Michael/Wesley review; CL-4 also needs the HCI reviewer + Fahmi parity |
| 4 | CL-8 | reviewer + authority (§18 owner) |

## After the meeting
Paste the filled MINUTES here. I set the matching `reviewer`/`authority` blocks in
`assurance-case.json` (status done + name + date + decision-log ID) and re-run the validator, so each
claim flips **only** on a real, recorded decision. Claims that also need other gates (CL-1, CL-4, CL-14)
flip when **all** their gates are in.
