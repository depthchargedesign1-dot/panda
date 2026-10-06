"""Phase 3: build rename-plan.csv for image files inside the 2026 category folders (read-only; no Dropbox calls).

Owner's brief (5/6 Oct 2026): "remove the - and the _ and also any extra unwanted text, should just be the name and
maybe the show but any junk filename data needs removing".
  Target "Person Name.jpg"; "Person Name (Show).jpg" only where the show is needed to identify them (single-word
  character names such as "Becky (Coronation Street)"); no dashes or underscores; proper case; spelling fixes from
  tools/rename_overrides.py. Junk removed: years, copy, celebrity, mask, facemask, face, breakout, new, final, agency /
  camera codes, SKU codes, Dropbox "(2)" copy markers. KEPT: version numbers (Name 2), MH / JB markers (at the end),
  "(larger)". Lowercase extension.
Never overwrite: when the clean name is taken (by a file in the folder or another planned rename) a file of a different
size gets the next free version number; a same-size clash is left unrenamed and logged (rename-conflicts.csv).
Scope: files under top folders starting "2026 " except "2026 ! DUPLICATES TO CHECK". Not touched: TO SORT, loose root
files, MASKS NOT YET CUT, MASK PACK MOCKUP IMAGES, the JB folders, non-images, "._" files, pack/mockup images and files
whose name carries no usable person name (numeric SKU files, hashes, stock-photo ids).
Inputs: phase3/list/all-p*.json (recursive listing). Outputs: rename-plan.csv, rename-skipped.csv, rename-conflicts.csv,
phase3/rename-entries.json."""
import csv, glob, json, os, re, sys, unicodedata, collections
sys.path.insert(0, os.path.dirname(__file__))
from rename_overrides import OVERRIDES, WORD_FIX, PHRASE_FIX, JUNK_NAMES
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".jpf"}

