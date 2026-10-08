"""Printed Signature poster prints: new clean descriptions + import-queue rebuild (8 Oct 2026).

Owner (8 Oct 2026): "check the css and descriptions for the poster prints does not display correct".
Most of the 13,000+ Printed Signature posters still had old HTML (inline styles, font spans, <h1>,
tables, <br> soup, "limited edition / authentic / memorabilia" wording, no disclaimer).
Owner (8 Oct 2026): "i dont want reproduction Print in the title, it can be in the description".

What this script does
1. Builds a new description for every poster handle in the import queue, following CLAUDE.md:
   opening <p> with the primary keyword and "reproduction print" stated, one <h2>,
   <h3>Why you'll love it</h3>, <h3>Size &amp; details</h3> built from the product's REAL option
   values in the CSV rows, <h3>Delivery</h3> (fact sheet only), closing line, then
   <h3>Please note</h3><p class="disclaimer"> (signed-print disclaimer + the matching
   sports / celebrity / music / screen disclaimer naming the person and league where known).
   Wording varies per product (sentence pools keyed by category, picked by a hash of the handle).
2. Rewrites import-queue-2026-10-08 files 3 (test) and 4-7 in place: Body (HTML) on each poster's
   first row only; every other cell/row unchanged (mug rows untouched).
3. SAFEGUARD: Title and Status for every handle refreshed from a fresh live export, then
   "Reproduction Print" removed from poster titles (owner's 8 Oct instruction).
4. Validates and writes samples.html + a report.

Usage:
  python3 poster_descriptions.py LIVE_EXPORT.jsonl QUEUE_DIR OUT_DIR
LIVE_EXPORT.jsonl: bulk export of products { id handle title status productType tags
  collections { handle } } (collections as child lines with __parentId).
"""
import csv
import hashlib
import html
import io
import json
import os
import re
import sys

csv.field_size_limit(10 ** 9)

FILES = ["3-TEST-6-mugs-3-prints.csv", "4-mugs-and-prints-part1.csv", "5-mugs-and-prints-part2.csv",
         "6-mugs-and-prints-part3.csv", "7-mugs-and-prints-part4.csv"]

BANNED = re.compile(r"\b(signed|signature[sd]? by|autograph\w*|authentic|limited[- ]edition|memorabilia|"
                    r"official|licensed|genuine|approved|endorsed|merchandise|merch)\b", re.I)


# ------------------------------------------------------------------ helpers

def pick(pool, handle, slot):
    h = int(hashlib.md5((handle + "|" + slot).encode()).hexdigest(), 16)
    return pool[h % len(pool)]


def esc(s):
    return html.escape(s, quote=False)


MOJIBAKE = {"Ã©": "é", "ã©": "é", "Ã¡": "á", "ã¡": "á", "Ã³": "ó", "ã³": "ó", "Ã­": "í", "ã­": "í",
            "Ã¶": "ö", "ã¶": "ö", "Ã¼": "ü", "ã¼": "ü", "Ã±": "ñ", "ã±": "ñ", "Ã§": "ç", "ã§": "ç",
            "Ã¨": "è", "ã¨": "è", "Ã£": "ã", "Ã¤": "ä", "ã¤": "ä", "Ã¸": "ø", "ã¸": "ø", "Ãº": "ú",
            "ãº": "ú", "Ã«": "ë", "ã«": "ë", "Ã¯": "ï", "Ã´": "ô", "Ã¥": "å", "ã¥": "å"}


DOS_ACCENTS = {"\u00a1": "\u00ed", "\u00a4": "\u00f1", "\u00a2": "\u00f3", "\u00a3": "\u00fa", "\u201a": "\u00e9",
               "\u201e": "\u00e4", "\u2026": "\u00e0", "\u2021": "\u00e7", "\u0160": "\u00e8", "\u201d": "\u00f6"}


SPECIFIC_FIXES = [  # garbled names seen in live poster titles (8 Oct 2026)
    ('"Cowboy"\ufffd', "\u201cCowboy\u201d"), ("Jir\u00a1 Proch zka", "Ji\u0159\u00ed Proch\u00e1zka"),
    ("Sch\u00e3R", "Sch\u00e4r"), ("Almir\u00e3N", "Almir\u00f3n"), ("ALMIR\u00c3 N", "ALMIR\u00d3N"),
    ("Seasons 3\u00e211", "Seasons 3\u201311"),
]
CP1252_MOJIBAKE = {"\u00e2\u20ac\u2122": "\u2019", "\u00e2\u20ac\u201c": "\u2013", "\u00e2\u20ac\u201d": "\u2014",
                   "\u00e2\u20ac\u0153": "\u201c", "\u00e2\u20ac\u009d": "\u201d", "\u00e2\u20ac\u02dc": "\u2018",
                   "\u00e2\u20ac\u00a6": "\u2026"}


def fix_mojibake(s):
    """Repair garbled characters (owner/coordinator 8 Oct 2026). Keeps real accents and curly quotes."""
    for k, v in SPECIFIC_FIXES:
        s = s.replace(k, v)
    for k, v in CP1252_MOJIBAKE.items():
        s = s.replace(k, v)
    for k, v in MOJIBAKE.items():
        # "C\u00e3\u00a9Sar" -> "C\u00e9sar": the letter after a repaired accent was wrongly capitalised
        s = re.sub(re.escape(k) + r"([A-Z])(?=[a-z])", lambda m, v=v: v + m.group(1).lower(), s)
        s = s.replace(k, v)
    for k, v in DOS_ACCENTS.items():
        s = re.sub(r"(?<=[A-Za-z])" + re.escape(k) + r"(?=[A-Za-z])", v, s)
    s = s.replace("\ufffd", "")
    return re.sub(r"[ \t]{2,}", " ", s)


