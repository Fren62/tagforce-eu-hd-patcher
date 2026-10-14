"""duel_texts: HD (4x) Italian duel HUD art for ULES00600 (duel/basic_ii.ehp).

  Catena (CHAIN, colored + gray flash), TURNO badges (blue/red), TOCCA AL GIOCATORE SUCCE|SSIVO banners (blue/red),
  INIZIA IL DUEL|LO banner (+ its flash), Attacco Diretto! (+ flash), the numbers/icons sheet card_icon03, card_side.

run:  python3 -I duel_texts.py USRDIR PACK_US OUT [group ...]      (groups: chain turn next start attack icons)

Method - nothing is cut out of the (AI-upscaled) art of the English pack, the lettering is typeset from scratch:
  * lettering: every word is ONE line typeset with ONE macOS system font, the one whose letterforms are those of the
    English HD lettering of the same element (measured on its letters): SF Rounded for CHAIN, Chalkboard SE (Bold,
    5 degree lean) for START/DUEL, Chalkboard SE Regular for Next Player's Turn, Comic Sans MS Bold (slight lean)
    for DIRECT ATACK, SF Expanded Black for the TURN badge.  One baseline, one size, one stroke weight, one slant,
    natural proportions: the glyphs are signed-distance fields of the font outlines and are never refitted letter
    by letter.  Only position, size, a squeeze of at most 10 % and the tracking of the whole line are solved so that
    the line (fill + outline + shadow) occupies the box of the low-res Italian original.  The stroke weight is the
    absolute stroke width (HD px) of the English letters.  For banners cut over two textures the cut lies in a
    letter gap (exactly like the originals: ...SUCCE | SSIVO..., ...DUEL | LO), so each texture holds whole letters.
  * look: fill gradient, outline and drop shadow are measured on the English HD texture of the same element
    (outline/shadow profiles fitted on the English letters) and re-applied to the Italian letters.
  * TURNO badges: the English HD badge frame / gradient / highlight bar (smooth art, 75 % of the pixels) is kept, the
    area under the English letters is inpainted and 'TURNO' is typeset and shadowed like the English 'TURN'.
  * TOCCA AL GIOCATORE SUCCE|SSIVO: 29 wide letters in the slot of 29 condensed ones, so the size is limited by the
    width.  Natural typesetting levers only, to make the letters as large as possible: optical kerning (letters 0.04 em
    apart), small word spaces, the full 10 % squeeze, a box 3 low-res px wider on each side; outline overlap between
    neighbouring letters.  Remaining compromise: the cap height is about 75 % of the original's condensed capitals.
  * flash textures (gray CHAIN, start, attack): the originals are already blurred silhouettes, so the HD flash is the
    smooth bicubic 4x upsample of the original alpha (0.35 low-res px blur, flat colour of the English HD flash): exact
    extent and word gaps of the original glow.
  * card_icon03: the English HD sheet (95 % of the pixels) + the cells in which the European game differs from the US
    pack (check disc, grey ball, empty pill, TEMPO) as exact 4x copies of the Italian pixel art, like the neighbouring
    pixel-art cells of that sheet.  card_side: exact 4x of the (finer palette) European English plaid."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import alt_font  # noqa: nessun font Apple
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import common

S = common.SCALE
SUP = '/System/Library/Fonts/Supplemental/'
SYS = '/System/Library/Fonts/'
# key: (file, face index, variation style name | None); SF Rounded is also driven by its weight axis (get_font)
FONT = {
    'sfr': (SYS + 'SFNSRounded.ttf', 0, 'Black'),
    'sfx_black': (SYS + 'SFNS.ttf', 0, 'Expanded Black'),
    'chalk_b': (SUP + 'ChalkboardSE.ttc', 2, None),
    'chalk_r': (SUP + 'ChalkboardSE.ttc', 1, None),
    'comic_b': (SUP + 'Comic Sans MS Bold.ttf', 0, None),
}
EM = 400      # glyph raster size (px per em) for the SDFs
PAD = 48      # glyph raster padding


# ----------------------------------------------------------------------------------------------------- optimiser
def nelder_mead(f, x0, step, iters=400, tol=1e-7):
    n = len(x0)
    pts = [np.array(x0, float)]
    for i in range(n):
        p = np.array(x0, float)
        p[i] += step[i]
        pts.append(p)
    vals = [f(p) for p in pts]
    for _ in range(iters):
        o = np.argsort(vals)
        pts = [pts[i] for i in o]
        vals = [vals[i] for i in o]
        if abs(vals[-1] - vals[0]) <= tol * (abs(vals[0]) + 1e-12):
            break
        c = np.mean(pts[:-1], 0)
        xr = c + (c - pts[-1]); fr = f(xr)
        if fr < vals[0]:
            xe = c + 2 * (c - pts[-1]); fe = f(xe)
            pts[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]:
            pts[-1], vals[-1] = xr, fr
        else:
            xc = c + 0.5 * (pts[-1] - c); fc = f(xc)
            if fc < vals[-1]:
                pts[-1], vals[-1] = xc, fc
            else:
                for i in range(1, n + 1):
                    pts[i] = pts[0] + 0.5 * (pts[i] - pts[0]); vals[i] = f(pts[i])
    i = int(np.argmin(vals))
    return pts[i], vals[i]


# ----------------------------------------------------------------------------------------------------- glyphs
def sdf_of(mask):
    """signed distance (px, <0 inside) of a binary mask."""
    m = (mask > 0.5).astype(np.uint8)
    dout = cv2.distanceTransform(1 - m, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    din = cv2.distanceTransform(m, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    return (dout - din + np.where(m > 0, 0.5, -0.5)).astype(np.float32)


def get_font(fkey, size, weight=None):
    path, idx, var = FONT[fkey]
    f = ImageFont.truetype(path, size, index=idx)
    if weight is not None:
        f.set_variation_by_axes([400, weight])       # SF Rounded: (GRAD, Weight)
    elif var:
        f.set_variation_by_name(var)
    return f


class Glyph:
    """SDF of one letter (px of the EM raster, < 0 inside) + metrics: bbox = box of the raster relative to the pen
    origin on the baseline (y up negative), ink = true ink box in the same coordinates, adv = advance."""

    def __init__(self, sdf, bbox, adv):
        self.sdf, self.bbox, self.adv = sdf, bbox, adv
        ys, xs = np.nonzero(sdf < 0)
        ox, oy = bbox[0] - PAD, bbox[1] - PAD
        self.ink = (xs.min() + ox, ys.min() + oy, xs.max() + 1 + ox, ys.max() + 1 + oy)


_gcache = {}


def font_glyph(fkey, ch, weight=None):
    k = (fkey, ch, weight)
    if k not in _gcache:
        f = get_font(fkey, EM, weight)
        x0, y0, x1, y1 = f.getbbox(ch, anchor='ls')
        w, h = x1 - x0 + 2 * PAD, y1 - y0 + 2 * PAD
        im = Image.new('L', (w * 2, h * 2), 0)
        ImageDraw.Draw(im).text(((PAD - x0) * 2, (PAD - y0) * 2), ch, font=get_font(fkey, EM * 2, weight), fill=255,
                                anchor='ls')
        m = np.asarray(im.resize((w, h), Image.BOX), np.float32) / 255
        _gcache[k] = Glyph(sdf_of(m), (x0, y0, x1, y1), f.getlength(ch))
    return _gcache[k]


class Line:
    """a typeset line: characters of one font on one baseline.  Parameters (HD px): x = pen start, base = baseline,
    k = HD px per EM-raster px, sx = horizontal squeeze (1 = natural), track = extra spacing after each character
    (HD px), shear = slant (dx/dy, > 0 leans right), spf = width factor of the spaces."""

    def __init__(self, text, fkey, weight=None):
        self.text, self.fkey, self.weight = text, fkey, weight
        self.glyphs = {c: font_glyph(fkey, c, weight) for c in set(text) if c != ' '}
        self.space = get_font(fkey, EM, weight).getlength(' ')
        self.shear = 0.0
        self.kern = {}

    def kerning(self, g_em, xgap=None):
        """optical kerning: every pair of neighbouring letters (never across a space) is brought together until the
        true (euclidean) distance between the two letter fills is g_em (em units) - a pair whose natural distance is
        already smaller is left alone.  xgap = {(a, b): x} keeps, for the listed pairs, at least x em of free
        columns between the two letters (the place where a banner is cut between two textures)."""
        self.kern = {}
        g = g_em * EM
        for a, b in set(zip(self.text, self.text[1:])):
            if a == ' ' or b == ' ':
                continue
            ga, gb = self.glyphs[a], self.glyphs[b]
            yb, xb = np.nonzero((gb.sdf < 0) & (gb.sdf >= -1.0))
            xb = xb + gb.bbox[0] - PAD
            yb = yb + gb.bbox[1] - PAD
            ax, ay = ga.bbox[0] - PAD, ga.bbox[1] - PAD

            def dist(D):
                ix = np.rint(xb + D - ax).astype(int)
                iy = np.rint(yb - ay).astype(int)
                ok = (ix >= 0) & (ix < ga.sdf.shape[1]) & (iy >= 0) & (iy < ga.sdf.shape[0])
                v = np.full(len(xb), float(PAD), np.float32)
                v[ok] = ga.sdf[iy[ok], ix[ok]]
                return float(v.min())
            lo, hi = ga.adv - EM, ga.adv + 0.25 * EM       # dist() grows with D
            for _ in range(24):
                mid = (lo + hi) / 2
                if dist(mid) < g:
                    lo = mid
                else:
                    hi = mid
            D = hi
            if xgap and (a, b) in xgap:
                D = max(D, xgap[(a, b)] * EM + ga.ink[2] - gb.ink[0])
            self.kern[(a, b)] = min(0.0, D - ga.adv)

    def pens(self, x, k, sx, track, spf=1.0):
        """pen x of every character (HD px)."""
        out = []
        for i, c in enumerate(self.text):
            out.append(x)
            if c == ' ':
                adv = self.space * spf
            else:
                adv = self.glyphs[c].adv
                if self.kern and i + 1 < len(self.text):
                    adv += self.kern.get((c, self.text[i + 1]), 0.0)
            x += adv * k * sx + track
        return out, x

    def render(self, shape, x, base, k, sx=1.0, track=0.0, spf=1.0, sdf_out=None):
        """signed-distance image (HD px) of the line on a canvas of 'shape'."""
        H, W = shape
        sdf = np.full(shape, 1e4, np.float32) if sdf_out is None else sdf_out
        pens, _ = self.pens(x, k, sx, track, spf)
        for c, px in zip(self.text, pens):
            if c == ' ':
                continue
            g = self.glyphs[c]
            gx0, gy0 = g.bbox[0] - PAD, g.bbox[1] - PAD
            gh, gw = g.sdf.shape
            sh = self.shear
            M = np.float32([[k * sx, -sh * k, px + k * sx * gx0 - sh * k * gy0], [0, k, base + k * gy0]])
            corners = M[:, :2] @ np.float32([[0, gw, 0, gw], [0, 0, gh, gh]]) + M[:, 2:]
            rx0, ry0 = np.floor(corners.min(1)).astype(int)
            rx1, ry1 = np.ceil(corners.max(1)).astype(int) + 1
            rx0, ry0, rx1, ry1 = max(0, rx0), max(0, ry0), min(W, rx1), min(H, ry1)
            if rx1 <= rx0 or ry1 <= ry0:
                continue
            M[0, 2] -= rx0
            M[1, 2] -= ry0
            w = cv2.warpAffine(g.sdf, M, (rx1 - rx0, ry1 - ry0), flags=cv2.INTER_LINEAR,
                               borderMode=cv2.BORDER_CONSTANT, borderValue=float(PAD)) * k * np.sqrt(sx)
            np.minimum(sdf[ry0:ry1, rx0:rx1], w, out=sdf[ry0:ry1, rx0:rx1])
        return sdf


def cover(sdf, emb=0.0):
    """anti-aliased coverage (0..1) from an SDF in canvas px; emb > 0 makes the strokes bolder by emb px."""
    return np.clip(0.5 - (sdf - emb), 0, 1).astype(np.float32)


def down(a, f=S):
    return cv2.resize(a, (a.shape[1] // f, a.shape[0] // f), interpolation=cv2.INTER_AREA)


# ----------------------------------------------------------------------------------------------------- fitting
def extent_sub(T):
    """sub-pixel extent (x0, x1, y0, y1) in low-res px of a fill coverage map."""
    cm, rm = T.max(0), T.max(1)
    xs, ys = np.nonzero(cm > 0.05)[0], np.nonzero(rm > 0.05)[0]
    return (xs[0] + 1 - cm[xs[0]], xs[-1] + cm[xs[-1]], ys[0] + 1 - rm[ys[0]], ys[-1] + rm[ys[-1]])


def ink_span(line, p, spf=1.0):
    """(left, right) ink extent in HD px of a line with params p = [x, base, k, sx, track]."""
    x, base, k, sx, tr = p
    pens, _ = line.pens(x, k, sx, tr, spf)
    idx = [i for i, c in enumerate(line.text) if c != ' ']
    i0, i1 = idx[0], idx[-1]
    g0, g1 = line.glyphs[line.text[i0]], line.glyphs[line.text[i1]]
    return pens[i0] + g0.ink[0] * k * sx, pens[i1] + g1.ink[2] * k * sx


def gap_at(line, p, i, spf=1.0):
    """(right edge of the ink before character i, left edge of the ink of character i) in HD px, at mid height of
    the letters (so that a slant is taken into account)."""
    x, base, k, sx, tr = p
    pens, _ = line.pens(x, k, sx, tr, spf)
    j = i - 1
    while line.text[j] == ' ':
        j -= 1
    g0, g1 = line.glyphs[line.text[j]], line.glyphs[line.text[i]]
    top = min(g.ink[1] for g in line.glyphs.values())
    ymid = top / 2
    lean = line.shear * k * -ymid
    return pens[j] + g0.ink[2] * k * sx + lean, pens[i] + g1.ink[0] * k * sx + lean


def solve_line(line, x0, x1, base, height, ref, sx_lim=(0.9, 1.0), track_lim=(0.0, 0.0), spf=1.0, k_cap=None):
    """parameters p = [x, base, k, sx, track] of ONE line (natural proportions) that spans x0..x1 (HD px):
    size k from the height (HD px) of the reference glyph string 'ref'; if the line is longer than the slot the
    tracking is tightened first (down to track_lim[0], in em), then the line is squeezed (sx >= sx_lim[0]) and
    last the size is reduced; if it is shorter, it is widened by the tracking (<= track_lim[1] em) after a stretch
    of at most sx_lim[1]."""
    top = min(line.glyphs[c].ink[1] for c in ref)
    bot = max(line.glyphs[c].ink[3] for c in ref)
    k = height / (bot - top)
    if k_cap is not None:
        k = min(k, k_cap)
    n = max(1, sum(1 for c in line.text if c != ' ') - 1)
    W = x1 - x0
    for _ in range(40):
        sx, tr = 1.0, 0.0
        p = [0.0, base, k, sx, tr]
        l, r = ink_span(line, p, spf)
        w = r - l
        if w > W:
            tr = max(track_lim[0] * k * EM, -(w - W) / n)
            p = [0.0, base, k, sx, tr]
            l, r = ink_span(line, p, spf)
            w = r - l
            if w > W:
                sx = max(sx_lim[0], W / w)
                p = [0.0, base, k, sx, tr]
                l, r = ink_span(line, p, spf)
                w = r - l
                if w > W + 0.25:
                    k *= W / w * 0.999
                    continue
        else:
            sx = min(sx_lim[1], W / w)
            p = [0.0, base, k, sx, tr]
            l, r = ink_span(line, p, spf)
            w = r - l
            if w < W:
                tr = min(track_lim[1] * k * EM, (W - w) / n)
                p = [0.0, base, k, sx, tr]
                l, r = ink_span(line, p, spf)
        break
    p[0] = x0 - l
    p[1] = (base - height / 2) - k * (top + bot) / 2      # the letter band stays centred on the original one
    return p


# ----------------------------------------------------------------------------------------------------- style
def signed_dist(cov):
    """signed distance (HD px, < 0 inside) from an anti-aliased coverage map, computed at 2x for sub-pixel edges."""
    up = cv2.resize(cov, (cov.shape[1] * 2, cov.shape[0] * 2), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(sdf_of(up), (cov.shape[1], cov.shape[0]), interpolation=cv2.INTER_AREA) / 2


def fill_target(rgba, chan, lo, hi):
    """fill coverage of a styled text image: position of a channel between outline (lo) and fill (hi) colour."""
    a = np.asarray(rgba, np.float32)
    return (np.clip((a[..., chan] - lo) / (hi - lo), 0, 1) * (a[..., 3] >= 250)).astype(np.float32)


def shift(a, dx, dy):
    return cv2.warpAffine(a, np.float32([[1, 0, dx], [0, 1, dy]]), (a.shape[1], a.shape[0]), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def smooth(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


class Style:
    """outline (colour co, solid up to r1 px from the fill, fading out at r2) + drop shadow (offset dx,dy, blur sg,
    opacity op, colour cs) + fill colour (vertical gradient, HD rows)."""

    def __init__(self, co, r1, r2, dx=0.0, dy=0.0, sg=1.0, op=0.0, cs=(0, 0, 0)):
        self.co, self.r1, self.r2 = np.float32(co), r1, r2
        self.dx, self.dy, self.sg, self.op, self.cs = dx, dy, sg, op, np.float32(cs)

    def params(self):
        return [self.r1, self.r2, self.dx, self.dy, self.sg, self.op]

    def set(self, p):
        self.r1, self.r2, self.dx, self.dy, self.sg, self.op = [float(v) for v in p]
        self.r2 = max(self.r2, self.r1 + 0.5)
        self.sg, self.op = max(self.sg, 0.3), float(np.clip(self.op, 0, 1))
        return self


def render_style(cov, fillrgb, st, d=None):
    """RGBA float (0..1 alpha, 0..255 colour) of a styled text from its fill coverage (HD) and fill colours
    (H x W x 3 or H x 1 x 3)."""
    if d is None:
        d = signed_dist(cov)
    ao = smooth((st.r2 - d) / (st.r2 - st.r1)) if st.r2 > 0 else np.zeros_like(cov)
    at = np.maximum(cov, ao)
    rgb = cov[..., None] * fillrgb + (1 - cov[..., None]) * st.co
    if st.op > 0:
        sh = cv2.GaussianBlur(shift(at, st.dx, st.dy), (0, 0), st.sg) * st.op
    else:
        sh = np.zeros_like(at)
    al = at + sh * (1 - at)
    out = (rgb * at[..., None] + st.cs * (sh * (1 - at))[..., None]) / np.maximum(al, 1e-6)[..., None]
    return np.dstack([out, al])


def to_image(rgba):
    a = np.dstack([np.clip(rgba[..., :3], 0, 255), np.clip(rgba[..., 3:] * 255, 0, 255)])
    return Image.fromarray(np.round(a).astype(np.uint8), 'RGBA')


def row_gradient(rgba, cov, thr=0.95, smooth_px=3):
    """per-row median fill colour of a styled HD text (rows without fill take the nearest one), H x 1 x 3."""
    a = np.asarray(rgba, np.float32)
    H = a.shape[0]
    g = np.full((H, 3), np.nan, np.float32)
    for y in range(H):
        sel = cov[y] > thr
        if sel.sum() >= 3:
            g[y] = np.median(a[y, sel, :3], 0)
    ok = ~np.isnan(g[:, 0])
    ys = np.arange(H)
    for c in range(3):
        g[:, c] = np.interp(ys, ys[ok], g[ok, c])
    if smooth_px:
        g = cv2.GaussianBlur(g.reshape(H, 1, 3), (1, 6 * smooth_px + 1), 0, sigmaY=smooth_px).reshape(H, 3)
    return g[:, None, :], (ys[ok].min(), ys[ok].max())


def calibrate(ref, cov, st, fit=(0, 1, 2, 3, 4, 5), iters=250, grad=None):
    """fit the outline/shadow parameters of st so that render_style(cov) reproduces the HD reference ref."""
    R = np.asarray(ref, np.float32)
    Rp = np.dstack([R[..., :3] * R[..., 3:] / 255, R[..., 3:]])
    if grad is None:
        grad, _ = row_gradient(ref, cov)
    d = signed_dist(cov)
    p0 = np.array(st.params(), float)

    def loss(q):
        p = p0.copy()
        p[list(fit)] = q
        st.set(p)
        o = render_style(cov, grad, st, d)
        op = np.dstack([o[..., :3] * o[..., 3:], o[..., 3:] * 255])
        return float(np.abs(op - Rp).mean())
    q, v = nelder_mead(loss, p0[list(fit)], [[1.0, 1.0, 1.0, 1.0, 1.0, 0.1][i] for i in fit], iters)
    p = p0.copy()
    p[list(fit)] = q
    st.set(p)
    return st, v


def grad_map(gref, ref_rows, rows, H):
    """HD reference gradient (n x 1 x 3) mapped by geometry: ref_rows = (top, bottom) of the English letters,
    rows = (top, bottom) of the Italian letters -> gradient H x 1 x 3."""
    a = (ref_rows[1] - ref_rows[0]) / max(1.0, rows[1] - rows[0])
    src = np.clip(ref_rows[0] + (np.arange(H) - rows[0]) * a, 0, len(gref) - 1)
    g = gref[:, 0, :]
    return np.stack([np.interp(src, np.arange(len(g)), g[:, c]) for c in range(3)], 1)[:, None, :].astype(np.float32)


def fill_rows(cov, thr=0.5):
    ys = np.nonzero(cov.max(1) > thr)[0]
    return float(ys.min()), float(ys.max() + 1)


class Ref:
    """style measured on an English HD text texture."""

    def __init__(self, pack, rel, chan, lo, hi, st0, fit=(0, 1, 2, 3, 4, 5)):
        self.img = common.reference(pack, rel)
        self.cov = fill_target(self.img, chan, lo, hi)
        self.grad, self.span = row_gradient(self.img, self.cov)
        self.st, self.err = calibrate(self.img, self.cov, st0, fit, grad=self.grad)


# ----------------------------------------------------------------------------------------------------- textures
LANG = os.environ.get('TF1_LANG', 'it')
# texts per language: b = game archive (duel/basic_<b>.ehp), cut = part of the text before the cut between two textures,
# r* = characters that measure the capital height; Chaine/Turn... = words of the language's original
TXT = {'it': dict(b='ii', chain='Catena', next='TOCCA AL GIOCATORE SUCCESSIVO', next_cut='TOCCA AL GIOCATORE SUCCE', rnext='TLE',
                  start='INIZIA IL DUELLO', start_cut='INIZIA IL DUEL', rstart='IL', attack='Attacco Diretto!', turn='TURNO', rturn='TURN'),
       'fr': dict(b='ff', chain='Chaîne', next='TOUR DU JOUEUR SUIVANT', next_cut='TOUR DU JOUEUR SUIV', rnext='TE',
                  start='DÉMARRER DUEL', start_cut='DÉMARRER DU', rstart='ED', attack='Attaque Directe!', turn='TOUR', rturn='TUR'),
       # Spanish: in the original the cut between the two textures passes inside a letter (E of DUELO, A of JUGADOR), without a gap: no anchor.
       # The TURNO badge has the same hash as Italian (ui_it applies) and card_icon03 is made with icon03_languages.py.
       'es': dict(b='ss', chain='Cadena', next='TURNO DEL SIGUIENTE JUGADOR', next_cut=None, rnext='TE',
                  start='COMENZAR DUELO', start_cut=None, rstart='ED', attack='Ataque Directo', rattack='AD', turn='TURNO', rturn='TURN'),
       # German: the "NÄCHSTER SPIELER" banner is on 0003 (256 px) + 0002 (64 px, the cut passes inside the L) and the dots of the Ä are a
       # separate texture (0001, 0005 for red) that the game puts over the A: I draw them inside the lettering and empty that texture.
       'de': dict(b='gg', chain='Ketten', rchain='K', next='NACHSTER SPIELER', next_final='NÄCHSTER SPIELER', next_cut=None, rnext='TE',
                  next_members=((('next_player0003.gim', 'next_player0002.gim'), 'next_player0001.gim'),
                                (('next_player0007.gim', 'next_player0006.gim'), 'next_player0005.gim')),
                  start='DUELL BEGINNEN', start_cut=None, rstart='ED', attack='Direkter Angriff!', rattack='Dgf', turn='SPIELZUG', rturn='ELZ',
                  next_kw=dict(sx_lim=(0.9, 1.12), track_lim=(0.0, 0.1)), attack_kw=dict(sx_lim=(0.92, 1.12), track_lim=(-0.04, 0.08)))}[LANG]
BASIC = f"duel/basic_{TXT['b']}.ehp"
PFX = f"basic_{TXT['b']}__"


def load(usrdir, *members):
    """low-res Italian texture(s) side by side (one canvas) + the textures + their hashes."""
    ims = [common.texture(usrdir, BASIC, m) for m in members]
    W = sum(i.width for i, _ in ims)
    can = Image.new('RGBA', (W, ims[0][0].height))
    x = 0
    for i, _ in ims:
        can.paste(i, (x, 0))
        x += i.width
    return can, [i for i, _ in ims], [h for _, h in ims]


def split(hd, lows):
    """cut an HD canvas back into the pieces of the original textures (4x their widths)."""
    out, x = [], 0
    for l in lows:
        out.append(hd.crop((x, 0, x + l.width * S, l.height * S)))
        x += l.width * S
    return out


def soft_flash(low, color):
    """soft glow/flash texture (one flat colour, alpha only).  The originals are already blurred silhouettes of their
    words, so the HD flash is a smooth bicubic 4x upsample of the original alpha (plus a 0.35 low-res px blur that
    hides the quantisation steps): the exact extent and word gaps of the original glow, no new edges."""
    La = np.asarray(low, np.float32)[..., 3] / 255
    a = cv2.resize(La, (low.width * S, low.height * S), interpolation=cv2.INTER_CUBIC)
    a = np.clip(cv2.GaussianBlur(a, (0, 0), 0.35 * S), 0, 1)
    return np.dstack([np.broadcast_to(np.float32(color), a.shape + (3,)), a])


def flat_color(img):
    a = np.asarray(img, np.float32)
    return np.median(a[a[..., 3] > 200][:, :3], 0)


def anchor_solve(line, p0, x0, x1, i, X, spf=1.0):
    """position x, squeeze sx and tracking tr (size k kept) of a line whose gap before character i is centred on X
    (HD px; the cut between two textures of a split banner lies there) while its ink still starts near x0 and ends
    near x1: weighted least squares around the unanchored solution p0 (the cut is a hard condition, the two ends
    soft ones; sx and tr are kept close to p0).  Newton iterations (the slant adds a constant)."""
    k, base = p0[2], p0[1]
    n = len(line.text) - 1
    nat = [0.0, base, k, 1.0, 0.0]
    L0, R0 = ink_span(line, nat, spf)
    g = gap_at(line, nat, i, spf)
    G0 = (g[0] + g[1]) / 2
    em = k * EM
    A = np.array([[1, L0, 0], [1, R0, n], [50, 50 * G0, 50 * i], [0, 3000, 0], [0, 0, 20]], float)
    q = np.array([p0[0], p0[3], p0[4]], float)
    for _ in range(4):
        p = [q[0], base, k, q[1], q[2]]
        L, R = ink_span(line, p, spf)
        gg = gap_at(line, p, i, spf)
        res = np.array([x0 - L, x1 - R, 50 * (X - (gg[0] + gg[1]) / 2), 3000 * (p0[3] - q[1]), 20 * (p0[4] - q[2])], float)
        q = q + np.linalg.lstsq(A, res, rcond=None)[0]
    return [q[0], base, k, q[1], q[2]]


def typeset(low, line, p, emb=0.0, shear=0.0, spf=1.0):
    """fill coverage (HD) of a line with parameters p."""
    line.shear = shear
    shape = (low.height * S, low.width * S)
    return cover(line.render(shape, p[0], p[1], p[2], p[3], p[4], spf), emb)


def seam_shift(cov, X, reach=14):
    """horizontal shift (HD px) that puts the cut X inside the nearest column run without any letter fill (so that
    each texture of a split banner holds whole letters, like the originals)."""
    free = cov.max(0) < 0.02
    cols = [c for c in range(int(X) - reach, int(X) + reach + 1) if 0 <= c < len(free) and free[c]]
    if not cols:
        return 0.0
    # runs of free columns
    runs, start = [], cols[0]
    for a, b in zip(cols, cols[1:] + [None]):
        if b != a + 1:
            runs.append((start, a))
            start = b
    best = min(runs, key=lambda r: 0 if r[0] <= X <= r[1] else min(abs(X - r[0]), abs(X - r[1])))
    if best[0] <= X <= best[1]:
        return 0.0
    c = (best[0] + best[1]) / 2
    return float(X - c)


def place_line(low, line, T, ref, rows_ref, ref_chars, sx_lim=(0.9, 1.1), track_lim=(0.0, 0.0), shear=0.0, emb=0.0, spf=1.0, iters=3,
               k_cap=None, anchor=None, grow=(0.0, 0.0), dy=0.0):
    """position of ONE line (natural proportions, one size) such that the fill AND its outline + shadow
    occupy the same box as the low-res original: the fill extent given by T is corrected, iteratively, by the
    margin that the style (outline, shadow) adds around the HD letters.  anchor = (i, X): the gap before
    character i is centred on X (the cut between the textures of a split banner).  grow = (left, right) low-res
    px by which the box may be wider than the original one (a line whose letters cannot be condensed); dy = vertical
    offset (HD px) of the box.  Returns (cov, rgba, params)."""
    La = np.asarray(low, np.float32)[..., 3] / 255
    tx0, tx1, ty0, ty1 = [v * S for v in extent_sub(La)]
    ex = [v * S for v in extent_sub(T)]
    tx0, tx1, ex[0], ex[1] = tx0 - grow[0] * S, tx1 + grow[1] * S, ex[0] - grow[0] * S, ex[1] + grow[1] * S
    ty0, ty1, ex[2], ex[3] = ty0 + dy, ty1 + dy, ex[2] + dy, ex[3] + dy
    for it in range(iters):
        p = solve_line(line, ex[0], ex[1], ex[3], ex[3] - ex[2], ref_chars, sx_lim, track_lim, spf, k_cap)
        if anchor is not None:
            for _ in range(30):
                q = anchor_solve(line, p, ex[0], ex[1], anchor[0], anchor[1], spf)
                if q[3] >= sx_lim[0] - 0.005 and q[4] >= track_lim[0] * q[2] * EM * 1.3 - 0.3:
                    break
                p = solve_line(line, ex[0], ex[1], ex[3], ex[3] - ex[2], ref_chars, sx_lim, track_lim, spf, p[2] * 0.985)
            p = q
        cov = typeset(low, line, p, emb, shear, spf)
        if anchor is not None:
            dx = seam_shift(cov, anchor[1])
            if dx:
                p = list(p)
                p[0] += dx
                cov = typeset(low, line, p, emb, shear, spf)
        rgba, st = style_text(cov, ref, rows_ref, low)
        fx0, fx1, fy0, fy1 = [v * S for v in extent_sub(down(rgba[..., 3]))]
        d = [tx0 - fx0, tx1 - fx1, ty0 - fy0, ty1 - fy1]
        if max(abs(v) for v in d) < 0.4:
            break
        ex = [ex[0] + d[0], ex[1] + d[1], ex[2] + d[2], ex[3] + d[3]]
    return cov, rgba, p


def style_text(cov, ref, rows_ref, low=None, rows=None):
    """RGBA float of the styled line: fill gradient mapped from the English letters (rows_ref = top/bottom of its
    capitals) to the Italian ones; outline and shadow exactly as measured on the English HD texture."""
    H = cov.shape[0]
    if rows is None:
        rows = fill_rows(cov)
    grad = grad_map(ref.grad, rows_ref, rows, H)
    return render_style(cov, grad, ref.st), ref.st


def ref_letters(img, chan, lo, hi, chars, minarea=40, conn=8):
    """letters of an English HD text, cut out of its fill coverage (left to right): {char: coverage mask}.  They are
    only MEASURED (cap height, stroke width), never pasted."""
    T = fill_target(img, chan, lo, hi)
    n, lab, st, _ = cv2.connectedComponentsWithStats((T > 0.5).astype(np.uint8), connectivity=conn)
    ids = [i for i in np.argsort(st[1:, 0]) + 1 if st[i, 4] >= minarea]
    assert len(ids) == len(chars), (len(ids), chars)
    out, boxes = {}, {}
    for c, i in zip(chars, ids):
        x, y, w, h, _ = st[i]
        out.setdefault(c, (lab[y:y + h, x:x + w] == i).astype(np.float32))
        boxes.setdefault(c, (x, y, w, h))
    return out, boxes


def stem(mask):
    """stroke width (px) of a letter: twice the largest inscribed radius."""
    m = np.pad((mask > 0.5).astype(np.uint8), 2)
    return 2.0 * float(cv2.distanceTransform(m, cv2.DIST_L2, cv2.DIST_MASK_PRECISE).max())


def weight_emb(letters, fkey, chars, k, weight=None):
    """stroke weight correction (emb, HD px; > 0 = bolder) of the font at size k so that its letters 'chars' have the
    same stroke width, in HD pixels, as the same letters of the English HD lettering (dict of masks): the strokes
    keep the absolute thickness of the mod's lettering (the outline and the shadow have it too)."""
    d = []
    for c in chars:
        m = letters[c]
        g = font_glyph(fkey, c, weight)
        sd = np.full((int((g.ink[3] - g.ink[1]) * k + 40), int((g.ink[2] - g.ink[0]) * k + 40)), 1e4, np.float32)
        Line(c, fkey, weight).render(sd.shape, 20 - g.ink[0] * k, 20 - g.ink[1] * k, k, 1.0, 0.0, 1.0, sd)
        d.append((stem(m) - stem(cover(sd))) / 2)
    return float(np.median(d))


