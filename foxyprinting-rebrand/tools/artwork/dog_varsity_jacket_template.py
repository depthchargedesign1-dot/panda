"""Editable, print-ready name + number transfer templates for the Personalised Dog Varsity Jacket
(Portman & Pooch PP005 blank from Ralawise; never name the blank maker to customers).

Usage:
    python3 tools/artwork/dog_varsity_jacket_template.py --out exports/pets/2026-10-08-dog-varsity-jacket/artwork

One template per size. Print areas are Ralawise's own figures for PP005 (shop.ralawise.com, "PrintArea",
read 8 Oct 2026), given as L x W (length along the dog's back x width across it):
    XS 10x10 cm, S 14x14, M 19x16.5, L 20x18, XL 23x18, 2XL 24x19.  3XL and 4XL: not given (ASK) - the 2XL
    area is used for them until the owner confirms.
The transfer reads across the back (width = horizontal, length = vertical, top = neck end).

Customer fields (foxy.personalise_fields): "Dog's name (optional)" and "Number (optional)" (max 3 characters).
Writes per size: SVG (layers Artwork, Text, CUT, Guides) + ASCII PDF (real layers) + 300 dpi preview PNG,
plus README.txt and Fonts/ (download links + OFL licence). Drawing/PDF code is shared with hat_badge_template.py.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

if os.environ.get('PYTHONHASHSEED') != '0':
    os.execvpe(sys.executable, [sys.executable] + sys.argv, {**os.environ, 'PYTHONHASHSEED': '0'})
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hat_badge_template as hb  # noqa: E402

TODAY = '8 Oct 2026'
SKU = 'FOXY-PP005-BLA-XS'
SHORT = 'Personalised Dog Varsity Jacket'
# size: (width mm across the back, length mm along the back, confirmed?)
SIZES = [  # 3XL/4XL rows only feed the README; no separate files (they use the 2XL file)
    ('XS', 100, 100, True), ('S', 140, 140, True), ('M', 165, 190, True), ('L', 180, 200, True),
    ('XL', 180, 230, True), ('2XL', 190, 240, True), ('3XL', 190, 240, False), ('4XL', 190, 240, False),
]
INK = (0, 0, 0, 100)        # placeholder colour: change to the customer's chosen text colour (white on Black/Navy)
SHOPIFY_FONT = 'https://cdn.shopify.com/s/files/1/1774/9115/files/BebasNeue-Regular.ttf?v=1791283074'


def jacket_doc(tw, th):
    hb.TRIM_W, hb.TRIM_H = float(tw), float(th)   # used by write_pdf for the TrimBox
    B, S = hb.BLEED, hb.SAFE
    W, H = tw + 2 * B, th + 2 * B
    d = hb.Doc(W, H)
    cx = W / 2
    sw_, sh_ = tw - 2 * S, th - 2 * S
    # Name in the top part of the safe area, number underneath (about 2x the name height)
    name = 'BUSTER'
    name_pt = hb.fit_size(name, 'bebas', sw_ * 0.9, (sh_ * 0.26) / hb.PT / 0.7)
    name_cap = name_pt * hb.PT * 0.7
    num = '7'
    num_pt = (sh_ * 0.52) / hb.PT / 0.7
    num_pt = min(num_pt, hb.fit_size('88', 'bebas', sw_ * 0.6, num_pt))
    num_cap = num_pt * hb.PT * 0.7
    top = B + S + (sh_ - (name_cap + sh_ * 0.08 + num_cap)) / 2   # centre the name + number block
    d.add('Text', hb.text(cx, top + name_cap, name, 'bebas', name_pt, INK, id_='Dogs_name'))
    d.add('Text', hb.text(cx, top + name_cap + sh_ * 0.08 + num_cap, num, 'bebas', num_pt, INK, id_='Number'))
    d.add('CUT', hb.rect(B, B, tw, th, rgb_stroke=(255, 0, 0), sw=hb.CUT_W_PT * hb.PT))
    d.add('Guides', hb.rect(0.15, 0.15, W - 0.3, H - 0.3, stroke=hb.GUIDE_BLEED, sw=0.2, dash=(1, 0.7)))
    d.add('Guides', hb.rect(B + S, B + S, sw_, sh_, stroke=hb.GUIDE_SAFE, sw=0.2, dash=(1, 0.7)))
    d.add('Guides', hb.text(cx, 2.1, 'NECK END - BLEED 3 mm', 'barlow-sb', 4.5, hb.GUIDE_TEXT))
    d.add('Guides', hb.text(cx, H - 0.8, 'TRIM %g x %g mm  |  SAFE 3 mm' % (tw, th), 'barlow-sb', 4.5, hb.GUIDE_TEXT))
    return d


def fonts_txt():
    return f"""FONTS USED IN THESE TEMPLATES (free, SIL Open Font License 1.1 - see OFL.txt)

