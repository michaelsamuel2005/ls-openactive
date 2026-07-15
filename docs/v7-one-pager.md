# v7 — the scientific core, on one page

**Status: DRAFT for team ratification, 2026-07-15. NOT ratified. NOT adopted.**
Depends on D-021, D-022, D-023 (all **PROPOSED**). If D-021 is rejected, this falls with it.
Sources: `docs/execution-blueprint.md` §§1–2 (design), `docs/brief-traceability.md` (alignment),
`docs/decision-log.md` D-021→D-023 (evidence and constraints).

---

## Title

> **Determinable Discovery from Incomplete Opportunity Data: publication-process effects and
> query-level fitness for use in London's OpenActive ecosystem**

Provisional. The working title "Closing the Activity Gap" — London Sport's own priority
framing — is retained as **motivation only**, not as a description of what this project measures.

## Aim

> To determine which constraint-based searches are supported determinately by a reconciled
> London OpenActive corpus, identify the publication and processing mechanisms that cause
> indeterminate results, and quantify which validated repairs most improve query-level
> discovery coverage.

## Research questions — exactly three

| | Question | Permitted conclusion |
|---|---|---|
| **RQ1** | **Corpus validity.** Which feeds, entity types, parent–child structures and semantic fields are actually represented, and what acquisition or extraction losses constrain discovery? | Specific structures/fields are present or absent, per platform and per feed kind, *for this vintage*. |
| **RQ2** | **Discovery determinability.** Across a prespecified benchmark of London searches, what proportion return enough determinate matches, only indeterminate candidates, or no observed listed match? | A profile over a frozen query set — never an intrinsic property of London or of OpenActive. |
| **RQ3** | **Mechanism and repair.** How much do parent resolution and selected secondary mechanisms change determinable discovery coverage, for which constraints, and at what coverage/error cost? | Named mechanisms materially do / do not change defined outputs. |

**RQ1 now has a measured answer** (D-025, Check 2): across 14,790 resolved children, the
acquisition/extraction loss that "constrains discovery" is quantified per field —
`location` **100.0%** and `category` **97.0%** are published-but-destroyed by child-only
extraction (**instrument-side**), while `level` **100.0%** and `activity` **97.0%** are
never published at all (**publication-side**). Both mechanisms are real, complementary, and
now measured rather than argued.

**No fourth RQ.** The prototype is an experimental surface for RQ3, not another research programme.

## Falsifiable central proposition

> Correct corpus reconstruction and uncertainty-aware retrieval materially change the result
> or interpretation of prespecified London discovery queries relative to child-only,
> closed-world filtering.

**How it dies:** if reconstruction and uncertainty representation do **not** materially change
the outcome, that bounded null is the result, and the improvement claim is withdrawn. The
threshold is set **before** the contrast is run (D-023) and never after.

---

## Kill rules — pre-committed, non-negotiable

Each is a *pre-declared* action, not a discretionary judgement. Firing one is a result, not a failure.

| # | Trigger | Action — no renegotiation after the fact |
|---|---|---|
| **K1** | The parent pointer is **not** materially prevalent on the child records the primary ablation acts on (measured **per `kind`**, never pooled) | The ablation is null by construction. Do not run it; report the prevalence finding instead. **STATUS: DOES NOT FIRE for session feeds** — `superEvent` on `ScheduledSession` = **18,935/18,935 = 100.0%** (census, 173/173 declared sites, 124 publishers). **FIRES for facilities** — `Slot` = **0/92,359 = 0.0%** ⇒ **the primary mechanism study is scoped to session feeds only.** |
| **K2** | The primary contrast shows no material effect at the pre-declared threshold | Report the bounded null with its uncertainty. **Withdraw the improvement claim.** Do not re-cut the threshold, the query set, or `k`. |
| **K3** | Corpus gate fails — `attempted ÷ declared` cannot be reported at catalogue/site/feed level, or failed endpoints are not visible | All ecosystem-wide claims suspended. First contribution becomes corpus/pipeline reconstruction. **STATUS: PASSES** — census reports **173/173 = 100.0% of declared**, 969 endpoints each with a status, 52 failures (5.4%) retained and visible. |
| **K4** | A field's "missingness" cannot be attributed to publication-side vs instrument-side from retained raw | That field is **excluded** from any mechanism or repair claim. Unattributed missingness is the exact defect that retired the 7 July corpus (D-021). **STATUS: DOES NOT FIRE for the 13 traced fields** — attribution is now measured per record (D-025, Check 2): every field is classed instrument-side or publication-side over 14,790 resolved children, with UNRESOLVED reported, never folded into absence. |
| **K5** | The benchmark query set is not frozen with provenance before results are seen | The prototype is labelled **exploratory only** and makes no comparative claim. |
| **K6** | A non-author cannot reproduce the headline table/figure from a clean clone | **No exceptional claim.** **STATUS: DOES NOT FIRE — re-tested 2026-07-15, correcting an earlier claim that it did.** The scripts producing every current headline figure (`src/harvest_pilot.py`, `src/verify_licences.py` → `results/census_*.csv`, `results/licence_audit.csv`) have **exactly one third-party import — `requests` — and it is declared in `requirements.txt`.** A clean clone reproduces the current evidence chain. *(The retired corpus is a separate matter — see F-DEP.)* |
| **K7** | Any reference is cited without a team member having read it | It is marked `TODO-VERIFY` and **may not appear in a submitted artefact.** **STATUS: CURRENTLY FIRING** — Razniewski & Nutt is the blueprint's only citation and nobody has read it. |

**One kill rule is firing right now: K7** (an unread citation). It is fixable this week and not
by harvesting more data — someone has to read the paper.

