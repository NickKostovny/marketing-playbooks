# Shipping an SEO audit and a post refresh: one action, then a measurable loop

**Shipped:** October 2026. Audit, four refreshes, one structured-data change, one scheduled monthly check.
**Type:** A B2B software site in a regulated industry, a one-person marketing team, a small organic footprint. Everything is grounded in crawl data, live fetches of the pages, and stored research from earlier months.

## The brief

Install an SEO tool in the coding agent, run an audit, and turn it into actions that can ship without a meeting. Then work out how to see whether any of it moved anything.

## Step 1. Install and sign in

The agent could install the skills and register the connection. It could not sign in for me. Sign-in is an OAuth approval in the browser, so the tools stayed unavailable until I did it. I only claimed "connected" after two free read calls (account and project list) came back.

## Step 2. Reuse before you spend

The project already held a research log from earlier months. The audit skill checks that log first and reuses anything under 30 days old. I bought only three things: a 100-page crawl, a backlink overview, and a domain overview. About 400 credits. Keyword research was skipped because the log already had it.

## Step 3. Verify every finding by hand

The crawler reports. It does not know your site. I fetched the home page, robots file, sitemap, and the pages the crawler flagged, and checked each claim against the raw HTML.

Findings the crawl made and the hand check confirmed or changed:

| Finding | Crawl said | Hand check |
|---|---|---|
| Thin product pages | 12 pages under 150 words | Confirmed, about 200 words including the menu |
| Text-only copies in the sitemap | Not reported | Found by reading the sitemap: about half of 340 URLs, no noindex |
| Duplicate H1 | 1 page | Confirmed in page source |
| Link spike | Referring domains up about 6x in six weeks | Mostly auto-generated "backlink checker" sites, spam score 35. No action |
| Tracking-parameter URLs | Flagged as noindex and canonicalized | Intentional. Moved to "already working" |

## Step 4. Choose one thing

The site was technically clean, so the one thing came from the data, not from a generic list: the best non-brand page still carried last year in its title. Refresh it, keep the address.

Rules for the one thing: doable this week, copy-paste steps, and a way to check it worked.

## Step 5. The mistake

The four refreshes changed the front-matter `date` to the refresh day. The blog sorts by that date, so three refreshed posts jumped to the top of the blog index ahead of genuinely new posts. A teammate's first instinct was to space the dates out. That would still be false dates.

The fix:
- Restore the original publish dates.
- Record the refresh in a separate `updated` field.
- Hold back the fourth refresh, a comparison post, because it would not have earned the top slot.

Lesson: freshness belongs in the modified date, not the published date. Check what your template sorts by before a refresh changes it.

## Step 6. A structured-data change, tested before merge

An old open change added post-level structured data (title, author, dates, publisher). I merged it onto the latest main in a throwaway copy, ran the type check and a production build, and read the rendered markup. Then I merged, then I read the live page source. No tool trusted a green preview alone.

## Step 7. Make it recurring

A scheduled task now runs on the first of each month. Prompt in `prompts/monthly-seo-impact-check.md`. It reads the same metrics, compares against a written baseline, writes a one-page report, and appends to the project log. Spend is capped.

## Results so far

Too early. Baseline: roughly 400 estimated monthly visits, about 80 ranked keywords, two non-brand terms in the top 10. All numbers are third-party estimates until the first-party search tool is connected. Judge the refreshes in about eight weeks.

## What I would do differently

1. Check what the blog sorts by before the first refresh, not after the merge.
2. Connect the first-party search tool on day one. Without it, every number is an estimate.
3. Ship metadata fixes as one weekly batch from the start, so each ranking move maps to one change set.
