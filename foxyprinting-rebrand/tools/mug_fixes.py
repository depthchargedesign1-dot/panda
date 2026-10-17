"""Plan the direct API fixes for mugs (6 Oct 2026): vendor -> Foxy Printing, Google Shopping metafields, third-party-name tag.
Usage: python3 tools/mug_fixes.py <bulk_export.jsonl> <mug_copy out_dir> <age-group import csv ...>
Writes fixes.json (vendor ids, metafields, tag ids) and the GraphQL batch files batches/NN.graphql."""
import csv, json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mug_copy as m
from age_group import age_group

export, out = sys.argv[1], sys.argv[2]
queued = {}
for f in sys.argv[3:]:
    for r in csv.DictReader(open(f, encoding="utf-8-sig")):
        queued[r["Handle"]] = (r[[k for k in r if "age_group" in k][0]], r[[k for k in r if ".gender" in k][0]])
P = [p for p in m.load(export) if m.is_mug(p) and not m.excluded(p)]
tp = {r["Handle"] for r in csv.DictReader(open(f"{out}/third-party-names.csv")) if r["Had third-party-name tag"] == "no"}
vendor, mfs, tags, log = [], [], [], collections.Counter()
per = collections.defaultdict(list)
for p in P:
    h, mf = p["handle"], p["mf"]
    if p["vendor"] != "Foxy Printing" and p["vendor"] != "kite.ly":
        vendor.append(p["id"]); log["vendor"] += 1
    skus = [v["sku"] for v in p["variants"] if v["sku"]]
    want = {}
    if mf.get("custom_product") != "true": want["custom_product"] = ("true", "boolean")
    if mf.get("condition") != "new": want["condition"] = ("new", "single_line_text_field")
    standard = p["productType"] not in m.NON_STANDARD_TYPES and "Thermal Mug" not in p["title"] and h != "mug"
    if standard and mf.get("google_product_category") != m.GPC:
        want["google_product_category"] = (m.GPC, "single_line_text_field")
    ag = age_group(p["productType"], p["title"], p["tags"])
    q = queued.get(h)
    if mf.get("age_group") != ag and not (q and q[0] == ag): want["age_group"] = (ag, "single_line_text_field")
    if mf.get("gender") != "unisex" and not (q and q[1] == "unisex"): want["gender"] = ("unisex", "single_line_text_field")
    if not (mf.get("color") or "").strip(): want["color"] = ("Multicolor", "single_line_text_field")
    if skus and mf.get("mpn") not in skus: want["mpn"] = (skus[0], "single_line_text_field")
    for k, (v, t) in want.items():
        mfs.append({"ownerId": p["id"], "namespace": "mm-google-shopping", "key": k, "value": v, "type": t})
        log["mf:" + k] += 1
        per[h].append(k)
    if h in tp:
        tags.append(p["id"]); log["tag"] += 1
json.dump({"vendor": vendor, "metafields": mfs, "tags": tags, "per_product": per}, open(f"{out}/fixes.json", "w"))
print(dict(log), "products with metafield changes:", len(per))
