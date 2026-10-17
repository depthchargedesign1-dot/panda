"""Build the CSV import, markdown plan and Admin API batches from plan/catalogue.py.

Usage:  python3 tools/build_plan.py
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "plan"))
import catalogue as C  # noqa: E402

OUT = ROOT / "tools" / "out"
OUT.mkdir(parents=True, exist_ok=True)

RANGES = {h: dict(handle=h, title=t, department=d, blurb=b) for h, t, d, b in C.RANGES}

FINISH = {
    "UV": "printed direct with vivid, scratch-resistant UV inks",
    "UVDTF": "finished with a permanent, dishwasher-tough UV DTF print",
    "DTF": "pressed with a soft-feel, stretch-friendly DTF print that lasts wash after wash",
    "CUT": "printed and precision-cut in our UK workshop",
    "PRESS": "printed on premium stock in our UK workshop",
}

# Which live-preview mockup the theme's personaliser should use.
MOCKUP_RULES = [
    (r"opener|phone case|transfer|gang sheet|labels|reindeer", "flat"),
    (r"game case card", "card"),
    (r"box(es)?\b|calendar|sleeve|game case", "box"),
    (r"card|letter|coupon|invitation|print\b|portrait", "card"),
    (r"t-shirt|hoodie|sweatshirt|jumper|pyjama|baby grow|vest|bib|outfit|polo|bandana|bag|apron|sash|blanket", "apparel"),
    (r"tumbler|can cup|bottle|cup\b|mug|flask|glass|flute|jar|candle|bowl", "drinkware"),
    (r"bauble|decoration|key\b", "bauble"),
]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def mockup_for(title):
    t = title.lower()
    for pattern, kind in MOCKUP_RULES:
        if re.search(pattern, t):
            return kind
    return "flat"


def variants_of(p):
    v = p["variants"]
    if isinstance(v, (int, float)):
        return "Title", [("Default Title", v)]
    if isinstance(v, tuple):
        return v[0], v[1]
    return "Size", v


def body_html(p, r):
    fields = p["personalise"]
    lines = [f"<p><strong>{p['title']}</strong> - {FINISH[p['machine']]}.</p>",
             f"<p>{r['blurb']}</p>"]
    if fields:
        lines.append("<p>Personalise it with: " + ", ".join(fields).lower() +
                     ". See a live preview before you add it to your basket.</p>")
    lines.append("<ul><li>Made to order in the UK</li><li>Free digital proof on request</li>"
                 "<li>Fast dispatch - see delivery options at checkout</li></ul>")
    return "".join(lines)


def tags_of(p, r):
    t = ["foxy-new-2026", f"range-{r['handle']}", f"dept-{slug(r['department'])}",
         f"machine-{p['machine'].lower()}", f"wave-{p['wave']}"]
    if p["personalise"]:
        t.append("personalised")
    if p["trend"] >= 5:
        t.append("trending")
    return t


_SKU_BASES = {}


def sku(p, i, value):
    """Stable, unique SKU: FOXY-<machine>-<title initials>[-n]-<variant no>."""
    key = p["title"]
    if key not in _SKU_BASES:
        base = "FOXY-" + p["machine"] + "-" + "".join(w[0] for w in slug(p["title"]).split("-"))[:8].upper()
        taken = set(_SKU_BASES.values())
        candidate, n = base, 2
        while candidate in taken:
            candidate, n = f"{base}{n}", n + 1
        _SKU_BASES[key] = candidate
    return f"{_SKU_BASES[key]}-{i:02d}"


def build():
    products = []
    for p in C.P:
        r = RANGES[p["range"]]
        opt, vals = variants_of(p)
        products.append(dict(
            handle=slug(p["title"]), title=p["title"], range=r, machine=p["machine"],
            wave=p["wave"], trend=p["trend"], option=opt, values=vals,
            personalise=p["personalise"], notes=p["notes"], body=body_html(p, r),
            tags=tags_of(p, r), mockup=mockup_for(p["title"]),
            product_type=r["title"],
        ))
    handles = Counter(x["handle"] for x in products)
    dupes = [h for h, n in handles.items() if n > 1]
    assert not dupes, f"duplicate handles: {dupes}"
    return products


def write_csv(products):
    cols = ["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
            "Option1 Name", "Option1 Value", "Variant SKU", "Variant Inventory Policy",
            "Variant Fulfillment Service", "Variant Price", "Variant Requires Shipping",
            "Variant Taxable", "Template Suffix", "Status",
            "Personalisation fields (product.metafields.foxy.personalise_fields)",
            "Live preview mockup (product.metafields.foxy.mockup)"]
    path = ROOT / "plan" / "new-products-shopify-import.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for p in products:
            for i, (value, price) in enumerate(p["values"]):
                first = i == 0
                w.writerow([
                    p["handle"],
                    p["title"] if first else "",
                    p["body"] if first else "",
                    "Foxy Printing" if first else "",
                    p["product_type"] if first else "",
                    ", ".join(p["tags"]) if first else "",
                    "FALSE" if first else "",
                    p["option"] if first else "",
                    value, sku(p, i + 1, value), "continue", "manual", f"{price:.2f}",
                    "TRUE", "TRUE",
                    "personalised" if first and p["personalise"] else "",
                    "draft" if first else "",
                    " | ".join(p["personalise"]) if first else "",
                    p["mockup"] if first else "",
                ])
    return path


def write_batches(products, size=10):
    """ProductSetInput objects, grouped for aliased productSet mutations."""
    items = []
    for p in products:
        inp = {
            "title": p["title"],
            "handle": p["handle"],
            "descriptionHtml": p["body"],
            "vendor": "Foxy Printing",
            "productType": p["product_type"],
            "status": "DRAFT",
            "tags": p["tags"],
            "productOptions": [{"name": p["option"], "values": [{"name": v} for v, _ in p["values"]]}],
            "variants": [{
                "optionValues": [{"optionName": p["option"], "name": v}],
                "price": f"{price:.2f}",
                "sku": sku(p, i + 1, v),
                "inventoryPolicy": "CONTINUE",
            } for i, (v, price) in enumerate(p["values"])],
            "metafields": [
                {"namespace": "foxy", "key": "mockup", "type": "single_line_text_field", "value": p["mockup"]},
            ],
        }
        if p["personalise"]:
            inp["templateSuffix"] = "personalised"
            inp["metafields"].append({"namespace": "foxy", "key": "personalise_fields",
                                      "type": "list.single_line_text_field",
                                      "value": json.dumps(p["personalise"])})
        items.append(inp)
    batches = [items[i:i + size] for i in range(0, len(items), size)]
    for n, b in enumerate(batches, 1):
        (OUT / f"products-batch-{n:02d}.json").write_text(json.dumps(b, indent=1))
    # Smart collections (unpublished) - one per range.
    cols = [{"title": r["title"], "handle": f"new-{r['handle']}", "descriptionHtml": f"<p>{r['blurb']}</p>",
             "ruleSet": {"appliedDisjunctively": False,
                         "rules": [{"column": "TAG", "relation": "EQUALS", "condition": f"range-{r['handle']}"}]}}
            for r in RANGES.values()]
    (OUT / "collections.json").write_text(json.dumps(cols, indent=1))
    return len(batches)


def money(x):
    return f"£{x:.2f}"


def write_markdown(products):
    by_range = defaultdict(list)
    for p in products:
        by_range[p["range"]["handle"]].append(p)
    by_machine = Counter(p["machine"] for p in products)
    by_wave = defaultdict(list)
    for p in products:
        by_wave[p["wave"]].append(p)

    md = ["# Foxy Printing: new product plan (2026–27)", "",
          "_Generated from `plan/catalogue.py` by `tools/build_plan.py`. Prices are suggested RRPs in GBP including VAT._", "",
          f"**{len(products)} new product lines** in **{len(RANGES)} ranges**, all made in-house on your existing and new kit.", "",
          "## Products per machine", "", "| Machine | Lines | What it unlocks |", "|---|---:|---|"]
    for k, desc in C.MACHINES.items():
        md.append(f"| {k} | {by_machine.get(k, 0)} | {desc} |")
    md += ["", "## Launch waves", ""]
    for w in (1, 2, 3, 0):
        items = sorted(by_wave[w], key=lambda p: -p["trend"])
        md.append(f"### {C.WAVES[w]} ({len(items)} lines)")
        md.append("")
        md.append(", ".join(f"{p['title']}{' 🔥' if p['trend'] >= 5 else ''}" for p in items))
        md.append("")
    md += ["## Full range list by mega-menu department", ""]
    for dept in C.DEPARTMENTS:
        ranges = [r for r in RANGES.values() if r["department"] == dept]
        if not ranges:
            continue
        md.append(f"### {dept}")
        md.append("")
        for r in ranges:
            md.append(f"#### {r['title']}")
            md.append(f"_{r['blurb']}_")
            md.append("")
            md.append("| Product | Machine | Wave | Trend | Options & RRP | Personalisation | Notes |")
            md.append("|---|---|---|---|---|---|---|")
            for p in by_range[r["handle"]]:
                opts = "; ".join(f"{v} {money(pr)}" if v != "Default Title" else money(pr) for v, pr in p["values"])
                md.append(f"| {p['title']} | {p['machine']} | {p['wave'] or 'Core'} | {'★' * p['trend']} | {opts} | "
                          f"{', '.join(p['personalise']) or '–'} | {p['notes']} |")
            md.append("")
    path = ROOT / "plan" / "product-lines.md"
    path.write_text("\n".join(md))
    return path


if __name__ == "__main__":
    prods = build()
    print("products:", len(prods), "variants:", sum(len(p["values"]) for p in prods))
    print("csv:", write_csv(prods))
    print("batches:", write_batches(prods))
    print("md:", write_markdown(prods))
