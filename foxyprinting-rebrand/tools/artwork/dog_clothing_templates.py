"""Editable, print-ready name (+ optional number) transfer templates for the Portman & Pooch dog clothing range
(PP001 raglan tee, PP002 hoodie, PP003 denim, PP004 puffer, PP006 parka, PP008 football shirt).
The varsity jacket (PP005) has its own script: dog_varsity_jacket_template.py.

Usage:
    python3 tools/artwork/dog_clothing_templates.py --out exports/pets/2026-10-08-dog-clothing-upgrade/artwork

Print areas are Ralawise's "PrintArea" figures (L x W, read 8 Oct 2026), stored here as (width across the back,
length along the back) in mm. Sizes that share an area share one file. 3XL/4XL areas are not given by Ralawise
(ASK); the 2XL area is used. PP008 has no published print area at all (ASK); the PP001 tee areas are used.
Writes SVG (layers Artwork, Text, CUT, Guides) + ASCII PDF (real layers) + 100 dpi preview PNG per area,
plus README.txt and Fonts/ per product. Drawing/PDF code is shared with hat_badge_template.py.
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
import dog_varsity_jacket_template as dv  # noqa: E402  (fonts text, Shopify font link)

TODAY = '8 Oct 2026'
INK = (0, 0, 0, 100)
TEE = [('XS', 100, 100), ('S', 100, 150), ('M', 150, 180), ('L-XL-2XL-3XL-4XL', 180, 230)]
PRODUCTS = {
    'PP001': dict(short='Personalised Dog Raglan T-Shirt', sku='FOXY-PP001-BW-XS', handle='personalised-dog-raglan-t-shirt',
                  number=True, areas=TEE, ask_area=False, sample=('BELLA', '3')),
    'PP002': dict(short='Personalised Dog Fleece Hoodie', sku='FOXY-PP002-BLA-XS', handle='personalised-dog-fleece-hoodie',
                  number=True, areas=TEE, ask_area=False, sample=('TEDDY', '5')),
    'PP003': dict(short='Personalised Dog Denim Jacket', sku='FOXY-PP003-IND-XS', handle='personalised-dog-denim-jacket',
                  number=False, areas=[('XS', 90, 90), ('S', 100, 140), ('M', 115, 180), ('L', 130, 200), ('XL-2XL-3XL-4XL', 180, 230)],
                  ask_area=False, sample=('LUNA', None)),
    'PP004': dict(short='Personalised Dog Puffer Jacket', sku='FOXY-PP004-BLA-XS', handle='personalised-dog-puffer-jacket',
                  number=False, areas=[('XS', 100, 25), ('S', 100, 40), ('M', 150, 40), ('L-XL', 180, 60), ('2XL-3XL-4XL', 190, 80)],
                  ask_area=False, sample=('BEAR', None)),
    'PP006': dict(short='Personalised Dog Parka Jacket', sku='FOXY-PP006-KHA-XS', handle='personalised-dog-parka-jacket',
                  number=False, areas=[('XS', 100, 100), ('S', 130, 130), ('M', 130, 200), ('L', 140, 230), ('XL-2XL-3XL-4XL', 180, 230)],
                  ask_area=False, sample=('MAX', None)),
    'PP008': dict(short='Personalised Dog Football Shirt', sku='FOXY-PP008-WRN-XS', handle='personalised-dog-football-t-shirt',
                  number=True, areas=TEE, ask_area=True, sample=('OLLIE', '10')),
}
RALAWISE_AREA_TEXT = {
    'PP001': 'XS L10xW10cm, S L15xW10, M L18xW15, L/XL/2XL L23xW18',
    'PP002': 'XS L10xW10cm, S L15xW10, M L18xW15, L/XL/2XL L23xW18',
    'PP003': 'XS L9xW9cm, S L14xW10, M L18xW11.5, L L20xW13, XL/2XL L23xW18',
    'PP004': 'XS L2.5xW10cm, S L4xW10, M L4xW15, L/XL L6xW18, 2XL L8xW19 (narrow decoration panel with a concealed platen sheath)',
    'PP006': 'XS L10xW10cm, S L13xW13, M L20xW13, L L23xW14, XL/2XL L23xW18',
    'PP008': 'not published by Ralawise (ASK) - the PP001 raglan tee areas are used as a placeholder',
}


def doc_for(tw, th, name, number):
    hb.TRIM_W, hb.TRIM_H = float(tw), float(th)
    B, S = hb.BLEED, hb.SAFE
    W, H = tw + 2 * B, th + 2 * B
    d = hb.Doc(W, H)
    cx = W / 2
    sw_, sh_ = tw - 2 * S, th - 2 * S
    if number:
        name_pt = hb.fit_size(name, 'bebas', sw_ * 0.9, (sh_ * 0.26) / hb.PT / 0.7)
        name_cap = name_pt * hb.PT * 0.7
        num_pt = (sh_ * 0.52) / hb.PT / 0.7
        num_pt = min(num_pt, hb.fit_size('88', 'bebas', sw_ * 0.6, num_pt))
        num_cap = num_pt * hb.PT * 0.7
        top = B + S + (sh_ - (name_cap + sh_ * 0.08 + num_cap)) / 2
        d.add('Text', hb.text(cx, top + name_cap, name, 'bebas', name_pt, INK, id_='Dogs_name'))
        d.add('Text', hb.text(cx, top + name_cap + sh_ * 0.08 + num_cap, number, 'bebas', num_pt, INK, id_='Number'))
    else:
        max_h = sh_ * (0.8 if th < 100 else 0.35)
        name_pt = hb.fit_size(name, 'bebas', sw_ * 0.9, max_h / hb.PT / 0.7)
        name_cap = name_pt * hb.PT * 0.7
        d.add('Text', hb.text(cx, B + S + (sh_ + name_cap) / 2, name, 'bebas', name_pt, INK, id_='Dogs_name'))
    d.add('CUT', hb.rect(B, B, tw, th, rgb_stroke=(255, 0, 0), sw=hb.CUT_W_PT * hb.PT))
    d.add('Guides', hb.rect(0.15, 0.15, W - 0.3, H - 0.3, stroke=hb.GUIDE_BLEED, sw=0.2, dash=(1, 0.7)))
    d.add('Guides', hb.rect(B + S, B + S, sw_, sh_, stroke=hb.GUIDE_SAFE, sw=0.2, dash=(1, 0.7)))
    lab = 1.6 if th >= 40 else 1.2
    d.add('Guides', hb.text(cx, 2.1, 'NECK END - BLEED 3 mm', 'barlow-sb', lab / hb.PT * 0.9, hb.GUIDE_TEXT))
    d.add('Guides', hb.text(cx, H - 0.8, 'TRIM %g x %g mm  |  SAFE 3 mm' % (tw, th), 'barlow-sb', lab / hb.PT * 0.9, hb.GUIDE_TEXT))
    return d


def readme(code, p, files):
    pers = '"Dog’s name (optional)" and "Number (optional)" (up to 3 characters)' if p['number'] else '"Dog’s name (optional)" only'
    lines = '\n'.join(f'  {s:<18} {w:g} x {h:g} mm (width x length)' for s, w, h in p['areas'])
    ask = '\n- ASK: Ralawise publishes no print area for this garment. Sizes above are a placeholder.' if p['ask_area'] else ''
    return f"""{p['short']} - {p['sku']}
