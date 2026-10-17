"""Turn payload.json + the rollback snapshot into per-product mutation variables (vars.json)."""
import json, pathlib
H = pathlib.Path(__file__).parent
d = json.load(open(H / 'payload.json'))
b = {p['id']: p for p in json.load(open(H / '../rollback/2026-10-06-bobble-hats/before.json'))['products']}
outs = []
for p in d['products']:
    o = b[p['id']]
    tags = sorted(set(o['tags']) | {"Bobble Hats", "Personalised Hats", "Workwear", "Club Hats", "io-bobble-hat", p['colour'],
                                    "range-football", "range-fb-scarves-hats", "range-workwear", "personalised", "machine-dtf"})
    mfs = [dict(ownerId=p['id'], namespace='mm-google-shopping', key=k, type=t, value=v) for k, t, v in [
        ('custom_product', 'boolean', 'true'), ('condition', 'single_line_text_field', 'new'),
        ('google_product_category', 'single_line_text_field', 'Apparel & Accessories > Clothing Accessories > Hats'),
        ('gender', 'single_line_text_field', 'unisex'), ('age_group', 'single_line_text_field', 'adult'),
        ('color', 'single_line_text_field', p['gcolor']), ('mpn', 'single_line_text_field', p['sku'])]]
    mfs += [dict(ownerId=p['id'], namespace='foxy', key='mockup', type='single_line_text_field', value='photo'),
            dict(ownerId=p['id'], namespace='foxy', key='personalise_fields', type='list.single_line_text_field',
                 value=json.dumps(d['fields'], ensure_ascii=False))]
    outs.append(dict(
        product=dict(id=p['id'], title=p['title'], descriptionHtml=p['descriptionHtml'], vendor='Foxy Printing',
                     productType='Bobble Hats', tags=tags, templateSuffix='personalised',
                     seo=dict(title=p['seo_title'], description=p['meta'])),
        pid=p['id'],
        variants=[dict(id=p['variant'], inventoryPolicy='CONTINUE', inventoryItem=dict(sku=p['sku'], tracked=False))],
        mf=mfs, files=[dict(id=m['id'], alt=p['alt']) for m in o['media']['nodes']]))
json.dump(outs, open(H / 'vars.json', 'w'), ensure_ascii=False, indent=1)
for v in outs:
    print(json.dumps(v, ensure_ascii=False))
