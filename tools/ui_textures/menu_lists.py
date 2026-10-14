"""menu_lists: HD Italian menu lists, title words, result icon sheet and calendar sheet (4x), in the style of the
English HD pack.

    python3 -I menu_lists.py USRDIR PACK_US OUT [texture id ...]

Textures (all redrawn at exactly 4x the Italian original, same words at the same places):
  title_menu_i__m_menu_title01   main menu titles (yellow)          ref ui/text/mainmenu_options.png
  title_menu_i__trnsmt02         wireless menu list (silver)        ref ui/text/dueloptions.png
  title_menu_i__press_start0003  PREMI TASTO START (yellow-green)   ref ui/text/press_start_button.png
  result_i__menu02               duel result titles (silver)        ref ui/text/duel_result.png
  result_i__menu01               result icon sheet + VITTORIA/PAREGGIO/SCONFITT labels (the pack has no HD of it)
  always_bri_ita__story_sys02    calendar sheet (days, months, digits, Giorni al Torneo, Mattina/Pomeriggio)
                                                                    ref ui/text/tournamentdates.png
Nothing of the mod's pixels is pasted: its HD art is a style reference (fonts, colours, outline, shadow) and every
letter is the system font's glyph, drawn here.

Lettering (all six textures).  Every line is ONE piece of lettering: one font, one size and weight per texture
family, one baseline, constant tracking inside the line, glyphs exactly as the font draws them (no stretching, no
shearing, no per-letter resizing or vertical moves).  Fonts, found by measuring the English HD letters:
  Futura Bold   menu lists (the natural width of Futura Bold at the cap height of the Italian lines matches the
                low-res lines within 1-3 %, so it is the game's font);
  Futura Condensed ExtraBold   the lines the game itself sets condensed: result_i__menu02 lines 3-4 (BONUS NUOVO PUNTEGGIO
                MASSIMO / BONUS COMPLETAMENTO SFIDA, 29 and 25 letters in 250 px, as in the English sheet) and the
                VITTORIA / PAREGGIO / SCONFITT labels (8 letters in 52 px).  It is the condensed cut of Futura Bold, same
                stem weight and round forms, so these lines keep the FULL cap height (17 rows / 11.3 rows) of the original
                with only a whole-line squeeze (labels: one squeeze, 0.90, for the three words; menu02: 0.83 / 0.98, the two
                lines are condensed differently in the original too);
  Times Bold    weekdays and months of the calendar (best overlap with the English HD words, same size as them);
  Hiragino Maru Gothic W4   digits, month/day kanji, "Days Until Tournament" style words (overlap with the HD digits
                and words, rounded stroke ends).
A line is placed on the left/right ink edges of the original: x0 and tracking are solved from them, the tracking is kept
inside [-0.03, +0.04] em, then the whole line may be squeezed by at most 10 %, and if it still does not fit the size is
reduced (cap height kept centred on the original's; lines of a group that all need it share the smallest size).  A line
that needs looser tracking than +0.04 em is centred on the original's ink instead.  The only per-letter freedom is an
optical pen shift (x only, at most 0.5 low-res px, the lists and labels only) so that the letters land where the
original's did; no letter changes shape.
HD look: lists = fill colours/gradient sampled from the English HD image (baseline aligned through a line level fit on the
English texture) + the soft edge and black drop shadow measured on the English HD lines; calendar = white fill, opaque
outline and soft shadow fitted on the English HD sheet; result sheet = clean upscale of the pixel art (class masks, then
a vector pass: the outline of every region is simplified to a polygon so the diagonals are straight; the antialiased
white check mark is rebuilt from its coverage as one crisp shape with a soft shadow)."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import alt_font  # noqa: nessun font Apple
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import cv2
from PIL import Image, ImageFont
import common

SUP = '/System/Library/Fonts/Supplemental/'
SYS = '/System/Library/Fonts/'
FUTURA_BOLD = (SUP + 'Futura.ttc', 2)
FUTURA_COND_MED = (SUP + 'Futura.ttc', 3)      # a face drawn as a condensed cut (not a squeezed Futura Bold)
FUTURA_COND_XB = (SUP + 'Futura.ttc', 4)
K = common.SCALE           # 4
SS = 16                    # super-sampling: pixels per low-res pixel for the final rendering (HD = SS / K)
FIT_SS = 8                 # super-sampling used while measuring / fitting


# ----------------------------------------------------------------------------------------------- glyphs
_fonts, _glyphs = {}, {}


def font(spec, size):
    k = (spec, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(spec[0], size, index=spec[1])
    return _fonts[k]


def glyph(spec, ch, size, stroke=0):
    """(alpha float32, left offset, top offset from the baseline) of one character at an integer pixel size,
    emboldened by `stroke` pixels (disc dilation)"""
    k = (spec, ch, size, stroke)
    if k not in _glyphs:
        f = font(spec, size)
        m, (ox, oy) = f.getmask2(ch, mode='L', anchor='ls')
        a = np.asarray(m, np.float32).reshape(m.size[1], m.size[0]) / 255.0 if m.size[0] else np.zeros((1, 1), np.float32)
        if stroke > 0:
            a = np.pad(a, ((stroke + 1, stroke + 1), (stroke + 1, stroke + 1)))
            ox -= stroke + 1
            oy -= stroke + 1
            a = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * stroke + 1, 2 * stroke + 1)))
        _glyphs[k] = (a, ox, oy)
    return _glyphs[k]


def cap_ratio(spec):
    """cap height of the font in em"""
    f = font(spec, 1000)
    b = f.getbbox('H', anchor='ls')
    return -b[1] / 1000.0


def pens(spec, text, size, sx, x0, track):
    """pen x of each character (low-res px): font advances (with kerning pairs) * sx + tracking"""
    f = font(spec, round(size * 64))
    xs, x = [], x0
    for i, ch in enumerate(text):
        xs.append(x)
        adv = f.getlength(text[i:i + 2]) - f.getlength(text[i + 1]) if i + 1 < len(text) else f.getlength(ch)
        x += adv / 64 * sx + track
    return xs


def paste_max(can, a, X, Y):
    y0, x0 = max(Y, 0), max(X, 0)
    y1, x1 = min(Y + a.shape[0], can.shape[0]), min(X + a.shape[1], can.shape[1])
    if y1 > y0 and x1 > x0:
        np.maximum(can[y0:y1, x0:x1], a[y0 - Y:y1 - Y, x0 - X:x1 - X], out=can[y0:y1, x0:x1])


def down(a, k):
    H, W = a.shape[0] // k, a.shape[1] // k
    return a[:H * k, :W * k].reshape(H, k, W, k).mean((1, 3))


class Line:
    """one line of lettering: font, size, weight (px of emboldening), squeeze, tracking, left pen, baseline (low-res px,
    sheet coordinates).  The squeeze is applied to the whole line, every glyph is the font's glyph, unmodified."""

    def __init__(self, text, spec=FUTURA_BOLD, size=20.0, bold=0.3, sx=1.0, x0=0.0, track=0.0, yb=16.0):
        self.text, self.spec = text, spec
        self.size, self.bold, self.sx, self.x0, self.track, self.yb = size, bold, sx, x0, track, yb
        self.gdx = [0.0] * len(text)      # optical spacing: per-letter pen shift (x only), bounded by the fitter

    def pen_x(self):
        return [x + d for x, d in zip(pens(self.spec, self.text, self.size, self.sx, self.x0, self.track), self.gdx)]

    def render(self, H, W, ss, k, y_off=0.0, x_off=0.0):
        """coverage of the line on a canvas of H x W low-res px whose top-left is (x_off, y_off) in sheet coordinates,
        rendered at ss px per low-res px and area-averaged down to k px per low-res px"""
        can = np.zeros((H * ss, W * ss), np.float32)
        xs = self.pen_x()
        for i, ch in enumerate(self.text):
            if ch != ' ':
                a, ox, oy = glyph(self.spec, ch, max(1, round(self.size * ss)), max(0, round(self.bold * ss)))
                w = max(1, round(a.shape[1] * self.sx))
                if w != a.shape[1]:
                    a = cv2.resize(a, (w, a.shape[0]), interpolation=cv2.INTER_AREA if w < a.shape[1] else cv2.INTER_LINEAR)
                paste_max(can, a, round((xs[i] - x_off) * ss + ox * self.sx), round((self.yb - y_off) * ss + oy))
        return down(can, ss // k)


# ----------------------------------------------------------------------------------------------- measuring the original
def fill_estimate(L):
    """fill coverage of a low-res text texture whose words have a BLACK drop shadow: premultiplied colour divided
    by the row's fill colour (the colour of the fully covered pixels of that row; gradients are vertical)"""
    L = np.asarray(L, np.float32)
    P = L[..., :3].sum(2) * L[..., 3] / 255.0
    G = np.zeros(L.shape[0], np.float32)
    for y in range(L.shape[0]):
        m = L[y, :, 3] == 255
        if m.any():
            G[y] = L[y, m, :3].sum(1).max()
    idx = np.nonzero(G)[0]
    for y in range(L.shape[0]):
        if G[y] == 0 and len(idx):
            G[y] = G[idx[np.abs(idx - y).argmin()]]
    return np.clip(P / np.maximum(G[:, None], 1), 0, 1)


def outline_fill_estimate(L, outline_rgb):
    """fill coverage of WHITE words with an opaque coloured outline (and a translucent shadow): luminance between the
    outline and white on the opaque pixels"""
    L = np.asarray(L, np.float32)
    w = np.array([0.299, 0.587, 0.114], np.float32)
    lo = float(np.dot(outline_rgb, w))
    return np.clip((L[..., :3] @ w - lo) / (255 - lo), 0, 1) * (L[..., 3] > 254.5)


def colour_fill_estimate(L, fill_rgb):
    """fill coverage of words of one flat colour on a transparent background (partial coverage is in the alpha, the
    shadow is black): projection of the premultiplied colour on the fill colour"""
    L = np.asarray(L, np.float32)
    c = np.asarray(fill_rgb, np.float32)
    return np.clip((L[..., :3] @ c) * L[..., 3] / 255.0 / float(c @ c), 0, 1)


def line_rows(L, pad=1, n=None):
    """(y0, y1) row ranges of the text lines (rows with any visible pixel), padded.  n = expected number of lines: if the
    accents of the capitals (French) merge two lines, the pitch of the clean lines is used (the lines have a fixed pitch)"""
    a = np.asarray(L)[..., 3]
    rows = (a > 0).any(1)
    segs, y = [], 0
    while y < len(rows):
        if rows[y]:
            s = y
            while y < len(rows) and rows[y]:
                y += 1
            segs.append((max(s - pad, 0), min(y + pad, len(rows))))
        y += 1
    if n is not None and len(segs) != n:
        import collections
        p = collections.Counter(b - a_ for a_, b in segs if b - a_ <= 23).most_common(1)[0][0]       # line pitch (21): the most frequent (de: a clean line is 22 high)
        segs = [(i * p, (i + 1) * p) for i in range(n)]
    return segs


def extent(T):
    """(left, right) ink edges of a fill coverage image, sub-pixel (column maxima)"""
    cm = T.max(0)
    cols = np.nonzero(cm > 0.05)[0]
    return cols[0] + (1 - cm[cols[0]]), cols[-1] + cm[cols[-1]]


class Fitter:
    """fits a Line on the fill coverage F inside the window box = (x0, y0, x1, y1) of the original (low-res px);
    only line level parameters"""

    def __init__(self, F, box, ss=FIT_SS):
        x0, y0, x1, y1 = box
        self.x0, self.y0, self.x1, self.y1, self.ss = x0, y0, x1, y1, ss
        self.T = F[y0:y1, x0:x1]
        self.H, self.W = self.T.shape
        l, r = extent(self.T)
        self.xl, self.xr = l + x0, r + x0
        rows = self.T.sum(1)
        ys = np.nonzero(rows > 0.05 * rows.max())[0]
        self.ytop, self.ybot = ys[0] + y0, ys[-1] + 1 + y0        # ink rows of the original (low-res px)

    def image(self, ln, wide=False):
        """coverage of the line on the window of the original (wide: on a canvas wide enough for any line)"""
        im = np.minimum(ln.render(self.H, self.W + 480, self.ss, 1, self.y0, self.x0), 1)
        return im if wide else im[:, :self.W]

    def ext(self, ln):
        l, r = extent(self.image(ln, True))
        return l + self.x0, r + self.x0

    def err(self, ln):
        return float(((self.image(ln) - self.T) ** 2).sum())

    def fit_yb(self, ln):
        best = (self.err(ln), ln.yb)
        y_c, step = ln.yb, 0.5
        while step >= 0.0625:
            for d in (-step, step):
                ln.yb = best[1] + d
                e = self.err(ln)
                if e < best[0]:
                    best = (e, ln.yb)
            if best[1] == y_c:
                step /= 2
            y_c = best[1]
        ln.yb = best[1]
        return best[0]

    def solve_edges(self, ln, fix_track=False):
        """x0 and tracking that put the ink edges of the line on those of the original (secant steps)"""
        n = len(ln.text)
        for _ in range(4):
            xl, xr = self.ext(ln)
            ln.x0 += self.xl - xl
            if fix_track or n < 2:
                break
            xl, xr = self.ext(ln)
            ln.track += ((self.xr - self.xl) - (xr - xl)) / (n - 1)
            if abs((xr - xl) - (self.xr - self.xl)) < 0.02:
                break
        xl, xr = self.ext(ln)
        ln.x0 += self.xl - xl

    def centre(self, ln):
        """x0 such that the ink of the line is centred on the ink of the original"""
        xl, xr = self.ext(ln)
        ln.x0 += (self.xl + self.xr) / 2 - (xl + xr) / 2

    def fit_spacing(self, ln, bound=0.5):
        """optical letter spacing: a pen shift (x only, |dx| <= bound low-res px) per letter, nothing else of the
        letter changes (no scaling, no vertical move)"""
        e = self.err(ln)
        for step in (0.25, 0.125, 0.0625):
            for _ in range(2):
                for i, ch in enumerate(ln.text):
                    if ch == ' ':
                        continue
                    for sg in (1, -1):
                        while True:
                            old = ln.gdx[i]
                            ln.gdx[i] = old + sg * step
                            if abs(ln.gdx[i]) > bound + 1e-9:
                                ln.gdx[i] = old
                                break
                            e2 = self.err(ln)
                            if e2 < e - 1e-6:
                                e = e2
                            else:
                                ln.gdx[i] = old
                                break
        return e

    def fit_size_bold(self, text, sizes, bold=0.3, spec=FUTURA_BOLD):
        """size (and sx) free: used for the English lines (colour baseline)"""
        best = None
        for size in sizes:
            for sx in (1.0, 0.9, 0.8):
                ln = Line(text, spec, size=size, bold=bold, sx=sx, x0=self.xl, yb=self.y1 - 3.0)
                self.solve_edges(ln)
                self.fit_yb(ln)
                self.solve_edges(ln)
                e = self.err(ln)
                if best is None or e < best[0]:
                    best = (e, ln)
        best[1].rms = (best[0] / self.T.size) ** 0.5
        return best[1]

    def fit_set(self, text, size, bold, spec=FUTURA_BOLD, tmin=0.03, sx_min=0.9, size_min=0.4, spacing=0.5,
                k_fixed=None, sx_fixed=None, max_track=0.04, yb=None):
        """the line of the Italian texture, common size / weight `size`, `bold`: tracking solved from the width; if it
        would be tighter than -tmin em the line is squeezed (down to sx_min), if that is not enough the size shrinks
        (weight in proportion) and the cap height stays centred on the original's.  The tracking is kept inside
        [-tmin, +max_track] em; a line that would need more is centred on the original's ink instead of justified to it.
        k_fixed / sx_fixed: size factor / squeeze imposed by a group of lines that share them."""
        cr = cap_ratio(spec)
        n = len(text)
        tgt = self.xr - self.xl
        if yb is None:
            ln0 = Line(text, spec, size=size, bold=bold, x0=self.xl, yb=self.ybot - 0.5)
            self.solve_edges(ln0)
            self.fit_yb(ln0)
            yb = ln0.yb
        k = 1.0 if k_fixed is None else k_fixed
        sxs = [sx_fixed] if sx_fixed is not None else list(np.arange(1.0, sx_min - 1e-6, -0.005))
        while True:
            s = size * k
            ln = Line(text, spec, size=s, bold=bold * k, x0=self.xl, yb=yb - cr * (size - s) / 2)
            xl, xr = self.ext(ln)
            w0 = xr - xl                                    # natural width at this size
            ok = False
            for sx in sxs:
                track = (tgt - w0 * sx) / (n - 1)
                if track >= -tmin * s:
                    ok = True
                    break
            if ok or k_fixed is not None or k <= size_min:
                break
            k -= 0.005
        ln.sx, ln.k = float(sx), k
        ln.track = float(np.clip(track, -tmin * s, max_track * s))
        if ln.track != track:
            # the original is looser (or tighter) than the limits: keep the limit, centre the line
            self.solve_edges(ln, fix_track=True)
            self.centre(ln)
        else:
            self.solve_edges(ln)
        if spacing > 0 and n > 1:
            self.fit_spacing(ln, spacing * k)
        ln.rms = (self.err(ln) / self.T.size) ** 0.5
        return ln

    def fit_free(self, text, ref, left_x, track):
        """a line whose TEXT differs from the original texture's (changed on purpose, e.g. TAUSCHEN -> SCAMBIO): same size, weight,
        squeeze and baseline as `ref` (the fit of the original word), natural spacing `track`, ink left edge on `left_x`.
        Nothing is fitted to the original's ink (no justification, no optical spacing)."""
        ln = Line(text, ref.spec, size=ref.size, bold=ref.bold, sx=ref.sx, x0=self.xl, track=track, yb=ref.yb)
        ln.k = ref.k
        xl, _ = self.ext(ln)
        ln.x0 += left_x - xl
        ln.rms = 0.0
        return ln

    def fit_cond(self, text, spec, size, bold, sx_lo=0.95, sx_hi=1.05, tmin=0.03, max_track=0.04, spacing=0.0, yb=None):
        """line of a condensed face (a face designed condensed, drawn at the cap height of the original's line): the
        whole line gets the squeeze sx in [sx_lo, sx_hi] and the constant tracking (inside [-tmin, +max_track] em)
        that bring its ink edges onto those of the original; the tracking is kept as near to zero as the squeeze
        allows, the squeeze as near to 1"""
        n = len(text)
        tgt = self.xr - self.xl
        if yb is None:
            ln0 = Line(text, spec, size=size, bold=bold, x0=self.xl, yb=self.ybot - 0.5)
            self.solve_edges(ln0)
            self.fit_yb(ln0)
            yb = ln0.yb
        ln = Line(text, spec, size=size, bold=bold, x0=self.xl, yb=yb)
        xl, xr = self.ext(ln)
        w0 = xr - xl
        sx = 1.0
        track = (tgt - w0) / (n - 1)
        if track > max_track * size:
            sx = min((tgt - (n - 1) * max_track * size) / w0, sx_hi)
        elif track < -tmin * size:
            sx = max((tgt + (n - 1) * tmin * size) / w0, sx_lo)
        sx = min(max(sx, sx_lo), sx_hi)
        ln.sx = float(sx)
        ln.k = 1.0
        ln.track = float(np.clip((tgt - w0 * sx) / (n - 1), -tmin * size, max_track * size))
        self.solve_edges(ln, fix_track=False)
        if spacing > 0 and n > 1:
            self.fit_spacing(ln, spacing)
        ln.rms = (self.err(ln) / self.T.size) ** 0.5
        return ln


# ----------------------------------------------------------------------------------------------- HD style
def hd_coverage(lines, Hlo, Wlo):
    """HD (4x) fill alpha of several fitted lines"""
    out = np.zeros((Hlo * K, Wlo * K), np.float32)
    for ln in lines:
        r = ln.render(Hlo, Wlo, SS, K)
        if getattr(ln, 'clip', None) is not None:
            r[:int(round(ln.clip * K))] = 0
        np.maximum(out, r, out=out)
    return out


def shift(a, dx, dy):
    return cv2.warpAffine(a, np.float32([[1, 0, dx], [0, 1, dy]]), (a.shape[1], a.shape[0]), flags=cv2.INTER_LINEAR)


def blur(a, s):
    return a if s <= 0.05 else cv2.GaussianBlur(a, (0, 0), s)


def compose(Af, C, st):
    """Af: HD fill alpha; C: HD fill colour per pixel (H,W,3) 0..1 or per row (H,3); st: style dict.
    layers, bottom to top: black drop shadow, the fill"""
    if C.ndim == 2:
        C = np.broadcast_to(C[:, None, :], Af.shape + (3,))
    A = blur(Af, st['soft'])
    As = blur(shift(Af, st['dx'], st['dy']), st['shadow_blur']) * st['shadow']
    P = C * A[..., None]
    alpha = A + As * (1 - A)
    rgb = P / np.maximum(alpha[..., None], 1e-6)
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(alpha, 0, 1)[..., None]], 2)


