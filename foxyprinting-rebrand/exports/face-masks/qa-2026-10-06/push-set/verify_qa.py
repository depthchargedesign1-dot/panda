"""Compare a bulk export (JSONL with id, descriptionHtml, seo{title,description}) against qa/expected.json.
Usage: python3 verify_qa.py export.jsonl  -> counts of products whose live value equals 'new' (fixed), 'old' (not yet pushed) or neither (drift)."""
import json, sys, collections
exp = json.load(open(__file__.rsplit('/', 1)[0] + '/expected.json'))
c = collections.Counter(); drift = []
for l in open(sys.argv[1]):
    o = json.loads(l)
    if o['id'] not in exp: continue
    v = exp[o['id']]; live = dict(d=o.get('descriptionHtml') or '', m=(o.get('seo') or {}).get('description') or '', t=(o.get('seo') or {}).get('title') or '')
    if all(live[f] == v['new'][f] for f in 'dmt'): c['fixed'] += 1
    elif all(live[f] == v['old'][f] for f in 'dmt'): c['not pushed'] += 1
    else: c['drift'] += 1; drift.append(o['id'])
print(dict(c), 'of', len(exp)); json.dump(drift, open('drift.json', 'w'))
