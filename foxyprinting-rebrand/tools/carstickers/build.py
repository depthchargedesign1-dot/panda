#!/usr/bin/env python3
"""Build before.json, plan.json and batched mutations for the car sticker 2-size update."""
import json, re, hashlib, os, html

W = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(f"{W}/collection_raw.json"))

STD = 'Standard 15cm (6")'
LRG = 'Large 30cm (12")'

SKIP = {
    "dcd-vinyl-vector-sticker-pack-collection":
        "Title says 'Sticker Pack Collection' - may be a multi-sticker pack, so a single 15cm/30cm size and per-sticker copy may be wrong. Owner to confirm.",
}

# Display names (fix apostrophes / casing / typos for the copy only; titles untouched)
DISPLAY = {
    "im-not-short-im-fun-sized-bumper-window-sticker": "I'm Not Short, I'm Fun Sized",
    "its-not-leaking-oil-its-sweating-power-2-bumper-window-sticker": "It's Not Leaking Oil, It's Sweating Power",
    "its-not-leaking-oil-its-sweating-power-bumper-window-sticker": "It's Not Leaking Oil, It's Sweating Power",
    "im-not-drunk-just-avoiding-potholes-bumper-window-sticker": "I'm Not Drunk, Just Avoiding Potholes",
    "trust-me-im-a-pro-bumper-window-sticker": "Trust Me I'm a Pro",
    "my-daddys-the-boss-2-bumper-window-sticker": "My Daddy's the Boss",
    "my-daddys-the-boss-bumper-window-sticker": "My Daddy's the Boss",
    "be-patient-im-lowered-bumper-sticker-bumper-window-sticker": "Be Patient, I'm Lowered",
    "0-60-eventually-v2-bumper-window-sticker": "0-60 Eventually",
    "0-60-eventually-bumper-window-sticker": "0-60 Eventually",
    "yourwebsite-co-uk-bumper-window-sticker": "YourWebsite.co.uk",
    "quit-hatin-bumper-window-sticker": "Quit Hatin'",
    "powered-by-poniesbumper-window-sticker": "Powered By Ponies",
    "powered-by-fairydust-bumper-window-sticker": "Powered By Fairy Dust",
    "not-my-boyfriends-car-bumper-window-sticker": "Not My Boyfriend's Car",
    "made-in-japan-perfected-in-my-garage-bumper-window-sticker": "Made in Japan, Perfected in My Garage",
    "killin-it-bumper-window-sticker": "Killin' It",
    "im-on-it-bumper-window-sticker": "I'm On It",
    "i-have-brakes-hows-your-insurance-bumper-window-sticker": "I Have Brakes, How's Your Insurance?",
    "dyslexics-are-teople-poo-bumper-window-sticker": "Dyslexics Are Teople Poo",
    "dont-steal-the-government-hates-comp-bumper-window-sticker": "Don't Steal, The Government Hates Competition",
    "dont-follow-me-3-bumper-window-sticker": "Don't Follow Me",
    "dont-follow-me-2-bumper-window-sticker": "Don't Follow Me",
    "dont-follow-me-bumper-window-sticker": "Don't Follow Me",
    "domokungking-bumper-window-sticker": "Domokun King",
    "certified-wd40-technician-bumper-sticker-bumper-window-sticker": "Certified WD-40 Technician",
    "caution-small-animals-may-dissapear-bumper-sticker-bumper-window-sticker": "Caution: Small Animals May Disappear",
    "caution-i-brake-for-no-reason-bumper-sticker-bumper-window-sticker": "Caution: I Brake for No Reason",
    "caution-may-go-side-ways-bumper-sticker-bumper-window-sticker": "Caution: May Go Sideways",
    "caution-drift-both-ways-bumper-sticker-bumper-window-sticker": "Caution: Drift Both Ways",
    "built-with-ebay-parts-bumper-sticker-bumper-window-sticker": "Built With eBay Parts",
    "because-im-happy-bumper-sticker-bumper-window-sticker": "Because I'm Happy",
    "yourname-bumper-window-sticker": "@YourName",
    "jesus-is-my-airbag-bumper-window-sticker": "Jesus Is My Airbag",
    "2-x-love-vw-bumper-window-sticker": "2 x Love VW",
    "as-seen-on-tv-bumper-sticker-bumper-window-sticker": "As Seen On TV",
    "grow-a-pair-2-bumper-window-sticker": "Grow a Pair",
    "angry-citroen-bumper-sticker-bumper-window-sticker": "Angry Citroën",
    "citroen-sport-bumper-sticker-bumper-window-sticker": "Citroën Sport",
    "citroen-bumper-sticker-bumper-window-sticker": "Citroën",
    "zombie-eat-fresh-bumper-window-sticker": "Zombie, Eat Fresh",
    "sweep-ride-bro-bumper-window-sticker": "Sweep Ride Bro",
    "official-speed-camera-test-vehicle-bumper-window-sticker": "Speed Camera Test Vehicle",
}

