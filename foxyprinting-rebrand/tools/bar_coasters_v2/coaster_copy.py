"""Copy, fields and tags for the 20 older bar / man cave coasters (v2, 8 Oct 2026).

Facts used (plan/product-facts.md "Home bar" sheet + the live coaster listings): square coaster 90 x 90 mm,
cork-backed MDF (hardboard) with a bright glossy top, dye-sublimation printed, dishwasher safe (owner, 8 Oct 2026),
sold singly. Delivery: made to order, postage shown at checkout (no dispatch promise). No proofs.
"""
WHOSE = "Whose cave? e.g. Dave’s (optional)"
NO_PROOF = "We print exactly what you enter, so please check names and spelling in the live preview before you order."

SPECS = """<h3>Size &amp; details</h3>
<ul>
<li>Square drinks coaster, 90 x 90 mm</li>
<li>Cork-backed MDF with a bright glossy top</li>
<li>Printed in full colour by dye-sublimation</li>
<li>Dishwasher safe</li>
<li>Sold as a single coaster</li>
</ul>"""

DELIVERY = ("<h3>Delivery</h3>\n<p>Every coaster is made to order in our North Yorkshire workshop. Postage options and costs "
            "are shown at checkout, and if you have a date to hit, give us a ring on 01439 771468 before you order.</p>")

JD_DISCLAIMER = ("<h3>Please note</h3>\n<p class=\"disclaimer\">This is an unofficial product made by Foxy Printing. It is not made, "
                 "endorsed or approved by Jack Daniel’s. Jack Daniel’s is a trademark of its owner and is used only to describe "
                 "the design theme.</p>")


def ul(items):
    return "<ul>\n" + "\n".join(f"<li>{i}</li>" for i in items) + "\n</ul>"


def desc(opening, h2, how, love, close, extra=""):
    return (f"<p>{opening}</p>\n<h2>{h2}</h2>\n<p>{how} {NO_PROOF}</p>\n<h3>Why you’ll love it</h3>\n{ul(love)}\n{SPECS}\n"
            f"{DELIVERY}\n<p>{close}</p>" + (f"\n{extra}" if extra else ""))


BAR, CAVE = "bar", "cave"

