# Decision D-012 — Hold inactivity out of need; validate against held-out signals only
*Append to `decisions.md`. Convention follows D-007…D-011.*

---

### D-012 · Hold adult inactivity out of the NEED composite and restrict validation anchors to held-out signals (remove validation circularity)

- **Status:** ADOPTED — implemented in code and tests on 2026-07-01; proposal §§6–8 updated to match.
- **Date:** 2026-07-01
- **Owners:** WS2 (Michael) with the evaluation/validation lead (Fahmi). Partner-facing wording routed through Dalila O'Grady as usual.
- **Relationships:**
  - **Refines** D-011 (§4 of that decision — "VALIDATION = triangulation of the activity-gap index against deprivation, Active Lives inactivity, and OHID Fingertips, with the facility layer as corroboration"). D-011 named anchors that were *also* need inputs; D-012 tightens the rule so validation anchors must be **held out** of the need composite.
  - **Consistent with** D-010 (methods right-sized for n ≈ 33) — this changes the *validation logic*, not the unit, the method family, or the sample size.
  - **Depends on** D-007 (IoD2025 as the deprivation source — deprivation stays *in* need) and D-008 (borough is the unit of analysis).
  - **Supersedes** the validation wording of Proposal §7 (v4) and the dual "need + validation" role labels in the §6 dataset table. Replacement text: "Proposal §§6–8 (v4, D-012 revision)".

**Context.** The activity-gap index is `z(need) − z(provision)`. As specified in D-011 and Proposal v4, the NEED composite combined deprivation (IoD2025) + Census demographics + **Active Lives inactivity**, and the index was then "validated by triangulation" against **deprivation, inactivity, and Fingertips**. Two of the three validation anchors — deprivation and inactivity — were themselves inputs to the need score. Correlating the gap against a variable used to build it is partly tautological: it measures the index's internal consistency, not its external validity. An examiner would reasonably read this as circular, weakening precisely the claim the evaluation section rests on.

**Decision.**
1. **Hold adult inactivity (Active Lives `pct_inactive_adults`) out of the NEED composite.** NEED = deprivation (IoD2025) + demographic risk (Census 2021: share aged 65+, disability, limiting illness / "bad" general health, economic inactivity). Inactivity is no longer a need input.
2. **Validation anchors = held-out signals only.** The gap is validated against signals it was *not* built from: adult inactivity (now held out) as the primary independent outcome, plus OHID Fingertips activity/health indicators where they are not entered into need, with the Active Places facility layer as corroboration. **Deprivation, being a need input, is no longer claimed as an independent validator.**
3. **Reclassify roles.** Active Lives inactivity moves from "need + validation" (dual) to **validation-only (held-out outcome)**. OHID Fingertips is likewise treated as a **held-out validation** source rather than a need-health input (health in the need score is already carried by the Census "bad health" indicator, so Fingertips-in-need was redundant).

**Rationale.**
- **Removes circularity.** External validity now means agreement with an outcome the index never saw. This is the standard hold-out logic and is the honest version of the claim in Evaluation §8.
- **Inactivity is the *right* held-out anchor.** Physical inactivity is the real-world outcome the "activity gap" is ultimately about, so "a wider gap coincides with more inactivity" is a genuine, falsifiable prediction — far stronger evidence than a within-construct correlation.
- **Cleaner conceptual separation.** NEED = upstream structural risk (who is likely underserved: deprived + demographically at-risk populations); VALIDATION = downstream outcome (are they in fact less active?). Provision stays the community-session layer; facilities stay corroboration (unchanged from D-009/D-011).
- **Deprivation rightly stays in need.** Deprivation is a need construct (D-007), not an outcome; the fix is simply to stop double-counting it as a validator.
- **Preserves multi-signal validation.** Inactivity + Fingertips (both held out) keep a genuine triangulation, now defensible.

**Consequences.**
- **Code — `src/pipeline/gap_index.py`:** `NEED_GROUPS` drops the `inactivity` group; `NEED_WEIGHTINGS` is re-expressed over {deprivation, demographic} (base `equal`; alternatives `deprivation_led`, `demographic_led`, replacing the old `inactivity_led`); `VALIDATION_SIGNALS = ["pct_inactive_adults"]` (held-out only). Module docstring and design notes updated.
- **Tests — `tests/test_analysis.py`:** validation assertions now require inactivity as a held-out anchor and assert deprivation is **absent** from the anchors; a new **perturbation proof** reverses the inactivity column and asserts the gap index is numerically identical (if inactivity leaked into need, the ranking would move). `test_analysis` and `test_run` both pass (`ALL ASSERTIONS PASSED ✓`).
- **Proposal (v4):** §6 dataset roles (Active Lives → validation-only; Fingertips → held-out validation), §7 need-composite sentence (inactivity removed), §7 gap-index validation sentence (held-out, not "deprivation + inactivity"), §7 success criteria, §8 evaluation, and §10 wording — all updated; decision-log range bumped to D-007–D-012.
- **No change on today's real feature table.** IoD, inactivity and facilities are not yet acquired, so on the current data NEED was already demographics-only and validation already could not run; the refinement is verified now on synthetic data and takes visible effect once those sources land.
- **Sensitivity now probes deprivation-vs-demographic weighting** (the two surviving need groups) rather than an inactivity weighting.

**Contingencies / notes.**
1. **One role per source.** When Fingertips activity indicators are wired into the pipeline, route each to exactly one role — need **or** validation, never both — to preserve the held-out property.
2. **Name collision to watch.** `pct_econ_inactive` (economic inactivity, Census — a **need** demographic) is distinct from `pct_inactive_adults` (physical inactivity, Active Lives — the **held-out** outcome). Similar names, different roles; do not conflate in code or prose.
3. **Supervisor awareness.** Note the held-out-validation refinement to Dalila O'Grady at the next supervision, as a strengthening of the evaluation design.

**Verification status (FACT).** Implemented and tested on 2026-07-01. `python -m tests.test_analysis` and `python -m tests.test_run` both pass; `python -m src.run_analysis` runs clean on the real 33-borough table with no ranking change (the refinement is behaviour-preserving until the held-out sources are acquired).
