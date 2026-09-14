# Claude skills: a working library

Skills I run in Claude (Cowork and Claude Code) as Head of Marketing at Invert. A skill is a Markdown file with a trigger description and a body of decisions, tests, and constraints. Each one exists because a default model answer was wrong for my work in a specific, repeatable way.

This is the public subset. The private library also holds company-specific skills (CRM writes, customer briefs, product source of truth) that are not mine to publish. Some files here reference those by name; treat the names as pointers into a larger system. Four more skills are held back for now.

## How the library is built

- **Skills carry what only I know**: decisions, sources of truth, taste, exemplars. Anything the model could produce unprompted is cut. `skill-audit` is the rulebook for that.
- **Descriptions are the expensive layer.** They load every turn. Bodies load only when a skill fires.
- **Tool names are verified against the live toolset.** A rail that names a dead tool is worse than no rail.
- **Contradictions are kept when they are real.** `portable-handoff` and `session-state` disagree about handoff documents. `portable-handoff` wins, by decision on 2026-08-06. The argument stays visible.
- **Sourced / Inferred / Invented.** Every claim about a practitioner's world is labeled. Invented never ships.

## Index

### Operating system for the work

| Skill | Fires when |
|---|---|
| [`skill-audit`](skill-audit/SKILL.md) | Governs writing, editing, compressing, merging, splitting, or deleting skill files in this library, including inside skill-creator runs. |
| [`portable-handoff`](portable-handoff/SKILL.md) | Package any handoff, brief, or context transfer as ONE self-contained artifact you can copy or attach in a single action. |
| [`session-state`](session-state/SKILL.md) | Persist and resume work-session state through Linear instead of pasted handoff documents. |
| [`linear-write-cleanup`](linear-write-cleanup/SKILL.md) | De-bloat pass on any text Claude writes into Linear: issue titles and descriptions, comments, project and initiative descriptions, documents, status updates. |
| [`uncertainty-killer`](uncertainty-killer/SKILL.md) | Apply whenever communicating with internal stakeholders: Slack messages, status updates, emails to teammates, syncs, or keeping founders and cross-functional partners informed. |
| [`strategy-decisions`](strategy-decisions/SKILL.md) | Apply Reid Hoffman's two-rule strategy framework to a strategic decision, a set of options, or a debate about whether to pursue something. |

### Marketing judgment

| Skill | Fires when |
|---|---|
| [`saddles-positioning`](saddles-positioning/SKILL.md) | Apply at strategic positioning moments: "what are we actually selling," "what business are we in," "how do we position against X." |
| [`content-proportion-check`](content-proportion-check/SKILL.md) | Editorial gate on any marketing content representing Invert to bioprocessing practitioners and the leaders who fund their tools. |
| [`defensibility-check`](defensibility-check/SKILL.md) | Sentence-level review of marketing content, from any source: apply "what specifically do you mean?" to each claim-making sentence. |
| [`writing-craft`](writing-craft/SKILL.md) | Invert's house style decisions for any prose: Slack, email, LinkedIn, blog, status updates, investor comms, internal docs. |
| [`hamming-taste-principles`](hamming-taste-principles/SKILL.md) | Aspirational taste principles for writing, briefing, reviewing, or evaluating marketing content. |
| [`idea-to-brief`](idea-to-brief/SKILL.md) | Convert raw inputs (call transcripts, pasted ideas, conference takeaways, customer quotes, Slack threads, rough notes) into a structured marketing brief plus a downstream-tool prompt. |
| [`blog-cold-read`](blog-cold-read/SKILL.md) | Run a cold read on blog or LinkedIn content at two altitudes: a text draft, and the finished, assembled artifact. |
| [`transcript-audit`](transcript-audit/SKILL.md) | Audit a raw, auto-generated transcript for likely mis-transcriptions and return a grouped list of catches to fix. It does not rewrite the transcript. |

### Thinking and people

| Skill | Fires when |
|---|---|
| [`learning-medium`](learning-medium/SKILL.md) | Anti-transmissionist learning principles for exploring a new domain or building mental models of unfamiliar concepts. |
| [`giving-feedback`](giving-feedback/SKILL.md) | Prepare feedback for someone: a direct report, a peer, a founder, a collaborator. |

## Layout

```
<name>/SKILL.md            the skill
<name>/references/*.md     reasoning and exemplars, loaded on demand
REDACTION-NOTES.md         what kinds of changes were made between the private and public copies
```

## Using them

Copy a folder into your own skills directory. Read the description first. It is the trigger. Then edit the body until it carries your decisions, not mine.
