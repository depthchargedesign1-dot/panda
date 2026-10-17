import sys,json,os,csv; sys.path.insert(0,'../verify'); from gqlparse import parse_file
B='../push'; R='/home/user/panda/foxyprinting-rebrand/exports/rollback'
def done(s): return [json.loads(l)['batch'] for l in open(f'{B}/{s}/done.jsonl') if l.strip() and json.loads(l)['status']=='ok']
exp={}; src={}
def apply(p,tag,fields=None):
    i=p['id']
    if i not in exp: return False
    for k,v in p.items():
        if k=='id' or (fields and k not in fields): continue
        if k=='seo':
            s=dict(exp[i].get('seo') or {}); s.update({kk:vv for kk,vv in v.items() if (not fields or 'seo.'+kk in fields or 'seo' in fields)}); exp[i]['seo']=s
        else: exp[i][k]=v
    src[i].append(tag); return True
for b in done('masks'):
    for a,p in parse_file(f'{B}/masks/batches/b{b}.gql'):
        exp[p['id']]=dict(p); src[p['id']]=['masks/'+b]
print('mask products',len(exp))
for f in ('masks/seo_fix.gql','masks/seo_fix_245.gql'):
    for a,p in parse_file(f'{B}/{f}'): apply(p,f)
for v in json.load(open('../sens/mut.json'))['variables'].values():
    apply({k:v[k] for k in ('id','descriptionHtml','seo','title') if k in v},'sens/mut')
for b in done('fixes'):
    if b=='0003': continue
    for a,p in parse_file(f'{B}/fixes/batches/b{b}.gql'): apply(p,'fixes/'+b)
# titles plan
for r in csv.DictReader(open(f'{B}/titles/plan.csv')):
    if r['id'] in exp: exp[r['id']]['title']=r['new title']; src[r['id']].append('titles')
n=0
for b in done('seotitles'):
    for a,p in parse_file(f'{B}/seotitles/batches/b{b}.gql'):
        n+=apply({'id':p['id'],'seo':{'title':p['seo']['title']}},'seotitles/'+b)
print('seotitles applied',n)
for f in ('2026-10-05-sensitive-masks/after.json','2026-10-05-sensitive-masks/after_hall_glitter.json'):
    for p in json.load(open(f'{R}/{f}')): print('sens',p['id'],apply(p,f.split('/')[1]))
cf=json.load(open(f'{R}/2026-10-05-conflicted-titles/after-final.json'))
k=[x for x in cf if isinstance(cf[x],list)]
for key in k:
    for p in cf[key]:
        if p.get('id') in exp: print('conflicted overlaps',p['id']); apply({x:p[x] for x in ('id','title','descriptionHtml') if x in p},'conflicted')
from gql2 import parse_any
for a,fn,ar in parse_any(f"{B}/fixes/batches/b0003.gql"):
  if fn=="productUpdate": p=ar["product"]; print('bond',p['id'],apply(p,'fixes/0003'))
json.dump({'exp':exp,'src':src},open('expected2.json','w'),ensure_ascii=False)
print('total',len(exp))
