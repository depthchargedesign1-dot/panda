import json,re,collections
from gen import build, classify, G
sel=json.load(open('sel.json'))
plan,_=build(sel)
GPC='Home & Garden > Kitchen & Dining > Tableware > Drinkware > Mugs'
TEE='Apparel & Accessories > Clothing > Shirts & Tops'
items=[]; stats=collections.Counter()
for p in sel:
    r=plan.get(p['id']); tee='T-Shirt' in p['title']
    cls=r['cls'] if r else None
    it={'id':p['id'],'handle':p['handle']}
    pu={}
    if p['vendor']!='Foxy Printing': pu['vendor']='Foxy Printing'; stats['vendor']+=1
    tp = bool(r and r.get('third_party'))
    disc=None
    old=p['descriptionHtml'] or ''
    clean=re.sub(r'</p>"','</p>',old.replace('\u00b6\u00ff','').replace('\u00b6','').replace('\u00ff',''))
    if r and 'html' in r:
        pu['descriptionHtml']=r['html']; stats['desc_new']+=1
    elif tp and 'class="disclaimer"' not in (p['descriptionHtml'] or ''):
        # append disclaimer block only
        from gen import describe
        html,_=describe(cls,r['colour'],0,p['handle'])
        block=html[html.index('\n<h3>Please note</h3>'):]
        pu['descriptionHtml']=clean.rstrip()+block; stats['disc_appended']+=1
    elif clean!=old:
        pu['descriptionHtml']=clean; stats['junk_cleaned']+=1
    if pu: pu['id']=p['id']; it['pu']=pu
    if tp and 'third-party-name' not in p['tags']: it['tags']=['third-party-name']; stats['tag']+=1
    mf=[]; cur=lambda k:(p['mf'].get(k) or {}).get('value')
    def S(k,v,t='single_line_text_field'):
        mf.append({'ownerId':p['id'],'namespace':'mm-google-shopping','key':k,'type':t,'value':v}); stats['mf_'+k]+=1
    if cur('age_group')!='adult': S('age_group','adult')
    if cur('gender')!='unisex': S('gender','unisex')
    want = TEE if tee else GPC
    if cur('google_product_category')!=want: S('google_product_category',want)
    if cur('condition')!='new': S('condition','new')
    if cur('custom_product')!='true': S('custom_product','true','boolean')
    sku=p['vars'][0]['sku']
    if sku and cur('mpn')!=sku: S('mpn',sku)
    if not tee:
        c0=(r['colour'] if r else 'white'); c='White' if c0=='white' else 'White/'+c0.title()
        cc=cur('color')
        if (cc or '').lower()!=c.lower() and not (cc=='Multicolor' and c=='White'): S('color',c)
    if mf: it['mf']=mf; stats['products_mf']+=1
    # alt text
    alts=[]
    if not (cls and cls.get('pred')=='loves small girls'):
        if cls and cls.get('kw'): base=cls['kw']+' mug'
        elif cls and cls.get('cat')=='skip':
            base=re.sub(r'\s*(Printed Office Mug|Personalised ADULT OFFICE MUG|Mug)\s*$','',p['title'],flags=re.I)+' mug'
        else: base=p['title']
        for i,m in enumerate(p['media']):
            if not (m.get('alt') or '').strip():
                if tee: a=f"{base} – photo {i+1}"
                else: a = f"{base} – 11oz ceramic slogan mug" if i==0 else f"{base} – another view of the 11oz ceramic mug"
                alts.append({'id':m['id'],'alt':a}); stats['alt']+=1
    if alts: it['alts']=alts
    if len(it)>2: items.append(it)
print(stats, len(items))
json.dump(items,open('push_items.json','w'),ensure_ascii=False)
