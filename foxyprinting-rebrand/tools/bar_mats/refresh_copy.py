"""Bar-mat copy, SEO and Google data refresh (owner, 8 Oct 2026):
  "Fix the bar mat height it is 250mm not 330mm my mistage"
  "They are all rubber backed and sublimation printed they can be put in a dishwasher"
  "Can you give all the bar mats new better seo descriptions and check all metatags and google data"

Input : before.json  (live snapshot of every product_type 'Bar Mat' product, 142 on 8 Oct 2026)
Output: OUT/plan.json (per product: new description, SEO, alts, tags, metafields, option renames)
        OUT/m_*.graphql (aliased mutation batches)
Usage : python3 refresh_copy.py before.json OUT
Facts : plan/product-facts.md "Home bar" sheet only. Rubber thickness is ASK and never stated.
"""
import hashlib, html, itertools, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import data as D            # the 54 designs created on 8 Oct 2026
import refresh_data as R    # M-series, football club and VE Day designs

ROOT = Path(__file__).resolve().parents[2]
SMALL, LARGE = "Small 440mm x 250mm", "Large 880mm x 250mm"
CAT = "Home & Garden > Kitchen & Dining > Barware"
PHONE = "01439 771468"
q = json.dumps


def pick(pool, key, salt=""):
    h = int(hashlib.md5((key + salt).encode()).hexdigest(), 16)
    return pool[h % len(pool)]


THE_LED = ("my ", "it’s", "life ", "enjoy ", "well ", "take ", "five ", "satur", "beer o’clock", "bar rules", "old fashioned", "skull")


def art(pk):
    if pk.startswith(THE_LED):
        return "the"
    return "an" if pk[0] in "aeiou8" else "a"


def cap(s):
    return s[0].upper() + s[1:]


def words(htm):
    htm = htm.split("<h3>Please note</h3>")[0]
    return len(re.sub(r"<[^>]+>", " ", htm).split())


# ------------------------------------------------------------------ shared pools (each bullet names the design)
RUBBER = [
    "Rubber-backed and non-slip, so the {d} mat sits flat and stays put while the drinks are flowing",
    "A non-slip rubber back keeps the {d} runner from sliding about when glasses are put down in a hurry",
    "Rubber backing grips the bar top, so your {d} mat won’t creep along the counter",
    "The rubber back holds the {d} design flat on wood, granite or a laminate worktop",
]
SUBLI = [
    "Dye-sublimation printed, so the {c} colours are part of the surface and won’t peel or crack",
    "Printed by dye-sublimation in our own workshop: the ink becomes part of the top, so it won’t peel, crack or rub off",
    "Sublimation printing keeps every detail sharp and the {c} colours won’t peel or crack with use",
    "Full-colour dye-sublimation print that won’t peel or crack, even after plenty of spills",
]
DISH = [
    "Dishwasher safe, so sticky spills and beer rings wash straight off",
    "Pop it in the dishwasher after a party and it comes out ready for the next one",
    "Dishwasher safe – no scrubbing after a long night",
    "Goes in the dishwasher when it needs a proper clean",
]
SIZEB = [
    "Two sizes: the 440mm small mat fits a shelf or drinks trolley, the 880mm runner covers a full bar top",
    "Choose the small 440mm mat for a kitchen counter or the 880mm runner for a long bar",
    "Small (440mm) for a drinks trolley, large (880mm) for a proper run of pints",
    "Order the large 880mm runner for the bar and a small 440mm one for the side",
]
OPEN = [
    "This {pk} is the easiest way to make a home bar feel like your own local.",
    "Give your bar a proper pub finish with this {pk}.",
    "Our {pk} brings real pub character to a kitchen island, garden bar or man cave.",
    "Looking for {a} {pk}? This one is printed to order in our North Yorkshire workshop.",
    "Every good home bar needs a mat to catch the drips, and this {pk} does it in style.",
]
H2 = [
    "{A} {pk} made for your home bar",
    "Your {pk}, printed to order",
    "Why this {pk} makes a great gift",
    "The {pk} for home bars and man caves",
]
DELIV = [
    "Every bar mat is printed to order in our North Yorkshire workshop and posted out once it’s made. Postage options and costs are shown at checkout.",
    "We print your bar mat to order in North Yorkshire and send it on its way once it’s made – you’ll see the postage options and costs at checkout.",
    "Made to order in our North Yorkshire workshop, then posted out to you. Postage choices and prices are at checkout.",
]
ASK = [
    "Questions about your {pk}? Give us a ring on {ph}.",
    "Not sure which size to choose for your {pk}? Ring us on {ph} and we’ll help.",
    "Any questions about the {pk}, just call us on {ph}.",
]
PK_FIX = {"personalised established bar mat black": "personalised black established bar mat"}
SECONDARY = ["home bar gift", "man cave gift", "bar runner", "pub bar mat", "garden bar accessories", "personalised bar mat"]


