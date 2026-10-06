"""Personalised "ANY NAME" number plate mug (Foxy Printing, Oct 2026).

Same look as the funny number plate mug range (number_plate_mugs.py): one yellow UK-style plate
round an 11oz mug, country band (GB / Scotland / Wales / Northern Ireland / Ireland). Here the
plate text is the CUSTOMER'S text, plus an optional small "dealer line" along the bottom of the
plate (like the supplier name on a real plate). Both are live, editable text in the SVG/PDF.

Run (from foxyprinting-rebrand/):
  python3 tools/artwork/any_name_number_plate_mug.py
      -> listing artwork with the sample text, textures for mockups, blank plate for the live
         preview, zip, product.json  (exports/any-name-number-plate-mug/)
  python3 tools/artwork/any_name_number_plate_mug.py order --text "DAV3 5" --country Wales \
          [--dealer "Dad's Garage"] --out "ORDER 1234"
      -> print files for one order (SVG, PDF, MIRRORED PDF, 300 dpi PNG)

Wrap: 200 x 70 mm + 3 mm bleed = 206 x 76 mm, 3 mm safe area (plan/artwork-specs.md).
Font: Barlow Condensed (SIL OFL 1.1). Novelty plate - not a real registration.
"""
import argparse
import html
import json
import os
import re
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import number_plate_mugs as npm  # noqa: E402  (shared plate geometry, flags, fonts, PNG dpi stamp)

ROOT = npm.ROOT
OUT = os.path.join(ROOT, "exports", "any-name-number-plate-mug")
SAMPLE = "Y0UR N4ME"
PRICE = "8.99"
TITLE = "Personalised Number Plate Mug – Any Name or Text – Custom Reg Gift – 11oz Ceramic"
SKU = "FOXY-SUB-PNPMANOT"
FIELDS = ["Your plate text (max 8 characters)", "Dealer line on the plate (optional, e.g. Dad’s Garage)"]
_cmaps = {}


def tw(s, size, weight="700"):
    """Text width in mm for any character (full cmap, not only A-Z0-9)."""
    from fontTools.ttLib import TTFont
    if weight not in _cmaps:
        f = {"600": "BarlowCondensed-SemiBold.ttf", "700": "BarlowCondensed-Bold.ttf"}[weight]
        t = TTFont(os.path.join(npm.ASSETS, "fonts", f))
        _cmaps[weight] = (t.getBestCmap(), t["hmtx"], t["head"].unitsPerEm, t["OS/2"].sCapHeight / t["head"].unitsPerEm)
    cmap, hmtx, upm, _ = _cmaps[weight]
    adv = sum(hmtx[cmap.get(ord(c), cmap[ord("?")])][0] for c in s) / upm
    return adv * size + npm.LS * size * (len(s) - 1)


def cap_ratio(weight="700"):
    tw("A", 1, weight)
    return _cmaps[weight][3]


def clean_plate(text):
    """UK plate style: capitals, digits and single spaces only."""
    t = re.sub(r"[^A-Z0-9 ]", "", (text or "").upper())
    return re.sub(r"\s+", " ", t).strip()


