"""icon_sheets: icon/UI sheets that are the English HD sheet except for a few Italian words.

usage: python3 -I icon_sheets.py USRDIR PACK_US OUT

Every texture starts from the English HD sheet of MikeyMK's pack: the pixels that do not change are the pack's own,
untouched (a diff against the pack shows changes only inside the boxes listed below).  Only the places where the
Italian low-res texture differs from it (Italian words, the few spots where the European sheet differs from the
American one the pack was made on) are redrawn, each the way the pack draws that element, as CLEAN art (crisp
edges, one font / one weight / one shadow per word, no blur, nothing fitted letter by letter):
  all_i__icon04      'TUTTE', 'Mia', 'Lab', 'N', the 'A' badges: nearest x4 of the Italian pixels, exactly how the pack
                     keeps 'ALL', 'My', 'LAB', 'NEW', 'R' (nearest-x4 patches only where they differ from the sheet);
                     'Comp!' -> 'Set!': the WHOLE word (the '!' too) is redrawn in one rounded, non-condensed face
                     (SF Compact Rounded Bold, chosen by measured overlap with the pack's C-o-m-p among the rounded
                     faces), one size / baseline / weight, the pack's gold gradient (measured on the pack's C and
                     o/m/p), brown outline and soft shadow; the pack's thumb is kept;
                     '5,6' -> '5.6': the pack's comma is removed and a clean round dot is set on the ball body;
                     the European document with a lightning bolt: nearest x4 of the Italian pixels, bolt included
                     (the pack's own DL document next to it is nearest x4 pixel art as well).
  all_i__s_pack      'ESAURITE': PT Sans Bold (+0.5 px weight), the best match of the pack's 'SOLD OUT' by measured
                     overlap, at the pack's cap height, in the pack's red; the white band is the pack's own, repeated,
                     up to its edge.
  all_i__panel       'prati': Futura Bold, the best match of the pack's 'Kind of card' (overlap 0.84, next font 0.77),
                     pack x-height, +0.6 px weight and 1.5 px rounded corners like the pack's heavy lettering, the
                     pack's white + drop shadow; the tab is rebuilt from a text-free column of the pack's tab.
  always_bri_ita__pda_pack01
                     the pack keeps the whole sheet at nearest x4, so 'NUOVO' and the European label column are
                     nearest x4 of the Italian pixels.
  cardalbum__icon06_i  the pack's own 'NEW' tile with its hidden lower half mirrored and the pack's own N scaled in
                     (one uniform scale, native proportions).
  cardalbum__ocglist_i the pack only has the American sheet at 1:1 (nothing enlarged): the Italian sheet is the plain
                     nearest-x4 enlargement of its own pixel art.
  title_menu_i__mein_menu00 / trnsmt01
                     'NUOVO' on the pack's orange button (navy strokes through the pixel centres, like the pack's thin
                     'NEW'), the pack's yellow N moved / widened to the Italian N (mein_menu00), the European document
                     + bolt as in icon04 but with a clean polygon bolt and a soft shadow like the pack's other (smooth)
                     documents of that sheet;
                     trnsmt01: the pack's art is kept down to HD row 396; below it the Italian pixels of the three box
                     icons are enlarged without blur (Scale4x classes + sharp sigmoid), the 'N' badges are clean
                     polygon letters, and the pack's glow / shadow are generated for the new art (no seam, no blur).
Fonts were chosen by measuring the overlap (IoU, one common scale) between the pack's real letters and every installed
face of /System/Library/Fonts, .../Supplemental and /Library/Fonts.  Only ISO data, the English pack and those fonts are
used."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import alt_font  # noqa: nessun font Apple
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SUP = '/System/Library/Fonts/Supplemental/'
SYS = '/System/Library/Fonts/'
K = common.SCALE
LANG = os.environ.get('TF1_LANG', 'it')
LL = {'it': 'i', 'fr': 'f', 'es': 's', 'de': 'g', 'en': 'e'}[LANG]
SP_TEXT, SP_X = {'it': ('ESAURITE', (27.5, 243.5)), 'fr': ('ÉPUISÉ', (45.0, 228.0)), 'es': ('AGOTADO', (29.0, 245.0)), 'de': ('AUSVERKAUFT', (22.0, 248.0)), 'en': ('SOLD OUT', (40.0, 240.0))}[LANG]
PANEL_TEXT = {'it': 'prati', 'fr': 'hetés', 'es': 'rados', 'de': 'ypen', 'en': 'ased'}[LANG]
PANEL_X = {'de': (720.5, 830.0)}.get(LANG, (724.5, 836.0))
EN_LOW = None          # low-resolution English texture (comparison for the languages without their own words in the pack)

# (file, face index, variation) of the fonts used
PT_SANS_BOLD = (SUP + 'PTSans.ttc', 7, None)
FUTURA_BOLD = (SUP + 'Futura.ttc', 2, None)
SF_COMPACT_ROUNDED_BOLD = (SYS + 'SFCompactRounded.ttf', 0, (700,))     # variable font, weight axis 700


# ---------------------------------------------------------------- generic helpers
def arr(im):
    return np.asarray(im.convert('RGBA')).astype(np.float32)


def img(a):
    return Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8), 'RGBA')


def nn(a, k=K):
    return np.repeat(np.repeat(a, k, 0), k, 1)


def low_of(a, k=K):
    """area (box) downscale by k of a float array."""
    h, w = a.shape[:2]
    return cv2.resize(a, (w // k, h // k), interpolation=cv2.INTER_AREA)


def over(dst, color, alpha, region=None):
    """composite a flat colour with coverage `alpha` (float 0..1, HD size of region) onto dst (in place)."""
    if region is None:
        region = (0, 0, dst.shape[1], dst.shape[0])
    x0, y0, x1, y1 = region
    d = dst[y0:y1, x0:x1]
    a = np.clip(alpha, 0, 1)[..., None]
    c = np.asarray(color, np.float32)
    da = d[..., 3:4] / 255
    oa = a + da * (1 - a)
    rgb = (c[:3] * a + d[..., :3] * da * (1 - a)) / np.maximum(oa, 1e-6)
    d[..., :3] = np.where(oa > 0, rgb, d[..., :3])
    d[..., 3:4] = oa * 255


def over_rgba(dst, src, x0, y0):
    """alpha-composite a float RGBA array onto dst at (x0, y0)."""
    h, w = src.shape[:2]
    d = dst[y0:y0 + h, x0:x0 + w]
    sa = src[..., 3:4] / 255
    da = d[..., 3:4] / 255
    oa = sa + da * (1 - sa)
    rgb = (src[..., :3] * sa + d[..., :3] * da * (1 - sa)) / np.maximum(oa, 1e-6)
    d[..., :3] = np.where(oa > 0, rgb, d[..., :3])
    d[..., 3:4] = oa * 255


def prem(a):
    return np.concatenate([a[..., :3] * a[..., 3:] / 255, a[..., 3:]], -1)


def blur(a, s):
    return cv2.GaussianBlur(a, (0, 0), s) if s > 0 else a


def disk_dilate(cov, r, ss=4):
    """coverage dilated by a disc of radius r (HD px), antialiased."""
    h, w = cov.shape
    big = cv2.resize(cov, (w * ss, h * ss), interpolation=cv2.INTER_LINEAR)
    R = int(round(r * ss))
    big = cv2.dilate(big, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * R + 1, 2 * R + 1)))
    return np.clip(cv2.resize(big, (w, h), interpolation=cv2.INTER_AREA), 0, 1)


def shift(a, dx, dy):
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(a, M, (a.shape[1], a.shape[0]), flags=cv2.INTER_LINEAR, borderValue=0)


def patch_nn(out, low, box, thr=40):
    """nearest x4 of the Italian pixels inside the low-res `box` wherever they differ from the HD sheet
    (box-downscaled): used where the pack kept the pixel art at nearest x4."""
    x0, y0, x1, y1 = box
    ref = low_of(prem(out[y0 * K:y1 * K, x0 * K:x1 * K]))
    it = low[y0:y1, x0:x1]
    m = np.abs(ref - prem(it)).max(-1) > thr
    blk = nn(it)
    mm = nn(m[..., None].astype(np.uint8))[..., 0].astype(bool)
    out[y0 * K:y1 * K, x0 * K:x1 * K][mm] = blk[mm]
    return int(m.sum())


# ---------------------------------------------------------------- lettering
_fonts = {}
_ink = {}


def face_font(face, size):
    path, idx, var = face
    key = (face, round(size, 3))
    if key not in _fonts:
        f = ImageFont.truetype(path, size, index=idx)
        if isinstance(var, tuple):
            f.set_variation_by_axes(list(var))
        elif var:
            f.set_variation_by_name(var)
        _fonts[key] = f
    return _fonts[key]


def ink_box(face, ch, size):
    """ink bbox (l, t, r, b) of the glyph `ch` rendered at `size`, relative to the baseline origin (y down)"""
    key = (face, ch, round(size, 3))
    if key not in _ink:
        f = face_font(face, size)
        S = int(size * 3) + 8
        im = Image.new('L', (S, S), 0)
        ImageDraw.Draw(im).text((size, size * 2), ch, font=f, fill=255, anchor='ls')
        ys, xs = np.nonzero(np.asarray(im) > 127)
        _ink[key] = (xs.min() - size, ys.min() - size * 2, xs.max() + 1 - size, ys.max() + 1 - size * 2)
    return _ink[key]


def cap_ratio(face, ref='H'):
    l, t, r, b = ink_box(face, ref, 400)
    return (b - t) / 400.0


def word_cov(text, face, cap, x0, x1, base, region, ref='H', dil=0.0, round_px=0.0, track_range=(-0.045, 0.12),
             squeeze_max=0.10, ss=8):
    """coverage (float 0..1, HD px of `region` = (x0, y0, x1, y1)) of `text` set in one font: the glyph `ref` is `cap`
    px tall, the baseline is at `base`, the ink spans x0..x1.  One size, one baseline, natural glyph shapes; the
    tracking is solved to hit the width (kerning of the font kept); only if it would have to go below
    track_range[0] em the whole word is squeezed horizontally (at most squeeze_max).  `dil` thickens the strokes,
    `round_px` rounds the convex corners (morphological opening) like the pack's rounded lettering."""
    rx0, ry0, rx1, ry1 = region
    size = cap / cap_ratio(face, ref) * ss
    f = face_font(face, size)
    n = len(text)
    pos = [f.getlength(text[:i + 1]) - f.getlength(text[i]) for i in range(n)]
    bl = ink_box(face, text[0], size)
    br = ink_box(face, text[-1], size)
    W0 = (pos[-1] + br[2]) - (pos[0] + bl[0])
    Wt = (x1 - x0) * ss
    sq = 1.0
    tr = (Wt - W0) / (n - 1) if n > 1 else 0.0
    if tr < track_range[0] * size:
        tr = track_range[0] * size
        sq = max(Wt / (W0 + (n - 1) * tr), 1 - squeeze_max)
    elif tr > track_range[1] * size:
        tr = track_range[1] * size
    H, W = (ry1 - ry0) * ss, (rx1 - rx0) * ss
    left = (x0 - rx0) * ss - (pos[0] + bl[0])
    Wd = max(W, int(left + pos[-1] + br[2] + (n - 1) * tr) + 4 * ss) if sq != 1.0 else W    # if the word must be compressed it is drawn whole and then squeezed
    im = Image.new('L', (Wd, H), 0)
    d = ImageDraw.Draw(im)
    for i, ch in enumerate(text):
        d.text((left + pos[i] + i * tr, (base - ry0) * ss), ch, font=f, fill=255, anchor='ls')
    a = np.asarray(im).astype(np.float32) / 255
    if sq != 1.0:
        ax = (x0 - rx0) * ss
        a = cv2.warpAffine(a, np.float32([[sq, 0, ax * (1 - sq)], [0, 1, 0]]), (W, H), flags=cv2.INTER_LINEAR,
                           borderValue=0)
    if dil > 0:
        k = int(round(dil * ss)) * 2 + 1
        a = cv2.dilate(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    if round_px > 0:
        ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(round(round_px * ss)) * 2 + 1,) * 2)
        a = cv2.dilate(cv2.erode(a, ker), ker)
    return cv2.resize(a, (rx1 - rx0, ry1 - ry0), interpolation=cv2.INTER_AREA)


