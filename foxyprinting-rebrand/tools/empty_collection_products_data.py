"""Product data + copy for the products made to fill empty collections (8 Oct 2026).
Facts only from plan/product-facts.md: "Mugs (11oz ceramic, sublimation)" and "Posters & prints".
Dispatch time and paper stock are ASK, so the copy promises neither.
Writes exports/collections-audit/2026-10-08/products/products.json (productCreate inputs).
"""
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "exports/collections-audit/2026-10-08/products/products.json"

MUG_CAT = "Home & Garden > Kitchen & Dining > Tableware > Drinkware > Mugs"
PRINT_CAT = "Home & Garden > Decor > Artwork > Posters, Prints, & Visual Artwork"
NO_PROOF = "We print exactly what you enter, so please check names and spelling in the live preview before you order."

MUG_DETAILS = """<h3>Size &amp; details</h3>
<ul>
<li>White ceramic mug, 11oz (approx. 325ml)</li>
<li>C-shaped handle and a high-gloss finish</li>
<li>Sublimation printed in-house in North Yorkshire, with the design on both sides</li>
<li>Dishwasher and microwave safe &ndash; avoid abrasive scourers</li>
</ul>
<h3>Delivery</h3>
<p>Every mug is printed to order in our North Yorkshire workshop and sent out in protective packaging for UK delivery.</p>"""

MUG_TAGS = ["11oz mug", "foxy-new-2026", "machine-sublimation", "personalised", "personalised mug 1",
            "personalised-mugs", "Personalised Mug", "Printed Mug", "io-mugs"]

P = []

P.append(dict(
    code="TMIAM", collection="trust-me-im-a-mugs",
    title="Personalised Trust Me I’m A… Mug – Any Job Title – Funny Work Gift – 11oz Ceramic",
    handle="personalised-trust-me-im-a-mug",
    primary="personalised trust me I’m a mug",
    seo_title="Personalised Trust Me I’m A Mug | Foxy Printing",
    seo_desc="A personalised trust me I’m a mug with any job title and their name. Great for nurses, plumbers and teachers – printed on 11oz white ceramic.",
    fields=["Job title (e.g. Nurse)", "Name (optional)"],
    tags=MUG_TAGS + ["Trust Me I'm A... Mugs", "trust me mug", "job mug", "work gift", "funny-mugs", "colleague gift"],
    html=f"""<p>This personalised trust me I’m a mug is for the person everyone turns to when something needs sorting, whether that’s a nurse on a long shift, a plumber with the answer to every leak or the teacher who keeps the whole class going. Add their job title and name and it becomes a mug that’s properly theirs.</p>
<h2>A personalised trust me I’m a mug with their job title</h2>
<p>Type their job into the first box and it’s printed big and bold under “Trust me, I’m a”. Nurse, electrician, mechanic, dental nurse, accountant &ndash; any job works, and longer titles are sized down to fit. Add their name in the second box if you’d like it under the line, or leave it blank. Watch it come together in the live preview as you type. {NO_PROOF}</p>
<h3>Why you’ll love it</h3>
<ul>
<li>A funny job mug that works for almost any trade or profession</li>
<li>A thoughtful work gift for a new starter, a qualification or a well-earned thank you</li>
<li>Navy and coral lettering that stays crisp and easy to read across the room</li>
<li>Printed on both sides, so it reads right whether they’re left or right-handed</li>
<li>Sublimation printed onto an 11oz white ceramic mug for everyday brews</li>
</ul>
{MUG_DETAILS}
<p>A personalised trust me I’m a mug makes a lovely colleague gift for the staff room &ndash; add a box of biscuits and it’s sorted.</p>"""))

P.append(dict(
    code="ILAM3PM", collection="i-like-mugs",
    title="Personalised I Like… and Maybe 3 People Mug – Any Hobby – Funny Gift – 11oz Ceramic",
    handle="personalised-i-like-and-maybe-3-people-mug",
    primary="I like and maybe 3 people mug",
    seo_title="I Like and Maybe 3 People Mug | Foxy Printing",
    seo_desc="Our personalised I like and maybe 3 people mug shows their favourite hobby and name. A funny gift for gardeners, gamers and walkers on 11oz ceramic.",
    fields=["Hobby (e.g. Gardening)", "Name (optional)"],
    tags=MUG_TAGS + ["I Like... Mugs", "hobby mug", "funny-mugs", "gardening gift", "introvert gift"],
    html=f"""<p>The I like and maybe 3 people mug is made for the happily unsociable: the gardener who’d rather be in the greenhouse, the angler at the water by six, the gamer who wants one more level. Tell the world what they love most, then let them decide who the three lucky people are.</p>
<h2>A personalised I like and maybe 3 people mug for any hobby</h2>
<p>Pop their hobby in the first box &ndash; gardening, fishing, knitting, golf, baking, cycling &ndash; and it’s printed large in the middle, with “and maybe 3 people” underneath. Add a name in the second box for a small signature at the bottom, or leave it off. The live preview shows exactly how it will look. {NO_PROOF}</p>
<h3>Why you’ll love it</h3>
<ul>
<li>A funny hobby mug that sums up their passion in one word</li>
<li>Easy birthday, Christmas or Secret Santa present for the person who has everything</li>
<li>Teal, navy and coral lettering with a clean, modern look</li>
<li>The design is printed twice, so it faces them whichever hand holds the mug</li>
<li>Sublimation printed onto 11oz white ceramic, made to be used every day</li>
</ul>
{MUG_DETAILS}
<p>Picking a present for a keen gardener? Pair the I like and maybe 3 people mug with a packet of seeds for a gardening gift they’ll actually use.</p>"""))

