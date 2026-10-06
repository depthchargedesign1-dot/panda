"""Rude number plate mugs (Foxy Printing, owner's request 6 Oct 2026).

10 adult-humour registrations in OUR existing full-wrap number plate style (number_plate_mugs.py):
one yellow plate across the 200 x 70 mm wrap (206 x 76 mm with 3 mm bleed), 5 country bands
(GB, Scotland, Wales, Northern Ireland, Ireland), no EU stars. Same files as the v2 zips:
SVG (live text), PDF, MIRRORED PDF, 300 dpi PNG (pHYs), README, PRINT NOTES, Fonts.

Run:  python3 tools/artwork/rude_number_plate_mugs.py              (artwork, zips, textures, products.json)
      python3 tools/artwork/rude_number_plate_mugs.py ebay URLS.json (eBay CSV, separate file)

Rude product rules: the swear word is never spelled out in titles, SEO, meta or alt text - only the
plate as written. Adult humour, not for children. Not published to Google & YouTube, Facebook &
Instagram or TikTok (profanity restrictions) - Online Store and Shop only.
"""
import csv
import html
import json
import os
import re
import shutil
import sys

import number_plate_mugs as npm
from number_plate_mugs import COUNTRIES, PRICE, slug

OUT = os.path.join(npm.ROOT, "exports", "rude-number-plate-mugs")

FACTS = dict(  # MUGS fact sheet only (plan/product-facts.md)
    details=[
        "White ceramic mug, 11oz (approx. 325ml)",
        "C-shaped handle and a high-gloss finish",
        "Sublimation printed in-house in North Yorkshire",
        "Dishwasher and microwave safe – avoid abrasive scourers",
        "Novelty plate design – not a real or road-legal registration",
        "Adult humour – not suitable for children",
    ],
    delivery="Every mug is printed to order in our North Yorkshire workshop and sent out in protective packaging for UK delivery.",
)

COMMON_BULLETS = [
    "One long yellow number plate printed right round the mug, so the joke reads from every side",
    "Pick the band that suits them – GB with the Union flag, Scotland with the saltire and SCO, Wales with the dragon and CYM, Northern Ireland with NI lettering, or Ireland with the tricolour and IRL",
    "Sublimation printed onto an 11oz white ceramic mug, dishwasher and microwave safe for everyday brews",
]

ADULT_NOTE = "Please note: this is an adult humour mug with rude wording, so it isn’t one for children or the kids’ cupboard."