# ---------------------------------------------------------------- pixel art -> crisp HD
def scale2x(a):
    """EPX / AdvMAME2x (exact colour equality), the classic pixel-art doubler."""
    p = np.pad(a, ((1, 1), (1, 1), (0, 0)), mode='edge')
    E, B, D, F, H = p[1:-1, 1:-1], p[:-2, 1:-1], p[1:-1, :-2], p[1:-1, 2:], p[2:, 1:-1]
    eq = lambda x, y: (x == y).all(-1)
    c = (~eq(B, H)) & (~eq(D, F))
    o = np.zeros((a.shape[0] * 2, a.shape[1] * 2) + a.shape[2:], a.dtype)
    o[0::2, 0::2] = np.where((c & eq(D, B))[..., None], D, E)
    o[0::2, 1::2] = np.where((c & eq(B, F))[..., None], F, E)
    o[1::2, 0::2] = np.where((c & eq(D, H))[..., None], D, E)
    o[1::2, 1::2] = np.where((c & eq(H, F))[..., None], F, E)
    return o


def quantize(low, thr=16.0):
    """merge the colours of a low-res region that are closer than `thr` (RGB distance, alpha within 40) into the most
    frequent colour of their group: removes the 1-2 level noise of the originals, keeps every real shade."""
    low = np.round(low).astype(np.float32)
    cols, inv, cnt = np.unique(low.reshape(-1, 4), axis=0, return_inverse=True, return_counts=True)
    centres = []
    assign = np.zeros(len(cols), np.int32)
    for i in np.argsort(-cnt, kind='stable'):
        c = cols[i]
        best, bd = -1, 1e9
        for j, cc in enumerate(centres):
            if abs(cc[3] - c[3]) > 40:
                continue
            d = float(np.sqrt(((cc[:3] - c[:3]) ** 2).sum()))
            if d < bd:
                best, bd = j, d
        if best >= 0 and bd < thr:
            assign[i] = best
        else:
            centres.append(c)
            assign[i] = len(centres) - 1
    return np.array(centres, np.float32)[assign[inv.reshape(-1)]].reshape(low.shape)