P.append(dict(
    code="IUTDRM", collection="i-used-to-drive-mugs",
    title="Personalised I Used To Drive… Mug – Retirement Gift for Lorry, Bus & Taxi Drivers – 11oz Ceramic",
    handle="personalised-i-used-to-drive-retirement-mug",
    primary="personalised retirement mug for drivers",
    seo_title="Personalised Retirement Mug for Drivers | Foxy Printing",
    seo_desc="A personalised retirement mug for drivers: I used to drive lorries, now I just drive everyone mad. Add what they drove and their name on 11oz ceramic.",
    fields=["What they drove (e.g. Lorries, Buses, Taxis)", "Name"],
    tags=MUG_TAGS + ["I Used To Drive Mugs", "retirement gift", "driver gift", "lorry driver gift", "bus driver gift", "funny-mugs", "gifts for dad"],
    html=f"""<p>After years behind the wheel, this personalised retirement mug for drivers gives them the send-off they deserve. “I used to drive lorries, now I just drive everyone mad” &ndash; a cheeky nod to all those miles, early starts and motorway services, with their name in the farewell line.</p>
<h2>A personalised retirement mug for drivers who’ve hung up the keys</h2>
<p>Fill in what they drove &ndash; lorries, buses, taxis, trains, forklifts, delivery vans &ndash; and it’s printed in bold mustard in the middle of the design. Their name goes into the “Happy retirement” line at the bottom. Check it all in the live preview before you add it to your basket. {NO_PROOF}</p>
<h3>Why you’ll love it</h3>
<ul>
<li>A funny retirement gift that every lorry, bus or taxi driver will recognise</li>
<li>Ideal for a leaving do, a depot collection or a card-and-mug retirement present</li>
<li>Works for any vehicle you type in, so the same mug suits a whole team of drivers</li>
<li>Printed on both sides, so the joke is facing out on the tea break</li>
<li>Sublimation printed onto 11oz white ceramic for years of retirement brews</li>
</ul>
{MUG_DETAILS}
<p>Lorry driver gift sorted: give this personalised retirement mug for drivers with a card signed by the whole depot.</p>"""))

P.append(dict(
    code="IGTM", collection="ive-got-mugs",
    title="Personalised I’ve Got This Mug – Motivational Gift with Name & Message – 11oz Ceramic",
    handle="personalised-ive-got-this-mug",
    primary="personalised I’ve got this mug",
    seo_title="Personalised I’ve Got This Mug | Foxy Printing",
    seo_desc="A personalised I’ve got this mug with their name and a short message. A motivational gift for exams, new jobs and fresh starts, on 11oz ceramic.",
    fields=["Name", "Message (optional, e.g. Good luck in your new job)"],
    tags=MUG_TAGS + ["I've Got Mugs", "motivational mug", "good luck gift", "new job gift", "exam gift"],
    html=f"""<p>A personalised I’ve got this mug is a small daily reminder for someone facing something big &ndash; a new job, exams, a driving test, a fresh start or a tough week. Their name and your message turn a morning coffee into a quiet bit of encouragement.</p>
<h2>A personalised I’ve got this mug with name and message</h2>
<p>“I’ve got this” is printed big and bold under a little mustard sunrise, with their name in a flowing coral script underneath. Add a short message in the second box, such as “Good luck in your new job” or “Proud of you”, and it appears in small capitals at the bottom; leave it blank for a cleaner look. The live preview shows it all as you type. {NO_PROOF}</p>
<h3>Why you’ll love it</h3>
<ul>
<li>A motivational mug that cheers them on every single morning</li>
<li>A good luck gift for exams, interviews, promotions or starting university</li>
<li>Navy, mustard and coral colours with a bright, positive feel</li>
<li>The design is printed on both sides of the mug</li>
<li>Sublimation printed onto 11oz white ceramic, dishwasher safe for daily use</li>
</ul>
{MUG_DETAILS}
<p>A personalised I’ve got this mug makes a thoughtful new job gift for a friend, daughter or colleague &ndash; pair it with a card wishing them luck.</p>"""))

