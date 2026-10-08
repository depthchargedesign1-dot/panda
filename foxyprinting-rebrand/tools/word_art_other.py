"""Upgrade the rest of the Personalised Word Art Prints collection (8 Oct 2026).

Owner (8 Oct 2026): "yes do the same for the word art prints" -> give the 166 other
word art prints (pets, hobbies, numbers, "Pop Figures"...) the same treatment as the
53 "Personalised Name Word Art" letters (tools/word_art_sizes.py and
tools/word_art_descriptions.py). The 53 letter ids are excluded.

Facts come only from the owner's old copy (A4 350gsm card, A3 170gsm gloss, A2/A1
210gsm gloss, mm sizes, A3 frames clip to hang / A4 frames stand, next working day or
same day before 12pm by Royal Mail, first word shown once prominently, 20-30 words,
no phrases over 3 words) plus the Premium Display frames wording (owner, 6 Oct 2026).

Usage:
  python3 tools/word_art_other.py plan <before.json> <out_dir>
  python3 tools/word_art_other.py a <out_dir> <ids,>        # sizes, copy, tags, metafields
  python3 tools/word_art_other.py b <out_dir> <after_variants.json> <ids,>   # SKUs + images
"""
import json, os, re, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from age_group import age_group  # noqa: E402

LOC = "gid://shopify/Location/103075971453"
NEW = [  # (value, price, suffix, framed size) - same as tools/word_art_sizes.py
    ("A3 Print Only", "9.99", "-A3", None),
    ("A2 Print Only", "12.99", "-A2", None),
    ("A1 Print Only", "19.99", "-A1", None),
    ("A4 Print + Black Frame", "19.99", "-A4-BLK", "A4"),
    ("A4 Print + Silver Frame", "19.99", "-A4-SLV", "A4"),
    ("A3 Print + Black Frame", "29.99", "-A3-BLK", "A3"),
    ("A3 Print + Silver Frame", "29.99", "-A3-SLV", "A3"),
]
FRAMED_W = {"A4": 740, "A3": 1300}
MSG = "Your words message (20–30 words, separated by commas)"

# ---------------------------------------------------------------- profiles
# index in collection order (after removing the 53 letters):
# (title check, subject for copy, keyword subject, category, colour/design note, SEO subject, google colour)
D, C, PET, AN, KID, HOB, LOVE, FAM, STY, TRV, NUM, POP = ("dog", "cat", "pet", "animal", "kids", "hobby", "love",
                                                          "family", "style", "travel", "number", "pop")
