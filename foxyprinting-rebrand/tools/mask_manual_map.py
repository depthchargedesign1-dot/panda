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

JTV = "Jane the Virgin"; JP = "Jurassic Park"; TGM = "Top Gun: Maverick"; OITNB = "Orange Is the New Black"; OFF = "The Office"
GG = "The Golden Girls"; SG = "Still Game"; FNAF = "Five Nights at Freddy's"; DAD = "Dumb and Dumber"; LB = "Little Britain"


def CP(a, b):  # couple pack
    return K([a, b], 2, note="couple")


D.update({
640: P("William Abadie", "tv", EIP),
641: P("Andrea Navedo", "tv", JTV), 642: P("Gina Rodriguez", "tv", JTV), 643: P("Ivonne Coll", "tv", JTV), 644: P("Jaime Camil", "tv", JTV),
645: P("Justin Baldoni", "tv", JTV), 646: P("Yael Grobglas", "tv", JTV),
647: P("Ariana Richards", "film", JP), 648: P("BD Wong", "film", JP), 649: P("Joseph Mazzello", "film", JP, title_spelling="Joseph Mazzallo"),
650: P("Laura Dern", "film", JP), 651: P("Richard Attenborough", "film", JP), 652: P("Wayne Knight", "film", JP),
653: P("Antony Starr", "tv", "The Boys", title_spelling="Anthony Star"),
654: P("Glen Powell", "film", TGM), 655: P("Jay Ellis", "film", TGM), 656: P("Lewis Pullman", "film", TGM), 657: P("Miles Teller", "film", TGM),
658: P("Monica Barbaro", "film", TGM),
659: P("B.J. Novak", "tv", OFF, character="Ryan Bailey Howard"),
660: P("José María Yazpik", "tv", "Narcos", title_spelling="Jose Maria Yazpik"), 661: P("Michael Peña", "tv", "Narcos"),
662: P("Jason Biggs", "tv", OITNB), 663: P("Kate Mulgrew", "tv", OITNB), 664: P("Laura Prepon", "tv", OITNB), 665: P("Michelle Hurst", "tv", OITNB),
666: P("King Charles III", "royal", note="on sticks"),
667: K([], 6, FR, "tv"),
668: P("King Charles III", "royal", note="Coronation 2023"),
669: P("Jesy Nelson", "music"),
670: K([], 5, cat="music", group="One Direction"),
671: P("Kate Middleton", "royal", title_spelling="Princess Kate Middleton"), 672: P("Camilla Parker Bowles", "royal"),
673: K([], 8, cat="royal", note="Royal Family Coronation 2023"),
674: P("Cooper", "tv", "The Farm"), 675: P("Kaleb", "tv", "The Farm"),
676: K(["Jeremy Clarkson", "Kaleb Cooper"], 3, "The Farm", "tv", note="3-pack; title names only these"),
677: P("Lloyd", "film", DAD), 678: P("Harry", "film", DAD), 679: K([], None, DAD, "film"),
680: P("King Charles III", "royal", note="with crown masks"),
681: K(["King Charles III"], 5, cat="royal", note="5 of the same mask + crowns"),
682: K(["King Charles III"], 12, cat="royal", note="12 of the same mask"),
683: P("Queen Camilla", "royal"), 684: K(["Queen Camilla"], 10, cat="royal", note="10 of the same mask"),
685: K([], 5, cat="music", group="Spice Girls"),
686: P("21 Savage", "music"), 687: P("070 Shake", "music"), 688: P("Raye", "music"), 689: P("Raye", "music"), 690: P("Rema", "music"),
691: P("Sinach", "music"), 692: P("SZA", "music"), 693: P("Venbee", "music"),
694: P("Lou", "comedy", LB), 695: K([], 3, LB, "comedy"),
696: K([], 7, "Ryder Cup", "golf", note="European team 2023"),
697: C(note="personalised face beach towel (male)"), 698: C(note="personalised face beach towel (female)"), 699: C(note="personalised celebrity face beach towel"),
700: K(["Francis Ngannou", "Tyson Fury"], 2, cat="boxing", title_spelling="Francis Nganou"),
701: K([], None, cat="music", group="Tenacious D"),
702: K([], None, note="'Queen' pack - band or royal not clear from title"),
703: P("Axl Rose", "music", band="Guns N' Roses"), 704: K([], 3, LB, "comedy"),
705: G("Beavis", "Beavis and Butt-Head"), 706: G("Butt-Head", "Beavis and Butt-Head"),
707: K([], 9, "Ryder Cup", "golf", note="American team 2023"),
708: G("Foxy", FNAF), 709: G("Bonnie", FNAF), 710: G("Chica", FNAF), 711: G("Freddy Fazbear", FNAF), 712: G("Golden Freddy", FNAF),
713: G("The Marionette", FNAF), 714: G("Springtrap", FNAF),
715: P("Mackenyu", "tv", "One Piece", character="Roronoa Zoro"), 716: P("Iñaki Godoy", "tv", "One Piece", character="Monkey D. Luffy"),
717: K([], None, "One Piece", "tv", note="Straw Hat crew"),
718: P("John Krasinski", "tv", OFF, character="Jim"), 719: P("Leslie David Baker", "tv", OFF, character="Stanley"),
720: P("Rainn Wilson", "tv", OFF, character="Dwight"),
721: P("Lord Alan Sugar"), 722: P("Sacha Baron Cohen", character="Borat"), 723: U("Wham - band name; single mask or pack?"),
724: P("Emma Watson", "film", "Beauty and the Beast"), 725: P("Baby", "film", "Dirty Dancing"), 726: G("Barbie", "Barbie"),
727: P("Blanche", "tv", GG), 728: P("Anthony Stewart Head", "tv", "Buffy the Vampire Slayer", character="Giles"),
729: P("Dorothy", "tv", GG), 730: P("Rose", "tv", GG), 731: P("Sophia", "tv", GG), 732: P("Chris Packham"),
733: P("Edith", "tv", SG),
734: P("Hafþór Júlíus Björnsson", "tv", "Game of Thrones", character="The Mountain", title_spelling="Hafbor Julius Thor Bjornsson"),
735: P("Jennifer Grey", character="Baby"), 736: G("Morty", "Rick and Morty"),
737: P("Roger Lloyd-Pack", "tv", OFAH, character="Trigger"), 738: P("José de Sousa", "darts"),
739: P("Leonardo DiCaprio", "film", "Django Unchained", note="laughing meme"),
740: P("Kiefer Sutherland", "film", "The Lost Boys", character="David", title_spelling="Keifer Sutherland"),
741: P("Zoe Saldaña", title_spelling="Zoey Saldaña"), 742: P("Isa", "tv", SG), 743: P("Liam", "tv", "Benidorm"), 744: P("Mateo", "tv", "Benidorm"),
745: G("Imperial Stormtrooper", "Star Wars"),
746: CP("Adam Brody", "Leighton Meester"), 747: CP("Alicia Keys", "Swizz Beatz") | {"title_spelling": "Swiss Beatz"},
748: CP("Beyoncé", "Jay-Z"), 749: CP("Blake Lively", "Ryan Reynolds"), 750: CP("Brad Takei", "George Takei"),
751: CP("Chrissy Teigen", "John Legend"), 752: CP("Cynthia Nixon", "Christine Marinoni"), 753: CP("Dax Shepard", "Kristen Bell"),
754: CP("Denzel Washington", "Pauletta Washington"), 755: CP("Elton John", "David Furnish"), 756: CP("Emily Blunt", "John Krasinski"),
757: CP("Enrique Iglesias", "Anna Kournikova"), 758: CP("Freddie Prinze Jr.", "Sarah Michelle Gellar"), 759: CP("Goldie Hawn", "Kurt Russell"),
760: CP("Harrison Ford", "Calista Flockhart"), 761: CP("Jason Momoa", "Lisa Bonet"), 762: CP("Judd Apatow", "Leslie Mann"),
763: CP("Julia Louis-Dreyfus", "Brad Hall"), 764: CP("Julia Roberts", "Danny Moder"), 765: CP("Justin Mikita", "Jesse Tyler Ferguson"),
766: CP("Kevin Bacon", "Kyra Sedgwick"), 767: CP("Lance Bass", "Michael Turchin"), 768: CP("LeBron James", "Savannah Brinson"),
769: CP("Lily Tomlin", "Jane Wagner"), 770: CP("Mark Consuelos", "Kelly Ripa"), 771: CP("Matthew Broderick", "Sarah Jessica Parker"),
772: CP("Matthew McConaughey", "Camila Alves"), 773: CP("Maya Rudolph", "Paul Thomas Anderson"), 774: CP("Melissa McCarthy", "Ben Falcone"),
775: CP("Neil Patrick Harris", "David Burtka"), 776: CP("Oprah Winfrey", "Stedman Graham"), 777: CP("Penélope Cruz", "Javier Bardem"),
778: CP("Pink", "Carey Hart"), 779: CP("RuPaul", "Georges LeBar"), 780: CP("Sarah Paulson", "Holland Taylor"), 781: CP("Seth Rogen", "Lauren Miller"),
782: CP("Steve Carell", "Nancy Walls"), 783: CP("Thandie Newton", "Ol Parker"), 784: CP("Tim McGraw", "Faith Hill"),
785: CP("Tom Brady", "Gisele Bündchen") | {"title_spelling": "Gisele Bundchen"}, 786: CP("Tom Hanks", "Rita Wilson"),
787: CP("Victoria Beckham", "David Beckham"), 788: CP("Viola Davis", "Julius Tennon"), 789: CP("Will Smith", "Jada Pinkett Smith"),
790: CP("Angelina Jolie", "Brad Pitt"), 791: CP("Ashton Kutcher", "Mila Kunis"), 792: CP("Ben Affleck", "Jennifer Lopez"),
793: CP("Chris Brown", "Rihanna"), 794: CP("Ellen DeGeneres", "Portia de Rossi"), 795: CP("Gwen Stefani", "Blake Shelton"),
796: CP("Iman", "David Bowie"), 797: CP("Jesse Plemons", "Kirsten Dunst"), 798: CP("John F. Kennedy Jr.", "Carolyn Bessette Kennedy"),
799: CP("Justin Bieber", "Hailey Bieber"), 800: CP("Kim Kardashian", "Kanye"), 801: CP("Leslie Mann", "Judd Apatow"),
802: CP("Matthew McConaughey", "Sarah Jessica Parker"), 803: CP("Meghan Markle", "Prince Harry"), 804: CP("Michelle Obama", "Barack Obama"),
805: CP("Nicole Kidman", "Keith Urban"), 806: CP("Prince William", "Catherine Middleton"), 807: CP("Priyanka Chopra", "Nick Jonas"),
808: CP("Ryan Gosling", "Eva Mendes"), 809: CP("Sarah Hyland", "Wells Adams"), 810: CP("Savannah Brinson", "LeBron James"),
811: CP("Sue Bird", "Megan Rapinoe"), 812: CP("Tom Holland", "Zendaya"), 813: CP("Tracy Pollan", "Michael J. Fox"),
814: P("Kôji Yakusho", "film"), 815: P("Mahershala Ali", "film"), 816: P("Michael Peña", "film"), 817: P("Timothée Chalamet", "film"),
818: P("Kôji Yakusho", "film"), 819: P("Michael Peña", "film"), 820: P("Timothée Chalamet", "film", "Wonka"), 821: P("Xolo Maridueña", "film"),
822: P("Cara De La Hoyde", "reality", LI), 823: P("Chloë Crowhurst", "reality", LI),
824: P("Ekin-Su Cülcüloğlu", "reality", LI, title_spelling="Ekinsu Cülcüloglu"), 825: P("Jessica Shears", "reality", LI),
826: P("Sophie Piper", "reality", LI), 827: P("Tom Powell", "reality", LI),
828: P("Malin Åkerman", "tv", "Eurovision", title_spelling="Malin åkerman"),
829: K([], None, "Eurovision", "music", note="2024 super pack"), 830: K([], None, "Eurovision", "music", note="2024 pack 1"),
831: K([], None, "Eurovision", "music", note="2024 pack 2"),
832: K([], None, cat="music", group="ABBA"),
833: P("Marc Guéhi", "football"), 834: P("Paul Gascoigne", note="'96 blond, 'Gazza'"),
835: K(["Foden", "Gazza"], 2, cat="football", note="England Euros blonde pack"),
836: K([], None, cat="football", note="England Euros 2024 pack 3"), 837: K([], None, cat="football", note="England Euros 2024 pack 2"),
838: K([], None, cat="football", note="England Euros 2024 pack 1"), 839: K([], None, cat="football", note="England Euros 2024 pack 4"),
840: P("Jayne Torvill"), 841: P("Christopher Dean"), 842: P("Tam", "tv", SG),
843: P("Michael Keaton", "film", "Beetlejuice"), 844: P("Sarah Connor", "film", "The Terminator"),
845: P("Aragorn", "film", "The Lord of the Rings"), 846: G("Gromit", "Wallace & Gromit", title_spelling="Grommit"),
847: G("Jigsaw puppet", "Saw"), 848: P("Jim Carrey", "film", "The Mask", note="Mask of Loki"),
849: P("Slash", "music", band="Guns N' Roses"), 850: G("Zippy", "Rainbow"),
851: P("Adil C", "music"), 852: P("Ayo Sk3tch", "music"), 853: P("Britti", "music"), 854: P("DNorri", "music"), 855: P("Sekou", "music"),
856: P("Eiza González", "tv", "3 Body Problem", character="Auggie Salazar"),
857: P("Noémie Schmidt"), 858: P("Aitana Sánchez-Gijón"), 859: P("Blanca Suárez"), 860: P("Magdalena Dębicka"), 861: P("Chino Darín"),
862: P("Eduard Fernández"), 863: P("Sergi López"), 864: P("Michael Keaton", "film", "Beetlejuice", note="2024"),
865: G("Deadpool", "Deadpool"), 866: P("Zendaya", "film", "Dune", character="Chani"),
867: P("Colin Farrell", "tv", "The Penguin", title_spelling="Collin Farrell"), 868: P("Zoë Kravitz", character="Catwoman"), 869: P("Zoë Kravitz"),
870: P("Abigail Morris", note="The Last Dinner Party"), 871: P("Charli XCX", title_spelling="Charlie XCX"), 872: P("Naoya", "boxing"),
873: P("Endrick", "football"), 874: P("Gavi", "football"), 875: P("Pedri", "football"),
876: P("Dricus du Plessis", "sport", note="'Stillknocks'"), 877: P("Chico", "music", XF), 878: U("Future - reads as a word"), 879: P("Gunna"),
})

