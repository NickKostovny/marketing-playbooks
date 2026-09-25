# Gating a webinar recording: "The gap between collecting process data and using it"

**Live:** https://invertbio.com/university/process-data-gap. The short link `invertbio.com/process-data-gap` redirects there and keeps its source tag.
**Shipped:** September 23, 2026. Brief September 21. One owner review round and one design pass in between. The LinkedIn sequence that points at it starts after this write-up.
**Type:** A 94-minute webinar recording (two talks and the audience Q&A) behind a work-email form, housed in our video library, with seven cut clips and a scheduled LinkedIn sequence to send people to it.

## The brief

We ran a webinar on September 16 with a process-monitoring and data lead at a large pharma manufacturer and our head of product. I had the recording. The brief to Claude Code was: gate it behind a form, share it on LinkedIn today, collect emails, and let people raise a hand for a walkthrough. Look at how the site already does this sort of thing, plan it, and tell me what you need from me.

"Today" did not happen. The page took three days, and the reasons are most of this log. What I got is a reusable gated-content pattern in the site, a capture flow that lands where sales can act on it, and a cutting tool for the next long recording.

## Step 1. Decide what the gate is for

A gate costs you viewers. It only pays when the people who get through are the people you want to talk to, and when what you learn about them is usable. So the first decisions were about the ask, not the page.

**Work email only, and say so.** The buyer for a bioprocess data platform works at a manufacturer or a CDMO. A personal address gives sales nothing to act on, and the newsletter list gets a subscriber we cannot qualify. The form refuses the common personal and disposable domains and the page says so before you type: "Gmail, Outlook, Yahoo and similar addresses are not accepted." Saying it up front saves the visitor a failed submit and saves me a bounce complaint.

**Unlock on the page, not by email.** Most gated-content flows email you the link. That couples the reward to email deliverability and to the visitor checking their inbox. Here the form submits, the server records the lead, and the player appears in place. The email is the price, not the delivery channel. A returning visitor stays unlocked in that browser.

**One optional hand-raise, as a checkbox.** "I would like a walkthrough with the Invert team." Not a second form, not a calendar embed. The checkbox is the whole ask. A second, unchecked box offers the newsletter, with double opt-in.

**Fail closed.** If the capture request fails, the video does not unlock. A gate that opens on error is not a gate.

## Step 2. Where the leads go, and how spam is kept out

The capture route writes one record per submit and fans it out. Every sink is independent and switched on by its own environment variables, so the page could ship before every downstream owner had done their part.

| Sink | When | Status at ship |
| --- | --- | --- |
| Server log line | Always | On. The audit trail if everything else is down. |
| Spreadsheet database (Airtable), its own base | Always when configured | On and verified with a live test row, then deleted. |
| CRM form submission | When the form GUID is set | Off. Owed by the CRM owner. Optional. |
| Newsletter subscription | Only when the visitor ticks the box | Off. Owed by the newsletter owner. Double opt-in when on. |
| Team chat alert | Only on a sink failure | Off by owner decision. |

The last row was a decision, not an omission. The first plan pinged the team on every unlock. The owner's answer was that nobody wants a chat message every time someone watches a video; capture it in the database and let people look. So the chat webhook now fires only when a sink fails, which is the one case where a human should act now.

The spam posture is layered and has no CAPTCHA. A CAPTCHA on a B2B form punishes the exact visitor you want. Each layer catches a different thing, and none of them is visible to a real person except the blocklist message:

- **Work-email blocklist**, checked server side as well as in the form.
- **Honeypot field**, hidden from people, filled by bots, silently rejected.
- **Same-origin check and a 4 KB body cap** on the route.
- **Opt-in boxes unchecked by default**, so a bot that ticks everything is still not a consent.
- **Double opt-in on the newsletter**, so the list only gets addresses that confirmed.

The full list, with what each layer does and does not catch, is in [checklists/capture-form-spam-posture.md](checklists/capture-form-spam-posture.md).

The same email filter and the same newsletter hook then went into the product trial sign-up form, so both capture flows share one posture. The trial form only subscribes on a completed sign-up with the product-updates box ticked.

## Step 3. Where it lives on the site

