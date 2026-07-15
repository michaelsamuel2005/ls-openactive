# Attribution and licensing

**This repository is public and redistributes derivatives of third-party open data.**
The attributions below are **conditions of the upstream licences, not courtesies.**
CC-BY 4.0 permits redistribution *only with attribution*; the Open Government Licence
requires acknowledgement in a specified form. Removing or omitting them makes the
redistribution unlicensed.

Every licence recorded here is **verified**, not assumed — see the evidence column.
Source of record: `docs/data-sources.md`.

---

## 1. What licence covers what

| Content | Licence | Notes |
|---|---|---|
| **Source code** — `src/`, `tests/`, configuration | **MIT** (see `LICENSE`) | Chosen so London Sport can use, embed and modify the work with no legal review — see D-024. |
| **Documentation and analytical outputs** — `docs/`, `results/`, `reports/` | **CC-BY-4.0** | Matches the upstream OpenActive licence, so derivatives flow back into the ecosystem on the ecosystem's own terms. |
| **Third-party data and every derivative of it** | **Upstream licence — unchanged** | Our licence choices cannot and do not relicense other people's data. See §2. |
| **The London Sport brief (P1/P2)** | **NOT LICENSED TO US FOR REDISTRIBUTION** | **Must not be committed.** See §3. |

## 2. Upstream data sources — attribution required

### 2.1 OpenActive (CC-BY 4.0) — the primary source

> Contains information from the **OpenActive** ecosystem, published by **144 named data
> publishers** across four data catalogues (LeisureCloud, Legend, Bookteq, singular),
> licensed under the
> **[Creative Commons Attribution 4.0 International Licence (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/)**.
> **This work modifies that data**: records were harvested from RPDE feeds, filtered,
> aggregated to field-presence and endpoint-status summaries, and are redistributed here in
> derived form. The publishers do not endorse this work or its conclusions.

**Evidence — this licence is measured, not assumed.** `src/verify_licences.py` walked the
canonical catalogue collection and read the `license` field declared by every dataset site:

- **162 of 162 readable dataset sites declare `https://creativecommons.org/licenses/by/4.0/` — 100.0%, unanimous.**
- **11 of 173 declared sites were unreadable** (HTTP errors / no parseable JSON-LD), so their
  licences are **unknown, not assumed**.
- Full audit: **`results/licence_audit.csv`** (one row per declared site).

> ⚠️ **CORRECTION (2026-07-15) — an earlier version of this section claimed "No data from
> unreadable sites is redistributed here." That was FALSE**, and falsified by an artefact in
> the same commit. **One publisher — `Halo` — returned HTTP 403 on its dataset site (so its
> licence is unknown) yet contributes 14 derived rows to `results/census_field_presence.csv`,
> published in this public repository.** The cause: `src/verify_licences.py` reads the
> *dataset site*, while `src/harvest_pilot.py` reads the *feed endpoints* — a site can 403 on
> one and serve on the other, so the two runs disagree about who was readable.
>
> **Status: unresolved, disclosed rather than papered over.** This is the one assertion in
> this file with external legal consequence, in the document written to fix exactly this
> class of defect, and it did not hold. **Team decision required — options:** (a) drop Halo's
> 14 rows from published artefacts; (b) re-read Halo's site to establish its licence; or
> (c) rely on the **RPDE envelope's own `license` field**, which every feed page carries and
> which neither run has yet used — the strongest option, because it attributes at the level
> of the data actually redistributed rather than at site level. **Until resolved, Halo's rows
> are redistributed without a verified licence.** Tracked as **D-026**.

This discharges the open ask recorded at `docs/data-sources.md` — *"verify per-feed licences
before publishing derived outputs"*.

**Also:** the OpenActive **Open Sessions** SessionSeries feed
(`https://opensessions.io/api/rpde/session-series`), operated by **London Sport** — **CC-BY 4.0**.

### 2.2 Crown-copyright sources — Open Government Licence

> Contains public sector information licensed under the
> **[Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)**.
> Contains **National Statistics** data © Crown copyright and database right 2021–2025.

| Source | Publisher | Licence |
|---|---|---|
| English Indices of Deprivation 2025, File 10 v2 (lower-tier LAD summaries) | MHCLG | **OGL v3.0** |
| Census 2021 demographics (bulk LTLA) | ONS | **OGL v3.0** |
| Boundaries — 2021 LAD | ONS Open Geography Portal | **OGL v3.0** |
| Active Lives adult inactivity (2024/25) | Sport England | **OGL v3.0** |

> ⚠️ **TfL PTAL is OGL v2, not v3** — a distinct licence, verified against the Datastore API
> record and easy to get wrong:
>
> Contains **Transport for London** data, "Public Transport Accessibility Levels", 2015 grid,
> licensed under the
> **[Open Government Licence v2.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/)**.

### 2.3 Sport England Active Places — its own licence, NOT OGL

> ⚠️ Active Places is **not** OGL. It is governed by Sport England's own licence page
> (`https://www.activeplacespower.com/pages/license`), and the required acknowledgement is
> verbatim:
>
> **"Contains data Copyright Sport England"**
>
> Recorded at `docs/data-sources.md`, which notes explicitly that the pre-acquisition runbook
> had wrongly assumed a bare OGL v3.0. **Reproduce the wording exactly; do not paraphrase it.**

## 3. What must NOT be redistributed here

**The London Sport 1 brief.** The project's primary requirement sources are:

- **P1** — `LS machine learning projects_29-05-2026.pdf`, London Sport's own deck, authored by
  a named employee (`author: Josef Baines`), unpublished.
- **P2** — the challenge listing image.

**Neither may be committed to this repository.** This repo is public; committing them would
republish a partner's internal document to the open internet. No confidentiality marking
appears on P1, but **absence of a marking is not a licence** — copyright subsists
automatically and London Sport has granted none.

**Quoting clauses for academic criticism and review is a different and defensible act**, and
`docs/brief-traceability.md` does exactly that, with each quotation attributed to P1 or P2 and
machine-checked against the source. That document records **SHA-256 digests** of both
artefacts so any team member holding them can verify identity — verification without
distribution.

## 4. Standing caveats that travel with any output

- **Absence of data is not absence of activity.** OpenActive under-captures private and
  commercial provision, so well-provided areas can appear under-served. This caveat must
  accompany any output that maps or ranks provision.
- **Data vintages differ and must be stated:** IoD **2025** · Census **2021** · Active Lives
  **2024/25** · PTAL **2015** · OpenActive census snapshot **2026-07-15**.
- **`data/` is not redistributed** — raw and processed data are gitignored. Only derived
  summaries in `results/` and `reports/` are published.

---

*Licences in §2 are recorded in `docs/data-sources.md` with retrieval dates and SHA-256
prefixes. The OpenActive licence in §2.1 is independently verified by `src/verify_licences.py`
→ `results/licence_audit.csv` (audit run 2026-07-15). Licence choices for our own work are
recorded as **D-024** in `docs/decision-log.md`.*
