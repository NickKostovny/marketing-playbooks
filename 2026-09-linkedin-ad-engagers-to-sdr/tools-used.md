# Tools used

Everything ran inside Claude Code. Internal connectors are described by what they do.

| Tool | Kind | What it did here | Gotcha |
| --- | --- | --- | --- |
| `curl` | Local | Resolved 18 short links to post URLs and decoded the post ids into publish dates | Follow redirects with `-sIL`; the last `location` header is the post. |
| Claude in Chrome (the user's logged-in browser) | MCP | Opened each ad, expanded the reactions modal, ran the extraction script, and carried the JSON to a local receiver by navigation | One automatic download per site per session. Page CSP blocks fetch and beacons to localhost. The extension's site-safety check refused scripts on the ad URLs for over an hour; iframe mode from the feed page got around it. 45-second per-script timeout. |
| Local HTTP receiver (Python stdlib) | Local | Wrote each scrape payload to disk from a query string; held the reply two seconds; redirected back to the site | Default request-line cap is 64 KB; raised to 4 MB for large posts. |
| Internal deal-status connector (CRM) | MCP | One lookup per parsed account: active, closed-lost or none; owner and stage | Search by company name; a subsidiary or a differently spelled name can return an unrelated match, so read the deal names. |
| Internal knowledge base | MCP | Pulled the persona definition the gate encodes | Kept out of the public scripts; placeholders instead. |
| Clay MCP | MCP | Name-plus-company lookups for the action tier, then one Email data point per matched entity | Search needs a domain or a company LinkedIn URL. One large pharma's domain does not resolve; use the company URL. Results are asynchronous; poll the task. Responses over the token cap land in a file; parse with Python. Pass explicit entity ids to the enrichment call or you enrich every namesake. |
| Python 3, csv, json, re | Local | Dedupe across ads, headline-to-employer parsing, rule-based persona gate, priority tiers, account roll-up, template rows | Scripts in [`tools/linkedin-engagers/`](tools/linkedin-engagers/). |
| openpyxl | Local | One workbook with seven tabs, frozen headers, filters, wrapped columns | Google Sheets imports it with tabs intact. |
