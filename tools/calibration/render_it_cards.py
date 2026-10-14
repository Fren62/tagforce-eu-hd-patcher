"""Render complete Italian small cards with candidate description styles and build a comparison sheet:
for each card id: English HD original | Italian with the CURRENT style | Italian with each candidate (x3 zoom of the
lower half of the card, where the description is).
usage: render_it_cards.py OUT.png "effect=FIT.json,st=FIT.json,normal=FIT.json" [ "..." ...] -- ID [ID ...]
       (a kind left out keeps the current style; FIT.json from fit_descfont.py)"""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import alt_font  # noqa: nessun font Apple
import json, os, re, sys
O = '/private/tmp/claude-502/-Users-admin-Desktop-tmp/6f120653-f98e-4c52-ac72-7928833fda52/scratchpad'
sys.argv = [sys.argv[0], O + '/tools'] + sys.argv[1:]
sys.path.insert(0, O + '/tools')
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import small_it as S
from cardprops import load
from smallbg import frame_of

out = sys.argv[2]
k = sys.argv.index('--')
sets, ids = sys.argv[3:k], [int(x) for x in sys.argv[k + 1:]]
CARDS = O + '/mikey_x/ULUS10136/cards/small'
IT = load(O + '/ex/PSP_GAME/USRDIR/duelsys/cardinfo_ita.ehp')
EN = {int(a): b.strip() for a, b in re.findall(r'^#(\d{4}):\s*(.*)$', open(O + '/mikey_x/ULUS10136/textures.ini', encoding='utf-8').read(), re.M)}
CUR = {k: dict(v) for k, v in S.DESC.items()}


def styles_of(spec):
    d = {k: dict(v) for k, v in CUR.items()}
    names = []
    for part in [p for p in spec.split(',') if p]:
        kind, f = part.split('=')
        j = json.load(open(f))
        st = j['style']; st['font'] = tuple(j['font'])
        d[kind] = st
        names.append(f"{kind}: {j['name']}")
    return d, ' / '.join(names) or 'attuale'


def render(cid, styles):
    S.DESC.clear(); S.DESC.update(styles)
    g = frame_of(IT[cid])
    clean = np.asarray(Image.open(f'{O}/smallbg/clean_{g}.png').convert('RGB')).astype(np.int32)
    tmp = f'{O}/peek/_rit_{os.getpid()}.png'
    S.localize(f'{CARDS}/{cid}.png', tmp, IT[cid], EN.get(cid), clean)
    return Image.open(tmp).convert('RGB')


cols = [('inglese (mod)', None), ('italiano attuale', CUR)] + [(n, d) for d, n in (styles_of(s) for s in sets)]
Z = 3
box = (14, 184, 242, 246)
W, H = (box[2] - box[0]) * Z, (box[3] - box[1]) * Z
lab = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 16)
sheet = Image.new('RGB', (len(cols) * (W + 8), len(ids) * (H + 24)), (30, 30, 30))
d = ImageDraw.Draw(sheet)
for r, cid in enumerate(ids):
    for c, (name, st) in enumerate(cols):
        im = Image.open(f'{CARDS}/{cid}.png').convert('RGB') if st is None else render(cid, st)
        X, Y = c * (W + 8), r * (H + 24) + 20
        sheet.paste(im.crop(box).resize((W, H), Image.NEAREST), (X, Y))
        d.text((X + 2, Y - 19), f'{cid} {name}', font=lab, fill=(255, 215, 0) if c > 1 else (255, 255, 255))
sheet.save(out)
print(out, sheet.size)
