"""Copy for the 53 "DCD Terrace Flags" products (launch 6 Oct 2026).

Facts come only from plan/product-facts.md ("Stadium / terrace flags"): 115gsm knitted
polyester, digitally printed in the UK and hand-stitched, 25mm edge binding, eyelets on
all 4 edges, single-sided (double-sided on request, quote), fire label on every flag
(certificate on request), indoor and outdoor use, any wording, FREE UK delivery,
3 sizes 3ft x 2ft / 5ft x 3ft / 8ft x 5ft. No dispatch times, no wash care.

Run: python3 tools/terrace_flags_copy.py  -> writes exports/terrace-flags/listings.json
"""
import json, re, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'exports', 'terrace-flags', 'listings.json')

# ---------------------------------------------------------------------------
# Per-product data. code = old SKU uppercased without FOXY-FLAG- prefix.
# kind: country | club | england (football, national team)
# ---------------------------------------------------------------------------
P = []

def add(**k):
    P.append(k)

# ----------------------------- COUNTRY FLAGS ------------------------------
add(code='CFLAG01', pid='8783846637819', kind='country', name='China', color='Red',
    title='Personalised China Terrace Flag – Red Chinese Flag with Yellow Stars – 3 Sizes',
    seo_title='Personalised China Terrace Flag | Foxy Printing',
    seo_desc='A red Chinese flag with yellow stars and your own wording printed on it. Pick 3ft x 2ft, 5ft x 3ft or 8ft x 5ft, with free UK delivery on every flag.',
    kw='personalised China terrace flag',
    intro='Our personalised China terrace flag puts the bright red flag and its five yellow stars together with your own words, so the people you’re cheering for know exactly who’s behind them. It’s a proud pick for Chinese New Year parties, international tournaments and family celebrations.',
    h2='A personalised China terrace flag with your name on it',
    personal='Type the wording you want in the box above, whether that’s a family name, a hometown or a short slogan, and add a second line if you need one. You can upload a logo too. The live preview shows your details next to the flag photo, and anything else you’d like, just tell us in the message box.',
    close='Ordering for a group? A big 8ft x 5ft Chinese flag is easy for everyone to spot across a crowd.')

add(code='CFLAG02', pid='8783850930427', kind='country', name='England', color='White',
    title='Personalised England Terrace Flag – St George Cross Football Fan Flag – 3 Sizes',
    seo_title='Personalised England St George Flag | Foxy Printing',
    seo_desc='Fly the red cross of St George with your name, pub or town printed across it. Three sizes up to 8ft x 5ft, eyelets on every edge and free UK delivery.',
    kw='personalised England terrace flag',
    intro='This personalised England terrace flag is the classic red St George cross on white, with your own wording printed right across it. Hang it in the stand, the beer garden or the front window when the big tournaments come round.',
    h2='Personalised England terrace flag – St George cross with your words',
    personal='Tell us the text for the flag, maybe your town, your local or the names of the lads travelling together, and there’s an optional second line. Got a logo for your group? Upload it. The live preview pops your details up beside the flag photo before you order.',
    close='Watching with friends? A 5ft x 3ft St George flag fills a pub wall nicely.')

add(code='CFLAG03', pid='8783853125883', kind='country', name='India', color='Multicolor',
    title='Personalised India Terrace Flag – Indian Tricolour Sports Fan Flag – 3 Sizes',
    seo_title='Personalised India Tricolour Fan Flag | Foxy Printing',
    seo_desc='Saffron, white and green with the wheel at its centre, plus your words. A personalised Indian flag for cricket and celebrations, delivered free in the UK.',
    kw='personalised India terrace flag',
    intro='Cheer on your team with a personalised India terrace flag: the saffron, white and green tricolour with the navy wheel at its heart, printed with the wording you choose. It’s made for cricket days, Diwali and Independence Day get-togethers, and weddings where the family wants to be seen.',
    h2='Your personalised India terrace flag, printed with your wording',
    personal='Add a family name, a city, a cricket club or a cheeky line for the boundary rope, with a second line if you want one. You can upload a logo, and the live preview shows what you’ve typed next to the flag photo. Use the message box for anything else.',
    close='A personalised Indian flag also makes a thoughtful gift for a relative heading to a big match.')

add(code='CFLAG04', pid='8783854829819', kind='country', name='Scotland', color='Blue',
    title='Personalised Scotland Terrace Flag – Saltire Football Fan Flag – 3 Sizes',
    seo_title='Personalised Scotland Saltire Flag | Foxy Printing',
    seo_desc='The white saltire on blue, printed with your clan, town or group name. A personalised Scottish flag in 3 sizes up to 8ft x 5ft, with free UK delivery.',
    kw='personalised Scotland terrace flag',
    intro='Take the Saltire on the road with a personalised Scotland terrace flag: the white cross on blue, printed with your own words. It’s a proper sight at away trips, rugby weekends and Burns Night parties alike.',
    h2='A personalised Scotland terrace flag for the Tartan faithful',
    personal='Pop in your clan name, home town or the name of your travelling crew, plus a second line if you like. You can upload a logo too. The live preview shows your wording beside the flag photo, and the message box is there for anything else.',
    close='Off to watch the game abroad? A 3ft x 2ft Scottish flag folds small enough for a rucksack.')

add(code='CFLAG06', pid='8783857418491', kind='country', name='Italy', color='Multicolor',
    title='Personalised Italy Terrace Flag – Italian Tricolore Football Fan Flag – 3 Sizes',
    seo_title='Personalised Italy Tricolore Flag | Foxy Printing',
    seo_desc='Green, white and red with your family name or town printed on it. A personalised Italian flag for match days and parties, 3 sizes, free UK delivery.',
    kw='personalised Italy terrace flag',
    intro='Our personalised Italy terrace flag keeps the green, white and red tricolore bold and simple, then adds the words you want on it. Perfect for watching Italy with the family, for a nonna’s birthday or for an Italian-themed party.',
    h2='Personalised Italy terrace flag in classic green, white and red',
    personal='Add a family surname, the town your grandparents came from or a short slogan, and use the second line if it needs more room. Upload a logo if you have one. The live preview shows your details alongside the flag photo before you buy.',
    close='A personalised Italian flag looks just as good in a restaurant or deli as it does at the match.')

add(code='CFLAG07', pid='8783860203771', kind='country', name='South Africa', color='Multicolor',
    title='Personalised South Africa Terrace Flag – Rugby & Sports Fan Flag – 3 Sizes',
    seo_title='Personalised South Africa Fan Flag | Foxy Printing',
    seo_desc='The six-colour South African flag with your own wording printed on it. Great for rugby and cricket days, in 3 sizes up to 8ft x 5ft and free UK delivery.',
    kw='personalised South Africa terrace flag',
    intro='Whether it’s a rugby test, a cricket series or a braai with friends, a personalised South Africa terrace flag lets you show where your heart is. It carries the full six-colour flag with your own words printed on it.',
    h2='A personalised South Africa terrace flag in all six colours',
    personal='Type the name of your family, your home town back in SA or your supporters’ group, with an optional second line. Upload a logo if you’d like one included. The live preview puts your wording next to the flag photo, and the message box takes any extra notes.',
    close='For a big group in the stand, go for the 8ft x 5ft size so the whole crowd can see it.')

