"""Third-party name tables and title clean-up for tools/mug_copy.py (mug descriptions, 6 Oct 2026)."""
import re

# ---------------------------------------------------------------- swear-word censor (copy never spells them out)
# (pattern, number of leading letters kept, letters starred after them)
CENSOR = [(r"motherf\w*", None), (r"f+u+c+k\w*", 1), (r"f\*+c?k\w*", None), (r"fckwit", 1), (r"cunt\w*", 1),
          (r"shit\w*", 2), (r"twat\w*", 2), (r"wank\w*", 1), (r"bitch\w*", 1), (r"bastard\w*", 1), (r"prick\w*", 2),
          (r"arsehole\w*", 2), (r"asshole\w*", 1), (r"arse", 2), (r"dick\w*", 1), (r"slag\w*", 2), (r"slut\w*", 2),
          (r"whore\w*", 2), (r"tosser\w*", 1), (r"piss\w*", 1), (r"cock(s|burger|nose)?", 1), (r"knob\w*", 2),
          (r"nob(s|head|jockey)?", 1), (r"vagina", 1), (r"anal", 2), (r"dumass", 3), (r"jackass", 5), (r"douche\w*", 1),
          (r"minge", 1), (r"porn\w*", 1), (r"milf", 1), (r"dilf", 1), (r"slapper", 2), (r"tits", 1), (r"jizz\w*", 1),
          (r"bollocks", 1), (r"twinge", None)]

def _star(word, keep):
    if keep is None:
        return word
    # star one vowel after the kept letters (e.g. f*ck, sh*t, tw*t, c*nt): readable but not spelled out
    for i in range(keep, len(word)):
        if word[i].lower() in "aeiouy":
            return word[:i] + "*" + word[i + 1:]
    return word[:keep] + "*" + word[keep + 1:]

def censor(s):
    for pat, keep in CENSOR:
        if pat.startswith("motherf"):
            s = re.sub(r"(?i)\bmotherf\w*", lambda m: m.group(0)[0] + "*****f*****", s)
            continue
        s = re.sub(r"(?i)\b(?:" + pat + r")\b", lambda m: _star(m.group(0), keep), s)
    # words hidden inside compounds (dumbshit, shitcunt, fuckface ...)
    for core, keep in (("fuck", 1), ("cunt", 1), ("shit", 2), ("twat", 2), ("wank", 1), ("dick", 1), ("piss", 1),
                       ("bitch", 1), ("knob", 2), ("jizz", 1)):
        s = re.sub(r"(?i)" + core, lambda m: _star(m.group(0), keep), s)
    return s

SWEARY = re.compile(r"(?i)\b(f+u+c+k|f\*|cunt|c\*nt|shit|sh\*t|twat|tw\*t|wank|bitch|bastard|prick|arse\b|arseh|ass\b|asshole|"
                    r"dickhead|dick\b(?! (van dyke|turpin|whittington))|slag|slut|whore|tosser|piss|p\*ss|cock\b|cocks\b|c\*ck|"
                    r"knob|kn\*b|nob\b|vagina|fanny|minge|porn|milf|dilf|anal\b|boob|tits\b|nipple|inches in my|bum ?hole|"
                    r"horny|sex\b|jizz|j\*zz|c\*m|douche|d\*uche|ar\*e|b\*llbags|b\*mhole|d\*ck|sm\*ghead|t\*sspot|"
                    r"naughty list|dumass|jackass|dumbshit|shove it|slapper|red light|pot head|weed|w33d|drugs|fart\b|"
                    r"chicken choker|meat beater|cyclops|carrot polisher|eel wrestler|pipe layer|lick me|bad things|fecking|swear)")

# Slurs and mocking-a-condition designs: no sales copy written, listed for the owner to decide.
SKIP_OFFENSIVE = re.compile(r"(?i)\b(dyke|fag|queer|fucktard|turettes)\b")

# ---------------------------------------------------------------- casing
SMALL = {"and", "or", "of", "the", "a", "an", "in", "on", "to", "for", "my", "at", "by", "with", "but"}

