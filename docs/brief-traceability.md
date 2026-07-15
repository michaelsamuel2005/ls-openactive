# Brief traceability — London Sport 1 → research choice → deliverable → acceptance evidence → limitation

**Status: DRAFT for team ratification (2026-07-15). Not adopted.**
Companion to decision entries D-019/D-020/D-021 (all PROPOSED).

This document exists to answer one examiner question — *"where does this requirement come
from, and how do you know you met it?"* — with a citation rather than an assertion. Every
left-hand clause below is **verbatim partner text**, quoted from a primary source held
locally and verified by direct extraction. Nothing in the left-hand column is paraphrased,
reconstructed, or inferred.

---

## 0. Provenance of the brief (read this before trusting any row)

Two primary sources exist. They are **not interchangeable** — they differ in wording, and
each row below states which one it quotes.

| # | Source | What it is | How it was verified |
|---|---|---|---|
| **P1** | `LS machine learning projects_29-05-2026.pdf`, pp.16–19 and pp.22–24 | London Sport's own "Let's Move London" deck. Section headed **OPENACTIVE PROJECT**; slide title *"EXPLORING INNOVATIVE USE OF OPENACTIVE DATA TO INCREASE PHYSICAL ACTIVITY IN LONDON"* | PDF metadata `author: Josef Baines` (named in this project's own records as **J. Baines, Insight Manager, London Sport**), `creator: Microsoft PowerPoint for Microsoft 365`, `creationDate: 2026-06-03`. 25 pages, real embedded text layer; text extracted directly via PyMuPDF, not transcribed by eye. |
| **P2** | Challenge listing image, headed **"1. London Sport 1"** | The numbered partner-challenge listing. Prose restatement of the same brief. **Sole source of the label "London Sport 1"** — the deck never uses that name. | Read directly as an image. Held at `CODEX_FINAL_ADVERSARIAL_HANDOFF_BUNDLE.zip → image(4).png`. |

**Citation form used below:** `P1 p.NN` = deck page NN. `P2` = listing.

### 0.1 Provenance risks — stated, not hidden

- **Neither primary is in this repository, and neither may be committed to it.**
  **This repository is PUBLIC and carries no licence file.** P1 is London Sport's own
  unpublished deck, authored by a named employee; committing it here would **republish a
  partner's internal document to the open internet** without their permission. Absence of a
  confidentiality marking is not permission — copyright subsists automatically. **Do not
  commit P1 or P2.** Quoting clauses for academic criticism, as this document does, is a
  different and defensible act; republishing the artefact is not.

- **Verification without publication — the identity block below is the substitute.** Any
  team member holding the deck can confirm they hold the *same* artefact these quotations
  were taken from, and can then check every row themselves. This closes the bus-factor gap
  without distributing anything.

  | Source | SHA-256 | Size | Detail |
  |---|---|---|---|
  | **P1** `LS machine learning projects_29-05-2026.pdf` | `5afccb820391fc4dad999e4fdc0cc04f31da49efd11410a942603a4d0959bb9f` | 1,992,626 bytes | 25 pp · `author: Josef Baines` · created `2026-06-03T12:58:00+01:00` |
  | **P2** listing image (`image(4).png`) | `8bc9b29747c95ca4fc1f1d6042ac476c9108ab901151933760d2ac4969dd6707` | 580,032 bytes | Held in `CODEX_FINAL_ADVERSARIAL_HANDOFF_BUNDLE.zip` |

  Verify with `shasum -a 256 "<file>"`. A mismatch means you hold a **different** artefact
  and **must not** rely on these quotations until reconciled. *(A second copy,
  `…_29-05-2026 (1).pdf`, is byte-identical — same digest — so the duplicate is not a fork.)*

- **Still open — the team must decide.** (a) Ask London Sport whether the deck may be
  committed, or whether a citable public reference exists; and/or (b) circulate P1 through
  the team's own private channel (email/Teams/OneDrive), **not** this repo. Until one of
  those happens, quotations are checkable only by members who already hold the deck.
  **This is a genuine residual gap against output O8**, and it is recorded rather than
  closed by wishful thinking.
