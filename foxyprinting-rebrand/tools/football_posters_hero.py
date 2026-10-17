# Builds foxy-home-football-posters-hero.jpg (2400x1240) for the homepage "Football star poster prints" promo-hero.
# Run in the Higgsfield sandbox (cdn.shopify.com is reachable there). Uses our own product images only.
import os, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
B="https://cdn.shopify.com/s/files/1/1774/9115/files/"
SRC={
 'yamal':B+'Lamine-yamal-v2.jpg',
 'ronaldo':B+'RonaldoSILVERSignedFootballPrintSJ-POSTERONLY__12203.jpg',
 'kanebell':B+'judebellingham_harrykaneengland2026.jpg?width=1200',
 'messi':B+'LIONELMESSIINTERMIAMISIGNEDPOSTERICON.jpg',
 'liv':B+'LiverpoolTeam2023SignedPrintSalahKloppVanDijk.jpg?width=1800',
 'mci':B+'ManchesterCityTeamTrebleWinners2023GuardiolaHaalandDeBruyne.jpg?width=1800',
}
os.makedirs('src',exist_ok=True)
for k,u in SRC.items():
    p=f'src/{k}.jpg'
    if not os.path.exists(p): subprocess.run(['curl','-sfL','--max-time','30',u,'-o',p],check=True)
im={k:Image.open(f'src/{k}.jpg').convert('RGB') for k in SRC}
im['ronaldo']=im['ronaldo'].crop((166,68,634,729))
W,H=2400,1240
# background: deep navy-teal with floodlight glows
bg=Image.new('RGB',(W,H))
d=ImageDraw.Draw(bg)
for y in range(H):
    t=y/H
    c=(int(8+6*t),int(38-14*t),int(52-20*t))
    d.line([(0,y),(W,y)],fill=c)
glow=Image.new('L',(W,H),0); g=ImageDraw.Draw(glow)
for (cx,cy,r,a) in [(1550,-120,900,120),(2350,60,520,90),(700,-60,480,70)]:
    g.ellipse((cx-r,cy-r,cx+r,cy+r),fill=a)
glow=glow.filter(ImageFilter.GaussianBlur(220))
teal=Image.new('RGB',(W,H),(0,184,169))
bg=Image.composite(teal,bg,glow.point(lambda v:int(v*0.55)))
light=Image.new('RGB',(W,H),(255,255,255))
spot=Image.new('L',(W,H),0); ImageDraw.Draw(spot).ellipse((1100,-500,2100,250),fill=60)
bg=Image.composite(light,bg,spot.filter(ImageFilter.GaussianBlur(160)))
vig=Image.new('L',(W,H),0); ImageDraw.Draw(vig).ellipse((-400,-300,W+600,H+500),fill=255)
vig=vig.filter(ImageFilter.GaussianBlur(200)).point(lambda v:255-v)
bg=Image.composite(Image.new('RGB',(W,H),(4,14,20)),bg,vig.point(lambda v:int(v*0.8)))
canvas=bg.convert('RGBA')
def framed(img,w,h,fw=15,mt=20):
    iw,ih=w-2*fw-2*mt,h-2*fw-2*mt
    sc=min(iw/img.width,ih/img.height)
    art=img.resize((round(img.width*sc),round(img.height*sc)),Image.LANCZOS)
    f=Image.new('RGB',(w,h),(16,16,18)); fd=ImageDraw.Draw(f)
    fd.rectangle((0,0,w-1,h-1),outline=(64,64,68),width=2)
    fd.rectangle((fw,fw,w-fw-1,h-fw-1),fill=(244,242,236))
    fd.line((fw,fw,w-fw,fw),fill=(205,203,196),width=4)
    fd.line((fw,fw,fw,h-fw),fill=(220,218,211),width=3)
    ax=(w-art.width)//2; ay=(h-art.height)//2
    fd.rectangle((ax-2,ay-2,ax+art.width+1,ay+art.height+1),fill=(190,186,176))
    f.paste(art,(ax,ay))
    # glass sheen
    sheen=Image.new('L',(w,h),0); sd=ImageDraw.Draw(sheen)
    sd.polygon([(0,0),(int(w*0.55),0),(int(w*0.25),h),(0,h)],fill=18)
    f=Image.composite(Image.new('RGB',(w,h),(255,255,255)),f,sheen.filter(ImageFilter.GaussianBlur(30)))
    return f
def place(img,x,y,w,h):
    sh=Image.new('L',(W,H),0); ImageDraw.Draw(sh).rectangle((x+10,y+24,x+w+10,y+h+30),fill=200)
    sh=sh.filter(ImageFilter.GaussianBlur(26))
    canvas.alpha_composite(Image.merge('RGBA',[Image.new('L',(W,H),0)]*3+[sh]))
    canvas.paste(framed(img,w,h),(x,y))
# layout: two landscape team prints on top, four portrait prints below
gap=40; LW=740; LH=round(LW/1.414); x0=2370-(2*LW+gap)
PW=(2*LW+gap-3*gap)//4; PH=round(PW/0.7071)
top=(H-(LH+gap+PH))//2
place(im['liv'],x0,top,LW,LH); place(im['mci'],x0+LW+gap,top,LW,LH)
pg=gap
py=top+LH+gap
for i,k in enumerate(['yamal','ronaldo','kanebell','messi']):
    place(im[k],x0+i*(PW+pg),py,PW,PH)
out=canvas.convert('RGB')
out.save('hero.jpg',quality=88,optimize=True,progressive=True)
out.resize((1200,620)).save('preview.jpg',quality=80)
# mobile crop preview (right 5:4) and desktop preview with left fade
mob=out.crop((W-int(H*1.25),0,W,H)).resize((620,496)); mob.save('mobile.jpg',quality=80)
print(out.size, os.path.getsize('hero.jpg'), x0, py+PH)
