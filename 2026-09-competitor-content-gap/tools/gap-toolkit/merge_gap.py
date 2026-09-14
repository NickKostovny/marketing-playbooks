#!/usr/bin/env python3
"""Merge the by-volume and by-traffic competitor samples and compute the gap against your site.

Usage: merge_gap.py --own DOMAIN --ranked ranked.csv --calls CALLS_DIR --brands brands.json
                    --out merged.csv [--top 20] [--relevant REGEX]

ranked.csv comes from flatten_ranked.py. CALLS_DIR is calllog.py's output; suggestion results
(get_domain_keyword_suggestions) are read from it. brands.json maps competitor domain to a regex
of brand terms; matching suggestion rows are dropped (the ranked pull should already have used
excludeBrandTerms). Gap: "no" if your site holds a position <= --top for the keyword, "weak" if
it ranks lower, "yes" otherwise.
"""
import argparse, csv, glob, json, re
from collections import Counter


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--own", required=True)
    ap.add_argument("--ranked", required=True)
    ap.add_argument("--calls", required=True)
    ap.add_argument("--brands", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--relevant", default=None)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.ranked)))
    for r in rows:
        for k in ("volume", "kd", "position", "rank_absolute"):
            r[k] = int(float(r[k])) if r.get(k) not in (None, "", "None") else None
    have = {(r["target"], r["keyword"]) for r in rows}
    brands = json.load(open(a.brands))
    for f in sorted(glob.glob(f"{a.calls}/*_get_domain_keyword_suggestions.json")):
        rec = json.load(open(f))
        d = rec.get("output") or {}
        tgt = d.get("target")
        for s in d.get("keywords", []):
            if (tgt, s["keyword"]) in have or re.search(brands.get(tgt, r"(?!)"), s["keyword"], re.I):
                continue
            rows.append(dict(target=tgt, keyword=s["keyword"], volume=s.get("searchVolume"), kd=s.get("keywordDifficulty"),
                             cpc=s.get("cpc"), intent=None, position=s.get("position"), rank_absolute=None, etv=s.get("traffic"),
                             url=None, detected_language=None, other_language=None, ai_overview=None, domain_rank=None,
                             source="suggestions_by_traffic"))
    own = {r["keyword"]: r["position"] for r in rows if r["target"] == a.own and r["position"] is not None}
    for r in rows:
        p = own.get(r["keyword"])
        r["own_position"] = p
        r["gap"] = "no" if (p is not None and p <= a.top) else ("weak" if p is not None else "yes")
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("rows per target:", dict(Counter(r["target"] for r in rows)))
    print("competitor keywords you already hold (gap=no):",
          [(r["target"], r["keyword"], r["position"], r["own_position"]) for r in rows if r["gap"] == "no" and r["target"] != a.own])
    print("competitor keywords you rank for below --top (gap=weak):",
          [(r["target"], r["keyword"], r["position"], r["own_position"]) for r in rows if r["gap"] == "weak" and r["target"] != a.own])
    if a.relevant:
        pat = re.compile(a.relevant, re.I)
        for t in sorted({r["target"] for r in rows} - {a.own}):
            rs = sorted([r for r in rows if r["target"] == t and r["gap"] != "no" and pat.search(r["keyword"])], key=lambda r: -(r["volume"] or 0))
            print(f"\n--- {t}: {len(rs)} relevant gap rows ---")
            for r in rs:
                u = (r["url"] or "")
                u = u[u.find("/", 8):][:55] if u else ""
                print(f"{r['volume']!s:>6} kd={r['kd']!s:>3} pos={r['position']!s:>3} {r['keyword'][:44]:<44} {u}")


if __name__ == "__main__":
    main()
