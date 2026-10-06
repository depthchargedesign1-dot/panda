#!/usr/bin/env python3
r"""mugkit - Foxy Printing mug artwork engine.

One JSON spec -> print-ready sublimation files for a mug wrap:
  * <base> - 300dpi.png          raster print file (300 dpi metadata set)
  * <base>.pdf                   vector print file, LIVE text (editable in Illustrator / Acrobat Pro)
  * <base> - MIRRORED.pdf        only for drivers/RIPs that don't mirror transfers
  * <base> (editable).svg        layered master: Background / Artwork / Personalisation
  * <base> - PROOF.jpg           guides + labels, for checking
  * mockups (white-background product shots) and a zip with Fonts/

Usage:
  python3 mugkit.py all   spec.json --out OUTDIR [--set Name=SMITH --set Number=10]
  python3 mugkit.py build spec.json --out OUTDIR [--set ...]
  python3 mugkit.py mockups OUTDIR/<base>\ -\ 300dpi.png --out OUTDIR [--size 11oz]

Needs: python3 + Pillow + numpy, node + playwright (Chromium). Fonts are pulled from
Google Fonts (OFL) on first use and cached in ~/.mugkit-fonts.
"""
import argparse, base64, html, io, json, math, os, re, shutil, subprocess, sys, urllib.request, zipfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("MUGKIT_FONTS", os.path.expanduser("~/.mugkit-fonts"))

# Print area (trim) in mm, plus mug body size for mockups. Check against your blanks/press.
SIZES = {
    "11oz":    dict(trim=(200, 70), bleed=3, safe=3, dia=82, height=96, label="11oz full wrap"),
    "11oz-85": dict(trim=(200, 85), bleed=3, safe=3, dia=82, height=96, label="11oz tall wrap"),
    "15oz":    dict(trim=(215, 90), bleed=3, safe=3, dia=87, height=117, label="15oz full wrap"),
}

# --------------------------------------------------------------------------- fonts
_font_cache = {}


def _get(url, ua="Wget/1.21"):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def font_file(spec):
    """'Oswald:700' -> path to a TTF. Google Fonts first, then fc-match."""
    if spec in _font_cache:
        return _font_cache[spec]
    fam, _, weight = spec.partition(":")
    weight = weight or "400"
    os.makedirs(FONT_DIR, exist_ok=True)
    path = os.path.join(FONT_DIR, f"{fam.replace(' ', '')}-{weight}.ttf")
    if not os.path.exists(path):
        q = fam.strip().replace(" ", "+")
        for url in (f"https://fonts.googleapis.com/css2?family={q}:wght@{weight}",
                    f"https://fonts.googleapis.com/css2?family={q}"):
            try:
                m = re.search(rb"url\((https://[^)]+?\.ttf)\)", _get(url))
                if m:
                    open(path, "wb").write(_get(m.group(1).decode()))
                    break
            except Exception:
                continue
        else:
            out = subprocess.run(["fc-match", "-f", "%{file}", f"{fam}:weight={weight}"],
                                 capture_output=True, text=True).stdout.strip()
            if not out:
                sys.exit(f"font not found: {spec}")
            path = out
    _font_cache[spec] = path
    return path


def font_family(spec):
    return ImageFont.truetype(font_file(spec), 20).getname()[0]


def font_weight(spec):
    return spec.partition(":")[2] or "400"


def text_width(text, spec, size, spacing=0.0):
    f = ImageFont.truetype(font_file(spec), 400)
    return f.getlength(text) / 400 * size + spacing * max(len(text) - 1, 0)


def fit_size(text, spec, size, max_w, spacing=0.0):
    w = text_width(text, spec, size, spacing)
    return size if not max_w or w <= max_w else size * max_w / w


# --------------------------------------------------------------------------- svg helpers
def esc(s):
    return html.escape(str(s), quote=True)


def svg_text(x, y, text, font, size, fill, anchor="middle", outline=None, spacing=0.0, ident=None):
    """Live text. Outline is a separate stroke copy underneath (prints the same everywhere)."""
    fam, wt = font_family(font), font_weight(font)
    common = (f'x="{x:.3f}" y="{y:.3f}" font-family="{esc(fam)}" font-weight="{wt}" '
              f'font-size="{size:.3f}" text-anchor="{anchor}"'
              + (f' letter-spacing="{spacing:.3f}"' if spacing else ""))
    parts = []
    if outline:
        parts.append(f'<text {common} fill="{outline["color"]}" stroke="{outline["color"]}" '
                     f'stroke-width="{outline["width"]:.3f}" stroke-linejoin="round">{esc(text)}</text>')
    parts.append(f'<text {common} fill="{fill}">{esc(text)}</text>')
    body = "".join(parts)
    if ident:
        return f'<g id="{esc(ident)}" data-field="{esc(ident)}">{body}</g>'
    return body