PROFILES = [
    ("Dachshund", "dachshund", "dachshund", D, "a sausage dog portrait in soft greys", "Dachshund", "Grey"),
    ("Unicorn 1 B", "unicorn", "unicorn", KID, "a pastel rainbow unicorn head with leaves and flowers", "Pastel Unicorn Head", "Multicolor"),
    ("Saxophone", "saxophone", "saxophone", HOB, "a tall saxophone in mint green", "Saxophone", "Green"),
    ("Cricket", "cricketer", "cricket", HOB, "a batsman mid-shot in black and grey", "Cricket Batsman", "Black"),
    ("Cockapoo", "cockapoo", "cockapoo", D, "a curly cockapoo face in warm peach and cream", "Cockapoo Dog", "Multicolor"),
    ("Voldermort", "Lord Voldemort", "dark wizard", POP, "a dark wizard pop figure in stone greys", "Dark Wizard Pop", "Grey"),
    ("Snow White", "Snow White", "fairytale princess", POP, "a princess pop figure in yellow, blue and red", "Apple Princess Pop", "Multicolor"),
    ("Snape", "Severus Snape", "potions master", POP, "a potions master pop figure in black and grey", "Potions Master Pop", "Black"),
    ("Sirius", "Sirius Black", "wizard", POP, "a long-haired wizard pop figure in brown and grey", "Long-Haired Wizard", "Brown"),
    ("Ross", "Ross Geller", "sitcom", POP, "a sitcom pop figure in warm browns and blue", "Sitcom Dino Fan Pop", "Multicolor"),
    ("Ron Weasley", "Ron Weasley", "wizard", POP, "a red-haired wizard pop figure in soft browns", "Red-Haired Wizard", "Brown"),
    ("Copy of Copy of Personalised Rachel", "Rachel Green", "sitcom", POP, "a sitcom pop figure in brown and denim blue", "Sitcom Waitress Pop", "Multicolor"),
    ("Rapunzel", "Rapunzel", "princess", POP, "a long-haired princess pop figure in golden yellow and lilac", "Long-Haired Princess", "Yellow"),
    ("Personalised Rachel Word", "Rachel Green", "sitcom", POP, "a sitcom pop figure in brown and denim blue", "Sitcom Waitress Pop", "Multicolor"),
    ("Rachel (1)", "Rachel Green", "sitcom", POP, "a sitcom pop figure with golden hair and denim tones", "Sitcom Style Icon Pop", "Multicolor"),
    ("Pheobe", "Phoebe Buffay", "sitcom", POP, "a sitcom pop figure with blonde bunches in red and blue", "Sitcom Singer Pop", "Multicolor"),
    ("Copy of Personalised Mulan", "Mulan", "warrior princess", POP, "a warrior princess pop figure in deep red and cream", "Warrior Princess Pop", "Red"),
    ("Personalised Mulan", "Mulan", "warrior princess", POP, "a warrior princess pop figure in deep red and cream", "Warrior Princess Pop", "Red"),
    ("Monica", "Monica Geller", "sitcom", POP, "a sitcom pop figure in warm browns and cream", "Sitcom Chef Pop", "Brown"),
    ("Moaning Martel", "Moaning Myrtle", "ghost girl", POP, "a ghostly pop figure in bright blue", "Ghost Girl Pop", "Blue"),
    ("Merida", "Merida", "archer princess", POP, "an archer princess pop figure with fiery red curls and teal", "Archer Princess Pop", "Red"),
    ("Mcgonagol", "Professor McGonagall", "witch professor", POP, "a witch professor pop figure in greys", "Witch Professor Pop", "Grey"),
    ("Luna", "Luna Lovegood", "witch", POP, "a dreamy witch pop figure in pale blonde and grey", "Dreamy Witch Pop", "Grey"),
    ("Joey", "Joey Tribbiani", "sitcom", POP, "a sitcom pop figure in dark brown and grey", "Sitcom Actor Pop", "Brown"),
    ("Jasmine", "Princess Jasmine", "desert princess", POP, "a desert princess pop figure in turquoise and brown", "Desert Princess Pop", "Blue"),
    ("Harry Potter", "Harry Potter", "boy wizard", POP, "a boy wizard pop figure in grey and tan", "Boy Wizard Pop", "Grey"),
    ("Hagrid", "Rubeus Hagrid", "gamekeeper", POP, "a bearded gamekeeper pop figure in dark brown and grey", "Gamekeeper Pop", "Brown"),
    ("Ginny Weasley", "Ginny Weasley", "witch", POP, "a red-haired witch pop figure in copper and grey", "Red-Haired Witch Pop", "Multicolor"),
    ("Dumbledor", "Albus Dumbledore", "wizard headmaster", POP, "a wizard headmaster pop figure in silver-grey and lilac", "Headmaster Wizard Pop", "Grey"),
    ("Draco", "Draco Malfoy", "wizard", POP, "a blond wizard pop figure in black and pale gold", "Blond Wizard Pop", "Black"),
    ("Dobby", "Dobby the house-elf", "house-elf", POP, "a house-elf pop figure in soft pink and brown", "House-Elf Pop", "Multicolor"),
    ("Cinderella", "Cinderella", "glass slipper princess", POP, "a ballgown princess pop figure in pale blue and gold", "Ballgown Princess Pop", "Blue"),
    ("Chandler", "Chandler Bing", "sitcom", POP, "a sitcom pop figure in brown and black", "Sitcom Joker Pop", "Brown"),
    ("Belle", "Belle", "bookworm princess", POP, "a bookworm princess pop figure in golden yellow", "Bookworm Princess Pop", "Yellow"),
    ("Aurora", "Aurora", "sleeping princess", POP, "a sleeping princess pop figure in pink and golden blonde", "Sleeping Princess Pop", "Pink"),
    ("Wine Glass 1 Word", "wine glass", "wine glass", STY, "a big wine glass in black, with the name in bold across the bowl", "Wine Glass", "Black"),
    ("Wine Glass 1 B", "wine glass", "wine glass", STY, "a black wine glass with the name picked out in red", "Wine Glass Red Name", "Black"),
    ("Wine Glass 1 (3)", "wine glass", "wine glass", STY, "a black wine glass with the name in red script at the base", "Wine Glass Script", "Black"),
    ("Unicorn 3", "unicorn", "unicorn", KID, "a sleepy unicorn lying down in soft pink", "Sleepy Pink Unicorn", "Pink"),
    ("Unicorn 2 B", "unicorn", "unicorn", KID, "a leaping unicorn in purple and pink", "Leaping Unicorn", "Purple"),
    ("Unicorn 1 Word", "unicorn", "unicorn", KID, "a pastel rainbow unicorn head with the name underneath", "Rainbow Unicorn", "Multicolor"),
    ("Train", "train", "train", KID, "a steam train pulling carriages in bright colours", "Steam Train", "Multicolor"),
    ("Teddy Bear", "teddy bear", "teddy bear", KID, "a cuddly teddy bear in warm browns", "Teddy Bear", "Brown"),
    ("Superhero 3", "superhero", "superhero", KID, "a crouching superhero in black with orange highlights", "Crouching Superhero", "Multicolor"),
    ("Superhero 2", "superhero", "superhero", KID, "a flying superhero in black and sky blue", "Flying Superhero", "Blue"),
    ("Superhero 1", "superhero", "superhero", KID, "a standing superhero with a bright red cape", "Caped Superhero", "Red"),
    ("Street Dancer", "street dancer", "street dancer", HOB, "a street dancer mid-move in black and grey", "Street Dancer", "Black"),
    ("Personalised Staue of Liberty", "Statue of Liberty", "Statue of Liberty", TRV, "the Statue of Liberty in coral red", "Statue of Liberty", "Red"),
    ("Staue of Liberty 1 Personalised Shiatsu", "Statue of Liberty", "New York", TRV, "the Statue of Liberty in coral red, with the name on the plinth", "New York Statue", "Red"),
    ("Shiatsu", "Shih Tzu", "Shih Tzu", D, "a fluffy Shih Tzu face in soft greys", "Shih Tzu", "Grey"),
    ("Seahorse", "seahorse", "seahorse", AN, "a curling seahorse in soft blue and pink", "Seahorse", "Blue"),
    ("Runner", "runner", "runner", HOB, "a runner in full stride, in rainbow colours with confetti triangles", "Runner", "Multicolor"),
    ("Rainbow Heart Word", "rainbow heart", "rainbow heart", LOVE, "a rainbow-striped heart", "Rainbow Heart", "Multicolor"),
    ("Rainbow Heart 2", "rainbow heart", "rainbow heart", LOVE, "a rainbow-striped heart with the name in bold black", "Bold Rainbow Heart", "Multicolor"),
    ("Rainbow 1 Word", "rainbow", "rainbow", STY, "a rainbow arch with the name in purple underneath", "Rainbow Arch", "Multicolor"),
    ("Rainbow 1 B", "rainbow", "rainbow", STY, "a rainbow arch with the name woven through the colours", "Rainbow", "Multicolor"),
    ("Racoon", "raccoon", "raccoon", AN, "a raccoon in shades of grey", "Raccoon", "Grey"),
    ("Pug 4", "pug", "pug", D, "a pug face in fawn and black", "Pug Face", "Brown"),
    ("Pug 3", "pug", "pug", D, "a pug in a Viking helmet, in peach and cream", "Viking Pug", "Multicolor"),
    ("Pug 3", "pug", "pug", D, "a pug in a Viking helmet, in peach and cream", "Viking Pug", "Multicolor"),
    ("Pug 2", "pug", "pug", D, "a dapper pug in a top hat and bow tie", "Top Hat Pug", "Grey"),
    ("Pug 1", "pug", "pug", D, "a pug face in soft fawn and beige", "Fawn Pug", "Brown"),
    ("Princess 1", "princess", "princess", KID, "a little princess in a pink dress and gold crown", "Little Princess", "Pink"),
    ("Pink Flower Word", "pink flower", "pink flower", STY, "a pink flower with the name woven into the petals", "Pink Flower", "Pink"),
    ("Pink Flower 2", "pink flower", "pink flower", STY, "a pink flower with the name written underneath", "Pink Flower Name", "Pink"),
    ("Penguin", "penguin", "penguin", AN, "a round penguin in black and grey with an orange beak", "Penguin", "Black"),
    ("Paw Prints 2", "paw prints", "paw print", PET, "two grey paw prints", "Two Paw Prints", "Grey"),
    ("Paw Prints 1", "paw prints", "paw print", PET, "two outlined paw prints", "Outline Paw Prints", "Grey"),
    ("Paw Print 2", "paw print heart", "paw print heart", PET, "a heart with a paw print in the middle, in browns", "Paw Print Heart", "Brown"),
    ("Paw Print 1", "paw print", "paw print", PET, "one big paw print in browns and greys", "Big Paw Print", "Brown"),
    ("Owl 1 Word", "owl", "owl", AN, "a wide-eyed owl in bright orange", "Orange Owl", "Orange"),
    ("Owl 1 B", "owl", "owl", AN, "a wide-eyed owl in peach, with the name across its tummy", "Peach Owl", "Orange"),
    ("Mini Schnauzer", "miniature schnauzer", "mini schnauzer", D, "a schnauzer face in greys", "Mini Schnauzer", "Grey"),
    ("Lips 1 Word", "lips", "lips", LOVE, "a pair of red lips", "Red Lips", "Red"),
    ("Lips 1 (3)", "lips", "lips", LOVE, "a pair of lips in pink and lilac", "Pink Lips", "Pink"),
    ("Lips 1 (2)", "lips", "lips", LOVE, "a pair of red lips with the name in large letters", "Lips Big Name", "Red"),
    ("Labrador", "Labrador", "Labrador", D, "a smiling Labrador in golden tones", "Labrador", "Yellow"),
    ("Jack Russell Word", "Jack Russell", "Jack Russell", D, "a Jack Russell face framed by sunny yellow word panels", "Jack Russell", "Yellow"),
    ("Jack Russell 2", "Jack Russell", "Jack Russell", D, "a Jack Russell in a graduation cap, framed by blue word panels", "Jack Russell Blue", "Blue"),
    ("Ihasa Apso", "Lhasa Apso", "Lhasa Apso", D, "a long-haired Lhasa Apso in soft greys", "Lhasa Apso", "Grey"),
    ("Husky", "husky", "husky", D, "a husky face in grey and black", "Husky", "Grey"),
    ("House", "house", "new home", FAM, "a little house with a red roof in bright colours", "New Home House", "Multicolor"),
    ("Horse Racer", "racehorse and jockey", "horse racing", HOB, "a racehorse and jockey at full gallop in black and grey", "Horse Racing", "Black"),
    ("Heart 2 (2)", "heart", "heart", LOVE, "a ring of little pink hearts with the name in the middle", "Ring of Hearts", "Pink"),
    ("Heart 1 Word", "heart", "heart", LOVE, "a bold red heart", "Red Heart", "Red"),
    ("Heart 1 Family B", "family heart", "family heart", FAM, "a pink and purple heart with the word Family in large letters", "Family Heart", "Pink"),
    ("Heart 1 B", "heart", "heart", LOVE, "a pink and purple heart with the name in large letters", "Pink Heart", "Pink"),
    ("Guitar", "guitar", "guitar", HOB, "an acoustic guitar in pastel shades", "Acoustic Guitar", "Multicolor"),
    ("Golfer Girl Word", "lady golfer", "golf", HOB, "a lady golfer mid-swing in black and grey, with the name in pink", "Lady Golfer", "Black"),
    ("Golfer Girl 2", "lady golfer", "golf", HOB, "a lady golfer mid-swing in bright pink", "Pink Lady Golfer", "Pink"),
    ("Golf 1", "golfer", "golf", HOB, "a golfer lining up a putt, in navy blue", "Golfer", "Blue"),
    ("Personalised German Shepard", "German Shepherd", "German Shepherd", D, "a German Shepherd in tan and grey", "German Shepherd", "Brown"),
    ("FGerman Shepard", "German Shepherd", "German Shepherd", D, "an alert German Shepherd in tan and grey", "German Shepherd Dog", "Brown"),
    ("French Bulldog", "French Bulldog", "French Bulldog", D, "a French Bulldog with big ears in grey and black", "French Bulldog", "Grey"),
    ("Footballer", "footballer", "football", HOB, "a footballer doing an overhead kick, in black", "Overhead Kick", "Black"),
    ("Fox", "fox", "fox", AN, "a sitting fox in bright orange", "Fox", "Orange"),
    ("Family 1 Word", "family", "family", FAM, "a family of four holding hands, in greys", "Family of Four", "Grey"),
    ("Family 1 B", "family", "family", FAM, "a family of four holding hands, with the name in bold underneath", "Family Name", "Black"),
    ("Fairy 1 B", "fairy", "fairy", KID, "a smiling fairy in a pink dress, with the name below", "Pink Fairy", "Pink"),
    ("Fairy 1 Word", "fairy", "fairy", KID, "a smiling fairy in a pink dress with a wand", "Fairy", "Pink"),
    ("Elephant", "elephant", "elephant", AN, "a baby elephant in soft blue holding a red heart", "Baby Elephant", "Blue"),
    ("Eiffel Tower", "Eiffel Tower", "Eiffel Tower", TRV, "the Eiffel Tower in pale blue", "Eiffel Tower Paris", "Blue"),
    ("Dress 1 B", "dress", "dress", STY, "a party dress in coral red", "Party Dress", "Red"),
    ("Dress 1 B", "dress", "dress", STY, "a party dress in coral red, with the name across the skirt", "Coral Party Dress", "Red"),
    ("Donut", "doughnut", "doughnut", STY, "a pink iced doughnut", "Doughnut", "Pink"),
    ("Dolphin 1 Word", "dolphin", "dolphin", AN, "a leaping dolphin in ocean blue", "Dolphin", "Blue"),
    ("Dolphin 1 B", "dolphin", "dolphin", AN, "a leaping dolphin in blue, with the name in big letters below", "Blue Dolphin", "Blue"),
    ("Dog Bone", "dog bone", "dog bone", PET, "a dog bone in warm browns", "Dog Bone", "Brown"),
    ("Dog 2", "dog", "dog", PET, "a playful puppy stretching, in peach and orange", "Playful Puppy", "Orange"),
    ("Dog 1", "dog", "dog", PET, "a cartoon puppy face in cream and brown", "Puppy Face", "Brown"),
    ("Dinosaur 2", "dinosaur", "dinosaur", KID, "a baby dinosaur hatching from its egg, in yellow and teal", "Baby Dinosaur Egg", "Multicolor"),
    ("Dino 1", "dinosaur", "dinosaur", KID, "a stegosaurus in bright red", "Red Stegosaurus", "Red"),
    ("Dalmatian", "Dalmatian", "Dalmatian", D, "a spotty Dalmatian in black and grey", "Dalmatian", "Black"),
    ("Crown 3", "crown", "crown", STY, "a five-point crown in gold", "Gold Crown", "Gold"),
    ("Crown 2", "crown", "crown", STY, "a royal crown topped with a cross, in gold", "Royal Crown", "Gold"),
    ("Crown 1", "crown", "crown", STY, "a fleur-de-lis crown in gold", "Fleur-de-Lis Crown", "Gold"),
    ("Couple 2", "couple", "wedding couple", LOVE, "a bride and groom sharing a kiss, in black", "Wedding Couple", "Black"),
    ("Couple 1", "couple", "proposal", LOVE, "a proposal on one knee, in black", "Proposal Couple", "Black"),
    ("Corgi", "corgi", "corgi", D, "a smiling corgi in tan and cream", "Corgi Dog", "Brown"),
    ("Chihuahua", "Chihuahua", "Chihuahua", D, "a big-eared Chihuahua in tan", "Chihuahua Dog", "Brown"),
    ("Cavalier Spaniel", "Cavalier spaniel", "Cavalier spaniel", D, "a Cavalier spaniel in chestnut and cream", "Cavalier Spaniel Dog", "Brown"),
    ("Cat 9", "cat", "cat", C, "a fluffy cat in very pale greys", "Pale Fluffy Cat", "Grey"),
    ("Cat 8", "cat", "cat", C, "a tabby cat in soft browns", "Tabby Cat", "Brown"),
    ("Cat 7", "cat", "cat", C, "a fluffy tabby cat in browns", "Fluffy Tabby Cat", "Brown"),
    ("Cat 6", "cat", "cat", C, "a blue-eyed long-haired cat in greys", "Blue-Eyed Cat", "Grey"),
    ("Cat 5", "cat", "cat", C, "a grey cat with amber eyes", "Grey Cat", "Grey"),
    ("Cat 4", "cat", "cat", C, "a ginger and grey cat", "Ginger and Grey Cat", "Multicolor"),
    ("Cat 3", "cat", "cat", C, "a ginger cat", "Ginger Cat", "Orange"),
    ("Cat 2 ", "cat", "cat", C, "a grey tabby cat", "Grey Tabby Cat", "Grey"),
    ("Cat 2 B", "cat", "cat", C, "a cartoon cat curled up, in grey with a pink nose", "Cartoon Cat", "Grey"),
    ("Cat 1 Word", "cat", "cat", C, "a blue-eyed tabby cat", "Tabby Cat Blue Eyes", "Brown"),
    ("Cat 1 B", "cat", "cat", C, "a black cat silhouette with the name in big letters above", "Black Cat", "Black"),
    ("Car 5", "car", "car", HOB, "a hatchback car in red", "Red Car", "Red"),
    ("Car 4", "car", "car", HOB, "a convertible car in grey", "Convertible Car", "Grey"),
    ("Car 3", "car", "car", HOB, "a rounded classic car in pale blue", "Classic Car", "Blue"),
    ("Car 2", "car", "car", HOB, "a classic small car in green", "Green Classic Car", "Green"),
    ("Car 1", "car", "car", HOB, "a small car in sunny yellow", "Yellow Car", "Yellow"),
    ("Butterfly 2", "butterfly", "butterfly", AN, "a butterfly in black and grey", "Butterfly", "Black"),
    ("Butterfly 1 Word", "butterfly", "butterfly", AN, "a butterfly in blue and teal", "Blue Butterfly", "Blue"),
    ("Butterfly 1 B", "butterfly", "butterfly", AN, "a butterfly in pink", "Pink Butterfly", "Pink"),
    ("Bulldog Bruno", "bulldog", "bulldog", D, "a bulldog in black and grey", "Bulldog", "Black"),
    ("Border Collie", "Border Collie", "Border Collie", D, "a Border Collie in grey and black", "Border Collie", "Grey"),
    ("Blue Flower Word", "blue flower", "blue flower", STY, "a teal daisy with the name at its centre", "Blue Flower", "Blue"),
    ("Blue Flower B", "blue flower", "blue flower", STY, "a teal daisy with the name in big letters below", "Blue Daisy", "Blue"),
    ("Beagle Dog", "beagle", "beagle", D, "a beagle face in brown and black", "Beagle Dog", "Brown"),
    ("Beagle 1", "beagle", "beagle", D, "a beagle in tan and cream", "Beagle", "Brown"),
    ("Ariel", "Ariel", "mermaid princess", POP, "a mermaid princess pop figure in red and pink", "Mermaid Princess Pop", "Red"),
    ("Ballet Dancer", "ballet dancer", "ballet", HOB, "a ballerina on pointe in grey, with the name in pink", "Ballet Dancer", "Grey"),
    ("Ballet 4", "ballerina", "ballet", HOB, "a ballerina in pastel blue and peach", "Pastel Ballerina", "Blue"),
    ("Ballet 2", "ballerina", "ballet", HOB, "a ballerina in an arabesque, in pink", "Arabesque Ballerina", "Pink"),
    ("Ballet 1 Word", "ballerina", "ballet", HOB, "a ballerina in pink, with the name underneath", "Pink Ballerina", "Pink"),
    ("Ballet 1 B", "ballerina", "ballet", HOB, "a ballerina in pink with arms outstretched", "Ballerina", "Pink"),
]
for n, col in ((50, "Black"), (50, "Pink"), (30, "Black"), (30, "Pink"), (30, "Blue"), (21, "Black"), (21, "Pink"),
               (21, "Blue"), (18, "Black"), (18, "Pink"), (18, "Blue"), (16, "Black"), (16, "Pink"), (16, "Blue")):
    PROFILES.append((f"Number {n}", str(n), str(n), NUM, col.lower(), f"{col} {n}th Birthday".replace("21th", "21st"), col))

