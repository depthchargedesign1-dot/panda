---
name: foxy-production-artwork
description: Make editable, print-ready production artwork for a Foxy Printing product (print files, cut/crease files for the Intec ColorCut flatbed, fillable PDFs) and save it in its own named folder inside "/AI DESIGNS 2026" on Dropbox. Use whenever the owner asks for artwork, a print file, a cut file, a dieline, an editable PDF or a template for a product.
---

# Foxy Printing production artwork

Owner's rules (5–6 Oct 2026):
- **Every new product gets print-ready artwork with bleed** (3 mm on every trimmed or cut edge, or the wrap bleed from artwork-specs.md), a 3 mm safe area, and 300 dpi images, made before the product goes live.
- **Every product gets its own folder** in Dropbox: `/AI DESIGNS 2026/<Product title> - <SKU>/` (e.g. `/AI DESIGNS 2026/Halloween Treat Boxes - FOXY-CUT-HTBPO1-01/`). Never dump files loose in `/AI DESIGNS 2026`, and don't edit its INDEX.md.
- Files must be **editable**: live text for anything the customer personalises (name, age, message), vectors where possible.
- **Never delete, move or overwrite anything in Dropbox.** Only create new folders/files. If a saved file is wrong, save a "(fixed)" copy and tell the owner which one to delete.

