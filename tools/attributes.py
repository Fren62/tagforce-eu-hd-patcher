"""Attribute symbols (LIGHT, DARK, WATER, FIRE, EARTH, WIND, SPELL, TRAP, DIVINE) with the lettering in the card's language.
In the game the icon table (icon01.gim, the same in all languages) has the English lettering; on the real cards each language has its own
(LUCE, OSCURITA' ... / LUMIERE, TENEBRES... / LICHT, FINSTERNIS... / LUZ, OSCURIDAD...). The words are the game's own
(DLG_Text of cardinfo_xxx.ehp, indexes 531-539, see languages.py).
usage: attributes.py table LANGUAGE PACK OUT_PNG [CARDINFO.ehp]    icons_attribute_race.png with the language's lettering
       attributes.py cards LANGUAGE PACK SMALL_CARDS_DIR           replaces the icon on the small cards (cards/small_<l>) in place
The table is unique per installation (same hash in all languages): with several languages the first wins."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import alt_font   # noqa: nessun font Apple
import languages

ORDER = ['LIGHT', 'DARK', 'WATER', 'FIRE', 'EARTH', 'WIND', 'SPELL', 'TRAP', 'DIVINE']
INDEX_DLG = {'LIGHT': 531, 'DARK': 532, 'WATER': 533, 'FIRE': 534, 'EARTH': 535, 'WIND': 536, 'DIVINE': 537, 'SPELL': 538, 'TRAP': 539}
# large 62x62 and small 45x45 icons in the pack's 512x512 table (cards/frame/icons_attribute_race.png)
LARGE = {'LIGHT': (1, 274), 'DARK': (69, 274), 'WATER': (137, 274), 'FIRE': (205, 274), 'EARTH': (273, 274), 'WIND': (341, 274),
          'SPELL': (409, 274), 'TRAP': (341, 342), 'DIVINE': (409, 342)}
SMALL = {n: (48 * i, 432) for i, n in enumerate(ORDER)}
# text band: (y0, y1, x0, x1, capital height, maximum width) relative to the icon
BAND = {62: (5, 18, 6, 56, 9.0, 40), 45: (3, 12, 5, 41, 6.0, 29)}
FONT = os.path.join(HERE, 'alt_fonts', 'static', 'Tinos-Bold.ttf')
SS = 8


def words(cardinfo):
    d = languages.dlg(cardinfo)
    return {n: d[INDEX_DLG[n]].upper() for n in ORDER}


def clean(icon, band):
    """erases the lettering with inpainting: mask = very light, low-saturation pixels in the band (plus border)."""
    s = icon.shape[0]
    y0, y1, x0, x1, _, _ = band
    rgb = icon[..., :3]
    mx, mn = rgb.max(-1).astype(int), rgb.min(-1).astype(int)
    light = (mn >= 150) & ((mx - mn) < 80)
    m = np.zeros(light.shape, np.uint8)
    m[y0:y1, x0:x1] = light[y0:y1, x0:x1]
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=2)
    m[y1:] = 0                      # never above the kanji
    out = cv2.inpaint(np.ascontiguousarray(rgb), m, 3, cv2.INPAINT_TELEA)
    # inpainting darkens the cleaned area (it takes the dark colours under the lettering): it is filled vertically instead,
    # interpolating in every column between the first untouched pixel above and the one below the lettering
    vert = rgb.astype(np.float32).copy()
    for x in range(m.shape[1]):
        col = np.where(m[:, x] > 0)[0]
        if not len(col):
            continue
        for run in np.split(col, np.where(np.diff(col) > 1)[0] + 1):
            a_, b_ = run[0] - 1, run[-1] + 1
            if a_ < 0 or b_ >= m.shape[0]:
                continue
            t = ((run - a_) / (b_ - a_)) ** 0.3          # the colour below the lettering weighs more than the one on the dark border above
            vert[run, x] = rgb[a_, x] * (1 - t)[:, None] + rgb[b_, x] * t[:, None]
    w = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.8)[..., None].clip(0, 1) * (m > 0).astype(np.float32)[..., None]
    out = np.where((m > 0)[..., None], vert * 0.85 + out.astype(np.float32) * 0.15, out).astype(np.uint8)
    res = icon.copy(); res[..., :3] = out
    return res


def draw(icon, text, band):
    s = icon.shape[0]
    y0, y1, x0, x1, cap, wmax = band
    f = ImageFont.truetype(FONT, int(round(cap / 0.66 * SS)))     # Tinos capitals are about 0.66 em
    asc = -f.getbbox('H', anchor='ls')[1]
    base = int(asc * 1.6)                                          # space above the baseline for the accents
    W, H = int(f.getlength(text)) + 8 * SS, base + int(asc * 0.5)
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).text((4 * SS, base), text, font=f, fill=255, anchor='ls')
    xs = np.where(np.asarray(m).max(0) > 0)[0]
    m = m.crop((xs.min(), 0, xs.max() + 1, H))
    larg = min(m.width / SS, wmax)
    m = m.resize((max(1, round(larg)), max(1, round(H / SS))), Image.LANCZOS)
    a = np.asarray(m).astype(np.float32) / 255
    out = icon.astype(np.float32).copy()
    X = (s - a.shape[1]) // 2
    Y = y0 + 2 + cap - base / SS          # the baseline stays where the English text's was
    Y = int(round(Y))
    h, w = a.shape
    ys0, xs0 = max(Y, 0), max(X, 0)
    a = a[ys0 - Y:, xs0 - X:]
    h, w = a.shape
    shadow = np.zeros(out.shape[:2], np.float32)
    shadow[ys0 + 1:ys0 + 1 + h, xs0:xs0 + w] = a[:max(0, out.shape[0] - ys0 - 1), :][:h]
    shadow = cv2.GaussianBlur(shadow, (0, 0), 0.6) * 0.5
    out[..., :3] *= (1 - shadow)[..., None]
    reg = out[ys0:ys0 + h, xs0:xs0 + w, :3]
    out[ys0:ys0 + h, xs0:xs0 + w, :3] = reg * (1 - a[..., None]) + 255 * a[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


def icon_localized(sheet, name, large, text):
    x, y = (LARGE if large else SMALL)[name]
    s = 62 if large else 45
    ic = np.asarray(sheet.crop((x, y, x + s, y + s)))
    ic = clean(ic, BAND[s])
    return draw(ic, text, BAND[s])


def build_table(language, pack, out, cardinfo):
    sheet = Image.open(os.path.join(pack, 'cards/frame/icons_attribute_race.png')).convert('RGBA')
    names = words(cardinfo)
    res = sheet.copy()
    for name in ORDER:
        for large in (True, False):
            x, y = (LARGE if large else SMALL)[name]
            ic = Image.fromarray(icon_localized(sheet, name, large, names[name]), 'RGBA')
            res.paste(ic, (x, y))
    res.save(out)
    print('written', out)


ATTR_NAME = {1: 'LIGHT', 2: 'DARK', 3: 'WATER', 4: 'FIRE', 5: 'EARTH', 6: 'WIND'}   # values of the 'attr' field of cardprops.load
SPELL, TRAP = 13, 14
CARD = (213, 12, 26, 16)   # x, y, width, height of the icon on the 256x256 small cards (squashed: the icon is an ellipse), measured with the English


def replace_small_icons(sheet_png, dir_cards, cardinfo):
    """replaces the attribute icon on the small cards (id.png, ida.png...) of cards_dir, in place."""
    import re
    import cardprops
    cards = cardprops.load(cardinfo, corrected=False)
    sheet = Image.open(sheet_png).convert('RGBA')
    x0, y0, wi, hi = CARD
    icons = {n: sheet.crop((LARGE[n][0], LARGE[n][1], LARGE[n][0] + 62, LARGE[n][1] + 62)).resize((wi, hi), Image.LANCZOS) for n in ORDER}
    done = 0
    for f in sorted(os.listdir(dir_cards)):
        m = re.match(r'(\d+)', f)
        if not f.endswith('.png') or not m or int(m.group(1)) not in cards:
            continue
        c = cards[int(m.group(1))]
        name = 'SPELL' if c['kind'] == SPELL else 'TRAP' if c['kind'] == TRAP else ATTR_NAME.get(c['attr'])
        if not name:
            continue
        p = os.path.join(dir_cards, f)
        im = Image.open(p).convert('RGBA')
        im.alpha_composite(icons[name], (x0, y0))
        im.save(p)
        done += 1
    print('icons replaced on', done, 'cards in', dir_cards)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'table':
        language, pack, out = sys.argv[2:5]
        ehp = sys.argv[5] if len(sys.argv) > 5 else languages.current_ehp()
        build_table(language, pack, out, ehp)
    elif cmd == 'cards':
        replace_small_icons(sys.argv[2], sys.argv[3], sys.argv[4])   # SHEET_PNG CARDS_DIR CARDINFO.ehp
