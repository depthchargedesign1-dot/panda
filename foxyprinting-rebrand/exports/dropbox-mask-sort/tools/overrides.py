"""Manual decisions for the mask sort (phase 1).

OVERRIDE : normalised base key (tools/norm.py) -> (person, category, sport, show/reason)
KEY_CAT  : master-list key -> (category, sport) to re-file people the 2 Oct master list put under
           "other" (or sport "other")
SENSITIVE: people whose masks the owner should confirm before they go into the clean set

Categories: tv, reality, film, music, football, sport, comedy, politics, royal, models, bollywood,
characters, kids, pack, business, online, novelty, unsure, leave.
"""

OVERRIDE = {
    # not masks / working files
    "daveswiftlambretta2snoodmockup": ("Dave Swift", "leave", "", "Lambretta snood product mockup, not a face mask"),
    "daveswiftlambretta2mockup": ("Dave Swift", "leave", "", "Lambretta product mockup, not a face mask"),
    "daveswiftlambrettaredworkwearbundle": ("Dave Swift", "leave", "", "Lambretta clothing artwork, not a face mask"),
    "daveswiftlambrettahoodyandjacketfrontblack": ("Dave Swift", "leave", "", "Lambretta clothing artwork, not a face mask"),
    "depthchargedesignfacemasks": ("Depth Charge Design", "leave", "", "company branding image, not a face mask"),
    "staghenheader": ("", "leave", "", "website header graphic"),
    "stylestrokelauncheventarrivals8gdkvflj7akl": ("", "unsure", "", "press-agency photo name; open it to see who it is"),
    # packs
    "thegrabber3pack": ("The Grabber 3 pack", "pack"),
    "tenaciousdpack": ("Tenacious D pack", "pack"),
    "musicpackof": ("Music pack of 8", "pack"),
    # people the master list missed
    "carolebaskintigerking": ("Carole Baskin", "reality", "", "Tiger King"),
    "carolebaskin": ("Carole Baskin", "reality", "", "Tiger King"),
    "exoticjoe": ("Joe Exotic", "reality", "", "Tiger King"),
    "roseanneparkroseblackpink": ("Rosé (Blackpink)", "music"),
    "victorvaldesbarcelona": ("Víctor Valdés", "football"),
    "scottmillsmusic": ("Scott Mills", "tv"),
    "gunthersteinertheaustriangrandprix": ("Günther Steiner", "sport", "f1"),
    "oscarisaacwars": ("Oscar Isaac", "film", "", "Star Wars"),
    "oscarisaacstarwars": ("Oscar Isaac", "film", "", "Star Wars"),
    "oldsarahconnortheterminator": ("Linda Hamilton (Sarah Connor)", "film", "", "The Terminator"),
    "harrystylesbg": ("Harry Styles", "music"),
    "higuainargentina": ("Gonzalo Higuaín", "football"),
    "gotze": ("Mario Götze", "football"),
    "zoeysaldana": ("Zoe Saldaña", "film"),
    "jessicaparemegandraper": ("Jessica Paré", "tv", "", "Mad Men"),
    "kushidubey": ("Kushi Dubey", "bollywood"),
    "dharmendradeol": ("Dharmendra", "bollywood"),
    "whiteanimalmoomintrollmoominssnufkinmoominmammamoominpappabokchoymiscellaneouswhitemammal": ("Moomin", "kids"),
    "moomintrollmoominsartmoominwhitefoodcartoon": ("Moomin", "kids"),
    "gamoramarvelguardiansofthegalaxybuystarmasksatstarstills": ("Gamora (Zoe Saldaña)", "film", "", "Guardians of the Galaxy"),
    "draxmarvelguardiansofthegalaxybuystarmasksatstarstills": ("Drax (Dave Bautista)", "film", "", "Guardians of the Galaxy"),
}

