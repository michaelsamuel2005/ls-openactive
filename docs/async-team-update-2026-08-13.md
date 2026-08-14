# Async update — Clarence's stream (can't attend the 13 Aug meeting)

**Branch:** `clarence/c-block-05` · **PR:** open · **Maturity:** research_demonstration only.
**One-command check (any machine):** `python3 docs/assurance/validate_assurance.py` →
*Graph SOUND, 14 suites green, 15 claims all BLOCKED pending your sign-offs* (that's the expected,
honest state — not a failure).

## TL;DR
My whole stream is built, tested, and green on **both macOS and Windows**. It is deliberately at
"green evidence, BLOCKED pending human sign-off." **What I need from the team tomorrow is decisions and
reviews only you can make** — listed under "Asks" below. Nothing of mine is blocking you; several of
your decisions are blocking me.

## What is functioning (demonstrable now)
- **Public discovery app** — runs locally; all four honest outcome states (supported / no listed match
  / can't-answer / service problem), the conversational route (clarify + confirm), compare (no
  "winner"), and a no-JavaScript core.
- **Staff assurance app** — role-gated (403 without a role); public-state replay, failure-chain,
  action-card workflow (no skip of review/approval; only an authoriser can send), 4 workspaces.
- **Independent certificate checker** — 13 negative cases + branch mutation, 0 survivors.
- **14 executable check/test suites** — all pass (contracts, checker, register, wording, IA,
  action-cards, conditions, privacy, security, ethics, both app slices, conversation, K7 reading).
- **Executable assurance case** — 15 claims, graph SOUND, evidence green, orphan-free.
- Scope guardrails hold: no conformance / human-effect / deployment claims are made anywhere.

## What I've delivered (on the branch)
Application contracts (C-BLOCK-05), certificate checker (C-09), reconciliation register (C-01, 15
blockers), evidence-language + linter (C-11), public & staff IA (C-04/C-06), both applications,
evaluation conditions + telemetry schema (C-17), privacy/security/ethics packages (C-13/14/15), and the
executable assurance case (C-16). This review pass I also verified everything on Windows, fixed a
Windows jsonschema crash and a disclosure leak (the failure page was naming an internal stage), and
built the CA-5 reading matrix with web-verified DOIs.

## Asks — decisions/reviews I need from you (please action even without me)
1. **Schedule the C-BLOCK-05 contract workshop (me + Michael + Wesley).** Everything downstream waits on
   freezing the envelope / terminal decision / disclosure-class schemas. This is the keystone — please
   give it the first date.
2. **Michael (evidence semantics):** confirm the C-BLOCK-05 enums/vocabulary; resolve **CA-2 /
   RATIFY-09-04** (may the claim-contract author also author the production interpreter, or must that
   split?). Unlocks CL-1/3/6/14.
3. **Wesley (transport/IAM):** version/compatibility rules, server-side enforcement of the disclosure
   classes, and real IAM to replace my role stub. Unlocks CL-5/CL-13.
4. **Fahmi (evaluation):** we jointly own the **`L_reliance` referent (C-BLOCK-15 / F-BLOCK-09)** — it
   must bind to the terminal DecisionEnvelope (identical across P0/P1/P2), not to displayed evidence.
   **Please assign this a single named owner.** Unlocks CL-7.
5. **Name the Section 08 accountable owner (C-BLOCK-01)** and bind it to a real decision-log ID (no
   invented RATIFY-08-*). Unlocks CL-14.
6. **Name the eligible non-author HCI/accessibility reviewer (C-BLOCK-03 / RATIFY-14-02)** — I can't
   review my own applications. Unlocks CL-10.
7. **Ratify a small contract change (F1):** I reclassed `failed_stage` PUBLIC_SAFE → STAFF_AGGREGATE so
   the public failure page no longer names an internal stage. Also please confirm three disclosure
   questions from my audit: what `budget_state.budget` actually is (EVOI vs user budget), the
   `predicate_id` public/staff split, and which provenance versions are public.
8. **Team ratifications:** RATIFY-19-04 (accept my work package) and RATIFY-19-06 (public/staff product
   lead — C-BLOCK-02).

## Institutional gates (progressing in parallel — named authorities decide, not me)
Bristol PGT **ethics** route (RATIFY-15-03), **DPIA** / controller-processor / lawful basis
(RATIFY-15-02/04), **security** review (RATIFY-15-07). I maintain the evidence pack for each; I can't
self-sign them. Happy to have these put on the agenda so owners are named.

## What I'm doing next (my in-flight work — not blocking anyone)
K7 primary-source reading + my own verdicts; authorship pass rewriting the scaffolds in my words; and
my two independent cross-reviews — C-19 (Michael's evidence stream) and C-20 (Fahmi's evaluation
stream).

*Questions before or after: reply on the PR or ping me. I'll pick up any decisions from the minutes.*
