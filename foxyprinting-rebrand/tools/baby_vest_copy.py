"""Baby vest / baby grow description rewrite (catalogue audit 9 Oct 2026, Fix 2).

Usage: python3 -I baby_vest_copy.py EXPORT.jsonl OUT_DIR

Rewrites the old (2017-era, Word/Amazon HTML) descriptions of the 2,004 single-variant "Baby Vest"
listings at £8.99. The newer £12.99 "Standard" vests already have new copy and are left alone.

Facts come only from plan/product-facts.md "Baby grows / baby vests": 100% cotton, soft feel, short sleeve,
nickel-free poppers, wash and iron inside out, sizes 0-3 / 3-6 / 6-9 / 9-12 months, made in-house in
North Yorkshire. Blank brand and print method are ASK there, so the copy names neither.
The listings have no size option and no personalisation box, so the copy doesn't say how the size or the
name on the back is chosen (ASK added to the fact sheet).

Writes OUT_DIR/baby-vest-descriptions.csv (Handle, Body (HTML)), tag-ids.txt (products that need the
third-party-name tag, added through the API), review.csv, samples.html, problems.csv.
"""
import csv
import hashlib
import html
import json
import os
import re
import sys

SUFFIX = re.compile(r"\s*(Personalised FOOTBALL TEAM Baby Grow|TEXT STYLE Baby Grow Bodysuit|Personalised Baby Boy Girl Unisex Short Sleeve Bodysuit|"
                    r"Printed Baby Grow Bodysuit Boy Girl Unisex Gift|Football Fan Baby Grow Bodysuit|Baby Grow Bodysuit|"
                    r"Baby Personalised Baby Boy Girl Unisex Short Sleeve Bodysuit)\s*$", re.I)
BANNED = re.compile(r"\b(official|licensed|authentic|genuine|approved|endorsed|merchandise|signed|autographed|memorabilia|limited edition|the best|best quality|best price|cheapest)\b", re.I)


def h(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)


def pick(pool, key, slot):
    return pool[h(key + slot) % len(pool)]


def esc(s):
    return html.escape(s, quote=False)


def text(x):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(x or ""))).strip()


# ---------- clubs ----------
CLUB_FIX = {
    "Afc Accrington Stanley": "Accrington Stanley", "Afc Wimbledon": "AFC Wimbledon", "Bournmouth": "Bournemouth",
    "Brighton And Hove": "Brighton & Hove Albion", "Brighton and Hove": "Brighton & Hove Albion", "Brighton And Hove Albion": "Brighton & Hove Albion",
    "Gillngham": "Gillingham", "Milwall": "Millwall", "Tettenham": "Tottenham Hotspur", "Tottenham": "Tottenham Hotspur",
    "Notts Forest": "Nottingham Forest", "Man United": "Manchester United", "Man City": "Manchester City", "Sheff Utd": "Sheffield United",
    "Sheff Wednesday": "Sheffield Wednesday", "West Brom": "West Bromwich Albion", "West Bromwich": "West Bromwich Albion",
    "Mk Dons": "MK Dons", "Huddersfield": "Huddersfield Town", "Leicester": "Leicester City", "Newcastle": "Newcastle United",
    "Swansea": "Swansea City", "West Ham": "West Ham United", "Hamilton": "Hamilton Academical", "Hearts": "Heart of Midlothian",
    "Chelsea": "Chelsea", "Queens Park Rangers": "Queens Park Rangers", "Red Devil": "Manchester United",
}
SCOTTISH = {"Celtic", "Rangers", "Hibernian", "Heart of Midlothian", "Dundee", "Kilmarnock", "Motherwell", "Hamilton Academical", "Partick Thistle",
            "Ross County", "St Johnstone", "Aberdeen", "Dundee United", "St Mirren", "Livingston", "Inverness"}
