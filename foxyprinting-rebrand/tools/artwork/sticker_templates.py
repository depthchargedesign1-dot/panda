"""Editable, print-ready sticker and label templates for Foxy Printing (one set per product).

Usage:
    python3 tools/artwork/sticker_templates.py --out exports/sticker-artwork            # every product
    python3 tools/artwork/sticker_templates.py --out DIR --only FOXY-VG540-CBLS-001     # one product
    python3 tools/artwork/sticker_templates.py --out DIR --only FOXY-VG540-CBLS-001 --size 76   # another size

For each product it writes, into <out>/<SKU>/:
  <name>.svg   layers (inkscape:groupmode="layer"): Artwork, Text, CUT, Guides (Guides hidden)
  <name>.pdf   real PDF layers (OCGs) Artwork, Text, CUT, Guides (Guides off and non-printing).
               Pure ASCII (ASCII85 + Flate streams, header bytes patched) so it can be saved to Dropbox as text.
  <name> - preview.png   render with the guides switched on (green = bleed, magenta = safe area)
  README.txt, Fonts/FONTS - DOWNLOAD LINK.txt, Fonts/OFL.txt

Rules followed (CLAUDE.md, foxy-production-artwork skill, plan/product-facts.md):
  * sizes/shapes only from the product's own options and fact sheet (VG540 stickers: 25-102 mm; roll labels 20 x 40 mm)
  * 3 mm bleed, 3 mm safe area, background art runs into the bleed, live text, CMYK colours
  * cut path on its own layer "CUT": 0.25 pt stroke, RGB 255,0,0, no fill, on the trim line
  * open-licence fonts only (Google Fonts, SIL OFL), kept in tools/artwork/assets/fonts
"""
import argparse
import base64
import math
import os
import re
import subprocess
import sys
import zlib

if os.environ.get('PYTHONHASHSEED') != '0':   # ReportLab's font subsetting depends on set order: fix it so re-runs are byte-identical
    os.execvpe(sys.executable, [sys.executable] + sys.argv, {**os.environ, 'PYTHONHASHSEED': '0'})
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab import rl_config

rl_config.invariant = 1

HERE = Path(__file__).resolve().parent
FONT_DIR = HERE / 'assets' / 'fonts'
PT = 0.352778          # mm per point
BLEED = 3.0
SAFE = 3.0
CUT_W_PT = 0.25        # cut line stroke, points (brief: 0.25 pt red RGB 255,0,0)

# font key -> (file, css family, css weight, Google Fonts page)
FONTS = {
    'poppins-bold': ('Poppins-Bold.ttf', 'Poppins', 700, 'https://fonts.google.com/specimen/Poppins'),
    'pacifico': ('Pacifico-Regular.ttf', 'Pacifico', 400, 'https://fonts.google.com/specimen/Pacifico'),
    'fredoka': ('Fredoka-SemiBold.ttf', 'Fredoka', 600, 'https://fonts.google.com/specimen/Fredoka'),
    'bebas': ('BebasNeue-Regular.ttf', 'Bebas Neue', 400, 'https://fonts.google.com/specimen/Bebas+Neue'),
}
FONT_COPYRIGHT = {
    'Poppins': 'Copyright 2020 The Poppins Project Authors (https://github.com/itfoundry/Poppins)',
    'Pacifico': 'Copyright 2018 The Pacifico Project Authors (https://github.com/googlefonts/Pacifico)',
    'Fredoka': 'Copyright 2016 The Fredoka Project Authors (https://github.com/hafontia/Fredoka-One)',
    'Bebas Neue': 'Copyright 2019 The Bebas Neue Project Authors (https://github.com/dharmatype/Bebas-Neue)',
}
for key, (fn, *_r) in FONTS.items():
    pdfmetrics.registerFont(TTFont(key, str(FONT_DIR / fn)))


def cmyk_to_rgb(c, m, y, k):
    c, m, y, k = (v / 100 for v in (c, m, y, k))
    return tuple(round(255 * (1 - a) * (1 - k)) for a in (c, m, y))


def hexrgb(rgb):
    return '#%02x%02x%02x' % rgb


# palettes: (background, accent, text) as CMYK percentages - all inside a normal CMYK gamut
PAL = {
    'navy':   ((100, 80, 20, 30), (0, 30, 90, 0), (0, 0, 0, 0)),
    'pink':   ((0, 35, 10, 0), (0, 80, 30, 0), (0, 60, 40, 60)),
    'cream':  ((0, 5, 20, 0), (0, 45, 90, 10), (0, 40, 80, 70)),
    'honey':  ((0, 35, 95, 0), (0, 10, 60, 0), (0, 50, 90, 75)),
    'sage':   ((25, 0, 30, 10), (55, 10, 60, 25), (70, 30, 70, 60)),
    'berry':  ((20, 95, 40, 20), (0, 20, 30, 0), (0, 0, 0, 0)),
    'coffee': ((30, 60, 80, 55), (0, 25, 50, 0), (0, 5, 15, 0)),
    'blush':  ((0, 15, 10, 0), (10, 40, 20, 0), (40, 60, 40, 40)),
    'kraft':  ((10, 25, 45, 5), (0, 0, 0, 90), (0, 0, 0, 90)),
    'red':    ((0, 95, 90, 0), (0, 0, 0, 0), (0, 0, 0, 0)),
    'teal':   ((75, 10, 40, 10), (0, 10, 60, 0), (0, 0, 0, 0)),
    'lilac':  ((15, 25, 0, 0), (45, 60, 0, 10), (60, 80, 20, 40)),
    'ivory':  ((0, 3, 10, 0), (0, 20, 50, 15), (30, 40, 50, 60)),
    'green':  ((60, 0, 80, 20), (0, 0, 0, 0), (0, 0, 0, 0)),
    'black':  ((40, 30, 30, 100), (0, 20, 90, 0), (0, 0, 0, 0)),
    'mint':   ((30, 0, 15, 0), (60, 0, 35, 20), (80, 30, 60, 50)),
    'orange': ((0, 60, 95, 0), (0, 0, 0, 0), (0, 0, 0, 0)),
    'yellowstock': ((0, 0, 0, 0), (0, 0, 0, 100), (0, 0, 0, 100)),
}

