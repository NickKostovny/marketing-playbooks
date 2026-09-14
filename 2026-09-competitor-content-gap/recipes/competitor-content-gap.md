# Recipe: competitor content-gap analysis that ends in a decision

Tooling: an SEO MCP with domain overview, ranked keywords per domain, keyword metrics, live SERPs and a SERP-competitor scan. I use OpenSEO, which sits on DataForSEO data. The steps and the traps transfer to any equivalent.

## 0. Read before you buy

Read the SEO project's shared context and research log. Note the site goal, the baseline and what was bought recently. Check the credit balance so you can report cost at the end.

## 1. Footprints

One domain-overview call per competitor and one for your own site. Record estimated traffic and keyword count. If backlinks come back null, compare authority on the domain rank field in the ranked-keyword rows instead, and say so.

## 2. Two samples per competitor

Both listing tools stop at 100 rows, and they sort differently.

- Ranked keywords: `limit 100`, organic only, minimum volume 10, `excludeBrandTerms` set per competitor (brand, product names, common misspellings), sorted by volume. Raw rows are large and will spill to a file; flatten with `flatten_ranked.py`.
- Keyword suggestions: no parameters; returns the top 100 by estimated traffic, flat rows, brand terms included. Remove brand rows in the merge.

For a competitor product that lives inside a huge domain, run one live search for the product name to find its section path, then pull ranked keywords with `scope: subfolder` on that path and `scope: exact_url` on the product page.

Small competitors will return a handful of rows or none. Write that down; it is a result.

## 3. Your own keywords and the gap

Pull your own ranked keywords with the same settings and no brand exclusion. A competitor keyword is a gap unless you hold a top-20 position for it. Run `merge_gap.py`. Expect the gap to be nearly everything if your footprint is small; the work is in the relevance filter and in reading the rows by competitor to name clusters.

## 4. Expand and hydrate

For each cluster write the candidates by hand: head term, acronym, "what is," "meaning," "vs" pairs, the pharma-modified and bioprocess-modified versions, vendor and instrument names. Hydrate up to 700 in one keyword-metrics call with monthly trends off. Diff input against output; the missing ones have no measured volume. Repeat for each market you were asked about; if a market and language pair is unsupported the call errors, and that is a limitation to report.

## 5. Live check the head terms

Fetch live SERPs, depth 10, for the strongest term in each cluster. Record the cast (regulators, Wikipedia, vendors, publishers, forums) and whether an AI Overview sits on top. Compare against the dataset positions you are about to quote; mark any that do not reproduce. Run one SERP-competitor scan over all candidate terms to see which named competitors appear anywhere on them.

## 6. Ground "why us"

Before scoring, query the product knowledge base for each cluster's topic and read the landscape entries for the competitors involved. No entry means the idea loses its "why us" line and usually its place. Anything marked outside the product's scope is removed regardless of volume.

## 7. Score

Three scores, 1 to 5 each: winnability (difficulty against your authority, plus the live cast), reader fit, direction fit. Label gap type: keyword, topic, quality. Break ties on direction fit, then on measured domain-specific volume. Lower winnability for navigational or transactional terms; a post does not satisfy them.

## 8. Deliver two files

- The memo: lead with the ask. One line per idea: title, gap type, volume, difficulty, why us. Under 150 words. One sentence saying positions are dataset positions unless verified.
- The data file: scoring table for every candidate including the removed ones, per-idea keyword rows for each market, removed ideas with reasons, missing data, cost, and the call log. Every figure carries `[call N]`.

## 9. Record

Append a research-log entry to the SEO project: what was bought, the result in one line, the cost, a do-not-re-buy date. Save the raw call files next to the memo.
