"""Print-ready v2 artwork for the 20 older bar / man cave coasters (8 Oct 2026).

usage: python3 tools/bar_coasters_v2/art.py SRC_DIR OUT_DIR [key ...]
SRC_DIR holds the owner's 2021 files renamed <key>.pdf (x21..x30 = bar mats 3x10 "NN. 100x100.pdf",
o01..o10 = others mats x10 "N. 100x100 others.pdf").

For each design:
  * background = the original vector/raster artwork with all old text removed (redaction, text only; o03 has
    outlined text, so its two lines are covered with the flat background colour), scaled 100 -> 96 mm so the
    whole design fills the 96 x 96 mm bleed page and the 90 x 90 mm trim sits 3 mm in;
  * live text re-set in OFL Google Fonts (spec.py), kept inside the 3 mm safe area (6..90 mm on the page);
  * <out>/<key>.pdf  (layers Artwork + Text, fonts embedded) and <key>.svg (groups Artwork / Text / hidden Guides,
    text elements with ids named after the website fields), <key>-check.png (with trim + safe guides).
"""
import os
import re
import subprocess
import sys
import tempfile

import pymupdf
from fontTools.ttLib import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spec import DESIGNS, FONTS, FONT_NAMES  # noqa: E402

FONT_DIR = os.path.join(HERE, "..", "artwork", "assets", "fonts")
PAGE = 96.0
SCALE = PAGE / 100.0
TRIM0, TRIM1 = 3.0, 93.0
SAFE0, SAFE1 = 6.0, 90.0
_cap = {}


def cap_frac(key):
    if key not in _cap:
        t = TTFont(os.path.join(FONT_DIR, FONTS[key]))
        ch = getattr(t["OS/2"], "sCapHeight", 0) or 0.7 * t["head"].unitsPerEm
        _cap[key] = ch / t["head"].unitsPerEm
        try:
            pdfmetrics.getFont(key)
        except KeyError:
            pdfmetrics.registerFont(RLFont(key, os.path.join(FONT_DIR, FONTS[key])))
    return _cap[key]


def layout(line):
    """-> dict(text, font, size(mm), track(mm), cx, baseline (page mm, y down), width)"""
    f = line["font"]
    c = cap_frac(f)
    cap_h = (line["cap"] or (line["y1"] - line["y0"])) * SCALE
    if line["script"]:
        cap_h *= 1.0
    size = cap_h / c
    maxw = min((line["x1"] - line["x0"]) * SCALE, SAFE1 - SAFE0)
    cx = (line["x0"] + line["x1"]) / 2 * SCALE

    def width(sz):
        return pdfmetrics.stringWidth(line["text"], f, sz) + line["track"] * sz * max(0, len(line["text"]) - 1)

    if width(size) > maxw:
        size *= maxw / width(size)
    w = width(size)
    base = line["y1"] * SCALE
    top = base - size * c
    if top < SAFE0:
        base += SAFE0 - top
    if base > SAFE1:
        base = SAFE1
    cx = min(max(cx, SAFE0 + w / 2), SAFE1 - w / 2)
    return dict(text=line["text"], font=f, size=size, track=line["track"] * size, cx=cx, base=base, width=w,
                colour=line["colour"], shadow=line["shadow"], field=line["field"])


def background(src, spec, out_pdf):
    doc = pymupdf.open(src)
    page = doc[0]
    if not spec.get("cover"):
        for b in page.get_text("dict")["blocks"]:
            for l_ in b.get("lines", []):
                for s in l_["spans"]:
                    if s["text"].strip():
                        page.add_redact_annot(pymupdf.Rect(s["bbox"]) + (-3, -3, 3, 3), fill=False)
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    # second pass: line art lying wholly inside a strip box (outline strokes drawn over the old text, x26).
    # Separate pass because overlapping redaction boxes stop "remove if covered" from working.
    for (x0, y0, x1, y1) in spec.get("strip", []):
        page.add_redact_annot(pymupdf.Rect(x0 * mm, y0 * mm, x1 * mm, y1 * mm), fill=False)
    if spec.get("strip"):
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                              text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    for (x0, y0, x1, y1, col) in spec.get("cover", []):
        rgb = tuple(int(col[i:i + 2], 16) / 255 for i in (1, 3, 5))
        page.draw_rect(pymupdf.Rect(x0 * mm, y0 * mm, x1 * mm, y1 * mm), color=None, fill=rgb, overlay=True)
    assert not page.get_text().strip(), "text left in background"
    out = pymupdf.open()
    p = out.new_page(width=PAGE * mm, height=PAGE * mm)
    p.show_pdf_page(p.rect, doc, 0)
    out.save(out_pdf, garbage=3, deflate=True)


