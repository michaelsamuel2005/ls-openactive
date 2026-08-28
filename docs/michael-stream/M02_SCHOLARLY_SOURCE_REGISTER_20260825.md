# M-02 scholarly-source register

**Gate:** `M02-ACADEMIC-STANDARD-01` (prerequisite-free)
**Status:** `PREPARED_FOR_ADOPTION` — field-complete for every source with retained evidence;
open fields are marked, not hidden. Adoption lines at the end.
**Prepared:** 2026-08-25, from the frozen reading records of 23–24 August, the pinned source
copies, and the primary-source verification performed 25 August (Wiley/Springer/PhilPapers).
**Standing rules adopted with this register:**
1. *Approved-primary-source rule* — a load-bearing claim cites a source entry in this register
   with a pinned copy hash or Version-of-Record DOI; no other citation path.
2. *No unapproved preprint* — no preprint carries a load-bearing claim. **Current status:
   satisfied** — `optional_sources_relied_on = NONE` in all frozen OA records; no preprint is
   relied on anywhere in the evidence chain to date.
3. *Specification-versus-research separation* — standards documents are authoritative for
   protocol semantics but are never cited as peer-reviewed academic evidence; the two roles are
   labelled on every entry below and may not be blended in report text.

---

## Part A — OpenActive specification and guidance sources (roles: SPECIFICATION / STANDARDS)

### SRC-OA-MOD20 — Modelling Opportunity Data 2.0

| Field | Entry |
|---|---|
| Bibliographic identity | OpenActive Community Group, *Modelling Opportunity Data 2.0* (W3C Community Group Final Report). Stable ID: pinned repo revision `openactive/modelling-opportunity-data@113704f0…19d6`, file `2.0/index.html` |
| Pinned copy SHA-256 | `b75a461d145b08ee0e67923e7d40a461d51502201c87d27d68807b39f04db325` |
| Publication / review status | W3C **Community Group** report — standards document; not peer-reviewed academic literature |
| Role | SPECIFICATION — authoritative for protocol semantics only |
| Lawful access | Public web publication; pinned public-repository copy retained |
| Sections read (per block) | OA-1: §5.4; §§5.6.9–5.6.9.3; §2 and typographical convention for normative force. OA-2: §§5.6.7, 5.6.8.1. OA-4: §2; §§5.4–5.6 incl. §5.6.4, §5.6.1, §5.6.3, §§5.6.6.1–5.6.6.3, §5.6.7, §5.6.8.1, §§5.6.9–5.6.9.3, §§5.7–5.7.2, §§5.9–5.12 |
| Normative modal force | RFC 2119 capitalised modals; note-status material distinguished via §2 and the report's typographical convention (recorded in Michael's OA-1 raw answer) |
| Reading dates | 2026-08-23 (OA-1 13:38–13:48; OA-2 14:23–14:27; OA-4 within the recorded OA-4 chronology) |
| Supported claim (attested) | Property-specific parent fallback permitted when child silent; explicit child wins; five named properties and Offers never inherit by default, with the scoped SessionSeries→ScheduledSession Offers permission (OA-2 v3, `21c65e28…`) |
| Unsupported claim (attested) | No exhaustive inheritance whitelist; no universal cancellation-implies-exceptDate rule (SHOULD NOT / SHOULD force preserved, not upgraded) (OA-1/OA-2 records) |
| Limitation / counter-position | Example-based eligibility rule leaves per-property ambiguity (esp. `schema:startDate`); HTML pinned copy lacks stable print pagination |
| Michael's two-sentence verdict | Retained verbatim in `OA-1_V3…`/`OA-2_V3_ATTESTATION_PROPOSAL.json` (hashes `004f15e2…`, `21c65e28…`) |
| Substantive challenge | **PENDING** — awaits eligible challenger appointment (`M02-OA-ELIG-01`) |

### SRC-OA-SCHEDULES-L2 — OpenActive Schedules guidance

