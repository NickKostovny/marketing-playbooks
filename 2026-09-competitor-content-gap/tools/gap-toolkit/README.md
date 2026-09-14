# Gap toolkit

Three small scripts that turn OpenSEO MCP output into a merged competitor keyword table, a gap against your own site, and a citable call log. Python 3.9 or later, standard library only.

## Where the input comes from

Claude Code shows small MCP results inline and spills large ones to disk. Both matter here.

- Spilled results: the tool result says `Output has been saved to <path>`. The files live under the project's Claude folder, `~/.claude/projects/<project-slug>/<session-id>/tool-results/`. Ranked-keyword pulls always spill.
- Inline results (keyword suggestions, metrics, SERPs, domain overviews): only in the session transcript, `~/.claude/projects/<project-slug>/<session-id>.jsonl`. `calllog.py` recovers them.

## calllog.py

```bash
python3 calllog.py ~/.claude/projects/<slug>/<session>.jsonl out/calls --prefix mcp__openseo__
```

Walks the transcript, pairs every `tool_use` whose name starts with the prefix to its `tool_result`, and writes `out/calls/NN_<tool>.json` with `{n, tool, input, output, spill_file}`. Inline JSON is parsed into `output`; spilled results keep `output: null` and record the path in `spill_file`. Also writes `index.json` and `calllog_table.md`, the table you paste into the data file so `[call N]` resolves.

## flatten_ranked.py

```bash
python3 flatten_ranked.py out/ranked.csv ~/.claude/projects/<slug>/<session>/tool-results/ out/calls/
```

Reads every ranked-keyword JSON it finds (spilled `.txt` files and recovered call files alike) and writes one CSV: target, keyword, volume, difficulty, cpc, intent, position (`rank_group`, the organic group rank), rank_absolute, estimated traffic, URL, detected language, AI Overview flag, domain rank. Quote `position`, not `rank_absolute`.

## merge_gap.py

```bash
python3 merge_gap.py --own yourdomain.com --ranked out/ranked.csv --calls out/calls \
  --brands brands.json --out out/merged.csv --top 20 --relevant 'bioprocess|lims|gmp|...'
```

Adds the by-traffic suggestion rows (recovered by `calllog.py`) to the by-volume ranked rows, drops suggestion rows that match the competitor's brand pattern in `brands.json` (`{"competitor.com": "brand|product|misspelling"}`), and computes the gap: `no` if your site holds a position within `--top`, `weak` if it ranks lower, `yes` otherwise. Prints the overlap, and if `--relevant` is given, the relevant gap rows per competitor sorted by volume.

## Notes

- The suggestions tool caps at 100 rows by traffic and includes brand terms; the ranked tool caps at 100 per call. Merged samples are samples. Report the API's `totalCount` alongside.
- Keyword metrics drops keywords with no data. The call files let you diff input against output; `calllog.py` keeps both.
