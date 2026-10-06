import json,sys
d=json.load(open('expected2.json')); exp,src=d['exp'],d['src']
live={}
for l in open(sys.argv[1]):
    o=json.loads(l)
    if o['id'] in exp: live[o['id']]=o
json.dump(live,open('live_masks.json','w'),ensure_ascii=False)
F=[('title',lambda p:p.get('title')),('descriptionHtml',lambda p:p.get('descriptionHtml')),('seo.title',lambda p:(p.get('seo') or {}).get('title')),('seo.description',lambda p:(p.get('seo') or {}).get('description'))]
mm=[];cnt={};ok=0
for i,p in exp.items():
    l=live.get(i)
    if not l: mm.append((i,'MISSING')); continue
    bad=[f for f,g in F if g(p) is not None and g(p)!=g(l)]
    if not bad: ok+=1
    for f in bad: cnt[f]=cnt.get(f,0)+1; mm.append((i,f,src[i]))
print('checked',len(exp),'live',len(live),'exact',ok,cnt)
json.dump(mm,open('mismatch.json','w'),ensure_ascii=False)
