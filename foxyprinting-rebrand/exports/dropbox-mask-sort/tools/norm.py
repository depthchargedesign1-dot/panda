"""Name normalisation for the Dropbox mask sort (phase 1, read-only plan)."""
import re, os, unicodedata

NOISE = {"mh","jb","face","mask","masks","facemask","copy","final","new","jpg","jpeg","png","cutout","cut","out","celebrity",
         "cpdvd","mint","onbuy","ver","amazon","small","cropped","party","fancy","dress","dresss","footballer","golfer","player",
         "tmp","transparent","thumbnail","breakout","scotish","scottish","darts","rapper","bollywood"}
BASIC_NOISE = {"mh","jb","face","mask","facemask","copy"}
IMG = {".jpg",".jpeg",".png",".gif",".webp",".jpf"}

def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def parse(name):
    """Return dict(base_key, version, copy_marker, year, display, qualifier).
    base_key  : letters only, lower, person/subject part (before ' - ')
    version   : '' or digit string when the name ends in a version number ("Name 2", "Name2")
    copy_marker: '(2)' style Dropbox/Windows copy suffix, or ' - Copy'
    year      : 4-digit year tokens like 2018/2021 (not versions)
    """
    stem, ext = os.path.splitext(name)
    s = strip_accents(stem).replace("_", " ").strip()
    copy = ""
    m = re.search(r"\s*\((\d+)\)\s*$", s)
    while m:
        copy += f"({m.group(1)})"; s = s[:m.start()].strip(); m = re.search(r"\s*\((\d+)\)\s*$", s)
    if re.search(r"\s*-\s*copy\s*$", s, re.I):
        copy += "copy"; s = re.sub(r"\s*-\s*copy\s*$", "", s, flags=re.I)
    years = re.findall(r"(?<!\d)(?:19|20)\d\d(?!\d)", s)
    s = re.sub(r"(?<!\d)(?:19|20)\d\d(?!\d)", " ", s)
    # qualifier after ' - ' / ' -' (club, show, sport ...)
    parts = re.split(r"\s+-\s*|\s*-\s+", s, maxsplit=1)
    subject = parts[0]; qual = parts[1].strip() if len(parts) > 1 else ""
    subject = re.sub(r"\+", " ", subject)
    toks = re.findall(r"[A-Za-z]+|\d+", subject)
    toks = [t for t in toks if not (t.isdigit() and len(t) >= 3)]
    # drop noise tokens at the end/anywhere
    toks = [t for t in toks if t.lower() not in NOISE]
    version = ""
    if toks and toks[-1].isdigit() and len(toks[-1]) <= 2:
        version = str(int(toks[-1])); toks = toks[:-1]
    elif toks and re.fullmatch(r"[A-Za-z]+\d{1,2}", toks[-1]):
        m2 = re.fullmatch(r"([A-Za-z]+)(\d{1,2})", toks[-1]); toks[-1] = m2.group(1); version = str(int(m2.group(2)))
    pass  # keep other digits (e.g. "50 Cent")
    # trailing noise again
    while toks and toks[-1].lower() in NOISE: toks.pop()
    if version in ("1",): version = ""  # "Name 1" treated as the main image
    display = " ".join(toks)
    key = "".join(toks).lower()
    qkey = re.sub(r"[^a-z]", "", qual.lower())
    return dict(base_key=key, version=version, copy_marker=copy, year=",".join(years), display=display, qualifier=qual, qual_key=qkey, ext=ext.lower())

def master_key_candidates(name):
    """Keys tried against the 2 Oct master list (whose keys sometimes keep the qualifier)."""
    p = parse(name)
    c = [p["base_key"], p["base_key"] + p["qual_key"]]
    stem = os.path.splitext(strip_accents(name))[0]
    full = re.sub(r"\(\d+\)|(?:19|20)\d\d", "", stem)
    full = "".join(t for t in re.findall(r"[A-Za-z]+", full) if t.lower() not in BASIC_NOISE).lower()
    c.append(full)
    return [x for x in dict.fromkeys(c) if x]
