"""The new 3-level mega menu (Online Store → Navigation → "Foxy Mega Menu", handle foxy-mega-menu).

Level 1 = department in the bar, level 2 = column heading, level 3 = links.
Handles starting with `new-` are the unpublished smart collections created for the new ranges;
everything else is an existing collection on foxyprinting.co.uk.
"""


def c(handle):
    return f"/collections/{handle}"


BASE_MENU = [
    ("Christmas", c("christmas-novelty-gifts"), [
        ("Christmas Eve & Advent", c("new-christmas-eve-boxes"), [
            ("Christmas Eve Boxes", c("new-christmas-eve-boxes")),
            ("Advent Calendars", c("new-christmas-eve-boxes")),
            ("Selection Box Sleeves", c("new-christmas-eve-boxes")),
            ("Letters from Santa", c("new-christmas-eve-boxes")),
        ]),
        ("Decorations", c("new-christmas-baubles"), [
            ("Name Baubles", c("new-christmas-baubles")),
            ("Photo Baubles", c("new-christmas-baubles")),
            ("Santa's Magic Key", c("new-christmas-baubles")),
            ("Wooden Tree Decorations", c("new-wooden-gifts")),
        ]),
        ("Christmas Clothing", c("new-christmas-clothing"), [
            ("Family Christmas Jumpers", c("new-christmas-clothing")),
            ("Christmas Pyjamas", c("new-christmas-clothing")),
            ("Baby's First Christmas", c("new-christmas-clothing")),
        ]),
        ("Stockings & Sacks", c("personalised-custom-christmas-stockings"), [
            ("Personalised Stockings", c("personalised-custom-christmas-stockings")),
            ("Santa Sacks", c("printed-santa-sacks")),
            ("Superhero Santa Sacks", c("superhero-cartoon-santa-sacks")),
        ]),
        ("Christmas Gifts", c("christmas-novelty-gifts"), [
            ("Christmas & Novelty Gifts", c("christmas-novelty-gifts")),
            ("Rude Wrapping Paper", c("wrapping-paper")),
            ("Gift Tags", c("new-papercraft")),
        ]),
    ]),
    ("Cards & Invitations", c("all-cards"), [
        ("Birthday Cards", c("all-cards"), [
            ("Kids' Cards", c("kids-cards")), ("Adult Cards", c("adult-cards")), ("Funny Cards", c("funny-cards")),
            ("Animal Cards", c("animal-cards")), ("Car Cards", c("car-cards")), ("Sports Cards", c("sports-cards")),
            ("Gaming Cards", c("gaming-cards")), ("Music Cards", c("musician-cards")), ("Celebrity Cards", c("celebrity-cards")),
        ]),
        ("Occasion Cards", c("all-cards"), [
            ("Valentine's Cards", c("valentines-day-card")), ("Father's Day Cards", c("fathers-day-cards")),
            ("Thank You Cards", c("thank-you-cards")), ("Pop-Up 3D Cards", c("new-papercraft")),
        ]),
        ("Invitations", c("invitation-cards"), [
            ("Party Invites", c("party-invites")), ("Kids' Party Invitations", c("girls-invites")),
            ("Christening Invites", c("christening-invites")), ("Engagement Invites", c("engagement-invites")),
            ("Wedding Invitations", c("new-weddings")),
        ]),
        ("Party Printing", c("all-party-printing"), [
            ("Party Bunting", c("party-buntin")), ("Birthday Banners", c("birthday-banners")),
            ("Cake Toppers", c("new-papercraft")), ("Bottle Labels", c("fruit-shoot-bottle-labels")),
            ("Wine & Alcohol Labels", c("alcohol-labels")),
        ]),
    ]),
    ("Personalised Gifts", c("popular-personalised"), [
        ("Photo Gifts", c("new-acrylic-photo-gifts"), [
            ("Acrylic Photo Blocks", c("new-acrylic-photo-gifts")), ("LED Night Lights", c("new-acrylic-photo-gifts")),
            ("Slate Gifts", c("new-slate-stone-gifts")), ("Wooden Gifts", c("new-wooden-gifts")),
            ("Personalised Prints", c("all-personalised-prints")), ("Word Art Prints", c("personalised-word-art-prints")),
        ]),
        ("Keyrings & Magnets", c("new-acrylic-photo-gifts"), [
            ("Photo Keyrings", c("new-acrylic-photo-gifts")), ("Photo Fridge Magnets", c("new-acrylic-photo-gifts")),
            ("Retro Gaming Keyrings", c("all-retro-gaming-keyrings")), ("Retro Gaming Magnets", c("retro-gaming-magnets")),
        ]),
        ("Gifts for Him", c("fathers-day-gifts-1"), [
            ("Golf & Darts", c("new-golf-gifts")), ("Whisky & Pint Glasses", c("new-glassware")),
            ("Bar Mats", c("personalised-bar-mats")), ("Father's Day Gifts", c("fathers-day-gifts-1")),
        ]),
        ("Gifts for Her", c("new-candles-jars"), [
            ("Gin & Wine Glasses", c("new-glassware")), ("Candles & Jars", c("new-candles-jars")),
            ("Glass Can Cups", c("new-glass-can-cups")), ("Unicorn Cushions", c("unicorn-magic-cushions")),
        ]),
        ("Tech & Desk", c("new-tech-accessories"), [
            ("Phone Cases", c("new-tech-accessories")), ("Mouse Mats", c("printed-mouse-mats")),
            ("Controller Skins", c("new-gamer-skins")), ("Notebooks", c("new-tech-accessories")),
        ]),
    ]),
    # Photo gift range made on sublimation blanks (plan/longforte-plan.md).
    ("Photo Gifts", c("personalised-photo-slates"), [
        ("Photo Prints & Wall Art", c("personalised-photo-slates"), [
            ("Photo Slates", c("personalised-photo-slates")),
            ("Metal Photo Panels", c("personalised-metal-photo-panels")),
            ("Photo Clocks & Glass Frames", c("personalised-clocks-and-glass-photo-frames")),
            ("Photo Plaques & Ceramic Tiles", c("personalised-photo-plaques-and-ceramic-tiles")),
        ]),
        ("Home & Table", c("personalised-cushions-and-home-textiles"), [
            ("Cushions, Blankets & Aprons", c("personalised-cushions-and-home-textiles")),
            ("Coasters & Placemats", c("personalised-coasters-and-placemats")),
            ("Photo Jigsaws", c("personalised-photo-jigsaws")),
        ]),
        ("Drinkware", c("personalised-travel-mugs-tumblers-and-bottles"), [
            ("Tumblers, Travel Mugs & Bottles", c("personalised-travel-mugs-tumblers-and-bottles")),
            ("Enamel, Latte & Speciality Mugs", c("personalised-enamel-latte-and-speciality-mugs")),
        ]),
        ("Little Gifts", c("personalised-keyrings-and-fridge-magnets"), [
            ("Keyrings & Fridge Magnets", c("personalised-keyrings-and-fridge-magnets")),
            ("Teddy Bears & Plush Toys", c("personalised-teddy-bears-and-plush-toys")),
            ("Kids & Back to School", c("personalised-kids-and-back-to-school")),
            ("Pet Gifts", c("personalised-pet-gifts")),
            ("Christmas Baubles & Ornaments", c("personalised-christmas-baubles-and-ornaments")),
        ]),
    ]),
    # Team kit, flags and fan gifts for grassroots clubs (plan/product-facts.md, football sheet).
    ("Football", c("personalised-football-merchandise"), [
        ("Team Kit", c("personalised-team-footballs-and-kit"), [
            ("Personalised Footballs", c("personalised-team-footballs-and-kit")),
            ("Kids' Shin Pads", c("personalised-team-footballs-and-kit")),
            ("Football Socks", c("personalised-team-footballs-and-kit")),
            ("Boot Bags", c("personalised-team-footballs-and-kit")),
        ]),
        ("Scarves & Bobble Hats", c("personalised-football-scarves-and-bobble-hats"), [
            ("Custom Satin Scarves", c("personalised-football-scarves-and-bobble-hats")),
            ("Knitted Bobble Hats", c("personalised-football-scarves-and-bobble-hats")),
            ("Printed Badge Scarves", c("scarves")),
            ("Printed Badge Bobble Hats", c("bobble-hats")),
        ]),
        ("Flags", c("custom-football-stadium-and-corner-flags"), [
            ("Stadium Flags", c("custom-football-stadium-and-corner-flags")),
            ("Corner Flags", c("custom-football-stadium-and-corner-flags")),
            ("Car Flags", c("custom-football-stadium-and-corner-flags")),
            ("Club Bunting", c("custom-football-stadium-and-corner-flags")),
            ("Terrace Flags", c("football-flags")),
        ]),
        ("Coach & Team Gifts", c("football-coach-and-team-gifts"), [
            ("Thank You Coach Mugs", c("football-coach-and-team-gifts")),
            ("Coach Keyrings", c("football-coach-and-team-gifts")),
            ("Team Pennants", c("football-coach-and-team-gifts")),
        ]),
        ("Fan Favourites", c("all-football-mugs"), [
            ("Football Team Mugs", c("all-football-mugs")),
            ("Football Posters", c("football-posters")),
            ("Football Coasters", c("football-coasters")),
            ("Football Bar Mats", c("football-bar-mats")),
            ("Football Towels", c("football-bath-towels")),
            ("Footballer Face Masks", c("footballer-face-masks")),
        ]),
    ]),
    ("Clothing", c("t-shirts"), [
        ("T-Shirts & Hoodies", c("new-custom-clothing"), [
            ("Design Your Own T-Shirt", c("new-custom-clothing")), ("Printed T-Shirts", c("t-shirts")),
            ("Hoodies", c("hoodies")), ("Gaming T-Shirts", c("gaming-t-shirts")), ("Pride Clothing", c("pride-t-shirts")),
        ]),
        ("Parties", c("hen-doo-t-shirts"), [
            ("Hen Do T-Shirts", c("hen-doo-t-shirts")), ("Stag Do T-Shirts", c("stag-doo-t-shirts")),
            ("Party Sashes", c("new-bags-aprons-textiles")),
        ]),
        ("School & Clubs", c("new-school-leavers"), [
            ("Leavers Hoodies", c("new-school-leavers")), ("Club & Team Hoodies", c("new-school-leavers")),
            ("Captain's Armbands", c("custom-captains-armbands")),
        ]),
        ("Bags & Accessories", c("new-bags-aprons-textiles"), [
            ("Tote & PE Bags", c("new-bags-aprons-textiles")), ("Aprons", c("new-bags-aprons-textiles")),
            ("Bobble Hats", c("bobble-hats")), ("Scarves", c("scarves")),
        ]),
    ]),
    ("Baby & Kids", c("baby-vests"), [
        ("Baby", c("baby-vests"), [
            ("Baby Grows", c("baby-vests")), ("Bibs, Vests & Blankets", c("new-baby-clothing")),
            ("New Baby Keepsakes", c("new-new-baby")), ("Milestone Discs", c("new-wooden-gifts")),
        ]),
        ("School & Nursery", c("new-kids-labels-bottles"), [
            ("Name Labels", c("new-kids-labels-bottles")), ("Lunch Boxes", c("personalised-lunchboxes")),
            ("Water Bottles", c("new-kids-labels-bottles")), ("PE Bags", c("new-bags-aprons-textiles")),
        ]),
        ("Kids' Gifts", c("personalised-teddys"), [
            ("Teddy Bears", c("personalised-teddys")), ("Kids' Towels", c("personalised-bath-towels")),
            ("Birthday T-Shirts", c("new-custom-clothing")), ("Game Case Gifts", c("new-custom-game-cases")),
        ]),
        ("Kids' Parties", c("all-party-printing"), [
            ("Party Invitations", c("girls-invites")), ("Bunting", c("party-buntin")), ("Favour Boxes", c("new-party-boxes")),
        ]),
    ]),
    ("Pets", c("personalised-pet-products"), [
        ("Pet Accessories", c("new-pet-clothing"), [
            ("Bandanas & Hoodies", c("new-pet-clothing")), ("ID Tags", c("new-pet-clothing")),
            ("Bowls & Treat Jars", c("new-pet-clothing")), ("Dog Bowl Mats", c("personalised-dog-bowl-mats")),
        ]),
        ("Pet Gifts", c("personalised-pet-products"), [
            ("Pet Portraits", c("new-pet-clothing")), ("Pet Blankets", c("new-pet-clothing")),
            ("Pet Memorials", c("new-memorial")), ("Pet Christmas", c("new-christmas-baubles")),
        ]),
    ]),
    ("Home & Drinkware", c("mugs"), [
        ("Mugs", c("mugs"), [
            ("Name Mugs", c("personalised-name-mugs")), ("Funny Mugs", c("funny-mugs-1")),
            ("Job & Occupation Mugs", c("occupational-mugs")), ("Football Team Mugs", c("all-football-mugs")),
            ("Celebrity Mugs", c("all-celebrity-mugs")), ("Birthday Mugs", c("this-is-my-birthday-mug")),
            ("Rude Mugs", c("adult-mugs-rude")), ("Full-Wrap Mugs", c("full-wrap-mugs")),
        ]),
        ("Cups, Tumblers & Glasses", c("new-glass-can-cups"), [
            ("Glass Can Cups", c("new-glass-can-cups")), ("40oz Tumblers", c("new-glass-can-cups")),
            ("Water Bottles", c("new-glass-can-cups")), ("Gin, Wine & Pint Glasses", c("new-glassware")),
        ]),
        ("Home", c("drinks-coaster"), [
            ("Towels", c("personalised-bath-towels")), ("Sports Towels", c("football-bath-towels")),
            ("Coasters", c("drinks-coaster")), ("Bar Mats", c("bar-mats")), ("Slate & Stone", c("new-slate-stone-gifts")),
            ("Candles", c("new-candles-jars")), ("Cushions", c("celebrity-cushions")),
        ]),
        ("Wall Art", c("posters-canvas-art"), [
            ("Posters & Canvas", c("posters-canvas-art")), ("Signed Prints", c("signed-autographed-prints")),
            ("Word Art Prints", c("personalised-word-art-prints")),
        ]),
    ]),
    ("Occasions", c("occasion-birthday"), [
        ("Celebrations", c("occasion-birthday"), [
            ("Birthdays", c("occasion-birthday")), ("Weddings", c("new-weddings")),
            ("New Baby", c("new-new-baby")), ("Engagements", c("engagement-invites")),
        ]),
        ("Seasonal", c("new-halloween"), [
            ("Halloween", c("new-halloween")), ("Valentine's & Mother's Day", c("new-valentines-mothers-day")),
            ("Easter", c("new-easter")), ("Father's Day", c("fathers-day-gifts-1")), ("Pride", c("occasion-pride")),
        ]),
        ("Remembrance", c("new-memorial"), [("Memorial Gifts", c("new-memorial"))]),
        ("Parties", c("all-party-printing"), [
            ("Stag & Hen", c("stag-hen-party-face-masks")), ("Party Printing", c("all-party-printing")),
        ]),
    ]),
    ("Boxes & Packaging", c("new-gift-packaging"), [
        ("Gift Boxes", c("new-gift-packaging"), [
            ("Christmas Eve Boxes", c("new-christmas-eve-boxes")), ("Letterbox Gifts", c("new-gift-packaging")),
            ("Golf Ball Boxes", c("new-gift-packaging")), ("Mug Gift Boxes", c("new-gift-packaging")),
        ]),
        ("Party Boxes", c("new-party-boxes"), [
            ("Cupcake Boxes", c("new-party-boxes")), ("Favour Boxes", c("new-party-boxes")),
            ("Popcorn Boxes", c("new-party-boxes")), ("Treat Boxes", c("new-party-boxes")),
        ]),
        ("Game Cases", c("new-custom-game-cases"), [
            ("Put Yourself on a Game Case", c("new-custom-game-cases")),
            ("Replacement Game Cases", c("all-replacement-game-cases")),
        ]),
        ("For Business", c("new-gift-packaging"), [("Printed Mailer Boxes", c("new-gift-packaging"))]),
    ]),
    ("Business Printing", c("business-cards"), [
        ("Stationery", c("business-cards"), [
            ("Business Cards", c("business-cards")), ("Premium & Spot-Gloss Cards", c("new-business-stationery")),
            ("Flyers & Leaflets", c("new-business-stationery")), ("Loyalty Cards", c("loyalty-cards")),
            ("Thank You Cards", c("loyalty-and-thank-you-cards")), ("Address Labels", c("address-labels")),
        ]),
        ("Stickers & Labels", c("new-stickers-labels"), [
            ("Custom Stickers", c("new-stickers-labels")), ("Product Labels", c("new-stickers-labels")),
            ("Vinyl Car Decals", c("car-stickers")),
        ]),
        ("Signs & Awards", c("new-signs-displays"), [
            ("QR & Review Stands", c("new-signs-displays")), ("Awards & Medals", c("new-awards-plaques")),
        ]),
        ("Branded Clothing & Trade", c("new-workwear"), [
            ("Workwear & Teamwear", c("new-workwear")), ("DTF & UV DTF Transfers", c("new-craft-supplies")),
        ]),
    ]),
    ("Fan Shop & Retro", c("all-retro-gaming"), [
        ("Retro Gaming", c("all-retro-gaming"), [
            ("Replacement Game Cases", c("all-replacement-game-cases")), ("Retro Game Posters", c("all-retro-game-posters")),
            ("Keyrings", c("all-retro-gaming-keyrings")), ("Magnets", c("retro-gaming-magnets")),
            ("Controller Skins", c("new-gamer-skins")), ("PerfectDraft Skins", c("perfect-skins")),
        ]),
        ("Celebrity Face Masks", c("all-facemasks"), [
            ("All Face Masks", c("all-facemasks")), ("Footballers", c("footballer-face-masks")),
            ("TV Stars", c("tv-star-masks")), ("Movie Actors", c("movie-actor-face-masks")),
            ("Your Own Face", c("custom-printed-face-masks")),
        ]),
        ("Sports Fans", c("football-posters"), [
            ("Football Posters", c("football-posters")), ("Signed Prints", c("signed-autographed-prints")),
            ("Football Coasters", c("football-coasters")), ("Football Flags", c("football-flags")),
        ]),
    ]),
]



def _with_extra(menu):
    """Append the generated "More …" columns (plan/menu_extra.json) to their departments."""
    import json
    from pathlib import Path
    path = Path(__file__).with_name("menu_extra.json")
    extra = json.loads(path.read_text()) if path.exists() else {}
    out = []
    for title, url, cols in menu:
        more = [(col, links[0][1], [tuple(link) for link in links]) for col, links in extra.get(title, {}).items()]
        out.append((title, url, list(cols) + more))
    return out


MENU = _with_extra(BASE_MENU)


def as_json():
    return [{"title": t, "url": u, "items": [{"title": t2, "url": u2, "items": [{"title": t3, "url": u3} for t3, u3 in kids]}
                                             for t2, u2, kids in cols]} for t, u, cols in MENU]


def as_menu_input():
    """MenuItemCreateInput tree for the Admin API menuCreate mutation."""
    def item(title, url, children=()):
        d = {"title": title, "type": "HTTP", "url": url}
        if children:
            d["items"] = children
        return d
    return [item(t, u, [item(t2, u2, [item(t3, u3) for t3, u3 in kids]) for t2, u2, kids in cols]) for t, u, cols in MENU]
