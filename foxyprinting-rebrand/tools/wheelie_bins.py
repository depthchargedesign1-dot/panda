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
    for i in range(0, 30, 5):
        parts = []
        for r in rows[i:i + 5]:
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


# ---------------------------------------------------------------------------
# New listings: Design 31-36 (DRAFT). Pack option Single / Pair / Pack of 4.
# ---------------------------------------------------------------------------
HF = "https://d2ol7oe51mr4n9.cloudfront.net/user_3HUr7G8la20J0fiH66SaF8cNGi7/"
HFG = "https://d8j0ntlcm91z4.cloudfront.net/user_3HUr7G8la20J0fiH66SaF8cNGi7/"
TAGS = ["bin sticker", "foxy-new-2026", "foxy-src-dropbox", "house number sticker", "io-home-gifts",
        "machine-cut", "new home gift", "outdoor sticker", "personalised", "range-wheelie-bin",
        "wheelie bin sticker"]
PACKS = [("Single", "4.99", "01"), ("Pair", "8.99", "02"), ("Pack of 4", "14.99", "03")]
GOOGLE_CATEGORY = "Home & Garden > Decor > Home Decor Decals"  # per coordinator brief 5 Oct 2026

NEW = {
    31: dict(
        mock="6a0fb8df-303f-4c6d-9867-7bd01fd102ad.jpg", flat="b29f3759-6780-4ba2-815b-236755d0732f.jpg",
        life="hf_20261005_171057_522eed69-cfeb-492a-ba0c-923a203eccd7.png",
        flat_alt="Design 31 flat A5 sticker: the number 68 and the name Sarcel framed by tall floral vines",
        life_alt="Design 31 sticker on a green wheelie bin next to a front door and a potted plant",
        sample="68 Sarcel",
        intro="Give your bin a touch of the cottage garden with this personalised wheelie bin sticker, framed on both sides by tall, curling floral vines.",
        style="Design 31 sets a big, classic house number in the middle with the name or street underneath, so it suits a short street name or even a house name. Our sample reads “68 Sarcel”.",
        why=["Elegant floral vines that make a plain bin look cared for",
             "Large house number that’s easy to spot from the pavement",
             "Room for a short street or house name underneath"],
        close="Got a matching door sign or house plaque? This floral style sits nicely alongside it.",
        meta="Floral personalised wheelie bin sticker with your house number and street name. A5 laminated outdoor vinyl that lasts 5+ years. Single, pair or 4-pack."),
    32: dict(
        mock="93077eea-9e90-47fe-96a4-49a8a64a42ed.jpg", flat="a61bb07f-7d2a-4295-8346-89ac6f94b2db.jpg",
        life="hf_20261005_172649_438dfc6d-66b4-4c8c-886b-72e161524254.png",
        flat_alt="Design 32 flat A5 sticker: Hospital Drove across the top above a large number 6 with ornate floral scrolls",
        life_alt="Design 32 sticker on a black wheelie bin beside a stone cottage wall with roses",
        sample="Hospital Drove above a large 6",
        intro="This personalised wheelie bin sticker flips the usual layout: your street name runs across the top and the house number sits large in the centre, wrapped in ornate floral scrolls.",
        style="It works brilliantly for single and double-digit numbers, where a big, bold figure really stands out. Our sample shows “Hospital Drove” above the number 6.",
        why=["Street name across the top, so it reads like a proper house sign",
             "Ornate scrolls give a traditional, period feel",
             "Big centre number that’s easy to see on collection day"],
        close="Lovely for older houses and cottages, and a thoughtful little extra for anyone who’s just moved in.",
        meta="Ornate personalised wheelie bin sticker with your street name over a big house number. A5 laminated outdoor vinyl, lasts 5+ years. Single, pair or 4-pack."),
    33: dict(
        mock="651bf068-bddb-46dc-b073-ed1a2200fca5.jpg", flat="52347ea6-bc3b-4136-8a85-8cf2aad79940.jpg",
        life="hf_20261005_171057_c104c67c-56e5-4445-8507-2c7cadf32b63.png",
        flat_alt="Design 33 flat A5 sticker: number 28 inside a laurel wreath with a small heart and Gateacre Court below",
        life_alt="Design 33 stickers on green, black, blue and brown wheelie bins on a brick driveway",
        sample="28 Gateacre Court",
        intro="A delicate laurel wreath with a little heart at its base makes this personalised wheelie bin sticker one of our prettiest styles.",
        style="Your house number sits inside the wreath and your street name runs underneath in a soft, classic lettering. Our sample reads “28 Gateacre Court”.",
        why=["Laurel wreath and heart for a gentle, homely look",
             "Number framed in the centre so it stands out",
             "Looks smart on green, black, blue and brown bins alike"],
        close="Pick the pack of 4 and you can match every bin on the drive.",
        meta="Laurel wreath personalised wheelie bin sticker with your house number and street name. A5 laminated outdoor vinyl lasting 5+ years. Single, pair or 4-pack."),
    34: dict(
        mock="72b4c2fd-e207-4f6e-a3d4-f428baa3f26f.jpg", flat="12dce669-efb1-488b-96a1-2a0ddfe4621c.jpg",
        life="hf_20261005_172647_a903f610-5c3c-4801-b2a7-5854238223c1.png",
        flat_alt="Design 34 flat A5 sticker: large number 28 above a fern-leaf wreath with Gateacre Court underneath",
        life_alt="Design 34 sticker on a blue recycling wheelie bin next to a white front door",
        sample="28 Gateacre Court",
        intro="Bold and leafy, this personalised wheelie bin sticker cradles your house number in a sweeping fern wreath.",
        style="The number sits large at the top of the wreath with the street name below, so it reads clearly from the kerb. Our sample shows “28 Gateacre Court”.",
        why=["Sweeping fern leaves with a crisp, graphic finish",
             "Extra-large number at the top of the design",
             "A neat way to tell your bins apart from next door’s"],
        close="A great choice for new-build homes, and a handy housewarming extra for friends who’ve just moved.",
        meta="Fern wreath personalised wheelie bin sticker with your house number and street name. Printed on A5 laminated outdoor vinyl that lasts 5+ years. 1, 2 or 4."),
    35: dict(
        mock="74577660-c96c-4065-ba31-553bb5051cd1.jpg", flat="c47dc438-db3b-40c2-8c2d-6d30c57dd6dc.jpg",
        life="hf_20261005_172648_2ddd3aa7-a57f-404e-9e56-308aa6ff9718.png",
        flat_alt="Design 35 flat A5 sticker: number 28 between curling leaf sprigs with Gateacre Court and a leafy heart line below",
        life_alt="Design 35 sticker on a brown garden waste wheelie bin beside a wooden gate",
        sample="28 Gateacre Court",
        intro="Curling leaf sprigs above and a leafy line with a heart below give this personalised wheelie bin sticker a light, botanical feel.",
        style="There’s no heavy border, so the design feels open and airy, with the house number up top and the street name in the middle. Our sample reads “28 Gateacre Court”.",
        why=["Botanical sprigs and a little heart for a friendly touch",
             "Open layout without a heavy frame",
             "Clear number and street name that are easy to read"],
        close="Pair it with a matching sticker on the garden waste bin so every bin finds its way home.",
        meta="Botanical personalised wheelie bin sticker with leaf sprigs, your house number and street. A5 laminated outdoor vinyl that lasts 5+ years. 1, 2 or 4 pack."),
    36: dict(
        mock="9f04c731-626e-4182-a00c-f034fdd82a07.jpg", flat="73de4914-d3a9-44ad-abd9-02a38792556e.jpg",
        life="hf_20261005_172647_cafeff54-6bfa-4e3d-b2fb-78e63cf398ad.png",
        flat_alt="Design 36 flat A5 sticker: number 28 inside an oak-leaf wreath with Gateacre Court underneath",
        life_alt="Design 36 sticker on a grey wheelie bin on a block-paved drive in front of a semi-detached house",
        sample="28 Gateacre Court",
        intro="Oak leaves are a proper British classic, and this personalised wheelie bin sticker uses them to frame your house number in a full, rounded wreath.",
        style="Your number sits in the centre of the wreath with the street name in clean lettering underneath. Our sample shows “28 Gateacre Court”.",
        why=["Oak-leaf wreath with a timeless, traditional look",
             "House number framed in the centre for easy reading",
             "Smartens up a grey, black or green bin in seconds"],
        close="Ordering for the whole household? The pack of 4 covers general waste, recycling, garden and food bins.",
        meta="Oak leaf personalised wheelie bin sticker with your house number and street name. A5 laminated outdoor vinyl that lasts 5+ years. Single, pair or 4-pack."),
}


