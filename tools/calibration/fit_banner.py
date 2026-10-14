"""Fit the LARGE-card name banner style on the English HD banners (alpha only, exact coverage).
usage: fit_banner.py TOOLS PACK_CARDS CARDINFO_ENG FONT IDX"""
import os, sys, re
sys.path.insert(0, sys.argv[1])
import cv2
import numpy as np
from PIL import Image, ImageFilter
import banner as B
import small_it as S
from cardprops import load
from subpix import subpix

cdir, ehp, ff, fi = sys.argv[2:6]
FONT = (ff, int(fi))
cards = load(ehp)


def render(text, p):
    """banner alpha (48x320, 0..1) with style p."""
    ss = 8
    cap_ss = p['cap'] * ss
    m, asc = S.smallcaps(text.replace("'", '’'), FONT, p['cap'] * ss / ss, p['cap'] * p['sc'], p.get('track', 0.0))
    # S.smallcaps works in final px * SS internally (SS=8): cap given in final px
    if p['emb'] > 0:
        m = m.filter(ImageFilter.MaxFilter(p['emb']))
    elif p['emb'] < 0:
        m = m.filter(ImageFilter.MinFilter(-p['emb']))
    a = np.asarray(m)
    cols = np.where(a.max(0) > 0)[0]
    m = Image.fromarray(a[:, cols.min():cols.max() + 1])
    nat = m.width / S.SS * p['hs']
    r = min(1.0, B.MAXW / nat)
    v = max(0.62, min(1.0, r / 0.78))
    W, H = max(1, round(nat * r)), max(1, round(m.height / S.SS * v))
    m = m.resize((W, H), Image.LANCZOS)
    al = np.zeros((48, 320), np.float32)
    top = p['base'] - asc / S.SS * v
    ty, tx = int(np.floor(top)), int(round(B.X0))
    fy = top - ty
    sub = np.asarray(m, np.float32) / 255
    sub = cv2.warpAffine(np.pad(sub, ((1, 1), (0, 0))), np.float32([[1, 0, 0], [0, 1, fy]]), (sub.shape[1], sub.shape[0] + 2), flags=cv2.INTER_LINEAR)
    y0 = ty - 1
    ya, yb = max(0, y0), min(48, y0 + sub.shape[0]); xb = min(320, tx + sub.shape[1])
    al[ya:yb, tx:xb] = np.maximum(al[ya:yb, tx:xb], sub[ya - y0:yb - y0, :xb - tx])
    if p.get('g', 1.0) != 1.0:
        al = np.power(np.clip(al, 0, 1), p['g'])
    if p.get('k', 1.0) != 1.0:   # edge contrast: fewer half-covered pixels, same weight
        al = np.clip((al - 0.5) * p['k'] + 0.5, 0, 1) * (al > 0)
    return al


def strokes(cov):
    """median horizontal run length of solid ink (vertical stem width) and edge softness
    (pixels in the 0.15..0.85 band per solid pixel)."""
    solid = cov > 0.5
    runs = []
    for row in solid:
        x = 0
        n = len(row)
        while x < n:
            if row[x]:
                s0 = x
                while x < n and row[x]:
                    x += 1
                runs.append(x - s0)
            x += 1
    stem = float(np.median(runs)) if runs else 0.0
    soft = float(((cov > 0.15) & (cov < 0.85)).sum() / max(1, solid.sum()))
    return stem, soft


def dens(cov):
    solid = cov > 0.5
    rows = np.where(solid.sum(1) >= 2)[0]; cols = np.where(solid.any(0))[0]
    c = np.where(cov > 0.15, cov, 0)
    return c[rows.min():rows.max() + 1, cols.min():cols.max() + 1].sum() / ((rows.max() - rows.min() + 1) * (cols.max() - cols.min() + 1))


