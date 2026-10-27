# Tools used

| Tool | Kind | What it did | Gotcha |
|---|---|---|---|
| Agent app (Claude) with MCP connectors | Agent | Ran the whole pipeline, spawned the reviewer and checker agents | Subagents inherit nothing unless you pass it. That is the point for the cold reviewer |
| Chat connector (read-only) | Data | Read the engineering "shipped" channel and threads | Keep it read-only in the task prompt, in capitals, with no exceptions |
| Project tracker connector (read-only) | Data | Closed issues in the last 14 days, rolled up by project | Big projects often have no shipped-channel post. Flag them, do not write about them |
| Social-media drafting tool with brand voice (MCP) | Draft engine | Wrote first drafts from a brief | A brand rule like "lead with a quote" makes it invent quotes. Check the brand's do/don't list before trusting output |
| Social scheduling and review tool (MCP) | Review | Where drafts are reviewed and tracked | Its API cannot mark a post as published if you posted natively; I mark the title |
| Call-note connector | Data | 51 transcripts for the vocabulary study | Separate the recorder's microphone from other speakers; count only clear outside speakers |
| CRM connector | Data | Target-account list for the job-post study; rep notes | Rep notes are paraphrase. Count them apart from customer words |
| Web search and fetch | Data | Public practitioner writing and job posts | Forums were blocked by the proxy. Quotes from a model-assisted fetch must be checked at the URL |
| Shared doc connector | Output | The digest people comment on | Some renames are not reachable from the agent; do them by hand |
| Scheduled task | Automation | Runs every other Monday with an ISO-week gate | A "TEST RUN" suffix skips the gate for on-demand runs |
| Python | Local | Wilson confidence intervals for the word counts | A zero count still has an upper bound. Report it |

Skills: `working-in-public` (this entry), `content-proportion-check` and `writing-craft` (post copy), and a new cold-reader skill built from `prompts/cold-reviewer-pack.md`.
