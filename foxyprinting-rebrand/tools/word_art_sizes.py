"""Build aliased Shopify mutations that turn the single-variant
"Personalised Name Word Art" prints into the 8 Size variants used on the
printed signature prints (6 Oct 2026). Usage:
  python3 tools/word_art_sizes.py <before.json> <out_dir> [batch_size]
Writes descriptions.json (old->new HTML) and batch_NN.graphql/.vars.json."""
import json, sys, os, re

NL, SEP = "\n", ",\n"
LOC = "gid://shopify/Location/103075971453"
FRAMED_W = {"A4": 740, "A3": 1300}  # from A. J. Green AF-1 framed variants
NEW = [  # (value, price, suffix, framed-size or None)
    ("A3 Print Only", "9.99", "-A3", None),
    ("A2 Print Only", "12.99", "-A2", None),
    ("A1 Print Only", "19.99", "-A1", None),
    ("A4 Print + Black Frame", "19.99", "-A4-BLK", "A4"),
    ("A4 Print + Silver Frame", "19.99", "-A4-SLV", "A4"),
    ("A3 Print + Black Frame", "29.99", "-A3-BLK", "A3"),
    ("A3 Print + Silver Frame", "29.99", "-A3-SLV", "A3"),
]
OLD_SENT = ("They are High-Quality Prints in Full Colour and framed in Black, Silver, "
            "White or Gold Frames. You can even choose if you want your print in A3, A4 or as a card.")
NEW_SENT = ("They are High-Quality Prints in Full Colour, available as a print only in A4, A3, "
            "A2 or A1, or framed in a Black or Silver frame in A4 or A3.")
ANCHOR = '<h4 id="templatedesctxt">A1 - 210 gsm Gloss</h4>'
SECTION = ('<h3>Size &amp; details</h3>\n<ul>\n<li>A4: 210 x 297 mm</li>\n<li>A3: 297 x 420 mm</li>\n'
           '<li>A2: 420 x 594 mm</li>\n<li>A1: 594 x 841 mm</li>\n</ul>\n'
           '<p>Framed options come in our Premium Display frames – thick, chunky and very '
           'professional, not cheap thin frames – in black or silver.</p>\n')

def new_desc(html):
    if "Premium Display frames" in html:
        return html
    assert OLD_SENT in html and ANCHOR in html, "description template changed"
    html = html.replace(OLD_SENT, NEW_SENT)
    return html.replace(ANCHOR, ANCHOR + "\n" + SECTION, 1)

def taxpol(v):
    # defaults are taxable:true, inventoryPolicy:DENY; only send what differs
    out = "" if v["taxable"] else "taxable:false, "
    return out + ("" if v["inventoryPolicy"] == "DENY" else f'inventoryPolicy:{v["inventoryPolicy"]}, ')

def q(s):
    return json.dumps(s, ensure_ascii=False)

def seo_title(title):
    m = re.search(r"(Pink|Blue) Letter ([A-Z])$", title)
    return f"Personalised Word Art Print {m.group(1)} Letter {m.group(2)} | Foxy Printing"

