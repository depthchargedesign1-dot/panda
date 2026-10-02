"""Manual name map for the 1,196 face-mask listings in exports/face-masks/masks-manual-review.csv.

Decisions are made from the listing TITLE only and keyed by CSV row index (0-based, header excluded).
Run: python3 tools/mask_manual_map.py  ->  writes exports/face-masks/manual-name-map.json keyed by handle.

Types: person / pack / custom / generic / unclear.
Extra keys: character (role named in title), title_spelling (the title's spelling when the name was
corrected), note.
"""
import csv, json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "exports", "face-masks", "masks-manual-review.csv")
OUT = os.path.join(HERE, "..", "exports", "face-masks", "manual-name-map.json")


def P(name, cat="celeb", show=None, **kw):
    return {"type": "person", "name": name, "show": show, "category": cat, **kw}


def K(names, size=None, show=None, cat=None, **kw):
    d = {"type": "pack", "names": list(names), "pack_size": size}
    if show: d["show"] = show
    if cat: d["category"] = cat
    d.update(kw)
    return d


def C(**kw):
    return {"type": "custom", **kw}


def G(name, show=None, **kw):
    return {"type": "generic", "name": name, "show": show, **kw}


def U(note=None, **kw):
    d = {"type": "unclear"}
    if note: d["note"] = note
    d.update(kw)
    return d


BB = "The Big Bang Theory"; EE = "EastEnders"; FR = "Friends"; MM = "Mad Men"; SATC = "Sex and the City"
IAC = "I'm a Celebrity"; MIC = "Made in Chelsea"; TW = "The Only Way Is Essex"; NB = "Neighbours"
BOND = "James Bond"; ST = "Star Trek"; MBB = "Mrs Brown's Boys"; HA = "Home and Away"; GS = "Geordie Shore"
BRB = "Breaking Bad"; CS = "Coronation Street"; DD = "Dragons' Den"; XF = "The X Factor"; AP = "American Pie"
FF = "Fast & Furious"; ATEAM = "The A-Team"; GB = "Great British Bake Off"; OFAH = "Only Fools and Horses"