# ------------------------------------------------------------------------------------------------- Catena (CHAIN)
def do_chain(fam, U, P):
    low, _, (h,) = load(U, 'chain010005.gim')
    T = fill_target(low, 0, 25, 215)
    ref = Ref(P, 'ui/text/chain.png', 0, 25, 215, Style((2, 2, 2), 6, 12, 1.5, 1.5, 2, 0.5))
    letters, boxes = ref_letters(ref.img, 0, 25, 215, 'CHAIN')
    line = Line(TXT['chain'], 'sfr', weight=720)
    kw = dict(sx_lim=(0.92, 1.05), track_lim=(-0.03, 0.03))
    rows_ref = (ref.span[0], ref.span[1] + 1)
    p = place_line(low, line, T, ref, rows_ref, TXT.get('rchain', 'C'), **kw)[2]
    emb = weight_emb(letters, 'sfr', 'HINA', p[2], 720)
    cov, rgba, p = place_line(low, line, T, ref, rows_ref, TXT.get('rchain', 'C'), emb=emb, **kw)
    print('catena', p, 'stroke correction', emb)
    fam.save(PFX + 'chain010005', to_image(rgba), h, low)
    lowg, _, (hg,) = load(U, 'chain010003.gim')
    g = soft_flash(lowg, flat_color(common.reference(P, 'ui/text/chain_gray.png')))
    fam.save(PFX + 'chain010003', to_image(g), hg, lowg)


