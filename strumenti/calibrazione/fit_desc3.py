"""Physical calibration of the description text on the English HD cards.
- line box measured: justified lines span x 22..234 (212 px)
- px: chosen so that the first-line ink profile FWHM matches the English cards
- hs: chosen so that the English text wraps into the same number of lines as the English cards
- emb (weight): chosen by blurred correlation
usage: fit_desc3.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG KIND FONT_FILE FONT_INDEX"""
import os, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import Image
import small_it as S
import fit_desc as FD
import fit_desc2 as FD2
from smallbg import frame_of

cards, kind, cdir = FD.cards, FD.kind, FD.cdir
X0, X1 = 22.0, 234.0
LY = (199, 207) if kind != 'st' else (192, 200)   # first line band


def fwhm(band):
    prof = band.mean(1)
    up = np.interp(np.arange(0, len(prof), 0.25), np.arange(len(prof)), prof)
    above = np.where(up >= 0.5 * up.max())[0]
    return (above.max() - above.min() + 1) * 0.25


ids = [cid for cid in FD2.WIDS if len(cards[cid]['desc']) > 60][:80]
ref = np.median([fwhm(np.abs(np.asarray(Image.open(os.path.join(cdir, 'small', f'{cid}.png')).convert('RGB')).astype(float)
                             - FD.CLEAN[frame_of(cards[cid])]).sum(-1)[LY[0]:LY[1], 24:232]) for cid in ids])
base0 = FD.p['base']


def my_fwhm(px, hs, emb):
    vals = []
    for cid in ids[:30]:
        cv, _ = FD.render(cards[cid]['desc'], dict(px=px, pitch=5.5, base=base0, x0=X0, x1=X1, emb=emb, hs=hs))
        y0 = FD.BOX[1]
        vals.append(fwhm(cv[LY[0] - y0:LY[1] - y0, 24 - FD.BOX[0]:232 - FD.BOX[0]]))
    return float(np.median(vals))


res = []
for emb in (0, 3, 5):
    # px from the vertical profile (hs does not change it)
    pxs = np.arange(5.6, 8.61, 0.2)
    fw = [my_fwhm(px, 1.0, emb) for px in pxs]
    px = float(pxs[int(np.argmin([abs(f - ref) for f in fw]))])
    # hs from line breaks
    f = S.font(FD.FONT, px * S.SS)
    agree = {}
    for hs in np.arange(0.70, 1.16, 0.01):
        agree[round(float(hs), 2)] = sum(len(S.wrap(cards[cid]['desc'].split(), f, (X1 - X0) * S.SS / hs)) == FD2.MEAS[cid] for cid in FD2.WIDS)
    top = max(agree.values())
    hs_ok = [h for h, a in agree.items() if a >= top - 1]
    hs = float(np.median(hs_ok))
    # baseline + correlation
    best = max(((FD.score(dict(px=px, pitch=5.5, base=float(b), x0=X0, x1=X1, emb=emb, hs=hs)), float(b))
                for b in np.arange(base0 - 1.0, base0 + 1.01, 0.25)))
    res.append((best[0], emb, px, hs, best[1], top))
    print(f'peso {emb}: corpo {px:.1f} (FWHM rif {ref:.2f}), larghezza {hs:.2f} (righe uguali {top}/{len(FD2.WIDS)}), base {best[1]}, correlazione {best[0]:.4f}', flush=True)
s, emb, px, hs, b, top = max(res)
print(f'MIGLIORE {os.path.basename(FD.FONT[0])} {FD.FONT[1]}: corr {s:.4f} px {px} hs {hs} emb {emb} base {b} righe {top}/{len(FD2.WIDS)}')
