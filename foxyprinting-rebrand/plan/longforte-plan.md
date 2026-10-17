# Longforte blanks: retail plan for Foxy Printing

Full data: `longforte-catalogue.json` in this folder (112 supplier facts, 14 categories, 70 products).

## How this was researched
- www.longforte.com and shop.app are blocked from this environment, and WebFetch returned `EGRESS_BLOCKED`. All facts come from web-search titles and snippets limited to longforte.com. Nothing was copied from memory.
- Prices in the snippets show a `$` sign. Longforte is a UK site, so they are probably £, but it isn't clear whether VAT is included. **Check every price in the trade account before costing.**
- RRPs in the JSON are **estimates**. They're about 2.5–4× wholesale where a price was visible; otherwise they're set against similar personalised gifts.

## Proposed categories (14 categories, 70 products)

| Handle | Category | Products | Example blanks (as found) |
|---|---|---|---|
| lf-photo-slates | Personalised Photo Slates | 4 | 10x15cm, 15x15 / 30x30cm square, 15cm round with stands, 15x15cm heart |
| lf-metal-photo-panels | Personalised Metal Photo Panels | 4 | Ultra HD gloss white 1.15mm aluminium in 4x6, 5x7, 6x7.8, 8x10 and 12x5in; gloss silver 11.5x11.5in; self-adhesive easels |
| lf-clocks-glass-frames | Personalised Clocks & Glass Photo Frames | 6 | MDF clock 30cm; glass clocks 20/30cm; aluminium clocks 19.8cm round / 22.8cm square; slate clock 25x40cm; glass and frosted frames |
| lf-plaques-tiles | Personalised Photo Plaques & Ceramic Tiles | 4 | MDF plaques 10x15 to 30x40cm; 12in round bevelled plaque; ceramic tiles 4.25in to 8x12in; 4in heart tile |
| lf-coasters-placemats | Personalised Coasters & Placemats | 5 | Slate coaster 10cm; glass coaster 10cm; MDF coasters 9.5cm; MDF placemats 20x26 / 20x28cm with cork; kids hardboard placemat 19x23cm |
| lf-tumblers-bottles | Personalised Travel Mugs, Tumblers & Bottles | 6 | 40oz tumbler; 16oz with straw; 14oz travel mug; 12oz ceramic travel mug; 720ml one-touch; 500/600ml aluminium bottles |
| lf-speciality-mugs-glassware | Personalised Enamel, Latte & Speciality Mugs | 6 | 12oz enamel (5 colours); 12oz latte with coloured inside and handle; colour-changing; "I Love You" inner heart; 550ml glass can; frosted beer steins |
| lf-kids-school | Personalised Kids & Back to School | 6 | 6oz polymer mug (6 colours); 13oz sippy cup; lunchbox; lunch bag; pencil cases; baby bibs |
| lf-cushions-textiles | Personalised Cushions & Home Textiles | 6 | 40/45cm cushion covers; 9-panel cushion; blankets 75x100 / 110x150cm; tea towels; aprons; linen tote |
| lf-keyrings-magnets | Personalised Keyrings & Fridge Magnets | 5 | Metal keyrings with box (5 shapes); MDF double-sided keyrings; bottle opener keyring; glass, MDF and rubber magnets; musical magnet |
| lf-christmas-ornaments | Personalised Christmas Baubles & Ornaments | 5 | Mirror baubles with insert; aluminium ornaments (8 shapes); MDF ornaments with ribbon; stocking 20.5x45cm |
| lf-plush-toys | Personalised Teddy Bears & Plush Toys | 4 | Teddy with t-shirt (cream / dark brown, about 8in); bunny (4 colours); bear and bunny keyrings |
| lf-jigsaws | Personalised Photo Jigsaws | 5 | A4 80pcs; A3 300pcs pearl; 30pcs kids; magnetic heart 75pcs; round MDF 24pcs in case |
| lf-pet-gifts | Personalised Pet Gifts | 4 | Bandanas S/M/L; ceramic dog bowl; dog tags; pet photo keyring |

