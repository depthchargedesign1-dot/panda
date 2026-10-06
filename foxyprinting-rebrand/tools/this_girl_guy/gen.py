import json, re, hashlib, collections, sys
from slog import slogan
from topics import T, SKIP, FOODLINE
from fans import A, D

def pron(line):
    line = re.sub(r"\bhe’s\b", "{she}’s", line)
    line = re.sub(r"\bhis\b", "{her}", line)
    line = re.sub(r"\bhe\b", "{she}", line)
    line = re.sub(r"\bhim\b", "{him}", line)
    line = re.sub(r"\bshe\b", "{she}", line)
    line = re.sub(r"\bher\b", "{her}", line)
    return line

G = {'girl': dict(she='she', She='She', her='her', Her='Her', him='her', girl='girl', woman='woman', parent='dog mum', who='her', pal='girlfriend'),
     'guy': dict(she='he', She='He', her='his', Her='His', him='him', girl='guy', woman='man', parent='dog dad', who='him', pal='mate')}

BRANDS = {'AC Cars': ('AC Cars', 'AC Cars'), 'Cadillacs': ('Cadillac', 'Cadillac'), 'Chevrolets': ('Chevrolet', 'Chevrolet'), 'Fords': ('Ford', 'Ford'),
          'Hondas': ('Honda', 'Honda'), 'Audis': ('Audi', 'Audi'), 'iPhones': ('Apple', 'iPhone'), 'Facebook': ('Meta', 'Facebook'), 'Twitter': ('X Corp', 'Twitter'),
          'KFC': ('KFC', 'KFC'), 'McDonald’s': ('McDonald’s', 'McDonald’s'), 'Nando’s': ('Nando’s', 'Nando’s'), 'Subway': ('Subway', 'Subway'),
          'CrossFit': ('CrossFit', 'CrossFit'), 'Bumble': ('Bumble', 'Bumble'), 'Grindr': ('Grindr', 'Grindr'), 'Match': ('Match', 'Match'),
          'POF': ('Plenty of Fish', 'POF and Plenty of Fish'), 'Tinder': ('Tinder', 'Tinder'), 'Babestation': ('Babestation', 'Babestation')}

def brand_of(kw):
    for b in BRANDS:
        if re.search(r'(?<!\w)' + re.escape(b) + r'(?!\w)', kw):
            return BRANDS[b]
    return None

def col_from(p):
    if not p['media']:
        return 'white'
    f = p['media'][0]['image']['url'].split('/')[-1].split('?')[0].lower().replace('_20', ' ')
    for c in ['pink', 'red', 'black']:
        if re.search(r'(?<![a-z])' + c + r'(?=[ _-]?mug)', f) or (c + 'mug') in f:
            return c
    return 'white'

def classify(p):
    t = p['title']
    if 'T-Shirt' in t:
        return None
    g = 'guy' if re.match(r'\s*this guy', t, re.I) else 'girl'
    if re.match(r'padel', t, re.I):
        g = 'guy'
    m = re.match(r'This (girl|guy) loves (her|his) (.*?)(?: -)? Mug - Dog Lover Mug$', t, re.I)
    if m:
        name, trait = D[m.group(3).strip(' -')]
        return dict(g=g, cat='dog', kw=f"This {g.title()} Loves {'Her' if g=='girl' else 'His'} {name}", name=name, trait=trait)
    m = re.match(r'This (Girl|Guy) is an? (.*?) SUPERFAN', t, re.I)
    if m:
        name, desc = A[m.group(2)]
        art = 'an' if re.match(r'[AEIOU]', name) and not name.startswith('Usher') else 'a'
        if name.startswith('Usher'): art = 'an'
        return dict(g=g, cat='superfan', kw=f"This {g.title()} Is {art.title()} {name} Superfan", name=name, desc=desc, artist=name)
    s = slogan(t)
    m = re.match(r'This (Girl|Guy) (.*)', s, re.I)
    pred = (m.group(2) if m else s).lower()
    if pred in SKIP:
        return dict(g=g, cat='skip', reason=SKIP[pred], pred=pred)
    cat, kwp, line = T[pred]
    kw = kwp if pred == 'padel is my hobby' else f"This {g.title()} {kwp}"
    noun = re.sub(r'^(Loves To|Loves Her|Loves His|Loves|Wants To|Wants A|Wants|Is On|Is Premium On|Is Shagging On|Is Smashing On|Is A|Is|Has A|Looks Like A)\s+', '', kwp)
    if pred == 'padel is my hobby': noun = 'Padel'
    if cat in ('food', 'drink'):
        line = {'wants food': "is always hungry and always asking what’s for tea", 'wants dinner': "is always asking what’s for tea",
                'wants coffee': "can’t start the day until the coffee’s on", 'wants tea': "is always dropping hints about putting the kettle on"}.get(pred) or FOODLINE[noun]
    d = dict(g=g, cat=cat, kw=kw, noun=noun, line=pron(line), pred=pred)
    if cat == 'celeb':
        d['artist'] = {'5SOS': '5 Seconds of Summer (5SOS)'}.get(noun, noun)
    b = brand_of(kw)
    if b:
        d['brand'] = b
    return d