VG540_FACTS = dict(
    method='Print & cut on the Roland VG2-540 / VG2-640 (contour cut to shape)',
    sizes='25 mm, 38 mm, 51 mm, 64 mm, 76 mm or 102 mm',
    materials='gloss vinyl, matt vinyl, waterproof & tearproof (laminated), clear, metallic gold, metallic silver',
    shapes='circle, square, rectangle, oval, or die-cut to the outline of the design (customer chooses)',
)

# (sku, short title, palette, [lines], logo?)  line = (text, font key, relative size)
VG540 = [
    ('FOXY-VG540-CBLS-001', 'Custom Business Logo Stickers', 'navy', [('YOUR BUSINESS NAME', 'poppins-bold', 1.0), ('www.yourwebsite.co.uk', 'poppins-bold', 0.6)], True),
    ('FOXY-VG540-CBKS-001', 'Custom Bakery Stickers', 'pink', [('Your Bakery', 'pacifico', 1.2), ('FRESHLY BAKED WITH LOVE', 'poppins-bold', 0.55)], True),
    ('FOXY-VG540-TYSB-001', 'Thank You for Supporting My Small Business Stickers', 'blush', [('Thank you', 'pacifico', 1.3), ('FOR SUPPORTING MY', 'poppins-bold', 0.5), ('SMALL BUSINESS', 'poppins-bold', 0.5), ('@yourhandle', 'poppins-bold', 0.5)], False),
    ('FOXY-VG540-CHJL-001', 'Custom Honey Jar Labels', 'honey', [('YOUR APIARY', 'poppins-bold', 0.9), ('Pure Local Honey', 'pacifico', 1.0), ('Net weight 000 g', 'poppins-bold', 0.5)], True),
    ('FOXY-VG540-CCL-001', 'Custom Candle Labels', 'ivory', [('YOUR CANDLE CO.', 'poppins-bold', 0.9), ('Scent Name', 'pacifico', 1.0), ('Your safety wording here', 'poppins-bold', 0.45)], True),
    ('FOXY-VG540-PJJL-001', 'Personalised Jam Jar Labels', 'berry', [('Strawberry Jam', 'pacifico', 1.1), ("YOUR KITCHEN NAME", 'poppins-bold', 0.6), ('Made on: 00 / 00 / 00', 'poppins-bold', 0.5)], False),
    ('FOXY-VG540-CSS-001', 'Coffee Shop Stickers', 'coffee', [('YOUR COFFEE SHOP', 'poppins-bold', 0.9), ('Blend Name', 'pacifico', 1.0), ('FRESHLY ROASTED', 'poppins-bold', 0.5)], True),
    ('FOXY-VG540-WCL-001', 'Waterproof Cosmetic Labels', 'mint', [('YOUR BRAND', 'poppins-bold', 1.0), ('Product Name', 'pacifico', 0.9), ('000 ml', 'poppins-bold', 0.5)], True),
    ('FOXY-VG540-PSSB-001', 'Packaging Stickers for Small Business', 'lilac', [('YOUR BUSINESS NAME', 'poppins-bold', 0.9), ('@yourhandle', 'poppins-bold', 0.6)], True),
    ('FOXY-VG540-TBSS-001', 'Takeaway Stickers', 'red', [('YOUR TAKEAWAY', 'bebas', 1.4), ('Enjoy your meal!', 'pacifico', 0.8), ('01234 567890', 'poppins-bold', 0.55)], True),
    ('FOXY-VG540-CBTL-001', 'Custom Bottle Labels', 'black', [('YOUR BREWERY', 'bebas', 1.4), ('Drink Name', 'pacifico', 0.9), ('000 ml  |  0.0% ABV', 'poppins-bold', 0.5)], True),
    ('FOXY-VG540-FBS-001', 'Florist Stickers', 'blush', [('Your Florist', 'pacifico', 1.2), ('HAND-TIED WITH LOVE', 'poppins-bold', 0.5), ('@yourhandle', 'poppins-bold', 0.5)], True),
    ('FOXY-VG540-DTL-001', 'Dog Treat Labels', 'teal', [('YOUR DOG BAKERY', 'fredoka', 1.0), ('Treat Name', 'fredoka', 0.8), ('Your wording here', 'poppins-bold', 0.45)], True),
    ('FOXY-VG540-SLS-001', 'Salon Stickers', 'black', [('YOUR SALON', 'poppins-bold', 1.0), ('Thank you for visiting', 'pacifico', 0.75), ('Book: 01234 567890', 'poppins-bold', 0.5)], True),
    ('FOXY-VG540-PWFS-001', 'Personalised Wedding Stickers', 'ivory', [('Sarah & James', 'pacifico', 1.2), ('THANK YOU', 'poppins-bold', 0.55), ('12.06.2027', 'poppins-bold', 0.5)], False),
    ('FOXY-VG540-CFPS-001', 'Price Stickers for Craft Fairs', 'kraft', [('£0.00', 'bebas', 2.2), ('YOUR SHOP NAME', 'poppins-bold', 0.55)], False),
    ('FOXY-VG540-FHWC-001', 'Fragile Stickers', 'red', [('FRAGILE', 'bebas', 2.0), ('HANDLE WITH CARE', 'poppins-bold', 0.6), ('YOUR BUSINESS NAME', 'poppins-bold', 0.45)], False),
    ('FOXY-VG540-FSEL-001', 'Farm Shop Labels', 'sage', [('YOUR FARM NAME', 'poppins-bold', 0.9), ('Free Range Eggs', 'pacifico', 1.0), ('Packed on: 00 / 00', 'poppins-bold', 0.5)], True),
    ('FOXY-VG540-CBRS-001', 'Clothing Brand Stickers', 'black', [('YOUR BRAND', 'bebas', 1.6), ('EST. 0000', 'poppins-bold', 0.5)], True),
    ('FOXY-VG540-SBBL-001', 'Soap Labels', 'mint', [('YOUR SOAP CO.', 'poppins-bold', 0.9), ('Soap Name', 'pacifico', 1.0), ('Net weight 000 g', 'poppins-bold', 0.5)], True),
    ('FOXY-VG540-GCLS-001', 'Club Stickers', 'green', [('YOUR CLUB NAME', 'bebas', 1.5), ('EST. 0000', 'poppins-bold', 0.5)], True),
]

