#!/usr/bin/env python3
"""people.csv (+ deals.json, clay_emails.json when present) -> SDR handoff files.

Gate 1 = persona SOP (your ICP document), rule-based on
         the LinkedIn headline. Verdicts are HYPOTHESES (headline != HR title); PASS rows get eyeballed.
Gate 2 = deals.json, one entry per account from your CRM (see tools README). Missing entry -> "UNCHECKED" (never "clear").
Outputs: people-gated.csv, accounts.csv, unify-accounts-spec.csv, unify-accounts-HOLD-do-not-run.csv,
         contacts-P0-P2.csv. Spec header matches the account template our outbound tool imports; swap in yours.
"""
import csv, json, pathlib, re, collections
HERE = pathlib.Path(__file__).parent
ADS = {a["id"]: a for a in json.loads((HERE / "ads.json").read_text())}
DEALS = json.loads((HERE / "deals.json").read_text()) if (HERE / "deals.json").exists() else {}
EMAILS = json.loads((HERE / "clay_emails.json").read_text()) if (HERE / "clay_emails.json").exists() else {}
CAPTURED = "2026-09-18"

SPEC_HEADERS = ["account_name","account_domain","site_name","site_city","site_state_region","site_country",
  "site_address_optional","site_function_atomic","modality_atomic","manufacturing_stage","priority_reason",
  "evidence_url","evidence_snippet","target_personas","target_titles_include","target_titles_exclude",
  "seniority_include","site_affiliation_keywords","linkedin_search_hint","notes_for_unify"]
CONTACT_HEADERS = ["full_name","first_name","last_name","work_email","linkedin_url","job_title","company_name",
  "company_domain","deal_status","site_location","geo_priority","seniority_band","sop_persona_match","sop_flag",
  "engagement_signal","engagement_date","source","email_status","priority"]
# Paste your own persona definition here. Ours is an internal document; these placeholders keep the columns.
SOP_PERSONAS = "<persona groups, semicolon separated>"
SOP_TITLES_IN = "<target titles, semicolon separated>"
SOP_TITLES_EX = "<excluded departments and role types, semicolon separated>"
SOP_SENIORITY = "<seniority floor and above, semicolon separated>"

DEPT_PASS = re.compile(r"process\s*(development|dev\b|sciences?|engineer|scientist|expert)|upstream|downstream|\bMSAT\b|MS&T|"
  r"manufacturing scien|\bCMC\b|tech(nology)?\s*transfer|purification|bioprocess|cell culture|fermentation|"
  r"R&D IT|digitali[sz]ation|process (data|analytics|modeling)|\bPAT\b|digital twin", re.I)
DEPT_EXCL = re.compile(r"analytical|quality control|\bQC\b|\bQA\b|quality assurance|quality engineer|procurement|regulatory|"
  r"technician|associate scientist|sales|account (manager|executive)|marketing|brand manager|finance|accountant|controller|"
  r"\bHR\b|recruit|talent|legal|student|professor|lecturer|phd candidate|medical (representative|advisor|affairs)|"
  r"supply chain|logistics|pharmacist|clinical|commercial|business development|\bBD\b|founder|CEO|consultant", re.I)
def band(h):
    if re.search(r"\b(VP|Vice President|SVP|EVP|Chief|CTO|CSO|COO|CIO|CDO|Head of|Head,|Global Head|President)\b", h, re.I): return "VP+/Head"
    if re.search(r"\b(Associate Director|Assoc\.? Director|Director|Sr\.? Director|Senior Director|Executive Director)\b", h, re.I): return "Director"
    if re.search(r"\b(Senior Manager|Sr\.? Manager)\b", h, re.I): return "Senior Manager"
    if re.search(r"\b(Manager|Lead|Principal|Supervisor|Team Leader)\b", h, re.I): return "Manager/Lead"
    if re.search(r"\b(Senior|Sr\.?)\b", h, re.I): return "Senior IC"
    return "IC/unclear"
