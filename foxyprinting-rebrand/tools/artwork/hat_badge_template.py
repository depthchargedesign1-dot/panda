"""Editable, print-ready cuff badge template for the personalised bobble hats (FOXY-DTF-PBH-01 to -08).

Usage:
    python3 tools/artwork/hat_badge_template.py --out exports/hat-artwork

Blank: Beechfield B472 Stadium Beanie (never name the blank to customers). The customer's badge/logo is
printed in full colour on the front of the cuff (internal machine code DTF). The template is the same for
all 8 colourways; one folder per product is written so each SKU has its own set (as in Dropbox).

For each product it writes, into <out>/<short title> - <SKU>/:
  <SKU> - cuff badge 60x50mm.svg   layers (inkscape:groupmode="layer"): Artwork, Text, CUT, Guides (Guides hidden)
  <SKU> - cuff badge 60x50mm.pdf   real PDF layers (OCGs) Artwork, Text, CUT, Guides (Guides off, non-printing).
                                   Pure 7-bit ASCII (ASCII85 + Flate streams, header bytes patched) so it can be
                                   saved to Dropbox as a text file.
  <SKU> - cuff badge 60x50mm - preview.png   300 dpi render with guides on
  README.txt, Fonts/FONTS - DOWNLOAD LINK.txt, Fonts/OFL.txt

Size: plan/artwork-specs.md has no beanie cuff size yet, so the print area is 60 x 50 mm (marked ASK there).
Change TRIM_W / TRIM_H and re-run if the owner gives a different size.

Patterns follow tools/artwork/sticker_templates.py (not imported: that file is being edited elsewhere).
"""
import argparse
import base64
import io
import os
import subprocess
import sys
import zlib

if os.environ.get('PYTHONHASHSEED') != '0':   # font subsetting depends on set order: fix it so re-runs are byte-identical
    os.execvpe(sys.executable, [sys.executable] + sys.argv, {**os.environ, 'PYTHONHASHSEED': '0'})
from pathlib import Path

from reportlab import rl_config
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

rl_config.invariant = 1

HERE = Path(__file__).resolve().parent
FONT_DIR = HERE / 'assets' / 'fonts'
TODAY = '6 Oct 2026'
PT = 0.352778          # mm per point

TRIM_W, TRIM_H = 60.0, 50.0   # ASK: cuff print area (no size in artwork-specs.md yet)
BLEED = 3.0
SAFE = 3.0
CUT_W_PT = 0.25               # cut path: 0.25 pt, RGB 255,0,0, no fill, on the trim line

FONTS = {
    'bebas': ('BebasNeue-Regular.ttf', 'Bebas Neue', 400, 'https://fonts.google.com/specimen/Bebas+Neue',
              'https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf'),
    'barlow-sb': ('BarlowCondensed-SemiBold.ttf', 'Barlow Condensed', 600, 'https://fonts.google.com/specimen/Barlow+Condensed',
                  'https://github.com/google/fonts/raw/main/ofl/barlowcondensed/BarlowCondensed-SemiBold.ttf'),
}
FONT_COPYRIGHT = {
    'Bebas Neue': 'Copyright 2019 The Bebas Neue Project Authors (https://github.com/dharmatype/Bebas-Neue)',
    'Barlow Condensed': 'Copyright 2017 The Barlow Project Authors (https://github.com/jpt/barlow)',
}
for key, (fn, *_r) in FONTS.items():
    pdfmetrics.registerFont(TTFont(key, str(FONT_DIR / fn)))

# CMYK percentages, all well inside a normal CMYK gamut (no rich blacks over 300% TAC)
WHITE = (0, 0, 0, 0)            # badge backing: prints as white ink on the DTF transfer
NAVY = (100, 80, 20, 30)        # frame and text default: reads on every cuff colour because it sits on the white backing
PLACEHOLDER = (0, 0, 0, 45)
GUIDE_BLEED = (70, 0, 100, 0)
GUIDE_SAFE = (0, 100, 0, 0)
GUIDE_TEXT = (0, 0, 0, 70)

# SKU, short title (Dropbox folder), colourway as on the store (plan/product-facts.md order)
PRODUCTS = [
    ('FOXY-DTF-PBH-01', 'Personalised Bobble Hat Black Red & White', 'Black/Classic Red/White'),
    ('FOXY-DTF-PBH-02', 'Personalised Bobble Hat Black & Gold', 'Black/Gold'),
    ('FOXY-DTF-PBH-03', 'Personalised Bobble Hat Black & White', 'Black/White'),
    ('FOXY-DTF-PBH-04', 'Personalised Bobble Hat Royal Blue & White', 'Royal/White'),
    ('FOXY-DTF-PBH-05', 'Personalised Bobble Hat Red & White', 'Classic Red/White'),
    ('FOXY-DTF-PBH-06', 'Personalised Bobble Hat Navy Red & White', 'French Navy/Red/White'),
    ('FOXY-DTF-PBH-07', 'Personalised Bobble Hat Navy & White', 'Navy/White'),
    ('FOXY-DTF-PBH-08', 'Personalised Bobble Hat Green & White', 'Kelly Green/White'),
]

