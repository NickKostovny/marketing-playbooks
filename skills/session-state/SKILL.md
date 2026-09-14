---
name: session-state
description: >
  Persist and resume work-session state through Linear instead of pasted handoff documents.
  Trigger whenever Nick asks for a "handoff doc", "hand-off document", "brief I can hand to a
  new chat", "package this up for a fresh chat", "carry this into a new session", or any request
  to document context so a future conversation can continue the work. Also trigger at the START
  of a session when Nick says "continue [campaign/project]", "pick up where we left off", or
  pastes a long handoff/brief blob from a previous chat. Also trigger near the END of any
  substantial work session when clear next steps exist — the close-out should launch work or
  write state, never produce a paste-me document. This skill replaces the handoff-doc habit
  entirely; use it proactively even when Nick asks for the document by name.
---

# Session State

One rule: **state lives in Linear and is pulled by reference. It is never relayed by paste.**

## Why this exists

An audit of ten consecutive sessions found four taxed by the handoff-doc loop (write doc → paste into new chat → repeat), and two killed on the first turn by policy-error rejections of the pasted blob. Pasted context also arrives as one undifferentiated block, which bypasses the skill triggers that would otherwise fire on a normal request. The handoff doc feels like diligence; it is actually the single largest workflow tax.

## The three moments

### 1. Closing a session (intercepts "make me a handoff doc")

When Nick asks for a handoff doc, or the session is wrapping with known next steps:

1. Create or update the Linear state doc for the campaign/project (format below). Attach it to the relevant Linear issue or project. Run `linear-write-cleanup` before writing.
2. Reply with a one-line resume command, e.g.: `Next session: "continue the paid ads campaign" — state is in Linear.`
3. Offer to launch the next phase now — parallel subagents for research or production work, a scheduled task for recurring work — instead of leaving it documented-but-unstarted. Respect existing approval gates (Slack posts, HubSpot writes, Linear writes Nick reviews).

Do not produce a handoff document in chat. If Nick needs a portable copy for a person, write the Linear doc first and export from there — Linear stays the source of truth.

### 2. Resuming a session ("continue X")

1. Find the state doc: `list_documents` / `get_document` on the campaign's project or issue.
2. Load it, note its last-updated date, and flag what's likely stale (deal stages, quotes, metrics).
3. Re-verify volatile facts from their sources of truth (`gtm-rules` governs which) rather than trusting the doc's copies.
4. Start working. Never ask Nick to paste context he has already paid to produce once.

### 3. Intercepting a paste

If Nick pastes a handoff blob anyway: extract what's new, merge it into the Linear state doc, treat embedded quotes and pipeline facts as unverified until re-pulled, then proceed with the actual work. One line of redirect is enough — "merged into the Linear state doc; next time 'continue X' is all I need." Fix the plumbing without lecturing.

## State doc format

Keep it under ~60 lines. It is a pointer index plus decision log, not prose:

```
# State: [Campaign / project name]
Updated: [date] · Status: [active / paused / blocked on X]

## Decisions made
- [decision] — [one-line why]

## Open items
- [item] — [owner]

## Next actions
- [action] — [launchable now? Y/N]

## Links
- Issue/project: [Linear ref]
- Assets: [files, designs, docs]
- Sources: [calls and docs the claims came from]
```

The cap matters: a long state doc becomes the new handoff blob. Anything wanting more than a line belongs in a linked asset, and verbatim customer quotes belong in transcripts (re-pull via `messaging-from-calls`), not in state.

## What this skill does not own

- Sentence quality of the doc → `linear-write-cleanup`
- Campaign brief structure → `idea-to-brief` (its briefs persist to Linear under the same rule)
- External deliverables → `content-proportion-check` and the content stack

## Precedence note

Where this skill and `portable-handoff` disagree about producing a handoff document, `portable-handoff` wins, by decision on 2026-08-06. The disagreement is kept visible on purpose; see the library README.
