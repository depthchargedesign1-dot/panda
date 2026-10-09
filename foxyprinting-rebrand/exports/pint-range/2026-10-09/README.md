# 8 new personalised pint glasses (9 Oct 2026)

Owner: "yes make all 8 and list on foxy" (after the Etsy research `plan/etsy-pint-glass-research-2026-10-09.md` and his reference photos). Clear-glass UV DTF style (owner, 9 Oct: text/logos/photos only, middle of the glass, no background).

**Status: DRAFT** – everything is done except the product photos. Rule 7 (real photos only) + the owner's "clean and crisp" rule mean they go ACTIVE (and onto Online Store, Shop, Google & YouTube, Facebook & Instagram, TikTok – none has a logo/badge) only once real-photo composites are attached. Blocked on `downloadscdn6.magnific.com` (Freepik full-size downloads) being allowed in the environment's network settings.

| Product | id | Handle | SKUs | Price |
|---|---|---|---|---|
| Face Photo "Hands Off!" | 16066542043517 | personalised-face-photo-pint-glass-hands-off | FOXY-UVDTF-PFHOPG-01 | £13.99 |
| Dad + gold script name | 16066542371197 | personalised-dad-pint-glass-gold-script-name | FOXY-UVDTF-PDNPG-01 | £11.99 |
| No.1 Grandad hexagon | 16066542862717 | personalised-no1-grandad-pint-glass | FOXY-UVDTF-PN1PG-01 | £11.99 |
| Prom (Design x Colour) | 16066543092093 | personalised-prom-pint-glass-tuxedo-bow-tie | FOXY-UVDTF-PPROMPG-01..12 | £11.99 |
| Wedding party (Role x Colour) | 16066544075133 | personalised-wedding-party-pint-glass-tuxedo | FOXY-UVDTF-PWPPG-01..12 | £11.99 |
| Vintage birthday | 16066544238973 | personalised-vintage-birthday-pint-glass | FOXY-UVDTF-PVBPG-01 | £11.99 |
| Pet photo | 16066544402813 | personalised-pet-photo-pint-glass | FOXY-UVDTF-PPFPG-01 | £13.99 |
| The [Surname] Arms | 16066544533885 | personalised-the-surname-arms-pub-pint-glass | FOXY-UVDTF-PSAPG-01 | £11.99 |

Prices: £11.99 = the other personalised pints; £13.99 for the two photo cut-out designs (owner to confirm).

Each product: unique copy (180–350 words, one h2; `copy-checks.json`), SEO title/meta, Google fields (Beer Glasses, unisex, adult, colour, mpn), product type Personalised Glassware, vendor Foxy Printing, `personalised` template, `foxy.mockup = drinkware`, `foxy.personalise_fields`, tags incl. `range-glassware`, `range-home-bar`, `foxy-new-2026`, `machine-uvdtf`, `io-pint-glasses`, `pint-range-2026-10-09` (auto-collections: Personalised Glassware, Personalised Printed Glassware, Home Bar; Dad/No.1 also landed in Father's Day). Unlimited (untracked, continue selling). No third-party names → no disclaimer.

Print files: 30 SVG/PDF (6 single + 12 prom + 12 wedding), 90 x 130 mm artboard + 3 mm bleed, design centred (~56 x 90 mm), CUT layer, live text, OFL fonts, min text 10.8pt. Shopify Files: **pint-range-artwork.zip** https://cdn.shopify.com/s/files/1/1774/9115/files/pint-range-artwork.zip?v=1791539274 (1,670,801 bytes, md5 756255220ebd0b1f74bdf9c3c43603d4, verified). Dropbox: 8 folders `/AI DESIGNS 2026/<title> - <SKU>/` with `README - how to print.txt` + `FONTS - DOWNLOAD LINK.txt` (texts in `dropbox-texts.json`).

Generators: `tools/pint_range/designs.py` (artwork), `products.py` (copy/data), `build.py` (print files + checks); `tools/artwork/bar_pairings.py` gained an `ellipse` element.

## To finish (when Freepik downloads work)
1. Download the nonic pint photo (A, already approved), composite each design with `tools/real_photo_glass/wrap.py` (+ prom/wedding: one image per design/colour shown), show the owner.
2. Face + pet designs need a real licensed stock photo of a person / dog for the sample (no AI faces).
3. Upload, attach with alt text, set ACTIVE, publish to the 5 channels, re-read.
