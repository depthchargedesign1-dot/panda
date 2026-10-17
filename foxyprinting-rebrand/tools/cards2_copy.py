"""Name-themed cards, second batch: description rewrite (catalogue audit 9 Oct 2026, Fix 2).

Usage: python3 -I cards2_copy.py EXPORT.jsonl OUT_DIR

Covers the old ACTIVE "Sport Cards", "Celebrity Cards", "Musician Cards", "Music Cards", "Personalised Cards"
(Bollywood / WWE / game designs), "Animal Cards" and "Valentines Cards" listings (2017-era eBay HTML).
Funny Cards and Adult Cards are NOT covered here: rude slogans and slurs need a separate, hand-checked pass.

Facts come only from plan/product-facts.md "Personalised cards" (same as cards_copy.py). Each title is classified
into a kind (F1, club, wrestler, boxer, footballer, vehicle brand, Bollywood, game, celebrity, musician, animal,
Valentine, generic) which sets the wording and the CLAUDE.md disclaimer template. Generic designs get no disclaimer.

Writes OUT_DIR/<family>-descriptions.csv (Handle, Body (HTML)), review.csv, problems.csv, tag-ids.txt, samples.html.
"""
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cards_copy import BANNED, esc, h, pick, text  # noqa: E402

FAMILIES = {"Sport Cards": "sport-cards", "Celebrity Cards": "celebrity-cards", "Musician Cards": "musician-cards",
            "Music Cards": "music-cards", "Personalised Cards": "bollywood-wwe-game-cards", "Animal Cards": "animal-cards",
            "Valentines Cards": "valentines-cards"}
BOIL = [r"\(SA\)?", r"\bTHEME INSPIRED\b", r"\bINSPIRED THEME\b", r"\bTheme\b", r"\bInspired\b", r"\bStyle\b", r"\bPERSONALISED\b",
        r"\bPersonalised\b", r"\bKids Adult\b", r"\bFUNNY\b", r"\bFunny\b", r"\bBirthday Card\b", r"\bBirthdary Card\b", r"\bCard\b",
        r"\bKids\b", r"\bAdult\b", r"\bGift Present\b", r"\bNew 2017\b", r"\bCelebrity\b", r"\bSports\b", r"\bBirthday\b",
        r"\bFan TEAM\b", r"\bFOOTBALL TEAM\b", r"\bFan\b", r"\bKE\b", r"\bSJ\b", r"\bBM\d?\b", r"\bValentines Day\b", r"\bVALENTINES\b"]
VEHICLE = re.compile(r"\b(Aston Martin|BMW|Bugatti|Chev|Dunlop|Ford|Honda|Kawasaki|Lambo|Lamborghini|Maclaren|Mazda|Mustang|Pagani|"
                     r"Porsche|Rangerover|Range Rover|Suzuki|Yamaha|Ducati|Ferrari|Audi|Nissan|Subaru|Mitsubishi|Triumph|Harley|"
                     r"Volkswagen|VW|Jaguar|Bentley|Rolls Royce|Mini|Vauxhall|Toyota)\b", re.I)
PROFANE = re.compile(r"\b(fuck\w*|cunt\w*|shit\w*|twat|wank\w*|bitch\w*|dick\w*|cock|bastard|slag|arse|arsehole|knob|nob|bellend|tits|"
                     r"boobs|faggot|poof|bender|cum|anal|blow ?job|penis|scrotum|willy|balls)\b", re.I)
