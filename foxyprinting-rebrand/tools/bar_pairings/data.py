"""Bar-mat pairing products (owner, 8 Oct 2026): "matching coasters, personalised pint glasses or whisky
tumblers, and home bar signs ... YES MAKE ALL OF THESE".

Facts used (nothing invented):
* Coasters: the live drinks-coaster listings - square cork-backed MDF/hardboard coaster, 90 x 90 mm, bright
  glossy finish, dye-sublimation printed, sold singly at 3.99 (50 g).
* Glassware: plan/product-facts.md "Printed glassware: full-colour UV DTF" + the live Personalised Pint Glass
  (11.99) and Personalised Whisky Tumbler (13.99). 20oz nonic pint. Tumbler capacity ASK. Print kept 10mm below
  the rim. Care: hand wash recommended; if you must, top rack on a gentle cycle.
* Metal signs: product-facts "Home bar" + "Metal photo panels" and the live Personalised Metal Pub Sign:
  1.15mm ultra HD gloss white aluminium, dye-sublimation, 12 x 5in panoramic (30.5 x 12.7cm) 19.99 or
  8 x 10in 24.99. Fixings / outdoor use not confirmed.
* No proofs: "We print exactly what you enter ..." line.
"""

COASTER_PRICE = "3.99"
PINT_PRICE = "11.99"
TUMBLER_PRICE = "13.99"
SIGN_SIZES = [("12 x 5in panoramic", "19.99", "wide"), ("8 x 10in", "24.99", "tall")]

PINT_CAT = "Home & Garden > Kitchen & Dining > Tableware > Drinkware > Beer Glasses"
TUMBLER_CAT = "Home & Garden > Kitchen & Dining > Tableware > Drinkware > Tumblers"
COASTER_CAT = "Home & Garden > Kitchen & Dining > Barware > Coasters"
SIGN_CAT = "Home & Garden > Decor > Decorative Plaques"

NO_PROOF = "We print exactly what you enter, so please check names and spelling in the live preview before you order."

PINT_SPECS = """<h3>Size &amp; details</h3>
<ul>
<li>Glass: 20oz nonic pint glass</li>
<li>Print: full-colour UV DTF on the outside of the glass, kept 10mm below the rim</li>
<li>Care: hand wash recommended to keep the print bright; if you must, top rack of the dishwasher on a gentle cycle</li>
<li>Made to order in our North Yorkshire workshop</li>
</ul>"""

TUMBLER_SPECS = """<h3>Size &amp; details</h3>
<ul>
<li>Glass: classic whisky (rocks) tumbler</li>
<li>Print: full-colour UV DTF on the outside of the glass, kept 10mm below the rim</li>
<li>Care: hand wash recommended to keep the print bright; if you must, top rack of the dishwasher on a gentle cycle</li>
<li>Made to order in our North Yorkshire workshop</li>
</ul>"""

SIGN_SPECS = """<h3>Size &amp; details</h3>
<ul>
<li>Material: 1.15mm ultra HD gloss white aluminium</li>
<li>Sizes: 12 x 5in panoramic (30.5 x 12.7cm) or 8 x 10in</li>
<li>Print: full-colour dye-sublimation</li>
<li>Wall fixings and outdoor use: not confirmed yet, so please get in touch if you need them</li>
</ul>"""

COASTER_SPECS = """<h3>Size &amp; details</h3>
<ul>
<li>Square coaster, 90 x 90 mm</li>
<li>Cork-backed MDF with a bright glossy finish</li>
<li>Print: dye-sublimation, full colour</li>
<li>Sold as a single coaster</li>
</ul>"""

DELIVERY = ("<h3>Delivery</h3>\n<p>Every order is made to order in our North Yorkshire workshop. Postage options and costs "
            "are shown at checkout, and if you have a date to hit, give us a ring on 01439 771468 before you order.</p>")


def ul(items):
    return "<ul>\n" + "\n".join(f"<li>{i}</li>" for i in items) + "\n</ul>"


def desc(opening, h2, how, love, specs, close, delivery=DELIVERY):
    return (f"<p>{opening}</p>\n<h2>{h2}</h2>\n<p>{how}</p>\n<h3>Why you’ll love it</h3>\n{ul(love)}\n{specs}\n"
            f"{delivery}\n<p>{close}</p>")


BASE_TAGS = ["foxy-new-2026", "personalised", "range-home-bar", "home bar", "bar-pairings-2026-10-08", "io-home-bar"]

P = []

