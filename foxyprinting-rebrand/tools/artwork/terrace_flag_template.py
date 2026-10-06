"""Editable, print-ready templates for the personalised terrace flags (tag "DCD Terrace Flags", SKUs FOXY-FLAG-<CODE>-01..03).

Usage:
    python3 tools/artwork/terrace_flag_template.py --out exports/terrace-flag-artwork

One shared template set (3 sizes) is used by all 53 flag products. It writes:
  <out>/_templates/Terrace Flag Template <size>.svg   layers (inkscape:groupmode="layer"): Artwork, Text, CUT, Guides (Guides hidden)
  <out>/_templates/Terrace Flag Template <size>.pdf   real PDF layers (OCGs) Artwork, Text, CUT, Guides (Guides off, non-printing),
                                                     TrimBox/BleedBox set. Pure 7-bit ASCII (ASCII85 + Flate streams, header
                                                     bytes patched) so it can be saved to Dropbox as a text file.
  <out>/_templates/Terrace Flag Template <size> - preview.png   small render with guides on (repo only)
  <out>/_templates/Fonts/FONTS - DOWNLOAD LINK.txt, OFL.txt
  <out>/<short title> - FOXY-FLAG-<CODE>/README.txt   one per product: names the club/country design and its colours

Dropbox layout (owner's rule, one folder per product): /AI DESIGNS 2026/<short title> - FOXY-FLAG-<CODE>/ holding the 3 size
templates (SVG + PDF), README.txt and Fonts/. The first folder gets the files with create_file; the rest are Dropbox copies.

Settings (plan/artwork-specs.md, "Terrace flags"):
- Trim = finished flag size: 3ft x 2ft 914 x 610 mm, 5ft x 3ft 1524 x 914 mm, 8ft x 5ft 2438 x 1524 mm.
- Bleed 3 mm past the trim. ASK: the sewn-flag hem/bleed allowance with 25 mm binding is not in the specs yet.
- Safe area 25 mm inside the trim (covers the 25 mm edge binding and the eyelets). ASK.
- Eyelets: centred 12.5 mm in from each edge (middle of the binding), one at each corner plus evenly spaced along every
  edge at no more than EYELET_MAX_GAP mm apart. ASK: real eyelet count/spacing.
- Images: 150 dpi at full size for 3x2 and 5x3, 100 dpi for 8x5 (large-format default). ASK.
- CUT layer: red (RGB 255,0,0) 0.25 pt trim path, no fill. Guides never print.
"""
import argparse
import base64
import io
import json
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
REPO = HERE.parent.parent
FONT_DIR = HERE / 'assets' / 'fonts'
TODAY = '6 Oct 2026'
PT = 0.352778          # mm per point

SIZES = [  # label, trim W, trim H (mm), image dpi at full size
    ('3ft x 2ft', 914.0, 610.0, 150),
    ('5ft x 3ft', 1524.0, 914.0, 150),
    ('8ft x 5ft', 2438.0, 1524.0, 100),
]
BLEED = 3.0          # ASK: hem/bleed allowance for sewn flags
SAFE = 25.0          # ASK: binding 25 mm + eyelets
EYELET_INSET = 12.5  # ASK: eyelet centre from the trim edge
EYELET_D = 12.0      # marker diameter
EYELET_MAX_GAP = 500.0  # ASK: max spacing between eyelets
CUT_W_PT = 0.25

FONTS = {   # one open-licence font, so the ASCII PDFs stay small enough to save to Dropbox as text
    'bebas': ('BebasNeue-Regular.ttf', 'Bebas Neue', 400, 'https://fonts.google.com/specimen/Bebas+Neue',
              'https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf'),
}
SHOPIFY_FONT_URLS = {  # copies in Shopify Files (fileCreate from the Google Fonts GitHub .ttf, 6 Oct 2026)
    'Bebas Neue': 'https://cdn.shopify.com/s/files/1/1774/9115/files/BebasNeue-Regular.ttf?v=1791283074',
}
FONT_COPYRIGHT = {
    'Bebas Neue': 'Copyright 2019 The Bebas Neue Project Authors (https://github.com/dharmatype/Bebas-Neue)',
}
for key, (fn, *_r) in FONTS.items():
    pdfmetrics.registerFont(TTFont(key, str(FONT_DIR / fn)))