def data_uri(img, fmt="PNG"):
    b = io.BytesIO()
    img.save(b, fmt, **({"quality": 92} if fmt == "JPEG" else {"optimize": True}))
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(b.getvalue()).decode()


def load_image(src, spec_dir):
    if re.match(r"https?://", src):
        return Image.open(io.BytesIO(_get(src, "Mozilla/5.0"))).convert("RGBA")
    p = src if os.path.isabs(src) else os.path.join(spec_dir, src)
    return Image.open(p).convert("RGBA")


# --------------------------------------------------------------------------- football shirt
# Shirt drawn in a 1000 x 1100 unit box. Short sleeves, side panels, cuffs, collar,
# fabric shading. view = back (name + number) or front (crest/chest text + small number).
SHIRT_OUTLINE = ("M395,48 Q300,62 238,88 Q150,170 58,300 L176,412 L262,338 "
                 "Q270,690 268,1040 Q500,1062 732,1040 Q730,690 738,338 L824,412 L942,300 "
                 "Q850,170 762,88 Q700,62 605,48 {neck} Z")
NECK_BACK = "Q500,92 395,48"
NECK_FRONT = {"crew": "Q500,128 395,48", "v": "L500,190 L395,48", "polo": "L500,150 L395,48"}
LEFT_SLEEVE = "M238,88 Q150,170 58,300 L176,412 L262,338 Q262,200 300,95 Z"
RIGHT_SLEEVE = "M762,88 Q850,170 942,300 L824,412 L738,338 Q738,200 700,95 Z"
LEFT_CUFF = "M58,300 L176,412 L201,385 L84,272 Z"
RIGHT_CUFF = "M942,300 L824,412 L799,385 L916,272 Z"

PATTERNS = ("plain", "stripes", "pinstripes", "hoops", "halves", "quarters", "sash", "chevron", "gradient")


def shirt_pattern(pattern, c):
    c0, c1 = c[0], (c[1] if len(c) > 1 else c[0])
    out = [f'<rect x="0" y="0" width="1000" height="1100" fill="{c0}"/>']
    if pattern == "stripes":
        w = 1000 / 9
        for i in range(9):
            if i % 2:
                out.append(f'<rect x="{i*w:.1f}" y="0" width="{w:.1f}" height="1100" fill="{c1}"/>')
    elif pattern == "pinstripes":
        for i in range(1, 40):
            out.append(f'<rect x="{i*25-2.5:.1f}" y="0" width="5" height="1100" fill="{c1}"/>')
    elif pattern == "hoops":
        for i in range(0, 12):
            if i % 2:
                out.append(f'<rect x="0" y="{i*100:.0f}" width="1000" height="100" fill="{c1}"/>')
    elif pattern == "halves":
        out.append(f'<rect x="500" y="0" width="500" height="1100" fill="{c1}"/>')
    elif pattern == "quarters":
        out.append(f'<rect x="500" y="0" width="500" height="560" fill="{c1}"/>'
                   f'<rect x="0" y="560" width="500" height="540" fill="{c1}"/>')
    elif pattern == "sash":
        out.append(f'<polygon points="250,60 420,60 860,1100 690,1100" fill="{c1}"/>')
    elif pattern == "chevron":
        out.append(f'<polygon points="230,170 500,420 770,170 770,290 500,540 230,290" fill="{c1}"/>')
    elif pattern == "gradient":
        out.append(f'<defs><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c0}"/>'
                   f'<stop offset="1" stop-color="{c1}"/></linearGradient></defs>'
                   '<rect x="0" y="0" width="1000" height="1100" fill="url(#sg)"/>')
    if len(c) > 2 and pattern in ("stripes", "hoops"):  # optional thin accent pinline
        pass
    return "".join(out)


CREST = "M500,0 L560,18 L560,70 Q560,110 500,130 Q440,110 440,70 L440,18 Z"


