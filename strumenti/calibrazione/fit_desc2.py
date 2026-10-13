"""Description style fit with two constraints:
1) horizontal metrics: the English text must wrap into the same number of lines as on the HD card;
2) among the configurations that wrap best, maximise the (blurred) correlation of the rendering.
usage: fit_desc2.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG KIND FONT_FILE FONT_INDEX"""
import os, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import Image
import small_it as S
import fit_desc as FD  # reuses render()/corr()/INK/IDS (same argv layout)
from cardprops import load
from smallbg import frame_of

cards, kind, cdir = FD.cards, FD.kind, FD.cdir


def measured_lines(cid):
    img = np.asarray(Image.open(os.path.join(cdir, 'small', f'{cid}.png')).convert('RGB')).astype(float)
    cl = FD.CLEAN[frame_of(cards[cid])]
    y0, y1 = (200, 231) if kind != 'st' else (192, 240)
    sm = np.convolve(np.abs(img - cl).sum(-1)[y0:y1, 20:236].mean(1), np.ones(3) / 3, mode='same')
    peaks = [y for y in range(1, len(sm) - 1) if sm[y] > sm[y - 1] and sm[y] >= sm[y + 1] and sm[y] > 0.35 * sm.max()]
    merged = []
    for y in peaks:
        if merged and y - merged[-1] < 3:
            if sm[y] > sm[merged[-1]]:
                merged[-1] = y
        else:
            merged.append(y)
    return len(merged)


want = {'effect': (1,), 'normal': (0,), 'st': (13, 14)}[kind]
WIDS = [cid for cid, c in sorted(cards.items()) if c['kind'] in want and '\n' not in c['desc'] and len(c['desc']) < 300
        and os.path.exists(os.path.join(cdir, 'small', f'{cid}.png'))][::3]
MEAS = {cid: measured_lines(cid) for cid in WIDS}

if __name__ == '__main__':
    cands = []
    for px in np.arange(6.0, 8.61, 0.2):
        f = S.font(FD.FONT, px * S.SS)
        for hs in np.arange(0.76, 1.12, 0.02):
            width = 215.0 * S.SS / hs
            agree = sum(len(S.wrap(cards[cid]['desc'].split(), f, width)) == MEAS[cid] for cid in WIDS)
            cands.append((agree, round(float(px), 2), round(float(hs), 2)))
    top = max(c[0] for c in cands)
    good = [c for c in cands if c[0] >= top - 2]
    print(os.path.basename(FD.FONT[0]), FD.FONT[1], f'righe uguali: max {top}/{len(WIDS)}, configurazioni buone {len(good)}', flush=True)

    best = None
    for agree, px, hs in good:
        for emb in (0, 3, 5):
            for base in np.arange(FD.p['base'] - 1.0, FD.p['base'] + 1.01, 0.25):
                p = dict(px=px, pitch=5.5, base=float(base), x0=21.0, x1=236.0, emb=emb, hs=hs)
                s = FD.score(p)
                if best is None or s > best[0]:
                    best = (s, agree, p)
    s, agree, p = best
    print(f'risultato: correlazione {s:.4f}, righe uguali {agree}/{len(WIDS)}', {k: round(v, 3) for k, v in p.items()}, flush=True)
