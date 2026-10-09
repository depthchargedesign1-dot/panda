"""Batch: remove the logo from every image detect.py found it in (score > 0.5).
Checks: nothing changes outside the logo neighbourhood; the logo can no longer be
found by the same template match. Saves JPEG q95 4:4:4, same size, ICC kept.
Usage: python3 batch.py <orig_dir> <detect.csv> <out_dir> <report.csv>"""
import sys, os, csv
import cv2, numpy as np
from PIL import Image
from remove import remove_logo
cv2.setNumThreads(1)

orig, det, outd, rep = sys.argv[1:5]
shard, nshard = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (0, 1)
os.makedirs(outd, exist_ok=True)
ref = cv2.imread(os.path.join(orig, '33587616186619.jpg'))
tpl = ref[60:335, 1365:1935]

def edges(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(cv2.Canny(cv2.GaussianBlur(g, (3, 3), 0), 60, 160).astype(np.float32), (5, 5), 0)

def rescore(img, box):
    x0, y0, x1, y1 = box
    t = cv2.resize(tpl, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA)
    pad = 20
    sub = img[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad]
    return float(cv2.matchTemplate(edges(sub), edges(t), cv2.TM_CCOEFF_NORMED).max())

rows = []
for n, d in enumerate(csv.DictReader(open(det))):
    if float(d['score']) <= 0.5 or n % nshard != shard: continue
    mid = d['mid']; box = tuple(int(d[k]) for k in ('x0', 'y0', 'x1', 'y1'))
    src = os.path.join(orig, mid + '.jpg')
    im = cv2.imread(src)
    res, mask = remove_logo(im, box)
    diff = np.abs(res.astype(int) - im.astype(int)).max(-1) > 0
    sc = im.shape[1] / 2000
    allowed = np.zeros_like(diff); m = int(40 * sc)
    allowed[box[1] - m:box[3] + m, box[0] - m:box[2] + m] = True
    outside = int((diff & ~allowed).sum())
    after = rescore(res, box)
    pil = Image.open(src)
    Image.fromarray(cv2.cvtColor(res, cv2.COLOR_BGR2RGB)).save(
        os.path.join(outd, mid + '.jpg'), quality=95, subsampling=0,
        icc_profile=pil.info.get('icc_profile'))
    rows.append(dict(mid=mid, w=im.shape[1], h=im.shape[0], before=d['score'],
                     after=round(after, 3), changed_px=int(diff.sum()), outside_px=outside,
                     ok=int(outside == 0 and after < 0.35)))
    print(rows[-1], flush=True)
with open(rep, 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