def plate_svg(text, dealer, country, uid="plate"):
    """The full-wrap plate with the customer's text (live) and optional dealer line (live)."""
    _, code, flag, _ = country
    W, H = npm.PLATE_W, npm.PLATE_H
    cx, cy = npm.TRIM_W / 2 + npm.BLEED, npm.TRIM_H / 2 + npm.BLEED
    L, T = cx - W / 2, cy - H / 2
    R, B = L + W, T + H
    bw = 30.0
    s = [f'<g id="{uid}" inkscape:groupmode="layer" inkscape:label="Number plate (full wrap)">',
         f'<clipPath id="{uid}c"><rect x="{L:.3f}" y="{T:.3f}" width="{W}" height="{H}" rx="7"/></clipPath>',
         f'<rect x="{L:.3f}" y="{T:.3f}" width="{W}" height="{H}" rx="7" fill="{npm.YELLOW}" stroke="#8A8A8A" stroke-width="0.25"/>',
         f'<g clip-path="url(#{uid}c)"><rect x="{L:.3f}" y="{T:.3f}" width="{bw}" height="{H}" fill="{npm.BLUE}"/></g>']
    bx = L + bw / 2
    if flag:
        fw = bw - 7.0
        fs, _ = npm.flag_svg(flag, bx - fw / 2, T + 7.0, fw, uid + "f")
        s.append(fs)
        csize = 10.0 / cap_ratio()
        s.append(f'<text x="{bx:.3f}" y="{B - 7.0:.3f}" font-family="Barlow Condensed" font-weight="700" '
                 f'font-size="{csize:.3f}" fill="#FFFFFF" text-anchor="middle">{code}</text>')
    else:  # Northern Ireland: lettering only (owner's rule)
        csize = 16.0 / cap_ratio()
        s.append(f'<text x="{bx:.3f}" y="{cy + 8.0:.3f}" font-family="Barlow Condensed" font-weight="700" '
                 f'font-size="{csize:.3f}" fill="#FFFFFF" text-anchor="middle">{code}</text>')
    x0, x1 = L + bw + 4.0, R - 5.0
    mid = (x0 + x1) / 2
    has_dealer = bool((dealer or "").strip())
    if text:
        cap = H * (0.64 if has_dealer else 0.72)
        size = cap / cap_ratio()
        while tw(text, size) > (x1 - x0) * 0.94 and size > 1:
            size *= 0.97
        cap = size * cap_ratio()
        centre_y = cy - (3.2 if has_dealer else 0)
        s.append(f'<text id="Plate text" data-field="Your plate text" x="{mid:.3f}" y="{centre_y + cap / 2:.3f}" '
                 f'font-family="Barlow Condensed" font-weight="700" font-size="{size:.3f}" '
                 f'letter-spacing="{npm.LS * size:.3f}" fill="{npm.INK}" text-anchor="middle" '
                 f'xml:space="preserve">{html.escape(text)}</text>')
    if has_dealer:
        d = dealer.strip()
        dsize = 3.4 / cap_ratio("600")
        while tw(d, dsize, "600") > (x1 - x0) * 0.8 and dsize > 1:
            dsize *= 0.96
        s.append(f'<text id="Dealer line" data-field="Dealer line" x="{mid:.3f}" y="{B - 4.6:.3f}" '
                 f'font-family="Barlow Condensed" font-weight="600" font-size="{dsize:.3f}" fill="{npm.INK}" '
                 f'text-anchor="middle">{html.escape(d)}</text>')
    s.append(f'<rect x="{L + 2.2:.3f}" y="{T + 2.2:.3f}" width="{W - 4.4:.3f}" height="{H - 4.4:.3f}" '
             f'rx="5.2" fill="none" stroke="{npm.INK}" stroke-width="1.0"/></g>')
    return "\n".join(s)


