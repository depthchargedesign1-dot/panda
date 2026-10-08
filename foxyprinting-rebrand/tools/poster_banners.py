#!/usr/bin/env python3
"""Celebrity Posters collection header banners (1800x600), 8 Oct 2026.

Builds one banner per poster collection from our OWN product photos (featuredImage on cdn.shopify.com):
crops each print out of its product photo (black mat detection), puts it in a black / gold / silver
frame with a drop shadow, and fans 5-7 of them across the right-hand ~55% of a brand-colour background.
The left ~45% stays calm because the live theme writes the collection title + description over it on
desktop (on mobile the 3:1 banner shows first and the text sits underneath), so no headline is baked in.

Usage:  python3 -I tools/poster_banners.py <download_dir> <out_dir>
  download_dir: where the product images are (downloaded with curl from the URLs in PICKS)
  out_dir:      where foxy-header-<handle>.jpg files are written
"""
import hashlib, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1800, 600
INK = (29, 18, 64); PURPLE = (122, 43, 245); ORANGE = (255, 106, 19); PINK = (255, 45, 135); CREAM = (255, 244, 234)
CDN = 'https://cdn.shopify.com/s/files/1/1774/9115/'

# handle -> (collection title, accent, [poster image paths under CDN]); order = hero first, then outwards
PICKS = {
 'celebrity-posters': ('Celebrity Posters', PINK, [
   'products/TYSON_20FURY_20-_20Poster_20Only.jpg', 'products/Cristiano_20Ronaldo_201_20-_20POSTER_20ONLY.jpg',
   'products/KOBE_20BRYANT_202_20-_20POSTER_20ONLY.jpg', 'files/TaylorSwift.jpg',
   'files/Eminem_48ce7a7a-f4d4-4eb9-9aba-fcf8bb89fa8d.jpg', 'products/Keanu_20Reeves_203_20-_20POSTER_20ONLY.jpg',
   'products/LANA_20DEL_20REY_20_1_20-_20POSTER_20ONLY.jpg']),
 'football-star-posters': ('Football Star Posters', ORANGE, [
   'products/Cristiano_20Ronaldo_201_20-_20POSTER_20ONLY.jpg', 'products/KYLIAN_20MBAPPE_202_20-_20POSTER_20ONLY.jpg',
   'products/KENNY_20DALGLISH_20-_20POSTER_20ONLY.jpg', 'products/HENRIK_20LARSSON_20-_20Poster_20Only.jpg',
   'products/BOBBY_20MOORE_20__20PELE_20-_20Poster_20Only.jpg', 'products/JORDAN_20PICKFORD_20-_20POSTER_20ONLY.jpg',
   'files/CristianoRonaldoTopFootballer2023AutographedPrintLandscape.jpg']),
 'music-star-posters': ('Music Star Posters', PINK, [
   'products/LANA_20DEL_20REY_20_1_20-_20POSTER_20ONLY.jpg', 'files/TaylorSwift.jpg',
   'files/Adele_06ce0487-a112-41d6-9326-cd836e9524d5.jpg', 'files/Eminem_48ce7a7a-f4d4-4eb9-9aba-fcf8bb89fa8d.jpg',
   'files/CentralCee.jpg', 'files/Madonna_eee13961-82e0-4168-82e2-bee98817735e.jpg',
   'products/Robbie_Williams-Black.jpg']),
 'film-star-posters': ('Film Star Posters', PURPLE, [
   'products/Keanu_20Reeves_203_20-_20POSTER_20ONLY.jpg',
   'products/Dylan_20O_Brien_202_20-_20POSTER_20ONLY_3659413c-fd2a-4ba6-87a3-9177f5fb0898.jpg',
   'products/COLUMBO_PETER-Silver.jpg',
   'products/Terminator_2-Silver.jpg', 'products/David_Tennant-Black.jpg',
   'files/THE_GREATEST_SHOWMAN___35102.jpg']),
 'tv-star-posters': ('TV Star Posters', ORANGE, [
   'products/TOM_20HARDY_202_20-_20POSTER_20ONLY.jpg', 'products/VERA_20LYNN_20-_20POSTER_20ONLY.jpg',
   'products/STEPHEN_20MERCHANT_20RICKY_20GERVAIS_20AND_20KARL_20PILKINGTON_202_20-_20POSTER_20ONLY.jpg',
   'products/JEFFREY_20DEAN_20MORGAN_202_20-_20POSTER_20ONLY.jpg',
   'products/ANDREW_20LINCOLN_20__20NORMAN_20REEDUS_202_20-_20POSTER_20ONLY.jpg',
   'files/SusanBoyleM935-BlackFrame__85834.jpg']),
 'nfl-american-football-posters': ('NFL & American Football Star Posters', ORANGE, [
   'products/PEYTON_20MANNING_202_20-_20POSTER_20ONLY.jpg', 'products/NICK_20FOLES_20_1_20-_20POSTER_20ONLY.jpg',
   'products/Julio_20Jones_201_20-_20POSTER_20ONLY.jpg', 'products/ODELL_20BECKHAM_20JR_20_1_20-_20POSTER_20ONLY.jpg',
   'products/RUSSELL_20WILSON_202_20-_20POSTER_20ONLY.jpg', 'products/Dak_20Prescott_202_20-_20POSTER_20ONLY.jpg']),
 'boxing-star-posters': ('Boxing Star Posters', ORANGE, [
   'products/TYSON_20FURY_20-_20Poster_20Only.jpg', 'products/ROCKY_20MARCIANO_20-_20Poster_20Only.jpg',
   'products/MUHAMMAD_20ALI_20__20GEORGE_20FOREMAN_20-_20Poster_20Only.jpg', 'products/NIGEL_20BENN_20-_20Poster_20Only.jpg',
   'files/OleksandrUsyktopboxerAutographedPrintLandscape.jpg', 'files/CaneloAlvareztopboxerAutographedPrintLandscape.jpg',
   'products/TYSON_20FURY_202_20-_20Poster_20Only.jpg']),
 'ufc-mma-wrestling-posters': ('UFC, MMA & Wrestling Posters', PINK, [
   'products/CONOR_20McGREGOR_202_20-_20POSTER_20ONLY.jpg', 'products/Israel_20Adesanya_20-_20POSTER_20ONLY.jpg',
   'products/Michael_20Bisping_20-_20POSTER_20ONLY.jpg', 'products/Rose_20Namajunas_20-_20POSTER_20ONLY.jpg',
   'files/MaxHolloway.jpg', 'files/LeonEdwards.jpg']),
 'darts-snooker-star-posters': ('Darts & Snooker Star Posters', PURPLE, [
   'files/LukeLittlerworlddartschampion2026.jpg', 'products/JUDD_TRUMP_2_-_POSTER_ONLY.jpg',
   'products/STEVE_DAVIS_-_POSTER_ONLY.jpg', 'products/Michael_Van_Gerwen-Black.jpg', 'products/Gary_Anderson-Black.jpg']),
 'cricket-star-posters': ('Cricket Star Posters', ORANGE, [
   'products/JOE_20ROOT_20__20BEN_20STOKES_20-_20Poster_20Only.jpg', 'products/JAMES_20ANDERSON_20-_20Poster_20Only.jpg',
   'products/VIRAT_20KOHLI_20-_20Poster_20Only.jpg', 'products/ANDREW_20FLINTOFF_202_20-_20Poster_20Only.jpg',
   'products/SHANE_20WARNE-_20POSTER_20ONLY.jpg', 'products/IAN_20BOTHAM_20-_20Poster_20Only.jpg',
   'products/JONNY_20BAIRSTOW-_20POSTER_20ONLY.jpg']),
 'rugby-star-posters': ('Rugby Star Posters', PINK, [
   'files/henrypollockengland.jpg', 'products/DAN_20CARTER_202_20-_20POSTER_20ONLY.jpg',
   'files/finnrussellscotland.jpg', 'products/DAN_20BIGGAR_201_20-_20POSTER_20ONLY.jpg',
   'files/marcussmithengland.jpg', 'files/jamiegeorgeengland.jpg', 'files/henrysladeengland.jpg']),
 'golf-star-posters': ('Golf Star Posters', ORANGE, [
   'products/JORDAN_20SPIETH_20-_20POSTER_20ONLY.jpg', 'products/JUSTIN_20ROSE_202_20-_20POSTER_20ONLY.jpg',
   'products/JOHN_20DALY_20-_20POSTER_20ONLY.jpg', 'products/LUKE_20DONALD_20-_20POSTER_20ONLY.jpg',
   'products/PHIL_20MICKELSON_20-_20POSTER_20ONLY.jpg', 'products/JASON_20DAY_20-_20POSTER_20ONLY.jpg',
   'products/TOM_20WATSON_20-_20POSTER_20ONLY.jpg']),
 'tennis-star-posters': ('Tennis Star Posters', PINK, [
   'files/RafaelNadalM626-BlackFrame__14994.jpg', 'products/NOVAK_20DJOKOVIC_20_1_20-_20POSTER_20ONLY.jpg',
   'products/TIM_20HENMAN_20-_20POSTER_20ONLY.jpg', 'files/SteffiGrafM646-BlackFrame__54394.jpg',
   'products/JOHN_20MCENROE_202_20-_20POSTER_20ONLY.jpg', 'files/AnnaKournikovaM539-BlackFrame__24858.jpg',
   'products/JIMMY_20CONNORS_202_20-_20POSTER_20ONLY.jpg']),
 'horse-racing-star-posters': ('Horse Racing Star Posters', PURPLE, [
   'products/FRANKIE_20DETTORI_202_20-_20POSTER_20ONLY.jpg', 'files/APMcCOY-BLACKFRAME__29558.jpg',
   'files/RUBYWALSH-BLACKFRAME__07477.jpg', 'products/LESTER_20PIGGOTT_20-_20POSTER_20ONLY.jpg',
   'products/HAYLEY_20TURNER_202_20-_20POSTER_20ONLY.jpg', 'files/ZARAPHILLIPS_1_-BLACKFRAME__80811.jpg',
   'products/BARRY_20GERAGHTY_202_20-_20POSTER_20ONLY.jpg']),
 'f1-motorsport-star-posters': ('F1 & Motorsport Star Posters', ORANGE, [
   'products/AYRTON_20SENNA_20HITCHING_20-_20POSTER_20ONLY.jpg', 'products/TOTO_20WOLFF_202_20-_20POSTER_20ONLY.jpg',
   'files/LandoNorrisF1DriverAutographedPrintLandscape.jpg', 'files/LewisHamiltonF1DriverAutographedPrintLandscape.jpg',
   'files/GeorgeRussellF1DriverAutographedPrintLandscape.jpg', 'files/OscarPiastriF1DriverAutographedPrintLandscape.jpg']),
 'athletics-olympic-star-posters': ('Athletics & Olympic Star Posters', PURPLE, [
   'products/MARK_20CAVENDISH_20-_20POSTER_20ONLY.jpg', 'products/TOM_20DALEY_20-_20Poster_20Only.jpg',
   'products/GERAINT_20THOMAS_20-_20POSTER_20ONLY.jpg', 'files/UsainBolt.jpg', 'files/NadiaCoMAneci.jpg',
   'products/ALISTAIR_20__20JONNY_20BROWNLEE_20_1_20-_20POSTER_20ONLY.jpg', 'files/MAXWHITLOCK-BLACKFRAME__57229.jpg']),
 'basketball-baseball-hockey-posters': ('Basketball, Baseball & Ice Hockey Posters', ORANGE, [
   'products/KOBE_20BRYANT_20_1_20-_20POSTER_20ONLY.jpg', 'products/LARRY_20BIRD_202_20-_20POSTER_20ONLY.jpg',
   'products/KAWHI_20LEONARD_20_1_20-_20POSTER_20ONLY.jpg', 'files/AllenIversoncopy2-WhiteFrame__38951.jpg',
   'files/Zdeno_Chara_M1257_-_Print_Only__48073.jpg', 'files/Vladislav_Tretiak_M1253_-_Gold_Frame__56418.jpg',
   'products/MICHAEL_20JORDAN_20__20SCOTTIE_20PIPPEN_202_20-_20POSTER_20ONLY.jpg']),
 'icons-legends-posters': ('Authors, Scientists & Icons Posters', PINK, [
   'files/StephenKingM275-WhiteFrame__82023.jpg', 'files/ElonMusk-BlackFrame__61133.jpg',
   'files/AgathaChristieM182-BlackFrame__74820.jpg', 'files/Stephen_Hawking_M452_-_Print_Only__30198.jpg',
   'files/RichardFeynmanM449-BlackFrame__15489.jpg', 'files/MichaelFaradayM446-BlackFrame__38521.jpg',
   'files/RosalindElsieFranklinM451-BlackFrame__01932.jpg']),
}

