"""Wheelie bin sticker listings (5 Oct 2026).

Builds the copy fixes for the 30 live "Personalised Wheelie Bin Sticker – Design N"
listings and writes GraphQL mutation files (productUpdate + metafields only, never
productSet).

Facts come from plan/product-facts.md ("Wheelie bin stickers"):
A5 (210 x 148 mm), laminated outdoor vinyl that lasts 5+ years outside.
The owner dropped the colour choice, so all colour wording goes.
Design 2 is "74 Make Believe Close" (the listing photo), not the 39 Carnaughton Place PDF.

Usage: python3 tools/wheelie_bins.py  -> exports/wheelie-bins/old_updates.json + .gql batches
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
BEFORE = ROOT / "exports/rollback/2026-10-05-wheelie-bins/before.json"
OUT = ROOT / "exports/wheelie-bins"

FIELDS = ["House number", "Street name"]

PARA_FIX = {
    "Type in the details you want, such as your house number and street name, in the boxes above the Add to Basket button and choose your colours.":
        "Type in the details you want, such as your house number and street name, in the boxes above the Add to Basket button.",
    "Fill in your number and street in the boxes above the Add to Basket button and choose a colour scheme to suit your bins.":
        "Fill in your number and street in the boxes above the Add to Basket button and we’ll set them in this design for you.",
    "Just add your house number, your street name and the colours you like. We cut and print your pair to order.":
        "Just add your house number and your street name. We cut and print your pair to order.",
    "Pop your house number and street name into the boxes above the Add to Basket button and pick your colours.":
        "Pop your house number and street name into the boxes above the Add to Basket button.",
}
LI_FIX = {
    "Choose colours to match your door, bins or house sign": "Laminated so it keeps looking smart for 5+ years outdoors",
    "Pick the colours that suit your home": "Laminated so it keeps looking smart for 5+ years outdoors",
    "Personalised with your house number, street name and colours": "Personalised with your house number and street name",
    "Sticker size, vinyl type and outdoor life: please call us before ordering if you need exact details":
        "Size: A5, 210 × 148 mm per sticker</li>\n<li>Material: laminated outdoor vinyl that lasts 5+ years outside",
}
SEO_FIX = {
    "Make your bin easy to spot: a pair of personalised wheelie bin stickers (design {n}) with your number, street and colours. Made in-house in the UK.":
        "Make your bin easy to spot: a pair of personalised wheelie bin stickers (design {n}) with your number and street, on A5 laminated outdoor vinyl.",
}


def fix_desc(n, html):
    for a, b in PARA_FIX.items():
        html = html.replace(f"<p>{a}</p>", f"<p>{b}</p>")
    for a, b in LI_FIX.items():
        html = html.replace(f"<li>{a}</li>", f"<li>{b}</li>")
    if n == 2:
        html = html.replace("39 Carnaughton Place", "74 Make Believe Close")
    # if the "why" list now has the vinyl bullet and the specs list too, that's fine (different sections)
    return html


def fix_seo(n, desc):
    for a, b in SEO_FIX.items():
        if desc == a.format(n=n):
            return b.format(n=n)
    return desc


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ps = json.load(open(BEFORE))
    rows = []
    for p in sorted(ps, key=lambda p: int(p["handle"].rsplit("-", 1)[1])):
        n = int(p["handle"].rsplit("-", 1)[1])
        html = fix_desc(n, p["descriptionHtml"])
        seo_d = fix_seo(n, p["seo"]["description"])
        bad = re.findall(r"colou?r|A6|call us before ordering|Carnaughton", html, re.I)
        assert not bad, (n, bad)
        assert "A5, 210 × 148 mm" in html and "5+ years" in html, n
        assert not re.search(r"colou?r", seo_d, re.I), n
        words = len(re.sub(r"<[^>]+>", " ", html).split())
        rows.append({"n": n, "id": p["id"], "descriptionHtml": html,
                     "seo": {"title": p["seo"]["title"], "description": seo_d},
                     "words": words, "meta_len": len(seo_d)})
    json.dump(rows, open(OUT / "old_updates.json", "w"), indent=1, ensure_ascii=False)
    fields = json.dumps(json.dumps(FIELDS, ensure_ascii=False), ensure_ascii=False)
    for i in range(0, 30, 10):
        parts = []
        for r in rows[i:i + 10]:
            parts.append(
                f'u{r["n"]}: productUpdate(product:{{id:"{r["id"]}", descriptionHtml:{json.dumps(r["descriptionHtml"], ensure_ascii=False)}, '
                f'seo:{{title:{json.dumps(r["seo"]["title"])}, description:{json.dumps(r["seo"]["description"])}}}, '
                f'metafields:[{{namespace:"foxy", key:"personalise_fields", type:"list.single_line_text_field", value:{fields}}}]}}) '
                f'{{ userErrors {{ field message }} }}')
        (OUT / f"old_updates_{i + 1}.gql").write_text("mutation { " + " ".join(parts) + " }")
    for r in rows:
        print(r["n"], r["words"], r["meta_len"])


if __name__ == "__main__":
    main()
