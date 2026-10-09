"""Personalised Wheelie Bin Sticker - Design 1-36: editable, print-ready production artwork (6 Oct 2026).

Sticker (plan/product-facts.md): A5 210 x 148 mm, laminated outdoor vinyl. Page = trim + 3 mm bleed = 216 x 154 mm,
3 mm safe area. The owner's originals ("WHEELIE BIN - N.pdf", A4 landscape 297 x 210 mm) are recreated at A5
(scale 210/297, same proportions) with the house number and street name as LIVE text, sample "74 Make Believe Close".

Per design it writes into --out:
  <base>.svg          Illustrator-editable; top-level groups "Artwork" and "CUT" open as layers
  <base>.pdf          vector PDF with real layers "Artwork" and "CUT", fonts embedded, pure ASCII (Dropbox create_file)
  <base> - check.png  preview render (CUT line visible) to check by eye
CUT = red RGB 255,0,0 (CMYK 2/98/95/0), 0.25 mm, closed path at the trim; corners rounded 3 mm where the original
sticker has rounded corners. PageMARKs and the ColorCut job barcode are added by the owner in Illustrator.

Two kinds of design:
  * "frame" designs: background, rounded frames and (5, 18) the house icon are drawn here from measured values;
    no source file needed.
  * "deco" designs (ornate borders, scrolls, wreaths, vines): the ornaments are the owner's ORIGINAL VECTOR paths,
    read from the source PDF with PyMuPDF (--src DIR holding "N.pdf" or "WHEELIE BIN - N.pdf") and scaled to A5.
    Only the text is replaced (by live text), so these stay fully vector too.

Fonts (open licence, Google Fonts look-alikes of the owner's system fonts) are read from --fonts DIR (.ttf files).

Usage:
  python3 tools/artwork/wheelie_bin_stickers.py --fonts FONTDIR --out OUTDIR [--src SRCDIR] [--designs 1,2,5-9]
  (no --src: only the frame designs are built)
"""
import argparse
import re
import sys
from pathlib import Path

from reportlab import rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

rl_config.invariant = 1   # repeatable output
rl_config.useA85 = 1      # ASCII85 streams: the PDF is plain text

MM = 72 / 25.4
TRIM_W, TRIM_H, BLEED = 210.0, 148.0, 3.0
PAGE_W, PAGE_H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED
CUT_R = 3.0                       # rounded corner radius of the originals (A5 scale)
SCALE = 210 / 297                 # A4 original -> A5
TEXT = '#231f20'
FRAME = '#221f1f'
GREY = '#f1f2f2'
NUMBER, STREET_UC, STREET_MC = '74', 'MAKE BELIEVE CLOSE', 'Make Believe Close'

# font key -> (ttf file, SVG font-family list, svg weight, svg style)
FONTS = {
    'ptsans': ('PT_Sans-Web-Regular.ttf', "'PT Sans', 'PTSans-Regular'", 400, 'normal'),
    'marcellus': ('Marcellus-Regular.ttf', "'Marcellus', 'Marcellus-Regular'", 400, 'normal'),
    'arvo': ('Arvo-Regular.ttf', "'Arvo'", 400, 'normal'),
    'archivo': ('ArchivoBlack-Regular.ttf', "'Archivo Black', 'ArchivoBlack-Regular'", 400, 'normal'),
    'gilda': ('GildaDisplay-Regular.ttf', "'Gilda Display', 'GildaDisplay-Regular'", 400, 'normal'),
    'courgette': ('Courgette-Regular.ttf', "'Courgette', 'Courgette-Regular'", 400, 'normal'),
    'oldstd': ('OldStandard-Regular.ttf', "'Old Standard TT', 'OldStandardTT-Regular'", 400, 'normal'),
    'delius': ('Delius-Regular.ttf', "'Delius', 'Delius-Regular'", 400, 'normal'),
    'ribeye': ('Ribeye-Regular.ttf', "'Ribeye', 'Ribeye-Regular'", 400, 'normal'),
    'goudy': ('SortsMillGoudy-Regular.ttf', "'Sorts Mill Goudy', 'SortsMillGoudy-Regular'", 400, 'normal'),
    'patrick': ('PatrickHand-Regular.ttf', "'Patrick Hand', 'PatrickHand-Regular'", 400, 'normal'),
    'alegreyasc': ('AlegreyaSC-Bold.ttf', "'Alegreya SC', 'AlegreyaSC-Bold'", 700, 'normal'),
    'bowlby': ('BowlbyOne-Regular.ttf', "'Bowlby One', 'BowlbyOne-Regular'", 400, 'normal'),
    'anton': ('Anton-Regular.ttf', "'Anton', 'Anton-Regular'", 400, 'normal'),
    'crimson': ('CrimsonText-Regular.ttf', "'Crimson Text', 'CrimsonText-Regular'", 400, 'normal'),
    'crimsonit': ('CrimsonText-Italic.ttf', "'Crimson Text', 'CrimsonText-Italic'", 400, 'italic'),
    'shortstack': ('ShortStack-Regular.ttf', "'Short Stack', 'ShortStack-Regular'", 400, 'normal'),
    'lobster': ('Lobster-Regular.ttf', "'Lobster', 'Lobster-Regular'", 400, 'normal'),
    'federo': ('Federo-Regular.ttf', "'Federo', 'Federo-Regular'", 400, 'normal'),
    'kalam': ('Kalam-Bold.ttf', "'Kalam', 'Kalam-Bold'", 700, 'normal'),
    'della': ('DellaRespira-Regular.ttf', "'Della Respira', 'DellaRespira-Regular'", 400, 'normal'),
}
# owner's original font -> look-alike (for the README / fonts list)
ORIGINAL_FONT = {
    'ptsans': 'Myriad Pro', 'marcellus': 'Optimus Princeps / Adobe Arabic', 'arvo': 'Rockwell',
    'archivo': 'Adobe Gothic Std Bold', 'gilda': 'Kozuka Mincho Light', 'courgette': 'Lucida Handwriting',
    'oldstd': 'Imprint MT Shadow / Mongolian Baiti', 'delius': 'Maiandra GD', 'ribeye': 'Harrington',
    'goudy': 'Goudy Old Style / High Tower Text', 'patrick': 'MV Boli', 'alegreyasc': 'Nueva Std Bold',
    'bowlby': 'Poplar Std', 'anton': 'Haettenschweiler', 'crimson': 'Minion Pro / Palatino Linotype',
    'crimsonit': 'Lucida Fax Italic', 'shortstack': 'Kristen ITC', 'lobster': 'Magneto Bold',
    'federo': 'Lithos Pro', 'kalam': 'Kitten Bold', 'della': 'Poor Richard',
}