def text_pdf(items, out_pdf, title):
    c = canvas.Canvas(out_pdf, pagesize=(PAGE * mm, PAGE * mm))
    c.setTitle(title)
    c.setAuthor("Foxy Printing")
    for it in items:
        for (dx, dy, col) in ([it["shadow"]] if it["shadow"] else []) + [(0, 0, it["colour"])]:
            c.setFillColor(HexColor(col))
            t = c.beginText((it["cx"] - it["width"] / 2 + dx) * mm, (PAGE - it["base"] - dy) * mm)
            t.setFont(it["font"], it["size"] * mm)
            t.setCharSpace(it["track"] * mm)
            t.textOut(it["text"])
            c.drawText(t)
    c.showPage()
    c.save()


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(key, src_dir, out_dir, sku=None, title=""):
    spec = DESIGNS[key]
    items = [layout(l_) for l_ in spec["lines"]]
    tmp = tempfile.mkdtemp()
    bg = os.path.join(tmp, "bg.pdf")
    tx = os.path.join(tmp, "tx.pdf")
    background(os.path.join(src_dir, f"{key}.pdf"), spec, bg)
    text_pdf(items, tx, title)
    name = os.path.join(out_dir, sku or key)
    # ---- PDF with layers
    out = pymupdf.open()
    p = out.new_page(width=PAGE * mm, height=PAGE * mm)
    oc_art = out.add_ocg("Artwork", on=True)
    oc_txt = out.add_ocg("Text", on=True)
    p.show_pdf_page(p.rect, pymupdf.open(bg), 0, oc=oc_art)
    p.show_pdf_page(p.rect, pymupdf.open(tx), 0, oc=oc_txt)
    out.set_metadata(dict(title=title, author="Foxy Printing", subject="90 x 90 mm coaster + 3 mm bleed"))
    out.save(name + ".pdf", garbage=3, deflate=True)
    # ---- SVG: background from pdftocairo + live text
    subprocess.run(["pdftocairo", "-svg", bg, os.path.join(tmp, "bg.svg")], check=True)
    s = open(os.path.join(tmp, "bg.svg")).read()
    inner = re.sub(r"^.*?<svg[^>]*>", "", s, flags=re.S)
    inner = re.sub(r"</svg>\s*$", "", inner)
    k = 1 / mm  # pt -> mm
    a = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{PAGE}mm" '
         f'height="{PAGE}mm" viewBox="0 0 {PAGE} {PAGE}">',
         f'<g id="Artwork" transform="scale({k:.6f})">', inner, "</g>", '<g id="Text">']
    for i, it in enumerate(items):
        idt = re.sub(r"[^A-Za-z0-9]+", "_", it["field"]).strip("_") if it["field"] else f"fixed_{i}"
        for (dx, dy, col) in ([it["shadow"]] if it["shadow"] else []):
            a.append(f'<text x="{it["cx"] + dx:.2f}" y="{it["base"] + dy:.2f}" font-family="{FONT_NAMES[it["font"]]}" '
                     f'font-size="{it["size"]:.2f}" letter-spacing="{it["track"]:.2f}" text-anchor="middle" fill="{col}">{esc(it["text"])}</text>')
        a.append(f'<text id="{idt}" x="{it["cx"]:.2f}" y="{it["base"]:.2f}" font-family="{FONT_NAMES[it["font"]]}" '
                 f'font-size="{it["size"]:.2f}" letter-spacing="{it["track"]:.2f}" text-anchor="middle" fill="{it["colour"]}">{esc(it["text"])}</text>')
    a.append("</g>")
    a.append('<g id="Guides" style="display:none">'
             f'<rect x="{TRIM0}" y="{TRIM0}" width="{TRIM1 - TRIM0}" height="{TRIM1 - TRIM0}" rx="3" fill="none" stroke="#00AEEF" stroke-width="0.2"/>'
             f'<rect x="{SAFE0}" y="{SAFE0}" width="{SAFE1 - SAFE0}" height="{SAFE1 - SAFE0}" fill="none" stroke="#EC008C" stroke-width="0.2" stroke-dasharray="1 1"/></g>')
    a.append("</svg>")
    open(name + ".svg", "w").write("\n".join(a))
    # ---- check render with guides
    d = pymupdf.open(name + ".pdf")
    pg = d[0]
    pg.draw_rect(pymupdf.Rect(TRIM0 * mm, TRIM0 * mm, TRIM1 * mm, TRIM1 * mm), color=(0, 0.68, 0.94), width=0.6)
    pg.draw_rect(pymupdf.Rect(SAFE0 * mm, SAFE0 * mm, SAFE1 * mm, SAFE1 * mm), color=(0.93, 0, 0.55), width=0.4, dashes="[2 2] 0")
    pg.get_pixmap(dpi=110).save(name + "-check.png")
    return items


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    keys = sys.argv[3:] or sorted(DESIGNS)
    for k_ in keys:
        its = build(k_, src, out)
        print(k_, [(i["text"], round(i["size"] * cap_frac(i["font"]), 1)) for i in its])