- Bebas Neue (BebasNeue-Regular.ttf, weight 400) - name and number
  Google Fonts page: https://fonts.google.com/specimen/Bebas+Neue
  Direct .ttf download: https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf
  Shopify Files copy: {SHOPIFY_FONT}
  Copyright 2019 The Bebas Neue Project Authors (https://github.com/dharmatype/Bebas-Neue)

- Barlow Condensed SemiBold (guide labels only, hidden layer, never prints)
  https://fonts.google.com/specimen/Barlow+Condensed

Install Bebas Neue before opening the SVG/PDF in Illustrator, otherwise the live text is substituted.
"""


def readme(rows):
    lines = '\n'.join(f'  {s:<4} {w:g} x {h:g} mm (width x length){"" if ok else "   ASK - Ralawise gives no print area; 2XL used"}'
                      for s, w, h, ok in rows)
    return f"""{SHORT} - {SKU}
Print-ready, editable name + number transfer templates, made {TODAY}. One file per jacket size.
Product: https://foxyprinting.co.uk/products/personalised-dog-varsity-jacket
SKUs FOXY-PP005-<BLA|NAV|PIN>-<size> (Black, Navy, Pink; 3XL/4XL Black only from the supplier).

PERSONALISATION (both optional - a jacket can be ordered plain)
- "Dog's name (optional)" and "Number (optional)" (up to 3 characters). The customer also picks a font and a
  text colour on the website (order line properties "Font" and "Text colour"): use them; the template default
  is Bebas Neue in K100 as a placeholder. On Black and Navy jackets white usually reads best.
- If only a name is given, delete the number and move the name down to the middle; if only a number, delete the
  name and centre the number.

PRINT AREA (trim) - Ralawise PP005 figures (L x W), read 8 Oct 2026
{lines}
- Bleed 3 mm on every edge; safe area 3 mm inside the trim. The name/number has no background, so the bleed is
  only there for the film trim line.
- Placement: centred on the back, reading across the back, top of the text towards the neck. Exact distance from
  the collar: ASK.

LAYERS
- Artwork: empty (no background on this design).
- Text: live, editable "BUSTER" (id Dogs_name) and "7" (id Number) in Bebas Neue.
- CUT: red RGB 255,0,0, 0.25 pt, no fill, on the trim line - for trimming the transfer film, never prints.
- Guides (hidden, non-printing): green dashed = bleed edge, magenta dashed = safe area.

PRINT AND PRESS - ASK
- Transfer method (DTF or vinyl), whether the RIP needs a mirrored file (these are unmirrored), and press
  settings. The supplier care label says "do not iron", so test-press one jacket first at a low temperature.

FILES
- Dog varsity jacket name and number - <size> <W>x<L>mm.svg : editable artwork, layers Artwork / Text / CUT / Guides.
  (3XL and 4XL use the 2XL file until the owner confirms their print area.)
- The matching PDFs (real layers, TrimBox and BleedBox set) are in Shopify Files: links in
  "PDF - DOWNLOAD LINKS.txt" in this folder.
- Fonts/FONTS - DOWNLOAD LINK.txt and Fonts/OFL.txt.
- 100 dpi PNG previews are kept in the website repo (Dropbox here only takes text files):
  foxyprinting-rebrand/exports/pets/2026-10-08-dog-varsity-jacket/artwork/

Regenerate: python3 tools/artwork/dog_varsity_jacket_template.py --out <folder>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    out = Path(a.out)
    (out / 'Fonts').mkdir(parents=True, exist_ok=True)
    for size, w, h, ok in SIZES:
        if not ok:
            continue
        doc = jacket_doc(w, h)
        name = f'Dog varsity jacket name and number - {size} {w:g}x{h:g}mm'
        title = f'Dog varsity jacket name + number transfer, size {size}, {w:g}x{h:g}mm - FOXY-PP005'
        hb.write_svg(doc, out / f'{name}.svg', title)
        hb.write_pdf(doc, out / f'{name}.pdf', title, guides_on=False)
        prev = out / '_preview.pdf'
        hb.write_pdf(doc, prev, title, guides_on=True)
        subprocess.run(['pdftoppm', '-r', '100', '-png', '-singlefile', str(prev), str(out / f'{name} - preview')], check=True)
        prev.unlink()
        print(name)
    (out / 'README.txt').write_text(readme(SIZES), encoding='utf-8')
    (out / 'Fonts' / 'FONTS - DOWNLOAD LINK.txt').write_text(fonts_txt(), encoding='utf-8')
    (out / 'Fonts' / 'OFL.txt').write_text(hb.ofl_txt(), encoding='utf-8')


if __name__ == '__main__':
    main()