def to_image(o):
    return Image.fromarray((np.clip(o, 0, 1) * 255 + 0.5).astype(np.uint8), 'RGBA')


def colour_table(lines_en, hd_en, nbins_per_em=80):
    """fill colour as a function of the height above the baseline in em, sampled inside the letters of the English HD
    image (fitted English lines). returns (t0, table): table[j] = colour at height (t0 + j) / nbins_per_em em"""
    H, W = hd_en.shape[0] // K, hd_en.shape[1] // K
    Af = hd_coverage(lines_en, H, W)
    inner = cv2.erode((Af > 0.99).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    acc = {}
    for ln in lines_en:
        for y in range(max(0, int((ln.yb - ln.size) * K)), min(H * K, int((ln.yb + 2) * K))):
            m = inner[y]
            if m.sum() >= 4:
                t = ((y + 0.5) / K - ln.yb) / ln.size
                j = int(np.floor(t * nbins_per_em))
                acc.setdefault(j, []).append(np.median(hd_en[y, m, :3], 0))
    js = sorted(acc)
    tab = np.array([np.mean(acc[j], 0) for j in js], np.float32)
    full = np.zeros((js[-1] - js[0] + 1, 3), np.float32)
    for c in range(3):
        full[:, c] = np.interp(np.arange(js[0], js[-1] + 1), js, tab[:, c])
    return js[0], full, nbins_per_em


def row_colours(lines, Hhd, table, cr):
    """per HD row fill colour for the given (Italian) lines, from the baseline-relative colour table (height in em
    of the line, so a smaller line gets the same gradient over its smaller cap height)"""
    j0, tab, nb = table
    C = np.zeros((Hhd, 3), np.float32)
    mids = np.array([getattr(ln, 'gy', ln.yb) - cr * getattr(ln, 'gsize', ln.size) / 2 for ln in lines])
    for y in range(Hhd):
        yl = (y + 0.5) / K
        ln = lines[int(np.argmin(np.abs(mids - yl)))]
        j = int(np.floor((yl - getattr(ln, 'gy', ln.yb)) / getattr(ln, 'gsize', ln.size) * nb)) - j0
        C[y] = tab[min(max(j, 0), len(tab) - 1)]
    return C


# Edge softness and black drop shadow of the English HD pack's menu words, in HD pixels. Measured by fitting this
# model on the English HD images (mainmenu_options, dueloptions, duel_result, press_start_button) against the
# English words rendered with the same fitted letters: soft = gaussian sigma of the letter edge, (dx, dy) shadow
# offset, shadow_blur its gaussian sigma, shadow its opacity.
STYLE_MENU = dict(soft=0.6, dx=3.4, dy=3.6, shadow_blur=1.05, shadow=0.46)
STYLE_PRESS = dict(soft=1.0, dx=3.9, dy=3.4, shadow_blur=1.3, shadow=0.42)

LISTS = [
    # id, Italian (file, member), English (file, member), HD reference, Italian lines, English lines,
    # English lines usable for the colours (same words in the HD image), common size / weight of the Italian
    # lines (px of the low-res texture; chosen by the `calibrate` mode: lowest alpha error of the HD texture
    # box-downscaled against the original, the squeezed lines of menu02 left out), style
    dict(id='title_menu_i__m_menu_title01', it=('title_menu/title_menu_i.ehp', 'm_menu_title01.gim'),
         en=('title_menu/title_menu_e.ehp', 'm_menu_title01.gim'), ref='ui/text/mainmenu_options.png',
         it_text=['MENU PRINCIPALE', 'INSERISCI IL NOME', 'LISTA CARTE SCARICATA', 'SFIDE DUELLO', 'OPZIONI',
                  'IMPOSTAZIONI LINGUA'],
         en_text=['MAIN MENU', 'ENTER NAME', 'DOWNLOADED CARD LIST', 'DUEL PUZZLE', 'OPTIONS', 'LANGUAGE SETTINGS'],
         en_use=[0, 1, 3, 4, 5],   # the HD image says DOWNLOAD (US text), not DOWNLOADED
         size=20.0, bold=0.2, sizes=(19.0, 20.0, 21.0), style=STYLE_MENU),
    dict(id='title_menu_i__trnsmt02', it=('title_menu/title_menu_i.ehp', 'trnsmt02.gim'),
         en=('title_menu/title_menu_e.ehp', 'trnsmt02.gim'), ref='ui/text/dueloptions.png',
         it_text=['LISTA GRUPPO', 'FORMA NUOVO GRUPPO', 'LISTA ISCRITTI', 'DUELLO', 'SCAMBIO', 'INVIA RICETTA',
                  'INVIA CARTA', 'INVIA SFIDA DUELLO', 'DUELLO LIBERO', 'DUELLO NORMALE', 'DUELLO TAG'],
         en_text=['GROUP LIST', 'MAKE NEW GROUP', 'ENTRY LIST', 'DUEL', 'CARD TRADE', 'SEND RECIPE', 'SEND CARD',
                  'SEND DUEL PUZZLE', 'FREE DUEL', 'NORMAL DUEL', 'TAG DUEL'],
         en_use=list(range(11)), size=21.0, bold=0.2, sizes=(19.0, 20.0, 21.0), style=STYLE_MENU,
         orig_text={4: 'TAUSCHEN'}),   # the original says TAUSCHEN (German); SCAMBIO on request
    dict(id='result_i__menu02', it=('duel/result/result_i.ehp', 'menu02.gim'),
         en=('duel/result/result_e.ehp', 'menu02.gim'), ref='ui/text/duel_result.png',
         it_text=['RISULTATO DEL DUELLO', 'BONUS DUELLO', 'BONUS NUOVO PUNTEGGIO MASSIMO', 'BONUS COMPLETAMENTO SFIDA',
                  'RISULTATI INTERMEDI', 'RISULTATI FINALI'],
         en_text=['DUEL RESULT', 'DUEL BONUS', 'NEW HIGH SCORE BONUS', 'CHALLENGE COMPLETE BONUS',
                  'INTERMEDIATE RESULT', 'FINAL RESULT'],
         en_use=[0, 1, 4, 5], size=19.8, bold=0.2, sizes=(19.0, 20.0, 21.0), style=STYLE_MENU,
         # lines 3 and 4 are set condensed by the game (and by the English HD sheet): Futura Condensed ExtraBold, the
         # condensed cut of the same family and stem weight, at the full cap height of the other lines
         cond=dict(lines=[2, 3], spec=FUTURA_COND_XB, bold=0.2, sx_lo=0.8, sx_hi=1.0, spacing=0.5, cap_extra=0.3)),
    dict(id='title_menu_i__press_start0003', it=('title_menu/title_menu_i.ehp', 'press_start0003.gim'),
         en=('title_menu/title_menu_e.ehp', 'press_start0003.gim'), ref='ui/text/press_start_button.png',
         it_text=['PREMI TASTO START'], en_text=['PRESS START BUTTON'], en_use=[0],
         size=13.75, bold=0.2, sizes=(13.0, 14.0), style=STYLE_PRESS),
]


LANG = os.environ.get('TF1_LANG', 'it')
LL = {'it': 'i', 'fr': 'f', 'es': 's', 'de': 'g', 'en': 'e'}[LANG]                 # language letter in the game's archive names
# menu texts in the language (those of the original game); in fr 'SCAMBIA' is an Italian leftover in the original texture: ECHANGE is written
TESTI = {
    # en: same text as the European original; the US pack has 'DOWNLOAD' (US text) and does not cover this hash
    'en': {'title_menu_i__m_menu_title01': dict(it_text=['MAIN MENU', 'ENTER NAME', 'DOWNLOADED CARD LIST', 'DUEL PUZZLE', 'OPTIONS',
                                                         'LANGUAGE SETTINGS']),
           'title_menu_i__trnsmt02': dict(it_text=['GROUP LIST', 'MAKE NEW GROUP', 'ENTRY LIST', 'DUEL', 'TRADE', 'SEND RECIPE', 'SEND CARD',
                                                   'SEND DUEL PUZZLE', 'FREE DUEL', 'NORMAL DUEL', 'TAG DUEL']),
           'result_i__menu02': dict(it_text=['DUEL RESULT', 'DUEL BONUS', 'NEW HIGH SCORE BONUS', 'CHALLENGE COMPLETE BONUS',
                                             'INTERMEDIATE RESULT', 'FINAL RESULT']),
           'title_menu_i__press_start0003': dict(it_text=['PRESS START BUTTON'])},
    'fr': {'title_menu_i__m_menu_title01': dict(it_text=['MENU PRINCIPAL', 'SAISIR NOM', 'LISTE CARTES TÉLÉCHARGÉE', 'PUZZLE DUEL',
                                                         'OPTIONS', 'SÉLECTION DE LA LANGUE']),
           'title_menu_i__trnsmt02': dict(it_text=['LISTE DE GROUPE', 'FAIRE UN NOUVEAU GROUPE', "LISTE D'ENTRÉE", 'DUEL', 'ÉCHANGE',
                                                   'ENVOYER UNE RECETTE', 'ENVOYER UNE CARTE', 'ENVOYER UN PUZZLE DUEL',
                                                   'DUEL LIBRE', 'DUEL NORMAL', 'TAG DUEL'], orig_text={4: 'SCAMBIA'}),
           'result_i__menu02': dict(it_text=['RÉSULTAT DU DUEL', 'BONUS DUEL', 'BONUS NOUVEAU MEILLEUR SCORE', 'BONUS DÉFI COMPLÉTÉ',
                                             'RÉSULTAT INTERMÉDIAIRE', 'RÉSULTAT FINAL']),
           'title_menu_i__press_start0003': dict(it_text=['APPUYEZ SUR LA TOUCHE START'])},
    'es': {'title_menu_i__m_menu_title01': dict(it_text=['MENÚ PRINCIPAL', 'INTRODUCE EL NOMBRE', 'LISTA DE CARTAS DESCARGADAS',
                                                         'DUELO ACERTIJO', 'OPCIONES', 'AJUSTES DEL IDIOMA']),
           'title_menu_i__trnsmt02': dict(it_text=['AGRUPAR LISTA', 'FORMAR GRUPO NUEVO', 'INTRODUCIR LISTA', 'DUELO', 'CAMBIAR',
                                                   'ENVIAR RECETA', 'ENVIAR CARTA', 'ENVIAR ACERTIJO DUELO',
                                                   'DUELO LIBRE', 'DUELO NORMAL', 'DUELO TAG']),
           'result_i__menu02': dict(it_text=['RESULTADO DEL DUELO', 'BONUS DUELO', 'BONUS NUEVA PUNTUACIÓN ALTA',
                                             'BONUS DESAFÍO COMPLETO', 'RESULTADO INTERMEDIO', 'RESULTADO FINAL']),
           'title_menu_i__press_start0003': dict(it_text=['PRESIONA EL BOTÓN START'])},
    # de: the original game's texts; 'ÉCHANGE' is a French leftover in the German texture -> TAUSCHEN (as tushin_msg: "Tauschen");
    # 'NEW HIGH SCORE BONUS' / 'CHALLENGE COMPLETE BONUS' stay English as in the game's German strings (New High Score Bonus)
    'de': {'title_menu_i__m_menu_title01': dict(it_text=['HAUPTMENÜ', 'NAMEN EINGEBEN', 'HERUNTERLADENE KARTENLISTE', 'DUELLRÄTSEL',
                                                         'OPTIONEN', 'SPRACHEINSTELLUNGEN']),
           'title_menu_i__trnsmt02': dict(it_text=['GRUPPENLISTE', 'NEUE GRUPPE ERSTELLEN', 'EINGANGSLISTE', 'DUELL', 'TAUSCHEN',
                                                   'REZEPT SENDEN', 'KARTEN SENDEN', 'DUELLRÄTSEL SENDEN',
                                                   'FREIES DUELL', 'NORMALES DUELL', 'TAG-DUELL'], orig_text={4: 'ÉCHANGE'}),
           'result_i__menu02': dict(it_text=['DUELLERGEBNIS', 'DUELLBONUS', 'NEW HIGH SCORE BONUS', 'CHALLENGE COMPLETE BONUS',
                                             'ZWISCHENSTAND', 'ERGEBNIS']),
           'title_menu_i__press_start0003': dict(it_text=['START-TASTE DRÜCKEN'])},
}
if LANG != 'it':
    for d in LISTS:
        ch = TESTI[LANG][d['id']]
        d.update(ch)
        d['it'] = (d['it'][0].replace('_i.ehp', f'_{LL}.ehp'), d['it'][1])
        d['id'] = d['id'].replace('_i__', f'_{LL}__')
    if LANG == 'fr':
        LISTS[2]['cond'] = dict(lines=[2], spec=FUTURA_COND_XB, bold=0.2, sx_lo=0.8, sx_hi=1.0, spacing=0.5, cap_extra=0.3)
    if LANG == 'de':     # the English lines 'NEW HIGH SCORE BONUS' / 'CHALLENGE COMPLETE BONUS' are not condensed in the German texture
        LISTS[2].pop('cond', None)
    if LANG == 'es':     # 'BONUS DESAFIO COMPLETO' is shorter than the line: the letters widen (sx_hi 1.25) instead of spreading apart
        LISTS[2]['cond'] = dict(lines=[2, 3], spec=FUTURA_COND_XB, bold=0.2, sx_lo=0.8, sx_hi=1.25, spacing=0.5, cap_extra=0.3)


def build_list(fam, d, log):
    low, h = common.texture(fam.usrdir, *d['it'])
    L = np.asarray(low)
    F = fill_estimate(L)
    cr = cap_ratio(FUTURA_BOLD)
    lines = []
    W = L.shape[1]
    fits = [Fitter(F, (0, y0, W, y1)) for y0, y1 in line_rows(L, n=len(d['it_text']))]
    cd = d.get('cond')
    lines = [None if cd and i in cd['lines'] else ft.fit_set(t, d['size'], d['bold'])
             for i, (ft, t) in enumerate(zip(fits, d['it_text']))]
    orig = d.get('orig_text', {})        # line index -> the word the ORIGINAL texture has there (the Italian text was changed on request)
    if orig:
        left_x = float(np.median([ft.xl for ft in fits]))
        track = float(np.median([ln.track for i, ln in enumerate(lines) if ln is not None and i not in orig]))
        for i, word in orig.items():
            ref = fits[i].fit_set(word, d['size'], d['bold'])
            lines[i] = fits[i].fit_free(d['it_text'][i], ref, left_x, track)
    rows_ = line_rows(L, n=len(d['it_text']))
    for i, t in enumerate(d['it_text']):        # accented capitals (French): the accent must not leave the line's box (it would end up on the line above)
        if lines[i] is not None and i not in orig and any(c in 'ÀÂÉÈÊËÎÏÔÙÛÇÁÍÓÚ' for c in t):
            cell_top = rows_[i][0] - 0.5
            for k in np.arange(0.99, 0.915, -0.01):       # 8 % at most: beyond that the accent tip is cut at the line edge
                ln = fits[i].fit_set(t, d['size'], d['bold'], k_fixed=float(k))
                cov = ln.render(L.shape[0], L.shape[1], SS, K)
                rr = np.where(cov.max(1) > 0.3)[0]
                lines[i] = ln
                if len(rr) and rr.min() >= cell_top * K:
                    break
            else:
                lines[i].clip = cell_top
    for grp in d.get('groups', []):
        # lines that do not fit at the common size share ONE reduced size (the smallest any of them needs)
        kmin = min(lines[i].k for i in grp)
        for i in grp:
            lines[i] = fits[i].fit_set(d['it_text'][i], d['size'], d['bold'], k_fixed=kmin)
    if cd:
        # the lines the game itself sets in a condensed cut: a face drawn condensed, at the cap height (and so the line
        # height) of the other lines of the texture, one face / size / weight for all of them
        capink = d['size'] * cr + 2 * d['bold']                       # ink cap height of the regular lines
        csize = (capink + cd.get('cap_extra', 0.0) - 2 * cd['bold']) / cap_ratio(cd['spec'])
        for i in cd['lines']:
            ln = fits[i].fit_cond(d['it_text'][i], cd['spec'], csize, cd['bold'], sx_lo=cd['sx_lo'], sx_hi=cd['sx_hi'],
                                  spacing=cd.get('spacing', 0.0))
            # colour gradient: same ink cap height / baseline as the regular lines
            ln.gsize = (capink - 2 * d['bold']) / cr
            ln.gy = ln.yb + cd['bold'] - d['bold']
            lines[i] = ln
    for ln in lines:
        log('  %-32s size %.2f (x%.3f) bold %.2f squeeze %.3f track %+.2f  rms %.3f' %
            (ln.text, ln.size, ln.k, ln.bold, ln.sx, ln.track, ln.rms))
    # colours of the English HD image, baseline aligned through a line level fit on the English texture
    low_en, _ = common.texture(fam.usrdir, *d['en'])
    Le = np.asarray(low_en)
    Fe = fill_estimate(Le)
    en_lines = [Fitter(Fe, (0, y0, W, y1)).fit_size_bold(t, d['sizes'])
                for (y0, y1), t in zip(line_rows(Le), d['en_text'])]
    hd_en = np.asarray(common.reference(fam.pack_us, d['ref']), np.float32) / 255
    table = colour_table([en_lines[i] for i in d['en_use']], hd_en)
    H, W = L.shape[:2]
    Af = hd_coverage(lines, H, W)
    out = compose(Af, row_colours(lines, H * K, table, cr), d['style'])
    fam.save(d['id'], to_image(out), h, low)


# ----------------------------------------------------------------------------------------------- outlined words
TIMES_BOLD = (SYS + 'Times.ttc', 1)
MARU = (SYS + 'ヒラギノ丸ゴ ProN W4.ttc', 0)
SSH = 8                     # px per low-res px of the layers composed before the final 4x area average (2 per HD px)

# Style of the English HD calendar sheet (ui/text/tournamentdates.png): white fill, opaque outline r HD px wide, black
# soft shadow shifted (dx, dy) HD px.  Fitted (least squares on alpha and premultiplied colour) on the English HD
# digits / weekdays and on "Days Until Tournament"; the fill coverage used there is the HD image's own white mask.
STYLE_GREEN = dict(r=6.05, soft=0.32, dx=0.75, dy=0.95, sb=0.5, so=0.70, outline=(0, 72, 58))
STYLE_BROWN = dict(r=6.0, soft=0.36, dx=0.84, dy=1.19, sb=0.46, so=0.56, outline=(73, 51, 0))


def outlined(cov, st, fill=(255, 255, 255)):
    """cov: fill coverage at SSH px per low-res px; returns the HD (K px per low-res px) RGBA float array: white fill,
    outline of radius st['r'] HD px (distance to the fill edge, antialiased), black drop shadow of the outlined shape"""
    f = SSH / K
    A = blur(cov, st['soft'] * f)
    dist = cv2.distanceTransform((cov <= 0.5).astype(np.uint8), cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    O = np.clip(st['r'] * f + 0.5 - dist, 0, 1)
    O = blur(np.maximum(O, A), st['soft'] * f)
    As = blur(shift(O, st['dx'] * f, st['dy'] * f), st['sb'] * f) * st['so']
    fc = np.asarray(fill, np.float32) / 255
    oc = np.asarray(st['outline'], np.float32) / 255
    P = fc * A[..., None] + (1 - A[..., None]) * oc * O[..., None]
    alpha = A + (1 - A) * (O + (1 - O) * As)
    out = np.concatenate([P, alpha[..., None]], 2)
    H, W = out.shape[0] // int(f), out.shape[1] // int(f)
    out = out[:H * int(f), :W * int(f)].reshape(H, int(f), W, int(f), 4).mean((1, 3))      # premultiplied, area average
    a = out[..., 3:]
    rgb = out[..., :3] / np.maximum(a, 1e-6)
    return np.concatenate([np.clip(rgb, 0, 1), np.clip(a, 0, 1)], 2)


def over(dst, src):
    """straight alpha 'over' of float RGBA arrays"""
    a = src[..., 3:] + dst[..., 3:] * (1 - src[..., 3:])
    rgb = (src[..., :3] * src[..., 3:] + dst[..., :3] * dst[..., 3:] * (1 - src[..., 3:])) / np.maximum(a, 1e-6)
    return np.concatenate([rgb, a], 2)


CAL_SERIF = [   # weekdays and months: (text, window x0, y0, x1, y1 of the low-res sheet)
    ('Domenica', (0, 0, 58, 16)), ('Lunedì', (58, 0, 120, 16)), ('Martedì', (120, 0, 184, 16)),
    ('Mercoledì', (184, 0, 256, 16)), ('Giovedì', (0, 16, 58, 32)), ('Venerdì', (58, 16, 120, 32)),
    ('Sabato', (120, 16, 184, 32)), ('Maggio', (0, 95, 58, 112)), ('Luglio', (0, 112, 58, 128)),
    ('Giugno', (58, 95, 120, 112)), ('Agosto', (58, 112, 120, 128))]
CAL_ROUND = [   # the cream words with brown outline
    ('Giorni', (30, 49, 110, 63)), ('al Torneo', (10, 63, 110, 77)),
    ('Mattina', (120, 95, 184, 112)), ('Pomeriggio', (120, 112, 184, 128))]
if LANG == 'fr':
    CAL_SERIF = [(t, b) for t, (_, b) in zip(['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Mai', 'Juillet',
                                                 'Juin', 'Août'], CAL_SERIF)]
    CAL_ROUND = [(t, b) for t, (_, b) in zip(['jours', 'avant le tournoi', 'Matin', 'Soir'], CAL_ROUND)]
if LANG == 'es':
    CAL_SERIF = [(t, b) for t, (_, b) in zip(['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Mayo', 'Julio',
                                                 'Junio', 'Agosto'], CAL_SERIF)]
    # AM / PM instead of Mattina / Pomeriggio; 'de' (12 de Mayo) is an extra word that Italian does not have, under 'para el torneo'
    CAL_ROUND = [('Días', (30, 49, 110, 63)), ('para el torneo', (10, 63, 110, 77)), ('AM', (120, 95, 184, 112)),
                 ('PM', (120, 112, 184, 128)), ('de', (0, 77, 30, 92))]
if LANG == 'de':
    CAL_SERIF = [(t, b) for t, (_, b) in zip(['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Mai', 'Juli',
                                                 'Juni', 'August'], CAL_SERIF)]
    # 'Tage / bis zum Turnier' and 'Vormittag / Nachmittag' as in the German original; the '.' (date: "12.") sits below, on the left
    CAL_ROUND = [('Tage', (30, 49, 110, 63)), ('bis zum Turnier', (10, 63, 110, 77)), ('Vormittag', (120, 95, 184, 112)),
                 ('Nachmittag', (120, 112, 184, 128)), ('.', (0, 80, 14, 92))]
CAL = {'it': 'ita', 'fr': 'fra', 'es': 'spa', 'de': 'ger', 'en': 'usa'}[LANG]
DIGITS = '0123456789月日ー'
SIB_SQUEEZE = 0.95        # Mattina / Pomeriggio


def digit_windows(F, y0, y1):
    """column windows of the glyphs of the digit row (gaps of 2+ empty columns separate them)"""
    cols = F[y0:y1].max(0) > 0.05
    xs = np.nonzero(cols)[0]
    out, s, p = [], xs[0], xs[0]
    for x in xs[1:]:
        if x - p > 2:
            out.append((s, p + 1))
            s = x
        p = x
    out.append((s, p + 1))
    return [(max(a - 1, 0), y0, b + 1, y1) for a, b in out]


def build_calendar(fam, log):
    low, h = common.texture(fam.usrdir, f'field/always_bri_{CAL}.ehp', 'story_sys02.gim')
    L = np.asarray(low)
    H, W = L.shape[:2]
    Fg = outline_fill_estimate(L, (0, 74, 59))
    Fb = outline_fill_estimate(L, (74, 52, 1))
    green, brown = [], []
    # --- weekdays and months: Times Bold (the font of the English HD words), one size and weight
    for text, box in CAL_SERIF:
        ln = Fitter(Fg, box).fit_set(text, 13.0, 0.0, spec=TIMES_BOLD, spacing=0)
        green.append(ln)
        log('  %-12s size %.2f (x%.3f) squeeze %.3f track %+.2f rms %.3f' % (text, ln.size, ln.k, ln.sx, ln.track, ln.rms))
    # --- digits, 月 日 ー: Hiragino Maru Gothic, centred on the original glyphs, one baseline
    wins = digit_windows(Fg, 32, 50)
    assert len(wins) == len(DIGITS), wins
    glyphs = []
    for ch, box in zip(DIGITS, wins):
        ft = Fitter(Fg, box)
        ln = Line(ch, MARU, size=13.75, bold=0.5, x0=ft.xl, yb=ft.ybot - 1.0)
        ft.centre(ln)
        glyphs.append((ft, ln))
    ybs = []
    for ft, ln in glyphs:
        ft.fit_yb(ln)
        ybs.append(ln.yb)
    yb = float(np.median(ybs))
    for ft, ln in glyphs:
        ln.yb = yb
        ft.centre(ln)
        ln.rms = (ft.err(ln) / ft.T.size) ** 0.5
        green.append(ln)
    log('  digits: baseline %.2f  rms %s' % (yb, ' '.join('%.2f' % ln.rms for _, ln in glyphs)))
    # --- Giorni al Torneo / Mattina / Pomeriggio: Maru, brown outline
    fits = [(t, Fitter(Fb, box)) for t, box in CAL_ROUND]
    lines = [ft.fit_set(t, 12.0, 0.25, spec=MARU, spacing=0) for t, ft in fits]
    # Mattina / Pomeriggio are siblings: ONE squeeze (0.95) and one size (the smallest either needs), so their letters
    # have the same width; the tracking of each is whatever its slot needs inside the limits (a looser word is centred)
    for i in (2, 3):
        lines[i] = fits[i][1].fit_set(fits[i][0], 12.0, 0.25, spec=MARU, sx_fixed=SIB_SQUEEZE, spacing=0)
    kmin = min(lines[2].k, lines[3].k)
    for i in (2, 3):
        lines[i] = fits[i][1].fit_set(fits[i][0], 12.0, 0.25, spec=MARU, k_fixed=kmin, sx_fixed=SIB_SQUEEZE, spacing=0)
    for ln in lines:
        log('  %-12s size %.2f (x%.3f) squeeze %.3f track %+.2f rms %.3f' % (ln.text, ln.size, ln.k, ln.sx, ln.track, ln.rms))
    brown.extend(lines)
    out = np.zeros((H * K, W * K, 4), np.float32)
    for lns, st in ((green, STYLE_GREEN), (brown, STYLE_BROWN)):
        can = np.zeros((H * SSH, W * SSH), np.float32)
        for ln in lns:
            np.maximum(can, ln.render(H, W, SS, SSH), out=can)
        out = over(out, outlined(can, st))
    fam.save(f'always_bri_{CAL}__story_sys02', to_image(out), h, low)


# ----------------------------------------------------------------------------------------------- icon sheet
def straighten(lab, ncls, eps):
    """vector pass on a label map: the outline of every region is simplified to a polygon (Douglas-Peucker, tolerance
    eps px of the label map), so the one-pixel stair steps of the diagonals become straight edges and the arcs
    clean polylines while true corners stay; the regions are painted back largest first (holes are kept)"""
    out = lab.copy()
    areas = np.bincount(lab.ravel(), minlength=ncls)
    for ci in np.argsort(-areas, kind='stable'):
        if areas[ci] == 0:
            continue
        m = (lab == ci).astype(np.uint8)
        cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        poly = np.zeros_like(m)
        for i, c in enumerate(cs):
            if hier[0][i][3] == -1:                                 # outer contour
                cv2.fillPoly(poly, [cv2.approxPolyDP(c, eps, True)], 1)
        for i, c in enumerate(cs):
            if hier[0][i][3] != -1:                                 # hole
                cv2.fillPoly(poly, [cv2.approxPolyDP(c, eps, True)], 0)
        out[poly > 0] = ci
    return out


def upscale_classes(L, k=K, ss=16, sigma=0.42, eps=0.3):
    """clean k-times upscale of flat-colour pixel art: every distinct colour of the low-res image is a class, its
    indicator image is upscaled with a bicubic kernel to ss px per low-res px and smoothed (gaussian, sigma low-res px:
    the one-pixel steps of the diagonals become straight lines), every output sample belongs to the class with the
    largest value (hard edges, no blur), the result is
    area-averaged down to k px per low-res px (antialiasing).  Translucent colours (the 50 % black drop shadows) are
    classes of their own."""
    L = np.asarray(L).copy()
    L[L[..., 3] == 0] = 0
    H, W = L.shape[:2]
    uniq, inv = np.unique(L.reshape(-1, 4), axis=0, return_inverse=True)
    inv = inv.reshape(H, W)
    best = np.full((H * ss, W * ss), -9.0, np.float32)
    lab = np.zeros((H * ss, W * ss), np.int32)
    for ci in range(len(uniq)):
        up = cv2.resize((inv == ci).astype(np.float32), (W * ss, H * ss), interpolation=cv2.INTER_CUBIC)
        up = cv2.GaussianBlur(up, (0, 0), sigma * ss)
        m = up > best
        best[m] = up[m]
        lab[m] = ci
    if eps > 0:
        lab = straighten(lab, len(uniq), eps * ss)
    c = uniq.astype(np.float32) / 255
    prem = np.concatenate([c[..., :3] * c[..., 3:], c[..., 3:]], 1)[lab]           # premultiplied, (H*ss, W*ss, 4)
    f = ss // k
    out = prem.reshape(H * k, f, W * k, f, 4).mean((1, 3))
    a = out[..., 3:]
    return np.concatenate([np.clip(out[..., :3] / np.maximum(a, 1e-6), 0, 1), a], 2)


def coverage_art(L, box, ss=16, k=K, eps=0.3):
    """white graphic with an antialiased edge and a translucent black drop shadow (the check mark of the result sheet),
    redrawn crisp: the white coverage of the low-res pixels (alpha x luminance) is upscaled (bicubic, light smoothing)
    and thresholded at 1/2 into ONE shape whose outline is simplified to straight edges, the shadow alpha (the black part
    of the low-res pixels, filled under the white) is upscaled as a soft translucent layer under it.  Returns the HD
    (h*k, w*k, 4) straight-alpha float array of the box."""
    x0, y0, x1, y1 = box
    sub = np.asarray(L[y0:y1, x0:x1], np.float32)
    a = sub[..., 3] / 255
    lum = sub[..., :3] @ np.array([.299, .587, .114], np.float32) / 255
    cw = a * lum                                                          # white coverage
    cs = np.where(cw < 0.999, (a - cw) / np.maximum(1 - cw, 1e-3), 0).clip(0, 1)      # shadow alpha
    valid = cw < 0.99
    s0 = np.where(valid, cs, 0).astype(np.float32)
    sh = np.where(valid, s0, cv2.dilate(s0, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))))
    h, w = a.shape
    up = cv2.GaussianBlur(cv2.resize(cw, (w * ss, h * ss), interpolation=cv2.INTER_CUBIC), (0, 0), 0.3 * ss)
    mask = (up > 0.5).astype(np.uint8)
    cs_, hier = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    mask = np.zeros_like(mask)
    for i, c in enumerate(cs_):
        cv2.fillPoly(mask, [cv2.approxPolyDP(c, eps * ss, True)], 1 if hier[0][i][3] == -1 else 0)
    mask = mask.astype(np.float32)
    shadow = np.clip(cv2.GaussianBlur(cv2.resize(sh, (w * ss, h * ss), interpolation=cv2.INTER_CUBIC), (0, 0), 0.25 * ss), 0, 1)
    alpha = mask + (1 - mask) * shadow                                    # white over the black shadow
    prem = np.concatenate([mask[..., None].repeat(3, 2), alpha[..., None]], 2)
    f = ss // k
    pm = prem.reshape(h * k, f, w * k, f, 4).mean((1, 3))
    return np.concatenate([np.clip(pm[..., :3] / np.maximum(pm[..., 3:], 1e-6), 0, 1), pm[..., 3:]], 2)


