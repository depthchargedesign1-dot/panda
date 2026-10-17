"""SEO descriptions, SEO titles and meta descriptions for celebrity card face masks.

Facts come only from the "Face masks" sheet in plan/product-facts.md. Each listing gets its own copy:
the star's name, their category (sport, music, TV ...) and phrasing picked per product from several
variants, so no two listings read the same. The celebrity disclaimer (CLAUDE.md) is the last block.

Usage: python3 tools/mask_copy.py <shopify_masks.jsonl> <out_dir>
"""
import csv
import hashlib
import html
import json
import re
import sys
from collections import defaultdict

CUT = re.compile(
    r"\s+(?:-|–|\||\(|JB\b|MH\b|NEW\b|New\b|OK\b|Celebrity\b|Celebrities\b|Face\s*Mask|Facemask|Fancy\s+Dress|Cardboard|"
    r"Party\b|Mask\b|Actor\b|Actress\b|Footballer|Football\b|Golfer|Tennis\b|Boxer|Boxing\b|Darts?\b|Cricket|Rugby|Snooker|F1\b|"
    r"Formula|GOLF\b|STARS?\b|SPORTS?\b|Sports?\b|TV\b|Movie|Film\b|Music|Singer|Rapper|Comedian|Funny|Love\s+Island|Lionesses?|Grey\b|"
    r"20\d\d\b|19\d\d\b|\d+\b)", re.I)
PACK = re.compile(r"\b(pack|\d+\s*x\b|couple|and\s+[A-Z][a-z]+\s+[A-Z])", re.I)
CUSTOM = re.compile(r"personalised|custom|your own|request", re.I)

CATS = [  # (key, test on tags+type+title, label, who it's for, occasions)
    ("football", r"footballer|football|lioness|euros|england 20|premier", "football star",
     "football fans", ["a big match watch party", "a five-a-side end-of-season do", "a stag do before the cup final", "a football-themed birthday"]),
    ("darts", r"dart", "darts star", "darts fans", ["a darts night down the pub", "the walk-on at a darts party", "an Ally Pally trip"]),
    ("golf", r"golf", "golfer", "golf fans", ["a golf society dinner", "a 19th-hole celebration", "a golf day fancy dress round"]),
    ("f1", r"\bf1\b|formula|driver", "Formula 1 driver", "motorsport fans", ["a race-day watch party", "a motorsport-themed birthday", "a trip to the Grand Prix"]),
    ("tennis", r"tennis", "tennis star", "tennis fans", ["a summer tennis party", "a strawberries-and-cream garden do", "a tennis club social"]),
    ("boxing", r"\bbox(er|ers|ing)\b", "boxer", "fight fans", ["a fight-night watch party", "a boxing-themed stag do", "a big-fight sweepstake night"]),
    ("cricket", r"cricket", "cricketer", "cricket fans", ["a cricket club dinner", "a Test match day out", "a summer cricket social"]),
    ("rugby", r"rugby", "rugby star", "rugby fans", ["a rugby club social", "a Six Nations watch party", "a rugby tour fancy dress day"]),
    ("snooker", r"snooker", "snooker star", "snooker fans", ["a snooker hall night out", "a cue-sports birthday", "a club tournament social"]),
    ("sport", r"sport|athlet|olymp|cycl|basketball|nfl|wrestl|ufc|mma", "sports star", "sports fans",
     ["a sports-themed birthday", "a big-game watch party", "a club awards night"]),
    ("royal", r"\broyal|politic|\bking\b|\bqueen\b|\bprince\b|\bprincess\b|prime minister|president", "public figure", "anyone who loves a laugh at the big names",
     ["a street party", "an election-night get-together", "a jubilee-style garden party"]),
    ("music", r"music|singer|rapper|band|pop\b|rock|x ?factor|eurovision|musician", "music star", "music fans",
     ["a concert pre-party", "a karaoke night", "a festival weekend", "a tribute-act birthday"]),
    ("comedy", r"comed|funny", "comedian", "comedy fans", ["a comedy night", "a birthday roast", "a stag or hen do"]),
    ("reality", r"love island|towie|only way|geordie|made in chelsea|real housewives|i'?m a celebrity|strictly|bake off", "reality TV star",
     "reality TV fans", ["a finale watch party", "a girls' night in", "a hen do"]),
    ("film", r"movie|film|actor|actress|bollywood|bond|mcu|hollywood", "film star", "film fans", ["a movie night", "an Oscars-style party", "a themed birthday"]),
    ("tv", r"tv|soap|eastenders|coronation|emmerdale|hollyoaks|netflix|doctor who", "TV star", "TV fans", ["a series finale watch party", "a soap-themed birthday", "a telly-night quiz"]),
]
DEFAULT = ("celeb", "", "celebrity", "anyone planning a party", ["a birthday party", "a stag or hen do", "a wedding photo booth"])

