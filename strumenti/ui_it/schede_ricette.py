"""schede_ricette: HD Italian recipe-view / limit-list / title-menu tabs, recipe panels and duel-record parts.

    python3 -I schede_ricette.py USRDIR PACK_US OUT

Every texture is rebuilt at 4x from the low-res Italian original (common.texture); the mod's HD pixels are only a style reference or,
where they are clean hand-drawn art (ui/limited.png: pouch, arrow, swirl, limit circles), resampled; the deck-editor tabs and the
ui/misc sheets are AI upscales and are not copied.  Look and feel = schede_deck.py:
  frames     crisp EPX upscale (schede_deck.upscale) of the Italian original with text, icon and white slot wiped; flat bands are
             wiped with the per-row colour of the tab's own clean band, panel headers with a clean column of the same texture.
             The white counter slot is a clean rounded box.  Lone corner pixels that EPX would turn into blips (t_window0008/0026
             at (1, 1); parts_i: bottom-right corner of the pink and red bevelled pieces) are replaced by their neighbour first;
             the square 'back to the deck' button of the recipe panel gets its four corner pixels back as plain blocks.
  words      ONE font and ONE style for every word: tabword.render_word (SF Pro Rounded Black, white fill, hard shadow in a dark
             shade of the tab colour), regular letters.  The six recipe tabs (recipe_view 008/015/027/029/031, recipe_sel00033) share
             ONE size (RECIPE_SIZE), the standard tracking and at most 7 % squeeze, and their white ink really ends at the declared
             right limit (render_exact), i.e. >= 2.5 px before the frame / the shadow clears it like in the original; the limit-list
             and title-menu tabs use tabword.render_tab_word with a common size cap per group.  Words start where the Italian ink
             starts; 'NUOVO' (dark on orange) and the 'R' of the duel-record badge use the same font without shadow.
  icons      document icons: the game's 9x13 cell icon at 4x nearest (the same look as the mod's own document icons) + hard
             shadow; the 'downloaded recipe' icon (green document with lightning bolt) is the original's 10x15 cells (page, bolt and
             pixel shadow) at 4x nearest too, so bolt and page share one pixel grid.  Deck-box pouch: the mod's clean HD pouch of
             ui/limited.png resampled to the original's 8x11 cells and recoloured to the original's steel blue; return arrow: the
             silhouette of the mod's arrow (big head, thick hook) redrawn as straight-edged vector shape in the original's flat
             yellow; side-deck card: vector card with four hard-edged golden corner triangles (rim 1 px) like the original's gold
             corner cells; fusion swirl and the limit circles (1, 2, forbidden): the mod's clean HD icons of ui/limited.png
             (resampled / edge-sharpened), registered on the original position; scroll arrows and arrow buttons: vector triangles.
  marble     recipe panel bars: the marble is an indexed image (one colour ramp: vein colour - flat base - light blotches); it is
             rebuilt as smooth blotch gradient (cubic, no sharpening) + flat base + veins redrawn as constant-width antialiased
             lines (vein probability -> smooth upscale -> hard smoothstep, diagonal steps bridged, specks dropped); frame bands
             crisp across and smooth along (the strongly mottled outer columns of the left band / end caps are calmed with a light
             vertical gaussian).  Digits of dmenu_recipe: 4x nearest of the original, pixel-identical to the first row of the
             mod's own digit sheet ui/duels/numbers.png (normalised correlation 1.000; NOT ui/text/numbers.png, a gold serif sheet).
  parts_i    EPX upscale of the sheet, with the R square, NUOVO, the arrows and the two arrow buttons redrawn.
Note: the title menu tabs say 'Tauschen' (German) in the original Italian game; on the user's request they are drawn as 'Scambio'."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import cv2
from PIL import Image
from collections import Counter
import common
import tabword
from schede_deck import upscale, over, paint, rrect, arr, img, premul, unpremul, clean_alpha

S = common.SCALE


def nearest(a, s=S):
    return np.repeat(np.repeat(a, s, 0), s, 1)


# ------------------------------------------------------------------------------------------------ vector icons
def shift_mask(m, dx, dy):
    out = np.zeros_like(m)
    h, w = m.shape
    out[max(dy, 0):h + min(dy, 0), max(dx, 0):w + min(dx, 0)] = m[max(-dy, 0):h - max(dy, 0), max(-dx, 0):w - max(dx, 0)]
    return out


def vgrad(h, w, y0, y1, c0, c1):
    """vertical colour ramp (float 0..1 RGB) between rows y0 and y1."""
    t = np.clip((np.arange(h, dtype=np.float32) - y0) / max(1e-6, y1 - y0), 0, 1)[:, None, None]
    ramp = np.asarray(c0, np.float32) / 255.0 * (1 - t) + np.asarray(c1, np.float32) / 255.0 * t
    return np.broadcast_to(ramp, (h, w, 3))


def blank(h, w):
    return np.zeros((h, w, 4), np.float32)


def fill(dst, cov, rgb):
    """composite an RGB image/colour (0..1 floats, HxWx3) with coverage cov over dst."""
    src = np.concatenate([np.broadcast_to(np.asarray(rgb, np.float32), dst.shape[:2] + (3,)), np.clip(cov, 0, 1)[..., None]], -1)
    return over(dst, src)


POUCH_MOD = (4, 348, 46, 400)       # the mod's deck-box pouch in ui/limited.png (x0, y0, x1, y1), without the neighbouring icons
ARROW_MOD = (432, 192, 470, 229)    # the return arrow of the mod's pouch + arrow icon (same sheet)
ICON2_ORIGIN = (420, 171)           # top-left of the outline of the pouch in that icon
# luminance -> colour ramp of the original game's steel-blue pouch (outline, body, flap, flap highlight) used to recolour the mod's pouch
POUCH_RAMP = ((0.00, (0, 0, 0)), (0.06, (0, 0, 0)), (0.232, (52, 87, 121)), (0.418, (78, 115, 150)), (0.50, (98, 136, 172)), (1.0, (150, 180, 208)))
ARROW_YELLOW = ((250, 226, 0), (236, 204, 0))      # top / bottom colour of the original's flat yellow arrow


def pouch_source():
    """the mod's pouch (RGBA floats, origin = top-left of its outline) and the factors that bring its body to the original's
    8 x 11 cells, as (image, fx, fy, body origin in sheet pixels)."""
    x0, y0, x1, y1 = POUCH_MOD
    im = arr(common.reference(PACK[0], LIMITED))[y0:y1, x0:x1].copy()
    im[399 - y0:, 42 - x0:] = 0                                  # top of the next icon of the sheet touches the shadow's corner
    ys, xs = np.nonzero(im[:y1 - y0 - 1, :40 - x0, 3] > 0.8)
    bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    return im[by0:, bx0:], 8 * S / (bx1 - bx0), 11 * S / (by1 - by0), (x0 + bx0, y0 + by0)


def pouch_sprite(shadow_a=0.4):
    """the deck-box icon: the mod's own clean HD pouch (ui/limited.png: black outline, shaded flap with highlight and curved lower edge,
    slit; hand-drawn, no noise), resampled to the 8 x 11 cells of the original (area resampling of the premultiplied pixels) and
    recoloured to the original game's steel blue (luminance ramp).  Origin (0, 0) = top-left of the outline; the soft shadow of the
    mod's art is kept (alpha scaled to shadow_a)."""
    crop, fx, fy, _ = pouch_source()
    p = cv2.resize(premul(crop), (int(round(crop.shape[1] * fx)), int(round(crop.shape[0] * fy))), interpolation=cv2.INTER_AREA)
    out = unpremul(p)
    lum = out[..., :3] @ np.array([0.299, 0.587, 0.114], np.float32)
    ramp_y = np.array([k for k, _ in POUCH_RAMP], np.float32)
    ramp_c = np.array([c for _, c in POUCH_RAMP], np.float32) / 255.0
    out[..., :3] = np.stack([np.interp(lum, ramp_y, ramp_c[:, c]) for c in range(3)], -1)
    yy, xx = np.mgrid[0:out.shape[0], 0:out.shape[1]]
    shadow = (xx >= 8 * S) | (yy >= 11 * S)
    out[..., 3] = np.where(shadow, out[..., 3] * shadow_a / 0.63, out[..., 3])
    return out


