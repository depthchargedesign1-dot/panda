#!/usr/bin/env python3
"""Generate new descriptions, SEO titles and meta descriptions for every
Personalised Cards (personalised-cards.co.uk) product.

Inputs (scratchpad): products.json, categories.json, research/*.json
Output: rewrite.json  {product_id: {description, page_title, meta_description}}

Usage:
  python3 pc_rewrite.py <scratch_dir> [--sample N] [--ids 123,456]
"""
from __future__ import annotations
import glob, hashlib, html, json, os, re, sys

# ---------------------------------------------------------------- facts --
STORE = "Personalised Cards"
EMAIL = "sales@personalised-cards.co.uk"
PHONE = os.environ.get("PC_PHONE", "")          # set once the owner confirms
POSTAGE = "£2.99"
SIZES_HTML = (
    "<li>A6: 148 x 105mm, a neat note-size card</li>"
    "<li>A5: 210 x 148.5mm, our most popular size</li>"
    "<li>A4: 297 x 210mm, a big statement card</li>"
)

# ------------------------------------------------- category -> family ---
KIDS_SHOWS = {"Number Blocks","Cloudbabies","Topsy and Tim","Octanaughts","Paw Patrol","Bob The Builder","Roary","Dinotrux","Go Jetters","Twirlywoos","Charlie and Lola","Chica Show","Clangers","Dinopaws","Doc Mcstuffins","Footy Pups","Patchwork Pals","Peter Rabbit","Ruff Ruff Tweet and Dave","The Adventures Of Abney and Teal","The Numtums","Chugginton","Pocoyo","Voltron","Bing","Fifi and The Flowertots","Iconicles","Olivia","Peppa Pig","Abadas","All Hail King Julien","Harry & Toto","Hey Duggee","In The Night Garden","Mr Blooms Nursery","Mr Peabody and Sherman","Noddy Toyland Detective","Rupert Bear","321 Penguins","Andys Wild Adventures","Caspers Scare School","Dawn Of The Croods","Dream Defenders","Fimbles","Get Squiggling","Guess with Jess","Home Adventures","Kerwhizz","Raa Raa The Noisy Lion","The Lingo Show","3rd & Bird","Alphablocks","Baby Jake","Boj","Clifford The Big Red Dog","Dragons","Everythings Rosie","Kate & Mim-Mim","Kazoops","Melody and Friends","Messy Goes To Okido","Mike The Knight","Nelly and Nora","Pajanimals","Show Me Show Me","Spot Bots","Teletubbies","Tinga Tinga Tales","Postman Pat","Kids Cartoon Cards"}
FAMILY = {
    "Music":"celeb","Football Players":"celeb","Female Movie Stars":"celeb","Male Movie Stars":"celeb",
    "Reality Stars":"celeb","Male TV Celebrities":"celeb","Female TV Celebrity Cards":"celeb",
    "Wrestling and Boxing Cards":"celeb","Cricket Players":"celeb","UFC":"celeb","Boxing":"celeb",
    "Golfers":"celeb","Basketball Players":"celeb","Darts Players":"celeb","Tennis":"celeb","Formula 1":"celeb",
    "Donald Trump":"celeb","TV and Movie Stars":"celeb","Tiger King & Carole Baskin":"show",
    "Football":"club","Bollywood":"bollywood","Game Of Thrones":"show","Video Games":"show",
    "Rude":"rude","Rude Birthday Card":"rude","Funny Rude Cards":"rude","Rude Valentines Day Cards":"rude_val",
    "Rude Anniversary":"rude_anniv","Rude Thank You":"rude_thanks","Rude Christmas":"rude_xmas",
    "Funny":"funny","Birthday":"birthday","Cards For Her":"her","Cards For Him":"him","Cards For Gingers":"funny",
    "Funny Animals":"animals","Engagement and Wedding Cards":"wedding",
    "Funny Couples Cards Anniversary or Birthday":"couples","Anniversary":"anniv","Valentines Day":"val",
    "Fathers Day":"dad","Mothers Day":"mum","Gay + LGBT":"lgbt","Thank You":"thanks","Teacher":"teacher",
    "1st Birthday Cards":"first","Baby":"baby","New/First Day of School":"school","Eid":"eid","Yoga":"yoga",
    "Get Well Soon":"getwell","Bon Voyage":"voyage","Congratulations":"congrats","Graduation":"grad",
    "Sympathy":"sympathy","Goodbye":"leaving","Sorry You're Leaving":"leaving","Leaving Cards":"leaving",
    "Sorry":"sorry","Good Luck":"luck","Friendship":"friend","Just to say":"justsay","Exams":"exams",
    "Dance & Cheerleading":"dance","Other Occasions":"other","Photo Upload Cards":"photo","New Job":"newjob",
    "Easter":"easter","Christmas":"xmas","Divorce":"divorce","Golf":"golf","Unicorn":"unicorn",
    "Personalised Cards":"other",
}
for k in KIDS_SHOWS: FAMILY.setdefault(k, "kids")

