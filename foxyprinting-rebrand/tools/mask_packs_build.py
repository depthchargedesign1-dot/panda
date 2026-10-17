"""Celebrity face mask PACKS and PAIRS approved by the owner on 6 Oct 2026 ("Yes make all the pairing ideas").

  python3 tools/mask_packs_build.py <out_dir>    # writes products.json (copy, SEO, tags, metafields, media plan) + checks

Structure copied from the existing listings (read 6 Oct 2026):
  * BTS 5-pack  -> "Spice Girls Face Masks – 5-Pack Party Set" / "One Direction Face Masks – 5-Pack Party Set":
                   one variant (Default Title), £6.99, masks cut to shape with eye holes, elastic supplied.
  * Pairs       -> "Lou and Andy Couple Face Mask Pair": option Style = Ready to Wear £4.99 / DIY £2.99.
Product type "Celebrity Facemask" (the house type for new masks; the two 5-packs use different legacy types,
"Fancy Dress Face Mask" and "TV STARS", and this type also puts the pack in the ALL MASKS collection).
Main images: tools/mask_pack_images.py (masks side by side, no text). Facts: plan/product-facts.md "Face masks".
Not built: Dubois v Wardley fight pack (no mask artwork for either boxer; both on FACE-PHOTOS-NEEDED.txt).
"""
import json
import os
import re
import sys

CATEGORY = "Apparel & Accessories > Costumes & Accessories > Masks"
CATEGORY_ID = "gid://shopify/TaxonomyCategory/aa-3-4"
SHOPIFY_MF = [("shopify", "fabric", "list.metaobject_reference", '["gid://shopify/Metaobject/562294882685"]'),
              ("shopify", "age-group", "list.metaobject_reference", '["gid://shopify/Metaobject/283517714813"]'),
              ("shopify", "target-gender", "list.metaobject_reference", '["gid://shopify/Metaobject/283517747581"]'),
              ("shopify", "usage-type", "list.metaobject_reference", '["gid://shopify/Metaobject/283517813117"]')]
ASSEMBLE_RTW = "gid://shopify/MediaImage/69780412662141"   # how to assemble ready-to-wear
ASSEMBLE_DIY = "gid://shopify/MediaImage/69780412694909"   # how to assemble DIY
INFO = ["gid://shopify/MediaImage/64890134987133",          # product information
        "gid://shopify/MediaImage/64890135085437",          # masks in use at a party
        "gid://shopify/MediaImage/64890135216509"]          # group photos
LIFESTYLE = ["gid://shopify/MediaImage/69808200909181", "gid://shopify/MediaImage/69808201040253",
             "gid://shopify/MediaImage/69808206086525"]
BASE_TAGS = ["Cardboard Face Masks", "Celebrity Face Mask", "Celebrity Party Masks", "Costume Mask", "Face Mask", "Facemask",
             "Fancy Dress", "Hen Party Mask", "Mask Pack", "mask-packs-couples", "Photo Booth Prop", "TV Stars And Celebrity Masks",
             "celebrity-face-mask", "foxy-new-2026", "foxy-range-celebrity-masks", "foxy-trending-oct2026", "foxy-mask-pack",
             "new-arrivals", "third-party-name", "MUSIC STARS", "mask-music", "Music Fancy Dress"]

CELEB = ("This is an unofficial novelty product made for fun and fancy dress. {names} have not endorsed, sponsored or approved "
         "this product, and Foxy Printing has no connection with them. Their names are used only to describe the design.")
BAND = ("It is also an unofficial fan design, not endorsed by or connected with {band}, their management or record label. "
        "All names and trademarks belong to their respective owners.")
TM = " All names and trademarks belong to their respective owners."

