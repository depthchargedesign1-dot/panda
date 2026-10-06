"""Copy-QA engine for live face-mask products. Reads work.json (live values), writes proposed.json + changes report.
Never touches titles/handles/status/prices/images. Only descriptionHtml and seo{title,description} (+ tag third-party-name for sensitive)."""
import json, re, sys, unicodedata, collections
sys.path.insert(0, '.')
from dec_names import N as NAMEOPS
from dec_custom import X, B, SKIPBLURB
from dec_chars import C as CHARS, BRAND, disc_tv, disc_brand
import dec_sens
from pools import OCC, FAM, GENERIC

P = 'gid://shopify/Product/'
live = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'work.json'))
names = json.load(open('../push/titles/names.json'))
LEAK = json.load(open('leak_map.json'))
LEAK.update({P + '9520533448': 'cricket', P + '9520750024': 'snooker', P + '7807382388987': 'tv', P + '14931220103549': 'film',
             P + '15834842628477': 'football', P + '15836925428093': 'football', P + '8249154797819': 'tv', P + '7551007916283': 'tv'})
R = '/home/user/panda/foxyprinting-rebrand/exports/rollback/2026-10-05-sensitive-masks/'
EXCL = {p['id'] for f in ('after.json', 'after_hall_glitter.json') for p in json.load(open(R + f))}
EXCL |= {P + '9438652104', P + '9614911688', P + '9438651336', P + '9530631496'}
SEO_TITLE_KEEP = {P + '6890951671995', P + '8042789535995', P + '4328413233227'}
MANUALSEO = {P + '8245753905403': 'Baby Face Mask | Foxy Printing', P + '9437813256': 'Madge Face Mask | Foxy Printing', P + '9437813512': 'Mel Face Mask | Foxy Printing', P + '15865891815805': 'Harry Lewis (W2S) Face Mask | Foxy Printing'}

def fold(s):
    return unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower().replace('-', ' ').replace('.', '').replace("'", '').replace('’', '').strip()

# ---------------- pools for leakage ----------------
NEWPOOL = {'film': ['a movie night', 'a red-carpet party', 'a film-themed birthday'],
           'tv': ['a series finale watch party', 'a telly-night quiz', 'a box-set binge night'],
           'reality': ['a finale watch party', "a girls' night in", 'a hen do'],
           'music': ['a concert pre-party', 'a karaoke night', 'a festival weekend'],
           'comedy': ['a comedy night', 'a birthday roast', 'a stag or hen do'],
           'sport': ['a sports-themed birthday', 'a big-game watch party', 'a sports club social'],
           'boxing': ['a fight-night watch party', 'a boxing-themed stag do', 'a big-fight night'],
           'football': ['a big match watch party', 'a five-a-side end-of-season do', 'a football-themed birthday'],
           'cricket': ['a cricket club dinner', 'a Test match day out', 'a summer cricket social'],
           'snooker': ['a snooker hall night out', 'a club tournament social', 'a cue-sports birthday'],
           'royal': ['a royal-themed street party', 'a British history night', 'a street party'],
           'celeb': ['a birthday party', 'a stag or hen do', 'a fancy dress night out']}
NEWLABEL = {'film': 'film star', 'tv': 'TV star', 'reality': 'reality TV star', 'music': 'music star', 'comedy': 'comedian', 'sport': 'sports star',
            'boxing': 'boxer', 'football': 'football star', 'cricket': 'cricketer', 'snooker': 'snooker star', 'royal': 'public figure', 'celeb': 'celebrity'}
NEWWHO = {'film': 'film fans', 'tv': 'TV fans', 'reality': 'reality TV fans', 'music': 'music fans', 'comedy': 'comedy fans', 'sport': 'sports fans',
          'boxing': 'fight fans', 'football': 'football fans', 'cricket': 'cricket fans', 'snooker': 'snooker fans', 'royal': 'anyone who loves a laugh at the big names',
          'celeb': 'anyone planning a party'}
