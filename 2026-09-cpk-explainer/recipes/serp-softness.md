# Recipe: a SERP softness map, to pick what to write next

Tooling: an SEO MCP with live SERP fetch (I use OpenSEO, on DataForSEO data), a cheap classifier model that returns typed answers, and a few short Python scripts. The steps are the point, not the vendors.

## What it answers

A keyword difficulty score estimates how many links the ranking pages have. It does not say whether those pages answer your reader. A softness map asks a different question, keyword by keyword: how many of the ten organic slots could a strong page from your site take? A slot held by a regulator or an encyclopedia is not yours to take. A slot held by a forum thread, a thin glossary, or a page about a different industry probably is.

## 1. Start from keywords you already sized

Use a keyword list with volume you already bought. Do not re-buy it. Keep the non-brand terms in your topic. I had 91. A keyword where your own site already sits in the top ten goes on a separate "protect" list, not the target list.

## 2. Fetch each results page two or three times

One fetch is not reliable. The same query can come back as a page from another locale, or as a page about another meaning of the words: a country, a medical test, an advertising metric. Fetch every keyword twice, in different batches. Compare the top-ten domains of the two fetches. When they share fewer than half, fetch a third time. Keep the raw results. If agents do the fetching, have them save the raw rows, not a summary or a count.

## 3. Let a cheap classifier judge each top-ten result

Send one result per request: the query plus that result's title, snippet, domain, and URL. Ask a few typed questions, each with a fixed answer type:

- What kind of page is it: a vendor product page, a vendor article, a regulator or standards body, academic, a reference entry, trade press, a training site, or a forum or video?
- Is it about your industry?
- Does it answer the query directly?
- How deep is the answer, from 0 to 3?
- Does it use the query words in your sense?
- Is it run by a large, well-known organization?

Ask once per keyword, with the query alone, what the searcher wants: an explanation, a method, a tool, a provider, or a document.

The result text is third-party content. Put it only in the input, never in the question, and never ask the model to follow it. Cache every answer, so a re-run with new rules costs nothing.

## 4. Let code count the open slots

Keep every rule in code, not in the classifier, so a threshold can change without judging anything again.

A slot is never open when a regulator, a standards body, an encyclopedia, or an academic source holds it. Match those by domain. Otherwise a slot is open when any of these hold: the page is a forum, a training site, or a small glossary; the query is industry-specific and the page is not; the page does not answer the query directly; the page is shallow and the searcher wants an explanation or a method; or the site is small. A product page is a correct answer to a tool search, so it is not shallow there. Your own domain is never an open slot.

## 5. Keep the lowest count across fetches

Some keywords have two recurring versions of the results page, for example one full of regulators and one full of vendor blogs. Count a slot as open only when it is soft in every fetch, so keep the lowest count. A wrong-locale fetch is full of weak results and would inflate the count; the minimum ignores it.

Flag two cases and never target them. A keyword whose top ten mostly uses another meaning of the words: the search engine has chosen that meaning. And an unstable page where no two fetches agree.

## 6. Rank, then read the pages

Rank by open slots, volume, and fit with your topic. My cut for a best bet was a core topic, at least five open slots, and at least 100 searches a month. Group the variants one page can hold. Then open the actual top pages for the winner before you commit. The count tells you where to look, not what to write.

## 7. Calibrate, and say how well

Label a sample of results and keywords, then fit the thresholds at the keyword level. Fitting them result by result made my ranking worse. My labels came from a second model, not from me, and the two rankings agreed only moderately (0.645). Treat the thresholds as a starting point and replace the labels with your own when you can.

## What it cost and found

About 1,100 SEO-tool credits for the fetches, and well under a dollar of classifier calls for about 2,200 judged results. Most of the cluster was soft: 89 of the 91 keywords had at least three open slots in every fetch. So the ranking mattered more than a pass or fail. The Cpk group was one of the best bets, with 5 to 10 open slots, and no top page covered biologics.