POP_SETS = {  # character -> (where from, rights holders)
    "hp": ("Harry Potter", "the Harry Potter books and films", "J.K. Rowling, Warner Bros. Entertainment"),
    "friends": ("Friends", "the TV series Friends", "Warner Bros. Television"),
    "disney": ("Disney", "Disney", "The Walt Disney Company"),
}
HP = {"Lord Voldemort", "Severus Snape", "Sirius Black", "Ron Weasley", "Moaning Myrtle", "Professor McGonagall",
      "Luna Lovegood", "Harry Potter", "Rubeus Hagrid", "Ginny Weasley", "Albus Dumbledore", "Draco Malfoy",
      "Dobby the house-elf"}
FRIENDS = {"Ross Geller", "Rachel Green", "Phoebe Buffay", "Monica Geller", "Joey Tribbiani", "Chandler Bing"}


def pop_set(subject):
    return "hp" if subject in HP else "friends" if subject in FRIENDS else "disney"


def ordinal(n):
    n = int(n)
    return f"{n}{'st' if n % 10 == 1 and n != 11 else 'nd' if n % 10 == 2 and n != 12 else 'rd' if n % 10 == 3 and n != 13 else 'th'}"


def keyword(p):
    subj, kw, cat = p[1], p[2], p[3]
    if cat == NUM:
        return f"personalised {ordinal(kw)} birthday word art print"
    if cat == POP:
        return "personalised pop figure word art print"
    return f"personalised {kw} word art print"


