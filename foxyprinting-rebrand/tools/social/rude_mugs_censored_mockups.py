"""Censored mug renders for the rude number plate mug adverts (TikTok / Reels / Facebook feed).

Social platforms restrict posts that show profanity, so the adverts never show the registration.
This draws a bold black CENSORED bar over the whole registration on the flat 200 x 70 mm wrap
texture BEFORE it is wrapped round the mug (so the bar curves with the mug), then renders with
tools/artwork/number_plate_mug_local_mockups.py and writes transparent-background RGBA PNGs
(mug + soft contact shadow) so they can be composited onto brand-coloured backgrounds.

usage: python3 rude_mugs_censored_mockups.py TEXTURES_DIR products.json OUT_DIR
writes, per design n (1..10):
  <n>-front.png   handle right, the middle of the bar facing camera (CENSORED fully readable)
  <n>-band.png    handle left, the country band end facing camera
  pair.png        two mugs (band end + far end) for design 1
  censored-texture-<n>.png  flat censored plate (for the stills)
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "artwork"))
import number_plate_mug_local_mockups as M  # noqa: E402

ANTON = "/root/.fonts/Anton-Regular.ttf"
BANDS = ["GB", "SCO", "CYM", "NI", "IRL"]
PINK = (255, 45, 135)


def censor(tex_path):
    """Return the wrap texture with an opaque black CENSORED bar over every registration character."""
    t = Image.open(tex_path).convert("RGBA")
    w, h = t.size
    a = np.asarray(t).astype(int)
    dark = (a[..., 0] < 90) & (a[..., 1] < 90) & (a[..., 2] < 90) & (a[..., 3] > 200)
    dark[: int(h * .15)] = 0
    dark[int(h * .85):] = 0
    dark[:, : int(w * .18)] = 0
    dark[:, int(w * .95):] = 0
    ys, xs = np.nonzero(dark)
    # generous fixed-size bar (same on every design) that always contains the detected text
    x0, x1 = min(int(w * .200), xs.min() - 30), max(int(w * .935), xs.max() + 30)
    y0, y1 = min(int(h * .195), ys.min() - 30), max(int(h * .805), ys.max() + 30)
    d = ImageDraw.Draw(t)
    r = int((y1 - y0) * .12)
    d.rounded_rectangle([x0, y0, x1, y1], r, fill=(14, 12, 20, 255))
    # thin pink inset line
    ins = int((y1 - y0) * .07)
    d.rounded_rectangle([x0 + ins, y0 + ins, x1 - ins, y1 - ins], max(1, r - ins), outline=PINK + (255,),
                        width=max(4, int((y1 - y0) * .022)))
    size = int((y1 - y0) * .62)
    f = ImageFont.truetype(ANTON, size)
    txt = "CENSORED"
    sp = int(size * .06)
    widths = [d.textlength(c, font=f) for c in txt]
    tw = sum(widths) + sp * (len(txt) - 1)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    x = cx - tw / 2
    for c, cw in zip(txt, widths):
        d.text((x, cy), c, font=f, fill=(255, 255, 255, 255), anchor="lm")
        x += cw + sp
    # safety check: no original dark text pixel may remain outside the bar
    b = np.asarray(t).astype(int)
    left = dark & ~((np.arange(w)[None, :] >= x0) & (np.arange(w)[None, :] <= x1)
                    & (np.arange(h)[:, None] >= y0) & (np.arange(h)[:, None] <= y1))
    assert not left.any(), "registration pixels outside the bar"
    return t


def scene_rgba(mugs, out_size=M.N):
    """Like M.scene but returns RGBA: mug opaque, contact shadow as translucent black."""
    S = out_size * M.SS
    canvas = np.ones((S, S, 3), np.float32)
    shadow = np.zeros((S, S), np.float32)
    cover = np.zeros((S, S), bool)
    for cxf, ytf, pxmm, tex, centre, handle in mugs:
        M.draw_mug(canvas, shadow, cover, cxf * S, ytf * S, pxmm * M.SS, tex, centre, handle)
    sh = Image.fromarray((np.clip(shadow, 0, 1) * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(14 * M.SS))
    sh = np.asarray(sh).astype(np.float32) / 255 * 0.55
    alpha = np.where(cover, 1.0, sh)
    rgb = np.where(cover[..., None], canvas, 0.0)
    img = np.dstack([np.clip(rgb, 0, 1), alpha])
    im = Image.fromarray((img * 255 + 0.5).astype(np.uint8), "RGBA")
    im = im.resize((out_size, out_size), Image.LANCZOS)
    return im.crop(im.getbbox())


def single(tex, centre_mm, handle):
    pxmm = 13.6
    ext_h, ext_o = M.mug_extent_mm()
    width = (ext_h + ext_o) * pxmm
    cx = M.N / 2 + (width / 2 - ext_o * pxmm) * (1 if handle == "left" else -1)
    ytop = (M.N - M.MUG_H_MM * pxmm) / 2 + 0.035 * M.N
    return scene_rgba([(cx / M.N, ytop / M.N, pxmm, tex, centre_mm, handle)])


def pair(tex):
    pxmm = 7.9
    ext_h, ext_o = M.mug_extent_mm()
    gap = 170
    w1 = (ext_h + ext_o) * pxmm
    left0 = (M.N - 2 * w1 - gap) / 2
    cx1 = left0 + ext_h * pxmm
    cx2 = left0 + w1 + gap + ext_o * pxmm
    ytop = (M.N - M.MUG_H_MM * pxmm) / 2 - 0.01 * M.N
    return scene_rgba([(cx1 / M.N, ytop / M.N, pxmm, tex, 36.0, "left"),
                       (cx2 / M.N, ytop / M.N, pxmm, tex, 164.0, "right")])


def to_arr(img):
    return np.asarray(img).astype(np.float32) / 255


def main(tex_dir, products_path, out):
    os.makedirs(out, exist_ok=True)
    for p in json.load(open(products_path)):
        n, sb = p["n"], p["sku_base"]
        band = BANDS[(n - 1) % len(BANDS)]
        tex = censor(os.path.join(tex_dir, f"{sb}-{band}-wrap.png"))
        tex.save(os.path.join(out, f"censored-texture-{n}.png"))
        arr = to_arr(tex)
        single(arr, 112.0, "right").save(os.path.join(out, f"{n}-front.png"))
        single(arr, 62.0, "left").save(os.path.join(out, f"{n}-band.png"))
        if n == 1:
            pair(arr).save(os.path.join(out, "pair.png"))
        print(n, sb, band, "done", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
