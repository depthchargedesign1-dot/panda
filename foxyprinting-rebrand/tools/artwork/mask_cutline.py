#!/usr/bin/env python3
"""Face mask cut file: face image -> SRA4 print + cut file for the Intec ColorCut.

For each face image (cut-out face on a white background, like the celebrity mask artwork):
  1. Places the image in a 210 x 297 mm (A4) area, centred on an SRA4 sheet (225 x 320 mm, portrait).
     The image keeps its proportions (it is fitted inside the A4 area, never stretched).
  2. Traces the face outline and draws a MAGENTA cut line about 2 mm inside it.
  3. Finds the eyes and draws a magenta cut line for each eye hole, so the wearer can see out.
  4. Writes "<name>.pdf" and "<name>.svg" (same name as the image) (cut lines on their own layer "CUT"),
     plus "<name> - check.png", a preview to check the eye holes before cutting.

Cut line: magenta RGB 255,0,255 / CMYK 0,100,0,0, 0.1 mm stroke, no fill (owner's spec, 5 Oct 2026).

Usage:
  python3 mask_cutline.py face1.jpg [face2.png ...] [--out DIR] [--inset 2] [--stroke 0.1]
Needs: pip install numpy "opencv-python-headless<5" reportlab pikepdf
"""
import argparse
import base64
import os
import sys

import cv2
import numpy as np
from reportlab.lib.colors import CMYKColor
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

SHEET_W, SHEET_H = 225.0, 320.0  # SRA4 portrait, mm
AREA_W, AREA_H = 210.0, 297.0    # A4 mask area, mm
MAGENTA_CMYK = CMYKColor(0, 1, 0, 0)
MAGENTA_HEX = '#FF00FF'


def face_mask(img):
    """Binary mask of the face: everything that isn't white background, holes filled."""
    diff = 255 - img.min(axis=2)  # 0 on pure white
    fg = (cv2.GaussianBlur(diff, (5, 5), 0) > 18).astype(np.uint8) * 255
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not cnts:
        raise ValueError('no face found (is the background white?)')
    big = max(cnts, key=cv2.contourArea)
    filled = np.zeros_like(fg)
    cv2.drawContours(filled, [big], -1, 255, -1)  # fills teeth, eye whites etc.
    return filled


def inset_contour(mask, inset_px):
    """Outline `inset_px` inside the mask edge, smoothed."""
    dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)
    inner = (dist > inset_px).astype(np.uint8) * 255
    inner = cv2.GaussianBlur(inner, (0, 0), max(2, inset_px * 0.6))
    inner = (inner > 127).astype(np.uint8) * 255
    cnts, _ = cv2.findContours(inner, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cnts, key=cv2.contourArea)
    return cv2.approxPolyDP(c, 1.0, True)[:, 0, :].astype(float)


