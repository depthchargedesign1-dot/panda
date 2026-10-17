# Personalised number plate mug: blank live-preview plate + "squeeze" text fitting (8 Oct 2026)

Product: https://foxyprinting.co.uk/products/personalised-number-plate-mug-any-name (`gid://shopify/Product/16064473629053`, SKUs FOXY-SUB-PNPMANOT-01..05).
Owner asked: "make a blank numberplate where people can edit live online and the text and font fits in the design nice same height just squeeze in the text".

## What changed

### 1. Blank plates, one per country band (LIVE now)
- Made with the other session's own generator (`tools/artwork/any_name_number_plate_mug.py` on branch
  `claude/designer-bots-mug-products-auuvhs`, `texture("", "", country)`) + `number_plate_mug_local_mockups.flat()` on this branch,
  so they match the product's flat-plate image exactly (GB blank vs. the old blank base: mean pixel difference 0.01).
  Script: `test/make_blanks.py`. Files: `preview-blanks/FOXY-SUB-PNPMANOT-preview-blank-{GB,SCO,CYM,NI,IRL}.jpg` (2048 x 2048).
- Uploaded to Shopify Files (READY): GB `69884517712253`, SCO `69884517745021`, CYM `69884517777789`, NI `69884517810557`, IRL `69884517843325`.
- Why the flat plate and not the mug photo: on the mug photos only the first 3 letters of the plate are visible (it wraps round the mug),
  so customers couldn't see their whole text. The flat plate shows the full plate.
- `foxy.preview_base` = GB blank (`gid://shopify/MediaImage/69884517712253`).

### 2. `foxy.preview_zone` (set 8 Oct, LIVE)
Measured in pixels on the 2048 px blank (plate inner border y 737–1290, yellow area x 412–1909) and taken from the print geometry
(text box = 0.94 x the 155 mm area between band and border, cap height 72% of the 64 mm plate):
- main text: x 0.2396, y 0.3923, w 0.6502, h 0.2057 (= 491, 803, 1332 x 421 px); with a dealer line it moves to y 0.3894, h 0.1829 (64% plate height, 3.2 mm higher), like the print file.
- dealer line (nested in `also`): x 0.288, y 0.6023, w 0.5534, h 0.0152 (3.4 mm cap height, baseline 4.6 mm above the plate edge), only drawn when filled in.
- `"fit":"squeeze"`, `"fitFont":"Barlow Condensed"` (weight 700, the print font), `"transform":"plate"` (capitals, A–Z 0–9 and spaces only, same cleaning as the print generator), `"letterSpacing":0.035`, `"placeholder":"Y0UR N4ME"`,
  `"bases"`: one blank per Country option value (GB / Scotland / Wales / Northern Ireland / Ireland).
- `"font":"Bebas Neue"` kept for the current live theme (it ignores the new keys and draws the plate text as before, in Bebas Neue, on the new blank).

### 3. Theme: `assets/personaliser.js` in new unpublished copy **"Foxy Pop 2026 – plate squeeze" (`189519069565`)**
"Foxy Pop 2026 – poster tidy" (189518610813) had been PUBLISHED by the owner by the time this ran (role MAIN), so it could not be
edited (never edit the live theme). Duplicated it to "plate squeeze" and changed only `assets/personaliser.js`
(md5 `1b76c0414cd831e0f9396f179a16a4d2`, re-read from the store and matches `theme-working-copy-leavers-designer/assets/personaliser.js`).
All new behaviour is opt-in per zone, so other products are unchanged:
- `"fit":"squeeze"`: font size set so the capital height = zone height (always the same height), text centred, and squeezed
  horizontally (scaleX < 1) only when it's wider than the zone. Never shrunk in height.
- `"fitFont"`: loads that font from Google Fonts (OFL) only for squeeze zones that need it.
- `"field"` (pick a box by label text), `"optional"` (draw nothing when empty), `"transform"`, `"placeholder"`, `"weight"`, `"letterSpacing"`, `"whenFilled"`, `"also"` (extra zones, ignored by old theme versions).
- `"bases"`: on a Country change the preview switches to that band's blank plate. **Fixes a live bug:** the current theme swaps the
  preview to the variant photo (the mug with "YOUR NAME" on it) whenever the country is changed or the confirm box is ticked, and then
  draws the customer's text on top of the mug photo.

**Owner: preview and publish "Foxy Pop 2026 – plate squeeze"** for the squeeze fitting, Barlow Condensed lettering, dealer line and
per-country blanks to go live:
https://foxyprinting.co.uk/products/personalised-number-plate-mug-any-name?preview_theme_id=189519069565
Until then the live site already shows the new blank GB plate with the text drawn in Bebas Neue (shrinks to fit, as before).

## Test (`test/test.js`, Playwright + /opt/pw-browsers/chromium, the real personaliser.js, the 5 blanks, local OFL fonts)
Screenshots in `screenshots/` (contact sheet: `screenshots/contact-sheet.png`): empty (placeholder), BOB, DAD 50, GRANDAD1,
WWWWWWWW and MMMM MMM (widest 8-character texts), GRANDAD1 + "Dad’s Garage", BOB on Wales, DAD 50 on NI, "dav3 5!" (cleaned to DAV3 5).
Measured on the 1000 px canvas (zone y 392–598, x 240–890): every text is 205–212 px tall (round letters overshoot a little) and
sits inside x 242–886, so it always fills the plate height, is centred and never overflows. Country change loads the right blank.
Also checked that the current live personaliser.js still draws the plate text on the new blank with the new zone (no errors).

## Print file vs. preview: MISMATCH for the owner
The print generator (`tools/artwork/any_name_number_plate_mug.py`, other session's branch, not changed here) uses the same font,
position and text cleaning, but fits long text by **shrinking the whole text (height too)**, not squeezing:

| text | print file capital height | preview capital height (squeezed to) |
|---|---|---|
| BOB | 46.1 mm | 46.1 mm (no squeeze) |
| DAD 50 | 37.2 mm | 46.1 mm (82% width) |
| GRANDAD1 | 25.8 mm | 46.1 mm (57% width) |
| WWWWWWWW | 17.4 mm | 46.1 mm (38% width) |

Its README also says "shrink it if it runs past the plate border" for hand edits. To match what customers now see, the generator
(and hand edits) should keep the font size and squeeze horizontally, e.g. SVG `textLength="<box width>" lengthAdjust="spacingAndGlyphs"`
on the "Plate text" object only when the text is wider than the box (in Illustrator: Horizontal Scale < 100%). Same for the dealer line.
Ask that session (or say the word) to add a squeeze mode before the next order is printed.
