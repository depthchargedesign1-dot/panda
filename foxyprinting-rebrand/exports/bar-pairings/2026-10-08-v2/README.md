# Bar pairings v2: real glass print areas + the 20 older bar coasters modernised (8 Oct 2026)

Owner's answers (8 Oct 2026): "Pint glass print area can be 90 x 130 / Whiskey will be 50 x 50 / Coasters 90 x 90 / Yes safe [coasters dishwasher safe] / Metal signs fine / Yes modernise the coasters. Make sure they look real".

## 1. Glass artwork at the real print areas (10 products)
- New print files for the 6 personalised pint glasses at **90 x 130 mm** (w x h) and the 4 whisky tumblers at **50 x 50 mm**: 3 mm bleed (the background now runs into the bleed; v1 was clipped at the trim), 3 mm safe area, red RGB 255,0,0 0.25 mm CUT trim path (2.5 mm corners) on its own layer, live text (sample "Ava"), OFL fonts, transfer kept 10 mm below the rim. Tumbler designs (man cave, walnut) got tighter letter spacing so the small lines stay at 6 pt or more. Check render: `checks/glass-v2-print-files.png`.
- Shopify Files: **bar-pairings-artwork-v2.zip** https://cdn.shopify.com/s/files/1/1774/9115/files/bar-pairings-artwork-v2.zip (2,759,893 bytes, md5 77666e227a42a5122a57d637f6167bc9, verified after upload). Same coaster/sign files as v1 + the v2 glass PDFs/SVGs (all 17 club colourways) + `READ ME - v2 sizes.txt`; the old 70 x 90 / 70 x 60 placeholder glass files are left out (they stay in v1 `bar-pairings-artwork.zip` and in Dropbox). The v2 zip was first uploaded without glass bleed and replaced in place minutes later (same file id, `fileUpdate`); nothing deleted.
- Dropbox, each glass folder `/AI DESIGNS 2026/<title> - <SKU>/`: new `<SKU> - v2 90x130mm transfer [- Red and White] - PRINT.svg` / `- v2 50x50mm transfer - PRINT.svg` (md5 spot-checked against local) + `READ ME - v2 sizes.txt`. Beer O’Clock's SVG (8.7 KB of bubbles) is in the zip only, as in v1. Old files untouched.
- Product copy: all 10 glass descriptions got one new Size & details line: "Print area: up to 90 x 130 mm (width x height)" (pints) / "Print area: up to 50 x 50 mm" (tumblers). Tumbler capacity still not stated.
- `plan/artwork-specs.md` updated (placeholders/ASK removed for the print areas and coaster size). Generators: `tools/artwork/bar_pairings.py` (PINT/TUMBLER + bleed), `tools/bar_pairings/glass_v2.py`.
- **Not done:** the glass product images are still the drawn mockups made earlier today (CLAUDE.md rule 7 now says real photos only). They need real photos of the blank 20oz nonic pint and the whisky tumbler (see "Needs the owner").

## 2. Club colours coaster copy (personalised-club-colours-coaster)
Copy only (media untouched, another helper owns the images): Size & details now "Square coaster, 90 x 90 mm (printed edge to edge across the full 90 x 90 mm)" + "Dishwasher safe"; a "goes in the dishwasher after match night" note in the glossy-finish bullet; meta description now ends "90 x 90 mm and dishwasher safe."

## 3. The 20 older matching bar / man cave coasters
https://foxyprinting.co.uk/collections/bar-coasters and https://foxyprinting.co.uk/collections/man-cave-coasters (handles unchanged, all still ACTIVE, channels not touched).

