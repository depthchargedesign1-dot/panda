"""Compact 1800x600 collection banners. crop: 3:1 crop + dark ink fade over the left ~50% (Higgsfield mug scenes). pad: scale to 600px high and extend the plain left edge (existing foxy-header-*.png). Run in the Higgsfield sandbox: python3 banner_compact.py crop|pad SRC DST"""
import sys
from PIL import Image
INK=(29,18,64)
def fade(im, start=0.80, end=0.52):
    W,H=im.size
    ov=Image.new('RGBA',(W,H),INK+(0,))
    a=Image.new('L',(W,1))
    ex=int(W*end)
    for x in range(W):
        t=x/ex if x<ex else 1.0
        v=start*(1-t)**1.6
        a.putpixel((x,0),int(255*v))
    ov.putalpha(a.resize((W,H)))
    return Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
def crop_fade(src,dst,yoff=0.5):
    im=Image.open(src).convert('RGB'); W,H=im.size
    ch=round(W/3); y=int((H-ch)*yoff)
    im=im.crop((0,y,W,y+ch)).resize((1800,600),Image.LANCZOS)
    fade(im).save(dst,'JPEG',quality=85,optimize=True,progressive=True)
def pad_left(src,dst):
    im=Image.open(src).convert('RGB'); W,H=im.size
    nw=round(W*600/H); im=im.resize((nw,600),Image.LANCZOS)
    out=Image.new('RGB',(1800,600)); pad=1800-nw
    if pad>0:
        col=im.crop((0,0,3,600)).resize((1,600)).resize((pad,600))
        out.paste(col,(0,0)); out.paste(im,(pad,0))
    else:
        out=im.crop((nw-1800,0,nw,600))
    out.save(dst,'JPEG',quality=85,optimize=True,progressive=True)
if __name__=='__main__':
    mode,src,dst=sys.argv[1:4]
    {'crop':crop_fade,'pad':pad_left}[mode](src,dst,*([float(sys.argv[4])] if len(sys.argv)>4 else []))
