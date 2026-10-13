import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); import font_alt  # noqa: nessun font Apple
import sys, json, os, re, glob
from PIL import Image, ImageDraw, ImageFont
R, W, OUT = sys.argv[1:4]
man = {e['id']: e for e in json.load(open(W + '/ui/manifest.json'))}
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 14)
TEAL = (0, 110, 110, 255)
def tile(im, w):
    bg = Image.new('RGBA', im.size, TEAL); bg.alpha_composite(im.convert('RGBA'))
    s = min(1.0, w / im.width)
    return bg.convert('RGB').resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS if s < 1 else Image.NEAREST), s
for ini in sorted(glob.glob(R + '/ui_it/*.ini')):
    fam = os.path.basename(ini)[:-4]
    ids = [re.search(r'/([^/]+)\.png', l).group(1) for l in open(ini) if ' = ' in l]
    blocks = []
    for tid in ids:
        e = man[tid]
        hd = Image.open(f'{R}/ui_it/{fam}/{tid}.png').convert('RGBA')
        w = 640 if len(ids) < 12 else 300
        if hd.width <= 256: w = hd.width
        it = Image.open(e['dir'] + '/it.png').convert('RGBA').resize(hd.size, Image.NEAREST)
        cols = [('IT', it), ('nuovo', hd)]
        if os.path.exists(e['dir'] + '/en.png') and e['group'] != 1 or (os.path.exists(e['dir'] + '/hd.png') and e.get('hd')):
            p = e['dir'] + '/hd.png' if os.path.exists(e['dir'] + '/hd.png') else None
            if p:
                ref = Image.open(p).convert('RGBA')
                if ref.width >= it.width // 2: cols.append(('HD mod', ref.resize(hd.size, Image.LANCZOS) if ref.size != hd.size else ref))
        ts = [(n, tile(im, w)[0]) for n, im in cols]
        blocks.append((tid, ts))
    # flow layout
    maxw = 2400; x = y = 0; rowh = 0; placed = []
    for tid, ts in blocks:
        bw = sum(t.width for _, t in ts) + 4 * (len(ts) - 1); bh = max(t.height for _, t in ts) + 18
        if x + bw > maxw and x > 0: x = 0; y += rowh + 10; rowh = 0
        placed.append((x, y, tid, ts)); x += bw + 14; rowh = max(rowh, bh)
    H = y + rowh + 6; Wd = max(px + sum(t.width for _, t in ts) + 4 * (len(ts) - 1) for px, py, _, ts in placed)
    sheet = Image.new('RGB', (Wd, H), (30, 30, 30)); d = ImageDraw.Draw(sheet)
    for px, py, tid, ts in placed:
        d.text((px, py), tid.split('__')[-1][:34], font=font, fill=(255, 215, 0)); cx = px
        for n, t in ts:
            sheet.paste(t, (cx, py + 16)); cx += t.width + 4
    sheet.save(f'{OUT}/{fam}.png'); print(fam, len(ids), sheet.size)
