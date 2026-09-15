# Deciding what to write next: a competitor content-gap analysis from SEO data

**Type:** Decision memo. Nine competitor and adjacent domains, our own footprint, one keyword gap, five blog ideas scored on winnability, audience fit and strategic fit. Every number cites the API call that produced it.

SEO tools usually arrive after a piece is written, to pick a title. This run used the SEO data before anything was written, to decide which product-adjacent pieces should ship at all. What competitors rank for and we do not is a map of the questions our buyers already type into a search box that nobody on our side has answered. That is a product-content decision, and it deserves data of the same quality as any other decision.

## The brief

One page. Who reads us (process development scientists, MSAT engineers, CMC people at biopharma, CDMOs and cell and gene therapy companies). The content direction (integrations plus AI, not AI alone). Nine competitor domains. Markets: US and EU, English. Four steps: pull each competitor's top pages and keywords, pull ours and run the gap, score each candidate 1 to 5 on winnability, audience fit and direction fit and label the gap type, pick five and drop any idea with no source data. Two output files: a Slack message under 150 words that leads with the ask, and a data file with scores, API sources, removed ideas and missing data.

Two rules did most of the work: do not invent numbers, cite the API call for each figure; flag missing data, do not estimate. A reusable version of the brief is in [`prompts/competitor-gap-brief.md`](prompts/competitor-gap-brief.md).

## Step 1. Footprints first

One domain-overview call per site. Competitor names are replaced with descriptions here; the numbers are as returned.

| Site | Est. organic visits/mo (US) | Organic keywords |
| --- | --- | --- |
| Us | 363 | 40 |
| A, enterprise bioprocess informatics suite | 1,768 | 343 |
| B, GxP manufacturing-intelligence SaaS | 155 | 34 |
| C, ELN and LIMS platform with a bioprocess product | 6,670 | 1,110 |
| D, bioprocess data tool inside a life-science catalog domain | 4,553,040 | 253,947 |
| E, industrial time-series analytics vendor | 5,924 | 596 |
| F, bioprocess control-layer software | 1 | 6 |
| G, scientific data cloud | 1,913 | 313 |
| H, hybrid-modeling specialist | 43 | 2 |
| I, digital experiment platform | 5,893 | 864 |

Backlink counts came back null for every domain, so authority was compared on the dataset's domain rank instead: ours sits around 200, the two largest competitors around 425, most of the rest between 260 and 300. That gap is the ceiling on every winnability score below.

## Step 2. Sample what each competitor ranks for, twice

Two tools list a domain's ranking keywords, and both stop at 100 rows. One sorts by search volume and lets you exclude brand terms and set a volume floor. The other sorts by estimated traffic, includes brand terms, and returns flat rows. Sorted by volume, a big domain's top 100 is generic vocabulary. Sorted by traffic, it is the pages that actually work. Pulling both and merging them gave 755 competitor rows to read instead of 400.

Competitor D lives inside a catalog domain with a quarter of a million keywords, so a domain-level pull would have returned laboratory chemicals. One live search for the product name gave the section path, and a path-scoped pull returned its 15 keywords.

Three competitors turned out to have no non-brand footprint at all with ten or more US searches a month: 31 rows of brand collisions, 6 misspellings of a name, and one PDF. That is a finding. The specialists in this market are not found through search.

## Step 3. The gap is almost everything

Our site ranks for 40 keywords. Two of them are non-brand and in the top 20 (the two spellings of "bioprocess software," both held by one listicle). Four competitor rows overlapped with those. Everything else was a gap by construction, so the computation took one line and the work moved to filtering: a relevance pattern cut 755 rows to 280, then I read those competitor by competitor and named the clusters.