def name_label(cat):
    return {D: "Dog’s name (shown largest)", C: "Cat’s name (shown largest)", PET: "Pet’s name (shown largest)",
            FAM: "Family name (shown largest)"}.get(cat, "Name (shown largest)")


# ---------------------------------------------------------------- copy pools
OPEN = {
    D: ["If they talk about their {s} more than anything else, this {kw} is the gift for them: {d}, filled with the words that sum their dog up.",
        "Our {kw} turns {d} into a keepsake made entirely from words about one very good dog.",
        "Every dog has a story, and this {kw} tells it: {d}, made from your dog's name and the things that make them who they are.",
        "Give a {s} lover something they'll smile at every day with this {kw}, {d} built from their dog's name and favourite things."],
    C: ["Cat people will love this {kw}: {d}, filled with the name and quirks of their favourite feline.",
        "This {kw} shows {d}, made from the words that describe one very special cat.",
        "A {kw} is a lovely way to celebrate a much-loved cat. This design is {d}, built from their name and your words.",
        "Our {kw} captures {d} in a cloud of words: their name, their naughty habits and all the things you love about them."],
    PET: ["This {kw} is made for pet lovers: {d}, filled with your pet's name and the words that describe them.",
          "Celebrate a four-legged member of the family with this {kw}, featuring {d} made from words you choose.",
          "A {kw} makes a thoughtful gift for any dog or cat owner. This one is {d}, built from their pet's name and favourite things."],
    AN: ["This {kw} shows {d}, filled with a name and the words that mean most to them.",
         "Animal lovers of all ages will enjoy this {kw}: {d}, made from their name and a list of words you choose.",
         "Our {kw} turns {d} into a one-off picture made entirely from words."],
    KID: ["This {kw} is a lovely way to brighten a bedroom or nursery: {d}, made from a child's name and their favourite things.",
          "Little ones love seeing their name on the wall, and this {kw} puts it in pride of place: {d}, built from your words.",
          "Our {kw} shows {d}, filled with a name and all the words that make them smile."],
    HOB: ["Got someone who lives for their hobby? This {kw} shows {d}, made from their name and the words that describe them.",
          "This {kw} is a gift for the {s} in your life: {d}, built from words about them and what they love.",
          "Our {kw} celebrates a passion in style: {d}, filled with a name and a list of words you choose."],
    LOVE: ["This {kw} lets you say it with words, lots of them: {d}, made from names and the words that sum up your love.",
           "A {kw} is a romantic gift that's genuinely personal: {d}, filled with your names, memories and in-jokes.",
           "This {kw} features {d}, built from the words that tell your story together."],
    FAM: ["This {kw} brings the whole family together in one picture: {d}, made from names and the words that describe your family.",
          "Our {kw} is a warm, personal gift for the home: {d}, filled with family names and favourite things.",
          "A {kw} makes a thoughtful gift for a new home or a family celebration. This one is {d}, built from your words."],
    STY: ["This {kw} shows {d}, filled with a name and the words that describe them best.",
          "Our {kw} is a fun, personal gift: {d}, made from their name and a list of words you choose.",
          "Looking for something different? This {kw} features {d}, built entirely from words."],
    TRV: ["For anyone who loves to travel, this {kw} shows {d}, made from a name and the memories that go with it.",
          "Our {kw} features {d}, filled with a name, favourite places and the words that sum up a trip of a lifetime."],
    NUM: ["Mark a big birthday with this {kw}: a large {d} number {s}, filled with their name and the words that sum them up.",
          "This {kw} turns a {d} number {s} into a keepsake made from the words that describe the birthday star.",
          "Our {kw} is a {d} number {s}, built from a name and 20 to 30 words about the person turning {s}."],
    POP: ["This {kw} is inspired by {s} from {src}: {d}, filled with a name and your own words.",
          "Fans of {src} will love this {kw}. It shows {d}, inspired by {s} and made from the words you choose.",
          "Our {kw} is a fun gift for fans of {src}: {d} inspired by {s}, built from a name and your words."],
}
OPEN2 = {
    D: ["It's a lovely gift for a new puppy, a dog's birthday or a dog-mad friend.", "It also makes a thoughtful keepsake of a much-loved dog.",
        "Perfect for the hallway, the kitchen or wherever the dog bed lives."],
    C: ["It's a lovely gift for a new kitten, a cat's birthday or a cat-mad friend.", "It also makes a thoughtful keepsake of a much-loved cat."],
    PET: ["It works for dogs, cats and any other pet with a big personality.", "It also makes a thoughtful keepsake of a much-loved pet."],
    AN: ["It looks lovely in a bedroom, nursery or living room.", "A gift that suits children and grown-ups alike."],
    KID: ["It makes a cheerful nursery print or a birthday gift they'll keep.", "Grandparents, godparents and parents love them."],
    HOB: ["It's a great birthday, Christmas or team gift.", "A thoughtful present for a club mate, coach or proud parent."],
    LOVE: ["It's a lovely anniversary, Valentine's or wedding gift.", "Perfect for an anniversary, an engagement or just because."],
    FAM: ["It's a lovely housewarming or Mother's Day gift.", "Perfect for the family living room or hallway."],
    STY: ["It's a fun birthday or Christmas gift for a friend.", "Perfect for a bedroom wall or a best friend's birthday."],
    TRV: ["It's a lovely gift for a honeymoon, a big trip or a travel fan.", "Perfect for remembering a holiday you'll never forget."],
    NUM: ["It's a gift they'll keep long after the party.", "Hang it at the party, then on the wall at home."],
    POP: ["It's a fun birthday or Christmas gift for a fan.", "A great one for a bedroom, a games room or a fan's first flat."],
}
H2 = ["Your {kw}, made with your words", "How your {kw} comes together", "Create a {kw} in two boxes",
      "Make your own {kw}"]
