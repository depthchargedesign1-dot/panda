"""Compliance rewrite (9 Oct 2026): products whose copy breaks the house rules in a way Google or a rights holder
would notice, from the full catalogue audit (exports/catalogue-audit/2026-10-09):

  * "Limited Edition" on reproduction prints (Tiny Men Big Balls club posters, team display posters,
    Liverpool 2020 posters, two baby grows, the rude sock, the Top Gun mask pack);
  * "memorabilia" wording (2025/2026 player, squad, darts, F1, boxing and horror film posters);
  * third-party-name products with no disclaimer (YouTuber, K-pop and footballer face masks, a few posters).

Every product gets a full house-style description (one h2, Why you'll love it, Size & details, Delivery,
closing line, Please note disclaimer last), facts only from plan/product-facts.md ("Posters & prints",
"Face masks"), plus SEO title/meta. Titles that themselves say "Autographed", "Memorabilia" or
"Limited Edition" are cleaned too (handles unchanged).

Usage: python3 -I compliance_copy.py EXPORT.jsonl IDS.txt OUT_DIR
  EXPORT.jsonl  bulk export: products { id handle title status productType tags descriptionHtml seo options variants }
  IDS.txt       product gids, one per line
Writes OUT_DIR/updates.json (productUpdate inputs + tags to add), OUT_DIR/review.csv, OUT_DIR/samples.html
and prints any product whose copy fails the checks.
"""
import csv
import hashlib
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from poster_descriptions import parse_sizes, DIMS, join_and, join_or  # noqa: E402

BANNED = re.compile(r"\b(signed|autograph\w*|authentic|limited[- ]edition|memorabilia|collectibles?|collector'?s?|"
                    r"official(ly)?|licensed|genuine|approved|endorsed|merchandise|merch)\b", re.I)


def pick(pool, key, slot):
    return pool[int(hashlib.md5((key + "|" + slot).encode()).hexdigest(), 16) % len(pool)]


def esc(s):
    return html.escape(s, quote=False)


def text(h):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(h or ""))).strip()


def words(body):
    return len(text(body.split("<h3>Please note</h3>")[0]).split())


def fix_q(s):
    # "Wubben?Moy", "Left?Back": a lost non-breaking hyphen
    return re.sub(r"(?<=\w)\?(?=\w)", "-", s)


SIGNED = ("This is a printed reproduction. The signature is printed as part of the design – it is not hand-signed "
          "and is not an original autograph. ")

FOOTBALL_BODY = "the Premier League, the English Football League, the FA or any football club, league or player"
FOOTBALL_BODY_INT = "FIFA, UEFA, any national football association, or any football club, league or player"

# ------------------------------------------------------------------ shared poster blocks

FRAME_LINE = [
    "Framed options come in our Premium Display frames – thick, chunky and very professional, not the cheap thin frames you often see.",
    "Go framed and it arrives in one of our Premium Display frames: thick, chunky and properly professional, not a flimsy thin frame.",
    "The framed versions use our Premium Display frames, a thick, chunky, professional finish rather than a cheap thin frame.",
]
DELIVERY = [
    "Printed to order in our North Yorkshire workshop. Postage options and costs are shown at checkout.",
    "Each print is made to order here in North Yorkshire. You'll see the postage options and costs at checkout.",
    "We print your poster when you order, in our own North Yorkshire workshop. Postage options and prices are shown at checkout.",
]
MADE = ["Made in-house in North Yorkshire, UK, and printed when you order",
        "Printed to order in our own North Yorkshire workshop",
        "Designed and printed in-house in North Yorkshire"]


def size_block(p, key):
    """(sentence for the details paragraph, bullet(s), Size & details items, has_frames)"""
    vals = [v for o in p["options"] for v in o["values"] if v != "Default Title"]
    prints, frames = parse_sizes(vals)
    if not (prints or frames):
        sent = pick(["Pick your size and finish from the choices shown on this page before you add it to your basket.",
                     "Choose your size and finish from the options on this page.",
                     "The sizes and finishes on offer are shown in the choices on this page."], key, "nosz")
        items = ["Size and finish: as shown in the choices on this page", "Full-colour print, made to order",
                 "Printed in North Yorkshire, UK"]
        return sent, [], items, None
    cols = sorted({c for v in frames.values() for c in v}, key=["Black", "Silver", "Gold", "White"].index)
    parts = []
    if prints:
        parts.append(("a print-only " + prints[0]) if len(prints) == 1 else ("print-only sizes " + join_or(prints)))
    if frames:
        parts.append("a framed " + join_or(list(frames)) + (" in " + join_or([c.lower() for c in cols]) if cols else ""))
    sent = pick(["Pick the size that suits your wall: {p}.", "Choose from {p}.", "It comes in {p}, so there's an option for every wall."],
                key, "sz").format(p=", or ".join(parts))
    bl = []
    if len(prints) >= 2:
        bl.append(f"Print-only sizes from {prints[0]} up to {prints[-1]}")
    elif prints:
        bl.append(f"Print-only {prints[0]} size")
    if frames:
        bl.append(f"Framed {join_and(list(frames))} options in {join_or([c.lower() for c in cols])} Premium Display frames")
        if "A3" in frames and "A4" in frames:
            bl.append("A3 frames have a clip on the back to hang; A4 frames have a stand")
    items = [f"{s} print only: {DIMS[s]}" for s in prints] + [f"{s} framed: {join_or(c)} frame" for s, c in frames.items()]
    return sent, bl, items, bool(frames)


def assemble(opening, h2, detail, bullets, items, delivery, close, disc):
    seen, bl = set(), []
    for b in bullets:
        if b and b not in seen:
            seen.add(b)
            bl.append(b)
    return "\n".join([
        f"<p>{opening}</p>", f"<h2>{h2}</h2>", f"<p>{detail}</p>",
        "<h3>Why you'll love it</h3>", "<ul>\n" + "\n".join(f"<li>{b}</li>" for b in bl) + "\n</ul>",
        "<h3>Size &amp; details</h3>", "<ul>\n" + "\n".join(f"<li>{s}</li>" for s in items) + "\n</ul>",
        "<h3>Delivery</h3>", f"<p>{delivery}</p>", f"<p>{close}</p>",
        "<h3>Please note</h3>", f'<p class="disclaimer">{disc}</p>'])


def football_disc(names, international=False, signed=False):
    return ((SIGNED if signed else "") + "This is an unofficial, fan-made design created and printed by Foxy Printing. "
            "It is not endorsed by, sponsored by, or affiliated with " + ", ".join(names) + ", " +
            (FOOTBALL_BODY_INT if international else FOOTBALL_BODY) +
            ". Club and player names are used only to describe the design and who it's for. All trademarks belong to their respective owners.")


# ------------------------------------------------------------------ football: Tiny Men Big Balls club posters

CLUB_FIX = {"Ipswitch": "Ipswich", "Norwitch": "Norwich", "Man Utd": "Manchester United", "Man City": "Manchester City",
            "Notts Forest": "Nottingham Forest"}


