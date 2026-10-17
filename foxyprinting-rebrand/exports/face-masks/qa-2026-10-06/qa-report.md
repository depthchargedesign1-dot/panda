# Face-mask verification and copy QA: 6 Oct 2026

## Part A: verification against the expected text
Live export: bulk operation 11732538130813 (all 58,747 products), compared byte-for-byte with the expected values built by
`qa/expected2.py` (precedence: masks batches, seo_fix/seo_fix_245/sens mut, fixes b0001/b0002/b0100/b0101, titles/plan.csv,
seotitles (SEO title only), sensitive after*.json, conflicted-titles after-final (no overlap with masks), Bond fixes b0003).

| | count |
|---|---|
| Products checked (all 1,227 mask batches) | 6,133 |
| Exact match on title, description, SEO title and meta | 6,126 |
| Title differs: the 4 deliberate hand fixes (Uri Geller, Laz Alonso, Tyrrell Hatton, Wendy Williams) | 4 (left alone) |
| SEO title differs: Phil Foden (New Hair), hand fix excluded from seotitles | 1 (left alone) |
| Real mismatches repaired (one product per mutation, text copied from the expected source, re-read after) | 2 |

Repairs:
1. **Gary Glitter (Young) 8122432028923**: the seotitles push (b0017) had sent the old party-style meta back over the neutral sensitive rewrite.
   Restored the meta from `after_hall_glitter.json`.
2. **Ekadarville The Defenders 7455548113147**: pre-edit "Grab a Ekadarville" -> file's "Grab an Ekadarville".

## Part B: copy QA of live text
Scripts: `tools/engine.py` with decision tables `tools/dec_names.py` (hand-checked name fixes), `dec_custom.py` (wrong-person rewrites, custom first paragraphs),
`dec_chars.py` (TV/film character disclaimers), `dec_sens.py` (neutral sensitive rewrites), `leak_map.json` (hand-reviewed category leakage).
Every change is listed in `qa-fixes.jsonl` (id, field, types, old, new).

### Products needing a fix, by issue type (a product can have several)
| issue | products |
|---|---|
| SEO title junk / missing "\| Foxy Printing" / over 60 / wrong name (incl. 99 Golden Globes 2025) | 1,272 |
| "theme a themed birthday" / "theme a soap-themed…" duplication | 757 |
| trademark in meta ("Oscars-style party" -> "red-carpet party", Six Nations, Golden Globes) and "photo booth and photo booths" | 378 |
| misspelled or wrong name in copy (title name is the reference) | 318 |
| a/an errors ("a Aaron", "A The Queen", "a Álvaro") | 197 |
| truncated metas (completed or trimmed, all ≤160 chars) | 148 |
| template leakage (wrong occasion/label for the person; tags were unreliable so every case was hand-reviewed) | 128 |
| couple packs: SEO title "A & B Couple Face Masks", disclaimer names both people | 109 |
| disclaimer naming a show/film/product or junk name -> TV/film character template (or brand/original-design note) | 100 |
| junk suffixes in names (Heartstopper, Lupin, Ozark, Narcos, Brooklyn, UK, Lakeside, Sidemen…) | 82 |
| "jubilee-style garden party" for non-royals -> "summer garden party" | 70 |
| sensitive figures: neutral rewrite | 30 |
| wrong-person or character first paragraph rewritten | 27 |
| **total products** | **2,850** |

### Push status
- **Pushed and confirmed (userErrors empty): 130 products** in 26 mutations of ≤5: all 30 sensitive rewrites, all wrong-person rewrites
  (João Pedro, João Gomes, Jørgen Strand Larsen, Rúben Dias, Karla Sofía Gascón, Jamie-Lee O'Donnell, Thomas Ian Griffith, Martín Berrote/Palermo,
  Joseph Michael Cole, Michael Clarke (cricketer), Mark Williams (snooker)), the Spider-Man/Still Game actors, and the character-disclaimer set.
  `tagsAdd third-party-name` on the 30 sensitive products.
- **Queued, not yet pushed: 2,720 products** in `push/qa/batches/b0000–b0543.gql` (5 aliases each, round-trip checked against expected.json: 0 mismatches).
  Send with `./show.sh qa NNNN` -> graphql_mutation unchanged -> `./log.sh qa NNNN ok`. bulkOperationRunMutation is blocked by the MCP safety policy,
  so these must go as ordinary mutations. Themed-duplication-only batches are last (b0441–b0543).
- After sending: bulk-export and run `push/qa/verify_qa.py export.jsonl`.

