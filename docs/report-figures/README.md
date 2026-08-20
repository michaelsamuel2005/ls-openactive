# Report figures & tables (Group 41 — Execution section)

Generated from branch `clarence/c-block-05`, 2026-08-14 (all 14 suites green). **These are data
artefacts you can use directly.** The *prose* of each section is still yours to write — see
`docs/report-contribution-map.md` for what to cover.

## Files
- `architecture-two-projections.svg` — Figure: one DecisionEnvelope → two projections (§3.4/§3.6).
- `report-tables.tex` — the five tables below as paste-ready LaTeX (`\usepackage{booktabs}`).
- this README — Markdown previews + the two screenshots you capture yourself.

## Using the figure in LaTeX
LaTeX prefers PDF/PNG. Convert the SVG once, then `\includegraphics`:
```
# any one of these:
rsvg-convert -f pdf -o architecture-two-projections.pdf architecture-two-projections.svg
inkscape architecture-two-projections.svg --export-filename=architecture-two-projections.pdf
# or open the .svg in a browser and "Print → Save as PDF"
```

## Two screenshots to capture (I can't screenshot your running app)
Start the apps (`docs/RUN-apps.md`), then capture:
1. **Public four states** (§3.4) — a 2×2 of `/discover?scenario=supported`, `…=no_match`,
   `…=indeterminate`, `…=service_failure` at `http://127.0.0.1:8000`.
2. **Staff workbench dashboard** (§3.5) — `http://127.0.0.1:8001/?role=analyst` (the card grid).

---

## Table previews (Markdown)

### T1 — Certificate checker: negative cases → outcome (§3.2)
Golden certificate → `PASS`; branch mutation kills all 8 branches (0 survivors).

| # | Injected defect | Outcome |
|---|---|---|
| 1 | Missing witness | `FAIL_MISSING_WITNESS` |
| 2 | Truncated evidence path | `FAIL_MISSING_WITNESS` |
| 3 | Swapped receipt | `FAIL_DIGEST_MISMATCH` |
| 4 | Forged hash | `FAIL_DIGEST_MISMATCH` |
| 5 | Stale vintage | `FAIL_VERSION_MISMATCH` |
| 6 | Incompatible schema/interpretation version | `FAIL_VERSION_MISMATCH` |
| 7 | `U`/`B` escalated to supported | `FAIL_ILLEGAL_ESCALATION` |
| 8 | Scope qualifier dropped | `FAIL_SCOPE_INCONSISTENCY` |
| 9 | Ineligible candidate in a supported slate | `FAIL_ILLEGAL_ESCALATION` |
| 10 | Certificate for another query | `FAIL_DIGEST_MISMATCH` |
| 11 | Predicate outside the certifiable fragment | `FAIL_UNSUPPORTED_FRAGMENT` |
| 12 | Unresolved receipt | `FAIL_UNRESOLVED_RECEIPT` |
| 13 | Duplicated / ambiguous identity | `FAIL_MALFORMED` |

### T2 — Field-level disclosure classes (§3.6)
Fail-closed: any unclassified field is dropped from every plane.

| Class (#) | Visible on | Representative fields |
|---|---|---|
| PUBLIC_SAFE (48) | public, staff, research | terminal decision, scope qualifier, recommendation action, coverage statement, candidate id/rank/pool, predicate evidence-state/mechanism/grade, digest, vintage |
| STAFF_AGGREGATE (15) | staff, research | internal score, model/policy version, latency, coarsened origin, failed stage, unevaluated feeds |
| STAFF_EVIDENCE (15) | staff, research | receipts (id, content digest), lineage note, why-not predicate/blocking state, claim verification |
| RESEARCH_RESTRICTED (5) | research only | episode id, trace id, editable-interpretation source span |

### T3 — Release-blocking invariants (§3.6)
2 valid fixtures pass all; 6 adversarial fixtures each caught by the targeted gate.

| Invariant | Guarantees |
|---|---|
| INV-DISCLOSURE | public projection contains only PUBLIC_SAFE fields (content-scanned) |
| INV-NONINTERFERENCE | mutating only non-public fields leaves the public projection byte-identical (CA-1) |
| INV-SYMMETRY | public & staff agree on decision, scope, action, coverage, candidate id+order, vintage |
| INV-REPLAY | retained public payload recomputes to the stored digest |
| INV-NO-UNVERIFIED | no claim with verification ≠ verified is renderable |
| INV-NO-COLLAPSE | no definite listing claim over a U/B predicate |
| INV-COVERAGE | every bounded_non_match carries a coverage qualifier |
| INV-SLATE-ORDER | array order equals certified rank; authorised slate holds only supported candidates |

### T4 — Staff role → capability matrix (§3.5)
Send is authoriser-only; review/approval cannot be skipped (§8.5).

| Capability | analyst | assurance | authoriser |
|---|:---:|:---:|:---:|
| view | ✓ | ✓ | ✓ |
| triage | ✓ | ✓ | — |
| draft | ✓ | ✓ | — |
| review | — | ✓ | — |
| approve | — | ✓ | — |
| send | — | — | ✓ |

### T5 — Executable assurance case: 15 claims (§3.6 / Critical Evaluation)
Graph SOUND, evidence green, all claims BLOCKED pending named non-author review + authority.

| Claim | Guarantee (abbreviated) | Verdict |
|---|---|---|
| CL-1 | public/staff never disagree; restricted values can't move public output | BLOCKED |
| CL-2 | unknown never rendered as a negative fact | BLOCKED |
| CL-3 | no unsupported factual token reaches a user | BLOCKED |
| CL-4 | certified slate and order preserved; abstention not bypassed | BLOCKED |
| CL-5 | restricted staff information cannot leak; role-gated | BLOCKED |
| CL-6 | forged/stale/swapped/escalated evidence rejected by the checker | BLOCKED |
| CL-7 | application effects not confounded with backend differences | BLOCKED |
| CL-8 | governed actions can't skip review/approval; send needs a role | BLOCKED |
| CL-9 | all pre-code reconciliation blockers dispositioned | BLOCKED |
| CL-10 | evaluated *toward* WCAG 2.2 AA within a tested matrix | BLOCKED |
| CL-11 | telemetry transient-by-default; no raw utterance/exact location | BLOCKED |
| CL-12 | every human-facing activity ethically gated with a fallback | BLOCKED |
| CL-13 | app-facing injection/output controls; no committed secret | BLOCKED |
| CL-14 | conversation converges on the certified decision; never decides truth | BLOCKED |
| CL-15 | every load-bearing source attested to K7 | BLOCKED |
