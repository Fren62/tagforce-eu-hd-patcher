"""result_letters: big letter tiles of the end-of-duel banners, HD Italian (4x).

  HAI VINTO  (win, yellow)       duel_win1000{02..14}  H A I V N T O   (one I tile, drawn twice by the game)
                                 duel_win100016        64x32 blurred "HAI VINTO" silhouette (glow behind the banner)
  HAI PERSO  (lose, violet/cyan) duel_lose1000{02..16} H A I P E R S O
  PAREGGIO   (draw, red/pink)    duel_draw1000{02..14} P A R E G I O   (one G tile, drawn twice by the game)

Style = the English HD pack (MikeyMK, ui/text/win|lose/*.png, the letters of YOU WIN / YOU LOSE): Times Bold glyph
filled with a vertical gradient, ~11.7 px purple outline with a soft edge, soft drop shadow toward the lower right.
The pack's own letters are clean art, but they cannot be pasted: they sit 10-50 HD px away from the Italian
positions (alpha MAE 16-35 against the Italian tiles), the draw family is red and the win/lose gradients differ.
So every tile is RENDERED with one style model (fitted on the twelve English HD letters; it reproduces them within
~1.5 alpha levels per pixel, see the validation in the QA sheets) from a letter SHAPE:
  - I N O S: the fill contour of the English HD letter itself (real mod art; for O and S the mod's glyph differs
    from Times Bold and the Italian low-res tiles follow the mod's glyph: fit error 0.0005-0.0008 against
    0.004-0.006 with Times Bold),
  - H A V T E P R G: Times Bold (macOS /System/Library/Fonts/Times.ttc), the font of the English HD letters (best of
    all system fonts by measured overlap with the English letters; the Italian low-res tiles agree).
The Italian low-res tiles share one geometry that the script MEASURES (calibrate) instead of fitting letter by letter:
  - the same cap line / baseline in all 22 letter tiles (fill rows 11.27 .. 46.73 of 64), so ONE cap height for every
    letter (the scale of each shape source is derived from it, no per-letter scaling),
  - one stroke weight: the Italian glyphs are ~0.4 low-res px (1.6 HD px per side) bolder than the English ones,
  - one horizontal scale per word: HAI PERSO is squeezed to 0.96 (the original squeezed the 8 letters of that
    banner), HAI VINTO / PAREGGIO are not,
  - per tile only the horizontal position (the letters are centred by their ink).
Letters are built with an exact signed distance field (8x supersampling), so edges are smooth and constant-width.
Fill gradients are measured row by row on the Italian low-res tiles (one gradient per family), the outline colour
profile on the English HD letters.
The silhouette tile is a blur: the English pack leaves its own untouched at 64x32; here the Italian original is
resampled x4 (cubic) and lightly smoothed to hide its 16-level quantisation.
Run:  python3 -I result_letters.py USRDIR PACK_US OUT
"""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import alt_font  # noqa: nessun font Apple
import os, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

cv2.setNumThreads(1)                                       # bit-identical results from run to run

NAME = 'lettere_esito'
LANG = os.environ.get('TF1_LANG', 'it')
B = {'it': 'ii', 'fr': 'ff', 'es': 'ss', 'de': 'gg', 'en': 'be'}[LANG]
ARCH = f'duel/basic_{B}.ehp'
FONT = ('/System/Library/Fonts/Times.ttc', 1)              # Times Bold: best match of the English HD letters
T = 256                                                    # HD tile size (64x64 x4)
LETTERS = {'it': {'win': 'HAIVNTO', 'lose': 'HAIPERSO', 'draw': 'PAREGIO'},
           'fr': {'win': 'TUASGNÉ', 'lose': 'TUASPERD', 'draw': 'EGALIT'},
           'es': {'win': 'HASGNDO', 'lose': 'HASPERDIO', 'draw': 'EMPAT'},
           'de': {'win': 'DUGEWINST', 'lose': 'DUVERLIST', 'draw': 'UNETSCHID'},
           'en': {'win': '', 'lose': '', 'draw': 'DRAW'}}[LANG]      # en: win/lose are already in the US pack, only DRAW is missing      # one tile per letter, as the game composes them
