# Team notes — 15 July 2026: the pilot changed the data plan

Evidence: `src/harvest_pilot.py` · `results/pilot_field_presence.csv` (434 rows, 11
publishers) · `results/pilot_endpoint_log.csv` (77 endpoints) · raw pages in
`data/raw/pilot_20260715T*/` · decision entry **D-021 (PROPOSED)**.

Nothing below is adopted: D-020 and D-021 are both PROPOSED and need team ratification.

---

## For Wesley — the harvest design changes completely

**What the pilot established (verified, not inferred).**

The legacy corpus (`dataset_2026-07-07.csv`, 549,169 rows) has **no** `@id`,
`superEvent`, `organizer`, `category`, publisher/feed identity, RPDE `modified`/`state`,
and **no retained raw JSON-LD**. I then read the canonical catalogue → dataset sites →
RPDE feeds directly over plain HTTP (deliberately *not* through the `openactive` client)
and found the feeds carry all of it:

- `ScheduledSession` children are **pointers**: dates, capacity, `superEvent`, nothing
  else. **100.0% (1,533/1,533)** carry `superEvent`. Every descriptive field —
  name, location, `offers`, `category` — lives on the `SessionSeries` **parent**.
- The RPDE envelope carries `modified` and `state` (`updated`/`deleted`) — current-state
  reconstruction is fully supported and was simply never used.
- Structured `offers` objects (identifier `ADULT`, name, description,
  `acceptedPaymentMethod`) were flattened to a single `adultPrice` number.

**So the corpus is retired** (D-021) and a fresh, raw-retaining, paired-feed harvest is
**Deliverable 1**. It cannot repair 7 July retrospectively: RPDE is a change feed, the
parent state at that date is gone, and no raw was kept. The frozen observation date moves.

**The single most important design finding — stratify by platform.**

My first run sampled the first six sites from a concatenated catalogue list. All six ran
on **one platform (LeisureCloud)**, and I nearly reported a platform artefact as an
ecosystem fact. Stratified across all four catalogues, field availability is
**near-deterministic by platform and near-invariant within it**:

| Platform (catalogue) | `category` on parents | `activity` (Activity List URI) |
|---|---|---|
| LeisureCloud (5 publishers) | **100%** (all five) | 0% (all five) |
| singular (Better; Bookwhen) | 0%; 53% | **100%** (both) |
| Legend (BwD Leisure) | 0% | **100%** |
| Bookteq (3 publishers) | 0% | 0% |

Five different councils on LeisureCloud behave identically; two publishers on singular do
the exact inverse. **That is vendor software, not publisher diligence** — and it means a
sampling frame that isn't platform-stratified will produce confounded rates.

**Harvest requirements, derived from the above:**

1. **Walk the canonical collection** (`https://openactive.io/data-catalogs/data-catalog-collection.jsonld`)
   → 4 catalogues → **173 declared dataset sites**. Report **`attempted ÷ declared`** at
   catalogue, site and feed level. "100% of the feeds we tried" is not coverage.
2. **Stratify the selection by catalogue/platform**, and state the selection rule.
3. **Harvest feed *pairs*** — `SessionSeries` **with** `ScheduledSession`, `FacilityUse`
   **with** `Slot`. A child feed alone is unusable.
4. **Retain raw JSON-LD exactly as served**, plus the RPDE envelope
   (`id`, `modified`, `kind`, `state`). Flattening happens downstream, reversibly, never
   at harvest.
5. **Log every endpoint's status** (`COMPLETE` / `TIMEOUT` / `ERROR_HTTP_nnn`) and keep
   failures visible. The pilot already found **8 failures in 77 endpoints**: Wigan's
   declared `ScheduledSession` **404**; three Legend **500**s; three **403**s; a Bookteq
   site **404**. Failed/partial reads must never silently become "zero opportunities".
6. **Apply `state: deleted` tombstones** to produce current state.
7. **Be a polite consumer** — the pilot uses 1 request/second and a research User-Agent.
8. **Capacity is not a problem**: ~1,772 bytes/item raw → **~14 GB** for all 7.9M items.
   Zip snapshots and checksum the archive.

**Two things to settle:**

- **F2 (harvest date)** is now moot for analysis — both candidate snapshots are retired —
  but still needed to cite the legacy figures as history. Please record it if recoverable,
  or mark it formally unrecoverable.
- **F-DEP (new).** `openactive` produced the entire legacy corpus
  (`notebooks/load_dataset.ipynb` does `import openactive`) but is **declared in neither
  `requirements.txt` nor `environment.yml`**, and isn't installed in the shared
  environment — **nobody cloning this repo can rebuild the corpus.** The package also
  self-describes as *"experimental"* and advises against use *"for critical pipelines"*.
  If we use it, it must be pinned, declared, and its join/delete/pagination behaviour
  verified against the raw feeds. `src/harvest_pilot.py` uses plain HTTP and adds no
  dependency; it can serve as the reference implementation or the cross-check.

`src/harvest_pilot.py` is a working, ruff-clean, platform-stratified starting point —
please take it, don't rewrite it.

---

## For Clarence — please push today, and don't retarget yet

**1. Push your branch today, regardless of everything else.** The recommender exists on
one machine; no commit has ever touched `src/recommender/`. That is a bus-factor risk on
the largest piece of build work anyone has done, and it's independent of any design debate.

**2. Do not retarget it to the equity-reranker spec — that spec is retired.** Under the
pivot the artefact becomes a **thin three-state discovery demonstrator**. For a given
query with hard constraints, classify each record as:

- **determinate match** — every hard constraint verifiably satisfied;
- **indeterminate candidate** — nothing contradicts, but at least one constraint is
  *unknown* from the record;
- **known non-match** — at least one constraint explicitly contradicted.

and compare that presentation against two baselines: **closed-world** (unknown = reject;
risks *false suppression*) and **permissive** (unknown = allow; risks *false assurance*).
The measured outcomes are **false-suppression and false-assurance rates** against an
adjudicated sample — not relevance, not equity uplift.

**What survives from your build:** the hard-filter skeleton, the query/candidate plumbing,
the test harness. **What doesn't:** the equity term, the α-sweep, the gap-index dependency,
the synthetic personas as evidence.

**3. Wait for the new corpus before building further.** Today's pilot proved the current
CSV lost `superEvent`, `category` and structured `offers` — so the three-state logic can't
even be exercised honestly against it (you cannot evaluate "unknown" when the field was
destroyed by extraction rather than absent at source). Evidence: D-021 and
`results/pilot_field_presence.csv`.

---

## What this means for the project's framing

Both mechanisms are real, and they compose into a better story than either alone:

- **Instrument-side:** our pipeline discarded fields the platform published on 100% of
  records. For LeisureCloud, the "missingness" was self-inflicted.
- **Publication-side:** the ecosystem is **not one vocabulary regime but four**. A
  consumer joining these feeds gets `category` from one platform, Activity List URIs from
  another, neither from a third — so **cross-platform activity analysis compares
  incommensurable fields**. The deployed Intelligence Platform reports "785 activities"
  across exactly this heterogeneity.

The defensible framing is neither "publishers are negligent" nor "our pipeline was bad",
but: **field availability in OpenActive is determined by booking-platform software, and
that determines which discovery questions can be answered where.** That is mechanistically
explanatory, evidenced, brief-aligned, and not occupied by any incumbent tool.

**Caveat to hold:** 11 publishers, 20 of 173 declared sites (11.6%), one page per feed.
The platform dichotomy is a hypothesis with 11 data points, not a rate. Whether it holds
is the first thing the full harvest must measure.
