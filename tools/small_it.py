"""Italian text for the HD small cards (256x256): name, spell/trap label, Tipo line, description.
The English text areas are replaced by the exact text-free frame of the card type (smallclean.py),
then the Italian text from cardinfo_ita.ehp is drawn.
usage: small_it.py TOOLS PACK_DIR CARDINFO_ITA US_INI CLEAN_DIR [IDS...]   (writes PACK/cards/small_it)"""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__))))  # alt_font: percorso
import os, re, sys
from multiprocessing import Pool
sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from cardprops import load
from smallbg import frame_of
import languages
LANG = languages.current()   # it|fr|de|es|en (see languages.py)

FONTS = '/System/Library/Fonts/Supplemental/'
BOLD = (FONTS + 'Palatino.ttc', 2)   # large-card label atlas (label_it.py)
SS = 8  # supersampling

TYPE = {1: 'Drago', 2: 'Zombie', 3: 'Demone', 4: 'Pyro', 5: 'Serpente Marino', 6: 'Roccia', 7: 'Macchina',
        8: 'Pesce', 9: 'Dinosauro', 10: 'Insetto', 11: 'Bestia', 12: 'Guerriero-Bestia', 13: 'Pianta',
        14: 'Acqua', 15: 'Guerriero', 16: 'Bestia Alata', 17: 'Fata', 18: 'Incantatore', 19: 'Tuono',
        20: 'Rettile', 21: 'Divinità'}
# same convention as the English HD cards (and prints of that era): no '/Effect' after Toon/Spirit/Union
KIND = {0: '', 1: '/Effetto', 2: '/Fusione', 3: '/Fusione/Effetto', 4: '/Rituale', 5: '/Rituale/Effetto',
        6: '/Toon', 7: '/Spirito', 8: '/Unione', 9: '/Token'}
SPELL, TRAP = 13, 14
WORDS = ('Carta Magia', 'Carta Trappola')
if LANG != 'it':   # the other languages use the game's terms (DLG_Text of cardinfo_xxx.ehp); Italian stays the one chosen above
    _ehp = languages.current_ehp()
    if _ehp:
        TYPE, KIND, *WORDS = languages.terms(_ehp)

# layout of the 256x256 HD small card. Every value below was fitted on the ENGLISH text of the
# HD pack (fit_small.py, fit_desc*.py, fit_breaks.py) so the Italian text gets the same look.
IOWAN_BLACK = (FONTS + 'Iowan Old Style.ttc', 4)
CHARTER_BLACK = (FONTS + 'Charter.ttc', 5)
CHARTER_BOLD = (FONTS + 'Charter.ttc', 3)
TIMES_ITALIC = (FONTS + 'Times New Roman Italic.ttf', 0)
NAME_R = (18, 11, 211, 31)            # x0, y0, x1, y1 replaced by clean frame
# names/type line: physical fit (fit_metrics*.py): solid-ink cap height, small caps, width and ink density
NAME = dict(font=IOWAN_BLACK, cap=11.0, sc=0.8, track=0.0, emb=-3, hs=1.039, base=25.6, x=18.75, maxw=189,
            edge=dict(g=1.0, sx=0.7, sy=0.5, kx=1.2, hx=1.4, ky=0.2, hy=1.1))   # fit_edge.py + fit_subpix.py
LABEL_R = (100, 32, 233, 43)
LABEL = dict(font=IOWAN_BLACK, cap=6.8, sc=0.76, track=0.2, emb=5, hs=1.14, base=39.5, right=229.0, right_icon=210.0,
             bracket_emb=3, bracket_cap=5.6, bracket_dy=0.0, gap=0.0,   # letters on the original rows (34-40), short brackets
             # leftmost x of the label = Italian low-res card x4 + the shift the HD pack applied to the English labels
             starts={('Magia', True): 112, ('Magia', False): 125, ('Trappola', True): 91, ('Trappola', False): 100})
ICON_R = (212, 31, 229, 44)
TYPELINE = dict(font=CHARTER_BLACK, cap=4.8, sc=0.81, track=0.1, emb=3, hs=1.377, base=199.0, x=21.5, maxw=213,
                bracket_emb=3, gap=1.5, gap_r=0.0)   # brackets as heavy as the letters and tight to the words, like the HD cards (zoom check)
