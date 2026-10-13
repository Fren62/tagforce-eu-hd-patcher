"""Tag Force 1 large-card name banner: extract / measure / render / write back.
Banner (HD, 4x): 320x48 assembled from 3 atlas pieces of the 512x256 large card PNG.
"""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)))); import font_alt  # noqa: nessun font Apple
import numpy as np
from PIL import Image, ImageFilter

PIECES = [((320, 160, 512, 208), (0, 0)), ((320, 208, 448, 240), (192, 0)), ((0, 240, 128, 256), (192, 32))]
BASE, X0, MAXW = 34, 12, 300  # measured on MikeyMK/chrisfand banners


def extract(im):
    b = Image.new('RGBA', (320, 48), (0, 0, 0, 0))
    for src, dst in PIECES:
        b.paste(im.crop(src), dst)
    return b


def write_back(im, b):
    im = im.copy()
    for (x0, y0, x1, y1), (dx, dy) in PIECES:
        im.paste(b.crop((dx, dy, dx + x1 - x0, dy + y1 - y0)), (x0, y0))
    return im


def text_color(b):
    a = np.array(b)
    op = a[a[..., 3] > 200][:, :3]
    return tuple(int(v) for v in np.median(op, 0)) if len(op) else None


def alpha(text, p):
    """banner alpha (48x320, 0..1) in style p (fitted on the HD banners by fit_banner.py)."""
    import cv2
    import small_it as S
    m, asc = S.smallcaps(text.replace("'", '\u2019'), p['font'], p['cap'], p['cap'] * p['sc'], p.get('track', 0.0))
    if p['emb'] > 0:
        m = m.filter(ImageFilter.MaxFilter(p['emb']))
    elif p['emb'] < 0:
        m = m.filter(ImageFilter.MinFilter(-p['emb']))
    a = np.asarray(m)
    cols = np.where(a.max(0) > 0)[0]
    m = Image.fromarray(a[:, cols.min():cols.max() + 1])
    nat = m.width / S.SS * p['hs']
    r = min(1.0, MAXW / nat)
    v = max(0.94, min(1.0, r / 0.6))  # nomi lunghi: solo condensati (le carte inglesi HD hanno la stessa altezza, misurato)
    m = S.widen(m, r, asc / S.SS, p['hs'], stem=0.08)
    m = m.resize((max(1, round(nat * r)), max(1, round(m.height / S.SS * v))), Image.LANCZOS)
    al = np.zeros((48, 320), np.float32)
    top = p['base'] - asc / S.SS * v
    ty = int(np.floor(top))
    sub = np.asarray(m, np.float32) / 255
    sub = cv2.warpAffine(np.pad(sub, ((1, 1), (0, 0))), np.float32([[1, 0, 0], [0, 1, top - ty]]), (sub.shape[1], sub.shape[0] + 2), flags=cv2.INTER_LINEAR)
    y0 = ty - 1
    ya, yb = max(0, y0), min(48, y0 + sub.shape[0]); xb = min(320, X0 + sub.shape[1])
    al[ya:yb, X0:xb] = np.maximum(al[ya:yb, X0:xb], sub[ya - y0:yb - y0, :xb - X0])
    al = np.power(np.clip(al, 0, 1), p['g'])
    return np.clip((al - 0.5) * p['k'] + 0.5, 0, 1) * (al > 0)  # edge contrast like the HD banners


# fitted on 24 English HD banners (fit_banner.py): cap/small-cap heights, baseline, width, ink density,
# stem width and edge softness all within measurement noise
STYLE = dict(font=('/System/Library/Fonts/Supplemental/Charter.ttc', 3), cap=24.0, sc=0.75, emb=0, hs=0.926, base=35.25,
             g=1.2, k=1.4, track=0.02)


def make_banner(text, color, style=STYLE):
    """like the original HD banners: constant text colour, only alpha varies (no dark fringe when filtered)."""
    b = Image.new('RGBA', (320, 48), color + (0,))
    b.putalpha(Image.fromarray((alpha(text, style) * 255).round().astype(np.uint8)))
    return b
