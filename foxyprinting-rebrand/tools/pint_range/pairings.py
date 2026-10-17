"""Pairing products for the pint range (owner, 16 Oct 2026: "Yes make them").

7 matching whisky tumblers (no prom tumbler: prom is for school leavers) + 3 sets:
Dad pint & tumbler gift set, wedding party pint set (4 or 6), prom group pint set (4, 6 or 8).
Facts: plan/product-facts.md "Printed glassware" (UV DTF, 10 mm below the rim, tumbler print area up to 50 x 50 mm,
care wording). Tumbler capacity is still ASK, so it is not stated.
Prices: tumblers £13.99 like the existing whisky tumblers, £15.99 for the photo cut-out ones (+£2, as on the pints);
sets priced below buying the glasses separately. Owner can change.
"""
import designs as D
import products as PR
import tumblers as TU

DELIVERY = PR.DELIVERY


def tdetails(extra=""):
    return ("<h3>Size &amp; details</h3>\n<ul>\n<li>Glass: classic whisky (rocks) tumbler with a heavy base</li>\n"
            "<li>Print: UV DTF on the outside of the glass, kept 10mm below the rim; the design sits in the middle and the glass "
            "around it stays clear</li>\n<li>Print area: up to 50 x 50 mm</li>\n" + extra +
            "<li>Care: hand wash recommended to keep the print bright; if you must, top rack of the dishwasher on a gentle cycle</li>\n"
            "<li>Made to order in our North Yorkshire workshop</li>\n</ul>")


TTAGS = ["personalised", "whisky tumbler", "whisky glass", "whisky gift", "range-glassware", "range-home-bar", "machine-uvdtf",
         "foxy-new-2026", "dept-home-drinkware", "io-whisky-tumblers", "pint-range-pairings-2026-10-16", "uv dtf glass"]
STAGS = ["personalised", "pint glass", "beer glass", "gift set", "range-glassware", "range-home-bar", "machine-uvdtf", "foxy-new-2026",
         "dept-home-drinkware", "io-pint-glasses", "pint-range-pairings-2026-10-16", "uv dtf glass"]
TCAT = "Home & Garden > Kitchen & Dining > Tableware > Drinkware > Tumblers"
BCAT = "Home & Garden > Kitchen & Dining > Tableware > Drinkware > Beer Glasses"
DCAT = "Home & Garden > Kitchen & Dining > Tableware > Drinkware"