# swear = also tagged for the "Rude Swear Word Mugs" smart collection (tag "Swear Word Mugs")
D = [
    dict(reg=("A33", "HOI3"), gift="Funny Adult Banter Gift", primary="rude number plate mug", swear=True,
         seo_title="Rude Number Plate Mug – A33 HOI3 | Foxy Printing",
         meta="A rude number plate mug reading A33 HOI3 for the mate who has it coming. Pick a GB, Scotland, Wales, NI or Ireland band. Adult humour, printed in the UK.",
         opening="This rude number plate mug is for the mate who winds everybody up and somehow still gets invited to everything. It reads A33 HOI3 on a proper yellow plate, and anyone who has ever squinted at a cheeky private reg will get it in about two seconds.",
         h2="A rude number plate mug for the group chat legend",
         para="A33 HOI3 is printed on one long yellow number plate that wraps right round the mug, with the country band of your choice on the left: GB, Scotland, Wales, Northern Ireland or Ireland. We let the plate do the talking – no rude words spelled out, just numbers standing in for letters the way the best banter plates do. It’s a novelty design, not a real registration, so there’s no DVLA paperwork involved.",
         bullets=["A banter gift for birthdays, Secret Santa or the lads’ weekend away", "Sits on a desk looking innocent until somebody reads it properly"],
         closing="Pair this rude number plate mug with a card that’s just as cheeky for a birthday they won’t forget.",
         tags=["banter gift", "gift for mates"]),
    dict(reg=("B3LL", "3ND"), gift="Cheeky Gift for Mates", primary="cheeky mug for mates", swear=True,
         seo_title="Cheeky Mug for Mates – B3LL 3ND Plate | Foxy Printing",
         meta="A cheeky mug for mates styled like a UK number plate reading B3LL 3ND. Choose a GB, Scotland, Wales, NI or Ireland band. Adult banter, printed in the UK.",
         opening="Every friendship group has one, and this cheeky mug for mates tells them so with love. The yellow plate reads B3LL 3ND – a classic bit of British banter dressed up as a private registration.",
         h2="The cheeky mug for mates who can take a joke",
         para="We print B3LL 3ND on a single yellow number plate that runs all the way round the mug, so the joke is on show from every angle. Choose a GB, Scotland, Wales, Northern Ireland or Ireland band to match where they’re from. It’s a novelty number plate, not a real one, and the rude bit is left for the reader to work out.",
         bullets=["Made for best mates, brothers and five-a-side teammates", "A funny leaving do or birthday gift that gets a proper laugh"],
         closing="Fill it with their favourite sweets and it’s a ready-made banter gift for a birthday or Secret Santa.",
         tags=["banter gift", "gift for mates"]),
    dict(reg=("8008", "I3S"), gift="Rude Birthday Gift", primary="rude birthday mug", swear=False,
         seo_title="Rude Birthday Mug – 8008 I3S Plate | Foxy Printing",
         meta="A rude birthday mug with a UK number plate reading 8008 I3S – the calculator joke everyone knows. Choose a GB, Scotland, Wales, NI or Ireland band.",
         opening="This rude birthday mug brings back the oldest joke from the back of the maths class. The plate reads 8008 I3S, and anyone who ever turned a calculator upside down will be grinning before the kettle boils.",
         h2="A rude birthday mug with a schoolyard classic",
         para="8008 I3S is printed on a big yellow number plate that wraps round the whole mug, with the country band you pick: GB, Scotland, Wales, Northern Ireland or Ireland. It’s cheeky rather than crude, and it’s a novelty plate rather than a real registration – no number cruncher required.",
         bullets=["A daft birthday gift for anyone who never really grew up", "Gets a giggle in the staffroom, the workshop or the uni flat"],
         closing="A cheeky Secret Santa idea too – pop it in with a bag of sweets and wait for the reactions.",
         tags=["birthday mug", "secret santa gift"]),
    dict(reg=("CL1", "NT"), gift="Very Rude Adult Humour Gift", primary="very rude mug", swear=True,
         seo_title="Very Rude Mug – CL1 NT Number Plate | Foxy Printing",
         meta="A very rude mug for adults only, styled like a UK number plate reading CL1 NT. Choose a GB, Scotland, Wales, NI or Ireland band. Strong adult humour.",
         opening="This very rude mug is for a very particular friend – the one whose sense of humour would make a builder blush. The plate reads CL1 NT, and it doesn’t need any more explaining than that.",
         h2="A very rude mug for strictly grown-up banter",
         para="CL1 NT is printed on one long yellow number plate that goes right round the mug, with a GB, Scotland, Wales, Northern Ireland or Ireland band on the end. This is the strongest plate in our rude range, so please choose your recipient carefully – it’s meant for close mates with a filthy sense of humour, not your nan. It’s a novelty design and not a real registration.",
         bullets=["The ultimate in-joke mug for best friends who swear like sailors", "A shock-value Secret Santa for an office that’s definitely in on the joke"],
         closing="Strong stuff – if you’d like something a bit softer, have a look at the rest of our rude number plate mugs.",
         tags=["very rude mug", "offensive mug"]),
    dict(reg=("D1K", "H34D"), gift="Rude Secret Santa Gift", primary="rude Secret Santa mug", swear=True,
         seo_title="Rude Secret Santa Mug – D1K H34D | Foxy Printing",
         meta="A rude Secret Santa mug with a UK number plate design reading D1K H34D. Pick a GB, Scotland, Wales, NI or Ireland band for an adult office gift.",
         opening="If you’ve drawn the office wind-up in the Christmas draw, this rude Secret Santa mug says what everyone’s thinking, on a plate that reads D1K H34D.",
         h2="The rude Secret Santa mug they’ll actually use",
         para="D1K H34D runs round the mug on a single yellow number plate, and you choose the band: GB, Scotland, Wales, Northern Ireland or Ireland. Numbers stand in for the letters, so it reads like a cheeky private plate rather than shouting the word at you. It’s a novelty number plate, not a real registration.",
         bullets=["Comfortably under most Secret Santa budgets", "A funny birthday or leaving gift for a mate who loves a bit of stick"],
         closing="Wrap it with a bag of chocolate coins and you’ve sorted the office Secret Santa.",
         tags=["secret santa gift", "office mug"]),
    dict(reg=("N0B", "H34D"), gift="Rude Gift for Him", primary="rude mug for him", swear=True,
         seo_title="Rude Mug for Him – N0B H34D Number Plate | Foxy Printing",
         meta="A rude mug for him styled like a UK number plate reading N0B H34D. Choose a GB, Scotland, Wales, NI or Ireland band – a cheeky gift for brothers and mates.",
         opening="This rude mug for him is for the brother, husband or best mate who’s a lovable idiot most of the time. The plate reads N0B H34D, which is exactly what you’ve been calling him for years.",
         h2="A rude mug for him with a proper plate layout",
         para="We print N0B H34D on a long yellow number plate that wraps right round the mug, with a GB, Scotland, Wales, Northern Ireland or Ireland band – your choice. It’s cheeky British banter rather than anything nasty, and it’s a novelty plate, not a real registration.",
         bullets=["A birthday or Father’s Day gift for the joker of the family", "Perfect for the van, the garage or the work canteen"],
         closing="Add a funny card and it’s a birthday gift for your brother that he’ll keep using.",
         tags=["gift for him", "banter gift"]),
    dict(reg=("P3N", "15"), gift="Rude Joke Gift", primary="rude joke mug", swear=False,
         seo_title="Rude Joke Mug – P3N 15 Number Plate | Foxy Printing",
         meta="A rude joke mug styled like a UK number plate that reads P3N 15. Pick a GB, Scotland, Wales, NI or Ireland band – a cheeky adult gift for hen and stag dos.",
         opening="Some jokes never get old, and this rude joke mug proves it. The plate reads P3N 15 – say it out loud and you’ll see why it’s the most snorted-at reg in the car park.",
         h2="A rude joke mug that reads like a real plate",
         para="P3N 15 is printed on one long yellow number plate that wraps round the mug, with the band of your choice on the end: GB, Scotland, Wales, Northern Ireland or Ireland. The numbers do the work, so it looks like a perfectly normal registration until someone reads it properly. It’s a novelty design, not a real plate.",
         bullets=["A giggle-worthy gift for hen dos, stag dos and birthday banter", "Looks innocent from a distance – the best kind of rude"],
         closing="A great add-on for a hen do bag or a cheeky birthday hamper.",
         tags=["hen do gift", "stag do gift"]),
    dict(reg=("T05", "53R"), gift="Rude Leaving Gift", primary="rude leaving gift", swear=True,
         seo_title="Rude Leaving Gift Mug – T05 53R Plate | Foxy Printing",
         meta="A rude leaving gift mug with a UK number plate design reading T05 53R. Choose a GB, Scotland, Wales, NI or Ireland band – adult banter for the leaving do.",
         opening="Looking for a rude leaving gift that sums up years of desk-side banter? This mug does it in one plate: T05 53R.",
         h2="A rude leaving gift with a number plate twist",
         para="T05 53R is printed on a long yellow number plate that runs all the way round the mug, with a GB, Scotland, Wales, Northern Ireland or Ireland band. Pass it round the leaving card and everybody will know who it’s for. It’s a novelty plate rather than a real registration, and the insult is all in good fun.",
         bullets=["Gives the leaving do a laugh before the speeches start", "Also works as a birthday wind-up for a sibling or best friend"],
         closing="Pair it with a signed leaving card and a box of biscuits for the full send-off.",
         tags=["leaving gift", "office mug"]),
    dict(reg=("W4N", "K3R"), gift="Funny Adult Banter Gift", primary="adult humour mug", swear=True,
         seo_title="Adult Humour Mug – W4N K3R Number Plate | Foxy Printing",
         meta="An adult humour mug styled like a UK number plate that reads W4N K3R. Pick a GB, Scotland, Wales, NI or Ireland band – the classic insult for your mates.",
         opening="This adult humour mug is the classic British insult, delivered as a private plate. It reads W4N K3R, and there isn’t a pub in the country where that needs translating.",
         h2="An adult humour mug for the classic wind-up",
         para="W4N K3R wraps all the way round the mug on one big yellow number plate, with the country band you choose: GB, Scotland, Wales, Northern Ireland or Ireland. Swapping the numbers in keeps it cheeky rather than crude, and it’s a novelty number plate, not a real registration.",
         bullets=["A banter gift for brothers, best mates and the whole Sunday league team", "Gets the biggest laugh at a 30th, 40th or 50th birthday"],
         closing="Put one in every stocking on the lads’ Christmas night out – a banter gift that keeps on giving.",
         tags=["banter gift", "gift for mates"]),
    dict(reg=("W3T", "W1P3"), gift="Rude Office Gift", primary="rude office mug", swear=False,
         seo_title="Rude Office Mug – W3T W1P3 Number Plate | Foxy Printing",
         meta="A rude office mug made like a UK number plate reading W3T W1P3. Choose a GB, Scotland, Wales, NI or Ireland band – a cheeky gift for the team softie.",
         opening="This rude office mug is for the colleague who moans about the air con and won’t go out in the rain. It gives them the plate they deserve: W3T W1P3.",
         h2="A rude office mug for the team softie",
         para="W3T W1P3 is printed on a single yellow number plate that goes right round the mug, with a GB, Scotland, Wales, Northern Ireland or Ireland band on the end. It’s more cheeky than filthy, so it’s a gentler pick from our rude range, but it’s still an adult humour mug. The plate is a novelty design, not a real registration.",
         bullets=["A wind-up gift for the colleague who always complains about the cold", "Ideal for Secret Santa, birthdays or a promotion leaving do"],
         closing="Pair it with a pack of hand warmers and a box of tissues for the full wind-up gift.",
         tags=["office mug", "secret santa gift"]),
]