DESC_R_MON = (19, 192, 237, 231)      # parchment above the ATK/DEF rule
DESC_R_ST = (19, 192, 237, 240)       # parchment (border starts at x=237 / y=240)
# justified lines x 22..234; fixed first line and pitch; lines added downwards up to nmax (measured)
# ink: opacity factor so the ink per character matches the English cards (measured)
# fitted on the English HD cards (deschar.Bench + fit_descfont.py), fonts chosen by a visual judge panel
DESC = {'effect': dict(font=('/System/Library/Fonts/Supplemental/Iowan Old Style.ttc', 0), px=5.110, hs=1.430, emb=3, ink=1.00, dk=0.90, pitch=5.550, base=203.449, nmax=6,
                   edge={'g': 0.9, 'sx': 0.55, 'sy': 0.55, 'kx': 1.0, 'hx': 1.6, 'ky': 0.5, 'hy': 1.2}),
        'st': dict(font=('/System/Library/Fonts/Supplemental/PTSerifCaption.ttc', 0), px=4.340, hs=1.459, emb=3, ink=1.00, dk=0.85, pitch=5.438, base=197.494, nmax=8,
                   edge={'g': 1.053, 'sx': 0.45, 'sy': 0.45, 'kx': 0.332, 'hx': 0.752, 'ky': 0.233, 'hy': 1.108}),
        'normal': dict(font=('/System/Library/Fonts/Supplemental/Athelas.ttc', 1), px=5.250, hs=1.720, emb=3, ink=1.00, dk=0.95, pitch=5.390, base=203.250, nmax=6,
                   edge={'g': 1.0, 'sx': 0.55, 'sy': 0.45, 'kx': 1.5, 'hx': 1.0, 'ky': 0.3, 'hy': 0.6})}
DESC_X0, DESC_X1 = 22.0, 234.0
import alt_font   # the project does not use Apple fonts: styles measured for the free fonts (see alt_font.py)
alt_font.apply(sys.modules[__name__])

_CR = {}


def font(spec, px):
    return ImageFont.truetype(spec[0], max(1, int(round(px))), index=spec[1])


def cap_ratio(spec):
    if spec not in _CR:
        l, t, r, b = font(spec, 1000).getbbox('H', anchor='ls')
        _CR[spec] = -t / 1000
    return _CR[spec]


def ink_color(img, clean, box, default, thr=40, pct=75):
    """median color of the stroke pixels that differ most from the clean frame."""
    x0, y0, x1, y1 = box
    d = np.abs(img[y0:y1, x0:x1].astype(np.int32) - clean[y0:y1, x0:x1]).sum(-1)
    m = d > thr
    if m.sum() < 8:
        return default
    sel = m & (d >= np.percentile(d[m], pct))
    return tuple(int(v) for v in np.median(img[y0:y1, x0:x1][sel], 0))


def smallcaps(text, spec, cap, sc, track=0.0):
    """L image (SS scale) of synthetic small caps; returns (img, ascent_px_at_SS).
    track: extra space after each glyph, as a fraction of the cap height."""
    f_cap = font(spec, cap * SS / cap_ratio(spec))
    f_sc = font(spec, sc * SS / cap_ratio(spec))
    asc = int(cap * SS * 1.6)
    w = int(sum(max(f_cap.getlength(ch.upper()), f_sc.getlength(ch.upper())) + track * cap * SS for ch in text) + 8 * SS)
    im = Image.new('L', (w, asc + int(cap * SS)), 0)
    d = ImageDraw.Draw(im)
    x = 0.0
    for ch in text:
        big = (not ch.isalpha() or ch.isupper()) and ch != '#'
        f = f_cap if big else f_sc
        g = ch.upper() if ch.isalpha() else ch
        d.text((x, asc), g, font=f, fill=255, anchor='ls')
        x += f.getlength(g) + track * cap * SS
    return im, asc


def widen(m, r, cap, hs, c=0.25, stem=0.14):
    """very condensed names: the vertical stems get thinner in proportion to r (less black than in English);
    before shrinking, the mask is thickened horizontally to recover the 25% of the thickness lost."""
    if r >= 0.85:
        return m
    import cv2
    k = int(round(stem * cap * (1 - r) * c * SS / (hs * r)))   # stem: stem thickness / capital height (0.14 small cards, ~0.08 banner)
    return Image.fromarray(cv2.dilate(np.asarray(m), np.ones((1, k + 1), np.uint8))) if k >= 1 else m