def tmbb(p):
    m = re.match(r"(.+?) Football Club gift\s*-\s*(?:(.+?)\s*-\s*)?Tiny Men Big Balls Poster", p["title"], re.I)
    club_raw, nick = m.group(1).strip(), (m.group(2) or "").strip()
    club = CLUB_FIX.get(club_raw, club_raw)
    key = p["handle"]
    e = dict(club=esc(club), nick=esc(nick or club))
    opening = pick([
        "Give a {club} fan something to grin about with our Tiny Men Big Balls football poster. It's a cheeky, fun print that pokes a bit of fun at the beautiful game, made to order here in North Yorkshire.",
        "Our Tiny Men Big Balls football poster for {club} fans is a light-hearted bit of wall art for a bedroom, man cave or office. It's printed in-house in North Yorkshire when you order.",
        "Looking for a funny football gift for a {club} supporter? This Tiny Men Big Balls football poster is a cheeky print that always gets a laugh, printed to order in our North Yorkshire workshop.",
        "If you know someone who lives and breathes {nick}, our Tiny Men Big Balls football poster for {club} fans is a fun way to show it. It's made to order in North Yorkshire.",
    ], key, "o").format(**e)
    h2 = pick(["Tiny Men Big Balls football poster for {club} fans", "{club} fan gift: Tiny Men Big Balls football poster",
               "Funny football poster for {club} supporters"], key, "h").format(**e)
    sent, sbl, items, fr = size_block(p, key)
    dpool = (["It's our own fan-made design in the Tiny Men Big Balls series, made for supporters of {club} – {nick} to their fans.",
              "The design is part of our own fan-made Tiny Men Big Balls range, with a version for {club} fans, known to many as {nick}.",
              "This is one of our own fan-made Tiny Men Big Balls designs, this time for anyone who follows {club} ({nick})."] if nick else
             ["It's our own fan-made design in the Tiny Men Big Balls series, made for supporters of {club}.",
              "The design is part of our own fan-made Tiny Men Big Balls range, with a version for {club} fans."])
    detail = (pick(dpool, key, "d").format(**e)
              + " " + sent + (" " + pick(FRAME_LINE, key, "f") if fr else
                               " Where framed options are offered, they come in our Premium Display frames – thick, chunky and very professional."))
    bullets = [pick(MADE, key, "m"), "A cheeky, light-hearted design that gets a laugh on match day"] + sbl + [
        pick(["Ideal for a birthday, Christmas or Father's Day", "A fun Secret Santa or birthday present for a football fan",
              "An easy gift for the {club} fan who has every shirt"], key, "g").format(**e),
        pick(["Looks great in a bedroom, games room, office or man cave", "Brightens up a man cave, bar area or bedroom wall"], key, "w"),
        "Fits standard A-size frames if you'd rather frame it yourself"]
    close = pick(["Pair it with a matching mug or bar mat for a {club} fan's birthday bundle. Custom designs are available on request – call 01439 771468.",
                  "Collecting the set? We make Tiny Men Big Balls posters for lots of clubs. Want a different team? Call us on 01439 771468.",
                  "Make it a gift bundle with a football mug or card for a {club} supporter. Custom designs on request – call 01439 771468."], key, "c").format(**e)
    disc = football_disc([esc(club)])
    body = assemble(opening, h2, detail, bullets, items, pick(DELIVERY, key, "dl"), close, disc)
    seo = f"Funny {club} Fan Football Poster | Foxy Printing"
    if len(seo) > 60:
        seo = f"{club} Fan Football Poster | Foxy Printing"
    if nick:
        seo = next(s for s in [f"{club} Fan Football Poster – {nick} | Foxy Printing", f"{club} Fan Football Poster – {nick}",
                               f"{club} Football Poster – {nick}", f"{club} Fan Football Poster"] if len(s) <= 60)
    meta = fit_meta([
        f"Funny football poster for {club} fans from our Tiny Men Big Balls range. Printed to order in North Yorkshire. A cheeky birthday or Christmas gift.",
        f"Cheeky Tiny Men Big Balls football poster for {club} supporters. Printed to order in our North Yorkshire workshop. A fun gift for any fan.",
    ], key, [" Order today.", " Fun gift.", " UK made."])
    title = f"{club} Fan Gift – Tiny Men Big Balls Football Poster" if club_raw != club else None
    return body, seo, meta, title, []


# ------------------------------------------------------------------ football: team display posters (Atalanta FC etc.)

def team_display(p):
    club = re.sub(r"\s*\d*\s*Football Team Printed Display Poster Gift$", "", p["title"]).strip()
    n = re.search(r"\b(\d)\s+Football Team", p["title"])
    key = p["handle"]
    e = dict(club=esc(club))
    opening = pick([
        "Our {club} football team poster is a smart piece of wall art for any supporter, printed to order in our North Yorkshire workshop. It makes an easy birthday or Christmas present for a football fan.",
        "Show who you follow with this {club} football team poster, a fan-made print for a bedroom, office, bar or man cave. We print it in-house in North Yorkshire when you order.",
        "Looking for a gift for a {club} supporter? This {club} football team poster is a fan-made print that looks the part on any wall, made to order in North Yorkshire.",
    ], key, "o").format(**e)
    h2 = pick(["{club} football team poster", "{club} football team poster print for fans", "Football team poster for {club} supporters"], key, "h").format(**e)
    sent, sbl, items, fr = size_block(p, key)
    detail = (pick(["It's our own fan-made team design for {club} supporters" + (" (design " + n.group(1) + ")" if n else "") + ".",
                    "The design is our own fan-made team print for anyone who follows {club}" + (", design " + n.group(1) if n else "") + "."],
                   key, "d").format(**e) + " " + sent + (" " + pick(FRAME_LINE, key, "f") if fr else ""))
    bullets = [pick(MADE, key, "m")] + sbl + [
        pick(["A thoughtful gift for a birthday, Christmas or Father's Day", "Ideal for a football fan's bedroom, office or bar"], key, "g"),
        "Full-colour print of the artwork"]
    close = pick(["Following more than one team? We make team posters for clubs across Europe – custom designs on request on 01439 771468.",
                  "Pair it with a football mug or bar mat for a matching gift. Custom designs are available on request – call 01439 771468."], key, "c")
    disc = football_disc([esc(club)], international=True)
    body = assemble(opening, h2, detail, bullets, items, pick(DELIVERY, key, "dl"), close, disc)
    seo = f"{club} Football Team Poster | Foxy Printing"
    if len(seo) > 60:
        seo = f"{club} Football Team Poster"
    meta = fit_meta([
        f"Fan-made {club} football team poster, printed to order in North Yorkshire. Choose print only or a Premium Display frame. A great gift for any fan.",
        f"Football team wall art for {club} supporters. Printed to order in our North Yorkshire workshop, print only or framed. A thoughtful gift.",
    ], key, [" Order today.", " UK made.", " Fun gift."])
    return body, seo, meta, None, []


# ------------------------------------------------------------------ football / sport player and squad posters

COUNTRIES = {"England": "the FA", "Argentina": "the Argentine Football Association", "Spain": "the Royal Spanish Football Federation"}


def subject_of(title):
    t = fix_q(title)
    head = re.split(r"\s+[–-]\s+", t)[0]
    head = re.sub(r"\s*\b(Football )?(Poster Print|Poster|Print)\b.*$", "", head).strip()
    for _ in range(4):
        head = re.sub(r"\s+(England|Argentina|Spain|Wolves|Liverpool FC|Newcastle United|Tribute|World Cup Champions 20\d\d|Football)$", "", head).strip()
    return head


def entities_from_title(t):
    """clubs / national teams named in the title (for the disclaimer and copy)"""
    t = fix_q(t)
    found = []
    pats = [("Liverpool FC Women", r"Liverpool FC Women"), ("Liverpool FC", r"\bLiverpool\b"),
            ("Manchester United", r"Man(chester)? (Utd|United)"), ("Manchester City", r"Man(chester)? City"),
            ("Chelsea", r"\bChelsea\b"), ("Arsenal", r"\bArsenal\b"), ("Gotham FC", r"Gotham FC"),
            ("Wolverhampton Wanderers", r"Wolverhampton Wanderers|\bWolves\b"), ("Newcastle United", r"Newcastle"),
            ("Aston Villa", r"Aston Villa"), ("Tottenham Hotspur", r"Tottenham|\bSpurs\b"), ("Rangers FC", r"\bRangers\b"),
            ("England", r"\bEngland\b|Lioness"), ("Argentina", r"\bArgentina\b"), ("Spain", r"\bSpain\b"),
            ("Norway", r"\bNorway\b"), ("Mexico", r"\bMexico\b")]
    for name, rx in pats:
        if re.search(rx, t, re.I) and name not in found:
            if name == "Liverpool FC" and "Liverpool FC Women" in found:
                continue
            found.append(name)
    return found


