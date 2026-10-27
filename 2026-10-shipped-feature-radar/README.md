# Shipping a feature radar: from what engineering shipped to LinkedIn posts an outsider can read

**Shipped:** 2026-10-26. A scheduled task, a word list built from about 1,300 outside sources, a cold reviewer, and a fact checker. Three test rounds in one day.
**Type:** Marketing operations system. Turns an engineering "shipped" channel and a project tracker into a ranked digest with one suggested LinkedIn post per feature. Grounded only in the engineers' own posts.

## The brief

Engineering ships faster than I can tell people about it. I wanted a system that reads what shipped every two weeks, picks what customers would care about, and drafts a post for each pick. The drafting tool (a social-media AI with our brand voice loaded) was the obvious engine. The open question was what has to sit between "an engineer posted it" and "a post goes out."

## Step 1. The first version, and why it failed

The first pass took three shipped features, had the drafting tool write posts from the engineers' text, and put them in the review tool. It was fast and, read by me, fine.

Then I read them as someone who has never used the product. Every post assumed the reader knew our screens and our words: "approved ingestion", "mapping", "open session", a button name. The drafting tool's own brand rule ("lead posts with a quote") also made it wrap an engineer's internal words in quote marks, so they read like a customer quote.

Decision: the drafts are not the problem to solve. The missing piece is a reader with no context.

## Step 2. Measure the vocabulary instead of guessing it

A cold reviewer is only as good as its idea of how the audience talks. So I measured it before writing the reviewer. Four agents ran in parallel, then a fifth on target-account job posts:

| Source | N | Measures | Bias |
|---|---|---|---|
| Target-account job postings | 121 postings, 51 companies | How buyers' employers describe the work | Job-post genre; mostly scientist roles |
| Public practitioner writing (jobs, trade press, talks) | 63 documents | How non-users write | Job posts dominate; forums were blocked |
| Customer support chats and in-app feedback | 261 items, 17 orgs | How users write | Users repeat our UI labels |
| Call transcripts | 51 read, 13 outside speakers | How people talk | Small N |
| CRM notes | 329 records | Rep paraphrase only | Not customer voice; counted separately |

What came back, with confidence (95% Wilson intervals where N allows):

| Our word | Finding | Verdict |
|---|---|---|
| import, ingest | 0 of 63 public docs (0 to 6%); 0 import, 1 ingest in 121 job posts. Users say "upload" (12 of 17 orgs vs 6 of 17 for "import") | Avoid |
| deviation | 35% of public docs and 33% of job posts, always the GMP quality record | Never use it to mean drift |
| transfer | Means tech transfer in 45% of job posts | Never use it for moving data |
| report | A written document in 78 of 84 job-post uses | Fine for a document, wrong for a live screen |
| AI assistant, copilot | 0 of 63 docs; AI words in 3 of 89 scientist job posts, 6 of 12 digital roles | Say what the AI does |
| session | 0 of 63 docs | Avoid |
| data platform, single source of truth, silo | Vendor pages only | Avoid |

The full table is in [`checklists/tof-lexicon.md`](checklists/tof-lexicon.md). Two numbers I trusted less than they looked: "alert" was rare everywhere (low N), and the first agent's claim that customers never say "alert" came from two tool calls. That is why I asked for a much larger N before arming the reviewer.

## Step 3. Two reviewers who must not share context

- **Cold reviewer.** Gets only the draft, a persona, and the word list. No product knowledge, no source. If the copy does not explain something, that is the finding. See [`prompts/cold-reviewer-pack.md`](prompts/cold-reviewer-pack.md).
- **Fact checker.** Gets the rewrite and the engineer's original post. Judges meaning, not words. See [`prompts/fact-check-pack.md`](prompts/fact-check-pack.md).

Keeping them apart matters. A reviewer with the source fills the gaps the reader cannot fill.

## Step 4. Test the reviewers like code

| Test | Result |
|---|---|
| Regression: 10 earlier drafts with known problems | 9 FAIL, 1 MINOR. Caught every known problem: made-up quotes, invented consequences, UI click paths, "deviation" meaning drift |
| Same 4 features, new brief template | 2 FAIL, 2 MINOR (from 9 of 10 FAIL). The drafting tool still invented two lines ("giving time back to science", "then hunt for them"); the reviewer caught both |
| Fact checker on the 4 rewrites | 4 of 4 needed a fix. Two unsupported claims came from my own brief, not the tool. Two material caveats had been dropped: a customer billing step, and that the fix only covers uploads you approved |

Bugs found in my own packs during testing:
1. I put an unconfirmed fact into the word list ("alert = a run leaves its range"). The reviewer copied it into rewrites. Fix: the reviewer may never add a fact; it leaves a `[placeholder]`.
2. The fact checker pushed copy back to internal words ("blocks", "dataset"). Fix: a list of approved plain-language translations.
3. The reviewer failed drafts forever on small unclear steps. Fix: those count as MINOR, and there are at most two review rounds.

## Step 5. The review that changed it

- **Head of product** shared a regulatory read: draft EU Annex 22 says AI can advise but cannot make critical GMP decisions alone. One of my posts said the AI fixed things "unasked." That is the wrong story for this buyer. Fix: a who-approves check. If a post says the AI changes something, it must say which person approves the change; if the engineer's post does not say, the engineer gets asked before the post goes out.
- **Me, reading the shared digest:** the boilerplate "X is our AI for that data" was redundant. Now the AI is introduced by what it does in that sentence. Also: no em dashes anywhere.
- **Sharing the digest with the company** pulled the discussion toward post wording instead of the system. The shared version now leaves the posts out; the digest I get still has them.

## Step 6. Ship

A scheduled task, every other Monday. It reads the shipped channel and the tracker (last 14 days), filters out infrastructure and security work, ranks by "can a customer see it, does it fix a known pain, can it be demoed", and runs each of the top five through: brief, draft, cold review, fact check, who-approves. Output: a shared doc and a short email to me. The task may create drafts in the drafting tool, but cannot publish, schedule, request review, or write in chat or the tracker. Prompt in [`prompts/radar-scheduled-task.md`](prompts/radar-scheduled-task.md).

## Results so far

- First digest: 5 picks. 2 posts passed both checks. 2 still FAIL after two review rounds and wait on an engineer's plain-words answer. 1 waits on who approves the AI's change. 4 tracker projects with real work and no shipped-channel post were flagged as "ask eng for the why"; the largest had about 45 closed issues.
- No outcome record yet. Countable from 2026-11-09 (the first scheduled digest) via a "Radar" label on every post that came from the system, and a radar campaign tag on each post's first-comment link, read in the web analytics and CRM source fields. First read 2026-11-23. Two posts already carry the label.

## What I would do differently

1. Wire the outcome tag before the first post, not after. The label exists; the campaign tag on links still depends on me adding it when I post, so the first count will be partial.
2. Measure the vocabulary first, then build. I built the first posts, then the reviewer, then measured. The first two rounds of posts were wasted on words the data would have ruled out.
3. Get one reader outside the company to read five radar posts cold. Every review so far is internal: my agents, my head of product, me. That is internal review, not proof that an outsider understands.
