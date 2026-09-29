# Shipping a statistics explainer: "What is Cpk, and how do biologics teams use it?"

**Live:** https://invertbio.com/blog/what-is-cpk-process-capability
**Shipped:** September 29, 2026. The keyword pick came out of a SERP softness map on September 28. Four review gates between the first draft and the merge.
**Type:** Long-form definitional explainer written to capture a search cluster, grounded in a statistics handbook and the regulator's own text, with the product's limit stated plainly.

## The brief

I did not start from a topic. I started from a question: of the non-brand keywords around our product, where could a strong page actually enter Google's top ten? A SERP softness map answered it for 91 keywords, and the Cpk group came out as one of the best bets. The brief to Claude Code was to write the concept explainer for that cluster, biologics-first, with every claim sourced.

## Step 1. Find the gap, and size it honestly

A difficulty score says how many links the ranking pages have. It does not say whether those pages answer my reader. The softness map counts, for each keyword, how many of the ten organic slots a strong page from our site could take. A regulator or an encyclopedia holds its slot. A forum thread, a thin glossary, or a page written for another industry probably does not. Recipe in [`recipes/serp-softness.md`](recipes/serp-softness.md).

For the Cpk group, 5 to 10 of the 10 slots were open, and none of the top pages covered biologics. The demand is generic quality-statistics vocabulary:

| Query | Monthly volume (US) | Difficulty |
| --- | --- | --- |
| what is cpk | 2,400 | 5 |
| cpk formula / cpk calculation | 1,900 | 0 |
| cpk vs ppk | 1,300 | 0 |
| process capability cpk | 1,000 | 5 |
| cpk meaning | 880 | 0 |
| process capability | 720 | 12 |
| how to calculate cpk | 390 | 0 |
| cpk calculator | 320 | 0 |
| what is a good cpk | 110 | 0 |

**Decision:** one definitional page that holds the whole group, with a heading for each variant (the formula, a worked example, Cp, Cpk, Pp and Ppk, Cpk vs Ppk, how to run the analysis, what a good Cpk is) and an FAQ for the long tail (what a Cpk of 1.33 means, whether it can be negative, how many batches you need, the Excel formula). The part no ranking page had: why capability is harder to read for biologics, and where it shows up in process validation.

## Step 2. Ground every claim

Every factual sentence got a row in a claim audit table before any review ran: a type, a source, an exact locator, whether I fetched the source again, a grade, and a disposition. Template and prompt in [`prompts/claim-audit-table.md`](prompts/claim-audit-table.md).

- **Statistics and thresholds:** the NIST/SEMATECH e-Handbook, section 6.1.6, for the definitions, the sample-size minimum, and the per-million table. Minitab's blog for Cpk vs Ppk. Steiner, Abraham, and MacKay for where the 1.33 and 1.67 thresholds come from: automotive supplier practice (AIAG), not pharmaceutical regulation.
- **Regulation and practice:** the FDA's 2011 process validation guidance, which asks for statistical trending and an evaluation of capability but names no Cpk index and no threshold. ISPE's *Pharmaceutical Engineering* (2020) and a BioProcess International CMC forum (2017) for how continued process verification uses capability.
- **Not cited:** two professional-body pages returned HTTP 403. I could not open them, so they are not in the post, even where I thought I knew what they said.
- **Product claims:** checked against the company's internal product knowledge base. The post says plainly that there is no built-in Cpk index today, and that the AI analyst writes the calculation as Python code in each chat.
- **Customer voice:** none. A search of the sales-call corpus found no call that mentioned Cpk. The calls did support the framing (capability trending in process verification, and spreadsheets as the workaround), so the framing stayed and no quote went in.

This step caught one thing too late. The first outline assumed a built-in capability feature. The product check came after the outline, and the feature does not exist. The section was rebuilt around what does.

## Step 3. Draft and render

The blog pipeline renders markdown without table support, so the three tables are raw HTML, each in its own horizontal scroll frame. The formulas are an HTML block with real subscripts, and it scrolls inside itself on a narrow screen instead of wrapping mid-formula. The worked example has an inline SVG figure: one distribution between two limits, with the nearer gap marked. The numbers in it are labeled illustrative.

