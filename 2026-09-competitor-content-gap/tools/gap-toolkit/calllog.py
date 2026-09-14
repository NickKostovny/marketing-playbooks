#!/usr/bin/env python3
"""Build a citable call log from a Claude Code session transcript.

Usage: calllog.py TRANSCRIPT.jsonl OUT_DIR [--prefix mcp__openseo__]

Pairs every tool_use whose name starts with the prefix to its tool_result and writes
OUT_DIR/NN_<tool>.json = {"n", "tool", "input", "output", "spill_file"}.
Inline JSON results are parsed into "output"; results the harness spilled to disk keep
output null and record the path the harness printed. Also writes index.json and
calllog_table.md (a Markdown table to paste into the data file).
"""
import json, os, re, sys


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    prefix = "mcp__openseo__"
    for i, a in enumerate(sys.argv):
        if a == "--prefix" and i + 1 < len(sys.argv):
            prefix = sys.argv[i + 1]
    if len(args) < 2:
        sys.exit(__doc__)
    transcript, out = args[0], args[1]
    os.makedirs(out, exist_ok=True)
    uses, results, order = {}, {}, []
    for line in open(transcript):
        try:
            obj = json.loads(line)
        except Exception:
            continue
        content = (obj.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "tool_use":
                uses[item["id"]] = (item.get("name"), item.get("input"))
                order.append(item["id"])
            elif item.get("type") == "tool_result":
                c = item.get("content")
                texts = [c] if isinstance(c, str) else [x.get("text", "") for x in c if isinstance(x, dict)]
                results[item["tool_use_id"]] = "\n".join(texts)
    n, index = 0, []
    for tid in order:
        name, inp = uses[tid]
        if not (name or "").startswith(prefix):
            continue
        n += 1
        raw = results.get(tid, "")
        parsed = None
        if raw.startswith("{"):
            try:
                parsed = json.loads(raw)
            except Exception:
                parsed = None
        m = re.search(r"saved to (\S+\.txt)", raw)
        spill = m.group(1) if m else None
        tool = name[len(prefix):]
        rec = {"n": n, "tool": tool, "input": inp, "output": parsed, "spill_file": spill,
               "error": None if (parsed or spill) else raw[:300]}
        json.dump(rec, open(os.path.join(out, f"{n:02d}_{tool}.json"), "w"))
        params = {k: v for k, v in (inp or {}).items() if k != "projectId"}
        index.append((n, tool, json.dumps(params)[:110], "spill" if spill else ("json" if parsed else "error/none")))
    json.dump(index, open(os.path.join(out, "index.json"), "w"))
    table = "| # | Tool | Parameters | Result |\n|---|---|---|---|\n" + "\n".join(
        f"| {a} | {b} | `{c.replace('|', '/')}` | {d} |" for a, b, c, d in index)
    open(os.path.join(out, "calllog_table.md"), "w").write(table)
    for row in index:
        print(row)
    print(f"{n} calls written to {out}")


if __name__ == "__main__":
    main()
