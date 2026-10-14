"""Comparison sheets for reading by eye the texts drawn in the textures: for every texture of `ui_<L>` puts on the left the ORIGINAL
of the ISO (low resolution, enlarged without smoothing) and on the right the pack's HD PNG, with the file name and the origin (archive:member).
Then the sheets are looked at and the text is transcribed into `docs/changes_<l>/texture_texts_<l>.md` (see docs/NEW_LANGUAGE_GUIDE.md sec. 10).
usage: python texture_comparison_sheets.py ORIGINAL_ISO LANGUAGE OUT_DIR      -> OUT_DIR/<family>_<n>.png (6 textures per sheet)
(it: base pack PSP/TEXTURES/ULES00600; other languages: PSP/TEXTURES/modules/<l>)"""
import collections, io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'tools')); sys.path.insert(0, os.path.join(B, 'tools', 'corrections'))
import pycdlib, gim, apply_to_iso as ai
from PIL import Image, ImageDraw

iso, L, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
LET = {'it': 'i', 'fr': 'f', 'de': 'g', 'es': 's', 'en': 'e'}[L]
I = pycdlib.PyCdlib(); I.open(iso)
idx = collections.defaultdict(list); gims = {}


def walk(p):
    for ch in I.list_children(iso_path=p):
        n = ch.file_identifier().decode().split(';')[0]
        if n in ('.', '..'):
            continue
        q = p.rstrip('/') + '/' + n
        if ch.is_dir():
            yield from walk(q)
        elif n.endswith('.ehp'):
            yield q


for q in walk('/PSP_GAME/USRDIR'):
    b = io.BytesIO(); I.get_file_from_iso_fp(b, iso_path=q)
    try:
        _, f = ai.open_ehp(b.getvalue())
    except Exception:
        continue
    for k in f:
        if k.endswith('.gim'):
            try:
                g = gim.parse(bytes(f[k])); idx[gim.data_hash(g)].append((q, k, g))
            except Exception:
                pass

ui = 'ui_' + L
root = os.path.join(B, 'PSP', 'TEXTURES', 'ULES00600' if L == 'it' else os.path.join('modules', L))
ini = os.path.join(root, 'textures.ini' if L == 'it' else f'{L}.ini')
mp = {}
for l in open(ini, encoding='utf-8'):
    m = re.match(r'^[0-9a-f]{16}([0-9a-f]{8})\s*=\s*(' + ui + r'/\S+\.png)', l)
    if m:
        mp[m.group(2)] = m.group(1)
fams = collections.defaultdict(list)
for rel, h in sorted(mp.items()):
    fams[rel.split('/')[1]].append((rel, h))
W = 560
for fam, items in fams.items():
    for part in range(0, len(items), 6):
        ims = []
        for rel, h in items[part:part + 6]:
            locs = sorted(idx[h], key=lambda x: (f'_{LET}' not in x[0] + x[1],))
            q, k, g = locs[0]
            o = gim.to_png(g).convert('RGBA')
            hd = Image.open(os.path.join(root, *rel.split('/'))).convert('RGBA')
            s = min(4, W / o.width)
            o2 = o.resize((max(1, int(o.width * s)), max(1, int(o.height * s))), Image.NEAREST)
            s2 = W / hd.width if hd.width > W else 1
            hd2 = hd.resize((int(hd.width * s2), int(hd.height * s2)), Image.LANCZOS)
            ims.append((rel, q.split('/')[-1] + ':' + k, o2, hd2))
        H = sum(max(a.height, b.height) + 22 for _, _, a, b in ims)
        sh = Image.new('RGB', (2 * W + 20, H), (70, 70, 80)); d = ImageDraw.Draw(sh); y = 0
        for rel, src, a, b in ims:
            d.text((2, y), rel.split('/', 2)[2] + '   [orig ' + src + ']', fill=(255, 255, 0))
            for x0, im in ((0, a), (W + 20, b)):
                bg = Image.new('RGBA', (W, max(a.height, b.height)), (110, 110, 120, 255)); bg.alpha_composite(im, (0, 0))
                sh.paste(bg.convert('RGB'), (x0, y + 16))
            y += max(a.height, b.height) + 22
        sh.save(os.path.join(out, f'{fam}_{part // 6}.png'))
        print(f'{fam}_{part // 6}', sh.size)
