"""Fit one font face for the small-card DESCRIPTION on the English HD cards (deschar.Bench):
size, width, weight, ink, first baseline, pitch and edge look (sharpness + light halo).
usage: fit_descfont.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG KIND FONT_FILE FONT_INDEX OUT_JSON [quick|full] [START_JSON]
prints one line 'RISULTATO ...' and writes the best style + metrics to OUT_JSON."""
import json, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import ImageFont
import small_it as S
from deschar import Bench

cdir, clean_dir, ehp, kind, ff, fi, out = sys.argv[2:9]
mode = sys.argv[9] if len(sys.argv) > 9 else 'quick'
FONT = (ff, int(fi))
bench = Bench(cdir, clean_dir, ehp, kind, n=10 if mode == 'quick' else 16)
R = bench.ref

if len(sys.argv) > 10:
    p = json.load(open(sys.argv[10]))['style']
    p['font'] = FONT
    p.setdefault('dk', 1.0)
else:
    # start: x-height from the font's own 'x' so that the English x-band is matched
    f = ImageFont.truetype(ff, 200, index=int(fi))
    l, t, r_, b = f.getbbox('x')
    xh_ratio = (b - t) / 200
    px = float(np.clip((R['xh'] - 0.3) / max(xh_ratio, 0.3), 4.5, 10.0))
    p = dict(font=FONT, px=round(px, 2), hs=1.0, emb=0, ink=1.0, pitch=round(R['pitch'] if kind == 'st' else S.DESC[kind]['pitch'], 2),
             base=S.DESC[kind]['base'], nmax=S.DESC[kind]['nmax'],
             dk=1.0, edge=dict(g=1.0, sx=0.4, sy=0.3, kx=1.0, hx=1.2, ky=0.3, hy=1.0))   # dk: needed by the random search (KeyError 'dk' with new fonts)


def ev(q):
    return bench.evaluate(q)


best = (*ev(p), p)


def tryset(key, vals, sub=None):
    global best
    for v in vals:
        q = json.loads(json.dumps(best[2]))
        q['font'] = FONT
        if sub:
            q[sub][key] = float(v)
        else:
            q[key] = int(v) if key == 'emb' else float(v)
        l, r = ev(q)
        if r is not None and l < best[0] - 1e-6:
            best = (l, r, q)


def solve_hs(wide=False):
    """width: hs so that the English text wraps into the same lines (line count + last line end)."""
    if wide:
        tryset('hs', np.arange(0.6, 2.01, 0.03))
    tryset('hs', np.arange(max(0.6, best[2]['hs'] - 0.1), best[2]['hs'] + 0.101, 0.01))


EMBS = [-3, 0, 3, 5, 7, 9, 11]
if len(sys.argv) <= 10:
    # joint size x weight grid on the shape metrics only (line breaks come later with hs)
    shape = None
    for emb in EMBS:
        for px in np.arange(p['px'] - 1.5, p['px'] + 1.51, 0.25):
            q = dict(p, emb=emb, px=float(px))
            l, r = ev(q)
            if r is None:
                continue
            ls = abs(r['xh']) / 0.15 + abs(r['up']) / 0.3 + abs(r['dn']) / 0.3 + abs(r['dens']) / 0.05 + abs(r['dark']) / 0.05
            if shape is None or ls < shape[0]:
                shape = (ls, q)
    best = (*ev(shape[1]), shape[1])
    solve_hs(wide=True)

rounds = 1 if mode == 'quick' else 4
for rnd in range(rounds):
    pc = best[2]['px']
    tryset('px', np.arange(pc - 1.2, pc + 1.21, 0.15 if mode == 'quick' else 0.1))
    solve_hs()
    tryset('emb', EMBS)
    tryset('base', np.arange(best[2]['base'] - 1.0, best[2]['base'] + 1.01, 0.25))
    tryset('pitch', np.arange(best[2]['pitch'] - 0.3, best[2]['pitch'] + 0.31, 0.05))
    tryset('ink', np.arange(0.7, 1.01, 0.05))
    tryset('dk', np.arange(0.5, 1.01, 0.05))
    tryset('g', np.arange(0.3, 1.61, 0.1), 'edge')
    tryset('sx', np.arange(0.05, 1.01, 0.1), 'edge')
    tryset('sy', np.arange(0.05, 1.01, 0.1), 'edge')
    tryset('kx', np.arange(0.0, 6.01, 0.5), 'edge')
    tryset('hx', np.arange(0.4, 2.01, 0.2), 'edge')
    tryset('ky', np.arange(0.0, 4.01, 0.5), 'edge')
    tryset('hy', np.arange(0.4, 2.01, 0.2), 'edge')
    solve_hs()

# joint random search: the edge look, ink and weight are coupled (a stronger halo changes darkness and density)
STEP = dict(px=0.1, hs=0.02, base=0.15, pitch=0.04, ink=0.04, dk=0.04)
ESTEP = dict(g=0.08, sx=0.08, sy=0.08, kx=0.4, hx=0.15, ky=0.3, hy=0.15)
LIM = dict(ink=(0.5, 1.0), dk=(0.4, 1.0), g=(0.3, 2.0), sx=(0.05, 1.5), sy=(0.05, 1.5), kx=(0.0, 8.0), hx=(0.3, 3.0), ky=(0.0, 6.0), hy=(0.3, 3.0))
rng = np.random.default_rng(int(fi) * 7919 + len(ff) + len(kind))
for it in range(120 if mode == 'quick' else 300):
    q = json.loads(json.dumps(best[2])); q['font'] = FONT
    for k, sd in STEP.items():
        if rng.random() < 0.4:
            q[k] = float(np.clip(q[k] + rng.normal(0, sd), *LIM.get(k, (-1e9, 1e9))))
    for k, sd in ESTEP.items():
        if rng.random() < 0.5:
            q['edge'][k] = float(np.clip(q['edge'][k] + rng.normal(0, sd), *LIM[k]))
    if rng.random() < 0.15:
        q['emb'] = int(rng.choice(EMBS))
    l, r = ev(q)
    if r is not None and l < best[0] - 1e-6:
        best = (l, r, q)

l, r, p = best
res = dict(kind=kind, font=[ff, int(fi)], name=' '.join(ImageFont.truetype(ff, 20, index=int(fi)).getname()), loss=l,
           metrics=r, style={k: v for k, v in p.items() if k != 'font'}, ref={k: np.asarray(v).tolist() for k, v in R.items()})
print('RISULTATO', kind, res['name'], 'perdita %.2f' % l, {k: round(v, 3) for k, v in r.items()}, flush=True)
json.dump(res, open(out, 'w'), indent=1)