# shape source of the Italian letters that exist in the English HD set (rel path in the pack, flat-bottomed
# reference letter of the same English tile family: win -> i, lose -> l); every other letter is Times Bold
WIN_I = ('ui/text/win/i.png', 'ui/text/win/i.png')
EN_SRC = {
    'win':  {'I': WIN_I, 'N': ('ui/text/win/n.png', 'ui/text/win/i.png'), 'O': ('ui/text/win/o.png', 'ui/text/win/i.png'),
             'S': ('ui/text/lose/s.png', 'ui/text/win/i.png')},
    'lose': {'I': WIN_I, 'S': ('ui/text/lose/s.png', 'ui/text/lose/l.png'), 'O': ('ui/text/lose/o.png', 'ui/text/lose/l.png')},
    'draw': {'I': WIN_I, 'O': ('ui/text/lose/o.png', 'ui/text/lose/l.png')},
}
EN_ALT = {'E': ('ui/text/lose/e.png', 'ui/text/lose/l.png')}      # English E: measured, not used (Times Bold fits better)
USE_EN_E = False
# --- Italian low-res geometry (rows of the 64x64 tile, measured on the fill coverage of all 22 tiles) ---
FILL_TOP, FILL_BOT = 11.27, 46.73                          # flat letters; round ones overshoot by 0.74 each side
LOSE_SQUEEZE0 = 0.96                                       # starting values of the calibration
# --- style constants, fitted (least squares) on the 12 English HD letters, HD pixels ---
# body (fill + outline) alpha = GaussianBlur(clip(R_OUT - sd + .5), SIG_OUT), sd = signed distance to the glyph edge
R_OUT, SIG_OUT = 11.675, 1.722
# shadow = SH_OP * GaussianBlur(shift(clip(SH_R - sd + .5), SH_DX, SH_DY), SH_SIG), black, under the body
SH_R, SH_DX, SH_DY, SH_SIG, SH_OP = 3.438, 12.505, 16.651, 6.312, 0.726
OUTLINE_LOW = np.array([123, 0, 106], np.float32)          # outline colour of the low-res tiles (all three families)
SSC, SSX = 2, 8                                            # supersampling: calibration / final render


