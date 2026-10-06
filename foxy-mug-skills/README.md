# Foxy Printing mug designer skills

| Skill | What it does |
|---|---|
| `mug-designer-bot` | Main entry. Send phrases/images -> concepts -> artwork -> Dropbox -> images -> Shopify -> marketplace files |
| `mug-print-artwork` | mugkit engine: 300 dpi wrap PNG, live-text PDF + mirrored PDF, layered SVG, proof, mockups, zip |
| `football-shirt-mug` | Proper drawn football shirt with editable NAME + NUMBER (stripes, hoops, halves, quarters, sash...) |
| `mug-lifestyle-shopify` | Mockups + Higgsfield lifestyle photos (checked for correct print) + Foxy Printing Shopify draft |

**Claude.ai:** Settings -> Capabilities -> Skills -> Upload skill, and upload each `.zip` in this folder.
**Claude Code:** they are already active from `.claude/skills/` in this repo.

The scripts are fetched from this (public) repo's branch `claude/designer-bots-mug-products-auuvhs`
when they run in the Higgsfield sandbox, so keep that branch (or update the URL in
`mug-print-artwork/SKILL.md` after merging).

Preview: `.claude/skills/football-shirt-mug/examples/preview.jpg`

| `amazon-listing-converter` | Shopify -> Amazon UK upload pack: variations, Amazon Custom (name/number boxes), IP hold-back, filled category template, JSON_LISTINGS_FEED |
