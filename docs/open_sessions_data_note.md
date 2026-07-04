# Open Sessions — corrected canonical description and figures
**Status:** resolves §11 items 1–3 of the 2026-07-03 hand-off · **Date:** 3 July 2026
**Provenance:** every figure below is computed by `src/verify_open_sessions.py` from the frozen snapshot (2026-06-30) and recorded in `results/metrics.csv` with population, unit, definition, commit, and corroboration. Panel cross-checks (independent grep counts on the raw file) agree exactly for n, free, paid, and access-info counts.

---

## 1. What Open Sessions is (corrected description — use this wording everywhere)

Open Sessions is **London Sport's free OpenActive publishing platform**. It is **not a London-only feed**: providers nationwide publish through it (one of the largest OpenActive publishers in the country), so the platform's headline figures are **national**. This project uses the **London subset** of Open Sessions as its primary provision source (D-009); the separate full national OpenActive catalogue (all publishers) is used for context only and is never merged.

**Every Open Sessions figure must therefore be labelled national or London. The two populations differ materially (see §2).**

## 2. The correctly-labelled figures (2026-06-30 frozen snapshot)

| Quantity | National (all publishers) | London (this project's subset) |
|---|---|---|
| Live SessionSeries | **1,585** | **494** |
| Free (price = 0) | 659 | 217 |
| Paid (price > 0) | 920 | 277 |
| Price missing | 6 | 0 |
| **Free share** (all-rows denominator) | **41.6%** | **43.9%** |
| **Typical paid price** (median, price > 0 only) | **£8.00** (n = 920) | **£10.00** (n = 277) |
| Paid price mean (price > 0 only) | £9.47 | £10.55 |
| Distinct venues (location_name strings) | 989 | **264** |
| Distinct mapped positions (lat/lon, 5 dp) | 954 | 252 |
| Accessibility info present (share True) | 43.7%* | **22.7%** (112/494) |

Definitions: free = price exactly 0; missing price is counted **not free** (audit-notebook rule; London has no missing prices, so both denominators give 43.9%). "Typical paid price" = median over paid series only — free and missing-price rows excluded. Venue = distinct venue name/address string in `location_name`.

\* The national accessibility figure traces to `reports/field_completeness_2026-06-30.csv` (692/1,585 — national-scoped, verified by integer reconstruction), not to `verify_open_sessions.py`, whose raw-JSON extractor does not pull that field. All other national figures are script-computed.

## 3. Superseded figures — do not reuse

| Old figure | Status | Replacement |
|---|---|---|
| "41.6% free" (context implied London) | **Confirmed mislabel** — it is the NATIONAL rate (659/1,585 = 41.58%), matching London Sport's published ~41% (>700 of ~1,700). | London: **43.9%**; national: **41.6%**, each labelled |
| "£4.80 typical paid price" | **Untraceable and doubly flawed** — no recorded population, and its magnitude matches zeros-included `describe()` medians (national £4.50; London £4.00), i.e. a statistic contaminated by free sessions, probably from the 27 June harvest. Exact origin not reconstructed. | London paid median **£10.00** / mean £10.55; national paid median **£8.00** |
| "~254–264 venues" | Resolved — 264 = distinct `location_name`; ~254 was an estimate close to the 252 distinct coordinate positions. | **264 named venues** (252 mapped positions) |
| "~1,605 national series" | Working figure, superseded by the committed-snapshot count. | **1,585** |
| Field-completeness block (price 99.6%, access 43.7%, capacity 2.0%) presented as London context | **National-scoped** — verified: each percentage × 1,585 reconstructs an exact integer. | London completeness computed separately (see §2; full set in `results/metrics.csv`) |

## 4. New substantive observations (for the report, with caveats)

1. **London's free share (43.9%) is slightly higher than the national platform rate (41.6%)** — the mislabel was conservative, but the two must never be interchanged.
2. **London's paid sessions are dearer than the platform-wide figure** (median £10.00 vs £8.00).
3. **Accessibility information is markedly scarcer on London series** (22.7% vs 43.7% national). Caveat: this measures *published* accessibility information, not actual accessibility — publisher practice, not provision quality, may drive it.
4. **Live-feed drift is real but small:** today's harvest (2026-07-03) has 497 London series (+3), free share 43.7%, paid median unchanged (£10.00). All reported analysis stays pinned to the frozen 2026-06-30 snapshot.

Standing caveats carried from the audit: series ≠ events (494 series is not 494 sessions-on-the-ground); coverage bias — OpenActive captures openly-published provision only, so all provision figures are lower bounds.

## 5. Corrections to propagate

- [ ] `Project_Context.md` §5 — replace the Open Sessions description with §1 above; granularity and method text also stale (D-008/D-010).
- [ ] `Activity_Gap_Plain_English_Guide_Updated.pdf` — Open Sessions block (London-only claim; 41.6%; £4.80; venue count).
- [ ] `Activity_Gap_Technical_Dossier.pdf` — same block.
- [ ] Any slides/guides quoting 41.6%, £4.80, ~1,605, or 254 venues.
- [ ] Hand-off Appendix B — items now resolved: rows 3–5 move from V3 to verified-with-definition.

## 6. Decision-log entries to file (docs/decision-log.md, once consolidated)

**D-016 — Metrics-manifest verification protocol. [ADOPTED 2026-07-03]**
All headline numbers live in `results/metrics.csv` (one row per metric: id, value, population, unit, vintage, source, definition, script, results file, commit, timestamp, corroboration, verified-by). Scripts own metric-id prefixes and replace only their own rows. No number enters a deliverable unless it traces to a manifest row. Rationale: the 41.6%/£4.80 mislabels arose precisely because numbers circulated without population labels or provenance. Alternative (status quo, numbers in documents) rejected as the demonstrated failure mode.

**Correction record — Open Sessions figures (2026-07-03).**
41.6% free confirmed as the national rate (London: 43.9%); £4.80 superseded by properly-defined paid-only prices (London median £10.00); venue count fixed at 264 distinct `location_name` (252 distinct positions); national live series 1,585. Field-completeness report identified as national-scoped; London completeness computed separately. Computed by `src/verify_open_sessions.py`; independently cross-checked by panel grep counts (exact agreement on all counts).

*Four-eyes step per D-016 remains open: a second team member (suggest Fahmi) re-derives the §2 headline figures independently before they enter the report.*