def local_name(rel):
    url = CDN + rel
    return hashlib.md5(url.encode()).hexdigest()[:12] + os.path.splitext(rel)[1].lower()

def download(dl_dir):
    os.makedirs(dl_dir, exist_ok=True)
    for _, _, rels in PICKS.values():
        for rel in rels:
            p = os.path.join(dl_dir, local_name(rel))
            if not os.path.exists(p):
                subprocess.run(['curl', '-sS', '-f', '-o', p, CDN + rel + '?width=1200'], check=True)

# ---------- crop the print (black mat) out of a product photo ----------
def _runs(mask):
    m = mask.astype(np.int32); best = np.zeros(m.shape[1], int); cur = np.zeros(m.shape[1], int)
    for row in m:
        cur = (cur + 1) * row; best = np.maximum(best, cur)
    return best

def crop_print(path, frac=0.3, thr=70):
    im = Image.open(path).convert('RGB')
    small = im.copy(); small.thumbnail((600, 600)); s = im.width / small.width
    dark = np.asarray(small).astype(int).max(axis=2) < thr
    h, w = dark.shape
    cols = np.where(_runs(dark) >= frac * h)[0]; rows = np.where(_runs(dark.T) >= frac * w)[0]
    if len(cols) < 2 or len(rows) < 2:
        return im
    x0, x1, y0, y1 = cols[0], cols[-1] + 1, rows[0], rows[-1] + 1
    for _ in range(3):  # peel off edges that are not mostly black mat (floor, wall, frame lip)
        while y1 - y0 > 10 and dark[y0, x0:x1].mean() < 0.5: y0 += 1
        while y1 - y0 > 10 and dark[y1 - 1, x0:x1].mean() < 0.5: y1 -= 1
        while x1 - x0 > 10 and dark[y0:y1, x0].mean() < 0.5: x0 += 1
        while x1 - x0 > 10 and dark[y0:y1, x1 - 1].mean() < 0.5: x1 -= 1
    if (x1 - x0) < w * 0.3 or (y1 - y0) < h * 0.3:
        return im
    return im.crop((int(x0 * s), int(y0 * s), int(x1 * s), int(y1 * s)))

