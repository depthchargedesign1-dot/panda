"""Character-themed birthday cards: description rewrite (catalogue audit 9 Oct 2026, Fix 2).

Usage: python3 -I cards_copy.py EXPORT.jsonl OUT_DIR

Covers the old ACTIVE "Kids Cards", "Gaming Cards" and "Movie Cards" listings (2017-era HTML pasted from eBay).
Facts come only from plan/product-facts.md "Personalised cards": 350gsm silk art board, printed A4 and folded
to A5, printed inside and out if wanted, machine cut and folded, free white envelope, posted flat in a
board-backed envelope, Royal Mail 1st Class same day or next working day at busy times.
These listings have no personalisation box or live preview of their own, so the copy only says "add the name,
age and message when you order" (same wording as their current SEO meta).

Every design is themed on someone else's character, show, film or game, so every card gets the matching
disclaimer (CLAUDE.md templates) and needs the third-party-name tag (tag-ids.txt, added through the API).

Writes OUT_DIR/<family>-descriptions.csv (Handle, Body (HTML)), review.csv, problems.csv, tag-ids.txt, samples.html.
"""
import csv
import hashlib
import html
import json
import os
import re
import sys

FAMILIES = {"Kids Cards": "kids-cards", "Gaming Cards": "gaming-cards", "Movie Cards": "movie-cards"}
BOIL = [r"\(SA\d*\)", r"THEME INSPIRED Kids Adult Personalised Birthday Card", r"THEME INSPIRED Style PERSONALISED Kids Adult FUNNY Birthday Card",
        r"Style Theme Personalised Kidshows Birthday Card", r"Style Inspired Cartoon Birthday Card", r"Inspired Style Game Kids Inspired Birthday Card",
        r"Inspired Theme Personalised Kids Inspired Birthday Card", r"Movie Inspired Theme Personalised Kids Inspired Birthday Card",
        r"Theme Style Personalised Kids Inspired Movie Birthday Card", r"INSPIRED THEME Movie Birthday Card", r"^INSPIRED STYLE",
        r"^Personalised Kids Inspired", r"Birthday Card", r"\bBirthdary Card\b", r"\bPersonalised\b", r"\bKids Inspired\b", r"\bTHEME INSPIRED\b",
        r"\bInspired\b", r"\bStyle\b", r"\bTheme\b", r"\bFUNNY\b", r"\bKids Adult\b"]
BANNED = re.compile(r"\b(official|licensed|authentic|genuine|approved|endorsed|merchandise|signed|autographed|memorabilia|limited edition|"
                    r"the best|best quality|best price|cheapest)\b", re.I)
GENERIC = re.compile(r"^(elephant|cartoon character|unicorn|dinosaur|princess|pirate|mermaid|farm|down on the farm|football|tractor|robot|space|"
                     r"monster truck|monster trucks)( 3d)?$", re.I)


def h(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)


def pick(pool, key, slot):
    return pool[h(key + slot) % len(pool)]


def esc(s):
    return html.escape(s, quote=False)


def text(x):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(x or ""))).strip()


def theme_of(title):
    s = title
    for b in BOIL:
        s = re.sub(b, " ", s, flags=re.I)
    s = re.sub(r"\s+", " ", s).strip(" -–|,")
    design = None
    m = re.search(r"\bDesign (\d+)\b", s, re.I)
    if m:
        design, s = m.group(1), (s[:m.start()] + s[m.end():]).strip()
    s = re.sub(r"\s+BM\d?\b", "", s)
    s = re.sub(r"\s+(Movie|Game)$", "", s, flags=re.I)
    m = re.search(r"\s+(\d{1,2}[a-z]?)$", s)
    if m and not re.search(r"\b(19|20)\d\d$", s):
        design = design or m.group(1)
        s = s[:m.start()]
    s = re.sub(r"\s+(Movie|Game)$", "", s, flags=re.I).strip(" -–|,")
    words = []
    for w in s.split():
        if w.isupper() and len(w) > 3 and w not in ("GTA", "WWE", "WWF", "LEGO"):
            w = w.capitalize()
        words.append(w)
    s = " ".join(words)
    s = re.sub(r"\bLego\b", "LEGO", s)
    s = re.sub(r"\b(?=[ivx]{2,}\b)x{0,3}(?:ix|iv|v?i{0,3})\b", lambda m: m.group(0).upper(), s, flags=re.I)
    s = re.sub(r"\s+\b(Hd|HD|Wallpapers?|Vector)\b", "", s).strip()
    return s, design


