#!/usr/bin/env python3
"""Builds the Foxy Websites site into ./site/ (upload the contents of site/ to the web host).

Pages share one header, footer, stylesheet and script, so edit the content below and re-run:
    python3 build.py
"""
import html, json, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'site')
SITE = 'https://www.foxywebsites.co.uk/'

CO = {
    'legal': 'DepthChargeDesign & Print Ltd',
    'street': 'Unit 1, Balmforth Business Park, Sawmill Lane',
    'town': 'Helmsley', 'city': 'York', 'postcode': 'YO62 5DQ',
    'phone': '01439 771468', 'phone_intl': '+441439771468',
    'email': 'sales@foxyprinting.co.uk',
    'company_no': '09618286', 'vat': 'GB295734264',
}

def e(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------- logos & icons
# Official marks come from Simple Icons (CC0). Brands that have asked for their marks
# to be withheld (Amazon, Adobe/Magento, OpenCart, OnBuy) are shown as plain text.
LOGOS = {
    'shopify': ('Shopify', 'shopify'), 'bigcommerce': ('BigCommerce', 'bigcommerce'),
    'wordpress': ('WordPress', 'wordpress'), 'woocommerce': ('WooCommerce', 'woocommerce'),
    'wix': ('Wix', 'wix'), 'squarespace': ('Squarespace', 'squarespace'),
    'ebay': ('eBay', 'ebay'), 'etsy': ('Etsy', 'etsy'), 'google': ('Google', 'google'),
    'googleads': ('Google Ads', 'googleads'), 'searchconsole': ('Search Console', 'googlesearchconsole'),
    'tiktok': ('TikTok Shop', 'tiktok'), 'facebook': ('Facebook', 'facebook'), 'instagram': ('Instagram', 'instagram'),
    'amazon': ('Amazon', None), 'magento': ('Magento', None), 'opencart': ('OpenCart', None), 'onbuy': ('OnBuy', None),
}
WORDMARKS = {'ebay', 'wix', 'woocommerce'}  # logos that already spell the name
GLYPHS = {
    'amazon': 'A', 'magento': 'M', 'opencart': 'OC', 'onbuy': 'OB',
}
SVGI = {
    'code': 'M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14',
    'wrench': 'M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.4-.6-.6-2.4z',
    'move': 'M4 7h14l-3-3M20 17H6l3 3',
    'list': 'M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01',
    'team': 'M8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM16 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM2 20c0-3 2.7-5 6-5s6 2 6 5M14 15.2c.6-.1 1.3-.2 2-.2 3.3 0 6 2 6 5',
    'mail': 'M3 6h18v12H3zM3 7l9 6 9-6',
}

def mi(key, rel):
    """Small square icon used in menus and cards."""
    if key in SVGI:
        return ('<span class="mi"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" '
                'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                f'<path d="{SVGI[key]}"/></svg></span>')
    title, f = LOGOS[key]
    if f:
        return f'<span class="mi"><img src="{rel}logos/{f}.svg" alt=""></span>'
    return f'<span class="mi"><b>{GLYPHS[key]}</b></span>'

def tile(key, rel, href=None):
    title, f = LOGOS[key]
    if f in WORDMARKS:
        inner = f'<img src="{rel}logos/{f}.svg" alt="{e(title)} logo" height="24">'
    elif f:
        inner = f'<img src="{rel}logos/{f}.svg" alt="{e(title)} logo" height="24"><span>{e(title)}</span>'
    else:
        inner = f'<b>{e(title)}</b>'
    cls = 'logo-tile' + ('' if f else ' txt')
    if href:
        return f'<a class="{cls}" href="{rel}{href}">{inner}</a>'
    return f'<span class="{cls}">{inner}</span>'

# ---------------------------------------------------------------- service pages
PAGES = [
  dict(slug='shopify-websites', nav='Shopify', sub='Shops, themes, apps and channels', icon='shopify', group='web',
    c='var(--leaf)', logos=['shopify'],
    title='Shopify Web Design & Store Setup | Foxy Websites',
    desc='Shopify web design, store setup, custom themes and apps from a UK design team with 30 years of experience. Fixed-price quotes, real people, Helmsley, North Yorkshire.',
    eyebrow='Shopify websites', h1='Shopify shops that look good and <em>sell</em>.',
    lede='From a brand-new store to a full redesign, we set up Shopify properly: the theme, the product pages, payments, delivery and the sales channels that put your products on Google, Facebook and TikTok.',
    glance=['Store setup from scratch or a redesign','Custom theme sections and product pages','Payments, shipping, tax and apps','Google, Shop, Facebook and TikTok channels','Product personalisers with live previews'],
    intro_h='Shopify web design, done properly',
    intro=['Shopify is the platform we build on most, because it lets small teams run a serious online shop without worrying about servers or security patches. The catch is that a default theme and a few apps only get you so far. Shops that sell well have product pages that answer every question, clear delivery information and collections that make browsing easy.',
           'Our design team plans the shop around how your customers buy. We set up the structure, design the pages, load and tidy your products, and connect the sales channels. If you sell personalised products, we can build a live preview so customers see their name, photo or logo on the product before they order.',
           'We run our own Shopify shop, Foxy Printing, with a custom product designer and thousands of products, so we know where shops tend to go wrong and how to fix it.'],
    aside_h='Good fit if you...', aside=['are starting a new online shop','have outgrown a free theme','sell on eBay or Etsy and want your own site','need personalised or made-to-order products','want Google Shopping set up from day one'],
    feat_h='What we do on Shopify',
    feats=[('Store setup','Domain, payments, shipping profiles, tax, policies and checkout settings, all set up and tested with real orders.'),
           ('Theme design','A theme chosen to suit your range, then customised with your branding and custom sections where the theme falls short.'),
           ('Product pages','Layouts, size guides, delivery info, variants and photos that answer buyers\' questions before they ask.'),
           ('Collections & filters','Menus, collections and filters that make big ranges easy to browse on a phone.'),
           ('Apps & integrations','Only the apps you need, set up properly: reviews, bundles, subscriptions, print-on-demand and accounting.'),
           ('Sales channels','Google & YouTube, Shop, Facebook & Instagram and TikTok channels connected to your catalogue.')],
    why=[('Built to sell','Every page is designed around what makes a customer buy, not just what looks nice in a mock-up.'),
         ('You can run it','We hand over a shop you can edit yourself, with a short walkthrough of the bits you\'ll use every day.'),
         ('Fixed price','You get a clear list of what we\'ll do and a fixed quote before we start.')],
    faqs=[('How long does a Shopify store take?','A straightforward shop with up to a few hundred products usually takes two to four weeks, depending on how quickly we get your content and decisions. Bigger catalogues and custom features take longer, and we agree the timeline in your quote.'),
          ('Do I need to pay for Shopify separately?','Yes. The Shopify subscription, any paid apps and your theme are paid to Shopify directly, so the shop stays in your name. We help you pick the right plan.'),
          ('Can you move my existing shop to Shopify?','Yes. We move products, customers and order history from WooCommerce, Magento, BigCommerce, Wix or eBay, and set up redirects so you keep your Google rankings.'),
          ('Can customers personalise products?','Yes. We can add personalisation fields or build a full product designer with a live preview, like the leavers hoodie designer on our own shop.')],
    related=['google-shopping-merchant-center','website-migrations','product-listing-seo'], cta_p='Shopify'),

  dict(slug='bigcommerce-websites', nav='BigCommerce', sub='Big catalogues and B2B', icon='bigcommerce', group='web',
    c='var(--sky)', logos=['bigcommerce'],
    title='BigCommerce Web Design & Development | Foxy Websites',
    desc='BigCommerce store design, Stencil theme work, bulk product imports and multi-channel selling for larger catalogues and trade customers. UK design team, fixed-price quotes.',
    eyebrow='BigCommerce websites', h1='BigCommerce stores for <em>bigger</em> catalogues.',
    lede='BigCommerce handles large ranges, lots of variants and trade pricing well. We design and build the store, import your products in bulk and connect it to eBay, Amazon and Google.',
    glance=['Store build and Stencil theme design','Bulk product and category imports','Customer groups and trade price lists','eBay, Amazon and Google channels','Order and stock reporting'],
    intro_h='When BigCommerce is the right choice',
    intro=['BigCommerce suits businesses with thousands of products, complicated options or trade customers who need their own prices. It includes features that other platforms charge apps for, such as customer groups, price lists and built-in marketplace channels.',
           'Our design team builds BigCommerce stores on the Stencil theme framework, so the design is fully yours and still easy to update. We import your catalogue with clean categories, options and images, then connect the channels you sell on.',
           'We also look after existing BigCommerce stores: fixing theme problems, speeding up slow pages, cleaning up product data and sorting Google Shopping feeds.'],
    aside_h='Good fit if you...', aside=['have thousands of products or variants','sell to trade and retail customers','need multi-channel selling built in','want fewer monthly app costs','already run BigCommerce and need help'],
    feat_h='What we do on BigCommerce',
    feats=[('Store build','Settings, payments, shipping zones, tax and checkout set up and tested end to end.'),
           ('Stencil theme work','A custom design built on a Stencil theme, with your branding, layouts and product templates.'),
           ('Bulk imports','Products, categories, options and images imported from spreadsheets or your old platform.'),
           ('Trade pricing','Customer groups, price lists and account sign-up for trade buyers.'),
           ('Multi-channel','eBay, Amazon, Google and social channels connected so stock stays in step.'),
           ('Ongoing support','Theme fixes, speed improvements, data clean-ups and new features as you grow.')],
    why=[('Large ranges handled','We\'re used to catalogues with thousands of products and messy supplier data.'),
         ('One stock list','Sell on your site and the marketplaces without overselling.'),
         ('Clear handover','Your team gets a store they understand and can manage day to day.')],
    faqs=[('Is BigCommerce better than Shopify?','It depends on your range and customers. BigCommerce is often better for large catalogues and trade pricing; Shopify is often simpler for smaller shops. We\'ll recommend the one that suits you.'),
          ('Can you import products from a spreadsheet?','Yes. We clean and map your spreadsheet or supplier feed into BigCommerce\'s import format, including options, images and categories.'),
          ('Can trade customers see different prices?','Yes. We set up customer groups and price lists so approved trade accounts see their own pricing.'),
          ('Do you work on existing BigCommerce stores?','Yes. Send us the store link and what\'s wrong, and we\'ll take a look before quoting.')],
    related=['product-listing-seo','amazon-seller-setup','ebay-shop-design'], cta_p='BigCommerce'),

  dict(slug='wordpress-woocommerce-websites', nav='WordPress & WooCommerce', sub='Sites and shops you can edit', icon='wordpress', group='web',
    c='var(--berry)', logos=['wordpress','woocommerce'],
    title='WordPress & WooCommerce Web Design | Foxy Websites',
    desc='WordPress websites and WooCommerce shops designed and built by a UK team with 30 years of experience. Custom themes, security, backups and SEO. Fixed-price quotes.',
    eyebrow='WordPress & WooCommerce', h1='WordPress sites and WooCommerce shops you can <em>run yourself</em>.',
    lede='Business websites, blogs and online shops on WordPress, designed to your brand, built to be fast and secure, and simple for you to update.',
    glance=['Custom WordPress themes and page layouts','WooCommerce shops and payments','Plugins set up properly, not piled up','Security, backups and updates','Blog and SEO structure'],
    intro_h='WordPress websites without the plugin mess',
    intro=['WordPress runs a huge share of the web because it is flexible and you own everything. That flexibility is also where it goes wrong: too many plugins, a heavy page builder and no updates soon add up to a slow, fragile site.',
           'Our design team builds lean WordPress sites. We design the pages around your content, choose a small set of reliable plugins, and set up security, backups and updates from the start. For shops we use WooCommerce, with payments, delivery and product pages set up to sell.',
           'Already have a WordPress site that has become slow or broken? We can tidy it up, update it safely or rebuild it on a cleaner setup.'],
    aside_h='Good fit if you...', aside=['want a business website with a blog','need to own and host your own site','already use WordPress and want it sorted','want a shop with lots of content around it','need custom features or integrations'],
    feat_h='What we do on WordPress',
    feats=[('Custom design','Pages designed around your business and content, then built on a lightweight theme.'),
           ('WooCommerce shops','Products, payments, delivery, tax and emails set up and tested with real orders.'),
           ('Plugins done right','A short list of trusted plugins instead of dozens that slow the site down.'),
           ('Security & backups','Firewall, spam protection, automatic backups and safe updates.'),
           ('SEO structure','Clean URLs, page titles, descriptions, sitemaps and structured data set up.'),
           ('Training','A short walkthrough so you can add pages, posts and products yourself.')],
    why=[('Fast and lean','Fewer plugins and lighter pages mean faster loading and fewer things to break.'),
         ('Yours to keep','You own the site, the hosting and the content. No lock-in.'),
         ('Looked after','Optional care plans keep updates, backups and fixes taken care of.')],
    faqs=[('Should I use WordPress or Shopify?','WordPress suits content-heavy sites and businesses that want full ownership. Shopify is usually simpler for shops that mostly sell products. We\'ll help you decide.'),
          ('Can you fix my slow WordPress site?','Yes. We look at hosting, plugins, images and caching, fix what\'s slowing it down and keep everything backed up while we work.'),
          ('Do you provide hosting?','We can recommend and set up reliable UK hosting in your name, or work with your existing host.'),
          ('Can I edit the site myself?','Yes. We build it so you can change text, images, pages and products without touching code.')],
    related=['website-repairs','website-migrations','product-listing-seo'], cta_p='WordPress'),

  dict(slug='wix-squarespace-websites', nav='Wix & Squarespace', sub='Quick sites for local businesses', icon='wix', group='web',
    c='var(--fox)', logos=['wix','squarespace'],
    title='Wix & Squarespace Website Design | Foxy Websites',
    desc='Professional Wix and Squarespace website design for trades, makers and local businesses. Bookings, forms, simple shops and Google Business Profile set up. Fixed-price quotes.',
    eyebrow='Wix & Squarespace', h1='Good-looking sites for <em>local businesses</em>, fast.',
    lede='When you need a professional website quickly and want to edit it yourself, Wix and Squarespace are a great choice. We design it, write it with you and get it found on Google.',
    glance=['Design and build from your content','Bookings, enquiry forms and simple shops','Google Business Profile set up','Domain and business email','Basic SEO and Google Search Console'],
    intro_h='A proper design on an easy platform',
    intro=['Wix and Squarespace make it easy to keep your own website up to date. What they don\'t do is decide what your site should say, how it should look or how people will find it. That\'s where most DIY sites fall down.',
           'Our design team plans the pages, designs them to match your brand, and helps you write clear text that tells customers what you do and how to get in touch. We set up bookings, forms or a small shop if you need one, and connect your Google Business Profile so you show up in local searches.',
           'It\'s ideal for trades, salons, cafés, makers and small service businesses that want to look professional without a big budget.'],
    aside_h='Good fit if you...', aside=['are a trade or local service business','want to update the site yourself','need bookings or enquiry forms','sell a small range of products','want to be found on Google Maps'],
    feat_h='What we do on Wix and Squarespace',
    feats=[('Page design','Home, services, gallery, about and contact pages designed to your brand.'),
           ('Copy help','We help you write clear, friendly text that explains what you do.'),
           ('Bookings & forms','Online booking, enquiry forms and quote requests that land in your inbox.'),
           ('Simple shops','A small online shop with payments and delivery for a focused range.'),
           ('Local SEO','Google Business Profile, Search Console and local keywords set up.'),
           ('Domain & email','Your domain connected and a business email address set up.')],
    why=[('Quick to launch','Most small sites are live within a couple of weeks of getting your content.'),
         ('Easy to edit','Change your prices, photos and opening times yourself.'),
         ('Room to grow','If you outgrow it later, we can move you to Shopify or WordPress.')],
    faqs=[('Wix or Squarespace: which is better?','Squarespace has polished templates and suits image-led businesses. Wix is more flexible for bookings and add-ons. We\'ll suggest the better fit for what you need.'),
          ('Can you redesign my existing Wix site?','Yes. We can refresh the design, rewrite pages and fix SEO problems on your current site.'),
          ('Will it show up on Google?','We set up the basics properly: page titles, descriptions, Search Console and your Google Business Profile. Rankings take time, but your site will be set up to be found.'),
          ('Who pays for the Wix or Squarespace plan?','You do, directly, so the site stays in your name. We help you choose the right plan.')],
    related=['shopify-websites','custom-websites','website-repairs'], cta_p='Wix'),

  dict(slug='magento-opencart-support', nav='Magento & OpenCart', sub='Support or a safe move off', icon='magento', group='web',
    c='var(--red)', logos=['magento','opencart'],
    title='Magento & OpenCart Support and Migration | Foxy Websites',
    desc='Help with older Magento and OpenCart shops: fixes, updates and extension problems, or a safe move to Shopify or BigCommerce with your products, customers and Google rankings kept.',
    eyebrow='Magento & OpenCart', h1='Older shop systems, <em>kept running</em> or moved safely.',
    lede='Magento and OpenCart shops can be costly to keep secure and up to date. We fix what\'s broken today, and when you\'re ready, move you to a modern platform without losing products, customers or rankings.',
    glance=['Fixes, updates and extension problems','Security clean-ups','Moves to Shopify or BigCommerce','Products, customers and orders carried over','301 redirects to protect Google rankings'],
    intro_h='Support for shops that still need to trade',
    intro=['Many businesses still run on Magento 1, Magento 2 or OpenCart. They often work, but updates are hard, developers are expensive and extensions break when anything changes. Older versions no longer get security updates at all.',
           'Our design team can stabilise your shop first: fixing errors, broken checkouts and extension conflicts, and cleaning up after hacks. Then we can plan a move to Shopify or BigCommerce, carrying over your products, customers and order history.',
           'The most important part of a move is keeping your Google rankings. We map every old URL to its new page with 301 redirects, so customers and Google land in the right place.'],
    aside_h='Signs it\'s time to move', aside=['your version no longer gets security updates','small changes cost a lot of developer time','extensions break after updates','the site is slow on phones','hosting bills keep going up'],
    feat_h='What we do',
    feats=[('Urgent fixes','Checkout errors, white screens, broken extensions and email problems sorted.'),
           ('Security clean-up','Malware removed, passwords reset, and the holes that let it in closed.'),
           ('Migration plan','A clear plan for what moves, what changes and when, with a test site first.'),
           ('Data transfer','Products, images, categories, customers and order history carried across.'),
           ('Redirects & SEO','Every old URL mapped with 301 redirects so rankings and links keep working.'),
           ('Launch & checks','We go live together and check orders, emails and Google afterwards.')],
    why=[('Nothing lost','Products, customers and history come with you.'),
         ('Rankings protected','Redirects and checks so Google traffic carries on.'),
         ('Lower running costs','Hosted platforms usually mean fewer developer and server bills.')],
    faqs=[('Can you keep my Magento shop running for now?','Yes. We can fix urgent problems and keep it stable while you decide what to do next.'),
          ('Will I lose my Google rankings if I move?','Not if it\'s done properly. We map every old page to a new one with 301 redirects and check Search Console after launch.'),
          ('Can customer accounts move too?','Customer details and order history can move. For security, customers usually set a new password the first time they log in.'),
          ('How long does a migration take?','Most moves take four to eight weeks, depending on the size of the catalogue and any custom features.')],
    related=['website-migrations','shopify-websites','bigcommerce-websites'], cta_p='Magento'),

  dict(slug='custom-websites', nav='Hand-built websites', sub='Custom code, tools and integrations', icon='code', group='web',
    c='var(--sun)', logos=[],
    title='Custom Website Design & Development | Foxy Websites',
    desc='Hand-built websites, landing pages, product designers, calculators and custom integrations from a UK design team. Fast, lightweight and built for your exact needs.',
    eyebrow='Hand-built websites', h1='Custom-coded sites when a platform <em>gets in the way</em>.',
    lede='Sometimes a platform is overkill, or can\'t do what you need. We hand-build fast websites, landing pages and custom tools like product designers, quote calculators and integrations.',
    glance=['Landing pages and one-page sites','Product designers with live previews','Quote and price calculators','Custom integrations and APIs','Hosting, SSL and speed tuning'],
    intro_h='Built for exactly what you need',
    intro=['Hand-built websites load quickly, have no monthly platform fees and do exactly what you need, nothing more. They\'re ideal for landing pages, campaign sites and small business sites that rarely change.',
           'We also build custom tools that plug into your existing shop. Our own Foxy Printing shop uses a product designer we built, where customers add names, fonts and logos to a hoodie, see it on real photos and order, and print-ready files are made automatically.',
           'If your shop needs something no app does well, such as a price calculator, a custom checkout step or a link to your supplier\'s system, we can build it.'],
    aside_h='Good fit if you need...', aside=['a fast landing page for a campaign','a product designer or personaliser','a price or quote calculator','to connect two systems together','a site with no platform fees'],
    feat_h='What we build',
    feats=[('Landing pages','Fast, focused pages for adverts and launches, built to turn visits into enquiries.'),
           ('Small business sites','Lightweight sites with a few pages that load instantly and cost little to host.'),
           ('Product designers','Customers personalise products, preview them and order, with print files made automatically.'),
           ('Calculators','Price, quote and size calculators that do the maths for your customers.'),
           ('Integrations','Connect your shop to suppliers, accounts software, spreadsheets or marketplaces.'),
           ('Hosting & speed','Hosting, SSL, caching and image optimisation set up for fast pages.')],
    why=[('Fast','No heavy platform code, so pages load quickly on any phone.'),
         ('Exactly right','Built around your process instead of bending to a template.'),
         ('Proven','We use the same tools on our own shop every day.')],
    faqs=[('Can I edit a hand-built site?','For sites that change often we\'ll recommend a platform instead. For sites that rarely change, we make updates for you quickly on a care plan.'),
          ('Can you add a custom tool to my Shopify shop?','Yes. We build designers, calculators and integrations that work inside Shopify and other platforms.'),
          ('Do you host the site?','We can set up hosting in your name or use your existing host. Hand-built sites are cheap to host.'),
          ('How much does a landing page cost?','It depends on the content and features. We give a fixed price once we know what you need.')],
    related=['shopify-websites','product-listing-seo','wix-squarespace-websites'], cta_p='Custom'),

  dict(slug='ebay-shop-design', nav='eBay', sub='Shop design, templates and bulk listing', icon='ebay', group='market',
    c='var(--red)', logos=['ebay'],
    title='eBay Shop Design, Listing Templates & Bulk Listing | Foxy Websites',
    desc='eBay shop creation, store design, mobile-friendly listing templates and bulk listing by upload file. Shopify to eBay connectors and listing error fixes. UK design team.',
    eyebrow='eBay shops', h1='eBay shops that look like a <em>proper brand</em>.',
    lede='From opening your eBay Store to thousands of live listings. We design the shop, build a listing template that works on phones, load your products in bulk and connect it all to your website.',
    glance=['eBay Store creation and setup','Shop logo, billboard and description','Mobile-friendly listing template','Bulk listing with item specifics','Shopify to eBay stock sync'],
    intro_h='eBay shop design and listing, start to finish',
    intro=['eBay still brings in a huge number of buyers, but it\'s strict about how listings are built. Templates with active content, missing item specifics or contact details in descriptions can get listings blocked or buried in search.',
           'Our design team sets up your eBay Store properly: business policies, store categories, a branded logo and billboard, and a listing template designed to eBay\'s current rules that looks good on a phone. Then we write and load your products in bulk using eBay\'s upload templates, with item specifics filled in so buyers can find them.',
           'If you also sell on your own website, we connect the two so stock, prices and orders stay in step. We\'ve built and loaded large eBay ranges for our own business, so we know the pitfalls.'],
    aside_h='Good fit if you...', aside=['are opening an eBay Store','want your eBay shop to match your brand','have hundreds or thousands of items to list','keep overselling between eBay and your site','have listings blocked or hidden'],
    feat_h='What we do on eBay',
    feats=[('Shop creation','Store subscription, business policies, returns, postage and store categories set up properly.'),
           ('Shop design','Store logo, billboard banner and description that match your website.'),
           ('Listing template','A clean, mobile-friendly product description template that follows eBay\'s rules.'),
           ('Bulk listing','Products written and loaded by upload file, with titles, item specifics and photos.'),
           ('Connectors','Shopify, BigCommerce or WooCommerce linked to eBay for stock, prices and orders.'),
           ('Listing fixes','Policy blocks, missing item specifics, VeRO notices and image problems sorted.')],
    why=[('Rules followed','Templates and listings built to eBay\'s current policies.'),
         ('Found in search','Titles and item specifics written the way buyers search.'),
         ('Fast at volume','Large ranges loaded in bulk, not one listing at a time.')],
    faqs=[('Can you design my eBay shop?','Yes. We create your store logo, billboard banner, description and categories, and a listing template that matches your brand.'),
          ('Can you list thousands of products?','Yes. We prepare your products in eBay\'s bulk upload format, with item specifics and photos, and load them in batches.'),
          ('Can eBay and my website share stock?','Yes. We set up a connector app so an item sold on one channel comes off stock on the other.'),
          ('Why are my eBay listings being blocked?','Common causes are links or contact details in the description, active content in templates, missing item specifics or brand rights issues. We find the cause and fix it.')],
    related=['amazon-seller-setup','etsy-shop-setup','product-listing-seo'], cta_p='eBay'),

  dict(slug='amazon-seller-setup', nav='Amazon', sub='Seller Central, listings and connectors', icon='amazon', group='market',
    c='var(--sun)', logos=['amazon'],
    title='Amazon Seller Setup & Product Listing Service | Foxy Websites',
    desc='Amazon Seller Central setup, product listing with category templates and feeds, Shopify to Amazon connectors, A+ content and suppressed listing fixes. UK design team.',
    eyebrow='Amazon selling', h1='Amazon set up <em>right</em> the first time.',
    lede='Amazon is strict about how products are listed. We handle Seller Central, the listing files and the connectors, so your products go live without being suppressed.',
    glance=['Seller Central account setup','Listings built from Amazon\'s templates','Shopify and WooCommerce connectors','A+ content and Brand Store','Personalised products with Amazon Custom'],
    intro_h='Amazon product listing without the headaches',
    intro=['Selling on Amazon can add a big new stream of orders, but listing there is very different from your own shop. Each category has its own template and required attributes, and a missing value can stop a product appearing at all.',
           'Our design team sets up your Seller Central account, shipping templates and business details, then builds your listings from Amazon\'s category templates or listing feeds. We write titles, bullet points and descriptions that follow Amazon\'s style rules and the words buyers search for.',
           'If you\'re brand registered, we design A+ content and a Brand Store. If you sell personalised items, we set up Amazon Custom so customers can add names, text or photos. And we link Amazon to your website so stock and orders stay in sync.'],
    aside_h='Good fit if you...', aside=['are new to selling on Amazon','have products stuck as suppressed','want listings that follow Amazon\'s rules','sell personalised products','need Amazon linked to your website'],
    feat_h='What we do on Amazon',
    feats=[('Seller Central setup','Account, business details, shipping templates and tax settings.'),
           ('Product listing','Listings built from Amazon\'s category templates and listing feeds, with every required attribute.'),
           ('Amazon connectors','Shopify, BigCommerce or WooCommerce linked to Amazon for stock and orders.'),
           ('A+ content & Brand Store','Rich product pages and a branded storefront for registered brands.'),
           ('Amazon Custom','Personalisation options set up for names, text and photos.'),
           ('Suppressed listings','Missing attributes, image and category errors found and fixed.')],
    why=[('Done to Amazon\'s rules','Listings built the way Amazon expects, so they go live first time.'),
         ('Written to sell','Titles and bullet points written for buyers, not keyword lists.'),
         ('Joined up','Amazon, your website and other marketplaces working from one stock list.')],
    faqs=[('Can you set up my Amazon seller account?','We guide you through registration, which Amazon requires the business owner to complete, then set up shipping, business details and listings.'),
          ('Why are my Amazon listings suppressed?','Usually a missing required attribute, an image that breaks the rules or the wrong category. We check the listing quality report and fix each one.'),
          ('Can you list personalised products on Amazon?','Yes. We set up Amazon Custom so buyers can add text, names or photos when they order.'),
          ('Can Amazon orders come into Shopify?','Yes. We set up a connector so stock and orders flow between Amazon and your shop.')],
    related=['ebay-shop-design','etsy-shop-setup','product-listing-seo'], cta_p='Amazon'),

  dict(slug='etsy-shop-setup', nav='Etsy', sub='Shop setup, SEO and sync', icon='etsy', group='market',
    c='var(--fox)', logos=['etsy'],
    title='Etsy Shop Setup, Branding & Listing SEO | Foxy Websites',
    desc='Etsy shop setup, banners and branding, listings with titles and all 13 tags written for Etsy search, personalisation options and Etsy to Shopify sync. UK design team.',
    eyebrow='Etsy shops', h1='Etsy shops that <em>get found</em>.',
    lede='Etsy rewards good titles, tags and photos. We set up your shop, design the branding, write listings that match what buyers search for, and connect it to your own website.',
    glance=['Shop setup, policies and delivery','Banner, shop icon and About page','Titles and all 13 tags for Etsy search','Personalisation and variations','Etsy and Shopify sync'],
    intro_h='Etsy shop setup and listing SEO',
    intro=['Etsy is brilliant for handmade, personalised and vintage products, but it\'s crowded. Shops that do well have a clear brand, great photos and listings written the way buyers search.',
           'Our design team sets up your shop sections, policies, payments and delivery profiles, and designs a banner, shop icon and About page that tell your story. We write each listing with a clear title, all 13 tags and a description that answers buyers\' questions.',
           'Personalised products need clear options, so we set up personalisation boxes and variations that are easy to fill in. If you also run your own website, we link the two so you can manage stock in one place.'],
    aside_h='Good fit if you...', aside=['are opening a new Etsy shop','sell handmade or personalised gifts','have listings that don\'t get views','want a shop that matches your brand','sell on Etsy and your own site'],
    feat_h='What we do on Etsy',
    feats=[('Shop setup','Shop name, sections, policies, payments and delivery profiles.'),
           ('Shop branding','Banner, shop icon and About page that tell your story.'),
           ('Listings & SEO','Titles, all 13 tags and descriptions written for Etsy search.'),
           ('Personalisation','Personalisation boxes and variations for names, colours and sizes.'),
           ('Etsy ↔ Shopify sync','Stock and orders managed from one place.'),
           ('Bulk uploads','Large ranges loaded quickly instead of one listing at a time.')],
    why=[('Search-led','Every listing written around the words buyers actually use.'),
         ('On-brand','Your Etsy shop looks like the same business as your website.'),
         ('Time saved','Bulk tools and sync mean less copying between channels.')],
    faqs=[('Can you write my Etsy tags and titles?','Yes. We research the phrases buyers use and write titles and all 13 tags for each listing.'),
          ('Can you design my Etsy banner and logo?','Yes. We design the banner, shop icon and listing images to match your brand.'),
          ('Can Etsy link to my Shopify shop?','Yes. We set up an integration so products and stock stay in step across both.'),
          ('Do you take photos?','We can place your designs onto real product photos and create clean listing images. For new product photography, we\'ll advise on what you need.')],
    related=['ebay-shop-design','amazon-seller-setup','shopify-websites'], cta_p='Etsy'),

  dict(slug='google-shopping-merchant-center', nav='Google Shopping', sub='Merchant Center, feeds and fixes', icon='google', group='market',
    c='var(--sky)', logos=['google','googleads','searchconsole'],
    title='Google Shopping & Merchant Center Setup and Fixes | Foxy Websites',
    desc='Google Merchant Center setup, product feeds, disapproval fixes and misrepresentation suspension help. Free listings and Shopping ads set up by a UK design team.',
    eyebrow='Google Shopping', h1='Your products on Google, <em>approved</em> and showing.',
    lede='Shoppers compare products on Google before they buy. We set up Merchant Center, clean up your product feed, fix disapprovals and suspensions, and get you into free listings and Shopping ads.',
    glance=['Merchant Center setup and verification','Clean product feeds from your shop','Disapproval and warning fixes','Misrepresentation suspension help','Free listings and Shopping ads'],
    intro_h='Google Merchant Center, set up and fixed',
    intro=['Google Shopping can send steady, ready-to-buy traffic to your shop, including free product listings that cost nothing per click. But Merchant Center is strict. Missing barcodes, price mismatches, unclear returns pages or contact details can get products disapproved, or the whole account suspended.',
           'Our design team sets up Merchant Center, verifies your website, and connects a clean product feed from Shopify, BigCommerce or WooCommerce. We set the right identifiers, categories, delivery and returns settings so products are approved.',
           'If your account has been suspended for misrepresentation, we review your site the way Google does: business details, policies, checkout, pricing and product claims. We fix the causes on your site first, then request the review.'],
    aside_h='Common problems we fix', aside=['Account suspended for misrepresentation','Missing value [gtin] or brand','Price or availability mismatch','Images too small or with overlays','Missing delivery or returns settings'],
    feat_h='What we do on Google',
    feats=[('Merchant Center setup','Account, website verification, business details, delivery and returns settings.'),
           ('Product feeds','Clean feeds from your shop with titles, categories, GTINs and brand set correctly.'),
           ('Disapproval fixes','Identifiers, prices, images and landing page errors found and fixed.'),
           ('Suspension help','Misrepresentation and policy problems fixed on your site, then reviewed.'),
           ('Shopping ads','Performance Max and Shopping campaigns set up with conversion tracking.'),
           ('Search Console','Your site connected to Google Search Console, sitemaps submitted and errors checked.')],
    why=[('We fix the cause','Not just the feed: the website problems behind the warnings too.'),
         ('Free listings first','Get products showing for free before spending on ads.'),
         ('Tested on our own shop','We manage Google Shopping for our own large catalogue.')],
    faqs=[('Why was my Merchant Center account suspended?','The most common reason is misrepresentation: Google couldn\'t confirm who you are or found unclear policies, pricing or claims. We review the site, fix the issues and request a review.'),
          ('What does "Missing value [gtin]" mean?','Google wants a barcode for branded products. We add the right GTINs, or mark your own-made products correctly so they don\'t need one.'),
          ('Are Google Shopping listings free?','Yes, free listings are available alongside paid Shopping ads. We set up both, starting with free listings.'),
          ('How long does a suspension review take?','Google usually replies within a few days to a couple of weeks. The important thing is to fix the causes before requesting it.')],
    related=['website-repairs','shopify-websites','product-listing-seo'], cta_p='Google Shopping', console=True),

  dict(slug='social-shops-tiktok-facebook-instagram', nav='TikTok, Facebook & Instagram', sub='Social shops and more marketplaces', icon='tiktok', group='market',
    c='var(--leaf)', logos=['tiktok','facebook','instagram','onbuy'],
    title='TikTok Shop, Facebook & Instagram Shop Setup | Foxy Websites',
    desc='TikTok Shop, Facebook and Instagram shop setup with your product catalogue synced from your website. Plus OnBuy and Google Business Profile. UK design team.',
    eyebrow='Social shops & more', h1='Sell where people <em>scroll</em>.',
    lede='TikTok Shop, Facebook and Instagram let people buy without leaving the app. We connect your catalogue, set up the shops and keep everything in sync with your website.',
    glance=['TikTok Shop seller setup','Facebook & Instagram Shops','Catalogue synced from your website','OnBuy and other UK marketplaces','Google Business Profile with products'],
    intro_h='Social shops connected to your website',
    intro=['More and more shopping starts on social media. A product spotted in a TikTok video or an Instagram post can be bought in a couple of taps, if your shop is connected.',
           'Our design team sets up your TikTok Shop and Meta commerce account, connects your product catalogue from Shopify or another platform, and makes sure products are approved and tagged ready for posts and videos.',
           'We also set up other places to sell, such as OnBuy, and your Google Business Profile with products, so local customers find you on Google Maps.'],
    aside_h='Good fit if you...', aside=['post products on social media','want customers to buy inside the app','already sell on Shopify','want more UK marketplaces','need everything managed from one place'],
    feat_h='What we do',
    feats=[('TikTok Shop','Seller account, product catalogue, shipping settings and Shopify link.'),
           ('Facebook & Instagram Shops','Catalogue synced and products ready to tag in posts and reels.'),
           ('Catalogue clean-up','Titles, images and categories fixed so products get approved.'),
           ('OnBuy','UK marketplace account and listings set up.'),
           ('Google Business Profile','Your business on Google Maps with products, photos and reviews.'),
           ('One order screen','Orders from every channel landing in one place.')],
    why=[('Joined up','Every channel runs from your main product catalogue.'),
         ('Approved first time','Catalogue data cleaned so products pass each platform\'s checks.'),
         ('Less admin','Stock and orders in one place instead of five.')],
    faqs=[('Can you set up TikTok Shop in the UK?','Yes. We help you register, connect your catalogue and set up shipping and returns.'),
          ('Do I need Shopify for social shops?','No, but it makes syncing much easier. We can also connect BigCommerce and WooCommerce catalogues.'),
          ('Can products be tagged in Instagram posts?','Yes, once your shop is approved, products can be tagged in posts, reels and stories.'),
          ('What is OnBuy?','OnBuy is a UK online marketplace, similar to Amazon and eBay. It can be a useful extra channel for some products.')],
    related=['shopify-websites','google-shopping-merchant-center','ebay-shop-design'], cta_p='TikTok Shop'),

  dict(slug='website-repairs', nav='Website repairs', sub='Broken sites, hacks and errors', icon='wrench', group='fix',
    c='var(--red)', logos=['shopify','wordpress','woocommerce','bigcommerce','wix','squarespace'],
    title='Website Repair & Fix Service: Broken, Hacked or Slow Sites | Foxy Websites',
    desc='Website repairs for broken, hacked or slow sites on Shopify, WordPress, WooCommerce, BigCommerce, Wix and more. Checkout errors, SSL warnings and email problems fixed. UK team.',
    eyebrow='Website repairs', h1='Broken website? <em>We\'ll fix it.</em>',
    lede='Send us the error message, a screenshot, or just "it\'s stopped working". We find the cause, fix it, and tell you in plain English what went wrong.',
    glance=['Site down or white screen','Checkout not taking payments','Hacked sites and malware','"Not secure" SSL warnings','Slow pages and email problems'],
    intro_h='Website fixes on any platform',
    intro=['When your website or shop breaks, every hour costs you orders and trust. It might be a theme update that broke the layout, a plugin conflict, a payment gateway that stopped working, an expired SSL certificate or a hack.',
           'Our design team has been fixing websites for 30 years, on everything from hand-coded HTML to Shopify, WordPress, WooCommerce, BigCommerce, Magento, Wix and Squarespace. We work out what changed, fix the cause and check everything else still works.',
           'Once it\'s fixed, we explain what happened and how to stop it happening again, whether that\'s updates, backups, better hosting or a care plan.'],
    aside_h='Things we fix every week', aside=['White screen or error 500','Checkout or payment failures','Theme or plugin update problems','Hacked site and spam pages','Domain, DNS and email issues'],
    feat_h='What we fix',
    feats=[('Site down','White screens, error 500s, database errors and hosting problems.'),
           ('Checkout & payments','Payment gateways, shipping rates, tax and order email problems.'),
           ('Layout broken','Theme updates, plugin conflicts and pages that look wrong on phones.'),
           ('Hacks & malware','Malware removed, spam pages cleared, passwords reset and security tightened.'),
           ('SSL & speed','"Not secure" warnings fixed and slow pages sped up.'),
           ('Domain & email','DNS, domain renewals and business email that stopped working.')],
    why=[('Plain English','We tell you what went wrong and what we did, without jargon.'),
         ('Any platform','Shopify, WordPress, BigCommerce, Wix, Magento or hand-coded.'),
         ('Prevention','Backups, updates and monitoring so it doesn\'t happen again.')],
    faqs=[('How quickly can you fix my website?','Urgent problems like a site being down or a broken checkout get looked at first. Call us on 01439 771468 and we\'ll tell you what we can do.'),
          ('Can you fix a site someone else built?','Yes. Most of our repair work is on sites built by other people.'),
          ('My site has been hacked. What should I do?','Change your hosting and admin passwords, then contact us. We\'ll clean the site, close the hole that let the hacker in and help you get removed from any Google warnings.'),
          ('How much does a repair cost?','It depends on the problem. We take a look first, tell you what we\'ve found and give you a fixed price before we do the work.')],
    related=['google-shopping-merchant-center','wordpress-woocommerce-websites','website-migrations'], cta_p='Not sure yet', cta_s='Fix a broken site'),

  dict(slug='website-migrations', nav='Platform moves', sub='eBay to Shopify, WooCommerce to Shopify...', icon='move', group='fix',
    c='var(--fox)', logos=['ebay','woocommerce','magento','shopify','bigcommerce'],
    title='Website Migration Service: Move to Shopify or BigCommerce | Foxy Websites',
    desc='Move your shop from eBay, WooCommerce, Magento, Wix or BigCommerce to Shopify or BigCommerce with products, customers, orders and Google rankings kept. UK design team.',
    eyebrow='Platform moves', h1='Move platforms <em>without losing</em> anything.',
    lede='eBay to Shopify, WooCommerce to Shopify, Magento to BigCommerce and more. We move your products, customers and orders, and keep your Google rankings with proper redirects.',
    glance=['Products, images and variants moved','Customers and order history carried over','301 redirects for every old URL','Test site before you switch','Launch day checks with you'],
    intro_h='Website migration, planned properly',
    intro=['Moving your shop to a new platform can cut costs and make it easier to run, but a rushed move can lose products, break links and drop your Google rankings overnight.',
           'Our design team plans the move first: what comes across, what gets tidied up on the way and how old URLs map to new ones. We move products, images, variants, customers and order history, and build the new design on a test site so you can check it before anything goes live.',
           'On launch day we switch the domain, set up 301 redirects for every old page, and check orders, emails, payments and Google Search Console afterwards.'],
    aside_h='Popular moves', aside=['eBay shop to your own Shopify site','WooCommerce to Shopify','Magento to Shopify or BigCommerce','Wix or Squarespace to Shopify','BigCommerce to Shopify, or the reverse'],
    feat_h='What we move',
    feats=[('Products','Titles, descriptions, images, variants, SKUs, prices and stock levels.'),
           ('Customers & orders','Customer details and order history, where the platforms allow it.'),
           ('Content','Pages, blog posts and images, tidied up as they come across.'),
           ('Redirects','Every old URL mapped to its new page with a 301 redirect.'),
           ('Design','A fresh design on the new platform, or your current look rebuilt.'),
           ('Launch checks','Payments, emails, tracking and Google Search Console checked after go-live.')],
    why=[('No lost rankings','Redirects and checks protect the Google traffic you\'ve built up.'),
         ('Test first','You see and approve the new shop before it goes live.'),
         ('Keep selling','We plan the switch so your shop stays open throughout.')],
    faqs=[('Can I move my eBay shop to my own website?','Yes. We bring your listings, photos and descriptions across to Shopify or BigCommerce, and you can keep selling on eBay alongside it.'),
          ('Will my Google rankings drop?','A properly redirected move keeps most rankings. We map every old URL and monitor Search Console after launch.'),
          ('Will my shop be offline during the move?','No. We build the new shop on a test site and switch over when it\'s ready, usually with no downtime.'),
          ('Can you move customer passwords?','Platforms don\'t allow passwords to be moved for security reasons, so customers set a new one at their next login.')],
    related=['shopify-websites','magento-opencart-support','ebay-shop-design'], cta_p='Not sure yet', cta_s='Move platforms'),

  dict(slug='product-listing-seo', nav='Product listing & SEO copy', sub='Bulk uploads, product pages and photos', icon='list', group='fix',
    c='var(--berry)', logos=['shopify','ebay','amazon','etsy','google'],
    title='Product Listing, Bulk Upload & SEO Product Descriptions | Foxy Websites',
    desc='Bulk product uploads, SEO product descriptions, product page design, photos and mockups for Shopify, eBay, Amazon, Etsy and Google Shopping. Written by a UK design team.',
    eyebrow='Product listing & SEO', h1='Hundreds of products, <em>listed properly</em>.',
    lede='Product listing is where most shops fall behind. We write, price and load your products in bulk, with SEO descriptions, clean data and images that sell, on your website and every marketplace.',
    glance=['Bulk uploads by CSV or feed','SEO product descriptions in UK English','Product page design','Photos, mockups and white-background images','Personalisation options'],
    intro_h='Product listing and SEO product descriptions',
    intro=['A shop is only as good as its product pages. Thin descriptions, missing sizes and blurry photos lose sales and rankings. Doing it properly for hundreds or thousands of products takes time most business owners don\'t have.',
           'Our design team prepares your products in bulk: titles, descriptions, variants, SKUs, prices, stock and images, formatted for your website and each marketplace. Descriptions are written in friendly UK English around the words customers search for, with sizes, materials and delivery facts included.',
           'AI tools help us with first drafts and data checks at scale, and every description is checked and edited by a person before it goes live. That\'s how we keep quality high on big catalogues.'],
    aside_h='Good fit if you...', aside=['have a spreadsheet of products to load','have thin or copied descriptions','sell the same range on several channels','need marketplace-ready images','want personalised product options'],
    feat_h='What we do',
    feats=[('Bulk uploads','Products prepared and loaded by CSV, feed or marketplace template.'),
           ('SEO descriptions','Unique, human-sounding descriptions built around real search terms.'),
           ('Product page design','Layouts with sizes, materials, delivery and FAQs that answer buyers\' questions.'),
           ('Photos & mockups','Your designs placed onto real product photos, plus white-background marketplace images.'),
           ('Personalisation','Name, photo and message options set up, with live previews where needed.'),
           ('Data clean-up','Duplicate products, broken variants, missing SKUs and messy tags fixed.')],
    why=[('Written for people','Copy that reads naturally and still ranks.'),
         ('Every channel','Your site, eBay, Amazon, Etsy and Google from one set of product data.'),
         ('Checked by people','AI helps with volume; our team checks every product.')],
    faqs=[('How many products can you list?','From a handful to tens of thousands. We work in batches and check each one before it goes live.'),
          ('Will the descriptions be unique?','Yes. Each product gets its own description. We never paste the same text across a range.'),
          ('Do you use AI to write descriptions?','AI helps with first drafts and checking data at scale. Our design team edits and approves every description so it\'s accurate and sounds like your business.'),
          ('Can you create product images?','Yes. We place your artwork onto real product photos and create clean white-background images for marketplaces.')],
    related=['ebay-shop-design','amazon-seller-setup','google-shopping-merchant-center'], cta_p='Not sure yet', cta_s='Product listing'),
]
PG = {p['slug']: p for p in PAGES}
GROUPS = [('web', 'Websites'), ('market', 'Marketplaces'), ('fix', 'Fixes & services')]

# ---------------------------------------------------------------- shared parts
FOX_SYMBOL = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="fox" viewBox="0 0 240 200">
    <path d="M112 30 Q110 10 118 2 Q116 16 122 26 Q124 8 134 4 Q126 18 128 32 Z" fill="#F26B21"/>
    <path d="M120 192 L52 132 Q16 104 14 70 L10 22 Q9 8 22 12 L78 38 Q120 22 162 38 L218 12 Q231 8 230 22 L226 70 Q224 104 188 132 Z" fill="#F26B21"/>
    <path d="M26 26 L70 46 Q46 56 32 74 Z" fill="#D9452B"/>
    <path d="M214 26 L170 46 Q194 56 208 74 Z" fill="#D9452B"/>
    <path d="M18 84 Q48 64 82 62 Q100 110 120 176 L58 128 Q28 108 18 84 Z" fill="#EEEDF2"/>
    <path d="M222 84 Q192 64 158 62 Q140 110 120 176 L182 128 Q212 108 222 84 Z" fill="#EEEDF2"/>
    <g fill="none" stroke="#231942" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
      <path d="M40 90 L30 99 L40 108"/><path d="M60 86 L52 112"/><path d="M72 92 L82 101 L72 110"/>
    </g>
    <circle cx="168" cy="88" r="7" fill="#E53935"/><circle cx="186" cy="94" r="7" fill="#FBC02D"/>
    <circle cx="166" cy="106" r="7" fill="#43A047"/><circle cx="184" cy="112" r="7" fill="#1E5BC6"/>
    <path d="M96 168 Q120 160 144 168 Q134 188 120 190 Q106 188 96 168 Z" fill="#231942" stroke="#F26B21" stroke-width="4" stroke-linejoin="round"/>
  </symbol>
</svg>'''

def org_ld():
    return {
        '@context': 'https://schema.org', '@type': 'ProfessionalService', '@id': SITE + '#business',
        'name': 'Foxy Websites', 'legalName': CO['legal'], 'url': SITE,
        'logo': SITE + 'brand/logo-square.png', 'image': SITE + 'brand/og-image.png',
        'telephone': CO['phone_intl'], 'email': CO['email'], 'vatID': CO['vat'],
        'identifier': {'@type': 'PropertyValue', 'propertyID': 'Companies House', 'value': CO['company_no']},
        'address': {'@type': 'PostalAddress', 'streetAddress': CO['street'], 'addressLocality': CO['town'],
                    'addressRegion': 'North Yorkshire', 'postalCode': CO['postcode'], 'addressCountry': 'GB'},
        'areaServed': 'GB',
        'description': 'Web design, ecommerce websites and marketplace shop setup for Shopify, BigCommerce, WordPress, eBay, Amazon, Etsy and Google Shopping.',
    }

def head(title, desc, path, extra_ld=()):
    rel = ''
    canon = SITE + ('' if path == 'index.html' else path)
    lds = [org_ld()] + list(extra_ld)
    ld = '\n'.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Foxy Websites">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}brand/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1B1236">
<link rel="icon" href="{rel}brand/fox-head.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rel}brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lilita+One&family=Figtree:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap">
<link rel="stylesheet" href="{rel}assets/site.css">
{ld}
</head>
<body>
{FOX_SYMBOL}
'''

def header(active=''):
    def menu(group):
        items = []
        for p in PAGES:
            if p['group'] != group:
                continue
            cur = ' aria-current="page"' if p['slug'] == active else ''
            items.append(f'<a href="{p["slug"]}.html"{cur}>{mi(p["icon"], "")}<span>{e(p["nav"])}<small>{e(p["sub"])}</small></span></a>')
        return '\n          '.join(items)
    def top_link(href, label, slug):
        cur = ' aria-current="page"' if active == slug else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Foxy Websites home">
      <svg viewBox="0 0 240 200" aria-hidden="true"><use href="#fox"/></svg>
      <b><span>FOXY</span> WEBSITES</b>
    </a>
    <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="main-nav">Menu</button>
    <nav class="nav" id="main-nav" aria-label="Main">
      <div class="dd"><a href="index.html#websites">Websites</a>
        <div class="dd-menu">
          {menu('web')}
        </div>
      </div>
      <div class="dd"><a href="index.html#marketplaces">Marketplaces</a>
        <div class="dd-menu">
          {menu('market')}
        </div>
      </div>
      <div class="dd"><a href="index.html#services">Fixes &amp; services</a>
        <div class="dd-menu">
          {menu('fix')}
        </div>
      </div>
      {top_link('design-team.html', 'Design team', 'design-team')}
      {top_link('contact.html', 'Contact', 'contact')}
    </nav>
    <a class="btn btn-fox" href="contact.html">Get a quote</a>
  </div>
</header>
'''

def cta_band(p=None):
    q = ''
    if p:
        parts = []
        if p.get('cta_p'): parts.append('platform=' + p['cta_p'].replace(' ', '%20'))
        if p.get('cta_s'): parts.append('service=' + p['cta_s'].replace(' ', '%20'))
        q = '?' + '&amp;'.join(parts) if parts else ''
    return f'''<section class="cta-band">
  <div class="wrap">
    <div>
      <h2>Tell us what you need. We'll send a fixed-price quote.</h2>
      <p>No jargon, and no charge for looking at what you've got now.</p>
    </div>
    <div class="acts">
      <a class="btn btn-light" href="contact.html{q}">Start your quote</a>
      <span>or call {CO['phone']}</span>
    </div>
  </div>
</section>
'''

def footer():
    def col(group, title):
        links = ''.join(f'<a href="{p["slug"]}.html">{e(p["nav"])}</a>' for p in PAGES if p['group'] == group)
        return f'<div><b>{title}</b>{links}</div>'
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-top">
      <div style="display:grid;gap:22px">
        <img class="foot-logo" src="brand/logo-horizontal-on-dark.svg" alt="Foxy Websites" width="320" height="123">
        <address class="foot-co">
          <b>{e(CO['legal'])}</b>
          <span>Unit 1, Balmforth Business Park<br>Sawmill Lane, Helmsley<br>York {CO['postcode']}<br>United Kingdom</span>
          <span class="reg">Company no. {CO['company_no']} · Registered in England and Wales<br>VAT no. {CO['vat']}</span>
          <a class="tel" href="tel:{CO['phone_intl']}">{CO['phone']}</a>
          <a href="mailto:{CO['email']}">{CO['email']}</a>
        </address>
      </div>
      <div class="foot-cols">
        {col('web', 'Websites')}
        {col('market', 'Marketplaces')}
        <div><b>Services</b>{''.join(f'<a href="{p["slug"]}.html">{e(p["nav"])}</a>' for p in PAGES if p['group']=='fix')}<a href="design-team.html">Design team</a><a href="contact.html">Contact &amp; quote</a><a href="privacy.html">Privacy</a></div>
      </div>
    </div>
    <div class="foot-base">
      <span>© 2026 Foxy Websites is a trading name of {e(CO['legal'])}, company no. {CO['company_no']}. Websites, marketplaces and fixes, by our in-house design team.</span>
      <span>Sister company: <a href="https://foxyprinting.co.uk" target="_blank" rel="noopener">Foxy Printing</a></span>
      <p class="foot-tm">Shopify, BigCommerce, WordPress, WooCommerce, Wix, Squarespace, eBay, Amazon, Etsy, Google, TikTok, Facebook, Instagram, Magento, OpenCart and OnBuy are trademarks of their respective owners. Logos are shown only to identify the platforms we work with. Foxy Websites is an independent design agency and is not endorsed by, sponsored by or affiliated with these companies.</p>
    </div>
  </div>
</footer>
<script src="assets/site.js" defer></script>
</body>
</html>
'''

def crumbs(items):
    lis = []
    for label, href in items:
        lis.append(f'<li><a href="{href}">{e(label)}</a></li>' if href else f'<li aria-current="page">{e(label)}</li>')
    return '<ol class="crumbs">' + ''.join(lis) + '</ol>'

def crumbs_ld(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': label, 'item': SITE + (href or '').replace('index.html', '')}
        for i, (label, href) in enumerate(items)]}

def faq_ld(faqs):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}

