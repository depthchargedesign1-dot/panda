---
name: trending-celebrity-masks
description: Find who is trending right now (events, TV line-ups, charts, sport, influencers) that Foxy Printing has no face mask of, then build each one end to end from the owner's mask artwork - print + cut file, website image, live listing in the right collections, Dropbox artwork folder - plus pairing packs. Use when the owner asks for "trending masks", masks for an event (Strictly, I'm a Celeb, Traitors, Love Island, Euros, darts, Eurovision...), or new celebrity masks.
---

# Trending celebrity face masks (Foxy Printing)

First run: 6 Oct 2026 (top-100 list, 17 masks live, 3 new collections, packs). Records:
`foxyprinting-rebrand/exports/face-masks/2026-10-06-trending-100/` (trending-100.csv, excluded.csv,
collections.md, built-masks.csv, FACE-PHOTOS-NEEDED.txt). Read CLAUDE.md and STATUS.md first.

## Hard rules (owner + safety)
- **Faces come only from the owner's own artwork** (Dropbox mask folders) or photos the owner drops in
  `/AI DESIGNS 2026/00 TRENDING MASKS - FACE PHOTOS NEEDED/`. Never pull photos off the web and never
  AI-generate a real person's face (mask art or "people wearing the mask" lifestyle shots).
- Exclude: under-18s, people convicted of sexual/violent crimes or otherwise disgraced, recently deceased
  (poor taste), racial caricatures, private individuals known by first name only. Flag borderline cases
  (e.g. allegations without conviction) for the owner.
- Real people only; flat printed card masks, so skip Halloween/costume-character trends unless asked.
- Channels (owner, 6 Oct): celebrity faces go on all 5 channels; only club badges / infringing logos stay
  website + Shop only. Owner-requested masks go ACTIVE straight away.
- Dropbox: create only. Never delete, move or overwrite.

## 1. Research (one agent, read-only)
- WebSearch (extended for recency), UK-weighted: charts, TV line-ups (Strictly, I'm a Celeb, Traitors,
  Love Island, Big Brother, soaps), film releases, sport (football, darts, boxing, cricket, F1, rugby,
  tennis, NFL in UK), influencers/streamers, people in the news. ~180-250 candidates, each with a
  "why now" line and source URL.
- Store check: products(query:"title:*<surname>* AND title:*mask*") per candidate, plus alternative
  spellings/accents. A combined mask (e.g. "JUNKOOK JIMIN") doesn't count as a single.
- Dropbox check: `exports/face-masks/dropbox-masks-master-list.csv` + Dropbox search (title_only) inside
  `/2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES` and `/Anna and RAFIA Work 2/.../NEW FACE MASK`.
  Poster artwork is not mask artwork.
- Output CSV: rank,name,known_for,category,why_trending,source_url,dropbox_artwork_path,suggested_collections,notes.
- Collections: ~95 mask collections, mostly smart (tag rules). Key ones in collections.md; plus
  `youtuber-influencer-face-masks` (tag youtuber-masks), `k-pop-face-masks` (kpop-masks),
  `the-traitors-face-masks` (traitors-masks), made 6 Oct 2026. Make a new tag-based collection for a new
  event if none fits (ask the owner first).

## 2. Build each mask that has artwork (`tools/trending_masks_build.py` is the template)
1. **Artwork:** Dropbox `download_link` → local `curl` (`*.dl.dropboxusercontent.com` and `cdn.shopify.com`
   are allowed in the environment's network settings). PDFs → `pdftoppm -r 300`. Crop sheets with two faces /
   registration marks to one face. Look at every face.
2. **Print + cut:** `tools/artwork/mask_cutline.py face.jpg --out DIR` (A4 face on SRA4, magenta 0.1 mm cut
   2 mm inside, eye holes). Look at every `- check.png`; set eye centres by hand when detection misses
   (glasses, winks, forehead hits). Pale hair on white → `tools/artwork/mask_cutline_soft.py`.
   Flag low-res art (< ~1200 px tall prints soft).
3. **Website image:** face mask on plain white, ≤ 2048 px tall, no text.
4. **Upload:** `stagedUploadsCreate` (httpMethod PUT) → local `curl -X PUT -H "Content-Type: image/jpeg"
   --upload-file` (only that header) → `productCreateMedia` / `fileCreate`. Never send files or staged
   URLs to Higgsfield or any third party.
5. **Product** (productCreate, ACTIVE; never productSet):
   - Title `<Name> Face Mask – Fancy Dress Cardboard Costume Mask` (bands: `V Face Mask (Kim Taehyung, BTS) – …`;
     TV characters: `Gwen Face Mask (Melanie Walters) – …`).
   - Type `Celebrity Facemask`, vendor Foxy Printing, category Masks (`gid://shopify/TaxonomyCategory/aa-3-4`).
   - Options Style (Ready Cut / DIY) × Fitting (Elastic / Stick): £2.99 / £3.49 / £1.50 / £2.00;
     SKUs `FaceMask-<Name>-RC-E/-RC-S/-DIY-E/-DIY-S`. Never say elastic/stick is pre-attached.
   - Copy from `tools/mask_copy.py` + a hand-written intro on why they're trending; Face masks fact sheet only;
     celebrity disclaimer last (band line for bands; TV-character template for characters).
   - SEO title ≤ 60, meta 140–155; Google `mm-google-shopping` fields (custom_product, condition new,
     category, gender unisex, age_group adult, color Multicolor, mpn = RC-E SKU); `shopify.*` category
     metafields as in the script.
   - Images: main, then the standard EXTRA_MEDIA + LIFESTYLE ids in the script (fileUpdate referencesToAdd).
   - Tags: BASE_TAGS + COLL_TAGS for the suggested collections + event tags (kpop-masks, traitors-masks,
     youtuber-masks, Strictly Come Dancing…).
   - Publish to Online Store, Shop, Google & YouTube, FB & IG, TikTok. Re-read every product.
6. **Dropbox:** `/AI DESIGNS 2026/<Product title> - <RC-E SKU>/` with the cut SVG, `DOWNLOAD LINK.txt`
   (print PDF in Shopify Files) and `README - how to print and cut.txt` (foxy-production-artwork skill).
7. Record in `built-masks.csv`; commit and push.

## 3. People without artwork
Write the names (trending order) into `README - names needed.txt` in the Dropbox face-photos folder and
tell the owner. When photos arrive, run step 2.

## 4. Pairings (always suggest; build when the owner says yes)
Band packs (all members), siblings/duos, couples (e.g. Travis Kelce + Taylor Swift), fight packs (both
boxers, before fight night), show cast packs. Main image: masks side by side, clean background, NO text.
Copy structure and prices from existing packs (Spice Girls / One Direction 5-packs, couple pairs).
Records: `exports/face-masks/2026-10-06-packs/`.

## 5. Report to the owner
Live URLs, what was skipped and why, doubtful cut checks, low-res art, the names still needing photos,
pairing ideas, and any new-collection suggestions.