def wrap_svg(text, dealer, country, mirrored=False, guides=False):
    PW, PH = npm.PAGE_W, npm.PAGE_H
    content = (f'<g id="Background" inkscape:groupmode="layer" inkscape:label="Background (bleed)">'
               f'<rect width="{PW}" height="{PH}" fill="#FFFFFF"/></g>\n' + plate_svg(text, dealer, country))
    if mirrored:
        content = f'<g transform="translate({PW},0) scale(-1,1)">{content}</g>'
    g = (f'<g id="Guides" inkscape:groupmode="layer" inkscape:label="Guides (do not print)" '
         f'style="display:{"inline" if guides else "none"}" fill="none" stroke-width="0.2">'
         f'<rect x="{npm.BLEED}" y="{npm.BLEED}" width="{npm.TRIM_W}" height="{npm.TRIM_H}" stroke="#00AEEF" stroke-dasharray="2,1"/>'
         f'<rect x="{npm.BLEED + npm.SAFE}" y="{npm.BLEED + npm.SAFE}" width="{npm.TRIM_W - 2 * npm.SAFE}" '
         f'height="{npm.TRIM_H - 2 * npm.SAFE}" stroke="#EC008C" stroke-dasharray="1,1"/></g>')
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<!-- Foxy Printing | {TITLE} | {country[0]} | 11oz sublimation wrap: trim {npm.TRIM_W:g} x {npm.TRIM_H:g} mm, '
            f'bleed {npm.BLEED:g} mm (page {PW:g} x {PH:g} mm), safe area {npm.SAFE:g} mm. Font: Barlow Condensed (SIL OFL 1.1). '
            f'Personalise: edit the text objects "Plate text" and "Dealer line". -->\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            f'width="{PW:g}mm" height="{PH:g}mm" viewBox="0 0 {PW:g} {PH:g}">\n{content}\n{g}\n</svg>\n')


def texture(text, dealer, country, path):
    import cairosvg
    t = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
         f'width="{npm.TRIM_W:g}mm" height="{npm.TRIM_H:g}mm" viewBox="{npm.BLEED:g} {npm.BLEED:g} {npm.TRIM_W:g} {npm.TRIM_H:g}">'
         + plate_svg(text, dealer, country) + "</svg>")
    cairosvg.svg2png(bytestring=t.encode(), dpi=300, write_to=path)


def print_files(text, dealer, country, folder, stem):
    import cairosvg
    os.makedirs(folder, exist_ok=True)
    svg = wrap_svg(text, dealer, country)
    open(os.path.join(folder, stem + ".svg"), "w").write(svg)
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=os.path.join(folder, stem + ".pdf"))
    cairosvg.svg2pdf(bytestring=wrap_svg(text, dealer, country, mirrored=True).encode(),
                     write_to=os.path.join(folder, stem + " - MIRRORED.pdf"))
    png = os.path.join(folder, stem + " - 300dpi.png")
    cairosvg.svg2png(bytestring=svg.encode(), dpi=300, write_to=png)
    npm.png_set_dpi(png)
    return stem


README = """Foxy Printing - {title}
SKU {sku}-01 to -05 (GB, Scotland, Wales, Northern Ireland, Ireland)  |  PERSONALISED: customer's plate text

PERSONALISING AN ORDER
  Fast:    python3 tools/artwork/any_name_number_plate_mug.py order --text "DAV3 5" --country Wales --dealer "Dad's Garage" --out "ORDER 1234"
  By hand: open the country's .svg (or .pdf) in Illustrator, edit the text object "Plate text" (and "Dealer line",
           or delete it if the customer left it blank). Text is centred; shrink it if it runs past the plate border.
  The order's line item shows: "Your plate text (max 8 characters)" and "Dealer line on the plate (optional...)".

FILES (one set per country band; sample text {sample})
  ... .svg            editable master (live text, layers: Background / Number plate (full wrap) / Guides)
  ... .pdf            print file, 206 x 76 mm (200 x 70 mm wrap + 3 mm bleed each edge)
  ... - MIRRORED.pdf  same, flipped - only if your print driver/RIP does NOT mirror sublimation transfers
  ... - 300dpi.png    2433 x 898 px, tagged 300 dpi

Spec: 11oz white sublimation mug, FULL WRAP: print area 200 x 70 mm + 3 mm bleed = 206 x 76 mm, 3 mm safe area.
One yellow plate (194 x 64 mm) runs right round the mug; band at the left end. Print at 100% (actual size).
Colours: plate #FFD100, band #003DA5, text #111111.
Font: Barlow Condensed Bold + SemiBold (SIL Open Font License 1.1) - Fonts folder. Install before editing.
Wales flag: flag-icons (MIT). Novelty plate design - not a real or road-legal registration.
"""