def pick(seq, h, k=0):
    return seq[(h + k) % len(seq)]

OCC = {
 'sport': ["It’s a fun gift for birthdays, Christmas, end-of-season presentations or a well-earned rest day.",
           "Give it for a birthday, Christmas or after a big match – it’s the perfect post-training brew mug.",
           "It makes a great birthday or Christmas gift, or a thank-you for a coach or team-mate."],
 'hobby': ["It’s a fun gift for birthdays, Christmas or just because.",
           "Give it for a birthday, Christmas or a ‘thinking of you’ moment – it says it all before the kettle has boiled.",
           "It makes a cheerful birthday or Christmas present, or a little treat for the office."],
 'food': ["It’s a fun foodie gift for birthdays, Christmas, Secret Santa or just because.",
          "Give it for a birthday, Christmas or as a Secret Santa that will actually get used.",
          "It makes a cheerful birthday present, stocking filler or office Secret Santa."],
 'animal': ["It’s a lovely gift for birthdays, Christmas or just because, and it says it all before the first sip.",
            "Give it for a birthday or Christmas – it’s the kind of present animal lovers smile at every morning.",
            "It makes a sweet birthday or Christmas gift for any animal lover."],
 'music': ["It’s a fun gift for birthdays, Christmas or before a big gig.",
           "Give it for a birthday, Christmas or to the friend who’s always in charge of the playlist.",
           "It makes a great birthday or Christmas present for any music lover."],
 'place': ["It’s a fun gift for birthdays, Christmas or a bon voyage.",
           "Give it for a birthday, Christmas or to someone counting down to their next trip.",
           "It makes a cheerful birthday or Christmas present, or a welcome-home gift after a holiday."],
 'relation': ["It’s a heartfelt gift for birthdays, anniversaries, Valentine’s Day, Mother’s Day, Father’s Day or Christmas.",
              "Give it for an anniversary, a birthday or Christmas – it says what you mean every time the kettle goes on.",
              "It makes a sweet birthday, anniversary or Christmas present."],
 'faith': ["It’s a thoughtful gift for birthdays, Christmas, Eid, Easter or simply to show you care.",
           "Give it for a birthday, a religious festival or just because – a gentle reminder of what matters most.",
           "It makes a thoughtful present for anyone whose faith means everything to them."],
 'trait': ["It’s a fun gift for birthdays, Christmas, leaving dos or Secret Santa.",
           "Give it for a birthday, Christmas or office Secret Santa – it’s sure to raise a laugh.",
           "It makes a cheeky birthday present or a Secret Santa that gets everyone laughing."],
 'type': ["It’s a cheeky gift for birthdays, hen dos, Christmas or Secret Santa between friends.",
          "Give it for a birthday or Christmas to the friend who always knows exactly what she likes.",
          "It makes a fun, cheeky present between friends who share a sense of humour."],
 'cheeky': ["It’s a cheeky gift for birthdays, stag dos, Christmas or Secret Santa.",
            "Give it for a birthday or Christmas to the mate with a cheeky grin.",
            "It makes a fun, cheeky present between friends."],
 'rude': ["It’s a rude, laugh-out-loud gift for birthdays, Secret Santa, hen and stag dos – strictly for adults with a good sense of humour.",
          "It’s strictly one for grown-ups: a rude gift for birthdays, Christmas or Secret Santa between friends who won’t be offended.",
          "It’s an adults-only gift for birthdays, leaving dos and Secret Santa – best for friends who love rude humour."],
 'dating': ["It’s a cheeky gift for birthdays, Christmas or Secret Santa for the friend whose love life is always the main topic of conversation.",
            "Give it for a birthday or Christmas to the friend who keeps the group chat updated on every date.",
            "It makes a fun, cheeky present for anyone giving online dating a go."],
 'datingrude': ["It’s a rude, laugh-out-loud gift for birthdays, stag and hen dos or Secret Santa – strictly for adults.",
                "It’s strictly one for grown-ups: a cheeky gift for birthdays, Christmas or Secret Santa between friends who won’t be offended.",
                "It’s an adults-only joke gift for the friend with the most talked-about love life."],
 'brand': ["It’s a fun gift for birthdays, Christmas or Secret Santa.",
           "Give it for a birthday, Christmas or as a Secret Santa that will actually get used.",
           "It makes a cheerful birthday present or office Secret Santa."],
 'celeb': ["It’s a fun gift for birthdays, Christmas or before a big gig.",
           "Give it for a birthday or Christmas to the biggest fan you know.",
           "It makes a great birthday or Christmas present for a true fan."],
}
OCC['drink'] = OCC['food']; OCC['brandsport'] = OCC['sport']
OCC['superfan'] = OCC['celeb']
OCC['dog'] = ["It’s a lovely gift for birthdays, Christmas or a new puppy, and it says it all before the first sip.",
              "Give it for a birthday, Christmas or from the dog – yes, we know who really buys these.",
              "It makes a sweet birthday or Christmas present for any proud dog owner.",
              "It’s the perfect gift for a birthday, Christmas or a ‘gotcha day’ celebration.",
              "It’s a cheerful gift for birthdays, Christmas or a thank-you to a dog walker or groomer."]