def vector_mask(cov, eps=1.0, SS=4):
    """re-draw a pixel-stepped coverage mask as a clean vector shape: contour of the (cubic-upsampled) mask, simplified to straight
    edges (Douglas-Peucker, eps in HD px) so diagonals are straight and tips stay sharp, filled antialiased."""
    h, w = cov.shape
    big = cv2.resize(cov, (w * SS, h * SS), interpolation=cv2.INTER_CUBIC)
    m = (big > 0.5).astype(np.uint8)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    can = np.zeros((h * SS, w * SS), np.uint8)
    for c in cs:
        if cv2.contourArea(c) > 4 * SS * SS:
            cv2.fillPoly(can, [cv2.approxPolyDP(c, eps * SS, True)], 255)
    return cv2.resize(can, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0


def arrow_sprite(shadow_a=0.4):
    """yellow return arrow of the 'back to the deck' icon: the silhouette of the mod's arrow (big head, thick hook; the warm pixels of
    its orange fill, without the dark outline of the mod's art), resampled like the pouch, in the flat yellow of the original with
    the original's soft grey shadow.  Returns (sprite, (dx, dy)): offset of the sprite from the pouch's top-left, in HD px."""
    _, fx, fy, _ = pouch_source()
    px, py = ICON2_ORIGIN
    x0, y0, x1, y1 = ARROW_MOD
    im = arr(common.reference(PACK[0], LIMITED))[y0:y1, x0:x1]
    cov = np.clip(((im[..., 0] - im[..., 2]) - 0.25) / 0.35, 0, 1) * im[..., 3]
    pad = 2 * S
    cov = cv2.resize(cov, (int(round(cov.shape[1] * fx)), int(round(cov.shape[0] * fy))), interpolation=cv2.INTER_AREA)
    cov = np.pad(cov, ((pad, pad), (pad, pad)))
    cov = vector_mask(cov)                                            # the sheet's pixel stairs become straight edges
    h, w = cov.shape
    spr = blank(h, w)
    spr = paint(spr, shift_mask(cov, S, S) * shadow_a, (0, 0, 0))
    t = np.clip((np.arange(h, dtype=np.float32) - pad) / max(1.0, h - 2 * pad), 0, 1)[:, None, None]
    col = np.asarray(ARROW_YELLOW[0], np.float32) / 255 * (1 - t) + np.asarray(ARROW_YELLOW[1], np.float32) / 255 * t
    spr = fill(spr, cov, np.broadcast_to(col, (h, w, 3)))
    return spr, (int(round((x0 - px) * fx)) - pad, int(round((y0 - py) * fy)) - pad)


def card_sprite(shadow_a=0.4):
    """the side-deck icon (dark brown card back with golden corners, black outline), 7 x 10 cells + shadow."""
    h, w = 11 * S, 8 * S
    spr = blank(h, w)
    outer = rrect(h, w, 0, 0, 7 * S, 10 * S, 3.6)
    spr = paint(spr, shift_mask(outer, S, S) * shadow_a, (0, 0, 0))
    spr = paint(spr, outer, (0, 0, 0))
    ring = rrect(h, w, S, S, 6 * S, 9 * S, 2.2)
    spr = paint(spr, ring, (91, 54, 23))
    spr = paint(spr, rrect(h, w, 2 * S, 2 * S, 5 * S, 8 * S, 1.4), (62, 43, 27))
    # the four golden corner pieces of the original (a gold cell with two darker-gold cells beside it): hard-edged triangles with a
    # 1 px darker rim along the hypotenuse, clipped by the card's own rounded ring
    L, rim = 2.5 * S, 1.2
    for (cx, cy), (sx, sy) in (((S, S), (1, 1)), ((6 * S, S), (-1, 1)), ((S, 9 * S), (1, -1)), ((6 * S, 9 * S), (-1, -1))):
        tri = lambda k: poly_cov(h, w, [(cx, cy), (cx + sx * k, cy), (cx, cy + sy * k)])
        spr = paint(spr, ring * tri(L), (113, 74, 14))
        spr = paint(spr, ring * tri(L - rim * 1.4142), (165, 122, 29))
    return spr


def swirl_sprite(pack, width):
    """the fusion swirl icon: the mod's HD swirl (clean hand-drawn art), resampled to `width` HD px and edge-sharpened."""
    im = arr(common.reference(pack, LIMITED))[349:400, 93:144]
    al = im[..., 3]
    ys, xs = np.nonzero(al[:, 2:46] > 0.5)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min() + 2, xs.max() + 3
    c = im[y0:y1, x0:x1]
    k = width / c.shape[1]
    p = premul(c)
    p = cv2.resize(p, (int(round(c.shape[1] * k)), int(round(c.shape[0] * k))), interpolation=cv2.INTER_AREA)
    out = unpremul(p)
    out[..., 3] = np.clip((out[..., 3] - 0.5) * 3.0 + 0.5, 0, 1)
    return out


# ------------------------------------------------------------------------------------------------ tabs
RV = 'deck/recipe_view_i.ehp'
LL = 'database/limitlist.ehp'
TM = 'title_menu/title_menu_i.ehp'

# id: file, member, word, (first, last) interior column of the coloured band (row 3), icon, text start (low px),
#     text right limit (low px), white slot columns [x0, x1) or None
TABS = {
    'recipe_view_i__recipe010008': dict(file=RV, member='recipe010008.gim', word='Personaggio', ix=(58, 124), icon=('doc', 59), doc='pink', tx=(70.5, 121.5), exact=True),
    'recipe_view_i__recipe010015': dict(file=RV, member='recipe010015.gim', word='Utente', ix=(3, 69), icon=('doc', 4), tx=(16, 66), exact=True),
    'recipe_view_i__recipe010027': dict(file=RV, member='recipe010027.gim', word='Ricette Scaricate', ix=(17, 124), icon=('bolt', 18), tx=(29.5, 120), exact=True),
    'recipe_view_i__recipe010029': dict(file=RV, member='recipe010029.gim', word='Ricette Personaggio', ix=(5, 112), icon=('doc', 6), doc='pink', tx=(18, 109.5), exact=True),
    'recipe_view_i__recipe010031': dict(file=RV, member='recipe010031.gim', word='Ricette Utente', ix=(3, 110), icon=('doc', 4), tx=(16, 107), exact=True),
    'title_menu_i__recipe_sel00033': dict(file=TM, member='recipe_sel00033.gim', word='Ricette Personaggio', ix=(3, 110), icon=('doc', 4), doc='pink', tx=(16, 107.5), exact=True),
    'limitlist__window_i0002': dict(file=LL, member='window_i0002.gim', word='Limitata', ix=(3, 106), icon=('lim_1', 3), tx=(15, 84.5), slot=(87, 106)),
    'limitlist__window_i0004': dict(file=LL, member='window_i0004.gim', word='Semi-Limitata', ix=(20, 124), icon=('lim_2', 20), tx=(32, 102.5), slot=(105, 124)),
    'limitlist__window_i0012': dict(file=LL, member='window_i0012.gim', word='Proibita', ix=(3, 106), icon=('lim_forbid', 3), tx=(16, 84.5), slot=(87, 106)),
    'title_menu_i__t_window0008': dict(file=TM, member='t_window0008.gim', word='Scambio', ix=(3, 56), icon=None, tx=(4, 43), slot=(45, 56), heal=((1, 1, 2, 1),)),
    'title_menu_i__t_window0026': dict(file=TM, member='t_window0026.gim', word='Scambio', ix=(3, 56), icon=None, tx=(4, 43), slot=(45, 56), heal=((1, 1, 2, 1),)),
}

# francese: stessa geometria dell'italiano (stessi riquadri), parole e limite destro del testo misurati sulle texture francesi.
# Le altre texture della famiglia (pannelli, dmenu, parts) hanno lo stesso hash in tutte le lingue: restano quelle italiane.
# 'Scambia' e' un residuo italiano nelle texture francesi: si scrive 'Échange'.
FR_WORDS = {'recipe010008': ('Personnage', 122.5), 'recipe010015': ('Utilisateur', 67.5), 'recipe010027': ('Téléchargée', 98.5),
            'recipe010029': ('Personnage', 82.5), 'recipe010031': ('Utilisateur', 69.5), 'recipe_sel00033': ('Personnage', 80.5),
            'window_i0002': ('Limitée', None), 'window_i0004': ('Semi-limitée', None), 'window_i0012': ('Interdite', None),
            't_window0008': ('Échange', None), 't_window0026': ('Échange', None)}
ES_WORDS = {'recipe010008': ('Personaje', 121.0), 'recipe010015': ('Usuario', 56.5), 'recipe010027': ('Recetas descargadas', 120.5),
            'recipe010029': ('Recetas de personaje', 107.5), 'recipe010031': ('Recetas de usuario', 105.5),
            'recipe_sel00033': ('Recetas de personaje', 105.5), 'window_i0002': ('Limitada', None),
            'window_i0004': ('Semi-Limitada', None), 'window_i0012': ('Prohibida', None),
            't_window0008': ('Cambiar', None), 't_window0026': ('Cambiar', None)}
# tedesco: parole dell'originale tedesco; limite destro = fine dell'inchiostro bianco misurato sulle texture tedesche (meno mezzo pixel)
DE_WORDS = {'recipe010008': ('Charakter', 122.5), 'recipe010015': ('Benutzer', 61.5), 'recipe010027': ('Heruntergeladene', 120.5),
            'recipe010029': ('Charakterrezepte', 109.5), 'recipe010031': ('Benutzerrezepte', 103.5),
            'recipe_sel00033': ('Charakterrezepte', 107.5), 'window_i0002': ('Limitiert', None),
            'window_i0004': ('Halblimitiert', None), 'window_i0012': ('Verboten', None),
            't_window0008': ('Tauschen', None), 't_window0026': ('Tauschen', None)}   # 'Échange' e' un residuo francese nella texture tedesca
_LANG = os.environ.get('TF1_LANG', 'it')
EN_WORDS = {'recipe010008': ('Character', 122.5), 'recipe010015': ('User', 38.0), 'recipe010027': ('Downloaded Recipes', 122.5),
            'recipe010029': ('Character Recipes', 112.0), 'recipe010031': ('User Recipes', 85.0), 'recipe_sel00033': ('Character Recipes', 109.5),
            'window_i0002': ('Limited', 78.0), 'window_i0004': ('Semi-Limited', 102.0), 'window_i0012': ('Forbidden', 78.0),
            't_window0008': ('Trade', 36.5), 't_window0026': ('Trade', 36.5)}   # inglese europeo: parole e limiti misurati sulle texture originali
_LET = {'fr': 'f', 'es': 's', 'de': 'g', 'en': 'e'}.get(_LANG)
TABS_FR = {}
if _LET:
    for _tid, _sp in TABS.items():
        _w, _r = {'fr': FR_WORDS, 'es': ES_WORDS, 'de': DE_WORDS, 'en': EN_WORDS}[_LANG][_sp['member'][:-4]]
        TABS_FR[_tid.replace('_i__', f'_{_LET}__').replace('_i0', f'_{_LET}0')] = dict(
            _sp, file=_sp['file'].replace('_i.ehp', f'_{_LET}.ehp'), member=_sp['member'].replace('_i0', f'_{_LET}0'), word=_w,
            tx=(_sp['tx'][0], _r if _r else _sp['tx'][1]))

LIMITED = 'ui/limited.png'
SPRITES = {'lim_forbid': (0, 304, 36, 341), 'lim_1': (48, 304, 85, 341), 'lim_2': (95, 304, 132, 341)}


def sprite(pack, name):
    x0, y0, x1, y1 = SPRITES[name]
    return arr(common.reference(pack, LIMITED))[y0:y1, x0:x1].copy()


def box_down(a):
    h, w = a.shape[0] // S, a.shape[1] // S
    return a.reshape(h, S, w, S, a.shape[2]).mean((1, 3))


def fit_sprite(hd, low_a, spr, xy, search=6):
    """composite the HD sprite over hd at the HD offset (around 4*xy, +-search px) whose box-downscale best matches the
    original (premultiplied colour error over the sprite window)."""
    h, w = spr.shape[:2]
    bx, by = int(round(xy[0] * S)), int(round(xy[1] * S))
    low = low_a.astype(np.float32) / 255.0
    best = None
    for dy in range(-search, search + 1):
        for dx in range(-search, search + 1):
            x, y = bx + dx, by + dy
            if x < 0 or y < 0 or x + w > hd.shape[1] or y + h > hd.shape[0]:
                continue
            wx0, wy0 = (x // S) * S, (y // S) * S
            wx1, wy1 = -(-(x + w) // S) * S, -(-(y + h) // S) * S
            win = hd[wy0:wy1, wx0:wx1].copy()
            layer = np.zeros_like(win)
            layer[y - wy0:y - wy0 + h, x - wx0:x - wx0 + w] = spr
            win = over(win, layer)
            d = box_down(premul(win))
            l = premul(low[wy0 // S:wy1 // S, wx0 // S:wx1 // S])
            e = float(np.abs(d - l).mean())
            if best is None or e < best[0]:
                best = (e, x, y)
    _, x, y = best
    layer = np.zeros_like(hd)
    layer[y:y + h, x:x + w] = spr
    return over(hd, layer), best


def band_profile(low_a, ix0, ix1):
    """per-row colour of the flat coloured band of a tab (rows 3..17): rows 3..13 are flat (mode of row 3), rows 14..17
    are the lower bevel (mode of the row over the band, text/icon columns are a minority there)."""
    row3 = Counter(tuple(low_a[3, x]) for x in range(ix0, ix1 + 1)).most_common(1)[0][0]
    prof = [row3] * 11
    for y in range(14, 18):
        row = [tuple(low_a[y, x]) for x in range(ix0, ix1 + 1) if int(low_a[y, x, :3].min()) < 230]
        prof.append(Counter(row).most_common(1)[0][0])
    return np.array(prof, np.uint8)


def clean_band(low_a, ix0, ix1):
    """the Italian tab with text, icon and white slot wiped from the band (columns ix0+1 .. ix1-1, rows 3..17)."""
    prof = band_profile(low_a, ix0, ix1)
    out = low_a.copy()
    out[3:18, ix0 + 1:ix1] = prof[:, None, :]
    return out, prof


def heal(a, fixes):
    """replace lone single pixels (x, y, from_x, from_y) of a low-res frame by their neighbour's colour before the EPX upscale: an
    isolated corner pixel that equals another one two cells away is otherwise turned into a small diamond/blip."""
    a = a.copy()
    for x, y, sx, sy in fixes:
        a[y, x] = a[sy, sx]
    return a


def tab_base(low, ix0, ix1, fixes=()):
    a = np.asarray(low.convert('RGBA'))
    clean, prof = clean_band(a, ix0, ix1)
    hd = upscale(Image.fromarray(heal(clean, fixes), 'RGBA'))
    return hd, prof


DOC = ('BBBBBBBBB', 'BWWWWWWWB', 'BWMWMMMWB', 'BWWWWWWWB', 'BWMMMMWWB', 'BWWWWWWWB', 'BWMMWMMWB',
       'BWWWWWWWB', 'BWMMWMWWB', 'BWWWWWWWB', 'BWMWMMMWB', 'BWWWWWWWB', 'BBBBBBBBB')      # 9 x 13 cells of the game's document icon
DOC_COLORS = {'blue': (48, 111, 169), 'pink': (195, 22, 165), 'green': (0, 122, 46)}
# 'downloaded recipe' document of the European game (green, white page, brown-outlined yellow lightning bolt that pokes through the
# bottom edge): the original's 10 x 15 cells (page, bolt and its pixel shadow) are read once from dmenu_recipe (x 38, y 2) in main()
BOLT_CELLS = [None]
BOLT_BOX = (38, 2, 48, 17)


def stamp(hd, spr, x, y):
    layer = np.zeros_like(hd)
    h, w = spr.shape[:2]
    layer[y:y + h, x:x + w] = spr
    return over(hd, layer)


def doc_sprite(color, bolt=False, shadow_a=0.42):
    """HD sprite (14 x 10 cells) of the game's document icon: crisp pixel-art cells (the same look as the mod's own document
    icons, 4x nearest) plus a hard shadow; bolt=True: the European 'downloaded recipe' icon (green document, yellow bolt, 15 x 10 cells):
    the original's cells at 4x nearest as well - the bolt is drawn on the same pixel grid as the page (hard 1-cell brown outline, hard
    1-cell shadow), like the mod does for its own 'DL' document."""
    if bolt:
        cells = BOLT_CELLS[0].copy()
        shadow = (cells[..., :3].max(-1) == 0) & (cells[..., 3] < 1)           # the original's translucent black shadow cells
        cells[shadow, 3] *= shadow_a / 0.5
        return nearest(cells)
    cells = np.zeros((13, 9, 4), np.float32)
    for y, row in enumerate(DOC):
        for x, ch in enumerate(row):
            cells[y, x] = (1, 1, 1, 1) if ch == 'W' else (*[c / 255.0 for c in color], 1)
    h, w = 14 * S, 10 * S
    spr = np.zeros((h, w, 4), np.float32)
    sil = np.zeros((h, w), np.float32)
    sil[S:14 * S, S:10 * S] = 1.0
    spr = paint(spr, sil * shadow_a, (0, 0, 0))
    spr[:13 * S, :9 * S] = over(spr[:13 * S, :9 * S], nearest(cells))
    return spr


RECIPE_SIZE = 41.5 if _LANG == 'de' else 38.0      # letter size of every recipe-view / recipe-select tab (the longest words fit their slots with <= 7 % squeeze); de: le lettere dell'originale tedesco sono piu' larghe (~5,8 px a lettera)


def render_exact(word, fill, shape, x0, x_limit, size):
    """tab word at a given size and the standard tracking, squeezed (at most 10 %) so that the white ink ends at x_limit (HD px), the
    shadow outside it; baseline as tabword.render_tab_word places words below the full size."""
    base = 54 - 0.35 * (tabword.SIZE - size)
    track = tabword.TRACK
    if _LANG == 'de' and len(word) > 1:      # il testo tedesco dell'originale e' piu' largo: si allarga la spaziatura (max +3 px a lettera) fino al limite
        slot = x_limit - x0
        for _ in range(3):
            lo, hi = tabword.ink_extent(word, size, track)
            track = min(tabword.TRACK + 3.0, track + (slot - (hi - lo)) / (len(word) - 1))
    return tabword.render_word(word, fill, shape, x0, x_limit + tabword.SHADOW[0] + tabword.OUTLINE, base, size=size, track=track)


def build_tab(tid, spec, low):
    ix0, ix1 = spec['ix']
    H, W = low.height * S, low.width * S
    low_a = np.asarray(low.convert('RGBA'))
    hd, prof = tab_base(low, ix0, ix1, spec.get('heal', ()))
    kind, ic_x = spec['icon'] if spec.get('icon') else (None, None)
    if kind in ('doc', 'bolt'):
        col = DOC_COLORS['green' if kind == 'bolt' else spec.get('doc', 'blue')]
        hd = stamp(hd, doc_sprite(col, bolt=(kind == 'bolt')), ic_x * S, 3 * S)
    elif kind in SPRITES:
        hd, _ = fit_sprite(hd, low_a, sprite(PACK[0], kind), (ic_x, 4))
    if spec.get('slot'):
        sx0, sx1 = spec['slot']
        hd = paint(hd, rrect(H, W, sx0 * S, 3 * S, sx1 * S, 15 * S, 3.0), (255, 255, 255))
    fill = tuple(int(v) for v in prof[5][:3])
    t0, t1 = spec['tx']
    if spec.get('exact'):
        # recipe tabs: ONE size for the whole group, and the white ink really ends at the right limit (tx[1])
        lay, info = render_exact(spec['word'], fill, (H, W), t0 * S, t1 * S, RECIPE_SIZE)
    else:
        cap = 45.0 if tid.startswith('limitlist__') else 41.0  # one common size per group of sibling tabs
        lay, info = tabword.render_tab_word(spec['word'], fill, (H, W), t0 * S, t1 * S + 4.2, 54, cap=cap)
    INFO[tid] = info
    return over(hd, lay)


# ------------------------------------------------------------------------------------------------ recipe-view panels
PANELS = {
    # bar rows to wipe (inclusive), stripes rows below the bar that carry the text shadow, wipe columns, icon, word, text start (low px), baseline (HD px)
    'recipe_view_i__recipe010002': dict(member='recipe010002.gim', word='Deck', rows=(2, 12), srows=(13, 16), cols=(4, 62), icon='deck', ix=(4, 2), tx=16, base=48),
    'recipe_view_i__recipe010004': dict(member='recipe010004.gim', word='Fusion Deck', rows=(0, 10), srows=(11, 14), cols=(3, 92), icon='swirl', ix=(3, 0), tx=15.2, base=40),
    'recipe_view_i__recipe010006': dict(member='recipe010006.gim', word='Side Deck', rows=(0, 10), srows=(11, 14), cols=(3, 78), icon='card', ix=(4, 0), tx=15.2, base=40),
}
PANEL_REF_X = 150


def build_panel(tid, spec, low):
    H, W = low.height * S, low.width * S
    a = np.asarray(low.convert('RGBA')).copy()
    r0, r1 = spec['rows']
    c0, c1 = spec['cols']
    a[r0:r1 + 1, c0:c1] = a[r0:r1 + 1, PANEL_REF_X:PANEL_REF_X + 1]
    s0, s1 = spec['srows']
    a[s0:s1 + 1, c0 + 2:c1] = a[s0:s1 + 1, PANEL_REF_X:PANEL_REF_X + 1]
    hd = upscale(Image.fromarray(a, 'RGBA'))
    ix, iy = spec['ix']
    if spec['icon'] == 'deck':
        hd = stamp(hd, pouch_sprite(), ix * S, iy * S)
    elif spec['icon'] == 'card':
        hd = stamp(hd, card_sprite(), ix * S, iy * S)
    else:
        spr = swirl_sprite(PACK[0], 38)
        hd, _ = fit_sprite(hd, np.asarray(low.convert('RGBA')), spr, (ix, iy), search=8)
    bar = tuple(int(v) for v in a[r0 + 4, PANEL_REF_X, :3])
    t0 = spec['tx']
    word = spec['word']
    lo, hi = tabword.ink_extent(word, tabword.SIZE)
    lay, info = tabword.render_word(word, bar, (H, W), t0 * S, t0 * S + (hi - lo) + 4.2 + 2, spec['base'])
    INFO[tid] = info
    return over(hd, lay)


# ------------------------------------------------------------------------------------------------ title menu: recipe panel (marble bars)
BARS = ((0, 'doc', 'blue', (2, 1)), (32, 'doc', 'pink', (2, 33)), (64, 'bolt', 'green', (3, 66)))


def smoothstep(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


MARBLE_COLS = (13, 127)       # columns of a bar's marble that are not disturbed by the icon (palette + level statistics)
V_HI = 0.13                   # marble level (0 = vein colour, 1 = lightest blotch) below which a pixel counts as vein
V_BASE = 0.22                 # level of the flat base colour of the marble
BLOT_SIG = 0.8                # low-res smoothing of the blotch field before the cubic upscale
VEIN_SIG, VEIN_T0, VEIN_T1 = 0.6, 0.30, 0.50   # vein field: smoothing (low px) and the smoothstep that turns it into a clean line


def marble_palette(clean):
    """palette of an undisturbed marble bar: the marble is an indexed image of ~19 colours of ONE colour ramp (dark vein colour ->
    flat base -> light blotches -> white glints).  Returns the principal axis of the palette (the marble level of a colour is its
    projection on it, 0..1) and the palette sorted along it."""
    u, cnt = np.unique(np.rint(clean.reshape(-1, 3) * 255).astype(np.int32), axis=0, return_counts=True)
    u, cnt = u[cnt >= 4].astype(np.float64), cnt[cnt >= 4].astype(np.float64)
    mean = (u * cnt[:, None]).sum(0) / cnt.sum()
    cov = ((u - mean).T * cnt) @ (u - mean)
    d = np.linalg.eigh(cov)[1][:, -1]
    if d @ np.array([0.299, 0.587, 0.114]) < 0:
        d = -d
    p = (u - mean) @ d
    lo, hi = p.min(), p.max()
    order = np.argsort(p, kind='stable')
    return dict(d=d, mean=mean, lo=lo, hi=hi, level=(p[order] - lo) / (hi - lo), rgb=u[order] / 255.0)


def marble_level(reg, pal):
    return np.clip(((reg.reshape(-1, 3) * 255 - pal['mean']) @ pal['d'] - pal['lo']) / (pal['hi'] - pal['lo']), 0, 1).reshape(reg.shape[:2])


def vein_field(v):
    """vein probability (low-res) -> 4-connected network: isolated specks are dropped, diagonal steps are bridged so that the thin
    lines stay connected after the smoothing."""
    m = (v > 0.5).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] <= 2:
            v = np.where(lab == i, 0.0, v)
    vb = v.copy()
    on = v > 0.5
    d1 = on[:-1, :-1] & on[1:, 1:] & ~on[:-1, 1:] & ~on[1:, :-1]       # \ diagonal step
    d2 = on[:-1, 1:] & on[1:, :-1] & ~on[:-1, :-1] & ~on[1:, 1:]       # / diagonal step
    for y, x in zip(*np.nonzero(d1)):
        vb[y, x + 1] = max(vb[y, x + 1], 0.5)
        vb[y + 1, x] = max(vb[y + 1, x], 0.5)
    for y, x in zip(*np.nonzero(d2)):
        vb[y, x] = max(vb[y, x], 0.5)
        vb[y + 1, x + 1] = max(vb[y + 1, x + 1], 0.5)
    return vb


def marble_up(reg, pal):
    """clean 4x marble from the low-res indexed marble (HxWx3, 0..1): a smooth gradient field for the light blotches (cubic, no
    sharpening, so no grain/halos), a flat base, and the veins rebuilt as constant-width antialiased lines (vein probability
    -> smooth upscale -> hard smoothstep) in the vein colour of the palette."""
    h, w = reg.shape[:2]
    s = marble_level(reg, pal)
    cub = lambda f: cv2.resize(f, (w * S, h * S), interpolation=cv2.INTER_CUBIC)
    blot = cub(cv2.GaussianBlur(np.clip((s - V_BASE) / (1 - V_BASE), 0, 1).astype(np.float32), (0, 0), BLOT_SIG))
    lvl = V_BASE + np.clip(blot, 0, 1) * (1 - V_BASE)
    col = np.stack([np.interp(lvl, pal['level'], pal['rgb'][:, c]) for c in range(3)], -1)
    v = vein_field(np.clip((V_HI - s) / V_HI, 0, 1).astype(np.float32))
    vh = cub(cv2.GaussianBlur(v, (0, 0), VEIN_SIG))
    vm = smoothstep(vh, VEIN_T0, VEIN_T1) * (1 - smoothstep(blot, 0.25, 0.5))
    vein = np.asarray(pal['rgb'][0], np.float32)
    return np.clip(col * (1 - vm[..., None]) + vein * vm[..., None], 0, 1).astype(np.float32)


def band_up(reg, axis, amount=0.6, sigma=2.0):
    """upscale a frame band that is a crisp line pattern across and a smooth mottling along its length: cubic along `axis`
    (0: rows run along y, 1: along x), nearest across."""
    h, w = reg.shape[:2]
    if axis == 1:
        c = cv2.resize(reg, (w * S, h), interpolation=cv2.INTER_CUBIC)
        out = np.repeat(c, S, 0)
    else:
        c = cv2.resize(reg, (w, h * S), interpolation=cv2.INTER_CUBIC)
        out = np.repeat(c, S, 1)
    return np.clip(out, 0, 1)


def calm_band(reg, sigma=1.5):
    """left frame band (5 columns): the two outer columns carry a strong mottling along the band; a light vertical gaussian keeps the
    pattern but takes the smeared blotches out, so the band matches the calm right edge of the bars."""
    out = reg.copy()
    out[:, 0:2] = cv2.GaussianBlur(np.ascontiguousarray(reg[:, 0:2]), (1, 9), 0, sigmaY=sigma, borderType=cv2.BORDER_REPLICATE)
    return out


def inpaint(low_a, box):
    """fill the low-res box (x0, y0, x1, y1) from its surroundings (hidden under an icon that is redrawn)."""
    x0, y0, x1, y1 = box
    mask = np.zeros(low_a.shape[:2], np.uint8)
    mask[y0:y1, x0:x1] = 255
    rgb = cv2.inpaint(np.ascontiguousarray(low_a[..., :3]), mask, 3, cv2.INPAINT_TELEA)
    out = low_a.copy()
    out[y0:y1, x0:x1, :3] = rgb[y0:y1, x0:x1]
    out[y0:y1, x0:x1, 3] = 255
    return out


def fill_icon_hole(a, bar_y0, box):
    """wipe an icon (and its shadow, box = x0, y0, x1, y1) from a marble bar: the top band continues from the right, the
    left frame columns repeat the clean rows below, the marble is inpainted."""
    x0, y0, x1, y1 = box
    a = a.copy()
    for y in range(y0, bar_y0 + 3):
        a[y, x0:x1] = a[y, x1]
    for y in range(bar_y0 + 3, y1):
        a[y, x0:5] = a[y1 + (y1 - 1 - y) % 3, x0:5]
    return inpaint(a, (5, bar_y0 + 3, x1, y1))


BUTTON_BOX = (24, 96, 38, 116)      # the 'back to the deck' button of the recipe panel (low-res box, square corners)


def square_corners(hd, fa, box):
    """the EPX upscale rounds the convex corners of a box; the original's box is square, so the four corner pixels are put back as
    plain 4x4 blocks of their original colour."""
    x0, y0, x1, y1 = box
    hd = hd.copy()
    for cx, cy in ((x0, y0), (x1 - 1, y0), (x0, y1 - 1), (x1 - 1, y1 - 1)):
        hd[cy * S:(cy + 1) * S, cx * S:(cx + 1) * S] = fa[cy, cx]
    return hd


def build_recipe_panel(low):
    H, W = low.height * S, low.width * S
    a0 = np.asarray(low.convert('RGBA')).copy()
    a = a0.copy()
    for y0, kind, col, (dx, dy) in BARS:
        a = fill_icon_hole(a, y0, (dx, dy, dx + 10, dy + (17 if kind == 'bolt' else 14)))
    for y in range(98, 113):                              # icon of the button: marble of the rows below, mirrored
        a[y, 26:38] = a[113 + (112 - y) % 3, 26:38]
    hd = upscale(Image.fromarray(a, 'RGBA'))
    fa = a.astype(np.float32) / 255.0
    hd = square_corners(hd, fa, BUTTON_BOX)
    for y0, kind, col, (dx, dy) in BARS:
        r0, r1 = y0 + 3, y0 + 26
        pal = marble_palette(fa[r0:r1, MARBLE_COLS[0]:MARBLE_COLS[1], :3])
        m = marble_up(fa[r0:r1, 5:127, :3], pal)
        hd[r0 * S:r1 * S, 5 * S:127 * S] = np.concatenate([m, np.ones(m.shape[:2] + (1,), np.float32)], -1)
        hd[y0 * S:r0 * S, 5 * S:127 * S] = band_up(fa[y0:r0, 5:127], 1)               # top band
        hd[r1 * S:(y0 + 29) * S, 5 * S:127 * S] = band_up(fa[r1:y0 + 29, 5:127], 1)   # bottom band
        hd[r0 * S:r1 * S, 0:5 * S] = band_up(calm_band(fa[r0:r1, 0:5]), 0)            # left band
        hd[r0 * S:r1 * S, 127 * S:128 * S] = band_up(fa[r0:r1, 127:128], 0)           # right edge
    for k in range(3):                                   # right end caps of the three bars: crisp lines across, smooth along
        hd[97 * S:124 * S, 8 * k * S:(8 * k + 5) * S] = band_up(calm_band(fa[97:124, 8 * k:8 * k + 5]), 0)
    for y0, kind, col, (dx, dy) in BARS:
        hd = stamp(hd, doc_sprite(DOC_COLORS[col], bolt=(kind == 'bolt'), shadow_a=0.5), dx * S, dy * S)
    # 'back to the deck' button: corner of the blue bar + deck-box icon with a yellow return arrow
    hd = stamp(hd, pouch_sprite(0.4), 26 * S, 98 * S)
    spr, (ax, ay) = arrow_sprite()
    hd, _ = fit_sprite(hd, a0, spr, ((26 * S + ax) / S, (98 * S + ay) / S), search=6)
    return hd


# ------------------------------------------------------------------------------------------------ title menu: recipe icons + digits
def build_dmenu(low):
    H, W = low.height * S, low.width * S
    a = np.asarray(low.convert('RGBA')).astype(np.float32) / 255.0
    hd = np.zeros((H, W, 4), np.float32)
    for x, kind, col in ((4, 'doc', 'blue'), (21, 'doc', 'pink'), (38, 'bolt', 'green')):
        hd = stamp(hd, doc_sprite(DOC_COLORS[col], bolt=(kind == 'bolt'), shadow_a=0.5), x * S, 2 * S)
    hd[:, 56 * S:] = nearest(a[:, 56:])          # digits 0-9: the game's pixel font, 4x nearest (pixel-identical to ui/duels/numbers.png, row 1)
    return hd


# ------------------------------------------------------------------------------------------------ duel record parts
class no_shadow:
    """tabword with its hard shadow and outline switched off (dark-on-light or flat badge lettering)."""

    def __enter__(self):
        self.old = (tabword.SHADOW, tabword.OUTLINE)
        tabword.SHADOW, tabword.OUTLINE = (0.0, 0.0), 0.0

    def __exit__(self, *a):
        tabword.SHADOW, tabword.OUTLINE = self.old


def poly_cov(h, w, pts, SS=4):
    """antialiased coverage (HD px) of a polygon given in HD coordinates."""
    can = np.zeros((h * SS, w * SS), np.uint8)
    cv2.fillPoly(can, [np.round(np.asarray(pts, np.float64) * SS).astype(np.int32)], 255)
    return cv2.resize(can, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0


def arrows(H, W):
    """the yellow scroll arrows (three pairs, the last two semi-transparent as in the sheet) and the two dark arrow buttons
    of the sheet, drawn as crisp symmetric vector triangles on the sheet's grid (low-res coordinates x S)."""
    out = blank(H, W)
    tri = lambda pts: poly_cov(H, W, [(x * S, y * S) for x, y in pts])
    cx = 50.1
    for k, al in enumerate((1.0, 0.63, 0.44)):
        dy = 16 * k
        up = tri([(cx, 1.85 + dy), (cx - 2.95, 6.0 + dy), (cx + 2.95, 6.0 + dy)])
        dn = tri([(cx - 2.95, 8.0 + dy), (cx + 2.95, 8.0 + dy), (cx, 12.15 + dy)])
        out = paint(out, np.maximum(up, dn) * al, (255, 255, 31))
    # dark buttons: black triangle, translucent grey ring, translucent white lower edge
    cx = 50.0
    ring = tri([(cx, 47.7), (cx - 3.4, 52.95), (cx + 3.4, 52.95)])
    core = tri([(cx, 48.9), (cx - 2.45, 52.0), (cx + 2.45, 52.0)])
    out = paint(out, np.clip(ring - core, 0, 1) * 0.5, (127, 127, 127))
    out = paint(out, core, (0, 0, 0))
    out = paint(out, tri([(cx - 3.0, 52.0), (cx + 3.0, 52.0), (cx + 3.0, 53.0), (cx - 3.0, 53.0)]) * 0.5, (255, 255, 255))
    ring = tri([(cx - 3.4, 55.9), (cx + 3.4, 55.9), (cx, 61.0)])
    core = tri([(cx - 2.45, 56.9), (cx + 2.45, 56.9), (cx, 59.9)])
    out = paint(out, np.clip(ring - core, 0, 1) * 0.5, (127, 127, 127))
    out = paint(out, core, (0, 0, 0))
    out = paint(out, np.clip(ring - core, 0, 1) * np.clip((np.mgrid[0:H, 0:W][1] / S - cx) * 0.9, 0, 1) * 0.5, (255, 255, 255))
    return out


def build_parts(low):
    H, W = low.height * S, low.width * S
    a = np.asarray(low.convert('RGBA')).copy()
    red, orange = (255, 0, 0, 255), (255, 168, 0, 255)
    a[0:12, 0:12] = 0                                    # the red R square: redrawn as clean vector shapes
    a[2:7, 14:33] = orange                               # NUOVO, wiped
    a[0:63, 46:54] = 0                                   # arrows: redrawn as vector triangles
    a = heal(a, ((22, 40, 21, 40), (22, 60, 21, 60)))    # lone light pixel in the bottom-right corner of the pink / red bevelled pieces
    hd = upscale(Image.fromarray(a, 'RGBA'))
    hd = over(hd, arrows(H, W))
    sq = rrect(H, W, 0, 0, 11 * S, 11 * S, 3.0)
    hd = paint(hd, shift_mask(sq, S, S) * 0.5, (0, 0, 0))
    hd = paint(hd, sq, (255, 0, 0))
    with no_shadow():
        lay, info = tabword.render_word('R', (255, 0, 0), (H, W), 2 * S, 2 * S + 28 + 0.0, 9 * S, size=40, track=-3.8,
                                        fill_top=(255, 255, 255), fill_bottom=(255, 255, 255))
        hd = over(hd, lay)
        INFO['R'] = info
        lay, info = tabword.render_word('NUOVO', (255, 168, 0), (H, W), 14 * S, 33 * S, 7 * S - 1, size=26,
                                        fill_top=(0, 36, 60), fill_bottom=(0, 36, 60))
        hd = over(hd, lay)
        INFO['NUOVO'] = info
    return hd


INFO = {}
PACK = [None]


def main(argv):
    fam = common.Family('schede_ricette', argv)
    PACK[0] = fam.pack_us
    low, _ = common.texture(fam.usrdir, TM, 'dmenu_recipe.gim')
    x0, y0, x1, y1 = BOLT_BOX
    BOLT_CELLS[0] = arr(low)[y0:y1, x0:x1]
    fr = _LANG != 'it'
    for tid, spec in (TABS_FR if fr else TABS).items():
        low, h = common.texture(fam.usrdir, spec['file'], spec['member'])
        hd = clean_alpha(build_tab(tid, spec, low), low)
        fam.save(tid, img(hd), h, low)
    if _LANG == 'de':     # 'Fusionsdeck' (nell'originale tedesco la linguetta e' scritta cosi'; Deck e Side Deck hanno lo stesso hash dell'inglese)
        spec = dict(PANELS['recipe_view_i__recipe010004'], word='Fusionsdeck')
        low, h = common.texture(fam.usrdir, 'deck/recipe_view_g.ehp', spec['member'])
        fam.save('recipe_view_g__recipe010004', img(clean_alpha(build_panel('recipe_view_g__recipe010004', spec, low), low)), h, low)
    if fr:
        fam.finish()
        return
    low, h = common.texture(fam.usrdir, TM, 'recipe_panel.gim')
    fam.save('title_menu_i__recipe_panel', img(clean_alpha(build_recipe_panel(low), low)), h, low)
    low, h = common.texture(fam.usrdir, TM, 'dmenu_recipe.gim')
    fam.save('title_menu_i__dmenu_recipe', img(clean_alpha(build_dmenu(low), low)), h, low)
    low, h = common.texture(fam.usrdir, 'database/duelrecord.ehp', 'parts_i.gim')
    fam.save('duelrecord__parts_i', img(clean_alpha(build_parts(low), low)), h, low)
    for tid, spec in PANELS.items():
        low, h = common.texture(fam.usrdir, RV, spec['member'])
        hd = clean_alpha(build_panel(tid, spec, low), low)
        fam.save(tid, img(hd), h, low)
    fam.finish()
    for k, v in INFO.items():
        print(k, {a: (round(b, 2) if isinstance(b, float) else b) for a, b in v.items()})


if __name__ == '__main__':
    main(sys.argv)
