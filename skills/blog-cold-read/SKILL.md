---
name: blog-cold-read
description: >
  Run a CEO-grade "cold read" on Invert blog/LinkedIn content at two altitudes: (A) a text draft,
  and (B) the finished, assembled artifact — e.g. when the blog copy and a Claude Code-built visual
  or interactive demo are merged into a Vercel preview before publish. Fires automatically after
  Claude drafts or substantially revises a blog/LinkedIn post, after Claude assembles or merges
  content into a page or preview, and on demand when Nick pastes a draft or shares a preview URL and
  wants it graded. Trigger signals: "write/draft a blog or LinkedIn post," "here's a draft," "grade
  this," "review this blog," "is this ready to publish," "merged into a Vercel preview," "review the
  preview," "the page is assembled," "ready to deploy." Works in both Cowork and Claude Code. Does
  NOT edit inline — it spawns a standalone grader agent that reads with zero Invert context and
  returns a scorecard. Do NOT trigger for emails, decks, one-pagers, ads, or short-form copy.
---

# The Cold Read — CEO blog grader

## What this is

A standalone editorial grader for blog and LinkedIn content. It was built from 28 real comments left by a senior reviewer at Invert on a draft blog post. Those comments collapse into **8 recurring failure patterns** — plus a 9th, target resonance, added from Invert's marketing strategy — and almost all of them flow from one root failure:

> **The draft was written for a reader who already knows Invert.**

Top-of-funnel content reaches people with zero Invert context. When a draft assumes that context, every other problem follows — undefined terms, buried points, claims that read as false. The reviewer's own role on that draft was to be the reader who *didn't* have the context. This skill automates that role.

It does not edit inline. It runs a **cold read**: a separate agent — no memory of having written the piece, no Invert knowledge loaded — reads the draft as the *target persona* (fluent in their field, but having never heard of Invert) and grades it. Clean context is the entire point. The author (you, or Claude having just drafted) rationalizes the gaps a cold reader trips on. A grader sharing the author's context will miss the same things the author missed.

## When this fires — two altitudes

**Mode A — Draft cold read (text).** After Claude drafts or substantially revises a blog/LinkedIn post, or when Nick pastes text to grade. Reviews the words.

**Mode B — Assembled cold read (finished artifact).** After the blog copy and a Claude Code-built visual/interactive are merged into a page or Vercel preview — the last gate before publish. Reviews the whole thing a visitor lands on: copy + visuals + the demo + what's above the fold, together. This is the higher-value read: text-only review can't catch a visual that contradicts the copy or a demo that distracts from the point.

- **Automatically** — run before presenting the draft (Mode A), or before deploy/publish (Mode B).
- **On demand** — when Nick pastes a draft or shares a preview URL and asks for a grade or "is this ready."

Not for emails, decks, one-pagers, ads, or any short-form copy.

## How it runs — spawn the grader agent

**Do not grade in the same context that wrote the draft.** That defeats the purpose. Spawn a standalone subagent.

1. Gather the inputs: the content (**Mode A** the draft text; **Mode B** the merged content — blog text + the Claude Code-built page/component files + the Vercel preview URL if one exists), **the target persona** (the specific job title), and **the piece type** (shipped or aspirational). If the target persona is missing, get it before grading — the grader reads *as* that persona.
2. Spawn a subagent with the **Agent tool** (`subagent_type: "general-purpose"`), pasting the prompt block below with the draft (Mode A) or the assembled inputs (Mode B) substituted in. For Mode B, follow "Seeing the render" below.
3. Receive the scorecard.
4. If the verdict is **HOLD**, or any **BLOCKING** pattern is **FAIL**: revise the draft to clear every blocking issue, then spawn a fresh grader and re-run. Repeat until no blocking FAILs remain.
5. Only then present the draft to Nick, with the final scorecard attached so he sees what was checked.

### The read-aloud pass (spawn alongside the cold read)

Spawn a SECOND, separate agent that does nothing but read the piece out loud. The comprehension grader rewards a crisp line even when it sounds machine-made — a clean em-dash antithesis sails through. Saying it aloud is the only reliable detector of AI voice, so it gets its own agent and its own mandate.

Spawn it at the same time as the cold reader (step 2), with the same content (Mode A the draft text; Mode B the assembled copy) and the same target persona. Receive both scorecards. A read-aloud verdict of SOUNDS GENERATED, or any STUMBLE/UNSAYABLE headline, forces REVISE: rewrite the flagged lines and re-run before presenting — same loop as a blocking FAIL, scoped to voice. Deep sentence surgery still defers to writing-craft; this pass only decides whether it sounds spoken.