HOW = [
    "Type the {who} in the first box; it appears once, in pride of place. In the second box, type 20 to 30 words separated by commas: {ideas}. We repeat them in different sizes, fonts and shades to fill the {shape}. The preview shows your details before you add it to your basket.",
    "The name box comes first, and whatever you type there is shown once, nice and big. Then add 20 to 30 words, with a comma between each: {ideas}. We repeat your words in different sizes, fonts and shades until the {shape} is full. Check the preview before you order.",
    "Fill in two boxes: the {who}, which sits once prominently in the design, and your word list of 20 to 30 words separated by commas, such as {ideas}. We repeat the words randomly in different sizes, fonts and shades across the {shape}, and the preview shows what you've typed next to the print photo.",
]
IDEAS = {
    D: ["nicknames, favourite walks, toys, treats and the people they love", "walkies spots, silly habits, nicknames and best friends"],
    C: ["nicknames, favourite sleeping spots, treats and naughty habits", "purrs, toys, nicknames and the people they love"],
    PET: ["nicknames, favourite toys, treats and habits", "walks, naps, nicknames and the people they love"],
    AN: ["hobbies, nicknames, family names and favourite places", "the people they love, favourite things and in-jokes"],
    KID: ["family names, favourite toys, pets and hobbies", "brothers and sisters, best friends, favourite foods and games"],
    HOB: ["teams, clubs, nicknames, achievements and favourite moments", "club names, places, friends and the words their mates use about them"],
    LOVE: ["pet names, places you've been, songs and special dates", "memories, in-jokes, places and the things you love about each other"],
    FAM: ["family names, pets, places and favourite sayings", "everyone's names, pets, holidays and family jokes"],
    STY: ["hobbies, nicknames, friends and favourite things", "the people they love, favourite places and in-jokes"],
    TRV: ["places, cities, landmarks and travel buddies", "trips, memories, people and favourite foods"],
    NUM: ["nicknames, friends, hobbies, places and memories", "family names, achievements, in-jokes and favourite things"],
    POP: ["nicknames, hobbies, friends and favourite things", "family names, favourite moments and in-jokes"],
}
WHO = {D: "dog's name", C: "cat's name", PET: "pet's name", FAM: "family name"}
TIPS = [
    "Tips: use single words or phrases of no more than three words, put commas between them and check your spelling. No icons, emoji or accented letters, please. We print exactly what you type.",
    "Single words work best, and no phrase should be longer than three words. Check the spelling carefully, as we print exactly what you enter. Icons, emoji and accents can't be included.",
    "Keep to single words or short phrases (three words at most), separated by commas, and leave out emoji, icons and accented letters. We print exactly what you type, so read it through once more.",
]
BULLETS = [
    "One of a kind: every word comes from you, so no two prints are the same",
    "The name stands out once, and your other words repeat in different sizes, fonts and shades",
    "High-quality full-colour print, made to order",
    "Four print-only sizes, from a shelf-sized A4 to a statement A1",
    "Premium Display frames in black or silver: thick, chunky and very professional, not cheap thin frames",
    "Ready to display: A3 frames have a clip on the back for hanging, and A4 frames have a stand",
]
CLOSE = {
    D: ["Pair it with a matching dog mug for the ultimate dog lover's gift.", "A brilliant personalised dog gift for birthdays, Christmas or a new puppy.",
        "Order one for every dog in the family and hang them side by side."],
    C: ["A brilliant personalised cat gift for birthdays, Christmas or a new kitten.", "Pair it with a cat mug for the crazy cat lady or gent in your life."],
    PET: ["A thoughtful personalised pet gift for birthdays, Christmas or a new arrival.", "Pair it with a pet mug for a gift any animal lover will adore."],
    AN: ["A thoughtful personalised gift for animal lovers, young or old.", "Lovely as new baby wall art or a birthday gift for a nature lover."],
    KID: ["A lovely personalised children's gift for birthdays, christenings or Christmas.", "Order one for each child and hang them side by side in a shared bedroom."],
    HOB: ["A personalised hobby gift they'll be proud to hang up.", "Great for a birthday, a club presentation or an end-of-season thank you."],
    LOVE: ["A romantic personalised anniversary gift that says more than a bunch of flowers.", "Lovely for Valentine's Day, an engagement or a wedding anniversary."],
    FAM: ["A heart-warming personalised family gift for a new home or Mother's Day.", "Perfect as new home wall art or a Christmas present for the whole family."],
    STY: ["A fun personalised birthday gift for a friend, sister or Mum.", "Pick their favourite words and we'll do the rest."],
    TRV: ["A lovely personalised travel gift for honeymooners and globetrotters.", "Perfect for remembering a special trip, or dreaming about the next one."],
    NUM: ["A brilliant personalised {o} birthday gift they'll keep for years.", "Pair it with a birthday mug for a {o} gift they'll love."],
    POP: ["A fun personalised gift for a fan's birthday or Christmas.", "Collect the set and hang them side by side."],
}


