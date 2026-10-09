"""Independent checks on import/*.csv against the bulk export (MASK_DATA/m.jsonl)."""
import csv, glob, json, os, re, random, collections
D = os.environ['MASK_DATA'] + '/'
P = {}; V = collections.defaultdict(list)
for l in open(D + 'm.jsonl'):
    o = json.loads(l)
    (V[o['__parentId']].append(o) if '__parentId' in o else P.__setitem__(o['handle'], o))
byid = {p['id']: p for p in P.values()}
PRICE = {('Ready Cut', 'Elastic'): '2.99', ('Ready Cut', 'Stick'): '3.49', ('DIY', 'Elastic'): '1.50', ('DIY', 'Stick'): '2.00'}
SUF = {('Ready Cut', 'Elastic'): '-RC-E', ('Ready Cut', 'Stick'): '-RC-S', ('DIY', 'Elastic'): '-DIY-E', ('DIY', 'Stick'): '-DIY-S'}
PACKRX = re.compile(r'\b(pack|set|couple|pair|duo|trio|bundle|multipack|trade price|bulk|face covering|mix & match|make your own|request any)\b|\b\d+\s*x\b', re.I)
rows = collections.defaultdict(list); files = {}
errs = []
for f in sorted(glob.glob('import/*.csv')):
    sz = os.path.getsize(f)
    if sz > 15e6: errs.append('too big ' + f)
    for r in csv.DictReader(open(f, encoding='utf-8')):
        rows[r['Handle']].append(r); files.setdefault(r['Handle'], set()).add(f)
skus = collections.Counter()
for h, rs in rows.items():
    p = P.get(h)
    if not p: errs.append('unknown handle ' + h); continue
    if len(files[h]) != 1: errs.append('handle in 2 files ' + h)
    if len(rs) != 4: errs.append('rows!=4 ' + h)
    if rs[0]['Title'] != p['title']: errs.append('title ' + h)
    if rs[0]['Status'] != p['status'].lower(): errs.append('status ' + h)
    if any(r['Title'] or r['Status'] or r['Option1 Name'] or r['Option2 Name'] for r in rs[1:]): errs.append('extra fields ' + h)
    if (rs[0]['Option1 Name'], rs[0]['Option2 Name']) != ('Style', 'Fitting'): errs.append('opt names ' + h)
    combos = {(r['Option1 Value'], r['Option2 Value']) for r in rs}
    if combos != set(PRICE): errs.append('combos ' + h)
    vs = V[p['id']]
    base = vs[0]['sku'] if len(vs) == 1 else [v for v in vs if v['title'] == 'Ready to Wear'][0]['sku']
    for r in rs:
        k = (r['Option1 Value'], r['Option2 Value'])
        if r['Variant Price'] != PRICE[k]: errs.append('price ' + h)
        if r['Variant SKU'] != (base or 'FOXY-MASK-' + p['id'].rsplit('/', 1)[1]) + SUF[k]: errs.append('sku ' + h)
        if (r['Variant Inventory Policy'], r['Variant Inventory Tracker'], r['Variant Fulfillment Service'], r['Variant Requires Shipping'], r['Variant Taxable']) != ('continue', '', 'manual', 'TRUE', 'TRUE'): errs.append('variant fields ' + h)
        skus[r['Variant SKU'].upper()] += 1
    if PACKRX.search(p['title']) and 'lloyd-pack' not in p['title'].lower() and '1 x factor' not in p['title'].lower(): errs.append('PACK? ' + p['title'])
    if [o['name'] for o in p['options']] not in (['Title'], ['Style']): errs.append('options ' + h)
errs += ['dup sku ' + s for s, n in skus.items() if n > 1]
print('products', len(rows), 'rows', sum(map(len, rows.values())), 'unique skus', len(skus))
print('status', collections.Counter(rs[0]['Status'] for rs in rows.values()))
print('old prices', collections.Counter('/'.join(v['price'] for v in V[P[h]['id']]) for h in rows).most_common())
print('ERRORS', len(errs)); [print(' ', e) for e in errs[:30]]
random.seed(6)
print('SPOT', json.dumps(random.sample(sorted(rows), 10)))