# ------------------------------------------------------------------ disclaimers (CLAUDE.md templates)
def disc_football(club_full, league):
    return (f"This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, "
            f"or affiliated with {club_full}, {league}, or any club, league or player. Club and player names are used only to "
            f"describe the design and who it’s for. All trademarks belong to their respective owners.")


def disc_props():
    return ("This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by Ballantine’s. "
            "Ballantine’s is a trademark of its owner; the bottles in the photos are props only and are not included.")


def disc_game(kind, name, owner, props):
    if kind == "film":
        s = (f"This is an unofficial design inspired by {name}. It is not official merchandise and is not endorsed by, sponsored by, "
             f"or connected with {name} or {owner}, or any of their licensees. All names, characters and trademarks belong to their respective owners.")
    else:
        s = (f"This is an unofficial, fan-made print produced by Foxy Printing. It is not made, endorsed or licensed by {owner}. "
             f"All trademarks, character and game names belong to their respective owners and are used only to identify the theme.")
    if props:
        s += " It is also not made, endorsed or approved by Ballantine’s, a trademark of its owner; the bottles in the photos are props only and are not included."
    return s


def disc_ve():
    return ("This is an unofficial commemorative design made by Foxy Printing. It is not made, endorsed or approved by the UK Government "
            "or the official VE Day 80 programme. Any commemorative emblem is used only to describe the design theme.")


# ------------------------------------------------------------------ description builder
def describe(x):
    k = x["id"]
    pk = x["pk"]
    d = x["d"]
    c = x["cw"]
    op = x.get("opening") or pick(OPEN, k).format(pk=pk, a=art(pk))
    parts = [f"<p>{op} {x['look']} {x['hook']}</p>"]
    parts.append(f"<h2>{cap(x.get('h2') or pick(H2, k, 'h2').format(pk=pk, A=cap(art(pk))))}</h2>")
    parts.append(f"<p>{x['pers']}</p>")
    bl = [x["b1"],
          pick(RUBBER, k, "r").format(d=d.replace("&", "and")),
          pick(SUBLI, k, "s").format(c=c),
          pick(DISH, k, "w"),
          pick(SIZEB, k, "z")]
    if x.get("b6"):
        bl.append(x["b6"])
    parts.append("<h3>Why you’ll love it</h3>\n<ul>\n" + "\n".join(f"<li>{b}</li>" for b in bl) + "\n</ul>")
    det = [f"Small: 440mm x 250mm", f"Large: 880mm x 250mm", "Rubber-backed, non-slip base",
           "Dye-sublimation printed in-house in North Yorkshire, UK", "Dishwasher safe", x["detail"]]
    parts.append("<h3>Size &amp; details</h3>\n<ul>\n" + "\n".join(f"<li>{b}</li>" for b in det) + "\n</ul>")
    parts.append(f"<h3>Delivery</h3>\n<p>{pick(DELIV, k, 'dl')}</p>")
    parts.append(f"<p>{x['close']} {pick(ASK, k, 'a').format(pk=pk, ph=PHONE)}</p>")
    if x.get("disc"):
        parts.append(f"<h3>Please note</h3>\n<p class=\"disclaimer\">{x['disc']}</p>")
    return "\n".join(parts)


