"""Line-break fidelity: for English cards, compare line count AND last-line end x with my wrapping.
usage: fit_breaks.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG"""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import font_alt  # noqa: nessun font Apple
import os, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import Image
import small_it as S
from cardprops import load
from smallbg import frame_of
cdir, clean_dir, ehp = sys.argv[2:5]
E = load(ehp)
CLEAN = {}
X0, X1 = 22.0, 234.0


def measure(cid, st):
    c = E[cid]; g = frame_of(c)
    if g not in CLEAN:
        CLEAN[g] = np.asarray(Image.open(f'{clean_dir}/clean_{g}.png').convert('RGB')).astype(float)
    img = np.asarray(Image.open(f'{cdir}/small/{cid}.png').convert('RGB')).astype(float)
    y0, y1 = (200, 231) if not st else (192, 240)
    d = np.abs(img - CLEAN[g]).sum(-1)[y0:y1]
    sm = np.convolve(d[:, 22:234].mean(1), np.ones(3) / 3, mode='same')
    peaks = [y for y in range(1, len(sm) - 1) if sm[y] > sm[y - 1] and sm[y] >= sm[y + 1] and sm[y] > 0.35 * sm.max()]
    merged = []
    for y in peaks:
        if merged and y - merged[-1] < 3:
            if sm[y] > sm[merged[-1]]:
                merged[-1] = y
        else:
            merged.append(y)
    if not merged:
        return None
    ly = merged[-1]
    band = d[max(0, ly - 1):ly + 2, :]
    cols = np.where(band.max(0) > 60)[0]
    cols = cols[(cols >= 20) & (cols <= 234)]
    return len(merged), (cols.max() + 1 if len(cols) else None)


KIND = sys.argv[5]
samples = []
for cid, c in sorted(E.items()):
    st = c['kind'] in (13, 14)
    want = {'effect': (1,), 'st': (13, 14), 'normal': (0,)}[KIND]
    if c['kind'] in want and '\n' not in c['desc'] and 40 < len(c['desc']) < 300 and os.path.exists(f'{cdir}/small/{cid}.png'):
        m = measure(cid, st)
        if m and m[1]:
            samples.append((cid, m[0], m[1]))
print(KIND, 'campioni', len(samples), flush=True)
F = '/System/Library/Fonts/Supplemental/'
fonts = [('Charter.ttc', 3), ('Charter.ttc', 0), ('Palatino.ttc', 0), ('Georgia.ttf', 0)] if KIND != 'normal' else \
        [('Times New Roman Italic.ttf', 0), ('Georgia Italic.ttf', 0), ('Palatino.ttc', 1), ('Charter.ttc', 1), ('Iowan Old Style.ttc', 2)]
res = []
for fname, idx in fonts:
    for px in (6.6, 6.8, 7.0, 7.2, 7.4, 7.6, 7.8, 8.0, 8.2):
        f = S.font((F + fname, idx), px * S.SS)
        for hs in [x / 100 for x in range(86, 111, 1)]:
            width = (X1 - X0) * S.SS / hs
            ok = cnt = 0
            for cid, n, xe in samples:
                lines = S.wrap(E[cid]['desc'].split(), f, width)
                if len(lines) == n:
                    cnt += 1
                    if abs(X0 + f.getlength(lines[-1]) * hs / S.SS - xe) <= 3:
                        ok += 1
            res.append((ok, cnt, fname, idx, px, hs))
res.sort(reverse=True)
for r in res[:10]:
    print(r)