def nice(s):
    """Title-case ALL-CAPS phrases, keep mixed case as it is."""
    s = re.sub(r"\s+", " ", s).strip(" -–—")
    letters = [c for c in s if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.6:
        words = []
        for i, w in enumerate(s.lower().split(" ")):
            if i and w in SMALL:
                words.append(w)
            elif w[:2] == "mc" and len(w) > 3:
                words.append("Mc" + w[2:].capitalize())
            else:
                words.append(w[:1].upper() + w[1:])
        s = " ".join(words)
        s = re.sub(r"\bI'm\b|\bim\b|\bIm\b", "I'm", s)
    return s

# ---------------------------------------------------------------- brands and names
DRINK_GENERIC = {x.lower() for x in """Beer|Lager|Cosmopolitan|Daiquiri|Espresso Martini|Fizz|Gin & Lemonade|Gin And Tonic|Mai Tai|
Manhattan|Margarita|Martini|Mojito|Pina Colada|Rose And Soda|Rose Wine|Vodka & Lemonade|White Wine|Wine N Soda|French 75|Golden Ales|
Americano|Appletini|Aviation|B 52|Brandy|Buttery Nipples|Tequila|Clover Clubs|Dry Gin|Gimlet|Gin|Highball|Jelly Shots|Liqueur|
Mind Eraser|Motor Oil|Panty Mans|Port|Prairie Oyster|Red Headed Slut|Rum|Screwdriver|Sherry|Vermouth|Whisky|Sex On The Beach|Woo Woo|
Sidecar|Mint Julep|Bloody Mary|Bloody Kir|Bloody Spritz|Bellini|Icons|Icons Shaun|Moscow Mule""".replace("\n", "").split("|")}
DRINK_FIX = {"guiness": "Guinness", "kronenberg": "Kronenbourg", "dissaronno": "Disaronno", "smirnofff": "Smirnoff",
             "strong bow": "Strongbow", "strongbow": "Strongbow", "stella": "Stella Artois", "bud": "Budweiser",
             "bud bottle": "Budweiser", "budweiser bottle": "Budweiser", "becks": "Beck's", "tetleys": "Tetley's",
             "john smiths": "John Smith's", "john smith's": "John Smith's", "corona bottle": "Corona", "old crafty": "Old Crafty Hen",
             "old speckled": "Old Speckled Hen", "badger fursty": "Badger Fursty Ferret", "banks amber": "Banks's Amber",
             "brothers toffee": "Brothers Cider", "dark n stormy": "Dark 'n' Stormy", "newcastle brown": "Newcastle Brown Ale",
             "mcewans": "McEwan's", "marstons": "Marston's", "theakstons": "Theakston", "caffreys": "Caffrey's",
             "kopparberg": "Kopparberg", "frosty jacks": "Frosty Jack's", "keo beer": "KEO", "hop house": "Hop House 13",
             "shandy carib": "Shandy Carib", "dg dragon": "Dragon Stout", "iron maiden": "Iron Maiden Trooper",
             "rumple minze": "Rumple Minze", "grouse": "The Famous Grouse", "fullers": "Fuller's", "youngs": "Young's",
             "samuel adams": "Samuel Adams", "sharps": "Sharp's", "jagermeister": "Jägermeister", "pedigree": "Pedigree",
             "golden sheep": "Black Sheep Golden Sheep", "greene king": "Greene King", "white star": "White Star",
             "white lightning": "White Lightning", "russian standard": "Russian Standard", "sourz": "Sourz"}
MIXER_BRANDS = {"coke": "Coca-Cola", "redbull": "Red Bull", "jack": "Jack Daniel's", "malibu": "Malibu", "yeaga": "Jägermeister"}

ILOVE_BRANDS = {"ac cars": "AC Cars", "audis": "Audi", "bentleys": "Bentley", "bmw's": "BMW", "bugatti": "Bugatti",
                "bumble": "Bumble", "crossfit": "CrossFit", "dodge's": "Dodge", "facebook": "Facebook", "fiat's": "Fiat",
                "fords": "Ford", "gmc's": "GMC", "jeeps": "Jeep", "kfc": "KFC", "mazdas": "Mazda", "mini's": "MINI",
                "mustang": "Ford Mustang", "nissans": "Nissan", "peugeot": "Peugeot", "pizza hut": "Pizza Hut",
                "porches": "Porsche", "toyotas": "Toyota", "sazuki's": "Suzuki", "tinder": "Tinder", "twitter": "Twitter",
                "volvos": "Volvo", "subaru's": "Subaru", "subway": "Subway", "jaguars": "Jaguar"}
ILOVE_BANDS = {"1d": "One Direction", "5sos": "5 Seconds of Summer", "beyonce": "Beyoncé", "dr. dre": "Dr. Dre",
               "drake": "Drake", "eminem": "Eminem", "justin bieber": "Justin Bieber", "kanye west": "Kanye West",
               "the vamps": "The Vamps", "will i am": "will.i.am", "the script": "The Script", "little mix": "Little Mix"}
ILOVE_GAMES = {"wii fit": ("Wii Fit", "Nintendo")}

MOTOR = {"budweiser": "Budweiser", "daimler": "Daimler", "delorean": "DeLorean", "fiat": "Fiat", "fiatlove": "Fiat",
         "ford": "Ford", "gm": "General Motors (GM)", "gremlin": "AMC Gremlin", "holden": "Holden", "honda": "Honda",
         "honda bike": "Honda", "honda wings black": "Honda", "impreza": "Subaru", "jeep": "Jeep", "kia": "Kia",
         "lamborghini": "Lamborghini", "lotus": "Lotus", "mazda": "Mazda", "mclaren": "McLaren", "ninja black": "Kawasaki",
         "nissan": "Nissan", "passat": "Volkswagen", "peugeot": "Peugeot", "proton": "Proton", "r1": "Yamaha",
         "renault": "Renault", "rover": "Rover", "saab": "Saab", "seat": "SEAT", "smart": "smart", "splitfire": "SplitFire",
         "sti": "Subaru", "subaru": "Subaru", "subaru wrx": "Subaru", "suzuki": "Suzuki", "toyota": "Toyota",
         "toyota sport": "Toyota", "trail blazer": "Chevrolet", "triumph blue": "Triumph", "triumph red": "Triumph",
         "vespa": "Vespa", "vespa black": "Vespa", "yokohama": "Yokohama"}

CAR_MAKES = [("Aston Martin", "Aston Martin"), ("Audi Bentley", "Audi and Bentley"), ("Audi", "Audi"), ("BMW", "BMW"),
             ("Bugatti", "Bugatti"), ("Dodge", "Dodge"), ("Jaguar", "Jaguar"), ("Mazda", "Mazda"),
             ("Mercedes", "Mercedes-Benz"), ("Porsche", "Porsche"), ("Range Rover", "Land Rover (Range Rover)"),
             ("Rolls Royce", "Rolls-Royce"), ("Subaru", "Subaru")]

GAMES = [("call of duty", "Activision"), ("battlefield", "Electronic Arts"), ("counter strike", "Valve"),
         ("csgo", "Valve"), ("team fortress", "Valve"), ("half life", "Valve"), ("portal", "Valve"), ("valve", "Valve"),
         ("destiny", "Bungie"), ("fall out", "Bethesda"), ("farcry", "Ubisoft"), ("rainbow 6", "Ubisoft"),
         ("fifa", "Electronic Arts"), ("madden", "Electronic Arts"), ("forza", "Microsoft"),
         ("gears of war", "Microsoft"), ("overwatch", "Blizzard Entertainment"), ("pro evolution", "Konami"),
         ("rust", "Facepunch Studios"), ("mlg", "Major League Gaming"), ("esea", "ESEA"), ("faze", "FaZe Clan"),
         ("obey", "the Obey Alliance team"), ("team liquid", "Team Liquid")]

def join(names):
    names = list(dict.fromkeys(n for n in names if n))
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]