LFC2020 = {"Virgil Van Dijk": "Virgil van Dijk", "Klopp": "Jürgen Klopp", "Henderson": "Jordan Henderson", "Firmino": "Roberto Firmino",
           "Sadio Mane": "Sadio Mané", "Robertson Mane": "Robertson and Mané"}

EXTRA = {
    "sport": ["It's a lovely way to celebrate a favourite team or player, whether they're a current star or a legend from years gone by. Hang it in a bedroom, games room, office or man cave, or wrap it up for a birthday or Christmas.",
              "Fans of all ages love seeing their heroes on the wall. It makes a simple, thoughtful present for a birthday, Christmas, Father's Day or a big match day, and it brightens up any bedroom, den or office.",
              "Whether they never miss a game or just love a big moment, a print like this is an easy way to show it. It suits a bedroom, games room, office or bar area and makes a handy gift for any sports fan."],
    "film": ["It's a great way to show off a favourite film, whether you watch it every Halloween or all year round. Hang it in a den, home cinema, bedroom or games room, or wrap it up for a horror fan's birthday.",
             "Horror fans love a bit of menace on the wall, and a classic poster is an easy way to add it. It suits a home cinema, den or bedroom and makes a simple, thoughtful gift.",
             "Whether it's a cult classic or a newer sequel, a print like this is an easy way to show off your taste in films. It brightens up any den, games room or home cinema."],
}


def add_extra(body, group, key):
    if words(body) >= 185:
        return body
    para = pick(EXTRA[group], key, "extra")
    return re.sub(r"(</h2>\n<p>.*?</p>)", lambda m: m.group(1) + "\n<p>" + para + "</p>", body, count=1, flags=re.S)


def player_poster(p, kind):
    t = fix_q(p["title"])
    key = p["handle"]
    old = text(p["descriptionHtml"])
    name = subject_of(t)
    lfc = re.match(r"Champions of England Liverpool (.+?) Poster Print 2020", t)
    if lfc:
        name = LFC2020.get(lfc.group(1), lfc.group(1))
    ents = entities_from_title(t) if not lfc else ["Liverpool FC"]
    signed = bool(re.search(r"signature|signed|autograph", t + " " + old, re.I))
    women = bool(re.search(r"Lioness|Women", t))
    m26 = re.search(r"(Mexico|Norway|Argentina) vs England 2026", t)
    wc = "World Cup" in t
    team_word = "England" if "England" in ents else (ents[0] if ents else "their team")
    nat = [c for c in ents if c in ("England", "Argentina", "Spain")]
    if kind == "darts":
        name = re.sub(r"\s+Darts$", "", name)
        nick = re.search(r"(The Iceman|The Ferret|Cool Hand Luke|The Nuke|MVG|The Bullet)", t)
        e = dict(name=esc(name), nick=esc(nick.group(1)) if nick else "")
        opening = pick([
            "Our {name} darts poster is made for the fan who never misses a big night on the oche. It's a fan-made print with a printed signature-style graphic, made to order in North Yorkshire.",
            "Put a darts favourite on the wall with this {name} darts poster. It's our own fan-made print with a printed signature-style design, ready for a games room, bar or man cave.",
            "Looking for a gift for a darts fan? This {name} darts poster is a fan-made print with a printed signature-style graphic, printed in-house in North Yorkshire.",
        ], key, "o").format(**e)
        h2 = pick(["{name} darts poster print", "Darts poster of {name} with printed signature-style design"], key, "h").format(**e)
        lead = pick(["The design shows {name}" + (", '{nick}'," if nick else "") + " in action with a printed signature-style graphic and a player profile panel.",
                     "You get a full-colour print of {name}" + (" ('{nick}')" if nick else "") + " with a player profile panel and a signature-style graphic printed as part of the artwork."], key, "d").format(**e)
        gift = pick(["A great gift for a darts fan's birthday, Christmas or the World Darts Championship", "Ideal for a games room, home bar or practice area next to the board"], key, "g")
        disc = (SIGNED + "This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, "
                "or affiliated with " + esc(name) + ", the PDC or any darts organisation, tournament or player. Names are used only to describe "
                "the design and who it's for. All trademarks belong to their respective owners.")
        seo = f"{name} Darts Poster Print | Foxy Printing"
        metas = [f"Darts wall art of {name} with a printed signature-style design. A fan-made print, made to order in North Yorkshire. A great gift for a darts fan.",
                 f"Fan-made {name} darts poster with a printed signature-style graphic. Printed to order in North Yorkshire. Ideal for a games room or home bar."]
        close = pick(["Pair it with another player from our darts poster range, or a darts bar mat for the games room. Custom designs on request – call 01439 771468.",
                      "Collecting darts prints? Browse our other darts posters to build a matching wall. Custom designs on request – call 01439 771468."], key, "c")
    else:
        e = dict(name=esc(name), team=esc(team_word))
        who = "player" if not re.search(r"goalkeeper", t, re.I) else "goalkeeper"
        sig_phr = " with a printed signature-style design" if signed else ""
        if women:
            opening = pick([
                "Celebrate one of the stars of the women's game with our {name} football poster. It's a fan-made print" + sig_phr + ", made to order in North Yorkshire – a lovely gift for a young fan.",
                "Our {name} football poster is made for fans of the women's game, from first-time supporters to season-ticket holders. It's a fan-made print" + sig_phr + ", printed in-house in North Yorkshire.",
                "Looking for a gift for a girl or boy who loves women's football? This {name} poster is a fan-made print" + sig_phr + ", ready for a bedroom wall.",
            ], key, "o").format(**e)
        else:
            opening = pick([
                "Give a football fan something to smile about with our {name} football poster. It's a fan-made print" + sig_phr + ", made to order here in North Yorkshire.",
                "Our {name} football poster is a simple way to show who you follow. It's our own fan-made print" + sig_phr + ", and an easy gift for any football fan.",
                "Looking for a present for a football fan? This {name} football poster is a fan-made print" + sig_phr + ", printed in-house in North Yorkshire and ready for the wall.",
            ], key, "o").format(**e)
        h2 = pick(["{name} football poster print", "{name} football poster for fans", "Football poster of {name}"], key, "h").format(**e)
        if m26:
            lead = f"The design celebrates {esc(name)} with match-day imagery inspired by {esc(m26.group(0).replace(' 2026', ''))} at the 2026 World Cup"
        elif wc:
            lead = f"The design celebrates {esc(name)} with imagery inspired by the 2026 World Cup"
        elif lfc:
            lead = f"The design celebrates {esc(name)} and Liverpool FC's 2020 title win as Champions of England"
        elif "Tribute" in t:
            lead = f"It's a tribute design celebrating {esc(name)}" + (f" in the colours of {esc(ents[0])}" if ents and ents[0] not in nat else "")
        else:
            lead = f"The design shows {esc(name)}" + (f", {esc(join_and(ents))}" if ents else "")
        lead += (", with the signature printed as part of the artwork." if signed else ".")
        gift = pick(["A great gift for a birthday, Christmas or a big match day", "Ideal for a bedroom, games room, office or man cave",
                     "A thoughtful present for a fan of any age"], key, "g")
        clubs_named = [c for c in ents if c not in ("Norway", "Mexico")]
        disc = football_disc([esc(name)] + [esc(c if c not in COUNTRIES else COUNTRIES[c]) for c in clubs_named],
                             international=bool(nat), signed=signed)
        seo = f"{name} Football Poster Print | Foxy Printing"
        metas = [f"Fan-made {name} football poster" + (" with a printed signature-style design" if signed else "") + ". Printed to order in North Yorkshire, a great gift for any football fan.",
                 f"Football wall art of {name}, printed to order in our North Yorkshire workshop. A fan-made print and an easy birthday or Christmas gift."]
        close = pick(["Pair it with another player from our football poster range for a matching wall. Custom designs on request – call 01439 771468.",
                      "Want a different player? Custom designs are available on request – call 01439 771468.",
                      "Make it a set with more prints from our football poster range, or call 01439 771468 about a custom design."], key, "c")
    sent, sbl, items, fr = size_block(p, key)
    detail = lead + " " + sent + (" " + pick(FRAME_LINE, key, "f") if fr else "")
    if signed:
        detail += " Please note it's a reproduction print: the signature is printed on, not hand-written."
    bullets = [pick(MADE, key, "m"), ("Honest reproduction print: the signature is part of the printed design" if signed else
                                       "Our own fan-made design, printed in full colour")] + sbl + [gift,
               pick(["Fits standard A-size frames if you'd like to frame it yourself", "Bright, full-colour print of the artwork"], key, "b5")]
    body = assemble(opening, h2, detail, bullets, items, pick(DELIVERY, key, "dl"), close, disc)
    if len(seo) > 60:
        seo = seo.replace(" | Foxy Printing", "")
    meta = fit_meta(metas, key, [" Order today.", " UK made.", " Great gift."])
    return body, seo, meta, clean_title(p["title"]), []