# Cheeky / rude: never quote the slogan in the description.
RUDE = {h for h in """
minge-mobile-bumper-window-sticker i-dont-need-sex-the-government-fucks-me-bumper-window-sticker
clunge-magnet-bumper-window-sticker when-in-doubt-fuck-it-bumper-window-sticker slow-as-fuck-bumper-window-sticker
powered-by-bitchdust-bumper-window-sticker driven-by-a-mad-bitch-bumper-window-sticker you-bumder-bumper-window-sticker
vags-are-for-fags-bumper-window-sticker no-fat-chicks-bumper-window-sticker fuck-bumper-window-sticker
fuck-you-and-your-prius-bumper-window-sticker bus-wankers-bumper-sticker-bumper-window-sticker
your-mum-likes-this-bumper-window-sticker sucks-like-ya-mum-bumper-window-sticker screw-you-bumper-window-sticker
oh-shit-bumper-window-sticker lower-than-a-smackheads-morals-bumper-window-sticker like-shit-off-a-shovel-bumper-window-sticker
jap-is-scrap-bumper-window-sticker if-its-not-jap-its-s-crap-bumper-window-sticker hello-titty-bumper-window-sticker
grow-a-pair-2-bumper-window-sticker grow-a-pair-bumper-window-sticker fubar-bumper-window-sticker
does-my-arse-look-big-bumper-window-sticker cool-story-hoe-bumper-window-sticker clunge-bumper-window-sticker
chinese-doggystyle-bumper-sticker-bumper-window-sticker bus-wankers-2-bumper-sticker-bumper-window-sticker
boobies-bumper-sticker-bumper-window-sticker be-a-flirt-lift-your-shirt-2-bumper-sticker-bumper-window-sticker
be-a-flirt-lift-your-shirt-bumper-sticker-bumper-window-sticker 100-bitch-bumper-sticker-bumper-window-sticker
""".split()}

# Third-party names -> (kind, names)
BRAND = {}
def b(handles, kind, names):
    for h in handles.split():
        BRAND[h] = (kind, names)
b("vw-performance-bumper-window-sticker vw-dope-bumper-window-sticker volkswagen-bumper-window-sticker "
  "performance-vw-bumper-window-sticker 2-x-love-vw-bumper-window-sticker golf-bumper-window-sticker",
  "brand", ["Volkswagen"])
b("vags-are-for-fags-bumper-window-sticker", "brand", ["Volkswagen Group (VAG)"])
b("toyoda-bumper-window-sticker toyota-devil-bumper-window-sticker toyota-devil-2-bumper-window-sticker "
  "toyota-sport-bumper-window-sticker fuck-you-and-your-prius-bumper-window-sticker", "brand", ["Toyota"])
b("renault-sport-bumper-window-sticker clio-sport-bumper-window-sticker", "brand", ["Renault"])
b("subaru-devil-bumper-window-sticker", "brand", ["Subaru"])
b("scooby-pig-bumper-window-sticker scooby-pig-king-bumper-window-sticker", "brand", ["Subaru", "Warner Bros. (Scooby-Doo)"])
b("corsa-killer-bumper-window-sticker", "brand", ["Vauxhall"])
b("citroen-sport-bumper-sticker-bumper-window-sticker angry-citroen-bumper-sticker-bumper-window-sticker "
  "citroen-bumper-sticker-bumper-window-sticker", "brand", ["Citroën"])