# ----------------------------------------------------------- helpers ----
def pick(options, *seed):
    h = int(hashlib.md5("|".join(map(str, seed)).encode()).hexdigest(), 16)
    return options[h % len(options)]

CODE_RE = re.compile(r"\b(Mc|Rm|Rmbc|Fun|Td|Gb|Sj|Raf)\s?\d+[a-z]?(-[A-Za-z])?\b", re.I)
def clean_name(name: str) -> str:
    n = CODE_RE.sub("", name)
    n = re.sub(r"\bNaughty\s*\d+[a-z]?\b", "", n, flags=re.I)
    n = re.sub(r"\((SA|[A-Z]{1,3})\)", "", n)
    n = re.sub(r"\s*-\s*(Solid|Plain)\s+\w+\s*$", "", n, flags=re.I)
    n = re.sub(r"\s+-\s*(Fathers Day Card|Me To You)\s*$", "", n, flags=re.I)
    n = re.sub(r"\b(Birthday Card|Card)\s*$", "", n, flags=re.I).strip()
    n = re.sub(r"\s+\d{1,2}\s*$", "", n)          # trailing design number, e.g. "Funny Pug 3"
    n = re.sub(r"\s{2,}", " ", n).strip(" -.,")
    return n

def subject_of(name: str) -> str:
    """Same reduction used to build the research keys."""
    n = name
    n = re.sub(r"\b(Mc|Rm|Rmbc|Fun|Td|Gb|Sj)\d+[a-z]?(-[A-Za-z])?\b", "", n, flags=re.I)
    n = re.sub(r"\bNaughty\s*\d+[a-z]?\b", "", n, flags=re.I)
    n = re.sub(r"\((SA|[A-Z]{1,3})\)", "", n)
    for w in ["Personalised","Personalized","Celebrity Fan","Celebrity","Football Fan Card","Football Birthday Card","Football Card","Birthday Card","Bollywood","Music","Wwe","Kidshows","Funny","Novelty","Card"]:
        n = re.sub(r"\b"+re.escape(w)+r"\b", "", n, flags=re.I)
    n = re.sub(r"\s+\d+\s*$", "", n); n = re.sub(r"\b\d\b", "", n)
    return re.sub(r"\s+", " ", n).strip(" -")

def sentence_case(s: str) -> str:
    """Turn a Title Case slogan into a readable sentence, keeping I / I'm etc."""
    words = s.split()
    out = []
    for i, w in enumerate(words):
        if i == 0 or w.lower() in ("i", "i'm", "i'll", "i've", "i'd") or re.match(r"^[A-Z]{2,}$", w):
            out.append(w)
        else:
            out.append(w.lower())
    t = " ".join(out)
    t = re.sub(r"\bi\b", "I", t)
    t = re.sub(r"([.!?])\s+([a-z])", lambda m: m.group(1)+" "+m.group(2).upper(), t)
    t = t.replace(" dont ", " don't ").replace(" cant ", " can't ").replace(" youre ", " you're ").replace(" havent ", " haven't ").replace(" im ", " I'm ").replace("Im ", "I'm ")
    return t

