"""Lettering of the HD "tab words" (Cassa, Fusion, Side, Deck, Affitto, ...): one font, one style, regular letters.

The mod's tab words (ui/deckedit: Trunk, Fusion, Side, Deck) are a heavy rounded sans with tight spacing and a hard offset shadow,
but the mod's own HD pixels are an AI upscale (wobbly letters), so they are only a MEASUREMENT target, never copied:
  font    SF Pro Rounded (SFNSRounded.ttf), weight 900: best overlap with the mod's real letter cores of all system fonts
          (mean IoU 0.557, the next ones <= 0.51; tools/calibration/fit_tabfont*.py)
  size    50 px: capitals ~35, x-height ~28 HD px (the mod's words: 37 / 26), tracking -3.8 px, white fill with a faint gradient
  shadow  the glyph grown by 1.2 px, offset (3, 3), in a dark shade of the tab colour; nothing around the letters on the lit side
Words longer than their slot are fitted with the least invasive step of LADDER (tracking, size, squeeze of at most 10 %):
no condensed letterforms, no touching letters.

    layer, info = render_word('Fusione', fill_rgb, (H, W), x0, x1, baseline)
returns a float RGBA HxWx4 layer (0..1, straight alpha), supersampled for clean edges; info has size, track, squeeze, ink, overflow."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import alt_font  # noqa: nessun font Apple
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = '/System/Library/Fonts/SFNSRounded.ttf'
WEIGHT = 900
SIZE = 50.0          # px: cap height ~35, x-height ~28 HD px (the mod's words: 37 / 26; SF Rounded has shorter capitals)
SPACE_EXTRA = 5.0    # px added to the word space (the tight tracking would otherwise make two-word titles run together)
TRACK = -3.8         # px between letters: tight like the mod's words but the outlines of neighbours only touch
SHADOW = (3.0, 3.0)  # offset of the hard shadow (HD px)
OUTLINE = 1.2        # the shadow shape is the glyph grown by this much; no outline on the lit side (like the mod's words)
SS = 4               # supersampling
MIN_SIZE = 0.78      # a long word may shrink to this fraction of SIZE
MAX_SQUEEZE = 0.10   # ... and then be squeezed horizontally by at most this much


def _font(size):
    f = ImageFont.truetype(FONT, max(8, int(round(size * SS))))
    axes = f.get_variation_axes()
    vals = [a['default'] for a in axes]
    for i, a in enumerate(axes):
        if a.get('name') in (b'Weight', 'Weight'):
            vals[i] = WEIGHT
    f.set_variation_by_axes(vals)
    return f


def shade(rgb, k):
    return tuple(int(round(c * k)) for c in rgb[:3])


def layout(word, size, track):
    """glyph pen positions (supersampled px, from 0) and total advance."""
    f = _font(size)
    xs, x = [], 0.0
    for i, ch in enumerate(word):
        xs.append(x)
        adv = f.getlength(word[:i + 1]) - f.getlength(word[:i]) if i else f.getlength(ch)
        x += adv + track * SS * size / SIZE + (SPACE_EXTRA * SS * size / SIZE if ch == ' ' else 0.0)
    return f, xs, x - track * SS * size / SIZE


def ink_extent(word, size, track=TRACK):
    """(left, right) ink extent in HD px relative to the pen origin, outline excluded."""
    f, xs, _ = layout(word, size, track)
    lo, hi = 1e9, -1e9
    for ch, x in zip(word, xs):
        if ch == ' ':
            continue
        x0, _, x1, _ = f.getbbox(ch, anchor='ls')
        lo, hi = min(lo, x + x0), max(hi, x + x1)
    return lo / SS, hi / SS


# ladder of fits, from the least to the most invasive: (tracking, minimum size factor, minimum squeeze)
LADDER = ((TRACK, 0.85, 0.97), (TRACK, 0.78, 0.93), (TRACK - 0.8, 0.78, 0.93), (TRACK - 0.8, 0.74, 0.90), (TRACK - 1.6, 0.72, 0.88))


def fit(word, slot, size=SIZE):
    """(size, tracking, squeeze, overflow) of the least invasive fit of `word` in `slot` HD px (ink width, shadow excluded)."""
    last = None
    for tr, fmin, qmin in LADDER:
        lo, hi = ink_extent(word, size, tr)
        r = slot / (hi - lo)                      # width scales linearly with the size (tracking scales too)
        if r >= 1:
            return size, tr, 1.0, 0.0
        f = min(1.0, max(fmin, r ** 0.5))
        qq = r / f
        if qq < qmin:
            f = max(fmin, r / qmin)
            qq = r / f
        last = (size * f, tr, min(1.0, max(qq, qmin)))
        if f * min(1.0, max(qq, qmin)) >= r - 1e-6 and qq >= qmin - 1e-6 and f >= fmin - 1e-6:
            return size * f, tr, min(1.0, qq), 0.0
    s_, tr, sq = last
    lo, hi = ink_extent(word, s_, tr * s_ / size)
    return s_, tr, sq, max(0.0, (hi - lo) * sq - slot)


def render_word(word, fill_rgb, shape, x0, x1, baseline, size=SIZE, track=None, fill_top=(255, 255, 255), fill_bottom=(238, 242, 250)):
    """lettering of `word` inside the HD slot [x0, x1) with the baseline at row `baseline` (HD px); the shadow stays inside the slot.
    returns (layer, info): layer = float HxWx4; info = dict(size, track, squeeze, ink=(left, right), overflow)."""
    H, W = shape
    slot = x1 - x0 - (SHADOW[0] + OUTLINE)
    if track is None:
        s, track_, sq, overflow = fit(word, slot, size)
        track = track_ * s / size                 # fit() returns the tracking at the reference size
        track_ref = track_
    else:
        s, sq, overflow, track_ref = size, 1.0, 0.0, track
        lo, hi = ink_extent(word, s, track)
        if hi - lo > slot:
            sq = max(1 - MAX_SQUEEZE, slot / (hi - lo)); overflow = max(0.0, (hi - lo) * sq - slot)
    lo, hi = ink_extent(word, s, track)
    tr = track
    f, xs, _ = layout(word, s, tr)
    lo, hi = ink_extent(word, s, tr)
    shapes = Image.new('L', (W * SS, H * SS), 0)
    # glyphs are drawn in one supersampled layer, then squeezed horizontally as a whole
    cw = int((hi - lo) * SS + 8 * SS)
    mask = Image.new('L', (cw + 8 * SS, H * SS), 0)
    d = ImageDraw.Draw(mask)
    pen = 4 * SS - lo * SS
    for ch, x in zip(word, xs):
        if ch != ' ':
            d.text((pen + x, baseline * SS), ch, font=f, fill=255, anchor='ls')
    if sq != 1.0:
        mask = mask.resize((max(1, int(round(mask.width * sq))), mask.height), Image.LANCZOS)
    ox = int(round((x0 - 4 + (0 if sq == 1.0 else 0)) * SS))
    canvas = Image.new('L', (W * SS, H * SS), 0)
    canvas.paste(mask, (ox, 0))
    ink_l = x0
    ink_r = x0 + (hi - lo) * sq
    # build the three layers from the one glyph mask: outline (dilated), shadow (offset outline), fill
    import cv2
    m = np.asarray(canvas, np.uint8)
    k = int(round(OUTLINE * SS))
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * k + 1, 2 * k + 1))
    outl = cv2.dilate(m, ker)
    dx, dy = int(round(SHADOW[0] * SS)), int(round(SHADOW[1] * SS))
    shad = np.zeros_like(outl)
    shad[dy:, dx:] = outl[:H * SS - dy, :W * SS - dx]

    def down(a):
        return np.asarray(Image.fromarray(a).resize((W, H), Image.LANCZOS), np.float32) / 255.0

    a_fill, a_out, a_sh = down(m), down(outl), down(shad)
    dark = np.asarray(shade(fill_rgb, 0.36), np.float32) / 255.0
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    rows = (baseline - 38 * s / SIZE, baseline + 2)      # gradient across the cap height
    t = np.clip((np.arange(H, dtype=np.float32) - rows[0]) / (rows[1] - rows[0]), 0, 1)[:, None, None]
    fill = (np.asarray(fill_top, np.float32) * (1 - t) + np.asarray(fill_bottom, np.float32) * t) / 255.0
    fill = np.broadcast_to(fill, (H, W, 3))
    out = np.zeros((H, W, 4), np.float32)

    def over(dst, rgb, a):
        a = a[..., None]
        oa = a + dst[..., 3:] * (1 - a)
        oc = np.where(oa > 1e-6, (np.broadcast_to(rgb, dst[..., :3].shape) * a + dst[..., :3] * dst[..., 3:] * (1 - a)) / np.maximum(oa, 1e-6), 0)
        return np.concatenate([oc, oa], -1)

    out = over(out, dark, a_sh)           # hard shadow: the grown glyph, offset down-right
    out = over(out, fill, a_fill)         # white fill, nothing around it on the lit side
    return out, dict(size=s, track=track_ref, squeeze=sq, ink=(ink_l, ink_r), overflow=overflow)


def render_tab_word(word, fill_rgb, shape, x0, x1, baseline=54, cap=SIZE, **kw):
    """render_word for a tab: the size never exceeds `cap` (one common size per group of sibling tabs, like the game's constant
    letter height), words that do not fit are fitted below it, smaller words stay centred in the band."""
    lay, info = render_word(word, fill_rgb, shape, x0, x1, baseline, size=SIZE, **kw)
    ref = SIZE
    if info['size'] > cap + 0.5:
        ref = cap
        lay, info = render_word(word, fill_rgb, shape, x0, x1, baseline, size=ref, **kw)
    if info['size'] < SIZE - 0.5:
        lay, info = render_word(word, fill_rgb, shape, x0, x1, baseline - 0.35 * (SIZE - info['size']), size=ref, **kw)
    return lay, info
