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
