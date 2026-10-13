"""Description text: physical comparison between the English HD cards and our renderer drawing the
SAME English text on the same (erased) card.  Library used by fit_descfont.py and the previews.

measure(img, cid) -> dict of metrics on the description box:
  nlines, base1 (centre of the 1st line), pitch, xh (x-band FWHM), up / dn (ascender / descender
  extent above / below the x-band centre, rows with ink > 15% of the line peak), lastx (ink end of
  the last line), dark (p95 stroke darkness, luma), dens (ink per line area), xsh / xsv (stroke
  cross-sections, see xsec), soft (half-covered / solid pixels), cov (signed map for correlation)
"""
import os
import cv2
import numpy as np
from PIL import Image
import small_it as S
from cardprops import load
from smallbg import frame_of

LUMA = np.array([0.3, 0.59, 0.11], np.float32)
BOX = {'effect': (19, 199, 237, 231), 'normal': (19, 199, 237, 231), 'st': (19, 192, 237, 240)}
KINDS = {'effect': (1,), 'normal': (0,), 'st': (13, 14)}
MAXLINES = {'effect': 5, 'normal': 5, 'st': 7}   # English cards still at the nominal size


def xsec(d, axis):
    """median luma cross-section of the strokes: centre (local minimum darker than half the darkest
    pixels) and 1, 2, 3 px aside; axis 0 = across vertical stems, 1 = across horizontal strokes."""
    a = d if axis == 0 else d.T
    thr = 0.5 * np.percentile(a, 0.5)
    c = (a[:, 3:-3] < thr) & (a[:, 3:-3] <= a[:, 2:-4]) & (a[:, 3:-3] < a[:, 4:-2])
    ys, xs = np.where(c)
    xs = xs + 3
    if not len(xs):
        return np.zeros(4)
    prof = [a[ys, xs]] + [(a[ys, xs - o] + a[ys, xs + o]) / 2 for o in (1, 2, 3)]
    return np.median(np.array(prof), 1)