Print-ready, editable name{' + number' if p['number'] else ''} transfer templates, made {TODAY}.
Product: https://foxyprinting.co.uk/products/{p['handle']}

PERSONALISATION (optional - a plain garment can be ordered)
- {pers}. The customer also picks a font and a text colour on the website (order line properties "Font" and
  "Text colour"): use them; the template default is Bebas Neue in K100 as a placeholder.
- Sample text in the files: {p['sample'][0]}{(' / ' + p['sample'][1]) if p['sample'][1] else ''}. Replace with the customer's text; delete a line if it's blank.

PRINT AREA (trim) - Ralawise {code}: {RALAWISE_AREA_TEXT[code]}
{lines}
- 3XL and 4XL: Ralawise gives no print area (ASK); the largest file is used.{ask}
- Bleed 3 mm on every edge; safe area 3 mm inside the trim (the bleed is for the film trim line only).
- Placement: centred on the back, reading across the back, top of the text towards the neck. Distance from the collar: ASK.

LAYERS
- Artwork: empty (no background). Text: live, editable Bebas Neue (ids Dogs_name{', Number' if p['number'] else ''}).
- CUT: red RGB 255,0,0, 0.25 pt, no fill, on the trim line - for trimming the transfer film, never prints.
- Guides (hidden, non-printing): green dashed = bleed edge, magenta dashed = safe area.

PRINT AND PRESS - ASK
- Transfer method, mirroring (these are unmirrored) and press settings. The supplier care label says "do not iron",
  so test-press one garment first.

FILES
{chr(10).join('- ' + f for f in files)}
- PDFs with real layers (TrimBox/BleedBox set) are in Shopify Files: links in "PDF - DOWNLOAD LINKS.txt".
- Fonts/FONTS - DOWNLOAD LINK.txt and Fonts/OFL.txt.
- 100 dpi PNG previews: website repo, foxyprinting-rebrand/exports/pets/2026-10-08-dog-clothing-upgrade/artwork/

Regenerate: python3 tools/artwork/dog_clothing_templates.py --out <folder>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    for code, p in PRODUCTS.items():
        out = Path(a.out) / f"{p['short']} - {p['sku']}"
        (out / 'Fonts').mkdir(parents=True, exist_ok=True)
        files = []
        for size, w, h in p['areas']:
            doc = doc_for(w, h, p['sample'][0], p['sample'][1] if p['number'] else None)
            name = f"{code} name{' and number' if p['number'] else ''} - {size} {w:g}x{h:g}mm"
            title = f"{p['short']} transfer, size {size}, {w:g}x{h:g}mm - {code}"
            hb.write_svg(doc, out / f'{name}.svg', title)
            hb.write_pdf(doc, out / f'{name}.pdf', title, guides_on=False)
            prev = out / '_preview.pdf'
            hb.write_pdf(doc, prev, title, guides_on=True)
            subprocess.run(['pdftoppm', '-r', '100', '-png', '-singlefile', str(prev), str(out / f'{name} - preview')], check=True)
            prev.unlink()
            files.append(f'{name}.svg')
        (out / 'README.txt').write_text(readme(code, p, files), encoding='utf-8')
        (out / 'Fonts' / 'FONTS - DOWNLOAD LINK.txt').write_text(dv.fonts_txt(), encoding='utf-8')
        (out / 'Fonts' / 'OFL.txt').write_text(hb.ofl_txt(), encoding='utf-8')
        print(out)


if __name__ == '__main__':
    main()
