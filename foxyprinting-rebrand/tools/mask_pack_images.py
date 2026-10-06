"""Main images for celebrity face mask packs and pairs (6 Oct 2026).

Owner's rule: for any product with 2+ masks the first image shows the masks side by side on a clean
background with NO text. Faces come from the single masks' own website images (cdn.shopify.com) or the
owner's Dropbox mask artwork; nothing is generated.

Usage: python3 -I tools/mask_pack_images.py <src_dir> <out_dir>
  <src_dir> holds the single-mask images named as in PACKS below.
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageFilter

SIZE = 2048
BG = (246, 244, 241)  # very light warm grey, clean studio look

PACKS = {
    # name: rows of (file, soft_edge) back row first; heights in px
    "bts-face-masks-5-pack-party-set": dict(rows=[["jimin-bts-face-mask.jpg", "v-kim-taehyung-bts-face-mask.jpg",
                                                   "rm-kim-namjoon-bts-face-mask.jpg"],
                                                  ["suga-min-yoongi-bts-face-mask.jpg", "j-hope-jung-hoseok-bts-face-mask.jpg"]],
                                            h=900, soft={"jimin-bts-face-mask.jpg"}),
    "liam-and-noel-gallagher-face-masks-brothers-pair": dict(rows=[["liam.jpg", "noel_a.jpg"]], h=1180, soft=set()),
    "travis-kelce-and-taylor-swift-couple-face-mask-pair": dict(rows=[["travis.jpg", "taylor.png"]], h=1180, soft=set()),
}


def load_rgb(path):
    im = Image.open(path)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg
    return cv2.cvtColor(np.array(im.convert("RGB")), cv2.COLOR_RGB2BGR)


def face_alpha(img, soft=False):
    diff = 255 - img.min(axis=2)
    k, t, c = ((9, 11, 45) if soft else (5, 18, 9))
    fg = (cv2.GaussianBlur(diff, (k, k), 0) > t).astype(np.uint8) * 255
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((c, c), np.uint8))
    cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    big = max(cnts, key=cv2.contourArea)
    filled = np.zeros_like(fg)
    cv2.drawContours(filled, [big], -1, 255, -1)
    if soft:
        filled = cv2.GaussianBlur(filled, (0, 0), 9)
        filled = ((filled > 127) * 255).astype(np.uint8)
    return cv2.GaussianBlur(filled, (0, 0), 1.2)


def cutout(path, height, soft):
    img = load_rgb(path)
    a = face_alpha(img, soft)
    ys, xs = np.where(a > 10)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([cv2.cvtColor(img, cv2.COLOR_BGR2RGB), a])[y0:y1, x0:x1]
    im = Image.fromarray(rgba, "RGBA")
    w = int(round(im.width * height / im.height))
    return im.resize((w, height), Image.LANCZOS)


def place(canvas, im, cx, cy, angle):
    im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    # soft drop shadow, offset down-right
    a = im.split()[-1]
    sh = Image.new("RGBA", im.size, (40, 30, 20, 0))
    sh.putalpha(a.point(lambda v: int(v * 0.38)))
    pad = 60
    shp = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    shp.paste(sh, (pad, pad))
    shp = shp.filter(ImageFilter.GaussianBlur(22))
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    canvas.alpha_composite(shp, (x - pad + 18, y - pad + 26))
    canvas.alpha_composite(im, (x, y))


def build(name, cfg, src, out):
    canvas = Image.new("RGBA", (SIZE, SIZE), BG + (255,))
    rows = cfg["rows"]
    h = cfg["h"]
    angles = [-6, 4, -3, 5, -4]
    k = 0
    if len(rows) == 1:
        ims = [cutout(os.path.join(src, f), h, f in cfg["soft"]) for f in rows[0]]
        overlap = 0.12
        total = sum(i.width for i in ims) - overlap * sum(i.width for i in ims[1:])
        x = (SIZE - total) / 2
        for i, im in enumerate(ims):
            cx = x + im.width / 2
            place(canvas, im, cx, SIZE / 2 + (30 if i % 2 else -10), angles[i])
            x += im.width * (1 - overlap)
    else:
        ys = [SIZE * 0.31, SIZE * 0.69]
        for r, row in enumerate(rows):
            ims = [cutout(os.path.join(src, f), h, f in cfg["soft"]) for f in row]
            overlap = 0.10 if r == 0 else -0.05
            total = sum(i.width for i in ims) - overlap * sum(i.width for i in ims[1:])
            x = (SIZE - total) / 2
            for im in ims:
                place(canvas, im, x + im.width / 2, ys[r], angles[k % len(angles)])
                x += im.width * (1 - overlap)
                k += 1
    path = os.path.join(out, name + ".jpg")
    canvas.convert("RGB").save(path, quality=90, optimize=True)
    print(path)


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for n, c in PACKS.items():
        build(n, c, src, out)
