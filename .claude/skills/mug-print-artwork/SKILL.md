---
name: mug-print-artwork
description: Build print-ready Foxy Printing mug artwork from a design spec - 300 dpi wrap PNG, vector PDF with live (editable) text, mirrored PDF, layered editable SVG, proof, white-background mockups and a zip with fonts. Use for any new mug design, and to personalise an order (name, number, date) from an existing spec.
---

# Mug print artwork (mugkit)

The engine is `scripts/mugkit.py` (+ `scripts/render.js`). One JSON spec in, every print file out.
Text is always **live text** (never baked into an image) so personalised fields stay editable.

## Where to run it
1. **Here, if you can**: needs python3 + Pillow + numpy, node + playwright (Chromium) and internet for
   Google Fonts. Claude Code cloud sessions have all of this.
   `python3 scripts/mugkit.py all spec.json --out OUT`
2. **Otherwise in the Higgsfield sandbox** (`mcp__Higgsfield__sandbox_exec`, has internet, node + Playwright):
   ```
   B=https://raw.githubusercontent.com/depthchargedesign1-dot/panda/claude/designer-bots-mug-products-auuvhs/.claude/skills/mug-print-artwork/scripts
   curl -sfLO $B/mugkit.py && curl -sfLO $B/render.js && pip install -q numpy pypdf >/dev/null
   cat > spec.json <<'EOF'
   ...spec...
   EOF
   NODE_PATH=$(npm root -g) python3 mugkit.py all spec.json --out out
   ```
   The sandbox is wiped ~10 s after each call, so do build + upload in ONE command: call
   `mcp__Higgsfield__media_upload` first (one entry per file you need: the zip, the mockups, the 300dpi PNG),
   then append `curl -sf -X PUT -H 'Content-Type: <type>' --data-binary @"out/<file>" '<upload_url>'` for each,
   then `media_confirm`. Look at the PROOF with `image_paths` in the same call before uploading.

## Spec format
```json
{
  "sku": "FOXY-SUB-XXXX-01", "name": "short design name (file names)", "title": "full product title",
  "size": "11oz",                      // 11oz = 200x70 trim (+3mm bleed = 206x76, 2433x898 px); 11oz-85; 15oz
  "background": "#ffffff", "background_image": "optional.png (cover, full bleed)",
  "defaults": {"Name": "SMITH"},       // sample values for personalised fields
  "elements": [ ... ]
}
```
Every element has `panel`: `left` | `right` | `full` and `dx_mm` (offset from the panel centre).
Left panel shows with the handle on the left, right panel with the handle on the right.
- `text`: `text` or `field` (personalised), `font` ("Oswald:700" - any Google Font family:weight),
  `size_mm`, `y_mm` (BASELINE, from trim top), `max_w_mm` (auto-shrinks long names), `color`,
  `outline {color,width_mm}`, `upper`, `align`, `spacing_mm`.
- `image`: `src` (path or https URL - AI art from Higgsfield), `y_mm`, `w_mm`, `h_mm` (fit inside box).
  Generate art with NO lettering; set all words as `text` elements.
- `shirt`: football shirt - see the `football-shirt-mug` skill.
- `rect`: `dx_mm`, `y_mm`, `w_mm`, `h_mm`, `r_mm`, `color` (rules, bars, badges).

## Personalising an order
`python3 mugkit.py build spec.json --out "ORDER 1234" --set Name=O'CONNOR --set Number=7`
Fields are the `field` names in the spec. Long names shrink to fit their box automatically.

## Outputs (base = "<SKU> <name> - <size> wrap <W>x<H>mm")
`<base> - 300dpi.png` (300 dpi metadata), `<base>.pdf` (live text, editable in Illustrator/Acrobat Pro;
TrimBox/BleedBox set), `<base> - MIRRORED.pdf`, `<base> (editable).svg` (layers Background / Artwork /
Personalisation, field ids = field names), `<base> - PROOF.jpg`, mockups 0-3 (pure white background,
Amazon-safe), `README - how to print.txt`, `<SKU> - print artwork.zip` (all of the above + Fonts/).

## Saving (house rules)
- Dropbox root for new mugs: `/AI DESIGNS 2026/NEW MUGS/<Product title> - <SKU>/` (create the
  `NEW MUGS` folder once if missing).
- The Dropbox connector only writes TEXT files. Save there: `README - how to print.txt`, the
  `(editable).svg` when it is pure vector (shirt / text designs - it is small), the spec as
  `<SKU> spec.json`, and `DOWNLOAD LINK.txt` pointing at the zip.
- Put the zip in Shopify Files: GraphQL `fileCreate(files:[{originalSource:"<cloudfront url>",
  contentType:FILE, filename:"<SKU> - print artwork.zip"}])`, poll until READY, use the cdn.shopify.com URL
  in `DOWNLOAD LINK.txt` (same layout as the existing number-plate mug folders).
- Check the PROOF before anything goes live: text inside the blue safe line, nothing important across
  the panel gap, names spelt right.