ROLL = [
    ('FOXY-LBL-PTL-01', 'Personalised Tool Labels', [('PROPERTY OF', 'poppins-bold', 0.8), ('J. SMITH BUILDERS', 'poppins-bold', 1.0), ('07700 900123', 'poppins-bold', 0.9)]),
    ('FOXY-LBL-AWS-01', 'Allergen Warning Stickers', [('CONTAINS NUTS', 'poppins-bold', 1.0), ('MAY CONTAIN SESAME', 'poppins-bold', 0.7), ('YOUR BUSINESS NAME', 'poppins-bold', 0.6)]),
]

KISS = ('FOXY-CUT-KCSS-01', 'Custom Kiss-Cut Sticker Sheets')


# ---------------------------------------------------------------- drawing model (mm, origin top-left)
LAYER_LABEL = {'Stock': 'Label stock - do not print'}


class Doc:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.layers = {n: [] for n in ('Stock', 'Artwork', 'Text', 'CUT', 'Guides')}
        self.fonts = set()

    def add(self, layer, op):
        self.layers[layer].append(op)
        if op[0] == 'text':
            self.fonts.add(op[4])


def rect(x, y, w, h, r=0, fill=None, stroke=None, sw=0.0, dash=None, rgb_stroke=None):
    return ('rect', x, y, w, h, r, fill, stroke, sw, dash, rgb_stroke)


def circ(cx, cy, r, fill=None, stroke=None, sw=0.0, dash=None, rgb_stroke=None):
    return ('circle', cx, cy, r, fill, stroke, sw, dash, rgb_stroke)


def text(x, y, s, font, size_pt, fill, anchor='middle'):
    return ('text', x, y, s, font, size_pt, fill, anchor)


def fmt(v):
    s = ('%.2f' % v).rstrip('0').rstrip('.')
    return s if s != '-0' else '0'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def paint_attrs(fill, stroke, sw, dash, rgb_stroke):
    a = ' fill="%s"' % (hexrgb(cmyk_to_rgb(*fill)) if fill else 'none')
    if rgb_stroke or stroke:
        col = hexrgb(rgb_stroke) if rgb_stroke else hexrgb(cmyk_to_rgb(*stroke))
        a += ' stroke="%s" stroke-width="%s"' % (col, fmt(sw))
        if dash:
            a += ' stroke-dasharray="%s"' % ','.join(fmt(d) for d in dash)
    return a


def write_svg(doc, path, title):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
           'width="%smm" height="%smm" viewBox="0 0 %s %s">' % (fmt(doc.w), fmt(doc.h), fmt(doc.w), fmt(doc.h)),
           '<title>%s</title>' % esc(title)]
    for name, ops in doc.layers.items():
        if name == 'Stock' and not ops:
            continue
        style = ' style="display:none"' if name in ('Guides', 'Stock') else ''
        label = LAYER_LABEL.get(name, name)
        out.append('<g id="%s" inkscape:groupmode="layer" inkscape:label="%s"%s>' % (name, label, style))
        for op in ops:
            if op[0] == 'rect':
                _, x, y, w, h, r, fill, stroke, sw, dash, rgbs = op
                rr = ' rx="%s"' % fmt(r) if r else ''
                out.append('<rect x="%s" y="%s" width="%s" height="%s"%s%s/>' % (fmt(x), fmt(y), fmt(w), fmt(h), rr, paint_attrs(fill, stroke, sw, dash, rgbs)))
            elif op[0] == 'circle':
                _, cx, cy, r, fill, stroke, sw, dash, rgbs = op
                out.append('<circle cx="%s" cy="%s" r="%s"%s/>' % (fmt(cx), fmt(cy), fmt(r), paint_attrs(fill, stroke, sw, dash, rgbs)))
            elif op[0] == 'text':
                _, x, y, s, font, size, fill, anchor = op
                _fn, fam, weight, _u = FONTS[font]
                out.append('<text x="%s" y="%s" font-family="\'%s\', sans-serif" font-weight="%d" font-size="%s" text-anchor="%s" fill="%s">%s</text>'
                           % (fmt(x), fmt(y), fam, weight, fmt(size * PT), anchor, hexrgb(cmyk_to_rgb(*fill)), esc(s)))
        out.append('</g>')
    out.append('</svg>')
    Path(path).write_text('\n'.join(out) + '\n', encoding='utf-8')