add(code='CFLAG08', pid='8783862628603', kind='country', name='South Korea', color='White',
    title='Personalised South Korea Terrace Flag – Korean Football Fan Flag – 3 Sizes',
    seo_title='Personalised South Korea Fan Flag | Foxy Printing',
    seo_desc='The white Korean flag with its red and blue circle and black trigrams, printed with your words. Three sizes, eyelets on all 4 edges and free UK delivery.',
    kw='personalised South Korea terrace flag',
    intro='A personalised South Korea terrace flag is a great way to back your team: the white flag with its red and blue circle and four black trigrams, printed with your own message. Bring it to a watch party, a K-pop concert or a Korean community event.',
    h2='Personalised South Korea terrace flag with your own message',
    personal='Add a name, a group, a city or a short cheer in the first box, with a second line if you need one. You can also upload a logo. The live preview shows your text beside the flag photo, and the message box is for anything we should know.',
    close='Supporting with friends? Order a matching 3ft x 2ft Korean flag each.')

add(code='CFLAG09', pid='8783866003707', kind='country', name='Spain', color='Red',
    title='Personalised Spain Terrace Flag – Spanish Football Fan Flag – 3 Sizes',
    seo_title='Personalised Spain Flag with Your Name | Foxy Printing',
    seo_desc='Red and yellow Spanish flag printed with your own words, from a family name to a town. A personalised flag in 3 sizes, eyelets all round, free UK delivery.',
    kw='personalised Spain terrace flag',
    intro='Red, yellow, red: a personalised Spain terrace flag is about as cheerful as a flag gets, and this one carries the words you choose. Wave it on match night, hang it at a fiesta-themed party or bring a bit of holiday sunshine to the garden.',
    h2='A personalised Spain terrace flag in bold red and yellow',
    personal='Write the name of your family, your peña or your favourite Spanish town, plus a second line if you want. Upload a logo if there is one. The live preview shows your details next to the flag photo before you check out.',
    close='A personalised Spanish flag makes a fun gift for anyone with a place in the sun.')

add(code='CFLAG10', pid='8783868985595', kind='country', name='Turkey', color='Red',
    title='Personalised Turkey Terrace Flag – Turkish Football Fan Flag – 3 Sizes',
    seo_title='Personalised Turkey Flag for Fans | Foxy Printing',
    seo_desc='The red Turkish flag with its white crescent and star, printed with your words. A personalised fan flag in 3 sizes up to 8ft x 5ft, free UK delivery.',
    kw='personalised Turkey terrace flag',
    intro='The white crescent and star on red looks striking from any distance, and our personalised Turkey terrace flag adds your own words to it. It’s ideal for match nights, community events, family celebrations and the restaurant wall.',
    h2='Personalised Turkey terrace flag – crescent and star with your words',
    personal='Fill in a family name, a city, a business or a supporters’ group, and use the second line if needed. You can upload a logo too. The live preview shows your wording beside the flag photo, and you can leave us a note in the message box.',
    close='For a shop or restaurant, a 5ft x 3ft Turkish flag with your business name makes a smart display.')

add(code='CFLAG11', pid='8783871803643', kind='country', name='Ukraine', color='Blue/Yellow',
    title='Personalised Ukraine Terrace Flag – Blue & Yellow Ukrainian Flag – 3 Sizes',
    seo_title='Personalised Ukraine Flag Blue & Yellow | Foxy Printing',
    seo_desc='The blue and yellow Ukrainian flag with your own words printed on it. Choose 3ft x 2ft, 5ft x 3ft or 8ft x 5ft, eyelets on all 4 edges, free UK delivery.',
    kw='personalised Ukraine terrace flag',
    intro='Two simple bands, blue sky over yellow fields: a personalised Ukraine terrace flag carries a lot of meaning, and with your own wording it becomes yours. Show support at a match, a community fundraiser or a family gathering.',
    h2='A personalised Ukraine terrace flag in blue and yellow',
    personal='Add a town, a family name, a community group or a short message of support, plus a second line if needed. Upload a logo for your group if you have one. The live preview shows your wording next to the flag photo before you buy.',
    close='Running a fundraiser? A large Ukrainian flag with your group’s name makes a great backdrop.')

add(code='CFLAG12', pid='8783874949371', kind='country', name='Union Jack', color='Multicolor',
    title='Personalised Union Jack Terrace Flag – Great Britain Fan Flag – 3 Sizes',
    seo_title='Personalised Union Jack Terrace Flag | Foxy Printing',
    seo_desc='A Union Jack printed with your name, town or team. Ideal for sporting summers, street parties and away trips, in 3 sizes up to 8ft x 5ft, free UK delivery.',
    kw='personalised Union Jack terrace flag',
    intro='Nothing says Great Britain quite like the red, white and blue, and our personalised Union Jack terrace flag adds your own words to it. Fly it for a big sporting summer, a royal celebration, a street party or a sports trip abroad.',
    h2='Personalised Union Jack terrace flag with your own wording',
    personal='Choose the words for the flag, perhaps your street, your family or your club, with an optional second line. Upload a logo if you want one on it. The live preview shows your details beside the flag photo, and the message box takes any extra notes.',
    close='Planning a street party? Pair this Great Britain flag with a second design so both ends of the road match.')

add(code='CFLAG13', pid='8783877701883', kind='country', name='Union Jack', color='Multicolor', design2=True,
    title='Personalised Union Jack Terrace Flag – Great Britain Fan Flag Design 2 – 3 Sizes',
    seo_title='Union Jack Flag with Your Name, Design 2 | Foxy Printing',
    seo_desc='Our second personalised Union Jack design, printed with the words you choose. Three sizes, eyelets on all four edges and free UK delivery on every flag.',
    kw='personalised Union Jack flag',
    intro='Here’s a second take on our personalised Union Jack flag, giving you another layout for your wording on the red, white and blue. It’s a good choice if you’re ordering two flags and want them to look a little different.',
    h2='Personalised Union Jack flag, design 2',
    personal='Type in your text, a name, a place or a team, and add a second line if you need it. A logo upload is there if you want one. The live preview shows your wording next to the flag photo so you can compare it with our first Union Jack design.',
    close='Ordering for a group trip? Mix design 1 and design 2 so everyone can spot their own flag.')

