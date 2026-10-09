# Towel images: DCD TEAMWEAR logo removal (9 Oct 2026)

Owner's request: "https://foxyprinting.co.uk/collections/football-bath-towels can you remove the DCDTEAMWEAR LOGO from all images and reupload".

Collection `gid://shopify/Collection/409794314491` (handle `football-bath-towels`): **205 products, 327 images**, all checked (every image, not only the featured one). Full list: `products.json`.

## What was found
| Range | Products | Images | Logo? |
|---|---|---|---|
| Retro football/cricket "Lightweight Beach Gym Towel" (beach scene) | 177 | 177 (1 each) | **Yes, all 177**: top-right on the sand, same spot in every image (2000x1333: x 1362–1937, y 60–335; 3000x2000: x 2043–2906, y 90–502) |
| Personalised "Dream Team" beach towels | 28 | 150 | **No.** Template match scores 0.26–0.37 (logo images score 0.88–0.90) and checked by eye on a contact sheet of all 150 |

No image was in doubt: the scores split cleanly (≥ 0.88 vs ≤ 0.37), so there is nothing left to check by hand.

## How it was removed (all local, Python/OpenCV; no third-party or AI service)
Scripts in `foxyprinting-rebrand/tools/towel_logo/`:
- `detect.py`: multi-scale edge template match against a crop of the logo, on every image.
- `logomask.py`: exact logo shape (black outline + white "DCD" + blue "TEAMWEAR"), grown by a few px.
- `remove.py`: fills only the logo shape (plus a ~10 px cross-fade band) with sand: lighting interpolated from the surrounding sand + real sand grain quilted from clean sand next to the logo (each patch chosen to match the sand it joins). The towel, its print and everything else are untouched.
- `batch.py`: runs all 177, checks **0 pixels changed outside the logo area** and that the logo can no longer be found (score after ≤ 0.35), saves JPEG q95 4:4:4, same pixel size, ICC profile kept.
- `contact_sheet.py`: before/after sheets (`contact-sheet-*.jpg` here, 15 samples checked by eye at full size and 1:1 crops; no smudges or seams).
- `gen.py` + `put_staged.py`: build the upload mutations and PUT files to Shopify staged uploads.

## Upload method (per product)
`stagedUploadsCreate` (PUT) → upload → `productCreateMedia` (alt text: the old alts were all empty, so each gets a plain-words alt from the title, e.g. "Bristol Rovers 1995 retro football lightweight beach gym towel laid out on the sand") → `productReorderMedia` to the old image's position → old image **detached** with `fileUpdate referencesToRemove` (the original file stays in Shopify Files; nothing deleted).

## Status
See `log.csv` (product handle, old media id, new media id, status).
- **Pilot done and checked (3):** Bristol Rovers 1995 (3000 px), Bournemouth 1992 Away (3000 px, slightly different scene file), Cardiff 1992 (2000 px, slightly different scene file). Re-read: one image each, READY, featured, right size; the live CDN images viewed: no logo, sand looks natural.
- **Remaining 174:** cleaned images are ready (all passed the checks), but the bulk upload was **stopped by this session's permission guard** ("modify shared resources") before any further store changes. Needs the owner's go-ahead (or a permission rule) to continue; then it's ~9 batches of 20 with the same steps.

## Sales channels (report only, nothing changed)
CLAUDE.md says club badges/crests and brand logos stay **website only**. These towels show club names, crest-style designs and shirt-sponsor brand marks (e.g. Newcastle Brown Ale on the Newcastle shirts, JVC, Guinness, Holsten, Philips, asics, Bass, ICI…).
- **176 of the 177 retro towels are published to Google & YouTube, Facebook & Instagram AND TikTok.** Only `middlesbrough-1973-retro-football-lightweight-beach-gym-towel` is off all three.
- The 28 personalised Dream Team towels are on none of the three (website only).
- Per-product list: `channels.csv`. Shopify's MCP blocks unpublishing from here (STATUS known block), so the owner would need to unpublish them in Shopify admin (bulk edit → Sales channels) if he wants them website-only.

## Re-running
The 177 cleaned JPEGs are not committed (≈200 MB); they were made in the session scratchpad. They are deterministic: download the originals (`products.json` media ids/files from cdn.shopify.com), then run `detect.py` → `batch.py` (seed fixed) to get identical files. `clean-check.csv` holds the per-image checks (all 177: 0 px changed outside the logo area, logo score after ≤ 0.18).
