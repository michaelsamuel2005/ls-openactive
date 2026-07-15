# Data sources & provenance register (tracked)
**Canonical, committed record of every dataset the project uses** — supersedes the git-ignored `data/external/SOURCES.md` (WS1-planning era; retained on disk for history, no longer maintained). Closes WS1 audit gap 4: provenance documentation now lives in version control.
**Integrity:** SHA-256 prefixes recorded below make silent changes to acquired files detectable; "Retrieved" dates come from file metadata and audit artefacts, not memory. Every published output must carry **CC-BY 4.0 attribution** (OpenActive/Open Sessions) **and OGL v3.0 acknowledgement** (Crown-copyright sources).

---

## Active sources (feed the pipeline)

### 1. Open Sessions — SessionSeries (PRIMARY provision layer; D-009)
- **Publisher:** London Sport (nationwide OpenActive publishing platform — *not* London-only; see `docs/open_sessions_data_note.md`).
- **Endpoint:** `https://opensessions.io/api/rpde/session-series` · **Licence: CC-BY 4.0.**
- **Frozen analysis snapshot:** `data/raw/session_series_raw_2026-06-30.json` — 1,585 live series · sha256 `5873b002ccfbcd69` · harvested 2026-06-30 by the RPDE walk now scripted in `src/harvest_open_sessions.py` (offline rebuild reproduces the processed CSV **byte-identically**).
- **Processed:** `data/processed/london_sessions_2026-06-30.csv` — 494 London series · sha256 `886812f924d92136`.
- Other snapshots on disk (NOT authoritative): 2026-06-27 (`6b769acbbeda09a1`, first audit run), 2026-07-03 (`bc4d702b2992307c`, drift check: 497 London), 2026-07-07 (raw `30e6629945be91ca`, processed `6e349a9f1b646904` — **live-mode proof run**, supervised: 37 pages, 16,534 tombstones processed, 1,581 national live / 494 London / 215 free / 261 venues; closes WS1 examiner finding F8). Seven-day drift vs frozen: net −4 national; London count coincidentally equal at 494 with changed composition (−2 free, −3 venues) — churn evidence for the report's "point-in-time snapshot" caveat.