def write_pdf(doc, path, title, guides_on):
    H = doc.h
    c = canvas.Canvas(str(path), pagesize=(doc.w * mm, doc.h * mm), pageCompression=1)
    c.setTitle(title)
    c.setAuthor('Foxy Printing')
    used = [n for n, ops in doc.layers.items() if ops or n != 'Stock']
    for name in used:
        ops = doc.layers[name]
        c._code.append('/OC /%s BDC' % name)
        for op in ops:
            c.saveState()
            if op[0] in ('rect', 'circle'):
                if op[0] == 'rect':
                    _, x, y, w, h, r, fill, stroke, sw, dash, rgbs = op
                else:
                    _, cx, cy, r, fill, stroke, sw, dash, rgbs = op
                if fill:
                    c.setFillColorCMYK(*(v / 100 for v in fill))
                if rgbs:
                    c.setStrokeColorRGB(*(v / 255 for v in rgbs))
                elif stroke:
                    c.setStrokeColorCMYK(*(v / 100 for v in stroke))
                if rgbs or stroke:
                    c.setLineWidth(sw * mm)
                    if dash:
                        c.setDash([d * mm for d in dash])
                f, s = (1 if fill else 0), (1 if (rgbs or stroke) else 0)
                if op[0] == 'rect':
                    if r:
                        c.roundRect(x * mm, (H - y - h) * mm, w * mm, h * mm, r * mm, stroke=s, fill=f)
                    else:
                        c.rect(x * mm, (H - y - h) * mm, w * mm, h * mm, stroke=s, fill=f)
                else:
                    c.circle(cx * mm, (H - cy) * mm, r * mm, stroke=s, fill=f)
            elif op[0] == 'text':
                _, x, y, s, font, size, fill, anchor = op
                c.setFont(font, size)
                c.setFillColorCMYK(*(v / 100 for v in fill))
                {'middle': c.drawCentredString, 'start': c.drawString, 'end': c.drawRightString}[anchor](x * mm, (H - y) * mm, s)
            c.restoreState()
        c._code.append('EMC')
    c.showPage()
    c.save()
    finish_pdf(path, guides_on, used)


def dehint(font_bytes):
    import io
    from fontTools.ttLib import TTFont as FTFont
    f = FTFont(io.BytesIO(font_bytes))
    for tag in ('fpgm', 'prep', 'cvt ', 'gasp', 'hdmx', 'LTSH', 'VDMX'):
        if tag in f:
            del f[tag]
    glyf = f['glyf']
    for name in f.getGlyphOrder():
        glyf[name].removeHinting()
    buf = io.BytesIO()
    f.save(buf)
    return buf.getvalue()


def finish_pdf(path, guides_on, names):
    """Add the OCG layers, re-encode every stream as ASCII85+Flate and make the whole file 7-bit ASCII."""
    import pikepdf
    with pikepdf.open(path, allow_overwriting_input=True) as pdf:
        ocg = {}
        for n in names:
            d = pikepdf.Dictionary(Type=pikepdf.Name.OCG, Name=LAYER_LABEL.get(n, n))
            if n in ('Guides', 'Stock'):
                d.Usage = pikepdf.Dictionary(Print=pikepdf.Dictionary(PrintState=pikepdf.Name.OFF))
            ocg[n] = pdf.make_indirect(d)
        order = pikepdf.Array([ocg[n] for n in names])
        hidden = [n for n in names if n in ('Guides', 'Stock')]
        on = pikepdf.Array([ocg[n] for n in names if guides_on or n not in hidden])
        off = pikepdf.Array([] if guides_on else [ocg[n] for n in hidden])
        pdf.Root.OCProperties = pikepdf.Dictionary(
            OCGs=order,
            D=pikepdf.Dictionary(Name='Layers', Order=order, ON=on, OFF=off,
                                 AS=pikepdf.Array([pikepdf.Dictionary(Event=pikepdf.Name.Print, Category=pikepdf.Array([pikepdf.Name.Print]), OCGs=order)])))
        for page in pdf.pages:
            page.obj.Resources.Properties = pikepdf.Dictionary({'/' + n: ocg[n] for n in names})
        for obj in pdf.objects:
            if isinstance(obj, pikepdf.Stream):
                raw = obj.read_bytes()
                if '/Length1' in obj:          # embedded TrueType subset: drop hinting to keep the ASCII PDF small
                    raw = dehint(raw)
                    obj.Length1 = len(raw)
                enc = base64.a85encode(zlib.compress(raw, 9), wrapcol=76) + b'~>'
                obj.write(enc, filter=pikepdf.Array([pikepdf.Name.ASCII85Decode, pikepdf.Name.FlateDecode]))
        pdf.save(path, compress_streams=False, stream_decode_level=pikepdf.StreamDecodeLevel.none,
                 object_stream_mode=pikepdf.ObjectStreamMode.disable, static_id=True)
    data = bytearray(Path(path).read_bytes())
    nl = data.index(b'\n')
    for i in range(nl + 1, min(nl + 12, len(data))):   # the binary comment line after %PDF-1.x
        if data[i] >= 128:
            data[i] = ord('~')
    bad = [i for i, b in enumerate(data) if b >= 128]
    assert not bad, '%s: non-ASCII bytes at %s' % (path, bad[:5])
    Path(path).write_bytes(bytes(data))
    with pikepdf.open(path) as pdf:     # must still open cleanly
        assert len(pdf.pages) == 1