NEWFAM = {'film': 'V', 'tv': 'V', 'reality': 'V', 'comedy': 'V', 'music': 'M', 'royal': 'R', 'celeb': 'C', 'sport': 'S', 'boxing': 'S', 'football': 'S', 'cricket': 'S', 'snooker': 'S'}
ALLLABELS = ['football star', 'darts star', 'golfer', 'Formula 1 driver', 'tennis star', 'boxer', 'cricketer', 'rugby star', 'snooker star', 'sports star',
             'public figure', 'music star', 'comedian', 'reality TV star', 'film star', 'TV star', 'celebrity']
LABFAM = {'football star': 'S', 'darts star': 'S', 'golfer': 'S', 'Formula 1 driver': 'S', 'tennis star': 'S', 'boxer': 'S', 'cricketer': 'S', 'rugby star': 'S',
          'snooker star': 'S', 'sports star': 'S', 'public figure': 'R', 'music star': 'M', 'comedian': 'V', 'reality TV star': 'V', 'film star': 'V', 'TV star': 'V', 'celebrity': 'C'}
ALLWHO = ['football fans', 'darts fans', 'golf fans', 'motorsport fans', 'tennis fans', 'fight fans', 'cricket fans', 'rugby fans', 'snooker fans', 'sports fans',
          'anyone who loves a laugh at the big names', 'music fans', 'comedy fans', 'reality TV fans', 'film fans', 'TV fans']
WHOFAM = {'football fans': 'S', 'darts fans': 'S', 'golf fans': 'S', 'motorsport fans': 'S', 'tennis fans': 'S', 'fight fans': 'S', 'cricket fans': 'S', 'rugby fans': 'S',
          'snooker fans': 'S', 'sports fans': 'S', 'anyone who loves a laugh at the big names': 'R', 'music fans': 'M', 'comedy fans': 'V', 'reality TV fans': 'V',
          'film fans': 'V', 'TV fans': 'V'}
ALLOCC = sorted(OCC, key=len, reverse=True)

def first_p_split(d):
    m = re.match(r'(<p>.*?</p>)', d, re.S)
    return (m.group(1), d[m.end():]) if m else ('', d)

def sub_all(rx, new, s):
    return re.sub(rx, lambda m: new, s)

def apply_ops(ops, d, m, t, skipblurb=False):
    for rx, new in ops:
        if skipblurb:
            a, b = first_p_split(d); d = a + sub_all(rx, new, b)
        else:
            d = sub_all(rx, new, d)
        m = sub_all(rx, new, m); t = sub_all(rx, new, t)
    return d, m, t

def set_disc(d, text):
    return re.sub(r'(<p class="disclaimer">)(.*?)(</p>)', lambda mm: mm.group(1) + text + mm.group(3), d, count=1, flags=re.S)

JUNK = (r"England Euros|England|Euros|Bollywood|Breaking Bad|Bad Boys|Still Game|X-Factor|X Factor|Celebrity Party|Heartstopper|Lupin|Ozark|Narcos|Brooklyn|Bridgerton|"
        r"Eurovision|Sidemen|Shameless|Dallas|Ab Fab|Benidorm|Derry Girls|Lakeside|Mancity|Argentina|Brazil|Italy|UK|Olympic|Christmas|Halloween|Comedy|Colour|TV Stars|TV Star|"
        r"Strictly|Towie|Hollyoaks|EastEnders|Emmerdale|Minecraft|Golden Globes 2025 Celebrity Face Masks")

def strip_junk(n, s):
    if not n or len(n) < 4:
        return s
    rx = r'(?<![\w-])' + re.escape(n) + r'((?: (?:' + JUNK + r'))+)(?=(?: (?:[Cc]ard )?[Ff]ace [Mm]asks?| has not| [Cc]elebrity|:|\.|,| \|))'
    s2 = re.sub(rx, n, s)
    s2 = s2.replace(n + ' Face Mask Face Mask', n + ' Face Mask')
    return s2

