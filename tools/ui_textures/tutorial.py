"""tutorial: the six duel-tutorial illustrations of tutorial/tutorial_i.ehp (tuto_duelimg01..06, 256x256) in HD.

The English HD pack has no version of these images, so they are rebuilt from the HD pack's own pieces; whatever
cannot be reused is drawn again as clean shapes (no blur upscale anywhere):
  01  the duel Yes/No dialog.  Backdrop (the faded screenshot of the duel field around the box): the colours of the
      visible strips are grouped into 12 flat material classes, every class becomes a smooth mask (one-hot -> bicubic
      -> soft argmax) painted with its own gently varying colour; the fade-out of the alpha is analytic.  Box: drawn
      analytically (crisp rounded rectangle, olive -> gold -> cream border).  Text: Sansation Bold (picked by
      measurement among ~90 system faces on the original lettering), one size, one weight, one baseline pitch;
      SI/NO buttons = the pack's own oval sprites (ui/misc ...b03bdb88, scaled 0.795 as in the original), labels in the
      same font; NO (11 px wide in the original) is set 5% smaller, tracked -0.4 px and squeezed 8% as a whole word;
      small trap card (Rinforzi / Reinforcements) = the large-card layout of the pack scaled down.
  02-06  type disc (equip, continuous, counter, quick-play, field) = the pack's large icon enlarged 2.65x (Lanczos +
      overshoot-clamped sharpening + steeper edges, analytic disc edge); card = the large-card layout of the game rebuilt from the pack
      at native resolution and scaled down (cards/frame/spell|trap.png pieces, the 312x312 art of cards/large/<id>.png
      placed where the original draws it, attribute and type icons, [CARTA MAGIA]/[CARTA TRAPPOLA] label from the
      Italian HD atlas of label_it.py), the Italian name in the HD banner style (Charter small caps; long names are
      set one size smaller, condensed by at most 8%) and the Italian description from cardinfo_ita, set justified.
Pack pieces are recoloured (least-squares colour transform per region plus a smooth drift of the marbled frame) so
that the HD image, box-filtered back to 256x256, matches the original Italian texture.  The text inks are the pack's.
usage: tutorial.py USRDIR PACK_US OUT   (env TUTO_ONLY=2,3 builds only those images)"""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import alt_font  # noqa: nessun font Apple
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import common  # noqa: E402  (also puts TOOLS on sys.path)
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
_argv = sys.argv
if os.environ.get('TF1_LANG', 'it') in ('fr', 'es', 'de', 'en'):      # small_it / label_it derive terms and labels from the language's cardinfo
    os.environ.setdefault('TF1_EHP', os.path.join(_argv[1], 'duelsys', 'cardinfo_' + {'fr': 'fra', 'es': 'spa', 'de': 'ger', 'en': 'eng'}[os.environ['TF1_LANG']] + '.ehp'))
sys.argv = [_argv[0], TOOLS]          # small_it reads its tools dir from argv[1] at import
import small_it as SI  # noqa: E402
import banner as BN  # noqa: E402
from cardprops import load as load_cards  # noqa: E402
sys.argv = _argv

X4 = common.SCALE
LANG = os.environ.get('TF1_LANG', 'it')
LL = {'it': 'i', 'fr': 'f', 'es': 's', 'de': 'g', 'en': 'e'}[LANG]
FILE = f'tutorial/tutorial_{LL}.ehp'
FONTS = '/System/Library/Fonts/'
SUPP = FONTS + 'Supplemental/'
LIBF = '/Library/Fonts/'

# ----------------------------------------------------------------------------------------------- helpers

def f32(im):
    return np.asarray(im, np.float32)


def down(a, k=X4):
    """box filter: HD float array -> low-res (exactly what common.check does)."""
    h, w = a.shape[:2]
    return a.reshape(h // k, k, w // k, k, *a.shape[2:]).mean((1, 3))


def to_img(rgb, alpha):
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), np.clip(alpha, 0, 255)]).round().astype(np.uint8), 'RGBA')


def fit_affine(src, dst, ridge=200.0):
    """dst ~ src @ M + b (3x3 + offset), ridge towards the identity; src/dst: (N,3)."""
    X = np.hstack([src, np.ones((len(src), 1), np.float32)]).astype(np.float64)
    prior = np.vstack([np.eye(3), np.zeros((1, 3))])
    R = np.diag([ridge, ridge, ridge, 0.0])
    return np.linalg.solve(X.T @ X + R, X.T @ dst.astype(np.float64) + R @ prior)


def apply_affine(rgb, B):
    sh = rgb.shape
    flat = rgb.reshape(-1, 3).astype(np.float64)
    return np.clip(flat @ B[:3] + B[3], 0, 255).reshape(sh).astype(np.float32)


def recolour(hd_rgb, low_rgb, mask_low, mask_hd, ridge=200.0):
    """fit the colour transform on the low-res pixels of mask_low, apply it to hd pixels weighted by mask_hd."""
    B = fit_affine(down(hd_rgb)[mask_low], low_rgb[mask_low], ridge)
    out = apply_affine(hd_rgb, B)
    return hd_rgb + (out - hd_rgb) * mask_hd[..., None]


def solve_ink(cover_hd, base_hd, low_rgb, mask_low=None, amin=0.05):
    """ink colour c minimising |down((1-a)*base + a*c) - low| over the pixels covered by the text (a > amin)."""
    a = down(cover_hd)
    rest = low_rgb - down(base_hd * (1 - cover_hd[..., None]))
    m = a > amin
    if mask_low is not None:
        m &= mask_low
    c = (a[m][:, None] * rest[m]).sum(0) / max((a[m] ** 2).sum(), 1e-6)
    return np.clip(c, 0, 255)