def faq_block(faqs, title='Questions people ask'):
    items = '\n'.join(f'      <details{" open" if i == 0 else ""}><summary>{e(q)}</summary><p>{e(a)}</p></details>' for i, (q, a) in enumerate(faqs))
    return f'''<section class="band" id="faq" style="background:#EDE9F7">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Questions</p><h2>{e(title)}</h2></div>
    <div class="faq-list">
{items}
    </div>
  </div>
</section>
'''

STEPS = '''<ol class="steps">
      <li style="--c:var(--fox)"><strong>Talk</strong><p>A free chat about your products, your shop and what's not working.</p></li>
      <li style="--c:var(--sun)"><strong>Plan &amp; quote</strong><p>A clear list of what we'll do, on which platforms, with a fixed price.</p></li>
      <li style="--c:#6FD07A"><strong>Build &amp; list</strong><p>Design, setup and listings, with previews for you to check as we go.</p></li>
      <li style="--c:#6FA0FF"><strong>Launch</strong><p>We go live together, test real orders and check Google can see it all.</p></li>
      <li style="--c:#FF6FA8"><strong>Look after</strong><p>Fixes, updates and new listings whenever you need them.</p></li>
    </ol>'''

CONSOLE = '''<div class="console" id="console">
      <div class="console-head">
        <b>Google Merchant Center · Diagnostics</b>
        <span class="score" id="score">6 issues · 312 products affected</span>
      </div>
      <ul class="issues">
        <li class="issue"><span class="st">Suspended</span><code>Misrepresentation</code><p class="errmsg">Account suspended. No products showing on Google.</p><p class="fixmsg"><strong>Fixed:</strong> contact details, returns and delivery pages rewritten, checkout made clear, review requested.</p></li>
        <li class="issue"><span class="st">Disapproved</span><code>Missing value [gtin]</code><p class="errmsg">Products need barcodes or a brand exemption.</p><p class="fixmsg"><strong>Fixed:</strong> GTINs, MPNs and brand added, or identifier_exists set correctly for own-made items.</p></li>
        <li class="issue"><span class="st">Disapproved</span><code>Mismatched value (page crawl) [price]</code><p class="errmsg">The feed price doesn't match the product page.</p><p class="fixmsg"><strong>Fixed:</strong> feed sync and sale prices corrected, structured data repaired.</p></li>
        <li class="issue"><span class="st">Limited</span><code>Image too small / promotional overlay</code><p class="errmsg">Images are blurry or have text on top.</p><p class="fixmsg"><strong>Fixed:</strong> clean main images replaced at full size.</p></li>
        <li class="issue"><span class="st">Disapproved</span><code>Missing shipping information</code><p class="errmsg">No delivery cost set for the UK.</p><p class="fixmsg"><strong>Fixed:</strong> delivery services and costs set up to match the checkout.</p></li>
        <li class="issue"><span class="st">Disapproved</span><code>Unavailable desktop landing page</code><p class="errmsg">Links in the feed go to a 404 page.</p><p class="fixmsg"><strong>Fixed:</strong> broken URLs and redirects repaired, feed re-fetched.</p></li>
      </ul>
      <div class="console-foot">
        <button class="btn btn-fox" type="button" id="fix-btn">Show it fixed</button>
        <small>Example of a typical Google Shopping repair job.</small>
      </div>
    </div>'''

