# Tools used

Everything ran inside Claude Code. Internal connectors are described by what they do, not by name.

| Tool | Kind | What it did here | Gotcha |
| --- | --- | --- | --- |
| Workflow tool (multi-agent orchestration) | Built-in | Six runs: an 11-agent decision run (data read, code map, peer sites, downstream value, three design lenses, a judge, two skeptics, synthesis), a peer-site and diff check, an offset and mechanism audit, two pre-merge reviews, and an A/B feasibility check that ended with a skeptic | Give every agent the same context block, and put the source discussion in it, not your summary of it. |
| Product analytics MCP | MCP | Click counts by page, CTA tag and device; trial-page arrivals by source; per-visitor rates for the power check | Bots are counted by default, so filter them. Internal devices had to be inferred from timing and city. There was no internal-traffic filter. |
| CRM MCP | MCP | Demo bookings from the site's meetings link (aggregate counts only) | The meeting object needed extra permissions, so bookings were counted from contact properties. Those keep only the latest value. |
| Signup table export | Manual | Completed signups and their Source column, pasted into the session | This was the count of record. Analytics runs only after consent, so it undercounts. |
| Web fetch and in-app browser | Built-in | 21 peer homepages, plus inner pages for eight of them: nav CTAs, computed button styles, bars, close controls | Many navs render client-side, so record what you could not see. Take one dated snapshot, and do not generalize past it. |
| Git worktree + Next.js dev server | Local | Isolated checkout off the remote main branch, its own port | Turbopack panics on a symlinked `node_modules`. An APFS clone (`cp -cR`) takes three seconds and uses no extra disk. |
| In-app browser + JavaScript | Local | Every bar and nav state, sticky offsets against the nav's bottom edge, layout-shift entries, phone and mid-width screens | The pane is often hidden, so real clicks and screenshots fail. Dispatch synthetic clicks and measure with scripts. |
| Click listener with the site's CTA selector | Local | Checked that each new tag would be recorded, with analytics off in development | Copy the selector exactly. An element outside it sends nothing, which is how the mobile trial link went untracked. |
| `next build` | Local | Confirmed that every page stayed static and the homepage became static again | It runs alongside a dev server, because the dev server writes to its own folder. |
| curl | Local | Production checks after each merge: the bar, the source tags, the swap rules in the live stylesheet, the cookie flags | Add a cache-busting query when you poll for a new deploy. |
| GitHub CLI | CLI | Pull requests, squash merges, remote branch cleanup | `gh pr merge --delete-branch` breaks under worktrees. Delete the remote branch with `git push origin --delete`. |
| [`tools/power-check/`](tools/power-check/) | Script | Test duration for clicks and for rare outcomes | Use the traffic that can actually reach the test, not total site traffic. |