# ---------------------------------------------------------------- low-res measurements
def low_gradient(lows):
    """per low-res row fill colour (median of the interior fill pixels of all the tiles of a family)."""
    rows = {}
    for low in lows:
        a = np.asarray(low, np.float32)
        body = a[..., 3] == 255
        fill = body & (np.abs(a[..., :3] - OUTLINE_LOW).sum(-1) > 6)
        inner = cv2.erode(fill.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
        for y in range(a.shape[0]):
            if inner[y].any():
                rows.setdefault(y, []).append(a[y][inner[y]][:, :3])
    ys = np.array(sorted(rows), np.float32)
    vals = np.array([np.median(np.concatenate(rows[int(y)]), 0) for y in ys], np.float32)
    return ys, vals


def hd_gradient(ys, vals):
    """HD per-row colours (T,3): linear interpolation between the low-res row centres, clamped at the ends."""
    u = (np.arange(T) + 0.5) / common.SCALE - 0.5
    g = np.stack([np.interp(u, ys, vals[:, c]) for c in range(3)], 1)
    k = np.exp(-0.5 * (np.arange(-3, 4) / 1.0) ** 2)
    k /= k.sum()
    return np.stack([np.convolve(np.pad(g[:, c], 3, mode='edge'), k, 'valid') for c in range(3)], 1).astype(np.float32)


def low_fill(low, grad_rows):
    """fill coverage of a low-res tile: position of each opaque pixel between the outline colour and the row gradient.
    Only the fill/outline mix counts: translucent pixels (outer edge, shadow) and pixels far from that colour line
    (the black shadow projects onto the yellow gradient) are not fill."""
    a = np.asarray(low, np.float32)
    ys, vals = grad_rows
    g = np.stack([np.interp(np.arange(a.shape[0]), ys, vals[:, c]) for c in range(3)], 1)[:, None, :]
    d = g - OUTLINE_LOW
    f = np.clip(((a[..., :3] - OUTLINE_LOW) * d).sum(-1) / np.maximum((d * d).sum(-1), 1), 0, 1)
    resid = np.sqrt(((a[..., :3] - (OUTLINE_LOW + f[..., None] * d)) ** 2).sum(-1))
    f = np.where((resid > 45) | (a[..., 3] < 250), 0, f)
    return f.astype(np.float32)


# ---------------------------------------------------------------- English HD letters (style source)
def en_fill(a, win):
    """fill coverage and per-row fill colour of an English HD letter (win: yellow fill, lose: violet/cyan fill;
    purple outline with G = 0 and B ~ 112)."""
    hdc = np.asarray(a, np.float32)
    ch, lo = (1, 0.0) if win else (2, 112.0)
    core = ((hdc[..., 1] > 100) if win else (hdc[..., 2] > 170)) & (hdc[..., 3] > 250)
    inner = cv2.erode(core.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
    g = np.zeros((T, 3), np.float32)
    ok = np.zeros(T, bool)
    for y in range(T):
        if inner[y].any():
            g[y] = np.median(hdc[y, :, :3][inner[y]], 0)
            ok[y] = True
    yy = np.where(ok)[0]
    g = np.stack([np.interp(np.arange(T), yy, g[yy, c]) for c in range(3)], 1)
    f = np.clip((hdc[..., ch] - lo) / np.maximum(g[:, None, ch] - lo, 1), 0, 1) * (hdc[..., 3] > 200)
    return f.astype(np.float32), g


def sdf_px(mask):
    """signed distance (pixels, negative inside) to the edge of a binary mask."""
    m = mask.astype(np.uint8)
    din = cv2.distanceTransform(m, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    dout = cv2.distanceTransform(1 - m, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    return np.where(m > 0, -(din - 0.5), dout - 0.5).astype(np.float32)


def sdf_from_hd_cov(f, ss=4):
    """signed distance in HD px of an HD coverage map (computed at ss x, area-reduced)."""
    big = cv2.resize(f, None, fx=ss, fy=ss, interpolation=cv2.INTER_CUBIC)
    return cv2.resize(sdf_px(big > 0.5) / ss, (f.shape[1], f.shape[0]), interpolation=cv2.INTER_AREA)


def outline_lut(pack_us, files):
    """outline colour as a function of the distance from the fill edge, measured on English HD letters
    (body colour with the black shadow removed, fill contribution removed)."""
    bins = np.arange(0.0, 16.01, 0.25)
    num = np.zeros((len(bins), 3))
    den = np.zeros(len(bins))
    edge = np.zeros((len(bins), 3))
    eden = np.zeros(len(bins))
    for rel in files:
        a = np.asarray(common.reference(pack_us, rel), np.float32)
        f, g = en_fill(a, '/win/' in rel)
        s = sdf_from_hd_cov(f)
        ab, _ = body_alpha(s)
        m = (ab > 0.6) & (a[..., 3] > 200) & (f < 0.95) & (s > -0.5)
        cb = a[..., :3] * (a[..., 3:] / 255.0) / np.maximum(ab[..., None], 1e-3)
        x = (cb - f[..., None] * g[:, None, :]) / np.maximum(1 - f[..., None], 0.05)
        w = (1 - f) ** 2
        idx = np.clip(np.round(s / 0.25).astype(int), 0, len(bins) - 1)
        gy, gx = np.gradient(s)
        ul = (gx + gy < -0.5) & (a[..., 3] > 2)       # upper-left side of the outline: no shadow under it
        for i in range(len(bins)):
            mm = m & (idx == i)
            num[i] += (x[mm] * w[mm][:, None]).sum(0)
            den[i] += w[mm].sum()
            me = ul & (idx == i)
            edge[i] += a[..., :3][me].sum(0)
            eden[i] += me.sum()
    lut = np.clip(num / np.maximum(den, 1e-6)[:, None], 0, 255)
    # outer soft edge (sd >= 8): the colour stored by the English letters there (it darkens towards the rim)
    outer = bins >= 8
    lut[outer] = edge[outer] / np.maximum(eden[outer], 1)[:, None]
    k = np.array([1, 2, 3, 2, 1], np.float32)
    k /= k.sum()
    lut = np.stack([np.convolve(np.pad(lut[:, c], 2, mode='edge'), k, 'valid') for c in range(3)], 1)
    return bins, lut.astype(np.float32)


def lut_eval(lut, s):
    bins, v = lut
    return np.stack([np.interp(s, bins, v[:, c]) for c in range(3)], -1).astype(np.float32)


# ---------------------------------------------------------------- style model
def body_alpha(s):
    ab = cv2.GaussianBlur(np.clip(R_OUT - s + 0.5, 0, 1).astype(np.float32), (0, 0), SIG_OUT)
    src = np.clip(SH_R - s + 0.5, 0, 1).astype(np.float32)
    sh = cv2.warpAffine(src, np.float32([[1, 0, SH_DX], [0, 1, SH_DY]]), (s.shape[1], s.shape[0]))
    sh = cv2.GaussianBlur(sh, (0, 0), SH_SIG) * SH_OP
    return ab, ab + sh * (1 - ab)


def render(f, s, grad, lut):
    """HD letter tile from fill coverage f and signed distance s (HD px)."""
    ab, a = body_alpha(s)
    x = lut_eval(lut, np.clip(s, 0, 16))
    cb = f[..., None] * grad[:, None, :] + (1 - f[..., None]) * x
    c = cb * (ab / np.maximum(a, 1e-4))[..., None]
    out = np.dstack([np.clip(c, 0, 255), np.clip(a * 255, 0, 255)])
    return Image.fromarray(np.round(out).astype(np.uint8), 'RGBA')


# ---------------------------------------------------------------- letter shapes (rasters at pitch 1/ss HD px)
_cap = {}


def cap_ratio():
    """cap height / em of Times Bold, measured on H"""
    if 'r' not in _cap:
        ft = ImageFont.truetype(FONT[0], 1000, index=FONT[1])
        l, t, r, b = ft.getbbox('H', anchor='ls')
        _cap['r'] = (b - t) / 1000.0
    return _cap['r']


def glyph_raster(ch, ss, cap_hd=141.0):
    """Times Bold glyph coverage, pitch 1/ss HD px, nominal cap height cap_hd HD px.
    returns (raster, ax, base, cap): ax = x of the ink centre, base = baseline row (pixel-edge coordinates, raster px),
    cap = measured cap height of the font at this size (HD px)."""
    size = cap_hd * ss / cap_ratio()
    ft = ImageFont.truetype(FONT[0], size, index=FONT[1])
    l, t, r, b = ft.getbbox(ch, anchor='ls')
    m = 8 * ss
    im = Image.new('L', (int(np.ceil(r - l)) + 2 * m, int(np.ceil(b - t)) + 2 * m), 0)
    ox, oy = m - l, m - t
    ImageDraw.Draw(im).text((ox, oy), ch, font=ft, fill=255, anchor='ls')
    R = np.asarray(im, np.float32) / 255
    ys, xs = np.where(R > 0.5)
    ax = (xs.min() + xs.max() + 1) / 2.0
    return R, ax, float(oy), cap_of_font(ss, cap_hd)


def cap_of_font(ss, cap_hd=141.0):
    if (ss, cap_hd) in _cap:
        return _cap[(ss, cap_hd)]
    size = cap_hd * ss / cap_ratio()
    ft = ImageFont.truetype(FONT[0], size, index=FONT[1])
    l, t, r, b = ft.getbbox('H', anchor='ls')
    im = Image.new('L', (int(np.ceil(r - l)) + 8, int(np.ceil(b - t)) + 8), 0)
    ImageDraw.Draw(im).text((4 - l, 4 - t), 'H', font=ft, fill=255, anchor='ls')
    ys, xs = np.where(np.asarray(im) > 127)
    _cap[(ss, cap_hd)] = (ys.max() + 1 - ys.min()) / ss
    return _cap[(ss, cap_hd)]


def row_edge(f, bottom=True):
    """sub-pixel position (HD px, pixel-edge coordinate) of the flat bottom / top of a coverage map"""
    rows = f.max(1)
    inside = np.where(rows > 0.5)[0]
    if bottom:
        y = inside[-1] + 1
        return y + (rows[y] if y < len(rows) else 0.0)
    y = inside[0]
    return y - (rows[y - 1] if y > 0 else 0.0)


def en_raster(pack, src, ss):
    """fill contour of an English HD letter, cubic-upsampled to pitch 1/ss HD px.
    returns (raster, ax, base, cap): base = flat baseline and cap = flat cap height of the English tile family,
    measured on the flat-bottomed reference letter src[1] (i for win, l for lose)."""
    rel, ref = src
    a = np.asarray(common.reference(pack, rel), np.float32)
    f, _ = en_fill(a, '/win/' in rel)
    R = np.clip(cv2.resize(f, None, fx=ss, fy=ss, interpolation=cv2.INTER_CUBIC), 0, 1)
    ys, xs = np.where(R > 0.5)
    ax = (xs.min() + xs.max() + 1) / 2.0
    fr, _ = en_fill(np.asarray(common.reference(pack, ref), np.float32), '/win/' in ref)
    base, top = row_edge(fr, True), row_edge(fr, False)
    return R, ax, float(base * ss), float(base - top)


def place(R, ax, base, sx, sy, xc, yb, ss, n):
    """warp the raster so that (ax, base) lands at (xc, yb) HD px of an n x n canvas (pitch 1/ss), scale (sx, sy)."""
    M = np.float32([[sx, 0, sx * (0.5 - ax) + xc * ss - 0.5],
                    [0, sy, sy * (0.5 - base) + yb * ss - 0.5]])
    W = cv2.warpAffine(R, M, (n, n), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return W > 0.5


def sdf_canvas(mask, ss):
    """signed distance (HD px, negative inside) of a binary canvas mask"""
    return sdf_px(mask) / ss


def coverage(sd, w, ss):
    """fill coverage (continuous AA ramp at canvas pitch) of the shape offset by w HD px (w > 0: bolder)"""
    return np.clip(0.5 - (sd - w) * ss, 0, 1).astype(np.float32)


# ---------------------------------------------------------------- calibration (geometry shared by all tiles)
def accent_down(shape, flow, ss, w=1.5):
    """lowers the accent (detached component above the letter) until its top coincides with that of the low-resolution fill"""
    R, ax, base, cap = shape
    n, lab, st, _ = cv2.connectedComponentsWithStats((R > 0.5).astype(np.uint8), connectivity=8)
    acc = min(range(1, n), key=lambda i: st[i, 1])
    top_now = st[acc, 1]
    want = base - ((FILL_BOT - np.where(flow > 0.5)[0].min()) * common.SCALE - 2 * w) * ss
    d = int(round(top_now - want)) * -1                      # > 0 = downwards
    R2 = R.copy()
    m = lab == acc
    R2[m] = 0
    ys, xs = np.where(m)
    ys2 = np.clip(ys + d, 0, R.shape[0] - 1)
    R2[ys2, xs] = np.maximum(R2[ys2, xs], R[ys, xs])
    return R2, ax, base, cap


class Letter:
    def __init__(self, kind, ch, member, low, h, flow, src):
        self.kind, self.ch, self.member, self.low, self.h, self.flow, self.src = kind, ch, member, low, h, flow, src
        ys, xs = np.where(flow > 0.5)
        self.cx = (xs.min() + xs.max() + 1) / 2.0 * common.SCALE       # HD px, centre of the low-res fill
        self.shape = {}

    def get_shape(self, pack, ss):
        if ss not in self.shape:
            if self.src:
                self.shape[ss] = en_raster(pack, self.src, ss)
            else:
                self.shape[ss] = glyph_raster(self.ch, ss)
                if self.ch == 'É':        # Times' accent is higher than the game's: I lower it to the top of the original tile
                    self.shape[ss] = accent_down(self.shape[ss], self.flow, ss)
        return self.shape[ss]


def letter_params(let, pack, ss, P):
    """(scale sx, sy, weight w) of a letter: one cap height for all shapes; the word squeeze only for HAI PERSO"""
    R, ax, base, cap = let.get_shape(pack, ss)
    cap_low = (FILL_BOT - FILL_TOP) * common.SCALE                       # flat cap height of the Italian fill (HD px)
    sy = (cap_low - 2 * P['w']) / cap
    sx = P['sx'] * (P['squeeze'] if let.kind == 'lose' else P.get('wide', 1.0) if let.kind == 'draw' else 1.0)
    return sx, sy


def make_canvas(let, pack, ss, P, n):
    R, ax, base, cap = let.get_shape(pack, ss)
    sx, sy = letter_params(let, pack, ss, P)
    yb = FILL_BOT * common.SCALE - P['w']                                # baseline of the shape (the weight adds below)
    mask = place(R, ax, base, sx, sy, T / 2.0, yb, ss, n)
    sd = sdf_canvas(mask, ss)
    return sd, coverage(sd, P['w'], ss)


def x_search(c, flow, k0, steps):
    """integer canvas shift of coverage c that best matches the low-res fill coverage (area-reduced to 64x64)"""
    def err(k):
        return float(((cv2.resize(np.roll(c, int(k), axis=1), (64, 64), interpolation=cv2.INTER_AREA) - flow) ** 2).mean())
    k, e = int(k0), err(k0)
    for step in steps:
        while True:
            moved = False
            for s in (-step, step):
                e2 = err(k + s)
                if e2 < e:
                    k, e, moved = k + s, e2, True
            if not moved:
                break
    return k, e


def fit_error(let, pack, P):
    sd, c = make_canvas(let, pack, SSC, P, T * SSC)
    k, e = x_search(c, let.flow, int(round((let.cx - T / 2.0) * SSC)), (8, 4, 2, 1))
    return e, k / float(SSC)


def calibrate(letters, pack):
    """shared geometry: horizontal scale of the shapes, stroke weight (HD px per side) and the HAI PERSO squeeze,
    by coordinate descent on the mean squared error between the area-reduced model fill and the Italian low-res fill
    (each letter only free in x position)."""
    def total(v):
        P = dict(sx=v[0], w=v[1], squeeze=v[2])
        if len(v) > 3:
            P['wide'] = v[3]            # French: the EGALIT tiles are wider than those of the other words
        return sum(fit_error(l, pack, P)[0] for l in letters) / len(letters)
    p, steps, mins = [1.0, 1.5, LOSE_SQUEEZE0], [0.01, 0.4, 0.01], [0.0005, 0.05, 0.0005]
    if LANG in ('fr', 'es', 'de'):
        p, steps, mins = p + [1.2], steps + [0.05], mins + [0.0005]
    cur = total(p)
    while max(s / m for s, m in zip(steps, mins)) > 1:
        better = False
        for i in range(len(p)):
            for sg in (-1, 1):
                q = list(p)
                q[i] += sg * steps[i]
                e = total(q)
                if e < cur:
                    cur, p, better = e, q, True
        if not better:
            steps = [s / 2 for s in steps]
    return dict(sx=p[0], w=p[1], squeeze=p[2], **({'wide': p[3]} if len(p) > 3 else {})), cur


# ---------------------------------------------------------------- builders
def build_letter(let, pack, P, grad, lut):
    """HD tile of a letter at the final supersampling; returns (image, info)"""
    n = T * SSX
    sd, c = make_canvas(let, pack, SSX, P, n)
    k0 = int(round(fit_error(let, pack, P)[1] * SSX))
    k, e = x_search(c, let.flow, k0, (4, 2, 1))
    c, sd = np.roll(c, k, axis=1), np.roll(sd, k, axis=1) - P['w']      # distance to the edge of the (bolder) fill
    f = cv2.resize(c, (T, T), interpolation=cv2.INTER_AREA)
    s = cv2.resize(sd, (T, T), interpolation=cv2.INTER_AREA)
    sx, sy = letter_params(let, pack, SSX, P)
    return render(f, s, grad, lut), (('English HD shape ' + let.src[0]) if let.src else 'Times Bold', sx, sy, k / float(SSX), e)


def silhouette(low):
    """64x32 blurred cream "HAI VINTO" silhouette (glow behind the banner).  The English pack keeps its YOU WIN
    silhouette at the original resolution (ui/duels/you_win_silhouette.png is the untouched 64x32 texture): the
    content is a blur, so the HD version is the Italian original resampled x4 (cubic) and lightly smoothed to
    hide its 16-level quantisation; colour follows alpha exactly as in the original 16-colour palette.
    Why not rebuild it from the HD letters: the glow must keep the extent of the original (rule 1) and the banner layout
    that would place those letters is not part of this tile.  Why sigma 1.0 HD px: measured alpha MAE against the
    original is 2.0 (no smoothing), 2.9 (sigma 1), 5.4 (sigma 2), 8.8 (sigma 3): sigma 1 is the largest smoothing inside
    the alpha target (<= ~4) and it already removes the stair-stepping of the 4x nearest upscale."""
    la = np.asarray(low, np.float32)
    pal = {}
    for px in la.reshape(-1, 4):
        if px[3] > 0:
            pal[float(px[3])] = px[:3]
    pa = np.array(sorted(pal)) / 255.0
    pc = np.array([pal[k] for k in sorted(pal)])
    m = 2
    al = np.pad(la[..., 3] / 255.0, m)
    up = cv2.resize(al, None, fx=common.SCALE, fy=common.SCALE, interpolation=cv2.INTER_CUBIC)
    up = up[m * common.SCALE:-m * common.SCALE, m * common.SCALE:-m * common.SCALE]
    up = np.clip(cv2.GaussianBlur(up, (0, 0), 1.0), 0, 1)
    rgb = np.stack([np.interp(up, pa, pc[:, c]) for c in range(3)], -1)
    out = np.dstack([rgb, up * 255])
    return Image.fromarray(np.round(np.clip(out, 0, 255)).astype(np.uint8), 'RGBA')


# ---------------------------------------------------------------- main
def main(argv):
    fam = common.Family(NAME, argv)
    usr, pack = fam.usrdir, fam.pack_us
    luts = {'win': outline_lut(pack, ['ui/text/win/' + c + '.png' for c in 'younwi']),
            'lose': outline_lut(pack, ['ui/text/lose/' + c + '.png' for c in 'youlse'])}
    luts['draw'] = luts['lose']
    letters, grads = [], {}
    for kind, chars in LETTERS.items():
        if not chars:
            continue
        tiles = []
        for i, ch in enumerate(chars):
            member = 'duel_%s1000%02d.gim' % (kind, 2 * i + 2)
            low, h = common.texture(usr, ARCH, member)
            tiles.append((member, ch, low.convert('RGBA'), h))
        grad_rows = low_gradient([t[2] for t in tiles])
        grads[kind] = hd_gradient(*grad_rows)
        for member, ch, low, h in tiles:
            src = EN_SRC[kind].get(ch)
            if ch == 'E' and USE_EN_E:
                src = EN_ALT['E']
            letters.append(Letter(kind, ch, member, low, h, low_fill(low, grad_rows), src))
    P, cal_err = calibrate(letters, pack)
    print('calibration: x scale %.4f  stroke weight %.3f HD px/side  HAI PERSO squeeze %.4f  (mean sq. error %.5f)'
          % (P['sx'], P['w'], P['squeeze'], cal_err))
    # diagnostic: the other shape source for the letters that exist in both (not used)
    for let in letters:
        if let.ch in 'INOSE':
            alt = Letter(let.kind, let.ch, let.member, let.low, let.h, let.flow,
                         None if let.src else (EN_SRC[let.kind].get(let.ch) or EN_ALT.get(let.ch)))
            if alt.src is None and let.src is None:
                continue
            e0, e1 = fit_error(let, pack, P)[0], fit_error(alt, pack, P)[0]
            print('  source check %-5s %s: used %-12s err %.5f | other %-12s err %.5f'
                  % (let.kind, let.ch, 'English' if let.src else 'Times Bold', e0, 'Times Bold' if let.src else 'English', e1))
    log = []
    for let in letters:
        hd, info = build_letter(let, pack, P, grads[let.kind], luts[let.kind])
        tid = f'basic_{B}__' + let.member[:-4]
        fam.save(tid, hd, let.h, let.low)
        log.append((tid, let.ch) + info)
        if let.kind == 'win' and let.member == 'duel_win1000%02d.gim' % (2 * len(LETTERS['win'])):                          # last tile of the win word: its silhouette follows
            low, h = common.texture(usr, ARCH, 'duel_win1000%02d.gim' % (2 * len(LETTERS['win']) + 2))
            fam.save('basic_%s__duel_win1000%02d' % (B, 2 * len(LETTERS['win']) + 2), silhouette(low.convert('RGBA')), h, low.convert('RGBA'))
    for tid, ch, how, sx, sy, tx, e in log:
        print('%-30s %s %-44s sx %.4f sy %.4f  x %.2f  fit %.5f' % (tid, ch, how, sx, sy, tx, e))
    fam.finish()


if __name__ == '__main__':
    main(sys.argv)