def sop(headline):
    h = headline or ""
    dept = bool(DEPT_PASS.search(h)); excl = bool(DEPT_EXCL.search(h)); b = band(h)
    sen_ok = b in ("VP+/Head", "Director", "Senior Manager")
    if dept and not excl and sen_ok: return "PASS", b, "dept+seniority match"
    if dept and not excl: return "FAIL-seniority", b, f"dept matches, {b} below Senior Manager"
    if not dept and sen_ok: return "FAIL-dept", b, "seniority ok, dept not PD/MSAT/CMC/R&D-IT" + (" (excluded dept)" if excl else "")
    return "FAIL-both", b, "no dept match, below seniority" + (" (excluded dept)" if excl else "")

def norm_acct(e): return re.sub(r"\s+", " ", re.sub(r"[^\w& ]", " ", (e or ""))).strip().lower()
def deal_for(acct):
    for k, v in DEALS.items():
        if norm_acct(k) == norm_acct(acct) or norm_acct(k) in norm_acct(acct): return v
    return None

def main():
    people = list(csv.DictReader(open(HERE / "people.csv")))
    out = []
    for p in people:
        verdict, b, why = sop(p["headline"])
        acct = p["inferred_employer"]; d = deal_for(acct) if acct else None
        status = (d or {}).get("status", "UNCHECKED" if acct else "no employer in headline")
        strong = p["strong_reaction"]; multi = int(p["n_ads"]) > 1; comm = int(p["comments"]) > 0
        if p["class"] != "prospect?": pri, reason = "P4", p["class"]
        elif status.startswith("ACTIVE"): pri, reason = "P0", "ACTIVE deal: route to owner"
        elif verdict == "PASS": pri, reason = "P1", "clears SOP" + ("" if d else " (deal status UNCHECKED)")
        elif verdict == "FAIL-seniority" or multi or comm or status.startswith("CLOSED LOST") or (strong and DEPT_PASS.search(p["headline"] or "")):
            pri, reason = "P2", "; ".join(x for x in [
                "PD/MSAT dept, below seniority" if verdict == "FAIL-seniority" else "", "multi-ad" if multi else "",
                "commented" if comm else "", "closed-lost revival" if status.startswith("CLOSED LOST") else ""] if x)
        else: pri, reason = "P4", "no signal"
        # Enrichment scope: only rows an SDR would act on -> P0/P1/P2 AND (target-department match OR Director+) AND a known domain
        actionable = pri in ("P0", "P1", "P2") and (bool(DEPT_PASS.search(p["headline"] or "")) or b in ("VP+/Head", "Director"))
        enrich = "yes" if actionable and (d or {}).get("domain") else ("no-domain" if actionable else "no")
        out.append({**p, "sop_verdict": verdict, "seniority_band": b, "sop_reason": why, "deal_status": status,
                    "routing": (d or {}).get("routing", ""), "priority": pri, "priority_reason": reason, "enrich_flag": enrich})
    order = {"P0": 0, "P1": 1, "P2": 2, "P4": 4}
    out.sort(key=lambda r: (order[r["priority"]], -int(r["signal_score"]), r["name"]))
    cols = list(out[0].keys())
    with open(HERE / "people-gated.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)

    # ---- account roll-up (prospect-class only, employer parsed) ----
    accts = collections.OrderedDict()
    for r in out:
        if r["class"] != "prospect?" or not r["inferred_employer"]: continue
        a = accts.setdefault(norm_acct(r["inferred_employer"]), {"account_name": r["inferred_employer"], "people": [], "ads": set()})
        a["people"].append(r); a["ads"].update(r["ads"].split(";"))
    rows, spec, hold = [], [], []
    for a in accts.values():
        ppl = a["people"]; d = deal_for(a["account_name"]) or {}
        status = d.get("status", "UNCHECKED"); dom = d.get("domain", "")
        n = len(ppl); passes = [p for p in ppl if p["sop_verdict"] == "PASS"]
        strong = [p for p in ppl if p["strong_reaction"]]
        how = {p["employer_how"] for p in ppl}
        names = "; ".join(f'{p["name"]} ({p["headline"][:60]})' for p in ppl[:6])
        rows.append({"account_name": a["account_name"], "account_domain": dom, "deal_status": status, "routing": d.get("routing", ""),
                     "n_engagers": n, "n_sop_pass": len(passes), "n_strong_reactions": len(strong), "n_ads": len(a["ads"]),
                     "employer_confidence": "low" if how <= {"last-segment?"} else "headline", "engagers": names})
        if not dom: continue  # spec rows need a domain; unresolved accounts stay in accounts.csv
        evidence = f"{n} LinkedIn ad engager(s), our LinkedIn ads: " + names
        reason = (f"{n} employee(s) engaged our LinkedIn ads" + (f"; {len(passes)} clear the persona SOP" if passes else "")
                  + (f"; {len(strong)} non-like reaction(s)" if strong else ""))
        urls = "; ".join(ADS[i]["post_url"] for i in sorted(a["ads"]) if i in ADS)
        hint = (f'{a["account_name"]} AND ("process development" OR "MSAT" OR "manufacturing science" OR "CMC" OR bioprocess) '
                f'AND (Director OR "Associate Director" OR "Senior Manager" OR VP)')
        row = [a["account_name"], dom, "", "", "", "", "", "", "", "", reason, urls, evidence, SOP_PERSONAS, SOP_TITLES_IN,
               SOP_TITLES_EX, SOP_SENIORITY, "", hint, d.get("routing", "") or "Engagers are account signals, not the target; apply SOP titles verbatim."]
        (hold if status.startswith("ACTIVE") else spec).append(row)
    rows.sort(key=lambda r: (-r["n_sop_pass"], -r["n_engagers"], r["account_name"]))
    with open(HERE / "accounts.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    for fn, rs in (("unify-accounts-spec.csv", spec), ("unify-accounts-HOLD-do-not-run.csv", hold)):
        with open(HERE / fn, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(SPEC_HEADERS); w.writerows(rs)

    # ---- contact file: P0/P1/P2 only ----
    with open(HERE / "contacts-P0-P2.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(CONTACT_HEADERS)
        for r in out:
            if r["priority"] not in ("P0", "P1", "P2"): continue
            e = EMAILS.get(r["name"], {}); d = deal_for(r["inferred_employer"]) or {}
            base = r["name"].split(",")[0].strip(); first, _, last = base.partition(" ")
            sig = f'{r["reactions"]}' + (f'; {r["comments"]} comment(s)' if int(r["comments"]) else "") + f'; {r["n_ads"]} ad(s)'
            w.writerow([r["name"], first, last, e.get("email", ""), r["profile"], e.get("title", r["headline"][:120]),
                        r["inferred_employer"], d.get("domain", ""), r["deal_status"], e.get("location", ""), "",
                        r["seniority_band"], r["sop_verdict"], r["sop_reason"] + ("; ACTIVE deal - DO NOT COLD OUTBOUND" if r["priority"] == "P0" else ""),
                        sig, ", ".join(sorted({ADS[i]["published"] for i in r["ads"].split(";") if i in ADS})),
                        "LinkedIn ad engagers, company page",
                        e.get("status") or {"yes": "pending in Clay", "no-domain": "no employer domain in headline - not searchable"}.get(r["enrich_flag"], "out of enrichment scope (role not PD/MSAT/Director+); signal only"),
                        r["priority"]])
    c = collections.Counter(r["priority"] for r in out); v = collections.Counter(r["sop_verdict"] for r in out if r["class"] == "prospect?")
    print("enrich_flag:", dict(collections.Counter(r["enrich_flag"] for r in out)))
    print(f"{len(out)} people -> people-gated.csv | priorities {dict(c)} | SOP {dict(v)}")
    print(f"{len(rows)} accounts -> accounts.csv | spec rows {len(spec)} | HOLD rows {len(hold)} | deals.json entries {len(DEALS)}")

if __name__ == "__main__": main()
