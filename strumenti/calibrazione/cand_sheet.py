"""One sheet per candidate description style, for visual judging (x3 zoom of the description box):
 rows A: English HD original | candidate drawing the SAME English text (fidelity, apples to apples)
 rows B: English HD original | candidate drawing the Italian text on the full Italian card
usage: cand_sheet.py KIND FIT.json|current OUT.png ID_A1,ID_A2,.. ID_B1,ID_B2,.."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import font_alt  # noqa: nessun font Apple
import json, os, re, sys
O = '/private/tmp/claude-502/-Users-admin-Desktop-tmp/6f120653-f98e-4c52-ac72-7928833fda52/scratchpad'
kind, fit, out, ida, idb = sys.argv[1:6]
sys.argv = [sys.argv[0], O + '/tools']
sys.path.insert(0, O + '/tools')
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import small_it as S
from cardprops import load
from smallbg import frame_of
from deschar import Bench

CARDS = O + '/mikey_x/ULUS10136/cards'
IT = load(O + '/ex/PSP_GAME/USRDIR/duelsys/cardinfo_ita.ehp')
EN = {int(a): b.strip() for a, b in re.findall(r'^#(\d{4}):\s*(.*)$', open(O + '/mikey_x/ULUS10136/textures.ini', encoding='utf-8').read(), re.M)}
if fit == 'current':
    style, name = dict(S.DESC[kind]), 'attuale'
else:
    j = json.load(open(fit))
    style = j['style']; style['font'] = tuple(j['font']); name = j['name']
bench = Bench(CARDS, O + '/smallbg', O + '/ex/PSP_GAME/USRDIR/duelsys/cardinfo_eng.ehp', kind, n=3)


def italian(cid):
    S.DESC[kind] = style
    g = frame_of(IT[cid])
    clean = np.asarray(Image.open(f'{O}/smallbg/clean_{g}.png').convert('RGB')).astype(np.int32)
    tmp = f'{O}/peek/_cs_{os.getpid()}.png'
    S.localize(f'{CARDS}/small/{cid}.png', tmp, IT[cid], EN.get(cid), clean)
    return np.asarray(Image.open(tmp).convert('RGB'))


rows = []
for cid in [int(x) for x in ida.split(',') if x]:
    img = bench.load(cid)
    rows.append((f'{cid} inglese (mod)', img, f'{cid} {name}: stesso testo inglese', bench.render(cid, img, style)))
for cid in [int(x) for x in idb.split(',') if x]:
    rows.append((f'{cid} inglese (mod)', bench.load(cid), f'{cid} {name}: testo italiano', italian(cid)))
Z = 3
box = (14, 184, 242, 246)
W, H = (box[2] - box[0]) * Z, (box[3] - box[1]) * Z
lab = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 16)
sheet = Image.new('RGB', (2 * W + 8, len(rows) * (H + 24)), (30, 30, 30))
d = ImageDraw.Draw(sheet)
for r, (la, a, lb, b) in enumerate(rows):
    for c, (lab_, im) in enumerate(((la, a), (lb, b))):
        X, Y = c * (W + 8), r * (H + 24) + 20
        sheet.paste(Image.fromarray(im).crop(box).resize((W, H), Image.NEAREST), (X, Y))
        d.text((X + 2, Y - 19), lab_, font=lab, fill=(255, 215, 0) if c else (255, 255, 255))
sheet.save(out)
print(out, sheet.size)
