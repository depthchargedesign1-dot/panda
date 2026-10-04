"""Retro gaming posters: new copy, SEO and £4.99 A4 price, as Shopify import CSVs.

Usage: python3 build.py export.jsonl OUT_DIR
Reads the bulk export of collection all-retro-game-posters. Only single-variant "Default Title"
retro gaming posters at 2.99 are rewritten; everything else goes to odd_ones.csv.
"""
import collections
import csv
import hashlib
import html
import json
import os
import re
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

P, V = {}, collections.defaultdict(list)
for line in open(SRC):
    o = json.loads(line)
    (V[o["__parentId"]].append(o) if "__parentId" in o else P.__setitem__(o["id"], o))

# ---------- consoles ----------
# key: (regex on title, regex on productType, short, long, maker for disclaimer, maker short for prose)
CONSOLES = [
    ("megacd", r"mega\s*cd", r"mega\s*cd", "Mega CD", "Sega Mega CD", "Sega"),
    ("32x", r"\b32x\b", r"32x", "Sega 32X", "Sega 32X", "Sega"),
    ("saturn", r"saturn", r"saturn", "Sega Saturn", "Sega Saturn", "Sega"),
    ("dreamcast", r"dreamcast", r"dreamcast", "Dreamcast", "Sega Dreamcast", "Sega"),
    ("gamegear", r"game\s*gear", r"game\s*gear", "Game Gear", "Sega Game Gear", "Sega"),
    ("megadrive", r"mega\s*drive|genesis", r"megadrive", "Mega Drive", "Sega Mega Drive", "Sega"),
    ("mastersystem", r"master\s*system", r"master system", "Master System", "Sega Master System", "Sega"),
    ("snes", r"super\s*nintendo|\bsnes\b", r"\bsnes\b", "SNES", "Super Nintendo (SNES)", "Nintendo"),
    ("n64", r"\bn64\b|nintendo\s*64", r"n64", "N64", "Nintendo 64", "Nintendo"),
    ("gamecube", r"game\s*cube", r"game\s*cube", "GameCube", "Nintendo GameCube", "Nintendo"),
    ("gameboy", r"game\s*boy", r"game\s*boy", "Game Boy", "Nintendo Game Boy", "Nintendo"),
    ("nes", r"\bnes\b", r"\bnes\b", "NES", "Nintendo Entertainment System (NES)", "Nintendo"),
    ("ps4", r"\bps4\b|playstation\s*4", r"playstation 4|ps4", "PS4", "PlayStation 4", "Sony"),
    ("ps2", r"\bps2\b|playstation\s*2", r"playstation 2|ps2", "PS2", "PlayStation 2", "Sony"),
    ("ps1", r"\bps1\b|\bpsx\b|playstation", r"playstation", "PlayStation", "original PlayStation", "Sony"),
    ("jaguarcd", r"jaguar\s*cd", r"jaguar cd", "Atari Jaguar CD", "Atari Jaguar CD", "Atari"),
    ("jaguar", r"jaguar", r"jaguar", "Atari Jaguar", "Atari Jaguar", "Atari"),
    ("lynx", r"lynx", r"lynx", "Atari Lynx", "Atari Lynx", "Atari"),
    ("a7800", r"7800", r"7800", "Atari 7800", "Atari 7800", "Atari"),
    ("a5200", r"5200", r"5200", "Atari 5200", "Atari 5200", "Atari"),
    ("a2600", r"2600", r"2600", "Atari 2600", "Atari 2600", "Atari"),
    ("intellivision", r"intellivis", r"intellivis", "Intellivision", "Intellivision", None),
    ("neogeo", r"neo\s*geo", r"neo\s*geo", "Neo Geo", "Neo Geo", "SNK"),
    ("cd32", r"cd\s*32", r"cd32", "Amiga CD32", "Amiga CD32", None),
    ("odyssey", r"odys", r"odd?ess?y", "Odyssey", "Magnavox Odyssey", None),
    ("coleco", r"coleco", r"coleco", "ColecoVision", "ColecoVision", None),
]
DISCLAIMER_MAKER = {"Nintendo": "Nintendo", "Sega": "Sega", "Sony": "Sony", "Atari": "Atari", "SNK": "SNK"}


