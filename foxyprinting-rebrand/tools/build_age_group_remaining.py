#!/usr/bin/env python3
"""Build the Shopify CSV import for the age_group/gender fixes not yet pushed by API (phase 2, batches 7+).
usage: build_age_group_remaining.py [export_after.jsonl]  (bulk export giving id -> handle)"""
import json, csv, sys, os, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = f'{ROOT}/exports/rollback/2026-10-05-google-fixes/'
OUT = f'{ROOT}/exports/google-fields/2026-10-06-age-group-remaining/'
EXPORT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/-home-user-panda/b27c821e-842d-5652-8996-b16be4651f6f/scratchpad/export_after.jsonl'
B = 175  # batch size used by nb.py
HDR = ['Handle',
       'Google Shopping / Age Group (product.metafields.mm-google-shopping.age_group)',
       'Google Shopping / Gender (product.metafields.mm-google-shopping.gender)']
items = json.load(open(R + 'phase2_items.json'))
before = json.load(open(R + 'phase2_before.json'))
done = {int(x) for x in open(R + 'phase2_done.log').read().split()}
assert done == set(range(max(done) + 1)), 'done batches must be contiguous from 0'
skip = (max(done) + 1) * B
pending = items[skip:]
print('items', len(items), 'done', skip, 'pending', len(pending))

plan = {}  # pid -> planned values (from phase2_before 'set')
for x in before:
    plan[x['id'].rsplit('/', 1)[1]] = x['set']
# every product's planned age_group is always known, so gender-only changes keep it
pend = collections.OrderedDict()
for pid, k, v in pending:
    assert plan[pid][k] == v
    pend.setdefault(pid, {})[k] = v

handles = {}
need = set(pend)
with open(EXPORT) as f:
    for line in f:
        if '"handle"' not in line: continue
        o = json.loads(line)
        if 'handle' in o and '__parentId' not in o:
            p = o['id'].rsplit('/', 1)[1]
            if p in need: handles[p] = o['handle']
missing = need - set(handles)
assert not missing, f'no handle for {len(missing)} products'

rows = []; kinds = collections.Counter()
for pid, ch in pend.items():
    ag = plan[pid]['age_group']            # planned age group (never blank)
    ge = 'unisex'                          # owner's rule; matches planned value / current value for age-only rows
    if 'gender' in plan[pid]: assert plan[pid]['gender'] == 'unisex'
    kinds[('age_group+gender' if len(ch) == 2 else ('age_group only' if 'age_group' in ch else 'gender only')), ag] += 1
    rows.append([handles[pid], ag, ge])
assert len({r[0] for r in rows}) == len(rows), 'duplicate handles'


def write(name, rs):
    with open(OUT + name, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(HDR); w.writerows(rs)
    print(name, len(rs), os.path.getsize(OUT + name))
# test file: one of each kind where possible (kids, adult, and a Gender-changing one)
def first(pred):
    return next(r for r in rows if pred(r))
test = [first(lambda r: r[1] == 'adult' and 'gender' in pend[next(p for p, h in handles.items() if h == r[0])]),
        first(lambda r: r[1] == 'kids'), first(lambda r: r[1] == 'adult')]
test = list(dict.fromkeys(map(tuple, test)))
for r in rows:
    if len(test) >= 3: break
    if tuple(r) not in test: test.append(tuple(r))
write('00-TEST-3-products.csv', [list(t) for t in test])
rest = [r for r in rows if tuple(r) not in set(test)]
CH = 25000
for i in range(0, len(rest), CH):
    write(f'{i // CH + 1:02d}-age-group-gender.csv', rest[i:i + CH])
print(dict(kinds))
