# Shipping a webinar landing page: "Reengineering the economics of autologous cell therapy"

**Live:** a hidden, noindex page on the company site, linked from LinkedIn posts and an email. A public mock of the same page on a personal Vercel project came first.
**Shipped:** October 15, 2026. All of it in one day: brief in the morning, five production merges by late afternoon. One design handoff and eleven rounds of owner feedback in between.
**Type:** A registration page for a trade-publication panel the company sits on. Four speakers, one register button, one product demo. The panel is hosted and gated by the publication, so the page's only job is to get a reader to click through and register.

## The brief

A trade publication is hosting a one-hour panel on why autologous cell therapies stay expensive at scale. Our Head of Product is one of four speakers, alongside a customer's site head and two vendors. I asked for the whole campaign kit: landing page, speaker graphic copy, three LinkedIn posts, a first-person post for our speaker, and an email. Then: build the page on the same design as our QuickStart mock, give me a public link, and merge it when it is right.

Two constraints from the brief that shaped everything: use only the proof I supply (no invented numbers, quotes, or dates), and never imply that the vendors on the panel endorse us.

## Step 1. Read the listing, not the brief

The brief had the publication's working title, "TBD" for one vendor's speakers, and no date. The publication's listing had the real title, the date, the length, and three of the four speakers with bios. The listing is Cloudflare-walled, so the in-app browser and a plain fetch both failed. Reading it through the owner's signed-in browser worked.

The page was built from the listing, and the brief's placeholders stayed placeholders in the copy document until the fourth speaker arrived from the owner late in the day. The copy kit is in [`checklists/copy-kit-placeholders.md`](checklists/copy-kit-placeholders.md): what was supplied, what was bracketed, and what the brackets were replaced with.

## Step 2. Model it on the QuickStart mock, then cut it

The first page was a copy of our QuickStart landing mock: header, hero with the panel beside it, a "what you'll learn" row, a point-of-view band, bios, a closing band, a footer. It went up on a public Vercel alias within the hour.

The owner then came back with a Claude Design handoff that cut it to two sections. The handoff's argument, which I agree with: a reader decides in seconds whether to register, so the page answers what, when, how long, what it costs, who is speaking, and gives one obvious button. Everything else was a reason to scroll past the button. The cut table, with the reason for each cut, is in [`checklists/webinar-page-cut.md`](checklists/webinar-page-cut.md).

The handoff was a Claude Design source file, not drop-in code. See Step 4.

## Step 3. Fill the white space with product, not more copy

Two sections left a lot of ground. The owner wanted it filled with something that supplements the panel's thesis and shows what we do, "understated, but nice." Three things went in, each from an existing asset:

- **The homepage Assist demo**, isolated and embedded as an iframe that starts when scrolled into view. We already had a demo on an autologous CAR-T dataset: 25 simulated patient lots, near-identical growth curves, wide swings in transduction efficiency, and the one timing step that separates them. It fit the panel's topic exactly, so it shipped in the time a new demo would have taken to brief. A cost-per-dose demo was drafted as the better fit and parked.
- **A rotating wireframe cell** from our cell therapy solutions page, ported from a React canvas component to plain JavaScript so the static mock could run it. It sits in the hero's right column under the register card, hidden on phones, paused off-screen.
- **Two partner logos** in the header at 70 percent opacity, in place of the text label "A [publication] webinar." The owner supplied white logos on a navy image. A small script turned luminance into alpha and recoloured them to the page ink, so they sit on a light header with no box. The script is [`tools/recolour-logos.py`](tools/recolour-logos.py).

A "Book a demo" button went under the demo section's lead, with campaign UTMs so bookings from this page are attributable.

## Step 4. The design-system back-and-forth

This page passed through four design contexts in one day, and the handoffs between them are where the time went. Writing them down so the next page skips the detours.

| From | To | What broke, and the fix |
| --- | --- | --- |
| **QuickStart mock** (standalone HTML on design system v2: a light ground, 1px lines, no lifts, no eyebrows) | **First webinar page** | Nothing broke. Copying the mock's stylesheet and swapping content took minutes. This is the argument for keeping one standalone mock per design system as the seed for the next. |
| **Claude Design handoff** (`.dc.html`: a custom element wrapper, template holes, a loop tag, speaker data in a class method, inline styles everywhere) | **Standalone page** | The handoff is a spec, not code. I read the layout, spacing and colours out of the inline styles into named classes on the same tokens, and moved the speaker data into plain markup. The handoff used a text placeholder for the wordmark and grey squares for photos; the real wordmark SVG and headshots replaced them. |
| **Solutions page** (a React client component drawing on a canvas, composed for a hero slot at 78 percent of the width) | **Standalone page** | The component imports composition helpers and React hooks. The port kept the geometry, seeds and opacities byte for byte and replaced only the composition (centre of its host, 94 percent of the shorter side) and the lifecycle (a resize observer, an intersection observer to pause off-screen). |
| **Standalone page** (its own stylesheet, nothing else on the page) | **Site repo** (Next.js app, one global stylesheet that styles elements, two earlier campaign pages that each carry a scoped block) | Three real problems. (1) The global stylesheet sets colour and weight on `a`, `h1`, `p`, so the scoped rules needed `!important` on leads and labels, and the button's white label lost to `.fw a` on specificity until the rule became `.fw a.fw-button`. (2) The canvas went back to being a React component, a copy of the original with the composition change, wrapped in a client-only dynamic import so it never server-renders. (3) The demo iframe became a client component with the scroll trigger in an effect and a touch shield for iOS Safari, both lifted from the previous campaign page. |

