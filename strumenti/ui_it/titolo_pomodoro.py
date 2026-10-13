"""Banner "Versione Pomodoro Mistico" (Pomodoro Mistico HD, carta 4930) in cima alla schermata del titolo, una versione per lingua.

Il fondale del titolo e' fatto da 20 texture 128x64 (title_menu_i.ehp: main_title00001..00020, ordine inverso:
la 1 e' in basso a destra). Il banner sta nella fila in alto, sopra "SHONEN JUMP'S", e cade nelle tessere
18 e 19 (x 128-384 dello schermo PSP). Il pack di base resta SENZA banner (tessere originali): il banner di ogni
lingua vive nel modulo di quella lingua, moduli/<lingua>/intro/title_screen/, e componi_pack.py lo copia solo
per la lingua scelta. Gli originali delle due tessere sono in confronti/backup_prima_titolo/.

uso: titolo_pomodoro.py [LINGUA ...]               genera i moduli (default: tutte) e rimette le tessere originali nel pack di base
     titolo_pomodoro.py --applica PACK LINGUA      scrive il banner di LINGUA direttamente in un pack (es. quello di PPSSPP)
"""
import json, os, shutil, sys
import cv2, numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.normpath(os.path.join(AQUI, '..', '..'))
PACK = os.path.join(RADICE, 'PSP', 'TEXTURES', 'ULES00600')
BACKUP = os.path.join(RADICE, 'confronti', 'backup_prima_titolo')
FONT = os.path.join(AQUI, '..', 'font_alternativi', 'scaricati', 'PTSans-Bold.ttf')
ID_CARTA = 4930
MODULI = os.path.join(RADICE, 'PSP', 'TEXTURES', 'moduli')
# (parola piccola, nome della carta nella lingua del gioco, la parola piccola va dopo il nome?)
# Formule come i titoli Pokemon: it "Versione Rossa", fr "Version Rouge", es "Edición Roja", de "Rote Edition", en "Red Version"
TESTI = {'it': ('VERSIONE', 'POMODORO MISTICO', False), 'fr': ('VERSION', 'TOMATE MYSTIQUE', False),
         'de': ('EDITION', 'MYSTISCHE TOMATE', True), 'es': ('EDICIÓN', 'TOMATE MÍSTICO', False),
         'en': ('VERSION', 'MYSTIC TOMATO', True)}
FLAG_W, FLAG_H = 32, 21   # px del pack
S = 4                      # pixel del pack per pixel PSP
TESSERE = (19, 18)         # da sinistra a destra, a x = 128 e 256 (unita' PSP), fila in alto
CENTRO_X = 480 * S // 2    # il logo e' centrato sullo schermo


def tessere():
    inv = json.load(open(os.path.join(RADICE, 'strumenti', 'analisi', 'inventory.json')))
    m = {e['member']: e['pack_file'] for e in inv if e['file'] == 'title_menu/title_menu_i.ehp'}
    return [m['main_title%05d.gim' % i] for i in TESSERE]


def pomodoro():
    """Ritaglio del Pomodoro Mistico dalla carta grande HD (l'arte e' spezzata in 3 pezzi nell'atlante)."""
    A = Image.open(os.path.join(PACK, 'cards', 'large', f'{ID_CARTA}.png')).convert('RGB')
    arte = Image.new('RGB', (312, 312))
    arte.paste(A.crop((0, 0, 312, 240)), (0, 0))
    arte.paste(A.crop((320, 0, 512, 72)), (0, 240))
    arte.paste(A.crop((320, 80, 440, 152)), (192, 240))
    a = np.array(arte)
    mask = np.zeros(a.shape[:2], np.uint8)
    cv2.grabCut(a[:, :, ::-1].copy(), mask, (25, 25, 262, 270), np.zeros((1, 65)), np.zeros((1, 65)), 10, cv2.GC_INIT_WITH_RECT)
    m = ((mask == 1) | (mask == 3)).astype(np.uint8)
    n, l, st, _ = cv2.connectedComponentsWithStats(m)
    m = (l == 1 + np.argmax(st[1:, 4])).astype(np.uint8)
    f = np.zeros_like(m)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(f, cs, -1, 1, -1)   # riempie i buchi (la bocca scura)
    im = Image.fromarray(np.dstack([a, f * 255]))
    return im.crop(im.getbbox())


