# Four-lens adversarial review of a signup-flow change

Run this before merging any change to a form that captures leads. Four reviewers each get one lens. Every finding then goes to a skeptic whose job is to refute it. Only findings the skeptic can reproduce from the code survive.

I ran it as a Claude Code workflow: the four lens reviews and a production build in parallel, then one skeptic per lens as soon as that lens finished. Any orchestration works. What matters is that the reviewers are independent and the skeptic defaults to "not real".

## 1. Shared context block (paste into every agent)

Fill in the braces. The "known facts" list is the most important part: without it, skeptics and reviewers spend their time on problems that existed before your change.

```text
You are reviewing an UNCOMMITTED change in {{repo path}}. Base is {{base branch}}.
See the diff with: git diff {{base}} -- .
READ-ONLY: do not edit files, commit, push, or submit the form against production.
A dev server runs at {{local URL}}; you may request it but not drive a browser.

WHAT THE OWNER ASKED FOR:
{{the brief, in their words}}
{{any decisions they made when asked}}

WHAT CHANGED:
{{one line per file}}

KNOWN, ESTABLISHED FACTS (do not re-litigate):
- {{how capture works: which events fire when, and the guards against double counting}}
- {{honesty rules for the copy: what the page may never promise}}
- {{pre-existing issues that are not regressions}}
```

## 2. The four lenses

**Capture and attribution.** Compare the new form component with the old one, line by line, for every path that sends a record or an ad-platform event. Could any interaction now send a record more or fewer times than before, send a stale value, or drop a field? Does source attribution still reach the stored record? Trace every inbound link and every redirect. Are there references left to deleted code, including comments that are now false?

**Interaction state machine and accessibility.** Walk every sequence: forward through all steps; reopen step one and pick the same answer; pick a different answer after the last step was opened; fold the open step by clicking its own header; start over from the done screen; keyboard only. Where does focus go after each pick? Is there any state where nothing can be clicked, where the submit button is reachable but its field is hidden, or where a hidden panel still holds focus? Check long labels, narrow screens, reduced motion, and any later global rule that overrides these styles.

**Framework correctness.** Check redirects, static versus dynamic rendering, hooks rules, hydration, and boolean attributes against the framework's own docs for the version in the repo. Run the type checker and a scoped lint. Report only new errors.

**Copy, honesty and leftovers.** Read every visible string, old and new. Report new copy that over-promises (immediacy, an account that does not exist, "ready"), approved copy that disappeared and mattered, metadata that no longer fits the page, dead CSS, and comments that are now false.

Ask each reviewer for: file, line, severity, one-sentence summary, a concrete failure scenario (inputs and state that lead to wrong output), and a suggested fix. An empty list is a valid answer.

## 3. The skeptic (one per lens)

```text
{{shared context block}}

A reviewer (lens: {{lens}}) reported the findings below. Be a skeptic. For EACH one,
try to REFUTE it by reading the actual code (and docs, or a request to the dev server,
where useful). Mark real=true only if you can confirm the failure scenario happens with
this code. Mark real=false if it is wrong, speculative, already true before the change,
or listed under KNOWN FACTS. Default to real=false when uncertain.

{{numbered findings with file, line, summary, scenario}}
```

## What it caught the first time

A first-load dead end: clicking the header of the step that was already open folded it and disabled it, and with the later steps still locked, nothing on the page could be clicked. I had tested every path except that one. Details in the [ship log](../README.md#step-5-adversarial-review-before-merge).
