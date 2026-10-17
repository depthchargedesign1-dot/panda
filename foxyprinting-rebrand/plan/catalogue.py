"""Single source of truth for the Foxy Printing new-product plan.

Every new product line lives here once. `tools/build_plan.py` turns this into:
  * plan/new-products-shopify-import.csv  (Shopify product CSV, all DRAFT)
  * plan/new-product-plan.md              (the human-readable plan)
  * tools/out/*.json                      (batches used to create drafts via the Admin API)

Prices are suggested UK RRPs (GBP, inc. VAT) benchmarked against Vistaprint UK,
Etsy UK bestsellers and Not On The High Street. Review before publishing.
"""

# Machines -------------------------------------------------------------------
MACHINES = {
    "UV": "Roland VersaUV LEF-300 (UV flatbed, 762 x 330 mm bed, up to 100 mm tall, CMYK + white + gloss)",
    "UVDTF": "UV DTF printer (cured transfers applied to glass, metal, plastic & curved surfaces)",
    "DTF": "DTF clothing printer (heat-press transfers for cotton, poly, blends, fleece, canvas)",
    "CUT": "Flatbed digital cutter (boxes, packaging, die-cut cards, stickers, game cases)",
    "PRESS": "Existing digital press / mug & sublimation kit (cards, paper, mugs, existing lines)",
}

# Launch waves ----------------------------------------------------------------
WAVES = {
    1: "Wave 1 - Christmas 2026 (live by 31 Oct 2026; last-order date ~18 Dec)",
    2: "Wave 2 - Valentine's, Mother's Day (UK: 7 Mar 2027) & Easter (28 Mar 2027) - live by 10 Jan 2027",
    3: "Wave 3 - Spring/Summer 2027: weddings, Father's Day (20 Jun 2027), teacher thank-yous & school leavers - live by 1 Apr 2027",
    0: "Always-on - core range, launch as soon as samples are approved",
}

# Mega-menu departments (top level of the new navigation) ---------------------
DEPARTMENTS = [
    "Cards & Invitations",
    "Personalised Gifts",
    "Clothing",
    "Baby & Kids",
    "Pets",
    "Home & Drinkware",
    "Occasions",
    "Boxes & Packaging",
    "Business Printing",
    "Fan Shop & Retro",
]

# Ranges: handle, title, department, blurb ------------------------------------
RANGES = [
    # UV flatbed
    ("acrylic-photo-gifts", "Acrylic Photo Gifts", "Personalised Gifts", "Crystal-clear acrylic blocks, plaques and night lights printed edge-to-edge with white + gloss."),
    ("slate-stone-gifts", "Slate & Stone Gifts", "Home & Drinkware", "Natural slate printed in full colour - coasters, plaques, house signs and memorials."),
    ("wooden-gifts", "Wooden Gifts & Keepsakes", "Personalised Gifts", "Birch, oak-effect and bamboo pieces printed direct with UV ink."),
    ("golf-gifts", "Golf & Darts Gifts", "Personalised Gifts", "Printed golf balls, markers and dart flights - perfect for Father's Day and club prizes."),
    ("tech-accessories", "Phone Cases & Tech", "Personalised Gifts", "Phone cases, chargers, power banks and desk accessories."),
    ("awards-plaques", "Awards, Medals & Plaques", "Business Printing", "Club awards, medal inserts and recognition plaques."),
    # UV DTF
    ("glass-can-cups", "Glass Can Cups & Tumblers", "Home & Drinkware", "The cup of the moment: glass cans, 40oz tumblers and bottles with permanent UV DTF names."),
    ("glassware", "Personalised Glassware", "Home & Drinkware", "Gin, wine, pint and whisky glasses with dishwasher-tough UV DTF prints."),
    ("christmas-baubles", "Personalised Baubles & Decorations", "Occasions", "Name baubles, photo ornaments, Santa keys and memorial decorations."),
    ("candles-jars", "Candles & Jars", "Home & Drinkware", "Personalised candles, sweet jars and treat tins."),
    ("kids-labels-bottles", "School Labels, Bottles & Lunchboxes", "Baby & Kids", "Waterproof name labels, bottles and lunchboxes for nursery and school."),
    ("gamer-skins", "Controller & Console Skins", "Fan Shop & Retro", "UV DTF decals for controllers, consoles, laptops and PerfectDraft machines."),
    ("craft-supplies", "UV DTF & DTF Transfers (Trade)", "Business Printing", "Ready-to-apply transfers and gang sheets for crafters and print shops."),
    # DTF clothing
    ("custom-clothing", "Custom T-Shirts & Hoodies", "Clothing", "Full-colour DTF printing on tees, hoodies and sweats - no minimum order."),
    ("school-leavers", "School Leavers & Club Hoodies", "Clothing", "Leavers hoodies with every name on the back, plus club and team wear."),
    ("christmas-clothing", "Christmas Jumpers & Pyjamas", "Occasions", "Matching family Christmas jumpers, PJs and Christmas Eve tees."),
    ("baby-clothing", "Baby Clothing & Keepsakes", "Baby & Kids", "Baby grows, bibs, vests and announcement tees."),
    ("pet-clothing", "Pet Bandanas & Accessories", "Pets", "Bandanas, dog hoodies, pet blankets, ID tags and bowls."),
    ("bags-aprons-textiles", "Bags, Aprons & Textiles", "Clothing", "Totes, PE bags, aprons, caps and party sashes."),
    ("workwear", "Workwear & Teamwear", "Business Printing", "Logo polos, hi-vis, kit names & numbers."),
    # Cutter
    ("christmas-eve-boxes", "Christmas Eve Boxes & Advent Calendars", "Boxes & Packaging", "Personalised Christmas Eve boxes, fill-your-own advent calendars and selection box sleeves."),
    ("party-boxes", "Party, Favour & Treat Boxes", "Boxes & Packaging", "Cupcake, favour, pillow and popcorn boxes printed to match your party."),
    ("gift-packaging", "Gift Boxes & Letterbox Gifts", "Boxes & Packaging", "Mug boxes, bauble boxes, golf ball boxes and letterbox gifts."),
    ("custom-game-cases", "Custom Video Game Cases", "Fan Shop & Retro", "Put anyone on the cover of their own video game - plus our 3,300+ replacement cases."),
    ("papercraft", "Cake Toppers, 3D Cards & Party Paper", "Cards & Invitations", "Die-cut cake toppers, pop-up cards, photo booth props and gift tags."),
    # Business (Vistaprint parity)
    ("business-stationery", "Business Cards & Stationery", "Business Printing", "Premium business cards (spot-gloss, metal, rounded), flyers, leaflets and more."),
    ("stickers-labels", "Stickers & Product Labels", "Business Printing", "Die-cut stickers, kiss-cut sheets and product labels for small businesses."),
    ("signs-displays", "Signs, QR & Review Stands", "Business Printing", "Acrylic QR/tap-to-review stands, door signs and small-format signage."),
    # Seasonal / special days (cross-machine)
    ("halloween", "Halloween", "Occasions", "Trick-or-treat bags, spooky tees, treat boxes and party printing."),
    ("valentines-mothers-day", "Valentine's & Mother's Day", "Occasions", "Love-themed keepsakes for Valentine's and Mother's Day."),
    ("easter", "Easter", "Occasions", "Egg hunt kits, Easter bags and egg boxes."),
    ("weddings", "Weddings & Engagements", "Occasions", "Welcome signs, table numbers, favours and stationery."),
    ("memorial", "Memorial & Remembrance", "Occasions", "Gentle, beautifully printed keepsakes for loved ones and pets."),
    ("new-baby", "New Baby & Pregnancy", "Baby & Kids", "Announcements, milestone cards and birth keepsakes."),
]

