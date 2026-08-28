# M-01–M-08 foundation programme — independent verification and block-by-block assessment

**Date:** 24 August 2026
**Prepared by:** AI assistant (cloud session), at Michael's request: "assess each one by one thoroughly … what is it, what is academically exceptional, and what is missing."
**Object assessed:** `michael-foundations-m01-m08-20260824/` (24 Aug handoff from the local Codex process), verified this session from bytes staged off the device.
**Provenance:** AI-assisted analysis; PROPOSED; contains no human signature and closes no gate.

| Human-control field | Entry |
|---|---|
| Reviewed by Michael | *(blank)* |

---

## Part 0 — Verification verdict (read this first)

**The handoff is truthful.** I independently re-derived its headline claims from the staged bytes in a clean cloud environment, and every number and hash I could test reproduced exactly. The one thing I could not check is the Mac's free disk (the device shell VM failed to start this session; file staging still worked).

### FACTS — independently verified this session

| Claim in the handoff | My independent result |
|---|---|
| 124 requirements = 45 PROVED_BOUNDED / 43 INCOMPLETE / 34 MISSING / 2 CONTRADICTED | **Reproduced exactly** (awk count + their validator, byte-identical output) |
| 62 gates = 2 RESOLVED_BYTES_VERIFIED / 60 unresolved, with the stated 9-state distribution | **Reproduced exactly** |
| Matrix `a2f808be…`, gate register `f610310b…`, validator `61fbe9f3…`, receipt `31fb7f41…`, Wesley-v2 manifest `6d785e45…` | **All five SHA-256s match** |
| OA-4 v3 card at `19c0fced…` | **Match** — staged the actual card (46,759 bytes, currently materialised, not an iCloud placeholder) |
| Manifest chain: `PROGRAMME_MANIFEST.tsv.sha256` → programme manifest → 11 lane/sub `SHA256SUMS` → every file | **All 11 manifests verify; chain closed end to end** |
| Master handoff `f3c4c85d…`, final approval `c407e59d…` (per document index) | **Match** |
| Root `M01_M08_HANDOFF_VERIFICATION_RECEIPT_20260824.json` binds programme + integration manifests | **Bindings match the hashes I computed** |
| `validate_completion_registers.py` passes | **Passes in my clean Linux environment with byte-identical PASS lines** (`PROGRAMME_COMPLETE=false`) |
| Bounded suites: M-03 48, M-04 80, M-05/M-06 25, M-07 exp. 20, scaffold 6, M-08 39, Wesley v2 26, register 27 | **Replayed** — see the portability findings below for the exact deltas and why every delta is environmental, not semantic |
| The 2 CONTRADICTED rows are M01-R14 (M-01 conjunctive closure) and M08-R12 (hidden programme) | **Confirmed in the matrix** |
| Work package pinned at `25722813…` | **Matches the base-manifest hash in my own Execution Register v3 from 9 August** — the two evidence chains (cloud pack and local programme) now cross-agree on the controlling source bytes |

### FACTS — new findings from the clean-room replay (all environmental/portability; none semantic)

Replaying the suites on Linux instead of the Mac's `/opt/anaconda3` produced four precise deltas. Each is fail-closed behaviour doing its job, but together they show the programme is **environment-bound and not yet self-contained**:

