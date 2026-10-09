# Description & SEO cleanup (Oct 2026)

Fix 2 (descriptions) and Fix 3 (SEO) from `../catalogue-audit/2026-10-09/README.md`. Built by a side session for the main session to hand over. **CSV imports are run by the owner only.** None of these files are in `IMPORT-SCHEDULE.md` yet; the main session adds them.

## 1. Compliance fixes: DONE, pushed straight to the store (9 Oct 2026)
- **318 products** updated through the API (`productUpdate` in batches of 6–12, every result checked; a sample re-read after the push matched).
  - "Limited Edition", "memorabilia", "Autographed"/"Collectible" taken out of titles and copy (reproduction prints now say "Printed Signature" and carry the signed-print disclaimer).
  - The right disclaimer is the last block (`<h3>Please note</h3><p class="disclaimer">`), with the real names filled in.
  - `third-party-name` tag added where it was missing.
  - SEO title (≤ 60) and meta description (140–155) set on every one.
- Plus the 2 royal family 8-pack masks (`7710732189947`, `8062795743483`), fully rewritten.
- Record of exactly what was sent: `compliance-api/applied_2026-10-09.json.gz`. Readable list: `compliance-api/review.csv`. All 318 descriptions on one page: `compliance-api/samples.html`.
- Generator: `tools/compliance_copy.py`.
- **Left out on purpose:**
  - 2 baby grows "Boys/Girls Name Limited Edition": this is the slogan printed on the vest, so they're left for the baby vest rewrite.
  - The "movie memorabilia" hobby coaster: it names a hobby; it doesn't claim the product is memorabilia.
  - The personalised sock: rewritten by hand; its material and sizes are **ASK**.