# Products --------------------------------------------------------------------
# (range_handle, title, machine, wave, trend(1-5), [ (option_value, price) ...] or price, personalisation fields, notes)
# option name defaults to "Size"; use a tuple ("Option name", [(value, price), ...]) to override.

P = []


def add(range_handle, title, machine, wave, trend, variants, personalise, notes=""):
    P.append(dict(range=range_handle, title=title, machine=machine, wave=wave, trend=trend,
                  variants=variants, personalise=personalise, notes=notes))


NAME = ["Name"]
NAME_MSG = ["Name", "Message"]
PHOTO_NAME = ["Photo upload", "Name"]
PHOTO_MSG = ["Photo upload", "Message"]

# --- UV flatbed: acrylic -------------------------------------------------------
add("acrylic-photo-gifts", "Personalised Acrylic Photo Block", "UV", 0, 5,
    [("10 x 15 cm", 19.99), ("15 x 15 cm", 22.99), ("15 x 20 cm", 26.99)], PHOTO_MSG,
    "20 mm freestanding acrylic; print reverse with white flood for vivid colour.")
add("acrylic-photo-gifts", "Our Song Acrylic Music Plaque", "UV", 1, 5,
    [("A5 with stand", 17.99), ("A4 with stand", 24.99)], ["Photo upload", "Song title", "Artist", "Names"],
    "Big TikTok/Etsy trend. Avoid platform logos/trademarks; render our own player design.")
add("acrylic-photo-gifts", "Personalised LED Acrylic Night Light", "UV", 1, 5,
    [("Warm white base", 24.99), ("Colour-changing base", 29.99)], PHOTO_NAME,
    "Engrave-look via white ink layer on 5 mm acrylic slotted into USB LED base.")
add("acrylic-photo-gifts", "Personalised Photo Fridge Magnet (Acrylic)", "UV", 0, 4,
    [("Single", 4.99), ("Set of 4", 14.99), ("Set of 9", 27.99)], PHOTO_NAME,
    "Ties into existing magnet range; 3 mm acrylic with magnetic backing.")
add("acrylic-photo-gifts", "Personalised Photo Keyring (Double-Sided Acrylic)", "UV", 0, 4,
    [("Rectangle", 5.99), ("Heart", 5.99), ("Circle", 5.99)], PHOTO_NAME, "")
add("acrylic-photo-gifts", "Personalised Acrylic Cake Topper (Printed)", "UV", 0, 4,
    [("15 cm", 9.99), ("20 cm", 12.99)], ["Name", "Age"], "Full-colour printed rather than plain cut acrylic.")
