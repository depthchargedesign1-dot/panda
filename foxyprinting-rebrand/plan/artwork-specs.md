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
| 11oz white mug wrap | **200 × 85 mm** trim + **3 mm bleed** each edge = **206 × 91 mm** page | Safe area 3 mm inside trim. 300 dpi for any raster. Standard 11oz sublimation template, used for the number plate mugs (Oct 2026). **ASK** the owner to confirm against their mug blanks/press. |

- Mirroring: supply unmirrored masters; a "- MIRRORED.pdf" is included for drivers/RIPs that don't mirror sublimation transfers automatically.
- Generator example: `tools/artwork/number_plate_mugs.py`.
