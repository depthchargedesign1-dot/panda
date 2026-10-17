import sys; sys.path.insert(0,'../verify'); from gqlparse import P
def parse_any(path):
    t=open(path,encoding='utf-8').read().strip()
    p=P(t); assert p.name()=='mutation'; p.ws(); assert t[p.i]=='{'; p.i+=1
    res=[]
    while True:
        p.ws()
        if t[p.i]=='}': break
        alias=p.name(); p.ws(); assert t[p.i]==':'; p.i+=1; p.ws()
        fn=p.name(); p.ws(); assert t[p.i]=='('; p.i+=1
        args={}
        while True:
            p.ws()
            if t[p.i]==')': p.i+=1; break
            k=p.name(); p.ws(); assert t[p.i]==':'; p.i+=1; args[k]=p.value()
        p.ws(); assert t[p.i]=='{'; depth=0
        while True:
            if t[p.i]=='{': depth+=1
            elif t[p.i]=='}':
                depth-=1
                if depth==0: p.i+=1; break
            elif t[p.i]=='"': p.string(); continue
            p.i+=1
        res.append((alias,fn,args))
    return res
