# Shipping a definitional SEO explainer: "What is OPC UA, and how do bioreactors use it?"

**Live:** https://invertbio.com/blog/what-is-opc-ua-bioreactors
**Shipped:** September 14, 2026. First draft September 8. One product-manager review in between.
**Type:** Long-form explainer written to capture a search cluster, grounded in the product's real integration list, and pointed at from a LinkedIn post.

## The brief

I had a LinkedIn post ready about how our platform connects to bioprocess equipment over OPC UA. I wanted the "learn more" link under it to land on a blog post that also filled a gap in what search engines index for us. The brief to Claude Code was one sentence: use the SEO tool to write a blog post that fills gaps in our indexing, pointing back to this LinkedIn post.

What follows is what actually happened, including the part where a colleague told me the draft would make an engineer discount our product.

## Step 1. Find the gap, and size it honestly

Before any writing, the SEO MCP (OpenSEO, which sits on DataForSEO data) answered three questions.

**Do we have anything on this topic?** No. The site named OPC UA on the integrations page and in two case studies, but ranked for nothing related. One older post mentioned it in passing. No cannibalization risk.

**What do people actually search?** The bioprocess-specific phrasing I assumed people used has no measurable volume. "OPC UA bioreactor", "Sartorius OPC UA", "bioreactor data integration": all zero. The demand is generic industrial vocabulary.

| Query | Monthly volume (US) | Difficulty |
| --- | --- | --- |
| what is opc ua | 390 | 8 |
| opc ua vs opc da (both word orders) | 420 | 0 |
| opc ua protocol | 260 | 12 |
| opc ua meaning | 170 | 13 |
| opc ua vs mqtt | 110 | 0 |
| what does opc ua stand for | 50 | 16 |

**Who ranks?** Generic automation vendors, the standards body, Wikipedia, and one Reddit thread. No bioprocess-native explainer existed. Every bioprocess-modified query carried an AI Overview, which is a second reason to write the definitive version.

**Decision:** one definitional page that holds all the variants (what it is, vs DA, vs MQTT, vs Modbus, the acronym), written biologics-first, in the format a validation-software company uses to earn most of its traffic from a small article section. Realistic target: positions 6 to 10 on the head term, top 3 on the bioprocess-modified queries.

## Step 2. Ground every product claim before writing

Product claims came from three sources, none of them memory.

- The internal product knowledge base (an MCP over our feature specs) for how ingestion works: an edge component that reads OPC UA, OPC DA, and the PI historian, rules that link streams to runs by time window, alerts on the live stream, and the honest limits (IT has to install it, instruments outside the catalog need engineering).
- The site's own integration table for which vendor speaks which protocol, and at what latency.
- A call-intelligence MCP for practitioner language. The search results carried paraphrased signals, not speech, so a subagent pulled six transcripts and returned four verbatim quotes. Two made it into the post, anonymized by role.

This step caught two things in my own LinkedIn post. One vendor I had listed under OPC UA actually exposes OPC DA. And the "about two weeks" deployment figure exists nowhere in the product documentation. I kept it as my claim and flagged it in review.

## Step 3. Draft, render, check on a phone

The blog pipeline renders markdown without table support, so the two comparison tables are raw HTML. The process diagram started as an inline SVG and became HTML and CSS boxes instead: SVG text shrinks to nothing on a 375-pixel screen, CSS boxes reflow and stack.

Every draft went through the real dev server in an isolated git worktree, then a 375-pixel viewport check: no horizontal page scroll, tables scroll inside their own frame, diagram stacks vertically.

## Step 4. Cold read by agents with no context

Two grader agents ran before I read the draft myself. Neither had seen the drafting session.

- A **cold reader** playing the target persona, fluent in bioreactors and historians, who had never heard of the company. It grades nine patterns, most of them variants of one failure: writing for a reader who already knows the product.
- A **read-aloud pass** that only judges how sentences sound spoken. It catches machine cadence, the "X, not Y" habit, and 40-word sentences.

Verdicts: REVISE with no blocking issues, and SOUNDS HUMAN. Fixes applied in one pass. Prompts are in [`prompts/`](prompts/).

## Step 5. Get a link people could open

The branch built a preview on Vercel automatically, but our previews sit behind single sign-on. The MCP could not mint a bypass link on this team. The durable route is in the dashboard: open the deployment, click Share, choose "Anyone with the link." A share link is per deployment, so it has to be recreated after each push. Recipe in [`recipes/preview-and-share.md`](recipes/preview-and-share.md).

## Step 6. The review that changed the post

A product manager with a bioprocess engineering background read the draft and said, in short: this reads as "we use OPC UA" and "versus your historian," and an engineer who looks at their historian every day will stop reading before the second paragraph.

Three changes followed.

1. **Product-centered, not protocol-centered.** The post now says we read whatever interface a system already exposes, OPC UA or otherwise, and get every signal into one place, batch-linked, live.
2. **No versus-historian posture.** The section that contrasted "the usual path" with "reading at the equipment" became a section that credits what a historian does well and locates the friction precisely: getting a complete, batch-labeled record of a run into the tool where analysis happens.
3. **Nuance an engineer will not discount.** Batch context exists in some historians (event frames, batch historians) and is often unconfigured. Compression is a setting. Every mechanism claim is hedged to what is defensible.

He also asked whether "vendor + OPC" compound keywords would be a better target. I ran it: every one has zero measured volume. Good hypothesis, wrong answer, ten minutes to settle.

The second cold read used a sharper persona: an engineer who owns a PI historian with live trends and is proud of it. The checklist that came out of this review is in [`checklists/technical-content-review.md`](checklists/technical-content-review.md).

## Step 7. Wording and the card

One late note from the company: "agent" is a loaded word here, so every "edge agent" became "edge connector." Five places, including the diagram.

The blog index needed a card image. Nothing in the image library was unused and on brand, so a small builder generated one: 1600 by 1000, the card's exact aspect ratio, white ground so it stays distinct on the card, one bioreactor glyph with three live signal traces, three short lines of copy. The builder renders through headless Chrome and writes a 400 by 250 proof so you see what the grid will actually show. Generic version in [`tools/thumb-builder/`](tools/thumb-builder/).

## Step 8. Ship

Date set to the publish day, pull request marked ready, one green check, merged. Production verified with a plain fetch: status 200, correct title, correct date, card present on the index. The live URL was recorded in the SEO project context as a key page so the December ranking check has a baseline.

## Results so far

Live on September 14, 2026. Ranking baseline is zero, by design. First check December 2026 on "what is opc ua," "opc ua vs opc da," and "opc ua vs mqtt."

## What I would do differently

- Get the domain reviewer in before the first cold read, not after. The persona for the grader should include the reviewer's objection from day one.
- Write this ship log at ship time. It took one prompt because the session held everything; a week later it would have taken a morning.
- Test the compound-keyword hypothesis on day one. It reshaped the SEO conversation and cost ten minutes.