### Sensitive neutral rewrites (30)
Bill Cosby (×3), Jeffrey Epstein (×3), Evil Epstein, Ed Gein, Jeffrey Dahmer, Reggie Kray, Ronnie Kray, OJ Simpson, Rolf Harris, R Kelly, P Diddy, Stuart Hall (JB copy 9369909064), Osama Bin Laden, Prince Andrew, Vladimir Putin (×2), Kim Jong Un (archived copy 9438735048), Kim Jong Il (×2), Bashar al-Assad, Leon Trotsky, Adolf Hitler (×2), Jonathan King, Josef Fritzl (×2). Neutral satire/theatre/drama copy, no jokes or party hype, nothing for children, no comment on crimes, "does not support or promote the views or
actions of any person portrayed" line, SEO title "<Name> Face Mask for Satire/Drama/Theatre | Foxy Printing", third-party-name tag added. Status unchanged.
Already-done overrides (Savile, Stuart Hall 8122431799547, Gary Glitter ×2, the 9 dictator/other masks, Bond actors) were excluded and not touched.

### For the owner
- Not rewritten, decision needed: Kevin Spacey (×2, acquitted), Marilyn Manson (accused, not convicted), Chris Brown (2009 conviction) still carry party copy.
- Identity assumptions: 9520533448 "Michael Clarke" = the cricketer and 9520750024 "Mark Williams" = the snooker player (old titles said CRICKET/SNOOKER);
  8249154797819 "Joseph Michael Cole" = actor Joe Cole (old title also said Winston Churchill); 15865891815805 "Harry" (Sidemen) SEO title set to Harry Lewis (W2S).
- Couple packs: only the SEO title and disclaimer name both people; the body copy still describes one person (needs a hand-written description).
- Many other fictional characters (Basil Fawlty, Alan Partridge, Del Boy…) still use the celebrity disclaimer; not changed (not show/product names).
- mask-* category tags are wrong on several hundred masks (e.g. US musicians tagged mask-footballers, The Boys cast tagged mask-politicians-royals); copy was fixed, tags not.
- Fat Bastard title is still in titles/skip.csv awaiting a decision.

### 15 before -> after examples
| # | issue (product id) | before | after |
|---|---|---|---|
| 1 | wrong-person copy (15834842628477) | <p>Jo O'Meara was the lead voc | <p>João Pedro is the Brazilian f |
| 2 | wrong-person copy (7807382388987) | <p>Jamie Lee Curtis became a horro | <p>Jamie-Lee O'Donnell played the  |
| 3 | SEO title naming another person (14931220103549) | Karla Sofía Gascon Golden Globes 2025 Celebrity Face Masks | Karla Sofía Gascón Face Mask / Foxy Printing |
| 4 | misspelled name (9520510216) | Olivier Ground Face Mask: guaranteed laughs at any party. A4 size on 350gsm card, with eye holes cut and elastic included. Order yours today. | Olivier Giroud Face Mask: guaranteed laughs at any party. A4 size on 350gsm card, with eye holes cut and elastic included. Order yours today. |
| 5 | misspelled name (9369898184) | Get the party started with a Jason Mannford face mask. Full-colour print on 350gsm card, cut to shape with elastic. Great for a stag or hen do. | Get the party started with a Jason Manford face mask. Full-colour print on 350gsm card, cut to shape with elastic. Great for a stag or hen do. |
| 6 | template leakage (jubilee for US actor) (7808947945723) | <p>Planning a jubilee-style garden party?  | <p>Planning a series finale watch party? T |
| 7 | template leakage (musician as football star) (14834571116925) | <p>Bring a famous face to a five-a-side end-of-season do | <p>Bring a famous face to a concert pre-party with this Doja Ca |
| 8 | template leakage (club awards night) (14931213844861) | <p>Planning a club awards night? This Em | <p>Planning a series finale watch party? This Emma |
| 9 | disclaimer naming a show (7558244466939) | <p>Still Game follows pensio | <p>Mark Cox is the Scottish actor who played tight-fisted Tam Mullen in Still Game. Bring this ma |
| 10 | disclaimer naming a film (7550957912315) | <p>Planning a movie night? This REGGIE Bad Boys face mask is the easy fa | <p>Planning a movie night? This Reggie face mask is the easy fa |
| 11 | a/an + junk name (8062787158267) | ace to a street party with this The Queen Coronation face mask, printed on s | ace to a street party with this The Queen face mask, printed on s |
| 12 | junk words / misspelling in SEO title (9530629512) | Darcy Bussel Face Mask / Foxy Printing | Darcey Bussell Face Mask / Foxy Printing |
| 13 | Golden Globes SEO title (14931204669821) | Jeremy Allen White Golden Globes 2025 Celebrity Face Masks | Jeremy Allen White Face Mask / Foxy Printing |
| 14 | themed duplication (9233214024) |  at a themed birthday with a Leonardo Di Caprio face mask that's m |  at a themed birthday with a Leonardo DiCaprio face mask that's m |
| 15 | couple pack SEO title (8350245814523) | Jay-Z Face Mask Beyoncé / Foxy Printing | Beyoncé & Jay-Z Couple Face Masks / Foxy Printing |