1. **F1 — no environment lock ships with the programme.** M-03 first ran 41/48 here: seven URI-format subtests fail because `rfc3987` is absent, so jsonschema's `format: uri` checking silently becomes a no-op — the tests correctly refuse to certify. Installing `rfc3987` gives **48/48 exactly as claimed**. This is the third recurrence of the environment-pinning defect family (v0.1 RB-08 → the v2.1 `rfc3339-validator` lock omission I found on 10 Aug → now no `requirements-test.lock` at all in the folder). The reproduction commands point at `/opt/anaconda3/bin/python`, i.e. one specific machine.
2. **F2 — two macOS-only constructs in test code.** `test_completion_registers.py` hardcodes `/private/tmp` (26/27 here; 27/27 in their recorded macOS run), and `test_candidate_expansion.py` reads `os.stat_result.st_flags` — a BSD/macOS attribute that raises `AttributeError` on Linux (20 passed + 8 subtest errors here vs 20/20 recorded). The `st_flags` use is honest in intent (it detects iCloud `SF_DATALESS` eviction) but needs a `hasattr` guard.
3. **F3 — the folder binds bytes outside itself.** The M-05/M-06 suite, the scaffold audit and 10 of 26 Wesley-v2 tests bind artefacts in sibling folders (`michael-execution-pack-v2-completed/pack/…`, the sealed DEF filing zip, the K7 tree). In my partial staging they fail closed — correct behaviour — but the deeper fact is that one bound target (`…v2-completed/pack/08_SPEC_EXTRACTS_EVIDENCE_20260809.md`) is **currently an iCloud dataless placeholder on the device itself**, so even on the Mac the full expanded run reports non-runs (their runner honestly prints `NOT_RUN_FILEPROVIDER_DATALESS`; their `SOURCE_INVENTORY.v0.2` self-flags `FILE_PROVIDER_RISK`). The programme's completeness claims survive because they are scoped, but the physical evidence base is one iCloud eviction away from being unreplayable.
4. **F4 — count-vocabulary mismatch (cosmetic).** "M-04 80 tests" is their runner's count (74 semantic + 6 metadata); pytest counts the same files as 154 because of parameterisation. Harmless, but the report should pick one counting convention per suite and say so, or an examiner replaying it will see a mismatch exactly the way I did.

**Proposed fixes (one short Codex task, after disk is freed):** ship `requirements-test.lock` pinning `jsonschema`, `rfc3339-validator`, `rfc3987`, `pytest` (and the interpreter version); replace `/private/tmp` with `tempfile.gettempdir()`; guard `st_flags` with `hasattr`; and either copy the four externally-bound artefacts into `integration/pinned_sources/` or record the external-binding boundary explicitly in the README. All four are successor-pack edits, not re-audits.

### ASSUMPTIONS I am carrying

- Disk headroom is still ~101–236 MiB as the handoff states (unverifiable this session).
- The `oa1–oa4-reading-record-20260823` folders I can see at the workspace root are **your own** reading records from 23 August (please confirm — item 8 below; if your OA-1 card is frozen through K7, my standing embargo on revealing my researched OA-1 spec answers can be lifted after I check the freeze).
- The 2025/26 unit weights/hand-in date remain unconfirmed (standing caveat).

---

## Part 1 — Block-by-block: what it is, what is exceptional, what is missing

One framing correction first, because you asked for "MSc dissertation level": this is the 60-credit **group project** (SEMTM0044), assessed as a group written report + repository (60%), group presentation (20%) and individual reflective account (20%). "Dissertation-level" is the right *ambition* for rigour; the *deliverable* is the group report, and this assessment ties each block to that.

### The integration layer (registers, validator, manifests) — the container itself

**What it is.** A machine-checked completion audit: a 124-row requirement matrix and 62-row dependency-gate register in TSV, a validator that re-hashes every evidence anchor with descriptor-pinned, no-follow, ancestor-swap-resistant file access, 27 adversarial tests against the auditor itself, and a closed manifest chain (sidecar → programme manifest → lane manifests → every file). In plain viva terms: *"our project's status claims are data, and there is a program that refuses to run if any status, hash, or dependency edge has been tampered with."*

**What is academically exceptional.** Three things, and they are unusual well beyond Master's level: (1) the *auditor is itself adversarially tested* — including a real ancestor-directory-swap race and a same-descriptor hash-and-parse (TOCTOU) test; (2) statuses have defined semantics (`PROVED_BOUNDED` ≠ complete) and the validator enforces non-strengthening, so the system cannot quietly promote a claim; (3) negative results are first-class — the register records its own programme as incomplete (`PROGRAMME_COMPLETE=false`) and two rows as CONTRADICTED. This is the mechanism that makes every other claim in the project checkable.

**What is missing.** (a) The three portability fixes above — without a lock file, "the suites pass" is a fact about one laptop; (b) the matrix's own honest caveat: nobody has yet verified that the 124 rows exhaustively transcribe the work package (that is your acceptance review, gate `WP-MICHAEL-ACCEPT-01`); (c) most importantly, **none of this earns marks until it is narrated in the report** — it currently lives in a folder no examiner will ever open unaided. Action: Michael (acceptance) + Codex (fixes) + me (report narration, offered below).