def squad_poster(p):
    t = fix_q(p["title"])
    key = p["handle"]
    old = text(p["descriptionHtml"])
    feat = re.search(r"Featuring (.+?)(?:\s+[–-]\s+|$)", t)
    people = []
    if feat:
        people = [x.strip() for x in re.split(r",|&| and ", feat.group(1)) if x.strip()]
    elif "Rashford" in t:
        people = ["Ollie Watkins", "Emiliano Martinez", "Marcus Rashford"]
    elif "Arteta" in old:
        people = []
    m = re.match(r"(.+?)\s+(?:FC |AFC )?(?:Team|Poster|Premier|Europa)", t)
    club = re.sub(r"\s+(FC|AFC)$", "", m.group(1)).strip() if m else subject_of(t)
    club = {"AFC Bournemouth": "AFC Bournemouth", "Tottenham": "Tottenham Hotspur", "Aston Villa FC": "Aston Villa"}.get(club, club)
    season = "2026"
    if "Europa League Champions 2025" in t:
        what, season = "2025 Europa League win", "2025"
    elif "Europa League Winners 2026" in t:
        what = "2026 Europa League win"
    elif "Premier League Champions 2026" in t:
        what = "2026 Premier League title"
    elif "Team Collage" in t:
        what = "team"
    else:
        what = "2026 squad"
    signed = bool(re.search(r"signature", t + " " + old, re.I))
    e = dict(club=esc(club), what=esc(what), people=esc(join_and(people)) if people else "")
    opening = pick([
        "Celebrate {club}'s {what} with this fan-made football poster, printed to order in our North Yorkshire workshop. It's an easy birthday or Christmas gift for any supporter.",
        "Our {club} football poster puts the {what} on the wall in one bold collage. It's our own fan-made print, made to order in North Yorkshire.",
        "Looking for a gift for a {club} supporter? This fan-made football poster celebrating the {what} is printed in-house in North Yorkshire and ready for a bedroom, office or man cave.",
    ], key, "o").format(**e)
    h2 = pick(["{club} football poster: {what}", "{club} {what} football poster", "Football poster for {club} fans"], key, "h").format(**e)
    h2 = h2[:1].upper() + h2[1:]
    lead = ("It's a full-colour collage of team, match-day and supporter images" + (", featuring " + e["people"] if people else "") +
            (", with signature-style graphics printed as part of the artwork." if signed else "."))
    sent, sbl, items, fr = size_block(p, key)
    detail = lead + " " + sent + (" " + pick(FRAME_LINE, key, "f") if fr else "")
    if signed:
        detail += " Any signatures are printed reproductions, not hand-written."
    bullets = [pick(MADE, key, "m"), "Packed collage design with team, match-day and supporter images"] + sbl + [
        pick(["A great gift for a birthday, Christmas or the end of the season", "Ideal for a bedroom, office, bar or man cave"], key, "g"),
        pick(["Fits standard A-size frames if you'd like to frame it yourself", "Bright, full-colour print of the artwork"], key, "b5")]
    close = pick(["Pair it with a football mug or bar mat for a matching gift. Custom designs are available on request – call 01439 771468.",
                  "Want a different club or season? Custom designs on request – call 01439 771468."], key, "c")
    names = [esc(club)] + [esc(x) for x in people]
    disc = football_disc(names, international="Europa" in t, signed=signed)
    body = assemble(opening, h2, detail, bullets, items, pick(DELIVERY, key, "dl"), close, disc)
    yr = (" " + season) if season in t else ""
    seo = f"{club} Football Poster{yr} | Foxy Printing"
    if len(seo) > 60:
        seo = f"{club} Football Poster{yr}"
    meta = fit_meta([f"Fan-made {club} football poster celebrating the {what}. Printed to order in North Yorkshire. A great gift for any supporter.",
                     f"Celebrate the {what} with this fan-made {club} football poster, printed to order in our North Yorkshire workshop."],
                    key, [" Order today.", " UK made.", " Great gift."])
    return body, seo, meta, clean_title(p["title"]), []


def f1_poster(p):
    t = p["title"]
    key = p["handle"]
    old = text(p["descriptionHtml"])
    race = re.match(r"(.+?Grand Prix)", t).group(1).replace(" Podium", "")
    m = re.search(r"winner ([A-Z][\w ]+?)\s*,\s*alongside ([A-Z][\w ]+?) and ([A-Z][\w ]+?)\s*,", old)
    drivers = [m.group(1), m.group(2), m.group(3)] if m else []
    e = dict(race=esc(race), d=esc(join_and(drivers)))
    opening = pick([
        "Relive the 2026 {race} with this fan-made podium poster, printed to order in our North Yorkshire workshop. It's a great gift for any motorsport fan.",
        "Our 2026 {race} podium poster is made for the fan who never misses a race weekend. It's our own fan-made print, made to order in North Yorkshire.",
    ], key, "o").format(**e)
    h2 = "2026 {race} podium poster".format(**e)
    lead = ("The design is a collage of race-day and podium images" + (", featuring " + e["d"] if drivers else "") +
            ", with signature-style graphics printed as part of the artwork.")
    sent, sbl, items, fr = size_block(p, key)
    detail = lead + " " + sent + " Any signatures are printed reproductions, not hand-written."
    bullets = [pick(MADE, key, "m"), "Podium collage design celebrating one race weekend"] + sbl + [
        "A great gift for a motorsport fan's birthday or Christmas", "Ideal for a garage, games room, office or bedroom"]
    close = "Collecting race posters? Browse our other motorsport prints, or call 01439 771468 about a custom design."
    disc = (SIGNED + "This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or "
            "affiliated with " + (e["d"] + ", " if drivers else "") + "Formula 1, the FIA, any racing team or driver, or the organisers of the " + e["race"] +
            ". Names are used only to describe the design and who it's for. All trademarks belong to their respective owners.")
    body = assemble(opening, h2, detail, bullets, items, pick(DELIVERY, key, "dl"), close, disc)
    seo = f"2026 {race} Podium Poster | Foxy Printing"
    if len(seo) > 60:
        seo = f"2026 {race} Podium Poster"
    meta = fit_meta([f"Fan-made motorsport poster of the 2026 {race} podium, printed to order in North Yorkshire. A great gift for any racing fan."],
                    key, [" Order today.", " UK made.", " Great gift."])
    return body, seo, meta, clean_title(t), []


