"""schermata_vs: HD (4x) Italian textures of the duel intro / VS screen of ULES00600 (duel/start/*.ehp).

  DUELLO / NORMALE / TAG banner words (+ the two blurred pale-yellow glow layers "DUELLO NORMALE" / "DUELLO TAG"),
  "Modalità Singolo" / "Modalità Match", "1° / 2° / 3° Duello", "1° / 2° A GIOCARE" (rock-paper-scissors turn order),
  the janken card sheet (VITTORIA / SCONFITTA / PAREGGIO) and the player-slot sheet d_menu01_i ("n° GIOCATORE").

run:  python3 -I schermata_vs.py USRDIR PACK_US OUT      (writes OUT/ui_it/schermata_vs/<id>.png + OUT/ui_it/schermata_vs.ini)

Method.  The English HD pack (MikeyMK) is a STYLE reference, never a source of letters: its lettering is AI-upscaled
(wobbly outlines, glitches).  For every lettering of the pack the macOS system font whose glyphs best match the mod's real
letters was found by measurement (per-letter overlap + aspect error over all system fonts):
  * big banner words DUEL / NORMAL / TAG ......... Times Bold   (overlap 0.89, aspect error 1 %: the mod's letters ARE Times Bold)
  * SECOND / FIRST TO GO ......................... Futura Bold  (overlap 0.945, aspect error 1.5 %)
  * WIN! / LOSE / DRAW ........................... Hiragino Sans W8 (best of all fonts, 0.84)
  * Single / Match Mode, 1st round ............... heavy gothic: Hiragino Sans W9 (0.90) / Arial Black (0.87); Arial Black is used,
                                                  its accent is as high as its ascenders (the 16 px tall "Modalità Match") and its
                                                  weight is that of the mod's lettering
  * badge lettering "1st PLAYER" ................. Helvetica Regular (0.82); tab lettering "PLAYER" = Arial Black 33 px (142 px
                                                  wide, the pack's "PLAYER" is 144 px)
Every Italian word is typeset with ONE font, ONE size, ONE baseline, ONE stroke weight and ONE style per family; no glyph is
fitted, stretched or moved on its own.  A word longer than the original slot gets a slightly smaller size, tighter tracking
and a whole-word squeeze of at most 10 % (the wide "n° Duello" lettering is widened by 15 % as a whole).  The style
(gradient, bevel, outline, shadow) is rebuilt as clean layers at 4x oversampling (signed distance fields, exact antialiasing)
with the parameters measured on the English HD textures (see STYLE_*).

Flat art (frames, panels, cards) is NOT taken from the pack where the pack's version is AI-upscaled: it is rebuilt from the
LOW-RES Italian original in material classes - 1 px lines drawn crisp at their exact positions (nearest neighbour, dither
removed along the line), smooth colour fields (masked Gaussian / bilateral + bicubic) for the gradients, clouds and
backgrounds, hands cut out by HSV classes and drawn with one uniform outline (see jnk_* / render_art / dm_plates).
Real pack pixels that remain (judged clean at 8x): the interior of the two janken card backs (swirl, KONAMI label,
logo), the OK! buttons, the pointing-hand cursor and the 3 small boxes of the janken sheet; in d_menu01_i the tab frames,
bracket pieces, beige box + avatar, brown bar and the outline / shadow / bevel pixels of the "n° GIOCATORE" badges and tabs
(their body is rebuilt as a smooth vertical gradient, the left notch as an antialiased vector edge, English text removed)."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import font_alt  # noqa: nessun font Apple
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import common

LANG = os.environ.get('TF1_LANG', 'it')
BADGE_TXT = {'it': ['1° GIOCATORE', '2° GIOCATORE'] * 2, 'fr': ['1er JOUEUR', '2e JOUEUR'] * 2, 'es': ['JUGADOR 1', 'JUGADOR 2'] * 2, 'de': ['SPIELER 1', 'SPIELER 2'] * 2, 'en': ['1st PLAYER', '2nd PLAYER'] * 2}[LANG]     # etichette dei 4 distintivi
TAB_WORD, TAB_DW = {'it': ('GIOCATORE', 60), 'fr': ('JOUEUR', -16), 'es': ('JUGADOR', 14), 'de': ('SPIELER', 12), 'en': ('PLAYER', -16)}[LANG]       # linguetta: parola e allargamento (HD px; < 0 = piu' stretta)
SS = 4                                    # oversampling of every drawing (relative to the 4x HD texture)
SYS = '/System/Library/Fonts/'
SUP = '/System/Library/Fonts/Supplemental/'
TIMES_B = (SYS + 'Times.ttc', 1)                       # Times Bold
FUTURA_B = (SUP + 'Futura.ttc', 2)                     # Futura Bold
HIRA_W9 = (SYS + 'ヒラギノ角ゴシック W9.ttc', 0)       # Hiragino Sans W9
HIRA_W8 = (SYS + 'ヒラギノ角ゴシック W8.ttc', 0)       # Hiragino Sans W8
HELV = (SYS + 'Helvetica.ttc', 0)                      # Helvetica Regular
ARIAL_BLACK = (SUP + 'Arial Black.ttf', 0)


# ----------------------------------------------------------------------------------------------------- text engine
_fonts = {}


def font(spec, size):
    k = (spec, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(spec[0], size, index=spec[1])
    return _fonts[k]


def cap_height(spec):
    """cap height / em of a font"""
    return -font(spec, 200).getbbox('H', anchor='ls')[1] / 200.0


def line_mask(spec, text, size, shape, x, base, track=0.0, sx=1.0, ss=SS, space=1.0):
    """fill coverage (float 0..1, supersampled by ss) of one text line on an HD canvas of shape=(H, W).
    size = em in HD px, x = pen start, base = baseline y, track = extra advance per character (HD px, after the
    squeeze), sx = horizontal squeeze of the whole line (about x)."""
    H, W = shape
    f = font(spec, int(round(size * ss)))
    pad = int(size * ss * 0.5)
    xs = []
    sp = f.getlength(' ') * (space - 1.0)                       # extra advance of every space
    for i, ch in enumerate(text):
        xi = (f.getlength(text[:i + 1]) - f.getlength(ch)) if i else 0.0     # includes pair kerning
        xs.append(xi + sp * text[:i].count(' ') + track * ss * i / sx)
    total = f.getlength(text) + sp * text.count(' ') + track * ss * len(text) / sx
    im = Image.new('L', (int(total + 2 * pad) + 8, int(size * ss * 2)), 0)
    d = ImageDraw.Draw(im)
    by = int(size * ss * 1.3)
    for c, xi in zip(text, xs):
        if c != ' ':
            d.text((pad + xi, by), c, font=f, fill=255, anchor='ls')
    a = np.asarray(im, np.float32) / 255
    M = np.float32([[sx, 0, x * ss - pad * sx], [0, 1, base * ss - by]])
    return cv2.warpAffine(a, M, (W * ss, H * ss), flags=cv2.INTER_AREA if sx < 1 else cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def ink_width(spec, text, size, sx=1.0, track=0.0, space=1.0):
    """HD px width of the ink of a line (for fitting a word into a slot)."""
    m = line_mask(spec, text, size, (int(size * 2), int(size * len(text) * 1.5) + 200), 20, size * 1.3, track, sx, ss=1,
                  space=space)
    xs = np.nonzero(m.max(0) > 0.3)[0]
    return float(xs.max() - xs.min() + 1), float(xs.min() - 20)


def sdf(mask):
    """signed distance in px (< 0 inside) of a binarised coverage map."""
    m = (mask > 0.5).astype(np.uint8)
    dout = cv2.distanceTransform(1 - m, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    din = cv2.distanceTransform(m, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
    return (dout - din + np.where(m > 0, 0.5, -0.5)).astype(np.float32)


def rounded(cov, r, ss=SS):
    """soften the corners of a coverage map by r HD px (blur of the distance field: straight edges stay where they are)."""
    if r <= 0:
        return cov
    sd = cv2.GaussianBlur(sdf(cov), (0, 0), r * ss)
    return np.clip(0.5 - sd, 0, 1).astype(np.float32)


def smoothstep(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def shift(a, dx, dy):
    return cv2.warpAffine(a, np.float32([[1, 0, dx], [0, 1, dy]]), (a.shape[1], a.shape[0]), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def grad_table(tab, t):
    ts = np.array([x[0] for x in tab], np.float32)
    return np.stack([np.interp(t, ts, [x[1][c] for x in tab]) for c in range(3)], -1).astype(np.float32)


def render(cov, fill, outline=None, shadow=None, bevel=None, ytop=0.0, ybase=1.0, ss=SS):
    """styled text from a supersampled fill coverage.  Returns an HD float RGBA (straight alpha, 0..255).
    fill    : (r,g,b) or gradient table [(t,(r,g,b))], t = 0 at ytop, 1 at ybase (HD rows)
    outline : dict(col, r, soft)  solid up to r - soft/2 HD px from the fill, fading out at r + soft/2
    shadow  : dict(col, dx, dy, sg, op)  the outline-plus-fill shape shifted by (dx, dy) HD px, blurred sg px
    bevel   : dict(gs, lx, ly, k1, k2, tau)  light/shade inside the fill (normal . light) * exp(-depth / tau)"""
    H, W = cov.shape
    s = sdf(cov)
    d = s / ss
    A_f = np.clip(cov, 0, 1)
    if outline:
        A_o = smoothstep((outline['r'] + outline['soft'] / 2 - d) / outline['soft'])
    else:
        A_o = A_f
    A_u = np.maximum(A_f, A_o)
    if shadow:
        sh = cv2.GaussianBlur(shift(A_u, shadow['dx'] * ss, shadow['dy'] * ss), (0, 0), shadow['sg'] * ss) * shadow['op']
    else:
        sh = np.zeros_like(A_u)
    if isinstance(fill, (tuple, list)) and not isinstance(fill[0], (tuple, list)):
        rgb = np.broadcast_to(np.float32(fill), (H, W, 3)).copy()
    else:
        yy = (np.arange(H, dtype=np.float32) + 0.5) / ss
        t = ((yy - ytop) / (ybase - ytop))[:, None] * np.ones((1, W), np.float32)
        rgb = grad_table(fill, np.clip(t, 0, 1))
    if bevel:
        ds = cv2.GaussianBlur(s / ss, (0, 0), bevel['gs'] * ss)
        gy, gx = np.gradient(ds)
        n = np.sqrt(gx ** 2 + gy ** 2) + 1e-6
        nl = (gx * bevel['lx'] + gy * bevel['ly']) / n
        shade = (bevel['k1'] * nl + bevel['k2']) * np.exp(-np.maximum(-d, 0) / bevel['tau'])
        rgb = rgb + shade[..., None]
    rgb = np.clip(rgb, 0, 255)
    a_out = (A_u - A_f)                       # visible outline (outside the fill)
    a_sh = sh * (1 - A_u)
    co = np.float32(outline['col']) if outline else np.zeros(3, np.float32)
    cs = np.float32(shadow['col']) if shadow else np.zeros(3, np.float32)
    al = A_f + a_out + a_sh
    pm = rgb * A_f[..., None] + co * a_out[..., None] + cs * a_sh[..., None]
    out = cv2.resize(np.dstack([pm, al * 255.0]).astype(np.float32), (W // ss, H // ss), interpolation=cv2.INTER_AREA)
    a = out[..., 3:] / 255.0
    c = np.where(a > 1e-4, out[..., :3] / np.maximum(a, 1e-4), 0)
    return np.dstack([np.clip(c, 0, 255), np.clip(a * 255, 0, 255)])


def bleed(a):
    """colour of the fully transparent texels = colour of the nearest ink (instead of black), so that the bilinear
    filtering of the GPU does not draw a dark fringe around white / coloured edges.  Alpha is untouched."""
    rgb, al = a[..., :3].copy(), a[..., 3] / 255.0
    todo = al < 0.5 / 255
    have = ~todo
    for sg in (2.0, 6.0, 20.0, 60.0):
        if not todo.any():
            break
        w = have.astype(np.float32)
        num = cv2.GaussianBlur(rgb * w[..., None], (0, 0), sg)
        den = cv2.GaussianBlur(w, (0, 0), sg)
        ok = todo & (den > 1e-4)
        rgb[ok] = num[ok] / den[ok][:, None]
        have = have | ok
        todo = ~have
    return np.dstack([rgb, a[..., 3:]])


def to_img(a, fix=True):
    if fix:
        a = bleed(a)
    return Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8), 'RGBA')


# ----------------------------------------------------------------------------------------------------- banner words
# Times Bold, measured on ui/text/{duel_1,normal,tag}.png: size 217-219 px/em, natural width.  The Italian words are
# longer than the English ones: one common size (0.95x), squeeze 0.9 and tracking -14 for all three (the position /
# size within this envelope was chosen by a global search over the low-res original: alpha error within 0.7 of the optimum).
STYLE_BANNER = dict(
    grad=[(0, (253, 28, 105)), (.1, (253, 33, 95)), (.2, (253, 47, 86)), (.3, (253, 67, 75)), (.4, (252, 92, 63)),
          (.5, (250, 117, 50)), (.6, (250, 146, 41)), (.7, (249, 166, 31)), (.8, (248, 188, 17)), (.9, (241, 198, 4)),
          (1, (240, 203, 0))],
    outline=dict(col=(0, 0, 0), r=5.8, soft=5.0),
    shadow=dict(col=(0, 0, 0), dx=2.9, dy=5.0, sg=3.0, op=1.0),
    bevel=dict(gs=2.5, lx=0.87, ly=0.5, k1=-27, k2=-8, tau=15))
BANNER = dict(size=208.0, sx=0.9, track=-14.0, base=152.0, x=6.0)


def banner_word(text, shape):
    p = BANNER
    cov = line_mask(TIMES_B, text, p['size'], shape, p['x'], p['base'], p['track'], p['sx'])
    st = STYLE_BANNER
    return render(cov, st['grad'], st['outline'], st['shadow'], st['bevel'],
                  ytop=p['base'] - cap_height(TIMES_B) * p['size'], ybase=p['base'])


def banner_fit(text, low):
    """francese: le parole DUEL / NORMAL / TAG riempiono la loro texture (il gioco le allarga): dimensione, compressione, posizione e
    linea di base si cercano in modo che il riquadro dell'inchiostro (alfa > 1/2, contorno e ombra compresi) coincida con quello dell'originale."""
    shape = (low.height * 4, low.width * 4)
    A = np.asarray(low.convert('RGBA'), np.float32)[..., 3]
    ys, xs = np.where(A > 128)
    tgt = np.array([xs.min() * 4, (xs.max() + 1) * 4, ys.min() * 4, (ys.max() + 1) * 4], float)
    p = dict(BANNER)
    st = STYLE_BANNER
    for _ in range(6):
        cov = line_mask(TIMES_B, text, p['size'], shape, p['x'], p['base'], p['track'], p['sx'])
        out = render(cov, st['grad'], st['outline'], st['shadow'], st['bevel'], ytop=p['base'] - cap_height(TIMES_B) * p['size'], ybase=p['base'])
        yy, xx = np.where(out[..., 3] > 128)
        cur = np.array([xx.min(), xx.max() + 1, yy.min(), yy.max() + 1], float)
        p['size'] *= (tgt[3] - tgt[2]) / (cur[3] - cur[2])
        p['sx'] = min(max(p['sx'] * ((tgt[1] - tgt[0]) / (cur[1] - cur[0])) / ((tgt[3] - tgt[2]) / (cur[3] - cur[2])), 0.7), 1.3)
        p['x'] += tgt[0] - cur[0]
        p['base'] += tgt[3] - cur[3]
    return render(line_mask(TIMES_B, text, p['size'], shape, p['x'], p['base'], p['track'], p['sx']), st['grad'], st['outline'], st['shadow'],
                  st['bevel'], ytop=p['base'] - cap_height(TIMES_B) * p['size'], ybase=p['base'])


# pale-yellow glow layers: the same Times Bold word, embolden + blur, flat colour (255, 253, 153) as in the originals
# bold / blur are relative to the em size (the ink mass of the two glows lands within 0.1 of the originals')
STYLE_GLOW = dict(col=(255, 253, 153), bold=0.105, blur=0.045, sx=0.9, track=-0.03)


def fit_size(spec, text, width, sx, trf):
    w100, _ = ink_width(spec, text, 100, sx, trf * 100)
    return 100.0 * width / w100


def glow_word(text, shape, width):
    st = STYLE_GLOW
    H, W = shape
    size = fit_size(TIMES_B, text, width, st['sx'], st['track'])
    w, off = ink_width(TIMES_B, text, size, st['sx'], st['track'] * size)
    base = H / 2 + cap_height(TIMES_B) * size / 2
    cov = line_mask(TIMES_B, text, size, shape, (W - w) / 2 - off, base, st['track'] * size, st['sx'])
    cb = np.clip(0.5 - (sdf(cov) / SS - st['bold'] * size) * SS, 0, 1)         # emboldened
    a = cv2.GaussianBlur(cb, (0, 0), st['blur'] * size * SS)
    a = cv2.resize(a, (W, H), interpolation=cv2.INTER_AREA)
    rgb = np.broadcast_to(np.float32(st['col']), (H, W, 3))
    return np.dstack([rgb, a * 255])


def glow_from_original(low):
    """the glow layer redrawn from the ORIGINAL Italian alpha (a blurred, tall and horizontally condensed word that the game
    stretches non-uniformly): smooth bicubic 4x upsample of the alpha + a 1.5 px blur, flat pale yellow.  Used for "DUELLO
    TAG", whose natural-proportion typesetting is 26 % too short for the original layout (the 10-letter word fills the slot
    with fewer rows than the stretched original); the glow has no letterforms to preserve, only mass and extent."""
    a = np.asarray(low.convert('RGBA'), np.float32)[..., 3]
    up = cv2.resize(a, (a.shape[1] * 4, a.shape[0] * 4), interpolation=cv2.INTER_CUBIC)
    up = np.clip(cv2.GaussianBlur(up, (0, 0), 1.5), 0, 255)
    rgb = np.broadcast_to(np.float32(STYLE_GLOW['col']), up.shape + (3,))
    return np.dstack([rgb, up])


def put_line(spec, text, shape, size, base, x_left=None, x_center=None, track=0.0, sx=1.0, ss=SS, space=1.0):
    """fill coverage of a line whose INK starts at x_left (or is centred on x_center)."""
    w, off = ink_width(spec, text, size, sx, track, space)
    x = (x_left if x_left is not None else x_center - w / 2.0) - off
    return line_mask(spec, text, size, shape, x, base, track, sx, ss, space)


def fit_track(spec, text, size, sx, width, space=1.0):
    """tracking (HD px per char) that makes the ink of the line `width` px wide."""
    w0 = ink_width(spec, text, size, sx, 0.0, space)[0]
    return (width - w0) / (len(text) - 1)


# ----------------------------------------------------------------------------------------------------- "1/2 A GIOCARE"
# Futura Bold (measured on ui/text/{second,first}_to_go.png: 80 px/em, tracking 0): black letters, white outline
STYLE_GIOCARE = dict(fill=(2, 1, 3), outline=dict(col=(255, 255, 255), r=7.2, soft=4.5),
                     shadow=dict(col=(255, 255, 255), dx=0.56, dy=0.23, sg=1.86, op=0.89))
GIOCARE = dict(size=76.0, sx=0.96, base=96.0, gap=24.0)


def giocare_word(digit, shape, cx):
    """"n°" + "A GIOCARE" (the ordinal sign hugs its digit, as in the original), centred on cx."""
    p, st = GIOCARE, STYLE_GIOCARE
    w1 = ink_width(FUTURA_B, digit + '°', p['size'], p['sx'])[0]
    w2 = ink_width(FUTURA_B, 'A GIOCARE', p['size'], p['sx'])[0]
    x1 = cx - (w1 + p['gap'] + w2) / 2.0
    cov = np.maximum(put_line(FUTURA_B, digit + '°', shape, p['size'], p['base'], x_left=x1, sx=p['sx']),
                     put_line(FUTURA_B, 'A GIOCARE', shape, p['size'], p['base'], x_left=x1 + w1 + p['gap'], sx=p['sx']))
    return render(cov, st['fill'], st['outline'], st['shadow'])


# ----------------------------------------------------------------------------------------------------- "n Duello"
# white letters, black outline (measured on ui/text/first_round.png).  Arial Black (the heavy weight of the original
# lettering; the digit '1' is 42 HD px tall, the original's is 40 + antialiasing), widened by 15 % as a whole (the mod's lettering is about
# 30 % wider than Arial Black: 'o' w/h 1.6 against 1.23; the rest of the slot is tracking), corners rounded by a
# distance-field blur (rd 2 px) like the rounded lettering of the mod; the digit sits in a fixed digit slot so that
# "° Duello" stays put from 1 to 3.
STYLE_ROUND = dict(fill=(255, 255, 255), outline=dict(col=(0, 0, 0), r=7.6, soft=4.5),
                   shadow=dict(col=(0, 0, 0), dx=0.4, dy=0.55, sg=1.8, op=0.6))
ROUND = dict(size=58.0, sx=1.15, base=55.0, x0=82.0, x1=428.0, space=0.7, rd=2.0)       # position / size: search over the original


def round_word(digit, shape):
    p, st = ROUND, STYLE_ROUND
    slot = max(ink_width(ARIAL_BLACK, d, p['size'], p['sx'])[0] for d in '123')
    cov = put_line(ARIAL_BLACK, digit, shape, p['size'], p['base'], x_center=p['x0'] + slot / 2, sx=p['sx'])
    tx = p['x0'] + slot + 5.0
    track = fit_track(ARIAL_BLACK, '° Duello', p['size'], p['sx'], p['x1'] - tx, p['space'])
    tail = put_line(ARIAL_BLACK, '° Duello', shape, p['size'], p['base'], x_left=tx, track=track, sx=p['sx'], space=p['space'])
    cov = rounded(np.maximum(cov, tail), p['rd'])
    return render(cov, st['fill'], st['outline'], st['shadow'])


def giocare_text(text, shape, left, right):
    """francese: l'intera frase ('DEUXIÈME À JOUER'), il cui inchiostro occupa left..right (HD px, misurati sull'originale)."""
    p, st = GIOCARE, STYLE_GIOCARE
    track = fit_track(FUTURA_B, text, p['size'], p['sx'], right - left)
    cov = put_line(FUTURA_B, text, shape, p['size'], p['base'], x_left=left, track=track, sx=p['sx'])
    return render(cov, st['fill'], st['outline'], st['shadow'])


def round_text(text, shape, left, right):
    """francese: '1er round' / '2e round' / '3e round' in una riga, l'inchiostro occupa left..right (HD px)."""
    p, st = ROUND, STYLE_ROUND
    track = fit_track(ARIAL_BLACK, text, p['size'], p['sx'], right - left, p['space'])
    cov = rounded(put_line(ARIAL_BLACK, text, shape, p['size'], p['base'], x_left=left, track=track, sx=p['sx'], space=p['space']), p['rd'])
    return render(cov, st['fill'], st['outline'], st['shadow'])


