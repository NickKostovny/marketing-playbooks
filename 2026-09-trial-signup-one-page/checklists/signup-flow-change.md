# Checklist: changing a lead-capture flow

Use before and after any change to a signup, trial or gated-content form. Each item comes from something that went wrong, or nearly did, on this rebuild or the flow before it.

## Before you edit

- [ ] List every record the form sends, and when (on blur, on submit, on refusal). This is your parity table.
- [ ] List every ad-platform or analytics event, and the guard that keeps each one from double counting.
- [ ] Find where attribution travels: query parameters, hidden fields, cookies. A plain form submit or a page change can drop the whole query string.
- [ ] Decode every printed QR code and list every link that points at the page. Changing a URL breaks print you cannot recall.
- [ ] Check what the live product actually does before you borrow its words ("Log in", "workspace", "account").

## While you build

- [ ] Retire an old route with a redirect that keeps attribution parameters and drops personal data (an email in a query string).
- [ ] Store the page URL with an allowlist of tracking parameters, not the raw address bar.
- [ ] Record terms acceptance only on the final submission, never on partial records.
- [ ] Show field errors after the person leaves the field, never mid-typing. Clear them when they return.
- [ ] If code moves focus, give the field a visible `:focus` style of its own. Browsers often skip the default ring for script focus after a mouse click.
- [ ] A folded step must stay clickable even if unanswered. Never leave a state where nothing can be clicked.
- [ ] No copy promises what the operation cannot deliver. If a person fulfils the request, the confirmation says so, with the real timeframe.

## Before you merge

- [ ] Run a multi-lens adversarial review ([prompt](../prompts/four-lens-review.md)).
- [ ] Test locally with the integrations switched off, so test signups never reach the queue a person works from.
- [ ] Check conflicts against every open pull request that touches the same files, not just against main.

## After you ship

- [ ] Verify on production: the new page, the redirect, and the exact URL your QR codes encode.
- [ ] Test focus and keyboard behavior with real clicks. Script clicks can leave the window unfocused and give false results.
- [ ] Confirm which system sends each notification (email, chat alert) before you switch any of them off.
- [ ] Note the date the analytics events changed, so before-and-after comparisons start there.
