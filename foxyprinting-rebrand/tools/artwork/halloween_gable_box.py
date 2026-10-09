"""Halloween treat gable box (100 x 60 x 100 mm) on SRA3 landscape, for the Intec ColorCut flatbed.

Writes, per colourway (black, orange):
  - <name>.svg : editable vector artwork with two top-level groups, "Artwork" (prints) and "CUT"
                 (does not print). Text stays live so the name can be changed.
  - <name>.pdf : the same as a vector PDF, written as plain ASCII so it can be saved into Dropbox as a text file.
Cut lines use the ColorCut Pro line colours from Intec's FB550 user guide (section 4.1):
  Red  CMYK 2/98/95/0  (RGB 255,0,0)  -> CUT with the blade
  Blue CMYK 91/80/1/0  (RGB 0,0,255)  -> CREASE with the creasing tool
Registration PageMARKs and the job barcode are NOT drawn here: the ColorCut Pro plug-in in Illustrator adds them
("ADD PageMARKs & BarCode") and stores the cut job in the Job Library. The design keeps the 12 mm (left) and 10 mm
(other edges) clear margins the marks need.
"""
import math
import sys
from pathlib import Path

from reportlab.lib.colors import CMYKColor
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab import rl_config

rl_config.invariant = 1          # repeatable output
rl_config.useA85 = 1             # ASCII85 streams: the PDF is plain text

SHEET_W, SHEET_H = 450.0, 320.0  # SRA3 landscape, mm
W, D, H = 100.0, 60.0, 100.0     # box width, depth, body height
GLUE = 12.0                      # glue flap
ROOF = 42.0                      # sloped roof panel on front/back (folds in at 45 degrees)
HANDLE = 45.0                    # handle panel above the roof
BOTTOM = D - 2.0                 # front/back bottom flaps
DUST = D / 2 - 2.0               # side bottom flaps
BLEED = 3.0

NET_W = GLUE + 2 * W + 2 * D
NET_TOP = H + ROOF + HANDLE
OX = (SHEET_W - NET_W) / 2                         # left edge of the glue flap
OY = (SHEET_H - (NET_TOP + BOTTOM)) / 2 + BOTTOM    # bottom fold of the body

# x positions of the panels: glue | front | side | back | side
X0 = 0.0
XF = GLUE
XS1 = XF + W
XB = XS1 + D
XS2 = XB + W
XE = XS2 + D

CUT_RGB, CREASE_RGB = (1, 0, 0), (0, 0, 1)
CUT_CMYK, CREASE_CMYK = (0.02, 0.98, 0.95, 0), (0.91, 0.80, 0.01, 0)

COLOURWAYS = {
    'black': dict(bg=(0.6, 0.4, 0.4, 1.0), bg_rgb='#141414', text=(0, 0.6, 1, 0), text_rgb='#F7931E',
                  star=(0, 0.6, 1, 0), star_rgb='#F7931E'),
    'orange': dict(bg=(0, 0.6, 1, 0), bg_rgb='#F7931E', text=(0.6, 0.4, 0.4, 1.0), text_rgb='#141414',
                   star=(0.6, 0.4, 0.4, 1.0), star_rgb='#141414'),
}


def outline():
    """Outer cut path of the flat net (mm, net coordinates, y up from the body's bottom fold)."""
    tri = D / 2  # side gable triangle height (matches the roof's 45 degree rise)
    pts = []
    # glue flap, tapered
    pts += [(X0, 3), (X0, H - 3), (XF, H)]
    # front: roof + handle panel
    pts += [(XF, H + ROOF + HANDLE), (XS1, H + ROOF + HANDLE)]
    # side 1: gable triangle
    pts += [(XS1, H), (XS1 + D / 2, H + tri), (XB, H)]
    # back: roof + handle panel
    pts += [(XB, H + ROOF + HANDLE), (XS2, H + ROOF + HANDLE)]
    # side 2: gable triangle
    pts += [(XS2, H), (XS2 + D / 2, H + tri), (XE, H)]
    # right edge down, then bottom flaps (side 2, back, side 1, front)
    pts += [(XE, 0), (XE - 3, -DUST), (XS2 + 3, -DUST), (XS2, 0)]
    pts += [(XS2, -BOTTOM + 4), (XS2 - 4, -BOTTOM), (XB + 4, -BOTTOM), (XB, -BOTTOM + 4), (XB, 0)]
    pts += [(XB, 0), (XB - 3, -DUST), (XS1 + 3, -DUST), (XS1, 0)]
    pts += [(XS1, -BOTTOM + 4), (XS1 - 4, -BOTTOM), (XF + 4, -BOTTOM), (XF, -BOTTOM + 4), (XF, 0)]
    pts += [(XF, 0), (X0, 3)]
    return pts