add(code='CFLAG14', pid='8783880388859', kind='country', name='USA', color='Multicolor',
    title='Personalised USA Terrace Flag – Stars & Stripes Sports Fan Flag – 3 Sizes',
    seo_title='Personalised USA Stars & Stripes Flag | Foxy Printing',
    seo_desc='Stars and Stripes printed with the words you choose, from a family name to a team. A personalised USA flag for game nights and parties, free UK delivery.',
    kw='personalised USA terrace flag',
    intro='Big, bright and instantly recognisable, the Stars and Stripes makes a great personalised USA terrace flag. Add your own words and it’s ready for game nights, Fourth of July parties, American football trips to London or an American-themed birthday.',
    h2='A personalised USA terrace flag – Stars and Stripes with your words',
    personal='Put a name, a state, a team or a short slogan in the first box, plus a second line if needed. You can upload a logo too. The live preview shows your wording beside the flag photo, and the message box is there for anything extra.',
    close='Throwing a Fourth of July party? An 8ft x 5ft American flag makes an instant backdrop.')

add(code='CFLAG15', pid='8783884812539', kind='country', name='Wales', color='Multicolor',
    title='Personalised Wales Terrace Flag – Welsh Dragon Football Fan Flag – 3 Sizes',
    seo_title='Personalised Wales Welsh Dragon Flag | Foxy Printing',
    seo_desc='The red Welsh dragon on green and white with your words printed on it. A personalised Wales flag for rugby, football and St David’s Day, free UK delivery.',
    kw='personalised Wales terrace flag',
    intro='The red dragon on green and white is one of the best-looking flags in the world, and our personalised Wales terrace flag adds your own words to it. It’s made for rugby weekends, football nights and St David’s Day.',
    h2='Personalised Wales terrace flag with the red dragon',
    personal='Add your town, your village, your club or a name in Welsh or English, with a second line if you want one. Upload a logo if you have one. The live preview shows your wording next to the flag photo before you order.',
    close='A personalised Welsh flag makes a lovely gift for anyone who’s moved away from home.')

# ----------------------------- FOOTBALL FLAGS -----------------------------
add(code='FFLAG1', pid='8783889989883', kind='england', name='England', color='Red/White',
    colours='red and white',
    title='Personalised Football Terrace Flag – Red & White England Fan Design – 3 Sizes',
    seo_title='Personalised England Football Fan Flag | Foxy Printing',
    seo_desc='A red and white football flag printed with your name, pub or town, made for England fans. Three sizes up to 8ft x 5ft and free UK delivery on every order.',
    kw='personalised England football flag',
    intro='Our personalised England football flag is a red and white fan design made for the summer tournaments, with space for your own words. Take it to the fan park, hang it over the bar at your local or drape it from the balcony on match night.',
    h2='A personalised England football flag for the whole squad of mates',
    personal='Add the name of your town, your pub or the group you watch with, and use the second line for a date or a chant. Upload a logo for your supporters’ club if you have one. The live preview shows your details next to the flag photo.',
    close='Going with a crowd? Pair it with our St George cross country flag so you’ve got both ends covered.')

clubs = [
 # code, pid, club, colours (words), google colour, design2, league
 # 6 Oct 2026: colours checked against the product photos; FFLAG10/13/19/29 corrected. The live store also has a
 # one-sentence layout note on every Design 2 (pushed by productUpdate); exports/terrace-flags/listings.json holds the live copy.
 ('FFLAG2','8784025616635','Arsenal','red and white','Red/White',False),
 ('FFLAG3','8784031219963','Aston Villa','claret and blue','Claret/Blue',False),
 ('FFLAG4','8784032563451','Brentford','red and white','Red/White',False),
 ('FFLAG5','8784034103547','Brighton','blue and white','Blue/White',False),
 ('FFLAG6','8784035315963','Chelsea','blue and white','Blue/White',False),
 ('FFLAG7','8784036692219','Crystal Palace','red and blue','Red/Blue',False),
 ('FFLAG8','8784038068475','Everton','royal blue and white','Blue/White',False),
 ('FFLAG9','8784040722683','Fulham','white and black','White/Black',False),
 ('FFLAG10','8784042623227','Ipswich','red, white and blue','Red/White/Blue',False),
 ('FFLAG11','8784043966715','Leicester City','blue and white','Blue/White',False),
 ('FFLAG12','8784045441275','Liverpool','red and yellow','Red/Yellow',False),
 ('FFLAG13','8784047046907','Man City','sky blue, white and black','Sky Blue/White/Black',False),
 ('FFLAG14','8784049340667','Man United','red, black and white','Red/Black/White',False),
 ('FFLAG15','8784050946299','Newcastle','black and white','Black/White',False),
 ('FFLAG16','8784052158715','Nottingham Forest','red and white','Red/White',False),
 ('FFLAG17','8784054321403','Southampton','red and white','Red/White',False),
 ('FFLAG18','8784057991419','Tottenham','navy and white','Navy/White',False),
 ('FFLAG19','8784059695355','West Ham','claret and white','Claret/White',False),
 ('FFLAG20','8784061956347','Wolves','old gold and white','Gold/White',False),
 ('FFLAG21','8784065659131','Wolves','old gold and black','Gold/Black',True),
 ('FFLAG22','8784081256699','West Ham','claret and blue','Claret/Blue',True),
 ('FFLAG23','8784093675771','West Ham','claret and blue','Claret/Blue',True),
 ('FFLAG24','8784094363899','Tottenham','navy and white','Navy/White',True),
 ('FFLAG25','8784094757115','Southampton','red and white','Red/White',True),
 ('FFLAG26','8784098361595','Nottingham Forest','red and white','Red/White',True),
 ('FFLAG27','8784098885883','Newcastle','black and white','Black/White',True),
 ('FFLAG28','8784099574011','Man United','red, black and white','Red/Black/White',True),
 ('FFLAG29','8784101474555','Man City','sky blue, white and black','Sky Blue/White/Black',True),
 ('FFLAG30','8784102129915','Liverpool','red and yellow','Red/Yellow',True),
 ('FFLAG31','8784103342331','Leicester City','blue and white','Blue/White',True),
 ('FFLAG32','8784104423675','Ipswich','blue and white','Blue/White',True),
 ('FFLAG33','8784105079035','Fulham','white and black','White/Black',True),
 ('FFLAG35','8784106160379','Crystal Palace','red and blue','Red/Blue',True),
 ('FFLAG36','8784106914043','Chelsea','blue and white','Blue/White',True),
 ('FFLAG37','8784107471099','Brighton','blue and white','Blue/White',True),
 ('FFLAG38','8784108683515','Brentford','red and white','Red/White',True),
 ('FFLAG39','8784109273339','Aston Villa','claret and blue','Claret/Blue',True),
 ('FFLAG40','8784109994235','Arsenal','red and white','Red/White',True),
]

