"""Find the DCD TEAMWEAR logo in every towel image (multi-scale template match).
Usage: python3 detect.py <orig_dir> <out_csv>"""
import sys, glob, os, csv
import cv2, numpy as np

ref = cv2.imread(os.path.join(sys.argv[1], '33587616186619.jpg'))
X0, Y0, X1, Y1 = 1365, 60, 1935, 335          # logo box in the 2000px reference
tpl_full = ref[Y0:Y1, X0:X1]
W = 800                                        # working width for search

def prep(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(cv2.GaussianBlur(g, (3, 3), 0), 60, 160).astype(np.float32)

rows = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.jpg'))):
    img = cv2.imread(f); h, w = img.shape[:2]
    s = W / w; small = cv2.resize(img, (W, int(h * s)), interpolation=cv2.INTER_AREA)
    es = cv2.GaussianBlur(prep(small), (5, 5), 0)
    best = (-1, None, None)
    for tw in range(120, 420, 10):             # logo width in working px
        k = tw / tpl_full.shape[1]
        t = cv2.resize(tpl_full, (tw, max(8, int(tpl_full.shape[0] * k))), interpolation=cv2.INTER_AREA)
        if t.shape[0] >= es.shape[0] or t.shape[1] >= es.shape[1]: continue
        et = cv2.GaussianBlur(prep(t), (5, 5), 0)
        r = cv2.matchTemplate(es, et, cv2.TM_CCOEFF_NORMED)
        _, mv, _, ml = cv2.minMaxLoc(r)
        if mv > best[0]: best = (mv, ml, t.shape[1::-1])
    mv, (x, y), (tw, th) = best
    rows.append(dict(mid=os.path.basename(f)[:-4], w=w, h=h, score=round(mv, 3),
                     x0=int(x / s), y0=int(y / s), x1=int((x + tw) / s), y1=int((y + th) / s)))
    print(rows[-1], flush=True)
with open(sys.argv[2], 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
