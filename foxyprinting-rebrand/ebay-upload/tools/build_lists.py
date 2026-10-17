#!/usr/bin/env python3
"""eBay upload project: sort the live Shopify range into upload lists (masks, posters, mugs, baby grows).

Inputs (both made through the Shopify MCP, saved in ../source/):
  active.jsonl   bulkOperationRunQuery on products(query:"status:active") with
                 id handle title productType vendor tags totalInventory priceRangeV2 variantsCount mediaCount
                 featuredMedia{preview{image{url}}} options{name values}
  sales365.json  ShopifyQL rows: FROM sales SHOW net_items_sold, gross_sales GROUP BY product_title
                 SINCE -365d UNTIL today ORDER BY net_items_sold DESC LIMIT 1000

Every product gets a tier:
  A  list first: our own designs and personalised items, no other person's or brand's name or face.
  B  check first: a third-party name in the text only (club names, film/TV characters, car makes, memes)
     or adult humour. eBay can remove these on a rights-owner report or for offensive wording.
  C  high risk on eBay: a real person's face, name or printed signature (celebrity masks, Printed Signature
     posters, celebrity mugs). eBay's faces, names and signatures policy doesn't allow these without the
     person's permission. Only list them if the owner accepts the risk, starting with a small test batch.
  X  don't list on eBay: club crests / logos / console box art, notorious criminals, "do not use" items,
     and checkout add-ons (upgrade listings) that only make sense on Shopify.

Usage:  python3 -I tools/build_lists.py source/active.jsonl source/sales365.json lists/
"""
import csv, json, os, re, sys
from collections import Counter

BATCH = 500  # listings per upload file (eBay's Seller Hub Reports limit is about 14.9 MB per file)

NOTORIOUS = re.compile(r"\b(epstein|savile|rolf harris|r\.? ?kelly|hitler|bin laden|saddam|gaddafi|"
                       r"harold shipman|ian huntley|fred west|rose west|myra hindley|ted bundy|charles manson|"
                       r"jeffrey dahmer|prince andrew|ghislaine)\b", re.I)
ADDON = re.compile(r"upgrade|total calculated at checkout|add any name on the back|do not use", re.I)
RETRO_GAME = re.compile(r"\b(neo ?geo|retro gaming|game inspired|arcade|jaguar cd|gamecube|nes|snes|sega|mega ?drive|megadrive|genesis|game ?cube|gameboy|game boy|"
                        r"playstation|ps1|ps2|n64|nintendo|dreamcast|saturn|atari|xbox|master system)\b", re.I)
CLUB_LOGO = re.compile(r"football team face covering|\bbadges?\b|\bcrests?\b|\blogos?\b", re.I)
# Football clubs, stadiums and car makes named in the text (trademarks: tier B, never A)
CLUBS = re.compile(r"\b(united|city|rovers|town|athletic|albion|wanderers|county|hotspur|tottenham|spurs|arsenal|"
                   r"chelsea|liverpool|everton|celtic|rangers|villa|palace|forest|wednesday|orient|argyle|"
                   r"hibernian|hearts|aberdeen|dundee|motherwell|kilmarnock|fulham|brentford|burnley|watford|"
                   r"newcastle|sunderland|middlesbrough|middlesborugh|millwall|wolves|west ham|leeds|bournemouth|"
                   r"southampton|brighton|reading|stoke|barnsley|blackburn|blackpool|bolton|wigan|walsall|"
                   r"stevenage|grimsby|accrington|wrexham|portsmouth|ipswich|norwich|derby|coventry|southend|"
                   r"football club|\bfc\b|stadium|premier league|bmw|audi|mercedes|ferrari|porsche|land rover|"
                   r"range rover|volkswagen|\bvw\b|vauxhall|tesla|toyota|nissan|honda|harley|ducati|jcb|"
                   r"john deere|massey ferguson|disney|marvel|pixar|star wars|harry potter|pokemon|lego|barbie|"
                   r"minions?|starfleet|star trek|muppets?|batman|superman|spider-?man|budweiser|guinness|"
                   r"inspired by|inspired)\b", re.I)
SWEAR = re.compile(r"fuck|shit|cunt|twat|wank|\bslag|bitch|bollock|\bdick|\bcock\b|\bpiss|\barse|\btits?\b|"
                   r"\bknob|bastard|\bprick|whore|\bslut|bellend|\bf\*|\bsh\*t|\*", re.I)
