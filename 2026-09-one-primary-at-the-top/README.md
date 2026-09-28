# One primary at the top: a trial bar, a demo button, and who gets the nav

**Live:** every page with the site nav on https://invertbio.com
**Shipped:** September 28, 2026. A review comment came in that morning, and two changes were merged the same day.
**Type:** Top-of-page CTA decision for a site that runs a self-serve trial and sales demos at the same time. It covers a data read, a pattern check, a test-feasibility check, and a static-site build.

## The strategy in one paragraph

The top of every page had two equal dark buttons, "Try Assist free" and "Book a demo". On the homepage, a trial bar above them also advertised the trial, so the trial CTA appeared twice. A colleague's review named the problem: two buttons were both trying to be primary. The fix I shipped keeps one primary at a time. While the trial bar shows, the nav has "Book a demo", so the trial is not repeated. When a visitor closes the bar, the nav button becomes "Try Assist free", because the site already has "Book a demo" in every hero and footer. The bar now appears on every page, because visitors do not always start on the homepage, and most peer sites show their bar on inner pages too. It comes back 30 days after it is closed. Getting there took four positions in one day. The data could not settle the question, so the decision had to rest on design reasons and on what the data could and could not show.

## The brief

A colleague reviewed the trial landing work and posted two screenshots: the nav with two solid buttons, and the homepage with the bar above them. They did not like two primaries. Their suggestion was to keep the bar for the trial and not also make the trial a primary button in the nav.

I first replied: keep the bar, remove the nav trial button, and should the bar come back some time after it is closed? The colleague then added that, if the trial converts best, the primary could swap when a visitor closes the bar, and that the nav could be reserved for the campaign that converts best, because the site has many other "Book a demo" CTAs. I agreed, and then asked Claude Code to work out the design.

## Step 1. What the data said

I asked for the numbers before any option was drawn. Everything came from the product-analytics tool, the signup table and the CRM. All figures are rounded, and the counts were small throughout.

- **The nav trial button earned very little.** It was on every page for a month and got a handful of clicks from outside the company. Most of its clicks came from one device that was likely internal.
- **On clicks, the trial won.** On the homepage, trial links got about three times as many outside clickers as "Book a demo". If I argued from clicks, I would argue against my own hesitation to put the trial in the nav.
- **After the click, the picture changed.** Almost none of those clicks became completed signups. "Book a demo" opens a booking calendar, so a click can become a sales call the same day. The trial has no outcome record yet.
- **The nav was not where trial traffic came from.** Paid ads sent more than three quarters of trial-page visitors. The nav sent 5% or fewer.
- **Two blind spots.** The mobile menu's trial link sent no analytics event at all, so phone taps were invisible. The nav trial link also had no source tag, so nav signups reached the signup table with an empty Source column.
- **Analytics sees only part of the traffic.** It runs after cookie consent, and an earlier check found it sees about one visitor in five. The signup table, filled by the server, is the count of record.

**What I took from it:** clicks and outcomes point in different directions, and the outcome data is too thin to decide anything. The first job is to make every entry point countable, so that the next read means something.

## Step 2. What other sites do

Claude Code checked 21 B2B software homepages on September 28 (logged out, desktop, one snapshot each). It rendered 14 in a browser and read the class names of the other 7.

| Finding | Count |
| --- | --- |
| Sites with both a trial CTA and a demo CTA in the nav | 13 |
| Of those, sites with two equal filled buttons | 0 |
| Of those, sites where the trial CTA is the filled one | 9 (the other 4 fill the demo CTA) |
| Sites with a top bar | 14 |
| Bars whose CTA repeats a nav CTA | 0 |

A second pass checked eight of the bar sites on an inner page. Seven show the bar on every page, and most use a text link in the bar, not a button. The bars mostly promote events, content or a separate free product. The closest match to our case was a lab-informatics platform. Its bar offers a free AI product with a text link, and "Request a demo" is its main nav button, next to a grey "Sign up" button.

The research also covered the "too many buttons" argument. Choice-overload studies use large sets (6 versus 24 options), and a meta-analysis puts the mean effect near zero, so they do not show that two buttons hurt. The better case for one primary button is visual hierarchy guidance and decision-conflict research: when two options look equal, more people defer. I kept that claim proportional in the thread.

## Step 3. Four positions in one day

I changed my mind three times. This table is the honest record, because the reasons are the useful part.

| Position | Nav | Bar | Why it changed |
| --- | --- | --- | --- |
| 1. The first recommendation | "Book a demo" solid, and "Try Assist free" as an outline after the bar is closed | Homepage only | The team preferred to remove the nav trial button entirely. |
| 2. Remove the nav trial button | "Book a demo" only | Homepage only, button CTA | Built, but never shipped on its own. No peer bar repeats a nav CTA, but the bar used a button and appeared only on the homepage. |
| 3. Bar on every page, as text | "Book a demo" only | Every site-nav page, text link | Visitors do not always start on the homepage, and seven of eight peer sites show the bar on inner pages. Shipped. Then I read the thread again. |
| 4. Swap on dismiss (shipped) | "Book a demo" while the bar shows, "Try Assist free" after the bar is closed | Every site-nav page, text link | This is what the colleague had proposed and I had agreed to. |

Between positions 3 and 4, I pasted the whole thread into the session and asked for an objective read. Its summary: the colleague's first comment argued against two primaries. My first reply agreed to remove the nav trial button. The colleague's follow-up then proposed the swap, and my last reply agreed to the swap. I had built from the first reply and missed the last one, because I worked from my memory of the thread, not from the thread.