- Fixed on the way:
  - K-pop masks where the old copy named the member's real name as the "group" (DK, Jun, Wonwoo, The8 → SEVENTEEN).
  - "Evan" mask: the store lists Evan as ENHYPEN, which has no member called Evan, so the group was left out. **Owner: which group is Evan in?**
  - Halloween III title no longer says Michael Myers (he isn't in that film), and the Halloween 6 title now says 1995.

## 2. "[brackets]" (80 products): not a customer-facing problem
All 80 are PerfectDraft Maxi Skins. The "brackets" are Word leftovers (`<!--[if !supportLineBreakNewLine]-->`) **inside HTML comments**, so shoppers never see them. The real problems are that these 82 listings are pasted from Word with inline styles, US spelling ("customize"), no disclaimer (PerfectDraft, Star Wars, Harry Potter, football clubs…) and contradictory specs: the titles say "vinyl sticker" but the handles say "magnetic skin". Their rewrite is waiting on the new **PerfectDraft skins** ASK section in `plan/product-facts.md`.

## 3. Active products with an empty description (49): owner decisions, not copy
| Group | Count | Suggestion |
|---|---|---|
| Poster upgrade helper items ("Poster is UPGRADED to A4 Gold Framed…", A0 upgrade) | 11 | Hide from Google & search (they're add-on items, not products). No copy needed. |
| SNES cases where the handle names a different game from the title (e.g. title "Romance Of The Three Kingdoms II", handle `roger-clemens-mvp-baseball…`) | 15 | Check which game each one really is, then they'll join the SNES case rewrite. |
| "Valentines" mugs built on homophobic slurs ("YOUR A DYKE / FAG / QUEER / FUCKTARD BUT I DO LOVE YOU") | 8 | **Recommend archiving.** No copy written. Marketplaces and Google will reject them anyway. |
| 2016-era items: 100 business cards, address labels (4 sizes), "Copy Of 12 X Personalized Princess Party Stickers", "Personalized Iron Man Kitkat Label", "Poster", "Wedding Gifts", "Rear Print on 123 Bundle" | 10 | Archive, or say which to keep and I'll write them up. |
| "This Girl Loves Ball / Breeding / Dt / Game" mugs | 4 | What do "Breeding" and "Dt" mean on these? Then they get mug copy. |
| "Test Party Bunting" | 1 | It's a test product that is ACTIVE. Set it to draft? |

## 4. SEO titles & meta descriptions: IMPORT FILE READY
- `seo-fill/seo-fill-01.csv`: **3,484 products**, columns `Handle, SEO Title, SEO Description` only (no Title/Status/Body). 0.9 MB. Import with "Overwrite products with matching handles".
- The 318 products from step 1 are excluded (they already have SEO from the API push).
- Where a product already had a valid value, that value is kept as it is. Only missing or broken fields were written: 3 printed gift tins had a meta description cut off mid-sentence ("Great for.").
- Checks on every row:
  - title ≤ 60 characters, meta 140–155 characters;
  - none of the words official / licensed / authentic / genuine / approved / endorsed / signed / autographed / memorabilia / limited edition;
  - no duplicate titles (repeats become "… Design 2", "… Design 3").
- What's in it:
  - **retro gaming posters, 3,307:** game name + "Retro Gaming Poster"; console brand names kept out of the title;
  - **Printed Signature music posters, 67:** "Printed Signature", never "signed";
  - **Santa sacks, 49:** hessian is only mentioned where the title says hessian; XL sacks don't claim a material;
  - **printed gift tins, 30;** **rugby towels, 9:** generic first, "Personalised Rugby Bath Towel – Bradford 1995 Away";
  - **kids' birthday banners, 15;** **football face coverings, 2;** **mugs, 2.**
- `seo-fill/skipped.csv` (31): 25 hidden option-helper products (not for sale), 4 retro posters whose game name can't be read from the title ("X", "D", "Th Ps3", "Mr Super Nintendo"), and "Santa Approved" (the design name contains "approved"; its handle says XL but its title says Small, so it needs checking).
- `seo-fill/notes.csv`: 2 cards that only got a title (no card meta template in this pass).
- Generator: `tools/seo_fill.py` (re-runnable on a fresh export).

**Samples (3 of 3,484):**
| Handle | SEO Title | SEO Description |
|---|---|---|
| `adventure-island` | Adventure Island Retro Gaming Poster \| Foxy Printing | Adventure Island retro gaming poster, a fan-made print made to order in our North Yorkshire workshop. A great gift for any gamer. Order today. |
| `westlife-2-signed-autographed-music-star-print-copy` | Westlife Printed Signature Poster 2 \| Foxy Printing | Fan-made Westlife music poster with a printed signature-style design. Printed to order in North Yorkshire. Order today. Ideal for a bedroom wall. |
| `personalised-santa-paws-bella-santa-sack-xl-extra-large-custom-name` | Personalised Santa Paws Bella XL Santa Sack \| Foxy Printing | Make Christmas Eve magic with a personalised extra large Santa sack: the Santa Paws Bella design, printed with any name in North Yorkshire. Order today. |

**Overlap to know about:** the 4 Oct retro poster import files (`../retro-posters/`, never imported) also set SEO on many of the same posters, plus new body copy, titles and prices. If the owner imports those later, they will overwrite these SEO values with their own (also compliant) ones. Either order is safe.

## 5. Family description rewrites: next
Order: Baby Vest, Kids Cards, Gaming Cards, Movie Cards, Holiday Stockings (+ dedupe), Coasters, SNES cases, NES/SNES posters/magnets/keyrings, Football Posters. Three samples per family will be added here before each full file. Families whose facts are **ASK** in `plan/product-facts.md` wait for the owner's answers.

## 6. Baby vests / baby grows: IMPORT FILE READY (9 Oct 2026)
- `baby-vest/baby-vest-descriptions.csv`: **2,004 products** (all ACTIVE £8.99 single-variant "Baby Vest" listings), columns `Handle, Body (HTML)` only, 3.4 MB. Import with "overwrite matching handles". The 67 newer £12.99 vests already have new copy and aren't in the file.
- Every row was checked:
  - one H2, then H3s;
  - no inline styles, spans or images;
  - 180–350 words;
  - none of the banned words (design slogans in quotes are allowed, e.g. "I Have The Best Dad Ever");
  - the disclaimer is the last block where a name appears.
- **Disclaimers:**
  - 862 football designs: sports template with the real club (spelling fixed: Bournmouth, Milwall, Tettenham, Gillngham…; Scottish clubs name the SPFL; England/Scotland/Wales name the FA);
  - 28 film/TV designs: Star Wars, Batman, Harry Potter, Game of Thrones, Pokémon, Frozen, Star Trek;
  - 10 band designs (Happy Mondays, Oasis);
  - 4 game designs (PlayStation, Xbox, Call of Duty);
  - 2 brand puns (Apple and Nintendo).
- **`third-party-name` tag: DONE via API** on those 906 products (re-counted afterwards: 908 Baby Vests carry the tag, including 2 that already had it). Not in the CSV, because a Tags column would wipe the other tags.
- Facts used: the baby grow sheet only (100% cotton, short sleeve, nickel-free poppers, wash and iron inside out, 4 sizes 0–3 to 9–12 months, made in North Yorkshire). No blank brand or print method is named (both still **ASK**).
- **ASK (added to the fact sheet):** these listings have **no size option and no personalisation box**, but the old copy said "email us your personalisation" and every listing is tagged "Add Name On Back". How does a customer pick the size and give the name? Until then the copy says "it comes in four sizes" and "let us know the name when you order", without saying how.
- **Channel note:** 862 are football designs; titles like "…Personalised FOOTBALL TEAM Baby Grow" may show club crests. Under the 6 Oct rule those must stay off Google/Facebook/TikTok. That's not checked here.
- Review: `baby-vest/review.csv` (handle, kind, name used in the disclaimer, word count), `baby-vest/samples.html`. Generator: `tools/baby_vest_copy.py`.

**3 samples:**

`me-and-my-aunty-love-lincoln-city-personalised-football-team-baby-grow`

```html
<p>Start them young with our Me and My Aunty Love Lincoln City baby grow, a fan-made Lincoln City baby vest that's perfect for match days, a baby shower or a new arrival.</p>
<h2>Me and My Aunty Love Lincoln City baby grow for Lincoln City fans</h2>
<p>The front reads “Me and My Aunty Love Lincoln City” in a bold football fan design. It's a lovely gift from an aunty who wants to pass on the football bug. It comes in four sizes, from 0–3 months up to 9–12 months. Want their name on the back? Tell us the name when you order and we'll add it.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Soft 100% cotton, kind to delicate skin</li>
<li>Printed in-house in North Yorkshire, UK, and made to order</li>
<li>A lovely gift for a baby shower</li>
<li>Four sizes from newborn (0–3 months) to 9–12 months</li>
<li>Wash and iron inside out to keep the print looking good</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Sizes: 0–3 months, 3–6 months, 6–9 months, 9–12 months</li>
<li>Material: 100% cotton, soft feel</li>
<li>Style: short sleeve baby vest with nickel-free poppers</li>
<li>Care: wash and iron inside out</li>
<li>Printed in North Yorkshire, UK</li>
</ul>
<h3>Delivery</h3>
<p>Each baby grow is printed to order in our North Yorkshire workshop. Postage options and costs are shown at checkout.</p>
<p>Buying for a baby shower? Add a personalised card and the Me and My Aunty Love Lincoln City baby grow is ready to give. Custom designs on request: call 01439 771468.</p>
<h3>Please note</h3>
<p class="disclaimer">This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or affiliated with Lincoln City, the Premier League, the English Football League or any club, league or player. Club and player names are used only to describe the design and who it's for. All trademarks belong to their respective owners.</p>
```

`i-have-the-best-dad-ever-personalised-baby-boy-girl-unisex-short-sleeve-bodysuit`

```html
<p>Say it with a slogan: our I Have The Best Dad Ever baby grow reads “I Have The Best Dad Ever” and is made in-house in our North Yorkshire workshop.</p>
<h2>I Have The Best Dad Ever baby grow</h2>
<p>The front of the vest reads “I Have The Best Dad Ever”. It makes a thoughtful gift from Dad or for a proud dad. It comes in four sizes, from 0–3 months up to 9–12 months. We can also add a name on the back, so just let us know the name you'd like when you order.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Short sleeves and nickel-free poppers for quick, easy nappy changes</li>
<li>Printed in-house in North Yorkshire, UK, and made to order</li>
<li>A lovely gift for a hospital bag surprise</li>
<li>Four sizes from newborn (0–3 months) to 9–12 months</li>
<li>Wash and iron inside out to keep the print looking good</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Sizes: 0–3 months, 3–6 months, 6–9 months, 9–12 months</li>
<li>Material: 100% cotton, soft feel</li>
<li>Style: short sleeve baby vest with nickel-free poppers</li>
<li>Care: wash and iron inside out</li>
<li>Printed in North Yorkshire, UK</li>
</ul>
<h3>Delivery</h3>
<p>Each baby grow is printed to order in our North Yorkshire workshop. Postage options and costs are shown at checkout.</p>
<p>Buying for a baby shower? Add a personalised card and the I Have The Best Dad Ever baby grow is ready to give. Custom designs on request: call 01439 771468.</p>
```

`future-jedi-master-personalised-baby-boy-girl-unisex-short-sleeve-bodysuit`

```html
<p>Our Future Jedi Master baby grow is a sweet, funny way to dress a little one, printed with “Future Jedi Master” and made to order here in North Yorkshire.</p>
<h2>Future Jedi Master baby grow</h2>
<p>The front of the vest reads “Future Jedi Master”. It's a fun outfit for everyday wear and a guaranteed photo moment. It comes in four sizes, from 0–3 months up to 9–12 months. A name on the back makes it even more special: just let us know it when you order.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Soft 100% cotton, kind to delicate skin</li>
<li>Short sleeves and nickel-free poppers for quick, easy nappy changes</li>
<li>Printed in-house in North Yorkshire, UK, and made to order</li>
<li>A lovely gift for a new arrival</li>
<li>Four sizes from newborn (0–3 months) to 9–12 months</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Sizes: 0–3 months, 3–6 months, 6–9 months, 9–12 months</li>
<li>Material: 100% cotton, soft feel</li>
<li>Style: short sleeve baby vest with nickel-free poppers</li>
<li>Care: wash and iron inside out</li>
<li>Printed in North Yorkshire, UK</li>
</ul>
<h3>Delivery</h3>
<p>Each baby grow is printed to order in our North Yorkshire workshop. Postage options and costs are shown at checkout.</p>
<p>Make it a set with a matching personalised mug for the proud parents. Want a different slogan? We do custom designs on request: call 01439 771468.</p>
<h3>Please note</h3>
<p class="disclaimer">This is an unofficial design inspired by Star Wars. It is not official merchandise and is not endorsed by, sponsored by, or connected with Star Wars, Lucasfilm or Disney, or any of their licensees. All names, characters and trademarks belong to their respective owners.</p>
```

## 7. Character birthday cards (Kids, Gaming, Movie Cards): IMPORT FILES READY (9 Oct 2026)
- `cards/kids-cards-descriptions.csv` (1,185), `cards/gaming-cards-descriptions.csv` (1,060), `cards/movie-cards-descriptions.csv` (876): all ACTIVE old-HTML listings in those three types. Columns `Handle, Body (HTML)` only (1.6–1.9 MB each). Overwrite matching handles.
- Facts used: the personalised cards sheet only:
  - 350gsm silk art board, printed A4 and folded to A5, machine cut and folded;
  - printed inside and out if wanted;
  - free white envelope, posted flat in a board-backed envelope;
  - Royal Mail 1st Class, same day or next working day at busy times.
- These listings have **no live preview or personalisation box of their own**, so the copy says "add the name, age and message when you order" (the same wording as their current SEO meta), plus the house line about checking spelling.
- The theme name comes from each title, with the old boilerplate removed ("THEME INSPIRED Kids Adult Personalised Birthday Card…", "(SA060917)"), design numbers kept as "(design 3)", and capitals and roman numerals tidied.
- **Disclaimers:**
  - every card names someone else's character, show, film or game, so 3,117 get one (4 generic designs such as "Elephant 3D" don't);
  - Kids/Movie Cards use the TV/film template ("its makers or rights holders");
  - Gaming Cards use the video-game template ("the game's publisher or any console maker");
  - Movie Cards add a sentence for the named actors.
- **`third-party-name` tag:** being added through the API (see the status line).
- **Owner note:** these designs use other people's character artwork. A disclaimer helps, but it doesn't give permission (see the note in CLAUDE.md). They're also 2017-era listings with odd titles ("Usa Gotg Chi Rocket", "Metroidsamusreturns"). Retiring the weakest sellers may be worth more than a rewrite.
- Review: `cards/review.csv` (theme name used for each handle), `cards/samples.html`. Generator: `tools/cards_copy.py`.

**3 samples:**

`personalised-kids-teletubbies-1-kidshows-birthday-card-sa`

```html
<p>Make their day with a personalised Teletubbies birthday card, printed on thick card in our North Yorkshire workshop and posted 1st Class.</p>
<h2>Teletubbies birthday card with name and age</h2>
<p>It's a Teletubbies inspired design (design 1), personalised with the name and age of the birthday little fan. We can print inside and out, so add your own inside message when you order. We print exactly what you enter, so please double-check names and spelling.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Printed on 350gsm silk art board, much thicker than the usual 240gsm card</li>
<li>Printed A4 and folded to A5, then machine cut and folded for a crisp finish</li>
<li>Personalised with their name, age and your own message</li>
<li>Printed inside and out if you want a message inside</li>
<li>Posted flat in a board-backed envelope so it arrives uncreased</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Size: printed A4, folded to A5</li>
<li>Card: 350gsm silk art board</li>
<li>Finish: machine cut and folded</li>
<li>Includes: free white envelope</li>
<li>Personalisation: name, age, front message and inside message</li>
</ul>
<h3>Delivery</h3>
<p>Sent Royal Mail 1st Class, dispatched the same day, or the next working day at busy times. It's posted flat in a board-backed envelope.</p>
<p>Buying for a little fan? Add a personalised mug or poster for a matching gift. Custom card designs on request: call 01439 771468.</p>
<h3>Please note</h3>
<p class="disclaimer">This is an unofficial design inspired by Teletubbies. It is not official merchandise and is not endorsed by, sponsored by, or connected with Teletubbies, its makers or rights holders, or any of their licensees. All names, characters and trademarks belong to their respective owners.</p>
```

`personalised-final-fantasy-xiii-1-game-birthday-card-sa`

```html
<p>Looking for a card for a Final Fantasy XIII fan? This personalised Final Fantasy XIII birthday card is made to order with the name, age and message you choose.</p>
<h2>Personalised Final Fantasy XIII birthday card</h2>
<p>You get a Final Fantasy XIII inspired card (design 1), printed with the name and age you give us. Want a message inside? Add it when you order and we'll print that as well. We print exactly what you enter, so please double-check names and spelling.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Printed A4 and folded to A5, then machine cut and folded for a crisp finish</li>
<li>Personalised with their name, age and your own message</li>
<li>Printed inside and out if you want a message inside</li>
<li>Comes with a free white envelope</li>
<li>Posted flat in a board-backed envelope so it arrives uncreased</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Size: printed A4, folded to A5</li>
<li>Card: 350gsm silk art board</li>
<li>Finish: machine cut and folded</li>
<li>Includes: free white envelope</li>
<li>Personalisation: name, age, front message and inside message</li>
</ul>
<h3>Delivery</h3>
<p>Sent Royal Mail 1st Class, dispatched the same day, or the next working day at busy times. It's posted flat in a board-backed envelope.</p>
<p>Buying for a gamer? Add a personalised mug or poster for a matching gift. Custom card designs on request: call 01439 771468.</p>
<h3>Please note</h3>
<p class="disclaimer">This is an unofficial, fan-made card produced by Foxy Printing, inspired by Final Fantasy XIII. It is not made, endorsed or licensed by the game's publisher or any console maker. All trademarks, characters and game titles belong to their respective owners and are used only to identify the theme.</p>
```

`jennifer-lawrence-in-the-hunger-games-catching-fire-movie-birthday-card-sa`

```html
<p>Looking for a card for a Jennifer Lawrence In The Hunger Games Catching Fire fan? This personalised Jennifer Lawrence In The Hunger Games Catching Fire birthday card is made to order with the name, age and message you choose.</p>
<h2>Personalised Jennifer Lawrence In The Hunger Games Catching Fire inspired birthday card</h2>
<p>You get a Jennifer Lawrence In The Hunger Games Catching Fire inspired card, printed with the name and age you give us. Want a message inside? Add it when you order and we'll print that as well. We print exactly what you enter, so please double-check names and spelling.</p>
<h3>Why you'll love it</h3>
<ul>
<li>Printed on 350gsm silk art board, much thicker than the usual 240gsm card</li>
<li>Printed A4 and folded to A5, then machine cut and folded for a crisp finish</li>
<li>Personalised with their name, age and your own message</li>
<li>Comes with a free white envelope</li>
<li>Posted flat in a board-backed envelope so it arrives uncreased</li>
</ul>
<h3>Size &amp; details</h3>
<ul>
<li>Size: printed A4, folded to A5</li>
<li>Card: 350gsm silk art board</li>
<li>Finish: machine cut and folded</li>
<li>Includes: free white envelope</li>
<li>Personalisation: name, age, front message and inside message</li>
</ul>
<h3>Delivery</h3>
<p>Sent Royal Mail 1st Class, dispatched the same day, or the next working day at busy times. It's posted flat in a board-backed envelope.</p>
<p>Pair the personalised Jennifer Lawrence In The Hunger Games Catching Fire birthday card with a personalised mug for a birthday gift that's sorted in one go. Custom cards on request: call 01439 771468.</p>
<h3>Please note</h3>
<p class="disclaimer">This is an unofficial design inspired by Jennifer Lawrence In The Hunger Games Catching Fire. It is not official merchandise and is not endorsed by, sponsored by, or connected with Jennifer Lawrence In The Hunger Games Catching Fire, its makers or rights holders, or any of their licensees. All names, characters and trademarks belong to their respective owners. Any actors or public figures named or pictured have not endorsed, sponsored or approved this product, and Foxy Printing has no connection with them. Their names are used only to describe the design.</p>
```