def place(canvas, mask_ss, asc, x, base, color, maxw=None, align='left', vsquash=True, embolden=3, hs=1.0, edge=None):
    """downsample an SS mask and composite it with its baseline at `base` (x = left or right edge).
    hs: horizontal glyph scale (the card font is narrower/wider than Palatino)."""
    if embolden > 0:      # thicker strokes (at SS scale)
        mask_ss = mask_ss.filter(ImageFilter.MaxFilter(embolden))
    elif embolden < 0:    # thinner strokes
        mask_ss = mask_ss.filter(ImageFilter.MinFilter(-embolden))
    a = np.asarray(mask_ss)
    cols = np.where(a.max(0) > 0)[0]
    if not len(cols):
        return x
    m = Image.fromarray(a[:, cols.min():cols.max() + 1])
    w = m.width / SS * hs
    r = min(1.0, maxw / w) if maxw else 1.0
    # long names: as in the HD English cards (measured: top of the letters always on the same row) only condensed in
    # width; the height drops by 6% at most (before up to 38%, the name ended too low)
    v = max(0.94, min(1.0, r / 0.6)) if vsquash else 1.0
    m = widen(m, r, asc / SS, hs) if maxw else m
    W, H = max(1, round(w * r)), max(1, round(m.height / SS * v))
    m = m.resize((W, H), Image.LANCZOS)
    top = base - asc / SS * v
    left = x - W if align == 'right' else x
    if edge:   # HD-pack edge look (soft edge + opposite-polarity halo), signed weights
        from edge import edge_filter, composite
        pad = 6
        a = np.zeros((m.height + 2 * pad, m.width + 2 * pad), np.float32)
        a[pad:pad + m.height, pad:pad + m.width] = np.asarray(m, np.float32) / 255
        a = edge_filter(a, edge)
        X0, Y0 = round(left) - pad, round(top) - pad
        H, Wc = canvas.size[1], canvas.size[0]
        ya, yb, xa, xb = max(0, Y0), min(H, Y0 + a.shape[0]), max(0, X0), min(Wc, X0 + a.shape[1])
        arr = np.asarray(canvas).astype(np.float32)
        rgb = arr[ya:yb, xa:xb, :3]
        composite(rgb, a[ya - Y0:yb - Y0, xa - X0:xb - X0], color)
        arr[ya:yb, xa:xb, :3] = rgb
        canvas.paste(Image.fromarray(arr.round().astype(np.uint8), 'RGBA'))
        return left + W
    lay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    lay.paste(Image.new('RGBA', m.size, color + (255,)), (round(left), round(top)), m)
    canvas.alpha_composite(lay)
    return left + W


def text_width(t, sty):
    """ink width (final px) of a string drawn with style sty (same trimming as place)."""
    m, asc = smallcaps(t, sty['font'], sty['cap'], sty['cap'] * sty['sc'], sty['track'])
    e = sty['emb']
    if e > 0:
        m = m.filter(ImageFilter.MaxFilter(e))
    elif e < 0:
        m = m.filter(ImageFilter.MinFilter(-e))
    cols = np.where(np.asarray(m).max(0) > 0)[0]
    return (cols.max() - cols.min() + 1) / SS * sty['hs'] if len(cols) else 0.0


def put_text(out, t, sty, x, color, align='left', maxw=None, vsquash=False, base=None):
    m, asc = smallcaps(t, sty['font'], sty['cap'], sty['cap'] * sty['sc'], sty['track'])
    return place(out, m, asc, x, sty['base'] if base is None else base, color, maxw=maxw, align=align, vsquash=vsquash,
                 embolden=sty['emb'], hs=sty['hs'], edge=sty.get('edge'))


def draw_typeline(out, inner, ty, color):
    """[TIPO/GENERE]: thin brackets `gap` px from the words, condensed to fit maxw."""
    thin = dict(ty, emb=ty['bracket_emb'])
    gl, gr = ty.get('gap_l', ty['gap']), ty.get('gap_r', ty['gap'])
    x = put_text(out, '[', thin, ty['x'], color) + gl
    room = ty['maxw'] - (x - ty['x']) - gr - text_width(']', thin)
    x = put_text(out, inner, ty, x, color, maxw=room) + gr
    put_text(out, ']', thin, x, color)


