---
name: football-shirt-mug
description: Design personalised football shirt mugs for Foxy Printing - a proper drawn kit (collar, cuffs, side panels, stripes/hoops/sash/halves/quarters, fabric shading) with the customer's NAME and NUMBER on the back as editable live text. Use whenever a mug needs a football shirt, kit, team colours, name and number, or "my team" design.
---

# Football shirt mug

Replaces the old flat football-shirt mugs. Uses the `shirt` element of mugkit
(`../mug-print-artwork/scripts/mugkit.py`, run it as that skill describes). Start from
`examples/red-white-stripes.json` and change colours, pattern, text.

## Shirt element
```json
{"type": "shirt", "panel": "left", "view": "back",          // back = name + number, front = crest/chest text
 "pattern": "stripes", "colors": ["#d71920", "#ffffff"],      // c0 = main, c1 = second colour
 "sleeves": "#d71920", "trim": "#111111", "collar": "#111111", "cuffs": "#ffffff",
 "neck": "v",                                                 // front only: v | crew | polo
 "font": "Oswald:700", "text_color": "#111111", "text_outline": {"color": "#ffffff", "width": 16},
 "name": {"field": "Name"}, "number": {"field": "Number"},
 "w_mm": 62, "dx_mm": 0, "y_mm": 4}
```
- Patterns: `plain stripes pinstripes hoops halves quarters sash chevron gradient`.
- `side_panels: false` removes the trim stripes down the sides.
- Front view extras: `"crest": {"text": "DFC", "color": "#fff", "outline": "#111"}` (a plain shield,
  never a real badge), `"chest_text": {"text": "DAD", "field": "Chest"}`, small `number`.
- Name auto-shrinks to fit across the back (O'CONNOR-SMITH works); number fits to the shirt.
- Kit fonts that work: `Oswald:700` (default), `Teko:600`, `Bebas Neue`, `Saira Condensed:800`,
  `Anton`. Keep the number in the same font as the name.

## Layouts that sell
1. **Back + slogan** (default example): back of shirt with NAME/NUMBER on the left panel; small front
   shirt + "CLUB LEGEND / EST. FOR LIFE" on the right.
2. **Back + front**: back (name/number) left, front (crest initials + chest text) right.
3. **Two shirts**: dad and kid (two fields each: Name, Number, Name2, Number2) for Father's Day.
4. **Retro**: `pattern: plain` + `neck: polo`, collar in contrast colour, `Saira Condensed`.
Offer 3 colourways per brief (for example red/white stripes, blue/white hoops, black/white halves)
so Shaun can pick before the full product run.

## Rules
- NO club crests, sponsor logos, kit-maker logos or real club names in the art, titles or tags unless
  Shaun confirms that licence. Describe colours instead ("Red & White Stripes Football Shirt Mug").
  Fan colours are fine; badges and trademarks are not.
- Personalised fields are `Name` and `Number` (and any extra like `Line1`). Number: 1-2 digits.
- Product defaults: Shopify product type `Mugs`, vendor `Foxy Printing`, tags include
  `personalised-mugs`, `football-mugs`, `football shirt mug`, `11oz mug`, `foxy-new-2026`,
  `machine-sublimation`; variant option `Colourway` when several kits ship as one product. Customers
  enter name and number in the line-item personalisation box (state that in the description).
- Variant SKUs: `FOXY-SUB-PFSM-<KIT CODE>-01`, for example `...-RWS-01` = red/white stripes, `BWH` = blue/white hoops.

## Order production
`python3 mugkit.py build kit.json --out "ORDER <no>" --set Name=SMITH --set Number=10`, check the
PROOF, then print the PDF (or the 300dpi PNG) at 100%.
