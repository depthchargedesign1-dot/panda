"""Build productCreate inputs + copy for the new bar mats (8 Oct 2026).
Writes exports/bar-mats/2026-10-08/products.json.
"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from data import P

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "exports/bar-mats/2026-10-08/products.json"
SMALL, LARGE = "Small 440mm x 330mm", "Large 880mm x 330mm"
CAT = "Home & Garden > Kitchen & Dining > Barware"
NO_PROOF = "We print exactly what you enter, so please check names and spelling in the live preview before you order."

BANK = [
    "Rubber-backed, so it sits flat on the bar top and stays put while the drinks are flowing",
    "Printed in full colour by dye-sublimation in our own North Yorkshire workshop",
    "Two sizes: the small 440mm mat for a shelf or drinks trolley, or the 880mm runner for a full bar top",
    "Catches the drips from glasses and bottles, so the bar top stays tidier through the evening",
    "Made to order, so each one is printed just for you rather than pulled off a shelf",
    "Works just as well on a garden bar, a games room counter or a kitchen island",
    "Looks smart under a row of pint glasses at a party or a match-day get-together",
    "A present that gets used every weekend instead of sitting in a drawer",
]
DETAILS = [
    ["Small: 440mm x 330mm", "Large: 880mm x 330mm", "Rubber-backed bar mat with a full-colour printed top",
     "Dye-sublimation printed in-house in North Yorkshire, UK"],
    ["Choose Small (440mm x 330mm) or Large (880mm x 330mm)", "Full-colour dye-sublimation print",
     "Rubber backing to help it grip the bar", "Made to order in our North Yorkshire workshop"],
    ["Sizes: 440mm x 330mm (Small) and 880mm x 330mm (Large)", "Printed by dye-sublimation, so the colours are part of the surface",
     "Rubber-backed", "Designed and made in-house in North Yorkshire"],
]
DELIVERY = [
    "Every bar mat is printed to order in our North Yorkshire workshop and posted out once it’s made. Postage options and costs are shown at checkout.",
    "We make each mat to order here in North Yorkshire. You’ll see the postage options and prices at checkout before you pay.",
    "Your bar runner is printed to order in North Yorkshire and then sent on its way – postage choices and costs are at checkout.",
]
DISCLAIMER_BRAND = ("This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {b}. "
                    "{b} is a trademark of its owner and is used only to describe the design theme.")


def esc(s):
    return s.replace("&", "&amp;") if "&amp;" not in s else s


def h(s):
    return esc(s)


def fields_sentence(fields):
    clean = [re.sub(r"\s*\(.*?\)", "", f).lower() for f in fields]
    if len(clean) == 1:
        return clean[0]
    return ", ".join(clean[:-1]) + " and " + clean[-1]


def description(p, i):
    pk = p["primary"]
    g = p["group"]
    b = [BANK[(i + k * 3) % len(BANK)] for k in range(3)]
    if g == "GB":
        opening = (f"This {pk} puts your own badge and club name on the bar, in proper team colours. {p['hook']}")
        h2 = f"A {pk} with your badge and name"
        how = ("Upload your club badge and it’s printed in the circles at both ends of the mat. Type the club or team name for the big middle line, "
               "and if you like, change the ‘Welcome to’ line and add the year the club was formed. Leave the optional boxes blank and we keep the design as shown. "
               f"You can see it all come together in the live preview. {NO_PROOF} Please only upload badges your club has the right to use.")
        spec = [p['colour_note'].rstrip('.'), "Your own club badge printed twice, so it reads from either end of the bar"]
        close = p["close"] + f" Questions about your {pk}? Ring us on 01439 771468."
    elif p["personalised"]:
        opening = (f"Give their home bar a name with this {pk}. {p['look']}")
        h2 = f"Your {pk}, made to order"
        how = (f"Fill in the {fields_sentence(p['fields'])} and we print it into the design for you, on whichever size you choose. "
               f"{p.get('how', 'The rest of the artwork stays exactly as shown in the photos.')} Watch it update in the live preview as you type. {NO_PROOF}")
        spec = [p.get("b1") or f"A {p['design'].lower()} design you won’t find in the supermarket",
                "Your wording is printed into the artwork, not stuck on, so it won’t peel off"]
        close = (p.get("close") or "Pair it with a personalised pint glass or a home bar sign to finish the corner.") + f" Every {pk} is made to order, so allow for that when you’re planning a gift."
    else:
        opening = (f"This {pk} is a fun finishing touch for any home bar, garden bar or man cave. {p['look']}")
        h2 = f"The {pk} for your home bar"
        how = ("This one is printed exactly as shown, so there’s nothing to fill in – just pick your size. The small 440mm mat sits neatly on a shelf or drinks trolley, "
               "while the 880mm runner stretches along a proper bar top. Want your own name or wording added? Give us a ring on 01439 771468 and we’ll talk you through it.")
        spec = [p.get("b1") or f"A ready-to-go {p['design'].lower()} design that needs no personalising",
                "Nothing to fill in, so it’s quick to order as a last-minute gift"]
        close = (p.get("close") or "Pair it with a set of pint glasses for a ready-made gift.") + f" Our {pk} is printed to order, just like everything else we make."
    bullets = spec + b
    det = DETAILS[i % 3]
    parts = [f"<p>{h(opening)}</p>", f"<h2>{h(h2[0].upper() + h2[1:])}</h2>", f"<p>{h(how)}</p>", "<h3>Why you’ll love it</h3>", "<ul>"]
    parts += [f"<li>{h(x)}</li>" for x in bullets]
    parts += ["</ul>", "<h3>Size &amp; details</h3>", "<ul>"] + [f"<li>{h(x)}</li>" for x in det] + ["</ul>"]
    parts += ["<h3>Delivery</h3>", f"<p>{h(DELIVERY[i % 3])}</p>", f"<p>{h(close)}</p>"]
    if p.get("brand"):
        parts += ["<h3>Please note</h3>", f"<p class=\"disclaimer\">{h(DISCLAIMER_BRAND.format(b=p['brand']))}</p>"]
    return "\n".join(parts)


def tcase(s):
    small = {"and", "or", "with", "for", "of", "in", "a", "the", "to"}
    w = s.split()
    return " ".join(x if (i and x in small) else (x[0].upper() + x[1:]) for i, x in enumerate(w))


PAD = [" Order yours today.", " A great gift.", " Made just for you.", " Ideal for a home bar."]


def fit(d):
    for extra in [""] + PAD:
        for extra2 in [""] + PAD:
            t = (d + extra + (extra2 if extra2 != extra else "")).strip()
            if 140 <= len(t) <= 155:
                return t
    return d


def seo(p):
    if p["group"] == "GB":
        t = p["seo_title"]
        if len(t) > 60:
            t = t.replace(" Club Bar Mat", " Bar Mat")
    else:
        t = f"{tcase(p['primary'])} | Foxy Printing".replace("O’clock", "O’Clock")
        if len(t) > 60:
            t = f"{p['design']} Bar Mat | Foxy Printing"
    dn = p["design"].replace(" Club", "").lower()
    if p["group"] == "GB":
        d = (f"Your club badge and name on a {dn} bar mat runner. Rubber-backed and printed in North Yorkshire, in 440mm or 880mm sizes.")
    elif p["personalised"]:
        d = (f"Add your {fields_sentence(p['fields'])} to this {dn} bar mat. Rubber-backed, printed to order in North Yorkshire, in 440mm or 880mm sizes.")
    else:
        d = (f"The {dn} bar mat runner for home bars, garden bars and man caves. Rubber-backed and printed to order in North Yorkshire.")
    return t, fit(d)


def build():
    out = []
    seen = set()
    for i, p in enumerate(P):
        assert p["handle"] not in seen; seen.add(p["handle"])
        st, sd = seo(p)
        sku1, sku2 = f"FOXY-SUB-{p['code']}-01", f"FOXY-SUB-{p['code']}-02"
        tags = sorted(set(["Bar Mat", "bar runner", "home bar", "range-home-bar", "foxy-new-2026", "machine-sublimation",
                           "bar-mats-2026-10-08"] + p["extra_tags"] + (["personalised"] if p["personalised"] else [])
                          + (["third-party-name"] if p.get("brand") else [])))
        mf = [
            {"namespace": "mm-google-shopping", "key": "custom_product", "type": "boolean", "value": "true"},
            {"namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
            {"namespace": "mm-google-shopping", "key": "google_product_category", "type": "single_line_text_field", "value": CAT},
            {"namespace": "mm-google-shopping", "key": "gender", "type": "single_line_text_field", "value": "unisex"},
            {"namespace": "mm-google-shopping", "key": "age_group", "type": "single_line_text_field", "value": "adult"},
            {"namespace": "mm-google-shopping", "key": "color", "type": "single_line_text_field", "value": p["colour"]},
            {"namespace": "mm-google-shopping", "key": "mpn", "type": "single_line_text_field", "value": sku1},
        ]
        if p["personalised"]:
            mf += [{"namespace": "foxy", "key": "mockup", "type": "single_line_text_field", "value": "photo"},
                   {"namespace": "foxy", "key": "personalise_fields", "type": "list.single_line_text_field",
                    "value": json.dumps(p["fields"], ensure_ascii=False)}]
        prod = {
            "title": p["title"], "handle": p["handle"], "descriptionHtml": description(p, i),
            "vendor": "Foxy Printing", "productType": "Bar Mat", "status": "ACTIVE", "tags": tags,
            "seo": {"title": st, "description": sd},
            "productOptions": [{"name": "Size", "values": [{"name": SMALL}, {"name": LARGE}]}],
            "metafields": mf,
        }
        if p["personalised"]:
            prod["templateSuffix"] = "personalised"
        out.append({"key": p["key"], "group": p["group"], "code": p["code"], "product": prod,
                    "variants": [{"size": SMALL, "sku": sku1, "price": p["price"][0]},
                                 {"size": LARGE, "sku": sku2, "price": p["price"][1]}],
                    "channels": p["channels"], "dropbox_sources": p["dropbox"], "img": p.get("img"),
                    "primary": p["primary"], "design": p["design"]})
    return out


if __name__ == "__main__":
    out = build()
    problems = []
    for o in out:
        pr = o["product"]
        words = len(re.sub("<[^>]+>", " ", pr["descriptionHtml"]).split())
        if len(pr["title"]) > 150: problems.append((o["key"], "title"))
        if len(pr["seo"]["title"]) > 60: problems.append((o["key"], "seo title", len(pr["seo"]["title"])))
        if not 120 <= len(pr["seo"]["description"]) <= 160: problems.append((o["key"], "meta", len(pr["seo"]["description"])))
        if not 180 <= words <= 350: problems.append((o["key"], "words", words))
        for bad in ("official", "licensed", "authentic", "genuine", "endorsed by", "merchandise"):
            if bad in pr["descriptionHtml"].lower() and "Please note" not in pr["descriptionHtml"]:
                problems.append((o["key"], bad))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(len(out), "products;", "problems:", problems)