# ---------------- truncated metas ----------------
def fix_trunc(m, fam_hint=None):
    orig = m
    LIM = 155
    def fits(x): return len(x) <= LIM
    if m.endswith(' Posted in a board-backed.'):
        c = m[:-len(' Posted in a board-backed.')] + ' Posted in a board-backed envelope.'
        m = c if fits(c) else m[:-len(' Posted in a board-backed.')]
    if m.endswith(' and photo.'):
        c = m[:-len(' and photo.')] + ' and photo booths.'
        m = c if fits(c) else m[:-len(' and photo.')] + '.'
    if m.endswith(' Order.'):
        c = m[:-len(' Order.')] + ' Order today.'
        m = c if fits(c) else m[:-len(' Order.')]
    mm = re.search(r'((?:Great|Perfect) for )((?:an?|the) [^.]+?)( and photo booths)?\.$', m)
    if mm:
        phrase = mm.group(2)
        if phrase not in OCC and phrase not in NEWPOOL_ALL:
            comps = [o for o in OCC if o.startswith(phrase) and o != phrase]
            head = m[:mm.start(2)]; tail = (mm.group(3) or '') + '.'
            done = False
            for o in sorted(comps, key=len):
                if fits(head + o + tail):
                    m = head + o + tail; done = True; break
            if not done:
                key = OCC.get(comps[0]) if comps else None
                alts = (sorted([o for o in OCC if OCC[o] == key], key=len) if key else []) + ['a hen do', 'a party']
                for o in alts:
                    if fits(head + o + tail):
                        m = head + o + tail; done = True; break
            if not done:
                m = m[:mm.start(1)].rstrip()
    return m

NEWPOOL_ALL = {o for v in NEWPOOL.values() for o in v}

# ---------------- leakage ----------------
def fix_leak(key, d, m):
    tf = NEWFAM[key]; pool = NEWPOOL[key]
    found = []
    for txt in (d, m):
        for o in ALLOCC:
            if o in GENERIC or o in pool:
                continue
            if FAM[OCC[o]] != tf and o in txt and o not in found and not any(o in f for f in found):
                found.append(o)
    # deterministic mapping, avoid duplicates with phrases already present
    present = [p for p in pool if p in d or p in m]
    avail = [p for p in pool if p not in present] + present
    mp = {}
    for i, o in enumerate(found):
        mp[o] = avail[i % len(avail)]
    for o, n in sorted(mp.items(), key=lambda x: -len(x[0])):
        d = d.replace(o, n); m = m.replace(o, n)
    for lab in ALLLABELS:
        if LABFAM[lab] != tf and lab != NEWLABEL[key]:
            d = re.sub(r'\b(this|the|a) ' + re.escape(lab) + r' (mask|face)\b', lambda x: f'{x.group(1)} {NEWLABEL[key]} {x.group(2)}', d)
    for w in ALLWHO:
        if WHOFAM[w] != tf and w != NEWWHO[key]:
            d = re.sub(r'(?<=for |ith )' + re.escape(w) + r'\b', NEWWHO[key], d)
    return d, m

ROYAL = re.compile(r"\b(King|Queen|Prince|Princess|Duke|Duchess|Royal|Camilla|Meghan|Markle|Middleton|Diana|Eugenie|Beatrice|Zara|Sophie|Coronation|Jubilee|Elizabeth|Charles|Philip|Harry|William|Edward|Anne|Margaret|Andrew|Wessex|Parker Bowles|Sarah Ferguson|George|Claire Foy|Erin Doherty|Denis Thatcher)\b")

def fix_jubilee(title, d, m):
    if ROYAL.search(title):
        return d, m
    for a, b in (('a jubilee-style garden party', 'a summer garden party'), ('a jubilee-style garden do', 'a summer garden party'),
                 ('a jubilee-style garden.', 'a summer garden party.')):
        d = d.replace(a, b); m = m.replace(a, b)
    return d, m

def fix_themed(d):
    d = d.replace('An easy, cheap way to theme a themed birthday', 'An easy, cheap way to theme a birthday party')
    d = re.sub(r'An easy, cheap way to theme (an?) ([\w-]+-themed )', r'An easy, cheap way to liven up \1 \2', d)
    return d

