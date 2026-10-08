"""Personalised number plate KEYRING and COASTER SET (Foxy Printing, Oct 2026).

Pairs with the ANY NAME number plate mug (any_name_number_plate_mug.py): same yellow UK-style plate,
same country bands and font (Barlow Condensed, SIL OFL 1.1), customer's own plate text + optional dealer line.

  keyring  - metal keyring, gloss white sublimation insert, "slim rectangle" shape (as the live metal keyring range).
             Print area NOT confirmed by the owner: artwork is vector, built at 60 x 13 mm + 1.5 mm bleed. Scale to
             the insert if it differs.
  coasters - set of 4 glossy MDF 9.5 cm square coasters with cork base. Square two-line plate (like a UK motorcycle
             plate): the text splits over two lines. Trim 95 x 95 mm + 3 mm bleed = 101 x 101 mm.

Run (from foxyprinting-rebrand/):
  python3 tools/artwork/number_plate_keyring_coasters.py                  listing artwork + product renders
  python3 tools/artwork/number_plate_keyring_coasters.py order keyring --text "DAV3 5" --country Wales --out DIR
  python3 tools/artwork/number_plate_keyring_coasters.py order coaster --text "J4CK 5" --country GB [--dealer "..."] --out DIR
"""
import argparse
import html
import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import number_plate_mugs as npm  # noqa: E402
import any_name_number_plate_mug as anpm  # noqa: E402

OUT = os.path.join(npm.ROOT, "exports", "number-plate-keyring-coasters")
SPEC = {
    "keyring": dict(trim=(60.0, 13.0), bleed=1.5, rx=1.6, band=8.6, sku="FOXY-SUB-PNPKAN",
                    title="Personalised Number Plate Keyring – Any Name or Text – Metal Keyring in Gift Box"),
    "coaster": dict(trim=(95.0, 95.0), bleed=3.0, rx=6.0, band=17.0, sku="FOXY-SUB-PNPCSAN",
                    title="Personalised Number Plate Coasters – Any Name – Set of 4 Square Coasters with Cork Base"),
}


def split_two(text):
    """Two-line square plate: split at the space nearest the middle, else in half."""
    if " " in text:
        parts = text.split(" ")
        best = min(range(1, len(parts)), key=lambda i: abs(len(" ".join(parts[:i])) - len(" ".join(parts[i:]))))
        return " ".join(parts[:best]), " ".join(parts[best:])
    return text, ""  # one word stays on one line


