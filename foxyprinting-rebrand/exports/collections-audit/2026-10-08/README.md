# Empty collections audit (8 Oct 2026)

Owner asked: find every collection with no products (bad for Google), fill the relevant ones with a new product, flag outdated or wrongly reactivated items, and list what is empty.

**"Visible"** = products that are ACTIVE **and** published to the Online Store (what shoppers and Google see).
Counted per collection with `productsCount(query:"collection_id:N status:active published_status:published")`.

Full list: **`empty-collections.csv`** (title, handle, URL, smart/manual, rule, on Online Store, total, visible, class, recommendation).
Raw data: `raw/` (all 491 collections, counts). Script: `tools/collections_audit.py`.

## Numbers
- **491 collections** in total (417 on the Online Store).
- **79 empty** (0 visible). Only **56** of those are on the Online Store, so only 56 matter to Google; the other 23 are already hidden.
- **29 near-empty** (1–2 visible).

## What the 56 empty, live collections are
| Class | Count | What to do |
|---|---|---|
| a. Outdated (VE Day 80th, King Charles Coronation 2023, "Printed Clothing New 2023", Covid "Social Distancing Stickers") | 34 | Products are already DRAFT: keep them that way. **Hide each collection from the Online Store** and add a 301 redirect (Shopify won't let Claude unpublish). |
| b. Products draft/archived on purpose | 6 | Atari posters / 7800 posters / Jaguar (drafted 7 Oct: retro box art and logos, keep draft, hide collection); Errea bags (UNLISTED old stock); leavers designer hoodies (drafts waiting for you); Plaques & occasion gifts (fixed, see c). |
| c. Broken rule / wrong tag, **fixed today** | 6 + 1 | Unicorn Santa Sacks, RuPaul's Drag Race, Stag & Hen Party Products, Personalised Flask, I Love Celebrity Mugs, The Voice; plus Plaques & occasion gifts (5 live plaques added). |
| d. Genuinely empty and still relevant | 8 | New products for 6 (see below); 2 A6 card-pack collections queued. |
| e. Duplicates of a live collection | 2 | THIS GUY IS, THIS IS MY BIRTHDAY MUGS: hide + 301 to the live one. |

## Rules fixed (8 Oct, directly, per house rule on tags/collection rules)
Old rules are in the CSV `rule` column (taken before the change) so they can be put back.
- `unicorn-santa-sacks`: TAG "UNICORN SANTA SACKS" (no product had it) → TITLE CONTAINS "Unicorn" AND TAG "Santa Sacks".
- `ru-pauls-drag-race`: added TAG "Ru Paul Drag Race" (spelling on the products).
- `stag-hen-ideas`: now a hub of stag & hen masks and T-shirts (OR of 7 tags).
- `personalised-flask`: added TAG "hip flask".
- `i-love-celebrity-mugs`: added TITLE CONTAINS "I Love Celebrity".
- `the-voice`: tag `THE VOICE` added to 12 masks of coaches/presenters (will.i.am ×2, Tom Jones, Danny Jones ×2, Anne-Marie, Emma Willis ×2, Rita Ora, Boy George, Holly Willoughby ×2).
- `plaques-occasion-gifts` (manual, in the mega menu): added 5 live products (wooden photo plaque, round award plaque, ceramic photo tile, heart photo tile, acrylic club award).

## Outdated items that are ACTIVE and visible right now (please decide)
Nothing outdated looks *reactivated*: every VE Day / Coronation collection product is DRAFT. But these older products are still ACTIVE on the website with dated wording:
- **Coronation 2023 royal masks (11)**: King Charles III, Prince William, Kate, Camilla, "The Queen", Prince Philip, 8-pack, King + crown, 5-pack, 12-pack, Queen Camilla 10-pack. Suggest: retitle without "Coronation 2023" (royal fancy-dress masks still sell). The Queen and Prince Philip have died: draft those or keep only as "royal family" fancy dress, your call.
- **Jubilee masks (3)**: Diamond Jubilee 7-pack, Queens Jubilee bulk mask, 8-pack Royal Family "Wedding Jubilee". Retitle or draft.
- **Euro 2020/2021 mask packs (12)**: England packs 1–9, "It's Coming Home", full squad (Euro 2020), Wales, Belgium. Most players have retired or left the squad; title typo "STRELING". Suggest DRAFT (World Cup 2026 masks would replace them).
- **Wales Football Face Masks** collection (`wales-2021-football-face-masks`): only that Wales Euro 2021 pack is live.
- **Euro 2024 / Eurovision 2024 / Darts 2024 / Golden Globes 2025 / "2023" celebrity masks** (~200): the people are fine; the year in the title dates them. Suggest a bulk retitle that removes the year (owner to OK).
- **Father's Day cards 54 and 94** ("social distance"): Covid jokes, updated today 08:44 by another job. Suggest draft.
- **EURO 2016 France birthday card**: dated, suggest draft.
- **Premier League Darts Masks 2024** collection (10 live): rename to "Premier League Darts Masks" before the 2027 season.
- **VE Day Bunting** (`ve-day-bunting`, hidden collection) still has 1 ACTIVE product visible on the store: draft it.

## New products for the genuinely empty collections
See "Phase 2" below (filled in as they are made).

## Queue (not done yet)
- A6 Movie and Film Poster Card Packs, A6 Printed Signature F1 Poster Card Packs: need your say on which films/drivers (no studio/team logos). Until then, hide both.
- Near-empty collections (1–2 products, see CSV) should get more products over time.
