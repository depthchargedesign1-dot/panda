"""Build DRAFT product-import CSVs for celebrity face masks whose artwork is in Dropbox but not yet on the store.

Inputs (all read-only):
  <work>/upload_part{0..3}.json     items: key, name, character, category, sport, show, known_as
  <work>/upload_done{0..3}.jsonl    Shopify Files uploads (latest line per key wins); upload_done_fix.jsonl too
  <work>/all_products.jsonl         bulk export of every product: id, handle, title, status, productType, tags
  <work>/all_skus.jsonl             bulk export of every variant: sku, product.handle
  <work>/recent_files.jsonl         bulk export of Files since 2 Oct (id, fileStatus, image.url): live READY status and exact URL
  exports/face-masks/dropbox-masks-master-list.csv   per-person blurb (intro paragraph)

Copy comes from tools/mask_copy.py (build) fed with the person's name, category, sport, show and blurb, so the
house structure, facts ("Face masks" sheet) and celebrity disclaimer are the same as the live masks. Cartoon and
film characters get the CLAUDE.md character disclaimer naming the rights holder instead; brand mascots get the
brand template. Football/sport blurbs that name a club or national team add the football wording.

Structure copies the 2 Oct 2026 skill-built masks (Graeme Swann, Cole Anderson-James, Jack Joseph):
option "Style" = Ready to Wear £2.99 (SKU FaceMask-<Name>) / DIY £1.50 (SKU FaceMask-<Name>-DIY),
type "Celebrity Facemask", vendor Foxy Printing, category Masks, the standard assembly/info/lifestyle images.

Usage: python3 tools/new_masks_build.py <work_dir> <out_dir>
"""
import csv
import hashlib
import html
import json
import os
import re
import sys
import unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mask_copy as MC  # noqa: E402
from age_group import age_group  # noqa: E402

ROOT = os.path.dirname(HERE)
MASTER = os.path.join(ROOT, "exports/face-masks/dropbox-masks-master-list.csv")

PRICE_RTW, PRICE_DIY = "2.99", "1.50"
CATEGORY = "Apparel & Accessories > Costumes & Accessories > Masks"
EXTRA_IMAGES = [  # identical on all three templates (and in the celebrity-face-mask-listing skill)
    ("https://cdn.shopify.com/s/files/1/1774/9115/files/How_to_do_MASK_ASSEMBLEY.png?v=1790758437",
     "How to assemble a ready-to-wear card face mask"),
    ("https://cdn.shopify.com/s/files/1/1774/9115/files/How_to_do_DIY_ASSEMBLEY_Mask.png?v=1790758437",
     "How to assemble a DIY card face mask kit"),
    ("https://cdn.shopify.com/s/files/1/1774/9115/files/57-_5_-_CORRECT-INFO_-small_5bf618d2-e926-4a92-8838-bb2b53d756ff.jpg?v=1742557671",
     "Card face mask product information"),
    ("https://cdn.shopify.com/s/files/1/1774/9115/files/MaskUploadimage1_753a44fd-ff7a-4b8d-9bed-b7070b4516dc.jpg?v=1742557671",
     "Example of printed card face masks in use at a party"),
    ("https://cdn.shopify.com/s/files/1/1774/9115/files/MaskUploadImage2_15e5fa9c-9ebb-47ac-82be-d57f08c928f5.jpg?v=1742557670",
     "Printed card face masks for group photos and fancy dress"),
]
BASE_TAGS = ["Cardboard Face Masks", "Celebrity Face Mask", "Celebrity Party Masks", "Costume Mask", "Face Mask", "Facemask",
             "Fancy Dress", "Photo Booth Prop", "TV Stars And Celebrity Masks", "new-arrivals", "foxy-new-2026",
             "foxy-range-celebrity-masks", "foxy-src-dropbox", "foxy-new-masks-oct2026", "third-party-name", "celebrity-face-mask"]