def T(role, font, size, cx, base, max_w, text=None, fill=TEXT):
    """A live text line. size in pt, cx/base in trim mm (y down), max_w = widest it may get (mm)."""
    if text is None:
        text = NUMBER if role == 'Number' else STREET_UC
    return dict(role=role, font=font, size=size, cx=cx, base=base, max_w=max_w, text=text, fill=fill)


F1 = [(3.82, 1.5, 2.25, True)]                           # single rounded frame on a white panel
F2 = [(3.82, 1.5, 2.25, True), (8.34, 1.5, 2.25, False)]  # double frame
# Measured from the owner's PDFs (A5 scale): baseline, centre and size of each text line.
DESIGNS = {
    1: dict(bg='#ffffff', frames=F2, texts=[T('Number', 'ptsans', 395.3, 105.0, 110.4, 176),
                                             T('Street', 'ptsans', 47.3, 105.0, 134.7, 182)]),
    2: dict(bg='#ffffff', frames=F2, texts=[T('Number', 'marcellus', 386.0, 105.0, 111.2, 176),
                                             T('Street', 'marcellus', 64.1, 105.0, 135.9, 182)]),
    3: dict(frames=F1, texts=[T('Number', 'arvo', 405.9, 105.0, 110.2, 190),
                              T('Street', 'arvo', 54.0, 105.0, 134.6, 190)]),
    4: dict(frames=F1, texts=[T('Number', 'archivo', 371.2, 105.0, 116.1, 190),
                              T('Street', 'marcellus', 72.0, 105.0, 135.7, 190)]),
    5: dict(frames=F1, house=5, texts=[T('Number', 'archivo', 200.0, 104.2, 120.0, 88, fill='#ffffff'),
                                       T('Street', 'archivo', 24.0, 104.2, 133.5, 124, fill='#ffffff')]),
    14: dict(frames=[(2.9, 1.5, 2.25, True)], texts=[T('Number', 'patrick', 383.9, 105.0, 110.3, 192),
                                                     T('Street', 'patrick', 67.2, 105.0, 135.6, 192)]),
    15: dict(frames=F2, texts=[T('Number', 'marcellus', 447.6, 105.0, 119.3, 176),
                               T('Street', 'alegreyasc', 75.1, 105.0, 133.8, 182)]),
    16: dict(frames=F2, texts=[T('Number', 'bowlby', 383.2, 105.0, 112.6, 166),
                               T('Street', 'bowlby', 97.2, 105.0, 135.3, 182)]),
    17: dict(frames=F2, texts=[T('Number', 'anton', 420.7, 105.0, 112.0, 176),
                               T('Street', 'anton', 85.4, 105.0, 137.5, 182)]),
    18: dict(frames=F1, house=18, texts=[T('Number', 'archivo', 213.4, 105.3, 112.5, 72, fill='#ffffff'),
                                         T('Street', 'ptsans', 79.2, 105.0, 141.8, 194)]),
    19: dict(frames=F1, texts=[T('Number', 'patrick', 363.4, 105.0, 105.7, 190),
                               T('Street', 'patrick', 55.2, 105.0, 121.7, 190, 'MAKE BELIEVE'),
                               T('Street line 2', 'patrick', 55.2, 105.0, 138.4, 190, 'CLOSE')]),
    20: dict(frames=F1, texts=[T('Number', 'oldstd', 437.7, 105.0, 118.8, 190),
                               T('Street', 'oldstd', 61.3, 105.0, 136.7, 188)]),
    21: dict(frames=F1, texts=[T('Number', 'crimson', 421.4, 105.0, 110.3, 190),
                               T('Street', 'crimson', 44.9, 105.0, 135.2, 186)]),
    22: dict(frames=F1, texts=[T('Number', 'delius', 442.6, 105.0, 118.8, 190),
                               T('Street', 'delius', 43.8, 105.0, 138.8, 192)]),
    23: dict(frames=F1, texts=[T('Number', 'crimsonit', 415.1, 105.0, 116.9, 190),
                               T('Street', 'crimsonit', 42.3, 105.0, 138.1, 190)]),
    24: dict(frames=F1, texts=[T('Number', 'shortstack', 417.2, 105.0, 116.6, 190),
                               T('Street', 'shortstack', 35.3, 105.0, 136.7, 190)]),
    26: dict(frames=F2, texts=[T('Number', 'lobster', 403.7, 105.0, 116.8, 176),
                               T('Street', 'lobster', 40.3, 105.0, 135.2, 182)]),
    27: dict(frames=F2, texts=[T('Number', 'federo', 367.0, 105.0, 111.4, 176),
                               T('Street', 'federo', 50.9, 105.0, 131.7, 182)]),
    28: dict(frames=F1, texts=[T('Number', 'shortstack', 427.1, 105.0, 111.2, 190),
                               T('Street', 'shortstack', 44.5, 104.2, 138.4, 192)]),
    29: dict(frames=F1, texts=[T('Number', 'shortstack', 422.1, 105.0, 115.8, 190),
                               T('Street', 'kalam', 44.5, 105.0, 136.8, 186)]),
    30: dict(frames=F1, texts=[T('Number', 'courgette', 374.7, 105.0, 108.1, 190),
                               T('Street', 'courgette', 48.1, 104.2, 133.4, 190)]),
    # --- deco designs: ornaments come from the source PDF ---
    6: dict(bg='#ffffff', square=True, deco=True, texts=[T('Number', 'gilda', 235.0, 100.6, 97.0, 150),
                                                          T('Street', 'gilda', 34.0, 104.0, 117.0, 128)]),
    7: dict(bg='#ffffff', square=True, deco=True, texts=[T('Number', 'courgette', 185.0, 100.0, 92.0, 150),
                                                          T('Street', 'courgette', 30.0, 104.0, 113.5, 148)]),
    8: dict(bg='#ffffff', square=True, deco=True, texts=[T('Number', 'oldstd', 310.4, 101.9, 104.0, 168),
                                                          T('Street', 'oldstd', 36.8, 100.8, 116.5, 137)]),
    9: dict(deco=True, texts=[T('Number', 'oldstd', 228.0, 104.5, 116.7, 150),
                              T('Street', 'oldstd', 41.7, 101.0, 132.0, 165)]),
    10: dict(deco=True, texts=[T('Number', 'oldstd', 281.4, 104.5, 101.1, 160),
                               T('Street', 'oldstd', 56.6, 105.1, 117.4, 150)]),
    11: dict(deco=True, texts=[T('Number', 'delius', 245.0, 103.4, 97.0, 120),
                               T('Street', 'delius', 30.0, 103.4, 117.0, 112)]),
    12: dict(deco=True, texts=[T('Number', 'ribeye', 330.0, 104.3, 103.4, 150),
                               T('Street', 'ribeye', 53.9, 105.0, 131.6, 140)]),
    13: dict(deco=True, texts=[T('Number', 'crimson', 385.4, 105.0, 112.0, 180),
                               T('Street', 'goudy', 71.5, 103.6, 132.3, 170)]),
    25: dict(deco=True, texts=[T('Number', 'ribeye', 330.0, 104.3, 109.6, 150),
                               T('Street', 'ribeye', 58.3, 104.3, 133.2, 140)]),
    31: dict(bg='#ffffff', square=True, deco=True, texts=[T('Number', 'crimson', 318.2, 103.1, 92.2, 110),
                                                          T('Street', 'della', 131.0, 105.0, 136.0, 118, STREET_MC)]),
    32: dict(bg='#ffffff', square=True, deco=True, texts=[T('Number', 'crimson', 318.2, 105.0, 109.3, 120),
                                                          T('Street', 'della', 57.7, 105.0, 23.7, 118, STREET_MC)]),
    33: dict(bg='#ffffff', square=True, deco=True, texts=[T('Number', 'crimson', 196.6, 107.3, 86.5, 80),
                                                          T('Street', 'della', 92.2, 103.2, 140.4, 190, STREET_MC)]),
    34: dict(bg='#ffffff', square=True, deco=True, texts=[T('Number', 'crimson', 244.6, 105.2, 71.7, 120),
                                                          T('Street', 'della', 92.2, 103.2, 140.4, 190, STREET_MC)]),
    35: dict(bg='#ffffff', square=True, deco=True, texts=[T('Number', 'crimson', 281.4, 105.8, 86.6, 120),
                                                          T('Street', 'della', 74.7, 103.3, 116.3, 150, STREET_MC)]),
    36: dict(bg='#ffffff', square=True, deco=True, texts=[T('Number', 'crimson', 281.4, 109.5, 87.6, 120),
                                                          T('Street', 'della', 85.5, 107.4, 140.3, 190, STREET_MC)]),
}


