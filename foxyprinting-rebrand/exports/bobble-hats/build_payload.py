"""Build the 6 Oct 2026 rewrite of the 8 personalised bobble hats (Beechfield B472 blank).

Facts: plan/product-facts.md, "Personalised bobble hats (Ralawise blank)".
Writes payload.json (used for the productUpdate / metafieldsSet / variant calls) and checks lengths.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).parent

FIELDS = [
    "Badge or logo upload",
    "Club or business name (optional)",
    "Text to print under the design (optional)",
    "Message for us (e.g. how many hats, team order details)",
]

SIZE = """<h3>Size &amp; details</h3>
<ul>
<li>One size (adult)</li>
<li>100% soft-touch acrylic, double-layer knit</li>
<li>Turn-up cuff with stripes and a contrasting pom pom</li>
<li>Your badge or logo printed in full colour on the front of the cuff</li>
<li>Care: machine wash warm, do not iron, do not dry clean</li>
</ul>
<h3>Delivery</h3>
<p>Every hat is printed to order and posted by Royal Mail. We work Monday to Friday, so weekend orders are picked up on Monday. Postage options and costs are shown at checkout.</p>"""

UPLOAD = ("Upload your badge or logo in the first box – it’s needed before the hat can go in your basket. You can add your club or business name and a short line of text to go under the design, "
          "and use the message box to tell us about team orders. The live preview shows your details as you type. We print "
          "exactly what you upload, so please check it before you order. Please only upload a badge or logo "
          "you have the right to use, such as your own club, school or business.")

P = [
 dict(id=8062691082491, var=44393502441723, inv=46466169045243, media=None, colour="Black/Classic Red/White", gcolor="Black",
  short="Black, Red & White", seo_c="Black Red White",
  kw="personalised black and red bobble hat",
  intro="A personalised black and red bobble hat is the classic matchday look for any team that plays in red and black. "
        "Add your club badge or company logo and we’ll print it on the cuff, ready for cold touchlines and early-morning kick-offs.",
  h2="Personalised black and red bobble hat with your badge",
  why=["Black, red and white colourway with a striped cuff and a contrasting pom pom – bold colours that suit red-and-black kits",
       "Double-layer knit in soft-touch acrylic keeps ears warm through a full ninety minutes",
       "Your badge printed in full colour, so club badges and detailed logos keep their colours",
       "Great for Sunday league squads, junior club coaches and supporters’ groups wanting a matching hat",
       "Bulk and team orders welcome – ring us on 01439 771468 for a big order"],
  close="Kitting out the whole squad? A personalised black and red bobble hat pairs nicely with a personalised football scarf from our football range.",
  meta="Matchday kit for red-and-black teams: a personalised black and red bobble hat with your club badge or business logo on the cuff. Team orders welcome."),
 dict(id=8062691967227, var=44393504375035, inv=46466170978555, media=None, colour="Black/Gold", gcolor="Black",
  short="Black & Gold", seo_c="Black & Gold",
  kw="personalised black and gold bobble hat",
  intro="Our personalised black and gold bobble hat stands out from across the pitch, and it’s a smart pick for teams that play in amber and black. "
        "It works just as well for businesses with gold branding who want warm, eye-catching winter workwear.",
  h2="A personalised black and gold bobble hat with your logo",
  why=["Black and gold colourway with a striped cuff and contrasting pom pom – easy to spot in a crowd",
       "Soft-touch acrylic in a double-layer knit for proper winter warmth",
       "Ideal for staff at outdoor events, market stalls, car parks and hospitality on cold evenings",
       "A team gift that looks the part for amber-and-black clubs, from under-9s parents to vets’ sides",
       "Order one or a whole batch – bulk and team orders are welcome"],
  close="Want the same logo for summer? Team your personalised black and gold bobble hat with our personalised caps and T-shirts for an easy staff uniform.",
  meta="Stand out on the touchline or at work with a personalised black and gold bobble hat – your club badge or company logo printed in full colour on the cuff."),
 dict(id=8062692327675, var=44393505554683, inv=46466172158203, media=None, colour="Black/White", gcolor="Black",
  short="Black & White", seo_c="Black & White",
  kw="personalised black and white bobble hat",
  intro="A personalised black and white bobble hat goes with almost any logo, which is why it’s our go-to for businesses, schools and black-and-white clubs alike. "
        "Send us your badge and we’ll print it in full colour on the cuff.",
  h2="Your logo on a personalised black and white bobble hat",
  why=["Monochrome colourway with a striped cuff and pom pom – any badge colour sits well against it",
       "A simple branded workwear hat for trades, delivery drivers and outdoor staff",
       "Double-layer soft-touch acrylic knit that stays warm and comfortable all day",
       "Suits black-and-white football and rugby clubs, school PE staff and supporters’ groups",
       "Bulk and team orders welcome, so the whole crew can match"],
  close="Building a branded winter range? Pair a personalised black and white bobble hat with logo T-shirts or hoodies so your team looks the same on site.",
  meta="Simple branded winter workwear: a personalised black and white bobble hat with your logo or club badge printed on the cuff. One size, bulk orders welcome."),
 dict(id=8062692720891, var=44393506013435, inv=46466172616955, media=None, colour="Royal/White", gcolor="Blue",
  short="Royal Blue & White", seo_c="Royal Blue & White",
  kw="personalised royal blue bobble hat",
  intro="This personalised royal blue bobble hat is bright, cheerful and made for blue-and-white teams. "
        "Junior club coaches and parents, netball teams and school staff love it for winter fixtures, presentation nights and fundraising.",
  h2="Personalised royal blue bobble hat for clubs and schools",
  why=["Bright royal blue and white with a striped cuff and contrast pom pom – a proper blues colourway",
       "Your school or club badge printed in full colour on the front of the cuff",
       "Warm double-layer knit in soft-touch acrylic for chilly touchlines and playgrounds",
       "A great fundraiser for PTAs and junior clubs – order a batch and sell them on",
       "Bulk and team orders welcome; ring 01439 771468 to talk numbers"],
  close="A personalised royal blue bobble hat makes a lovely end-of-season gift for coaches and volunteers, too.",
  meta="A bright personalised royal blue bobble hat with your school or club badge printed on the cuff. Ideal for junior teams, PTAs and fundraisers."),
 dict(id=8062693114107, var=44393506930939, inv=46466173534459, media=None, colour="Classic Red/White", gcolor="Red",
  short="Red & White", seo_c="Red & White",
  kw="personalised red and white bobble hat",
  intro="Nothing says winter football like a personalised red and white bobble hat. "
        "It’s a favourite for red-and-white clubs and supporters’ groups, and it’s festive enough for Christmas markets and charity events too.",
  h2="Personalised red and white bobble hat with your club badge",
  why=["Classic red and white colourway with a striped cuff and contrasting pom pom",
       "Your badge or logo printed in full colour, sitting front and centre on the cuff",
       "Soft-touch acrylic, double-layer knit – soft and warm",
       "Brilliant for supporters’ coach trips, Boxing Day fixtures and festive fun runs",
       "Bulk and team orders welcome for squads, committees and volunteers"],
  close="Heading to the match? Add a personalised football scarf to your personalised red and white bobble hat for the full set.",
  meta="Get matchday ready with a personalised red and white bobble hat – your club badge or logo printed in full colour on the cuff. Great for fans and squads."),
 dict(id=8062693769467, var=44393508471035, inv=46466175074555, media=None, colour="French Navy/Red/White", gcolor="Navy",
  short="Navy, Red & White", seo_c="Navy Red & White",
  kw="personalised navy, red and white bobble hat",
  intro="A personalised navy, red and white bobble hat has a smart, traditional feel that suits schools, sailing and cricket clubs as well as football teams. "
        "Your logo goes on the cuff, printed in full colour.",
  h2="A personalised navy, red and white bobble hat with your logo",
  why=["Three-colour striped cuff in French navy, red and white with a contrast pom pom",
       "Smart enough for school uniform shops, staff at outdoor events and branded corporate gifts",
       "Double-layer soft-touch acrylic knit for warmth on frosty mornings",
       "Suits clubs in navy and red, and any business with red, white and blue branding",
       "Bulk and team orders welcome – just give us a ring"],
  close="Looking for a thank-you gift for coaches or staff? A personalised navy, red and white bobble hat is always a winter favourite.",
  meta="Smart and traditional: a personalised navy, red and white bobble hat with your school, club or company logo on the cuff. Warm, one size, adult."),
 dict(id=8062694555899, var=44393509945595, inv=46466176549115, media=None, colour="Navy/White", gcolor="Navy",
  short="Navy & White", seo_c="Navy & White",
  kw="personalised navy bobble hat with logo",
  intro="If you want something understated, this personalised navy bobble hat with logo is the one. "
        "Navy and white looks tidy with a uniform or work jacket, so it’s popular for workwear, school staff and rugby clubs.",
  h2="Personalised navy bobble hat with logo for workwear and teams",
  why=["Navy and white colourway with a striped cuff and pom pom – smart, not shouty",
       "A practical branded hat for site teams, groundstaff, drivers and outdoor events crews",
       "Your company or club logo printed in full colour on the front of the cuff",
       "Warm double-layer knit in soft-touch acrylic that’s machine washable",
       "Order a few or a whole team’s worth – bulk orders welcome"],
  close="Pair your personalised navy bobble hat with logo T-shirts or hoodies for an easy matching staff uniform.",
  meta="Tidy branded workwear: a personalised navy bobble hat with your company or club logo on the cuff. Warm double-layer knit, and bulk staff orders welcome."),
 dict(id=8062695309563, var=44393511387387, inv=46466177990907, media=None, colour="Kelly Green/White", gcolor="Green",
  short="Green & White", seo_c="Green & White",
  kw="personalised green and white bobble hat",
  intro="Our personalised green and white bobble hat is a cracking choice for clubs in green and white hoops, and for gardeners, landscapers and outdoor businesses who want their logo on show. "
        "It’s great for St Patrick’s Day events too.",
  h2="Personalised green and white bobble hat with your badge or logo",
  why=["Bright kelly green and white with a striped cuff and contrasting pom pom",
       "A cosy branded hat for landscaping crews, garden centres, farm shops and charity fun runs",
       "Your badge or logo printed in full colour on the front of the cuff",
       "Double-layer soft-touch acrylic for warmth through long winter shifts",
       "Bulk and team orders welcome for squads, staff and volunteers"],
  close="Kitting out a green and white team? Match your personalised green and white bobble hat with a flag or scarf from our football range.",
  meta="A personalised green and white bobble hat with your club badge or business logo on the cuff. Warm, one size and great for teams, staff and outdoor events."),
]


def description(p):
    why = "\n".join(f"<li>{w}</li>" for w in p["why"])
    return (f"<p>{p['intro']}</p>\n<h2>{p['h2'][0].upper() + p['h2'][1:]}</h2>\n<p>{UPLOAD}</p>\n"
            f"<h3>Why you’ll love it</h3>\n<ul>\n{why}\n</ul>\n{SIZE}\n<p>{p['close']}</p>")


def main():
    out = []
    for i, p in enumerate(P, 1):
        sku = f"FOXY-DTF-PBH-{i:02d}"
        title = (f"Personalised Football Bobble Hat with Your Club or Business Logo – {p['short']} Striped Cuff – "
                 f"One Size Team & Workwear Beanie")
        seo_title = f"Personalised {p['seo_c']} Bobble Hat | Foxy Printing"
        desc = description(p)
        words = len(re.sub("<[^>]+>", " ", desc).split())
        meta = p["meta"]
        out.append(dict(id=f"gid://shopify/Product/{p['id']}", variant=f"gid://shopify/ProductVariant/{p['var']}",
                        inventoryItem=f"gid://shopify/InventoryItem/{p['inv']}", sku=sku, colour=p["colour"],
                        title=title, seo_title=seo_title, meta=meta, descriptionHtml=desc, words=words,
                        gcolor=p["gcolor"], keyword=p["kw"],
                        alt=f"{p['kw'][0].upper() + p['kw'][1:]}, with a full-colour printed {'logo' if 'logo' in p['kw'] else 'badge'} on the striped cuff".replace("with logo, with a full-colour printed logo", "with a full-colour printed logo")))
        print(sku, words, len(title), len(seo_title), len(meta), "|", seo_title, "|", meta)
        assert 180 <= words <= 350 and len(title) <= 150 and len(seo_title) <= 60 and 140 <= len(meta) <= 155, (sku, words, len(meta))
        assert desc.lower().count(p["kw"]) >= 3, (sku, "keyword")
    json.dump(dict(fields=FIELDS, products=out), open(HERE / "payload.json", "w"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
