Custom Kiss-Cut Sticker Sheets - FOXY-CUT-KCSS-01
Production sheet template for kiss-cut sticker sheets, made 6 Oct 2026.

WHAT IS KNOWN (Shopify listing)
- Sold as 5 or 20 sheets; the customer uploads their own sheet artwork and can mix shapes, sizes and designs.
- Printed and kiss-cut in-house (SKU prefix FOXY-CUT = flatbed cutter, Intec ColorCut). No proofs.
- ASK (no fact sheet yet): the finished sheet size the customer receives (A4, A5, A6?), the sticker material,
  and whether the sheet outline is cut through on the ColorCut. Until then this is a cutter-sheet layout only.

THIS TEMPLATE
- SRA4 sheet, 225 x 320 mm (the ColorCut sheet size in the foxy-production-artwork skill).
- 12 mm clear on the left and 10 mm on the other edges for the ColorCut PageMARKs and barcode (blue dashed guide).
- EXAMPLE layout: 15 stickers of 51 mm (alternating circles and rounded squares), each with 3 mm bleed and a
  3 mm safe area. Replace them with the customer's designs; the sizes are examples, not a product spec.
- Each sticker's kiss-cut is a red path on the CUT layer, on the trim line.

HOW TO CUT (Intec ColorCut Pro)
1. Open in Illustrator, place the customer's artwork into the circles/squares (or redraw cut paths to their shapes).
2. Run "Foxy - 1 Prepare cut file", then the ColorCut plug-in "ADD PageMARKs & BarCode".
3. Hide the CUT layer and print ("Foxy - 2 Save print PDF").
4. In ColorCut Pro map Red = Cut and set the blade depth for a KISS cut (through the vinyl, not the backing),
   or recolour the paths Yellow = Score (half-depth) if you prefer the house convention. Test-cut the first sheet.

FILES
- FOXY-CUT-KCSS-01 - SRA4 kiss-cut sheet template.svg  : editable artwork. Layers: Artwork, Text, CUT, Guides (Guides hidden - switch it on to see the lines).
- FOXY-CUT-KCSS-01 - SRA4 kiss-cut sheet template.pdf  : the same, with real PDF layers Artwork / Text / CUT / Guides (Guides is off and never prints).
- Fonts/      : FONTS - DOWNLOAD LINK.txt and OFL.txt (licence).
- A PNG preview is kept in the website repo: foxyprinting-rebrand/exports/sticker-artwork/FOXY-CUT-KCSS-01/

LINE COLOURS
- CUT layer = red = cut. 0.25 pt stroke, RGB 255,0,0, no fill, sitting exactly on the trim line.
- Guides (not printed): green dashed = 3 mm bleed edge, magenta dashed = 3 mm safe area.

Regenerate: python3 tools/artwork/sticker_templates.py --out <folder> --only FOXY-CUT-KCSS-01
