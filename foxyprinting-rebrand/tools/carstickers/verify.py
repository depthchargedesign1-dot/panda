import json,re,collections
live={}
for i in range(1,6):
    for n in json.load(open(f'verify/v{i}.json'))['data']['collection']['products']['nodes']: live[n['id']]=n
plan={x['id']:x for x in json.load(open('plan.json'))}
before={x['id']:x for x in json.load(open('before.json'))}
skipped=json.load(open('skipped.json'))
print('live products',len(live),'plan',len(plan),'before',len(before))
issues=collections.defaultdict(list)
allskus=[]
BANNED=re.compile(r'\b(official|licensed|authentic|genuine|approved|endorsed|merchandise)\b',re.I)
for pid,pl in plan.items():
    n=live.get(pid)
    if not n: issues[pid].append('missing in live'); continue
    b=before[pid]
    v=n['variants']['nodes']
    if len(v)!=2: issues[pid].append(f'variants={len(v)}')
    if n['options']!=[{'name':'Size','values':['Standard 15cm (6")','Large 30cm (12")']}]: issues[pid].append(f"options {n['options']}")
    vs={x['sku']:x for x in v}
    s=vs.get(pl['stdSku']); l=vs.get(pl['largeSku'])
    if not s or s['price']!='3.49': issues[pid].append(f'std {s}')
    if not l or l['price']!='6.99': issues[pid].append(f'large {l}')
    if l and (l['inventoryPolicy']!=pl['inventoryPolicy'] or l['taxable']!=pl['taxable'] or l['inventoryItem']['tracked']!=pl['tracked'] or l['inventoryItem']['requiresShipping']!=pl['requiresShipping']): issues[pid].append('large attrs differ')
    allskus+= [x['sku'] for x in v]
    d=n['descriptionHtml']
    norm=lambda h: re.sub(r'>\s+<','><',h).strip()
    if norm(d)!=norm(pl['descriptionHtml']): issues[pid].append('description differs from plan')
    if d.count('<h2')!=1: issues[pid].append('h2 count')
    if re.search('FAST DISPATCH|Many more in our Store|6" WIDE',d): issues[pid].append('old text')
    if 'Posted flat in a hard-backed envelope. Postage options and costs are shown at checkout.' not in d: issues[pid].append('delivery line')
    words=len(re.sub('<[^>]+>',' ',d).split())
    dis='class="disclaimer"' in d
    if dis: words_body=len(re.sub('<[^>]+>',' ',d.split('<h3>Please note')[0]).split())
    else: words_body=words
    if not 150<=words_body<=220: issues[pid].append(f'words {words_body}')
    if dis!=pl['branded']: issues[pid].append('disclaimer mismatch')
    if pl['branded'] and 'third-party-name' not in n['tags']: issues[pid].append('missing tag')
    if BANNED.search(d.split('<h3>Please note')[0]): issues[pid].append('banned word')
    st,sd=n['seo']['title'],n['seo']['description']
    if st!=pl['seoTitle'] or sd!=pl['seoDescription']: issues[pid].append('seo differs')
    if not st or len(st)>60: issues[pid].append(f'seo title len {len(st or "")}')
    if not sd or not 140<=len(sd)<=155: issues[pid].append(f'seo desc len {len(sd or "")}')
    if (n['mpn'] or {}).get('value')!=pl['stdSku']: issues[pid].append(f"mpn {n['mpn']}")
    if n['title']!=b['title'] or n['handle']!=b['handle'] or n['status']!=b['status']: issues[pid].append('title/handle/status changed')
    if set(b['tags'])-set(n['tags']): issues[pid].append('tags lost')
dups=[k for k,c in collections.Counter(allskus).items() if c>1]
print('duplicate SKUs within scope:',dups)
for s in skipped:
    sid=s['id'] if isinstance(s,dict) else s
    n=live[sid]; b=before[sid]
    same = n['descriptionHtml']==b['descriptionHtml'] and len(n['variants']['nodes'])==1 and n['variants']['nodes'][0]['price']==b['variants'][0]['price'] if 'variants' in b and isinstance(b['variants'],list) else None
    print('skipped',n['handle'],'variants',len(n['variants']['nodes']),n['variants']['nodes'][0]['price'],'desc unchanged',n['descriptionHtml']==b['descriptionHtml'],'opts',n['options'])
print('products with issues:',len(issues))
for k,v in list(issues.items())[:40]: print(plan[k]['handle'],v)
print('branded',sum(p['branded'] for p in plan.values()),'rude',sum(p['rude'] for p in plan.values()))
print('statuses',collections.Counter(n['status'] for n in live.values()))