def crisp_up(low, sigma=0.7, beta=10.0):
    """x4 enlargement of flat pixel art: Scale4x gives the shape of every colour class, each class is softened with a
    small gaussian (sigma, HD px) and the classes are mixed with a steep softmax (beta): edges are smooth, 1 px
    antialiased and constant in width, interiors are flat (no blur, no halo).  low: float RGBA (h, w, 4)."""
    low = np.round(low).astype(np.float32)
    S = scale2x(scale2x(low))
    flat = S.reshape(-1, 4).copy()
    flat[flat[:, 3] == 0] = 0
    cols, inv = np.unique(flat, axis=0, return_inverse=True)
    inv = inv.reshape(S.shape[:2])
    U = np.zeros(S.shape[:2] + (len(cols),), np.float32)
    for k in range(len(cols)):
        ind = (inv == k).astype(np.float32)
        U[..., k] = cv2.GaussianBlur(ind, (0, 0), sigma) if sigma > 0 else ind
    w = np.exp(beta * (U - U.max(-1, keepdims=True)))
    w /= w.sum(-1, keepdims=True)
    out = w @ prem(cols)
    a = out[..., 3:4]
    rgb = np.where(a > 1e-3, out[..., :3] * 255 / np.maximum(a, 1e-3), 0)
    return np.concatenate([rgb, a], -1)


