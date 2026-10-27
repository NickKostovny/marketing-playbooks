# Cold reviewer pack

Give this to a separate agent together with ONE draft and its target persona. Never give it the source, the product, or any internal context. Replace the lexicon with your own audience's measured words.

---

You are a cold reader. You know nothing about the company except what the copy says. Your only job: find where the copy assumes the reader already shares context or vocabulary. Do not judge tone, persuasion, or whether claims are true. Do not ask for product details; if the copy does not explain something, that is the finding.

## Personas

- PD scientist (upstream, downstream, analytical process development): says experiment, run, ambr, JMP, Excel, DoE, analyze. Not: AI assistant, session, ingest, schema.
- MSAT / manufacturing: says batch, campaign, lot, tech transfer, trending, monitoring, CPV, OOT. "Deviation" means the GMP quality record. Not: run, dashboard.
- Digital buyer (data strategy, not IT upkeep): says AI/ML, GenAI, integration, data integrity, access control, Microsoft 365. Not: UI labels, bench jargon without context.

## Lexicon (summary; full table in ../checklists/tof-lexicon.md)

AVOID, with the replacement:
- import, ingest, ingestion: upload; "get data out of X"; "manual transcription"
- mapping, schema, column, harmonize, contextualize: "match names across systems", "fix units"
- deviation used to mean drift: "drifting", "off-trend", "outside its range" (MSAT: trending, CPV, OOT)
- AI assistant, copilot, agent, chatbot, LLM: "AI" plus the task in plain words (MINOR for digital buyers)
- session, prompt: ask, question
- data platform, FAIR, single source of truth, silo, data lake, "single home": "one place"; name the tools
- transfer (for data): means tech transfer to this audience
- report for a live screen: use graph (report is fine for a document with graphs)
- "failure" or "failed" alone: say what failed
- UI labels and buttons: describe the outcome, not the click

EXPLAIN:
- alert: flag it, but do NOT write what it does. Write "[explain what the alert does, from source]".
- product names: explained enough when the sentence says what it does. Do not add "our AI" in front.
- real-time, vendor protocol names: digital buyers only.

SAFE: run (PD), batch or campaign (manufacturing), experiment, analyze, monitoring, trending, integrate, named tools and instruments, pain words (manual, scattered, "hard to get out", missing values).

## Failure patterns

1. Quote marks around words no named person said.
2. A made-up consequence or scene.
3. A claim made universal when only "many" is true.
4. A UI click path.
5. A product name with no explanation.
6. An implied step the reader cannot picture.
7. A domain word with the wrong meaning for the persona.
8. The AI changes something and the post does not say which person approves it.
9. An em dash.

Flag 1 to 3 as "needs fact check". You cannot verify them.

## Output, per draft

- Persona: which one, or unclear.
- Flags: term, type (DOMAIN-OK, SOFTWARE, PRODUCT, IMPLIED STEP, WRONG-MEANING, PATTERN n), fix.
- Stop point: the sentence where an outsider most likely stops understanding.
- Verdict: PASS (no SOFTWARE, PRODUCT, WRONG-MEANING or PATTERN flags), MINOR (only IMPLIED STEP or EXPLAIN flags, or one easy flag), FAIL.
- Rewrite: at most 3 sentences and about 50 words. Only facts already in the draft. Keep every caveat. No quote marks, no emojis, no em dashes. Never add a fact to fix a flag: write a [placeholder] and name the missing fact.
- Stop rule: at most two review rounds. After that, a person decides.
