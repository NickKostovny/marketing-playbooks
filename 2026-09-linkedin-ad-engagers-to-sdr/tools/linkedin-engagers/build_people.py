#!/usr/bin/env python3
"""raw/reactors-*.json + raw/comments-*.json  ->  people.csv (one row per person, all ads).

Free stage: no Clay. Headline-parsed fields are HYPOTHESES (inferred_*).
Gates (deal status, persona SOP) are applied later in build_handoff.py once every ad is scraped.
"""
import csv, glob, json, re, pathlib, collections

HERE = pathlib.Path(__file__).parent
ADS = {a["id"]: a for a in json.loads((HERE / "ads.json").read_text())}

STAFF = set()  # lowercase full names of your own team, so they drop out of the prospect pool
COMPANY = "yourcompany"  # your company name as it appears in headlines ("@ YourCompany", "at YourCompany")
NON_PROSPECT = {  # employer keyword -> class; fill in your own competitors, suppliers and vendors
  "<competitor-a>": "competitor", "<competitor-b>": "competitor", "<supplier-a>": "supplier", "<vendor-a>": "vendor",
  "consulting": "services", "university": "academic", "universit": "academic", "student": "academic", "phd student": "academic",
}
STRONG = {"insightful", "love", "support", "celebrate"}  # anything beyond a plain like

def norm(s): return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("ph.d.", "").replace("phd", "")).strip()

KNOWN = ["AstraZeneca","Novo Nordisk","Biogen","Teva","Bristol Myers Squibb","BMS","Pfizer","Roche","Genentech","Novartis",
  "Sanofi","GSK","Merck","MSD","Amgen","Gilead","Takeda","Bayer","Boehringer","Lonza","Samsung Biologics","WuXi","Fujifilm",
  "Catalent","Thermo Fisher","Sartorius","Cytiva","Moderna","BioNTech","CSL","Regeneron","Vertex","AbbVie","Lilly",
  "Johnson & Johnson","J&J","Janssen"]  # public names only; extend with whatever your audience actually works at

ALIAS = {"j&j": "Johnson & Johnson", "johnson & johnson": "Johnson & Johnson", "bms": "Bristol Myers Squibb",
         "bristol myers squibb": "Bristol Myers Squibb", "msd": "MSD", "merck": "MSD", "lilly": "Eli Lilly", "eli lilly": "Eli Lilly",
         "gilead": "Gilead Sciences", "gilead sciences": "Gilead Sciences", "wuxi biologics": "WuXi Biologics"}
COMPANY_SUFFIX = re.compile(r"\b(Ltd|Inc|GmbH|AG|SA|S\.A\.|BV|B\.V\.|LLC|Corp|Corporation|Biologics|Pharma|Pharmaceuticals|Biotech|Bio|Therapeutics|Sciences|Group|Labs?)\b", re.I)
def canon(e):
    e = (e or "").strip(" .")
    return ALIAS.get(e.lower(), e)

def employer(headline):
    """Best-effort employer from a LinkedIn headline. Returns (employer, how). Hypothesis, not fact."""
    h = headline or ""
    first = h.split(" | ")[0]
    for pat, how in ((r"\b(?:at|@)\s*([A-Z][\w&.'\u2019\- ]{1,50}?)(?=\s*[|,\u2022\u00b7\-\u2013]|$)", "at/@"),
                     (r"\b(?:at|@)\s*([A-Z][\w&.'\u2019\- ]{1,50})", "at/@ loose"),
                     (r"\b(?:chez|bei|w firmie|en|presso)\s+([A-Z][\w&.'\u2019\- ]{1,50}?)(?=\s*[|,\u2022\u00b7]|$)", "chez/bei/w firmie")):
        m = re.search(pat, first) or re.search(pat, h)
        if m: return m.group(1).strip(" ."), how
    low = h.lower()
    for k in KNOWN:
        if re.search(r"(?<![a-z])" + re.escape(k.lower()) + r"(?![a-z])", low): return k, "known-name"
    segs = [x.strip() for x in re.split(r"\s*[|\u2022\u00b7]\s*", h) if x.strip()]
    if len(segs) >= 2 and 1 <= len(segs[-1].split()) <= 3 and segs[-1][:1].isupper() and COMPANY_SUFFIX.search(segs[-1]) \
       and not re.search(r"(?i)manager|engineer|scientist|specialist|director|lead|head|analyst|consultant|expert|phd|msc|mba", segs[-1]):
        return segs[-1], "last-segment?"
    return "", ""