# Hand-written, per product: (intro, h2, personal, close, seo_desc)
# {k} is replaced by the primary keyword.
CLUB_COPY = {
'FFLAG2': ('Our {k} is a fan-made red and white design for Arsenal supporters, printed with your own words. Hang it in the stand, over the sofa on derby day or in a young Gooner’s bedroom.',
  'A {k} printed with your name',
  'Type a name, a town or your supporters’ group, and use the second line for a date or a favourite chant. If your group has its own logo, upload it. The live preview shows your wording next to the flag photo before you order.',
  'Buying for a birthday? A 3ft x 2ft flag fits neatly on a bedroom wall.',
  'A red and white football fan flag printed with your name or group. Pick 3ft x 2ft, 5ft x 3ft or 8ft x 5ft, all hand-stitched, with free UK delivery.'),
'FFLAG3': ('Claret and blue through and through? This {k} is a fan-made design in the colours Villa fans know best, finished with the words you choose. It looks the part on an away day and just as good in the man cave.',
  'Your own {k} in claret and blue',
  'Add your name, your village or the coach you travel on, with room for a second line underneath. Upload your group’s logo if you have one. Check everything in the live preview, which shows your details beside the flag photo.',
  'Pair it with a second flag for the away end, or go big with 8ft x 5ft for the whole group.',
  'A claret and blue football flag with your own wording, printed in the UK and hand-stitched. Three sizes up to 8ft x 5ft, with free UK delivery included.'),
'FFLAG4': ('This {k} is a red and white fan design for Brentford supporters, with your own words printed into it. It’s a neat way to mark a first match, a season ticket or a big birthday.',
  'Make it yours: a {k}',
  'Pop in a name, the year you started going, or your supporters’ group, and use the second line if there’s more to say. You can upload a logo too. The live preview shows your text next to the flag photo.',
  'A great gift alongside a match ticket for a Bees fan.',
  'Red and white football fan flag printed with the name, date or group you choose. Hand-stitched 115gsm polyester in 3 sizes, with free delivery in the UK.'),
'FFLAG5': ('Blue and white stripes, your words: our {k} is a fan-made design for Brighton supporters on the south coast and beyond. Fly it in the stand or hang it at home for the big games.',
  'A {k} with your own wording',
  'Tell us the name, town or fan group to print, and add a second line if you like. Upload a logo for your group if you have one. The live preview shows your details alongside the flag photo before you check out.',
  'Watching with the family? The 5ft x 3ft size suits a living room wall.',
  'A blue and white striped football fan flag with your name or group printed on it. Three sizes, eyelets on all 4 edges, and free UK delivery on every flag.'),
'FFLAG6': ('Our {k} is a blue and white fan design for Chelsea supporters, with any wording you like printed on it. Bring it to the ground, hang it in the pub or give it to the Blues fan who has everything.',
  'Design your {k}',
  'Add a name, a nickname, your home town or the group you go with, with an optional second line. You can upload a logo. The live preview shows your details next to the flag photo, and the message box is for anything else.',
  'For a grandparent who’s followed the club for years, add their name and the year they first went.',
  'A blue and white football fan flag printed with your words, in 3ft x 2ft, 5ft x 3ft or 8ft x 5ft. Made to order in the UK, with free UK delivery included.'),
'FFLAG7': ('Red and blue and loud about it: this {k} is a fan-made design for Palace supporters in south London and everywhere else. Add your own words and it’s ready for a loud afternoon in the stand.',
  'A {k} printed with your words',
  'Type in your name, your area or the fan group you stand with, plus a second line if you need it. Upload a logo if you’ve got one. The live preview shows your wording beside the flag photo.',
  'Going as a group? The 8ft x 5ft size makes a real statement.',
  'A red and blue football fan flag printed with your name, area or group. Three sizes, hand-stitched with a 25mm binding, and free UK delivery on every flag.'),
'FFLAG8': ('This {k} is a royal blue and white fan design for Everton supporters, printed with your own words. It’s ideal for match days, a new season ticket or a Toffees fan’s birthday.',
  'Your {k} in royal blue and white',
  'Add a name, a street, a pub or your supporters’ group, and use the second line for a year or a short message. You can upload a logo. The live preview shows your details next to the flag photo before you order.',
  'Pair it with a smaller 3ft x 2ft flag for the little one in the family.',
  'A royal blue and white football fan flag with the wording you choose printed on it. Pick from 3 sizes up to 8ft x 5ft, with free delivery in the UK.'),
'FFLAG9': ('Our {k} is a white and black fan design for Fulham supporters, with any words you like printed on it. Hang it by the river on match day, in the pub or at home.',
  'A {k} made just for you',
  'Fill in a name, a group or a town, with a second line if there’s more to add. Upload your group’s logo if you have one. The live preview shows your wording beside the flag photo, and you can leave notes in the message box.',
  'A thoughtful gift for a Cottagers fan, with their name front and centre.',
  'White and black football fan flag printed with your name or group. Single-sided print on 115gsm polyester, 3 sizes up to 8ft x 5ft, free UK delivery.'),
'FFLAG10': ('This {k} is a blue and white fan design for Ipswich supporters, ready for the words you choose. Take it to Suffolk’s big match days or hang it proudly at home.',
  'Your {k} with your own text',
  'Add a name, a village or your supporters’ group, with a second line for a year or a slogan. You can upload a logo too. The live preview shows your wording next to the flag photo before you buy.',
  'Ordering for a supporters’ club? Ask about double-sided printing in the message box and we’ll quote.',
  'A blue and white football fan flag printed with your own words, made in the UK. Choose 3ft x 2ft, 5ft x 3ft or 8ft x 5ft, with free UK delivery included.'),
'FFLAG11': ('Our {k} is a blue and white fan design for Leicester City supporters, printed with the words you pick. It’s great for match days, family parties and Foxes fans of every age.',
  'A {k} with your name on it',
  'Type a name, a town or your fan group, and add a second line if you like. Upload a logo if you’d like one. The live preview shows your details beside the flag photo, and the message box is for anything else.',
  'Treat a young fan: their name on a 3ft x 2ft flag above the bed.',
  'A blue and white football fan flag printed with the name or group you choose. Hand-stitched 115gsm polyester in 3 sizes, and delivered free in the UK.'),
'FFLAG12': ('This {k} is a red and yellow fan design for Liverpool supporters, finished with your own words. Bring it to the match, the pub or the front room on a big European night.',
  'Your own {k}',
  'Add a name, a street, a group or a line from a favourite song, and use the second line if needed. You can upload a logo for your group. The live preview shows your wording next to the flag photo.',
  'Pair it with a matching flag for a mate so you’ve both got one for the away end.',
  'A red and yellow football fan flag printed with your words. Three sizes up to 8ft x 5ft, eyelets on all four edges, and free UK delivery on every flag.'),
'FFLAG13': ('Celebrate the treble season with this {k}, a sky blue and white fan design for Man City supporters with your own words printed on it. It’s a proud one for the stand, the bar or the bedroom.',
  'A treble-themed {k}',
  'Tell us the name, town or fan group to add, plus a second line for a year or a message. Upload a logo if you have one. The live preview shows your details beside the flag photo before you order.',
  'A brilliant gift for a City fan who was there for the treble.',
  'A sky blue and white treble-themed football fan flag, printed with your name or group. Three sizes, hand-stitched in the UK, with free UK delivery.'),
'FFLAG14': ('Our {k} is a red, black and white fan design for Man United supporters, ready for any words you want. Hang it in the stand, at home or in your local on match day.',
  'Create your {k}',
  'Add a name, a town, a group or a favourite chant, and use the second line if there’s more. Upload your group’s logo if you have one. The live preview shows your wording next to the flag photo.',
  'For a big group of Reds, go for 8ft x 5ft so it’s seen right across the stand.',
  'A red, black and white football fan flag printed with your words. Made to order in 3ft x 2ft, 5ft x 3ft or 8ft x 5ft, with free delivery across the UK.'),
'FFLAG15': ('Black and white and proud: this {k} is a fan-made design for Newcastle supporters, printed with your own words. Take it to the match, hang it at home or bring it to the pub on derby day.',
  'A {k} with your words on it',
  'Type a name, your town or your fan group, with an optional second line. You can upload a logo. The live preview shows your details beside the flag photo, and the message box is there for anything else.',
  'Ordering two? A 3ft x 2ft and a 5ft x 3ft make a good pair for home and away.',
  'A black and white football fan flag printed with your name, town or group. Hand-stitched with eyelets on all four edges, 3 sizes, and free UK delivery.'),
'FFLAG16': ('Our {k} is a red and white fan design for Nottingham Forest supporters, with the words you choose printed on it. It’s ideal for match day or for a Forest fan’s wall at home.',
  'Your {k}, made to order',
  'Add a name, a town or your supporters’ group, with a second line for a year or a short message. Upload a logo if you want one. The live preview shows your wording next to the flag photo.',
  'A lovely gift for a lifelong Forest fan: add their name and the year they first went.',
  'A red and white football fan flag printed with your name or group, made in the UK. Three sizes up to 8ft x 5ft and free delivery to any UK address.'),
'FFLAG17': ('This {k} is a red and white fan design for Southampton supporters, with your own words printed on it. Wave it on match day, or hang it in a young Saints fan’s bedroom.',
  'A {k} with your own text',
  'Tell us the name, town or group to print, and use the second line if you need it. You can upload a logo. The live preview shows your details beside the flag photo before you buy.',
  'Perfect for a birthday: their name in big letters on a 5ft x 3ft flag.',
  'A red and white football fan flag printed with the name, town or group you choose. Pick from 3 sizes, single-sided print, with free UK delivery.'),
'FFLAG18': ('Our {k} is a navy and white fan design for Tottenham supporters, with any wording you like printed on it. Bring it to the match, the pub or the living room for the big games.',
  'A {k} in navy and white',
  'Add a name, an area of London, your fan group or a short chant, with a second line if needed. Upload a logo for your group if you have one. The live preview shows your wording next to the flag photo.',
  'Pair it with a second flag for a Spurs-mad friend.',
  'A navy and white football fan flag printed with your words. Hand-stitched 115gsm polyester in 3ft x 2ft, 5ft x 3ft or 8ft x 5ft, with free UK delivery.'),
'FFLAG19': ('This {k} is a claret and blue fan design for West Ham supporters, printed with the words you choose. It’s made for match days in east London and for the Hammers fan’s wall at home.',
  'Your own {k}',
  'Type in a name, a borough, a pub or your supporters’ group, and add a second line if you like. You can upload a logo. The live preview shows your details beside the flag photo, and the message box is for anything else.',
  'For a big group heading to an away game, the 8ft x 5ft size is hard to miss.',
  'A claret and blue football fan flag printed with your name, area or group. Three sizes up to 8ft x 5ft, eyelets all round and free delivery within the UK.'),
'FFLAG20': ('Our {k} is an old gold and white fan design for Wolves supporters, printed with your own words. Hang it in the stand, at the pub or in the spare room you’ve turned into a shrine.',
  'A {k} in old gold',
  'Add a name, a town or your fan group, with a second line for a year or a message. Upload a logo if you have one. The live preview shows your wording next to the flag photo before you order.',
  'Want a different look? Our design 2 Wolves flag comes in old gold and black.',
  'An old gold and white football fan flag printed with your name or group. Made to order in the UK in 3 sizes, with free UK delivery on every order.'),
'FFLAG21': ('Here’s our second {k}: an old gold and black fan design for Wolves supporters, with any words you like printed on it. It’s bold enough for the stand and smart enough for the bar.',
  'Wolves fan flag design 2 – a {k}',
  'Tell us the name, town or fan group to add, and use the second line for anything extra. You can upload a logo. The live preview shows your details beside the flag photo, so you can compare it with our first Wolves design.',
  'Ordering for two fans? Get one of each design so they can tell them apart.',
  'Our second old gold and black football fan flag, printed with your own words. Three sizes up to 8ft x 5ft, hand-stitched, with free delivery in the UK.'),
'FFLAG22': ('This is our second {k}: a claret and blue fan design for West Ham supporters, with your own words printed on it. It gives you a different look to our first Hammers flag.',
  'West Ham fan flag design 2 – your {k}',
  'Add a name, an area, a pub or your group, with a second line if you need it. Upload a logo if you’d like one included. The live preview shows your wording next to the flag photo.',
  'A smart gift for a Hammers fan who already has our first design.',
  'A second claret and blue football fan flag design, printed with your name or group. Choose 3ft x 2ft, 5ft x 3ft or 8ft x 5ft, with free UK delivery.'),
'FFLAG23': ('A claret and blue {k}, design 2, for West Ham supporters who want their own words on show. It’s made to order in the UK in three sizes.',
  'Claret and blue {k} – design 2',
  'Type a name, a borough or your supporters’ group, plus a second line if you like. You can upload a logo. The live preview shows your details beside the flag photo, and the message box is for any extra notes.',
  'Hang it at home, or take the 3ft x 2ft size to an away game.',
  'Claret and blue football fan flag, design 2, printed with the words you choose. Hand-stitched polyester in 3 sizes, with free delivery to any UK address.'),
'FFLAG24': ('Our second {k} is a navy and white fan design for Tottenham supporters, printed with any words you choose. It’s a different layout to our first Spurs flag.',
  'Tottenham fan flag design 2 – a {k}',
  'Add a name, an area, your fan group or a date, with an optional second line. Upload a logo for your group if you have one. The live preview shows your wording next to the flag photo before you buy.',
  'Watching with friends? A 5ft x 3ft flag fits nicely behind the sofa.',
  'Our second navy and white football fan flag, printed with your name or group. Three sizes up to 8ft x 5ft, eyelets on all 4 edges and free UK delivery.'),
'FFLAG25': ('Here’s design 2 of our {k}: a red and white fan design for Southampton supporters, finished with your own words. Choose it if you fancy a change from our first Saints flag.',
  'Southampton fan flag design 2 – your {k}',
  'Tell us the name, town or group to print, and add a second line if needed. You can upload a logo. The live preview shows your details beside the flag photo.',
  'Pair both Saints designs for the home end and the garage wall.',
  'A second red and white football fan flag design with your words printed on it. Made in the UK in 3ft x 2ft, 5ft x 3ft or 8ft x 5ft, free UK delivery.'),
'FFLAG26': ('Our second {k} is a red and white fan design for Nottingham Forest supporters, with the words you choose printed on it. It gives you another style to pick from.',
  'Nottingham Forest fan flag design 2 – a {k}',
  'Add a name, a town or your supporters’ group, and use the second line for a year or a short message. Upload a logo if you want. The live preview shows your wording next to the flag photo.',
  'A handy second flag for the car boot, so there’s always one ready for away days.',
  'Our second red and white football fan flag, printed with your name or group. Hand-stitched 115gsm polyester, 3 sizes, with free delivery within the UK.'),
'FFLAG27': ('Design 2 of our {k} is a black and white fan design for Newcastle supporters, ready for any words you like. It’s a different look to our first Toon flag.',
  'Newcastle fan flag design 2 – your {k}',
  'Type a name, a town or your fan group, with a second line if you need one. You can upload a logo. The live preview shows your details beside the flag photo, and the message box takes anything else.',
  'A great gift for a Geordie living away from home.',
  'A second black and white football fan flag design, printed with your own words. Three sizes up to 8ft x 5ft, eyelets all round, and free UK delivery.'),
'FFLAG28': ('Here’s our second {k}: a red, black and white fan design for Man United supporters, printed with the words you choose. Pick it if you want a change from our first United flag.',
  'Man United fan flag design 2 – a {k}',
  'Add a name, a town, your fan group or a chant, and use the second line if there’s more. Upload a logo if you have one. The live preview shows your wording next to the flag photo before you order.',
  'Ordering for a dad and son? One of each design works well.',
  'Our second red, black and white football fan flag, printed with your name or group. Made to order in 3 sizes, with free delivery anywhere in the UK.'),
'FFLAG29': ('Our second treble-themed {k} is a sky blue and white fan design for Man City supporters, with your own words printed on it. It’s another way to remember that season.',
  'Man City treble fan flag design 2 – your {k}',
  'Tell us the name, town or group to add, with a second line for a year or a message. You can upload a logo. The live preview shows your details beside the flag photo.',
  'Pair it with our first treble design for the full set.',
  'A second sky blue and white treble-themed football fan flag with your words. Three sizes up to 8ft x 5ft, hand-stitched in the UK, free UK delivery.'),
'FFLAG30': ('Design 2 of our {k} is a red and yellow fan design for Liverpool supporters, finished with the words you choose. It’s a fresh look next to our first Reds flag.',
  'Liverpool fan flag design 2 – a {k}',
  'Add a name, a street, your group or a song lyric, with an optional second line. Upload a logo if you have one. The live preview shows your wording next to the flag photo, and you can leave notes in the message box.',
  'A big 8ft x 5ft flag makes a real impact on a European away trip.',
  'Our second red and yellow football fan flag design, printed with your own words. Pick 3ft x 2ft, 5ft x 3ft or 8ft x 5ft, with free delivery in the UK.'),
'FFLAG31': ('Here’s design 2 of our {k}: a blue and white fan design for Leicester City supporters, printed with your own words. Choose it if you want something different from our first Foxes flag.',
  'Leicester City fan flag design 2 – your {k}',
  'Type a name, a town or your supporters’ group, plus a second line if needed. You can upload a logo. The live preview shows your details beside the flag photo before you buy.',
  'A lovely gift for a young Foxes fan, with their name in big letters.',
  'A second blue and white football fan flag design, printed with your name or group. Hand-stitched 115gsm polyester, 3 sizes and free UK delivery.'),
'FFLAG32': ('Our second {k} is a blue and white fan design for Ipswich supporters, printed with whatever wording you like. It’s another style to choose from.',
  'Ipswich fan flag design 2 – a {k}',
  'Add a name, a village or your fan group, with a second line for a year or a slogan. Upload a logo if you want one included. The live preview shows your wording next to the flag photo.',
  'Running a supporters’ club? Get in touch about double-sided printing for a quote.',
  'Our second blue and white football fan flag, printed with your own words. Three sizes up to 8ft x 5ft, eyelets on all four edges, free UK delivery.'),
'FFLAG33': ('Design 2 of our {k} is a white and black fan design for Fulham supporters, ready for your own words. It’s a different layout to our first Fulham flag.',
  'Fulham fan flag design 2 – your {k}',
  'Tell us the name, group or town to add, with a second line if you need it. You can upload a logo. The live preview shows your details beside the flag photo, and the message box is there for extras.',
  'Hang it by the front door on match day, or take it to the ground.',
  'A second white and black football fan flag design with your name or group. Made to order in the UK, 3 sizes up to 8ft x 5ft, with free UK delivery.'),
'FFLAG35': ('Here’s our second {k}: a red and blue fan design for Crystal Palace supporters, printed with the words you choose. Pick it for a change from our first Palace flag.',
  'Crystal Palace fan flag design 2 – a {k}',
  'Add a name, your area or your fan group, and use the second line for anything extra. Upload a logo if you have one. The live preview shows your wording next to the flag photo before you order.',
  'Order one of each Palace design for the home end and the living room.',
  'Our second red and blue football fan flag, printed with your name, area or group. Three sizes, hand-stitched with 25mm binding, and free UK delivery.'),
'FFLAG36': ('Design 2 of our {k} is a blue and white fan design for Chelsea supporters, with any words you like printed on it. It’s another look to sit alongside our first Blues flag.',
  'Chelsea fan flag design 2 – your {k}',
  'Type a name, a nickname, a town or your group, with an optional second line. You can upload a logo. The live preview shows your details beside the flag photo.',
  'A great gift for a Blues fan’s birthday or Christmas.',
  'A second blue and white football fan flag design, printed with your own words. Pick 3ft x 2ft, 5ft x 3ft or 8ft x 5ft, with free delivery across the UK.'),
'FFLAG37': ('Our second {k} is a blue and white fan design for Brighton supporters, printed with the words you choose. It’s a different style to our first Seagulls flag.',
  'Brighton fan flag design 2 – a {k}',
  'Add a name, a town or your fan group, with a second line if you like. Upload a logo for your group if you have one. The live preview shows your wording next to the flag photo, and the message box takes any notes.',
  'Pair it with a 3ft x 2ft flag for the youngest fan in the house.',
  'Our second blue and white football fan flag, printed with your name or group. Hand-stitched 115gsm polyester in 3 sizes, with free UK delivery included.'),
'FFLAG38': ('Here’s design 2 of our {k}: a red and white fan design for Brentford supporters, finished with your own words. Choose it if you fancy a different look.',
  'Brentford fan flag design 2 – your {k}',
  'Tell us the name, year or supporters’ group to print, and use the second line if needed. You can upload a logo. The live preview shows your details beside the flag photo before you buy.',
  'A thoughtful gift for a Bees fan who already has our first design.',
  'A second red and white football fan flag design with the words you choose. Three sizes up to 8ft x 5ft, eyelets all round and free delivery in the UK.'),
'FFLAG39': ('Our second {k} is a claret and blue fan design for Aston Villa supporters, printed with any wording you like. It gives you another style to pick from.',
  'Aston Villa fan flag design 2 – a {k}',
  'Add a name, a village or the coach you travel on, with a second line for a year or message. Upload a logo if you have one. The live preview shows your wording next to the flag photo.',
  'Going big for a cup run? The 8ft x 5ft size is made for it.',
  'Our second claret and blue football fan flag, printed with your own words. Made to order in the UK in 3 sizes, with free delivery to any UK address.'),
'FFLAG40': ('Design 2 of our {k} is a red and white fan design for Arsenal supporters, ready for the words you choose. It’s a fresh look next to our first Gunners flag.',
  'Arsenal fan flag design 2 – your {k}',
  'Type a name, a town or your fan group, with an optional second line. You can upload a logo. The live preview shows your details beside the flag photo, and you can leave us a note in the message box.',
  'Pair it with our first Arsenal design so the whole family has one.',
  'A second red and white football fan flag design, printed with your name or group. Single-sided print on 115gsm polyester, 3 sizes, free UK delivery.'),
}