def fix_meta_tm(m):
    m = m.replace('an Oscars-style party', 'a red-carpet party').replace('An Oscars-style party', 'A red-carpet party')
    m = m.replace('a Six Nations watch party', 'a rugby watch party')
    m = m.replace(' Golden Globes 2025 Celebrity Face Masks', ' Face Mask')
    return m

# ---------------- SEO titles ----------------
DESC_OK = {'Young', 'Old', 'Cap', 'Beard', 'Cartoon', 'Laughing', 'Smiling', 'Sad', 'Hat', 'Glasses', 'Sunglasses', 'Colour', 'Short Hair', 'Long Hair', 'Blonde', 'Red Hair', 'New Hair'}
NAMEFIX = {'Jada Pinkett': 'Jada Pinkett Smith', 'Jamie Lee': 'Jamie Lee Curtis', 'Emmett J': 'Emmett J. Scanlan', 'The Muppets Beaker': 'Beaker', 'Rhee Steven Yeun': 'Steven Yeun', 'Tony Pulis-Welsh': 'Tony Pulis', 'Mini-Me': 'Mini-Me'}
BADN = re.compile(r"^(Batman The|Madge From|MEL From|Prince William Baby|Jimmy Hill Portrait|Norris McWhirter Left|Tom Oliver Lou|Sara Gilbert Darlene|Jason Biggs Jim|"
                  r"Tara Reid Vicky|Jason Voorhees Hockey|Michael Jackson Bad|Terry Butcher Blood|Travis Pastrana Portrait|Joe Tracini Dennis|Artem Strictly|Miley Cyrus Missy|"
                  r"Bricktop Alan Ford|Catherine Tate Girl|Eastenders Girl|Charlotte|Gaz|Holly|Jay|Harry|Coach|Baby|Police|Madge|Annie The|Adrian Rocky|Half .*|.* The)$")
SEO_OK = re.compile(r'^(.+?)(?: (\d{1,2}))?(?: \(([^)]+)\))? Face Mask \| Foxy Printing$')

def canon_seo(pid, t, title):
    r = names.get(pid)
    if not r or not r.get('name'):
        return None
    n = NAMEFIX.get(r['name'], r['name'])
    if BADN.match(n):
        return None
    num = r.get('num'); desc = list(r.get('desc') or [])
    mm = re.match(r'^(.*?) Face Mask(.*?)\s*\|\s*Foxy Printing$', t or '')
    tail = mm.group(2).strip() if mm else ''
    if not num:
        v = re.fullmatch(r'(?:Design )?(\d{1,2})', tail) or re.search(r' (\d{1,2})$', (mm.group(1) if mm else ''))
        if v and v.group(1) not in ('0',):
            num = str(int(v.group(1)))
    if not desc and tail in DESC_OK:
        desc = [tail]
    oldn = re.sub(r'(?: \d{1,2})$', '', mm.group(1)) if mm else ''
    if oldn and (fold(oldn) == fold(n) or (fold(oldn).startswith(fold(n) + ' ') and len(fold(n)) >= 6 and re.search(r'[A-Z]\.?$', n))):
        n = oldn
    core = n + (' ' + num if num else '') + (' (' + ', '.join(desc) + ')' if desc else '')
    out = core + ' Face Mask | Foxy Printing'
    if len(out) > 60 and len(desc) > 1:
        out = n + (' ' + num if num else '') + ' (' + desc[0] + ') Face Mask | Foxy Printing'
    if len(out) > 60:
        out = n + (' ' + num if num else '') + ' Face Mask | Foxy Printing'
    if len(out) > 60:
        return None
    return out

def needs_seo(pid, t):
    r = names.get(pid)
    mm = SEO_OK.match(t or '')
    if not mm or len(t) > 60:
        return True
    if r and r.get('name') and fold(mm.group(1)) != fold(NAMEFIX.get(r['name'], r['name'])):
        return True
    return False