def draw_label(out, word, has_icon, sty, color, icon=None):
    """[WORDS] / [WORDS (icon)] right-aligned, thin brackets `gap` px from the words (like the HD cards)."""
    thin = dict(sty, emb=sty.get('bracket_emb', sty['emb']), cap=sty.get('bracket_cap', sty['cap']))
    bbase = sty['base'] + sty.get('bracket_dy', 0.0)
    gap = sty.get('gap', 0.0)
    put_text(out, ']', thin, sty['right'], color, align='right', base=bbase)
    if has_icon:
        if icon is not None:
            out.paste(icon[0], ICON_R[:2], icon[1])
        wr = sty['right_icon']
    else:
        wr = sty['right'] - text_width(']', thin) - gap
    words = word.lstrip('[')
    wsty = sty
    target = sty.get('starts', {}).get((words.split()[-1], has_icon))
    if target is None and LANG != 'it':
        target = LABEL_R[0] + 4   # without the game's data: the label does not go out to the left of the cleaned area
    if target is not None:
        room = wr - gap - text_width('[', thin) - target
        nat = text_width(words, sty)
        if nat > room > 0:   # condense (never expand) to the original Italian layout
            wsty = dict(sty, hs=sty['hs'] * room / nat)
    put_text(out, words, wsty, wr, color, align='right')
    put_text(out, '[', thin, wr - text_width(words, wsty) - gap, color, align='right', base=bbase)


FALLBACK = ('/System/Library/Fonts/LucidaGrande.ttc', 0)   # glyphs missing in the text font
BULLET = '●'
BULLET_D, BULLET_GAP = 3.8, 1.0   # the HD cards draw '●' as a solid black disc ~4 px wide (measured), then ~1 px space
JUSTIFY_MAX = 2.75                # a justified gap may grow to this many normal spaces, beyond that the line stays ragged
SQUEEZE = 1.07                    # ...unless the next word fits by condensing that line by up to 7%


@__import__('functools').lru_cache(maxsize=None)
def has_glyph(spec, ch):
    f = font(spec, 40)
    a, b = np.asarray(f.getmask(ch)), np.asarray(f.getmask('\U0010FFFD'))
    return ch.isspace() or not (a.shape == b.shape and (a == b).all())


def typo(text):
    """typographic quotes/apostrophes like the HD cards; no space before punctuation (fr: non-breaking space before
    : ; ! ? and inside « », as on the French cards)."""
    if LANG == 'fr':
        text = re.sub(r'\s*([:;!?])', ' \\1', text)
    else:
        text = re.sub(r' +([,.;:!?])', r'\1', text)
    out = []
    for i, ch in enumerate(text):
        if ch == '"':
            prev = text[i - 1] if i else ' '
            opening = prev.isspace() or prev in '([●'
            if LANG == 'fr':
                ch = '« ' if opening else ' »'
            else:
                ch = '“' if opening else '”'
        elif ch == "'":
            ch = '’'
        out.append(ch)
    return ''.join(out)


def tokens(words):
    """words -> [token, space_before]; long compounds may also break after '-' or '/' (like the HD cards)."""
    out = []
    for w in words:
        parts = re.findall(r'.+?(?:(?<=[^\W\d_])-(?=[^\W\d_])|(?<=\w)/(?=\w))|.+$', w)
        for k, t in enumerate(parts):
            out.append([t, k == 0])
    return out