# ----------------------------------------------------------------------------------------------------- "Modalita' ..."
# Arial Black (heavy; its accent is as high as its ascenders, so the grave of "a" fits in the 16 px tall texture),
# white outline, hard dark shadow (measured on ui/text/{singlemode,match_mode}.png); fill colours of the mod's HD art
STYLE_MODE = dict(outline=dict(col=(255, 255, 255), r=7.8, soft=4.5),
                  shadow=dict(col=(0, 0, 0), dx=3.6, dy=3.8, sg=0.7, op=0.53))
MODE = dict(size=58.0, sx=0.93, rd=0.8)
FILL_SINGLE = (1, 84, 166)
FILL_MATCH = [(0, (192, 16, 70)), (.3, (178, 6, 74)), (1, (172, 10, 75))]


def mode_word(text, shape, fill, base, left, right):
    p, st = MODE, STYLE_MODE
    track = fit_track(ARIAL_BLACK, text, p['size'], p['sx'], right - left)
    cov = rounded(put_line(ARIAL_BLACK, text, shape, p['size'], base, x_left=left, track=track, sx=p['sx']), p['rd'])
    return render(cov, fill, st['outline'], st['shadow'], ytop=base - 0.725 * p['size'], ybase=base)


# ----------------------------------------------------------------------------------------------------- janken sheet
# jnk_card01 (512x256 -> 2048x1024): six janken cards (rock / scissors / paper, blue and pink row, cell 80 x 116 px), two
# card backs, then the Italian label strip (VITTORIA / SCONFITTA / PAREGGIO), the OK! buttons, the cursor and 3 small boxes.
# The card art of the pack's ui/janken.png is AI-upscaled (mottled, haloed double outlines, soft bevels), so it is NOT
# copied: every card is rebuilt from the LOW-RES Italian art in classes (see jnk_cell / render_art):
#   * frame lines (3 px ring, name strip, art frame, description box, corner accents): the 1 px lines of the original,
#     drawn as crisp 4 px lines at the exact pixel positions (nearest neighbour; the dither of a line is removed by a
#     running median along the line, its gradient is kept);
#   * body / name strip / description fills: smooth masked-Gaussian colour field of the original's cloud pattern, bicubic;
#   * art background: median + bilateral denoised colour field of the original art, bicubic, hand region filled;
#   * hand: the skin class is cut out (HSV classes), its silhouette smoothed (blurred mask -> signed distance), and drawn
#     as ONE uniform outline (thin dark brown line, pale two-tone halo outside, width constant) around a gently graded skin
#     field; the dark finger creases are drawn as strokes from the original's dark pixels.
# Kept from the pack (real mod pixels): the interior of the two card backs (swirl art, KONAMI label, logo: a clean
# vector-like drawing), the OK! buttons, the cursor and the small boxes.  The backs' 3 px frame is redrawn crisp.
# Labels: Hiragino Sans W8 (best match of the mod's labels), one size / one squeeze for the three words, flat fills.
STYLE_JNK = dict(outline=dict(col=(0, 0, 0), r=7.0, soft=4.0), shadow=dict(col=(0, 0, 0), dx=0.3, dy=0.4, sg=1.5, op=0.9))
JNK = dict(size=52.5, sx=0.9, base=997.0, rd=1.0, clear_y=930, clear_x=960,
           words=[('VITTORIA', (255, 250, 0), 24.0), ('SCONFITTA', (46, 80, 252), 323.0), ('PAREGGIO', (209, 0, 101), 666.0)])
