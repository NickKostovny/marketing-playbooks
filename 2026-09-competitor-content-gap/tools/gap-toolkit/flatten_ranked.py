#!/usr/bin/env python3
"""Flatten OpenSEO get_ranked_keywords output (raw DataForSEO passthrough) into one CSV.

Usage: flatten_ranked.py OUT.csv FILE_OR_DIR [FILE_OR_DIR ...]

Accepts the spilled tool-result .txt files, inline .json files, and the call files written
by calllog.py (their "output" field). Each source is JSON with a top-level "keywords" list of
{keyword_data, ranked_serp_element}. "position" is rank_group, the organic group rank;
rank_absolute counts SERP features (AI Overview, People Also Ask) as positions.
"""
import csv, glob, json, os, sys


def rows_from(d):
    tgt, out = d.get("target"), []
    for r in d.get("keywords", []):
        kd = r["keyword_data"]
        si = r["ranked_serp_element"]["serp_item"]
        ki = kd.get("keyword_info") or {}
        kp = kd.get("keyword_properties") or {}
        types = (kd.get("serp_info") or {}).get("serp_item_types") or []
        out.append(dict(
            target=tgt, keyword=kd["keyword"], volume=ki.get("search_volume"),
            kd=kp.get("keyword_difficulty"), cpc=ki.get("cpc"),
            intent=(kd.get("search_intent_info") or {}).get("main_intent"),
            position=si.get("rank_group"), rank_absolute=si.get("rank_absolute"),
            etv=si.get("etv"), url=si.get("url"), detected_language=kp.get("detected_language"),
            other_language=kp.get("is_another_language"), ai_overview=("ai_overview" in types),
            domain_rank=(si.get("rank_info") or {}).get("main_domain_rank"), source="ranked_by_volume"))
    return out


def candidates(d):
    if isinstance(d, dict) and d.get("keywords") and isinstance(d["keywords"], list) and "keyword_data" in d["keywords"][0]:
        yield d
    if isinstance(d, dict) and isinstance(d.get("output"), dict):
        yield from candidates(d["output"])


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out, inputs = sys.argv[1], sys.argv[2:]
    files = []
    for p in inputs:
        files += sorted(glob.glob(os.path.join(p, "*"))) if os.path.isdir(p) else [p]
    rows, seen = [], set()
    for f in files:
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for c in candidates(d):
            key = (c.get("target"), c.get("scope"), len(c["keywords"]))
            if key in seen:
                continue
            seen.add(key)
            r = rows_from(c)
            rows += r
            print(f"{os.path.basename(f)}: target={c.get('target')} rows={len(r)} totalCount={c.get('totalCount')}")
    if not rows:
        sys.exit("no ranked-keyword JSON found")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote", out, len(rows), "rows")


if __name__ == "__main__":
    main()
