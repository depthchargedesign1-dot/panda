#!/usr/bin/env python3
"""
Turns the AWDis studio photos (from Dropbox: /New Jobs 2026/3025 awdis hoodie colours and the Ralawise
JH009 / JH043 shots) into the garment photos the designer draws prints onto.

  python3 tools/process-photos.py <raw-dir> <out-dir>

  <raw-dir>/jh001/JH001_<Colour>_FRONT.jpg|_FT.jpg|_BACK.jpg   College Hoodie: one real photo per colour and view
  <raw-dir>/raw/jh043_*.jpg, jh009_*.jpg                       Varsity / Baseball fronts

Every photo is placed on a 1000 x 1000 white square with the garment at the same size and position, so one
set of print positions (in leavers-photos.js) fits every colour. Varsity and Baseball colourways without
their own photo are recoloured from a real photo of the same garment, and their back views are retouched
from the real front (studs, placket, pockets, drawcords and hood opening removed).
"""
import json, os, re, sys, glob
import numpy as np
import cv2
from PIL import Image

RAW, OUT = sys.argv[1], sys.argv[2]
SIZE = 1000
manifest = {}


def save(img_bgr, product, cid, view):
    d = os.path.join(OUT, product)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f'ld-{product}-{cid}-{view}.jpg')
    cv2.imwrite(path, img_bgr, [cv2.IMWRITE_JPEG_QUALITY, 80, cv2.IMWRITE_JPEG_PROGRESSIVE, 1])
    if view == 'front':
        thumb = cv2.resize(img_bgr, (180, 180), interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(d, f'ld-{product}-{cid}-thumb.jpg'), thumb, [cv2.IMWRITE_JPEG_QUALITY, 82])
    return os.path.basename(path)


def garment_mask(img):
    diff = (255 - img.astype(int)).max(axis=2)
    m = (diff > 14).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:
        big = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        m = (lab == big).astype(np.uint8)
    # fill holes (light areas inside the garment)
    inv = 1 - m
    n, lab, stats, _ = cv2.connectedComponentsWithStats(inv)
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        if x > 0 and y > 0 and x + w < m.shape[1] and y + h < m.shape[0]:
            m[lab == i] = 1
    return m


def normalise(img, height=880, top=60):
    """Scale so the garment is `height` px tall, centred, on a white 1000 square."""
    m = garment_mask(img)
    ys, xs = np.where(m > 0)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    crop = img[y0:y1 + 1, x0:x1 + 1]
    s = height / crop.shape[0]
    crop = cv2.resize(crop, (round(crop.shape[1] * s), height), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    canvas = np.full((SIZE, SIZE, 3), 255, np.uint8)
    w = crop.shape[1]
    x = (SIZE - w) // 2
    canvas[top:top + height, x:x + w] = crop
    return canvas


def sample_hex(img, box):
    x0, y0, x1, y1 = box
    px = img[y0:y1, x0:x1].reshape(-1, 3)
    b, g, r = np.median(px, axis=0)
    return '#%02X%02X%02X' % (int(r), int(g), int(b))


def hex_lab(hexv):
    r, g, b = int(hexv[1:3], 16), int(hexv[3:5], 16), int(hexv[5:7], 16)
    return cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2LAB)[0, 0].astype(float)


def recolour(img, mask, target_hex, contrast=1.0):
    """Repaint the masked fabric in target colour, keeping the photo's folds and texture."""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(float)
    t = hex_lab(target_hex)
    sel = mask > 0
    L = lab[..., 0]
    mean = np.median(L[sel])
    # Lighter targets need gentler shading so folds don't turn muddy.
    k = contrast * (0.75 if t[0] > 200 else 1.0)
    out = lab.copy()
    newL = t[0] + (L - mean) * k
    out[..., 0] = np.where(sel, np.clip(newL, 0, 255), L)
    out[..., 1] = np.where(sel, t[1], lab[..., 1])
    out[..., 2] = np.where(sel, t[2], lab[..., 2])
    res = cv2.cvtColor(out.astype(np.uint8), cv2.COLOR_LAB2BGR)
    # feather the mask edge
    soft = cv2.GaussianBlur(mask.astype(np.float32), (5, 5), 0)[..., None]
    return (res * soft + img * (1 - soft)).astype(np.uint8)


