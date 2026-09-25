# Accordion signup demo

A single HTML file that shows the patterns from this playbook with no framework and no build step. Open `index.html` in a browser.

What it demonstrates:

- Three steps, all headers visible from the start, one open at a time. A pick folds its step down to the answer, shown under the question.
- The last step opens by itself once both questions are answered, and focus moves to the email field. The field has its own `:focus` style, because browsers often hide their default ring when script moves the focus.
- Panels animate on `grid-template-rows` (`0fr` to `1fr`). Closed panels are `inert`. The list is built once and only its attributes change, so the transition can run.
- A folded step that has no answer yet stays clickable (the "todo" state), so there is never a moment with nothing to click.
- The email error appears only after the field loses focus, and clears when the visitor returns to it.
- Only the `completed` record carries the terms acceptance. The panel under the card shows the records the page would send.

Swap `OPTIONS` for your own questions. Nothing is sent anywhere; records only appear on the page.
