# Moving one page across four design contexts

The same page lived, in one day, as a standalone mock, a Claude Design handoff, a canvas port from the marketing site, and a route in the site's Next.js app. The tokens never changed. The way rules reached elements changed every time. This is what to expect at each boundary.

## 1. Standalone mock to standalone mock

Keep one finished standalone page per design system as the seed for the next. Copy its stylesheet, swap the content, ship. This boundary costs nothing, which is the reason to maintain the seed.

## 2. Claude Design handoff to HTML

A Claude Design doc-page source is a spec, not code. Expect:

- A custom element wrapper and a helmet block. Discard both.
- Template holes (`{{name}}`) and a loop tag (`<sc-for>`). The data they loop over sits in a class method at the bottom of the file. Lift the data into plain markup.
- Inline styles on every element. Read them into named classes on your tokens. The handoff's values are the spec; the inline form is not.
- Placeholders for the wordmark and photos. Replace with the real assets; the handoff author could not see them.
- A placeholder link in brackets. Never guess the real one.

Port the layout, spacing and colours closely. Resist rewriting copy during the port; reviewers cannot then tell which change they are reacting to.

## 3. A React canvas component to plain JavaScript (and back)

Marketing-site figures are often React client components that draw on a canvas and import a composition helper (where the figure sits in its hero). To reuse one in a standalone page:

- Keep geometry, random seeds, opacities and speeds byte for byte. The figure should be indistinguishable from the site's.
- Replace only the composition (centre and scale relative to the host) and the lifecycle (a resize observer on the host, an intersection observer that pauses the frame loop off-screen, reduced-motion respected).
- Mount it in a positioned host box with an explicit minimum height. The canvas is absolutely positioned inside it.
- Hide it below the width where the layout stacks. A decorative canvas pushing content down on a phone is worse than no canvas.

Going back into the site, the plain port becomes a copy of the original component with the composition change, wrapped in a client-only dynamic import so it never server-renders.

## 4. Standalone page into a site with a global stylesheet

The site's global stylesheet styles elements (`a`, `h1`, `p`, `img`). A scoped block appended to it has to win against those rules. Three things to expect:

- Leads, labels and captions need `!important` on colour and weight. The earlier campaign pages in the repo already do this; copy their pattern rather than fighting it.
- A styled link loses to the scope's own link rule. `.scope a { color: ink }` has higher specificity than `.scope-button { color: white }`. Write `.scope a.scope-button`.
- Anything with state or browser APIs (a scroll-triggered iframe, a canvas) becomes a `'use client'` component. Lift the iOS touch shield and the scroll trigger from the previous campaign page rather than rewriting them.

Metadata: noindex and nofollow, a canonical, and the shared Open Graph helper so the title and description unfurl in chat tools. The sitemap should not discover the route; check.

## The constant

Six colours, one line weight, one radius scale, one font stack. Decide those once in the design system and every boundary above becomes a mechanical port instead of a design decision.
