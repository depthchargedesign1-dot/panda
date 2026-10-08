"""Print-ready artwork + local mockups for the products made to fill empty collections (8 Oct 2026).

Five personalised 11oz mugs and one personalised abstract art print. Each design is a short list of
elements (text / circle / rect / arch) in millimetres on the TRIM area. From it we write:
  * <SKU> - PRINT.svg   layers "Artwork" (live text, font-family named) and "Guides" (hidden: bleed, trim, safe)
  * <SKU> - PRINT.pdf   pure-ASCII PDF (A85, uncompressed, subset-embedded OFL fonts), live text, trim box
  * <SKU>-texture.png   300 dpi RGBA texture of the trim area (used for the mug mockups)
  * mockups: main (single mug, handle left), both sides, flat wrap; for the print a flat print image.
Mug wrap: 200 x 70 mm print area + 3 mm bleed = 206 x 76 mm page (plan/artwork-specs.md); the design is
placed twice, centred at 50 mm and 150 mm, so it shows whichever hand holds the mug.
Art print: A4 master 210 x 297 mm + 3 mm bleed; A3/A2/A1 are the same artwork scaled (vector).
Sample name "Ava" kept where the customer types a name (the owner's Illustrator script swaps it).

usage: python3 tools/artwork/empty_collection_products.py OUT_DIR
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "assets", "fonts")
BEBAS = os.path.join(FONTS, "BebasNeue-Regular.ttf")
PACIFICO = os.path.join(FONTS, "Pacifico-Regular.ttf")
FONT_NAME = {BEBAS: "Bebas Neue", PACIFICO: "Pacifico"}
PDF_NAME = {BEBAS: "BebasNeue", PACIFICO: "Pacifico"}
DPI_MM = 300 / 25.4
BLEED = 3.0
SAFE = 3.0

# CMYK-safe brand-ish colours (no neon, no pure RGB primaries)
NAVY = "#1F3A5F"
CORAL = "#D9583B"
MUSTARD = "#D99A1E"
TEAL = "#2A7F7A"
SAGE = "#8FA98B"
CREAM = "#F3EBDD"
TERRA = "#C4643F"


def text_w(font, size_mm, s):
    """width in mm of string s at font size size_mm (em size)"""
    f = ImageFont.truetype(font, 400)
    l, t, r, b = f.getbbox(s)
    return (r - l) / 400 * size_mm


def fit(font, size_mm, s, max_w):
    w = text_w(font, size_mm, s)
    return size_mm if w <= max_w else size_mm * max_w / w


# ------------------------------------------------------------------ designs
def mug_panel(cx, lines):
    """lines: (font, size_mm, text, colour, baseline_y_mm, max_w) -> elements centred on cx"""
    out = []
    for font, size, s, col, y, mw in lines:
        out.append(dict(kind="text", font=font, size=fit(font, size, s, mw), text=s, fill=col, x=cx, y=y))
    return out


def mug_design(lines, extras=()):
    els = []
    for cx in (50.0, 150.0):
        for e in extras:
            e2 = dict(e)
            e2["x"] = e["x"] + cx
            els.append(e2)
        els += mug_panel(cx, lines)
    return els


MW = 80  # max text width per panel (mm); panel is 100 mm, keeps 10 mm each side clear of the other copy

DESIGNS = {
    "TMIAM": dict(  # Trust Me I'm A ... mug
        kind="mug", w=200, h=70,
        els=mug_design([
            (BEBAS, 17, "TRUST ME", NAVY, 20.5, MW),
            (PACIFICO, 9, "I'm a", CORAL, 30.0, MW),
            (BEBAS, 25, "NURSE", CORAL, 51.0, MW),
            (PACIFICO, 8, "Ava", NAVY, 63.8, MW),
        ], extras=[dict(kind="rect", x=-22, y=53.2, w=44, h=0.7, fill=NAVY)])),
    "ILAM3PM": dict(  # I Like ... and maybe 3 people
        kind="mug", w=200, h=70,
        els=mug_design([
            (BEBAS, 14, "I LIKE", NAVY, 18.0, MW),
            (BEBAS, 25, "GARDENING", TEAL, 40.0, MW),
            (BEBAS, 10.5, "AND MAYBE 3 PEOPLE", NAVY, 52.0, MW),
            (PACIFICO, 7, "Ava", CORAL, 63.5, MW),
        ], extras=[dict(kind="circle", x=-30, y=13.5, r=1.6, fill=TEAL), dict(kind="circle", x=30, y=13.5, r=1.6, fill=TEAL)])),
    "IUTDRM": dict(  # I Used To Drive ... retirement mug
        kind="mug", w=200, h=70,
        els=mug_design([
            (BEBAS, 12, "I USED TO DRIVE", NAVY, 14.5, MW),
            (BEBAS, 23, "LORRIES", MUSTARD, 33.5, MW),
            (BEBAS, 12, "NOW I JUST DRIVE", NAVY, 44.5, MW),
            (BEBAS, 12, "EVERYONE MAD", NAVY, 54.5, MW),
            (PACIFICO, 6.5, "Happy retirement, Ava", CORAL, 63.0, MW),
        ])),
    "IGTM": dict(  # I've Got This mug
        kind="mug", w=200, h=70,
        els=mug_design([
            (BEBAS, 26, "I'VE GOT THIS", NAVY, 34.0, MW),
            (PACIFICO, 11, "Ava", CORAL, 50.0, MW),
            (BEBAS, 7.5, "GOOD LUCK IN YOUR NEW JOB", TEAL, 61.0, MW),
        ], extras=[dict(kind="arch", x=0, y=15.0, r=9.0, fill=MUSTARD)])),
    "CBM": dict(  # Cheeky Brew mug
        kind="mug", w=200, h=70,
        els=mug_design([
            (PACIFICO, 13, "Ava's", CORAL, 25.0, MW),
            (BEBAS, 21, "CHEEKY LITTLE", NAVY, 45.0, MW),
            (BEBAS, 21, "BREW", NAVY, 62.0, MW),
        ], extras=[dict(kind="circle", x=-25, y=55.0, r=1.4, fill=CORAL), dict(kind="circle", x=25, y=55.0, r=1.4, fill=CORAL)])),
    "MCAAP": dict(  # Mid-century abstract art print, A4 master (portrait)
        kind="print", w=210, h=297,
        els=[
            dict(kind="bg", fill=CREAM),
            dict(kind="arch", x=78, y=150, r=52, fill=TERRA),
            dict(kind="arch", x=78, y=150, r=34, fill=CREAM),
            dict(kind="arch", x=78, y=150, r=18, fill=MUSTARD),
            dict(kind="circle", x=148, y=78, r=26, fill=MUSTARD),
            dict(kind="circle", x=52, y=62, r=13, fill=SAGE),
            dict(kind="rect", x=30, y=88, w=44, h=4, fill=TERRA),
            dict(kind="rect", x=118, y=104, w=60, h=46, fill=SAGE),
            dict(kind="circle", x=148, y=150, r=30, fill=NAVY, half="top"),
            dict(kind="rect", x=26, y=150, w=158, h=6, fill=NAVY),
            dict(kind="circle", x=56, y=200, r=18, fill=SAGE),
            dict(kind="circle", x=118, y=206, r=12, fill=TERRA),
            dict(kind="rect", x=146, y=186, w=38, h=38, fill=MUSTARD),
            dict(kind="text", font=BEBAS, size=fit(BEBAS, 26, "THE TAYLORS", 150), text="THE TAYLORS", fill=NAVY, x=105, y=262),
            dict(kind="text", font=BEBAS, size=9, text="EST. 2019", fill=TERRA, x=105, y=276),
        ]),
}


# ------------------------------------------------------------------ renderers
def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def render_png(d, pad_bleed=False, scale=DPI_MM):
    W, H = d["w"], d["h"]
    off = BLEED if pad_bleed else 0
    Wp, Hp = round((W + 2 * off) * scale), round((H + 2 * off) * scale)
    img = Image.new("RGBA", (Wp, Hp), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    P = lambda v: (v + off) * scale
    for e in d["els"]:
        col = hexrgb(e["fill"]) + (255,)
        k = e["kind"]
        if k == "bg":
            dr.rectangle([0, 0, Wp, Hp], fill=col)
        elif k == "rect":
            dr.rectangle([P(e["x"]), P(e["y"]), P(e["x"] + e["w"]), P(e["y"] + e["h"])], fill=col)
        elif k == "circle":
            box = [P(e["x"] - e["r"]), P(e["y"] - e["r"]), P(e["x"] + e["r"]), P(e["y"] + e["r"])]
            if e.get("half") == "top":
                dr.pieslice(box, 180, 360, fill=col)
            else:
                dr.ellipse(box, fill=col)
        elif k == "arch":  # half disc sitting on y
            dr.pieslice([P(e["x"] - e["r"]), P(e["y"] - e["r"]), P(e["x"] + e["r"]), P(e["y"] + e["r"])], 180, 360, fill=col)
        elif k == "text":
            f = ImageFont.truetype(e["font"], max(1, round(e["size"] * scale)))
            dr.text((P(e["x"]), P(e["y"])), e["text"], font=f, fill=col, anchor="ms")
    return img


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace("'", "&#39;")


def write_svg(d, path, title):
    W, H = d["w"] + 2 * BLEED, d["h"] + 2 * BLEED
    o = BLEED
    a = [f'<?xml version="1.0" encoding="UTF-8"?>',
         f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">',
         f'<title>{esc(title)}</title>',
         '<g id="Artwork" inkscape:groupmode="layer" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape">']
    for e in d["els"]:
        k, c = e["kind"], e["fill"]
        if k == "bg":
            a.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{c}"/>')
        elif k == "rect":
            a.append(f'<rect x="{e["x"] + o:.2f}" y="{e["y"] + o:.2f}" width="{e["w"]:.2f}" height="{e["h"]:.2f}" fill="{c}"/>')
        elif k == "circle" and e.get("half") != "top":
            a.append(f'<circle cx="{e["x"] + o:.2f}" cy="{e["y"] + o:.2f}" r="{e["r"]:.2f}" fill="{c}"/>')
        elif k in ("arch", "circle"):
            x, y, r = e["x"] + o, e["y"] + o, e["r"]
            a.append(f'<path d="M {x - r:.2f} {y:.2f} A {r:.2f} {r:.2f} 0 0 1 {x + r:.2f} {y:.2f} Z" fill="{c}"/>')
        elif k == "text":
            a.append(f'<text x="{e["x"] + o:.2f}" y="{e["y"] + o:.2f}" font-family="{FONT_NAME[e["font"]]}" '
                     f'font-size="{e["size"]:.2f}" text-anchor="middle" fill="{c}">{esc(e["text"])}</text>')
    a.append('</g>')
    a.append('<g id="Guides" style="display:none">')
    a.append(f'<rect x="{o}" y="{o}" width="{d["w"]}" height="{d["h"]}" fill="none" stroke="#00AEEF" stroke-width="0.2"/>')
    a.append(f'<rect x="{o + SAFE}" y="{o + SAFE}" width="{d["w"] - 2 * SAFE}" height="{d["h"] - 2 * SAFE}" fill="none" stroke="#EC008C" stroke-width="0.2" stroke-dasharray="1 1"/>')
    a.append('</g></svg>')
    open(path, "w").write("\n".join(a))


def write_pdf(d, path, title, scale=1.0):
    from reportlab import rl_config
    rl_config.useA85 = 1
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    for f, n in PDF_NAME.items():
        try:
            pdfmetrics.getFont(n)
        except KeyError:
            pdfmetrics.registerFont(TTFont(n, f))
    s = scale
    W, H = (d["w"] + 2 * BLEED) * s, (d["h"] + 2 * BLEED) * s
    c = canvas.Canvas(path, pagesize=(W * mm, H * mm), pageCompression=1)
    c.setTitle(title)
    c.setAuthor("Foxy Printing")
    o = BLEED
    X = lambda v: (v + o) * s * mm
    Y = lambda v: (H - (v + o) * s) * mm
    for e in d["els"]:
        c.setFillColor(HexColor(e["fill"]))
        k = e["kind"]
        if k == "bg":
            c.rect(0, 0, W * mm, H * mm, stroke=0, fill=1)
        elif k == "rect":
            c.rect(X(e["x"]), Y(e["y"] + e["h"]), e["w"] * s * mm, e["h"] * s * mm, stroke=0, fill=1)
        elif k == "circle" and e.get("half") != "top":
            c.circle(X(e["x"]), Y(e["y"]), e["r"] * s * mm, stroke=0, fill=1)
        elif k in ("arch", "circle"):
            r = e["r"] * s * mm
            c.wedge(X(e["x"]) - r, Y(e["y"]) - r, X(e["x"]) + r, Y(e["y"]) + r, 0, 180, stroke=0, fill=1)
        elif k == "text":
            c.setFont(PDF_NAME[e["font"]], e["size"] * s * mm)
            c.drawCentredString(X(e["x"]), Y(e["y"]), e["text"])
    # trim box marker for RIPs (non-printing info in the page dictionary)
    c.setPageSize((W * mm, H * mm))
    c.showPage()
    c.save()
    ascii_streams(path)
    b = bytearray(open(path, "rb").read())
    for i in range(min(80, len(b))):
        if b[i] >= 128:
            b[i] = ord("~")
    assert all(x < 128 for x in b), "PDF not pure ASCII"
    open(path, "wb").write(bytes(b))


def ascii_streams(path):
    """ReportLab leaves the embedded font file binary: re-wrap every binary stream in ASCII85."""
    import base64
    import pikepdf
    pdf = pikepdf.open(path, allow_overwriting_input=True)
    for obj in pdf.objects:
        if isinstance(obj, pikepdf.Stream):
            raw = obj.read_raw_bytes()
            if any(x >= 128 or (x < 32 and x not in (9, 10, 13)) for x in raw):
                filt = obj.get("/Filter")
                filters = [] if filt is None else (list(filt) if isinstance(filt, pikepdf.Array) else [filt])
                enc = base64.a85encode(raw, wrapcol=76) + b"~>"
                obj.write(enc, filter=[pikepdf.Name.ASCII85Decode] + filters)
    pdf.save(path, compress_streams=False, object_stream_mode=pikepdf.ObjectStreamMode.disable,
             stream_decode_level=pikepdf.StreamDecodeLevel.none)


# ------------------------------------------------------------------ mockups
def mug_mockups(tex_png, out_prefix):
    sys.path.insert(0, HERE)
    import numpy as np
    import number_plate_mug_local_mockups as M
    tex = np.asarray(Image.open(tex_png).convert("RGBA")).astype(np.float32) / 255
    M.single(tex, centre_mm=150.0, handle="left").save(out_prefix + "-1-main.jpg", quality=88)
    # both sides: handle left shows the 150 mm copy, handle right shows the 50 mm copy
    pxmm = 7.9
    ext_h, ext_o = M.mug_extent_mm()
    gap = 170
    w1 = (ext_h + ext_o) * pxmm
    left0 = (M.N - 2 * w1 - gap) / 2
    cx1 = left0 + ext_h * pxmm
    cx2 = left0 + w1 + gap + ext_o * pxmm
    ytop = (M.N - M.MUG_H_MM * pxmm) / 2 - 0.01 * M.N
    M.scene([(cx1 / M.N, ytop / M.N, pxmm, tex, 150.0, "left"),
             (cx2 / M.N, ytop / M.N, pxmm, tex, 50.0, "right")]).save(out_prefix + "-2-both-sides.jpg", quality=88)
    M.flat(tex_png).save(out_prefix + "-3-flat-wrap.jpg", quality=88)


def mug_cutout(tex_png, out_png, size=1400):
    """single mug on a transparent background (for compositing onto lifestyle scenes)"""
    sys.path.insert(0, HERE)
    import numpy as np
    import number_plate_mug_local_mockups as M
    tex = np.asarray(Image.open(tex_png).convert("RGBA")).astype(np.float32) / 255
    N = M.N
    S = N * M.SS
    canvas = np.ones((S, S, 3), np.float32)
    shadow = np.zeros((S, S), np.float32)
    cover = np.zeros((S, S), bool)
    pxmm = 13.6
    ext_h, ext_o = M.mug_extent_mm()
    width = (ext_h + ext_o) * pxmm
    cx = N / 2 + (width / 2 - ext_o * pxmm)
    ytop = (N - M.MUG_H_MM * pxmm) / 2 + 0.035 * N
    M.draw_mug(canvas, shadow, cover, cx * M.SS, ytop * M.SS, pxmm * M.SS, tex, 150.0, "left")
    rgb = Image.fromarray((np.clip(canvas, 0, 1) * 255 + 0.5).astype(np.uint8))
    a = Image.fromarray((cover * 255).astype(np.uint8))
    img = rgb.convert("RGBA")
    img.putalpha(a)
    img = img.resize((N, N), Image.LANCZOS)
    img = img.crop(img.getbbox())
    img.thumbnail((size, size), Image.LANCZOS)
    img.save(out_png)


def print_flat(png_trim, out_jpg, N=2000):
    """art print on white with a soft drop shadow"""
    import numpy as np
    from PIL import ImageFilter
    t = Image.open(png_trim).convert("RGBA")
    h = N - 260
    t = t.resize((round(t.width * h / t.height), h), Image.LANCZOS)
    x, y = (N - t.width) // 2, (N - t.height) // 2
    img = Image.new("RGB", (N, N), (250, 250, 248))
    a = Image.new("L", (N, N), 0)
    a.paste(255, (x + 10, y + 22, x + 10 + t.width, y + 22 + t.height))
    a = a.filter(ImageFilter.GaussianBlur(24))
    sh = np.asarray(a).astype(np.float32) / 255 * 0.30
    arr = np.asarray(img).astype(np.float32) * (1 - sh[..., None])
    img = Image.fromarray(arr.astype(np.uint8))
    img.paste(t, (x, y), t)
    img.save(out_jpg, quality=88)


def main(out):
    os.makedirs(out, exist_ok=True)
    man = {}
    for code, d in DESIGNS.items():
        p = os.path.join(out, code)
        os.makedirs(p, exist_ok=True)
        tex = os.path.join(p, f"{code}-texture.png")
        render_png(d).save(tex)
        render_png(d, pad_bleed=True, scale=40 / 25.4).convert("RGBA").save(os.path.join(p, f"{code}-check.png"))
        write_svg(d, os.path.join(p, f"{code} - PRINT.svg"), code)
        if d["kind"] == "mug":
            write_pdf(d, os.path.join(p, f"{code} - PRINT.pdf"), code)
            mug_mockups(tex, os.path.join(p, code))
            mug_cutout(tex, os.path.join(p, f"{code}-cutout.png"))
        else:
            for name, sc in (("A4", 1.0), ("A3", 2 ** 0.5), ("A2", 2.0), ("A1", 2 * 2 ** 0.5)):
                write_pdf(d, os.path.join(p, f"{code} - {name} PRINT.pdf"), f"{code} {name}", scale=sc)
            print_flat(tex, os.path.join(p, f"{code}-1-main.jpg"))
        man[code] = sorted(os.listdir(p))
        print(code, "done", flush=True)
    json.dump(man, open(os.path.join(out, "manifest.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
