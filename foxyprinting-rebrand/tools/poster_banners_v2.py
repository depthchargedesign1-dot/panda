#!/usr/bin/env python3
"""Celebrity Posters collection header banners, v2 (8 Oct 2026, evening).

Owner: "on the poster print header mockups the images youve used does not fill the frames, make sure you use
proper frames that we sell and fill the image". v1 drew its own frames and left a gap round the prints.

v2 uses the REAL frames from our own framed product photos (the store's 1500x1500 brick-wall template, the
same frames we sell): Black (Robbie_Williams-Black.jpg), Silver (COLUMBO_PETER-Silver.jpg), White
(Cristiano_Ronaldo-White.jpg) and Gold (THE_GREATEST_SHOWMAN___35102.jpg). Each frame is cut out of its photo as
a ring (outside and opening transparent), rotated for portrait prints, and scaled so its opening is exactly the
size of the print: the whole print fills the frame, edge to edge, with nothing drawn.

Picks, background, layout and shadow come from tools/poster_banners.py (v1).

Usage:  python3 -I tools/poster_banners_v2.py <download_dir> <frames_dir> <out_dir> [handle ...]
  frames_dir holds the four full-size frame photos above (curl from cdn.shopify.com).
"""
import math, os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poster_banners as v1  # noqa: E402

W, H = v1.W, v1.H

# Frame photos (1500x1500 template): opening (inner) and outer edge of the moulding, measured from the photos.
# The opening is taken 2 px larger than the real one, so none of the photo's old print shows at the edge, and the
# outer edge 2 px smaller, so none of the brick wall shows.
FRAME_PHOTOS = {
    'black': ('Robbie_Williams-Black.jpg', (240, 399, 1268, 1117), (171, 330, 1337, 1186)),
    'silver': ('COLUMBO_PETER-Silver.jpg', (234, 393, 1270, 1120), (163, 322, 1341, 1184)),
    'white': ('Cristiano_Ronaldo-White.jpg', (241, 400, 1266, 1112), (169, 329, 1338, 1184)),
    'gold': ('THE_GREATEST_SHOWMAN___35102.jpg', (242, 398, 1269, 1121), (171, 329, 1337, 1184)),
}
TEMPLATE_INNER = (241, 398, 1268, 1118)  # the print area inside any frame photo made from the same template

_rings = {}


def ring(frame, frames_dir):
    """The frame moulding as RGBA (landscape), plus the opening box inside it."""
    if frame in _rings:
        return _rings[frame]
    name, (il, it, ir, ib), (ol, ot, orr, ob) = FRAME_PHOTOS[frame]
    im = Image.open(os.path.join(frames_dir, name)).convert('RGB')
    ol, ot, orr, ob = ol + 2, ot + 2, orr - 2, ob - 2
    il, it, ir, ib = il - 2, it - 2, ir + 2, ib + 2
    piece = im.crop((ol, ot, orr, ob)).convert('RGBA')
    a = np.full((ob - ot, orr - ol), 255, np.uint8)
    a[it - ot:ib - ot, il - ol:ir - ol] = 0
    piece.putalpha(Image.fromarray(a))
    _rings[frame] = (piece, (il - ol, it - ot, ir - ol, ib - ot))
    return _rings[frame]


def is_template_photo(im):
    """True for a framed product photo made from the brick-wall template (wall top-left, wooden floor bottom)."""
    if im.width != im.height:
        return False
    a = np.asarray(im.convert('RGB').resize((150, 150))).astype(float)
    wall = a[5:25, 5:25]
    floor = a[135:148, 60:90].mean(axis=(0, 1))
    return wall.mean() > 170 and wall.std() > 8 and floor[0] > floor[2] + 25  # textured brick, wooden floor


def has_floor(im):
    """A product photo staged on a floor (any template): its print can't be cut out by trimming white."""
    a = np.asarray(im.convert('RGB').resize((150, 150))).astype(float)
    floor = a[135:148, 60:90].mean(axis=(0, 1))
    return floor[0] > floor[2] + 25


def print_art(path):
    """The flat print: the area inside the frame for template photos, else the image trimmed of its white margin."""
    im = Image.open(path).convert('RGB')
    if is_template_photo(im):
        s = im.width / 1500
        l, t, r, b = TEMPLATE_INNER
        return im.crop((int(l * s) + 3, int(t * s) + 3, int(r * s) - 3, int(b * s) - 3))
    a = np.asarray(im).astype(int)
    ink = a.max(axis=2) < 235
    rows = np.where(ink.mean(axis=1) > 0.05)[0]
    cols = np.where(ink.mean(axis=0) > 0.05)[0]
    if len(rows) and len(cols):
        im = im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    return im