SHOWS = [  # tag → name used in the disclaimer (third-party show)
    ("LOVE ISLAND", "Love Island"), ("EASTENDERS", "EastEnders"), ("CORONATION STREET", "Coronation Street"),
    ("EMMERDALE", "Emmerdale"), ("HOLLYOAKS", "Hollyoaks"), ("STRICTLY", "Strictly Come Dancing"), ("Towie", "The Only Way Is Essex"),
    ("Doctor Who", "Doctor Who"), ("Squid Game", "Squid Game"), ("Money Heist", "Money Heist"), ("Stranger Things", "Stranger Things"),
    ("The Walking Dead", "The Walking Dead"), ("James Bond", "James Bond"), ("Star Trek", "Star Trek"), ("Friends Face", "Friends"),
    ("Big Bang Theory", "The Big Bang Theory"), ("Only Fools", "Only Fools and Horses"), ("Gangs of London", "Gangs of London"),
    ("The Boys", "The Boys"), ("Still Game", "Still Game"), ("Made In Chelsea", "Made in Chelsea"), ("GEORDIE", "Geordie Shore"),
]


def pick(seq, key, salt):
    h = int(hashlib.md5((key + salt).encode()).hexdigest(), 16)
    return seq[h % len(seq)]


CLUBS = r"(Brighton|Bournemouth|Brentford|Fulham|Wolves|Wolverhampton|Crystal Palace|Nottingham Forest|Forest|Ipswich|Leicester|Southampton|Sunderland|Burnley|Sheffield|Real Madrid|Barcelona|Man(chester)? (Utd|United|City)|Liverpool|Chelsea|Arsenal|Tottenham|Spurs|Everton|Newcastle|Celtic|Rangers|Leeds|Aston Villa|West Ham|Juventus|PSG|Bayern|England|Scotland|Wales|Ireland|Lionesses)"
SHOW_WORDS = "|".join(re.escape(n) for _, n in SHOWS) + r"|Peaky Blinders|Umbrella Academy|Breaking Bad|Game of Thrones|The Crown|Big Bang Theory|Stranger Things|Walking Dead|Mad ?Men|Bollywood|I'?.?m A Celeb\w*|Black ?Adder|Hangover|Spider-Man|Iron Man|Mrs Browns? Boys|Dirty Dancing|Last Of Us|Footloose"