D = {}
D.update({
0: P("Zendaya", "tv"),
1: P("Victoria", "tv", FR), 2: P("Victoria", "tv", FR),
3: K(["Vincent Simone", "Flavia"], 2, "Strictly Come Dancing", "reality", note="couple"),
4: P("Govinda", "film"), 5: P("Rekha", "film"), 6: P("Sridevi", "film"),
7: P("Lewis", "reality", TW),
8: U("first name only: Kevin"),
9: P("Maria", "tv", MBB),
10: P("Mark Gatiss", "tv", "Sherlock", character="Mycroft"),
11: P("Stuart", "tv", BB),
12: C(note="DIY comedian mask"), 13: C(note="DIY comedian 2-mask"), 14: C(note="DIY comedians"), 15: C(note="DIY comedians"),
16: P("Louis C.K.", "comedy"),
17: P("Raj", "tv", BB), 18: P("Penny", "tv", BB), 19: P("Sheldon", "tv", BB), 20: P("Leonard", "tv", BB),
21: P("Shirley", "tv", EE),
22: P("Lacey Turner", character="Stacey Slater"),
23: P("Lorna Fitzgerald", character="Abbi Branning"),
24: P("Matt Di Angelo", character="Dean Wicks", title_spelling="Matt Di Angel"),
25: P("Dean Gaffney", character="Robbie Jackson"),
26: P("Samantha Womack", character="Ronnie Mitchell"),
27: P("Ross", "tv", FR), 28: P("Rachel", "tv", FR), 29: P("Phoebe", "tv", FR), 30: P("Monica", "tv", FR),
31: P("Mel", "reality", GB),
32: K([], 4, GB, "reality", note="all 4 judges; names not in title"),
33: P("Chris Eubank", "reality", IAC), 34: P("George Shelley", "reality", IAC), 35: P("Jorgie Porter", "reality", IAC),
36: P("Lady Colin Campbell", "reality", IAC), 37: P("Susannah Constantine", "reality", IAC), 38: P("Susannah", "reality", IAC),
39: P("Yvette Fielding", "reality", IAC),
40: P("Ollie", "reality", MIC), 41: P("Proudlock", "reality", MIC),
42: P("January Jones", "tv", MM, character="Betty Francis"),
43: P("Jon Hamm", "tv", MM, character="Don Draper"),
44: P("Vincent Kartheiser", "tv", MM, character="Pete Campbell"),
45: P("Jesse", "tv", NB, title_spelling="JESSE"), 46: P("Lou", "tv", NB), 47: P("Madge Ramsay", "tv", NB, title_spelling="MADGE RAMSEY"),
48: P("Toby", "tv", NB, title_spelling="TOBY"),
49: P("Marlene", "tv", OFAH),
50: P("Alexander", "tv", SATC), 51: P("Samantha", "tv", SATC), 52: P("Miranda", "tv", SATC),
53: C(show=SATC, note="request a Sex and the City mask"),
54: P("Smith", "tv", SATC),
55: P("Hikaru Sulu", "tv", ST), 56: P("Sulu", "tv", ST), 57: P("Worf", "tv", ST),
58: K([], None, BOND, "film"), 59: P("Jaws", "film", BOND), 60: P("Ursula Andress", "film", BOND, title_spelling="Ursula Anders"),
61: P("Naomie Harris", "film", BOND, character="Moneypenny", title_spelling="Naomi Harris"),
62: K([], None, BOND, "film", note="trade price pack"), 63: K([], None, BOND, "film", note="Bond Pack 1"),
64: K([], None, BOND, "film", note="Bond Pack 2"), 65: K([], None, BOND, "film", note="Bond mega pack"),
66: P("Ben Stiller", note="Blue Steel pose"),
67: P("Walter White", "tv", BRB),
68: P("Sean Bean", "film", note="long hair"),
69: P("Mortdecai", "film", title_spelling="Mortedecai"),
70: P("Natalie Dormer", "film", title_spelling="Nataliedormer"),
71: P("Olivia Wilde", "film", "Back to the Future"),
72: P("Rebel Wilson", "film", character="Fat Amy"),
73: P("Kate McKinnon"), 74: P("Sheryl Crow"), 75: P("Snooki"),
76: G("BFG", "The BFG"),
77: P("President Bush"), 78: P("President Obama"),
79: P("The Queen", "royal"),
80: K(["The Queen", "Prince Philip", "Prince Harry", "Prince William", "Kate", "Prince Charles", "Camilla"], 7, cat="royal", note="Diamond Jubilee"),
81: P("Gadhafi"), 82: P("Hitler"), 83: P("JFK"),
84: K([], 7, cat="royal", note="Royal Family set"),
85: P("Sophie, Countess of Wessex", "royal", title_spelling="Princess Sophie Of Wessex"),
86: G("Corgi"),
87: G("Royal Baby", note="title says 'Masks'; may be a set"),
88: P("Lenin"), 89: P("President Nixon"), 90: P("President Sarkozy"),
91: P("Iain Duncan Smith"), 92: P("Edwin Poots"), 93: P("The Queen Mother", "royal", title_spelling="Queen Mum", note="young"),
94: P("The Queen", "royal"),
95: P("Andrea Leadsom"), 96: P("Alun Cairns"), 97: P("Amber Rudd"), 98: P("Angela Merkel"), 99: P("Bernie Sanders"),
100: P("Boris Johnson"), 101: P("Chris Grayling", title_spelling="Chris Gayling"), 102: P("Elizabeth Truss"), 103: P("Gavin Williamson"),
104: P("Hillary Clinton"), 105: P("Jeremy Hunt"), 106: P("Justine Greening"), 107: P("Kim Jong Un", title_spelling="KIM JUNG UN"),
108: P("Michael Fallon"), 109: P("Patrick McLoughlin"), 110: P("Philip Hammond"), 111: P("Priti Patel"), 112: P("Rupert Murdoch"),
113: P("Sajid Javid"), 114: P("Theresa Villiers"), 115: P("Tony Blair"),
116: P("Gandhi"), 117: P("Shakespeare"), 118: P("Stalin"),
119: P("Alex Salmond"), 120: P("James Folder", note="name as in title; unfamiliar"), 121: P("Michelle Obama", title_spelling="Michelle_Obamamint"),
122: G("Minions", "Minions"),
123: U("Pinky - could be a character, no context"),
124: U("Pryro - Pyro?"), 125: U("Pyro"), 126: U("Pyroo"), 127: U("Pyrooo"), 128: U("Pyrooo"),
129: G("Santa"), 130: G("Santa"),
131: G("Dobby", "Harry Potter"),
132: P("Phil 'The Power' Taylor", "darts"), 133: P("Terry Jenkins", "darts"),
134: P("Mervyn King", "darts", title_spelling="Mervin King"), 135: P("Gary Anderson", "darts"),
136: P("Big John Henderson", "darts"), 137: P("Martin 'Wolfie' Adams", "darts"), 138: P("Ted 'The Count' Hankey", "darts"),
139: C(note="DIY choose a boxer"), 140: C(note="DIY boxers"),
141: P("Tyson Fury", "boxing"), 142: P("Tyson Fury", "boxing", note="smiling"),
143: C(note="custom photo"),
144: P("Lewis Hamilton", "f1"), 145: P("Sebastian Vettel", "f1"),
146: P("Jimenez", "golf"), 147: P("Rory McIlroy", "golf"),
148: K([], None, "Ryder Cup", "golf", note="Ryder Cup team pack 1"), 149: K([], None, "Ryder Cup", "golf", note="Ryder Cup team pack 2"),
150: P("Mark O'Meara", "golf"), 151: P("Mark O'Meara", "golf"),
152: P("Negredo", "football", title_spelling="Negrado"),
153: P("Jessica Ennis", "sport"), 154: P("Mark Cavendish", "sport"),
155: G("USA flag"), 156: G("Scotland flag"), 157: G("Ireland flag"), 158: G("France flag"),
159: P("Edwin van der Sar", "football"), 160: P("David Beckham", "football", note="cartoon"), 161: P("Peter Crouch", "football", note="cartoon"),
162: P("Andre Villas-Boas", "football"), 163: P("Ronaldinho", "football", note="cartoon"),
164: P("Zola"), 165: P("Gazza"), 166: P("Neymar"), 167: P("Paul Merson"), 168: P("Peter Schmeichel", title_spelling="Peterschmeichel"),
169: U("Rio - single name"), 170: P("Soldado"),
171: P("Luis Suarez"), 172: P("Wealdstone Raider"),
173: P("Anthony Martial", "football"), 174: P("Dante", "football"), 175: U("garbled name (Kad..)", category="football"),
176: P("Marcelo", "football"), 177: P("Neymar", "football"), 178: P("Abidal", "football"), 179: P("Benzema"),
180: P("Deco", "football"), 181: P("Edmilson", "football"), 182: P("Eto'o", "football", title_spelling="ETO"), 183: P("Flamini"),
184: P("Gudjohnsen", "football", title_spelling="GUDJHONSEN"), 185: P("Henry", "football"), 186: P("Iniesta", "football"),
187: P("Jorquera", "football"), 188: P("Lallana"), 189: P("Lennon"), 190: P("Marquez", "football"), 191: P("Mertesacker"),
192: P("Mertesacker"), 193: P("Messi", "football"), 194: P("Milito", "football"), 195: P("Monreal"), 196: P("Puyol", "football"),
197: P("Ronaldinho", "football"), 198: P("Sturridge"), 199: P("Sylvinho", "football"),
})

