# Celebrity face mask folders: phase 1 move plan (read-only)

Made on 5 Oct 2026 from a full read-only listing of `/2019 TIDY - CELEBRITY FACEMASKS FINAL 7200 IMAGES` (13,054 entries: 12,875 files, 179 folders). **Nothing in Dropbox has been moved, copied, renamed, created or deleted.**

Files: `plan.csv` (one row per source file), `proposed-folders.md`, `missed-candidates.md`, `inventory.csv` (every file and folder in the set, with size and dates), `raw-listings.tar.gz` (the raw Dropbox listings), `tools/` (the scripts).

## Totals

| | TO SORT folder | Loose images in the root | Total |
|---|---:|---:|---:|
| Files looked at | 971 | 2426 | 3397 |
| `move` | 716 | 1537 | 2253 |
| `variant` | 3 | 29 | 32 |
| `check` | 75 | 280 | 355 |
| `duplicate_larger` | 16 | 63 | 79 |
| `duplicate_exact` | 61 | 194 | 255 |
| `duplicate_smaller` | 59 | 189 | 248 |
| `unsure` | 36 | 99 | 135 |
| `leave` | 5 | 35 | 40 |

The TO SORT folder holds 951 files at the top level plus 20 in its `Rappers` subfolder (971 in all).

### What the actions mean

- **move**: a new person (or a new numbered version) for the clean set. Move to `destination_path`.
- **variant**: the person is already in the 2026 folders, but this file has a different number ("Name 2", "Name3"). Owner's rule: a number always means a different image, so keep both and move it.
- **check**: same name and number as a file already in the 2026 folders, but one of the two names carries a Dropbox/Windows copy marker such as `(2)`, `- Copy` or a year such as `2021`. Those are not version numbers, so this is **not** counted as a duplicate. The reason column gives both sizes (and says when they are byte-identical). Owner to look before anything moves.
- **duplicate_larger**: same name and number as an existing file, and this file is **larger**. Plan: move it in beside the old one as `<name> (larger).jpg` (never overwrite), then the owner retires the smaller one.
- **duplicate_exact**: same name and number and the same size in bytes as a file already in the set. Leave it where it is.
- **duplicate_smaller**: same name and number, but the copy already in the set is larger. Leave this one where it is; flagged so nothing replaces the better file.
- **unsure**: person or category not clear from the file name (bare first names, random camera/agency names) or a sensitive subject. Not moved.
- **leave**: not a face image (PDF, InDesign, PSD, `.DS_Store`, product mockups, header graphics). Not moved.

Duplicates are matched on the normalised name **and** number (e.g. `Mark Owen 2.jpg` = `mark owen 2 MH.jpg`; `Mark Owen.jpg` is a different image from `Mark Owen 2.jpg`). Suffixes MH, JB, CPDVD, MINT, Onbuy ver, Face, Mask, `_`, `-` and agency numbers are ignored; the part after ` - ` (club, show, sport) is ignored for matching. Sizes are compared in bytes from the Dropbox listing, not by pixels.

## Where the files would go (move + variant + check + duplicate_larger)