def shirt_svg(el, uid, values):
    """Return (svg group, fields used) for a shirt element, in its own 1000-unit space."""
    view = el.get("view", "back")
    colors = el.get("colors", ["#d71920", "#ffffff"])
    pattern = el.get("pattern", "plain")
    trim = el.get("trim", "#111111")
    sleeves = el.get("sleeves")
    collar = el.get("collar", trim)
    cuffs = el.get("cuffs", trim)
    neck = NECK_BACK if view == "back" else NECK_FRONT.get(el.get("neck", "v"), NECK_FRONT["v"])
    outline = SHIRT_OUTLINE.format(neck=neck)
    cid = f"clip{uid}"
    g = [f'<defs><clipPath id="{cid}"><path d="{outline}"/></clipPath>'
         f'<linearGradient id="shd{uid}" x1="0" y1="0" x2="1" y2="0">'
         '<stop offset="0" stop-color="#000" stop-opacity="0.32"/>'
         '<stop offset="0.22" stop-color="#000" stop-opacity="0.02"/>'
         '<stop offset="0.42" stop-color="#fff" stop-opacity="0.10"/>'
         '<stop offset="0.6" stop-color="#000" stop-opacity="0.0"/>'
         '<stop offset="0.8" stop-color="#000" stop-opacity="0.06"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0.34"/></linearGradient>'
         f'<radialGradient id="fold{uid}" cx="0.5" cy="0.5" r="0.5">'
         '<stop offset="0" stop-color="#000" stop-opacity="0.16"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="vsh{uid}" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#fff" stop-opacity="0.12"/>'
         '<stop offset="0.35" stop-color="#fff" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#000" stop-opacity="0.14"/></linearGradient></defs>']
    # drop shadow
    g.append(f'<path d="{outline}" transform="translate(10,16)" fill="#000" fill-opacity="0.18"/>')
    g.append(f'<g clip-path="url(#{cid})">{shirt_pattern(pattern, colors)}')
    if sleeves:
        g.append(f'<path d="{LEFT_SLEEVE}" fill="{sleeves}"/><path d="{RIGHT_SLEEVE}" fill="{sleeves}"/>')
    g.append(f'<path d="{LEFT_CUFF}" fill="{cuffs}"/><path d="{RIGHT_CUFF}" fill="{cuffs}"/>')
    # side panels
    if el.get("side_panels", True):
        g.append(f'<path d="M270,345 Q277,690 276,1040 L289,1040 Q290,690 283,350 Z" fill="{trim}"/>'
                 f'<path d="M730,345 Q723,690 724,1040 L711,1040 Q710,690 717,350 Z" fill="{trim}"/>')
    # raglan / shoulder seams and hem band
    g.append('<path d="M262,338 Q285,190 345,62 M738,338 Q715,190 655,62" fill="none" stroke="#000" '
             'stroke-opacity="0.18" stroke-width="5"/>'
             '<path d="M268,1010 Q500,1032 732,1010" fill="none" stroke="#000" stroke-opacity="0.15" stroke-width="5"/>')
    # shading: edges, folds, top light
    g.append(f'<rect x="0" y="0" width="1000" height="1100" fill="url(#shd{uid})"/>'
             f'<rect x="0" y="0" width="1000" height="1100" fill="url(#vsh{uid})"/>'
             f'<ellipse cx="330" cy="760" rx="55" ry="260" fill="url(#fold{uid})"/>'
             f'<ellipse cx="690" cy="700" rx="45" ry="230" fill="url(#fold{uid})"/>'
             f'<ellipse cx="300" cy="300" rx="70" ry="40" fill="url(#fold{uid})"/>'
             f'<ellipse cx="700" cy="300" rx="70" ry="40" fill="url(#fold{uid})"/>')
    g.append("</g>")
    # collar
    if view == "back":
        g.append(f'<path d="M395,48 Q500,92 605,48" fill="none" stroke="{collar}" stroke-width="26" stroke-linecap="round"/>')
    else:
        nk = NECK_FRONT.get(el.get("neck", "v"), NECK_FRONT["v"])
        # inside of the back of the shirt, seen through the neck opening
        g.append(f'<path d="M395,48 Q500,80 605,48 {nk} Z" fill="{colors[0]}"/>'
                 f'<path d="M395,48 Q500,80 605,48 {nk} Z" fill="#000" fill-opacity="0.38"/>'
                 f'<path d="M395,48 Q500,80 605,48" fill="none" stroke="{collar}" stroke-width="16" stroke-linecap="round"/>')
        g.append(f'<path d="M605,48 {nk}" fill="none" stroke="{collar}" stroke-width="26" '
                 'stroke-linecap="round" stroke-linejoin="round"/>')
        if el.get("neck") == "polo":
            g.append(f'<path d="M395,48 L340,120 L470,165 Z M605,48 L660,120 L530,165 Z" fill="{collar}"/>')
    g.append(f'<path d="{outline}" fill="none" stroke="#000" stroke-opacity="0.35" stroke-width="4"/>')

    used = {}
    tfont = el.get("font", "Oswald:700")
    tcol = el.get("text_color", "#ffffff")
    toutline = el.get("text_outline")  # {"color": "#000", "width": 14}

    def field_text(spec_part, default_field):
        if not spec_part:
            return None, None
        fld = spec_part.get("field", default_field)
        txt = values.get(fld, spec_part.get("text", "")) if fld else spec_part.get("text", "")
        if spec_part.get("upper", True):
            txt = txt.upper()
        if fld:
            used[fld] = txt
        return txt, fld

    if view == "back":
        name, nf = field_text(el.get("name"), "Name")
        if name:
            nfont = el["name"].get("font", tfont)
            sp = el["name"].get("spacing", 6)
            size = fit_size(name, nfont, el["name"].get("size", 120), 430, sp)
            g.append(svg_text(500, 285, name, nfont, size, tcol, outline=toutline and
                              {"color": toutline["color"], "width": toutline.get("width", 14) * 0.6},
                              spacing=sp, ident=nf))
        num, nmf = field_text(el.get("number"), "Number")
        if num:
            mfont = el["number"].get("font", tfont)
            size = fit_size(num, mfont, el["number"].get("size", 430), 420)
            g.append(svg_text(500, 730, num, mfont, size, tcol, outline=toutline and
                              {"color": toutline["color"], "width": toutline.get("width", 14)}, ident=nmf))
    else:
        crest = el.get("crest")
        if crest:
            ccol = crest.get("color", tcol)
            g.append(f'<g transform="translate(150,190)"><path d="{CREST}" fill="{ccol}" '
                     f'stroke="{crest.get("outline", trim)}" stroke-width="6"/></g>')
            ct, cf = field_text(crest, None)
            if ct:
                cfont = crest.get("font", tfont)
                g.append(svg_text(650, 268, ct, cfont, fit_size(ct, cfont, 46, 100),
                                  crest.get("text_color", trim), ident=cf))
        chest, cf = field_text(el.get("chest_text"), None)
        if chest:
            cfont = el["chest_text"].get("font", tfont)
            g.append(svg_text(500, 560, chest, cfont, fit_size(chest, cfont, el["chest_text"].get("size", 110), 520),
                              tcol, outline=toutline and {"color": toutline["color"], "width": 8}, ident=cf))
        num, nmf = field_text(el.get("number"), "Number")
        if num:
            mfont = el["number"].get("font", tfont)
            g.append(svg_text(350, 300, num, mfont, fit_size(num, mfont, 120, 120), tcol, ident=nmf))
    return "".join(g), used


