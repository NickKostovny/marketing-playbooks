# Tools used

Everything ran inside Claude Code. Internal connectors are described by what they do, not by name. No custom skills fired on this run; it was tool calls, three small scripts, and reading.

| Tool | Kind | What it did here | Gotcha |
| --- | --- | --- | --- |
| OpenSEO MCP (DataForSEO data) | MCP | 37 calls: 10 domain overviews, 11 ranked-keyword pulls (two of them path-scoped), 6 keyword-suggestion pulls, 3 keyword-metrics batches (200 US, 74 UK, 74 Ireland), 2 live SERP batches (12 queries), 1 SERP-competitor scan over 52 keywords, project context read and research-log write | Ranked-keyword rows are raw passthrough at about 4 KB each; 100 rows spill to a file, flatten it with Python. The suggestions tool caps at 100 rows by traffic and includes brand terms. Keyword metrics silently drops keywords with no data; diff your input list. Domain overview returned null backlinks for every domain. No English for Germany; European English is UK and Ireland. Quote `rank_group`, not `rank_absolute`, which counts AI Overviews as positions. |
| Internal product knowledge base | MCP | Landscape entries for six competitors; eight topic searches for the "why us" lines | Four of eight topics had no entry, which removed two ideas. An ambiguous competitor name returned two entry titles and no content. The explainable-analysis story was filed under a competitor comparison, not under its own name. |
| Site repository, blog folder | Local | Listing of the 39 published posts, to tell a quality gap (page exists, does not rank) from a topic gap (no page) | The inventory is what turns "write" into "rewrite" for one of the five. |
| Python 3, csv and json | Local | Flatten spilled ranked-keyword files, merge the two competitor samples, compute the gap, build the call log | Scripts in [`tools/gap-toolkit/`](tools/gap-toolkit/). |
| Claude Code session transcript | Local | Source of the citable call log: the input and output of every MCP call, including results that were only shown inline | Results the harness spilled to disk are referenced by path in the transcript, not embedded. |