SEO_TITLES = {
 'FFLAG2':'Personalised Red & White Football Fan Flag | Foxy Printing',
 'FFLAG3':'Personalised Claret & Blue Terrace Flag | Foxy Printing',
 'FFLAG4':'Red & White Terrace Flag with Your Name | Foxy Printing',
 'FFLAG5':'Blue & White Striped Football Flag | Foxy Printing',
 'FFLAG6':'Personalised Blue & White Football Flag | Foxy Printing',
 'FFLAG7':'Personalised Red & Blue Terrace Flag | Foxy Printing',
 'FFLAG8':'Royal Blue Football Flag with Your Name | Foxy Printing',
 'FFLAG9':'Personalised White & Black Fan Flag | Foxy Printing',
 'FFLAG10':'Blue & White Terrace Flag, Custom Text | Foxy Printing',
 'FFLAG11':'Blue & White Fan Flag with Your Name | Foxy Printing',
 'FFLAG12':'Personalised Red & Yellow Football Flag | Foxy Printing',
 'FFLAG13':'Sky Blue Treble Football Fan Flag | Foxy Printing',
 'FFLAG14':'Red, Black & White Football Fan Flag | Foxy Printing',
 'FFLAG15':'Personalised Black & White Terrace Flag | Foxy Printing',
 'FFLAG16':'Red & White Football Flag, Custom Text | Foxy Printing',
 'FFLAG17':'Red & White Fan Flag with Your Name | Foxy Printing',
 'FFLAG18':'Personalised Navy & White Football Flag | Foxy Printing',
 'FFLAG19':'Claret & Blue Football Flag, Your Name | Foxy Printing',
 'FFLAG20':'Personalised Old Gold Football Fan Flag | Foxy Printing',
 'FFLAG21':'Old Gold & Black Terrace Flag Design 2 | Foxy Printing',
 'FFLAG22':'Claret & Blue Fan Flag Design 2 | Foxy Printing',
 'FFLAG23':'Claret & Blue Terrace Flag, Design 2 | Foxy Printing',
 'FFLAG24':'Navy & White Terrace Flag Design 2 | Foxy Printing',
 'FFLAG25':'Red & White Terrace Flag Design 2 | Foxy Printing',
 'FFLAG26':'Red & White Football Fan Flag Design 2 | Foxy Printing',
 'FFLAG27':'Black & White Football Flag Design 2 | Foxy Printing',
 'FFLAG28':'Red, Black & White Fan Flag Design 2 | Foxy Printing',
 'FFLAG29':'Sky Blue Treble Fan Flag Design 2 | Foxy Printing',
 'FFLAG30':'Red & Yellow Terrace Flag Design 2 | Foxy Printing',
 'FFLAG31':'Blue & White Football Flag Design 2 | Foxy Printing',
 'FFLAG32':'Blue & White Terrace Flag Design 2 | Foxy Printing',
 'FFLAG33':'White & Black Football Flag Design 2 | Foxy Printing',
 'FFLAG35':'Red & Blue Football Fan Flag Design 2 | Foxy Printing',
 'FFLAG36':'Blue & White Fan Flag Design 2 | Foxy Printing',
 'FFLAG37':'Blue & White Striped Flag Design 2 | Foxy Printing',
 'FFLAG38':'Red & White Fan Flag, Design 2 | Foxy Printing',
 'FFLAG39':'Claret & Blue Football Flag Design 2 | Foxy Printing',
 'FFLAG40':'Red & White Football Flag, Design 2 | Foxy Printing',
}

