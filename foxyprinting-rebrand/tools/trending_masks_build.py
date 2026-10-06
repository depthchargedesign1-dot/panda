"""Build the 6 Oct 2026 "trending 100" celebrity face masks (the rows with Dropbox artwork).

Steps (run in order):
  python3 tools/trending_masks_build.py images <scratch_dir>   # src/<Name>.jpg -> web/<handle>.jpg (white bg, A4, <= 2048 px tall)
  python3 tools/trending_masks_build.py build  <scratch_dir>   # products.json + create_*.gql (productCreate, ACTIVE)

<scratch_dir>/src/<Name>.jpg are the Dropbox artwork files (one face each); print + cut files come from
tools/artwork/mask_cutline.py (Jeff Hordley and Jimin needed hand-set eye centres; Jimin a softer outline for
his pale pink hair, see tools/artwork/mask_cutline_soft.py).

Copy comes from tools/mask_copy.py (build) with a hand-written intro per person, then the option-specific
wording is swapped in: every single mask now sells as Style Ready Cut / DIY and Fitting Elastic / Stick
(owner, 6 Oct 2026; plan/product-facts.md "Face masks"). Never say the elastic or stick is pre-attached.
"""
import hashlib
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mask_copy as MC  # noqa: E402

CATEGORY = "Apparel & Accessories > Costumes & Accessories > Masks"
CATEGORY_ID = "gid://shopify/TaxonomyCategory/aa-3-4"
# shopify.* category metafields, copied from the Graeme Swann 2026 mask (graeme-swann-2026-face-mask)
SHOPIFY_MF = [("shopify", "fabric", "list.metaobject_reference", '["gid://shopify/Metaobject/562294882685"]'),
              ("shopify", "age-group", "list.metaobject_reference", '["gid://shopify/Metaobject/283517714813"]'),
              ("shopify", "target-gender", "list.metaobject_reference", '["gid://shopify/Metaobject/283517747581"]'),
              ("shopify", "usage-type", "list.metaobject_reference", '["gid://shopify/Metaobject/283517813117"]')]
# Standard extra images (existing MediaImage files), same order as the Graeme Swann 2026 mask
EXTRA_MEDIA = ["gid://shopify/MediaImage/69780412662141",  # how to assemble ready-to-wear
               "gid://shopify/MediaImage/69780412694909",  # how to assemble DIY
               "gid://shopify/MediaImage/64890134987133",  # product information
               "gid://shopify/MediaImage/64890135085437",  # masks in use at a party
               "gid://shopify/MediaImage/64890135216509"]  # group photos
LIFESTYLE = ["gid://shopify/MediaImage/69808200909181", "gid://shopify/MediaImage/69808201040253",
             "gid://shopify/MediaImage/69808206086525", "gid://shopify/MediaImage/69808218702205",
             "gid://shopify/MediaImage/69808201105789", "gid://shopify/MediaImage/69808206152061"]
VARIANTS = [("Ready Cut", "Elastic", "RC-E", "2.99"), ("Ready Cut", "Stick", "RC-S", "3.49"),
            ("DIY", "Elastic", "DIY-E", "1.50"), ("DIY", "Stick", "DIY-S", "2.00")]
BASE_TAGS = ["Cardboard Face Masks", "Celebrity Face Mask", "Celebrity Party Masks", "Costume Mask", "Face Mask", "Facemask",
             "Fancy Dress", "Stag Do Mask", "Hen Party Mask", "mask-stag-hen", "Photo Booth Prop", "TV Stars And Celebrity Masks",
             "foxy-new-2026", "foxy-range-celebrity-masks", "foxy-src-dropbox", "foxy-trending-oct2026", "new-arrivals",
             "third-party-name", "celebrity-face-mask"]
# Tags that put the mask into the suggested smart collections (rules read 6 Oct 2026)
COLL_TAGS = {"music-celebrities": ["mask-music", "MUSIC STARS"], "sport-celebrities": ["mask-sport", "Sport Celebrities", "SPORTS STARS"],
             "movie-actor-face-masks": ["mask-film-stars", "MOVIE STARS"], "tv-celebritys": ["Movie Actor Face Masks"],
             "tv-star-masks": ["mask-tv-stars", "TV STARS"], "film-movie-celebrities": ["Film Celebrities"],
             "reality-tv-face-masks": ["mask-reality-tv"], "emmerdale": ["EMMERDALE"], "comedians": ["mask-comedians"],
             "strictly-come-dancing": ["Strictly Come Dancing"]}