# ---------------- a/an ----------------
AN_LETTERS = set('AEFHILMNORSX')
def want_an(word):
    w = word.strip('"\'‘’“”(')
    w = w.rstrip('.,;:!?)')
    if re.fullmatch(r'[A-Z]', w):
        return w in AN_LETTERS
    if not w or w[0].isdigit():
        return None
    if w.startswith('The') and (len(w) == 3):
        return 'THE'
    if re.match(r'[A-Z](?:&|\.[A-Z])', w):
        return w[0] in AN_LETTERS
    if re.fullmatch(r'[A-Z0-9]{2,4}', w) and not re.fullmatch(r'[A-Z][a-z]+', w):
        if w in ('UFC', 'USA', 'UEFA'):
            return False
        return w[0] in AN_LETTERS
    if re.match(r'(?i)(eu|one|once|uni[^s]|union|united|ukrain|usa\b|use|ufc)', w):
        return False
    if re.match(r'(?i)(hour|honest|heir|honou?r)', w):
        return True
    return unicodedata.normalize('NFKD', w[0]).encode('ascii', 'ignore').decode().upper() in 'AEIOU' or w[0] in 'ØÆ'

def fix_articles(s):
    def rep(mo):
        art, word = mo.group(1), mo.group(2)
        wa = want_an(word)
        if wa is None or wa == 'THE':
            return mo.group(0)
        if wa and art.lower() == 'a':
            return ('An' if art[0] == 'A' else 'an') + ' ' + word
        if not wa and art.lower() == 'an':
            return ('A' if art[0] == 'A' else 'a') + ' ' + word
        return mo.group(0)
    s = re.sub(r'(?<![\w-])([Aa]n?) ([A-Z0-9ÁÉÍÓÚØÖÜÆ][^\s<]*)', rep, s)
    # "a The X face mask" -> "a face mask of The X"
    s = re.sub(r'(?<![\w-])([Aa]n?) (The [^.<,:;!?]{1,40}?) face mask', lambda mo: ('A' if mo.group(1)[0] == 'A' else 'a') + ' face mask of ' + mo.group(2), s)
    return s

# ---------------- couples ----------------
COUPLE = re.compile(r'^(.*?) (?:and|And|&) (.*?) (?:Celebrity Couple|-Roadhouse|Fight Mask Pack)')
COUPLEFIX = {'Brad|George Takei': ('George Takei', 'Brad Takei'), 'Victoria|David Beckham': ('Victoria Beckham', 'David Beckham'),
             'Kim Kardashian|Kanye': ('Kim Kardashian', 'Kanye West'), 'Gerry Corner|Christian Horner': ('Geri Horner', 'Christian Horner'),
             'Francis Nganou|Tyson Fury': ('Francis Ngannou', 'Tyson Fury'), 'Savannah Brinson|Lebron James': ('Savannah Brinson', 'LeBron James'),
             'Ellen Degeneres|Portia De Rossi': ('Ellen DeGeneres', 'Portia de Rossi'), 'Tom Brady|Gisele Bundchen': ('Tom Brady', 'Gisele Bündchen')}

def couple_names(title):
    mo = COUPLE.match(title)
    if not mo:
        return None
    a, b = mo.group(1).strip(), mo.group(2).strip()
    return COUPLEFIX.get(a + '|' + b, (a, b))

def fix_couple(pid, title, d, t):
    cn = couple_names(title)
    if not cn:
        return d, t, False
    a, b = cn
    nt = None
    for cand in (f'{a} & {b} Couple Face Masks | Foxy Printing', f'{a} & {b} Face Masks | Foxy Printing', f'{a} & {b} | Foxy Printing'):
        if len(cand) <= 60:
            nt = cand; break
    mo = re.search(r'<p class="disclaimer">This is an unofficial novelty product made for fun and fancy dress\. (.*?) has not endorsed, sponsored or approved this product, and Foxy Printing has no connection with them(.*?)\. The names? (?:is|are) used only to describe the design\.</p>', d)
    if mo and (fold(a) not in fold(mo.group(1)) or fold(b) not in fold(mo.group(1))):
        new = (f'<p class="disclaimer">This is an unofficial novelty product made for fun and fancy dress. {a} and {b} have not endorsed, sponsored or approved this product, '
               f'and Foxy Printing has no connection with them{mo.group(2)}. The names are used only to describe the design.</p>')
        d = d[:mo.start()] + new + d[mo.end():]
    return d, (nt or t), True

