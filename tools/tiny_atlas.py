"""Deck thumbnail atlases (cards/tinyMikeyMK/<a>_<b>.png, 2048x2048): each page is a 23x17 grid of 88x120 cells
with one vertical card each (on the first page the first cell is the card back). The pages have the same hash in all
languages, so without this work the Italian/French/... game would show the English names. Here every page is rebuilt
with the HD small cards of the language (cards/small_<l>): each cell is the resized small card.
The pages do not contain all the cards of their range: the cell -> card association is derived by comparing the English
images (analyze) and saved in data/tiny_atlas.json.
usage: tiny_atlas.py analyze PACK            associates every cell with its card (comparison with cards/small)
       tiny_atlas.py generate LANGUAGE PACK OUT   writes OUT/cards/tiny_<language>/<page>.png   (uses OUT/cards/small_<language>)"""
import glob, json, os, re, sys
import numpy as np
from PIL import Image

CW, CH, COLS, ROWS = 88, 120, 23, 17
HERE = os.path.dirname(os.path.abspath(__file__))
JSON = os.path.join(HERE, 'data', 'tiny_atlas.json')


def ncc(a, b):
    a = a - a.mean(); b = b - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))


def pages(pack, style='tinyMikeyMK'):
    out = []
    for f in sorted(glob.glob(os.path.join(pack, 'cards', style, '*.png'))):
        m = re.match(r'(\d+)_(\d+)\.png$', os.path.basename(f))
        if m:
            out.append((int(m.group(1)), int(m.group(2)), f))
    return out


def ids_existing(pack):
    return sorted({int(re.match(r'\d+', f).group()) for f in os.listdir(os.path.join(pack, 'cards', 'small')) if re.fullmatch(r'\d+\.png', f)})


def rect(idx):
    return (idx % COLS) * CW, (idx // COLS) * CH


def analyze(pack):
    all = ids_existing(pack)
    cache = {}

    def model(cid):
        if cid not in cache:
            cache[cid] = np.asarray(Image.open(os.path.join(pack, 'cards/small', f'{cid}.png')).convert('RGB').resize((CW, CH), Image.LANCZOS)).astype(np.float32)
        return cache[cid]

    res = {}
    for a, b, f in pages(pack):
        ids = [i for i in all if a <= i <= b]
        atlas = np.asarray(Image.open(f).convert('RGB')).astype(np.float32)
        p, cells, doubtful = 0, [], 0
        for idx in range(COLS * ROWS):
            x0, y0 = rect(idx)
            reg = atlas[y0:y0 + CH, x0:x0 + CW]
            if p >= len(ids):
                cells.append(0); continue
            scores = [(ncc(reg, model(ids[q])), q) for q in range(p, min(p + 8, len(ids)))]
            s, q = next(((s, q) for s, q in scores if s > 0.9), (None, None))
            if q is None:
                s, q = max(scores)
                if s < 0.6:   # card back or unrecognized cell (e.g. other art): does not consume cards
                    if idx == 0 and a == 4007:
                        cells.append(0); continue
                    q, doubtful = p, doubtful + 1
            cells.append(ids[q])
            p = q + 1
        res[os.path.basename(f)] = cells
        used = sum(1 for c in cells if c)
        print(os.path.basename(f), 'cards in the range', len(ids), 'cells assigned', used, 'unrecognized (assigned in order)', doubtful, flush=True)
    return res


def generate(language, pack, out):
    geo = json.load(open(JSON))
    dst = os.path.join(out, 'cards', f'tiny_{language}')
    os.makedirs(dst, exist_ok=True)
    for a, b, f in pages(pack):
        atlas = Image.open(f).convert('RGBA')
        n = 0
        for idx, cid in enumerate(geo[os.path.basename(f)]):
            if not cid:
                continue
            sm = os.path.join(out, 'cards', f'small_{language}', f'{cid}.png')
            if not os.path.exists(sm):
                sm = os.path.join(pack, 'cards', f'small_{language}', f'{cid}.png')
            if not os.path.exists(sm):
                continue
            atlas.paste(Image.open(sm).convert('RGBA').resize((CW, CH), Image.LANCZOS), rect(idx))
            n += 1
        atlas.save(os.path.join(dst, os.path.basename(f)))
        print(os.path.basename(f), n, 'celle', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'analyze':
        json.dump(analyze(sys.argv[2]), open(JSON, 'w'))
    else:
        generate(sys.argv[2], sys.argv[3], sys.argv[4])
