"""Product data + copy for the 8 new personalised pint glasses (owner, 9 Oct 2026: "yes make all 8 and list on foxy").

Facts from plan/product-facts.md "Printed glassware: full-colour UV DTF": 20oz nonic pint, UV DTF on the outside of
the glass kept 10 mm below the rim, print area up to 90 x 130 mm, care wording, made in the North Yorkshire workshop.
Prices: £11.99 like the other personalised pints; £13.99 for the two photo-cut-out designs (more artwork per order;
Etsy UK face pints sell at ~£13–£19). Owner can change.
"""
import designs as D

DELIVERY = ("<h3>Delivery</h3>\n<p>Every glass is made to order in our North Yorkshire workshop. Postage options and costs are shown "
            "at checkout, and if you have a date to hit, give us a ring on 01439 771468 before you order.</p>")


def details(extra=""):
    return ("<h3>Size &amp; details</h3>\n<ul>\n<li>Glass: 20oz nonic pint glass, the classic British pub shape</li>\n"
            "<li>Print: UV DTF on the outside of the glass, kept 10mm below the rim; the design sits in the middle of the glass "
            "and the glass around it stays clear</li>\n" + extra +
            "<li>Care: hand wash recommended to keep the print bright; if you must, top rack of the dishwasher on a gentle cycle</li>\n"
            "<li>Made to order in our North Yorkshire workshop</li>\n</ul>")


BASE_TAGS = ["personalised", "pint glass", "beer glass", "range-glassware", "range-home-bar", "machine-uvdtf", "foxy-new-2026",
             "dept-home-drinkware", "io-pint-glasses", "pint-range-2026-10-09", "uv dtf glass"]