class Pen:
    """advances / drawing of tokens in font f (SS scale) with fallback glyphs and the bullet disc."""
    def __init__(self, f, spec, hs, scale=1.0):
        self.f, self.spec, self.hs = f, spec, hs
        self.fb = None
        self.space = f.getlength(' ')
        self.d, self.gap = BULLET_D * scale, BULLET_GAP * scale   # final px, shrinks with the text
        l, t, r, b = f.getbbox('x', anchor='ls')
        self.xh = -t / SS

    def runs(self, s):
        out = []
        for ch in s:
            kind = 'b' if ch == BULLET else ('f' if not has_glyph(self.spec, ch) else 't')
            if out and out[-1][1] == kind and kind != 'b':
                out[-1][0] += ch
            else:
                out.append([ch, kind])
        return out

    def font_of(self, kind):
        if kind == 'f':
            if self.fb is None:
                self.fb = ImageFont.truetype(FALLBACK[0], self.f.size, index=FALLBACK[1])
            return self.fb
        return self.f

    def length(self, s):
        n = 0.0
        for t, kind in self.runs(s):
            n += (self.d + self.gap) * SS / self.hs if kind == 'b' else self.font_of(kind).getlength(t)
        return n

    def line_length(self, toks):
        return sum(self.length(t) + (self.space if sp and i else 0) for i, (t, sp) in enumerate(toks))

    def draw(self, dr, bdr, x, y, s):
        for t, kind in self.runs(s):
            if kind == 'b':
                r = self.d * SS / 2
                cx, cy = x + r / self.hs, y - self.xh * SS / 2
                bdr.ellipse((cx - r / self.hs, cy - r, cx + r / self.hs, cy + r), fill=255)
                x += (self.d + self.gap) * SS / self.hs
            else:
                g = self.font_of(kind)
                dr.text((x, y), t, font=g, fill=255, anchor='ls')
                x += g.getlength(t)
        return x


def wrap(words, f, width, length=None):
    length = length or f.getlength
    lines, cur = [], ''
    for w in words:
        t = (cur + ' ' + w) if cur else w
        if length(t) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def loose(toks, pen, width):
    nsp = sum(1 for k, (t, sp) in enumerate(toks) if sp and k)
    return nsp == 0 or pen.space + (width - pen.line_length(toks)) / nsp > JUSTIFY_MAX * pen.space


def wrap_tokens(toks, pen, width):
    lines, cur = [], []
    for t in toks:
        if cur and pen.line_length(cur + [t]) > width:
            if pen.line_length(cur + [t]) <= width * SQUEEZE and loose(cur, pen, width):
                cur.append(t)                   # condensed a little instead of leaving holes
                continue
            lines.append(cur)
            cur = [[t[0], False]]
        else:
            cur.append(t if cur else [t[0], False])
    if cur:
        lines.append(cur)
    return lines


def layout_desc(text, st):
    """like the HD cards: fixed size and pitch, lines added downwards up to nmax; then condense horizontally; only
    then shrink the font a little at a time, the lines then filling the box down to the usual last line."""
    paras = [tokens(re.split(r'[^\S ]+', p.strip())) for p in re.split(r'\r?\n', typo(text).strip())]
    bottom = st['base'] + (st['nmax'] - 1) * st['pitch']      # lowest baseline
    for scale in np.arange(1.0, 0.44, -0.03):
        base0 = st['base'] - 0.7 * st['px'] * (1 - scale)      # the top of the text block stays put
        pitch = st['pitch'] * scale
        nmax = 1 + int((bottom - base0) / pitch + 1e-6)
        f = font(st['font'], st['px'] * scale * SS)
        for cond in (1.0, 0.95, 0.9, 0.85, 0.8):
            hs = st['hs'] * cond
            pen = Pen(f, st['font'], hs, scale)
            width = (DESC_X1 - DESC_X0) * SS / hs
            lines = [(l, i == len(ls) - 1) for p in paras for ls in [wrap_tokens(p, pen, width) or [[]]] for i, l in enumerate(ls)]
            if len(lines) <= nmax:
                if scale < 0.999 and len(lines) > 1:
                    pitch = min(st['pitch'], (bottom - base0) / (len(lines) - 1))
                return lines, pen, base0, pitch, scale
    return lines, pen, base0, pitch, scale


