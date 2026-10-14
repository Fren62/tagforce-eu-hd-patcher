"""deck_screens: HD Italian tabs/labels of deck editor, shop, lab (Cassa, Fusion, Side, Deck, Affitto, Laboratorio,
Convertitore, Tipi di Carte Posseduti, Carte Comprate / Tipi di Carte com..., INVIO key, plain bars).

    python3 -I deck_screens.py USRDIR PACK_US OUT

Every texture is rebuilt at 4x from the Italian original (common.texture), never from the work folders:
  - coloured tabs: the original pixels with the word and white box wiped, upscaled (nearest + light premultiplied
    blur, so the European frame geometry is kept exactly); crisp rounded white box; word redrawn with SF Pro
    (variable, weight 850, width axis fitted) placed on the Italian letters, white fill + drop shadow like the HD
    tab words. "Side"/"Deck" (same word in Italian) reuse the English HD letters (ui/deckedit).
  - gold-framed brown boxes: the English HD "Kind of possession card" box (frame, white box, START, ?) with the
    English words wiped by the frame's own vertical profile; the plain bars and the shop brown box are assembled
    from the same HD frame (caps + body); the shop blue tab is the HD "Purchase Card" tab (identical geometry).
  - the plain bar d_window00034 is identical to the European English one: English HD image as is.
  - INVIO: letters vectorised from the original (bicubic + smoothing + re-threshold), shadow refitted.
Words are fitted glyph by glyph (fit_text + refine_glyphs) to the white coverage of the original text."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import alt_font  # noqa: nessun font Apple
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import common

S = common.SCALE
FONTS = '/System/Library/Fonts/'
SUPP = FONTS + 'Supplemental/'


# ---------------------------------------------------------------- image helpers
def arr(im):
    return np.asarray(im.convert('RGBA'), np.float32) / 255.0


def img(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8), 'RGBA')


def premul(a):
    b = a.copy()
    b[..., :3] *= b[..., 3:]
    return b


def unpremul(b):
    a = b.copy()
    al = b[..., 3:]
    a[..., :3] = np.where(al > 1e-4, b[..., :3] / np.maximum(al, 1e-4), 0)
    return np.clip(a, 0, 1)


def blur(a, sigma):
    """gaussian blur of a float HxWxC array (premultiplied when RGBA)."""
    import cv2
    if sigma <= 0:
        return a
    return cv2.GaussianBlur(a, (0, 0), sigma, borderType=cv2.BORDER_REPLICATE)


def _epx(a):
    """Scale2x/EPX of a float RGBA array: edge-preserving 2x for flat pixel art (straight edges stay straight, corners round)."""
    q = np.clip(np.rint(a * 255), 0, 255).astype(np.uint8)
    q[q[..., 3] == 0] = 0                                   # transparent pixels compare equal whatever their colour
    pk = q.view(np.uint32)[..., 0]
    P = np.pad(pk, 1, mode='edge')
    A, B, C, D = P[:-2, 1:-1], P[1:-1, 2:], P[1:-1, :-2], P[2:, 1:-1]
    pp = np.pad(a, ((1, 1), (1, 1), (0, 0)), mode='edge')
    cA, cB, cC, cD = pp[:-2, 1:-1], pp[1:-1, 2:], pp[1:-1, :-2], pp[2:, 1:-1]
    H, W = pk.shape
    out = np.repeat(np.repeat(a, 2, 0), 2, 1).copy()
    m1 = (C == A) & (C != D) & (A != B)
    m2 = (A == B) & (A != C) & (B != D)
    m3 = (D == C) & (D != B) & (C != A)
    m4 = (B == D) & (B != A) & (D != C)
    out[0::2, 0::2] = np.where(m1[..., None], cA, a)
    out[0::2, 1::2] = np.where(m2[..., None], cB, a)
    out[1::2, 0::2] = np.where(m3[..., None], cC, a)
    out[1::2, 1::2] = np.where(m4[..., None], cD, a)
    return out


def upscale(low, sigma=0.55):
    """crisp 4x upscale of flat UI art: EPX twice (no nearest+blur softness), then a very light premultiplied blur for antialiasing."""
    a = arr(low)
    a = _epx(_epx(a))
    return unpremul(blur(premul(a), sigma))


def over(dst, src):
    """alpha-composite float RGBA src over dst (straight alpha)."""
    sa = src[..., 3:]
    da = dst[..., 3:]
    oa = sa + da * (1 - sa)
    oc = np.where(oa > 1e-5, (src[..., :3] * sa + dst[..., :3] * da * (1 - sa)) / np.maximum(oa, 1e-5), 0)
    return np.concatenate([oc, oa], -1)


def paint(dst, cov, color):
    """paint a solid color with coverage cov (HxW, 0..1) over dst."""
    src = np.zeros(dst.shape, np.float32)
    src[..., :3] = np.asarray(color, np.float32)[:3] / 255.0
    src[..., 3] = np.clip(cov, 0, 1)
    return over(dst, src)


def rrect(h, w, x0, y0, x1, y1, r, soft=0.7):
    """coverage of an antialiased rounded rectangle [x0,x1)x[y0,y1) (HD pixel units)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32) + 0.5
    cx = np.clip(xx, x0 + r, x1 - r)
    cy = np.clip(yy, y0 + r, y1 - r)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) - r
    return np.clip(0.5 - d / (2 * soft), 0, 1)