def opening_after_rotation(box, size):
    """Opening box (l, t, r, b) of a landscape ring of `size` after PIL rotate(90, expand=True)."""
    w, h = size
    l, t, r, b = box
    # rotate(90) turns anticlockwise: a point (x, y) moves to (y, w - x)
    return (t, w - r, b, w - l)


def framed_v2(art, height, frame, frames_dir):
    piece, box = ring(frame, frames_dir)
    if art.height > art.width:
        box = opening_after_rotation(box, piece.size)
        piece = piece.rotate(90, expand=True)
    il, it, ir, ib = box
    ow, oh = ir - il, ib - it
    ph = int(round(height))
    pw = int(round(ph * art.width / art.height))
    sx, sy = pw / ow, ph / oh
    fr = piece.resize((int(round(piece.width * sx)), int(round(piece.height * sy))), Image.LANCZOS)
    out = Image.new('RGBA', fr.size, (0, 0, 0, 0))
    out.paste(art.resize((pw, ph), Image.LANCZOS).convert('RGBA'), (int(round(il * sx)), int(round(it * sy))))
    out.alpha_composite(fr)
    return out


FRAME_CYCLE = ['black', 'silver', 'gold', 'white', 'black', 'silver', 'gold']


def build(handle, dl_dir, frames_dir, out_dir, count=5):
    title, accent, rels = v1.PICKS[handle]
    arts = []
    for r in rels:
        im = Image.open(os.path.join(dl_dir, v1.local_name(r)))
        if not is_template_photo(im) and (has_floor(im) or any(k in r for k in ('Frame', 'FRAME', '-Black', '-Silver', '-White'))):
            continue  # a framed/staged photo from another template: its print can't be cut out cleanly, skip it
        arts.append(print_art(os.path.join(dl_dir, v1.local_name(r))))
        if len(arts) == count:
            break
    n = len(arts)
    canvas = v1.background(accent)

    def sizes(k):
        out = []
        for i, pr in enumerate(arts):
            ar = pr.width / pr.height
            area = 0.8 * (430 * k * v1.RANK_SCALE[i]) ** 2 * (1.45 if ar > 1.1 else 1.0)
            h = min(math.sqrt(area / ar), 400 * k * v1.RANK_SCALE[i])
            out.append((h, h * ar * 1.16))  # framed width: the moulding adds about 8% each side
        return out
    order = [r for r in range(n - 1, 0, -1) if r % 2 == 0] + [0] + [r for r in range(1, n) if r % 2 == 1]
    k = 1.0
    span = v1.REGION[1] - v1.REGION[0]
    while True:
        sz = sizes(k)
        widths = [sz[r][1] for r in order]
        total = sum(widths)
        covered = [widths[j] if order[j] > order[j + 1] else widths[j + 1] for j in range(n - 1)]
        f = max(0.0, (total - span) / max(1.0, sum(covered)))
        if f <= 0.40 or k < 0.6:
            break
        k -= 0.02
    ovs = [f * c for c in covered]
    x = v1.REGION[0] + max(0.0, (span - (total - sum(ovs))) / 2)
    centres = {}
    for j, (r, w) in enumerate(zip(order, widths)):
        centres[r] = x + w / 2
        x += w - (ovs[j] if j < n - 1 else 0)
    for r in sorted(range(n), key=lambda r: -r):
        h = sz[r][0]
        cy = 300 + (1 - v1.RANK_SCALE[r]) * 30
        v1.place(canvas, framed_v2(arts[r], h, FRAME_CYCLE[r], frames_dir), centres[r], cy, v1.RANK_ANGLE[r])
    fade = Image.new('L', (W, 1)); fade.putdata([int(max(0, 1 - x / 760) ** 1.6 * 150) for x in range(W)])
    fade = fade.resize((W, H))
    canvas = Image.composite(Image.new('RGBA', (W, H), v1.INK + (255,)), canvas, fade)
    out = os.path.join(out_dir, f'foxy-header-{handle}.jpg')
    canvas.convert('RGB').save(out, quality=88, optimize=True, progressive=True)
    return out


if __name__ == '__main__':
    dl_dir, frames_dir, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out_dir, exist_ok=True)
    v1.download(dl_dir)
    for h in (sys.argv[4:] or list(v1.PICKS)):
        print(build(h, dl_dir, frames_dir, out_dir))