if LANG == 'fr':     # (testo, colore, sinistra, destra) misurati sull'originale francese; la larghezza si ottiene con il tracking
    JNK.update(size=81.0, base=1017.0)       # le lettere francesi sono alte 17 righe (68 HD px), quelle italiane 11
    JNK['words'] = [('GAGNÉ', (255, 250, 0), 16.0, 300.0), ('PERDU', (46, 80, 252), 340.0, 624.0), ('EGALITE', (209, 0, 101), 668.0, 936.0)]

if LANG == 'es':
    JNK.update(size=81.0, base=1017.0)
    JNK['words'] = [('GANAS', (255, 250, 0), 16.0, 284.0), ('PIERDES', (46, 80, 252), 336.0, 628.0), ('EMPATE', (209, 0, 101), 656.0, 936.0)]

if LANG == 'de':     # le parole tedesche sono alte 11 righe come le italiane; larghezze misurate sull'originale tedesco
    JNK['words'] = [('GEWONNEN', (255, 250, 0), 16.0, 304.0), ('VERLOREN', (46, 80, 252), 340.0, 620.0), ('UNENTSCHIEDEN', (209, 0, 101), 656.0, 940.0)]

CW, CH = 80, 116                                   # card cell in low-res px (pitch 80 x 116)


def rect_mask(rects, shape=(CH, CW)):
    m = np.zeros(shape, bool)
    for x0, y0, x1, y1 in rects:
        m[y0:y1 + 1, x0:x1 + 1] = True
    return m