# ---------- framed print with shadow ----------
FRAMES = {
    'black': [(18, 18, 20), (58, 58, 64), (8, 8, 10)],
    'gold': [(176, 136, 58), (236, 204, 120), (120, 88, 30)],
    'silver': [(160, 162, 168), (226, 228, 232), (104, 106, 112)],
}

def framed(print_im, height, frame='black'):
    ar = print_im.width / print_im.height
    ph = int(height); pw = int(round(ph * ar))
    art = print_im.resize((pw, ph), Image.LANCZOS)
    t = max(8, int(height * 0.028))  # moulding width
    base, light, dark = FRAMES[frame]
    fw, fh = pw + 2 * t, ph + 2 * t
    fr = Image.new('RGB', (fw, fh), base); d = ImageDraw.Draw(fr)
    # bevel: light top/left, dark bottom/right, thin inner lip
    d.polygon([(0, 0), (fw, 0), (fw - t, t), (t, t), (t, fh - t), (0, fh)], fill=base)
    for i in range(t):
        a = i / t
        c = tuple(int(light[k] * (1 - a) + base[k] * a) for k in range(3))
        d.line([(i, i), (fw - i, i)], fill=c); d.line([(i, i), (i, fh - i)], fill=c)
        c2 = tuple(int(dark[k] * (1 - a) + base[k] * a) for k in range(3))
        d.line([(i, fh - 1 - i), (fw - i, fh - 1 - i)], fill=c2); d.line([(fw - 1 - i, i), (fw - 1 - i, fh - i)], fill=c2)
    fr.paste(art, (t, t))
    d.rectangle([t - 1, t - 1, t + pw, t + ph], outline=dark, width=1)
    # glass sheen
    sheen = Image.new('L', (fw, fh), 0); sd = ImageDraw.Draw(sheen)
    sd.polygon([(int(fw * 0.55), t), (int(fw * 0.75), t), (int(fw * 0.25), fh - t), (int(fw * 0.05), fh - t)], fill=22)
    fr = Image.composite(Image.new('RGB', (fw, fh), (255, 255, 255)), fr, sheen)
    return fr.convert('RGBA')

