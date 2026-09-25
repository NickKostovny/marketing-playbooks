# Checklist: launching a gated recording

Every line here is a mistake I made or nearly made on the first one. Run it in order.

## Before you write a word

- [ ] Open the actual file. Probe its duration. Read the video host's metadata title. Compare both against what you were told. Do not describe a video from its filename or from its host title alone.
- [ ] Decide the page's long-term home now: campaign URL, blog post, or library entry. Build there. Add the short campaign URL as a redirect, not as the page.
- [ ] If anyone outside the company appears in the recording, ask for consent to cut and post clips today. Hold their clips until the answer is yes.

## Capture flow

- [ ] The capture sink has its own database base. A new table inside an existing base inherits that base's automations. A test submit will fire them.
- [ ] The route reads only its own environment variables, with no fallback to another flow's variables.
- [ ] Every sink is switched on by its own variables, so the page can ship before every downstream owner is ready.
- [ ] Fail closed: on a capture error the content stays locked.
- [ ] Alerts fire on sink failure only, unless the owner asks for more. Nobody wants a message per view.
- [ ] Secrets are entered from a normalised file, never pasted into a chat or a terminal history. See `recipes/secret-env-from-a-file.md`. Check for a byte-order mark.
- [ ] Sensitive variables cannot be read back or pulled locally. Plan a redeploy and a live test on a preview or on production.

## The page

- [ ] The work-email rule is stated on the page, next to the field, before the visitor types.
- [ ] Honeypot present. Opt-in boxes unchecked by default. Same-origin check and a body-size cap on the route.
- [ ] The newsletter opt-in uses double opt-in on the newsletter side.
- [ ] Structured data omits the embed URL for gated videos. No transcript on the page.
- [ ] The redirect from the campaign URL keeps the query string, so the source tag survives.
- [ ] If the page adopts a design that the rest of the site does not, scope it with a wrapper class and put the token block last in the stylesheet. Then check the footer and header against the approved preview after the merge, because sitewide token changes will leak in.

## Embed

- [ ] Domain-level embed privacy is on at the video host, with the production domain listed. See `recipes/vimeo-domain-lock.md`.
- [ ] The player URL loaded directly in a fresh browser shows a privacy notice, not the video.
- [ ] Accept that preview and review copies on other hosts no longer play the video. That is the lock working.

## Merge and ship

- [ ] Run a merge dry run, then also check the pull request page. End-of-file appends to a shared file conflict without showing up in a hunk-level dry run.
- [ ] Verify on production, not on a preview: locked render, personal-address refusal message, unlock with a work address, redirect with tag, one database row with every field, no alert fired.
- [ ] Delete the test rows.

## Distribution

- [ ] Clips end on a card that states the full length, the work-email requirement, and the short URL.
- [ ] The page link goes in the first comment of each LinkedIn post, not in the body.
- [ ] Posts for an external speaker's clips carry a blocking approval on the relationship owner. Everything else can ship on silence.
- [ ] Decide what you will measure after week one, and check that the route records it. Refusals were not recorded on the first one.
