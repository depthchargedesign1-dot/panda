"""Before/after contact sheet: for each media id, the full image (before | after) plus a 1:1 crop of the logo area.
Usage: python3 contact_sheet.py <orig_dir> <clean_dir> <detect.csv> <out.jpg> mid1 mid2 ..."""
import sys, csv
from PIL import Image, ImageDraw
o, c, det, out = sys.argv[1:5]; mids = sys.argv[5:]
boxes = {d['mid']: tuple(int(d[k]) for k in ('x0', 'y0', 'x1', 'y1')) for d in csv.DictReader(open(det))}
TW, CW = 420, 360
rows = []
for mid in mids:
    a = Image.open(f'{o}/{mid}.jpg'); b = Image.open(f'{c}/{mid}.jpg')
    x0, y0, x1, y1 = boxes[mid]; m = 40
    crop = (x0 - m, y0 - m, x1 + m, y1 + m)
    tiles = []
    for im in (a, b):
        t = im.copy(); t.thumbnail((TW, TW)); tiles.append(t)
    for im in (a, b):
        t = im.crop(crop); t.thumbnail((CW, CW)); tiles.append(t)
    h = max(t.size[1] for t in tiles) + 24
    row = Image.new('RGB', (2 * TW + 2 * CW + 50, h), 'white')
    x = 5
    for t in tiles: row.paste(t, (x, 20)); x += t.size[0] + 10
    ImageDraw.Draw(row).text((5, 4), f'{mid}   before | after | logo area before | after', fill='black')
    rows.append(row)
sheet = Image.new('RGB', (rows[0].size[0], sum(r.size[1] for r in rows)), 'white')
y = 0
for r in rows: sheet.paste(r, (0, y)); y += r.size[1]
sheet.save(out, quality=88)