### Seeing the render (Mode B)

A Vercel preview is a live, client-rendered page — fetching its HTML returns a near-empty shell, so don't judge it from source HTML alone. In order of preference:

1. If a browser/screenshot tool is available (e.g. Claude in Chrome), navigate to the preview URL, screenshot the top of the page and scroll through it, and grade what actually renders.
2. Otherwise, read the source files — the blog text plus the Claude Code component/page — and reason about the assembled result.

The grader must state which it did. Never claim to have seen a render you only inferred from source.

### The grader agent prompt (paste verbatim, with the draft)

```
You are grading a piece of writing for Invert, a bioprocessing data company.

TARGET PERSONA: {{the specific job title this piece targets — e.g. "downstream
process scientist, AAV" or "Director of Scale-Up at a CDMO." If none was given, ask
for it before grading. "Everyone in bioprocessing" is not a valid target.}}
PIECE TYPE: {{shipped | aspirational. "shipped" = what Invert does today.
"aspirational" = intentionally forward-looking ("pull the future forward"). If not
given, assume shipped.}}

Read AS THAT PERSONA, with one twist: you are fluent in their field and their daily
work but have NEVER HEARD OF INVERT and have no idea what its product does. Assume all
the DOMAIN knowledge the target has (their unit ops, modality, jargon); assume ZERO
Invert/product knowledge. You are NOT the author. Grade only what is on the page. If
you have to guess what Invert does or who this is for, that is a failure of the writing.

Grade the draft against these 8 patterns. For each, return PASS, FLAG, or FAIL and
QUOTE THE EXACT LINE(S) that triggered it. No quote, no flag.

1. INVERT-CONTEXT ASSUMPTION  [BLOCKING] — Does it explain what Invert / the product
   is before leaning on it, for someone who has never heard of Invert? FAIL if it
   assumes you already know what Invert does. Domain and job knowledge is fair to
   assume — this is about INVERT context, not field context.

2. FACTUAL TRUTH — PRODUCT & CUSTOMER  [BLOCKING] — FLAG every concrete product / SKU /
   feature / customer claim for the author to confirm (you can't verify them). If PIECE
   TYPE is "shipped": FAIL anything stated as current fact that contradicts itself or
   reads as not-yet-real. If PIECE TYPE is "aspirational": do NOT fail it for describing
   an unshipped capability — instead FAIL only if that future capability is framed as if
   it already ships today. Aspirational is allowed; dishonest tense is not.

3. EARNED CLAIMS  [BLOCKING] — For each sentence that asserts value, ask "what does
   this sentence do for me, the reader?" FAIL sentences that carry no weight, state
   a non-contrast ("X is deterministic" with no stated alternative), or could be
   deleted with no loss.

4. CONCRETE REFERENCE  [BLOCKING] — Does every "this / that / it" point at
   something already named on the page? Is every term defined at first use? FAIL
   orphan pronouns ("fix that data" — what data?) and cold terms (a feature name or
   "preview" appearing with no prior introduction).

5. SETUP BEFORE PAYOFF  [BLOCKING] — Two things; don't confuse them. (a) REFERENTIAL
   setup: FAIL a term or "this/that" used before it's understandable ("that's what
   changed" before anything was established as changing). (b) Leading with the demo /
   result and putting the data-foundation mechanics LAST is the INTENDED Invert
   structure — do NOT flag payoff-first ordering. "Lead with the main point" means lead
   with the hook/result, not the mechanics. Only FAIL if the main hook is actually
   buried below the fold, or a claim is never paid off.

6. EARNED TECHNICAL DEPTH  [FLAG] — Judge jargon RELATIVE TO THE TARGET PERSONA. Do
   NOT flag domain/modality terms the target already knows (strain, cell line, vector,
   TFF) — those are the targeting mechanism, not a problem. FLAG only terms THIS persona
   wouldn't know, or Invert-specific terms used without explanation. Never penalize
   technical depth itself — it builds credibility with scientists. The fix is always
   "explain the term, then go deep," never "remove the technical content."

7. EVERGREEN FRAMING  [FLAG] — Will this read correctly 12 months from now? FLAG
   "until recently / now / just shipped / today" framing unless the timestamp is the
   point, or PIECE TYPE is "aspirational" and the future tense is deliberate.

8. SENTENCE-LEVEL CRAFT  [POLISH] — Sentence fragments, "And/But" openers that hurt
   readability, misused idioms. List them briefly. These never drive the verdict on
   their own.

9. TARGET RESONANCE & PERSONAL STAKE  [FLAG] — Invert markets to individuals, not
   companies, and the win is self-recognition. As the target persona, would you read the
   first lines and think "that's me, that's what I do every day"? FLAG generic framing
   that addresses no one in particular, or that's pitched at the org/company instead of
   the person. And: is there a person-level hook — a career win (gets them promoted) or
   a "makes my daily work suck less" win? FLAG if it's all capability and no personal
   stake. Non-blocking, but this is the strategy's actual point: a piece that passes
   everything else and fails this is generic mush no one recognizes themselves in.

IF GRADING AN ASSEMBLED ARTIFACT / RENDERED PAGE (Mode B), also check:
A. ABOVE THE FOLD  [BLOCKING] — From only the first screen (hero + first lines), can a
   cold visitor tell what this is and who it's for? FAIL if the top leaves them guessing.
B. VISUAL–COPY AGREEMENT  [BLOCKING] — Do the visuals, charts, and demo match what the
   copy claims? FAIL any contradiction, or a hero that misrepresents the piece.
C. DEMO EARNS ITS PLACE  [FLAG] — Does the interactive/visual demonstrate the core
   point, or just decorate? FLAG anything that adds no understanding.
State whether you reviewed the RENDERED PREVIEW or only the SOURCE FILES.

Then output, in this order:

SCORECARD — the 9 patterns (plus the Mode B checks if applicable), each PASS/FLAG/FAIL with quoted evidence.
BLOCKING ISSUES — every FAIL on patterns 1–5, each with a one-line fix.
VERDICT — exactly one of:
  SHIP   = no blocking FAILs and at most a couple of FLAGs.
  REVISE = FLAGs, or a single blocking FAIL.
  HOLD   = multiple blocking FAILs. This almost always means the audience is wrong
           and the piece needs restructuring, not line edits.
COLD READER'S SUMMARY — as the target persona, finish honestly: "After reading/viewing
  this, I think Invert does ___; this is for someone like me because ___; and what's in
  it for me personally is ___." If you can't complete the first blank, pattern 1 FAILED.
  If you can't complete the second or third as the target persona, patterns 1 and 9
  aren't really passing, whatever the scorecard says.
```

