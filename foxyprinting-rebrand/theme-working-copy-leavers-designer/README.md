# Leavers designer theme: changes made from this session (8 Oct 2026)

"Foxy Pop 2026 – leavers designer" (189501276541) was built in the owner's other session (branch
claude/zealous-wozniak-qzr6bg, folder leavers-designer/). The owner PUBLISHED it on 8 Oct 2026 (~14:50 UTC).
Before it went live this session changed, in that theme:
- assets/leavers-designer.js / .css: small round colour swatches (two-tone split) + "Colour: <name>" line,
  full-width "School name (in full)" box (80 chars), always-visible "All pupils' names in full" list box,
  name boxes 32 -> 40 chars.
- snippets/personaliser-field.liquid: the "(optional)" fix from "optional fields" (189502947709).

New unpublished copy "Foxy Pop 2026 – swatches & posters" (189514809725), duplicated from the live leavers theme:
- sections/main-product.liquid: Colour options shown as round swatches (snippets/colour-hex.liquid maps names to
  colours; unknown colours stay text pills); text boxes with "school" allow 80 chars; message boxes with "name"
  (a whole class list) allow 3000 chars.
- snippets/colour-hex.liquid (new).
- sections/main-collection.liquid from "mug tiles" (Shop by type tiles, compact banners). All files checksum-verified against the store 8 Oct 15:05 UTC.

## 8 Oct 15:42 UTC: leavers session merged into the shared copy 189514809725
The "Leavers hoodies designer tool" session (branch claude/zealous-wozniak-qzr6bg) three-way merged our swatch/name-box
changes and upserted only its own files: assets/leavers-engine.js (efc6d66e…), leavers-designer.js (a24d74ba…, still has
the round swatches, Colour line, 80-char school box, always-visible names box, 40-char names), leavers-designer.css
(b465c692…), leavers-photos.js (1fa94e2e…). Verified against the store. Its source of truth for those files is now that
branch (leavers-designer/theme/assets/); the copies in this folder's assets/ are the older pre-merge versions.
Do NOT publish "Foxy Pop 2026 – leavers logo upload" (189515399549): superseded by 189514809725.

## 8 Oct: Celebrity Posters mega-menu promo (celebrity-posters session)
- sections/header-group.json in 189514809725: new "Department style" block `d8` for the menu item "Celebrity Posters"
  (accent purple, eyebrow "New department", heading "Music, film & sport star posters with printed signatures",
  button "Shop posters", image `shopify://shop_images/TaylorSwift.jpg`, link /collections/celebrity-posters), placed
  after the Celebrity Masks block. Store checksum after upsert: f06f80c43f3d262a94d8d46bf3730fbb (matches this file).
  No other header file changed: the live header.liquid already renders any 3-level menu item as a mega panel, so the
  new "Celebrity Posters" menu item works on the live theme now; the promo tile appears once this copy is published.

## 8 Oct ~17:30 UTC: "Foxy Pop 2026 – poster tidy" (189518610813), duplicate of the live "swatches & posters"
- sections/main-product.liquid (md5 1f4eebad…, this folder): option values longer than 8 characters (poster sizes "A4 Print Only",
  "A3 Print + Silver Frame") render as an even grid of equal buttons (`option-pills--grid`, 2 columns on phones);
  description headings h1/h2 1.3rem, h3/h4 1.05rem, inline font styles/tables in old descriptions neutralised.

## 8 Oct ~17:10 UTC: "Foxy Pop 2026 – plate squeeze" (189519069565), duplicate of the live "poster tidy"
"poster tidy" (189518610813) was already PUBLISHED (MAIN) when the number plate mug work ran, so it was duplicated.
- assets/personaliser.js (md5 1b76c0414cd831e0f9396f179a16a4d2, this folder; base = live 8214edfb…): opt-in preview_zone keys
  `fit:"squeeze"` (same capital height, centred, squeezed horizontally only when too long), `fitFont` (Google Font loaded only
  for those zones), `field`, `optional`, `transform` ("upper"/"plate"), `placeholder`, `weight`, `letterSpacing`, `whenFilled`,
  `also` (extra zones) and `bases` (blank base image per variant option instead of the variant photo). Other products unchanged.
  Used by the personalised number plate mug; record: exports/number-plate-mug/2026-10-08/README.md.
- Put further theme changes in this copy (it is live + this one file). Owner to preview and publish.
