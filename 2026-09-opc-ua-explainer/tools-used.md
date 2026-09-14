# Tools used

Everything ran inside Claude Code. Internal connectors are described by what they do, not by name.

| Tool | Kind | What it did here | Gotcha |
| --- | --- | --- | --- |
| OpenSEO MCP (DataForSEO data) | MCP | Keyword volume and difficulty for 137 candidates, live SERPs for 7 queries, 108 related keywords for the seed term, project context and research log | Zero-volume keywords are silently dropped from results. Two of its tools return payloads too large for the context window; flatten the spilled file with Python. |
| Internal product knowledge base | MCP | Feature specs for data ingestion and integrations; the source for every capability claim and every stated limit | If it has no entry, say so in the copy instead of inferring. The "two weeks" figure had no entry. |
| Internal call intelligence | MCP | Searched calls for "OPC" and "historian"; pulled six transcripts for verbatim quotes | Search results are paraphrased signals, not speech. Verbatim needs the transcript tool, three calls at a time, inside a subagent. |
| Vercel MCP | MCP | Deployment list and state, protection settings, build logs | Cannot mint a share link on a single-sign-on team. Use the dashboard Share button. |
| GitHub CLI | CLI | Open-PR survey, conflict check, mark ready, merge | A merge-tree dry run against main before merging catches conflicts with other branches. |
| Next.js dev server in a git worktree | Local | Rendered every draft through the real blog pipeline | Markdown content edits need a server restart to show. |
| In-app browser | Local | Desktop and 375 px checks; JavaScript measurements of overflow and layout | Screenshots reset scroll to the top; hide preceding elements to frame a mid-page section. |
| Headless Chrome, Pillow, ffmpeg | Local | Full-page render of the post; thumbnail render and 400 by 250 card-scale proof | Headless Chrome clamps narrow window widths; do mobile checks in a real viewport. |
| Cold-read grader | Claude Code skill | Two agents: persona cold read and read-aloud pass, run before and after the PM review | Give the grader the reviewer's persona, including the incumbent tool they own. |
| Product source-of-truth | Claude Code skill | Forces product claims through the knowledge base connector | |
| Verify UI before steps | Claude Code skill | Checked Vercel's current docs before writing the Share click-path | Vendor UIs move; quote button labels from current docs. |
| Wikipedia, OPC Foundation reference | Web | Standard facts: IEC 62541, OPC Classic and DCOM, the LADS companion specification and its bioreactor example | |