EXTRA_TAGS = ["rude", "adult-humour", "rude-mugs", "number-plate-mug", "no-kids", "ADULT MUGS (RUDE)",
              "range-rude-number-plate-mugs", "rude number plate mug"]


def reg_text(d):
    return " ".join(d["reg"])


def title(d):
    return f"Rude Number Plate Mug – {reg_text(d)} – {d['gift']} – 11oz Ceramic"


def short_title(d):
    return f"Rude Number Plate Mug – {reg_text(d)}"


_TAKEN = set()


def sku_base(d):  # build_plan.sku convention: FOXY-<machine>-<title initials, 8 max>
    if "_sku" not in d:
        base = "FOXY-SUB-" + "".join(w[0] for w in slug(title(d)).split("-"))[:8].upper()
        cand, n = base, 2
        while cand in _TAKEN:
            cand, n = f"{base}{n}", n + 1
        _TAKEN.add(cand)
        d["_sku"] = cand
    return d["_sku"]


def description(d):
    li = lambda xs: "".join(f"<li>{html.escape(x, quote=False)}</li>" for x in xs)
    e = lambda s: html.escape(s, quote=False)
    return (f"<p>{e(d['opening'])}</p>"
            f"<h2>{e(d['h2'][0].upper() + d['h2'][1:])}</h2>"
            f"<p>{e(d['para'])}</p>"
            f"<p>{e(ADULT_NOTE)}</p>"
            f"<h3>Why you’ll love it</h3><ul>{li(d['bullets'] + COMMON_BULLETS)}</ul>"
            f"<h3>Size &amp; details</h3><ul>{li(FACTS['details'])}</ul>"
            f"<h3>Delivery</h3><p>{e(FACTS['delivery'])}</p>"
            f"<p>{e(d['closing'])}</p>")


