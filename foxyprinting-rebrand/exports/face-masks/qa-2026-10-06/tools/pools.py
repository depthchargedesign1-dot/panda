import sys,re
sys.path.insert(0,'/home/user/panda/foxyprinting-rebrand/tools')
import mask_copy as M
OCC={}   # phrase -> key
for key,rx,label,who,occ in M.CATS:
    for o in occ: OCC[o]=key
for o in M.DEFAULT[4]: OCC[o]='celeb'
LABEL={c[0]:c[2] for c in M.CATS}; WHO={c[0]:c[3] for c in M.CATS}
POOLS={c[0]:c[4] for c in M.CATS}; POOLS['celeb']=M.DEFAULT[4]
TAGKEY={'mask-footballers':['football'],'mask-darts':['darts'],'mask-golf':['golf'],'mask-f1':['f1'],'mask-tennis':['tennis'],'mask-boxing':['boxing'],
 'mask-cricket':['cricket'],'mask-rugby':['rugby'],'mask-snooker':['snooker'],'mask-sport':['sport'],'mask-politicians-royals':['royal'],
 'mask-music':['music'],'mask-comedians':['comedy'],'mask-reality-tv':['reality'],'mask-film-stars':['film'],'mask-tv-stars':['tv'],
 'mask-stag-hen':['celeb'],'mask-packs-couples':['celeb'],'mask-characters':['celeb']}
SPORTS={'football','darts','golf','f1','tennis','boxing','cricket','rugby','snooker','sport'}
def allowed(tags):
    a={'celeb'}
    for t in tags:
        for k in TAGKEY.get(t,[]): a.add(k)
    if a & SPORTS: a.add('sport')
    if 'sport' in a and not (a & (SPORTS-{'sport'})): a |= SPORTS   # generic sport tag only
    if a & {'film','tv','reality','comedy'}: a |= {'film','tv'} if a & {'film','tv'} else set()
    return a
FAM={'football':'S','darts':'S','golf':'S','f1':'S','tennis':'S','boxing':'S','cricket':'S','rugby':'S','snooker':'S','sport':'S',
     'music':'M','royal':'R','film':'V','tv':'V','reality':'V','comedy':'V','celeb':'C'}
LABELFAM={'football star':'S','darts star':'S','golfer':'S','Formula 1 driver':'S','tennis star':'S','boxer':'S','cricketer':'S','rugby star':'S','snooker star':'S','sports star':'S','music star':'M','public figure':'R'}
def tagfams(tags):
    f=set()
    for t in tags:
        for k in TAGKEY.get(t,[]): f.add(FAM[k])
    return f
GENERIC={"a hen do","a stag or hen do","a girls' night in","a karaoke night","a movie night","a themed birthday","a birthday roast","a finale watch party","a telly-night quiz","a street party","a birthday party","a wedding photo booth"}
