"""Wrap a flat UV DTF transfer onto a real photo of a glass (cylinder/taper wrap with perspective, shading, gloss).

Used for the bar-pairing pint and whisky tumbler images (owner's rule 8 Oct 2026: real photos only; 9 Oct 2026:
glass is always printed UV DTF, images clean and crisp). The base photo is a licensed real stock photo of the
plain blank; nothing is drawn: only the transfer is placed, curved round the glass and lit like the photo.

Geometry per blank is in BLANKS (measured on the full-size photo, in fractions of image width/height so the same
numbers work on the preview). The glass outline (left/right outer edge per row) is detected from the photo.

usage: python3 -I wrap.py BLANK PHOTO TRANSFER.png OUT.jpg [--reflect]
"""
import json
import sys

import numpy as np
from PIL import Image, ImageFilter

BLANKS = {
    # nonic pint (aetbvideo): rim y, bottom of glass y, rim outer diameter in mm (20oz nonic, approx), print area
    "pint": dict(rim=0.176, base=0.853, rim_mm=87.0, print_mm=(90.0, 130.0), below_rim_mm=10.0,
                 e_top=0.03, e_bot=0.07, thresh=200, reflect=True),
    # rocks tumbler (alenkadr)
    "tumbler": dict(rim=0.195, base=0.846, rim_mm=83.0, print_mm=(50.0, 50.0), below_rim_mm=10.0,
                    e_top=0.056, e_bot=0.09, thresh=215, reflect=False),
}