D.update({
200: P("Thuram", "football"), 201: P("Toure", "football"), 202: P("Valdes", "football"),
203: P("Víctor Valdés", "football", title_spelling="VÃ­ctor ValdÃ£Â©S"), 204: P("Viviano", "football"),
205: P("Xavi", "football"), 206: P("Xavi"), 207: P("Xavi", "football"), 208: P("Zambrotta", "football"),
209: P("Benzema"), 210: P("Debuchy", "football"), 211: P("Pele", "football"), 212: P("Michael Holding"),
213: P("Chris Robshaw", "rugby"), 214: P("Dan Cole", "rugby"), 215: P("Manusamoa Tuilagi", "rugby"), 216: P("Owen Farrell", "rugby"),
217: C(note="request any celebrity or custom photo"),
218: P("Conor McGregor", "sport", title_spelling="Connor Mcgregor"), 219: P("Frank Mir", "sport"),
220: P("Mark Warburton", "sport"), 221: G("Motorbiker"),
222: P("Ronda Rousey", "sport", note="bob hair"), 223: P("Ronda Rousey", "sport"),
224: P("Shaquille O'Neal", "sport", title_spelling="Shaquille O â€™Neil"),
225: P("Rafa Nadal", "tennis", title_spelling="Rafa Nedal"),
226: P("Dan Hegarty", "sport"), 227: P("Dean Harrison", "sport"), 228: P("Gary Johnson", "sport"), 229: P("Guy Martin", "sport"),
230: P("Dan Kneen", "sport"), 231: P("James Hillier", "sport", title_spelling="James Hiller"), 232: P("Jamie Hamilton", "sport"),
233: P("Jimmy Storrar", "sport"), 234: P("Lee Johnston", "sport", title_spelling="Lee Johnson", note="check spelling"), 235: P("Michael Dunlop", "sport"),
236: K([], None, cat="music", group="Abba"),
237: P("Björn Ulvaeus", "music"), 238: P("Agnetha Fältskog"),
239: P("Niall Horan", "music"), 240: P("Zayn Malik", "music"), 241: P("Zayn Malik", "music"),
242: P("Simon Cowell", "music", XF), 243: P("Gary Barlow", "music", XF), 244: P("Max George", "music"),
245: K([], None, XF, "music", note="X Factor judges pack"),
246: P("Charlie Rundle"), 247: P("Honey G", "music", XF),
248: U("no name in title"),
249: P("Borat"), 250: U("Fizz - no context"), 251: K(["Keith", "Orville"], 2, note="Keith and Orville"),
252: P("Betty", "tv", CS), 253: P("Gavin", "tv", "Gavin & Stacey"), 254: P("Joanna Page", "tv", "Gavin & Stacey"),
255: P("Beyoncé", title_spelling="Beyonce"), 256: P("Joey", "tv", FR), 257: P("Chandler", "tv", FR),
258: P("Carrie Bradshaw", "tv", SATC), 259: P("Harry", "tv", SATC), 260: P("Charlotte", "tv", SATC),
261: P("Billie", "reality", TW), 262: P("Deborah Meaden", "tv", DD), 263: U("Dino - no context"),
264: P("Duncan Bannatyne", "tv", DD, title_spelling="Duncan Banatyne"), 265: P("Einstein"), 266: P("Gemma", "reality", TW),
267: G("Gonzo", "The Muppets"), 268: P("Hilary Devey", "tv", DD, title_spelling="Hilary Davey"), 269: P("James Caan", "tv", DD),
270: P("Kim", "tv", EE), 271: P("Dog the Bounty Hunter"), 272: P("Heather Small", note="on a stick"),
273: P("Howard", "tv", BB), 274: K([], 3, "Eurovision", "music"), 275: P("Howard", "tv", BB), 276: P("Alf", "tv", HA),
277: P("Amy", "tv", BB), 278: P("Becker"), 279: P("Becky", "tv", CS), 280: U("Breaking Bad - character not named", show=BRB),
281: P("Casey Braxton", "tv", HA), 282: P("Darryl Braxton", "tv", HA), 283: P("Denise Welch", title_spelling="Denise Welsh", note="ice skating"),
284: P("Dexter", "tv", EE), 285: U("Downton - character not named", show="Downton Abbey"), 286: U("Downton - character not named", show="Downton Abbey"),
287: U("EastEnders - character not named", show=EE), 288: U("Emmerdale - character not named", show="Emmerdale"),
289: P("Andy Devine", "tv", "Emmerdale", character="Shadrach Dingle"), 290: P("Gaz", "reality", GS),
291: P("Philip Glenister", character="Gene Hunt"), 292: P("Gus", "tv", BRB), 293: P("Heath Braxton", "tv", HA, title_spelling="Heath Baxton"),
294: U("Homer - no context"), 295: U("Hutch - no context"), 296: P("Jason Bradbury", "tv", "The Gadget Show"), 297: P("Jay", "reality", GS),
298: P("Bernard Bresslaw", "film", "Carry On"), 299: U("Bith"), 300: P("Boycie"), 301: U("Brain - no context"),
302: P("Brax", "tv", HA), 303: P("Buster", "tv", MBB), 304: P("Buster", "tv", MBB), 305: U("Chesney - first name only"),
306: P("Christian", "tv", EE), 307: G("Compare the Market", "Compare the Market"), 308: P("Dino", "tv", MBB),
309: P("Elizabeth", "tv", "Keeping Up Appearances"),
310: P("Christina Hendricks", "tv", MM, character="Joan Harris"), 311: P("Elisabeth Moss", "tv", MM, character="Peggy Olson"),
312: P("John Slattery", "tv", MM, character="Roger Sterling"),
313: P("Brian Littrell", "music", band="Backstreet Boys"), 314: P("David Neilson", "tv", character="Roy"), 315: P("Heskey", "tv"),
316: P("Jacqueline Jossa", "tv", character="Lauren Branning"), 317: P("Julie Hesmondhalgh", "tv", character="Hayley"),
318: P("Kim Kardashian", "tv", note="brown hair"), 319: P("Bouncer", "tv", NB), 320: P("Daphne Clarke", "tv", NB),
321: U("Alisha - first name only"), 322: P("Andy Gray", "tv", title_spelling="Andy Grey", note="check spelling"), 323: P("Ben Shephard", "tv", title_spelling="Ben Shepherd1"),
324: P("Hank", "tv", BRB), 325: P("Grado", "tv"), 326: P("Lucy Mecklenburgh", "tv", note="red hair"), 327: P("Marnie", "reality", GS),
328: P("Michelangelo"), 329: P("Rosemary Shrager", "tv", title_spelling="Rosemary SCHRAGER"), 330: P("Skyler", "tv", BRB),
331: P("James Avery", "tv", character="Uncle Phil"), 332: P("Cheska", "reality", MIC),
333: U("MIA"), 334: U("MIS2"), 335: P("Hailee Steinfeld"), 336: U("KIP"), 337: U("Aimeet"),
338: P("Bergüzar Korel", "tv", title_spelling="BergÃ£Â¼Zar Korel"), 339: U("Booth1a2412"), 340: P("Cascada", "tv"),
341: P("Fergie", "tv"), 342: P("Inna", "tv"), 343: P("Adam Driver", "tv"), 344: P("Annette Badland", "tv"),
345: U("Alessandra - first name only"), 346: P("Alex O'Loughlin"), 347: P("Ava Gardner"), 348: P("B.A.", "tv", ATEAM),
349: P("Baden-Powell"), 350: G("The Joker", "Batman"), 351: G("Batman", "Batman"), 352: P("Blofeld"),
353: P("Danny", "film", "Grease"), 354: P("David Bowie", "film", "Labyrinth", character="Jareth"), 355: P("Diaz"),
356: P("Dolph Lundgren", character="Ivan Drago"), 357: P("Eddie Kaye", "film", AP, character="Paul Finch", note="name as in title"),
358: U("Ellen - first name only"), 359: P("Eugene Levy", "film", AP, character="Jim's Dad"), 360: U("Fantastic"),
361: P("Sandy", "film", "Grease"), 362: G("Gestapo officer"), 363: P("Hannibal Smith", "tv", ATEAM), 364: P("Jesse", "tv", BRB, title_spelling="Jessie"),
365: P("Jordana Brewster", "film", FF), 366: U("Lively - surname only, reads as a word"), 367: P("Michelangelo"),
368: U("Miranda - first name only"), 369: P("Murdock", "tv", ATEAM, title_spelling="Murdoch"), 370: P("Perlman"),
371: P("Russell Crowe", "film", "Robin Hood", title_spelling="Russel Crow"), 372: P("Rosie Huntington-Whiteley", title_spelling="Rosie Huntington Whitely"),
373: P("Ryan Reynolds", "film", "Green Lantern"), 374: P("Seann William Scott", "film", AP, character="Stifler", title_spelling="Sean William Scott"),
375: P("Snape"), 376: P("Tyrese Gibson", "film", FF), 377: U("Vespa"), 378: P("Vin Diesel", "film", FF),
379: P("Will Smith", "film", "Suicide Squad", character="Deadshot"), 380: P("Winslet"), 381: P("Harry Kane", "football"),
382: G("Braveheart", "Braveheart"), 383: P("Cher"), 384: G("Chucky", "Child's Play"), 385: G("Chucky", "Child's Play"),
386: P("Clooney"), 387: P("Daniel Craig"), 388: G("Day of the Dead"), 389: G("Day of the Dead"), 390: G("Day of the Dead"), 391: G("Day of the Dead"),
392: G("Dracula"), 393: P("Dunga"), 394: P("Heath Ledger"), 395: G("Pennywise", "It"), 396: P("Jean-Claude Van Damme"),
397: P("Jennifer Aniston", title_spelling="jennifer_anniston"), 398: P("Kenan Thompson"), 399: P("Kenny Ireland"), 400: P("Kim Kardashian"),
401: P("Michael J. Fox", note="young"), 402: P("Michael J. Fox", note="young"), 403: U("Nani - single name"), 404: P("Nas"),
405: U("Pedro - first name only"), 406: P("Pink"), 407: P("Redfoo"), 408: P("Russell Brand"), 409: U("Sloth - character or animal?"),
410: G("Stormtrooper", "Star Wars"), 411: P("Taylor Swift"), 412: P("Tiger Woods"),
413: P("Adele", "music"), 414: P("Beyoncé", "music", title_spelling="BEYONCE"), 415: P("Cher", "music"), 416: P("Coolio", "music"),
417: P("Drake", "music"), 418: P("Elvis", "music"), 419: P("Eminem", "music"),
})

