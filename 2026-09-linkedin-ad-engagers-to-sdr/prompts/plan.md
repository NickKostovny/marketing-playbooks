# The approved plan (as written before the run)

**Cost model.** Scraping costs zero credits. Only the enrichment data point burns them. Gate everything for free first and enrich last, only the survivors.

**Steps**

1. Resolve and date every link with `curl`, no browser. Output a checkpoint file with post URL, id, date, scraped flag, shown and captured counts.
2. Scrape in the user's logged-in browser. Per post: open the reactors modal, page it out, save one JSON per post; then comments.
3. Dedupe across all ads. One row per person with ads engaged, reaction types, comment count, a strong-reaction flag.
4. Employer from the headline, labeled inferred. Drop own staff, competitors, suppliers, academics.
5. Deal gate on every account. Active goes to a hold file. Closed-lost is a revival flag.
6. Persona gate, rule-based on the headline. Expect roughly zero passes and report it plainly.
7. Enrich only rows in the action tier with a target-department match or director level, and a resolved domain. Twenty per call, email only. Poll the asynchronous results.
8. Ship an account-level template for the outbound tool, a short contact list, a hold file, and a read-me.

**Credit budget.** About ten credits per contact. At twenty-plus ads the unique-person count can reach several hundred, so confirm the enrichment workspace and its per-user cap before step 7, and report the planned count before spending.

**Batching.** Work directory with a `raw/` folder for every payload. The checkpoint file is the resume point. Build the dedupe and gates only after all ads are scraped, then enrich once.

**Pilot.** Steps 1 to 6 on one ad first. Confirm the modal still paginates the same way and the capture count matches. Then batch the rest.
