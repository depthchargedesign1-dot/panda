import json,re
def load(path):
    P={};V=[]
    for l in open(path):
        o=json.loads(l)
        if '__parentId' in o: V.append(o)
        else: P[o['id']]=o
    return P,V
def vtext(v): return (v['title']+' | '+' | '.join(f"{s['name']}={s['value']}" for s in v['selectedOptions']))
NEG=re.compile(r'print only|no frame|unframed|without frame|frameless',re.I)
def framed_size(v):
    t=vtext(v)
    if not re.search(r'frame',t,re.I) or NEG.search(v['title']): return None
    a4=re.search(r'\bA4\b',v['title'],re.I); a3=re.search(r'\bA3\b',v['title'],re.I)
    if a4 and not a3: return 'A4'
    if a3 and not a4: return 'A3'
    return '?'
