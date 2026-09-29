# Claim audit table

Every factual sentence in the draft gets one row before any review gate runs. The table is the evidence the graders and the reviewer check against, and it is what you open when someone asks "where does that number come from?" six months later.

Run it in a fresh agent that did not write the draft, with the draft, the research notes, and the source URLs. Then re-read every row marked anything other than `Sourced` yourself.

## The columns

| Column | What goes in it |
| --- | --- |
| `claim_id` | C1, C2, and so on, in the order the claims appear. Keep the id when a claim is reworded. |
| `claim` | The claim in ten words or fewer. Not the full sentence. |
| `type` | `concept` (domain knowledge), `number` (a figure, threshold, or table value), `regulatory` (what a regulator or standard requires), `attribution` (a quote or "X says"), `product` (what your product does), `customer-context` (what practitioners do or say), `math` (arithmetic in a worked example). |
| `source` | `external`, `call`, `product`, `math`, or `none`. |
| `locator` | Where exactly: section number, table name, quoted string, or feature entry. Precise enough that someone else finds it in a minute. |
| `refetch` | `yes` (fetched again for this audit, and the words or number are there), `no`, `blocked` (the page would not open, with the status code), or `n/a` (math or reasoning). |
| `grade` | `Sourced`, `Inferred` (reasoning, and hedged in the copy with "usually" or "often"), `Unsourced`, `Unreachable`, or `Contradicted`. |
| `disposition` | `keep`, `reword`, `hedge`, `cut`, or `cite another source`. Add what changed and why when a review moved it. |

## Rules

- An `Unreachable` source is never cited, even when you remember what it says. Find a source you can open or cut the claim.
- A `regulatory` claim needs the regulation's own text. For a claim that a document does *not* say something, search the full text for the term and record the zero in `locator`.
- An `attribution` claim traces to the original. A threshold that everyone quotes usually came from somewhere specific; find where.
- A `product` row cites the product's own source of truth, and only for what ships today. If the source of truth has no entry, the copy says so or the claim goes.
- A `customer-context` row needs a call, a survey, or a published source. An empty call search means no customer voice in the copy, not a paraphrase from memory.
- Every `math` row is recomputed in code, not by eye.
- A row fixed after review stays in the table. Its disposition records the history.

## Prompt

```
You are auditing every factual claim in a draft before it goes to review. You did not
write it. You have the draft, the author's research notes, and the source URLs.

1. Go through the draft sentence by sentence. Every sentence that states a definition,
   a formula, a number, a threshold, a requirement, an attribution, a product
   capability, or what practitioners do gets one row. Skip pure transitions.
2. For each row, fill: claim_id | claim | type | source | locator | refetch | grade |
   disposition, using the vocabulary below. Fetch every external source again. Record
   the status code when a page does not open.
3. Recompute every number in a worked example in code and show the result.
4. For every claim that a regulation or guidance does NOT name something, search the
   full text for the term and record the number of matches.
5. Do not grade a claim Sourced from memory. If you could not open it, it is
   Unreachable.

type:        concept | number | regulatory | attribution | product | customer-context | math
source:      external | call | product | math | none
refetch:     yes | no | blocked (status) | n/a
grade:       Sourced | Inferred | Unsourced | Unreachable | Contradicted
disposition: keep | reword | hedge | cut | cite another source

Output:
TABLE: one row per claim, in draft order.
NOT CLAIMED, ON PURPOSE: capabilities or facts the research touched that the draft
correctly leaves out, one line each, with why.
ACTION LIST: every row that is not "Sourced, keep", with the exact sentence and the fix.
```

## Example rows from the Cpk explainer

Public sources only. The full table had 24 rows.

| claim_id | claim | type | source | locator | refetch | grade | disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | Cpk = distance to nearer limit / 3 sigma | concept | external | NIST/SEMATECH e-Handbook 6.1.6 | yes | Sourced | keep |
| C8 | Worked example: Cpu 1.11, Cpl 1.67, Cpk 1.11, Cp 1.39 | math | math | recomputed in code; labeled illustrative in the copy | n/a | Sourced | keep |
| C10 | One result per batch: within sigma from the moving range | concept | external | individuals-chart method, average moving range / 1.128; Steiner, Abraham, and MacKay | n/a | Sourced | keep (rewritten after a blocking review finding) |
| C12 | FDA process validation guidance names no index or threshold | regulatory | external | FDA 2011 guidance, section IV.D; full-text search for Cpk and Ppk, 0 matches | yes | Sourced | keep |
| C13 | 1.33 and 1.67 come from automotive supplier practice | attribution | external | Steiner, Abraham, and MacKay, citing AIAG | yes | Sourced | keep |
| C14 | Cp 1.33 is about 64 per million outside the limits | number | external | NIST 6.1.6 table (NIST lists 1.66, not 1.67) | yes | Sourced | keep |
| C18 | Purity and impurity data near a bound are often skewed | concept | none | statistical reasoning | n/a | Inferred | keep, hedged "often" |
| C24 | No built-in Cpk index today | product | product | internal product source of truth, feature entry | yes | Sourced | keep, stated in the copy as the limit |
| (none) | Two professional-body pages from the research | attribution | external | both returned HTTP 403 | blocked (403) | Unreachable | not cited; nothing in the post rests on them |
