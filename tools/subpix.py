"""Sub-pixel text height metrics on a coverage map: small-cap body height and full cap height."""
import numpy as np


def subpix(cov, skip_first_run=False):
    solid = cov > 0.5
    cols = np.where(solid.any(0))[0]
    if len(cols) < 3:
        return None
    lx0 = cols.min()
    if skip_first_run:
        runs = []; s = p = None
        for x in cols:
            if s is None: s = x
            elif x != p + 1: runs.append((s, p)); s = x
            p = x
        runs.append((s, p))
        lx0 = runs[1][0] if len(runs) > 1 else runs[0][0]
    r = cov[:, lx0:].sum(1)
    pk = np.sort(r)[-4:].mean()
    half = 0.5 * pk
    idx = np.where(r >= half)[0]
    t, b = idx.min(), idx.max()
    top = t - (r[t] - half) / max(r[t] - r[t - 1], 1e-6) if t > 0 else float(t)
    bot = b + (r[b] - half) / max(r[b] - r[b + 1], 1e-6) if b + 1 < len(r) else float(b)
    q = 0.12 * pk
    idq = np.where(r >= q)[0]
    tq = idq.min()
    ctop = tq - (r[tq] - q) / max(r[tq] - r[tq - 1], 1e-6) if tq > 0 else float(tq)
    return float(bot - top), float(bot - ctop), float(bot)
