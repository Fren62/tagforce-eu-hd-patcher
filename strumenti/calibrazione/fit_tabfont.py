"""Rank system fonts by overlap with the mod's tab letter cores, searching one horizontal scale per font."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import font_alt  # noqa: nessun font Apple
import sys, json, os, glob
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
P, G, FACES, OUT = sys.argv[1:5]
glyphs = json.load(open(G))
TABS = {'Trunk': '00000000a33778db85d8f4f8.png', 'Fusion': '0000000065037c929f671d8d.png', 'Side': '000000006c2037fcdf435532.png', 'Deck': '00000000f1fc5e4cf83d4357.png'}
X_BOX = {'Trunk': 150, 'Fusion': 146, 'Side': 146, 'Deck': 146}
ref = []
for name, f in TABS.items():
    a = np.asarray(Image.open(P + '/ui/deckedit/' + f).convert('RGB')).astype(np.int32)
    core = (a.min(-1) > 205); core[:8] = False; core[72:] = False; core[:, X_BOX[name]:] = False; core[:, :8] = False
    for g in glyphs[name]:
        ref.append(dict(ch=g['ch'], m=core[g['y']:g['y'] + g['h'], g['x']:g['x'] + g['w']], w=g['w'], h=g['h']))
XH = float(np.median([r['h'] for r in ref if r['ch'] in 'runsoe']))


def make_font(ff, fi, wt, size):
    f = ImageFont.truetype(ff, size, index=fi)
    if wt is not None:
        ax = f.get_variation_axes(); v = [a['default'] for a in ax]
        for i, a in enumerate(ax):
            if a.get('name') in (b'Weight', 'Weight'): v[i] = wt
        f.set_variation_by_axes(v)
    return f


def glyph(f, ch):
    x0, y0, x1, y1 = f.getbbox(ch, anchor='ls')
    pad = 6
    m = Image.new('L', (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), 0)
    ImageDraw.Draw(m).text((pad - x0, pad - y0), ch, font=f, fill=255, anchor='ls')
    m = np.asarray(m) > 127
    ys, xs = np.where(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1], y1 - pad  # crop, bottom relative to baseline (+ = below)


def iou_at(gm, bottom_rel, r):
    H, W = r['h'] + 24, r['w'] + 24
    can = np.zeros((H, W), bool)
    base_y = 12 + r['h']                       # baseline of the mod glyph = its bottom
    top = base_y + bottom_rel - gm.shape[0]
    left = 12 + (r['w'] - gm.shape[1]) // 2
    ya, yb = max(0, top), min(H, top + gm.shape[0]); xa, xb = max(0, left), min(W, left + gm.shape[1])
    if yb > ya and xb > xa:
        can[ya:yb, xa:xb] = gm[ya - top:yb - top, xa - left:xb - left]
    refc = np.zeros((H, W), bool); refc[12:12 + r['h'], 12:12 + r['w']] = r['m'].astype(bool)
    return (can & refc).sum() / max(1, (can | refc).sum())


cands = []
for line in open(FACES):
    ff, fi, name = line.rstrip('\n').split('|'); cands.append((ff, int(fi), name, None))
for ff in ('/System/Library/Fonts/SFNSRounded.ttf', '/System/Library/Fonts/SFNS.ttf'):
    for w in (700, 800, 900, 1000):
        cands.append((ff, 0, os.path.basename(ff) + f' w{w}', w))
for ff in glob.glob('/Library/Fonts/*.ttf') + glob.glob('/Library/Fonts/*.otf'):
    cands.append((ff, 0, os.path.basename(ff), None))
res = []
for ff, fi, name, wt in cands:
    try:
        f0 = make_font(ff, fi, wt, 100); xb = f0.getbbox('x', anchor='ls'); xh100 = xb[3] - xb[1]
        if xh100 <= 0: continue
        f = make_font(ff, fi, wt, max(8, int(round(100 * XH / xh100))))
        gl = {ch: glyph(f, ch) for ch in set(r['ch'] for r in ref)}
        best = None
        for sx in (1.0, 0.95, 0.9, 0.85, 0.8, 0.75):
            sc = []
            for r in ref:
                gm, bot = gl[r['ch']]
                if sx != 1.0:
                    gm = cv2.resize(gm.astype(np.uint8), (max(1, int(round(gm.shape[1] * sx))), gm.shape[0]), interpolation=cv2.INTER_AREA) > 0
                sc.append(iou_at(gm, bot, r))
            m_ = float(np.mean(sc))
            if best is None or m_ > best[0]: best = (m_, sx)
        res.append((best[0], best[1], name, ff, fi, wt))
    except Exception:
        continue
res.sort(reverse=True)
json.dump([dict(score=s, sx=x, name=n, file=f, index=i, wght=w) for s, x, n, f, i, w in res[:40]], open(OUT, 'w'), indent=1)
for s, x, n, f, i, w in res[:24]:
    print('%.3f sx%.2f %-40s %s' % (s, x, n, os.path.basename(f)))