def con_contorno(im, nero, bianco):
    """Contorno nero di `nero` px e alone bianco morbido di `bianco` px attorno alla sagoma di im (RGBA)."""
    p = nero + bianco * 2 + 2
    base = Image.new('RGBA', (im.width + 2 * p, im.height + 2 * p))
    base.paste(im, (p, p))
    al = base.getchannel('A')
    nero_a = al.filter(ImageFilter.MaxFilter(2 * nero + 1))
    alone = nero_a.filter(ImageFilter.MaxFilter(2 * bianco + 1)).filter(ImageFilter.GaussianBlur(bianco / 2))
    out = Image.new('RGBA', base.size)
    out.paste((255, 255, 255, 255), mask=alone)
    out.paste((10, 10, 20, 255), mask=nero_a)
    out.alpha_composite(base)
    return out


def sagoma(w, h, sk):
    """Maschera L di una targa col lati obliqui (come le punte del logo TAG FORCE), supercampionata x3."""
    k = 3
    m = Image.new('L', (w * k, h * k), 0)
    ImageDraw.Draw(m).polygon([(sk * k, 0), (w * k, 0), ((w - sk) * k, h * k), (0, h * k)], fill=255)
    return m


def scia(mask, nero, bianco, col_bordo, col_alone=(255, 255, 255)):
    """Bordo colorato di `nero` px e alone morbido di `bianco` px attorno a una maschera L."""
    bordo = mask.filter(ImageFilter.MaxFilter(2 * nero + 1))
    alone = bordo.filter(ImageFilter.MaxFilter(2 * bianco + 1)).filter(ImageFilter.GaussianBlur(bianco / 2)) if bianco else bordo
    out = Image.new('RGBA', mask.size)
    out.paste(col_alone + (255,), mask=alone)
    out.paste(col_bordo + (255,), mask=bordo)
    return out


def sfumato(size, alto, basso):
    g = Image.new('RGB', size)
    d = ImageDraw.Draw(g)
    for y in range(size[1]):
        t = y / max(1, size[1] - 1)
        d.line([(0, y), (size[0], y)], fill=tuple(int(alto[i] + (basso[i] - alto[i]) * t) for i in range(3)))
    return g


