"""Foglio numeri/LP/TEMPO del duello (card_icon03) per it, en, fr, de, es.  Ricetta (scelta dell'utente, 2026-10-11):

  * righe 0-180 (cifre e segni piccoli, tasti arancioni 1/2/3, cifre grandi 0-9 + LP, cifre piccole 0-9 + parola del tempo):
    dal **pack USA di MikeyMK** (ui/duels/numbers.png), tutto in pixel art netta;
  * (attenzione: le celle si incollano solo nella loro fascia, altrimenti i pixel europei rovinano la parte alta delle cifre grandi)
  * le celle in cui il gioco europeo differisce dal pack USA (disco con la spunta, palla grigia, pillola vuota, parola del tempo):
    i pixel originali del gioco ingranditi 4x senza sfumare (parola: TEMPO / TEMPS / TIME / ZEIT / TIEMPO, dalla texture della lingua);
  * righe 181-263 (moltiplicatori x1...x12) e tutto cio' che sta sotto (icone, carte, frecce): dal foglio italiano gia' nel pack
    (copia stabile in strumenti/dati/card_icon03_base_it.png), che all'utente piace.

Per una nuova lingua: aggiungerla in LINGUE (archivio duel/basic_b? e hash letto dalla texture) e rilanciare.
uso: python icon03_lingue.py [--applica]   (senza --applica scrive solo le anteprime in OUT)"""
import io, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'strumenti')); sys.path.insert(0, os.path.join(B, 'strumenti', 'correzioni'))
sys.stdout.reconfigure(encoding='utf-8')
import pycdlib, gim, applica_iso as ai
T = os.path.join(B, 'PSP', 'TEXTURES', 'ULES00600')
OUT = os.environ.get('TMP_ICON03', os.path.join(B, 'confronti', 'icon03'))
S = 4
LINGUE = {'it': 'basic_bi.ehp', 'en': 'basic_be.ehp', 'fr': 'basic_bf.ehp', 'de': 'basic_bg.ehp', 'es': 'basic_bs.ehp'}
CELLE = [(27, 18, 45, 28), (53, 18, 83, 28)]      # disco con spunta, palla grigia + pillola vuota (pixel originali)
PAROLA = (69, 37, 97, 47)                         # parola del tempo
Y_PILLS = 102                                     # fine della fascia dei tasti arancioni (le cifre grandi iniziano a 104)
Y_WORD = 152                                      # inizio della fascia della parola del tempo
Y_XN = 181                                        # da qui i moltiplicatori x1...: foglio italiano

I = pycdlib.PyCdlib(); I.open(os.path.join(B, 'PSP', 'GAME', 'ULES00600_YuGiOh_GX_TagForce_EUR.iso'))


def low(arch):
    b = io.BytesIO(); I.get_file_from_iso_fp(b, iso_path='/PSP_GAME/USRDIR/duel/' + arch)
    e, f = ai.apri(b.getvalue())
    g = gim.parse(bytes(f['card_icon03.gim']))
    return np.asarray(gim.to_png(g).convert('RGBA')), gim.data_hash(g)


us = np.asarray(Image.open(os.path.join(T, 'ui', 'duels', 'numbers.png')).convert('RGBA'))
it = np.asarray(Image.open(os.path.join(B, 'strumenti', 'dati', 'card_icon03_base_it.png')).convert('RGBA'))
os.makedirs(OUT, exist_ok=True)
for lang, arch in LINGUE.items():
    lo, h = low(arch)
    out = it.copy()
    out[:Y_XN] = us[:Y_XN]
    for x0, y0, x1, y1 in CELLE:      # solo la fascia dei tasti arancioni: sotto (riga 104) iniziano le cifre grandi, che restano quelle USA
        ye = min(y1 * S, Y_PILLS)
        out[y0 * S:ye, x0 * S:x1 * S] = np.repeat(np.repeat(lo[y0:y1, x0:x1], S, 0), S, 1)[:ye - y0 * S]
    x0, y0, x1, y1 = PAROLA            # solo la fascia della parola (righe 152-180): sopra ci sono le cifre grandi USA
    ya, ye = max(y0 * S, Y_WORD), min(y1 * S, Y_XN)
    out[ya:ye, x0 * S:x1 * S] = np.repeat(np.repeat(lo[y0:y1, x0:x1], S, 0), S, 1)[ya - y0 * S:ye - y0 * S]
    im = Image.fromarray(out, 'RGBA')
    im.save(os.path.join(OUT, f'icon03_{lang}_{h}.png'))
    if '--applica' in sys.argv:
        dst = os.path.join(T, 'ui_it', 'scritte_duello', 'basic_ii__card_icon03.png') if lang == 'it' else os.path.join(T, 'upscale_extra', f'{h}.png')
        im.save(dst); print('scritto', lang, h, dst)
    else:
        print('anteprima', lang, h)