| Destination folder | From TO SORT | From the root | Total | Folder exists? |
|---|---:|---:|---:|---|
| 2026 TV SHOWS AND STARS | 231 | 447 | 678 | yes |
| 2026 MOVIE STARS | 77 | 300 | 377 | yes |
| 2026 FOOTBALLERS | 105 | 212 | 317 | yes |
| 2026 MUSIC | 108 | 189 | 297 | yes |
| 2026 COMEDIANS 2019 | 55 | 89 | 144 | yes |
| 2026 ROYALS AND POLITICIANS | 36 | 104 | 140 | yes |
| 2026 SPORTS STARS/Golf | 24 | 71 | 95 | yes |
| 2026 CELEBRITY KIDS CARTOON | 27 | 42 | 69 | yes |
| WAG MODEL | 6 | 42 | 48 | yes |
| 2026 BUSINESS AND PUBLIC FIGURES | 17 | 29 | 46 | **new** |
| 2026 DARTS | 7 | 38 | 45 | yes |
| 2026 SPORTS STARS/RUGBY 2019 | 18 | 20 | 38 | yes |
| 2026 F1 DRIVER | 9 | 21 | 30 | yes |
| 2026 TV SHOWS AND STARS/2026 Emmerdale | 4 | 25 | 29 | yes |
| 2026 SPORTS STARS/Tennis | 3 | 25 | 28 | yes |
| 2026 BOLLYWOOD ACTORS | 13 | 13 | 26 | yes |
| 2026 CRICKET | 1 | 22 | 23 | yes |
| 2026 TV SHOWS AND STARS/2026 CORONATION STREET | 0 | 22 | 22 | yes |
| 2026 NOVELTY, ANIMALS AND EMOJIS | 4 | 17 | 21 | **new** |
| 2026 MOVIE STARS/Harry Potter | 6 | 13 | 19 | yes |
| 2026 SPORTS STARS/Olympic Athletes | 9 | 10 | 19 | yes |
| 2026 TV SHOWS AND STARS/Hollyoaks | 4 | 14 | 18 | yes |
| 2026 TV SHOWS AND STARS/Strictly Come Dancing | 4 | 13 | 17 | yes |
| 2026 TV SHOWS AND STARS/TOWIE | 4 | 13 | 17 | yes |
| 2026 BOXERS | 1 | 13 | 14 | yes |
| 2026 SPORTS STARS/Snooker | 3 | 11 | 14 | **new** |
| 2026 TV SHOWS AND STARS/2026 Eastenders | 1 | 13 | 14 | yes |
| 2026 SPORTS STARS/Cycling | 5 | 6 | 11 | yes |
| 2026 YOUTUBERS AND INFLUENCERS | 2 | 9 | 11 | **new** |
| 2026 SPORTS STARS/Motorbike Racing | 1 | 9 | 10 | **new** |
| 2026 SPORTS STARS/Wrestling | 6 | 4 | 10 | **new** |
| 2026 SPORTS STARS/Basketball | 3 | 6 | 9 | yes |
| 2026 ATHLETES | 1 | 7 | 8 | yes |
| 2026 TV SHOWS AND STARS/LOVE ISLAND | 1 | 7 | 8 | yes |
| 2026 SPORTS STARS/MMA | 1 | 6 | 7 | yes |
| 2026 SPORTS STARS/Misc Sports | 5 | 2 | 7 | yes |
| 2026 TV SHOWS AND STARS/2026 BENIDORM | 1 | 5 | 6 | yes |
| 2026 TV SHOWS AND STARS/GEORDIE SHORE | 1 | 4 | 5 | yes |
| 2026 TV SHOWS AND STARS/STRANGER THINGS | 2 | 2 | 4 | yes |
| !!MASK PACK MOCKUP IMAGES | 1 | 2 | 3 | yes |
| 2026 TV SHOWS AND STARS/Friends | 0 | 3 | 3 | yes |
| 2026 TV SHOWS AND STARS/still game | 1 | 2 | 3 | yes |
| 2026 MOVIE STARS/Spider man | 1 | 1 | 2 | yes |
| 2026 TV SHOWS AND STARS/GAVIN STACEY | 1 | 1 | 2 | yes |
| 2026 MOVIE STARS/Mamma Mia | 0 | 1 | 1 | yes |
| 2026 MOVIE STARS/Saw | 0 | 1 | 1 | yes |
| 2026 TV SHOWS AND STARS/IM A CELEB | 0 | 1 | 1 | yes |
| 2026 TV SHOWS AND STARS/Ru Pauls Drag Race | 0 | 1 | 1 | yes |
| 2026 TV SHOWS AND STARS/The Boys Tv | 0 | 1 | 1 | yes |

## Duplicates

- `duplicate_exact`: 255
- `duplicate_smaller`: 248
- `duplicate_larger`: 79
- `check`: 355

Full detail (which file each one matches, both sizes) is in `plan.csv` (`match_path`, `match_size`, `reason`).

## Unsure (135) and best guesses