NATIONS = {"England": "the FA", "Scotland": "the Scottish FA", "Wales": "the Football Association of Wales"}
KNOWN = ["Arsenal", "Aston Villa", "Chelsea", "Everton", "Liverpool", "Man United", "Man Utd", "Manchester United", "Man City", "Manchester City",
         "Tottenham", "Spurs", "West Ham", "Westham", "Newcastle", "Leeds", "Celtic", "Rangers", "Sunderland", "Middlesbrough", "Hibernian", "Aberdeen",
         "Wolves", "Nottingham Forest", "Crystal Palace", "Brighton", "Fulham", "Brentford", "Burnley", "Southampton", "Leicester", "Wrexham"]
KNOWN_CLUB = re.compile(r"\b(" + "|".join(KNOWN) + r")\b", re.I)
CLUB_FIX.update({"Westham": "West Ham United", "Man Utd": "Manchester United", "Spurs": "Tottenham Hotspur", "Leeds": "Leeds United", "Wolves": "Wolverhampton Wanderers",
                 "Brighton": "Brighton & Hove Albion"})
CLUB_RE = [re.compile(r"^Me [Aa]nd (?:[Mm]y )?(\w+) [Ll]ove (.+)$"), re.compile(r"^(.+?) (?:in Training|Eat Sleep Repeat|Fan Starting)$")]


def club_name(raw):
    raw = re.sub(r"\s*Baby Grow\d*$", "", raw.strip())
    t = raw
    if raw.isupper() or raw.islower():
        t = " ".join(w if w in ("and", "of") else w.capitalize() for w in raw.lower().split())
    t = t.replace("Afc", "AFC").replace("Mk ", "MK ")
    return CLUB_FIX.get(t, CLUB_FIX.get(t.title(), t))


# ---------- third-party themes (non-football) ----------
THEMES = [
    (re.compile(r"\bjedi\b|vader|r2d2|wookie|star wars", re.I), "theme", "Star Wars", "Lucasfilm or Disney"),
    (re.compile(r"batman|batcave|\bbat ?baby\b", re.I), "theme", "Batman", "DC or Warner Bros."),
    (re.compile(r"harry potter|snitch", re.I), "theme", "Harry Potter", "Warner Bros. or the author"),
    (re.compile(r"thrones", re.I), "theme", "Game of Thrones", "HBO"),
    (re.compile(r"pokemon", re.I), "theme", "Pokémon", "Nintendo, Game Freak or The Pokémon Company"),
    (re.compile(r"frozen|olaf", re.I), "theme", "Frozen", "Disney"),
    (re.compile(r"trekkie", re.I), "theme", "Star Trek", "Paramount"),
    (re.compile(r"call of duty", re.I), "game", "Call of Duty", "Activision"),
    (re.compile(r"playstation|\bps4\b", re.I), "game", "PlayStation", "Sony"),
    (re.compile(r"xbox", re.I), "game", "Xbox", "Microsoft"),
    (re.compile(r"ipoo|\bwii\b", re.I), "brand", "Apple and Nintendo", None),
    (re.compile(r"happy mondays", re.I), "band", "Happy Mondays", None),
    (re.compile(r"\boasis\b", re.I), "band", "Oasis", None),
]


def slogan_of(title):
    s = SUFFIX.sub("", title).strip(" -–")
    s = re.sub(r"\s+\d+\.?$|\s+0\d$", "", s)                    # "Little Sister 2." / "03"
    fixes = {r"\bMater\b": "Matter", r"\bLive Throws\b": "Life Throws", r"\bNEICE\b": "Niece", r"\bWorlds\b": "World's",
             r"\bMummys\b": "Mummy's", r"\bDaddys\b": "Daddy's", r"\bMy First 1st\b": "My First", r"\b1st First\b": "First", r"\bYou Jedi\b": "Your Jedi"}
    for a, b in fixes.items():
        s = re.sub(a, b, s)
    small = {"and", "of", "the", "a", "an", "to", "in", "on", "at", "for", "with", "is", "my", "me", "as", "be", "or", "from", "by"}
    keep = {"TV", "UK", "PS4", "R&B", "DJ", "BBQ", "MK", "AFC", "QPR", "R2D2", "ABCD", "I"}
    out = []
    for i, w in enumerate(s.split()):
        if w in keep or not re.search(r"[A-Za-z]", w):
            out.append(w)
        elif w.isupper() and len(w) > 1:
            out.append(w.capitalize() if i == 0 or w.lower() not in small else w.lower())
        elif w.islower() and w not in small:
            out.append(w.capitalize())
        else:
            out.append(w)
    return re.sub(r"\s+", " ", " ".join(out)).strip()