samples = []
for cid, c in sorted(cards.items())[::11]:
    p = f'{cdir}/large/{cid}.png'
    if not os.path.exists(p) or not (6 <= len(c['name']) <= 16):
        continue
    al = np.asarray(B.extract(Image.open(p).convert('RGBA')))[..., 3].astype(np.float32) / 255
    sp = subpix(al)
    if sp:
        cols = np.where((al > 0.5).any(0))[0]
        samples.append((c['name'], al, sp, dens(al), cols.min(), cols.max(), strokes(al)))
SAMPLES = samples[:24]
T = np.median([s[2] for s in SAMPLES], 0)


def evaluate(p):
    E, D, C, W = [], [], [], []
    ST = []
    for name, al, sp, de, c0, c1, stk in SAMPLES:
        mine = render(name, p)
        s = subpix(mine)
        if s is None:
            return 1e9, None
        E.append(s); D.append(dens(mine) / de - 1)
        sm = strokes(mine); ST.append((sm[0] - stk[0], sm[1] - stk[1]))
        mc = np.where((mine > 0.5).any(0))[0]
        W.append((mc.max() - mc.min()) / max(1, c1 - c0) - 1)
        a = cv2.GaussianBlur(al, (0, 0), 0.6); b = cv2.GaussianBlur(mine, (0, 0), 0.6)
        a = a - a.mean(); b = b - b.mean()
        C.append(float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9)))
    M = np.median(E, 0)
    r = dict(sc=M[0] - T[0], cap=M[1] - T[1], base=M[2] - T[2], dens=float(np.median(D)), width=float(np.median(W)), corr=float(np.median(C)),
             stem=float(np.median([x[0] for x in ST])), soft=float(np.median([x[1] for x in ST])))
    loss = (abs(r['sc']) + abs(r['cap'])) / 0.3 + abs(r['base']) / 0.3 + abs(r['dens']) / 0.03 + abs(r['width']) / 0.015 + (1 - r['corr']) / 0.04 \
           + abs(r['stem']) / 0.5 + abs(r['soft']) / 0.1
    return loss, r


best = None
START = eval(sys.argv[6]) if len(sys.argv) > 6 else None   # refine from a known style (skips the coarse grid)
if START:
    l, r = evaluate(START)
    best = (l, r, START)
for cap in ([] if START else np.arange(20.0, 27.1, 1.0)):
    for sc in np.arange(0.68, 0.83, 0.03):
        for emb in (-5, -3, 0, 3, 5):
            p = dict(cap=float(cap), sc=float(sc), emb=emb, hs=0.9, base=float(B.BASE + 0.5), g=1.0, k=1.4)
            l, r = evaluate(p)
            if r is None:
                continue
            p['hs'] = p['hs'] / (1 + r['width'])
            l, r = evaluate(p)
            if best is None or l < best[0]:
                best = (l, r, p)
grid = [('cap', np.arange(best[2]['cap'] - 1.0, best[2]['cap'] + 1.01, 0.2)), ('sc', np.arange(0.66, 0.86, 0.01)),
        ('base', np.arange(32.0, 37.01, 0.25)), ('g', np.arange(0.6, 2.61, 0.2)), ('k', np.arange(1.0, 2.21, 0.1)), ('emb', [-5, -3, 0, 3, 5]),
        ('track', np.arange(0.0, 0.241, 0.02))]
for rnd in range(3 if START else 2):
    for key, vals in grid:
        for v in vals:
            q = dict(best[2]); q[key] = int(v) if key == 'emb' else float(v)
            l, r = evaluate(q)
            if r is None:
                continue
            q['hs'] = q['hs'] / (1 + r['width'])
            l, r = evaluate(q)
            if l < best[0] - 1e-6:
                best = (l, r, q)
l, r, p = best
print(f'MIGLIORE {os.path.basename(ff)} {fi}: perdita {l:.2f}', {k: round(v, 3) for k, v in r.items()}, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in p.items()}, 'rif', np.round(T, 2), flush=True)