| File | Where | Best guess / why |
|---|---|---|
| 114392 BILL.jpg | root (loose) | Bill: name too vague to identify (bare first name or unidentified: 'Celebrity face mask'); may be a customer's personalised mask, open the image to check |
| cdd48c7e-2b32-4145-bfc7-97f6cc01af77.png | root (loose) | Unidentified: name too vague to identify (bare first name or unidentified: 'Unidentified celebrity face'); may be a customer's personalised mask, open the image to check |
| Charlie-Rundle.jpg | root (loose) | Charlie Rundle: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| da1dbb10-b4fb-41e4-b673-e01787f720f1.png | root (loose) | Unidentified: name too vague to identify (bare first name or unidentified: 'Unidentified celebrity face'); may be a customer's personalised mask, open the image to check |
| david love.jpg | root (loose) | David Love: name too vague to identify (bare first name or unidentified: 'Celebrity face'); may be a customer's personalised mask, open the image to check |
| e62ace54-9b20-46eb-af36-1a6b16ca0364.jpg | root (loose) | Unidentified celebrity: name too vague to identify (bare first name or unidentified: 'Celebrity face'); may be a customer's personalised mask, open the image to check |
| ed gein.jpg | root (loose) | Ed Gein: SENSITIVE (American murderer): owner to decide whether this mask is still wanted; see ../face-masks/removed-sensitive-masks.csv |
| f3e04dfb-4df8-4b2b-afcb-682cf48cbf81.png | root (loose) | Unidentified celebrity: name too vague to identify (bare first name or unidentified: 'Celebrity face'); may be a customer's personalised mask, open the image to check |
| Fergie.jpg | root (loose) | Fergie: name too vague to identify (bare first name or unidentified: 'Ambiguous nickname'); may be a customer's personalised mask, open the image to check |
| forum MH.jpg | root (loose) | Forum: name too vague to identify (bare first name or unidentified: 'Unclear artwork'); may be a customer's personalised mask, open the image to check |
| Freddie Goodwin.jpg | root (loose) | Freddie Goodwin: name too vague to identify (bare first name or unidentified: 'Celebrity face'); may be a customer's personalised mask, open the image to check |
| Gallagher.jpg | root (loose) | Gallagher: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| gary johnson.jpg | root (loose) | Gary Johnson: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| Georgia.jpg | root (loose) | Georgia: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| gerson bergher .jpg | root (loose) | Gerson Bergher: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| gerson-bergher-.jpg | root (loose) | Gerson Bergher: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| Gustappo.jpg | root (loose) | Gustappo: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| guy mask.jpeg | root (loose) | Guy: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| HALEY ROBERTS.jpg | root (loose) | Haley Roberts: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| harriet mask.jpg | root (loose) | Harriet: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| harry best.jpg | root (loose) | Harry Best: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| henry.jpg | root (loose) | Henry: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| IMG_2005.JPG | root (loose) | Unidentified Celebrity: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| Jacqui Holland.jpg | root (loose) | Jacqui Holland: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| James Folder - G8.jpg | root (loose) | James: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| James Hiller.jpg | root (loose) | James Hiller: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| Jamie Hamilton.jpg | root (loose) | Jamie Hamilton: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| Jamie Maguire.jpg | root (loose) | Jamie Maguire: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| Jamie.jpg | root (loose) | Jamie: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| jeffrey dahmer.jpg | root (loose) | Jeffrey Dahmer: SENSITIVE (Notorious American criminal): owner to decide whether this mask is still wanted; see ../face-masks/removed-sensitive-masks.csv |
| Jeffrey Epstein.jpg | root (loose) | Jeffrey Epstein: SENSITIVE (American financier and convicted offender): owner to decide whether this mask is still wanted; see ../face-masks/removed-sensitive-masks.csv |
| jenny mask.jpg | root (loose) | Jenny: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| jerry ledbetter_2.jpg | root (loose) | Jerry Ledbetter: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| JESSE.jpg | root (loose) | Jesse: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| Jimmy storrar.jpg | root (loose) | Jimmy Storrar: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| Joanne Lamont.jpg | root (loose) | Joanne Lamont: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| John MacMillan.jpg | root (loose) | John MacMillan: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| Johnny.jpg | root (loose) | Johnny: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| jonathan aintone.jpg | root (loose) | Jonathan Aintone: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| Jonathan Wrather.jpg | root (loose) | Jonathan Wrather: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| Jonathan Wrather2.jpg | root (loose) | Jonathan Wrather: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| Jonny Russel (2).jpg | root (loose) | Jonny Russell: name too vague to identify (bare first name or unidentified: 'Sports personality'); may be a customer's personalised mask, open the image to check |
| Jonny Russel.jpg | root (loose) | Jonny Russell: name too vague to identify (bare first name or unidentified: 'Sports personality'); may be a customer's personalised mask, open the image to check |
| Jordan-Mas-2.jpg | root (loose) | Jordan Mas: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| Joseph Fritzel - Crazy Mask.jpg | root (loose) | Josef Fritzl: SENSITIVE (Austrian criminal): owner to decide whether this mask is still wanted; see ../face-masks/removed-sensitive-masks.csv |
| Joseph-Fritzel--Crazy-Mask.jpg | root (loose) | Josef Fritzl: SENSITIVE (Austrian criminal): owner to decide whether this mask is still wanted; see ../face-masks/removed-sensitive-masks.csv |
| Julie Lake.jpg | root (loose) | Julie Lake: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| justice MH.jpg | root (loose) | Justice: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| karen Maguire.jpg | root (loose) | Karen Maguire: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| KAREN PHIL.png | root (loose) | Karen Phil: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| KasandrA Kahler.jpg | root (loose) | Kasandra Kahler: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| Kath - Jayne Taylor (2).jpg | root (loose) | Kath: name too vague to identify (bare first name or unidentified: 'Well-known personality'); may be a customer's personalised mask, open the image to check |
| KEN WRIGHT.jpg | root (loose) | Ken Wright: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| kessler1.jpg | root (loose) | Kessler: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Kevin Neylon.jpg | root (loose) | Kevin Neylon: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Kevin-NeylonPROOF.jpg | root (loose) | Kevin Neylon: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| KINGSLEY.jpg | root (loose) | Kingsley: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| KIP.jpg | root (loose) | Kip: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Kshatriya Ari.jpg | root (loose) | Kshatriya Ari: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Lee Johnson.jpg | root (loose) | Lee Johnson: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Lindsay Stoppard JB.jpg | TO SORT | Lindsay Stoppard: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Lovely Jaime MH.jpg | root (loose) | Jaime: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Lugano.jpg | root (loose) | Lugano: name too vague to identify (bare first name or unidentified: 'Unidentified design'); may be a customer's personalised mask, open the image to check |
| Luke Chilton.jpg | root (loose) | Luke Chilton: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Luke.JPG | root (loose) | Luke: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Maori.JPG | root (loose) | Māori Face: SENSITIVE (Māori-themed face design): owner to decide whether this mask is still wanted; see ../face-masks/removed-sensitive-masks.csv |
| Marcel.jpg | root (loose) | Marcel: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Mark Dowlan.jpg | root (loose) | Mark Dowlan: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| masanori kobayashi.jpg | root (loose) | Masanori Kobayashi: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| Mathilda Belladonna.jpg | root (loose) | Mathilda Belladonna: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| maxresdefault.jpg | root (loose) | Unknown: name too vague to identify (bare first name or unidentified: 'Unidentified face'); may be a customer's personalised mask, open the image to check |
| mcgregor.jpg | root (loose) | McGregor: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| MIA.jpg | root (loose) | Mia: bare first name; open the image |
| MICHELLE.jpg | root (loose) | Michelle: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| mickey gooch.jpg | root (loose) | Mickey Gooch: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| mickey-gooch.jpg | root (loose) | Mickey Gooch: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| Miguel Fiance.jpg | root (loose) | Miguel: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| mike.jpg | root (loose) | Mike: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| Miranda MH.jpg | root (loose) | Miranda: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| MIS2-0251.jpg | root (loose) | Unknown: name too vague to identify (bare first name or unidentified: 'Unidentified face'); may be a customer's personalised mask, open the image to check |
| MIS2-0531.jpg | root (loose) | Unknown: name too vague to identify (bare first name or unidentified: 'Unidentified face'); may be a customer's personalised mask, open the image to check |
| MIS2-0611.jpg | root (loose) | Unknown: name too vague to identify (bare first name or unidentified: 'Unidentified face'); may be a customer's personalised mask, open the image to check |
| MIS2-0896.jpg | root (loose) | Unknown: name too vague to identify (bare first name or unidentified: 'Unidentified face'); may be a customer's personalised mask, open the image to check |
| Montana.jpg | root (loose) | Montana: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| Moya.jpg | root (loose) | Moya: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| Muriel2.jpg | root (loose) | Muriel: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| NEXT DAYER.jpg | root (loose) | Unknown: name too vague to identify (bare first name or unidentified: 'Unidentified face'); may be a customer's personalised mask, open the image to check |
| nicola king.jpg | root (loose) | Nicola King: name too vague to identify (bare first name or unidentified: 'Public figure'); may be a customer's personalised mask, open the image to check |
| Ollie.jpg | root (loose) | Ollie: name too vague to identify (bare first name or unidentified: 'TV personality'); may be a customer's personalised mask, open the image to check |
| Osama Bin Laden.jpg | root (loose) | Osama bin Laden: SENSITIVE (Founder of the terrorist group al-Qaeda): owner to decide whether this mask is still wanted; see ../face-masks/removed-sensitive-masks.csv |
| osama-bin-laden-mask-ZOOM.jpg | root (loose) | Osama bin Laden: SENSITIVE (Founder of the terrorist group al-Qaeda): owner to decide whether this mask is still wanted; see ../face-masks/removed-sensitive-masks.csv |
| paul 1.jpg | root (loose) | Paul: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| Pauli Gualitire.jpg | root (loose) | Pauli Gualitire: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| philomena.JPG | root (loose) | Philomena: could be Philomena Cunk (Diane Morgan) or Philomena Lee; open the image |
| Project Dawn1.jpg | root (loose) | Project Dawn: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| rachel (2).jpg | root (loose) | Rachel: name too vague to identify (bare first name or unidentified: 'TV personality'); may be a customer's personalised mask, open the image to check |
| Rachel Roberts.jpg | TO SORT | Rachel Roberts: name too vague to identify (bare first name or unidentified: 'Actress'); may be a customer's personalised mask, open the image to check |
| rafa cabello.jpg | TO SORT | Rafa Cabello: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| rebecca ferguson long hair.jpg | TO SORT | Rebecca Ferguson: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| rebecca ferguson.jpg | TO SORT | Rebecca Ferguson: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| Reggie Kray - Legend.jpg | root (loose) | Reggie Kray: SENSITIVE (London gangster of the 1960s): owner to decide whether this mask is still wanted; see ../face-masks/removed-sensitive-masks.csv |
| robbie lawson.jpg | TO SORT | Robbie Lawson: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| Robert Lonsdale.jpg | TO SORT | Robert Lonsdale: name too vague to identify (bare first name or unidentified: 'Actor'); may be a customer's personalised mask, open the image to check |
| Ronnie Kray.jpg | root (loose) | Ronnie Kray: SENSITIVE (1960s London gangster and twin of Reggie Kray): owner to decide whether this mask is still wanted; see ../face-masks/removed-sensitive-masks.csv |
| Ross Holding.jpg | TO SORT | Ross Holding: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| rupert jones.jpg | TO SORT | Rupert Jones: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Ryan Hall.jpg | TO SORT | Ryan Hall: name too vague to identify (bare first name or unidentified: 'Sports personality'); may be a customer's personalised mask, open the image to check |
| Sam Bottomley.jpg | TO SORT | Sam Bottomley: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| sam-bentham.jpg | TO SORT | Sam Bentham: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| sandy sinatra.jpg | TO SORT | Sandy Sinatra: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| SARAH DAYS.jpg | TO SORT | Sarah Days: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Sarah Goodhart (2).jpg | TO SORT | Sarah Goodhart: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Sarah Goodhart.jpg | TO SORT | Sarah Goodhart: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Sarah Hoare.jpg | TO SORT | Sarah Hoare: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Sarah O Brian.jpg | TO SORT | Sarah O'Brien: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Scott Bench Taylor.jpg | TO SORT | Scott Bench-Taylor: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Shane Maguire.jpg | TO SORT | Shane Maguire: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| shayne byrne.jpg | TO SORT | Shayne Byrne: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Simon Cass.jpg | TO SORT | Simon Cass: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| sophie replace.jpg | TO SORT | Sophie: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Stephen jones.jpg | TO SORT | Stephen Jones: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| steve jones.jpg | TO SORT | Steve Jones: name too vague to identify (bare first name or unidentified: 'Personality'); may be a customer's personalised mask, open the image to check |
| Stuart Kellet.JPG | TO SORT | Stuart Kellet: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| Style+Stroke+Launch+Event+Arrivals+8gDKVfLj7Akl.jpg | TO SORT | press-agency photo name; open it to see who it is |
| the REAL Randy-Chavez-.jpg | root (loose) | Randy Chavez: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| thomas atkinson lachlan white.jpg | TO SORT | Thomas Atkinson: name too vague to identify (bare first name or unidentified: 'Actor'); may be a customer's personalised mask, open the image to check |
| TOM FELL.jpg | TO SORT | Tom Fell: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| tommy x 20.jpg | TO SORT | Tommy: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| TP.jpg | TO SORT | TP: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| tumblr vomiGk MH.jpg | TO SORT | Unknown: name too vague to identify (bare first name or unidentified: 'Unidentified face mask'); may be a customer's personalised mask, open the image to check |
| tw5wF8ZvUqJyE9Qtsiqhvk.jpg | root (loose) | Unknown: name too vague to identify (bare first name or unidentified: 'Unidentified face mask'); may be a customer's personalised mask, open the image to check |
| wenn23074779_46_5014_10.jpg | TO SORT | Unknown: name too vague to identify (bare first name or unidentified: 'Unidentified face mask'); may be a customer's personalised mask, open the image to check |
| Whirter (2).jpg | TO SORT | Whirter: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| ye yang.jpg | TO SORT | Ye Yang: name too vague to identify (bare first name or unidentified: 'Celebrity'); may be a customer's personalised mask, open the image to check |
| Your Face.jpg | TO SORT | Unknown: name too vague to identify (bare first name or unidentified: 'Unidentified face mask'); may be a customer's personalised mask, open the image to check |

