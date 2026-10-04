"""Build SEO title + meta description import CSVs for every Foxy Printing product that needs them.

Usage: python3 build.py   (reads scope.json made from the 4 Oct 2026 bulk export)
"""
import collections
import csv
import hashlib
import json
import os
import random
import re
import sys

from family import family as _family

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/user/panda/foxyprinting-rebrand/exports/seo"
SUFFIX = " | Foxy Printing"

# ---------------------------------------------------------------- word rules
ACRONYMS = {"UK", "TV", "NFL", "NBA", "WWE", "WWF", "UFC", "NHS", "NES", "SNES", "USA", "GTA", "DIY", "DTF", "UV", "VE",
            "PS1", "PS2", "PS3", "PS4", "PS5", "N64", "BMX", "3DO", "CD32", "F1", "MDF", "NHL", "NASA", "RAF", "ABBA", "XL",
            "XXL", "DJ", "PE", "TT", "MMA", "BBC", "ITV", "GP", "AC", "FC", "AFC", "QR", "ID", "ET", "OK", "LED", "PJ",
            "PJS", "GBA", "PSP", "DS", "3DS", "CD", "DVD", "VHS", "MTV", "BTS", "UB40", "ELO", "REM", "INXS", "AC/DC", "KISS",
            "PC", "RPG", "NBA2K", "WRC", "MLB", "NCAA", "PGA", "LPGA", "BMW", "VW", "MG", "TVR", "RS", "GT", "GTI", "SUV",
            "HGV", "LGBT", "LGBTQ", "OMG", "LOL", "WTF", "BFF", "FTW", "SAS", "MI5", "NYC", "LA", "UEFA", "IT", "HR", "CEO",
            "RX", "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "XIII", "XIV", "XV", "UFO", "KO", "NWA", "DMX",
            "EU", "US", "AU", "JP", "PAL", "NTSC", "RC", "ATV", "HMS", "RNLI", "NCT", "EXO", "SNK", "GB", "GBC", "SFX", "HAL"}
JUNK_CAPS = {"SA", "JB", "SJ", "KE", "BM", "MC", "SH", "CM", "JD", "LH", "NB", "AM", "RM", "TM"}
SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "with", "from", "into", "vs"}

BANNED = re.compile(r"\b(official(ly)?|licen[sc]ed|authentic|genuine|autograph(ed|s)?|memorabilia|merchandise|best|cheapest|"
                    r"(free |digital |email(ed)? (a )?)proofs?|proofs? on request|live preview|endorsed|approved)\b|\bsigned\b", re.I)
BEST_OK = re.compile(r"best of the best|(george|harry|calum|pete|feorge|clint|angie|james|jake|leo|tino|lindsay|darren|wayne|tony|kevin|eric|ronnie) best\b", re.I)
PROFANE = re.compile(r"\b(f+u+c+k\w*|fuk(in|ing|ed|ker|kers)?|sh[i1]t|sh[i1]tt?(ing|ed|er|s|y|hole|head)\w*|cunt\w*|twat\w*|wank\w*|bollock\w*|"
                     r"bitch\w*|bastard\w*|slut\w*|piss|pissed|pissing|piss(ed)?head\w*|arse|arses|arsehole\w*|tits|knobhead\w*|"
                     r"bellend\w*|minge\w*|dickhead\w*|feck\w*)\b", re.I)
RUDE_HINT = re.compile(r"\b(rude|adult|18\+|naughty|sex\w*|willy|boobs|penis|vagina|orgasm|horny|stag|hen do)\b", re.I)


def censor(m):
    w = m.group(0)
    root = re.match(r"[A-Za-z]+?(?=(ing|in'|in|ed|er|ers|s|y)?$)", w)
    core = root.group(0) if root else w
    return core[0] + "*" * (len(core) - 1) + w[len(core):]


def smart_word(w):
    """Title-case one token, keeping acronyms."""
    bare = re.sub(r"[^A-Za-z0-9/]", "", w)
    if not bare:
        return w
    if bare.upper() in ACRONYMS and (bare.isupper() or bare.upper() in {"NES", "SNES", "NFL", "UFC", "WWE", "NHS", "UK", "TV", "F1"}):
        return w.upper() if bare.isalpha() or bare.isalnum() else w
    if len(bare) == 2 and bare.isupper() and bare not in JUNK_CAPS:
        return w
    if len(bare) > 2 and bare[0].islower() and bare[1:].isupper():
        bare = bare.upper()
        w = w.upper()
    if any(c.isdigit() for c in bare) and bare.upper() == bare and len(bare) <= 5:
        return w  # 3DO, PS1, N64
    if re.fullmatch(r"\d+(st|nd|rd|th|ml|cm|mm|oz|s)", bare, re.I):
        return w.lower()
    if bare.isupper() and len(bare) >= 2 or bare.islower():
        def cap(p):
            if not p:
                return p
            if re.match(r"(?i)mc[a-z]{2,}", p):
                return "Mc" + p[2:3].upper() + p[3:].lower()
            return p[0].upper() + p[1:].lower()
        out = re.sub(r"(?<![0-9])[A-Za-z]+", lambda m: cap(m.group(0)), w)
        # o'neill -> O'Neill but don't -> Don't, it's -> It's
        out = re.sub(r"\b([A-Z])'([a-z])(?=[a-z]{2,})", lambda m: m.group(1) + "'" + m.group(2).upper(), out)
        out = re.sub(r"(?<=[a-z])'(S|T|Re|Ll|Ve|D|M)\b", lambda m: "'" + m.group(1).lower(), out)
        return out
    return w


def tidy_case(s):
    toks = s.split(" ")
    out = []
    for i, t in enumerate(toks):
        w = smart_word(t)
        if i and w.lower() in SMALL and out and not out[-1].endswith(("–", ":")):
            w = w.lower()
        elif w in ("x", "X") and out and re.match(r"^\d+$", out[-1]):
            w = "x"
        elif w[:1].islower() and not re.match(r"^\d", w) and w.lower() not in {"x"}:
            w = w[:1].upper() + w[1:]
        out.append(w)
    return " ".join(out)


SIZE_LIST = re.compile(r"\b(A[0-6]|A6 Card)(\s*(,|/|&|\+|or|and|-)?\s*A[0-6]\b)+(\s*(or|&)\s*A[0-6]\b)?", re.I)
JUNK_PHRASES = [
    r"game inspired theme", r"theme inspired style", r"inspired theme style", r"theme inspired", r"inspired theme",
    r"inspired style", r"style theme", r"theme style", r"style game", r"inspired by pop figures", r"\binspired by\b",
    r"\binspired\b", r"kids\s*-\s*adults\s*-", r"kids adults?", r"high quality", r"any name you want!?", r"customi[sz]e present",
    r"limited edition", r"special edition", r"\bcopy of\b", r"\(?copy\)?", r"total calculated at checkout",
    r"fancy dress hen birthday party fun stag do hen", r"text style",
    r"collectible|collectable|memorabilia|merchandise|\bmerch\b", r"\bofficial(ly)?\b", r"\blicen[sc]ed\b", r"\bauthentic\b",
    r"\bgenuine\b", r"\bcertified\b", r"\bcoa\b", r"\bfor fans (&|and) collectors\b", r"\bphoto signature\b", r"\bsignatur\b",
    r"\bcheapest\b", r"\bpremium party decorations\b", r"\bincluding cushion insert\b", r"\bnovelty funny mug\b",
]
JUNK_RX = re.compile("|".join(JUNK_PHRASES), re.I)
CODE_RX = re.compile(r"\b(?!X\d+\b)(?=[A-Z0-9]*\d)(?=[A-Z0-9]*[A-Z])[A-Z]{1,4}\d{2,}[A-Z0-9]*\b|\bSA\d+\b|\b\d{5,}\b")
REPEAT_FILLER = {"personalised", "personalized", "birthday", "card", "mug", "gift", "poster", "print", "mask", "celebrity",
                 "funny", "novelty", "printed", "custom", "retro", "gaming", "game", "kids", "theme", "style", "face",
                 "football", "fancy", "dress", "party", "cardboard", "costume", "sticker", "coaster", "keyring", "magnet",
                 "towel", "case", "cover", "replacement", "baby", "grow", "bodysuit", "name", "office", "adult", "framed",
                 "signed", "star", "inspired", "t-shirt", "tee", "christmas", "stocking", "sack", "santa", "bunting", "unisex"}