LI = "Love Island"; RH = "The Real Housewives"; CH = "The Chase"; DEF = "The Defenders"; BBY = "Bad Boys"; IM = "Ink Master"
MH = "Money Heist"; VIC = "The Victim"; QF = "The Queen of Flow"; AUS = "Austin Powers"; BCS = "Better Call Saul"; CK = "Cobra Kai"
DC = "The Dark Crystal"; DG = "Derry Girls"; EIP = "Emily in Paris"; BLL = "Big Little Lies"


def T(*names):  # football pack, names exactly as listed in the title
    return K(list(names), len(names), cat="football")


D.update({
420: P("Hardwell", "music"), 421: P("Jamelia", "music"), 422: P("Ludacris", "music"), 423: P("Meat Loaf", "music", title_spelling="MEATLOAF"),
424: P("Michael Jackson", "music", note="Jackson Five era"), 425: P("Michael Jackson", "music", note="Off the Wall era"),
426: P("Pitbull", "music"), 427: P("Skrillex", "music"), 428: P("Sting", "music"), 429: P("Tulisa", "music"), 430: P("Usher", "music"),
431: P("will.i.am", "music"), 432: P("Zayn Malik", "music"), 433: P("Zayn Malik", "music"),
434: P("Camilla", "royal", title_spelling="CARMILLA"), 435: P("Prince Philip", "royal", note="with hat"), 436: P("The Queen", "royal"),
437: P("Sophie, Countess of Wessex", "royal"),
438: P("Isco", "football"), 439: P("Koke", "football"), 440: P("Neymar", "football"), 441: P("Neymar", "football"), 442: P("Pele", "football"),
443: P("Zico", "football"),
444: P("Carlos Sainz Jr", "f1", note="cap"), 445: P("Kimi Räikkönen", "f1", title_spelling="KIMI RAIKKONEN", note="cap"),
446: P("Paul Casey", "golf", title_spelling="PAULCASEY"), 447: P("Martina Hingis", "tennis", note="90s"),
448: T("Kane", "Rashford", "Southgate"), 449: T("Kane", "Rashford", "Foden", "Southgate"),
450: T("Grealish", "Sancho", "Coady", "Southgate"), 451: T("Greenwood", "Shaw", "Saka", "Southgate"),
452: T("Alexander-Arnold", "James", "Mings", "Southgate"), 453: T("Calvert-Lewin", "White", "Henderson", "Southgate"),
454: T("Bale", "Ramsey", "Davies", "Allen"), 455: T("Silva", "Firmino", "Alisson"), 456: T("Suarez", "Cavani"),
457: T("Messi", "Di Maria", "Aguero"), 458: T("Lukaku", "De Bruyne", "Hazard"), 459: T("Grealish", "Kane", "Foden"),
460: T("James", "Alexander-Arnold", "Trippier", "Walker"),
461: dict(T("Rashford", "Kane", "Sterling"), title_spelling="STRELING"),
462: P("Phil Foden", "football", note="new hair"),
463: K([], None, cat="football", note="England Euro 2020 full squad"),
464: T("Kane", "Foden", "Sterling", "Grealish"),
})
for i, n in zip(range(465, 494), [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 35, 40, 45, 50]):
    D[i] = C(pack_size=n, note="personalised photo masks")