def boxing_poster(p):
    t = p["title"]
    key = p["handle"]
    fight2 = "Fight 2" in t
    e = dict(f="Conor Benn vs Chris Eubank Jr" + (" fight 2" if fight2 else ""))
    opening = pick(["Relive {f} with this fan-made printed signature collage poster, made to order in our North Yorkshire workshop. It's a great gift for any boxing fan.",
                    "Our {f} collage poster is made for fight fans who were glued to every round. It's a fan-made print with printed signatures, made to order in North Yorkshire."],
                   key, "o").format(**e)
    h2 = "{f} printed signature poster".format(**e)
    h2 = h2[:1].upper() + h2[1:]
    sent, sbl, items, fr = size_block(p, key)
    detail = ("The design is a collage of fight-night images – face-offs, in-ring action and the big moments – with the fighters' signatures printed as part of the artwork. "
              + sent + " Please note it's a reproduction print: the signatures are printed on, not hand-written.")
    bullets = [pick(MADE, key, "m"), "Honest reproduction print: the signatures are part of the printed design"] + sbl + [
        "A great gift for a boxing fan's birthday, Christmas or fight night", "Ideal for a gym, games room, office or man cave"]
    close = "Pair it with our boxing face masks for a fight-night party. Custom designs on request – call 01439 771468."
    disc = (SIGNED.replace("The signature is", "The signatures are").replace("it is not hand-signed and is not an original autograph",
                                                                             "they are not hand-signed and are not original autographs")
            + "This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or affiliated with "
            "Conor Benn, Chris Eubank Jr, or any boxing promoter, broadcaster, sanctioning body or venue. Names are used only to describe the design "
            "and who it's for. All trademarks belong to their respective owners.")
    body = assemble(opening, h2, detail, bullets, items, pick(DELIVERY, key, "dl"), close, disc)
    seo = ("Benn vs Eubank Jr Fight 2 Boxing Poster | Foxy Printing" if fight2 else "Benn vs Eubank Jr Boxing Poster | Foxy Printing")
    meta = fit_meta([f"Fan-made boxing poster of {e['f']} with printed signatures. Printed to order in North Yorkshire. A great gift for a fight fan."],
                    key, [" Order today.", " UK made.", " Great gift."])
    return body, seo, meta, clean_title(t), []


# ------------------------------------------------------------------ horror film posters and sets

def film_poster(p):
    t = p["title"]
    key = p["handle"]
    old = text(p["descriptionHtml"])
    franchise = "Friday the 13th" if t.startswith("Friday") else ("Halloween" if t.startswith("Halloween") else "Batman")
    film = re.split(r"\s+[–-]\s+", t)[0]
    film = re.sub(r"\s*\b(Movie )?(Poster Prints?|Poster|Print)\b.*$", "", film).strip()
    is_set = bool(re.search(r"Set of 6", t))
    if is_set:
        film = franchise
    year = re.search(r"\((19|20)\d\d\)", film)
    e = dict(film=esc(film), fr=esc(franchise))
    if franchise == "Batman":
        return lego_batman(p)
    if is_set:
        opening = pick(["Our {fr} poster print set gives a horror fan six classic-style designs in one go, ready for a gallery wall. Each one is a fan print, made to order in North Yorkshire.",
                        "Build a horror wall in one go with this set of six {fr} poster prints, printed to order in our North Yorkshire workshop."], key, "o").format(**e)
        h2 = "{fr} poster print set of 6".format(**e)
        lead = "You get six different poster designs inspired by films in the " + e["fr"] + " series, printed in full colour as a matching set."
    else:
        opening = pick(["Our {film} poster print is made for horror fans who love a classic slasher. It's a fan print, made to order here in North Yorkshire.",
                        "Give a horror fan's wall some menace with this {film} poster print, printed to order in our North Yorkshire workshop.",
                        "Looking for a gift for a horror film fan? This {film} poster print is ready for a den, home cinema or bedroom wall."], key, "o").format(**e)
        h2 = pick(["{film} poster print", "{film} horror movie poster print"], key, "h").format(**e)
        feat = re.search(r"Featuring (the )?(.+?), this", old)
        lead = "The print shows the poster artwork for " + e["film"] + (", " + esc(feat.group(2)).rstrip(".") if feat and len(feat.group(2)) < 110 else "") + "."
    sent, sbl, items, fr = size_block(p, key)
    detail = lead + " " + sent + (" " + pick(FRAME_LINE, key, "f") if fr else "")
    bullets = [pick(MADE, key, "m"), ("Six designs that work together as a gallery wall" if is_set else "Full-colour print of the classic poster artwork")] + sbl + [
        pick(["A great gift for a horror fan's birthday, Christmas or Halloween", "Ideal for a den, home cinema, bedroom or games room"], key, "g"),
        "Great for Halloween decorating, or all year round"]
    close = pick(["Pair it with more prints from our horror range for a full movie wall. Custom designs on request – call 01439 771468.",
                  "Planning a Halloween party? Add a few of our horror face masks. Custom designs on request – call 01439 771468."], key, "c")
    disc = ("This is an unofficial design inspired by " + e["fr"] + ". It is not official merchandise and is not endorsed by, sponsored by, or connected with "
            + e["fr"] + ", the film's studio, distributors or rights holders, or any of their licensees. All names, characters and trademarks belong to their respective owners.")
    body = assemble(opening, h2, detail, bullets, items, pick(DELIVERY, key, "dl"), close, disc)
    seo = (f"{franchise} Horror Poster Print Set of 6 | Foxy Printing" if is_set else f"{film} Horror Poster Print | Foxy Printing")
    if len(seo) > 60:
        seo = seo.replace(" | Foxy Printing", "").replace(" Horror", "")
    meta = fit_meta([f"Horror movie wall art inspired by {film}" + (": six poster prints in one set." if is_set else ".") +
                     " Printed to order in North Yorkshire. A great gift for any horror fan.",
                     f"Classic slasher poster print inspired by {film}, printed to order in our North Yorkshire workshop. Ideal for a den or home cinema."],
                    key, [" Order today.", " UK made.", " Great gift."])
    return body, seo, meta, clean_title(t), []


def lego_batman(p):
    key = p["handle"]
    opening = "This Batman-themed brick-style superhero poster brings a bit of Gotham City to a kids' bedroom, playroom or games room. It's a fan print, made to order in our North Yorkshire workshop."
    h2 = "Brick-style superhero poster print for kids' rooms"
    sent, sbl, items, fr = size_block(p, key)
    detail = ("The print shows the brick-built caped hero against a city skyline, inspired by Legacy of the Dark Knight, in bright full colour. " + sent +
              (" " + pick(FRAME_LINE, key, "f") if fr else ""))
    bullets = [pick(MADE, key, "m"), "Bright, full-colour superhero artwork", "Ideal for a kids' bedroom, playroom or games room"] + sbl + [
        "A fun birthday or Christmas present for a young superhero fan", "Fits standard A-size frames if you'd like to frame it yourself"]
    close = "Pair it with more prints from our film and TV range for a superhero wall. Custom designs on request – call 01439 771468."
    disc = ("This is an unofficial design inspired by LEGO Batman. It is not official merchandise and is not endorsed by, sponsored by, or connected with "
            "the LEGO Group, DC Comics, Warner Bros. or any of their licensees. All names, characters and trademarks belong to their respective owners.")
    body = assemble(opening, h2, detail, bullets, items, pick(DELIVERY, key, "dl"), close, disc)
    seo = "Superhero Brick-Style Poster for Kids' Rooms | Foxy Printing"
    meta = fit_meta(["Bright superhero wall art for a kids' bedroom or playroom, inspired by LEGO Batman. Printed to order in North Yorkshire. A fun gift."],
                    key, [" Order today.", " UK made."])
    title = "Batman Superhero Poster Print – Brick-Style Wall Art for Kids' Room, Bedroom, Playroom & Game Room"
    return body, seo, meta, title, []