def base_clean(title):
    t = title.replace("_", " ").replace("’", "'").replace("‘", "'")
    t = re.sub(r"[“”\"]", "", t)
    for a, b in (("favorite", "favourite"), ("Favorite", "Favourite"), ("FAVORITE", "FAVOURITE"), ("ersonalized", "ersonalised"),
                 ("ERSONALIZED", "ERSONALISED"), ("Color", "Colour"), ("color", "colour"), ("Customized", "Customised"),
                 ("customized", "customised"), ("Mom ", "Mum "), ("Mommy", "Mummy")):
        t = t.replace(a, b)
    for _ in range(3):
        t = re.sub(r"\(([^()]*)\)", lambda m: " " if not re.fullmatch(r"(?i)kids|adults?", m.group(1).strip()) else " [[" + m.group(1) + "]] ", t)
    t = re.sub(r"[()]", " ", t).replace("[[", "(").replace("]]", ")")
    t = re.sub(r"(?i)\bworlds?'?s? best\b", "World's No.1", t)
    t = re.sub(r"(?i)\b(?<!of the )best\b(?! of the best)", "No.1", t) if not BEST_OK.search(t) else t
    t = re.sub(r"\b(\d+) [xX]\b", r"\1 x", t)
    t = re.sub(r"\[(?!\[)[^\]]*\](?!\])", " ", t)
    t = re.sub(r"(?<!\[)\[(?!\[)|(?<!\])\](?!\])|[{}<>]", " ", t)
    t = SIZE_LIST.sub(" ", t)
    letters = [c for c in t if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.6:
        t = " ".join(w if re.sub(r"[^A-Za-z0-9/]", "", w).upper() in ACRONYMS - {"US", "IT", "OK", "LA", "ID", "AM", "PE", "ET", "AU"} else w.lower() for w in t.split())
    t = re.sub(r"\b\d+\s*mm\s*x\s*\d+\s*mm\b|\b\d+\s*x\s*\d+\s*(mm|cm)\b|\b\d+\s*(mm|cm)\b|\b\d+\"", " ", t, flags=re.I)
    t = JUNK_RX.sub(" ", t)
    t = CODE_RX.sub(" ", t)
    t = re.sub(r"\b[a-z0-9]+(-[a-z0-9]+){2,}\b", " ", t)  # pasted handles
    t = re.sub(r"\b(" + "|".join(JUNK_CAPS) + r")\b(?!')", " ", t)
    t = re.sub(r"\s*[|•]\s*", " – ", t)
    t = re.sub(r"\s+[-–—]+\s+|\s+[-–—]+(?=\w)|(?<=\w)[-–—]+\s+|\s*:\s+", " – ", t)
    t = re.sub(r"\s+", " ", t).strip(" -–,.!")
    # tidy each segment
    segs = []
    seen = set()
    for seg in re.split(r"\s+–\s+|,\s+", t):
        seg = seg.strip(" -–,.&+")
        if not seg:
            continue
        key = seg.lower()
        if key in seen:
            continue
        seen.add(key)
        segs.append(tidy_case(seg))
    # remove repeated filler words across the whole title (keep first)
    used = set()
    out = []
    for seg in segs:
        ws = []
        for w in seg.split():
            k = re.sub(r"[^a-z\-]", "", w.lower())
            if k in REPEAT_FILLER and k in used:
                continue
            if ws and k and re.sub(r"[^a-z]", "", ws[-1].lower()) == k:
                continue
            used.add(k)
            ws.append(w)
        s = " ".join(ws).strip(" -–&,")
        s = re.sub(r"\s+(and|&|with|for|of|the|or|a|in)$", "", s, flags=re.I)
        if s:
            out.append(s)
    return out


def words_trim(s, limit):
    """Shorten to <= limit at a word boundary without leaving a dangling small word."""
    if len(s) <= limit:
        return s
    ws = s.split()
    while ws and len(" ".join(ws)) > limit:
        ws.pop()
    while ws and (ws[-1].lower() in SMALL or ws[-1] in {"–", "&", "-", "+"}):
        ws.pop()
    return " ".join(ws)


PRODUCT_NOUNS = r"(mugs?|cushion|bottles?|glass|tumbler|cup|sign|hanger|plaque|medals?|badge|flags?|towel|mat|bags?|armband|scarf|" \
    r"t-shirt|tee|hoodie|jumper|card|bunting|banner|stickers?|labels?|coaster|runner|case|keyring|magnet|poster|print|" \
    r"masks?|sack|stocking|bauble|cap|hat|apron|bib|box|invites|invitations|skin|bowl|portrait|frame|calendar|bookmark|" \
    r"wrapping paper|fleece|sash|socks|clock|jigsaw|puzzle|slate|tile|plate|lanyard|wristband|tattoos?|balloons?|topper)"
LOW_VALUE = r"(?<![-\w])(premium|decorations|including|printed|novelty|custom|style|design|logo|gift|gifts|high quality|quality|" \
    r"durable|lightweight|thick|full colour|unisex|perfect|ideal|great|fun|extra large|standard|ceramic|romantic|" \
    r"retro football|official)(?![-\w])"


def fit_title(core, noun="", extra=""):
    """core: subject words; noun: family words that must stay at the end. Returns SEO title <= 60."""
    core = re.sub(r"\s+", " ", core).strip(" –-,&")
    if extra:
        core = core + " " + extra
    full = (core + (" " + noun if noun else "")).strip()
    full = re.sub(r"\s+", " ", full)
    if len(full) + len(SUFFIX) <= 60:
        return full + SUFFIX
    if len(full) <= 60:
        return full
    room = 60 - (len(noun) + 1 if noun else 0)
    c2 = re.sub(r"\s+", " ", re.sub(LOW_VALUE, "", core, flags=re.I)).strip(" –-")
    c2 = re.sub(r"\s+–\s+–\s+", " – ", c2)
    if len(c2.split()) >= 2 and len(c2) <= room:
        full = (c2 + (" " + noun if noun else "")).strip()
        return full + SUFFIX if len(full) + len(SUFFIX) <= 60 else full
    segs = core.split(" – ")
    while len(segs) > 1 and len(" – ".join(segs)) > room:
        segs.pop()
    c = " – ".join(segs)
    orig = core.split(" – ")
    if len(c) < 15 and len(orig) > 1:
        c = words_trim(" – ".join(orig[:2]), room)
    if not noun and len(c) > room:
        # cut just after the first product noun, if that leaves a real phrase
        m = re.search(r"\b" + PRODUCT_NOUNS + r"\b", c, re.I)
        if m and m.end() >= 15 and m.end() <= room:
            c = c[: m.end()]
    if len(c) > room:
        c2 = re.sub(r"\s+", " ", re.sub(LOW_VALUE, "", c, flags=re.I)).strip(" –-")
        if len(c2.split()) >= 2:
            c = c2
    if len(c) > room and not noun:
        m = None
        for m in re.finditer(r"\b" + PRODUCT_NOUNS + r"\b", c, re.I):
            pass
        if m and m.end() == len(c):
            tail = m.group(0)
            head = words_trim(c[: m.start()].strip(), room - len(tail) - 1)
            c = (head + " " + tail).strip()
    if extra and extra not in c:
        c = words_trim(c, room - len(extra) - 1) + " " + extra
    c = words_trim(c, room)
    c = c.strip(" –-,&")
    return (c + (" " + noun if noun else "")).strip()


def has_noun(s, rx):
    return re.search(rx, s, re.I) is not None


def hsh(s, n):
    return int(hashlib.md5(s.encode()).hexdigest(), 16) % n


# ---------------------------------------------------------------- trademarks
CLUBS = (r"arsenal|aston villa|villa|bournemouth|brentford|brighton|burnley|chelsea|crystal palace|everton|fulham|ipswich|"
         r"leeds|leicester|liverpool|luton|man(chester)? (city|utd|united)|man city|man utd|newcastle|nottingham forest|forest|"
         r"sheffield (utd|united|wednesday)|sheff wednesday|southampton|spurs|tottenham|west ham|westham|wolves|wolverhampton|"
         r"sunderland|middlesbrough|norwich|watford|west brom|stoke|swansea|cardiff|coventry|derby|hull|millwall|"
         r"blackburn|blackpool|bolton|bristol (city|rovers)|birmingham|qpr|reading|preston|plymouth|portsmouth|"
         r"huddersfield|barnsley|rotherham|charlton|wigan|oxford united|peterborough|wrexham|celtic|rangers|aberdeen|"
         r"hearts|hibs|hibernian|dundee|kilmarnock|motherwell|st johnstone|st mirren|ross county|livingston|"
         r"real madrid|barcelona|juventus|psg|bayern|ajax|ac milan|inter milan|lazio|roma|napoli|benfica|porto|"
         r"york city|leyton orient|cheltenham|northampton|bury|doncaster|grimsby|hartlepool|mansfield|gillingham|"
         r"crewe|walsall|tranmere|port vale|carlisle|accrington|morecambe|fleetwood|salford|stevenage|exeter|"
         r"lincoln|shrewsbury|burton|wimbledon|sutton|barrow|harrogate|bradford|notts county|swindon|colchester|"
         r"denver|broncos|nuggets|lakers|yankees|patriots|cowboys|packers|steelers|warrington|wigan warriors|leeds rhinos|"
         r"st helens|saracens|leicester tigers|premier league|championship|ipl|six nations")
BRANDS = (r"nintendo|\bnes\b|snes|super nintendo|sega|mega ?drive|genesis|master ?system|game ?boy|gamecube|game cube|"
          r"dreamcast|saturn|mega cd|32x|playstation|\bps[1-5]\b|psx|xbox|atari|jaguar|lynx|neo ?geo|colecovision|coleco|"
          r"intellivision|odyssey|amiga|cd32|3do|\bn64\b|nintendo 64|switch|wii|"
          r"mario|sonic|pokemon|pikachu|zelda|minecraft|fortnite|roblox|disney|pixar|marvel|\bdc\b|batman|superman|"
          r"spider-?man|avengers|star wars|harry potter|paw patrol|peppa|bluey|frozen|minions?|lego|barbie|hello kitty|"
          r"guinness|peroni|jack daniels|perfectdraft|coca|pepsi|fruit shoot|gtа|\bgta\b|call of duty|fifa|"
          r"wwe|wwf|\bnfl\b|\bnba\b|\bufc\b|\bf1\b|formula 1|family guy|simpsons|south park|gavin and stacey|"
          r"only fools|eastenders|coronation street|love island|x ?factor|strictly|bake off|walking dead|"
          r"james bond|007|star trek|doctor who|dr who|friends|big bang|sex and the city|made in chelsea|towie|"
          r"geordie shore|turtles|tmnt|scooby|spongebob|transformers|power rangers|thomas the tank|hey duggee|"
          r"teletubbies|number ?blocks|cocomelon|super ?hero|captain marvel|cat ?woman|wonder woman|hulk|thor|"
          r"iron man|deadpool|joker|harley quinn|yoda|jedi|sith|mandalorian|grogu|shrek|toy story|cars|lexus|"
          r"ferrari|lamborghini|porsche|pagani|bugatti|mclaren|bmw|audi|mercedes|aston martin|jaguar|land rover|"
          r"ford|vauxhall|volkswagen|\bvw\b|mini cooper|tesla|honda|yamaha|kawasaki|ducati|harley")


SHOWS = re.compile(r"\b(" + CLUBS + r"|walking dead|love island|friends|big bang theory|big bang|eastenders|sex and the city|made in chelsea|towie|"
                   r"geordie shore|james bond|007|star trek|doctor who|dr who|x ?factor|strictly|bake off|coronation street|"
                   r"only fools|gavin and stacey|six nations|wwe|wwf|ufc|nfl|nba|f1|marvel|batman|spider-?man|deadpool|hulk|"
                   r"star wars|harry potter|game of thrones|i'?m a celebrity|benidorm|neighbours|the hangover|madmen|mad men|"
                   r"one direction|eurovision|olympics( 2012)?|man city|man utd)\b", re.I)


def is_tm(o, fam):
    t = o["title"] + " " + (o["productType"] or "")
    if fam in ("case", "magnet", "keyring"):
        return True
    if "third-party-name" in (o.get("tags") or []):
        return True
    if re.search(r"inspired|theme\b|style theme", o["title"], re.I) and fam not in ("mask",):
        return True
    if re.search(r"\b(" + CLUBS + r")\b", t, re.I):
        return True
    if re.search(r"\b(" + BRANDS + r")\b", t, re.I):
        return True
    if fam == "card" and re.search(r"gaming|movie|sport|celebrity|music|kids cards|car cards", o["productType"] or "", re.I):
        return True
    return False


def is_personalised(o):
    s = o["title"] + " " + " ".join(o.get("tags") or [])
    return bool(re.search(r"personali[sz]|custom|any name|your name|add name|with name|name on|own photo|your photo|any text", s, re.I))


def is_rude(o):
    t = o["title"]
    return bool(PROFANE.search(t) or re.search(r"\b(rude|naughty|porn\w*|sex|sexy|willy|boobs|penis|orgasm|horny|wank\w*|slut|"
                                              r"dildo|m\.?i\.?l\.?f|d\.?i\.?l\.?f|g\.?i\.?l\.?f|[a-z]x{2,}\w*|\w+\*+\w*)\b", t, re.I)
                or re.search(r"rude", o["productType"] or "", re.I))


# ---------------------------------------------------------------- per family titles
SPORTS = [("NFL", r"\bnfl\b|american football"), ("Basketball", r"basketball|\bnba\b"), ("Boxing", r"boxing|boxer"),
          ("Rugby", r"rugby"), ("Cricket", r"cricket"), ("Darts", r"darts"), ("Golf", r"golf"), ("UFC", r"\bufc\b|mma"),
          ("Wrestling", r"wrestl|wwe"), ("Tennis", r"tennis"), ("F1", r"\bf1\b|formula 1"), ("Ice Hockey", r"hockey"),
          ("Baseball", r"baseball"), ("Snooker", r"snooker"), ("Horse Racing", r"horse racing|jockey"),
          ("Athletics", r"athlet"), ("Music", r"music|singer|rapper|band|rock"), ("Movie", r"movie|film|actor|actress"),
          ("TV", r"\btv\b|television"), ("Football", r"football|soccer|\bfc\b")]

SIGNED_JUNK = re.compile(r"\b(printed signature|signed|autographed|autograph|signature|limited|edition|print|prints|poster|posters|"
                         r"framed|frame|black|silver|gold|white|merch|gift|gifts|star|photo|picture|wall art|tribute|display|"
                         r"reproduction|printed|artwork|fan|fans|collectors?|for|with|jersey|number|by|a4|a3|a2|a1|a0|and)\b", re.I)


def signed_title(o, segs):
    pt = o["productType"] or ""
    t = o["title"]
    for prefix in sorted({p.strip() for p in pt.split(",") if p.strip()}, key=len, reverse=True):
        t = re.sub(r"^\s*" + re.escape(prefix) + r"[\s,]*", "", t, flags=re.I)
    segs = base_clean(t)
    first = segs[0] if segs else t
    # the subject is everything before the first junk word run
    words = first.split()
    subj = []
    for w in words:
        if SIGNED_JUNK.fullmatch(re.sub(r"[^A-Za-z0-9 ]", "", w)) and len(subj) >= 2:
            break
        if SIGNED_JUNK.fullmatch(re.sub(r"[^A-Za-z0-9 ]", "", w)):
            continue
        subj.append(w)
    subj = [w for w in subj if not re.fullmatch(r"\d", w)] or subj
    num = re.search(r"\b(\d)\b", first)
    name = " ".join(subj).strip(" –-")
    name = re.sub(r"\b(Football Player|Footballers?|Football|Player|Rugby Player|Boxer|Golfer|Cricketer|Darts|Rugby|Boxing|Golf|Cricket|NFL)$", "", name).strip()
    if not name:
        name = tidy_case(first)
    sport = ""
    hay = (o["title"] + " " + pt).lower()
    for s, rx in SPORTS:
        if re.search(rx, hay):
            sport = s
            break
    kind = "Poster" if re.search(r"poster", o["title"], re.I) and not re.search(r"\bprint\b", o["title"], re.I) else "Print"
    extra = f"Design {num.group(1)}" if num and num.group(1) != "1" else ""
    cands = []
    for core in ([f"{name} {sport}".strip()] if sport and sport.lower() not in name.lower() else []) + [name]:
        cands.append(f"{core} Printed Signature {kind}")
    for c in cands:
        if len(c) + len(SUFFIX) <= 60:
            return c + SUFFIX, name, sport, extra
    for c in cands:
        if len(c) <= 60:
            return c, name, sport, extra
    return fit_title(name, f"Printed Signature {kind}"), name, sport, extra


MUG_JUNK = re.compile(r"\b(i love mug|football crazy|adult office|adult gift|gaming mugs|novelty funny printed mug|novelty funny mug|funny printed mug|printed mug|celebrity mug|adult office mug|"
                      r"office mug|adult mug|personalised mug|tv show mug|funny mug|mug)\b", re.I)


def drop_best(s):
    s2 = re.sub(r"\bworld'?s best\b", "", s, flags=re.I)
    s2 = re.sub(r"\bbest\b", "", s2, flags=re.I)
    s2 = re.sub(r"\s+", " ", s2).strip(" –-")
    return s2, s2 != s


def generic_title(o, segs, noun, noun_rx, max_segs=2, drop_rx=None):
    segs = [s for s in segs if not (drop_rx and re.fullmatch(drop_rx, s, re.I))]
    core = " – ".join(segs[:max_segs]) if segs else tidy_case(o["title"])
    core, had_best = drop_best(core)
    if drop_rx:
        core = re.sub(drop_rx, "", core, flags=re.I).strip()
    core = re.sub(r"\s+", " ", core).strip(" –-&,")
    if had_best and not re.search(r"\b(funny|novelty)\b", core, re.I):
        core = "Funny " + core
    if noun and has_noun(core, noun_rx):
        # move nothing; noun already present
        return fit_title(core)
    return fit_title(core, noun)


def make_title(o, fam):
    t = o["title"]
    if fam in ("poster", "display"):
        t = re.sub(r"\b(hand[- ]?)?(signed|autographed)( and autographed)?\b|\bautograph\b", "Printed Signature", t, flags=re.I)
        t = re.sub(r"(Printed Signature)(.*?)\s*\bPrinted Signature\b", r"\1\2", t)
    elif fam != "signed":
        t = re.sub(r"\bsigned for\b|\b(hand[- ]?)?signed\b|\bautograph(ed)?\b", " ", t, flags=re.I)
    segs = base_clean(t)
    segs = [PROFANE.sub(censor, s) for s in segs]
    info = {}
    if fam == "signed":
        title, name, sport, extra = signed_title(o, segs)
        info.update(name=name, sport=sport, extra=extra)
        return title, info
    if fam == "mask":
        first = segs[0] if segs else "Fancy Dress Party"
        name = re.split(r"\s+(?:Celebrity|Face|Fancy|Party|Mask|Cardboard|Costume|Music Star|Footballer|Actor|Movie|Tv|Golf|"
                        r"Rugby|Cricket|Tennis|Darts|Snooker|Boxer|F1|Politician|Royal|Sports?)\b", first, maxsplit=1)[0]
        name = re.split(r"\s+(?:19|20)\d\d\b|\s+Dress\b", name)[0]
        name = re.sub(r"\s+\d{4}$|\s+\d$", "", name).strip(" –-")
        if not name or re.search(r"personali|custom|photo|pack|\bx\b", t, re.I):
            name = re.sub(r"\b(face masks?|masks?)\b", "", segs[0] if segs else "Fancy Dress Party", flags=re.I).strip()
        info["name"] = name
        return fit_title(name, "Face Mask" if not re.search(r"masks\b", t, re.I) or re.search(r"\b1 x\b", t, re.I) else "Face Masks"), info
    if fam == "mug":
        segs2 = []
        for s in segs:
            s = re.sub(r"^(Red|Black|Pink|Blue|White|Green) Mug$", "", s, flags=re.I)
            s = MUG_JUNK.sub("", s)
            s = re.sub(r"\bPersonalised Your Custom Name\b", "Personalised", s, flags=re.I)
            s = re.sub(r"\s+", " ", s).strip(" –-")
            if s and not re.fullmatch(r"(?i)(novelty|funny|celebrity|novelty funny|adult|office|custom|gift)( \w+)?", s):
                segs2.append(s)
        colour = re.match(r"^(RED|BLACK|PINK|BLUE|GREEN) MUG", t)
        noun = (colour.group(1).title() + " Mug") if colour else "Mug"
        core = " – ".join(segs2[:2]) if segs2 else "Novelty"
        core, had_best = drop_best(core)
        if had_best:
            core = "Funny " + core if not re.search(r"funny|novelty", core, re.I) else core
        return fit_title(core, noun), info
    if fam == "card":
        segs2 = []
        for s in segs:
            s = re.sub(r"\b(Birthday Card|Card|Kidshows|Kids Adult|Funny|Celebrity|Movie|Game|Musician|Kids)\b", lambda m: m.group(0) if m.group(0) in ("Funny",) else "", s)
            s = re.sub(r"\bPersonalised\b", "", s, flags=re.I)
            s = re.sub(r"^Signed For\b", "", s)
            s = re.sub(r"\s+", " ", s).strip(" –-&")
            if s:
                segs2.append(s)
        num = None
        core = segs2[0] if segs2 else ""
        m = re.search(r"\s(\d{1,2})$", core)
        if m and not re.search(r"\b(age|aged|turning)\b", core, re.I):
            num = m.group(1)
            core = core[: m.start()].strip()
        core, had_best = drop_best(core)
        kind = "Birthday Card"
        for k, rx in [("Christmas Card", r"christmas|xmas"), ("Valentine's Card", r"valentine"), ("Father's Day Card", r"father'?s day"),
                      ("Mother's Day Card", r"mother'?s day"), ("Anniversary Card", r"anniversary"), ("Wedding Card", r"wedding"),
                      ("Retirement Card", r"retire"), ("Leaving Card", r"leaving"), ("New Baby Card", r"new baby"),
                      ("Get Well Card", r"get well"), ("Thank You Card", r"thank you"), ("Engagement Card", r"engage"),
                      ("Good Luck Card", r"good luck"), ("Birthday Card", r"birthday")]:
            if re.search(rx, t, re.I):
                kind = k
                break
        KREM = {"Father's Day Card": r"(happy )?father'?s'? day", "Mother's Day Card": r"(happy )?mother'?s'? day",
                "Valentine's Card": r"(happy )?valentine'?s?( day)?", "Christmas Card": r"(merry )?(christmas|xmas)",
                "Birthday Card": r"(happy )?birthday", "Anniversary Card": r"(happy )?anniversary", "Thank You Card": r"thank you",
                "Get Well Card": r"get well( soon)?", "Good Luck Card": r"good luck", "New Baby Card": r"new baby"}
        core = re.sub(r"\b" + KREM.get(kind, re.escape(kind.split()[0])) + r"\b", "", core, flags=re.I).strip()
        core = re.sub(r"\s+", " ", core).strip(" –-&")
        pers = "Personalised " if re.search(r"personali", t, re.I) else ""
        info["num"] = num
        if not core:
            return fit_title(pers.strip(), kind), info
        return fit_title(pers + core, kind), info
    if fam == "case":
        console = ""
        for c, rx in [("Mega Drive", r"mega ?drive|genesis"), ("Master System", r"master ?system"), ("Mega CD", r"mega ?cd"),
                      ("SNES", r"snes|super nintendo"), ("NES", r"\bnes\b"), ("Game Boy Color", r"game ?boy colou?r|gbc"),
                      ("Game Boy Advance", r"advance|\bgba\b"), ("Game Boy", r"game ?boy"), ("N64", r"\bn64\b|nintendo ?64"),
                      ("GameCube", r"game ?cube"), ("PS1", r"playstation|\bps1\b|psx"), ("Dreamcast", r"dreamcast"),
                      ("Saturn", r"saturn"), ("Atari 2600", r"2600"), ("Atari 5200", r"5200"), ("Atari 7800", r"7800"),
                      ("Atari Jaguar", r"jaguar"), ("ColecoVision", r"coleco|colevision"), ("Odyssey 2", r"odyssey|oddesey"),
                      ("Amiga CD32", r"cd32|amiga")]:
            if re.search(rx, t + " " + (o["productType"] or ""), re.I):
                console = c
                break
        g = t
        g = re.sub(r"(?i)\b(sega|nintendo|genesis|megadrive|mega drive|master system|mastersystem|snes|super nintendo|nes|"
                   r"playstation 1|playstation|ps1|psx|game ?boy colou?r|game ?boy advance|game ?boy|gamecube|game cube|dreamcast|dc|"
                   r"saturn|atari|2600|5200|7800|jaguar cd|jaguar|coleco ?vision|colevision|odyssey 2|odyssey|amiga|cd32|n64|"
                   r"replacement|retro|gaming|game|case|cases|or|cover|covers|for|retail|to fit a ugc style|to fit|ugc style|ugc|3d boxes|"
                   r"boxes|box|pal|eu|au|us|uk|jp|ntsc|inspired|style|theme|custom)\b", " ", g)
        g = " ".join(base_clean(g)[:1]) or "Retro Game"
        g = re.sub(r"\s+", " ", g).strip(" –-")
        info["game"] = g
        info["console"] = console
        noun = f"{console} Replacement Case".strip() if console else "Replacement Game Case"
        return fit_title(g, noun), info
    if fam in ("magnet", "keyring"):
        console = ""
        for c, rx in [("NES", r"\bnes\b"), ("SNES", r"snes"), ("Mega Drive", r"mega ?drive|genesis"), ("Master System", r"master ?system"),
                      ("Mega CD", r"mega ?cd"), ("Saturn", r"saturn"), ("Dreamcast", r"dreamcast"), ("PS1", r"playstation 1|\bps1\b|playstation$"),
                      ("PS4", r"\bps4\b|playstation 4"), ("GameCube", r"game ?cube"), ("Game Boy Advance", r"advance"),
                      ("Game Boy Color", r"colou?r"), ("Game Boy", r"game ?boy"), ("Atari 2600", r"2600"), ("Atari 5200", r"5200"),
                      ("Atari 7800", r"7800"), ("Atari Jaguar", r"jaguar"), ("Atari XE", r"atari xe"), ("Neo Geo", r"neo ?geo"),
                      ("CD32", r"cd32"), ("Odyssey", r"odyssey"), ("Coleco", r"coleco"), ("3DO", r"3do"), ("32X", r"32x")]:
            if re.search(rx, (o["productType"] or "") + " " + t, re.I):
                console = c
                break
        g = re.sub(r"(?i)\b(retro|nintendo|sega|nes|snes|mega ?drive|genesis|master ?system|mega cd|saturn|dreamcast|dc|playstation 1|"
                   r"playstation 4|playstation|ps1|ps4|gamecube|game cube|game ?boy advance|game ?boy colou?r|game ?boy|gba|atari 2600|"
                   r"atari 5200|atari 7800|atari jaguar cd|atari jaguar|atari xe|atari|2600|5200|7800|jaguar|neo ?geo|cd32|odyssey|"
                   r"coleco|3do|32x|x32|game|inspired|gaming|fridge|magnet|keyring|cover|art|eu|au|us|pal|jp|theme|style)\b", " ", t)
        g = re.sub(r"\s\d{2,4}$", "", g.strip())
        g = " ".join(base_clean(g)[:1]) or "Retro Game"
        info["game"] = g
        info["console"] = console
        noun = ("Retro " + (console + " " if console else "") + ("Fridge Magnet" if fam == "magnet" else "Keyring")).replace("  ", " ")
        return fit_title(g, noun), info
    if fam == "babygrow":
        s = " – ".join(segs[:1])
        s = re.sub(r"(?i)\b(baby grow bodysuit|baby boy girl unisex short sleeve bodysuit|boy girl unisex|unisex|short sleeve|"
                   r"bodysuit|baby grow|baby vest|printed|gift|baby boy girl|boy girl)\b", "", s)
        s = re.sub(r"\s+", " ", s).strip(" –-")
        s, hb = drop_best(s)
        return fit_title(s, "Baby Grow"), info
    if fam == "christmas":
        s = segs[0] if segs else t
        name = ""
        if re.search(r"santa sack", t, re.I):
            noun = "Santa Sack"
        elif re.search(r"stocking", t, re.I):
            noun = "Christmas Stocking"
        elif re.search(r"bauble", t, re.I):
            noun = "Bauble"
        else:
            noun = ""
        s = re.sub(r"(?i)\b(xl|large|children's|childrens|christmas|santa sack|stocking|present|cartoon|super hero|hero|bauble)\b", "", s)
        s = re.sub(r"\s+", " ", s).strip(" –-")
        if not s.lower().startswith("personalised") and re.search(r"personali", t, re.I):
            s = "Personalised " + s
        return fit_title(s, noun), info
    NOUNS = {
        "coaster": ("Coaster", r"coaster|bar mat|runner|placemat"),
        "cushion": ("Cushion", r"cushion|pillow"),
        "towel": ("Towel", r"towel"),
        "sticker": ("Sticker", r"sticker|decal|label"),
        "party": ("", r"."),
        "pets": ("", r"."),
        "glassware": ("", r"."),
        "clothing": ("", r"."),
        "plaque": ("", r"."),
        "poster": ("Poster", r"poster|print|art"),
        "mousemat": ("Mouse Mat", r"mat\b|pad\b"),
        "display": ("Lego Display Case", r"display case"),
        "generic": ("", r"."),
    }
    noun, rx = NOUNS.get(fam, ("", r"."))
    if fam == "display":
        s = segs[0] if segs else t
        s = re.sub(r"(?i)\b(signed|lego|display case|minifigure|display|background|and frames)\b", "", s)
        s = re.sub(r"\s+", " ", s).strip(" –-")
        return fit_title(s, "Minifigure Display Case"), info
    if fam == "coaster":
        m = re.search(r"(?i)thinking about (.+?)\W*hobby coaster", t)
        m2 = re.search(r"(?i)listening to you but\W*\(([^)]+)\)", t)
        if m or m2:
            hobby = tidy_case((m or m2).group(1).lower())
            return fit_title(hobby, "Coaster – I Might Look Like I'm Listening" if m else "Coaster – I May Look Like I'm Listening"), info
    if fam == "towel":
        s = segs[0] if segs else t
        s = re.sub(r"(?i)\blightweight beach gym towel\b", "Beach Towel", s)
        return generic_title(o, [s] + segs[1:], noun, rx, 1), info
    return generic_title(o, segs, noun, rx, 2 if fam not in ("coaster",) else 1), info


# ---------------------------------------------------------------- metas
def lower_first(s):
    return s[:1].lower() + s[1:] if s and not re.match(r"[A-Z]{2}|I\b", s) else s


FAM_GENERIC = {
    "card": "personalised card", "mug": "printed mug", "mask": "celebrity face mask", "signed": "printed signature print",
    "poster": "poster print", "case": "replacement game case", "magnet": "retro gaming fridge magnet",
    "keyring": "retro gaming keyring", "babygrow": "baby grow", "clothing": "printed top", "coaster": "drinks coaster",
    "cushion": "cushion", "towel": "printed towel", "sticker": "sticker", "party": "party piece", "christmas": "Christmas gift",
    "pets": "pet gift", "glassware": "printed glass", "plaque": "sign", "generic": "printed gift", "mousemat": "mouse mat",
    "display": "minifigure display case",
}

FACTS = {
    "card": ["Printed on thick 350gsm card, folded to A5, with a free white envelope.",
             "It's printed on 350gsm silk art board and comes with a white envelope.",
             "Posted Royal Mail 1st Class, dispatched the same or next working day.",
             "Sent 1st Class in a board-backed envelope so it arrives flat."],
    "mask": ["Printed on 350gsm silk card, cut to shape with eye holes and elastic.",
             "A4 size on 350gsm card, with eye holes cut and elastic included.",
             "Posted in a board-backed envelope so it arrives flat."],
    "mug": ["An 11oz white ceramic mug that's dishwasher and microwave safe.",
            "Printed on an 11oz glossy ceramic mug, safe in the dishwasher and microwave.",
            "Sublimation printed, so the design is part of the glaze."],
    "signed": ["The signature is printed as part of the design, not added by hand.",
               "A printed reproduction: the signature is part of the print.",
               "Printed to order in our North Yorkshire workshop."],
    "poster": ["Printed to order in our North Yorkshire workshop.",
               "Made in-house in North Yorkshire."],
    "case": ["It's a printed case or cover only; no game is included.",
             "Printed in-house in North Yorkshire. No game included.",
             "Made to order in our North Yorkshire workshop; no game included."],
    "magnet": ["Printed in-house in North Yorkshire in full colour.", "Made to order in our North Yorkshire workshop."],
    "keyring": ["Printed in-house in North Yorkshire in full colour.", "Made to order in our North Yorkshire workshop."],
    "babygrow": ["Soft 100% cotton with short sleeves and nickel-free poppers.",
                 "Made from 100% cotton with nickel-free poppers. Wash inside out."],
    "glassware": ["Full-colour UV print, kept clear of the rim. Hand wash recommended.",
                  "Printed in full colour in-house; hand washing keeps it bright."],
    "party": ["Printed in-house in our North Yorkshire workshop.", "Made to order in North Yorkshire."],
    "bunting": ["A5 flags on 300gsm silk card, ready to thread and hang.",
                "Semi-waterproof 300gsm card flags, simply thread and hang."],
}
DEFAULT_FACTS = ["Made to order in our North Yorkshire workshop.", "Printed in-house in North Yorkshire, UK.",
                 "Custom designs are available on request."]
CTAS = ["Order yours today.", "Order today.", "Add it to your basket today.", "Treat them today.", "Order now and make their day."]
XMAS_CTAS = ["Order early for Christmas.", "Order yours today.", "Get it ordered for Christmas."]

OPEN = {
    "card": ["Make their day with this {name}.", "Send a smile with this {name}.", "This {name} is a lovely way to mark their big day.",
             "Our {name} is made to make someone feel special.", "A {name} they'll want to keep."],
    "mug": ["Brighten their brew with this {name}.", "This {name} makes a fun gift for any tea or coffee lover.",
            "Start the day with a smile thanks to this {name}.", "Our {name} is a cheerful gift for the office or home.",
            "Give them a laugh with this {name}."],
    "mask": ["Be the life of the party with this {name}.", "Get the party started with this {name}.",
             "Our {name} is perfect for stag dos, hen parties and fancy dress.", "Turn heads at any party with this {name}.",
             "This {name} is a fun pick for birthdays, stag and hen dos."],
    "signed": ["Celebrate a favourite with this {name}.", "This {name} makes a great gift for fans.",
               "Add this {name} to your wall or give it as a gift.", "Our {name} is a lovely gift for any fan.",
               "Show your support with this {name}."],
    "poster": ["Brighten up a wall with this {name}.", "This {name} makes a thoughtful gift.",
               "Our {name} adds a personal touch to any room.", "Give a room some character with this {name}."],
    "case": ["Give your game a fresh look with this {name}.", "Tidy up your collection with this {name}.",
             "This {name} is a neat way to rehouse a loose cartridge or disc.", "Restore your shelf with this {name}."],
    "magnet": ["Add some retro fun to the fridge with this {name}.", "This {name} is a fun gift for any retro gamer.",
               "Bring back the classics with this {name}.", "A nostalgic {name} for gamers of all ages."],
    "keyring": ["Keep your keys retro with this {name}.", "This {name} is a fun little gift for any gamer.",
                "Carry a classic with you on this {name}.", "A nostalgic {name} for retro gaming fans."],
    "babygrow": ["Dress the little one in this {name}.", "This {name} makes a sweet gift for a new arrival.",
                 "Our {name} is a fun pick for baby showers and new babies.", "A cute {name} for proud families."],
}
DEFAULT_OPEN = ["Treat someone special to this {name}.", "Add a personal touch with this {name}.",
                "Brighten someone's day with this {name}."]
PERS = {
    "card": ["Add their name, age and your own message inside.", "Personalise it with a name, age and message.",
             "Add a name, age and a message inside before you order."],
    "mug": ["Add their name to make it their own.", "Personalise it with a name before you order.", "Add any name to make it unique."],
    "mask": ["Send us a clear, front-facing photo to make it.", "Made from the photo you upload."],
    "babygrow": ["Add a name to make it their own.", "Personalise it with the baby's name."],
    "christmas": ["Add their name to make it their own.", "Personalise it with any name."],
    "poster": ["Add the name or text you'd like.", "Personalise it with your own name or text."],
}
DEFAULT_PERS = ["Personalise it with your own name or text.", "Add the name or text you'd like.", "Add a name to make it theirs."]
SHORT_FACTS = {
    "card": ["Thick 350gsm card with a free envelope.", "Posted 1st Class with a free envelope.",
             "Folded to A5 on 350gsm card.", "Dispatched the same or next working day."],
    "mask": ["350gsm card with eye holes and elastic.", "Cut to shape with eye holes."],
    "mug": ["Dishwasher and microwave safe.", "11oz ceramic, dishwasher safe."],
    "signed": ["The signature is printed in the design.", "Printed in North Yorkshire."],
    "poster": ["Printed in North Yorkshire.", "Made to order in-house."],
    "case": ["No game included.", "Printed in North Yorkshire."],
    "magnet": ["Printed in North Yorkshire."], "keyring": ["Printed in North Yorkshire."],
    "babygrow": ["100% cotton with nickel-free poppers.", "Wash and iron inside out."],
    "glassware": ["Hand wash recommended."],
    "bunting": ["Ready to thread and hang.", "Semi-waterproof 300gsm card."],
}
SHORT_DEFAULT = ["Made to order in North Yorkshire.", "Custom designs on request."]
NAMED = {
    "card": ["a card they'll want to keep", "made to make their day", "a lovely way to mark the occasion", "a card with a personal touch"],
    "mug": ["a fun gift for any tea or coffee lover", "a cheerful gift for home or the office", "a smile with every cuppa",
            "a mug that brightens every brew"],
    "mask": ["perfect for stag dos, hen parties and fancy dress", "a fun pick for birthdays and photo booths",
             "guaranteed laughs at any party", "a crowd-pleaser for fancy dress and nights out"],
    "signed": ["a great gift for any fan", "a striking piece for a fan's wall", "a lovely gift for a true fan"],
    "poster": ["a thoughtful gift and an easy way to brighten a wall", "wall art that adds character to any room",
               "a great gift for their wall"],
    "babygrow": ["a sweet gift for a new arrival", "a cute pick for baby showers", "a fun outfit for proud families"],
    "clothing": ["a fun top for parties, gifts and days out", "a great gift that's made to order", "made to stand out"],
    "coaster": ["a fun little gift for the home or office", "a cheerful gift for anyone who loves a cuppa",
                "a fun gift for the home bar"],
    "cushion": ["a cosy gift that adds a personal touch to any room", "a lovely gift for the sofa or bedroom"],
    "towel": ["a great gift for the beach, gym or bathroom", "a handy gift for holidays and the gym"],
    "sticker": ["printed to order for your home, car or business", "a quick way to add some personality"],
    "party": ["a fun finishing touch for any celebration", "made to make the party"],
    "christmas": ["a festive gift that makes Christmas extra special", "a lovely way to start a family tradition"],
    "pets": ["a thoughtful gift for pet lovers", "made for proud pet owners"],
    "glassware": ["a thoughtful gift for any occasion", "a gift they'll use again and again"],
    "plaque": ["a thoughtful gift and a great talking point", "a fun finishing touch for the home"],
    "mousemat": ["a great upgrade for any desk or gaming setup", "a fun gift for gamers and home workers"],
    "display": ["a great way to show off your minifigures"],
}
NAMED_DEFAULT = ["a thoughtful gift, made to order", "a fun gift for someone special", "a great gift idea for any occasion"]
RUDE_OPEN = ["A cheeky novelty {noun} for someone with a wicked sense of humour.",
             "This tongue-in-cheek {noun} is a gift for friends who like a laugh.",
             "A naughty-but-nice {noun} for adults with a sense of humour."]


KEYS = ("dishwasher", "north yorkshire", "custom designs", "350gsm", "envelope", "thread", "cotton", "signature", "game",
        "hand wash", "eye holes", "1st class", "folded", "printed in")


def _overlap(a, b):
    a, b = a.lower(), b.lower()
    return a in b or b in a or any(k in a and k in b for k in KEYS)


def meta_for(o, fam, info, seo_title):
    rude = is_rude(o)
    tm = is_tm(o, fam)
    pers = is_personalised(o)
    h = o["handle"]
    xmas = re.search(r"christmas|xmas|santa|stocking|bauble", o["title"], re.I) is not None
    noun = FAM_GENERIC[fam]
    if fam == "party" and re.search(r"bunting", o["title"], re.I):
        noun = "personalised bunting" if pers else "printed bunting"
    if fam == "christmas":
        noun = "personalised " + ("Santa sack" if re.search(r"sack", o["title"], re.I) else "Christmas stocking" if re.search(r"stocking", o["title"], re.I) else "Christmas gift")
        if not pers:
            noun = noun.replace("personalised ", "")
    if fam == "card" and pers:
        noun = "personalised " + (re.search(r"(Birthday|Christmas|Valentine's|Father's Day|Mother's Day|Anniversary|Wedding|Retirement|Leaving|New Baby|Get Well|Thank You|Engagement|Good Luck) Card", seo_title) or re.search("(Birthday) Card", "Birthday Card")).group(0).replace("Birthday Card", "birthday card").replace("Card", "card")
    if fam == "card" and not pers:
        noun = "printed card"
    # specific name
    core = re.sub(re.escape(SUFFIX) + "$", "", seo_title)
    named = None
    if fam == "mask":
        named = re.sub(r"\s+", " ", core if re.search(r"face masks?$", core, re.I) else f"{info.get('name') or core} Face Mask")
    elif fam == "signed":
        if not re.search(r"\b(" + CLUBS + r")\b", info["name"], re.I):
            named = f"{info['name']} Printed Signature Print"
    elif not tm and not rude:
        named = re.sub(r"\s+–\s+", " ", core)
    if named and fam in ("mask", "signed"):
        named = re.sub(r"\s+", " ", SHOWS.sub("", named)).strip(" –-")
        if len(named.split()) < 3:
            named = None
    if named and (len(named) > 75 or problems(named)):
        named = None
    sets = []
    if named:
        sets.append([f"{named}: {b}." for b in NAMED.get(fam, NAMED_DEFAULT)])
    gen = RUDE_OPEN if rude else OPEN.get(fam, DEFAULT_OPEN)
    sets.append([g.replace("{name}", noun).replace("{noun}", noun) for g in gen])
    if fam == "party" and "bunting" in noun:
        facts = FACTS["bunting"]
    else:
        facts = FACTS.get(fam, DEFAULT_FACTS)
    perss = PERS.get(fam, DEFAULT_PERS) if pers else [""]
    if fam == "mask" and not re.search(r"photo|personali|custom", o["title"], re.I):
        perss = [""]
    if fam == "mask" and perss != [""]:
        facts = FACTS["mask"] + ["Dispatched the next working day."]
    ctas = XMAS_CTAS if xmas else CTAS
    shorts = SHORT_FACTS.get("bunting" if (fam == "party" and "bunting" in noun) else fam, SHORT_DEFAULT)
    extras = shorts + ["Made in North Yorkshire.", "A great gift idea."]
    rot = hsh(h, 1000003)

    def rotl(lst, k):
        if not lst:
            return lst
        k = k % len(lst)
        return lst[k:] + lst[:k]

    ps_r = rotl(perss, rot // 7) + ([""] if perss != [""] else [])
    fc_r = rotl(facts + shorts, rot // 13)
    ex_r = [""] + rotl(extras, rot // 17)
    ct_r = rotl(ctas, rot // 19)
    for opens in sets:
        ops_r = rotl(opens, rot)
        for want_ct in (True, False):
            for op0 in ops_r:
                op = op0
                op = re.sub(r"\b([Aa]) ([aeiouAEIOU])", lambda m: m.group(1) + "n " + m.group(2), op)
                op = op[:1].upper() + op[1:]
                for ps in ps_r:
                    for fc in fc_r:
                        for ex in ex_r:
                            if ex and _overlap(ex, fc):
                                continue
                            for ct in (ct_r if want_ct else [""]):
                                n = len(op) + len(ps) + len(fc) + len(ex) + len(ct) + sum(1 for p in (ps, fc, ex, ct) if p)
                                if 140 <= n <= 155:
                                    s = " ".join(p for p in (op, ps, fc, ex, ct) if p)
                                    s = re.sub(r"\s+", " ", s).strip()
                                    if 140 <= len(s) <= 155:
                                        return s
    return None


# ---------------------------------------------------------------- validation
def title_ok(s):
    return bool(s) and len(s) <= 60 and not problems(s)


def meta_ok(s):
    return bool(s) and 140 <= len(s) <= 155 and not problems(s)


def problems(s):
    p = []
    s0 = BEST_OK.sub("", s)
    if BANNED.search(s0):
        p.append("banned:" + BANNED.search(s0).group(0))
    if PROFANE.search(s):
        p.append("profanity")
    for w in re.findall(r"\b[A-Z][A-Z0-9/]{3,}\b", s.replace("'s", "").replace("'", " ")):
        if w not in ACRONYMS and not re.search(r"\d", w):
            p.append("caps:" + w)
            break
    if "  " in s:
        p.append("double space")
    if re.search(r" - -|–\s*–|-\s*–|–\s*-", s):
        p.append("dash run")
    if re.search(r"[{}\[\]]", s):
        p.append("placeholder")
    if re.search(r"live preview", s, re.I):
        p.append("preview")
    return p


def main():
    P = json.load(open(os.path.join(HERE, "scope.json")))
    # earlier face mask copy (same SEO the face-mask import uses)
    mask_seo = {}
    for f in ("masks-00-TEST.csv", "masks-01.csv", "masks-02.csv"):
        p = os.path.join("/home/user/panda/foxyprinting-rebrand/exports/face-masks", f)
        if os.path.exists(p):
            for r in csv.DictReader(open(p, newline="", encoding="utf-8")):
                mask_seo[r["Handle"]] = (r["SEO Title"], r["SEO Description"])
    rows = []
    stats = collections.Counter()
    fails = []
    existing = collections.Counter()
    for o in P:
        et = (o["seo"] or {}).get("title") or ""
        if et and title_ok(et):
            existing[(_family(o), et.lower())] += 1
    for o in P:
        if o["productType"] == "OPTIONS_HIDDEN_PRODUCT":
            stats["skipped helper (OPTIONS_HIDDEN_PRODUCT)"] += 1
            continue
        fam = _family(o)
        if fam == "mask" and re.search(r"face covering", o["title"], re.I):
            fam = "generic"
        old_t = (o["seo"] or {}).get("title") or ""
        old_d = (o["seo"] or {}).get("description") or ""
        t_ok, d_ok = title_ok(old_t), meta_ok(old_d)
        fam0 = _family(o)
        if t_ok and existing[(fam0, old_t.lower())] > 1:
            t_ok = False  # shared with another product in the same family
        if t_ok and d_ok:
            stats["already fine"] += 1
            continue
        new_t, info = make_title(o, fam)
        if fam == "mask" and o["handle"] in mask_seo:
            mt, md = mask_seo[o["handle"]]
            if title_ok(mt):
                new_t = mt
            good = meta_ok(md) and md.endswith(".") and not re.search(r"\ba [AEIOU]|\b(in|a|the|and|to|for)\.$", md)
            info["mask_meta"] = md if good else None
        rows.append(dict(handle=o["handle"], fam=fam, old_title=o["title"], old_seo_t=old_t, old_seo_d=old_d,
                         t=old_t if t_ok else new_t, d=old_d if d_ok else None, wrote_t=not t_ok, wrote_d=not d_ok,
                         info={k: v for k, v in info.items() if k != "mask_meta"}, _o=o, _mm=info.get("mask_meta")))
    # de-duplicate SEO titles within each family
    by = collections.defaultdict(list)
    for r in rows:
        by[(r["fam"], r["t"].lower())].append(r)
    taken_by = collections.defaultdict(set)
    for r in rows:
        taken_by[r["fam"]].add(r["t"].lower())
    for (fam, _), group in by.items():
        if len(group) < 2:
            continue
        taken = taken_by[fam]
        for i, r in enumerate(group[1:], start=2):
            if not r["wrote_t"]:
                continue
            core = re.sub(re.escape(SUFFIX) + "$", "", r["t"])
            cand_words = []
            raw = re.sub(r"[()\[\],|–\-]", " ", r["old_title"])
            if r["fam"] != "signed":
                for w in raw.split():
                    wl = w.lower().strip(".!?'")
                    if (wl and wl not in core.lower() and wl not in SMALL and not BANNED.search(w) and not PROFANE.search(w)
                            and wl not in REPEAT_FILLER and len(wl) > 1 and not CODE_RX.fullmatch(w) and wl not in {"copy", "x"}
                            and not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)+", wl) and not re.fullmatch(r"\d+(mm|cm|ml|oz|\")?", wl)):
                        cand_words.append(tidy_case(w.strip(".!?")))
                regions = [w for w in cand_words if w.upper() in {"EU", "AU", "US", "PAL", "JP", "NTSC", "UK"}]
                cand_words = [w.upper() for w in regions] + [w for w in cand_words if w not in regions]
            m = re.search(r"\b(\d{1,3})\b(?!\s*(st|nd|rd|th|mm|cm|ml|oz|x)\b)", r["old_title"])
            if m and m.group(1) not in core:
                cand_words.insert(0, ("Design " + m.group(1)) if r["fam"] == "signed" else m.group(1))
            new = None
            for w in cand_words[:8]:
                c = insert_word(core, w)
                if c and c.lower() not in taken:
                    new = c
                    break
            n = i
            while not new:
                c = insert_word(core, f"Design {n}")
                if c and c.lower() not in taken:
                    new = c
                n += 1
                if n > 999:
                    break
            r["t"] = new
            taken.add(new.lower())
    for r in rows:
        o = r.pop("_o")
        mm = r.pop("_mm")
        if r["wrote_d"]:
            r["d"] = mm or meta_for(o, r["fam"], r["info"], r["t"])
    for r in rows:
        if r["wrote_t"]:
            stats["titles written"] += 1
        if r["wrote_d"]:
            stats["metas written"] += 1
        if not title_ok(r["t"]) or not meta_ok(r["d"] or ""):
            fails.append(r)
    json.dump(rows, open(os.path.join(HERE, "rows.json"), "w"))
    print(stats, "fails", len(fails))
    fc = collections.Counter(r["fam"] for r in fails)
    print(fc)
    for r in fails[:60]:
        print(r["fam"], "|", r["old_title"][:90], "|", r["t"], problems(r["t"]), "|", r["d"], problems(r["d"] or ""))


def insert_word(core, w):
    """Add a distinguishing word; keep the product noun at the end and the whole title <= 60."""
    w = tidy_case(w) if not w.startswith("Design ") else w
    cand = f"{core} {w}"
    if len(cand) + len(SUFFIX) <= 60:
        return cand + SUFFIX
    if len(cand) <= 60:
        return cand
    c2 = re.sub(r"\s+", " ", re.sub(LOW_VALUE, "", core, flags=re.I)).strip(" –-")
    if len(c2.split()) >= 2 and len(c2) + len(w) + 1 <= 60:
        return f"{c2} {w}"
    m = None
    for m in re.finditer(r"\b" + PRODUCT_NOUNS + r"\b|Printed Signature (Print|Poster)|Replacement Case|Fridge Magnet|Face Masks?|Baby Grow", c2, re.I):
        pass
    if m and m.end() >= len(c2) - 1:
        tail = c2[m.start():]
        head = words_trim(c2[: m.start()].strip(" –-"), 60 - len(tail) - len(w) - 2)
        if head:
            return f"{head} {tail} {w}"
    room = 60 - len(w) - 1
    c = words_trim(c2, room)
    return f"{c} {w}" if c else None


if __name__ == "__main__":
    main()