def fit_meta(cands):
    """first combination of sentences 140-155 chars"""
    for combo in cands:
        s = " ".join(combo)
        if 140 <= len(s) <= 155:
            return s
    raise ValueError("no meta fits: " + " | ".join(" ".join(c) + f" ({len(' '.join(c))})" for c in cands))


def metas(lead, extras):
    """lead sentence + any 1-2 of the extras"""
    out = []
    for n in (1, 2):
        for comb in itertools.permutations(extras, n):
            out.append((lead,) + comb)
    return out


def seo_title(kw):
    t = f"{kw} | Foxy Printing"
    if len(t) > 60:
        t = f"{kw.replace('Personalised ', '')} | Foxy Printing"
    if len(t) > 60:
        raise ValueError(t)
    return t


EXTRA_P = ["Rubber-backed, dishwasher safe and sublimation printed in North Yorkshire.",
           "Rubber-backed and dishwasher safe, in 440mm or 880mm.",
           "Printed to order in North Yorkshire.",
           "Non-slip rubber back, dishwasher safe.",
           "Order yours today.",
           "Small 440mm or large 880mm."]
EXTRA_PERS = ["Add your own wording and order today."] + EXTRA_P


# ------------------------------------------------------------------ per-family records
def club_record(n, name):
    full, league, colours, gcol, region, seo, hook, close = R.CLUBS[name]
    fan = name.replace("St. Johnstone FC", "St Johnstone").replace("St. Mirren", "St Mirren").replace("Man United", "Manchester United").replace("Man City", "Manchester City").replace("Leeds", "Leeds United").replace("Leicester", "Leicester City").replace("Wolves", "Wolves").replace("Brighton and Hove Albion", "Brighton & Hove Albion")
    pk = f"personalised football bar mat for {fan} fans"
    sec = pick(["football bar runner", "man cave gift", "home bar gift"], n["id"], "sec")
    return dict(
        pk=pk, d=f"{colours}", cw=colours, colour=gcol,
        opening=f"Our {pk} gives a home bar, garage or garden bar a proper {region} match-day feel.",
        look=f"It’s printed in {colours} with WELCOME TO at the top and your own wording in large capitals across the middle.",
        hook=hook,
        h2=f"A {pk}, with your own wording",
        pers=(f"Type your wording in the custom text box on this page – a bar name, a nickname or the family surname – and we print it in place of YOUR TEXT. "
              f"We print exactly what you type, so check the spelling first. It makes a great {sec} for match days and birthdays."),
        b1=f"Printed in {colours} from end to end, so it looks right at home next to the scarf and the signed shirt",
        detail="Personalised with your own wording",
        close=close,
        disc=disc_football(full, league),
        seo=seo,
        meta=metas(f"A personalised football bar mat in {colours} for {region} fans, with your bar name across the middle.",
                   EXTRA_PERS),
        tags=["third-party-name", "bar runner", "home bar", "Personalised Bar Mat"],
        alt_d=f"{colours} design",
    )