CAT_TAG = {"football": "mask-footballers", "sport": "mask-sport", "tv": "mask-tv-stars", "film": "mask-film-stars",
           "music": "mask-music", "comedy": "mask-comedians", "reality": "mask-reality-tv", "royal": "mask-politicians-royals",
           "politics": "mask-politicians-royals", "characters": "mask-characters", "models": "mask-tv-stars", "other": "mask-tv-stars"}
LEGACY_TAG = {"football": ["FOOTBALLERS", "Sport Celebrities"], "sport": ["SPORTS STARS", "Sport Celebrities"], "music": ["MUSIC STARS"],
              "royal": ["Politicians And Royals"], "politics": ["Politicians And Royals"], "film": ["MOVIE STARS"],
              "characters": ["MOVIE STARS"]}

# Generic Halloween/novelty designs: no person or character, so the celebrity copy doesn't fit. Left for the owner.
GENERIC = {"Acid Smiley", "Scary Clown", "Halloween Scary Face", "Pumpkin Man", "Scary Hockey Mask", "Halloween Wizard",
           "Grim Reaper", "Scary Skin Mask", "Green Zombie", "Screaming Eyes", "Halloween Monkey", "Santa Claws", "Mr Hyde",
           "Frankenstein's monster"}
MINORS = {"Princess Charlotte", "Prince Louis"}  # real children: owner to decide
# Checked by hand: the store product is someone else (Adriano Celentano, Danilo Fischetti) or a couple pack, not this person.
REAL_PEOPLE_AS_CHARACTERS = {"Chloë Grace Moretz", "Jennifer Tilly", "Fred Gwynne"}  # actors listed under "characters"
NOT_DUPLICATE = {"Adriano", "Danilo", "Gisele Bündchen"}

# Character template: show -> (what it's inspired by, rights holder(s)). Brand mascots use the brand template.
RIGHTS = {
    "Up": "Disney and Pixar", "Despicable Me": "Illumination and Universal Pictures", "James Bond": "Eon Productions, Danjaq or Amazon MGM Studios",
    "Forrest Gump": "Paramount Pictures", "A Nightmare on Elm Street": "New Line Cinema or Warner Bros.",
    "The Simpsons": "20th Television or Disney", "King Kong": "the film studios that own King Kong", "Mickey Mouse": "Disney",
    "Toy Story": "Disney, Pixar or Hasbro", "Peppa Pig": "Hasbro or Entertainment One", "Children in Need": "BBC Children in Need",
    "LazyTown": "LazyTown Entertainment", "Harry Potter": "Warner Bros. or J.K. Rowling", "SpongeBob SquarePants": "Nickelodeon or Paramount",
    "Monsters, Inc.": "Disney and Pixar", "The Muppets": "Disney or The Muppets Studio", "Worzel Gummidge": "its producers or rights holders",
    "Guardians of the Galaxy": "Marvel or Disney", "Sex and the City": "HBO or Warner Bros. Discovery", "Pinky and the Brain": "Warner Bros.",
    "Back to the Future": "Universal Pictures or Amblin Entertainment", "Fifi and the Flowertots": "its producers or rights holders",
    "Diary of a Wimpy Kid": "Jeff Kinney, his publishers or the film studios", "Thunderbirds": "ITV Studios",
    "Grand Theft Auto IV": "Rockstar Games or Take-Two Interactive", "Family Guy": "20th Television or Disney", "Marvel": "Marvel or Disney",
    "High School Musical": "Disney", "Peter Pan": "Disney", "The Flintstones": "Hanna-Barbera or Warner Bros.",
    "Twilight": "Summit Entertainment or Lionsgate", "Creepy": "its publishers or rights holders",
    "The Shawshank Redemption": "Castle Rock Entertainment or Warner Bros.", "Rugrats": "Nickelodeon or Paramount",
    "Dora the Explorer": "Nickelodeon or Paramount", "Fireman Sam": "Mattel", "Postman Pat": "DreamWorks Classics or Universal",
    "Charlie and the Chocolate Factory": "The Roald Dahl Story Company or Netflix", "Shrek": "DreamWorks Animation or Universal",
    "The Avengers": "Marvel or Disney", "The Big Bang Theory": "Warner Bros. Television", "Strawberry Shortcake": "WildBrain",
    "The Incredible Hulk": "Marvel or Disney", "Betty Boop": "Fleischer Studios or King Features", "Supernatural": "Warner Bros. Television",
    "Dallas": "Warner Bros. Television", "Batman": "DC or Warner Bros.", "Star Wars": "Lucasfilm or Disney", "Hello Kitty": "Sanrio",
    "Sesame Street": "Sesame Workshop", "Fear and Loathing in Las Vegas": "Universal Pictures or the Hunter S. Thompson estate",
    "Saw": "Lionsgate", "Top Gear": "the BBC", "The Lord of the Rings": "Middle-earth Enterprises or Warner Bros.",
    "Labyrinth": "The Jim Henson Company or Sony Pictures", "Home Alone 2": "20th Century Studios or Disney",
    "The BFG": "The Roald Dahl Story Company", "Kick-Ass": "Marv Studios or Lionsgate", "Child's Play": "Universal Pictures",
    "The Munsters": "Universal", "LEGO": None,
}
BRANDS = {"Lego Minifigure": ("LEGO", "the LEGO Group"), "Aleksandr Orlov": ("Compare the Market", "BGL Group"),
          "Flat Eric": ("Levi's", "Levi Strauss & Co.")}
