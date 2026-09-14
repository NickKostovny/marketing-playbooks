# Prompt: competitor content-gap analysis, five blog ideas

The brief that produced this playbook, with names replaced by placeholders. Give it to an agent that has an SEO MCP (keyword metrics, ranked keywords per domain, live SERPs) and, if you have one, a product knowledge base MCP. The two rules at the end are the part that matters.

---

## Context

{{COMPANY}} ({{DOMAIN}}) is {{ONE-LINE DESCRIPTION}}. Readers: {{ROLES}} at {{COMPANY TYPES}}. Content direction: {{DIRECTION, e.g. "integrations plus AI, not AI alone"}}.

## Inputs

- SEO tool: {{TOOL}}
- Competitors: {{LIST OF DOMAINS, one per line, with one phrase on where you meet them}}
- Limits: {{MARKETS}}, {{LANGUAGE}}

## Steps

1. Get each competitor's top pages and ranking keywords.
2. Get {{COMPANY}}'s ranking keywords. Run the keyword gap.
3. Score each candidate 1 to 5 on winnability (keyword difficulty against {{COMPANY}}'s authority), reader fit, and direction fit. Label the gap type: keyword, topic, or quality.
4. Select the top five. Remove any idea with no source data.

## Output

`slack.md`: one Slack message for {{DECISION MAKER}}. Lead with the ask. Then five ideas, one line each: title, gap type, volume, KD, why {{COMPANY}} wins. No tables. Under 150 words.

`data.md`: scores, API sources, removed ideas, missing data.

## Rules

- Do not invent numbers. Cite the API call for each figure.
- Flag missing data. Do not estimate.

---

## Notes from running it

- "Cite the API call for each figure" only works if every call's input and output is saved. The toolkit's call-log script does that from the session transcript after the fact, but it is simpler to save as you go.
- Add a third rule if your tool distinguishes dataset positions from live ones: label every position by source.
- Add the gap-type definitions to the brief so the agent does not invent its own: keyword (topic covered, term not targeted), topic (no page), quality (page exists, competitor's ranks, yours does not).
