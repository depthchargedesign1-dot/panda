"""Pick the right Shopify Standard Product Taxonomy category for every product, from its title (then product type).

Rules are checked in order; the first match wins. Products that match nothing keep their current category.
Usage: python3 tools/category_rules.py <all_products.jsonl> <out_dir>
Writes product-categories-NN.csv (Handle, Product Category) for products whose category should change,
plus category-review.csv (counts of old -> new) for checking.
"""
import csv
import json
import re
import sys
from collections import Counter

A = "Apparel & Accessories > "
HG = "Home & Garden > "
PARTY = "Arts & Entertainment > Party & Celebration > "
DRINK = HG + "Kitchen & Dining > Tableware > Drinkware > "
KIDS = r"\b(kids?|child|children|toddler|boys?|girls?|baby|junior|youth|age \d|\d+(st|nd|rd|th) birthday)\b"
CONSOLE = r"\b(nes|snes|sega|mega ?drive|genesis|master ?system|mega ?cd|saturn|dreamcast|playstation|ps[1-5]|psx|game ?boy|gameboy|gamecube|game cube|n64|nintendo|atari|3do|xbox|switch|wii|lynx|jaguar|neo ?geo|turbografx|pc engine|virtual boy)\b"

RULES = [  # (title regex, category) — order matters
    (r"face covering|snood|neck gaiter|buff\b", A + "Clothing Accessories > Fashion Face Masks"),
    (r"face ?masks?\b|facemask|\bmask\b(?! ?(stand|holder))", A + "Costumes & Accessories > Masks"),
    (r"baby ?grow|babygrow|baby vest|bodysuit|onesie|sleep ?suit|romper", A + "Clothing > Baby & Children's Clothing > Baby & Children's Tops > Bodysuits"),
    (r"\bmugs?\b", DRINK + "Mugs"),
    (r"\bmagnets?\b", HG + "Decor > Refrigerator Magnets"),
    (r"key ?rings?|keychains?|key fobs?", A + "Handbag & Wallet Accessories > Keychains"),
    (r"phone case", "Electronics > Communications > Telephony > Mobile & Smart Phone Accessories > Mobile Phone Cases"),
    (r"(game|replacement|cartridge|disc|cd|dvd)\s*(storage\s*)?(case|box|cover)|\bcases?\b.*" + CONSOLE + "|" + CONSOLE + r".*\bcases?\b", "Electronics > Video Game Console Accessories"),
    (r"controller (skin|decal)|console (skin|decal)|laptop skin|light ?bar", "Electronics > Video Game Console Accessories"),
    (r"armband", "Sporting Goods > Athletics > Coaching & Officiating > Captains Armbands"),
    (r"display case|display frame", "Business & Industrial > Retail > Retail Display Cases"),
    (r"pin badges?|\bbadges?\b|lapel pin", A + "Jewelry > Brooches & Lapel Pins"),
    (r"lunch (box|bag)|cool(er)? bag", HG + "Kitchen & Dining > Food & Beverage Carriers > Lunch Boxes & Totes"),
    (r"poster (pack|print cards?)|\ba6\b.*(pack|cards?)", HG + "Decor > Artwork > Posters, Prints, & Visual Artwork"),
    (r"\bposters?\b", HG + "Decor > Artwork > Posters, Prints, & Visual Artwork > Posters"),
    (r"stocking", HG + "Decor > Seasonal & Holiday Decorations > Holiday Stockings"),
    (r"advent calendar", HG + "Decor > Seasonal & Holiday Decorations > Advent Calendars"),
    (r"bauble|christmas (tree )?(ornament|decoration)|hanging decoration", HG + "Decor > Seasonal & Holiday Decorations > Holiday Ornaments"),
    (r"santa sack|\bsacks?\b|gift bag|party bags?|treat bag|reindeer food", PARTY + "Gift Giving > Gift Wrapping > Gift Bags"),
    (r"wrapping paper|gift wrap", PARTY + "Gift Giving > Gift Wrapping > Wrapping Paper"),
    (r"(gift|treat|favour|favor|eve|selection|popcorn|cupcake|cake|mailer|keepsake|letterbox|pillow|easter egg|sweet|memory|golf ball) box|boxes\b|\bbox\b", PARTY + "Gift Giving > Gift Wrapping > Gift Boxes & Tins"),
    (r"coasters?\b", HG + "Kitchen & Dining > Barware > Coasters"),
    (r"bar mats?|bar runner", HG + "Kitchen & Dining > Barware"),
    (r"bunting|banner|garland", PARTY + "Party Supplies > Banners"),
    (r"business cards?", "Office Supplies > General Office Supplies > Paper Products > Business Cards"),
    (r"sport cards?|trading cards?", "Arts & Entertainment > Hobbies & Creative Arts > Collectibles > Collectible Trading Cards > Sports Trading Cards"),
    (r"poster card|a6 .*card pack", HG + "Decor > Artwork > Posters, Prints, & Visual Artwork"),
    (r"certificate", PARTY + "Trophies & Awards > Award Certificates"),
    (r"\bmedals?\b", PARTY + "Trophies & Awards > Award Pins & Medals"),
    (r"trophy|award", PARTY + "Trophies & Awards > Award Plaques"),
    (r"\bcards?\b|invitations?\b|invites?\b", PARTY + "Gift Giving > Greeting & Note Cards > Greeting Cards"),
    (r"postcards?|flyers?|leaflets?", "Office Supplies > General Office Supplies > Paper Products"),
    (r"\bposters?\b", HG + "Decor > Artwork > Posters, Prints, & Visual Artwork > Posters"),
    (r"\bprints?\b|word art|wall art|canvas|portrait", HG + "Decor > Artwork > Posters, Prints, & Visual Artwork"),
    (r"t-?shirts?|\btees?\b", "TSHIRT"),
    (r"hoodies?|hooded", "HOODIE"),
    (r"sweatshirts?|jumpers?|sweaters?", "SWEAT"),
    (r"polo shirts?|\bpolos?\b|hi-?vis|workwear", A + "Clothing > Clothing Tops > Polos"),
    (r"\bcaps?\b|snapback|trucker", A + "Clothing Accessories > Hats > Baseball Caps"),
    (r"\bhats?\b|beanie|bobble", A + "Clothing Accessories > Hats"),
    (r"cufflinks?", A + "Clothing Accessories > Cufflinks"),
    (r"\bsash(es)?\b", A + "Clothing Accessories > Sashes"),
    (r"aprons?", HG + "Kitchen & Dining > Kitchen Tools & Utensils > Aprons"),
    (r"lunch (box|bag)|cool(er)? bag", HG + "Kitchen & Dining > Food & Beverage Carriers > Lunch Boxes & Totes"),
    (r"back ?packs?|rucksacks?|school bag", "Luggage & Bags > Backpacks"),
    (r"tote|shopping bag|drawstring|pe bag|gym bag|book bag|\bbags?\b", "Luggage & Bags > Tote Bags"),
    (r"golf towel", "Sporting Goods > Outdoor Recreation > Golf > Golf Towels"),
    (r"beach\b.*towel|gym towel", HG + "Linens & Bedding > Towels > Beach Towels"),
    (r"tea towel", HG + "Linens & Bedding > Kitchen Linens Sets"),
    (r"towels?\b", HG + "Linens & Bedding > Towels > Bath Towels & Washcloths > Bath Towels"),
    (r"blankets?|throw\b|fleece", HG + "Linens & Bedding > Bedding > Blankets > Throw Blankets"),
    (r"cushions?|pillow", HG + "Decor > Throw Pillows"),
    (r"teddy|plush|soft toy|cuddly", "Toys & Games > Toys > Dolls, Playsets & Toy Figures > Stuffed Animals"),
    (r"jigsaw|puzzle", "Toys & Games > Puzzles > Jigsaw Puzzles"),
    (r"mouse ?(mat|pad)|desk mat|gaming mat", "Electronics > Electronics Accessories > Computer Accessories > Mouse Pads"),
    (r"tumbler|can cup|can glass|glass can|travel (mug|cup)", DRINK + "Tumblers"),
    (r"water bottle|sports bottle|drinks? bottle", HG + "Kitchen & Dining > Food & Beverage Carriers > Water Bottles"),
    (r"wine glass|champagne|prosecco|flute|gin glass|goblet|stemless|cocktail glass", DRINK + "Stemware"),
    (r"shot glass", DRINK + "Shot Glasses"),
    (r"pint glass|beer glass|stein|tankard|beer mug|whisky glass|glassware", DRINK + "Beer Glasses"),
    (r"pet (id )?tag|dog tag|collar tag", "Animals & Pet Supplies > Pet Supplies > Pet ID Tags"),
    (r"bandana", "Animals & Pet Supplies > Pet Supplies > Pet Apparel > Pet Bandanas"),
    (r"(pet|dog|cat) bowl|feeding mat|bowl mat", "Animals & Pet Supplies > Pet Supplies > Pet Bowls, Feeders & Waterers"),
    (r"golf balls?", "Sporting Goods > Outdoor Recreation > Golf > Golf Balls"),
    (r"dart flights?", "Sporting Goods > Indoor Games > Throwing Darts > Dart Parts > Dart Flights"),
    (r"clocks?\b", HG + "Decor > Clocks > Wall Clocks"),
    (r"calendar", "Office Supplies > Filing & Organization > Calendars, Organizers & Planners > Wall Calendars"),
    (r"photo (block|frame)|picture frame|\bframes?\b|acrylic block", HG + "Decor > Picture Frames"),
    (r"plaque|slate|\bsigns?\b|door hanger", HG + "Decor > Decorative Plaques"),
    (r"bookmarks?", "Office Supplies > Book Accessories > Bookmarks"),
    (r"\bflags?\b|windsock", HG + "Decor > Flags & Windsocks"),
    (r"car (sticker|decal)|bumper sticker|vinyl (car )?(sticker|decal)|van (sticker|decal)", "Vehicles & Parts > Vehicle Parts & Accessories > Vehicle Maintenance, Care & Decor > Vehicle Decor > Bumper Stickers"),
    (r"wheelie bin|wall (sticker|decal)|window (sticker|decal|cling)", HG + "Decor > Home Decor Decals"),
    (r"labels?\b", "Office Supplies > General Office Supplies > Labels & Tags"),
    (r"stickers?|decals?", "Arts & Entertainment > Hobbies & Creative Arts > Arts & Crafts > Art & Crafting Materials > Embellishments & Trims > Decorative Stickers"),
    (r"cake toppers?", PARTY + "Party Supplies"),
]
CLOTHES = {
    "TSHIRT": (A + "Clothing > Baby & Children's Clothing > Baby & Children's Tops > T-Shirts", A + "Clothing > Clothing Tops > T-Shirts"),
    "HOODIE": (A + "Clothing > Baby & Children's Clothing > Baby & Children's Tops > Hoodies", A + "Clothing > Clothing Tops > Hoodies"),
    "SWEAT": (A + "Clothing > Baby & Children's Clothing > Baby & Children's Tops > Sweatshirts", A + "Clothing > Clothing Tops > Sweatshirts"),
}
COMPILED = [(re.compile(rx, re.I), cat) for rx, cat in RULES]


