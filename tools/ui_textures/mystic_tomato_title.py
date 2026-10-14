"""Banner "Versione Pomodoro Mistico" (Mystic Tomato HD, card 4930) at the top of the title screen, one version per language.

The title backdrop is made of 20 128x64 textures (title_menu_i.ehp: main_title00001..00020, reverse order:
1 is bottom right). The banner sits in the top row, above "SHONEN JUMP'S", and falls in tiles
18 and 19 (x 128-384 of the PSP screen). The base pack stays WITHOUT banner (original tiles): each
language's banner lives in that language's module, modules/<language>/intro/title_screen/, and compose_pack.py copies it only
for the chosen language. The originals of the two tiles are in comparisons/backup_before_title/.

usage: mystic_tomato_title.py [LANGUAGE ...]               generates the modules (default: all) and puts the original tiles back in the base pack
       mystic_tomato_title.py --apply PACK LANGUAGE        writes the LANGUAGE banner directly into a pack (e.g. PPSSPP's)
"""
import json, os, shutil, sys
import cv2, numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
PACK = os.path.join(ROOT, 'PSP', 'TEXTURES', 'ULES00600')
BACKUP = os.path.join(ROOT, 'comparisons', 'backup_before_title')
FONT = os.path.join(HERE, '..', 'alt_fonts', 'downloaded', 'PTSans-Bold.ttf')
ID_CARD = 4930
MODULES = os.path.join(ROOT, 'PSP', 'TEXTURES', 'modules')
# (small word, name of the card in the game's language, does the small word go after the name?)
# Formulas like the Pokemon titles: it "Versione Rossa", fr "Version Rouge", es "Edición Roja", de "Rote Edition", en "Red Version"
TESTI = {'it': ('VERSIONE', 'POMODORO MISTICO', False), 'fr': ('VERSION', 'TOMATE MYSTIQUE', False),
         'de': ('EDITION', 'MYSTISCHE TOMATE', True), 'es': ('EDICIÓN', 'TOMATE MÍSTICO', False),
         'en': ('VERSION', 'MYSTIC TOMATO', True)}
FLAG_W, FLAG_H = 32, 21   # pack px
S = 4                      # pack pixel per PSP pixel
TILES = (19, 18)         # from left to right, at x = 128 and 256 (PSP units), top row
CENTER_X = 480 * S // 2    # the logo is centred on the screen


def tiles():
    inv = json.load(open(os.path.join(ROOT, 'tools', 'analysis', 'inventory.json')))
    m = {e['member']: e['pack_file'] for e in inv if e['file'] == 'title_menu/title_menu_i.ehp'}
    return [m['main_title%05d.gim' % i] for i in TILES]


def pomodoro():
    """Cut-out of the Mystic Tomato from the HD large card (the art is split into 3 pieces in the atlas)."""
    A = Image.open(os.path.join(PACK, 'cards', 'large', f'{ID_CARD}.png')).convert('RGB')
    art = Image.new('RGB', (312, 312))
    art.paste(A.crop((0, 0, 312, 240)), (0, 0))
    art.paste(A.crop((320, 0, 512, 72)), (0, 240))
    art.paste(A.crop((320, 80, 440, 152)), (192, 240))
    a = np.array(art)
    mask = np.zeros(a.shape[:2], np.uint8)
    cv2.grabCut(a[:, :, ::-1].copy(), mask, (25, 25, 262, 270), np.zeros((1, 65)), np.zeros((1, 65)), 10, cv2.GC_INIT_WITH_RECT)
    m = ((mask == 1) | (mask == 3)).astype(np.uint8)
    n, l, st, _ = cv2.connectedComponentsWithStats(m)
    m = (l == 1 + np.argmax(st[1:, 4])).astype(np.uint8)
    f = np.zeros_like(m)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(f, cs, -1, 1, -1)   # fills the holes (the dark mouth)
    im = Image.fromarray(np.dstack([a, f * 255]))
    return im.crop(im.getbbox())


def con_outline(im, black, white):
    """Black outline of `black` px and soft white halo of `white` px around the silhouette of im (RGBA)."""
    p = black + white * 2 + 2
    base = Image.new('RGBA', (im.width + 2 * p, im.height + 2 * p))
    base.paste(im, (p, p))
    al = base.getchannel('A')
    black_a = al.filter(ImageFilter.MaxFilter(2 * black + 1))
    alone = black_a.filter(ImageFilter.MaxFilter(2 * white + 1)).filter(ImageFilter.GaussianBlur(white / 2))
    out = Image.new('RGBA', base.size)
    out.paste((255, 255, 255, 255), mask=alone)
    out.paste((10, 10, 20, 255), mask=black_a)
    out.alpha_composite(base)
    return out


