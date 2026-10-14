"""Per-element alignment of the Italian HD small cards vs the game's own Italian 64x64 cards.
usage: align_small.py TOOLS CARD_DIR CARDS_DIR [IDS...]"""
import sys; sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import Image
from tfcards import slots, small_blob, dxt1

card, C = sys.argv[2:4]
ids = [int(x) for x in sys.argv[4:]] or [4307, 4335, 4018, 4007, 4021]
d = open(f'{card}/cardm_i.cip', 'rb').read()
# regions in 64x64 card coordinates (x0, y0, x1, y1)
REG = {'CORNICE+ARTE': (0, 0, 64, 64), 'riquadro arte': (5, 11, 59, 47), 'nome': (4, 2, 54, 8), 'etichetta': (28, 8, 60, 11), 'riga Tipo': (4, 47, 40, 51), 'descrizione': (4, 49, 60, 58)}


def lum(a):
    return a.astype(float) @ np.array([0.3, 0.59, 0.11])


def shift_img(a, dx, dy):
    return np.asarray(Image.fromarray(a.astype(np.float32), mode='F').transform(
        (a.shape[1], a.shape[0]), Image.AFFINE, (1, 0, -dx, 0, 1, -dy), Image.BILINEAR))


res = {k: [] for k in REG}
for cid in ids:
    lo = lum(dxt1(small_blob(d, slots(d, cid)[0]), 64, 64))
    hd = Image.open(f'{C}/small_it/{cid}.png').convert('RGB')
    # bring HD to the same 64x64 grid (area average), then upsample both 8x for sub-pixel search
    hd64 = lum(np.asarray(hd.resize((64, 64), Image.BOX)))
    up = lambda a: np.asarray(Image.fromarray(a.astype(np.float32), mode='F').resize((512, 512), Image.BILINEAR))
    L0 = None
    L, H = up(lo), up(hd64)
    for name, (x0, y0, x1, y1) in REG.items():
        best = None
        for dx in np.arange(-24, 24.5, 1):      # 1/8 px steps of the 64 grid
            for dy in np.arange(-24, 24.5, 1):
                S = shift_img(H, dx, dy)[y0 * 8:y1 * 8, x0 * 8:x1 * 8]
                A = L[y0 * 8:y1 * 8, x0 * 8:x1 * 8]
                A = A - A.mean(); S = S - S.mean()
                c = (A * S).sum() / (np.sqrt((A * A).sum() * (S * S).sum()) + 1e-9)
                if best is None or c > best[0]:
                    best = (c, dx / 8, dy / 8)
        res[name].append((cid, *best))
for name, v in res.items():
    print(f'{name:12s}', '  '.join(f'{cid}: dx {dx:+.2f} dy {dy:+.2f} (c {c:.2f})' for cid, c, dx, dy in v))