def _patch():
    """point the shared artwork helpers at this range's titles/SKUs"""
    npm.title = title
    npm.sku_base = sku_base
    npm.reg_text = reg_text


def build():
    import cairosvg
    _patch()
    npm.FM = npm._font_metrics()
    art_root, zip_root, tex_root = (os.path.join(OUT, x) for x in ("artwork", "zips", "textures"))
    for p in (art_root, zip_root, tex_root):
        shutil.rmtree(p, ignore_errors=True)
        os.makedirs(p)
    products, problems = [], []
    for i, d in enumerate(D, 1):
        sb = sku_base(d)
        folder = os.path.join(art_root, f"{sb} {reg_text(d)}")
        os.makedirs(folder)
        files = []
        for country in COUNTRIES:
            stem = f"{sb} {reg_text(d)} {country[3]} - 11oz full wrap 206x76mm"
            svg = npm.wrap_svg(d, country)
            open(os.path.join(folder, stem + ".svg"), "w").write(svg)
            cairosvg.svg2pdf(bytestring=svg.encode(), write_to=os.path.join(folder, stem + ".pdf"))
            cairosvg.svg2pdf(bytestring=npm.wrap_svg(d, country, mirrored=True).encode(),
                             write_to=os.path.join(folder, stem + " - MIRRORED.pdf"))
            cairosvg.svg2png(bytestring=svg.encode(), dpi=300, write_to=os.path.join(folder, stem + " - 300dpi.png"))
            npm.png_set_dpi(os.path.join(folder, stem + " - 300dpi.png"))
            files.append(stem)
            tsvg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
                    f'width="{npm.TRIM_W:g}mm" height="{npm.TRIM_H:g}mm" viewBox="{npm.BLEED:g} {npm.BLEED:g} {npm.TRIM_W:g} {npm.TRIM_H:g}">'
                    + npm.plate_svg(d, country, npm.PLATE_CX[0], npm.YELLOW, "plate") + "</svg>")
            cairosvg.svg2png(bytestring=tsvg.encode(), dpi=300,
                             write_to=os.path.join(tex_root, f"{sb}-{country[1]}-wrap.png"))
        open(os.path.join(folder, "README - how to print.txt"), "w").write(
            npm.README.format(title=title(d), sku=sb, reg=reg_text(d)))
        zpath = os.path.join(zip_root, f"{sb}-rude-number-plate-mug-full-wrap-artwork.zip")
        npm.make_zip(d, folder, zpath)
        desc = description(d)
        words = len(re.sub("<[^>]+>", " ", desc).split())
        t = title(d)
        pk = d["primary"].lower()
        checks = [(len(t) <= 150, f"title {len(t)}"), (len(d["seo_title"]) <= 60, f"seo title {len(d['seo_title'])}"),
                  (140 <= len(d["meta"]) <= 155, f"meta {len(d['meta'])}"), (180 <= words <= 350, f"words {words}"),
                  (desc.lower().count(pk) >= 2, "primary kw count"),
                  (pk in re.split(r"(?<=[.!?:])\s", d["opening"])[0].lower(), "primary in 1st sentence"),
                  (pk in d["h2"].lower(), "primary in h2")]
        for ok, msg in checks:
            if not ok:
                problems.append(f"{reg_text(d)}: {msg}")
        tags = BASE_TAGS + EXTRA_TAGS + d["tags"] + [pk] + (["Swear Word Mugs"] if d["swear"] else [])
        products.append(dict(
            n=i, reg=reg_text(d), title=t, short_title=short_title(d), handle=slug(f"rude number plate mug {reg_text(d)}"),
            sku_base=sb, skus={c[0]: f"{sb}-{k:02d}" for k, c in enumerate(COUNTRIES, 1)},
            productType="Mugs", vendor="Foxy Printing", price=PRICE,
            tags=sorted(set(tags), key=str.lower),
            seo=dict(title=d["seo_title"], description=d["meta"]), descriptionHtml=desc, words=words,
            primary=d["primary"], zip=os.path.relpath(zpath, npm.ROOT), artwork_files=files,
            dropbox_folder=f"/AI DESIGNS 2026/{short_title(d)} - {sb}-01",
            google=dict(custom_product="true", condition="new",
                        google_product_category="Home & Garden > Kitchen & Dining > Tableware > Drinkware > Mugs",
                        gender="unisex", age_group="adult", color="Multicolor", mpn=f"{sb}-01"),
            alt=dict(
                main=f"Two views of the {reg_text(d)} rude number plate mug: the GB band end and the far end of the yellow plate printed round a white 11oz ceramic mug",
                flat=f"Flat view of the full {reg_text(d)} yellow number plate artwork with a GB band, as printed round the rude number plate mug",
                **{c[0]: f"Rude number plate mug with a {reg_text(d)} yellow plate wrapping round a white 11oz ceramic mug, {c[0]} band"
                   for c in COUNTRIES})))
    json.dump(products, open(os.path.join(OUT, "products.json"), "w"), indent=1, ensure_ascii=False)
    proofs = []
    for d in D:
        for country in COUNTRIES:
            p = os.path.join("/tmp", f"proof-{sku_base(d)}-{country[1]}.png")
            cairosvg.svg2png(bytestring=npm.wrap_svg(d, country, guides=True).encode(), dpi=60, write_to=p)
            proofs.append(p)
    os.system("convert " + " ".join(f"'{p}'" for p in proofs) + f" -bordercolor '#999' -border 1 miff:- | "
              f"montage - -tile 5x10 -geometry +2+2 '{OUT}/proof-sheet.png'")
    print("\n".join(problems) or "all copy checks passed")
    for p in products:
        print(p["sku_base"], p["reg"], "|", p["title"], len(p["title"]), "|", p["words"], "words |", len(p["seo"]["description"]))


