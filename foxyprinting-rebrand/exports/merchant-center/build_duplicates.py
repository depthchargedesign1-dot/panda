"""Build the 2026-10-06 Merchant Center duplicate report from two bulk exports (read only, nothing changed).
usage: python3 build_duplicates.py products.jsonl media.jsonl conflicted_identical.csv outdir"""
import json, re, collections, hashlib, csv, sys, os

prod_f, media_f, ident_f, outdir = sys.argv[1:5]
P = [json.loads(l) for l in open(prod_f)]
IMG = {}
for l in open(media_f):
    m = json.loads(l); im = (m.get('featuredMedia') or {}).get('image')
    if im:
        fn = im['url'].split('?')[0].rsplit('/', 1)[-1]
        fn = re.sub(r'_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?=\.)', '', fn)
        IMG[m['id']] = (fn.lower(), im['width'], im['height'])
KNOWN58 = {r['id']: r['twin_id'] for r in csv.DictReader(open(ident_f))}

def nt(t):
    t = re.sub(r'\(\s*copy\s*\)|\bcopy of\b', '', t, flags=re.I)
    return re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip()
def nd(d): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', d or '')).strip().lower()
COPY_RX = re.compile(r'(^copy-of-|-copy(-|$))')
def is_copy(p): return bool(COPY_RX.search(p['handle']) or re.search(r'\(\s*copy\s*\)|\bcopy of\b', p['title'], re.I))
def nid(g): return g.split('/')[-1]

A = [p for p in P if p['status'] == 'ACTIVE']
H = {p['handle']: p for p in P}
groups = collections.defaultdict(list)
for p in A:
    groups[(nt(p['title']), hashlib.md5(nd(p['descriptionHtml']).encode()).hexdigest())].append(p)

rows, done = [], set()
def img_rel(a, b):
    ia, ib = IMG.get(a['id']), IMG.get(b['id'])
    if not ia or not ib: return 'no image on one or both'
    return 'same image file' if ia == ib else 'different image'

for (t, h), v in groups.items():
    if len(v) < 2: continue
    v = sorted(v, key=lambda p: (is_copy(p), p['createdAt'], int(nid(p['id']))))
    orig = v[0]
    for p in v[1:]:
        rel = img_rel(p, orig)
        known = p['id'] in KNOWN58
        if known:
            rec = 'Set to DRAFT + URL redirect to original (owner kept ACTIVE on 5 Oct 2026; revisit only if Merchant Center flags it)'
        elif rel == 'different image':
            rec = 'Make unique: give the title the next free number (different image) and rewrite the description'
        else:
            rec = 'Set to DRAFT + URL redirect to original'
        reason = 'same title + identical description' + (' + copy in handle/title' if is_copy(p) else '')
        prio = 'HIGH' if rel != 'different image' else 'MEDIUM'
        rows.append([p['id'], p['title'], p['handle'], p['status'], orig['id'], rec, reason, rel, prio,
                     'yes' if known else '', p['productType']])
        done.add(p['id'])

# copy-handle/title products not already covered
for p in A:
    if p['id'] in done or not is_copy(p): continue
    base = re.sub(r'-copy(-\d+)?$', '', re.sub(r'^copy-of-(copy-of-)*', '', p['handle']))
    base = re.sub(r'-copy(?=-)', '', base)
    twin = H.get(base) if base != p['handle'] else None
    if twin and twin['id'] != p['id']:
        same_desc = nd(twin['descriptionHtml']) == nd(p['descriptionHtml'])
        rel = img_rel(p, twin)
        if same_desc and rel == 'same image file':
            rec, prio = 'Set to DRAFT + URL redirect to original', 'HIGH'
        else:
            rec, prio = 'Make unique: tidy the handle (drop "copy", with redirect) and rewrite the description if it matches', 'LOW'
        reason = 'copy in handle/title; twin handle exists' + ('; identical description' if same_desc else '; different description')
        rows.append([p['id'], p['title'], p['handle'], p['status'], twin['id'], rec, reason, rel, prio,
                     'yes' if p['id'] in KNOWN58 else '', p['productType']])
    else:
        rows.append([p['id'], p['title'], p['handle'], p['status'], '', 'Keep ACTIVE; optional: tidy the handle (drop "copy", with redirect)',
                     'copy in handle/title only; no twin found', '', 'LOW', '', p['productType']])

HELPER = re.compile(r'^your poster is upgraded|hidden product', re.I)
for r in rows:
    if r[10] == 'OPTIONS_HIDDEN_PRODUCT' or HELPER.search(r[1]):
        r[5] = 'Keep ACTIVE (option/upgrade helper product used at checkout); exclude it from the Google feed instead'
        r[8] = 'LOW'
    elif r[7] == 'no image on one or both' and r[5].startswith('Set to DRAFT +'):
        r[5] = 'Check the images, then set to DRAFT + URL redirect to original'
order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
rows.sort(key=lambda r: (order[r[8]], r[10], r[1]))
with open(os.path.join(outdir, '2026-10-06-duplicates.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['id', 'title', 'handle', 'status', 'likely_original_id', 'recommendation', 'reason', 'main_image_vs_original',
                'priority', 'in_58_conflicted_copies', 'product_type'])
    w.writerows(rows)

# identical-description template groups (different titles): summary only
dg = collections.defaultdict(list)
for p in A:
    d = nd(p['descriptionHtml'])
    if d: dg[d].append(p)
with open(os.path.join(outdir, '2026-10-06-shared-descriptions.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['listings_sharing_text', 'main_product_types', 'example_id', 'example_title', 'text_start'])
    for d, v in sorted(dg.items(), key=lambda kv: -len(kv[1])):
        if len(v) < 2: continue
        pts = '; '.join(f'{k or "(none)"} ({n})' for k, n in collections.Counter(p['productType'] for p in v).most_common(3))
        w.writerow([len(v), pts, v[0]['id'], v[0]['title'], d[:140]])

c = collections.Counter((r[8], r[5].split(':')[0]) for r in rows)
print('rows', len(rows)); [print(' ', k, n) for k, n in sorted(c.items())]
print('known58 in rows', sum(1 for r in rows if r[9]), 'of', len(KNOWN58))
print('empty-description ACTIVE', sum(1 for p in A if not nd(p['descriptionHtml'])))
print('shared-desc groups', sum(1 for v in dg.values() if len(v) > 1), 'listings', sum(len(v) for v in dg.values() if len(v) > 1))
print('dup rows by type', collections.Counter(r[10] for r in rows if r[8] != 'LOW').most_common(8))