WHO = {  # gift-for bullet
 'sport': "An easy gift for team-mates, coaches, club members and anyone who lives in sports kit",
 'hobby': "An easy gift for friends, family or colleagues who share the same passion",
 'food': "A great Secret Santa or stocking filler for the foodie in your life",
 'drink': "A great Secret Santa or stocking filler for anyone who loves a drink",
 'animal': "An easy gift for animal lovers, pet owners and nature fans",
 'music': "A great gift for music fans, gig-goers and playlist kings and queens",
 'place': "A great gift for travellers, expats and proud patriots",
 'relation': "A thoughtful gift that says what you mean without needing a card",
 'faith': "A thoughtful gift for friends and family of faith",
 'trait': "A fun gift for friends, family and colleagues with a sense of humour",
 'type': "A cheeky gift for friends with a shared sense of humour",
 'cheeky': "A cheeky gift for mates with a shared sense of humour",
 'rude': "Adult humour only – one for friends who’ll laugh, not for your nan",
 'dating': "A fun gift for single friends and online daters",
 'datingrude': "Adult humour only – one for friends who’ll laugh",
 'brand': "A fun gift for fans, collectors and enthusiasts",
 'brandsport': "An easy gift for gym buddies, coaches and fitness fans",
 'celeb': "A great gift for fans of every age (well, every grown-up age)",
 'superfan': "A great gift for fans, gig-goers and record collectors",
 'dog': "An easy gift for dog walkers, groomers, breeders and proud dog owners",
}
H2 = {
 'sport': "a gift for {noun} fans", 'hobby': "a fun gift idea", 'food': "a gift for {noun} lovers", 'drink': "a gift for {noun} lovers",
 'animal': "a gift for animal lovers", 'music': "a gift for music lovers", 'place': "a gift for travellers and proud fans",
 'relation': "a gift from the heart", 'faith': "a thoughtful gift", 'trait': "a funny gift idea", 'type': "a cheeky gift idea",
 'cheeky': "a cheeky gift idea", 'rude': "a rude gift for grown-ups", 'dating': "a gift for online daters", 'datingrude': "a rude gift for grown-ups",
 'brand': "a gift for fans", 'brandsport': "a gift for fitness fans", 'celeb': "a gift for fans", 'superfan': "a gift for true fans",
 'dog': "a gift for every {parent}",
}
CLOSE = {
 'sport': ["Looking for more sports gifts? Browse our other This Girl and This Guy mugs – there’s one for nearly every sport.",
           "Pair it with a matching mug for a team-mate, or browse our other This Girl and This Guy mugs for the whole squad.",
           "Want a matching pair? We make This Girl and This Guy versions of lots of sports mugs."],
 'default': ["Looking for more funny slogan mugs? Browse our other This Girl and This Guy mugs to find one for everyone.",
             "Want a matching pair? Have a look through our This Girl and This Guy mugs – there’s one for nearly everybody.",
             "Pair it with a matching mug for a friend, or browse our full This Girl and This Guy range."],
 'dog': ["Got more than one dog lover in the house? We make This Girl and This Guy versions for dozens of breeds.",
         "Pair it with the matching This Guy or This Girl version so the whole family is covered.",
         "Looking for more dog lover gifts? Browse our other breed mugs – we cover dozens of breeds.",
         "Want a matching pair? Order the This Girl and This Guy versions together for a couple who share a dog.",
         "Treat the whole household: browse our other dog lover mugs to find every breed in the family."],
 'superfan': ["Got a fan couple? We make This Girl and This Guy versions of every superfan mug.",
              "Pair it with a gig ticket or a vinyl record for a birthday they won’t forget.",
              "Looking for more music gifts? Browse our other superfan mugs."],
 'rude': ["Looking for more rude gifts? Browse our other This Girl and This Guy mugs – some are cheeky, some are downright filthy.",
          "Pair it with a rude birthday card from our range for the full laugh-out-loud gift.",
          "Want more adult humour? Our This Girl and This Guy range has plenty more where this came from."],
}
CLOSE['datingrude'] = CLOSE['rude']
CLOSE['brandsport'] = CLOSE['sport']; CLOSE['celeb'] = CLOSE['superfan']
FAV = {  # topic bullet
 'sport': "Big, bold slogan that {noun} fans will spot straight away",
 'food': "Bold slogan that tells everyone exactly where {her} priorities lie",
 'drink': "The ideal mug for {her} favourite drink – the slogan says it all",
 'dog': "Bold slogan that shows off {her} love for {her} {name}",
 'superfan': "Bold slogan that tells the world exactly who {she} has on repeat",
 'rude': "A rude slogan that’s guaranteed to get a reaction in the staff room",
 'datingrude': "A cheeky slogan that’s guaranteed to get a reaction",
}

