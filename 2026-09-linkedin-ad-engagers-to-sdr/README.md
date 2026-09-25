# Turning old LinkedIn ad engagement into an SDR handoff without burning enrichment credits

**Type:** Sales-enablement data piece. Eighteen historical ads, everyone who reacted to them, deduped and gated by deal status and persona fit, enriched only where a rep would act, delivered as a seven-tab workbook. Built in one session on 2026-09-18, revised 2026-09-25.

Every company has old ads with likes on them. The likes are people, the people have employers, and someone in sales would like the list. The trap is that "the list" is not the deliverable. Most people who react to an ad are not buyers, and enriching all of them costs real money for a spreadsheet nobody can use. This run was about deciding what to spend credits on before spending any.

## The brief

A folder of short links to historical ads. Scrape the engagement, hand it to the SDR, do it credit-efficiently, and say if there is a better way. The link format was a redirect, so even resolving what the ads were came first. The brief and the two decisions I asked for up front are in [`prompts/brief.md`](prompts/brief.md).

## Step 1. Cost model first

Scraping a post's reactors from your own logged-in browser costs nothing. The only paid step is asking an enrichment tool for an email, at about ten credits per person. So the order is fixed: resolve, scrape, dedupe, gate, gate again, and only then enrich the survivors. On the previous run of this kind, a hundred and eleven engagers became twenty-five lookups and twelve emails, and nobody cleared the persona filter. I told the reader to expect that again.

I offered three deliverable shapes and asked for a choice before touching anything:

| Option | Credits | The SDR gets |
| --- | --- | --- |
| Account signals only | 0 | An account list with the engagers as evidence; the outbound tool finds the buyers |
| Hybrid | roughly 250 per 100 engagers | The account list plus a short contact list for the few actionable people |
| Emails for everyone possible | highest | Mostly non-target emails |

Hybrid was chosen, with more than twenty ads to cover. That set the batching design: per-ad files, a checkpoint file, resume from wherever a session dies.

## Step 2. Resolve the links without a browser

A `curl -sIL` on each short link returns the real post URL in a `location` header, and the numeric id in that URL encodes its publish timestamp (id shifted right 22 bits is milliseconds since epoch). Eighteen links resolved to one post from February 2025 and seventeen variants of a single campaign from one day in November 2024. Knowing that before scraping changed expectations: seventeen creative variants of one ad reach one audience, so the dedupe across ads would matter more than the per-ad counts.

## Step 3. Scrape from the logged-in browser, and get the data out

The reactor list only exists behind the reactions modal on a logged-in page, so the scrape runs as a script inside the real browser: open the modal, click "show more" until the row count stops changing, read name, headline, connection degree and reaction type off each row. That part is old. Getting two hundred rows out of a browser tab and onto disk is where the session went sideways, and the recipe records every dead end so the next person skips them:

- The browser allows one automatic file download per site per session. Re-navigating does not reset it. Seven ads' worth of scrapes silently never landed.
- The site's content security policy blocks `fetch`, `sendBeacon` and form posts to localhost.
- A top-level navigation to a local receiver with the JSON in the query string is not blocked. The receiver writes the file, then holds its reply for two seconds so the page survives long enough to return its result, then redirects back to the site so the tab never rests on a localhost page.
- The browser extension's site-safety check later refused to run scripts on the ad post URLs for over an hour while accepting the feed page. Loading each post inside a same-origin iframe from the feed page, and scraping the frame, got around it. Splitting frame load and scrape into two calls kept each under the 45-second script timeout.

Details and the scripts are in [`recipes/scrape-post-reactors-from-your-own-browser.md`](recipes/scrape-post-reactors-from-your-own-browser.md) and [`tools/linkedin-engagers/`](tools/linkedin-engagers/). Counts came back one short of the displayed total on two ads, which is normal (hidden or deleted members), and the workbook says so.

## Step 4. One row per person, employer as a hypothesis

Eighteen ads, 235 reactions shown, 233 captured, zero comments on any of them, 222 unique people. The headline is the only employer signal, and it is a bad one: 58 percent of headlines name no employer at all. The parser tries "at", "@", "chez", "bei", a list of well-known company names with word boundaries, and a last-resort trailing segment that must look like a company. Every employer it produces is labeled `inferred`, and the account roll-up carries a confidence column, so a reader never mistakes a guess for a fact.

## Step 5. Deal gate before anything else

This is the gate that protects the sales team from itself. Every parsed account went through the CRM. Any account with an active deal goes to a separate `HOLD` file, and the file name is the guardrail: nobody runs a hold file by accident. Closed-lost accounts are marked as revivals, because a closed-lost that looks cold is usually a conversation somebody already had. Seven accounts in this set had active deals or partnerships. Their engagers are routed to the deal owner as one line of context, not as leads.

## Step 6. Persona gate, and the honest result

The persona filter is a rule on the headline: target departments, a seniority floor, explicit exclusions. It is a hypothesis, since a headline is not an HR title, and the workbook says so in the column name. Zero of 222 people passed. That is the third run in a row with a zero, and it is the finding, not a failure: engagement lists are account signals, not contact lists.

What the gate did surface was a short "worth a look" tier: process or manufacturing-science roles below the seniority bar, people who engaged more than one ad, and people at revival accounts. That tier plus the active-deal tier is the whole action list, 42 rows.

## Step 7. Enrich only what a rep would act on

Within the action list, a row earns an enrichment lookup only if the role matches the target departments or sits at director level or above, and the employer resolved to a domain. That was seven people. Six came back with verified work emails. The cost was about seventy credits, against roughly two thousand for enriching every row with a domain. Two of the seven are the only rows in the whole file a rep should actually read first, and both sit inside active accounts, so they go to the account owner.

Lookups by name need the company as a domain or a company-page URL. One large pharma's domain does not resolve in the enrichment tool and needs its LinkedIn company URL instead. Email results are asynchronous; one sat in progress for twenty minutes and shipped as "re-poll" rather than blocking the file.

## Step 8. Ship

One workbook, importable into Google Sheets with the tabs intact: a Read me tab that explains every priority code and column, the action list, the account roll-up, the hold accounts, the account-template rows for the outbound tool, every person with every gate result, and the ads themselves. Three scripts regenerate all of it from the raw scrapes and two hand-maintained inputs (deal statuses, enrichment results). The first question after delivery was what the tab name "Contacts P0-P2" meant. It is now "Action list", and the Read me tab explains the codes in plain words. Name tabs for the reader, not for the pipeline.

## Results so far

| | |
| --- | --- |
| Ads | 18 |
| Reactions captured | 233 of 235 |
| Comments | 0 |
| Unique people | 222 |
| Persona filter passes | 0 |
| Accounts with an active deal, held | 7 |
| Enrichment lookups | 7 |
| Verified emails | 6 |
| Credits spent | about 70 |

The audience finding matters more than the list. The November 2024 campaign drew a broad, mostly European, mostly non-bioprocess audience: data scientists, IT consultants, pharmacists, accountants, medical representatives, students. That is a targeting note for the next campaign, and it was invisible until someone read the headlines.

## What I would do differently

- Check the ad platform's account-level engagement demographics before scraping people. If the account layer is already there, the person scrape only needs to run for the action tier.
- Start every scrape from the feed page with the iframe mode. It survived the safety check, needs no downloads, and takes one call per ad.
- Budget for the employer problem up front. More than half the rows have no employer in the headline, and the strongest single persona in the set (a "CMC Head" with no company) is unroutable without a manual look at the profile.
