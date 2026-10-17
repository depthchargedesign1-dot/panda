import json,re
html="""<p>Kitting out a grassroots football club, a school team or a small business? Send us your badge or logo and we print it on bobble hats, caps, polo shirts, hi-vis vests, scarves, flags, bunting, stickers and more.</p>
<h2>Club, team and business logo products</h2>
<p>Every item here is made to order with your own design. Upload your badge or logo on the product page, add your team or business name, and the live preview shows your details as you type. We print exactly what you send, so please check spelling before you order. Please only upload a badge or logo you have the right to use, such as your own club, school or business. We don’t print professional club crests.</p>
<h3>Multi-buy savings for teams</h3>
<ul>
<li>Clothing multi-buy: 5% off 3 or more, 20% off 10 or more and 30% off 20 or more, and you can mix hats, scarves, socks and other clothing</li>
<li>Terrace flags: buy 3 or more and save 10%</li>
</ul>
<p>Savings come off automatically at checkout. Ordering for a whole squad, a staff team or a club shop? Ring us on 01439 771468 and we’ll help you get it right.</p>"""
seo={"title":"Club, Team & Business Logo Products | Foxy Printing","description":"Send us your club badge or business logo and we print it on hats, caps, polos, flags, bunting and stickers. Team multi-buy savings come off at checkout."}
t=re.sub('<[^>]+>',' ',html); print(len(t.split()), len(seo['title']), len(seo['description']))
tags=["range-football","range-fb-flags","range-fb-scarves-hats","range-workwear","Club Hats","Terrace Flags","workwear","club-stickers","logo-stickers","foxy-bundle"]
inp={"title":"Clubs, Teams & Business Logo Products","handle":"clubs-teams-logo-products","descriptionHtml":html,"seo":seo,
 "ruleSet":{"appliedDisjunctively":True,"rules":[{"column":"TAG","relation":"EQUALS","condition":c} for c in tags]}}
json.dump({"input":inp},open('coll.json','w'),ensure_ascii=False)
