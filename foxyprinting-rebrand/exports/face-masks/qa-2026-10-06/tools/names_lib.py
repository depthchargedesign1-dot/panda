import re
def h2name(d):
    m=re.search(r'<h2>(.*?)</h2>',d)
    if not m: return None
    h=m.group(1)
    m2=re.match(r'^(.*?) (?:Celebrity |Card |Fancy Dress |Party |Novelty |Cardboard )?(?:Face Mask|Mask)\b',h)
    return m2.group(1) if m2 else h
def discname(d):
    m=re.search(r'<p class="disclaimer">(.*?)</p>',d)
    if not m: return None
    m2=re.search(r'(?:fancy dress|satire|drama|theatre)\. (.*?) (?:has|have) not endorsed',m.group(1))
    return m2.group(1) if m2 else None
def seoname(s):
    m=re.match(r'^(.*?) Face Mask',s or ''); return m.group(1) if m else None
def metaname(s):
    s=s or ''
    for pat in [r'^Get the party started with an? (.*?) face mask',r'^Fancy dress made easy: an? (.*?) face mask',r'^(.*?) card face mask for',r'^(.*?) Face Mask:',r'^An? (.*?) face mask']:
        m=re.match(pat,s)
        if m: return m.group(1)
    return None
