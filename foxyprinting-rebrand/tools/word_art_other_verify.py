"""Re-read check for the 166 'other' Word Art prints (8 Oct 2026).

Usage: python3 tools/word_art_other_verify.py <out_dir> <result.json> [<result.json> ...]
Merges the saved nodes() reads into <out_dir>/after.json and prints every problem found.
"""
import json, os, re, sys

out = sys.argv[1]
nodes = []
for f in sys.argv[2:]:
    d = json.load(open(f))
    nodes += (d.get("data") or d)["nodes"]
plan = {e["id"]: e for e in json.load(open(os.path.join(out, "plan.json")))}
prev = os.path.join(out, "after.json")
have = {}
if os.path.exists(prev):
    have = {n["id"]: n for n in json.load(open(prev))["data"]["nodes"]}
for n in nodes:
    have[n["id"]] = n
json.dump({"data": {"nodes": list(have.values())}}, open(prev, "w"), ensure_ascii=False, indent=0)

PRICE = {"A4 Print Only": None, "A3 Print Only": "9.99", "A2 Print Only": "12.99", "A1 Print Only": "19.99",
         "A4 Print + Black Frame": "19.99", "A4 Print + Silver Frame": "19.99",
         "A3 Print + Black Frame": "29.99", "A3 Print + Silver Frame": "29.99"}
WEIGHT = {"A4 Print + Black Frame": 740, "A4 Print + Silver Frame": 740, "A3 Print + Black Frame": 1300,
          "A3 Print + Silver Frame": 1300}
SUF = {"A4 Print Only": "-A4", "A3 Print Only": "-A3", "A2 Print Only": "-A2", "A1 Print Only": "-A1",
       "A4 Print + Black Frame": "-A4-BLK", "A4 Print + Silver Frame": "-A4-SLV",
       "A3 Print + Black Frame": "-A3-BLK", "A3 Print + Silver Frame": "-A3-SLV"}
probs, allskus = [], []
for n in nodes:
    e = plan[n["id"]]
    p = lambda m: probs.append((n["id"][-13:], n["title"][:45], m))
    if n["options"][0]["name"] != "Size" or len(n["options"]) != 1:
        p("options " + str(n["options"]))
    vs = n["variants"]["nodes"]
    if sorted(v["title"] for v in vs) != sorted(PRICE):
        p("variant titles " + str([v["title"] for v in vs]))
    for v in vs:
        t = v["title"]
        if t not in PRICE:
            continue
        allskus.append(v["sku"])
        if v["sku"] != e["base_sku"] + SUF[t]:
            p(f"sku {t}: {v['sku']}")
        if PRICE[t] and v["price"] != PRICE[t]:
            p(f"price {t}: {v['price']}")
        if t == "A4 Print Only" and v["price"] != e["variant"]["price"]:
            p(f"A4 price changed {v['price']}")
        if t != "A4 Print Only" and v["compareAtPrice"]:
            p(f"compareAt {t}: {v['compareAtPrice']}")
        w = v["inventoryItem"]["measurement"]["weight"]
        if w["value"] != WEIGHT.get(t, 800) or w["unit"] != "GRAMS":
            p(f"weight {t}: {w}")
        if e["images_ok"]:
            want = e["order"][0] if "Black" in t else e["order"][1] if "Silver" in t else None
            murl = {m["id"]: (m.get("image") or {}).get("url", "").split("?")[0] for m in n["media"]["nodes"]}
            got = ((v["image"] or {}).get("url") or "").split("?")[0]
            if want and got != murl.get(want):
                p(f"variant image {t}: {got[-40:]}")
    if n["templateSuffix"] != "personalised":
        p("template " + str(n["templateSuffix"]))
    tags = set(n["tags"])
    if "io-word-art" not in tags or "Poster Options" in tags or "Word Art" not in tags:
        p("tags " + str(sorted(tags)))
    if ("third-party-name" in tags) != e["third_party"]:
        p("third-party-name tag mismatch")
    if n["descriptionHtml"].replace("\n", "") != e["descriptionHtml"].replace("\n", ""):
        p("description differs from plan")
    h = n["descriptionHtml"]
    if re.search(r"style=|<h4|#|<p>\s*</p>|<li>\s*</li>", h) or h.count("<h2") != 1:
        p("description html rule")
    if n["seo"]["title"] != e["seo_title"] or n["seo"]["description"] != e["seo_description"]:
        p(f"seo {n['seo']}")
    if json.loads(n["pf"]["value"] if n["pf"] else "[]") != e["fields"]:
        p("personalise_fields " + str(n["pf"]))
    want_mf = {"mk": "photo", "cp": "true", "mpn": e["base_sku"] + "-A4", "col": e["color"], "gen": "unisex",
               "cond": "new", "age": "adult"}
    for k, val in want_mf.items():
        if (n[k] or {}).get("value") != val:
            p(f"metafield {k}: {n[k]}")
    if not (n["gpc"] or {}).get("value"):
        p("google_product_category missing")
    media = n["media"]["nodes"]
    if e["images_ok"]:
        if [m["id"] for m in media] != e["order"]:
            p("media " + str([m["id"][-11:] for m in media]))
        for m in media:
            if m["alt"] != e["alts"].get(m["id"]):
                p(f"alt {m['id'][-11:]}: {m['alt']}")
print(len(nodes), "nodes checked;", len(have), "in after.json;", len(probs), "problems")
for x in probs:
    print(*x)
dup = {s for s in allskus if allskus.count(s) > 1}
print("duplicate SKUs inside this read:", dup or "none")