### M-01 — dependency and baseline audit (state: BLOCKED, closure CONTRADICTED — and that is correct)

**What it is.** The proof of what the team's repository actually does at commit `286da75`: ten tests and four script modules pass, and `tests.test_harvest` **fails** at line 102 — the London spatial filter returns nothing where the fixture requires ID `[1]`. The diagnostic narrows it to a first-call EPSG:4326→27700 transformation producing an infinite, invalid polygon while a later call in the same process behaves correctly (pyproj 3.6.1 / PROJ 9.3.1, network-enabled PROJ), and deliberately stops short of claiming root cause. Four defect filings (DEF-M0-1..4) are sealed and ready; DEF-M0-1 must cite decision-log **D-031** as the prior record (paste block already prepared in memo 17).

**What is exceptional.** Preserving a red result as the *deliverable* rather than an embarrassment is exactly the research integrity examiners reward — and the substance matters even more here: **an order-sensitive coordinate-transform failure in the London filter is a direct validity threat to the entire equity analysis**. If it silently mis-filtered, every LSOA/MSOA count downstream would be wrong. Catching it at the foundation, binding it to an exact worktree hash, and refusing to close M-01 until the owner fixes it is the strongest single "rigour" story your stream owns.

**What is missing.** Everything human: file the packet (you), owner disposition + correction (Wesley/acquisition owner), your non-author review of the fix PR, one owner-approved deterministic command, two accepted clean runs, and **one immutable real S0 delivery**. Nine of the 62 gates are this batch (`M01-CORRECTION`).

### M-02 — source-first evidence dossier (state: IN PROGRESS — the most human-gated block)

**What it is.** The proof that *you personally* understand the primary sources (OpenActive OA-1..4; theory TH-1..4) — reading records, comparison dispositions, personal attestations, then independent challenge. Current state: OA-1..3 have frozen v2 comparisons and *ready v3 attestation proposals awaiting one instruction from you*; OA-4 is v3-attested (`19c0fced…`, verified) but unchallenged; TH-1..4 are NOT_STARTED, with TH-1 blocked purely on lawful access to Belnap (1977) and Ginsberg (1988).

**What is exceptional.** The K7 leak-hygiene (pre-read kits sharing zero bytes with comparison dossiers; 202-event chained integrity log) makes "the student actually read the sources first" *demonstrable* rather than asserted — I know of no standard coursework practice that can show this. The insistence that a reprint may not silently substitute the required 1977 Belnap edition is real bibliographic discipline.

