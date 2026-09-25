#!/usr/bin/env python3
"""Resolve lnkd.in short links -> ads.json checkpoint (free, no browser).

Usage: python3 resolve_ads.py links.txt        # one link per line, '#' comments ok
Re-running is safe: existing entries keep their scraped/counts fields.
"""
import datetime, json, re, subprocess, sys, pathlib

HERE = pathlib.Path(__file__).parent
OUT = HERE / "ads.json"

def resolve(short):
    r = subprocess.run(["curl", "-sIL", "-A", "Mozilla/5.0", short],
                       capture_output=True, text=True, timeout=30)
    locs = re.findall(r"^location:\s*(\S+)", r.stdout, flags=re.I | re.M)
    return locs[-1] if locs else None

def parse(url):
    m = re.search(r"(ugcPost|activity|share)[-:](\d{15,})", url or "")
    if not m:
        return None, None, None
    kind, sid = m.group(1), int(m.group(2))
    ts = datetime.datetime.utcfromtimestamp((sid >> 22) / 1000)
    return kind, str(sid), ts.strftime("%Y-%m-%d")

def main(path):
    ads = {}
    if OUT.exists():
        ads = {a["short"]: a for a in json.loads(OUT.read_text())}
    for line in pathlib.Path(path).read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s in ads and ads[s].get("post_url"):
            continue
        full = resolve(s)
        kind, sid, date = parse(full)
        clean = full.split("?")[0] if full else None
        ads[s] = {"short": s, "post_url": clean, "urn_type": kind, "id": sid,
                  "published": date, "scraped": False,
                  "reactions_headline": None, "reactions_captured": None,
                  "comments_headline": None, "comments_captured": None,
                  "topic": None}
        print(f"{s} -> {kind} {sid} {date}")
    OUT.write_text(json.dumps(list(ads.values()), indent=1))
    print(f"{len(ads)} ads in {OUT}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else HERE / "links.txt")
