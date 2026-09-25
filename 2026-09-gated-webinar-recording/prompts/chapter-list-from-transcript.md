# Prompt: an "In this session" chapter list from a transcript

Used for the bullets on the gated page. The goal is to make someone want the whole recording without giving the talks away. Paste the transcript (with timestamps) after the prompt.

```
Read this webinar transcript. Write an "In this session" list for the page that hosts the recording.

Rules:
- Five to eight bullets, each with the timestamp where the moment starts.
- Each bullet is one line, at most 14 words, and starts with the speaker's point, not with "Speaker discusses".
- Entice, do not summarise. Name the question or the claim. Do not give the answer.
- Every bullet must be checkable against the transcript. No claims the speakers did not make.
- Plain punctuation. No em dashes, no colons used as reveals, no exclamation marks.
- Use the vocabulary of the audience: process engineers and data leads at biologics manufacturers. mAb, CHO, AAV, cultivation. Never "fermentation".
- Do not name customers or companies the speakers mention. Roles only.

Return the list, then a second list of the transcript lines each bullet rests on, so I can check them.
```

What to check on the output: the second list is the point. Read each supporting line. A bullet that rests on a paraphrase gets rewritten or cut.