# ------------------------------------------------------------------------- TOCCA AL GIOCATORE SUCCE|SSIVO
def do_next(fam, U, P):
    text = TXT['next']
    nm = TXT.get('next_members', ((('next_player0002.gim', 'next_player0001.gim'), None), (('next_player0005.gim', 'next_player0004.gim'), None)))
    versions = [(nm[0][0], tuple(PFX + m[:-4] for m in nm[0][0]), 2, 60, 'ui/text/nextplayersturn_blue.png', (78, 0, 54), nm[0][1]),
                (nm[1][0], tuple(PFX + m[:-4] for m in nm[1][0]), 0, 68, 'ui/text/nextplayersturn_red.png', (62, 0, 56), nm[1][1])]
    cov = None
    for members, ids, chan, lo, rel, co, dots in versions:
        can, lows, hs = load(U, *members)
        T = fill_target(can, chan, lo, 250)
        ref = Ref(P, rel, chan, lo + 10, 240, Style(co, 6, 10, 3, 3, 4, 0.4))
        letters, boxes = ref_letters(ref.img, chan, lo + 10, 240, "NextPlayer's" + 'Turn')
        rows_ref = (boxes['N'][1], boxes['N'][1] + boxes['N'][3])
        if cov is None:
            # 29 wide letters in the slot of 29 condensed ones: the size is limited by the width, so every width
            # lever of natural typesetting is used: optical kerning (letters 0.04 em apart, never touching), small
            # word spaces (fill gap 4.5-5.5 low-res px, the original has 3-4), the full 10 % squeeze and a box 3
            # low-res px wider on each side (the English banner fills 97 % of its texture); the cut stays in the
            # E|S gap
            line = Line(text, 'chalk_r')
            line.kerning(0.04, {('E', 'S'): 0.06})
            kw = dict(sx_lim=(0.9, 1.0), track_lim=(0.0, 0.0), spf=0.45, grow=(3.0, 3.0), dy=-2.5,
                      anchor=(len(TXT['next_cut']), lows[0].width * S) if TXT['next_cut'] else None)
            kw.update(TXT.get('next_kw', {}))
            p = place_line(can, line, T, ref, rows_ref, TXT['rnext'], **kw)[2]
            emb = weight_emb(letters, 'chalk_r', 'NPT', p[2])
            print('next: stroke correction', emb)
            cov, rgba, p = place_line(can, line, T, ref, rows_ref, TXT['rnext'], emb=emb, **kw)
            print('next: p', p)
        else:
            rgba, st = style_text(cov, ref, rows_ref, can)
        for i, piece, hh, l in zip(ids, split(to_image(rgba), lows), hs, lows):
            fam.save(i, piece, hh, l)
        if dots:
            ld, _, (hd_,) = load(U, dots)
            fam.save(PFX + dots[:-4], dots_hd(ld, line, p), hd_, ld)