def sku(n):
    return f'FOXY-CUT-PWBSD{n}-01'


def base_name(n):
    return f'Wheelie Bin Sticker Design {n} - {sku(n)} - A5 print file'


def kind(n):
    return 'vector (ornaments from the original)' if DESIGNS[n].get('deco') else 'vector (redrawn)'


# ------------------------------------------------------------------------------------------- geometry
def rrect_path(x0, y0, x1, y1, r):
    """Rounded rectangle as an SVG path (y down)."""
    k = 0.5523 * r
    return (f'M{x0 + r:.3f} {y0:.3f}H{x1 - r:.3f}C{x1 - r + k:.3f} {y0:.3f} {x1:.3f} {y0 + r - k:.3f} {x1:.3f} {y0 + r:.3f}'
            f'V{y1 - r:.3f}C{x1:.3f} {y1 - r + k:.3f} {x1 - r + k:.3f} {y1:.3f} {x1 - r:.3f} {y1:.3f}'
            f'H{x0 + r:.3f}C{x0 + r - k:.3f} {y1:.3f} {x0:.3f} {y1 - r + k:.3f} {x0:.3f} {y1 - r:.3f}'
            f'V{y0 + r:.3f}C{x0:.3f} {y0 + r - k:.3f} {x0 + r - k:.3f} {y0:.3f} {x0 + r:.3f} {y0:.3f}Z')


def house_shapes(n):
    """House icon of designs 5 and 18 (the original is a 512 px bitmap; redrawn as vector). Trim mm, y down.
    Returns (roof polyline, roof stroke width, body path, chimney polygon)."""
    roof = [(14.4, 79.7), (104.2, 16.2), (195.8, 77.2)]
    chimney = [(143.0, 7.9), (173.5, 7.9), (173.5, 62.4), (143.0, 42.0)]
    body = [(34.8, 83.7), (104.2, 35.9), (173.5, 83.7)]
    bottom, width = 140.0, 14.0
    if n == 18:   # same house, 0.89 x, moved up, shorter body (street name underneath)
        k, (ax, ay), (bx, by) = 0.8916, (6.6, -9.3), (18.3, -5.3)
        f = lambda p: ((p[0] - ax) * k + bx, (p[1] - ay) * k + by)
        roof, chimney, body = [f(p) for p in roof], [f(p) for p in chimney], [f(p) for p in body]
        bottom, width = 119.0, width * k
    (lx, ly), (ax_, ay_), (rx, ry) = body
    r = 3.0
    d = (f'M{lx:.2f} {ly:.2f}L{ax_:.2f} {ay_:.2f}L{rx:.2f} {ry:.2f}V{bottom - r:.2f}'
         f'Q{rx:.2f} {bottom:.2f} {rx - r:.2f} {bottom:.2f}H{lx + r:.2f}Q{lx:.2f} {bottom:.2f} {lx:.2f} {bottom - r:.2f}Z')
    return roof, width, d, chimney


