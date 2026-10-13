"""Ingrandimento levigato di sprite a pixel grossi, contenuto nel riquadro originale.
Nel gioco ogni sprite (cifra, freccia, icona) e' ritagliato da un rettangolo che coincide con i pixel dell'originale: se la
versione ingrandita esce da quel riquadro (un tratto arrotondato che arriva al bordo) il gioco la taglia di netto. Qui ogni
componente connessa dell'originale (con la sua ombra) e' ingrandita da sola (bicubico sui colori premoltiplicati + bordo
dell'alfa riaffilato) e poi ADATTATA dentro il proprio riquadro rimpicciolito di `margine` pixel, cosi' le estremita' restano
arrotondate invece che mozzate.
Il pack di MikeyMK ridisegna molte icone ma lascia altre solo ingrandite 4x a blocchi: questo strumento ricostruisce solo le
componenti che nel suo PNG sono ancora un ingrandimento a blocchi (nearest) dell'originale, oppure quelle in fasce indicate.
usage: pixel_hd.py ORIGINALE_128.png HD.png OUT.png [margine_px=1.5] [tutte | y0-y1,y0-y1,...]
  senza opzioni sostituisce solo le componenti identiche a un ingrandimento nearest; con 'tutte' le ricostruisce tutte;
  con fasce (y in pixel HD, es. 0-36,146-264) ogni fascia e' trattata da sola (le componenti non passano da una fascia all'altra)."""
import sys
import numpy as np
import cv2
from PIL import Image


def liscia(rgba, k=4, lo=0.30, hi=0.62):
    a = np.asarray(rgba, np.float32) / 255
    pm = a.copy(); pm[..., :3] *= a[..., 3:4]
    big = cv2.resize(pm, (a.shape[1] * k, a.shape[0] * k), interpolation=cv2.INTER_CUBIC)
    al = cv2.GaussianBlur(np.clip(big[..., 3], 0, 1), (0, 0), 0.6)
    t = np.clip((al - lo) / (hi - lo), 0, 1)
    col = np.clip(big[..., :3] / np.maximum(big[..., 3:4], 1e-3), 0, 1)
    return np.dstack([col, t * t * (3 - 2 * t)])


def adatta(spr, x0, y0, x1, y1):
    """spr: sprite RGBA float (HD); lo ridimensiona (anisotropo) perche' l'inchiostro stia in [x0,x1)x[y0,y1)."""
    ys, xs = np.where(spr[..., 3] > 0.04)
    if not len(xs):
        return spr
    bx0, bx1, by0, by1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    crop = spr[by0:by1, bx0:bx1]
    w, h = max(1, round(x1 - x0)), max(1, round(y1 - y0))
    if (bx1 - bx0) <= w and (by1 - by0) <= h:      # sta gia' dentro: non si tocca
        return spr
    nw, nh = min(bx1 - bx0, w), min(by1 - by0, h)
    pm = crop.copy(); pm[..., :3] *= pm[..., 3:4]
    pm = cv2.resize(pm, (nw, nh), interpolation=cv2.INTER_AREA)
    pm[..., :3] /= np.maximum(pm[..., 3:4], 1e-3)
    out = np.zeros_like(spr)
    ox, oy = bx0 + (bx1 - bx0 - nw) // 2, by0 + (by1 - by0 - nh) // 2
    out[oy:oy + nh, ox:ox + nw] = pm
    return out


def ricostruisci(low_arr, hd_a, nn, res, margine, k, solo_nearest, righe=None):
    """low_arr: originale RGBA uint8 (con alfa gia' azzerato fuori dalla fascia); modifica res (HD, 0..1) sul posto."""
    a = low_arr[..., 3] > 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(a.astype(np.uint8), connectivity=8)
    fatte = 0
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area < 6:
            continue
        mask_low = (lab == i)
        mask_hd = np.kron(mask_low, np.ones((k, k), bool))
        if solo_nearest:
            d = np.abs(hd_a[..., :3] - nn[..., :3])[mask_hd].mean() + np.abs(hd_a[..., 3] - nn[..., 3])[mask_hd].mean()
            if d > 14:      # gia' ridisegnata da MikeyMK
                continue
        solo = np.zeros_like(low_arr)
        solo[mask_low] = low_arr[mask_low]
        spr = liscia(Image.fromarray(solo, 'RGBA'), k)
        spr = adatta(spr, x * k + margine, y * k + margine, (x + w) * k - margine, (y + h) * k - margine)
        res[mask_hd] = 0
        al = spr[..., 3:4]
        da = res[..., 3:4]
        oa = al + da * (1 - al)
        res[..., :3] = np.where(oa > 0, (spr[..., :3] * al + res[..., :3] * da * (1 - al)) / np.maximum(oa, 1e-6), 0)
        res[..., 3:4] = oa
        fatte += 1
    return fatte, n - 1


def main(orig, hd, out, margine=1.5, tutte=False, k=4, bande=None):
    low = Image.open(orig).convert('RGBA')
    H = Image.open(hd).convert('RGBA')
    assert H.size == (low.width * k, low.height * k), (low.size, H.size)
    nn = np.asarray(low.resize(H.size, Image.NEAREST)).astype(np.float32)
    hd_a = np.asarray(H).astype(np.float32)
    res = hd_a.copy() / 255
    low_arr = np.asarray(low).copy()
    tot = [0, 0]
    if bande:
        for b0, b1 in bande:
            lb = low_arr.copy()
            lb[:b0 // k] = 0; lb[b1 // k:] = 0
            f, n = ricostruisci(lb, hd_a, nn, res, margine, k, False)
            tot[0] += f; tot[1] += n
    else:
        f, n = ricostruisci(low_arr, hd_a, nn, res, margine, k, not tutte)
        tot = [f, n]
    Image.fromarray((np.clip(res, 0, 1) * 255).round().astype(np.uint8)).save(out)
    print(f'componenti ricostruite: {tot[0]} su {tot[1]}')


if __name__ == '__main__':
    a = sys.argv
    fasce = [tuple(int(v) for v in t.split('-')) for t in a[-1].split(',')] if len(a) > 4 and a[-1][0].isdigit() and '-' in a[-1] else None
    mg = float(a[4]) if len(a) > 4 and a[4].replace('.', '').isdigit() else 1.5
    main(a[1], a[2], a[3], mg, 'tutte' in a, 4, fasce)