for code, pid, club, colours, gcol, d2 in clubs:
    intro, h2, personal, close, sd = CLUB_COPY[code]
    k = f'personalised {club} football flag'
    cols = [w.strip().title() for w in colours.replace(', ', ' and ').split(' and ')]
    cap_colours = (', '.join(cols[:-1]) + ' & ' + cols[-1]) if len(cols) > 1 else cols[0]
    label = club + (' Treble' if club == 'Man City' else '')
    title = f'Personalised Football Terrace Flag – {cap_colours} {label} Fan Design' + (' 2' if d2 else '') + ' – 3 Sizes'
    add(code=code, pid=pid, kind='club', name=club, colours=colours, color=gcol, design2=d2,
        title=title, seo_title=SEO_TITLES[code], seo_desc=sd, kw=k,
        intro=intro.format(k=k), h2=h2.format(k=k)[0].upper() + h2.format(k=k)[1:],
        personal=personal, close=close)

# ----------------------- shared blocks, varied wording -----------------------
WHY = [
 ['Printed on 115gsm knitted polyester, a light fabric that’s easy to carry to the ground',
  'Made from 115gsm knitted polyester, so it’s light enough to roll up and take with you',
  '115gsm knitted polyester keeps the flag light and easy to pack for an away day'],
 ['Digitally printed in the UK and hand-stitched, so every flag is made to order for you',
  'Each flag is digitally printed here in the UK and finished by hand',
  'Made to order: digitally printed in the UK, then hand-stitched'],
 ['A strong 25mm edge binding runs around the flag for a neat, sturdy finish',
  'Finished with strong 25mm edge binding all the way round',
  'Strong 25mm binding on the edges gives it a tidy, hard-wearing finish'],
 ['Eyelets on all 4 edges, so you can tie it to a railing, fence or wall either way up',
  'Eyelets along all 4 edges make it easy to hang from a barrier, balcony or pole',
  'Hang it how you like, with eyelets on all 4 edges'],
 ['Any wording you want: a name, a group, a town or a chant',
  'Fully customisable, so you can add any wording you like',
  'Your own text printed into the design, from a single name to a whole slogan'],
 ['A fire label on every flag, with the certificate available on request if a venue asks',
  'Every flag carries a fire label, and we can send the certificate on request',
  'Fire label fitted as standard; ask us if you need the certificate'],
 ['Suitable for indoor and outdoor use, from the stand to the bedroom wall',
  'Use it indoors or outdoors: at the match, in the pub or at home',
  'Made for indoor and outdoor use'],
]

