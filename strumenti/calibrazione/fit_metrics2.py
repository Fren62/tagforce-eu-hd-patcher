"""Joint physical calibration (names / type line) on the English HD cards.
Grid over cap, small-cap ratio and weight; the horizontal scale is solved from the measured
ink width; then cap/sc/density errors and shape correlation decide.
usage: fit_metrics2.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG ELEMENT FONT IDX"""
import os, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
import fit_metrics as FM   # samples, metrics, render, REF (same argv layout)

E = FM.element


def run(p):
    out = []
    for cid, text, cov, m in FM.samples:
        mine = FM.render(text, p)
        mm = FM.metrics(mine)
        if mm is None:
            return None
        out.append((cov, m, mine, mm))
    return out


def score(res):
    import cv2
    cap = np.median([mm['cap'] - m['cap'] for cov, m, mine, mm in res])
    sc = np.median([mm['sc'] - m['sc'] for cov, m, mine, mm in res])
    wid = np.median([mm['width'] / m['width'] - 1 for cov, m, mine, mm in res])
    dens = np.median([mm['dens'] / m['dens'] - 1 for cov, m, mine, mm in res])
    cs = []
    for cov, m, mine, mm in res:
        a = cv2.GaussianBlur(cov, (0, 0), 0.5); b = cv2.GaussianBlur(mine, (0, 0), 0.5)
        a = a - a.mean(); b = b - b.mean()
        cs.append(float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9)))
    corr = float(np.median(cs))
    loss = abs(cap) / 0.5 + abs(sc) / 0.5 + abs(wid) / 0.02 + abs(dens) / 0.04 + (1 - corr) / 0.05
    return loss, dict(cap=float(cap), sc=float(sc), width=float(wid), dens=float(dens), corr=corr)


if E.startswith('name'):
    base, x = 25.6, 18.75
    caps, scs = np.arange(9.0, 12.61, 0.3), np.arange(0.72, 0.93, 0.03)
else:
    base, x = 199.0, 20.75
    caps, scs = np.arange(4.4, 7.01, 0.2), np.arange(0.72, 0.95, 0.03)
best = None
for emb in (-5, -3, 0, 3, 5):
    for cap in caps:
        for sc in scs:
            for track in ((0.0,) if E.startswith('name') else (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)):
                p = dict(cap=float(cap), sc=float(sc), track=track, emb=emb, hs=1.0, base=base, x=x)
                res = run(p)
                if res is None:
                    continue
                p['hs'] = float(np.median([m['width'] / mm['width'] for cov, m, mine, mm in res]))  # solve width
                res = run(p)
                if res is None:
                    continue
                l, e = score(res)
                if best is None or l < best[0]:
                    best = (l, p, e)
# refine baseline / x
l, p, e = best
for key, vals in (('base', np.arange(base - 1.0, base + 1.01, 0.25)), ('x', np.arange(x - 1.25, x + 1.26, 0.25))):
    for v in vals:
        q = dict(p); q[key] = float(v)
        res = run(q)
        if res is None:
            continue
        lq, eq = score(res)
        if lq < l:
            l, p, e = lq, q, eq
print(f'MIGLIORE {os.path.basename(FM.FONT[0])} {FM.FONT[1]} {E}: perdita {l:.2f}', {k: round(v, 3) for k, v in p.items()}, {k: round(v, 3) for k, v in e.items()}, 'rif', {k: round(v, 3) for k, v in FM.REF.items()}, flush=True)