def fix_text(s):
    s = fix_mojibake(s)
    # old DOS code-page accents inside words (Mar\u00a1a -> Mar\u00eda, Mu\u00a4oz -> Mu\u00f1oz)
    for k, v in DOS_ACCENTS.items():
        s = re.sub(r"(?<=[A-Za-z])" + re.escape(k) + r"(?=[A-Za-z])", v, s)
    s = s.replace("\ufffd", "").replace("\u2019", "'")
    return re.sub(r"\s{2,}", " ", s).strip()


def smart_case(s):
    def word(w):
        if not w:
            return w
        if re.fullmatch(r"(?i)(ii|iii|iv|jr|sr|ufc|nfl|nba|wwe|ac|dc|fc|ufc|usa|uk|ksi|dj|mc)\.?", w):
            return w.upper() if w.lower() not in ("jr", "sr", "jr.", "sr.") else w.capitalize()
        if re.fullmatch(r"(?i)(van|von|der|of|the|and)", w):
            return w.lower()
        out = w[:1].upper() + w[1:].lower()
        out = re.sub(r"^(Mc|O'|D')([a-z])", lambda m: m.group(1) + m.group(2).upper(), out)
        out = re.sub(r"-([a-z])", lambda m: "-" + m.group(1).upper(), out)
        return out
    words = s.split(" ")
    res = [word(w) for w in words]
    if res and res[0][:1].islower():
        res[0] = res[0][:1].upper() + res[0][1:]
    return " ".join(res)


def strip_repro(title):
    """Remove 'Reproduction Print' wording from a title (owner, 8 Oct 2026); keep 'Printed Signature'."""
    t = re.sub(r"\s*[-–—|,:]?\s*\(?\bReproduction\s+Print\b\)?", "", title, flags=re.I)
    t = re.sub(r"\s*([-–—|,:])\s*(?=[-–—|,]|$)", "", t)
    t = re.sub(r"\s{2,}", " ", t).strip(" -–—|,:")
    return t


# ------------------------------------------------------------------ category

CATS = [
    # key, regex on title/type/tags/collections
    ("pack", r"\bA6\b.*\bpack\b|\bposter pack\b|print cards"),
    ("nfl", r"\bnfl\b|american football|cp-nfl|nfl-poster"),
    ("basketball", r"basketball|\bnba\b"),
    ("icehockey", r"ice hockey|\bnhl\b"),
    ("baseball", r"baseball|\bmlb\b"),
    ("rugby", r"rugby"),
    ("cricket", r"cricket"),
    ("golf", r"golf"),
    ("tennis", r"tennis"),
    ("darts", r"\bdarts?\b"),
    ("snooker", r"snooker"),
    ("mma", r"\bmma\b|\bufc\b|wrestl|\bwwe\b"),
    ("boxing", r"boxing|boxer|fight night"),
    ("f1", r"\bf1\b|formula (one|1)|motorsport|racing driver|motor racer|motogp|nascar"),
    ("football", r"football|soccer|footballer|team player|premier league"),
    ("screen", r"walking dead|game of thrones|sherlock|star wars|marvel|avengers|batman|superman|harry potter|"
               r"doctor who|eastenders|coronation street|peaky blinders|stranger things|breaking bad|the office|"
               r"only fools|lord of the rings|james bond|\b007\b|comedian|comedy|sitcom"),
    ("music", r"music|singer|\bband\b|rapper|\bdj\b|k-?pop|\brock\b|pop star"),
    ("bollywood", r"bollywood"),
    ("screen", r"movie|film|actor|actress|television|tv show|\btv\b|netflix|sitcom|soap|cinema"),
    ("business", r"business|entrepreneur"),
    ("sportother", r"athlet|olympi|cycling|cyclist|horse racing|jockey|swimm|sprinter"),
]
CATS = [(k, re.compile(r, re.I)) for k, r in CATS]


def category(title, ptype, tags, colls):
    t = title.lower()
    # title first (most reliable), then type, then tags/collections
    # Most tags are old noise (e.g. "Signed Athletics Prints" sits on 9,485 posters of every kind),
    # so only the new cp-<group> tags are trusted after the title and product type.
    cp = " ".join(x for x in tags if x.lower().startswith("cp-")).lower()
    for src in (t, (ptype or "").lower(), cp):
        for k, rx in CATS:
            if rx.search(src):
                return k
    return "celebrity"


