"""Fit the edge model (softness + halo) and stroke weight of the NAMES on the English HD cards:
the English name is re-rendered with small_it's engine on the erased card and both images are
compared on directional edge profiles (d=1..3 px, 4 directions) and on stroke density.
usage: fit_edge.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG"""
import os, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import Image
import small_it as S
from cardprops import load
from smallbg import frame_of

cdir, clean_dir, ehp = sys.argv[2:5]
cards = load(ehp)
CLEAN = {}
BOX = (11, 31, 18, 205)   # y0, y1, x0, x1
LUMA = np.array([0.3, 0.59, 0.11], np.float32)
DIRS = (('destra', 1, 0), ('sinistra', -1, 0), ('sotto', 0, 1), ('sopra', 0, -1))


def clean_of(c):
    g = frame_of(c)
    if g not in CLEAN:
        CLEAN[g] = np.asarray(Image.open(os.path.join(clean_dir, f'clean_{g}.png')).convert('RGB')).astype(np.int32)
    return CLEAN[g]


def profiles(img, clean):
    y0, y1, x0, x1 = BOX
    d = img[y0:y1, x0:x1].astype(np.float32) @ LUMA - clean[y0:y1, x0:x1].astype(np.float32) @ LUMA
    light = (d > 60).sum() > (d < -60).sum()
    core = (d > 0.55 * d.max()) if light else (d < 0.55 * d.min())
    if core.sum() < 30:
        return None
    contrast = float(np.median(np.abs(d[core])))
    opp = (-d if light else d) / contrast * 100
    H, W = d.shape
    out = {}
    for name, dx, dy in DIRS:
        ys, xs = np.where(core)
        vals = []
        for y, x in zip(ys, xs):
            ny, nx = y + dy, x + dx
            if not (0 <= ny < H and 0 <= nx < W) or core[ny, nx]:
                continue
            prof = []
            for r in (1, 2, 3):
                yy, xx = y + dy * r, x + dx * r
                if not (0 <= yy < H and 0 <= xx < W) or core[yy, xx]:
                    break
                prof.append(opp[yy, xx])
            if len(prof) == 3:
                vals.append(prof)
        out[name] = np.median(np.array(vals), 0) if vals else np.zeros(3)
    # stroke density (solid ink inside the text box)
    cov = np.clip((-opp) / 100, 0, 1)
    solid = cov > 0.5
    rows = np.where(solid.sum(1) >= 2)[0]; cols = np.where(solid.any(0))[0]
    dens = cov[rows.min():rows.max() + 1, cols.min():cols.max() + 1].sum() / ((rows.max() - rows.min() + 1) * (cols.max() - cols.min() + 1))
    return out, dens, light


samples = []
for cid, c in sorted(cards.items()):
    p = os.path.join(cdir, 'small', f'{cid}.png')
    if not os.path.exists(p) or not (6 <= len(c['name']) <= 15):
        continue
    img = np.asarray(Image.open(p).convert('RGB'))
    r = profiles(img, clean_of(c))
    if r:
        samples.append((cid, img, r))
light = [s for s in samples if s[2][2]][::12][:10]
dark = [s for s in samples if not s[2][2]][::12][:10]
SAMPLES = light + dark
print('campioni', len(light), 'chiari +', len(dark), 'scuri', flush=True)


def render_en(cid, img, sty):
    c = cards[cid]
    clean = clean_of(c)
    arr = img.copy()
    col = S.ink_color(arr, clean, S.NAME_R, (0, 0, 0))
    S.erase(arr, clean, S.NAME_R)
    cv = Image.fromarray(arr).convert('RGBA')
    m, asc = S.smallcaps(c['name'].replace("'", '’'), sty['font'], sty['cap'], sty['cap'] * sty['sc'], sty['track'])
    S.place(cv, m, asc, sty['x'], sty['base'], col, maxw=sty['maxw'], vsquash=True, embolden=sty['emb'], hs=sty['hs'],
            edge=sty.get('edge'))
    return np.asarray(cv.convert('RGB'))


def evaluate(sty):
    perr, derr = [], []
    for cid, img, (pe, de, li) in SAMPLES:
        mine = profiles(render_en(cid, img, sty), clean_of(cards[cid]))
        if mine is None:
            return 1e9, None
        pm, dm, _ = mine
        perr.append(np.mean([((pm[k] - pe[k]) ** 2).mean() for k in pe]))
        derr.append(dm / de - 1)
    prof_rmse = float(np.sqrt(np.median(perr)))
    dens = float(np.median(derr))
    return prof_rmse / 3.0 + abs(dens) / 0.05, dict(prof_rmse=round(prof_rmse, 2), dens=round(dens, 3))


sty = dict(S.NAME)
edge = dict(g=1.0, sx=0.4, sy=0.2, kx=0.8, hx=1.4, ky=0.3, hy=1.0)
sty['edge'] = edge
best = (*evaluate(sty), dict(edge), sty['emb'])
print('iniziale', best[0], best[1], flush=True)
grid = [('g', np.arange(0.5, 1.81, 0.1)), ('sx', np.arange(0.0, 1.21, 0.1)), ('sy', np.arange(0.0, 1.01, 0.1)), ('kx', np.arange(0.0, 2.01, 0.1)),
        ('hx', np.arange(0.6, 3.01, 0.2)), ('ky', np.arange(0.0, 2.01, 0.1)), ('hy', np.arange(0.3, 2.51, 0.2)), ('emb', [-7, -5, -3, 0, 3, 5])]
for rnd in range(4):
    for key, vals in grid:
        for v in vals:
            e = dict(best[2]); emb = best[3]
            if key == 'emb':
                emb = int(v)
            else:
                e[key] = float(v)
            t = dict(sty, edge=e, emb=emb)
            l, info = evaluate(t)
            if l < best[0] - 1e-6:
                best = (l, info, e, emb)
    print(f'giro {rnd + 1}: perdita {best[0]:.3f}', best[1], {k: round(v, 2) for k, v in best[2].items()}, 'emb', best[3], flush=True)
# final per-direction report
t = dict(sty, edge=best[2], emb=best[3])
for name, _, _ in DIRS:
    en = np.median([s[2][0][name] for s in SAMPLES], 0)
    me = np.median([profiles(render_en(cid, img, t), clean_of(cards[cid]))[0][name] for cid, img, _ in SAMPLES], 0)
    print(f'   {name:9s} originale {np.round(en, 1)}  mio {np.round(me, 1)}')