DANCE_SHOWS = {"Dance Moms"}
FIX = {
    # music
    "AC DC Heavy Metal Hard Rock Classic Bands": "AC/DC", "AOA Rock Pop Dance": "AOA", "30 Seconds To Mars Jared Leto": "30 Seconds to Mars",
    "30 Seconds To Mars": "30 Seconds to Mars", "Adele Adkins": "Adele", "Alicia Key": "Alicia Keys", "Amy Whinehouse": "Amy Winehouse",
    "Arianna Grande": "Ariana Grande", "Areana Grande": "Ariana Grande", "Art Yoona SNS": "Yoona", "Im Yoona": "Yoona",
    "Avicii Wake Me Up": "Avicii", "House Dj Avicii": "Avicii", "B A P": "B.A.P", "Baby Metal": "Babymetal",
    "Babymetal Japanese Band": "Babymetal", "Beatles Black And White": "The Beatles", "Behemoth Guitar BW Mask": "Behemoth",
    "Beyonce Blue": "Beyonce", "Beyonce Heat": "Beyonce", "Black Eyed": "Black Eyed Peas", "Blink 1": "Blink-182", "Blink 2": "Blink-182",
    "Bryan Sdams": "Bryan Adams", "Cheryl Tweedy": "Cheryl", "Cheryl Cole": "Cheryl", "Closeup Girls Generation": "Girls' Generation",
    "Girls Generation": "Girls' Generation", "Snsdkpop": "Girls' Generation", "DC1 Miley Cyrus": "Miley Cyrus", "Miley Cirus": "Miley Cyrus",
    "Daft Punk (2)": "Daft Punk", "DAL Shabet": "Dal Shabet", "Disturbed Fantasycelebrity": "Disturbed", "Dnce": "DNCE", "Dnce Retro": "DNCE",
    "Eazy E Nwa 1 Gangsta": "Eazy-E", "Eazy E Nwa 2 Gangsta": "Eazy-E", "Epica Simone": "Epica", "Emilie Autumn Liddell": "Emilie Autumn",
    "Five Second Of Summers": "5 Seconds of Summer", "5sos": "5 Seconds of Summer", "G Dragon Bigbang": "G-Dragon", "Ghost B C G": "Ghost",
    "Girls DAY": "Girl's Day", "Hardwell DJ": "Hardwell", "Harry Styles Landscape": "Harry Styles", "Harry Styles Red": "Harry Styles",
    "Hollywood Undead Notes": "Hollywood Undead", "Iron Maiden Bands": "Iron Maiden", "Jabberwockies Bands": "Jabberwockies",
    "Jessie J Minnie Mouse": "Jessie J", "K Pop Miss A Suzy": "Suzy", "Kamelot Poetry": "Kamelot", "Katie Perry": "Katy Perry",
    "Kiss Band": "Kiss", "Kiss Heavy Metal Rock": "Kiss", "Kylie Minogues": "Kylie Minogue", "Lacuna Coil Cristina Scabbia": "Lacuna Coil",
    "Lamb OF GOD Lacuna Coil": "Lamb of God", "Lady Gaga Sexy": "Lady Gaga", "Little Mix Phones": "Little Mix", "Lorde Indie": "Lorde",
    "Maddona": "Madonna", "Maisey Williams": "Maisie Williams", "Mark Bolan": "Marc Bolan", "Maroon": "Maroon 5", "Megadeth Band": "Megadeth",
    "Metallica Band": "Metallica", "Michael Jackson This Is It": "Michael Jackson", "Michael Jackson Xscape": "Michael Jackson",
    "Mj Blue": "Michael Jackson", "Minzy Kpop": "Minzy", "Namie Amuru": "Namie Amuro", "Nicki Minaj Purple": "Nicki Minaj",
    "Nikki Minaj": "Nicki Minaj", "Nicole Sherzinger": "Nicole Scherzinger", "Orianthi Panagaris": "Orianthi", "Ozzy Osbourn": "Ozzy Osbourne",
    "Paula Abdu;": "Paula Abdul", "Psy Gangnam": "Psy", "Gangnam": "Psy", "Queen Band": "Queen", "Queen Retro": "Queen",
    "Bohemian Rhapsody": "Queen", "Rhianna Denim": "Rihanna", "Rhianna Red": "Rihanna", "Sexy Rhianna": "Rihanna", "Slayer Groups": "Slayer",
    "Sistar K": "Sistar", "T A T U": "t.A.T.u.", "Will I Am": "will.i.am", "Zac Effrom Pose": "Zac Efron", "Zac Effron Topless": "Zac Efron",
    "Alt J": "Alt-J", "Fx": "f(x)", "Iu": "IU", "Bts": "BTS", "Btob": "BTOB", "Cnblue": "CNBLUE", "2ne1": "2NE1", "2pm": "2PM", "Got7": "GOT7",
    "B1a4": "B1A4", "4minute": "4Minute", "Tech N9ne": "Tech N9ne", "Deadmau5": "deadmau5",
    # celebrities
    "Aishwariya Rai": "Aishwarya Rai", "Marylin Monroe": "Marilyn Monroe", "Paeis Hilton": "Paris Hilton", "Robert Downey": "Robert Downey Jr",
    "Rosie Huntington": "Rosie Huntington-Whiteley", "Jodi Lyn O Keefe": "Jodi Lyn O'Keefe", "Shanzahn Padamsee": "Shazahn Padamsee",
    # sport
    "Chelsea Fc": "Chelsea FC", "Conor Mcgregor": "Conor McGregor", "Conor Mcgregor MMA": "Conor McGregor", "Conor Mcgregor UFC": "Conor McGregor",
    "Conor Mcgregor New Design 2 MMA": "Conor McGregor", "Conor Mcgregor New Design 3 MMA": "Conor McGregor",
    "Conor Mcgregor New Design 4 MMA": "Conor McGregor", "Broc Lesnar MMA": "Brock Lesnar", "Carlos Tevez SJ1": "Carlos Tevez",
    "Cristiano Ronaldo Portuguese": "Cristiano Ronaldo", "Eden Hazard Belgian": "Eden Hazard", "Novak Djokovic-1": "Novak Djokovic",
    "Djokovic": "Novak Djokovic", "Olympics NEW": "Olympics", "Olympics New 2 Usain Bolt": "Usain Bolt", "Olympics New 3 Mo Farah": "Mo Farah",
    "Im Keeping You": "I'm Keeping You", "To My Hedge Hog": "To My Hedgehog", "Shelby Brothers Design 2": "Shelby Brothers",
    "Rafael Nadel": "Rafael Nadal", "Rafeal Dos Anjos UFC": "Rafael dos Anjos", "Sergio Agureo": "Sergio Aguero",
    "Sergio Aguero Soccer": "Sergio Aguero", "Sho Gun Rua MMA MMA": "Shogun Rua", "VAN Persie": "Robin van Persie", "Van Persie": "Robin van Persie",
    "Rugby World CUP": "Rugby World Cup", "Michael Jordan Clean": "Michael Jordan", "Kobe Bryant Invincible": "Kobe Bryant",
    "Lebron James American Basketball": "LeBron James", "Lebron James": "LeBron James", "Stephen Curry Basketball": "Stephen Curry",
    "Maria Sharapova Tennis": "Maria Sharapova", "Lionel Messi Soccer": "Lionel Messi", "Luis Suarez Uruguayan": "Luis Suarez",
    "James Rodriguez Spanish": "James Rodriguez", "Muhammad Ali Boxer": "Muhammad Ali", "Rodrieguez": "James Rodriguez",
    "Eroc Camtpma Man U": "Eric Cantona", "Saido Mane Liverpool": "Sadio Mane", "Dortmund Fan2 Happy": "Borussia Dortmund",
    "Dortmund": "Borussia Dortmund", "Dortmund Happy": "Borussia Dortmund", "Manchester Utd.": "Manchester United", "Robinho Nike Brand": "Robinho", "Neymar Jr. PSG": "Neymar", "Ngolo Kante": "N'Golo Kante",
    "Phillipe Coutinho Liverpool": "Philippe Coutinho", "ICE Hockey": "Ice Hockey", "Euro 2016 France": "Euro 2016",
    "Happy Ford Mustang RED Cars": "Ford Mustang", "Happy Ford Mustang5.0 Cars": "Ford Mustang 5.0", "Happy Orange Lambo Cars": "Lamborghini",
    "Lambo Lover": "Lamborghini", "Bugatti Car": "Bugatti", "Chev Car": "Chevrolet", "Mustang Car": "Ford Mustang", "Mazda RS": "Mazda",
    "Honda Sport Concept Car": "Honda", "Red Corvette Rear": "Chevrolet Corvette", "Car 2 Car": "Car",
    # wrestling
    "Big Case": "Big Cass", "Golddust": "Goldust", "Sheamus Celtic": "Sheamus", "Elias Samson Design": "Elias Samson",
    "The Usos New Deisgn": "The Usos",
    # Bollywood
    "2 States 1": "2 States", "2 States 2": "2 States", "Jolly Llb2 1": "Jolly LLB 2", "Jolly Llb2 2": "Jolly LLB 2", "Krrish3": "Krrish 3",
    "Nh10": "NH10", "Creature 3d": "Creature 3D", "PK": "PK",
    # games
    "Bf4 Captain Rex": "Battlefield 4", "Battlefield 31": "Battlefield 3", "DLC Ff13": "Final Fantasy XIII", "DMC": "Devil May Cry",
    "DMC Vergil": "Devil May Cry", "RA3 Girls": "Red Alert 3", "NFS The Run Irina Shayk And Chrissy": "Need for Speed The Run",
    "Fallout Photo Manipulation": "Fallout", "Mass Effect Wallpaper": "Mass Effect", "R8 In Japan Gt5": "Gran Turismo 5",
    "Crysis 2 Shooter": "Crysis 2", "Need Fo Speed 2015": "Need for Speed", "Need Fo Speed Payback": "Need for Speed Payback",
    "Battlefield 1 Xbox": "Battlefield 1", "Citroen GT Race Car": "Gran Turismo", "Mercedes Benz AMG": "Gran Turismo",
}
WORDFIX = [(r"\bMortal Komabt\b", "Mortal Kombat"), (r"\bAssassins Creed\b", "Assassin's Creed"), (r"\bLabradoor\b", "Labrador"),
           (r"\bDalmation\b", "Dalmatian"), (r"\bBuldog\b", "Bulldog"), (r"\bGumpy\b", "Grumpy"), (r"\bGerman Shep\b", "German Shepherd"),
           (r"\bAvatar 3d\b", "Avatar 3D")]
