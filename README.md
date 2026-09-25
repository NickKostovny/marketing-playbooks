# Marketing playbooks

How I ship marketing work in 2026, with the reasoning, the tools, and the reusable parts.

I am the one-person marketing function at a bioprocess data company. Most of what I ship is built with Claude Code, a set of MCP connectors, and a handful of custom skills. The finished piece goes on the company blog or LinkedIn. This repo holds what those channels cannot show: the decisions, the checks, and the tooling.

## How to read a playbook

One folder per shipped piece. Every folder has the same shape.

| Path | What it is |
| --- | --- |
| `README.md` | The ship log. Goal, gap, decisions, what review changed, result, what I would do differently. |
| `tools-used.md` | Every MCP, skill, and script used, and what each one did. |
| `prompts/` | Grader and generator prompts, sanitized so you can run them. |
| `checklists/` | Review gates that came out of the work. |
| `recipes/` | Step-by-step procedures for a tool or a platform. |
| `tools/` | Small scripts. Each has its own README. |
| `assets/` | Public artifacts only. |

## Index

| Shipped | Piece | Type |
| --- | --- | --- |
| 2026-09-24 | [Rebuilding a free-trial signup: one page, product first, email last](2026-09-trial-signup-one-page/) | Conversion-flow redesign. Two pages into one, accordion steps, a four-lens adversarial review before merge, fixes from a live-page review |
| 2026-09-18 | [Turning old LinkedIn ad engagement into an SDR handoff without burning enrichment credits](2026-09-linkedin-ad-engagers-to-sdr/) | Sales-enablement data. 18 ads, 222 people, two free gates before any paid lookup, seven lookups instead of two hundred, one workbook with a Read me tab |
| 2026-09-23 | [Gating a webinar recording behind a work-email form](2026-09-gated-webinar-recording/) | Gated video in the site's video library. Unlock on the page, fail-closed capture to an isolated base, no CAPTCHA spam posture, domain-locked embed, seven word-timed clips |
| 2026-09-14 | [What is OPC UA, and how do bioreactors use it?](2026-09-opc-ua-explainer/) | Definitional SEO explainer, product-grounded, reviewed by a PM, generated card thumbnail |
| 2026-09-22 | [Rebuilding a conference one-pager on a new design system](2026-09-bpi-one-pager/) | Two-sided booth handout. Pattern-removal audit, one job per side, measured print output, print-shop bleed pass |
| 2026-09-09 | [Deciding what to write next: a competitor content-gap analysis](2026-09-competitor-content-gap/) | Decision memo from SEO data. Nine competitors, one keyword gap, five ideas scored, every number cites its API call |

## Skills library

The playbooks run on a library of Claude skills: Markdown files with a trigger description and a body of decisions, tests, and constraints. The public subset lives in [`skills/`](skills/), 16 of them, grouped as the operating system for the work, marketing judgment, and thinking and people. Each playbook's `tools-used.md` names the ones it used.

## Rules I hold myself to here

- Nothing from customer calls, internal knowledge bases, deal data, or private repos. Colleagues appear as roles, not names.
- Every claim in a ship log is something I could show you the tool output for.
- The reusable parts run as published. If a script needs a licensed asset, the public version swaps in a free one and says so.

Start a new entry from [`TEMPLATE/`](TEMPLATE/).

## License

Code, prompts, and checklists are MIT licensed. Artifacts in `assets/` are shown for reference and belong to the company that published them.
