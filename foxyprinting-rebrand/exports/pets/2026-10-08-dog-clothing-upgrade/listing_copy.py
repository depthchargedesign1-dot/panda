"""Titles, copy, SEO and personalisation for the 6 dog clothing products (8 Oct 2026).
Facts only from plan/product-facts.md "Pet apparel" (Ralawise PP001-PP008 pages)."""
SIZES = 'Back length (base of the neck to base of the tail): XS 25cm, S 30cm, M 35cm, L 40cm, XL 45cm, 2XL 50cm, 3XL 55cm, 4XL 60cm. If your dog is between sizes, go up one.'
DELIVERY = '<h3>Delivery</h3>\n<p>Each one is printed to order in our North Yorkshire workshop. Postage options and costs are shown at checkout.</p>'
CHECK = 'We print exactly what you enter, so please check names and spelling before you order.'
NAME_NUM = ('Both personalisation boxes are optional. Add your dog\'s name, a number (up to 3 characters, such as their age or a lucky number), '
            'both or neither, and we\'ll print it on the back in our North Yorkshire workshop. Leave both boxes empty for a plain {g}. '
            'Pick your colour and size, then type your text in the boxes above. ' + CHECK)
NAME_ONLY = ('Adding a name is optional. Type your dog\'s name in the box above and we\'ll print it on the back in our North Yorkshire workshop, '
             'or leave it empty for a plain {g}. Pick your colour and size first. ' + CHECK)

