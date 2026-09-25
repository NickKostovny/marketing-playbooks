# Tools used

Everything ran inside Claude Code. Internal connectors are described by what they do, not by name.

| Tool | Kind | What it did here | Gotcha |
| --- | --- | --- | --- |
| Claude Code clarifying question | Built-in | Asked me the two decisions only I could make (how "Log in" works, what goes above the card), each with a recommended option, before any code was written | Ask after scouting, not before. Checking the real app's sign-in page first is what made the options concrete. |
| Workflow tool (multi-agent orchestration) | Built-in | Four reviewers with one lens each plus a build agent, then one skeptic per lens told to refute every finding. Nine agents, about five minutes | Give every agent the same context block, including a "known facts, do not re-litigate" list. Without it, skeptics waste time on pre-existing issues. |
| Git worktree + Next.js dev server | Local | Isolated checkout off the remote main branch, its own dev server port | Branch from the remote main, not a stale local main. Copy `node_modules` with an APFS clone (`cp -Rc`) instead of reinstalling. |
| In-app browser | Local | Clicked through every accordion path, measured layout and focus with JavaScript, desktop and 375 px | A fixed cookie banner covers controls on a short viewport: use a taller viewport rather than clicking the banner. Script clicks can leave the window unfocused, so `:focus` reads false. |
| Claude in Chrome | Browser extension | Switched off the lead table's email automation in a signed-in session | The in-app browser is not signed in to third-party tools; the extension uses your real browser session. Reload after the change to confirm it saved. |
| Vercel CLI and MCP | CLI, MCP | Environment variable names (not values), production deployment list, runtime logs, preview status | Full-text log queries time out over wide windows. Scope to one deployment id. |
| GitHub CLI | CLI | Pull requests, merge, remote branch cleanup, open-PR overlap check | GitHub computes mergeability against main only. `git merge-tree --write-tree` against each open PR's head finds PR-to-PR conflicts. |
| Product analytics MCP | MCP | Event and property discovery | Its query tool loaded without a parameter schema in this session, so every query failed validation. The answer came from reading the tracking code instead. |
| Headless Chrome over the DevTools protocol | Local | The screenshots in `assets/`, with the consent banner hidden by CSS for the picture only | Chrome's command-line print flag hangs on this machine, so I did not rely on the command-line flags. Driving it over the DevTools protocol works. |
| CoreImage QR detector (Swift) | Local | Decoded every QR image in the print files to confirm where they point | macOS only. Script in [`tools/qr-decode/`](tools/qr-decode/). |
| Next.js bundled docs | Docs | Confirmed `redirect()` returns a 307 from a server component and when it falls back to a meta refresh | The framework version in the repo differs from most training data. Read the docs in `node_modules`, then verify with curl. |