LAYERS = ('Artwork', 'Text', 'CUT', 'Guides')


# ---------------------------------------------------------------- drawing model (mm, origin top-left of the bleed box)
class Doc:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.layers = {n: [] for n in LAYERS}
        self.fonts = set()

    def add(self, layer, op):
        self.layers[layer].append(op)
        if op[0] == 'text':
            self.fonts.add(op[4])


def rect(x, y, w, h, r=0, fill=None, stroke=None, sw=0.0, dash=None, rgb_stroke=None):
    return ('rect', x, y, w, h, r, fill, stroke, sw, dash, rgb_stroke)


def text(x, y, s, font, size_pt, fill, anchor='middle', id_=None):
    return ('text', x, y, s, font, size_pt, fill, anchor, id_)


def cmyk_to_rgb(c, m, y, k):
    c, m, y, k = (v / 100 for v in (c, m, y, k))
    return tuple(round(255 * (1 - a) * (1 - k)) for a in (c, m, y))


def hexrgb(rgb):
    return '#%02x%02x%02x' % rgb


def fmt(v):
    s = ('%.3f' % v).rstrip('0').rstrip('.')
    return s if s != '-0' else '0'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def text_width(s, font, size_pt):
    return pdfmetrics.stringWidth(s, font, size_pt) * PT


def fit_size(s, font, max_w, max_pt):
    size = max_pt
    while text_width(s, font, size) > max_w and size > 4:
        size -= 0.25
    return size


def badge_doc():
    W, H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
    d = Doc(W, H)
    t0x, t0y = BLEED, BLEED                       # trim box top-left
    s0x, s0y = BLEED + SAFE, BLEED + SAFE         # safe box top-left
    sw_, sh_ = TRIM_W - 2 * SAFE, TRIM_H - 2 * SAFE
    cx = W / 2

    # Artwork: white backing runs into the bleed, navy frame inside the safe area, dashed logo box
    d.add('Artwork', rect(0, 0, W, H, fill=WHITE))
    fr = 1.0                                      # frame inset from the safe line
    d.add('Artwork', rect(s0x + fr, s0y + fr, sw_ - 2 * fr, sh_ - 2 * fr, r=2.5, stroke=NAVY, sw=0.6))
    logo_w, logo_h = 30.0, 22.0
    logo_y = s0y + 3.0
    d.add('Artwork', rect(cx - logo_w / 2, logo_y, logo_w, logo_h, r=1.0, stroke=PLACEHOLDER, sw=0.3, dash=(1.2, 0.8)))
    d.add('Artwork', text(cx, logo_y + logo_h / 2 - 0.4, 'YOUR BADGE', 'barlow-sb', 7, PLACEHOLDER))
    d.add('Artwork', text(cx, logo_y + logo_h / 2 + 2.9, 'OR LOGO HERE', 'barlow-sb', 7, PLACEHOLDER))

    # Text: live, editable club/business name and an optional line under it
    inner_w = sw_ - 2 * fr - 4.0
    name = 'YOUR CLUB NAME'
    name_pt = fit_size(name, 'bebas', inner_w, 15)
    name_base = logo_y + logo_h + 7.2
    d.add('Text', text(cx, name_base, name, 'bebas', name_pt, NAVY, id_='Club_or_business_name'))
    line = 'Optional line - Est. 1985'
    line_pt = fit_size(line, 'barlow-sb', inner_w, 8)
    d.add('Text', text(cx, name_base + 4.6, line, 'barlow-sb', line_pt, NAVY, id_='Text_under_design'))

    # CUT: red 0.25 pt trim path
    d.add('CUT', rect(t0x, t0y, TRIM_W, TRIM_H, rgb_stroke=(255, 0, 0), sw=CUT_W_PT * PT))

    # Guides (hidden, non-printing): bleed edge, safe area, labels
    d.add('Guides', rect(0.15, 0.15, W - 0.3, H - 0.3, stroke=GUIDE_BLEED, sw=0.2, dash=(1, 0.7)))
    d.add('Guides', rect(s0x, s0y, sw_, sh_, stroke=GUIDE_SAFE, sw=0.2, dash=(1, 0.7)))
    d.add('Guides', text(cx, 2.1, 'BLEED 3 mm', 'barlow-sb', 4.5, GUIDE_TEXT))
    d.add('Guides', text(cx, H - 0.8, 'TRIM %g x %g mm  |  SAFE 3 mm' % (TRIM_W, TRIM_H), 'barlow-sb', 4.5, GUIDE_TEXT))
    return d