SPORT = {
    # noun for the H2 ("... football print"), fan phrase, league/governing body phrase for disclaimer,
    # occasion phrase, collection phrase, people word
    "nfl": dict(topic="American football", fan="NFL fan", body="the NFL, or any NFL team or player",
                when="Super Bowl night", range="American football poster", who="player"),
    "football": dict(topic="football", fan="football fan", body="the Premier League, or any football club, league or governing body",
                     when="a big match day", range="football poster", who="player"),
    "basketball": dict(topic="basketball", fan="basketball fan", body="the NBA, or any basketball team, league or player",
                       when="the play-offs", range="basketball poster", who="player"),
    "icehockey": dict(topic="ice hockey", fan="ice hockey fan", body="the NHL, or any ice hockey team, league or player",
                      when="the play-offs", range="ice hockey poster", who="player"),
    "baseball": dict(topic="baseball", fan="baseball fan", body="Major League Baseball, or any baseball team or player",
                     when="the World Series", range="baseball poster", who="player"),
    "rugby": dict(topic="rugby", fan="rugby fan", body="any rugby club, union, league or player",
                  when="the Six Nations", range="rugby poster", who="player"),
    "cricket": dict(topic="cricket", fan="cricket fan", body="any cricket board, county, club or player",
                    when="an Ashes summer", range="cricket poster", who="player"),
    "golf": dict(topic="golf", fan="golf fan", body="any golf tour, club or governing body",
                 when="the Ryder Cup", range="golf poster", who="golfer"),
    "tennis": dict(topic="tennis", fan="tennis fan", body="any tennis tour, tournament or governing body",
                   when="Wimbledon fortnight", range="tennis poster", who="player"),
    "darts": dict(topic="darts", fan="darts fan", body="any darts organisation, tournament or player",
                  when="the World Darts Championship", range="darts poster", who="player"),
    "snooker": dict(topic="snooker", fan="snooker fan", body="any snooker tour, tournament or player",
                    when="the World Championship at the Crucible", range="snooker poster", who="player"),
    "mma": dict(topic="fight", fan="fight fan", body="any MMA or wrestling promotion (including the UFC and WWE), or any fighter",
                when="fight night", range="fight poster", who="fighter"),
    "boxing": dict(topic="boxing", fan="boxing fan", body="any boxing promoter, sanctioning body or fighter",
                   when="fight night", range="boxing poster", who="boxer"),
    "f1": dict(topic="motorsport", fan="motorsport fan", body="Formula 1, or any racing team, series or driver",
               when="a Grand Prix weekend", range="motorsport poster", who="driver"),
    "sportother": dict(topic="sport", fan="sports fan", body="any sports club, team, league or governing body",
                       when="a big race or match", range="sports poster", who="star"),
}

CLUBS = ["Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton", "Burnley", "Chelsea", "Crystal Palace",
         "Everton", "Fulham", "Leeds United", "Leicester City", "Liverpool", "Manchester City", "Manchester United",
         "Newcastle United", "Nottingham Forest", "Sunderland", "Tottenham Hotspur", "Tottenham", "West Ham United", "West Ham",
         "Wolves", "Norwich City", "Ipswich Town", "Southampton", "Sheffield United", "Sheffield Wednesday",
         "Middlesbrough", "Blackburn Rovers", "Bolton Wanderers", "Derby County", "Stoke City", "Celtic", "Rangers",
         "Real Madrid", "Barcelona", "Juventus", "AC Milan", "Inter Milan", "Inter Miami CF", "Inter Miami",
         "Bayern Munich", "Borussia Dortmund", "Paris Saint-Germain", "PSG", "Ajax", "Atletico Madrid",
         "Leeds Rhinos", "Wigan Warriors", "St Helens", "Saracens", "Leicester Tigers"]
CLUB_RX = re.compile(r"\b(" + "|".join(re.escape(c) for c in sorted(CLUBS, key=len, reverse=True)) + r")\b", re.I)


# ------------------------------------------------------------------ subject name

CUT = re.compile(
    r"\s+[-–—]\s+|\s*\(\d+\)|\s+\bM[C]?\d{2,5}\b|(?<!Part)\s+\d+\b|\bGift\b|\bInspired\b|\bHorse Rac\w*|\bRacer\b|"
    r"\bGolf\b|\bMotorcycle\b|\bComedy\b|\bStar\b|\bMartial Arts\b|\bLive Concert\b|\bPrinted Signature\b|\bPrinted Signed\b|"
    r"\b(Footballers?|Football Player|Football|American Football|NFL|Basketball Player|Basketball|Cricketer|"
    r"Golfer|Rugby|Darts|Boxing|Boxer|top boxer|MMA|Tennis Player|Tennis|Movie|Television|Tv Show|TV|Music|Bollywood|"
    r"Actors?|Actress|Netflix Shows?|Ice Hockey|Team Player|Famous|Black Frame|Framed|Poster|Print|Signed|"
    r"Autographed|Snooker|Formula|F1|Wrestler|Wrestling|Baseball|Athlete|Athletics|Cyclist|Jockey|Cricket|Hockey|"
    r"Motorsport|Racing|Player|Authors?|Scientist|Comedian|Rappers?|Singers?|UFC)\b", re.I)


def subject(title):
    t = fix_text(strip_repro(title))
    t = re.sub(r"^Printed Signature (By|Of)\s+", "", t, flags=re.I)
    name = t
    for m in CUT.finditer(t):
        if t[:m.start()].strip(" -–—_:,|"):
            name = t[:m.start()]
            break
    name = re.sub(r"\s*\bNo Badge Do Not Use\b", "", name, flags=re.I)
    name = name.strip(" -–—_:,|")
    name = re.sub(r"\s*[_+]\s*", " & ", name)
    name = re.sub(r"^(Iconic|Legend(ary)?)\s+", "", name, flags=re.I)
    if not name:
        name = t
    caps = [w for w in re.findall(r"[A-Za-z]{3,}", name) if w.isupper()]
    if name.isupper() or name.islower() or len(caps) >= 2:
        name = smart_case(name)
    return name


def pack_names(title):
    m = re.search(r"\(([^)]+)\)", title)
    if not m:
        return []
    return [smart_case(x.strip()) if x.strip().isupper() or x.strip().islower() else x.strip()
            for x in m.group(1).split(",") if x.strip()]


# ------------------------------------------------------------------ sizes from option values

DIMS = {"A0": "841 x 1189 mm", "A1": "594 x 841 mm", "A2": "420 x 594 mm", "A3": "297 x 420 mm",
        "A4": "210 x 297 mm", "A5": "148 x 210 mm", "A6": "105 x 148 mm"}
ORDER = ["A6", "A5", "A4", "A3", "A2", "A1", "A0"]
COLOURS = ["Black", "Silver", "Gold", "White"]


