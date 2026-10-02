"""Build Shopify import CSVs that set all 7 Google Shopping metafields (mm-google-shopping) correctly.

Inputs: a bulk export JSONL (products + mm-google-shopping metafields + variant SKUs), the category fix CSVs
in exports/categories, and Shopify's product-taxonomy repo (Shopify -> Google category mapping).
Usage: python3 google_fields.py export.jsonl product-taxonomy-dir outdir
"""
import csv, glob, os, re, sys, collections
import yaml
sys.path.insert(0, os.path.dirname(__file__))
from age_group import age_group
from meta_audit import load

COLS = [("custom_product", "Google Shopping / Custom Product"), ("condition", "Google Shopping / Condition"),
        ("google_product_category", "Google Shopping / Google Product Category"), ("gender", "Google Shopping / Gender"),
        ("age_group", "Google Shopping / Age Group"), ("color", "Google Shopping / Color"), ("mpn", "Google Shopping / MPN")]
MULTI = re.compile(r"^(multi|multicolou?r|multi-colou?r|mixed)$", re.I)

def taxonomy(pt):
    g = yaml.safe_load(open(f"{pt}/data/integrations/google/2021-09-21/full_names.yml"))
    gid2name = {str(x["id"]): x["full_name"] for x in g}
    rules = yaml.safe_load(open(f"{pt}/data/integrations/google/2021-09-21/mappings/from_shopify.yml"))["rules"]
    s2g = {r["input"]["product_category_id"]: str(r["output"]["product_category_id"][0]) for r in rules}
    name2sid = {}
    for line in open(f"{pt}/dist/en/categories.txt"):
        if line.startswith("gid://"):
            gid, name = line.split(" : ", 1)
            name2sid[name.strip()] = gid.strip().rsplit("/", 1)[1]
    return gid2name, s2g, name2sid

def target(p, newcat, gid2name, s2g, name2sid):
    mf = p["mf"]
    valid = set(gid2name.values())
    cat = newcat.get(p["handle"]) or (p.get("category") or {}).get("fullName")
    mapped = gid2name.get(s2g.get(name2sid.get(cat or ""), ""))
    if cat and cat.endswith("Baby & Children's Tops > Bodysuits"):  # Google's own bucket for baby grows
        mapped = "Apparel & Accessories > Clothing > Baby & Toddler Clothing > Baby One-Pieces"
    cur = (mf.get("google_product_category") or "").strip()
    if re.fullmatch(r"\d+(\.0)?", cur):
        cur = gid2name.get(cur.split(".")[0], "")
    if cur not in valid:
        cur = ""
    gpc = cur if cur and (not mapped or cur.startswith(mapped)) else (mapped or cur)
    color = (mf.get("color") or "").strip()
    color = "Multicolor" if (not color or MULTI.match(color)) else color[:1].upper() + color[1:]
    skus = [s for s in p["skus"] if s]
    mpn = mf.get("mpn") if mf.get("mpn") in skus else (skus[0] if skus else (mf.get("mpn") or ""))
    return {"custom_product": "true", "condition": "new", "google_product_category": gpc, "gender": "unisex",
            "age_group": age_group(p.get("productType"), p.get("title"), p.get("tags")), "color": color, "mpn": mpn}

if __name__ == "__main__":
    export, pt, out = sys.argv[1:4]
    here = os.path.dirname(os.path.abspath(__file__))
    newcat = {}
    for f in glob.glob(f"{here}/../exports/categories/product-categories-0[1-9].csv"):
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            newcat[r["Handle"]] = r["Product Category"]
    gid2name, s2g, name2sid = taxonomy(pt)
    rows, changed, nogpc = [], collections.Counter(), []
    for p in load(export).values():
        t = target(p, newcat, gid2name, s2g, name2sid)
        diff = [k for k, _ in COLS if (p["mf"].get(k) or "") != t[k]]
        if not t["google_product_category"]:
            nogpc.append([p["handle"], p["title"], p.get("productType")])
        if diff:
            changed.update(diff)
            rows.append([p["handle"], p["title"]] + [t[k] for k, _ in COLS])
    os.makedirs(out, exist_ok=True)
    head = ["Handle", "Title"] + [f"{n} (product.metafields.mm-google-shopping.{k})" for k, n in COLS]
    def write(name, part):
        with open(f"{out}/{name}", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(head); w.writerows(part)
    test = [r for r in rows if "bodysuit" in r[0]][:1] + [r for r in rows if "signed" in r[0] or "autograph" in r[0]][:1] \
         + [r for r in rows if "face-mask" in r[0]][:1]
    write("00-TEST-3-products.csv", test)
    for i in range(0, len(rows), 15000):
        write(f"{i // 15000 + 1:02d}-google-fields.csv", rows[i:i + 15000])
    with open(f"{out}/no-google-category.csv", "w", newline="") as f:
        csv.writer(f).writerows([["Handle", "Title", "Type"]] + nogpc)
    print(len(rows), "products to update; field changes:", dict(changed), "; no category:", len(nogpc))