def disclaimer(fam, theme):
    if fam == "Gaming Cards":
        body = (f"This is an unofficial, fan-made card produced by Foxy Printing, inspired by {theme}. It is not made, endorsed or licensed by "
                "the game's publisher or any console maker. All trademarks, characters and game titles belong to their respective owners and are "
                "used only to identify the theme.")
    else:
        body = (f"This is an unofficial design inspired by {theme}. It is not official merchandise and is not endorsed by, sponsored by, or connected with "
                f"{theme}, its makers or rights holders, or any of their licensees. All names, characters and trademarks belong to their respective owners.")
        if fam == "Movie Cards":
            body += (" Any actors or public figures named or pictured have not endorsed, sponsored or approved this product, and Foxy Printing "
                     "has no connection with them. Their names are used only to describe the design.")
    return "\n<h3>Please note</h3>\n<p class=\"disclaimer\">" + esc(body) + "</p>"


WHO = {"Kids Cards": "little fan", "Gaming Cards": "gamer", "Movie Cards": "film fan"}


def build(p):
    fam, key = p["productType"], p["handle"]
    theme, design = theme_of(p["title"])
    t = esc(theme)
    kw = f"personalised {t} birthday card"
    who = WHO[fam]
    dz = f" (design {design})" if design else ""
    opener = pick([
        f"Make their day with a {kw}, printed on thick card in our North Yorkshire workshop and posted 1st Class.",
        f"Our {kw} is a fun way to wish a {who} happy birthday, with their name and age added to a {t} inspired design.",
        f"Looking for a card for a {t} fan? This {kw} is made to order with the name, age and message you choose.",
    ], key, "o")
    h2 = pick([f"Personalised {t} birthday card", f"{t} birthday card with name and age", f"Personalised {t} inspired birthday card"], key, "h")
    what = pick([
        f"The front shows a {t} inspired design{dz}. Add the birthday name, age and your own front message when you order, and we can print a message inside too.",
        f"You get a {t} inspired card{dz}, printed with the name and age you give us. Want a message inside? Add it when you order and we'll print that as well.",
        f"It's a {t} inspired design{dz}, personalised with the name and age of the birthday {who}. We can print inside and out, so add your own inside message when you order.",
    ], key, "w")
    check = " We print exactly what you enter, so please double-check names and spelling."
    bullets_pool = [
        "Printed on 350gsm silk art board, much thicker than the usual 240gsm card",
        "Printed A4 and folded to A5, then machine cut and folded for a crisp finish",
        "Personalised with their name, age and your own message",
        "Printed inside and out if you want a message inside",
        "Comes with a free white envelope",
        "Posted flat in a board-backed envelope so it arrives uncreased",
    ]
    order = sorted(range(len(bullets_pool)), key=lambda i: h(key + "b" + str(i)))[:5]
    bullets = "\n".join(f"<li>{bullets_pool[i]}</li>" for i in sorted(order))
    closer = pick([
        f"Can't find the character you're after? We can design a custom birthday card: call 01439 771468.",
        f"Pair the {kw} with a personalised mug for a birthday gift that's sorted in one go. Custom cards on request: call 01439 771468.",
        f"Buying for a {who}? Add a personalised mug or poster for a matching gift. Custom card designs on request: call 01439 771468.",
    ], key, "c")
    body = (f"<p>{opener}</p>\n<h2>{h2}</h2>\n<p>{what}{check}</p>\n"
            f"<h3>Why you'll love it</h3>\n<ul>\n{bullets}\n</ul>\n"
            "<h3>Size &amp; details</h3>\n<ul>\n<li>Size: printed A4, folded to A5</li>\n<li>Card: 350gsm silk art board</li>\n"
            "<li>Finish: machine cut and folded</li>\n<li>Includes: free white envelope</li>\n"
            "<li>Personalisation: name, age, front message and inside message</li>\n</ul>\n"
            "<h3>Delivery</h3>\n<p>Sent Royal Mail 1st Class, dispatched the same day, or the next working day at busy times. "
            "It's posted flat in a board-backed envelope.</p>\n"
            f"<p>{closer}</p>")
    named = not GENERIC.match(theme)
    if named:
        body += disclaimer(fam, theme)
    if len(text(body).split()) > 350:
        body = body.replace(f"<p>{closer}</p>", "<p>Custom card designs on request: call 01439 771468.</p>")
    return body, theme, named


