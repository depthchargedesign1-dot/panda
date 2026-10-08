# Foxy Leavers Designer

A leavers-hoodie designer for foxyprinting.co.uk. Customers pick a garment colour and a back design, add their year group's names, choose fonts and print colours, add a front design and a personal name, check a live preview and the actual print files, then order for themselves or for a whole group. Every order line carries a link that regenerates the exact 300 dpi print files.

## What's in here

| Path | What it does |
| --- | --- |
| `theme/assets/leavers-engine.js` | Rendering engine shared by everything: layouts, fonts, garment mockups, 300 dpi PNG export, design codes |
| `theme/assets/leavers-designer.js` / `.css` | The product-page designer app |
| `theme/assets/leavers-print-studio.js` | Staff Print Studio: link from the order → print-ready PNGs |
| `theme/sections/leavers-designer.liquid` | Shopify product section (reads variants, posts to `/cart/add.js`) |
| `theme/sections/leavers-print-studio.liquid` | Shopify page section for the Print Studio |
| `theme/templates/product.leavers-designer.json` | Product template, set as the template on every leavers product |
| `theme/templates/page.leavers-print-studio.json` | Page template for `/pages/leavers-print-studio` |
| `demo/index.html`, `demo/print-studio.html` | Run the designer and studio locally without Shopify (open in a browser) |
| `tools/render-print-files.mjs` | Command-line / server renderer (Playwright Chromium, same engine) |

## Range (AWDis Just Hoods blanks from Ralawise)

| Garment | Tag | Sizes | Price | Colours | Back print |
| --- | --- | --- | --- | --- | --- |
| College Hoodie 2.0 (JH001) | `ld-college-hoodie` | Kids 3-4 to 12-13 yrs, adult XS–5XL | kids £15.99, adult from £18.99 | 46, every one a real AWDis photo (front and back) | adult 400×500 mm, kids 300×375 mm |
| Baseball Hoodie (JH009) | `ld-baseball-hoodie` | XS–2XL | from £21.99 | 13 body/sleeve colourways | 400×500 mm |
| Varsity Jacket (JH043) | `ld-varsity-jacket` | XS–2XL | from £29.99 | 16 body/sleeve colourways | 400×480 mm |

Names, front print and a personal nickname are included in every price.

### Garment photos

The previews use real AWDis studio photos from Dropbox (`/New Jobs 2026/3025 awdis hoodie colours`, plus the Ralawise JH009/JH043 shots). `tools/process-photos.py` places every photo on the same 1000 × 1000 frame so one set of print positions fits every colour. It writes them to `garment-photos/`. The photos are hosted in Shopify Files, and `tools/build-photo-manifest.py` writes `theme/assets/leavers-photos.js`, which lists them.

- **College Hoodie:** a real front and back photo for every colour. Combat Green is left out because there is no back photo yet.
- **Varsity Jacket and Baseball Hoodie:** only some colourways had a real photo, and none had a back. The other colourways are recoloured from a real photo of the same garment, and the backs are retouched from the real fronts. Drop the Ralawise `_bk` back shots into Dropbox and re-run the two scripts to replace them.

**Back designs (9):** Names in the Year, Heart of Names, Star of the Show, Stacked Block, Class Of, College Badge, Squad Shirt, Name Wall, Year Only.
**Front designs:** plain, chest badge (text and icon), varsity letter, uploaded school logo, big college front (arched), big stacked front.
**Personal name:** down the sleeve, front right chest, or above the back design.
**Fonts:** 26 Google Fonts in Bold, Varsity, Script, Fun and Classic groups. **Print colours:** 16.

## How an order becomes a print file

1. The designer adds one basket line per hoodie, with readable properties (colour, back design, names count, fonts, colours, front, personal name). It also adds two hidden properties:
   - `_Print files`: `https://foxyprinting.co.uk/pages/leavers-print-studio#d=<code>`. The code is the full design, compressed. It sits in the URL fragment, so it is never sent to a server.
   - `_Group design`: a short reference that is the same for every hoodie sharing one back design, so a group order can be batched.
2. In Shopify admin, open the order and click the `_Print files` link. The Print Studio shows the mockups, every name for a spelling check, and a **Generate print files** button. It produces transparent PNGs at 300 dpi, with the dpi written into the file so RIP and DTF software opens them at the correct physical size.
3. Or render the files without opening anything:

```bash
node tools/render-print-files.mjs "<_Print files link>" --out print-files --prefix order1042
node tools/render-print-files.mjs --order order.json --out print-files   # Shopify order JSON / webhook payload
```

An uploaded logo is stored by Shopify with the first basket line, and its CDN URL is written into every design code.

## Install on a theme

Upload the files in `theme/` to the theme. Tag each product `ld-<garment>`, give it a single **Size** option, and set its template to `leavers-designer`. The garment picker lists the products in the collection set in the section's "Range collection" setting (only active products appear). Create a page with the handle `leavers-print-studio` using the `leavers-print-studio` template.