P.append(dict(
    code="CBM", collection="cheeky-mugs",
    title="Personalised Cheeky Little Brew Mug – Name Mug for Tea & Coffee Lovers – 11oz Ceramic",
    handle="personalised-cheeky-little-brew-mug",
    primary="personalised cheeky brew mug",
    seo_title="Personalised Cheeky Brew Mug with Name | Foxy Printing",
    seo_desc="Treat them to a personalised cheeky brew mug with their name. Choose brew, cuppa or coffee for a fun tea lover gift on a classic 11oz white mug.",
    fields=["Name", "Drink word (e.g. Brew, Cuppa, Coffee)"],
    tags=MUG_TAGS + ["Cheeky Mugs", "name mug", "tea lover gift", "coffee lover gift", "funny-mugs"],
    html=f"""<p>This personalised cheeky brew mug is for the person who’s always “just having a quick one” &ndash; the tea break champion, the coffee-first-then-talk friend, the Mum who deserves five minutes’ peace. Their name sits on top in a playful script, so everyone knows whose mug it is.</p>
<h2>A personalised cheeky brew mug with their name</h2>
<p>Add their name and it’s printed in coral script above “Cheeky little brew” in bold navy letters. Prefer a different drink? Type cuppa, coffee, tea or hot choc into the second box and we’ll swap the last word. The live preview updates as you type, so you can see it before you order. {NO_PROOF}</p>
<h3>Why you’ll love it</h3>
<ul>
<li>A fun name mug that stops the office mug mix-ups for good</li>
<li>A tea lover gift or coffee lover gift for birthdays, Mother’s Day or a thank you</li>
<li>Cheerful navy and coral design that suits any kitchen</li>
<li>Printed on both sides, so their name faces out either way</li>
<li>Sublimation printed onto 11oz white ceramic for everyday brews</li>
</ul>
{MUG_DETAILS}
<p>Add a box of their favourite tea bags or biscuits and your personalised cheeky brew mug becomes a ready-made little gift.</p>"""))

P.append(dict(
    code="MCAAP", collection="art-poster", kind="print",
    title="Personalised Mid-Century Abstract Family Name Print – Modern Wall Art – A4 to A1",
    handle="personalised-mid-century-abstract-family-name-print",
    primary="personalised family name print",
    seo_title="Personalised Family Name Abstract Print | Foxy Printing",
    seo_desc="A personalised family name print in mid-century abstract style, with your surname and the year you began. Modern wall art in A4, A3, A2 or A1 sizes.",
    fields=["Family name (e.g. The Taylors)", "Est. year (optional)"],
    tags=["Art poster", "personalised poster", "Poster", "foxy-new-2026", "personalised", "io-prints", "wall art",
          "abstract art print", "family name print", "new home gift", "mid-century print"],
    html=f"""<p>Our personalised family name print brings a touch of mid-century style to the hallway, living room or kitchen. Soft geometric shapes in terracotta, mustard, sage and navy sit above your family name, with the year your family began written underneath.</p>
<h2>A personalised family name print in mid-century abstract style</h2>
<p>Type your family name &ndash; “The Taylors”, “The Khan Family”, “Ava &amp; Sam” &ndash; and it’s printed in tall, clean capitals beneath the artwork. Add the year you got married, moved in or became a family, or leave that box empty. The live preview shows your wording on the print before you order. {NO_PROOF}</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Modern abstract wall art that feels personal without being fussy</li>
<li>A lovely new home gift, wedding or anniversary present</li>
<li>Warm, earthy colours that sit happily with wood, linen and neutral walls</li>
<li>Four sizes, from a desk-sized A4 to a statement A1 above the sofa</li>
<li>Designed and printed in-house in North Yorkshire</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>A4 (210 &times; 297 mm) &pound;4.99, A3 (297 &times; 420 mm) &pound;8.99, A2 (420 &times; 594 mm) &pound;12.99, A1 (594 &times; 841 mm) &pound;19.99</li>
<li>Portrait layout; the artwork scales to every size without losing sharpness</li>
<li>Print only &ndash; frame not included</li>
</ul>
<h3>Delivery</h3>
<p>Each print is made to order in our North Yorkshire workshop and sent out for UK delivery.</p>
<p>Moving house soon? A personalised family name print makes a thoughtful housewarming gift alongside a pair of matching mugs.</p>"""))


def words(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())


if __name__ == "__main__":
    for p in P:
        w = words(p["html"])
        print(p["code"], w, "words", len(p["seo_title"]), "seo", len(p["seo_desc"]), "meta", len(p["title"]), "title")
        assert 180 <= w <= 350 and len(p["seo_title"]) <= 60 and 140 <= len(p["seo_desc"]) <= 155, p["code"]
        assert p["primary"].lower() in re.sub(r"<[^>]+>", " ", p["html"]).replace("&rsquo;", "’").lower()
    json.dump(P, open(OUT, "w"), indent=1, ensure_ascii=False)