# show / qualifier phrases that may sit inside a name without a dash. key regex -> display ("" = always drop)
SHOWS = [
    (r"coronation street", "Coronation Street"), (r"corrie", "Coronation Street"), (r"east ?enders".replace(" ?", ""), "EastEnders"), (r"east enders", "EastEnders"),
    (r"emmerdale", "Emmerdale"), (r"hollyoaks", "Hollyoaks"), (r"real house wives", "Real Housewives"), (r"real housewives", "Real Housewives"),
    (r"gangs of london", "Gangs of London"), (r"love island", "Love Island"), (r"towie", "TOWIE"),
    (r"strictly come dancing", "Strictly Come Dancing"), (r"stri(?:c|ck|k)t?lys?", "Strictly"),
    (r"x factor judges pack from", ""), (r"x factor", "X Factor"), (r"xfactor", "X Factor"), (r"the chase", "The Chase"),
    (r"car chasers", "Car Chasers"), (r"i'?m a celeb(?:rity)?(?: get me (?:o?ut) of here)?", "I'm a Celebrity"),
    (r"get me ut of here", ""), (r"stranger things", "Stranger Things"), (r"the office", "The Office"),
    (r"mrs brown", "Mrs Brown's Boys"), (r"benidorm", "Benidorm"), (r"geordie shore", "Geordie Shore"),
    (r"gavin and stacey", "Gavin and Stacey"), (r"still games?", "Still Game"), (r"one piece", "One Piece"),
    (r"friends", "Friends"), (r"harry potter", "Harry Potter"), (r"mamma mia", "Mamma Mia"),
    (r"loose women", "Loose Women"), (r"the voice", "The Voice"), (r"walking dead", "The Walking Dead"),
    (r"brooklyn 99", "Brooklyn Nine-Nine"), (r"blink 182", ""), (r"avengers", ""), (r"grease", "Grease"),
    (r"money heist", "Money Heist"), (r"squid game", "Squid Game"), (r"bake off", "Bake Off"),
    (r"ab fab", "Ab Fab"), (r"saw puppet", ""), (r"bad boys", "Bad Boys"),
    (r"england euros?", ""), (r"euros?", ""), (r"bbc", ""), (r"golf", ""), (r"rugby", ""), (r"ufc", ""),
    (r"darts", ""), (r"dancer", ""), (r"bollywood", ""), (r"music star", ""), (r"politician", ""),
    (r"footballer", ""), (r"golfer", ""), (r"lionesses", ""), (r"england", ""), (r"brazil", ""),
    (r"belgium", ""), (r"tennis", ""), (r"boxer", ""), (r"snooker", ""), (r"cricket(?:er)?", ""),
    (r"f1", ""), (r"formula 1", ""), (r"wwe", ""), (r"rapper", ""), (r"singer", ""), (r"actor", ""), (r"actress", ""), (r"comedian", ""), (r"football", ""), (r"argentina", ""),
    (r"wales", ""), (r"scotland", ""), (r"ireland", ""), (r"france", ""), (r"spain", ""), (r"germany", ""), (r"italy", ""),
    (r"portugal", ""), (r"chile", ""), (r"costa rica", ""), (r"lioness", ""), (r"chef", ""), (r"presenter", ""),
]
SHOWS += [(k, v) for k, v in [
    (r"back ?street boys", "Backstreet Boys"), (r"little britain", "Little Britain"), (r"umbrella academy", "The Umbrella Academy"),
    (r"sex and (?:the )?city", "Sex and the City"), (r"home (?:and|n) away", "Home and Away"), (r"made in chelsea", "Made in Chelsea"),
    (r"better call saul", "Better Call Saul"), (r"breaking bad", "Breaking Bad"), (r"grey'?s anatomy", "Grey's Anatomy"),
    (r"big little lies", "Big Little Lies"), (r"dragons den", "Dragons' Den"), (r"ted lasso", "Ted Lasso"),
    (r"torvill and dean", ""), (r"the last kingdom", "The Last Kingdom"), (r"last kingdom", "The Last Kingdom"),
    (r"keeping up appearences", "Keeping Up Appearances"), (r"peaky blinders", "Peaky Blinders"),
    (r"game of thrones", "Game of Thrones"), (r"mean girls", "Mean Girls"), (r"the defenders", "The Defenders"),
    (r"the farm", "Clarkson's Farm"), (r"mrs brown'?s boys", "Mrs Brown's Boys"), (r"doctor who", "Doctor Who"),
    (r"dr who", "Doctor Who"), (r"the wanted", "The Wanted"), (r"take that", "Take That"), (r"s club", "S Club 7"),
    (r"mcbusted", "McBusted"), (r"bts", "BTS"), (r"blackpink", "Blackpink"), (r"ateez", "Ateez"),
    (r"(?:the )?big bang theory", "The Big Bang Theory"), (r"carry on", "Carry On"), (r"legend from gladiators", ""),
    (r"gladiators", "Gladiators"), (r"gadget show", ""), (r"diy sos", "DIY SOS"), (r"dirty dancing", "Dirty Dancing"),
    (r"fast furious", "Fast & Furious"), (r"pirates of the(?: caribbean)?", "Pirates of the Caribbean"), (r"die hard", "Die Hard"),
    (r"pulp fiction", "Pulp Fiction"), (r"titanic", ""), (r"guardians of the galaxy.*", ""), (r"star wars", "Star Wars"),
    (r"fawlty towers", "Fawlty Towers"), (r"allo allo", "'Allo 'Allo!"), (r"(?:the )?hangover", "The Hangover"),
    (r"american pie", "American Pie"), (r"wet wet wet", ""), (r"status quo", ""), (r"red hot chili peppers", ""),
    (r"shameless", "Shameless"), (r"supernatural", "Supernatural"), (r"top gun maverick", ""), (r"the godfather", ""),
    (r"home alone", "Home Alone"), (r"dumb n dumber", ""), (r"inbetweeners?", "The Inbetweeners"), (r"scrubs", "Scrubs"),
    (r"sherlock", "Sherlock"), (r"mindhunter", ""), (r"suits", ""), (r"ofah", "Only Fools and Horses"),
    (r"golden girls", "The Golden Girls"), (r"queer eye", "Queer Eye"), (r"spice girls?", ""), (r"girls aloud", ""),
    (r"1 direction|one direction", ""), (r"westlife", ""), (r"coronation royals", ""), (r"tiger king", ""),
    (r"fnaf", "FNAF"), (r"teletubbies", "Teletubbies"), (r"sesame street", "Sesame Street"), (r"brotherhood of man", ""),
    (r"wallace and grommit", "Wallace and Gromit"), (r"flintstones", "The Flintstones"), (r"turtles", "Ninja Turtles"),
    (r"newcastle", ""), (r"barcelona", ""), (r"arsenal", ""), (r"liverpool", ""), (r"man utd(?: manager)?", ""),
    (r"manchester city", ""), (r"coventry", ""), (r"halifax panthers", ""), (r"chelsea", ""), (r"leeds goalkeeper", ""),
    (r"world cup", ""), (r"tv movie star", ""), (r"tv stars?", ""), (r"movies? stars?", ""), (r"(?:british|russian|candian|canadian) star", ""),
    (r"sensation", ""), (r"signing", ""), (r"champion", ""), (r"manager", ""), (r"director", ""), (r"fighter", ""),
    (r"swimmer", ""), (r"music", ""), (r"movies?", ""), (r"promo", ""), (r"pr photos", ""), (r"photos", ""),
    (r"download", ""), (r"web", ""), (r"portable", ""), (r"fixed", ""), (r"to add", ""), (r"mp", ""),
    (r"fc", ""), (r"logo", ""), (r"profile", ""), (r"scotish", ""), (r"wallabies", ""), (r"rwc", ""), (r"net worth", ""),
    (r"transparent bg", ""), (r"uhq", ""), (r"sq", ""), (r"amazoon", ""), (r"doctiored", ""), (r"formula", ""),
    (r"aston martin raci\w*", ""), (r"rubber", ""), (r"rolling stone cover", ""), (r"mr porter interview", ""),
    (r"selects his post 6 nations lions xv", ""), (r"at the austrian grand prix", ""), (r"tas suzuki", ""),
    (r"coronation", "Coronation Street"), (r"in the office", ""),
]]
SHOW_RE = [(re.compile(r"(?<![a-z0-9'])" + k.replace(" ", r"[\s_\-]+") + r"(?![a-z0-9])", re.I), v) for k, v in SHOWS]
JUNK = {"copy", "celebrity", "celebrities", "celeb", "mask", "masks", "facemask", "facemasks", "face", "breakout",
        "new", "final", "mint", "cpdvd", "onbuy", "ver", "amazon", "ebay", "large", "cut", "cutout", "cutouts", "jpg",
        "jpeg", "png", "tmp", "foxy", "alt", "res", "low", "wallpapers", "wallpaper", "sku", "image", "photo", "pic",
        "hd", "hq", "edit", "edited", "version", "crop", "cropped", "official", "portrait", "headshot", "nintchdbpict"}
