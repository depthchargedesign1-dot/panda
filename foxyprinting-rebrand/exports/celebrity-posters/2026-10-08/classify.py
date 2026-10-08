import json,collections,re,sys
src=sys.argv[1]
rows=[json.loads(l) for l in open(src)]
cp=[r for r in rows if 'printed signature' in r['title'].lower()]
TYPEMAP={
 'american football posters':'american-football','signed nfl footballers':'american-football',
 'signed music posters':'music','signed rock music prints':'music',
 'signed movie star posters':'film','signed bollywood prints':'film',
 'signed tv show prints':'tv','signed television prints':'tv','signed comedian prints':'tv',
 'signed athletics prints':None,'signed basketball player prints':'us-sports','signed baseball player prints':'us-sports','signed ice hockey prints':'us-sports',
 'signed darts posters':'darts','signed rugby prints posters':'rugby','signed cricketer prints':'cricket','signed cricket posters':'cricket',
 'signed ufc prints posters':'mma-wrestling','signed wrestling prints':'mma-wrestling','signed wwe wrestling prints':'mma-wrestling',
 'signed golf prints':'golf','signed golfer prints posters':'golf','signed boxing prints':'boxing','signed boxing prints posters':'boxing',
 'signed footballer posters':'football','signed footballer prints':'football','signed footballer posters, signed footballer prints':'football',
 'signed tennis player prints':'tennis','signed horse racing prints':'horse-racing','signed authors prints':'icons',
 'signed formula 1 drivers':'motorsport','signed formula1 prints posters':'motorsport','signed motor racer prints':'motorsport',
 'signed famous businessmen prints':'icons','signed scientist prints':'icons','signed fashion designer prints':'icons',
 'signed a6 poster cards':'football','signed swimmer prints':'athletics','signed team player prints':'football','signed dancers prints':'icons',
}
KW=[ # title keywords (checked in order) for mixed types
 ('american football','american-football'),('nfl','american-football'),
 ('horse rac','horse-racing'),('jockey','horse-racing'),
 ('mma','mma-wrestling'),('wrestl','mma-wrestling'),('ufc','mma-wrestling'),('fiighter','mma-wrestling'),('fighter','mma-wrestling'),
 ('rugby','rugby'),('cricket','cricket'),('golf','golf'),('tennis','tennis'),('darts','darts'),('snooker','snooker'),
 ('formula','motorsport'),('f1 driver','motorsport'),('motor','motorsport'),
 ('basketball','us-sports'),('baseball','us-sports'),('ice hockey','us-sports'),
 ('boxer','boxing'),('boxing','boxing'),
 ('athletics','athletics'),('olympian','athletics'),('swimmer','athletics'),
 ('walking dead','tv'),('game of thrones','tv'),('tv show','tv'),('netflix','tv'),('shows framed','tv'),('television','tv'),('comedian','tv'),
 ('movie','film'),('actor','film'),('film','film'),('bollywood','film'),
 ('music','music'),('singer','music'),('rapper','music'),('band','music'),('tour','music'),
 ('football','football'),('footballer','football'),('team player','football'),('teams framed','football'),('team framed','football'),
]
TAGKW=[('Music Star Autograph','music'),('Movie Star Autograph','film'),('Tv Show Star Autograph','tv'),('Walking Dead Star Autograph','tv'),('Game Of Thrones Star Autograph','tv'),
 ('Snooker Star Autograph','snooker'),('Tennis Star Autograph','tennis'),('Formula 1 Star Autograph','motorsport'),('Boxer Autograph','boxing'),('Golfer Autograph','golf'),
 ('Rugby Star Autograph','rugby'),('Cricketer Autograph','cricket'),('Horse Racing Star Autograph','horse-racing'),('Mma Wrestling Star Autograph','mma-wrestling'),
 ('American Footballer Autograph','american-football'),('Football Player Autograph','football'),('Singers','music'),('Rappers','music'),('ActorsGift','film'),('NetflixShows','tv'),
 ('Athletics Autograph','athletics'),('Basketball Player Autograph','us-sports'),('Darts Print','darts'),('Football Poster','football'),
 ('Football Print','football'),('Music Print','music'),('Movie Print','film'),('Boxer Print','boxing'),('Top Boxers print','boxing'),('MMA Print','mma-wrestling'),('Wrestler Print','mma-wrestling'),
 ('Cricket Print','cricket'),('CRICKET','cricket'),('Racer Print','motorsport'),('Formula 1 Themed Gifts','motorsport'),('Tennis Print','tennis'),('Rugby Print','rugby'),('Basketball Print','us-sports'),('Snooker Print','snooker'),
 ('Motorcycle Motorsport  Star Autograph','motorsport'),('Lewis Hamilton','motorsport'),('Yuki Tsunoda','motorsport'),('LadiesFootballTeams','football'),('PremierLeagueFootballTeamGift','football'),('OlympiansGift','athletics'),('UFCFIightersGift','mma-wrestling'),
 ('James Bond','film'),('MovieStar','film'),('Batman','film'),('Superman','film'),('StrangerThings','tv'),('Doctor Who','tv'),('SignedTVStarPrint','tv'),('CricketStarPrint','cricket'),('SignedFootballers','football')]
def classify(r):
    t=r['title'].lower(); ty=r['productType'].strip().lower(); tags=set(r['tags'])
    g=TYPEMAP.get(ty)
    # darts / snooker override (titles)
    if 'darts' in t or 'Darts Print' in tags: return 'darts'
    if 'snooker' in t or 'Snooker Star Autograph' in tags: return 'snooker'
    if g: return g
    for tg,gg in TAGKW:
        if tg in tags: return gg
    for k,gg in KW:
        if k in t: return gg
    for k,gg in [('usain bolt','athletics'),(' f1 ','motorsport'),('verstappen','motorsport'),('conor benn','boxing'),('eubank','boxing'),('tv series','tv'),('star wars','tv'),
                 (' fc','football'),('f.c.','football'),('afc','football'),('national team','football'),('lionesses','football'),('goalkeeper','football'),('midfielder','football'),('striker','football'),('defender','football'),('forward','football'),('united','football'),('fa cup','football'),('carabao','football'),('premier league','football'),('wolves','football'),('ajax','football'),(' cf ','football'),('aston villa','football'),('tottenham','football'),('shearer','football'),('sørloth','football')]:
        if k in t: return gg
    for k,gg in NAMES.items():
        if t.startswith(k): return gg
    return 'unknown'
NAMES={'ayrton senna':'motorsport','barry sheene':'motorsport','charles leclerc':'motorsport','colin mcrae':'motorsport','fernando alonso':'motorsport','george russell':'motorsport','lando norris':'motorsport','marc marquez':'motorsport','michael schumacher':'motorsport','mick doohan':'motorsport','nigel mansell':'motorsport','sebastian vettel':'motorsport','valentino rossi':'motorsport',
'john cena':'mma-wrestling','ronda rousey':'mma-wrestling','joanah lomu':'rugby','jonah lomu':'rugby','jonny wilkinson':'rugby','andy murray':'tennis','roger federer':'tennis','jimmy white':'snooker'}
if __name__=='__main__':
    res={r['id']:classify(r) for r in cp}
    c=collections.Counter(res.values()); print(len(cp), c.most_common())
    for r in cp:
        if res[r['id']]=='unknown' and len(sys.argv)>3: print('  ?',r['productType'],'|',r['title'][:100],'|',r['tags'][:6])
    json.dump({r['id']:[res[r['id']],r['title'],r['productType'],r['status'],r['tags'],r['handle']] for r in cp},open(sys.argv[2],'w'))