BAND = "It is also an unofficial fan design, not endorsed by or connected with BTS, their management or record label. All names and trademarks belong to their respective owners."

P = [  # name (as on the mask), title name, handle, sku stem, ident category, show, suggested collections, intro, extra
    dict(key="Liam Gallagher", title="Liam Gallagher", handle="liam-gallagher-face-mask", sku="LiamGallagher", cat="music",
         colls=["music-celebrities"],
         intro="Our Liam Gallagher face mask brings a bit of rock and roll swagger to any party, from gig pre-drinks to a Britpop-themed birthday. Add a parka and a tambourine and you're halfway there."),
    dict(key="Travis Kelce", title="Travis Kelce", handle="travis-kelce-face-mask", sku="TravisKelce", cat="sport", sport="nfl",
         colls=["music-celebrities", "sport-celebrities"],
         intro="This Travis Kelce face mask is a winner for American football fans and pop fans alike, whether it's a big-game watch party or a wedding-themed hen do. Pair him up with a pop star mask for the perfect couple's costume."),
    dict(key="Matt Damon", title="Matt Damon", handle="matt-damon-face-mask", sku="MattDamon", cat="film",
         colls=["movie-actor-face-masks", "tv-celebritys"],
         intro="Our Matt Damon face mask puts a Hollywood leading man at your next movie night or awards-style party. Hand a few out and watch the group photos fill up with the same famous grin."),
    dict(key="Jerry Hall", title="Jerry Hall", handle="jerry-hall-face-mask", sku="JerryHall", cat="tv",
         colls=["tv-star-masks", "film-movie-celebrities"],
         intro="Our Jerry Hall face mask brings supermodel glamour to hen dos, birthdays and 70s-themed parties. The famous blonde waves and bright red lipstick make it instantly recognisable across the room."),
    dict(key="Jimin", title="Jimin Face Mask (BTS)", handle="jimin-bts-face-mask", sku="JiminBTS", cat="music", band=True,
         colls=["music-celebrities"],
         intro="Our Jimin face mask is made for K-pop fans heading to a concert pre-party, a fan meet-up or a themed birthday. The pink hair makes it a stand-out in any group photo."),
    dict(key="V", title="V Face Mask (Kim Taehyung, BTS)", handle="v-kim-taehyung-bts-face-mask", sku="VKimTaehyungBTS", cat="music", band=True,
         colls=["music-celebrities"], name="V (Kim Taehyung)",
         intro="Our V (Kim Taehyung) face mask is a must for K-pop fans planning a concert night, a sleepover or a fan-club party. Line up with friends in the other member masks for a group shot to remember."),
    dict(key="RM", title="RM Face Mask (Kim Namjoon, BTS)", handle="rm-kim-namjoon-bts-face-mask", sku="RMKimNamjoonBTS", cat="music", band=True,
         colls=["music-celebrities"], name="RM (Kim Namjoon)",
         intro="Our RM (Kim Namjoon) face mask, complete with a cheeky wink, is a fun pick for K-pop fans at a karaoke night, a concert pre-party or a themed birthday."),
    dict(key="Suga", title="Suga Face Mask (Min Yoongi, BTS)", handle="suga-min-yoongi-bts-face-mask", sku="SugaMinYoongiBTS", cat="music", band=True,
         colls=["music-celebrities"], name="Suga (Min Yoongi)",
         intro="Our Suga (Min Yoongi) face mask is a great way for K-pop fans to show who their favourite is, at a gig, a fan meet-up or a birthday party. Collect the set and bring the whole crew."),
    dict(key="J-Hope", title="J-Hope Face Mask (Jung Hoseok, BTS)", handle="j-hope-jung-hoseok-bts-face-mask", sku="JHopeJungHoseokBTS", cat="music", band=True,
         colls=["music-celebrities"], name="J-Hope (Jung Hoseok)",
         intro="Our J-Hope (Jung Hoseok) face mask brings a big smile to K-pop parties, concert queues and dance-themed birthdays. It's a sunny addition to any fan's group photo."),
    dict(key="Florence Welch", title="Florence Welch", handle="florence-welch-face-mask", sku="FlorenceWelch", cat="music",
         colls=["music-celebrities"],
         intro="Our Florence Welch face mask comes with that unmistakable flame-red hair, ready for festival weekends, karaoke nights and gig pre-drinks."),
    dict(key="Mark Ronson", title="Mark Ronson", handle="mark-ronson-face-mask", sku="MarkRonson", cat="music",
         colls=["music-celebrities"],
         intro="Our Mark Ronson face mask is a fun pick for music lovers, DJs and anyone throwing a dance-floor birthday. The sharp quiff does half the work for you."),
    dict(key="Ben Price", title="Ben Price", handle="ben-price-face-mask", sku="BenPrice", cat="tv",
         colls=["reality-tv-face-masks", "tv-star-masks"],
         intro="Our Ben Price face mask is a fun one for telly fans, whether you're hosting a reality TV launch night or a soap-themed birthday. It's sure to get a laugh when the cameras come out."),
    dict(key="Andrew Garfield", title="Andrew Garfield", handle="andrew-garfield-face-mask", sku="AndrewGarfield", cat="film",
         colls=["movie-actor-face-masks", "tv-celebritys"],
         intro="Our Andrew Garfield face mask brings a film-star face to movie nights, Oscars-style parties and fancy dress birthdays."),
    dict(key="Nicholas Hoult", title="Nicholas Hoult", handle="nicholas-hoult-face-mask", sku="NicholasHoult", cat="film",
         colls=["movie-actor-face-masks", "tv-celebritys"],
         intro="Our Nicholas Hoult face mask is a great pick for film fans planning a movie night, a themed birthday or a stag do with a difference."),
    dict(key="Jeff Hordley", title="Jeff Hordley", handle="jeff-hordley-face-mask", sku="JeffHordley", cat="tv", show="Emmerdale",
         colls=["tv-star-masks", "film-movie-celebrities", "emmerdale"],
         intro="Our Jeff Hordley face mask is made for soap fans, perfect for an Emmerdale watch party, a telly awards night or a soap-themed birthday."),
    dict(key="Joel Dommett", title="Joel Dommett", handle="joel-dommett-face-mask", sku="JoelDommett", cat="comedy",
         colls=["comedians", "tv-star-masks"],
         intro="Our Joel Dommett face mask is a cheeky pick for comedy nights, birthday roasts and telly awards parties. That big grin-ready face is made for group photos."),
    dict(key="Gwen", title="Gwen Face Mask (Melanie Walters)", handle="gwen-melanie-walters-face-mask", sku="GwenMelanieWalters", cat="tv",
         show="Gavin & Stacey", character=True, colls=["strictly-come-dancing", "tv-star-masks"], name="Gwen",
         intro="Our Gwen face mask shows Melanie Walters as the much-loved Welsh mum from Gavin & Stacey, perfect for a Barry Island-themed party, a telly night in or a family fancy dress do."),
]