def dots_hd(low, line, p):
    """dots of the Ä (separate sprite, the game puts it over the A): the original enlarged 4x (cubic, on premultiplied colours)
    and centred over our A (second letter of the line, parameters p)"""
    x, base, k, sx, tr = p
    pens, _ = line.pens(x, k, sx, tr, 0.45)
    g = line.glyphs[line.text[1]]
    xa = pens[1] + (g.ink[0] + g.ink[2]) / 2.0 * k * sx                  # centre of our A (HD px)
    a = np.asarray(low.convert('RGBA'), np.float32)
    xs = np.nonzero(a[..., 3].max(0) > 0)[0]
    dx = xa - (xs[0] + xs[-1] + 1) / 2.0 * S
    print('Ä dots: shift', round(dx, 2), 'px HD')
    pm = np.dstack([a[..., :3] * a[..., 3:] / 255.0, a[..., 3:]])
    M = np.float32([[S, 0, dx + (S - 1) / 2.0], [0, S, (S - 1) / 2.0]])
    up = cv2.warpAffine(pm, M, (low.width * S, low.height * S), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT)
    al = np.clip(up[..., 3], 0, 255)
    rgb = np.clip(up[..., :3] / np.maximum(al[..., None] / 255.0, 1e-3), 0, 255)
    return Image.fromarray(np.round(np.dstack([rgb, al])).astype(np.uint8), 'RGBA')


