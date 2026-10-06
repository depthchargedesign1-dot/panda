# Face mask copy fixes – import (6 Oct 2026)

2,714 face masks get corrected wording (130 more were already fixed live, including all 30 sensitive-figure neutral rewrites).
Fixes: junk/over-long SEO titles, misspelled or wrong names, "theme a themed birthday", trademarks in meta descriptions,
a/an errors, cut-off meta descriptions, wrong occasions, disclaimers naming a show as a person. Full list: ../qa-report.md, ../qa-fixes.jsonl.

Columns: Handle, Body (HTML), SEO Title, SEO Description. Titles, prices, images, tags and status are not in the file, so they don't change.

## Import
1. Products → Import → `00-TEST-3-masks.csv`, tick **Overwrite products with matching handles**. Open one of the 3 masks and check the description and "Search engine listing".
2. Import `01-mask-copy-fixes.csv` (2,720 rows).

## Update 6 Oct 2026: rows removed
01-mask-copy-fixes.csv now has 2,714 rows. The Little Britain masks were removed earlier, and these 5 were removed because they got a neutral rewrite pushed live (owner's decision; rollback in exports/rollback/2026-10-05-sensitive-masks/): Kevin Spacey JB, Chris Brown (High-Quality and 2025), Chris Brown & Rihanna (both packs). Kevin Spacey 9369921032, Marilyn Manson and Chris Brown JB were not in the CSV. 00-TEST had none of them.