## Not face images (left where they are): 40

- _SKU_COUNTER_00010.txt (root (loose)): not a face image (.txt); leave where it is
- adrien truffert.pdf (root (loose)): not a face image (.pdf); leave where it is
- alex jimenez.pdf (root (loose)): not a face image (.pdf); leave where it is
- ANGRY GINGE FACE MASK.pdf (root (loose)): not a face image (.pdf); leave where it is
- Anxious Emoji.pdf (root (loose)): not a face image (.pdf); leave where it is
- Cat Emoji.pdf (root (loose)): not a face image (.pdf); leave where it is
- DAVE-SWIFT-LAMBRETTA-2_Hoody-and-Jacket-Front-BLACK.jpg (root (loose)): Lambretta clothing artwork, not a face mask
- DAVE-SWIFT-LAMBRETTA-2_RED-WORKWEAR-BUNDLE.jpg (root (loose)): Lambretta clothing artwork, not a face mask
- DAVE_SWIFT_LAMBRETTA_2_Mask_Mockup.jpg (root (loose)): Lambretta product mockup, not a face mask
- DAVE_SWIFT_LAMBRETTA_2_Snood_Mockup.jpg (root (loose)): Lambretta snood product mockup, not a face mask
- DepthChargeDesign Facemasks.jpg (root (loose)): company branding image, not a face mask
- DepthChargeDesign Facemasks.psd (root (loose)): not a face image (.psd); leave where it is
- Donald and Hillary SRA3 Print Grid.indd (root (loose)): not a face image (.indd); leave where it is
- FRIDAY 10.6.22.pdf (root (loose)): not a face image (.pdf); leave where it is
- Half-prince-william_tmp20460 (root (loose)): not a face image (no extension); leave where it is
- HONEY G MH.pdf (root (loose)): not a face image (.pdf); leave where it is
- Jack-duckworth_tmp2272 (root (loose)): not a face image (no extension); leave where it is
- Jane-horrocks_tmp20059 (root (loose)): not a face image (no extension); leave where it is
- john virgo.pdf (root (loose)): not a face image (.pdf); leave where it is
- Joseph-Fritzel--Crazy-Mask_tmp4770 (root (loose)): not a face image (no extension); leave where it is
- KIOSK KATH.pdf (root (loose)): not a face image (.pdf); leave where it is
- Kyle Sinckler + eddie jones.pdf (root (loose)): not a face image (.pdf); leave where it is
- laugh cry emoji.pdf (root (loose)): not a face image (.pdf); leave where it is
- love emoji.pdf (root (loose)): not a face image (.pdf); leave where it is
- luke donald 2.pdf (root (loose)): not a face image (.pdf); leave where it is
- Lydias-towie_tmp7234 (root (loose)): not a face image (no extension); leave where it is
- MACAULEY CULKIIN.pdf (root (loose)): not a face image (.pdf); leave where it is
- MIKE SKINNER .pdf (root (loose)): not a face image (.pdf); leave where it is
- money.pdf (root (loose)): not a face image (.pdf); leave where it is
- OLYMPIC MASKS.psd (root (loose)): not a face image (.psd); leave where it is
- PIDGEON LADY .pdf (root (loose)): not a face image (.pdf); leave where it is
- poo emoji.pdf (root (loose)): not a face image (.pdf); leave where it is
- ryder cup pack 2.indd (root (loose)): not a face image (.indd); leave where it is
- staghen-header.gif (root (loose)): website header graphic
- star wars masks.indd (root (loose)): not a face image (.indd); leave where it is
- tony benn .pdf (TO SORT): not a face image (.pdf); leave where it is
- towie CAST.indd (TO SORT): not a face image (.indd); leave where it is
- Ving Rhames CUT.pdf (TO SORT): not a face image (.pdf); leave where it is
- wink emoji.pdf (TO SORT): not a face image (.pdf); leave where it is
- WOOD.svg (TO SORT): not a face image (.svg); leave where it is

