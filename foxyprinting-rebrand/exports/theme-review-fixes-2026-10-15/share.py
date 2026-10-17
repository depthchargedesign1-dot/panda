import sys
from PIL import Image, ImageDraw, ImageFont
d=sys.argv[1]
W,H=1200,630
ink=(29,18,64); orange=(255,106,19); pink=(255,45,135); yellow=(255,200,61); teal=(0,184,169); purple=(122,43,245)
im=Image.new('RGB',(W,H),ink)
dr=ImageDraw.Draw(im)
# brand blobs, same idea as the theme hero
for (cx,cy,r,c) in [(1080,-40,230,pink),(1180,560,170,orange),(930,600,80,yellow),(60,-30,90,purple),(40,640,60,teal)]:
    dr.ellipse([cx-r,cy-r,cx+r,cy+r],fill=c)
logo=Image.open(d+'/logo.png').convert('RGBA')
lh=470; lw=int(logo.width*lh/logo.height)
logo=logo.resize((lw,lh),Image.LANCZOS)
im.paste(logo,(70,(H-lh)//2),logo)
fb=ImageFont.truetype(d+'/Poppins-Bold.ttf',58)
fs=ImageFont.truetype(d+'/Poppins-SemiBold.ttf',30)
x=70+lw+50
lines=['Personalised','mugs, cards,','prints & gifts']
y=150
for i,l in enumerate(lines):
    dr.text((x,y),l,font=fb,fill=(255,255,255) if i!=2 else yellow)
    y+=74
y+=18
dr.text((x,y),'Printed in the UK',font=fs,fill=(255,255,255))
dr.text((x,y+44),'foxyprinting.co.uk',font=fs,fill=orange)
im.save(sys.argv[2],'JPEG',quality=90,optimize=True,progressive=True)