DEATH_RE = re.compile(r"\b(died|death|passed away|the late|deceased|killed|murder|suicide)\b", re.I)
def tidy_research(r: dict) -> dict:
    r = dict(r)
    who = (r.get("who") or "").strip().rstrip(".")
    who = re.split(r";|\s+rather than\s|,\s*not a specific", who)[0].strip()
    who = re.sub(r"^a generic ", "a ", who)
    who = re.sub(r"\bthe late\s+", "", who)
    if "check the product image" in who.lower(): who = who.split(" check the")[0].strip(" ,;")
    hook = (r.get("hook") or "").strip().rstrip(".")
    if DEATH_RE.search(hook) or DEATH_RE.search(who) or "check the product image" in hook.lower() or "disclaimer" in hook.lower(): hook = ""
    if DEATH_RE.search(who): who = ""
    r["who"], r["hook"] = who, hook
    return r

def esc(s: str) -> str:
    return html.escape(s, quote=False)

def trim(s: str, n: int) -> str:
    if len(s) <= n: return s
    cut = s[:n].rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:-") + ("" if cut.endswith(".") else "")

# ------------------------------------------------------- copy blocks -----
def personalise_block(fam, seed):
    lead = pick([
        "Choose your size, add a name and age if the design has space for them, and decide whether you want a printed message inside or a blank card to write in yourself.",
        "Pick A6, A5 or A4, type in a name and age where the design needs one, and tell us if you'd like us to print a message inside.",
        "Select the size you want, enter any name or age the design calls for, and either leave the inside blank or have us print your words.",
    ], seed, "p1")
    photo = pick([
        "If the design has a photo space, upload your picture on the product page and we'll drop it in.",
        "Designs with a photo space let you upload a picture straight from your phone or computer.",
        "Where the design takes a photo, just upload one on this page and we do the rest.",
    ], seed, "p2")
    return f"<p>{lead} {photo} Everything you type is printed exactly as you enter it, so do check spelling before you order.</p>"

def why_block(fam, seed):
    base = [
        "Printed on thick 350gsm silk card, so it feels like a proper shop-bought card, not a flimsy print",
        "Machine scored for a crisp, clean fold",
        "Comes with a bright coloured envelope that matches the design",
        "Posted inside a kraft outer envelope, so you can check it before handing it over",
        "Three sizes, from a neat A6 to a whopping A4",
    ]
    extra = {
        "celeb": ["Made for a fan, so it's a card they'll actually keep"],
        "club": ["Perfect for the supporter who bleeds the club colours"],
        "bollywood": ["A fun pick for any Bollywood fan"],
        "rude": ["Properly rude, so make sure they can take a joke"],
        "rude_val": ["Rude enough to make them blush on Valentine's Day"],
        "kids": ["Bright, bold and made to be loved by little ones"],
        "wedding": ["A keepsake they'll want to hold on to"],
        "couples": ["Funny because it's true"],
        "animals": ["Guaranteed to get a smile"],
        "dad": ["Made for the dad who laughs at his own jokes"],
        "teacher": ["A thoughtful way to say thank you at the end of term"],
        "photo": ["Your own photo makes it one of a kind"],
    }
    items = base + extra.get(fam, [])
    # rotate order a little so pages are not identical
    k = int(hashlib.md5(str(seed).encode()).hexdigest(), 16) % 3
    items = items[k:] + items[:k]
    return "<ul>" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"