# --------------------------------------------------------------------------- build
class Layout:
    def __init__(self, size):
        s = SIZES[size]
        self.size, self.s = size, s
        self.W, self.H = s["trim"]
        self.b, self.safe = s["bleed"], s["safe"]
        self.pw, self.ph = self.W + 2 * self.b, self.H + 2 * self.b

    def panel(self, name):
        """(centre x, usable width) in page mm."""
        if name == "full":
            return self.b + self.W / 2, self.W - 2 * self.safe
        cx = self.b + (self.W / 4 if name == "left" else 3 * self.W / 4)
        return cx, self.W / 2 - 2 * self.safe


def build_svg(spec, spec_dir, values):
    L = Layout(spec.get("size", "11oz"))
    fonts, used = set(), {}
    bg = spec.get("background", "#ffffff")
    layers = {"Background": [f'<rect x="0" y="0" width="{L.pw}" height="{L.ph}" fill="{bg}"/>'],
              "Artwork": [], "Personalisation": []}
    if spec.get("background_image"):
        im = load_image(spec["background_image"], spec_dir)
        tw, th = round(L.pw / 25.4 * 300), round(L.ph / 25.4 * 300)
        sc = max(tw / im.width, th / im.height)
        im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
        im = im.crop(((im.width - tw) // 2, (im.height - th) // 2, (im.width - tw) // 2 + tw, (im.height - th) // 2 + th))
        layers["Background"].append(f'<image x="0" y="0" width="{L.pw}" height="{L.ph}" '
                                    f'preserveAspectRatio="none" href="{data_uri(im.convert("RGB"), "JPEG")}"/>')
    for i, el in enumerate(spec.get("elements", [])):
        cx, pw = L.panel(el.get("panel", "left"))
        cx += el.get("dx_mm", 0)
        t = el["type"]
        if t == "image":
            im = load_image(el["src"], spec_dir)
            bw, bh = el.get("w_mm", pw), el.get("h_mm", L.H - 2 * L.safe)
            y = L.b + el.get("y_mm", L.safe)
            sc = min(bw / im.width, bh / im.height)
            w, h = im.width * sc, im.height * sc
            px = (round(w / 25.4 * 300), round(h / 25.4 * 300))
            if px[0] < im.width:
                im = im.resize(px, Image.LANCZOS)
            layers["Artwork"].append(f'<image x="{cx - w/2:.3f}" y="{y + (bh - h)/2:.3f}" width="{w:.3f}" height="{h:.3f}" '
                                     f'href="{data_uri(im)}"/>')
        elif t == "text":
            fld = el.get("field")
            txt = values.get(fld, el.get("text", "")) if fld else el.get("text", "")
            if el.get("upper"):
                txt = txt.upper()
            font = el.get("font", "Oswald:700")
            fonts.add(font)
            sp = el.get("spacing_mm", 0)
            size = fit_size(txt, font, el.get("size_mm", 10), el.get("max_w_mm", pw), sp)
            ol = el.get("outline")
            anchor = {"left": "start", "right": "end"}.get(el.get("align"), "middle")
            x = cx if anchor == "middle" else (cx - pw / 2 if anchor == "start" else cx + pw / 2)
            s = svg_text(x, L.b + el["y_mm"], txt, font, size, el.get("color", "#111111"), anchor,
                         ol and {"color": ol["color"], "width": ol.get("width_mm", 0.6)}, sp, fld)
            if fld:
                used[fld] = txt
            layers["Personalisation" if fld else "Artwork"].append(s)
        elif t == "shirt":
            body, u = shirt_svg(el, i, values)
            used.update(u)
            for part in ("name", "number", "chest_text", "crest"):
                if el.get(part):
                    fonts.add(el[part].get("font", el.get("font", "Oswald:700")))
            fonts.add(el.get("font", "Oswald:700"))
            w = el.get("w_mm", min(pw, (L.H - 2 * L.safe) / 1.1))
            sc = w / 1000
            y = L.b + el.get("y_mm", (L.H - 1100 * sc) / 2)
            layers["Artwork"].append(f'<g id="Shirt-{i}" transform="translate({cx - w/2:.3f},{y:.3f}) scale({sc:.6f})">{body}</g>')
        elif t == "rect":
            w = el.get("w_mm", pw)
            layers["Artwork"].append(f'<rect x="{cx - w/2:.3f}" y="{L.b + el.get("y_mm", 0)}" width="{w}" '
                                     f'height="{el.get("h_mm", 1)}" rx="{el.get("r_mm", 0)}" fill="{el.get("color", "#000")}"/>')
        else:
            sys.exit(f"unknown element type {t}")
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
           f'width="{L.pw}mm" height="{L.ph}mm" viewBox="0 0 {L.pw} {L.ph}">',
           f'<title>{esc(spec.get("title", ""))} - {SIZES[L.size]["label"]} {L.pw:g}x{L.ph:g}mm incl {L.b}mm bleed</title>']
    for name, items in layers.items():
        out.append(f'<g id="{name}">' + "".join(items) + "</g>")
    out.append("</svg>")
    return "\n".join(out), L, fonts, used


def font_faces(fonts):
    css = []
    for f in sorted(fonts):
        css.append(f"@font-face{{font-family:'{font_family(f)}';font-weight:{font_weight(f)};"
                   f"src:url('file://{font_file(f)}');}}")
    return "".join(css)


def render(svg, L, fonts, base, outdir):
    html_doc = ("<!doctype html><html><head><meta charset='utf-8'><style>"
                f"{font_faces(fonts)}@page{{size:{L.pw}mm {L.ph}mm;margin:0}}"
                "html,body{margin:0;padding:0;background:#fff}svg{display:block}"
                ".m svg{transform:scaleX(-1)}</style></head><body>" + svg + "</body></html>")
    hp = os.path.join(outdir, ".render.html")
    open(hp, "w").write(html_doc)
    env = dict(os.environ)
    if "NODE_PATH" not in env:
        env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    png = os.path.join(outdir, f"{base} - 300dpi.png")
    cmd = ["node", os.path.join(HERE, "render.js"), hp, str(L.pw), str(L.ph), png,
           os.path.join(outdir, f"{base}.pdf"), os.path.join(outdir, f"{base} - MIRRORED.pdf")]
    subprocess.run(cmd, check=True, env=env)
    os.remove(hp)
    fix_pdf_size([os.path.join(outdir, f"{base}.pdf"), os.path.join(outdir, f"{base} - MIRRORED.pdf")], L)
    im = Image.open(png).convert("RGB")
    want = (round(L.pw / 25.4 * 300), round(L.ph / 25.4 * 300))
    if im.size != want:
        im = im.resize(want, Image.LANCZOS)
    im.save(png, dpi=(300, 300), optimize=True)
    return png


def fix_pdf_size(paths, L):
    """Chromium rounds the page up to whole CSS px; trim the media box back to the exact mm size."""
    try:
        import pypdf
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pypdf"], check=True)
        import pypdf
    wpt, hpt = L.pw / 25.4 * 72, L.ph / 25.4 * 72
    for p in paths:
        r = pypdf.PdfReader(p)
        w = pypdf.PdfWriter()
        for pg in r.pages:
            top = float(pg.mediabox.top)
            x0 = 0.0  # the svg is mirrored about its own centre, so both files sit flush left
            box = pypdf.generic.RectangleObject([x0, top - hpt, x0 + wpt, top])
            pg.mediabox = box
            pg.cropbox = box
            pg.trimbox = pypdf.generic.RectangleObject([x0 + L.b / 25.4 * 72, top - hpt + L.b / 25.4 * 72,
                                                        x0 + wpt - L.b / 25.4 * 72, top - L.b / 25.4 * 72])
            pg.bleedbox = box
            w.add_page(pg)
        w.add_metadata({"/Title": os.path.basename(p)[:-4], "/Creator": "Foxy Printing mugkit"})
        with open(p, "wb") as f:
            w.write(f)


def proof(png, L, path, used):
    im = Image.open(png).convert("RGB")
    k = 1600 / im.width
    im = im.resize((1600, round(im.height * k)), Image.LANCZOS)
    pad = 60
    c = Image.new("RGB", (im.width + 2 * pad, im.height + 2 * pad + 70), "#e9e9e6")
    c.paste(im, (pad, pad))
    d = ImageDraw.Draw(c)
    mm = 300 / 25.4 * k

    def box(inset, col):
        d.rectangle((pad + inset * mm, pad + inset * mm, pad + im.width - inset * mm, pad + im.height - inset * mm),
                    outline=col, width=2)
    box(L.b, "#e3001b")
    box(L.b + L.safe, "#0077ff")
    for name in ("left", "right"):
        x = pad + L.panel(name)[0] * mm
        d.line((x, pad, x, pad + im.height), fill="#00a65a", width=1)
    f = ImageFont.truetype(font_file("Montserrat:600"), 22)
    txt = (f"{SIZES[L.size]['label']}  page {L.pw:g}x{L.ph:g}mm  (trim {L.W}x{L.H} + {L.b}mm bleed)   "
           "red = trim   blue = safe   green = panel centres")
    d.text((pad, pad + im.height + 18), txt, fill="#222", font=f)
    if used:
        d.text((pad, pad + im.height + 44), "Personalised fields: " + ", ".join(f"{k}={v}" for k, v in used.items()),
               fill="#c0006a", font=f)
    c.save(path, quality=88)


# --------------------------------------------------------------------------- mockups
def mug_render(art, size="11oz", view="left", handle=None, W=1600):
    """Render a white ceramic mug with the wrap printed on it. art = 300dpi PNG (incl bleed)."""
    s = SIZES[size]
    L = Layout(size)
    art = np.asarray(art.convert("RGB")).astype(np.float32) / 255.0
    apx = art.shape[1] / L.pw  # px per mm
    SS = 2
    Wc = W * SS
    canvas = np.ones((Wc, Wc, 3), np.float32)
    alpha = np.zeros((Wc, Wc), np.float32)
    BW = Wc * 0.5
    R = BW / 2
    BH = BW * s["height"] / s["dia"]
    e = BW * 0.085
    cx = Wc / 2 - (BW * 0.06 if handle == "right" else -BW * 0.06 if handle == "left" else 0)
    top = (Wc - BH) / 2 - e * 0.3
    r_mm = s["dia"] / 2
    uc = L.panel(view)[0] if view in ("left", "right") else view  # page mm at view centre
    if handle is None:
        handle = "left" if view == "left" else "right"
    hs = -1 if handle == "left" else 1

    yy, xx = np.mgrid[0:Wc, 0:Wc].astype(np.float32)
    # handle (drawn first, body covers the join)
    hcx, hcy = cx + hs * R * 0.98, top + BH * 0.47
    ro = ((xx - hcx) / (BW * 0.27)) ** 2 + ((yy - hcy) / (BH * 0.33)) ** 2
    ri = ((xx - hcx) / (BW * 0.16)) ** 2 + ((yy - hcy) / (BH * 0.215)) ** 2
    hmask = (ro <= 1) & (ri > 1) & (hs * (xx - cx) > R * 0.5)
    hshade = 0.80 + 0.2 * np.clip(1 - ((yy - (hcy - BH * 0.2)) / (BH * 0.5)) ** 2, 0, 1) - 0.18 * np.clip(ro - 0.6, 0, 1)
    canvas[hmask] = (np.stack([hshade] * 3, -1) * 0.97)[hmask]
    alpha[hmask] = 1

    # interior + rim (top ellipse)
    ell = ((xx - cx) / R) ** 2 + ((yy - top) / e) ** 2
    inner = ((xx - cx) / (R * 0.94)) ** 2 + ((yy - top - e * 0.06) / (e * 0.88)) ** 2
    rim = ell <= 1
    canvas[rim] = 0.93
    ins = inner <= 1
    g = 0.58 + 0.25 * np.clip((yy - (top - e)) / (2 * e), 0, 1) + 0.1 * np.clip((xx - cx) / R, -1, 1) * 0
    canvas[ins] = np.stack([g] * 3, -1)[ins]
    alpha[rim] = 1

    # body
    xn = (xx - cx) / R
    inside_x = np.abs(xn) <= 1
    xnc = np.clip(xn, -1, 1)
    ytop = top + e * np.sqrt(1 - xnc ** 2)
    yrel = (yy - ytop) / BH
    body = inside_x & (yrel >= 0) & (yrel <= 1)
    theta = np.arcsin(xnc)
    u_mm = uc + theta * r_mm
    v_mm = yrel * s["height"] - (s["height"] - L.H) / 2 + L.b  # print centred on body height
    ui = np.clip((u_mm * apx).astype(int), 0, art.shape[1] - 1)
    vi = np.clip((v_mm * apx).astype(int), 0, art.shape[0] - 1)
    printed = body & (u_mm >= L.b) & (u_mm <= L.b + L.W) & (v_mm >= L.b * 0.5) & (v_mm <= L.ph - L.b * 0.5)
    col = np.full((Wc, Wc, 3), 0.965, np.float32)
    col[printed] = art[vi[printed], ui[printed]]
    shade = 0.70 + 0.30 * np.clip(np.cos(theta + 0.25), 0, 1) ** 0.7
    shade = shade - 0.10 * np.clip((yrel - 0.85) / 0.15, 0, 1)
    spec = 0.55 * np.exp(-((theta + 0.62) / 0.10) ** 2) + 0.18 * np.exp(-((theta - 1.05) / 0.05) ** 2)
    lit = col * shade[..., None] + spec[..., None] * (1 - col * 0.3)
    canvas[body] = np.clip(lit, 0, 1)[body]
    alpha[body] = 1

    img = Image.fromarray((canvas * 255).astype(np.uint8))
    a = Image.fromarray((alpha * 255).astype(np.uint8))
    # soft contact shadow
    sh = Image.new("L", (Wc, Wc), 0)
    ImageDraw.Draw(sh).ellipse((cx - R * 1.05, top + BH + e * 0.2, cx + R * 1.15, top + BH + e * 1.6), fill=120)
    sh = sh.filter(ImageFilter.GaussianBlur(Wc * 0.012))
    out = Image.new("RGB", (Wc, Wc), (255, 255, 255))
    out.paste((150, 150, 150), (0, 0), sh)
    out.paste(img, (0, 0), a.filter(ImageFilter.GaussianBlur(0.8)))
    return out.resize((W, W), Image.LANCZOS)


def mockups(png, outdir, base, size="11oz"):
    art = Image.open(png)
    L = Layout(size)
    files = []
    left = mug_render(art, size, "left")
    right = mug_render(art, size, "right")
    p = os.path.join(outdir, f"{base} - mockup 1 left side.jpg"); left.save(p, quality=92); files.append(p)
    p = os.path.join(outdir, f"{base} - mockup 2 right side.jpg"); right.save(p, quality=92); files.append(p)
    both = Image.new("RGB", (2000, 2000), "white")  # renders are on white, so plain crops tile cleanly
    l2, r2 = left.resize((1250, 1250), Image.LANCZOS), right.resize((1250, 1250), Image.LANCZOS)
    both.paste(l2.crop((150, 0, 1100, 1250)), (60, 375))
    both.paste(r2.crop((150, 0, 1100, 1250)), (990, 375))
    p = os.path.join(outdir, f"{base} - mockup 0 both sides.jpg"); both.save(p, quality=92); files.insert(0, p)
    # flat artwork shot
    flat = Image.new("RGB", (2000, 2000), (246, 246, 244))
    a = art.convert("RGB")
    a = a.resize((1800, round(1800 * a.height / a.width)), Image.LANCZOS)
    sh = Image.new("L", flat.size, 0)
    y = (2000 - a.height) // 2
    ImageDraw.Draw(sh).rectangle((110, y + 20, 110 + a.width, y + 20 + a.height), fill=90)
    flat.paste((180, 180, 180), (0, 0), sh.filter(ImageFilter.GaussianBlur(18)))
    flat.paste(a, (100, y))
    d = ImageDraw.Draw(flat)
    f = ImageFont.truetype(font_file("Montserrat:600"), 46)
    d.text((1000, y - 90), "FULL WRAP DESIGN", fill="#333", font=f, anchor="ma")
    p = os.path.join(outdir, f"{base} - mockup 3 flat wrap.jpg"); flat.save(p, quality=92); files.append(p)
    return files


# --------------------------------------------------------------------------- packaging
OFL_NOTE = ("Fonts used in this artwork are open-licence Google Fonts (SIL Open Font License 1.1).\n"
            "Install the .ttf files in this folder before editing the SVG/PDF so the live text\n"
            "(names, numbers, phrases) keeps the right typeface. Licence: https://openfontlicense.org\n")


def readme(spec, L, base, used):
    fields = ", ".join(used) if used else "none (fixed design)"
    return f"""Foxy Printing - mug print artwork
Product: {spec.get('title', '')}
SKU: {spec.get('sku', '')}
Size: {SIZES[L.size]['label']} - trim {L.W} x {L.H} mm + {L.b} mm bleed = {L.pw:g} x {L.ph:g} mm page, {L.safe} mm safe area.
Personalised fields (live text): {fields}

FILES
- {base} - 300dpi.png      raster print file, {round(L.pw/25.4*300)} x {round(L.ph/25.4*300)} px, 300 dpi metadata
- {base}.pdf               vector print file with LIVE text - open in Illustrator / Acrobat Pro to edit names
- {base} - MIRRORED.pdf    only if your printer driver / RIP does NOT mirror sublimation transfers
- {base} (editable).svg    layered master: Background / Artwork / Personalisation (ids = field names)
- {base} - PROOF.jpg       check copy with trim (red), safe (blue) and panel centres (green)
- Fonts/                   the .ttf files used - install before editing

PERSONALISING AN ORDER
Fast: python3 mugkit.py build spec.json --out ORDER --set Name=SMITH --set Number=10
By hand: open the .pdf or .svg in Illustrator, edit the text in the Personalisation layer
(long names: reduce the font size so the text stays inside the safe area), save, print at 100%.

PRINT: white 11oz/15oz sublimation mug, print at 100% (actual size), press per your blank's settings.
"""


def zip_pack(outdir, base, fonts, zpath):
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(outdir)):
            p = os.path.join(outdir, f)
            if os.path.isfile(p) and f.startswith(base) and not f.endswith(".zip"):
                z.write(p, f)
        if os.path.exists(os.path.join(outdir, "README - how to print.txt")):
            z.write(os.path.join(outdir, "README - how to print.txt"), "README - how to print.txt")
        for fs in sorted(fonts):
            z.write(font_file(fs), "Fonts/" + os.path.basename(font_file(fs)))
        z.writestr("Fonts/OFL - licence note.txt", OFL_NOTE)


