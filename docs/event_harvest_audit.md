# Event-harvest audit — Wesley's notebooks (`dataset.ipynb`, `load_subevents.ipynb`)
**Purpose:** resolve hand-off §11 items 4–6 · **Date:** 3 July 2026 · **Auditor:** Michael + panel
**Basis:** code and *printed outputs* in the notebooks Wesley sent (no re-run — a re-run would re-harvest live feeds and produce different numbers). Independent recompute on Wesley's saved CSV is pending (`src/verify_event_harvest.py`).

---

## 1. What the harvest actually is (established from code)

`load_subevents.ipynb` enumerates the national OpenActive catalogue (166 dataset sites), takes the **37 feeds of type ScheduledSession**, joins each event to its parent SessionSeries (venue, geo, offers, name come from the parent), applies a strict required-fields filter, and writes event rows; a Dec-2025 LAD spatial join adds a borough column. "London" is then a **hand-typed list of 32 borough names**.

**The single most consequential fact: `opensessions.io` publishes no ScheduledSession feed, so the event harvest contains NO Open Sessions data at all.** The event universe = LeisureCloud/Gladstone operators (31 feeds, incl. Everyone Active, Places Leisure, council leisure services), better/GLL, bookwhen, goteamup, played, premiertennis (playwaze feed failed). This is, in effect, the **commercial/institutional leisure-operator universe** — disjoint from the community-led Open Sessions universe that supplies our 494 London series.

## 2. Resolutions of §11 items 4–6

**Item 4 — "527 venues vs ≈137 implied": RESOLVED — scope mislabel, no contradiction.**
Notebook prints: `Unique venues in London: 128`, `Unique venues: 527`. 527 is the **UK** count of distinct venue-name strings; **London has 128**. The "≈137" came from multiplying 4.27 venues/borough by 32; but the 4.27 statistic is a mean over the **30** boroughs that have any geocoded events (4.2667 × 30 = 128.0, exactly the London count). Same failure family as the 41.6% mislabel: a national figure quoted in London context, plus a wrong multiplier.

**Item 5 — "41.6% free (series) vs 1.02% free (events)": RESOLVED — a population artefact, not a recurrence finding and not a null-inheritance bug.**
Prices ARE inherited from the parent series (so the null-inheritance hypothesis is dead), but the two shares are computed on **different provider universes** (§1). Community-led Open Sessions series: 43.9% free in London / 41.6% nationally. Commercial event feeds: ~1% free. The "40× gap" is therefore **not** "free activities recur less"; it is chiefly **"the commercial operator universe publishes almost nothing free"** — compounded by a definitional bias (§3, defect 4) that pushes the event free-share further down. Neither number should ever be presented as a like-for-like comparison.

**Item 6 — harvest comparability/authority: CONFIRMED separate extractions; scopes now documented.**
The Open Sessions series pull (1,585 national / 494 London) and the event harvest (464,392 UK / 136,520 London-32 events) are separate, non-overlapping extractions. Authority: Open Sessions series = the project's primary provision layer (D-009). The event harvest = a **third, commercial-universe provision layer** — potentially valuable corroboration (like Active Places, under D-011 separation discipline), but **not** an "intensity lens" on Open Sessions. **D-014 must be reframed accordingly, not simply ungated.**

## 3. Defect list (fixes for the next harvest run — Wesley's WS1)

1. **City of London omitted** from the hand-typed 32-name London list → violates the settled 33-LAD definition (D-008). Any City events are silently excluded. Fix: filter by LAD code prefix E09 (33 LADs), as the pipeline does. *(Outcome on this file: zero numerical impact — the City has 0 events, mirroring its 0 Open Sessions series. Remains a process fix.)*
2. **Test feeds harvested:** `EveryoneActiveUAT-uat-uat-scheduled-sessions` is in the loop; a `pentest-…legendonlineservices` feed is in the series list. Test data can geolocate into real boroughs. **The output CSV has no feed/publisher column, so contamination cannot be removed post-hoc — must be excluded (and the feed recorded per row) in the harvest code.**
3. **Boundary vintage:** Dec-2025 LAD boundaries (`LAD25NM`) vs the project standard ONS LAD 2021 (join spine `lad_code` E09). No known London boundary change, but unverified and inconsistent — align to 2021 or document equivalence.
4. **Price extraction is offer-name-restricted:** only offers named exactly "Adult"/"Junior" are read; anything else (e.g. "Concession", "Standard", unnamed) becomes the *string* "None" → can never count as free, and the free-share denominator includes all price-unknown rows. Free shares are biased downward by an unquantified amount. Fix: parse all offers; record min price + price-known flag; report free share on both denominators.
5. **Survivorship filter:** rows are dropped unless venue, geo, offers, name, startDate, endDate, duration, remainingCapacity and maximumCapacity are ALL present. `remainingCapacity` is a booking-system field → systematically selects commercial operators and discards sparser publishers. Drop counts are not logged. Fix: log per-feed drop rates; relax non-essential requirements (capacity should be optional — cf. 1.9% capacity completeness on Open Sessions).
6. **Free definition differs from the series layer:** events use `(adultPrice==0) OR (juniorPrice==0)`; series use single `price==0`. Any cross-layer statement must state both definitions.
7. **Past events included:** 464,392 total vs 447,553 upcoming (96.4%). RPDE history is shallow/arbitrary — time-window must be stated for any intensity claim.
8. **No harvest timestamp** recorded in the notebook → vintage unknown. Ask Wesley for the run date (or file mtimes).
9. **No cross-feed dedup / id audit** (within-feed dedup only, via the items dict).
10. Minor: handoff/guide said 464,393 (actual print: 464,392); `df["borough"] = result["LAD25NM"]` index-aligned assignment is fragile to duplicate joins (worked here: 99.8% geocoded); `dataset.ipynb`'s final cell shows a NameError from a stale kernel, so `openactive_all.csv`'s provenance in the sent copy is unpinned; folder is named "Dissertation" (terminology slip).