**K6 was previously reported as firing. It is not** — that claim was tested and withdrawn
(see the row above). The confusion came from conflating two different reproducibility
questions: *the retired corpus* is permanently unrebuildable (F-DEP), while *the current
evidence chain* reproduces from a clean clone. Only the second is what K6 tests.

---

## Constraint of record: no further partner elicitation (D-022)

London Sport's requirement set is **fixed, complete and enumerable**, and consists of exactly
two verified primary artefacts:

- **P1** — `LS machine learning projects_29-05-2026.pdf`, pp.16–19 (brief) and pp.22–24
  (output framework). Partner-authored: PDF metadata `author: Josef Baines`, named in this
  project's records as **J. Baines, Insight Manager, London Sport**; created 2026-06-03.
- **P2** — the challenge listing headed **"1. London Sport 1"** (sole source of that label).

There will be no clarification of ambiguous clauses, no scope negotiation, and no acceptance
criteria beyond the brief's own words.

**Therefore:**

1. **Do not claim "100% partner alignment."** Without elicitation it is unknowable. What *is*
   achievable and fully within the team's control is **brief traceability**: every clause
   controls a research choice, a deliverable, an acceptance test and a stated limitation.
   That is `docs/brief-traceability.md`, and it is the **alignment ceiling**.
2. The permitted alignment claim is exactly: *"The project is maximally and transparently
   aligned to the supplied London Sport overview through a documented task-derivation process.
   No claim is made that the selected task was separately validated or prioritised by the
   partner."*
3. Every ambiguity is closed by **documented interpretation**, marked `[INTERPRETATION]`, and
   defended — never by assumption presented as fact.
4. **"The partner didn't specify" is not available as a defence** for an unmet clause. The
   clauses are fixed and enumerated.

> **UNVERIFIED — the team must supply this before ratification.** The *reason* elicitation is
> unavailable, and its *date*, are recorded nowhere. Do not ratify this section until written down.

---

## Why this is on-brief, not a retreat from it

The pivot has been discussed internally as a retreat from the equity study. Against the
verified brief it is the opposite. P1 p.22 names **"DATA QUALITY AND SUITABILITY ASSESSMENT"**
as a **required output type**, itemising verbatim: "Completeness of the data" · "Missing or
inconsistent fields" · "Issues with data granularity" · "Any assumptions made" · "Limitations
in using the data for modelling or forecasting" · "Areas where findings should be treated with
caution."

**That is a line-by-line description of D-021.** `[INTERPRETATION]` — this is the team's
reading of O3's scope, not a partner statement of intent.

## Honest standing against the five required outputs (P1 p.19)

| Clause | Verdict, 2026-07-15 |
|---|---|
| R1 — understand the ecosystem | **Met, strongly.** Census: 173/173 declared sites, 124 publishers, 217,743 items. |
| R2 — "Highlight various approaches used across the country." | **Not met.** No literature review; no national scan; `docs/references.bib` does not exist. |
| R3 — challenges/opportunities in how Londoners search | **Mechanism evidenced; artefact not built.** |
| R4 — propose interventions | **Proposed; not built, not evaluated.** |
| R5 — embedding into London's system | **Not addressed.** |

**One of five.** R2 and R5 depend on no further harvesting and can start today. This is a
draft-stage project with a strong evidenced data-quality core and four open obligations — and
saying so here is cheaper than an examiner saying it in September.

---

## What the team is being asked to ratify

1. **The title, aim, three RQs and the central proposition** above — or amend them now, before freeze.
2. **The seven kill rules**, including that **K1 scopes the primary mechanism study to session
   feeds only** on census evidence.
3. **D-021** (legacy corpus retired; **note the amendment** — the claim is now `platform × feed
   kind`, not "platform, not publisher"), **D-022** (brief provenance + elicitation constraint),
   **D-023** (answerability pivot, rejected alternatives, thresholds).
4. **That the alignment claim is "traceability", never "100% alignment".**

## Blocking items — none need more data

| | Item | Owner |
|---|---|---|
| 1 | **Misquotation of the partner inside quote marks.** Both primaries read "tailored **specifically** to London's diverse communities"; the proposals drop "specifically". Fix every artefact. | unassigned |
| 2 | **F-DEP — now CLOSED as a task, and it strengthens D-021 rather than blocking it.** Re-examined 2026-07-15: the legacy corpus is unrebuildable for **three independent reasons**, not one. `openactive` is declared in **neither** `requirements.txt` **nor** `environment.yml`; it is **not installed** in the environment; and **`notebooks/load_dataset.ipynb` has never been committed on any branch** — the corpus-building code is not in the repo *at all*. This is not a gap to fix: the corpus is **retired** (D-021), and this is *why it cannot be salvaged*. No forward dependency exists — `harvest_pilot.py` uses plain HTTP. **Nothing to do; cite it as evidence.** | *closed* |
| 3 | **K7.** Razniewski & Nutt unread; `docs/references.bib` absent. | unassigned |
| 4 | **Neither primary brief artefact is in the repo.** P1 sits in one member's Downloads; P2 only inside a zip. No teammate can check a single quotation. | unassigned |
| 5 | **`src/recommender/` has never been committed by anyone.** Bus-factor risk on the largest build effort to date. | Clarence |
| 6 | **The reason/date for the elicitation constraint** is unrecorded (D-022). | team |

*Every figure on this page is computed by code in this repository and traceable to a results
file: `results/census_field_presence.csv`, `results/census_endpoint_log.csv`. Brief clauses are
quoted from P1 by direct PDF text extraction and from P2 by direct image reading, 2026-07-15,
and machine-checked against the deck.*
