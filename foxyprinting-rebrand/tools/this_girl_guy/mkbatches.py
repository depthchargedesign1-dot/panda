import json,os
items=json.load(open('push_items.json'))
heavy=[i for i in items if 'descriptionHtml' in i.get('pu',{})]
light=[i for i in items if i not in heavy]
batches=[heavy[k:k+10] for k in range(0,len(heavy),10)]+[light[k:k+20] for k in range(0,len(light),20)]
os.makedirs('batches',exist_ok=True)
for n,b in enumerate(batches):
    q=[];V={};dec=[]
    for j,it in enumerate(b):
        if 'pu' in it:
            dec.append(f'$p{j}:ProductUpdateInput!'); V[f'p{j}']=it['pu']
            q.append(f'p{j}:productUpdate(product:$p{j}){{userErrors{{field message}}}}')
        if 'tags' in it:
            q.append(f't{j}:tagsAdd(id:"{it["id"]}",tags:["third-party-name"]){{userErrors{{field message}}}}')
    mfs=[m for it in b for m in it.get('mf',[])]
    for c in range(0,len(mfs),25):
        k=c//25; dec.append(f'$m{k}:[MetafieldsSetInput!]!'); V[f'm{k}']=mfs[c:c+25]
        q.append(f'm{k}:metafieldsSet(metafields:$m{k}){{userErrors{{field message}}}}')
    alts=[a for it in b for a in it.get('alts',[])]
    if alts:
        dec.append('$f:[FileUpdateInput!]!'); V['f']=alts
        q.append('f:fileUpdate(files:$f){userErrors{field message}}')
    doc='mutation('+','.join(dec)+'){'+' '.join(q)+'}'
    assert len(doc)<16384
    json.dump({'query':doc,'variables':V,'ids':[it['id'] for it in b]},open(f'batches/{n:03d}.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(batches), max(os.path.getsize('batches/'+f) for f in os.listdir('batches')))
