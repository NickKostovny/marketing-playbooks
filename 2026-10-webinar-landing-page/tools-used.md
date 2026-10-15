# Tools used

Everything ran inside Claude Code. Internal connectors are described by what they do, not by name.

| Tool | Kind | What it did here | Gotcha |
| --- | --- | --- | --- |
| Owner's signed-in browser | Local | Read the publication's listing (title, date, length, bios); LinkedIn people search for speaker handles; one speaker's public profile for a bio | The listing is behind a bot check that the in-app browser cannot pass. A web search refuses to look up named people; LinkedIn's own people search does not. |
| Static page build (Node script) | Local | Inlines the wordmark SVG and the two licensed font weights as data URIs into one HTML file | The public version in `tools/static-page/` swaps the licensed font for the system stack. |
| Vercel CLI | CLI | Deploys the standalone mock to a personal project with a public alias | Only the clean alias is public. The per-deploy hash URLs sit behind single sign-on and return a redirect to anyone else. Production deploys with `--prod`; without it the deploy is a preview nobody outside the team can open. |
| Pillow | Local | Turned white-on-navy partner logos into ink-on-transparent PNGs (`tools/recolour-logos.py`); centre-cropped circular headshots to squares | A square cropped inside a circular headshot keeps about 72 percent of the diameter. Ask for square originals. |
| Next.js site in a git worktree | Local | The production page: a route, two client components, a page-scoped public folder, a scoped block appended to the global stylesheet | Turbopack refuses a symlinked `node_modules`; clone the folder with `cp -c -R`. The global stylesheet styles elements, so scoped rules on leads and labels need `!important`, and a styled link needs `.scope a.class`, not `.class`. |
| GitHub CLI | CLI | Five PRs, five squash merges, check polling | A worktree branch cut from the remote main tracks main until the first `git push -u`; `gh pr create` then aborts unless you pass `--head`. |
| Background check loop | Local | `until` loops on `gh pr checks` and on `curl` against production, so merges and confirmations happened without polling by hand | Foreground `sleep` is blocked in this harness; put the loop in a background task. |
| In-app browser | Local | Render checks at 1280, 900, 800 and 390; computed-style and bounding-box reads for the fold measurement; console and network checks | A screenshot taken before the image optimizer finishes shows grey boxes. Read the network log, then screenshot again. |
| LinkedIn scheduling tool | MCP | Three posts at to-do with non-blocking review requests, internal comments with the preview link, speaker and company mentions by URN | A pre-tool hook rejects em dashes. Scheduled posts auto-publish, so stage as to-do. Mention URNs come from a vanity-name lookup, which needs the handle first. |
| Campaign-page skill | Claude Code skill | The port procedure: read the newest campaign page in the repo fresh, branch off the remote main, scoped CSS, dynamic client components, noindex metadata, build before push | The template page had moved on since the skill was written. Reading it fresh each run is the point. |
| Git author identity skill | Claude Code skill | Set a real author before the first commit so preview deploys are not blocked | The repo convention was the owner's work email, which beat the GitHub no-reply form here. |
| Writing craft | Claude Code skill | Copy pass on the page and the posts | See [skills/writing-craft](../skills/writing-craft/). |