def new_desc(n, d):
    why = "".join(f"<li>{w}</li>\n" for w in d["why"])
    return (
        f"<p>{d['intro']} {d['style']}</p>\n"
        f"<h2>Personalised Wheelie Bin Sticker – Design {n}</h2>\n"
        "<p>Type your house number and street name into the boxes above the Add to Basket button and check the preview. "
        "We print and cut your sticker to order in our North Yorkshire workshop, with your details set in this design.</p>\n"
        "<h3>Why you’ll love it</h3>\n<ul>\n" + why +
        "<li>Laminated outdoor vinyl that lasts 5+ years outside</li>\n"
        "<li>Choose a single sticker, a pair or a pack of 4 for every bin you own</li>\n</ul>\n"
        "<h3>Size &amp; details</h3>\n<ul>\n"
        "<li>Size: A5, 210 × 148 mm per sticker</li>\n"
        "<li>Material: laminated outdoor vinyl that lasts 5+ years outside</li>\n"
        "<li>Packs: single, pair (2 stickers) or pack of 4</li>\n"
        "<li>Personalised with your house number and street name</li>\n"
        f"<li>Sample wording shown: {d['sample']}</li>\n</ul>\n"
        "<h3>Delivery</h3>\n"
        "<p>Your stickers are made to order in our North Yorkshire workshop and posted from the UK. "
        "Delivery options and costs are shown at checkout. Any questions, call us on 01439 771468.</p>\n"
        f"<p>{d['close']}</p>")