def delivery_block(seed):
    a = pick([
        "Order before 1pm Monday to Friday and we print and post your card the same working day.",
        "Cards ordered before 1pm on a working day are printed and posted that same day.",
    ], seed, "d1")
    b = f"Standard 1st Class Royal Mail postage is {POSTAGE} per order, and there's a next-day Special Delivery option at checkout if it's urgent."
    return f"<p>{a} {b}</p>"

def contact_block():
    phone = f" or call us on {esc(PHONE)}" if PHONE else ""
    return (f"<p>Want something you can't see here? We design cards from scratch using your own photos and wording. "
            f"Email <a href=\"mailto:{EMAIL}\">{EMAIL}</a>{phone} and we'll sort it.</p>")

def disclaimer(kind, name, extra=""):
    if kind == "other":
        return (f"This is an unofficial, fan-made design created and printed by {STORE}. It is not endorsed by, sponsored by, or affiliated with "
                f"any club, league, player, performer or rights holder. Any names are used only to describe the design and who it's for. All trademarks belong to their respective owners.")
    if kind == "club":
        return (f"This is an unofficial, fan-made design created and printed by {STORE}. It is not endorsed by, sponsored by, or affiliated with {name}, "
                f"any league, or any club or player. Club names are used only to describe the design and who it's for. All trademarks belong to their respective owners.")
    if kind == "person":
        return (f"This is an unofficial fan card made for fun. {name} has not endorsed, sponsored or approved this product, and {STORE} has no connection with them. "
                f"The name is used only to describe the design and who the card is for.")
    if kind == "band":
        return (f"This is an unofficial fan design. It is not endorsed by, or connected with, {name}, their management or record label. "
                f"All names and trademarks belong to their respective owners.")
    return (f"This is an unofficial design inspired by {name}. It is not official merchandise and is not endorsed by, sponsored by, or connected with "
            f"{name}, its creators or rights holders, or any of their licensees. All names, characters and trademarks belong to their respective owners.")

# --------------------------------------------------------- openings -----
OCCASION = {
    "rude":"birthday","rude_val":"Valentine's Day","rude_anniv":"anniversary","rude_thanks":"thank you","rude_xmas":"Christmas",
    "funny":"birthday","birthday":"birthday","her":"birthday","him":"birthday","animals":"birthday","wedding":"wedding",
    "couples":"anniversary","anniv":"anniversary","val":"Valentine's Day","dad":"Father's Day","mum":"Mother's Day",
    "lgbt":"birthday","thanks":"thank you","teacher":"thank you","first":"1st birthday","baby":"new baby","school":"first day at school",
    "eid":"Eid","yoga":"birthday","getwell":"get well soon","voyage":"bon voyage","congrats":"congratulations","grad":"graduation",
    "sympathy":"sympathy","leaving":"leaving","sorry":"sorry","luck":"good luck","friend":"friendship","justsay":"just to say",
    "exams":"exam","dance":"birthday","other":"greetings","photo":"photo","newjob":"new job","easter":"Easter","xmas":"Christmas",
    "divorce":"divorce","golf":"birthday","unicorn":"birthday","kids":"birthday","celeb":"birthday","club":"birthday","bollywood":"birthday","show":"birthday",
}

