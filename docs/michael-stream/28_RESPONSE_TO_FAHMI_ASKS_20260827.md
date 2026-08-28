# Response to Fahmi's "What I need from Michael" (19 Aug) — all twelve items

**Date:** 27 August 2026 · **Prepared for Michael's review before sending** — items 5–7 are *your personal decisions*; everything else is drafted as your answer and ready to send once you confirm.
**Context that changed since Fahmi wrote it (19 Aug):** the deadline moved to **22 Sep 23:59** (his 24/26/29 Aug need-by dates were set against 4 Sep — everything gains ~18 days); Wesley's full acquisition landed (H1: 2.33M S0 records, 95.5k located-London; H2 built; a new snapshot harvested overnight 26–27 Aug, delivery incoming); and the MS/WY/FA review loops all closed. His asks get *better* answers now than they could have had on time.
**Provenance:** AI-assisted, PROPOSED; role acceptances and the date commitment are Michael's human acts.

---

## §1 Blocking items

**1. S1/S1b delivery date — the answer he says everything depends on.**
Proposed commitment, in exactly the form he asked for (a committed date + a pre-agreed dated fallback):

> **Committed: S1 (parent-inheritance reconstruction) and S1b (schedule-expansion) deterministic outputs on the H1 corpus, delivered by Wednesday 10 September.** H2 follows if time allows; H3 is never touched (your §4 — agreed, see below). **Fallback, agreed and dated today:** if the outputs are not in your hands by 23:59 on 10 September, your §5 activates automatically — F-09 becomes written specification plus a dry run on synthetic outputs, and H-P is recorded as *unexecuted rather than failed*, decision dated 27 August.

Why 10 Sep is honest rather than optimistic: the real corpus is in hand this week (receipt protocol running); the S1b expansion logic exists as the tested slice prototype; S1 inheritance follows the M-06 table (built, 59 rows) over the ScheduledSession→SessionSeries join that Wesley's manifest shows is the workload (1.97M no-coord children, `"lineage_metrics": "pending S1 (Michael)"`). Twelve working days is enough to make it real *if it is the only major build*, which is why the arbiter decision (item 5) matters.

**2. B0 baseline unacceptable-decision rate on DEV.** Not computable today — it requires the engine running over a DEV vintage, i.e. it sits strictly downstream of item 1. Committed as **the first number produced from the S1 run: due with or before the 10 Sep delivery, computed on H1-DEV under your F-04 partition**. If the §5 fallback triggers, this item stops mattering by his own note. (No interim guess will be supplied — an anchor for a risk ceiling must not be invented.)

**3. Which arms will actually exist.** Answerable **today, from the repository**: the surfaces that exist are the certified evidence engine plus **Clarence's three presentation conditions P0/P1/P2** (same terminal DecisionEnvelope, presentation-only differences, per his C-17 condition manifest — P2 adds the conversational route, which after MS-9 surfaces unsupported constraints instead of guessing). **No recommender was built** — his own F-14 records it, Wesley's §5.2 remit confirms no retrieval/reranking or Bayesian preference engine exists in any branch, and my sweep of all 13 branches yesterday confirms it. So: every arm whose definition requires a recommender does not exist; there is **no eligible superiority comparator**; the evaluation is an evidence-communication comparison across P0/P1/P2 plus baseline, exactly as his eligibility matrix concluded. He should keep F-02 §10's reason rewritten in those terms (see item 6).

**4. Lineage pack format — defined here, v0.1 PROPOSED, enough to pilot judgment 3 now.** One pack per assessed decision, one JSON object, seven parts:

| Field | Content |
|---|---|
| `decision_ref` | query id + terminal decision + `decision_digest` (matches the DecisionEnvelope the assessor is judging) |
| `candidates[]` | per candidate: `candidate_id`, pool, rank |
| `evidence[]` | per predicate: `predicate_id`, evidence state (T/F/U/B), grade (`explicit` / `schedule_derived` / `specification_default`) |
| `lineage[]` | per evidence atom: source feed id + item id + RPDE `modified`, the JSON path(s) read, the transformation/interpretation rule id **and version** (M-05 register id), and for schedule-derived values the expansion inputs (schedule hash, occurrence index) |
| `receipts[]` | content digests binding each atom to the retained raw page (`pages.csv` sha256 row ⇒ byte-level ground truth) |
| `versions` | corpus vintage, interpretation version, engine version, seed id |
| `limits` | what the assessor may NOT infer (scope/collection qualifiers, unevaluated fields) |

Assessors therefore reconstruct from lineage only, tracing any value from decision → rule → source bytes without seeing the engine. Format frozen as v0.1 for his pilot; field-level schema follows with the 10 Sep delivery. If he needs a worked example before then, one can be hand-built from a census2 record against the M-05/M-06 tables.

## §2 Role decisions — YOURS to make (recommendations only)