CHECK_BOX = (144, 0, 170, 23)       # the white check mark of the result sheet


LABELS = [   # result sheet labels: text, window (x0, y0, x1, y1) of the low-res sheet, fill colour of the low-res word
    ('VITTORIA', (0, 47, 54, 64), (255, 245, 1)),
    ('PAREGGIO', (54, 47, 109, 64), (210, 0, 99)),
    ('SCONFITT', (109, 47, 162, 64), (52, 81, 255)),
]
if LANG == 'en':
    LABELS[:] = [('WIN', (0, 47, 54, 64), (255, 245, 1)), ('DRAW', (54, 47, 109, 64), (210, 0, 99)), ('LOSE', (109, 47, 162, 64), (52, 81, 255))]
if LANG == 'fr':
    LABELS[:] = [('GAGNÉ', (0, 47, 54, 64), (255, 245, 1)), ('ÉGALITÉ', (54, 47, 109, 64), (210, 0, 99)),
                 ('PERDU', (109, 47, 162, 64), (52, 81, 255))]
if LANG == 'es':
    LABELS[:] = [('GANAS', (0, 47, 54, 64), (255, 245, 1)), ('EMPATE', (54, 47, 109, 64), (210, 0, 99)),
                 ('PIERDES', (109, 47, 162, 64), (52, 81, 255))]
