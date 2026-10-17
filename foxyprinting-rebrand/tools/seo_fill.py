"""Fill missing SEO titles / meta descriptions for ACTIVE products (catalogue audit 9 Oct 2026, Fix 3).

Usage: python3 -I seo_fill.py EXPORT.jsonl OUT_DIR [SKIP_IDS.txt]

EXPORT.jsonl is a bulkOperationRunQuery export (products with seo, productType, variants as child lines).
Writes OUT_DIR/seo-fill-NN.csv (Handle, SEO Title, SEO Description), OUT_DIR/skipped.csv and samples.

Rules (CLAUDE.md): SEO title <= 60 chars, meta 140-155 chars, UK English, no "official/licensed/signed..."
claims, trademarks out of the SEO title where we can (lead with the generic description), no invented specs.
An existing, valid value is kept as it is; only missing or broken values are written.
"""
import csv
import hashlib
import itertools
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from retro_poster_copy import parse_game, seo_title as game_seo_title  # noqa: E402

SUFFIX = " | Foxy Printing"
BANNED = re.compile(r"\b(official|licensed|authentic|genuine|approved|endorsed|memorabilia|autographed|hand-signed|limited edition)\b", re.I)


def h(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)


def fit_title(core, alts=()):
    for c in (core,) + tuple(alts):
        if len(c + SUFFIX) <= 60:
            return c + SUFFIX
    for c in (core,) + tuple(alts):
        if len(c) <= 60:
            return c
    words = core.split()
    while words and len(" ".join(words)) > 60:
        words.pop()
    return " ".join(words).rstrip(" -–,&:")


def fit_meta(stems, pads, key):
    order = sorted(range(len(stems)), key=lambda i: h(key + str(i)))
    for i in order:
        base = stems[i]
        if len(base) > 155:
            continue
        for r in range(0, 4):
            for combo in sorted(itertools.permutations(pads, r), key=lambda c: h(key + "".join(c))):
                s = base + "".join(combo)
                if 140 <= len(s) <= 155:
                    return s
    return None


def valid_meta(s):
    return bool(s) and 140 <= len(s) <= 155 and not re.search(r"\b(for|a|an|the|and|with|to|of)\.$", s) and not BANNED.search(s)


def valid_title(s):
    return bool(s) and len(s) <= 60 and not BANNED.search(s)


def tidy(t):
    t = re.sub(r"\s+", " ", t.replace("_", " ")).strip(" -–|")
    t = re.sub(r"\bWorlds\b", "World's", t)
    return t


# ---------- families ----------
GAME_META = [
    "Fan-made {g} retro gaming poster, printed to order in our North Yorkshire workshop.",
    "Relive the classic {g} with this fan-made retro gaming poster, printed to order in North Yorkshire.",
    "Add {g} to your gaming wall with this fan-made retro poster, printed to order in North Yorkshire.",
    "A {g} retro gaming poster for game rooms, man caves and collectors, printed to order in North Yorkshire.",
    "{g} retro gaming poster, a fan-made print made to order in our North Yorkshire workshop.",
]
GAME_PADS = [" Sizes {sz}.", " A great gift for any gamer.", " Ideal for a game room.", " Order today."]


def sizes_from(p):
    got = []
    for v in p["variants"]:
        m = re.match(r"(A[0-6])\b", v.get("title") or "")
        if m and m.group(1) not in got:
            got.append(m.group(1))
    if len(got) >= 2:
        order = sorted(got, key=lambda a: -int(a[1]))
        return f"{order[0]} to {order[-1]}"
    return None


def game_poster(p):
    g = parse_game(p["title"])
    if not g:
        return None, None, "could not read the game name"
    title = game_seo_title(g)
    sz = sizes_from(p)
    pads = [x.format(sz=sz) for x in GAME_PADS if sz or "{sz}" not in x]
    art = "An" if re.match(r"[AEIOU]", g) else "A"
    meta = fit_meta([s.format(g=g).replace("A " + g, art + " " + g) for s in GAME_META], pads, p["handle"])
    return title, meta, None


