import json
plan=json.load(open('plan.json'))
DISC='<h3>Please note</h3><p class="disclaimer">These are unofficial, fan-made prints designed and printed by Foxy Printing. The signature is printed as part of the design – it is not hand-signed and is not an original autograph. The people shown have not endorsed, sponsored or approved these products, and Foxy Printing has no connection with them, their clubs, teams, studios or record labels. Names are used only to describe the design. All trademarks belong to their respective owners.</p>'
SUBS=[
 ('music','music-star-posters','Music Star Posters','Music Star Posters with Printed Signature','Music star posters with a printed signature – singers, bands and rappers for your wall. A4 to large sizes, print only or framed. Great gift for music fans.',
  'Music star posters for every playlist – pop icons, rock legends, rappers and much-loved bands, each with the signature printed into the design.','Perfect for a bedroom, music room or studio, and a lovely gift for a gig-goer or a fan counting down to the next tour.'),
 ('film','film-star-posters','Film Star Posters','Film Star Posters with Printed Signature','Film star posters with a printed signature – Hollywood and Bollywood actors in a choice of sizes, print only or framed. A great gift for movie fans.',
  'Film star posters for movie lovers – Hollywood leading men and women, action heroes and Bollywood favourites, each with a printed signature as part of the artwork.','Ideal for a home cinema, a film buff’s den or as a birthday surprise for someone who can quote every line.'),
 ('tv','tv-star-posters','TV Star Posters','TV Star Posters with Printed Signature','TV star posters with a printed signature – faces from your favourite shows and comedy. Choose your size, print only or framed. A fun gift for TV fans.',
  'TV star posters celebrating the faces from the shows you binge – drama, comedy, reality and box-set favourites, each finished with a printed signature.','A brilliant gift for a superfan, and a great way to brighten up a lounge, games room or bedroom wall.'),
 ('football','football-star-posters','Football Star Posters','Football Star Posters with Printed Signature','Football star posters with a printed signature – Premier League, Lionesses, legends and international players. Print only or framed. Ideal fan gift.',
  'Football star posters for every fan – current Premier League players, Lionesses, international captains and all-time legends, each with the signature printed into the design.','A top pick for a bedroom, man cave or clubhouse, and a cracking birthday or Christmas present for the football mad.'),
 ('american-football','nfl-american-football-posters','NFL & American Football Star Posters','NFL & American Football Posters – Printed Signature','NFL and American football star posters with a printed signature – quarterbacks, receivers and legends. Choose your size, print only or framed.',
  'NFL and American football star posters for gridiron fans – quarterbacks, running backs, receivers and defensive greats, each with a printed signature.','Perfect for a Super Bowl party, a games room or the NFL fan who has everything.'),
 ('boxing','boxing-star-posters','Boxing Star Posters','Boxing Star Posters with Printed Signature','Boxing star posters with a printed signature – world champions and ring legends. Choose your size, print only or framed. A knockout gift for fight fans.',
  'Boxing star posters for fight fans – heavyweight champions, British favourites and all-time ring legends, each with the signature printed into the design.','A knockout gift for a gym, garage or living room wall.'),
 ('mma-wrestling','ufc-mma-wrestling-posters','UFC, MMA & Wrestling Posters','UFC, MMA & Wrestling Posters – Printed Signature','UFC, MMA and wrestling star posters with a printed signature – fighters and wrestling icons. Choose your size, print only or framed. Great fan gift.',
  'UFC, MMA and wrestling posters for fight-night regulars – octagon champions and wrestling icons, each with a printed signature.','Great for a gym, a games room or a fan who never misses a pay-per-view.'),
 ('darts','darts-snooker-star-posters','Darts & Snooker Star Posters','Darts & Snooker Star Posters – Printed Signature','Darts and snooker star posters with a printed signature – oche heroes and cue legends. Choose your size, print only or framed. Ideal for a games room.',
  'Darts and snooker star posters for the games room – world champions from the oche and the baize, each with the signature printed into the design.','Hang one above the dartboard or snooker table, or give it to the player who always wins the pub league.'),
 ('cricket','cricket-star-posters','Cricket Star Posters','Cricket Star Posters with Printed Signature','Cricket star posters with a printed signature – England heroes and world greats. Choose your size, print only or framed. A great gift for cricket fans.',
  'Cricket star posters for fans of the summer game – England heroes, Ashes favourites and world greats, each with a printed signature.','A lovely gift for a cricket club member, coach or young player.'),
 ('rugby','rugby-star-posters','Rugby Star Posters','Rugby Star Posters with Printed Signature','Rugby star posters with a printed signature – union and league heroes. Choose your size, print only or framed. A great gift for rugby fans.',
  'Rugby star posters for union and league fans – Six Nations heroes, World Cup winners and club legends, each with the signature printed into the design.','Perfect for a clubhouse, a player’s bedroom or a Six Nations party.'),
 ('golf','golf-star-posters','Golf Star Posters','Golf Star Posters with Printed Signature','Golf star posters with a printed signature – major winners and Ryder Cup heroes. Choose your size, print only or framed. A great gift for golfers.',
  'Golf star posters for players and fans – major winners, Ryder Cup heroes and legends of the game, each with a printed signature.','A smart gift for a golfer’s study, office or clubhouse.'),
 ('tennis','tennis-star-posters','Tennis Star Posters','Tennis Star Posters with Printed Signature','Tennis star posters with a printed signature – Grand Slam champions and legends. Choose your size, print only or framed. A great gift for tennis fans.',
  'Tennis star posters for fans of the game – Grand Slam champions and Wimbledon favourites, each with the signature printed into the design.','A great gift for a club player or anyone who lives for the summer fortnight.'),
 ('horse-racing','horse-racing-star-posters','Horse Racing Star Posters','Horse Racing Star Posters – Printed Signature','Horse racing star posters with a printed signature – champion jockeys and racing legends. Choose your size, print only or framed. Great racing fan gift.',
  'Horse racing star posters for racing fans – champion jockeys and Grand National and Cheltenham heroes, each with a printed signature.','A lovely gift for a racegoer, a stable lad or lass, or a Cheltenham regular.'),
 ('motorsport','f1-motorsport-star-posters','F1 & Motorsport Star Posters','F1 & Motorsport Star Posters – Printed Signature','F1 and motorsport star posters with a printed signature – drivers and riders, past and present. Choose your size, print only or framed. Great fan gift.',
  'F1 and motorsport star posters for petrolheads – Formula 1 drivers, rally heroes and MotoGP riders, past and present, each with the signature printed into the design.','Ideal for a garage, a sim-racing setup or a race-day gift.'),
 ('athletics','athletics-olympic-star-posters','Athletics & Olympic Star Posters','Athletics & Olympic Star Posters – Printed Signature','Athletics and Olympic star posters with a printed signature – sprinters, swimmers and champions. Choose your size, print only or framed. Inspiring gift.',
  'Athletics and Olympic star posters – sprinters, swimmers and champions from the track and the pool, each with a printed signature.','An inspiring print for a young athlete’s bedroom, a gym or a running club.'),
 ('us-sports','basketball-baseball-hockey-posters','Basketball, Baseball & Ice Hockey Posters','Basketball, Baseball & Ice Hockey Posters','Basketball, baseball and ice hockey star posters with a printed signature – greats of the court, diamond and rink. Print only or framed.',
  'Basketball, baseball and ice hockey star posters for fans of American sport – hoops legends, home-run hitters and ice hockey greats, each with the signature printed into the design.','A great gift for a games room, a basketball fan’s bedroom or a trip-to-the-States souvenir.'),
 ('icons','icons-legends-posters','Authors, Scientists & Icons Posters','Authors, Scientists & Icons Posters – Printed Signature','Posters of famous authors, scientists, business leaders and fashion icons with a printed signature. Choose your size, print only or framed.',
  'Posters of the authors, scientists, business leaders, designers and dancers who changed the world, each with a printed signature.','A thoughtful gift for a study, classroom, office or a bookworm’s reading nook.'),
]
def rules_for(key):
    rs=[{'column':c,'relation':'EQUALS' if c=='TYPE' else 'CONTAINS','condition':v} for c,v in plan[key]['rules']]
    if key=='darts':
        pass
    rs.append({'column':'TAG','relation':'EQUALS','condition':'cp-'+key})
    return rs
