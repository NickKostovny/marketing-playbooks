# Recipe: a gated-content pattern that unlocks on the page

Platform-neutral. Ours is a Next.js site, but nothing here depends on it.

## Shape

```
registry (slug -> title, embed URL, duration)
   |
   v
gate component (poster + form)  --POST-->  capture route  --fan out-->  log
   |                                              |                     database
   v                                              |                     CRM form (optional)
player (only after {ok: true})                    |                     newsletter (only if opted in)
                                                  +--on sink failure--> team chat
```

## Registry

One object per asset, keyed by slug: title, embed URL, human duration. The page reads its asset by slug. The registry is the only place the embed URL lives in source.

## Form

- Work email, required. Name, optional. One checkbox for the hand-raise, one for the newsletter, both unchecked.
- The work-email rule is printed under the field before the visitor types.
- Hidden honeypot field with a plausible name.
- Remember the unlock in local storage under `gated:<slug>` so a returning visitor is not asked twice. Read it with a store subscription, not by setting state inside an effect, or the lint rule fires.
- The submit button carries an analytics attribute so the click is countable.

## Capture route

Accepts JSON, refuses anything else. In order:

1. Same-origin check. Body under 4 KB.
2. Honeypot filled: return `{ok: true}` and do nothing. Bots should not learn they were caught.
3. Email regex, then the personal-domain blocklist. Refusal: `{ok: false, error: "personal_email"}`. The form shows the on-page message.
4. Build one record: timestamp, asset slug, email, name, hand_raise, newsletter, source (from the page's `?s=` tag), CRM tracking cookie, page URL.
5. Write the log line. Always.
6. Fan out to each configured sink. Each sink is gated on its own environment variables and skips with a logged warning when they are missing.
7. If any sink threw, post the failure to the team chat webhook, if configured.
8. Respond `{ok, hubspot, airtable, newsletter}` with a boolean per sink.

The form unlocks only on `ok: true`. Any other response leaves the poster in place with a message.

## Sinks

| Sink | Variables | Notes |
| --- | --- | --- |
| Database (Airtable) | token, base id, table name | Its own base. Read only these variables, with no fallback to another flow's. Field names as typed in the base, `typecast: false` so a wrong field name fails loudly. |
| CRM form (HubSpot) | form GUID | Submit the standard fields plus the tracking cookie and page URL. |
| Newsletter (beehiiv) | API key, publication id | Only when `newsletter` is true. `double_opt_override: "on"`, no welcome email, UTM fields set to the site, the form, and the source tag. |
| Team chat (Slack) | webhook URL | Failure only. |

## Page

- Locked state: poster, duration, a chip that says "Work email to watch", the form.
- Unlocked state: the player iframe with autoplay, fullscreen, and picture-in-picture allowed, strict-origin referrer policy.
- Structured data: a VideoObject with name, description, duration, thumbnail, upload date. **No embed URL** for gated videos.
- No transcript on the page.
- The campaign short URL is a redirect to the page that preserves the query string.

## Embed lock

The embed URL is a client prop and therefore readable in the page payload. Lock the video at the host to your domain so the URL is useless outside your pages. See `vimeo-domain-lock.md`.