LOWER_CAPS = {"OF", "AND", "YOU", "MY", "FOR", "IS", "MAN", "JOB", "NOB", "RED", "ICE", "DAY", "JOE", "VAI", "MOB", "OKU", "NEW", "CUP",
              "VAN", "HIP", "HOP", "WIZ", "GOD", "TO", "ME", "MOO", "HOG", "IM"}
GENERIC_NAMES = {
    "Angels Wings", "Asian Guitar", "Asian Oriental", "Australian Singer", "Beats Girl", "Boy Guitar", "Boy Toy", "Break Dance",
    "Brunettes Women", "Cello", "Club Girl D J", "Console Pioner Zhulanov", "Dance Hip Hop", "Dancer Red Leather Jacket",
    "Dark Reaper Skeleton", "Deca String", "Dj Cropped", "Eadphones Face", "Electronic Disc Jockey Gangsta", "Entertainment", "Face Girls",
    "Girl Guitar", "Green Eyed", "Guitar Girl", "Guitar Male", "Guitar Soul My Liffe Notes", "Guitar Tattoos", "Guitars Musician", "Guy Mood",
    "Hip Hop Dance", "Headphones", "Headphones DJ", "Headphones Women", "Hip Hop", "Musical", "Musician", "On Stage", "Pretty Nature",
    "Singers", "Singing Girl", "Singing The Girl Retro", "South Korean Singer", "Speakers Face", "Stellar Synth", "Tattoo Tattoos",
    "Tattoos Piercings", "Violinist", "Women Dance", "Boys Band Korean", "RES Dj", "Quigley", "Univz", "Julie", "Crayon",
    "Atv Motocross Quadrocycle", "Australian Cricketer", "Bangladesh Catcher", "Cricket Bat And Ball", "Cricket Speed Ball", "Cricket Wicket",
    "Girl Skateboarder", "Ice Hockey", "Legends", "Motorsport Race", "Mountain Biking", "Mountain Skiing", "One Goal", "West Indies Catcher",
    "New Zealand Catch", "New Zealand Player", "Erko Jun", "Tavi Castro", "Concept Car", "Yellow Car Side View",
}
CELEB_IN_MUSIC = {"Brad Pitt", "Kate Upton", "Kristen Stewart", "Sophia Bush", "Stacy Keibler", "Stana Katic", "Zac Efron", "Sophia Myles",
                  "Nora Arnezeder", "Maisie Williams"}
