import json, re
GS='mm-google-shopping'
def mf(ns,k,t,v): return {"namespace":ns,"key":k,"type":t,"value":v}

# ---------- Club Winter Pack ----------
cwp_html = """<p>Our personalised club winter pack puts a bobble hat and a satin football scarf together, both carrying your own club or business badge, so you’re kitted out for cold touchlines in one go. It suits grassroots club shops, coaches and supporters’ groups.</p>
<h2>Personalised club winter pack: bobble hat and football scarf with your badge</h2>
<p>Pick your hat colour, then upload your badge or logo in the first box. We print it in full colour on the hat’s cuff and use it on the scarf too. Add your team or business name, scarf colours and a slogan, and use the message box for anything else. The live preview shows your details as you type, and we print exactly what you enter, so please check spelling first. Only upload a badge or logo you have the right to use, such as your own club, school or business.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Two winter favourites for less: the pack costs about 10% less than buying the hat and scarf separately</li>
<li>Double-layer knit bobble hat in soft-touch acrylic, with a striped turn-up cuff and a contrasting pom pom</li>
<li>Satin football scarf with a shiny, glossy surface, printable on both sides and finished with tassels</li>
<li>The scarf is printed by sublimation, so your team colours are bold and part of the fabric</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>What’s included: 1 personalised bobble hat and 1 personalised satin football scarf</li>
<li>Hat: one size (adult), 100% soft-touch acrylic, double-layer knit, badge printed in full colour on the cuff</li>
<li>Hat care: machine wash warm, do not iron, do not dry clean</li>
<li>Scarf: 16.5cm x 142cm, polyester with a glossy satin surface, tasselled ends</li>
<li>Separate prices: hat £8.50 and scarf £14.99 (£23.49 in total)</li>
</ul>
<h3>Delivery</h3>
<p>Both items are made to order in-house in North Yorkshire and posted by Royal Mail. We work Monday to Friday. Postage options and costs are shown at checkout. Need packs for a whole squad? Ring us on 01439 771468.</p>
<p>Want the full matchday look? A personalised football car flag in the same colours goes nicely with your personalised club winter pack.</p>"""

hats=[("Black, Red & White","FOXY-DTF-PBH-01","https://cdn.shopify.com/s/files/1/1774/9115/products/Black-and-Red-Bobble-Hat-Mockup-custom-logo.jpg?v=1677145244","black, red and white"),
("Black & Gold","FOXY-DTF-PBH-02","https://cdn.shopify.com/s/files/1/1774/9115/products/Black-and-Yellow-Bobble-Hat-Mockup-custom-logo.jpg?v=1677145447","black and gold"),
("Black & White","FOXY-DTF-PBH-03","https://cdn.shopify.com/s/files/1/1774/9115/products/Black-and-white-Bobble-Hat-Mockup-custom-logo.jpg?v=1677146329","black and white"),
("Royal Blue & White","FOXY-DTF-PBH-04","https://cdn.shopify.com/s/files/1/1774/9115/products/Blue-and-White-Bobble-Hat-Mockup-custom-logo.jpg?v=1677145651","royal blue and white"),
("Red & White","FOXY-DTF-PBH-05","https://cdn.shopify.com/s/files/1/1774/9115/products/Red-and-White-Bobble-Hat-Mockup-custom-logo.jpg?v=1677145741","red and white"),
("Navy, Red & White","FOXY-DTF-PBH-06","https://cdn.shopify.com/s/files/1/1774/9115/products/Navy-and-Red-Bobble-Hat-Mockup-custom-logo.jpg?v=1677145923","navy, red and white"),
("Navy & White","FOXY-DTF-PBH-07","https://cdn.shopify.com/s/files/1/1774/9115/products/Navy-and-White-Bobble-Hat-Mockup-custom-logo.jpg?v=1677146013","navy and white"),
("Green & White","FOXY-DTF-PBH-08","https://cdn.shopify.com/s/files/1/1774/9115/products/Green-Bobble-Hat-Mockup-custom-logo.jpg?v=1677146126","green and white")]
scarf_img=["https://cdn.shopify.com/s/files/1/1774/9115/files/hf_20261002_062109_9a8e8c80-795d-45f7-ae93-c1129e29064a.png?v=1790922349",
"https://cdn.shopify.com/s/files/1/1774/9115/files/hf_20261002_062110_571c8cc7-137d-436d-b568-5b22675aeab0.png?v=1790922350"]
cwp_media=[{"originalSource":hats[0][2],"mediaContentType":"IMAGE","alt":"Personalised club winter pack bobble hat in black, red and white with a full-colour badge on the cuff"},
 {"originalSource":scarf_img[0],"mediaContentType":"IMAGE","alt":"Satin football scarf in red and white with tassels, team name and badge, included in the pack"},
 {"originalSource":scarf_img[1],"mediaContentType":"IMAGE","alt":"Supporters holding up satin football scarves printed with their team name"}]