add("acrylic-photo-gifts", "Personalised Acrylic Door Plaque", "UV", 0, 3,
    [("A5", 14.99), ("A4", 19.99)], NAME_MSG, "Kids' bedrooms, offices, holiday lets.")
add("acrylic-photo-gifts", "Personalised Acrylic Photo Bookmark", "UV", 2, 3, 6.99, PHOTO_NAME, "")

# --- UV flatbed: slate ---------------------------------------------------------
add("slate-stone-gifts", "Personalised Photo Slate Coasters", "UV", 0, 4,
    [("Single", 5.99), ("Set of 4", 16.99)], PHOTO_NAME, "Upsell existing coaster buyers.")
add("slate-stone-gifts", "Personalised Photo Slate Plaque", "UV", 0, 4,
    [("20 x 20 cm", 19.99), ("30 x 20 cm", 24.99)], PHOTO_MSG, "")
add("slate-stone-gifts", "Personalised Slate House Sign", "UV", 0, 3,
    [("30 x 20 cm", 29.99)], ["House number", "House name", "Design"], "New-home gifts; outdoor-rated with gloss coat.")
add("slate-stone-gifts", "Personalised Slate Serving & Cheese Board", "UV", 1, 4,
    [("Rectangle 30 x 20 cm", 24.99), ("Round 25 cm", 24.99)], ["Family name", "Est. year"], "Food-safe: print on underside rim/edge only or use food-safe sealing.")

# --- UV flatbed: wood ----------------------------------------------------------
add("wooden-gifts", "Personalised Bamboo Chopping Board", "UV", 1, 5,
    [("Small 30 x 20 cm", 22.99), ("Large 38 x 28 cm (fits LEF bed)", 29.99)], ["Family name", "Recipe/handwriting upload"],
    "Handwritten-recipe boards are a huge trend; decorative side only.")
add("wooden-gifts", "Personalised Christmas Eve Wooden Board", "UV", 1, 5,
    [("30 cm", 19.99)], ["Child's name"], "Santa's treat plate - pairs with Christmas Eve box.")
add("wooden-gifts", "Personalised Wooden Tree Decorations", "UV", 1, 4,
    [("Single", 4.99), ("Set of 3", 11.99), ("Family set of 6", 19.99)], NAME, "")
add("wooden-gifts", "Personalised Wooden Photo Block", "UV", 0, 3,
    [("10 x 10 cm", 14.99), ("15 x 10 cm", 16.99)], PHOTO_MSG, "")
add("wooden-gifts", "Baby Milestone Wooden Discs (Set of 12)", "UV", 0, 4, 19.99, ["Baby's name"], "Monthly photo props.")
add("wooden-gifts", "Personalised Wooden Bottle Opener", "UV", 3, 4,
    [("Wall-mounted", 16.99), ("Handheld", 12.99)], NAME_MSG, "Father's Day hero.")
add("wooden-gifts", "Personalised Wooden Dog Lead Hook", "UV", 0, 3, 19.99, ["Pet names"], "Cross-sell with pet range.")
add("wooden-gifts", "Personalised Wooden Jigsaw Puzzle", "UV", 1, 3,
    [("30 pieces (kids)", 16.99), ("120 pieces", 22.99)], PHOTO_MSG, "Print onto pre-cut blanks.")

# --- UV flatbed: golf & darts --------------------------------------------------
add("golf-gifts", "Personalised Printed Golf Balls", "UV", 0, 5,
    [("3 balls", 14.99), ("6 balls", 24.99), ("12 balls", 39.99)], ["Photo/logo upload", "Name"],
    "Needs a ball jig. Sold with optional printed 3-ball box (cutter).")
add("golf-gifts", "Personalised Golf Ball Marker & Divot Tool", "UV", 3, 3, 9.99, NAME, "")
add("golf-gifts", "Personalised Dart Flights", "UV", 0, 4,
    [("1 set (3 flights)", 6.99), ("3 sets", 16.99)], ["Name", "Photo/logo upload"],
    "Natural fit with darts face-mask audience (Ally Pally, Lakeside).")
add("golf-gifts", "Golf Gift Set - Printed Balls in Personalised Box", "UV", 3, 4, 24.99, ["Name", "Message"],
    "Bundle: 3 printed balls + cutter-made printed box.")

# --- UV flatbed: tech ----------------------------------------------------------
add("tech-accessories", "Personalised Photo Phone Case", "UV", 0, 4,
    ("Model", [("iPhone (choose model at checkout)", 14.99), ("Samsung Galaxy", 14.99), ("Google Pixel", 14.99)]), PHOTO_NAME,
    "Revives dormant Phone & Tablet Cases collection. Batch 8-12 cases per LEF jig.")
add("tech-accessories", "Personalised Wireless Charging Pad", "UV", 1, 3, 21.99, PHOTO_NAME, "")
add("tech-accessories", "Personalised Power Bank", "UV", 0, 3, 19.99, ["Photo/logo upload"], "Also sells B2B as promo merch.")
add("tech-accessories", "Personalised Compact Mirror", "UV", 2, 3, 9.99, NAME_MSG, "")
add("tech-accessories", "Custom Printed Building Bricks", "UV", 1, 4,
    [("Single 2x4 brick", 3.99), ("Set of 6", 17.99)], ["Photo/name upload"],
    "Fits existing 'Lego' product type. Do not use LEGO name/logo - say 'compatible building bricks'.")