# ------------------------------------------------------------------------------------------- ornaments from source
def find_source(src, n):
    for name in (f'{n}.pdf', f'WHEELIE BIN - {n}.pdf'):
        p = Path(src) / name
        if p.exists():
            return p
    raise FileNotFoundError(f'source PDF for design {n} not found in {src}')


def deco_items(src, n):
    """Vector drawings of the owner's PDF (text left out), scaled to A5 trim mm (y down).
    Leaves out the page background (a fill covering the whole page) and white page outlines."""
    import pymupdf
    page = pymupdf.open(find_source(src, n))[0]
    s = 25.4 / 72 * SCALE
    pw, ph = page.rect.width, page.rect.height

    def f(v):
        return ('%.2f' % (v * s)).rstrip('0').rstrip('.')

    def col(c):
        return c and '#%02x%02x%02x' % tuple(round(x * 255) for x in c[:3])

    out = []
    for g in page.get_drawings(extended=True):
        if g['type'] in ('clip', 'group'):   # clipping masks / groups: kept, so hidden parts stay hidden
            d = ''.join(seg for seg in _items_to_d(g.get('items') or [], f)) if g['type'] == 'clip' else ''
            out.append(dict(type=g['type'], level=g.get('level', 0), d=d, evenodd=bool(g.get('even_odd'))))
            continue
        r = g['rect']
        whole = r.width >= pw * 0.95 and r.height >= ph * 0.95
        if whole and (col(g.get('fill')) in ('#ffffff', GREY, None)) and col(g.get('color')) in ('#ffffff', None):
            continue
        d = _items_to_d(g['items'], f)
        if g.get('closePath'):
            d.append('Z')
        out.append(dict(type=g['type'], level=g.get('level', 0), fill=col(g.get('fill')), stroke=col(g.get('color')),
                        width=(g.get('width') or 0) * s, evenodd=bool(g.get('even_odd')), d=''.join(d)))
    return out


def _items_to_d(items, f):
    d, last = [], None
    if True:
        for it in items:
            op = it[0]
            if op == 'l':
                a, b = it[1], it[2]
                if last is None or abs(last.x - a.x) > 1e-3 or abs(last.y - a.y) > 1e-3:
                    d.append(f'M{f(a.x)} {f(a.y)}')
                d.append(f'L{f(b.x)} {f(b.y)}')
                last = b
            elif op == 'c':
                a, c1, c2, b = it[1:5]
                if last is None or abs(last.x - a.x) > 1e-3 or abs(last.y - a.y) > 1e-3:
                    d.append(f'M{f(a.x)} {f(a.y)}')
                d.append('C' + ' '.join(f'{f(q.x)} {f(q.y)}' for q in (c1, c2, b)))
                last = b
            elif op == 're':
                q = it[1]
                d.append(f'M{f(q.x0)} {f(q.y0)}H{f(q.x1)}V{f(q.y1)}H{f(q.x0)}Z')
                last = None
            elif op == 'qu':
                q = it[1]
                d.append(f'M{f(q.ul.x)} {f(q.ul.y)}L{f(q.ur.x)} {f(q.ur.y)}L{f(q.lr.x)} {f(q.lr.y)}L{f(q.ll.x)} {f(q.ll.y)}Z')
                last = None
    return d


# ------------------------------------------------------------------------------------------- text fitting
TOP_GAP = 2.5          # mm kept clear between the tallest glyph and the inner frame (or the trim + safe area)
_YMAX = {}             # font key -> {char: glyph top in em}


def top_limit(D):
    """Highest point (trim mm, y down) any text may reach."""
    frames = D.get('frames') or []
    if frames:
        inset, sw, _r, _p = max(frames)
        return inset + sw / 2 + TOP_GAP
    return D.get('top', BLEED + TOP_GAP)


def fit(t, D=None):
    """Font size (pt): the measured size, shrunk to max_w and so the glyph tops stay below top_limit().
    Returns (size, width_mm)."""
    name = 'F_' + t['font']
    w = pdfmetrics.stringWidth(t['text'], name, t['size']) / MM
    size = t['size'] if w <= t['max_w'] else t['size'] * t['max_w'] / w
    if D is not None:
        ymax = max(_YMAX[t['font']].get(c, 0) for c in t['text'])       # em
        room = t['base'] - top_limit(D)                                  # mm above the baseline
        if ymax > 0 and ymax * size * 25.4 / 72 > room:
            size = room / ymax * 72 / 25.4
    return size, pdfmetrics.stringWidth(t['text'], name, size) / MM


_WORK = {}


def pdf_font(key, text):
    """A font holding only the glyphs this design uses (fontTools subset, no hinting / layout tables),
    registered for the PDF so the embedded font is a few KB. Metrics are identical to the full font."""
    from fontTools import subset
    import hashlib
    chars = ''.join(sorted(set(text)))
    name = f'F_{key}_{hashlib.md5(chars.encode()).hexdigest()[:8]}'
    if name not in pdfmetrics._fonts:
        src = _WORK['dir'] / FONTS[key][0]
        dst = _WORK['dir'] / f'{name}.ttf'
        opt = subset.Options()
        opt.layout_features = []
        opt.hinting = False
        opt.name_IDs = [0, 1, 2, 3, 4, 5, 6]
        opt.notdef_outline = True
        f = subset.load_font(str(src), opt)
        sub = subset.Subsetter(opt)
        sub.populate(text=chars)
        sub.subset(f)
        subset.save_font(f, str(dst), opt)
        # registerFont() would reuse the full font already registered under the same face name
        # (e.g. "PTSans-Regular"), so put the subset in the registry directly; the face name is kept
        # so Illustrator still recognises the installed font.
        pdfmetrics._fonts[name] = TTFont(name, str(dst))
    return name


