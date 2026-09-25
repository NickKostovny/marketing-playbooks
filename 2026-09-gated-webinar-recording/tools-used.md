# Tools used

Everything ran inside Claude Code. Internal connectors are described by what they do, not by name.

| Tool | Kind | What it did here | Gotcha |
| --- | --- | --- | --- |
| Next.js site in a git worktree | Local | Asset registry, gate form, capture route, sinks, library entry with `gated` and `chapters` fields, campaign redirect, scoped design tokens | The repo lint rejects setting state inside an effect; read the remembered unlock through a store subscription. End-of-file appends to a shared stylesheet conflict with any branch that also appends there, and a hunk-level merge dry run does not show it. |
| Vercel CLI | CLI | Sensitive environment variables from a file, redeploy an alias to pick them up, deploy a public review copy of the branch to a personal project | `env add` only works inside the linked folder. Sensitive values cannot be pulled locally, so the live test is the only test. A BOM in the token file becomes part of the secret. |
| Vercel REST API | Web | Set the review project's framework and turn off SSO protection | The Vercel MCP is scoped to one team and returns 403 for a personal project; use the CLI token against the REST API. A project created without a framework runs as generic Node and the middleware returns 500. |
| Vimeo | Web | Host for the recording; oEmbed for title and duration; domain-level embed privacy | Read the oEmbed title and probe the duration before writing copy. The domain lock stops preview copies from playing, which is correct. |
| Spreadsheet database (Airtable) through an automation platform's raw-request tool | MCP | Created the dedicated base and table, inserted and deleted test rows, read them back to verify fields | A table inside an existing base inherits that base's automations. A test row fired a sales-facing workflow. |
| Newsletter platform (beehiiv) | MCP and API | Draft newsletter issue pointing at the page; the subscribe endpoint with double opt-in for the capture route | The MCP disconnected mid-project. The API path is gated on its own variables and skips with a warning when they are missing. |
| LinkedIn scheduling tool | MCP | Main post, one post per clip, explanatory comments, clip uploads, approvals removed then re-added as non-blocking, a blocking approval on the external speaker's clips | A pre-tool hook rejects em dashes in any payload. Uploads are a two-step signed multipart; put the signature in a file, not on the command line. Scheduled posts auto-publish, so stage as to-do. |
| whisper.cpp | Local | Full transcript once; word-offset JSON per clip window | Control tokens such as `<\|endoftext\|>` leak into the token stream unless filtered. The small model mishears domain terms; keep a fixes list. |
| ffmpeg and Pillow | Local | Cuts, rounded-card compositing, PNG subtitle overlays timed with `enable=between(t,a,b)`, loudness normalisation, title and end cards, contact sheets | This ffmpeg build has no `drawtext` or `subtitles` filter. Render text to PNG and overlay it. |
| In-app browser and the owner's signed-in browser | Local | Render checks on previews and production; a live form submit on production | Previews on a single-sign-on team need the owner's browser session. A headless screenshot of a mobile viewport lies about layout on this site; check in a real viewport. |
| Design system artifact | Claude artifact | Source of the tokens for the scoped `.pdg` block | The CSS minifier deletes `backdrop-filter: none`. Write the value you want. |
| Writing craft | Claude Code skill | Copy pass on the page, the chapter list, and the posts | See [skills/writing-craft](../skills/writing-craft/). |
| Uncertainty killer | Claude Code skill | Shaped the owner-actions list: what is blocked, on whom, by when | See [skills/uncertainty-killer](../skills/uncertainty-killer/). |
| Blog cold read | Claude Code skill | Cold read of the chapter list and the page copy against the target persona | See [skills/blog-cold-read](../skills/blog-cold-read/). |
| LinkedIn post shape (private skill) | Claude Code skill | Five beats, about 70 words, link in the first comment | Published here as [prompts/clip-post-five-beats.md](prompts/clip-post-five-beats.md). |