def plate(kind, text, dealer, country):
    s = SPEC[kind]
    W, H = s["trim"]
    b = s["bleed"]
    PW, PH = W + 2 * b, H + 2 * b
    _, code, flag, _ = country
    L, T, R, B = b, b, b + W, b + H
    bw = s["band"]
    out = [f'<g id="Background" inkscape:groupmode="layer" inkscape:label="Background (bleed)">'
           f'<rect width="{PW}" height="{PH}" fill="{npm.YELLOW}"/></g>',
           f'<g id="plate" inkscape:groupmode="layer" inkscape:label="Number plate">',
           f'<rect x="0" y="0" width="{b + bw:.3f}" height="{PH}" fill="{npm.BLUE}"/>']  # band runs into the bleed
    bx = L + bw / 2
    cap = anpm.cap_ratio()
    if kind == "keyring":
        csize = 2.6 / cap
        if flag:
            fw = bw - 2.4
            fs, fh = npm.flag_svg(flag, bx - fw / 2, T + 1.4, fw, "kf")
            out.append(fs)
        out.append(f'<text x="{bx:.3f}" y="{B - 1.3:.3f}" font-family="Barlow Condensed" font-weight="700" '
                   f'font-size="{csize:.3f}" fill="#FFFFFF" text-anchor="middle">{code}</text>')
    else:
        if flag:
            fw = bw - 4.0
            fs, fh = npm.flag_svg(flag, bx - fw / 2, T + 6.0, fw, "cf")
            out.append(fs)
            out.append(f'<text x="{bx:.3f}" y="{B - 6.0:.3f}" font-family="Barlow Condensed" font-weight="700" '
                       f'font-size="{7.0 / cap:.3f}" fill="#FFFFFF" text-anchor="middle">{code}</text>')
        else:
            out.append(f'<text x="{bx:.3f}" y="{(T + B) / 2 + 5.0:.3f}" font-family="Barlow Condensed" font-weight="700" '
                       f'font-size="{10.0 / cap:.3f}" fill="#FFFFFF" text-anchor="middle">{code}</text>')
    x0, x1 = L + bw + (1.2 if kind == "keyring" else 4.0), R - (1.5 if kind == "keyring" else 5.0)
    mid = (x0 + x1) / 2
    has_dealer = bool((dealer or "").strip())
    ls = lambda size: npm.LS * size

    def fit(t, cap_mm, maxw):
        size = cap_mm / cap
        while anpm.tw(t, size) > maxw and size > 0.5:
            size *= 0.97
        return size

    if text:
        if kind == "keyring":
            size = fit(text, H * 0.66, (x1 - x0) * 0.95)
            base = T + H / 2 + size * cap / 2
            out.append(f'<text id="Plate text" x="{mid:.3f}" y="{base:.3f}" font-family="Barlow Condensed" font-weight="700" '
                       f'font-size="{size:.3f}" letter-spacing="{ls(size):.3f}" fill="{npm.INK}" text-anchor="middle" '
                       f'xml:space="preserve">{html.escape(text)}</text>')
        else:
            l1, l2 = split_two(text)
            area_top, area_bot = T + 7.0, B - (13.0 if has_dealer else 7.0)
            gap = 5.0
            if l2:
                capmm = (area_bot - area_top - gap) / 2
                size = min(fit(l1, capmm, (x1 - x0) * 0.95), fit(l2, capmm, (x1 - x0) * 0.95))
                c = size * cap
                y1 = area_top + (area_bot - area_top - (2 * c + gap)) / 2 + c
                y2 = y1 + gap + c
            else:
                size = fit(l1, (area_bot - area_top) * 0.45, (x1 - x0) * 0.95)
                c = size * cap
                y1 = area_top + (area_bot - area_top) / 2 + c / 2
                y2 = y1
            for tid, t, y in (("Plate text line 1", l1, y1), ("Plate text line 2", l2, y2)):
                if t:
                    out.append(f'<text id="{tid}" x="{mid:.3f}" y="{y:.3f}" font-family="Barlow Condensed" font-weight="700" '
                               f'font-size="{size:.3f}" letter-spacing="{ls(size):.3f}" fill="{npm.INK}" '
                               f'text-anchor="middle" xml:space="preserve">{html.escape(t)}</text>')
    if has_dealer and kind == "coaster":
        d = dealer.strip()
        dsize = fit(d, 3.0, (x1 - x0) * 0.85) if False else 3.0 / anpm.cap_ratio("600")
        while anpm.tw(d, dsize, "600") > (x1 - x0) * 0.85:
            dsize *= 0.96
        out.append(f'<text id="Dealer line" x="{mid:.3f}" y="{B - 6.0:.3f}" font-family="Barlow Condensed" font-weight="600" '
                   f'font-size="{dsize:.3f}" fill="{npm.INK}" text-anchor="middle">{html.escape(d)}</text>')
    ins = 1.0 if kind == "keyring" else 3.0
    out.append(f'<rect x="{L + ins:.3f}" y="{T + ins:.3f}" width="{W - 2 * ins:.3f}" height="{H - 2 * ins:.3f}" '
               f'rx="{max(s["rx"] - ins, 0.5):.3f}" fill="none" stroke="{npm.INK}" '
               f'stroke-width="{0.35 if kind == "keyring" else 0.9}"/></g>')
    guides = (f'<g id="Guides" inkscape:groupmode="layer" inkscape:label="Guides (do not print)" style="display:none" '
              f'fill="none" stroke-width="0.15"><rect x="{L}" y="{T}" width="{W}" height="{H}" rx="{s["rx"]}" '
              f'stroke="#00AEEF" stroke-dasharray="1,0.5"/></g>')
    svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<!-- Foxy Printing | {s["title"]} | {country[0]} | trim {W:g} x {H:g} mm '
           f'+ {b:g} mm bleed (page {PW:g} x {PH:g} mm). Font: Barlow Condensed (SIL OFL 1.1). Personalise: edit "Plate text". -->\n'
           f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
           f'width="{PW:g}mm" height="{PH:g}mm" viewBox="0 0 {PW:g} {PH:g}">\n' + "\n".join(out) + "\n" + guides + "\n</svg>\n")
    return svg, (PW, PH)


def files(kind, text, dealer, country, folder, stem):
    import cairosvg
    os.makedirs(folder, exist_ok=True)
    svg, (PW, PH) = plate(kind, text, dealer, country)
    open(os.path.join(folder, stem + ".svg"), "w").write(svg)
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=os.path.join(folder, stem + ".pdf"))
    mir = svg.replace('<g id="Background"', f'<g transform="translate({PW},0) scale(-1,1)"><g id="Background"', 1) \
             .replace('\n<g id="Guides"', '</g>\n<g id="Guides"', 1)
    cairosvg.svg2pdf(bytestring=mir.encode(), write_to=os.path.join(folder, stem + " - MIRRORED.pdf"))
    png = os.path.join(folder, stem + " - 300dpi.png")
    cairosvg.svg2png(bytestring=svg.encode(), dpi=300, write_to=png)
    npm.png_set_dpi(png)
    return png