def register_fonts(font_dir, work_dir):
    """Register each TTF with its hinting removed (hinting is screen-only; it made the embedded subsets 3x bigger)."""
    from fontTools.ttLib import TTFont as FT
    from fontTools.pens.boundsPen import BoundsPen
    work = Path(work_dir) / '_fonts_unhinted'
    work.mkdir(parents=True, exist_ok=True)
    _WORK['dir'] = work
    for key, (ttf, *_rest) in FONTS.items():
        f = FT(str(Path(font_dir) / ttf))
        gs, upm, cmap = f.getGlyphSet(), f['head'].unitsPerEm, f.getBestCmap()
        tops = {}
        for c in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
            if ord(c) in cmap:
                pen = BoundsPen(gs)
                gs[cmap[ord(c)]].draw(pen)
                tops[c] = (pen.bounds[3] / upm) if pen.bounds else 0
        _YMAX[key] = tops
        for tag in ('fpgm', 'prep', 'cvt ', 'hdmx', 'VDMX', 'LTSH', 'DSIG', 'gasp'):
            if tag in f:
                del f[tag]
        if 'glyf' in f:
            for g in f['glyf'].glyphs.values():
                if hasattr(g, 'program'):
                    g.program.fromBytecode(b'')
        f.save(str(work / ttf))
        pdfmetrics.registerFont(TTFont('F_' + key, str(work / ttf)))