# geometry of a card cell (low-res px, inclusive) - read off the original
RING = rect_mask([(0, 0, 79, 2), (0, 113, 79, 115), (0, 3, 2, 112), (77, 3, 79, 112)])
STRIP_BOX, STRIP_IN = (6, 5, 74, 16), (8, 7, 72, 14)
ART_BOX, ART_IN = (8, 22, 71, 85), (11, 25, 68, 82)
DESC_BOX, DESC_IN = (6, 87, 74, 110), (8, 89, 71, 108)
M_STRIP_IN, M_ART_IN, M_DESC_IN = rect_mask([STRIP_IN]), rect_mask([ART_IN]), rect_mask([DESC_IN])
M_BOXES = rect_mask([STRIP_BOX, ART_BOX, DESC_BOX])
M_STRUCT = RING | (M_BOXES & ~M_STRIP_IN & ~M_ART_IN & ~M_DESC_IN)          # 1 px frame lines, corner accents, ring
M_BODY = ~RING & ~M_BOXES
# straight line runs (row / column, from, to): the dither is removed along the run (end / corner pixels stay raw)
H_RUNS = [(r, 3, 76) for r in (0, 1, 2, 113, 114, 115)] + [(r, 8, 72) for r in (5, 6, 15, 16)] + \
         [(r, 12, 67) for r in (22, 23, 24, 83, 84, 85)] + [(r, 9, 71) for r in (87, 88, 109, 110)]
V_RUNS = [(c, 3, 112) for c in (0, 1, 2, 77, 78, 79)] + [(c, 8, 14) for c in (6, 7, 73, 74)] + \
         [(c, 28, 80) for c in (8, 9, 10, 69, 70, 71)] + [(c, 91, 107) for c in (6, 7, 72, 73, 74)]
ART_X, ART_Y = 11, 25                              # art window of the cell (58 x 58 px)

# hand style (HD px); colours are those of the original's hand pixels (outline / halo measured on the low-res art)
JNK_ART = dict(sig_s=1.25, bil=(25, 2.0), sig_bg2=0.8, sig_bg=0.8, sig_sk=0.7, u_bg=(1.6, 0.6), u_sk=(1.6, 0.6),
               w_o=2.0, w_h=6.0, a_h=0.9, c_h1=(105, 101, 99), c_h2=(225, 230, 228), t_mid=0.7, c_o=(80, 55, 35),
               sig_l=0.4, thr_l=0.42, k_l=8, a_l=0.9, c_l=(110, 76, 44), min_inner=3)
ART_PAD = 6


def hsv_deg(rgb):
    hsv = cv2.cvtColor((np.asarray(rgb, np.float32) / 255).astype(np.float32), cv2.COLOR_RGB2HSV)
    return hsv[..., 0], hsv[..., 1], hsv[..., 2]


def norm_conv(img, mask, sigma):
    """masked Gaussian smoothing of an image (H, W, 3): only the pixels of `mask` count; wider kernels fill the holes."""
    w = mask.astype(np.float32)
    out = np.zeros(img.shape, np.float32)
    have = np.zeros(mask.shape, bool)
    for sg in (sigma, sigma * 2.5, sigma * 6, sigma * 16):
        num = cv2.GaussianBlur(img * w[..., None], (0, 0), sg, borderType=cv2.BORDER_REPLICATE)
        den = cv2.GaussianBlur(w, (0, 0), sg, borderType=cv2.BORDER_REPLICATE)
        ok = (den > 0.02) & ~have
        out[ok] = num[ok] / den[ok][:, None]
        have |= ok
        if have.all():
            break
    return out


def unsharp(img, sig, amt):
    return img + amt * (img - cv2.GaussianBlur(img, (0, 0), sig, borderType=cv2.BORDER_REPLICATE))


def fill_holes(P):
    lab = cv2.connectedComponents(np.pad((~P).astype(np.uint8), 1, constant_values=1), connectivity=4)[1]
    outside = (lab == lab[0, 0])[1:-1, 1:-1]
    return P | (~outside & ~P)


def hand_mask(A):
    """skin / hand silhouette (skin + the dark outline pixels touching it, holes filled) and the dark-pixel class of a
    low-res art crop A (58 x 58 x 3)."""
    h, s, v = hsv_deg(A)
    skin = (h >= 22) & (h <= 44) & (s >= .26) & (s <= .6) & (v >= .6)
    n, lab, st, _ = cv2.connectedComponentsWithStats(skin.astype(np.uint8), connectivity=4)
    comp = lab == (1 + np.argmax(st[1:, cv2.CC_STAT_AREA]))
    dark = (h >= 8) & (h <= 48) & (s > .28) & (v < .6) & (v > .15)
    near = cv2.dilate(comp.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))) > 0
    return fill_holes(comp | (dark & near)), comp, dark