if LANG == 'de':
    LABELS[:] = [('GEWONNEN', (0, 47, 54, 64), (255, 245, 1)), ('UNENTSCHIEDEN', (54, 47, 107, 64), (210, 0, 99)),
                 ('VERLOREN', (109, 47, 162, 64), (52, 81, 255))]
LABEL_SPEC, LABEL_SX = (FUTURA_COND_XB, (0.9, 0.9)) if LANG == 'it' else (FUTURA_COND_XB, (0.6, 1.0)) if LANG == 'de' else (FUTURA_BOLD, (0.95, 1.25))   # the French words (5-7 letters) are not condensed
LABEL_CAP, LABEL_BOLD = (8.9 if LANG == 'de' else 10.9), 0.1       # de: the three words are 9 rows tall (it/fr/es 11)
LABEL_CAP_UNUSED = None        # ink cap height (low-res rows) and weight (px of emboldening) of the labels
STYLE_LABEL = dict(soft=0.6, dx=4.0, dy=4.0, shadow_blur=0.9, shadow=0.5)       # the sheet's own 1 px, 50 % black shadow


def build_icons(fam, log):
    low, h = common.texture(fam.usrdir, f'duel/result/result_{LL}.ehp', 'menu01.gim')
    L = np.asarray(low)
    H, W = L.shape[:2]
    clean = L.copy()
    clean[47:, :162] = 0                                  # the three words (they are redrawn below)
    x0, y0, x1, y1 = CHECK_BOX
    box = L[y0:y1, x0:x1].astype(int)
    assert (np.ptp(box[..., :3], axis=2)[box[..., 3] > 0] < 100).all()     # only white / black (grey) pixels in the box
    clean[y0:y1, x0:x1] = 0                               # the check mark (redrawn below as coverage art)
    out = upscale_classes(clean)
    out[y0 * K:y1 * K, x0 * K:x1 * K] = coverage_art(L, CHECK_BOX)
    # --- the labels: the sheet sets VITTORIA / PAREGGIO / SCONFITT condensed, at 11.3 rows of cap height and about 52 px
    # wide for 8 letters; Futura Condensed ExtraBold (the condensed cut of Futura Bold) at that cap height, ONE squeeze
    # for the three words, one baseline, flat colour, the sheet's own drop shadow
    cap_ink, bold = LABEL_CAP, LABEL_BOLD
    size = (cap_ink - 2 * bold) / cap_ratio(LABEL_SPEC)
    fits = []
    for text, box, rgb in LABELS:
        F = colour_fill_estimate(L, rgb)
        fits.append((text, Fitter(F, box), rgb))
    ybs = []
    for t, ft, _ in fits:
        ln0 = Line(t, LABEL_SPEC, size=size, bold=bold, x0=ft.xl, yb=ft.ybot - 0.5)
        ft.solve_edges(ln0)
        ft.fit_yb(ln0)
        ybs.append(ln0.yb)
    yb = float(np.median(ybs))                                  # one baseline for the three words
    lines = [ft.fit_cond(t, LABEL_SPEC, size, bold, sx_lo=LABEL_SX[0], sx_hi=LABEL_SX[1], tmin=0.045, spacing=0.5, yb=yb)
             for t, ft, _ in fits]
    for ln in lines:
        log('  %-10s size %.2f squeeze %.3f track %+.2f rms %.3f' % (ln.text, ln.size, ln.sx, ln.track, ln.rms))
    for ln, (_, _, rgb) in zip(lines, fits):
        Af = ln.render(H, W, SS, K)
        C = np.broadcast_to(np.asarray(rgb, np.float32) / 255, Af.shape + (3,))
        out = over(out, compose(Af, C, STYLE_LABEL))
    fam.save(f'result_{LL}__menu01', to_image(out), h, low)