# --------------------------------------------------------------------------------- INIZIA IL DUEL|LO (+ flash)
def do_start(fam, U, P):
    can, lows, hs = load(U, 'start_duel10002.gim', 'start_duel10001.gim')
    T = fill_target(can, 0, 123, 255)
    ref = Ref(P, 'ui/text/start.png', 0, 123, 255, Style((122, 5, 110), 10, 14, 3, 4, 6, 0.5))
    letters, boxes = ref_letters(ref.img, 0, 123, 255, 'START')
    l2, b2 = ref_letters(common.reference(P, 'ui/text/duel_2.png'), 0, 123, 255, 'DUEL')
    letters.update(l2)
    SHEAR = 0.09          # lean of the English START / DUEL letters (measured on their strokes)
    rows_ref = (boxes['S'][1], boxes['S'][1] + boxes['S'][3])
    line = Line(TXT['start'], 'chalk_b')
    kw = dict(sx_lim=(0.9, 1.05), track_lim=(-0.04, 0.03), shear=SHEAR,
              anchor=(len(TXT['start_cut']), lows[0].width * S) if TXT['start_cut'] else None)
    p = place_line(can, line, T, ref, rows_ref, TXT['rstart'], **kw)[2]
    emb = weight_emb(letters, 'chalk_b', 'TEDLU', p[2])
    print('start: stroke correction', emb)
    cov, rgba, p = place_line(can, line, T, ref, rows_ref, TXT['rstart'], emb=emb, **kw)
    print('start: p', p)
    for i, piece, hh, l in zip((PFX + 'start_duel10002', PFX + 'start_duel10001'), split(to_image(rgba), lows),
                               hs, lows):
        fam.save(i, piece, hh, l)
    lowg, _, (hg,) = load(U, 'start_duel10005.gim')
    g = soft_flash(lowg, flat_color(common.reference(P, 'ui/text/direct_attack_gray.png')))
    fam.save(PFX + 'start_duel10005', to_image(g), hg, lowg)


