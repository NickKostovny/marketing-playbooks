# linkedin-engagers

Scripts from the ad-engagement-to-SDR run. Python 3.9+ and `openpyxl` for the workbook. Everything else is stdlib. The browser scripts are pasted into a script-execution tool in a logged-in browser session.

| File | Runs where | Does |
| --- | --- | --- |
| `resolve_ads.py` | shell | Short links -> `ads.json` checkpoint (post URL, id, publish date, scraped flag, counts). Idempotent. |
| `receiver.py` | shell, background | Local HTTP receiver. `GET /save?name=<file>.json&d=<urlencoded json>` writes `raw/<file>.json`, holds two seconds, redirects to the site. |
| `scrape_reactors.js` | browser, on the post page | Reactions modal -> rows -> receiver. Replace `__POST_ID__`. |
| `scrape_comments.js` | browser, on the post page (fresh load) | Comments -> receiver, only if any. Replace `__POST_ID__`. |
| `scrape_iframe.js` | browser, on the feed page | Same as both above but from a same-origin iframe. Use when scripts are refused on the post URL. |
| `build_people.py` | shell | `raw/*.json` -> `people.csv`: one row per person across ads, inferred employer, class (prospect, own staff, competitor, supplier, vendor, services, academic), signal score. |
| `build_handoff.py` | shell | `people.csv` + `deals.json` + `clay_emails.json` -> `people-gated.csv`, `accounts.csv`, account-template rows, `HOLD` file, `contacts-P0-P2.csv`. |
| `build_workbook.py` | shell | All of the above -> one `.xlsx` with a Read me tab. |

## Inputs you maintain by hand

`deals.json`, one entry per account name as it appears in `people.csv`:

```json
{"Example Pharma": {"domain": "example.com", "status": "ACTIVE - <stage>, owner <role>", "routing": "DO NOT COLD OUTBOUND - route to owner", "checked": "2026-09-18"}}
```

`status` starting with `ACTIVE` sends the account to the hold file; starting with `CLOSED LOST` marks a revival. Accounts with no entry stay `UNCHECKED`.

`clay_emails.json`, keyed by the person's name as scraped:

```json
{"Jane Example": {"email": "jane@example.com", "title": "MSAT team lead", "company": "Example Pharma", "location": "", "linkedin": "", "status": "verified (2026-09-18)"}}
```

## Things to replace before running

- `build_people.py`: `STAFF`, `COMPANY`, `NON_PROSPECT`, and extend `KNOWN` with the companies your audience works at.
- `build_handoff.py`: the four `SOP_*` strings (your persona definition) and, if you want, the `DEPT_PASS` / `DEPT_EXCL` patterns and the seniority regexes in `band()`.
- The receiver port (`8871`) in the three browser scripts if it is taken.

## Order

```bash
python3 resolve_ads.py links.txt
nohup python3 receiver.py 8871 > receiver.log 2>&1 &
# scrape in the browser, one script per post, until every ads.json entry is scraped
python3 build_people.py
# fill deals.json from your CRM, then:
python3 build_handoff.py
# enrich the enrich_flag == yes rows, fill clay_emails.json, then:
python3 build_handoff.py && python3 build_workbook.py
```