def music_poster(p):
    m = re.match(r"(.+?)\s*(\d+)?\s*[–-]\s*Printed Signature", p["title"])
    if not m:
        return None, None, "could not read the artist"
    artist, n = m.group(1).strip(), m.group(2)
    core = f"{artist} Printed Signature Poster" + (f" {n}" if n else "")
    title = fit_title(core, (f"{artist} Music Poster" + (f" {n}" if n else ""),))
    stems = [f"Fan-made {artist} music poster with a printed signature-style design. Printed to order in North Yorkshire.",
             f"{artist} music star print with the signature printed as part of the design. A fan-made poster, printed to order in North Yorkshire.",
             f"Put {artist} on the wall with this fan-made music poster. The signature is part of the print. Made to order in North Yorkshire."]
    meta = fit_meta(stems, [" A great gift for any fan.", " Order today.", " Ideal for a bedroom wall."], p["handle"])
    return title, meta, None


def santa_sack(p):
    t = re.sub(r"^Personalised\s+|\s*Custom Name$", "", p["title"]).strip()
    t = re.sub(r"^Official\s+", "", t)
    hessian = "Hessian" in t
    m = re.match(r"(.+?)\s+(?:Small\s+)?(?:Hessian\s+)?Santa Sack(?:\s+XL EXTRA LARGE)?$", t)
    design = (m.group(1) if m else "").strip()
    if design in ("Small", "Official"):
        design = ""
    size = "small " if re.search(r"\bSmall\b", t) else ("extra large " if "EXTRA LARGE" in t else "")
    kind = ("hessian " if hessian else "") + "Santa sack"
    core = (f"Personalised {design} XL Santa Sack" if "EXTRA LARGE" in t else f"Personalised {design} {kind.title()}") if design \
        else f"Personalised {size.title()}{kind.title()}"
    title = fit_title(re.sub(r"\s+", " ", core), (f"{design} Santa Sack with Name",) if design else ())
    d = f"the {design} design" if design else "a festive design"
    stems = [f"Personalised {size}{kind} with {d} and your child's name, printed in our North Yorkshire workshop.",
             f"Make Christmas Eve magic with a personalised {size}{kind}: {d}, printed with any name in North Yorkshire."]
    meta = fit_meta(stems, [" Order in time for Christmas.", " A lovely family keepsake.", " Order today."], p["handle"])
    return title, meta, None


def gift_tin(p):
    name = re.sub(r"\s*Metal Tin$", "", p["title"]).strip()
    title = fit_title(f"{name} Printed Gift Tin", (f"{name} Gift Tin", f"{name} Tin"))
    meta = None
    if not valid_meta((p.get("seo") or {}).get("description")):
        stems = [f"{name} printed gift tin: a 10cm x 4cm metal tin with a removable lid and a UV DTF print.",
                 f"{name} metal gift tin, 10cm x 4cm with a removable lid, printed in-house with UV DTF."]
        meta = fit_meta(stems, [" Great for gifts and keepsakes.", " Printed in North Yorkshire.", " Order today."], p["handle"])
    return title, meta, None


def towel(p):
    t = tidy(p["title"])
    m = re.match(r"(.+?)\s+Personalised Rugby Bath Towel", t)
    team = m.group(1) if m else t
    return fit_title(f"Personalised Rugby Bath Towel – {team}", (f"Rugby Bath Towel – {team}",)), None, None


def generic(p):
    t = tidy(p["title"])
    if p["productType"] in ("coach mugs",):
        m = re.search(r"IM A (.+?) Coach", t, re.I)
        if m:
            return fit_title(f"Funny {m.group(1).title()} Coach Mug"), fit_meta(
                [f"Funny {m.group(1).lower()} coach mug: 'to save time, let's just assume I'm always right'. Printed in our North Yorkshire workshop."],
                [" A great gift.", " Order today.", " Ideal for the office."], p["handle"]), None
    if re.search(r"Librarian Mug", t):
        return fit_title("World's Best Public Librarian Mug"), fit_meta(
            ["World's best public librarian mug, a funny thank-you gift for a librarian. Printed in our North Yorkshire workshop."],
            [" Order today.", " Ideal for the office.", " A great leaving gift."], p["handle"]), None
    m = re.match(r"(.+?) Children's Birthday Banner (Thick|Thin)\s*(\d*)", t)
    if m:
        theme, kind, n = m.group(1), m.group(2), m.group(3)
        return fit_title(f"Children's Birthday Banner – {theme} {kind}{(' ' + n) if n else ''}"), None, None
    m = re.match(r"(.+?) Football Team Face Covering Mask", t)
    if m:
        return fit_title(f"Football Fan Face Covering – {m.group(1)}"), None, None
    return fit_title(t), None, "generic title only; meta needs a family fact sheet" if not valid_meta((p.get("seo") or {}).get("description")) else None