| Key | Handle | New title | Website boxes |
|---|---|---|---|
| x21 | personalized-welcome-name-drinks-coaster-2 | Personalised Welcome Name Coaster – Blush Script Design | Name, Welcome line (optional) |
| x22 | personalized-your-bar-name-drinks-coaster | Personalised Bar Coaster – Emerald Flourish Design | Your name, Est. year (optional) |
| x23 | personalized-bar-name-crown-drinks-coaster | Personalised Bar Name Coaster – Crown & Copper Design | Bar name – line 1, line 2 (optional) |
| x24 | personalized-bar-name-purple-drinks-coaster | Personalised Bar Name Coaster – Plum Filigree Design | Bar name – line 1, line 2 (optional) |
| x25 | personalized-welcome-bar-name-drinks-coaster | Personalised Welcome Bar Coaster – Teal Welcome Design | Bar name, Welcome line (optional) |
| x26 | personalized-bar-name-drinks-coaster | Personalised Bar Name Coaster – Walnut & Gold Design | Bar name – line 1, line 2 (optional) |
| x27 | personalized-bar-name-establish-date-drinks-coaster | Personalised Bar Name Established Coaster – Olive Oval Design | Bar name ×2, Est. year, Welcome line (optional) |
| x28 | personalized-bar-name-establish-date-drinks-coaster-2 | Personalised Rustic Established Bar Coaster – Wood Effect | Bar name ×2, Est. year (optional) |
| x29 | personalized-bar-name-billiards-drinks-coaster | Personalised Pool Ball Bar Coaster – Rainbow Bubbles Design | Top row letters (up to 3), Bottom row letters (up to 4), Welcome line (optional) |
| x30 | personalized-bar-name-enjoy-your-time-drinks-coaster | Personalised Bar Name Coaster – Ruby Script Design | Bar name |
| o01 | personalized-man-cave-drinks-coaster | Personalised Man Cave Coaster – Slate & Gold Design | Whose cave? e.g. Dave’s (optional), Est. year (optional) |
| o02 | personalized-come-in-bud-drinks-coaster | Personalised Well Come In Bud Coaster | Name to replace ‘Bud’ (optional) |
| o03 | personalized-my-cave-my-rules-drinks-coaster | Personalised My Cave My Rules Coaster – Navy & Gold Design | Whose cave? (optional) |
| o04 | personalized-initial-drinks-coaster | Personalised Initial Coaster – Midnight & Red Monogram Design | Initial |
| o05 | personalized-my-cave-my-rules-drinks-coaster-1 | Personalised Man Cave Take a Sip Coaster – Whisky Glass Design | Whose cave? (optional) |
| o06 | personalized-my-cave-my-rules-2-drinks-coaster | Personalised My Cave My Rules Whiskey Coaster – Orange & Black Design (Jack Daniel’s disclaimer kept, `third-party-name`) | Whose cave? (optional) |
| o07 | personalized-your-name-drinks-coaster | Personalised Welcome Name Coaster – Burgundy Welcome Design | Name, Welcome line (optional) |
| o08 | personalized-enjoy-my-man-cave-drinks-coaster | Personalised Enjoy My Man Cave Coaster – Teal Retro Design | Whose cave? (optional) |
| o09 | personalized-welcome-man-cave-drinks-coaster | Personalised Welcome Man Cave Coaster – Blue & Gold Ribbon Design | Whose cave? (optional) |
| o10 | personalized-your-text-here-drinks-coaster | Personalised Your Text Coaster – Golden Lions Design | Line 1, Line 2, Line 3 (optional) |

(Full titles end "– 90mm Drinks Coaster…"; see `coaster-updates.json`.)

What changed on every one (productUpdate / metafieldsSet / tagsAdd / tagsRemove / fileUpdate alt; no productSet):
- New unique UK-English copy (230–290 words: one h2, Why you’ll love it, Size & details, Delivery, pairing line with the matching bar mat), from the Home bar sheet only: 90 x 90 mm, cork-backed MDF with a bright glossy top (live listings), dye-sublimation, **dishwasher safe**, sold singly; delivery = made to order, postage at checkout (no dispatch promise); the no-proofs line. o06 keeps its Jack Daniel’s disclaimer as the last block. "Personalized" gone from titles/copy (handles unchanged).
- SEO title (≤ 60) and meta (140–153 chars), trademark kept out of o06's SEO title. Vendor Foxy Printing, type Coasters, image alt text rewritten.
- Theme personalisation: `templateSuffix` personalised, `foxy.mockup` photo, `foxy.personalise_fields` as above (curly apostrophes).
- Tags: removed the Infinite Options trigger / collection tags they carried (`Custom Name` ×12, `Custom Date` ×2, `Custom Initial`, `Initial`, `Custom Text`, `Drinks Coaster` ×20, `Bar Coasters` ×9, `Man Cave Coasters` ×11). Added `drinks-coaster-2026`, `bar-coaster-2026` (the 9 that were in Bar Coasters) or `man-cave-coaster-2026` + `man cave` (the 11 in Man Cave Coasters), `io-bar-coasters`, `personalised`, `range-home-bar`, `home bar`, `coaster`, `bar coaster`, `machine-sublimation`, `bar-coasters-v2-2026-10-08`. New tags were added before old ones were removed.
- Collections: `man-cave-coasters` widened first to "Man Cave Coasters OR man-cave-coaster-2026" (any condition); `bar-coasters` and `drinks-coaster` already had the OR rules. Counts before → after: Printed Drinks Coasters 656 → 656, Bar Coasters 10 → 10, Man Cave Coasters 11 → 11, Football Coasters 353 (untouched). Home Bar, Garden Bar & Man Cave 180 → 194 (all 20 coasters now members through `range-home-bar`; 3 were already in by title; the count was still settling, and other sessions are editing too).
- Google fields (`mm-google-shopping`) were already complete and correct on all 20 (custom_product true, condition new, Home & Garden > Kitchen & Dining > Barware > Coasters, unisex, adult, Multicolor, mpn = SKU) and were re-checked, not rewritten.
- Re-read after: 20/20 OK (title, description, SEO, template, fields, mockup, Google fields, no old IO tags, `io-bar-coasters`, ACTIVE, alt text). Before-state saved in `coasters-before.json`.