def main():
    before, out = sys.argv[1], sys.argv[2]
    bs = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    prods = json.load(open(before))["data"]["products"]["nodes"]
    skip = set(sys.argv[4].split(",")) if len(sys.argv) > 4 else set()
    prods = [p for p in prods if p["id"] not in skip]
    os.makedirs(out, exist_ok=True)
    descs = {}
    for p in prods:
        descs.setdefault(p["descriptionHtml"], new_desc(p["descriptionHtml"]))
    keys = list(descs)
    json.dump([{"old": k, "new": descs[k]} for k in keys], open(f"{out}/descriptions.json", "w"),
              ensure_ascii=False, indent=1)
    plan = []
    for b in range(0, len(prods), bs):
        chunk = prods[b:b + bs]
        lines, mf, varsd = [], [], {}
        for i, p in enumerate(chunk):
            v = p["variants"]["nodes"]
            assert len(v) == 1 and v[0]["title"] == "Default Title", p["handle"]
            v = v[0]; opt = p["options"][0]; ii = v["inventoryItem"]
            sku = v["sku"]; w = ii["measurement"]["weight"]
            pid = q(p["id"])
            lines.append(f'o{i}: productOptionUpdate(productId:{pid}, option:{{id:{q(opt["id"])}, name:"Size"}}, '
                         f'optionValuesToUpdate:[{{id:{q(opt["optionValues"][0]["id"])}, name:"A4 Print Only"}}]) {{ userErrors {{ field message }} }}')
            lines.append(f'u{i}: productVariantsBulkUpdate(productId:{pid}, variants:[{{id:{q(v["id"])}, inventoryItem:{{sku:{q(sku + "-A4")}}}}}]) {{ userErrors {{ field message }} }}')
            vs = []
            for name, price, suf, fr in NEW:
                wt = FRAMED_W[fr] if fr else w["value"]
                item = {"sku": sku + suf, "tracked": ii["tracked"],
                        "measurement": {"weight": {"value": wt, "unit": "GRAMS"}},
                        "countryCodeOfOrigin": ii["countryCodeOfOrigin"],
                        "harmonizedSystemCode": ii["harmonizedSystemCode"]}
                if not ii["requiresShipping"]:
                    item["requiresShipping"] = False
                var = {"optionValues": [{"optionName": "Size", "name": name}], "price": price,
                       "compareAtPrice": None, "inventoryItem": item,
                       "inventoryQuantities": [{"locationId": LOC, "availableQuantity": v["inventoryQuantity"]}]}
                if not v["taxable"]:
                    var["taxable"] = False
                if v["inventoryPolicy"] != "DENY":
                    var["inventoryPolicy"] = v["inventoryPolicy"]
                vs.append(var)
            varsd[f"v{i}"] = vs
            lines.append(f'c{i}: productVariantsBulkCreate(productId:{pid}, variants:$v{i}) {{ userErrors {{ field message }} }}')
            dv = f'$d{keys.index(p["descriptionHtml"])}'
            # productUpdate clears the meta description unless it is sent too
            seo_desc = next(m["value"] for m in p["metafields"]["nodes"] if m["key"] == "description_tag")
            lines.append(f'p{i}: productUpdate(product:{{id:{pid}, descriptionHtml:{dv}, seo:{{title:{q(seo_title(p["title"]))}, description:{q(seo_desc)}}}}}) {{ userErrors {{ field message }} }}')
            if any(m["key"] == "mpn" for m in p["metafields"]["nodes"]):
                mf.append(f'{{ownerId:{pid}, namespace:"mm-google-shopping", key:"mpn", type:"single_line_text_field", value:{q(sku + "-A4")}}}')
        if mf:
            lines.append(f'm: metafieldsSet(metafields:[{", ".join(mf)}]) {{ userErrors {{ field message code }} }}')
        used = sorted({keys.index(p["descriptionHtml"]) for p in chunk})
        sig = ", ".join([f"$v{i}: [ProductVariantsBulkInput!]!" for i in range(len(chunk))] + [f"$d{k}: String!" for k in used])
        doc = f"mutation({sig}) {{\n" + "\n".join(lines) + "\n}\n"
        n = b // bs
        open(f"{out}/batch_{n:02d}.graphql", "w").write(doc)
        json.dump({**varsd, **{f"d{k}": descs[keys[k]] for k in used}}, open(f"{out}/batch_{n:02d}.vars.json", "w"), ensure_ascii=False, separators=(",", ":"))
        plan.append({"batch": n, "handles": [p["handle"] for p in chunk]})
    json.dump(plan, open(f"{out}/plan.json", "w"), indent=1)



# ---- Two-phase variant (used for the rollout; the MCP caps a GraphQL document
# at 16 KB, so phase A creates the 7 new variants from ONE shared variable $V
# (identical for every product apart from the SKU) and phase B sets the SKUs
# by variant id once they exist.)
def shared_variants(p):
    v = p["variants"]["nodes"][0]; ii = v["inventoryItem"]; w = ii["measurement"]["weight"]
    out = []
    for name, price, suf, fr in NEW:
        wt = FRAMED_W[fr] if fr else w["value"]
        out.append({"optionValues": [{"optionName": "Size", "name": name}], "price": price,
                    "compareAtPrice": None, "taxable": v["taxable"], "inventoryPolicy": v["inventoryPolicy"],
                    "inventoryItem": {"tracked": ii["tracked"], "requiresShipping": ii["requiresShipping"],
                                      "measurement": {"weight": {"value": wt, "unit": w["unit"]}},
                                      "countryCodeOfOrigin": ii["countryCodeOfOrigin"],
                                      "harmonizedSystemCode": ii["harmonizedSystemCode"]},
                    "inventoryQuantities": [{"locationId": LOC, "availableQuantity": v["inventoryQuantity"]}]})
    return out