# key, handle, group, matching mat handle, mat name, title, fields, colour words, seo title, seo desc, description, alt
P = [
    dict(key="x21", handle="personalized-welcome-name-drinks-coaster-2", group=BAR, mat="personalised-bar-mat-runner-blush-script",
         title="Personalised Welcome Name Coaster – Blush Script Design – 90mm Drinks Coaster for a Home Bar",
         fields=["Name", "Welcome line (optional)"],
         seo_title="Personalised Welcome Name Coaster | Foxy Printing",
         seo_desc="A personalised welcome name coaster in soft blush pink with your name in flowing script. 90 x 90 mm, glossy, dishwasher safe and made to order in the UK.",
         alt="Personalised welcome name coaster in blush pink with a name in gold script between two Welcome lines",
         description=desc(
             "This personalised welcome name coaster is a gentle, pretty way to put your name on the bar, the bedside table or a "
             "friend’s new kitchen. The blush pink background, fine white frame and gold script name feel more boutique hotel than pub.",
             "A personalised welcome name coaster in blush and gold",
             "Type the name you want in the script panel, and if you fancy something other than ‘Welcome’ above and below it, add your "
             "own short line; leave it blank and we keep Welcome. The live preview shows your wording on the coaster as you type.",
             ["Soft blush tones and a gold script name that suit a bedroom, a dressing table or a gin corner",
              "Lovely as a housewarming gift, a bridesmaid thank-you or a little treat for Mum",
              "Thin white frame and scrollwork so the name always sits neatly in the middle",
              "Dye-sublimation print, so the colours sit in the glossy surface rather than on top of it",
              "Matches our Blush Script bar mat runner if you want a set"],
             "Pair it with the matching Blush Script bar mat, or order one for each guest as a name card that doubles as a keepsake.")),
    dict(key="x22", handle="personalized-your-bar-name-drinks-coaster", group=BAR, mat="personalised-bar-mat-runner-emerald-flourish",
         title="Personalised Bar Coaster – Emerald Flourish Design – Your Name & Est. Year – 90mm Drinks Coaster",
         fields=["Your name", "Est. year (optional)"],
         seo_title="Personalised Emerald Bar Coaster | Foxy Printing",
         seo_desc="A personalised bar coaster in emerald green with gold flourishes, your name in script and the year your bar opened. Glossy and dishwasher safe.",
         alt="Personalised bar coaster in emerald green with gold flourishes and a name, Bar and est. year in gold script",
         description=desc(
             "Give your home bar a proper sign of ownership with this personalised bar coaster. Deep emerald green, swirling gold and "
             "mint flourishes and your name written in script above the word Bar make it feel like a smart cocktail lounge.",
             "Personalised bar coaster with your name and year",
             "Add your name the way you’d like it to read (for example ‘Dave’s’ or ‘The Smiths’) and, if you like, the year the bar "
             "opened. Leave the year empty and we simply leave that line off. You’ll see it all in the live preview first.",
             ["Rich emerald and gold colours that look great next to dark wood and brass",
              "Script lettering that turns a first name into a bar name in seconds",
              "Optional ‘est.’ year, perfect for a bar built during lockdown or a new garden room",
              "Bright glossy top with a cork back to protect the counter",
              "Goes with our Emerald Flourish bar mat runner"],
             "Buy a few so every stool has one, and add the Emerald Flourish bar mat for the full look.")),
    dict(key="x23", handle="personalized-bar-name-crown-drinks-coaster", group=BAR, mat="personalised-bar-mat-runner-crown-copper",
         title="Personalised Bar Name Coaster – Crown & Copper Design – 90mm Drinks Coaster for a Home Pub",
         fields=["Bar name – line 1", "Bar name – line 2 (optional)"],
         seo_title="Personalised Crown Bar Name Coaster | Foxy Printing",
         seo_desc="A personalised bar name coaster with a copper crown and wide spaced lettering on slate blue. Your bar name on two lines, glossy and dishwasher safe.",
         alt="Personalised bar name coaster in slate blue with a copper crown and a bar name in wide copper capitals",
         description=desc(
             "Crown your home pub with this personalised bar name coaster. A copper crown and fine scrollwork sit above your bar name, "
             "spaced out in elegant capitals on a slate blue panel with a warm copper border.",
             "A personalised bar name coaster fit for the King’s Head",
             "Type your bar name over two lines: the first box is the top line and the second is optional, so a short name can sit "
             "on one line. Think ‘The Crown’, ‘Royal Oak’ or ‘Smith’s Bar’. The live preview shows how it lines up.",
             ["Classic pub-sign styling with a regal crown, ideal for a traditional English bar",
              "Two lines of text so longer pub names still look balanced",
              "Copper and slate colours that sit nicely with brick, wood and leather",
              "Glossy, wipe-clean top and a cork back that won’t scratch the bar",
              "Designed alongside our Crown & Copper bar mat runner"],
             "Pair it with the Crown & Copper bar mat for a matching set, or give a stack of them to the landlord of your local.")),
    dict(key="x24", handle="personalized-bar-name-purple-drinks-coaster", group=BAR, mat="personalised-bar-mat-runner-plum-filigree",
         title="Personalised Bar Name Coaster – Plum Filigree Design – 90mm Drinks Coaster for a Gin Bar",
         fields=["Bar name – line 1", "Bar name – line 2 (optional)"],
         seo_title="Personalised Plum Bar Name Coaster | Foxy Printing",
         seo_desc="A personalised plum bar name coaster with lilac filigree and your bar name in spaced capitals. Lovely for a gin bar. Glossy and dishwasher safe.",
         alt="Personalised bar name coaster in deep plum with lilac filigree and a bar name in pale lilac capitals",
         description=desc(
             "A personalised bar name coaster in deep plum, made for gin lovers and anyone who likes their bar with a bit of glamour. "
             "Delicate lilac filigree frames your bar name, set in airy capitals with a magenta edge down each side.",
             "Personalised plum bar name coaster with filigree",
             "Enter your bar name across two lines: line one is required and line two is optional. ‘Gin O’Clock’, ‘The Plum Bar’ or "
             "simply your surname all work well. Check the spacing in the live preview before you add it to your basket.",
             ["A rich plum and lilac colourway that makes a change from black and gold",
              "Ideal for a gin bar, a garden room or a she shed",
              "Filigree flourishes above and below so short and long names both look finished",
              "Glossy dye-sublimation print that copes with condensation from a cold glass",
              "Matches our Plum Filigree bar mat runner"],
             "Add a Plum Filigree bar mat and a set of coasters for the gin fan who has everything.")),
    dict(key="x25", handle="personalized-welcome-bar-name-drinks-coaster", group=BAR, mat="personalised-bar-mat-runner-teal-welcome",
         title="Personalised Welcome Bar Coaster – Teal Welcome Design – Your Bar Name – 90mm Drinks Coaster",
         fields=["Bar name", "Welcome line (optional)"],
         seo_title="Personalised Teal Welcome Bar Coaster | Foxy Printing",
         seo_desc="A personalised welcome bar coaster in deep teal with a vintage tile border and your bar name in white. 90 x 90 mm, glossy and dishwasher safe.",
         alt="Personalised welcome bar coaster in deep teal with a tile border, your bar name in white and Welcome above and below",
         description=desc(
             "Say hello to every guest with this personalised welcome bar coaster. A deep teal background, a vintage tile-style border "
             "and your bar name in crisp white capitals give it a smart, slightly Victorian pub feel.",
             "A personalised welcome bar coaster in teal",
             "Type your bar name on one line, for example ‘The Snug’ or ‘Jones’s Bar’. The small line above and below says Welcome; "
             "you can swap it for something else, such as ‘Cheers’ or ‘Est. 2024’, or leave the box blank to keep Welcome.",
             ["Deep teal and stone colours inspired by old pub tiles",
              "One-line bar name in big white capitals, easy to read across the room",
              "Welcome lines top and bottom that you can change if you like",
              "Bright glossy top, cork back, and dishwasher safe for easy cleaning",
              "Made to match our Teal Welcome bar mat runner"],
             "Pop the Teal Welcome bar mat on the counter and a coaster at every seat, and the bar is ready for visitors.")),
    dict(key="x26", handle="personalized-bar-name-drinks-coaster", group=BAR, mat="personalised-bar-mat-runner-walnut-gold",
         title="Personalised Bar Name Coaster – Walnut & Gold Design – 90mm Drinks Coaster for a Home Bar",
         fields=["Bar name – line 1", "Bar name – line 2 (optional)"],
         seo_title="Personalised Walnut Bar Name Coaster | Foxy Printing",
         seo_desc="A personalised bar name coaster with a dark walnut wood look and gold corner scrolls. Your bar name on two lines, glossy and dishwasher safe.",
         alt="Personalised bar name coaster with a dark walnut wood look, gold corner scrolls and a bar name in gold capitals",
         description=desc(
             "This personalised bar name coaster has the look of dark walnut panelling with ornate gold corners, the kind of finish "
             "you’d find in an old gentlemen’s club. Your bar name sits in the middle in tall, widely spaced gold capitals.",
             "Personalised walnut and gold bar name coaster",
             "Fill in line one with the first part of your bar name and, if you need it, line two with the rest. Short names look "
             "great on a single line too. The live preview shows the gold lettering on the wood before you order.",
             ["Rich wood-look print with gold scrolls, without the cost of a real wooden coaster",
              "Two lines for your bar name, so ‘The Red Lion’ fits as nicely as ‘Ted’s’",
              "Suits a classic home bar, a study or a whisky corner",
              "Glossy top that wipes clean, and dishwasher safe",
              "Part of our Walnut & Gold range with a matching bar mat, glass and sign"],
             "Complete the set with the Walnut & Gold bar mat runner and a personalised whisky tumbler.")),
    dict(key="x27", handle="personalized-bar-name-establish-date-drinks-coaster", group=BAR, mat="personalised-bar-mat-runner-olive-oval",
         title="Personalised Bar Name Established Coaster – Olive Oval Design – Name & Year – 90mm Drinks Coaster",
         fields=["Bar name – line 1", "Bar name – line 2 (optional)", "Est. year (optional)", "Welcome line (optional)"],
         seo_title="Personalised Established Bar Coaster | Foxy Printing",
         seo_desc="A personalised established bar coaster in olive and amber with your bar name and the year it opened. 90 x 90 mm, glossy and dishwasher safe.",
         alt="Personalised established bar coaster in olive green and amber with a bar name and est. year in a circle",
         description=desc(
             "A personalised established bar coaster with a bold retro feel: a big olive circle on an amber square, with your bar name "
             "in large capitals and the year it opened underneath. It’s a fun way to make a new home bar feel like it’s been there for years.",
             "Your bar name and year on a personalised established bar coaster",
             "Add your bar name over one or two lines, then the year your bar opened (or the year you married, moved in or retired). "
             "The small ‘Welcome’ line at the top can be changed too. Leave any optional box blank and we tidy the design for you.",
             ["Retro olive and amber colours that stand out on a dark counter",
              "Up to four boxes, so you can add a name, a year and your own welcome line",
              "Great for a new garden bar, a shed pub or a 40th birthday gift",
              "Dye-sublimation print with a bright glossy finish, dishwasher safe",
              "Matches our Olive Oval bar mat runner"],
             "Order one with the year they opened the bar and pair it with the Olive Oval bar mat for a proper housewarming present.")),
    dict(key="x28", handle="personalized-bar-name-establish-date-drinks-coaster-2", group=BAR, mat="personalised-bar-mat-runner-rustic-established",
         title="Personalised Rustic Established Bar Coaster – Wood Effect – Your Bar Name & Year – 90mm Drinks Coaster",
         fields=["Bar name – line 1", "Bar name – line 2 (optional)", "Est. year (optional)"],
         seo_title="Personalised Rustic Established Coaster | Foxy Printing",
         seo_desc="A personalised rustic established coaster with a warm wood effect, your bar name and the year it opened in gold. Glossy and dishwasher safe.",
         alt="Personalised rustic established coaster with a warm wood effect, Welcome To, a bar name and Established year in gold",
         description=desc(
             "This personalised rustic established coaster looks like a slice of old oak with a gold-edged frame, reading ‘Welcome to’ "
             "your bar and ‘Established’ with the year. It’s made for log-cabin bars, garden pubs and anyone who loves a country inn.",
             "A personalised rustic established coaster for your bar",
             "Type the bar name over one or two lines and add the year it was established. If you’d rather not have a year, leave that "
             "box empty and we leave off the Established line. See the result in the live preview straight away.",
             ["Warm wood-effect print with a bold blue edge, so it looks rustic without being dull",
              "Your bar name in tall gold capitals, framed by ‘Welcome to’ and ‘Established’",
              "A thoughtful gift for a new garden bar, a pub shed or a retirement project",
              "Bright glossy top that’s dishwasher safe and easy to keep clean",
              "Matches our Rustic Established bar mat, pint glass and home bar sign"],
             "Build the full Rustic Established set with the matching bar mat, pint glass and metal home bar sign.")),
    dict(key="x29", handle="personalized-bar-name-billiards-drinks-coaster", group=BAR, mat="personalised-bar-mat-runner-rainbow-bubbles",
         title="Personalised Pool Ball Bar Coaster – Rainbow Bubbles Design – Letters on Pool Balls – 90mm Drinks Coaster",
         fields=["Top row letters (up to 3)", "Bottom row letters (up to 4)", "Welcome line (optional)"],
         seo_title="Personalised Pool Ball Bar Coaster | Foxy Printing",
         seo_desc="A personalised pool ball bar coaster with your letters on seven coloured balls. Great for a games room bar. 90 x 90 mm, glossy and dishwasher safe.",
         alt="Personalised pool ball bar coaster with letters on seven coloured balls on an olive background with Welcome lines",
         description=desc(
             "Made for games rooms and pool tables, this personalised pool ball bar coaster spells out your word on seven bright "
             "pool-style balls on an olive baize-green background, with ‘Welcome’ above and below.",
             "Personalised pool ball bar coaster with your letters",
             "There are three balls on the top row and four on the bottom, one letter each. Try ‘DAD’S / BAR!’, ‘THE / SNUG’, "
             "‘POOL / ROOM’ or initials and a year. You can also change the Welcome line. The live preview shows each letter in its ball.",
             ["A playful games-room design that suits pool, snooker and darts fans",
              "Seven coloured balls with one letter each, so short names really pop",
              "Bold amber Welcome lines that you can swap for your own words",
              "Glossy, dishwasher-safe top with a cork back for the bar or the side table",
              "Pairs with our Rainbow Bubbles bar mat runner"],
             "Pop one beside the pool table and add the Rainbow Bubbles bar mat to the bar for a matching games room.")),
    dict(key="x30", handle="personalized-bar-name-enjoy-your-time-drinks-coaster", group=BAR, mat="personalised-bar-mat-runner-ruby-script",
         title="Personalised Bar Name Coaster – Ruby Script Design – Enjoy Your Time – 90mm Drinks Coaster",
         fields=["Bar name"],
         seo_title="Personalised Ruby Script Bar Coaster | Foxy Printing",
         seo_desc="A personalised ruby script bar coaster with your bar name in flowing red lettering and an Enjoy Your Time line. Glossy, dishwasher safe, made in the UK.",
         alt="Personalised ruby script bar coaster in deep red with a bar name in flowing script and Enjoy Your Time below",
         description=desc(
             "Deep ruby, a red ornamental crest and your bar name in sweeping script make this personalised ruby script bar coaster "
             "feel like a little piece of a wine bar. The small ‘Enjoy your time’ line underneath says the rest.",
             "Personalised ruby script bar coaster with your bar name",
             "Just type your bar name, for example ‘Sam’s Bar’, ‘The Wine Cellar’ or ‘Casa Rossi’. We set it in flowing red script "
             "in the middle of the coaster. Watch it appear in the live preview as you type.",
             ["Rich ruby reds that suit a wine rack, a cocktail cabinet or a dinner party table",
              "Flowing script lettering for a softer, more elegant bar name",
              "‘Enjoy your time’ line and ornamental crest already in the design",
              "Bright glossy top and cork back, dishwasher safe",
              "Matches our Ruby Script bar mat runner"],
             "Lay the Ruby Script bar mat along the counter and give each guest a coaster with the bar’s name on it.")),
    # ------------------------------------------------------------------- man cave
    dict(key="o01", handle="personalized-man-cave-drinks-coaster", group=CAVE, mat="bar-mat-runner-man-cave-slate",
         title="Personalised Man Cave Coaster – Slate & Gold Design – Your Name & Est. Year – 90mm Drinks Coaster",
         fields=[WHOSE, "Est. year (optional)"],
         seo_title="Personalised Man Cave Coaster | Foxy Printing",
         seo_desc="A personalised man cave coaster in slate grey and gold. Add a name to make it Dave’s Cave, plus the year. 90 x 90 mm, glossy and dishwasher safe.",
         alt="Personalised man cave coaster in slate grey with gold stripes and a name’s Cave in white capitals",
         description=desc(
             "This personalised man cave coaster turns the spare room, garage or shed into somebody’s official territory. Dark slate, "
             "gold hazard-style stripes in the corners and big white capitals with a gold shadow give it a bold, industrial look.",
             "A personalised man cave coaster with a name and year",
             "Add a name with an apostrophe s, such as ‘Dave’s’ or ‘Grandad’s’, and the big lettering reads DAVE’S CAVE. Leave it empty "
             "to keep MAN CAVE. The bottom line can show the year it was set up; leave that blank and we keep ‘Welcome’.",
             ["Slate and gold styling that suits garages, sheds and gaming dens",
              "Turns MAN CAVE into your own name’s cave in big white capitals",
              "Optional year line for a ‘since’ date or a special birthday",
              "Glossy, dishwasher-safe top with a cork back",
              "Matches our Man Cave Slate bar mat runner"],
             "Add the Man Cave Slate bar mat and a personalised pint glass and that’s Father’s Day sorted.")),
    dict(key="o02", handle="personalized-come-in-bud-drinks-coaster", group=CAVE, mat="bar-mat-runner-well-come-in-bud",
         title="Personalised Well Come In Bud Coaster – Funny Man Cave Drinks Coaster – Your Name – 90mm",
         fields=["Name to replace ‘Bud’ (optional)"],
         seo_title="Personalised Well Come In Bud Coaster | Foxy Printing",
         seo_desc="A funny personalised Well Come In Bud coaster for the man cave. Swap Bud for a name, or keep the original. 90 x 90 mm, glossy and dishwasher safe.",
         alt="Personalised Well Come In Bud coaster in dark brown with orange scrolls, beer glasses and white capitals",
         description=desc(
             "‘Well, come in bud!’ is the warmest welcome a man cave can give, and this personalised Well Come In Bud coaster makes "
             "the joke with dark chocolate brown, amber scrolls and frothy pint glasses in each corner.",
             "Personalised Well Come In Bud coaster for the man cave",
             "Keep the classic ‘Bud!’ or type a name to replace it, so it reads ‘Well, come in Dave!’ or ‘Well, come in Grandad!’. "
             "We add the exclamation mark for you. Check it in the live preview first.",
             ["A cheeky pun that gets a smile from every visitor",
              "Swap ‘Bud’ for a name to make it a one-off gift",
              "Warm brown and amber colours that suit wood panelling and leather sofas",
              "Bright glossy finish, cork back and dishwasher safe",
              "Matches our Well Come In Bud bar mat runner"],
             "Pair it with the matching Well Come In Bud bar mat for a man cave gift that keeps the joke going.")),
    dict(key="o03", handle="personalized-my-cave-my-rules-drinks-coaster", group=CAVE, mat="bar-mat-runner-my-cave-my-rules-navy",
         title="Personalised My Cave My Rules Coaster – Navy & Gold Design – Your Name – 90mm Man Cave Drinks Coaster",
         fields=[WHOSE],
         seo_title="Personalised My Cave My Rules Coaster | Foxy Printing",
         seo_desc="A personalised My Cave My Rules coaster in navy and gold. Add a name to make it Dave’s Cave, My Rules. 90 x 90 mm, glossy and dishwasher safe.",
         alt="Personalised My Cave My Rules coaster in navy with gold scrolls, white and yellow capitals and small crowns",
         description=desc(
             "Lay down the law with this personalised My Cave My Rules coaster. Royal navy, ornate gold scrollwork with little crowns "
             "and big bold capitals in white and yellow make the house rules very clear.",
             "Personalised My Cave My Rules coaster in navy and gold",
             "Leave the box empty for the classic MY CAVE / MY RULES, or type a name with an apostrophe s, such as ‘Dave’s’, and the "
             "top line becomes DAVE’S CAVE with MY RULES underneath. The live preview shows the exact wording.",
             ["Regal navy and gold that looks smart in a games room or garage bar",
              "Bold slab capitals that are easy to read from across the room",
              "Optional name so the cave is clearly his (or hers)",
              "Glossy, dishwasher-safe top with a protective cork back",
              "Matches our My Cave My Rules Navy bar mat runner"],
             "Make it a set with the My Cave My Rules Navy bar mat, or buy a stack for the lads’ poker night.")),
    dict(key="o04", handle="personalized-initial-drinks-coaster", group=CAVE, mat="personalised-bar-mat-runner-name-medallions",
         title="Personalised Initial Coaster – Midnight & Red Monogram Design – 90mm Drinks Coaster",
         fields=["Initial"],
         seo_title="Personalised Initial Coaster | Foxy Printing",
         seo_desc="A personalised initial coaster with your letter in an elegant monogram frame on midnight blue and red. 90 x 90 mm, glossy and dishwasher safe.",
         alt="Personalised initial coaster with a large white serif letter inside a red monogram frame on midnight blue",
         description=desc(
             "Simple, smart and a bit luxurious, this personalised initial coaster puts one big serif letter in the centre of a red "
             "monogram frame on a midnight blue background that fades to deep red at the edges.",
             "A personalised initial coaster with a monogram frame",
             "Type the initial you want in the box, usually a first name or surname letter. One capital looks best, but two letters "
             "will also fit. The live preview shows your letter in the frame before you buy.",
             ["Elegant monogram styling that suits a study, a hallway or a bedside table",
              "Easy to buy as a set, with a different initial for each person in the family",
              "Red and midnight blue colours that look rich next to dark wood",
              "Glossy, dishwasher-safe top with a cork back",
              "Goes with our Name Medallions bar mat runner"],
             "Order a set with each family member’s initial, or pair one with a personalised whisky tumbler for a smart gift.")),
    dict(key="o05", handle="personalized-my-cave-my-rules-drinks-coaster-1", group=CAVE, mat="bar-mat-runner-man-cave-take-a-sip",
         title="Personalised Man Cave Take a Sip Coaster – Whisky Glass Design – Your Name – 90mm Drinks Coaster",
         fields=[WHOSE],
         seo_title="Personalised Man Cave Take a Sip Coaster | Foxy Printing",
         seo_desc="A personalised man cave Take a Sip coaster with splashing whisky glasses and a gold laurel. Add a name for Dave’s Cave. Glossy and dishwasher safe.",
         alt="Personalised man cave Take a Sip coaster in black with two splashing whisky glasses and a gold laurel wreath",
         description=desc(
             "Two whisky glasses clinking with a splash, a gold laurel wreath and the words ‘Take a sip and enjoy’ make this "
             "personalised man cave Take a Sip coaster the perfect spot to rest a dram at the end of the day.",
             "Personalised man cave Take a Sip coaster",
             "Leave the box blank for MAN CAVE in the laurel, or add a name with an apostrophe s, like ‘Jim’s’, and it reads JIM’S CAVE. "
             "The ‘Take a sip and enjoy’ line stays as it is. You’ll see it in the live preview first.",
             ["Whisky splash artwork that suits a spirits shelf or a home bar",
              "Gold laurel and lettering on black for a classy, after-dinner feel",
              "A name option for a gift that feels made for them",
              "Glossy, dishwasher-safe top and a cork back that protects the table",
              "Matches our Man Cave Take a Sip bar mat runner"],
             "Pair it with a personalised whisky tumbler and the Take a Sip bar mat for a whisky lover’s gift set.")),
    dict(key="o06", handle="personalized-my-cave-my-rules-2-drinks-coaster", group=CAVE, mat="bar-mat-runner-my-cave-my-rules-whiskey",
         title="Personalised My Cave My Rules Whiskey Coaster – Orange & Black Design – Your Name – 90mm Drinks Coaster",
         fields=[WHOSE],
         seo_title="Personalised Whiskey Man Cave Coaster | Foxy Printing",
         seo_desc="A personalised My Cave My Rules whiskey coaster in orange and black with a bourbon bottle trio. Add a name if you like. Glossy and dishwasher safe.",
         alt="Personalised My Cave My Rules whiskey coaster in orange and black with three bourbon bottles and orange capitals",
         description=desc(
             "Bourbon fans will love this personalised My Cave My Rules whiskey coaster. Three whiskey bottles fan out across a black "
             "stripe on bright orange, with MY CAVE at the top and MY RULES at the bottom.",
             "Personalised My Cave My Rules whiskey coaster",
             "Keep MY CAVE as it is, or type a name with an apostrophe s, such as ‘Dave’s’, so the top reads DAVE’S CAVE. The MY RULES "
             "line stays at the bottom. Check the wording in the live preview before you order.",
             ["Bold orange and black colours that pop on a dark bar top",
              "Whiskey bottle artwork for the spirits fan in your life",
              "Optional name so it becomes their cave, their rules",
              "Glossy, dishwasher-safe top with a cork back",
              "Matches our My Cave My Rules Whiskey bar mat runner"],
             "Pair it with the matching whiskey bar mat and a personalised whisky tumbler for birthdays and Father’s Day.",
             extra=JD_DISCLAIMER)),
    dict(key="o07", handle="personalized-your-name-drinks-coaster", group=CAVE, mat="personalised-bar-mat-runner-burgundy-welcome",
         title="Personalised Welcome Name Coaster – Burgundy Welcome Design – Your Name in Script – 90mm Drinks Coaster",
         fields=["Name", "Welcome line (optional)"],
         seo_title="Personalised Burgundy Welcome Coaster | Foxy Printing",
         seo_desc="A personalised burgundy welcome coaster with your name in pale pink script inside an ornate frame. 90 x 90 mm, glossy, dishwasher safe, UK made.",
         alt="Personalised burgundy welcome coaster with a name in pale pink script inside an ornate frame between Welcome lines",
         description=desc(
             "Warm burgundy, a fine ornamental frame and your name in pale pink handwriting script make this personalised burgundy "
             "welcome coaster a cosy, grown-up gift for a den, a snug or a reading corner.",
             "A personalised burgundy welcome coaster with your name",
             "Type the name you’d like in the centre, and change the ‘Welcome’ wording above and below if you want something else, "
             "like ‘Cheers’ or ‘Est. 2025’. Leave the second box empty to keep Welcome. The live preview shows it all.",
             ["Deep burgundy and blush tones that feel warm and inviting",
              "Script name in the middle of an ornate frame, like a hotel bar coaster",
              "Your own welcome line if you want to change it",
              "Bright glossy top, cork back and dishwasher safe",
              "Matches our Burgundy Welcome bar mat runner"],
             "Give it with the Burgundy Welcome bar mat, or order one for each couple at a wedding table.")),
    dict(key="o08", handle="personalized-enjoy-my-man-cave-drinks-coaster", group=CAVE, mat="bar-mat-runner-enjoy-my-man-cave",
         title="Personalised Enjoy My Man Cave Coaster – Teal Retro Design – Your Name – 90mm Drinks Coaster",
         fields=[WHOSE],
         seo_title="Personalised Enjoy My Man Cave Coaster | Foxy Printing",
         seo_desc="A personalised Enjoy My Man Cave coaster in bright teal with retro dots. Add a name so it reads Enjoy Dave’s Man Cave. Glossy and dishwasher safe.",
         alt="Personalised Enjoy My Man Cave coaster in bright teal with coloured dots, a black frame and white capitals",
         description=desc(
             "Bright teal, a bold black frame and confetti-style coloured dots give this personalised Enjoy My Man Cave coaster a fun, "
             "retro feel that suits gaming rooms, garages and garden bars.",
             "Personalised Enjoy My Man Cave coaster",
             "Leave the box empty for ENJOY MY / MAN CAVE, or add a name with an apostrophe s, like ‘Tom’s’, and the top line becomes "
             "ENJOY TOM’S. The live preview shows the wording on the coaster before you order.",
             ["Cheerful teal and multi-coloured dots that brighten up a dark den",
              "Black frame and clean capitals that are easy to read",
              "Optional name so visitors know whose cave they’re in",
              "Glossy, dishwasher-safe top with a cork back",
              "Matches our Enjoy My Man Cave bar mat runner"],
             "Pair it with the Enjoy My Man Cave bar mat and a set of coasters for game night.")),
    dict(key="o09", handle="personalized-welcome-man-cave-drinks-coaster", group=CAVE, mat="bar-mat-runner-man-cave-welcome",
         title="Personalised Welcome Man Cave Coaster – Blue & Gold Ribbon Design – Your Name – 90mm Drinks Coaster",
         fields=[WHOSE],
         seo_title="Personalised Welcome Man Cave Coaster | Foxy Printing",
         seo_desc="A personalised welcome man cave coaster in soft blue with gold Welcome ribbons. Add a name to make it Dave’s Cave. Glossy and dishwasher safe.",
         alt="Personalised welcome man cave coaster in soft blue with gold Welcome ribbons and white capitals",
         description=desc(
             "Gold ‘Welcome’ banners above and below, curly scrolls at the sides and big white capitals in the middle: this "
             "personalised welcome man cave coaster is a friendly, slightly vintage take on the man cave sign.",
             "A personalised welcome man cave coaster with ribbons",
             "Keep MAN CAVE, or type a name with an apostrophe s, such as ‘Steve’s’, and it reads STEVE’S CAVE between the ribbons. "
             "You’ll see your wording in the live preview before you add it to your basket.",
             ["Soft blue and gold colours that are calmer than the usual black and orange",
              "Vintage ribbon banners with Welcome built into the design",
              "Optional name for a personal touch",
              "Glossy, dishwasher-safe top with a cork back",
              "Matches our Man Cave Welcome bar mat runner"],
             "Add the matching Man Cave Welcome bar mat for a coordinated bar, or tuck one in a Father’s Day card.")),
    dict(key="o10", handle="personalized-your-text-here-drinks-coaster", group=CAVE, mat="personalised-bar-mat-runner-golden-lions",
         title="Personalised Your Text Coaster – Golden Lions Design – Three Lines of Text – 90mm Drinks Coaster",
         fields=["Line 1", "Line 2", "Line 3 (optional)"],
         seo_title="Personalised Golden Lions Text Coaster | Foxy Printing",
         seo_desc="A personalised golden lions coaster with your own three lines of text between two rampant lions on bold red. 90 x 90 mm, glossy, dishwasher safe.",
         alt="Personalised golden lions coaster in bold red with two gold lions and three lines of your own text",
         description=desc(
             "Two rampant golden lions on bold red, a small crown at the top and your own words in the middle: this personalised golden "
             "lions coaster has the look of a coat of arms for your home bar.",
             "Personalised golden lions coaster with your own text",
             "You get three lines. Use them for a bar name and year (‘The Lions’ / ‘Bar’ / ‘Est. 2025’), a family name, or a short "
             "motto. Line three is optional. Keep each line short so it fits between the lions; the live preview shows exactly how it looks.",
             ["Heraldic red and gold styling that suits a traditional pub or a sports bar",
              "Three lines of your own wording, so it works for almost any message",
              "Rampant lions that look the part on match day",
              "Glossy, dishwasher-safe top with a cork back",
              "Matches our Golden Lions bar mat runner"],
             "Pair it with the Golden Lions bar mat for match days, or order a set with each player’s name.")),
]

OLD_IO_TAGS = ["Bar Coasters", "Man Cave Coasters", "Drinks Coaster", "Custom Name", "Custom Date", "Custom Initial",
               "Initial", "Custom Text", "Personalised Text"]
BASE_TAGS = ["drinks-coaster-2026", "io-bar-coasters", "personalised", "range-home-bar", "home bar", "coaster",
             "bar coaster", "machine-sublimation", "bar-coasters-v2-2026-10-08"]
GROUP_TAGS = {BAR: ["bar-coaster-2026"], CAVE: ["man-cave-coaster-2026", "man cave"]}
CAT = "Home & Garden > Kitchen & Dining > Barware > Coasters"
