---
name: foxy-leavers-designer
description: Build, change, test and deploy the Foxy Printing leavers hoodie designer (Shopify product-page app where customers add names, fonts, designs and a school logo, preview, order, and staff generate 300 dpi print files). Use for any work on leavers hoodies/varsity jackets, the designer, the Print Studio, garment photos, or deploying it to foxyprinting.co.uk.
---

# Foxy Leavers Designer

All code is in `leavers-designer/` (see its `README.md` for the full feature list). This skill covers how to work on it and get changes live safely.

## Map

| Path | Role |
| --- | --- |
| `theme/assets/leavers-engine.js` | `window.LeaversEngine`: products, print areas, fonts, inks, back/front templates, layout, mockups on real photos, 300 dpi PNG export, design codes (`encode`/`decode`), prices |
| `theme/assets/leavers-designer.js` / `.css` | Customer app: 7 steps (garment and colour swatches, back design, wording and names, fonts and colours, front design and school logo, personal name, sizes and order) |
| `theme/assets/leavers-print-studio.js` | Staff page `/pages/leavers-print-studio`: open an order's `_Print files` link and download PNGs |
| `theme/assets/leavers-photos.js` | Generated list of garment photo URLs (Shopify Files CDN). Do not edit by hand |
| `theme/sections/leavers-designer.liquid`, `leavers-print-studio.liquid`, `theme/templates/*.json` | Shopify glue |
| `tools/process-photos.py` → `tools/build-photo-manifest.py` | Raw AWDis photos → `garment-photos/` (1000×1000, recoloured, backs retouched) → `leavers-photos.js` |
| `tools/render-print-files.mjs` | Headless print-file renderer (`<link>` or `--order order.json`) |
| `demo/index.html`, `demo/print-studio.html` | Local test pages (demo mode, no Shopify) |

Key engine rules:
- Layout uses a 1000-unit reference width, so the preview, proof and print file always match.
- Each product has `areas` (mm) and `photo` placement. College Hoodie also has `kidsAreas`, used when `d.size` is a kids size.
- Hidden design fields start with `_` and are stripped from codes.

## Range and store (foxyprinting.co.uk)

| Product | AWDis | Shopify ID | Price |
| --- | --- | --- | --- |
| College Hoodie 2.0 | JH001 | 16065598292349 | kids £15.99, adult £18.99 (+£2 2XL/3XL, +£4 4XL/5XL) |
| Baseball Hoodie | JH009 | 16065598325117 | £21.99 (+£2 2XL) |
| Varsity Jacket | JH043 | 16065598521725 | £29.99 (+£2 2XL) |

- Collection: `design-your-own-leavers-hoodies-2026` (gid 690657034621). Products are tagged `ld-<garment>` and use template `product.leavers-designer`.
- Print Studio page: gid 699784036733.
- Photos live at `https://cdn.shopify.com/s/files/1/1774/9115/files/<filename>`.
- Prices must stay cheaper than schoolleaverscompany.co.uk.

## Test before deploying

```bash
node <script>.mjs   # Playwright: import from /opt/node22/lib/node_modules/playwright/index.mjs
```
Open `file:///home/user/panda/leavers-designer/demo/index.html`. `window.app.design` is the live design. Check:
- page errors
- `LeaversEngine.renderPrintFiles(window.app.design, {dpi: 50})`
- screenshots of the front, back and close-up views

Look at the screenshots yourself. Back prints must be big (about 90% of the back width).

## Deploy (the live theme is write-protected)

The Shopify MCP blocks `themePublish` and any write to the MAIN theme. Never try to work around that.

1. Commit and push to the working branch, and note the commit SHA.
2. Find the MAIN theme with `themes { nodes { id name role } }`.
3. Run `themeDuplicate` on the MAIN theme, named e.g. "Foxy Pop 2026 – <change>".
4. Run `themeFilesUpsert` on the copy, with each file as `{type: URL, value: https://raw.githubusercontent.com/depthchargedesign1-dot/panda/<SHA>/leavers-designer/theme/<path>}`.
5. Verify the upload: the copy's `files(filenames: [...]) { checksumMd5 }` must equal the local `md5sum`.
6. Give the user a preview link, `https://foxyprinting.co.uk/products/design-your-own-leavers-college-hoodie?preview_theme_id=<id>`. Ask them to publish the copy in Online Store → Themes.

Photos and product media need no theme write:
- Upload photos with `fileCreate`, using a new filename (e.g. `-v2`) so the CDN cache can't serve the old image.
- Swap product media with `fileUpdate`.

## Where the artwork goes after an order

Nothing is saved as a file automatically. The design itself travels with the order:

- **On the order:** every line item carries readable properties (garment, colour, back design, names count, fonts, colours, front, school logo, personal name). It also carries two hidden ones:
  - `_Print files`: a link to the Print Studio. The whole design is compressed into the `#d=` code.
  - `_Group design`: lines with the same value share a back, so they can be batched.
- **Generating the print files:** a staff member opens the `_Print files` link from the order in Shopify admin and clicks Generate. They get transparent PNGs at 300 dpi, saved to their computer's Downloads. Alternatively, run `tools/render-print-files.mjs`.
- **School logo:** the original is uploaded to Shopify with the order. Its CDN URL is in the "School logo" property and inside the design code.
- **Fonts:** print files refuse to render with fallback fonts, so the output never silently changes.

## Gotchas

- `.ld [hidden]` uses `display: none !important`. Keep it, or hidden fields reappear.
- Re-render on the `leavers:photo` event and on fonts `loadingdone`, or the first paint shows missing photos or fonts.
- The default colour should be dark (`defaultColour`), because the default ink is white.
- Varsity and Baseball backs are retouched from front photos. If the user says a back "looks like the front", the collar/neckline is the tell: see `back_collar` in `process-photos.py`.
- Combat Green (College) is skipped because there is no back photo.
