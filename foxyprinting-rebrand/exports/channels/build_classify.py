import json,glob,re,csv
done=set()
for f in sorted(glob.glob('b*.ids'))[:11]: done|=set(json.load(open(f)))
tg=json.load(open('targets.json'))
retro=set(r['id'] for r in csv.DictReader(open('/home/user/panda/foxyprinting-rebrand/exports/merchant-center/2026-10-06-retro-gaming-boxart-risk.csv')))
clubs=r"arsenal|aston villa|villa park|bournemouth|brentford|brighton|chelsea|crystal palace|everton|fulham|leeds|leicester|liverpool|man(chester)? (city|utd|united)|newcastle|nottingham forest|southampton|tottenham|spurs|west ham|wolves|celtic|rangers|ipswich|sunderland|coventry|hull city|anfield|old trafford|emirates|stamford bridge|selhurst|craven cottage|elland road|portman road|etihad|st james|city ground|stadium of light|dean court|falmer|burnley|sheffield|middlesbrough|derby|stoke|norwich|watford|cardiff|swansea|aberdeen|hearts|hibs|hibernian|barcelona|real madrid|juventus|premier league"
brands=r"nintendo|sega|playstation|xbox|atari|snes|n64|gameboy|game boy|mega drive|lego|disney|marvel|pokemon|star wars|harry potter|barbie|minecraft|fortnite|peppa|paw patrol|bluey|coca|pepsi|perfectdraft|guinness|jack daniel|lamborghini|ferrari|porsche|bmw|mercedes|apple|iphone|samsung|google|tiktok|instagram|netflix|friends|simpsons|doctor who|little britain|leatherface|insidious|grinch|elf |frozen|sonic|mario|zelda|stranger things|rebel alliance|dark side|sith|jedi|straight outta|little miss|mr men|gruffalo|hungry caterpillar"
rude=r"\bf\*?u?ck|f\*\*k|\bshit|\bsh\*t|bollocks|\bcunt|c\*nt|\btwat|\bwank|\bdick|\bknob|\barse\b|\bass\b|bitch|piss|\btits?\b|\bboobs?\b|willy|rude|naughty|cheeky bum|bellend|\bslag|\bwhore|sex"
def why(r):
    t=r['title']; tl=t.lower(); pt=r['productType'].lower(); tags=[x.lower() for x in r['tags']]
    rs=[]
    if 'third-party-name' in tags: rs.append('third-party-name')
    if r['id'] in retro: rs.append('retro-gaming')
    if 'signed' in pt or 'printed signature' in tl or 'signed' in tl or any('signed' in x for x in tags): rs.append('signed-print')
    if ('face mask' in tl or 'facemask' in pt) and 'personalised' not in pt: rs.append('celebrity/character-mask')
    if re.search(clubs,tl): rs.append('football-club')
    if re.search(brands,tl): rs.append('brand/character')
    if re.search(rude,tl) or any(x in ('rude','adult','rude cards','adult humour') for x in tags): rs.append('rude')
    return rs
out=[]
for r in tg:
    out.append({'id':r['id'],'title':r['title'],'productType':r['productType'],'tags':r['tags'],'done':r['id'] in done,'reasons':why(r),'missing':[k for k in ('fb','tt','gg') if not r[k]]})
json.dump(out,open('classified.json','w'))
import collections
print('done risky',sum(1 for o in out if o['done'] and o['reasons']),'done ok',sum(1 for o in out if o['done'] and not o['reasons']))
print('rem risky',sum(1 for o in out if not o['done'] and o['reasons']),'rem ok',sum(1 for o in out if not o['done'] and not o['reasons']))
