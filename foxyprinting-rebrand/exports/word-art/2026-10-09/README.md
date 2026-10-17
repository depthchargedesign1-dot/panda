# Word art: Ben's Dropbox folder review + new products + sub-categories (9 Oct 2026)

Owner: "review this folder G:\Dropbox\BENS FILES\OLD STUFF\WORD ART HQ JPEG, upload them all to foxyprinting under word art posters in their own sub categories if you think we are allowed".

## The folder (1,425 images; Dropbox path /BENS FILES/OLD STUFF/WORD ART HQ JPEG/WORD ART HQ JPEG)
| Set | Verdict |
|---|---|
| WORD ART LETTERS WITH NAMES (74 boys + 79 girls named examples, ~900 frame/card mock-ups) | Already sold as the 52 personalised Pink/Blue Letter A-Z products, so no new products. The named JPEGs are examples only. |
| POPS (29 Disney princess / Harry Potter / Friends designs x 3 frames) | All 29 already live ("Inspired By Pop Figures"). Third-party characters: legally risky, website only. |
| MOVIES (45: Batman, Joker, Deadpool, Marvel logo, Captain America shield, Star Wars, Toy Story, Up, LOTR, Game of Thrones, Stan Lee, Scarface...) | NOT uploaded: studio characters/logos (Disney, Marvel, DC, Lucasfilm, Warner) and real people. |
| Root: Avengers Endgame, Royal Wedding Big Bang Theory | NOT uploaded (same reason). |
| AGES (Age 16-100 rainbow numbers) | UPLOADED: 11 new rainbow age products. ("Colourful 80 Em" is a customer's order with names, skipped.) |
| ANIMALS AND HOBBIES: Mum 1, MAM 2 | UPLOADED: 2 new heart products. |
| ANIMALS AND HOBBIES: Nanna Loveheart, charlie bear, BABY BLUE ELEPHANT (BEN) | Skipped: real family/customer names in them. |
| ANIMALS AND HOBBIES: baby blue dog | Skipped: it's Blue from Blue's Clues (Nickelodeon character). |
| ANIMALS AND HOBBIES: panda, dolphin, flamingo, elephants, fox, owl, lion, girls basketball/football/biking/scooter | ON HOLD: the cartoon pictures look like bought clip art; licence to be confirmed by the owner. |
| GEMINI 1 (black/white frame mock-ups, 800 px) | Skipped: mock-ups only, no print-resolution artwork. |

## Created (ACTIVE, Online Store + Shop + Google + FB/IG + TikTok)
`created.json`: 11 x "Personalised <N> Birthday Rainbow Word Art Print - Number N" (16, 18, 21, 30, 40, 50, 60, 70, 80, 90, 100),
"Personalised Mum Heart Word Art Print", "Personalised MAM Word Art Print". Same 8 sizes/prices as the existing word art
(A4 4.99, A3 9.99, A2 12.99, A1 19.99, A4 framed 19.99, A3 framed 29.99), template `personalised`, same 2 personalisation
fields, Google fields, SKUs FOXY-POSTER-WA-RAINBOW-<N>-<size> / FOXY-POSTER-WA-MUM|MAM-HEART-<size>.
Images: real store frame photos (black + silver, `tools/word_art_new/framed_images.py`) + print-only flat.
Originals copied to Dropbox `/AI DESIGNS 2026/<title> - <SKU>/`.

## Sub-categories (smart collections by tag, Online Store + Shop; tiles via `foxy.subcollections` on personalised-word-art-prints)
word-art-name-letters (wa-names, 52) · word-art-ages-birthdays (wa-ages, 25) · word-art-pets-animals (wa-pets-animals, 53) ·
word-art-hobbies-sport (wa-hobbies-sport, 21) · word-art-love-family (wa-love-family, 18) · word-art-kids (wa-kids, 24) ·
word-art-places-home (wa-places, 3) · word-art-pop-characters (wa-pop, 29). Sorting rules: `tools/word_art_new/subcategories.py`;
`subcategory-tags.csv` = the 212 existing products and their tag. New word art products need one wa-* tag to join a sub-category.