add("tech-accessories", "Personalised A5 Notebook (UV Printed Cover)", "UV", 0, 3, 12.99, NAME_MSG, "Teacher & office gift.")

# --- UV flatbed: awards --------------------------------------------------------
add("awards-plaques", "Printed Medal Inserts (25 mm)", "UV", 0, 3,
    ("Quantity", [("10", 14.99), ("25", 29.99), ("50", 49.99)]), ["Logo upload", "Event text"],
    "B2B for clubs/races - pairs with existing medal products.")
add("awards-plaques", "Acrylic Club Award / Trophy", "UV", 0, 3, [("Small 15 cm", 14.99), ("Large 20 cm", 19.99)],
    ["Club logo upload", "Award title", "Winner name"], "")
add("awards-plaques", "Metal Business Cards (UV on Anodised Aluminium)", "UV", 0, 3,
    ("Quantity", [("25", 49.99), ("50", 79.99)]), ["Artwork upload"], "Premium tier vs Vistaprint.")

# --- UV DTF: drinkware ---------------------------------------------------------
add("glass-can-cups", "Personalised Glass Can Cup with Bamboo Lid & Straw (16oz)", "UVDTF", 0, 5,
    [("Clear", 12.99), ("Frosted", 13.99)], ["Name", "Design"], "#1 trending drinkware item; also wholesale wraps to crafters.")
add("glass-can-cups", "Personalised 40oz Tumbler with Handle", "UVDTF", 0, 5,
    ("Colour", [("Cream", 27.99), ("Black", 27.99), ("Pink", 27.99), ("Sage", 27.99), ("Lilac", 27.99)]), NAME,
    "Stanley-style quencher. Never use 'Stanley' in titles.")
add("glass-can-cups", "Personalised 20oz Skinny Tumbler", "UVDTF", 0, 4,
    ("Colour", [("White", 19.99), ("Black", 19.99), ("Pink", 19.99)]), NAME_MSG, "")
add("glass-can-cups", "Personalised Stainless Steel Water Bottle", "UVDTF", 0, 4,
    ("Size", [("500 ml", 14.99), ("750 ml", 16.99)]), NAME, "Gym, school, office.")
add("glass-can-cups", "Personalised Travel Coffee Cup", "UVDTF", 0, 3, 14.99, NAME_MSG, "")
add("glass-can-cups", "Personalised Enamel Camping Mug", "UVDTF", 3, 3, 12.99, NAME_MSG, "")
add("glass-can-cups", "Personalised Hip Flask", "UVDTF", 3, 3, 14.99, NAME_MSG, "Revives VE Day hip flask blanks.")

# --- UV DTF: glassware -----------------------------------------------------------
add("glassware", "Personalised Gin Balloon Glass", "UVDTF", 1, 4, 14.99, NAME_MSG, "")
add("glassware", "Personalised Wine Glass", "UVDTF", 1, 4, 12.99, NAME_MSG, "")
add("glassware", "Personalised Pint Glass", "UVDTF", 3, 4, 11.99, NAME_MSG, "")
add("glassware", "Personalised Whisky Tumbler", "UVDTF", 3, 4, 13.99, NAME_MSG, "")
add("glassware", "Personalised Prosecco Flute", "UVDTF", 3, 3, [("Single", 12.99), ("Pair", 22.99)], NAME, "Weddings & hen parties.")

# --- UV DTF: baubles & decorations ---------------------------------------------------
add("christmas-baubles", "Personalised Name Bauble", "UVDTF", 1, 5,
    ("Colour", [("Red", 5.99), ("Gold", 5.99), ("Silver", 5.99), ("Clear", 5.99), ("Green", 5.99)]), NAME,
    "Highest-volume Christmas item in the category. Offer bauble gift box upsell.")
add("christmas-baubles", "Personalised Photo Bauble", "UVDTF", 1, 5, 7.99, PHOTO_NAME, "")
add("christmas-baubles", "Baby's First Christmas Bauble", "UVDTF", 1, 5, 7.99, ["Name", "Year"], "")
add("christmas-baubles", "Memorial Robin Bauble", "UVDTF", 1, 4, 7.99, ["Name", "Message"], "'Robins appear when loved ones are near'.")
add("christmas-baubles", "Personalised Santa's Magic Key", "UV", 1, 5, 6.99, ["Family name"], "UK Christmas trend for homes without chimneys.")
add("christmas-baubles", "Pet's First Christmas Bauble", "UVDTF", 1, 4, 7.99, ["Pet name", "Photo upload"], "")

# --- UV DTF: candles & jars ------------------------------------------------------
add("candles-jars", "Personalised Scented Candle", "UVDTF", 1, 4,
    ("Scent", [("Vanilla", 14.99), ("Cinnamon Christmas", 14.99), ("Fresh Linen", 14.99)]), NAME_MSG, "")
