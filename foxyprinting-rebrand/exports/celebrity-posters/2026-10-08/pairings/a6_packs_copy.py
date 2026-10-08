"""Copy, SEO and Google fields for the 4 A6 star card packs (8 Oct 2026). Writes packs.json."""
import json

SIGNED = ("This is a printed reproduction. The signature is printed as part of the design – it is not hand-signed "
          "and is not an original autograph.")


def disclaimer(names, pron="them"):
    return ('<h3>Please note</h3>\n<p class="disclaimer">' + SIGNED + " These cards are an unofficial novelty product "
            "made for fans. " + names + " have not endorsed, sponsored or approved this product, and Foxy Printing has "
            "no connection with " + pron + ". The names are used only to describe the design. All names and "
            "trademarks belong to their respective owners.</p>")


SIZE = ("<h3>Size &amp; details</h3>\n<ul>\n<li>6 cards per pack, one design per star</li>\n"
        "<li>Each card is A6: 148 x 105 mm, landscape</li>\n<li>Printed on 350gsm premium card stock</li>\n"
        "<li>Printed reproduction – the signature is part of the printed design</li>\n</ul>\n"
        "<h3>Delivery</h3>\n<p>Printed to order in our North Yorkshire workshop. Postage options and costs are shown "
        "at checkout.</p>")