Drafts rendered through the real blog pipeline on a local dev server, in an isolated git worktree cut from the remote main branch.

## Step 4. Four review gates

Four gates ran on the draft. The cold read ran in a fresh agent that had not seen the drafting session.

- A **defensibility check**: could I defend each sentence to the reader who knows the subject best? ([skill](../skills/defensibility-check/))
- A **zero-context cold read** by a persona fluent in the statistics who had never heard of the company, with the **read-aloud grader** alongside it. Same prompts as the [OPC UA entry](../2026-09-opc-ua-explainer/prompts/). ([skill](../skills/blog-cold-read/))
- A **claim-proportion check**: is each claim the size its evidence supports, and is practitioner language sourced? ([skill](../skills/content-proportion-check/))
- A **brand review** for voice and terminology.

All four said REVISE. None said HOLD.

## Step 5. Preview

The branch was pushed without a pull request, so Vercel built a preview and the review happened there before anyone asked for a merge. Previews on this team sit behind single sign-on; the share-link route is in the OPC UA entry's [preview recipe](../2026-09-opc-ua-explainer/recipes/preview-and-share.md).

## Step 6. The finding that changed it

The cold read returned one blocking FAIL, and it was right. The draft said Cpk describes the process "when nothing changes between batches."

That is wrong for a biologics reader. With one result per batch, the within-subgroup standard deviation is estimated from the moving range between consecutive batches. Batch-to-batch noise is in it. What it changes little with is slow drift and sustained shifts, and that gap is what Ppk picks up. The line now reads: "With one result per batch, it is usually estimated from the moving range between consecutive batches, so it captures batch-to-batch noise and changes little with slow drift or sustained shifts." Re-checked, passed. The read-aloud grader's verdict on the revision: SOUNDS HUMAN.

A quality engineer who computes Cpk every week would have stopped reading at the original sentence. Nobody who does not compute it would have noticed.

The other fixes from the four gates:

1. **Name the sigma in every formula.** Within-subgroup for Cp and Cpk, overall for Pp and Ppk, stated next to the formulas.
2. **Pp and Ppk also assume normal data.** The draft only warned about Cpk.
3. **One-sided limits, for both families.** Ppu and Ppl now sit beside Cpu and Cpl.
4. **An Excel example with 100 values, not 39.** Thirty-nine is under the minimum the post had just given. The example also says that `STDEV.S` gives Ppk, not Cpk.
5. **No unsourced "many sites" claims.** Each one was sourced or cut.

The checklist that came out of this is in [`checklists/statistics-explainer.md`](checklists/statistics-explainer.md).

## Step 7. Late changes and the card

I rewrote the product-limit line myself. It now reads: "Assist writes the calculation as Python code in each chat, which you can review." It follows a plain "Invert does not compute Cpk as a built-in index today."

The blog index needed a card image, so the same builder style as the OPC UA card made one: 1600 by 1000, white ground, three short lines of copy, one distribution between two dashed limits. The mean sits off center, and only the nearer gap gets the accent color. The geometry is a real Cpk (Cpu 1.09, Cpl 2.05), so the picture makes the same point as the post. Generic version in [`tools/thumb-builder/`](tools/thumb-builder/), shipped card in [`assets/thumbnail.png`](assets/thumbnail.png).

## Step 8. Ship

Pull request opened after the preview review, merged. Production verified with a plain fetch: HTTP 200, the canonical URL points at itself, and the robots meta says index, follow. The live URL went into the SEO project context as a key page with its target terms, so the first ranking check has a baseline.

## Results so far

Too early. Live on September 29, 2026, with a ranking baseline of zero. First check in December 2026, on "what is cpk," "cpk formula," "cpk vs ppk," "process capability cpk," and "cpk meaning."

## What I would do differently

- Check the product source of truth before outlining, not after. The first outline assumed a built-in capability feature that does not exist, and a section had to be rebuilt around what does.
- Fetch every results page two or three times from the start. One fetch can come back from the wrong locale or for another meaning of the words, and I had to fetch again to get counts I could trust.