def stadium_set(p):
    key = p["handle"]
    st = ["Wembley Stadium", "Allianz Arena", "Estadio Azteca", "Camp Nou", "Santiago Bernabéu", "La Bombonera"]
    opening = ("Our vintage football stadium poster print set brings six of the world's great grounds to one wall – a lovely gift for a football fan "
               "who loves the history of the game. Each print is made to order in our North Yorkshire workshop.")
    h2 = "Vintage football stadium poster print set of 6"
    vals = [v for o in p["options"] for v in o["values"]]
    sizes = [s for s in ["A6", "A5", "A4", "A3"] if any(s in v for v in vals)]
    detail = ("You get six vintage-style illustrated stadium prints: " + esc(join_and(st)) + ". Choose " + join_or(sizes) +
              " for the whole set, so they hang together as a matching gallery wall.")
    bullets = [pick(MADE, key, "m"), "Six vintage-style stadium illustrations that work as a set",
               f"Choose {join_or(sizes)} for the whole set", "Ideal for a bedroom, office, games room or bar area",
               "A thoughtful gift for a football fan who loves a groundhop"]
    items = [f"{s}: {DIMS[s]} per print" for s in sizes] + ["Prints in the set: 6", "Print only (no frames)"]
    close = "Pair the set with a football bar mat or mug for a ready-made gift. Custom designs on request – call 01439 771468."
    disc = ("This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or affiliated with "
            "the owners or operators of " + esc(join_and(st)) + ", or any football club, league or governing body. Stadium names are used only to describe "
            "the design. All trademarks belong to their respective owners.")
    body = assemble(opening, h2, detail, bullets, items, pick(DELIVERY, key, "dl"), close, disc)
    seo = "Vintage Football Stadium Poster Set of 6 | Foxy Printing"
    meta = fit_meta(["Six vintage-style football stadium prints in one set, from A6 to A3. Printed to order in North Yorkshire. A great gift for any football fan."],
                    key, [" Order today.", " UK made."])
    return body, seo, meta, None, []


def fight_display(p):
    key = p["handle"]
    opening = ("Remember the night Conor Benn and Chris Eubank Jr finally met with this framed fight-night photo display from 26 April 2025 at Tottenham "
               "Hotspur Stadium. It's a fan-made display, made in-house in North Yorkshire, and a great gift for any boxing fan.")
    h2 = "Benn vs Eubank Jr framed fight night photo display"
    detail = ("The display commemorates the 26 April 2025 fight with fight-night photography and the event details. Choose an A4 or A3 display, then pick "
              "your frame finish: Matt Black, Brushed Silver, Gloss White or Metallic Gold. Every display comes in one of our Premium Display frames – "
              "thick, chunky and very professional, not a cheap thin frame.")
    bullets = [pick(MADE, key, "m"), "Supplied framed, ready to display", "Four frame finishes: Matt Black, Brushed Silver, Gloss White or Metallic Gold",
               "Two sizes: A4 or A3", "A great gift for a boxing fan's birthday, Christmas or fight night"]
    items = ["A4: 210 x 297 mm, framed", "A3: 297 x 420 mm, framed", "Frame finishes: Matt Black, Brushed Silver, Gloss White, Metallic Gold"]
    close = "Pair it with our boxing face masks for a fight-night party. Custom designs on request – call 01439 771468."
    disc = ("This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or affiliated with "
            "Conor Benn, Chris Eubank Jr, Tottenham Hotspur Stadium, or any boxing promoter, broadcaster or sanctioning body. Names are used only "
            "to describe the design and who it's for. All trademarks belong to their respective owners.")
    body = assemble(opening, h2, detail, bullets, items, "Each display is made to order in our North Yorkshire workshop. Postage options and costs are shown at checkout.", close, disc)
    seo = "Benn vs Eubank Jr Framed Fight Night Display | Foxy Printing"
    meta = fit_meta(["Framed fan-made fight night display of Benn vs Eubank Jr, 26 April 2025. A4 or A3 in four frame finishes. Made in North Yorkshire."],
                    key, [" Order today.", " Great gift."])
    title = "Conor Benn vs Chris Eubank Jr Fight Night Framed Photo Display – 26 April 2025 – Boxing Fan Gift"
    return body, seo, meta, title, []


# ------------------------------------------------------------------ face masks

MASK_HOW = [
    "Each {pk} is digitally printed in full colour on 350gsm silk card. Choose Ready Cut and we cut it to the shape of the face and cut out the eye holes for you, or choose DIY and it comes printed only, for you to cut out at home.",
    "We print this mask in full colour on thick 350gsm silk card. Ready Cut masks arrive cut to shape with the eye holes cut; DIY masks are printed only, so you cut them out yourself and save a little.",
    "Printed in full colour on 350gsm silk card, the mask comes in two styles: Ready Cut (cut to the face shape with the eye holes cut) or DIY (printed only, for you to cut out).",
]
MASK_FIT = "Then pick your fitting: elastic and sticky tabs, or a stick and stickers for a hand-held mask, supplied for you to attach."


def mask_name(p):
    t = p["title"]
    name = re.split(r"\s+(?:Face Mask|Film Character|Black Eye Face Mask|20\d\d)\b|\s+[–-]\s+", t)[0].strip()
    return name


def mask_group(p, name):
    old = text(p["descriptionHtml"])
    m = re.search(re.escape(name) + r"\s*\(([^)]{2,30})\)", old)
    if m:
        return m.group(1).strip()
    m = re.search(r"(ENHYPEN|SEVENTEEN|TXT|TOMORROW X TOGETHER|ATEEZ|BLACKPINK|NewJeans|LE SSERAFIM|aespa|KATSEYE|BOYNEXTDOOR|"
                  r"TWS|Hearts2Hearts|xikers|Sidemen|BABYMONSTER|ILLIT|tripleS|KiiiKiii|izna|MEOVV)", old)
    return m.group(1) if m else None