def disclaimer(p):
    s = p[1]
    k = pop_set(s)
    name, src, owners = POP_SETS[k]
    who = {"hp": f"{s} from {src}", "friends": f"{s} from {src}", "disney": f"Disney's {s}"}[k]
    brand = {"hp": "Harry Potter", "friends": "Friends", "disney": "Disney"}[k]
    return ("<h3>Please note</h3>\n<p class=\"disclaimer\">This is an unofficial design inspired by "
            f"{who}, drawn in the style of collectable pop vinyl figures. It is not official merchandise and is not "
            f"endorsed by, sponsored by, or connected with {brand}, {owners} or Funko, or any of their licensees. "
            "All names, characters and trademarks belong to their respective owners.</p>")


def describe(i, p):
    title_chk, s, kw_s, cat, d, seo_s, gcol = p
    kw = keyword(p)
    o = ordinal(kw_s) if cat == NUM else ""
    src = POP_SETS[pop_set(s)][1] if cat == POP else ""
    f = lambda t: t.format(s=s, kw=kw, d=d, src=src, o=o)
    shape = {NUM: f"number {kw_s}", POP: "figure", TRV: "design", FAM: "design", LOVE: "shape", STY: "shape"}.get(cat, kw_s if cat not in (D, C) else ("dog" if cat == D else "cat"))
    if cat in (HOB, KID, AN, PET):
        shape = "design"
    who = WHO.get(cat, "name")
    rest = [x for x in BULLETS if "Premium Display" not in x]
    b = (rest[i % 5:] + rest[:i % 5])[:3]
    b.insert(i % 4, BULLETS[4])
    op = OPEN[cat]
    parts = [
        f"<p>{f(op[i % len(op)])} {OPEN2[cat][(i // len(op)) % len(OPEN2[cat])]}</p>",
        f"<h2>{H2[i % 4].format(kw=kw)}</h2>",
        f"<p>{HOW[i % 3].format(who=who, ideas=IDEAS[cat][i % 2], shape=shape)}</p>",
        f"<p>{TIPS[(i // 3) % 3]}</p>",
        "<h3>Why you'll love it</h3>",
        "<ul>" + "".join(f"<li>{x}</li>" for x in b) + "</ul>",
        "<h3>Size &amp; details</h3>",
        "<ul>"
        f"<li>Design: {d}, filled with your name and 20–30 words</li>"
        "<li>Print only: A4 (210 x 297 mm), A3 (297 x 420 mm), A2 (420 x 594 mm) or A1 (594 x 841 mm)</li>"
        "<li>Paper: A4 on 350gsm card, A3 on 170gsm gloss, A2 and A1 on 210gsm gloss</li>"
        "<li>Framed: A4 (with a stand) or A3 (with a hanging clip) in a black or silver Premium Display frame</li>"
        "</ul>",
        "<h3>Delivery</h3>",
        f"<p>Your {kw} is posted the next working day, or the same day if you order before 12pm, by Royal Mail.</p>",
        f"<p>{f(CLOSE[cat][i % len(CLOSE[cat])])}</p>",
    ]
    if cat == NUM:
        parts[0] = parts[0].replace(f"{d} number", f"{d} number")
    if cat == POP:  # keep within 350 words once the disclaimer is added
        parts[0] = f"<p>{f(op[i % len(op)])}</p>"
        parts[3] = "<p>Short words work best. We print exactly what you type, so check the spelling.</p>"
        parts[-1] = "<p>Posted the next working day (same day if you order before 12pm) by Royal Mail. " + parts[-1][3:]
        parts.pop(-2)
        parts[5] = "<ul>" + "".join(f"<li>{x}</li>" for x in b[:3]) + "</ul>"
        if BULLETS[4] not in parts[5]:
            parts[5] = "<ul>" + "".join(f"<li>{x}</li>" for x in [BULLETS[4]] + b[:2]) + "</ul>"
        parts.append(disclaimer(p))
    h = "\n".join(parts)
    # the H2 must start with a capital letter
    h = re.sub(r"<h2>(\w)", lambda m: "<h2>" + m.group(1).upper(), h)
    return h


def words(h):
    return len(re.sub(r"<[^>]+>", " ", html.unescape(h)).split())