for name,sku,url,words in hats[1:]:
    cwp_media.append({"originalSource":url,"mediaContentType":"IMAGE","alt":f"Bobble hat in {words} with a full-colour printed badge on the striped cuff"})
cwp={"title":"Personalised Club Winter Pack – Bobble Hat & Satin Football Scarf with Your Badge – Save 10%",
 "handle":"personalised-club-winter-pack-bobble-hat-scarf","status":"DRAFT","vendor":"Foxy Printing","productType":"Football Bundles",
 "templateSuffix":"personalised","descriptionHtml":cwp_html,
 "tags":["foxy-bundle","bundle","club winter pack","personalised","personalised bobble hat","football scarf","grassroots football","team colours","supporters gift","range-football","range-fb-scarves-hats","io-football","machine-dtf","machine-sublimation","foxy-new-2026"],
 "seo":{"title":"Personalised Club Winter Pack: Hat & Scarf | Foxy Printing",
        "description":"A personalised bobble hat and satin football scarf with your club or business badge, for about 10% less than buying them apart. Made in North Yorkshire."},
 "productOptions":[{"name":"Hat colour","values":[{"name":h[0]} for h in hats]}],
 "metafields":[mf("foxy","mockup","single_line_text_field","photo"),
  mf("foxy","personalise_fields","list.single_line_text_field",json.dumps(["Badge or logo upload","Team or business name","Scarf colours","Scarf slogan","Message for us (e.g. how many packs, team order details)"])),
  mf(GS,"custom_product","boolean","true"),mf(GS,"condition","single_line_text_field","new"),
  mf(GS,"google_product_category","single_line_text_field","Apparel & Accessories > Clothing Accessories > Hats"),
  mf(GS,"gender","single_line_text_field","unisex"),mf(GS,"age_group","single_line_text_field","adult"),
  mf(GS,"color","single_line_text_field","Multicolor"),mf(GS,"mpn","single_line_text_field","FOXY-BNDL-CWP-01")]}
cwp_vars=[{"optionValues":[{"optionName":"Hat colour","name":h[0]}],"price":"20.99","compareAtPrice":"23.49",
  "inventoryPolicy":"CONTINUE","inventoryItem":{"sku":f"FOXY-BNDL-CWP-{i+1:02d}","tracked":False,"requiresShipping":True}} for i,h in enumerate(hats)]

# ---------- Matchday Pack ----------
mdp_html = """<p>Our personalised matchday pack brings together a 3ft x 2ft terrace flag, a football car flag and 9m of club bunting, so your supporters’ group, clubhouse or family car is dressed for the big game in one order. It’s ideal for cup finals, tournaments and presentation nights.</p>
<h2>Personalised matchday pack: terrace flag, car flag and club bunting</h2>
<p>Upload your club badge or logo and add your team name and colours for the car flag and bunting, plus the season if you want it. For the terrace flag, pick any design from our Football Terrace Flags range, name it in the box and type your wording. The live preview shows your details as you type, and we print exactly what you enter, so please check spelling first. Only upload a badge or logo you have the right to use, such as your own club, school or business.</p>
<h3>Why you’ll love it</h3>
<ul>
<li>Three matchday favourites for about 10% less than buying them separately</li>
<li>Terrace flag in 115gsm knitted polyester with strong 25mm edge binding and eyelets on all 4 edges</li>
<li>Car flag in 100% polyester on a 43cm plastic stand with a window clip and fastener</li>
<li>Club bunting printed on both sides, so it looks right from wherever people are standing</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>What’s included: 1 personalised terrace flag (3ft x 2ft), 1 personalised car flag and 1 run of personalised club bunting</li>
<li>Terrace flag: single-sided print, hand-stitched, with a fire label (certificate available on request)</li>
<li>Car flag: 100% polyester flag with a 43cm plastic stand, window clip and fastener</li>
<li>Bunting: 9m long with about 30 A4 flags, printed both sides</li>
<li>Separate prices: terrace flag £19.99, car flag £9.99 and bunting £24.99 (£54.97 in total)</li>
</ul>
<h3>Delivery</h3>
<p>Every item in your personalised matchday pack is made to order. Postage options and costs are shown at checkout. Got a set date, or need packs for a whole club? Ring us on 01439 771468.</p>
<p>Want the supporters kitted out too? Add a personalised club winter pack with a matching bobble hat and satin scarf.</p>"""
mdp_media=[{"originalSource":"https://cdn.shopify.com/s/files/1/1774/9115/files/hf_20261002_062144_e84d679f-01a1-40a2-8b21-277ccfdfad6f.png?v=1790922350","mediaContentType":"IMAGE","alt":"Football car flag with window clip printed with a team name and badge, part of the personalised matchday pack"},
 {"originalSource":"https://cdn.shopify.com/s/files/1/1774/9115/files/hf_20261002_062144_de36c954-beca-42d9-b073-d0f6dbad4a3b.png?v=1790922351","mediaContentType":"IMAGE","alt":"Green and white club bunting with team name, badge and season"},
 {"originalSource":"https://cdn.shopify.com/s/files/1/1774/9115/files/UnionJackFlag-FullyCustomisable-01copy.jpg?v=1724239835","mediaContentType":"IMAGE","alt":"Example 3ft x 2ft terrace flag, a Union Jack design printed with custom wording"},
 {"originalSource":"https://cdn.shopify.com/s/files/1/1774/9115/files/hf_20261002_062144_f5a4d923-3942-49f5-83da-aca09cf926fb.png?v=1790922351","mediaContentType":"IMAGE","alt":"Family car on matchday with a team car flag on the rear window"},
 {"originalSource":"https://cdn.shopify.com/s/files/1/1774/9115/files/hf_20261002_062144_e77ab82f-af80-459f-a2de-20bbea90ac61.png?v=1790922350","mediaContentType":"IMAGE","alt":"Village hall awards night decorated with club bunting in team colours"}]
