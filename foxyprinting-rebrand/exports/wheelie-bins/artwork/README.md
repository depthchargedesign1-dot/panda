# Wheelie bin stickers: editable A5 production artwork

Job date: 6 Oct 2026. This covers the 36 "Personalised Wheelie Bin Sticker – Design N" products.

## Where the files are (Dropbox)

Each design has its own folder:

`/AI DESIGNS 2026/Personalised Wheelie Bin Sticker – Design N - FOXY-CUT-PWBSDN-01/`

Each folder contains:
- the owner's original design file(s) (.pdf / .ai), **copied** from the original location (never moved);
- `README - how to print and cut.txt`;
- `Fonts/FONTS - DOWNLOAD LINK.txt` and `Fonts/OFL.txt`;
- for the redrawn designs: `Wheelie Bin Sticker Design N - FOXY-CUT-PWBSDN-01 - A5 print file.svg` and `.pdf`.

Each print file is laid out as follows:
- **Page:** 216 × 154 mm. That is A5 trim (210 × 148 mm) plus 3 mm bleed, with a 3 mm safe area.
- **Personalisation:** the house number and street are **live text**. The sample is "74 Make Believe Close".
- **Cut line:** red RGB 255,0,0 at 0.25 mm, on its own layer/group named **CUT**. Corners are rounded (3 mm radius); designs 6, 7, 8 and 31–36 have square corners, like the originals.
- **PDF format:** pure ASCII, with two layers (OCGs) named "Artwork" and "CUT". The fonts are subset and embedded.

## Status per design

| Designs | Status |
|---|---|
| 1–5, 14–24, 26–30 (21 designs) | Redrawn fully in vector with live text. SVG + PDF are saved in Dropbox, and their content hashes are verified against the generator output. For 5 and 18 the house icon was redrawn as vector (the original was a 512 px bitmap). |
| 6–13, 25, 31–36 (15 ornate designs) | Built as fully vector files: the original ornaments are extracted as vector paths with their clip groups, and the text is live. **The print files are not in Dropbox yet.** Uploading them through the Higgsfield sandbox was blocked by a permission check. Each of these folders has `PRINT FILE - HOW TO BUILD (ornate designs).txt` instead. |

Designs 5, 6, 7 and 11 show only a number in the original. A street line has been added because the listings say a street can be added. It can be deleted if it isn't wanted.

## Fonts (Google Fonts / SIL OFL look-alikes)

The fonts used are:
- PT Sans
- Marcellus
- Arvo
- Archivo Black
- Gilda Display
- Courgette
- Old Standard TT
- Delius
- Ribeye
- Sorts Mill Goudy
- Patrick Hand
- Alegreya SC Bold
- Bowlby One
- Anton
- Crimson Text (Regular / Italic)
- Short Stack
- Lobster
- Federo
- Kalam Bold
- Della Respira

All of them are in one zip on Shopify Files:
https://cdn.shopify.com/s/files/1/1774/9115/files/Wheelie-Bin-Sticker-fonts-OFL.zip?v=1791280736

`ORIGINAL_FONT` in the generator lists which of the owner's fonts each one replaces.

## Rebuilding / building the ornate designs

You need Python 3 with `reportlab pikepdf pymupdf fonttools`, plus `cairosvg` for the check PNGs.

```
python3 foxyprinting-rebrand/tools/artwork/wheelie_bin_stickers.py \
  --fonts <folder with the TTFs from the zip above> \
  --src <folder with the original Design N PDFs> \
  --out <output folder> --designs 6-13,25,31-36 [--texts] [--no-png]
```

The `--src` option is needed for the ornate designs, because their ornaments are read from the owner's original PDF. Check each `- check.png` before printing.

## Notes

- Design 2's "original" PDF and some of the extra PDFs for Design 31 are customer proofs ("39 Carnaughton Place" etc.). They were copied as found.
- The `Wheelie-Bin-Sticker-artwork-generator.zip` on Shopify Files is an older copy of the generator, from before the clip-group fix. Use the copy in this repo instead.