def check(h, kw):
    probs = []
    if h.count("<h2") != 1: probs.append("h2")
    low = h.replace("350gsm card", "").replace("Snow White", "").lower()
    for bad in ("style=", "<h4", "#", "<span", "<div", "card", "greeting", "white", "official merch", "licensed", "gold frame"):
        if bad in low.replace("not official merchandise", "").replace("unofficial", ""):
            probs.append(bad)
    if re.search(r"<(\w+)[^>]*>\s*</\1>", h): probs.append("empty tag")
    n = words(h)
    if not 180 <= n <= 350: probs.append(f"words={n}")
    first = re.search(r"<p>(.*?)</p>", h).group(1).split(". ")[0].lower()
    kw = kw.lower()
    if kw not in first: probs.append("kw not in first sentence")
    if kw not in h.split("<h2>")[1].split("</h2>")[0].lower(): probs.append("kw not in h2")
    return probs


def seo(p, i):
    title = f"Personalised {p[5]} Word Art Print | Foxy Printing"
    if len(title) > 60:
        title = f"Personalised {p[5]} Word Art | Foxy Printing"
    assert len(title) <= 60, title
    cat = p[3]
    if cat == POP:
        subj = p[5].replace(" Pop", "").lower() + " pop figure"
    elif cat == NUM:
        subj = f"{ordinal(p[2])} birthday"
    else:
        subj = p[5].lower()
    who = {D: "their dog's name", C: "their cat's name", PET: "your pet's name", FAM: "your family name"}.get(cat, "a name")
    opts = [
        f"A personalised {subj} word art print made from {who} and 20–30 words you choose. A4 to A1, or framed in black or silver. Posted next working day.",
        f"Make a {subj} word art print with {who} and your own words. Print only A4 to A1, or in a chunky black or silver frame. Posted next working day.",
        f"Fill this {subj} word art print with {who} and 20–30 words. Choose A4 to A1 print only or a black or silver frame. Order by 12pm for same-day post.",
        f"Personalised {subj} word art with {who} and 20–30 of your own words. Sizes A4 to A1, or framed in black or silver. Order by 12pm for same-day post.",
        f"Personalised {subj} word art print with {who} and your words. A4 to A1 or framed in black or silver, posted next working day by Royal Mail.",
        f"{subj[0].upper() + subj[1:]} word art print, personalised with {who} and your words. A4 to A1 or framed in black or silver. Posted next working day.",
        f"Personalise this {subj} print with {who} and 20–30 words. A4 to A1 print only or framed in black or silver. Posted next working day by Royal Mail.",
    ]
    rot = opts[i % len(opts):] + opts[:i % len(opts)]
    for m in rot:
        if 140 <= len(m) <= 155:
            return title, m
    # pad / trim fallbacks
    for m in rot:
        for extra in (" Order today.", " Great gift.", " A gift they'll keep."):
            if 140 <= len(m + extra) <= 155:
                return title, m + extra
    raise AssertionError((p[0], [len(x) for x in opts]))


def media_kind(url):
    f = url.split("/")[-1].split("?")[0].rsplit(".", 1)[0].upper()
    f = re.sub(r"_[0-9A-F]{8}(-[0-9A-F]{4}){3}-[0-9A-F]{12}$", "", f)
    f = re.sub(r"_[0-9A-F]{6,}$", "", f)
    f = re.sub(r"_\d+$", "", f)
    for k in ("BLACKFRAME", "SILVERFRAME", "WHITEFRAME", "GOLDFRAME", "PINKBACKGROUND", "GREETINGSCARD", "POSTERONLY", "PRINTONLY"):
        if f.endswith(k):
            return {"POSTERONLY": "PRINT", "PRINTONLY": "PRINT"}.get(k, k)
    return None


def plan(before, out):
    nodes = json.load(open(before))["data"]["products"]["nodes"]
    ex = {x["id"] for x in json.load(open(os.path.join(ROOT, "exports/word-art/2026-10-06-sizes/list.json")))}
    P = [n for n in nodes if n["id"] not in ex]
    assert len(P) == len(PROFILES), (len(P), len(PROFILES))
    res, seen, seo_seen = [], set(), {}
    for i, (n, p) in enumerate(zip(P, PROFILES)):
        assert p[0] in n["title"], (i, p[0], n["title"])
        v = n["variants"]["nodes"]
        skip = None
        if len(v) != 1 or v[0]["title"] != "Default Title" or n["options"][0]["name"] != "Title":
            skip = "already has options"
        kw = keyword(p)
        h = describe(i, p)
        assert h not in seen, n["title"]
        seen.add(h)
        probs = check(h, kw)
        assert not probs, (n["title"], probs, words(h))
        st, sd = seo(p, i)
        kinds = {}
        for m in n["media"]["nodes"]:
            kinds.setdefault(media_kind(m["image"]["url"]), []).append(m["id"])
        e = {"id": n["id"], "title": n["title"], "handle": n["handle"], "category": p[3], "keyword": kw,
             "descriptionHtml": h, "words": words(h), "seo_title": st, "seo_description": sd,
             "fields": [name_label(p[3]), MSG], "third_party": p[3] == POP, "color": p[6],
             "age_group": age_group(n["productType"], n["title"], n["tags"]), "skip": skip,
             "base_sku": v[0]["sku"], "variant": v[0], "option": n["options"][0]}
        img_ok = (len(kinds.get("BLACKFRAME", [])) == 1 and len(kinds.get("SILVERFRAME", [])) == 1
                  and None not in kinds)
        e["images_ok"] = bool(img_ok)
        e["media_kinds"] = {k or "?": vv for k, vv in kinds.items()}
        if img_ok:
            alt = kw[0].upper() + kw[1:]
            if p[3] == POP:
                alt = f"Personalised pop figure word art print inspired by {p[1]}"
            e["alts"] = {kinds["BLACKFRAME"][0]: f"{alt} in a black frame", kinds["SILVERFRAME"][0]: f"{alt} in a silver frame"}
            e["detach"] = [m for k in ("WHITEFRAME", "GOLDFRAME", "PINKBACKGROUND", "GREETINGSCARD") for m in kinds.get(k, [])]
            e["order"] = [kinds["BLACKFRAME"][0], kinds["SILVERFRAME"][0]]
        res.append(e)
    json.dump(res, open(os.path.join(out, "plan.json"), "w"), indent=1, ensure_ascii=False)
    print(len(res), "products;", sum(e["images_ok"] for e in res), "images ok; words",
          min(e["words"] for e in res), "-", max(e["words"] for e in res), "; skip", sum(bool(e["skip"]) for e in res))
    for e in res:
        if not e["images_ok"]:
            print("IMAGES LEFT:", e["title"], e["media_kinds"])


def q(s):
    return json.dumps(s, ensure_ascii=False)


def shared_variants(v, qty):
    ii = v["inventoryItem"]
    out = []
    for name, price, suf, fr in NEW:
        wt = FRAMED_W[fr] if fr else ii["measurement"]["weight"]["value"]
        out.append({"optionValues": [{"optionName": "Size", "name": name}], "price": price, "compareAtPrice": None,
                    "taxable": v["taxable"], "inventoryPolicy": v["inventoryPolicy"],
                    "inventoryItem": {"tracked": ii["tracked"], "requiresShipping": ii["requiresShipping"],
                                      "measurement": {"weight": {"value": wt, "unit": "GRAMS"}},
                                      "countryCodeOfOrigin": ii["countryCodeOfOrigin"],
                                      "harmonizedSystemCode": ii["harmonizedSystemCode"]},
                    "inventoryQuantities": [{"locationId": LOC, "availableQuantity": qty}]})
    return out


