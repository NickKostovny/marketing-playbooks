# Recipe: fold a two-page signup into one page

The situation: page one makes the offer and collects an email, page two asks setup questions and shows the product. Most visitors never reach page two. You want one page that leads with the product and asks for the email last.

## 1. Inventory what the page change was doing for you

The hop between pages usually carries more than it looks like:

- **Prefilled values.** Page one passed the email to page two in the URL. Once the flow is one page, nothing needs the email in a URL, and the code that stripped it back out can go.
- **Attribution.** A plain form submit replaces the query string with the form fields, so campaign tags and ad click ids were carried across by hidden fields. On one page they stay in the address bar, and that code can go too.
- **Analytics steps.** "Reached page two" was a funnel step. Replace it with one event per question.
- **Records fired on arrival.** If page two filed a record when it loaded with a prefilled email, that trigger has to move to the email field itself.

## 2. Build the page

- Put the product visual beside the form on desktop, pinned to the top so it does not move as the form grows.
- Use an accordion: every step's header visible from the start, one open at a time, each answer folding down under its question.
- Auto-advance on a pick. Open the email step automatically once the last question is answered; a click to open it carries no decision.
- Focus the email field when its step opens, and style `:focus` so the focus is visible.
- Validate on blur. Record consent on the final submit only.

A standalone version of all of this is in [`tools/accordion-signup-demo/`](../tools/accordion-signup-demo/). Open `index.html` in a browser; no build step.

## 3. Retire the old page-two route

Keep the URL alive as a redirect to the new page. Carry every query parameter except personal data:

```tsx
// app/<flow>/setup/page.tsx (Next.js App Router)
import { redirect } from 'next/navigation';

export default async function Page({ searchParams }: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const params = await searchParams;
  const carried = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (key === 'email' || value === undefined) continue;
    for (const v of Array.isArray(value) ? value : [value]) carried.append(key, v);
  }
  const qs = carried.toString();
  redirect(qs ? `/<flow>?${qs}` : '/<flow>');
}
```

Check it returns a real 307, not a meta refresh: `curl -sI "<site>/<flow>/setup?email=a%40b.com&utm_source=x"`. If a server-side landing counter includes the old path, remove it, or every old link counts twice.

## 4. Verify without polluting the lead queue

- Run the dev server with the integrations switched off (no API keys in the local environment). Test signups then produce only a log line.
- Click through every path, including folding the step you are on, changing an earlier answer after reaching the last step, and starting over.
- Check on a 375 px viewport for horizontal overflow: long answers on one line can widen a grid column past the card. `min-width: 0` on the column fixes it.
- After deploy, check production with real clicks, and load the exact URL your QR codes encode.
