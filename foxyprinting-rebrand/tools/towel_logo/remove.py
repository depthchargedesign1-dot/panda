"""Remove the DCD TEAMWEAR logo from a towel beach-scene image.

Fill = smooth lighting interpolated from the surrounding sand
     + sand texture by image quilting: tiles are filled in raster order, and for
       each tile the source patch (taken from clean sand near the logo) that best
       matches the pixels it overlaps (real sand around the hole and tiles already
       filled) is chosen. Only pixels inside the dilated logo mask change."""
import cv2, numpy as np
from logomask import logo_mask

def _lowfreq_fill(c, m, k=8):
    h, w = m.shape
    sm = cv2.resize(c, (w // k, h // k), interpolation=cv2.INTER_AREA)
    mm = cv2.resize(m, (w // k, h // k), interpolation=cv2.INTER_NEAREST)
    mm = cv2.dilate(mm, np.ones((3, 3), np.uint8))
    out = np.empty_like(sm)
    for ch in range(3):
        out[..., ch] = cv2.inpaint(sm[..., ch], mm, 6, cv2.INPAINT_TELEA)
    up = cv2.resize(out, (w, h), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    return cv2.GaussianBlur(up, (0, 0), k)

def remove_logo(im, box, seed=7, ncand=600):
    H, W = im.shape[:2]
    sc = W / 2000.0
    x0, y0, x1, y1 = box
    mask = logo_mask(im, box)
    X0, Y0 = max(0, x0 - int(500 * sc)), max(0, y0 - int(60 * sc))
    X1, Y1 = min(W, x1 + int(200 * sc)), min(H, y1 + int(160 * sc))
    c = im[Y0:Y1, X0:X1].astype(np.float32)
    logo = mask[Y0:Y1, X0:X1] > 0
    f = max(4, int(10 * sc))                       # cross-fade band outside the logo
    m = cv2.dilate(logo.astype(np.uint8) * 255, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * f + 1,) * 2))
    hole = m > 0
    s = 14 * sc
    lf = cv2.GaussianBlur(c, (0, 0), s)
    hf = c - lf
    lf_known = lf.copy()
    # lighting inside the hole, interpolated from the surrounding sand only
    lf_masked = cv2.GaussianBlur(np.where(hole[..., None], 0, c), (0, 0), s)
    wgt = cv2.GaussianBlur((~hole).astype(np.float32), (0, 0), s)[..., None]
    lf_local = lf_masked / np.maximum(wgt, 1e-3)
    lf_t = _lowfreq_fill(lf_local.clip(0, 255).astype(np.uint8), m)
    lf_t = np.where(hole[..., None], lf_t, lf_known)
    # clean sand sources (no logo, towel, objects)
    hsv = cv2.cvtColor(cv2.GaussianBlur(c, (0, 0), 3 * sc).astype(np.uint8), cv2.COLOR_BGR2HSV)
    sand = ((hsv[..., 2] < 235) & (hsv[..., 2] > 80) & (hsv[..., 1] > 45) & (hsv[..., 1] < 140)
            & (hsv[..., 0] >= 8) & (hsv[..., 0] <= 26)).astype(np.uint8)
    P = max(16, int(40 * sc)); OV = max(6, int(12 * sc))
    near = cv2.dilate(m, np.ones((int(20 * sc) | 1,) * 2, np.uint8))
    ok = ((sand > 0) & (near == 0)).astype(np.uint8)
    okf = cv2.erode(ok, np.ones((P, P), np.uint8), anchor=(0, 0))
    ys, xs = np.nonzero(okf[:-P, :-P])
    rng = np.random.default_rng(seed)
    hfs = cv2.GaussianBlur(hf, (0, 0), 2.5 * sc)          # structure only, for matching
    loc_sd = np.sqrt(cv2.blur((hf ** 2).mean(-1), (P, P), anchor=(0, 0)))
    sd_ref = np.median(loc_sd[ys, xs])
    keep = np.abs(loc_sd[ys, xs] / sd_ref - 1) < 0.2     # sources with typical grain strength
    ys, xs = ys[keep], xs[keep]
    cur = np.where(hole[..., None], 0, hf).astype(np.float32)   # working HF canvas
    known = (~hole).astype(np.float32)
    my, mx = np.nonzero(hole)
    step = P - OV
    ramp = np.ones(P, np.float32); t = np.linspace(0, 1, OV + 2)[1:-1].astype(np.float32)
    ramp[:OV] = t
    for ty in range(my.min() - OV, my.max() + 1, step):
        for tx in range(mx.min() - OV, mx.max() + 1, step):
            ty0, tx0 = max(ty, 0), max(tx, 0)
            ty1, tx1 = min(ty + P, c.shape[0]), min(tx + P, c.shape[1])
            if not hole[ty0:ty1, tx0:tx1].any(): continue
            hh, ww = ty1 - ty0, tx1 - tx0
            kn = known[ty0:ty1, tx0:tx1]
            tgt = cur[ty0:ty1, tx0:tx1]
            idx = rng.integers(len(ys), size=ncand)
            cands = np.stack([hf[ys[i]:ys[i] + hh, xs[i]:xs[i] + ww] for i in idx])
            if kn.sum() > 0:
                cs = np.stack([hfs[ys[i]:ys[i] + hh, xs[i]:xs[i] + ww] for i in idx])
                ts = cv2.GaussianBlur(tgt, (0, 0), 2.5 * sc)
                err = (((cs - ts) ** 2).sum(-1) * kn).sum((1, 2)) / kn.sum()
                best = cands[int(np.argmin(err))]
            else:
                best = cands[0]
            # blend: weight of the new patch ramps up across the overlap with known pixels
            wy = ramp[ty0 - ty:ty0 - ty + hh] if ty >= 0 else ramp[:hh]
            wx = ramp[tx0 - tx:tx0 - tx + ww] if tx >= 0 else ramp[:ww]
            a = np.minimum.outer(wy, wx)
            a = np.where(kn > 0, a, 1.0)
            newv = tgt * (1 - a[..., None]) + best * a[..., None]
            hsub = hole[ty0:ty1, tx0:tx1]
            # only hole pixels are written; known sand stays untouched
            cur[ty0:ty1, tx0:tx1] = np.where(hsub[..., None], newv, tgt)
            known[ty0:ty1, tx0:tx1] = np.where(hsub, 1, kn)
    fill = lf_t + cur
    # alpha: 1 on the logo, fades to 0 across the band (original sand at the outer edge)
    dist = cv2.distanceTransform((~logo).astype(np.uint8), cv2.DIST_L2, 5)
    alpha = np.clip(1 - dist / f, 0, 1)
    alpha = cv2.GaussianBlur(alpha, (0, 0), 1.0) * hole
    alpha = np.where(logo, 1.0, alpha)[..., None]
    out = c * (1 - alpha) + fill * alpha
    res = im.copy()
    res[Y0:Y1, X0:X1] = out.clip(0, 255).astype(np.uint8)
    return res, mask