CELEB_TYPES = re.compile(r"celebrit|tv stars|footballer|golfer|politician|royal|movie actor|f1 face|darts face|"
                         r"cricket face|boxer face|rugby face|eastenders|olympics|james bond|tennis face|xfactor|"
                         r"snooker face|sports face|man city|signed|athlet", re.I)
PERSONAL_MASK = re.compile(r"personalised|custom photo|your (own )?(photo|face)|(groom|bride)'?s face|"
                           r"make your own", re.I)
PRINTED_SIG = re.compile(r"printed signature|signed|autograph|signature", re.I)
ADULT = re.compile(r"adult|rude|naughty", re.I)
CELEB_MUG = re.compile(r"celebrity|movie star|band|music artist|superfan|celebrity husband|meme|gaming|motor|car mug|"
                       r"football crazy|keep calm support|signs for football", re.I)


def category(o):
    t = (o['productType'] + ' ' + o['title']).lower()
    if 'mask' in t and 'card' not in o['productType'].lower():
        return 'masks'
    if re.search(r'baby ?grow|baby vest|babygrow|bodysuit', t):
        return 'baby-grows'
    if re.search(r'\bmugs?\b', t):
        return 'mugs'
    if re.search(r'poster|\bprints?\b', t) and not re.search(r'keyring|magnet|\bcase\b|\bcards?\b|t-shirt|shirt|cushion|'
                                                         r'glass|flute|tumbler|bottle|laptop|pyjama|treat box|'
                                                         r'metal|panel|bundle|mug', t):
        return 'posters'
    return None


def tier(o, cat):
    title, pt, tags = o['title'], o['productType'], ' '.join(o['tags'])
    blob = f"{title} {pt} {tags}"
    if ADDON.search(title):
        return 'X', 'checkout add-on / not for sale on its own'
    if NOTORIOUS.search(title):
        return 'X', 'notorious person: eBay offensive-material policy'
    if re.search(r'caricature|ting tong|blackface|yellowface', title, re.I):
        return 'X', 'racial caricature'
    if cat == 'masks':
        if CLUB_LOGO.search(title):
            return 'X', 'club crest / logo'
        if re.search(r'request any', title, re.I):
            return 'B', 'made-to-order celebrity mask service: check the listing pictures show no real faces'
        if PERSONAL_MASK.search(title):
            return 'A', 'personalised mask from the customer\'s own photo'
        if pt in ('Halloween Mask', 'Kids Face Masks') and not CLUBS.search(title):
            return 'B', 'Halloween / kids mask: check each one; film or TV characters (Disney, Muppets, Minions) are high risk'
        return 'C', 'real person\'s face (celebrity / sports star mask)'
    if cat == 'posters':
        if RETRO_GAME.search(pt) or RETRO_GAME.search(title) or ('Other Console Posters' in o['tags'] and RETRO_GAME.search(blob)):
            return 'X', 'console / game box art (publisher logos)'
        if CLUB_LOGO.search(title):
            return 'X', 'club crest / logo'
        if re.search(r'movie|film|franchise|horror|hunger games|lord of the rings|indiana jones|terminator|'
                     r'friday the 13th|michael myers|ghibli', title, re.I):
            return 'C', 'film artwork / characters owned by the studio'
        if PRINTED_SIG.search(blob) or CELEB_TYPES.search(pt) or re.search(r'unofficial', title, re.I):
            return 'C', 'real person\'s photo + printed signature'
        if re.search(r'^(all poster sizes|choose (your )?poster size|poster size|poster$|copy of)', title.strip(), re.I):
            return 'X', 'checkout add-on / not for sale on its own'
        if 'third-party-name' in o['tags'] or CLUBS.search(title):
            return 'B', 'third-party name in the design (club, stadium, brand or character)'
        if SWEAR.search(title):
            return 'B', 'adult wording: check against eBay\'s offensive-material policy'
        return 'A', 'own design (word art, travel, personalised)'
    if cat == 'mugs':
        if CLUB_LOGO.search(title):
            return 'X', 'club crest / logo'
        if re.search(r'celebrity', pt + ' ' + tags, re.I) or re.search(r'Male Movie Stars|Female Movie Stars|Top 100', tags):
            return 'C', 'real person\'s name / face'
        if SWEAR.search(title) or ADULT.search(pt + ' ' + title) or 'ADULT MUGS (RUDE)' in o['tags']:
            return 'B', 'adult humour: check wording against eBay\'s offensive-material policy'
        if 'third-party-name' in o['tags'] or CELEB_MUG.search(pt) or CLUBS.search(title):
            return 'B', 'third-party name (club, band, brand, game or meme)'
        return 'A', 'own design / personalised'
    if cat == 'baby-grows':
        if CLUB_LOGO.search(title):
            return 'X', 'club crest / logo'
        if 'FOOTBALL' in o['tags'] or 'third-party-name' in o['tags'] or CLUBS.search(title):
            return 'B', 'club or brand name in the text (no crest): check first'
        if SWEAR.search(title):
            return 'B', 'adult wording: check against eBay\'s offensive-material policy'
        return 'A', 'own design / personalised'
    return None, ''