SIZE = [
 ['Sizes: 3ft x 2ft, 5ft x 3ft or 8ft x 5ft',
  'Material: 115gsm knitted polyester',
  'Finish: hand-stitched with strong 25mm edge binding, eyelets on all 4 edges',
  'Print: single-sided as standard; double-sided on request (get in touch for a quote)',
  'Safety: fire label on every flag, certificate available on request'],
 ['Choose 3ft x 2ft, 5ft x 3ft or 8ft x 5ft',
  '115gsm knitted polyester, digitally printed in the UK',
  '25mm edge binding and eyelets on all 4 edges',
  'Single-sided print; contact us for a double-sided quote',
  'Fire label on every flag (certificate on request)'],
 ['Three sizes: 3ft x 2ft, 5ft x 3ft, 8ft x 5ft',
  'Fabric: 115gsm knitted polyester, hand-stitched',
  'Edges: strong 25mm binding with eyelets on all 4 sides',
  'Printed on one side; double-sided is available on request, just ask for a quote',
  'Every flag has a fire label; we can supply the certificate'],
]

DELIVERY = [
 'UK delivery is free on every flag. Each one is printed to order with your wording, so please check the spelling in the live preview before you order.',
 'Delivery is free anywhere in the UK. Because we make each flag to order with your text, double-check your wording in the preview before checkout.',
 'We deliver free of charge within the UK. Every flag is printed just for you, so take a moment to check your text in the live preview.',
]