add("candles-jars", "Personalised Sweet Jar", "UVDTF", 0, 4, [("Empty", 9.99), ("Filled with retro sweets", 16.99)],
    ["Name", "e.g. Grandad's Sweets"], "")
add("candles-jars", "Personalised Tooth Fairy Tin", "UVDTF", 0, 3, 6.99, NAME, "")

# --- UV DTF: school ----------------------------------------------------------------
add("kids-labels-bottles", "Waterproof Kids Name Labels", "UVDTF", 0, 5,
    ("Pack", [("30 labels", 8.99), ("60 labels", 13.99), ("120 labels", 19.99)]), ["Name", "Icon"],
    "Back-to-school peak Aug/Sep; dishwasher-safe UV DTF. Big repeat purchase.")
add("kids-labels-bottles", "Personalised Kids School Water Bottle", "UVDTF", 0, 4, 12.99, NAME, "")
add("kids-labels-bottles", "Personalised Kids Lunch Box", "UVDTF", 0, 4, 11.99, NAME, "Existing 5-product range - expand designs.")
add("kids-labels-bottles", "Personalised Bike / Riding Helmet Name Decals", "UVDTF", 0, 3, 6.99, NAME, "")

# --- UV DTF: gamer ---------------------------------------------------------------------
add("gamer-skins", "Custom Games Controller Skin", "UVDTF", 0, 4,
    ("Controller", [("PS5 DualSense", 9.99), ("Xbox Series", 9.99), ("Switch Pro", 9.99)]), ["Name", "Photo upload"],
    "Huge fit for the retro gaming audience. Use own artwork only.")
add("gamer-skins", "Custom Laptop Skin", "UVDTF", 0, 3, ("Size", [("13 inch", 14.99), ("15 inch", 16.99)]), ["Photo upload"], "")

# --- Trade transfers -------------------------------------------------------------------
add("craft-supplies", "UV DTF Cup Wrap Transfer (16oz)", "UVDTF", 0, 4,
    ("Quantity", [("1", 3.49), ("10", 27.99), ("25", 59.99)]), ["Artwork upload"], "Wholesale to crafters - strong Etsy/FB group demand.")
add("craft-supplies", "UV DTF Gang Sheet", "UVDTF", 0, 4, ("Size", [("A4", 9.99), ("A3", 14.99)]), ["Artwork upload"], "")
add("craft-supplies", "DTF Clothing Transfers Gang Sheet", "DTF", 0, 5,
    ("Size", [("A3", 7.99), ("56 x 50 cm", 11.99), ("56 x 100 cm", 19.99)]), ["Artwork upload"],
    "Sell by the metre to UK print shops/home pressers - fills machine downtime.")

# --- DTF clothing ------------------------------------------------------------------------
add("custom-clothing", "Personalised Adult T-Shirt", "DTF", 0, 4,
    [("S", 14.99), ("M", 14.99), ("L", 14.99), ("XL", 14.99), ("2XL", 16.99)], ["Photo/design upload", "Text"], "")
add("custom-clothing", "Personalised Kids T-Shirt", "DTF", 0, 4,
    [("3-4 yrs", 11.99), ("5-6 yrs", 11.99), ("7-8 yrs", 11.99), ("9-11 yrs", 11.99), ("12-13 yrs", 11.99)], ["Name", "Age", "Design"], "")
add("custom-clothing", "Personalised Adult Hoodie", "DTF", 0, 4,
    [("S", 27.99), ("M", 27.99), ("L", 27.99), ("XL", 27.99), ("2XL", 29.99)], ["Photo/design upload", "Text"], "")
add("custom-clothing", "Personalised Sweatshirt", "DTF", 0, 3,
    [("S", 22.99), ("M", 22.99), ("L", 22.99), ("XL", 22.99)], ["Design upload", "Text"], "")
add("custom-clothing", "Birthday Age T-Shirt (Kids)", "DTF", 0, 4,
    [("1", 11.99), ("2", 11.99), ("3", 11.99), ("4", 11.99), ("5", 11.99), ("6", 11.99)], ["Name", "Age", "Theme"], "")
add("custom-clothing", "Big Brother / Big Sister T-Shirt", "DTF", 0, 4,
    [("2-3 yrs", 12.99), ("3-4 yrs", 12.99), ("5-6 yrs", 12.99), ("7-8 yrs", 12.99)], NAME, "Pregnancy announcement trend.")
add("school-leavers", "School Leavers Hoodie (Names on Back)", "DTF", 3, 5,
    [("Kids 7-8", 24.99), ("Kids 9-11", 24.99), ("Kids 12-13", 24.99), ("Adult S", 26.99), ("Adult M", 26.99), ("Adult L", 26.99)],
    ["School name", "Year", "Class names list"], "Year 6/11/13 leavers. Sell group packs with school admin discount codes.")
add("school-leavers", "Club / Team Hoodie with Logo", "DTF", 0, 3,
    [("Kids", 22.99), ("Adult", 26.99)], ["Logo upload", "Name", "Number"], "")