def classify(p):
    s = slogan_of(p["title"])
    for rx in CLUB_RE:
        m = rx.match(s)
        if m and ("FOOTBALL" in " ".join(p["tags"]).upper() or "TEXT STYLE" in p["title"] or "Football Fan" in p["title"] or "Fan Starting" in s):
            club = club_name(m.group(m.lastindex))
            if club in ("Trekkie",):
                break
            who = m.group(1) if m.lastindex == 2 else None
            return dict(kind="football", slogan=s, club=club, who=who)
    m = KNOWN_CLUB.search(s)
    if m:
        return dict(kind="football", slogan=s, club=club_name(m.group(0)), who=None)
    for rx, kind, name, owner in THEMES:
        if rx.search(s):
            return dict(kind=kind, slogan=s, name=name, owner=owner)
    return dict(kind="plain", slogan=s)


# ---------- disclaimers (CLAUDE.md templates) ----------
def disclaimer(c):
    if c["kind"] == "football":
        club = c["club"]
        if club in NATIONS:
            body = (f"This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or affiliated with "
                    f"{NATIONS[club]}, the {club} national team or any club, league or player. Team names are used only to describe the design and who it's for. "
                    "All trademarks belong to their respective owners.")
        else:
            league = "the Scottish Professional Football League" if club in SCOTTISH else "the Premier League, the English Football League"
            body = (f"This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or affiliated with "
                    f"{club}, {league} or any club, league or player. Club and player names are used only to describe the design and who it's for. "
                    "All trademarks belong to their respective owners.")
    elif c["kind"] == "theme":
        body = (f"This is an unofficial design inspired by {c['name']}. It is not official merchandise and is not endorsed by, sponsored by, or connected with "
                f"{c['name']}, {c['owner']}, or any of their licensees. All names, characters and trademarks belong to their respective owners.")
    elif c["kind"] == "game":
        body = (f"This is an unofficial, fan-made design produced by Foxy Printing. It is not made, endorsed or licensed by {c['owner']}. "
                f"{c['name']} is a trademark of its owner and is used only to describe the design theme.")
    elif c["kind"] == "brand":
        body = (f"This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {c['name']}. "
                "Their names are trademarks of their owners and are used only as a play on words in the design.")
    elif c["kind"] == "band":
        body = (f"This is an unofficial fan design. It is not endorsed by, or connected with, {c['name']}, their management or record label. "
                "All names and trademarks belong to their respective owners.")
    else:
        return ""
    return "\n<h3>Please note</h3>\n<p class=\"disclaimer\">" + esc(body) + "</p>"


# ---------- copy ----------
FAMILY = re.compile(r"\b(Mummy|Mommy|Mum|Mom|Mama|Mammy|Daddy|Dad|Grandad|Grandpa|Grandma|Nanny|Nana|Nan|Granny|Uncle|Aunty|Auntie|Aunt|Godmother|Godfather|"
                    r"Sister|Brother|Cousin|Cousins|Siblings|Grandparents)\b", re.I)
OCCASION = [(re.compile(r"christmas|xmas|santa|elf", re.I), "Christmas"), (re.compile(r"valentine", re.I), "Valentine's Day"),
            (re.compile(r"mother'?s day", re.I), "Mother's Day"), (re.compile(r"father'?s day", re.I), "Father's Day"),
            (re.compile(r"halloween", re.I), "Halloween"), (re.compile(r"easter", re.I), "Easter"), (re.compile(r"diwali", re.I), "Diwali"),
            (re.compile(r"christening", re.I), "a christening"), (re.compile(r"birthday", re.I), "a first birthday")]


def occasion(s):
    for rx, name in OCCASION:
        if rx.search(s):
            return name
    return None