# ---------------- main ----------------
out = {}; log = collections.defaultdict(list); tagadd = []
for pid, p in live.items():
    if pid in EXCL:
        continue
    d0, m0, t0 = p['descriptionHtml'], p['seo']['description'] or '', p['seo']['title'] or ''
    d, m, t = d0, m0, t0
    types = []
    def mark(tp, before):
        if (d, m, t) != before:
            types.append(tp)
    if pid in dec_sens.S:
        d, m, t = dec_sens.build(dec_sens.S[pid]); types.append('sensitive')
        if 'third-party-name' not in p['tags']:
            tagadd.append(pid)
    else:
        b4 = (d, m, t)
        ops = list(NAMEOPS.get(pid, [])) + list((X.get(pid) or {}).get('ops', []))
        if ops:
            d, m, t = apply_ops(ops, d, m, t, skipblurb=(pid in SKIPBLURB or pid in B or bool((X.get(pid) or {}).get('blurb'))))
        mark('name', b4); b4 = (d, m, t)
        bl = B.get(pid) or (X.get(pid) or {}).get('blurb')
        if bl:
            a, rest = first_p_split(d); d = bl + rest
        mark('wrong-person/char blurb', b4); b4 = (d, m, t)
        if pid in CHARS:
            d = set_disc(d, disc_tv(*CHARS[pid]))
        elif pid in BRAND:
            d = set_disc(d, disc_brand(BRAND[pid]))
        elif (X.get(pid) or {}).get('disc'):
            d = set_disc(d, X[pid]['disc'])
        mark('disclaimer', b4); b4 = (d, m, t)
        nm = (names.get(pid) or {}).get('name')
        if nm and fold(nm) in fold(p['title']) and not BADN.match(nm):
            d, m, t = strip_junk(nm, d), strip_junk(nm, m), strip_junk(nm, t)
        mark('name-junk', b4); b4 = (d, m, t)
        m = fix_trunc(m)
        mark('truncated-meta', b4); b4 = (d, m, t)
        if pid in LEAK:
            d, m = fix_leak(LEAK[pid], d, m)
        mark('template-leakage', b4); b4 = (d, m, t)
        d, m = fix_jubilee(p['title'], d, m)
        mark('jubilee-leakage', b4); b4 = (d, m, t)
        d = fix_themed(d)
        mark('themed-duplication', b4); b4 = (d, m, t)
        d, m, t = d.replace("Dragon's Den", "Dragons' Den"), m.replace("Dragon's Den", "Dragons' Den"), t.replace("Dragon's Den", "Dragons' Den")
        mark('dragons-den', b4); b4 = (d, m, t)
        m = fix_meta_tm(m)
        mark('trademark-in-meta', b4); b4 = (d, m, t)
        d, t2, is_couple = fix_couple(pid, p['title'], d, t)
        if is_couple:
            t = t2
        mark('couple', b4); b4 = (d, m, t)
        if pid in MANUALSEO:
            t = MANUALSEO[pid]
        elif not is_couple and pid not in SEO_TITLE_KEEP and needs_seo(pid, t):
            c = canon_seo(pid, t, p['title'])
            if c:
                t = c
        mark('seo-title', b4); b4 = (d, m, t)
        d, m = fix_articles(d), fix_articles(m)
        mark('a/an', b4); b4 = (d, m, t)
    if m != m0 and len(m) > 160:
        m = re.sub(r' (?:Order today|Order yours today|Order now[^.]*|Add it to your basket today|Treat them today)\.$', '', m)
    if (d, m, t) != (d0, m0, t0):
        out[pid] = dict(id=pid, title=p['title'], types=types, old=dict(d=d0, m=m0, t=t0), new=dict(d=d, m=m, t=t))
json.dump(out, open('proposed.json', 'w'), ensure_ascii=False)
json.dump(tagadd, open('tagadd.json', 'w'))
cnt = collections.Counter(tp for v in out.values() for tp in v['types'])
print('products changed', len(out), dict(cnt), 'tagadd', len(tagadd))