def draw_desc(canvas, text, st, color):
    """justified description drawn on ONE supersampled canvas (exact sub-pixel line positions), then the HD edge
    look (st['edge']: sharp strokes + light halo), ink opacity st['ink'] and darkness st['dk']."""
    lines, pen, base0, pitch, scale = layout_desc(text, st)
    f, hs = pen.f, pen.hs
    width = (DESC_X1 - DESC_X0) * SS / hs
    PAD, Y0, HB = 2, 184, 64                                     # final px: left margin for italic overhang, block top, height
    Wss = int((DESC_X1 - DESC_X0 + 2 * PAD + 4) * SS / hs)
    im = Image.new('L', (Wss, HB * SS), 0)
    bim = Image.new('L', (Wss, HB * SS), 0)
    dr, bdr = ImageDraw.Draw(im), ImageDraw.Draw(bim)
    x0 = PAD * SS / hs
    for i, (toks, last) in enumerate(lines):
        if not toks:
            continue
        nsp = sum(1 for k, (t, sp) in enumerate(toks) if sp and k)
        natural = pen.line_length(toks)
        squeeze = min(1.0, width / natural)                       # < 1 only for lines condensed by wrap_tokens
        extra = 0.0
        if not last and nsp and squeeze == 1.0:
            extra = max(0.0, (width - natural) / nsp)
            if pen.space + extra > JUSTIFY_MAX * pen.space:      # would leave holes: keep this line ragged
                extra = 0.0
        y = (base0 + i * pitch - Y0) * SS
        if squeeze < 1.0:                                        # draw at natural width, then condense into the line
            lim, lbim = Image.new('L', (int(natural + 2 * SS), HB * SS), 0), Image.new('L', (int(natural + 2 * SS), HB * SS), 0)
            ldr, lbdr = ImageDraw.Draw(lim), ImageDraw.Draw(lbim)
        else:
            ldr, lbdr = dr, bdr
        x = 0.0 if squeeze < 1.0 else x0
        for k, (t, sp) in enumerate(toks):
            if sp and k:
                x += pen.space + extra
            x = pen.draw(ldr, lbdr, x, y, t)
        if squeeze < 1.0:
            nw = max(1, round(lim.width * squeeze))
            for src, dst in ((lim, im), (lbim, bim)):
                dst.paste(src.resize((nw, src.height), Image.LANCZOS), (round(x0), 0), src.resize((nw, src.height), Image.LANCZOS))
    if st['emb'] > 0:
        im = im.filter(ImageFilter.MaxFilter(st['emb']))
    elif st['emb'] < 0:
        im = im.filter(ImageFilter.MinFilter(-st['emb']))
    size = (round(Wss / SS * hs), HB)
    al = np.asarray(im.resize(size, Image.LANCZOS), np.float32) / 255
    bl = np.asarray(bim.resize(size, Image.LANCZOS), np.float32) / 255
    if st.get('edge'):
        from edge import edge_filter
        al = np.minimum(edge_filter(al, st['edge']), 1.0)       # halo (<0) kept, strokes never darker than the ink
        bl = np.minimum(edge_filter(bl, st['edge']), 1.0)
    al *= st['ink']
    from edge import composite
    arr = np.asarray(canvas).astype(np.float32)
    left = round(DESC_X0) - PAD
    H, W = arr.shape[:2]
    xb = min(W, left + size[0])
    rgb = arr[Y0:Y0 + HB, left:xb, :3].copy()
    composite(rgb, al[:, :xb - left], tuple(v * st.get('dk', 1.0) for v in color))   # dk < 1: darker ink (HD cores)
    composite(rgb, bl[:, :xb - left], (0, 0, 0))                                     # bullets: solid black like the HD cards
    arr[Y0:Y0 + HB, left:xb, :3] = rgb
    canvas.paste(Image.fromarray(arr.round().astype(np.uint8), 'RGBA'))


def erase(img, clean, box, light_ref=False, thr=30, grow=2):
    """Replace only the English text of `box` (plus a small halo) with the clean frame, after
    matching the clean frame to this card's own tone; everything else keeps the card's pixels."""
    import cv2
    x0, y0, x1, y1 = box
    a = img[y0:y1, x0:x1].astype(np.float32)
    c = clean[y0:y1, x0:x1].astype(np.float32)
    diff = (a - c).reshape(-1, 3)
    if light_ref:   # dark text on parchment: the brightest pixels are surely background
        luma = a.reshape(-1, 3) @ np.array([0.3, 0.59, 0.11], np.float32)
        diff = diff[luma >= np.percentile(luma, 60)]
    c = np.clip(c + np.median(diff, 0), 0, 255)
    m = (np.abs(a - c).sum(-1) > thr).astype(np.uint8)
    m = cv2.dilate(m, np.ones((2 * grow + 1, 2 * grow + 1), np.uint8)).astype(np.float32)
    soft = cv2.GaussianBlur(m, (0, 0), 0.7)[..., None]
    img[y0:y1, x0:x1] = np.clip(a * (1 - soft) + c * soft, 0, 255).round().astype(np.uint8)


