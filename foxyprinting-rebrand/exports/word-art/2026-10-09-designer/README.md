# Word Art Designer (9 Oct 2026)

Owner: "any products that are online must have the options for the designer to upload their own words into our artwork and order. we then must use the options to save the printed ready file on dropbox with order number".

## What's built (v1, in shared working copy "Foxy Pop 2026 – plate squeeze" 189519069565, unpublished)
- `assets/word-art-designer.js` (engine + UI), `assets/word-art-designer.css`, `snippets/word-art-designer.liquid`, plus one render line in `sections/main-product.liquid` (after `#infiniteoptions-container`).
- Shows on every product tagged `Word Art` (or `wa-upload` for Create your own). It hides the old two-box panel while running and gives it back if it can't start.
- Customer: Name + Words → live preview of our artwork shape filled with the words (word cloud on an occupancy grid, name once and big, 0°/90°), Shuffle (new seed), 9 colour schemes ("Original" = the artwork's own colours), 9 Google fonts (OFL).
- Add to basket / Buy it now: renders the print file at A4–A1 + 3 mm bleed, up to 300 dpi (capped at 16.7 MP for phones: A4 300, A3 ~288, A2 ~205, A1 ~145 dpi). Text is redrawn at print size (not upscaled). Posted with multipart `/cart/add.js` as `_Print file`, plus `Name`, `Words`, `Colours`, `Font`, `Layout code` (`WA1.<seed>.<scheme>.<font>`), `_Print spec`, and (Create your own) `_Your picture`.
- Tested in a local Playwright harness (real theme CSS): desktop + phone, letter/number/picture/upload shapes, basket post captured (A3 frame line → 3436×4830 PNG; A1 → 4835×3425). Screenshots: `screenshots/`.

## Shapes (`foxy.word_art_mask`, file_reference to an RGBA PNG)
- 52 Pink/Blue letters: drawn from Russo One (`tools/word_art_designer/letter_masks.py`), coloured from the original (the photos have a big example name across the letter).
- 167 others: traced from the black-frame photo (`tools/word_art_designer/make_masks.py`): paper found inside the frame, words merged into a smoothed silhouette, colours spread across it.
- `foxy.word_art_off = true` (old two boxes stay): 10 broken traces + 3 products with no image, listed in `mask-review.json` / `masks-final/manifest.json`.
- `mask-review.json` → `example_name`: 9 designs where the example name "Anna" is part of the artwork (usable, but worth re-tracing).
- Masks were imported to Shopify Files from this repo (public raw GitHub URL, pinned commit).

## Create your own
`create-your-own-word-art-print` (gid://shopify/Product/16066581430653), **DRAFT** until the owner approves. Tag `wa-upload`, 8 sizes, same prices, SKUs `FOXY-POSTER-WA-CREATE-*`, Google fields, SEO. Images: a real store black-frame photo with a designer-made dolphin print composited in, plus the flat print.

## Dropbox
See `DROPBOX-SAVING.md`. Recommended: Shopify Flow "Order created" → Dropbox `files/save_url`; the owner sets up the Dropbox app and key.

## To do
- Re-trace the 10 broken + 9 "Anna" designs from Ben's HQ originals (`/BENS FILES/OLD STUFF/WORD ART HQ JPEG/`).
- Re-make page for Layout codes (production).
- Owner: preview/publish plate squeeze; set up Flow; approve Create your own.