def over(rgb, cover, colour):
    """composite a flat colour with coverage `cover` (0..1, may be soft) on rgb."""
    c = np.asarray(colour, np.float32)
    return rgb + cover[..., None] * (c - rgb)


def shift(a, dx, dy, shape):
    """place float array a with its top-left at the sub-pixel position (dx, dy) on a zero canvas of `shape`."""
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(a, M, (shape[1], shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def font(path, size, index=0):
    return ImageFont.truetype(path, max(1, int(round(size))), index=index)


def resize_f(a, w, h):
    return cv2.resize(a, (max(1, int(round(w))), max(1, int(round(h)))), interpolation=cv2.INTER_AREA)


def disc(cx, cy, r, shape, soft=0.7):
    """anti-aliased disc coverage (HD px)."""
    ys, xs = np.mgrid[0:shape[0], 0:shape[1]].astype(np.float32)
    d = np.sqrt((xs + 0.5 - cx) ** 2 + (ys + 0.5 - cy) ** 2)
    return np.clip((r - d) / soft + 0.5, 0, 1)


def rect_mask(r, shape, feather=0.0):
    m = np.zeros(shape, np.float32)
    x0, y0, x1, y1 = [int(round(v)) for v in r]
    m[max(0, y0):y1, max(0, x0):x1] = 1
    return cv2.GaussianBlur(m, (0, 0), feather) if feather > 0 else m


def inside_low(m_hd):
    """low-res pixels whose 4x4 HD block is entirely inside the HD mask."""
    return down((m_hd > 0.999).astype(np.float32)) > 0.999


def extend_rgb(rgb, alpha, it=12):
    """give fully transparent pixels the colour of the nearest visible ones (no dark fringes when filtered)."""
    w = (alpha > 0).astype(np.float32)
    acc = rgb * w[..., None]
    out = rgb.copy()
    known = w > 0
    for _ in range(it):
        acc = cv2.blur(acc, (5, 5)); w2 = cv2.blur(w, (5, 5))
        fill = (~known) & (w2 > 1e-4)
        out[fill] = acc[fill] / w2[fill][:, None]
        known = known | fill
        w = known.astype(np.float32); acc = out * w[..., None]
    return out


def lanczos_pre(img, w, h):
    """Lanczos resize of an RGBA PIL image with premultiplied alpha -> (rgb float, alpha 0..255 float)."""
    a = f32(img)
    al = a[..., 3:4] / 255
    pre = np.dstack([a[..., :3] * al, al[..., 0] * 255]).astype(np.float32)
    big = cv2.resize(pre, (int(round(w)), int(round(h))), interpolation=cv2.INTER_LANCZOS4 if w > a.shape[1] else cv2.INTER_AREA)
    A = np.clip(big[..., 3], 0, 255)
    rgb = big[..., :3] / np.maximum(A[..., None], 1) * 255
    return np.clip(rgb, 0, 255), A


def clamp_sharpen(rgb, amt, sigma, win):
    """unsharp mask limited to the local min/max (no halos, no ringing): crisp edges after an enlargement."""
    blur = cv2.GaussianBlur(rgb, (0, 0), sigma)
    k = np.ones((win, win), np.uint8)
    return np.clip(rgb + amt * (rgb - blur), cv2.erode(rgb, k), cv2.dilate(rgb, k))


def steepen_edges(rgb, k=2.0, r=2, lo=40.0, hi=80.0):
    """make the edges of an enlarged picture crisper without aliasing: where the local luminance range is large (strong
    edges only, soft gradients and texture are left alone) the value between the local min and max is passed through
    a steeper smooth S curve (continuous, so the anti-aliasing of the edge is kept, the transition is k times narrower)."""
    wgt = np.float32([.299, .587, .114])
    lum = rgb @ wgt
    kern = np.ones((2 * r + 1, 2 * r + 1), np.uint8)
    mn = np.minimum(cv2.GaussianBlur(cv2.erode(lum, kern), (0, 0), 1.0), lum)
    mx = np.maximum(cv2.GaussianBlur(cv2.dilate(lum, kern), (0, 0), 1.0), lum)
    con = mx - mn
    t = np.clip((lum - mn) / np.maximum(con, 1e-3), 0, 1)
    u = np.clip((t - 0.5) * k + 0.5, 0, 1)
    u = u * u * (3 - 2 * u)
    w = np.clip((con - lo) / (hi - lo), 0, 1)
    w = w * w * (3 - 2 * w)
    return np.clip(rgb + ((mn + con * u) - lum)[..., None] * w[..., None], 0, 255)


# ----------------------------------------------------------------------------------------------- text
def text_masks(runs, fspec, size, x, base, shape, bold=0.0):
    """anti-aliased coverage (HD px) of one line made of runs [(text, key)] set one after the other on one baseline:
    glyphs of `fspec` at `size` HD px, pen origin (x, base); bold: stroke widening (HD px). -> {key: coverage}."""
    S = 8
    f = font(fspec[0], size * S, fspec[1])
    pad = 8
    full = ''.join(t for t, _ in runs)
    w = int(f.getlength(full) / S) + 2 * pad + int(size)
    h = int(size * 2) + 2 * pad
    sw = int(round(bold * S / 2))
    out = {}
    pre = ''
    for t, k in runs:
        im = Image.new('L', (w * S, h * S), 0)
        d = ImageDraw.Draw(im)
        d.text((pad * S + f.getlength(pre), (pad + size * 1.3) * S), t, font=f, fill=255, anchor='ls', stroke_width=sw)
        m = cv2.resize(f32(im) / 255, (w, h), interpolation=cv2.INTER_AREA)
        m = shift(m, x - pad, base - pad - size * 1.3, shape)
        out[k] = np.maximum(out.get(k, 0), m)
        pre += t
    return out


def word_mask(text, fspec, size, cx, base, shape, bold=0.0, hs=1.0, track=0.0):
    """one short word on one baseline, centred on cx (HD px): every glyph at its natural advance + `track` (HD px, same
    for all letters), the whole word squeezed horizontally by hs (one factor for the word) and widened by `bold`."""
    S = 8
    f = font(fspec[0], size * S, fspec[1])
    sw = int(round(bold * S / 2))
    adv = [f.getlength(ch) / S for ch in text]
    total = sum(adv) + track * (len(text) - 1)
    pad = 8
    w = int(total + 2 * pad + size)
    h = int(size * 2) + 2 * pad
    im = Image.new('L', (w * S, h * S), 0)
    d = ImageDraw.Draw(im)
    pen = 0.0
    for ch, a in zip(text, adv):
        d.text(((pad + pen) * S, (pad + size * 1.3) * S), ch, font=f, fill=255, anchor='ls', stroke_width=sw)
        pen += a + track
    m = cv2.resize(f32(im) / 255, (w, h), interpolation=cv2.INTER_AREA)
    wh = max(1, int(round(w * hs)))
    m = cv2.resize(m, (wh, h), interpolation=cv2.INTER_AREA)
    return shift(m, cx - (pad + total / 2) * hs, base - pad - size * 1.3, shape)


# ----------------------------------------------------------------------------------------------- cards
# large-card layout of the game (HD 'L space', 432x616): frame pieces of cards/frame/<kind>.png, art 312x312 at (60,136)
LW, LH = 432, 616
ICON_BIG = dict(counter=0, field=67, equip=135, continuous=203, quickplay=271)    # x in icons_attribute_race.png, y 204
ICON_SMALL = dict(equip=(3, 4), field=(35, 4), continuous=(67, 4), quickplay=(3, 36), counter=(67, 36))  # label icons
ATTR = dict(spell=(409, 274), trap=(341, 342))   # 62x62 attribute icons (SPELL / TRAP) in icons_attribute_race.png
COPYRIGHT_L = (236, 585, 396, 601)               # '(c) 1996 KAZUKI TAKAHASHI' of the frame (absent from the originals)


def frame_L(pack, kind, keep_copyright=False):
    sp = Image.open(f'{pack}/cards/frame/{kind}.png').convert('RGBA')
    c = Image.new('RGBA', (LW, LH), (0, 0, 0, 0))
    c.paste(sp.crop((0, 0, 432, 136)), (0, 0))
    for (y0, x) in ((136, 0), (196, 372)):       # side bars of the art window are stored as horizontal strips
        strip = np.asarray(sp.crop((0, y0, 312, y0 + 60))).transpose(1, 0, 2)
        c.paste(Image.fromarray(np.ascontiguousarray(strip)), (x, 136))
    c.paste(sp.crop((0, 256, 432, 424)), (0, 448))
    if not keep_copyright:
        # the originals have no copyright line: paint the strip with the clean frame texture beside it (feathered)
        x0, y0, x1, y1 = COPYRIGHT_L
        w = x1 - x0
        src = c.crop((x0 - w - 8, y0, x0 - 8, y1))
        m = np.zeros((y1 - y0, w), np.float32)
        m[2:-2, 2:-2] = 1
        m = cv2.GaussianBlur(m, (0, 0), 2.0)
        sa, ba = f32(src), f32(c.crop(COPYRIGHT_L))
        mix = ba * (1 - m[..., None]) + sa * m[..., None]
        c.paste(Image.fromarray(mix.round().astype(np.uint8), 'RGBA'), (x0, y0))
    return c


def art_large(pack, cid):
    """the card art at native resolution: the three pieces of the 512x256 large-card atlas."""
    lg = Image.open(f'{pack}/cards/large/{cid}.png').convert('RGBA')
    a = Image.new('RGBA', (312, 312))
    a.paste(lg.crop((0, 0, 312, 240)), (0, 0))
    a.paste(lg.crop((320, 0, 512, 72)), (0, 240))
    a.paste(lg.crop((320, 80, 440, 152)), (192, 240))
    return a


ART_QUAD = (55.7, 134.7, 371.6, 441.1)   # where the original game draws the art (L px), measured on the five cards


def art_window(pack, cid):
    """312x312 window (L px 60..372 x 136..448) of the pack frame filled with the art at native resolution, placed on
    the quad where the original draws it (x -4 px, 6 px shorter; the 4 px strip it does not reach is mirrored)."""
    art = f32(art_large(pack, cid).convert('RGB'))
    x0, y0, x1, y1 = ART_QUAD
    sx, sy = 312 / (x1 - x0), 312 / (y1 - y0)
    M = np.float32([[sx, 0, (60 - x0) * sx], [0, sy, (136 - y0) * sy]])
    w = cv2.warpAffine(art, M, (312, 312), flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT_101)
    return Image.fromarray(np.clip(w, 0, 255).round().astype(np.uint8), 'RGB').convert('RGBA')


def wrap_lines(text, f, width):
    """greedy wrap (in font units of f); returns list of (words, is_last_of_paragraph)."""
    out = []
    for para in SI.typo(text).replace('　', ' ').split('\n'):
        words = para.split()
        cur = []
        for w in words:
            if cur and f.getlength(' '.join(cur + [w])) > width:
                out.append((cur, False))
                cur = [w]
            else:
                cur.append(w)
        if cur:
            out.append((cur, True))
    return out


def desc_mask(text, fspec, size, pitch, x0, x1, base0, shape, justify=True):
    """justified paragraph text: HD coverage array. size = font size (HD px), lines start at baseline base0."""
    S = 8
    f = font(fspec[0], size * S, fspec[1])
    width = (x1 - x0) * S
    lines = wrap_lines(text, f, width)
    H = int((base0 + pitch * len(lines) + size) * S) + 8
    im = Image.new('L', (int(width) + 8 * S, H), 0)
    d = ImageDraw.Draw(im)
    sp = f.getlength(' ')
    for i, (words, last) in enumerate(lines):
        y = (base0 + i * pitch) * S
        nat = sum(f.getlength(w) for w in words)
        gap = sp
        if justify and not last and len(words) > 1:
            gap = (width - nat) / (len(words) - 1)
            if gap > 2.75 * sp:
                gap = sp
        xx = 0.0
        for w in words:
            d.text((xx, y), w, font=f, fill=255, anchor='ls')
            xx += f.getlength(w) + gap
    m = f32(im) / 255
    m = cv2.resize(m, (m.shape[1] // S, m.shape[0] // S), interpolation=cv2.INTER_AREA)
    return shift(m, x0, 0, shape), len(lines)


def name_mask(text, style, cap, x, base, shape, hs, track):
    """HD-pack card-name look (banner.STYLE: Charter small caps, gamma/contrast of the HD banners) at the font's
    natural proportions (the style's own 0.926 condensing is not applied); returns (coverage, width)."""
    m, asc = SI.smallcaps(text.replace("'", '’'), style['font'], cap, cap * style['sc'], track)
    a = f32(m) / 255
    cols = np.where(a.max(0) > 0)[0]
    a = a[:, cols.min():cols.max() + 1]
    w = max(1, int(round(a.shape[1] / SI.SS * hs)))
    a = cv2.resize(a, (w, max(1, int(round(a.shape[0] / SI.SS)))), interpolation=cv2.INTER_AREA)
    a = shift(a, x, base - asc / SI.SS, shape)
    a = np.power(np.clip(a, 0, 1), style.get('g', 1.0))
    return np.clip((a - 0.5) * style.get('k', 1.0) + 0.5, 0, 1) * (a > 0), w


# per-card layout in HD card space (256x368 = the 64x92 card of the tutorial x4); L -> HD scale
CW, CH = 256, 368
KX, KY = CW / LW, CH / LH
NAME_X, NAME_BASE, NAME_CAP = 24.5, 43.5, 16.0
NAME_MAXW = 176.0                      # room left of the attribute icon (HD card px)
NAME_HS_MIN = 0.92                     # never condense more than 8%; longer names are set one size smaller instead
NAME_TRACK = 0.06                      # letter-spacing of the names (fraction of the cap height): the original's are wide
DESC = dict(font=(SUPP + 'PTSerifCaption.ttc', 0), size=7.75, pitch=9.0, base=294.6,
            x0=40 * KX + 4.5, x1=390 * KX - 4.5)     # inside the rope border of the parchment (L x 40..390)
LABEL_DX, LABEL_Y = -79.0, 84.0      # atlas strip column c -> L x = c + LABEL_DX ; strip row 0 at L y = LABEL_Y
ATTR_L = (350.0, 37.0, 40.0)         # attribute icon (SPELL/TRAP) in the name box: L x, y, size
LICON_L = (346.0, 90.0, 28.0)        # spell/trap type icon inside the label gap: L x, y, size


def card_layers(pack, atlas, spec, W, H, texts=True):
    """HD pieces of one card drawn at W x H: base RGB (frame+art+icons), region masks, text coverages."""
    sx, sy = W / LW, H / LH
    kind = spec['kind']
    L = frame_L(pack, kind)
    L.alpha_composite(art_window(pack, spec['cid']), (60, 136))
    icons = Image.open(f'{pack}/cards/frame/icons_attribute_race.png').convert('RGBA')
    ax, ay = ATTR[kind]
    x, y, s = ATTR_L
    att = icons.crop((ax, ay, ax + 62, ay + 62)).resize((round(s), round(s)), Image.LANCZOS)
    L.alpha_composite(att, (round(x), round(y)))
    stl = Image.open(f'{pack}/cards/frame/icons_spell_trap.png').convert('RGBA')
    ix, iy = ICON_SMALL[spec['icon']]
    x2, y2, s2 = LICON_L
    lic = stl.crop((ix, iy, ix + 28, iy + 28)).resize((round(s2), round(s2)), Image.LANCZOS)
    L.alpha_composite(lic, (round(x2), round(y2)))
    base = lanczos_pre(L, W, H)[0]
    shape = (H, W)
    reg = {}
    reg['art'] = rect_mask((60 * sx, 136 * sy, 372 * sx, 448 * sy), shape, 0.6)
    reg['parch'] = rect_mask((40 * sx, 480 * sy, 391 * sx, 578 * sy), shape, 0.6)
    a = np.zeros((LH, LW), np.float32)
    a[round(y):round(y) + round(s), round(x):round(x) + round(s)] = f32(att)[..., 3] / 255
    reg['attr'] = resize_f(a, W, H)
    a = np.zeros((LH, LW), np.float32)
    a[round(y2):round(y2) + round(s2), round(x2):round(x2) + round(s2)] = f32(lic)[..., 3] / 255
    reg['licon'] = resize_f(a, W, H)
    # texts
    txt = {}
    if not texts:
        return base, reg, txt
    k = H / CH
    st = BN.STYLE
    cap = NAME_CAP * k
    nx, nb, room = NAME_X * W / CW, NAME_BASE * k, NAME_MAXW * W / CW
    nat = name_mask(spec['name'], st, cap, nx, nb, shape, 1.0, NAME_TRACK)[1]
    if nat <= room:
        txt['name'], _ = name_mask(spec['name'], st, cap, nx, nb, shape, 1.0, NAME_TRACK)
    else:   # too long for its slot: tight tracking, then the whole word one size smaller (<= 8% condensed)
        w0 = name_mask(spec['name'], st, cap, nx, nb, shape, 1.0, 0.0)[1]
        s_fit = min(1.0, room / (w0 * NAME_HS_MIN))
        txt['name'], _ = name_mask(spec['name'], st, cap * s_fit, nx, nb, shape, NAME_HS_MIN, 0.0)
    st_ = atlas.crop((0, 32 * spec['strip'], 512, 32 * spec['strip'] + 32))
    al = np.zeros((LH, LW), np.float32)
    sa = f32(st_)[..., 3] / 255
    x0 = int(LABEL_DX) + 100
    al[int(LABEL_Y):int(LABEL_Y) + 32, x0:x0 + 412] = sa[:, 100:512][:, :LW - x0]
    txt['label'] = np.clip(resize_f(al, W, H), 0, 1)
    d = DESC
    txt['desc'], _ = desc_mask(spec['desc'], d['font'], d['size'] * k, d['pitch'] * k, d['x0'] * W / CW, d['x1'] * W / CW,
                               d['base'] * k, shape)
    return base, reg, txt


SMOOTH_SIGMA, SMOOTH_MAX = 1.6, 40.0


def finish_card(base, reg, txt, low_rgb, inks=None, ridge=200.0, smooth=True):
    """recolour the pack pieces region by region to the original, then draw the texts with fitted inks."""
    shape = base.shape[:2]
    textany = np.zeros(shape, np.float32)
    for t in txt.values():
        textany = np.maximum(textany, t)
    notext = down(cv2.dilate(textany, np.ones((5, 5), np.uint8))) < 0.02
    rgb = base.copy()
    full = np.ones(shape, np.float32)
    special = np.maximum.reduce([reg[k] for k in ('art', 'parch', 'attr', 'licon')])
    order = [('frame', np.clip(full - special, 0, 1)), ('art', reg['art']), ('parch', reg['parch']),
             ('attr', reg['attr']), ('licon', reg['licon'])]
    for name, m in order:
        ml = inside_low(m if name != 'frame' else (m > 0.99).astype(np.float32)) & notext
        if name in ('attr', 'licon'):
            ml = down(m) > 0.9
        if ml.sum() < 6:
            continue
        rgb = recolour(rgb, low_rgb, ml, m, ridge=ridge if name not in ('attr', 'licon') else 2000.0)
    if smooth:     # gentle colour drift of the marbled frame/parchment towards the original (no new detail, no seams)
        for name, m in (('frame', np.clip(full - special, 0, 1)), ('parch', reg['parch'])):
            ml = inside_low((m > 0.99).astype(np.float32)) & notext
            if ml.sum() < 20:
                continue
            w = ml.astype(np.float32)
            r = (low_rgb - down(rgb)) * w[..., None]
            den = cv2.GaussianBlur(w, (0, 0), SMOOTH_SIGMA)
            f = cv2.GaussianBlur(r, (0, 0), SMOOTH_SIGMA) / np.maximum(den[..., None], 1e-3)
            f = np.where(den[..., None] > 0.05, f, 0)
            F = cv2.resize(np.clip(f, -SMOOTH_MAX, SMOOTH_MAX), (shape[1], shape[0]), interpolation=cv2.INTER_CUBIC)
            rgb = np.clip(rgb + F * m[..., None], 0, 255)
    for name in ('desc', 'label', 'name'):
        if name in txt:
            rgb = over(rgb, txt[name], inks[name])
    return rgb, inks


def big_icon(pack, kind, cx, cy, r, fit, shape):
    """the pack's large spell/trap type icon enlarged 2.65x to the original disc: Lanczos, then an overshoot-clamped
    sharpening (crisp edges without halos). The disc edge is an analytic circle (cx, cy, r, measured on the alpha of
    the original); the artwork inside is placed at the offset/scale `fit` measured on the original's silver parts."""
    icons = Image.open(f'{pack}/cards/frame/icons_attribute_race.png').convert('RGBA')
    x0 = ICON_BIG[kind]
    src = icons.crop((x0, 204, x0 + 66, 270))
    dx, dy, kk = fit
    k = r * kk / 32.6                     # visible radius of the pack icon: 32.6 px
    n = int(round(66 * k))
    rgb, A = lanczos_pre(src, n, n)
    rgb = steepen_edges(clamp_sharpen(extend_rgb(rgb, A), 1.6, 2.2, 5))
    out = np.dstack([shift(rgb[..., c].copy(), cx + dx - n / 2, cy + dy - n / 2, shape) for c in range(3)])
    return out, disc(cx, cy, r, shape, 1.2)


CARD_SPECS = {   # tutorial card (64x92 at x=119) + spell/trap type disc (cx, cy, r in HD px, fitted on the alpha)
    2: dict(cid=4317, kind='spell', strip=3, icon='equip', name='Pendente Nero', disc=(373.3, 90.55, 86.5), icon_fit=(-2.5, 1.5, 1.015)),
    3: dict(cid=5161, kind='spell', strip=3, icon='continuous', name='Scudo Giallo del Desiderio',
            disc=(373.45, 90.3, 86.5), icon_fit=(-1.5, 2.0, 1.005)),
    4: dict(cid=4863, kind='trap', strip=1, icon='counter', name='I Sette Attrezzi del Bandito', disc=(371.7, 91.75, 86.9),
            icon_fit=(1.0, 1.0, 1.03)),
    5: dict(cid=5355, kind='spell', strip=3, icon='quickplay', name='Crollo', disc=(374.8, 90.8, 86.25), icon_fit=(-1.5, 2.5, 1.03)),
    6: dict(cid=4340, kind='spell', strip=3, icon='field', name='Umi', disc=(377.35, 90.4, 86.25), icon_fit=(-2.0, 1.5, 1.015)),
}
CARD_AT = (119, 0)   # low-res position of the card


def card_inks(pack, spec):
    """text colours of the HD pack's cards: description and [label] black, names white (spells and traps alike)."""
    return dict(desc=(0, 0, 0), label=(0, 0, 0), name=(255, 255, 255))


def build_card_image(fam, i, atlas, cards):
    member = f'tuto_duelimg{i:02d}.gim'
    low, h = common.texture(fam.usrdir, FILE, member)
    lowf = f32(low)
    low_rgb, low_a = lowf[..., :3], lowf[..., 3]
    S = (low.height * X4, low.width * X4)
    spec = dict(CARD_SPECS[i], desc=cards[CARD_SPECS[i]['cid']]['desc'])
    if LANG != 'it':
        spec['name'] = cards[CARD_SPECS[i]['cid']]['name']
    rgb = np.zeros(S + (3,), np.float32)
    A = np.zeros(S, np.float32)
    # type icon
    cx, cy, r = spec['disc']
    irgb, ia = big_icon(fam.pack_us, spec['icon'], cx, cy, r, spec['icon_fit'], S)
    ml = (down(ia) > 0.999) & (low_a > 250)
    irgb = recolour(irgb, low_rgb, ml, np.full(S, 0.5, np.float32), ridge=2e5)   # half-way towards the original's tone: keeps the pack's warm brown
    rgb = rgb * (1 - ia[..., None]) + irgb * ia[..., None]
    A = np.maximum(A, ia * 255)
    # card
    base, reg, txt = card_layers(fam.pack_us, atlas, spec, CW, CH)
    X, Y = CARD_AT
    crgb, inks = finish_card(base, reg, txt, low_rgb[Y:Y + CH // X4, X:X + CW // X4], card_inks(fam.pack_us, spec))
    rgb[Y * X4:Y * X4 + CH, X * X4:X * X4 + CW] = crgb
    A[Y * X4:Y * X4 + CH, X * X4:X * X4 + CW] = 255
    rgb = extend_rgb(rgb, A)
    return to_img(rgb, A), h, low


def italian_label_atlas(usrdir, pack, tmp):
    """[CARTA MAGIA]/[CARTA TRAPPOLA] HD atlas exactly as the project builds it for the cards (label_it.py)."""
    eu, _ = common.texture(usrdir, 'database/cardalbum.ehp', f'spelltrap_{LL}.gim')
    src, out = os.path.join(tmp, 'eu.png'), os.path.join(tmp, 'atlas.png')
    eu.save(src)
    subprocess.run([sys.executable, os.path.join(TOOLS, 'label_it.py'), TOOLS,
                    os.path.join(pack, 'cards/frame/icons_spell_trap.png'), src, out], check=True, capture_output=True)
    return Image.open(out).convert('RGBA')


# ----------------------------------------------------------------------------------------------- dialog (01)
FIELD_RECT = (25.0, 2.0, 230.0, 124.0)      # low-res px: the faded screenshot of the duel field behind the dialog
FIELD_R = 10.0                              # its rounded corner
FEATHER_D = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12.5, 400]               # distance inside the rect (low-res px)
FEATHER_A = [30, 50, 70, 95, 121, 148, 173, 194, 213, 228, 240, 249, 254, 255, 255]   # alpha (fitted on the original)
BOX = (33.0, 10.0, 222.0, 116.0)            # the dialog box, low-res px
BOX_R = 0.6
BOX_CREAM = (255, 247, 230)
# border of the box, from the outer edge inwards (HD px): olive outline -> gold -> pale gold -> cream
BOX_EDGE_D = [0, 3, 5, 8, 11, 14, 16]
BOX_EDGE_RGB = [(166, 145, 92), (178, 156, 99), (206, 176, 107), (228, 200, 130), (243, 230, 190), (255, 252, 238), (255, 247, 230)]
TEXT_FONT = (LIBF + 'Sansation_Bold.ttf', 0)
TEXT_SIZE = 10.4 if LANG == 'de' else 11.0                            # low-res px (fitted on the original lettering, all three lines)
TEXT_X = 36.6 if LANG == 'en' else 37.6 if LANG in ('es', 'de') else 43.6      # es: the box is wider
TEXT_BASE = (27.6, 36.85, 46.1) if LANG == 'it' else (27.0, 36.6, 46.1)
TEXT_BOLD = 0.5                             # HD px of stroke widening: ink mass of the original
INK = (32, 30, 32)
PINK = (189, 25, 107)
BTN_S = 0.795                               # scale of the pack's oval sprites (fitted on both buttons)
BTN_BLUE_AT = (72.75, 57.875)               # low-res position of the blue oval sprite (+ yellow outline at -1,-1)
BTN_CREAM_AT = (137.0, 58.125)
BTN_LABEL = dict(size=9.3, base=69.7, bold=0.9, cx=(22.9, 22.3))   # label size (low-res px), baseline, stroke widening, centre x relative to the sprite origin (SI, NO)
BTN_NO = dict(size=8.8, hs=0.92, track=-0.4)    # NO: the original is 11 px wide, one size smaller + 8% squeeze + tight tracking (letter shapes stay natural)
MINI_AT = (120.0, 85.0, 16.0, 24.0)         # the small trap card (Reinforcements): x, y, w, h low-res px
MINI_CARD = dict(cid=4849, kind='trap', icon='counter', name='', desc='', strip=1)


if LANG in ('fr', 'es', 'de', 'en'):     # French/Spanish/German dialogue: 2 lines instead of 3, the box is lower (measured on the original)
    BOX = {'fr': (37.0, 10.0, 219.0, 107.0), 'en': (30.0, 10.0, 226.0, 107.0)}.get(LANG, (27.0, 10.0, 233.0, 107.0))      # de as es (to measure); en: measured on the cream box (34..221, 13..102)
    FIELD_RECT = {'fr': (29.0, 2.0, 227.0, 114.0), 'en': (23.0, 2.0, 233.0, 113.0)}.get(LANG, (19.0, 2.0, 241.0, 114.0))
    BTN_BLUE_AT, BTN_CREAM_AT = (72.75, 48.875), (137.0, 49.125)
    BTN_LABEL = dict(BTN_LABEL, base=60.7)
    MINI_AT = (120.0, 75.0, 16.0, 24.0)


def rrect_sdf(shape, x0, y0, x1, y1, r):
    """signed distance (px, negative inside) to the rounded rectangle (x0, y0, x1, y1), radius r; all in HD px."""
    ys, xs = np.mgrid[0:shape[0], 0:shape[1]].astype(np.float32)
    qx = np.abs(xs + 0.5 - (x0 + x1) / 2) - ((x1 - x0) / 2 - r)
    qy = np.abs(ys + 0.5 - (y0 + y1) / 2) - ((y1 - y0) / 2 - r)
    return np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2) + np.minimum(np.maximum(qx, qy), 0) - r


def feather_alpha(shape):
    """alpha of the whole picture: the field screenshot fades out over 12 low-res px at its border (analytic)."""
    sd = rrect_sdf(shape, *[v * X4 for v in FIELD_RECT], FIELD_R * X4)
    d = -sd / X4
    a = np.interp(d, FEATHER_D, FEATHER_A) * np.clip(d * X4 + 0.5, 0, 1)
    return cv2.GaussianBlur(a.astype(np.float32), (0, 0), 1.2)


def field_rgb(lr_rgb, valid, K=12):
    """clean rebuild of the field screenshot around the dialog: the colours of the visible strips are grouped into K
    flat material classes (k-means, fixed seed), every class becomes a smooth mask (one-hot -> bicubic -> soft argmax)
    painted with the gently varying class colour -> crisp shapes, no blur upscale. Hidden pixels take the nearest class."""
    H, W = lr_rgb.shape[:2]
    cv2.setRNGSeed(1)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.05)
    _, lab, cen = cv2.kmeans(lr_rgb[valid].astype(np.float32), K, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    L = np.full((H, W), -1, np.int32)
    L[valid] = lab[:, 0]
    _, near = cv2.distanceTransformWithLabels((~valid).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    Lf = np.concatenate([[0], L[valid]])[near]
    one = np.stack([cv2.GaussianBlur((Lf == c).astype(np.float32), (0, 0), 0.6) for c in range(K)], -1)
    big = np.stack([cv2.resize(one[..., c], None, fx=X4, fy=X4, interpolation=cv2.INTER_CUBIC) for c in range(K)], -1)
    e = np.exp(12 * (big - big.max(-1, keepdims=True)))
    p = e / e.sum(-1, keepdims=True)
    out = 0
    for c in range(K):
        w = ((Lf == c) & valid).astype(np.float32)
        den = cv2.GaussianBlur(w, (0, 0), 1.5)
        cf = np.where(den[..., None] > 1e-3, cv2.GaussianBlur(lr_rgb * w[..., None], (0, 0), 1.5) / np.maximum(den[..., None], 1e-3), cen[c])
        out = out + p[..., c:c + 1] * cv2.resize(cf, None, fx=X4, fy=X4, interpolation=cv2.INTER_CUBIC)
    return np.clip(out, 0, 255)


def box_layer(shape):
    """the dialog box drawn analytically: crisp rounded outline, olive -> gold -> cream border, flat cream."""
    sd = rrect_sdf(shape, *[v * X4 for v in BOX], BOX_R * X4)
    cov = np.clip(0.5 - sd, 0, 1)
    din = np.clip(-sd, 0, None)
    rgb = np.dstack([np.interp(din, BOX_EDGE_D, [c[k] for c in BOX_EDGE_RGB]) for k in range(3)]).astype(np.float32)
    return rgb, cov


def sprite_hd(img, s, x, y, shape):
    """RGBA float sprite (premultiplied resize by s, whole-pixel placement at HD (x, y)) -> (rgb, alpha 0..1) on `shape`."""
    a = f32(img)
    al = a[..., 3:4] / 255
    pre = np.dstack([a[..., :3] * al, al[..., 0] * 255]).astype(np.float32)
    nw, nh = int(round(a.shape[1] * s)), int(round(a.shape[0] * s))
    big = cv2.resize(pre, (nw, nh), interpolation=cv2.INTER_AREA)
    canvas = np.zeros(shape + (4,), np.float32)
    x, y = int(round(x)), int(round(y))
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(shape[1], x + nw), min(shape[0], y + nh)
    canvas[y0:y1, x0:x1] = big[y0 - y:y1 - y, x0 - x:x1 - x]
    A = np.clip(canvas[..., 3] / 255, 0, 1)
    return canvas[..., :3] / np.maximum(A[..., None], 1e-3), A


def build_dialog(fam, atlas, cards):
    member = 'tuto_duelimg01.gim'
    low, h = common.texture(fam.usrdir, FILE, member)
    lowf = f32(low)
    lr = lowf[..., :3]
    S = (low.height * X4, low.width * X4)
    # 1. backdrop: the duel field (visible only in a strip around the box)
    valid = np.zeros(lr.shape[:2], bool)
    fx0, fy0, fx1, fy1 = [int(v) for v in FIELD_RECT]
    valid[fy0:fy1, fx0:fx1] = True
    bx0, by0, bx1, by1 = [int(v) for v in BOX]
    valid[by0:by1, bx0:bx1] = False
    rgb = field_rgb(lr, valid)
    # 2. box
    brgb, bcov = box_layer(S)
    rgb = rgb * (1 - bcov[..., None]) + brgb * bcov[..., None]
    # 3. buttons (the pack's sprites)
    sheet = Image.open(os.path.join(fam.pack_us, 'ui/misc/00000000b03bdb881960a6b5.png')).convert('RGBA')
    blue, cream, outline = sheet.crop((246, 8, 482, 97)), sheet.crop((6, 8, 242, 97)), sheet.crop((0, 197, 238, 288))
    for img, (ox, oy), dxy in ((blue, BTN_BLUE_AT, (0, 0)), (outline, BTN_BLUE_AT, (-1, -1)), (cream, BTN_CREAM_AT, (0, 0))):
        srgb, sa = sprite_hd(img, BTN_S, ox * X4 + dxy[0] * BTN_S, oy * X4 + dxy[1] * BTN_S, S)
        rgb = rgb * (1 - sa[..., None]) + srgb * sa[..., None]
    # 4. the small card
    mx, my, mw, mh = MINI_AT
    mini, mreg, _ = card_layers(fam.pack_us, atlas, MINI_CARD, int(mw * X4), int(mh * X4), texts=False)
    mini, _ = finish_card(mini, mreg, {}, lr[int(my):int(my) + int(mh), int(mx):int(mx) + int(mw)])
    x0, y0 = int(round(mx * X4)), int(round(my * X4))
    ml = np.zeros(S, np.float32)
    ml[y0:y0 + mini.shape[0], x0:x0 + mini.shape[1]] = 1
    patch = np.zeros(S + (3,), np.float32)
    patch[y0:y0 + mini.shape[0], x0:x0 + mini.shape[1]] = mini
    rgb = rgb * (1 - ml[..., None]) + patch * ml[..., None]
    # 5. text
    sz = TEXT_SIZE * X4
    lines = [[("Il tuo avversario ha dichiarato", 'ink')],
             [("battaglia", 'pink'), (".", 'ink')],
             [("Vuoi ", 'ink'), ("attivare", 'pink'), (" l'effetto della Carta?", 'ink')]]
    if LANG == 'es':
        lines = [[("Tu oponente ha declarado la ", 'ink'), ("batalla", 'pink'), (".", 'ink')],
                 [("¿", 'ink'), ("activar", 'pink'), (" el efecto de la carta?", 'ink')]]
    if LANG == 'de':
        lines = [[("Dein Gegner hat den ", 'ink'), ("Kampf", 'pink'), (" eröffnet.", 'ink')],
                 [("Effekt der Karte ", 'ink'), ("aktivieren", 'pink'), ("?", 'ink')]]
    if LANG == 'en':
        lines = [[("Your opponent has declared ", 'ink'), ("battle", 'pink'), (".", 'ink')],
                 [("Activate", 'pink'), (" the effect of a card?", 'ink')]]
    if LANG == 'fr':
        lines = [[("Ton adversaire a déclaré le ", 'ink'), ("duel", 'pink'), (".", 'ink')],
                 [("Activer", 'pink'), (" l'effet de la carte" + chr(0xa0) + "?", 'ink')]]
    masks = {'ink': np.zeros(S, np.float32), 'pink': np.zeros(S, np.float32)}
    for runs, base in zip(lines, TEXT_BASE):
        for k, m in text_masks(runs, TEXT_FONT, sz, TEXT_X * X4, base * X4, S, bold=TEXT_BOLD).items():
            masks[k] = np.maximum(masks[k], m)
    rgb = over(rgb, masks['ink'], INK)
    rgb = over(rgb, masks['pink'], PINK)
    # button labels
    lab = BTN_LABEL
    for (ox, oy), text, cx in ((BTN_BLUE_AT, {'it': 'SÌ', 'es': 'SÍ', 'de': 'JA', 'en': 'YES'}.get(LANG, 'OUI'), lab['cx'][0]),(BTN_CREAM_AT, {'fr': 'NON', 'de': 'NEIN'}.get(LANG, 'NO'), lab['cx'][1])):
        if text in ('NO', 'NON', 'NEIN'):
            n = BTN_NO
            m = word_mask(text, TEXT_FONT, n['size'] * X4, (ox + cx) * X4, lab['base'] * X4, S, bold=lab['bold'],
                          hs=n['hs'], track=n['track'] * X4)
            c = solve_ink(m, rgb, lr, amin=0.6)     # ink from the fully covered pixels (the original's is near black)
        else:
            f = font(TEXT_FONT[0], lab['size'] * X4 * 8)
            wd = f.getlength(text) / 8 / X4
            m = text_masks([(text, 'l')], TEXT_FONT, lab['size'] * X4, (ox + cx - wd / 2) * X4, lab['base'] * X4, S, bold=lab['bold'])['l']
            c = solve_ink(m, rgb, lr)
        rgb = over(rgb, m, c)
    A = feather_alpha(S)
    rgb = extend_rgb(rgb, A)
    return to_img(rgb, A), h, low


def main():
    fam = common.Family('tutorial', sys.argv)
    cards = load_cards(os.path.join(fam.usrdir, 'duelsys/cardinfo_' + {'it': 'ita', 'fr': 'fra', 'es': 'spa', 'de': 'ger', 'en': 'eng'}[LANG] + '.ehp'))
    with tempfile.TemporaryDirectory() as tmp:
        atlas = italian_label_atlas(fam.usrdir, fam.pack_us, tmp)
    only = [int(v) for v in os.environ.get('TUTO_ONLY', '').split(',') if v]
    for i in range(1, 7):
        if only and i not in only:
            continue
        if i == 1:
            hd, h, low = build_dialog(fam, atlas, cards)
        else:
            hd, h, low = build_card_image(fam, i, atlas, cards)
        fam.save(f'tutorial_{LL}__tuto_duelimg{i:02d}', hd, h, low)
    fam.finish()


if __name__ == '__main__':
    main()
