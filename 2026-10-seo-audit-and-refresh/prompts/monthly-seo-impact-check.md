# Monthly SEO impact check (scheduled task prompt)

Replace the bracketed items. Each run starts with no memory, so keep the prompt self-contained.

```
Run the monthly SEO impact check for [DOMAIN] using the [SEO TOOL] connection.
Project ID: [PROJECT ID] ([COUNTRY], [LANGUAGE]). If sign-in is needed, stop and say so in one line.

BASELINE ([DATE], third-party estimates): [VISITS] monthly organic visits, [N] ranked keywords,
[N] non-brand keywords in the top 10 ([LIST]). Brand terms were [X]% of traffic.
CONTEXT: [LIST OF CHANGES SHIPPED, WITH DATES]. Judge refreshes after about eight weeks.

STEPS
1. Check account credits. If under [FLOOR], stop and report.
2. Read the project log. Do not re-buy research from the last 30 days.
3. If the first-party search tool is connected, use it as the main source. If not, say so in one line.
4. Pull traffic and keyword count.
5. Pull ranked keywords. Split brand from non-brand. Count non-brand top 10 and top 100.
   Report ranks for [KEY TERMS].
6. Check the live results for [2 HEAD TERMS], fetched twice (single fetches are unreliable).
   Count the organic position, not the AI answer box.
7. Backlinks only every third month. Judge links on non-spam domains.
Keep spend under [BUDGET].

OUTPUT
- One-page report to [PATH]/YYYY-MM.md: table of metric, baseline, now, change; then three
  sentences on what moved and what to do next. Brand and non-brand reported separately.
  Label every number as first-party or estimate. No hype.
- Append one line to the project log.
- Reply in under 120 words: headline change, one risk, one next action, report path.
```