FOOTBALL_DISC = ('This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or affiliated with {club}, the Premier League, the English Football League, or any club, league or player. Club and player names are used only to describe the design and who it’s for. All trademarks belong to their respective owners.')
ENGLAND_DISC = ('This is an unofficial, fan-made design created and printed by Foxy Printing. It is not endorsed by, sponsored by, or affiliated with the England national football team, The Football Association, or any club, league or player. Team and player names are used only to describe the design and who it’s for. All trademarks belong to their respective owners.')

CLUB_FULL = {'Man City':'Manchester City Football Club','Man United':'Manchester United Football Club',
 'Wolves':'Wolverhampton Wanderers Football Club','Tottenham':'Tottenham Hotspur Football Club',
 'West Ham':'West Ham United Football Club','Newcastle':'Newcastle United Football Club',
 'Brighton':'Brighton & Hove Albion Football Club','Ipswich':'Ipswich Town Football Club',
 'Leicester City':'Leicester City Football Club','Arsenal':'Arsenal Football Club','Aston Villa':'Aston Villa Football Club',
 'Brentford':'Brentford Football Club','Chelsea':'Chelsea Football Club','Crystal Palace':'Crystal Palace Football Club',
 'Everton':'Everton Football Club','Fulham':'Fulham Football Club','Liverpool':'Liverpool Football Club',
 'Nottingham Forest':'Nottingham Forest Football Club','Southampton':'Southampton Football Club'}

e = html.escape

LEADS = ['Your {k} takes a minute to set up. ', 'Setting up your {k} is simple. ', 'Making your {k} is easy. ']

def build(p, i):
    # pick 5 of the 7 WHY facts, rotating which two are left out and the wording
    idx = [(i + j) % 7 for j in range(7)][:5]
    why = [WHY[f][(i + f) % 3] for f in idx]
    if p['kind'] != 'country' and i % 2 == 0:
        why[0] = why[0] if 'colour' in why[0] else why[0]
    size = SIZE[i % 3]
    deliv = DELIVERY[(i // 2) % 3]
    parts = [f"<p>{e(p['intro'], quote=False)}</p>",
             f"<h2>{e(p['h2'], quote=False)}</h2>",
             f"<p>{e(LEADS[i % 3].format(k=p['kw']) + p['personal'], quote=False)}</p>",
             "<h3>Why you’ll love it</h3>",
             '<ul>' + ''.join(f'<li>{e(w, quote=False)}</li>' for w in why) + '</ul>',
             "<h3>Size &amp; details</h3>",
             '<ul>' + ''.join(f'<li>{e(s, quote=False)}</li>' for s in size) + '</ul>',
             "<h3>Delivery</h3>",
             f"<p>{e(deliv, quote=False)}</p>",
             f"<p>{e(p['close'], quote=False)}</p>"]
    if p['kind'] == 'club':
        parts += ["<h3>Please note</h3>",
                  f"<p class=\"disclaimer\">{e(FOOTBALL_DISC.format(club=CLUB_FULL[p['name']]), quote=False)}</p>"]
    elif p['kind'] == 'england':
        parts += ["<h3>Please note</h3>", f"<p class=\"disclaimer\">{e(ENGLAND_DISC, quote=False)}</p>"]
    return '\n'.join(parts)

def words(h):
    return len(re.sub(r'<[^>]+>', ' ', h).split())

BANNED = re.compile(r'\b(official|licensed|authentic|genuine|approved|merchandise|trerrace)\b', re.I)

def main():
    out = []
    for i, p in enumerate(P):
        d = build(p, i)
        rec = dict(p)
        rec['descriptionHtml'] = d
        rec['words'] = words(d)
        out.append(rec)
    problems = []
    seen_t, seen_s, seen_d = set(), set(), set()
    for r in out:
        body_wo_disc = r['descriptionHtml'].split('<h3>Please note</h3>')[0]
        checks = {
            'words': 180 <= r['words'] <= 350,
            'seo_title_len': len(r['seo_title']) <= 60,
            'seo_desc_len': 140 <= len(r['seo_desc']) <= 155,
            'title_len': len(r['title']) <= 150,
            'banned_body': not BANNED.search(body_wo_disc + r['title'] + r['seo_title'] + r['seo_desc']),
            'kw_first_sentence': r['kw'].lower() in r['intro'].lower().split('. ')[0] or r['kw'].lower() in r['intro'].lower(),
            'kw_h2': r['kw'].lower() in r['h2'].lower() or r['kw'].replace('terrace flag','flag').lower() in r['h2'].lower(),
            'straight_apostrophe': "'" not in r['descriptionHtml'],
        }
        for k, ok in checks.items():
            if not ok:
                problems.append((r['code'], k, r['words'], len(r['seo_title']), len(r['seo_desc'])))
        for s, key in ((seen_t, 'title'), (seen_s, 'seo_title'), (seen_d, 'seo_desc')):
            if r[key] in s and not (key == 'title' and r['code'] == 'FFLAG23'):  # FFLAG23 = possible duplicate of FFLAG22, stays DRAFT
                problems.append((r['code'], 'dup ' + key))
            s.add(r[key])
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w'), ensure_ascii=False, indent=1)
    print(len(out), 'listings;', 'word range', min(r['words'] for r in out), '-', max(r['words'] for r in out))
    for pr in problems:
        print('PROBLEM', pr)

if __name__ == '__main__':
    main()