def testo_metallico(s, corpo, alto, basso):
    """Scritta con riempimento sfumato in verticale e contorno scuro."""
    k = 3
    f = ImageFont.truetype(FONT, corpo * k)
    bb = f.getbbox(s)
    p = 5 * k
    w, h = bb[2] - bb[0] + 2 * p, bb[3] - bb[1] + 2 * p
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).text((p - bb[0], p - bb[1]), s, font=f, fill=255)
    cont = scia(m, 3 * k // 2 + 1, 0, (60, 0, 12))   # contorno scuro
    cont.alpha_composite(Image.composite(sfumato((w, h), alto, basso).convert('RGBA'), Image.new('RGBA', (w, h)), m))
    return cont


def bandiera(lingua):
    """Bandiera della lingua (RGBA, FLAG_W x FLAG_H) con bordo bianco e contorno scuro. Spagna senza stemma, en = Union Jack."""
    k = 4
    w, h = FLAG_W * k, FLAG_H * k
    f = Image.new('RGB', (w, h))
    d = ImageDraw.Draw(f)
    tre = lambda cols, ver: [d.rectangle([i * w // 3, 0, (i + 1) * w // 3, h], fill=c) if ver else d.rectangle([0, i * h // 3, w, (i + 1) * h // 3], fill=c) for i, c in enumerate(cols)]
    if lingua == 'it':
        tre([(0, 146, 70), (255, 255, 255), (206, 43, 55)], True)
    elif lingua == 'fr':
        tre([(0, 85, 164), (255, 255, 255), (239, 65, 53)], True)
    elif lingua == 'de':
        tre([(0, 0, 0), (221, 0, 0), (255, 206, 0)], False)
    elif lingua == 'es':
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


def banner(lingua):
    k = 3   # sovracampionamento della targa
    tom = con_contorno(pomodoro().resize((84, 84), Image.LANCZOS), 2, 2)
    piccola, nome, dopo = TESTI[lingua]
    v = testo_metallico(piccola, 21, (255, 236, 150), (255, 190, 40))
    t = testo_metallico(nome, 37, (255, 255, 255), (214, 224, 248))
    gap = 5 * k
    tw = v.width + gap + t.width
    # targa rossa come il logo TAG FORCE: filetto bianco interno, bordo azzurro, alone bianco
    H, sk = 56, 14
    W = 44 + tw // k + 28 + sk + FLAG_W + 10   # tomato + testo + margine, la targa si adatta alla lunghezza
    core = sagoma(W, H, sk)
    pad = 7 * k
    big = Image.new('L', (core.width + 2 * pad, core.height + 2 * pad), 0)
    big.paste(core, (pad, pad))
    out = scia(big, 3 * k, 4 * k, (36, 110, 232))
    rosso = Image.new('RGBA', core.size)
    rosso.paste(sfumato(core.size, (255, 40, 40), (150, 0, 22)), mask=core)
    luce = Image.new('L', core.size, 0)
    ImageDraw.Draw(luce).rectangle([0, 0, core.width, core.height // 2 - 2], fill=46)
    rosso.paste((255, 255, 255, 255), mask=ImageChops.multiply(luce, core))   # riflesso sulla meta' alta
    out.alpha_composite(rosso, (pad, pad))
    filetto = ImageChops.subtract(core, core.filter(ImageFilter.MinFilter(2 * k + 1)))
    fl = Image.new('L', big.size, 0)
    fl.paste(filetto, (pad, pad))
    out.paste((255, 255, 255, 255), mask=fl)
    # testi nella parte libera dal pomodoro
    zx = pad + 44 * k
    zw = out.width - zx - pad - sk * k - (FLAG_W + 10) * k
    x = zx + (zw - tw) // 2
    a, b = (t, v) if dopo else (v, t)
    out.alpha_composite(a, (x, (out.height - a.height) // 2 + (0 if dopo else k)))
    out.alpha_composite(b, (x + a.width + gap, (out.height - b.height) // 2 + (k if dopo else 0)))
    targa = out.resize((out.width // k, out.height // k), Image.LANCZOS)
    fl = bandiera(lingua)
    targa.alpha_composite(fl, (targa.width - 7 - sk - fl.width, (targa.height - fl.height) // 2))
    r = Image.new('RGBA', (targa.width + 40, max(tom.height, targa.height)))
    r.alpha_composite(targa, (40, (r.height - targa.height) // 2))
    r.alpha_composite(tom, (0, (r.height - tom.height) // 2))
    return r


def tessere_banner(lingua):
    """[(percorso relativo, immagine)] delle tessere con il banner di `lingua`."""
    rel = tessere()
    os.makedirs(BACKUP, exist_ok=True)
    tela = Image.new('RGBA', (len(rel) * 128 * S, 64 * S))
    for i, r in enumerate(rel):
        orig = os.path.join(BACKUP, os.path.basename(r))
        if not os.path.exists(orig):
            shutil.copy(os.path.join(PACK, r), orig)
        tela.paste(Image.open(orig).convert('RGBA'), (i * 128 * S, 0))
    b = banner(lingua)
    tela.alpha_composite(b, (CENTRO_X - 128 * S - b.width // 2, 6))
    return [(r, tela.crop((i * 128 * S, 0, (i + 1) * 128 * S, 64 * S))) for i, r in enumerate(rel)]


def scrivi(radice, lingua):
    for r, im in tessere_banner(lingua):
        os.makedirs(os.path.dirname(os.path.join(radice, r)), exist_ok=True)
        im.save(os.path.join(radice, r))


def main(args):
    if args and args[0] == '--applica':
        scrivi(args[1], args[2])
        return
    for r in tessere():   # pack di base senza banner (copia sul posto: gli hard link dei pack composti restano validi)
        shutil.copyfile(os.path.join(BACKUP, os.path.basename(r)), os.path.join(PACK, r))
    for l in args or TESTI:
        scrivi(os.path.join(MODULI, l), l)
        print('modulo', l, TESTI[l][1])


if __name__ == '__main__':
    main(sys.argv[1:])
