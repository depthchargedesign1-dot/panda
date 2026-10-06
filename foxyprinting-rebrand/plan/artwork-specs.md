# Foxy Pop theme: artwork sizes

Sizes are for the Foxy Pop theme at its default 1360px page width. Supply them at 2× the on-screen size so they stay sharp on retina screens.

**File format**
- JPG at 80–85% quality, or WebP, under about 500 KB each.
- sRGB colour.
- Use PNG only when you need transparency (category circles, logo).
- Don't put headline text or buttons in the artwork. The theme adds those as live, editable text that search engines can read.

## Homepage

| Slot | Where to set it | Upload size | Shape | Safe zone / notes |
|---|---|---|---|---|
| **Main hero** | Customize → Hero banners → Main banner → Background image | **1680 × 1100 px** | about 3:2 | Text sits on the **left 45%**. Keep that area plain (it matches the tile colour). Put the subject in the right half. Mobile crops a 5:4 area from the right, so keep key details inside the **right 1375 px**. |
| **Side banners** (×2) | Hero banners → Side banner → Background image | **900 × 550 px** | about 1.65:1 | Text covers the **left 70%** on desktop. Put the subject in the **right 30%**, or use a soft, low-detail image. |
| **Category circles** (×12) | Category circles → Category → Image (otherwise the collection's own image is used) | **600 × 600 px** | 1:1, shown as a circle | Keep the product inside the **middle 75%**, because the corners are cut off. Use a plain or transparent background. Shown at about 120–140 px. |
| **Feature tiles** ("New ranges" and "Business printing", 4 each) | Feature tiles → Tile → Image | **800 × 550 px** | 16:11 | Fills the tile top edge to edge. The title shows underneath, not on top. |
| **Mega menu promo** (one per department, optional) | Header & mega menu → department block → Promo image | **600 × 750 px** | 4:5 portrait | Title and link sit over the **bottom 35%** on a dark fade. Keep the subject in the top half. |
| **Logo** | Header → Logo | **440 px wide** (PNG, transparent) | any | Shown up to 120 px tall on desktop and 64 px on mobile. **Needs dark text**, because the header is white. |

## Collection pages

| Slot | Where to set it | Upload size | Shape | Safe zone / notes |
|---|---|---|---|---|
| **Collection header banner** | Collection → Metafields → **Header banner** (`foxy.header_image`) | **2400 × 640 px** | 3.75:1 | Title, breadcrumb and description sit on the **left 45%**. Keep it plain, ideally one solid colour. Mobile shows a 16:9 crop from the right, so keep the key subject inside the **right 1140 px**. If no banner is set, the header falls back to a coloured block. |
| **Collection image** | Collection → Collection image | **1000 × 1000 px** | 1:1 | Used for the category circles, the "all collections" grid (4:3, not cropped) and the small header circle when there's no banner. Use a centred product on a plain background. |

## Products

| Slot | Upload size | Notes |
|---|---|---|
| Product images | **2000 × 2000 px** square | The theme shows the whole image (contain, not crop). Use a white or very light background so cards line up in grids. |

## AI-generated artwork (Higgsfield)
- For the hero, generate at **3:2** (or 16:9 and accept a small crop).
- For collection headers, generate at **21:9** and then crop to 3.75:1, which removes about 20% top and bottom. Alternatively, ask for "very wide panoramic, subject vertically centred" so nothing important is near the top or bottom edge.

## Mugs: 11oz sublimation wrap (print files)

| Item | Size | Notes |
|---|---|---|
| 11oz white mug wrap | **200 × 70 mm** print area (owner, 6 Oct 2026) + **3 mm bleed** each edge = **206 × 76 mm** page | Safe area 3 mm inside trim. 300 dpi for any raster. Full-wrap designs (e.g. the number plate mugs) run the whole 200 mm width around the mug. |

- Mirroring: supply unmirrored masters; a "- MIRRORED.pdf" is included for drivers/RIPs that don't mirror sublimation transfers automatically.
- Generator example: `tools/artwork/number_plate_mugs.py`.

## Bobble hats: cuff badge (FOXY-DTF-PBH-01 to -08)

| Item | Size | Notes |
|---|---|---|
| Beanie cuff badge (full colour, DTF) | **60 × 50 mm** print area (landscape) + **3 mm bleed** each edge = **66 × 56 mm** page. **ASK:** size not confirmed by the owner, and cuff depth/width of the B472 not known. | Safe area 3 mm inside trim. 300 dpi for any raster. Centred on the front of the turned-up cuff (exact position from the fold: **ASK**). CUT layer = red 0.25 pt trim path for trimming the film. Supply unmirrored; whether the DTF RIP needs a pre-mirrored file: **ASK**. Press settings: **ASK**. |

- Generator: `tools/artwork/hat_badge_template.py` (change `TRIM_W` / `TRIM_H` and re-run if the owner gives a size).

## Terrace flags (FOXY-FLAG-<CODE>-01..03, tag "DCD Terrace Flags")

| Size | Trim (finished flag) | Artboard with bleed | Images at full size |
|---|---|---|---|
| 3ft x 2ft | **914 × 610 mm** | 920 × 616 mm | 150 dpi (**ASK**) |
| 5ft x 3ft | **1524 × 914 mm** | 1530 × 920 mm | 150 dpi (**ASK**) |
| 8ft x 5ft | **2438 × 1524 mm** | 2444 × 1530 mm | 100 dpi (**ASK**) |

- **Bleed: 3 mm** on every edge. **ASK:** the hem/bleed allowance for sewn flags with the 25 mm binding (some makers want 10–20 mm per edge for a turned hem). Not given by the owner yet; 3 mm is a placeholder.
- **Safe area: 25 mm** inside the trim, clear of the 25 mm binding and the eyelets. **ASK** (confirm).
- **Eyelets:** templates mark them 12.5 mm in from the edge (middle of the binding), at each corner plus evenly spaced, no more than 500 mm apart (3x2: 8, 5x3: 14, 8x5: 22). **ASK:** real count and spacing.
- **Resolution:** 300 dpi is impractical at 8 ft; large-format default used: 150 dpi at full size (3x2, 5x3), 100 dpi (8x5). **ASK** (confirm with the RIP/printer).
- **Printer / roll width: ASK.** An 8x5 flag needs a roll at least 1530 mm wide (or panels); the 24 in (610 mm) sublimation printer in `large-format-plan.md` can't print even the 3x2 with bleed in one piece. Mirroring, ICC profile and fabric shrinkage: **ASK**.
- Layers: Artwork (placeholder background), Text (live "YOUR NAME / GROUP" + second line, Bebas Neue, OFL), CUT (red RGB 255,0,0, 0.25 pt trim path), Guides (hidden, non-printing: bleed, trim, safe, eyelets). CMYK-safe colours.
- Never add a real club crest, league logo or trophy artwork without a licence.
- Generator: `tools/artwork/terrace_flag_template.py` (change `BLEED`, `SAFE`, `EYELET_*` and re-run once the owner answers).