**What is missing.** Almost entirely *your* twenty minutes plus library access: (1) the one-line OA-1..3 adoption instruction (`APPROVE OA-1 TO OA-3 PERSONAL ATTESTATIONS`, if the proposals still express your understanding — Batch 1); (2) one Bristol library session for the two TH-1 texts (Ginsberg via the university's Wiley access, confirmed earlier in this stream; for Belnap, either the original chapter or the 2019 Omori & Wansing reprint *with a recorded edition crosswalk / source-map amendment* — the TH1 action doc is explicit about this); (3) appointing eligible challengers (Wesley only if he clears the 8-item eligibility declaration, per object). 13 of M-02's 24 rows are MISSING — the largest gap in the programme — and no machine can close any of them.

### M-03 — S0 input contract (state: technically stable proposal; `effective=false` is correct)

**What it is.** The boundary contract for what counts as an acceptable raw OpenActive delivery: a closed-shape v0.4 JSON schema plus a semantic validator enforcing declared-universe completeness, RPDE cursor chains and terminal-page rules, typed identifiers, tombstone-wins current-state reduction, chronology, extraction policy and a content-addressed release tuple; S0-AT-01..09 acceptance tests; 48 bounded synthetic tests (48/48 reproduced here once the format plugins exist).

**What is exceptional.** The fail-closed catalogue reads like a checklist of everything that silently corrupts real feed research (broken cursor chains, `true`/`1` JSON equality, non-2xx completions, self-authenticating caller authority — all mutation-tested), and the production mode's refusal of test-only authority is a genuinely good design idea (test evidence cannot leak into production claims *by construction*).

**What is missing.** The Phase-M2 contract family (evidence-atom/receipt/claim schemas at this generation), acquisition-owner co-design (Wesley), eligible reconstruction review, ratified trust/release policy, and — the big one — **a real S0 delivery**. All 48 passing tests are synthetic; the contract has never met a byte of real OpenActive data.

### M-04 — identity and stage-presence contract (state: technically stable proposal, not adopted)

**What it is.** The rules for *what is the same thing* across the pipeline: explicit vs generated identities, scoped equivalence, S0/S1/S1b presence semantics, hide relations, same-vintage collision quarantine, lifecycle distinctions — with typed evidence/coverage registries and 80 bounded tests (my pytest counts 154 due to parameterisation; same suite), plus an execution receipt and dual pre/post lane manifests.

**What is exceptional.** Identity is where most linked-data projects quietly go wrong; here every identity assertion must cite a typed evidence registry entry, generic deep-merge is *removed as unreachable*, and collisions quarantine the whole same-vintage cluster instead of guessing. The pre-execution vs post-execution manifest separation (input snapshot `2e41a6cb…` vs closed lane `65e1760…`) is chain-of-custody thinking applied to test runs.

**What is missing.** Real M-03 provenance (blocked on the real S0), eligible reconstruction review, the six `M04-D-01..06` dispositions, and team adoption. Nothing here is yours alone; it is reviewer + team work.

### M-05 — interpretation register (state: candidate rules, unratified)

**What it is.** Thirty **source-referenced candidate rules** for interpreting OpenActive data (schedule expansion, timezone/DST via RFC 5545, defaults, collisions), with 17 declared source bindings, closed action/fallback vocabularies, 81 typed fallback cases, and 8 open decisions (`M05-D-AUTHORITY … M05-D-GEO-ACTIVITY`). The register's own precision — 4 `SOURCE_BOUND_PERSONAL_RECORD`, 20 `PROPOSED_PROJECT_POLICY_UNRATIFIED`, 1 proposed, 2 unresolved, 3 blocked — is enforced wording ("source-referenced", never "source-bound production rules").

**What is exceptional.** The refusal to blur *what the spec says* and *what we chose* is the project's central epistemic discipline, and here it is per-rule and machine-checked. `M05-D-DEFAULTS` is the standout: whether the MOD SHOULD-defaults (absent ageRange ⇒ adults-only 18+; absent eventStatus ⇒ scheduled; absent gender ⇒ null) enter primary evidence or a separate sensitivity arm **is a statistical-methods decision that directly shapes Fahmi's missingness/imputation model and the activity-gap index** — the register has correctly isolated it instead of burying it in code.

**What is missing.** Your source/runtime review; the 8 decisions (several jointly with Fahmi/team — take `M05-D-DEFAULTS` and `M05-D-HORIZON` to the same meeting as the imputation design); primary RFC 5545/IANA byte retention (`M05-D-TIME` is BLOCKED on it); SOURCE-CONFLICT-M01..M12 dispositions; challenge, freeze, activation.

### M-06 — inheritance-policy table (state: disciplined candidate, not active)

**What it is.** Fifty-nine property/relationship rows answering "when a SessionSeries/EventSeries/FacilityUse parent has a value and the child doesn't, what may be inherited?", with typed outcomes, 51 executable visible fixtures, an explicit ban on generic deep merge, and 8 open decisions — including `M06-D-07` (the FacilityUse→Slot scope you must read at source before anyone dispositions those 10 rows).

**What is exceptional.** Most pipelines inherit by convenience; this one makes all 59 choices enumerable, testable and individually ratifiable, and keeps "the source permits it" separate from "we adopted it". The invalid-child-blocks-fallback proposal (`M06-D-04`) is a thoughtful fail-closed default.

**What is missing.** Row-by-row and decision-by-decision disposition (team), your source-first Slot/FacilityUse reading (`M06-D-07`), reviewer challenge, freeze. This is the bulk of the 18-gate `M03-M06-RATIFICATION` batch — one well-prepared team meeting.

### M-07 — golden and adversarial fixtures (state: zero golden — and the register says so)

**What it is.** Fourteen visible candidate fixtures in seven primary/contrast pairs, plus a machine coverage map from proof obligations to test contacts, 20 expansion tests, and an honest coverage report: 3 fixture classes fully mapped, 10 partial, 1 wholly open (`Slot → FacilityUse`); differential and mutation evidence absent.

**What is exceptional.** The candidate/golden distinction is being *enforced*, not just stated: a fixture becomes golden only after your hand re-derivation against frozen M-05/M-06 hashes, real application output, non-author review, and freeze. The coverage map that names which obligation each fixture touches (and which have no contact) is the kind of test-adequacy argument examiners almost never see.

**What is missing.** Everything that makes "golden" true: effective upstream inputs (the ratifications), your derivations, real execution outputs, review, freeze — plus the ten listed visible additions (Slot→FacilityUse first). Until then the correct phrase is the register's own: *hash-inventoried visible development corpus with executable regressions*.

### M-08 — hidden fixture programme (state: protocol only; completion CONTRADICTED — correctly)

**What it is.** A blinded-evaluation protocol: an independent custodian holds hidden test cases you never see; you commit to outputs; the first comparison is frozen before unblinding. What exists is the fail-closed validation profile + 39 protocol tests + custodian handoff forms. What does not exist: any hidden case, any appointment, any custody, any comparison.

**What is exceptional.** Bringing pre-registration/blinded-evaluation methodology into a data-engineering group project is beyond-brief ambition, and the register refuses the obvious cheat (a protocol test suite masquerading as an executed programme — hence the CONTRADICTED row, which is the system working).

**What is missing.** All of it is people: custodian + deputy + hidden-case authors + statistical/evidence reviewer (all non-Michael, conflict-separated), restricted custody, authoring, lock ceremony, one authorised run, frozen comparison, bounded unblinding. **Feasibility warning (examiner's eye):** in a four-person team where you are the component owner, the eligible-role arithmetic is tight — Clarence, Fahmi and Wesley must cover custodian/deputy/author/reviewer with per-object conflicts respected, during report-writing season. Decide *early* whether M-08 executes at reduced scope (e.g. one custodian + one small hidden set + supervisor as witness) or is honestly descoped to "designed and protocol-tested, not executed, because independence could not be staffed" — which is itself a defensible limitations paragraph. Do not let it silently become the reason M-07 never freezes.

---

## Part 2 — Assessment of the whole: the examiner's-eye view

**INTERPRETATION 1 — the discipline is now genuinely distinction-grade; the *scope* it governs is not yet.** What exists is a governance and evidence architecture of unusual quality wrapped around: one red harvest test, four attested-or-proposed source readings, ~264 synthetic tests, 14 candidate fixtures, and **no real data**. The handoff itself says this (§11) and it is right. The risk is no longer rigour; it is **ratio** — 124 requirements and 62 gates now govern the foundation of 8 of the 26 deliverables of one member's stream, and every new register generation adds verification surface (this 24 Aug generation added ~40 files and its own two new stale-doc/portability liabilities). Meta-work compounds; marks do not.

**RECOMMENDATION 1 — freeze the governance perimeter.** Adopt a standing rule: no new register generations, no new manifest layers, no new audit documents except (a) the four portability fixes, and (b) recording a gate that actually closed. The machinery is finished. From here, every Codex/AI hour goes into gate *contents* (real S0, fixtures, chapters), and every Michael hour goes into the signatures only he can give.

**INTERPRETATION 2 — the path to the top band runs through five things, in order:**
1. **Real S0 corpus** (Wesley's harvester + the M-01 fix + one immutable delivery). This single unlock turns M-03/M-04 from synthetic to real, feeds M-07 derivations, and gives the group report its data chapter. Everything else queues behind it. Wesley's `wy25780-data-acquisition` branch is where to look first (he has 7 commits across the remote).
2. **The human signature backlog you can clear alone in ~1 day**: work-package acceptance; identity clarification (Chellam Sebastian / Samuel — Alternative A takes five minutes if true); OA-1..3 adoption; TH-1 library session; DEF filing with the D-031 paste block.
3. **One team meeting** for the 18-gate ratification batch + M-08 staffing decision + report chapter ownership (Clarence, Fahmi, Michael, Wesley).
4. **Report chapters (60% of the grade).** Nothing in this folder is currently in report form. The foundation narrates into: Data & Provenance (M-01/M-03/S0), Methods-rigour (registers, fail-closed validation, K7 — 2–4 pages + appendix pointers), Interpretation & Missingness (M-05/M-06 feeding Fahmi's imputation and the index), Evaluation design (M-07/M-08), Threats to validity (EPSG defect, defaults sensitivity, data sufficiency LSOA→MSOA/borough). I can draft this skeleton now — it is the highest-value work I can do without any gate closing.
5. **Your reflective account (20%)** — the audit chain (v0.1 → hostile audit → v2.1 → re-audit → this programme) with its honestly-kept red runs is ready-made reflective material about supervising AI assistance with integrity; keep the receipts.

**INTERPRETATION 3 — the equity thread must stay visible.** The proposal's analytical core is equity of provision; the foundation's most brief-relevant content is exactly the places where data silences bias equity conclusions: the SHOULD-default dispositions (who gets counted as adult-only/scheduled/no-gender when publishers stay silent), inheritance rules (what a Slot inherits from a FacilityUse changes what "available session" means), and the London filter defect. Frame them that way in the report and the foundation stops looking like plumbing and starts looking like the equity analysis's integrity case.

---

## Part 3 — What I need from you (numbered; answer what you can, in any order)

1. **Deadline and format:** confirmed 2025/26 submission date and report word limit (the unit-page caveat still stands). This decides how aggressive the descoping in #6 must be.
2. **Real data status:** does any harvested OpenActive corpus exist yet (Wesley's `wy25780-data-acquisition` branch or elsewhere)? Roughly how many live London sessions? This decides LSOA vs MSOA/borough — the project's dominant open risk.
3. **Your five solo signatures (~1 day):** (a) work-package acceptance (or corrections); (b) identity clarification — Alternative A or B of the template; (c) the one-line OA-1..3 adoption instruction, if the proposals still express your understanding; (d) TH-1 library session — Ginsberg 1988 is reachable through Bristol's Wiley subscription (confirmed earlier in this stream); for Belnap use the original 1977 chapter or the 2019 Omori & Wansing reprint *with* the required edition crosswalk/source-map amendment; say if you want a step-by-step route sheet; (e) DEF-M0-1..4 filing with the D-031 paste block. Tell me which you are doing and I will prepare anything missing.
4. **Wesley round:** his exact GitHub handle/contact, the private repo owner/URL you are authorised to use, and (from him, in his own words) the eight-item eligibility declaration — or your decision to appoint a different reviewer for specific objects.
5. **Team meeting date** for the M03–M06 ratification batch (18 gates), `M05-D-DEFAULTS`/`M05-D-HORIZON` jointly with Fahmi, M-08 staffing (or descoping) decision, and report chapter ownership across Clarence, Fahmi, Michael, Wesley.
6. **M-08 scope decision** (can be provisional): full execution, reduced execution, or designed-but-not-executed with a limitations paragraph.
7. **Disk:** free ≥1 GB on the Mac before Codex reseals anything (I could not verify headroom this session; the device shell VM did not start, though file staging worked).
8. **Reading records:** confirm the `oa1–oa4-reading-record-20260823` folders are your own personal reading, done through the K7 flow. If yes and your OA-1 card is frozen, I can run the comparison step next and lift my OA-1 answer embargo.
9. **My next drafting target — pick one (or reorder):** (a) group-report skeleton + the methods-rigour section draft narrating this foundation (my recommendation); (b) the supervisor-routed data-sufficiency request (via Dalila O'Grady / Alex — never direct to London Sport); (c) the portability-fix successor task spec for Codex (F1–F4, ready to run once disk is freed); (d) the Bristol library route sheet for TH-1.

**RECOMMENDATION (if you only do one thing before we speak again):** item 3(c) — the OA-1..3 adoption — and item 5, booking the team meeting. One instruction and one calendar entry unblock more gates than any amount of further engineering.

---

*Integrity boundary: this memo verifies bytes and reproduces machine checks; it does not sign any acceptance field, close any gate, or attest any reading. Grade outcomes follow execution and examiner judgment; no band is guaranteed. The separate VISA coursework remains off-limits for reuse.*