**5. Arbiter on usefulness/relevance (+ hours estimate).** The one to be careful with: it needs the F-05 v0.3 codebook read first and arbitration hours in mid-September — exactly when S1 lands and chapters are drafted, and item 1's date is credible only if S1 is your sole major build. *Recommendation:* **accept conditionally and capped** — "yes, up to 4 hours in w/c 15 Sep, codebook read by 5 Sep; if arbitration volume exceeds that, we reassign the overflow at the meeting" — or decline and propose Clarence/Wesley. Ask Fahmi for the expected judgment count before finalising the cap.
**6. Non-author reproducer of headline tables.** Bounded (~2–3h, ~17–20 Sep), mechanical (re-execute frozen code on frozen inputs, hash-compare), high value as report reproduction evidence, and you are cleanly non-author. *Recommendation:* **accept**, scope stated as mechanical reproduction, not statistical review.
**7. Locked-run custodian.** Light duty (hold the sealed analysis plan, release at execution, log access), and you don't author his analysis so you are eligible; the consideration is role-budget — the team must also staff M-08's non-Michael custodian from the same three people. *Recommendation:* **accept**, and note at the meeting that custody roles now sit Michael↔Fahmi symmetrically (you hold his lock; a non-you custodian holds M-08), which is tidy rather than conflicted.
**8. F-02 review (~1h, named, scoped).** *Recommendation:* **accept, this week** — name the date in the reply.

## §3 Engine-output commitments (9–12) — all four: YES, and cheaply

These are already the architecture's own rules, restated as his interface: **(9)** typed failure codes `timeout` / `crash` / `malformed_output` emitted, never swallowed — same fail-closed family as the checker's typed exits; **(10)** terminal DecisionEnvelope with evidence state and digest per response; **(11)** corpus/interpretation/engine hashes + seed id on **every result row**; **(12)** the shared terminal referent produced-and-verified, never hardcoded — accepted as a **locked-run precondition**, which also finally closes the F-12 M-2 blocker on his CL-7 sign-off. All four bind to the 10 Sep delivery; if §5 triggers they remain in the written spec.

## §4 H3 — agreed, and it changes this week's data handling

Committed: **nothing runs against H3.** Development and the S1 build use H1 (and H2 where already exposed) only. **Action item this affects immediately:** Wesley's overnight 26–27 Aug harvest is very likely the newest clean vintage — the receipt message to him must ask **"which vintage is this delivery (H3 or later)?"**, and if it is the clean one, the receipt protocol runs integrity-only (hash the zip, spot-check pages against pages.csv digests, record, **seal**) with *no analysis, no S1 development, no peeking* — quarantined as the robustness holdout. One line added to the Wesley ask accordingly.

## §5 Fallback — agreed now, dated

Recorded above under item 1: automatic activation at 23:59 on 10 September, decision dated 27 August — precisely so it is "dated before the deadline rather than discovered after it," per his own words, redated for the corrected submission date.

---

## Ready-to-send reply (paste to Fahmi once you've settled items 5–7)

> Fahmi — answers to all twelve, sorry for the lag; the world moved in our favour since you wrote it (deadline is now 22 Sep 23:59, and Wesley's full corpus landed — H1 alone: 2.33M S0 records, 95.5k directly-located London).
> **1.** Committed: S1/S1b deterministic outputs on H1 by **Wed 10 September**. Fallback agreed now, dated today: not delivered by then → your §5 activates automatically (F-09 = spec + synthetic dry run; H-P recorded unexecuted, not failed).
> **2.** First number out of that run, on H1-DEV under your F-04 partition — with or before 10 Sep. No invented interim anchor.
> **3.** Arms that exist: the certified engine + Clarence's P0/P1/P2 presentation conditions (same envelope). No recommender exists anywhere in the repo — your F-14 stands — so no superiority comparator; it's an evidence-communication comparison. Rewrite F-02 §10's reason in those terms or I'll take the role per item 6.
> **4.** Lineage pack v0.1 attached/defined: decision_ref + candidates + evidence states/grades + per-atom lineage (source item, JSON path, rule id+version, expansion inputs) + receipts to retained raw bytes + versions/seed + limits. Enough to pilot judgment 3; full schema ships with the delivery. Want a hand-built worked example this week?
> **5.** Arbiter: [accept, capped at ~4h w/c 15 Sep, codebook by 5 Sep / decline — what's the expected judgment count?]
> **6.** Non-author reproducer: accept — mechanical re-execution + hash-compare, w/c 15 Sep.
> **7.** Locked-run custodian: accept — sealed plan held, released at execution, access logged.
> **8.** F-02 review: accept — 1h, by [date this week].
> **9–12.** All four: yes, as binding output contract — typed failure codes never swallowed; terminal envelope + digest per response; hashes + seed on every result row; shared referent produced-and-verified as a locked-run precondition (which also closes your F-12 M-2).
> **H3:** agreed, nothing touches it. Checking with Wesley which vintage the new delivery is; if it's the clean one it gets sealed on receipt — integrity checks only.

## Register effect

Item 1's commitment + fallback should be recorded as a dated decision (next D-number after the 15 July changeset lands, or in your stream's decision records now, migrated later); items 5–8 acceptances go to Fahmi's F-registers under your name and date; §4 adds a quarantine line to the S0 receipt protocol. Fahmi's unblock does not close any M-gate directly, but item 1 *is* the M-09/M-10 schedule commitment, now with an external consumer and a dated fallback — which is exactly what makes a delivery date real.
