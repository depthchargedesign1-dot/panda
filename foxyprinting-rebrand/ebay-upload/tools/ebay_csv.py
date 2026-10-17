#!/usr/bin/env python3
"""Build eBay UK upload CSVs (Seller Hub > Reports > Uploads) from a Shopify bulk export of products.

Input: a bulkOperationRunQuery JSONL with, per product:
  id handle title productType tags descriptionHtml options{name values}
  media{ MediaImage{ image{url altText} } }  variants{ sku title price selectedOptions{name value} image{url} }
(see ../PLAN.md for the exact query; source/masks-first-81.jsonl is the first one).

Usage:
  python3 -I tools/ebay_csv.py <export.jsonl> <list.csv> <out.csv> [--config config/masks.json] [--limit N] [--tier A]
  <list.csv> picks which products go in the file, and in which order (a lists/ file, filtered by --tier / --batch).

Every listing:
  - Action Add, Fixed price (FixedPrice, GTC), condition New (1000), quantity 3 per variation (owner, 9 Oct 2026).
  - CustomLabel = the Shopify SKU (so orders match Shopify), variation rows for Shopify options.
  - Title cut to eBay's 80 characters at a word boundary, after the config's title rules.
  - Up to 12 pictures from Shopify (main picture first).
  - Description = templates/listing.html filled with the Shopify description, cleaned of Shopify-only text
    (live preview, basket/checkout, phone numbers, links) - eBay doesn't allow links or contact details off eBay.
  - Postage, returns and payment come from the owner's eBay business policies, named in the config.
  - Personalised items get the eBay "Personalise" item specific + instructions (the buyer types into a box
    next to Buy It Now and it reaches us as a message to seller).
"""
import argparse, csv, html, json, re, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ACTION = '*Action(SiteID=UK|Country=GB|Currency=GBP|Version=1193)'


def load_export(path):
    prods, kids = {}, defaultdict(list)
    for line in open(path, encoding='utf-8'):
        o = json.loads(line)
        if 'handle' in o:
            prods[o['id']] = o
        else:
            kids[o['__parentId']].append(o)
    for pid, o in prods.items():
        o['variants'] = [k for k in kids[pid] if 'sku' in k]
        o['images'] = [k['image']['url'] for k in kids[pid] if 'sku' not in k and k.get('image')]
    return prods


def clean_url(u):
    return u.split('?')[0] if u else u


# ---------- titles ----------
def cut80(t):
    t = re.sub(r'\s+', ' ', t).strip()
    if len(t) <= 80:
        return t
    out = ''
    for w in t.split(' '):
        if len((out + ' ' + w).strip()) > 80:
            break
        out = (out + ' ' + w).strip()
    return out.rstrip(' –-,&|')