HOW = [
    "Each {pk} is digitally printed in full colour on 350gsm silk card. Choose Ready Cut and we cut it to the shape of the face and cut out the eye holes for you, or choose DIY and it comes printed only, for you to cut out at home.",
    "We print this {label} mask in full colour on thick 350gsm silk card. Ready Cut masks arrive cut to shape with the eye holes cut; DIY masks are printed only, so you cut them out yourself and save a little.",
    "Printed in full colour on 350gsm silk card, the mask comes in two styles: Ready Cut (cut to the face shape with the eye holes cut) or DIY (printed only, for you to cut out).",
]
FIT = "Then pick your fitting: elastic and sticky tabs, or a stick and stickers for a hand-held mask, supplied for you to attach."


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def body_for(p):
    name = p.get("name", p["key"])
    ident = dict(name=name, show=p.get("show"), category=p["cat"], sport=p.get("sport"), blurb=p["intro"])
    prod = {"handle": p["handle"], "title": p["title"], "productType": "Celebrity Facemask", "tags": []}
    b = MC.build(prod, ident)
    body = b["body"]
    pk = f"{name} face mask"
    k = MC.SPORT_CAT.get(ident.get("sport") or "", "sport") if p["cat"] == "sport" else MC.IDENT_CAT.get(p["cat"], "celeb")
    label = next((c[2] for c in MC.CATS if c[0] == k), "celebrity")
    # option-aware "how" paragraph (replaces mask_copy's elastic-only wording)
    how = MC.pick(HOW, p["handle"], "how2").format(pk=pk, label=label)
    body = re.sub(r"(<h2>.*?</h2>\n<p>)(.*?)( (?:Want|Need|Can't find))", lambda m: m.group(1) + html.escape(how + " " + FIT, quote=False) + m.group(3), body, count=1, flags=re.S)
    body = body.replace("<li>Pre-cut eye holes, with elastic and sticky tabs included</li>",
                        "<li>Ready Cut or DIY, with elastic or a stick supplied for you to attach</li>")
    body = body.replace("<li>Fit: one size for adults; elastic and sticky tabs included</li>",
                        "<li>Fitting: elastic and sticky tabs, or a stick and stickers, supplied for you to attach</li>")
    body = body.replace("<li>Pre-cut eye holes; cut to the shape of the face</li>",
                        "<li>Style: Ready Cut (cut to shape, eye holes cut) or DIY (printed only)</li>")
    body = body.replace("Full A4 size (297 x 210 mm), so it covers an adult face", "Full A4 size (297 x 210 mm), big enough to cover an adult face")
    if p.get("character"):
        disc = ("This is an unofficial design inspired by Gwen from Gavin &amp; Stacey. It is not official merchandise and is not endorsed by, "
                "sponsored by, or connected with Gavin &amp; Stacey, the BBC, the show's producers or any of their licensees. Melanie Walters has "
                "not endorsed, sponsored or approved this product, and Foxy Printing has no connection with her. All names, characters and "
                "trademarks belong to their respective owners.")
        body = re.sub(r'<p class="disclaimer">.*?</p>$', f'<p class="disclaimer">{disc}</p>', body, flags=re.S)
        body = body.replace("Celebrity Face Mask</h2>", "TV Character Face Mask</h2>")
    elif p.get("band"):
        body = re.sub(r'(<p class="disclaimer">.*?)(</p>)$', lambda m: m.group(1) + " " + html.escape(BAND, quote=False) + m.group(2), body, flags=re.S)
    if len(re.sub(r"<[^>]+>", " ", body).split()) > 350:  # keep within 180-350 words: drop the 5th bullet
        body = re.sub(r"(<h3>Why you'll love it</h3>\n<ul>\n(?:<li>.*?</li>\n){4})<li>.*?</li>\n", r"\1", body, count=1)
    return body, b, pk