# ---------------------------------------------------------------- the European 'download' document with the bolt
def bolt_polygon(core, shape):
    """clean lightning-bolt coverage (HD px, antialiased) from the yellow core pixels (bool, low-res) of the European
    document icon: the core is smoothed, its contour simplified to a handful of straight edges (a real bolt, no
    wobble) and filled with 8x supersampling."""
    c = np.pad(core.astype(np.float32), 1)
    h, w = c.shape
    c8 = cv2.GaussianBlur(cv2.resize(c, (w * 8, h * 8), interpolation=cv2.INTER_CUBIC), (0, 0), 2.8)
    cs, _ = cv2.findContours((c8 > 0.25).astype(np.uint8) * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    ap = cv2.approxPolyDP(max(cs, key=cv2.contourArea), 10.0, True)
    big = np.zeros((h * 8, w * 8), np.uint8)
    cv2.fillPoly(big, [ap], 255, lineType=cv2.LINE_AA)
    cov = cv2.resize(big.astype(np.float32) / 255, (w * K, h * K), interpolation=cv2.INTER_AREA)
    return cov[K:-K, K:-K]


def bolt_doc(out, low, box, y_top, y_bot, soft_shadow=False, vector_bolt=True):
    """The European sheets show a green document crossed by a lightning bolt where the American ones have 'DL'.
    The document (frame, white page, green lines, shadow) is the Italian pixels at nearest x4 - square corners and
    4 px lines like the pack's blue and pink documents - and the bolt (the Italian low-res bolt is a few yellow
    pixels in a thick brown outline) is redrawn as a clean polygon bolt that follows the yellow core, flat yellow
    with a thin dark outline.  box = low-res box around the document; y_top / y_bot = its first / last frame row;
    soft_shadow: replace the 1-px hard shadow by a soft one (sheets whose other icons have soft shadows)."""
    x0, y0, x1, y1 = box
    reg = low[y0:y1, x0:x1].copy()
    if not vector_bolt:                                          # whole document (bolt included) as nearest x4
        out[y0 * K:y1 * K, x0 * K:x1 * K] = nn(reg)
        return

    def near(c, tol=6):
        return (np.abs(reg[..., :3] - np.array(c, np.float32)).max(-1) <= tol) & (reg[..., 3] > 200)
    core = near((255, 245, 1)) | near((248, 235, 41))
    bolt = core | near((96, 79, 36)) | near((128, 128, 128)) | near((0, 61, 23))   # the last: the bolt's shadow on the frame
    doc = reg.copy()
    ys, xs = np.nonzero(bolt)
    green = reg[y_top - y0, 88 - x0].copy()                      # frame colour (top-left corner of the document)
    for y, x in zip(ys, xs):
        gy, gx = y + y0, x + x0
        if gy in (y_top, y_bot) or gx in (88, 96):               # frame row / column under the bolt
            doc[y, x] = green
        elif gy > y_bot:
            doc[y, x] = (0, 0, 0, 128)
        else:
            doc[y, x] = (255, 255, 255, 255)
    if soft_shadow:
        doc[(doc[..., 3] > 0) & (doc[..., 3] < 255) & (doc[..., :3].max(-1) < 5)] = 0
    up = nn(doc)
    if soft_shadow:
        layer = np.zeros_like(up)
        over(layer, (0, 0, 0), blur(shift(up[..., 3] / 255, 4.0, 4.0), 1.6) * 0.6)
        over_rgba(layer, up, 0, 0)
        up = layer
    cov = bolt_polygon(core, reg.shape[:2])
    over(up, (70, 52, 12), disk_dilate(cov, 2.0))
    over(up, (255, 240, 0), cov)
    out[y0 * K:y1 * K, x0 * K:x1 * K] = up


# ---------------------------------------------------------------- icon04 (deck editor icons)
def row_run_dist(mask):
    """for every pixel of a boolean mask: distance (px) to the left end and to the right end of its horizontal run"""
    h, w = mask.shape
    dl = np.zeros((h, w), np.float32)
    dr = np.zeros((h, w), np.float32)
    for y in range(h):
        run = 0
        for x in range(w):
            run = run + 1 if mask[y, x] else 0
            dl[y, x] = run
        run = 0
        for x in range(w - 1, -1, -1):
            run = run + 1 if mask[y, x] else 0
            dr[y, x] = run
    return dl, dr


def set_label(out, pack):
    """'Comp!' -> 'Set!'.  The pack's thumb is kept (and stays in front of the letters, as in the Italian sheet); every
    letter of 'Comp!' including its '!' is erased and the whole word 'Set!' is drawn in ONE rounded, non-condensed
    face (SF Compact Rounded Bold - the best-matching rounded face of the pack's C-o-m-p by measured overlap), one
    size / baseline / weight, with the recipe of the pack's lettering: vertical gold gradient measured on the pack's
    'C' stem (cream-white at the cap top -> yellow -> orange), a lighter left edge and darker right edge of every stroke,
    thin dark-brown outline, soft drop shadow.  'Set' spans the Italian x range 422..478, the '!' sits at the Italian
    '!' position (centre x 490); baseline 150, cap height 28.5 (the Italian 'S' is 32 px tall including its outline)."""
    rx0, ry0, rx1, ry1 = 400, 104, 506, 176
    ys, xs = np.mgrid[ry0:ry1, rx0:rx1]
    reg = out[ry0:ry1, rx0:rx1]
    # erase 'C', 'omp' (below the wrist of the thumb) and the '!'; the thumb itself stays
    reg[((xs < 441) & (ys >= 108)) | ((ys >= 134) & (xs < 482)) | ((xs >= 480) & (ys >= 108))] = 0
    cap, base = 28.5, 150.0
    face = SF_COMPACT_ROUNDED_BOLD
    region = (rx0, ry0, rx1, ry1)
    fill = word_cov('Set', face, cap, 422.0, 478.0, base, region, ref='H')
    size = cap / cap_ratio(face) * 8
    l, t, r, b = ink_box(face, '!', size)
    wid = (r - l) / 8.0
    fill = np.maximum(fill, word_cov('!', face, cap, 490.0 - wid / 2, 490.0 + wid / 2, base, region, ref='H'))
    H, W = fill.shape
    col = np.zeros((H, W, 3), np.float32)
    xh = cap * 0.77                                               # x-height of the face (SF: 0.77 of the cap height)
    # word-level gold gradient measured on the pack's 'Comp!': cream-white at the cap top (the C's top, row 127),
    # saturated yellow at the lowercase tops (the 'o' / 'm' tops), through amber to the orange-gold of the baseline
    # rows (the 'o', 'm', 'p' bottoms).  Stops: (distance below the cap top / the lowercase height, RGB)
    gy = [-(cap - xh) / xh, 0.0, 0.30, 0.50, 0.65, 0.85, 1.0]
    gc = np.array([(253, 251, 221), (255, 255, 134), (255, 250, 110), (251, 222, 76), (250, 205, 58), (254, 193, 42),
                   (255, 176, 28)], np.float32)
    for y in range(H):
        t = (ry0 + y - (base - xh)) / xh
        col[y] = [np.interp(t, gy, gc[:, c]) for c in range(3)]
    dl, dr = row_run_dist(fill > 0.5)
    light = np.clip(1 - (dl - 0.5) / 3.5, 0, 1) * 0.45            # lighter left edge of every stroke
    dark = np.clip(1 - (dr - 0.5) / 3.0, 0, 1) * 0.22             # darker / more orange right edge
    col = col * (1 - light[..., None]) + np.array([255, 253, 232], np.float32) * light[..., None]
    col = col * (1 - dark[..., None]) + np.array([226, 138, 20], np.float32) * dark[..., None]
    inner = np.clip(1 - cv2.distanceTransform((fill > 0.5).astype(np.uint8), cv2.DIST_L2, 5) / 1.4, 0, 1)
    col = col * (1 - 0.18 * inner[..., None]) + np.array([214, 124, 18], np.float32) * 0.18 * inner[..., None]
    outline = disk_dilate(fill, 1.7)
    shadow = blur(shift(outline, 1.5, 2.5), 1.4) * 0.4
    layer = np.zeros((H, W, 4), np.float32)
    over(layer, (0, 0, 0), shadow)
    over(layer, (78, 28, 4), outline)
    a = fill[..., None]
    layer[..., :3] = layer[..., :3] * (1 - a) + col * a
    layer[..., 3:] = np.maximum(layer[..., 3:], a * 255)
    over_rgba(out, layer, rx0, ry0)


def round_box(px, py, x0, y0, x1, y1, r):
    """coverage (antialiased) of the rounded rectangle x0..x1, y0..y1 with corner radius r at the points px, py"""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    qx = np.abs(px - cx) - ((x1 - x0) / 2 - r)
    qy = np.abs(py - cy) - ((y1 - y0) / 2 - r)
    d = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2) + np.minimum(np.maximum(qx, qy), 0) - r
    return np.clip(0.5 - d, 0, 1)


