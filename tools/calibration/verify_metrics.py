"""Compare IT vs EN small cards on physical text metrics (solid-ink cap height, small-cap height, stroke density)."""
import os, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import Image
from cardprops import load
from smallbg import frame_of
O = sys.argv[2]
E = load(O + '/ex/PSP_GAME/USRDIR/duelsys/cardinfo_eng.ehp')
CL = {}
REG = {'nome': (17, 9, 211, 31), 'tipo': (19, 190, 175, 200), 'etichetta': (100, 31, 210, 44)}


def cov(img, clean, box):
    x0, y0, x1, y1 = box
    a, c = img[y0:y1, x0:x1], clean[y0:y1, x0:x1]
    d = np.abs(a - c).sum(-1)
    if (d > 30).sum() < 20:
        return None
    sel = d >= np.percentile(d[d > 30], 90)
    ink = np.median(a[sel], 0)
    return np.clip(d / (np.abs(ink - c).sum(-1) + 1e-3), 0, 1)


def met(cv):
    solid = cv > 0.5
    rows = solid.sum(1)
    cols = np.where(solid.any(0))[0]
    if len(cols) < 3 or rows.max() < 3:
        return None
    r = np.where(rows >= 2)[0]
    top, base = r.min(), r.max() + 1
    sc_top = np.where(rows >= 0.35 * rows.max())[0].min()
    c = np.where(cv > 0.15, cv, 0)
    return base - top, base - sc_top, c[top:base, cols.min():cols.max() + 1].sum() / ((cols.max() - cols.min() + 1) * (base - top))


if __name__ == '__main__':
    out = {k: [] for k in REG}
    for cid, c in sorted(E.items())[::3]:
        p_en = f'{O}/mikey_x/ULUS10136/cards/small/{cid}.png'; p_it = f'{O}/stage/cards/small_it/{cid}.png'
        if not (os.path.exists(p_en) and os.path.exists(p_it)):
            continue
        g = frame_of(c)
        if g not in CL:
            CL[g] = np.asarray(Image.open(f'{O}/smallbg/clean_{g}.png').convert('RGB')).astype(float)
        en = np.asarray(Image.open(p_en).convert('RGB')).astype(float); it = np.asarray(Image.open(p_it).convert('RGB')).astype(float)
        for k, box in REG.items():
            if k == 'tipo' and c['kind'] >= 13: continue
            if k == 'etichetta' and c['kind'] < 13: continue
            a, b = cov(en, CL[g], box), cov(it, CL[g], box)
            if a is None or b is None: continue
            ma, mb = met(a), met(b)
            if ma and mb:
                out[k].append((mb[0] - ma[0], mb[1] - ma[1], mb[2] / ma[2]))
    for k, v in out.items():
        d = np.array(v)
        print(f'{k:10s} n={len(v):4d}  altezza maiuscole IT-EN mediana {np.median(d[:,0]):+.1f} px | maiuscoletto {np.median(d[:,1]):+.1f} px | spessore IT/EN {np.median(d[:,2]):.3f} (p25 {np.percentile(d[:,2],25):.3f} p75 {np.percentile(d[:,2],75):.3f})')
