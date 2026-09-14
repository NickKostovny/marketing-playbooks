# Redaction notes

What changed between the private skill library and this public copy, described by kind. The line-level log with the original text stays private, because a diff of a redaction is the redaction undone.

Source: the synced skill library on 2026-09-14. Files not listed below are byte-identical to the private copy.

## Left out of the public set

- Company operational work product: skills that write to the CRM, build customer briefs and case studies, generate branded artifacts and product videos, draft outreach from call transcripts, and gate product claims against the internal product hub. Ten skills.
- Anthropic-authored skills that ship with Claude: document, spreadsheet, slide, and PDF tooling, memory import, morning routine, skill creator.
- Internal meeting transcripts and handoff files.
- Four skills held back for a decision, not for a leak: one marketing framework whose tone in two lines needs a second look before it represents me publicly, and three that describe my own working habits in the second person.

## Kinds of changes in the published files

| Kind | What was done | Files touched |
| --- | --- | --- |
| People | Named executives and colleagues became roles ("a senior reviewer," "the reviewer") | blog-cold-read, and the observed-preferences section of writing-craft |
| Customers | Named customer sites and accounts became generic descriptors ("a CDMO customer," "a large biopharma customer") | brand-marketing-framework (held), hamming-taste-principles, idea-to-brief, content-proportion-check |
| Customer individuals | A named scientist used as a test persona became an unnamed role | brand-marketing-framework (held), hamming-taste-principles |
| Internal files | References to specific transcripts and handoff documents in my working folders were removed | brand-marketing-framework (held), idea-to-brief |
| Prices and commercial detail | A price point and a deal-specific detail were removed | brand-marketing-framework (held) |
| Internal channels | A named paid channel became "the paid ads campaign" | idea-to-brief, session-state, portable-handoff |
| Stale tool names | A dead tool reference became a generic one; a stale "no Linear MCP" paragraph was generalized | learning-medium, linear-write-cleanup |
| Placeholders | "[Competitor]" placeholders left by an earlier pass became plain descriptions | idea-to-brief |
| Precedence | The decision that `portable-handoff` wins over `session-state` was added to `session-state` itself, not only the README | session-state |

## Left in on purpose

- References to private skills by name (`gtm-rules`, `product-source-of-truth`, `deal-update`, `case-study`, `cx-demo-brief`, `messaging-from-calls`, `brand-review`). The README says this is a subset; the names are pointers.
- Internal tool names for call search and transcript retrieval. They describe how a gate works, not what it found.
- Public product names and the cloud provider. Neither is confidential.
- Anonymized customer stories where the point is the lesson, not the account.
