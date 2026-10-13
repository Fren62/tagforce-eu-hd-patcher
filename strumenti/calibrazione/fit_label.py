"""Physical calibration of the small-card [SPELL CARD]/[TRAP CARD] label on the English HD cards:
cap height, small caps, stroke density, start x and shape, with thin brackets like the original.
usage: fit_label.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG"""
import os, sys
sys.path.insert(0, sys.argv[1])
import cv2
import numpy as np
from PIL import Image
import small_it as S
from cardprops import load
from smallbg import frame_of

cdir, clean_dir, ehp = sys.argv[2:5]
cards = load(ehp)
CLEAN = {}
REG = (96, 30, 211, 45)      # x0, y0, x1, y1: words + left bracket (icon/right bracket excluded)


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


def metrics(cov):
    solid = cov > 0.5
    cols = np.where(solid.any(0))[0]
    # letters only: skip the left bracket (first run of columns)
    runs = []; s = p = None
    for x in cols:
        if s is None: s = x
        elif x != p + 1: runs.append((s, p)); s = x
        p = x
    runs.append((s, p))
    start = runs[0][0] + REG[0]
    lx0 = runs[1][0] if len(runs) > 1 else runs[0][0]
    let = solid[:, lx0:]
    rows = let.sum(1)
    r = np.where(rows >= 2)[0]
    top, base = r.min(), r.max() + 1
    sc_top = np.where(rows >= 0.35 * rows.max())[0].min()
    c = np.where(cov[:, lx0:] > 0.15, cov[:, lx0:], 0)
    lc = np.where(let.any(0))[0]
    dens = c[top:base, lc.min():lc.max() + 1].sum() / ((lc.max() - lc.min() + 1) * (base - top))
    return dict(cap=base - top, sc=base - sc_top, dens=dens, start=start, base=base + REG[1])


def draw_label(img, c, sty):
    clean = clean_of(c)
    arr = img.copy()
    col = S.ink_color(arr, clean, S.LABEL_R, (20, 20, 20))
    icon = None
    if c['icon']:
        x0, y0, x1, y1 = S.ICON_R
        patch = arr[y0:y1, x0:x1].copy()
        dd = np.abs(patch.astype(np.int32) - clean[y0:y1, x0:x1]).sum(-1)
        hsv = np.asarray(Image.fromarray(patch).convert('HSV'))
        m = (dd > 30) & ((hsv[..., 1] > 40) | (hsv[..., 2] > 150))
        from PIL import ImageFilter
        m = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.5))
        icon = (Image.fromarray(patch), m)
    S.erase(arr, clean, S.LABEL_R)
    out = Image.fromarray(arr).convert('RGBA')
    word = '[Spell Card' if c['kind'] == 13 else '[Trap Card'
    S.draw_label(out, word, bool(icon), sty, col, icon)
    return np.asarray(out.convert('RGB'))


samples = []
for cid, c in sorted(cards.items()):
    if c['kind'] not in (13, 14):
        continue
    p = os.path.join(cdir, 'small', f'{cid}.png')
    if not os.path.exists(p):
        continue
    img = np.asarray(Image.open(p).convert('RGB'))
    cov = coverage(img, clean_of(c))
    try:
        m = metrics(cov)
    except Exception:
        continue
    samples.append((cid, img, cov, m))
groups = {}
for s in samples:
    c = cards[s[0]]
    groups.setdefault((c['kind'], bool(c['icon'])), []).append(s)
SAMPLES = [x for g in groups.values() for x in g[::max(1, len(g) // 5)][:5]]
REF = {k: float(np.median([s[3][k] for s in SAMPLES])) for k in ('cap', 'sc', 'dens')}
print('campioni', len(SAMPLES), 'riferimento', REF, {k: np.median([s[3]['start'] for s in g]) for k, g in groups.items()}, flush=True)


def evaluate(sty):
    e = dict(cap=[], sc=[], dens=[], start=[], corr=[])
    for cid, img, cov, m in SAMPLES:
        mine = draw_label(img, cards[cid], sty)
        mc = coverage(mine, clean_of(cards[cid]))
        try:
            mm = metrics(mc)
        except Exception:
            return 1e9, None
        e['cap'].append(mm['cap'] - m['cap']); e['sc'].append(mm['sc'] - m['sc'])
        e['dens'].append(mm['dens'] / m['dens'] - 1); e['start'].append(mm['start'] - m['start'])
        a = cv2.GaussianBlur(cov, (0, 0), 0.5); b = cv2.GaussianBlur(mc, (0, 0), 0.5)
        a = a - a.mean(); b = b - b.mean()
        e['corr'].append(float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9)))
    r = {k: float(np.median(v)) for k, v in e.items()}
    loss = abs(r['cap']) / 0.5 + abs(r['sc']) / 0.5 + abs(r['dens']) / 0.04 + abs(r['start']) / 1.0 + (1 - r['corr']) / 0.05
    return loss, r


sty = dict(S.LABEL, emb=3, bracket_emb=3, sc=0.8, hs=1.16, base=40.5, right_icon=210.5, edge=dict(S.NAME['edge']))
best = (*evaluate(sty), dict(sty))
print('iniziale', round(best[0], 2), best[1], flush=True)
grid = [('cap', np.arange(5.0, 7.61, 0.2)), ('sc', np.arange(0.70, 0.93, 0.02)), ('hs', np.arange(0.9, 1.41, 0.02)),
        ('track', np.arange(0.0, 0.41, 0.04)), ('emb', [-3, 0, 3, 5]), ('base', np.arange(38.5, 41.01, 0.25)),
        ('right_icon', np.arange(207.0, 212.1, 0.5)), ('right', np.arange(227.0, 231.1, 0.5)),
        ('bracket_emb', [-3, 0, 3]), ('gap', np.arange(0.0, 2.51, 0.5)), ('g', np.arange(0.6, 1.61, 0.1))]
for rnd in range(3):
    for key, vals in grid:
        for v in vals:
            t = dict(best[2]); t['edge'] = dict(t['edge'])
            if key == 'g':
                t['edge']['g'] = float(v)
            else:
                t[key] = int(v) if key in ('emb', 'bracket_emb') else float(v)
            l, r = evaluate(t)
            if l < best[0] - 1e-6:
                best = (l, r, t)
    print(f'giro {rnd + 1}: perdita {best[0]:.2f}', {k: round(v, 3) for k, v in best[1].items()},
          {k: (round(v, 3) if isinstance(v, float) else v) for k, v in best[2].items() if k != 'font'}, flush=True)