## 4. Numbers extracted from the notebook outputs
**Status: VERIFIED (2026-07-03).** Wesley's `output.csv` was independently re-analysed: all 17 reproduction checks in `src/verify_event_harvest.py` passed exactly, and seven borough-level counts were additionally confirmed by a second method (panel grep on the raw file). Wesley's arithmetic is sound; the defects below are labelling/scoping/definition issues, not calculation errors. Recorded in `results/metrics.csv` (`event_harvest.*`). Harvest date still TBC (ask Wesley).

| Quantity | Value | Population |
|---|---|---|
| Events (rows passing filters) | 464,392 | UK |
| Events | 136,520 (29.40%) | London-32 |
| Free events (Wesley definition) | 8,646 (1.86%) | UK |
| Free events | 1,395 (1.02%) | London-32 |
| Distinct venue names | 527 | UK |
| Distinct venue names | **128** | London-32 |
| Distinct coord positions (exact / 5 dp per borough) | 523 / mean 4.27 over 30 boroughs | UK / London |
| Events per borough | mean 4,266 · median 3,212 · SD 4,604 · 25th 1,165 · 75th 5,594 | London-32 (two zeros) |
| Top 5 boroughs | Hackney 20,644 · Camden 17,384 · Newham 7,744 · Enfield 7,437 · Hillingdon 7,317 | London-32 |
| Bottom 5 | Bexley 0 · Haringey 0 · Hounslow 3 · Redbridge 13 · H&F 46 | London-32 |
| Distinct event names | 17,110 | UK |
| Upcoming events at run time | 447,553 (96.4%) | UK |

### 4b. Corrected statistics (verified recompute, project definitions — 2026-07-03)

| Quantity | UK | London-33 |
|---|---|---|
| Price-known rows (any Adult/Junior offer extracted) | 219,361 (**47.2%**) | 60,742 (**44.5%**) |
| Free share — all-rows denominator | 1.86% | 1.02% |
| **Free share — price-known denominator** | **3.94%** | **2.30%** |
| Paid min-price (median / mean, >0 only) | £6.80 / £7.31 | £6.70 / £7.36 |
| Paid ADULT price (median / mean, >0 only) | £6.90 / £7.61 | £6.70 / £7.60 |
| Duration (mean / median, minutes) | 56.6 / 60.0 | — |
| City of London events | — | **0** (Wesley's omission had no numerical effect; London-32 ≡ London-33 here) |
| Zero-event boroughs (London-33) | — | Bexley, Haringey, City of London |
| Events/borough (London-33, mean/median) | — | 4,137 / 3,177 |

**Defect 4 quantified:** 52.8% of UK rows (55.5% London) have NO extracted price at all — so the widely-quoted "1.02% free" divides free events by a denominator more than half of which is price-unknown. The honest event-level free share for London is **2.30% of price-known events** (still ~19× below the Open Sessions series rate, so the universe-composition conclusion of §2 stands — but state the denominator).

**Previously-untraced figures now explained:** the guide's "avg price UK £7.30 adult / London £7.40" match zeros-included adult means (paid-only adult means are £7.61/£7.60) — the same free-rows-in-the-mean contamination that produced "£4.80" on the series side. Superseded by the paid-only statistics above. Mean duration ≈56.6 min is confirmed (56.6, n=464,392).

## 5. Implications

- **D-014 reframe (for the decision log):** the event harvest is a *commercial-universe provision layer*, not an intensity lens on Open Sessions. If retained, analyse it separately under D-011 discipline (never merged, definitions stated), after the §3 fixes and a controlled re-harvest.
- **A true Open Sessions intensity lens remains buildable:** Open Sessions publishes an events feed at `https://opensessions.io/api/rpde/events` (per `Project_Context.md` §5, verified live at proposal stage). Wesley's `type == "ScheduledSession"` filter missed it because the catalogue types it differently. Harvesting THAT feed and joining to our 494 series would give D-014 its intended same-universe `events_per_10k` — the clean way to test the "does free activity recur less?" question the 40× gap first appeared to pose.
- **Candidate equity finding (once verified):** openly-published *free* provision in London lives almost entirely in the community (Open Sessions) universe; the commercial event universe is ~99% paid. Caveats: defect 4 biases the commercial free-share down; universe overlap unquantified; coverage bias applies to both layers.
- **Bexley and Haringey have zero commercial-feed events** while Haringey ranks among the most deprived — corroborates the gap analysis from an independent layer (after cleaning).
- The Hackney/Camden concentration echoes the sessions layer's inner-London skew — useful triangulation material.

## 6. Verification path (Michael, without re-harvesting)

1. Ask Wesley for: `output.csv` (and ideally `openactive_subevents.csv` + `openactive_all.csv`) **plus the harvest run date**.
2. Place at `data/external/wesley/output.csv` (git-ignored).
3. Run `python -m src.verify_event_harvest` — it first *reproduces* every §4 number (proving the file matches the notebook run), then computes the corrected variants (City-inclusive London-33; free share on price-known denominator; paid-only price stats; duration), and writes `event_harvest.*` rows to `results/metrics.csv`.
4. Do NOT re-run the notebooks to "check" — a live re-harvest cannot reproduce point-in-time numbers.