def single_mask(p):
    key = p["handle"]
    tags = " ".join(p["tags"])
    name = mask_name(p)
    if name == "Mr Who's The Boss":
        name = "Mrwhosetheboss"
    if name == "Harry" and "sidemen" in key:
        name = "Harry (Sidemen)"
    if name == "Mr Beast":
        name = "MrBeast"
    if name == "Pewdiepie":
        name = "PewDiePie"
    design = ""
    m = re.match(r"(Stokes Twins) (\d)$", name)
    if m:
        name, design = m.group(1), m.group(2)
    group = mask_group(p, re.sub(r"\s*\(.*\)", "", name))
    bare = re.sub(r"\s*\(.*\)", "", name)
    black_eye = "Black Eye" in p["title"]
    if "kpop-masks" in tags:
        kind, who, occ = "K-pop star", "K-pop fans", ["a concert pre-party", "a fan meet-up", "a K-pop themed birthday", "a karaoke night"]
    elif "mask-golf" in tags:
        kind, who, occ = "golf YouTuber", "golf fans", ["a golf society day", "a 19th-hole celebration", "a golf-themed birthday"]
    elif "mask-boxing" in tags:
        kind, who, occ = "YouTuber and boxer", "fight fans", ["a fight-night watch party", "a boxing-themed stag do", "a big-fight sweepstake night"]
    elif "youtuber-masks" in tags:
        kind, who, occ = "YouTuber", "online video fans", ["a gaming-themed birthday", "a sleepover party", "a stag or hen do", "a YouTube watch party"]
    elif "mask-film-stars" in tags:
        kind, who, occ = "film star", "film fans", ["a movie night", "an Oscars-style party", "a themed birthday"]
    else:
        kind, who, occ = "famous face", "anyone planning a party", ["a birthday party", "a stag or hen do", "a wedding photo booth"]
    o1, o2 = pick(occ, key, "o1"), pick(occ[::-1], key, "o2")
    if o1 == o2:
        o2 = "a fancy dress night out"
    pk = f"{bare} face mask" if not black_eye else f"{bare} black eye face mask"
    gtxt = f" from {group}" if group and group != "Sidemen" else (" of the Sidemen" if group == "Sidemen" else "")
    e = dict(pk=esc(pk), name=esc(bare), g=esc(gtxt), o1=o1, o2=o2, who=who, kind=kind)
    opening = pick([
        "Our {pk} is a quick way to get everyone laughing at {o1}, and it's a fun surprise for {who}. It shows {name}{g} printed on sturdy card.",
        "Bring a famous face to {o1} with this {pk}. It's a favourite with {who}, and it posts flat, so it's easy to send as a gift.",
        "Planning {o1}? This {pk}{g} is the easy fancy dress win for {who}.",
        "Turn heads at {o1} with a {pk} made for photos, laughs and a bit of mischief. {who_cap} love it.",
    ], key, "intro").replace("{who_cap}", who[:1].upper() + who[1:]).format(**e)
    if black_eye:
        opening = ("Our {pk} shows the {kind} with a cartoon-style shiner, so it's a cheeky pick for {o1} or {o2}. It posts flat, so it's an easy gift for {who}.").format(**e)
    h2 = pick(["{name} face mask for parties", "{name} card face mask", "{name} fancy dress face mask"], key, "h2").format(**e)
    if black_eye:
        h2 = "{name} black eye face mask".format(**e)
    how = pick(MASK_HOW, key, "how").format(pk=esc(pk)) + " " + MASK_FIT
    custom = pick(["Want a mask of someone who isn't in our range, like the birthday boy or the bride-to-be? We can make one from your photo.",
                   "Need a face we don't stock, such as the groom or a friend? Send us a photo and we'll make a custom mask.",
                   "Can't find the face you need? We also make custom masks from your own photo."], key, "custom")
    pool = ["Thick 350gsm silk card holds its shape all night",
            "Semi-waterproof finish, so it copes with spilt drinks and outdoor parties",
            "Ready Cut or DIY, with elastic or a stick supplied for you to attach",
            "Full-colour digital print for a sharp, recognisable face",
            "Posted flat in a board-backed envelope to keep it crease-free",
            "Full A4 size (297 x 210 mm), big enough to cover an adult face",
            f"An easy, cheap way to theme {o1}",
            "Brilliant for photo booths and group shots"]
    start = int(hashlib.md5((key + "b").encode()).hexdigest(), 16) % len(pool)
    bullets = [pool[(start + i) % len(pool)] for i in range(5)]
    items = ["Size: 297 x 210 mm (A4), a full adult-size face", "Material: 350gsm silk card, full-colour digital print",
             "Finish: semi-waterproof", "Style: Ready Cut (cut to shape, eye holes cut) or DIY (printed only)",
             "Fitting: elastic and sticky tabs, or a stick and stickers, supplied for you to attach", "Packaging: board-backed envelope"]
    close = pick([f"Order one for {o2}, or buy a few so the whole group can turn up as {esc(bare)}.",
                  f"A {esc(pk)} is a cheap and cheerful way to make {o2} one to remember.",
                  f"Grab a {esc(pk)} for {o2} and get the camera ready."], key, "close")
    disc = ("This is an unofficial novelty product made for fun and fancy dress. " + esc(bare) + " has not endorsed, sponsored or approved this product, "
            "and Foxy Printing has no connection with them. The name is used only to describe the design.")
    if group and group != "Sidemen":
        disc += (" It is also an unofficial fan design, not endorsed by or connected with " + esc(group) +
                 ", their management or record label. All names and trademarks belong to their respective owners.")
    elif group == "Sidemen":
        disc += " It is not endorsed by or connected with the Sidemen. All names and trademarks belong to their respective owners."
    body = "\n".join([f"<p>{opening}</p>", f"<h2>{h2}</h2>", f"<p>{esc(how)} {custom}</p>",
                      "<h3>Why you'll love it</h3>", "<ul>\n" + "\n".join(f"<li>{esc(b)}</li>" for b in bullets) + "\n</ul>",
                      "<h3>Size &amp; details</h3>", "<ul>\n" + "\n".join(f"<li>{i}</li>" for i in items) + "\n</ul>",
                      "<h3>Delivery</h3>", "<p>Printed in our North Yorkshire workshop and posted to you in a board-backed envelope. Dispatch and postage options are shown at checkout.</p>",
                      f"<p>{close}</p>", "<h3>Please note</h3>", f'<p class="disclaimer">{disc}</p>'])
    seo = f"{bare} Face Mask | Foxy Printing" if not black_eye else f"{bare} Black Eye Face Mask | Foxy Printing"
    if design:
        seo = f"{bare} Face Mask Design {design} | Foxy Printing"
        h2 = h2 + f" (design {design})"
        body = body.replace(f"<h2>{h2[:-len(f' (design {design})')]}</h2>", f"<h2>{h2}</h2>")
    meta = fit_meta([f"Fancy dress made easy: a {bare} face mask on thick 350gsm card, Ready Cut or DIY, with elastic or a stick. Great for {o1}.",
                     f"Get the party started with a {bare} face mask. Full-colour print on 350gsm card, Ready Cut or DIY. Perfect for {o1}.",
                     f"{bare} card face mask for {o1}. Printed on 350gsm silk card, Ready Cut or DIY, with elastic or a stick."],
                    key, [" Posted flat.", " Order today.", " UK made.", " Fun for all."])
    title = clean_title(p["title"])
    body = re.sub(r"\b([Aa]) (?=[AEIOU])", r"\1n ", body)
    meta = re.sub(r"\b([Aa]) (?=[AEIOU])", r"\1n ", meta)
    return body, seo, meta, title, ([] if "third-party-name" in p["tags"] else ["third-party-name"])


# ------------------------------------------------------------------ one-offs

def top_gun(p):
    key = p["handle"]
    opening = ("Our Top Gun-inspired face mask pack gives you three famous flyboys in one go – perfect for an 80s night, a movie-themed birthday "
               "or a stag do that feels the need for speed.")
    h2 = "Top Gun-inspired face mask pack of 3"
    detail = ("The pack has three card face masks of Top Gun flyboys, including Tom Cruise as Maverick and Val Kilmer as Iceman – "
              "the photos show the full line-up. Each mask is printed in full colour on 350gsm card, cut to the shape of the face with the eye holes cut. "
              "Elastic and sticky tabs are supplied for you to attach in seconds.")
    bullets = ["Three masks in one pack, ready for a group costume", "Thick 350gsm card that holds its shape all night",
               "Cut to shape with the eye holes cut; elastic and sticky tabs supplied", "Semi-waterproof finish for parties indoors or out",
               "Brilliant for photo booths and 80s-themed parties"]
    items = ["Pack contents: 3 face masks", "Size: each mask is 297 x 210 mm (A4), a full adult-size face",
             "Material: 350gsm card, full-colour digital print, semi-waterproof", "Fitting: elastic and sticky tabs supplied for you to attach",
             "Packaging: board-backed envelope"]
    close = "Add some aviator sunglasses and you're ready for take-off."
    disc = ("This is an unofficial novelty product made for fun and fancy dress, inspired by Top Gun. It is not official merchandise and is not "
            "endorsed by, sponsored by, or connected with Top Gun, Paramount Pictures or any of their licensees. Tom Cruise, Val Kilmer and the other "
            "actors shown have not endorsed, sponsored or approved this product, and Foxy Printing has no connection with them. The names are used only to describe "
            "the design. All names, characters and trademarks belong to their respective owners.")
    body = assemble(opening, h2, detail, bullets, items,
                    "Printed in our North Yorkshire workshop and posted to you in a board-backed envelope. Dispatch and postage options are shown at checkout.",
                    close, disc)
    return body, "80s Movie Pilot Face Mask Pack of 3 | Foxy Printing", fit_meta(
        ["Three card face masks inspired by Top Gun, including Maverick and Iceman. Cut to shape with eye holes on thick 350gsm card. Great for 80s parties."],
        key, [" Order today."]), None, ["third-party-name"]


MANUAL = {}


def clean_title(t):
    t2 = re.sub(r"\s*[–-]\s*[^–-]*\b(Memorabilia|Collectible|Collector)\b[^–-]*$", "", t, flags=re.I)
    t2 = re.sub(r"\b(Autographed|Limited Edition)\s*", "", t2, flags=re.I)
    t2 = re.sub(r"\s*\bMemorabilia\b", "", t2, flags=re.I)
    t2 = re.sub(r"\s{2,}", " ", t2).strip(" –-")
    t2 = fix_q(t2)
    return t2 if t2 != t else None


