"""Simboli degli attributi (LIGHT, DARK, WATER, FIRE, EARTH, WIND, SPELL, TRAP, DIVINE) con la scritta nella lingua della carta.
Nel gioco la tabella delle icone (icon01.gim, uguale in tutte le lingue) ha la scritta inglese; sulle carte vere ogni lingua ha la sua
(LUCE, OSCURITA', ACQUA... / LUMIERE, TENEBRES... / LICHT, FINSTERNIS... / LUZ, OSCURIDAD...). Le parole sono quelle del gioco
(DLG_Text di cardinfo_xxx.ehp, indici 531-539, vedi lingue.py).
usage: attributi.py tabella LINGUA PACK OUT_PNG [CARDINFO.ehp]    icons_attribute_race.png con le scritte della lingua
       attributi.py carte  LINGUA PACK DIR_CARTE_PICCOLE         sostituisce l'icona sulle carte piccole (cards/small_<l>) sul posto
La tabella e' unica per installazione (stesso hash in tutte le lingue): con piu' lingue vince la prima."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import font_alt   # noqa: nessun font Apple
import lingue

ORDINE = ['LIGHT', 'DARK', 'WATER', 'FIRE', 'EARTH', 'WIND', 'SPELL', 'TRAP', 'DIVINE']
INDICE_DLG = {'LIGHT': 531, 'DARK': 532, 'WATER': 533, 'FIRE': 534, 'EARTH': 535, 'WIND': 536, 'DIVINE': 537, 'SPELL': 538, 'TRAP': 539}
# icone grandi 62x62 e piccole 45x45 nella tabella 512x512 del pack (cards/frame/icons_attribute_race.png)
GRANDI = {'LIGHT': (1, 274), 'DARK': (69, 274), 'WATER': (137, 274), 'FIRE': (205, 274), 'EARTH': (273, 274), 'WIND': (341, 274),
          'SPELL': (409, 274), 'TRAP': (341, 342), 'DIVINE': (409, 342)}
PICCOLE = {n: (48 * i, 432) for i, n in enumerate(ORDINE)}
# banda del testo: (y0, y1, x0, x1, altezza maiuscole, larghezza massima) relativi all'icona
BANDA = {62: (5, 18, 6, 56, 9.0, 40), 45: (3, 12, 5, 41, 6.0, 29)}
FONT = os.path.join(HERE, 'font_alternativi', 'static', 'Tinos-Bold.ttf')
SS = 8


def parole(cardinfo):
    d = lingue.dlg(cardinfo)
    return {n: d[INDICE_DLG[n]].upper() for n in ORDINE}


def pulisci(icona, banda):
    """cancella la scritta con l'inpainting: maschera = pixel molto chiari e poco saturi nella banda (piu' bordo)."""
    s = icona.shape[0]
    y0, y1, x0, x1, _, _ = banda
    rgb = icona[..., :3]
    mx, mn = rgb.max(-1).astype(int), rgb.min(-1).astype(int)
    chiaro = (mn >= 150) & ((mx - mn) < 80)
    m = np.zeros(chiaro.shape, np.uint8)
    m[y0:y1, x0:x1] = chiaro[y0:y1, x0:x1]
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=2)
    m[y1:] = 0                      # mai sopra il kanji
    out = cv2.inpaint(np.ascontiguousarray(rgb), m, 3, cv2.INPAINT_TELEA)
    # l'inpainting scurisce la zona ripulita (prende i colori scuri sotto la scritta): si riempie invece in verticale,
    # interpolando in ogni colonna tra il primo pixel non toccato sopra e quello sotto la scritta
    vert = rgb.astype(np.float32).copy()
    for x in range(m.shape[1]):
        col = np.where(m[:, x] > 0)[0]
        if not len(col):
            continue
        for run in np.split(col, np.where(np.diff(col) > 1)[0] + 1):
            a_, b_ = run[0] - 1, run[-1] + 1
            if a_ < 0 or b_ >= m.shape[0]:
                continue
            t = ((run - a_) / (b_ - a_)) ** 0.3          # il colore sotto la scritta pesa di piu' di quello sul bordo scuro sopra
            vert[run, x] = rgb[a_, x] * (1 - t)[:, None] + rgb[b_, x] * t[:, None]
    w = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.8)[..., None].clip(0, 1) * (m > 0).astype(np.float32)[..., None]
    out = np.where((m > 0)[..., None], vert * 0.85 + out.astype(np.float32) * 0.15, out).astype(np.uint8)
    res = icona.copy(); res[..., :3] = out
    return res


def disegna(icona, testo, banda):
    s = icona.shape[0]
    y0, y1, x0, x1, cap, wmax = banda
    f = ImageFont.truetype(FONT, int(round(cap / 0.66 * SS)))     # le maiuscole di Tinos sono circa 0,66 em
    asc = -f.getbbox('H', anchor='ls')[1]
    base = int(asc * 1.6)                                          # spazio sopra la linea di base per gli accenti
    W, H = int(f.getlength(testo)) + 8 * SS, base + int(asc * 0.5)
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).text((4 * SS, base), testo, font=f, fill=255, anchor='ls')
    xs = np.where(np.asarray(m).max(0) > 0)[0]
    m = m.crop((xs.min(), 0, xs.max() + 1, H))
    larg = min(m.width / SS, wmax)
    m = m.resize((max(1, round(larg)), max(1, round(H / SS))), Image.LANCZOS)
    a = np.asarray(m).astype(np.float32) / 255
    out = icona.astype(np.float32).copy()
    X = (s - a.shape[1]) // 2
    Y = y0 + 2 + cap - base / SS          # la linea di base resta dove stava quella del testo inglese
    Y = int(round(Y))
    h, w = a.shape
    ys0, xs0 = max(Y, 0), max(X, 0)
    a = a[ys0 - Y:, xs0 - X:]
    h, w = a.shape
    ombra = np.zeros(out.shape[:2], np.float32)
    ombra[ys0 + 1:ys0 + 1 + h, xs0:xs0 + w] = a[:max(0, out.shape[0] - ys0 - 1), :][:h]
    ombra = cv2.GaussianBlur(ombra, (0, 0), 0.6) * 0.5
    out[..., :3] *= (1 - ombra)[..., None]
    reg = out[ys0:ys0 + h, xs0:xs0 + w, :3]
    out[ys0:ys0 + h, xs0:xs0 + w, :3] = reg * (1 - a[..., None]) + 255 * a[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


def icona_localizzata(sheet, nome, grande, testo):
    x, y = (GRANDI if grande else PICCOLE)[nome]
    s = 62 if grande else 45
    ic = np.asarray(sheet.crop((x, y, x + s, y + s)))
    ic = pulisci(ic, BANDA[s])
    return disegna(ic, testo, BANDA[s])


def tabella(lingua, pack, out, cardinfo):
    sheet = Image.open(os.path.join(pack, 'cards/frame/icons_attribute_race.png')).convert('RGBA')
    nomi = parole(cardinfo)
    res = sheet.copy()
    for nome in ORDINE:
        for grande in (True, False):
            x, y = (GRANDI if grande else PICCOLE)[nome]
            ic = Image.fromarray(icona_localizzata(sheet, nome, grande, nomi[nome]), 'RGBA')
            res.paste(ic, (x, y))
    res.save(out)
    print('scritto', out)


ATTR_NOME = {1: 'LIGHT', 2: 'DARK', 3: 'WATER', 4: 'FIRE', 5: 'EARTH', 6: 'WIND'}   # valori del campo 'attr' di cardprops.load
SPELL, TRAP = 13, 14
CARTA = (213, 12, 26, 16)   # x, y, larghezza, altezza dell'icona sulle carte piccole 256x256 (schiacciate: l'icona e' un'ellisse), misurato con l'inglese


def carte(sheet_png, dir_carte, cardinfo):
    """sostituisce l'icona dell'attributo sulle carte piccole (id.png, ida.png...) di dir_carte, sul posto."""
    import re
    import cardprops
    cards = cardprops.load(cardinfo, corretto=False)
    sheet = Image.open(sheet_png).convert('RGBA')
    x0, y0, wi, hi = CARTA
    icone = {n: sheet.crop((GRANDI[n][0], GRANDI[n][1], GRANDI[n][0] + 62, GRANDI[n][1] + 62)).resize((wi, hi), Image.LANCZOS) for n in ORDINE}
    fatte = 0
    for f in sorted(os.listdir(dir_carte)):
        m = re.match(r'(\d+)', f)
        if not f.endswith('.png') or not m or int(m.group(1)) not in cards:
            continue
        c = cards[int(m.group(1))]
        nome = 'SPELL' if c['kind'] == SPELL else 'TRAP' if c['kind'] == TRAP else ATTR_NOME.get(c['attr'])
        if not nome:
            continue
        p = os.path.join(dir_carte, f)
        im = Image.open(p).convert('RGBA')
        im.alpha_composite(icone[nome], (x0, y0))
        im.save(p)
        fatte += 1
    print('icone sostituite su', fatte, 'carte in', dir_carte)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'tabella':
        lingua, pack, out = sys.argv[2:5]
        ehp = sys.argv[5] if len(sys.argv) > 5 else lingue.ehp_corrente()
        tabella(lingua, pack, out, ehp)
    elif cmd == 'carte':
        carte(sys.argv[2], sys.argv[3], sys.argv[4])   # SHEET_PNG DIR_CARTE CARDINFO.ehp
