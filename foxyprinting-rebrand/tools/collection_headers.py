"""Pick a themed header banner for every collection (first matching rule wins)."""
import re
RULES = [
    ("skip", r"^kids-cards$"),  # has its own banner
    ("skins", r"skins?$|perfect-skins"),
    ("pets", r"pet|dog"),
    ("baby", r"baby|new-baby|teddy|christening"),
    ("christmas", r"christmas|santa|stocking|bauble|wrapping"),
    ("halloween", r"halloween"),
    ("easter", r"easter"),
    ("love", r"valentine|wedding|engagement|future-husband|future-mrs|celebrity-lover|mothers|memorial"),
    ("commemorative", r"^king-charles|(?<!street-)coronation(?!-street)|jubilee|^ve-day|flags"),
    ("retro", r"all-other-magnets|all-other-keyrings|atari|nintendo|sega|playstation|ps1|ps4|gameboy|snes|nes-|dreamcast|odyssey|coleco|colevision|neo-geo|amiga|intelivision|xbox|mega-cd|retro-gam|game-case|replacement|other-console|cd32|3do|all-play"),
    ("prints", r"signed|autograph|poster|prints?$|canvas|word-art|a6-"),
    ("prints", r"walking-dead-star"),
    ("masks", r"mask|celebrit|tv-star|comedians|politicians|towie|emmerdale|bollywood|request|love-island|money-heist|squid|saw$|maid|bad-boys|ink-master|stranger|the-boys|the-victim|queen-of-flow|still-game|god-of-hellfire|gangs-of-london|austin|real-housewives|the-chase|britain-s-got|strictly|walking-dead|friends|neighbours|only-fools|sex-and|star-trek|madmens|hangover|hollyoaks|geordie|made-in-chelsea|coronation-street|eastenders|bake-off|big-bang|benidorm|eurovision|one-direction|xfactor|im-a-celebrity|marvel|copa|euro-2021|england-2021|wales-2021|face-cover"),
    ("business", r"business|loyalty|thank-you|signs-displays|craft-supplies|stationery"),
    ("kids", r"kids-labels|school|lunchbox|backpack|reward"),
    ("stickers", r"sticker|label|decal|phone-case|stickers-cases"),
    ("gaming", r"gaming|gamer|game"),
    ("bar", r"coaster|bar-mat|man-cave"),
    ("drinkware", r"glass|can-cup|bottle|flask|drinkware"),
    ("mugs", r"mug|i-like|i-love|id-rather|this-girl|this-guy|keep-calm|carry-on|scrabble|star-sign|dating|emoticon|alchemy|occupational|office-humour|coach|kings-are|manufacured|top-100|male-movie|female-movie|football-crazy|signs-for|league|national-league|scottish-football|premier-league|championship|international-football"),
    ("party", r"invite|invitation|party|bunting|banner|kit-kat|papercraft|birthday-banners"),
    ("cards", r"cards?$|card-|birthday|occasion-birthday|fathers-day-cards"),
    ("kids", r"kids|school|lunchbox|backpack|reward"),
    ("sports", r"football|rugby|sport|golf|armband|towel|errea|euros|darts"),
    ("clothing", r"t-shirt|tee|hoodie|clothing|apparel|scarves|bobble|workwear|pride|stag|hen-"),
    ("stickers", r"sticker|label|decal|phone-case|stickers-cases"),
    ("business", r"business|loyalty|thank-you|signs|craft-supplies|stationery"),
    ("gifts", r".*"),
]

def header_for(handle):
    for group, pat in RULES:
        if re.search(pat, handle):
            return group
    return "gifts"
