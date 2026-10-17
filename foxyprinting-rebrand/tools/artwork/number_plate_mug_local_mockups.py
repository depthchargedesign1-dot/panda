"""Local studio mockups for the funny number plate mugs (no AI scene photos, no third-party services).

Draws a white glossy 11oz ceramic mug procedurally in numpy (cylinder body with soft shading and a
vertical specular highlight, elliptical rim with the inner wall, C-shaped handle, soft contact shadow)
and wraps the real 200 x 70 mm print texture round it with the same cylinder mapping as
number_plate_mug_mockups.py (arc = asin(u) * R, texture x = arc + centre_mm).

usage: python3 number_plate_mug_local_mockups.py TEXTURES_DIR products.json OUT_DIR [SKU_BASE ...]
Per design it writes 7 JPGs (2048 x 2048, quality 85):
  <sku>-1-GB.jpg, -2-SCO, -3-CYM, -4-NI, -5-IRL  (handle left, band end of the plate facing the camera)
  <sku>-6-both-ends.jpg                          (two mugs: band end + far end of the plate)
  <sku>-7-flat-plate.jpg                         (the full 200 x 70 mm print, flat, subtle drop shadow)
and manifest.json.
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy.spatial import cKDTree

N = 2048
SS = 2                      # supersampling factor
MUG_R_MM = 41.0             # 11oz mug, ~82 mm diameter
MUG_H_MM = 95.0
TEX_W_MM, TEX_H_MM = 200.0, 70.0
PRINT_TOP_MM = (MUG_H_MM - TEX_H_MM) / 2   # band centred vertically on the body
TILT = 0.11                 # rim ellipse minor/major ratio (slightly above eye level)
CODES = ["GB", "SCO", "CYM", "NI", "IRL"]
NAMES = {"GB": "GB", "SCO": "Scotland", "CYM": "Wales", "NI": "Northern Ireland", "IRL": "Ireland"}
GLAZE = np.array([0.975, 0.975, 0.97], np.float32)
LIGHT = np.array([-0.48, -0.30, 0.82], np.float32)
LIGHT /= np.linalg.norm(LIGHT)
HALF = LIGHT + np.array([0, 0, 1], np.float32)
HALF /= np.linalg.norm(HALF)


def sample(tex, xs, ys):
    """bilinear sample of an RGBA float texture; transparent outside"""
    h, w = tex.shape[:2]
    x0 = np.clip(np.floor(xs).astype(int), 0, w - 2)
    y0 = np.clip(np.floor(ys).astype(int), 0, h - 2)
    fx, fy = np.clip(xs - x0, 0, 1)[..., None], np.clip(ys - y0, 0, 1)[..., None]
    a = tex[y0, x0] * (1 - fx) + tex[y0, x0 + 1] * fx
    b = tex[y0 + 1, x0] * (1 - fx) + tex[y0 + 1, x0 + 1] * fx
    out = a * (1 - fy) + b * fy
    out[(xs < 0) | (xs > w - 1) | (ys < 0) | (ys > h - 1)] = 0
    return out


def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def mug_extent_mm():
    """horizontal extent of mug + handle, from body centre: (towards handle, away from handle)"""
    return MUG_R_MM + 31.0, MUG_R_MM


def draw_mug(canvas, shadow, cover, cx, ytop, pxmm, tex, centre_mm, handle="left"):
    """canvas: HxWx3 float (supersampled). cx, ytop: body centre x and rim centre y in canvas px."""
    H, W = canvas.shape[:2]
    R = MUG_R_MM * pxmm
    e = TILT * R
    ybot = ytop + MUG_H_MM * pxmm
    sgn = -1 if handle == "left" else 1          # handle direction on screen

    # ---------------- contact shadow (accumulated, blurred later)
    sy0, sy1 = max(0, int(ybot - 4 * e)), min(H, int(ybot + 4 * e))
    sx0, sx1 = max(0, int(cx - 2 * R)), min(W, int(cx + 2 * R))
    yy, xx = np.mgrid[sy0:sy1, sx0:sx1].astype(np.float32)
    d = ((xx - cx - sgn * 0.12 * R) / (R * 1.18)) ** 2 + ((yy - ybot - 0.15 * e) / (e * 1.6)) ** 2
    shadow[sy0:sy1, sx0:sx1] += 0.55 * np.exp(-d * 2.2)
    d2 = ((xx - cx) / (R * 0.98)) ** 2 + ((yy - ybot) / (e * 0.9)) ** 2
    shadow[sy0:sy1, sx0:sx1] += 0.45 * (d2 < 1)

    # ---------------- handle: a superellipse "C" tube in profile
    hx0 = cx + sgn * (R - 4 * pxmm)
    yA, yB = ytop + 17 * pxmm, ytop + 77 * pxmm
    ym, b = (yA + yB) / 2, (yB - yA) / 2
    a = 31 * pxmm + (R - abs(hx0 - cx))
    t = np.linspace(-np.pi / 2, np.pi / 2, 1400)
    n = 2.8
    sp = lambda v: np.sign(v) * np.abs(v) ** (2 / n)
    px = hx0 + sgn * a * sp(np.cos(t))
    py = ym + b * sp(np.sin(t))
    pts = np.stack([px, py], 1)
    tang = np.gradient(pts, axis=0)
    tang /= np.linalg.norm(tang, axis=1, keepdims=True) + 1e-9
    nrm = np.stack([tang[:, 1], -tang[:, 0]], 1)          # 2D normal
    r_tube = 5.0 * pxmm * (1 + 0.35 * np.exp(-((np.abs(t) - np.pi / 2) / 0.22) ** 2))  # flare at the joints
    x0, x1 = int(min(px.min(), hx0) - 12 * pxmm), int(max(px.max(), hx0) + 12 * pxmm)
    y0, y1 = int(py.min() - 12 * pxmm), int(py.max() + 12 * pxmm)
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    gy, gx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    q = np.stack([gx.ravel(), gy.ravel()], 1)
    dist, idx = cKDTree(pts).query(q, workers=-1)
    dist, idx = dist.reshape(gx.shape), idx.reshape(gx.shape)
    rr = r_tube[idx]
    inside = dist < rr
    off = np.stack([gx - px[idx], gy - py[idx]], -1)
    s = np.clip((off * nrm[idx]).sum(-1) / rr, -1, 1)       # signed position across the tube
    nz = np.sqrt(np.clip(1 - s ** 2, 0, 1))
    N3 = np.stack([s * nrm[idx][..., 0], s * nrm[idx][..., 1], nz], -1)
    ndl = np.clip(N3 @ LIGHT, 0, 1)
    spec = np.clip(N3 @ HALF, 0, 1) ** 60 * 0.55
    sh = 0.50 + 0.50 * ndl
    # the inner face of the C sits in the body's shade
    col = GLAZE * sh[..., None] + spec[..., None]
    sl = canvas[y0:y1, x0:x1]
    sl[inside] = col[inside]
    cover[y0:y1, x0:x1][inside] = True

    # ---------------- body (front surface)
    bx0, bx1 = int(cx - R) - 2, int(cx + R) + 2
    by0, by1 = int(ytop - e) - 2, int(ybot + e) + 2
    gy, gx = np.mgrid[by0:by1, bx0:bx1].astype(np.float32)
    u = (gx - cx) / R
    inb = np.abs(u) < 1
    uc = np.clip(u, -0.9999, 0.9999)
    th = np.arcsin(uc)
    ct = np.cos(th)
    front_top = ytop + e * ct
    front_bot = ybot + e * ct
    body = inb & (gy >= front_top) & (gy <= front_bot)
    hmm = (gy - front_top) / pxmm                            # mm down from the rim along the body
    N3 = np.stack([uc, np.zeros_like(uc), ct], -1)
    ndl = np.clip(N3 @ LIGHT, -1, 1)
    shade = 0.70 + 0.30 * np.clip(ndl, 0, 1) - 0.12 * np.clip(-ndl, 0, 1)
    shade *= 1 - 0.30 * smooth(np.abs(uc), 0.55, 1.0) ** 1.5   # turning away at the silhouette
    shade *= 1 - 0.10 * smooth(hmm, MUG_H_MM - 9, MUG_H_MM)    # base occlusion
    shade *= 1 - 0.04 * (1 - smooth(hmm, 0, 5))                 # just under the rim
    vwin = smooth(hmm, 4, 14) * (1 - smooth(hmm, MUG_H_MM - 14, MUG_H_MM - 4))
    th_hi = -0.42
    spec = (0.30 * np.exp(-((th - th_hi) / 0.075) ** 2) + 0.07 * np.exp(-((th - th_hi) / 0.30) ** 2)
            + 0.12 * np.exp(-((th - 1.18) / 0.06) ** 2)) * vwin
    # print, wrapped (same maths as number_plate_mug_mockups.composite)
    tw_h, tw_w = tex.shape[:2]
    arc = th * MUG_R_MM
    tx = (arc + centre_mm) / TEX_W_MM * tw_w
    ty = (hmm - PRINT_TOP_MM) / TEX_H_MM * tw_h
    smp = sample(tex, tx, ty)
    alpha = smp[..., 3:4] * 0.97
    albedo = GLAZE * (1 - alpha) + smp[..., :3] * alpha
    col = albedo * shade[..., None] + spec[..., None]
    # slight darkening/softening right at the silhouette (glaze turning away)
    edge = smooth(1 - np.abs(u), 0, 0.04)[..., None]
    col = col * (0.85 + 0.15 * edge)
    sl = canvas[by0:by1, bx0:bx1]
    sl[body] = np.clip(col[body], 0, 1)
    cover[by0:by1, bx0:bx1][body] = True

    # ---------------- rim lip and opening (ellipse at the top)
    ell = ((gx - cx) / R) ** 2 + ((gy - ytop) / e) ** 2
    Ri = R - 3.2 * pxmm
    ei = e * Ri / R
    ell_i = ((gx - cx) / Ri) ** 2 + ((gy - ytop) / ei) ** 2
    lip = (ell <= 1) & (ell_i > 1)
    v = (gy - ytop) / e
    lipcol = GLAZE * (0.93 + 0.06 * (-v).clip(0, 1))[..., None] + 0.05 * smooth(-u, 0.2, 0.7)[..., None]
    sl[lip] = np.clip(lipcol[lip], 0, 1)
    cover[by0:by1, bx0:bx1][lip] = True
    hole = ell_i <= 1
    ui = (gx - cx) / Ri
    vi = (gy - ytop) / ei
    inner = 0.70 + 0.13 * ui - 0.10 * (vi + 1) / 2
    inner -= 0.16 * smooth(vi, 0.1, 1.0) * (1 - np.abs(ui))    # shadow of the front rim
    inner += 0.10 * np.exp(-((ui - 0.55) / 0.12) ** 2) * (1 - smooth(vi, -0.2, 0.6))   # soft highlight on the inner wall
    sl[hole] = (GLAZE * inner[..., None])[hole]
    cover[by0:by1, bx0:bx1][hole] = True
    # crisp highlight along the front rim edge
    rimline = np.abs(ell - 1) < (2.2 / e) * (gy > ytop)
    sl[rimline] = np.clip(sl[rimline] * 0.6 + 0.42, 0, 1)


def scene(mugs, out_size=N):
    """mugs: list of (cx_frac, ytop_frac, pxmm_final, tex, centre_mm, handle). Returns PIL RGB."""
    S = out_size * SS
    canvas = np.ones((S, S, 3), np.float32)
    shadow = np.zeros((S, S), np.float32)
    cover = np.zeros((S, S), bool)
    for cxf, ytf, pxmm, tex, centre, handle in mugs:
        draw_mug(canvas, shadow, cover, cxf * S, ytf * S, pxmm * SS, tex, centre, handle)
    # contact shadow: blur, then multiply only where the canvas is background
    sh = Image.fromarray((np.clip(shadow, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14 * SS))
    sh = np.asarray(sh).astype(np.float32) / 255
    bg = ~cover
    canvas[bg] *= (1 - 0.42 * sh[bg])[:, None]
    img = Image.fromarray((np.clip(canvas, 0, 1) * 255 + 0.5).astype(np.uint8))
    return img.resize((out_size, out_size), Image.LANCZOS)


def single(tex, centre_mm=36.0, handle="left"):
    pxmm = 13.6
    ext_h, ext_o = mug_extent_mm()
    width = (ext_h + ext_o) * pxmm
    cx = N / 2 + (width / 2 - ext_o * pxmm) * (1 if handle == "left" else -1)
    ytop = (N - MUG_H_MM * pxmm) / 2 + 0.035 * N
    return scene([(cx / N, ytop / N, pxmm, tex, centre_mm, handle)])


def both_ends(tex):
    pxmm = 7.9
    ext_h, ext_o = mug_extent_mm()
    gap = 170
    w1 = (ext_h + ext_o) * pxmm
    left0 = (N - 2 * w1 - gap) / 2
    cx1 = left0 + ext_h * pxmm                       # handle left
    cx2 = left0 + w1 + gap + ext_o * pxmm            # handle right
    ytop = (N - MUG_H_MM * pxmm) / 2 - 0.01 * N
    return scene([(cx1 / N, ytop / N, pxmm, tex, 36.0, "left"),
                  (cx2 / N, ytop / N, pxmm, tex, 164.0, "right")])


def flat(tex_path):
    t = Image.open(tex_path).convert("RGBA")
    w = N - 220
    t = t.resize((w, round(t.height * w / t.width)), Image.LANCZOS)
    x, y = 110, (N - t.height) // 2 - 10
    img = Image.new("RGB", (N, N), (255, 255, 255))
    a = Image.new("L", (N, N), 0)
    a.paste(t.split()[3], (x + 6, y + 18))
    a = a.filter(ImageFilter.GaussianBlur(22))
    sh = np.asarray(a).astype(np.float32) / 255 * 0.28
    arr = np.asarray(img).astype(np.float32) * (1 - sh[..., None])
    img = Image.fromarray(arr.astype(np.uint8))
    img.paste(t, (x, y), t)
    return img


def load_tex(path):
    return np.asarray(Image.open(path).convert("RGBA")).astype(np.float32) / 255


def main(tex_dir, products_path, out, only=()):
    os.makedirs(out, exist_ok=True)
    manifest = []
    for p in json.load(open(products_path)):
        sb = p["sku_base"]
        if only and sb not in only:
            continue
        tp = lambda c: os.path.join(tex_dir, f"{sb}-{c}-wrap.png")
        for i, code in enumerate(CODES):
            fn = f"{sb}-{i + 1}-{code}.jpg"
            single(load_tex(tp(code))).save(os.path.join(out, fn), quality=85)
            manifest.append(dict(sku=sb, file=fn, kind="mockup", country=NAMES[code]))
        fn = f"{sb}-6-both-ends.jpg"
        both_ends(load_tex(tp("GB"))).save(os.path.join(out, fn), quality=85)
        manifest.append(dict(sku=sb, file=fn, kind="both-ends", country="GB"))
        fn = f"{sb}-7-flat-plate.jpg"
        flat(tp("GB")).save(os.path.join(out, fn), quality=85)
        manifest.append(dict(sku=sb, file=fn, kind="flat", country="GB"))
        print(sb, "done", flush=True)
    if not only:
        json.dump(manifest, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print(len(manifest), "images")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], tuple(sys.argv[4:]))