def main():
    people = collections.OrderedDict()
    def key(r): return r.get("profile") or norm(r["name"])
    for f in sorted(glob.glob(str(HERE / "raw" / "reactors-*.json"))):
        d = json.loads(pathlib.Path(f).read_text())
        for r in d["rows"]:
            if r.get("is_company"): continue
            p = people.setdefault(key(r), {"name": r["name"], "profile": r.get("profile",""), "headline": r.get("headline",""),
                                           "degree": r.get("degree",""), "ads": set(), "reactions": [], "comments": 0, "comment_text": []})
            p["ads"].add(d["post_id"]); p["reactions"].append(r.get("reaction",""))
        for r in d.get("comments", []):  # iframe-mode scrapes embed comments in the reactors payload
            p = people.setdefault(key(r), {"name": r["name"], "profile": r.get("profile",""), "headline": r.get("headline",""),
                                           "degree": "", "ads": set(), "reactions": [], "comments": 0, "comment_text": []})
            p["ads"].add(d["post_id"]); p["comments"] += 1; p["comment_text"].append(r.get("text",""))
    for f in sorted(glob.glob(str(HERE / "raw" / "comments-*.json"))):
        d = json.loads(pathlib.Path(f).read_text())
        for r in d["rows"]:
            p = people.setdefault(key(r), {"name": r["name"], "profile": r.get("profile",""), "headline": r.get("headline",""),
                                           "degree": "", "ads": set(), "reactions": [], "comments": 0, "comment_text": []})
            p["ads"].add(d["post_id"]); p["comments"] += 1; p["comment_text"].append(r.get("text",""))

    cols = ["name","inferred_employer","employer_how","class","degree","n_ads","ads","ad_topics","n_engagements",
            "reactions","strong_reaction","comments","signal_score","headline","profile","comment_text"]
    out = []
    for p in people.values():
        emp, how = employer(p["headline"]); emp = canon(emp)
        cls = "prospect?"
        hl = p["headline"].lower()
        if norm(p["name"]) in STAFF or re.search(r"(@\s*|\bat\s+)" + re.escape(COMPANY) + r"\b", hl): cls = "own-staff"
        else:
            for k, v in NON_PROSPECT.items():
                if k in (emp + " " + p["headline"]).lower(): cls = v; break
        strong = sorted(set(r for r in p["reactions"] if r in STRONG))
        score = len(p["ads"]) + 2*p["comments"] + (1 if strong else 0)
        out.append({"name": p["name"], "inferred_employer": emp, "employer_how": how, "class": cls, "degree": p["degree"],
                    "n_ads": len(p["ads"]), "ads": ";".join(sorted(p["ads"])),
                    "ad_topics": ";".join((ADS.get(i,{}).get("topic") or i) for i in sorted(p["ads"])),
                    "n_engagements": len(p["reactions"]) + p["comments"], "reactions": ";".join(p["reactions"]),
                    "strong_reaction": ";".join(strong), "comments": p["comments"], "signal_score": score,
                    "headline": p["headline"], "profile": p["profile"], "comment_text": " || ".join(p["comment_text"])})
    out.sort(key=lambda r: (-r["signal_score"], r["class"] != "prospect?", r["name"]))
    with open(HERE / "people.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(out)
    c = collections.Counter(r["class"] for r in out)
    print(f"{len(out)} unique people across {len(ADS)} ads -> people.csv"); print(dict(c))
    print("no employer parsed:", sum(1 for r in out if not r["inferred_employer"] and r["class"]=="prospect?"))

if __name__ == "__main__": main()
