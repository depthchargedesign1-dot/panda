"""Build the aliased productUpdate / tags / metafields batches for the 20 v2 coasters.
usage: python3 build_updates.py BEFORE_JSON OUT_DIR"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coaster_copy as C

before = {n["handle"]: n for n in json.load(open(sys.argv[1]))["data"]["nodes"]}
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
rows = []
for p in C.P:
    n = before[p["handle"]]
    sku = n["variants"]["nodes"][0]["sku"]
    old = [t for t in n["tags"] if t in C.OLD_IO_TAGS]
    # keep every collection: replace each collection-feeding old tag with its new 2026 tag
    add = list(C.BASE_TAGS)
    if "Bar Coasters" in n["tags"]:
        add.append("bar-coaster-2026")
    if "Man Cave Coasters" in n["tags"]:
        add += ["man-cave-coaster-2026", "man cave"]
    if "third-party-name" in n["tags"]:
        add.append("third-party-name")
    pid = n["id"]
    mf = [dict(ownerId=pid, namespace="foxy", key="mockup", type="single_line_text_field", value="photo"),
          dict(ownerId=pid, namespace="foxy", key="personalise_fields", type="list.single_line_text_field",
               value=json.dumps(p["fields"], ensure_ascii=False))]
    # mm-google-shopping was already complete and correct on all 20 (checked 8 Oct: custom_product true, condition new,
    # Barware > Coasters, unisex, adult, Multicolor, mpn = SKU), so only the foxy fields are set here.
    for k, t, v in () and (("custom_product", "boolean", "true"), ("condition", "single_line_text_field", "new"),
                    ("google_product_category", "single_line_text_field", C.CAT), ("gender", "single_line_text_field", "unisex"),
                    ("age_group", "single_line_text_field", "adult"), ("color", "single_line_text_field", "Multicolor"),
                    ("mpn", "single_line_text_field", sku)):
        mf.append(dict(ownerId=pid, namespace="mm-google-shopping", key=k, type=t, value=v))
    prod = dict(id=pid, title=p["title"], descriptionHtml=p["description"], templateSuffix="personalised",
                vendor="Foxy Printing", productType="Coasters", seo=dict(title=p["seo_title"], description=p["seo_desc"]))
    media = [m["id"] for m in n["media"]["nodes"]]
    rows.append(dict(key=p["key"], handle=p["handle"], id=pid, sku=sku, add=add, rm=old, product=prod, mf=mf, media=media, alt=p["alt"]))
json.dump(rows, open(os.path.join(out, "updates.json"), "w"), ensure_ascii=False, indent=1)
# batches of 4 products
for b in range(0, len(rows), 5):
    chunk = rows[b:b + 5]
    defs, body, var = [], [], {}
    for i, r in enumerate(chunk):
        defs += [f"$id{i}: ID!", f"$add{i}: [String!]!", f"$rm{i}: [String!]!", f"$p{i}: ProductUpdateInput!", f"$mf{i}: [MetafieldsSetInput!]!"]
        body += [f"a{i}: tagsAdd(id: $id{i}, tags: $add{i}) {{ userErrors {{ field message }} }}",
                 f"u{i}: productUpdate(product: $p{i}) {{ product {{ id title }} userErrors {{ field message }} }}",
                 f"m{i}: metafieldsSet(metafields: $mf{i}) {{ userErrors {{ field message }} }}",
                 f"r{i}: tagsRemove(id: $id{i}, tags: $rm{i}) {{ userErrors {{ field message }} }}"]
        var.update({f"id{i}": r["id"], f"add{i}": r["add"], f"rm{i}": r["rm"], f"p{i}": r["product"], f"mf{i}": r["mf"]})
    q = "mutation(" + ", ".join(defs) + ") { " + " ".join(body) + " }"
    json.dump(dict(query=q, variables=var), open(os.path.join(out, f"batch{b // 5}.json"), "w"), ensure_ascii=False, separators=(",", ":"))
print(len(rows), [ (r['key'], r['rm'], len(r['media'])) for r in rows])
