"""Contact sheets of the inventory + visual search of English HD counterparts for the Italian text textures
whose English variant has no hash match in the pack (the US text may differ from the EU English one).
usage: sheets.py USRDIR PACK_DIR inventory.json OUTDIR"""
import json, os, re, sys, glob, collections
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, '/Users/admin/Desktop/tmp/TF1_HD_ITA/strumenti')
import numpy as np
from PIL import Image, ImageDraw
from ehp import read
import gim

U, P, inv, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
items = json.load(open(inv))
_cache = {}


def load_gim(use):
    f, m = use.split(':', 1)
    if f not in _cache:
        p = os.path.join(U, f)
        _cache.clear()
        _cache[f] = read(p) if p.endswith('.ehp') else {os.path.basename(p): open(p, 'rb').read()}
    return gim.to_png(gim.parse(_cache[f][m]))


def en_variant(v):
    f, m = v['uses'][0].split(':', 1)
    cands = [(re.sub(r'_i(\d*\.gim)$', r'_e\1', m), f), (m, re.sub(r'_i\.ehp$', '_e.ehp', f)),
             (m, f.replace('_ita.ehp', '_eng.ehp')), (m, re.sub(r'basic_ii', 'basic_ee', f))]
    for mm, ff in cands:
        if (mm, ff) == (m, f):
            continue
        try:
            return load_gim(ff + ':' + mm), ff + ':' + mm
        except Exception:
            pass
    return None, None


def cat(v):
    if v['covered']:
        return 'HD'
    if v['lang_specific'] and v['en_covered']:
        return 'A'
    return 'B' if v['lang_specific'] else 'C'


# pack PNGs, downscaled once per target size on demand
pack_files = [p for p in glob.glob(P + '/**/*.png', recursive=True) if '/cards/' not in p]
pack_small = {}


def pack_at(size):
    if size not in pack_small:
        res = []
        for p in pack_files:
            try:
                im = Image.open(p)
                if abs(im.width / im.height - size[0] / size[1]) > 0.02:
                    continue
                a = np.asarray(im.convert('RGBA').resize(size, Image.BOX), np.float32)
                res.append((p, a))
            except Exception:
                pass
        pack_small[size] = res
    return pack_small[size]


def corr(a, b):
    a = a[..., :3].mean(-1) * (a[..., 3] / 255); b = b[..., :3].mean(-1) * (b[..., 3] / 255)
    a = a - a.mean(); b = b - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))


report = []
for v in items:
    c = cat(v)
    if c not in ('A', 'B'):
        continue
    it = load_gim(v['uses'][0])
    en, en_use = en_variant(v)
    best = (None, -1)
    if c == 'B' and en is not None:
        a = np.asarray(en.convert('RGBA'), np.float32)
        for p, b in pack_at(en.size):
            s = corr(a, b)
            if s > best[1]:
                best = (p, s)
    hd = os.path.join(P, v['en_pack_file']) if c == 'A' else (best[0] if best[1] > 0.85 else None)
    report.append(dict(v, cat=c, it_img=it, en_img=en, en_use=en_use, hd=hd, match=best[1]))


def sheet(rows, name, T=240):
    H = T // 2 + 22
    im = Image.new('RGB', (3 * (T + 8), len(rows) * H + 4), (40, 40, 40))
    d = ImageDraw.Draw(im)
    for i, r in enumerate(rows):
        for k, (lab, src) in enumerate((('IT', r['it_img']), ('EN (gioco)', r['en_img']), ('HD pack', r['hd']))):
            if src is None:
                continue
            t = Image.open(src) if isinstance(src, str) else src
            bg = Image.new('RGBA', t.size, (60, 110, 110, 255)); bg.alpha_composite(t.convert('RGBA'))
            t = bg.convert('RGB'); t.thumbnail((T, T // 2))
            im.paste(t, (k * (T + 8), i * H + 20))
        d.text((2, i * H + 4), f"{r['file'].split('/')[-1]}:{r['member']} {r['w']}x{r['h']}"
               + (f"  match {r['match']:.2f}" if r['cat'] == 'B' else ''), fill=(255, 255, 0))
    im.save(os.path.join(out, name))


for c in ('A', 'B'):
    rows = sorted([r for r in report if r['cat'] == c], key=lambda r: (r['file'], r['member']))
    for k in range(0, len(rows), 18):
        sheet(rows[k:k + 18], f'{c}_{k // 18 + 1}.png')
    print(c, len(rows), 'con HD inglese trovato:', sum(1 for r in rows if r['hd']))
json.dump([{k: v for k, v in r.items() if not k.endswith('_img')} for r in report], open(os.path.join(out, 'ab.json'), 'w'), indent=1)