def opening(d, h):
    G_ = G[d['g']]
    kw = d['kw']
    cat = d['cat']
    if cat == 'dog':
        opts = [f"Our {kw} mug is made for the proud {G_['parent']} whose {d['name']} – {d['trait']} – is the best dog in the world.",
                f"The {kw} mug is for the {G_['girl']} who’d happily tell anyone about {G_['her']} {d['name']}, {d['trait']}.",
                f"If you know a {G_['parent']} who adores {G_['her']} {d['name']}, {d['trait']}, our {kw} mug is the one to get.",
                f"Our {kw} mug celebrates the {d['name']} – {d['trait']} – and the {G_['girl']} who loves it more than anything.",
                f"Every {d['name']} owner deserves a {kw} mug: a bold, happy way for a proud {G_['parent']} to show off {G_['her']} best friend."]
        return opts[h % 5]
    if cat == 'superfan':
        opts = [f"Our {kw} mug is made for the {G_['girl']} who knows every word, owns every album and would queue all night for {d['name']}, {d['desc']}.",
                f"The {kw} mug is for the {G_['girl']} who has {d['name']} – {d['desc']} – on repeat at home, in the car and at work.",
                f"If you know a {G_['girl']} who can’t get enough of {d['name']}, {d['desc']}, our {kw} mug says it loud and proud."]
        return opts[h % 3]
    line = d['line'].format(**G_)
    if cat in ('rude', 'datingrude'):
        opts = [f"Our {kw} mug is a rude, cheeky gift for the {G_['girl']} who {line}.",
                f"The {kw} mug is for the {G_['girl']} who {line} – and the friends who love {G_['him']} for it.",
                f"Got a {G_['pal']} who {line}? The {kw} mug was made with {G_['who']} in mind."]
        return opts[h % 3]
    opts = [f"Our {kw} mug is made for the {G_['girl']} who {line}.",
            f"The {kw} mug is for the {G_['girl']} in your life who {line}.",
            f"If you know a {G_['girl']} who {line}, our {kw} mug was made with {G_['who']} in mind."]
    return opts[h % 3]