def fit_meta(pool, key, pads):
    order = sorted(range(len(pool)), key=lambda i: hashlib.md5((key + str(i)).encode()).hexdigest())
    for i in order:
        s = pool[i]
        if 140 <= len(s) <= 155:
            return s
        for pd in pads:
            if 140 <= len(s + pd) <= 155:
                return s + pd
        for a in pads:
            for b in pads:
                if a != b and 140 <= len(s + a + b) <= 155:
                    return s + a + b
    s = pool[order[0]]
    if len(s) > 155:
        s = s[:152].rsplit(" ", 1)[0].rstrip(",.;:") + "."
    return s


def classify(p):
    t = p["title"]
    if "Tiny Men Big Balls" in t:
        return tmbb
    if "Football Team Printed Display Poster" in t:
        return team_display
    if re.search(r"face ?mask|Celebrity Mask|Cardboard Celebrity Mask", t, re.I) and "Pack" not in t and "Poster" not in t:
        return single_mask
    if t.startswith("Top Gun"):
        return top_gun
    if "Darts Poster" in t:
        return lambda q: player_poster(q, "darts")
    if "Grand Prix" in t:
        return f1_poster
    if t.startswith("Conor Benn") and "Display" in t:
        return fight_display
    if t.startswith("Conor Benn"):
        return boxing_poster
    if t.startswith(("Friday the 13th", "Halloween", "LEGO Batman")):
        return film_poster
    if t.startswith("Vintage Football Stadium"):
        return stadium_set
    if re.search(r"Team 2026|Team Poster 2026|Champions 20|Winners 2026|Team Collage|Rangers FC Fan Poster", t) and "World Cup Champions" not in t:
        return squad_poster if "Rangers" not in t else rangers
    if re.search(r"Poster|Print", t):
        return lambda q: player_poster(q, "football")
    return None


def rangers(p):
    key = p["handle"]
    opening = ("Show your support with our Rangers FC fan poster, a bold bit of football wall art for a bedroom, office, bar or man cave. "
               "It's a fan-made print, made to order in our North Yorkshire workshop.")
    h2 = "Rangers FC fan poster print"
    sent, sbl, items, fr = size_block(p, key)
    detail = "It's our own fan-made design for Rangers supporters, printed in full colour. " + sent + " Where framed options are offered, they come in our Premium Display frames – thick, chunky and very professional."
    bullets = [pick(MADE, key, "m"), "Bold, full-colour fan design for match-day pride", "A great gift for a birthday, Christmas or Father's Day",
               "Ideal for a bedroom, office, bar or man cave", "Fits standard A-size frames if you'd like to frame it yourself"]
    close = "Pair it with a football mug or bar mat for a matching gift. Custom designs on request – call 01439 771468."
    disc = football_disc(["Rangers FC", "the Scottish Professional Football League"])
    body = assemble(opening, h2, detail, bullets, items, pick(DELIVERY, key, "dl"), close, disc)
    return body, "Rangers FC Fan Football Poster | Foxy Printing", fit_meta(
        ["Fan-made Rangers FC football poster, printed to order in North Yorkshire. A bold bit of wall art and a great gift for any Rangers supporter."],
        key, [" Order today.", " UK made."]), None, []


# ------------------------------------------------------------------ checks

def problems(body, seo, meta):
    pr = []
    if body.count("<h2") != 1:
        pr.append("h2")
    if not body.rstrip().endswith("</p>") or '<p class="disclaimer">' not in body.split("<h3>Please note</h3>")[-1]:
        pr.append("disclaimer last")
    if re.search(r"style=|<span|<h1|<table|<br|<img", body):
        pr.append("html")
    nd = re.sub(r'<p class="disclaimer">.*?</p>', "", body, flags=re.S)
    m = BANNED.search(text(nd))
    if m and not re.search(r"signature", m.group(0), re.I):
        pr.append("banned:" + m.group(0))
    if re.search(r"\[|\]|\{|\}", body):
        pr.append("brackets")
    w = words(body)
    if not 180 <= w <= 350:
        pr.append(f"words {w}")
    if len(seo) > 60:
        pr.append(f"seo {len(seo)}")
    if not 140 <= len(meta) <= 155:
        pr.append(f"meta {len(meta)}")
    if BANNED.search(seo + " " + meta):
        pr.append("banned seo")
    return pr


def main(src, idfile, out):
    want = set(x.strip() for x in open(idfile) if x.strip())
    P = {}
    for line in open(src, encoding="utf-8"):
        o = json.loads(line)
        if "__parentId" in o:
            continue
        if o["id"] in want:
            P[o["id"]] = o
    os.makedirs(out, exist_ok=True)
    ups, rows, skipped, bad = [], [], [], []
    seen_seo, dup_seo = set(), []
    for pid, p in P.items():
        fn = classify(p)
        if not fn:
            skipped.append(p)
            continue
        body, seo, meta, title, tags = fn(p)
        body = re.sub(r"\b([Aa]) (?=(?!Eu)[AEIO])", r"\1n ", body)
        meta = re.sub(r"\b([Aa]) (?=(?!Eu)[AEIO])", r"\1n ", meta)
        if not re.search(r"face ?mask|Mask Pack|Facemask", p["title"], re.I):
            body = add_extra(body, "film" if p["title"].startswith(("Friday", "Halloween")) else "sport", p["handle"])
        pr = problems(body, seo, meta)
        if pr:
            bad.append((p["handle"], pr))
        if seo in seen_seo:
            kw = next((k for k in ["Mexico vs England", "Norway vs England", "Argentina vs England", "Semi Final", "Goal Celebration", "Landscape",
                                   "World Cup", "Newcastle", "Liverpool", "Dual Signature", "2025", "Collection"] if k in p["title"]), None)
            if not kw and re.search(r"\b2\b", p["title"]):
                kw = "Design 2"
            if kw:
                base = seo.replace(" | Foxy Printing", "")
                seo = f"{base} – {kw}" + (" | Foxy Printing" if len(f"{base} – {kw} | Foxy Printing") <= 60 else "")
                if len(seo) > 60:
                    seo = f"{base.replace(' Print', '')} – {kw}"
            for alt in (seo.replace(" Face Mask", " Party Face Mask"), seo.replace(" Poster Print", " Wall Art Poster"),
                        seo.replace(" Face Mask", " Fancy Dress Mask")):
                if alt not in seen_seo and alt != seo and len(alt) <= 60:
                    seo = alt
                    break
            else:
                dup_seo.append(p["handle"])
        seen_seo.add(seo)
        u = {"id": pid, "descriptionHtml": body, "seo": {"title": seo, "description": meta}}
        if title and title != p["title"]:
            u["title"] = title
        ups.append({"input": u, "tagsAdd": tags, "handle": p["handle"], "oldTitle": p["title"]})
        rows.append([p["handle"], p["title"], title or "", seo, meta, words(body), "; ".join(pr)])
    json.dump(ups, open(f"{out}/updates.json", "w"), ensure_ascii=False, indent=0)
    with open(f"{out}/review.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Handle", "Old title", "New title", "SEO title", "Meta", "Words", "Problems"])
        w.writerows(rows)
    with open(f"{out}/samples.html", "w", encoding="utf-8") as f:
        f.write("<meta charset=utf-8><style>body{font-family:sans-serif;max-width:800px;margin:auto}section{border-bottom:2px solid #ccc;padding:1em 0}</style>")
        for u in ups:
            f.write(f"<section><h1 style='font-size:1em;color:#666'>{esc(u['handle'])}</h1><b>{esc(u['input'].get('title', u['oldTitle']))}</b>"
                    f"<p><i>{esc(u['input']['seo']['title'])}</i><br><i>{esc(u['input']['seo']['description'])}</i></p>{u['input']['descriptionHtml']}</section>")
    print(f"built {len(ups)}, skipped {len(skipped)}, with problems {len(bad)}")
    for s in skipped:
        print("  SKIP", s["handle"], "|", s["title"])
    for h, pr in bad:
        print("  BAD", h, pr)
    print("duplicate SEO titles left:", dup_seo)


if __name__ == "__main__":
    main(*sys.argv[1:4])