BRANDS = {"Gibson Guitar": "Gibson", "Converse": "Converse", "Redbull": "Red Bull", "Red Bull Skydiver": "Red Bull"}
GAME_AS_SPORT = {"Fifa 2017": "FIFA 17", "Fifa Footy": "FIFA", "NHL 2017": "NHL 17"}
CLUB_TAIL = re.compile(r"^(.+?) (Spurs|Man U|Man City|Liverpool|Gunners|Barca|Fc Barcelona|Barcelona|Real Madrid|Real|PSG|Bayern M|"
                       r"Toffees|Chelsea|Manchester United|Brazil|Sweden|India|Portuguese|Wimbledon|Spanish|Belgian|Uruguayan)$")
CLUB_NAMES = {"Spurs": "Tottenham Hotspur", "Man U": "Manchester United", "Man City": "Manchester City", "Gunners": "Arsenal",
              "Barca": "FC Barcelona", "Fc Barcelona": "FC Barcelona", "Barcelona": "FC Barcelona", "Real": "Real Madrid",
              "Real Madrid": "Real Madrid", "PSG": "Paris Saint-Germain", "Bayern M": "Bayern Munich", "Toffees": "Everton",
              "Liverpool": "Liverpool", "Chelsea": "Chelsea", "Manchester United": "Manchester United"}
SHOWS = [(r"\s+Of Thrones$", "Game of Thrones"), (r"\s+Peaky Blinders$", "Peaky Blinders")]
SHOW_NAMES = {"Sleepy Hollow": "Sleepy Hollow", "Ewok Defending Nuts From Squirrel": "Star Wars", "Yoda": "Star Wars", "Blake Lively The Shallows": "The Shallows"}


