"""\"Vector\" enlargement of pixel art: every colour of the original becomes a soft map, oversampled and chosen by
maximum (like a vectorization), then brought back to the final resolution with antialiasing. The edges stay sharp and rounded,
without the blurry effect of bicubic and without the steps of nearest.
It is used in place of pixel_hd.smooth:  pixel_hd.smooth = vector.vect"""
import numpy as np
import cv2


def _palette(px, mx):
    u, inv = np.unique(px.reshape(-1, 4), axis=0, return_inverse=True)
    if len(u) <= mx:
        return u.astype(np.float32), inv.reshape(px.shape[:2])
    data = px.reshape(-1, 4).astype(np.float32)
    data[:, :3] *= data[:, 3:4] / 255.0                     # premultiplied: the transparent ones group together
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.5)
    _, lab, cen = cv2.kmeans(data, mx, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    cen = cen.copy(); cen[:, :3] = cen[:, :3] / np.maximum(cen[:, 3:4] / 255.0, 1e-3)
    return np.clip(cen, 0, 255), lab.reshape(px.shape[:2])


def vect(rgba, k=4, lo=None, hi=None, sigma=0.55, sup=2, maxcol=40):
    """rgba: PIL image or uint8 array (h, w, 4) at low resolution. Returns float (h*k, w*k, 4) 0..1, non-premultiplied colour."""
    px = np.asarray(rgba, np.uint8)
    h, w = px.shape[:2]
    pal, lab = _palette(px, maxcol)
    s = k * sup
    best, arg = None, None
    for i in range(len(pal)):
        m = (lab == i).astype(np.float32)
        m = cv2.GaussianBlur(m, (0, 0), sigma, borderType=cv2.BORDER_REPLICATE)
        m = cv2.resize(m, (w * s, h * s), interpolation=cv2.INTER_LINEAR)
        if best is None:
            best, arg = m, np.zeros(m.shape, np.int32)
        else:
            up = m > best
            best[up] = m[up]; arg[up] = i
    big = pal[arg] / 255.0                                  # (H*s, W*s, 4) straight
    pm = big.copy(); pm[..., :3] *= pm[..., 3:4]
    pm = cv2.resize(pm, (w * k, h * k), interpolation=cv2.INTER_AREA)
    al = pm[..., 3:4]
    col = np.clip(pm[..., :3] / np.maximum(al, 1e-3), 0, 1)
    return np.dstack([col, al])


def _epx(a):
    """Scale2x (EPX) on an array (h, w, 4) uint8: sharp edges, 1-pixel details remain."""
    h, w = a.shape[:2]
    p = np.pad(a, ((1, 1), (1, 1), (0, 0)), mode='edge')
    P = a; A = p[:-2, 1:-1]; D = p[2:, 1:-1]; C = p[1:-1, :-2]; B = p[1:-1, 2:]
    eq = lambda x, y: (x == y).all(axis=2)
    out = np.empty((h * 2, w * 2, 4), a.dtype)
    out[0::2, 0::2] = np.where((eq(C, A) & ~eq(C, D) & ~eq(A, B))[..., None], A, P)
    out[0::2, 1::2] = np.where((eq(A, B) & ~eq(A, C) & ~eq(B, D))[..., None], B, P)
    out[1::2, 0::2] = np.where((eq(D, C) & ~eq(D, B) & ~eq(C, A))[..., None], C, P)
    out[1::2, 1::2] = np.where((eq(B, D) & ~eq(B, A) & ~eq(D, C))[..., None], D, P)
    return out


def epx4(rgba, k=4, aa=0.7, **_):
    """Scale4x = two EPX passes, then light antialiasing of the remaining steps. k must be 4."""
    px = np.asarray(rgba, np.uint8)
    big = _epx(_epx(px)).astype(np.float32) / 255.0
    pm = big.copy(); pm[..., :3] *= pm[..., 3:4]
    if aa:
        pm = cv2.GaussianBlur(pm, (0, 0), aa)
    al = pm[..., 3:4]
    return np.dstack([np.clip(pm[..., :3] / np.maximum(al, 1e-3), 0, 1), al])


def hybrid(rgba, k=4, lo=None, hi=None, threshold=48, aa=0.6):
    """EPX 4x (sharp edges) where the original has outlines, bicubic where the colours vary slowly (gradients, background rows)."""
    px = np.asarray(rgba, np.uint8)
    h, w = px.shape[:2]
    E = epx4(px, 4, aa=aa)
    a = px.astype(np.float32) / 255.0
    pm = a.copy(); pm[..., :3] *= pm[..., 3:4]
    B = cv2.resize(pm, (w * 4, h * 4), interpolation=cv2.INTER_CUBIC)
    alB = np.clip(B[..., 3:4], 0, 1)
    B = np.dstack([np.clip(B[..., :3] / np.maximum(alB, 1e-3), 0, 1), alB])
    p = np.pad(px.astype(np.int16), ((1, 1), (1, 1), (0, 0)), mode='edge')
    d = np.zeros((h, w), np.int16)
    for dy, dx in ((0, 1), (2, 1), (1, 0), (1, 2)):
        d = np.maximum(d, np.abs(p[dy:dy + h, dx:dx + w] - px).max(axis=2))
    m = (d > threshold).astype(np.float32)
    m = cv2.dilate(m, np.ones((3, 3), np.uint8))
    m = cv2.GaussianBlur(np.kron(m, np.ones((4, 4), np.float32)), (0, 0), 1.2)[..., None]
    out = E * m + B * (1 - m)
    # alpha: from the EPX (sharp edges), never larger than the bicubic outside the box
    out[..., 3:4] = E[..., 3:4]
    return out