def description():
    e = lambda s: html.escape(s, quote=False)
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    return (
        "<p>Our personalised number plate mug puts any name, nickname or in-joke on a proper UK-style yellow plate, "
        "so it finally gets the registration it deserves. It’s a brilliant personalised gift for car lovers, new drivers, "
        "dads, grandads and anyone who has ever wanted their own private plate.</p>"
        "<h2>A personalised number plate mug with their name on</h2>"
        "<p>Type the text you want on the plate – a name like DAV3, a nickname, initials or a short phrase. Up to 8 letters "
        "and digits looks just like a real plate; we print it exactly as you type it, in capitals. You can also add an "
        "optional dealer line along the bottom of the plate, such as “Dad’s Garage” or “Est. 1965”. The live preview shows "
        "your text on the plate as you type. Then choose the band: GB with the Union flag, Scotland with the saltire and SCO, "
        "Wales with the dragon and CYM, Northern Ireland with NI lettering, or Ireland with the tricolour and IRL.</p>"
        "<h3>Why you’ll love it</h3><ul>"
        + li(["Any name or text on one long yellow plate that wraps right round the mug, so it reads from every side",
              "Optional dealer line for a cheeky extra – a family garage name, a year or a nickname",
              "A custom number plate gift that costs a fraction of a real private plate",
              "Matches our funny number plate mug range, so you can make a set for the whole family",
              "Sublimation printed onto an 11oz white ceramic mug, dishwasher and microwave safe for everyday brews"])
        + "</ul><h3>Size &amp; details</h3><ul>" + li(npm.FACTS["details"]) + "</ul>"
        f"<h3>Delivery</h3><p>{e(npm.FACTS['delivery'])}</p>"
        "<p>Pair your personalised number plate mug with one of our funny number plate mugs, like D4D T4X1, for a matching "
        "car lover gift.</p>")


SEO_TITLE = "Personalised Number Plate Mug – Any Name | Foxy Printing"
META = ("Put any name or text on a UK-style number plate mug. Choose a GB, Scotland, Wales, NI or Ireland band – "
        "a personalised gift for car lovers and dads.")