KIDS_SHOWS = {"Up", "Despicable Me", "Mickey Mouse", "Toy Story", "Peppa Pig", "Children in Need", "LazyTown", "SpongeBob SquarePants",
              "Monsters, Inc.", "The Muppets", "Fifi and the Flowertots", "Diary of a Wimpy Kid", "Peter Pan", "Rugrats", "Dora the Explorer",
              "Fireman Sam", "Postman Pat", "Shrek", "Strawberry Shortcake", "Hello Kitty", "Sesame Street", "The BFG",
              "Worzel Gummidge", "Thunderbirds", "Charlie and the Chocolate Factory", "Pinky and the Brain"}
EXTRA_CLUBS = (r"Borussia Dortmund|Dortmund|Bayer Leverkusen|Schalke|AC Milan|Inter Milan|Inter|Napoli|Roma|Lazio|Ajax|PSV|Porto|Benfica|"
               r"Sporting|Atl[eé]tico Madrid|Valencia|Sevilla|Villarreal|Marseille|Lyon|Monaco|Galatasaray|Fenerbah[cç]e|Santos|Flamengo|"
               r"Boca Juniors|River Plate|LA Galaxy|Inter Miami|Aston Villa|Middlesbrough|Watford|Norwich|Stoke|Blackburn|Bolton|Derby|"
               r"Coventry|Hull|QPR|Portsmouth|Hibernian|Hearts|Aberdeen|Dundee|Northern Ireland|Brazil|Argentina|Spain|France|Germany|"
               r"Italy|Portugal|Netherlands|Belgium|Croatia")
NATIONS = {"Brazil", "Argentina", "Spain", "France", "Germany", "Italy", "Portugal", "Netherlands", "Belgium", "Croatia", "Northern Ireland","England", "Scotland", "Wales", "Ireland", "Lionesses"}

# Two extra copy profiles for characters (monkey-patched onto mask_copy's category table).
MC.CATS.append(("kidschar", r"$^", "much-loved character", "kids and families",
                ["a children's birthday party", "World Book Day", "a family fancy dress day", "a kids' movie night"]))
