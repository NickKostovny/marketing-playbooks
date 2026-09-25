# Brief: historical ad engagement to SDR handoff

The ask, as given:

> I have a bunch of historical ads that I want to scrape the engagement from on LinkedIn. I want this so that I can ultimately pass it along to our SDR. Can you help me design a process to do this with credit efficiency? Here is an example link. Let me know if there is a better way to run this.

Two decisions asked for before any work, because they change the cost:

1. **What does the SDR receive?** Account signals only (zero enrichment credits; the outbound tool finds the buyers), hybrid (account list plus a short contact list, enrich only actionable rows), or emails for everyone with a known employer (highest spend, mostly non-target).
2. **How many ads?** Under five, up to twenty, or more. More than twenty means batching across sessions with a checkpoint file.

Standing rules the plan was built on:

- Scraping is free; enrichment costs about ten credits per person. Gate first, enrich last.
- Deal status is a blocking gate. Active-deal accounts ship in a separate hold file and go to the deal owner only.
- The persona filter is applied to headlines and labeled as a hypothesis. Expect near zero passes.
- Engagement lists are account signals, not contact lists. Say so at the top of the deliverable.
