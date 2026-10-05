from load import *
import csv,json
from collections import Counter,defaultdict
P,V=load('export_before.jsonl')
OLD={'A4':'14.99','A3':'19.99'}; NEW={'A4':'19.99','A3':'24.99'}
GAME=re.compile(r'retro gaming|game inspired|gaming poster|nes poster|snes|sega|playstation|atari|game ?cube|neo geo|oddesy|odyssey|amiga|jaguar|coleco|mega cd|dreamcast|saturn|ps1|ps4|n64|nintendo',re.I)
def family(p):
    s=p['title']+' '+p['handle']+' '+p['productType']
    if re.search(r'stadium',s,re.I): return 'stadium posters'
    if re.search(r'signed|autograph|printed signature|signature',s,re.I): return 'signed / printed-signature prints'
    if GAME.search(s): return 'retro gaming posters'
    return 'other prints'
def is_pet(p): return bool(re.search(r'pet[- ]portrait',p['title']+' '+p['handle']+' '+p['productType'],re.I))
NONPOSTER=re.compile(r'photo frame|picture frame|frame only|mirror|clock|cufflink|mug|card\b',re.I)
changes=defaultdict(list); other=[]; pets=[]; doubtful=[]
for v in V:
    s=framed_size(v)
    if not s: continue
    p=P[v['__parentId']]
    row=[p['id'],p['handle'],p['title'],p['status'],p['productType'],v['id'],v['title'],v.get('sku') or '',v['price']]
    if is_pet(p): pets.append(row); continue
    if NONPOSTER.search(p['title']) and not re.search(r'poster|print',p['title'],re.I): doubtful.append(row); continue
    if s=='?': doubtful.append(row); continue
    if v['price']==OLD[s]: changes[p['id']].append((v,s,row))
    else: other.append(row+['already at target' if v['price']==NEW[s] else 'different price'])
H=['product_id','handle','product_title','status','product_type','variant_id','variant_title','sku','price']
if __name__=='__main__':
    with open('before.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(H[:2]+['family']+H[2:]+['new_price','size'])
        for pid,l in changes.items():
            for v,s,row in l: w.writerow(row[:2]+[family(P[pid])]+row[2:]+[NEW[s],s])
    with open('other_prices.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(H+['note']); w.writerows(other)
    with open('pet_portraits_excluded.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(H); w.writerows(pets)
    with open('doubtful_excluded.csv','w',newline='') as f:
        w=csv.writer(f); w.writerow(H); w.writerows(doubtful)
    with open('plan.jsonl','w') as f:
        for pid,l in changes.items():
            f.write(json.dumps({'productId':pid,'variants':[{'id':v['id'],'price':NEW[s]} for v,s,_ in l]})+'\n')
    fam=Counter(); famv=Counter()
    for pid,l in changes.items(): fam[family(P[pid])]+=1; famv[family(P[pid])]+=len(l)
    print('products',len(changes),'variants',sum(len(l) for l in changes.values()))
    for k in fam: print(k,fam[k],famv[k])
    print('other',len(other),Counter(r[-1] for r in other),'pets',len(pets),'doubtful',len(doubtful))
    print(Counter(P[pid]['productType'] for pid in changes).most_common())
    print(Counter(P[pid]['status'] for pid in changes))
    # mixed products
    mixed=[pid for pid,l in changes.items() if any(r[0]==pid for r in other)]
    print('products with both changed and other-price framed variants',len(mixed))