_O = "other"
KEY_CAT = {
    # sport "other" -> a real sport folder
    "katherinegrainger": ("sport", "olympic"), "gemmagibbonssport": ("sport", "olympic"),
    "michaelphelpsrio": ("sport", "olympic"), "michaelphelpsrioolympics": ("sport", "olympic"), "michaelphelps": ("sport", "olympic"),
    "shaunwhite": ("sport", "olympic"), "steveredgrave": ("sport", "olympic"), "rebeccadownie": ("sport", "olympic"),
    "simonebiles": ("sport", "olympic"), "samquek": ("sport", "olympic"), "jaynetorvilltorvillanddean": ("sport", "olympic"),
    "christopherdeantorvillanddean": ("sport", "olympic"), "raismanalexandra": ("sport", "olympic"),
    "spiridonovadaria": ("sport", "olympic"), "schaeferpauline": ("sport", "olympic"), "lindseyvonn": ("sport", "olympic"),
    "benainsley": ("sport", "olympic"), "ianthorpe": ("sport", "olympic"), "mathewpinsent": ("sport", "olympic"),
    "lutalomuhammad": ("sport", "olympic"), "markfoster": ("sport", "olympic"), "josephcraigswimmer": ("sport", "olympic"),
    "jadejones": ("sport", "olympic"), "nickwoodbridgewithmedal": ("sport", "olympic"),
    "travispastrana": ("sport", "motorbike"), "gallerytravispastranaportrait": ("sport", "motorbike"),
    "jamestoseland": ("sport", "motorbike"), "johnmcguinness": ("sport", "motorbike"), "jennytinmouth": ("sport", "motorbike"),
    "jennytinemouth": ("sport", "motorbike"), "michaeldunlop": ("sport", "motorbike"), "jorgelorenzo": ("sport", "motorbike"),
    "mariacostello": ("sport", "motorbike"),
    # "other" -> business, public and historical figures
    **{k: ("business", "") for k in [
        "lordkitchener", "nedrocknroll", "maryquant", "sherylsandberg", "jamespatterson", "johnthebaptist", "deepakchopra",
        "philipgreen", "robertfalconscott", "sheikhmansour", "elonmusk", "rupertmurdoch", "versace", "romanabramvich",
        "stevewozniak", "edgarallanpoe", "thomasmarkle", "alberteinstein", "natashaarcher", "marcjacobs", "laurensilverman",
        "colonelsanders", "badenpowell", "satyanadella", "andywarhol", "larryflynt", "markzuckerberg", "kimsears", "billgates",
        "matthewwilliamson", "natashazinko", "traceyemin", "pippamiddleton", "mezhganhussainy", "tomford", "hyungtaekim",
        "richardbransonold", "richardbransonentrepreneurwhiteeye", "jennajameson", "stormydaniels", "urigeller"]},
    # "other" -> TV / radio personalities
    **{k: ("tv", "") for k in ["terryfator", "ritaseaker", "pollysherman", "ricciguarnaccio", "paddymaguire", "kenbruce",
                               "lynnebowle", "lisaarmstrong", "alexbelfield", "nancydellolio"]},
    "stevebest": ("comedy", ""),
    "monicalewinsky": ("politics", ""), "gretathunberg": ("politics", ""), "gretathunbergpic": ("politics", ""),
    "jamiebrysonnn": ("politics", ""),
    "nickbateman": ("models", ""),
    # "other" -> YouTubers and influencers
    **{k: ("online", "") for k in ["ethandolan", "graysondolan", "pewdipie", "zoella", "hasbullamagomedov", "martymckenna",
                                   "gracehelbig", "meredithfoster", "evagutwoski", "ellacatliff", "wealdstoneraideryougotnofans"]},
    "ksi": ("music", ""),
    # "other" -> novelty, animals, emojis
    **{k: ("novelty", "") for k in ["littlegirl", "bison", "outline", "motorbiker", "africanlion", "persoanlised", "curlyhair",
                                    "corpsezombie", "anxiousemoji", "monkeytounge", "acid", "catemoji", "monkeyselfie", "baby",
                                    "fox", "scouser", "manutdman", "notpaulmerson", "raysofsunshine", "olympicmasks",
                                    "ladbrokesman"]},
    # sensitive: owner decides
    **{k: ("unsure", "") for k in ["reggiekray", "ronniekray", "osamabinladen", "osamabinladenzoom", "jeffreyepstein",
                                   "josephfritzel", "josephfritzelcrazy", "edgein", "jeffreydahmer", "maori"]},
}

# everything else the master list filed as "other" is a bare first name / unidentified face
_VAGUE = """lukechilton jamiemaguire davidpalmer paul georgia muriel gallagher justice miranda mickeygooch julielake mateo mis
mike haleyroberts kingsley mathildabelladonna lugano jameshiller rosssmith joannelamont leejohnson nextdayer cddcebbfcfccaf
kshatriyaari luke kessler rafacabello suetuke tomfell sarahjane shaynebyrne robbielawson wood sophiereplace samobobrien
lindsaystoppard sarahdays rebeccaferguson tumblrvomigk jeffallen sarahhoare sroberta sarahgoodhart wenn tori scottbenchtaylor
rebeccafergusonlonghair robertlonsdale whirter meganmccallister sambottomley sambentham stevejones your tommyx rupertjones
sandysinatra tp thomasatkinsonlachlanwhite yeyang sarahobrian shanemaguire stewart tymekkucharczyk mrg rossholding simoncass
stuartkellet tam rachelroberts stephenjones pauligualitire montana harriet liam mcgregor jonathanaintone karenmaguire
gersonbergher jonathanwrather maxresdefault markashton markdowlan davidlove bill kath garyjohnson mathieu nickbains nicolaking
isa miguelfiance freddiegoodwin ollie rachel jacquiholland fergie projectdawn maxwell rose harrybest henry forum
twwfzvuqjyeqtsiqhvk marcel taajmanzoor kevinneylon kevinneylonproof jordanmas jerryledbetter lisahouseman kenwright heathbaxton
fedfbdfbbafcbcfcbf sophia img edith jamiehamilton michelle kasandrakahler johnny therealrandychavez gustappo dannywoods
lovelyjaime kip karenphil jamie johnmacmillan charlierundle natashalyons masanorikobayashi jamesfolder jenny guy jesse moya
jimmystorrar eacebebafabca dadbbbfbebeff ryanhall jonnyrussel""".split()
for _k in _VAGUE:
    KEY_CAT.setdefault(_k, ("unsure", ""))

SENSITIVE = {"Reggie Kray", "Ronnie Kray", "Osama bin Laden", "Jeffrey Epstein", "Josef Fritzl", "Ed Gein", "Jeffrey Dahmer",
             "joseph fritzel", "Māori Face"}