def detect_console(title, ptype):
    hits = []
    for i, (key, tre, pre, short, long_, maker) in enumerate(CONSOLES):
        m = re.search(tre, title, re.I)
        if m:
            hits.append((m.start(), i, (key, short, long_, maker)))
    if hits:
        return min(hits)[2]
    for key, tre, pre, short, long_, maker in CONSOLES:
        if re.search(pre, ptype, re.I):
            return key, short, long_, maker
    return None


# ---------- game name ----------
CUT = re.compile(
    r"\s+-\s+|\s*\bGAME\s+INSPIRED\b|\s*\bGame\s+Style\s+Inspired\b|\s*\bGame\s+Inspired\b|\s*\bInspired\b|"
    r"\s*\bRetro\s+Gam(?:e|ing)\b|\s*\bGaming\s+Poster\b|\s*\bA4\s+A3\b|\s*\bA2\s+A3\b|\s*\bPoster\s+Art\b|\s*\bRetro\s+Poster\b", re.I)
CONSOLE_WORDS = (r"Super\s+Nintendo|Nintendo\s+NES|Nintendo|S?NES|Sega\s+Mega\s*drive|Sega\s+Master\s+System|Master\s*System|Mega\s*drive|"
                 r"Sega\s+Saturn|Saturn|Sega\s+Dreamcast|Dreamcast|Sega|Mega\s*CD|PS[1-4]|Playstation\s*\d?|Game\s*cube|Game\s*boy|"
                 r"Atari\s*\d{4}|Atari|Jaguar\s*CD|Jaguar|Lynx|Neo\s*Geo|Intellivis(?:i)?on|Amiga\s*CD\s*32|CD32|32X|Odd?ess?y|Coleco")
TRAIL = re.compile(r"(?:[\s_]+(?:" + CONSOLE_WORDS + r"))+\s*$", re.I)
LEAD = re.compile(r"^(?:(?:Intellivis(?:i)?on|Sega\s+Saturn|SNES)\s+)+", re.I)
REGION = re.compile(r"(?:[\s_]+(?:pal|eu|euro|gb|none|ca|au|aus|us|usa|jp|jap|jpn|de|fr|ger|germ|ntsc|uk|pc|e|u|j|0))+\s*$", re.I)
ACRONYMS = {"wwf", "wwe", "wcw", "nba", "nfl", "nhl", "fifa", "pga", "usa", "uk", "ufc", "tmnt", "gp", "f1", "f-1", "rbi", "nhra",
            "ii", "iii", "iv", "vi", "vii", "viii", "ix", "xi", "3d", "2d", "dx", "ex", "gt", "rc", "wc", "mlb", "tv", "ufo", "et", "x-men",
            "ncaa", "ea", "snk", "ok", "kof", "pba", "lsd", "dbz", "3ds", "hd", "bmx", "atv", "cd", "sos", "vmu", "rpg", "stg", "nba", "ii"}
SMALL = {"of", "the", "and", "in", "on", "a", "an", "to", "for", "at", "vs", "or", "with", "from", "by"}
fallback_log = []


def fix_word(w, first):
    lw = w.lower()
    if lw in ACRONYMS:
        return lw.upper() if lw not in {"x-men"} else "X-Men"
    if "." not in w and re.fullmatch(r"[A-Z0-9'&:!]+", w) and len(w) >= 2 and re.search(r"[A-Z]", w):
        # all-caps word -> title case (keep short ones with digits)
        if re.search(r"\d", w):
            return w
        w = w.capitalize()
        lw = w.lower()
    if not first and lw in SMALL:
        return lw
    if w[:1].islower() and not first and lw not in SMALL:
        return w[:1].upper() + w[1:]
    if first:
        return w[:1].upper() + w[1:]
    return w


