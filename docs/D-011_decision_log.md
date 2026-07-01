# Decision D-011 — Adopt the tiered, validated external-data architecture
*Append to `decisions.md`. Convention follows D-007…D-010.*

---

### D-011 · Adopt the tiered, validated external-data architecture (two-layer provision; triangulated validation; PTAL-weighted accessibility)

- **Status:** PROPOSED — adopted for WS1 implementation; contingencies below to close before any external figure is published.
- **Date:** 2026-06-30
- **Owners:** WS1 (Wesley) with WS2 (Michael). Any partner-data question routed through Dalila O'Grady — never to London Sport directly.
- **Relationships:**
  - **Extends** D-009 (provision-layer separation) — from "do not merge the commercial national catalogue" to a positive two-layer architecture.
  - **Depends on** D-008 (borough is the unit of analysis) and D-007 (IoD2025 as the deprivation source).
  - **Consistent with** D-010 (methods right-sized for n ≈ 33) — this decision changes *data*, not *methods*.
  - **Supersedes** the data content of proposal v3 §6 (single-source provision; small-area framing; single-source validation). Replacement text: "Proposal §6 (v4)".

**Context.** Proposal v3 §6 listed external datasets without a role discipline, implied a small-area unit, and validated the gap against a single source. WS1 then fixed the borough as the unit (D-008) and confirmed data sufficiency at that scale. The open question — *which* external data, at *what* scope, and validated *how* — is what this decision settles.

**Decision.** Adopt **Tier 1 + Tier 2** of the Data Sources & Integration Plan:
1. **Provision = two separate layers**, never merged: community sessions (Open Sessions, primary) and facility stock (Active Places Power, independent). *(Extends D-009.)*
2. **NEED composite** from IoD2025 + Census 2021 demographics (age, disability, limiting illness) + Active Lives inactivity, reported under **≥2 weightings** (sensitivity).
3. **ACCESSIBILITY** via an E2SFCA measure **weighted by PTAL**.
4. **VALIDATION = triangulation** of the activity-gap index against deprivation, Active Lives inactivity, and OHID Fingertips, with the facility layer as corroboration.
5. **Tier 3** held as documented, question-driven candidates only (scope-creep guard).

**Rationale.**
- Every dataset serves exactly one of the three roles (need / provision / accessibility+validation); nothing is added for show. This is the project's own discipline principle, applied.
- The two-layer split directly answers the examiner objection that one publisher gives a partial provision picture, and it *enables* triangulation rather than merely adding data.
- Multi-source validation (three independent signals) is materially stronger than the single-source check in v3.
- All Tier-1/Tier-2 sources are open-licensed and API/machine-retrievable → the pipeline is reproducible (LO1/LO5) and nationally scalable, with PTAL the sole London-bound layer.
- Because Active Lives is published natively at local-authority level, borough inactivity is a **direct measurement**, not a small-area inference — the ecological-inference risk of finer geographies is avoided.

**Consequences.**
- Proposal §6 is replaced (v4); the methodology section is unaffected (already revised under D-010).
- Variable names are fixed by the integrated schema; all code, figures and report text use those names.
- Integration/QA cost rises with more sources — mitigated by the Tier-1+2 cap and the already-tested feature pipeline (execution step 3).

**Contingencies (must close before publishing any external figure).**
1. **Active Places licence** — read the info/licence file bundled in the download; attribute Sport England. *(This is the one source not under a blanket OGL.)*
2. **PTAL is London-only** — excluded from the national-scalability claim.
3. **Active Lives borough estimates** carry wide confidence intervals — reported with CIs and used for ranking/validation, not precise point claims.
4. **Supervisor awareness** — Dalila O'Grady to be sighted on the adopted data architecture at the next supervision.

**Verification status (FACT).** All Tier-1 and Tier-2 sources were verified against their providers on 2026-06-30 (Census 2021 via Nomis bulk/API; ONS Dec-2021 exact-fit lookup, noting the Aug-2025 correction; Active Lives via Fingertips; Active Places downloads; PTAL 2023 grid). Access routes and join keys are confirmed and documented in the Acquisition Guide.

**Open assumption (ASSUMPTION, to confirm).** IoD2025 LA-summary join uses the LAD-code column as published; confirm its exact vintage/header before the headline deprivation figures are quoted.
