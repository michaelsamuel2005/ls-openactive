# Step 7a authorship worksheet — C-BLOCK-05.md

**What this is:** prompts to write *against*, not sentences to copy. Answer each in your own words and
that prose becomes your authored `C-BLOCK-05.md`. Nothing here is drafted for you on purpose — the
whole point of 7a is that the reasoning and the phrasing are yours. Keep the **authorship notice** at
the top until the doc is genuinely yours, then rewrite it to say you authored it.

**How to work:** open `docs/applications/C-BLOCK-05.md` beside this. For each section below, read what
the scaffold currently claims, then write your version from the prompt — say *why*, as you understand
it, not just *what*. When you're done, send it to me and I'll review it for substance, over-claiming,
and whether it still sounds like you (I have your portfolio for that).

---

## Section-by-section prompts

**§1 — Why this is the keystone.** In your own words: what breaks downstream if the envelope, the
terminal decision object, the projections and the disclosure classes are *not* frozen first? Name one
concrete thing that can't be built on sand.

**§2 — The contract bundle.** Describe, as if explaining to a teammate, what each of the four
artefacts is *for* (decision-envelope schema, application-envelope schema, disclosure-classes,
projector+invariants). One clause each — what job it does.

**§3 — The vocabulary that must not collapse.** Pick the two collapses you think are most dangerous
(e.g. `U`→`F`, or `service_failure`→"no results") and explain *why* each is harmful to a real user.
This is where your own judgement should show.

**§4 — Disclosure classes + the projection rule.** In your words: why is a *single staff-complete
envelope with a derived public view* better than two hand-maintained schemas? What specific failure
does "fail-closed / drop-by-default" prevent? (Tie it to your F1 finding if you like — you found a
real instance.)

**§5 — The release-blocking invariants.** You don't need to restate the table. Instead: explain what
it means that each adversarial fixture is *caught* by its gate — why is "a gate that can't fail is not
evidence" the right standard? Say it the way you'd defend it at viva.

**§6 — CA-1 (the `L_reliance` referent).** This is the review's sharpest catch and worth owning
completely. In your words: how could a system score "safer by showing less," and how does binding the
referent to the terminal `DecisionEnvelope` (identical across P0/P1/P2) stop that? Why does
`INV-NONINTERFERENCE` make the fix real rather than aspirational?

**§7 — The decision-table row.** Keep the structured format, but write the `rationale` line yourself.
Leave `date` and `decision_log_ref` as PENDING — those aren't yours to set.

**§8 — What to agree with Michael and Wesley.** These are your open questions for the workshop. Add
anything Step 4b surfaced (the `budget_state.budget` meaning, the `predicate_id` split, the provenance
versions) so the list is genuinely yours and current.

**§9 — Permitted wording.** Write the one-sentence claim this artefact licenses — bounded, no
"secure/compliant/accessible".

**§10 — Status and next step.** State honestly what remains: the workshop, a real `decision_log_ref`,
the joint C-BLOCK-15 opening with Fahmi, and a non-author reviewer.

---

## Decisions you must be able to defend in your own reasoning
(if you can't yet explain one from scratch, that's the section to slow down on)

1. One staff-complete envelope + derived projection **vs** two hand-maintained schemas.
2. Fail-closed projection (unlisted field → dropped) **vs** allow-by-default.
3. Disclosure *classes* on fields **vs** ad-hoc "hide this in the template".
4. `L_reliance` bound to the terminal decision **vs** to displayed evidence (CA-1).
5. Semantic replay via digest **vs** trusting the public HTML.

## Wording guardrails (from WP §19)
- Never write, unqualified: *safe, secure, private, compliant, accessible, first, novel,
  production-ready, trustworthy*.
- Use instead: *projection / derived / evaluated toward / candidate / PROPOSED / research
  demonstration*.
- The interface may **remove** detail; it may never **add** certainty. Keep that framing.

## Done-checklist for your authored §
- [ ] Every paragraph is your phrasing, not the scaffold's, and you can explain each sentence.
- [ ] Each major choice states the **rejected alternative** and why it loses *here*.
- [ ] No prohibited wording; claims sit inside the boundary.
- [ ] Authorship notice updated to reflect that you now authored it.
- [ ] Sent to a non-author reviewer (Michael for semantics) — recorded, not assumed.

---

*When you've drafted it, send it back. I'll check it covers the substance, flag anything that drifts
over the claim boundary, and tell you where it stops sounding like your portfolio voice — without
putting words in your mouth.*