add("christmas-clothing", "Matching Family Christmas Jumper", "DTF", 1, 5,
    ("Who", [("Adult", 24.99), ("Kids", 19.99), ("Baby", 14.99), ("Dog", 14.99)]), NAME, "")
add("christmas-clothing", "Personalised Christmas Pyjamas", "DTF", 1, 5,
    ("Who", [("Adult", 24.99), ("Kids", 19.99), ("Baby", 14.99)]), NAME, "Christmas Eve box filler.")
add("christmas-clothing", "My First Christmas Baby Grow", "DTF", 1, 5,
    [("0-3 m", 9.99), ("3-6 m", 9.99), ("6-12 m", 9.99)], NAME, "Extends existing 2,000-strong baby grow range.")
add("baby-clothing", "Personalised Baby Bib", "DTF", 0, 4, 7.99, NAME, "")
add("baby-clothing", "Personalised Baby Vest", "DTF", 0, 3, [("0-3 m", 9.99), ("3-6 m", 9.99), ("6-12 m", 9.99)], NAME_MSG, "")
add("baby-clothing", "Cake Smash First Birthday Outfit", "DTF", 0, 4, [("12-18 m", 14.99)], NAME, "")
add("baby-clothing", "Personalised Baby Blanket (Fleece)", "DTF", 0, 4, 19.99, ["Name", "Birth date"], "")
add("pet-clothing", "Personalised Dog Bandana", "DTF", 0, 5, [("S", 8.99), ("M", 8.99), ("L", 9.99)], ["Pet name"], "")
add("pet-clothing", "Personalised Dog Hoodie", "DTF", 1, 4, [("XS", 16.99), ("S", 16.99), ("M", 17.99), ("L", 18.99)], ["Pet name"], "")
add("pet-clothing", "Personalised Pet Blanket", "DTF", 1, 4, [("Small", 17.99), ("Large", 22.99)], ["Pet name", "Photo upload"], "")
add("pet-clothing", "Personalised Pet ID Tag", "UV", 0, 4, [("Bone", 7.99), ("Round", 7.99), ("Heart", 7.99)], ["Pet name", "Phone number"], "")
add("pet-clothing", "Personalised Stainless Steel Pet Bowl", "UVDTF", 0, 4, [("Small", 14.99), ("Large", 17.99)], ["Pet name"], "Pairs with existing dog bowl mats.")
add("pet-clothing", "Personalised Pet Treat Jar", "UVDTF", 0, 3, 12.99, ["Pet name"], "")
add("pet-clothing", "Custom Pet Portrait Print", "PRESS", 0, 5, [("A4", 19.99), ("A3", 26.99)], ["Photo upload", "Pet name"],
    "Illustrated-style portrait from photo; reuse artwork on mugs/cushions/tees.")
add("bags-aprons-textiles", "Personalised Tote Bag", "DTF", 0, 4, 8.99, NAME_MSG, "Teacher gifts, hen parties, business promo.")
add("bags-aprons-textiles", "Personalised Drawstring PE Bag", "DTF", 0, 4, 8.99, NAME, "")
add("bags-aprons-textiles", "Personalised Apron", "DTF", 3, 3, [("Kids", 11.99), ("Adult", 14.99)], NAME_MSG, "")
add("bags-aprons-textiles", "Personalised Cap", "DTF", 0, 3, 12.99, ["Text", "Logo upload"], "")
add("bags-aprons-textiles", "Personalised Party Sash", "DTF", 0, 4, 6.99, ["Text"], "Hen, birthday, prom.")
add("bags-aprons-textiles", "Personalised Trick or Treat Bag", "DTF", 1, 4, 7.99, NAME, "Launch immediately for Halloween 2026.")
add("bags-aprons-textiles", "Personalised Teddy Bear with T-Shirt", "DTF", 0, 4, 19.99, NAME_MSG, "Existing teddy range - new designs.")
add("workwear", "Logo Polo Shirt (Workwear)", "DTF", 0, 3, [("S", 15.99), ("M", 15.99), ("L", 15.99), ("XL", 15.99), ("2XL", 17.99)], ["Logo upload"], "Bulk tiered pricing.")
add("workwear", "Hi-Vis Vest with Logo", "DTF", 0, 3, 9.99, ["Logo upload"], "")
add("workwear", "Football Kit Name & Number Printing", "DTF", 0, 3, 5.99, ["Name", "Number"], "Service product per shirt.")

# --- Cutter: boxes & packaging ---------------------------------------------------------------
add("christmas-eve-boxes", "Personalised Christmas Eve Box", "CUT", 1, 5,
    [("Medium", 14.99), ("Large", 19.99), ("XL Family", 24.99)], ["Child's name", "Design"], "UK hero product Oct-Dec.")
add("christmas-eve-boxes", "Fill-Your-Own Personalised Advent Calendar", "CUT", 1, 5,
    [("24 drawers - kids", 24.99), ("24 drawers - adult", 24.99)], ["Name", "Photo upload"], "Start selling 1 Oct; last date ~25 Nov.")