def build_new():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for n, d in NEW.items():
        html = new_desc(n, d)
        words = len(re.sub(r"<[^>]+>", " ", html).split())
        assert 180 <= words <= 350, (n, words)
        assert 140 <= len(d["meta"]) <= 155, (n, len(d["meta"]))
        assert not re.search(r"colou?r|A6", html, re.I), n
        title = f"Personalised Wheelie Bin Sticker – Design {n}"
        seo_title = f"Personalised Wheelie Bin Sticker Design {n} | Foxy Printing"
        assert len(seo_title) <= 60
        skus = [f"FOXY-CUT-PWBSD{n}-{s}" for _, _, s in PACKS]
        mf = [("foxy", "mockup", "single_line_text_field", "flat"),
              ("foxy", "personalise_fields", "list.single_line_text_field", json.dumps(FIELDS)),
              ("mm-google-shopping", "custom_product", "boolean", "true"),
              ("mm-google-shopping", "condition", "single_line_text_field", "new"),
              ("mm-google-shopping", "google_product_category", "single_line_text_field", GOOGLE_CATEGORY),
              ("mm-google-shopping", "gender", "single_line_text_field", "unisex"),
              ("mm-google-shopping", "age_group", "single_line_text_field", "adult"),
              ("mm-google-shopping", "color", "single_line_text_field", "Multicolor"),
              ("mm-google-shopping", "mpn", "single_line_text_field", skus[0])]
        media = [(HF + d["mock"], f"Personalised wheelie bin sticker design {n} on a green wheelie bin, with the flat A5 sticker in front"),
                 (HF + d["flat"], d["flat_alt"]),
                 (HFG + d["life"], d["life_alt"])]
        rows.append(dict(n=n, title=title, handle=f"personalised-wheelie-bin-sticker-design-{n}",
                         descriptionHtml=html, words=words, seo={"title": seo_title, "description": d["meta"]},
                         tags=TAGS, metafields=mf, media=media, skus=skus))
    json.dump(rows, open(OUT / "new_listings.json", "w"), indent=1, ensure_ascii=False)
    q = lambda s: json.dumps(s, ensure_ascii=False)
    for part, chunk in enumerate([rows[:3], rows[3:]], 1):
        docs = []
        for r in chunk:
            mfs = ", ".join(f"{{namespace:{q(a)}, key:{q(b)}, type:{q(c)}, value:{q(v)}}}" for a, b, c, v in r["metafields"])
            med = ", ".join(f"{{originalSource:{q(u)}, alt:{q(a)}, mediaContentType:IMAGE}}" for u, a in r["media"])
            docs.append(
                f"c{r['n']}: productCreate(product:{{title:{q(r['title'])}, handle:{q(r['handle'])}, status:DRAFT, "
                f"vendor:\"Foxy Printing\", productType:\"Wheelie Bin Stickers\", templateSuffix:\"personalised\", "
                f"tags:{q(r['tags'])}, descriptionHtml:{q(r['descriptionHtml'])}, "
                f"seo:{{title:{q(r['seo']['title'])}, description:{q(r['seo']['description'])}}}, "
                f"productOptions:[{{name:\"Pack\", values:[{{name:\"Single\"}}, {{name:\"Pair\"}}, {{name:\"Pack of 4\"}}]}}], "
                f"metafields:[{mfs}]}}, media:[{med}]) {{ product {{ id handle }} userErrors {{ field message }} }}")
        (OUT / f"new_create_{part}.gql").write_text("mutation { " + " ".join(docs) + " }")
    for r in rows:
        print(r["n"], r["words"], len(r["seo"]["description"]))


if __name__ == "__main__" and "new" in __import__("sys").argv:
    build_new()
