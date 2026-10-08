"""Rename bar-mat size option values and fix the size lines in descriptions (owner, 8 Oct 2026):
"change Small to Small 440 x 330 and the large to Large 880mm x 330mm".
Input: exports/bar-mats/2026-10-08/before-existing-bar-mats.json (all product_type 'Bar Mat').
Writes batched GraphQL mutations (productOptionUpdate + productUpdate aliases) to OUT dir.
The 51 personalised designs used "Medium" for the 440mm mat (same 440 size), so Medium is renamed to Small too.
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "exports/bar-mats/2026-10-08/before-existing-bar-mats.json"
OUT = Path(sys.argv[1])
SMALL, LARGE = "Small 440mm x 330mm", "Large 880mm x 330mm"
q = json.dumps

def new_value(name):
    n = name.lower()
    if n.startswith("small") or n.startswith("medium"):
        return SMALL
    if n.startswith("large"):
        return LARGE
    raise ValueError(name)

def new_desc(html):
    html = re.sub(r"(Small|Medium)=\s*440mm x 250mm", "Small = 440mm x 330mm", html)
    html = re.sub(r"Large=\s*880mm x 250mm", "Large = 880mm x 330mm", html)
    return html

prods = json.load(open(SRC))
plan, blocks = [], []
for i, p in enumerate(prods):
    opt = p["options"][0]
    upd = [{"id": v["id"], "name": new_value(v["name"])} for v in opt["optionValues"] if v["name"] != new_value(v["name"])]
    d2 = new_desc(p["descriptionHtml"])
    plan.append({"id": p["id"], "title": p["title"], "handle": p["handle"], "status": p["status"],
                 "values_before": [v["name"] for v in opt["optionValues"]],
                 "values_after": [new_value(v["name"]) for v in opt["optionValues"]],
                 "skus": [v["sku"] for v in p["variants"]["nodes"]],
                 "prices": [v["price"] for v in p["variants"]["nodes"]],
                 "description_changed": d2 != p["descriptionHtml"]})
    b = []
    if upd:
        vals = ", ".join("{id: %s, name: %s}" % (q(u["id"]), q(u["name"])) for u in upd)
        b.append('o%d: productOptionUpdate(productId: %s, option: {id: %s}, optionValuesToUpdate: [%s]) { userErrors { field message } }'
                 % (i, q(p["id"]), q(opt["id"]), vals))
    if d2 != p["descriptionHtml"]:
        b.append('d%d: productUpdate(product: {id: %s, descriptionHtml: %s}) { userErrors { field message } }' % (i, q(p["id"]), q(d2)))
    blocks.append(b)
OUT.mkdir(parents=True, exist_ok=True)
json.dump(plan, open(ROOT / "exports/bar-mats/2026-10-08/renamed-size-options.json", "w"), indent=1, ensure_ascii=False)
flat = [x for b in blocks for x in b]
n = 0
for k in range(0, len(flat), 40):
    (OUT / f"rename_{n}.graphql").write_text("mutation {\n" + "\n".join(flat[k:k+40]) + "\n}\n")
    n += 1
print(len(flat), "ops in", n, "files")