## 1. Gather facts first
- Product: title, SKU (first variant), personalisation fields (`foxy.personalise_fields`), product photos (to match the look).
- Size, material, sheet size, how it's cut/folded: from `foxyprinting-rebrand/plan/product-facts.md`. If missing, ask the owner once (AskUserQuestion, with sensible options) and record the answers in the fact sheet.
- Look at the product photos (Higgsfield `sandbox_exec` with `image_paths`, since our own sandbox can't reach cdn.shopify.com) so the artwork matches what customers see.

## 2. Build the artwork (Python, reportlab — installed locally)
- Write the generator as a script in `foxyprinting-rebrand/tools/artwork/<product>.py` (see `halloween_gable_box.py` as the pattern) so it can be re-run for changes.
- Units in mm. Page = the real print sheet (SRA3 = 450 × 320 mm landscape, A4 = 210 × 297 mm). **3 mm bleed** past every cut line.
- Output both **SVG** (opens in Illustrator; top-level groups `Artwork` and `CUT` become layers) and **PDF** (real PDF layers `Artwork` and `CUT` via pikepdf, see `mask_cutline.py`).
- **Fillable PDFs** (letters, certificates, kits): reportlab `acroForm` text fields, named after the customer fields (e.g. `Child_name`, `Age`); reuse the same field name wherever the same value repeats.
- Fonts: standard PDF fonts (Helvetica/Times) always work; a handwriting look can use Patrick Hand (OFL) inside the Higgsfield sandbox (https://github.com/google/fonts/raw/main/ofl/patrickhand/PatrickHand-Regular.ttf). Our sandbox can't download fonts.
- Background art (borders, illustrations) can be generated with Higgsfield `gpt_image_2_5` (high, 4k) using the product photo as reference — **no text in generated images**; put text in as live text.

## 3. Cut and crease lines for the Intec ColorCut (ColorCut Pro)
From Intec's ColorCut Pro FB550 user guide (sections 4–7):
- Cut lines go on their **own layer called `CUT`** (owner's rule, 5 Oct 2026), separate from the print artwork; they never print.
- ColorCut Pro recognises **8 line colours** (RGB or CMYK); spot/Pantone colours must be converted to one of them. House convention:
  - **Red** RGB 255,0,0 / CMYK 2,98,95,0 → **Cut** (blade)
  - **Blue** RGB 0,0,255 / CMYK 91,80,1,0 → **Crease** (creasing tool)
  - Yellow 4,2,98,0 → Score (half-depth blade); Green 76,0,100,0 → Perforate — only if needed.
- Stroke 0.25 mm, no fill. Closed paths for outlines and holes.
- **PageMARKs (registration marks, 10 × 4 mm, 100% K) and the job barcode/QR are added by the owner** in Illustrator with the ColorCut Pro plug-in ("ADD PageMARKs & BarCode"), which stores the job in their Job Library. We can't generate that barcode (it's tied to their cutter PC). Keep the artwork clear of a **12 mm margin on the left and 10 mm on the other edges** of the sheet for the marks and barcode.
- The owner's Illustrator scripts automate the layer setup and print-PDF saving: `/AI DESIGNS 2026/00 Foxy Illustrator Scripts - ColorCut/` (source in `foxyprinting-rebrand/tools/artwork/illustrator/`). "Foxy - 1 Prepare cut file" moves red/magenta/blue lines to the "CUT" layer (renames an old "Cut lines" layer) and swaps the sample name (keep the sample name "Ava" in new artwork, or update the script); "Foxy - 2 Save print PDF" saves the .ai and a "- PRINT.pdf" without cut lines. Only the plug-in's ADD PageMARKs & BarCode click is manual. For a whole folder use "Foxy - 3 Batch barcodes": it runs the owner's recorded action (set "Foxy ColorCut", action "Add barcode" = Insert Menu Item File > Add PageMARKs and BarCode) on the CUT layer of each file; the plug-in auto-fills a new unused job number (FB550 guide 7.1, range 0–64,000), the script saves <name>.ai + <name> - PRINT.pdf in "ColorCut ready" and logs job numbers to a CSV. One job number per design, reused for repeat orders.
- Always include a `README - how to print and cut.txt` with the steps (layer the cut lines, add PageMARKs & BarCode, hide the cut layer, print, scan barcode, map Red = Cut / Blue = Crease, test-cut the first sheet).

## 3b. Face masks (cut line from just an image)
- `python3 foxyprinting-rebrand/tools/artwork/mask_cutline.py face.jpg [more.jpg ...] --out DIR` (needs `pip install numpy "opencv-python-headless<5" reportlab`).
- Fits the face image inside 210 x 297 mm (A4, never stretched), centred on **SRA4 (225 x 320 mm)**; traces the face and draws a **magenta 0.1 mm cut line 2 mm inside** the edge, plus almond **eye holes** (26 x 11 mm, `--eye-w/--eye-h`) found by face/eye detection and centred on the iris.
- Writes `<image name>.pdf`, `.svg` (layers `Artwork` / `CUT`) and `<name> - check.png`. **Look at every check.png** – eye detection falls back to typical positions if it can't see the eyes (sunglasses, side-on faces).
- Magenta (CMYK 0,100,0,0) is the owner's mask cut colour (5 Oct 2026); map Magenta = Cut in ColorCut Pro. "Foxy - 1 Prepare cut file" treats magenta as cut.

## 4. Check it
- Render every page to PNG (`pdftoppm -r 40 -png`) and **look at it** (Read the PNG). Fix overlaps, clipping, text outside the safe area, missing bleed.
- For fillable PDFs, also render a copy with example values filled in.

## 5. Save to Dropbox
- `create_folder` → `/AI DESIGNS 2026/<Product title> - <SKU>`.
- The Dropbox connector only takes **text** (`create_file`). SVG, TXT and **pure-ASCII PDFs** work:
  reportlab `rl_config.useA85 = 1`, `pageCompression=0`, then replace the 4 high bytes in ReportLab's header comment (first ~64 bytes) with `~` and assert every byte is < 128. Keep these PDFs small (vector only, < ~60 KB); big raster images make them impractical.
- After saving, **verify**: `download_link` → `curl` + `md5sum` in the Higgsfield sandbox → must equal the local file's md5.
- Files with large images or binary formats: upload to Shopify Files (`stagedUploadsCreate` → curl → `fileCreate`, or Higgsfield `media_upload` → `fileCreate`) and save a `<name> - DOWNLOAD LINK.txt` in the product's Dropbox folder instead.
- Also send the files to the owner in chat (`SendUserFile`) and commit the generator script to the repo.

## 6. Tell the owner
Folder path, file list, the line colours used, what they must do in Illustrator (PageMARKs & BarCode), and anything that needs a test cut.