# ---------------------------------------------------------------- text engine
class Font:
    def __init__(self, path, index=0, axes=None, ref=200):
        self.f = ImageFont.truetype(path, ref, index=index)
        if axes:
            self.f.set_variation_by_axes(axes)
        self.ref = ref
        self.cache = {}

    def glyph(self, ch):
        """(L mask, ox, oy): mask pixel (u,v) sits at pen + (u+ox, v+oy) in reference units (baseline at y=0)."""
        if ch not in self.cache:
            x0, y0, x1, y1 = self.f.getbbox(ch, anchor='ls')
            pad = 12
            m = Image.new('L', (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), 0)
            ImageDraw.Draw(m).text((pad - x0, pad - y0), ch, font=self.f, fill=255, anchor='ls')
            self.cache[ch] = (m, x0 - pad, y0 - pad, (x0, y0, x1, y1))
        return self.cache[ch]

    def adv(self, ch):
        return self.f.getlength(ch)


class VarFont:
    """SF Pro (variable): fixed weight, width axis chosen per word by fit_text."""

    def __init__(self, path, weight, opsz=28, wmin=30, wmax=150, ref=200):
        self.path, self.weight, self.opsz, self.wmin, self.wmax, self.ref = path, weight, opsz, wmin, wmax, ref
        self.cache = {}

    def variant(self, width):
        width = round(width, 2)
        if width not in self.cache:
            self.cache[width] = Font(self.path, 0, [width, self.opsz, 400, self.weight], self.ref)
        return self.cache[width]


class Text:
    """a word laid out glyph by glyph: pen x (HD px) and horizontal scale per glyph, shared scale k and baseline."""

    def __init__(self, font, word, k, base, x0, hscale=1.0, track=0.0):
        self.font, self.word, self.k, self.base = font, word, k, base
        self.xs, self.hs = [], []
        x = x0
        for ch in word:
            self.xs.append(x)
            self.hs.append(hscale)
            x += (font.adv(ch) * k * hscale + track) if ch != ' ' else font.adv(' ') * k * hscale + track
        self.idx = [i for i, ch in enumerate(word) if ch != ' ']

    def render(self, h, w, dx=0.0, dy=0.0, only=None):
        """fill coverage HxW (HD px), the layout shifted by (dx, dy)."""
        cov = np.zeros((h, w), np.float32)
        for i in (self.idx if only is None else only):
            m, ox, oy, _ = self.font.glyph(self.word[i])
            kx, ky = self.k * self.hs[i], self.k
            X, Y = self.xs[i] + dx, self.base + dy
            dx0 = int(np.ceil(X + ox * kx))
            dy0 = int(np.ceil(Y + oy * ky))
            dx1 = int(np.floor(X + (ox + m.width) * kx))
            dy1 = int(np.floor(Y + (oy + m.height) * ky))
            if dx1 <= dx0 or dy1 <= dy0:
                continue
            box = (max(0.0, (dx0 - X) / kx - ox), max(0.0, (dy0 - Y) / ky - oy),
                   min(float(m.width), (dx1 - X) / kx - ox), min(float(m.height), (dy1 - Y) / ky - oy))
            g = np.asarray(m.resize((dx1 - dx0, dy1 - dy0), Image.LANCZOS, box=box), np.float32) / 255.0
            # clip to canvas
            sx0, sy0 = max(0, -dx0), max(0, -dy0)
            ex0, ey0 = max(0, dx0), max(0, dy0)
            ex1, ey1 = min(w, dx1), min(h, dy1)
            if ex1 <= ex0 or ey1 <= ey0:
                continue
            sub = g[sy0:sy0 + ey1 - ey0, sx0:sx0 + ex1 - ex0]
            cov[ey0:ey1, ex0:ex1] = 1 - (1 - cov[ey0:ey1, ex0:ex1]) * (1 - sub)
        return cov

    def ink(self, i):
        """HD x extent of glyph i's ink."""
        _, _, _, (x0, y0, x1, y1) = self.font.glyph(self.word[i])
        kx = self.k * self.hs[i]
        return self.xs[i] + x0 * kx, self.xs[i] + x1 * kx


def coverage_target(low, rect, bg, white=255.0):
    """per-pixel white-fill coverage of the original text inside rect=(x0,y0,x1,y1) (low px):
    (min channel - bg min channel) / (white - bg min channel)."""
    a = np.asarray(low.convert('RGBA'), np.float32)
    x0, y0, x1, y1 = rect
    m = a[y0:y1, x0:x1, :3].min(2)
    b = min(bg[:3])
    return np.clip((m - b) / (white - b), 0, 1)