MC.CATS.append(("character", r"$^", "famous character", "film and TV fans",
                ["a movie night", "a Halloween party", "a themed birthday", "a fancy dress night out"]))


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower().replace("&", " and ")
    s = re.sub(r"['’`]", "", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def slug(s):
    return norm(s).replace(" ", "-")


def sku_base(name):
    return "FaceMask-" + "".join(w[:1].upper() + w[1:] for w in norm(name).split())


def latest(path):
    d = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            if line.strip():
                r = json.loads(line)
                d[r["key"]] = r
    return d


def theme(cat, sport):
    return {"football": "Football Fan", "sport": "Sports Fan", "music": "Music Fan", "comedy": "Comedy Night", "reality": "Reality TV",
            "royal": "Street Party", "politics": "Election Night", "film": "Movie Night", "tv": "TV Night",
            "characters": "Character"}.get(cat, "Celebrity")


def disclaimer(it, name, blurb):
    show = it["show"] or ""
    cat = it["category"]
    if name in BRANDS:
        b, owner = BRANDS[name]
        return (f"This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {b} or {owner}. "
                f"{b} is a trademark of its owner and is used only to describe the design theme.")
    is_person = cat != "characters" or name in REAL_PEOPLE_AS_CHARACTERS
    if not is_person:
        who = show if show and show != name else name
        holder = RIGHTS.get(show) or "its creators or rights holders"
        inspired = name if not show or show == name else f"{name} from {show}"
        return (f"This is an unofficial design inspired by {inspired}. It is not official merchandise and is not endorsed by, sponsored by, "
                f"or connected with {who}, {holder}, or any of their licensees. All names, characters and trademarks belong to their respective owners.")
    text = (f"This is an unofficial novelty product made for fun and fancy dress. {name} has not endorsed, sponsored or approved this product, "
            f"and Foxy Printing has no connection with them" + (f" or with {show}, its producers or broadcasters" if show else "") +
            (". The names are used only to describe the design." if show else ". The name is used only to describe the design."))
    if cat in ("football", "sport"):
        clubs = []
        for m in re.finditer(r"\b(?:" + MC.CLUBS + "|" + EXTRA_CLUBS + r")\b", blurb):
            c = m.group(0)
            if c in NATIONS and cat != "football":  # "a golfer from Spain" isn't a team reference
                continue
            c = f"the {c} national team" if c in NATIONS and c != "Lionesses" else ("the England Lionesses" if c == "Lionesses" else c)
            if c not in clubs:
                clubs.append(c)
        if clubs:
            lst = ", ".join(clubs[:-1]) + (" or " if len(clubs) > 1 else "") + clubs[-1]
            text += (f" It is not endorsed by, sponsored by, or affiliated with {lst}, or any club, league or player. Club and team names are "
                     f"used only to describe who it's for. All trademarks belong to their respective owners.")
    return text


def SPORT_CAT_KEY(ident):  # same category resolution as mask_copy.build(ident=...)
    if ident.get("category") == "sport":
        return MC.SPORT_CAT.get(ident.get("sport") or "", "sport")
    return MC.IDENT_CAT.get(ident.get("category"), "celeb")


FILLERS = [" Posted in a board-backed envelope.", " Ideal for groups.", " Quick UK delivery.", " Fun for all.", " Order today.", " UK made."]


def make_meta(name, handle):
    """Meta description of 140-155 characters made of whole sentences only (mask_copy's own filler can cut mid-phrase)."""
    k = MC.IDENT_CAT.get("_last")  # set per product before calling
    occ = k[4]
    o1 = MC.pick(occ, handle, "o1")
    bases = [f"{name} card face mask for {o1}. Printed on 350gsm silk card cut to shape with eye holes and elastic. Order yours today.",
             f"Fancy dress made easy: a {name} face mask on thick card with eye holes and elastic. Perfect for {o1} and photo booths.",
             f"Get the party started with a {name} face mask. Full-colour print on 350gsm card, cut to shape with elastic. Great for {o1}.",
             f"A {name} face mask printed on 350gsm silk card, cut to shape with eye holes and elastic. Great for {o1}.",
             f"{name} face mask on thick 350gsm card with eye holes and elastic."]
    start = int(hashlib.md5((handle + "meta").encode()).hexdigest(), 16) % 3
    for base in bases[start:3] + bases[:start] + bases[3:]:
        if len(base) > 155:
            continue
        m = base
        for f in FILLERS:
            if len(m) >= 140:
                break
            if len(m + f) <= 155:
                m += f
        if 140 <= len(m) <= 155:
            return m
    return None


def main(work, out):
    os.makedirs(out, exist_ok=True)
    items = []
    for n in range(4):
        items += json.load(open(f"{work}/upload_part{n}.json", encoding="utf-8"))
    done = {}
    for n in range(4):
        done.update(latest(f"{work}/upload_done{n}.jsonl"))
    done.update(latest(f"{work}/upload_done_fix.jsonl"))
    live_path = f"{work}/recent_files.jsonl"  # bulk export of Files (id, fileStatus, image.url): live status wins
    if os.path.exists(live_path):
        live = {}
        for l in open(live_path, encoding="utf-8"):
            o = json.loads(l)
            live[o["id"]] = o
        for r in done.values():
            o = live.get(r.get("shopify_file_id"))
            r["status"] = o["fileStatus"] if o else "MISSING"
            r["url"] = ((o or {}).get("image") or {}).get("url") or ""
    master = {r["key"]: r for r in csv.DictReader(open(MASTER, encoding="utf-8"))}

    prods = [json.loads(l) for l in open(f"{work}/all_products.jsonl", encoding="utf-8")]
    store_handles = {p["handle"] for p in prods}
    store_skus = {}
    for l in open(f"{work}/all_skus.jsonl", encoding="utf-8"):
        o = json.loads(l)
        if o.get("sku"):
            store_skus.setdefault(o["sku"].lower(), o["product"]["handle"])
    masks = [p for p in prods if ("celebrity-face-mask" in [t.lower() for t in p["tags"]] or "mask" in (p["productType"] or "").lower())
             and not re.search(r"face covering", p["title"], re.I)]
    mask_text = [(p, " " + norm(p["title"]) + " ", " " + norm(p["handle"].replace("-", " ")) + " ") for p in masks]
    json.dump([{k: p[k] for k in ("handle", "title", "status")} for p in masks], open(f"{work}/store_masks.json", "w"), ensure_ascii=False)

    def existing(phrase):
        n = " " + norm(phrase) + " "
        if len(n.strip()) < 3:
            return None
        for p, t, h in mask_text:
            if n in t:
                return p, "title"
        for p, t, h in mask_text:
            if n in h:
                return p, "handle only (title is someone else: check)"
        return None

    rows, skipped, seen = [], [], {}
    for it in items:
        name = it["name"].strip()
        r = done.get(it["key"])
        if not r or r.get("status") != "READY" or not (r.get("url") or "").startswith("https://cdn.shopify.com/"):
            skipped.append((it, "no READY Shopify artwork", "")); continue
        if name in GENERIC:
            skipped.append((it, "generic Halloween/novelty design, not a person or character: needs its own copy", "")); continue
        if name in MINORS:
            skipped.append((it, "real child (minor): owner to decide", "")); continue
        hit = None if name in NOT_DUPLICATE else existing(name)
        via = "name"
        if not hit and name not in NOT_DUPLICATE and it["character"] and it["character"] != name and len(norm(it["character"]).split()) >= 2:
            hit, via = existing(it["character"]), "character " + it["character"]
        if hit:
            p0, how = hit
            skipped.append((it, "already on the store", f"matched {via} in {how}: {p0['handle']} ({p0['status']}) {p0['title']}")); continue
        nk = norm(name)
        if nk in seen:
            skipped.append((it, "duplicate artwork in this batch", seen[nk])); continue
        seen[nk] = it["key"]
        rows.append((it, r, master[it["key"]]))

    products, used_handles, used_skus = [], set(), set()
    for it, r, m in rows:
        name = re.sub(r"\s+Mask$", "", it["name"].strip())  # "Saw Pig Mask" -> "Saw Pig"
        cat = it["category"]
        is_char = cat == "characters" and name not in REAL_PEOPLE_AS_CHARACTERS
        handle = slug(name) + "-face-mask"
        if handle in store_handles or handle in used_handles:
            handle = slug(name) + "-celebrity-card-face-mask"
        used_handles.add(handle)
        base = sku_base(name)
        sku, k = base, 2
        while sku.lower() in store_skus or (sku + "-DIY").lower() in store_skus or sku.lower() in used_skus:
            sku = f"{base}-{k}"; k += 1
        used_skus.add(sku.lower())
        ident = dict(name=name, show=it["show"] or None, category=cat, sport=it["sport"] or None, blurb=m["blurb"])
        if is_char:
            MC.IDENT_CAT["characters"] = "kidschar" if (it["show"] in KIDS_SHOWS or name in KIDS_SHOWS) else "character"
        else:
            MC.IDENT_CAT["characters"] = "film"
        title = (f"{name} Face Mask – Celebrity Card Face Mask" if not is_char else f"{name} Face Mask – Card Character Face Mask")
        p = {"handle": handle, "title": title, "productType": "Celebrity Facemask", "tags": []}
        b = MC.build(p, ident)
        kk = SPORT_CAT_KEY(ident)
        MC.IDENT_CAT["_last"] = next((c for c in MC.CATS if c[0] == kk), MC.DEFAULT)
        pk = f"{name} face mask"
        body = b["body"]
        first = re.split(r"(?<=[.!?])\s", m["blurb"])[0]
        if pk.lower() not in first.lower():  # house rule: primary keyword in the first sentence
            lead = MC.pick([f"Our {pk} is a quick way to get everyone laughing.",
                            f"This {pk} is printed on thick card and cut to shape, ready for the party.",
                            f"Add a {pk} to your fancy dress plans and get the camera ready."], handle, "lead")
            body = body.replace("<p>" + html.escape(m["blurb"], quote=False), "<p>" + html.escape(lead + " " + m["blurb"], quote=False), 1)
        disc = disclaimer(it, name, m["blurb"])
        disc = re.sub(r"(?<!\.)\.\.(?!\.)", ".", disc)  # "Monsters, Inc.." -> "Monsters, Inc." (keeps "...")
        body = re.sub(r'<p class="disclaimer">.*?</p>$', f'<p class="disclaimer">{html.escape(disc, quote=False)}</p>', body, flags=re.S)
        if len(re.sub(r"<[^>]+>", " ", body).split()) > 350:  # long club disclaimers: drop the 5th bullet (4 remain)
            body = re.sub(r"(<h3>Why you'll love it</h3>\n<ul>\n(?:<li>.*?</li>\n){4})<li>.*?</li>\n", r"\1", body, count=1)
        if is_char:  # the celebrity profile says "famous face"; fine for characters, but not "celebrity"
            body = body.replace("Celebrity Face Mask</h2>", "Character Face Mask</h2>")
        tags = list(BASE_TAGS) + [CAT_TAG.get(cat, "mask-tv-stars")] + LEGACY_TAG.get(cat, ["TV STARS"])
        if cat == "sport" and it["sport"] in MC.SPORT_CAT:
            tags.append("mask-" + it["sport"])
        if cat == "sport" and it["sport"]:
            tags.append(it["sport"].title() if it["sport"] != "f1" else "F1")
        if it["show"]:
            pass  # show names stay out of tags (third-party names are described in the copy only)
        age = age_group("Celebrity Facemask", f"{title} {it['show'] if is_char else ''}", tags)
        if is_char and (it["show"] in KIDS_SHOWS or name in KIDS_SHOWS):
            age = "kids"
        if not is_char:  # real people are always adult (age_group's character regex misfires on e.g. "Elsa Pataky")
            age = "adult"
        products.append(dict(key=it["key"], name=name, handle=handle, title=title, body=body, seo_title=b["seo_title"], meta=make_meta(name, handle),
                             tags=sorted(set(tags), key=str.lower), sku=sku, age=age, image=r["url"], is_char=is_char,
                             alt=f"{name} face mask – printed cardboard {'character' if is_char else 'celebrity'} face mask, front view",
                             category=cat, show=it["show"]))

    # ---- checks -------------------------------------------------------------------------------------------
    bad_words = re.compile(r"\b(licen[cs]ed|authentic|genuine|signed|autograph\w*)\b", re.I)
    problems = []
    bodies = Counter(p["body"] for p in products)
    for p in products:
        w = len(re.sub(r"<[^>]+>", " ", p["body"]).split())
        if not 180 <= w <= 350: problems.append((p["handle"], f"words {w}"))
        if len(p["seo_title"]) > 60: problems.append((p["handle"], "seo title > 60"))
        if not p["meta"] or not 140 <= len(p["meta"]) <= 155 or not p["meta"].endswith("."):
            problems.append((p["handle"], f"meta {p['meta']!r}"))
        if p["body"].count("<h2>") != 1: problems.append((p["handle"], "h2 count"))
        if not p["body"].rstrip().endswith("</p>") or '<p class="disclaimer">' not in p["body"].rsplit("<h3>", 1)[-1]: problems.append((p["handle"], "disclaimer not last"))
        if "[" in p["body"]: problems.append((p["handle"], "bracket left in copy"))
        if bad_words.search(re.sub(r'<p class="disclaimer">.*', "", p["body"], flags=re.S)): problems.append((p["handle"], "banned word"))
        if re.search(r"\bofficial\b|\bmerchandise\b|\bendorsed\b|\bapproved\b", re.sub(r'<h3>Please note</h3>.*', "", p["body"], flags=re.S), re.I):
            problems.append((p["handle"], "official/endorsed wording outside disclaimer"))
        if bodies[p["body"]] > 1: problems.append((p["handle"], "duplicate description"))
        if len(p["title"]) > 150: problems.append((p["handle"], "title > 150"))
        if not p["image"].startswith("https://cdn.shopify.com/"): problems.append((p["handle"], "image not on Shopify CDN"))
        if p["handle"] in store_handles: problems.append((p["handle"], "handle exists in store"))
        for s in (p["sku"], p["sku"] + "-DIY"):
            if s.lower() in store_skus: problems.append((p["handle"], f"sku clash {s}"))
    hs = Counter(p["handle"] for p in products)
    problems += [(h, "duplicate handle") for h, c in hs.items() if c > 1]
    ss = Counter(p["sku"].lower() for p in products)
    problems += [(s, "duplicate sku") for s, c in ss.items() if c > 1]
    if problems:
        for x in problems[:50]:
            print("PROBLEM", x)
        sys.exit(f"{len(problems)} problems; nothing written")

    # ---- write ----------------------------------------------------------------------------------------------
    G = "mm-google-shopping"
    cols = ["Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published", "Status",
            "Option1 Name", "Option1 Value", "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Policy",
            "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price", "Variant Requires Shipping", "Variant Taxable",
            "Image Src", "Image Position", "Image Alt Text", "SEO Title", "SEO Description",
            f"Google Shopping / Custom Product (product.metafields.{G}.custom_product)",
            f"Google Shopping / Condition (product.metafields.{G}.condition)",
            f"Google Shopping / Google Product Category (product.metafields.{G}.google_product_category)",
            f"Google Shopping / Gender (product.metafields.{G}.gender)",
            f"Google Shopping / Age Group (product.metafields.{G}.age_group)",
            f"Google Shopping / Color (product.metafields.{G}.color)",
            f"Google Shopping / MPN (product.metafields.{G}.mpn)"]

    def lines(p):
        imgs = [(p["image"], p["alt"])] + EXTRA_IMAGES
        out = []
        first = {c: "" for c in cols}
        first.update({"Handle": p["handle"], "Title": p["title"], "Body (HTML)": p["body"], "Vendor": "Foxy Printing",
                      "Product Category": CATEGORY, "Type": "Celebrity Facemask", "Tags": ", ".join(p["tags"]), "Published": "FALSE",
                      "Status": "draft", "Option1 Name": "Style", "SEO Title": p["seo_title"], "SEO Description": p["meta"],
                      cols[25]: "TRUE", cols[26]: "new", cols[27]: CATEGORY, cols[28]: "unisex", cols[29]: p["age"],
                      cols[30]: "Multicolor", cols[31]: p["sku"]})
        variants = [("Ready to Wear", p["sku"], PRICE_RTW), ("DIY", p["sku"] + "-DIY", PRICE_DIY)]
        n = max(len(variants), len(imgs))
        for i in range(n):
            row = first if i == 0 else {c: "" for c in cols}
            row["Handle"] = p["handle"]
            if i < len(variants):
                v, s, pr = variants[i]
                row.update({"Option1 Value": v, "Variant SKU": s, "Variant Grams": "0", "Variant Inventory Tracker": "",
                            "Variant Inventory Policy": "continue", "Variant Fulfillment Service": "manual", "Variant Price": pr,
                            "Variant Requires Shipping": "TRUE", "Variant Taxable": "TRUE"})
            if i < len(imgs):
                row.update({"Image Src": imgs[i][0], "Image Position": str(i + 1), "Image Alt Text": imgs[i][1]})
            out.append([row[c] for c in cols])
        return out

    def write(path, ps):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for p in ps:
                w.writerows(lines(p))

    order = sorted(products, key=lambda p: p["handle"])
    test_keys = ["paullambert", "darthvader", "crowleysupernatural"]
    test = [p for k in test_keys for p in order if p["key"] == k]
    if len(test) < 3:
        test += [p for p in order if p not in test][: 3 - len(test)]
    write(f"{out}/00-TEST-3-new-masks.csv", test)
    rest = [p for p in order if p not in test]
    files = []
    for n, i in enumerate(range(0, len(rest), 1000)):
        path = f"{out}/{n + 1:02d}-new-masks.csv"
        write(path, rest[i:i + 1000])
        files.append((os.path.basename(path), len(rest[i:i + 1000])))
    with open(f"{out}/skipped.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "name", "category", "reason", "existing product (handle, status, title) / note"])
        for it, why, note in skipped:
            w.writerow([it["key"], it["name"], it["category"], why, note])
    with open(f"{out}/preview.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "handle", "title", "category", "show", "age_group", "sku", "tags", "seo_title", "meta", "image"])
        where = {p["handle"]: "00-TEST-3-new-masks.csv" for p in test}
        for n, i in enumerate(range(0, len(rest), 1000)):
            for p in rest[i:i + 1000]:
                where[p["handle"]] = f"{n + 1:02d}-new-masks.csv"
        for p in order:
            w.writerow([where[p["handle"]], p["handle"], p["title"], p["category"], p["show"], p["age"], p["sku"], ", ".join(p["tags"]),
                        p["seo_title"], p["meta"], p["image"]])
    json.dump({"products": len(products), "test": [p["handle"] for p in test], "files": files,
               "skipped": Counter(w for _, w, _ in skipped), "age": Counter(p["age"] for p in products),
               "characters": sum(p["is_char"] for p in products)}, open(f"{out}/build_summary.json", "w"), indent=1)
    print(json.dumps(json.load(open(f"{out}/build_summary.json")), indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