def parse_sizes(values):
    prints, frames = set(), {}
    for v in values:
        s = re.search(r"\bA([0-6])\b", v, re.I)
        if not s:
            continue
        size = "A" + s.group(1)
        cols = [c for c in COLOURS if re.search(r"\b" + c + r"\b", v, re.I)]
        if re.search(r"frame", v, re.I) and not re.search(r"un-?framed|no frame|print only", v, re.I):
            for c in cols or ["Black"]:
                frames.setdefault(size, [])
                if c not in frames[size]:
                    frames[size].append(c)
        else:
            prints.add(size)
    prints = [s for s in ORDER if s in prints]
    frames = {s: sorted(frames[s], key=COLOURS.index) for s in ORDER if s in frames}
    return prints, frames


def join_or(xs):
    xs = list(xs)
    if len(xs) == 1:
        return xs[0]
    return ", ".join(xs[:-1]) + " or " + xs[-1]


def join_and(xs):
    xs = list(xs)
    if len(xs) == 1:
        return xs[0]
    return ", ".join(xs[:-1]) + " and " + xs[-1]


# ------------------------------------------------------------------ copy pools

def group_of(cat):
    if cat in SPORT:
        return "sport"
    return {"music": "music", "screen": "screen", "bollywood": "screen", "pack": "pack"}.get(cat, "people")


def kind_words(cat):
    """(topic adjective for the poster, fan phrase, gift occasion, range phrase)."""
    if cat in SPORT:
        s = SPORT[cat]
        return s["topic"], s["fan"], s["when"], s["range"]
    return {
        "music": ("music", "music fan", "a gig night", "music poster"),
        "screen": ("film and TV", "film and TV fan", "a film night", "film and TV poster"),
        "bollywood": ("Bollywood", "Bollywood fan", "a film night", "Bollywood poster"),
        "business": ("famous face", "fan", "a new job or promotion", "celebrity poster"),
    }.get(cat, ("celebrity", "fan", "a birthday", "celebrity poster"))


OPEN = {
    "sport": [
        "Give a {fan} something to smile about with this printed signature {topic} poster of {name}. It's a reproduction print with the signature printed into the design, and it suits a bedroom, games room, office or man cave.",
        "This printed signature {topic} poster of {name} brings a bit of {when} feeling into any room. It's a reproduction print, made to order here in North Yorkshire, and an easy gift for a {fan}.",
        "Looking for a present for a {fan}? Our printed signature {topic} poster of {name} is a reproduction print with the signature reproduced on the artwork, ready for a bedroom, den or office wall.",
        "Our printed signature {topic} poster of {name} is a simple way to show who you follow. It's a reproduction print – the signature is part of the printed design – and it makes a thoughtful gift for any {fan}.",
        "If there's a {fan} in your life, this printed signature {topic} poster of {name} is a gift they'll actually put on the wall. Please note it's a reproduction print, with the signature printed as part of the design.",
        "Celebrate a favourite {who} with this printed signature {topic} poster of {name}. It's a reproduction print made in-house, so the signature is printed into the artwork rather than written by hand.",
    ],
    "music": [
        "This printed signature music poster of {name} is a lovely way to put a favourite artist on the wall. It's a reproduction print with the signature printed into the design, made to order in North Yorkshire.",
        "Give a music fan something special with our printed signature music poster of {name}. It's a reproduction print – the signature is part of the artwork – and it looks great in a bedroom, studio or hallway.",
        "Our printed signature music poster of {name} is made for the fan who knows every lyric. Please note it's a reproduction print, with the signature printed as part of the design.",
        "Looking for a gift for a gig-goer? This printed signature music poster of {name} is a reproduction print, printed in-house and ready to frame or hang.",
        "Bring a bit of the front row home with this printed signature music poster of {name}. It's a reproduction print, so the signature is printed on rather than hand-written.",
    ],
    "screen": [
        "This printed signature {topic} poster of {name} is a fun gift for anyone who loves a good film or box set. It's a reproduction print with the signature printed into the design.",
        "Our printed signature {topic} poster of {name} is made for movie nights and TV binges. It's a reproduction print, made to order here in North Yorkshire.",
        "Treat a {fan} to this printed signature {topic} poster of {name}. Please note it's a reproduction print – the signature is printed as part of the artwork.",
        "Looking for a gift for a film buff? This printed signature {topic} poster of {name} is a reproduction print that looks great in a lounge, den or home cinema.",
        "Add a familiar face to the wall with our printed signature {topic} poster of {name}. It's a reproduction print, printed in-house with the signature reproduced on the design.",
    ],
    "people": [
        "This printed signature poster of {name} is a fun gift for a fan. It's a reproduction print with the signature printed into the design, made to order in North Yorkshire.",
        "Our printed signature poster of {name} is an easy way to put a favourite famous face on the wall. Please note it's a reproduction print – the signature is part of the printed artwork.",
        "Looking for something a bit different for a fan? This printed signature poster of {name} is a reproduction print, printed in-house and ready for the wall.",
        "Give a fan of {name} a smile with this printed signature poster. It's a reproduction print, so the signature is printed on rather than hand-written.",
    ],
    "pack": [
        "This printed signature A6 poster pack of {name} is a fun little set for a {fan}. Each card is a reproduction print with the signature printed into the design.",
        "Our printed signature A6 poster pack of {name} gives a {fan} a handful of favourite faces in one go. Please note they're reproduction prints – the signatures are part of the printed artwork.",
        "Looking for a stocking filler for a {fan}? This printed signature A6 poster pack of {name} is a set of reproduction prints, made to order in North Yorkshire.",
    ],
}