# ------------------------------------------------------------------------------- Attacco Diretto! (+ flash)
def do_attack(fam, U, P):
    low, _, (h,) = load(U, 'dilect_atk00001.gim')
    T = fill_target(low, 0, 0, 255)
    ref = Ref(P, 'ui/text/direct_attack.png', 0, 10, 245, Style((0, 0, 0), 6, 12, 1, 1, 3, 0.5))
    letters, boxes = ref_letters(ref.img, 0, 10, 245, 'DIRECTATACK!!', minarea=100)
    SHEAR = 0.06
    rows_ref = (boxes['D'][1], boxes['D'][1] + boxes['D'][3])
    line = Line(TXT['attack'], 'comic_b')
    kw = dict(sx_lim=(0.92, 1.05), track_lim=(-0.04, 0.03), shear=SHEAR, spf=0.8)
    kw.update(TXT.get('attack_kw', {}))
    p = place_line(low, line, T, ref, rows_ref, TXT.get('rattack', 'AD!'), **kw)[2]
    emb = weight_emb(letters, 'comic_b', 'DIETK', p[2])
    print('attack: stroke correction', emb)
    cov, rgba, p = place_line(low, line, T, ref, rows_ref, TXT.get('rattack', 'AD!'), emb=emb, **kw)
    print('attack: p', p)
    fam.save(PFX + 'dilect_atk00001', to_image(rgba), h, low)
    lowg, _, (hg,) = load(U, 'dilect_atk00003.gim')
    g = soft_flash(lowg, flat_color(common.reference(P, 'ui/text/direct_attack_gray.png')))
    fam.save(PFX + 'dilect_atk00003', to_image(g), hg, lowg)