def m_record(n, num):
    pk, seo, look, hook, close, gcol, example = R.M[num]
    if not n["media"]["nodes"] and num == 49:   # image-less duplicate of M49
        pk, seo = "pink satur-yay bar runner", "Pink Satur-Yay Cocktail Bar Runner"
    props = bool(n["media"]["nodes"]) and num not in R.M_PROP_BOTTLES_EXCEPT
    game = R.M_GAME.get(num)
    if game:
        disc = disc_game(*game, props)
    elif props:
        disc = disc_props()
    else:
        disc = None
    dname = re.sub(r"^.*Runner (.*?) Design M\d+$", r"\1", n["title"]).strip()
    if example and not example.startswith("a "):
        pers = (f"The name in the photo (‘{example}’) is only an example. Type your own bar or pub name in the personalisation box on this page "
                f"and we print it in the same style" + (", with your year on the EST. line" if "EST" in look else "") +
                f". Want any of the other wording changed? Ring us on {PHONE} before you order and we’ll talk it through.")
    elif example:
        pers = (f"The pub name in the photo is only an example. Type your own bar or pub name in the personalisation box on this page and we print it "
                f"in the same retro style. Please check the spelling before you order, as we print exactly what you type.")
    else:
        pers = (f"This design is printed as shown, so you can simply choose your size. Fancy a name added or the wording tweaked? Use the "
                f"personalisation box on this page, or ring us on {PHONE} before you order and we’ll talk it through.")
    cw = gcol.lower().replace("multicolor", "bright").replace("light blue", "sky blue")
    return dict(
        pk=pk, d=dname.lower(), cw=cw, colour=gcol, look=look, hook=hook, pers=pers,
        b1=pick(["The {n} artwork is laid out to fill the whole mat, with no plain borders",
                 "Every part of the {n} design is printed edge to edge in full colour",
                 "The {n} layout works on both sizes, so the small mat and the long runner match",
                 "Our {n} design is one of the most popular in the range for home pubs"], n["id"], "b1").format(n=dname),
        detail="Personalised with your wording" if example else "Printed as shown (wording changes on request)",
        close=close, disc=disc, seo=seo,
        meta=metas(f"Make your home bar your own local with {art(pk)} {pk}.", (EXTRA_PERS if example else EXTRA_P))
             + metas(f"{cap(art(pk))} {pk} for your home bar, pub shed or man cave.", (EXTRA_PERS if example else EXTRA_P)),
        tags=(["third-party-name"] if disc else []) + ["bar runner", "home bar"],
        alt_d=f"{dname} design",
    )


def ve_record(n, num):
    style, gcol, look, emblem = R.VE[num]
    pk = "VE Day 80th anniversary bar mat"
    return dict(
        pk=pk, d=style, cw=style.split(" Union")[0].replace("lettering", "").strip(), colour=gcol,
        opening=f"This {pk} marks 80 years since Victory in Europe, in a {style} design.",
        look=look, hook="It makes a proud keepsake for a family with wartime stories, a Legion club bar or a pub that hosted the street party.",
        h2=f"A {pk} to remember 8 May",
        pers="This special edition is printed exactly as shown, so there’s nothing to fill in – just choose your size.",
        b1=f"Design {num} of five: {style}, with the dates 1945 and 2025",
        detail="Printed as shown – a special edition design",
        close=f"Pair it with a set of pint glasses for a remembrance gathering or a Legion club night.",
        disc=disc_ve() if emblem else None,
        seo=f"VE Day 80th Anniversary Bar Mat – Design {num}",
        meta=metas(f"A VE Day 80th anniversary bar mat in a {style} design, marking 80 years since 8 May 1945.", EXTRA_P),
        tags=(["third-party-name"] if emblem else []) + ["Bar Mat", "bar runner", "home bar"],
        alt_d=f"{style} design {num}",
    )