def build():
    import cairosvg
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    art, tex, extra = (os.path.join(OUT, x) for x in ("artwork", "textures", "extra-textures"))
    for p in (art, tex, extra):
        os.makedirs(p)
    stems = []
    for country in npm.COUNTRIES:
        stems.append(print_files(SAMPLE, "", country, art, f"{SKU} {country[3]} - 11oz full wrap 206x76mm (sample {SAMPLE})"))
        texture(SAMPLE, "", country, os.path.join(tex, f"{SKU}-{country[1]}-wrap.png"))
    gb = npm.COUNTRIES[0]
    texture("", "", gb, os.path.join(extra, "blank-GB-wrap.png"))                    # live preview base
    texture("D4V3", "DAD’S GARAGE", gb, os.path.join(extra, "dealer-GB-wrap.png"))  # dealer line example
    for i, (t, c) in enumerate((("J4CK 5", 1), ("M1LLY", 2), ("GR4NDAD", 3))):     # example names
        texture(t, "", npm.COUNTRIES[c], os.path.join(extra, f"example{i + 1}-wrap.png"))
    open(os.path.join(art, "README - how to print.txt"), "w").write(README.format(title=TITLE, sku=SKU, sample=SAMPLE))
    zpath = os.path.join(OUT, f"{SKU}-personalised-number-plate-mug-artwork.zip")
    top = f"{TITLE} - {SKU}-01"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(art)):
            z.write(os.path.join(art, f), f"{top}/{f}")
        z.write(os.path.abspath(__file__), f"{top}/any_name_number_plate_mug.py (order generator).txt")
        for f in npm.ZIP_FONTS:
            z.write(os.path.join(npm.ASSETS, "fonts", f), f"{top}/Fonts/{f}")
        z.write(os.path.join(npm.ASSETS, "flag-icons-LICENSE.txt"), f"{top}/Fonts/flag-icons (Wales flag) LICENSE.txt")
    proofs = []
    for country in npm.COUNTRIES:
        p = f"/tmp/anpm-proof-{country[1]}.png"
        cairosvg.svg2png(bytestring=wrap_svg(SAMPLE, "", country, guides=True).encode(), dpi=60, write_to=p)
        proofs.append(p)
    p = "/tmp/anpm-proof-dealer.png"
    cairosvg.svg2png(bytestring=wrap_svg("GR4NDAD", "EST. 1958", gb, guides=True).encode(), dpi=60, write_to=p)
    proofs.append(p)
    os.system("convert " + " ".join(proofs) + " -bordercolor '#999' -border 1 miff:- | "
              f"montage - -tile 2x3 -geometry +4+4 '{OUT}/proof-sheet.png'")
    desc = description()
    words = len(re.sub("<[^>]+>", " ", desc).split())
    checks = {"title<=150": len(TITLE) <= 150, "seo<=60": len(SEO_TITLE) <= 60, "meta 140-155": 140 <= len(META) <= 155,
              "words 180-350": 180 <= words <= 350,
              "primary in 1st sentence/h2/x3": desc.lower().count("personalised number plate mug") >= 3}
    product = dict(
        title=TITLE, handle="personalised-number-plate-mug-any-name", sku_base=SKU, price=PRICE,
        skus={c[0]: f"{SKU}-{k:02d}" for k, c in enumerate(npm.COUNTRIES, 1)},
        productType="Mugs", vendor="Foxy Printing", templateSuffix="personalised",
        tags=sorted(set(npm.BASE_TAGS + ["personalised", "personalised-mugs", "personalised number plate mug",
                                         "custom number plate mug", "name mug", "gift for dad", "io-number-plate-mugs"])),
        seo=dict(title=SEO_TITLE, description=META), descriptionHtml=desc, words=words,
        personalise_fields=FIELDS, checks=checks, zip=os.path.relpath(zpath, ROOT),
        dropbox_folder=f"/AI DESIGNS 2026/{TITLE} - {SKU}-01",
        google=dict(custom_product="true", condition="new",
                    google_product_category="Home & Garden > Kitchen & Dining > Tableware > Drinkware > Mugs",
                    gender="unisex", age_group="adult", color="White", mpn=f"{SKU}-01"))
    json.dump([product], open(os.path.join(OUT, "products.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: product[k] for k in ("title", "skus", "words", "checks")}, indent=1, ensure_ascii=False))
    print("lengths: title", len(TITLE), "seo", len(SEO_TITLE), "meta", len(META))


def order(a):
    country = next((c for c in npm.COUNTRIES if a.country.lower() in (c[0].lower(), c[1].lower(), c[3].lower())), None)
    if not country:
        sys.exit("country must be GB, Scotland, Wales, Northern Ireland or Ireland")
    text = clean_plate(a.text)
    if not text:
        sys.exit("plate text is empty after cleaning (letters, digits and spaces only)")
    stem = f"{SKU}-{npm.COUNTRIES.index(country) + 1:02d} {text} {country[3]} - 11oz full wrap 206x76mm"
    print_files(text, a.dealer or "", country, a.out, stem)
    print("wrote", os.path.join(a.out, stem), "(.svg .pdf - MIRRORED.pdf - 300dpi.png)")
    if text != (a.text or "").strip().upper():
        print(f"NOTE: plate text cleaned to {text!r} (only A-Z, 0-9 and spaces print on the plate)")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "order":
        ap = argparse.ArgumentParser()
        ap.add_argument("cmd")
        ap.add_argument("--text", required=True)
        ap.add_argument("--country", default="GB")
        ap.add_argument("--dealer", default="")
        ap.add_argument("--out", default="order")
        order(ap.parse_args())
    else:
        build()