# ---------------------------------------------------------------- layout helpers
def font_box(font, size_pt):
    face = pdfmetrics.getFont(font).face
    asc = face.ascent / 1000 * size_pt * PT
    dsc = -face.descent / 1000 * size_pt * PT
    # caps/x-height of placeholder text sits well below the font's full ascent; use 80% of ascent as the visible top
    return asc * 0.8, dsc


def text_width(s, font, size_pt):
    return pdfmetrics.stringWidth(s, font, size_pt) * PT


def stack_layout(items, half_width_at, top, bottom, gap_ratio=0.18):
    """items: list of ('text', s, font, rel) or ('logo', w_rel, h_rel). Finds the largest scale that fits.
    half_width_at(y) -> half the usable width at height y (mm, None if outside). Returns placed items."""
    def place(k):
        blocks = []
        for it in items:
            if it[0] == 'text':
                size = it[3] * k
                a, d = font_box(it[2], size)
                blocks.append([it, size, a, d, text_width(it[1], it[2], size) / 2])
            else:
                hh = it[2] * k * PT
                blocks.append([it, None, hh, 0.0, it[1] * k * PT / 2])
        total = sum(b[2] + b[3] for b in blocks) + gap_ratio * k * PT * (len(blocks) - 1)
        y = (top + bottom) / 2 - total / 2
        placed = []
        for b in blocks:
            y_top = y
            y_base = y + b[2]
            y_bot = y_base + b[3]
            placed.append((b, y_top, y_base, y_bot))
            y = y_bot + gap_ratio * k * PT
        return placed, total

    def fits(k):
        placed, total = place(k)
        if total > bottom - top:
            return False
        for b, yt, yb, ybo in placed:
            for yy in (yt, ybo):
                hw = half_width_at(yy)
                if hw is None or b[4] > hw:
                    return False
        return True

    lo, hi = 1.0, 200.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if fits(mid):
            lo = mid
        else:
            hi = mid
    return place(lo * 0.97)[0]


def draw_stack(doc, cx, placed, text_col, accent):
    for b, yt, yb, ybo in placed:
        it = b[0]
        if it[0] == 'text':
            doc.add('Text', text(cx, yb, it[1], it[2], round(b[1], 2), text_col))
        else:
            w = b[4] * 2
            h = b[2]
            doc.add('Artwork', rect(cx - w / 2, yt, w, h, r=1.0, fill=(0, 0, 0, 0), stroke=accent, sw=0.35, dash=(1.2, 0.8)))
            lab = 'YOUR LOGO HERE'
            fs = min(h * 0.28 / PT, 0.8 * w / (text_width(lab, 'poppins-bold', 1.0)))
            doc.add('Text', text(cx, yt + h / 2 + fs * PT * 0.35, lab, 'poppins-bold', round(fs, 2), (0, 0, 0, 55)))


def guide_label(doc, x, y, s):
    doc.add('Guides', text(x, y, s, 'poppins-bold', 6, (0, 0, 0, 70)))


# ---------------------------------------------------------------- templates
def vg540_doc(lines, palette, logo, size):
    bg, accent, fg = PAL[palette]
    tile = size + 2 * BLEED
    margin, gap, label_h = 5.0, 10.0, 8.0
    doc = Doc(margin * 2 + tile * 2 + gap, margin + tile + label_h)
    items = []
    if logo:
        items.append(('logo', 3.6, 1.8))
    items += [('text',) + ln for ln in lines]

    # circle tile
    cx, cy, r = margin + tile / 2, margin + tile / 2, size / 2
    doc.add('Artwork', circ(cx, cy, r + BLEED, fill=bg))
    doc.add('Artwork', circ(cx, cy, r - SAFE + 1.2, stroke=accent, sw=0.4))
    rs = r - SAFE - 1.2   # keep text inside the decorative ring too
    hw = lambda yy: (math.sqrt(rs ** 2 - (yy - cy) ** 2) if abs(yy - cy) < rs else None)
    draw_stack(doc, cx, stack_layout(items, hw, cy - rs, cy + rs), fg, accent)
    doc.add('CUT', circ(cx, cy, r, stroke=None, sw=CUT_W_PT * PT, rgb_stroke=(255, 0, 0)))
    doc.add('Guides', circ(cx, cy, r + BLEED, stroke=(70, 0, 100, 0), sw=0.2, dash=(1, 1)))
    doc.add('Guides', circ(cx, cy, r - SAFE, stroke=(0, 100, 0, 0), sw=0.2, dash=(1, 1)))
    guide_label(doc, cx, margin + tile + 5, 'CIRCLE %g mm  (+3 mm bleed, 3 mm safe)' % size)

    # square tile
    x0 = margin + tile + gap
    sx, sy = x0 + BLEED, margin + BLEED
    doc.add('Artwork', rect(x0, margin, tile, tile, fill=bg))
    doc.add('Artwork', rect(sx + SAFE - 1.2, sy + SAFE - 1.2, size - 2 * SAFE + 2.4, size - 2 * SAFE + 2.4, r=1.5, stroke=accent, sw=0.4))
    inner = SAFE + 1.2
    hw2 = lambda yy: (size / 2 - inner) if sy + inner <= yy <= sy + size - inner else None
    draw_stack(doc, sx + size / 2, stack_layout(items, hw2, sy + inner, sy + size - inner), fg, accent)
    doc.add('CUT', rect(sx, sy, size, size, stroke=None, sw=CUT_W_PT * PT, rgb_stroke=(255, 0, 0)))
    doc.add('Guides', rect(x0, margin, tile, tile, stroke=(70, 0, 100, 0), sw=0.2, dash=(1, 1)))
    doc.add('Guides', rect(sx + SAFE, sy + SAFE, size - 2 * SAFE, size - 2 * SAFE, stroke=(0, 100, 0, 0), sw=0.2, dash=(1, 1)))
    guide_label(doc, x0 + tile / 2, margin + tile + 5, 'SQUARE %g x %g mm  (+3 mm bleed, 3 mm safe)' % (size, size))
    return doc