Already sold heavily, so left out: standard 11oz white mugs, bath towels, baby grows, santa sacks, mouse mats. Also left out:
- phone cases, because the models change too fast;
- snowglobe bottles, because they're UV DTF or vinyl, not sublimation;
- lanyards, because they suit business orders more than gifts.

20 more blanks that were found are in `facts` but held back to keep the first launch to about 70 products.

## Gaps: specs not findable from search results (ASK the owner or Longforte)
- Price currency and VAT basis (snippets show `$`).
- Size or capacity: ceramic dog bowl, glass door sign, ceramic ornaments, musical magnet (size and battery), bunny print area, plush shapes such as monkey, panda and elephant.
- Piece counts for the A5 felt and pearl jigsaws.
- Whether batteries come with the clocks, and whether tiles come with an easel.
- Cushion inners (only covers were found).
- Whether a 20oz white sublimation skinny tumbler exists (only a black engravable one was confirmed).
- Capacities of the enamel and latte mugs are as listed (12oz). Dishwasher-safe claims were only seen for the ORCA, 6oz ceramic, latte and polymer mugs.

## Before listing (CLAUDE.md)
- Create every product as a **DRAFT**.
- Most families need a new sheet in `product-facts.md`. Anything above marked ASK has to be asked before copy is written.
- Never use "Stanley" (mentioned in Longforte's 40oz tumbler copy) or "Printa Plush" (Longforte's brand) in customer-facing titles.

## Main sources
- Slates: https://www.longforte.com/products/small-square-photo-slate
- Metal sheets: https://www.longforte.com/products/pack-of-10-x-ultra-hd-115mm-thick-sublimation-aluminium-sheets-8-x-10-203cm-x-254cm
- Easels: https://www.longforte.com/products/pack-of-10-x-small-self-adhesive-black-easel-for-sublimation-metal-sheets-38mm-x-89mm
- Clocks: https://www.longforte.com/products/mdf-sublimation-clock-30cm
- Glass frames: https://www.longforte.com/collections/glass-frames
- MDF plaques: https://www.longforte.com/collections/photo-panels
- Tiles: https://www.longforte.com/products/lrg-ceramic-tile-8x8
- Coasters and placemats: https://www.longforte.com/collections/coasters-and-place-mats
- Tumblers: https://www.longforte.com/collections/sublimation-tumblers
- Water bottles: https://www.longforte.com/collections/water-bottles
- Enamel mugs: https://www.longforte.com/collections/enamel-mugs
- Latte mugs: https://www.longforte.com/collections/latte-mugs
- Beer steins: https://www.longforte.com/collections/beer-mugs-tankards
- Glass jars: https://www.longforte.com/products/mugs-glass-550ml-glass-jar-with-bamboo-lid-straw-red
- Kids polymer mugs: https://www.longforte.com/products/mug-polymer-6oz-unbreakable-mug-white-2
- Lunch boxes: https://www.longforte.com/collections/lunch-boxes
- Pencil cases: https://www.longforte.com/collections/pencil-cases
- Bibs: https://www.longforte.com/products/pink-baby-bib-sublimation
- Cushions: https://www.longforte.com/products/square-cushion-cover-super-soft-finish-40cm
- Blankets: https://www.longforte.com/collections/blankets
- Aprons: https://www.longforte.com/products/adult-sublimation-apron-with-pocket-white
- Tote bags: https://www.longforte.com/collections/tote-bags
- Keyrings: https://www.longforte.com/products/metal-keyring-round-shape
- Magnets: https://www.longforte.com/products/fridge-magnet-10-x-glass-rectangle-5cm-x-7cm
- Ornaments: https://www.longforte.com/collections/ornaments
- Stocking: https://www.longforte.com/products/sublimation-xmas-stocking-with-red-border
- Plush: https://www.longforte.com/collections/printa-plush
- Jigsaws: https://www.longforte.com/products/jigsaw-puzzles-cardboard-pearl-finish-a3
- Pets: https://www.longforte.com/products/pet-products-adjustable-pet-bandana-medium
- Dog bowl: https://www.longforte.com/products/carton-12-x-bowls-ceramic-dog-bowl

Every product and fact in the JSON has its own `source_url`.