b("suzuki-bumper-window-sticker", "brand", ["Suzuki"])
b("nissan-devil-bumper-window-sticker", "brand", ["Nissan"])
b("mitsubishi-bumper-window-sticker mitsubishi-devil-bumper-window-sticker lancer-evolution-bumper-window-sticker "
  "eclipse-bumper-window-sticker", "brand", ["Mitsubishi"])
b("audi-bumper-sticker-bumper-window-sticker", "brand", ["Audi"])
b("certified-wd40-technician-bumper-sticker-bumper-window-sticker", "brand", ["WD-40 Company (WD-40)"])
b("built-with-ebay-parts-bumper-sticker-bumper-window-sticker", "brand", ["eBay"])
b("fatlace-bumper-window-sticker illest-bumper-window-sticker hella-flush-bumper-window-sticker", "brand", ["Fatlace"])
b("dubway-bumper-window-sticker zombie-eat-fresh-bumper-window-sticker", "brand", ["Subway"])
b("dubmeister-bumper-window-sticker", "brand", ["Jägermeister"])
b("tweet-this-bumper-window-sticker", "brand", ["X Corp (Twitter)"])
b("hello-titty-bumper-window-sticker", "brand", ["Sanrio (Hello Kitty)"])
b("domokungking-bumper-window-sticker", "character", ("Domo-kun", "NHK"))
b("bazinga-bumper-sticker-bumper-window-sticker", "character", ("The Big Bang Theory", "Warner Bros."))
b("rip-paul-walker-bumper-window-sticker", "celebrity", "Paul Walker")

CUSTOM_TEXT = {"yourwebsite-co-uk-bumper-window-sticker", "your-hashtag-bumper-window-sticker",
               "phone-number-bumper-window-sticker", "yourname-bumper-window-sticker"}

MASK = [(r"\bfuck", "F**k"), (r"\bshit\b", "Sh*t"), (r"\bbitch", "B*tch"), (r"\bwankers\b", "W*nkers"),
        (r"\bfags\b", "F*gs"), (r"\bclunge\b", "Cl*nge"), (r"\bminge\b", "M*nge"), (r"\btitty\b", "T*tty"),
        (r"\bbumder\b", "B*mder"), (r"\bhoe\b", "H*e"), (r"\bjap\b", "J*p"), (r"\bsex\b", "S*x"),
        (r"\barse\b", "A*se"), (r"\bdoggystyle\b", "D*ggystyle"), (r"\bboobies\b", "B**bies"),
        (r"\bs\.crap\b", "S.cr*p")]

def mask(s):
    for pat, rep in MASK:
        s = re.sub(pat, lambda m: rep if m.group(0)[0].isupper() else rep.lower(), s, flags=re.I)
    return s

def slogan_from_title(p):
    t = p["title"]
    t = re.sub(r"\s*novelty Vinyl Car Sticker$", "", t, flags=re.I)
    t = re.sub(r"\s*Bumper Sticker$", "", t)
    return t.strip()

def version(p):
    s = slogan_from_title(p)
    m = re.search(r"\s+[Vv]?(\d)$", s)
    return m.group(1) if m and not re.fullmatch(r"\d+", s) else None

def display(p):
    if p["handle"] in DISPLAY:
        return DISPLAY[p["handle"]]
    s = slogan_from_title(p)
    s = re.sub(r"\s+[Vv]?\d$", "", s) if version(p) else s
    return s

def hsh(handle, salt=""):
    return int(hashlib.md5((salt + handle).encode()).hexdigest(), 16)

def pick(lst, handle, salt):
    return lst[hsh(handle, salt) % len(lst)]

def e(s):
    return html.escape(s, quote=False)