def mask_title(title):
    """'Gerwyn Price Face Mask – Fancy Dress Cardboard Costume Mask' -> 'Gerwyn Price Celebrity Face Mask ...'"""
    if re.search(r'masks|pack|set of|personalised', title, re.I):
        return cut80(re.sub(r'\s+-\s*(?=[A-Z])', ' – ', title))
    m = re.match(r"\s*(.+?)\s+(?:celebrity\s+)?(?:cardboard\s+)?(?:party\s+)?(?:face\s*)?mask\b", title, re.I)
    name = m.group(1) if m else title
    name = re.sub(r'\s+(celebrity|cardboard)$', '', name, flags=re.I)
    name = re.sub(r'\b(LF\d*|JB|\d+)\b|\bActor Movie Tv\b', '', name)          # shop codes / numbering
    name = re.sub(r'\s*-\s*', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    if name.isupper():
        name = name.title()
    return cut80(f"{name} Face Mask Celebrity Card Fancy Dress Mask Stag Hen Party Photo Prop")


# ---------- description ----------
DROP_SENTENCE = re.compile(r"[^.!?<>]*(live preview|basket|checkout|at checkout|01439|call us|phone|website|"
                           r"foxyprinting\.co\.uk|click|add to cart|order online|our site|contact|e-?mail|whatsapp|"
                           r"www\.|https?://|\S+@\S+\.\w|07\d{3}\s?\d{6}|(?-i:\bREMEMBER\b))[^.!?<>]*[.!?]?", re.I)


def clean_body(h):
    h = re.sub(r'<a\b[^>]*>(.*?)</a>', r'\1', h, flags=re.S | re.I)          # no links off eBay
    h = re.sub(r'<img\b[^>]*>', '', h, flags=re.I)                           # pictures go in the gallery, not the text
    h = re.sub(r'<(script|style|iframe|form)\b.*?</\1>', '', h, flags=re.S | re.I)
    h = re.sub(r'\s(style|class|id)="[^"]*"', lambda m: m.group(0) if 'disclaimer' in m.group(0) else '', h)
    # drop the Shopify "Delivery" section: eBay shows its own postage box
    h = re.sub(r'<h3>\s*Delivery\s*</h3>\s*<p>.*?</p>', '', h, flags=re.S | re.I)
    h = DROP_SENTENCE.sub('', h)
    for _ in range(3):
        h = re.sub(r'<(span|strong|em|b)>\s*</\1>', '', h)
    h = re.sub(r'<p>(\s|&nbsp;|-)*</p>', '', h)
    h = re.sub(r'<h2>', '<h2 style="font-family:\'Baloo 2\',\'Trebuchet MS\',Arial,sans-serif;font-size:21px;color:#FF6A13;margin:18px 0 8px;">', h)
    h = re.sub(r'<h3>', '<h3 style="font-family:\'Baloo 2\',\'Trebuchet MS\',Arial,sans-serif;font-size:18px;color:#7A2BF5;margin:16px 0 6px;">', h)
    h = h.replace('<p class="disclaimer">', '<p style="font-size:12px;color:#6b6585;">')
    return h.strip()


def badge(text, colour):
    return (f'<span style="display:inline-block;background:{colour};color:#FFFFFF;border-radius:999px;'
            f'padding:4px 12px;margin:0 6px 6px 0;font-size:13px;font-weight:700;">{html.escape(text)}</span>')


def personalise_box(text):
    return ('<div style="background:#FFF8DC;border:2px dashed #FFC83D;border-radius:12px;padding:12px 16px;'
            'margin:0 0 16px;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.5;">'
            '<strong style="color:#1D1240;font-size:17px;">&#9998; How to personalise</strong><br>'
            f'{text}</div>')


def build_description(tpl, title, body_html, cfg, personalised):
    for a, b in cfg.get('replace', []):
        body_html = re.sub(a, b, body_html)
    badges = ''.join(badge(t, c) for t, c in zip(cfg.get('badges', []),
                                                ['#FF6A13', '#FF2D87', '#7A2BF5', '#00B8A9', '#1D1240']))
    box = personalise_box(cfg['personalise_box']) if personalised and cfg.get('personalise_box') else ''
    if cfg.get('fallback_disclaimer') and 'endorsed' not in body_html:   # Shopify copy without one: eBay still needs it
        body_html += ('<h3>Please note</h3><p class="disclaimer">' + cfg['fallback_disclaimer'] + '</p>')
    d = (tpl.replace('{{TITLE}}', html.escape(title)).replace('{{INTRO_BADGES}}', badges)
         .replace('{{PERSONALISE_BOX}}', box).replace('{{BODY}}', clean_body(body_html))
         .replace('{{POSTAGE}}', cfg['postage_text']).replace('{{RETURNS}}', cfg['returns_text']))
    d = re.sub(r'<!--.*?-->', '', d, flags=re.S)
    return re.sub(r'\n\s*', '', d)


# ---------- SKUs ----------
SKU_MAP = {}


def ebay_sku(sku):
    """eBay's Custom label is 50 characters at most: shorten the middle of long Shopify SKUs, keep the ending."""
    if len(sku) <= 50:
        return sku
    m = re.match(r'(.*?)(-(?:RC|DIY)-(?:E|S)|-\d+)?$', sku)
    base, suf = m.group(1), m.group(2) or ''
    short = base[:50 - len(suf)].rstrip('-') + suf
    n = 2
    while short in SKU_MAP and SKU_MAP[short] != sku:
        tag = f'-{n}'
        short = base[:50 - len(suf) - len(tag)].rstrip('-') + tag + suf
        n += 1
    SKU_MAP[short] = sku
    return short


# ---------- rows ----------
def build(prods, order_ids, cfg, tpl):
    specifics = cfg['item_specifics']
    spec_cols = [f'C:{k}' for k in specifics] + ['C:Personalise', 'C:Personalisation Instructions']
    cols = [ACTION, 'CustomLabel', '*Category', 'StoreCategory', '*Title', '*ConditionID'] + spec_cols + [
        'Relationship', 'RelationshipDetails', 'PicURL', '*Description', '*Format', '*Duration', '*StartPrice',
        '*Quantity', '*Location', 'PostalCode', 'ShippingProfileName', 'ReturnProfileName', 'PaymentProfileName']
    rows, report = [], []
    for pid in order_ids:
        o = prods.get(pid)
        if not o:
            report.append(f'MISSING from export: {pid}')
            continue
        personalised = bool(re.search(cfg.get('personalised_regex', r'^$'), o['title'], re.I))
        title = cfg.get('titles', {}).get(o['handle']) or (
            mask_title(o['title']) if cfg.get('title_rule') == 'mask' else cut80(o['title']))
        title = cut80(title)
        rename = cfg.get('option_rename', {})
        opts = [x for x in o['options'] if x['name'] != 'Title']
        pics = [clean_url(u) for u in o['images']][:12]
        base = {c: '' for c in cols}
        base.update({ACTION: 'Add', '*Category': cfg['category_id'], 'StoreCategory': cfg.get('store_category', ''),
                     '*Title': title, '*ConditionID': '1000', 'PicURL': '|'.join(pics),
                     '*Description': build_description(tpl, title, o['descriptionHtml'], cfg, personalised),
                     '*Format': 'FixedPrice', '*Duration': 'GTC', '*Location': cfg['location'],
                     'PostalCode': cfg['postcode'], 'ShippingProfileName': cfg['shipping_profile'],
                     'ReturnProfileName': cfg['return_profile'], 'PaymentProfileName': cfg['payment_profile']})
        for k, v in specifics.items():
            base[f'C:{k}'] = v
        if personalised:
            base['C:Personalise'] = 'Yes'
            base['C:Personalisation Instructions'] = cfg['personalise_instructions'][:200]
        price = lambda p: f"{float(p) * cfg.get('price_multiplier', 1.0):.2f}"
        if not opts or len(o['variants']) == 1:
            v = o['variants'][0]
            base.update({'CustomLabel': ebay_sku(v['sku']), '*StartPrice': price(v['price']), '*Quantity': str(cfg['quantity'])})
            rows.append(base)
        else:
            names = [rename.get(x['name'], x['name']) for x in opts]
            parent = re.sub(r'-(RC|DIY)-(E|S)$', '', o['variants'][0]['sku'])
            if parent == o['variants'][0]['sku']:
                parent = 'EBAY-' + o['handle'].upper()
            base['CustomLabel'] = ebay_sku(parent)
            base['Relationship'] = ''
            base['RelationshipDetails'] = '|'.join(f"{n}={';'.join(x['values'])}" for n, x in zip(names, opts))
            rows.append(base)
            for v in o['variants']:
                r = {c: '' for c in cols}
                sel = {s['name']: s['value'] for s in v['selectedOptions']}
                r.update({'CustomLabel': ebay_sku(v['sku']), 'Relationship': 'Variation',
                          'RelationshipDetails': ';'.join(f"{rename.get(n, n)}={sel[n]}" for n in [x['name'] for x in opts]),
                          '*StartPrice': price(v['price']), '*Quantity': str(cfg['quantity'])})
                rows.append(r)
        if len(o['title']) > 80 or title != o['title']:
            report.append(f'title: {o["title"]!r} -> {title!r} ({len(title)})')
        if not pics:
            report.append(f'NO PICTURES: {o["title"]}')
    return cols, rows, report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('export'); ap.add_argument('listcsv'); ap.add_argument('out')
    ap.add_argument('--config', required=True); ap.add_argument('--tier'); ap.add_argument('--limit', type=int)
    ap.add_argument('--exclude-regex')
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding='utf-8'))
    tpl = (HERE / 'templates' / 'listing.html').read_text(encoding='utf-8')
    prods = load_export(a.export)
    order = []
    for r in csv.DictReader(open(a.listcsv, encoding='utf-8')):
        if a.tier and r['tier'] != a.tier:
            continue
        if a.exclude_regex and re.search(a.exclude_regex, r['title'], re.I):
            continue
        order.append(r['product_id'])
    if a.limit:
        order = order[:a.limit]
    cols, rows, report = build(prods, order, cfg, tpl)
    with open(a.out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, cols)
        w.writeheader()
        w.writerows(rows)
    with open(Path(a.out).with_suffix('.sku-map.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['ebay_custom_label', 'shopify_sku'])
        w.writerows(sorted(SKU_MAP.items()))
    rep = Path(a.out).with_suffix('.report.txt')
    rep.write_text('\n'.join(report) + '\n', encoding='utf-8')
    print(f'{a.out}: {len(order)} listings, {len(rows)} rows; report {rep.name}')


if __name__ == '__main__':
    main()