def place(canvas, piece, cx, cy, angle):
    rot = piece.rotate(angle, resample=Image.BICUBIC, expand=True)
    pad = 60
    sh = Image.new('RGBA', (rot.width + 2 * pad, rot.height + 2 * pad), (0, 0, 0, 0))
    alpha = rot.split()[3].point(lambda v: int(v * 0.62))
    sh.paste(Image.new('RGBA', rot.size, (8, 4, 24, 255)), (pad, pad), alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    x = int(cx - rot.width / 2); y = int(cy - rot.height / 2)
    canvas.alpha_composite(sh, (x - pad + 12, y - pad + 18)) if x - pad + 12 >= 0 else canvas.paste(sh, (x - pad + 12, y - pad + 18), sh)
    canvas.paste(rot, (x, y), rot)

# ---------- background ----------
def background(accent):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = (xx / W)[..., None]
    left = np.array(INK, np.float32); right = np.array((52, 22, 110), np.float32)
    img = left * (1 - t) + right * t
    # accent glow behind the posters
    g = np.exp(-(((xx - 1320) / 620) ** 2 + ((yy - 330) / 360) ** 2))[..., None]
    img = img * (1 - 0.55 * g) + np.array(accent, np.float32) * (0.55 * g)
    # second softer glow, top right
    g2 = np.exp(-(((xx - 1750) / 380) ** 2 + ((yy + 40) / 260) ** 2))[..., None]
    img = img * (1 - 0.25 * g2) + np.array(PURPLE, np.float32) * (0.25 * g2)
    bg = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert('RGBA')
    # subtle light beams fanning from the top right
    beams = Image.new('L', (W, H), 0); bd = ImageDraw.Draw(beams)
    for i, ang in enumerate(range(100, 200, 14)):
        a = math.radians(ang)
        ox, oy = 1500, -120
        p1 = (ox + 2400 * math.cos(a - 0.035), oy + 2400 * math.sin(a - 0.035))
        p2 = (ox + 2400 * math.cos(a + 0.035), oy + 2400 * math.sin(a + 0.035))
        bd.polygon([(ox, oy), p1, p2], fill=18 if i % 2 else 10)
    beams = beams.filter(ImageFilter.GaussianBlur(10))
    bg = Image.composite(Image.new('RGBA', (W, H), CREAM + (255,)), bg, beams)
    # faint halftone dots, bottom left, so the calm side isn't flat
    dots = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(dots)
    for yv in range(330, H + 20, 22):
        for xv in range(0, 700, 22):
            f = max(0.0, 1 - math.hypot(xv / 700, (H - yv) / 270))
            r = 1 + 4.5 * f
            if f > 0.02:
                dd.ellipse([xv - r, yv - r, xv + r, yv + r], fill=accent + (int(26 + 40 * f),))
    bg.alpha_composite(dots)
    return bg

# Row layout: hero in the middle, the rest alternate right / left outwards, outer ones smaller and
# tucked slightly behind. Sizes shrink until every print shows at least ~72% of its width.
REGION = (750, 1785)
RANK_SCALE = [1.0, 0.86, 0.86, 0.74, 0.74, 0.64, 0.64]
RANK_ANGLE = [0, -2, 2, -4, 4, -6, 6]
FRAME_CYCLE = ['black', 'gold', 'silver', 'silver', 'gold', 'black', 'black']

def build(handle, dl_dir, out_dir, count=5):
    title, accent, rels = PICKS[handle]
    rels = rels[:count]
    n = len(rels)
    canvas = background(accent)
    prints = [crop_print(os.path.join(dl_dir, local_name(r))) for r in rels]
    def sizes(k):
        out = []
        for i, pr in enumerate(prints):
            ar = pr.width / pr.height
            area = 0.8 * (430 * k * RANK_SCALE[i]) ** 2 * (1.45 if ar > 1.1 else 1.0)  # landscapes a bit bigger
            h = min(math.sqrt(area / ar), 450 * k * RANK_SCALE[i])
            out.append((h, h * ar * 1.06))   # approx framed width
        return out
    # left-to-right order of ranks, e.g. n=5 -> [4, 2, 0, 1, 3]
    order = [r for r in range(n - 1, 0, -1) if r % 2 == 0] + [0] + [r for r in range(1, n) if r % 2 == 1]
    k = 1.0
    span = REGION[1] - REGION[0]
    while True:
        sz = sizes(k)
        widths = [sz[r][1] for r in order]
        total = sum(widths)
        # each join hides part of the print behind (the higher rank); wide prints absorb more of it
        covered = [widths[j] if order[j] > order[j + 1] else widths[j + 1] for j in range(n - 1)]
        f = max(0.0, (total - span) / max(1.0, sum(covered)))
        if f <= 0.40 or k < 0.6:
            break
        k -= 0.02
    ovs = [f * c for c in covered]
    x = REGION[0] + max(0.0, (span - (total - sum(ovs))) / 2)
    centres = {}
    for j, (r, w) in enumerate(zip(order, widths)):
        centres[r] = x + w / 2
        x += w - (ovs[j] if j < n - 1 else 0)
    # draw outermost first so inner prints overlap the outer ones
    for r in sorted(range(n), key=lambda r: -r):
        h = sz[r][0]
        cy = 302 + (1 - RANK_SCALE[r]) * 30
        place(canvas, framed(prints[r], h, FRAME_CYCLE[r]), centres[r], cy, RANK_ANGLE[r])
    # keep the text side calm: soft ink fade over the far left
    fade = Image.new('L', (W, 1)); fade.putdata([int(max(0, 1 - x / 760) ** 1.6 * 150) for x in range(W)])
    fade = fade.resize((W, H))
    canvas = Image.composite(Image.new('RGBA', (W, H), INK + (255,)), canvas, fade)
    out = os.path.join(out_dir, f'foxy-header-{handle}.jpg')
    canvas.convert('RGB').save(out, quality=88, optimize=True, progressive=True)
    return out

if __name__ == '__main__':
    dl_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    download(dl_dir)
    only = sys.argv[3:] or list(PICKS)
    for h in only:
        print(build(h, dl_dir, out_dir))
