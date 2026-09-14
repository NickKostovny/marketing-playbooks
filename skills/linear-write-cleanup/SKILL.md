---
name: linear-write-cleanup
description: De-bloat pass on any text Claude writes into Linear — issue titles and descriptions, comments, project and initiative descriptions, documents, status updates — run before the write lands, by whatever path it takes. Fires even if Nick does not say humanize or clean up. Not for reading Linear, not for external copy (content-proportion-check), not for text Nick pastes to submit verbatim.
---

# Linear Write Cleanup

The last gate before Claude-authored text lands in Linear. It is the *internal* sibling of an external humanizing pass — same enemy, different success metric.

## The one idea that changes everything here

The external humanizing prompt optimizes for **invisible voice**: make the text pass as human, because reading as AI is a credibility cost in front of scientists.

A Linear ticket has no such audience. Nobody runs a Turing test on a ticket. The cost of AI-written Linear content is not "it sounds robotic" — it is **bloat**: the reader has to wade through preamble and padding to find the actual ask. So the success metric internally is **density and scannability**, not human voice.

This has two consequences that make this skill diverge from the external pass:

1. **Keep structure.** Numbered acceptance criteria, bulleted repro steps, a Context / Task / Done-when shape — these make a ticket scannable. The external pass strips signposting to make prose flow; here, do the opposite. Never flatten a list into a paragraph to make it "read human."
2. **Do not add voice.** No fragments-for-rhythm, no personality, no casual filler. A ticket wants clarity, not a narrator. Adding voice is itself a new tell and makes the ticket worse.

So: cut the bloat, protect the structure, add nothing.

## When to run

Run this pass immediately before the text becomes a Linear record — **whatever path the write takes.**
Do not gate on tool names. Whatever path a Linear write takes — MCP tool, API call, or script — this pass runs first.

The test is the action, not the API: text is about to land in Linear → clean it first, then write.


This applies to **Claude-authored** content — the common case where Claude drafts a ticket, comment,
or update from a conversation or a Cowork task.

## When NOT to run

- **Reading** Linear — queries, lookups, listing issues. No write, no pass.
- **External-facing** copy — LinkedIn, landing pages, blog, email to a prospect. That is content-proportion-check + the external humanizing pass, not this.
- **Verbatim paste** — if Nick pastes text and says "put exactly this in the ticket," submit it as-is. Do not edit his words.
- **Scope honesty:** this only governs text Claude writes, at the moment Claude writes it. It cannot clean a teammate's Cowork session that does not load this skill, hand-typed UI tickets, or the existing backlog. Do not imply broader coverage than that.

## The cleanup pass

Preserve meaning, claims, identifiers, and structure. Cut the following:

- **Preamble / framing throat-clears** — "This task involves," "The goal of this ticket is to," "In order to," "This PR aims to," "The purpose of this issue is." Open with the actual ask, in the imperative: "Add CPV report export," not "This ticket involves adding the ability to export CPV reports."
- **Rule-of-three padding** — three adjectives, three bullets, three examples when the work has one or five. List only the real items.
- **Hedge-stacked acceptance criteria** — "should ideally," "could potentially," "may want to consider." A criterion is a commitment: assert it. "Export returns a valid CSV," not "the export should ideally return something resembling a valid CSV."
- **Restating closers** — "In summary," "Ultimately, this will," "To wrap up." End on the last real point.
- **Filler words** — leverage, robust, seamless, crucial, utilize, facilitate, streamline, comprehensive, holistic, delve, foster, elevate, underscore, landscape, realm. Use the plain word; do not thesaurus to another stilted one.
- **Empty quantifiers** — "a number of," "various," "several different," "a wide range of" when a count or the plain plural will do.

Lower priority internally (fix only when it is also padding, do not go out of your way):

- **Clip-negation cadence** ("It isn't a UI bug. It's a data issue.") — internally this is a density problem, not a passing-as-human problem. If it pads, collapse it ("Data issue, not UI: ..."). If it is the clearest way to state a real fork, leave it. This is the high-signal tell *externally*; here it barely matters.

## What to leave alone

- **Structure** — lists, headings, the ticket's Context/Task/Done-when shape. Protect it.
- **Technical terms and identifiers** — A280, pool UV cutoff, CPV, PPQ, endpoint names, file paths, ticket IDs (INV-123), code blocks, error strings, URLs. Never reword these.
- **Anything already concrete and tight.** If a line is already specific, do not touch it. Over-editing tight text is its own failure mode.

## Output

Replace the draft with the cleaned version, then issue the write. Do not narrate the pass to Nick unless he asks — it runs silently as part of writing to Linear. If a draft is already clean, say so briefly and write it unchanged rather than inventing edits.

## Examples

**Example 1 — issue description (preamble + padding + filler)**

Before:
> This task involves implementing a robust solution for CPV report export. The goal of this ticket is to enable users to seamlessly export their report data. In order to accomplish this, we will need to leverage the existing API and do a number of things: build the export endpoint, add the UI button, and write comprehensive tests.

After:
> Add CPV report export. Users need to export report data as CSV.
>
> - Build the export endpoint
> - Add the UI button
> - Tests

**Example 2 — comment (clip-negation as padding → collapse, keep the fact)**

Before:
> This isn't a UI bug. It's a data issue. The A280 values aren't rendering because the upstream pipeline drops them before the component ever receives them.

After:
> Data issue, not UI: the A280 values aren't rendering because the upstream pipeline drops them before the component receives them.

**Example 3 — protect structure (do NOT do this)**

Before (acceptance criteria as a list):
> Done when:
> 1. Export returns a valid CSV with all report columns.
> 2. Empty reports return a 422 with a clear message.
> 3. The button is disabled while the export is running.

Wrong "humanized" output — flattening the list into prose to make it sound human:
> This will be done when the export returns a valid CSV with all the report columns, and when empty reports return a clear error, and once the button is appropriately disabled during the export process.

The list is correct as-is. Tighten individual lines if needed, but keep the numbered structure — it is what makes the criteria checkable.

## If Nick wants the existing backlog cleaned

That is a separate batch job, not this skill, and it carries a consent issue: rewriting tickets other people wrote changes their words. Do not bulk-rewrite the team's tickets silently. Surface it as an explicit, opt-in task scoped to his own tickets, and confirm before writing anything back.

## Before writing

Check that the cleaned text still contains every identifier, number, and list item the draft had. This pass only removes padding; losing a fact is a failure, not a tightening.
