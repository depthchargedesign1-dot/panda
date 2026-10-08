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
