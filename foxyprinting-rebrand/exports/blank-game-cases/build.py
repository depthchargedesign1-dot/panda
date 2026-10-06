"""Build productCreate inputs for the 6 blank replacement game case DRAFTS (6 Oct 2026).
Facts only from plan/product-facts.md -> "Blank replacement game cases". Unknown specs (size, material,
colour, pack sizes, dispatch time) are ASK and kept out of the copy."""
import json, re, sys, pathlib

DISCLAIMER = ('<h3>Please note</h3>\n<p class="disclaimer">This is an unofficial, fan-made replacement case produced by Foxy Printing. '
              'It is not made, endorsed or licensed by {owner}. No game, cartridge or disc is included. '
              'All trademarks and game titles belong to their respective owners and are used only to identify compatibility.</p>')

DELIVERY = ('<h3>Delivery</h3>\n<p>Your {primary} is sent from our North Yorkshire workshop in a board-backed envelope to keep them '
            'flat and safe in the post. Dispatch and postage options are shown at checkout.</p>')

P = [
 dict(code="SNES", fmt="SNES", owner="Nintendo",
  title="Blank Replacement Game Case – Fits SNES Cartridges – Empty Case, No Artwork",
  seo_title="Blank Replacement Game Case for SNES Carts | Foxy Printing",
  seo_desc="An empty replacement game case for your loose SNES cartridges. No artwork, so you can add your own cover. Sent in a board-backed envelope from Yorkshire.",
  primary="blank SNES replacement game case",
  tags=["snes", "super nintendo case", "cartridge storage"],
  body="""<p>This blank SNES replacement game case gives a loose cartridge a proper home on the shelf again. If you've picked up Super Nintendo carts at car boot sales or found a stack in the loft without their boxes, it's an easy way to tidy them up.</p>
<h2>Blank SNES Replacement Game Case</h2>
<p>You get one empty case with no artwork on it at all, so it's ready for a cover you've printed yourself, a hand-drawn label, or one of our printed covers if you'd like a matching set. There's nothing to personalise and no preview to check: just choose how many you need.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Keeps loose SNES cartridges together and off the carpet</li>
<li>Completely blank, so it suits any cover or label you choose</li>
<li>Handy for collectors filling gaps in a boxed shelf</li>
<li>A useful extra for anyone who has bought a retro console second-hand</li>
<li>Packed and posted from our North Yorkshire workshop, where we also print replacement case covers</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Format: to fit SNES cartridges</li>
<li>Sold as: one empty case</li>
<li>Artwork: none, the case is supplied blank</li>
<li>No game, cartridge, manual or cover is included</li>
</ul>
"""),
 dict(code="NES", fmt="NES", owner="Nintendo",
  title="Blank Replacement Game Case – Fits NES Cartridges – Empty Case, No Artwork",
  seo_title="Blank Replacement Game Case for NES Carts | Foxy Printing",
  seo_desc="Give loose NES cartridges a home with this empty replacement game case. Blank, so you add your own cover. Posted in a board-backed envelope from Yorkshire.",
  primary="blank NES replacement game case",
  tags=["nes", "8-bit", "cartridge storage"],
  body="""<p>A blank NES replacement game case is the simple fix for 8-bit cartridges that lost their boxes years ago. Slot a cart in, stand it on the shelf, and your collection looks like a collection again rather than a pile.</p>
<h2>Blank NES Replacement Game Case</h2>
<p>Each listing is for one empty case with no printing on it. Use it plain, slip in a cover you've made, or pick up one of our printed covers to go with it. There's nothing to type in or upload, so ordering takes seconds.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Protects bare NES cartridges from dust and knocks on the shelf</li>
<li>Plain case with no artwork, ready for your own cover</li>
<li>Lines up neatly with other cases in a retro gaming corner</li>
<li>A thoughtful add-on when you're gifting a second-hand console</li>
<li>Sent out from the same workshop that prints our retro case covers</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Format: to fit NES cartridges</li>
<li>Sold as: one empty case</li>
<li>Artwork: none, supplied blank</li>
<li>No game, cartridge, manual or cover is included</li>
</ul>
"""),
 dict(code="MD", fmt="Mega Drive and Genesis", owner="Sega",
  title="Blank Replacement Game Case – Fits Mega Drive & Genesis Cartridges – Empty Case, No Artwork",
  seo_title="Blank Retro Game Case for Mega Drive Carts | Foxy Printing",
  seo_desc="An empty replacement game case to store loose Mega Drive and Genesis cartridges. Blank and ready for your own cover, posted in a board-backed envelope.",
  primary="blank Mega Drive replacement game case",
  tags=["mega drive", "genesis", "16-bit", "cartridge storage"],
  body="""<p>Our blank Mega Drive replacement game case is made for the 16-bit cartridges that turn up without a box. Whether you're rebuilding a childhood collection or sorting out a bundle you bought online, it keeps each game tidy and easy to find.</p>
<h2>Blank Mega Drive Replacement Game Case</h2>
<p>This is one empty case to fit Mega Drive and Genesis cartridges, with no artwork. Leave it plain, add a label of your own, or team it with one of our printed covers. There are no personalisation boxes on this one: just add it to your basket.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Gives unboxed Mega Drive and Genesis carts somewhere safe to live</li>
<li>No printing at all, so any cover or spine label will suit it</li>
<li>Makes a shelf of mixed games look uniform</li>
<li>Good value way to bulk out a collection display</li>
<li>Posted from our print workshop in North Yorkshire</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Format: to fit Mega Drive and Genesis cartridges</li>
<li>Sold as: one empty case</li>
<li>Artwork: none, supplied blank</li>
<li>No game, cartridge, manual or cover is included</li>
</ul>
"""),
 dict(code="SMS", fmt="Master System", owner="Sega",
  title="Blank Replacement Game Case – Fits Master System Cartridges – Empty Case, No Artwork",
  seo_title="Blank Retro Game Case for Master System | Foxy Printing",
  seo_desc="Store loose Master System cartridges in this empty replacement game case. No artwork, ready for your own cover, and sent in a board-backed envelope.",
  primary="blank Master System replacement game case",
  tags=["master system", "8-bit", "cartridge storage"],
  body="""<p>This blank Master System replacement game case is for the Sega fans whose carts have been rattling around in a drawer since the 80s. Pop each one in its own case and the collection is protected, tidy and easy to browse again.</p>
<h2>Blank Master System Replacement Game Case</h2>
<p>You're buying one empty case, sized for Master System cartridges, with nothing printed on it. Keep it plain or add a cover of your choice, including one of the printed covers from our range. There's no text to enter, so it's a quick order.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Stops loose Master System carts getting scratched and lost</li>
<li>Blank front and spine for your own artwork or labels</li>
<li>Helps a part-boxed collection look complete on the shelf</li>
<li>Ideal when you've bought a job lot of unboxed games</li>
<li>Sent from our North Yorkshire workshop alongside our retro case covers</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Format: to fit Master System cartridges</li>
<li>Sold as: one empty case</li>
<li>Artwork: none, supplied blank</li>
<li>No game, cartridge, manual or cover is included</li>
</ul>
"""),
 dict(code="GB", fmt="Game Boy and Game Boy Color", owner="Nintendo",
  title="Blank Replacement Game Case – Fits Game Boy & Game Boy Color Cartridges – Empty Case, No Artwork",
  seo_title="Blank Handheld Game Case for Game Boy Carts | Foxy Printing",
  seo_desc="An empty replacement game case for loose Game Boy and Game Boy Color cartridges. Blank for your own cover and posted in a board-backed envelope.",
  primary="blank Game Boy replacement game case",
  tags=["game boy", "game boy color", "handheld", "cartridge storage"],
  body="""<p>A blank Game Boy replacement game case is the answer to those tiny cartridges that always seem to go missing. Give each one its own case and they'll stay together on the shelf instead of hiding down the back of the sofa.</p>
<h2>Blank Game Boy Replacement Game Case</h2>
<p>This listing is one empty case to fit Game Boy and Game Boy Color cartridges. It comes with no artwork, so you can leave it clean, add your own cover, or choose a printed cover from our handheld range. Nothing needs personalising.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Keeps small handheld cartridges from getting lost</li>
<li>Plain case that works with any cover or label</li>
<li>Turns a tin of loose carts into a proper display</li>
<li>Nice extra to tuck in with a second-hand handheld as a gift</li>
<li>Packed by a North Yorkshire workshop that prints retro case covers</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Format: to fit Game Boy and Game Boy Color cartridges</li>
<li>Sold as: one empty case</li>
<li>Artwork: none, supplied blank</li>
<li>No game, cartridge, manual or cover is included</li>
</ul>
"""),
 dict(code="PS1", fmt="PS1", owner="Sony",
  title="Blank Replacement Game Case – Fits PS1 Game Discs – Empty Case, No Artwork",
  seo_title="Blank Replacement Disc Game Case for PS1 | Foxy Printing",
  seo_desc="Replace a cracked or missing case with this empty replacement game case for PS1 discs. Blank for your own cover, sent in a board-backed envelope.",
  primary="blank PS1 replacement game case",
  tags=["ps1", "playstation 1", "disc storage"],
  body="""<p>This blank PS1 replacement game case is for the discs that ended up in a spindle, a wallet or a cracked old box. Give them a fresh case and they're protected from scratches and back on the shelf where they belong.</p>
<h2>Blank PS1 Replacement Game Case</h2>
<p>You get one empty case for PS1 game discs, with no artwork printed on it. Use your own cover, leave it plain, or match it with a printed cover from our range. There are no options to fill in, so it's a simple order.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Swap out cracked or missing cases in a few seconds</li>
<li>Helps keep loose discs away from scratches</li>
<li>Blank, so your own cover or label fits right in</li>
<li>Makes a shelf of 90s favourites look tidy again</li>
<li>Sent from our UK workshop, home to a big range of retro case covers</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Format: to fit PS1 game discs</li>
<li>Sold as: one empty case</li>
<li>Artwork: none, supplied blank</li>
<li>No game, disc, manual or cover is included</li>
</ul>
"""),
]

