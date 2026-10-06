"""Write unique, fact-checked descriptions for every Foxy Printing mug with an empty or poor description (6 Oct 2026).

Usage: python3 tools/mug_copy.py <bulk_export.jsonl> <out_dir> [queued_seo_csv ...]
The export holds products (id handle title status vendor productType tags descriptionHtml seo options featuredMedia),
their variants (title sku) and their mm-google-shopping metafields.

Facts come only from the "Mugs (11oz ceramic, sublimation)" sheet in plan/product-facts.md.
Rude designs are described without spelling out swear words. Third-party names get the CLAUDE.md disclaimers.
"""
import csv, html, json, os, random, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mug_copy_names import *          # noqa: F401,F403  (tables, censor, disclaimers)
from age_group import age_group

GPC = "Home & Garden > Kitchen & Dining > Tableware > Drinkware > Mugs"
ALLMUGS_TYPES = {"keep calm support", "championship football team", "league one football team", "league two football team",
                 "national league south", "national league north", "international football team",
                 "premier league football team", "scottish football teams"}
# Not the standard 11oz ceramic sublimation mug, or a service: the mug fact sheet doesn't cover them, so no copy written here.
NON_STANDARD_TYPES = {"Travel Mugs", "Enamel Mugs", "Latte Mugs", "Magic Mugs", "Kids Cups", "Glass Can Cups & Tumblers",
                      "Gift Boxes & Letterbox Gifts", "Coasters", "Celebrity Facemask", "Homeware"}

# ------------------------------------------------------------------------------------------------ loading
def load(path):
    prods, order = {}, []
    for line in open(path):
        o = json.loads(line)
        pid = o.get("__parentId")
        if pid:
            if "key" in o:
                prods[pid]["mf"][o["key"]] = o["value"]
            else:
                prods[pid]["variants"].append(o)
        else:
            o["variants"], o["mf"] = [], {}
            prods[o["id"]] = o
            order.append(o["id"])
    return [prods[i] for i in order]

def text(h):
    t = re.sub(r"<[^>]+>", " ", h or "")
    return re.sub(r"\s+", " ", html.unescape(t)).strip()

def in_allmugs(p):
    t, ty = p["title"].lower().strip(), (p["productType"] or "").lower()
    return ("mug" in ty or t.endswith("mug") or "mug –" in t or "mug -" in t or "mug design" in t or ty in ALLMUGS_TYPES)

def is_mug(p):
    return in_allmugs(p) or bool(re.search(r"\bmugs?\b", p["title"], re.I))

def excluded(p):
    return (p["productType"] == "This Guy / This Girl Mugs" or p["title"].lower().startswith(("this girl", "this guy"))
            or p["handle"].startswith(("rude-number-plate-mug-", "funny-number-plate-mug-")))

