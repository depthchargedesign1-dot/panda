import json,copy
m=json.load(open('menu_live.json'))['data']['menu']
# (path) -> (new title, new url)
CP='/collections/celebrity-posters'
MAP={
 ('Home & Drinkware','Wall Art'):('Wall Art',CP),
 ('Home & Drinkware','Wall Art','Posters & Canvas'):('Celebrity Posters',CP),
 ('Home & Drinkware','Wall Art','Signed Prints'):('Football Star Posters','/collections/football-star-posters'),
 ('Home & Drinkware','More Prints & Posters'):('More Prints & Posters',CP),
 ('Home & Drinkware','More Prints & Posters','A6 Autographed Football Poster Card Packs'):('A6 Football Poster Card Packs','/collections/signed-a6-football-poster-card-packs'),
 ('Home & Drinkware','More Prints & Posters','A6 Autographed Poster Card Packs'):('A6 Poster Card Packs','/collections/signed-a6-poster-card-packs'),
 ('Home & Drinkware','More Prints & Posters','American Football Posters'):('NFL & American Football Posters','/collections/nfl-american-football-posters'),
 ('Home & Drinkware','More Prints & Posters','Formula 1 Star Autograph'):('F1 & Motorsport Star Posters','/collections/f1-motorsport-star-posters'),
 ('Home & Drinkware','More Prints & Posters','Horse Racing Star Autograph'):('Horse Racing Star Posters','/collections/horse-racing-star-posters'),
 ('Home & Drinkware','More Prints & Posters','Movie Star Autograph'):('Film Star Posters','/collections/film-star-posters'),
 ('Home & Drinkware','More Prints & Posters','Music Star Autograph'):('Music Star Posters','/collections/music-star-posters'),
 ('Home & Drinkware','More Prints & Posters','Posters & signed prints'):('All Celebrity Posters',CP),
 ('Home & Drinkware','More Prints & Posters','Signed Boxing Posters'):('Boxing Star Posters','/collections/boxing-star-posters'),
 ('Home & Drinkware','More Prints & Posters','Signed Cricket Posters'):('Cricket Star Posters','/collections/cricket-star-posters'),
 ('Home & Drinkware','More Prints & Posters','Signed Footballer Posters'):('Football Star Posters','/collections/football-star-posters'),
 ('Home & Drinkware','More Prints & Posters','Signed Game of Thrones Star Posters'):('Game of Thrones Star Posters','/collections/game-of-thrones-star-autograph'),
 ('Home & Drinkware','More Prints & Posters','Signed Golfer Posters'):('Golf Star Posters','/collections/golf-star-posters'),
 ('Home & Drinkware','More Prints & Posters','Signed MMA & Wrestling Posters'):('UFC, MMA & Wrestling Posters','/collections/ufc-mma-wrestling-posters'),
 ('Home & Drinkware','More Prints & Posters','Signed Rugby Posters'):('Rugby Star Posters','/collections/rugby-star-posters'),
 ('Home & Drinkware','More Prints & Posters','Signed The Walking Dead Posters'):('The Walking Dead Star Posters','/collections/walking-dead-star-autograph'),
 ('Home & Drinkware','More Prints & Posters','Signed TV Star Posters'):('TV Star Posters','/collections/tv-star-posters'),
 ('Home & Drinkware','More Prints & Posters','Snooker Star Autograph'):('Darts & Snooker Star Posters','/collections/darts-snooker-star-posters'),
 ('Football','Fan Favourites','American Football Posters'):('NFL & American Football Posters','/collections/nfl-american-football-posters'),
 ('Fan Shop & Retro','Sports Fans'):('Sports Fans','/collections/football-star-posters'),
 ('Fan Shop & Retro','Sports Fans','American Football Posters'):('NFL & American Football Posters','/collections/nfl-american-football-posters'),
 ('Fan Shop & Retro','Sports Fans','Signed Prints'):('Celebrity Posters',CP),
}
used=set(); changes=[]
def conv(items,path):
  out=[]
  for it in items:
    p=path+(it['title'],)
    o={'id':it['id'],'title':it['title'],'type':it['type'],'url':it['url']}
    if it.get('resourceId'): o['resourceId']=it['resourceId']
    if it.get('tags'): o['tags']=it['tags']
    if p in MAP:
      used.add(p); nt,nu=MAP[p]
      changes.append({'path':' > '.join(p),'old_title':it['title'],'old_url':it['url'],'old_type':it['type'],'new_title':nt,'new_url':nu})
      o['title']=nt; o['url']=nu; o['type']='HTTP'; o.pop('resourceId',None)
    if it.get('items') is not None and len(it['items'])>0: o['items']=conv(it['items'],p)
    elif 'items' in it: o['items']=[]
    out.append(o)
  return out
items=conv(m['items'],())
# new links in Celebrity Posters > Music, Film & TV (no id = new item)
for top in items:
  if top['title']=='Celebrity Posters':
    for col in top['items']:
      if col['title']=='Music, Film & TV':
        col['items']+= [{'title':'A6 Music Star Card Packs','type':'HTTP','url':'/collections/a6-music-star-poster-card-packs'},
                        {'title':'A6 Film Star Card Packs','type':'HTTP','url':'/collections/a6-movie-and-film-poster-card-packs'},
                        {'title':'Celebrity Mugs','type':'HTTP','url':'/collections/all-celebrity-mugs'}]
        added=True
assert used==set(MAP), set(MAP)-used
v={'id':m['id'],'title':m['title'],'handle':m['handle'],'items':items}
json.dump(v,open('menu_vars.json','w'),separators=(',',':'),ensure_ascii=False)
json.dump(changes,open('menu_changes.json','w'),indent=1)
print(len(changes))
