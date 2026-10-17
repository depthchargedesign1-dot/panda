# Celebrity Posters department (8 Oct 2026)

Owner's request (8 Oct): "add a new category at the top menu for Celebrity Posters" / "upload all the posters into it and
make a mega menu for it with all the collections of posters".

## What counts as a celebrity poster
- **13,375** products with "Printed Signature" in the title (bulk export of the whole store; 13,348 ACTIVE, 22 ARCHIVED,
  4 DRAFT, 1 UNLISTED). Every one is a person / cast / squad print with a printed signature.
- **+95** person posters without "Printed Signature" in the title (Lionesses, England/Argentina/Spain player posters,
  Liverpool & Leeds 2020 player prints, darts "Signature Style" posters, the 16 "Unofficial ... Wall Art" music/sport
  posters, Ilia Topuria). These got the tag `celebrity-poster`.
- **Total: 13,470** (the parent collection count matches exactly).
- Not included (not a person): club/team "Printed Display Poster" prints, Tiny Men Big Balls club posters, club
  colours posters, stadium posters, retro game posters, word art, pet portraits, travel/film poster sets, GP podium
  posters, LEGO display cases.

## Collections (all smart, sort Best selling, published to Online Store + Shop)
| Collection | Handle | Products | Rules (any condition) |
|---|---|---|---|
| Celebrity Posters (parent) | `celebrity-posters` | 13,470 | title contains "Printed Signature" OR tag `celebrity-poster` |
| Music Star Posters | `music-star-posters` | 1,507 | 2 types + 2 title phrases + tag `cp-music` |
| Film Star Posters | `film-star-posters` | 843 | 2 types + 3 title phrases + tag `cp-film` |
| TV Star Posters | `tv-star-posters` | 624 | 2 types + 5 title phrases + tag `cp-tv` |
| Football Star Posters | `football-star-posters` | 3,976 | 4 types + 6 title phrases + tag `cp-football` |
| NFL & American Football Star Posters | `nfl-american-football-posters` | 2,001 | 2 types + tag `cp-american-football` |
| Boxing Star Posters | `boxing-star-posters` | 326 | 2 types + 2 title phrases + tag `cp-boxing` |
| UFC, MMA & Wrestling Posters | `ufc-mma-wrestling-posters` | 686 | 2 types + 3 title phrases + tag `cp-mma-wrestling` |
| Darts & Snooker Star Posters | `darts-snooker-star-posters` | 301 | 1 type + 1 title phrase + tag `cp-darts` |
| Cricket Star Posters | `cricket-star-posters` | 544 | 3 title phrases + tag `cp-cricket` |
| Rugby Star Posters | `rugby-star-posters` | 493 | 1 type + 3 title phrases + tag `cp-rugby` |
| Golf Star Posters | `golf-star-posters` | 468 | 1 type + 2 title phrases + tag `cp-golf` |
| Tennis Star Posters | `tennis-star-posters` | 148 | 1 type + 1 title phrase + tag `cp-tennis` |
| Horse Racing Star Posters | `horse-racing-star-posters` | 186 | 1 type + 1 title phrase + tag `cp-horse-racing` |
| F1 & Motorsport Star Posters | `f1-motorsport-star-posters` | 240 | 2 types + 4 title phrases + tag `cp-motorsport` |
| Athletics & Olympic Star Posters | `athletics-olympic-star-posters` | 135 | 1 type + 3 title phrases + tag `cp-athletics` |
| Basketball, Baseball & Ice Hockey Posters | `basketball-baseball-hockey-posters` | 715 | 2 types + 1 title phrase + tag `cp-us-sports` |
| Authors, Scientists & Icons Posters | `icons-legends-posters` | 278 | 5 types + tag `cp-icons` |

Full rule sets, SEO titles/meta and descriptions: `collections.json`. Each description is UK English, says the prints
are printed reproductions (signature printed, not hand-signed), mentions Premium Display frames (no measurements: frame
depth/material is still ASK), and ends with the "Please note" disclaimer. No "official/licensed/authentic".

