# Checklist: spam posture for a B2B capture form

No CAPTCHA. A CAPTCHA on a B2B form punishes the visitor you want and stops the least sophisticated bots only. Layer instead. Each layer catches a different thing, and each one is invisible to a real person except the first.

| Layer | Where | Catches | Does not catch |
| --- | --- | --- | --- |
| Work-email blocklist, with the rule stated on the page | Form and server | Personal and disposable addresses, and the honest visitor who would have typed one | A bot with a real corporate-looking domain |
| Honeypot field, hidden by CSS, named like a real field | Form and server | Form fillers that populate every field | Bots that read the DOM for visibility |
| Same-origin check on the route | Server | Direct POSTs from scripts and other sites | A script that spoofs the header |
| Body-size cap (4 KB) | Server | Payload stuffing | Small junk |
| Opt-in boxes unchecked by default | Form | Consent inflation from bots that tick everything | Nothing else; this is a consent control |
| Double opt-in on the newsletter | Newsletter platform | Every unconfirmed address, human or not | Nothing on the lead side; the lead record still exists |
| Fail closed on capture error | Server and form | A gate that opens when a sink is down | Nothing; this is a correctness control |
| Failure-only alerting | Server | Silent sink outages | Nothing about spam; keeps humans out of the loop for normal traffic |

Two things this posture does not do, on purpose:

- **It does not block on a "free-mail" API or a paid verification service.** The static list covers the common providers. A paid verifier adds latency to every submit and a dependency to every unlock.
- **It does not rate-limit by IP.** Corporate networks share egress addresses. A rate limit would lock out the second person at the same manufacturer.

Record refusals. A blocklist that refuses a hundred addresses a week is either working or costing you leads, and you cannot tell which without the count.