- A ranks with definitional explainers far from bioprocess (a proteomics glossary page, cell-therapy definitions, conference pages) plus one cluster on chromatography data systems.
- C runs a knowledge base of acronym explainers: process performance qualification at 5,400 searches a month, position 4, plus twelve variants at positions 2 to 4; then electronic lab notebooks, LIMS, MES, GxP, contract manufacturing terms.
- E holds eight spelling variants of "first principles model" at positions 1 to 4, a generic root-cause-analysis explainer, a statistical-process-control use-case page, historian terms, signal filtering.
- G's data-integrity post ranks 3rd for "alcoa plus," and it has LIMS-and-ELN content and a review-by-exception video.
- I owns design of experiments: 7th on the 12,100-a-month head term, 1st on "types of doe," 5th on "what is doe," plus quality-by-design definitions.

## Step 4. Expand the clusters and size them in three markets

From those clusters I wrote 200 candidate keywords by hand and hydrated them in one call, monthly trends off. 138 came back with rows. 62 came back empty, and five more with zero volume. The empty list is the same lesson as the OPC UA post: every bioprocess-modified phrasing has no measured volume.

| Came back empty (a sample of the 62) |
| --- |
| hybrid model bioprocess, digital twin bioprocess, doe bioprocess, doe cell culture, doe upstream process development |
| root cause analysis pharma, deviation investigation pharma, control chart pharma, process capability pharma |
| ai in biomanufacturing, ai in bioprocessing, gxp ai, explainable ai pharma |
| golden batch (every variant), bioprocess data, bioprocess data analysis, scale-up comparability, tech transfer biologics |

The demand is generic vocabulary. The way to win it is the generic term written for our reader, not the reader's term.

EU coverage was the brief's second market. The dataset has no English for Germany at all (the call errors with "Available: de"). English in Europe means the United Kingdom, which is not in the EU, and Ireland, where the same 74 keywords returned 66 rows for the UK and 39 for Ireland with volumes from 10 to 320 a month. Ireland was the strongest EU signal in the study, and it was strongest on data integrity, which fits a country full of drug-product plants. All of this is stated in the data file as a limitation rather than smoothed over.

## Step 5. Check the dataset against live results

Every competitor position so far came from the dataset. Ten live searches on the strongest head terms tested it. Two positions did not reproduce: competitor E's 6th place for "root cause analysis example" and its 1st-to-4th on "first principles modeling" were both absent from the live top ten that day. So the memo says, in its second sentence, that every position in it is a dataset position.

The live casts also set the ceilings. "alcoa principles" is vendor blogs and publishers, winnable. "electronic batch record" is MES vendors and a Microsoft documentation page, not winnable from our authority. "root cause analysis example" is generic business content, the wrong reader. "design of experiments" is a quality association, a statistics vendor, a university and Wikipedia; the head term is out of reach and the bioprocess tail is empty.

## Step 6. Ground "why us" before scoring, not after

Each "why we would win" line had to come from the product knowledge base, not memory. Six competitor landscape entries and eight topic searches. Four of the eight topics returned nothing: data integrity and Part 11, MES and electronic batch records, validation status, and the phrasing I used for the explainable-analysis story (which does exist, filed under a competitor comparison rather than under its own name; that is a knowledge-base gap worth fixing).

The consequences were real. The MES and electronic-batch-record idea had a 6,600-a-month head term at difficulty 10 and a competitor at position 9, and it was dropped, because a "why us" line I cannot source is a line I cannot write. The process-performance-qualification cluster, the biggest single gap found, was dropped because the knowledge base marks that work as outside the product's scope. On the positive side, deviation investigation is marked as core value and design of experiments as an established capability, which is what put one on the list and kept the other in the running.

## Step 7. Score and pick

Winnability, audience fit and direction fit, each 1 to 5. Gap types: keyword (we cover the topic, not the term), topic (no page of ours covers it), quality (our page exists, the competitor's ranks, ours does not). Ties broke on direction fit, then on measured pharma-specific volume. One adjustment: a chromatography-data cluster scored a point lower on winnability because its terms carry navigational intent (people looking for a vendor's software download), which a blog post does not satisfy.