# ------------------------------------------------------------------------------------------- SVG
def svg(n, deco):
    D = DESIGNS[n]
    bg = D.get('bg', GREY)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
         f'width="{PAGE_W}mm" height="{PAGE_H}mm" viewBox="0 0 {PAGE_W} {PAGE_H}">',
         f'<title>Personalised Wheelie Bin Sticker - Design {n} - {sku(n)} - A5 210x148 mm + 3 mm bleed</title>',
         '<g id="Artwork" inkscape:groupmode="layer" inkscape:label="Artwork">',
         f'<rect id="Background_bleed" x="0" y="0" width="{PAGE_W}" height="{PAGE_H}" fill="{bg}"/>',
         f'<g id="Design" transform="translate({BLEED} {BLEED})">']
    for inset, sw, r, panel in D.get('frames', []):
        o.append(f'<path d="{rrect_path(inset, inset, TRIM_W - inset, TRIM_H - inset, r)}" '
                 f'fill="{"#ffffff" if panel else "none"}" stroke="{FRAME}" stroke-width="{sw}"/>')
    if D.get('house'):
        roof, rw, body, chim = house_shapes(D['house'])
        o.append(f'<g id="House" fill="{FRAME}">')
        o.append('<polygon points="' + ' '.join(f'{x:.2f},{y:.2f}' for x, y in chim) + '"/>')
        o.append('<polyline points="' + ' '.join(f'{x:.2f},{y:.2f}' for x, y in roof) +
                 f'" fill="none" stroke="{FRAME}" stroke-width="{rw:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(f'<path d="{body}"/></g>')
    if deco:
        o.append('<g id="Ornaments">')
        stack, nclip = [], 0
        for it in deco:
            while stack and stack[-1] >= it.get('level', 0):
                stack.pop()
                o.append('</g>')
            if it['type'] == 'clip':
                nclip += 1
                rule = ' clip-rule="evenodd"' if it['evenodd'] else ''
                o.append(f'<clipPath id="clip{nclip}"><path d="{it["d"]}"{rule}/></clipPath><g clip-path="url(#clip{nclip})">')
                stack.append(it['level'])
                continue
            if it['type'] == 'group':
                o.append('<g>')
                stack.append(it['level'])
                continue
            fill = it['fill'] if it['type'] in ('f', 'fs') and it['fill'] else 'none'
            st = (f' stroke="{it["stroke"]}" stroke-width="{it["width"]:.3f}"'
                  if it['type'] in ('s', 'fs') and it['stroke'] else '')
            rule = ' fill-rule="evenodd"' if it['evenodd'] else ''
            o.append(f'<path d="{it["d"]}" fill="{fill}"{st}{rule}/>')
        o.extend('</g>' for _ in stack)
        o.append('</g>')
    o.append('<g id="Personalisation">')
    for t in D['texts']:
        size, _ = fit(t, D)
        _f, family, weight, style = FONTS[t['font']]
        o.append(f'<text id="{t["role"].replace(" ", "_")}" x="{t["cx"]:.2f}" y="{t["base"]:.2f}" text-anchor="middle" '
                 f'font-family="{family}" font-weight="{weight}" font-style="{style}" '
                 f'font-size="{size * 25.4 / 72:.2f}" fill="{t["fill"]}">{t["text"]}</text>')
    o.append('</g></g></g>')
    r = 0 if D.get('square') else CUT_R
    o.append('<g id="CUT" inkscape:groupmode="layer" inkscape:label="CUT">')
    o.append(f'<path d="{rrect_path(BLEED, BLEED, BLEED + TRIM_W, BLEED + TRIM_H, r) if r else f"M{BLEED} {BLEED}H{BLEED + TRIM_W}V{BLEED + TRIM_H}H{BLEED}Z"}" '
             f'fill="none" stroke="#FF0000" stroke-width="0.25"/>')
    o.append('</g></svg>')
    return '\n'.join(o) + '\n'


# ------------------------------------------------------------------------------------------- PDF
TOK = re.compile(r'[MLCHVQZ]|-?\d*\.?\d+')


def draw_svg_path(cv, d, ox, oy):
    """Draw an SVG path (M L C H V Q Z, absolute, mm, y down) into a reportlab path."""
    P = lambda x, y: ((ox + x) * MM, (PAGE_H - (oy + y)) * MM)
    p = cv.beginPath()
    toks = TOK.findall(d)
    i, cmd, cur = 0, None, (0.0, 0.0)
    while i < len(toks):
        if toks[i] in 'MLCHVQZ':
            cmd = toks[i]
            i += 1
            if cmd == 'Z':
                p.close()
                continue
        nums = lambda k: [float(v) for v in toks[i:i + k]]
        if cmd == 'M':
            x, y = nums(2); p.moveTo(*P(x, y)); cur = (x, y); i += 2; cmd = 'L'
        elif cmd == 'L':
            x, y = nums(2); p.lineTo(*P(x, y)); cur = (x, y); i += 2
        elif cmd == 'H':
            x, = nums(1); p.lineTo(*P(x, cur[1])); cur = (x, cur[1]); i += 1
        elif cmd == 'V':
            y, = nums(1); p.lineTo(*P(cur[0], y)); cur = (cur[0], y); i += 1
        elif cmd == 'C':
            a = nums(6); p.curveTo(*P(a[0], a[1]), *P(a[2], a[3]), *P(a[4], a[5])); cur = (a[4], a[5]); i += 6
        elif cmd == 'Q':
            qx, qy, x, y = nums(4)
            c1 = (cur[0] + 2 / 3 * (qx - cur[0]), cur[1] + 2 / 3 * (qy - cur[1]))
            c2 = (x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y))
            p.curveTo(*P(*c1), *P(*c2), *P(x, y)); cur = (x, y); i += 4
        else:
            raise ValueError(f'unexpected path data near {toks[i]}')
    return p


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def pdf(n, deco, path):
    D = DESIGNS[n]
    cv = canvas.Canvas(str(path), pagesize=(PAGE_W * MM, PAGE_H * MM), pageCompression=1,
                       initialFontName=pdf_font(D['texts'][0]['font'], ''.join(u['text'] for u in D['texts'] if u['font'] == D['texts'][0]['font'])))
    cv.setTitle(f'Personalised Wheelie Bin Sticker - Design {n} - {sku(n)}')
    cv.setAuthor('Foxy Printing')
    cv.setSubject('A5 210 x 148 mm + 3 mm bleed; layers Artwork / CUT (red 0.25 mm)')
    cv._code.append('/OC /Artwork BDC')
    cv.setFillColorRGB(*hexrgb(D.get('bg', GREY)))
    cv.rect(0, 0, PAGE_W * MM, PAGE_H * MM, stroke=0, fill=1)
    for inset, sw, r, panel in D.get('frames', []):
        cv.setLineWidth(sw * MM)
        cv.setStrokeColorRGB(*hexrgb(FRAME))
        cv.setFillColorRGB(1, 1, 1)
        cv.drawPath(draw_svg_path(cv, rrect_path(inset, inset, TRIM_W - inset, TRIM_H - inset, r), BLEED, BLEED),
                    stroke=1, fill=1 if panel else 0)
    if D.get('house'):
        roof, rw, body, chim = house_shapes(D['house'])
        cv.setFillColorRGB(*hexrgb(FRAME))
        cv.setStrokeColorRGB(*hexrgb(FRAME))
        cv.drawPath(draw_svg_path(cv, 'M' + 'L'.join(f'{x} {y}' for x, y in chim) + 'Z', BLEED, BLEED), stroke=0, fill=1)
        cv.setLineWidth(rw * MM); cv.setLineCap(1); cv.setLineJoin(1)
        cv.drawPath(draw_svg_path(cv, 'M' + 'L'.join(f'{x} {y}' for x, y in roof), BLEED, BLEED), stroke=1, fill=0)
        cv.drawPath(draw_svg_path(cv, body, BLEED, BLEED), stroke=0, fill=1)
        cv.setLineCap(0); cv.setLineJoin(0)
    if deco:
        cv.saveState()
        clip = cv.beginPath(); clip.rect(0, 0, PAGE_W * MM, PAGE_H * MM)
        cv.clipPath(clip, stroke=0, fill=0)
        stack = []
        for it in deco:
            while stack and stack[-1] >= it.get('level', 0):
                stack.pop()
                cv.restoreState()
            if it['type'] in ('clip', 'group'):
                cv.saveState()
                stack.append(it['level'])
                if it['type'] == 'clip' and it['d']:
                    cv.clipPath(draw_svg_path(cv, it['d'], BLEED, BLEED), stroke=0, fill=0,
                                fillMode=1 if it['evenodd'] else 0)
                continue
            do_fill = it['type'] in ('f', 'fs') and it['fill']
            do_stroke = it['type'] in ('s', 'fs') and it['stroke']
            if do_fill:
                cv.setFillColorRGB(*hexrgb(it['fill']))
            if do_stroke:
                cv.setStrokeColorRGB(*hexrgb(it['stroke'])); cv.setLineWidth(it['width'] * MM)
            cv.drawPath(draw_svg_path(cv, it['d'], BLEED, BLEED), stroke=1 if do_stroke else 0,
                        fill=1 if do_fill else 0, fillMode=1 if it['evenodd'] else 0)
        for _ in stack:
            cv.restoreState()
        cv.restoreState()
    for t in D['texts']:
        size, _ = fit(t, D)
        cv.setFillColorRGB(*hexrgb(t['fill']))
        used = ''.join(u['text'] for u in D['texts'] if u['font'] == t['font'])
        cv.setFont(pdf_font(t['font'], used), size)
        cv.drawCentredString((BLEED + t['cx']) * MM, (PAGE_H - BLEED - t['base']) * MM, t['text'])
    cv._code.append('EMC')
    cv._code.append('/OC /CUT BDC')
    cv.setLineWidth(0.25 * MM)
    cv.setStrokeColorRGB(1, 0, 0)
    r = 0 if D.get('square') else CUT_R
    cv.roundRect(BLEED * MM, BLEED * MM, TRIM_W * MM, TRIM_H * MM, r * MM, stroke=1, fill=0) if r else \
        cv.rect(BLEED * MM, BLEED * MM, TRIM_W * MM, TRIM_H * MM, stroke=1, fill=0)
    cv._code.append('EMC')
    cv.showPage()
    cv.save()
    add_layers_ascii(path)


