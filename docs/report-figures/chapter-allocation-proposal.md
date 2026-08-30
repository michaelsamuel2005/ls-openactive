# Report structure — proposal for the meeting (Clarence)

**Against:** Michael's skeleton `ClosingTheActivityGap_group_mscthesis_SKELETON_v0_1`
**Position:** adopt the skeleton; amend one chapter split. **Status:** proposal, team ratifies.

---

## 1. Adopt the skeleton

It is a clean build of the official template and it removes every defect in the current
`SEMT0044_Group41_Report (6)`: the title page and Declaration there still read *Daniel Page* with the
template's placeholder title; the Abstract and Supporting Technologies (both compulsory) are still
instruction text; *Summary of Changes* (resubmissions only) and the *Prelude* guidance page are still
present; and the Lists of Algorithms and Listings are empty. The skeleton has none of these. Adopting
it is the single highest-value structural decision available, and it should be uncontroversial.

---

## 2. The amendment: one chapter per stream

The skeleton allocates a chapter to each stream except one:

| Stream | Skeleton allocation |
|--------|--------------------|
| Wesley — data acquisition, integrity, provenance | **Chapter 3** (3 sections) |
| Michael — reconstruction and the evidence engine | **Chapter 4** (4 sections) |
| Fahmi — corpus characterisation, equity analysis | **Ch 5.1, 5.2**, and leads Ch 6 |
| **Clarence — applications and application assurance** | **§5.3 only** |

§5.3 as drafted has to carry: two applications, the C-BLOCK-05 contract and disclosure model, the
independent certificate checker, eight executable release invariants, a fifteen-claim executable
assurance case, the accessibility evaluation, and the frozen evaluation instruments. That is
chapter-sized material, and it is the part of the project carrying the strongest external evidence —
three independent reviews, roughly eighteen defects found and dispositioned, each fix landed with the
adversarial test that would have caught it.

**Proposed amendment.** Split the skeleton's Chapter 5 so that each stream owns one chapter:

- **Ch 5 — Analysis and Provision Insight** (Fahmi): 5.1 corpus characterisation, 5.2 equity-aware
  provision analysis.
- **Ch 6 — Discovery Applications and Application Assurance** (Clarence), new:
  - 6.1 Two surfaces over one certified decision contract *(Figure: two-projection architecture)*
  - 6.2 Disclosure classes and fail-closed projection *(Table: disclosure classes)*
  - 6.3 Independent verification: the certificate checker *(Table: injected defects → rejection codes)*
  - 6.4 Release-blocking invariants and the executable assurance case *(Tables: invariants; 15 claims)*
  - 6.5 Presentation conditions P0/P1/P2 and the conversational route
  - 6.6 Accessibility and inclusive interaction
- Chapters 6 and 7 become 7 (Critical Evaluation) and 8 (Conclusions).

**Page budget:** 4 pages for Ch 6, the same as Ch 3 and Ch 4. This is a redistribution inside the
30-page limit, not an increase — the figure and five tables already exist, compile, and are currently
carried in the old report.

**Fallback if the team prefers to keep six chapters:** §5.3 expands to 5.3.1–5.3.6 as above with a
named 4-page budget, plus a dedicated Clarence subsection in the Critical Evaluation chapter.

---

## 3. Contribution to the Critical Evaluation chapter

Whichever split is adopted, the applications stream contributes its own evaluation section, per the
skeleton's rule that every stream evaluates itself:

- what the executable gates demonstrate, and what they do not;
- the falsification conditions declared in advance, and the result against each;
- the disclosure defect found in review, reclassified, and closed with a regression test — reported
  openly, because a control that can fail is evidence that the case is capable of failing;
- the honest maturity position: evidence green, human authorisation outstanding, and why an assurance
  dashboard that reported "not yet reviewed" as "authorised" would commit exactly the error the
  applications are built to prevent;
- named limits: accessibility evaluated *toward* WCAG 2.2 AA within a tested matrix rather than
  conformance; the role gate a demonstration stub, not production IAM; the parser deterministic and
  standing in for a language model behind the same contract.

---

## 4. Two template rules that bind the whole team

- No font, spacing or margin changes to fit the 30 pages — exceeding the limit is a mark penalty.
- The class file must be renamed to `dissertation.cls` (it downloads as `dissertation(1).cls`).

---

## 5. Dates

All three components — group report (60), individual reflective accounts (20), presentation (20) —
are due **Thursday 18 September, 13:00 (GMT+1)**; the working deadline is the evening of the 17th.
Chapter drafts to Dalila and Alex by **8–10 September**, per Ayush's warning that late full drafts get
little or no feedback. Presentation delivered **Monday 22 September, 11:00**, with the deck assumed
due on the 18th until confirmed otherwise.
