"""Build the word art designer's shape masks from each product's framed photo.

For every Word Art product: take the black-frame photo (else the first photo), find the paper inside the
frame, and turn the artwork on it into an RGBA PNG the size of the paper:
  alpha = the artwork's shape (words merged into a solid, smoothed silhouette)
  RGB   = the artwork's own colours, spread smoothly across the shape (so rainbow numbers stay rainbow)
The designer fills that shape with the customer's words and colours each word from the RGB under it.

Usage: python3 make_masks.py products_all.json out_dir [handle ...]
"""
import io, json, os, sys, urllib.request
import numpy as np
import cv2
from scipy import ndimage as ndi
from PIL import Image

MAX_SIDE = 640


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return np.array(Image.open(io.BytesIO(r.read())).convert('RGB'))


def paper_rect(rgb):
    """Bounding box (x0,y0,x1,y1) of the paper inside the frame, or None."""
    h, w = rgb.shape[:2]
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    # Black frames are dark; silver frames are grey and low-saturation - we prefer black-frame photos.
    dark = (gray < 75).astype(np.uint8)
    dark = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    lab, n = ndi.label(dark)
    best = None
    for i in range(1, n + 1):
        comp = lab == i
        area = comp.sum()
        if area < 0.01 * h * w:
            continue
        filled = ndi.binary_fill_holes(comp)
        inner = filled & ~comp
        ia = inner.sum()
        if ia < 0.08 * h * w:
            continue
        if best is None or ia > best[0]:
            best = (ia, inner)
    if best is None:
        return None
    inner = best[1]
    # largest inner component = paper (+ artwork that's enclosed)
    lab2, n2 = ndi.label(inner)
    sizes = ndi.sum(inner, lab2, range(1, n2 + 1))
    paper = lab2 == (1 + int(np.argmax(sizes)))
    paper = ndi.binary_fill_holes(paper)
    ys, xs = np.where(paper)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    # trim the frame's shadow/bevel: inset 3%
    ix, iy = int((x1 - x0) * 0.03), int((y1 - y0) * 0.03)
    return x0 + ix, y0 + iy, x1 - ix, y1 - iy


def stretch(col, inside):
    """Picture-style artwork (dogs, figures) has a wide range of shades: spread them out so the picture still
    reads when it is re-made from words. Single-colour artwork (a pink heart) is left as it is."""
    lum = (0.2126 * col[..., 0] + 0.7152 * col[..., 1] + 0.0722 * col[..., 2]) / 255
    v = lum[inside]
    if v.size < 50:
        return col
    lo, hi = np.percentile(v, 3), np.percentile(v, 97)
    if hi - lo < 0.18:
        return col
    t = np.clip((lum - lo) / (hi - lo), 0, 1)
    target = 0.12 + t * 0.7
    k = (target / np.maximum(lum, 1e-3))[..., None]
    out = col * k
    # brighten towards white without clipping hue
    over = out.max(axis=2, keepdims=True)
    out = np.where(over > 255, out * (255 / np.maximum(over, 1)), out)
    return out


def drop_example_name(f, ink, diff):
    """Name letters (Pink/Blue Letter A-Z) have an example name printed big and dark across the letter.
    Remove it, then rebuild the letter through the gap it leaves: in each column, join the letter above
    the name band to the letter below it."""
    h, w = ink.shape
    lum = (0.2126 * f[..., 0] + 0.7152 * f[..., 1] + 0.0722 * f[..., 2]) / 255
    med = np.median(lum[ink]) if ink.any() else 1
    dark = ink & (lum < med * 0.62)
    dark = cv2.dilate(dark.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    rows = np.where(dark.sum(axis=1) > w * 0.04)[0]
    body = ink & ~dark
    if rows.size:
        r0, r1 = rows.min(), rows.max()
        k = max(3, int(min(h, w) * 0.025)) | 1
        solid = cv2.morphologyEx(body.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))).astype(bool)
        look = max(4, int(h * 0.03))
        for x in range(w):
            above = solid[max(0, r0 - look):r0, x].any()
            below = solid[r1 + 1:r1 + 1 + look, x].any()
            if above and below:
                body[r0:r1 + 1, x] = True
    diff = np.where(dark, 0, diff)
    return body, diff