BASE_TAGS = npm.BASE_TAGS


def ebay(urls_path):
    """Separate eBay CSV for the rude range (eBay restricts profanity in titles - see README)."""
    products = json.load(open(os.path.join(OUT, "products.json")))
    urls = json.load(open(urls_path))
    outdir = os.path.join(npm.ROOT, "exports", "ebay", "number-plate-mugs")
    head = ["*Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193)", "CustomLabel", "*Category", "*Title",
            "*ConditionID", "*C:Brand", "C:Type", "C:Material", "C:Capacity", "C:Colour", "C:Theme", "C:Features",
            "C:Care Instructions", "C:Country/Region of Manufacture", "Relationship", "RelationshipDetails",
            "PicURL", "*Description", "*Format", "*Duration", "*StartPrice", "*Quantity", "*Location",
            "ShippingProfileName", "ReturnProfileName", "PaymentProfileName"]
    rows = []
    for p in products:
        u = urls.get(p["sku_base"])
        if not u:
            continue
        short = f"Rude Number Plate Mug {p['reg']} Adult Humour Banter Gift 11oz Ceramic"
        assert len(short) <= 80, short
        desc = re.sub(r"\s+", " ", p["descriptionHtml"]).replace('"', "'")
        rows.append({head[0]: "Add", "CustomLabel": p["sku_base"], "*Category": "",
                     "*Title": short, "*ConditionID": "1000", "*C:Brand": "Foxy Printing", "C:Type": "Mug",
                     "C:Material": "Ceramic", "C:Capacity": "11oz", "C:Colour": "White",
                     "C:Theme": "Novelty", "C:Features": "Dishwasher Safe|Microwave Safe",
                     "C:Care Instructions": "Dishwasher Safe", "C:Country/Region of Manufacture": "United Kingdom",
                     "RelationshipDetails": "Country=" + ";".join(c[0] for c in COUNTRIES),
                     "PicURL": "|".join([u["main"], u["GB"]] + u.get("extra", [])[:10]),
                     "*Description": npm.EBAY_HTML.format(h=html.escape(p["title"]), body=desc),
                     "*Format": "FixedPrice", "*Duration": "GTC", "*StartPrice": "", "*Quantity": "",
                     "*Location": "North Yorkshire, UK"})
        for c in COUNTRIES:
            rows.append({"Relationship": "Variation", "RelationshipDetails": f"Country={c[0]}",
                         "CustomLabel": p["skus"][c[0]], "*StartPrice": PRICE, "*Quantity": "10",
                         "PicURL": f"Country={c[0]}|{u[c[0]]}"})
    path = os.path.join(outdir, "rude-number-plate-mugs-ebay.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=head)
        w.writeheader()
        w.writerows(rows)
    print("wrote", path, len(rows), "rows")


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    if len(sys.argv) > 1 and sys.argv[1] == "ebay":
        ebay(sys.argv[2])
    else:
        build()