def main(src, sales_path, out):
    sales = {}
    for r in json.load(open(sales_path)):
        sales[r[0].strip().lower()] = int(float(r[1]))
    rows = {k: [] for k in ('masks', 'posters', 'mugs', 'baby-grows')}
    for line in open(src):
        o = json.loads(line)
        cat = category(o)
        if not cat:
            continue
        t, why = tier(o, cat)
        img = ((o.get('featuredMedia') or {}).get('preview') or {}).get('image') or {}
        pr = o.get('priceRangeV2') or {}
        title = o['title']
        rows[cat].append({
            'tier': t, 'tier_reason': why,
            'sold_12m': sales.get(title.strip().lower(), 0),
            'title': title, 'title_chars': len(title),
            'ebay_title_ok': 'yes' if len(title) <= 80 else 'shorten (eBay max 80)',
            'product_type': o['productType'],
            'variants': (o.get('variantsCount') or {}).get('count', ''),
            'options': ' / '.join(f"{x['name']}: {', '.join(x['values'][:8])}" for x in o.get('options', [])
                                  if x['name'] != 'Title'),
            'price_min': (pr.get('minVariantPrice') or {}).get('amount', ''),
            'price_max': (pr.get('maxVariantPrice') or {}).get('amount', ''),
            'images': (o.get('mediaCount') or {}).get('count', ''),
            'main_image': img.get('url', ''),
            'handle': o['handle'],
            'shopify_url': f"https://foxyprinting.co.uk/products/{o['handle']}",
            'product_id': o['id'],
        })
    os.makedirs(out, exist_ok=True)
    order = {'A': 0, 'B': 1, 'C': 2, 'X': 3}
    prefix = {'masks': '1', 'posters': '2', 'mugs': '3', 'baby-grows': '4'}
    code = {'masks': 'M', 'posters': 'P', 'mugs': 'U', 'baby-grows': 'B'}
    summary = []
    for cat, L in rows.items():
        L.sort(key=lambda r: (order[r['tier']], -r['sold_12m'], r['title'].lower()))
        n = Counter()
        for r in L:
            if r['tier'] == 'X':
                r['batch'] = 'do not list'
                continue
            n[r['tier']] += 1
            r['batch'] = f"{code[cat]}-{r['tier']}-{(n[r['tier']] - 1) // BATCH + 1:02d}"
        cols = ['batch', 'tier', 'tier_reason', 'sold_12m', 'title', 'title_chars', 'ebay_title_ok', 'product_type',
                'variants', 'options', 'price_min', 'price_max', 'images', 'main_image', 'handle', 'shopify_url',
                'product_id']
        path = os.path.join(out, f"{prefix[cat]}-{cat}.csv")
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, cols)
            w.writeheader()
            w.writerows(L)
        c = Counter(r['tier'] for r in L)
        sold = Counter()
        for r in L:
            sold[r['tier']] += r['sold_12m']
        long_titles = sum(1 for r in L if r['tier'] != 'X' and r['title_chars'] > 80)
        no_img = sum(1 for r in L if r['tier'] != 'X' and not r['main_image'])
        summary.append({'category': cat, 'file': os.path.basename(path), 'total': len(L),
                        **{f'tier_{k}': c.get(k, 0) for k in 'ABCX'},
                        **{f'sold_12m_{k}': sold.get(k, 0) for k in 'ABC'},
                        'titles_over_80': long_titles, 'no_main_image': no_img})
    with open(os.path.join(out, '0-summary.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, list(summary[0]))
        w.writeheader()
        w.writerows(summary)
    for s in summary:
        print(s)


if __name__ == '__main__':
    main(*sys.argv[1:4])