def new_record(n, p):
    """one of the 54 created on 8 Oct (tools/bar_mats/data.py)"""
    g = p["group"]
    pk = PK_FIX.get(p["primary"], p["primary"])
    design = p["design"]
    pers_flag = p["personalised"]
    fields = p.get("fields") or []
    cw = p["colour"].lower().replace("multicolor", "bright").replace("/", " and ")
    if pers_flag:
        flist = ", ".join(f"‘{f}’" for f in fields)
        how = p.get("how") or "Your wording is set in the same style as the design shown."
        if g == "GB":
            how = ("Upload your club badge and it’s printed in the circles at both ends of the mat. Type the club or team name for the big middle line, "
                   "and if you like, change the ‘Welcome to’ line and add the year the club was formed. Leave the optional boxes blank and we keep the design as shown. "
                   "Please only upload badges your club has the right to use.")
        intro = "" if g == "GB" else f"Fill in the personalisation boxes on this page ({flist}). "
        pers = (f"{intro}{how} As you type, the live preview shows your details beside the design, "
                f"so you can check names and spelling before you order – we print exactly what you enter.")
    else:
        pers = (f"This one is printed exactly as shown, so there’s nothing to fill in – just pick your size. Want your own name or wording added? "
                f"Give us a ring on {PHONE} and we’ll talk you through it.")
    hook = p.get("hook") or {
        "BR": "It’s a gift that makes a home bar feel finished, and it’s printed with their own name.",
        "AN": ("A nice finishing touch for a home bar, a summer house bar or a pub-style kitchen."
               if pers_flag else "No fuss, nothing to fill in – a quick, fun gift for anyone with a home bar."),
    }.get(g, "A fun finishing touch for any home bar, garden bar or man cave.")
    look = p.get("look") or p.get("colour_note")
    b1 = p.get("b1") or p.get("colour_note") or {
        "BR": f"The {design} artwork is one of our own designs, laid out to run the full length of the mat",
        "AN": f"The {design} artwork runs edge to edge, with no plain borders",
    }[g]
    b1 = b1.rstrip(".")
    close = p.get("close") or {
        "BR": f"Pair it with a set of personalised pint glasses and the bar is ready for guests.",
        "AN": f"Add a personalised bar sign and the whole corner matches.",
    }[g]
    disc = None
    if p.get("brand"):
        disc = (f"This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {p['brand']}. "
                f"{p['brand']} is a trademark of its owner and is used only to describe the design theme.")
    seo_kw = p.get("seo_title", "") or ""
    seo_kw = seo_kw.replace(" | Foxy Printing", "") or " ".join(cap(w) if w not in ("and", "with", "in") else w for w in pk.split())
    seo_kw = seo_kw.replace("O’clock", "O’Clock")
    lead = (f"{cap(art(pk))} {pk} for home bars, garden bars and man caves." if not pers_flag
            else f"{cap(art(pk))} {pk}, printed with your own wording.")
    return dict(
        pk=pk, d=design.lower(), cw=cw, colour=p["colour"], look=look, hook=hook, pers=pers, b1=b1,
        detail="Personalised with your details" if pers_flag else "Printed as shown",
        close=close, disc=disc, seo=seo_kw,
        meta=metas(lead, EXTRA_PERS if pers_flag else EXTRA_P) + metas(f"Our {pk} is rubber-backed, dishwasher safe and dye-sublimation printed.", EXTRA_PERS if pers_flag else EXTRA_P),
        tags=(["third-party-name"] if disc else []) + ["bar runner", "home bar"],
        alt_d="team colours with a badge circle at each end" if g == "GB" else f"{design} design",
    )