| Field | Entry |
|---|---|
| Bibliographic identity | OpenActive developer documentation, *Publishing data: Schedules*. Stable ID: `openactive/developer-documentation@6680902e…3c0c`, `docs/publishing-data/schedules.md` |
| Pinned copy SHA-256 | `cc11806aa07addeb312ddc499d5f35475dcc21f607120405f43f7414470e5b82` |
| Publication / review status | Official operational guidance — not a Community Group final report, not peer-reviewed |
| Role | SPECIFICATION-ADJACENT GUIDANCE — authoritative for consumer procedure; weaker authority layer than MOD 2.0, recorded as such |
| Lawful access | Public web publication; pinned public-repository copy retained |
| Sections read | Complete page: Schedule/PartialSchedule distinction, publication, template, processing procedure, worked example (OA-1, 2026-08-23 13:48–13:56) |
| Normative modal force | "must not be extrapolated" (PartialSchedule); processing steps 2.1/2.2/3 for hide-by-`@id` |
| Supported claim (attested) | A matching explicitly published ScheduledSession supersedes the generated occurrence and is used in its entirety |
| Unsupported claim / limitation | The deletion/version sentence ("do not have an older…") is ambiguous and is not adopted as a settled stale-record algorithm (OA1-C7, PARTLY_AGREE) |
| Michael's verdict | Retained verbatim in the OA-1 v3 attestation (`004f15e2…`) |
| Substantive challenge | **PENDING** (`M02-OA-ELIG-01`) |

### SRC-OA-RPDE10 — Realtime Paged Data Exchange 1.0

| Field | Entry |
|---|---|
| Bibliographic identity | OpenActive, *Realtime Paged Data Exchange 1.0* (W3C Community Group Final Report). Stable ID: `openactive/realtime-paged-data-exchange@f1d52a09…3a31` |
| Pinned copy SHA-256 | `ab94bd518cd73e532ff665083d9a24e71761bdd1bffe9d42ff578cfce25e14ef` |
| Publication / review status | W3C Community Group report — standards document; not peer-reviewed academic literature |
| Role | SPECIFICATION |
| Lawful access | Public web publication; pinned copy retained |
| Sections read | §2; §§4.2–4.6 incl. §§4.4.1–4.4.2; §§5.1.2, 5.1.5, 5.1.6; §5.2 (OA-3, 2026-08-23 16:26–16:50) |
| Normative modal force | Last-page rule requires BOTH empty `items` AND self-referential `next` (§5.1.5); empty array alone insufficient (§5.1.6); deleted items retained ≥7 days (§4.6) |
| Supported claim (attested) | A conforming unbroken traversal reaching empty-and-self-referential establishes catch-up to that endpoint's exposed tail at that response time |
| Unsupported claim (attested) | RPDE alone proves no real-world completeness, historical completeness, cross-endpoint scope or atomic snapshot |
| Limitation / counter-position | No express cross-endpoint ID scope, standalone stable-identity modal, tombstone-expiry recovery, or certificate format — all derived project controls, labelled as such |
| Michael's verdict | Retained verbatim in the OA-3 v3 attestation (`383fb989…`) |
| Substantive challenge | **PENDING** (`M02-OA-ELIG-01`) |

### SRC-OA-SCHEDULE-PROFILE — pinned `Schedule.json` model profile

| Field | Entry |
|---|---|
| Bibliographic identity | Pinned `Schedule.json` and property/type mappings, as recorded in the frozen OA-4 source record |
| Pinned copy SHA-256 | Recorded in the frozen OA-4 source record (hash-bound there; not restated here to avoid a second authority) |
| Publication / review status | Machine-readable model artefact — standards material, not peer-reviewed |
| Role | SPECIFICATION (machine profile) |
| Sections read | Complete pinned file (OA-4, 2026-08-23) |
| Claims / verdict / uncertainty | Carried at block level in the OA-4 v3 attestation (`19c0fced…`), incl. the source-layer rule that no universal absence/invalidity/inheritance/defaulting rule exists |
| Substantive challenge | **PENDING** — OA-4 challenge is the first packet of the reviewer campaign |

### SRC-OA-TEST-PROFILE — OpenActive test-suite defaults profile

| Field | Entry |
|---|---|
| Bibliographic identity | OpenActive test-suite documentation, defaults profile; pinned copy `integration/pinned_sources/openactive-test-suite-defaults-profile-20260810.html` |
| Pinned copy SHA-256 | `95d9ff5ac74ca63ac18fe28c7c95150c775f9ba9dbbe109c3a6dfd38fdff6aa4` |
| Publication / review status | Operational tooling documentation — establishes current capabilities only; never theoretical validity |
| Role | OPERATIONAL EVIDENCE (weakest authority layer; labelled per §12 of the work package) |
| Sections read | Test scope, Opportunity Feed extract, complete Validations section, C1/C2/B request-response-assertion blocks (OA-4) |
| Claims / verdict | Block-level in OA-4 v3; exact release provenance of the tooling evidence retained as an open uncertainty |
| Substantive challenge | **PENDING** (OA-4 packet) |

### SRC-OA-SCHEMAORG-SCHEDULE — schema.org `Schedule` definition