def build(p):
    c = classify(p)
    s, key = c["slogan"], p["handle"]
    q = f"“{esc(s)}”"
    kw = f"{esc(s)} baby grow"
    if re.search(r"limited edition", s, re.I):
        kw = "personalised " + esc(re.sub(r"\s*Limited Edition", "", s, flags=re.I).strip().lower()) + " baby grow"
    occ = occasion(s)
    fam = FAMILY.search(s)
    who = c.get("who") or (fam.group(1).capitalize() if fam else None)
    if c["kind"] == "football":
        club = esc(c["club"])
        opener = pick([
            f"Start them young with our {kw}, a fan-made {club} baby vest that's perfect for match days, a baby shower or a new arrival.",
            f"Our {kw} is a fun way to welcome the newest {club} fan to the family, printed to order in our North Yorkshire workshop.",
            f"Got a little one who'll be cheering on {club} before they can walk? This {kw} says it loud and proud.",
        ], key, "o")
        h2 = pick([f"{esc(s)} baby grow for {club} fans", f"{club} fan baby vest: {esc(s)}", f"{esc(s)} baby grow"], key, "h")
        what = f"The front reads {q} in a bold football fan design."
        if who:
            art = "an" if who[0].lower() in "aeiou" else "a"
            what += f" It's a lovely gift from {art} {esc(who.lower())} who wants to pass on the football bug."
        gift = pick(["a baby shower", "a new arrival in the family", "their first match-day photo", "a christening or naming day"], key, "g")
    else:
        opener = pick([
            f"Our {kw} is a sweet, funny way to dress a little one, printed with {q} and made to order here in North Yorkshire.",
            f"Looking for a baby gift that raises a smile? This {kw} has {q} printed on the front and makes a lovely present for a new arrival.",
            f"Say it with a slogan: our {kw} reads {q} and is made in-house in our North Yorkshire workshop.",
        ], key, "o")
        h2 = pick([f"{esc(s)} baby grow", f"{esc(s)} baby vest", f"Personalised {esc(s)} baby grow"], key, "h") if kw.startswith(esc(s)) else kw[0].upper() + kw[1:] + " with slogan"
        what = f"The front of the vest reads {q}" + (" (these are the words printed on the front; each vest is made to order)." if "imited Edition" in s else ".") + (f" It's a great choice for {occ}, or any day you want a cute photo." if occ else
                                                         (f" It makes a thoughtful gift from {esc(who)} or for a proud {esc(who.lower())}." if who else
                                                          " It's a fun outfit for everyday wear and a guaranteed photo moment."))
        gift = pick(["a baby shower", "a new arrival", "a hospital bag surprise", occ or "a first photo shoot"], key, "g")
    name_line = pick([" We can also add a name on the back, so just let us know the name you'd like when you order.",
                      " Want their name on the back? Tell us the name when you order and we'll add it.",
                      " A name on the back makes it even more special: just let us know it when you order."], key, "n")
    sizes = " It comes in four sizes, from 0–3 months up to 9–12 months."
    bullets_pool = [
        "Soft 100% cotton, kind to delicate skin",
        "Short sleeves and nickel-free poppers for quick, easy nappy changes",
        "Printed in-house in North Yorkshire, UK, and made to order",
        f"A lovely gift for {gift}",
        "Four sizes from newborn (0–3 months) to 9–12 months",
        "Wash and iron inside out to keep the print looking good",
    ]
    order = sorted(range(len(bullets_pool)), key=lambda i: h(key + "b" + str(i)))[:5]
    bullets = "\n".join(f"<li>{b}</li>" for b in [bullets_pool[i] for i in sorted(order)])
    closer = pick([
        f"Pair the {kw} with a personalised new baby card for a ready-made gift. Custom slogans and designs are available on request: call 01439 771468.",
        "Make it a set with a matching personalised mug for the proud parents. Want a different slogan? We do custom designs on request: call 01439 771468.",
        f"Buying for a baby shower? Add a personalised card and the {kw} is ready to give. Custom designs on request: call 01439 771468.",
    ], key, "c")
    body = (f"<p>{opener}</p>\n<h2>{h2}</h2>\n<p>{what}{sizes}{name_line}</p>\n"
            f"<h3>Why you'll love it</h3>\n<ul>\n{bullets}\n</ul>\n"
            "<h3>Size &amp; details</h3>\n<ul>\n<li>Sizes: 0–3 months, 3–6 months, 6–9 months, 9–12 months</li>\n"
            "<li>Material: 100% cotton, soft feel</li>\n<li>Style: short sleeve baby vest with nickel-free poppers</li>\n"
            "<li>Care: wash and iron inside out</li>\n<li>Printed in North Yorkshire, UK</li>\n</ul>\n"
            "<h3>Delivery</h3>\n<p>Each baby grow is printed to order in our North Yorkshire workshop. Postage options and costs are shown at checkout.</p>\n"
            f"<p>{closer}</p>" + disclaimer(c))
    return body, c