def ink_extent(target, thr=0.35):
    """sub-pixel horizontal extent (low px, relative to the target origin) of the text coverage."""
    col = target.max(0)
    xs = np.nonzero(col > thr)[0]
    x0, x1 = xs[0], xs[-1] + 1
    # refine by the partial coverage of the border columns
    l = x0 - (col[x0 - 1] if x0 > 0 else 0)
    r = x1 + (col[x1] if x1 < len(col) else 0)
    return float(l), float(r)


def natural(font, word, k, hscale=1.0, track=0.0):
    t = Text(font, word, k, 0, 0, hscale, track)
    return t.ink(t.idx[0])[0], t.ink(t.idx[-1])[1]


def fit_text(font, word, target, rect, cap, baseline, extent=None, iters=0, weight_reg=40.0, track=0.0,
             capchar=None, fit_k=True, wmin=75, space_reg=0.05, max_shift=2.0):
    """lay out word so that its 4x box-downscaled fill matches target (low-res coverage of rect).
    cap: height (low px) of capitals (or of capchar), baseline: low-px row (absolute) of the baseline;
    extent: (left, right) absolute low px of the ink, default measured on target.
    The font is condensed with its width axis when it has one (font.widths), else scaled horizontally."""
    x0, y0, x1, y1 = rect
    W, H = (x1 - x0) * S, (y1 - y0) * S
    if extent is None:
        l, r = ink_extent(target)
        extent = (l + x0, r + x0)
    tl, tr = (extent[0] - x0) * S, (extent[1] - x0) * S
    ch = capchar or next((c for c in word if c.isupper()), word[0])

    def kof(f):
        return cap * S / -f.f.getbbox(ch, anchor='ls')[1]

    f = font
    if hasattr(font, 'variant'):          # variable width: pick the width giving the target extent (>= wmin)
        lo, hi = wmin, font.wmax
        for _ in range(14):
            mid = (lo + hi) / 2
            g = font.variant(mid)
            a, b = natural(g, word, kof(g), 1.0, track)
            if b - a > tr - tl:
                hi = mid
            else:
                lo = mid
        f = font.variant((lo + hi) / 2)
    k = kof(f)
    a, b = natural(f, word, k, 1.0, track)
    hs = (tr - tl) / (b - a)               # ~1 unless the width axis hit wmin (then squeeze horizontally)
    a, b = natural(f, word, k, hs, track)
    p = dict(k=k, base=(baseline - y0) * S, x0=tl - a, hscale=hs, track=track)
    x_ref = None

    def err(t):
        r = t.render(H, W)
        r = r.reshape(H // S, S, W // S, S).mean((1, 3))
        e = ((r - target) ** 2).sum()
        hm = np.mean([t.hs[i] for i in t.idx])
        e += weight_reg * sum((t.hs[i] / hm - 1) ** 2 for i in t.idx)
        if x_ref is not None:              # keep the spacing regular: neighbour glyphs move together
            d = [t.xs[i] - x_ref[i] for i in t.idx]
            e += space_reg * sum((d[j] - d[j - 1]) ** 2 for j in range(1, len(d)))
        return e

    def make(q):
        return Text(f, word, q['k'], q['base'], q['x0'], q['hscale'], q['track'])

    best = err(make(p))
    steps = dict(k=0.01 * k, base=1.0, x0=1.0, hscale=0.02, track=0.5)
    if not fit_k:
        steps.pop('k')
    for _ in range(3):
        improved = True
        while improved:
            improved = False
            for key, st in steps.items():
                for sgn in (1, -1):
                    q = dict(p)
                    q[key] = p[key] + sgn * st
                    e = err(make(q))
                    if e < best - 1e-6:
                        best, p, improved = e, q, True
        steps = {kk: v / 2 for kk, v in steps.items()}
    t = make(p)
    x_ref = list(t.xs)
    best = err(t)
    for it in range(iters):                # per glyph: move / rescale while it helps (bounded)
        for i in t.idx:
            improved = True
            while improved:
                improved = False
                for dx, dh in [(2, 0), (-2, 0), (1, 0), (-1, 0), (0.5, 0), (-0.5, 0), (0, 0.02), (0, -0.02),
                               (1, -0.02), (-1, 0.02)]:
                    ox, oh = t.xs[i], t.hs[i]
                    t.xs[i] += dx
                    t.hs[i] *= (1 + dh)
                    ok = abs(t.xs[i] - x_ref[i]) <= max_shift and abs(t.hs[i] / hs - 1) <= 0.08
                    e = err(t) if ok else 1e9
                    if e < best - 1e-6:
                        best, improved = e, True
                    else:
                        t.xs[i], t.hs[i] = ox, oh
    return t, best


def refine_glyphs(t, target, rect, iters=3, gap_reg=0.3, width_reg=30.0, max_w=0.2):
    """per-glyph refinement that keeps the font's spacing: glyphs may get wider/narrower (bounded) and blocks of
    glyphs may slide, but every change of an inter-glyph gap is penalised, so letters follow the original
    positions without holes or collisions."""
    x0, y0, x1, y1 = rect
    W, H = (x1 - x0) * S, (y1 - y0) * S
    idx = t.idx
    h0 = [t.hs[i] for i in idx]

    def gaps():
        g = []
        for j in range(1, len(idx)):
            g.append(t.ink(idx[j])[0] - t.ink(idx[j - 1])[1])
        return g
    g0 = gaps()

    def err():
        r = t.render(H, W).reshape(H // S, S, W // S, S).mean((1, 3))
        e = ((r - target) ** 2).sum()
        e += gap_reg * sum((a - b) ** 2 for a, b in zip(gaps(), g0))
        e += width_reg * sum((t.hs[i] / h - 1) ** 2 for i, h in zip(idx, h0))
        return e

    def shift(js, d):
        for j in js:
            t.xs[idx[j]] += d

    best = err()
    n = len(idx)
    for _ in range(iters):
        for step in (2.0, 1.0, 0.5):
            improved = True
            while improved:
                improved = False
                for j in range(n):
                    # 1) slide glyphs j..end (changes one gap)   2) widen glyph j, pushing the following ones
                    for kind in ('slide', 'widen', 'move'):
                        for sgn in (1, -1):
                            save = (list(t.xs), list(t.hs))
                            if kind == 'slide':
                                shift(range(j, n), sgn * step)
                            elif kind == 'move':
                                shift([j], sgn * step)
                            else:
                                i = idx[j]
                                l, r = t.ink(i)
                                f = 1 + sgn * 0.01 * step
                                if abs(t.hs[i] * f / h0[j] - 1) > max_w:
                                    continue
                                t.hs[i] *= f
                                nl, nr = t.ink(i)
                                t.xs[i] += l - nl                     # keep the left ink edge
                                shift(range(j + 1, n), (nr - nl) - (r - l))
                            e = err()
                            if e < best - 1e-6:
                                best, improved = e, True
                            else:
                                t.xs, t.hs = save
    return t, best


def text_layer(h, w, t, ox, oy, fill=(255, 255, 255), shadow=None, shadow_off=(3, 3), shadow_blur=0.6, embolden=0.0):
    """RGBA float layer (h x w) with the word t rendered at offset (ox,oy) HD px: optional drop shadow then fill."""
    cov = t.render(h, w, ox, oy)
    if embolden > 0:
        import cv2
        r = int(np.ceil(embolden))
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
        cov = np.maximum(cov, cv2.dilate(cov, k) * min(1.0, embolden / r))
    layer = np.zeros((h, w, 4), np.float32)
    if shadow is not None:
        sdx, sdy = shadow_off
        sh = np.zeros_like(cov)
        sh[max(0, sdy):h + min(0, sdy), max(0, sdx):w + min(0, sdx)] = cov[max(0, -sdy):h - max(0, sdy), max(0, -sdx):w - max(0, sdx)]
        sh = blur(sh, shadow_blur) if shadow_blur else sh
        layer = paint(layer, sh * (shadow[3] / 255.0 if len(shadow) > 3 else 1.0), shadow)
    layer = paint(layer, cov, fill)
    return layer, cov


# ---------------------------------------------------------------- fonts / styles
def fonts():
    return dict(
        tab=VarFont(FONTS + 'SFNS.ttf', 850),        # deck-editor tab words (HD: heavy humanist, white + drop shadow)
        label=VarFont(FONTS + 'SFNS.ttf', 700),      # boxed labels ("Kind of possession card", "Purchase Card" style)
    )


def shade(c, f):
    return tuple(int(round(v * f)) for v in c[:3])


# ---------------------------------------------------------------- tabs (Cassa, Fusion, Side, Deck, Affitto, ...)
TAB_ROWS = (3, 15)          # interior rows of every tab (fill colour, text and white box)


def tab(low, word, F, box_x0, right, text_x1=None, hd_text=None, cap=10, baseline=13.5):
    """tab with a coloured interior (rows 3..14, x 3..right), a white box [box_x0, right) and a word.
    Crisp EPX upscale of the Italian frame (geometry kept exactly), clean white box, and the word set with ui_it/tabword.py:
    one font (SF Pro Rounded Black), regular letters, outline + hard shadow like the mod's tab words."""
    import tabword
    a = np.asarray(low.convert('RGBA')).copy()
    fill = tuple(int(v) for v in a[TAB_ROWS[0], 5, :3])
    y0, y1 = TAB_ROWS
    a[y0:y1, 3:right + 1, :3] = fill
    a[y0:y1, 3:right + 1, 3] = 255
    H, W = low.height * S, low.width * S
    hd = upscale(Image.fromarray(a, 'RGBA'))
    hd = paint(hd, rrect(H, W, box_x0 * S, y0 * S, right * S, y1 * S, 3.0), (255, 255, 255))
    lay, info = tabword.render_tab_word(word, fill, (H, W), 13, (text_x1 or box_x0) * S - 5, 54, cap=TAB_CAP)
    TAB_INFO[word] = info
    return over(hd, lay)


TAB_INFO = {}
TAB_CAP = 44.0      # common letter size of the deck-editor / shop tabs (Deck, Side, Cassa, Affitto, ...): longer words go below it


def hd_fill(ref, x0, x1, y0, y1):
    """median colour (0-255) of an HD reference region (interior fill around the English word)."""
    r = np.asarray(ref.convert('RGBA'))[y0:y1, x0:x1, :3].reshape(-1, 3).astype(np.float32)
    # keep the pixels close to the dominant colour (drop letters / shadow)
    med = np.median(r, 0)
    keep = np.abs(r - med).max(1) < 40
    return tuple(np.median(r[keep], 0))


# ---------------------------------------------------------------- gold-framed brown boxes
def gold_rebuild(hd, x0, x1, y0, y1, clean_x0, clean_x1):
    """replace hd[y0:y1, x0:x1] by the vertical profile (per-row median) of the clean columns [clean_x0, clean_x1)."""
    prof = np.median(hd[y0:y1, clean_x0:clean_x1], 1)
    hd[y0:y1, x0:x1] = prof[:, None, :]
    return hd


def gold_bar(src, H, x0, x1, left=True, right=True):
    """HD gold-framed brown bar spanning low columns [x0, x1), built from the frame of the English HD
    "Kind of possession card" box (d_window00033: frame rows 0..21 + shadow, left cap at its low columns 1..4,
    right cap at 145..150, plain body column 144)."""
    s = arr(src)
    hd = np.zeros((H, x1 * S, 4), np.float32)
    a = x0 + 4 if left else x0
    b = x1 - 5 if right else x1
    if left:
        hd[:, x0 * S:a * S] = s[:H, 1 * S:5 * S]
    body = np.median(s[:H, 144 * S:145 * S], 1, keepdims=True)
    hd[:, a * S:b * S] = np.repeat(body, (b - a) * S, 1)
    if right:
        hd[:, b * S:x1 * S] = s[:H, 146 * S:151 * S]
    return hd


def label_text(hd, low, word, F, rect, cap, baseline, bg, shadow, font='label', shadow_off=(3, 3), extent=None):
    H, W = hd.shape[:2]
    tgt = coverage_target(low, rect, bg)
    t, _ = fit_text(F[font], word, tgt, rect, cap, baseline, extent=extent)
    t, _ = refine_glyphs(t, tgt, rect)
    lay, _ = text_layer(H, W, t, rect[0] * S, rect[1] * S, shadow=shadow, shadow_off=shadow_off)
    return over(hd, lay)


def paste_low(hd, low, x0, y0, x1, y1):
    """copy the nearest-upscaled original pixels of [x0,x1)x[y0,y1) (tiny details such as atlas specks)."""
    up = arr(low)[y0:y1, x0:x1]
    hd[y0 * S:y1 * S, x0 * S:x1 * S] = np.repeat(np.repeat(up, S, 0), S, 1)
    return hd


# ---------------------------------------------------------------- INVIO key caption
def key_caption(low):
    """INVIO: big white rounded capitals (22 px tall, 4-5 px strokes) with a soft black drop shadow, on a transparent
    background. The letters are large and clean enough to be vectorised from the original itself: white coverage
    upscaled (bicubic), smoothed and re-thresholded into crisp edges; the shadow is then refitted on the original alpha."""
    import cv2
    H, W = low.height * S, low.width * S
    a = np.asarray(low.convert('RGBA'), np.float32) / 255.0
    cov = a[..., 0] * a[..., 3]                       # white contribution (premultiplied)
    pad = 4
    p = np.pad(cov, pad)
    u = cv2.resize(p, (p.shape[1] * S, p.shape[0] * S), interpolation=cv2.INTER_CUBIC)[pad * S:-pad * S, pad * S:-pad * S]
    u = cv2.GaussianBlur(u, (0, 0), 2.0)
    c = np.clip((u - 0.5) * 6.4 + 0.5, 0, 1)
    best = None
    for dx in (2, 3, 4, 5, 6):
        for dy in (5, 6, 7, 8, 9, 10):
            sh0 = np.zeros_like(c)
            sh0[dy:, dx:] = c[:-dy, :-dx]
            for sg in (5.0, 6.0, 7.0, 8.0):
                sh1 = blur(sh0, sg)
                for op in (0.75, 0.85, 0.95, 1.05):
                    al = c + np.clip(sh1 * op, 0, 1) * (1 - c)
                    e = np.abs(al.reshape(low.height, S, low.width, S).mean((1, 3)) - a[..., 3]).mean()
                    if best is None or e < best[0]:
                        best = (e, dx, dy, sg, op)
    _, dx, dy, sg, op = best
    sh = np.zeros_like(c)
    sh[dy:, dx:] = c[:-dy, :-dx]
    sh = np.clip(blur(sh, sg) * op, 0, 1)
    out = np.zeros((H, W, 4), np.float32)
    out = paint(out, sh, (0, 0, 0))
    return paint(out, c, (255, 255, 255))


# ---------------------------------------------------------------- the family
DECK = 'deck/all_i.ehp'
TEX = {
    'all_i__d_window00008': (DECK, 'd_window00008.gim'),
    'all_i__d_window00016': (DECK, 'd_window00016.gim'),
    'all_i__d_window00024': (DECK, 'd_window00024.gim'),
    'all_i__d_window00031': (DECK, 'd_window00031.gim'),
    'all_i__d_window00033': (DECK, 'd_window00033.gim'),
    'all_i__d_window00034': (DECK, 'd_window00034.gim'),
    'all_i__d_window00062': (DECK, 'd_window00062.gim'),
    'all_i__d_window00120': (DECK, 'd_window00120.gim'),
    'all_i__d_window00051': (DECK, 'd_window00051.gim'),
    'all_i__d_window00101': (DECK, 'd_window00101.gim'),
    'all_i__tab_title': ('shop/all_i.ehp', 'tab_title.gim'),
    'conv_machine__window_i0009': ('labo/conv_machine.ehp', 'window_i0009.gim'),
    'conv_machine__window_i0022': ('labo/conv_machine.ehp', 'window_i0022.gim'),
    'rental__window_i0015': ('labo/rental.ehp', 'window_i0015.gim'),
    'rental__window_i0026': ('labo/rental.ehp', 'window_i0026.gim'),
    'password__key_i0027': ('labo/password.ehp', 'key_i0027.gim'),
}
REF = dict(
    trunk='ui/deckedit/00000000a33778db85d8f4f8.png',
    fusion='ui/deckedit/0000000065037c929f671d8d.png',
    side='ui/deckedit/000000006c2037fcdf435532.png',
    deck='ui/deckedit/00000000f1fc5e4cf83d4357.png',
    possession='ui/deckedit/000000003416c1579e1b269c.png',
    bar='ui/deckedit/00000000894a59a6c4fc9f5c.png',
    purchase='shop/purchase_text_box.png',
    shopui='shop/store_purchasing_ui.png',
)


def build(tid, low, pack, F):
    H, W = low.height * S, low.width * S
    ref = lambda k: common.reference(pack, REF[k])
    if tid in ('all_i__d_window00008', 'all_i__d_window00062'):
        return tab(low, 'Cassa', F, 38, 87)
    if tid == 'all_i__d_window00016':
        return tab(low, 'Fusion', F, 37, 56)
    if tid in ('all_i__d_window00024', 'all_i__d_window00120'):
        r = ref('side')
        return tab(low, 'Side', F, 37, 56, hd_text=(r, hd_fill(r, 12, 148, 12, 60)))
    if tid == 'all_i__d_window00031':
        r = ref('deck')
        return tab(low, 'Deck', F, 37, 56, hd_text=(r, hd_fill(r, 12, 148, 12, 60)))
    if tid in ('all_i__d_window00051', 'all_i__d_window00101', 'rental__window_i0026'):
        return tab(low, 'Affitto', F, 45, 56)
    if tid == 'rental__window_i0015':
        return tab(low, 'Laboratorio', F, 57, 92)
    if tid == 'conv_machine__window_i0009':
        return tab(low, 'Convertitore', F, 66, 85)
    if tid == 'all_i__d_window00034':
        return arr(ref('bar'))              # identical to the European English bar: the English HD image as is
    if tid == 'all_i__d_window00033':
        hd = arr(ref('possession'))
        # wipe "Kind of possession card" (its descenders cross the lower frame) with the frame's vertical profile
        hd = gold_rebuild(hd, 18, 107 * S - 1, 16, 90, 144 * S, 146 * S)
        return label_text(hd, low, 'Tipi di Carte Posseduti', F, (4, 3, 107, 19), 9, 15, (61, 53, 35),
                          (26, 22, 14, 255))
    if tid == 'conv_machine__window_i0022':
        hd = gold_bar(ref('possession'), H, 0, 256, left=True, right=True)
        return paste_low(hd, low, 236, 0, 243, 1)          # atlas specks on the top row, as in the original
    if tid == 'all_i__tab_title':
        hd = np.zeros((H, W, 4), np.float32)
        hd[:, :138 * S] = arr(ref('purchase'))[:, :138 * S]   # US "Purchase Card" tab: same geometry
        fb = hd_fill(ref('purchase'), 14, 320, 46, 90)
        hd[11 * S:23 * S, 3 * S:83 * S, :3] = np.array(fb) / 255.0
        hd = label_text(hd, low, 'Carte Comprate', F, (3, 10, 83, 23), 9, 21, (70, 92, 154), (34, 44, 74, 255))
        hd[:, 138 * S:] = over(hd[:, 138 * S:], gold_bar(ref('possession'), H, 138, 256, left=True, right=False)[:, 138 * S:])
        hd = label_text(hd, low, 'Tipi di Carte com', F, (141, 3, 256, 19), 9, 15, (61, 53, 36), (26, 22, 14, 255))
        return paste_low(hd, low, 240, 0, 246, 1)
    if tid == 'password__key_i0027':
        return key_caption(low)             # INVIO
    raise KeyError(tid)


TEX_FR = {   # French: only the textures that differ from English (the others have the same hash and come from the pack)
    'all_f__d_window00008': ('deck/all_f.ehp', 'd_window00008.gim', 'Coffre'),
    'all_f__d_window00062': ('deck/all_f.ehp', 'd_window00062.gim', 'Coffre'),
    'all_f__d_window00051': ('deck/all_f.ehp', 'd_window00051.gim', 'Location'),
    'all_f__d_window00101': ('deck/all_f.ehp', 'd_window00101.gim', 'Location'),
    'rental__window_f0026': ('labo/rental.ehp', 'window_f0026.gim', 'Location'),
    'rental__window_f0015': ('labo/rental.ehp', 'window_f0015.gim', 'Labo'),
    'conv_machine__window_f0009': ('labo/conv_machine.ehp', 'window_f0009.gim', 'Convertisseur'),
    'all_f__d_window00033': ('deck/all_f.ehp', 'd_window00033.gim', 'Types de cartes acquis'),
    'all_f__tab_title': ('shop/all_f.ehp', 'tab_title.gim', None),
    'password__key_f0027': ('labo/password.ehp', 'key_f0027.gim', None),
}


TEX_ES = {   # Spanish: the textures that differ from English (Fusión has the accent: it is not identical even in German)
    'all_s__d_window00008': ('deck/all_s.ehp', 'd_window00008.gim', 'Tronco'),
    'all_s__d_window00062': ('deck/all_s.ehp', 'd_window00062.gim', 'Tronco'),
    'all_s__d_window00016': ('deck/all_s.ehp', 'd_window00016.gim', 'Fusión'),
    'all_s__d_window00051': ('deck/all_s.ehp', 'd_window00051.gim', 'Alquiler'),
    'all_s__d_window00101': ('deck/all_s.ehp', 'd_window00101.gim', 'Alquiler'),
    'rental__window_s0026': ('labo/rental.ehp', 'window_s0026.gim', 'Alquiler'),
    'rental__window_s0008': ('labo/rental.ehp', 'window_s0008.gim', 'Alquiler'),
    'rental__window_s0015': ('labo/rental.ehp', 'window_s0015.gim', 'Laboratorio'),
    'conv_machine__window_s0009': ('labo/conv_machine.ehp', 'window_s0009.gim', 'Conversor'),
    'conv_machine__window_s0026': ('labo/conv_machine.ehp', 'window_s0026.gim', 'Conversor'),
    'conv_machine__window_s0016': ('labo/conv_machine.ehp', 'window_s0016.gim', 'Tronco'),
    'all_s__d_window00033': ('deck/all_s.ehp', 'd_window00033.gim', 'Tipos de carta en posesión'),
    'all_s__tab_title': ('shop/all_s.ehp', 'tab_title.gim', None),
    'password__key_s0027': ('labo/password.ehp', 'key_s0027.gim', None),
}
TEX_DE = {   # German: the textures that differ from English (as fr; 'Fusion', 'Side Deck' etc. have the same hash as English)
    'all_g__d_window00008': ('deck/all_g.ehp', 'd_window00008.gim', 'Truhe'),
    'all_g__d_window00062': ('deck/all_g.ehp', 'd_window00062.gim', 'Truhe'),
    'all_g__d_window00051': ('deck/all_g.ehp', 'd_window00051.gim', 'Miete'),
    'all_g__d_window00101': ('deck/all_g.ehp', 'd_window00101.gim', 'Miete'),
    'rental__window_g0026': ('labo/rental.ehp', 'window_g0026.gim', 'Miete'),
    'rental__window_g0015': ('labo/rental.ehp', 'window_g0015.gim', 'Labor'),
    'conv_machine__window_g0009': ('labo/conv_machine.ehp', 'window_g0009.gim', 'Konverter'),
    'all_g__d_window00016': ('deck/all_g.ehp', 'd_window00016.gim', 'Fusion'),     # same hash as English, but the pack has only an upscale: HD like the other tabs
    'rental__window_g0008': ('labo/rental.ehp', 'window_g0008.gim', 'Miete'),
    'conv_machine__window_g0016': ('labo/conv_machine.ehp', 'window_g0016.gim', 'Truhe'),
    'conv_machine__window_g0026': ('labo/conv_machine.ehp', 'window_g0026.gim', 'Konverter'),
    'all_g__d_window00033': ('deck/all_g.ehp', 'd_window00033.gim', 'Eigene Kartentypen'),
    'all_g__tab_title': ('shop/all_g.ehp', 'tab_title.gim', None),
    'password__key_g0027': ('labo/password.ehp', 'key_g0027.gim', None),
}
TEX_EN = {   # European English: same text as the original; the US pack has only an xBRZ upscale for these hashes
    'all_e__d_window00008': ('deck/all_e.ehp', 'd_window00008.gim', 'Trunk'),
    'all_e__d_window00062': ('deck/all_e.ehp', 'd_window00062.gim', 'Trunk'),
    'all_e__d_window00051': ('deck/all_e.ehp', 'd_window00051.gim', 'Rental'),
    'all_e__d_window00101': ('deck/all_e.ehp', 'd_window00101.gim', 'Rental'),
    'rental__window_e0026': ('labo/rental.ehp', 'window_e0026.gim', 'Rental'),
    'rental__window_e0008': ('labo/rental.ehp', 'window_e0008.gim', 'Rental'),
    'rental__window_e0015': ('labo/rental.ehp', 'window_e0015.gim', 'Lab'),
    'conv_machine__window_e0009': ('labo/conv_machine.ehp', 'window_e0009.gim', 'Converter'),
    'conv_machine__window_e0026': ('labo/conv_machine.ehp', 'window_e0026.gim', 'Converter'),
    'conv_machine__window_e0016': ('labo/conv_machine.ehp', 'window_e0016.gim', 'Trunk'),
    'all_e__d_window00033': ('deck/all_e.ehp', 'd_window00033.gim', 'Card types in possession'),
    'all_e__tab_title': ('shop/all_e.ehp', 'tab_title.gim', None),
    'password__key_e0027': ('labo/password.ehp', 'key_e0027.gim', None),
    'conv_machine__window_e0022': ('labo/conv_machine.ehp', 'window_e0022.gim', None),     # gold bar (same hash as rental e0021 and title_menu t_window0021)
}
TITLE = {'de': ('Gekaufte Karten', 'Gekaufte Kartenty'), 'fr': ('Cartes achetées', 'Types de cartes ac'), 'en': ('Purchased Cards', 'Card Types Purche'), 'es': ('Cartas compradas', 'Tipos de carta comp')}


LANG = __import__('os').environ.get('TF1_LANG', 'it')


def white_box(low):
    """(x0, x1) of the label's white box (like the hand parameters of `tab`): the last run of almost entirely white columns"""
    a = np.asarray(low.convert('RGBA'))
    w = (a[..., :3].min(-1) >= 250) & (a[..., 3] == 255)
    cnt = w[3:15].sum(0)
    cols = np.where(cnt >= 9)[0]
    r = int(cols.max())
    l = r
    while l - 1 >= 0 and cnt[l - 1] >= 9:
        l -= 1
    m = 2 if r + 1 - l < 20 else 1
    return l - m, r + 1 + m


def build_fr(tid, low, pack, F, word):
    ref = lambda k: common.reference(pack, REF[k])
    if tid == 'conv_machine__window_e0022':
        hd = gold_bar(ref('possession'), low.height * S, 0, 256, left=True, right=True)
        return paste_low(hd, low, 236, 0, 243, 1)
    if tid.endswith('__d_window00033'):
        hd = arr(ref('possession'))
        hd = gold_rebuild(hd, 18, 107 * S - 1, 16, 90, 144 * S, 146 * S)
        return label_text(hd, low, word, F, (4, 3, 103 if LANG == 'en' else 107, 19), 9, 15, (61, 53, 35), (26, 22, 14, 255))
    if tid.endswith('__tab_title'):
        H, W = low.height * S, low.width * S
        hd = np.zeros((H, W, 4), np.float32)
        hd[:, :138 * S] = arr(ref('purchase'))[:, :138 * S]
        fb = hd_fill(ref('purchase'), 14, 320, 46, 90)
        hd[11 * S:23 * S, 3 * S:83 * S, :3] = np.array(fb) / 255.0
        hd = label_text(hd, low, TITLE[LANG][0], F, (3, 10, {'fr': 83, 'de': 80, 'en': 77}.get(LANG, 75), 23), 9, 21, (70, 92, 154), (34, 44, 74, 255))
        hd[:, 138 * S:] = over(hd[:, 138 * S:], gold_bar(ref('possession'), H, 138, 256, left=True, right=False)[:, 138 * S:])
        hd = label_text(hd, low, TITLE[LANG][1], F, (141, 3, 256, 19), 9, 15, (61, 53, 36), (26, 22, 14, 255))
        return paste_low(hd, low, 240, 0, 246, 1)
    if tid.startswith('password__key_'):
        return key_caption(low)
    x0, x1 = white_box(low)
    if LANG == 'es' and word == 'Laboratorio':
        x0 -= 3                       # the long word must not touch the white box
    return tab(low, word, F, x0, x1)


def clean_alpha(hd, low):
    """keep the original transparency: HD blocks of pixels that are transparent in the original together with all
    their neighbours become fully transparent (removes halos of reused HD art and blur spill)."""
    import cv2
    a0 = (np.asarray(low.convert('RGBA'))[..., 3] == 0).astype(np.uint8)
    iso = cv2.erode(a0, np.ones((3, 3), np.uint8), borderType=cv2.BORDER_CONSTANT, borderValue=1)
    m = np.repeat(np.repeat(iso, S, 0), S, 1).astype(bool)
    hd = hd.copy()
    hd[m] = 0
    return hd


def main(argv):
    fam = common.Family('schede_deck', argv)
    F = fonts()
    import os
    fr = LANG != 'it'
    for tid, spec in ({'fr': TEX_FR, 'es': TEX_ES, 'de': TEX_DE, 'en': TEX_EN}.get(LANG, TEX)).items():
        file, member = spec[:2]
        low, h = common.texture(fam.usrdir, file, member)
        hd = clean_alpha(build_fr(tid, low, fam.pack_us, F, spec[2]) if fr else build(tid, low, fam.pack_us, F), low)
        fam.save(tid, img(hd), h, low)
    fam.finish()


if __name__ == '__main__':
    main(sys.argv)