def mid_dot(out):
    """'5,6' -> '5.6' as in the European sheet.  The American sheet's comma (white blob + tail hanging below the
    baseline) is removed and replaced by a round white dot with a dark ring (the digits' own outline colour) at the
    height of the Italian dot, set on the ball body: the pixels the comma covered between the two digits are the
    ball's body, which darkens (red -> dark red -> outline) toward the bottom of the ball as in the low-res art."""
    x0, y0, x1, y1 = 84, 36, 120, 76
    reg = out[y0:y1, x0:x1]
    bright = ((reg[..., :3].min(-1) > 140) & (reg[..., 3] > 128)).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(bright, connectivity=8)
    k = min(range(1, n), key=lambda i: (cen[i][0] + x0 - 100) ** 2 + (cen[i][1] + y0 - 58.5) ** 2)
    comma = (lab == k).astype(np.uint8)
    digits = ((bright > 0) & (lab != k)).astype(np.uint8)
    dist = cv2.distanceTransform(1 - digits, cv2.DIST_L2, 5)
    ring = (dist > 1.5) & (dist < 3.0) & (reg[..., :3].max(-1) < 70) & (reg[..., 3] > 250)
    dark = np.median(reg[..., :3][ring], 0)                        # the digits' own outline colour
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    px, py = xx + 0.5, yy + 0.5
    cx, cy, rw, ring_w, ybot = 101.0, 52.5, 3.6, 2.4, 62.6
    top = reg[49 - y0, int(cx) - x0 - 1:int(cx) - x0 + 2, :3].mean(0)   # ball colour just above the comma
    # 1) the comma (white + its outline) goes: below the plate's bottom edge back to transparent (but never the
    #    dark line that runs under the digits), elsewhere the plate repaints it
    near_comma = cv2.dilate(comma, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))).astype(bool) & (dist > 1.2)
    reg[near_comma & (py > ybot - 0.7) & (py < 66.8)] = 0
    # 2) the plate: ball red -> dark red -> outline colour, rounded bottom, between the outlines of the digits
    t = np.clip((py - 50) / 10.5, 0, 1)[..., None]
    col = top * (1 - t) + np.array([136, 10, 14], np.float32) * t
    t2 = np.clip((py - 60.4) / (ybot - 60.4), 0, 1)[..., None]
    col = col * (1 - t2) + dark * t2
    plate = round_box(px, py, 94.5, cy - 3, 107.5, ybot, 1.2) * (dist > 2.0)
    a = plate[..., None]
    reg[..., :3] = reg[..., :3] * (1 - a) + col * a
    reg[..., 3:] = np.maximum(reg[..., 3:], a * 255)
    # 3) the dot
    d = np.sqrt((px - cx) ** 2 + (py - cy) ** 2)
    over(reg, dark, np.clip(rw + ring_w - d + 0.5, 0, 1))
    over(reg, (255, 255, 255), np.clip(rw - d + 0.5, 0, 1))


def build_icon04(low, hd):
    """TUTTE/Mia/Lab/N and the 'A' badges: the pack keeps these at nearest x4, so nearest x4 of the Italian pixels.
    'Comp!' -> 'Set!' (set_label), '5,6' -> '5.6' (mid_dot), the European lightning document (bolt_doc)."""
    out = hd.copy()
    for box in ((17, 37, 36, 49), (4, 57, 48, 64), (36, 52, 62, 86)):
        patch_nn(out, low, box)
    bolt_doc(out, low, (86, 33, 100, 51), 35, 47, vector_bolt=False)
    set_label(out, hd)
    mid_dot(out)
    return out


def build_icon04_fr(low, hd):
    """French: the pack's English sheet where the French texture is equal to the English one (ALL, Comp!, NEW); where it differs
    ('Moi', the 'L' badges, ...) the French pixels x4 without smoothing, as the pack keeps the other pixel art of this sheet;
    the European document with the lightning bolt as in Italian."""
    out = hd.copy()
    m = np.abs(low - EN_LOW).max(-1) > 40
    m = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    m[33:51, 86:100] = False                                  # the document with the lightning bolt has separate treatment (bolt_doc)
    mm = nn(m[..., None].astype(np.uint8))[..., 0].astype(bool)
    out[mm] = nn(low)[mm]
    bolt_doc(out, low, (86, 33, 100, 51), 35, 47, vector_bolt=False)
    return out


