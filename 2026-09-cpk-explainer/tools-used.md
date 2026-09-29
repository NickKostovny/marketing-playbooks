# Tools used

Everything ran inside Claude Code. Internal connectors are described by what they do, not by name.

| Tool | Kind | What it did here | Gotcha |
| --- | --- | --- | --- |
| OpenSEO MCP (DataForSEO data) | MCP | Live results pages for 91 keywords, two or three fetches each; volume and difficulty reused from an earlier sweep; the key-page entry after ship | One fetch can come back from another locale or for another meaning of the words. Fetch two or three times and keep the lowest open-slot count. |
| Workflow tool (multi-agent orchestration) | Built-in | Ran the results-page fetches across parallel agents | The agents reported counts, not rows, so the raw results had to be read back out of their logs. Have agents save raw rows to files. |
| TypeSafe Jev (typed-judgment model) | API | Judged about 2,200 top-ten results with typed questions: page type, industry fit, direct answer, depth, sense of the words, site size; plus searcher intent per keyword | Third-party result text goes in the input only, never in a question. Cache every answer. The Python SDK needed a newer Python than this machine had; plain HTTP calls worked. |
| Python | Local | The open-slot rules and the ranking; the threshold calibration; a recompute of every worked-example number | Keep the rules in code, so a threshold change never needs the classifier again. |
| Internal product knowledge base | MCP | Checked every product claim; the source for the stated limit (no built-in Cpk index today) | Check it before the outline. The first outline assumed a feature that does not exist. |
| Internal call intelligence | MCP | Searched the sales-call corpus for Cpk and capability | No call mentioned Cpk. An empty search is a finding: no customer voice went into the post. |
| Web fetch | Built-in | NIST/SEMATECH, FDA, ISPE, Minitab, BioProcess International, and Steiner et al., fetched for research and again for the claim audit | Two professional-body pages returned HTTP 403. They were not cited. |
| Defensibility check | Claude Code skill | Sentence-level review: could each line be defended to an expert reader? ([public copy](../skills/defensibility-check/)) | |
| Blog cold read | Claude Code skill | Zero-context persona cold read plus the read-aloud grader; returned the one blocking FAIL ([public copy](../skills/blog-cold-read/)) | Give the persona the reader's actual data: one result per batch, not textbook subgroups. |
| Content-proportion check | Claude Code skill | Claim size against evidence, and whether practitioner language was sourced ([public copy](../skills/content-proportion-check/)) | |
| Brand review | Claude Code skill (marketing plugin) | Voice and terminology against the brand guide | |
| Product source-of-truth | Claude Code skill | Forces product claims through the knowledge-base connector | |
| Concept-explainer pipeline | Claude Code skill (custom, not published) | Staged the run: research, outline, draft, claim audit, gates | |
| Git worktree + Next.js dev server | Local | Rendered each draft through the real blog pipeline | Cut the branch from the remote main branch. The local main had drifted. |
| GitHub CLI | CLI | Pull request and merge | |
| curl | Local | Production check: status, canonical URL, robots meta | |
| Headless Chrome, Pillow | Local | Thumbnail render and the 400 by 250 card-size proof | |