def scard(p):
    return f'''<a class="scard" href="{p["slug"]}.html" style="--c:{p["c"]}">
        <div class="sc-top">{mi(p["icon"], "")}<h3>{e(p["nav"])}</h3></div>
        <p>{e(p["desc"].split(". ")[0].rstrip("."))}.</p>
        <span class="go">See {e(p["nav"])}</span>
      </a>'''

# ---------------------------------------------------------------- page builders
def service_page(p):
    path = p['slug'] + '.html'
    group_label = dict(GROUPS)[p['group']]
    anchor = {'web': 'websites', 'market': 'marketplaces', 'fix': 'services'}[p['group']]
    cr = [('Home', 'index.html'), (group_label, f'index.html#{anchor}'), (p['nav'], None)]
    cr_ld = [('Home', 'index.html'), (group_label, f'#{anchor}'), (p['nav'], path)]
    logos = ''.join(tile(k, '') for k in p['logos'])
    logos_html = f'<div class="logos">{logos}</div>' if logos else ''
    glance = ''.join(f'<li>{e(g)}</li>' for g in p['glance'])
    intro = '\n        '.join(f'<p>{e(x)}</p>' for x in p['intro'])
    aside = ''.join(f'<li>{e(x)}</li>' for x in p['aside'])
    feats = '\n      '.join(f'<article class="feat"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in p['feats'])
    why = '\n      '.join(f'<div class="why"><strong>{e(t)}</strong><p>{e(d)}</p></div>' for t, d in p['why'])
    related = '\n      '.join(scard(PG[s]) for s in p['related'])
    q = 'platform=' + p['cta_p'].replace(' ', '%20') + (('&amp;service=' + p['cta_s'].replace(' ', '%20')) if p.get('cta_s') else '')
    console = ''
    if p.get('console'):
        console = f'''<section class="band fix" style="padding-top:0">
  <div class="wrap">
    <div class="fix-copy">
      <p class="eyebrow" style="color:var(--red)">A typical repair</p>
      <h2>From suspended to approved.</h2>
      <p class="lede">This is the kind of Merchant Center report we see every week, and what we change to clear it. Press the button to see the fixed version.</p>
      <p><a class="btn btn-fox" href="contact.html?service=Fix%20Google%20Shopping">Get Google Shopping fixed</a></p>
    </div>
    {CONSOLE}
  </div>
</section>
'''
    body = f'''{header(p['slug'])}
<main id="top" style="--c:{p['c']}">

<section class="phero night">
  <div class="hero-glow"></div>
  <div class="wrap">
    <div class="phero-copy">
      {crumbs(cr)}
      <p class="eyebrow">{e(p['eyebrow'])}</p>
      <h1>{p['h1']}</h1>
      <p class="lede">{e(p['lede'])}</p>
      {logos_html}
      <div class="hero-cta">
        <a class="btn btn-fox" href="contact.html?{q}">Get a fixed-price quote</a>
        <a class="btn btn-ghost" style="color:#fff" href="tel:{CO['phone_intl']}">Call {CO['phone']}</a>
      </div>
    </div>
    <aside class="glance" aria-label="At a glance">
      <h2>At a glance</h2>
      <ul>{glance}</ul>
    </aside>
  </div>
</section>

<section class="band intro">
  <div class="wrap">
    <div class="prose">
        <h2>{e(p['intro_h'])}</h2>
        {intro}
    </div>
    <aside class="aside">
      <h3>{e(p['aside_h'])}</h3>
      <ul>{aside}</ul>
    </aside>
  </div>
</section>

<section class="band" style="padding-top:0">
  <div class="wrap">
    <div class="head"><p class="eyebrow">What's included</p><h2>{e(p['feat_h'])}</h2></div>
    <div class="feat-grid">
      {feats}
    </div>
  </div>
</section>

{console}<section class="band night">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Why Foxy Websites</p><h2>Designed by people who've done it for 30 years.</h2>
      <p class="lede">Our in-house design team plans, builds and checks every project. AI tools help with the legwork, and nothing goes live without a person signing it off.</p></div>
    <div class="why-grid">
      {why}
    </div>
    <div class="together" style="margin-top:48px"><p class="eyebrow">How a project runs</p></div>
    {STEPS}
  </div>
</section>

{faq_block(p['faqs'])}
<section class="band">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Related services</p><h2>Often done together.</h2></div>
    <div class="card-grid">
      {related}
    </div>
  </div>
</section>

</main>
{cta_band(p)}{footer()}'''
    return head(p['title'], p['desc'], path, [crumbs_ld(cr_ld), faq_ld(p['faqs'])]) + body

def home_page():
    faqs = [('Can you work on a site someone else built?','Yes. Most of our fix and listing work is on existing shops. We\'ll take a look first, tell you what we find, and only then quote.'),
            ('Can you move my eBay shop to my own website?','Yes. We bring your products, photos and descriptions across to Shopify, BigCommerce or WooCommerce, and keep your eBay shop running alongside it if you want both.'),
            ('Will one stock list work across my site, eBay, Amazon and Etsy?','Yes. We set up connector apps so an item sold on one channel comes off stock everywhere, and the orders land in one place.'),
            ('Do you use AI? Will my site look generic?','Your site is designed by people, not generated. We use the latest AI models for the legwork, like first drafts of product descriptions, building bulk listing files and checking feeds for errors. The design, the decisions and the final check are all down to our design team.'),
            ('Where are you based?','Our team is based in Helmsley, North Yorkshire, and works with businesses across the UK. Most projects are run by phone, email and video call.'),
            ('How much does it cost?','Every job is different, so we give you a fixed price after a free look at what you need. No hourly surprises.')]
    wall_keys = [('shopify','shopify-websites.html'),('bigcommerce','bigcommerce-websites.html'),('wordpress','wordpress-woocommerce-websites.html'),('woocommerce','wordpress-woocommerce-websites.html'),('wix','wix-squarespace-websites.html'),('squarespace','wix-squarespace-websites.html'),('magento','magento-opencart-support.html'),('opencart','magento-opencart-support.html'),('ebay','ebay-shop-design.html'),('amazon','amazon-seller-setup.html'),('etsy','etsy-shop-setup.html'),('google','google-shopping-merchant-center.html'),('googleads','google-shopping-merchant-center.html'),('tiktok','social-shops-tiktok-facebook-instagram.html'),('facebook','social-shops-tiktok-facebook-instagram.html'),('instagram','social-shops-tiktok-facebook-instagram.html'),('onbuy','social-shops-tiktok-facebook-instagram.html')]
    wall = '\n      '.join(tile(k, '', href) for k, href in wall_keys)
    def group_cards(g):
        return '\n      '.join(scard(p) for p in PAGES if p['group'] == g)
    body = f'''{header('home')}
<main id="top">

<section class="hero night">
  <div class="hero-glow"></div>
  <div class="wrap">
    <div class="hero-copy">
      <p class="eyebrow">Web design · Helmsley, North Yorkshire · 30 years</p>
      <h1>Your shop on <span class="c1">every platform</span>, built, <span class="c2">listed</span> and <span class="c3">fixed</span>.</h1>
      <p class="lede">Websites and online shops on Shopify, BigCommerce, WordPress and more, plus eBay, Amazon, Etsy and Google Shopping. Our design team builds the site, sets up the shops, loads the listings and sorts it out when something breaks.</p>
      <div class="hero-cta">
        <a class="btn btn-fox" href="contact.html">Start your quote</a>
        <a class="btn btn-ghost" href="website-repairs.html">Something's broken</a>
      </div>
      <div class="creds">
        <span><i class="dot" style="background:var(--red)"></i>Websites since the dial-up days</span>
        <span><i class="dot" style="background:var(--sun)"></i>12+ platforms</span>
        <span><i class="dot" style="background:var(--leaf)"></i>One in-house design team for site and marketplaces</span>
      </div>
    </div>

    <div class="switch" id="switch">
      <div class="tabs" role="tablist" aria-label="Pick a platform"></div>
      <div style="position:relative"><svg class="peek" viewBox="0 0 240 200" aria-hidden="true"><use href="#fox"/></svg>
      <div class="browser" aria-live="polite">
        <div class="bar"><i style="background:var(--red)"></i><i style="background:var(--sun)"></i><i style="background:var(--leaf)"></i><div class="url" id="sw-url"></div></div>
        <div class="shop" id="sw-shop"></div>
      </div></div>
    </div>
  </div>
</section>

<section class="band" style="padding-block:48px 0">
  <div class="wrap">
    <p class="eyebrow" style="margin-bottom:16px">Platforms we design, build and sell on</p>
    <div class="logo-wall">
      {wall}
    </div>
    <p class="tm-note">Logos belong to their owners and are shown to identify the platforms we work with. We are an independent agency, not affiliated with or endorsed by them.</p>
  </div>
</section>

<section class="band years" id="experience">
  <div class="wrap">
    <div class="years-copy">
      <span class="big30" aria-hidden="true">30</span>
      <p class="eyebrow">Years on the web</p>
      <h2>We've built through every version of the internet.</h2>
      <p class="lede">Our design team built their first websites by hand, when pages loaded line by line over a modem. Every platform since then, every marketplace, every change Google has made to how shops get found, they have designed, built and sold through it. That's why we can pick up any site, on any system, and know what to do with it.</p>
      <p class="lede">That experience is what you pay for: knowing what makes a shop look trustworthy, what makes a product page sell, and what Google and the marketplaces will and won't accept. Today the latest AI tools take care of the legwork, so the team spends its time on design and getting it right.</p>
      <p><a class="btn btn-ghost" href="design-team.html">Meet the design team</a></p>
    </div>
    <ol class="timeline" aria-label="The web we've worked through">
      <li style="--c:var(--red)"><b>Mid 90s</b><strong>Hand-coded HTML</strong><p>Table layouts, dial-up, guestbooks. Learning how the web really works, from the code up.</p></li>
      <li style="--c:var(--fox)"><b>Early 2000s</b><strong>The first online shops</strong><p>Shopping carts, payment gateways and the first eBay shops. Selling online becomes a real business.</p></li>
      <li style="--c:var(--sun)"><b>Late 2000s</b><strong>WordPress and social</strong><p>Sites the owner can edit themselves. Blogs, SEO and Facebook pages arrive.</p></li>
      <li style="--c:var(--leaf)"><b>2010s</b><strong>Shopify, Amazon and Etsy</strong><p>Hosted shop platforms, marketplace sellers, mobile-first design and Google Shopping feeds.</p></li>
      <li style="--c:var(--sky)"><b>2020s</b><strong>Everywhere at once</strong><p>One stock list feeding a website, eBay, Amazon, Etsy, TikTok Shop and Google, all kept in sync.</p></li>
      <li style="--c:var(--berry)"><b>Now</b><strong>Design-led, AI-assisted</strong><p>The same hands-on design team, with AI doing the repetitive jobs. Bigger projects done faster, every piece designed and checked by people.</p></li>
    </ol>
  </div>
</section>

<section class="band" id="websites" style="padding-top:0">
  <div class="wrap">
    <div class="head">
      <p class="eyebrow">What we do</p>
      <h2>Websites, marketplaces and fixes, under one roof.</h2>
      <p class="lede">Pick a service to see exactly what's included. Most projects mix a few: a new Shopify site, an eBay shop to match, and Google Shopping set up from day one.</p>
    </div>
    <div class="group-head"><h3>Websites</h3><p>New shops, redesigns and rebuilds on the platform that suits how you sell.</p></div>
    <div class="card-grid">
      {group_cards('web')}
    </div>
    <div class="group-head" id="marketplaces"><h3>Marketplaces</h3><p>Shop setup, design, listings and connectors for the sites where people already shop.</p></div>
    <div class="card-grid">
      {group_cards('market')}
    </div>
    <div class="group-head" id="services"><h3>Fixes &amp; services</h3><p>Repairs, platform moves and the product listing work that makes a shop sell.</p></div>
    <div class="card-grid">
      {group_cards('fix')}
    </div>
  </div>
</section>

<section class="band fix night" id="fixes">
  <div class="wrap">
    <div class="fix-copy">
      <p class="eyebrow" style="color:#FF8A86">Rescue &amp; repair</p>
      <h2>Broken site? Google Shopping switched off? We'll fix it.</h2>
      <p class="lede">Send us the error message, the screenshot, or just "it's stopped working". We find the cause, fix it, and tell you in plain English what went wrong.</p>
      <p style="display:flex;flex-wrap:wrap;gap:12px"><a class="btn btn-fox" href="website-repairs.html">Website repairs</a><a class="btn btn-ghost" style="color:#fff" href="google-shopping-merchant-center.html">Google Shopping fixes</a></p>
    </div>
    {CONSOLE}
  </div>
</section>

<section class="band" id="how">
  <div class="wrap">
    <div class="head">
      <p class="eyebrow">Who you work with</p>
      <h2>A real design team with 30 years behind it.</h2>
      <p class="lede">Your project is designed, built and checked by our in-house design team, from the first chat to launch day and after. AI now does the legwork in the background, so the team can put its time into the design, the detail and the results.</p>
    </div>
    <div class="duo-grid">
      <article class="person team">
        <p class="role">The heart of every project</p>
        <h3>The Design Team</h3>
        <p>Designers and web builders who have made websites, online shops and printed brands since the 90s. You talk to the same people throughout.</p>
        <div class="skills">
          <div class="skill"><strong>Web design &amp; UX</strong><span>Layouts, colours and customer journeys that make people trust you and buy.</span></div>
          <div class="skill"><strong>Shop builds &amp; development</strong><span>Themes, custom features, apps and integrations on every platform.</span></div>
          <div class="skill"><strong>Marketplace know-how</strong><span>eBay, Amazon and Etsy rules, categories and listing formats learnt the hard way.</span></div>
          <div class="skill"><strong>Product pages &amp; imagery</strong><span>Photos, mockups and page layouts that answer buyers' questions.</span></div>
          <div class="skill"><strong>SEO &amp; Google Shopping</strong><span>Titles, feeds and Merchant Center set up so customers find you.</span></div>
          <div class="skill"><strong>Branding &amp; print</strong><span>Logos and brand looks from a design and print business, so online matches offline.</span></div>
        </div>
      </article>
      <article class="person ai" style="background:var(--night)">
        <p class="role" style="color:var(--sun)">Behind the scenes</p>
        <h3>AI does the legwork</h3>
        <p>We use the latest AI models as tools, the same way we use design software. They speed up the repetitive jobs; the design team decides and checks everything.</p>
        <ul>
          <li>First drafts of product descriptions and SEO titles</li>
          <li>Building bulk listing files for big catalogues</li>
          <li>Scanning feeds and code for errors</li>
          <li>Checking and tidying product data</li>
        </ul>
        <p><strong style="color:#fff">Nothing goes live without a person signing it off.</strong></p>
      </article>
    </div>
  </div>
</section>

<section class="band proof" id="proof" style="padding-top:0">
  <div class="wrap">
    <div class="head" style="margin:0">
      <p class="eyebrow">We run our own shop</p>
      <h2>Tested on Foxy Printing first.</h2>
      <p class="lede">Everything we offer, we already do for our own print business. Same team, same tools. If it works for a shop with thousands of personalised products, it'll work for yours.</p>
      <p><a class="btn btn-ghost" href="https://foxyprinting.co.uk" target="_blank" rel="noopener">Visit foxyprinting.co.uk</a></p>
    </div>
    <div class="proof-card">
      <div class="url">foxyprinting.co.uk</div>
      <ul class="proof-rows">
        <li style="--c:var(--leaf)"><i class="dot"></i><strong>Shopify shop with a custom product designer</strong><p>Customers design their own leavers hoodies, preview them on real photos, and print files are made automatically.</p></li>
        <li style="--c:var(--fox)"><i class="dot"></i><strong>eBay shop design and bulk listings</strong><p>Branded shop, listing template and large product ranges loaded by upload file.</p></li>
        <li style="--c:var(--sky)"><i class="dot"></i><strong>Amazon listing feeds</strong><p>Products converted into Amazon's listing format, including personalised items.</p></li>
        <li style="--c:var(--sun)"><i class="dot"></i><strong>Google Shopping, Facebook and TikTok</strong><p>Every product carries the Google fields it needs and feeds the social sales channels.</p></li>
      </ul>
    </div>
  </div>
</section>

{faq_block(faqs, 'Things people ask us.')}
</main>
{cta_band()}{footer()}'''
    return head('Web Design & Online Shops in Helmsley, York | Foxy Websites',
                'Foxy Websites designs, builds and fixes online shops on Shopify, BigCommerce and WordPress, and sets up eBay, Amazon, Etsy and Google Shopping. 30 years of experience, North Yorkshire.',
                'index.html', [faq_ld(faqs)]) + body

def team_page():
    cr = [('Home', 'index.html'), ('Design team', None)]
    faqs = [('Who will I deal with?','The same small design team from first chat to launch and after. You won\'t be passed between departments.'),
            ('How do you use AI?','As a tool for repetitive work: first drafts of product descriptions, building bulk listing files, and scanning feeds and code for errors. The design, decisions and final checks are done by people.'),
            ('Do you only work locally?','We\'re based in Helmsley, North Yorkshire, and work with businesses across the UK by phone, email and video call.'),
            ('Are you connected to Foxy Printing?','Yes. Foxy Printing is our sister company. We design, build and run its website and marketplace shops, which is where we test everything we offer.')]
    body = f'''{header('design-team')}
<main id="top" style="--c:var(--fox)">
<section class="phero night">
  <div class="hero-glow"></div>
  <div class="wrap">
    <div class="phero-copy">
      {crumbs(cr)}
      <p class="eyebrow">Our design team</p>
      <h1>Real designers. <em>30 years</em> of websites.</h1>
      <p class="lede">Foxy Websites is the web design side of {e(CO['legal'])}, a design and print business in Helmsley, North Yorkshire. Our in-house team plans, designs, builds and looks after every project.</p>
      <div class="hero-cta"><a class="btn btn-fox" href="contact.html">Talk to the team</a></div>
    </div>
    <aside class="glance" aria-label="At a glance">
      <h2>The team in brief</h2>
      <ul><li>Building websites since the mid 90s</li><li>Design, development, marketplaces and SEO in one team</li><li>Same people from first chat to aftercare</li><li>Our own shop is the test bed</li><li>AI for the legwork, people for the decisions</li></ul>
    </aside>
  </div>
</section>

<section class="band intro">
  <div class="wrap">
    <div class="prose">
      <h2>Why experience matters</h2>
      <p>Anyone can put a theme on a website. Knowing what to change, and why, is what takes years. Our design team has worked through every stage of the web: hand-coded pages, the first online shops, WordPress, Shopify, Amazon, Etsy and today's world of shops that sell on five channels at once.</p>
      <p>That experience shows up in the details customers notice: product pages that answer their questions, delivery information they can trust, and a checkout that just works. It also shows up in the details Google and the marketplaces check, from structured data and redirects to item specifics and Merchant Center policies.</p>
      <p>Because we're also a design and print business, we think about your brand as a whole. Your website, your eBay shop, your packaging and your printed materials should all look like the same company.</p>
    </div>
    <aside class="aside" style="--c:var(--fox)">
      <h3>What the team covers</h3>
      <ul><li>Web design and user experience</li><li>Shop builds and custom development</li><li>eBay, Amazon and Etsy shops</li><li>Product listing and SEO copy</li><li>Google Shopping and Search Console</li><li>Branding, logos and print</li></ul>
    </aside>
  </div>
</section>

<section class="band night">
  <div class="wrap">
    <div class="duo-grid">
      <article class="person team">
        <p class="role">The heart of every project</p>
        <h3>The Design Team</h3>
        <p>Designers and web builders who have made websites, online shops and printed brands since the 90s. You talk to the same people throughout.</p>
        <div class="skills">
          <div class="skill"><strong>Web design &amp; UX</strong><span>Layouts, colours and customer journeys that make people trust you and buy.</span></div>
          <div class="skill"><strong>Shop builds &amp; development</strong><span>Themes, custom features, apps and integrations on every platform.</span></div>
          <div class="skill"><strong>Marketplace know-how</strong><span>eBay, Amazon and Etsy rules, categories and listing formats learnt the hard way.</span></div>
          <div class="skill"><strong>Product pages &amp; imagery</strong><span>Photos, mockups and page layouts that answer buyers' questions.</span></div>
          <div class="skill"><strong>SEO &amp; Google Shopping</strong><span>Titles, feeds and Merchant Center set up so customers find you.</span></div>
          <div class="skill"><strong>Branding &amp; print</strong><span>Logos and brand looks from a design and print business, so online matches offline.</span></div>
        </div>
      </article>
      <article class="person ai">
        <p class="role" style="color:var(--sun)">Behind the scenes</p>
        <h3>AI does the legwork</h3>
        <p>We use the latest AI models as tools, the same way we use design software. They speed up the repetitive jobs; the design team decides and checks everything.</p>
        <ul>
          <li>First drafts of product descriptions and SEO titles</li>
          <li>Building bulk listing files for big catalogues</li>
          <li>Scanning feeds and code for errors</li>
          <li>Checking and tidying product data</li>
        </ul>
        <p><strong style="color:#fff">Nothing goes live without a person signing it off.</strong></p>
      </article>
    </div>
    <div class="together"><p class="eyebrow">How a project runs</p></div>
    {STEPS}
  </div>
</section>

<section class="band years">
  <div class="wrap">
    <div class="years-copy">
      <span class="big30" aria-hidden="true">30</span>
      <p class="eyebrow">Years on the web</p>
      <h2>Every version of the internet, worked through.</h2>
      <p class="lede">The platforms change every few years. The basics of a shop that sells don't: trust, clear information, good photos and being easy to find.</p>
    </div>
    <ol class="timeline" aria-label="The web we've worked through">
      <li style="--c:var(--red)"><b>Mid 90s</b><strong>Hand-coded HTML</strong><p>Table layouts, dial-up, guestbooks. Learning how the web really works, from the code up.</p></li>
      <li style="--c:var(--fox)"><b>Early 2000s</b><strong>The first online shops</strong><p>Shopping carts, payment gateways and the first eBay shops.</p></li>
      <li style="--c:var(--sun)"><b>Late 2000s</b><strong>WordPress and social</strong><p>Sites the owner can edit themselves. Blogs, SEO and Facebook pages arrive.</p></li>
      <li style="--c:var(--leaf)"><b>2010s</b><strong>Shopify, Amazon and Etsy</strong><p>Hosted shop platforms, marketplace sellers, mobile-first design and Google Shopping feeds.</p></li>
      <li style="--c:var(--sky)"><b>2020s</b><strong>Everywhere at once</strong><p>One stock list feeding a website, eBay, Amazon, Etsy, TikTok Shop and Google.</p></li>
      <li style="--c:var(--berry)"><b>Now</b><strong>Design-led, AI-assisted</strong><p>The same hands-on team, with AI doing the repetitive jobs.</p></li>
    </ol>
  </div>
</section>

{faq_block(faqs, 'About working with us')}
</main>
{cta_band()}{footer()}'''
    return head('Our Web Design Team: 30 Years of Experience | Foxy Websites',
                'Meet the Foxy Websites design team in Helmsley, North Yorkshire: 30 years of web design, ecommerce, marketplace and print experience, with AI tools for the legwork.',
                'design-team.html', [crumbs_ld([('Home', 'index.html'), ('Design team', 'design-team.html')]), faq_ld(faqs)]) + body

def contact_page():
    cr = [('Home', 'index.html'), ('Contact & quote', None)]
    body = f'''{header('contact')}
<main id="top" style="--c:var(--fox)">
<section class="phero night" style="padding-bottom:48px">
  <div class="hero-glow"></div>
  <div class="wrap" style="grid-template-columns:1fr">
    <div class="phero-copy">
      {crumbs(cr)}
      <p class="eyebrow">Contact &amp; quote</p>
      <h1>Tell us what you need. <em>Tick as many as you like.</em></h1>
      <p class="lede">We'll reply with a fixed price and a plan. No jargon, and no charge for looking at what you've got now. Prefer to talk? Call {CO['phone']}.</p>
    </div>
  </div>
</section>

<section class="band quote" id="quote" style="padding-top:48px">
  <div class="wrap">
    <div class="contact-grid">
    <form class="q-form" id="q-form" novalidate>
      <fieldset class="q-group">
        <legend>Which platforms?</legend>
        <div class="chips" id="chips-platforms"></div>
      </fieldset>
      <fieldset class="q-group">
        <legend>What do you need?</legend>
        <div class="chips" id="chips-services"></div>
      </fieldset>
      <div class="fields">
        <div class="field"><label for="q-name">Your name</label><input id="q-name" name="name" autocomplete="name" placeholder="e.g. Sam Taylor"></div>
        <div class="field"><label for="q-email">Email</label><input id="q-email" name="email" type="email" autocomplete="email" placeholder="you@yourshop.co.uk"></div>
        <div class="field"><label for="q-site">Current website or shop link</label><input id="q-site" name="site" placeholder="yourshop.co.uk or eBay shop name"></div>
        <div class="field"><label for="q-size">How many products?</label>
          <select id="q-size" name="size"><option>Not sure yet</option><option>Under 50</option><option>50 to 500</option><option>500 to 5,000</option><option>Over 5,000</option></select></div>
        <div class="field full"><label for="q-msg">Anything else we should know?</label><textarea id="q-msg" name="msg" placeholder="What you sell, what's not working, any deadline..."></textarea></div>
      </div>
      <div class="q-actions">
        <button class="btn btn-fox" type="submit">Build my brief</button>
        <small id="q-note">Pick at least one service and add your email.</small>
      </div>
      <div class="brief" id="brief" hidden>
        <pre id="brief-text"></pre>
        <div class="brief-row">
          <button class="btn btn-fox" type="button" id="copy-btn">Copy brief</button>
          <span>then email it to</span>
          <span class="addr">{CO['email']}</span>
          <span>or call <b>{CO['phone']}</b></span>
        </div>
      </div>
    </form>
    <address class="contact-card">
      <b>Foxy Websites</b>
      <span>{e(CO['legal'])}<br>Unit 1, Balmforth Business Park<br>Sawmill Lane, Helmsley<br>York {CO['postcode']}<br>United Kingdom</span>
      <a class="tel" href="tel:{CO['phone_intl']}">{CO['phone']}</a>
      <a href="mailto:{CO['email']}">{CO['email']}</a>
      <span class="reg">Company no. {CO['company_no']} · Registered in England and Wales<br>VAT no. {CO['vat']}</span>
    </address>
    </div>
  </div>
</section>
</main>
{footer()}'''
    return head('Contact Us & Get a Website Quote | Foxy Websites',
                'Get a fixed-price quote for a new website, eBay, Amazon or Etsy shop, Google Shopping or a website repair. Call 01439 771468 or send us your brief. Helmsley, North Yorkshire.',
                'contact.html', [crumbs_ld([('Home', 'index.html'), ('Contact', 'contact.html')])]) + body

def privacy_page():
    cr = [('Home', 'index.html'), ('Privacy', None)]
    body = f'''{header()}
<main id="top">
<section class="phero night" style="padding-bottom:40px">
  <div class="wrap" style="grid-template-columns:1fr"><div class="phero-copy">{crumbs(cr)}<h1>Privacy notice</h1></div></div>
</section>
<section class="band">
  <div class="wrap plain">
    <p>This website is run by Foxy Websites, a trading name of {e(CO['legal'])}, {e(CO['street'])}, {CO['town']}, {CO['city']} {CO['postcode']}, United Kingdom (company no. {CO['company_no']}, registered in England and Wales). If you have any questions about your information, email {CO['email']} or call {CO['phone']}.</p>
    <h2>What we collect</h2>
    <p>The quote form on this website does not send or store anything. It builds a brief in your browser for you to copy and email to us. We only receive your details when you email or phone us.</p>
    <p>When you contact us, we keep your name, contact details and the information you send us so we can reply, prepare a quote and carry out any work you ask for.</p>
    <h2>How we use it</h2>
    <ul><li>To reply to your enquiry and prepare a quote</li><li>To carry out and invoice the work you ask for</li><li>To meet our legal and accounting obligations</li></ul>
    <p>We don't sell your information or use it for marketing without your permission.</p>
    <h2>Other services this site uses</h2>
    <p>This website loads fonts from Google Fonts, which means your browser connects to Google's servers. If we add analytics in future, we'll update this notice.</p>
    <h2>Your rights</h2>
    <p>You can ask to see, correct or delete the information we hold about you by emailing {CO['email']}. You can also complain to the Information Commissioner's Office (ico.org.uk).</p>
  </div>
</section>
</main>
{footer()}'''
    return head('Privacy Notice | Foxy Websites', 'How Foxy Websites, a trading name of DepthChargeDesign & Print Ltd, handles your information.', 'privacy.html') + body

def notfound_page():
    body = f'''{header()}
<main id="top">
<section class="phero night">
  <div class="wrap" style="grid-template-columns:1fr">
    <div class="phero-copy">
      <p class="eyebrow">Error 404</p>
      <h1>This page has <em>wandered off</em>.</h1>
      <p class="lede">The page you're looking for doesn't exist or has moved. Try one of these instead.</p>
      <div class="hero-cta"><a class="btn btn-fox" href="index.html">Go to the home page</a><a class="btn btn-ghost" style="color:#fff" href="contact.html">Contact us</a></div>
    </div>
  </div>
</section>
<section class="band"><div class="wrap"><div class="card-grid">
      {''.join(scard(p) for p in PAGES[:6])}
</div></div></section>
</main>
{footer()}'''
    h = head('Page not found | Foxy Websites', 'This page could not be found.', '404.html')
    return h.replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1) + body