# ---------------------------------------------------------------- product renders (PIL, white background)
def render_keyring(png, path, size=2048):
    from PIL import Image, ImageDraw, ImageFilter
    art = Image.open(png).convert("RGB")
    N = size
    img = Image.new("RGB", (N, N), "white")
    w = int(N * 0.66); h = int(w * art.height / art.width)
    fw, fh = w + 110, h + 110                          # metal frame around the insert
    fx, fy = (N - fw) // 2 + 150, (N - fh) // 2
    sh = Image.new("L", (N, N), 0)
    ImageDraw.Draw(sh).rounded_rectangle((fx + 20, fy + 40, fx + fw + 20, fy + fh + 40), 70, fill=120)
    img.paste((160, 160, 160), (0, 0), sh.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(img)
    for i, c in enumerate(range(200, 150, -5)):        # brushed metal frame with a soft bevel
        d.rounded_rectangle((fx + i, fy + i, fx + fw - i, fy + fh - i), 70 - i, fill=(c, c, c + 4))
    d.rounded_rectangle((fx + 40, fy + 40, fx + fw - 40, fy + fh - 40), 40, fill=(235, 235, 238))
    a = art.resize((w, h), Image.LANCZOS)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), 18, fill=255)
    img.paste(a, (fx + 55, fy + 55), m)
    # jump ring + split ring on the left
    cx, cy = fx - 40, fy + fh // 2
    d.ellipse((cx - 70, cy - 30, cx + 10, cy + 30), outline=(150, 150, 155), width=16)
    d.ellipse((cx - 330, cy - 170, cx - 60, cy + 170), outline=(170, 170, 176), width=22)
    d.arc((cx - 330, cy - 170, cx - 60, cy + 170), 200, 320, fill=(225, 225, 230), width=8)
    img.save(path, quality=90)


def render_coasters(pngs, path, size=2048):
    from PIL import Image, ImageDraw, ImageFilter
    N = size
    img = Image.new("RGB", (N, N), "white")
    s = int(N * 0.40)
    pos = [(int(N * 0.08), int(N * 0.08)), (int(N * 0.52), int(N * 0.10)), (int(N * 0.10), int(N * 0.53)), (int(N * 0.53), int(N * 0.55))]
    sh = Image.new("L", (N, N), 0)
    for x, y in pos:
        ImageDraw.Draw(sh).rounded_rectangle((x + 14, y + 26, x + s + 14, y + s + 26), 26, fill=110)
    img.paste((150, 150, 150), (0, 0), sh.filter(ImageFilter.GaussianBlur(24)))
    for (x, y), p in zip(pos, pngs):
        art = Image.open(p).convert("RGB")
        crop = int(art.width * 3 / 101)                 # drop the bleed
        art = art.crop((crop, crop, art.width - crop, art.height - crop)).resize((s, s), Image.LANCZOS)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((x + 6, y + 10, x + s + 6, y + s + 10), 26, fill=(168, 124, 82))   # cork edge
        m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, s, s), 24, fill=255)
        img.paste(art, (x, y), m)
        gl = Image.new("L", (s, s), 0); ImageDraw.Draw(gl).polygon([(0, 0), (int(s * .45), 0), (0, int(s * .45))], fill=38)
        img.paste((255, 255, 255), (x, y), Image.composite(gl, Image.new("L", (s, s), 0), m))  # gloss highlight
    img.save(path, quality=90)


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    renders = os.path.join(OUT, "renders")
    os.makedirs(renders)
    sample = {"keyring": "D4V3 5", "coaster": "J4CK 5"}
    made = {}
    for kind, s in SPEC.items():
        art = os.path.join(OUT, kind, "artwork")
        made[kind] = {}
        for i, country in enumerate(npm.COUNTRIES, 1):
            stem = f"{s['sku']} {country[3]} - {kind} {s['trim'][0]:g}x{s['trim'][1]:g}mm (sample {sample[kind]})"
            made[kind][country[1]] = files(kind, sample[kind], "", country, art, stem)
        open(os.path.join(art, "README - how to print.txt"), "w").write(README[kind].format(title=s["title"], sku=s["sku"]))
        z = os.path.join(OUT, f"{s['sku']}-artwork.zip")
        top = f"{s['title']} - {s['sku']}-01"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(os.listdir(art)):
                zf.write(os.path.join(art, f), f"{top}/{f}")
            zf.write(os.path.abspath(__file__), f"{top}/number_plate_keyring_coasters.py (order generator).txt")
            for f in npm.ZIP_FONTS:
                zf.write(os.path.join(npm.ASSETS, "fonts", f), f"{top}/Fonts/{f}")
            zf.write(os.path.join(npm.ASSETS, "flag-icons-LICENSE.txt"), f"{top}/Fonts/flag-icons (Wales flag) LICENSE.txt")
    for code, n in zip(("GB", "SCO", "CYM", "NI", "IRL"), range(1, 6)):
        render_keyring(made["keyring"][code], os.path.join(renders, f"keyring-{n}-{code}.jpg"))
    cdir = os.path.join(OUT, "coaster", "examples")
    ex = [anpm.clean_plate(t) for t in ("J4CK 5", "M1LLY", "GR4N DAD", "D4V3 5")]
    expngs = [files("coaster", t, "", npm.COUNTRIES[0], cdir, f"ex{i}") for i, t in enumerate(ex)]
    render_coasters(expngs, os.path.join(renders, "coasters-0-set-of-4.jpg"))
    for code, n in zip(("GB", "SCO", "CYM", "NI", "IRL"), range(1, 6)):
        render_coasters([made["coaster"][code]] * 4, os.path.join(renders, f"coasters-{n}-{code}.jpg"))
    shutil.rmtree(cdir)
    print(json.dumps({k: sorted(os.listdir(os.path.join(OUT, k, "artwork"))) for k in SPEC}, indent=1))
    print(sorted(os.listdir(renders)))