def opening(p, fam, cat, research):
    name = p["name"]; seed = p["id"]
    cn = clean_name(name)
    r = research
    if fam in ("celeb", "club", "bollywood", "show", "kids"):
        if not r or r.get("unsure"):
            r = {"name": subject_of(name) or cn, "who": "", "hook": "", "type": "generic"}
        r = tidy_research(r)
        who = r.get("who", ""); nm = r.get("name") or cn; hook = r.get("hook", "")
        comma_who = f", {who}" if who else ""
        if r.get("type") in ("other", "generic"):
            design = who or f"the {esc(nm)} design"
            occ_word = {"club": "football birthday", "kids": "birthday", "bollywood": "birthday"}.get(fam, "birthday")
            s1 = pick([
                f"A personalised {occ_word} card featuring {design}.",
                f"This personalised {occ_word} card shows {design}.",
            ], seed, "o")
            s2 = pick(["Add their name and age and we print it on the front.", "We print their name and age on the card so it's made just for them."], seed, "o2")
            return f"<p>{esc(s1)} {s2}</p>", nm, ""
        occ = "birthday" if "birthday" in name.lower() or fam != "show" else "birthday"
        if fam == "club":
            s1 = pick([
                f"A personalised birthday card for {nm} fans{comma_who}.",
                f"Made for anyone who follows {nm}{comma_who}, this personalised birthday card puts their club front and centre.",
                f"Know a {nm} supporter? This personalised card is made for them.",
            ], seed, "o")
            s2 = pick([
                "Add their name and age and it becomes a card no other fan has.",
                "We print their name and age on the front so it's theirs alone.",
                "With their name and age added, it beats anything off the shelf.",
            ], seed, "o2")
        elif fam == "bollywood":
            s1 = pick([
                f"A personalised birthday card for fans of {nm}{comma_who}.",
                f"This personalised birthday card is for anyone who loves {nm}{comma_who}.",
            ], seed, "o")
            s2 = pick(["Add their name and age and we print it just for them.", "Their name and age go on the front, printed by us, so it's one of a kind."], seed, "o2")
        elif fam in ("show", "kids"):
            s1 = pick([
                f"A personalised birthday card inspired by {nm}{comma_who}.",
                f"For a little fan of {nm}{comma_who}, this personalised birthday card is a sure-fire hit.",
            ], seed, "o") if fam == "kids" else pick([
                f"A personalised birthday card for fans of {nm}{comma_who}.",
                f"This personalised card is inspired by {nm}{comma_who}.",
            ], seed, "o")
            s2 = pick(["Add their name and age and we print it on the front.", "We print their name and age on the card so it's made just for them."], seed, "o2")
        else:  # celeb person/band
            s1 = pick([
                f"A personalised birthday card for fans of {nm}{comma_who}.",
                f"Know someone who adores {nm}{comma_who}? This personalised birthday card is made for them.",
                f"This personalised birthday card features {nm}{comma_who}.",
            ], seed, "o")
            s2 = pick([
                "Add their name and age and it's printed just for them.",
                "We print their name and age on the front, so it's theirs and no one else's.",
                "Their name and age go on the card, printed by us, so it's a proper one-off.",
            ], seed, "o2")
        s3 = f" {esc(hook)}." if hook else ""
        return f"<p>{esc(s1)} {esc(s2)}{s3}</p>", nm, who
    # slogan / generic families
    occ = OCCASION.get(fam, "greetings")
    slogan = sentence_case(cn) if cn and len(cn.split()) > 2 else cn
    quoted = f"“{esc(slogan)}”" if slogan else ""
    if fam in ("rude", "rude_val", "rude_anniv", "rude_thanks", "rude_xmas"):
        s1 = pick([
            f"A rude {occ} card that says {quoted}.",
            f"Not one for your nan: this rude {occ} card reads {quoted}.",
            f"If they've got a filthy sense of humour, this {occ} card, {quoted}, will land perfectly.",
        ], seed, "o") if quoted else f"A rude personalised {occ} card for someone with a filthy sense of humour."
        s2 = pick([
            "Add a name and we print it on the front, so the insult is personal.",
            "Personalise it with their name so there's no doubt who it's aimed at.",
            "We print their name on the card to make it extra personal.",
        ], seed, "o2")
    elif fam in ("wedding",):
        s1 = pick([
            f"A personalised wedding card with the words {quoted}.",
            f"Celebrate the happy couple with this personalised card: {quoted}.",
            f"This wedding card says {quoted}, and we print the couple's names so it's theirs alone.",
        ], seed, "o") if quoted else "A personalised card for a wedding, engagement or anniversary."
        s2 = pick(["Add their names and the date and we print it for you.", "Personalise it with their names for a card they'll keep."], seed, "o2")
    elif fam in ("couples", "anniv", "val"):
        s1 = pick([
            f"A personalised {occ} card that says {quoted}.",
            f"Say it with this {occ} card: {quoted}.",
            f"For the one you love (most of the time), this {occ} card reads {quoted}.",
        ], seed, "o") if quoted else f"A personalised {occ} card for the one you love."
        s2 = pick(["Add their name and we print it on the front.", "We print their name on the card so it's made just for them."], seed, "o2")
    elif fam == "animals":
        s1 = pick([
            f"A funny personalised birthday card featuring {esc(slogan.lower() if slogan else 'a cheeky animal')}.",
            f"This personalised birthday card stars {esc(slogan.lower() if slogan else 'a cheeky animal')}, and it's guaranteed to get a laugh.",
        ], seed, "o")
        s2 = pick(["Add their name and age and we print it on the front.", "We print their name and age on the card so it's made for them."], seed, "o2")
    elif fam == "dad":
        s1 = pick([
            f"A funny Father's Day card that says {quoted}.",
            f"Make Dad laugh this Father's Day with a card that reads {quoted}.",
        ], seed, "o") if quoted else "A funny personalised Father's Day card."
        s2 = "Add his name, or what you call him, and we print it on the front."
    elif fam == "teacher":
        s1 = pick([
            f"A personalised thank-you card for a teacher: {quoted}.",
            f"Say thank you at the end of term with this card, {quoted}.",
        ], seed, "o") if quoted else "A personalised thank-you card for a brilliant teacher."
        s2 = "Add the teacher's name and your child's name and we print both."
    elif fam in ("first", "baby", "school"):
        s1 = pick([
            f"A personalised {occ} card: {quoted}.",
            f"Celebrate their {occ} with this personalised card, {quoted}.",
        ], seed, "o") if quoted else f"A personalised {occ} card."
        s2 = "Add the little one's name and we print it on the front."
    elif fam == "photo":
        s1 = f"A personalised photo card: {quoted}." if quoted else "A personalised photo card."
        s2 = "Upload your photo, add a name or message, and we print it all for you."
    else:
        s1 = pick([
            f"A personalised {occ} card that says {quoted}.",
            f"This personalised {occ} card reads {quoted}.",
            f"Say it properly with a {occ} card that reads {quoted}.",
        ], seed, "o") if quoted else f"A personalised {occ} card."
        s2 = pick(["Add their name and we print it on the front.", "We print their name on the card so it's made just for them."], seed, "o2")
    return f"<p>{s1} {s2}</p>", (slogan or cn), ""