### 2. English Indices of Deprivation 2025 — File 10 v2 (need input; D-007)
- **Publisher:** MHCLG. Published 30 Oct 2025; **LAD summary files reissued as v2 on 17 Nov 2025** (ONS lookup correction) — v2 is mandatory.
- **Landing page:** `https://www.gov.uk/government/statistics/english-indices-of-deprivation-2025` · **Direct asset (pinned 2026-07-08, verified against the live page):** `https://assets.publishing.service.gov.uk/media/6917412ebc34c86ce4e6e7fc/File_10_-_IoD2025_Local_Authority_District_Summaries__lower-tier__v2.xlsx`. The page's own update history confirms the D-007 rationale: Files 10/11/14 reissued as v2 on 17 Nov 2025 after an ONS LSOA→LAD lookup correction — "Please ensure you are using the updated 'v2'".
- **File:** `data/raw/iod2025/File_10_-_IoD2025_Local_Authority_District_Summaries__lower-tier__v2.xlsx` · sha256 `6c38a2fd3998e0ca` · retrieved 2026-07-01 · **OGL v3.0**.
- **Used:** IMD sheet, `IMD - Average score` + `Rank of average score` (auto-detected by `build_iod`); join on LAD code (2024-coded headers, E09 filter). *Average score* choice (not average rank) is deliberate — justify in the report (Hackney #1 on score; Newham would lead on rank).

### 3. ONS Census 2021 — six ltla tables (need inputs + denominators)
- **Publisher:** ONS · **OGL v3.0** · bulk ltla CSVs (file timestamps preserve ONS publication dates 2022-11→2023-01; retrieved June 2026).
- ts001 population `7c30112abe9fb50d` · ts007a age `fb954e12e6c51959` · ts021 ethnicity `a343c70e6662a4a6` · ts037 health `c402be81ee9f34f5` · ts038 disability `0ee1fcc5aad26fbc` · ts066 economic activity `380b2f3900ef2539` — all at `data/raw/census2021/`.
- **Nested-category hazard:** ts066/ts021 carry parent+child rows — exact-match extraction only (`build_census_features`); `pct_econ_inactive` is a NEED input, never the validator.

### 4. ONS boundaries — LAD 2021 BGC (geography spine; D-008)
- **Publisher:** ONS Open Geography Portal (`https://geoportal.statistics.gov.uk/`) · **OGL v3.0**.
- **File:** `data/raw/boundaries/lad_2021_bgc.geojson` · sha256 `03363eb4f4f0cdb6` · retrieved 2026-06-30 · 374 UK LADs, filtered to the 33 E09 London LADs in code; EPSG:4326, reprojected to EPSG:27700 for all metric operations.
- **Companion London extracts** (granularity audit + notebook London filter): `data/external/london_lad_2021.geojson` `8ceed584996a514e` · `london_msoa_2021.geojson` `9e99bccb2a0aca4c` (1,002 MSOAs) · `london_lsoa_2021.geojson` `3c2b140641dd8175` (4,994 LSOAs) — first used 2026-06-27 (audit artefacts); file mtimes 2026-07-03 reflect a later copy.

### 5. Sport England Active Lives — adult physical inactivity (HELD-OUT validator; D-012)
- **Route:** OHID Fingertips API, indicator **93015** ("Percentage of physically inactive adults"), lower-tier LAs:
  `https://fingertips.phe.org.uk/api/all_data/csv/by_indicator_id?indicator_ids=93015&child_area_type_id=501&parent_area_type_id=6`
- **File:** `data/raw/active_lives/inactivity_la.csv` · sha256 `abe887dbf6696411` · retrieved 2026-07-01 · **OGL v3.0** · vintage used: **2024/25**, Sex=Persons, latest period per borough (`build_inactivity`).
- **Role discipline:** validation target ONLY — never a need input (D-012). `pct_inactive_adults` ≠ Census `pct_econ_inactive`.

### 6. OpenActive national catalogue — event-level harvest (secondary, commercial-universe layer; D-014 reframed)
- **Route:** catalogue collection `https://openactive.io/data-catalogs/data-catalog-collection.jsonld` → 37 ScheduledSession feeds (Open Sessions publishes none — different provider universe; see `docs/event_harvest_audit.md`).
- **File:** `data/external/wesley/output.csv` · sha256 `320357c093fc7a17` · 464,392 events · harvest run by Wesley, **date TBC (outstanding ask)** · licences: CC-BY 4.0 per publisher — **verify per-feed licences before publishing derived outputs**.
- **Status:** verified against Wesley's notebook exactly; usable only with the §3 defect list fixed (composite feed+id key, UAT/pentest exclusion, full offer parsing) and its time window stated (events span 2023-02→2027-03).
- **Successor snapshot (2026-07-07) — RETIRED as analysis corpus by D-021 (2026-07-15).**
  Historical/motivating evidence only; every diagnostic derived from it is suspended.
  Reason (verified): child-only `ScheduledSession` extraction with no `superEvent`,
  `@id`, `organizer`, `category`, publisher/feed identity, RPDE `modified`/`state`, and
  no retained raw JSON-LD — so ecosystem defects cannot be separated from extraction
  defects, and no raw exists to resolve it retrospectively. Deliverable 1 is a fresh
  raw-retaining paired-feed vintage. Details below retained as the historical record:
- **(historical, superseded) Successor snapshot (2026-07-07, candidate canonical — D-019 PROPOSED):**
  `data/raw/dataset_2026-07-07.csv` · **549,169 events** · sha256 `7542ed60329c9c06` ·
  harvested **2026-07-07** by Wesley via the `openactive` client
  (`notebooks/load_dataset.ipynb`, Section 1 — outputs preserved as the run record;
  reviewed and integrated by Michael). Fixes vs the TBC-dated file: **known harvest
  date**, structured adult/junior offer parsing, richer schema (capacity, duration,
  day-of-week, amenities). Remaining defects, documented in the notebook header:
  **harvest-time completeness filtering** (records missing venue/geo/offers/name are
  dropped — completeness figures describe the retained subset), **no provider column**
  (128 duplicate ids, cross-feed, unresolvable in-file), window 2023-02→2027-04.
  London (boundary filter): **192,032 events, 30/33 boroughs, 9.1% empty at borough /
  87.6% MSOA / 97.5% LSOA** — independently recomputed, matches the notebook.
  Free share: 1.54% of all rows / **3.12% of price-known** (48.4% priced) — always
  cite the pair. Not yet canonical: becomes so only when D-019 is adopted and
  `verify_event_harvest` is re-pointed with fresh dual-method expectations.

### 7. Sport England Active Places — facilities (corroboration layer; D-011) — **ACQUIRED 2026-07-07**
- **Route:** registered download from Active Places Power (`https://www.activeplacespower.com/`) — the full-database CSV bundle (`activeplacescsvs.zip`). The Hub's machine-readable DCAT catalogue (`/api/feed/dcat-us/1.1.json`) returns an **empty dataset array** — registration is the only working route; reproduce via the UI, not an API.
- **Extract vintage:** data version **2026-07-07 03:30:36**, CSVs created 2026-07-07 04:34 (per `information.txt`, retained alongside the data) · **Licence:** `https://www.activeplacespower.com/pages/license` — "Contains data Copyright Sport England" (acknowledge verbatim on outputs; note this is Sport England's own licence page, not a bare OGL v3.0 as the pre-acquisition runbook assumed).
- **Files at `data/raw/active_places/`:** `facilities.csv` 124,839 rows · sha256 `00eb9ffd7ef7a2e2` · `sites.csv` 43,469 rows (pandas-parsed; raw line count is higher — notes fields contain embedded newlines) · sha256 `42d331ee46aa90aa` · `facilitytype.csv` (code→name lookup shipped in the extract, read by the pipeline) · sha256 `46ab7c02ddcaab8b` · `information.txt` `06296203272c1cd2`.
- **Ingest rules are D-018** (decision log): operational-only (status code 3; decode verified against the text-labelled Hub export, identical 124,839 rows), community use = 'Public Access', type decode via the shipped lookup with the 'Grass Pitches' exact-safe needle. `sites.csv` is NOT read by the pipeline (n_sites derives from facility-file site ids, audit F6); retained for provenance and the LA-code cross-check.
- **Verified on ingest (2026-07-07):** London = **10,070 operational facilities · 3,553 sites** (point-in-polygon and site-LA-code routes **identical**); grass 3,235 · halls 1,505 · health&fitness 1,160 · pools 534; community-use share ~0.79; all 33 boroughs populated; schema green. City per-10k is a denominator artefact — see D-018 caveat.
- Unused duplicates from the same download session (ArcGIS Hub "GIS" exports of Sites/Facilities, text-labelled): used ONCE to verify the status-code decode, then not retained in `data/raw/` — the registered bundle is canonical.

### 8. TfL PTAL — public-transport accessibility (conditional E2SFCA weighting; D-010/D-011) — **ACQUIRED 2026-07-05**
- **File:** `data/raw/ptal/2015  PTALs Grid Values 280515.xlsx` (sheet Query1: ID, X, Y, AI2015, PTAL2015; 159,451 grid points, 100 m) · xlsx sha256 `1d9fea39a5cf25ee` · zip md5 verified `92c5810fd33a12ed04da285b16655976` against the Datastore API record · **OGL v2** · vintage **2015** (state it wherever used).
- **Verified on ingest:** X/Y are EPSG:27700 (503k–562k / 156k–201k); PTAL2015 grades exactly match `PTAL_GRADE_MAP`; borough means computed 33/33, range 1.28 (Havering) → 7.97 (City of London) — correct face validity for London's transit geography. `AI2015` (continuous access index) retained as the preferred weight if E2SFCA activates.
- Config points at the workbook (`PTAL_COLS = X/Y/PTAL2015`); reader handles xlsx.
- Original runbook (for reproduction):
- **Dataset located and verified via the Datastore API** (2026-07-05): TfL "Public Transport Accessibility Levels", **2015 grid** (100 m squares; the openly downloadable vintage — the config's `ptal_2023` name was aspirational; 2015 is usable for the *conditional* E2SFCA weighting with the vintage stated). **Licence: OGL v2** (per the dataset API — note v2, not v3).
- **Acquire (sandbox egress blocked for bulk files — run on a team machine):**
  ```bash
  cd ~/Documents/ls-openactive && mkdir -p data/raw/ptal && cd data/raw/ptal
  curl -sL -o ptal_2015_grid_values.zip \
    "https://data.london.gov.uk/download/24rz6/514d2847-94a8-4b9d-8a70-fdded01719a0/2015%20%20PTALs%20Grid%20Values.zip"
  md5 ptal_2015_grid_values.zip   # must print 92c5810fd33a12ed04da285b16655976
  unzip ptal_2015_grid_values.zip && ls -la
  ```
- Then: identify the grid CSV inside, check its coordinate/grade headers, point `config.py`'s `PATHS["ptal"]` and `PTAL_COLS` at the real names (grid is EPSG:27700), record the CSV's sha256 + date HERE, and rerun the pipeline (`mean_ptal` populates; schema stays green).
- PTAL is used ONLY if E2SFCA is activated — acquisition is cheap insurance, not a commitment.

## Superseded / unused artefacts (on disk, retained for audit trail)
- **`reports/` holds three artefact generations** (2026-06-27, 2026-06-30, 2026-07-03). **The 2026-06-30 set is canonical** — it matches the frozen snapshot (granularity: LSOA 95.6% / MSOA 81.4% empty; the 06-27 figures 95.5/81.2 are superseded working numbers). Cite only the 06-30 files in the report.
- `data/external/iod2025_imd_lsoa_2025-06-27.csv` (`b1b716aa2e476449`) — IoD **File 7** LSOA-level, acquired pre-D-007; superseded by File 10 v2 LAD summaries; unused by the pipeline.
- `data/external/SOURCES.md` (`5760cbc148a8cad3`) — planning-era provenance file this register replaces.

*Update discipline: add/amend a block in the SAME pull request as any acquisition or re-harvest; a data file without a register entry is treated as unprovenanced and must not be read by pipeline code.*