def phase_a(out, ids, name):
    """Sizes + description + SEO + template + tags + metafields for the given product ids (one document)."""
    plan_ = {e["id"]: e for e in json.load(open(os.path.join(out, "plan.json")))}
    lines, mf, vars_, decl = [], [], {}, []
    qtys = {}
    for n, pid in enumerate(ids):
        e = plan_[pid]
        assert not e["skip"]
        v, opt = e["variant"], e["option"]
        P = q(pid)
        qty = v["inventoryQuantity"]
        if qty not in qtys:
            qtys[qty] = f"V{len(qtys)}"
            vars_[qtys[qty]] = shared_variants(v, qty)
            decl.append(f"${qtys[qty]}: [ProductVariantsBulkInput!]!")
        assert shared_variants(v, qty) == vars_[qtys[qty]]
        lines.append(f'o{n}: productOptionUpdate(productId:{P}, option:{{id:{q(opt["id"])}, name:"Size"}}, optionValuesToUpdate:[{{id:{q(opt["optionValues"][0]["id"])}, name:"A4 Print Only"}}]) {{ userErrors {{ message }} }}')
        lines.append(f'u{n}: productVariantsBulkUpdate(productId:{P}, variants:[{{id:{q(v["id"])}, inventoryItem:{{sku:{q(e["base_sku"] + "-A4")}}}}}]) {{ userErrors {{ message }} }}')
        lines.append(f'c{n}: productVariantsBulkCreate(productId:{P}, variants:${qtys[qty]}) {{ userErrors {{ message }} }}')
        lines.append(f'p{n}: productUpdate(product:{{id:{P}, descriptionHtml:$d{n}, templateSuffix:"personalised", seo:{{title:{q(e["seo_title"])}, description:{q(e["seo_description"])}}}}}) {{ userErrors {{ message }} }}')
        decl.append(f"$d{n}: String!")
        vars_[f"d{n}"] = e["descriptionHtml"]
        add = ["io-word-art"] + (["third-party-name"] if e["third_party"] else [])
        lines.append(f'ta{n}: tagsAdd(id:{P}, tags:{q(add)}) {{ userErrors {{ message }} }}')
        lines.append(f'tr{n}: tagsRemove(id:{P}, tags:["Poster Options"]) {{ userErrors {{ message }} }}')
        fv = "$pf" if e["fields"][0] == "Name (shown largest)" else f"$pf{n}"
        if fv != "$pf":
            vars_[f"pf{n}"] = json.dumps(e["fields"], ensure_ascii=False)
            decl.append(f"$pf{n}: String!")
        g = lambda k, t, val: f'{{ownerId:{P}, namespace:"mm-google-shopping", key:"{k}", type:"{t}", value:{q(val)}}}'
        mf += [f'{{ownerId:{P}, namespace:"foxy", key:"personalise_fields", type:"list.single_line_text_field", value:{fv}}}',
               f'{{ownerId:{P}, namespace:"foxy", key:"mockup", type:"single_line_text_field", value:"photo"}}',
               g("custom_product", "boolean", "true"), g("mpn", "single_line_text_field", e["base_sku"] + "-A4"),
               g("color", "single_line_text_field", e["color"]), g("age_group", "single_line_text_field", e["age_group"]),
               g("gender", "single_line_text_field", "unisex"), g("condition", "single_line_text_field", "new"),
               g("google_product_category", "single_line_text_field", "Home & Garden > Decor > Artwork > Posters, Prints, & Visual Artwork")]
    vars_["pf"] = json.dumps(["Name (shown largest)", MSG], ensure_ascii=False)
    decl.append("$pf: String!")
    lines.append(f'm: metafieldsSet(metafields:[{", ".join(mf)}]) {{ userErrors {{ field message code }} }}')
    doc = f"mutation({', '.join(decl)}) {{\n" + "\n".join(lines) + "\n}\n"
    open(os.path.join(out, f"{name}.graphql"), "w").write(doc)
    json.dump(vars_, open(os.path.join(out, f"{name}.vars.json"), "w"), ensure_ascii=False)
    print(name, len(ids), "products,", len(doc), "bytes doc,", len(json.dumps(vars_)), "bytes vars")


def phase_b(out, after, ids, name):
    """SKUs on the 7 new variants + images (alt, detach, order, variant images)."""
    plan_ = {e["id"]: e for e in json.load(open(os.path.join(out, "plan.json")))}
    suf = {nm: s for nm, _, s, _ in NEW}
    suf["A4 Print Only"] = "-A4"
    prods = {p["id"]: p for p in json.load(open(after))["data"]["nodes"] if p}
    lines = []
    for n, pid in enumerate(ids):
        e, p = plan_[pid], prods[pid]
        P = q(pid)
        ups = []
        for v in p["variants"]["nodes"]:
            item = {}
            want = e["base_sku"] + suf[v["title"]]
            s = f'{{id:{q(v["id"])}'
            if v["sku"] != want:
                s += f', inventoryItem:{{sku:{q(want)}}}'
            if e["images_ok"]:
                t = v["title"]
                mid = e["order"][0] if "Black Frame" in t else e["order"][1] if "Silver Frame" in t else None
                if mid:
                    s += f', mediaId:{q(mid)}'
            s += "}"
            if s != f'{{id:{q(v["id"])}}}':
                ups.append(s)
        if ups:
            lines.append(f'v{n}: productVariantsBulkUpdate(productId:{P}, variants:[{", ".join(ups)}]) {{ userErrors {{ message }} }}')
        if e["images_ok"]:
            files = [f'{{id:{q(k)}, alt:{q(v)}}}' for k, v in e["alts"].items()]
            files += [f'{{id:{q(k)}, referencesToRemove:[{P}]}}' for k in e["detach"]]
            lines.append(f'f{n}: fileUpdate(files:[{", ".join(files)}]) {{ userErrors {{ field message code }} }}')
            moves = ", ".join(f'{{id:{q(k)}, newPosition:"{j}"}}' for j, k in enumerate(e["order"]))
            lines.append(f'r{n}: productReorderMedia(id:{P}, moves:[{moves}]) {{ mediaUserErrors {{ message }} }}')
    doc = "mutation {\n" + "\n".join(lines) + "\n}\n"
    open(os.path.join(out, f"{name}.graphql"), "w").write(doc)
    print(name, len(ids), "products,", len(doc), "bytes")


if __name__ == "__main__":
    if sys.argv[1] == "plan":
        plan(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "a":
        phase_a(sys.argv[2], sys.argv[3].split(","), sys.argv[4])
    elif sys.argv[1] == "b":
        phase_b(sys.argv[2], sys.argv[3], sys.argv[4].split(","), sys.argv[5])