# ======================================================================= COASTER
P.append(dict(
    key="club_coaster", kind="coaster", theme="club", code="PCCC", machine="SUB",
    title="Personalised Club Colours Coaster – Your Club Badge & Team Name – Matches Our Club Bar Mats",
    handle="personalised-club-colours-coaster",
    productType="Coasters",
    tags=BASE_TAGS + ["drinks-coaster-2026", "bar-coaster-2026", "football-coaster-2026", "club coaster", "team colours", "clubhouse",
                      "football club gift", "machine-sublimation", "io-football"],
    fields=["Club or team name", "Club badge upload", "Welcome line (optional)", "Est. year (optional)"],
    mockup="photo", cat=COASTER_CAT, color="Multicolor",
    sample=dict(name="YOUR CLUB NAME", est="EST. 1987"), art=dict(name="AVA’S FC", est="EST. 1987"),
    matches=["personalised-club-bar-mat-red-and-white", "personalised-club-bar-mat-blue-and-white"],
    seo_title="Personalised Club Colours Coaster | Foxy Printing",
    seo_desc="A personalised club colours coaster with your own badge and team name, in 17 colourways to match our club bar mats. Cork-backed and printed in the UK.",
    descriptionHtml=desc(
        "A personalised club colours coaster is the little finishing touch for any clubhouse bar, supporters’ lounge or "
        "home bar where the team comes first. Pick your club’s colours, upload your badge and add the team name, and every "
        "pint has its own spot to land on.",
        "Personalised club colours coaster with your badge",
        "Choose from 17 team colourways, from red and white stripes to claret and blue, then upload your club badge and "
        "type the club or team name. You can change the small ‘Welcome to’ line and add the year the club was formed, or "
        "leave those boxes blank and we keep the design as shown. The live preview shows it as you type. " + NO_PROOF +
        " Please only upload badges your club has the right to use.",
        ["Designed to match our personalised club bar mats, in the same 17 team colours",
         "Your own badge printed in the white circle, so it works for any football, rugby, cricket or darts club",
         "Bright glossy finish with a cork back that protects the bar top or table",
         "Dye-sublimation print, so the colours are part of the surface rather than a sticker",
         "Handy for raffles, presentation nights and thank-you gifts for volunteers"],
        COASTER_SPECS,
        "Pair it with a club bar mat and a personalised club colours pint glass and the clubhouse bar is ready for match day.")))

# ======================================================================= PINT GLASSES
P.append(dict(
    key="club_pint", kind="pint", theme="club", code="PCCPG", machine="UVDTF",
    title="Personalised Club Colours Pint Glass – Your Club Badge & Team Name – 17 Team Colours",
    handle="personalised-club-colours-pint-glass",
    productType="Personalised Glassware",
    tags=BASE_TAGS + ["range-glassware", "dept-home-drinkware", "pint glass", "beer glass", "club pint glass", "team colours",
                      "football club gift", "clubhouse", "machine-uvdtf", "io-football"],
    fields=["Club or team name", "Club badge upload", "Welcome line (optional)", "Est. year (optional)"],
    mockup="drinkware", cat=PINT_CAT, color="Multicolor",
    sample=dict(name="YOUR CLUB NAME", est="EST. 1987"), art=dict(name="AVA’S FC", est="EST. 1987"),
    matches=["personalised-club-bar-mat-red-and-white-stripes", "personalised-club-bar-mat-green-and-white-hoops"],
    seo_title="Personalised Club Colours Pint Glass | Foxy Printing",
    seo_desc="A personalised club colours pint glass with your own badge and team name in full colour. 17 colourways to match our club bar mats, printed in the UK.",
    descriptionHtml=desc(
        "This personalised club colours pint glass puts your own badge and team name on a proper 20oz pint, in the colours "
        "you wear every Saturday. It’s a great one for players, coaches, committee members and the fans who never miss a game.",
        "A personalised club colours pint glass for your team",
        "Choose your team colours from the 17 options, upload your club badge and type the club or team name. The ‘Welcome "
        "to’ line and the year the club was formed are optional, so leave them blank to keep the design as shown. Check "
        "everything in the live preview first. " + NO_PROOF + " Please only upload badges your club has the right to use.",
        ["Printed in full colour with UV DTF, so the badge keeps its real colours instead of a plain etched outline",
         "The same 17 team colourways as our personalised club bar mats and coasters",
         "A 20oz nonic pint that suits lager, bitter or cider",
         "Lovely as a player of the season prize, a thank-you for the coach or a birthday gift for a lifelong fan",
         "Order one for every player and the whole squad gets a matching glass"],
        PINT_SPECS,
        "Add a matching club colours coaster and bar mat, and the clubhouse bar looks like it was kitted out by the club shop.")))

