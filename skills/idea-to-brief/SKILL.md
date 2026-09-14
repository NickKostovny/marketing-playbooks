---
name: idea-to-brief
description: "Convert raw inputs (call transcripts, pasted ideas, conference takeaways, customer quotes, slack threads, rough notes) into a structured marketing brief plus a downstream-tool prompt — for landing pages, one-pagers, ad creative, email sequences, or any marketing asset. Trigger on signals like \"turn this transcript into a [page/one-pager/asset]\", \"build me a brief\", \"make this into a campaign\", \"draft a prompt for Claude Design\", \"I have an idea for a marketing piece\", or any moment where Nick is trying to convert raw material into a structured production-ready spec. Also trigger when Nick pastes a transcript or unstructured idea without a formal request — that's the most common failure mode (jumping straight to producing the asset). This skill is the gate. It produces the brief and the prompt. It NEVER produces the asset itself."
---

# Idea to Brief

This skill converts raw inputs into structured briefs and downstream-tool prompts. Its job is upstream — orchestration, sourcing, and decision-forcing — not production. Production happens elsewhere (Claude Design for landing pages, separate tools for one-pagers and ad creative, etc.).

## Why this skill exists

The most common failure when turning ideas into marketing assets is jumping straight to drafting the asset. Drafting creates sunk-cost momentum that overrides defensibility checks. Claims labeled *Inferred* or *Invented* slip past because the page already looks like a page. Audience recognition assumptions get baked in because the headline already feels good.

The fix is to separate the brief from the asset. The brief commits to claims, audience, foil, and story arc *before* any production tool sees the work. By the time Claude Design (or whichever production tool) gets involved, every load-bearing claim is sourced and every named entity is audience-validated.

This also makes the system asset-agnostic. A brief that survives the gates below can become a landing page, a one-pager, an ad, or an email sequence — production tooling changes, brief structure doesn't.

## When to use this skill

- Transcript dropped into chat (call, conference talk, internal meeting)
- Idea pasted without formal request ("here's something I'm thinking about...")
- Explicit ask: "turn this into a landing page / one-pager / asset"
- Explicit ask: "build me a Claude Design prompt"
- Customer quote or sales-call moment that feels asset-worthy
- Cluster of evidence that wants to become *something* but the something isn't named yet

## When NOT to use this skill

- Reviewing or editing an existing draft → use `content-proportion-check`, `defensibility-check`, `writing-craft`
- Strategy decisions about whether to make an asset at all → use `strategy-decisions`, `brand-marketing-framework`
- Pure execution problems with an existing pipeline → use `execution-compounding`
- Internal status updates → use `uncertainty-killer`
- The asset is already drafted and just needs polish → not this skill

## Core rule

**This skill produces a brief and a prompt. It does not produce the asset.**

If the urge appears to draft the page/one-pager/email itself, that urge is the failure mode this skill exists to prevent. Hand the brief and prompt off. Stop there.

## The four phases

Walk through these in order. Don't skip ahead. Each phase has a gate that must clear before moving on.

### Phase 1 — Source

Pull every available data source before drafting anything. First, state the **provisional cell** (layer × mode — see Phase 2, Pick 0) so you pull the right corpus; Pick 0 confirms or changes it.

- **Product Hub MCP** for feature specs, persona context, lifecycle phases, customer-product fit
- **search_calls** on every named entity (competitors, tools, methodologies, product names)
- **HubSpot deal status** for any company that might appear as an audience target — cross-reference active deals before any outbound is implied
- **Granola** for relevant meeting transcripts if context warrants
- **Existing Invert content** if the new piece relates to or extends prior work
- **For digital-layer assets**, scientist calls are the wrong corpus. Source from what digital leaders themselves say — their LinkedIn posts (a Sales Navigator list of digital leaders is the roster) and digital-side calls. A digital-layer pain claim with no such source is Inferred at best.

Then hand off to `content-proportion-check` for the Sourced / Inferred / Invented audit. Every external claim gets a label.

**Gate (blocking):** Anything labeled *Invented* must be sourced or cut before Phase 2. This is not a warning. It is a stop.

*Inferred* claims may pass, but only if labeled as Inferred **in the brief itself** — an unlabeled Inferred claim counts as Invented. A brief holds a stricter bar than published content because everything built downstream inherits the claim without re-checking it. The most common failure of this skill is letting Inferred claims survive unlabeled because they "feel right" or because the user wants to keep moving.

### Phase 2 — Story

Force four picks. Don't move forward until all four are made.

**Pick 0 — Cell (gate, blocking).** Name the layer and the mode from the matrix in `brand-marketing-framework`, and the distribution path:

- *Layer* — Scientist (IC who runs the workflow) / Program leadership (director owning a molecule's development) / Digital (owns infrastructure + AI budget across the business). IT and procurement are not valid audiences; if the input points there, stop and say so.
- *Mode* — Proof (Invert on screen: workflow clip, lifecycle map, the governed-AI stack) / Perspective (observation from inside the reader's problem, no Invert pitch).
- *Distribution* — Organic (scientist layer only) / Promoted or ads targeted to the persona (program layer) / Promoted or ads to the matched audience of digital leaders (digital layer). A program- or digital-layer brief with no promotion plan is not ready.

The cell decides which positioning applies: instrument framing at the scientist layer, lifecycle framing for program leadership, governed-AI-vendor framing for digital. Choosing the cell late is how a digital business case ends up written scientist-to-scientist.

**Pick 1 — Foil decision.** Three options:
- *Named foil* — explicitly call out a competitor, tool, or category leader (e.g. "A well-known tool designs the next experiment. Invert designs it from your data.")
- *Implicit foil* — indict the category without naming a specific player (e.g. "Most DOE tools start at a blank page.")
- *No foil* — lead with the practitioner problem alone, no comparison

Each has a tradeoff. Named foil is sharpest but assumes audience recognition (see audience recognition check below). Implicit foil is broader but blunter. No foil works when the practitioner problem is itself the wedge.

**Pick 2 — Sentence variants.** Generate three for the hero/lead:
- *Bold* — most concrete, takes a position, names names
- *Safe* — broader resonance, less brand risk
- *Provocative* — sharpest hook, highest churn risk

User picks one. Not "pick the best by feel" — the explicit tradeoff between bold/safe/provocative forces the reader-recognition decision.

**Pick 3 — Artifact type.** Three options:
- *Past-tense* — "here's what your data already shows" (analysis demo)
- *Future-tense* — "here's what we'd recommend next" (forward-looking demo)
- *Both* — past + future as a two-step narrative

For non-product assets (one-pagers, emails), translate to: existing-state evidence, future-state vision, or both.

**Audience recognition check (gate, blocking).** Any named entity in the hero — competitor, tool, methodology, internal product term — must pass: *does the audience know what this is without a definition?* Evidence comes from sales calls, conference signals, or industry-standard usage. If recognition can't be established, either name a different entity, switch to implicit foil, or add a reader-aid — but the recognition decision must be conscious, not assumed.

This gate is hypothesis-grade. It came from a single observed failure (a named competitor in a hero where audience evidence did not support the brand recognition). Track whether it generalizes.

### Phase 3 — Brief

Produce the structured brief. Use this exact template:

```
# [Asset name / route]

## Purpose
One sentence on what this asset is and where it lives (landing page / one-pager / etc.)

## Cell
Layer × mode (e.g. Digital × Perspective). Distribution: organic / promoted to [matched audience].

## Audience
Specific persona inside that layer. Default tools/workflows they use. Confirmed via [sources].

## Foil (or frame)
The position this asset takes against the alternative. Or, if no foil, the frame that organizes the message.

## Story arc
1. [Hero / lead]
2. [First section]
3. [Second section]
...
N. [CTA]

## Defensibility log
Table: Claim | Source | Status (Sourced / Inferred / Invented).
Anything not Sourced must be flagged with a TODO.

## Artifacts needed
What screenshots, captures, data points, or assets need to be produced before publish. Include who owns each.

## Status
Draft / Pending captures / Ready for production / Live.
```

The brief is the handoff artifact. It can be reviewed by anyone (CEO, Head of Sales, CX lead, agency, designer) and tells them everything they need to evaluate or extend the work — without producing the asset itself.

**Persist the brief in Linear — the chat copy is a working draft, not the artifact.** Write the finished brief to a Linear document attached to the campaign's issue or project (run `linear-write-cleanup` on it first). Use the Linear MCP tools — `save_document`, `save_issue`, `save_comment`, `list_documents`. This is not the handoff-doc loop — a brief has multiple human readers (CEO, Head of Sales, CX lead, agency, designer) and needs one canonical version they can all open. That is exactly what Linear is for.

Re-pasting a brief between chats is the thing to avoid: it bypasses skill triggers, has tripped policy filters and killed sessions on the first turn, and drifts from the live version. So future sessions resume by pointing at the Linear brief — "continue the paid ads campaign" — not by carrying its body along. If Nick does want a portable copy for a fresh chat, `portable-handoff` owns that artifact and Linear stays canonical.

### Phase 4 — Downstream-tool prompt

Generate the prompt for whichever production tool will build the asset. Structure:

1. **One-sentence frame** — what the codebase/file/spec contains. Tells the tool to read the brief before generating.
2. **Action verb** — "render first, then iterate" / "produce three variants" / "draft and stop." Without this, production tools default to over-elaborating.
3. **Locks before opens** — what's fixed (palette, copy, story arc) listed before what's variable. Naming what's fixed prevents drift more reliably than naming what's wanted.
4. **Open decisions surfaced explicitly** — any unresolved Phase 2 picks where multiple variants would be useful.

**Don't repeat what's in the brief.** The brief carries audience, foil, defensibility log, story arc. The prompt carries action and constraints. If the prompt is repeating the brief, the brief isn't being read by the production tool — fix that first.

**Offer to launch production immediately.** The prompt's destination is a production run — so offer to start it now, as a subagent or fresh session pointed at the Linear brief by reference (the canonical copy, not a pasted one). Ending the session with a prompt that waits for Nick to manually relay it is the handoff-doc loop in disguise.

## Failure modes this skill exists to prevent

Name these explicitly when you notice them happening:

- **Drafting drift.** "Let's just draft it and source it later." No. Phase 1 gate is blocking.
- **Audience recognition assumption.** Any named entity in the hero needs evidence the audience knows it. Don't assume.
- **Stat smuggling.** A specific number from a sales pitch is not a benchmark. If a quantitative claim isn't traceable to a measured behavior, flag it with a verification TODO.
- **Skipping foil decision.** The choice between named/implicit/no foil is a real fork. Defaulting silently to "named foil because it feels bold" without checking audience recognition is the most common drift.
- **Skipping the cell.** A brief with "audience: bioprocessing practitioners" and no layer or mode inherits the wrong positioning downstream. Name the cell or return that it cannot be named.
- **Producing the asset.** This skill produces the brief and the prompt. If a draft of the asset itself appears in output, the skill has failed.

## Hypothesis flags

This skill is hypothesis-grade — n=1 from a single landing-page workflow. Mark these as untested at scale:

- The four-phase structure (Source → Story → Brief → Prompt) — works for landing pages, untested elsewhere
- Audience recognition check — derived from one observed failure
- Asset-agnostic claim — needs validation across at least one one-pager and one ad-creative use before promoted from hypothesis
- "Build the brief, not the asset" rule — strong intuition, single confirmation

Revisit and revise after 3–5 uses. If a phase consistently doesn't earn its place, cut it.

## Examples

### Example 1 — Transcript → landing page brief

**Input:** User pastes a sales-call transcript and says "this feels like it could be a landing page."

**Output:**
- Phase 1: search_calls on every competitor and tool mentioned; pull Product Hub for relevant features; HubSpot check on any companies named; SII labels on every claim
- Phase 2: cell (layer × mode × distribution) + three foil options + three sentence variants + artifact type, force picks
- Phase 3: structured brief
- Phase 4: Claude Design prompt referencing the brief

What's NOT in the output: any HTML, copy beyond the hero sentence, or design direction. The brief carries those decisions for the production tool.

### Example 2 — Idea fragment → one-pager brief

**Input:** "I want to make a one-pager on the customer purification story for an analyst audience."

**Output:**
- Phase 1: search_calls on the customer, pull the existing narrative artifacts, audience recognition check
- Phase 2: cell (likely Program leadership × Proof, promoted), foil decision (probably implicit — the alternative is no instrument framing at all), sentence variants, artifact type (existing-state vs. forward)
- Phase 3: brief — purpose, audience, frame, story arc, defensibility log, what visuals/quotes are needed and who owns capture
- Phase 4: prompt for whichever tool will produce the one-pager (could be Claude Design, could be a doc generator, depends on output format)

### Example 3 — Premature production attempt

**Input:** User pastes notes and says "great, draft the page now."

**Correct response:** "Before drafting, let's run the brief. Phase 1 — what claims in here are sourced? [audit]. Phase 2 — what's the cell, then what's the foil? [force picks]." Hold the line. The skill exists because skipping to draft is the failure mode.

If the user pushes back, surface the failure mode by name: "The reason I'm holding the line is that drafting first is exactly what created the competitor-hero issue last time — momentum overrode the audience recognition check."

## What this skill delegates to

- `content-proportion-check` — Sourced / Inferred / Invented audit (Phase 1 gate)
- `writing-craft` — sentence-level rewrites if hero variants need polish (Phase 2)
- `defensibility-check` — sentence-level reviewing if a draft already exists outside this flow
- `hamming-taste-principles` — taste check on whether the story carries weight
- `brand-marketing-framework` — owns the layer × mode matrix and persona definitions (Pick 0); strategic stress-test if the asset's existence is in question

This skill is the orchestrator. The above are the specialists.