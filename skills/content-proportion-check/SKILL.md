---
name: content-proportion-check
description: "Editorial gate on any marketing content representing Invert to bioprocessing practitioners and the leaders who fund their tools — blog posts, LinkedIn, landing pages, ads, email, one-pagers, case studies, scripts. Fires on \"review this,\" \"draft a post,\" \"here's the copy,\" \"help me write,\" or when Nick reviews others' content. Owns claim proportion and whether practitioner language is sourced. Prose mechanics belong to writing-craft; category-level positioning to Nick."
---

# Content Proportion Check

**These are current decisions, not permanent ones (as of September 2026).** Nick's read of the market moves, so treat every claim below as falsifiable against
transcripts rather than as a rail. If call evidence contradicts something here — practitioners describing
Invert in platform terms, or a CDMO buying scientific reach rather than throughput — say so and propose
the edit. Silently applying a stale positioning decision is the failure mode this note exists to prevent.

## Step 0 — name the cell

Proportion depends on who the piece is for and what job it does. Before grading, state the cell. The full
matrix and persona definitions live in `brand-marketing-framework`; this is the routing summary:

| Layer | Proof (Invert on screen) | Perspective (no Invert pitch) |
|---|---|---|
| **Scientist** — the IC who runs the workflow | "How to do X in Invert." Pain hook with a number → clip. The daily asset. | Open question. |
| **Program leadership** — director owning a molecule's development | Lifecycle phase today vs. with Invert. | Open question. |
| **Digital** — owns infrastructure + AI budget across the business | The governed-AI stack: harness, skills, evals, validatable outputs, provenance, permissions, Bedrock. | Observational series on change management and adoption. No pitch. |

If the piece is for IT or procurement, stop — not a target. If the cell cannot be named, return that
before anything else.

## The positioning this rests on

**At the scientist layer, Invert is a scientific instrument.** Not a software platform, not an AI tool,
not a partner. An instrument — like a microscope or a chromatography system — that earns its place by being transparent,
reproducible, and subordinate to the science. Practitioners cite it in methods, present findings made
*with* it rather than *about* it, and judge it by what it lets them see.

**At the digital layer, Invert is the governed AI vendor for process development** that has already done
the hard, complete work. "AI" and "vendor" are allowed words there. "Platform," "transformative," and
feature lists with no story around them are still not.

**The transformation differs by segment, inside any layer.** Picking the wrong one fails harder than using
the wrong words for the right one:

- **CDMOs** buy operational leverage — throughput, fewer hours wrangling data, faster reporting cycles.
- **Development teams** buy scientific reach — seeing things they couldn't see, surfacing findings they
  weren't looking for.

**The exemplar for perspective and case studies: the customer slide.** All data, all results, one mention of
the tool. The scientist is the protagonist, the finding is the story, Invert is in the methods section.

**The exemplar for proof: the pain-hook video.** "Making this report takes our users six weeks without
Invert. Here's two minutes in Invert." Then the clip. The pain is the scientist's; the clip shows the
instrument doing the step.

## Four failure modes

1. **Hype inflation** — revolution/paradigm/transformative language; technology as protagonist; claims
   about the industry's future instead of a concrete present-tense change. Correction: shrink the claim
   to the demonstrable improvement. Name the workflow step that changes and what stays the same. At the
   digital layer, "we've done it already and it's hard" is the honest ceiling; "we transform pharma" is
   over it.
2. **Déjà vu** — could be said by any bioprocessing vendor with minor word changes. **Substitution test:**
   swap in a competitor's name. If it still reads, it's generic. Add specificity until the test fails.
   Digital-layer version: SSO, identity, SOC 2, "runs on Bedrock" stated alone read as any enterprise
   SaaS. They pass only as parts of the stack story.
3. **Timidity** — hedging that hides real value. Scientists don't distrust claims, they distrust
   *unsupported* ones. State it, support it, let them evaluate.
4. **Wrong shape for the cell.**
   - *Perspective and case studies:* "Invert" appears more than the practitioner's work; the arc is
     problem → Invert → solution rather than practitioner's work → finding → (Invert in how they got
     there). **Instrument test:** would a lab-equipment manufacturer describe it this way?
   - *Proof:* the arc is supposed to be pain → Invert. The failures are different: the hook is about
     Invert instead of the reader's week; the number in the hook is not defensible; the clip does not
     show the real product; a product post does not link to the trial; or a proof post is dressed as
     perspective (opens as observation, pivots to demo).

For CDMO audiences the "finding" may be operational (more programs through the same facility) rather than
scientific. The instrument framing still holds; the emphasis shifts.

## The language gate — verify, don't flag

Every claim about practitioner workflows, pain points, or mental models must trace to something a
practitioner actually said. Factual product descriptions and general industry context are exempt.
**Hook numbers are claims** — "six weeks" needs a source or an Inferred label like any other line.

**Do not just grade these — go source them.** For each practitioner claim, run `search_calls`, then
`get_call_transcript` on the best matches, and attach the verbatim quote. Only report claims that survive
the search with nothing behind them. For digital-layer claims, calls with scientists are the wrong
corpus; the source is what digital leaders themselves say (their LinkedIn posts, digital-side calls), and
a claim with no such source is Inferred at best.

- **Sourced** — traceable to observed practitioner language (transcripts, job postings, interviews).
  Example: a posting says "manage tech transfer documentation across multiple manufacturing sites" →
  using "tech transfer documentation" as a pain framing is Sourced. Confident claims allowed.
- **Inferred** — the pain point is grounded but the phrasing is synthesis. Acceptable in published content;
  note it. **Briefs hold a stricter bar** — see `idea-to-brief`, where an Inferred claim passes only if it
  is labeled as Inferred in the brief itself, because everything built downstream inherits it unchecked.
- **Invented** — no grounding. Either source it, cut it, or label it a hypothesis. Never ship as Sourced.

The dangerous case is Invented language that *sounds* authentic, because I'm good at mimicking domain
register. Precise-sounding workflow descriptions and plausible pain points are the tell. The test:
**can you point to the source?**

## Before returning

Return only what's wrong, ordered by cost to fix. Did you name the cell and grade against that cell's
shape, not all of them? Can you point to a source for every practitioner claim you let stand? If a claim
is Invented and you didn't search, you skipped the gate.