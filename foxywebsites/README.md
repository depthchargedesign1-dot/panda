# Foxy Websites

One-page website for Foxy Websites (our in-house design team, with AI tools for the legwork): website builds on every platform, eBay/Amazon/Etsy shop setup and listings, Google Shopping and broken-site fixes.

- `upload/foxywebsites-upload.zip`: everything the web host needs (index.html + brand/). Unzip it into the site's public folder (often `public_html`).
- `index.html`: the whole site (inline CSS and JS, Google Fonts). Open it in a browser or upload it to any host.
- `brand/`: the new logo, built from the Foxy fox head. The gamepad cheeks are now `</>` code brackets and four browser dots.
  - `fox-head.svg`: the icon (also used as the favicon)
  - `logo-horizontal.svg`: for light backgrounds
  - `logo-horizontal-on-dark.svg`: for dark backgrounds
  - `logo-square.svg`: 400×400 for social profiles and marketplace shop logos
  - The lettering is Lilita One, converted to outlines, so the logos look the same everywhere.

Company details (footer and quote section):
- DepthChargeDesign & Print Ltd, Unit 1, Balmforth Business Park, Sawmill Lane, Helmsley, York YO62 5DQ
- 01439 771468 · sales@foxyprinting.co.uk
- Company no. 09618286 (England and Wales) · VAT no. GB295734264
- The business has moved: never use the old Kirkbymoorside address.

Before going live:
- Domain: www.foxywebsites.co.uk (owned). Enquiries go to sales@foxyprinting.co.uk until a forwarding address such as hello@foxywebsites.co.uk -> sales@foxyprinting.co.uk is set up and tested. Then swap the address in `index.html`.
- The quote form builds a brief for the visitor to copy. To have it email you directly, point it at a form service such as Formspree or your host's form handler.
