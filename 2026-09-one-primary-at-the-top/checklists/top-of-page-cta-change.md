# Checklist: changing the CTAs at the top of every page

Use this before you change a nav button or an announcement bar. Each item comes from something that went wrong, or nearly did, during this change.

## Before you decide

- [ ] Paste the actual review thread into the working session. Build from what was said, not from what you remember.
- [ ] Count every entry point: desktop nav, mobile menu, bar, heroes, footer. Check that each one sends an analytics event and a source tag.
- [ ] Keep click evidence and outcome evidence apart. Clicks can point one way while completed signups and booked meetings point the other.
- [ ] Find where each CTA's traffic really comes from. Our nav sent 5% or fewer of trial-page visitors, and paid ads sent most of them.
- [ ] Check a sample of peer sites before you argue about convention. Record the date, the viewport and what you could not render.
- [ ] Before you propose a test, run the power check ([`tools/power-check/`](../tools/power-check/)). Put the duration in days next to the proposal.

## While you build

- [ ] One primary button at a time. Never show two equal filled buttons.
- [ ] The bar never repeats a nav CTA while both are visible.
- [ ] Decide dismissal before first paint. No server read if pages must stay static, and no removal after hydration.
- [ ] Set the dismissal cookie from a server response, so Safari keeps the full max-age.
- [ ] Give each new placement its own source tag. Do not rename existing tags, because reports depend on them.
- [ ] List the edge pages: the booking page, the trial page, its terms page, and campaign pages that have their own nav. Write a rule for each one.
- [ ] Run the offset audit for sticky elements, anchors and drawers.

## Before you merge

- [ ] Test every state: bar visible, closed in the session, closed before load, after Back, a page without a bar, phone width, and a mid-width screen where the nav could wrap.
- [ ] Test tracking with the site's real CTA selector if analytics is off in development.
- [ ] Run a production build and confirm which pages are static.
- [ ] Run an adversarial state-matrix review ([prompt](../prompts/state-matrix-review.md)).

## After you ship

- [ ] Check the live HTML for the bar, the source tags and the swap rules, on at least one page of each type.
- [ ] Record the date the change went live, so later comparisons start there.
- [ ] Agree a read date and a removal rule before the numbers come in.