# CMYK percentages, CMYK-safe (TAC well under 300%)
NAVY = (100, 80, 20, 30)
WHITE = (0, 0, 0, 0)
PLACEHOLDER = (0, 0, 0, 45)
GUIDE_BLEED = (70, 0, 100, 0)
GUIDE_TRIM = (100, 0, 0, 0)
GUIDE_SAFE = (0, 100, 0, 0)
GUIDE_EYELET = (0, 60, 100, 0)
GUIDE_TEXT = (0, 0, 0, 70)

LAYERS = ('Artwork', 'Text', 'CUT', 'Guides')

# code -> (short title for the Dropbox folder, design and colours as seen on the main product photo, 6 Oct 2026)
PRODUCTS = {
    'CFLAG01': ('China Terrace Flag', 'China national flag: red with five yellow stars'),
    'CFLAG02': ('England Terrace Flag', 'England St George cross: white with a red cross'),
    'CFLAG03': ('India Terrace Flag', 'India tricolour: saffron, white and green with the navy Ashoka Chakra'),
    'CFLAG04': ('Scotland Terrace Flag', 'Scotland saltire: blue with a white diagonal cross'),
    'CFLAG06': ('Italy Terrace Flag', 'Italy tricolore: green, white and red vertical bands'),
    'CFLAG07': ('South Africa Terrace Flag', 'South Africa flag: green, gold, black, white, red and blue'),
    'CFLAG08': ('South Korea Terrace Flag', 'South Korea flag: white with the red and blue taegeuk and black trigrams'),
    'CFLAG09': ('Spain Terrace Flag', 'Spain flag: red and yellow bands with the Spanish coat of arms'),
    'CFLAG10': ('Turkey Terrace Flag', 'Turkey flag: red with a white crescent and star'),
    'CFLAG11': ('Ukraine Terrace Flag', 'Ukraine flag: blue over yellow'),
    'CFLAG12': ('Union Jack Terrace Flag', 'Union Jack: red, white and blue'),
    'CFLAG13': ('Union Jack Terrace Flag Design 2', 'Union Jack in the top corner of a blue flag, panels down the right-hand side'),
    'CFLAG14': ('USA Terrace Flag', 'USA stars and stripes: red, white and blue'),
    'CFLAG15': ('Wales Terrace Flag', 'Wales flag: green and white with the red dragon'),
    'FFLAG1': ('England Football Fan Terrace Flag', 'Red and white St George cross with a football'),
    'FFLAG2': ('Arsenal Fan Terrace Flag', 'Red centre, white sides with navy-blue edge stripes'),
    'FFLAG3': ('Aston Villa Fan Terrace Flag', 'Claret and white diagonal bands on sky blue'),
    'FFLAG4': ('Brentford Fan Terrace Flag', 'Red and white vertical stripes with a white text band'),
    'FFLAG5': ('Brighton Fan Terrace Flag', 'Blue, white and blue horizontal bands'),
    'FFLAG6': ('Chelsea Fan Terrace Flag', 'White with a royal blue swoosh and a football'),
    'FFLAG7': ('Crystal Palace Fan Terrace Flag', 'Red with red, white and blue stripes at the hoist and a blue fly-end bar'),
    'FFLAG8': ('Everton Fan Terrace Flag', 'Royal blue and white with thin yellow stripes'),
    'FFLAG9': ('Fulham Fan Terrace Flag', 'White with black diagonal swooshes'),
    'FFLAG10': ('Ipswich Fan Terrace Flag', 'Red, white and blue watercolour design with round photo panels'),
    'FFLAG11': ('Leicester City Fan Terrace Flag', 'Royal blue with blue and white chequered corners'),
    'FFLAG12': ('Liverpool Fan Terrace Flag', 'Red with white diagonal bands and red and yellow chequered corners'),
    'FFLAG13': ('Man City Treble Fan Terrace Flag', 'Black, white and sky blue horizontal bands'),
    'FFLAG14': ('Man United Fan Terrace Flag', 'Red, white and black horizontal bands'),
    'FFLAG15': ('Newcastle Fan Terrace Flag', 'White with black diagonal stripes'),
    'FFLAG16': ('Nottingham Forest Fan Terrace Flag', 'Red and white chequerboard with a white text band'),
    'FFLAG17': ('Southampton Fan Terrace Flag', 'White with red diagonal swooshes'),
    'FFLAG18': ('Tottenham Fan Terrace Flag', 'White with navy bands top and bottom'),
    'FFLAG19': ('West Ham Fan Terrace Flag', 'Claret with white chequers and a white text band'),
    'FFLAG20': ('Wolves Fan Terrace Flag', 'Old gold with white chequers and a white text band'),
    'FFLAG21': ('Wolves Fan Terrace Flag Design 2', 'Old gold with black and gold chequered ends'),
    'FFLAG22': ('West Ham Fan Terrace Flag Design 2', 'Claret with claret and sky blue chequered ends'),
    'FFLAG23': ('West Ham Fan Terrace Flag Design 3', 'Claret with claret and sky blue chequered ends (photo matches Design 2)'),
    'FFLAG24': ('Tottenham Fan Terrace Flag Design 2', 'Navy, white and navy horizontal bands'),
    'FFLAG25': ('Southampton Fan Terrace Flag Design 2', 'Red and white vertical stripes with two white text bands'),
    'FFLAG26': ('Nottingham Forest Fan Terrace Flag Design 2', 'Red with red and white chequered ends'),
    'FFLAG27': ('Newcastle Fan Terrace Flag Design 2', 'Black and white vertical stripes with two white text bands'),
    'FFLAG28': ('Man United Fan Terrace Flag Design 2', 'Red, white and black horizontal bands, one round centre panel'),
    'FFLAG29': ('Man City Treble Fan Terrace Flag Design 2', 'Black, white and sky blue bands with three gold trophy shapes'),
    'FFLAG30': ('Liverpool Fan Terrace Flag Design 2', 'Red with red and yellow chequered ends'),
    'FFLAG31': ('Leicester City Fan Terrace Flag Design 2', 'Royal blue with blue and white chequered ends'),
    'FFLAG32': ('Ipswich Fan Terrace Flag Design 2', 'Royal blue with thin white and red pinstripes'),
    'FFLAG33': ('Fulham Fan Terrace Flag Design 2', 'Black, white and black horizontal bands'),
    'FFLAG35': ('Crystal Palace Fan Terrace Flag Design 2', 'Red centre between blue side bars edged in white'),
    'FFLAG36': ('Chelsea Fan Terrace Flag Design 2', 'Royal blue with a blue and white chequered band'),
    'FFLAG37': ('Brighton Fan Terrace Flag Design 2', 'Blue, white and blue horizontal bands with yellow lettering'),
    'FFLAG38': ('Brentford Fan Terrace Flag Design 2', 'Red and white vertical stripes with two white text bands'),
    'FFLAG39': ('Aston Villa Fan Terrace Flag Design 2', 'Claret, sky blue and claret horizontal bands'),
    'FFLAG40': ('Arsenal Fan Terrace Flag Design 2', 'Red centre, white sides with blue pinstripes'),
}