def clean_name(title):
    t = re.sub(r"\s+", " ", title).strip()
    t = re.split(r"\s+(?:" + CLUBS + "|" + SHOW_WORDS + r")\b", t, maxsplit=1, flags=re.I)[0]
    m = CUT.search(" " + t)
    name = (" " + t)[: m.start()].strip() if m else t
    name = re.sub(r"[^\w\s'.&-]", "", name).strip(" -–.")
    if name.isupper() or name.islower():
        name = " ".join(w.capitalize() if not re.match(r"^(Mc|Mac)", w, re.I) else w[:2].capitalize() + w[2:].capitalize() for w in name.split())
    words = name.split()
    noise = {"politician", "cycling", "c", "bond", "neighbour", "neighbours", "glasses", "old", "towie", "ofah", "bob", "golden",
             "globes", "acolyte", "bottom", "cartoon", "lf", "joker", "new", "mask", "masks", "royal", "prime", "minister", "president"}
    while len(words) > 1 and (words[-1].lower() in noise or (words[-1].isupper() and len(words[-1]) > 2 and words[-1] not in ("III", "II"))):
        words.pop()
    if words and words[0].lower() == "president" and len(words) > 1:
        words = words[1:]
    name = " ".join(words)
    name = re.sub(r"-(Eurovision|XFactor|X-Factor)$", "", name, flags=re.I)
    if len(words) == 1 and not re.search(r"football", title, re.I):
        words = []
    if len(words) == 1 and re.search(re.escape(name) + r"\s+(Celebrity|Face|Mask|Facemask|[A-Z]{3,})", title) is None:
        words = []  # a single word that isn't clearly a one-name star goes to manual review
    ok = 1 <= len(words) <= 3 and name.isascii() and not re.search(r"\b(DIY|Pup|Cut Out|Pose|Pack)\b", name, re.I) and all(re.match(r"^[A-Za-zÀ-ÿ'.&-]+$", w) for w in words) and len(name) >= 3
    return name, ok


def category(p):
    # The title is the most reliable source, then the product type, then tags (tags are noisy).
    generic = r"celebrity tv stars|actor movie tv celebrity|tv stars and celebrit\w*|\btv stars\b|fancy dress face mask|celebrity facemask"
    if re.search(r"\bTV STARS?\s+(20\d\d|Celebrity)", p["title"]):
        return next((c[0], c[2], c[3], c[4]) for c in CATS if c[0] == "tv")
    title = re.sub(generic, " ", p["title"], flags=re.I)
    ptype = re.sub(generic, " ", p.get("productType") or "", flags=re.I)
    tags = " ".join(t for t in p.get("tags", []) if not re.fullmatch(r"(?i)tv stars( stars)?|tv stars and celebrity masks|facebook|new-arrivals|new", t))
    for hay in (title, ptype, tags):
        for key, rx, label, who, occ in CATS:
            if re.search(rx, hay, re.I):
                return key, label, who, occ
    return DEFAULT[0], DEFAULT[2], DEFAULT[3], DEFAULT[4]


def show_of(p):
    hay = " ".join(p.get("tags", [])) + " " + p["title"]
    for tag, name in SHOWS:
        if tag.lower() in hay.lower():
            return name
    return None


IDENT_CAT = {  # identification categories (who/*.jsonl) -> mask_copy CATS keys
    "football": "football", "music": "music", "tv": "tv", "film": "film", "comedy": "comedy", "reality": "reality",
    "royal": "royal", "politics": "royal", "characters": "film", "models": "celeb", "other": "celeb",
}
SPORT_CAT = {"darts": "darts", "golf": "golf", "f1": "f1", "tennis": "tennis", "boxing": "boxing", "cricket": "cricket",
             "rugby": "rugby", "snooker": "snooker"}