# ------------------------------------------------------------------------------------------ TURNO (score-top10)
def over(top, bot):
    """'top' RGBA float (alpha 0..1) over 'bot' RGBA float."""
    ta, ba = top[..., 3:], bot[..., 3:]
    a = ta + ba * (1 - ta)
    rgb = (top[..., :3] * ta + bot[..., :3] * ba * (1 - ta)) / np.maximum(a, 1e-6)
    return np.dstack([rgb, a])


def as_float(img):
    a = np.asarray(img, np.float32)
    return np.dstack([a[..., :3], a[..., 3:] / 255])


def badge_background(ref_img, Tr, rows):
    """the English HD badge without its 'TURN': letters + their hard shadow are removed and the soft badge
    gradient under them is inpainted (smooth gradient only, the sharp letters are redrawn separately)."""
    text_m = cv2.dilate((Tr > 0.03).astype(np.uint8), np.ones((3, 3), np.uint8))
    sh_m = np.zeros_like(text_m)
    for dx in range(0, 6):
        for dy in range(0, 5):
            sh_m |= np.roll(np.roll(text_m, dy, 0), dx, 1)
    mask = ((text_m | sh_m) & rows).astype(np.uint8)
    rgb = np.ascontiguousarray(np.asarray(ref_img)[..., :3])
    bg_rgb = cv2.inpaint(rgb, mask * 255, 4, cv2.INPAINT_TELEA).astype(np.float32)
    bg_rgb = np.where(mask[..., None] > 0, cv2.GaussianBlur(bg_rgb, (0, 0), 1.5), bg_rgb)
    # the highlight bar of the English badge carries painterly noise along its length: smooth it along x only
    y0, y1, x0, x1 = 70, 77, 18, 110
    strip = bg_rgb[y0:y1, :]
    sm = cv2.GaussianBlur(strip, (0, 0), sigmaX=7, sigmaY=0.01, borderType=cv2.BORDER_REPLICATE)
    w = np.zeros((y1 - y0, bg_rgb.shape[1]), np.float32)
    w[:, x0:x1] = 1
    w = cv2.GaussianBlur(w, (0, 0), sigmaX=3, sigmaY=0.01)[..., None]
    bg_rgb[y0:y1, :] = strip * (1 - w) + sm * w
    return np.dstack([bg_rgb, as_float(ref_img)[..., 3:]])


