"""Composite the REAL number plate artwork onto blank AI mug photos (runs in the Higgsfield sandbox).

The AI images are blank white mugs (no text), so every letter on the plates comes from our own
print artwork (textures/*.png from number_plate_mugs.py), wrapped round the mug with a cylinder
mapping and multiplied by the photo's own shading.

usage: python3 number_plate_mug_mockups.py SCENES_DIR TEXTURES_DIR products.json OUT_DIR
SCENES_DIR holds s0.png (studio, handle right) and s1..s8.png (lifestyle).
"""
import json
import os
import sys

import numpy as np
from PIL import Image

N = 2048
MUG_R_MM = 41.0            # 11oz mug, ~82 mm diameter
TEX_W_MM, TEX_H_MM = 200.0, 70.0  # full wrap print area (textures/<sku>-<code>-wrap.png)

# body box as fractions of the image: left, right, top, bottom; sag = rim-ellipse curvature
SCENES = {
    "s0": dict(box=(0.236, 0.708, 0.206, 0.81), sag=0.02, name="studio"),
    "s1": dict(box=(0.324, 0.660, 0.330, 0.76), sag=0.06, name="kitchen worktop"),
    "s2": dict(box=(0.296, 0.664, 0.300, 0.77), sag=0.06, name="kitchen counter with biscuits"),
    "s3": dict(box=(0.330, 0.655, 0.336, 0.77), sag=0.06, name="office desk"),
    "s4": dict(box=(0.310, 0.644, 0.330, 0.745), sag=0.05, name="home office"),
    "s5": dict(box=(0.320, 0.652, 0.330, 0.75), sag=0.05, name="garage workbench"),
    "s6": dict(box=(0.326, 0.640, 0.336, 0.724), sag=0.05, name="car keys and driving gloves"),
    "s7": dict(box=(0.316, 0.660, 0.290, 0.736), sag=0.06, name="birthday gift"),
    "s8": dict(box=(0.330, 0.650, 0.350, 0.756), sag=0.06, name="kraft gift box"),
}
# 3 lifestyle scenes per design: kitchen, office, then garage/car or gift
LIFESTYLE = [["s1", "s3", "s5"], ["s2", "s4", "s8"], ["s1", "s3", "s7"], ["s2", "s4", "s6"], ["s1", "s3", "s5"],
             ["s2", "s4", "s8"], ["s1", "s3", "s7"], ["s2", "s4", "s6"], ["s1", "s3", "s5"], ["s2", "s4", "s7"]]
CODES = ["GB", "SCO", "CYM", "NI", "IRL"]
NAMES = {"GB": "GB", "SCO": "Scotland", "CYM": "Wales", "NI": "Northern Ireland", "IRL": "Ireland"}


def refine(lum, x, y0, y1, win=14):
    """snap a vertical mug edge to the strongest horizontal gradient near x"""
    band = lum[y0:y1, max(1, x - win):x + win + 1]
    g = np.abs(np.diff(band, axis=1)).mean(axis=0)
    return max(1, x - win) + int(np.argmax(g))


def sample(tex, xs, ys):
    """bilinear sample RGBA texture at float coords"""
    h, w = tex.shape[:2]
    x0 = np.clip(np.floor(xs).astype(int), 0, w - 2)
    y0 = np.clip(np.floor(ys).astype(int), 0, h - 2)
    fx, fy = (xs - x0)[..., None], (ys - y0)[..., None]
    a = tex[y0, x0] * (1 - fx) + tex[y0, x0 + 1] * fx
    b = tex[y0 + 1, x0] * (1 - fx) + tex[y0 + 1, x0 + 1] * fx
    out = a * (1 - fy) + b * fy
    outside = (xs < 0) | (xs > w - 1) | (ys < 0) | (ys > h - 1)
    out[outside] = 0
    return out