def main():
    before = json.load(open(sys.argv[1]))
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    created = {c["id"]: c["handle"] for c in json.load(open(ROOT / "exports/bar-mats/2026-10-08/created.json"))}
    newp = {p["handle"]: p for p in D.P}
    plan = []
    for n in before:
        t = n["title"]
        if n["id"] in created:
            x = new_record(n, newp[created[n["id"]]])
            fam = "new-" + newp[created[n["id"]]]["group"]
        elif t.startswith("Personalized ") and t.endswith(" Bar Mat - Home Bar Runner"):
            x = club_record(n, t[len("Personalized "):-len(" Bar Mat - Home Bar Runner")])
            fam = "club"
        elif re.search(r"Design M(\d+)$", t):
            x = m_record(n, int(re.search(r"Design M(\d+)$", t).group(1)))
            fam = "milan"
        elif t.startswith("VE Day 80th"):
            x = ve_record(n, int(re.search(r"Design (\d)", t).group(1)))
            fam = "ve-day"
        else:
            raise SystemExit("unknown bar mat: " + t)
        x["id"] = n["id"]
        desc = describe(x)
        st = seo_title(x["seo"])
        sd = fit_meta(x["meta"])
        pkC = cap(x["pk"])
        alts = []
        for i, m in enumerate(n["media"]["nodes"]):
            if not m.get("id"):
                continue
            a = f"{pkC} – {x['alt_d']}" if i == 0 else f"{pkC}, {x['alt_d']} – photo {i + 1}"
            alts.append({"id": m["id"], "alt": a})
        opt = n["options"][0]
        vals = []
        for v in opt["optionValues"]:
            nv = SMALL if v["name"].lower().startswith(("small", "medium")) else LARGE if v["name"].lower().startswith("large") else None
            if nv is None:
                raise SystemExit("odd option " + v["name"])
            if nv != v["name"]:
                vals.append({"id": v["id"], "name": nv})
        gtypes = {m["key"]: m["type"] for m in n["g"]["nodes"]}
        sku = n["variants"]["nodes"][0]["sku"]
        gm = {"custom_product": ("true", "boolean"), "condition": ("new", None), "google_product_category": (CAT, None),
              "gender": ("unisex", None), "age_group": ("adult", None), "color": (x["colour"], None), "mpn": (sku, None)}
        mfs = []
        for key, (val, typ) in gm.items():
            typ = gtypes.get(key) or typ or "single_line_text_field"
            mfs.append({"ownerId": n["id"], "namespace": "mm-google-shopping", "key": key, "value": val, "type": typ})
        tags_add = [tg for tg in x["tags"] if tg not in n["tags"]]
        plan.append(dict(id=n["id"], title=t, handle=n["handle"], status=n["status"], family=fam, primary_keyword=x["pk"],
                         descriptionHtml=desc, words=words(desc), seo_title=st, seo_description=sd,
                         option_id=opt["id"], option_values=vals, alts=alts, metafields=mfs, tags_add=tags_add,
                         productType="Bar Mats", vendor="Foxy Printing"))
    # checks
    bad = [(p["title"], p["words"]) for p in plan if not 180 <= p["words"] <= 350]
    dup = len(plan) - len({p["descriptionHtml"] for p in plan})
    print(len(plan), "products; words out of range:", bad, "; duplicate descriptions:", dup)
    for p in plan:
        assert "330" not in p["descriptionHtml"] + p["seo_title"] + p["seo_description"]
        assert len(p["seo_title"]) <= 60 and 140 <= len(p["seo_description"]) <= 155, p["title"]
        assert p["descriptionHtml"].count("<h2>") == 1 and "[" not in p["descriptionHtml"]
    json.dump(plan, open(out / "plan.json", "w"), indent=1, ensure_ascii=False)

    # mutations: A) productUpdate (+tags) B) options C) metafields D) alts
    def batches(ops, size, name):
        for i in range(0, len(ops), size):
            (out / f"{name}_{i // size:02d}.graphql").write_text("mutation {\n" + "\n".join(ops[i:i + size]) + "\n}\n")
    up, tg, op = [], [], []
    for i, p in enumerate(plan):
        up.append(f'u{i}: productUpdate(product: {{id: {q(p["id"])}, descriptionHtml: {q(p["descriptionHtml"])}, productType: "Bar Mats", '
                  f'vendor: "Foxy Printing", seo: {{title: {q(p["seo_title"])}, description: {q(p["seo_description"])}}}}}) '
                  f'{{ product {{ id }} userErrors {{ field message }} }}')
        if p["tags_add"]:
            tg.append(f'tg{i}: tagsAdd(id: {q(p["id"])}, tags: {q(p["tags_add"])}) {{ userErrors {{ field message }} }}')
        if p["option_values"]:
            vals = ", ".join("{id: %s, name: %s}" % (q(v["id"]), q(v["name"])) for v in p["option_values"])
            op.append(f'o{i}: productOptionUpdate(productId: {q(p["id"])}, option: {{id: {q(p["option_id"])}}}, optionValuesToUpdate: [{vals}]) '
                      f'{{ userErrors {{ field message }} }}')
    batches(up, 12, "a_update")
    batches(tg + op, 40, "b_tags_options")
    mfs = [m for p in plan for m in p["metafields"]]
    json.dump([mfs[i:i + 25] for i in range(0, len(mfs), 25)], open(out / "c_metafields.json", "w"), ensure_ascii=False)
    alts = [a for p in plan for a in p["alts"]]
    json.dump([alts[i:i + 50] for i in range(0, len(alts), 50)], open(out / "d_alts.json", "w"), ensure_ascii=False)
    print("files:", sorted(f.name for f in out.iterdir()))


if __name__ == "__main__":
    main()
