#!/usr/bin/env python3
"""Foxy Printing eBay shop artwork, from the website's logo, colours and banner pictures.

Makes, in shop/:
  ebay-logo-no-phone.png        the website logo without the phone number line (eBay doesn't allow contact
                                details in listings or the shop), for the listing template header
  store-logo-300.png            eBay Store logo (300 x 300)
  store-billboard-1280x288.jpg  eBay Store billboard / banner (1280 x 288)

Usage: python3 -I tools/ebay_branding.py <logo.png> <pictures_dir> <fonts_dir> <out_dir>
  logo.png      = FoxyPrinting-lOGO-new-number-2026-orange-white-text.png from Shopify Files
  pictures_dir  = foxy-mega-personalised-gifts.png, foxy-mega-drinkware.png, foxy-promo-photo-gifts.png,
                  foxy-mega-christmas.png (the website's mega-menu pictures; no celebrity faces on purpose)
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

INK = (29, 18, 64); ORANGE = (255, 106, 19); PINK = (255, 45, 135); PURPLE = (122, 43, 245)
TEAL = (0, 184, 169); YELLOW = (255, 200, 61); WHITE = (255, 255, 255)


def bands(alpha):
    rows = np.where(alpha.max(axis=1) > 0)[0]
    out, start, prev = [], rows[0], rows[0]
    for r in rows[1:]:
        if r != prev + 1:
            out.append((start, prev)); start = r
        prev = r
    out.append((start, prev))
    return out


def logo_no_phone(logo):
    a = np.array(logo)[:, :, 3]
    b = bands(a)
    cut = b[-1][0] - 6                    # the last text line is the phone number
    im = logo.crop((0, 0, logo.width, cut))
    return im.crop(im.getbbox())


def gradient_strip(w, h):
    stops = [ORANGE, PINK, PURPLE, TEAL]
    strip = Image.new('RGB', (w, h))
    px = strip.load()
    for x in range(w):
        t = x / (w - 1) * (len(stops) - 1)
        i = min(int(t), len(stops) - 2); f = t - i
        c = tuple(int(stops[i][k] * (1 - f) + stops[i + 1][k] * f) for k in range(3))
        for y in range(h):
            px[x, y] = c
    return strip


def rounded(im, r):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = im.convert('RGBA'); out.putalpha(m)
    return out


def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s + 0.5), int(im.height * s + 0.5)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((l, t, l + w, t + h))


def main(logo_path, pics, fonts, out):
    os.makedirs(out, exist_ok=True)
    logo = Image.open(logo_path).convert('RGBA')
    lg = logo_no_phone(logo)
    lg.save(os.path.join(out, 'ebay-logo-no-phone.png'))
    head = Image.fromarray(np.array(logo)).crop((0, 0, logo.width, bands(np.array(logo)[:, :, 3])[0][1] + 1))
    head = head.crop(head.getbbox())
    fred = lambda s: ImageFont.truetype(os.path.join(fonts, 'Fredoka-SemiBold.ttf'), s)
    pop = lambda s: ImageFont.truetype(os.path.join(fonts, 'Poppins-Bold.ttf'), s)

    # --- store logo 300 x 300 ---
    sq = Image.new('RGB', (300, 300), INK)
    h2 = head.copy(); h2.thumbnail((200, 140), Image.LANCZOS)
    sq.paste(h2, ((300 - h2.width) // 2, 38), h2)
    d = ImageDraw.Draw(sq)
    for txt, y, f, c in [('FOXY', 186, fred(44), ORANGE), ('PRINTING', 230, fred(34), WHITE)]:
        w = d.textlength(txt, font=f); d.text(((300 - w) / 2, y), txt, font=f, fill=c)
    sq.paste(gradient_strip(300, 8), (0, 292))
    sq.save(os.path.join(out, 'store-logo-300.png'))

    # --- billboard 1280 x 288 ---
    W, H = 1280, 288
    bb = Image.new('RGB', (W, H), INK)
    names = ['foxy-mega-personalised-gifts.png', 'foxy-mega-drinkware.png', 'foxy-promo-photo-gifts.png',
             'foxy-mega-christmas.png']
    x = 640
    tile_w = (W - x - 20 - 3 * 10) // 4
    for n in names:
        p = Image.open(os.path.join(pics, n)).convert('RGB')
        t = rounded(cover(p, tile_w, H - 56), 16)
        bb.paste(t, (x, 18), t)
        x += tile_w + 10
    # soft fade from the text panel into the pictures
    fade = Image.new('L', (W, 1)); fade.putdata([255 if i < 600 else max(0, int(255 * (1 - (i - 600) / 70))) for i in range(W)])
    bb = Image.composite(Image.new('RGB', (W, H), INK), bb, fade.resize((W, H)))
    lgb = lg.copy(); lgb.thumbnail((190, 236), Image.LANCZOS)
    bb.paste(lgb, (28, (H - 10 - lgb.height) // 2), lgb)
    d = ImageDraw.Draw(bb)
    d.text((240, 46), 'Personalised gifts &', font=fred(40), fill=WHITE)
    d.text((240, 92), 'party printing', font=fred(40), fill=ORANGE)
    d.text((240, 152), 'Celebrity masks · Mugs · Posters · Baby grows', font=pop(16), fill=YELLOW)
    d.text((240, 182), 'Printed to order in our North Yorkshire workshop', font=pop(15), fill=(220, 214, 240))
    bb.paste(gradient_strip(W, 10), (0, H - 10))
    bb.save(os.path.join(out, 'store-billboard-1280x288.jpg'), quality=90)
    print('done', lg.size)


if __name__ == '__main__':
    main(*sys.argv[1:5])