H2 = {
    "sport": ["Printed signature {topic} poster of {name}", "{name} printed signature {topic} print",
              "{name} {topic} poster with printed signature", "Printed signature {name} {topic} poster"],
    "music": ["Printed signature music poster of {name}", "{name} printed signature music print",
              "{name} music poster with printed signature"],
    "screen": ["Printed signature {topic} poster of {name}", "{name} printed signature poster print",
               "{name} poster with printed signature"],
    "people": ["Printed signature poster of {name}", "{name} printed signature poster print",
               "{name} poster with printed signature"],
    "pack": ["Printed signature A6 poster pack of {name}", "{name} printed signature A6 poster cards"],
}

DETAIL = [
    "The design shows {name} with a printed signature reproduced on the artwork, so it's a reproduction print rather than one written by hand. {sizes_sentence}",
    "Each poster shows {name} with the signature printed into the design. {sizes_sentence}",
    "You get a full-colour print of {name} with the signature printed as part of the artwork. {sizes_sentence}",
    "It's printed to order in our North Yorkshire workshop, with {name}'s signature reproduced as part of the print. {sizes_sentence}",
]

FRAME_LINES = [
    "Framed options come in our Premium Display frames – thick, chunky and very professional, not the cheap thin frames you often see.",
    "Choose a framed size and it arrives in one of our Premium Display frames: thick, chunky and properly professional, not a cheap thin frame.",
    "The framed versions use our Premium Display frames, a thick, chunky, professional finish rather than a flimsy thin frame.",
    "Going framed? Every framed option comes in a Premium Display frame – thick, chunky and very professional, nothing like a cheap thin frame.",
]

BULLETS_COMMON = [
    "Made in-house in North Yorkshire, UK, and printed when you order",
    "Printed to order in our own North Yorkshire workshop",
    "Clearly a reproduction – the signature is part of the print",
    "Honest reproduction print: the signature is printed on, not hand-written",
]


def gift_bullet(cat, handle):
    _, fan, when, _ = kind_words(cat)
    pool = {
        "sport": ["A gift idea for birthdays, Christmas, Father's Day or {when}",
                  "Ideal for a {fan}'s birthday, Christmas or {when}",
                  "A thoughtful present for any {fan}, young or old"],
        "music": ["A gift idea for birthdays, Christmas or after a gig",
                  "Ideal for a music fan's bedroom, studio or record corner",
                  "A thoughtful present for any music fan, young or old"],
        "screen": ["A gift idea for birthdays, Christmas or a film night",
                   "Ideal for a lounge, den or home cinema wall",
                   "A thoughtful present for any film and TV fan"],
        "people": ["A gift idea for birthdays, Christmas or just because",
                   "Ideal for a bedroom, office or hallway wall",
                   "A thoughtful present for any fan"],
        "pack": ["A handy stocking filler or party bag treat",
                 "Small enough for a desk, pinboard or scrapbook",
                 "A thoughtful little present for any {fan}"],
    }[group_of(cat)]
    return pick(pool, handle, "gift").format(fan=fan, when=when)


CLOSE = {
    "sport": ["Pair it with another {who} from our {range} range for a matching set. Custom designs on request – call 01439 771468.",
              "Collecting {topic} prints? Browse our other {range}s to build a matching wall. Custom designs are available on request – call 01439 771468.",
              "Want a different {who}? Get in touch on 01439 771468 – custom designs are available on request.",
              "Make it a set with more posters from our {range} range, or call 01439 771468 about a custom design."],
    "music": ["Pair it with another artist from our music poster range for a matching wall. Custom designs on request – call 01439 771468.",
              "Can't find your favourite artist? Custom designs are available on request – call 01439 771468.",
              "Make it a set with more prints from our music poster range, or call 01439 771468 about a custom design."],
    "screen": ["Pair it with more prints from our film and TV poster range for a matching wall. Custom designs on request – call 01439 771468.",
               "Can't see the star you're after? Custom designs are available on request – call 01439 771468.",
               "Make a movie wall with more posters from our film and TV range, or call 01439 771468 about a custom design."],
    "people": ["Pair it with more prints from our celebrity poster range. Custom designs on request – call 01439 771468.",
               "Can't see the famous face you're after? Custom designs are available on request – call 01439 771468."],
    "pack": ["Pair it with a full-size poster of their favourite from our poster range. Custom designs on request – call 01439 771468.",
             "Want a different line-up? Custom designs are available on request – call 01439 771468."],
}

DELIVERY = [
    "Printed to order in North Yorkshire. Postage options and costs are shown at checkout.",
    "Each print is made to order in our North Yorkshire workshop. You'll see the postage options and costs at checkout.",
    "We print your poster when you order, here in North Yorkshire. Postage options and prices are shown at checkout.",
]

