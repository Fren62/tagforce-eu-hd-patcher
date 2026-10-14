"""Physical calibration of small-caps text (names / type line) on the English HD cards.
For the English string of each sample card, compare my rendering with the HD card on:
  cap height, small-cap height, ink width, ink density (stroke weight), and correlation.
usage: fit_metrics.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG ELEMENT(name_dark|name_light|type) FONT IDX"""
import os, sys
sys.path.insert(0, sys.argv[1])
import cv2
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
TYPE_EN = {1: 'Dragon', 2: 'Zombie', 3: 'Fiend', 4: 'Pyro', 5: 'Sea Serpent', 6: 'Rock', 7: 'Machine', 8: 'Fish',
           9: 'Dinosaur', 10: 'Insect', 11: 'Beast', 12: 'Beast-Warrior', 13: 'Plant', 14: 'Aqua', 15: 'Warrior',
           16: 'Winged Beast', 17: 'Fairy', 18: 'Spellcaster', 19: 'Thunder', 20: 'Reptile', 21: 'Divine-Beast'}
KIND_EN = {0: '', 1: '/Effect', 2: '/Fusion', 3: '/Fusion/Effect', 4: '/Ritual', 5: '/Ritual/Effect',
           6: '/Toon', 7: '/Spirit', 8: '/Union', 9: '/Token'}
REG = (17, 9, 211, 31) if element.startswith('name') else (19, 190, 175, 200)


def coverage(cid):
    """English ink coverage (0..1) in REG, and its color."""
    img = np.asarray(Image.open(os.path.join(cdir, 'small', f'{cid}.png')).convert('RGB')).astype(np.float32)
    cl = CLEAN[frame_of(cards[cid])]
    x0, y0, x1, y1 = REG
    a, c = img[y0:y1, x0:x1], cl[y0:y1, x0:x1]
    d = np.abs(a - c).sum(-1)
    if d.max() < 60:
        return None
    sel = d >= np.percentile(d[d > 30], 90) if (d > 30).sum() > 20 else d > 30
    ink = np.median(a[sel], 0)
    contrast = np.abs(ink - c).sum(-1) + 1e-3
    cov = np.clip(d / contrast, 0, 1)
    return cov, ink


def metrics(cov):
    solid = cov > 0.5
    rows = solid.sum(1)
    cols = np.where(solid.any(0))[0]
    if len(cols) < 3 or rows.max() < 3:
        return None
    r = np.where(rows >= 2)[0]
    top, base = r.min(), r.max() + 1
    sc_top = np.where(rows >= 0.35 * rows.max())[0].min()      # small caps dominate the row counts
    width = cols.max() - cols.min() + 1
    c = np.where(cov > 0.15, cov, 0)
    dens = c[top:base, cols.min():cols.max() + 1].sum() / (width * (base - top))
    return dict(cap=base - top, sc=base - sc_top, width=width, dens=dens, x0=cols.min())


def is_dark(ink):
    return ink.mean() < 110


samples = []
for cid, c in sorted(cards.items()):
    if not os.path.exists(os.path.join(cdir, 'small', f'{cid}.png')):
        continue
    if element.startswith('name'):
        if not (6 <= len(c['name']) <= 16):
            continue
        text = c['name']
    else:
        if c['kind'] >= 13:
            continue
        text = '[' + TYPE_EN.get(c['type'], '?') + KIND_EN.get(c['kind'], '') + ']'
    r = coverage(cid)
    if r is None:
        continue
    cov, ink = r
    if element == 'name_dark' and not is_dark(ink):
        continue
    if element == 'name_light' and (is_dark(ink) or ink.mean() < 180):
        continue
    m = metrics(cov)
    if m:
        samples.append((cid, text, cov, m))
samples = samples[::max(1, len(samples) // 14)][:14]
REF = {k: float(np.median([s[3][k] for s in samples])) for k in ('cap', 'sc', 'dens')}


def render(text, p):
    m, asc = S.smallcaps(text, FONT, p['cap'], p['cap'] * p['sc'], p['track'])
    cv = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    S.place(cv, m, asc, p['x'], p['base'], (255, 255, 255), vsquash=False, embolden=p['emb'], hs=p['hs'])
    x0, y0, x1, y1 = REG
    return np.asarray(cv)[y0:y1, x0:x1, 3].astype(np.float32) / 255


def evaluate(p):
    errs = dict(cap=[], sc=[], width=[], dens=[], corr=[])
    for cid, text, cov, m in samples:
        mine = render(text, p)
        mm = metrics(mine)
        if mm is None:
            return None
        errs['cap'].append(mm['cap'] - m['cap']); errs['sc'].append(mm['sc'] - m['sc'])
        errs['width'].append(mm['width'] / m['width'] - 1); errs['dens'].append(mm['dens'] / m['dens'] - 1)
        a = cv2.GaussianBlur(cov, (0, 0), 0.5); b = cv2.GaussianBlur(mine, (0, 0), 0.5)
        a = a - a.mean(); b = b - b.mean()
        errs['corr'].append(float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9)))
    return {k: float(np.median(v)) for k, v in errs.items()}


def loss(e):
    # every physical metric must match; then shapes (correlation)
    return abs(e['cap']) / 0.5 + abs(e['sc']) / 0.5 + abs(e['width']) / 0.02 + abs(e['dens']) / 0.04 + (1 - e['corr']) / 0.05


if element.startswith('name'):
    p = dict(cap=11.6, sc=0.78, track=0.0, emb=0, hs=1.0, base=25.6, x=18.75)
    grid = [('cap', np.arange(9.6, 13.01, 0.2)), ('sc', np.arange(0.70, 0.93, 0.01)), ('hs', np.arange(0.86, 1.25, 0.02)),
            ('track', np.arange(0.0, 0.21, 0.02)), ('emb', [-5, -3, 0, 3, 5]), ('base', np.arange(24.5, 26.76, 0.25)), ('x', np.arange(17.5, 20.6, 0.25))]
else:
    p = dict(cap=6.2, sc=0.8, track=0.18, emb=0, hs=1.0, base=199.0, x=20.75)
    grid = [('cap', np.arange(4.6, 7.01, 0.1)), ('sc', np.arange(0.70, 0.95, 0.01)), ('hs', np.arange(0.86, 1.25, 0.02)),
            ('track', np.arange(0.0, 0.41, 0.02)), ('emb', [-5, -3, 0, 3, 5]), ('base', np.arange(198.0, 199.76, 0.25)), ('x', np.arange(19.5, 22.1, 0.25))]

if __name__ == '__main__':
    print(os.path.basename(FONT[0]), FONT[1], element, 'campioni', len(samples), 'riferimento', {k: round(v, 3) for k, v in REF.items()}, flush=True)
    e = evaluate(p); best = (loss(e), p, e)
    for rnd in range(3):
        for key, vals in grid:
            for v in vals:
                q = dict(best[1]); q[key] = int(v) if key == 'emb' else float(v)
                e = evaluate(q)
                if e is None:
                    continue
                l = loss(e)
                if l < best[0] - 1e-6:
                    best = (l, q, e)
        print(f'giro {rnd + 1}: perdita {best[0]:.2f}', {k: round(v, 3) for k, v in best[1].items()}, {k: round(v, 3) for k, v in best[2].items()}, flush=True)