def localize(src, dst, card, en_name, clean):
    rgba = Image.open(src).convert('RGBA')
    img = np.asarray(rgba.convert('RGB')).copy()
    st = card['kind'] in (SPELL, TRAP)
    redo_name = card['name'].casefold() != (en_name or '').casefold()
    name_col = ink_color(img, clean, NAME_R, (0, 0, 0))
    desc_col = ink_color(img, clean, (19, 194, 237, 240) if st else (19, 201, 237, 231), (25, 20, 15), pct=80)  # description rows only
    type_col = ink_color(img, clean, (19, 192, 120, 200), desc_col, pct=95) if not st else desc_col
    icon = None
    if st:
        label_col = ink_color(img, clean, LABEL_R, (20, 20, 20))
        if card['icon']:
            x0, y0, x1, y1 = ICON_R
            patch = img[y0:y1, x0:x1].copy()
            d = np.abs(patch.astype(np.int32) - clean[y0:y1, x0:x1]).sum(-1)
            hsv = np.asarray(Image.fromarray(patch).convert('HSV'))
            m = (d > 30) & ((hsv[..., 1] > 40) | (hsv[..., 2] > 150))  # colored/bright icon, not black text
            m = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.5))
            icon = (Image.fromarray(patch), m)
    if redo_name:
        erase(img, clean, NAME_R)
    if st:
        erase(img, clean, LABEL_R)
    erase(img, clean, DESC_R_ST if st else DESC_R_MON, light_ref=True)
    out = Image.fromarray(img).convert('RGBA')
    def text(t, sty, x, base, color, align='left', maxw=None, vsquash=False):
        m, asc = smallcaps(t, sty['font'], sty['cap'], sty['cap'] * sty['sc'], sty['track'])
        return place(out, m, asc, x, base, color, maxw=maxw, align=align, vsquash=vsquash, embolden=sty['emb'], hs=sty['hs'],
                     edge=sty.get('edge'))

    if redo_name:
        text(card['name'].replace("'", '\u2019'), NAME, NAME['x'], NAME['base'], name_col, maxw=NAME['maxw'], vsquash=True)
    if st:
        word = '[' + (WORDS[0] if card['kind'] == SPELL else WORDS[1])
        draw_label(out, word, icon is not None, LABEL, label_col, icon)
        draw_desc(out, card['desc'], DESC['st'], desc_col)
    else:
        draw_typeline(out, TYPE.get(card['type'], '?') + KIND.get(card['kind'], ''), TYPELINE, type_col)
        draw_desc(out, card['desc'], DESC['normal' if card['kind'] == 0 else 'effect'], desc_col)
    out.putalpha(rgba.getchannel('A'))
    out.save(dst)
    return 'ok'


CLEAN = {}


def job(args):
    src, dst, card, en_name, clean_dir = args
    g = frame_of(card)
    if g not in CLEAN:
        CLEAN[g] = np.asarray(Image.open(os.path.join(clean_dir, f'clean_{g}.png')).convert('RGB')).astype(np.int32)
    try:
        return src, localize(src, dst, card, en_name, CLEAN[g])
    except Exception as e:  # keep going, report at the end
        return src, f'ERR {e!r}'


if __name__ == '__main__':
    pack, ehp, us_ini, clean_dir = sys.argv[2:6]
    only = {int(x) for x in sys.argv[6:]}
    cards = load(ehp)
    en = {int(a): b.strip() for a, b in re.findall(r'^#(\d{4}):\s*(.*)$', open(us_ini, encoding='utf-8').read(), re.M)}
    src_dir, dst_dir = os.path.join(pack, 'cards/small'), os.path.join(os.environ.get('TF1_OUT', pack), f'cards/small_{LANG}')
    os.makedirs(dst_dir, exist_ok=True)
    todo = []
    for f in sorted(os.listdir(src_dir)):
        m = re.match(r'(\d+)', f)
        if f.endswith('.png') and m and int(m.group(1)) in cards and (not only or int(m.group(1)) in only):
            cid = int(m.group(1))
            todo.append((os.path.join(src_dir, f), os.path.join(dst_dir, f), cards[cid], en.get(cid), clean_dir))
    with Pool() as p:
        res = p.map(job, todo, chunksize=8)
    bad = [r for r in res if r[1] != 'ok']
    print('done', len(res) - len(bad), 'errors', len(bad), bad[:5])