mdp={"title":"Personalised Matchday Pack – 3ft x 2ft Terrace Flag, Car Flag & 9m Club Bunting – Save 10%",
 "handle":"personalised-matchday-pack-flag-car-flag-bunting","status":"DRAFT","vendor":"Foxy Printing","productType":"Football Bundles",
 "templateSuffix":"personalised","descriptionHtml":mdp_html,
 "tags":["foxy-bundle","bundle","matchday pack","matchday","personalised","terrace flag","car flag","club bunting","grassroots football","supporters gift","team colours","range-football","range-fb-flags","io-football","machine-sublimation","foxy-new-2026"],
 "seo":{"title":"Personalised Matchday Pack: Flags & Bunting | Foxy Printing",
        "description":"A personalised terrace flag, car flag and 9m club bunting with your badge and team colours, for about 10% less than buying them apart. Order the full set."},
 "productOptions":[{"name":"Pack","values":[{"name":"Terrace flag 3ft x 2ft + car flag + 9m bunting"}]}],
 "metafields":[mf("foxy","mockup","single_line_text_field","photo"),
  mf("foxy","personalise_fields","list.single_line_text_field",json.dumps(["Club badge or logo upload","Team name","Team colours","Terrace flag design (name from our range)","Text on the terrace flag","Season (for the bunting)","Message for us (anything else)"])),
  mf(GS,"custom_product","boolean","true"),mf(GS,"condition","single_line_text_field","new"),
  mf(GS,"google_product_category","single_line_text_field","Home & Garden > Decor > Flags & Windsocks"),
  mf(GS,"gender","single_line_text_field","unisex"),mf(GS,"age_group","single_line_text_field","adult"),
  mf(GS,"color","single_line_text_field","Multicolor"),mf(GS,"mpn","single_line_text_field","FOXY-BNDL-MDP-01")]}
mdp_vars=[{"optionValues":[{"optionName":"Pack","name":"Terrace flag 3ft x 2ft + car flag + 9m bunting"}],"price":"49.49","compareAtPrice":"54.97",
  "inventoryPolicy":"CONTINUE","inventoryItem":{"sku":"FOXY-BNDL-MDP-01","tracked":False,"requiresShipping":True}}]

for n,p in [("cwp",cwp),("mdp",mdp)]:
    txt=re.sub('<[^>]+>',' ',p["descriptionHtml"]); 
    print(n,'words',len(txt.split()),'title',len(p["title"]),'seoT',len(p["seo"]["title"]),'seoD',len(p["seo"]["description"]), "'" in p["descriptionHtml"])
    for m in p["metafields"]:
        if "'" in m["value"]: print("straight apostrophe in",m["key"])
json.dump({"product":cwp,"media":cwp_media},open('cwp_create.json','w'),ensure_ascii=False)
json.dump({"product":mdp,"media":mdp_media},open('mdp_create.json','w'),ensure_ascii=False)
json.dump(cwp_vars,open('cwp_vars.json','w'),ensure_ascii=False); json.dump(mdp_vars,open('mdp_vars.json','w'),ensure_ascii=False)