def find_eyes(img):
    """Return [(cx, cy, w)] for the two eyes in image pixels (left then right)."""
    g = cv2.equalizeHist(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    h, w = g.shape
    cf = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = cf.detectMultiScale(g, 1.1, 5, minSize=(w // 4, w // 4))
    if len(faces):
        fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])
    else:  # fall back to the face outline's bounding box
        fx, fy, fw, fh = cv2.boundingRect(cv2.findNonZero(face_mask(img)))
    cands = []
    for name in ('haarcascade_eye_tree_eyeglasses.xml', 'haarcascade_eye.xml'):
        cc = cv2.CascadeClassifier(cv2.data.haarcascades + name)
        for (x, y, ew, eh) in cc.detectMultiScale(g, 1.05, 5, minSize=(fw // 10, fw // 10), maxSize=(fw // 3, fw // 3)):
            cx, cy = x + ew / 2, y + eh / 2
            if fy + 0.15 * fh < cy < fy + 0.55 * fh and fx < cx < fx + fw:
                cands.append((cx, cy, ew))
        left = [c for c in cands if c[0] < fx + fw / 2]
        right = [c for c in cands if c[0] >= fx + fw / 2]
        if left and right:
            l, r = max(left, key=lambda c: c[2]), max(right, key=lambda c: c[2])
            if abs(l[1] - r[1]) < 0.12 * fh:
                return [l, r], (fx, fy, fw, fh)
    # Fallback: typical eye positions inside the face box.
    ey, ew = fy + 0.40 * fh, 0.17 * fw
    return [(fx + 0.30 * fw, ey, ew), (fx + 0.70 * fw, ey, ew)], (fx, fy, fw, fh)


def refine_eye(img, cx, cy, size):
    """Move the eye centre onto the iris (darkest area near the detected centre)."""
    g = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (0, 0), size * 0.06)
    r = int(size * 0.3)
    x0, y0 = int(max(cx - r, 0)), int(max(cy - r * 0.6, 0))
    roi = g[y0:int(cy + r * 0.6), x0:int(cx + r)]
    if roi.size == 0:
        return cx, cy
    _, _, (mx, my), _ = cv2.minMaxLoc(roi)
    nx, ny = x0 + mx, y0 + my
    # Don't let a dark lash line or brow pull it far away.
    if abs(nx - cx) > r * 0.7 or abs(ny - cy) > r * 0.5:
        return cx, cy
    return (cx + nx) / 2, (cy + ny) / 2


def eye_hole(cx, cy, w_px, h_px, n=48):
    """Almond eye hole (pointed ends, round middle), as a closed point list."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    x = cx + (w_px / 2) * np.cos(t)
    y = cy + (h_px / 2) * np.sin(t) * (0.55 + 0.45 * np.abs(np.sin(t)))
    return np.stack([x, y], axis=1)


def bezier_segments(pts):
    """Closed Catmull-Rom spline through pts -> list of cubic Bezier segments."""
    n = len(pts)
    segs = []
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        segs.append((p1, p1 + (p2 - p0) / 6.0, p2 - (p3 - p1) / 6.0, p2))
    return segs


def add_pdf_layers(pdf_path):
    """Register the "Artwork" and "CUT" layers (optional content groups) in the PDF."""
    import pikepdf
    with pikepdf.open(pdf_path, allow_overwriting_input=True) as pdf:
        ocgs = {n: pdf.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.OCG, Name=n)) for n in ('Artwork', 'CUT')}
        order = pikepdf.Array([ocgs['Artwork'], ocgs['CUT']])
        pdf.Root.OCProperties = pikepdf.Dictionary(OCGs=order, D=pikepdf.Dictionary(Order=order, ON=order, Name='Layers'))
        for page in pdf.pages:
            res = page.obj.Resources
            res.Properties = pikepdf.Dictionary({'/Artwork': ocgs['Artwork'], '/CUT': ocgs['CUT']})
        pdf.save(pdf_path)


def process(path, out_dir, inset_mm, stroke_mm, eye_w_mm, eye_h_mm, eye_override=None):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError('cannot read image')
    ih, iw = img.shape[:2]
    scale = min(AREA_W / iw, AREA_H / ih)  # mm per pixel, image fitted in the A4 area
    pw, ph = iw * scale, ih * scale
    ox, oy = (SHEET_W - pw) / 2, (SHEET_H - ph) / 2  # top-left of image on the sheet, mm

    # Pad with white so a face that touches the photo edge still gets the inset there.
    pad = int(inset_mm / scale) + 10
    padded = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    outline = inset_contour(face_mask(padded), inset_mm / scale) - pad
    holes = []
    if eye_override:  # eye centres given by hand (lx, ly, rx, ry in image pixels): use them as they are
        lx, ly, rx, ry = eye_override
        for (cx, cy) in ((lx, ly), (rx, ry)):
            holes.append(eye_hole(cx, cy, eye_w_mm / scale, eye_h_mm / scale))
    else:
        eyes, _ = find_eyes(img)
        for (cx, cy, ew) in eyes:
            cx, cy = refine_eye(img, cx, cy, ew)
            holes.append(eye_hole(cx, cy, eye_w_mm / scale, eye_h_mm / scale))

    def to_mm(pts):  # image px -> sheet mm (origin top-left, y down)
        return np.stack([ox + pts[:, 0] * scale, oy + pts[:, 1] * scale], axis=1)

    shapes = [to_mm(outline)] + [to_mm(h) for h in holes]
    base = os.path.splitext(os.path.basename(path))[0]
    os.makedirs(out_dir, exist_ok=True)

    # PDF
    pdf_path = os.path.join(out_dir, f'{base}.pdf')
    c = canvas.Canvas(pdf_path, pagesize=(SHEET_W * mm, SHEET_H * mm))
    c.setTitle(f'{base} - face mask SRA4 with cut line')
    c._code.append('/OC /Artwork BDC')  # PDF layer "Artwork"
    c.drawImage(path, ox * mm, (SHEET_H - oy - ph) * mm, pw * mm, ph * mm)
    c._code.append('EMC')
    c._code.append('/OC /CUT BDC')  # PDF layer "CUT" (owner's rule: cut lines on their own layer called CUT)
    c.setStrokeColor(MAGENTA_CMYK)
    c.setLineWidth(stroke_mm * mm)
    for s in shapes:
        p = c.beginPath()
        segs = bezier_segments(s)
        f = lambda q: (q[0] * mm, (SHEET_H - q[1]) * mm)
        p.moveTo(*f(segs[0][0]))
        for (_, c1, c2, e) in segs:
            p.curveTo(*f(c1), *f(c2), *f(e))
        p.close()
        c.drawPath(p, stroke=1, fill=0)
    c._code.append('EMC')
    c.showPage()
    c.save()
    add_pdf_layers(pdf_path)

    # SVG (opens in Illustrator; image embedded, cut lines in their own group)
    with open(path, 'rb') as fh:
        data = base64.b64encode(fh.read()).decode()
    mime = 'image/png' if path.lower().endswith('.png') else 'image/jpeg'
    d_list = []
    for s in shapes:
        segs = bezier_segments(s)
        d = 'M%.3f,%.3f ' % tuple(segs[0][0])
        d += ' '.join('C%.3f,%.3f %.3f,%.3f %.3f,%.3f' % (*c1, *c2, *e) for (_, c1, c2, e) in segs)
        d_list.append(d + ' Z')
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{SHEET_W}mm" height="{SHEET_H}mm" viewBox="0 0 {SHEET_W} {SHEET_H}">',
        f'<g id="Artwork"><image x="{ox:.3f}" y="{oy:.3f}" width="{pw:.3f}" height="{ph:.3f}" '
        f'xlink:href="data:{mime};base64,{data}"/></g>',
        '<g id="CUT">',
    ]
    for d in d_list:
        svg.append(f'<path d="{d}" fill="none" stroke="{MAGENTA_HEX}" stroke-width="{stroke_mm}"/>')
    svg += ['</g>', '</svg>']
    svg_path = os.path.join(out_dir, f'{base}.svg')
    with open(svg_path, 'w') as fh:
        fh.write('\n'.join(svg))

    # Check preview (sheet at 4 px/mm)
    k = 4
    prev = np.full((int(SHEET_H * k), int(SHEET_W * k), 3), 255, np.uint8)
    small = cv2.resize(img, (int(pw * k), int(ph * k)), interpolation=cv2.INTER_AREA)
    y0, x0 = int(oy * k), int(ox * k)
    prev[y0:y0 + small.shape[0], x0:x0 + small.shape[1]] = small
    for s in shapes:
        cv2.polylines(prev, [np.round(s * k).astype(np.int32)], True, (255, 0, 255), 2, cv2.LINE_AA)
    cv2.rectangle(prev, (0, 0), (prev.shape[1] - 1, prev.shape[0] - 1), (180, 180, 180), 1)
    png_path = os.path.join(out_dir, f'{base} - check.png')
    cv2.imwrite(png_path, prev)
    return pdf_path, svg_path, png_path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('images', nargs='+')
    ap.add_argument('--out', default='mask-cut-files')
    ap.add_argument('--inset', type=float, default=2.0, help='cut line distance inside the face edge, mm')
    ap.add_argument('--stroke', type=float, default=0.1, help='cut line width, mm')
    ap.add_argument('--eye-w', type=float, default=26.0, help='eye hole width, mm')
    ap.add_argument('--eye-h', type=float, default=11.0, help='eye hole height, mm')
    ap.add_argument('--eyes-json', help='JSON file {"<image name without extension>": [lx, ly, rx, ry]} to set eye centres by hand')
    a = ap.parse_args()
    import json
    overrides = json.load(open(a.eyes_json)) if a.eyes_json else {}
    bad = 0
    for p in a.images:
        try:
            out = process(p, a.out, a.inset, a.stroke, a.eye_w, a.eye_h,
                          overrides.get(os.path.splitext(os.path.basename(p))[0]))
            print('OK  ', p, '->', ', '.join(os.path.basename(o) for o in out))
        except Exception as e:  # keep going through a batch
            bad += 1
            print('FAIL', p, e, file=sys.stderr)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
