"""Audit product metadata from a bulk-export JSONL (products + mm-google-shopping metafields + variants).

Checks the house rules in CLAUDE.md: the 7 Google Shopping metafields, SEO title/meta description,
vendor, and banned "official"-type words in SEO text.  Usage: python3 meta_audit.py export.jsonl outdir
"""
import collections, csv, json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from age_group import age_group

BANNED = re.compile(r"\b(official|licensed|authentic|genuine|autographed|hand[- ]signed|memorabilia)\b", re.I)
KEYS = ["custom_product", "condition", "google_product_category", "gender", "age_group", "color", "mpn"]

def load(path):
    prods = collections.OrderedDict()
    for line in open(path):
        o = json.loads(line)
        if "__parentId" not in o:
            o["mf"], o["skus"] = {}, []
            prods[o["id"]] = o
        elif "key" in o:
            prods[o["__parentId"]]["mf"][o["key"]] = o["value"]
        else:
            prods[o["__parentId"]]["skus"].append(o.get("sku") or "")
    return prods

def audit(p):
    issues = []
    mf, seo = p["mf"], p.get("seo") or {}
    for k in KEYS:
        if not (mf.get(k) or "").strip():
            issues.append(f"missing:{k}")
    if mf.get("custom_product") not in (None, "true"):
        issues.append("custom_product!=true")
    if mf.get("condition") and mf["condition"].lower() != "new":
        issues.append("condition!=new")
    if mf.get("gender") and mf["gender"] != "unisex":
        issues.append(f"gender={mf['gender']}")
    want = age_group(p.get("productType"), p.get("title"), p.get("tags"))
    if mf.get("age_group") and mf["age_group"] != want:
        issues.append(f"age_group={mf['age_group']}->{want}")
    skus = [s for s in p["skus"] if s]
    if mf.get("mpn") and skus and mf["mpn"] not in skus:
        issues.append("mpn-not-a-sku")
    if not skus:
        issues.append("no-sku")
    t, d = (seo.get("title") or "").strip(), (seo.get("description") or "").strip()
    if not t: issues.append("seo-title-missing")
    elif len(t) > 70: issues.append("seo-title-long")
    if not d: issues.append("meta-desc-missing")
    elif len(d) > 160: issues.append("meta-desc-long")
    elif len(d) < 70: issues.append("meta-desc-short")
    if BANNED.search(t) or BANNED.search(d):
        issues.append("seo-banned-word")
    if (p.get("vendor") or "") != "Foxy Printing":
        issues.append("vendor")
    return issues, want

if __name__ == "__main__":
    prods = load(sys.argv[1]); out = sys.argv[2]
    cnt, by_status = collections.Counter(), collections.Counter()
    rows = []
    for p in prods.values():
        iss, want = audit(p)
        for i in iss:
            key = i.split("=")[0] if i.startswith(("gender", "age_group")) else i
            cnt[key] += 1; by_status[(key, p["status"])] += 1
        if iss:
            rows.append([p["handle"], p["status"], p["title"], p.get("productType"), "; ".join(iss)])
    with open(f"{out}/meta-issues.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["Handle", "Status", "Title", "Type", "Issues"]); w.writerows(rows)
    print(len(prods), "products,", len(rows), "with issues")
    for k, v in cnt.most_common():
        print(f"{v:6d} {k:24s} active={by_status[(k,'ACTIVE')]} draft={by_status[(k,'DRAFT')]} archived={by_status[(k,'ARCHIVED')]}")