def add_layers_ascii(path):
    """Register the Artwork / CUT layers, keep every stream ASCII85, and make the whole file plain ASCII."""
    import pikepdf
    with pikepdf.open(path, allow_overwriting_input=True) as doc:
        ocgs = {k: doc.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.OCG, Name=k)) for k in ('Artwork', 'CUT')}
        order = pikepdf.Array([ocgs['Artwork'], ocgs['CUT']])
        doc.Root.OCProperties = pikepdf.Dictionary(OCGs=order, D=pikepdf.Dictionary(Order=order, ON=order, Name='Layers'))
        for page in doc.pages:
            page.obj.Resources.Properties = pikepdf.Dictionary({'/Artwork': ocgs['Artwork'], '/CUT': ocgs['CUT']})
        # ReportLab leaves some font streams (ToUnicode, widths) as plain Flate: wrap them in ASCII85 too
        import base64
        for obj in doc.objects:
            if isinstance(obj, pikepdf.Stream):
                raw = obj.read_raw_bytes()
                if all(b < 128 for b in raw):
                    continue
                filt = obj.get('/Filter')
                filters = [] if filt is None else (list(filt) if isinstance(filt, pikepdf.Array) else [filt])
                parms = obj.get('/DecodeParms')
                obj.write(base64.a85encode(raw, wrapcol=76) + b'~>',
                          filter=pikepdf.Array([pikepdf.Name.ASCII85Decode] + filters),
                          decode_parms=None if parms is None else pikepdf.Array([pikepdf.Null()] + (list(parms) if isinstance(parms, pikepdf.Array) else [parms])))
        doc.save(path, compress_streams=False, stream_decode_level=pikepdf.StreamDecodeLevel.none,
                 object_stream_mode=pikepdf.ObjectStreamMode.disable, deterministic_id=True)
    data = bytearray(Path(path).read_bytes())
    for i, b in enumerate(data[:64]):
        if b > 127:
            data[i] = ord('~')
    assert all(b < 128 for b in data), 'PDF is not plain ASCII'
    Path(path).write_bytes(bytes(data))


def check_png(pdf_path, png_path):
    import pymupdf
    pymupdf.open(pdf_path)[0].get_pixmap(dpi=60).save(png_path)


# ------------------------------------------------------------------------------------------- folder text files
FONTS_ZIP = 'https://cdn.shopify.com/s/files/1/1774/9115/files/Wheelie-Bin-Sticker-fonts-OFL.zip?v=1791280736'
GENERATOR_ZIP = 'https://cdn.shopify.com/s/files/1/1774/9115/files/Wheelie-Bin-Sticker-artwork-generator.zip?v=1791280736'
DROPBOX_ROOT = '/AI DESIGNS 2026'


def folder_name(n):
    return f'Personalised Wheelie Bin Sticker – Design {n} - {sku(n)}'


def fonts_txt():
    users = {}
    for n, D in sorted(DESIGNS.items()):
        for t in D['texts']:
            users.setdefault(t['font'], set()).add(n)
    L = ['FONTS - Personalised Wheelie Bin Stickers (Designs 1-36)', '=' * 56, '',
         'All fonts are free, open-licence Google Fonts (SIL Open Font Licence 1.1, see OFL.txt).',
         'They stand in for the system fonts in the original artwork, which we cannot share.',
         'Install them (double-click each .ttf > Install) BEFORE opening the .svg / .pdf in Illustrator,',
         'so the house number and street name stay live, editable text.', '',
         'Download all 21 fonts + licences in one zip (Shopify Files):', FONTS_ZIP, '',
         'Font (file)  |  Google Fonts page  |  replaces  |  used in designs', '-' * 56]
    for key, (ttf, fam, *_r) in FONTS.items():
        name = fam.split(',')[0].strip(" '")
        url = 'https://fonts.google.com/specimen/' + name.replace(' ', '+')
        L.append(f'{name} ({ttf})  |  {url}  |  {ORIGINAL_FONT[key]}  |  '
                 + ', '.join(str(n) for n in sorted(users.get(key, []))))
    return '\n'.join(L) + '\n'


def ofl_txt(font_dir):
    L = ['Licences for the fonts in this folder', '', 'Each font below is licensed under the SIL Open Font',
         'License, Version 1.1 (full text after the copyright notices).', '']
    body = None
    for key, (ttf, fam, *_r) in FONTS.items():
        name = fam.split(',')[0].strip(" '")
        folder = name.lower().replace(' ', '')
        src = Path(font_dir) / f'OFL-{folder}.txt'
        txt = src.read_text(encoding='utf-8-sig')
        head, _sep, _rest = txt.partition('This Font Software is licensed')
        L += [f'{name}:', head.strip(), '']
        if body is None and 'SIL OPEN FONT LICENSE Version 1.1' in txt:
            body = txt[txt.index('-' * 59 if '-' * 59 in txt else 'SIL OPEN FONT LICENSE'):]
    L += ['This Font Software is licensed under the SIL Open Font License, Version 1.1.',
          'This license is copied below, and is also available with a FAQ at: https://openfontlicense.org', '',
          body.strip()]
    return '\n'.join(L) + '\n'