# ---------------------------------------------------------------- disclaimers (CLAUDE.md templates)
def d_club(club, league=None):
    lg = f", {league}," if league else ""
    who = f"{club}{lg} or any club, league or player" if club else "any football club, league or player"
    return ("This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, "
            f"or affiliated with {who}. Club and player names are used only to describe the design and who it's for. "
            "All trademarks belong to their respective owners.")

def d_character(show, rights):
    return (f"This is an unofficial design inspired by {show}. It is not official merchandise and is not endorsed by, "
            f"sponsored by, or connected with {show} or {rights}, or any of their licensees. All names, characters and "
            "trademarks belong to their respective owners.")

def d_celeb(name):
    return (f"This is an unofficial novelty product made for fun. {name} has not endorsed, sponsored or approved this "
            "product, and Foxy Printing has no connection with them. The name is used only to describe the design.")

def d_game(owners):
    return (f"This is an unofficial, fan-made mug design produced by Foxy Printing. It is not made, endorsed or licensed by "
            f"{join(owners)}. All trademarks and game titles belong to their respective owners and are used only to "
            "identify the theme.")

def d_band(name):
    return (f"This is an unofficial fan design. It is not endorsed by, or connected with, {name}, their management or "
            "record label. All names and trademarks belong to their respective owners.")

def d_brand(names):
    n = join(names)
    many = len(set(names)) > 1
    return (f"This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {n}. {n} "
            f"{'are trademarks of their owners and are' if many else 'is a trademark of its owner and is'} used only to "
            "describe the design theme.")
