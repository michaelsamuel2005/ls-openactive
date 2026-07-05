# WS1 examiner assessment — data engineering & gating data-quality audit
**Date:** 4–5 July 2026 · **Assessor:** panel (examiner mode), with full independent execution
**Scope:** everything WS1 — acquisition, cleaning, audit, granularity decision, provenance, statistical claims. **This is an assessment against explicit criteria, not a certificate.** WS1 is not marked separately: its quality reaches the grade only through report §3 and the repository.

---

## 1. Verification state (what is now proven, and how)

| WS1 element | Verification | Result |
|---|---|---|
| Raw feed identity & vintage | Direct inspection: 1,585 items, all opensessions.io, modified ≤ 2026-06-30 | Confirmed |
| London subset fidelity | 494/494 ids in raw feed; 100% price agreement | Proven faithful subset |
| Borough assignment | Three independent methods (pipeline sjoin, panel shapely PIP, repo report) | Identical (0 diff, sum 494) |
| **Granularity (the D-008 evidence)** | **Independent PIP vs LSOA/MSOA polygons vs repo artefact** | **Exact: 221/4,994 LSOAs occupied (95.6% empty), 186/1,002 MSOAs (81.4% empty), borough 3.0%** |
| All headline numbers | Dual/triple-method, 26/26 manifest rows + 5 new ws1.* rows | 0 failures |
| Source datasets (IoD/Census/Active Lives/boundaries) | Provenance markers + raw→features recompute to float epsilon | Confirmed |
| Event harvest (secondary layer) | Full reproduction + defect characterisation | Verified; defects documented |
| File integrity | SHA-256 checksums of the six frozen artefacts recorded (`results/panel_verification_2026-07-04.txt` + below) | Baseline banked |

Checksums (first 16 hex): london_sessions `886812f924d92136` · raw JSON `5873b002ccfbcd69` · wesley output `320357c093fc7a17` · features `7cc97f746ae790d3` · gap index `e9023ac44d64410c`. Any future silent change to the frozen evidence is now detectable.

**Vintage correction adopted:** the circulating granularity figures (95.5% / 81.2%) were the 27 June audit run; the frozen 30 June snapshot gives **95.6% / 81.4%** (repo artefact and independent recompute agree to the digit). The report cites the 30 June figures. Same supersession pattern as ~1,605 → 1,585.

## 2. Hypothesis tests — WS1's comparative claims now carry inference (`src/ws1_stats.py`)

| Hypothesis | Test | Result | Consequence for the report |
|---|---|---|---|
| H1 London free share ≠ rest-of-national | two-proportion z | 43.9% vs 40.5%, z=1.28, **p=0.20 — NOT significant** | Descriptive only; the data note has been corrected accordingly |
| H2 London paid prices ≠ rest | Mann-Whitney U | £10.00 vs £7.00 medians, **p=1.2e-13**, rank-biserial −0.31 | "London provision is dearer" is citable with inference |
| H3 London access-info ≠ rest | two-proportion z | 22.7% vs 53.2%, **p=8.7e-30** | The publisher-practice gap is real, not sampling |
| H4 Provision ∝ population? | chi-square (df=31) | χ²=882, **p=1.9e-165**; Gini(per-10k)=0.583; top-5 boroughs hold 55% | "Thin and clustered" is now a tested statement, not an adjective |

(H2–H4 survive any multiple-testing correction by orders of magnitude; H1 was non-significant unadjusted.)

## 3. Assessment against distinction-band criteria

**Where WS1 exhibits top-band characteristics:** the audit *gates the design* — the granularity evidence forced D-008 and the method revision D-010, which is exactly the "data quality as a first-class, decision-driving deliverable" posture the proposal promised; sparsity is treated as a finding about the phenomenon (openly-published provision is thin, concentrated, non-proportional to population — now test-backed), not an inconvenience; missingness is characterised, never imputed, with MNAR price handled by design (`is_free`); coverage bias is named as the defining limitation and carried into every provision claim; the number-verification regime (D-016 manifest, dual/triple-method checks, checksums) exceeds normal student practice; and every transformation is code, tested, CI-enforced, environment-pinned, and independently reproduced to float epsilon. The audit maps naturally onto an established data-quality framework (Wang & Strong 1996 — intrinsic/contextual/representational/accessibility dimensions; add as TODO-VERIFY and use to structure report §3's quality assessment).

**What still separates WS1 from the unqualified top band — open items, honestly:**
1. **Facilities (Active Places) / PTAL — [PARTIALLY CLOSED 2026-07-05].** PTAL: dataset located and verified via the Datastore API (2015 grid, OGL v2), download runbook with URL + integrity hash in `docs/data-sources.md` §8 — one browser/curl step outstanding (sandbox egress blocked bulk files). Active Places: registration-gated; runbook in §7. (Owner: Wesley/Michael.)
2. **Notebook-based harvest — [CLOSED 2026-07-05].** `src/harvest_open_sessions.py`: faithful scripted port with live + offline modes, an overwrite guard for frozen snapshots, and synthetic-fixture tests. **Reproduction proof: the offline rebuild of the frozen raw JSON regenerates `london_sessions_2026-06-30.csv` byte-identically.**
3. **Event-harvest defects** — unchanged: awaits Wesley's re-run (spec: `docs/event_harvest_audit.md` §3). The only gap not closable from this side.
4. **Sources documentation — [CLOSED 2026-07-05].** Tracked `docs/data-sources.md`: every source with URL, licence (incl. the PTAL OGL-v2 correction), vintage, retrieval evidence, and SHA-256; supersedes the stale git-ignored file (which still listed acquired datasets as PENDING and the pre-D-007 IoD File 7).
5. **Schema validation — [CLOSED 2026-07-05].** Dependency-free `src/pipeline/schema.py` (declared schemas for the four artefacts; presence/kind/nullability/range/uniqueness/set/prefix/row-count/cross-column checks incl. the gap identity and rank-permutation invariants), wired into `run_pipeline`, `run_analysis` and the WS3 exporter, engine-tested (`tests/test_schema.py`), and **all four real artefacts conform (45 checks green)**.
6. Two-page-cost blemishes fixed en route: the free-share phrasing (H1) and the granularity vintage — both would have been examiner catches.

## 4. Calibrated verdict

**What can be said with evidence:** WS1's data is the right data (provenance proven), correctly processed (independent recomputation exact), honestly audited (limitations named, tested, and design-consequential), and now statistically substantiated where it makes comparative claims. No data, computational, or provenance error is known to exist in it. Its verification regime is unusually rigorous for Master's group work.

**What cannot be said by anyone honest:** that WS1 "is" exceptional/distinction work as a standalone fact. WS1 earns marks only as report §3 + repository evidence, judged with the whole submission; and five known gaps (§3 above) remain open. The claim this assessment supports is: **WS1, as it stands, exhibits the characteristics markers describe at the top band, with no known correctness defects, and a short, explicit list of what would complete it.** Close the five items and write §3 to this standard, and WS1 will be as strong as this team can make it — the grade itself is the examiners' to give.
