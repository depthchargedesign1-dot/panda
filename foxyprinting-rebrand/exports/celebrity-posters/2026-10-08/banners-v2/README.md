# Poster collection header banners v2 (8 Oct 2026, ~22:00 UTC)

Owner: "on the poster print header mockups the images youve used does not fill the frames, make sure you use proper frames that we sell and fill the image".

- Built with `tools/poster_banners_v2.py`. It uses the real frames from our own framed product photos (Black: Robbie_Williams-Black.jpg, Silver: COLUMBO_PETER-Silver.jpg, White: Cristiano_Ronaldo-White.jpg, Gold: THE_GREATEST_SHOWMAN___35102.jpg; the store's 1500x1500 brick-wall template). Each frame is cut out as a ring and stretched so its opening is exactly the print, so every print fills its frame edge to edge. Nothing is drawn.
- Framed photos from other templates (white wall, portrait frame) are skipped because their prints can't be cut out cleanly. New picks for Basketball/Hockey and Icons (print-only images) are in `tools/poster_banners.py` PICKS.
- 18 new files `foxy-header-<handle>-v2.jpg` uploaded and set as each collection's `foxy.header_image`; ids in `manifest-v2.json` (v1 ids kept there for rollback; v1 files are still in Shopify Files, not deleted).
- Theme (working copy "plate squeeze" 189519069565, not yet published): collections with their own banner get a taller header on desktop (`collection-hero--tall`, min-height clamp(260px, 26vw, 470px)), so more of the banner shows.