def calibrate(argv):
    """python3 -I menu_lists.py USRDIR PACK_US OUT calibrate <list index> <sizes> <weights> [lines to skip]
    prints the alpha / colour error (HD box-downscaled against the original) of one list texture for a grid of common
    sizes and weights, e.g.  calibrate 0 19.8,20,20.2 0.1,0.2,0.3 ; this is how the `size` / `bold` constants of LISTS
    were chosen (lowest error, lines that the family squeezes excluded)."""
    idx = int(argv[5])
    sizes = [float(v) for v in argv[6].split(',')]
    bolds = [float(v) for v in argv[7].split(',')]
    skip = [int(v) for v in argv[8].split(',')] if len(argv) > 8 and argv[8] else []

    class Probe:
        usrdir, pack_us = argv[1], argv[2]

        def save(self, tex_id, hd, h, low):
            lo = np.asarray(low.convert('RGBA'), np.float32)
            sm = np.asarray(hd.convert('RGBA').resize((lo.shape[1], lo.shape[0]), Image.BOX), np.float32)
            keep = np.ones(lo.shape[0], bool)
            segs = line_rows(np.asarray(low))
            for i in skip:
                keep[segs[i][0]:segs[i][1]] = False
            vis = (lo[..., 3] > 128) & keep[:, None]
            self.res = (np.abs(sm[..., 3] - lo[..., 3])[keep].mean(), np.abs(sm[..., :3] - lo[..., :3])[vis].mean())
    for size in sizes:
        for bold in bolds:
            d = dict(LISTS[idx], size=size, bold=bold)
            pr = Probe()
            build_list(pr, d, lambda *a: None)
            print('%s size %.2f bold %.2f  alpha MAE %.1f  colour MAE %.1f' % ((d['id'], size, bold) + pr.res), flush=True)


def main(argv):
    if len(argv) > 5 and argv[4] == 'calibrate':
        return calibrate(argv)
    fam = common.Family('menu_liste', argv)
    only = set(argv[4:])
    for d in LISTS:
        if not only or d['id'] in only:
            print(d['id'], flush=True)
            build_list(fam, d, print)
    if not only or f'result_{LL}__menu01' in only:
        print(f'result_{LL}__menu01', flush=True)
        build_icons(fam, print)
    if not only or f'always_bri_{CAL}__story_sys02' in only:
        print(f'always_bri_{CAL}__story_sys02', flush=True)
        build_calendar(fam, print)
    fam.finish()


if __name__ == '__main__':
    main(sys.argv)
