import json,re,csv,collections,sys
sel=json.load(open(sys.argv[1])); out=sys.argv[2]
base='/home/user/panda/foxyprinting-rebrand/exports/seo/2026-10-06-remaining/'
hs=set()
for f in ['01-seo.csv','02-seo-CLEAN.csv']:
    for r in csv.DictReader(open(base+f)): hs.add(r['Handle'])
norm=lambda h: re.sub(r'\s+',' ',h or '').strip()
empty=lambda h: not re.sub(r'<[^>]+>|\s|&nbsp;','',h or '')
dc=collections.Counter(norm(p['descriptionHtml']) for p in sel if not empty(p['descriptionHtml']))
def imgkey(p):
    if not p['media']: return None
    f=p['media'][0]['image']['url'].split('/')[-1].split('?')[0]
    f=re.sub(r'_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}','',f)
    return f.lower()
dupk=collections.Counter(imgkey(p) for p in sel)
F=['age_group','gender','google_product_category','color','condition','custom_product','mpn']
with open(out,'w',newline='') as fh:
    w=csv.writer(fh)
    w.writerow(['product_id','handle','title','url','product_type','status','empty_description','duplicate_description','seo_title','seo_meta','in_seo_import_csv','vendor']+F+['mpn_matches_sku','image_count','empty_alt_count','price','sku','true_duplicate_of_same_design'])
    for p in sel:
        v=p['vars'][0]; mf=lambda k:(p['mf'].get(k) or {}).get('value','')
        d=p['descriptionHtml']
        w.writerow([p['id'].split('/')[-1],p['handle'],p['title'],'https://foxyprinting.co.uk/products/'+p['handle'],p['productType'],p['status'],
          'yes' if empty(d) else 'no','yes' if (not empty(d) and dc[norm(d)]>1) else 'no',
          'set' if p['seo']['title'] else 'missing','set' if p['seo']['description'] else 'missing','yes' if p['handle'] in hs else 'no',p['vendor']]+[mf(k) for k in F]+
          ['yes' if mf('mpn')==v['sku'] else 'no',len(p['media']),sum(1 for m in p['media'] if not (m.get('alt') or '').strip()),v['price'],v['sku'],
           'yes' if (imgkey(p) is not None and dupk[imgkey(p)]>1) else 'no'])
