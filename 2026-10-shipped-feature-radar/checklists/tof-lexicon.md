# Top-of-funnel lexicon for bioprocess buyers (v1, Oct 23 2026)

This list tells you which words a bioprocess reader who has never used the product already shares with us, and which words they do not.

## Evidence base

| Source | N | What it measures | Main bias |
|---|---|---|---|
| Public web (job posts, trade press, talks) | 63 practitioner docs (41 job posts) | How non-users write | Job-post genre under-reports everyday data chores; Reddit blocked |
| Customer support chats and in-app feedback | 261 customer items, 17 orgs, 2024-09 to 2026-10 | How users write | Users echo the product's UI labels; problem-heavy; 3 orgs give more than half the items |
| Call transcripts | 51 read, 13 external speakers (5 customers) | How people talk | Small N; mostly the marketer's calls, few sales calls |
| CRM | 329 rep-written records, 231 companies | Rep paraphrase only | Not customer voice; calls/notes API returned Forbidden |
| ICP job postings | 121 postings, 51 companies (39 from the CRM target list, 12 lookalike); big pharma 54, CDMO 32, CGT 20, mid-size 15 | How our buyers' employers describe the work | Job-post genre; 89 of 121 are scientist roles; counts are lower bounds (±10–15%) |

**v1.1 (ICP job postings) agrees with the generic web scan on import, transfer, report, deviation, mapping and platform words.** New: CDMOs say batch and campaign; PD says experiment; early-warning words are monitoring (25%), trending (12%), CPV (12%), OOT (3%); value is stated as decisions, robustness, yield, right-first-time.

**Confidence rule.** High: 2 or more independent sources agree, and one of them is a non-user source. Medium: one strong source, or the sources do not agree. Low: fewer than 5 uses in total.

## Word list

| Our word | Verdict | Use instead | Evidence | Confidence |
|---|---|---|---|---|
| ingest, ingestion | AVOID | upload; "get data out of X into one place" | Web 0/63 (95% CI 0–6%); Call transcripts 1/13 external speakers (a trained customer); Support chats 3 natural uses | High |
| import | AVOID in TOF | upload; "manual transcription", "export and re-enter" | Web 0/63 (0–6%); Support chats users say upload in 12/17 orgs vs import in 6/17, and import there means the job status ("my import is stuck") | Medium (genre bias) |
| mapping, schema, column, tag | AVOID | "match names across systems", "fix units", "clean up" | Support chats harmonize/standardize 0/261; web mapping 3/63, data roles only | High |
| harmonize, contextualize, standardize | AVOID | "inconsistent naming between sites/systems" | Support chats 0/261; Call transcripts: our staff only | High |
| deviation (to mean drift) | AVOID | "drifting", "off-trend", "outside its range"; for MSAT: trending, CPV, OOT, excursion | Web 22/63 and ICP jobs 33%, always the GMP quality record (investigation, CAPA); Call transcripts: always GMP | High |
| alert | EXPLAIN | "know when a run leaves its range"; "let someone know" | Web 1/63; Call transcripts external speakers 0/13; Support chats 0/261 | Medium (low N) |
| alarm | CAREFUL | Same as above. It carries control-system baggage ("nuisance alarms") | Web 4/63 | Low |
| monitoring, trending | USE | (same) | Web 16/63 and 14/63, core MSAT verbs | High |
| real-time | CAREFUL | OK for the digital persona; scientists did not say it | Call transcripts: staff only; CRM: rep text | Medium |
| run | USE for PD; say batch or lot for manufacturing | (same) | Support chats 13/17 orgs; Call transcripts: confusion with manufacturing people | High |
| bioreactor | USE; vessel name is better | "ambr 250", "the 2L", "tank" | Support chats users name the vessel | Medium |
| analyze, analysis | USE | (same) | Web 39/63 | High |
| report | USE only for a written document | (same) | Web 34/63, always a written document (tech report, CPV report) | High |
| dashboard | AVOID | graph | Support chats 1 use; graph 16 > plot, chart | Medium |
| AI assistant, copilot, agent, chatbot, LLM | AVOID | "AI" plus the task in plain words ("ask questions of your run data") | Web 0/63 for assistant and copilot; skeptical tone; Support chats: "the AI" | High |
| Product names | EXPLAIN on first use | say what it does in the same sentence | Product word | High |
| session, prompt | AVOID | ask, question | Web 0/63 (0–6%) | High |
| approved import, a "Fix with AI" button, other UI labels | AVOID | Describe the outcome, not the click | UI-only | High |
| MCP, vendor connector names, read-only tools | AVOID for scientists; OK for digital buyers | "connects to <tool> using each person's own access" | Cold-read: software terms | Medium |
| data platform, FAIR, single source of truth, silo | AVOID | "one place"; "scattered across Excel, Benchling, SharePoint" | Web: vendors only; Support chats 0; CRM 0 | High |
| integrate | OK | (same) | Web 9/63; CRM 33 companies | Medium |
| Excel, JMP, Benchling, SharePoint, ambr, paper batch records | USE | Name the tool, not the category | All four sources | High |
| manual, transcription, scattered, "hard to get out", "missing", "off by a factor of 10" | USE as pain words | (same) | CRM manual 53 companies; Support chats trust words | High |

## Known gaps (to raise N)

1. Sales-call recordings. CRM calls, meetings and notes returned Forbidden; re-authorize the connector. This is the largest source of prospect voice we have not read.
2. Practitioner forums (Reddit blocked by the proxy) and LinkedIn comments.
3. GMP and CDMO users are thin in every source.
4. Web quotes came through a model-assisted fetch. Check each quote at its URL before using it in copy.