def check(body, c):
    slogan = esc(c["slogan"])
    pr = []
    if body.count("<h2") != 1:
        pr.append("h2")
    if re.search(r"style=|<span|<h1|<table|<br|<img|\[|\]", body):
        pr.append("html")
    nd = re.sub(r'<p class="disclaimer">.*?</p>', "", body, flags=re.S).replace(slogan, "")
    nd = re.sub(r"\u201c[^\u201d]*\u201d", "", nd)
    m = BANNED.search(text(nd))
    if m:
        pr.append("banned:" + m.group(0))
    w = len(text(body).split())
    if not 180 <= w <= 350:
        pr.append(f"words {w}")
    if c["kind"] != "plain" and not body.rstrip().endswith("</p>") or (c["kind"] != "plain" and "Please note" not in body):
        pr.append("disclaimer")
    return pr


def main(src, out):
    os.makedirs(out, exist_ok=True)
    P = {}
    for line in open(src, encoding="utf-8"):
        o = json.loads(line)
        if "__parentId" in o:
            if o["__parentId"] in P:
                P[o["__parentId"]]["variants"].append(o)
            continue
        o["variants"] = []
        P[o["id"]] = o
    rows, review, probs, tag_ids, seen = [], [], [], [], {}
    for p in P.values():
        if p["productType"] != "Baby Vest" or p["status"] != "ACTIVE" or [v["title"] for v in p["variants"]] != ["Default Title"]:
            continue
        body, c = build(p)
        pr = check(body, c)
        if body in seen:
            pr.append("duplicate of " + seen[body])
        seen[body] = p["handle"]
        if pr:
            probs.append([p["handle"], p["title"], ";".join(pr)])
            continue
        rows.append([p["handle"], body])
        review.append([p["handle"], p["title"], c["kind"], c.get("club") or c.get("name") or "", len(text(body).split())])
        if c["kind"] != "plain" and "third-party-name" not in p["tags"]:
            tag_ids.append(p["id"])
    with open(os.path.join(out, "baby-vest-descriptions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Handle", "Body (HTML)"])
        w.writerows(rows)
    with open(os.path.join(out, "review.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Handle", "Title", "Kind", "Third-party name", "Words"])
        w.writerows(review)
    with open(os.path.join(out, "problems.csv"), "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([["Handle", "Title", "Problem"]] + probs)
    open(os.path.join(out, "tag-ids.txt"), "w").write("\n".join(tag_ids) + "\n")
    pick_kinds = {}
    for r in review:
        pick_kinds.setdefault(r[2], []).append(r[0])
    sample = [hs[h(k) % len(hs)] for k, hs in sorted(pick_kinds.items())]
    bodies = dict(rows)
    titles = {r[0]: r[1] for r in review}
    with open(os.path.join(out, "samples.html"), "w", encoding="utf-8") as f:
        f.write("<!doctype html><meta charset=utf-8><title>Baby vest samples</title><style>body{font-family:sans-serif;max-width:820px;margin:auto;padding:16px}"
                "section{border-bottom:1px solid #ccc;padding:12px 0}</style><h1>Baby vest description samples</h1>")
        for hd in sample:
            f.write(f"<section><p><b>{esc(titles[hd])}</b> <code>{hd}</code></p>{bodies[hd]}</section>")
    print(len(rows), "rows,", len(probs), "problems,", len(tag_ids), "need tag;", {k: len(v) for k, v in pick_kinds.items()})


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
