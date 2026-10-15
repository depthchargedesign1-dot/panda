# Foxy Websites

Multi-page website for Foxy Websites (www.foxywebsites.co.uk): web design on every platform, eBay/Amazon/Etsy shops, Google Shopping, repairs and migrations, by our in-house design team.

## Upload
`site/` is the finished website. Upload **everything inside `site/`** to the host's public folder (often `public_html`), keeping the folders. `upload/foxywebsites-upload.zip` is the same thing zipped.

Then in Google Search Console, add the site and submit `https://www.foxywebsites.co.uk/sitemap.xml`. If the host allows it, point 404 errors at `404.html`.

## Editing
Don't edit `site/` by hand. Change the content in `build.py` (all page text lives there), styles in `src/extra.css` / `src/base.css`, scripts in `src/site.js`, then run:

    python3 build.py

## Pages
- `index.html` home, `design-team.html`, `contact.html` (quote builder), `privacy.html`, `404.html`
- 14 service pages: Shopify, BigCommerce, WordPress & WooCommerce, Wix & Squarespace, Magento & OpenCart, hand-built sites, eBay, Amazon, Etsy, Google Shopping, TikTok/Facebook/Instagram, website repairs, platform moves, product listing & SEO copy
- Each page has its own SEO title and description, canonical URL, social preview tags, business details in Google's structured format (schema.org), breadcrumbs and FAQ markup. `sitemap.xml` and `robots.txt` are included.
- Contact links can pre-tick the quote form, e.g. `contact.html?platform=eBay&service=Shop%20setup`.

## Brand
- `brand/`: the Foxy Websites logo set (fox head with `</>` and browser-dot cheeks), plus `og-image.png` (social preview), `apple-touch-icon.png` and `logo-square.png`.
- `logos/`: platform logos from Simple Icons (CC0 licence, see `logos/SIMPLE-ICONS-LICENSE.md`). Amazon, Magento, OpenCart and OnBuy logos aren't in that library at those companies' request, so they appear as text. Every page footer carries a trademark note saying the logos identify platforms only and we're not affiliated.

## Company details
- DepthChargeDesign & Print Ltd, Unit 1, Balmforth Business Park, Sawmill Lane, Helmsley, York YO62 5DQ
- 01439 771468 · sales@foxyprinting.co.uk
- Company no. 09618286 (England and Wales) · VAT no. GB295734264
- The business has moved: never use the old Kirkbymoorside address.
- Enquiries go to sales@foxyprinting.co.uk until a forwarding address such as hello@foxywebsites.co.uk -> sales@foxyprinting.co.uk is set up and tested.