def classify(fam, title):
    t = title
    if fam == "Animal Cards":
        return "animal"
    if fam == "Valentines Cards":
        return "valentine"
    if fam == "Celebrity Cards":
        return "celebrity"
    if fam in ("Musician Cards", "Music Cards"):
        return "musician"
    if re.search(r"\bBollywood\b", t, re.I):
        return "bollywood"
    if re.search(r"\b(WWE|Wrestling)\b", t, re.I):
        return "wrestler"
    if re.search(r"\bGame\b", t) or re.search(r"\b(Call Of Duty|Mass Effect)\b", t, re.I):
        return "game"
    if re.search(r"\bF1\b", t):
        return "f1"
    if re.search(r"\bBoxing\b", t, re.I):
        return "boxer"
    if re.search(r"\b(Fan TEAM|FOOTBALL TEAM)\b", t, re.I) or re.search(
            r"\b(Cardinals|Panthers|Broncos|Nuggets|Hornets|Bulls|Jaguars|Dolphins|Vikings|Patriots|Lakers|Celtics|Warriors|Cowboys|"
            r"Packers|Steelers|Raiders|Giants|Eagles|Seahawks|Chiefs|Rams|Saints|Bears|Jets|Bills|Ravens|Texans|Colts|Titans|"
            r"Chargers|49ers|Falcons|Buccaneers|Lions|Browns|Bengals|Redskins|Knicks|Nets|Heat|Spurs|Rockets|Clippers|Celtic)\b", t):
        return "club"
    if re.search(r"\bFootball\b|\bBarca\b|\bBarcelona\b|\bGunners\b|\bPSG\b|\bBayern\b", t, re.I):
        return "footballer"
    if VEHICLE.search(t):
        return "vehicle"
    if re.search(r"\b(Car|Bike|Racer|Motorbike)\b", t, re.I):
        return "generic-vehicle"
    return "sport-person"


def refine(kind, theme):
    """Second pass on the cleaned name: generic designs, brands, TV characters, celebrities filed under music."""
    show = None
    for rx, name in SHOWS:
        if re.search(rx, theme):
            return "show", re.sub(r"\s+Design \d+$", "", re.sub(rx, "", theme).strip()), name
    if theme in SHOW_NAMES:
        return "show", theme if theme != "Blake Lively The Shallows" else "Blake Lively", SHOW_NAMES[theme]
    if theme in BRANDS:
        return "brand", BRANDS[theme], None
    if theme in GAME_AS_SPORT:
        return "game", GAME_AS_SPORT[theme], None
    if theme in GENERIC_NAMES:
        return ("generic-music" if kind == "musician" else "generic-sport" if kind not in ("generic-vehicle", "vehicle") else "generic-vehicle"), theme, None
    if kind in ("club", "footballer", "sport-person"):
        theme = re.sub(r"^Signed For ", "", theme)
        m = CLUB_TAIL.match(theme)
        if m and m.group(1) not in CLUB_NAMES and m.group(1) != "AFC":
            club = CLUB_NAMES.get(m.group(2))
            return ("footballer" if club else kind if kind != "club" else "sport-person"), m.group(1), club
    if kind == "musician" and theme in CELEB_IN_MUSIC:
        return "celebrity", theme, None
    return kind, theme, show


def theme_of(title, valentine=False):
    s = title
    if valentine:
        s = re.sub(r"\b(Girlfriend|Boyfriend|Hubby|Wife|Lover)\b", " ", s, flags=re.I)
    s = re.sub(r"\bDogs AND (Funny )?Puppy\b|\bKirsten\b|\bNEW Design\b|\bPhotographer\d\b", " ", s, flags=re.I)
    glued = re.search(r"\b(?!(?:Krrish|Deadmau|Mustang)\d)[A-Z][a-z]{2,}(\d)\b", s)
    s = re.sub(r"\b(?!(?:Krrish|Deadmau|Mustang)\d)([A-Z][a-z]{2,})\d\b", r"\1", s)
    s = re.sub(r"(?<=[a-z]) UFC\b", " ", s)
    s = re.sub(r"\bForce \d India\b", "Force India", s)
    s = re.sub(r"\bHaas \d F1\b", "Haas F1", s)
    design = glued.group(1) if glued else None
    m = re.search(r"\bKE(\d+)\b", s)
    if m:
        design = m.group(1)
    for b in BOIL:
        s = re.sub(b, " ", s, flags=re.I)
    s = re.sub(r"\s+(Bollywood|WWE|Wrestling|Boxing|Football|Game|Music|Movie)\b", " ", s, flags=re.I)
    s = re.sub(r"\bF1\b", " ", s)
    s = re.sub(r"\s+", " ", s).strip(" -–|,")
    m = re.search(r"\s+(\d{1,2})$", s)
    if m and not re.search(r"\b(Battlefield|Bioshock|Birds|States|Llb2|Blink|Effect|Duty|Mustang|Pagani Zonda)\s+\d{1,2}$", s, re.I):
        design = design or m.group(1)
        s = s[:m.start()]
    s = re.sub(r"\s+\d$", "", s) if re.search(r"\b(Mustang|Pagani Zonda)\s+\d$", s) else s
    words = []
    for w in s.split():
        if w.isupper() and len(w) > 3 and w not in ("WWE", "ABCD2", "NASA"):
            w = w.capitalize()
        words.append(w)
    s = " ".join(w.capitalize() if w in LOWER_CAPS else w for w in words)
    s = re.sub(r"\s+\bNew$", "", s)
    for rx, rep in WORDFIX:
        s = re.sub(rx, rep, s)
    s = re.sub(r"\s+", " ", s).strip(" -–|,")
    s = FIX.get(s, s)
    s = re.sub(r"\bMclaren\b|\bMaclaren\b", "McLaren", s)
    s = re.sub(r"\bRangerover\b", "Range Rover", s)
    s = re.sub(r"\bKevin Ovens\b", "Kevin Owens", s)
    s = re.sub(r"\bCm Punk\b", "CM Punk", s)
    s = re.sub(r"\bAj s\b|\bAJ s\b", "AJ Styles", s)
    s = re.sub(r"\bKelly Brooke\b", "Kelly Brook", s)
    s = re.sub(r"^His Or Hers.*", "His or Hers", s, flags=re.I)
    return s.strip(" -–|,"), design