EXTRA = {
    "sport": ["It's a lovely way to celebrate a favourite {who}, whether they're a current star or a legend from years gone by. Hang it in a bedroom, games room, office or man cave, or wrap it up for a birthday or Christmas.",
              "Fans of all ages love seeing a favourite {who} on the wall. It makes a simple, thoughtful present for a birthday, Christmas, Father's Day or {when}, and it brightens up a bedroom, den or office.",
              "Whether they watch every game or just love a sporting legend, a print like this is an easy way to show it. It suits a bedroom, games room, office or bar area and makes a handy gift for any {fan}."],
    "music": ["It's a lovely way to remember a favourite song, album or gig. Hang it in a bedroom, studio, hallway or music room, or wrap it up for a birthday or Christmas.",
              "Fans of all ages love seeing a favourite artist on the wall. It makes a simple, thoughtful present for a birthday, Christmas or after a big concert.",
              "Whether they've followed the music for years or just discovered it, a print like this is an easy way to show it, and it brightens up any bedroom, den or office."],
    "screen": ["It's a lovely way to remember a favourite film, show or performance. Hang it in a lounge, bedroom, den or home cinema, or wrap it up for a birthday or Christmas.",
               "Film and TV fans of all ages love seeing a familiar face on the wall. It makes a simple, thoughtful present for a birthday, Christmas or a film night in.",
               "Whether it's a classic or this year's favourite box set, a print like this is an easy way to show it, and it brightens up any bedroom, den or office."],
    "people": ["It's a fun way to put a favourite famous face on the wall. Hang it in a bedroom, office or hallway, or wrap it up for a birthday or Christmas.",
               "Fans of all ages love seeing someone they admire on the wall. It makes a simple, thoughtful present for a birthday, Christmas or just because."],
    "pack": ["They're great for a pinboard, scrapbook or desk, and make a handy stocking filler or party bag treat."],
}

EXTRA_BULLETS = ["Looks great in a bedroom, office, games room or hallway", "Easy to wrap and post as a gift",
                 "Bright, full-colour print of the artwork"]


SIGNED_SENTENCE = ("This is a printed reproduction. The signature is printed as part of the design – "
                   "it is not hand-signed and is not an original autograph.")


def disclaimer(cat, name, title, people):
    nm = esc(name)
    if cat in SPORT or cat == "pack":
        s = SPORT.get(cat) or SPORT["football"]
        if cat == "pack":
            # packs are mostly football line-ups
            for k in ("nfl", "basketball", "rugby", "cricket", "darts", "boxing", "mma", "golf", "f1"):
                if CATS_D[k].search(title):
                    s = SPORT[k]
                    break
        clubs = []
        for m in CLUB_RX.finditer(title):
            c = m.group(1)
            c = next((x for x in CLUBS if x.lower() == c.lower()), c)
            if c not in clubs:
                clubs.append(c)
        who = [nm] if not people else [esc(p) for p in people]
        if clubs and name.lower() not in [c.lower() for c in clubs]:
            who += [esc(c) for c in clubs]
        elif clubs and cat == "pack":
            pass
        return (SIGNED_SENTENCE + " This is an unofficial, fan-made design created and printed by Foxy Printing. "
                "It is not endorsed by, sponsored by, or affiliated with " + join_and(who) + ", " + s["body"] +
                ". Names are used only to describe the design and who it's for. All trademarks belong to their "
                "respective owners.")
    if cat == "music":
        return (SIGNED_SENTENCE + " This is an unofficial fan design. It is not endorsed by, or connected with, " + nm +
                ", their management or record label. All names and trademarks belong to their respective owners.")
    if cat in ("screen", "bollywood"):
        return (SIGNED_SENTENCE + " This is an unofficial fan print made by Foxy Printing. " + nm +
                " has not endorsed, sponsored or approved this product, and Foxy Printing has no connection with them, "
                "or with any studio, broadcaster, streaming service or production company. The name is used only to "
                "describe the design. All names, characters and trademarks belong to their respective owners.")
    return (SIGNED_SENTENCE + " This is an unofficial fan print made by Foxy Printing. " + nm +
            " has not endorsed, sponsored or approved this product, and Foxy Printing has no connection with them. "
            "The name is used only to describe the design. All trademarks belong to their respective owners.")


CATS_D = {k: rx for k, rx in CATS}


# ------------------------------------------------------------------ build one description