# ---------------------------------------------------------------- write everything
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'assets'))
    shutil.copytree(os.path.join(ROOT, 'brand'), os.path.join(OUT, 'brand'))
    shutil.copytree(os.path.join(ROOT, 'logos'), os.path.join(OUT, 'logos'),
                    ignore=shutil.ignore_patterns('*.md'))
    css = open(os.path.join(ROOT, 'src', 'base.css')).read() + open(os.path.join(ROOT, 'src', 'extra.css')).read()
    css += '\n.mi svg{width:18px;height:18px;color:var(--ink)}\n.scard .mi svg{width:24px;height:24px}\n'
    open(os.path.join(OUT, 'assets', 'site.css'), 'w').write(css)
    shutil.copy(os.path.join(ROOT, 'src', 'site.js'), os.path.join(OUT, 'assets', 'site.js'))
    pages = {'index.html': home_page(), 'design-team.html': team_page(), 'contact.html': contact_page(),
             'privacy.html': privacy_page(), '404.html': notfound_page()}
    for p in PAGES:
        pages[p['slug'] + '.html'] = service_page(p)
    for name, text in pages.items():
        open(os.path.join(OUT, name), 'w').write(text)
    urls = ['index.html'] + [p['slug'] + '.html' for p in PAGES] + ['design-team.html', 'contact.html', 'privacy.html']
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = SITE + ('' if u == 'index.html' else u)
        sm.append(f'  <url><loc>{loc}</loc></url>')
    sm.append('</urlset>')
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
    print('built', len(pages), 'pages into', OUT)

if __name__ == '__main__':
    main()