def poor_reasons(p, dupcount):
    h = p["descriptionHtml"] or ""
    t = text(h)
    if len(t) < 40:
        return ["empty"]
    r = []
    if len(t.split()) < 120:
        r.append("under 120 words")
    if re.search(r"style=|<font|<center|<img|<span[^>]*font|Bottles ordered", h, re.I):
        r.append("old eBay-style HTML")
    letters = [c for c in t if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.6:
        r.append("ALL CAPS")
    if dupcount[t] > 1:
        r.append(f"same text as {dupcount[t] - 1} other product(s)")
    if re.search(r"(\b[\w ]{2,25},){8,}", t) or t.count("#") > 5 or re.search(r"( - [\w' ]{2,30}){4,}", t):
        r.append("keyword list")
    return r

# ------------------------------------------------------------------------------------------------ classification
TRAIL = [r"Personalised ADULT OFFICE MUG", r"FUNNY OCCUPATION RUDE ADULT OFFICE MUG", r"ADULT OFFICE MUG", r"OFFICE MUG",
         r"Funny Mug Adult Mug Office Mug", r"Mug Adult Mug Office Mug", r"Adult Mug Office Mug", r"Mug Adult Mug Gift",
         r"Adult Mug Gift", r"Mug Rude Mug", r"Rude Adult Mug", r"Personalised Adult Mug", r"Adult Mug",
         r"Printed Gift Mug Office Funny", r"Printed Mug Office Funny", r"Novelty Funny Printed Mug", r"Novelty Funny Mug",
         r"Joke Gift Printed Novelty Mug", r"Novelty Printed Mug", r"Printed Mug", r"FUNNY MUG", r"FUNNY", r"Celebrity Mug",
         r"Gift Office Mug", r"Office Mug", r"Mug", r"KE", r"PERSONALISED", r"Personalised"]

def strip_filler(t):
    s = re.sub(r"\s*Mug Adult Mug Office Mug\s*", " Mug ", t)
    s = re.sub(r"\(\s*", "(", s)
    changed = True
    while changed:
        changed = False
        for f in TRAIL:
            n = re.sub(r"[\s\-–—]*\b" + f + r"\s*$", "", s, flags=re.I)
            if n != s:
                s, changed = n, True
    s = re.sub(r"\(\s*\)", "", s)
    return nice(re.sub(r"\s+", " ", s).strip(" -–—:,"))

def mug_colour(p):
    """Colour facts that come from the product's own title or options."""
    t = p["title"]
    opts = [o for o in p["options"] if o["name"].lower() != "title"]
    choice = None
    for o in opts:
        if re.search(r"colou?r", o["name"], re.I):
            choice = (o["name"], o["values"])
    m = re.match(r"(RED|BLACK) MUG - ", t)
    if m:
        return {"body": f"{m.group(1).lower()} mug", "white": False, "choice": choice}
    if re.search(r"black handle", t, re.I):
        return {"body": "black handle", "white": "(White)" in t, "choice": choice}
    if choice:
        vals = " ".join(choice[1]).lower()
        return {"body": None, "white": "white" in vals, "choice": choice}
    return {"body": None, "white": True, "choice": None}

NAME_FIX = {"acdc": "AC/DC", "boyz ii men": "Boyz II Men", "dnce": "DNCE", "dayay": "Daya", "a$ap rocky": "A$AP Rocky",
            "blink 182": "blink-182", "dj khaled": "DJ Khaled", "g eazy": "G-Eazy", "leonardo dicaprio": "Leonardo DiCaprio",
            "~troye sivan": "Troye Sivan", "tommy lee jones]": "Tommy Lee Jones", "jack nicholson2": "Jack Nicholson",
            "adrien brody i love": "Adrien Brody", "michael keaton i love": "Michael Keaton", "danny devito": "Danny DeVito",
            "emily vancamp": "Emily VanCamp"}

def fix_name(n):
    n = NAME_FIX.get(n.lower(), n)
    return re.sub(r"\bMc([a-z])", lambda m: "Mc" + m.group(1).upper(), n)

CARTOON_FIX = {"Radfahrer": "Cycling", "Schwimmer": "Swimming", "Verliebt": "Lovestruck", "Zauberer": "Wizard",
               "Hawian": "Hawaiian", "Pharao": "Pharaoh", "Beac ": "Beach ", "Balet": "Ballet", "Gardner": "Gardener",
               "Pillot": "Pilot", "Astronaught": "Astronaut", " MUG": "", "Babel Patz": "Babel Patz"}

def classify(p):
    t, ty, tags = p["title"], p["productType"] or "", set(p["tags"])
    tl = t.lower()
    c = {"fam": "generic", "subject": strip_filler(t), "personal": None, "rude": False, "disc": [], "tpnames": [],
         "colour": mug_colour(p)}
    tp = lambda kind, names, text_: (c["disc"].append(text_), c["tpnames"].extend(names))

    if ty == "Valentines Cards" or "ADULT MUGS (RUDE)" in tags or "Swear Word Mugs" in tags \
            or re.search(r"\brude\b", tl) or SWEARY.search(t):
        c["rude"] = True

    m = re.match(r"(?:(RED|BLACK) MUG - )?(The Future (Mr\.?|Mrs\.?)|This Guy loves) (.+?) mug - Celebrity Mug$", t, re.I)
    if m and ty == "Celebrity Mugs":
        name = nice(m.group(4))
        kind = "mr" if m.group(3) and m.group(3).lower().startswith("mr.") or (m.group(3) or "").lower() == "mr" else \
               ("mrs" if m.group(3) else "loves")
        c.update(fam="celeb_future", subject=name, kind=kind)
        tp("celeb", [name], d_celeb(name))
        return c
    m = re.match(r"(?:(RED|BLACK) MUG - )?(My Future Husband|My Lover Bought Me This|The Furture Mrs|The Future Mrs?\.?) (.+?) (?:Mug )?(?:Celebrity Face|- Celebrity Gift)", t)
    if m and ty == "Celebrity Mugs":
        name = nice(m.group(3).strip())
        lead = {"The Furture Mrs": "The Future Mrs"}.get(m.group(2), m.group(2))
        c.update(fam="celeb_other", subject=name, lead=lead)
        tp("celeb", [name], d_celeb(name))
        return c
    if ty == "Celebrity Mugs" and t.startswith("I Love FUTURE"):
        c.update(fam="celeb_ilove", subject="Future", band=True)
        tp("band", ["Future"], d_band("Future"))
        return c
    m = re.match(r"I Love (.+?)(?: Mug)?(?: - I Love Celebrity Mug.*| Celebrity Mug.*| Mug.*| - Novelty.*)?$", t)
    if ty in ("Celebrity Mug", "I Love Heart Mugs") and m:
        name = fix_name(nice(m.group(1)).strip())
        key = name.lower()
        if key in ("4x4",):
            c.update(fam="ilove", subject="4x4s")
            return c
        band = ILOVE_BANDS.get(key) or (name if tags & {"Top 100 Bands Of All Time", "Top 100 Music ArtistsBands"} else None)
        c.update(fam="celeb_ilove", subject=ILOVE_BANDS.get(key, name), band=bool(band))
        if band:
            tp("band", [band], d_band(band))
        else:
            tp("celeb", [name], d_celeb(name))
        return c
    m = re.match(r"Worlds Best (.+?)(?: Mug)? - (Novelty Funny Mug|Funny Rude Ceramic Mug Gift)", t)
    if m:
        c.update(fam="occ_rude" if "Rude" in t else "occ", subject=nice(m.group(1)))
        return c
    m = re.match(r"Awesome (.+?) (Printed )?Office Mug", t)
    if m:
        c.update(fam="awesome", subject=nice(m.group(1)))
        return c
    m = re.match(r"I'?M ?A?N? (.+?) TO SAVE TIME LETS JUST (ASSUME|SAY) IM ALWAYS RIGHT", t, re.I)
    if m:
        role = nice(m.group(1)).replace("Cricketl", "Cricket").replace("Balll", "Ball").replace("balll", "ball")
        role = re.sub(r"^(A|An) ", "", role)
        if not re.search(r"coach|teacher|instructor|designer|welder", role, re.I):
            role += " Coach"
        c.update(fam="always_right", subject=role)
        return c
    m = re.match(r"I'?d Rather Be (DRINKING )?(A PINT OF )?(.+?) (Mug )?Personalised", t, re.I)
    if m:
        what = re.sub(r"\s+Mug$", "", m.group(3)).strip()
        drinking = bool(m.group(1) or m.group(2))
        key = what.lower()
        brands = []
        if key not in DRINK_GENERIC:
            if drinking or key in {"amigos", "asahi", "badger fursty", "bavaria", "bishops finger", "black sheep",
                                   "blue moon", "brahma", "cobra", "crabbies", "dg dragon", "modelo", "spitfire", "tiger",
                                   "dark n stormy"}:
                parts = re.split(r"\s*&\s*", key)
                if len(parts) == 2 and parts[1] in MIXER_BRANDS:
                    brands = [MIXER_BRANDS.get(parts[0])] if parts[0] in MIXER_BRANDS else []
                    brands.append(MIXER_BRANDS[parts[1]])
                elif key in DRINK_GENERIC:
                    brands = []
                else:
                    brands = [DRINK_FIX.get(key, nice(what) if what.isupper() else what)]
        brands = [b for b in brands if b]
        c.update(fam="rather", subject=nice(what) if what.isupper() else what, drinking=drinking,
                 pint=bool(m.group(2)), personal="name")
        if re.search(r"\bslut\b|nipples|panty", key):
            c["rude"] = True
        if brands:
            tp("brand", brands, d_brand(brands))
        return c
    m = re.match(r"Best (.+?) ?Teacher (Male|FEMALE)", t, re.I) or re.match(r"Personalised Your CUSTOM Name Best (.+?) Teacher", t)
    if m:
        subj = nice(m.group(1)).replace("P.Eteacher", "P.E").replace("Phycology", "Psychology").replace("PHYCOLOGY", "Psychology")
        subj = re.sub(r"(?i)phycology", "Psychology", subj).replace("Copy", "").strip()
        subj = {"R.e": "RE", "P.e": "PE", "R.E": "RE", "P.E": "PE"}.get(subj, subj)
        c.update(fam="teacher", subject=subj, gender=(m.group(2).lower() if m.lastindex and m.lastindex > 1 else None),
                 personal="name" if "Personalised" in t else None)
        return c
    m = re.match(r"Personalised Your CUSTOM Name (.+?) Printed Mug", t)
    if m:
        c.update(fam="name", subject=nice(m.group(1)).strip("[]~ "), personal="name",
                 rude=bool(re.search(r"(?i)cunt|prick|slag|slut|tits|\bmilf\b|dickhead|twat|wanker|bitch|\bass\b", m.group(1))))
        return c
    m = re.match(r"This Is My Birthday Mug - My Birthday Is On ?(.*?)(?: - |$)", t)
    if m:
        c.update(fam="bday_date", subject=m.group(1).strip() or None)
        return c
    m = re.match(r"Manufactured In (\d{4})", t)
    if m:
        c.update(fam="bday_year", subject=m.group(1))
        return c
    if ty == "Personalised Cartoon Animals Mugs":
        s = re.sub(r"^Personalised (Cartoon )?(Funny )?", "", t)
        s = re.sub(r"\s*Mug.*$", "", s)
        for a, b in CARTOON_FIX.items():
            s = s.replace(a, b)
        s = re.sub(r"([a-z])(\d)$", r"\1 \2", s.strip())
        c.update(fam="cartoon", subject=s, personal="name")
        if re.search(r"Darth Vader|Storm Trooper", s):
            tp("character", ["Star Wars"], d_character("Star Wars", "Lucasfilm"))
        if "Tweety" in s:
            tp("character", ["Looney Tunes (Tweety)"], d_character("Looney Tunes", "Warner Bros."))
        return c
    # football
    club, league = None, None
    for pat in (r"Crazy (.+?) Fan Football Crazy", r"Keep Calm And Support (.+?) Mug", r"Personalised SIGNS FOR (.+?) Football",
                r"^(.+?) (?:INSPIRED )?Football Team Mug", r"^Personalised (.+?) Football Birthday Mug"):
        m = re.search(pat, t, re.I)
        if m:
            club = m.group(1).strip()
            break
    if club:
        leagues = {"Premier league Football Team": "the Premier League", "Championship Football team": "the English Football League",
                   "League One Football Team": "the English Football League", "League Two Football Team": "the English Football League",
                   "National League South": "the National League", "National League North": "the National League",
                   "Scottish Football Team Mugs": "the Scottish Professional Football League",
                   "Scottish Football Teams": "the Scottish Professional Football League"}
        sub = "crazy" if "Crazy" in t else "keepcalm" if "Keep Calm" in t else "signs" if "SIGNS FOR" in t else "team"
        intl = ty == "International Football Team"
        c.update(fam="football", subject=club, sub=sub, intl=intl,
                 personal="name and age" if sub in ("signs", "team") else None)
        if intl:
            tp("club", [club], d_club(f"the {club} national team, its football association,"))
        else:
            tp("club", [club], d_club(club, leagues.get(ty)))
        return c
    if ty == "Coffee Mug" and "Club Logo" in t:
        c.update(fam="dad_club", subject="World's Best Dad", personal="name, message and club badge photo")
        tp("club", [], d_club(None))
        return c
    if ty == "Motor Mugs":
        m = re.match(r"(.+?) Personalised Printed Mug", t)
        base = re.sub(r"([A-Za-z])(\d)", r"\1 \2", (m.group(1) if m else t).strip())
        key = re.sub(r"\s*\d+$", "", base).lower()
        if base.lower().startswith("personalised your custom name"):
            c.update(fam="name", subject=nice(re.sub(r"(?i)personalised your custom name|printed mug", "", t)), personal="name")
            return c
        brand = MOTOR.get(key)
        num = re.search(r"\s(\d+)$", base)
        c.update(fam="motor", subject=re.sub(r"\s\d+$", "", base), num=num.group(1) if num else None, personal="name")
        if brand:
            tp("brand", [brand], d_brand([brand]))
        else:
            c["disc"].append("This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by "
                             "any vehicle or parts maker. Any make, model or badge in the design is a trademark of its owner "
                             "and is used only to describe the design theme.")
            c["tpnames"].append(f"{base} (vehicle badge)")
        return c
    m = re.match(r"I Love My (.+?) (Printed Mug|Printed)", t)
    if ty == "Car Mugs" and m:
        car = m.group(1).strip()
        makes = [v for k, v in CAR_MAKES if car.lower().startswith(k.lower())]
        c.update(fam="car", subject=car)
        tp("brand", makes[:1], d_brand(makes[:1]))
        return c
    if ty == "Alchemy Mugs":
        m = re.match(r"(.+?) Black Handle Alchemy", t)
        c.update(fam="alchemy", subject=re.sub(r"\s*\(White\)", "", m.group(1)).strip() if m else "Alchemy")
        return c
    if ty in ("Emoticons Mugs", "poo imoji"):
        s = re.sub(r"^(Personalised )?Cartoon ", "", t)
        s = re.sub(r"\s*(Emoji )?Emoticons Mugs.*$|\s*Emoji Mug$", "", s).replace("Tounge", "Tongue").replace("Toungue", "Tongue")
        s = s.replace("Wirth", "With").replace("Grimising", "Grimacing")
        c.update(fam="emoji", subject=s.strip(), personal="name" if "Personalised" in t or "Any Name" in tags else None)
        return c
    if ty == "Gaming Mugs":
        g = re.sub(r"\s*-\s*Gaming Mugs$", "", t).replace("Warefare", "Warfare").replace(" Mug", "").strip()
        owners = [o for k, o in GAMES if k in g.lower()]
        if "Signature" in g:
            owners = ["Valve", "the players named in the design"]
        c.update(fam="gaming", subject=g)
        tp("game", [g], d_game(owners or ["the game's publisher"]))
        return c
    if ty == "Meme Mugs":
        m = re.search(r"MEME (\d+)", t)
        c.update(fam="meme", subject=f"Meme {m.group(1)}" if m else "Meme", personal="name")
        return c
    if ty == "Scrabble Mugs":
        m = re.search(r'Initial "(\w)"', t)
        c.update(fam="scrabble", subject=m.group(1) if m else "A", personal="name")
        tp("brand", ["Scrabble"], d_brand(["Scrabble"]))
        return c
    m = re.match(r"All (Men|Women) Are Created Equal (\w+)", t)
    if m:
        c.update(fam="starsign", subject=m.group(2), who=m.group(1))
        return c
    m = re.match(r"(Kings|Queens) Are Born In (\w+)", t)
    if m:
        c.update(fam="kingqueen", subject={"Novemeber": "November", "Febuary": "February"}.get(m.group(2), m.group(2)), who=m.group(1))
        return c
    m = re.match(r"Comic Style (.+?) Mug", t)
    if m:
        c.update(fam="comic", subject=m.group(1))
        return c
    m = re.match(r"KEEP CALM AND (.+?) Mug", t)
    if m or t == "Personalised Keep Calm Mug":
        phrase = nice(m.group(1)) if m else None
        c.update(fam="keepcalm", subject=phrase, personal=None if m else "wording")
        if phrase and re.search(r"lego", phrase, re.I):
            tp("brand", ["LEGO"], d_brand(["LEGO"]))
        if phrase and re.search(r"batman|robin", phrase, re.I):
            who = "Batman" if "atman" in phrase else "Robin"
            tp("character", [who], d_character(who, "DC Comics"))
        return c
    m = re.match(r"Family Guy INSPIRED Theme Style (.+?) TV SHOW MUG", t)
    if m:
        c.update(fam="tv", subject=nice(m.group(1)), show="Family Guy")
        tp("character", ["Family Guy"], d_character("Family Guy", "the show's creators and studio"))
        return c
    if "Twilight" in t or "Bourne Identity" in t:
        show = "Twilight" if "Twilight" in t else "The Bourne Identity"
        c.update(fam="tv", subject=None, show=show)
        tp("character", [show], d_character(show, "the film's studio" if "Bourne" in show else "the films' studio and the books' publisher"))
        return c
    if "Duff Beer" in t:
        col = re.search(r"Simpsons (\w+)", t)
        c.update(fam="tv", subject=f"Duff Beer{(' ' + col.group(1).lower()) if col and col.group(1) not in ('Funny', 'Mug') else ''}",
                 show="The Simpsons")
        tp("character", ["The Simpsons", "Duff Beer"], d_character("The Simpsons", "the show's creators and studio"))
        return c
    if ty == "Dating Mugs":
        s = re.sub(r"\s*-\s*Dating Mug$", "", t)
        c.update(fam="dating", subject=s)
        if "Tinder" in t:
            tp("brand", ["Tinder"], d_brand(["Tinder"]))
        return c
    if ty == "cartoon mug":
        c.update(fam="beardcartoon", subject=re.sub(r" Cartoon Mug.*$", "", t))
        return c
    m = re.match(r"Personalised Unicorn (\d+)", t)
    if m:
        c.update(fam="unicorn", subject=m.group(1), personal="name")
        return c
    if "Coronation" in t:
        s = re.sub(r"King Charles Coronation Official |Logo Mug.*$", "", t).strip()
        c.update(fam="coronation", subject=s, welsh="WELSH" in t)
        tp("celeb", ["King Charles III"], d_celeb("King Charles III").replace(
            "King Charles III has not endorsed", "Neither King Charles III nor the Royal Household has endorsed"))
        return c
    if "Platinum Jubilee" in t:
        c.update(fam="jubilee", subject=None)
        tp("celeb", ["Queen Elizabeth II"], d_celeb("The Royal Household").replace("has not endorsed", "has not endorsed"))
        return c
    m = re.match(r"VE Day 80th Anniversary Mug Design (\d+)", t)
    if m:
        c.update(fam="veday", subject=m.group(1))
        return c
    if "Any Image And Text" in t:
        c.update(fam="photo", subject=None, personal="photo and text")
        return c
    if re.search(r"until retirement", t, re.I):
        c.update(fam="retire", subject=None, personal="number of years")
        return c
    m = re.match(r"I LOVE (.+?) I Love Mug", t, re.I)
    if m:
        topic = m.group(1).strip()
        key = topic.lower()
        c.update(fam="ilove", subject=nice(topic) if topic.isupper() or topic[1:].isupper() else topic, personal="name")
        if key in ILOVE_BANDS:
            tp("band", [ILOVE_BANDS[key]], d_band(ILOVE_BANDS[key]))
        elif key in ILOVE_BRANDS:
            tp("brand", [ILOVE_BRANDS[key]], d_brand([ILOVE_BRANDS[key]]))
        elif key in ILOVE_GAMES:
            g, o = ILOVE_GAMES[key]
            tp("game", [g], d_game([o]))
        c["rude"] = bool(re.search(r"anal|boob|breast|cock|sex|legs|breeding|weed|w33d|drugs|your mum|your dad", key))
        return c
    if ty == "Funny Mugs" and re.match(r"(Beard|Moustache)", t):
        m = re.match(r"(Beard|Moustache) ?(\d*)", t)
        c.update(fam="beard", subject=m.group(1), num=m.group(2))
        return c
    m = re.match(r"(.+?) Funny Mug — (.+)$", t)
    if m:
        c.update(fam="british", subject=m.group(1), slogan=m.group(2))
        return c
    m = re.match(r"Valentines Day (.+?) (Personalised )?Romantic Ceramic Mug Gift", t)
    if m:
        c.update(fam="valentine", subject=m.group(1), personal="name" if m.group(2) else None)
        if re.search(r"F\*\*\*|MILF|DILF", m.group(1)):
            c["rude"] = True
        return c
    if ty == "Mugs" and "Rude Swear Word Printed Mug Design" in t:
        m = re.search(r"Design - (.+?) ?\(3 Colours\)", t)
        c.update(fam="swear", subject=m.group(1).strip(), rude=True)
        return c
    # rude one-liners and everything else: slogan from the title
    s = strip_filler(t)
    s = re.sub(r"\s*-\s*$", "", s)
    c.update(fam="slogan", subject=s)
    if re.search(r"Its A NAME Thing|Name's|Shauns|SHARON'S|personalised", t, re.I):
        c["personal"] = "name"
    for k, (show, rights) in {"R2D2": ("Star Wars", "Lucasfilm")}.items():
        if k in t:
            tp("character", ["Star Wars (R2-D2)"], d_character("Star Wars", rights))
    for k, b in (("PornHub", "Pornhub"), ("Pornhub", "Pornhub"), ("RedTube", "RedTube"), ("YouPorn", "YouPorn"),
                 ("Facebook", "Facebook")):
        if k in t and b not in c["tpnames"]:
            tp("brand", [b], d_brand([b]))
    return c

# ------------------------------------------------------------------------------------------------ copy
def an(word):
    return ("an " if word[:1].lower() in "aeiou" else "a ") + word

def esc(s):
    return html.escape(s, quote=False)

def pick(rng, items):
    return rng.choice(items)

def facts(c, rng):
    col = c["colour"]
    mat = ("white ceramic" if col["white"] and not col["body"] else "ceramic")
    lines = [f"Capacity: 11oz (approx. 325ml)",
             f"Material: {mat}, C-handle, high-gloss finish",
             pick(rng, ["Print: sublimation, printed in-house in North Yorkshire",
                        "Printing: sublimation, done in-house in North Yorkshire"]),
             pick(rng, ["Care: dishwasher and microwave safe; avoid abrasive scourers",
                        "Care: dishwasher and microwave safe (skip the abrasive scourers)"]),
             "Packaging: protective packaging for UK delivery"]
    if col["body"]:
        lines.insert(2, f"This listing: {col['body']} version, as named in the title")
    if col["choice"]:
        name, vals = col["choice"]
        name = {"color": "colour"}.get(name.lower(), name)
        lines.insert(2, f"{name.capitalize()} options: {join(vals)}".replace(" and ", " or ") if len(vals) > 1 else f"{name.capitalize()}: {vals[0]}")
    if c.get("personal"):
        lines.append(f"Personalisation: {c['personal']}, printed as part of the design")
    return lines

GENERIC_BULLETS = [
    ["A proper 11oz (approx. 325ml) mug, so there's room for a decent brew",
     "11oz (approx. 325ml): big enough for a proper cuppa, not a thimble",
     "Holds 11oz (approx. 325ml), the size most tea drinkers reach for"],
    ["Dishwasher and microwave safe, so it can go straight into daily use",
     "Happy in the dishwasher and the microwave, no special treatment needed",
     "Dishwasher and microwave safe for real-life kitchens"],
    ["Glossy ceramic with a comfy C-handle",
     "High-gloss ceramic finish and a C-handle that's easy to hold",
     "Classic C-handle shape with a shiny high-gloss finish"],
    ["Sublimation printed in-house in North Yorkshire",
     "Printed by us in North Yorkshire using sublimation",
     "Made in-house in North Yorkshire, not shipped in from overseas"],
    ["Printed to order and packed in protective packaging for UK delivery",
     "Each one is printed to order, then packed carefully for the post",
     "Sent in protective packaging so it turns up in one piece"],
    ["Fancy a tweak? We do custom designs on request, just ring 01439 771468",
     "Custom designs on request: give us a call on 01439 771468",
     "Want something slightly different? Custom designs are available on request (01439 771468)"],
]

ADULT_LINES = ["Adult humour: this one's for grown-ups with a thick skin, not the kids' cupboard.",
               "A heads-up: it's adult humour, so keep it for the grown-ups who'll find it funny.",
               "Strictly adult humour, best given to someone who'll laugh rather than clutch their pearls.",
               "Please note it's adult humour, so it's one for the grown-ups rather than the school run."]

def personal_line(c, rng):
    f = c.get("personal")
    if not f:
        return ""
    return pick(rng, [
        f"It's personalised, so just let us know the {f} you'd like when you order (or ring us on 01439 771468) and we'll print it for you.",
        f"Because it's personalised, tell us the {f} you want when you order, or give us a ring on 01439 771468, and we'll add it before printing.",
        f"To personalise it, send us the {f} with your order (or call 01439 771468) and we'll set it into the design.",
    ])

def kw_and_parts(c, p, rng):
    """Return primary keyword, H2, opening paragraph, middle paragraph, 2 family bullets, closing line."""
    f, s = c["fam"], c["subject"]
    if c["rude"] and s:
        s = censor(s)
    S = esc(censor(s) if c["rude"] and s else (s or ""))
    if f == "occ":
        kw = f"world's best {s.lower()} mug" if not s.isupper() else f"world's best {s} mug"
        op = pick(rng, [f"This {kw} is a cheerful thank-you for the {s.lower()} who keeps everything running. ",
                        f"This {kw} is for the {s.lower()} in your life who deserves a little recognition. ",
                        f"Our {kw} is a fun gift for {an(s.lower())} who's brilliant at the job and doesn't hear it often enough. "])
        op += pick(rng, ["It's a nice way to mark a new job, a promotion, a retirement or simply a good year.",
                         "Leave it on their desk or in the staff kitchen and watch it become their favourite cup.",
                         "It makes a thoughtful leaving present, secret Santa gift or birthday surprise."])
        mid = pick(rng, [f"The design reads “World's Best {S}”, printed on an 11oz ceramic mug so it's front and centre at every tea break.",
                         f"You get an 11oz ceramic mug printed with “World's Best {S}”, a little bit of praise they'll see every time they put the kettle on."])
        fb = [f"A simple, feel-good gift for any {s.lower()}", pick(rng, ["Works for colleagues, friends or family", "Great for leaving dos, promotions and Christmas"])]
        cl = pick(rng, [f"Pop a card in with it and your {kw} is ready to give.",
                        f"Buying for the whole team? Our {kw} sits nicely alongside the rest of our job and occupation mugs.",
                        f"A {kw} is a small gift that gets used every single day."])
    elif f == "occ_rude":
        kw = "rude novelty mug"
        op = pick(rng, [f"This {kw} hands out a very cheeky award: “World's Best {S}”. ",
                        f"Looking for a {kw} for the mate with the filthiest sense of humour? “World's Best {S}” should do it. "])
        op += pick(rng, ["It's the sort of gift that gets a groan, a laugh and a lot of questions from the in-laws.",
                         "Expect raised eyebrows in the office kitchen."])
        mid = pick(rng, [f"It's an 11oz ceramic mug printed with “World's Best {S}”. The innuendo does the talking, so you don't have to.",
                         f"The design is a mock award for the “World's Best {S}”, printed on an 11oz ceramic mug."])
        fb = ["Innuendo that's cheeky rather than crude on the page", "Good for birthdays, stag dos and Valentine's banter"]
        cl = pick(rng, [f"Pair this {kw} with one of our rude cards for the full wind-up.", f"A {kw} like this is guaranteed to get a reaction."])
    elif f == "awesome":
        kw = f"awesome {censor(s).lower()} mug" if c["rude"] else f"awesome {s.lower()} mug"
        if c["rude"]:
            op = f"This {esc(kw)} is a back-handed compliment in mug form, for the friend who'll laugh rather than take offence. "
            op += "It's cheeky, it's sweary and it's honest."
            mid = f"The design calls them an “Awesome {S}”, printed on an 11oz ceramic mug so the message lands every morning."
            fb = ["Sweary banter for close friends and partners", "A funny birthday or secret Santa gift for adults"]
        else:
            op = pick(rng, [f"This {kw} is a fun way to tell your favourite {s.lower()} they're doing a great job. ",
                            f"Say thanks to the {s.lower()} who's always there with this cheerful {kw}. "])
            op += pick(rng, ["It's a lovely little gift for birthdays, Christmas or just because.", "It brings a bit of a smile to every tea break."])
            mid = f"The design simply says “Awesome {S}”, printed on an 11oz ceramic mug that's made for daily use."
            fb = [f"A bright, positive message for any {s.lower()}", "Easy gift for work friends, family or teammates"]
        cl = pick(rng, [f"Our {esc(kw)} makes gift buying easy.", f"Add a card and the {esc(kw)} is ready to wrap."])
    elif f == "always_right":
        kw = f"funny {s.lower()} mug"
        op = pick(rng, [f"This {kw} is for the {s.lower()} who knows best (and knows it). ",
                        f"Every {s.lower()} needs this {kw} on the side of the pitch, in the staff room or at the club. "])
        op += "It's a light-hearted way to say thank you, and a gentle dig at the same time."
        mid = f"The slogan reads “I'm a {S}. To save time, let's just assume I'm always right”, printed on an 11oz ceramic mug."
        fb = ["A great end-of-season or thank-you present", f"Made for the {s.lower()} who never loses an argument"]
        cl = pick(rng, [f"A {kw} is a handy team gift: everyone chips in a quid.", f"Pop a card in and your {kw} is sorted."])
    elif f == "rather":
        what = esc(s)
        kw = f"I'd rather be {('drinking ' + ('a pint of ' if c.get('pint') else '')) if c.get('drinking') else ''}{s.lower() if not c.get('drinking') else s} mug"
        if c.get("drinking"):
            op = pick(rng, [f"This {esc(kw)} is for the friend who'd swap the office for a {what} any day of the week. ",
                            f"Know someone counting down to {what} o'clock? This {esc(kw)} is made for them. "])
            op += "It's a funny desk mug for work, a birthday or a leaving do."
            mid = f"The design reads “I'd rather be drinking {'a pint of ' if c.get('pint') else ''}{what}”. " + \
                  "It's 11oz of ceramic, so it'll hold their tea or coffee until the real thing is on offer."
            fb = ["A cheeky nod to their favourite tipple", "Brilliant for work desks and home offices"]
            if c["rude"]:
                fb[0] = "A cheeky cocktail name that raises a smile"
        else:
            op = pick(rng, [f"This {esc(kw)} is for anyone whose head is always at {what.lower()} even when they're at work. ",
                            f"If they live for {what.lower()}, this {esc(kw)} will speak to them. "])
            op += "It's a fun gift for teammates, club mates and hobby fans."
            mid = f"The design reads “I'd rather be {what}”, printed on an 11oz ceramic mug for the desk, the clubhouse or the kitchen."
            fb = [f"Perfect for {what.lower()} fans", "A simple gift for birthdays, Christmas or the end of the season"]
        cl = pick(rng, [f"Our {esc(kw)} is a winner for secret Santa.", f"Add a card and the {esc(kw)} is ready to give."])
    elif f == "teacher":
        subj = s if s.isupper() and len(s) <= 4 else s.title() if s.isupper() else s
        kw = f"best {subj} teacher mug"
        who = {"male": "him", "female": "her"}.get(c.get("gender"), "them")
        op = pick(rng, [f"Our {kw} is a lovely end-of-term thank-you for the {subj} teacher who made the difference. ",
                        f"Say thank you to a brilliant {subj} teacher with this {kw}. "])
        op += f"It's a gift they'll actually use, every break time and every marking session."
        mid = f"It's an 11oz ceramic mug printed with “Best {esc(subj)} Teacher”" + \
              (f", in the {c['gender']} version of the design" if c.get("gender") else "") + f", ready to cheer {who} through the staff room queue."
        fb = ["A thoughtful end-of-year or leaving gift", "Good for teachers, tutors and teaching assistants"]
        cl = pick(rng, [f"Pair this {kw} with a thank-you card from the class.", f"A {kw} is a gift that lasts well beyond the summer holidays."])
    elif f == "name":
        kw = f"personalised {s} name mug"
        op = pick(rng, [f"This {kw} is a simple, personal gift with their name printed big and bold. ",
                        f"Nothing says “this one's mine” quite like a {kw}. "])
        op += pick(rng, ["No more mix-ups in the office kitchen.", "It's ideal for birthdays, Christmas and new jobs."])
        mid = f"The design shows the name {esc(s)}, and you can have it with any name you like."
        fb = ["Ends the “who's got my mug?” argument for good", "A personal gift that doesn't cost the earth"]
        cl = pick(rng, [f"Order a {kw} for everyone in the family.", f"A {kw} pairs nicely with a personalised card."])
    elif f == "celeb_future":
        if c["kind"] == "loves":
            kw = f"this guy loves {s} mug"
            mid = f"The design says “This Guy Loves {esc(s)}”, printed on an 11oz ceramic mug."
        else:
            title = "Mr" if c["kind"] == "mr" else "Mrs"
            kw = f"future {title} {s} mug"
            mid = f"The design reads “The Future {title} {esc(s)}”, printed on an 11oz ceramic mug for some wishful thinking with every brew."
        op = pick(rng, [f"This {esc(kw)} is for the superfan who's already planning the wedding. ",
                        f"Got a celebrity crush that's gone a bit far? This {esc(kw)} is the perfect wind-up. "])
        op += pick(rng, ["It's a funny birthday gift, a secret Santa winner and a guaranteed giggle.",
                         "It's a cheeky present for friends, partners and the office joker."])
        fb = ["A funny gift for any celebrity crush", "Great for birthdays, Christmas and secret Santa"]
        cl = pick(rng, [f"Our {esc(kw)} is a light-hearted fan gift.", f"A {esc(kw)} is sure to get a laugh."])
    elif f == "celeb_other":
        lead = c["lead"]
        kw = f"{s} celebrity crush mug"
        op = pick(rng, [f"This {esc(kw)} is a cheeky gift for a fan with a very serious celebrity crush. ",
                        f"This {esc(kw)} is the wind-up for a friend who's convinced they're destined for {esc(s)}. "])
        op += "It's a funny present for birthdays, hen dos and secret Santa."
        mid = f"The design reads “{esc(lead)} {esc(s)}”, printed on an 11oz ceramic mug."
        fb = ["A funny fan gift with a wink", "Great for birthdays and secret Santa"]
        cl = pick(rng, [f"Our {esc(kw)} is guaranteed to raise a laugh.", f"Wrap up a {esc(kw)} for the superfan in your life."])
    elif f == "celeb_ilove":
        kw = f"I love {s} mug"
        op = pick(rng, [f"This {esc(kw)} lets a proper fan show it every time they put the kettle on. ",
                        f"Know someone who can't stop talking about {esc(s)}? This {esc(kw)} is for them. "])
        op += "It's a simple, fun fan gift for birthdays and Christmas."
        mid = f"The design reads “I Love {esc(s)}” on an 11oz ceramic mug."
        fb = ["A fun fan gift that won't break the bank", "Ideal for birthdays, Christmas and secret Santa"]
        cl = pick(rng, [f"Our {esc(kw)} makes a cheerful fan present.", f"Wrap up an {esc(kw)} for the biggest fan you know."])
    elif f == "ilove":
        kw = f"I love {censor(s) if c['rude'] else s} mug"
        op = pick(rng, [f"This {esc(kw)} is for anyone who's head over heels for {S.lower() if not S.isupper() else S}. ",
                        f"Show off a favourite thing with this {esc(kw)}. "])
        op += "It's a bright, simple gift for birthdays, Christmas or the office."
        mid = f"The design reads “I Love {S}”, printed on an 11oz ceramic mug."
        fb = [f"A fun gift for anyone who loves {S}", "Easy pick for secret Santa and birthdays"]
        cl = pick(rng, [f"Our {esc(kw)} makes gift buying easy.", f"An {esc(kw)} is a little thing that gets used every day."])
    elif f == "bday_date":
        d = s or "your chosen date"
        kw = f"{d} birthday mug" if s else "this is my birthday mug"
        op = pick(rng, [f"This {kw} is made for anyone born on {d} who likes everyone to know about it. ",
                        f"Birthday on {d}? This {kw} makes sure nobody forgets. "]) if s else \
             f"This {kw} is for anyone who wants their birthday remembered. "
        op += "It's a funny little gift that gets used long after the cake's gone."
        mid = f"The design says “This is my birthday mug”" + (f" with the date {d}" if s else "") + ", printed on an 11oz ceramic mug."
        fb = ["A personal-feeling gift for their birthday", "Fun for colleagues to spot in the office kitchen"]
        cl = pick(rng, [f"Pair the {kw} with a birthday card.", f"A {kw} is a gift with their day written all over it."])
    elif f == "bday_year":
        kw = f"manufactured in {s} birthday mug"
        op = pick(rng, [f"This {kw} is a funny gift for anyone born in {s}. ",
                        f"Born in {s}? This {kw} celebrates a vintage year. "])
        op += "It's a great way to mark a milestone birthday with a smile."
        mid = f"The design reads “Manufactured in {s}”, printed on an 11oz ceramic mug."
        fb = [f"Perfect for anyone born in {s}", "A light-hearted milestone birthday gift"]
        cl = pick(rng, [f"Pair your {kw} with a birthday card.", f"A {kw} is a cheeky present for a big birthday."])
    elif f == "cartoon":
        sl = s if re.search(r"Darth|Storm Trooper|Tweety", s) else s.lower()
        kw = f"personalised {sl} mug"
        op = pick(rng, [f"This {kw} has a funny cartoon {esc(sl)} on it, plus a name to make it theirs. ",
                        f"Our {kw} is a cheerful cartoon design with a name added. "])
        op += "It's a sweet gift for birthdays, Christmas or a new desk."
        mid = f"The design shows a cartoon {esc(sl)}, with a name printed alongside it."
        fb = ["A fun cartoon design with a personal touch", "Lovely for animal lovers of any age"]
        cl = pick(rng, [f"A {kw} is a fun way to brighten up a tea break.", f"Pick a {kw} for each of the family."])
    elif f == "football":
        C = esc(s)
        kw = {"crazy": f"crazy {s} fan mug", "keepcalm": f"keep calm and support {s} mug",
              "signs": f"personalised {s} signs for mug", "team": f"personalised {s} football birthday mug"}[c["sub"]]
        op = pick(rng, [f"This {esc(kw)} is a fun gift for a {C} fan. ",
                        f"Got a {C} supporter to buy for? This {esc(kw)} is a sure winner. "])
        op += pick(rng, ["It's ideal for birthdays, Father's Day and Christmas.", "Perfect for match-day brews and the office desk."])
        mid = {"crazy": f"The design says they're a “Crazy {C} Fan”, printed on an 11oz ceramic mug.",
               "keepcalm": f"The design reads “Keep Calm and Support {C}”, printed on an 11oz ceramic mug.",
               "signs": f"It's a “signs for {C}” design with their name and age, printed on an 11oz ceramic mug.",
               "team": f"The design is themed on {C}, with their name and age added, printed on an 11oz ceramic mug."}[c["sub"]]
        fb = [f"A thoughtful gift for any {C} fan", pick(rng, ["Great for birthdays and Father's Day", "Made for match-day cuppas"])]
        cl = pick(rng, [f"Pair your {esc(kw)} with a football birthday card.", f"A {esc(kw)} is a gift any fan will use."])
    elif f == "dad_club":
        kw = "personalised world's best dad football mug"
        op = f"This {kw} is a Father's Day or birthday gift for a dad who lives for his team. "
        op += "Add his name, a message and his club badge so it's all about him."
        mid = "You send us a photo of the badge, the name and the message, and we print them on an 11oz ceramic mug."
        fb = ["Personalised with name, message and club badge photo", "A great Father's Day or birthday present"]
        cl = f"A {kw} is a gift dad will use every single day."
    elif f == "motor":
        sl = s.lower()
        kind = "motorbike" if re.search(r"bike|ninja|^r ?1$|triumph|vespa|wings", sl) else \
               "motorsport" if re.search(r"budweiser|yokohama|splitfire|sport|layer|^gt$|^rr$|^xr$|fuka", sl) else "car"
        kw = f"{s} {kind} mug"
        op = pick(rng, [f"This {esc(kw)} is for the petrolhead who's always talking about their wheels. ",
                        f"Buying for a motoring fan? This {esc(kw)} is a gift they'll use every day. ",
                        f"Our {esc(kw)} is made for the {kind} fan who lives in the garage at weekends. "])
        op += pick(rng, ["It's great for the garage, the workshop or the office.", "It's ideal for birthdays, Christmas and Father's Day."])
        mid = (f"It's design {c['num']} of our {esc(s)} designs" if c.get("num") else f"It's the {esc(s)} design") + \
              " from our motor range, printed on an 11oz ceramic mug."
        fb = [pick(rng, ["A gift for car and bike enthusiasts", "Made for motoring fans"]),
              pick(rng, ["Good for birthdays, Christmas and Father's Day", "At home in the garage or on the desk"])]
        cl = pick(rng, [f"A {esc(kw)} is a sure hit with any petrolhead.", f"Pair your {esc(kw)} with a birthday card."])
    elif f == "car":
        kw = f"I love my {s} mug"
        op = pick(rng, [f"This {esc(kw)} is for the driver who's proud of their motor. ",
                        f"If they love their {esc(s)} more than anything, this {esc(kw)} says so. "])
        op += "It's a fun gift for birthdays, Christmas and new-car celebrations."
        mid = f"The design reads “I Love My {esc(s)}”, printed on an 11oz ceramic mug."
        fb = ["A great gift for car lovers", "Brilliant for a new car celebration"]
        cl = pick(rng, [f"Our {esc(kw)} is a gift any car fan will appreciate.", f"Add a card and the {esc(kw)} is ready to go."])
    elif f == "alchemy":
        kw = f"{s.lower()} alchemy symbol mug"
        op = pick(rng, [f"This {esc(kw)} is a dark, gothic piece for anyone into old symbols, magic and mystery. ",
                        f"Our {esc(kw)} brings a touch of the old alchemists to the morning brew. "])
        op += "It's a lovely gift for goths, horror fans and lovers of the strange and old."
        mid = f"It features the alchemy symbol for {esc(s)}, printed on an 11oz ceramic mug with a black handle."
        fb = ["A gothic gift with a story behind it", "Collect the set: we have lots of alchemy symbols"]
        cl = pick(rng, [f"{an(esc(kw)).capitalize()} is perfect for Halloween or a goth birthday.", f"Pick up {an(esc(kw))} for the witchy friend."])
    elif f == "emoji":
        kw = f"{s.lower()} emoji mug"
        op = pick(rng, [f"This {esc(kw)} says exactly how they feel before the first coffee. ",
                        f"Let a face do the talking with this {esc(kw)}. "])
        op += "It's a fun gift for teens, students and anyone who texts in emojis."
        mid = f"The design shows a cartoon {esc(s.lower())} face, printed on an 11oz ceramic mug."
        fb = ["Fun, colourful emoji design", "A cheap and cheerful gift for friends"]
        cl = pick(rng, [f"Grab an {esc(kw)} for the friend who replies in emojis.", f"An {esc(kw)} is ideal for stocking fillers."])
    elif f == "gaming":
        kw = f"{s} gaming mug"
        op = pick(rng, [f"This {esc(kw)} is for the gamer who needs a brew between rounds. ",
                        f"Our {esc(kw)} is a fun gift for anyone who loves {esc(s)}. "])
        op += "It's ideal for the gaming desk, birthdays and Christmas."
        mid = f"The design is themed on {esc(s)}, printed on an 11oz ceramic mug."
        fb = ["A gift for gamers and streamers", "Looks good on any gaming setup"]
        cl = pick(rng, [f"Pair a {esc(kw)} with a gaming birthday card.", f"A {esc(kw)} is perfect for gamers."])
    elif f == "meme":
        kw = "personalised meme mug"
        op = f"This {kw} is design {esc(s.split()[-1])} from our meme range, a funny cartoon-style gift for anyone who lives online. "
        op += "Add a name and it's ready to raise a laugh."
        mid = f"You get {esc(s)} from our range, printed on an 11oz ceramic mug with the name you choose."
        fb = ["A funny meme-style design", "Great for teens, students and gamers"]
        cl = pick(rng, [f"A {kw} is a cheap and cheerful gift.", f"Grab a {kw} for the group chat comedian."])
    elif f == "scrabble":
        kw = f"personalised initial {s} letter tile mug"
        op = f"This {kw} spells out a name in letter-tile style, starting with {s}. "
        op += "It's a great gift for word game fans and anyone with a name beginning with that letter."
        mid = f"The design starts with the letter {esc(s)} and spells out the name you choose, printed on an 11oz ceramic mug."
        fb = ["A personal gift for word game fans", f"Ideal for anyone whose name starts with {s}"]
        cl = pick(rng, [f"Order a {kw} for each of the family.", f"A {kw} is a smart, personal present."])
    elif f == "starsign":
        kw = f"{s} star sign mug"
        op = f"This {kw} is a funny gift for a {s} who knows they're better than everyone else. "
        op += "It's perfect for birthdays during their star sign season."
        mid = f"The slogan says “All {c['who']} Are Created Equal” with the {esc(s)} star sign, printed on an 11oz ceramic mug."
        fb = [f"A fun gift for any {s}", "Good for birthdays and astrology fans"]
        cl = pick(rng, [f"Pair the {kw} with a birthday card.", f"Our {kw} is a birthday winner."])
    elif f == "kingqueen":
        kw = f"{c['who'].lower()} are born in {s} mug"
        op = f"This {kw} is a fun birthday gift for anyone born in {s}. "
        op += "It's a confident little reminder that they rule the roost."
        mid = f"The design reads “{c['who']} Are Born in {esc(s)}”, printed on an 11oz ceramic mug."
        fb = [f"A birthday gift for anyone born in {s}", "Fun for the office or home"]
        cl = pick(rng, [f"A {kw} pairs well with a birthday card.", f"Our {kw} is a cheerful birthday present."])
    elif f == "comic":
        kw = f"comic style {s.lower()} mug"
        op = f"This {esc(kw)} has a big, bold comic book sound effect on it: “{esc(s)}”. "
        op += "It's a fun gift for comic fans and anyone who likes a bit of drama with their tea."
        mid = f"The design shows “{esc(s)}” in comic book style, printed on an 11oz ceramic mug."
        fb = ["Bright, bold comic book look", "Fun for desks, kitchens and dens"]
        cl = pick(rng, [f"Collect a few comic style mugs to make a set.", f"A {esc(kw)} brightens any shelf."])
    elif f == "keepcalm":
        if s:
            kw = f"keep calm and {s.lower()} mug"
            op = f"This {esc(kw)} is a fun twist on the classic poster slogan. "
            op += "It's a light-hearted gift for birthdays, Christmas or the office."
            mid = f"The design reads “Keep Calm and {esc(s)}”, printed on an 11oz ceramic mug."
        else:
            kw = "personalised keep calm mug"
            op = f"This {kw} lets you write your own keep calm slogan. "
            op += "It's a fun, personal gift for any occasion."
            mid = "Choose the wording you want and we'll print it in the keep calm style on an 11oz ceramic mug."
        fb = ["A classic slogan with a fun twist", "Great for gifts and the office"]
        cl = pick(rng, [f"Our {esc(kw)} is easy to gift.", f"A {esc(kw)} makes a great stocking filler."])
    elif f == "tv":
        kw = f"{c['show']} inspired mug"
        op = f"This {esc(kw)} is a fun pick for fans of {esc(c['show'])}. "
        op += "It's a great gift for birthdays, Christmas and film or TV nights."
        mid = (f"The design features “{esc(censor(s) if c['rude'] else s)}”, " if s else "The design is ") + \
              f"inspired by {esc(c['show'])}, printed on an 11oz ceramic mug."
        fb = [f"A fan gift for {esc(c['show'])} lovers", "Good for birthdays and secret Santa"]
        cl = pick(rng, [f"A {esc(kw)} is perfect for a box-set binge.", f"Wrap a {esc(kw)} for the biggest fan you know."])
    elif f == "dating":
        kw = "funny dating app mug"
        op = f"This {kw} is a cheeky gift for couples who met online or friends who are still swiping. "
        op += "It's a fun present for anniversaries, Valentine's Day and birthdays."
        mid = f"The design says “{esc(s)}”, printed on an 11oz ceramic mug."
        fb = ["Perfect for couples who met online", "Funny Valentine's or anniversary gift"]
        cl = f"A {kw} makes a cheeky Valentine's gift."
    elif f == "beardcartoon":
        kw = f"{s.lower()} cartoon mug"
        op = f"This {esc(kw)} is a fun way to show off a great look. "
        op += "It's ideal for birthdays, Father's Day and friends with famous facial hair."
        mid = f"The design shows a cartoon character with {esc(s.lower())}, printed on an 11oz ceramic mug."
        fb = ["A fun gift for bearded friends", "Great for Father's Day"]
        cl = f"Our {esc(kw)} is a fun cartoon gift."
    elif f == "unicorn":
        kw = "personalised unicorn mug"
        op = f"This {kw} is a magical gift with a name added to make it theirs. It's design {s} from our unicorn range. "
        op += "It's lovely for birthdays, Christmas and anyone who loves unicorns."
        mid = f"You get unicorn design {s}, printed with the name you choose on an 11oz ceramic mug."
        fb = ["A sparkly, cute unicorn design", "Personal touch with their name"]
        cl = f"Pair a {kw} with a birthday card for the full magic."
    elif f == "coronation":
        kw = "King Charles coronation mug"
        op = f"This {kw} is a keepsake to remember the coronation of King Charles III. "
        op += "It's a lovely gift for royal fans and collectors."
        mid = f"The design shows a coronation logo in the {esc(s.lower())} style" + (" with Welsh wording" if c.get("welsh") else "") + \
              ", printed on an 11oz ceramic mug."
        fb = ["A commemorative keepsake for royal fans", "Great for collectors and family gifts"]
        cl = f"Our {kw} is a lasting reminder of a historic day."
    elif f == "jubilee":
        kw = "platinum jubilee mug"
        op = f"This {kw} remembers the Queen's Platinum Jubilee in 2022. "
        op += "It's a lovely keepsake for royal fans and collectors."
        mid = "The design celebrates the Platinum Jubilee, printed on an 11oz ceramic mug."
        fb = ["A commemorative keepsake", "Great for collectors"]
        cl = f"A {kw} is a lovely reminder of a historic year."
    elif f == "veday":
        kw = "VE Day 80th anniversary mug"
        op = f"This {kw} marks 80 years since Victory in Europe Day. It's design {s} in our VE Day range. "
        op += "It's a thoughtful keepsake for history lovers and families remembering loved ones."
        mid = f"You get VE Day design {s}, printed on an 11oz ceramic mug."
        fb = ["A commemorative keepsake for VE Day 80", "Thoughtful gift for history fans"]
        cl = f"Our {kw} is a respectful way to mark the anniversary."
    elif f == "photo":
        kw = "personalised photo mug"
        op = f"This {kw} lets you put any image and text on a mug. "
        op += "It's ideal for family photos, pets, inside jokes and logos you own."
        mid = "Send us the photo and text you want and we'll print them on an 11oz ceramic mug."
        fb = ["Any image and text you choose", "A truly one-off gift"]
        cl = f"A {kw} is a gift nobody else will have."
    elif f == "retire":
        kw = "retirement countdown mug"
        op = f"This {kw} is a funny gift for anyone counting down to the end of work. "
        op += "It's perfect for birthdays and the office."
        mid = "The design reads “Only X years until retirement” with the number you choose, printed on an 11oz ceramic mug."
        fb = ["Funny countdown gift", "Personalised with the number of years"]
        cl = f"A {kw} is a cheeky office gift."
    elif f == "beard":
        kw = f"funny {s.lower()} mug"
        n = c.get("num")
        op = f"This {kw} gives the drinker a new look with every sip. " + (f"It's design {n} in our {s.lower()} range. " if n else "")
        op += "It's a funny gift for birthdays, Father's Day and secret Santa."
        mid = f"The design is a cartoon {s.lower()}" + (f" (design {n})" if n else "") + ", printed on an 11oz ceramic mug."
        fb = ["A silly gift that gets a laugh", "Great for Father's Day and secret Santa"]
        cl = f"Our {kw} is a fun present."
    elif f == "british":
        kw = f"funny {s.lower()} mug"
        op = f"This {esc(kw)} is a dry bit of British humour for the busy and tea-dependent. "
        op += "It's a nice gift for colleagues, parents and friends."
        mid = f"The slogan reads “{esc(c['slogan'])}”, printed on an 11oz ceramic mug."
        fb = ["British humour for busy people", "Great office or home gift"]
        cl = f"A {esc(kw)} is a smart office gift."
    elif f == "valentine":
        V = esc(censor(s) if c["rude"] else s)
        kw = "personalised Valentine's mug" if c.get("personal") else "Valentine's Day mug"
        op = pick(rng, [f"This {kw} with the “{V}” design is a sweet way to say I love you. ",
                        f"Spoil your other half with this {kw}: “{V}”. "])
        op += "It's lovely for Valentine's Day, anniversaries and just because."
        mid = f"The design is “{V}”, printed on an 11oz ceramic mug" + (" with the name you choose." if c.get("personal") else ".")
        fb = ["A romantic gift that gets used every day", "Great for anniversaries too"]
        cl = f"Pair your {kw} with a Valentine's card."
    elif f == "swear":
        word = esc(s)
        kw = "rude swear word mug"
        op = pick(rng, [f"This {kw} has a creative insult on it: “{word}”. ",
                        f"Know someone who deserves to be called a “{word}”? This {kw} says it for you. "])
        op += "It's a cheeky gift for mates, partners and work wind-ups."
        mid = f"The design reads “{word}”, with the rude bits starred out, printed on an 11oz ceramic mug."
        fb = ["Creative swearing, starred out on the design", "A guaranteed laugh for adults"]
        cl = f"Our {kw} is a funny gift for grown-ups."
    else:  # slogan
        sl = S
        kw = ("rude Valentine's mug" if "love you" in s.lower() else "funny rude mug") if c["rude"] else "funny slogan mug"
        op = pick(rng, [f"This {kw} says “{sl}”, so you don't have to. ",
                        f"Our “{sl}” design is a {kw} for people who like a laugh. "])
        op += "It's a fun gift for birthdays, secret Santa and the office."
        mid = f"The slogan reads “{sl}”, printed on an 11oz ceramic mug."
        fb = [pick(rng, ["A slogan that gets a reaction", "Says what everyone's thinking"]),
              pick(rng, ["Great for birthdays and secret Santa", "A wind-up gift for mates and colleagues"])]
        cl = pick(rng, [f"Pair this {kw} with one of our cheeky cards for the full wind-up.",
                        f"A {kw} like this gets passed round the whole office.",
                        f"Our {kw} makes secret Santa a lot more interesting."] if c["rude"] else
                       [f"A {kw} like this brightens up any tea break.", f"Pair this {kw} with a card and it's ready to give."])
    return kw, op, mid, fb, cl

def build(p, c, variant=0):
    rng = random.Random(p["handle"] + str(variant))
    kw, op, mid, fb, cl = kw_and_parts(c, p, rng)
    H2 = kw[:1].upper() + kw[1:]
    extra = []
    if c["rude"]:
        extra.append(pick(rng, ADULT_LINES))
    pl = personal_line(c, rng)
    paras = [f"<p>{op}</p>", f"<h2>{esc(H2) if '&' not in H2 else H2}</h2>",
             f"<p>{mid}{(' ' + pl) if pl else ''}{(' ' + ' '.join(extra)) if extra else ''}</p>"]
    gen = [pick(rng, g) for g in GENERIC_BULLETS]
    rng.shuffle(gen)
    bullets = fb + gen[:4]
    paras.append("<h3>Why you'll love it</h3><ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>")
    paras.append("<h3>Size &amp; details</h3><ul>" + "".join(f"<li>{esc(x)}</li>" for x in facts(c, rng)) + "</ul>")
    paras.append("<h3>Delivery</h3><p>Each mug is printed to order. Postage options and costs are shown at checkout.</p>")
    paras.append(f"<p>{cl}</p>")
    if c["disc"]:
        # one paragraph, even when two kinds of name are involved (CLAUDE.md)
        paras.append('<h3>Please note</h3><p class="disclaimer">' + esc(" ".join(dict.fromkeys(c["disc"]))) + "</p>")
    return "\n".join(paras), kw

EXTRA = ["If you're stuck for a present, a mug is one of those gifts that actually gets used.",
         "It's the kind of present that quietly becomes their go-to cup.",
         "Tea, coffee or hot chocolate: it isn't fussy.",
         "It looks just as at home on an office desk as it does by the kettle.",
         "We print every order ourselves, so if you've a question just ring 01439 771468.",
         "It's a small gift that gets a smile every single morning."]
EXTRA_RUDE = ["Expect a proper laugh when it's unwrapped.", "It's guaranteed to get a reaction in the office kitchen."]

def first_sentence(body):
    first = text(re.match(r"<p>(.*?)</p>", body, re.S).group(1))
    return re.split(r"(?<=[a-z0-9\u201d'!?)][.?!])(?<!\bSt\.)(?<!\bST\.)(?<!\bJr\.)\s+(?=[A-Z\u201c])", first)[0]

def words(body):
    main = body.split("<h3>Please note</h3>")[0]
    return len(text(main).split())

def finish(p, c, variant=0):
    """Build, then nudge length into 180-250 words (disclaimer not counted) and keep the keyword count at 3+."""
    for v in range(variant * 20, variant * 20 + 20):     # re-roll until the keyword sits in the first sentence
        body, kw = build(p, c, v)
        if html.unescape(kw).lower() in first_sentence(body).lower():
            break
    rng = random.Random(p["handle"] + "x" + str(variant))
    pool = EXTRA_RUDE + EXTRA if c["rude"] else EXTRA[:]
    rng.shuffle(pool)
    if text(body).lower().count(html.unescape(kw).lower()) < 3:
        body = body.replace("</p>\n<h3>Please note", f" Order your {kw} today.</p>\n<h3>Please note") if "<h3>Please note" in body \
            else body[:-4] + f" Order your {kw} today.</p>"
    # trim: drop generic bullets one at a time
    while words(body) > 250 and body.count("<li>") > 5 + len(facts(c, random.Random(0))) - 2:
        ul = body.split("<h3>Why you'll love it</h3><ul>")[1].split("</ul>")[0]
        items = re.findall(r"<li>.*?</li>", ul)
        body = body.replace(ul, "".join(items[:-1]))
    # pad: add short sentences to the "what you get" paragraph
    while words(body) < 182 and pool:
        s = pool.pop()
        body = body.replace("</p>\n<h3>Why you'll love it</h3>", f" {s}</p>\n<h3>Why you'll love it</h3>", 1)
    return body, kw

def options_rows(p):
    opts = [o for o in p["options"]]
    rows = []
    for v in p["variants"]:
        parts = v["title"].split(" / ") if len(opts) > 1 else [v["title"]]
        if len(parts) != len(opts):
            raise ValueError(f"{p['handle']}: variant title {v['title']!r} doesn't fit options {opts}")
        cells = []
        for i in range(3):
            cells += [opts[i]["name"], parts[i]] if i < len(opts) else ["", ""]
        rows.append(cells + [v["sku"] or ""])
    return rows

HEAD = ["Handle", "Title", "Status", "Body (HTML)", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value",
        "Option3 Name", "Option3 Value", "Variant SKU"]

def product_rows(p, body):
    out = []
    for i, cells in enumerate(options_rows(p)):
        first = i == 0
        out.append([p["handle"], p["title"] if first else "", p["status"].lower() if first else "", body if first else ""] + cells)
    return out

def write_split(path_fmt, start, prods, bodies, limit=14_000_000):
    files, cur, size, n = [], [], 0, start
    def flush():
        nonlocal cur, size, n
        if cur:
            path = path_fmt.format(n=n)
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f); w.writerow(HEAD); w.writerows(cur)
            files.append(path); n += 1; cur, size = [], 0
    for p in prods:
        rows = product_rows(p, bodies[p["handle"]])
        b = sum(len(",".join(r)) for r in rows) + 200
        if size + b > limit:
            flush()
        cur += rows; size += b
    flush()
    return files, n

