"""Product images for the 8 Oct 2026 bar mat build.
white_composite(large, small) -> clean white product image (large runner above small mat, soft shadow).
clean_mockup(path)            -> Dropbox wood mockup with the 4 coasters painted out (coasters are not sold).
wood_mockup(large, small)     -> runner + mat laid on a dark wood background (same look as the Dropbox mockups).
"""
from PIL import Image, ImageFilter, ImageChops

def trim(im, thresh=245):
    g = im.convert("L").point(lambda v: 255 if v < thresh else 0)
    box = g.getbbox()
    return im.crop(box) if box else im

def _shadow_paste(canvas, art, xy, blur=18, off=(10, 14), alpha=110):
    sh = Image.new("RGBA", (art.width + 80, art.height + 80), (0, 0, 0, 0))
    core = Image.new("RGBA", art.size, (0, 0, 0, alpha))
    sh.paste(core, (40, 40))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.paste(sh, (xy[0] - 40 + off[0], xy[1] - 40 + off[1]), sh)
    canvas.paste(art.convert("RGB"), xy)

def white_composite(large, small=None, W=2000):
    L = large.convert("RGB")
    lw = int(W * 0.88); L = L.resize((lw, int(L.height * lw / L.width)), Image.LANCZOS)
    if small is not None:
        S = small.convert("RGB")
        sw = int(W * 0.46); S = S.resize((sw, int(S.height * sw / S.width)), Image.LANCZOS)
        H = int(L.height + S.height + W * 0.20)
        c = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        top = int(W * 0.06)
        _shadow_paste(c, L, ((W - lw) // 2, top))
        _shadow_paste(c, S, ((W - sw) // 2, top + L.height + int(W * 0.06)))
    else:
        H = int(L.height + W * 0.16)
        c = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        _shadow_paste(c, L, ((W - lw) // 2, (H - L.height) // 2))
    return c.convert("RGB")

def clean_mockup(path):
    im = Image.open(path).convert("RGB")
    if im.size != (2801, 2007):
        return im
    patch_l = im.crop((140, 872, 450, 1138)); patch_r = im.crop((2350, 872, 2660, 1138))
    for patch, x0 in ((patch_l, 140), (patch_r, 2350)):
        y = 1138
        while y < 1870:
            im.paste(patch, (x0, y)); y += patch.height
    return im

def wood_mockup(large, small, wood_path, W=2400):
    wood = Image.open(wood_path).convert("RGB")
    H = int(W * 0.72)
    r = max(W / wood.width, H / wood.height)
    wood = wood.resize((int(wood.width * r) + 1, int(wood.height * r) + 1), Image.LANCZOS).crop((0, 0, W, H))
    c = wood.convert("RGBA")
    L = large.convert("RGB"); lw = int(W * 0.9); L = L.resize((lw, int(L.height * lw / L.width)), Image.LANCZOS)
    top = int(H * 0.07)
    _shadow_paste(c, L, ((W - lw) // 2, top), alpha=170)
    if small is not None:
        S = small.convert("RGB"); sw = int(W * 0.45); S = S.resize((sw, int(S.height * sw / S.width)), Image.LANCZOS)
        y = top + L.height + int(H * 0.08)
        if y + S.height > H - 20:
            s2 = (H - 20 - y) / S.height; S = S.resize((int(S.width * s2), int(S.height * s2)), Image.LANCZOS)
        _shadow_paste(c, S, ((W - S.width) // 2, y), alpha=170)
    return c.convert("RGB")

def save(im, path, maxw=2000):
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(path, "JPEG", quality=87, optimize=True, progressive=True)