def parse_game(title):
    t = title.replace("_", " ").replace("’", "'")
    m = CUT.search(t)
    name = t[: m.start()] if m else t
    name = re.sub(r"\s+", " ", name).strip(" -–|,")
    name = re.sub(r"\(\d+\)", "", name).strip()
    for _ in range(3):
        name = TRAIL.sub("", name).strip(" -–|,")
        name = REGION.sub("", name).strip(" -–|,")
    name = LEAD.sub("", name).strip(" -–|,")
    name = re.sub(r"\bpal\b|\(\d+\)", "", name, flags=re.I)
    name = re.sub(r"(\d)-in-(\d)", r"\1 in \2", name, flags=re.I)
    name = re.sub(r"(?<=[a-z])cd$", " CD", name)
    name = re.sub(r",\s*the$", "", name, flags=re.I)
    name = re.sub(r"'S\b", "'s", name)
    name = re.sub(r"\bXmen\b", "X-Men", name, flags=re.I)
    name = re.sub(r"\bL And\b", "Land", name)
    name = re.sub(r"(?<=[a-z])(\d)", r" \1", name)            # Sonic3 -> Sonic 3
    name = re.sub(r"\s+-\s*|\s*-\s+", " ", name)               # stray hyphens
    name = re.sub(r"\s+", " ", name).strip(" -–|,")
    words = name.split(" ")
    name = " ".join(fix_word(w, i == 0) for i, w in enumerate(words) if w)
    name = re.sub(r"\bIi\b", "II", name)
    bad = (not name or len(name) < 2 or (len(name) <= 2 and not re.search(r"\d", name)) or re.search(r"request|any game|poster", name, re.I)
           or not re.search(r"[A-Za-z]", name))
    return (None if bad else name)


# ---------- copy ----------
def h(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)


def pick(seq, key, salt):
    return seq[h(key + salt) % len(seq)]


def esc(s):
    return html.escape(s, quote=False)


OPENERS = [
    "This {g} retro gaming poster is for anyone who lost whole weekends to the {cs} as a kid, and it looks great in a game room.",
    "Bring back the glory days with this {g} retro gaming poster, a fun pick for collectors and retro gamers.",
    "Our {g} retro gaming poster is a cheerful bit of nostalgia for retro gamers, collectors and games rooms.",
    "This {g} retro gaming poster makes a great birthday or Christmas gift for a retro gamer.",
    "If the {cs} was the heart of your childhood, this {g} retro gaming poster belongs on your wall.",
]
DESIGN = [
    "Every {g} retro gaming poster is our own fan-made design inspired by the classic {cl} game. We print it in our North Yorkshire workshop and post it flat in a board-backed envelope.",
    "Each {g} retro gaming poster is a fan-made design inspired by the classic {cl} game, printed in our North Yorkshire workshop and posted flat in a board-backed envelope.",
]
BULLETS = [
    "Bold artwork that stands out on a gaming wall",
    "Printed to order, so yours is fresh off the printer",
    "Sized for a desk frame or a feature wall",
    "Sent flat with board backing, so it arrives crease-free",
    "A thoughtful gift for anyone who grew up with {acs}",
    "Mix and match with our other retro posters",
    "Fits standard A-size frames from any high street shop",
    "Ideal for a man cave, bedroom or student flat",
    "A nostalgic talking point for collectors and retro fans",
]
CLOSERS = [
    "Pair it with another {cs} classic and start your own retro gallery.",
    "A great little gift for the gamer in your life, whatever their age.",
    "Add a few more from our retro range and fill the wall.",
    "Perfect for a games room makeover or a birthday surprise.",
    "Frame it, pin it up and press start on some happy memories.",
]
META = [
    "Fan-made {g} retro gaming poster, printed to order in our North Yorkshire workshop and posted flat in a hard-backed envelope. A great gift for any gamer.",
    "Relive the classic {g} with this fan-made retro gaming poster. Printed to order in A4 or larger sizes and sent flat in a hard-backed envelope.",
    "A {g} retro gaming poster for game rooms, man caves and collectors. Printed to order in North Yorkshire and posted flat so it arrives crease-free.",
    "Add {g} to your gaming wall with this fan-made retro poster. Printed to order in North Yorkshire and posted flat in a hard-backed envelope.",
    "Brighten up a game room with this fan-made {g} retro gaming poster. Printed to order, sent flat in a hard-backed envelope. A fun gift for any gamer.",
    "Fan-made {g} poster for retro gamers and collectors. Printed to order in our North Yorkshire workshop and posted flat in a hard-backed envelope.",
]
META_SHORT = [  # for long game names
    "Fan-made {g} retro gaming poster, printed to order and posted flat.",
    "Fan-made {g} retro gaming poster for game rooms and collectors.",
    "{g} retro gaming poster, printed to order and posted flat.",
    "{g} fan-made poster, printed to order.",
]
META_PAD = [" A great gift for any gamer.", " Ideal for game rooms.", " Posted flat in a hard-backed envelope.", " Printed in North Yorkshire."]
ISO = {"A4": "A4 (210 x 297 mm)", "A3": "A3 (297 x 420 mm)", "A2": "A2 (420 x 594 mm)", "A1": "A1 (594 x 841 mm)", "A0": "A0 (841 x 1189 mm)"}


