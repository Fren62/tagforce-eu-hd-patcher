"""Smoothed enlargement of chunky-pixel sprites, contained in the original box.
In the game every sprite (digit, arrow, icon) is cut from a rectangle that coincides with the original's pixels: if the enlarged
version goes out of that box (a rounded stroke reaching the edge) the game cuts it flat. Here every connected
component of the original (with its shadow) is enlarged on its own (bicubic on premultiplied colours + re-sharpened
alpha edge) and then FITTED inside its own box shrunk by `margin` pixels, so the ends stay
rounded instead of cut off.
MikeyMK's pack redraws many icons but leaves others only enlarged 4x in blocks: this tool rebuilds only the
components that in its PNG are still a block (nearest) enlargement of the original, or those in the given bands.
usage: pixel_hd.py ORIGINAL_128.png HD.png OUT.png [margin_px=1.5] [all | y0-y1,y0-y1,...]
  without options it replaces only the components identical to a nearest enlargement; with 'all' it rebuilds all of them;
  with bands (y in HD pixels, e.g. 0-36,146-264) each band is handled on its own (components do not pass from one band to another)."""
import sys
import numpy as np
import cv2
from PIL import Image


def smooth(rgba, k=4, lo=0.30, hi=0.62):
    a = np.asarray(rgba, np.float32) / 255
    pm = a.copy(); pm[..., :3] *= a[..., 3:4]
    big = cv2.resize(pm, (a.shape[1] * k, a.shape[0] * k), interpolation=cv2.INTER_CUBIC)
    al = cv2.GaussianBlur(np.clip(big[..., 3], 0, 1), (0, 0), 0.6)
    t = np.clip((al - lo) / (hi - lo), 0, 1)
    col = np.clip(big[..., :3] / np.maximum(big[..., 3:4], 1e-3), 0, 1)
    return np.dstack([col, t * t * (3 - 2 * t)])


def fit(spr, x0, y0, x1, y1):
    """spr: float RGBA sprite (HD); resizes it (anisotropic) so the ink fits in [x0,x1)x[y0,y1)."""
    ys, xs = np.where(spr[..., 3] > 0.04)
    if not len(xs):
        return spr
    bx0, bx1, by0, by1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    crop = spr[by0:by1, bx0:bx1]
    w, h = max(1, round(x1 - x0)), max(1, round(y1 - y0))
    if (bx1 - bx0) <= w and (by1 - by0) <= h:      # already inside: not touched
        return spr
    nw, nh = min(bx1 - bx0, w), min(by1 - by0, h)
    pm = crop.copy(); pm[..., :3] *= pm[..., 3:4]
    pm = cv2.resize(pm, (nw, nh), interpolation=cv2.INTER_AREA)
    pm[..., :3] /= np.maximum(pm[..., 3:4], 1e-3)
    out = np.zeros_like(spr)
    ox, oy = bx0 + (bx1 - bx0 - nw) // 2, by0 + (by1 - by0 - nh) // 2
    out[oy:oy + nh, ox:ox + nw] = pm
    return out


def rebuild(low_arr, hd_a, nn, res, margin, k, only_nearest, rows=None):
    """low_arr: original uint8 RGBA (with alpha already zeroed outside the band); modifies res (HD, 0..1) in place."""
    a = low_arr[..., 3] > 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(a.astype(np.uint8), connectivity=8)
    done = 0
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area < 6:
            continue
        mask_low = (lab == i)
        mask_hd = np.kron(mask_low, np.ones((k, k), bool))
        if only_nearest:
            d = np.abs(hd_a[..., :3] - nn[..., :3])[mask_hd].mean() + np.abs(hd_a[..., 3] - nn[..., 3])[mask_hd].mean()
            if d > 14:      # already redrawn by MikeyMK
                continue
        only = np.zeros_like(low_arr)
        only[mask_low] = low_arr[mask_low]
        spr = smooth(Image.fromarray(only, 'RGBA'), k)
        spr = fit(spr, x * k + margin, y * k + margin, (x + w) * k - margin, (y + h) * k - margin)
        res[mask_hd] = 0
        al = spr[..., 3:4]
        da = res[..., 3:4]
        oa = al + da * (1 - al)
        res[..., :3] = np.where(oa > 0, (spr[..., :3] * al + res[..., :3] * da * (1 - al)) / np.maximum(oa, 1e-6), 0)
        res[..., 3:4] = oa
        done += 1
    return done, n - 1


def main(orig, hd, out, margin=1.5, all=False, k=4, bands=None):
    low = Image.open(orig).convert('RGBA')
    H = Image.open(hd).convert('RGBA')
    assert H.size == (low.width * k, low.height * k), (low.size, H.size)
    nn = np.asarray(low.resize(H.size, Image.NEAREST)).astype(np.float32)
    hd_a = np.asarray(H).astype(np.float32)
    res = hd_a.copy() / 255
    low_arr = np.asarray(low).copy()
    tot = [0, 0]
    if bands:
        for b0, b1 in bands:
            lb = low_arr.copy()
            lb[:b0 // k] = 0; lb[b1 // k:] = 0
            f, n = rebuild(lb, hd_a, nn, res, margin, k, False)
            tot[0] += f; tot[1] += n
    else:
        f, n = rebuild(low_arr, hd_a, nn, res, margin, k, not all)
        tot = [f, n]
    Image.fromarray((np.clip(res, 0, 1) * 255).round().astype(np.uint8)).save(out)
    print(f'componenti ricostruite: {tot[0]} su {tot[1]}')


if __name__ == '__main__':
    a = sys.argv
    fasce = [tuple(int(v) for v in t.split('-')) for t in a[-1].split(',')] if len(a) > 4 and a[-1][0].isdigit() and '-' in a[-1] else None
    mg = float(a[4]) if len(a) > 4 and a[4].replace('.', '').isdigit() else 1.5
    main(a[1], a[2], a[3], mg, 'all' in a, 4, fasce)