| Idea | Gap | Primary term, US vol / KD | W | Fit | Dir | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Deviation investigation with process data in one place | topic | pharma cluster 620/mo, KD 0 to 12 | 4 | 5 | 5 | 14 |
| ALCOA+ for AI-assisted process analysis | topic | alcoa principles 1,600 / 7 | 4 | 4 | 5 | 13 |
| Our ELN-and-LIMS post, rewritten to rank | quality | what is lims 1,300 / 13 | 3 | 5 | 4 | 12 |
| SPC reports for biologics | topic | statistical process control report 590 / 18 | 3 | 5 | 4 | 12 |
| Mechanistic vs data-driven models | keyword | mechanistic model 390 / 0 | 4 | 5 | 3 | 12 |
| Chromatography data into process analysis | topic | unicorn software 140 / 0 | 3 | 4 | 4 | 11 |
| Design of experiments for bioprocess | topic | design of experiments 12,100 / 19 | 3 | 5 | 3 | 11 |
| Quality by design explainer | topic | qbd 1,300 / 8 | 3 | 4 | 2 | 9 |
| MES and electronic batch records | topic | electronic batch record 6,600 / 10 | 2 | 3 | 3 | 8 |
| GxP for AI analysis | topic | gxp compliance 1,000 / 0 | 3 | 3 | 2 | 8 |

Five more were removed without scores: PPQ (out of scope), tech transfer (a quality gap of ours, but no listed competitor ranks there), data historians (already drafted), and two piles of off-audience terms (discovery-stage definitions, conference names, dilution calculators, file-glob syntax).

## Step 8. Deliver

Two files. The memo leads with the ask and gives each idea one line: title, gap type, volume, difficulty, why us. Under 150 words, one sentence of caveat. The data file carries the scoring table, the per-idea keyword rows in all three markets, the removed ideas with reasons, the missing-data list, and a 37-call log where every input and output is saved and every figure in the text points at a call number. Cost: 740 credits.

The memo, with competitors described instead of named:

> I need your pick: which two of these five do we write first? Volume, difficulty and competitor positions are US dataset figures.
>
> 1. Deviation investigation with process data in one place. Topic gap. 620/mo cluster, KD 0 to 12. The time-series vendor ranks with a generic RCA post. Our assistant compares the batch to history and helps draft the report.
> 2. ALCOA+ for AI-assisted process analysis. Topic gap. 1,600/mo, KD 7. The scientific data cloud ranks #3 for "alcoa plus". Inspectable code answers the auditability objection.
> 3. Our ELN-and-LIMS post, rewritten. Quality gap. 1,300/mo, KD 13. It ranks for nothing. Two competitors rank.
> 4. SPC reports for biologics. Topic gap. 590/mo, KD 18. The time-series vendor ranks #8. We ship automated CPV reports.
> 5. Mechanistic vs data-driven models. Keyword gap. 390/mo, KD 0. The time-series vendor and an equipment maker rank. Two demo posts exist.

## Results so far

Delivered September 9, 2026. The pick was still open when this log was written. Ranking baseline for all five topics is zero. The SEO project's research log records what was bought and a do-not-re-buy date, so the next session starts from the file, not from the API. First ranking check: December 2026, on whichever two ship.

## What I would do differently

- Run the product-knowledge check before scoring, not after. It removed two ideas late and would have saved the keyword work on both.
- Live-check every competitor position that will be quoted upward. Two of the strongest ones did not reproduce, and a caveat sentence is a weaker fix than a verified number.
- Check which markets the dataset actually serves before promising a market in the brief. "EU, English" turned out to mean Ireland at 10 to 320 searches a month, plus a country that left the EU.
- Pull both competitor samples from the start. Knowing that both tools cap at 100 rows, and sort differently, is the difference between reading a competitor's generic head terms and reading the pages that earn its traffic.
