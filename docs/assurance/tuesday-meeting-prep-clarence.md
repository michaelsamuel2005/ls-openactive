# Meeting prep — Clarence's lines (ratification meeting, 2 September 2026, 18:00)

Everything asked of me is done and pushed. This page is what I read from.

---

## 1. My two deliverables — both closed before the meeting

### 4.3 — Q disposition: the slate-order pointer (this closes the item)

**Line:** *"Yes — the projected decision digest covers slate content **and** order, so `Q → invariant_not_collected` closes unconditionally."*

**The mechanism, if asked:**

- `_decision_digest` (`validate_conditions.py`) projects the envelope to the plane, takes the whole
  `payload.decision`, pops only its own stored `digest`, and hashes the remainder.
- `canonical()` is `json.dumps(obj, sort_keys=True, …)` — **`sort_keys` sorts object keys only; JSON
  array order is preserved** — so `candidates[]` order is inside the hash.
- Content and order fields survive projection: `candidates[].candidate_id`, `.rank` and `.pool` are all
  `PUBLIC_SAFE` in `disclosure-classes.json` (lines 87–89).

**Demonstrated three ways** against `supported.json` — each changes the digest:
reverse the `candidates[]` array → differs; change one `candidate_id` → differs; swap the two `rank`
values → differs. Order is pinned twice: by array position *and* by the rank field.

### 4.4 — First-screen depth + the v0.2.1 vintage label

**Line:** *"Depth is a rule, not a number: judged depth = experienced depth = the full certified slate,
variable per task. No cap, no pagination, identical across arms. And the v0.2.1 successor is in."*

- Measured, not chosen: `results.html` iterates the whole candidate list with no slice; `build_view`
  applies no truncation; rendered count equals slate length in every scenario; no next-page /
  show-more / load-more control exists in the served HTML.
- Recorded as `first_screen_depth` in `condition-manifest.json` with method, measurements and
  consequence. The 2/0/0 figures are labelled **demonstration fixtures** — sizing uses expected slate
  length under the minted benchmark, never these.
- **v0.2.1 successor** (Michael's byte-check finding): new `frozen_vintage_role` labels
  `2026-06-30` as a demonstration value, not an operative freeze — it re-freezes to the ratified
  evaluation vintage when the ≥20-task benchmark is minted, and no vintage-dependent result may be
  reported from it until then. `vintage_note` now separates the operative *mechanism* from the
  placeholder *value*.
- **Position to hold:** no cap by default. A cap is a design change — it does not exist in the
  interface today, would have to be implemented, and must land identically across P0/P1/P2 to
  preserve the C-BLOCK-06 confound-proof. Nobody has yet given a reason a user should see less than
  the certified slate.

---

## 2. Where I assent

- **1.1 Structure = skeleton v0.2** — adopt. Eight chapters, budgets summing to exactly 30.0pp
  (`3+5+4+4.5+3+4+5+1.5` — I re-added it), Ch6 mine at 4.0pp with six sections. Verified against the
  compiled PDF and the zip.
- **1.2 Chapter parity + editor-labour line** — adopt. The editor role being recorded as a
  contribution matters now the Peer Evaluation Form is a live assessed instrument: it is real labour
  that otherwise leaves no visible authorship.

---

## 3. Two things to raise

### (a) Item 3.4 is voted before its dependency exists

3.4 (SOURCE-CONFLICT-M01) reads *"prepared at the C-BLOCK-05 workshop, ratified here … REC: as
workshop prepares."* But the §09 workshop is **two days after** this meeting (logistics line: 4 Sep,
18:00). So on the night there is nothing prepared to ratify. This is the agenda's own stated principle
— *"items are ordered so nothing is voted before its dependency."*

**Proposal:** defer 3.4 to a named follow-up immediately after the §09 session — async ratification on
the workshop's recorded disposition, or a 10-minute slot later that week. Everything else in Block 3
stands.

### (b) The day names don't match the dates

Checked against the calendar: **2 September 2026 is a Wednesday**, not a Tuesday. 4 September is a
**Friday**, not a Thursday. This is corroborated by Alex Williams' supervision invite for
*"Tue, 25 Aug"* — 25 August 2026 is indeed a Tuesday, which makes 1 September the Tuesday and
2 September the Wednesday.

Same drift downstream: the submission deadline of **18 September is a Friday** (not Thursday), and the
presentation on **22 September is a Tuesday** (not Monday).

**Proposal:** confirm by *date*, not by day name, before anyone books around it — say explicitly
whether the meeting is Tue 1 Sep or Wed 2 Sep. Deadlines are unaffected (the Blackboard dates are what
bind: 18 Sep 13:00, presentation 22 Sep 11:00) but the day names in our own documents should be
corrected so nobody plans a final week against the wrong weekday.

---

## 4. After the meeting

Chapter 6 drafting is already under way against skeleton v0.2 — six sections, 4.0pp — and chapter
drafts go to Dalila and Alex around 8–10 September.