P = [
    dict(key="t_face", kind="tumbler", code="PFHOWT", price="15.99", handle="personalised-face-photo-whisky-tumbler-hands-off", cat=TCAT,
         title="Personalised Face Photo Whisky Tumbler – “Your Name’s Whisky – Hands Off!” – Funny Photo Gift",
         seo_title="Personalised Face Photo Whisky Tumbler | Foxy Printing",
         seo_desc="Put their face on their whisky glass: a personalised face photo whisky tumbler with their name and ‘Hands Off!’ printed in full colour. A gift with a grin.",
         fields=["Face photo upload", "Name", "Bottom line (optional)"], colour="Multicolor",
         tags=["photo gift", "funny gift", "gift for him", "gift for dad", "birthday gift", "face glass"],
         design=lambda v: TU.to_tumbler(D.face_pint(word="WHISKY")),
         alt="Personalised face photo whisky tumbler with a cut-out face and the name’s Whisky – Hands Off! underneath",
         html="""<p>A personalised face photo whisky tumbler keeps the good stuff safe: their own face, their name and a firm “Hands Off!” printed on a heavy rocks glass. It’s the matching partner to our face photo pint glass, and it gets the same laugh every time it comes out of the cabinet.</p>
<h2>Personalised face photo whisky tumbler with their name</h2>
<p>Upload a clear photo of their face and type their name. We cut the face out neatly, add a bold outline so it stands out on the glass, and print, for example, “DAVE’S WHISKY” underneath with “Hands Off!” as the bottom line. Change that line to anything you like – “Back Off!” or “Grandad’s Only” both work. The live preview shows your wording before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Full-colour UV DTF print keeps real skin tones on clear glass</li>
<li>Matches the face photo pint glass for a his-and-his gift set</li>
<li>A funny birthday, Father’s Day or retirement present for a whisky drinker</li>
<li>Best with a front-on, well-lit photo where the face fills the picture</li>
<li>Made to order in our own workshop, one glass at a time</li>
</ul>
""" + tdetails("<li>Photo: we cut the face out from your upload; a sharp phone photo is fine</li>\n") + "\n" + DELIVERY +
         "\n<p>Pair it with the matching face photo pint glass so their beer is protected too.</p>"),

    dict(key="t_dad", kind="tumbler", code="PDNWT", price="13.99", handle="personalised-dad-whisky-tumbler-gold-script-name", cat=TCAT,
         title="Personalised Dad Whisky Tumbler – Bold DAD Lettering with Gold Script Name – Father’s Day Gift",
         seo_title="Personalised Dad Whisky Tumbler with Name | Foxy Printing",
         seo_desc="A personalised Dad whisky tumbler with bold DAD lettering and his name in gold script. Change the word to Grandad or Uncle – on a heavy rocks glass.",
         fields=["Big word (e.g. DAD, GRANDAD, UNCLE)", "Name"], colour="Black",
         tags=["gift for dad", "fathers day", "dad gift", "grandad gift", "dad whisky glass"],
         design=lambda v: TU.to_tumbler(D.word_name_pint()),
         alt="Personalised Dad whisky tumbler with bold black DAD lettering and a gold script name",
         html="""<p>This personalised Dad whisky tumbler is the smart one for his evening dram: big, bold DAD lettering with his name written across it in gold script. It’s the matching glass to our Dad pint glass, made for the man who likes a whisky after the football.</p>
<h2>Personalised Dad whisky tumbler with his name in gold</h2>
<p>Type the big word and his name. DAD is the favourite, but GRANDAD, UNCLE, GRANDPA or a nickname all fit. His name goes on in a flowing gold script over the black letters, a bit like a signature. Check the live preview to see how it sits before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Black and gold UV DTF print, crisp on a clear rocks glass</li>
<li>Heavy-based whisky tumbler that feels good in the hand</li>
<li>Matches the Dad pint glass for a gift set</li>
<li>Change the big word for Grandad, Uncle or Grandpa at no extra cost</li>
<li>A Father’s Day, birthday or Christmas gift he’ll use every week</li>
</ul>
""" + tdetails() + "\n" + DELIVERY + "\n<p>Want both? Our Dad pint and whisky tumbler gift set puts the pair together for less.</p>"),

    dict(key="t_no1", kind="tumbler", code="PN1WT", price="13.99", handle="personalised-no1-grandad-whisky-tumbler", cat=TCAT,
         title="Personalised No.1 Grandad Whisky Tumbler – Hexagon & Arrow Design – Grandad, Dad or Uncle Gift",
         seo_title="Personalised No.1 Grandad Whisky Tumbler | Foxy Printing",
         seo_desc="A personalised No.1 Grandad whisky tumbler in a smart hexagon and arrow design with his name. Change it to No.1 Dad or Uncle – UV printed on a rocks glass.",
         fields=["Title (e.g. GRANDAD, DAD, UNCLE)", "Name"], colour="Black",
         tags=["grandad gift", "gift for grandad", "gift for dad", "fathers day", "no 1 grandad"],
         design=lambda v: TU.to_tumbler(D.hexagon_pint()),
         alt="Personalised No.1 Grandad whisky tumbler with a hexagon frame, gold arrow and name",
         html="""<p>Raise a glass to the best: a personalised No.1 Grandad whisky tumbler with a clean hexagon frame, gold points top and bottom, a big No.1, his title, a gold arrow and his name. It’s the whisky-glass partner to our No.1 Grandad pint glass.</p>
<h2>Personalised No.1 Grandad whisky tumbler with his name</h2>
<p>Pick the title – GRANDAD, DAD, UNCLE, GRANDPA or GRAMPS – and add his name. Both go on in a classic serif font that reads like an old pub sign. The live preview shows the wording before you add it to the basket.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Black and gold UV DTF print on a clear heavy-based tumbler</li>
<li>Only the badge is printed, so his dram shows through all round</li>
<li>A grandad gift for birthdays, Father’s Day and Christmas</li>
<li>Matches the No.1 Grandad pint glass</li>
<li>Made to order with his own name</li>
</ul>
""" + tdetails() + "\n" + DELIVERY + "\n<p>Give him the pair: add the matching No.1 Grandad pint glass for his beer.</p>"),

    dict(key="t_wedding", kind="tumbler", code="PWPWT", price="13.99", handle="personalised-wedding-party-whisky-tumbler", cat=TCAT,
         title="Personalised Wedding Party Whisky Tumbler – Groom, Best Man, Usher or Father of the Bride – Tuxedo Design",
         seo_title="Personalised Best Man Whisky Tumbler | Foxy Printing",
         seo_desc="A personalised wedding party whisky tumbler for the groom, best man, ushers and dads – role, name and wedding date above a tuxedo. Navy or black.",
         fields=["Name", "Wedding date"], colour="Multicolor", options=[("Role", D.WED_ROLES), ("Colour", ["Navy", "Black"])],
         tags=["wedding", "best man gift", "usher gift", "groomsman gift", "father of the bride", "groom gift"],
         design=lambda v: TU.to_tumbler(D.wedding_pint(v[0], col=D.NAVY if v[1] == "Navy" else D.INK)),
         alt="Personalised best man whisky tumbler with the role in script, name and wedding date above a navy tuxedo",
         html="""<p>For the lads who prefer a dram, a personalised wedding party whisky tumbler says thank you in style. Each glass carries their role in elegant script, their name and your wedding date above a smart tuxedo and bow tie, matching our wedding party pint glasses.</p>
<h2>Personalised best man and usher whisky tumblers</h2>
<p>Choose the role – Groom, Best Man, Usher, Groomsman, Father of the Bride or Father of the Groom – and navy or black, then add their name and the date. Order one for each of the party and they’ll all match on the day. The live preview shows each glass before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>A best man, usher or father of the bride gift they’ll keep</li>
<li>Six roles in one matching tuxedo design</li>
<li>Navy or black UV DTF print on a clear heavy-based tumbler</li>
<li>Wedding date on every glass makes it a keepsake</li>
<li>Mix and match with the wedding party pint glasses</li>
</ul>
""" + tdetails() + "\n" + DELIVERY + "\n<p>Buying for the whole party? Our wedding party pint set does four or six glasses for less.</p>"),

    dict(key="t_vintage", kind="tumbler", code="PVBWT", price="13.99", handle="personalised-vintage-birthday-whisky-tumbler", cat=TCAT,
         title="Personalised Vintage Birthday Whisky Tumbler – Name, Year Born & Age – Aged to Perfection Gift",
         seo_title="Personalised Vintage Birthday Whisky Tumbler | Foxy Printing",
         seo_desc="A personalised vintage birthday whisky tumbler with their name, birth year and ‘Aged to Perfection’ – a 40th, 50th, 60th or 70th gift for a whisky fan.",
         fields=["Name", "Year born", "Age"], colour="Black",
         tags=["birthday gift", "milestone birthday", "50th birthday", "60th birthday", "aged to perfection", "vintage", "gift for him"],
         design=lambda v: TU.to_tumbler(D.vintage_pint()),
         alt="Personalised vintage birthday whisky tumbler with a gold script name, VINTAGE 1976 and Aged to Perfection",
         html="""<p>Like a good single malt, some people just get better with age – and a personalised vintage birthday whisky tumbler says so. Their name in gold script sits above VINTAGE and their birth year in big bold numbers, finished with “Aged to Perfection” and their years of awesome.</p>
<h2>Personalised vintage birthday whisky tumbler with year and age</h2>
<p>Add their name, the year they were born and the age they’re turning. It suits a 40th, 50th, 60th, 70th or any milestone, and it matches our vintage birthday pint glass. The live preview shows the finished design before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>A milestone birthday gift for a whisky or rum drinker</li>
<li>Black and gold UV DTF print, sharp on clear glass</li>
<li>Name, birth year and age make it theirs alone</li>
<li>Heavy-based rocks glass for a proper dram</li>
<li>Made to order in our North Yorkshire workshop</li>
</ul>
""" + tdetails() + "\n" + DELIVERY + "\n<p>Pair it with the matching vintage birthday pint glass for the full birthday round.</p>"),

    dict(key="t_pet", kind="tumbler", code="PPFWT", price="15.99", handle="personalised-pet-photo-whisky-tumbler", cat=TCAT,
         title="Personalised Pet Photo Whisky Tumbler – Your Dog or Cat’s Face & Name – Dog Lover Gift",
         seo_title="Personalised Pet Photo Whisky Tumbler | Foxy Printing",
         seo_desc="A personalised pet photo whisky tumbler with your dog or cat’s face, their name and a line like ‘Dad’s Drinking Buddy’, in full colour on a rocks glass.",
         fields=["Pet photo upload", "Pet’s name", "Bottom line (optional)"], colour="Multicolor",
         tags=["pet gift", "dog lover gift", "dog dad", "cat lover gift", "pet photo", "photo gift"],
         design=lambda v: TU.to_tumbler(D.pet_pint()),
         alt="Personalised pet photo whisky tumbler with a dog’s face cut out, the dog’s name and Dad’s Drinking Buddy",
         html="""<p>A personalised pet photo whisky tumbler puts their four-legged best friend on their favourite glass: your dog or cat’s face, their name and a line like “Dad’s Drinking Buddy”, with three little gold paw prints on top. It matches our pet photo pint glass.</p>
<h2>Personalised pet photo whisky tumbler with your pet’s name</h2>
<p>Upload a clear photo of your pet, type their name and choose the bottom line. We cut your pet out neatly and print them in full colour on the clear glass. Keep “Dad’s Drinking Buddy” or change it to “Mum’s Best Friend”, “Good Boy” or anything you like. The live preview shows the wording before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Full-colour UV DTF print keeps your pet’s real colours</li>
<li>Dogs, cats, rabbits, horses – any pet with a face to love</li>
<li>A dog lover gift for birthdays, Christmas and Father’s Day</li>
<li>Best with a sharp, well-lit photo looking at the camera</li>
<li>Made to order, so every glass is one of a kind</li>
</ul>
""" + tdetails("<li>Photo: we cut your pet out from your upload; a sharp phone photo is fine</li>\n") + "\n" + DELIVERY +
         "\n<p>Add the matching pet photo pint glass and the pair make a lovely gift.</p>"),

    dict(key="t_pub", kind="tumbler", code="PSAWT", price="13.99", handle="personalised-the-surname-arms-whisky-tumbler", cat=TCAT,
         title="Personalised Pub Whisky Tumbler – “The [Surname] Arms” Pub Sign Design – Home Bar Gift",
         seo_title="Personalised Family Pub Name Whisky Tumbler | Foxy Printing",
         seo_desc="A personalised pub whisky tumbler with ‘The [Surname] Arms’ on a traditional hanging pub sign, a second line and the year opened. Made for the home bar.",
         fields=["Surname (The ___ Arms)", "Second line (optional)", "Est. year"], colour="Black",
         tags=["home bar", "pub sign", "family name", "gift for dad", "housewarming", "man cave"],
         design=lambda v: TU.to_tumbler(D.pub_pint()),
         alt="Personalised pub whisky tumbler with The Smith Arms on a traditional hanging pub sign design",
         html="""<p>Every family local needs a top shelf, and a personalised pub whisky tumbler gives it one: “The [Surname] Arms” on a traditional hanging pub sign, with a second line and the year established. It matches our family pub name pint glass.</p>
<h2>Personalised pub whisky tumbler – The [Surname] Arms</h2>
<p>Type your surname and we’ll print THE … ARMS in classic pub lettering inside the hanging sign. The second line reads “Free House” unless you’d like the town or street, and the year goes underneath in gold. The live preview shows your pub name before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Traditional British pub sign design with your family name</li>
<li>Black and gold UV DTF print with clear glass all round</li>
<li>A housewarming, Father’s Day or new home bar gift</li>
<li>Matches the family pub name pint glass</li>
<li>Made to order in our own workshop</li>
</ul>
""" + tdetails() + "\n" + DELIVERY + "\n<p>Stock the whole bar: add the matching pint glasses, a home bar sign and coasters.</p>"),

    # ------------------------------------------------------------------ sets
    dict(key="s_dad", kind="set", code="PDGSET", price="22.99", compare="25.98", handle="personalised-dad-pint-and-whisky-tumbler-gift-set", cat=DCAT,
         title="Personalised Dad Pint Glass & Whisky Tumbler Gift Set – Bold DAD with Gold Script Name – Father’s Day Gift",
         seo_title="Personalised Dad Pint & Whisky Tumbler Set | Foxy Printing",
         seo_desc="A personalised Dad pint glass and whisky tumbler gift set: bold DAD lettering with his name in gold script on both. Change the word to Grandad or Uncle.",
         fields=["Big word (e.g. DAD, GRANDAD, UNCLE)", "Name"], colour="Black",
         tags=["gift for dad", "fathers day", "dad gift", "grandad gift", "whisky tumbler", "gift set for him"],
         alt="Personalised Dad pint glass and whisky tumbler gift set, both with bold DAD lettering and a gold script name",
         html="""<p>The personalised Dad pint glass and whisky tumbler gift set covers his beer and his dram in one go. Both glasses carry big, bold DAD lettering with his name across it in gold script, so they look like a proper matching pair on the shelf.</p>
<h2>Personalised Dad pint glass and whisky tumbler gift set</h2>
<p>Type the big word and his name once and we print both glasses to match. DAD is the classic, but GRANDAD, UNCLE, GRANDPA or a nickname all work. You get a 20oz nonic pint glass and a heavy-based whisky tumbler, both printed in black and gold. The live preview shows the design before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Two matching glasses for less than buying them separately</li>
<li>Black and gold UV DTF print, crisp on clear glass</li>
<li>A Father’s Day, birthday or Christmas gift that covers every drink</li>
<li>Change the big word for Grandad, Uncle or Grandpa</li>
<li>Made to order in our own workshop</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>In the set: one 20oz nonic pint glass and one whisky (rocks) tumbler</li>
<li>Print: UV DTF on the outside of each glass, kept 10mm below the rim, with clear glass around the design</li>
<li>Care: hand wash recommended to keep the print bright; if you must, top rack of the dishwasher on a gentle cycle</li>
<li>Made to order in our North Yorkshire workshop</li>
</ul>
""" + DELIVERY + "\n<p>Buying for Grandad as well? Order a second set with GRANDAD as the big word.</p>"),

    dict(key="s_wedding", kind="set", code="PWPSET", price=None, handle="personalised-wedding-party-pint-glass-set", cat=BCAT,
         title="Personalised Wedding Party Pint Glass Set – 4 or 6 Glasses – Groom, Best Man, Ushers & Dads – Tuxedo Design",
         seo_title="Personalised Wedding Party Pint Glass Set | Foxy Printing",
         seo_desc="A personalised wedding party pint glass set of 4 or 6 – each with its own role, name and your wedding date above a tuxedo. Navy or black. Save on the set.",
         fields=["Message – one line per glass: role and name (e.g. Best Man – Tom)", "Wedding date"], colour="Multicolor",
         options=[("Set", ["Set of 4", "Set of 6"]), ("Colour", ["Navy", "Black"])], prices={"Set of 4": ("42.99", "47.96"), "Set of 6": ("62.99", "71.94")},
         tags=["wedding", "best man gift", "usher gift", "groomsman gift", "father of the bride", "groom gift", "wedding party set"],
         alt="Personalised wedding party pint glass set with Groom, Best Man and Usher tuxedo designs",
         html="""<p>Kit out the whole top table with a personalised wedding party pint glass set. You get four or six matching pints, each with its own role in elegant script – Groom, Best Man, Usher, Groomsman, Father of the Bride or Father of the Groom – plus a name and your wedding date above a smart tuxedo and bow tie.</p>
<h2>Personalised wedding party pint glass set</h2>
<p>Choose a set of 4 or 6 and navy or black. In the message box, write one line per glass with the role and name, for example “Best Man – Tom”, then add the wedding date once. We print each glass to match. You can use any role more than once – three ushers is no problem. The live preview shows the design before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Every glass matches, so they look great lined up on the day</li>
<li>Cheaper than buying the glasses one at a time</li>
<li>Navy or black UV DTF print on clear 20oz nonic pints</li>
<li>A best man, usher and groomsman thank-you in one order</li>
<li>Wedding date on every glass makes them a keepsake</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>In the set: 4 or 6 x 20oz nonic pint glasses, each printed with its own role and name</li>
<li>Print: UV DTF on the outside of each glass, kept 10mm below the rim, with clear glass around the design</li>
<li>Care: hand wash recommended to keep the print bright; if you must, top rack of the dishwasher on a gentle cycle</li>
<li>Made to order in our North Yorkshire workshop</li>
</ul>
""" + DELIVERY + "\n<p>Got a whisky man in the party? Swap one in with the matching wedding party whisky tumbler.</p>"),

    dict(key="s_prom", kind="set", code="PPROMSET", price=None, handle="personalised-prom-pint-glass-group-set", cat=BCAT,
         title="Personalised Prom Pint Glass Group Set – 4, 6 or 8 Glasses – Names & Year – Tuxedo, Braces or Bow Tie Design",
         seo_title="Personalised Prom Pint Glass Group Set | Foxy Printing",
         seo_desc="A personalised prom pint glass group set of 4, 6 or 8 – each glass with its own name and prom year above a tuxedo, braces or bow tie. Save on the set.",
         fields=["Message – names for each glass, one per line", "Prom year", "Colour (Black, Navy, Red or Pink)"], colour="Multicolor",
         options=[("Set", ["Set of 4", "Set of 6", "Set of 8"]), ("Design", ["Tuxedo", "Braces & Bow Tie", "Bow Tie & Buttons"])],
         prices={"Set of 4": ("42.99", "47.96"), "Set of 6": ("62.99", "71.94"), "Set of 8": ("82.99", "95.92")},
         tags=["prom", "prom gift", "prom 2026", "leavers gift", "keepsake", "group gift", "prom set"],
         alt="Personalised prom pint glass group set with names and the prom year above tuxedo designs",
         html="""<p>Make the whole group’s night one to remember with a personalised prom pint glass group set. Every glass carries its own name and “Prom” in elegant script with the year underneath, above a smart tuxedo, braces or bow tie design – a keepsake for each friend.</p>
<h2>Personalised prom pint glass group set</h2>
<p>Choose a set of 4, 6 or 8 and the outfit design, then type the names in the message box, one per line, add the prom year and pick a colour – black, navy, red or pink. We print each glass with its own name so the set matches. The live preview shows the design before you order.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>A prom keepsake and leavers gift for the whole group in one order</li>
<li>Cheaper than buying the glasses one at a time</li>
<li>Three outfit designs and four colours to match the suits</li>
<li>Full-colour UV DTF print on clear 20oz nonic pints</li>
<li>Made to order in our workshop, each with its own name</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>In the set: 4, 6 or 8 x 20oz nonic pint glasses, each printed with its own name</li>
<li>Print: UV DTF on the outside of each glass, kept 10mm below the rim, with clear glass around the design</li>
<li>Care: hand wash recommended to keep the print bright; if you must, top rack of the dishwasher on a gentle cycle</li>
<li>Made to order in our North Yorkshire workshop</li>
</ul>
""" + DELIVERY + "\n<p>Need a different colour for each friend? Order single prom pint glasses and mix them up.</p>"),
]


def variants(p):
    pre = f"FOXY-UVDTF-{p['code']}"
    if "options" not in p:
        return [((), f"{pre}-01", p["price"], p.get("compare"))]
    (n1, v1), (n2, v2) = p["options"]
    out, i = [], 0
    for a in v1:
        for b in v2:
            i += 1
            pr, cmp = p["prices"][a] if "prices" in p else (p["price"], None)
            out.append(((a, b), f"{pre}-{i:02d}", pr, cmp))
    return out