P = [
    dict(key="face", code="PFHOPG", price="13.99", handle="personalised-face-photo-pint-glass-hands-off",
         title="Personalised Face Photo Pint Glass – “Your Name’s Pint – Hands Off!” – Funny Gift with Your Photo",
         seo_title="Personalised Face Photo Pint Glass | Foxy Printing",
         seo_desc="Put their face on their pint: a personalised face photo pint glass with their name and ‘Hands Off!’, printed in full colour on a 20oz pint. Guaranteed laughs.",
         fields=["Face photo upload", "Name", "Bottom line (optional)"], colour="Multicolor",
         tags=["photo gift", "face pint", "funny gift", "gift for him", "gift for dad", "birthday gift", "secret santa"],
         design=lambda v: D.face_pint(),
         alt="Personalised face photo pint glass with the face cut out and the name’s Pint – Hands Off! printed underneath",
         html="""<p>A personalised face photo pint glass is the surest way to stop anyone pinching their pint: their own grinning face, their name and a firm “Hands Off!” printed right on the glass. It gets passed round the table at birthdays, stag dos and Christmas.</p>
<h2>Personalised face photo pint glass with their name</h2>
<p>Upload a clear photo of their face, add their name and we’ll do the rest. We cut the face out neatly, add a bold outline so it pops off the glass, and print, for example, “DAVE’S PINT” underneath in big bold letters. The bottom line says “Hands Off!” unless you’d like something else – “Back Off!”, “Dad’s Only” or a house joke all work. The live preview shows your wording before you add it to the basket.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Full-colour UV DTF print, so the photo keeps real skin tones instead of a grey engraving</li>
<li>Only the face and words are printed – the rest of the 20oz pint stays crystal clear</li>
<li>Best with a front-on, well-lit photo where the face fills most of the picture</li>
<li>A funny birthday, Father’s Day or secret Santa gift that actually gets used</li>
<li>Made to order, one glass at a time, in our own workshop</li>
</ul>
""" + details("<li>Photo: we cut the face out from your upload; a sharp phone photo is fine</li>\n") + "\n" + DELIVERY +
         "\n<p>Doing a group? Order one for each of the lads with their own face – nobody will ever drink from the wrong pint again.</p>"),

    dict(key="dad", code="PDNPG", price="11.99", handle="personalised-dad-pint-glass-gold-script-name",
         title="Personalised Dad Pint Glass – Bold DAD Lettering with Gold Script Name – Father’s Day & Birthday Gift",
         seo_title="Personalised Dad Pint Glass with Name | Foxy Printing",
         seo_desc="A personalised Dad pint glass with bold DAD lettering and his name in gold script. Change the word to Grandad, Uncle or Grandpa – printed on a 20oz pint.",
         fields=["Big word (e.g. DAD, GRANDAD, UNCLE)", "Name"], colour="Black",
         tags=["gift for dad", "fathers day", "dad gift", "grandad gift", "dad pint glass", "birthday gift"],
         design=lambda v: D.word_name_pint(),
         alt="Personalised Dad pint glass with bold black DAD lettering and a gold script name across it",
         html="""<p>This personalised Dad pint glass keeps it simple and smart: big, bold DAD lettering with his name written across it in flowing gold script. It looks like something from a proper bar, and it’s the one glass in the cupboard nobody else will dare to use.</p>
<h2>Personalised Dad pint glass with his name in gold</h2>
<p>Type the big word and his name. DAD is the favourite, but GRANDAD, UNCLE, GRANDPA, BROTHER or even a nickname fit the same design. His name goes on in a gold handwritten-style script over the black letters, just like a signature. Check the live preview to see how your words sit before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Black and gold UV DTF print that stays crisp on clear glass</li>
<li>Bold block letters you can read from across the room</li>
<li>Works for Father’s Day, his birthday, Christmas or a “just because”</li>
<li>Change the big word for Grandad, Uncle or Grandpa at no extra cost</li>
<li>Printed in the middle of a 20oz nonic pint, leaving the rest of the glass clear</li>
</ul>
""" + details() + "\n" + DELIVERY +
         "\n<p>Buying for a few generations? Do a DAD and a GRANDAD glass as a pair for Father’s Day.</p>"),

    dict(key="no1", code="PN1PG", price="11.99", handle="personalised-no1-grandad-pint-glass",
         title="Personalised No.1 Grandad Pint Glass – Hexagon & Arrow Design – Dad, Grandad or Uncle Gift with Name",
         seo_title="Personalised No.1 Grandad Pint Glass | Foxy Printing",
         seo_desc="A personalised No.1 Grandad pint glass in a smart hexagon and arrow design with his name. Change it to No.1 Dad, Uncle or Grandpa – printed on a 20oz pint.",
         fields=["Title (e.g. GRANDAD, DAD, UNCLE)", "Name"], colour="Black",
         tags=["grandad gift", "gift for grandad", "gift for dad", "fathers day", "no 1 grandad", "birthday gift"],
         design=lambda v: D.hexagon_pint(),
         alt="Personalised No.1 Grandad pint glass with a hexagon frame, gold arrow and name",
         html="""<p>Tell him he’s the best with a personalised No.1 Grandad pint glass. The design is a clean hexagon frame with gold points top and bottom, a big No.1, his title, a gold arrow and his name underneath – smart enough for a proper pint and simple enough to suit any kitchen shelf.</p>
<h2>Personalised No.1 Grandad pint glass with his name</h2>
<p>Pick the title – GRANDAD is the classic, but DAD, UNCLE, GRANDPA or GRAMPS all fit – then add his name. We set both in a classic serif font so it reads like an old pub sign. The live preview shows the finished wording before you add it to the basket.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Crisp black and gold UV DTF print on a clear 20oz nonic pint</li>
<li>Only the badge is printed, so the beer shows through all around it</li>
<li>A grandad gift for birthdays, Father’s Day and Christmas</li>
<li>Change the title for Dad, Uncle or Grandpa to suit</li>
<li>Made to order with his own name, not a stock print</li>
</ul>
""" + details() + "\n" + DELIVERY +
         "\n<p>Pair it with a matching No.1 Dad glass so the whole family tree is covered for Father’s Day.</p>"),

    dict(key="prom", code="PPROMPG", price="11.99", handle="personalised-prom-pint-glass-tuxedo-bow-tie",
         title="Personalised Prom Pint Glass – Name & Year – Tuxedo, Braces or Bow Tie Design – Prom Keepsake Gift",
         seo_title="Personalised Prom Pint Glass with Name | Foxy Printing",
         seo_desc="A personalised prom pint glass with their name and prom year above a tuxedo, braces or bow tie design, in black, navy, red or pink. A keepsake of the big night.",
         fields=["Name", "Prom year"], colour="Multicolor",
         options=[("Design", ["Tuxedo", "Braces & Bow Tie", "Bow Tie & Buttons"]), ("Colour", ["Black", "Navy", "Red", "Pink"])],
         tags=["prom", "prom gift", "prom 2026", "leavers gift", "keepsake", "tuxedo", "bow tie"],
         design=lambda v: D.prom_pint({"Tuxedo": "tuxedo", "Braces & Bow Tie": "braces", "Bow Tie & Buttons": "bowtie"}[v[0]], v[1]),
         alt="Personalised prom pint glass with the name, Prom and year above a navy tuxedo and bow tie design",
         html="""<p>A personalised prom pint glass is a keepsake of the big night that will still be on the shelf years later. Their name and “Prom” go across the top in an elegant script with the year underneath, and below sits a smart tuxedo, braces or bow tie outfit – suited and booted, just like them.</p>
<h2>Personalised prom pint glass with name and year</h2>
<p>Choose the outfit design and the colour, then add their name and prom year. The tuxedo has lapels, a bow tie and buttons; Braces &amp; Bow Tie gives the dapper look; Bow Tie &amp; Buttons is the minimal one. Every design comes in black, navy, red or pink. The live preview shows the name before you add it to the basket.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>A prom keepsake and leavers gift with their own name and year</li>
<li>Three outfit designs and four colours, so you can match the suit or the tie</li>
<li>Full-colour UV DTF print on a clear 20oz nonic pint</li>
<li>Order a set for the whole group with each friend’s name</li>
<li>Made to order in our workshop, not a mass-produced print</li>
</ul>
""" + details() + "\n" + DELIVERY +
         "\n<p>Ordering for the whole prom group? Mix the colours and designs – every glass is printed with its own name.</p>"),

    dict(key="wedding", code="PWPPG", price="11.99", handle="personalised-wedding-party-pint-glass-tuxedo",
         title="Personalised Wedding Party Pint Glass – Groom, Best Man, Usher, Groomsman or Father of the Bride – Tuxedo Design",
         seo_title="Personalised Best Man & Usher Pint Glass | Foxy Printing",
         seo_desc="A personalised wedding party pint glass for the groom, best man, ushers and dads – their role, name and wedding date above a tuxedo design. Black or navy.",
         fields=["Name", "Wedding date"], colour="Multicolor",
         options=[("Role", D.WED_ROLES), ("Colour", ["Navy", "Black"])],
         tags=["wedding", "best man gift", "usher gift", "groomsman gift", "father of the bride", "wedding favour", "groom gift"],
         design=lambda v: D.wedding_pint(v[0], col=D.NAVY if v[1] == "Navy" else D.INK),
         alt="Personalised best man pint glass with the role in script, name and wedding date above a navy tuxedo design",
         html="""<p>Thank the lads who stood beside you with a personalised wedding party pint glass. Each glass carries their role in elegant script – Groom, Best Man, Usher, Groomsman, Father of the Bride or Father of the Groom – with their name and your wedding date, above a smart tuxedo and bow tie.</p>
<h2>Personalised best man and usher pint glasses</h2>
<p>Pick the role and the colour (navy or black), then type their name and the wedding date. Every glass in the set matches, so they look great lined up at the top table or handed out the night before. The live preview shows each glass before it goes in the basket.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Six roles, from the groom to both fathers, all in one matching design</li>
<li>A best man gift, usher gift or groomsman thank-you they’ll actually use</li>
<li>Navy or black UV DTF print on a clear 20oz nonic pint</li>
<li>Wedding date on every glass makes it a lasting keepsake</li>
<li>Made to order, so you can add a glass for anyone in the party</li>
</ul>
""" + details() + "\n" + DELIVERY +
         "\n<p>Add one for the groom too – order each role separately and they’ll all match on the day.</p>"),

    dict(key="vintage", code="PVBPG", price="11.99", handle="personalised-vintage-birthday-pint-glass",
         title="Personalised Vintage Birthday Pint Glass – Name, Year Born & Age – Aged to Perfection 30th 40th 50th 60th Gift",
         seo_title="Personalised Vintage Birthday Pint Glass | Foxy Printing",
         seo_desc="A personalised vintage birthday pint glass with their name, the year they were born and ‘Aged to Perfection’. Great for a 30th, 40th, 50th or 60th birthday.",
         fields=["Name", "Year born", "Age"], colour="Black",
         tags=["birthday gift", "milestone birthday", "40th birthday", "50th birthday", "60th birthday", "vintage", "aged to perfection", "gift for him"],
         design=lambda v: D.vintage_pint(),
         alt="Personalised vintage birthday pint glass with a gold script name, VINTAGE 1976 and Aged to Perfection",
         html="""<p>Celebrate a big birthday with a personalised vintage birthday pint glass – because some things really do get better with age. Their name sits in gold script above VINTAGE and the year they were born in big bold numbers, finished with “Aged to Perfection” and how many years of awesome they’ve clocked up.</p>
<h2>Personalised vintage birthday pint glass with year and age</h2>
<p>Add their name, the year they were born and the age they’re turning. It suits every milestone – 30th, 40th, 50th, 60th, 70th and beyond – and the age line reads “50 Years of Awesome” (or whatever their number is). The live preview shows the finished glass before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>A milestone birthday gift for a 30th, 40th, 50th or 60th</li>
<li>Black and gold UV DTF print that stays sharp on clear glass</li>
<li>Name, birth year and age, so it’s unique to them</li>
<li>Printed in the middle of a 20oz nonic pint, with the rest kept clear</li>
<li>Made to order in our North Yorkshire workshop</li>
</ul>
""" + details() + "\n" + DELIVERY +
         "\n<p>Throwing a party? Pair it with a personalised birthday card or a matching whisky tumbler.</p>"),

    dict(key="pet", code="PPFPG", price="13.99", handle="personalised-pet-photo-pint-glass",
         title="Personalised Pet Photo Pint Glass – Your Dog or Cat’s Face & Name – Dog Dad Gift",
         seo_title="Personalised Pet Photo Pint Glass | Foxy Printing",
         seo_desc="A personalised pet photo pint glass with your dog or cat’s face, their name and a line like ‘Dad’s Drinking Buddy’. Full-colour print on a 20oz pint.",
         fields=["Pet photo upload", "Pet’s name", "Bottom line (optional)"], colour="Multicolor",
         tags=["pet gift", "dog lover gift", "dog dad", "cat lover gift", "pet photo", "photo gift", "gift for dad"],
         design=lambda v: D.pet_pint(),
         alt="Personalised pet photo pint glass with a dog’s face cut out, the dog’s name and Dad’s Drinking Buddy",
         html="""<p>A personalised pet photo pint glass puts their best friend on their pint: your dog or cat’s face, their name in bold and a line like “Dad’s Drinking Buddy”. It’s the perfect gift for every dog dad, cat mum and proud pet parent – and it raises a smile every time it comes out of the cupboard.</p>
<h2>Personalised pet photo pint glass with your pet’s name</h2>
<p>Upload a clear photo of your pet, type their name and choose the bottom line. We cut your pet out neatly and print them in full colour with three little gold paw prints above. Leave the bottom line as “Dad’s Drinking Buddy” or change it – “Mum’s Best Friend”, “Good Boy” and “Walkies Then Pub” are favourites. The live preview shows the wording before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Full-colour UV DTF print keeps your pet’s real fur colours</li>
<li>Works for dogs, cats, rabbits and horses – any pet with a face to love</li>
<li>Best with a sharp, well-lit photo looking at the camera</li>
<li>A dog lover gift for birthdays, Christmas and Father’s Day</li>
<li>Made to order, so every glass is one of a kind</li>
</ul>
""" + details("<li>Photo: we cut your pet out from your upload; a sharp phone photo is fine</li>\n") + "\n" + DELIVERY +
         "\n<p>Got more than one? Order a glass for each pet – they’ll make a lovely set on the shelf.</p>"),

    dict(key="pub", code="PSAPG", price="11.99", handle="personalised-the-surname-arms-pub-pint-glass",
         title="Personalised Pub Pint Glass – “The [Surname] Arms” Traditional Pub Sign Design – Home Bar Gift",
         seo_title="Personalised Family Pub Name Pint Glass | Foxy Printing",
         seo_desc="Your own local on a pint: a personalised pub pint glass with ‘The [Surname] Arms’ on a traditional hanging pub sign, a second line and the year established.",
         fields=["Surname (The ___ Arms)", "Second line (optional)", "Est. year"], colour="Black",
         tags=["home bar", "home bar pint glass", "pub sign", "family name", "gift for dad", "housewarming", "man cave"],
         design=lambda v: D.pub_pint(),
         alt="Personalised pub pint glass with The Smith Arms on a traditional hanging pub sign design",
         html="""<p>Every home bar deserves a proper pub name, and this personalised pub pint glass gives it one: “The [Surname] Arms” on a traditional hanging pub sign, with a second line and the year it was established. It turns the kitchen, the shed or the garden bar into the family local.</p>
<h2>Personalised pub pint glass – The [Surname] Arms</h2>
<p>Type your surname and we’ll print THE … ARMS in classic pub lettering inside the hanging sign. The second line reads “Free House” unless you’d like the town, the street or “Est. by Dad”, and the year goes at the bottom in gold. The live preview shows your pub name before you add it to the basket.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Traditional British pub sign design with your family name</li>
<li>Black and gold UV DTF print, clear glass all around</li>
<li>A housewarming, Father’s Day or new home bar gift</li>
<li>Second line and year let you make it your own</li>
<li>Made to order in our own workshop</li>
</ul>
""" + details() + "\n" + DELIVERY +
         "\n<p>Complete the pub with a matching home bar sign and a set of coasters for the regulars.</p>"),
]


def variants(p):
    """list of (option values tuple, sku)"""
    pre = f"FOXY-UVDTF-{p['code']}"
    if "options" not in p:
        return [((), f"{pre}-01")]
    out = []
    (n1, v1), (n2, v2) = p["options"]
    i = 0
    for a in v1:
        for b in v2:
            i += 1
            out.append(((a, b), f"{pre}-{i:02d}"))
    return out