PACKS = [
    dict(
        key="bts", handle="bts-face-masks-5-pack-party-set", sku="FaceMask-BTS5Pack",
        title="BTS Face Masks – 5-Pack Party Set: Jimin, V, RM, Suga & J-Hope Card Masks",
        seo_title="K-Pop Boy Band Face Mask 5-Pack | Foxy Printing",
        meta=("Five K-pop star card face masks in one pack: Jimin, V, RM, Suga and J-Hope. Cut to shape with eye holes, "
              "elastic supplied. Great for fan parties."),
        variants=[dict(option=None, price="6.99", sku="FaceMask-BTS5Pack")],
        tags=["K-Pop Face Mask", "kpop-masks", "BTS", "Band Face Masks", "STAG & HEN PARTY FACE MASKS"],
        members=[("Jimin", "jimin-bts-face-mask", "gid://shopify/MediaImage/69873595318653"),
                 ("V (Kim Taehyung)", "v-kim-taehyung-bts-face-mask", "gid://shopify/MediaImage/69873595384189"),
                 ("RM (Kim Namjoon)", "rm-kim-namjoon-bts-face-mask", "gid://shopify/MediaImage/69873599971709"),
                 ("Suga (Min Yoongi)", "suga-min-yoongi-bts-face-mask", "gid://shopify/MediaImage/69873600004477"),
                 ("J-Hope (Jung Hoseok)", "j-hope-jung-hoseok-bts-face-mask", "gid://shopify/MediaImage/69873600168317")],
        alt="BTS face mask pack: five printed card masks of Jimin, V, RM, Suga and J-Hope side by side",
        extra=[ASSEMBLE_RTW] + INFO + LIFESTYLE,
        body="""<p>Our BTS face mask pack puts five members of the K-pop group in one envelope, so you and your friends can turn up to a concert pre-party, a fan meet-up or a themed birthday as the boys themselves. Line up for a group photo and see who guesses who.</p>
<h2>BTS Face Mask Pack – 5 Card Masks for K-Pop Fans</h2>
<p>Inside are five masks: Jimin, V (Kim Taehyung), RM (Kim Namjoon), Suga (Min Yoongi) and J-Hope (Jung Hoseok). We print every face in full colour on thick 350gsm silk card, cut each one to the shape of the face and cut out the eye holes. Elastic and sticky tabs are supplied for you to attach.</p>
<h3>Why you'll love it</h3>
<ul>
<li>A ready-made group costume for five K-pop fans, all in one order</li>
<li>Thick 350gsm silk card that holds its shape through a whole night of dancing</li>
<li>Semi-waterproof finish, so a spilt drink won't spoil the party</li>
<li>Eye holes come cut out, so you can still see the stage</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Contents: 5 masks (Jimin, V, RM, Suga and J-Hope)</li>
<li>Size: each mask is 297 x 210 mm (A4), a full adult-size face</li>
<li>Material: 350gsm silk card, full-colour digital print</li>
<li>Fitting: elastic and sticky tabs supplied for you to attach</li>
<li>Packaging: posted flat in a board-backed envelope</li>
</ul>
<h3>Delivery</h3>
<p>Printed in our UK workshop and posted to you. Dispatch and postage options are shown at checkout.</p>
<p>Just want your favourite? Each mask is sold singly too: <a href="/products/jimin-bts-face-mask">Jimin</a>, <a href="/products/v-kim-taehyung-bts-face-mask">V</a>, <a href="/products/rm-kim-namjoon-bts-face-mask">RM</a>, <a href="/products/suga-min-yoongi-bts-face-mask">Suga</a> and <a href="/products/j-hope-jung-hoseok-bts-face-mask">J-Hope</a> (see all our <a href="/collections/k-pop-face-masks">K-pop face masks</a>).</p>
<h3>Please note</h3>
""",
        disclaimer=CELEB.format(names="Jimin, V (Kim Taehyung), RM (Kim Namjoon), Suga (Min Yoongi) and J-Hope (Jung Hoseok)")
        + " " + BAND.format(band="BTS"),
        primary="bts face mask pack",
    ),
    dict(
        key="gallagher", handle="liam-and-noel-gallagher-face-masks-brothers-pair", sku="FaceMask-LiamNoelGallagherPair",
        title="Liam & Noel Gallagher Face Masks – Brothers Pair – Britpop Fancy Dress Card Masks",
        seo_title="Liam & Noel Gallagher Face Masks Pair | Foxy Printing",
        meta=("Turn up as Britpop's famous brothers with a pair of Liam and Noel Gallagher card face masks. Ready to Wear or "
              "DIY, elastic and tabs supplied."),
        variants=[dict(option="Ready to Wear", price="4.99", sku="FaceMask-LiamNoelGallagherPair"),
                  dict(option="DIY", price="2.99", sku="FaceMask-LiamNoelGallagherPair-DIY")],
        tags=["couple-masks", "Oasis", "Britpop", "STAG & HEN PARTY FACE MASKS", "Stag Do Mask", "mask-stag-hen"],
        members=[("Liam Gallagher", "liam-gallagher-face-mask", "gid://shopify/MediaImage/69873595187581"),
                 ("Noel Gallagher", "gallagher-face-mask", "NEW:noel-gallagher-single.jpg")],
        alt="Liam and Noel Gallagher face masks, two printed card masks side by side",
        extra=[ASSEMBLE_RTW, ASSEMBLE_DIY] + INFO + LIFESTYLE,
        body="""<p>These Liam and Noel Gallagher face masks are made for two mates who fancy turning up as rock and roll's most famous brothers. Wear them to a Britpop night, a gig pre-drinks or a stag do singalong, and expect a mock argument or two.</p>
<h2>Liam and Noel Gallagher Face Masks – Brothers Pair</h2>
<p>You get two masks in one order: Liam and Noel, the brothers behind Oasis. We print each face in full colour on thick 350gsm silk card. Choose Ready to Wear and both masks come cut to the shape of the face with the eye holes cut out. Choose DIY and they come printed only, for you to cut out at home. Either way, the elastic and sticky tabs are supplied for you to attach.</p>
<h3>Why you'll love it</h3>
<ul>
<li>A double act costume for two, no wigs needed</li>
<li>Printed on 350gsm silk card that stays stiff all night</li>
<li>Semi-waterproof finish, handy for festival fields and beer gardens</li>
<li>Ready to Wear eye holes come cut out, so you can still find the bar</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Contents: 2 masks (Liam Gallagher and Noel Gallagher)</li>
<li>Size: each mask is 297 x 210 mm (A4), a full adult-size face</li>
<li>Material: 350gsm silk card, full-colour digital print</li>
<li>Style: Ready to Wear (cut to shape, eye holes cut) or DIY (printed only)</li>
<li>Fitting: elastic and sticky tabs supplied for you to attach</li>
<li>Packaging: posted flat in a board-backed envelope</li>
</ul>
<h3>Delivery</h3>
<p>Printed in our UK workshop and posted to you. Dispatch and postage options are shown at checkout.</p>
<p>Bringing the whole crew? Add more <a href="/collections/music-celebrities">music star face masks</a>, or buy a single <a href="/products/liam-gallagher-face-mask">Liam</a> or <a href="/products/gallagher-face-mask">Noel</a> mask.</p>
<h3>Please note</h3>
""",
        disclaimer=CELEB.format(names="Liam Gallagher and Noel Gallagher") + " " + BAND.format(band="Oasis"),
        primary="liam and noel gallagher face masks",
    ),
    dict(
        key="kelce-swift", handle="travis-kelce-and-taylor-swift-couple-face-mask-pair", sku="FaceMask-TravisKelceTaylorSwiftPair",
        title="Travis Kelce & Taylor Swift Couple Face Mask Pair – Celebrity Couple Card Masks – Fancy Dress & Hen Party Props",
        seo_title="Pop Star & Football Star Couple Face Masks | Foxy Printing",
        meta=("Go as the world's favourite celebrity couple with a pair of Travis Kelce and Taylor Swift card face masks. Ready to "
              "Wear or DIY. Perfect for hen dos."),
        variants=[dict(option="Ready to Wear", price="4.99", sku="FaceMask-TravisKelceTaylorSwiftPair"),
                  dict(option="DIY", price="2.99", sku="FaceMask-TravisKelceTaylorSwiftPair-DIY")],
        tags=["couple-masks", "Celebrity Couples", "mask-sport", "Sport Celebrities", "SPORTS STARS", "mask-nfl", "American Football",
              "STAG & HEN PARTY FACE MASKS", "mask-stag-hen", "Singers"],
        members=[("Travis Kelce", "travis-kelce-face-mask", "gid://shopify/MediaImage/69873595220349"),
                 ("Taylor Swift", "taylor-swift-2025-celebrity-face-mask-fancy-dress-cardboard-costume-mask", "gid://shopify/MediaImage/64651198988669")],
        alt="Travis Kelce and Taylor Swift face masks, a celebrity couple pair of printed card masks side by side",
        extra=[ASSEMBLE_RTW, ASSEMBLE_DIY] + INFO + LIFESTYLE,
        body="""<p>This Travis Kelce and Taylor Swift face mask pair is the easiest couple's costume going, whether it's a hen do, an engagement party, a big-game watch party or a pop-themed birthday. One of you is the American football star, the other is the pop superstar, and everyone in the room will get it straight away.</p>
<h2>Travis Kelce and Taylor Swift Face Masks – Celebrity Couple Pair</h2>
<p>You get two masks in one order, one of each half of the couple. We print both faces in full colour on thick 350gsm silk card. Ready to Wear masks arrive cut to the shape of the face with the eye holes cut out; DIY masks are printed only, so you cut them out yourselves and save a little. The elastic and sticky tabs are supplied with both styles for you to attach.</p>
<h3>Why you'll love it</h3>
<ul>
<li>An instant couples costume for two, ideal for a bride and groom to be</li>
<li>Thick 350gsm silk card that won't flop halfway through the first dance</li>
<li>Semi-waterproof finish, so a spilt glass of fizz won't ruin it</li>
<li>Ready to Wear eye holes come cut, so you're ready in seconds</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Contents: 2 masks (Travis Kelce and Taylor Swift)</li>
<li>Size: each mask is 297 x 210 mm (A4), a full adult-size face</li>
<li>Material: 350gsm silk card, full-colour digital print</li>
<li>Style: Ready to Wear (cut to shape, eye holes cut) or DIY (printed only)</li>
<li>Fitting: elastic and sticky tabs supplied for you to attach</li>
<li>Packaging: posted flat in a board-backed envelope</li>
</ul>
<h3>Delivery</h3>
<p>Printed in our UK workshop and posted to you. Dispatch and postage options are shown at checkout.</p>
<p>More couples? Browse our <a href="/collections/celebrity-couples-fancy-dress-face-masks">celebrity couples face masks</a>, or add a single <a href="/products/travis-kelce-face-mask">Travis Kelce</a> or <a href="/products/taylor-swift-2025-celebrity-face-mask-fancy-dress-cardboard-costume-mask">Taylor Swift</a> mask for the rest of the party.</p>
<h3>Please note</h3>
""",
        disclaimer=CELEB.format(names="Travis Kelce and Taylor Swift") + TM,
        primary="travis kelce and taylor swift face mask",
    ),
]


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def build(out):
    bad = re.compile(r"\b(official|licen[cs]ed|authentic|genuine|approved|endorsed|merchandise|signed|autograph\w*|pre-attached)\b", re.I)
    rows = []
    for p in PACKS:
        body = p["body"] + f'<p class="disclaimer">{p["disclaimer"]}</p>'
        words = len(re.sub(r"<[^>]+>", " ", body).split())
        assert 180 <= words <= 350, (p["key"], words)
        assert len(p["seo_title"]) <= 60, (p["seo_title"], len(p["seo_title"]))
        assert 140 <= len(p["meta"]) <= 155, (p["key"], len(p["meta"]))
        assert len(p["title"]) <= 150, len(p["title"])
        assert body.count("<h2>") == 1 and "[" not in body and "style=" not in body
        assert not bad.search(body.split("<h3>Please note</h3>")[0]), p["key"]
        first = norm(re.sub(r"<[^>]+>", "", body.split("</p>")[0]).split(". ")[0])
        h2 = norm(re.search(r"<h2>(.*?)</h2>", body).group(1))
        assert p["primary"] in first and p["primary"] in h2, (p["key"], first, h2)
        assert norm(body).count(p["primary"]) >= 2, p["key"]
        tags = sorted(set(BASE_TAGS + p["tags"]), key=str.lower)
        mf = [("mm-google-shopping", "custom_product", "boolean", "true"),
              ("mm-google-shopping", "condition", "single_line_text_field", "new"),
              ("mm-google-shopping", "google_product_category", "single_line_text_field", CATEGORY),
              ("mm-google-shopping", "gender", "single_line_text_field", "unisex"),
              ("mm-google-shopping", "age_group", "single_line_text_field", "adult"),
              ("mm-google-shopping", "color", "single_line_text_field", "Multicolor"),
              ("mm-google-shopping", "mpn", "single_line_text_field", p["variants"][0]["sku"])] + SHOPIFY_MF
        rows.append(dict(key=p["key"], handle=p["handle"], title=p["title"], productType="Celebrity Facemask",
                         vendor="Foxy Printing", category=CATEGORY_ID, body=body, words=words, seo_title=p["seo_title"],
                         meta=p["meta"], tags=tags, variants=p["variants"], metafields=mf, alt=p["alt"],
                         members=p["members"], extra_media=p["extra"]))
        print(p["key"], words, len(p["seo_title"]), len(p["meta"]), len(p["title"]))
    json.dump(rows, open(os.path.join(out, "products.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    build(sys.argv[1])


STAGED = {  # resourceUrls from stagedUploadsCreate (6 Oct 2026)
    "bts": "https://shopify-staged-uploads.storage.googleapis.com/tmp/17749115/files/75f41472-4027-4dc1-a1c4-436dd4d66549/bts-face-masks-5-pack-party-set.jpg",
    "gallagher": "https://shopify-staged-uploads.storage.googleapis.com/tmp/17749115/files/e8e34b42-4102-4384-b73e-9499e9c9ad81/liam-and-noel-gallagher-face-masks-brothers-pair.jpg",
    "kelce-swift": "https://shopify-staged-uploads.storage.googleapis.com/tmp/17749115/files/5d06fd94-526b-4a1f-b10c-24b160591569/travis-kelce-and-taylor-swift-couple-face-mask-pair.jpg",
}


def gql_create(r):
    q = lambda s: json.dumps(s, ensure_ascii=False)
    mfs = ", ".join(f"{{namespace:{q(a)}, key:{q(b)}, type:{q(c)}, value:{q(v)}}}" for a, b, c, v in r["metafields"])
    opts = ""
    if r["variants"][0]["option"]:
        opts = "productOptions:[{name:\"Style\", values:[" + ", ".join(f"{{name:{q(v['option'])}}}" for v in r["variants"]) + "]}], "
    return (f"mutation {{ productCreate(product:{{title:{q(r['title'])}, handle:{q(r['handle'])}, status:ACTIVE, vendor:\"Foxy Printing\", "
            f"productType:{q(r['productType'])}, category:{q(r['category'])}, tags:{q(r['tags'])}, descriptionHtml:{q(r['body'])}, "
            f"seo:{{title:{q(r['seo_title'])}, description:{q(r['meta'])}}}, {opts}metafields:[{mfs}]}}, "
            f"media:[{{originalSource:{q(STAGED[r['key']])}, alt:{q(r['alt'])}, mediaContentType:IMAGE}}]) "
            f"{{ product {{ id handle variants(first:5) {{ nodes {{ id title }} }} media(first:2) {{ nodes {{ id }} }} }} userErrors {{ field message }} }} }}")


if __name__ == "__main__" and len(sys.argv) > 2 and sys.argv[2] == "gql":
    for r in json.load(open(os.path.join(sys.argv[1], "products.json"))):
        open(os.path.join(sys.argv[1], f"create_{r['key']}.gql"), "w").write(gql_create(r))