ROLL_W, ROLL_H, ROLL_R = 40.0, 20.0, 2.0   # label 40 x 20 mm (fact sheet); corner radius 2 mm is ASK (drawn, not confirmed)


def roll_doc(lines):
    margin, label_h = 5.0, 7.0
    tw, th = ROLL_W + 2 * BLEED, ROLL_H + 2 * BLEED
    doc = Doc(margin * 2 + tw, margin + th + label_h)
    x, y = margin + BLEED, margin + BLEED
    black = (0, 0, 0, 100)
    # The roll is pre-printed yellow stock: nothing but black prints, so the yellow is shown on the Guides layer only.
    doc.add('Stock', rect(margin, margin, tw, th, fill=(0, 10, 95, 0)))
    items = [('text',) + ln for ln in lines]
    hw = lambda yy: (ROLL_W / 2 - SAFE) if y + SAFE <= yy <= y + ROLL_H - SAFE else None
    draw_stack(doc, x + ROLL_W / 2, stack_layout(items, hw, y + SAFE, y + ROLL_H - SAFE, gap_ratio=0.12), black, black)
    doc.add('CUT', rect(x, y, ROLL_W, ROLL_H, r=ROLL_R, sw=CUT_W_PT * PT, rgb_stroke=(255, 0, 0)))
    doc.add('Guides', rect(margin, margin, tw, th, stroke=(70, 0, 100, 0), sw=0.2, dash=(1, 1)))
    doc.add('Guides', rect(x + SAFE, y + SAFE, ROLL_W - 2 * SAFE, ROLL_H - 2 * SAFE, stroke=(0, 100, 0, 0), sw=0.2, dash=(1, 1)))
    guide_label(doc, margin + tw / 2, margin + th + 4.5, '40 x 20 mm label (+3 mm bleed)')
    return doc


SRA4_W, SRA4_H = 225.0, 320.0


def kiss_doc(size=51.0):
    """SRA4 ColorCut sheet: 12 mm clear on the left, 10 mm on the other edges (PageMARKs + barcode)."""
    doc = Doc(SRA4_W, SRA4_H)
    tile = size + 2 * BLEED
    cols, rows, gap = 3, 5, 3.0
    area_x, area_y, area_w, area_h = 12.0, 10.0, SRA4_W - 22.0, SRA4_H - 20.0
    ox = area_x + (area_w - (cols * tile + (cols - 1) * gap)) / 2
    oy = area_y + (area_h - (rows * tile + (rows - 1) * gap)) / 2
    pals = ['navy', 'pink', 'teal', 'honey', 'lilac', 'sage']
    n = 0
    for rrow in range(rows):
        for ccol in range(cols):
            n += 1
            bg, accent, fg = PAL[pals[(n - 1) % len(pals)]]
            tx, ty = ox + ccol * (tile + gap), oy + rrow * (tile + gap)
            items = [('text', 'DESIGN %d' % n, 'poppins-bold', 1.0), ('text', 'Your artwork here', 'poppins-bold', 0.5)]
            if (rrow + ccol) % 2 == 0:
                cx, cy, r = tx + tile / 2, ty + tile / 2, size / 2
                doc.add('Artwork', circ(cx, cy, r + BLEED, fill=bg))
                rs = r - SAFE
                hw = lambda yy, cy=cy, rs=rs: (math.sqrt(rs ** 2 - (yy - cy) ** 2) if abs(yy - cy) < rs else None)
                draw_stack(doc, cx, stack_layout(items, hw, cy - rs, cy + rs), fg, accent)
                doc.add('CUT', circ(cx, cy, r, sw=CUT_W_PT * PT, rgb_stroke=(255, 0, 0)))
                doc.add('Guides', circ(cx, cy, r - SAFE, stroke=(0, 100, 0, 0), sw=0.2, dash=(1, 1)))
            else:
                sx, sy = tx + BLEED, ty + BLEED
                doc.add('Artwork', rect(tx, ty, tile, tile, r=BLEED + 3, fill=bg))
                hw = lambda yy, sy=sy: (size / 2 - SAFE) if sy + SAFE <= yy <= sy + size - SAFE else None
                draw_stack(doc, sx + size / 2, stack_layout(items, hw, sy + SAFE, sy + size - SAFE), fg, accent)
                doc.add('CUT', rect(sx, sy, size, size, r=3.0, sw=CUT_W_PT * PT, rgb_stroke=(255, 0, 0)))
                doc.add('Guides', rect(sx + SAFE, sy + SAFE, size - 2 * SAFE, size - 2 * SAFE, stroke=(0, 100, 0, 0), sw=0.2, dash=(1, 1)))
    doc.add('Guides', rect(12.0, 10.0, area_w, area_h, stroke=(100, 0, 0, 0), sw=0.25, dash=(2, 1.5)))
    guide_label(doc, SRA4_W / 2, 6.0, 'SRA4 225 x 320 mm ColorCut sheet - keep 12 mm left / 10 mm other edges clear for PageMARKs & barcode')
    return doc