KEEP_UPPER = {"LL", "JR", "DJ", "AJ", "TJ", "CJ", "PJ", "JJ", "KJ", "RJ", "BJ", "OJ", "JD", "JK", "TV", "UK", "US",
              "II", "III", "IV", "KSI", "MC", "ABBA", "AC", "DC", "UB", "MH", "JB", "TOWIE", "BBC", "UFC", "WWE", "MJ",
              "JLS", "TLC", "NSYNC", "RnB", "KT", "LP", "ASAP", "ZZ", "YG", "NF", "DMX", "RZA", "GZA", "EJ", "MK"}
PARTICLES = {"van", "de", "der", "den", "da", "di", "du", "la", "le", "von", "y", "del", "dos", "das", "bin", "al",
             "el", "and", "of", "the", "a"}

FOLD = {"Ł": "L", "ł": "l", "Ø": "O", "ø": "o", "ß": "ss", "Æ": "Ae", "æ": "ae", "Đ": "D", "đ": "d", "Œ": "Oe", "œ": "oe"}
def fold(s):
    s = "".join(FOLD.get(c, c) for c in s)
    return unicodedata.normalize("NFC", "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)))
def nfc(s): return unicodedata.normalize("NFC", s)

def case_word(w, first):
    if not w: return w
    if w.upper() in KEEP_UPPER and (w.isupper() or len(w) <= 2) and w.lower() not in PARTICLES: return w.upper()
    if re.fullmatch(r"(?:[A-Za-z]\.)+[A-Za-z]?\.?", w): return w.upper()          # initials like J.K.
    if w.islower() and w in PARTICLES and not first: return w
    if re.fullmatch(r"(?:ii|iii|iv|vi|vii|viii|ix|xv|xi)", w, re.I) and not first: return w.upper()
    if w.isupper() or w.islower():
        w = w[0].upper() + w[1:].lower()
        w = re.sub(r"^Mc([a-z])", lambda m: "Mc" + m.group(1).upper(), w)
        w = re.sub(r"^(O|D)'([a-z])", lambda m: m.group(1) + "'" + m.group(2).upper(), w)
        return w
    w = re.sub(r"^Mc([a-z])", lambda m: "Mc" + m.group(1).upper(), w)
    if re.fullmatch(r"(?:ii|iii|iv|vi|vii|viii|ix|xv|xi)", w, re.I) and not first: return w.upper()
    if len(w) > 1 and w[0].islower() and w[1:].isupper(): return w[0].upper() + w[1:].lower()
    if w[0].islower(): return w[0].upper() + w[1:]                                  # jessica -> handled; iPhone-ish
    return w

def proper(tokens):
    out = []
    for i, t in enumerate(tokens):
        out.append(case_word(t, i == 0))
    # "O leary" -> "O'Leary"
    j = []
    i = 0
    while i < len(out):
        if out[i] in ("O", "o") and i + 1 < len(out) and i > 0:
            j.append("O'" + out[i + 1][0].upper() + out[i + 1][1:]); i += 2; continue
        j.append(out[i]); i += 1
    return [WORD_FIX.get(w.lower(), w) for w in j]

def clean(name, folder):
    """Return (new_name or None, reason, parts)."""
    stem, ext = os.path.splitext(name)
    if ext.lower() not in IMG: return None, "not an image", {}
    if name.startswith("."): return None, "hidden/resource-fork file", {}
    s = fold(nfc(stem))
    if re.search(r"\b(?:pack\d*|packs|mock-?ups?|header|banner|poster|cast|characters?|squad|crew)\b", s.replace("_", " "), re.I) and not OVERRIDES.get(name):
        return None, "pack/mockup/group image (not a single face)", {}
    larger = bool(re.search(r"\(larger\)", s, re.I)); s = re.sub(r"\s*\(larger\)", " ", s, flags=re.I)
    s = re.sub(r"\(\s*\d+\s*\)", " ", s)                                   # Dropbox/Windows copy markers
    s = re.sub(r"\bSKU-?[A-Z]*\d+\b", " ", s, flags=re.I)
    s = re.sub(r"\.[A-Za-z0-9]{20,}", " ", s)                              # base64 tails
    s = s.replace("[", " ").replace("]", " ")
    if s.count("(") > s.count(")"): s = s.replace("(", " ")
    marks = [m.upper() for m in re.findall(r"(?<![A-Za-z])(MH|JB)(?![A-Za-z])", s, re.I)]
    s = re.sub(r"(?<![A-Za-z])(MH|JB)(?![A-Za-z])", " ", s, flags=re.I)
    # bracketed non-numeric text, e.g. "Myra McQueen (Nicole Barber-Lane)" or "(Wales)": keep as qualifier
    paren = [p.strip() for p in re.findall(r"\(([^)]*[A-Za-z][^)]*)\)", s)]
    s = re.sub(r"\([^)]*\)", " ", s)
    # dash qualifier: "Becky - Coronation Street", "Kyle Walker -England"
    qual = ""
    m = re.search(r"\s+-+\s*|\s*-+\s+", s)
    if m:
        qual = s[m.end():]; s = s[:m.start()]
    show = ""
    def take_show(text):
        nonlocal show
        for rx, disp in SHOW_RE:
            if rx.search(text):
                t2 = rx.sub(" ", text)
                if not disp and len([w for w in re.findall(r"[A-Za-z]{2,}", t2) if w.lower() not in JUNK]) < 2 and text is not qual:
                    continue
                if disp and not show: show = disp
                text = t2
        return text
    before = s
    s = take_show(s)
    removed_show = s != before
    q = take_show(qual) if qual else ""
    s = re.sub(r"(?<=[a-z]{2})\.(?=[A-Za-z]{2})", " ", s)                       # Mariah.carey
    s = re.sub(r"\b(?!Mac)([A-Z][a-z]{2,})([A-Z][a-z]{2,})\b", r"\1 \2", s)      # JimmyFallon -> Jimmy Fallon
    s = re.sub(r"(?i)\b([a-z]{3,})(mask|face|jb|mh)\b", lambda m: m.group(1) + " " + m.group(2), s)
    toks = re.findall(r"[^\s_\-]+", s)
    # " Aka ...", " As ...", " In ..." describe a role: drop when a full name comes before
    for kw in ("aka", "as", "in"):
        low = [t.lower() for t in toks]
        if kw in low[2:]:
            i = low.index(kw, 2)
            if kw == "aka" or toks[i][0].isupper(): toks = toks[:i]
    def scrub(ts, keep_version=True):
        out = []
        for t in ts:
            t2 = t.strip(".,;:'\"!&+").strip()
            if not t2: continue
            if re.fullmatch(r"(?:19|20)\d\d", t2): continue                         # years
            if re.fullmatch(r"\d{3,}[A-Za-z]?", t2): continue                       # agency / camera numbers
            if re.fullmatch(r"[0-9a-f]{12,}", t2, re.I): continue                   # hashes
            if re.fullmatch(r"(?:e|R|tmp|IMG|DSC|P)\d+|[A-Za-z]{0,2}\d{4,}[A-Za-z0-9]*", t2): continue
            if t2.lower() in JUNK: continue
            if len(t2) >= 5 and re.search(r"\d", t2) and re.search(r"[A-Za-z]", t2) and not re.fullmatch(r"[A-Za-z]+\d{1,2}", t2): continue
            if re.search(r"[@]|\d\.\d", t2) or re.fullmatch(r"\d+x\d+", t2): continue
            if re.fullmatch(r"(?:19|20)\d\d'?s", t2): continue
            out.append(t2 if t2 != t else t2)
        return out
    toks = scrub(toks)
    # trailing caps character name after a removed soap name: "Alison King CARLA" -> "Alison King"
    if removed_show and len(toks) >= 3 and toks[-1].isupper() and len(toks[-1]) > 2 and not all(t.isupper() for t in toks):
        while len(toks) > 2 and toks[-1].isupper() and len(toks[-1]) > 2: toks.pop()
    # trailing "DE" agency code
    # trailing maker tags (owner via coordinator, 6 Oct): DE, SJ, MO (and BM) mark separate images like MH/JB: keep them
    tail = []
    while len(toks) > 1 and (toks[-1] in ("DE", "SJ", "SJ1", "MO", "BM", "bm") or (toks[-1] == "Mo" and len(toks) > 2)):
        tail.insert(0, toks.pop().upper())
    marks = marks + tail
    version = ""
    if toks and re.fullmatch(r"\d{1,2}", toks[-1]) and len(toks) > 1:
        version = str(int(toks[-1])); toks = toks[:-1]
    elif toks and re.fullmatch(r"[A-Za-z]{2,}\d{1,2}", toks[-1]):
        mm = re.fullmatch(r"([A-Za-z]+)(\d{1,2})", toks[-1]); toks[-1] = mm.group(1); version = str(int(mm.group(2)))
    # a version number left in the middle ("Emma Rigby 2 Face" handled above; "Joey Friends 2" -> show removed)
    mid = [i for i, t in enumerate(toks) if re.fullmatch(r"\d{1,2}", t) and i > 0]
    if mid and not version and mid[-1] == len(toks) - 1:
        pass
    if version == "0" or version == "1": version = ""
    if version.startswith("0"): version = str(int(version))
    letters = sum(len(re.sub(r"[^A-Za-zÀ-ɏ]", "", t)) for t in toks)
    if letters < 3: return None, "no usable name left (numeric/stock-photo/hash file name)", {}
    name_t = proper(toks)
    if all(t.lower() in JUNK_NAMES for t in name_t) or not any(len(t) > 1 for t in name_t):
        return None, "no usable name left (numeric/stock-photo/hash file name)", {}
    pf = PHRASE_FIX.get(" ".join(name_t).lower())
    if pf == "SKIPNAME": return None, "no usable name left (numeric/stock-photo/hash file name)", {}
    if pf: name_t = pf.split()
    qtoks = proper(scrub(re.findall(r"[^\s_\-]+", q))) if q else []
    qdisp = " ".join(qtoks)
    shown = ""
    if len(name_t) == 1:
        shown = show or qdisp
    full = " ".join(name_t)
    for p in paren:
        pt = proper(scrub(re.findall(r"[^\s_\-]+", p)))
        if pt: full += " (" + " ".join(pt) + ")"
    if shown and shown.lower() != full.lower(): full += " (" + shown + ")"
    if version: full += " " + version
    for mk in dict.fromkeys(marks): full += " " + mk
    if larger: full += " (larger)"
    full = re.sub(r"\s+", " ", full).strip()
    return full + ext.lower(), "", dict(show=show, qual=qdisp, version=version, marks=" ".join(marks), larger=larger)

def main():
    ents = []
    for f in sorted(glob.glob(f"{D}/phase3/list/all-p*.json")): ents += json.load(open(f))["entries"]
    moved = {m["source_path"]: m for m in json.load(open(f"{D}/phase2/mhjb-entries.json"))}   # done 07:53, after listing
    for e in ents:
        m = moved.get(e.get("file_id"))
        if m: e["path"] = "ns:1384231538//" + m["dest_display"].split("IMAGES/", 1)[1]
    files = [e for e in ents if e["object_type"] == "file"]
    def rel(e): return e["path"].split("//", 1)[1]
    def in_scope(r): return r.startswith("2026 ") and not r.lower().startswith("2026 ! duplicates to check") and "/" in r
    byfolder = collections.defaultdict(list)
    for e in files: byfolder[os.path.dirname(rel(e)).lower()].append(e)
    plan, skipped, conflicts, entries = [], [], [], []
    for folder in sorted(byfolder):
        fes = byfolder[folder]
        if not in_scope(fes[0]["path"].split("//", 1)[1]): continue
        occupied = {e["name"].lower() for e in fes}                    # never target a name any file holds now
        cand = []
        for e in sorted(fes, key=lambda x: x["name"].lower()):
            r = rel(e)
            ov = OVERRIDES.get(r) or OVERRIDES.get(e["name"])
            if ov == "SKIP":
                skipped.append(dict(path=r, reason="left as is (reviewed)")); continue
            if ov:
                new, why = ov + os.path.splitext(e["name"])[1].lower() if not os.path.splitext(ov)[1] else ov, ""
            else:
                new, why, _ = clean(e["name"], folder)
            if not new:
                skipped.append(dict(path=r, reason=why)); continue
            if new == e["name"]: continue                               # already clean
            cand.append((e, new))
        # same-size clash among candidates / existing -> leave; different size -> next free version
        taken = {}                                                       # lower name -> size of file that will hold it
        for e in fes: taken[e["name"].lower()] = e["file"]["size"]
        moving = {e["name"].lower() for e, _ in cand}
        for e, new in cand:
            size = e["file"]["size"]
            tgt = new
            if new.lower() == e["name"].lower():                       # case-only change
                pass
            elif new.lower() in taken:
                if taken[new.lower()] == size:
                    conflicts.append(dict(path=rel(e), size=size, wanted=new, clash_with=new, clash_size=taken[new.lower()],
                                          reason="same name and same size already in folder: left unrenamed"))
                    continue
                stem, ext = os.path.splitext(new)
                m = re.match(r"^(.*?)(?: (\d+))?((?: (?:MH|JB|DE|SJ|MO|BM))*)( \(larger\))?$", stem)
                base, v, mk, lg = m.group(1), int(m.group(2) or 1), m.group(3) or "", m.group(4) or ""
                same_size_hit = None
                while True:
                    v += 1
                    t = f"{base} {v}{mk}{lg}{ext}"
                    if t.lower() not in taken: break
                    if taken[t.lower()] == size: same_size_hit = t; break
                if same_size_hit:
                    conflicts.append(dict(path=rel(e), size=size, wanted=new, clash_with=same_size_hit, clash_size=size,
                                          reason="same size as an existing numbered version: left unrenamed"))
                    continue
                tgt = t
                conflicts.append(dict(path=rel(e), size=size, wanted=new, clash_with=new, clash_size=taken[new.lower()],
                                      reason=f"different size: renamed to next free version -> {tgt}"))
            taken[tgt.lower()] = size
            plan.append(dict(folder=os.path.dirname(rel(e)), old=e["name"], new=tgt, size=size, file_id=e["file_id"]))
            entries.append(dict(source_path=e["file_id"], destination_path=e["path"].rsplit("/", 1)[0] + "/" + tgt,
                                old=r_ if (r_ := rel(e)) else "", new=os.path.dirname(rel(e)) + "/" + tgt))
    W = lambda fn, rows, fl: csv.DictWriter(open(f"{D}/{fn}", "w", newline="", encoding="utf-8"), fieldnames=fl)
    w = W("rename-plan.csv", plan, ["folder", "old", "new", "size", "file_id"]); w.writeheader(); w.writerows(plan)
    w = W("rename-skipped.csv", skipped, ["path", "reason"]); w.writeheader(); w.writerows(skipped)
    w = W("rename-conflicts.csv", conflicts, ["path", "size", "wanted", "clash_with", "clash_size", "reason"]); w.writeheader(); w.writerows(conflicts)
    json.dump(entries, open(f"{D}/phase3/rename-entries.json", "w"), indent=0, ensure_ascii=False)
    print("plan", len(plan), "skipped", len(skipped), collections.Counter(s["reason"] for s in skipped), "conflicts", len(conflicts),
          collections.Counter(c["reason"].split(":")[0] for c in conflicts))

if __name__ == "__main__":
    main()
