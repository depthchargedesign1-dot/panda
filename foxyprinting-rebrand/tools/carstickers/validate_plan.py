import json,re
it=json.load(open('plan.json'))
bad=[]
for x in it:
  d=x['descriptionHtml']; body=d.split('<h3>Please note')[0]
  wn=len(re.sub('<[^>]+>',' ',body).split())
  if not (150<=wn<=220) or d.count('<h2>')!=1 or len(x['seoTitle'])>60 or not x['seoDescription'] or not(140<=len(x['seoDescription'])<=155): bad.append((x['handle'],wn,x['seoTitle']))
  for w in ['official','licensed','authentic','genuine','merchandise','endorsed','approved']:
    if re.search(w,body+x['seoDescription']+x['seoTitle'],re.I): bad.append((x['handle'],'banned',w))
  if re.search(r'fuck|shit|bitch|wank|fags|clunge|minge|titty|bumder|\bhoe\b|\bjap\b|arse|doggy|boobies|\bsex\b|FAST DISPATCH|Many more|6" WIDE Custom',body+x['seoDescription'],re.I): bad.append((x['handle'],'swear/old'))
  if x['branded'] != ('class="disclaimer"' in d) or '[' in d: bad.append((x['handle'],'disc'))
print('bad',bad)
print(len(it), len({x['seoTitle'] for x in it}), len({x['descriptionHtml'] for x in it}))