SKIP_TYPES = {"OPTIONS_HIDDEN_PRODUCT": "hidden options helper product (not for sale on its own)"}
SKIP_TITLE = re.compile(r"\b(dyke|fag|queer|fucktard)\b|UPGRADED to|^Test Party|^Copy Of |^Bold Test$", re.I)


def build(p):
    pt = p["productType"] or ""
    if pt in SKIP_TYPES:
        return None, None, SKIP_TYPES[pt]
    if SKIP_TITLE.search(p["title"]):
        return None, None, "owner decision needed (test/helper/offensive listing)"
    if pt == "Signed Music Posters":
        return music_poster(p)
    if "poster" in pt.lower():
        return game_poster(p)
    if pt == "Holiday Stockings":
        return santa_sack(p)
    if pt == "Printed Gift Tin":
        return gift_tin(p)
    if pt == "Towel":
        return towel(p)
    return generic(p)


def load(path):
    P = {}
    for line in open(path):
        o = json.loads(line)
        if "__parentId" in o:
            if o["__parentId"] in P:
                P[o["__parentId"]]["variants"].append(o)
        else:
            o["variants"] = []
            P[o["id"]] = o
    return P


def main():
    src, out = sys.argv[1], sys.argv[2]
    skip_ids = set(open(sys.argv[3]).read().split()) if len(sys.argv) > 3 else set()
    os.makedirs(out, exist_ok=True)
    P = load(src)
    rows, skipped, seen_t = [], [], {}
    for p in P.values():
        if p["status"] != "ACTIVE" or p["id"] in skip_ids:
            continue
        seo = p.get("seo") or {}
        if valid_title(seo.get("title")) and valid_meta(seo.get("description")):
            continue
        if seo.get("title") and seo.get("description"):
            continue  # both present: not part of the "missing" set
        t, m, why = build(p)
        t = seo.get("title") if valid_title(seo.get("title")) else t
        m = seo.get("description") if valid_meta(seo.get("description")) and not m else m
        if not t and not m:
            skipped.append([p["handle"], p["title"], p["productType"], why or "no rule"])
            continue
        problems = []
        if t and (len(t) > 60 or BANNED.search(t)):
            problems.append("title")
        if m and (not 140 <= len(m) <= 155 or BANNED.search(m)):
            problems.append("meta")
        if problems:
            skipped.append([p["handle"], p["title"], p["productType"], "failed checks: " + ",".join(problems)])
            continue
        if t:
            seen_t.setdefault(t, []).append(p["handle"])
        rows.append([p["handle"], t or "", m or "", why or ""])
    # de-duplicate identical SEO titles: the 2nd, 3rd... copy becomes "... Design 2", "... Design 3"
    taken = {r[1] for r in rows}
    for t, hs in seen_t.items():
        if len(hs) < 2:
            continue
        n = 1
        for r in rows:
            if r[1] == t and r[0] != hs[0]:
                core = t.replace(SUFFIX, "")
                while True:
                    n += 1
                    new = fit_title(f"{core} Design {n}")
                    if len(new) > 60 or not new.endswith(f"Design {n}") and not new.endswith(SUFFIX):
                        new = f"{core[:60 - len(f' Design {n}')].rstrip(' -–,&:')} Design {n}"
                    if new not in taken:
                        break
                r[1] = new
                taken.add(new)
    CH = 5000
    for i in range(0, len(rows), CH):
        with open(os.path.join(out, f"seo-fill-{i // CH + 1:02d}.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Handle", "SEO Title", "SEO Description"])
            for r in rows[i:i + CH]:
                w.writerow(r[:3])
    with open(os.path.join(out, "skipped.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Handle", "Title", "Product type", "Why"])
        w.writerows(skipped)
    with open(os.path.join(out, "notes.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Handle", "SEO Title", "SEO Description", "Note"])
        w.writerows([r for r in rows if r[3]])
    print(len(rows), "rows,", len(skipped), "skipped")


if __name__ == "__main__":
    main()