class Bench:
    def __init__(self, cdir, clean_dir, ehp, kind, n=16):
        self.cdir, self.kind = cdir, kind
        self.cards = load(ehp)
        self.clean = {}
        self.clean_dir = clean_dir
        cand = []
        for cid, c in sorted(self.cards.items()):
            if c['kind'] not in KINDS[kind] or '\n' in c['desc'] or len(c['desc']) < 50:
                continue
            p = os.path.join(cdir, 'small', f'{cid}.png')
            if not os.path.exists(p):
                continue
            cand.append(cid)
        two, more = [], []   # half of the samples with 3+ lines (line pitch), half with 2
        for cid in cand[::max(1, len(cand) // (12 * n))]:
            img = self.load(cid)
            m = self.measure(img, cid)
            if m and 2 <= m['nlines'] <= MAXLINES[kind]:
                (more if m['nlines'] >= 3 else two).append((cid, img, m))
        k = min(len(more), n // 2)
        self.samples = more[:k] + two[:n - k]
        self.ref = self.summary([s[2] for s in self.samples])

    def load(self, cid):
        return np.asarray(Image.open(os.path.join(self.cdir, 'small', f'{cid}.png')).convert('RGB'))

    def clean_of(self, cid):
        g = frame_of(self.cards[cid])
        if g not in self.clean:
            self.clean[g] = np.asarray(Image.open(os.path.join(self.clean_dir, f'clean_{g}.png')).convert('RGB')).astype(np.int32)
        return self.clean[g]

    def signed(self, img, cid):
        """luma(card) - luma(tone-matched clean frame) on the box: ink < 0, halo > 0."""
        x0, y0, x1, y1 = BOX[self.kind]
        a = img[y0:y1, x0:x1].astype(np.float32) @ LUMA
        c = self.clean_of(cid)[y0:y1, x0:x1].astype(np.float32) @ LUMA
        d = a - c
        bright = a >= np.percentile(a, 60)          # surely parchment
        return d - np.median(d[bright])

    def measure(self, img, cid):
        d = self.signed(img, cid)
        ink = np.clip(-d, 0, None)
        xs = slice(22 - BOX[self.kind][0], 234 - BOX[self.kind][0])
        prof = ink[:, xs].mean(1)
        if prof.max() < 1:
            return None
        up = np.interp(np.arange(0, len(prof) - 1, 0.1), np.arange(len(prof)), prof)
        sm = np.convolve(up, np.ones(9) / 9, mode='same')
        pk = [i for i in range(1, len(sm) - 1) if sm[i] > sm[i - 1] and sm[i] >= sm[i + 1] and sm[i] > 0.35 * sm.max()]
        lines = []
        for i in pk:
            if lines and i - lines[-1] < 35:
                if sm[i] > sm[lines[-1]]:
                    lines[-1] = i
            else:
                lines.append(i)
        if not lines:
            return None
        xh, ups, dns = [], [], []
        for k, i in enumerate(lines):
            half = 0.5 * sm[i]
            l = i
            while l > 0 and sm[l] > half:
                l -= 1
            r = i
            while r < len(sm) - 1 and sm[r] > half:
                r += 1
            xh.append((r - l) / 10)
            lo = 0.15 * sm[i]
            l = i
            while l > 0 and sm[l] > lo:
                l -= 1
            r = i
            while r < len(sm) - 1 and sm[r] > lo:
                r += 1
            if k > 0:
                ups.append((i - l) / 10)
            dns.append((r - i) / 10)
        y0 = BOX[self.kind][1]
        ly = int(round(lines[-1] / 10))
        band = ink[max(0, ly - 2):ly + 3]
        cols = np.where(band.max(0) > 0.35 * ink.max())[0]
        lastx = float(cols.max() + BOX[self.kind][0] + 1) if len(cols) else 0.0
        core = ink > 0.5 * np.percentile(ink, 99.5)
        dark = float(np.percentile(ink[core], 95)) if core.any() else 0.0
        cn = np.clip(ink / max(dark, 1e-3), 0, 1)
        soft = float(((cn > 0.2) & (cn < 0.8)).sum() / max(1, (cn >= 0.8).sum()))
        dens = float(cn[:, xs].sum() / (len(lines) * (234 - 22)))
        return dict(nlines=len(lines), base1=lines[0] / 10 + y0, pitch=float(np.diff(lines).mean() / 10) if len(lines) > 2 else np.nan,
                    xh=float(np.median(xh)), up=float(np.median(ups)) if ups else np.nan, dn=float(np.median(dns)),
                    lastx=lastx, dark=dark, dens=dens, xsh=xsec(d, 0), xsv=xsec(d, 1), soft=soft, cov=d)

    @staticmethod
    def summary(ms):
        keys = ('base1', 'pitch', 'xh', 'up', 'dn', 'dark', 'dens', 'soft')
        out = {k: float(np.nanmedian([m[k] for m in ms])) for k in keys}
        out.update({k: np.median([m[k] for m in ms], 0) for k in ('xsh', 'xsv')})
        return out

    def render(self, cid, img, style, text=None):
        """the card with its description erased and `text` (default: the English one) drawn in `style`."""
        c = self.cards[cid]
        arr = img.copy()
        clean = self.clean_of(cid)
        st = self.kind == 'st'
        col = S.ink_color(arr, clean, (19, 194, 237, 240) if st else (19, 201, 237, 231), (25, 20, 15), pct=80)
        S.erase(arr, clean, BOX[self.kind], light_ref=True)
        out = Image.fromarray(arr).convert('RGBA')
        S.draw_desc(out, c['desc'] if text is None else text, style, col)
        return np.asarray(out.convert('RGB'))

    def evaluate(self, style):
        ms, lines_err, last_err, corr = [], [], [], []
        for cid, img, ref in self.samples:
            m = self.measure(self.render(cid, img, style), cid)
            if m is None:
                return 1e9, None
            ms.append(m)
            lines_err.append(abs(m['nlines'] - ref['nlines']))
            if m['nlines'] == ref['nlines']:
                last_err.append(m['lastx'] - ref['lastx'])
            a = cv2.GaussianBlur(ref['cov'], (0, 0), 0.6); b = cv2.GaussianBlur(m['cov'], (0, 0), 0.6)
            a = a - a.mean(); b = b - b.mean()
            corr.append(float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9)))
        mine = self.summary(ms)
        R = self.ref
        r = dict(lines=float(np.mean(lines_err)), last=float(np.median(np.abs(last_err))) if last_err else 99.0,
                 corr=float(np.median(corr)), **{k: mine[k] - R[k] for k in ('base1', 'pitch', 'xh', 'up', 'dn', 'soft')},
                 xsh=float(np.abs(mine['xsh'] - R['xsh']).sum()), xsv=float(np.abs(mine['xsv'] - R['xsv']).sum()),
                 dark=mine['dark'] / R['dark'] - 1, dens=mine['dens'] / R['dens'] - 1)
        for k, v in r.items():   # e.g. a single line: no ascender measure -> heavy penalty, not NaN
            if not np.isfinite(v):
                r[k] = 9.9
        loss = (r['lines'] / 0.1 + r['last'] / 6 + (1 - r['corr']) / 0.05 + abs(r['base1']) / 0.25 + abs(r['xh']) / 0.15
                + abs(r['pitch']) / 0.05 + abs(r['up']) / 0.3 + abs(r['dn']) / 0.3 + abs(r['dark']) / 0.05 + abs(r['dens']) / 0.05
                + r['xsh'] / 8.0 + r['xsv'] / 4.0 + abs(r['soft']) / 0.5)
        return loss, r
