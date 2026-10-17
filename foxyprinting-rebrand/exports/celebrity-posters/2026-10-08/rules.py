import json,collections,re,sys
d=json.load(open('work/classified.json'))
GROUPMERGE={'snooker':'darts'}
items=[(k,GROUPMERGE.get(v[0],v[0]),v[1],v[2],v[4]) for k,v in d.items()]
groups=sorted(set(i[1] for i in items))
def ngrams(title):
    w=re.sub(r'\s+',' ',title.lower()).split(' ')
    out=set()
    for n in (2,3,4):
        for i in range(len(w)-n+1):
            g=' '.join(w[i:i+n])
            if 'printed signature' in g and KWRE.search(g) and not re.search(r'\d|–',g): out.add(g)
    return out
BAN={'posters, prints, & visual artwork','signed team player prints','signed comedian prints','signed athletics prints','football posters','signed posters'}
KWRE=re.compile(r'football|nfl|music|singer|rapper|band|movie|film|actor|bollywood|tv|television|show|comedian|walking dead|thrones|netflix|box|ufc|mma|wrestl|wwe|fighter|fiighter|darts|snooker|cricket|rugby|golf|tennis|horse|racer|racing|jockey|formula|f1|driver|motor|basketball|baseball|hockey|athlet|olympian|swimmer|author|scientist|business|fashion|dancer|team player')
feat=collections.defaultdict(set)   # feature -> set of ids
for k,g,t,ty,tags in items:
    if ty.strip() and ty.strip().lower() not in BAN: feat[('TYPE',ty.strip())].add(k)
    for ng in ngrams(t): feat[('TITLE',ng)].add(k)
grp={k:g for k,g,*_ in items}
plan={}
for G in groups:
    members={k for k,g in grp.items() if g==G}
    cands=[]
    for f,ids in feat.items():
        good=sum(1 for i in ids if grp[i]==G)
        if good==len(ids) and good>=2: cands.append((f,ids))
    covered=set(); chosen=[]
    while len(chosen)<55:
        best=max(cands,key=lambda c:len(c[1]-covered),default=None)
        if not best or len(best[1]-covered)<2: break
        chosen.append(best[0]); covered|=best[1]
    plan[G]={'rules':chosen,'covered':len(covered),'members':len(members),'residual':sorted(members-covered)}
    print(G,len(members),'covered',len(covered),'residual',len(members-covered),'rules',len(chosen))
json.dump(plan,open('work/plan.json','w'),indent=0)
