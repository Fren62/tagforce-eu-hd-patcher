"""Game numbers texture (icon03.gim, 128x128): in MikeyMK's pack (ui/duels/numbers.png, 512x512) the big digits and
icons are redrawn, but the rows of symbols, the small digits, "x1 ... x12" (the level multiplier in the deck list)
are only enlarged in steps (nearest). Here those bands are rebuilt from the original at 128 px with a
smoothed enlargement (bicubic on premultiplied colours + re-sharpened alpha edge), in the same positions.
usage: hd_numbers.py ALL_I.ehp BASE_PACK OUT_PNG      (BASE_PACK contains ui/duels/numbers.png; ALL_I.ehp = USRDIR/deck/all_i.ehp)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from PIL import Image
from ehp import read
import gim
import cv2

# bands (y0, y1) in the 512x512 texture that are only enlarged in steps
FASCE = [(0, 36), (36, 70), (146, 184), (180, 224), (224, 264)]   # the bar/arrow icons (266-328) stay as they were: smoothed they swell


def smooth(rgba, k=4, lo=0.30, hi=0.62):
    """smoothed enlargement of a chunky-pixel RGBA image: bicubic premultiplied colours, alpha with re-sharpened edge."""
    a = np.asarray(rgba, np.float32) / 255
    pm = a.copy(); pm[..., :3] *= a[..., 3:4]
    big = cv2.resize(pm, (a.shape[1] * k, a.shape[0] * k), interpolation=cv2.INTER_CUBIC)
    al = cv2.GaussianBlur(np.clip(big[..., 3], 0, 1), (0, 0), 0.6)
    t = np.clip((al - lo) / (hi - lo), 0, 1)
    al2 = t * t * (3 - 2 * t)                                        # smoothstep: sharp edges but without steps
    col = np.clip(big[..., :3] / np.maximum(big[..., 3:4], 1e-3), 0, 1)
    return np.dstack([col, al2])


def main(all_i, pack, out):
    low = gim.to_png(gim.parse(read(all_i)['icon03.gim'])).convert('RGBA')
    base = Image.open(os.path.join(pack, 'ui/duels/numbers.png')).convert('RGBA')
    assert low.size == (128, 128) and base.size == (512, 512)
    res = np.asarray(base).astype(np.float32) / 255
    sm = smooth(low)
    # the game cuts each symbol with a precise rectangle: the smoothed ink must not leave the original's footprint
    # (before, the edge of the "6" rose by 1-3 px and was cut flat): outside the footprint alpha is 0, inside it fades in 1.5 px
    fp = (np.asarray(low.resize((512, 512), Image.NEAREST))[..., 3] > 0).astype(np.uint8)
    dist = cv2.distanceTransform(fp, cv2.DIST_L2, 3)
    sm[..., 3] *= np.clip((dist - 0.5) / 1.5, 0, 1)
    # rows "x1...x6" and "x7...x12": the game cuts each symbol from the first row of strong ink of the original (rows 46 and 57 at
    # low resolution); the smoothed enlargement rose one row above and the top (the tail of the 6) was cut flat.
    # Everything above that row is zeroed and faded in over the first 10 px, so the top stays rounded.
    for (y0, y1), top in (((180, 224), 184), ((224, 264), 228)):
        sm[y0:top, :, 3] = 0
        t = np.clip((np.arange(top, top + 10) - top + 1) / 11.0, 0, 1)
        sm[top:top + 10, :, 3] *= (t * t * (3 - 2 * t))[:, None]
    for y0, y1 in FASCE:
        res[y0:y1] = sm[y0:y1]
    Image.fromarray((res * 255).round().astype(np.uint8)).save(out)
    print('written', out)


if __name__ == '__main__':
    main(*sys.argv[1:4])