# ---------------------------------------------------------------- writers
def paint_attrs(fill, stroke, sw, dash, rgb_stroke):
    a = ' fill="%s"' % (hexrgb(cmyk_to_rgb(*fill)) if fill else 'none')
    if rgb_stroke or stroke:
        col = hexrgb(rgb_stroke) if rgb_stroke else hexrgb(cmyk_to_rgb(*stroke))
        a += ' stroke="%s" stroke-width="%s"' % (col, fmt(sw))
        if dash:
            a += ' stroke-dasharray="%s"' % ','.join(fmt(x) for x in dash)
    return a


def write_svg(doc, path, title):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
           'width="%smm" height="%smm" viewBox="0 0 %s %s">' % (fmt(doc.w), fmt(doc.h), fmt(doc.w), fmt(doc.h)),
           '<title>%s</title>' % esc(title),
           '<!-- Colours are CMYK-safe; CMYK values are in each element\'s data-cmyk attribute. -->']
    for name, ops in doc.layers.items():
        style = ' style="display:none"' if name == 'Guides' else ''
        out.append('<g id="%s" inkscape:groupmode="layer" inkscape:label="%s"%s>' % (name, name, style))
        for op in ops:
            if op[0] == 'rect':
                _, x, y, w, h, r, fill, stroke, sw, dash, rgbs = op
                rr = ' rx="%s"' % fmt(r) if r else ''
                cm = fill or stroke
                dc = ' data-cmyk="%s"' % ','.join(str(v) for v in cm) if cm else ''
                out.append('<rect x="%s" y="%s" width="%s" height="%s"%s%s%s/>'
                           % (fmt(x), fmt(y), fmt(w), fmt(h), rr, paint_attrs(fill, stroke, sw, dash, rgbs), dc))
            elif op[0] == 'text':
                _, x, y, s, font, size, fill, anchor, id_ = op
                _fn, fam, weight, _u, _r = FONTS[font]
                idattr = ' id="%s"' % id_ if id_ else ''
                out.append('<text%s x="%s" y="%s" font-family="\'%s\', sans-serif" font-weight="%d" font-size="%s" '
                           'text-anchor="%s" fill="%s" data-cmyk="%s">%s</text>'
                           % (idattr, fmt(x), fmt(y), fam, weight, fmt(size * PT), anchor,
                              hexrgb(cmyk_to_rgb(*fill)), ','.join(str(v) for v in fill), esc(s)))
        out.append('</g>')
    out.append('</svg>')
    Path(path).write_text('\n'.join(out) + '\n', encoding='utf-8')


def write_pdf(doc, path, title, guides_on):
    H = doc.h
    c = canvas.Canvas(str(path), pagesize=(doc.w * mm, doc.h * mm), pageCompression=0)
    c.setTitle(title)
    c.setAuthor('Foxy Printing')
    c.setTrimBox((BLEED * mm, BLEED * mm, (BLEED + TRIM_W) * mm, (BLEED + TRIM_H) * mm))
    c.setBleedBox((0, 0, doc.w * mm, doc.h * mm))
    for name in LAYERS:
        c._code.append('/OC /%s BDC' % name)
        for op in doc.layers[name]:
            c.saveState()
            if op[0] == 'rect':
                _, x, y, w, h, r, fill, stroke, sw, dash, rgbs = op
                if fill:
                    c.setFillColorCMYK(*(v / 100 for v in fill))
                if rgbs:
                    c.setStrokeColorRGB(*(v / 255 for v in rgbs))
                elif stroke:
                    c.setStrokeColorCMYK(*(v / 100 for v in stroke))
                if rgbs or stroke:
                    c.setLineWidth(sw * mm)
                    if dash:
                        c.setDash([v * mm for v in dash])
                f, s = (1 if fill else 0), (1 if (rgbs or stroke) else 0)
                if r:
                    c.roundRect(x * mm, (H - y - h) * mm, w * mm, h * mm, r * mm, stroke=s, fill=f)
                else:
                    c.rect(x * mm, (H - y - h) * mm, w * mm, h * mm, stroke=s, fill=f)
            elif op[0] == 'text':
                _, x, y, s, font, size, fill, anchor, _id = op
                c.setFont(font, size)
                c.setFillColorCMYK(*(v / 100 for v in fill))
                {'middle': c.drawCentredString, 'start': c.drawString, 'end': c.drawRightString}[anchor](x * mm, (H - y) * mm, s)
            c.restoreState()
        c._code.append('EMC')
    c.showPage()
    c.save()
    finish_pdf(path, guides_on)