def build(p, ident=None):
    """ident: optional identification record (name, character, show, category, sport, blurb) for this person."""
    if ident:
        name, ok = ident["name"], True
    else:
        name, ok = clean_name(p["title"])
    if not ok or (not ident and (PACK.search(p["title"]) or CUSTOM.search(p["title"]))):
        return None
    key = p["handle"]
    cat, label, who, occ = category(p)
    show = show_of(p)
    if ident:
        k = SPORT_CAT.get(ident.get("sport") or "", "sport") if ident.get("category") == "sport" else IDENT_CAT.get(ident.get("category"), "celeb")
        c = next((c for c in CATS if c[0] == k), None)
        cat, label, who, occ = (c[0], c[2], c[3], c[4]) if c else (DEFAULT[0], DEFAULT[2], DEFAULT[3], DEFAULT[4])
        show = ident.get("show") or show
    pk = f"{name} face mask"
    o1, o2 = pick(occ, key, "o1"), pick(occ[::-1], key, "o2")
    if o1 == o2:
        o2 = "a fancy dress night out"

    intro = pick([
        f"Our {pk} is a quick way to get everyone laughing, whether it's for {o1} or {o2}.",
        f"Bring a famous face to {o1} with this {pk}, printed on sturdy card and cut to shape.",
        f"Planning {o1}? This {pk} is the easy fancy dress win for {who}.",
        f"Turn heads at {o1} with a {pk} that's made for photos, laughs and a bit of mischief.",
    ], key, "intro")
    intro2 = pick([
        f"It's a firm favourite with {who}, and it travels flat in an envelope so it's easy to post as a gift.",
        "Hand a few out and watch the group photos fill up with the same famous face.",
        "Great for photo booths, surprise birthdays and anyone who loves a bit of fancy dress.",
        f"Pair it with a costume, or keep it simple and let the {label} face do the talking.",
    ], key, "intro2")
    h2 = pick([f"{name} Celebrity Face Mask", f"{name} Card Face Mask for Parties", f"{name} Fancy Dress Face Mask"], key, "h2")
    how = pick([
        f"Each {pk} is digitally printed in full colour on 350gsm silk card, cut to shape around the face, with pre-cut eye holes, plus elastic and sticky tabs so it takes seconds to put together.",
        f"We print this {label} mask in full colour on thick 350gsm silk card, cut it to the shape of the face and pre-cut the eye holes. Elastic and sticky tabs are included.",
        "Printed in full colour on 350gsm silk card and cut to shape, the mask comes with the eye holes already cut out, plus elastic and sticky tabs for a quick fit.",
    ], key, "how")
    custom = pick([
        "Want a mask of someone who isn't in our range, like the birthday boy or the bride-to-be? We can make one from your photo.",
        "Need a face we don't stock, such as the groom or a friend? Send us a photo and we'll make a custom mask.",
        "Can't find the face you need? We also make custom masks from your own photo.",
    ], key, "custom")
    bullets_pool = [
        "Thick 350gsm silk card holds its shape all night",
        "Semi-waterproof finish, so it copes with spilt drinks and outdoor parties",
        "Pre-cut eye holes, with elastic and sticky tabs included",
        "Full-colour digital print for a sharp, recognisable face",
        "Posted flat in a board-backed envelope to keep it crease-free",
        "Full A4 size (297 x 210 mm), so it covers an adult face",
        f"An easy, cheap way to theme {o1}",
        "Brilliant for photo booths and group shots",
    ]
    start = int(hashlib.md5((key + "b").encode()).hexdigest(), 16) % len(bullets_pool)
    bullets = [bullets_pool[(start + i) % len(bullets_pool)] for i in range(5)]
    close = pick([
        f"Order one for {o2}, or buy a few so the whole group can turn up as {name}.",
        f"A {pk} is a cheap and cheerful way to make {o2} one to remember.",
        f"Grab a {pk} for {o2} and get the camera ready.",
    ], key, "close")
    if show:
        disc = (f"This is an unofficial novelty product made for fun and fancy dress. {name} has not endorsed, sponsored or approved this product, "
                f"and Foxy Printing has no connection with them or with {show}, its producers or broadcasters. The names are used only to describe the design.")
    else:
        disc = (f"This is an unofficial novelty product made for fun and fancy dress. {name} has not endorsed, sponsored or approved this product, "
                f"and Foxy Printing has no connection with them. The name is used only to describe the design.")
    e = lambda x: html.escape(x, quote=False)
    body = (
        f"<p>{e(ident['blurb']) if ident and ident.get('blurb') else e(intro) + ' ' + e(intro2)}</p>\n<h2>{e(h2)}</h2>\n<p>{e(how)} {e(custom)}</p>\n"
        f"<h3>Why you'll love it</h3>\n<ul>\n" + "".join(f"<li>{e(b)}</li>\n" for b in bullets) + "</ul>\n"
        f"<h3>Size &amp; details</h3>\n<ul>\n<li>Size: 297 x 210 mm (A4), a full adult-size face</li>\n<li>Material: 350gsm silk card, full-colour digital print</li>\n"
        f"<li>Finish: semi-waterproof</li>\n<li>Fit: one size for adults; elastic and sticky tabs included</li>\n"
        f"<li>Pre-cut eye holes; cut to the shape of the face</li>\n<li>Packaging: board-backed envelope</li>\n</ul>\n"
        f"<h3>Delivery</h3>\n<p>Printed in our UK workshop and posted to you. Dispatch and postage options are shown at checkout.</p>\n"
        f"<p>{e(close)}</p>\n<h3>Please note</h3>\n<p class=\"disclaimer\">{e(disc)}</p>"
    )
    seo_title = f"{name} Face Mask | Foxy Printing"
    if len(seo_title) > 60:
        seo_title = f"{name} Face Mask"[:60]
    meta = pick([
        f"{name} card face mask for {o1}. Printed on 350gsm silk card cut to shape with eye holes and elastic. Order yours today.",
        f"Fancy dress made easy: a {name} face mask on thick card with eye holes and elastic. Perfect for {o1} and photo booths.",
        f"Get the party started with a {name} face mask. Full-colour print on 350gsm card, cut to shape with elastic. Great for {o1}.",
    ], key, "meta")
    for filler in [" Posted in a board-backed envelope.", " Quick UK delivery.", " Ideal for groups.", " Fun for all."]:
        if len(meta) >= 140:
            break
        meta += filler
    if len(meta) > 155:
        meta = meta[:152].rsplit(" ", 1)[0].rstrip(".,") + "."
    for filler in [" Order today.", " UK made.", " Fun!"]:
        if len(meta) >= 140:
            break
        if len(meta + filler) <= 155:
            meta += filler
    return dict(name=name, category=cat, show=show, body=body, seo_title=seo_title, meta=meta)