AAA = "Agatha All Along"; BR = "Baby Reindeer"; TPC = "The Perfect Couple"; SAB = "Shadow and Bone"

D.update({
880: P("Hozier"), 881: P("Latto"), 882: P("Marc Guéhi", "football"), 883: P("Iga Świątek", "tennis"),
884: P("21 Savage"), 885: P("Akon"), 886: P("Alex Rodriguez", note="A-Rod"), 887: P("Biggie"), 888: P("Beyoncé", title_spelling="Beyonce"),
889: U("Clara - first name only"), 890: P("DaBaby"), 891: P("Drake"), 892: P("Draya"), 893: P("Druski"), 894: P("Eminem"),
895: U("Fabulous - reads as a word"), 896: P("Giggs"), 897: P("GloRilla", title_spelling="Glorilla"), 898: P("Jhené Aiko"),
899: P("Ali Ahn", "tv", AAA), 900: P("Aubrey Plaza", "tv", AAA), 901: P("Debra Jo Rupp", "tv", AAA, title_spelling="Debra Joe Rupp"),
902: P("Joe Locke", "tv", AAA), 903: P("Kathryn Hahn", "tv", AAA), 904: P("Patti LuPone", "tv", AAA), 905: P("Sasheer Zamata", "tv", AAA),
906: P("Jess Gunning", "tv", BR), 907: P("Nava Mau", "tv", BR), 908: P("Nina Sosanya", "tv", BR), 909: P("Richard Gadd", "tv", BR),
910: P("Shalom Brune-Franklin", "tv", BR), 911: P("Tom Goodman-Hill", "tv", BR),
912: P("Emma Myers", "tv", "Wednesday", character="Enid Sinclair"), 913: P("Luis Guzmán", "tv", "Wednesday", character="Gomez Addams"),
914: P("Bill Camp", "tv", TPC), 915: P("Billy Howle", "tv", TPC), 916: P("Dakota Fanning", "tv", TPC), 917: P("Eve Hewson", "tv", TPC),
918: P("Isabelle Adjani", "tv", TPC), 919: P("Ishaan Khatter", "tv", TPC), 920: P("Jack Reynor", "tv", TPC), 921: P("Liev Schreiber", "tv", TPC),
922: P("Meghann Fahy", "tv", TPC), 923: P("Michael Beach", "tv", TPC), 924: P("Nicole Kidman", "tv", TPC),
925: P("Quavo"), 926: P("Raye"), 927: P("Rosalía", title_spelling="Rosalia"), 928: P("Saweetie"), 929: P("SZA"), 930: P("Tyla"),
931: P("YG", "music"), 932: P("Columbo"),
933: CP("Adam Brody", "Leighton Meester"), 934: CP("Alicia Keys", "Swizz Beatz") | {"title_spelling": "Swiss Beatz"},
935: CP("Beyoncé", "Jay-Z"), 936: CP("Blake Lively", "Ryan Reynolds"), 937: CP("Brad Takei", "George Takei"),
938: CP("Chrissy Teigen", "John Legend"), 939: CP("Cynthia Nixon", "Christine Marinoni"), 940: CP("Dax Shepard", "Kristen Bell"),
941: CP("Denzel Washington", "Pauletta Washington"), 942: CP("Elton John", "David Furnish"), 943: CP("Emily Blunt", "John Krasinski"),
944: CP("Enrique Iglesias", "Anna Kournikova"), 945: CP("Freddie Prinze Jr.", "Sarah Michelle Gellar"), 946: CP("Goldie Hawn", "Kurt Russell"),
947: CP("Harrison Ford", "Calista Flockhart"), 948: CP("Jason Momoa", "Lisa Bonet"), 949: CP("Judd Apatow", "Leslie Mann"),
950: CP("Julia Louis-Dreyfus", "Brad Hall"), 951: CP("Julia Roberts", "Danny Moder"), 952: CP("Justin Mikita", "Jesse Tyler Ferguson"),
953: CP("Kevin Bacon", "Kyra Sedgwick"), 954: CP("Lance Bass", "Michael Turchin"), 955: CP("LeBron James", "Savannah Brinson"),
956: CP("Lily Tomlin", "Jane Wagner"), 957: CP("Mark Consuelos", "Kelly Ripa"), 958: CP("Matthew Broderick", "Sarah Jessica Parker"),
959: CP("Matthew McConaughey", "Camila Alves"), 960: CP("Maya Rudolph", "Paul Thomas Anderson"), 961: CP("Melissa McCarthy", "Ben Falcone"),
962: CP("Neil Patrick Harris", "David Burtka"), 963: CP("Oprah Winfrey", "Stedman Graham"), 964: CP("Penélope Cruz", "Javier Bardem"),
965: CP("Pink", "Carey Hart"), 966: CP("RuPaul", "Georges LeBar"), 967: CP("Sarah Paulson", "Holland Taylor"), 968: CP("Seth Rogen", "Lauren Miller"),
969: CP("Steve Carell", "Nancy Walls"), 970: CP("Thandie Newton", "Ol Parker"), 971: CP("Tim McGraw", "Faith Hill"),
972: CP("Tom Brady", "Gisele Bündchen") | {"title_spelling": "Gisele Bundchen"}, 973: CP("Tom Hanks", "Rita Wilson"),
974: CP("Victoria Beckham", "David Beckham"), 975: CP("Viola Davis", "Julius Tennon"), 976: CP("Will Smith", "Jada Pinkett Smith"),
977: CP("Geri Horner", "Christian Horner") | {"title_spelling": "Gerry Corner", "note": "couple; title says 'Gerry Corner' - check"},
978: K(["Jake Gyllenhaal", "Conor McGregor"], 2, "Road House", "film", note="couple pack"),
979: CP("Mark Zuckerberg", "Priscilla Chan"),
980: CP("Angelina Jolie", "Brad Pitt"), 981: CP("Ashton Kutcher", "Mila Kunis"), 982: CP("Ben Affleck", "Jennifer Lopez"),
983: CP("Chris Brown", "Rihanna"), 984: CP("Ellen DeGeneres", "Portia de Rossi"), 985: CP("Gwen Stefani", "Blake Shelton"),
986: CP("Iman", "David Bowie"), 987: CP("Jesse Plemons", "Kirsten Dunst"), 988: CP("John F. Kennedy Jr.", "Carolyn Bessette Kennedy"),
989: CP("Justin Bieber", "Hailey Bieber"), 990: CP("Kim Kardashian", "Ye"), 991: CP("Leslie Mann", "Judd Apatow"),
992: CP("Meghan Markle", "Prince Harry"), 993: CP("Michelle Obama", "Barack Obama"), 994: CP("Nicole Kidman", "Keith Urban"),
995: CP("Prince William", "Catherine Middleton"), 996: CP("Priyanka Chopra", "Nick Jonas"), 997: CP("Ryan Gosling", "Eva Mendes"),
998: CP("Sarah Hyland", "Wells Adams"), 999: CP("Savannah Brinson", "LeBron James"), 1000: CP("Sue Bird", "Megan Rapinoe"),
1001: CP("Tom Holland", "Zendaya"), 1002: CP("Tracy Pollan", "Michael J. Fox"),
1003: P("Dawn Sutcliffe", "tv", "Gavin & Stacey"),
1004: P("Pete Sutcliffe", "tv", "Gavin & Stacey", title_spelling="Peter Sutcliffe", note="character; avoid 'Peter Sutcliffe' (shares a notorious real name)"),
1005: P("Toby Jones", "tv", "Mr Bates vs The Post Office", character="Alan Bates"),
1006: U("Camille - first name only", category="film"), 1007: P("Karla Sofía Gascón", "film", title_spelling="Karla Sofía Gascon"),
1008: P("Sofía Vergara", "film"), 1009: P("Zendaya", "film"),
1010: P("Michael Peña", "tv", "Narcos"), 1011: P("21 Savage"), 1012: P("Arrdee"), 1013: P("Joji"),
1014: P("Amita Suman", "tv", SAB), 1015: P("Archie Renaux", "tv", SAB), 1016: P("Kit Young", "tv", SAB), 1017: P("Ben Barnes", "tv", SAB),
1018: P("Zoë Wanamaker", "tv", SAB, title_spelling="Zoe Wanamaker"), 1019: P("Jessie Mei Li", "tv", SAB),
1020: G("Vecna", "Stranger Things"), 1021: P("Dave", "tv", "Top Boy"), 1022: P("Kano", "tv", "Top Boy"),
1023: P("David Castañeda", "tv", "The Umbrella Academy"), 1024: P("Moisés Arias", "tv", "Fallout"),
1025: G("Cecil", "Invincible"), 1026: G("Mark", "Invincible"),
1027: P("Akon"), 1028: P("A-Rod"), 1029: P("Beyoncé", title_spelling="Beyonce"), 1030: P("JT", "music", note="City Girls"),
1031: P("DaBaby", title_spelling="Dababy"), 1032: P("Drake"), 1033: P("Druski"), 1034: P("Eminem"), 1035: P("Fabolous"),
1036: P("Giggs"), 1037: P("GloRilla", title_spelling="Glorilla"), 1038: P("Jhené Aiko"), 1039: P("Lizzo"),
})