add("christmas-eve-boxes", "Personalised Selection Box Sleeve", "CUT", 1, 4, [("Sleeve only", 3.99), ("Pack of 5", 14.99)], NAME, "")
add("christmas-eve-boxes", "Reindeer Food Bag", "CUT", 1, 4, [("Single", 1.99), ("Pack of 10", 12.99)], NAME, "")
add("christmas-eve-boxes", "Personalised Letter from Santa", "PRESS", 1, 4, 4.99, ["Child's name", "Achievements"], "")
add("christmas-eve-boxes", "Christmas Elf Arrival Kit", "CUT", 1, 4, 9.99, ["Child's name"], "Avoid 'Elf on the Shelf' trademark.")
add("party-boxes", "Printed Cupcake Boxes (Window)", "CUT", 0, 4,
    ("Size", [("1 cupcake x10", 9.99), ("4 cupcakes x10", 14.99), ("6 cupcakes x10", 17.99)]), ["Name/logo", "Design"],
    "Consumer parties + B2B for home bakers.")
add("party-boxes", "Personalised Party Favour Boxes", "CUT", 0, 4, ("Quantity", [("10", 7.99), ("25", 16.99)]), ["Name", "Age", "Theme"], "")
add("party-boxes", "Wedding Favour Boxes", "CUT", 3, 4, ("Quantity", [("25", 19.99), ("50", 34.99), ("100", 59.99)]), ["Names", "Date"], "")
add("party-boxes", "Personalised Popcorn Boxes (Movie Night)", "CUT", 0, 3, ("Quantity", [("10", 6.99)]), NAME, "")
add("party-boxes", "Personalised Pillow Treat Boxes", "CUT", 0, 3, ("Quantity", [("10", 6.99)]), NAME, "")
add("gift-packaging", "Personalised Golf Ball Box (3-Ball)", "CUT", 3, 4, [("Empty box", 4.99), ("With 3 printed balls", 24.99)], NAME_MSG, "")
add("gift-packaging", "Mug Gift Box (Add-On)", "CUT", 0, 4, 2.49, [], "Checkout upsell for 14,000+ mugs - easy AOV win.")
add("gift-packaging", "Bauble Gift Box (Add-On)", "CUT", 1, 4, 1.99, [], "Checkout upsell.")
add("gift-packaging", "Personalised Letterbox Gift Box", "CUT", 0, 4, [("Empty printed box", 4.99), ("Hug in a Box (filled)", 16.99)], NAME_MSG, "")
add("gift-packaging", "Small Business Printed Mailer Boxes", "CUT", 0, 3, ("Quantity", [("25", 49.99), ("50", 84.99)]), ["Logo upload"], "Vistaprint competitor line - quote over 50.")
add("custom-game-cases", "Personalised Video Game Case - Put Yourself on the Cover", "CUT", 0, 5,
    ("Style", [("Modern console style", 12.99), ("Retro 16-bit style", 12.99), ("Handheld style", 11.99)]),
    ["Photo upload", "Game title", "Name"], "Leverages existing game-case expertise; birthday/gamer gift. Generic styling, no console logos.")
add("custom-game-cases", "Personalised Birthday Game Case Card", "CUT", 0, 4, 6.99, ["Photo upload", "Name", "Age"], "Card that looks like a game case.")
add("papercraft", "Personalised Glitter Card Cake Topper", "CUT", 0, 4, 6.99, ["Name", "Age"], "")
add("papercraft", "Personalised Cupcake Toppers (Set of 12)", "CUT", 0, 3, 4.99, ["Name", "Age", "Theme"], "")
add("papercraft", "Pop-Up 3D Birthday Card", "CUT", 0, 4, 5.99, ["Name", "Message"], "")
add("papercraft", "Photo Booth Props (Set of 20)", "CUT", 3, 3, 14.99, ["Names", "Date"], "Weddings & parties.")
add("papercraft", "Personalised Gift Tags (Pack of 20)", "CUT", 1, 3, 4.99, ["From name"], "")
add("papercraft", "Personalised Card Jigsaw", "CUT", 0, 3, [("A4", 14.99), ("A3", 19.99)], PHOTO_MSG, "")

# --- Business printing (Vistaprint parity) ------------------------------------------------------
add("business-stationery", "Spot-Gloss (Raised UV) Business Cards", "UV", 0, 4,
    ("Quantity", [("100", 29.99), ("250", 44.99), ("500", 64.99)]), ["Artwork upload"], "LEF-300 gloss channel creates raised spot finish.")
add("business-stationery", "Rounded-Corner & Square Business Cards", "CUT", 0, 3,
    ("Quantity", [("100", 19.99), ("250", 29.99), ("500", 39.99)]), ["Artwork upload"], "")
add("business-stationery", "Flyers & Leaflets", "PRESS", 0, 3,
    ("Size", [("A6 x 250", 24.99), ("A5 x 250", 34.99), ("A4 x 100", 34.99)]), ["Artwork upload"], "")