def kebab(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()


def words(name):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', name)


# ------------------------------------------------------------------ JH001 College Hoodie (all real photos)

fixed = {'AirforceBlue': 'AirForceBlue'}
pairs = {}
for f in glob.glob(os.path.join(RAW, 'jh001', 'JH001_*.jpg')):
    m = re.match(r'JH001_([A-Za-z]+)_(FRONT|FT|BACK)\.jpg', os.path.basename(f))
    if not m:
        continue
    colour = fixed.get(m.group(1), m.group(1))
    view = 'back' if m.group(2) == 'BACK' else 'front'
    pairs.setdefault(colour, {})[view] = f

college = []
for colour in sorted(pairs):
    v = pairs[colour]
    if 'front' not in v or 'back' not in v:
        print('skip (missing view):', colour)
        continue
    cid = kebab(colour)
    files = {}
    for view in ('front', 'back'):
        img = cv2.imread(v[view])
        img = cv2.resize(img, (SIZE, SIZE), interpolation=cv2.INTER_AREA)
        files[view] = save(img, 'college-hoodie', cid, view)
        if view == 'back':
            hexv = sample_hex(img, (430, 420, 570, 560))
    college.append({'id': cid, 'name': words(colour), 'hex': hexv, 'files': files})
manifest['college-hoodie'] = college
print('college colours', len(college))

# ------------------------------------------------------------------ JH043 Varsity Jacket

def varsity_masks(img):
    g = garment_mask(img)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(float)
    L = lab[..., 0]
    body = ((L < 110) & (g > 0)).astype(np.uint8)
    light = ((L >= 110) & (g > 0)).astype(np.uint8)
    # popper studs and the neck label stay as they are: small, roundish bright blobs inside the body
    keep = np.zeros_like(light)
    n, lab_, stats, _ = cv2.connectedComponentsWithStats(light)
    for i in range(1, n):
        x, y, w, h, a = stats[i]
        if a < 2600 and max(w, h) / max(1, min(w, h)) < 1.7 and SIZE * 0.35 < x + w / 2 < SIZE * 0.65:
            keep[lab_ == i] = 1
    sleeve = light * (1 - keep)
    return body, sleeve, keep


def resurface(img, region, patch_box, valid, sigma=22):
    """Replace a region with clean fabric: texture tiled from a clean patch, shading from nearby `valid` fabric."""
    x0, y0, x1, y1 = patch_box
    patch = img[y0:y1, x0:x1].astype(np.float32)
    tile = np.concatenate([patch, patch[:, ::-1]], 1)
    tile = np.concatenate([tile, tile[::-1]], 0)
    tex = np.tile(tile, (SIZE // tile.shape[0] + 1, SIZE // tile.shape[1] + 1, 1))[:SIZE, :SIZE]
    hf = tex - cv2.GaussianBlur(tex, (0, 0), 10)
    v = valid.astype(np.float32)
    num = cv2.GaussianBlur(img.astype(np.float32) * v[..., None], (0, 0), sigma)
    den = cv2.GaussianBlur(v, (0, 0), sigma)[..., None] + 1e-4
    lf = num / den
    new = np.clip(lf + hf, 0, 255)
    soft = cv2.GaussianBlur(region.astype(np.float32), (0, 0), 1.5)[..., None]
    return (new * soft + img * (1 - soft)).astype(np.uint8)


def varsity_back(img):
    """Retouch a real front into a back: plain body panel (no studs, placket or pockets), closed hem rib."""
    out = img.copy()
    out[800:880, 440:560] = img[800:880, 320:440]
    g = garment_mask(img)
    L = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[..., 0]
    fabric = (g > 0) & (L < 110)
    region = np.zeros(img.shape[:2], np.uint8)
    region[205:802, 296:694] = 1
    region &= fabric.astype(np.uint8) | ((L >= 110) & (region > 0) & (np.abs(np.arange(SIZE) - 500)[None, :] < 215)).astype(np.uint8)
    valid = fabric.copy()
    valid[:, 450:550] = False  # ignore the placket seam
    out = resurface(out, region, (320, 250, 420, 450), valid)
    return back_collar(out, valid)


def back_collar(img, valid):
    """Back of a varsity collar: the shoulders run up into a ribbed band that wraps round the back of the
    neck (curved neck seam, rounded ends, two stripes following the curve). No front V-neck or studs."""
    out = img.copy()
    body_col = np.median(img[300:450, 330:420].reshape(-1, 3), axis=0)
    xs = np.arange(SIZE)
    # collar outline: top edge and neck seam, both dipping slightly at the centre back
    def curve(x, ends, mid):
        return mid + (ends - mid) * ((x - 500) / 150.0) ** 2
    x0, x1 = 352, 648
    top = lambda x: curve(x, 96, 106)
    seam = lambda x: curve(x, 136, 152)
    # 1. shoulder line from the real photo's shoulders up to the collar ends; everything above it is background
    shoulder = np.interp(xs, [300, 318, 340, x0, x1, 660, 682, 700], [156, 150, 142, seam(x0), seam(x1), 142, 150, 165])
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    zone = (xx > 305) & (xx < 695) & (yy < 250)
    above = zone & (yy < shoulder[None, :])
    out[above] = 255
    # 2. the upper back panel below the shoulder line: clean fabric, shading taken from the fabric lower down
    panel = (zone & ~above & (yy < 245)).astype(np.uint8)
    out[(panel > 0) & (out.mean(axis=2) > 170)] = body_col
    below = valid.copy()
    below[:250] = False
    new = resurface(out, panel, (320, 250, 420, 450), below, sigma=30).astype(np.float32)
    # feather into the real fabric so there is no visible edge; fully new where the front collar used to be
    core = ((xx > 340) & (xx < 660) & (yy < 175) & (panel > 0)).astype(np.float32)
    w = np.maximum(cv2.GaussianBlur(panel.astype(np.float32) * ((xx > 330) & (xx < 670)), (0, 0), 14), core)
    w = np.clip(w * 1.3, 0, 1) * panel
    out = (new * w[..., None] + out.astype(np.float32) * (1 - w[..., None])).astype(np.uint8)
    # 3. the ribbed collar band
    band = np.zeros((SIZE, SIZE), np.uint8)
    tops = [(x, int(round(top(x)))) for x in range(x0 + 8, x1 - 7, 4)]
    seams = [(x, int(round(seam(x)))) for x in range(x1, x0 - 1, -4)]
    cv2.fillPoly(band, [np.array(tops + seams, np.int32)], 1)
    band = cv2.GaussianBlur(band.astype(np.float32), (0, 0), 1.2)
    ty = top(xx.astype(float))
    sy = seam(xx.astype(float))
    f = np.clip((yy - ty) / np.maximum(sy - ty, 1), 0, 1)        # 0 at the top edge, 1 at the neck seam
    rib = body_col[None, None, :] * (1.04 - 0.16 * f[..., None]) + 7 * np.sin(xx * 2 * np.pi / 6.5)[..., None]
    # two contrast stripes running along the band, curved with it
    stripe = np.zeros_like(f)
    for c in (0.24, 0.52):
        stripe = np.maximum(stripe, np.clip(1 - np.abs(f - c) / 0.085, 0, 1) ** 0.6)
    trim = np.array([238, 238, 238], np.float32) * (0.97 + 0.03 * np.sin(xx * 2 * np.pi / 6.5))[..., None]
    rib = rib * (1 - stripe[..., None]) + trim * stripe[..., None]
    # rounded ends: the band turns away round the side of the neck, so it darkens at each end
    turn = np.clip(1 - np.abs(xx - 500) / 148.0, 0, 1) ** 0.25
    rib = rib * (0.62 + 0.38 * turn[..., None])
    m = band[..., None]
    out = (np.clip(rib, 0, 255) * m + out * (1 - m)).astype(np.uint8)
    # 4. a soft shadow on the body just under the collar, and a darker neck seam
    shadow = np.clip(1 - np.abs(yy - sy - 6) / 10.0, 0, 1) * (np.abs(xx - 500) < 150) * (yy > sy)
    out = (out * (1 - 0.35 * shadow[..., None])).astype(np.uint8)
    return out


VARSITY_REAL = {
    'jet-black--white': 'jh043_black_white.jpg',
    'jet-black--heather-grey': 'jh043_black_grey.jpg',
    'jet-black--fire-red': 'jh043_black_red.jpg',
    'jet-black--sun-yellow': 'jh043_black_yellow.jpg',
    'burgundy--heather-grey': 'jh043_burgundy_grey.jpg',
}
VARSITY_WAYS = [
    ('jet-black', 'white'), ('jet-black', 'fire-red'), ('jet-black', 'sun-yellow'), ('jet-black', 'hot-pink'),
    ('jet-black', 'heather-grey'), ('jet-black', 'charcoal'), ('oxford-navy', 'white'), ('oxford-navy', 'heather-grey'),
    ('oxford-navy', 'burgundy'), ('burgundy', 'heather-grey'), ('fire-red', 'white'), ('royal-blue', 'white'),
    ('sapphire', 'heather-grey'), ('kelly-green', 'white'), ('purple', 'white'), ('heather-grey', 'white')
]
COLOURS = {
    'jet-black': ('Jet Black', '#1C1C1F'), 'white': ('White', '#F4F4F2'), 'fire-red': ('Fire Red', '#C3132C'),
    'sun-yellow': ('Sun Yellow', '#F4C20D'), 'hot-pink': ('Hot Pink', '#E2317D'), 'heather-grey': ('Heather Grey', '#A8AAAF'),
    'charcoal': ('Charcoal', '#3E4045'), 'oxford-navy': ('Oxford Navy', '#1F2A44'), 'burgundy': ('Burgundy', '#6B1A2C'),
    'royal-blue': ('Royal Blue', '#2149A6'), 'sapphire': ('Sapphire Blue', '#1677C6'), 'kelly-green': ('Kelly Green', '#1F8A3D'),
    'purple': ('Purple', '#4B2A82'), 'arctic-white': ('Arctic White', '#F3F3F1'), 'gold': ('Gold', '#E0A526'),
    'baby-pink': ('Baby Pink', '#F4C3D5')
}

base = normalise(cv2.imread(os.path.join(RAW, 'raw', 'jh043_black_white.jpg')))
base_back = varsity_back(base)
vbody, vsleeve, _ = varsity_masks(base)
bbody, bsleeve, _ = varsity_masks(base_back)
varsity = []
for body, trim in VARSITY_WAYS:
    cid = f'{body}--{trim}'
    files = {}
    real = VARSITY_REAL.get(cid)
    front = normalise(cv2.imread(os.path.join(RAW, 'raw', real))) if real else None
    if front is None:
        front = recolour(recolour(base, vbody, COLOURS[body][1], 1.6), vsleeve, COLOURS[trim][1])
    back = recolour(recolour(base_back, bbody, COLOURS[body][1], 1.6), bsleeve, COLOURS[trim][1])
    files['front'] = save(front, 'varsity-jacket', cid, 'front')
    files['back'] = save(back, 'varsity-jacket', cid, 'back')
    varsity.append({'id': cid, 'name': f'{COLOURS[body][0]} / {COLOURS[trim][0]}', 'hex': COLOURS[body][1], 'trim': COLOURS[trim][1],
                    'real': bool(real), 'files': files})
manifest['varsity-jacket'] = varsity

# ------------------------------------------------------------------ JH009 Baseball Hoodie

def baseball_masks(img):
    g = garment_mask(img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(int)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(int)
    chroma = np.hypot(lab[..., 1] - 128, lab[..., 2] - 128)
    body = ((chroma > 12) & (g > 0)).astype(np.uint8)
    body = cv2.morphologyEx(body, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    trim = ((g > 0) & (body == 0) & (lab[..., 0] < 200)).astype(np.uint8)
    return body, trim


def baseball_back(img):
    """Retouch the real front into a back: solid hood, plain body (no cords, eyelets or pocket)."""
    g = garment_mask(img)
    body_m, trim_m = baseball_masks(img)
    hood = np.zeros(img.shape[:2], np.uint8)
    cv2.fillPoly(hood, [np.array([[368, 178], [376, 70], [430, 50], [570, 50], [624, 70], [632, 178], [560, 210], [440, 210]])], 1)
    hood &= g
    L = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[..., 0].astype(float)
    sleeve_L = np.median(L[(trim_m > 0) & (np.arange(SIZE)[:, None] > 300)])
    # hood shading from the outer hood fabric only (the inside of the hood is darker)
    valid_hood = (trim_m > 0) & (np.abs(L - sleeve_L) < 18)
    out = resurface(img, hood, (215, 320, 265, 520), valid_hood, sigma=30)
    body = np.zeros_like(hood)
    body[205:800, 318:682] = 1
    # only the body panel (keep the raglan sleeves), plus the drawcords hanging over it
    centre = np.zeros_like(hood)
    centre[:, 440:560] = 1
    body &= g & ((cv2.dilate(body_m, np.ones((3, 3), np.uint8)) > 0) | (centre > 0)).astype(np.uint8)
    out = resurface(out, body, (330, 300, 430, 500), body_m > 0)
    return out


BASEBALL_WAYS = [
    ('jet-black', 'fire-red'), ('jet-black', 'gold'), ('jet-black', 'sapphire'), ('jet-black', 'arctic-white'),
    ('charcoal', 'jet-black'), ('charcoal', 'heather-grey'), ('heather-grey', 'jet-black'), ('heather-grey', 'oxford-navy'),
    ('oxford-navy', 'heather-grey'), ('oxford-navy', 'burgundy'), ('arctic-white', 'jet-black'), ('burgundy', 'charcoal'),
    ('baby-pink', 'heather-grey')
]
braw = normalise(cv2.imread(os.path.join(RAW, 'raw', 'jh009_burgundy_charcoal_ft.jpg')))
braw_back = baseball_back(braw)
fb, ft = baseball_masks(braw)
bb, bt = baseball_masks(braw_back)
baseball = []
for body, trim in BASEBALL_WAYS:
    cid = f'{body}--{trim}'
    real = cid == 'burgundy--charcoal'
    front = braw if real else recolour(recolour(braw, fb, COLOURS[body][1], 1.4), ft, COLOURS[trim][1], 1.2)
    back = braw_back if real else recolour(recolour(braw_back, bb, COLOURS[body][1], 1.4), bt, COLOURS[trim][1], 1.2)
    files = {'front': save(front, 'baseball-hoodie', cid, 'front'), 'back': save(back, 'baseball-hoodie', cid, 'back')}
    baseball.append({'id': cid, 'name': f'{COLOURS[body][0]} / {COLOURS[trim][0]}', 'hex': COLOURS[body][1], 'trim': COLOURS[trim][1],
                     'real': real, 'files': files})
manifest['baseball-hoodie'] = baseball

with open(os.path.join(OUT, 'manifest.json'), 'w') as f:
    json.dump(manifest, f, indent=1)
print({k: len(v) for k, v in manifest.items()})