README = {
    "keyring": """Foxy Printing - {title}
SKU {sku}-01 to -05 (GB, Scotland, Wales, Northern Ireland, Ireland)  |  PERSONALISED plate text

Blank: metal keyring with gloss white sublimation insert, SLIM RECTANGLE shape, supplied in a gift box.
Artwork: 60 x 13 mm trim + 1.5 mm bleed (63 x 16 mm page). PLEASE CHECK the slim rectangle insert size -
the artwork is vector, so scale it to the insert if it differs (keep the band at the left).
Files per band: editable .svg (live text "Plate text"), .pdf, - MIRRORED.pdf (only if your RIP doesn't mirror), 300dpi.png.
Order: python3 tools/artwork/number_plate_keyring_coasters.py order keyring --text "DAV3 5" --country Wales --out "ORDER 1234"
Font: Barlow Condensed (SIL OFL 1.1), in Fonts. Novelty plate - not a real or road-legal registration.
""",
    "coaster": """Foxy Printing - {title}
SKU {sku}-01 to -05 (GB, Scotland, Wales, Northern Ireland, Ireland)  |  PERSONALISED plate text, set of 4 (same design on all 4)

Blank: glossy MDF square coaster 9.5 cm with cork base (as the live wooden coaster range).
Artwork: 95 x 95 mm trim + 3 mm bleed = 101 x 101 mm page. Square two-line plate: the customer's text splits over
two lines at the space nearest the middle (J4CK 5 -> J4CK / 5). Optional dealer line along the bottom.
Files per band: editable .svg (live text "Plate text line 1/2", "Dealer line"), .pdf, - MIRRORED.pdf, 300dpi.png.
Print 4 per order. Order: python3 tools/artwork/number_plate_keyring_coasters.py order coaster --text "J4CK 5" --country GB --dealer "Est. 1958" --out "ORDER 1234"
Font: Barlow Condensed (SIL OFL 1.1), in Fonts. Novelty plate - not a real or road-legal registration.
""",
}


def order(a):
    country = next((c for c in npm.COUNTRIES if a.country.lower() in (c[0].lower(), c[1].lower(), c[3].lower())), None)
    if not country:
        sys.exit("country must be GB, Scotland, Wales, Northern Ireland or Ireland")
    text = anpm.clean_plate(a.text)
    s = SPEC[a.kind]
    stem = f"{s['sku']}-{npm.COUNTRIES.index(country) + 1:02d} {text} {country[3]} - {a.kind}"
    files(a.kind, text, a.dealer, country, a.out, stem)
    print("wrote", os.path.join(a.out, stem))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "order":
        ap = argparse.ArgumentParser()
        ap.add_argument("cmd"); ap.add_argument("kind", choices=list(SPEC))
        ap.add_argument("--text", required=True); ap.add_argument("--country", default="GB")
        ap.add_argument("--dealer", default=""); ap.add_argument("--out", default="order")
        order(ap.parse_args())
    else:
        build()
