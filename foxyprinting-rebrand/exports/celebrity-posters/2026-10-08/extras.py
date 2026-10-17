import json,re
rows=[json.loads(l) for l in open('dl/other.jsonl')]
rows=[r for r in rows if 'printed signature' not in r['title'].lower()]
inc=[]
for r in rows:
    t=r['title']; ty=r['productType']; tl=t.lower()
    g=None
    if ty=='Music Poster': g='music'
    elif ty=='Sports Poster': g='darts' if 'darts' in tl else 'football'
    elif 'darts poster print' in tl: g='darts'
    elif re.search(r'ilia topuria',tl): g='mma-wrestling'
    elif ty=='Signed Athletics Prints' and re.search(r'lioness|women|england & |& england|keira walsh|lucy bronze|michelle agyemang|khiara keating|diogo jota|wolves poster print – wolverhampton wanderers signature',tl) and not re.search(r'team|champions|portrait',tl): g='football'
    elif ty=='Signed Team Player Prints' and re.search(r'champions of england liverpool|leeds united champions 2020 football gift',tl): g='football'
    elif ty=='Posters, Prints, & Visual Artwork' and re.search(r'^(jude bellingham|anthony gordon|dan burn|declan rice|harry kane|jordan pickford|djed spence|elliot anderson|nico o.reilly|lionel messi|enzo fern|lautaro|lamine yamal|kevin keegan|rodri|gylfi)',tl) and 'poster pack' not in tl: g='football'
    elif ty=='Signed Footballer Posters': g='football'
    if g: inc.append({'id':r['id'],'title':t,'group':g,'status':r['status']})
json.dump(inc,open('work/extras.json','w'),indent=0)
print(len(inc))
for i in inc: print(i['group'],'|',i['title'][:90])