def main():
    export, out = sys.argv[1], sys.argv[2]
    queued_seo = set()
    for f in sys.argv[3:]:
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            queued_seo.add(r["Handle"])
    os.makedirs(out, exist_ok=True)
    P = load(export)
    dup = collections.Counter(text(p["descriptionHtml"]) for p in P)
    mugs = [p for p in P if is_mug(p)]
    checked = [p for p in mugs if not excluded(p)]
    stats = collections.Counter()
    rewrite, skipped, audit, tp_rows = [], [], [], []
    bodies, kws, classes = {}, {}, {}
    seen = {}
    for p in checked:
        r = poor_reasons(p, dup)
        stats["checked"] += 1
        stats["empty" if r == ["empty"] else ("poor" if r else "ok")] += 1
        skip = None
        tags = set(p["tags"])
        if r:
            if p["productType"] in NON_STANDARD_TYPES or "Thermal Mug" in p["title"] or p["handle"] == "mug":
                skip = "not a standard 11oz ceramic mug (or a service): mug fact sheet doesn't cover it"
            elif "foxy-new-2026" in tags:
                skip = "new 2026 listing written to the house rules; left alone"
            elif SKIP_OFFENSIVE.search(p["title"]):
                skip = "slur or mocks a condition: owner to decide whether to keep the product"
        c = classify(p) if r and not skip else None
        if c:
            body, kw = finish(p, c)
            v = 0
            while body in seen:
                v += 1
                body, kw = finish(p, c, v)
            seen[body] = p["handle"]
            bodies[p["handle"]], kws[p["handle"]], classes[p["handle"]] = body, kw, c
            rewrite.append(p)
            if c["tpnames"] or c["disc"]:
                tp_rows.append([p["handle"], p["title"], "; ".join(dict.fromkeys(c["tpnames"])) or "(see disclaimer)",
                                "yes" if "third-party-name" in tags else "no", p["id"]])
        elif r:
            skipped.append([p["handle"], p["title"], p["productType"], "; ".join(r), skip])
        mf = p["mf"]
        seo = p.get("seo") or {}
        img = (p.get("featuredMedia") or {}).get("image") or {}
        audit.append({"Handle": p["handle"], "Title": p["title"], "Type": p["productType"], "Status": p["status"].lower(),
                      "Description problems": "; ".join(r) or "ok",
                      "Rewritten in import file": "yes" if c else ("no: " + skip if skip else "no (already fine)"),
                      "Disclaimer added": "yes" if c and c["disc"] else "",
                      "Third-party names": "; ".join(dict.fromkeys(c["tpnames"])) if c else "",
                      "SEO title missing": "" if seo.get("title") else "yes",
                      "SEO description missing": "" if seo.get("description") else "yes",
                      "SEO in queued import (02-seo-CLEAN)": "yes" if p["handle"] in queued_seo else "",
                      "Vendor": p["vendor"], "Image alt text empty": "" if img.get("altText") else ("yes" if img else "no image"),
                      "id": p["id"]})
    # files
    rude_coll = lambda p: "ADULT MUGS (RUDE)" in p["tags"] or "Swear Word Mugs" in p["tags"]
    normal = [p for p in rewrite if not rude_coll(p)]
    rude = [p for p in rewrite if rude_coll(p)]
    pick3 = lambda L, fams: [next(p for p in L if classes[p["handle"]]["fam"] == f) for f in fams]
    test = pick3(normal, ["occ", "celeb_future", "football"]) + pick3(rude, ["slogan", "swear", "occ_rude"] if any(
        classes[p["handle"]]["fam"] == "occ_rude" for p in rude) else ["slogan", "swear", "slogan"])
    test = list({p["handle"]: p for p in test}.values())
    if len(test) < 6:
        test += [p for p in rude if p not in test][:6 - len(test)]
    with open(f"{out}/00-TEST-6-mugs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(HEAD)
        for p in test:
            w.writerows(product_rows(p, bodies[p["handle"]]))
    files, n = write_split(out + "/{n:02d}-mug-descriptions.csv", 1, normal, bodies)
    rfiles, _ = write_split(out + "/{n:02d}-rude-mug-descriptions.csv", n, rude, bodies)
    with open(f"{out}/audit-all-mugs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(audit[0].keys())); w.writeheader(); w.writerows(audit)
    with open(f"{out}/skipped.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Handle", "Title", "Type", "Description problems", "Why no copy was written"]); w.writerows(skipped)
    with open(f"{out}/third-party-names.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Handle", "Title", "Third-party names", "Had third-party-name tag", "Product ID"]); w.writerows(tp_rows)
    json.dump({"test": [p["handle"] for p in test], "files": [os.path.basename(x) for x in files + rfiles],
               "kws": kws}, open(f"{out}/build-info.json", "w"), indent=1)
    stats.update(rewritten=len(rewrite), normal=len(normal), rude=len(rude), skipped=len(skipped),
                 disclaimers=sum(1 for p in rewrite if classes[p["handle"]]["disc"]), tag_needed=sum(1 for r in tp_rows if r[3] == "no"))
    print(dict(stats))
    print("families:", collections.Counter(classes[h]["fam"] for h in classes).most_common())
    print("files:", [os.path.basename(x) for x in files + rfiles])

if __name__ == "__main__":
    main()