# ---------------------------------------------------------------- README / fonts text
def fonts_txt(doc):
    fams = sorted({FONTS[f][1] for f in doc.fonts})
    out = ['FONTS USED IN THIS TEMPLATE (all free, SIL Open Font License 1.1 - see OFL.txt)', '']
    for fam in fams:
        styles = sorted({'%s %d' % (FONTS[k][0], FONTS[k][2]) for k in doc.fonts if FONTS[k][1] == fam})
        url = [FONTS[k][3] for k in doc.fonts if FONTS[k][1] == fam][0]
        out += ['- %s' % fam, '  Files: %s' % ', '.join(styles), '  Download (free): %s' % url, '  %s' % FONT_COPYRIGHT[fam], '']
    out += ['Install the fonts before opening the SVG/PDF in Illustrator, otherwise the live text is substituted.',
            'A copy of every font file is also kept in the website repo: foxyprinting-rebrand/tools/artwork/assets/fonts/']
    return '\n'.join(out) + '\n'


def ofl_txt():
    body = (FONT_DIR / 'OFL.txt').read_text(encoding='utf-8')
    body = body[body.index('This Font Software is licensed'):]
    head = '\n'.join(FONT_COPYRIGHT[f] for f in ('Poppins', 'Pacifico', 'Fredoka', 'Bebas Neue'))
    return head + '\n\n' + body


COMMON_FILES = """FILES
- {name}.svg  : editable artwork. Layers: Artwork, Text, CUT, Guides (Guides hidden - switch it on to see the lines).
- {name}.pdf  : the same, with real PDF layers Artwork / Text / CUT / Guides (Guides is off and never prints).
- Fonts/      : FONTS - DOWNLOAD LINK.txt and OFL.txt (licence).
- A PNG preview is kept in the website repo: foxyprinting-rebrand/exports/sticker-artwork/{sku}/

LINE COLOURS
- CUT layer = red = cut. 0.25 pt stroke, RGB 255,0,0, no fill, sitting exactly on the trim line.
- Guides (not printed): green dashed = 3 mm bleed edge, magenta dashed = 3 mm safe area.

{regen}: python3 tools/artwork/sticker_templates.py --out <folder> --only {sku}{size_opt}
"""


def readme_vg540(sku, title, size, lines, logo):
    texts = '\n'.join('  - "%s"' % ln[0] for ln in lines)
    return f"""{title} - {sku}
Print-ready, editable sticker template (master size {size:g} mm), made {TODAY}.

PRODUCT FACTS (plan/product-facts.md, "Custom business stickers: print and cut")
- Print method: {VG540_FACTS['method']}. Supplied on backing sheets or rolls.
- Sizes sold: {VG540_FACTS['sizes']}.
- Shapes sold: {VG540_FACTS['shapes']}.
- Materials: {VG540_FACTS['materials']}. Waterproof & tearproof lasts up to 3 years outdoors.
- The customer supplies their own logo/artwork; we may tidy it up for free. No proofs.

THIS TEMPLATE
- Two {size:g} mm stickers on one page: a CIRCLE and a SQUARE, each with 3 mm bleed all round
  (artboard per sticker = {size + 6:g} x {size + 6:g} mm) and a 3 mm safe area inside the cut.
- Background colour runs into the bleed. Keep all text and logos inside the magenta safe line.
- Text to change (live text, Text layer):
{texts}
{"- Logo: replace the dashed 'YOUR LOGO HERE' box (Artwork layer) with the customer's logo (vector, or 300 dpi+ at size)." if logo else "- No logo box on this design; add the customer's logo inside the safe area if they send one."}
- Rectangle and oval: the listing gives one size figure only, so the second dimension is ASK (not drawn).
- Die-cut: place the customer's artwork, then draw the CUT path around its outline (or offset it ~2 mm) on the CUT layer.

OTHER SIZES ({VG540_FACTS['sizes']})
- Re-run the generator with --size (keeps bleed and safe area at exactly 3 mm), or in Illustrator scale the
  artwork only, then redraw the cut at the new size and keep 3 mm bleed / 3 mm safe.
- 25 mm: keep it to the logo or one short line - small text will not be readable.

HOW TO PRINT AND CUT (Roland VG2-540 / VG2-640 with VersaWorks)
1. Open the SVG or PDF in Illustrator, install the fonts (Fonts folder), change the text, place the logo.
2. Select the red path on the CUT layer and give it the "CutContour" spot swatch (Roland VersaWorks plug-in or a
   spot swatch named exactly CutContour), stroke only, no fill. VersaWorks cuts CutContour; it does not cut plain red.
3. Delete the sticker shape you don't need (circle or square), step-and-repeat the one ordered for the quantity.
4. Save as PDF (keep spot colours) and send to VersaWorks as a Print & Cut job. Test-cut one sticker first.

{COMMON_FILES.format(name=f"{sku} - template {size:g}mm", sku=sku, size_opt=" [--size 76]", regen="Regenerate or make another size")}"""