# ---------------------------------------------------------------- drawing model (mm, origin top-left of the bleed box)
class Doc:
    def __init__(self, w, h, trim_w, trim_h):
        self.w, self.h, self.trim_w, self.trim_h = w, h, trim_w, trim_h
        self.layers = {n: [] for n in LAYERS}
        self.fonts = set()

    def add(self, layer, op):
        self.layers[layer].append(op)
        if op[0] == 'text':
            self.fonts.add(op[4])


def rect(x, y, w, h, fill=None, stroke=None, sw=0.0, dash=None, rgb_stroke=None):
    return ('rect', x, y, w, h, fill, stroke, sw, dash, rgb_stroke)


def circle(cx, cy, r, fill=None, stroke=None, sw=0.0, dash=None):
    return ('circle', cx, cy, r, fill, stroke, sw, dash)


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
        size -= 0.5
    return size


def eyelet_positions(tw, th):
    """Eyelet centres (trim coordinates): corners plus evenly spaced along each edge, gap <= EYELET_MAX_GAP."""
    def along(length):
        span = length - 2 * EYELET_INSET
        n = max(1, -(-int(span) // int(EYELET_MAX_GAP)))     # segments
        return [EYELET_INSET + span * i / n for i in range(n + 1)]
    xs, ys = along(tw), along(th)
    pts = {(x, EYELET_INSET) for x in xs} | {(x, th - EYELET_INSET) for x in xs}
    pts |= {(EYELET_INSET, y) for y in ys} | {(tw - EYELET_INSET, y) for y in ys}
    return sorted(pts)


def flag_doc(tw, th):
    W, H = tw + 2 * BLEED, th + 2 * BLEED
    d = Doc(W, H, tw, th)
    cx = W / 2
    s0x, s0y = BLEED + SAFE, BLEED + SAFE
    sw_, sh_ = tw - 2 * SAFE, th - 2 * SAFE
    band = H / 3

    # Artwork: placeholder background in design colours (navy / white / navy), runs into the bleed
    d.add('Artwork', rect(0, 0, W, H, fill=NAVY))
    d.add('Artwork', rect(0, band, W, band, fill=WHITE))
    r = band * 0.42
    d.add('Artwork', circle(cx, H / 2, r, stroke=PLACEHOLDER, sw=th * 0.003, dash=(th * 0.012, th * 0.008)))
    lab = th * 0.022 / PT
    d.add('Artwork', text(cx, H / 2 - th * 0.005, 'LOGO / PHOTO', 'bebas', lab, PLACEHOLDER))
    d.add('Artwork', text(cx, H / 2 + th * 0.03, 'REPLACE BACKGROUND WITH THE FLAG DESIGN', 'bebas', lab * 0.55, PLACEHOLDER))

    # Text: live, editable lines, centred in the top and bottom bands, inside the safe area
    l1 = 'YOUR NAME / GROUP'
    l1_pt = fit_size(l1, 'bebas', sw_ * 0.9, (band - SAFE) * 0.62 / PT)
    d.add('Text', text(cx, BLEED + SAFE + (band - BLEED - SAFE) / 2 + l1_pt * PT * 0.35, l1, 'bebas', l1_pt, WHITE,
                       id_='Text_on_the_flag'))
    l2 = 'SECOND LINE - EST. 2026'
    l2_pt = fit_size(l2, 'bebas', sw_ * 0.8, (band - SAFE) * 0.42 / PT)
    d.add('Text', text(cx, 2 * band + (band - SAFE - BLEED) / 2 + l2_pt * PT * 0.35, l2, 'bebas', l2_pt, WHITE,
                       id_='Second_line'))

    # CUT: red 0.25 pt path on the trim line
    d.add('CUT', rect(BLEED, BLEED, tw, th, rgb_stroke=(255, 0, 0), sw=CUT_W_PT * PT))

    # Guides (hidden, non-printing)
    g = th * 0.0015
    dash = (th * 0.008, th * 0.005)
    d.add('Guides', rect(g / 2, g / 2, W - g, H - g, stroke=GUIDE_BLEED, sw=g, dash=dash))
    d.add('Guides', rect(BLEED, BLEED, tw, th, stroke=GUIDE_TRIM, sw=g))
    d.add('Guides', rect(s0x, s0y, sw_, sh_, stroke=GUIDE_SAFE, sw=g, dash=dash))
    for ex, ey in eyelet_positions(tw, th):
        d.add('Guides', circle(BLEED + ex, BLEED + ey, EYELET_D / 2, stroke=GUIDE_EYELET, sw=max(g, 0.8)))
    gl = th * 0.012 / PT
    d.add('Guides', text(cx, s0y + min(gl, 30) * PT + 3, 'TRIM %g x %g MM - BLEED %g MM - SAFE %g MM - EYELETS ORANGE'
                         % (tw, th, BLEED, SAFE), 'bebas', min(gl, 30), GUIDE_TEXT))
    return d


# ---------------------------------------------------------------- writers
def paint_attrs(fill, stroke, sw, dash, rgb_stroke=None):
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
           '<!-- Colours are CMYK-safe; CMYK values are in each element\'s data-cmyk attribute. Units: mm. -->']
    for name, ops in doc.layers.items():
        style = ' style="display:none"' if name == 'Guides' else ''
        out.append('<g id="%s" inkscape:groupmode="layer" inkscape:label="%s"%s>' % (name, name, style))
        for op in ops:
            if op[0] == 'rect':
                _, x, y, w, h, fill, stroke, sw, dash, rgbs = op
                cm = fill or stroke
                dc = ' data-cmyk="%s"' % ','.join(str(v) for v in cm) if cm else ''
                out.append('<rect x="%s" y="%s" width="%s" height="%s"%s%s/>'
                           % (fmt(x), fmt(y), fmt(w), fmt(h), paint_attrs(fill, stroke, sw, dash, rgbs), dc))
            elif op[0] == 'circle':
                _, ccx, ccy, r, fill, stroke, sw, dash = op
                cm = fill or stroke
                out.append('<circle cx="%s" cy="%s" r="%s"%s data-cmyk="%s"/>'
                           % (fmt(ccx), fmt(ccy), fmt(r), paint_attrs(fill, stroke, sw, dash), ','.join(str(v) for v in cm)))
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
    c.setTrimBox((BLEED * mm, BLEED * mm, (BLEED + doc.trim_w) * mm, (BLEED + doc.trim_h) * mm))
    c.setBleedBox((0, 0, doc.w * mm, doc.h * mm))
    for name in LAYERS:
        c._code.append('/OC /%s BDC' % name)
        for op in doc.layers[name]:
            c.saveState()
            if op[0] in ('rect', 'circle'):
                if op[0] == 'rect':
                    _, x, y, w, h, fill, stroke, sw, dash, rgbs = op
                else:
                    _, ccx, ccy, r, fill, stroke, sw, dash = op
                    rgbs = None
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
                if op[0] == 'rect':
                    c.rect(x * mm, (H - y - h) * mm, w * mm, h * mm, stroke=s, fill=f)
                else:
                    c.circle(ccx * mm, (H - ccy) * mm, r * mm, stroke=s, fill=f)
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
    with pikepdf.open(path) as pdf:
        assert len(pdf.pages) == 1
        assert [str(o.Name) for o in pdf.Root.OCProperties.OCGs] == list(LAYERS)


# ---------------------------------------------------------------- text files
def fonts_txt():
    out = ['FONTS USED IN THESE TEMPLATES (all free, SIL Open Font License 1.1 - see OFL.txt)', '']
    for key in sorted(FONTS):
        fn, fam, weight, page, raw = FONTS[key]
        out += ['- %s (%s, weight %d)' % (fam, fn, weight),
                '  Google Fonts page: %s' % page,
                '  Direct .ttf download: %s' % raw,
                '  Shopify Files copy: %s' % SHOPIFY_FONT_URLS.get(fam, '(not uploaded)'),
                '  %s' % FONT_COPYRIGHT[fam], '']
    out += ['Install the fonts before opening the SVG/PDF in Illustrator, otherwise the live text is substituted.',
            'A copy of each font file is also kept in the website repo: foxyprinting-rebrand/tools/artwork/assets/fonts/']
    return '\n'.join(out) + '\n'


def ofl_txt():
    body = (FONT_DIR / 'OFL.txt').read_text(encoding='utf-8')
    body = body[body.index('This Font Software is licensed'):]
    head = '\n'.join(FONT_COPYRIGHT.values())
    return head + '\n\n' + body


def file_name(label, tw, th):
    return 'Terrace Flag Template %s (%gx%gmm)' % (label.replace(' ', ''), tw, th)


def readme(code, short, design, listing):
    sku = 'FOXY-FLAG-%s' % code
    lines = []
    for label, tw, th, dpi in SIZES:
        n = eyelet_positions(tw, th)
        lines.append(f'- {label}: trim {tw:g} x {th:g} mm, artboard with bleed {tw + 2 * BLEED:g} x {th + 2 * BLEED:g} mm, '
                     f'{len(n)} eyelets, images {dpi} dpi at full size -> "{file_name(label, tw, th)}.svg / .pdf"')
    return f"""{short} - {sku}
Print-ready, editable terrace flag templates, made {TODAY}.

PRODUCT
- Shopify title: {listing.get('title', '')}
- Variant SKUs: {sku}-01 (3ft x 2ft), {sku}-02 (5ft x 3ft), {sku}-03 (8ft x 5ft)
- Design on the product photo: {design}
- Google colour: {listing.get('color', '')}
- Customer fields: "Text on the flag (name, group or town)", "Second line (optional)", "Logo upload (optional)",
  "Message for us (anything else)".

PRODUCT FACTS (plan/product-facts.md, "Stadium / terrace flags")
- 115gsm knitted polyester, digitally printed in the UK and hand-stitched, strong 25mm edge binding, eyelets on
  all 4 edges, single-sided print (double-sided on request), fire label on every flag.

THE TEMPLATES (one shared set, the same in every flag folder)
{chr(10).join(lines)}
- Bleed: {BLEED:g} mm past the trim on every edge. ASK - the hem/bleed allowance for sewn flags with 25 mm binding
  is not in plan/artwork-specs.md yet (some flag makers want 10-20 mm per edge for a turned hem).
- Safe area: {SAFE:g} mm inside the trim - keeps text and logos clear of the 25 mm binding and the eyelets. ASK.
- Eyelets (Guides layer, orange circles): centred {EYELET_INSET:g} mm in from the edge, one at each corner and
  evenly spaced along every edge, no more than {EYELET_MAX_GAP:g} mm apart. ASK - real count and spacing.
- Resolution: 150 dpi at full size for 3x2 and 5x3, 100 dpi for 8x5 (large-format default). ASK.

LAYERS
- Artwork: placeholder background in navy/white/navy bands with a dashed "LOGO / PHOTO" panel. Replace it with
  the flag design above ({design}). Keep the design running into the bleed.
- Text: live, editable text - "YOUR NAME / GROUP" and "SECOND LINE - EST. 2026", both in Bebas Neue (OFL).
  Swap in another open-licence font if you like. Type the customer's wording; keep it inside the magenta safe line.
- CUT: red trim path, 0.25 pt stroke, RGB 255,0,0, no fill, exactly on the trim line. Never prints.
- Guides (hidden, non-printing): green dashed = bleed edge, cyan = trim, magenta dashed = 25 mm safe area,
  orange circles = eyelets.

COLOURS
- CMYK-safe: navy C100 M80 Y20 K30, white C0 M0 Y0 K0, placeholder K45. Keep total ink well under 300%.

PRINTING - ASK
- Which printer/RIP prints the flags? An 8ft x 5ft flag needs a roll at least {SIZES[2][2] + 2 * BLEED:g} mm wide
  (or printing in panels), and the 24 in (610 mm) sublimation printer in plan/large-format-plan.md cannot print even
  the 3ft x 2ft flag with bleed in one piece. Confirm before quoting delivery times.
- Mirroring for transfer paper, ICC profile and fabric shrinkage allowance: ASK.

LICENSING
- Club names are used only to describe the design (fan-made, unofficial). Never add a real club crest, league
  logo or trophy artwork unless the owner confirms a licence.

FILES
- *.svg : editable artwork (Illustrator / Inkscape), layers Artwork, Text, CUT, Guides.
- *.pdf : the same with real PDF layers (Guides off and never prints), TrimBox = flag size, BleedBox = artboard.
- Fonts/ : FONTS - DOWNLOAD LINK.txt (Google Fonts URLs) and OFL.txt (licence).
- PNG previews are kept in the website repo only: foxyprinting-rebrand/exports/terrace-flag-artwork/_templates/

Regenerate: python3 tools/artwork/terrace_flag_template.py --out <folder>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    out = Path(a.out)
    tdir = out / '_templates'
    (tdir / 'Fonts').mkdir(parents=True, exist_ok=True)
    for label, tw, th, dpi in SIZES:
        doc = flag_doc(tw, th)
        name = file_name(label, tw, th)
        title = 'Personalised terrace flag template %s - %g x %g mm trim, %g mm bleed' % (label, tw, th, BLEED)
        write_svg(doc, tdir / f'{name}.svg', title)
        write_pdf(doc, tdir / f'{name}.pdf', title, guides_on=False)
        prev = tdir / '_preview.pdf'
        write_pdf(doc, prev, title, guides_on=True)
        subprocess.run(['pdftoppm', '-scale-to', '1400', '-png', '-singlefile', str(prev), str(tdir / f'{name} - preview')],
                       check=True)
        prev.unlink()
        print(tdir / name, (tdir / f'{name}.pdf').stat().st_size, 'bytes')
    (tdir / 'Fonts' / 'FONTS - DOWNLOAD LINK.txt').write_text(fonts_txt(), encoding='utf-8')
    (tdir / 'Fonts' / 'OFL.txt').write_text(ofl_txt(), encoding='utf-8')
    listings = {p['code']: p for p in json.loads((REPO / 'exports' / 'terrace-flags' / 'listings.json').read_text())}
    for code, (short, design) in PRODUCTS.items():
        d = out / f'{short} - FOXY-FLAG-{code}'
        d.mkdir(parents=True, exist_ok=True)
        (d / 'README.txt').write_text(readme(code, short, design, listings.get(code, {})), encoding='utf-8')
    print(len(PRODUCTS), 'product folders')


if __name__ == '__main__':
    main()