def handle_holes():
    """Rounded handle slots on the front and back handle panels: (cx, cy, w, h)."""
    cy = H + ROOF + HANDLE - 16
    return [(XF + W / 2, cy, 56, 14), (XB + W / 2, cy, 56, 14)]


def creases():
    lines = []
    for x in (XF, XS1, XB, XS2):                       # vertical body folds
        lines.append(((x, 0), (x, H)))
    lines.append(((XF, 0), (XE, 0)))                   # bottom flaps
    for x0 in (XF, XB):                                 # roof and handle folds on front/back
        lines.append(((x0, H), (x0 + W, H)))
        lines.append(((x0, H + ROOF), (x0 + W, H + ROOF)))
    for x0 in (XS1, XS2):                               # side gable fold
        lines.append(((x0, H), (x0 + D, H)))
    lines.append(((XF, 0), (XF, H)))                    # glue flap fold (same as front edge)
    return lines


def star(cx, cy, r):
    pts = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def ghost(cx, base, w):
    """Ghost outline as a polygon: rounded head, wavy hem."""
    h = w * 1.25
    pts = []
    for i in range(0, 181, 15):                         # head arc
        a = math.radians(i)
        pts.append((cx + (w / 2) * math.cos(a), base + h - w / 2 + (w / 2) * math.sin(a)))
    pts.append((cx - w / 2, base))
    for k in range(6):                                  # wavy hem
        x = cx - w / 2 + (k + 0.5) * w / 6
        pts.append((x, base + (w * 0.08 if k % 2 == 0 else -w * 0.04)))
    pts.append((cx + w / 2, base))
    return pts, h


def panel_motifs(x0, width, front):
    """Decoration for one panel in net coordinates. Returns list of (kind, data)."""
    items = []
    cx = x0 + width / 2
    if front:
        items.append(('text', (cx, 70, 'Ava’s', 15)))
        items.append(('text', (cx, 55, 'Party', 15)))
        for gx in (cx - 30, cx + 30):
            items.append(('ghost', (gx, 12, 16)))
        items.append(('pumpkin', (cx, 22, 15)))
        for sx, sy, r in ((x0 + 12, 88, 3), (x0 + width - 12, 86, 2.5), (x0 + 18, 45, 2), (x0 + width - 16, 47, 2.2)):
            items.append(('star', (sx, sy, r)))
    else:
        items.append(('pumpkin', (cx, 30, 10)))
        for sx, sy, r in ((cx - 15, 75, 2.5), (cx + 14, 82, 2), (cx, 60, 1.8), (cx - 10, 50, 1.5), (cx + 12, 55, 2)):
            items.append(('star', (sx, sy, r)))
    return items


def all_motifs():
    items = []
    for x0, wd, front in ((XF, W, True), (XS1, D, False), (XB, W, True), (XS2, D, False)):
        items += panel_motifs(x0, wd, front)
    for x0 in (XF, XB):                                 # stars on the handle panels
        for sx, sy, r in ((x0 + 15, H + ROOF + 12, 2.2), (x0 + W - 15, H + ROOF + 12, 2.2)):
            items.append(('star', (sx, sy, r)))
    return items