# ------------------------------------------------------------ build ----
def build(p, cat_name, research):
    fam = FAMILY.get(cat_name, "other")
    seed = p["id"]
    open_html, subj, who = opening(p, fam, cat_name, research)
    occ = OCCASION.get(fam, "greetings")
    h2 = {
        "celeb": f"Personalised {subj} birthday card",
        "club": f"Personalised {subj} football birthday card",
        "bollywood": f"Personalised {subj} Bollywood birthday card",
        "kids": f"Personalised {subj} birthday card",
        "show": f"Personalised {subj} card",
    }.get(fam, f"Personalised {occ} card" if occ not in ("greetings", "photo") else "Personalised card")
    parts = [
        open_html,
        f"<h2>{esc(h2)}</h2>",
        personalise_block(fam, seed),
        "<h3>Why you'll love it</h3>", why_block(fam, seed),
        "<h3>Size &amp; details</h3>",
        f"<ul>{SIZES_HTML}<li>350gsm silk card, printed in-house in the UK</li><li>Matching coloured envelope, plus a kraft outer envelope for posting</li><li>Blank inside unless you choose a printed message</li></ul>",
        "<h3>Delivery</h3>", delivery_block(seed),
        contact_block(),
    ]
    r = research or {}
    if fam in ("celeb", "club", "bollywood", "show", "kids"):
        rtype = r.get("type") if r and not r.get("unsure") else "generic"
        if rtype in ("other", "generic"):
            kind = "other" if fam == "club" else None
        else:
            kind = {"club": "club", "band": "band", "person": "person"}.get(rtype, "inspired")
        if kind:
            parts += ["<h3>Please note</h3>", f"<p class=\"disclaimer\">{esc(disclaimer(kind, subj))}</p>"]
    desc = "\n".join(parts)

    # SEO
    base_title = {
        "celeb": f"{subj} Personalised Birthday Card",
        "club": f"{subj} Fan Personalised Birthday Card",
        "bollywood": f"{subj} Personalised Birthday Card",
        "kids": f"{subj} Personalised Birthday Card",
        "show": f"{subj} Personalised Card",
    }.get(fam)
    if base_title is None:
        prefix = {"rude": "Rude Birthday Card", "rude_val": "Rude Valentine's Card", "rude_anniv": "Rude Anniversary Card",
                  "rude_thanks": "Rude Thank You Card", "rude_xmas": "Rude Christmas Card", "funny": "Funny Birthday Card",
                  "animals": "Funny Birthday Card", "wedding": "Wedding Card", "couples": "Funny Anniversary Card",
                  "anniv": "Anniversary Card", "val": "Valentine's Card", "dad": "Father's Day Card", "mum": "Mother's Day Card",
                  "teacher": "Teacher Thank You Card", "thanks": "Thank You Card", "first": "1st Birthday Card",
                  "baby": "New Baby Card", "photo": "Photo Card"}.get(fam, f"{occ.title()} Card" if occ != "greetings" else "Personalised Card")
        cn_title = clean_name(p["name"])
        base_title = f"{prefix} – {cn_title}" if cn_title and cn_title.lower() != prefix.lower() else prefix
    tail = " | Personalised Cards"
    title = base_title if len(base_title) > 60 - len(tail) else base_title + tail
    if len(title) > 60: title = trim(base_title, 60)
    if fam in ("celeb", "club", "bollywood", "kids", "show"):
        meta = f"Personalised {subj} birthday card with their name and age printed on the front. Thick 350gsm card, matching envelope, posted same day before 1pm."
    elif fam.startswith("rude"):
        meta = f"Rude personalised {occ} card with their name printed on it. Thick 350gsm card, matching envelope, posted same working day if ordered before 1pm."
    else:
        meta = f"Personalised {occ} card with their name printed on the front. Thick 350gsm card, matching envelope, posted same working day if ordered before 1pm."
    meta = trim(meta, 155)
    return {"description": desc, "page_title": title, "meta_description": meta, "family": fam, "subject": subj}

def main():
    scratch = sys.argv[1]
    P = json.load(open(f"{scratch}/products.json"))
    C = {c["id"]: c["name"] for c in json.load(open(f"{scratch}/categories.json"))}
    research = {}
    for f in sorted(glob.glob(f"{scratch}/research/*.json")):
        research.update(json.load(open(f)))
    ids = None
    if "--ids" in sys.argv:
        ids = {int(x) for x in sys.argv[sys.argv.index("--ids") + 1].split(",")}
    out = {}
    for p in P:
        if ids and p["id"] not in ids: continue
        cat = C.get(p["categories"][0], "") if p["categories"] else ""
        r = research.get(subject_of(p["name"]))
        out[p["id"]] = build(p, cat, r)
    json.dump(out, open(f"{scratch}/rewrite.json", "w"), indent=1)
    fams = {}
    for v in out.values(): fams[v["family"]] = fams.get(v["family"], 0) + 1
    print("built", len(out), "| families:", dict(sorted(fams.items(), key=lambda x: -x[1])))
    print("research entries:", len(research))

if __name__ == "__main__":
    main()