Rules were chosen so that, within the 13,375 posters, every type/title rule is 100% one group (checked locally, see
`rules.py`). Mixed product types ("Football Posters", "signed posters", "Signed Athletics Prints", "Posters, Prints, &
Visual Artwork", "Signed Team Player Prints") are NOT used as rules; those products got a `cp-<group>` tag instead.
**998 products tagged** with `tagsAdd` (903 `cp-<group>` only + 95 `celebrity-poster` + `cp-<group>`): `tags-added.csv`.
Groups were decided by `classify.py` (product type, then tags, then title words, then a few names).

**New posters:** a new "Printed Signature" product joins the parent automatically; it joins a sub-collection if its
type/title matches, otherwise add the tag `cp-music`, `cp-film`, `cp-tv`, `cp-football`, `cp-american-football`,
`cp-boxing`, `cp-mma-wrestling`, `cp-darts`, `cp-cricket`, `cp-rugby`, `cp-golf`, `cp-tennis`, `cp-horse-racing`,
`cp-motorsport`, `cp-athletics`, `cp-us-sports` or `cp-icons`. A poster without "Printed Signature" in the title also
needs `celebrity-poster`.

Existing poster collections were left untouched (signed-autographed-prints, football-player-autograph, boxer-autograph,
music-star-autograph, movie-star-autograph, etc.); the old "More Prints & Posters" / "Wall Art" / "Sports Fans" menu
columns still link to them. Small overlap: boxing has 1 more product than the classifier (one poster matches two
rule sets).

## Menu (foxy-mega-menu = the live header menu)
`menuUpdate` on `gid://shopify/Menu/314330022269`; every existing item sent back unchanged (re-read and diffed: 501
items before, all 501 identical after, 23 new). Backup of the old menu: `foxy-mega-menu-before.json`.

New top-level item **Celebrity Posters** (→ /collections/celebrity-posters), placed right after Celebrity Masks:
- **Music, Film & TV**: Music Stars · Film Stars · TV Stars · Authors, Scientists & Icons
- **Football**: Football Stars · NFL & American Football · A6 Poster Card Packs (existing `signed-a6-poster-card-packs`)
- **Fight Night**: Boxing · UFC, MMA & Wrestling
- **More Sport**: Darts & Snooker · Cricket · Rugby · Golf · Tennis · Horse Racing · F1 & Motorsport · Athletics &
  Olympians · Basketball, Baseball & Ice Hockey

The live theme ("Foxy Pop 2026 – leavers designer", 189501276541; header.liquid identical to `theme/sections/header.liquid`)
renders any level-1 item with 3 levels as a mega panel with a "Shop all Celebrity Posters" button, so it is live now
(no promo tile yet, the panel uses the no-promo layout). The top bar wraps (flex-wrap), so a 15th item is fine.

## Theme (unpublished copy only)
"Foxy Pop 2026 – swatches & posters" (189514809725): `sections/header-group.json` gets a Department style block `d8`
for "Celebrity Posters" (purple accent, promo tile with the Taylor Swift printed-signature print image
`shopify://shop_images/TaylorSwift.jpg`, "Shop posters" → /collections/celebrity-posters). Re-read: checksum
f06f80c43f3d262a94d8d46bf3730fbb. Mirror: `theme-working-copy-leavers-designer/sections/header-group.json`.
Shows once the owner publishes that copy.

## Notes for the owner
- 9,475 signature posters carry the misleading tags "Other Console Posters" and "Signed Athletics Prints" (they feed
  `all-posters-for-size-options`, so they were NOT removed; probably used by the poster size-options app).
- Product types are messy ("Football Posters" holds horse racing, rugby, MMA, TV posters). Not changed.
- Several sub-collections overlap with older ones (e.g. Music Star Printed Signature Prints, 66 products). Consider
  301-redirecting the old ones to the new handles later.
- Pairing ideas: matching celebrity face masks (link already in the parent description), A6 poster card packs for
  music/film stars (the 2 empty A6 Movie/F1 collections), a "frame upgrade" bundle, and celebrity mugs.
