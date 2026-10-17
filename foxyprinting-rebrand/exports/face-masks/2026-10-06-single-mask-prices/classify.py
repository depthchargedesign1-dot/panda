import json,collections,re,sys
import os
D=os.environ.get('MASK_DATA', os.path.dirname(os.path.abspath(__file__)))+'/'
P={};V=collections.defaultdict(list)
for l in open(D+'m.jsonl'):
    o=json.loads(l)
    if '__parentId' in o: V[o['__parentId']].append(o)
    else: P[o['id']]=o

PACK=[
 (r'\bpacks?\b|\d\s*-\s*pack|\bmega\s*pack', 'pack'),
 (r'\bsets?\b', 'set'),
 (r'\bcouples?\b', 'couple'),
 (r'\bpairs?\b', 'pair'),
 (r'\bduo\b', 'duo'),
 (r'\btrio\b', 'trio'),
 (r'\bbundle\b', 'bundle'),
 (r'\bmulti-?pack\b', 'multipack'),
 (r'\brequest an?\b', 'request custom'),
 (r'\bvs\.?\b|\bversus\b', 'vs'),
 (r'\b\d+\s*x\b|\bx\s*\d+\b', 'N x multiple'),
 (r'\b((?!(19|20)\d\d\b)\d+|two|three|four|five|six|seven|eight|nine|ten|twelve)\s+(celebrity\s+|face\s+|party\s+|photo\s+|card\s+)*masks\b', 'N masks'),
 (r'\bmix\s*(&|and)\s*match', 'mix & match custom'),
 (r'\bmake your own', 'make-your-own custom'),
 (r'\brequest any', 'request-any custom'),
 (r'\bface covering', 'fabric face covering'),
 (r'\btrade price\b', 'trade price'),
 (r'\bbulk\b', 'bulk'),
 (r'\bpick any\b', 'pick-any bundle'),
 (r'\bpersonalised\b|\bpersonalized\b|\bcustom photo\b|\byour (own )?(photo|face)\b', 'personalised/custom photo'),
 (r'\bfull squad\b|\bteam\b.*\bmasks\b|\bfamily\b.*\bmasks\b', 'team/family set of masks'),
]
SHOWS=[r'sex and( the)? city',r'gavin and stacey',r'home and away',r'kevin and perry',r'dumb and dumber',r'beavis and butt-head',r'rick and morty',r'wallace and grommit']
AMP=re.compile(r'\s(&|and|\+)\s',re.I)

def classify(p,vs):
    t=p['title']; tl=t.lower()
    opts=[o['name'] for o in p['options']]
    price=vs[0]['price'] if len(vs)==1 else '/'.join(sorted({v['price'] for v in vs}))
    if opts==['Style'] :
        vals=set(p['options'][0]['values'])
        if {x.lower() for x in vals}=={'ready to wear','diy'} :
            pass  # candidate, still apply title checks
        else:
            return 'borderline','Style option with values %s'%sorted(vals)
    elif opts!=['Title']:
        if opts==['DIY OR READY CUT']: return 'exclude','personalised photo multipack (DIY OR READY CUT option)'
        if opts==['Style','Quantity']: return 'exclude','Style + Quantity product'
        return 'borderline','unexpected options %s'%opts
    if 'king charles iii + crown' in tl and '5 x' not in tl: return 'exclude','KING CHARLES III + Crown (owner listed, £14.99)'
    if re.search(r'roger lloyd-pack',tl): tl=tl.replace('lloyd-pack','lloyd')
    tl=tl.replace('x factor','xfactor').replace('bates vs the post office','bates v post office')
    if 'strawhat crew pack' in tl or 'comedian 2 face masks' in tl:
        return 'borderline','title suggests several masks but price is single-mask £%s'%vs[0]['price']
    for rx,why in PACK:
        if re.search(rx,tl): return 'exclude','title: %s'%why
    if re.search(r'multipack|-pack-|-\d+-pack',p['handle'].replace('lloyd-pack','lloyd')): return 'exclude','handle says multipack/pack (title does not)'
    # "&"/"and"/"+" joining two names
    head=re.split(r'\s[–-]\s|\bface\s*mask|\bfacemask|\bmask\b|\bcelebrity\b|\bstrictly\b',t,1,flags=re.I)[0]
    head2=re.sub(r'\((black|blue|red) & white\)','',head,flags=re.I)
    for show in SHOWS: head2=re.sub(show,'',head2,flags=re.I)
    m=AMP.search(' '+head2+' ')
    if m:
        if re.search(r'strictly',tl): return 'exclude','title: two people joined with "&" (dance couple)'
        return 'borderline','name part joins two names with "%s": %s'%(m.group(1),head.strip())
    if 'mask' not in tl and 'face' not in tl:
        return 'borderline','title does not say mask'
    if re.search(r'\bmasks\b',tl) and not re.search(r'face masks? (fancy|–|-)',tl):
        return 'borderline','title says "masks" (plural)'
    pr=max(float(v['price']) for v in vs)
    if pr>=7.5: return 'exclude' if False else 'borderline','price £%.2f (>= £7.50), not clearly one mask'%pr
    if pr>=5.0: return 'borderline','price £%.2f is high for a single mask'%pr
    return 'include','single mask'

rows=[]
for pid,p in P.items():
    vs=V[pid]
    d,r=classify(p,vs)
    rows.append((pid,p,vs,d,r))
if __name__=='__main__':
    c=collections.Counter((d) for *_,d,r in rows); print(c)
    c2=collections.Counter((d,r) for *_,d,r in rows)
    for k,n in sorted(c2.items()): print(n,k)