def dehint(font_bytes):
    from fontTools.ttLib import TTFont as FTFont
    f = FTFont(io.BytesIO(font_bytes), recalcTimestamp=False)
    for tag in ('fpgm', 'prep', 'cvt ', 'gasp', 'hdmx', 'LTSH', 'VDMX'):
        if tag in f:
            del f[tag]
    glyf = f['glyf']
    for gname in f.getGlyphOrder():
        glyf[gname].removeHinting()
    buf = io.BytesIO()
    f.save(buf)
    return buf.getvalue()


def finish_pdf(path, guides_on):
    """Add the OCG layers, re-encode every stream as ASCII85+Flate and make the whole file 7-bit ASCII."""
    import pikepdf
    with pikepdf.open(path, allow_overwriting_input=True) as pdf:
        ocg = {}
        for n in LAYERS:
            dct = pikepdf.Dictionary(Type=pikepdf.Name.OCG, Name=n)
            if n == 'Guides':
                dct.Usage = pikepdf.Dictionary(Print=pikepdf.Dictionary(PrintState=pikepdf.Name.OFF))
            ocg[n] = pdf.make_indirect(dct)
        order = pikepdf.Array([ocg[n] for n in LAYERS])
        on = pikepdf.Array([ocg[n] for n in LAYERS if guides_on or n != 'Guides'])
        off = pikepdf.Array([] if guides_on else [ocg['Guides']])
        pdf.Root.OCProperties = pikepdf.Dictionary(
            OCGs=order,
            D=pikepdf.Dictionary(Name='Layers', Order=order, ON=on, OFF=off,
                                 AS=pikepdf.Array([pikepdf.Dictionary(Event=pikepdf.Name.Print,
                                                                      Category=pikepdf.Array([pikepdf.Name.Print]), OCGs=order)])))
        for page in pdf.pages:
            page.obj.Resources.Properties = pikepdf.Dictionary({'/' + n: ocg[n] for n in LAYERS})
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
    with pikepdf.open(path) as pdf:     # must still open cleanly, with 4 layers
        assert len(pdf.pages) == 1
        assert [str(o.Name) for o in pdf.Root.OCProperties.OCGs] == list(LAYERS)


# ---------------------------------------------------------------- text files
def fonts_txt(doc):
    out = ['FONTS USED IN THIS TEMPLATE (all free, SIL Open Font License 1.1 - see OFL.txt)', '']
    for key in sorted(doc.fonts):
        fn, fam, weight, page, raw = FONTS[key]
        out += ['- %s (%s, weight %d)' % (fam, fn, weight),
                '  Google Fonts page: %s' % page,
                '  Direct .ttf download: %s' % raw,
                '  %s' % FONT_COPYRIGHT[fam], '']
    out += ['Install the fonts before opening the SVG/PDF in Illustrator, otherwise the live text is substituted.',
            'A copy of each font file is also kept in the website repo: foxyprinting-rebrand/tools/artwork/assets/fonts/']
    return '\n'.join(out) + '\n'


def ofl_txt():
    body = (FONT_DIR / 'OFL.txt').read_text(encoding='utf-8')
    body = body[body.index('This Font Software is licensed'):]
    head = '\n'.join(FONT_COPYRIGHT[f] for f in ('Bebas Neue', 'Barlow Condensed'))
    return head + '\n\n' + body