### Images ("make sure they look real"): NOT changed, needs the owner
There is **no real photo of the 90 x 90 mm coaster blank** anywhere I could find: every coaster image in the store (the 20 + ~350 football / funny / VE / number-plate coasters) is a flat drawn mockup or an AI image, and the Dropbox coaster pictures (`/dcd print website/Brad Mockups tidy/coasters/`, Hartlepool and VE Day MOCKUPS, `Crest Coasters.jpg`) are Photoshop stock mockups (one carries an Envato watermark). Following rule 7, I did not draw or fake one and did not remove the current images (removing them would leave the products with no image). As soon as the owner sends real photos of a blank (or any printed) 90 x 90 coaster, I'll place each design on it with the right perspective, corners, edge and lighting, put it first and detach the flat images with `fileUpdate referencesToRemove`. Current images for reference: `checks/coasters-current-shop-images.jpg`.

### Production artwork (foxy-production-artwork skill)
- The 20 designs only existed as the owner's 2021 Illustrator files at **100 x 100 mm** with text in demo/commercial fonts (CreattionDemo, ROMANTICE, Butler, Caslon Titling, Boostard Signature, Rehn, Nexa, Nooa). New v2 print files: the original vector background with all old text removed (PyMuPDF redaction; o03's outlined text covered with its flat navy; x26's leftover outline strokes stripped), scaled 100 → 96 mm so the full design fills the **96 x 96 mm page = 90 x 90 trim + 3 mm bleed**, text re-set as **live text in OFL Google Fonts** (Cinzel, Great Vibes, Allura, Playfair Display, Montserrat, Zilla Slab) inside the 3 mm safe area. PDF layers Artwork + Text (fonts embedded); SVG groups Artwork / Text / Guides with text ids named after the website fields. Pre-cut blank, so no CUT layer. Check render: `checks/coasters-v2-print-files.png`.
- Shopify Files: **bar-coasters-v2-artwork.zip** https://cdn.shopify.com/s/files/1/1774/9115/files/bar-coasters-v2-artwork.zip (7,708,457 bytes, md5 b984a0fbcb9a5f42fd24a41af846a2c8, verified) = `<SKU>/<SKU> - 90x90mm coaster - PRINT.pdf/.svg` ×20 + `Fonts/*.ttf` + `Fonts/OFL.txt`.
- Dropbox: 20 new folders `/AI DESIGNS 2026/<new title> - <SKU>/` with `README - how to print.txt` (download link, sizes, boxes, design notes) and `Fonts/FONTS - DOWNLOAD LINK.txt` + `Fonts/OFL.txt` (copied from the first folder). PDFs/SVGs are 25 KB–2.6 MB with embedded artwork, so they live in the zip (text-only Dropbox connector). `coaster-dropbox-texts.json` = generated README text (the saved READMEs add short design notes for x26, x28, x29, o01–o03, o06, o10).
- Low-resolution backgrounds in the 2021 files: x26 walnut wood photo is about 87 ppi at print size and x28 rustic wood about 139 ppi (other photos are 300 ppi). Flagged in their READMEs.
- Generators: `tools/bar_coasters_v2/` (`spec.py` text positions + fonts, `art.py` print files, `coaster_copy.py` copy/fields/tags, `build_updates.py` Shopify batches, `package.py` zip, `dropbox_texts.py`).

## Needs the owner
1. **Real photos** of the blank 90 x 90 coaster, the 20oz nonic pint glass and the whisky tumbler (straight-on + 45°, plain background, good light). Then the 20 coasters and the 10 glasses can get real-photo images (rule 7); until then they keep their current drawn images.
2. Whisky tumbler **capacity** (still not stated anywhere).
3. Proof-print one v2 glass transfer and one v2 coaster to confirm sizes/colours (new fonts replace the 2021 ones).
4. x26 / x28 wood backgrounds are low-res (87 / 139 ppi): OK as is, or replace with better wood textures?
5. From the earlier README: unpublish "My Cave My Rules Whiskey" coaster (Jack Daniel’s bottles) from Google/FB/IG/TikTok? (I can't unpublish.) Also check in Infinite Options that no option set still attaches to these 20 by collection (they no longer carry any of the old trigger tags).
6. Optional tidy-up later: the v1 placeholder glass files in Dropbox (`transfer 70x90mm` / `70x60mm`) can be deleted by the owner if wanted.

## Pairing ideas (not made)
Set-of-4 version of each bar coaster (same design, four names); "Home Bar Gift Set" (matching bar mat + 2 coasters + pint glass in the same design); matching bar-name pump clip or beer mat (cardboard) for the Crown & Copper / Rustic Established ranges.