PACKS = [
 {
  "sku": "FOXY-PRESS-PDPSAPCP-01",
  "handle": "pop-divas-printed-signature-a6-poster-card-pack",
  "title": "Pop Divas Printed Signature A6 Poster Card Pack – 6 Music Star Cards (Taylor Swift, Adele, Ariana Grande, Pink, Beyoncé, Whitney Houston)",
  "names": "Taylor Swift, Adele, Ariana Grande, Pink, Beyoncé and Whitney Houston",
  "kind": "music", "channels": "all",
  "seo_title": "A6 Pop Star Poster Card Pack – 6 Cards | Foxy Printing",
  "seo_desc": "Six A6 pop star poster cards, each with a printed signature, on thick 350gsm card. A fun, low-cost gift for any music fan – order a pack today.",
  "alts": ["A6 pop star poster card pack: six music star cards laid out in a grid",
           "Six pop star poster cards with printed signatures scattered on a wall",
           "Size guide for one A6 pop star poster card, 148 x 105 mm"],
  "body": """<p>This A6 pop star poster card pack puts six of the biggest voices in music in your hand: Taylor Swift, Adele, Ariana Grande, Pink, Beyoncé and Whitney Houston. It’s a lovely little gift for the pop fan who sings into a hairbrush, and it costs less than a takeaway coffee and a cake.</p>
<p>Please note these are reproduction prints: each card carries a printed signature as part of the design.</p>
<h2>A6 pop star poster card pack</h2>
<p>Each card is a mini version of one of our best-selling music star posters, shrunk down to postcard size. You get a big main photo, four smaller shots, a name plate, a flag and the star’s signature printed into the design. They’re made to be pinned up, propped on a shelf or tucked into a scrapbook, so a whole wall of favourites doesn’t cost the earth.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Six different music star poster cards in one pack, so there’s no doubling up</li>
<li>Printed on thick 350gsm card that stands up on a shelf without curling</li>
<li>Postcard size, so they fit on a pin board, a locker door or a bedroom mirror</li>
<li>Pocket-money price for a stocking filler or party bag treat</li>
<li>Printed in-house in North Yorkshire, in the same style as our full-size posters</li>
</ul>
""",
  "close": "<p>Got a superfan? Add one of their favourite star’s full-size printed signature posters from our <a href=\"/collections/music-star-posters\">music star posters</a>, or a <a href=\"/collections/all-celebrity-mugs\">celebrity mug</a>, for a bigger gift for music fans.</p>",
 },
 {
  "sku": "FOXY-PRESS-RSPSAPCP-01",
  "handle": "rap-stars-printed-signature-a6-poster-card-pack",
  "title": "Rap Stars Printed Signature A6 Poster Card Pack – 6 Music Star Cards (Drake, Eminem, Kendrick Lamar, Stormzy, Central Cee, Dave)",
  "names": "Drake, Eminem, Kendrick Lamar, Stormzy, Central Cee and Dave",
  "kind": "music", "channels": "web",
  "seo_title": "A6 Rap Star Poster Card Pack – 6 Cards | Foxy Printing",
  "seo_desc": "Six A6 rap star poster cards from UK and US hip hop, each with a printed signature on 350gsm card. Great for bedroom walls – grab a pack today.",
  "alts": ["A6 rap star poster card pack: six hip hop star cards in a grid",
           "Six rap star poster cards with printed signatures pinned on a wall",
           "Size guide for one A6 rap star poster card, 148 x 105 mm"],
  "body": """<p>Our A6 rap star poster card pack mixes UK grime and US hip hop in one handy set: Drake, Eminem, Kendrick Lamar, Stormzy, Central Cee and Dave. Teenagers love them for bedroom walls, and they make a cheap and cheerful birthday add-on for anyone who lives with their headphones on.</p>
<p>These are reproduction prints, so the signature on each card is printed as part of the design.</p>
<h2>A6 rap star poster card pack</h2>
<p>Every card is a postcard-sized version of one of our rapper posters: a big centre photo, four smaller shots, a name plate and a printed signature, all on a black and gold background. Line all six up above a desk or decks, or pick a favourite for the fridge door.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Six different hip hop poster cards, from London to Compton</li>
<li>Thick 350gsm card, so they won’t flop when you stick them up</li>
<li>A6 size works with Blu Tack, washi tape or a small clip frame</li>
<li>A budget-friendly gift for teens and music lovers</li>
<li>Designed and printed in our own North Yorkshire workshop</li>
</ul>
""",
  "close": "<p>Want a statement piece too? Pick a full-size print from our <a href=\"/collections/music-star-posters\">music star posters</a> to sit with the cards, or browse the whole <a href=\"/collections/celebrity-posters\">celebrity posters</a> range.</p>",
 },
 {
  "sku": "FOXY-PRESS-HIPSAPCP-01",
  "handle": "hollywood-icons-printed-signature-a6-poster-card-pack",
  "title": "Hollywood Icons Printed Signature A6 Poster Card Pack – 6 Film Star Cards (Monroe, Hepburn, Kelly, Taylor, Garland, Leigh)",
  "names": "Marilyn Monroe, Audrey Hepburn, Grace Kelly, Elizabeth Taylor, Judy Garland and Vivien Leigh (and their estates)",
  "kind": "film", "channels": "all",
  "seo_title": "A6 Classic Film Star Poster Card Pack | Foxy Printing",
  "seo_desc": "Six A6 classic Hollywood film star cards with printed signatures, on thick 350gsm card. A stylish little gift for old film lovers – order yours now.",
  "alts": ["A6 classic film star poster card pack: six Hollywood actress cards in a grid",
           "Six classic Hollywood film star cards with printed signatures on a wall",
           "Size guide for one A6 film star poster card, 148 x 105 mm"],
  "body": """<p>This A6 classic film star poster card pack brings six golden-age Hollywood legends together: Marilyn Monroe, Audrey Hepburn, Grace Kelly, Elizabeth Taylor, Judy Garland and Vivien Leigh. It’s a sweet gift for Mum, Nan or anyone who never misses a Sunday afternoon black and white film.</p>
<p>Just so you know, these are reproduction prints: the signature on each card is printed into the design.</p>
<h2>A6 classic film star poster card pack</h2>
<p>Each card is a mini version of our actress posters, with a large portrait, four smaller photos, a name plate with a short line about her career, a flag and her printed signature. At postcard size they look gorgeous in a row on a dressing table, along a picture ledge or inside a vintage-style scrapbook.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Six screen icons in one pack, all different</li>
<li>Glamorous black, gold and silver design that suits a vintage look</li>
<li>Printed on 350gsm premium card, sturdy enough to prop up</li>
<li>Small enough for a card, a gift box or a Christmas stocking</li>
<li>Printed in-house in North Yorkshire</li>
</ul>
""",
  "close": "<p>For a bigger gift for film lovers, pair the pack with a full-size print from our <a href=\"/collections/film-star-posters\">film star posters</a>, which come in Premium Display frames too.</p>",
 },
 {
  "sku": "FOXY-PRESS-LLPSAPCP-01",
  "handle": "leading-ladies-printed-signature-a6-poster-card-pack",
  "title": "Leading Ladies Printed Signature A6 Poster Card Pack – 6 Film Star Cards (Robbie, Johansson, Lawrence, Roberts, Winslet, Streep)",
  "names": "Margot Robbie, Scarlett Johansson, Jennifer Lawrence, Julia Roberts, Kate Winslet and Meryl Streep",
  "kind": "film", "channels": "web",
  "seo_title": "A6 Film Actress Poster Card Pack – 6 Cards | Foxy Printing",
  "seo_desc": "Six A6 film actress poster cards with printed signatures on 350gsm card – Hollywood’s modern leading ladies in one pack. Order a set for a film fan.",
  "alts": ["A6 film actress poster card pack: six leading lady cards in a grid",
           "Six film actress poster cards with printed signatures pinned on a wall",
           "Size guide for one A6 film actress poster card, 148 x 105 mm"],
  "body": """<p>Our A6 film actress poster card pack celebrates six of today’s best-loved leading ladies: Margot Robbie, Scarlett Johansson, Jennifer Lawrence, Julia Roberts, Kate Winslet and Meryl Streep. Pop it in with a cinema voucher, or give it to the friend who always picks the film on movie night.</p>
<p>Each card is a reproduction print, with the actress’s signature printed as part of the design.</p>
<h2>A6 film actress poster card pack</h2>
<p>The cards are scaled-down versions of our actress posters: one big photo, four smaller ones, a silver name plate with a line about her films, a flag and a printed signature, framed in black and gold. Stick them round a mirror, line them up on a shelf or use them as a fun movie-night quiz prompt.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Six modern film stars in one set, each card different</li>
<li>350gsm premium card with a bold, glossy-look design</li>
<li>A6 size slots into a small frame, a gift bag or a birthday card</li>
<li>A thoughtful low-cost extra for film fans of any age</li>
<li>Made in our own workshop in North Yorkshire</li>
</ul>
""",
  "close": "<p>Pair it with the matching full-size <a href=\"/collections/film-star-posters\">film star poster</a> of their favourite, or our <a href=\"/collections/all-celebrity-mugs\">celebrity mugs</a>, for a movie-night gift set.</p>",
 },
]