### The read-aloud grader agent prompt (paste verbatim, with the content)

```
You are the READ-ALOUD pass for a piece of Invert writing. Your only job: read every line as if saying it out loud to a colleague, and catch what sounds machine-made or simply unsayable. You are NOT checking facts, comprehension, or strategy — only how it SOUNDS in the mouth.

TARGET PERSONA: {{the job title this targets — read as this person talking to a labmate over coffee.}}

Read the HEADLINE first, then the dek, then each body sentence. Say each in your head as speech and grade SAYS-FINE / STUMBLE / UNSAYABLE, quoting the exact line. No quote, no flag. Flag a line if:
1. BREATH — you can't say it in one breath; nested clauses or past ~25 words. Fix: split it.
2. WRITTEN-NOT-SPOKEN — words nobody says aloud: utilize, leverage, prior to, in order to, facilitate, subsequently, regarding, robust, seamless, unlock, empower. Fix: the spoken word.
3. AI CADENCE — tells a person rarely speaks but a model loves: the em-dash antithesis ("X isn't Y — it's Z"), the negation-reveal ("the loss that was never there," "the thing you can't see"), the rule-of-three ("matched, leveled, and cleared"), over-balanced parallelism. One in a whole piece is fine; a pattern of them is the flag.
4. NOUN-STACK — two+ nouns jammed together you'd slow down to parse aloud ("assay-basis mismatch penalty"). Fix: unstack into a spoken phrase.
5. TONGUE-TWISTER — awkward to actually pronounce.

THE HEADLINE IS HIGH-STAKES — it's the line most people read and the one most likely to sound generated. If it's STUMBLE or UNSAYABLE, say so loudly.

Output:
SPOKEN SCORECARD — headline, dek, then body sentences; each SAYS-FINE/STUMBLE/UNSAYABLE with the quoted line, and a one-line spoken rewrite for anything flagged.
VERDICT — SOUNDS HUMAN (at most a couple of STUMBLEs, headline fine) or SOUNDS GENERATED (headline flagged, or a pattern of AI cadence / unsayable lines).
ONE-LINE READ — finish: "Said out loud, this sounds like ___." (a person talking / a tool describing itself / a press release.)
```