def pick(p):
    for text in (p["title"], p.get("productType") or ""):
        for rx, cat in COMPILED:
            if rx.search(text):
                if cat in CLOTHES:
                    kids = re.search(KIDS, p["title"], re.I) is not None
                    return CLOTHES[cat][0 if kids else 1]
                return cat
    return None


def main(src, out):
    P = [json.loads(l) for l in open(src)]
    changes, review, nomatch = [], Counter(), Counter()
    for p in P:
        old = (p.get("category") or {}).get("fullName") or ""
        new = pick(p)
        if not new:
            nomatch[(p.get("productType") or "(no type)")] += 1
            continue
        if new != old:
            changes.append((p["handle"], new))
            review[(old or "(none)", new)] += 1
    for n, i in enumerate(range(0, len(changes), 15000)):
        with open(f"{out}/product-categories-{n + 1:02d}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["Handle", "Product Category"]); w.writerows(changes[i:i + 15000])
    with open(f"{out}/category-review.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Count", "Old category", "New category"])
        for (o, nw), c in review.most_common():
            w.writerow([c, o, nw])
    with open(f"{out}/category-unmatched-types.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Count", "Product type (no rule matched; category left as is)"])
        for t, c in nomatch.most_common():
            w.writerow([c, t])
    print(f"products {len(P)}, changes {len(changes)}, unmatched {sum(nomatch.values())}")
    return changes, review, nomatch


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
