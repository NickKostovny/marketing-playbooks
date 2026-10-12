# Tools used

| Tool | Kind | What it did | Gotcha |
|---|---|---|---|
| Coding agent with an SEO tool connection (MCP) | Agent plus data | Crawl, backlinks, traffic estimate, project memory | Sign-in is a browser step the agent cannot do. Verify with two free reads before saying "connected" |
| Site crawl (100 pages, no performance run) | Data | Flagged thin pages, long titles and descriptions, duplicate headings | The crawl is a lead list. Confirm every item in the raw HTML |
| Backlink overview | Data | Referring-domain trend | A sudden spike can be auto-generated junk. Look at spam score before celebrating or panicking |
| curl and a few lines of Python | Local | Fetched pages, counted visible words, read headers and sitemap | Strip scripts and styles before counting words |
| GitHub CLI | Local | Listed pull requests, checked merge state, merged | Delete-branch flags can fail from a git worktree. Skip them |
| git worktree | Local | Isolated copy of main to test a change before merging | A symlinked `node_modules` breaks the Turbopack build. Use the webpack build for the test |
| Google Rich Results Test | Web | Confirms structured data parses as an article | Needs a public URL or pasted code |
| Scheduled task in the agent app | Automation | Monthly check, one-page report | Runs only while the app is open. Click "run now" once to pre-approve tools |
