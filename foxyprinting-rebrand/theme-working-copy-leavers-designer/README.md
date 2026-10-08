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
- Still to port: sections/main-collection.liquid from "mug tiles" (theme-working-copy/).