PINTS = [
    dict(key="rustic_pint", theme="rustic", code="PRHBPG",
         title="Personalised Home Bar Pint Glass – Rustic Established Design – Your Bar Name & Year",
         handle="personalised-home-bar-pint-glass-rustic-established",
         tags=["home bar pint glass", "established sign", "rustic bar", "gift for dad", "man cave"],
         fields=["Bar name", "Welcome line (optional)", "Est. year"],
         sample=dict(name="JACK’S BAR", est="2021"),
         matches=["personalised-bar-mat-runner-rustic-established", "personalised-bar-mat-runner-vintage-wood-established"],
         seo_title="Personalised Home Bar Pint Glass – Rustic | Foxy Printing",
         seo_desc="A personalised home bar pint glass in our rustic Established design – add your bar name and year. Full-colour print on a 20oz pint, made in the UK.",
         d=desc("A personalised home bar pint glass is the easiest way to make the shed bar, the garage bar or the corner of the "
                "kitchen feel like the local. This one wears our rustic Established design: warm wood tones, gold frame lines "
                "and your bar name front and centre.",
                "Personalised home bar pint glass with your bar name",
                "Type in your bar name and the year it opened. We print ‘Welcome to’ above the name, and you can change that "
                "line if you’d rather say something else. The live preview shows your wording on the design before you add it "
                "to the basket. " + NO_PROOF,
                ["Full-colour UV DTF print, so the wood-look panel and gold detail come out in proper colour",
                 "Matches our Rustic Established and Vintage Wood bar mat runners",
                 "A 20oz nonic pint, the classic British pub shape",
                 "Good for Father’s Day, a housewarming or the day the home bar finally opens",
                 "Made to order, so every glass carries your own bar name"],
                PINT_SPECS,
                "Make a set for the regulars, or pair it with the matching rustic home bar sign for over the bar.")),
    dict(key="man_cave_pint", theme="man_cave", code="PMCPG",
         title="Personalised Man Cave Pint Glass – Gold & Charcoal Welcome Design – Your Name",
         handle="personalised-man-cave-pint-glass",
         tags=["man cave", "man cave gift", "gift for him", "gift for dad", "beer gift"],
         fields=["Name", "Est. year (optional)"],
         sample=dict(name="STEVE’S", est="2021"),
         matches=["bar-mat-runner-man-cave-welcome", "personalised-bar-mat-runner-name-man-cave"],
         seo_title="Personalised Man Cave Pint Glass | Foxy Printing",
         seo_desc="A personalised man cave pint glass with his name on our gold and charcoal Welcome design. Full-colour print on a 20oz pint glass, made to order in the UK.",
         d=desc("Every man cave needs its own glassware, and a personalised man cave pint glass with his name on it is the one "
                "nobody else is allowed to borrow. It carries the gold stripes and charcoal background of our Man Cave Welcome bar mat.",
                "Personalised man cave pint glass with his name",
                "Add a name – Steve’s, Dad’s, Grandad’s or a nickname – and it’s printed in gold above the words MAN CAVE. You can "
                "add the year the cave was established too, or leave it blank. Use the live preview to see the layout. " + NO_PROOF,
                ["Charcoal, cream and gold design printed in full colour with UV DTF",
                 "Pairs with our Man Cave Welcome bar mat runner and the Name Man Cave mat",
                 "Generous 20oz nonic pint for lager, ale or a pint of cider",
                 "A gift that suits birthdays, Father’s Day and Christmas stockings alike",
                 "Printed in our own workshop, not sent off to a factory"],
                PINT_SPECS,
                "Team it with the My Bar My Rules whisky tumbler for the man who likes a dram after his pint.")),
    dict(key="beer_pint", theme="beer", code="PBOCPG",
         title="Personalised Beer O’Clock Pint Glass – Retro Orange Design – Your Bar Name",
         handle="personalised-beer-oclock-pint-glass",
         tags=["beer o'clock", "beer lover gift", "funny pint glass", "garden bar", "gift for him"],
         fields=["Bar name"],
         sample=dict(name="THE SHED", est="2021"),
         matches=["bar-mat-runner-beer-oclock-bottles", "bar-mat-runner-its-beer-oclock"],
         seo_title="Personalised Beer O’Clock Pint Glass | Foxy Printing",
         seo_desc="It’s beer o’clock somewhere. A personalised pint glass with a retro orange Beer O’Clock design and your bar name, printed in full colour in the UK.",
         d=desc("A personalised Beer O’Clock pint glass is for the person who checks the time at four o’clock on a Friday and "
                "decides that’s close enough. Bright retro orange, a cheerful script ‘Beer’ and your bar name along the bottom.",
                "Personalised Beer O’Clock pint glass",
                "Type the name of your bar, shed or garden pub, and it’s printed as ‘At The Shed’, ‘At Dave’s Bar’ and so on under "
                "the Beer O’Clock lettering. The live preview shows exactly where it sits. " + NO_PROOF,
                ["Retro orange and cream design printed in full colour with UV DTF",
                 "Matches our Beer O’Clock Bottles and It’s Beer O’Clock bar mats",
                 "20oz nonic pint, roomy enough for a proper head on top",
                 "A fun Secret Santa, birthday or retirement gift for any beer fan",
                 "Your own bar name makes it a one-off"],
                PINT_SPECS,
                "Hang the matching Beer O’Clock home bar sign over the fridge and nobody will ever ask what time it is again.")),
    dict(key="union_pint", theme="union", code="PUJBPG",
         title="Personalised Union Jack Bar Pint Glass – British Flag Design – Your Bar Name & Year",
         handle="personalised-union-jack-bar-pint-glass",
         tags=["union jack", "british gift", "great britain", "pub gift", "gift for dad"],
         fields=["Bar name", "Welcome line (optional)", "Est. year (optional)"],
         sample=dict(name="JACK’S BAR", est="2021"),
         matches=["personalised-bar-mat-runner-distressed-union-jack"],
         seo_title="Personalised Union Jack Bar Pint Glass | Foxy Printing",
         seo_desc="A personalised Union Jack pint glass with your bar name and year on a bold British flag design. Full-colour print on a 20oz pint glass, made in the UK.",
         d=desc("Nothing says a proper British pub like the flag, and this personalised Union Jack bar pint glass puts your bar "
                "name on a white plaque right in the middle of it. It’s made to sit alongside our Distressed Union Jack bar mat.",
                "Personalised Union Jack bar pint glass",
                "Add your bar name and, if you like, the year it opened. ‘Welcome to’ sits above the name and can be changed or "
                "left as it is. Everything shows in the live preview while you type. " + NO_PROOF,
                ["Red, white and blue flag printed in full colour with UV DTF, edge to edge across the design",
                 "Partners our Distressed Union Jack bar mat runner",
                 "20oz nonic pint – the shape you get in a British pub",
                 "Great for jubilee parties, England match days and patriotic dads",
                 "Each glass printed to order with your own wording"],
                PINT_SPECS,
                "Complete the look with the matching Union Jack home bar sign above the optics.")),
    dict(key="best_bar_pint", theme="best_bar", code="PBBTPG",
         title="Personalised Best Bar in Town Pint Glass – Cream & Brown Design – Your Bar Name & Year",
         handle="personalised-best-bar-in-town-pint-glass",
         tags=["best bar in town", "home bar gift", "housewarming gift", "gift for him", "gift for her"],
         fields=["Bar name", "Welcome line (optional)", "Est. year"],
         sample=dict(name="THE FOX", est="2021"),
         matches=["personalised-bar-mat-runner-best-bar-in-town", "personalised-bar-mat-runner-best-bar-cream"],
         seo_title="Personalised Best Bar in Town Pint Glass | Foxy Printing",
         seo_desc="Welcome to the best bar in town. A personalised pint glass with your bar name and year on a cream and brown design, printed in full colour in the UK.",
         d=desc("Every home bar owner secretly believes theirs is the best in town, and this personalised Best Bar in Town pint "
                "glass says it for them. A cream panel, a handwritten-style ‘Welcome to the’ and your bar name on a brown plaque.",
                "Personalised Best Bar in Town pint glass",
                "Enter your bar name and the year it opened and they’re printed together on the brown plaque, like ‘The Fox | "
                "Est. 2021’. You can swap the ‘Welcome to the’ line for your own short greeting. Preview it live before ordering. "
                + NO_PROOF,
                ["Soft cream and chocolate-brown design in full colour, printed with UV DTF",
                 "Matches our Best Bar in Town and Best Bar Cream bar mat runners",
                 "20oz nonic pint glass, ideal for beer, cider or a long drink",
                 "A thoughtful housewarming, anniversary or new-garden-bar present",
                 "Made in-house for each order"],
                PINT_SPECS,
                "Hang the matching Best Bar in Town metal sign and the whole bar ties together.")),
]
for x in PINTS:
    P.append(dict(key=x["key"], kind="pint", theme=x["theme"], code=x["code"], machine="UVDTF", title=x["title"], handle=x["handle"],
                  productType="Personalised Glassware",
                  tags=BASE_TAGS + ["range-glassware", "dept-home-drinkware", "pint glass", "beer glass", "machine-uvdtf"] + x["tags"],
                  fields=x["fields"], mockup="drinkware", cat=PINT_CAT, color="Multicolor", sample=x["sample"],
                  art=dict(name="AVA’S BAR" if "BAR" in x["sample"]["name"] or x["theme"] != "man_cave" else "AVA’S", est="2021"),
                  matches=x["matches"], seo_title=x["seo_title"], seo_desc=x["seo_desc"], descriptionHtml=x["d"]))