def build(handle, title, cat, option_values):
    name = subject(title)
    people = pack_names(title) if cat == "pack" else []
    g = group_of(cat)
    topic, fan, when, rng = kind_words(cat)
    who = SPORT[cat]["who"] if cat in SPORT else "star"
    f = dict(name=esc(name), topic=topic, fan=fan, when=when, range=rng, who=who)

    prints, frames = parse_sizes(option_values)
    framed_sizes = list(frames)
    all_cols = sorted({c for v in frames.values() for c in v}, key=COLOURS.index)

    # sizes sentence + size list
    size_items = []
    if cat == "pack":
        m = re.search(r"(\d+)\s+Poster Print Cards", title, re.I)
        n = m.group(1) if m else None
        sizes_sentence = ("The pack has " + n + " A6 poster print cards" if n else "The pack is a set of A6 poster print cards") + \
            (", one for each of " + esc(join_and(people)) + "." if people and (not n or int(n) == len(people)) else ".")
        size_items.append("A6 poster print cards: " + DIMS["A6"] + " each")
        if n:
            size_items.append("Cards in the pack: " + n)
        if people:
            size_items.append("Featuring: " + esc(join_and(people)))
    elif prints or frames:
        parts = []
        if prints:
            parts.append(("a print-only " + join_or(prints)) if len(prints) == 1 else ("print-only sizes " + join_or(prints)))
        if frames:
            parts.append("a framed " + join_or(framed_sizes) + (" in " + join_or([c.lower() for c in all_cols]) if all_cols else ""))
        sizes_sentence = pick(["Pick the size that suits your wall: {p}.", "Choose from {p}.",
                               "It comes in {p}, so there's an option for every wall."], handle, "sz").format(p=", or ".join(parts))
        if len(prints) + sum(len(c) for c in frames.values()) > 9:
            sizes_sentence = pick(["Pick a print-only size or a framed {f} – the full list is below.",
                                   "Choose print only or a framed {f}; every size is listed below."], handle, "sz2").format(
                f=join_or(framed_sizes) if frames else "print")
        for s in prints:
            size_items.append(f"{s} print only: {DIMS[s]}")
        for s, cols in frames.items():
            size_items.append(f"{s} framed: {join_or(cols)} frame")
    else:
        sizes_sentence = "Pick your size and finish from the choices shown on this page before you add it to your basket."
        size_items.append("Size and finish: as shown in the choices on this page")
        size_items.append("Full-colour print with the signature printed into the design")
        size_items.append("Printed to order in North Yorkshire, UK")

    open_p = pick(OPEN[g], handle, "open").format(**f)
    h2 = pick(H2[g], handle, "h2").format(**f)
    h2 = h2[:1].upper() + h2[1:]
    detail = pick(DETAIL, handle, "detail").format(name=esc(name), sizes_sentence=sizes_sentence)
    if cat == "pack":
        detail = "Each card shows a player with the signature printed into the design, so they're reproduction prints rather than cards written on by hand. " + sizes_sentence
    frame_line = pick(FRAME_LINES, handle, "frame") if frames else ""

    bullets = [pick(BULLETS_COMMON[:2], handle, "b1"), pick(BULLETS_COMMON[2:], handle, "b2")]
    if cat == "pack":
        bullets.append("Handy A6 size, about the size of a postcard")
    elif prints:
        if len(prints) >= 2:
            bullets.append(f"{len(prints)} print-only sizes, from {prints[0]} up to a big {prints[-1]}"
                           if len(prints) <= 4 else f"Print-only sizes from {prints[0]} all the way up to {prints[-1]}")
        else:
            bullets.append(f"Print-only {prints[0]} size")
    if frames:
        bullets.append(f"Framed {join_and(framed_sizes)} options in {join_or([c.lower() for c in all_cols])} Premium Display frames")
        if "A3" in frames or "A4" in frames:
            bullets.append(pick(["A3 frames have a clip on the back to hang, A4 frames have a stand",
                                 "Framed A4s stand up on a shelf or desk; framed A3s have a clip on the back for the wall"], handle, "hang"))
    bullets.append(gift_bullet(cat, handle))
    if not frames:
        bullets.append(pick(["Bright, full-colour print of the artwork", "Full-colour print, made when you order",
                             "Easy to put in a frame of your own"], handle, "b5"))
    # de-duplicate, keep order
    seen, bl = set(), []
    for b in bullets:
        if b not in seen:
            seen.add(b)
            bl.append(b)

    close = pick(CLOSE[g], handle, "close").format(**f)
    delivery = pick(DELIVERY, handle, "delivery")
    disc = disclaimer(cat, name, fix_text(title), people)

    if not (prints or frames) or cat == "pack":
        # no size options to list: add a gifting paragraph and two more bullets so the copy is complete
        detail += "</p>\n<p>" + pick(EXTRA[g], handle, "extra").format(**f)
        for b in EXTRA_BULLETS:
            if b not in bl and len(bl) < 6:
                bl.append(b)
    out = [f"<p>{open_p}</p>", f"<h2>{h2}</h2>", f"<p>{detail}" + (f" {frame_line}" if frame_line else "") + "</p>",
           "<h3>Why you'll love it</h3>", "<ul>\n" + "\n".join(f"<li>{b}</li>" for b in bl) + "\n</ul>",
           "<h3>Size &amp; details</h3>", "<ul>\n" + "\n".join(f"<li>{s}</li>" for s in size_items) + "\n</ul>",
           "<h3>Delivery</h3>", f"<p>{delivery}</p>", f"<p>{close}</p>",
           "<h3>Please note</h3>", f'<p class="disclaimer">{disc}</p>']
    return "\n".join(out), name


# ------------------------------------------------------------------ validation

def problems(body):
    p = []
    if body.count("<h2") != 1:
        p.append("h2 count")
    if '<p class="disclaimer">' not in body or not body.rstrip().endswith("</p>"):
        p.append("disclaimer")
    if re.search(r"style=|<span|<h1|<table|<br", body, re.I):
        p.append("bad html")
    nd = re.sub(r'<p class="disclaimer">.*?</p>', "", body, flags=re.S)
    if BANNED.search(nd):
        p.append("banned: " + BANNED.search(nd).group(0))
    if re.search(r"\[|\]", body):
        p.append("brackets")
    if "reproduction" not in re.sub(r"<[^>]+>", " ", body.split("<h3>")[0]).lower():
        p.append("no reproduction near top")
    # CLAUDE.md: 180-350 words for the copy itself; the Please note disclaimer block comes on top.
    words = len(re.sub(r"<[^>]+>", " ", body.split("<h3>Please note</h3>")[0]).split())
    if not 180 <= words <= 350:
        p.append(f"words {words}")
    return p


# ------------------------------------------------------------------ main

def load_live(path):
    prods = {}
    byid = {}
    for line in open(path, encoding="utf-8"):
        o = json.loads(line)
        if "__parentId" in o:
            if o["__parentId"] in byid and "handle" in o:
                byid[o["__parentId"]]["colls"].append(o["handle"])
            continue
        o["colls"] = []
        byid[o["id"]] = o
        prods[o["handle"]] = o
    return prods


def is_poster(p):
    return "printed signature" in (p.get("title") or "").lower() or "printed signature" in (p.get("_csv_title") or "").lower()