def describe(d, colour, k=0, handle=''):
    h = int(hashlib.md5(handle.encode()).hexdigest(), 16) + k
    if d['cat'] == 'dog' and 'gi' in d:
        h = d['gi'] + k
    G_ = G[d['g']]
    kw = d['kw']; cat = d['cat']
    n = d.get('noun', '')
    NM = {'The Gym': 'gym', 'Playing Football': 'football', 'Playing Hockey': 'hockey', 'BMXing': 'BMX', 'CrossFit': 'CrossFit', 'Padel': 'padel',
          'Eat': 'food', 'Drink': 'drink', 'Dinner': 'dinner', 'Food': 'food', 'Sports': 'sports', 'To Golf': 'golf'}
    n = NM.get(n, n if re.search(r'[A-Z].*[A-Z]', n) and ' ' not in n else n.lower())
    fmt = dict(G_, noun=n, name=d.get('name', ''))
    white = 'white ' if colour == 'white' else ''
    occ = pick(OCC[cat], h, 1)
    p1 = f"<p>{opening(d, h)} {occ}</p>"
    h2 = f"<h2>{kw} mug – {H2[cat].format(**fmt)}</h2>"
    body = pick([
        f"The {kw} slogan is printed onto a glossy {white}11oz ceramic mug in our UK workshop. It’s a ready-made design, so there’s nothing to fill in – just add it to your basket and we’ll print it to order.",
        f"We print the {kw} design onto a high-gloss {white}11oz ceramic mug in our own UK workshop. It’s a ready-made design with nothing to fill in – pop it in your basket and we’ll do the rest.",
        f"This is a ready-made design, so there’s no personalisation to add. We print the {kw} slogan onto a glossy {white}11oz ceramic mug in our UK workshop, made to order for you.",
    ], h, 2)
    fav = FAV.get(cat, "Bold, easy-to-read slogan that says it all")
    bullets = [fav.format(**fmt),
               "Classic 11oz ceramic mug with a C-handle – the right size for a proper brew",
               "Sublimation printed in our own UK workshop",
               "Safe in the dishwasher and microwave",
               WHO[cat]]
    if (h // 7) % 2:
        bullets[1], bullets[2] = bullets[2], bullets[1]
    ul = "<ul>\n" + "\n".join(f"<li>{b}</li>" for b in bullets) + "\n</ul>"
    details = ("<ul>\n<li>Size: 11oz (approx. 325ml) ceramic mug with a C-handle</li>\n<li>Finish: high-gloss</li>\n"
               "<li>Print: sublimation, printed in our UK workshop</li>\n<li>Care: dishwasher and microwave safe – avoid abrasive scourers</li>\n"
               "<li>Packaging: protective packaging for UK delivery</li>\n</ul>")
    close = pick(CLOSE.get(cat, CLOSE['default']), h, 3)
    # keyword once more lower down
    close = close.replace('This Girl and This Guy mugs', 'This Girl and This Guy mugs', 1)
    third = f"<p>A {kw} mug is a small gift that gets used every single day.</p>" if pick([0, 1], h, 4) == 0 else f"<p>Whoever gets it, a {kw} mug will make their morning brew a little brighter.</p>"
    if cat in ('rude', 'datingrude'):
        third = f"<p>Just so you know: the {kw} mug carries adult language, so it’s best kept for grown-ups.</p>"
    html = (f"{p1}\n{h2}\n<p>{body}</p>\n<h3>Why you’ll love it</h3>\n{ul}\n<h3>Size &amp; details</h3>\n{details}\n"
            f"<h3>Delivery</h3>\n<p>Each mug is printed to order. Postage options and costs are shown at checkout.</p>\n<p>{close}</p>")
    if words(html) + words(third) <= 250:
        html = html.replace(f"\n<p>{close}</p>", f"\n{third}\n<p>{close}</p>")
    disc = None
    if cat in ('superfan', 'celeb'):
        a = d['artist']
        disc = f"This is an unofficial fan design. It is not endorsed by, or connected with, {a}, their management or record label. All names and trademarks belong to their respective owners."
    elif d.get('brand'):
        owner, mark = d['brand']
        if owner == mark:
            disc = f"This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {owner}. {mark} is a trademark of its owner and is used only to describe the design theme."
        else:
            pl = ' and ' in mark
            disc = f"This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {owner}. {mark} {'are trademarks' if pl else 'is a trademark'} of {'their' if pl else 'its'} owner and {'are' if pl else 'is'} used only to describe the design theme."
    if disc:
        html += f"\n<h3>Please note</h3>\n<p class=\"disclaimer\">{disc}</p>"
    return html, bool(disc)

def words(html):
    return len(re.sub(r'<[^>]+>', ' ', html).split())

def build(sel):
    out = {}; seen = set(); skipped = []
    empty = lambda x: not re.sub(r'<[^>]+>|\s|&nbsp;', '', x or '')
    norm = lambda x: re.sub(r'\s+', ' ', x or '').strip()
    dc = collections.Counter(norm(p['descriptionHtml']) for p in sel if not empty(p['descriptionHtml']))
    groups = collections.defaultdict(int)
    for p in sel:
        d = classify(p)
        if d is None:
            continue
        colour = col_from(p)
        need = p['status'] == 'ACTIVE' and (empty(p['descriptionHtml']) or dc[norm(p['descriptionHtml'])] > 1)
        if d['cat'] == 'dog':
            key = (d['g'], d['name']); d['gi'] = groups[key]; groups[key] += 1
        rec = dict(id=p['id'], handle=p['handle'], title=p['title'], cls=d, colour=colour, need_desc=need)
        if d['cat'] == 'skip':
            rec['skip'] = d['reason']; out[p['id']] = rec
            if need: skipped.append(rec)
            continue
        if need:
            k = 0
            while True:
                html, tp = describe(d, colour, k, p['handle'])
                if html not in seen: break
                k += 1
            seen.add(html); rec['html'] = html; rec['words'] = words(html.split('<h3>Please note')[0])
        rec['third_party'] = d['cat'] in ('superfan', 'celeb') or bool(d.get('brand'))
        out[p['id']] = rec
    return out, skipped

if __name__ == '__main__':
    sel = json.load(open('sel.json'))
    out, skipped = build(sel)
    json.dump(out, open('plan.json', 'w'), ensure_ascii=False, indent=0)
    w = [r['words'] for r in out.values() if 'html' in r]
    print('descs', len(w), 'min', min(w), 'max', max(w), 'skipped', len(skipped))
    print(collections.Counter(r['cls']['cat'] for r in out.values() if 'html' in r))
