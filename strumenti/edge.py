"""Edge model of the HD pack's text (upscaled look): soft edges + a faint halo of the opposite
polarity 2-3 px outside the strokes, stronger horizontally. Works on a float alpha map; the
result can be <0 (halo) or >1, so it is composited with `composite`, not with PIL alpha."""
import cv2
import numpy as np


def edge_filter(a, p):
    """a: float32 alpha 0..1. p: dict(sx, sy, kx, hx, ky, hy): gaussian softness, then separate
    horizontal / vertical unsharp halos (strength k, extent h)."""
    if p.get('g', 1.0) != 1.0:   # continuous stroke weight: gamma < 1 thicker, > 1 thinner
        a = np.power(np.clip(a, 0, 1), p['g'])
    if p.get('c', 1.0) != 1.0:   # edge contrast: crisper strokes (fewer half-covered pixels), same weight
        a = np.clip((a - 0.5) * p['c'] + 0.5, 0, 1) * (a > 0)
    s = cv2.GaussianBlur(a, (0, 0), sigmaX=max(p['sx'], 0.01), sigmaY=max(p['sy'], 0.01))
    out = s.copy()
    if p.get('kx', 0) > 0:
        out += p['kx'] * (s - cv2.GaussianBlur(s, (0, 0), sigmaX=max(p['hx'], 0.01), sigmaY=0.01))
    if p.get('ky', 0) > 0:
        out += p['ky'] * (s - cv2.GaussianBlur(s, (0, 0), sigmaX=0.01, sigmaY=max(p['hy'], 0.01)))
    return out


def composite(canvas_rgb, alpha, color):
    """canvas_rgb: float32 HxWx3 (modified in place), alpha: HxW signed weights, color: rgb tuple."""
    c = np.asarray(color, np.float32)
    canvas_rgb += alpha[..., None] * (c - canvas_rgb)
    np.clip(canvas_rgb, 0, 255, out=canvas_rgb)
    return canvas_rgb
