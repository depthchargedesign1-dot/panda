"""Put a sublimation wrap onto a REAL photo of a blank 11oz mug (owner's rule: no CAD mockups).

Base photo: Dropbox /RANDOM IMAGES LEFT ON/MUG BLANK.jpg (1500 x 1500, handle on the right).
The wrap (200 x 70 mm trim PNG) is bent round the photographed cylinder, then the photo's own
shading and gloss highlights are put back on top so it looks printed, not pasted.

  python3 real_mug_mockup.py <mug_blank.jpg> <wrap.png> <out.jpg> [--side left|right]
  side right = photo as shot (handle right, shows the END of the wrap)
  side left  = photo mirrored (handle left, shows the START of the wrap - band end of a plate)
  side front = handle retouched out (handle behind), shows the MIDDLE of the wrap
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter

# Geometry measured on MUG BLANK.jpg (pixels, 1500 px photo)
CX, R = 708.0, 333.0               # body centre x, radius
TOP_EDGE, TOP_B = 290.0, 20.0      # top rim: y at the sides, + depth of the front curve
BOT_EDGE, BOT_B = 1210.0, 43.0     # bottom: y at the sides, + depth of the front curve
MUG_H_MM = 96.0                    # body height the photo spans (top lip to base)
CIRC_MM = np.pi * 2 * R * MUG_H_MM / ((BOT_EDGE + BOT_B) - (TOP_EDGE + TOP_B))
WRAP_W, WRAP_H = 200.0, 70.0       # print area (trim)
GAP = CIRC_MM - WRAP_W             # unprinted strip at the handle
TEXT_MID = 114.5                   # middle of the plate text area on the wrap (mm) - faces you in the front view


def render(photo, wrap, side="right"):
    img = Image.open(photo).convert("RGB")
    if side == "left":
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    cx = CX if side != "left" else img.width - 1 - CX
    P = np.asarray(img).astype(np.float32) / 255.0
    if side == "front":  # handle turned to the back: retouch it out with the photo's own background
        x0 = int(cx + R + 3)
        src = np.clip((2 * cx - np.arange(x0, P.shape[1])).astype(int), 0, P.shape[1] - 1)
        P = P.copy()
        P[:, x0:] = P[:, src]
    w = Image.open(wrap).convert("RGBA")
    bg = Image.new("RGBA", w.size, (255, 255, 255, 255))
    T = np.asarray(Image.alpha_composite(bg, w).convert("RGB")).astype(np.float32) / 255.0
    th, tw_ = T.shape[:2]
    H, W = P.shape[:2]
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    s = (xs - cx) / R
    inside_x = np.abs(s) < 0.995
    sc = np.clip(s, -0.995, 0.995)
    curve = np.sqrt(1 - sc ** 2)
    ytop = TOP_EDGE + TOP_B * curve
    ybot = BOT_EDGE + BOT_B * curve
    t_mm = (ys - ytop) / (ybot - ytop) * MUG_H_MM          # height down the mug wall
    arc = np.arcsin(sc) * CIRC_MM / (2 * np.pi)             # mm round the wall from the front
    quarter = CIRC_MM / 4
    if side == "right":   # handle at +quarter, wrap ends GAP/2 before it
        u = arc + (WRAP_W - (quarter - GAP / 2))
    elif side == "left":  # handle at -quarter, wrap starts GAP/2 after it
        u = arc + (quarter - GAP / 2)
    else:                 # front: handle straight behind, middle of the wrap faces you
        u = arc + TEXT_MID
    v = t_mm - (MUG_H_MM - WRAP_H) / 2
    m = inside_x & (u >= 0) & (u < WRAP_W) & (v >= 0) & (v < WRAP_H)
    tx = np.clip((u / WRAP_W * tw_).astype(int), 0, tw_ - 1)
    ty = np.clip((v / WRAP_H * th).astype(int), 0, th - 1)
    tex = T[ty, tx]
    L = P.mean(axis=2)
    # photo shading: normalise by the bright body level, keep it gentle
    shade = np.clip(L / 0.965, 0, 1.03)[..., None]
    # foreshortening darkens the edges slightly more on a printed (non-white) surface
    edge = (0.86 + 0.14 * curve)[..., None]
    out = tex * shade * edge
    # gloss: put the photo's bright highlights back over the print
    blur = np.asarray(Image.fromarray((L * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(25))) / 255.0
    hl = np.clip((L - blur) * 6 + (L - 0.975) * 14, 0, 0.55)[..., None]
    out = out * (1 - hl) + hl
    # soft mask edges (anti-alias, ~1.5 px)
    mk = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    a = (np.asarray(mk).astype(np.float32) / 255.0)[..., None]
    res = P * (1 - a) + np.clip(out, 0, 1) * a
    im = Image.fromarray((res * 255 + 0.5).astype(np.uint8))
    if side == "front":  # square crop round the mug, inside the retouched area
        half = int(R + 275)
        im = im.crop((int(cx - half), 150, int(cx + half), 150 + 2 * half))
    return im


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("photo"); ap.add_argument("wrap"); ap.add_argument("out")
    ap.add_argument("--side", default="right", choices=["left", "right", "front"])
    a = ap.parse_args()
    render(a.photo, a.wrap, a.side).save(a.out, quality=92)
