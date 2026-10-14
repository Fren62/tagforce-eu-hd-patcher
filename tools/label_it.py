"""HD Italian label atlas in the HD MOD's style ([SPELL CARD] -> [CARTA MAGIA], small caps).
The words' style (font, cap, small caps, tracking, weight) is fitted on the English strips of the
mod's atlas; the Italian words end where the English ones do; brackets and icons are the mod's own.
usage: label_it.py TOOLS HD_EN EU_DUMP OUT [fit]   (fit: re-calibrate the style on the English strips)"""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)))); import alt_font  # noqa: nessun font Apple
import sys
sys.path.insert(0, sys.argv[1])
import cv2
import numpy as np
from PIL import Image
import small_it as S

hd_en, eu, out = sys.argv[2:5]
FIT = len(sys.argv) > 5
FONTS = '/System/Library/Fonts/Supplemental/'
B = Image.open(hd_en).convert('RGBA')
BA = np.asarray(B)[..., 3].astype(np.float32) / 255
EN_TEXT = ['[Trap Card', '[Trap Card', '[Spell Card', '[Spell Card']
IT_TEXT = ['[' + S.WORDS[1]] * 2 + ['[' + S.WORDS[0]] * 2   # current language (TF1_LANG / TF1_EHP, see languages.py)
X_MIN = 100          # icons live left of this


def runs(mask):
    cols = np.where(mask.any(0))[0]
    out = []; s = p = None
    for x in cols:
        if s is None: s = x
        elif x != p + 1: out.append((s, p)); s = x
        p = x
    out.append((s, p))
    return out


# geometry of the English strips
GEO = []
for k in range(4):
    a = BA[32 * k:32 * k + 32, X_MIN:]
    r = runs(a > 0.5)
    rb = r[-1]                    # "]"
    words_end = r[-2][1] + X_MIN  # last letter of the words
    lb = r[0]                     # "["
    GEO.append(dict(words_end=words_end + 1, rb=(rb[0] + X_MIN, rb[1] + X_MIN), lb=(lb[0] + X_MIN, lb[1] + X_MIN), first=r[1][0] + X_MIN))


def render(k, text, p, words_end=None):
    """alpha strip 32x512: '[Words' in style p right-aligned at the English words' end; the brackets are the
    mod's own (copied), "[" keeping the English gap before the first letter."""
    g = GEO[k]
    cv = Image.new('RGBA', (512, 32), (0, 0, 0, 0))
    font = (FONTS + p['font'][0], p['font'][1])
    sty = dict(font=font, cap=p['cap'], sc=p['sc'], track=p['track'], emb=p['emb'], hs=p['hs'], base=p['base'])
    words = text.lstrip('[')
    we = g['words_end'] if words_end is None else words_end
    S.put_text(cv, words, sty, we, (0, 0, 0), align='right')
    a = np.asarray(cv)[..., 3].astype(np.float32) / 255
    first = np.where((a > 0.5).any(0))[0].min()
    en = BA[32 * k:32 * k + 32]
    lb0, lb1 = g['lb'][0] - 1, g['lb'][1] + 2          # "[" incl. its antialiased edges
    dx = first - g['first']
    a[:, lb0 + dx:lb1 + dx] = np.maximum(a[:, lb0 + dx:lb1 + dx], en[:, lb0:lb1])
    a[:, g['rb'][0] - 1:g['rb'][1] + 2] = en[:, g['rb'][0] - 1:g['rb'][1] + 2]
    return a


def with_hs(p):
    """horizontal scale so that the words are exactly as wide as the English ones (strip 0)."""
    font = (FONTS + p['font'][0], p['font'][1])
    sty = dict(font=font, cap=p['cap'], sc=p['sc'], track=p['track'], emb=p['emb'], hs=1.0)
    return dict(p, hs=(GEO[0]['words_end'] - GEO[0]['first']) / S.text_width('Trap Card', sty))


def score(p):
    p = with_hs(p)
    cs = []
    ink = []
    for k in range(4):
        en = BA[32 * k:32 * k + 32, X_MIN:]
        me = render(k, EN_TEXT[k], p)[:, X_MIN:]
        a = cv2.GaussianBlur(en, (0, 0), 0.6); b = cv2.GaussianBlur(me, (0, 0), 0.6)
        a = a - a.mean(); b = b - b.mean()
        cs.append(float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9)))
        ink.append(me.sum() / en.sum())
    return float(np.mean(cs)) - 0.5 * abs(float(np.mean(ink)) - 1)


# fitted on the English strips (fit mode): Charter Black 0.897, Iowan Black 0.901 but with condensed letters
P = dict(font=('Charter.ttc', 5), cap=17.0, sc=0.78, track=0.05, emb=5, hs=1.0, base=29.0)
if FIT:
    best = None
    for font in (('Iowan Old Style.ttc', 4), ('Charter.ttc', 5), ('Charter.ttc', 3), ('Palatino.ttc', 2), ('Copperplate.ttc', 2), ('Baskerville.ttc', 1)):
        p = dict(P, font=font)
        sc = score(p)
        grid = [('cap', np.arange(13.0, 21.1, 0.5)), ('sc', np.arange(0.66, 0.91, 0.02)), ('track', np.arange(0.0, 0.61, 0.05)),
('base', np.arange(26.0, 31.1, 0.5)), ('emb', [-3, 0, 3, 5, 7])
]
        for rnd in range(2):
            for key, vals in grid:
                for v in vals:
                    q = dict(p); q[key] = int(v) if key in ('emb', 'bemb') else float(v)
                    s2 = score(q)
                    if s2 > sc + 1e-5:
                        sc, p = s2, q
        p = with_hs(p)
        print(f'{font}: somiglianza {sc:.3f}', {k: (round(float(v), 3) if not isinstance(v, (int, tuple)) else v) for k, v in p.items() if k != 'font'}, flush=True)
        if best is None or sc > best[0]:
            best = (sc, p)
    print('MIGLIORE', best, flush=True)
    sys.exit(0)

# Italian strips: the mod's icons (x < 100) + "[Carta ..." in the fitted style, words ending where the English
# words end; if the longer Italian words would start left of the game's own Italian text, they are condensed.
A = np.asarray(Image.open(eu).convert('RGBA'))[..., 3]
P = with_hs(P)
res = np.asarray(B).copy()
res[:, X_MIN:] = 0
res = Image.fromarray(res)
for k, t in enumerate(IT_TEXT):
    cols = np.where((A[8 * k:8 * k + 8, 40:] > 60).any(0))[0]
    eu_left = (cols.min() + 40) * 4.0
    p = dict(P)
    for _ in range(20):
        a = render(k, t, p)
        left = np.where((a[:, X_MIN:] > 0.5).any(0))[0].min() + X_MIN
        if left >= eu_left - 2:
            break
        p['hs'] *= 0.98
    res.alpha_composite(Image.fromarray(np.dstack([np.zeros((32, 512, 3), np.uint8), (a * 255).round().astype(np.uint8)]), 'RGBA'), (0, 32 * k))
    print(k, t, 'inizio', left, '(gioco', eu_left, ') hs', round(p['hs'], 3))
res.save(out)