def build_icon04_en(low, hd):
    """European English: the US pack's sheet, with the European texture's pixels x4 without smoothing where the two differ."""
    out = hd.copy()
    small = hd.reshape(hd.shape[0] // K, K, hd.shape[1] // K, K, hd.shape[2]).mean((1, 3))
    m = np.abs(low - small).max(-1) > 40
    m = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    mm = nn(m[..., None].astype(np.uint8))[..., 0].astype(bool)
    out[mm] = nn(low)[mm]
    return out


# ---------------------------------------------------------------- pda_pack01 (PDA / calendar sheet)
def build_pda_pack01(low, hd):
    """The pack keeps this sheet at nearest x4.  'NEW' -> 'NUOVO' next to the yellow frame, and the European
    column of 'NEW / NEU / NEW / NUOVO / NEW' labels (empty in the American sheet) is added."""
    out = hd.copy()
    for box in ((215, 15, 238, 26), (271, 12, 300, 69)):
        patch_nn(out, low, box)
    return out


# ---------------------------------------------------------------- panel (shop: purchase panel sheet)
def build_panel(low, hd):
    """The American tab reads 'Kind of card' and starts further left; the Italian piece of the tab starts at
    x=180 (the rest of the word is in another texture) and reads 'prati'.  The tab is rebuilt from a text-free
    column of the pack's tab, 'prati' is Futura Bold (the best match of the pack's 'Kind of card' letters), the same
    x-height (25 px) as the pack's lettering, stroke weight +0.6 px and corners rounded 1.5 px like the pack's
    heavy rounded letters, white with the pack's dark drop shadow."""
    out = hd.copy()
    out[568:676, 720:846] = out[568:676, 842:843]
    a = low[141:171, 133:180, 3] == 0                        # left of the Italian piece: empty
    out[141 * K:171 * K, 133 * K:180 * K, 3][nn(a[..., None].astype(np.uint8))[..., 0].astype(bool)] = 0
    region = (716, 584, 856, 664)
    cov = word_cov(PANEL_TEXT, FUTURA_BOLD, 25.0, PANEL_X[0], PANEL_X[1], 634.0, region, ref='x', dil=0.6, round_px=1.5)
    H, W = cov.shape
    layer = np.zeros((H, W, 4), np.float32)
    over(layer, (12, 9, 5), blur(shift(cov, 2.5, 2.5), 1.0) * 0.85)
    over(layer, (255, 255, 255), cov)
    over_rgba(out, layer, region[0], region[1])
    return out


# ---------------------------------------------------------------- title menu sheets (mein_menu00, trnsmt01)
def polyline_cov(lines, shape, r, ss=8):
    """coverage of round-capped polylines (HD coordinates) of radius r."""
    h, w = shape
    big = np.zeros((h * ss, w * ss), np.uint8)
    R = int(round(r * ss))
    for pts in lines:
        p = [(int(round(x * ss)), int(round(y * ss))) for x, y in pts]
        for a, b in zip(p[:-1], p[1:]):
            cv2.line(big, a, b, 255, 2 * R + 1, lineType=cv2.LINE_AA)
        for a in p:
            cv2.circle(big, a, R, 255, -1, lineType=cv2.LINE_AA)
    return cv2.resize(big.astype(np.float32) / 255, (w, h), interpolation=cv2.INTER_AREA)


# the Italian 3x5 pixel letters of the orange 'NUOVO' button, as strokes through the pixel centres
# (low-res units, origin = the letter's top-left pixel)
NEW_GLYPHS = {
    'N': [[(0, 4), (0, 0), (2, 4), (2, 0)]],
    'U': [[(0, 0), (0, 3.0), (0.35, 3.7), (1, 4), (1.65, 3.7), (2, 3.0), (2, 0)]],
    'O': [[(1, 0), (1.65, 0.3), (2, 1.0), (2, 3.0), (1.65, 3.7), (1, 4), (0.35, 3.7), (0, 3.0), (0, 1.0), (0.35, 0.3), (1, 0)]],
    'V': [[(0, 0), (0, 1.6), (1, 3.6), (1, 4)], [(2, 0), (2, 1.6), (1, 3.6)]],
}


def new_button(out):
    """'NEW' -> 'NUOVO' on the pack's orange button (same place in mein_menu00 and trnsmt01): the letters are
    removed by repeating each row's button colour, then the Italian letters are drawn as thin navy strokes with
    the faint yellow glow the pack's letters have."""
    reg = out[0:36, 52:136]
    orange = (reg[..., 0] > 230) & (reg[..., 1] > 120) & (reg[..., 1] < 190) & (reg[..., 2] < 70) & (reg[..., 3] > 250)
    for y in range(6, 31):
        sel = orange[y]
        sel[:6] = sel[-6:] = False
        reg[y, 6:80, :3] = np.median(reg[y][sel][:, :3], 0)
        reg[y, 6:80, 3] = 255
    lines = []
    for ch, c0 in zip('NUOVO', (14, 18, 22, 26, 30)):
        for pl in NEW_GLYPHS[ch]:
            lines.append([((c0 + x + 0.5) * K - 52, (2 + y + 0.5) * K) for x, y in pl])
    cov = polyline_cov(lines, (36, 84), 1.65)
    glow = blur(disk_dilate(cov, 2.0), 1.2) * 0.55
    over(reg, (255, 196, 18), glow)
    over(reg, (0, 12, 34), cov)


def copy_n(out, hd, src_l, src_r, src_r2, dst_x0, y0, y1, width=None, edge=14, feather=0):
    """reuse the pack's yellow 'N' (with its dark plate and glow) from a 'NEW' label.  [src_l, src_l+edge) is
    the left edge of the plate, [src_l+edge, src_r) the N up to its right stem, then the right edge of the plate
    is taken after the 'W' [src_r2, src_r2 + edge) or (src_r2=None) mirrored from the left edge.
    width: optional horizontal resample of the N body; feather: soft alpha at the piece's borders (px)."""
    ledge = hd[y0:y1, src_l:src_l + edge]
    body = hd[y0:y1, src_l + edge:src_r]
    redge = hd[y0:y1, src_r2:src_r2 + edge] if src_r2 is not None else ledge[:, ::-1]
    if width is not None:
        body = cv2.resize(body, (width, y1 - y0), interpolation=cv2.INTER_CUBIC)
    piece = np.clip(np.concatenate([ledge, body, redge], 1), 0, 255)
    if feather:
        h, w = piece.shape[:2]
        rx = np.clip(np.minimum(np.arange(w) + 0.5, w - np.arange(w) - 0.5) / feather, 0, 1)
        ry = np.clip((np.arange(h) + 0.5) / feather, 0, 1)
        piece[..., 3] *= ry[:, None] * rx[None, :]
    over_rgba(out, piece, dst_x0, y0)


def build_mein_menu00(low, hd):
    """'NEW' -> 'NUOVO' (orange button), yellow 'NEW' -> 'N' (the pack's own N moved to the Italian position),
    and the European document-with-lightning icon in place of the American 'DL' one (bolt_doc)."""
    out = hd.copy()
    new_button(out)
    # yellow N: the Italian N is the English N moved 5 px to the right
    out[14:58, 321:394] = 0
    copy_n(out, hd, 322, 344, 384, 342, 14, 58)
    bolt_doc(out, low, (86, 15, 99, 30), 16, 28, soft_shadow=True)
    return out


def raster_polys(polys, shape, origin, ss=8):
    """antialiased coverage of polygons given in low-res units; origin = HD pixel of the canvas' top-left"""
    h, w = shape
    ox, oy = origin
    big = np.zeros((h * ss, w * ss), np.uint8)
    for p in polys:
        pts = np.array([[(x * K - ox) * ss, (y * K - oy) * ss] for x, y in p], np.float64)
        cv2.fillPoly(big, [np.round(pts).astype(np.int32)], 255, lineType=cv2.LINE_AA)
    return cv2.resize(big.astype(np.float32) / 255, (w, h), interpolation=cv2.INTER_AREA)


def n_polys(sx, y0=100.0):
    """the Italian 5x5 pixel 'N' of a box badge (left stem at low-res column sx, rows y0..y0+5) as clean polygons:
    two 1-px stems and a 45-degree diagonal (the pixels (sx+1, y0+1), (sx+2, y0+2), (sx+3, y0+3))."""
    stem_l = [(sx, y0), (sx + 1, y0), (sx + 1, y0 + 5), (sx, y0 + 5)]
    stem_r = [(sx + 4, y0), (sx + 5, y0), (sx + 5, y0 + 5), (sx + 4, y0 + 5)]
    diag = [(sx, y0), (sx + 1.2, y0), (sx + 5, y0 + 4.2), (sx + 5, y0 + 5), (sx + 3.8, y0 + 5), (sx, y0 + 0.8)]
    return [stem_l, stem_r, diag]


def trnsmt_strip(out, low):
    """Under the three box icons the pack has 'NEW' (black plate, soft glow) hiding the boxes' bottoms; the Italian
    sheet shows the bottoms (and a small 'N' badge instead).  The pack's art is kept untouched down to the HD row 396
    (low-res row 99); from there the Italian pixels are enlarged WITHOUT any blur: Scale4x classes + a sharp sigmoid
    (crisp antialiased edges, no halo), the grey faces of the first low-res row take the pack's own shading (vertical
    extension of the pack's last clean rows), the Italian greys are matched to the pack's slightly darker greys, the
    Italian 1-px hard shadow is dropped and the glow of the pack (black, ~3 px fade, fitted on the pack's box outlines)
    is generated for the new art; the 'N' badges are redrawn as clean polygon letters (the Italian 5x5 N: 1-px stems,
    45-degree diagonal, 1-px black outline, yellow of the Italian N) with the heavier drop shadow of the pack's 'NEW'.
    The pack's shadow of the old 'NEW' plates just above the seam is cross-faded to the same glow model."""
    X0, X1, Y0, Y1, SEAM = 102, 157, 92, 111, 99
    reg = low[Y0:Y1, X0:X1].copy()
    reg[(reg[..., :3].max(-1) < 12) & (reg[..., 3] < 250)] = 0           # the Italian hard shadow
    stems = (109, 126, 143)
    for sx in stems:                                                      # the N badges are redrawn
        reg[100 - Y0:107 - Y0, sx - 1 - X0:sx + 6 - X0] = 0
    pad = np.pad(reg, ((1, 1), (1, 1), (0, 0)), mode='edge')
    art = crisp_up(quantize(pad, 16.0), 0.45, 12.0)[K:-K, K:-K]
    r, g, b = art[..., 0], art[..., 1], art[..., 2]
    grey = (np.abs(r - g) < 4) & (np.abs(g - b) < 4) & (g > 60) & (g < 235)
    art[..., 0] = np.where(grey, r * 0.978, r)                            # the pack's greys (measured) are a bit darker
    art[..., 1] = np.where(grey, g * 0.965, g)
    art[..., 2] = np.where(grey, b * 0.962, b)
    ys0 = (SEAM - Y0) * K
    art[:ys0] = 0
    pk = out[Y0 * K:Y1 * K, X0 * K:X1 * K]
    ref_row = pk[ys0 - 3:ys0 - 1].mean(0)                                 # the pack's shading just above the seam
    ref_row[..., :3] = cv2.GaussianBlur(ref_row[None, :, :3], (0, 0), sigmaX=1.5)[0]
    face = grey[ys0:ys0 + K] & (art[ys0:ys0 + K, :, 3] > 0)
    for yy in range(K):
        fy = face[yy] & (ref_row[:, 3] > 250) & (ref_row[:, :3].max(-1) > 100)
        art[ys0 + yy][fy, :3] = ref_row[fy, :3]
    H, W = art.shape[:2]
    nfill = np.zeros((H, W), np.float32)
    for sx in stems:
        nfill = np.maximum(nfill, raster_polys(n_polys(sx), (H, W), (X0 * K, Y0 * K)))
    nout = disk_dilate(nfill, 4.0)
    pack_sil = np.zeros((H, W), np.float32)
    pack_sil[:ys0] = (pk[:ys0, :, 3] > 200)
    sil = np.maximum(np.maximum(art[..., 3] / 255, nout), pack_sil)
    glow = blur(shift(disk_dilate(sil, 0.5), 0, 1.5), 2.2)                # the pack's glow around its icons
    drop = blur(shift(nout, 0.0, 3.0), 2.4) * 0.9                         # the heavier shadow of the pack's 'NEW'
    ga = np.clip(np.maximum(glow, drop), 0, 1)
    layer = np.zeros((H, W, 4), np.float32)
    over(layer, (0, 0, 0), ga)
    over_rgba(layer, art, 0, 0)
    over(layer, (0, 0, 0), nout)
    over(layer, (253, 255, 0), nfill)
    out[Y0 * K + ys0:Y1 * K, X0 * K:X1 * K] = layer[ys0:]
    band = 12
    pkb = out[Y0 * K + ys0 - band:Y0 * K + ys0, X0 * K:X1 * K]
    glow_only = (pkb[..., :3].max(-1) < 60) & (pkb[..., 3] < 250)
    w = ((np.arange(band) + 0.5) / band)[:, None]
    pkb[..., 3] = np.where(glow_only, pkb[..., 3] * (1 - w) + ga[ys0 - band:ys0] * 255 * w, pkb[..., 3])


def build_trnsmt01(low, hd):
    """'NEW' -> 'NUOVO' (orange button); under the three box icons 'NEW' -> 'N' (trnsmt_strip)."""
    out = hd.copy()
    new_button(out)
    trnsmt_strip(out, low)
    return out


# ---------------------------------------------------------------- icon06 (card album / duel icons)
def warp_piece(dst, src, sx, sy, tx, ty):
    """composite src (RGBA float) scaled by (sx, sy) and moved to (tx, ty) onto dst (premultiplied cubic)."""
    M = np.float32([[sx, 0, tx], [0, sy, ty]])
    p = cv2.warpAffine(prem(src), M, (dst.shape[1], dst.shape[0]), flags=cv2.INTER_CUBIC, borderValue=0)
    p = np.clip(p, 0, 255)
    p[..., :3] = np.minimum(p[..., :3], p[..., 3:])
    a = p[..., 3:4]
    over_rgba(dst, np.concatenate([np.where(a > 0, p[..., :3] * 255 / np.maximum(a, 1e-6), 0), a], -1), 0, 0)


def build_icon06(low, hd):
    """'NEW' tile -> 'N' tile.  The Italian tile shows the whole sunburst and card with a small N at the bottom
    right: the hidden lower half of the pack's tile is its upper half mirrored around the card's centre line
    (the sunburst and the card are symmetric), with the tile's drop shadow, and the pack's own N (its yellow
    glyph with the black outline, cut out of 'NEW') is scaled (uniformly, native proportions) into the Italian N's place."""
    out = hd.copy()
    T = hd[0:64, 0:64].copy()
    T[29:57] = T[27::-1]
    T[57:64] = 0
    sh = blur(shift(T[..., 3] / 255, 1, 3), 1.0) * 0.72
    tile = np.zeros_like(T)
    over(tile, (6, 4, 2), sh)
    over_rgba(tile, T, 0, 0)
    # the pack's N: everything in its box that is not the orange tile
    src = hd[30:59, 1:23].copy()
    r, g, b = src[..., 0], src[..., 1], src[..., 2]
    yellow = (r > 190) & (g > 190) & (b < 140)
    orange = (r > 170) & (g > 70) & (b < 90) & ~yellow
    m = (~orange & (src[..., 3] > 0)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    m = (lab == 1 + st[1:, cv2.CC_STAT_AREA].argmax()).astype(np.float32)
    src[..., 3] *= blur(m, 0.5)
    s = 28 / 27                               # ONE uniform scale (native proportions): the pack's N (box 2..22 x 31..58,
    # centre (12, 44.5)) as tall as the Italian N (28 px) and centred on the Italian N box (28..52, 28..56)
    warp_piece(tile, src, s, s, 40 - 11 * s, 42 - 14.5 * s)
    out[0:64, 0:64] = tile
    return out


# ---------------------------------------------------------------- ocglist (card album: flags / format icons)
def build_ocglist(low, hd):
    """The pack only has this sheet at 1:1 (the American one with 'OCG' - the same pixel art, nothing was enlarged), so
    the Italian/European sheet ('TCG') is the plain nearest-x4 enlargement of its own pixels: the pixel art (flags,
    controller, cards, format icons) stays exactly as drawn, square steps and all; pixels with alpha 0 stay black."""
    return nn(low)


# ---------------------------------------------------------------- s_pack (shop: booster packs sheet)
def build_s_pack(low, hd):
    """'1 Pack' and 'Sorry' are absent in the Italian sheet, 'SOLD OUT' -> 'ESAURITE'.
    The pack's labels are flat colours: the text-free column x=20 of each band is repeated over the text (the
    white band only up to its own right edge), 'ESAURITE' is PT Sans Bold (the best match of the pack's 'SOLD OUT'
    letters) at the pack's cap height (38.5 px), baseline of the pack's text, in the pack's red."""
    out = hd.copy()
    for y0, y1, x1 in ((764, 796, 258), (896, 928, 258), (928, 984, 254)):   # blue header, red header, white band
        out[y0:y1, 20:x1] = out[y0:y1, 20:21]
    red = out[990, 100].copy()                               # a50a08, the pack's text and box red
    region = (0, 928, 272, 984)
    cov = word_cov(SP_TEXT, PT_SANS_BOLD, 37.5, SP_X[0], SP_X[1], 975.0, region, ref='H', dil=0.5, squeeze_max=0.34 if LANG == 'de' else 0.10)   # de: AUSVERKAUFT (11 letters) in 58 px, as the original is condensed
    over(out, red, cov, region)
    return out


# ---------------------------------------------------------------- main
TEXTURES_EN = [
    ('all_e__icon04', 'deck/all_e.ehp', 'icon04.gim', 'ui/limited.png', build_icon04_en, None),
    ('all_e__panel', 'shop/all_e.ehp', 'panel.gim', 'shop/store_purchasing_ui.png', build_panel, None),
    ('always_bri_eng__pda_pack01', 'field/always_bri_eng.ehp', 'pda_pack01.gim', 'ui/menu/menu_icons.png', build_icon04_en, None),
]
TEXTURES_FR = [
    (f'all_{LL}__icon04', f'deck/all_{LL}.ehp', 'icon04.gim', 'ui/limited.png', build_icon04_fr, 'deck/all_e.ehp'),
    (f'all_{LL}__s_pack', f'shop/all_{LL}.ehp', 's_pack.gim', 'shop/packs/all_packs.png', build_s_pack, None),
    (f'all_{LL}__panel', f'shop/all_{LL}.ehp', 'panel.gim', 'shop/store_purchasing_ui.png', build_panel, None),
]
TEXTURES = [
    # id, file, member, English HD sheet (relative to PACK_US), builder
    ('all_i__icon04', 'deck/all_i.ehp', 'icon04.gim', 'ui/limited.png', build_icon04),
    ('all_i__s_pack', 'shop/all_i.ehp', 's_pack.gim', 'shop/packs/all_packs.png', build_s_pack),
    ('all_i__panel', 'shop/all_i.ehp', 'panel.gim', 'shop/store_purchasing_ui.png', build_panel),
    ('always_bri_ita__pda_pack01', 'field/always_bri_ita.ehp', 'pda_pack01.gim', 'ui/menu/menu_icons.png',
     build_pda_pack01),
    ('cardalbum__ocglist_i', 'database/cardalbum.ehp', 'ocglist_i.gim', None, build_ocglist),
    ('cardalbum__icon06_i', 'database/cardalbum.ehp', 'icon06_i.gim', 'ui/duels/icons.png', build_icon06),
    ('title_menu_i__mein_menu00', 'title_menu/title_menu_i.ehp', 'mein_menu00.gim',
     'ui/misc/000000002176ef40522b3050.png', build_mein_menu00),
    ('title_menu_i__trnsmt01', 'title_menu/title_menu_i.ehp', 'trnsmt01.gim',
     'ui/misc/00000000836977a003b3d6f2.png', build_trnsmt01),
]


def main():
    fam = common.Family('fogli_icone', sys.argv)
    global EN_LOW
    for tex_id, file, member, ref, build, *en in ([t + (None,) if len(t) == 5 else t for t in TEXTURES] if LANG == 'it' else TEXTURES_EN if LANG == 'en' else TEXTURES_FR):
        if en and en[0]:
            EN_LOW = arr(common.texture(fam.usrdir, en[0], member)[0])
        low, hash_ = common.texture(fam.usrdir, file, member)
        hd = arr(common.reference(fam.pack_us, ref)) if ref else None
        assert hd is None or (hd.shape[1] == low.size[0] * K and hd.shape[0] == low.size[1] * K), tex_id
        out = build(arr(low), hd)
        fam.save(tex_id, img(out), hash_, low)
    fam.finish()


if __name__ == '__main__':
    main()