def disclaimer(handle):
    if handle not in BRAND:
        return ""
    kind, names = BRAND[handle]
    if kind == "brand":
        if len(names) == 1:
            n = names[0]
            short = re.sub(r"\s*\(.*\)", "", n)
            txt = (f"This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {n}. "
                   f"{short} is a trademark of its owner and is used only to describe the design theme.")
            if "(" in n:
                inner = re.search(r"\((.*)\)", n).group(1)
                txt = (f"This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {short}. "
                       f"{inner} and {short} are trademarks of their owners and are referred to only to describe the design theme.")
        else:
            joined = " or ".join(names)
            txt = (f"This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {joined}. "
                   f"All names and trademarks belong to their respective owners and are used only to describe the design theme.")
    elif kind == "character":
        show, owner = names
        txt = (f"This is an unofficial design inspired by {show}. It is not official merchandise and is not endorsed by, "
               f"sponsored by, or connected with {show} or {owner}, or any of their licensees. All names, characters and "
               f"trademarks belong to their respective owners.")
    else:  # celebrity tribute
        txt = (f"This is an unofficial, fan-made tribute design. {names} has not endorsed, sponsored or approved this product, "
               f"and Foxy Printing has no connection with him or his estate. The name is used only to describe the design.")
    return f'<h3>Please note</h3><p class="disclaimer">{e(txt)}</p>'

SIZE_DETAILS = ('<h3>Size &amp; details</h3><ul>'
                '<li>Standard: 15cm (6") wide</li>'
                '<li>Large: 30cm (12") wide</li>'
                '<li>Height depends on the shape of the design</li>'
                '<li>Cut from coloured vinyl</li>'
                '<li>Apply to a clean, dry, smooth surface such as glass or paintwork</li>'
                '</ul>')
DELIVERY = '<h3>Delivery</h3><p>Posted flat in a hard-backed envelope. Postage options and costs are shown at checkout.</p>'

def noun(d):
    """Avoid 'Sell My Car Car Sticker' / 'Boot Sticker Car Sticker'."""
    dl = d.lower().rstrip("?!. ")
    if dl.endswith(" car"):
        return "sticker"
    if dl.endswith("sticker"):
        return "car decal"
    return "car sticker"

def primary_kw(p):
    h = p["handle"]
    if h in RUDE:
        return "rude car sticker"
    d = display(p)
    return f"{d} {noun(d)}"