GOL = "Gangs of London"; FB = "football"


def KP(name, group):
    return P(name, "music", group=group)


D.update({
1040: P("Maluma"), 1041: P("Mase"), 1042: P("MGK"), 1043: P("Ne-Yo"), 1044: P("Obama"), 1045: P("Offset"),
1046: P("Oprah", title_spelling="Oprah C"), 1047: P("Rihanna"), 1048: P("Safaree"), 1049: P("Saweetie"), 1050: P("Shaq"),
1051: P("Timbaland"), 1052: P("Trump"),
1053: P("Giant", "tv", "Gladiators"), 1054: P("Sabre", "tv", "Gladiators"),
1055: P("Koba", "tv", GOL), 1056: P("Lale", "tv", GOL), 1057: P("Merwan", "tv", GOL),
1058: P("Gunther", "sport", "WWE"), 1059: P("Naomi", "sport", "WWE"), 1060: P("Penta", "sport", "WWE"), 1061: P("Sheamus", "sport", "WWE"),
1062: G("The Grabber", "The Black Phone", note="'Silent' design"), 1063: G("The Grabber", "The Black Phone", note="'Frown' design"),
1064: G("The Grabber", "The Black Phone", note="'Grin' design"),
1065: P("DanTDM", title_spelling="Dan TDM"), 1066: P("Oliver Bearman", "f1", note="sunglasses and cap"),
1067: P("Gabriel Magalhães", FB), 1068: P("Viktor Gyökeres", FB), 1069: P("Emiliano Martínez", FB), 1070: P("Evanilson", FB),
1071: P("Fabian Hürzeler", FB), 1072: P("Jan Paul van Hecke", FB), 1073: P("Pascal Groß", FB), 1074: P("Enzo Fernández", FB),
1075: P("João Pedro", FB), 1076: P("Moisés Caicedo", FB), 1077: P("Daniel Muñoz", FB), 1078: P("Ismaïla Sarr", FB),
1079: P("Jørgen Strand Larsen", FB), 1080: P("Raúl Jiménez", FB), 1081: P("Saša Lukić", FB), 1082: P("Ibrahima Konaté", FB),
1083: P("Jérémy Doku", FB), 1084: P("Joško Gvardiol", FB), 1085: P("Marc Guéhi", FB), 1086: P("Rayan Aït-Nouri", FB),
1087: P("Rodri", FB), 1088: P("Rúben Dias", FB), 1089: P("Benjamin Šeško", FB), 1090: P("Casemiro", FB),
1091: P("Bruno Guimarães", FB), 1092: P("Fabian Schär", FB), 1093: P("Joelinton", FB), 1094: P("André", FB), 1095: P("André", FB),
1096: P("João Gomes", FB), 1097: P("José Sá", FB), 1098: P("Ladislav Krejčí", FB), 1099: P("Matheus Mané", FB),
1100: P("Hide the Pain Harold", note="meme"), 1101: P("KSI"), 1102: P("Logan Paul", note="black eye"),
1103: P("Mrwhosetheboss", title_spelling="Mr Whose The Boss"), 1104: P("PewDiePie"), 1105: P("Vikkstar"),
1106: P("Fabien Galthié", "rugby"), 1107: P("Mickaël Guillard", "rugby"), 1108: P("Oscar Jégou", "rugby"),
1109: P("Josh van der Flier", "rugby"), 1110: P("Gonzalo Quesada", "rugby"), 1111: P("Duhan van der Merwe", "rugby"),
1112: K([], None, cat="rugby", note="Ireland Six Nations players & coach"), 1113: K([], None, cat="rugby", note="England Six Nations players & coach"),
1114: K([], None, cat="rugby", note="France Six Nations players & coach"), 1115: K([], None, cat="rugby", note="Italy Six Nations players & coach"),
1116: K([], None, cat="rugby", note="Scotland Six Nations players & coach"), 1117: K([], None, cat="rugby", note="Wales Six Nations players & coach"),
1118: U("Gymskin - not clear if a person"),
1119: P("A-Train", "tv"), 1120: P("Firecracker", "tv"), 1121: P("Homelander", "tv"), 1122: P("Hughie", "tv"), 1123: P("Ryan", "tv"),
1124: P("Starlight", "tv"),
1125: K([], 6, cat=FB, note="Belgium football legends"), 1126: K([], 6, cat=FB, note="Brazil football legends"),
1127: K([], 6, cat=FB, note="England football legends"), 1128: K([], 6, cat=FB, note="France football legends"),
1129: K([], 6, cat=FB, note="Germany football legends"), 1130: K([], 6, cat=FB, note="football legends"),
1131: K([], 6, cat=FB, note="Netherlands football stars"), 1132: K([], 6, cat=FB, note="Portugal football stars"),
1133: K([], 6, cat=FB, note="Senegal football stars"), 1134: K([], 6, cat=FB, note="Spain football stars"),
1135: P("Gabriel Magalhães", FB), 1136: P("Marc Guéhi", FB), 1137: P("Jules Koundé", FB), 1138: P("Kylian Mbappé", FB),
1139: P("Antonio Rüdiger", FB), 1140: P("Leroy Sané", FB), 1141: P("Micky van de Ven"), 1142: P("Roberto Martínez", FB),
1143: P("Sadio Mané", FB), 1144: P("Luis de la Fuente", FB), 1145: P("Pau Cubarsí", FB), 1146: P("Sergiño Dest", FB),
1147: C(pack_size=5, category=FB, note="pick any 5 football masks"), 1148: C(pack_size=10, category=FB, note="pick any 10 football masks"),
1149: K([], 6, cat=FB, note="Scotland players & manager"),
1150: KP("Hoshi", "SEVENTEEN"), 1151: KP("Jay", "ENHYPEN"), 1152: KP("Seungkwan", "SEVENTEEN"), 1153: KP("Soobin", "TXT"),
1154: KP("Sunoo", "ENHYPEN"), 1155: KP("Taehyun", "TXT"), 1156: KP("Jiung", "P1Harmony"), 1157: KP("Jungwon", "ENHYPEN"),
1158: KP("Lisa", "BLACKPINK"), 1159: KP("Mingyu", "SEVENTEEN"), 1160: KP("Rosé", "BLACKPINK"), 1161: KP("Sunghoon", "ENHYPEN"),
1162: KP("Woozi", "SEVENTEEN"), 1163: KP("Yoonchae", "KATSEYE"), 1164: KP("DK", "SEVENTEEN"), 1165: KP("Jake", "ENHYPEN"),
1166: KP("Jongseob", "P1Harmony"), 1167: KP("Megan", "KATSEYE"), 1168: KP("Ni-ki", "ENHYPEN"), 1169: KP("S.Coups", "SEVENTEEN"),
1170: KP("Jun", "SEVENTEEN"), 1171: KP("Wonwoo", "SEVENTEEN"), 1172: KP("Jennie", "BLACKPINK"), 1173: KP("Kazuha", "LE SSERAFIM"),
1174: KP("Keeho", "P1Harmony"), 1175: KP("Lara", "KATSEYE"), 1176: KP("Manon", "KATSEYE"), 1177: KP("Sophia", "KATSEYE"),
1178: KP("Soul", "P1Harmony"), 1179: KP("Beomgyu", "TXT"), 1180: KP("Daniela", "KATSEYE"), 1181: KP("Evan", "ENHYPEN"),
1182: KP("Hongjoong", "ATEEZ"), 1183: KP("Intak", "P1Harmony"), 1184: KP("Jisoo", "BLACKPINK"), 1185: KP("San", "ATEEZ"),
1186: KP("The8", "SEVENTEEN"), 1187: KP("Theo", "P1Harmony"), 1188: KP("Wooyoung", "ATEEZ"), 1189: KP("Yeonjun", "TXT"),
1190: KP("Seonghwa", "ATEEZ"), 1191: KP("Vernon", "SEVENTEEN"),
1192: P("Eumaeus"), 1193: P("Odysseus"), 1194: P("Telemachus"),
1195: G("Halloween masks", pack_size=5, note="set of 5"),
})

# second thoughts on single-word stage names: the title itself makes the person clear
D[895] = P("Fabolous", title_spelling="Fabulous", note="spelling from sister listing 'Fabolous - John David Jackson'")
D[878] = P("Future")


def main():
    rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
    missing = [i for i in range(len(rows)) if i not in D]
    extra = [i for i in D if i >= len(rows)]
    assert not missing and not extra, (missing, extra)
    out = {}
    for i, r in enumerate(rows):
        d = dict(D[i])
        d["title"] = r["Title"]
        assert r["Handle"] not in out, r["Handle"]
        out[r["Handle"]] = d
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    c = collections.Counter(v["type"] for v in out.values())
    print(len(out), dict(c))
    print(collections.Counter(v.get("category") for v in out.values() if v["type"] == "person"))


if __name__ == "__main__":
    main()