GENERIC = re.compile(r"^(car|car lover|car yellow|car purple|car card|bike racer|black bike|blue bike|gb car|american muscle car|"
                     r"his or hers|sports person|superhero)$", re.I)

KINDS = {
    # kind: (who, keyword template, what the design is)
    "f1": ("motor racing fan", "personalised {t} F1 birthday card", "a {t} motor racing design"),
    "club": ("sports fan", "personalised {t} fan birthday card", "a {t} fan design"),
    "footballer": ("football fan", "personalised {t} football birthday card", "a {t} football design"),
    "wrestler": ("wrestling fan", "personalised {t} wrestling birthday card", "a {t} wrestling design"),
    "boxer": ("boxing fan", "personalised {t} boxing birthday card", "a {t} boxing design"),
    "sport-person": ("sports fan", "personalised {t} sports birthday card", "a {t} sports design"),
    "vehicle": ("petrolhead", "personalised {t} birthday card", "a {t} design"),
    "generic-vehicle": ("petrolhead", "personalised {t} birthday card", "a {t} design"),
    "bollywood": ("Bollywood fan", "personalised {t} Bollywood birthday card", "a {t} Bollywood design"),
    "game": ("gamer", "personalised {t} gaming birthday card", "a {t} gaming design"),
    "celebrity": ("fan", "personalised {t} birthday card", "a {t} design"),
    "musician": ("music fan", "personalised {t} music birthday card", "a {t} music design"),
    "animal": ("animal lover", "personalised {t} birthday card", "a {t} design"),
    "valentine": ("partner", "personalised Valentine's Day card", "a {t} Valentine's design"),
    "show": ("TV and film fan", "personalised {t} birthday card", "a {t} design inspired by {show}"),
    "brand": ("fan", "personalised {t} birthday card", "a {t} inspired design"),
    "generic-music": ("music fan", "personalised {t} music birthday card", "a {t} music design"),
    "generic-sport": ("sports fan", "personalised {t} sports birthday card", "a {t} sports design"),
}


def disclaimer(kind, theme, show=None):
    n = theme
    if kind in ("f1", "club", "footballer", "boxer", "sport-person"):
        extra = ", Formula 1" if kind == "f1" else f", {show}" if show else ""
        body = (f"This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or "
                f"affiliated with {n}{extra}, or any club, team, league or player. Names are used only to describe the design and who "
                "it's for. All trademarks belong to their respective owners.")
    elif kind == "wrestler":
        body = (f"This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or "
                f"affiliated with {n}, WWE, or any wrestling promotion or wrestler. Names are used only to describe the design and who "
                "it's for. All trademarks belong to their respective owners.")
    elif kind == "show":
        body = (f"This is an unofficial design inspired by {show}. It is not official merchandise and is not endorsed by, sponsored by, or "
                f"connected with {show}, its makers or rights holders, or any of their licensees. Any actors pictured have not endorsed, "
                "sponsored or approved this product, and Foxy Printing has no connection with them. All names, characters and "
                "trademarks belong to their respective owners.")
    elif kind == "brand":
        body = (f"This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {n}. {n} is a trademark "
                "of its owner and is used only to describe the design theme.")
    elif kind == "vehicle":
        body = (f"This is an unofficial product made by Foxy Printing. It is not made, endorsed or approved by {n} or its maker. "
                "Brand and model names are trademarks of their owners and are used only to describe the design theme.")
    elif kind == "game":
        body = (f"This is an unofficial, fan-made card produced by Foxy Printing, inspired by {n}. It is not made, endorsed or licensed by "
                "the game's publisher or any console maker. All trademarks, characters and game titles belong to their respective "
                "owners and are used only to identify the theme.")
    elif kind == "bollywood":
        body = (f"This is an unofficial design inspired by {n}. It is not official merchandise and is not endorsed by, sponsored by, or "
                f"connected with {n}, the film makers or rights holders, or any of their licensees. Any actors pictured have not "
                "endorsed, sponsored or approved this product, and Foxy Printing has no connection with them. All names and "
                "trademarks belong to their respective owners.")
    elif kind == "celebrity":
        body = (f"This is an unofficial novelty card made for fun. {n} has not endorsed, sponsored or approved this product, and Foxy "
                "Printing has no connection with them. The name is used only to describe the design.")
    elif kind == "musician" and theme in DANCE_SHOWS:
        body = (f"This is an unofficial design inspired by {n}. It is not official merchandise and is not endorsed by, sponsored by, or "
                f"connected with {n}, its makers or rights holders, or any of their licensees. All names and trademarks belong to "
                "their respective owners.")
    elif kind == "musician":
        body = (f"This is an unofficial fan design. It is not endorsed by, or connected with, {n}, their management or record label. "
                "All names and trademarks belong to their respective owners.")
    else:
        return ""
    return "\n<h3>Please note</h3>\n<p class=\"disclaimer\">" + esc(body) + "</p>"