def readme_roll(sku, title, lines):
    texts = '\n'.join('  - "%s"' % ln[0] for ln in lines)
    return f"""{title} - {sku}
Print-ready, editable label template, made {TODAY}.

PRODUCT FACTS (plan/product-facts.md, "Roll labels: 20 x 40 mm yellow, black print")
- Label: 20 x 40 mm rectangle with rounded corners, bright yellow, roll of 1,000.
- Print: BLACK ONLY. The yellow is the label stock - it is shown on the hidden layer
  "Label stock - do not print" for reference only and must never print.
- Packs: 50, 100, 250, 500 or a full roll of 1,000. Every label in an order carries the same design.
- Up to three short lines of text.
- ASK (not yet confirmed by the owner): paper or polypropylene stock; permanent or removable adhesive;
  thermal transfer or direct thermal printing; exact corner radius (drawn here at 2 mm - check against the roll).

THIS TEMPLATE
- One 40 x 20 mm label (landscape) with 3 mm bleed all round (artboard 46 x 26 mm) and a 3 mm safe area.
- Text to change (live text, Text layer):
{texts}
{"- Allergen stickers highlight allergens only: they don't replace a full ingredients label, and the customer is responsible for the wording." if 'AWS' in sku else "- Use a real phone number from the customer (07700 900123 is a drama/test number)."}

HOW TO PRINT
- The labels are pre-cut on the roll, so the CUT layer is only a reference for the label edge: hide it before printing.
- In the label printer software set the page to 40 x 20 mm (no bleed is needed for black-only text).
- Print one label first and check the position on the roll.

{COMMON_FILES.format(name=f"{sku} - template 40x20mm", sku=sku, size_opt="", regen="Regenerate")}"""


def readme_kiss(sku, title):
    return f"""{title} - {sku}
Production sheet template for kiss-cut sticker sheets, made {TODAY}.

WHAT IS KNOWN (Shopify listing)
- Sold as 5 or 20 sheets; the customer uploads their own sheet artwork and can mix shapes, sizes and designs.
- Printed and kiss-cut in-house (SKU prefix FOXY-CUT = flatbed cutter, Intec ColorCut). No proofs.
- ASK (no fact sheet yet): the finished sheet size the customer receives (A4, A5, A6?), the sticker material,
  and whether the sheet outline is cut through on the ColorCut. Until then this is a cutter-sheet layout only.

THIS TEMPLATE
- SRA4 sheet, 225 x 320 mm (the ColorCut sheet size in the foxy-production-artwork skill).
- 12 mm clear on the left and 10 mm on the other edges for the ColorCut PageMARKs and barcode (blue dashed guide).
- EXAMPLE layout: 15 stickers of 51 mm (alternating circles and rounded squares), each with 3 mm bleed and a
  3 mm safe area. Replace them with the customer's designs; the sizes are examples, not a product spec.
- Each sticker's kiss-cut is a red path on the CUT layer, on the trim line.

HOW TO CUT (Intec ColorCut Pro)
1. Open in Illustrator, place the customer's artwork into the circles/squares (or redraw cut paths to their shapes).
2. Run "Foxy - 1 Prepare cut file", then the ColorCut plug-in "ADD PageMARKs & BarCode".
3. Hide the CUT layer and print ("Foxy - 2 Save print PDF").
4. In ColorCut Pro map Red = Cut and set the blade depth for a KISS cut (through the vinyl, not the backing),
   or recolour the paths Yellow = Score (half-depth) if you prefer the house convention. Test-cut the first sheet.

{COMMON_FILES.format(name=f"{sku} - SRA4 kiss-cut sheet template", sku=sku, size_opt="", regen="Regenerate")}"""


TODAY = '6 Oct 2026'


def save_set(doc, out_root, sku, name, title, readme):
    d = Path(out_root) / sku
    (d / 'Fonts').mkdir(parents=True, exist_ok=True)
    svg, pdf = d / f'{name}.svg', d / f'{name}.pdf'
    write_svg(doc, svg, title)
    write_pdf(doc, pdf, title, guides_on=False)
    prev_pdf = d / '_preview.pdf'
    write_pdf(doc, prev_pdf, title, guides_on=True)
    png_base = d / f'{name} - preview'
    dpi = 60 if doc.w > 200 else 200
    subprocess.run(['pdftoppm', '-r', str(dpi), '-png', '-singlefile', str(prev_pdf), str(png_base)], check=True)
    prev_pdf.unlink()
    (d / 'README.txt').write_text(readme, encoding='utf-8')
    (d / 'Fonts' / 'FONTS - DOWNLOAD LINK.txt').write_text(fonts_txt(doc), encoding='utf-8')
    (d / 'Fonts' / 'OFL.txt').write_text(ofl_txt(), encoding='utf-8')
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', required=True)
    ap.add_argument('--only', nargs='*', help='SKUs to build (default: all)')
    ap.add_argument('--size', type=float, default=51.0, help='VG540 sticker size in mm (25, 38, 51, 64, 76 or 102)')
    a = ap.parse_args()
    want = lambda s: not a.only or s in a.only
    for sku, title, pal, lines, logo in VG540:
        if want(sku):
            doc = vg540_doc(lines, pal, logo, a.size)
            print(save_set(doc, a.out, sku, f'{sku} - template {a.size:g}mm', f'{title} - {sku}', readme_vg540(sku, title, a.size, lines, logo)))
    for sku, title, lines in ROLL:
        if want(sku):
            print(save_set(roll_doc(lines), a.out, sku, f'{sku} - template 40x20mm', f'{title} - {sku}', readme_roll(sku, title, lines)))
    sku, title = KISS
    if want(sku):
        print(save_set(kiss_doc(), a.out, sku, f'{sku} - SRA4 kiss-cut sheet template', f'{title} - {sku}', readme_kiss(sku, title)))


if __name__ == '__main__':
    main()