C = {
 'PP001': dict(
  title='Personalised Dog Raglan T-Shirt – Optional Name & Number – 5 Colours – Sizes XS–4XL',
  seo_title='Personalised Dog T-Shirt with Name & Number | Foxy Printing',
  seo_desc='A sporty raglan T-shirt for your dog, with their name and number printed on the back if you like. Stretchy cotton, harness slit, sizes XS to 4XL.',
  fields=['Dog’s name (optional)', 'Number (optional)'], tag='dog raglan t-shirt', color='Multicolor',
  html='''<p>Our personalised dog T-shirt is a sporty, baseball-style raglan tee with contrast sleeves, and you can add your dog's name and number on the back. It's a cute gift for a birthday, a new puppy or summer walks in the park.</p>
<h2>Personalised dog T-shirt with optional name and number</h2>
<p>{pers}</p>
<h3>Why you'll love it</h3>
<ul>
<li>Soft jersey fabric with contrast raglan sleeves for a classic baseball look</li>
<li>Lightweight and stretchy (95% cotton, 5% elastane, 190gsm), so they stay cool and move freely</li>
<li>Pullover style: easy on and easy off</li>
<li>Reinforced slit so it goes on over your dog's harness</li>
<li>Adjustable back leg straps keep it in place</li>
<li>Name and number printed in-house for a dog tee that's theirs alone</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>{sizes}</li>
<li>Colours: Black and White, Black, Navy, Navy and White, or Pink and White. 3XL and 4XL come in Black and in Black and White only.</li>
<li>Fabric: 95% cotton, 5% elastane</li>
<li>Care: machine wash at 30°C on a mild cycle. Do not bleach, tumble dry, iron or dry clean.</li>
</ul>
{delivery}
<p>Make it a set with a personalised dog bandana or a name-printed pet bowl.</p>'''),
 'PP002': dict(
  title='Personalised Dog Fleece Hoodie – Optional Name & Number – Black, Grey, Navy or Pink – Sizes XS–4XL',
  seo_title='Personalised Dog Fleece Hoodie | Foxy Printing',
  seo_desc='A cosy fleece-back hoodie for your dog, with their name and number printed on the back if you like. Harness slit, leg straps and sizes XS to 4XL.',
  fields=['Dog’s name (optional)', 'Number (optional)'], tag='dog fleece hoodie', color='Multicolor',
  html='''<p>Our personalised dog fleece hoodie keeps your dog snug on chilly walks, and you can add their name and number on the back. It makes a lovely Christmas or birthday gift for small dogs with big personalities.</p>
<h2>Personalised dog fleece hoodie with optional name and number</h2>
<p>{pers}</p>
<h3>Why you'll love it</h3>
<ul>
<li>Soft, fleece-back jersey (95% cotton, 5% elastane, 300gsm) for cosy winter walks</li>
<li>Ribbed sleeves and a ribbed back hem for a snug, stylish fit</li>
<li>Stretchy pullover style that's easy to put on and take off</li>
<li>Reinforced slit so it goes on over your dog's harness</li>
<li>Adjustable back leg straps stop it riding up</li>
<li>Printed in-house with your dog's name and number</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>{sizes}</li>
<li>Colours: Black, Grey, Navy or Pink. 3XL and 4XL come in Black and Grey only.</li>
<li>Fabric: 95% cotton, 5% elastane</li>
<li>Care: machine wash at 30°C on a mild cycle. Do not bleach, tumble dry, iron or dry clean.</li>
</ul>
{delivery}
<p>Pair this dog hoodie with a personalised pet blanket so they're cosy indoors too.</p>'''),
 'PP003': dict(
  title='Personalised Dog Denim Jacket – Optional Name on the Back – Indigo or Black – Sizes XS–4XL',
  seo_title='Personalised Dog Denim Jacket | Foxy Printing',
  seo_desc='A cool denim jacket for your dog with their name printed on the back if you like. Snap poppers, harness slit and raw-edge sleeves. Sizes XS to 4XL.',
  fields=['Dog’s name (optional)'], tag='dog denim jacket', color='Multicolor',
  html='''<p>Our personalised dog denim jacket gives your dog a laid-back street style, with their name printed on the back if you'd like it. It's a fun gift for a birthday, a new puppy or a dog who loves showing off around the neighbourhood.</p>
<h2>Personalised dog denim jacket with an optional name</h2>
<p>{pers}</p>
<h3>Why you'll love it</h3>
<ul>
<li>Lightweight, stretchy denim (270gsm) so they stay comfortable and move freely</li>
<li>Raw-edge sleeves for a relaxed, worn-in look</li>
<li>Reinforced snap-poppers under the belly: no tricky zips</li>
<li>Reinforced slit so it goes on over your dog's harness</li>
<li>Name printed in-house, so it's a dog jacket nobody else has</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>{sizes}</li>
<li>Colours: Indigo or Black. 3XL and 4XL come in Indigo only.</li>
<li>Fabric: 37% cotton, 32% polyester, 15% viscose, 8% lyocell, 4% acrylic, 4% polyamide</li>
<li>Care: hand wash, maximum 40°C. Do not bleach, tumble dry, iron or dry clean.</li>
</ul>
{delivery}
<p>Looking for more dog clothes? Add a personalised dog bandana for days when it's too warm for a jacket.</p>'''),
 'PP004': dict(
  title='Personalised Dog Puffer Jacket – Optional Name – Black or Grey – Sizes XS–4XL',
  seo_title='Personalised Dog Puffer Jacket | Foxy Printing',
  seo_desc='A warm padded puffer jacket for your dog, with their name printed on the back if you like. Snap poppers, harness slit, leg straps. Sizes XS to 4XL.',
  fields=['Dog’s name (optional)'], tag='dog puffer jacket', color='Multicolor',
  html='''<p>Our personalised dog puffer jacket keeps your dog warm on cold, frosty walks, and you can have their name printed on the back. It's a smart Christmas gift for any dog who feels the chill.</p>
<h2>Personalised dog puffer jacket with an optional name</h2>
<p>{pers} The print panel on a puffer is quite narrow, so shorter names fit best.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Padded, urban-style puffer: nylon shell and lining with a 200gsm polyester filling</li>
<li>Reinforced snap-poppers under the belly: no tricky zips</li>
<li>Reinforced slit so it goes on over your dog's harness</li>
<li>Adjustable back leg straps keep it in place on windy days</li>
<li>Name printed in-house on the back panel</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>{sizes}</li>
<li>Colours: Black or Grey, every size.</li>
<li>Fabric: shell and lining 100% nylon; filling 100% polyester</li>
<li>Care: hand wash, maximum 40°C. Do not bleach, tumble dry, iron or dry clean.</li>
</ul>
{delivery}
<p>Pair this dog coat with a name-printed pet bowl or a personalised pet ID tag for a winter gift set.</p>'''),
 'PP006': dict(
  title='Personalised Dog Parka Jacket – Optional Name – Faux Fur Trim – Khaki or Black – Sizes XS–4XL',
  seo_title='Personalised Dog Parka Jacket | Foxy Printing',
  seo_desc='A padded, faux-fur trimmed parka for your dog, with their name printed on the back if you like. Snap poppers and harness slit. Sizes XS to 4XL.',
  fields=['Dog’s name (optional)'], tag='dog parka', color='Multicolor',
  html='''<p>Our personalised dog parka jacket is a padded winter coat with a plush faux-fur trim, and you can have your dog's name printed on the back. It's perfect for chilly morning walks and makes a thoughtful Christmas gift.</p>
<h2>Personalised dog parka jacket with an optional name</h2>
<p>{pers}</p>
<h3>Why you'll love it</h3>
<ul>
<li>Padded parka with a faux-fur trim for warmth and a smart look</li>
<li>Outer fabric 57% polyester, 43% elastomultiester (166gsm) with polyester filling and lining</li>
<li>Reinforced snap-poppers under the belly: no tricky zips</li>
<li>Reinforced slit so it goes on over your dog's harness</li>
<li>Adjustable back leg straps keep it in place</li>
<li>Name printed in-house for a dog coat that's theirs alone</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>{sizes}</li>
<li>Colours: Khaki or Black, every size.</li>
<li>Fabric: 57% polyester, 43% elastomultiester; filling and lining 100% polyester</li>
<li>Care: hand wash, maximum 40°C. Do not bleach, tumble dry, iron or dry clean.</li>
</ul>
{delivery}
<p>Add a personalised pet blanket to their winter gift so they can warm up after the walk.</p>'''),
 'PP008': dict(
  title='Personalised Dog Football Shirt – Optional Name & Number – 4 Colours – Sizes XS–4XL',
  seo_title='Personalised Dog Football Shirt | Foxy Printing',
  seo_desc='Get your dog match-day ready with a football shirt printed with their name and squad number if you like. Harness loop, leg loops, sizes XS to 4XL.',
  fields=['Dog’s name (optional)', 'Number (optional)'], tag='dog football shirt', color='Multicolor',
  html='''<p>Our personalised dog football shirt gets your dog match-day ready, with their name and squad number on the back if you'd like them. It's great for watch parties, tournament summers and dog walks in your team's colours.</p>
<h2>Personalised dog football shirt with optional name and number</h2>
<p>{pers}</p>
<h3>Why you'll love it</h3>
<ul>
<li>Lightweight, sporty polyester (170gsm) with mesh panels to keep them cool</li>
<li>Pullover style that's easy to put on</li>
<li>Reinforced harness loop for wearing over a harness</li>
<li>Back leg loops keep the shirt secure and comfortable</li>
<li>Name and squad number printed in-house, just like a real kit</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>{sizes}</li>
<li>Colours: White with red and navy trims, Navy with navy and white trims, Red with white and green trims, or Yellow with white and green trims. Every size.</li>
<li>Fabric: body 100% polyester; mesh 100% polyester</li>
<li>Care: machine wash at 30°C on a mild cycle. Do not bleach, tumble dry, iron or dry clean.</li>
</ul>
{delivery}
<p>Make it a match-day set with a personalised dog bandana in the same colours.</p>'''),
}

GARMENT = {'PP001': 'T-shirt', 'PP002': 'hoodie', 'PP003': 'jacket', 'PP004': 'jacket', 'PP006': 'parka', 'PP008': 'shirt'}


def render(code):
    c = C[code]
    pers = (NAME_NUM if len(c['fields']) == 2 else NAME_ONLY).format(g=GARMENT[code])
    return c['html'].format(pers=pers, sizes=SIZES, delivery=DELIVERY)


if __name__ == '__main__':
    import re
    for k, c in C.items():
        h = render(k)
        w = len(re.sub('<[^>]+>', ' ', h).split())
        print(k, w, 'words | title', len(c['title']), '| seo', len(c['seo_title']), '| meta', len(c['seo_desc']), '| h2', h.count('<h2>'))
        open(f'description_{k}.html', 'w').write(h)