def build(p, kind, theme, design, show=None):
    key = p["handle"]
    t = esc(theme)
    who, kwt, whatt = KINDS[kind]
    kw = kwt.format(t=t)
    design_txt = f"a {t} design" if kind == "show" and show == theme else whatt.format(t=t, show=esc(show or ""))
    dz = f" (design {design})" if design else ""
    valentine = p["productType"] == "Valentines Cards"
    occasion = "Valentine's Day" if valentine else "birthday"
    if valentine:
        opener = pick([
            f"Say it properly this year with a {kw}, printed on thick card in our North Yorkshire workshop and posted 1st Class.",
            f"Our {kw} is made to order with your names and your own message, for a boyfriend, girlfriend, husband or wife.",
            f"Looking for a Valentine's card that's a bit more personal? This {kw} is printed with the names and message you choose.",
        ], key, "o")
        h2 = pick(["Personalised Valentine's Day card with names", "Personalised Valentine's card for him or her",
                   "Personalised Valentine's Day card"], key, "h")
        what = (f"The front shows {design_txt}{dz}. Add both names and your own front message when you order, and we can print a "
                "message inside too.")
        pers = "names, front message and inside message"
        bullet3 = "Personalised with your names and your own message"
    else:
        opener = pick([
            f"Make their day with a {kw}, printed on thick card in our North Yorkshire workshop and posted 1st Class.",
            f"Our {kw} is a fun way to wish a {who} happy birthday, with their name and age added to the design.",
            f"Looking for a card for a {who}? This {kw} is made to order with the name, age and message you choose.",
        ], key, "o")
        h2 = pick([kw[0].upper() + kw[1:], f"{t} birthday card with name and age", f"Personalised {t} birthday card"], key, "h")
        what = pick([
            f"The front shows {design_txt}{dz}. Add the birthday name, age and your own front message when you order, and we can print a message inside too.",
            f"You get {design_txt}{dz}, printed with the name and age you give us. Want a message inside? Add it when you order and we'll print that as well.",
            f"It's {design_txt}{dz}, personalised with the name and age of the birthday {who}. We can print inside and out, so add your own inside message when you order.",
        ], key, "w")
        pers = "name, age, front message and inside message"
        bullet3 = "Personalised with their name, age and your own message"
    check_line = " We print exactly what you enter, so please double-check names and spelling."
    pool = [
        "Printed on 350gsm silk art board, much thicker than the usual 240gsm card",
        "Printed A4 and folded to A5, then machine cut and folded for a crisp finish",
        bullet3,
        "Printed inside and out if you want a message inside",
        "Comes with a free white envelope",
        "Posted flat in a board-backed envelope so it arrives uncreased",
    ]
    order = sorted(range(len(pool)), key=lambda i: h(key + "b" + str(i)))[:5]
    bullets = "\n".join(f"<li>{pool[i]}</li>" for i in sorted(order))
    if valentine:
        closer = pick([
            "Pair it with a personalised mug for a Valentine's gift that's sorted in one go. Custom designs on request: call 01439 771468.",
            "Want your own photo or wording on it? We can design a custom card: call 01439 771468.",
            "Add a personalised mug or print for a matching Valentine's gift. Custom card designs on request: call 01439 771468.",
        ], key, "c")
    else:
        closer = pick([
            "Can't find the design you're after? We can make a custom birthday card: call 01439 771468.",
            f"Pair the {kw} with a personalised mug for a birthday gift that's sorted in one go. Custom cards on request: call 01439 771468.",
            f"Buying for a {who}? Add a personalised mug or poster for a matching gift. Custom card designs on request: call 01439 771468.",
        ], key, "c")
    body = (f"<p>{opener}</p>\n<h2>{h2}</h2>\n<p>{what}{check_line}</p>\n"
            f"<h3>Why you'll love it</h3>\n<ul>\n{bullets}\n</ul>\n"
            "<h3>Size &amp; details</h3>\n<ul>\n<li>Size: printed A4, folded to A5</li>\n<li>Card: 350gsm silk art board</li>\n"
            "<li>Finish: machine cut and folded</li>\n<li>Includes: free white envelope</li>\n"
            f"<li>Personalisation: {pers}</li>\n</ul>\n"
            "<h3>Delivery</h3>\n<p>Sent Royal Mail 1st Class, dispatched the same day, or the next working day at busy times. "
            "It's posted flat in a board-backed envelope.</p>\n"
            f"<p>{closer}</p>")
    named = not GENERIC.match(theme) and kind not in ("animal", "valentine", "generic-vehicle", "generic-music", "generic-sport")
    if named:
        body += disclaimer(kind, theme, show)
    if len(text(body).split()) > 350:
        body = body.replace(f"<p>{closer}</p>", "<p>Custom card designs on request: call 01439 771468.</p>")
    return body, named, occasion