| Field | Entry |
|---|---|
| Bibliographic identity | schema.org `Schedule` type page; pinned copy `integration/pinned_sources/schema-org-schedule-20260810.html` |
| Pinned copy SHA-256 | `0f43140835ea098ec250d7f09060fff094009ff01e2e84ea630c700d1acf1fb1` |
| Publication / review status | Vocabulary definition (schema.org) — standards material with its own status notice; not peer-reviewed |
| Role | SPECIFICATION (vocabulary layer) |
| Sections read | Definition/status notice, complete Schedule property table, `eventSchedule`, and the explicit source silences (OA-4) |
| Claims / verdict | Block-level in OA-4 v3; silences recorded as silences, not defaults |
| Substantive challenge | **PENDING** (OA-4 packet) |

---

## Part B — Theory sources (role: PEER-REVIEWED / SCHOLARLY RESEARCH)

### SRC-TH-BELNAP-1977 — "A Useful Four-Valued Logic"

| Field | Entry |
|---|---|
| Bibliographic identity (VoR) | Belnap, N. D., "A Useful Four-Valued Logic", in Dunn & Epstein (eds.), *Modern Uses of Multiple-Valued Logic*, D. Reidel, Dordrecht, 1977, pp. 5–37. DOI `10.1007/978-94-010-1161-7_2` |
| Publication / review status | **Edited scholarly volume chapter** — Version of Record; NOT a journal-refereed article and must not be described as one. Verified 2026-08-25 against Springer and PhilPapers |
| Role | SCHOLARLY RESEARCH (foundational; §11.1 credits four-valued logic as mature, not novel) |
| Lawful access | **PENDING** — `M02-TH1-ACCESS-01`; institutional route in progress; ILL draft prepared |
| Known pagination question | Springer chapter record: pp. 5–37; some citations give 8–37 — resolve against the actual PDF at intake |
| Reading, verdict, claims, challenge | ALL PENDING — nothing may be entered here until Michael's K7 reading occurs |

### SRC-TH-GINSBERG-1988 — "Multivalued logics: a uniform approach…"

| Field | Entry |
|---|---|
| Bibliographic identity (VoR) | Ginsberg, M. L., "Multivalued logics: a uniform approach to reasoning in artificial intelligence", *Computational Intelligence* 4(3), 1988, pp. 265–316. DOI `10.1111/j.1467-8640.1988.tb00280.x`; ISSN 0824-7935 / 1467-8640 |
| Publication / review status | **Peer-reviewed journal article** — Version of Record. Verified 2026-08-25 (Wiley). The 1986 AAAI paper is a barred substitute |
| Role | SCHOLARLY RESEARCH |
| Lawful access | **PENDING** — direct Wiley access refused under Bristol subscription 2026-08-25 (junk connector save recorded and deleted); "Get it!" resolver / ILL route next; ILL draft prepared |
| Reading, verdict, claims, challenge | ALL PENDING |

### SRC-TH-FITTING / SRC-TH-ARIELI — remaining TH-1 sources

| Field | Entry |
|---|---|
| Status | Copies retained with recorded copy limitations per `m02/TH1_LAWFUL_FULL_TEXT_ACCESS_ACTION.md`; full register entries to be completed at TH-1 intake alongside the two texts above |

### TH-2 · TH-3 · TH-4

Locators and hashes prepared per `M02_EVIDENCE_STATUS.tsv`; register entries open until each
block starts under the fixed sequence TH-1 → TH-2 → TH-3 → TH-4.

---

## Part C — What remains open on this gate, stated exactly

1. **Adoption.** The gate's actor is "Michael, source librarian or custodian, and
   scholarly-method owner." Michael's adoption line is below; custodian and method-owner
   adoption are team acts and remain open.
2. **Substantive challenges** — every OA entry: pending challenger appointment
   (`M02-OA-ELIG-01`).
3. **TH access and reading** — Part B rows complete only after `M02-TH1-ACCESS-01` and the
   K7 readings.

## Michael's adoption — RECORDED

Adopted by Michael on **2026-08-25T21:06:17+01:00** (BST), instruction given in his
authenticated session: close and adopt, on the basis of understanding already recorded.

Basis: the three standing rules restate §12 of the specialised work package, which Michael
accepted the same evening (`WP_MICHAEL_ACCEPTANCE_RECORD_20260825.md`, SHA-256 `ec332a58…`,
claims point 8). Part A was assembled mechanically from Michael's own frozen reading records
(hashes re-verified against the primary files before entry); adoption confirms that derivation
rather than a fresh re-reading. Open fields (substantive challenges; TH rows) remain open until
their evidence exists, per the register's own rules.

- Name as recorded: **Michael Samuel**
- Custodian and scholarly-method-owner adoption: **OPEN** — team act.