def shape_from_paper(crop, letter=False):
    h, w = crop.shape[:2]
    f = crop.astype(np.float32)
    # paper colour: median of a border strip
    b = max(3, int(min(h, w) * 0.03))
    border = np.concatenate([f[:b].reshape(-1, 3), f[-b:].reshape(-1, 3), f[:, :b].reshape(-1, 3), f[:, -b:].reshape(-1, 3)])
    paper = np.median(border, axis=0)
    # allow for gentle shading across the paper: compare with a heavily blurred background estimate
    diff = np.abs(f - paper).max(axis=2)
    ink = diff > 45
    if letter:
        ink, diff = drop_example_name(f, ink, diff)
    # Words merge into a solid shape
    k = max(3, int(min(h, w) * 0.025)) | 1
    ink_u8 = ink.astype(np.uint8)
    solid = cv2.morphologyEx(ink_u8, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    # Fill only small gaps between words. Big white areas inside the artwork stay open: they are part of
    # the design (a beagle's white blaze and muzzle, the hole in a 6, 8 or 0).
    holes = ndi.binary_fill_holes(solid) & ~solid.astype(bool)
    hl, hn = ndi.label(holes)
    if hn:
        hs = ndi.sum(holes, hl, range(1, hn + 1))
        small = np.isin(hl, 1 + np.where(hs < 0.006 * h * w)[0])
        solid = (solid.astype(bool) | small).astype(np.uint8)
    # drop specks (< 0.4% of the paper)
    lab, n = ndi.label(solid)
    if n:
        sizes = ndi.sum(solid, lab, range(1, n + 1))
        keep_ids = []
        for i, sz in enumerate(sizes, start=1):
            if sz < 0.004 * h * w:
                continue
            ys, xs = np.where(lab == i)
            touches = ys.min() == 0 or xs.min() == 0 or ys.max() == h - 1 or xs.max() == w - 1
            if touches and sz < 0.05 * h * w:  # a sliver of frame or shadow, not artwork
                continue
            keep_ids.append(i)
        solid = np.isin(lab, keep_ids).astype(np.uint8)
    # smooth the outline
    sm = cv2.GaussianBlur(solid.astype(np.float32), (0, 0), max(1.0, min(h, w) * 0.006))
    alpha = (sm > 0.5).astype(np.float32)
    # colour field: average ink colour, spread over the shape (normalised blur)
    # weight by ink strength so the solid middle of each letter counts, not its pale anti-aliased edge
    wgt = (np.clip((diff - 45) / 120, 0, 1) ** 2) * alpha
    col = np.zeros_like(f)
    sigma = max(2.0, min(h, w) * 0.02)
    den = cv2.GaussianBlur(wgt, (0, 0), sigma) + 1e-6
    for c in range(3):
        col[..., c] = cv2.GaussianBlur(f[..., c] * wgt, (0, 0), sigma) / den
    # where nothing nearby, use a much wider blur
    den2 = cv2.GaussianBlur(wgt, (0, 0), sigma * 6) + 1e-6
    sparse = den < 0.02
    for c in range(3):
        wide = cv2.GaussianBlur(f[..., c] * wgt, (0, 0), sigma * 6) / den2
        col[..., c] = np.where(sparse, wide, col[..., c])
    col = stretch(col, alpha > 0.5)
    rgba = np.dstack([np.clip(col, 0, 255), alpha * 255]).astype(np.uint8)
    return rgba, float(alpha.mean())


def pick_image(p):
    imgs = [m for m in p['media']['nodes'] if m and m.get('image')]
    for m in imgs:
        if 'black frame' in (m.get('alt') or '').lower():
            return m
    return imgs[0] if imgs else None


def main():
    products = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    only = set(sys.argv[3:])
    os.makedirs(out, exist_ok=True)
    report = []
    for p in products:
        if only and p['handle'] not in only:
            continue
        m = pick_image(p)
        row = {'id': p['id'], 'handle': p['handle'], 'title': p['title']}
        if not m:
            row['error'] = 'no image'; report.append(row); continue
        try:
            rgb = fetch(m['image']['url'])
            r = paper_rect(rgb)
            if r is None:
                row['error'] = 'no frame found'; report.append(row); continue
            x0, y0, x1, y1 = r
            crop = rgb[y0:y1, x0:x1]
            rgba, cover = shape_from_paper(crop, letter='wa-names' in p.get('tags', []))
            im = Image.fromarray(rgba, 'RGBA')
            s = MAX_SIDE / max(im.size)
            if s < 1:
                im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            fn = os.path.join(out, p['handle'] + '.png')
            im.save(fn, optimize=True)
            row.update({'file': fn, 'src': m['image']['url'], 'size': im.size, 'coverage': round(cover, 3)})
        except Exception as e:  # noqa
            row['error'] = repr(e)
        report.append(row)
        print(row.get('handle'), row.get('size'), row.get('coverage'), row.get('error', ''), flush=True)
    json.dump(report, open(os.path.join(out, 'report.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