def check(body, theme, named):
    pr = []
    if body.count("<h2") != 1:
        pr.append("h2")
    if re.search(r"style=|<span|<h1|<table|<br|<img|\[|\]", body):
        pr.append("html")
    nd = re.sub(r'<p class="disclaimer">.*?</p>', "", body, flags=re.S).replace(esc(theme), "")
    m = BANNED.search(text(nd))
    if m:
        pr.append("banned:" + m.group(0))
    if PROFANE.search(theme):
        pr.append("profane theme")
    if re.search(r"Anniversary Print|Wallpaper|Netflix|Naked", theme):
        pr.append("not a plain card / needs the rude-card pass")
    w = len(text(body).split())
    if not 180 <= w <= 350:
        pr.append(f"words {w}")
    if not theme or len(theme) < 2 or not re.search(r"[A-Za-z]", theme):
        pr.append("no theme")
    if named and 'class="disclaimer"' not in body:
        pr.append("disclaimer")
    return pr


def main(src, out):
    os.makedirs(out, exist_ok=True)
    P = {}
    for line in open(src, encoding="utf-8"):
        o = json.loads(line)
        if "__parentId" not in o:
            P[o["id"]] = o
    files = {f: [] for f in FAMILIES}
    review, probs, tag_ids, seen = [], [], [], {}
    for p in P.values():
        if p["productType"] not in FAMILIES or p["status"] != "ACTIVE":
            continue
        if "<h2" in (p["descriptionHtml"] or "") and not re.search(r"style=|<span", p["descriptionHtml"] or ""):
            continue  # already rewritten
        kind = classify(p["productType"], p["title"])
        theme, design = theme_of(p["title"], p["productType"] == "Valentines Cards")
        kind, theme, show = refine(kind, theme)
        body, named, _ = build(p, kind, theme, design, show)
        pr = check(body, theme, named)
        if body in seen:
            pr.append("duplicate of " + seen[body])
        seen[body] = p["handle"]
        if pr:
            probs.append([p["handle"], p["title"], kind, theme, ";".join(pr)])
            continue
        files[p["productType"]].append([p["handle"], body])
        review.append([p["handle"], p["title"], p["productType"], kind, theme, "yes" if named else "no", len(text(body).split())])
        if named and "third-party-name" not in p["tags"]:
            tag_ids.append(p["id"])
    for fam, rows in files.items():
        with open(os.path.join(out, f"{FAMILIES[fam]}-descriptions.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Handle", "Body (HTML)"])
            w.writerows(rows)
    with open(os.path.join(out, "review.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Handle", "Title", "Family", "Kind", "Theme name used", "Disclaimer", "Words"])
        w.writerows(review)
    with open(os.path.join(out, "problems.csv"), "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([["Handle", "Title", "Kind", "Theme", "Problem"]] + probs)
    open(os.path.join(out, "tag-ids.txt"), "w").write("\n".join(tag_ids) + "\n")
    with open(os.path.join(out, "samples.html"), "w", encoding="utf-8") as f:
        f.write("<!doctype html><meta charset=utf-8><title>Card samples 2</title><style>body{font-family:sans-serif;max-width:820px;"
                "margin:auto;padding:16px}section{border-bottom:1px solid #ccc;padding:12px 0}</style><h1>Name-themed card samples</h1>")
        for fam, rows in files.items():
            for hd, body in rows[:: max(1, len(rows) // 3)][:3]:
                f.write(f"<section><p><b>{fam}</b> <code>{hd}</code></p>{body}</section>")
    print({k: len(v) for k, v in files.items()}, len(probs), "problems,", len(tag_ids), "need tag")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