## Step 4. Could we A/B test it instead?

I asked whether some visitors could see the trial bar and others only "Book a demo". The build is simple: a sticky 50/50 cookie set at the edge, read by the same pre-paint script as the bar. It would touch about six files and take four to six hours. The traffic is the problem. The calculator is in [`tools/power-check/`](tools/power-check/).

| Question | What a readable answer needs | At our traffic |
| --- | --- | --- |
| Does the bar get more trial clicks? (1% base rate, detect 2x) | About 2,300 visitors per arm | Months. The answer is also obvious, because the control arm has no trial CTA. |
| Does "Book a demo" lose clicks? (detect a 50% drop) | About 12,000 per arm | More than a year |
| Signups plus demo bookings, detect 2x | About 70 events in total | At least a year, and longer than the campaign will run |
| The same, detect 4x | About 20 events | Many months |

Three more problems: most trial-page visitors arrive from ads and QR codes that go straight to the trial page, so they would never get an arm. About half of the bar's clicks looked like the team's own. And a test cookie can need consent. The UK regulator (ICO) exempts A/B testing if visitors get notice and an opt-out, but the French regulator's (CNIL) exempt list does not name it. I left that as a question for the business, not a decision for the code.

**Recommendation:** no test. Ship the design on its design reasons, count outcomes each month from the Source column and the CRM, and propose a rule for removing the bar now, before the numbers come in.

## Step 5. Build it without making pages dynamic

The first bar version read its dismissal cookie on the server, and that kept the bar on the homepage, which was the only dynamic page. To put it on every page and keep every page static, the decision moved into the browser. The code is in [`recipes/`](recipes/sitewide-dismissible-bar.md).

- **A pre-paint mark.** A one-line inline script at the top of `<body>` reads the cookie and sets an attribute on `<html>`. CSS hides the bar and removes its 44px offset. The script runs before the nav is parsed, so the first paint is already final. The cookie is still set by a server route (Safari caps cookies written by JavaScript at seven days), but it is no longer httpOnly, so the script can read it.
- **A CSS-only swap.** Both nav buttons are in the HTML. One rule hides the trial button while the bar is visible, and another hides the demo button after the bar is closed or when the page has no bar. No JavaScript runs, so nothing flickers.
- **An offset audit.** A bar on every page moves the fixed nav down 44px everywhere. An audit found every sticky element that cleared only the nav: two sidebars, two tables of contents, a report bar, a filter bar with its date markers, a table toolbar and header, and the mobile menu. The mobile menu already sat under the nav on the homepage. Each one now adds the bar height, and one root `scroll-padding-top` fixes every in-page anchor.
- **A source tag per page.** The homepage keeps its original tag, so existing views still work. Every other page adds its section, for example `banner-pricing` or `banner-blog`. The nav buttons send `nav` and `nav-mobile`.

The production build for the bar change confirmed that every page is still static, and that the homepage became static again.

## Step 6. Adversarial review

Every build got an independent review before merge, and one reviewer was told to try to refute it. Prompts are in [`prompts/`](prompts/state-matrix-review.md). No review found a blocker. The findings that changed the code:

- **The booking page would have offered the trial (major).** /demo has no bar, so the swap put "Try Assist free" in the nav of the page where people book a demo. Nav now keeps "Book a demo" there.
- **The Back button brought the bar back.** A page restored from the back/forward cache does not run the pre-paint script again. The bar now checks the cookie again on `pageshow`.
- **Browsers without `:has()`** never apply the offset, so the bar would cover the nav. It is now hidden there, and the nav falls back to its no-bar state.
- **Print, and a focus ring.** The bar printed on every page, and on one dark-themed section its focus ring was dark on dark.
- **An accepted cost.** Visitors who closed the bar under the old httpOnly cookie see it once more. A middleware migration was not worth the code.

I tested every state in the browser: bar visible, closed in the session, closed before page load, a page without a bar, phone width, and a mid-width screen. Analytics is off in development, so I checked the tracking with a click listener that uses the site's exact CTA selector.

## Step 7. Ship and verify on production

Both changes were squash-merged. Each was live about a minute later. I checked the live HTML with curl: the bar is on the homepage, pricing and a blog post, each with the right source tag. There is no bar on the booking page, the trial page or a campaign page. The live stylesheet contains the swap rules. The dismiss route returns a readable 30-day cookie.

## Measuring it

- **Primary:** completed signups with a Source that starts with `banner` or `nav`, counted monthly, with internal addresses removed.
- **Guardrail:** demo meetings booked from the site.
- **Read date:** 90 days after launch.
- **Proposed removal rule:** if the bar has brought no outside signups by the read date, it comes down. I proposed this rule. The team has not agreed to it yet.
- **What this cannot show:** cause. Ad spend, conferences and the season all move these numbers. The goal is to notice a large problem, not to measure a lift.

## What I would do differently

1. **Build from the thread, not from memory of it.** I built two positions before I read the colleague's actual proposal again. Paste the source discussion into the session before the first line of code.
2. **Separate click evidence from outcome evidence on day one.** The first read mixed them, and clicks told the opposite story from outcomes. Say which one a claim rests on every time.
3. **Instrument before debating.** The mobile trial link was untracked and the nav link had no source tag. We argued about a CTA that we could not fully see.
4. **List the edge pages before the review does.** The booking page, the trial page and its terms page each needed a rule. A two-minute list at the start would have caught the /demo case before review.
