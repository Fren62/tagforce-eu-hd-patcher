"""Directional edge profiles of name text: for each stroke edge, how the pixels outside move
(towards the text colour = antialias, away from it = outline/shadow), per direction and distance."""
import sys, os
sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import Image
from cardprops import load
from smallbg import frame_of
O, which = sys.argv[2], sys.argv[3]   # which: small (EN) or small_it (mine)
REGION = sys.argv[4] if len(sys.argv) > 4 else 'nome'
BOX = {'nome': (11, 31, 18, 205), 'tipo': (191, 200, 22, 170), 'desc': (201, 229, 22, 233)}[REGION]
E = load(O + '/ex/PSP_GAME/USRDIR/duelsys/cardinfo_eng.ehp')
CL = {}
src = O + ('/mikey_x/ULUS10136/cards/small' if which == 'small' else '/stage/cards/small_it')
W = np.array([0.3, 0.59, 0.11], np.float32)
res = {'chiaro': {}, 'scuro': {}}
for cid, c in sorted(E.items())[::4]:
    p = f'{src}/{cid}.png'
    if not os.path.exists(p): continue
    g = frame_of(c)
    if g not in CL: CL[g] = np.asarray(Image.open(f'{O}/smallbg/clean_{g}.png').convert('RGB')).astype(np.float32)
    img = np.asarray(Image.open(p).convert('RGB')).astype(np.float32)
    if REGION != 'nome' and c['kind'] >= 13: continue
    y0, y1, x0, x1 = BOX
    d = img[y0:y1, x0:x1] @ W - CL[g][y0:y1, x0:x1] @ W
    light = (d > 60).sum() > (d < -60).sum()
    key = 'chiaro' if light else 'scuro'
    core = (d > 0.55 * d.max()) if light else (d < 0.55 * d.min())
    if core.sum() < 30: continue
    contrast = float(np.median(np.abs(d[core])))
    opp = (-d if light else d) / contrast * 100   # % of contrast, > 0: away from text colour
    H, Wd = d.shape
    for name, (dx, dy) in (('destra', (1, 0)), ('sinistra', (-1, 0)), ('sotto', (0, 1)), ('sopra', (0, -1))):
        # edge pixels: core pixel whose neighbour in direction is not core
        ys, xs = np.where(core)
        vals = []
        for y, x in zip(ys, xs):
            ny, nx = y + dy, x + dx
            if not (0 <= ny < H and 0 <= nx < Wd) or core[ny, nx]: continue
            prof = []
            for r in (1, 2, 3, 4):
                yy, xx = y + dy * r, x + dx * r
                if not (0 <= yy < H and 0 <= xx < Wd): break
                if core[yy, xx]: break       # ran into another stroke
                prof.append(opp[yy, xx])
            if len(prof) == 4: vals.append(prof)
        if vals:
            res[key].setdefault(name, []).append(np.median(np.array(vals), 0))
for key, dd in res.items():
    print(f'== {REGION} {key} ({which}) [% del contrasto]')
    for name, v in dd.items():
        print(f'   {name:9s} distanza 1..4: {np.round(np.median(np.array(v), 0), 1)}')