def build_desc(p):
    h = p["handle"]
    d = e(display(p))
    rude = h in RUDE
    tribute = BRAND.get(h, (None,))[0] == "celebrity"
    custom = h in CUSTOM_TEXT
    kw = e(primary_kw(p))

    if rude:
        opener = pick([
            f"<p>Got a sense of humour that's a bit on the cheeky side? This rude car sticker carries a cheeky slogan that's sure to raise a smile (or an eyebrow) in traffic. We cut it ourselves from coloured vinyl here at Foxy Printing.</p>",
            f"<p>This rude car sticker is for drivers who like a laugh and don't mind a few raised eyebrows. The cheeky slogan is cut from coloured vinyl in our own workshop, so you get clean, sharp edges and no printed background.</p>",
            f"<p>If your mates would laugh at this one, it's probably the rude car sticker for you. We cut this cheeky slogan from coloured vinyl at Foxy Printing, ready to stick on your back window or bumper.</p>",
        ], h, "op")
        h2 = pick(["<h2>Rude Car Sticker with a Cheeky Slogan</h2>",
                   "<h2>Cheeky Rude Car Sticker for Grown-Up Drivers</h2>",
                   "<h2>A Rude Car Sticker in Two Sizes</h2>"], h, "h2")
    elif tribute:
        opener = (f"<p>This {kw} is a simple tribute for fans of the actor and of the car scene he loved. "
                  f"We cut it in-house from coloured vinyl, ready for your back window or bumper.</p>")
        h2 = f"<h2>{d} Car Sticker in Two Sizes</h2>"
    else:
        opener = pick([
            f"<p>Give your motor a bit of personality with this {kw}, cut in-house from coloured vinyl. It's a quick, low-cost way to make your car, van or back window stand out.</p>",
            f"<p>This {kw} is an easy way to add a bit of fun to your back window or bumper. We cut every one ourselves from coloured vinyl, so you get clean, sharp edges and no printed background.</p>",
            f"<p>Looking for a {kw}? This one is cut from coloured vinyl here at Foxy Printing and makes a great little gift for a car lover, or a treat for your own ride.</p>",
            f"<p>Show off your style with our {kw}. It's cut from coloured vinyl in our own workshop and looks great on back windows, bumpers and other smooth surfaces.</p>",
        ], h, "op")
        N = noun(display(p)).title()
        h2 = pick([f"<h2>{d} {N}</h2>",
                   f"<h2>{d} {N} in Two Sizes</h2>",
                   f"<h2>{d} {N} for Your Window or Bumper</h2>"], h, "h2")

    para2 = pick([
        "<p>Pick the Standard size at 15cm (6\") wide, or go big with the Large at 30cm (12\") wide. The height depends on the shape of the design. To fit it, make sure the glass or paintwork is clean and dry, then press it down firmly from the middle outwards.</p>",
        "<p>It comes in two sizes: Standard, 15cm (6\") wide, which suits most back windows, and Large, 30cm (12\") wide, for when you want it seen from further away. Height varies with the design. Just clean and dry the surface first, then smooth it on from the centre out.</p>",
        "<p>Choose Standard (15cm / 6\" wide) or Large (30cm / 12\" wide) from the size menu. The height depends on the design. For the best finish, apply it to a clean, dry surface and press it down firmly so every edge sits flat.</p>",
    ], h, "p2")
    if custom:
        para2 += "<p>Please check the photos to see exactly what is on this design before ordering.</p>"

    pool = [
        "<li>Cut from coloured vinyl, so there's no printed background, just the design itself</li>",
        "<li>Two sizes: Standard 15cm (6\") wide or Large 30cm (12\") wide</li>",
        "<li>Suits back windows, side windows, bumpers and other smooth surfaces</li>",
        "<li>Simple to fit on a clean, dry surface with no special tools</li>",
        "<li>Cut in-house by our small team at Foxy Printing</li>",
        "<li>Posted flat in a hard-backed envelope so it arrives in good shape</li>",
    ]
    if rude:
        pool.append("<li>Adult humour, best kept for grown-up drivers and their mates</li>")
    elif not tribute:
        pool.append("<li>A cheap and cheerful gift for car lovers and petrolheads</li>")
    order = sorted(range(len(pool)), key=lambda i: hsh(h, f"b{i}"))
    def why_n(n):
        return "<h3>Why you'll love it</h3><ul>" + "".join(pool[i] for i in sorted(order[:n])) + "</ul>"
    why = why_n(4)

    if rude:
        closing = pick([
            "<p>Maybe not one for the school run, but perfect for the joker in the family. Browse our other funny car stickers too.</p>",
            "<p>A cheeky little gift for the mate who has everything. Pair it with one of our other novelty bumper stickers.</p>",
            "<p>Add it to a birthday card for a laugh, or browse our other rude bumper stickers to complete the set.</p>",
        ], h, "cl")
    elif tribute:
        closing = "<p>A fitting window sticker for any car fan's daily driver.</p>"
    else:
        closing = pick([
            "<p>Pop one in with a birthday card for a fun, low-cost gift, or browse our other vinyl car decals.</p>",
            "<p>Why stop at one? Browse our other novelty bumper stickers and build a set for your ride.</p>",
            "<p>A great stocking filler for any car lover, and a fun window sticker for your own motor too.</p>",
            "<p>Treat your car, or the petrolhead in your life, to a new vinyl car decal today.</p>",
        ], h, "cl")

    opener = opener.replace("this This ", "our This ").replace("<p>This This ", "<p>Our This ")
    opener = re.sub(r"Looking for a (?=(?!Eu|eu|Uni|uni)[AEIOUaeiou8]|I'm|I )", "Looking for an ", opener)
    opener = opener.replace("Looking for a This ", "Looking for the This ")
    out = opener + h2 + para2 + why + SIZE_DETAILS + DELIVERY + closing
    if len(re.sub("<[^>]+>", " ", out).split()) > 220:
        out = opener + h2 + para2 + why_n(3) + SIZE_DETAILS + DELIVERY + closing
    return out + disclaimer(h)