def main(live_path, qdir, out_dir, files=None, dry=False):
    files = files or FILES
    os.makedirs(out_dir, exist_ok=True)
    live = load_live(live_path)
    report = {"files": {}, "posters": 0, "problems": [], "missing_live": [], "titles_changed": 0,
              "status_changed": 0, "cats": {}}
    samples = []
    poster_handles = set()
    for fn in files:
        test_file = fn.startswith("3-TEST")
        path = os.path.join(qdir, fn)
        raw = open(path, "rb").read()
        rows = list(csv.reader(io.StringIO(raw.decode("utf-8"), newline="")))
        head, body_rows = rows[0], rows[1:]
        H = {k: i for i, k in enumerate(head)}
        groups = {}
        for r in body_rows:
            groups.setdefault(r[H["Handle"]], []).append(r)
        before = {h: len(v) for h, v in groups.items()}
        seen_first = set()
        for r in body_rows:
            h = r[H["Handle"]]
            if h in seen_first:
                continue
            seen_first.add(h)
            lp = live.get(h)
            if lp is None:
                report["missing_live"].append(h)
                continue
            poster = "printed signature" in lp["title"].lower() or "printed signature" in r[H["Title"]].lower()
            if test_file and not poster:
                continue  # coordinator: leave the 6 test mug rows exactly as they are
            # SAFEGUARD: Title + Status from live
            new_title = lp["title"]
            if poster or re.search(r"reproduction\s+print", new_title, re.I):
                new_title = strip_repro(new_title)  # owner, 8 Oct 2026: no "Reproduction Print" in titles
            if poster:
                fixed = fix_mojibake(new_title)
                if fixed != new_title:
                    report.setdefault("titles_mojibake_fixed", []).append([h, new_title, fixed])
                    new_title = fixed
            if r[H["Title"]] != new_title:
                report["titles_changed"] += 1
            if r[H["Status"]] != lp["status"].lower():
                report["status_changed"] += 1
            r[H["Title"]] = new_title
            r[H["Status"]] = lp["status"].lower()
            if not poster:
                continue
            vals = []
            for x in groups[h]:
                for k in (1, 2, 3):
                    v = x[H[f"Option{k} Value"]]
                    if v and v != "Default Title":
                        vals.append(v)
            cat = category(lp["title"], lp.get("productType"), lp.get("tags") or [], lp["colls"])
            body, name = build(h, lp["title"], cat, vals)
            r[H["Body (HTML)"]] = body
            poster_handles.add(h)
            report["cats"][cat] = report["cats"].get(cat, 0) + 1
            pr = problems(body)
            if pr:
                report["problems"].append({"handle": h, "problems": pr})
            if True:
                samples.append((h, new_title, cat, name, body))
        # row counts per handle unchanged
        after = {}
        for r in body_rows:
            after[r[H["Handle"]]] = after.get(r[H["Handle"]], 0) + 1
        assert after == before, fn
        out = io.StringIO(newline="")
        csv.writer(out).writerows([head] + body_rows)
        data = out.getvalue().encode("utf-8")
        if not dry:
            open(path, "wb").write(data)
        # re-parse check
        chk = list(csv.reader(io.StringIO(data.decode("utf-8"), newline="")))
        assert len(chk) == len(rows) and all(len(x) == len(head) for x in chk), fn
        report["files"][fn] = {"rows": len(body_rows), "handles": len(groups), "bytes": len(data),
                               "posters": sum(1 for h in groups if h in poster_handles)}
    report["posters"] = len(poster_handles)
    report["poster_handles_by_file"] = None
    json.dump(report, open(os.path.join(out_dir, "report.json" if len(files) > 1 else "report-" + files[0][:1] + ".json"), "w"), indent=1, ensure_ascii=False)
    json.dump(sorted(poster_handles), open(os.path.join(out_dir, "_poster_handles.json"), "w"))
    write_samples(samples, os.path.join(out_dir, "samples.html"))
    print(json.dumps({k: v for k, v in report.items() if k != "problems"}, indent=1, ensure_ascii=False)[:4000])
    print("problems:", len(report["problems"]), report["problems"][:10])


def write_samples(samples, path):
    # 10 samples across different categories
    chosen, cats = [], set()
    want = [("nfl", "Size &amp; details</h3>\n<ul>\n<li>A4 print only"), ("football", "framed: Black, Silver, Gold or White"),
            ("football", "choices on this page"), ("music", "A4 print only"), ("screen", ""), ("mma", ""),
            ("pack", ""), ("celebrity", ""), ("cricket", ""), ("f1", "")]
    for cat, marker in want:
        for s in samples:
            if s[2] == cat and marker in s[4] and s not in chosen:
                chosen.append(s)
                break
    for s in samples:
        if len(chosen) >= 10:
            break
        if s not in chosen:
            chosen.append(s)
    chosen = chosen[:10]
    parts = ["<!doctype html><html lang='en'><head><meta charset='utf-8'>"
             "<meta name='viewport' content='width=device-width,initial-scale=1'>"
             "<title>Poster description samples</title><style>"
             "body{font-family:system-ui,sans-serif;max-width:760px;margin:0 auto;padding:16px;line-height:1.5;background:#fff;color:#222}"
             "article{border:1px solid #ddd;border-radius:8px;padding:16px;margin:24px 0}"
             ".meta{font-size:13px;color:#666}.disclaimer{font-size:13px;color:#555}"
             "</style></head><body><h1>Printed Signature poster descriptions – 10 samples (8 Oct 2026)</h1>"]
    for h, t, cat, name, body in chosen:
        parts.append(f"<article><div class='meta'>{esc(h)} · category: {cat} · subject: {esc(name)}</div>"
                     f"<h1 style='font-size:20px'>{esc(t)}</h1>{body}</article>")
    parts.append("</body></html>")
    open(path, "w", encoding="utf-8").write("\n".join(parts))


if __name__ == "__main__":
    fl = sys.argv[4].split(",") if len(sys.argv) > 4 and sys.argv[4] else None
    main(sys.argv[1], sys.argv[2], sys.argv[3], fl, dry=os.environ.get("DRY") == "1")
