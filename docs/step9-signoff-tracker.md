# Step 9 — sign-off tracker (closing the human gates)

**What Step 9 is:** as each *real* non-author review and authority decision lands, mark it `done` in
`docs/assurance/assurance-case.json` and re-run the validator; that claim flips **BLOCKED →
AUTHORISED**. **What Step 9 is not:** it is never filled ahead of the event. A gate marked `done`
asserts a named human actually signed. Do not backfill a cell from memory or intention (WP §3, §12.9).
**Current state: 0 / 15 AUTHORISED** — the honest position until sign-offs exist.

## The flip mechanics (do this per claim, only after the real sign-off)

In `assurance-case.json`, for the claim, set the reviewer/authority blocks:

```json
"reviewer":  { "scope": "…", "eligible_non_author": true, "status": "done", "name": "<real reviewer>" },
"authority": { "decision": "…", "holder": "<real authority + role>", "status": "done" }
```

Then:

```
python3 docs/assurance/validate_assurance.py
```

The claim's verdict changes to `AUTHORISED`. Record the evidence in the table below at the same time
(who signed, date, where it's minuted) so the flip is auditable.

## Per-claim unlock conditions + evidence slots

Fill the **Evidence** column only when it has genuinely happened (name · date · ref). Until then the
claim stays BLOCKED — correctly.

| Claim | Real event that unlocks it | Eligible signer(s) | Evidence (name · date · ref) | Status |
|---|---|---|---|---|
| CL-1 | evidence-semantics + transport review signed; public-safe demo authority records decision | Michael + Wesley | | BLOCKED |
| CL-2 | non-author content/HCI review; content sign-off | non-author HCI reviewer | | BLOCKED |
| CL-3 | Section 09 vocabulary ratified; evidence-semantics review | Michael (RATIFY-09-*) | | BLOCKED |
| CL-4 | HCI/eval-parity review; public-safe demo gate | non-author HCI / Fahmi | | BLOCKED |
| CL-5 | security/IAM review (real IAM replaces the stub) | Wesley (RATIFY-15-06) | | BLOCKED |
| CL-6 | non-author code review of the checker + Section 09 contract | non-author dev + Michael (RATIFY-09-04) | | BLOCKED |
| CL-7 | evaluation-parity review; ethics route for any human-effect claim | Fahmi (RATIFY-14-07/08) | | BLOCKED |
| CL-8 | Section 18 partner-route review + owner named | Section 18 owner | | BLOCKED |
| CL-9 | team ratifies the reconciliation register | team (RATIFY-19-04) | | BLOCKED |
| CL-10 | manual keyboard/screen-reader/AT testing done **and** non-author accessibility review | non-author HCI reviewer (C-BLOCK-03 / RATIFY-14-02) | | BLOCKED |
| CL-11 | controller/processor + lawful basis + DPIA signed | governance (RATIFY-15-02/04) | | BLOCKED |
| CL-12 | Bristol PGT ethics determination issued | PGT ethics (RATIFY-15-03) | | BLOCKED |
| CL-13 | security/assurance review of the app controls | security reviewer (RATIFY-15-07) | | BLOCKED |
| CL-14 | Section 08 accountable owner named (C-BLOCK-01) + evidence-semantics review | Section 08 owner + Michael | | BLOCKED |
| CL-15 | all load-bearing sources attested (28/28) **and** a non-author checks your records; your §26 acceptance completed | you (reading) + a non-author checker | | BLOCKED |

## What's realistically closest for you

- **CL-15** partly moves under your own steam: finish the reading + verdicts (→ `foundation-matrix.json`
  reaches 28/28), then a non-author spot-checks your records. Your reading is the long pole; the check
  is quick.
- **CL-6, CL-3, CL-14** unlock together the day Michael signs the evidence-semantics / checker contract
  — the same contract workshop as your Step 4 C-BLOCK-05 freeze.
- **CL-9** unlocks at team ratification (`RATIFY-19-04`) — put it on the next team agenda.
- Everything else is an institutional authority (ethics, DPIA, security, Section 08 owner). You
  *progress and evidence* those (draft the DPIA, submit the ethics application) but you cannot self-sign
  them — record the decision here when the named authority issues it.

**Done means:** all 15 read AUTHORISED *and* your Step-7 authorship pass is complete. Not before.