def phase_a(before, out, bs, skip):
    prods = [p for p in json.load(open(before))["data"]["products"]["nodes"] if p["id"] not in skip]
    os.makedirs(out, exist_ok=True)
    V = shared_variants(prods[0])
    assert all(shared_variants(p) == V for p in prods), "variant settings differ between products"
    descs = {}
    for p in prods:
        descs.setdefault(p["descriptionHtml"], new_desc(p["descriptionHtml"]))
    keys = list(descs)
    for b in range(0, len(prods), bs):
        chunk = prods[b:b + bs]; lines = []; mf = []
        for i, p in enumerate(chunk):
            v = p["variants"]["nodes"][0]; opt = p["options"][0]; pid = q(p["id"])
            assert len(p["variants"]["nodes"]) == 1 and v["title"] == "Default Title"
            seo_desc = next(m["value"] for m in p["metafields"]["nodes"] if m["key"] == "description_tag")
            lines.append(f'o{i}: productOptionUpdate(productId:{pid}, option:{{id:{q(opt["id"])}, name:"Size"}}, optionValuesToUpdate:[{{id:{q(opt["optionValues"][0]["id"])}, name:"A4 Print Only"}}]) {{ userErrors {{ message }} }}')
            lines.append(f'u{i}: productVariantsBulkUpdate(productId:{pid}, variants:[{{id:{q(v["id"])}, inventoryItem:{{sku:{q(v["sku"] + "-A4")}}}}}]) {{ userErrors {{ message }} }}')
            lines.append(f'c{i}: productVariantsBulkCreate(productId:{pid}, variants:$V) {{ userErrors {{ message }} }}')
            lines.append(f'p{i}: productUpdate(product:{{id:{pid}, descriptionHtml:$d{keys.index(p["descriptionHtml"])}, seo:{{title:{q(seo_title(p["title"]))}, description:{q(seo_desc)}}}}}) {{ userErrors {{ message }} }}')
            if any(m["key"] == "mpn" for m in p["metafields"]["nodes"]):
                mf.append(f'{{ownerId:{pid}, namespace:"mm-google-shopping", key:"mpn", type:"single_line_text_field", value:{q(v["sku"] + "-A4")}}}')
        if mf:
            lines.append(f'm: metafieldsSet(metafields:[{", ".join(mf)}]) {{ userErrors {{ message }} }}')
        used = sorted({keys.index(p["descriptionHtml"]) for p in chunk})
        sig = ", ".join(["$V: [ProductVariantsBulkInput!]!"] + [f"$d{k}: String!" for k in used])
        n = b // bs
        open(f"{out}/a_{n:02d}.graphql", "w").write(f"mutation({sig}) {{\n" + "\n".join(lines) + "\n}\n")
        json.dump({"V": V, **{f"d{k}": descs[keys[k]] for k in used}}, open(f"{out}/a_{n:02d}.vars.json", "w"),
                  ensure_ascii=False, separators=(",", ":"))

def phase_b(before, after_variants, out, bs):
    """after_variants: products query result with variants{id title sku}."""
    base = {p["id"]: p["variants"]["nodes"][0]["sku"] for p in json.load(open(before))["data"]["products"]["nodes"]}
    suf = {name: s for name, _, s, _ in NEW}
    todo = []
    for p in json.load(open(after_variants))["data"]["products"]["nodes"]:
        ups = [f'{{id:{q(v["id"])}, inventoryItem:{{sku:{q(base[p["id"]] + suf[v["title"]])}}}}}'
               for v in p["variants"]["nodes"] if v["title"] in suf and not v["sku"]]
        if ups:
            todo.append(f'b{len(todo)}: productVariantsBulkUpdate(productId:{q(p["id"])}, variants:[{", ".join(ups)}]) {{ userErrors {{ message }} }}')
    for b in range(0, len(todo), bs):
        open(f"{out}/b_{b // bs:02d}.graphql", "w").write("mutation {\n" + "\n".join(todo[b:b + bs]) + "\n}\n")
    print(len(todo), "products need SKUs")


if __name__ == "__main__":
    if sys.argv[1] == "a":    # a <before.json> <out> <batch> <skip ids,>
        phase_a(sys.argv[2], sys.argv[3], int(sys.argv[4]), set(sys.argv[5].split(",")) if len(sys.argv) > 5 else set())
    elif sys.argv[1] == "b":  # b <before.json> <after_variants.json> <out> <batch>
        phase_b(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]))
    else:
        main()