def render_art(A, prm=JNK_ART):
    """HD (4x) RGB of one janken art window from its low-res crop A (58 x 58 x 3, float): smooth background colour field +
    the hand drawn as clean shapes (uniform outline and halo, graded skin, crease strokes)."""
    H, W = A.shape[:2]
    P, comp, dark = hand_mask(A)
    h, s, v = hsv_deg(A)
    f = 4 * SS                                                   # supersampled grid = 16 x low-res
    # silhouette: blurred mask -> signed distance (SS px, < 0 inside); edge-replicated so that the cut at the window stays open
    big = cv2.resize(np.pad(P, ART_PAD, mode='edge').astype(np.float32), ((W + 2 * ART_PAD) * f, (H + 2 * ART_PAD) * f),
                     interpolation=cv2.INTER_NEAREST)
    c = ART_PAD * f
    d_ss = sdf(cv2.GaussianBlur(big, (0, 0), prm['sig_s'] * f) > 0.5)[c:c + H * f, c:c + W * f]
    # colour fields (low-res, smooth)
    Am = cv2.medianBlur(A.astype(np.uint8), 3)
    near = cv2.dilate(P.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    near |= (s < .22) & (v > .4) & (cv2.dilate(P.astype(np.uint8), np.ones((11, 11), np.uint8)) > 0)    # halo pixels
    Ab = cv2.bilateralFilter(cv2.medianBlur(A.astype(np.uint8), 5), 5, prm['bil'][0], prm['bil'][1],
                             borderType=cv2.BORDER_REPLICATE).astype(np.float32)          # 5x5 median: stray palette dots go
    bg = np.where(near[..., None], norm_conv(Ab, ~near, prm['sig_bg']), Ab)
    bg = unsharp(cv2.GaussianBlur(bg, (0, 0), prm['sig_bg2'], borderType=cv2.BORDER_REPLICATE), *prm['u_bg'])
    skinm = (cv2.erode(P.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0) & ~dark
    sk = unsharp(norm_conv(Am.astype(np.float32), skinm, prm['sig_sk']), *prm['u_sk'])
    bg_ss = cv2.resize(bg, (W * f, H * f), interpolation=cv2.INTER_CUBIC)
    sk_ss = cv2.resize(sk, (W * f, H * f), interpolation=cv2.INTER_CUBIC)
    # layers: background, halo (two-tone, constant width), outline, skin
    cov_in = np.clip(0.5 - d_ss, 0, 1)
    cov_core = np.clip(0.5 - (d_ss + prm['w_o'] * SS), 0, 1)
    cov_h = np.clip(0.5 - (d_ss - prm['w_h'] * SS), 0, 1)
    t = smoothstep(np.clip(d_ss / (prm['w_h'] * SS), 0, 1)[..., None] / prm['t_mid'])
    c_h = np.float32(prm['c_h1']) * (1 - t) + np.float32(prm['c_h2']) * t
    a_h = cov_h[..., None] * prm['a_h']
    rgb = bg_ss * (1 - a_h) + c_h * a_h
    rgb = rgb * (1 - cov_in[..., None]) + np.float32(prm['c_o']) * cov_in[..., None]
    rgb = rgb * (1 - cov_core[..., None]) + sk_ss * cov_core[..., None]
    # crease strokes: dark-pixel components of the hand that run into its interior
    inner = cv2.erode(P.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    n, lab = cv2.connectedComponents((dark & P).astype(np.uint8), connectivity=8)
    lines = np.zeros_like(P)
    for i in range(1, n):
        m = lab == i
        if (m & inner).sum() >= prm['min_inner']:
            lines |= m
    lb = cv2.resize(np.pad(lines, ART_PAD).astype(np.float32), ((W + 2 * ART_PAD) * f, (H + 2 * ART_PAD) * f),
                    interpolation=cv2.INTER_NEAREST)
    lb = cv2.GaussianBlur(lb, (0, 0), prm['sig_l'] * f)[c:c + H * f, c:c + W * f]
    cov_l = np.clip((lb - prm['thr_l']) * prm['k_l'] + 0.5, 0, 1) * cov_core * prm['a_l']
    rgb = rgb * (1 - cov_l[..., None]) + np.float32(prm['c_l']) * cov_l[..., None]
    return np.clip(cv2.resize(rgb, (W * 4, H * 4), interpolation=cv2.INTER_AREA), 0, 255)


def run_mask(runs, horizontal):
    m = np.zeros((CH, CW), bool)
    for k, a, b in runs:
        if horizontal:
            m[k, a:b + 1] = True
        else:
            m[a:b + 1, k] = True
    return m


M_HRUN, M_VRUN = run_mask(H_RUNS, True), run_mask(V_RUNS, False)


def run_smooth(S, runs, horizontal, sg=2.0):
    """smooth the colour of every straight line run ALONG the run (Gaussian, sg px): removes the dither of the 1 px line
    and keeps its gradient; the end / corner pixels outside the runs stay raw."""
    out = S.copy()
    for k, a, b in runs:
        line = S[k, a:b + 1, :3] if horizontal else S[a:b + 1, k, :3]
        n = len(line)
        idx = np.arange(n)
        w = np.exp(-0.5 * ((idx[:, None] - idx[None, :]) / sg) ** 2)
        sm = (w @ line) / w.sum(1, keepdims=True)
        if horizontal:
            out[k, a:b + 1, :3] = sm
        else:
            out[a:b + 1, k, :3] = sm
    return out


def up_nn(a, f=4):
    return cv2.resize(a, (a.shape[1] * f, a.shape[0] * f), interpolation=cv2.INTER_NEAREST)


def up_lines(S):
    """4x upsample of the line pixels of S: nearest neighbour across a line, linear along it (no 4 px steps of colour)."""
    H, W = S.shape[:2]
    hr = np.repeat(cv2.resize(S[..., :3], (W * 4, H), interpolation=cv2.INTER_LINEAR), 4, axis=0)
    vr = np.repeat(cv2.resize(S[..., :3], (W, H * 4), interpolation=cv2.INTER_LINEAR), 4, axis=1)
    out = up_nn(S[..., :3])
    mh, mv = up_nn(M_HRUN.astype(np.uint8)) > 0, up_nn(M_VRUN.astype(np.uint8)) > 0
    out[mh] = hr[mh]
    out[mv] = vr[mv]
    return out


def smooth_lines(cell):
    return run_smooth(run_smooth(cell, H_RUNS, True), V_RUNS, False)


def jnk_frame(cell):
    """crisp HD frame (464 x 320 RGBA float) of one card cell from its low-res RGBA (116 x 80 x 4); the art window is left
    as body colour, to be overwritten."""
    S = smooth_lines(cell)
    rgb = S[..., :3]
    out = cv2.resize(norm_conv(rgb, M_BODY, 0.8), (CW * 4, CH * 4), interpolation=cv2.INTER_CUBIC)
    for M in (M_STRIP_IN, M_DESC_IN):                            # the two inner fills have their own colour field
        fld = cv2.resize(norm_conv(rgb, M, 1.0), (CW * 4, CH * 4), interpolation=cv2.INTER_CUBIC)
        Mu = up_nn(M.astype(np.uint8)) > 0
        out[Mu] = fld[Mu]
    Su = up_nn(M_STRUCT.astype(np.uint8)) > 0
    ln = up_lines(S)
    out[Su] = ln[Su]
    return np.dstack([out, up_nn(cell[..., 3])])


def jnk_back(cell, hd_cell):
    """card back: the pack's swirl art kept inside, the 3 px bevelled frame redrawn crisp from the original's pixels."""
    S = smooth_lines(cell)
    Ru = up_nn(RING.astype(np.uint8)) > 0
    out = hd_cell.copy()
    out[Ru, :3] = up_lines(S)[Ru]
    out[Ru, 3] = up_nn(cell[..., 3])[Ru]
    return out


def jnk_cards(low, base_img):
    """paint the 6 cards and 2 backs (HD rows 0..927, columns 0..1279) of the sheet `base_img` in place."""
    L = np.asarray(low.convert('RGBA'), np.float32)
    for r in (0, 1):
        fr = jnk_frame(L[CH * r:CH * (r + 1), 0:CW])
        for k in range(3):
            cell = fr.copy()
            A = L[ART_Y:ART_Y + 58, ART_X + CW * k:ART_X + CW * k + 58, :3]          # the art is the same in both rows
            cell[ART_Y * 4:(ART_Y + 58) * 4, ART_X * 4:(ART_X + 58) * 4, :3] = render_art(A)
            cell[ART_Y * 4:(ART_Y + 58) * 4, ART_X * 4:(ART_X + 58) * 4, 3] = 255
            base_img[464 * r:464 * (r + 1), 320 * k:320 * (k + 1)] = cell
        y0 = 464 * r
        base_img[y0:y0 + 464, 960:1280] = jnk_back(L[CH * r:CH * (r + 1), 240:320], base_img[y0:y0 + 464, 960:1280])


def jnk_sheet(pack_us, low):
    base_img = np.asarray(common.reference(pack_us, 'ui/janken.png'), np.float32).copy()
    jnk_cards(low, base_img)
    p, st = JNK, STYLE_JNK
    y0 = 896                                                    # strip canvas = HD rows 896..1023
    shape = (1024 - y0, p['clear_x'])
    strip = np.zeros(shape + (4,), np.float32)
    for text, col, left, *right in p['words']:
        sx = p['sx']
        if right and LANG != 'it':          # larghezza dell'originale: prima la compressione (0.8-1.15), poi il tracking
            sx = min(max((right[0] - left) / ink_width(HIRA_W8, text, p['size'], 1.0)[0], 0.8), 1.15)
        tr = fit_track(HIRA_W8, text, p['size'], sx, right[0] - left) if right else 0.0
        cov = rounded(put_line(HIRA_W8, text, shape, p['size'], p['base'] - y0, x_left=left, sx=sx, track=tr), p['rd'])
        w = render(cov, col, st['outline'], st['shadow'])
        a = w[..., 3:] / 255.0
        strip[..., :3] = w[..., :3] * a + strip[..., :3] * (1 - a)       # words never overlap: plain "over" is exact
        strip[..., 3:] = np.maximum(strip[..., 3:], w[..., 3:])
    strip = bleed(strip)
    cy = p['clear_y']
    reg = base_img[cy:, :p['clear_x']]
    reg[:] = strip[cy - y0:]
    return to_img(base_img, fix=False)


# ----------------------------------------------------------------------------------------------------- player-slot sheet
# d_menu01_i (256x256).  The two panels and two bars are rebuilt from the low-res original (dm_plates).  Frames of the player
# tabs, bracket pieces, beige box and brown bar are the pack's own art (the same drawing in the Italian sheet, whose game
# only differs in dither) and are reused.  Redrawn: the four "n° GIOCATORE" badges (pack badge: bevel / outline / shadow
# pixels kept, English text removed, body = smooth vertical gradient, left notch = vector edge, see badge_clean), the
# "GIOCATORE" tab (the pack tab widened with the row-fill method) and the eight icon + digit tabs of the European game
# (the pack has "1P" there).
PACK_DM = 'ui/misc/00000000a5c5fc7813b292a5.png'
DM_BADGE = dict(x0=596, x1=916, h=56, pitch=60, size=42.0, sx=0.94, left=20.0, base=43.0, space=0.8, bold=0.8,
                grad=[(0, (255, 255, 255)), (1, (228, 226, 226))])
# tabs: text group centre x, text top y (HD) of the pack's "nP" tabs
DM_TABS = [(64, 520), (164, 648), (264.5, 776), (363.5, 904), (672, 928), (772, 928), (872, 928), (971.5, 928)]
DM_TABTEXT = dict(size=33.0)           # Arial Black: cap height 24 HD px and "PLAYER" 142 px wide like the pack's tab lettering


def over(dst, src, x, y):
    """alpha-composite straight-alpha float RGBA src onto dst at (x, y)."""
    h, w = src.shape[:2]
    if x < 0 or y < 0 or x + w > dst.shape[1] or y + h > dst.shape[0]:        # clip to the destination
        x0, y0 = max(x, 0), max(y, 0)
        x1, y1 = min(x + w, dst.shape[1]), min(y + h, dst.shape[0])
        src, x, y = src[y0 - y:y1 - y, x0 - x:x1 - x], x0, y0
        h, w = src.shape[:2]
    reg = dst[y:y + h, x:x + w]
    a = src[..., 3:] / 255.0
    ao = reg[..., 3:] / 255.0
    at = a + ao * (1 - a)
    c = np.where(a > 1e-6, (src[..., :3] * a + reg[..., :3] * ao * (1 - a)) / np.maximum(at, 1e-6), reg[..., :3])
    reg[..., :3] = c                                   # pixels the source does not touch stay bit-exact
    reg[..., 3:] = np.where(a > 1e-6, at * 255.0, reg[..., 3:])


def draw_icon(ss=8):
    """the little "player" bust of the tabs (24 x 32 HD px), drawn from shapes: black outline, tan face with a darker
    brow / lighter highlight, purple shirt (the colours of the 6 x 8 px original)."""
    W, H = 24, 32
    yy, xx = (np.mgrid[0:H * ss, 0:W * ss].astype(np.float32) + 0.5) / ss

    def ell(cx, cy, rx, ry):
        return 0.5 - np.clip((np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) - 1) * min(rx, ry) * ss, -0.5, 0.5)

    def rrect(x0, y0, x1, y1, rt, rb):
        # rounded rectangle, radius rt on the two top corners, rb on the two bottom ones (signed distance, then coverage)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        r = np.where(yy < cy, rt, rb)
        qx = np.abs(xx - cx) - ((x1 - x0) / 2 - r)
        qy = np.abs(yy - cy) - ((y1 - y0) / 2 - r)
        d = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2) + np.minimum(np.maximum(qx, qy), 0) - r
        return np.clip(0.5 - d * ss, 0, 1)

    head_o, head_f = ell(12, 10.5, 12.0, 10.6), ell(12, 10.8, 8.4, 7.6)
    body_o, body_f = rrect(0, 19, 24, 32, 8, 1.2), rrect(3, 22, 21, 29, 5, 1)
    outline = np.maximum(head_o, body_o)
    # face: lower edge tone a6915c, centre highlight dfcd9f, brow band 816743
    hl = np.exp(-(((xx - 11.2) / 4.6) ** 2 + ((yy - 11.5) / 4.8) ** 2))
    face = np.float32([0xa6, 0x91, 0x5c]) * (1 - hl[..., None]) + np.float32([0xdf, 0xcd, 0x9f]) * hl[..., None]
    brow = smoothstep((7.6 - yy) / 2.6)[..., None]
    face = face * (1 - brow) + np.float32([0x81, 0x67, 0x43]) * brow
    # shirt: bright centre a946f3 -> 5a0998 at the sides
    sx_ = np.clip(np.abs(xx - 12) / 8.5, 0, 1)[..., None]
    shirt = np.float32([0xa9, 0x46, 0xf3]) * (1 - sx_ ** 1.5) + np.float32([0x5a, 0x09, 0x98]) * sx_ ** 1.5
    rgb = np.zeros((H * ss, W * ss, 3), np.float32)
    a = outline.copy()
    for cov, col in [(head_f, face), (body_f, shirt)]:
        rgb = rgb * (1 - cov[..., None]) + col * cov[..., None]
    return premul_down(rgb, a, ss)


def premul_down(rgb, alpha, ss):
    H, W = alpha.shape
    pm = np.dstack([rgb * alpha[..., None], alpha[..., None] * 255.0]).astype(np.float32)
    d = cv2.resize(pm, (W // ss, H // ss), interpolation=cv2.INTER_AREA)
    a = d[..., 3:] / 255.0
    return np.dstack([np.where(a > 1e-4, d[..., :3] / np.maximum(a, 1e-4), 0), d[..., 3:]])


def erase_text(img, x0, x1, y0, y1, cols):
    """replace the text zone by the per-row median of the sample columns `cols` (the plain body of the badge / tab)."""
    for y in range(y0, y1):
        img[y, x0:x1] = np.median(img[y, cols], axis=0)


BADGE_X0, BADGE_X1 = 15, 306            # columns of a badge cell whose body is rebuilt (between the left and right bevel)
# left end of the badge (HD px, badge cell coordinates): the notch edge is the line x = 11.5 - 0.456 y, then x = 0 (vertical)
BADGE_NOTCH = dict(x0=11.5, k=0.456, ymax=24.8)


def badge_text_mask(sub):
    """English lettering of a badge (white letters) with their shade: pixels NOT to be used for the body colour."""
    wh = ((sub[..., :3].min(2) > 150) & (sub[..., 3] > 250)).astype(np.uint8)
    wh = cv2.morphologyEx(wh, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    return cv2.dilate(wh, np.ones((13, 13), np.uint8)) > 0


def badge_clean(sub):
    """a badge cell (56 x 320 RGBA float) of the pack without its English text and with a clean left notch.
    Body rows: one robust colour per row (median of the text-free pixels, outliers rejected), smoothed along y, so the body
    is a smooth vertical-only gradient; bevel rows (highlight at the top, dark bands at the bottom) keep the pack's pixels
    and only the pixels under the text are re-interpolated along x; the notch diagonal is redrawn as an antialiased line
    with the cross-section of the straight left edge (outline -> highlight -> body)."""
    H, W = sub.shape[:2]
    X0, X1 = BADGE_X0, BADGE_X1
    out = sub.copy()
    txt = badge_text_mask(sub)
    ok = (sub[..., 3] > 250) & ~txt
    prof = np.full((H, 3), np.nan, np.float32)
    for y in range(3, 50):
        m = ok[y, X0:X1]
        if m.sum() >= 10:
            px = sub[y, X0:X1][m][:, :3]
            keep = np.abs(px - np.median(px, axis=0)).max(1) < 25
            if keep.sum() >= 8:
                prof[y] = np.median(px[keep], axis=0)
    rows = np.arange(H)
    val = ~np.isnan(prof[:, 0])
    for c in range(3):
        prof[:, c] = np.interp(rows, rows[val], prof[val, c])
    sm = prof.copy()                                              # body rows 8..43: smoothed along y
    seg = prof[8:44]
    kern = np.exp(-0.5 * (np.arange(-4, 5) / 1.5) ** 2)
    kern /= kern.sum()
    pad = np.pad(seg, ((4, 4), (0, 0)), mode='edge')
    sm[8:44] = np.stack([np.convolve(pad[:, c], kern, mode='valid') for c in range(3)], -1)
    for y in range(8, 44):
        out[y, X0:X1, :3] = sm[y]
    xs = np.arange(X0, X1)
    for y in range(3, 8):                                         # top highlight rows: keep the pack's pixels (they brighten
        good = ~txt[y, X0:X1] & (sub[y, X0:X1, 3] > 250)          # towards the right), re-interpolate under the text only
        if good.sum() >= 8:
            for c in range(3):
                out[y, X0:X1, c] = np.interp(xs, xs[good], sub[y, X0:X1, c][good])
    for y in range(44, 50):                                       # bottom dark bands are uniform along x (the glint of the
        good = ~txt[y, X0:X1] & (sub[y, X0:X1, 3] > 250) & (xs < 285)      # right corner is outside the zone)
        if good.sum() >= 8:
            out[y, X0:X1, :3] = np.median(sub[y, X0:X1][good][:, :3], axis=0)
    # ---- left notch: cross-section of the straight left edge (rows 28..40), laid along the vector edge
    P = np.median(sub[28:41, 0:16], axis=0)                       # 16 x RGBA, column x = signed distance s = x + 0.5
    n = BADGE_NOTCH
    R = (slice(0, 30), slice(0, 34))
    yy, xx = np.mgrid[R[0], R[1]].astype(np.float32) + 0.5
    s_diag = (xx + n['k'] * yy - n['x0']) / np.sqrt(1 + n['k'] ** 2)
    s_L = np.minimum(s_diag, xx)                                  # inward distance to the left boundary (convex shape)
    s_top = yy
    sc = 0.5 + np.arange(16, dtype=np.float32)
    col = np.stack([np.interp(s_L, sc, P[:, c]) for c in range(3)], -1)
    wb = smoothstep((s_L - 8.0) / 6.0)[..., None]                 # beyond the bevel: the row body colour
    body = np.broadcast_to(sm[:30, None, :], (30, 34, 3))
    col = col * (1 - wb) + body * wb
    al = np.where(s_L < 0.5, np.clip(P[0, 3] / 255 + 0.26 * (s_L - 0.5), 0, 1), np.interp(s_L, sc, P[:, 3] / 255)) * 255
    w = np.clip(0.5 + (s_top - s_L) / 3.0, 0, 1)[..., None]       # left profile where the notch edge is nearer than the top
    reg = out[R[0], R[1]]
    reg[..., :3] = reg[..., :3] * (1 - w) + col * w
    reg[..., 3] = reg[..., 3] * (1 - w[..., 0]) + al * w[..., 0]
    out[R[0], R[1]] = reg
    return out


# the two big panels and the two bars (frame of flat 1 px lines + a vertical gradient that is exactly constant along x in the
# original): rebuilt from the low-res original, the frame lines crisp (nearest neighbour = the exact 4 px lines, shadow and
# chamfered corners included), the gradient as a smooth bicubic ramp of the original's row colours, the little "player"
# icons of the bars as crisp 4 px pixel art.  plate rect (incl. shadow), interior rect, icon rect (all low-res, inclusive)
DM_PLATES = [((0, 0, 71, 71), (3, 3, 66, 66), None), ((72, 0, 143, 71), (75, 3, 138, 66), None),
             ((0, 72, 147, 95), (3, 75, 143, 90), (6, 78, 15, 89)), ((0, 96, 147, 119), (3, 99, 143, 114), (6, 102, 15, 113))]


def dm_plates(out, it):
    L = np.asarray(it.convert('RGBA'), np.float32)
    for (px0, py0, px1, py1), (ix0, iy0, ix1, iy1), icon in DM_PLATES:
        patch = np.repeat(np.repeat(L[py0:py1 + 1, px0:px1 + 1], 4, axis=0), 4, axis=1)       # exact 4 px lines, shadow, corners
        cols = np.arange(ix0, ix1 + 1)
        if icon:
            cols = cols[(cols < icon[0]) | (cols > icon[2])]
        prof = np.median(L[iy0:iy1 + 1][:, cols, :3], axis=1)                              # one colour per row
        prof = cv2.GaussianBlur(prof.reshape(-1, 1, 3), (0, 0), 0.8, borderType=cv2.BORDER_REPLICATE)
        ramp = cv2.resize(prof, (1, prof.shape[0] * 4), interpolation=cv2.INTER_CUBIC)       # smooth vertical gradient
        h, w = (iy1 - iy0 + 1) * 4, (ix1 - ix0 + 1) * 4
        fill = np.broadcast_to(ramp.reshape(h, 1, 3), (h, w, 3))
        y0, x0 = (iy0 - py0) * 4, (ix0 - px0) * 4
        reg = patch[y0:y0 + h, x0:x0 + w]
        if icon:                                                    # icon (+ its shadow) stays pixel art over the gradient
            keep = np.zeros((iy1 - iy0 + 1, ix1 - ix0 + 1), bool)
            keep[icon[1] - iy0:icon[3] - iy0 + 1, icon[0] - ix0:icon[2] - ix0 + 1] = True
            diff = np.abs(L[iy0:iy1 + 1, ix0:ix1 + 1, :3] - prof[:, 0][:, None, :]).max(2) > 12
            keep &= diff
            km = np.repeat(np.repeat(keep, 4, axis=0), 4, axis=1)
            reg[~km, :3] = fill[~km]
        else:
            reg[..., :3] = fill
        out[py0 * 4:(py1 + 1) * 4, px0 * 4:(px1 + 1) * 4] = bleed(patch)


def dm_sheet(pack_us, it):
    H = np.asarray(common.reference(pack_us, PACK_DM), np.float32).copy()
    out = H.copy()
    dm_plates(out, it)
    # ---- 1. the four badges "n° GIOCATORE"
    b = DM_BADGE
    cap = cap_height(HELV)
    for k, btxt in enumerate(BADGE_TXT):
        y0 = b['pitch'] * k
        sub = H[y0:y0 + b['h'], b['x0']:b['x1']].copy()
        clean = badge_clean(sub)
        zone = np.zeros(sub.shape[:2], bool)
        zone[4:48, BADGE_X0:BADGE_X1] = True
        shape = (b['h'], b['x1'] - b['x0'])
        cov = put_line(HELV, btxt, shape, b['size'], b['base'], x_left=b['left'], sx=b['sx'], space=b['space'])
        cov = np.clip(0.5 - (sdf(cov) / SS - b['bold']) * SS, 0, 1)
        txt = render(cov, b['grad'], None, dict(col=(40, 0, 20), dx=2.5, dy=2.5, sg=1.2, op=0.7),
                     ytop=b['base'] - cap * b['size'], ybase=b['base'])
        txt[..., 3] *= zone
        lay = clean.copy()
        over(lay, txt, 0, 0)
        out[y0:y0 + b['h'], b['x0']:b['x1']] = lay
    # ---- 2. the eight icon + digit tabs
    icon = draw_icon()                                                          # 32 x 24 HD
    t = DM_TABTEXT
    for k, (cx, ty) in enumerate(DM_TABS):
        # old text group "nP" spans cx +- 24 (+ glow), rows ty..ty+24: erase it with the row medians of the plain tab body
        cols = np.r_[int(cx) - 43:int(cx) - 35, int(cx) + 35:int(cx) + 43]
        erase_text(out, int(cx) - 32, int(cx) + 32, ty - 5, ty + 29, cols)
        digit = str(k % 4 + 1)
        wd = ink_width(ARIAL_BLACK, digit, t['size'])[0]
        gap = 12.0
        x_icon = cx - (24 + gap + wd) / 2.0                     # icon + digit centred on the tab text
        x_dig = x_icon + 24 + gap
        body = np.median(out[ty + 8, cols], axis=0)
        sh = dict(col=tuple(np.clip(body[:3] * 0.45, 0, 255)), dx=2.0, dy=2.5, sg=1.0, op=0.6)
        cv = rounded(put_line(ARIAL_BLACK, digit, (96, 96), t['size'], 60.0, x_left=20.0), 0.5)
        over(out, render(cv, (255, 255, 255), None, sh), int(round(x_dig - 20.0)), ty + 24 - 60)
        over(out, icon, int(round(x_icon)), ty - 4)
    # ---- 3. the "GIOCATORE" tab: the pack's "PLAYER" tab, text erased and widened by dw columns (the body is uniform
    # along x, so one column is repeated inside the tab and the same number of columns is dropped from the plain frame
    # line to the right: everything right of the tab keeps its place)
    tx0, tx1, ty0, ty1, dw, pos, pos2 = 504, 656, 515, 549, TAB_DW, 580, 800      # text zone, rows, widening, cut columns
    cols = np.r_[501:507, 655:660]
    erase_text(out, tx0, tx1, ty0, ty1, cols)
    band = out[508:566].copy()
    if dw >= 0:
        new = np.concatenate([band[:, :pos], np.repeat(band[:, pos:pos + 1], dw, axis=1), band[:, pos:pos2],
                              band[:, pos2 + dw:]], axis=1)
    else:       # linguetta piu' stretta di quella inglese: si tolgono colonne dal corpo e si allunga il filetto a destra
        n = -dw
        new = np.concatenate([band[:, :pos], band[:, pos + n:pos2], np.repeat(band[:, pos2:pos2 + 1], n, axis=1), band[:, pos2:]], axis=1)
    out[508:566] = new
    size = 31.0                                                  # "GIOCATORE" is wider than "PLAYER": 201 px at 31 px/em
    if LANG != 'it':
        size = min(33.0, fit_size(ARIAL_BLACK, TAB_WORD, 0.86 * (660 + dw - 496), 1.0, 0.0))
    body = np.median(out[528, cols], axis=0)
    sh = dict(col=tuple(np.clip(body[:3] * 0.45, 0, 255)), dx=2.0, dy=2.5, sg=1.0, op=0.6)
    w = ink_width(ARIAL_BLACK, TAB_WORD, size)[0]
    cv = rounded(put_line(ARIAL_BLACK, TAB_WORD, (96, 320), size, 60.0, x_left=20.0), 0.5)
    over(out, render(cv, (255, 255, 255), None, sh), int(round(496 + (660 + dw - 496) / 2.0 - w / 2.0 - 20.0)), 544 - 60)
    return to_img(out, fix=False)


# ----------------------------------------------------------------------------------------------------- family
FILES = {   # id -> (ehp file, member)
    'start_all__jyanken20_i0005': ('duel/start/start_all.ehp', 'jyanken20_i0005.gim'),
    'start_all__jyanken20_i0007': ('duel/start/start_all.ehp', 'jyanken20_i0007.gim'),
    'start_all__vs_much1_i0001': ('duel/start/start_all.ehp', 'vs_much1_i0001.gim'),
    'start_all__vs_much2_i0001': ('duel/start/start_all.ehp', 'vs_much2_i0001.gim'),
    'start_all__vs_much3_i0001': ('duel/start/start_all.ehp', 'vs_much3_i0001.gim'),
    'start_e__vs_bg01_1_i0005': ('duel/start/start_e.ehp', 'vs_bg01_1_i0005.gim'),
    'start_e__vs_bg01_1_i0007': ('duel/start/start_e.ehp', 'vs_bg01_1_i0007.gim'),
    'start_e__vs_bg01_1_i0008': ('duel/start/start_e.ehp', 'vs_bg01_1_i0008.gim'),
    'start_e__vs_bg01_1_i0012': ('duel/start/start_e.ehp', 'vs_bg01_1_i0012.gim'),
    'start_e__vs_bg01_1_i0014': ('duel/start/start_e.ehp', 'vs_bg01_1_i0014.gim'),
    'start_e__vs_bg01_2_i0001': ('duel/start/start_e.ehp', 'vs_bg01_2_i0001.gim'),
    'start_e__vs_bg01_2_i0004': ('duel/start/start_e.ehp', 'vs_bg01_2_i0004.gim'),
    'start_e__d_menu01_i': ('duel/start/start_e.ehp', 'd_menu01_i.gim'),
    'start_i__jnk_card01': ('duel/start/start_i.ehp', 'jnk_card01.gim'),
}


_L = {'fr': 'f', 'es': 's', 'de': 'g'}.get(LANG, 'i')
FILES_FR = {k.replace('_i0', f'_{_L}0').replace('menu01_i', f'menu01_{_L}').replace('start_i__', f'start_{_L}__'): (f.replace('start_i.ehp', f'start_{_L}.ehp'),
            m.replace('_i0', f'_{_L}0').replace('menu01_i', f'menu01_{_L}')) for k, (f, m) in FILES.items()}
# parole e larghezze (HD px) misurate sulle texture originali della lingua
TXT_VS = {
    'fr': dict(banners=['DUEL', 'NORMAL', 'TAG'], giocare=[('DEUXIÈME À JOUER', (148.0, 876.0)), ('PREMIER À JOUER', (180.0, 848.0))],
               rounds=[('1er round', (66.0, 446.0)), ('2e round', (82.0, 430.0)), ('3e round', (90.0, 442.0))],
               modes=[('Mode Un Duel', 52.0, 32.0, 476.0), ('Mode Match', 52.0, 60.0, 452.0)]),
    'de': dict(banners=['DUELL', 'NORMALES', 'TAG-'], giocare=[('ZWEITER', (328.0, 700.0)), ('ERSTER', (364.0, 664.0))],
               rounds=[('1. Runde', (86.0, 426.0)), ('2. Runde', (82.0, 430.0)), ('3. Runde', (82.0, 430.0))],
               modes=[('Einzelmodus', 52.0, 58.0, 454.0), ('Matchmodus', 52.0, 50.0, 458.0)]),
    'es': dict(banners=['DUELO', 'NORMAL', 'TAG'], giocare=[('SEGUNDO EN SALIR', (152.0, 872.0)), ('PRIMERO EN SALIR', (172.0, 856.0))],
               rounds=[('1ra vuelta', (56.0, 456.0)), ('2da vuelta', (44.0, 468.0)), ('3ra vuelta', (52.0, 460.0))],
               modes=[('Modo Individual', 52.0, 20.0, 492.0), ('Modo Combate', 52.0, 12.0, 496.0)]),
}


def main_fr(argv):
    """francese: stessi stili dell'italiano, parole e larghezze (misurate sulle texture francesi) in tabella"""
    fam = common.Family('schermata_vs', argv)
    low, hsh = {}, {}
    for k, (f, m) in FILES_FR.items():
        low[k], hsh[k] = common.texture(fam.usrdir, f, m)
    out = {}
    T = TXT_VS[LANG]
    ids = lambda t: t.replace('_f0', f'_{_L}0')
    for tid, text in zip(['start_e__vs_bg01_1_f0007', 'start_e__vs_bg01_1_f0008', 'start_e__vs_bg01_1_f0014'], T['banners']):
        tid = ids(tid)
        out[tid] = to_img(banner_fit(text, low[tid]))
    for tid in ('start_e__vs_bg01_1_f0005', 'start_e__vs_bg01_1_f0012'):
        tid = ids(tid)
        out[tid] = to_img(glow_from_original(low[tid]))
    for tid, (text, lr) in zip(['start_all__jyanken20_f0005', 'start_all__jyanken20_f0007'], T['giocare']):
        tid = ids(tid); l = low[tid]
        out[tid] = to_img(giocare_text(text, (l.height * 4, l.width * 4), *lr))
    for tid, (text, lr) in zip(['start_all__vs_much1_f0001', 'start_all__vs_much2_f0001', 'start_all__vs_much3_f0001'], T['rounds']):
        tid = ids(tid); l = low[tid]
        out[tid] = to_img(round_text(text, (l.height * 4, l.width * 4), *lr))
    for tid, fill, (text, base, x0, x1) in zip(['start_e__vs_bg01_2_f0001', 'start_e__vs_bg01_2_f0004'], [FILL_SINGLE, FILL_MATCH], T['modes']):
        tid = ids(tid); l = low[tid]
        out[tid] = to_img(mode_word(text, (l.height * 4, l.width * 4), fill, base, x0, x1))
    out[f'start_{_L}__jnk_card01'] = jnk_sheet(fam.pack_us, low[f'start_{_L}__jnk_card01'])
    out[f'start_e__d_menu01_{_L}'] = dm_sheet(fam.pack_us, low[f'start_e__d_menu01_{_L}'])
    assert sorted(out) == sorted(FILES_FR), 'missing textures'
    for tid in FILES_FR:
        im = out[tid]
        assert im.size == (low[tid].width * 4, low[tid].height * 4), tid
        fam.save(tid, im, hsh[tid], low[tid])
    fam.finish()


def main_en(argv):
    """inglese europeo: solo le texture che il pack USA non copre (2nd/3rd round e il foglio dei distintivi 1st/2nd PLAYER)"""
    fam = common.Family('schermata_vs', argv)
    ROUND.update(sx=1.7, size=54.0)         # il testo inglese e' piu' largo e piu' compatto di quello delle altre lingue (cercato su vs_much2/3)
    for tid, (f, m), text, lr in [('start_e__vs_much2_e0001', ('duel/start/start_e.ehp', 'vs_much2_e0001.gim'), '2nd round', (40.0, 472.0)),
                                  ('start_e__vs_much3_e0001', ('duel/start/start_e.ehp', 'vs_much3_e0001.gim'), '3rd round', (48.0, 464.0))]:
        low, h = common.texture(fam.usrdir, f, m)
        fam.save(tid, to_img(round_text(text, (low.height * 4, low.width * 4), *lr)), h, low)
    low, h = common.texture(fam.usrdir, 'duel/start/start_e.ehp', 'd_menu01_e.gim')
    im = dm_sheet(fam.pack_us, low)
    assert im.size == (low.width * 4, low.height * 4)
    fam.save('start_e__d_menu01_e', im, h, low)
    fam.finish()


def main(argv):
    if LANG == 'en':
        return main_en(argv)
    if LANG != 'it':
        return main_fr(argv)
    fam = common.Family('schermata_vs', argv)
    low = {}
    hsh = {}
    for k, (f, m) in FILES.items():
        low[k], hsh[k] = common.texture(fam.usrdir, f, m)
    out = {}
    for tid, text in [('start_e__vs_bg01_1_i0007', 'DUELLO'), ('start_e__vs_bg01_1_i0008', 'NORMALE'),
                      ('start_e__vs_bg01_1_i0014', 'TAG')]:
        l = low[tid]
        out[tid] = to_img(banner_word(text, (l.height * 4, l.width * 4)))
    l = low['start_e__vs_bg01_1_i0005']
    out['start_e__vs_bg01_1_i0005'] = to_img(glow_word('DUELLO NORMALE', (l.height * 4, l.width * 4), 985))
    out['start_e__vs_bg01_1_i0012'] = to_img(glow_from_original(low['start_e__vs_bg01_1_i0012']))
    for tid, text, cx in [('start_all__jyanken20_i0005', '2', 510), ('start_all__jyanken20_i0007', '1', 516)]:
        l = low[tid]
        out[tid] = to_img(giocare_word(text, (l.height * 4, l.width * 4), cx))
    for tid, d in [('start_all__vs_much1_i0001', '1'), ('start_all__vs_much2_i0001', '2'), ('start_all__vs_much3_i0001', '3')]:
        l = low[tid]
        out[tid] = to_img(round_word(d, (l.height * 4, l.width * 4)))
    l = low['start_e__vs_bg01_2_i0001']
    out['start_e__vs_bg01_2_i0001'] = to_img(mode_word('Modalità Singolo', (l.height * 4, l.width * 4), FILL_SINGLE, 84.0, 20.0, 492.0))
    l = low['start_e__vs_bg01_2_i0004']
    out['start_e__vs_bg01_2_i0004'] = to_img(mode_word('Modalità Match', (l.height * 4, l.width * 4), FILL_MATCH, 52.0, 28.0, 484.0))
    out['start_i__jnk_card01'] = jnk_sheet(fam.pack_us, low['start_i__jnk_card01'])
    out['start_e__d_menu01_i'] = dm_sheet(fam.pack_us, low['start_e__d_menu01_i'])
    assert sorted(out) == sorted(FILES), 'missing textures'
    for tid in FILES:
        im = out[tid]
        assert im.size == (low[tid].width * 4, low[tid].height * 4), tid
        fam.save(tid, im, hsh[tid], low[tid])
    fam.finish()


if __name__ == '__main__':
    main(sys.argv)