def readme(sku, short, colour, name):
    W, H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
    return f"""{short} - {sku}
Print-ready, editable cuff badge template, made {TODAY}.
Colourway: {colour}. The template is the same for all 8 bobble hat colours (FOXY-DTF-PBH-01 to -08).

PRODUCT FACTS (plan/product-facts.md, "Personalised bobble hats (Ralawise blank)")
- Blank: Beechfield B472 Stadium Beanie, one size (adult), 100% soft-touch acrylic, double-layer knit,
  striped turn-up cuff, contrasting pom pom, TearAway label. Never name the blank maker to customers.
- Personalisation: the customer's own badge or logo printed in full colour on the FRONT OF THE CUFF,
  plus an optional club/business name and an optional line of text under the design.
  Customer fields: "Badge or logo upload", "Club or business name (optional)",
  "Text to print under the design (optional)", "Message for us".
- Only print badges/logos the customer has the right to use (own club, school or business).

SIZE  (ASK - no cuff size in plan/artwork-specs.md yet)
- Print area (trim): {TRIM_W:g} x {TRIM_H:g} mm (landscape) - a sensible cuff badge size, NOT confirmed by the owner.
- Artboard with 3 mm bleed: {W:g} x {H:g} mm. Safe area: 3 mm inside the trim ({TRIM_W - 6:g} x {TRIM_H - 6:g} mm).
- ASK: cuff depth and width of the B472 when turned up, and the badge size the owner wants.
  Change TRIM_W / TRIM_H in the generator and re-run if it differs.

CUFF PLACEMENT
- Centre the badge on the front of the turned-up cuff, left to right over the front centre of the hat
  (opposite the back seam), and centred top to bottom within the cuff depth.
- ASK: exact distance from the cuff fold / lower edge, and whether it sits over the stripes as on the
  product photos.

THIS TEMPLATE (layers)
- Artwork: white badge backing (runs into the 3 mm bleed), navy frame inside the safe area, and the dashed
  "YOUR BADGE OR LOGO HERE" placeholder box. Replace the placeholder with the customer's badge/logo
  (vector, or 300 dpi or more at print size). Delete the backing and frame if the order is logo-only.
- Text: live, editable text - "YOUR CLUB NAME" (Bebas Neue) and "Optional line - Est. 1985"
  (Barlow Condensed SemiBold). Type the customer's club/business name and line; delete either if blank.
  Keep all text and logos inside the magenta safe line.
- CUT: red trim path, 0.25 pt stroke, RGB 255,0,0, no fill, exactly on the trim line ({TRIM_W:g} x {TRIM_H:g} mm).
  Use it to trim the transfer film; it never prints.
- Guides (hidden, non-printing): green dashed = 3 mm bleed edge, magenta dashed = 3 mm safe area.

COLOURS
- All colours are CMYK-safe: navy C100 M80 Y20 K30, white backing C0 M0 Y0 K0 (prints as white ink),
  placeholder K45. Change navy to the club colours if wanted; keep the total ink well under 300%.
- Any placed image must be 300 dpi at final size.

DTF PRINT AND PRESS
- Supply the artwork unmirrored (this file). The DTF RIP mirrors / adds the white underbase as set up on
  your printer. ASK: does your RIP need a pre-mirrored file? (none is included because the facts do not
  say so).
- Press settings (temperature, time, pressure, hot or cold peel) for the acrylic knit cuff: ASK - not in
  the product facts. Exact transfer method on knit is also ASK in product-facts.md. Test-press one hat first.

FILES
- {name}.svg : editable artwork (opens in Illustrator / Inkscape). Layers Artwork, Text, CUT, Guides.
- {name}.pdf : the same with real PDF layers Artwork / Text / CUT / Guides (Guides off and never prints),
               TrimBox {TRIM_W:g} x {TRIM_H:g} mm and BleedBox {W:g} x {H:g} mm.
- Fonts/     : FONTS - DOWNLOAD LINK.txt (Google Fonts URLs) and OFL.txt (licence).
- The PNG preview (300 dpi, guides on) is kept in the website repo, because Dropbox here only takes
  text files: foxyprinting-rebrand/exports/hat-artwork/{short} - {sku}/

Regenerate: python3 tools/artwork/hat_badge_template.py --out <folder>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    doc = badge_doc()
    for sku, short, colour in PRODUCTS:
        d = Path(a.out) / f'{short} - {sku}'
        (d / 'Fonts').mkdir(parents=True, exist_ok=True)
        name = f'{sku} - cuff badge {TRIM_W:g}x{TRIM_H:g}mm'
        title = f'Personalised bobble hat cuff badge template {TRIM_W:g}x{TRIM_H:g}mm - FOXY-DTF-PBH-01 to -08'  # same file for all 8
        write_svg(doc, d / f'{name}.svg', title)
        write_pdf(doc, d / f'{name}.pdf', title, guides_on=False)
        prev = d / '_preview.pdf'
        write_pdf(doc, prev, title, guides_on=True)
        subprocess.run(['pdftoppm', '-r', '300', '-png', '-singlefile', str(prev), str(d / f'{name} - preview')], check=True)
        prev.unlink()
        (d / 'README.txt').write_text(readme(sku, short, colour, name), encoding='utf-8')
        (d / 'Fonts' / 'FONTS - DOWNLOAD LINK.txt').write_text(fonts_txt(doc), encoding='utf-8')
        (d / 'Fonts' / 'OFL.txt').write_text(ofl_txt(), encoding='utf-8')
        print(d)


if __name__ == '__main__':
    main()