The pattern that held across all four: tokens first, components second. Every context used the same six colours and the same 1px line. What changed was how the rules reached the elements. The recipe is [`recipes/design-system-handoffs.md`](recipes/design-system-handoffs.md).

## Step 5. The owner's review, eleven rounds

Every round was a sentence or two in chat and shipped within minutes. In order:

1. Reuse the CAR-T demo, not a new one, to fill the white space.
2. Panel above the demo. Cut section padding 30 percent.
3. Add a Book a demo button under the demo text.
4. Two partner logos in the header, 70 percent transparent, evenly spaced with the wordmark.
5. A moving diagram from the solutions pages, "understated, but nice."
6. Cut padding another 15 percent so the speakers' faces show on landing.
7. The demo heading in plain English. "Every lot is a different patient. Assist reads them as one dataset." became "Every autologous batch starts from a different patient's cells. Assist still lines them up and compares them."
8. Bios as the publication lists them, not one-line topics.
9. Nothing under "On the panel" but the photos.
10. Company above title on each card, so the cards level across different title lengths.
11. The publication's own one-sentence description of the panel as the hero lead.

Round 6 is the one worth copying. "Faces above the fold" is a measurable target. The photo top was at 856px on a 900px viewport after the padding cut; trimming the figure slot, the card padding and the facts gap brought it to 784px. A number settles a layout argument faster than a screenshot.

After the merge, three more rounds came as production PRs: drop "free" from the length fact because the button already says it, new copy for the demo section from the owner, and the fourth speaker.

## Step 6. Posts, in the organiser's shape

The publication's sponsor (our customer) had already posted its own announcement. The owner asked for ours to be "pretty similar." Our announcement now opens on the same observation, that programs learn their real cost after the process is locked, names the four speakers with LinkedIn tags, and lists the same four topics. Three posts are staged in the scheduling tool with non-blocking review requests to our speaker and the sales lead: the announcement, a week-before post with one line per speaker, and a day-before reminder. The link goes in the first comment, never the body. The three posts, sanitized, are in [`prompts/three-webinar-posts.md`](prompts/three-webinar-posts.md).

Two of the four speakers' LinkedIn handles did not resolve from a web search, which refuses to look up named people. A people search in the owner's signed-in browser found them in one pass.

## Step 7. Ship

Five squash merges to the site's main branch in one afternoon, each on a fresh branch off the remote main. The loop that made it cheap: push, open the PR with an explicit head branch, run a background loop on the PR's checks until the deploy check leaves "pending," merge when it passes, then a second loop that polls production until the change is served. Recipe: [`recipes/merge-when-the-deploy-passes.md`](recipes/merge-when-the-deploy-passes.md).

Three things that cost time once and are now written down:

- The site builds with Turbopack, which refuses a symlinked `node_modules` in a git worktree. A copy-on-write clone of the folder (`cp -c -R` on APFS) takes seconds and works.
- A worktree cut from the remote main tracks it until the first `git push -u`, and the GitHub CLI refuses to open a PR from a branch whose upstream is main. Pass `--head`.
- The deploy check passed before the AI code review did on every PR. The review is advisory. Merging on the deploy check alone is the rule here.

## Results so far

**Outcome line:** No outcome record yet. Registrations happen on the publication's platform, so we will see a count only when it sends the registrant list after the panel. What is countable from October 15: clicks on the register and Book a demo buttons through the site's CTA event, and demo bookings through the meetings link's campaign tag. First read on October 28, the day after the panel.

Inputs as of ship, all from tool output:

| Measure | Value |
| --- | --- |
| Production merges | 5 |
| Owner feedback rounds before the first merge | 11 |
| Speaker cards | 4, one written from a public profile because the listing lacked it |
| Posts staged | 3, none published at the time of writing |
| Page sections | 3, down from 8 |

## What I would do differently

- **Start from the listing.** The first hour went into a long page built from the brief, which the listing then contradicted on the title and the brief's cut sheet then removed. Read the listing first, build the two-section page first, and treat everything else as a candidate for the white space.
- **Wire the outcome before the first post.** The register button goes to the publication, so we only learn the count when they share it. A short redirect on our domain in front of the registration link would have counted clicks by source from day one, and the posts could have carried per-post links. That is the revenue item: this page's only outcome is registrations and the demos they turn into, and the first of those is not ours to count yet.
- **Keep the mock.** The public Vercel alias stayed the fastest review loop all day, before and after the site merge. Two copies of a page is a cost, but a review link that needs no login and redeploys in twenty seconds paid for it eleven times.
