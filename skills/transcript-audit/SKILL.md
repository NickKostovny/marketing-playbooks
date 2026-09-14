---
name: transcript-audit
description: >-
  Audit a raw, auto-generated transcript for likely mis-transcriptions and
  return a grouped list of catches to fix — it does NOT rewrite the transcript.
  Use this whenever Nick pastes a transcript from a recorded call, interview,
  talk, webinar, or podcast and wants errors caught — especially when the
  speaker has a strong or non-native accent, since those produce predictable
  phonetic mishearings. Trigger on phrases like "audit this transcript,"
  "clean up this transcript," "catch the errors," "did the transcription
  mishear anything," "one more audit," "review this transcript," or simply a
  long pasted transcript with a request to check or fix it. Strongly biased
  toward bioprocessing / RNA / mRNA manufacturing content and Invert Bio
  terminology, where domain jargon gets garbled the same way every time
  (HEPES→"heapy-space," dsRNA→"double-standard," oligo-dT→"oligodity"). Use it
  even when Nick doesn't say the word "skill" or "audit" — if a raw transcript
  is being checked for transcription errors, this is the tool.
---

# Transcript Audit

## What this does and why it works

Auto-transcription errors on accented speech are not random. They are **phonetic
substitutions**: the transcriber hears the right sounds and picks the wrong
words. In a technical talk this hits the domain jargon hardest, because the
transcriber has no model for "HEPES" or "oligo-dT" and falls back on common
English ("heapy-space," "oligodity"). Two things make these highly catchable:

1. **A domain lexicon.** The same terms get mangled the same way across every
   recording. `references/lexicon.md` holds the known mishearing → correct-term
   mappings plus the RNA/bioprocess and Invert terms most likely to be garbled.
2. **Context clues.** The transcript usually contains its own answer key. A
   term mangled in one place often appears correctly elsewhere; a defined
   acronym gets used later; a number is restated. Internal consistency is your
   strongest tool — lean on it before the lexicon.

This skill produces an **audit list**, not a cleaned transcript. Nick applies
the fixes himself (often in a separate editor). Do not rewrite the transcript
unless he explicitly asks — the job is to surface catches he can act on fast.

## Method

1. **Read the whole transcript first.** Do not audit top-to-bottom on first
   pass. Later passages disambiguate earlier ones (a buffer named "heapy-space"
   at minute 20 is confirmed by "conjugate bases for HEPES" at minute 40).
2. **Cross-check against the lexicon.** Read `references/lexicon.md` and scan
   for its entries. Treat it as a checklist of usual suspects, not a limit —
   catch anything that fits the phonetic-substitution pattern even if it's not
   listed.
3. **Run consistency checks.** Flag internal contradictions: numbers that don't
   match a value stated elsewhere, an acronym defined one way and used another,
   a term spelled two ways. These catch the errors the lexicon can't.
4. **Classify each catch by confidence** (see Output). The single most
   important discipline: **fix what context proves; flag what you can't
   verify.** Never silently "correct" a proper noun.
5. **Leave disfluencies alone.** Stutters, false starts, and filler ("the the,"
   "two two two," "um") are left verbatim — Nick keeps the transcript faithful
   to the recording. Note in one line that they remain; do not itemize them.

## Output format

Return a grouped list. Quote the **exact heard text** in each entry so Nick can
find-and-replace directly. Keep entries to one line of "why" — the reasoning is
what lets him trust or overrule the catch. Use this structure:

```
**Technical / domain terms** (high confidence — misheard jargon)
- "heard text" → correction — one-line why (usually the context clue)

**Meaning errors** (wrong word or dropped word that changes the meaning)
- "heard text" → correction — what it does to the meaning

**Verify — can't confirm from the text** (names, products, instruments, figures)
- "heard text" → best guess (if any) — why it's uncertain + what to check against

**Punctuation / run-ons** (only if egregious or if Nick asks)
- brief note

**Disfluencies**
- One line: left verbatim per your default; note they remain if a clean read is wanted.
```

If a section has no catches, drop it. Lead with the substantive tiers
(Technical, Meaning) — those are what Nick acts on first.

## The two rules that matter most

**Context is the answer key.** When a term appears both mangled and correct in
the same transcript, the correct instance is ground truth: fix the mangled ones
to match and note the inconsistency. When a number or claim contradicts one
stated elsewhere, flag the contradiction and say which value the surrounding
context supports. These internal-evidence catches are more reliable than any
lexicon and are the ones a human skim misses.

**Flag, don't guess, on anything you can't verify.** Speaker and company names,
product names, instrument makes/models, citations, and specific figures cannot
be recovered from audio-driven text alone. Offer a best guess when you have one,
but mark it clearly and tell Nick what to check it against (his slides, notes,
the attendee list). Silently "fixing" a name is worse than flagging it — it
launders an error into something that looks confident.

## Worked examples

**Example 1 — context-clue fix (Technical):**
Input: "commonly used buffers in IVT are heapy-space or tree-space buffers"
Output: `"heapy-space or tree-space" → HEPES or Tris` — later the speaker says
"conjugate bases for HEPES" and "we can do it for Tris," which confirms both.

**Example 2 — consistency catch (Meaning):**
Input: "40 species for the full model and 50 species for the simplified model"
Output: `"50 species for the simplified model" → 15` — everywhere else the
simplified (Henderson-Hasselbalch) model is 15 species and the kinetic model is
40; "50" contradicts the rest of the talk. Worth confirming against the slide.

**Example 3 — flag, don't guess (Verify):**
Input: "we just used a tiny pH probe, a five-rotic pH probe"
Output: `"five-rotic pH probe" → likely "fiber-optic pH probe"` — fits "tiny"
and fiber-optic pH microsensors exist, but it's a specific instrument that
can't be confirmed from the text. Check the slide/notes before trusting it.

**Example 4 — dropped word (Meaning):**
Input: "a lot of automation which would / the number of operators needed"
Output: `insert "reduce"` → "automation which would **reduce** the number of
operators" — a verb dropped out; the sentence is incomplete without it.

## Growing the lexicon

The lexicon is the compounding asset here — each recording surfaces a few new
mishearings worth saving. When Nick confirms a new mapping (or gives you Invert
product/people/competitor names to watch for), offer to add it to
`references/lexicon.md`. If this skill is installed and read-only, note that he
can ask you to regenerate an updated `.skill` package with the additions.
