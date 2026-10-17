#!/usr/bin/env python3
"""Main (first) product image for the Little Britain multi-mask listings (6 Oct 2026).

Owner's rule: any product with 2+ masks has, as its first image, the masks side by side on a clean
background with NO text, logos or badges. Uses the same Dropbox artwork and the same cut-out method
as lb_build.py (flood fill from the border, or the PNG's alpha; eye holes cut at the detected eye centres).

Usage (Higgsfield sandbox):  python3 lb_main_image.py SRC_DIR OUT_DIR
SRC_DIR holds lou.jpg, andy.jpg, vicky.jpg, bubbles.png. Writes 2048x2048 JPEGs:
  OUT_DIR/lou-and-andy-couple-mask-pair-main.jpg
  OUT_DIR/little-britain-characters-face-mask-pack-main.jpg
Dropbox sources (see README.md):
  /2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES/2026 TV SHOWS AND STARS/Lou - Little Britain (larger).jpg
  /2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES/2026 TV SHOWS AND STARS/andy pipkins.jpg
  /2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES/2026 ! DUPLICATES TO CHECK/Vicky Pollard.jpg
  /2019 tidy - celebrity facemasks png jpegs only missing some/WOMEN PNG NO BACKGROUND/ Bubbles de vere.png
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

SRC, OUT = sys.argv[1:3]
os.makedirs(OUT, exist_ok=True)
S = 2048
BG = (246, 246, 244, 255)  # very light warm grey

# name, file, fallback eye centres (lx, ly, rx, ry) in source pixels (same as lb_build.py)
MASKS = {
    "lou": ("lou.jpg", (256, 571, 556, 564)),
    "andy": ("andy.jpg", (1064, 1579, 1766, 1579)),
    "vicky": ("vicky.jpg", (772, 2140, 1591, 2140)),
    "bubbles": ("bubbles.png", (95, 300, 205, 300)),
}


def load_rgb(path):
    im = Image.open(path)
    if im.mode == "CMYK":
        im = im.convert("RGB")
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        return Image.alpha_composite(bg, im).convert("RGB"), im.getchannel("A")
    return im.convert("RGB"), None


def detect_eyes(rgb, fallback):
    try:
        import cv2
    except ImportError:
        return fallback
    g = cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2GRAY)
    h, w = g.shape
    found = []
    for name in ("haarcascade_eye_tree_eyeglasses.xml", "haarcascade_eye.xml"):
        E = cv2.CascadeClassifier(cv2.data.haarcascades + name).detectMultiScale(g, 1.05, 5, minSize=(w // 16, w // 16), maxSize=(w // 3, w // 3))
        found += [(x + a / 2, y + b / 2) for x, y, a, b in E]
    lx, ly, rx, ry = fallback
    tol = 0.07 * w
    L = [p for p in found if math.hypot(p[0] - lx, p[1] - ly) < tol]
    R = [p for p in found if math.hypot(p[0] - rx, p[1] - ry) < tol]
    if L and R:
        l = min(L, key=lambda p: math.hypot(p[0] - lx, p[1] - ly)); r = min(R, key=lambda p: math.hypot(p[0] - rx, p[1] - ry))
        return (int(l[0]), int(l[1]), int(r[0]), int(r[1]))
    return fallback


def cutout(key):
    fn, fb = MASKS[key]
    rgb, a = load_rgb(os.path.join(SRC, fn))
    if a is None:  # white background -> flood fill from the border
        arr = np.asarray(rgb).astype(int)
        m = Image.fromarray((arr.min(axis=2) < 242).astype(np.uint8) * 255, "L")
        m = ImageOps.expand(m, 4, 0).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
        ImageDraw.floodfill(m, (0, 0), 128)
        a = Image.fromarray(np.where(np.asarray(m) == 128, 0, 255).astype(np.uint8)[4:-4, 4:-4], "L")
    eyes = detect_eyes(rgb, fb)
    bb = a.getbbox(); r = int((bb[2] - bb[0]) * 0.034)
    d = ImageDraw.Draw(a)
    for x, y in ((eyes[0], eyes[1]), (eyes[2], eyes[3])):
        d.ellipse((x - r, y - r, x + r, y + r), fill=0)
    a = a.point(lambda v: 255 if v > 128 else 0).filter(ImageFilter.GaussianBlur(1.2))
    im = rgb.convert("RGBA"); im.putalpha(a)
    print(key, "eyes", eyes, "fallback" if eyes == fb else "detected", "size", rgb.size)
    return im.crop(a.getbbox())


def to_height(l, h):
    return l.resize((max(1, round(l.width * h / l.height)), h), Image.LANCZOS)


def put(bg, l, cx, cy):
    """Paste a mask centred on (cx, cy) with a thin card edge and a soft drop shadow."""
    A = l.getchannel("A"); x, y = int(cx - l.width / 2), int(cy - l.height / 2)
    sh = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    s = Image.new("RGBA", l.size, (40, 40, 40, 255)); s.putalpha(A.point(lambda v: v * 70 // 255))
    sh.paste(s, (x + 14, y + 22), s)
    bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
    e = Image.new("RGBA", l.size, (214, 212, 207, 255)); e.putalpha(A)
    for i in (4, 3, 2, 1):  # card thickness
        bg.alpha_composite(e, (x + i, y + i))
    bg.alpha_composite(l, (x, y))


def compose(keys, rows, out):
    faces = [cutout(k) for k in keys]
    bg = Image.new("RGBA", (S, S), BG)
    margin, gap = 150, 90
    n = len(faces) // rows
    per_row = [faces[r * n:(r + 1) * n] for r in range(rows)]
    # one common height for every mask, as large as fits both width and height
    max_h_rows = (S - 2 * margin - gap * (rows - 1)) / rows
    max_h_width = min((S - 2 * margin - gap * (len(row) - 1)) / sum(f.width / f.height for f in row) for row in per_row)
    h = int(min(max_h_rows, max_h_width))
    block_h = rows * h + (rows - 1) * gap
    y0 = (S - block_h) / 2
    for r, row in enumerate(per_row):
        rs = [to_height(f, h) for f in row]
        total = sum(f.width for f in rs) + gap * (len(rs) - 1)
        x = (S - total) / 2
        cy = y0 + r * (h + gap) + h / 2
        for f in rs:
            put(bg, f, x + f.width / 2, cy); x += f.width + gap
    bg.convert("RGB").save(out, quality=92, optimize=True)
    print("wrote", out, "mask height", h)


compose(["lou", "andy"], 1, f"{OUT}/lou-and-andy-couple-mask-pair-main.jpg")
compose(["vicky", "lou", "andy", "bubbles"], 2, f"{OUT}/little-britain-characters-face-mask-pack-main.jpg")
print("OK")