SEO_OVERRIDE = {
    "you-look-really-stupid-with-your-head-like-that-bumper-window-sticker": "You Look Really Stupid Car Sticker",
    "dont-steal-the-government-hates-comp-bumper-window-sticker": "Government Hates Competition Car Sticker",
    "i-dont-need-sex-the-government-fucks-me-bumper-window-sticker": "I Don't Need S*x Car Sticker",
    "its-not-leaking-oil-its-sweating-power-2-bumper-window-sticker": "Not Leaking Oil, Sweating Power Sticker 2",
    "its-not-leaking-oil-its-sweating-power-bumper-window-sticker": "Not Leaking Oil, Sweating Power Sticker",
    "im-not-drunk-just-avoiding-potholes-bumper-window-sticker": "I'm Not Drunk, Avoiding Potholes Sticker",
    "not-sponsored-by-loans-and-overdrafts-bumper-window-sticker": "Not Sponsored By Loans & Overdrafts Sticker",
    "made-in-japan-perfected-in-my-garage-bumper-window-sticker": "Perfected in My Garage Car Sticker",
    "you-can-go-fast-but-i-can-go-anywhere-bumper-window-sticker": "You Can Go Fast, I Can Go Anywhere Sticker",
    "been-there-done-that-got-the-sticker-bumper-sticker-bumper-window-sticker": "Been There, Done That, Got the Sticker",
}

def seo_title(p):
    h = p["handle"]
    s = mask(display(p))
    if h == "official-speed-camera-test-vehicle-bumper-window-sticker":
        s = "Speed Camera Test Vehicle"
    if h in SEO_OVERRIDE:
        return SEO_OVERRIDE[h] + " | Foxy Printing"
    v = version(p)
    tail = " | Foxy Printing"
    N = noun(s).title()
    for fmt in ([f"{s} {N} (Design {v})", f"{s} {N} {v}", f"{s} Sticker {v}"] if v
                else [f"{s} {N}", f"{s} Sticker"]):
        if len(fmt + tail) <= 60:
            return fmt + tail
    # shorten slogan at a word boundary
    words = s.split()
    suffix = f" Sticker {v}" if v else " Car Sticker"
    while words and len(" ".join(words) + suffix + tail) > 60:
        words.pop()
    return " ".join(words).rstrip(",:") + suffix + tail

def seo_desc(p):
    h = p["handle"]
    rude = h in RUDE
    branded = h in BRAND
    d = display(p)
    if rude or branded or h == "official-speed-camera-test-vehicle-bumper-window-sticker":
        subj = pick(["this cheeky car sticker", "this rude car sticker", "this cheeky bumper sticker"], h, "sd") if rude \
            else pick(["this vinyl car sticker", "this novelty car sticker", "this car window sticker"], h, "sd")
        name = None
    elif len(d) > 30:
        subj = pick(["this slogan car sticker", "this novelty car sticker"], h, "sd")
        name = None
    else:
        subj = f"the {d} {noun(d)}"
        name = d
    starts = [f"Cut from coloured vinyl, {subj} comes in Standard 15cm (6\") or Large 30cm (12\") wide.",
              f"Add {subj} to your back window or bumper. Choose Standard 15cm (6\") or Large 30cm (12\") wide.",
              f"Grab {subj}, cut from coloured vinyl in Standard 15cm (6\") or Large 30cm (12\") wide."]
    ends = [" Posted flat in a hard-backed envelope.",
            " Easy to apply and posted flat.",
            " Posted flat, ready to stick on.",
            " Order yours today."]
    first = pick(range(len(starts)), h, "sa")
    cands = []
    for i in range(len(starts)):
        st = starts[(first + i) % len(starts)]
        for j in range(len(ends)):
            en = ends[(pick(range(len(ends)), h, "se") + j) % len(ends)]
            cands.append(st + en)
            cands.append(st + en.replace(" Order yours today.", " Order yours today from Foxy Printing."))
            cands.append(st + " Posted flat in a hard-backed envelope. Order yours today.")
            cands.append(st + en + " Great gift for car fans.")
    for c in cands:
        if 140 <= len(c) <= 155:
            return c
    return None