out = []
for p in PACKS:
    pron = "them"
    html = p["body"] + SIZE + "\n" + p["close"] + "\n" + disclaimer(p["names"], pron)
    tags = ["A6 Card Packs", "A6 Poster Card Packs", "third-party-name", "celebrity-a6-pack", "Printed Signature",
            "cp-music" if p["kind"] == "music" else "cp-film",
            "Music Posters" if p["kind"] == "music" else "Movie Posters"]
    if p["channels"] == "web":
        tags.append("web-only-logos")
    words = len(__import__("re").sub("<[^>]+>", " ", html).split())
    out.append(dict(p, descriptionHtml=html, tags=tags, words=words))
    assert len(p["title"]) <= 150 and len(p["seo_title"]) <= 60 and 140 <= len(p["seo_desc"]) <= 155, (p["sku"], len(p["title"]), len(p["seo_title"]), len(p["seo_desc"]))
    for bad in ["Reproduction Print", "signed", "autographed", "official", "licensed", "memorabilia", "limited edition"]:
        assert bad not in p["title"], bad
        if bad != "Reproduction Print":
            assert not __import__("re").search(r"\b" + bad.lower() + r"\b", html.lower().replace("hand-signed", "")), (p["sku"], bad)
    assert "reproduction print" in html.lower() and "Reproduction Print" not in p["seo_title"]
    print(p["sku"], words, len(p["title"]), len(p["seo_title"]), len(p["seo_desc"]))
json.dump(out, open(__file__.replace("a6_packs_copy.py", "packs.json"), "w"), indent=1, ensure_ascii=False)
