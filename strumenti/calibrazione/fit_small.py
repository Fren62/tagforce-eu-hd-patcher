"""Fit the text style of small_it.py on the ENGLISH text of the HD pack's small cards.
For each element the English string is rendered with small_it's engine and compared with the
English HD card (ink = difference from the clean frame); a staged grid search maximises the
mean correlation over sample cards.
usage: fit_small.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG ELEMENT FONT_FILE FONT_INDEX"""
import itertools, os, re, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import Image
import small_it as S
from cardprops import load
from smallbg import frame_of

cdir, clean_dir, ehp, element = sys.argv[2:6]
FONT = (sys.argv[6], int(sys.argv[7]))
cards = load(ehp)
CLEAN = {g: np.asarray(Image.open(os.path.join(clean_dir, f'clean_{g}.png')).convert('RGB')).astype(np.float32)
         for g in ('normal', 'effect', 'fusion', 'ritual', 'spell', 'trap', 'token')}
TIPO_EN = {1: 'Dragon', 2: 'Zombie', 3: 'Fiend', 4: 'Pyro', 5: 'Sea Serpent', 6: 'Rock', 7: 'Machine', 8: 'Fish',
           9: 'Dinosaur', 10: 'Insect', 11: 'Beast', 12: 'Beast-Warrior', 13: 'Plant', 14: 'Aqua', 15: 'Warrior',
           16: 'Winged Beast', 17: 'Fairy', 18: 'Spellcaster', 19: 'Thunder', 20: 'Reptile', 21: 'Divine-Beast'}
KIND_EN = {0: '', 1: '/Effect', 2: '/Fusion', 3: '/Fusion/Effect', 4: '/Ritual', 5: '/Ritual/Effect',
           6: '/Toon/Effect', 7: '/Spirit/Effect', 8: '/Union/Effect', 9: '/Token'}


def ink(cid):
    img = np.asarray(Image.open(os.path.join(cdir, 'small', f'{cid}.png')).convert('RGB')).astype(np.float32)
    return np.abs(img - CLEAN[frame_of(cards[cid])]).sum(-1)


def render(text, p, x, base, align):
    """alpha (0..1) of the text on a 256x256 canvas."""
    m, asc = S.smallcaps(text, FONT, p['cap'], p['cap'] * p['sc'], p['track'])
    cv = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    S.place(cv, m, asc, x, base, (255, 255, 255), align=align, vsquash=False, embolden=p['emb'], hs=p['hs'])
    return np.asarray(cv)[..., 3].astype(np.float32) / 255


def corr(a, b):
    import cv2
    a = cv2.GaussianBlur(a.astype(np.float32), (0, 0), 0.7); b = cv2.GaussianBlur(b.astype(np.float32), (0, 0), 0.7)
    a = a - a.mean(); b = b - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))


def samples():
    out = []
    for cid, c in sorted(cards.items()):
        if not os.path.exists(os.path.join(cdir, 'small', f'{cid}.png')):
            continue
        if element == 'label' and c['kind'] in (13, 14):
            word = '[Spell Card' if c['kind'] == 13 else '[Trap Card'
            out.append((cid, word if c['icon'] else word + ']', bool(c['icon'])))
        elif element == 'type' and c['kind'] < 13:
            out.append((cid, '[' + TIPO_EN.get(c['type'], '?') + KIND_EN.get(c['kind'], '') + ']', False))
        elif element == 'name' and 6 <= len(c['name']) <= 16:
            out.append((cid, c['name'], False))
    step = max(1, len(out) // 12)
    return out[::step][:12]


SAMPLES = samples()
INK = {cid: ink(cid) for cid, _, _ in SAMPLES}
if element == 'label':
    REGION = (116, 30, 233, 45)
elif element == 'type':
    REGION = (19, 190, 160, 200)  # stop above the first description line
else:
    REGION = (17, 9, 211, 31)


def score(p):
    tot = 0.0
    x0, y0, x1, y1 = REGION
    for cid, text, icon in SAMPLES:
        e = INK[cid][y0:y1, x0:x1]
        if element == 'label':
            right = p['right_icon'] if icon else p['right']
            r = render(text, p, right, p['base'], 'right')[y0:y1, x0:x1]
            if icon:  # compare only left of the icon
                cut = int(round(p['right_icon'])) - x0 + 2
                e = e[:, :cut]; r = r[:, :cut]
        else:
            r = render(text, p, p['x'], p['base'], 'left')[y0:y1, x0:x1]
        tot += corr(e, r)
    return tot / len(SAMPLES)


if element == 'label':
    p = dict(cap=6.8, sc=0.8, track=0.2, emb=5, hs=1.0, base=40.0, right=229.0, right_icon=210.0)  # start near the type-line style
    grid = [('base', np.arange(38.5, 42.6, 0.25)), ('cap', np.arange(5.0, 8.01, 0.2)), ('right', np.arange(227, 233.1, 0.5)),
            ('right_icon', np.arange(207, 214.1, 0.5)), ('sc', np.arange(0.66, 0.95, 0.02)), ('track', np.arange(0, 0.31, 0.02)),
            ('hs', np.arange(0.84, 1.17, 0.02)), ('emb', [0, 3, 5])]
elif element == 'type':
    p = dict(cap=6.2, sc=0.8, track=0.18, emb=3, hs=1.0, base=199.0, x=20.5)  # start near the label style
    grid = [('base', np.arange(198.0, 199.76, 0.25)), ('x', np.arange(18, 23.1, 0.25)), ('cap', np.arange(4.6, 7.41, 0.2)),  # baseline ~199 (row profile)
            ('sc', np.arange(0.66, 0.95, 0.02)), ('track', np.arange(0, 0.41, 0.02)), ('hs', np.arange(0.84, 1.25, 0.02)),
            ('emb', [0, 3, 5])]
else:
    p = dict(cap=11.6, sc=0.77, track=0.0, emb=5, hs=1.0, base=25.6, x=19.5)
    grid = [('base', np.arange(24.0, 27.6, 0.25)), ('x', np.arange(17.5, 22.1, 0.25)), ('cap', np.arange(10.0, 13.41, 0.2)),
            ('sc', np.arange(0.66, 0.95, 0.02)), ('track', np.arange(0, 0.31, 0.02)), ('hs', np.arange(0.84, 1.17, 0.02)),
            ('emb', [0, 3, 5, 7, 9])]

best = score(p)
print(os.path.basename(FONT[0]), FONT[1], 'campioni', len(SAMPLES), 'iniziale %.4f' % best)
for rnd in range(3):  # coordinate descent, 3 passes
    for key, vals in grid:
        for v in vals:
            q = dict(p); q[key] = float(v) if key != 'emb' else int(v)
            sc = score(q)
            if sc > best + 1e-5:
                best, p = sc, q
    print(f'giro {rnd + 1}: correlazione media {best:.4f}', {k: round(v, 3) for k, v in p.items()}, flush=True)