def composite(base, scene, tex, flip=False, centre_mm=100.0):
    img = base.transpose(Image.FLIP_LEFT_RIGHT) if flip else base
    arr = np.asarray(img).astype(np.float32) / 255
    lum = arr @ np.array([0.299, 0.587, 0.114], np.float32)
    l, r, t, b = scene["box"]
    if flip:
        l, r = 1 - r, 1 - l
    yA, yB = int((t + 0.25 * (b - t)) * N), int((t + 0.75 * (b - t)) * N)
    xl, xr = refine(lum, int(l * N), yA, yB), refine(lum, int(r * N), yA, yB)
    cx, R = (xl + xr) / 2, (xr - xl) / 2
    pxmm = R / MUG_R_MM
    yc = (t + b) / 2 * N + 0.02 * (b - t) * N        # print zone centred on the body
    e = scene["sag"] * R
    hh = int(TEX_H_MM / 2 * pxmm + e + 4)
    X0, X1 = int(xl) + 1, int(xr)
    Y0, Y1 = int(yc - hh), int(yc + hh)
    ys, xs = np.mgrid[Y0:Y1, X0:X1].astype(np.float32)
    u = np.clip((xs - cx) / R, -0.999, 0.999)
    th = np.arcsin(u)
    arc = th * MUG_R_MM
    ymm = (ys - yc - e * np.cos(th)) / pxmm
    th_, tw_ = tex.shape[:2]
    tx = (arc + centre_mm) / TEX_W_MM * tw_   # centre_mm = point of the wrap facing the camera
    ty = (ymm + TEX_H_MM / 2) / TEX_H_MM * th_
    s = sample(tex, tx, ty)
    rgb, a = s[..., :3], s[..., 3:4]
    region = lum[Y0:Y1, X0:X1]
    body = lum[int(yA):int(yB), int(xl + 0.2 * R):int(xr - 0.2 * R)]
    ref = np.percentile(body, 96)
    shade = (region / ref)[..., None]
    lit = np.clip(rgb * np.minimum(shade, 1.0) + np.clip(shade - 1.0, 0, 1) * 0.6, 0, 1)
    a = a * np.clip((1 - np.abs(u)) * 25, 0, 1)[..., None]   # fade at the silhouette
    arr[Y0:Y1, X0:X1] = arr[Y0:Y1, X0:X1] * (1 - a) + lit * a
    return Image.fromarray((arr * 255 + 0.5).astype(np.uint8))


def main(scenes_dir, tex_dir, products_path, out):
    os.makedirs(out, exist_ok=True)
    bases = {k: Image.open(os.path.join(scenes_dir, k + ".png")).convert("RGB").resize((N, N), Image.LANCZOS)
             for k in SCENES if SCENES[k]["box"]}
    tex = lambda sb, code, which: np.asarray(
        Image.open(os.path.join(tex_dir, f"{sb}-{code}-{which}.png")).convert("RGBA")).astype(np.float32) / 255
    manifest = []
    for i, p in enumerate(json.load(open(products_path))):
        sb = p["sku_base"]
        # Geometry: the wrap starts just past the handle. Text reads left to right, so with the handle on the LEFT
        # you see the band end (wrap x ~36 mm faces the camera); with the handle on the RIGHT you see the far end (~164 mm).
        for code in CODES:   # one mockup per country, handle left, so the country band is in view
            fn = f"{sb}-{code}-mockup.jpg"
            composite(bases["s0"], SCENES["s0"], tex(sb, code, "wrap"), flip=True, centre_mm=36).save(os.path.join(out, fn), quality=88)
            manifest.append(dict(sku=sb, file=fn, kind="mockup", country=NAMES[code]))
        # wrap view: two mugs turned so you see the band end and the far end of the plate going round
        a = composite(bases["s0"], SCENES["s0"], tex(sb, "GB", "wrap"), flip=True, centre_mm=36)
        b = composite(bases["s0"], SCENES["s0"], tex(sb, "GB", "wrap"), centre_mm=164)
        crop = lambda im, l, r: im.crop((int(l * N), 0, int(r * N), N))
        a, b = crop(a, 0.08, 0.80), crop(b, 0.20, 0.92)
        w = a.width + b.width
        sc = Image.new("RGB", (w, N), (255, 255, 255)); sc.paste(a, (0, 0)); sc.paste(b, (a.width, 0))
        canvas = Image.new("RGB", (w, w), (255, 255, 255)); canvas.paste(sc, (0, (w - N) // 2))
        fn = f"{sb}-wrap-views.jpg"
        canvas.resize((N, N), Image.LANCZOS).save(os.path.join(out, fn), quality=88)
        manifest.append(dict(sku=sb, file=fn, kind="wrap-views", country="GB"))
        # flat full wrap
        flat = Image.new("RGB", (N, N), (255, 255, 255))
        t = Image.open(os.path.join(tex_dir, f"{sb}-GB-wrap.png")).convert("RGBA")
        t = t.resize((N - 160, int(t.height * (N - 160) / t.width)), Image.LANCZOS)
        flat.paste(t, (80, (N - t.height) // 2), t)
        fn = f"{sb}-flat-wrap.jpg"
        flat.save(os.path.join(out, fn), quality=90)
        manifest.append(dict(sku=sb, file=fn, kind="flat", country="GB"))
        for k, sc_key in enumerate(LIFESTYLE[i]):
            code = CODES[(i + k) % 5]
            fn = f"{sb}-life-{k + 1}.jpg"
            composite(bases[sc_key], SCENES[sc_key], tex(sb, code, "wrap"), flip=(k != 1), centre_mm=(36, 164, 36)[k]).save(os.path.join(out, fn), quality=88)
            manifest.append(dict(sku=sb, file=fn, kind="lifestyle", country=NAMES[code], scene=SCENES[sc_key]["name"]))
    json.dump(manifest, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print(len(manifest), "images")


if __name__ == "__main__":
    main(*sys.argv[1:5])