def main(src, out):
    P, M = {}, defaultdict(list)
    for line in open(src):
        o = json.loads(line)
        (M[o["__parentId"]].append(o) if "__parentId" in o else P.__setitem__(o["id"], o))
    done, skipped = [], []
    for p in P.values():
        if re.search(r"face covering", p["title"], re.I):
            continue
        r = build(p)
        (done if r else skipped).append((p, r))
    words = [len(re.sub(r"<[^>]+>", " ", r["body"]).split()) for p, r in done]
    print(f"written {len(done)}, skipped for manual review {len(skipped)}; words {min(words)}-{max(words)}")
    # Single-variant products go through CSV import; multi-variant ones through the API (safer for variants).
    single = [(p, r) for p, r in done if p.get("totalVariants", 1) == 1]
    multi = [(p, r) for p, r in done if p.get("totalVariants", 1) != 1]
    cols = ["Handle", "Body (HTML)", "SEO Title", "SEO Description"]
    for n, i in enumerate(range(0, len(single), 3500)):
        with open(f"{out}/masks-{n + 1:02d}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(cols)
            for p, r in single[i:i + 3500]:
                w.writerow([p["handle"], r["body"], r["seo_title"], r["meta"]])
    with open(f"{out}/masks-00-TEST.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(cols)
        for p, r in single[:3]:
            w.writerow([p["handle"], r["body"], r["seo_title"], r["meta"]])
    json.dump([{"id": p["id"], "descriptionHtml": r["body"], "seo": {"title": r["seo_title"], "description": r["meta"]}} for p, r in multi],
              open(f"{out}/masks-api-multivariant.json", "w"), ensure_ascii=False)
    with open(f"{out}/masks-manual-review.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Handle", "Title", "Why"])
        for p, _ in skipped:
            w.writerow([p["handle"], p["title"], "pack / custom / name unclear"])
    with open(f"{out}/masks-preview.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Handle", "Old title", "Name used", "Category", "Show", "SEO Title", "SEO Description"])
        for p, r in done:
            w.writerow([p["handle"], p["title"], r["name"], r["category"], r["show"] or "", r["seo_title"], r["meta"]])
    print(f"csv rows {len(single)}, api {len(multi)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