out=[]
for key,handle,title,seot,seod,intro,closing in SUBS:
    body=(f'<p>{intro} Every design is a printed reproduction made in-house by Foxy Printing.</p>'
          f'<h2>{title}</h2>'
          '<p>Most designs come in a choice of sizes, as a print only or in one of our Premium Display frames – thick, chunky and very professional, not cheap thin frames. Open any poster to see its sizes and prices.</p>'
          f'<p>{closing} Browse all of our <a href="/collections/celebrity-posters">celebrity posters</a> for more.</p>'+DISC)
    out.append({'title':title,'handle':handle,'descriptionHtml':body,'seo':{'title':seot,'description':seod},'sortOrder':'BEST_SELLING','ruleSet':{'appliedDisjunctively':True,'rules':rules_for(key)}})
    assert len(seot)<=60, seot
parent={'title':'Celebrity Posters','handle':'celebrity-posters','sortOrder':'BEST_SELLING',
 'seo':{'title':'Celebrity Posters with Printed Signature | Foxy Printing','description':'Celebrity posters of music, film, TV and sport stars, each with a printed signature. Choose your size, print only or framed – a great gift for any fan.'},
 'ruleSet':{'appliedDisjunctively':True,'rules':[{'column':'TITLE','relation':'CONTAINS','condition':'Printed Signature'},{'column':'TAG','relation':'EQUALS','condition':'celebrity-poster'}]},
 'descriptionHtml':('<p>Celebrity posters for every kind of fan – music icons, film and TV stars, football heroes and sporting legends, each with the signature printed into the design. They make a brilliant birthday, Christmas or Father’s Day gift, and they look great on a bedroom, games room or office wall.</p>'
  '<h2>Celebrity posters with a printed signature</h2>'
  '<p>Every poster is a printed reproduction designed and printed in-house by Foxy Printing. Most designs come in a choice of sizes, as a print only or in one of our Premium Display frames – thick, chunky and very professional, not cheap thin frames. Open any poster to see its sizes and prices.</p>'
  '<h3>Shop by star</h3><ul>'+''.join(f'<li><a href="/collections/{h}">{t}</a></li>' for _,h,t,*_ in SUBS)+'<li><a href="/collections/signed-a6-poster-card-packs">A6 Poster Card Packs</a></li></ul>'
  '<p>Looking for something to go with it? Our <a href="/collections/all-facemasks">celebrity face masks</a> make a fun party pairing.</p>'+DISC)}
assert len(parent['seo']['title'])<=60
for o in [parent]+out: print(len(o['seo']['description']), len(o['ruleSet']['rules']), o['handle'])
json.dump([parent]+out,open('colls.json','w'),indent=1)