- **P1 is a deck, not a specification.** Slide bullets are elliptical ("London Sport –
  strengthen its use of…"). Where a bullet is not a grammatical sentence it is quoted
  exactly as it appears and **not silently completed**.
- **The deck is dated 29-05-2026 in its filename but its PDF was created 2026-06-03.** The
  brief predates every architecture decision in `docs/decision-log.md` from D-019 onward.
- **No further partner elicitation is available to this team** (see §4). The brief text is
  therefore *fixed input*: ambiguities in it must be resolved by documented interpretation,
  never by asking. Every interpretive leap below is marked **[INTERPRETATION]**.

### 0.2 A live defect this document found

The project's own proposals **misquote the partner inside quotation marks.**

- **P1 p.19 and P2 both read:** "…recommendations tailored **specifically** to London's
  diverse communities."
- **`Closing_the_Activity_Gap_Project_Proposal.pdf` p.1 renders it, inside quote marks, as:**
  "new models, prototypes or recommendations tailored to London's diverse communities".
  `Updatedprojectproposal.pdf` p.3 does the same.

The word **"specifically"** is dropped from a direct quotation. This is not pedantry: it is
the difference between *making something for* diverse communities and *targeting it at*
them, and it weakens the single clause that most justifies an equity lens.
**Fix required in every proposal artefact before submission.**

> **Note against this document itself.** A first draft of this file committed the same
> class of error twice — rendering P1 p.19's "Highlight various approaches used across the
> country." as a reconstructed fragment, and its "could improve reach, engagement and
> equity of access" as "improve reach and engagement", dropping the equity clause. Both
> were caught by machine-checking every quoted span in this file against the deck's
> extracted text and are now corrected. **That check is the acceptance test for this
> document and must be re-run whenever it is edited.** A traceability matrix that
> misquotes the brief while accusing others of misquoting the brief is worse than none.

A second phrase, "new solutions that improve audience engagement…", is **correctly** quoted
from **P2** — but it does **not** match P1 p.18, which reads "New solutions **required to**
improve…". Anyone quoting it must attribute it to P2, not the deck.

---

## 1. Required outputs (P1 p.19) — the five the brief explicitly names

The brief enumerates exactly five under the heading "**Required outputs:**". These are the
only clauses in the brief phrased as requirements. Verdicts are as at 2026-07-15.

### R1 — "Demonstrate a clear understanding of the current OpenActive ecosystem."

| | |
|---|---|
| **Research choice** | Treat OpenActive as a **socio-technical publication system, not a census of provision**. Characterise it by walking the canonical catalogue collection → 4 catalogues → declared dataset sites → RPDE feeds, and measuring what is actually published, per platform. |
| **Deliverable** | `src/harvest_pilot.py`; `results/census_field_presence.csv`; `results/census_endpoint_log.csv`; `docs/data-sources.md`; D-021 incl. its census amendment. |
| **Acceptance evidence** | **Census, 2026-07-15 — complete coverage of the declared frame:** `attempted ÷ declared` = **173/173 = 100.0%**, 4 catalogues, **124 distinct publishers**, 969 endpoints, **217,743 items**. **Licence verified, not assumed: 162/162 *readable* sites declare CC-BY 4.0 (100.0%); 11 of 173 were unreadable and their licences are unknown** (`src/verify_licences.py` → `results/licence_audit.csv`). `superEvent` on `ScheduledSession` **18,935/18,935 = 100.0%** (`Slot` 0/92,359 — per-kind is the only honest denominator). Field availability is determined by **platform × feed kind**: on `SessionSeries`, LeisureCloud is `category` **28/28** and `activity` **0/28**; singular is `activity` **6/6**. `offers` inverts between models — parent for sessions, **`Slot` child** for facilities (77/77, 25/25, 2/2, 1/1: unanimous). **52 of 969 endpoints failed (5.4%)**; **14 of 173 declared sites (8.1%) unreadable**. Capacity ~1,329 bytes/item → **~10.5 GB** for all 7.9M. |
| **Verdict** | **Strongest row in this document — and now measured on the whole declared frame, not a sample.** |
| **Limitation** | Two RPDE pages per feed, so this is a **snapshot of feed heads, not the full corpus**; item-level rates could shift deeper in the feeds. The frame is **everything the catalogues declare** — publishers outside the four catalogues are invisible by construction, so "173/173" is 100% of *declared*, not of *existing*. The harvest is **national** (Wigan, BwD Leisure) while the analysis is London-scoped: defensible for characterising *platform* behaviour, but it must be stated. "Understanding" here is of the **publication layer**; the brief may have meant something broader. **[INTERPRETATION]** |

### R2 — "Highlight various approaches used across the country."

| | |
|---|---|
| **Research choice** | Prior-art assessment against **deployed** incumbents, to set the novelty floor. |
| **Deliverable** | Verified live 14–15 July 2026: the OpenActive **Data Intelligence Platform is deployed**, not announced — 7.9M opportunities, 175 publishers, 3,642 providers (15 Jul), 785 activities, 74% of local authorities, ODI-stewarded, daily refresh. Recorded in proposal §1. |
| **Acceptance evidence** | Direct verification of the live artefact, correcting an earlier project claim that it was consultation-stage. |
| **Verdict** | **PARTIAL — the weakest of the five.** |
| **Limitation** | **This is a genuine gap, not a nearly-done row.** The brief requires "Highlight various approaches used across the country." (P1 p.19); what exists is a handful of incumbent tools checked to bound our own novelty claim. There is **no literature review and no systematic national scan** in this repo. `docs/references.bib` does not yet exist. R2 as written is **not currently met.** |

### R3 — "Identify challenges and opportunities in the way Londoners search for and engage with local activities."

| | |
|---|---|
| **Research choice** | Reframe "challenge" from *user behaviour* to *answerability*: a Londoner's constraint (price, age, accessibility, time) can only be honoured if the field encoding it is published. Where the platform omits it, the constraint is **unknowable**, and a finder must either wrongly reject (false suppression) or wrongly reassure (false assurance). |
| **Deliverable** | Three-state discovery demonstrator — determinate match / indeterminate candidate / known non-match — against closed-world and permissive baselines. Specified in `docs/team-notes-2026-07-15.md`. |
| **Acceptance evidence** | The mechanism is **evidenced**: the four vocabulary regimes mean identical queries are answerable in one borough and not another, purely by which platform the operator bought. |
| **Verdict** | **Mechanism evidenced; artefact NOT BUILT.** |
| **Limitation** | Not yet implemented; `src/recommender/` has never been committed by anyone. False-suppression/false-assurance rates need an **adjudicated sample** that does not exist. This is an **area-level, catalogue-side** account of search — it describes what the catalogue can answer, **never what a Londoner experienced.** No user research; no interaction data. **[INTERPRETATION]** — the brief's "way Londoners search" plausibly means user behaviour, which this project cannot observe and does not claim. |

### R4 — "Propose innovative digital or data-driven interventions that could improve reach, engagement and equity of access."

| | |
|---|---|
| **Research choice** | Two interventions, both derived from measured defects: (a) **three-state presentation** instead of binary filtering; (b) **ranked data repairs** — which field, fixed by which platform, unlocks the most answerable queries. |
| **Deliverable** | RQ5 (repair value) and the demonstrator. Proposal v6.1 §2. |
| **Acceptance evidence** | Repair targets are **platform-addressable and named**, not generic — an intervention aimed at a vendor is actionable in a way *"publishers should try harder"* is not. **Census-corrected example:** on `SessionSeries`, LeisureCloud publishes `category` at 28/28 publishers but `activity` (Activity List URI) at **0/28**, while singular publishes `activity` at 6/6. One vendor adding one field would make Activity List queries answerable across 28 publishers at once. |
| **Verdict** | **PROPOSED — not built, not evaluated.** |
| **Limitation** | The brief's own wording is "could improve reach, engagement and equity of access" (P1 p.19). **Reach and engagement are not measurable by this project**: no behavioural outcome, no A/B test, no user cohort. Only *equity of access* is partially addressable, and then only as **catalogue answerability**, not lived access. Scenario estimates only. Equity is an **evaluation lens over listed supply**, and OpenActive under-captures private/commercial provision, so well-served areas can appear under-served. Any equity claim inherits that bias. **Two of the brief's three named improvement targets are out of reach and must be declared so.** |

### R5 — "Highlight how these approaches could be embedded into London's sport and physical activity system."

| | |
|---|---|
| **Research choice** | Target the **publication layer** — platforms and publishers — rather than build another consumer product, because the deployed DIP already occupies the consumer/dashboard space. |
| **Deliverable** | Not yet produced. |
| **Acceptance evidence** | **None.** |
| **Verdict** | **NOT ADDRESSED.** |
| **Limitation** | This row is currently empty and should be treated as an open work item. It maps to output type **O7 (Practical implications for London Sport)** below, which the brief names explicitly — so R5 is *doubly* required and *singly* unmet. This is the clearest actionable gap in the document. |

---

## 2. Research-focus clauses (P1 p.19 / P2)

### F1 — "Review, analyse and innovate using OpenActive data, drawing on approaches from across the country."

- **Choice:** OpenActive is the single primary dataset; other sources are complementary externals only.
- **Deliverable / evidence:** The harvest layer (R1). "Innovate" = the answerability reframing.
- **Limitation:** "drawing on approaches from across the country" is the **same unmet obligation as R2**. Note also that the pilot is **national in scope** (Wigan, BwD Leisure) while the analysis is London-scoped — a defensible sampling choice for characterising *platform* behaviour, but it must be stated, not glossed. **[INTERPRETATION]**

### F2 — "Develop new models, prototypes or recommendations tailored **specifically** to London's diverse communities."

- **Choice:** Deliver a **prototype** (three-state demonstrator) plus **recommendations** (ranked repairs). Explicitly **not** a learned model — there is no interaction ground truth, so no accuracy claim is possible.
- **Limitation:** The brief offers "models, prototypes **or** recommendations" — disjunctive, so declining to build a model is **compliant**, not a shortfall. **[INTERPRETATION]**
- **Limitation (material):** "**tailored specifically to London's diverse communities**" is the clause this project is **furthest from honouring**. Nothing in the current design is co-designed with, or validated by, any London community. Borough-level deprivation and demographics are **area proxies**, not communities. This should be stated as a limitation in the report rather than papered over — and it is the clause most at risk if the misquotation in §0.2 goes uncorrected, because dropping "specifically" makes the shortfall invisible.

---

## 3. Output framework (P1 pp.22–24) — nine output types the brief names

The brief specifies **nine** output types with suggested contents. This is the most concrete
part of the brief and the project's alignment is **strongest here**.

| # | Output type (verbatim) | Mapped deliverable | Verdict |
|---|---|---|---|
| O1 | **EXECUTIVE SUMMARY** — "A short, non-technical summary of the project, including:" • "The research focus" • "Key findings" • "Main limitations" • "Potential relevance for London Sport" | Report §1 | Not written |
| O2 | **INDUSTRY STYLE ANALYTICAL REPORT** — research question, data sources, analytical approach, key findings, limitations and caveats, implications, "Suggested next steps" | `docs/report_skeleton.md` | Skeleton only |
| O3 | **DATA QUALITY AND SUITABILITY ASSESSMENT** — "Completeness of the data / Missing or inconsistent fields / Issues with data granularity / Any assumptions made / Limitations in using the data for modelling or forecasting / Areas where findings should be treated with caution" | **D-021 + harvest pilot + field-presence CSVs + `docs/data-sources.md`** | **STRONGEST — see §3.1** |
| O4 | **METHODOLOGY EXPLANATION** — approach selected, why appropriate, "**What alternatives were considered**" | `docs/decision-log.md` (D-007…D-021) | Partial — see §3.2 |
| O5 | **MODEL PERFORMANCE, CONFIDENCE AND LIMITATIONS** — incl. "**What the model should not be used for**" | Three-state demonstrator; the no-accuracy-claims rule | Not built |
| O6 | **VISUAL OR PRESENTATION OUTPUT** — charts, maps, prototype dashboards, notebook visuals | WS4 | Not built |
| O7 | **PRACTICAL IMPLICATIONS FOR LONDON SPORT** — incl. "Digital activity discovery", "**Data quality improvement**", "Partner conversations", "Further research questions" | Maps to R5 | **Not addressed** |
| O8 | **REPRODUCIBLE HANDOVER MATERIAL** — "Code or notebooks / Method notes / Data source notes / Assumptions / Model explanations / **Instructions needed to reproduce the analysis**" | This repository | **FAILING — see §3.3** |
| O9 | **FINAL PRESENTATION** — key learning, findings, limitations, practical relevance, next steps | Assessed group presentation (20%) | Not built |

### 3.1 O3 is the alignment headline — and it reframes the pivot

The D-021 pivot has been discussed internally as a *retreat* from the original equity study.
Against the brief it is **the opposite**. Read O3's suggested contents beside what D-021
delivers:

| Brief asks for (verbatim, P1 p.22) | D-021 + census delivers |
|---|---|
| "Completeness of the data" | Per-field presence rates by platform and kind — **6,622 rows, 124 publishers, 173/173 declared sites** |
| "Missing or inconsistent fields" | Vocabulary regimes by **platform × feed kind**; `offers` structurally inverts between the session and facility models |
| "Issues with data granularity" | Parent/child (`SessionSeries`/`ScheduledSession`, `FacilityUse`/`Slot`); borough-level unit (D-008) |
| "Any assumptions made" | `docs/decision-log.md`, D-007→D-021 |
| "Limitations in using the data for modelling or forecasting" | D-021: the legacy corpus **cannot support** the planned analysis, and why |
| "Areas where findings should be treated with caution" | **Two denominator traps caught and recorded** — the all-kinds `superEvent` aggregate (17.0% vs the true per-kind 100.0%/0.0%), and pooling `FacilityUse` with `SessionSeries` parents, which made Bookteq's facility-only catalogue look like a publisher defect. Plus the platform confound in the pilot's first run. |

**The partner asked for a data quality and suitability assessment as a named required
output. D-021 is that output.** The pivot does not need defending as a deviation from the
brief; it should be presented as the brief's own second analytical deliverable, arrived at
empirically. **[INTERPRETATION]** — this is the project's reading of O3's scope, not the
partner's stated intent.

### 3.2 O4 gap — "What alternatives were considered"

The brief names this explicitly. `docs/decision-log.md` records alternatives for older
entries, but **for the pivot itself it does not**: greps return zero hits for the
answerability reframing, for rejected alternatives with reasons, for the
no-further-elicitation constraint, and for threshold rationale. **O4 is only partly met and
the missing part is the part the brief names verbatim.**

### 3.3 O8 is failing, and F-DEP is why

O8 requires "**Instructions needed to reproduce the analysis**". Finding **F-DEP**: the
`openactive` package produced the entire legacy corpus (`notebooks/load_dataset.ipynb` does
`import openactive`) but is declared in **neither `requirements.txt` nor `environment.yml`**
and is not installed in the shared environment. **Nobody cloning this repo can rebuild the
corpus.**

F-DEP has been treated as internal housekeeping. It is not: it is a **direct failure against
a partner-named required output.** Same for the provenance risk in §0.1 — a brief-traceability
document whose brief is not in the repo fails O8 on its own terms.

---

## 4. Constraint of record: no further partner elicitation

**The team has determined that no further partner elicitation is available.** What London
Sport supplied — P1 and P2 — is the complete statement of requirements. There will be no
clarification of ambiguous clauses, no scope negotiation, and no acceptance criteria beyond
the brief's own words.

**Consequences, which are the reason this document exists:**

1. Every ambiguity must be closed by **documented interpretation**, marked **[INTERPRETATION]**
   above, and defended in the report — never by assumption presented as fact.
2. **This document is the alignment ceiling.** Absent elicitation, the most alignment
   obtainable is: quote the brief verbatim, state the interpretation, name the deliverable,
   name the evidence, name the limitation. That is fully within the team's control, which is
   precisely why it is worth doing well.
3. "The partner didn't specify" is **not** available as a defence for an unmet clause. The
   clauses are fixed and enumerable; §1 and §3 enumerate them.

> **UNVERIFIED — team to confirm before ratification.** The *reason* no further elicitation
> is available (unit rule / partner availability / a team decision, and on what date) is not
> recorded anywhere in this repo. It is recorded here as a constraint the team asserts. A
> decision-log entry must state the reason and the date. Do not ratify this section until
> that is written down.

---

## 5. Honest coverage summary

Against the five clauses the brief phrases as **requirements** (P1 p.19):

| Clause | Verdict |
|---|---|
| R1 — understand the ecosystem | **Met, and strongly** (pending census) |
| R2 — approaches across the country | **Not met** — no literature review, no national scan |
| R3 — challenges/opportunities in how Londoners search | **Mechanism evidenced; artefact not built** |
| R4 — propose interventions | **Proposed; not built, not evaluated** |
| R5 — embedding into London's system | **Not addressed** |

**One of five met.** Against the nine output types, one (**O3**) is strong, one (**O8**) is
actively failing, and the rest are unbuilt or skeletal.

This is a **draft-stage project with a strong, evidenced data-quality core and four open
obligations** — not a project that is 100% aligned. The value of this document is that the
gaps are now *named, quoted and dated* rather than discovered by an examiner. R2 and R5 are
the two that no amount of harvesting will close, and neither depends on the census; both can
start today.

---

## 6. What must happen to this document

1. **Ratify or reject** alongside D-021 (PR #6).
2. **Fix the §0.2 misquotation** in every proposal artefact before any submission.
3. **Resolve §0.1**: get P1 into the repo, or record a citable reference to it.
4. **Write the §4 decision-log entry** giving the reason and date for the elicitation constraint.
5. **Re-run the §1/§3 verdicts** when the census lands and when WS3/WS4 are built. Verdicts are
   dated 2026-07-15 and will go stale.

*Provenance of this file: clauses extracted from P1 by direct PDF text extraction and from P2
by direct image reading, 2026-07-15. Repository claims verified against the working tree and
`git` history the same day. Figures cited from `results/pilot_*.csv` as committed in PR #6.*