# ----------------------------------------------------------------------------------------------------- SVG
def svg(colourway):
    c = COLOURWAYS[colourway]

    def P(x, y):  # net mm -> SVG mm (y down)
        return f'{OX + x:.2f},{SHEET_H - (OY + y):.2f}'

    def poly(pts):
        return ' '.join(P(x, y) for x, y in pts)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET_W}mm" height="{SHEET_H}mm" '
           f'viewBox="0 0 {SHEET_W} {SHEET_H}">',
           '<title>Halloween treat gable box 100x60x100 - SRA3</title>',
           '<g id="Artwork">']
    # background with bleed: outline filled, stroked 2*bleed in the same colour
    out.append(f'<polygon points="{poly(outline())}" fill="{c["bg_rgb"]}" stroke="{c["bg_rgb"]}" '
               f'stroke-width="{2 * BLEED}" stroke-linejoin="round"/>')
    for kind, d in all_motifs():
        if kind == 'star':
            out.append(f'<polygon points="{poly(star(*d))}" fill="{c["star_rgb"]}"/>')
        elif kind == 'ghost':
            pts, h = ghost(*d)
            out.append(f'<polygon points="{poly(pts)}" fill="#FFFFFF"/>')
            cx, base, w = d
            for ex in (cx - w * 0.16, cx + w * 0.16):
                out.append(f'<ellipse cx="{OX + ex:.2f}" cy="{SHEET_H - (OY + base + h * 0.62):.2f}" '
                           f'rx="{w * 0.07:.2f}" ry="{w * 0.1:.2f}" fill="#141414"/>')
        elif kind == 'pumpkin':
            cx, cy, r = d
            for dx, rx in ((-r * 0.45, r * 0.6), (r * 0.45, r * 0.6), (0, r * 0.62)):
                out.append(f'<ellipse cx="{OX + cx + dx:.2f}" cy="{SHEET_H - (OY + cy):.2f}" rx="{rx:.2f}" '
                           f'ry="{r * 0.78:.2f}" fill="#F26522" stroke="#C1440E" stroke-width="0.3"/>')
            out.append(f'<rect x="{OX + cx - r * 0.08:.2f}" y="{SHEET_H - (OY + cy + r * 1.0):.2f}" '
                       f'width="{r * 0.16:.2f}" height="{r * 0.3:.2f}" fill="#2E7D32"/>')
            for ex in (-0.3, 0.3):
                tri = [(cx + r * ex - r * 0.12, cy + r * 0.1), (cx + r * ex + r * 0.12, cy + r * 0.1),
                       (cx + r * ex, cy + r * 0.32)]
                out.append(f'<polygon points="{poly(tri)}" fill="#141414"/>')
            mouth = [(cx - r * 0.4, cy - r * 0.2), (cx + r * 0.4, cy - r * 0.2), (cx, cy - r * 0.45)]
            out.append(f'<polygon points="{poly(mouth)}" fill="#141414"/>')
        elif kind == 'text':
            cx, cy, t, size = d
            out.append(f'<text x="{OX + cx:.2f}" y="{SHEET_H - (OY + cy):.2f}" font-family="Arial Rounded MT Bold, '
                       f'Arial Black, Arial, sans-serif" font-weight="bold" font-size="{size}" '
                       f'text-anchor="middle" fill="{c["text_rgb"]}">{t}</text>')
    out.append('</g>')
    out.append('<g id="CUT" fill="none" stroke-width="0.25">')
    out.append(f'<polygon points="{poly(outline())}" stroke="#FF0000"/>')
    for cx, cy, w, h in handle_holes():
        out.append(f'<rect x="{OX + cx - w / 2:.2f}" y="{SHEET_H - (OY + cy + h / 2):.2f}" width="{w}" height="{h}" '
                   f'rx="{h / 2}" stroke="#FF0000"/>')
    for (x1, y1), (x2, y2) in creases():
        out.append(f'<line x1="{OX + x1:.2f}" y1="{SHEET_H - (OY + y1):.2f}" x2="{OX + x2:.2f}" '
                   f'y2="{SHEET_H - (OY + y2):.2f}" stroke="#0000FF"/>')
    out.append('</g></svg>')
    return '\n'.join(out) + '\n'