The page was first built at a campaign URL, `/process-data-gap`, because that is what a LinkedIn post needs: short, and memorable enough to type from a video end card. Then came the question of where it belongs long term. Three options:

1. **A campaign landing page.** Fast, but an orphan. Nothing links to it after the campaign, and the next recording needs another one.
2. **A blog post with the video in it.** Findable, but the blog pipeline is Markdown, and a form that unlocks a player does not fit a Markdown body.
3. **An entry in the video library.** The library already had talk pages, video cards, category chips, and structured data for videos. A gated talk is a talk with a lock.

The library won, on one condition from the owner: it had to make visual sense. So the library entry got a `gated` flag and a `chapters` list. The talk page renders a locked poster with a "Work email to watch" chip and the form beside it, then swaps in the player. The video card shows the same chip in the grid. The structured data omits the embed URL for gated videos, because the point of the gate is that the player URL is not public. There is no transcript on the page for the same reason.

In place of a transcript, the page carries an "In this session" list: seven chapters with timestamps, written to make someone want the whole 94 minutes without giving the talks away. The prompt that produced them is in [prompts/chapter-list-from-transcript.md](prompts/chapter-list-from-transcript.md).

The campaign URL survived as a redirect to the library page, and the redirect keeps the `?s=` source tag, so `invertbio.com/process-data-gap?s=linkedin` still tells me where the visitor came from.

## Step 4. The look

The site was mid-way through a design system revision, and the owner had seen a version of this page on the new system in a parallel session. The decision: "I like the design system copy better. Let's run with that."

Restyling the whole site for one page was not on the table. So the new system is scoped: the talk page wraps its content in one class when the video is gated, and a token block for that class sits at the end of the global stylesheet. Everything else on the site keeps its current look. Two things this cost:

- **The footer.** The footer's hairlines were inline styles, which the scoped class could not override, so they moved to CSS classes first. Then a separate pull request the same week changed the site's root colour tokens, and the footer on the gated page picked those up. The page now matches the approved preview in 21 of 22 measured properties. The footer ground is the one difference, and whether to pin it is an open call.
- **A build tool gotcha.** The CSS minifier drops `backdrop-filter: none`, so a reset that relies on it does nothing. Write the value you want instead of `none`.

## Step 5. Cut the clips

The full recording is gated. The clips are the free sample, and each one ends on a card that says how long the full session is, that it needs a work email, and where to get it.

Seven clips came out of the transcript: four from our head of product, on trust in AI for manufacturing data, what to ask a vendor, why "is the model validated" is the wrong question, and agentic root-cause analysis with a human in the loop; three from the external speaker, on scoring a manufacturing network, why data maturity is not digital transformation, and vendor continuity. The external speaker's three are cut, branded, and **held** until they consent to being clipped. A webinar appearance is not consent to a stand-alone video with their face on it.

Cutting is done on word timings, not on a scrubber. For each clip I gave a rough in and out point and the phrase the clip should start and end on. The tool transcribes a window around the rough points with whisper.cpp, finds the phrases in the word offsets, extends the end to the close of the sentence, cuts there, and writes word-grouped subtitles. A second script frames the cut in a 1080 by 1080 square with a title card in, a speaker line, burned-in subtitles, an end card out, and speech normalised to -14 LUFS. Both scripts are in [tools/clip-cutter/](tools/clip-cutter/) and run as published; the title and end cards in [assets/](assets/) came out of the published version.

Two things the transcript taught me: the small speech model mishears domain terms ("GP context" for "GMP context"), so the tool takes a fixes list; and whisper's control tokens leak into the word stream if you do not strip them, which is how `<|endoftext|>` nearly ended up burned into a subtitle.

## Step 6. The owner review: three decisions

The review round did not change the copy much. It changed the plumbing. Three decisions from the owner, each of which reversed something I had built:

1. **A new database base, not a new table.** I put the test table inside the base the trial sign-up flow uses. A test submit fired that base's automation, which is wired to the sales team. The fix was a dedicated base for gated content, and the route now reads only that base's variables with no fallback to the trial base. The lesson generalises: a table inherits the automations of the base it sits in, so a capture flow gets its own base or it is not isolated.
2. **No alerts on unlock.** Covered above. Capture, do not interrupt.
3. **Lock the embed.** The player URL has to be a client prop to render, so it sits in the page payload where a determined visitor can read it. The gate is a form, not a vault. What closes the gap is Vimeo's domain-level embed privacy: the video only plays inside pages on our domain. Loading the player URL directly now shows a privacy notice, and the preview copies on other hosts stopped playing, which is the correct trade. The steps, with the labels as they read at the time, are in [recipes/vimeo-domain-lock.md](recipes/vimeo-domain-lock.md).

The LinkedIn side was set up in the scheduling tool in the same round: one main post pointing at the page, one post per clip scheduled over the following three weeks, comments on each explaining what the clip is, and the page link in the first comment rather than the body. Approvals were removed, then re-added as non-blocking requests, with one exception: the external speaker's clips carry a blocking approval on the person who owns that relationship, so they cannot go out by silence.

## Step 7. What went wrong, and the checks it became

**I wrote copy for the wrong video, twice.** The first file I was pointed at was a 3-minute demo reel, and I described it from its filename. The corrected link was a different 3-minute cut, and I described it from its title on the video host. The recording was the 94-minute session. Every duration, chapter, and description had to be redone. The check now: read the video host's metadata for the title and duration, and probe the file, before writing a word.

**A byte-order mark became part of a secret.** The database token was handed over as a text file exported from a notes app, which prepended a UTF-8 BOM. Piped into the hosting CLI, the BOM became the first three bytes of the stored secret, and the sink returned 401 on production. Sensitive variables cannot be read back, so this took a redeploy and a live test to find. The recipe that came out of it strips line endings, checks the token's shape, and pipes the file in: [recipes/secret-env-from-a-file.md](recipes/secret-env-from-a-file.md).

**The merge conflicted where the dry run said it would not.** My branch and another both appended to the end of the global stylesheet. A merge-tree dry run showed nothing, because it reports conflicts by hunk and end-of-file appends land in the same hunk. The pull request page showed the conflict. Resolution was manual: the other branch's block first, then the gated and scoped-system block last, since the scoped tokens have to win.

**A review copy on a personal hosting project returned 500.** Creating the project from the CLI without a framework set deployed it as a generic Node app, and the middleware did not run. Setting the framework on the project fixed it. The review copy is a real deploy of the branch with every secret removed, so anyone with the link can see the page and submissions go nowhere.

All of these are now lines in [checklists/gated-recording-launch.md](checklists/gated-recording-launch.md).

## Step 8. Ship

One pull request, squash-merged on September 23 after the conflict resolution. Verification on production, not on a preview:

- The library page renders locked, the form refuses a personal address with the on-page message, and a work address unlocks the player.
- The short link redirects to the library page and the `?s=` tag survives the redirect.
- A live test submit landed as one row in the gated-content base with every field populated, and the test rows were then deleted.
- No chat alert fired on the unlock.
- The player URL, loaded directly in a fresh browser, shows Vimeo's privacy notice.

The CRM and newsletter sinks are dormant until their owners set the two remaining variables. The route already handles both.

## Results so far

The page has been live since September 23. As of this write-up on September 25 the LinkedIn sequence has not started, so there is no real submission to report. The test rows were deleted. What I will check after the first week of posts:

- Unlocks, and the share with the walkthrough box ticked.
- Where they came from, by `?s=` tag: LinkedIn post, clip posts, newsletter.
- How many visitors were refused on a personal address. The route returns that refusal to the form but does not record it, which is the first thing I would add.

## What I would do differently

1. **Watch the recording, or at least read its metadata, before writing anything.** Two rounds of copy went in the bin because I trusted a filename and then a title.
2. **Create the capture base before the first test submit, and never test in a base that has automations.** Isolation is a property of the base, not the table.
3. **Ask the external speaker for clip consent the day the webinar ends.** The clips were cut before the ask, so three of seven are sitting in a queue.
4. **Decide the page's long-term home before building it.** It was built as a campaign URL and moved to the library two days later. The redirect makes that invisible to visitors, but the move cost a day.
5. **Record refusals.** A count of personal-address attempts is the only measure of whether the blocklist is costing real leads.