# ======================================================================= WHISKY TUMBLERS
TUMBLERS = [
    dict(key="my_rules_tumbler", theme="my_rules", code="PMBMRWT",
         title="Personalised My Bar My Rules Whisky Tumbler – Navy & Gold Design – Your Name",
         handle="personalised-my-bar-my-rules-whisky-tumbler",
         tags=["my bar my rules", "whisky gift", "whisky glass", "man cave", "gift for dad"],
         fields=["Name", "Est. year (optional)"],
         sample=dict(name="DAVE’S BAR", est="2021"),
         matches=["bar-mat-runner-my-cave-my-rules-navy"],
         seo_title="Personalised My Bar My Rules Whisky Tumbler | Foxy Printing",
         seo_desc="My bar, my rules. A personalised whisky tumbler with a name on our navy and gold design, printed in full colour. A great gift for home bar owners.",
         d=desc("A personalised My Bar My Rules whisky tumbler is for the person who runs a tight ship behind their own bar – "
                "their measures, their music, their rules. Navy and gold, just like our My Cave My Rules bar mat, with their name on top.",
                "Personalised My Bar My Rules whisky tumbler",
                "Type a name, such as ‘Dave’s Bar’ or ‘Grandad’s’, and it sits above the big MY BAR MY RULES lettering. Add the "
                "year the bar opened if you want it along the bottom. See it in the live preview first. " + NO_PROOF,
                ["Bold navy, white and gold design printed in full colour with UV DTF",
                 "Pairs with our My Cave My Rules navy bar mat runner",
                 "A classic whisky tumbler for a dram, a rum or an old fashioned",
                 "Brilliant for 50th and 60th birthdays, Father’s Day or retirement",
                 "Each tumbler is printed to order with your own name"],
                TUMBLER_SPECS,
                "Add the My Cave My Rules metal sign and the bar has its house rules on the wall too.")),
    dict(key="vintage_tumbler", theme="vintage_black", code="PVEBWT",
         title="Personalised Vintage Established Bar Whisky Tumbler – Black & White Design – Your Bar Name",
         handle="personalised-vintage-established-whisky-tumbler",
         tags=["whisky gift", "whisky glass", "vintage bar", "established", "gift for him"],
         fields=["Bar name", "Welcome line (optional)", "Est. year"],
         sample=dict(name="JACK’S BAR", est="2020"),
         matches=["personalised-bar-mat-runner-vintage-black-established"],
         seo_title="Personalised Vintage Bar Whisky Tumbler | Foxy Printing",
         seo_desc="A personalised whisky tumbler in our vintage black Established design – add your bar name and year. Full-colour print, made to order in North Yorkshire.",
         d=desc("Sharp, simple and a little bit old-school, this personalised vintage bar whisky tumbler takes the black and white "
                "look of our Vintage Black Established bar mat and puts it on a proper short glass.",
                "Personalised vintage bar whisky tumbler with your bar name",
                "Add your bar name and the year it was established, for example ‘Jack’s Bar – Established 2020’. ‘Welcome to’ "
                "sits above the name and can be changed. The live preview shows the finished layout. " + NO_PROOF,
                ["Crisp black panel with white lettering and corner details, printed in full colour with UV DTF",
                 "Matches our Vintage Black Established bar mat runner",
                 "Classic short whisky tumbler for a neat dram or one on the rocks",
                 "A smart gift for a new home bar, a milestone birthday or the best man",
                 "Personalised to order in our own workshop"],
                TUMBLER_SPECS,
                "Order a pair so there’s always one for a guest – or add a personalised home bar pint glass for the beer drinkers.")),
    dict(key="walnut_tumbler", theme="walnut", code="PWGBWT",
         title="Personalised Walnut & Gold Bar Whisky Tumbler – Gentleman’s Bar Design – Your Bar Name",
         handle="personalised-walnut-gold-bar-whisky-tumbler",
         tags=["whisky gift", "whisky glass", "gentlemans bar", "walnut and gold", "retirement gift"],
         fields=["Bar name", "Welcome line (optional)", "Est. year"],
         sample=dict(name="GEORGE’S BAR", est="2021"),
         matches=["personalised-bar-mat-runner-walnut-gold", "personalised-bar-mat-runner-crown-copper"],
         seo_title="Personalised Walnut & Gold Whisky Tumbler | Foxy Printing",
         seo_desc="A personalised whisky tumbler with a walnut and gold gentleman’s bar design, your bar name and year. Full-colour print, made to order in North Yorkshire.",
         d=desc("Dark walnut, fine gold lines and a widely spaced bar name: this personalised walnut and gold whisky tumbler "
                "has the feel of a members’ club bar. It’s made to go with our Walnut & Gold bar mat runner.",
                "Personalised walnut and gold whisky tumbler",
                "Enter the bar name and year established, and change the small ‘Welcome to’ line if you like. The gold lettering "
                "is spaced out across the panel, so shorter names look especially smart. Check it in the live preview. " + NO_PROOF,
                ["Rich walnut-brown panel with gold detailing, printed in full colour with UV DTF",
                 "Matches our Walnut & Gold and Crown & Copper bar mat runners",
                 "Classic rocks-style whisky tumbler",
                 "A refined retirement, anniversary or 60th birthday present",
                 "Printed to order, so it carries your own bar name and year"],
                TUMBLER_SPECS,
                "Pair it with the matching walnut and gold home bar sign for a bar corner that looks properly finished.")),
    dict(key="man_cave_tumbler", theme="man_cave", code="PMCWT",
         title="Personalised Man Cave Whisky Tumbler – Gold & Charcoal Welcome Design – Your Name",
         handle="personalised-man-cave-whisky-tumbler",
         tags=["man cave", "man cave gift", "whisky gift", "whisky glass", "gift for dad"],
         fields=["Name", "Est. year (optional)"],
         sample=dict(name="DAD’S", est="2021"),
         matches=["bar-mat-runner-man-cave-welcome", "bar-mat-runner-man-cave-slate"],
         seo_title="Personalised Man Cave Whisky Tumbler | Foxy Printing",
         seo_desc="A personalised man cave whisky tumbler with his name on a charcoal and gold Welcome design. Full-colour print on a classic tumbler, made in the UK.",
         d=desc("For the evenings when a pint won’t do, a personalised man cave whisky tumbler keeps the man cave theme going "
                "into the whisky cabinet. Charcoal and gold with his name above MAN CAVE.",
                "Personalised man cave whisky tumbler with his name",
                "Type his name – Dad’s, Grandad’s, Mike’s – and add the year the man cave was established if you want it "
                "printed underneath. The live preview shows how it fits. " + NO_PROOF,
                ["Charcoal background with gold stripes and cream lettering, printed in full colour with UV DTF",
                 "Matches our Man Cave Welcome and Man Cave Slate bar mats",
                 "Classic short tumbler for whisky, brandy or a cocktail",
                 "Great for Father’s Day, birthdays and Christmas",
                 "Printed in-house for each order"],
                TUMBLER_SPECS,
                "Buy it with the matching man cave pint glass and he’s covered whatever he’s drinking.")),
]
for x in TUMBLERS:
    P.append(dict(key=x["key"], kind="tumbler", theme=x["theme"], code=x["code"], machine="UVDTF", title=x["title"], handle=x["handle"],
                  productType="Personalised Glassware",
                  tags=BASE_TAGS + ["range-glassware", "dept-home-drinkware", "whisky tumbler", "machine-uvdtf"] + x["tags"],
                  fields=x["fields"], mockup="drinkware", cat=TUMBLER_CAT, color="Multicolor", sample=x["sample"],
                  art=dict(name="AVA’S" if x["theme"] == "man_cave" else "AVA’S BAR", est="2021"),
                  matches=x["matches"], seo_title=x["seo_title"], seo_desc=x["seo_desc"], descriptionHtml=x["d"]))