## How the people and categories were worked out

1. Each file name is normalised (`tools/norm.py`) and matched to the person list built on 2 Oct 2026 (`../face-masks/dropbox-masks-master-list.csv`, 6,980 people with category, sport and show). 97% of the files matched.
2. The rest, and the people that list had filed as "other", were decided by hand in `tools/overrides.py` (e.g. `Linda - Gimmie Gimmie` = Kathy Burke, TV; `S Roberta - Barca` = Sergi Roberto, footballer; YouTubers, business people, novelty masks).
3. Category to folder: TV and reality to `2026 TV SHOWS AND STARS` (into the show's own subfolder where one already exists, e.g. Coronation Street, Emmerdale, Hollyoaks, TOWIE, Love Island); film to `2026 MOVIE STARS` (Harry Potter etc. into their subfolders); Indian film stars to `2026 BOLLYWOOD ACTORS`; sports by sport (see `proposed-folders.md`).
4. Then `tools/build_plan.py` checks every file against everything already in the 2026 folders and `WAG MODEL`, and against the other source files, and makes sure no destination name is used twice.

## Next steps (phase 2, needs the owner's go-ahead)

1. Owner reviews `plan.csv`, especially `check`, `duplicate_larger`, `unsure` and the new folders.
2. Create only the approved new folders, then move the approved `move`/`variant` rows in small batches with `mcp__Dropbox__move` (never `autorename` over an existing file, never delete), re-listing each destination after every batch.
3. Duplicates stay where they are until the owner says what to do with them; nothing is trashed.