D.update({
494: P("Clint Howard", "film", AUS), 495: P("Fat Bastard", "film", AUS), 496: P("Frau Farbissina", "film", AUS),
497: P("Mike Myers", "film", AUS), 498: P("Mini-Me", "film", AUS, title_spelling="Mini Me"), 499: P("Seth Green", "film", AUS),
500: P("Verne Troyer", "film", AUS),
501: P("Dom", "reality", LI), 502: P("Dom", "reality", LI), 503: P("Adam", "reality", LI), 504: P("Mike", "reality", LI),
505: P("Montanna", "reality", LI), 506: P("Rachel", "reality", LI), 507: P("Sam", "reality", LI),
508: P("Adele", "music"), 509: P("Beyoncé", "music", title_spelling="Beyonce"), 510: P("Drake", "music"), 511: P("Kygo", "music"),
512: P("Lizzo", "music"), 513: P("Lizzo", "music"), 514: P("Madonna", "music"), 515: P("Pink", "music"), 516: P("Pitbull", "music"),
517: P("Rihanna", "music"),
518: P("Adrienne Maloof", "reality", RH), 519: P("Camille Grammer", "reality", RH), 520: P("Dawn Ward", "reality", RH),
521: P("Dorit Kemsley", "reality", RH), 522: P("Eileen Davidson", "reality", RH), 523: P("Eva Marcille", "reality", RH),
524: P("Phaedra Parks", "reality", RH), 525: P("Porsha Williams", "reality", RH), 526: P("Rachel Lugo", "reality", RH),
527: P("Shamari Fears", "reality", RH), 528: P("Sheree Whitfield", "reality", RH, title_spelling="Sheree Whilfield"),
529: P("Tanya Bardsley", "reality", RH), 530: P("Teddi Jo Mellencamp", "reality", RH), 531: P("Teresa Giudice", "reality", RH),
532: P("Yolanda Hadid", "reality", RH),
533: P("Carson Kressley"), 534: P("RuPaul", "reality", "Drag Race", title_spelling="Ru Paul"),
535: P("Anne Hegerty", "tv", CH), 536: P("Jenny Ryan", "tv", CH), 537: P("Paul Sinha", "tv", CH), 538: P("Shaun Wallace", "tv", CH),
539: P("Frankie Essex"), 540: P("Jack Bennewith", note="brother of Diags"), 541: P("Michael Hassini"),
542: P("Nicole Kidman", "tv", BLL, character="Celeste Wright"), 543: P("Charlie Cox", "tv", DEF),
544: P("Finn Jones", "tv", "Iron Fist", character="Danny Rand"), 545: P("Finn Jones", "tv", DEF), 546: P("Krysten Ritter", "tv", DEF),
547: P("Shailene Woodley", "tv", BLL), 548: P("Tom Souter", "tv", "Car Chasers"),
549: P("Will Smith", "film", BBY), 550: P("Mike Lowrey", "film", BBY), 551: P("Alexander Ludwig", "film", BBY),
552: P("Charles Melton", "film", BBY), 553: P("Kate del Castillo", "film", BBY), 554: P("Isabel Aretas", "film", BBY),
555: P("Martin Lawrence", "film", BBY), 556: P("Paola Núñez", "film", BBY, title_spelling="PAOLA NUNEZ"), 557: P("Vanessa Hudgens", "film", BBY),
558: P("Chris Núñez", "reality", IM), 559: P("Cleen Rock", "reality", IM), 560: P("Dave Navarro", "reality", IM),
561: P("DJ Tambe", "reality", IM), 562: P("Oliver Peck", "reality", IM), 563: P("Ryan Ashley Malarkey", "reality", IM),
564: P("Alex", "tv", "Maid"), 565: P("Hank", "tv", "Maid"), 566: P("Maddy", "tv", "Maid"), 567: P("Nate", "tv", "Maid"),
568: P("Regina", "tv", "Maid"), 569: P("Sean", "tv", "Maid"),
570: P("Álvaro Morte", "tv", MH), 571: P("Darko Perić", "tv", MH), 572: P("Itziar Ituño", "tv", MH), 573: P("Rodrigo de la Serna", "tv", MH),
574: P("Úrsula Corberó", "tv", MH), 575: P("Denver", "tv", MH), 576: P("Marsella", "tv", MH), 577: P("Martín Berrote", "tv", MH),
578: P("Mónica Gaztambide", "tv", MH), 579: P("Nairobi", "tv", MH), 580: P("The Professor", "tv", MH, title_spelling="Professor"),
581: P("Rio", "tv", MH), 582: P("Tokyo", "tv", MH),
583: P("Ji-yeong", "tv", "Squid Game"),
584: P("Cal MacAninch", "tv", VIC), 585: P("James Harkness", "tv", VIC), 586: P("Jamie Sives", "tv", VIC), 587: P("John Scougall", "tv", VIC),
588: P("Karla Crome", "tv", VIC), 589: P("Kelly Macdonald", "tv", VIC), 590: P("Pooky Quesnel", "tv", VIC),
591: P("Carlos Torres", "tv", QF), 592: P("Carolina Ramírez", "tv", QF), 593: P("Guillermo Blanco", "tv", QF),
594: P("Juan Manuel Restrepo", "tv", QF), 595: P("Lucho Velasco", "tv", QF), 596: P("Mabel Moreno", "tv", QF),
597: P("Maria Jose Vargas", "tv", QF), 598: P("Mariana Garzón", "tv", QF),
599: K(["The Queen", "Prince Philip", "Kate", "William", "Harry", "Charles", "Camilla", "Meghan"], 8, cat="royal", title_spelling="Phillip"),
600: P("Kevin", "film", "Kevin & Perry"), 601: P("Perry", "film", "Kevin & Perry"), 602: P("Perry", "film", "Kevin & Perry"),
603: P("Touker Suleyman", "tv", DD), 604: P("Bethany England", "football"),
605: P("Bob Odenkirk", "tv", BCS), 606: P("Jonathan Banks", "tv", BCS), 607: P("Rhea Seehorn", "tv", BCS),
608: P("Joe Lo Truglio", "tv", "Brooklyn Nine-Nine"), 609: P("Marc Evan Jackson", "tv", "Brooklyn Nine-Nine", title_spelling="Marc Evans Jackson"),
610: P("Annalisa Cochrane", "tv", CK, title_spelling="Annalise Cochrane"), 611: P("Courtney Henggeler", "tv", CK),
612: P("Griffin Santopietro", "tv", CK), 613: P("Jacob Bertrand", "tv", CK), 614: P("Joe Seo", "tv", CK), 615: P("Martin Kove", "tv", CK),
616: P("Mary Mouser", "tv", CK), 617: P("Pat Morita", "tv", CK), 618: P("Peyton List", "tv", CK), 619: P("Ralph Macchio", "tv", CK),
620: P("Tanner Buchanan", "tv", CK, title_spelling="Tanner Buchanon"), 621: P("Thomas Ian Griffith", "tv", CK), 622: P("William Zabka", "tv", CK),
623: P("Xolo Maridueña", "tv", CK),
624: P("Anya Taylor-Joy", "tv", DC), 625: P("Jason Isaacs", "tv", DC), 626: P("Nathalie Emmanuel", "tv", DC),
627: P("Dylan Llewellyn", "tv", DG), 628: P("Jamie-Lee O'Donnell", "tv", DG), 629: P("Louisa Harland", "tv", DG, title_spelling="Louise Harland"),
630: P("Nicola Coughlan", "tv", DG), 631: P("Saoirse-Monica Jackson", "tv", DG),
632: P("Ashley Park", "tv", EIP), 633: P("Bruno Gouery", "tv", EIP), 634: P("Camille Razat", "tv", EIP), 635: P("Lily Collins", "tv", EIP),
636: P("Lucas Bravo", "tv", EIP), 637: P("Lucien Laviscount", "tv", EIP), 638: P("Philippine Leroy-Beaulieu", "tv", EIP),
639: P("Samuel Arnold", "tv", EIP),
})