def seo_title(p):
    name = p.get("name", p["key"])
    short = re.sub(r"\s*\(.*?\)", "", name)
    opts = [f"{name} Face Mask | Foxy Printing", f"{short} Face Mask | Foxy Printing", f"{short} Face Mask"]
    if p.get("band"):
        opts = [f"{short} K-Pop Star Face Mask | Foxy Printing", f"{short} K-Pop Face Mask | Foxy Printing"]
    if p.get("character"):
        opts = ["Gwen Face Mask – Welsh TV Mum | Foxy Printing", "Gwen Face Mask | Foxy Printing"]
    return next(t for t in opts if len(t) <= 60)


FILLERS = [" Posted in a board-backed envelope.", " Ideal for groups.", " Quick UK delivery.", " Fun for all.", " Order today.", " UK made."]


def meta(p, occ):
    name = re.sub(r"\s*\(.*?\)", "", p.get("name", p["key"]))
    bases = [f"Fancy dress made easy: a {name} face mask on thick 350gsm card, Ready Cut or DIY, with elastic or a stick. Great for {occ}.",
             f"Get the party started with a {name} face mask. Full-colour print on 350gsm card, Ready Cut or DIY. Perfect for {occ}.",
             f"{name} card face mask for {occ}. Printed on 350gsm silk card, Ready Cut or DIY, with elastic or a stick.",
             f"A {name} face mask printed on 350gsm silk card, Ready Cut or DIY, with elastic or a stick to attach.",
             f"{name} face mask on thick 350gsm card, Ready Cut or DIY."]
    start = int(hashlib.md5((p["handle"] + "meta").encode()).hexdigest(), 16) % 3
    for base in bases[start:3] + bases[:start] + bases[3:]:
        if len(base) > 155:
            continue
        m = base
        for f in FILLERS:
            if len(m) >= 140:
                break
            if len(m + f) <= 155:
                m += f
        m = re.sub(r"\ba ([AEIOU])", r"an \1", m)
        if 140 <= len(m) <= 155:
            return m
    raise SystemExit(f"meta failed {p['handle']}")


