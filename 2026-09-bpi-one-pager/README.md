# Rebuilding a conference one-pager: "Governed data and AI for process science"

**Live:** a printed, two-sided Letter leave-behind for a bioprocess trade show. There is no URL. It is handed over at the booth.
**Built:** September 21, 2026. Print-shop files prepared September 22. One team design thread in between.
**Type:** A two-sided sales handout. It was the first asset built on a new design system, so it was also the test case for that system.

## The brief

We already had a one-pager for the show. It was exported from a PDF library, and it had most of the patterns that make marketing look machine-made: a dark hero, monospaced all-caps eyebrows with accent rules, "01 / 02 / 03" ornaments, a stat strip, icon tiles, and watermark geometry.

At the same time, a team Slack thread had listed what people disliked about our current look: the off-white ground, the italic or contrast word in headlines, mono all-caps eyebrows, pills, and numbered lists. I owned the answer. So the brief to Claude Code had two parts: build a second version of the design system with those patterns removed, then rebuild the one-pager on it. If the system could not produce a better handout, the system was wrong.

## Step 1. Audit what to remove, one pattern at a time

I did not want "make it cleaner." I wanted a list where every removed pattern has a named replacement, so the next asset does not bring the pattern back.

| v1 pattern | Why it goes | v2 replacement |
| --- | --- | --- |
| Dark hero over the whole top third | Heavy ink, and it reads as a template | White page. The headline carries the top. |
| Mono all-caps eyebrow with an accent rule | The most common AI-design tell | 13px sentence-case section label in secondary ink |
| "01 / 02 / 03" on the how-it-works columns | Decoration. The order is not the point. | Plain columns with 1px dividers. Numerals only where order matters (the pilot steps). |
| Stat strip with big numbers | Numbers without context | Each outcome is a sentence, then one line of what changed |
| Icon tiles for each product | Icons add nothing a name does not | A table: product name, one-line job |
| Source-system logo row | Logo walls are unverifiable and date fast | One sentence that names the system types |
| Quote with accent bar, glyph, and avatar | Three ornaments on one quote | The quote, a role, and a company tier. Nothing else. |
| Watermark geometry | Fills space, says nothing | Removed |
| 0.5px lines | Vanish in print and on low-DPI screens | 1px lines |

The reusable form of this table is [`checklists/one-pager-restraint.md`](checklists/one-pager-restraint.md).

## Step 2. Give each side one job

A booth handout is read in two situations: three seconds at the table, and later at a desk. I gave each side one of these.

- **Front: what it is, and proof that it works.** One headline, one supporting sentence, the product architecture, how it works in three steps, and one piece of evidence: a real product screenshot next to a practitioner quote about time saved.
- **Back: why an enterprise team can say yes, and how to start.** Four enterprise objections answered in two lines each (architecture fit, one shared process model across teams, traceability, a foundation for governed AI). Then three outcome statements from customer work. Then a small pilot in three steps, and one call to action.

The product architecture is drawn as layers, not as a feature list. Four applications sit in one row across the top. The shared scientific record and the data-connection layer sit as full-width rows under them. A reader who sees only this box should understand that the applications share one foundation. That is the core claim.

## Step 3. Keep the copy, change almost nothing

The copy had already been through review. A redesign is a bad time to rewrite messaging, because reviewers then cannot tell which change they are reacting to. I allowed only these edits:

- Joined the hero's two short sentences into one.
- Wrote "&" as "and".
- Rewrote the stats as sentences, because the stat strip was gone.
- Wrote the screenshot caption from the chart title that is visible in the screenshot, so the caption cannot claim more than the image shows.

The quote is anonymized to a role and a company tier. No customer is named anywhere on the page.

## Step 4. Render and measure, for two printers

A handout has two print paths, and each one fails differently.

**Office printer (someone prints it the night before).** The HTML version uses `@page` Letter with 0.5in margins and no background fills, so it prints the same with "Background graphics" on or off. I did not trust the print preview. Headless Chrome's `--print-to-pdf` hangs on my Mac, so a small Node script drives Chrome over the DevTools protocol, reports each sheet's rendered height, and writes Letter and A4 PDFs. A Swift PDFKit script then renders each page to PNG and dumps its text. The gates were numeric: each sheet 960px or shorter, and exactly 2 pages on both Letter and A4. The final heights were 930 and 946.

**Print shop (the real run on good stock).** This version lives in a design canvas as two artboards. It has one light tint band on the front and a dark closing band on the back. That needs a different preparation. See Step 6.

## Step 5. The review

The one-pager did not get its own review round. The design-system thread was the review: the team's list of dislikes became the audit table in Step 1, and each item was checked against it. Two calls stayed with the brand owners and are still open: whether to keep the sage tint band at all, and whether our accent orange is too close to a well-known AI brand's orange.

## Step 6. Preparing for the print shop

When I asked for a version for "nice stock paper," five problems came up. None of them show on screen.

1. **No bleed.** The dark band ran to the page edge at exactly 8.5 × 11in. A trimmed sheet then shows a white sliver where the cut drifts. Fix: new artboards at 8.75 × 11.25in (0.125in bleed on each side). All content moves in by 0.125in, so after trim it sits exactly where it did.
2. **The screenshot was 246 dpi at placed size.** The canvas held a downsized copy. The original crop was 1317px wide, which gives 333 dpi across 3.96in. I swapped it in.
3. **The hairlines were 10% transparent ink.** On screen that is a nice line. On uncoated stock it can disappear, and some print RIPs flatten transparency badly. Fix: solid hex values that give the same color.
4. **The page ground was a 3% grey tint.** On premium stock that looks like dirty paper, and a light flat tint can band on a digital press. Fix: white, so the stock is the ground.
5. **Light text on the dark band was 14px.** Small light text on a dark flood fills in on absorbent paper. Fix: 15px and a slightly lighter color. The on-page link became plain bold text, because paper has no links.

The full list, with the numbers, is [`checklists/print-preflight.md`](checklists/print-preflight.md). The procedure is [`recipes/design-canvas-to-print-shop.md`](recipes/design-canvas-to-print-shop.md).

## Still open

- **Font license.** Our typeface is licensed as a web font. A PDF sent to a printer embeds it. I have not confirmed that the license covers this.
- **A QR code.** The v1 page had none, so I did not add one. A booth QR code to the trial page exists elsewhere and could go on the back.
- **A paper proof of the dark band.** A large dark area is where uncoated stock shows problems. Ask the printer for one proof before the full run.

## Results so far

Nothing measurable yet. The handout itself has no tracking. If a QR code goes on the back, it gets its own UTM source, so booth traffic can be counted separately in analytics.

## What I would do differently

- **Get the printer's spec before the first artboard.** Stock, coated or uncoated, bleed, and file format. Adding bleed later is easy. A layout that depends on a detail the stock cannot hold is not.
- **Make the design system's line token print-safe from the start.** The transparent hairline was a system default. It was correct on screen and wrong on paper. A system meant for PDFs needs a solid line color.
- **Keep assets at 300 dpi at placed size, and record the source.** The design tool stored a smaller copy of the screenshot. I found the full-resolution file only because the build folder kept the original crop.

---

See [`tools-used.md`](tools-used.md) for every tool and its gotcha. The reusable parts are in [`checklists/`](checklists/), [`recipes/`](recipes/), [`prompts/`](prompts/), and [`tools/print-kit/`](tools/print-kit/).