def plan():
    out, skipped = [], []
    for p in raw:
        h = p["handle"]
        v = p["variants"]["nodes"]
        ok = (p["productType"] == "Vinyl Car Stickers" and p["hasOnlyDefaultVariant"] and len(v) == 1
              and p["options"][0]["name"] == "Title" and v[0]["title"] == "Default Title")
        if not ok or h in SKIP:
            skipped.append({"id": p["id"], "handle": h, "title": p["title"],
                            "reason": SKIP.get(h, "not a single Default Title vinyl car sticker")})
            continue
        sv = v[0]
        ii = sv["inventoryItem"]
        sd = seo_desc(p)
        out.append({
            "id": p["id"], "handle": h, "title": p["title"],
            "optionId": p["options"][0]["id"], "optionValueId": p["options"][0]["optionValues"][0]["id"],
            "stdVariantId": sv["id"], "stdSku": sv["sku"], "largeSku": sv["sku"] + "-30CM",
            "inventoryPolicy": sv["inventoryPolicy"], "taxable": sv["taxable"],
            "tracked": ii["tracked"], "requiresShipping": ii["requiresShipping"],
            "weight": ii["measurement"]["weight"],
            "levels": [{"locationId": n["location"]["id"], "availableQuantity": n["quantities"][0]["quantity"]}
                       for n in ii["inventoryLevels"]["nodes"]],
            "descriptionHtml": build_desc(p),
            "seoTitle": seo_title(p), "seoDescription": sd,
            "branded": h in BRAND, "rude": h in RUDE,
            "mpnOld": (p["mpn"] or {}).get("value"),
        })
    return out, skipped

def gq(s):
    return json.dumps(s, ensure_ascii=False)

def mutation_for(items):
    parts = []
    for i, it in enumerate(items):
        pid = gq(it["id"])
        w = it["weight"]
        inv = ",".join(f'{{locationId:{gq(l["locationId"])},availableQuantity:{l["availableQuantity"]}}}' for l in it["levels"])
        parts.append(
            f'o{i}:productOptionUpdate(productId:{pid},option:{{id:{gq(it["optionId"])},name:"Size"}},'
            f'optionValuesToUpdate:[{{id:{gq(it["optionValueId"])},name:{gq(STD)}}}]){{userErrors{{field message}}}}\n'
            f'u{i}:productVariantsBulkUpdate(productId:{pid},variants:[{{id:{gq(it["stdVariantId"])},price:"3.49"}}]){{userErrors{{field message}}}}\n'
            f'c{i}:productVariantsBulkCreate(productId:{pid},variants:[{{optionValues:[{{optionName:"Size",name:{gq(LRG)}}}],'
            f'price:"6.99",inventoryPolicy:{it["inventoryPolicy"]},taxable:{str(it["taxable"]).lower()},'
            f'inventoryItem:{{sku:{gq(it["largeSku"])},tracked:{str(it["tracked"]).lower()},requiresShipping:{str(it["requiresShipping"]).lower()},'
            f'measurement:{{weight:{{unit:{w["unit"]},value:{w["value"]}}}}}}},inventoryQuantities:[{inv}]}}]){{productVariants{{id}} userErrors{{field message}}}}\n'
            f'p{i}:productUpdate(product:{{id:{pid},descriptionHtml:$d{i},'
            f'seo:{{title:{gq(it["seoTitle"])},description:{gq(it["seoDescription"])}}}}}){{userErrors{{field message}}}}\n'
            f'm{i}:metafieldsSet(metafields:[{{ownerId:{pid},namespace:"mm-google-shopping",key:"mpn",type:"single_line_text_field",value:{gq(it["stdSku"])}}}]){{userErrors{{field message}}}}\n'
            + (f't{i}:tagsAdd(id:{pid},tags:["third-party-name"]){{userErrors{{field message}}}}\n' if it["branded"] else "")
        )
    decl = ",".join(f"$d{i}:String!" for i in range(len(items)))
    q = "mutation(" + decl + "){\n" + "".join(parts) + "}"
    return q, {f"d{i}": it["descriptionHtml"] for i, it in enumerate(items)}

if __name__ == "__main__":
    items, skipped = plan()
    # before.json: full before state of every product in scope (and skipped ones)
    before = []
    for p in raw:
        before.append({k: p[k] for k in ("id", "handle", "title", "status", "productType", "tags", "descriptionHtml",
                                         "seo", "options", "variants", "mpn")})
    json.dump(before, open(f"{W}/before.json", "w"), indent=1, ensure_ascii=False)
    json.dump(items, open(f"{W}/plan.json", "w"), indent=1, ensure_ascii=False)
    json.dump(skipped, open(f"{W}/skipped.json", "w"), indent=1, ensure_ascii=False)
    os.makedirs(f"{W}/batches", exist_ok=True)
    print(len(items), "planned;", len(skipped), "skipped")