# ======================================================================= METAL SIGNS
P.append(dict(
    key="club_sign", kind="sign", theme="club", code="PCCBS", machine="SUB",
    title="Personalised Club Colours Bar Sign – Metal Sign with Your Club Badge & Name – 17 Team Colours",
    handle="personalised-club-colours-bar-sign",
    productType="Metal Signs",
    tags=BASE_TAGS + ["metal sign", "bar sign", "club bar sign", "team colours", "clubhouse", "football club gift",
                      "machine-sublimation", "io-football"],
    fields=["Club or team name", "Club badge upload", "Welcome line (optional)", "Est. year (optional)"],
    mockup="flat", cat=SIGN_CAT, color="Multicolor",
    sample=dict(name="YOUR CLUB NAME", est="EST. 1987"), art=dict(name="AVA’S FC", est="EST. 1987"),
    matches=["personalised-club-bar-mat-claret-and-blue", "personalised-club-bar-mat-black-and-white-stripes"],
    seo_title="Personalised Club Colours Bar Sign | Foxy Printing",
    seo_desc="A personalised metal bar sign in your club colours with your own badge and team name. 17 colourways, two sizes, printed on gloss aluminium in the UK.",
    descriptionHtml=desc(
        "A personalised club colours bar sign gives the clubhouse bar, the supporters’ room or a fan’s home bar a proper "
        "welcome. Choose your team colours, upload the badge and add the club name, and it’s printed on gloss white aluminium.",
        "Personalised club colours bar sign with your badge and club name",
        "Pick one of 17 colourways and a size: the long 12 x 5in panoramic shows your badge at both ends with the club name "
        "in the middle, and the taller 8 x 10in puts the badge at the top. Change the ‘Welcome to’ line or add the year the "
        "club was formed if you like. The live preview shows your details. " + NO_PROOF + " Please only upload badges your "
        "club has the right to use.",
        ["Printed by dye-sublimation on 1.15mm gloss white aluminium, so colours look rich and the print won’t peel",
         "The same 17 team colours as our club bar mats, coasters and pint glasses",
         "Two sizes: 12 x 5in panoramic for over the bar, or 8 x 10in for a wall or shelf",
         "Your own badge, so it works for football, rugby, cricket, darts or bowls clubs",
         "A great end-of-season gift for the clubhouse or a long-serving volunteer"],
        SIGN_SPECS,
        "Add a club colours bar mat and a set of coasters, and the bar looks like it belongs to the club.")))