def images(scratch):
    import cv2
    import numpy as np
    sys.path.insert(0, os.path.join(HERE, "artwork"))
    import mask_cutline as M
    out = os.path.join(scratch, "web")
    os.makedirs(out, exist_ok=True)
    for p in P:
        img = cv2.imread(os.path.join(scratch, "src", p["key"] + ".jpg"))
        h, w = img.shape[:2]
        pad = 20
        padded = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        m = M.face_mask(padded)[pad:-pad, pad:-pad]
        m = cv2.dilate(m, np.ones((7, 7), np.uint8))
        alpha = cv2.GaussianBlur(m, (0, 0), 1.5).astype(float)[..., None] / 255
        clean = (img * alpha + 255 * (1 - alpha)).astype(np.uint8)  # pure white outside the face
        if p["key"] == "Jimin":
            clean = img  # pale pink hair: keep the artwork exactly as supplied (background is already white)
        H = min(2048, h)
        W = int(round(H / 2 ** 0.5))
        canvas = np.full((H, W, 3), 255, np.uint8)
        s = min(W * 0.94 / w, H * 0.94 / h)
        nw, nh = int(w * s), int(h * s)
        small = cv2.resize(clean, (nw, nh), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
        x, y = (W - nw) // 2, (H - nh) // 2
        canvas[y:y + nh, x:x + nw] = small
        cv2.imwrite(os.path.join(out, p["handle"] + ".jpg"), canvas, [cv2.IMWRITE_JPEG_QUALITY, 90])
        print(p["handle"], W, H)


def build(scratch):
    q = lambda s: json.dumps(s, ensure_ascii=False)
    rows = []
    for i, p in enumerate(P):
        body, b, pk = body_for(p)
        k = MC.SPORT_CAT.get(p.get("sport") or "", "sport") if p["cat"] == "sport" else MC.IDENT_CAT.get(p["cat"], "celeb")
        occ = MC.pick(next((c[4] for c in MC.CATS if c[0] == k), MC.DEFAULT[4]), p["handle"], "o1")
        title = (p["title"] if "Face Mask" in p["title"] else f"{p['title']} Face Mask") + " – Fancy Dress Cardboard Costume Mask"
        skus = [f"FaceMask-{p['sku']}-{s}" for *_, s, _ in VARIANTS]
        tags = list(BASE_TAGS)
        for c in p["colls"]:
            tags += COLL_TAGS[c]
        if p["cat"] == "music":
            tags += ["Music Fancy Dress"]
        if p.get("band"):
            tags += ["K-Pop Face Mask"]
        if p.get("sport") == "nfl":
            tags += ["mask-nfl", "American Football"]
        tags = sorted(set(tags), key=str.lower)
        mf = [("mm-google-shopping", "custom_product", "boolean", "true"),
              ("mm-google-shopping", "condition", "single_line_text_field", "new"),
              ("mm-google-shopping", "google_product_category", "single_line_text_field", CATEGORY),
              ("mm-google-shopping", "gender", "single_line_text_field", "unisex"),
              ("mm-google-shopping", "age_group", "single_line_text_field", "adult"),
              ("mm-google-shopping", "color", "single_line_text_field", "Multicolor"),
              ("mm-google-shopping", "mpn", "single_line_text_field", skus[0])] + SHOPIFY_MF
        name = p.get("name", p["key"])
        alt = f"{name} face mask – printed cardboard {'TV character' if p.get('character') else 'celebrity'} face mask on a white background, front view"
        st = int(hashlib.md5(p["handle"].encode()).hexdigest(), 16) % len(LIFESTYLE)
        life = [LIFESTYLE[(st + j) % len(LIFESTYLE)] for j in range(3)]
        rows.append(dict(key=p["key"], name=name, title=title, handle=p["handle"], body=body, seo_title=seo_title(p), meta=meta(p, occ),
                         tags=tags, skus=skus, metafields=mf, alt=alt, extra_media=EXTRA_MEDIA + life, collections=p["colls"]))

    # checks
    bad = re.compile(r"\b(official|licen[cs]ed|authentic|genuine|approved|endorsed|merchandise|signed|autograph\w*)\b", re.I)
    for r in rows:
        words = len(re.sub(r"<[^>]+>", " ", r["body"]).split())
        assert 180 <= words <= 350, (r["handle"], words)
        assert len(r["seo_title"]) <= 60, r["seo_title"]
        assert 140 <= len(r["meta"]) <= 155, (r["handle"], len(r["meta"]))
        assert len(r["title"]) <= 150
        assert r["body"].count("<h2>") == 1 and "[" not in r["body"]
        assert r["body"].rstrip().endswith("</p>") and '<p class="disclaimer">' in r["body"].rsplit("<h3>", 1)[-1]
        assert not bad.search(r["body"].split("<h3>Please note</h3>")[0]), r["handle"]
        assert "pre-attached" not in r["body"] and "elastic and sticky tabs included" not in r["body"], r["handle"]
        first = re.sub(r"<[^>]+>", "", r["body"].split("</p>")[0])
        assert norm(r["name"] + " face mask") in norm(first.split(". ")[0]), (r["handle"], first)
        r["words"] = words
    assert len({r["body"] for r in rows}) == len(rows)
    json.dump(rows, open(os.path.join(scratch, "products.json"), "w"), indent=1, ensure_ascii=False)
    for r in rows:
        print(r["handle"], r["words"], len(r["meta"]), r["seo_title"])


def gql_create(r, resource_url):
    q = lambda s: json.dumps(s, ensure_ascii=False)
    mfs = ", ".join(f"{{namespace:{q(a)}, key:{q(b)}, type:{q(c)}, value:{q(v)}}}" for a, b, c, v in r["metafields"])
    return (f"productCreate(product:{{title:{q(r['title'])}, handle:{q(r['handle'])}, status:ACTIVE, vendor:\"Foxy Printing\", "
            f"productType:\"Celebrity Facemask\", category:{q(CATEGORY_ID)}, tags:{q(r['tags'])}, descriptionHtml:{q(r['body'])}, "
            f"seo:{{title:{q(r['seo_title'])}, description:{q(r['meta'])}}}, "
            f"productOptions:[{{name:\"Style\", values:[{{name:\"Ready Cut\"}}, {{name:\"DIY\"}}]}}, {{name:\"Fitting\", values:[{{name:\"Elastic\"}}, {{name:\"Stick\"}}]}}], "
            f"metafields:[{mfs}]}}, media:[{{originalSource:{q(resource_url)}, alt:{q(r['alt'])}, mediaContentType:IMAGE}}]) "
            f"{{ product {{ id handle variants(first:5) {{ nodes {{ id }} }} media(first:2) {{ nodes {{ id }} }} }} userErrors {{ field message }} }}")


def gql_variants(r, pid):
    q = lambda s: json.dumps(s, ensure_ascii=False)
    vs = []
    for (style, fit, _, price), sku in zip(VARIANTS, r["skus"]):
        vs.append(f"{{optionValues:[{{optionName:\"Style\", name:{q(style)}}}, {{optionName:\"Fitting\", name:{q(fit)}}}], price:{q(price)}, "
                  f"inventoryPolicy:CONTINUE, taxable:true, inventoryItem:{{sku:{q(sku)}, tracked:false, requiresShipping:true, "
                  f"measurement:{{weight:{{value:0, unit:GRAMS}}}}}}}}")
    return (f"productVariantsBulkCreate(productId:{q(pid)}, strategy:REMOVE_STANDALONE_VARIANT, variants:[{', '.join(vs)}]) "
            f"{{ productVariants {{ id sku price }} userErrors {{ field message }} }}")


if __name__ == "__main__":
    {"images": images, "build": build}[sys.argv[1]](sys.argv[2])
