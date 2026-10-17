Personalised Bobble Hat Black & White - FOXY-DTF-PBH-03
Print-ready, editable cuff badge template, made 6 Oct 2026.
Colourway: Black/White. The template is the same for all 8 bobble hat colours (FOXY-DTF-PBH-01 to -08).

PRODUCT FACTS (plan/product-facts.md, "Personalised bobble hats (Ralawise blank)")
- Blank: Beechfield B472 Stadium Beanie, one size (adult), 100% soft-touch acrylic, double-layer knit,
  striped turn-up cuff, contrasting pom pom, TearAway label. Never name the blank maker to customers.
- Personalisation: the customer's own badge or logo printed in full colour on the FRONT OF THE CUFF,
  plus an optional club/business name and an optional line of text under the design.
  Customer fields: "Badge or logo upload", "Club or business name (optional)",
  "Text to print under the design (optional)", "Message for us".
- Only print badges/logos the customer has the right to use (own club, school or business).

SIZE  (ASK - no cuff size in plan/artwork-specs.md yet)
- Print area (trim): 60 x 50 mm (landscape) - a sensible cuff badge size, NOT confirmed by the owner.
- Artboard with 3 mm bleed: 66 x 56 mm. Safe area: 3 mm inside the trim (54 x 44 mm).
- ASK: cuff depth and width of the B472 when turned up, and the badge size the owner wants.
  Change TRIM_W / TRIM_H in the generator and re-run if it differs.

CUFF PLACEMENT
- Centre the badge on the front of the turned-up cuff, left to right over the front centre of the hat
  (opposite the back seam), and centred top to bottom within the cuff depth.
- ASK: exact distance from the cuff fold / lower edge, and whether it sits over the stripes as on the
  product photos.

THIS TEMPLATE (layers)
- Artwork: white badge backing (runs into the 3 mm bleed), navy frame inside the safe area, and the dashed
  "YOUR BADGE OR LOGO HERE" placeholder box. Replace the placeholder with the customer's badge/logo
  (vector, or 300 dpi or more at print size). Delete the backing and frame if the order is logo-only.
- Text: live, editable text - "YOUR CLUB NAME" (Bebas Neue) and "Optional line - Est. 1985"
  (Barlow Condensed SemiBold). Type the customer's club/business name and line; delete either if blank.
  Keep all text and logos inside the magenta safe line.
- CUT: red trim path, 0.25 pt stroke, RGB 255,0,0, no fill, exactly on the trim line (60 x 50 mm).
  Use it to trim the transfer film; it never prints.
- Guides (hidden, non-printing): green dashed = 3 mm bleed edge, magenta dashed = 3 mm safe area.

COLOURS
- All colours are CMYK-safe: navy C100 M80 Y20 K30, white backing C0 M0 Y0 K0 (prints as white ink),
  placeholder K45. Change navy to the club colours if wanted; keep the total ink well under 300%.
- Any placed image must be 300 dpi at final size.

DTF PRINT AND PRESS
- Supply the artwork unmirrored (this file). The DTF RIP mirrors / adds the white underbase as set up on
  your printer. ASK: does your RIP need a pre-mirrored file? (none is included because the facts do not
  say so).
- Press settings (temperature, time, pressure, hot or cold peel) for the acrylic knit cuff: ASK - not in
  the product facts. Exact transfer method on knit is also ASK in product-facts.md. Test-press one hat first.

FILES
- FOXY-DTF-PBH-03 - cuff badge 60x50mm.svg : editable artwork (opens in Illustrator / Inkscape). Layers Artwork, Text, CUT, Guides.
- FOXY-DTF-PBH-03 - cuff badge 60x50mm.pdf : the same with real PDF layers Artwork / Text / CUT / Guides (Guides off and never prints),
               TrimBox 60 x 50 mm and BleedBox 66 x 56 mm.
- Fonts/     : FONTS - DOWNLOAD LINK.txt (Google Fonts URLs) and OFL.txt (licence).
- The PNG preview (300 dpi, guides on) is kept in the website repo, because Dropbox here only takes
  text files: foxyprinting-rebrand/exports/hat-artwork/Personalised Bobble Hat Black & White - FOXY-DTF-PBH-03/

Regenerate: python3 tools/artwork/hat_badge_template.py --out <folder>
