"""Decide Google Shopping age_group for every product (gender is always unisex).

Rules agreed with the owner:
- baby grows / baby clothing, kids' cards, kids' invites, school items, santa sacks & stockings -> kids
- adult / rude cards and mugs -> adult
- celebrity and fancy-dress face masks -> adult, unless the mask is a children's character
- everything else -> adult, unless the title clearly says it's for a child
"""
import re

KIDS_TYPES = re.compile(r"kids cards|kids invites|kids face masks|baby vest|baby grows|baby clothing|new baby|christening|"
                        r"school labels|school reward|school leavers|holiday stockings|christmas eve boxes|^lego$|party invites", re.I)
RUDE = re.compile(r"\b(rude|18\+|stag|hen do|hen party|swear|wank|sex|naughty|drunk|beer|gin|wine|vodka|prosecco|"
                  r"pint|booze|hangover|f\*+|c\*+)\b", re.I)
ADULT_WORD = re.compile(r"\badults?\b", re.I)
# "Kids Adult Personalised ..." in titles means "any age", so it isn't a signal either way.
ANY_AGE = re.compile(r"\b(kids?\s*(/|&|and|,)?\s*adults?|adults?\s*(/|&|and|,)?\s*kids?)\b", re.I)
KIDS_TITLE = re.compile(r"\b(kids?|child(ren)?|boys?|girls?|son|daughter|grandson|granddaughter|nephew|niece|baby|toddler|"
                        r"school|nursery|1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th|13th|age [1-9]|age 1[0-6]|"
                        r"(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve) today|years? old|is [1-9]\b)", re.I)
KIDS_CHARACTERS = re.compile(r"peppa|paw patrol|bluey|spongebob|mr tumble|frozen|elsa|olaf|minion|pokemon|pikachu|super mario|"
                             r"sonic the|teletubb|hey duggee|fireman sam|postman pat|thomas the tank|bob the builder|ben 10|"
                             r"power rangers?|ninja turtles|tmnt|in the night garden|iggle piggle|cocomelon|gruffalo|"
                             r"moana|encanto|toy story|paddington|peter rabbit|my little pony|hello kitty|barbie|"
                             r"roblox|minecraft|fortnite|among us|cbeebies|tweenies|noddy|scooby|dora the|unicorn|dinosaur", re.I)
MASK_CHARACTERS = re.compile(KIDS_CHARACTERS.pattern.replace("barbie|", "").replace("|unicorn|dinosaur", ""), re.I)
BABY_TYPES = re.compile(r"baby vest|baby grows|baby clothing", re.I)
# Drinkware, bar items and retro-gaming collectables are bought by and for adults.
ADULT_TYPES = re.compile(r"mug|coaster|bar mat|glass|flask|tumbler|poster|print|magnet|keyring|case|cover|signed|autograph|alcohol", re.I)
ADULT_TITLE = re.compile(r"replacement .*(case|cover)|game case|signed|autograph|\\bmug\\b|coaster", re.I)
MASK_TYPES = re.compile(r"mask|tv stars|celebrity facemask|footballer masks", re.I)


def age_group(product_type, title, tags):
    pt = product_type or ""
    ti = ANY_AGE.sub(" ", title or "")
    if BABY_TYPES.search(pt):
        return "kids"
    if RUDE.search(pt) or RUDE.search(ti) or re.search(r"adult|rude", pt, re.I):
        return "adult"
    if MASK_TYPES.search(pt) or "mask" in ti.lower():
        return "kids" if (MASK_CHARACTERS.search(ti) or re.search(r"kids face mask", pt, re.I)) else "adult"
    if ADULT_TYPES.search(pt) or ADULT_TITLE.search(ti):
        return "adult"
    if KIDS_TYPES.search(pt):
        return "kids"
    if ADULT_WORD.search(ti):
        return "adult"
    if KIDS_TITLE.search(ti) or KIDS_CHARACTERS.search(ti):
        return "kids"
    return "adult"
