#!/usr/bin/env python3
"""Little Britain mask pack + pair: product shots, lifestyle composite and print/cut artwork.

Runs in the Higgsfield sandbox (it has internet; Claude's own sandbox can't reach Dropbox/CDNs).
Uses only the owner's existing mask artwork from Dropbox (no AI faces). The lifestyle image is an
AI-generated empty party table (no people, no faces) with the real mask artwork composited on top.

Usage (in the sandbox):
  python3 lb_build.py SRC_DIR OUT_DIR BG_PAIR_URL BG_PACK_URL
SRC_DIR holds lou.jpg, andy.jpg, vicky.jpg, bubbles.png (downloaded from Dropbox, see README.md).
"""
import os, sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageCms

SRC, OUT, BG_PAIR, BG_PACK = sys.argv[1:5]
os.makedirs(OUT, exist_ok=True)

# name, file, fallback eye centres (lx, ly, rx, ry) in source pixels, read off the artwork
MASKS = {
    "lou": ("Lou Todd", "lou.jpg", (256, 571, 556, 564)),
    "andy": ("Andy Pipkin", "andy.jpg", (1064, 1579, 1766, 1579)),
    "vicky": ("Vicky Pollard", "vicky.jpg", (772, 2140, 1591, 2140)),
    "bubbles": ("Bubbles DeVere", "bubbles.png", (92, 358, 206, 358)),
}
PRODUCTS = {
    "lou-and-andy-couple-mask-pair": dict(keys=["lou", "andy"], head="LOU & ANDY FACE MASK PAIR", bg=BG_PAIR),
    "little-britain-characters-face-mask-pack": dict(keys=["vicky", "lou", "andy", "bubbles"],
                                                      head="4 CHARACTER FACE MASK PACK", bg=BG_PACK),
}

fonts = [l.split(":")[0] for l in subprocess.run(["fc-list"], capture_output=True, text=True).stdout.splitlines()]
FB = next((f for f in fonts if "Montserrat-Bold" in f), None) or next(f for f in fonts if "Bold" in f)
FR = next((f for f in fonts if "Montserrat-Regular" in f), FB)


def load_rgb(path):
    im = Image.open(path)
    if im.mode == "CMYK":  # Vicky's artwork is CMYK
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
    if L and R:  # detection agrees with the artwork estimate -> use the detected centres
        l = min(L, key=lambda p: math.hypot(p[0] - lx, p[1] - ly)); r = min(R, key=lambda p: math.hypot(p[0] - rx, p[1] - ry))
        return (int(l[0]), int(l[1]), int(r[0]), int(r[1]))
    return fallback


def cutout(key):
    name, fn, fb = MASKS[key]
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
    print(key, "eyes", eyes, "fallback" if eyes == fb else "detected")
    return im.crop(a.getbbox()), name