def check(body, theme, named):
    pr = []
    if body.count("<h2") != 1:
        pr.append("h2")
    if re.search(r"style=|<span|<h1|<table|<br|<img|\[|\]", body):
        pr.append("html")
    nd = re.sub(r'<p class="disclaimer">.*?</p>', "", body, flags=re.S).replace(esc(theme), "")
    m = BANNED.search(text(nd))
    if m:
        pr.append("banned:" + m.group(0))
    w = len(text(body).split())
    if not 180 <= w <= 350:
        pr.append(f"words {w}")
    if not theme or len(theme) < 2 or not re.search(r"[A-Za-z]", theme):
        pr.append("no theme")
    if named and not body.rstrip().endswith("</p>"):
        pr.append("disclaimer")
    return pr


def main(src, out):
    os.makedirs(out, exist_ok=True)
    P = {}
    for line in open(src, encoding="utf-8"):
        o = json.loads(line)
        if "__parentId" in o:
            continue
        P[o["id"]] = o
    files = {f: [] for f in FAMILIES}
    review, probs, tag_ids, seen = [], [], [], {}
    for p in P.values():
        if p["productType"] not in FAMILIES or p["status"] != "ACTIVE":
            continue
        if "<h2" in (p["descriptionHtml"] or "") and not re.search(r"style=|<span", p["descriptionHtml"] or ""):
            continue  # already rewritten
        body, theme, named = build(p)
        pr = check(body, theme, named)
        if body in seen:
            pr.append("duplicate of " + seen[body])
        seen[body] = p["handle"]
        if pr:
            probs.append([p["handle"], p["title"], ";".join(pr)])
            continue
        files[p["productType"]].append([p["handle"], body])
        review.append([p["handle"], p["title"], p["productType"], theme, "yes" if named else "no", len(text(body).split())])
        if named and "third-party-name" not in p["tags"]:
            tag_ids.append(p["id"])
    for fam, rows in files.items():
        with open(os.path.join(out, f"{FAMILIES[fam]}-descriptions.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Handle", "Body (HTML)"])
            w.writerows(rows)
    with open(os.path.join(out, "review.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Handle", "Title", "Family", "Theme name used", "Disclaimer", "Words"])
        w.writerows(review)
    with open(os.path.join(out, "problems.csv"), "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([["Handle", "Title", "Problem"]] + probs)
    open(os.path.join(out, "tag-ids.txt"), "w").write("\n".join(tag_ids) + "\n")
    with open(os.path.join(out, "samples.html"), "w", encoding="utf-8") as f:
        f.write("<!doctype html><meta charset=utf-8><title>Card samples</title><style>body{font-family:sans-serif;max-width:820px;margin:auto;padding:16px}"
                "section{border-bottom:1px solid #ccc;padding:12px 0}</style><h1>Character birthday card samples</h1>")
        for fam, rows in files.items():
            for hd, body in rows[:: max(1, len(rows) // 3)][:3]:
                f.write(f"<section><p><b>{fam}</b> <code>{hd}</code></p>{body}</section>")
    print({k: len(v) for k, v in files.items()}, len(probs), "problems,", len(tag_ids), "need tag")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
