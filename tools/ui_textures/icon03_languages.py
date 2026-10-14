"""Duel numbers/LP/TEMPO sheet (card_icon03) for it, en, fr, de, es.  Recipe (user's choice, 2026-10-11):

  * rows 0-180 (small digits and signs, orange keys 1/2/3, big digits 0-9 + LP, small digits 0-9 + time word):
    from MikeyMK's **US pack** (ui/duels/numbers.png), all in crisp pixel art;
  * (warning: the cells are pasted only in their band, otherwise the European pixels spoil the top of the big digits)
  * the cells in which the European game differs from the US pack (check disc, grey ball, empty pill, time word):
    the game's original pixels enlarged 4x without smoothing (word: TEMPO / TEMPS / TIME / ZEIT / TIEMPO, from the language's texture);
  * rows 181-263 (multipliers x1...x12) and everything below (icons, cards, arrows): from the Italian sheet already in the pack
    (stable copy in tools/data/card_icon03_base_it.png), which the user likes.

For a new language: add it to LANGUAGES (archive duel/basic_b? and hash read from the texture) and rerun.
usage: python icon03_languages.py [--apply]   (without --apply it writes only the previews in OUT)"""
import io, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'tools')); sys.path.insert(0, os.path.join(B, 'tools', 'corrections'))
sys.stdout.reconfigure(encoding='utf-8')
import pycdlib, gim, apply_to_iso as ai
T = os.path.join(B, 'PSP', 'TEXTURES', 'ULES00600')
OUT = os.environ.get('TMP_ICON03', os.path.join(B, 'comparisons', 'icon03'))
S = 4
LANGUAGES = {'it': 'basic_bi.ehp', 'en': 'basic_be.ehp', 'fr': 'basic_bf.ehp', 'de': 'basic_bg.ehp', 'es': 'basic_bs.ehp'}
CELLS = [(27, 18, 45, 28), (53, 18, 83, 28)]      # check disc, grey ball + empty pill (original pixels)
WORD = (69, 37, 97, 47)                         # time word
Y_PILLS = 102                                     # end of the orange keys band (the big digits start at 104)
Y_WORD = 152                                      # start of the time word band
Y_XN = 181                                        # from here the multipliers x1...: Italian sheet

I = pycdlib.PyCdlib(); I.open(os.path.join(B, 'PSP', 'GAME', 'ULES00600_YuGiOh_GX_TagForce_EUR.iso'))


def low(arch):
    b = io.BytesIO(); I.get_file_from_iso_fp(b, iso_path='/PSP_GAME/USRDIR/duel/' + arch)
    e, f = ai.open_ehp(b.getvalue())
    g = gim.parse(bytes(f['card_icon03.gim']))
    return np.asarray(gim.to_png(g).convert('RGBA')), gim.data_hash(g)


us = np.asarray(Image.open(os.path.join(T, 'ui', 'duels', 'numbers.png')).convert('RGBA'))
it = np.asarray(Image.open(os.path.join(B, 'tools', 'data', 'card_icon03_base_it.png')).convert('RGBA'))
os.makedirs(OUT, exist_ok=True)
for lang, arch in LANGUAGES.items():
    lo, h = low(arch)
    out = it.copy()
    out[:Y_XN] = us[:Y_XN]
    for x0, y0, x1, y1 in CELLS:      # only the orange keys band: below (row 104) the big digits start, which stay the US ones
        ye = min(y1 * S, Y_PILLS)
        out[y0 * S:ye, x0 * S:x1 * S] = np.repeat(np.repeat(lo[y0:y1, x0:x1], S, 0), S, 1)[:ye - y0 * S]
    x0, y0, x1, y1 = WORD            # only the word band (rows 152-180): above are the US big digits
    ya, ye = max(y0 * S, Y_WORD), min(y1 * S, Y_XN)
    out[ya:ye, x0 * S:x1 * S] = np.repeat(np.repeat(lo[y0:y1, x0:x1], S, 0), S, 1)[ya - y0 * S:ye - y0 * S]
    im = Image.fromarray(out, 'RGBA')
    im.save(os.path.join(OUT, f'icon03_{lang}_{h}.png'))
    if '--apply' in sys.argv:
        dst = os.path.join(T, 'ui_it', 'duel_texts', 'basic_ii__card_icon03.png') if lang == 'it' else os.path.join(T, 'upscale_extra', f'{h}.png')
        im.save(dst); print('written', lang, h, dst)
    else:
        print('anteprima', lang, h)
