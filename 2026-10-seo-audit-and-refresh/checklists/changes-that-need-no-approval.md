# SEO changes: approval or not

A working rule for a one-person team. The test is "can this change a claim or a date?"

## Ship without approval (metadata and links only)

- Shorten page titles over about 60 characters. Keep the main phrase first.
- Shorten meta descriptions over about 160 characters to one sentence.
- Fix a duplicate H1 (demote the second to H2).
- Add internal links from new posts to older high-ranking posts, and back.
- Remove duplicate or text-only addresses from the sitemap.

Conditions: one weekly batch, one pull request, no body copy, no dates, no changed addresses.

## Needs a second pair of eyes

- Any sentence that makes a product claim, number, or comparison.
- Any change to the web address of a page that ranks.
- Any change to `date`, `featured`, or whatever the site sorts by.
- A new post. Run it through your normal review.

## Before any refresh

1. What does the index page sort by? Do not touch that field.
2. Is there an `updated` field? If not, record the refresh date in the pull request and add the field later.
3. Keep the address. A changed address loses the ranking.
4. Add the page to the rank tracker the same day, so there is a before and after.

## After shipping

Open the live page. Check the title, the date, and the page source for structured data. Do not stop at a green preview.