def do_turn(fam, U, P):
    """TURNO badges (blue, red): the English badge (soft gradient frame, highlight bar) with its letters replaced
    by 'TURNO' typeset in SF Expanded Black, white gradient fill + hard dark shadow measured on the English badge."""
    placed = None
    for member, rel in (('score-top100011.gim', 'ui/text/turn_blue.png'), ('score-top100013.gim', 'ui/text/turn_red.png')):
        low, _, (h,) = load(U, member)
        img = common.reference(P, rel)
        R = as_float(img)
        Tr = fill_target(img, 1, 80, 250)
        rows = np.zeros(Tr.shape, np.uint8)
        rows[5:33, 3:125] = 1
        bg = badge_background(img, Tr, rows)
        grad, _ = row_gradient(img, Tr, thr=0.9, smooth_px=1)
        cs = np.float32([4, 0, 10])

        def text_layer(cov, p):
            dx, dy, sg, op = p
            return render_style(cov, grad, Style(cs, -1.0, -0.5, dx, dy, max(sg, 0.3), op, cs))
        sel = rows[..., None] > 0
        letters, boxes = ref_letters(img, 1, 80, 250, 'TURN', minarea=80)

        def loss(p):
            o = over(text_layer(Tr, p), bg)
            return float((np.abs(o[..., :3] - R[..., :3]) * sel).sum() / sel.sum() / 3)
        sp, _ = nelder_mead(loss, [3.0, 2.0, 0.6, 1.0], [1.0, 1.0, 0.3, 0.1], 200)
        if placed is None:
            T = fill_target(low, 1, 66, 255)
            T = T * (T > 0.5)
            line = Line(TXT['turn'], 'sfx_black')
            x0, x1, y0, y1 = [v * S for v in extent_sub(T)]
            p = solve_line(line, x0, x1, y1, y1 - y0, TXT['rturn'], (0.92, 1.05), (-0.05, 0.08))
            emb = weight_emb(letters, 'sfx_black', 'TURN', p[2])
            cov = typeset(low, line, p, emb)
            placed = cov
            print('turno: stroke correction', emb, 'p', p)
        out = over(text_layer(placed, sp), bg)
        fam.save(PFX + '' + member[:-4], to_image(out), h, low)


# ------------------------------------------------------------------------------------ card_icon03, card_side
def do_icons_fr(fam, U, P):
    """French: the texture differs from the Italian one only in a 10-pixel cell; start from the HD Italian version
    (already corrected: smooth LP/TURNO digits, border rows emptied) and put the French pixels x4 there without smoothing."""
    base = _os.path.join(HERE, '..', '..', 'PSP', 'TEXTURES', 'ULES00600', 'ui_it', 'duel_texts', 'basic_ii__card_icon03.png')
    hd = np.asarray(Image.open(base).convert('RGBA')).copy()
    fr, _, (h,) = load(U, 'card_icon03.gim')
    it = common.texture(U, 'duel/basic_ii.ehp', 'card_icon03.gim')[0]
    m = np.abs(np.asarray(fr, np.int32) - np.asarray(it, np.int32)).max(-1) > 30
    mm = np.repeat(np.repeat(m, S, 0), S, 1)
    hd[mm] = np.repeat(np.repeat(np.asarray(fr), S, 0), S, 1)[mm]
    fam.save(PFX + 'card_icon03', Image.fromarray(hd, 'RGBA'), h, fr)


def do_icons(fam, U, P):
    if LANG != 'it':
        return do_icons_fr(fam, U, P)
    """card_icon03: the English HD sheet (digits, signs, discs, big numbers, icons: real mod pixels).  The cells
    where the European game differs from the US pack (check mark disc, grey ball, empty pill, TEMPO) take the
    Italian pixels x4 exactly like the neighbouring pixel-art cells of the HD sheet (which are exact 4x copies of
    their low-res cells: hard-edged pixel art, not smoothed)."""
    low, _, (h,) = load(U, 'card_icon03.gim')
    hd = common.reference(P, 'ui/duels/numbers.png').copy()
    nn_ = low.resize((low.width * S, low.height * S), Image.NEAREST)
    for x0, y0, x1, y1 in [(27, 18, 45, 28), (53, 18, 83, 28), (69, 37, 97, 47)]:
        hd.paste(nn_.crop((x0 * S, y0 * S, x1 * S, y1 * S)), (x0 * S, y0 * S))
    fam.save(PFX + 'card_icon03', hd, h, low)
    # card_side (plaid, no text, not in the HD pack): the European English texture holds the same plaid with finer
    # colour depth than the 16-colour Italian one; pixel-exact x4 like the other pixel-art UI textures of the pack
    low, _, (h,) = load(U, 'card_side.gim')
    en = common.texture(U, 'duel/basic_ie.ehp', 'card_side.gim')[0]
    fam.save(PFX + 'card_side', en.resize((en.width * S, en.height * S), Image.NEAREST), h, low)


GROUPS = {'chain': do_chain, 'turn': do_turn, 'next': do_next, 'start': do_start, 'attack': do_attack,
          'icons': do_icons}


def main(argv):
    fam = common.Family('duel_texts', argv[:4])
    sel = argv[4:] or list(GROUPS)
    for name in sel:
        GROUPS[name](fam, fam.usrdir, fam.pack_us)
    fam.finish()


if __name__ == '__main__':
    main(sys.argv)
