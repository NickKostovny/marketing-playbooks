# State-matrix review of a top-of-page CTA change

A CSS-driven swap has many states, and most of them are invisible in a normal click-through. This prompt gives one reviewer the full matrix and tells it to refute the change. I ran it as a single agent after each build, and a second agent ran the production build in parallel.

## Shared context block

Fill in the braces.

```text
READ-ONLY review. Do not edit files, commit, push, or start servers.
Repo: {{path}}. Diff: git diff {{base}} HEAD -- .
Framework: {{framework + version}}. Read the bundled docs for version-specific behaviour.

INTENT:
The nav shows ONE solid button. "{{demo CTA}}" while the bar (.{{bar class}}) is visible;
"{{trial CTA}}" (link with ?s={{nav tag}}) once the bar is dismissed ({{html attribute}}="off",
set before first paint by an inline script and again by the dismiss handler) or not rendered
(hidden on {{routes}}). The swap is pure CSS.

KNOWN FACTS (do not re-litigate):
- {{pre-existing lint errors or issues on main}}
- {{accepted costs, e.g. old httpOnly cookies re-show the bar once}}
```

## The task

```text
Try to REFUTE that the change is correct. For EACH state below, say which CTAs are visible
(desktop nav and mobile menu), and whether exactly one is visible:

1. Bar visible, first load
2. Bar dismissed before this load (cookie present, attribute set by the inline script)
3. Bar dismissed in this session (component unmounted, attribute set by the handler)
4. Page where the bar is hidden by route
5. Bar removed after hydration by the component's own cookie check
6. Page restored from the back/forward cache after a dismissal on another page
7. Browser without :has() support
8. Print

Then check:
- Selector specificity against every rule that sets display on the buttons, including
  responsive @media rules and any scoped theme overrides.
- Sibling-margin rules in the mobile menu that assume two visible buttons.
- The modal-trigger attribute on the demo button still works.
- The analytics CTA selector matches both buttons, and each one sends its own tag.
- Hidden buttons leave the tab order and the accessibility tree.
- Any page where the swapped-in CTA is wrong for the page's job (e.g. the booking page).
- Anything else in the repo that references the old buttons: tests, docs, e2e selectors.

Report each issue with file:line, severity (blocker/major/minor), a concrete failure
scenario, and the fix. Say "no blockers" explicitly if there are none.
```

## What it caught here

The booking page case (major), stale comments, a dead margin rule, and a fallback rule that won only by source order. The earlier build's review also caught the back/forward cache case, the `:has()` fallback, print, and a dark-on-dark focus ring.