def silhouette(w, h, sk):
    """L mask of a plate with slanted sides (like the points of the TAG FORCE logo), supersampled x3."""
    k = 3
    m = Image.new('L', (w * k, h * k), 0)
    ImageDraw.Draw(m).polygon([(sk * k, 0), (w * k, 0), ((w - sk) * k, h * k), (0, h * k)], fill=255)
    return m


def scia(mask, black, white, col_border, col_alone=(255, 255, 255)):
    """Coloured border of `black` px and soft halo of `white` px around an L mask."""
    border = mask.filter(ImageFilter.MaxFilter(2 * black + 1))
    alone = border.filter(ImageFilter.MaxFilter(2 * white + 1)).filter(ImageFilter.GaussianBlur(white / 2)) if white else border
    out = Image.new('RGBA', mask.size)
    out.paste(col_alone + (255,), mask=alone)
    out.paste(col_border + (255,), mask=border)
    return out


def gradient(size, top, bottom):
    g = Image.new('RGB', size)
    d = ImageDraw.Draw(g)
    for y in range(size[1]):
        t = y / max(1, size[1] - 1)
        d.line([(0, y), (size[0], y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return g


def text_metallic(s, body, top, bottom):
    """Lettering with vertically graded fill and dark outline."""
    k = 3
    f = ImageFont.truetype(FONT, body * k)
    bb = f.getbbox(s)
    p = 5 * k
    w, h = bb[2] - bb[0] + 2 * p, bb[3] - bb[1] + 2 * p
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).text((p - bb[0], p - bb[1]), s, font=f, fill=255)
    cont = scia(m, 3 * k // 2 + 1, 0, (60, 0, 12))   # contorno scuro
    cont.alpha_composite(Image.composite(gradient((w, h), top, bottom).convert('RGBA'), Image.new('RGBA', (w, h)), m))
    return cont


def flag(language):
    """Flag of the language (RGBA, FLAG_W x FLAG_H) with white border and dark outline. Spain without coat of arms, en = Union Jack."""
    k = 4
    w, h = FLAG_W * k, FLAG_H * k
    f = Image.new('RGB', (w, h))
    d = ImageDraw.Draw(f)
    tre = lambda cols, ver: [d.rectangle([i * w // 3, 0, (i + 1) * w // 3, h], fill=c) if ver else d.rectangle([0, i * h // 3, w, (i + 1) * h // 3], fill=c) for i, c in enumerate(cols)]
    if language == 'it':
        tre([(0, 146, 70), (255, 255, 255), (206, 43, 55)], True)
    elif language == 'fr':
        tre([(0, 85, 164), (255, 255, 255), (239, 65, 53)], True)
    elif language == 'de':
        tre([(0, 0, 0), (221, 0, 0), (255, 206, 0)], False)
    elif language == 'es':
        d.rectangle([0, 0, w, h], fill=(170, 21, 27))
        d.rectangle([0, h // 4, w, 3 * h // 4], fill=(241, 191, 0))
    else:
        d.rectangle([0, 0, w, h], fill=(1, 33, 105))
        for col, lw in (((255, 255, 255), h // 4), ((200, 16, 46), h // 8)):
            d.line([(0, 0), (w, h)], fill=col, width=lw)
            d.line([(0, h), (w, 0)], fill=col, width=lw)
        d.rectangle([0, h * 3 // 8, w, h * 5 // 8], fill=(255, 255, 255))
        d.rectangle([w * 2 // 5, 0, w * 3 // 5, h], fill=(255, 255, 255))
        d.rectangle([0, h * 7 // 16, w, h * 9 // 16], fill=(200, 16, 46))
        d.rectangle([w * 9 // 20, 0, w * 11 // 20, h], fill=(200, 16, 46))
    f = f.convert('RGBA')
    g = Image.new('RGBA', (w + 4 * k, h + 4 * k), (255, 255, 255, 255))
    g.alpha_composite(f, (2 * k, 2 * k))
    d2 = ImageDraw.Draw(g)
    d2.rectangle([0, 0, g.width - 1, g.height - 1], outline=(40, 20, 30, 255), width=k)
    return g.resize((FLAG_W + 4, FLAG_H + 4), Image.LANCZOS)


def banner(language):
    k = 3   # plate oversampling
    tom = con_outline(pomodoro().resize((84, 84), Image.LANCZOS), 2, 2)
    small, name, after = TESTI[language]
    v = text_metallic(small, 21, (255, 236, 150), (255, 190, 40))
    t = text_metallic(name, 37, (255, 255, 255), (214, 224, 248))
    gap = 5 * k
    tw = v.width + gap + t.width
    # red plate like the TAG FORCE logo: inner white fillet, light-blue border, white halo
    H, sk = 56, 14
    W = 44 + tw // k + 28 + sk + FLAG_W + 10   # tomato + text + margin, the plate adapts to the length
    core = silhouette(W, H, sk)
    pad = 7 * k
    big = Image.new('L', (core.width + 2 * pad, core.height + 2 * pad), 0)
    big.paste(core, (pad, pad))
    out = scia(big, 3 * k, 4 * k, (36, 110, 232))
    red = Image.new('RGBA', core.size)
    red.paste(gradient(core.size, (255, 40, 40), (150, 0, 22)), mask=core)
    light = Image.new('L', core.size, 0)
    ImageDraw.Draw(light).rectangle([0, 0, core.width, core.height // 2 - 2], fill=46)
    red.paste((255, 255, 255, 255), mask=ImageChops.multiply(light, core))   # reflection on the upper half
    out.alpha_composite(red, (pad, pad))
    fillet = ImageChops.subtract(core, core.filter(ImageFilter.MinFilter(2 * k + 1)))
    fl = Image.new('L', big.size, 0)
    fl.paste(fillet, (pad, pad))
    out.paste((255, 255, 255, 255), mask=fl)
    # texts in the part free of the tomato
    zx = pad + 44 * k
    zw = out.width - zx - pad - sk * k - (FLAG_W + 10) * k
    x = zx + (zw - tw) // 2
    a, b = (t, v) if after else (v, t)
    out.alpha_composite(a, (x, (out.height - a.height) // 2 + (0 if after else k)))
    out.alpha_composite(b, (x + a.width + gap, (out.height - b.height) // 2 + (k if after else 0)))
    plate = out.resize((out.width // k, out.height // k), Image.LANCZOS)
    fl = flag(language)
    plate.alpha_composite(fl, (plate.width - 7 - sk - fl.width, (plate.height - fl.height) // 2))
    r = Image.new('RGBA', (plate.width + 40, max(tom.height, plate.height)))
    r.alpha_composite(plate, (40, (r.height - plate.height) // 2))
    r.alpha_composite(tom, (0, (r.height - tom.height) // 2))
    return r


def tiles_banner(language):
    """[(relative path, image)] of the tiles with the banner of `language`."""
    rel = tiles()
    os.makedirs(BACKUP, exist_ok=True)
    canvas = Image.new('RGBA', (len(rel) * 128 * S, 64 * S))
    for i, r in enumerate(rel):
        orig = os.path.join(BACKUP, os.path.basename(r))
        if not os.path.exists(orig):
            shutil.copy(os.path.join(PACK, r), orig)
        canvas.paste(Image.open(orig).convert('RGBA'), (i * 128 * S, 0))
    b = banner(language)
    canvas.alpha_composite(b, (CENTER_X - 128 * S - b.width // 2, 6))
    return [(r, canvas.crop((i * 128 * S, 0, (i + 1) * 128 * S, 64 * S))) for i, r in enumerate(rel)]


def write_file(root, language):
    for r, im in tiles_banner(language):
        os.makedirs(os.path.dirname(os.path.join(root, r)), exist_ok=True)
        im.save(os.path.join(root, r))


def main(args):
    if args and args[0] == '--apply':
        write_file(args[1], args[2])
        return
    for r in tiles():   # base pack without banner (in-place copy: the hard links of the composed packs stay valid)
        shutil.copyfile(os.path.join(BACKUP, os.path.basename(r)), os.path.join(PACK, r))
    for l in args or TESTI:
        write_file(os.path.join(MODULES, l), l)
        print('modulo', l, TESTI[l][1])


if __name__ == '__main__':
    main(sys.argv[1:])