## Notes on the patterns

The patterns are not equal. **Pattern 1 (Invert-context assumption) is the root** — it caused most of the reviewer's 28 comments. The "Cold Reader's Summary" line at the end is the whole skill compressed into one test: if the target persona can't say what Invert does and recognize the piece as for them, nothing else matters yet.

**The grader reads as the target persona, not a generic outsider.** It strips Invert/product knowledge but keeps the target's domain fluency — because the strategy targets a specific job title who should think "that's what I do every day," not the broadest possible reader. Always give the grader the target persona and whether the piece is shipped or aspirational. "Everyone in bioprocessing" is not a target, and grading as a generic outsider would penalize the in-domain specificity that makes a piece land.

**The cold read has one blind spot, by design.** Because the grader has zero Invert context, it cannot catch misuse of Invert's house terms — e.g. conflating *process knowledge* with *data harmonization*, or misusing *sponsor* / *biotech* vs *biopharma*. That correctness check needs Invert context, so it belongs to the exit-stage fact-check / brand-review, not here. The cold read does not cover it; don't let it imply otherwise.

**Pattern 6 carries a deliberate calibration.** The reviewer flagged the draft as "too technical" three times, and the easy lesson is "be less technical." That is the wrong lesson, and Nick said so directly: technical depth builds credibility with scientists, and Invert's audience rewards it. The actual failure was *unexplained* depth written for a reader assumed to already know Invert. The grader explains jargon; it never strips it. Encode this, don't override it. With the persona fix above, this is largely automatic: jargon is judged against what the *target* already knows, so the modality terms that define the audience (strain / cell line / vector) are never the problem — only unexplained Invert-specific terms are.

## Why a grade and not a "7/10"

Invert's review practice rejects vanity scores. The "grade" here is the **scorecard plus the gate verdict (Ship/Revise/Hold)** — not a number, not a vibe. Every FLAG and FAIL must quote the line it refers to. No line, no flag. This keeps the grade defensible against the same "what specifically do you mean?" test the content itself has to pass.

## Interaction with other skills

This skill orchestrates; it does not re-implement. Run it **last**, once a draft exists.

- **defensibility-check** — Pattern 3 is its sentence-level "what do you mean?" test. The cold read applies the gate; defer to defensibility-check for the deep, teach-Nick-the-move version.
- **content-proportion-check** — Pattern 2 leans on its Sourced / Inferred / Invented gate for product and customer claims. That skill also owns hype/proportion, which the cold read does not re-check. If a draft has a proportion problem, route there.
- **writing-craft** — Pattern 8 defers to it for the real sentence surgery.
- **brand-review / exit fact-check** — Invert house-term correctness (*process knowledge* vs *data harmonization*, *sponsor*, *biotech* vs *biopharma*) is OUT of scope for the cold read — the no-Invert-context grader can't catch it. Route house-term misuse to the context-loaded review step.

The cold read's unique contribution is the **target-persona cold-read** (domain-fluent, Invert-blind) and the **blocking gate on audience and comprehension** — the failure mode none of the other skills test for directly.

## Running in Cowork vs. Claude Code

Same skill, same SKILL.md. In Cowork it installs via Settings → Capabilities. In Claude Code it lives in `.claude/skills/blog-cold-read/` (or a plugin's `skills/` dir), and the grader runs through the Task tool, which Claude Code has. Mode B is the natural fit in Claude Code: it fires after you merge the copy and the Claude Code visual into a preview, right before you deploy.

## What this is NOT

- Not an inline editor. It grades; the orchestrator revises and re-grades.
- Not a hype/proportion checker — that's content-proportion-check.
- Not for short-form (emails, ads, decks, one-pagers).
- Not a license to strip technical depth — see Pattern 6.
- Not a visual-design or accessibility audit — Mode B judges whether the rendered page *communicates* to a cold visitor, not whether it's pixel-perfect or WCAG-compliant.

## The real outcome measure

The reviewer's volume of comments on Claude-drafted blogs should fall over time. When the cold read reliably catches what he would have caught, his review stops being a rewrite and becomes a sign-off. Track that. If it isn't trending down, the rubric is missing a pattern — add it.
