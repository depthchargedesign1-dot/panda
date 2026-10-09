"""Build the single-mask price/option import files (owner, 6 Oct 2026).

Usage: MASK_DATA=<dir with m.jsonl, weights*.jsonl> python3 build.py
  m.jsonl        bulk export of mask products + variants (id, handle, title, status, options, variants)
  weights*.jsonl bulk export of every store variant: id, sku, inventoryItem.measurement.weight
Writes classification.csv, borderline.csv and import/*.csv next to this script.
"""
import csv, glob, json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from classify import rows, D  # noqa: E402

SCHEME = [  # (Style, Fitting, price, SKU suffix)
    ('Ready Cut', 'Elastic', '2.99', '-RC-E'),
    ('Ready Cut', 'Stick', '3.49', '-RC-S'),
    ('DIY', 'Elastic', '1.50', '-DIY-E'),
    ('DIY', 'Stick', '2.00', '-DIY-S'),
]
TEST_HANDLES = [
    'aaron-chalmers-tv-stars-2015-celebrity-face-mask',  # Default Title, £2.49
    None,  # Jake Paul £4.99 YouTuber (found below)
    'jack-joseph-face-mask',  # old Ready to Wear / DIY
]
PER_FILE = 2000  # products per import file
COLS = ['Handle', 'Title', 'Status', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value',
        'Variant SKU', 'Variant Price', 'Variant Inventory Policy', 'Variant Inventory Tracker',
        'Variant Fulfillment Service', 'Variant Requires Shipping', 'Variant Taxable', 'Variant Grams']

# weights + every SKU in the store
W, store_skus = {}, {}
for f in glob.glob(D + 'weights*.jsonl'):
    for line in open(f):
        o = json.loads(line)
        w = ((o.get('inventoryItem') or {}).get('measurement') or {}).get('weight')
        if w:
            g = w['value'] * {'GRAMS': 1, 'KILOGRAMS': 1000, 'POUNDS': 453.592, 'OUNCES': 28.3495}[w['unit']]
            W[o['id']] = round(g)
        if o.get('sku'):
            store_skus[o['sku'].strip().upper()] = o['id']


def num(gid):
    return gid.rsplit('/', 1)[-1]


def money(x):
    return '£%.2f' % float(x)


inc, cls_rows, border = [], [], []
for pid, p, vs, d, r in rows:
    old = '/'.join(money(v['price']) for v in vs)
    cls_rows.append([num(pid), p['handle'], p['title'], old, p['status'], d, r])
    if d == 'borderline':
        border.append([num(pid), p['handle'], p['title'], old, p['status'], r])
    if d == 'include':
        inc.append((pid, p, vs))

with open(os.path.join(HERE, 'classification.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['id', 'handle', 'title', 'old price', 'status', 'decision', 'reason'])
    w.writerows(sorted(cls_rows, key=lambda x: ({'include': 0, 'borderline': 1, 'exclude': 2}[x[5]], x[1])))
with open(os.path.join(HERE, 'borderline.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['id', 'handle', 'title', 'old price', 'status', 'why it is borderline (left unchanged)'])
    w.writerows(border)

jake = [p['handle'] for pid, p, vs in inc if p['title'].startswith('Jake Paul Face Mask – Fancy Dress')]
TEST_HANDLES[1] = jake[0]

new_skus, out = Counter(), {}
for pid, p, vs in inc:
    if len(vs) == 1:
        base_v = vs[0]
    else:  # old Ready to Wear / DIY: base on the Ready to Wear variant
        base_v = [v for v in vs if v['title'].lower() == 'ready to wear'][0]
    base = (base_v.get('sku') or '').strip() or 'FOXY-MASK-%s' % num(pid)
    grams = W.get(base_v['id'])
    lines = []
    for i, (style, fit, price, suf) in enumerate(SCHEME):
        sku = base + suf
        new_skus[sku.upper()] += 1
        lines.append({
            'Handle': p['handle'],
            'Title': p['title'] if i == 0 else '',
            'Status': p['status'].lower() if i == 0 else '',
            'Option1 Name': 'Style' if i == 0 else '', 'Option1 Value': style,
            'Option2 Name': 'Fitting' if i == 0 else '', 'Option2 Value': fit,
            'Variant SKU': sku, 'Variant Price': price,
            'Variant Inventory Policy': 'continue', 'Variant Inventory Tracker': '',
            'Variant Fulfillment Service': 'manual', 'Variant Requires Shipping': 'TRUE',
            'Variant Taxable': 'TRUE', 'Variant Grams': str(grams) if grams else '',
        })
    out[p['handle']] = lines

dups = [s for s, n in new_skus.items() if n > 1]
clash = [s for s in new_skus if s in store_skus]
assert not dups, dups[:5]
assert not clash, clash[:5]

imp = os.path.join(HERE, 'import')


def write(name, handles):
    with open(os.path.join(imp, name), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, COLS)
        w.writeheader()
        for h in handles:
            w.writerows(out[h])


write('00-TEST-3-masks.csv', TEST_HANDLES)
rest = [h for h in out if h not in TEST_HANDLES]
for k in range(0, len(rest), PER_FILE):
    write('%02d-single-masks.csv' % (k // PER_FILE + 1), rest[k:k + PER_FILE])

print('include', len(inc), 'borderline', len(border), 'exclude', sum(1 for r in cls_rows if r[5] == 'exclude'))
print('grams known', sum(1 for pid, p, vs in inc if any(W.get(v['id']) for v in vs)))
print('test', TEST_HANDLES)