# --------------------------------------------------------------------------- cli
def base_name(spec, L):
    nm = re.sub(r'[\\/:*?"<>|]+', "-", spec.get("name", spec.get("title", "design")))
    return f"{spec.get('sku', 'FOXY-SUB-NEW')} {nm} - {L.size} wrap {L.pw:g}x{L.ph:g}mm".strip()


def cmd_build(spec_path, outdir, sets, do_mockups=False, do_zip=False):
    spec = json.load(open(spec_path))
    values = dict(spec.get("defaults", {}))
    values.update(sets)
    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)
    svg, L, fonts, used = build_svg(spec, os.path.dirname(os.path.abspath(spec_path)), values)
    fonts.add("Montserrat:600")
    base = base_name(spec, L)
    open(os.path.join(outdir, f"{base} (editable).svg"), "w").write(svg)
    png = render(svg, L, fonts, base, outdir)
    proof(png, L, os.path.join(outdir, f"{base} - PROOF.jpg"), used)
    open(os.path.join(outdir, "README - how to print.txt"), "w").write(readme(spec, L, base, used))
    result = {"base": base, "png": png, "fields": used, "page_mm": [L.pw, L.ph],
              "px": list(Image.open(png).size), "files": []}
    if do_mockups:
        result["mockups"] = mockups(png, outdir, base, L.size)
    if do_zip:
        z = os.path.join(outdir, f"{spec.get('sku', 'FOXY-SUB-NEW')} - print artwork.zip")
        zip_pack(outdir, base, fonts - {"Montserrat:600"} or fonts, z)
        result["zip"] = z
    result["files"] = sorted(os.listdir(outdir))
    print(json.dumps(result, indent=1))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["build", "all", "mockups"])
    ap.add_argument("path")
    ap.add_argument("--out", default="out")
    ap.add_argument("--set", action="append", default=[], help="Field=Value for personalised text")
    ap.add_argument("--size", default="11oz")
    a = ap.parse_args()
    sets = dict(s.split("=", 1) for s in a.set)
    if a.cmd == "mockups":
        os.makedirs(a.out, exist_ok=True)
        b = os.path.basename(a.path).replace(" - 300dpi.png", "")
        print(json.dumps(mockups(a.path, a.out, b, a.size), indent=1))
    else:
        cmd_build(a.path, a.out, sets, do_mockups=a.cmd == "all", do_zip=a.cmd == "all")


if __name__ == "__main__":
    main()
