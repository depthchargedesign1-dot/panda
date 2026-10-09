# Sales-channel publishing, 6 Oct 2026

Source: bulk export of all 56,022 ACTIVE products (bulk op 11739389428093), checking Online Store,
Facebook & Instagram (68348608699), TikTok (78820802811) and Google & YouTube (10722541604).

- 55,355 were already on all four. 538 were on the Online Store but missing from one or more channels
  (537 missing FB&IG, 538 missing TikTok, 537 missing Google). 129 ACTIVE products are not on the Online Store
  at all (`2026-10-06-active-not-on-online-store.csv`); left alone.
- 475 published to all three channels with `publishablePublish` (no errors). Nothing was unpublished.
- Mid-run the owner's new rule arrived (no copyright/trademark-risk items on social/Google). The first 275
  had already gone out; 18 of those fall under the new rule: `2026-10-06-risky-already-published.csv`
  (left published; owner to decide).
- 63 skipped under the new rule: `2026-10-06-skipped.csv` (reasons per row).
- `2026-10-06-publish-log.jsonl`: one row per product (published or skipped), for re-runs.
- `build_classify.py`: the risk rules used (tag third-party-name, club names, masks, signed prints,
  retro-gaming risk list, brand/character words, rude words), plus two manual skips.