def edge(l, t=7, shadow=90):
    A = l.getchannel("A"); p = 80
    out = Image.new("RGBA", (l.width + 2 * p, l.height + 2 * p), (0, 0, 0, 0)); sh = out.copy()
    s = Image.new("RGBA", l.size, (0, 0, 0, shadow)); s.putalpha(A.point(lambda v: v * shadow // 255)); sh.paste(s, (p + 18, p + 26), s)
    out = Image.alpha_composite(out, sh.filter(ImageFilter.GaussianBlur(22)))
    e = Image.new("RGBA", l.size, (205, 203, 198, 255)); e.putalpha(A)
    for i in range(t, 0, -1):
        out.paste(e, (p + i, p + i), e)
    out.paste(l, (p, p), l); return out


def fit(l, bw, bh):
    s = min(bw / l.width, bh / l.height); return l.resize((max(1, int(l.width * s)), max(1, int(l.height * s))), Image.LANCZOS)


def place(bg, l, cx, cy):
    bg.alpha_composite(l, (int(cx - l.width / 2), int(cy - l.height / 2)))


def lab(d, xy, t, sz, bold=True, fill=(20, 20, 20), anchor="la"):
    d.text(xy, t, font=ImageFont.truetype(FB if bold else FR, sz), fill=fill, anchor=anchor)


def back_of(front):
    b = Image.new("RGBA", front.size, (250, 250, 247, 0)); b.putalpha(front.getchannel("A")); b = ImageOps.mirror(b)
    d = ImageDraw.Draw(b); w, h = b.size; ey = int(h * 0.42); tab = int(w * 0.09)
    for tx in (int(w * .10), int(w * .90) - tab):
        d.rounded_rectangle((tx, ey - tab // 2, tx + tab, ey + tab // 2), radius=8, fill=(236, 240, 244, 255), outline=(170, 178, 186, 255), width=3)
    x0, x1 = int(w * .10) + tab // 2, int(w * .90) - tab // 2
    pts = [(x0 + (x1 - x0) * t, ey + h * .38 * (1 - (2 * t - 1) ** 2)) for t in [i / 60 for i in range(61)]]
    d.line([(x + 6, y + 8) for x, y in pts], fill=(200, 200, 196, 255), width=max(6, w // 90), joint="curve")
    d.line(pts, fill=(25, 25, 25, 255), width=max(5, w // 100), joint="curve")
    return b


def grid_positions(n, W, H, top, bottom):
    if n == 2:
        return [(W * 0.27, (top + H - bottom) / 2), (W * 0.73, (top + H - bottom) / 2)], (W * 0.46, H - top - bottom)
    cy1, cy2 = top + (H - top - bottom) * 0.26, top + (H - top - bottom) * 0.74
    return [(W * .27, cy1), (W * .73, cy1), (W * .27, cy2), (W * .73, cy2)], (W * 0.46, (H - top - bottom) * 0.48)


faces = {k: cutout(k) for k in MASKS}
W8 = (255, 255, 255, 255)
for slug, P in PRODUCTS.items():
    ms = [faces[k] for k in P["keys"]]; n = len(ms)
    # 1. hero, portrait 1240x1754
    bg = Image.new("RGBA", (1240, 1754), W8); d = ImageDraw.Draw(bg)
    lab(d, (620, 60), P["head"], 50, anchor="ma")
    pos, (bw, bh) = grid_positions(n, 1240, 1754, 150, 90)
    for (f, nm), (x, y) in zip(ms, pos):
        place(bg, fit(edge(f), bw, bh - 50), x, y - 20); lab(d, (x, y + (bh - 50) / 2 - 10), nm.upper(), 30, fill=(90, 90, 90), anchor="ma")
    lab(d, (620, 1700), "Unofficial fan-made novelty masks", 26, bold=False, fill=(120, 120, 120), anchor="ma")
    bg.convert("RGB").save(f"{OUT}/{slug}-mask-01.jpg", quality=93)
    # 2. back of the first mask
    f0 = ms[0][0]; b0 = back_of(f0)
    bg = Image.new("RGBA", (2000, 2000), (244, 244, 242, 255)); place(bg, fit(edge(b0), 1700, 1650), 1000, 1080)
    lab(ImageDraw.Draw(bg), (1000, 110), "REVERSE: ELASTIC + STICKY TABS FITTED", 58, anchor="ma")
    bg.convert("RGB").save(f"{OUT}/{slug}-02-back.jpg", quality=93)
    # 3. front + back with spec bullets
    bg = Image.new("RGBA", (2000, 2000), W8); d = ImageDraw.Draw(bg); lab(d, (1000, 70), P["head"], 64, anchor="ma")
    place(bg, fit(edge(f0), 900, 1150), 510, 830); place(bg, fit(edge(b0), 900, 1150), 1490, 830)
    lab(d, (510, 1430), "FRONT", 44, fill=(90, 90, 90), anchor="ma"); lab(d, (1490, 1430), "BACK", 44, fill=(90, 90, 90), anchor="ma")
    for i, t in enumerate(["350gsm silk card - digitally printed", "A4 size, eye holes pre-cut", "Elastic + sticky tabs fitted", "Semi-waterproof - wear outdoors"]):
        x = 170 if i % 2 == 0 else 1050; y = 1540 if i < 2 else 1690
        d.ellipse((x, y + 8, x + 36, y + 44), fill=(230, 57, 70)); lab(d, (x + 56, y), t, 40, bold=False)
    bg.convert("RGB").save(f"{OUT}/{slug}-03-front-back.jpg", quality=93)
    # 4. lifestyle: real mask artwork laid on an AI-generated empty party table
    subprocess.run(["curl", "-sfo", f"{OUT}/bg-{slug}.png", P["bg"]], check=True)
    life = Image.open(f"{OUT}/bg-{slug}.png").convert("RGBA").resize((2000, 2000), Image.LANCZOS)
    angles = [-9, 7] if n == 2 else [-10, 6, -4, 9]
    lpos = [(700, 1020), (1300, 1000)] if n == 2 else [(620, 690), (1380, 700), (640, 1340), (1360, 1330)]
    size = (780, 1050) if n == 2 else (680, 620)
    for (f, nm), (x, y), ang in zip(ms, lpos, angles):
        m = edge(fit(f, *size), t=5, shadow=140).rotate(ang, resample=Image.BICUBIC, expand=True)
        place(life, m, x, y)
    life.convert("RGB").save(f"{OUT}/{slug}-04-party.jpg", quality=92)
    # check sheet (for review only)
    cs = Image.new("RGB", (1600, 560), "white")
    for i, fn in enumerate(["mask-01", "02-back", "03-front-back", "04-party"]):
        t = Image.open(f"{OUT}/{slug}-{fn}.jpg"); t.thumbnail((390, 550)); cs.paste(t, (i * 400 + 5, 5))
    cs.save(f"{OUT}/{slug}-check.jpg", quality=70)

# print artwork sources for mask_cutline.py (white background, sRGB)
os.makedirs(f"{OUT}/art", exist_ok=True)
for k, (name, fn, _) in MASKS.items():
    rgb, _ = load_rgb(os.path.join(SRC, fn)); rgb.save(f"{OUT}/art/{name}.jpg", quality=97)
print("OK")