def outline(gray, y0, y1, thresh):
    """Outer left/right edge of the glass per row (smoothed)."""
    h, w = gray.shape
    L = np.full(h, np.nan)
    R = np.full(h, np.nan)
    for y in range(y0, y1):
        d = np.where(gray[y] < thresh)[0]
        if len(d) > 2:
            L[y], R[y] = d.min(), d.max()
    ys = np.arange(h)
    ok = ~np.isnan(L)
    L = np.interp(ys, ys[ok], L[ok])
    R = np.interp(ys, ys[ok], R[ok])
    k = max(3, h // 150) | 1  # odd smoothing window
    ker = np.ones(k) / k
    L = np.convolve(np.pad(L, k // 2, mode="edge"), ker, "valid")
    R = np.convolve(np.pad(R, k // 2, mode="edge"), ker, "valid")
    return L, R


def bilinear(img, xs, ys):
    """Sample RGBA float image at float coords (outside -> transparent)."""
    h, w, _ = img.shape
    x0 = np.floor(xs).astype(int)
    y0 = np.floor(ys).astype(int)
    fx = (xs - x0)[..., None]
    fy = (ys - y0)[..., None]
    out = np.zeros(xs.shape + (4,))
    for dx, dy, wt in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
        xi, yi = x0 + dx, y0 + dy
        ok = (xi >= 0) & (xi < w) & (yi >= 0) & (yi < h)
        v = np.zeros(xs.shape + (4,))
        v[ok] = img[yi[ok], xi[ok]]
        out += v * wt
    return out


def wrap(blank, photo_path, art_path, out_path, ss=2):
    B = BLANKS[blank]
    photo = Image.open(photo_path).convert("RGB")
    W, H = photo.size
    base = np.asarray(photo).astype(float) / 255
    gray = np.asarray(photo.convert("L")).astype(int)
    rim_y, base_y = B["rim"] * H, B["base"] * H
    L, R = outline(gray, int(rim_y) + 2, int(base_y) - 2, B["thresh"])
    cx = (L + R) / 2
    rad = (R - L) / 2  # px radius per row
    pxmm = 2 * rad[int(rim_y) + 4] / B["rim_mm"]
    pw, ph = B["print_mm"]
    top = rim_y + B["below_rim_mm"] * pxmm
    bot = top + ph * pxmm
    art = np.asarray(Image.open(art_path).convert("RGBA")).astype(float) / 255
    art[..., :3] *= art[..., 3:4]  # premultiply
    ah, aw, _ = art.shape

    def ecc(y):  # ellipse ratio of horizontal circles at image row y (perspective)
        t = np.clip((y - rim_y) / (base_y - rim_y), 0, 1)
        return B["e_top"] + (B["e_bot"] - B["e_top"]) * t

    # output region (supersampled)
    x_lo = int(np.nanmin(L[int(top):int(bot)])) - 2
    x_hi = int(np.nanmax(R[int(top):int(bot)])) + 3
    y_lo = int(top - B["e_bot"] * rad.max()) - 3
    y_hi = int(bot + B["e_bot"] * rad.max()) + 3
    gx, gy = np.meshgrid(np.arange(x_lo * ss, x_hi * ss) / ss + 0.5 / ss, np.arange(y_lo * ss, y_hi * ss) / ss + 0.5 / ss)
    # solve for the row y_c on the glass whose front-facing circle passes through (gx, gy)
    yc = gy.copy()
    for _ in range(6):
        yi = np.clip(yc, 0, H - 1)
        r = np.interp(yi, np.arange(H), rad)
        c = np.interp(yi, np.arange(H), cx)
        sn = np.clip((gx - c) / r, -1, 1)
        cs = np.sqrt(1 - sn ** 2)
        yc = gy - ecc(yi) * r * cs
    r = np.interp(yc, np.arange(H), rad)
    c = np.interp(yc, np.arange(H), cx)
    sn = (gx - c) / r
    front = np.abs(sn) < 1
    theta = np.arcsin(np.clip(sn, -1, 1))
    s_mm = theta * (r / pxmm)  # arc length from the front centre line, in mm (radius follows the glass profile)
    u = (s_mm / pw + 0.5) * aw - 0.5
    v = (yc - top) / (bot - top) * ah - 0.5
    smp = bilinear(art, u, v)
    smp[~front] = 0
    a = smp[..., 3:4]
    rgb = np.where(a > 1e-6, smp[..., :3] / np.maximum(a, 1e-6), 0)
    # lighting: soft fall-off towards the sides + glossy UV DTF highlights (lamp left-front)
    cs = np.cos(theta)[..., None]
    shade = 0.64 + 0.36 * cs ** 0.9
    rgb = rgb * shade
    th = theta[..., None]
    gloss = 0.22 * np.exp(-((th + 0.42) / 0.10) ** 2) + 0.09 * np.exp(-((th - 0.55) / 0.07) ** 2)
    gloss = gloss * (0.85 + 0.15 * np.cos((yc[..., None] - top) / (bot - top) * np.pi))
    rgb = 1 - (1 - rgb) * (1 - gloss)  # screen
    layer = np.concatenate([np.clip(rgb, 0, 1), a], -1)
    # downsample supersampled layer
    hh, ww = layer.shape[0] // ss, layer.shape[1] // ss
    layer = layer[: hh * ss, : ww * ss].reshape(hh, ss, ww, ss, 4)
    a_ds = layer[..., 3].mean((1, 3))
    rgb_ds = (layer[..., :3] * layer[..., 3:4]).mean((1, 3)) / np.maximum(a_ds, 1e-6)[..., None]
    # tiny raised-edge shadow (transfer is a thin raised film)
    edge = Image.fromarray((a_ds * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(1, W / 1800)))
    edge = np.asarray(edge).astype(float) / 255
    shadow = np.clip(edge - a_ds, 0, 1) * 0.25
    out = base.copy()
    reg = out[y_lo:y_lo + hh, x_lo:x_lo + ww]
    reg *= (1 - shadow)[..., None]
    reg[:] = reg * (1 - a_ds[..., None]) + rgb_ds * a_ds[..., None]
    if B["reflect"]:
        by = int(round(base_y))
        n = min(by - y_lo, H - by)
        src = out[by - n:by, x_lo:x_lo + ww][::-1]
        msk = np.zeros((n, ww))
        y_in = np.arange(by - n, by)[::-1]
        a_full = np.zeros((H, ww))
        a_full[y_lo:y_lo + hh] = a_ds
        msk = a_full[y_in]
        fade = np.clip(1 - np.arange(n) / (0.22 * H), 0, 1) ** 1.5 * 0.45
        dst = out[by:by + n, x_lo:x_lo + ww]
        m = (msk * fade[:, None])[..., None]
        dst[:] = dst * (1 - m) + src * m
    Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(out_path, quality=95, subsampling=0)
    return dict(px_per_mm=round(pxmm, 3), print_box=[x_lo, int(top), x_hi, int(bot)])


if __name__ == "__main__":
    print(json.dumps(wrap(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])))