# ----------------------------------------------------------------------------------------------------- PDF
def pdf(colourway, path, preview_name=None):
    c = COLOURWAYS[colourway]
    cv = canvas.Canvas(str(path), pagesize=(SHEET_W * mm, SHEET_H * mm), pageCompression=0)
    cv.setTitle(f'Halloween treat gable box 100x60x100 - {colourway} - SRA3')

    def T(x, y):
        return (OX + x) * mm, (OY + y) * mm

    def path_of(pts, close=True):
        p = cv.beginPath()
        p.moveTo(*T(*pts[0]))
        for q in pts[1:]:
            p.lineTo(*T(*q))
        if close:
            p.close()
        return p

    # Artwork
    cv.setFillColor(CMYKColor(*c['bg']))
    cv.setStrokeColor(CMYKColor(*c['bg']))
    cv.setLineWidth(2 * BLEED * mm)
    cv.setLineJoin(1)
    cv.drawPath(path_of(outline()), stroke=1, fill=1)
    for kind, d in all_motifs():
        if kind == 'star':
            cv.setFillColor(CMYKColor(*c['star']))
            cv.drawPath(path_of(star(*d)), stroke=0, fill=1)
        elif kind == 'ghost':
            pts, h = ghost(*d)
            cv.setFillColor(CMYKColor(0, 0, 0, 0))
            cv.drawPath(path_of(pts), stroke=0, fill=1)
            cx, base, w = d
            cv.setFillColor(CMYKColor(0.6, 0.4, 0.4, 1))
            for ex in (cx - w * 0.16, cx + w * 0.16):
                x, y = T(ex, base + h * 0.62)
                cv.ellipse(x - w * 0.07 * mm, y - w * 0.1 * mm, x + w * 0.07 * mm, y + w * 0.1 * mm, stroke=0, fill=1)
        elif kind == 'pumpkin':
            cx, cy, r = d
            cv.setFillColor(CMYKColor(0, 0.7, 0.95, 0))
            cv.setStrokeColor(CMYKColor(0, 0.75, 1, 0.2))
            cv.setLineWidth(0.3 * mm)
            for dx, rx in ((-r * 0.45, r * 0.6), (r * 0.45, r * 0.6), (0, r * 0.62)):
                x, y = T(cx + dx, cy)
                cv.ellipse(x - rx * mm, y - r * 0.78 * mm, x + rx * mm, y + r * 0.78 * mm, stroke=1, fill=1)
            cv.setFillColor(CMYKColor(0.8, 0.2, 1, 0.3))
            x, y = T(cx - r * 0.08, cy + r * 0.7)
            cv.rect(x, y, r * 0.16 * mm, r * 0.3 * mm, stroke=0, fill=1)
            cv.setFillColor(CMYKColor(0.6, 0.4, 0.4, 1))
            for ex in (-0.3, 0.3):
                tri = [(cx + r * ex - r * 0.12, cy + r * 0.1), (cx + r * ex + r * 0.12, cy + r * 0.1),
                       (cx + r * ex, cy + r * 0.32)]
                cv.drawPath(path_of(tri), stroke=0, fill=1)
            cv.drawPath(path_of([(cx - r * 0.4, cy - r * 0.2), (cx + r * 0.4, cy - r * 0.2), (cx, cy - r * 0.45)]),
                        stroke=0, fill=1)
        elif kind == 'text':
            cx, cy, t, size = d
            cv.setFillColor(CMYKColor(*c['text']))
            cv.setFont('Helvetica-Bold', size * mm / 0.3528 * 0.3528)  # size in mm -> points
            x, y = T(cx, cy - size * 0.35)
            cv.drawCentredString(x, y, t.replace('\u2019', "'"))
    # Cut lines (do not print: hide this layer when printing)
    cv.setLineWidth(0.25 * mm)
    cv.setStrokeColor(CMYKColor(*CUT_CMYK))
    cv.drawPath(path_of(outline()), stroke=1, fill=0)
    for cx, cy, w, h in handle_holes():
        x, y = T(cx - w / 2, cy - h / 2)
        cv.roundRect(x, y, w * mm, h * mm, h / 2 * mm, stroke=1, fill=0)
    cv.setStrokeColor(CMYKColor(*CREASE_CMYK))
    for a, b in creases():
        cv.line(*T(*a), *T(*b))
    cv.showPage()
    cv.save()
    # ReportLab's header comment has 4 high bytes; swap them for ASCII (same length, so offsets stay valid)
    # so the whole file is plain ASCII and can be saved to Dropbox as text.
    data = bytearray(Path(path).read_bytes())
    for i, b in enumerate(data[:64]):
        if b > 127:
            data[i] = ord('~')
    assert all(b < 128 for b in data), 'PDF is not plain ASCII'
    Path(path).write_bytes(bytes(data))


if __name__ == '__main__':
    out = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    out.mkdir(parents=True, exist_ok=True)
    for cw in COLOURWAYS:
        name = f'Halloween Treat Box - FOXY-CUT-HTBPO1-01 - {cw.title()} - SRA3'
        (out / f'{name}.svg').write_text(svg(cw))
        pdf(cw, out / f'{name}.pdf')
        print(name)