def sizes_for(title):
    found = re.findall(r"\bA([0-4])\b", title)
    s = sorted({"A" + d for d in found}, key=lambda x: -int(x[1]))  # A4 first
    if not s:
        s = ["A4", "A3", "A2", "A1"]
    if "A4" not in s:
        s = ["A4"] + s
    return s


def join_or(items):
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " or " + items[-1]


def disclaimer(maker, cs):
    if maker in DISCLAIMER_MAKER:
        who = f"{DISCLAIMER_MAKER[maker]} or the game's publisher"
    elif cs:
        who = f"the game's publisher or the makers of the {cs}"
    else:
        who = "the game's publisher"
    return ("This is an unofficial, fan-made print produced by Foxy Printing. It is not made, endorsed or licensed by "
            f"{who}. All trademarks and game titles belong to their respective owners and are used only to identify the theme.")


def seo_title(g):
    for fmt in ("{g} Retro Gaming Poster | Foxy Printing", "{g} Retro Poster | Foxy Printing", "{g} Poster | Foxy Printing"):
        s = fmt.format(g=g)
        if len(s) <= 60:
            return s
    words = g.split()
    while words and len(" ".join(words) + " Poster | Foxy Printing") > 60:
        words.pop()
    return " ".join(words).rstrip(":,&-") + " Poster | Foxy Printing"


def meta_desc(g, key):
    order = sorted(range(len(META)), key=lambda i: h(key + str(i)))
    for i in order:
        s = META[i].format(g=g)
        if 140 <= len(s) <= 155:
            return s
    # build from a shorter stem and pad with sentences until in range
    for stem in META + META_SHORT:
        base = stem.format(g=g)
        if len(base) > 155:
            continue
        for pads in _pad_combos():
            s = base + "".join(pads)
            if 140 <= len(s) <= 155:
                return s
    return None


def _pad_combos():
    import itertools
    for r in range(0, 4):
        for c in itertools.permutations(META_PAD, r):
            yield c


def body(g, gk, cs, cl, maker, sizes, key):
    art = "an" if re.match(r"[AEIOU]|NES|SNES|N64", cs) else "a"
    rep = dict(g=esc(g), cs=esc(cs), cl=esc(cl), acs=f"{art} {esc(cs)}")
    opener = pick(OPENERS, key, "o").format(**rep)
    design = pick(DESIGN, key, "d").format(**rep)
    n = 4
    order = sorted(range(len(BULLETS)), key=lambda i: h(key + "b" + str(i)))[:n]
    if len(g.split()) > 5:  # long names: use the shortest bullets to stay under 220 words
        order = sorted(range(len(BULLETS)), key=lambda i: len(BULLETS[i]))[:4]
    bullets = "".join(f"<li>{BULLETS[i].format(**rep)}</li>" for i in sorted(order))
    closer = pick(CLOSERS, key, "c").format(**rep)
    size_txt = join_or(sizes) + " (A4 is 210 x 297 mm)"
    return (
        f"<p>{opener}</p>"
        f"<h2>{esc(g) if g == cs else esc(g) + ' ' + esc(cs)} Retro Gaming Poster</h2>"
        f"<p>{design}</p>"
        f"<h3>Why you'll love it</h3><ul>{bullets}</ul>"
        f"<h3>Size &amp; details</h3><ul><li>Sizes: {size_txt}</li>"
        f"<li>Print only, no frame</li></ul>"
        f"<h3>Delivery</h3><p>Printed to order and posted in a hard-backed envelope to keep it flat. Postage options and costs are shown at checkout.</p>"
        f"<p>{closer}</p>"
        f"<h3>Please note</h3><p class=\"disclaimer\">{disclaimer(maker, cs)}</p>"
    )


def words(htm):
    return len(re.sub(r"<[^>]+>", " ", htm.replace("&amp;", "&")).split())


