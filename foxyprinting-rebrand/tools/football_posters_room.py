# Builds foxy-home-football-posters-room.jpg: our six football prints composited edge to edge into the black frames of a
# Higgsfield-generated games room (job 0a26372c-49ca-41e0-b07b-342e07304801). Run in the Higgsfield sandbox.
import os, subprocess, numpy as np
from PIL import Image, ImageFilter
B="https://cdn.shopify.com/s/files/1/1774/9115/files/"
SRC={'yamal':B+'Lamine-yamal-v2.jpg','ronaldo':B+'RonaldoSILVERSignedFootballPrintSJ-POSTERONLY__12203.jpg',
 'kanebell':B+'judebellingham_harrykaneengland2026.jpg?width=1000','messi':B+'LIONELMESSIINTERMIAMISIGNEDPOSTERICON.jpg',
 'liv':B+'LiverpoolTeam2023SignedPrintSalahKloppVanDijk.jpg?width=1400','mci':B+'ManchesterCityTeamTrebleWinners2023GuardiolaHaalandDeBruyne.jpg?width=1400',
 'room':'https://d8j0ntlcm91z4.cloudfront.net/user_3HUr7G8la20J0fiH66SaF8cNGi7/hf_20261006_172757_0a26372c-49ca-41e0-b07b-342e07304801.png'}
os.makedirs('src',exist_ok=True)
for k,u in SRC.items():
    p=f'src/{k}'
    if not os.path.exists(p): subprocess.run(['curl','-sfL','--max-time','40',u,'-o',p],check=True)
P={k:Image.open(f'src/{k}').convert('RGB') for k in SRC if k!='room'}
P['ronaldo']=P['ronaldo'].crop((166,68,634,729))
room=np.asarray(Image.open('src/room').convert('RGB')).astype(np.float32)
H,W,_=room.shape
TA=float(os.environ.get('TA','1.5'))
# openings (x0,y0,x1,y1) inclusive, measured
L=[(1054,179,1533,445),(1629,179,2095,445)]
PO=[(1046,535,1232,782),(1340,535,1528,781),(1632,534,1817,781),(1927,533,2111,779)]
# ---- narrow the two landscape frames by horizontal piecewise remap inside a band
BW=27  # frame border width approx
oh=L[0][3]-L[0][1]+1
ds=[ (L[i][2]-L[i][0]+1) - round(oh*TA) for i in range(2)]
ds=[d+(d%2) for d in ds]
B0=L[0][0]-BW-90; B1=L[1][2]+BW+90
c=[(l[0]+l[2])//2 for l in L]
# control points new_x -> orig_x
pts=[(B0,B0),
 (L[0][0]-BW+ds[0]//2, L[0][0]-BW),
 (c[0], c[0]-ds[0]//2), (c[0]+1, c[0]+ds[0]//2+1),
 (L[0][2]+BW-ds[0]//2, L[0][2]+BW),
 (L[1][0]-BW+ds[1]//2, L[1][0]-BW),
 (c[1], c[1]-ds[1]//2), (c[1]+1, c[1]+ds[1]//2+1),
 (L[1][2]+BW-ds[1]//2, L[1][2]+BW),
 (B1,B1)]
nx=np.arange(B0,B1+1)
ox=np.interp(nx,[p[0] for p in pts],[p[1] for p in pts])
y0b=L[0][1]-BW-40; y1b=L[0][3]+BW+26
band=room[y0b:y1b+1]
# linear interp sample columns
o0=np.floor(ox).astype(int); f=(ox-o0)[None,:,None]
newband=band[:,o0]*(1-f)+band[:,np.minimum(o0+1,W-1)]*f
# feather mask
hh,ww=newband.shape[:2]
my=np.clip(np.minimum(np.arange(hh),hh-1-np.arange(hh))/25.0,0,1)
mxm=np.clip(np.minimum(np.arange(ww),ww-1-np.arange(ww))/40.0,0,1)
m=(my[:,None]*mxm[None,:])[...,None]
room[y0b:y1b+1,B0:B1+1]=newband*m+room[y0b:y1b+1,B0:B1+1]*(1-m)
newL=[(L[i][0]+ds[i]//2, L[i][1], L[i][2]-ds[i]//2, L[i][3]) for i in range(2)]
# ---- composite posters using grey panel as lighting map
def put(img,box,inset=2):
    x0,y0,x1,y1=box; x0-=inset; y0-=inset; x1+=inset; y1+=inset
    w,h=x1-x0+1,y1-y0+1
    ta=w/h; a=img.width/img.height
    if a>ta: nw=round(img.height*ta); img=img.crop(((img.width-nw)//2,0,(img.width-nw)//2+nw,img.height))
    else: nh=round(img.width/ta); img=img.crop((0,(img.height-nh)//2,img.width,(img.height-nh)//2+nh))
    art=np.asarray(img.resize((w,h),Image.LANCZOS)).astype(np.float32)
    panel=room[y0:y1+1,x0:x1+1].mean(2)
    ref=np.percentile(panel,90)
    shade=np.clip(panel/ref,0,1.15)
    shade=np.asarray(Image.fromarray((shade*200).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)/200
    tint=np.array([1.0,0.965,0.91])*0.93
    out=art*shade[...,None]*tint
    # glass sheen
    yy,xx=np.mgrid[0:h,0:w]
    s=((xx/w)*0.6+(1-yy/h)*0.4)
    sheen=np.clip(1-np.abs(s-0.62)/0.10,0,1)*10
    out=out+sheen[...,None]
    room[y0:y1+1,x0:x1+1]=np.clip(out,0,255)
put(P['liv'],newL[0]); put(P['mci'],newL[1])
for k,b in zip(['yamal','ronaldo','kanebell','messi'],PO): put(P[k],b)
img=Image.fromarray(room.astype(np.uint8))
img.save('full.png')
cx0=int(os.environ.get('CX','190'))
crop=img.crop((cx0,0,cx0+2232,H)).resize((2400,1240),Image.LANCZOS)
crop.save('room_hero.jpg',quality=88,optimize=True,progressive=True)
crop.resize((1200,620)).save('prev.jpg',quality=78)
crop.crop((2400-1550,0,2400,1240)).resize((600,480)).save('mob.jpg',quality=75)
crop.crop((1150,150,1950,850)).save('zoom.jpg',quality=80)
print('ds',ds,'newL',newL,os.path.getsize('room_hero.jpg'))
