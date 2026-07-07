# Improvement register — everything open, priority-ordered
**Purpose:** the single checkable list of every known improvement, upgrade, and open item across the project. Priority = marks impact × time pressure (draft to supervisor ~10–14 Aug; submission 1pm 4 Sep). Tick items only when the "done means" clause is true. Update via PR like any other doc.
**Legend:** owner in bold · effort S/M/L · status ☐ open / ◐ partial / ☑ done-pending-verification.

---

## TIER 1 — CRITICAL (the marks live here; start/chase this week)

- [ ] **1.1 WS3 recommender build** — **Clarence** · L · *The largest unbuilt marks block (LO4).* Done means: the five-PR sequence in `docs/ws3-recommender-spec.md` §6 merged (scaffold+filters → relevance → equity+α → personas+evaluation harness → results tables), synthetic tests green in CI, `ws3.*` manifest rows written. ◐ Kickoff status unknown — confirm the message + OneDrive/Release data handover went out and collaborator access works.
- [ ] **1.2 Evaluation contract finalised BEFORE build** — **Fahmi** · S · Done means: spec §5/§5b/§5c reviewed and frozen by Fahmi, deviations logged. Blocks honest evaluation of 1.1.
- [ ] **1.3 Four-eyes re-derivation of manifest headline numbers** — **Fahmi** · S · Outstanding since 3 July. Done means: a second member independently re-derives the headline `results/metrics.csv` rows; discrepancies raised or verified_by column completed.
- [ ] **1.4 WS4 dashboard** — **Michael** · L · Unstarted; your own LO4 contribution. Done means: one-page view-by-decision design doc (Munzner task framing, per founding D9) agreed, then a code-based build (Streamlit/Dash per proposal; Tableau rejected CR-6), every number a pipeline artefact, vintage + absence-of-data caveat on each view.
- [ ] **1.5 Report §3 + §5 drafting** — **Michael (+Wesley for §3)** · M · Material verified and frozen; the top-band devices are bound into the skeleton (findings→decisions arrangement, DQ-framework mapping, reproducibility-spectrum position, threats-to-validity, robustness-first results, corrections narrative, traceability appendix). Done means: chapters drafted to the skeleton's page budget with every number manifest-traceable.
- [ ] **1.6 Literature review (§2)** — **all four, one strand each** · L · The biggest pure-writing gap. Strands: inactivity/public health (Wesley), equity of provision + 2SFCA (Michael), recommenders/fairness (Clarence), evaluation validity (Fahmi). 4–6 papers deep each, critical not descriptive. Done means: strand notes → drafted chapter; every reference read by a member (see 2.6).
- [ ] **1.7 Draft date agreed with supervisor** — **Michael** · S · The one-draft/≥14-days rule makes ~10–14 Aug the hardest internal date. Done means: an explicit date in writing, in the calendar, in the skeleton.
- [ ] **1.8 PR #5 reviewed and squash-merged** — **teammate** · S · Still open (reviewer request has slipped repeatedly). Done means: genuine review against the PR checklist, squash-merged with the clean message, branch deleted, everyone re-branches from main.
- [ ] **1.9 Branch-protection rulesets active** — **Michael** · S · `main` (PR + 1 approval + required "lint + tests" check) AND `feat/*` (block force pushes — the 5 July incident must be unrepeatable). Done means: both rulesets visibly Active in Settings → Rules. Status unconfirmed.
- [ ] **1.10 Supervisor sign-off bundle** — **Michael** · S · D-009/D-010/D-011 + D-014 reframe + D-015 ratification; handbook ambiguities (SEMTM vs EMATM code; IEEE vs Harvard — affects 2.6; tables-in-page-count; reassessment auto-extension interaction with the group deadline); presentation slot booking; written confirmation of the 6 July documentation guidance; surname resolution (O'Grady vs Avdic — then fix README/team.md/knowledge files). Done means: answers recorded in the decision log / unit-rules.
- [ ] **1.11 `src/bootstrap_ci.py` committed** — **Michael** · S · The bootstrap CI [0.097, 0.705] currently exists only in audit logs; §5 may not cite it until it is a committed, seeded script writing a results row. Twenty-minute job.

## TIER 2 — HIGH (bounded strengtheners; do while Tier 1 runs)

- [ ] **2.1 Active Places acquisition + facilities corroboration** — **Wesley/Michael** · M · Registration-gated (runbook: `docs/data-sources.md` §7). Unlocks the D-011 corroboration layer and the "thin sessions AND thin facilities" triangulation for §5. Pipeline ingests it unchanged; schema must stay green.
- [ ] **2.2 Event-harvest re-run with fixes** — **Wesley** · M · Fix list: composite (feed,id) key; exclude UAT/pentest feeds; record feed per row; parse ALL offers (not just "Adult"/"Junior"); log per-feed drop rates; state the time window. Spec: `docs/event_harvest_audit.md` §3. Done means: re-harvested file passes a rerun of `src/verify_event_harvest.py` phase-2 logic with the defects gone.
- [ ] **2.3 Harvest date for the event layer** — **Wesley** · S · 30-second answer; manifest vintage still "TBC". Then rerun the verify script with the date argument.
- [ ] **2.4 Open Sessions events-feed harvest (same-universe intensity lens)** — **Wesley (or Michael via the scripted harvester pattern)** · M · D-014 option (b): `opensessions.io/api/rpde/events` gives the TRUE events-per-series lens and cleanly answers "does free activity recur less often?" Optional but the single most interesting bounded analytical extension left.
- [ ] **2.5 Second held-out outcome (adult obesity via Fingertips)** — **Michael** · S/M · Optional under D-015; must be distinct from inactivity and from Census bad-health. Strengthens validation triangulation if time allows.
- [ ] **2.6 Reference verification programme** — **all** · M · Every TODO-VERIFY reference read by a member before it enters `references.bib` (Wang & Strong; Peng 2011; Kaminskas & Bridge; Burke 2017; Liu & Burke; the two fairness surveys; Karimi arXiv id unverified; Sallis; Withall; Rubin; Luo & Wang/Qi…). Style (Harvard vs IEEE) pends 1.10. Done means: bib entries complete, style consistent, zero unread citations.
- [ ] **2.7 Personas document** — **Clarence + Fahmi** · S · `docs/ws3-personas.md`, 6–10 personas spanning the constraint space, labelled illustrative. Blocks the evaluation harness.
- [ ] **2.8 Contribution evidence spread** — **Clarence, Fahmi, Wesley** · ongoing · Repo history is currently near-single-author; the handbook makes per-member GitHub activity + weekly logs load-bearing for each reflective account (20% each). Done means: all four have commits/PRs and current weekly logs. A small shared script to render per-author activity charts is legitimate common tooling — build once, all four use it.
- [ ] **2.9 Proposal delta-addendum OR refreshed condensed one-pager** — **Michael** · S · Decision pending (see review of the condensed proposal: six superseded items incl. IoD2019→2025, small-area→borough, MICE→none, UMAP→quadrants, E2SFCA scope, validate-vs-deprivation→D-012). File the PDF in `docs/` as historical either way.
- [ ] **2.10 Formative-presentation feedback actioned** — **all** · S · Panel feedback (if any) logged and folded into the report plan. Status unknown — capture it before it evaporates.

## TIER 3 — MEDIUM (results hygiene and robustness polish)

- [ ] **3.1 Manifest rows for WS2 headline stats** — **Michael** · S · ρ/CI/sensitivity currently live in `reports/incremental_validity.csv` (fine) but a `gap_index.*` recorder would unify everything under `results/metrics.csv` per D-016.
- [ ] **3.2 `median_price` column fix (audit Mo2)** — **Michael** · S · Borough feature includes free sessions in its median (contaminated definition, dormant but misleadingly named). Rename to `median_price_all` or recompute paid-only; schema + tests updated.
- [ ] **3.3 README refresh** — **Michael** · S · Stale: "direction being finalised" banner; milestones table (formative done; draft date); Python "3.10+" vs pinned 3.11; tech stack line; supervisor name pending 1.10. One honest pass.
- [ ] **3.4 team.md completion** — **all** · S · GitHub usernames missing for three members; role split stale ("Clarence — Prototype & evaluation lead" vs actual Clarence WS3 / Fahmi evaluation).
- [ ] **3.5 Tooling-docs removal per D-017 housekeeping** — **Michael** · S · Verify `docs/claude-project-instructions.md` and `docs/prompt-playbook.md` are actually untracked/removed (the D-017 entry records the intent; the removal commit may not have run). `git ls-files docs/ | grep -E 'playbook|instructions'` decides.
- [ ] **3.6 Config comment + .gitignore note (audit minors)** — **Michael** · S · `config.py` sessions path says "(latest)" — should say FROZEN; document the deliberate blanket `data/` ignore choice in the .gitignore.
- [ ] **3.7 Notebook pointer line** — **Wesley** · S · One markdown line in `data_audit.ipynb` routing readers to `docs/data-sources.md` for provenance.
- [ ] **3.8 Full data/ OneDrive mirror** — **Michael** · S · Release assets cover 3 files; the full tree (incl. Wesley's 475MB event file and Census/IoD/boundaries) still needs an off-laptop copy. Handbook: data loss ≠ exceptional circumstance.
- [ ] **3.9 Guides/PDF re-issue** — **Michael** · M · Plain-English Guide + Technical Dossier still carry superseded numbers (team warned off them). Re-issue from the corrected corpus when report drafting stabilises the prose (may be OBE if the report supersedes them entirely).

## TIER 4 — LOW (defensive polish; only after Tiers 1–2 are moving)

- [ ] **4.1 Presentation deck skeleton** — **all** · M · 20% component, 15 min, Teams, all members speak; window opens week of 24 Aug. Skeleton by early Aug; content flows from the report. (Rises to Tier 1 in August.)
- [ ] **4.2 pyproject/ruff config + pre-commit hooks** — **anyone** · S · CI already enforces; local hooks just shorten the loop.
- [ ] **4.3 Dashboard heuristic-walkthrough protocol** — **Michael + Fahmi** · S · The consent-based peer task or expert walkthrough plan (proposal §8/Mod2) — drafts inside the WS4 design doc.
- [ ] **4.4 Handover pack assembly** — **all** · M · Reproducible handover for London Sport (README-level run instructions, licence/attribution block, artefact index). Mostly assembly from existing docs; end of August.
- [ ] **4.5 Knowledge-base refresh (project workspace)** — **Michael** · S · Project_Context still pre-audit (small-area, imputation, Open Sessions description); sync the corrected docs + decision log so future sessions start from truth; fix the workspace description label.
- [ ] **4.6 Moran's I / small-n phrasing pass** — **Michael** · S · Ensure §5 prose states the normal-approximation caveat and n=32 power framing exactly once, correctly.

---

**Standing invariants while working ANY item (from `docs/engineering-rules.md`):** numbers only from the manifest/results files with population labels · no imputation · no accuracy vocabulary in WS3 · City of London excluded from scaling, quadrant NA · branch → PR → review → squash · schemas green · vintages stated everywhere.