# ---------- run ----------
rows, odd, fallbacks = [], [], []
single_299 = 0
for pid, p in P.items():
    vs = V[pid]
    v0 = vs[0] if vs else None
    is_single = len(vs) == 1 and v0["title"] == "Default Title"
    reason = None
    ptl = (p["productType"] + " " + p["title"]).lower()
    gaming = not re.search(r"signed|autograph", ptl) and (detect_console("", p["productType"]) or re.search(r"retro gam|game (?:style )?inspired", p["title"], re.I))
    if is_single and v0["price"] == "2.99":
        single_299 += 1
    if not gaming:
        reason = "not a retro gaming poster (" + p["productType"] + ")"
    elif not is_single:
        reason = f"{len(vs)} variant(s), not a single Default Title (prices {', '.join(sorted(set(v['price'] for v in vs)))})"
    elif v0["price"] != "2.99":
        reason = f"single variant at {v0['price']}"
    elif re.search(r"request", p["title"], re.I):
        reason = "request-a-poster product, needs its own copy"
    if reason:
        odd.append(dict(handle=p["handle"], title=p["title"], productType=p["productType"], status=p["status"],
                        variants=len(vs), prices=" ".join(sorted(set(v["price"] for v in vs))), reason=reason))
        continue
    con = detect_console(p["title"], p["productType"])
    cs, cl, maker = (con[1], con[2], con[3]) if con else ("retro console", "retro console", None)
    if not con:
        fallbacks.append((p["handle"], p["title"], "console"))
    g = parse_game(p["title"])
    key = p["handle"]
    sizes = sizes_for(p["title"])
    if g is None:
        fallbacks.append((p["handle"], p["title"], "game name"))
        gtxt = cs if con else "Classic Game"
        b = body(gtxt, gtxt, cs, cl, maker, sizes, key)
        st = seo_title(gtxt)
        md = meta_desc(gtxt, key)
    else:
        b = body(g, g, cs, cl, maker, sizes, key)
        st = seo_title(g)
        md = meta_desc(g, key)
    if md is None:
        fallbacks.append((p["handle"], p["title"], "meta length"))
        md = (f"Fan-made {g or 'classic'} retro gaming poster, printed to order and posted flat."[:150]).rsplit(" ", 1)[0] + "."
    tags = list(p["tags"])
    if "third-party-name" not in tags:
        tags.append("third-party-name")
    rows.append({
        "Handle": p["handle"], "Title": p["title"], "Body (HTML)": b, "Tags": ", ".join(tags),
        "SEO Title": st, "SEO Description": md, "Option1 Name": "Title", "Option1 Value": "Default Title",
        "Variant SKU": v0["sku"], "Variant Price": "4.99",
        "_game": g or "", "_console": cs, "_ptype": p["productType"], "_old_price": v0["price"], "_status": p["status"],
        "_has_options_tag": "Poster Options" in p["tags"], "_maker": maker or "",
    })

COLS = ["Handle", "Title", "Body (HTML)", "Tags", "SEO Title", "SEO Description", "Option1 Name", "Option1 Value", "Variant SKU", "Variant Price"]
rows.sort(key=lambda r: r["Handle"])


def write(path, rs):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rs)


# test file: 3 different consoles
seen, test = set(), []
for want in ("Mega Drive", "SNES", "PlayStation"):
    for r in rows:
        if r["_console"] == want and r["_game"] and r["Handle"] not in seen:
            test.append(r); seen.add(r["Handle"]); break
write(os.path.join(OUT, "00-TEST-3-products.csv"), test)
CHUNK = 5000
for i in range(0, len(rows), CHUNK):
    part = rows[i:i + CHUNK]
    write(os.path.join(OUT, f"{i // CHUNK + 1:02d}-retro-posters-{i + 1}-{i + len(part)}.csv"), part)

with open(os.path.join(OUT, "odd_ones.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["handle", "title", "productType", "status", "variants", "prices", "reason"])
    w.writeheader(); w.writerows(sorted(odd, key=lambda r: (r["reason"], r["handle"])))
with open(os.path.join(OUT, "parse_fallbacks.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["handle", "title", "what failed"]); w.writerows(fallbacks)
with open(os.path.join(OUT, "parsed_names.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["handle", "current title", "parsed game", "console", "status", "has Poster Options tag", "SEO title"])
    for r in rows:
        w.writerow([r["Handle"], r["Title"], r["_game"], r["_console"], r["_status"], r["_has_options_tag"], r["SEO Title"]])
json.dump(rows, open(os.path.join(OUT, "_rows.json"), "w"))
print("products", len(P), "single-variant at 2.99", single_299, "rows", len(rows), "odd", len(odd), "fallbacks", len(fallbacks))
print(collections.Counter(r["reason"].split(" (")[0] for r in odd))
print(collections.Counter(r["_console"] for r in rows))
