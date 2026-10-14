"""Sub-pixel fit of cap height / small-cap ratio / baseline / weight for NAMES or the TYPE line,
on the English HD cards (English text re-rendered with small_it on the erased card).
usage: fit_subpix.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG name|type"""
import os, sys
sys.path.insert(0, sys.argv[1])
import cv2
import numpy as np
from PIL import Image
import small_it as S
from cardprops import load
from smallbg import frame_of
from subpix import subpix

cdir, clean_dir, ehp, element = sys.argv[2:6]
cards = load(ehp)
CLEAN = {}
TYPE_EN = {1: 'Dragon', 2: 'Zombie', 3: 'Fiend', 4: 'Pyro', 5: 'Sea Serpent', 6: 'Rock', 7: 'Machine', 8: 'Fish',
           9: 'Dinosaur', 10: 'Insect', 11: 'Beast', 12: 'Beast-Warrior', 13: 'Plant', 14: 'Aqua', 15: 'Warrior',
           16: 'Winged Beast', 17: 'Fairy', 18: 'Spellcaster', 19: 'Thunder', 20: 'Reptile', 21: 'Divine-Beast'}
KIND_EN = {0: '', 1: '/Effect', 2: '/Fusion', 3: '/Fusion/Effect', 4: '/Ritual', 5: '/Ritual/Effect',
           6: '/Toon', 7: '/Spirit', 8: '/Union', 9: '/Token'}
REG = (17, 9, 211, 31) if element == 'name' else (21, 192, 175, 200)   # x0, y0, x1, y1
BOXR = S.NAME_R if element == 'name' else (19, 189, 175, 201)


def clean_of(c):
    g = frame_of(c)
    if g not in CLEAN:
        CLEAN[g] = np.asarray(Image.open(os.path.join(clean_dir, f'clean_{g}.png')).convert('RGB')).astype(np.int32)
    return CLEAN[g]


def coverage(img, clean):
    x0, y0, x1, y1 = REG
    a = img[y0:y1, x0:x1].astype(np.float32); c = clean[y0:y1, x0:x1].astype(np.float32)
    d = np.abs(a - c).sum(-1)
    sel = d >= np.percentile(d[d > 30], 90)
    ink = np.median(a[sel], 0)
    return np.clip(d / (np.abs(ink - c).sum(-1) + 1e-3), 0, 1)


def text_of(c):
    return c['name'] if element == 'name' else TYPE_EN.get(c['type'], '?') + KIND_EN.get(c['kind'], '')


def render(cid, img, sty):
    c = cards[cid]; clean = clean_of(c)
    arr = img.copy()
    col = S.ink_color(arr, clean, BOXR, (0, 0, 0))
    S.erase(arr, clean, BOXR)
    out = Image.fromarray(arr).convert('RGBA')
    if element == 'name':
        S.put_text(out, c['name'].replace("'", '’'), sty, sty['x'], col, maxw=sty['maxw'], vsquash=True)
    else:
        S.draw_typeline(out, text_of(c), sty, col)
    return np.asarray(out.convert('RGB'))


def dens_of(cov):
    solid = cov > 0.5
    rows = np.where(solid.sum(1) >= 2)[0]; cols = np.where(solid.any(0))[0]
    c = np.where(cov > 0.15, cov, 0)
    return c[rows.min():rows.max() + 1, cols.min():cols.max() + 1].sum() / ((rows.max() - rows.min() + 1) * (cols.max() - cols.min() + 1))


samples = []
for cid, c in sorted(cards.items()):
    p = os.path.join(cdir, 'small', f'{cid}.png')
    if not os.path.exists(p):
        continue
    if element == 'name' and not (6 <= len(c['name']) <= 15):
        continue
    if element == 'type' and c['kind'] >= 13:
        continue
    img = np.asarray(Image.open(p).convert('RGB'))
    try:
        cov = coverage(img, clean_of(c))
        sp = subpix(cov, element == 'type')
    except Exception:
        continue
    if sp:
        samples.append((cid, img, cov, sp, dens_of(cov)))
SAMPLES = samples[::max(1, len(samples) // 16)][:16]
T = np.median([s[3] for s in SAMPLES], 0)
print(element, 'originale: maiuscoletto %.2f maiuscole %.2f base %.2f' % tuple(T), flush=True)


def evaluate(sty):
    M, D, C, W = [], [], [], []
    for cid, img, cov, sp, de in SAMPLES:
        mc = coverage(render(cid, img, sty), clean_of(cards[cid]))
        s = subpix(mc, element == 'type')
        if s is None:
            return 1e9, None
        M.append(s); D.append(dens_of(mc) / de - 1)
        a = cv2.GaussianBlur(cov, (0, 0), 0.5); b = cv2.GaussianBlur(mc, (0, 0), 0.5)
        a = a - a.mean(); b = b - b.mean()
        C.append(float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9)))
        ce = np.where((cov > 0.5).any(0))[0]; cm = np.where((mc > 0.5).any(0))[0]
        W.append((cm.max() - cm.min()) / max(1, ce.max() - ce.min()) - 1)
    M = np.median(M, 0)
    r = dict(sc=M[0] - T[0], cap=M[1] - T[1], base=M[2] - T[2], dens=float(np.median(D)), corr=float(np.median(C)), width=float(np.median(W)))
    loss = abs(r['sc']) / 0.15 + abs(r['cap']) / 0.15 + abs(r['base']) / 0.25 + abs(r['dens']) / 0.04 + (1 - r['corr']) / 0.05 + abs(r['width']) / 0.02
    return loss, r


sty = dict(S.NAME if element == 'name' else S.TYPELINE)
if 'edge' not in sty and element == 'name':
    sty['edge'] = dict(S.NAME['edge'])
l0, r0 = evaluate(sty)
print('attuale', round(l0, 2), {k: round(v, 3) for k, v in r0.items()}, flush=True)
if element == 'name' and len(sys.argv) > 6:
    best = None
    w0 = sty['cap'] * sty['hs']
    for cap in np.arange(10.2, 11.81, 0.2):
        for sc in np.arange(0.68, 0.81, 0.02):
            for g in (1.0, 1.15, 1.3, 1.45):
                t = dict(sty, cap=float(cap), sc=float(sc), hs=float(w0 / cap * (0.8 + 0.2 * 0.8 / sc) / (0.8 + 0.2 * 0.8 / 0.8)),
                         edge=dict(sty['edge'], g=g))
                l, r = evaluate(t)
                if best is None or l < best[0]:
                    best = (l, r, t)
    l, r, t = best
    # refine width and baseline
    for key, vals in (('hs', np.arange(t['hs'] - 0.08, t['hs'] + 0.081, 0.01)), ('base', np.arange(t['base'] - 0.75, t['base'] + 0.76, 0.25))):
        for v in vals:
            u = dict(t); u[key] = float(v)
            lu, ru = evaluate(u)
            if lu < l:
                l, r, t = lu, ru, u
    print('MIGLIORE', round(l, 2), {k: round(v, 3) for k, v in r.items()}, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in t.items() if k != 'font'}, flush=True)