SIGNS = [
    dict(key="rustic_sign", theme="rustic", code="PREHBS",
         title="Personalised Rustic Established Home Bar Sign – Metal Sign with Your Bar Name & Year",
         handle="personalised-rustic-established-home-bar-sign",
         tags=["home bar sign", "established sign", "rustic bar", "shed bar", "gift for dad"],
         fields=["Bar name", "Welcome line (optional)", "Est. year"],
         sample=dict(name="JACK’S BAR", est="2021"),
         matches=["personalised-bar-mat-runner-rustic-established", "personalised-bar-mat-runner-vintage-wood-established"],
         seo_title="Personalised Rustic Home Bar Sign | Foxy Printing",
         seo_desc="A personalised rustic home bar sign with your bar name and year established, printed on gloss aluminium. Two sizes, made to order in North Yorkshire.",
         d=desc("A personalised rustic home bar sign tells everyone who walks in that this is a proper bar with a proper name. "
                "Warm wood-look planks, a double gold frame and ‘Established’ along the bottom, to match our Rustic Established bar mat.",
                "Personalised rustic home bar sign with your bar name",
                "Type your bar name and the year it opened, then choose the long 12 x 5in panoramic or the taller 8 x 10in. You "
                "can change the ‘Welcome to’ line too. The live preview shows the layout as you type. " + NO_PROOF,
                ["Wood-look design with gold detailing, dye-sublimated onto 1.15mm gloss white aluminium",
                 "Matches our Rustic Established and Vintage Wood bar mat runners and the rustic home bar pint glass",
                 "Panoramic size fits neatly above the optics or the bar back",
                 "Colours are sealed into the metal surface, so there’s no sticker to peel",
                 "A housewarming or Father’s Day gift that gets pride of place"],
                SIGN_SPECS,
                "Finish the set with the matching rustic home bar pint glass for the landlord.")),
    dict(key="my_cave_sign", theme="my_cave_rules", code="PMCMRS",
         title="Personalised My Cave My Rules Metal Sign – Navy & Gold Home Bar Sign – Your Name",
         handle="personalised-my-cave-my-rules-metal-sign",
         tags=["my cave my rules", "man cave sign", "man cave gift", "home bar sign", "gift for him"],
         fields=["Name", "Est. year (optional)"],
         sample=dict(name="DAVE’S BAR", est="2021"),
         matches=["bar-mat-runner-my-cave-my-rules-navy"],
         seo_title="Personalised My Cave My Rules Metal Sign | Foxy Printing",
         seo_desc="My cave, my rules. A personalised navy and gold metal sign with a name and year for the man cave or home bar. Two sizes, printed on gloss aluminium.",
         d=desc("Put the house rules where everyone can see them. This personalised My Cave My Rules metal sign is navy and gold, "
                "with a name across the top, and it matches our My Cave My Rules bar mat runner.",
                "Personalised My Cave My Rules metal sign",
                "Add a name – ‘Dave’s Bar’, ‘Dad’s Shed’, ‘Grandad’s’ – and, if you like, the year the cave was established. "
                "Choose the 12 x 5in panoramic or the 8 x 10in. Watch it build in the live preview. " + NO_PROOF,
                ["Navy, white and gold design dye-sublimated onto 1.15mm gloss white aluminium",
                 "Matches our My Cave My Rules bar mat and the My Bar My Rules whisky tumbler",
                 "Two sizes to suit a door, a wall or the space above the bar",
                 "Bright, glossy finish that brings the gold detail to life",
                 "A man cave gift for birthdays, Christmas and Father’s Day"],
                SIGN_SPECS,
                "Pair it with the My Bar My Rules whisky tumbler for a gift set that says it all.")),
    dict(key="beer_sign", theme="beer", code="PBOCHBS",
         title="Personalised Beer O’Clock Home Bar Sign – Retro Orange Metal Sign – Your Bar Name",
         handle="personalised-beer-oclock-home-bar-sign",
         tags=["beer o'clock", "home bar sign", "garden bar sign", "funny bar sign", "gift for him"],
         fields=["Bar name"],
         sample=dict(name="THE SHED", est="2021"),
         matches=["bar-mat-runner-beer-oclock-bottles", "bar-mat-runner-its-beer-oclock"],
         seo_title="Personalised Beer O’Clock Home Bar Sign | Foxy Printing",
         seo_desc="A personalised Beer O’Clock home bar sign in retro orange with your bar name, printed on gloss aluminium. Two sizes, made to order in the UK.",
         d=desc("Some bars have a clock; this one just has a personalised Beer O’Clock home bar sign. Retro orange with cream "
                "lettering, a big script ‘Beer’ and your bar name along the bottom.",
                "Personalised Beer O’Clock home bar sign",
                "Type the name of your bar, shed or garden pub and it’s printed as ‘At The Shed’ under the Beer O’Clock lettering. "
                "Choose 12 x 5in panoramic or 8 x 10in. The live preview shows your wording on the sign. " + NO_PROOF,
                ["Cheerful orange and cream design dye-sublimated onto 1.15mm gloss white aluminium",
                 "Matches our Beer O’Clock Bottles and It’s Beer O’Clock bar mats and the Beer O’Clock pint glass",
                 "Panoramic size suits a shelf edge or the top of the bar",
                 "Glossy metal finish that wipes over easily",
                 "A fun gift for a birthday, retirement or a new garden bar"],
                SIGN_SPECS,
                "Grab a Beer O’Clock pint glass to go with it and the joke is complete.")),
    dict(key="union_sign", theme="union", code="PUJHBS",
         title="Personalised Union Jack Home Bar Sign – British Flag Metal Sign – Your Bar Name & Year",
         handle="personalised-union-jack-home-bar-sign",
         tags=["union jack", "home bar sign", "british gift", "pub sign", "gift for dad"],
         fields=["Bar name", "Welcome line (optional)", "Est. year (optional)"],
         sample=dict(name="JACK’S BAR", est="2021"),
         matches=["personalised-bar-mat-runner-distressed-union-jack"],
         seo_title="Personalised Union Jack Home Bar Sign | Foxy Printing",
         seo_desc="A personalised Union Jack home bar sign with your bar name and year on the British flag, printed on gloss aluminium. Two sizes, made in the UK.",
         d=desc("A personalised Union Jack home bar sign gives your bar a proper British welcome. The flag fills the sign from edge "
                "to edge, with your bar name on a white plaque in the centre, just like our Distressed Union Jack bar mat.",
                "Personalised Union Jack home bar sign with your bar name",
                "Enter your bar name and, if you like, the year it opened and your own ‘Welcome to’ line. Pick the 12 x 5in "
                "panoramic or the 8 x 10in. Everything shows in the live preview. " + NO_PROOF,
                ["Red, white and blue flag dye-sublimated onto 1.15mm gloss white aluminium",
                 "Matches our Distressed Union Jack bar mat and the Union Jack bar pint glass",
                 "Bold enough to read from across the room",
                 "Perfect for England match days, jubilee parties and patriotic dads",
                 "Each sign made to order with your own wording"],
                SIGN_SPECS,
                "Add the Union Jack bar pint glass and the British-themed bar is sorted.")),
    dict(key="best_bar_sign", theme="best_bar", code="PBBTMS",
         title="Personalised Best Bar in Town Metal Sign – Cream & Brown Home Bar Sign – Your Bar Name & Year",
         handle="personalised-best-bar-in-town-metal-sign",
         tags=["best bar in town", "home bar sign", "housewarming gift", "gift for him", "gift for her"],
         fields=["Bar name", "Welcome line (optional)", "Est. year"],
         sample=dict(name="THE FOX", est="2021"),
         matches=["personalised-bar-mat-runner-best-bar-in-town", "personalised-bar-mat-runner-best-bar-cream"],
         seo_title="Personalised Best Bar in Town Sign | Foxy Printing",
         seo_desc="Welcome to the best bar in town. A personalised metal sign with your bar name and year in cream and brown, printed on gloss aluminium in the UK.",
         d=desc("Make it official: your bar is the best in town. This personalised Best Bar in Town metal sign has a soft cream "
                "background, a handwritten-style ‘Welcome to the’ and your bar name and year on a brown plaque.",
                "Personalised Best Bar in Town metal sign",
                "Add your bar name and year established and they’re printed together on the plaque, for example ‘The Fox | Est. "
                "2021’. Change the greeting line if you’d like your own. Choose 12 x 5in panoramic or 8 x 10in, and check the "
                "live preview. " + NO_PROOF,
                ["Cream and chocolate-brown design dye-sublimated onto 1.15mm gloss white aluminium",
                 "Matches our Best Bar in Town and Best Bar Cream bar mats and the Best Bar in Town pint glass",
                 "A softer look that suits kitchens, garden rooms and conservatory bars",
                 "Smooth gloss finish with crisp, sharp text",
                 "A housewarming or anniversary gift with a smile built in"],
                SIGN_SPECS,
                "Pick up the matching Best Bar in Town pint glass for the first round.")),
    dict(key="walnut_sign", theme="walnut", code="PWGHBS",
         title="Personalised Walnut & Gold Home Bar Sign – Gentleman’s Bar Metal Sign – Your Bar Name & Year",
         handle="personalised-walnut-gold-home-bar-sign",
         tags=["home bar sign", "gentlemans bar", "walnut and gold", "gift for him", "retirement gift"],
         fields=["Bar name", "Welcome line (optional)", "Est. year"],
         sample=dict(name="GEORGE’S BAR", est="2021"),
         matches=["personalised-bar-mat-runner-walnut-gold", "personalised-bar-mat-runner-crown-copper"],
         seo_title="Personalised Walnut & Gold Home Bar Sign | Foxy Printing",
         seo_desc="A personalised walnut and gold home bar sign with your bar name and year, printed on gloss aluminium. Two sizes, made to order in North Yorkshire.",
         d=desc("Dark walnut, gold chevrons and a widely spaced bar name give this personalised walnut and gold home bar sign the "
                "look of a members’ club. It matches our Walnut & Gold bar mat runner and whisky tumbler.",
                "Personalised walnut and gold home bar sign",
                "Enter your bar name and year established, and change the ‘Welcome to’ line if you like. Choose the 12 x 5in "
                "panoramic or the 8 x 10in. The live preview shows how your name sits on the sign. " + NO_PROOF,
                ["Walnut-brown and gold design dye-sublimated onto 1.15mm gloss white aluminium",
                 "Matches our Walnut & Gold and Crown & Copper bar mats and the walnut and gold whisky tumbler",
                 "Understated style that suits a study bar, drinks cabinet or snug",
                 "Glossy finish that makes the gold detail glow",
                 "A distinguished retirement or 60th birthday present"],
                SIGN_SPECS,
                "Pair it with the walnut and gold whisky tumbler for a gift set with real presence.")),
]
for x in SIGNS:
    P.append(dict(key=x["key"], kind="sign", theme=x["theme"], code=x["code"], machine="SUB", title=x["title"], handle=x["handle"],
                  productType="Metal Signs",
                  tags=BASE_TAGS + ["metal sign", "bar sign", "pub sign", "machine-sublimation"] + x["tags"],
                  fields=x["fields"], mockup="flat", cat=SIGN_CAT, color="Multicolor", sample=x["sample"],
                  art=dict(name="AVA’S BAR", est="2021"),
                  matches=x["matches"], seo_title=x["seo_title"], seo_desc=x["seo_desc"], descriptionHtml=x["d"]))