CLOSING = {
 "SNES": "<p>Want to make it really special? Pair it with our personalised video game case, where you put yourself on the cover, for a retro gamer gift with a twist.</p>",
 "NES": "<p>Looking for a gamer gift instead? Our personalised video game case puts a photo of them on the cover of their very own game.</p>",
 "MD": "<p>Sorting out a retro gaming shelf? Add a personalised video game case with their photo on the cover for a fun one-off.</p>",
 "SMS": "<p>For a cartridge storage case with a bit more personality, take a look at our personalised video game case with your own photo on the front.</p>",
 "GB": "<p>Buying for a handheld fan? Pair a few blank cases with our personalised video game case, where they're the star of the cover.</p>",
 "PS1": "<p>Want a gamer gift too? Our personalised video game case puts their photo on the cover of a game that's all about them.</p>",
}

def words(h): return len(re.sub(r"<[^>]+>", " ", h).split())

out = []
for i, p in enumerate(P, 1):
    html = p["body"].strip() + "\n" + DELIVERY.format(primary=p["primary"]) + "\n" + CLOSING[p["code"]] + "\n" + DISCLAIMER.format(owner=p["owner"])
    sku = f"FOXY-BLANK-BRGC{p['code']}-01"
    w = words(html); first = re.sub('<[^>]+>', '', html.split('</p>')[0])
    assert p["primary"].lower() in first.lower(), p["code"]
    assert len(p["seo_title"]) <= 60, (p["seo_title"], len(p["seo_title"]))
    assert 140 <= len(p["seo_desc"]) <= 155, (p["code"], len(p["seo_desc"]))
    assert len(p["title"]) <= 150
    assert html.lower().count(p["primary"].lower()) >= 3, (p["code"], html.lower().count(p["primary"].lower()))
    assert 180 <= w <= 350, (p["code"], w)
    for bad in ("official", "licensed merch", "authentic", "genuine", "approved", "merchandise"):
        assert bad not in html.lower().replace("unofficial", ""), (p["code"], bad)
    handle = "blank-replacement-game-case-" + {"SNES":"snes","NES":"nes","MD":"mega-drive","SMS":"master-system","GB":"game-boy","PS1":"ps1"}[p["code"]]
    tags = ["blank game case", "replacement game case", "retro gaming", "empty game case", "third-party-name",
            "foxy-new-2026", "dept-fan-shop-retro", "range-blank-game-cases"] + p["tags"]
    out.append(dict(code=p["code"], handle=handle, sku=sku, words=w, seo_title_len=len(p["seo_title"]), seo_desc_len=len(p["seo_desc"]),
      input=dict(title=p["title"], handle=handle, descriptionHtml=html, productType="Blank Replacement Game Cases",
        vendor="Foxy Printing", status="DRAFT", tags=tags, seo=dict(title=p["seo_title"], description=p["seo_desc"]),
        metafields=[
          dict(namespace="mm-google-shopping", key="custom_product", type="boolean", value="true"),
          dict(namespace="mm-google-shopping", key="condition", type="single_line_text_field", value="new"),
          dict(namespace="mm-google-shopping", key="google_product_category", type="single_line_text_field", value="Electronics > Video Game Console Accessories"),
          dict(namespace="mm-google-shopping", key="gender", type="single_line_text_field", value="unisex"),
          dict(namespace="mm-google-shopping", key="age_group", type="single_line_text_field", value="adult"),
          dict(namespace="mm-google-shopping", key="mpn", type="single_line_text_field", value=sku),
        ])))
    print(p["code"], w, len(p["seo_title"]), len(p["seo_desc"]), len(p["title"]), sku, handle)
pathlib.Path(__file__).with_name("products.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
