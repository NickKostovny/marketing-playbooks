# Recipe: a dismissible top bar on every page of a static site, with a nav CTA swap

This recipe puts a dismissible announcement bar on every page, keeps every page static, and gives the nav one primary button at a time. Nothing shifts or flickers. The examples use Next.js App Router and React 19, but the mechanism is plain HTML, CSS and one inline script.

Names are generic. Rename `promo_bar`, `data-promo-bar` and `--promo-bar-h` to suit your site.

## The problem

- **A server check makes the page dynamic.** If the server reads the dismissal cookie, the page must render per request. That is why our first version was on the homepage only.
- **A client-side check causes a jump.** If the page renders the bar and then removes it after hydration, the whole page moves up by the bar height on every load.
- **A bar above a fixed nav moves everything down.** Every sticky element and anchor that clears only the nav now ends up under the nav.

## 1. Decide before first paint

Put a one-line script first in `<body>`, before the nav markup. It reads the cookie and marks `<html>`.

```ts
// lib/promo-bar.ts
export const PROMO_COOKIE = 'promo_bar';
export const PROMO_CAMPAIGN = 'trial-2026q3'; // change this to show the bar to everyone again
export const PROMO_OFF_ATTR = 'data-promo-bar';

export const PROMO_STATE_SCRIPT =
  `try{if(document.cookie.split('; ').indexOf('${PROMO_COOKIE}=${PROMO_CAMPAIGN}')!==-1)` +
  `document.documentElement.setAttribute('${PROMO_OFF_ATTR}','off')}catch(e){}`;
```

```tsx
// app/layout.tsx
import { PROMO_STATE_SCRIPT } from '@/lib/promo-bar';

// suppressHydrationWarning: the script can add an attribute before hydration.
<html lang="en" suppressHydrationWarning>
  <body>
    <script id="promo-bar-state" dangerouslySetInnerHTML={{ __html: PROMO_STATE_SCRIPT }} />
    <main>{children}</main>
  </body>
</html>
```

Store the campaign id in the cookie value, not in the cookie name. When you change `PROMO_CAMPAIGN`, every old cookie stops matching, so everyone sees the bar again and no old cookie stays behind.

## 2. Set the cookie from the server, readable

Safari caps cookies that JavaScript writes at seven days. A cookie set by a server response keeps its full max-age, so the dismiss button calls a small route:

```ts
// app/api/promo-bar-dismiss/route.ts
import { NextResponse } from 'next/server';
import { PROMO_COOKIE, PROMO_CAMPAIGN } from '@/lib/promo-bar';

export async function POST() {
  const res = NextResponse.json({ ok: true });
  res.cookies.set({
    name: PROMO_COOKIE, value: PROMO_CAMPAIGN,
    maxAge: 60 * 60 * 24 * 30, path: '/', sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
    httpOnly: false, // the pre-paint script must read it; it holds only a campaign id
  });
  return res;
}
```

If the cookie was httpOnly before this change, JavaScript cannot read the old cookies. Those visitors see the bar once more. We accepted that.

## 3. Hide the bar, and set the offset, with CSS only

```css
html:has(.promo-bar):not([data-promo-bar="off"]) { --promo-bar-h: 44px; }
html[data-promo-bar="off"] .promo-bar { display: none; }
body { padding-top: var(--promo-bar-h, 0px); }
nav  { position: fixed; top: var(--promo-bar-h, 0px); }
html { scroll-padding-top: var(--promo-bar-h, 0px); } /* every in-page anchor at once */

/* Without :has() the offset never applies, so hide the bar there. */
@supports not selector(:has(*)) { .promo-bar, html .nav-cta-demo { display: none; } }
@media print { .promo-bar { display: none; } html { --promo-bar-h: 0px !important; } }
```

With no bar on the page, the variable falls back to `0px`, so those pages look exactly as they did before the change.

## 4. The nav swap

Put both buttons in the HTML, and let CSS show one of them:

```html
<a href="/demo"            class="btn nav-cta-demo">Book a demo</a>
<a href="/trial?s=nav"     class="btn nav-cta-trial">Try it free</a>
```

```css
/* Bar visible: the bar carries the trial, so the nav shows the demo. */
html:has(.promo-bar):not([data-promo-bar="off"]) .nav-cta-trial { display: none; }
/* Bar closed, or not on this page: the nav shows the trial. */
html:not(:has(.promo-bar)) .nav-cta-demo { display: none; }
html[data-promo-bar="off"] .nav-cta-demo { display: none; }
```

Keep each `:has()` rule on its own. Browsers drop the whole rule when one selector in a list is invalid. Set only `display: none`, so each button keeps its own display value in the nav and in the mobile menu.

Give pages that need a fixed nav their own rule. Our booking page has no bar, so the swap would have offered the trial there. The nav component checks the path, and on that page it renders only `<a href="/demo" class="btn">Book a demo</a>`, with no swap class and no trial button.

## 5. The bar component

```tsx
'use client';
import { useState, useSyncExternalStore } from 'react';
import { usePathname } from 'next/navigation';
import { PROMO_COOKIE, PROMO_CAMPAIGN, PROMO_OFF_ATTR } from '@/lib/promo-bar';
// sourceSlug is defined in step 6.

const HIDDEN_ON = ['/trial', '/trial-terms', '/demo']; // don't advertise the page you are on

// Backup for the <html> mark: re-read the cookie after hydration and on pageshow,
// which fires when Back restores a page from the back/forward cache.
const subscribe = (cb: () => void) => { addEventListener('pageshow', cb); return () => removeEventListener('pageshow', cb); };
const readDismissed = () => { try { return document.cookie.split('; ').includes(`${PROMO_COOKIE}=${PROMO_CAMPAIGN}`); } catch { return false; } };

export default function PromoBar() {
  const pathname = usePathname() ?? '/';
  const [hidden, setHidden] = useState(false);
  const dismissed = useSyncExternalStore(subscribe, readDismissed, () => false);

  function dismiss() {
    setHidden(true);
    // Client-side navigation does not re-run the layout script, so mark <html> now.
    document.documentElement.setAttribute(PROMO_OFF_ATTR, 'off');
    void fetch('/api/promo-bar-dismiss', { method: 'POST', keepalive: true }).catch(() => {});
  }

  if (hidden || dismissed || HIDDEN_ON.some((p) => pathname === p || pathname.startsWith(`${p}/`))) return null;
  return (
    <div className="promo-bar">
      <span>Try the product free.</span>
      <a href={`/trial?s=${sourceSlug(pathname)}`} className="promo-bar-link">Try it</a>
      <button type="button" onClick={dismiss} aria-label="Dismiss" data-track="promo-dismiss">×</button>
    </div>
  );
}
```

Render the bar from the nav component, not from the root layout. Then every page with the site nav gets it, and campaign pages that have their own nav do not.

## 6. One source tag per page

```ts
// The homepage keeps the original tag, so existing reports still work.
function sourceSlug(pathname: string): string {
  const seg = pathname.split('/').filter(Boolean)[0]?.toLowerCase() ?? '';
  const slug = `banner-${seg}`;
  return seg && /^[a-z0-9-]{1,40}$/.test(slug) ? slug : 'banner';
}
```

Check that every value passes the validation your signup endpoint applies to the source parameter. Ours rejects anything that is not a short lowercase slug.

## 7. The offset audit

Before you ship, search the CSS and any inline styles for:

- `position: sticky` or `position: fixed` with a `top` value
- `scroll-margin-top`, `scroll-padding-top` and `scrollIntoView` offsets
- `calc(100vh - …)` with a nav height inside
- drawers and overlays that are positioned from the top
- `IntersectionObserver` root margins in table-of-contents components

Add `var(--promo-bar-h, 0px)` to each one. For example, `top: 80px` becomes `top: calc(80px + var(--promo-bar-h, 0px))`. Then open every page type with the bar visible, and check that each sticky element's computed `top` is at or below the nav's bottom edge.