README = """README - how to print and cut (Personalised Wheelie Bin Sticker)
=================================================================

WHAT IS IN THIS FOLDER
- "WHEELIE BIN - N.pdf" / ".ai": your original design files (copied from
  "!! BEN JOE OWEN NEW PRODUCTS XMAS 2026 !!!/WHEELIE BIN STICKERS - Copy/ARTWORK").
  Design 2's original shows a customer proof "39 Carnaughton Place"; the shop sample is
  "74 Make Believe Close".
- "Wheelie Bin Sticker Design N - FOXY-CUT-PWBSDN-01 - A5 print file.svg / .pdf": the new,
  editable print file (Designs 1-5, 14-24 and 26-30). Designs 6-13, 25 and 31-36: see
  "PRINT FILE - HOW TO BUILD (ornate designs).txt".
- Fonts/: the open-licence fonts list (FONTS - DOWNLOAD LINK.txt) and their licences (OFL.txt).

SIZE
- Sticker (trim): A5 landscape, 210 x 148 mm. Page: 216 x 154 mm (3 mm bleed all round).
- Safe area: keep text 3 mm inside the trim. Background colour runs to the bleed edge.
- Material: laminated outdoor vinyl (lasts 5+ years outside).
- Corners: rounded 3 mm where the original sticker has rounded corners, square otherwise
  (6, 7, 8, 31-36). The CUT line shows which.

LAYERS
- Artwork: background, frames/ornaments, and the LIVE text objects "Number" and "Street"
  (sample "74" and "MAKE BELIEVE CLOSE"). Design 19 has the street on two lines.
- CUT: one red line (RGB 255,0,0 / CMYK 2,98,95,0), 0.25 mm, no fill, closed path on the trim.
  It never prints. In ColorCut Pro map Red = Cut.

EDITING AN ORDER
1. Install the fonts (Fonts/FONTS - DOWNLOAD LINK.txt) first.
2. Open the .svg (or .pdf) in Illustrator. Top-level groups "Artwork" and "CUT" are the layers.
3. Type the customer's house number and street name into the Number / Street text.
   Long street names: reduce the font size (or horizontal scale to no less than 85%)
   so the text stays inside the frame and the 3 mm safe area.
4. Save as .ai in the order folder.

PRINTING AND CUTTING (Intec ColorCut)
1. Run "Foxy - 1 Prepare cut file" from /AI DESIGNS 2026/00 Foxy Illustrator Scripts - ColorCut/
   (it puts the red line on the CUT layer). It swaps the sample name "Ava"; for these stickers
   change the Number / Street text by hand (step 3 above).
2. Place the sticker on your print sheet. One A5 sticker with bleed fits an A4 landscape sheet
   with the 12 mm (left) / 10 mm (other edges) clear margins the PageMARKs need.
3. Add PageMARKs & BarCode with the ColorCut Pro plug-in (File > Add PageMARKs and BarCode),
   or for a whole folder use "Foxy - 3 Batch barcodes". One job number per design.
4. "Foxy - 2 Save print PDF" saves the .ai and a "- PRINT.pdf" without the cut line.
5. Print on outdoor vinyl, then laminate (outdoor laminate) BEFORE cutting.
6. On the ColorCut: scan the barcode, check Red = Cut, and test-cut the first sheet.

Made by the generator foxyprinting-rebrand/tools/artwork/wheelie_bin_stickers.py
(Foxy Printing repo, branch claude/foxyprinting-rebrand-shopify-usf2x9).
"""

ORNATE_NOTE = """PRINT FILE - HOW TO BUILD (ornate designs 6-13, 25, 31-36)
==========================================================

The new print files for this design are rebuilt from the ornaments in your original PDF,
so they are 100% vector (the original scrolls, wreaths and vines) with the house number and
street name as live text. They were made and checked on 6 Oct 2026, but could not be saved
here automatically. To make them on any PC with Python 3:

1. Get the generator foxyprinting-rebrand/tools/artwork/wheelie_bin_stickers.py from the
   repo (branch claude/foxyprinting-rebrand-shopify-usf2x9). Use the repo version: the
   earlier copy in Shopify Files (Wheelie-Bin-Sticker-artwork-generator.zip) does not handle
   the clipping masks in Designs 31 and 32.
   Fonts: """ + FONTS_ZIP + """ (unzip into a folder "fonts").
2. Put the original "WHEELIE BIN - N.pdf" files in a folder "src".
3. pip install reportlab pikepdf pymupdf fonttools
4. python wheelie_bin_stickers.py --fonts fonts --src src --out out --designs 6-13,25,31-36
5. "out" then holds, per design, "<name>.svg", "<name>.pdf" (layers Artwork + CUT) and a
   "- check.png" preview. Save them into this folder.

Until then, the original "WHEELIE BIN - N.ai" in this folder is the editable artwork:
it is A4 (297 x 210 mm), so scale it to 70.71% for the A5 sticker and add 3 mm bleed
and the red CUT line (see README).
"""


def write_texts(out, font_dir):
    out = Path(out)
    (out / 'README - how to print and cut.txt').write_text(README)
    (out / 'FONTS - DOWNLOAD LINK.txt').write_text(fonts_txt())
    (out / 'OFL.txt').write_text(ofl_txt(font_dir))
    (out / 'PRINT FILE - HOW TO BUILD (ornate designs).txt').write_text(ORNATE_NOTE)


def parse_designs(spec):
    out = []
    for part in spec.split(','):
        a, _, b = part.partition('-')
        out += list(range(int(a), int(b or a) + 1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fonts', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--src')
    ap.add_argument('--designs', default='1-36')
    ap.add_argument('--no-png', action='store_true')
    ap.add_argument('--texts', action='store_true', help='also write README / FONTS / OFL text files')
    a = ap.parse_args()
    register_fonts(a.fonts, a.out)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.texts:
        write_texts(out, a.fonts)
    for n in parse_designs(a.designs):
        D = DESIGNS[n]
        if D.get('deco') and not a.src:
            print(f'{n}: skipped (needs --src for the ornaments)')
            continue
        deco = deco_items(a.src, n) if D.get('deco') else None
        b = out / base_name(n)
        Path(f'{b}.svg').write_text(svg(n, deco))
        pdf(n, deco, f'{b}.pdf')
        if not a.no_png:
            check_png(f'{b}.pdf', f'{b} - check.png')
        fits = ', '.join(f'{t["role"]} {fit(t, D)[0]:.0f}pt' for t in D['texts'])
        print(f'{n}: {kind(n)}; svg {Path(f"{b}.svg").stat().st_size // 1024} KB, '
              f'pdf {Path(f"{b}.pdf").stat().st_size // 1024} KB; {fits}')


if __name__ == '__main__':
    sys.exit(main())
