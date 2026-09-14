---
name: skill-audit
description: >
  Governs writing, editing, compressing, merging, splitting, or deleting skill files in this library,
  including inside skill-creator runs. Trigger on "audit my skills", "fix this skill", "compress this
  skill", "should these be merged", "write a new skill", "why didn't that skill fire", "this skill isn't
  helping", or when Nick reports bloated or over-templated output he can't trace to a source. Not for
  using a skill to do its job.
---

# Skill Audit

The library was built against an older baseline. The binding constraint has moved from capability to
salience: I can do the work, but competing directives, prescribed shapes, and expository prose degrade it.

**The test for every line: could I have produced this without being told?** If yes, it costs attention
rather than adding it. Skills earn tokens by carrying what only Nick knows — decisions, constraints,
sources of truth, taste, exemplars — not by teaching me how to work.

## Answer this before editing anything

**Does this skill exist to change my output, or to change Nick's thinking?**

Some files are notebooks Nick wrote to think with, that I read as instruction sets
(`hamming-taste-principles` is explicitly a research log). Compressing one of those and demoting its
reasoning to `references/` optimizes it for me and destroys it for its actual primary reader. The two
purposes want opposite treatment, so resolve this first. If it serves both, split it.

## Two layers, very different costs

| Layer | When it loads | Discipline |
|---|---|---|
| **Description** | Every turn, every skill, always | The expensive layer. Trigger signals plus one boundary clause. Budget ~400 chars. No rationale, no advocacy, no restating the body. |
| **SKILL.md body** | Only when the skill fires | Cheap by comparison. Compressing here saves tokens that were only spent when the skill was relevant. |

Never fix a body-layer problem by growing a description. Precedence rules belong in the body of whichever
skill owns the trigger, not in the always-resident layer.

## Classify — wrong class means opposite prescription

| Class | Purpose | Prescription |
|---|---|---|
| **A — Rails** (`gtm-rules`, `product-source-of-truth`, `deal-update`) | Stop me doing something plausible but wrong | Imperative, absolute, short. **Verify every tool name against the live toolset** — a rail naming a dead tool has absolute authority and sends me nowhere. Stale rails are worse than missing ones. |
| **B — Taste** (`content-proportion-check`, `writing-craft`, `linear-write-cleanup`) | Transfer Nick's standard | Decisions and discriminating tests in SKILL.md; reasoning in `references/`. Compress **after** benchmarking, never on the strength of an argument. |
| **C — Producers** (`case-study`, `cx-demo-brief`, `morning`) | Reliably build an artifact | Keep format prescription — a real consumer needs it. Deterministic steps → `scripts/`. |
| **D — Coaching** (`strategy-decisions`, `learning-medium`) | Change Nick's thinking, not the output | State explicitly: **the output is a question, not a document.** Otherwise co-firing Class B converts it into a report about coaching. |
| **E — Meta** (`skill-creator`, `schedule`, `setup-cowork`) | Operate the system | Leave alone unless asked. |

Mixed-class files get split — they get swallowed by whichever half fires louder.

## Rules

1. **Verify tool names.** Any skill naming a tool gets its references checked against the live toolset.
   Tool names drift; skills don't notice. This is the highest-severity defect class in the library.

2. **Verify, don't flag.** An instruction to "flag this for Nick" that a live tool could close is a tax
   charged on every fire. `search_calls` and `get_call_transcript` can source a practitioner claim; links
   can be fetched. Convert flag-and-report into verify-then-report.

3. **One trigger, one owner.** Grep the library before adding trigger phrases. On collision, prefer
   deduplication and narrowing over merging — a merged skill inherits the union of trigger surfaces and
   fires on a superset of signals. Merge only when both skills would return the same verdict. If you claim
   a precedence order, write it out; naming the fix is not the fix.

4. **Templates: measure, don't assume.** Prescribed sections cut both ways — they invite filler when I have
   nothing real for a slot, and they prevent omission by forcing enumeration. For a skill whose job is
   catching what's missing, omission is the costlier error. Keep format where a downstream consumer needs
   it (a HubSpot field, a .docx layout, a doc read cold). Elsewhere, benchmark before removing.

5. **Provenance is one line.** Name the source so we share vocabulary; don't re-teach the framework.

6. **Write in the register you want back.** Skill prose primes output prose. A file about concision written
   expansively argues against itself.

7. **Earn "always."** Proactive-override language only where genuinely unconditional. When a third of the
   library claims priority and none states rank, the word does nothing.

8. **One verification line.** "Before returning, check X." Cheapest quality gain available.

9. **Verify adversarially.** For any substantial skill edit or audit claim, spawn a fresh-context agent to
   fact-check it against the actual files. Self-review does not catch this class of error — a
   well-evidenced-looking audit can be wrong in most of its specifics and look right from the inside.
   `blog-cold-read`'s zero-context grader is the pattern.

A longer rubric with worked examples stays in the private library; the classes above cover most edits.

## Measure instead of arguing

`skill-creator` ships the harness: `scripts/run_eval.py`, `scripts/aggregate_benchmark.py`,
`agents/grader.md`, `eval-viewer/generate_review.py`. It runs with-skill against baseline in parallel and
reports pass rate, tokens, and time.

Nothing here has been baseline-tested against the current model, and baseline is what moved. **A skill
whose with-skill result matches baseline is pure cost.** Do not set line-count targets by aesthetics; the
non-derivable content sets the floor, and measurement finds it.

## Before returning any skill edit

State the class, the description-length delta and body-length delta separately, what was cut and where it
went, and which trigger phrases now collide with which other skills. If a cut removed something
non-derivable, say so and put it back.