add("business-stationery", "Postcards", "PRESS", 0, 3, ("Quantity", [("50", 17.99), ("100", 24.99)]), ["Artwork upload"], "")
add("business-stationery", "Gift Vouchers (Numbered)", "PRESS", 0, 3, ("Quantity", [("50", 24.99), ("100", 34.99)]), ["Artwork upload"], "")
add("business-stationery", "Appointment & Loyalty Cards", "PRESS", 0, 3, ("Quantity", [("100", 19.99), ("250", 29.99)]), ["Artwork upload"], "Extends existing loyalty cards.")
add("business-stationery", "Table Talkers & Menus", "CUT", 0, 3, ("Quantity", [("10", 19.99), ("25", 34.99)]), ["Artwork upload"], "")
add("stickers-labels", "Custom Die-Cut Stickers", "CUT", 0, 5,
    ("Quantity", [("50", 19.99), ("100", 29.99), ("250", 49.99)]), ["Artwork upload"], "Small-business staple.")
add("stickers-labels", "Kiss-Cut Sticker Sheets", "CUT", 0, 4, ("Quantity", [("5 sheets", 9.99), ("20 sheets", 29.99)]), ["Artwork upload"], "")
add("stickers-labels", "Product Labels (Candle, Jam, Cosmetics)", "CUT", 0, 4,
    ("Quantity", [("50", 14.99), ("100", 22.99), ("250", 39.99)]), ["Artwork upload"], "Huge small-business demand.")
add("stickers-labels", "Thank You for Your Order Stickers", "CUT", 0, 3, ("Quantity", [("100", 12.99)]), ["Logo upload"], "")
add("signs-displays", "Tap & Scan Google Review Stand (NFC + QR)", "UV", 0, 5, 19.99, ["Logo upload", "Review link"],
    "Trending with small businesses; embed NFC tag under acrylic.")
add("signs-displays", "Acrylic QR Code Sign (Scan to Pay / Follow / Wi-Fi)", "UV", 0, 4, [("A6 stand", 12.99), ("A5 stand", 16.99)], ["QR link", "Logo upload"], "")
add("signs-displays", "Acrylic Office & Door Sign", "UV", 0, 3, [("30 x 10 cm", 19.99)], ["Text", "Logo upload"], "")
add("signs-displays", "Small Foamex / Dibond Sign", "UV", 0, 3, [("A4", 14.99), ("A3", 24.99)], ["Artwork upload"], "Up to 762 x 330 mm in-house; outsource larger.")

# --- Seasonal extras -------------------------------------------------------------------------
add("halloween", "Personalised Halloween Kids T-Shirt", "DTF", 1, 4, [("3-4 yrs", 11.99), ("5-6 yrs", 11.99), ("7-8 yrs", 11.99), ("9-11 yrs", 11.99)], NAME, "")
add("halloween", "Halloween Treat Boxes (Pack of 10)", "CUT", 1, 3, 7.99, NAME, "")
add("halloween", "My First Halloween Baby Grow", "DTF", 1, 4, [("0-3 m", 9.99), ("3-6 m", 9.99), ("6-12 m", 9.99)], NAME, "")
add("valentines-mothers-day", "Reasons I Love You Jar", "UVDTF", 2, 4, 16.99, ["Names", "Reasons list"], "")
add("valentines-mothers-day", "Personalised Love Coupon Book", "PRESS", 2, 3, 6.99, ["Names"], "")
add("valentines-mothers-day", "Personalised Mum Slate Heart", "UV", 2, 4, 16.99, ["Names"], "")
add("valentines-mothers-day", "Mummy & Me Matching T-Shirts", "DTF", 2, 4, ("Who", [("Adult", 14.99), ("Kids", 11.99), ("Baby", 9.99)]), NAME, "")
add("easter", "Personalised Easter Egg Hunt Kit", "CUT", 2, 4, 9.99, NAME, "")
add("easter", "Personalised Easter Basket Bag", "DTF", 2, 4, 9.99, NAME, "")
add("easter", "Personalised Easter Egg Box", "CUT", 2, 3, 4.99, NAME, "")
add("weddings", "Acrylic Wedding Welcome Sign", "UV", 3, 5, [("A3", 49.99)], ["Names", "Date"], "A3 fits the LEF-300 bed.")
add("weddings", "Acrylic Wedding Table Numbers (Set of 10)", "UV", 3, 4, 34.99, ["Names", "Date"], "")
add("weddings", "Personalised Acrylic Place Names (Pack of 10)", "UV", 3, 4, 19.99, ["Guest names list"], "")
add("weddings", "Wedding Invitations (Pack of 25)", "PRESS", 3, 3, 34.99, ["Names", "Date", "Venue"], "")
add("memorial", "Pet Memorial Slate Plaque", "UV", 0, 4, 21.99, ["Pet name", "Photo upload", "Dates"], "")
add("memorial", "Memorial Acrylic Photo Plaque", "UV", 0, 4, [("A5", 19.99), ("A4", 26.99)], ["Name", "Photo upload", "Dates"], "")
add("new-baby", "Birth Announcement Print", "PRESS", 0, 4, [("A4", 14.99), ("A3", 19.99)], ["Name", "Date", "Weight", "Time"], "")
add("new-baby", "Pregnancy Announcement Scan Frame Plaque", "UV", 0, 4, 19.99, ["Scan photo upload", "Due date"], "")
add("new-baby", "Baby Keepsake Box (Printed)", "CUT", 0, 3, 14.99, ["Name", "Birth date"], "")
