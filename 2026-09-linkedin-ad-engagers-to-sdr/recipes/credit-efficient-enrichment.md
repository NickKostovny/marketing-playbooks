# Recipe: enrich an engagement list without burning credits

The rule: an enrichment lookup is the last step, never the first, and it runs only on rows a rep would act on.

## Order of operations

1. **Dedupe across every post before any lookup.** Each person is looked up once.
2. **Parse the employer from the headline and label it inferred.** No employer, no lookup; the name search needs a domain or a company-page URL.
3. **Deal gate.** Active-deal accounts are not enriched for outbound at all. Their engagers go to the deal owner as context.
4. **Persona gate.** Department match plus seniority floor plus exclusions, on the headline.
5. **Scope the lookup.** Action tier only (active-deal, passes, or worth-a-look), and within it only rows whose role matches a target department or sits at director level or above, and whose employer resolved to a domain. On this run that was seven of 222.
6. **Search by name plus company, up to twenty per call.** Check the resolved company name in the response before trusting any match; a domain can resolve to a namesake company. If a domain does not resolve, retry with the company's LinkedIn page URL.
7. **Add the Email data point with explicit entity ids.** Omitting the ids enriches every namesake the search returned.
8. **Poll.** Results are asynchronous. Most land in a minute or two; some sit in progress. Ship with those flagged "re-poll" rather than blocking.
9. **Write the reason for every empty email.** `email_status` says: verified, pending, not found, no employer domain, or out of scope. A blank is never an answer.

## Cost check

About ten credits per contact with one Email data point. Seven lookups cost about seventy credits and returned six emails. Enriching every row with a resolved domain would have cost roughly two thousand for a list nobody would send.
