"""Describes, for ONE language, how the texture pack is made: structure (folders, number of files, size), every interface texture
(`ui_<l>`: hash, family, script that generates it, ISO archive and member it derives from, size, neutral/specific), the
card images regenerated for the text corrections, the title banner and the inis.
usage: python document_pack.py ORIGINAL_ISO LANGUAGE OUT_DIR       (it: the base pack is Italian; fr/de/es: PSP/TEXTURES/modules/<l>)
Writes: pack_structure.csv, ui_textures.csv, card_images.csv, ini_lines.csv, pack_summary.json"""
import collections, csv, io, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'tools')); sys.path.insert(0, os.path.join(B, 'tools', 'corrections'))
sys.stdout.reconfigure(encoding='utf-8')
import pycdlib, gim, apply_to_iso as ai
from PIL import Image

iso_p, L, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
T = os.path.join(B, 'PSP', 'TEXTURES')
BASE = os.path.join(T, 'ULES00600')
MOD = BASE if L == 'it' else os.path.join(T, 'modules', L)
UI = f'ui_{L}'
SCRIPT = {'duel_texts': 'duel_texts.py', 'result_letters': 'result_letters.py', 'menu_lists': 'menu_lists.py', 'icon_sheets': 'icon_sheets.py',
          'deck_screens': 'deck_screens.py', 'recipe_screens': 'recipe_screens.py', 'vs_screen': 'vs_screen.py', 'tutorial': 'tutorial.py'}
I = pycdlib.PyCdlib(); I.open(iso_p)
idx = collections.defaultdict(list)


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


def language(q, k):
    m = re.search(r'_([efgis])(?:\d|\.gim)', k)
    if m:
        return m.group(1)
    a = os.path.basename(q)
    m = re.search(r'basic_[a-z]([efgis])\.ehp$', a) or re.search(r'_([efgis])\.ehp$', a)
    if m:
        return m.group(1)
    m = re.search(r'_(eng|fra|ger|ita|spa)\.ehp$', a)
    return {'eng': 'e', 'fra': 'f', 'ger': 'g', 'ita': 'i', 'spa': 's'}[m.group(1)] if m else '-'


size_low = {}
for q in walk('/PSP_GAME/USRDIR'):
    b = io.BytesIO(); I.get_file_from_iso_fp(b, iso_path=q)
    try:
        _, f = ai.open_ehp(b.getvalue())
    except Exception:
        continue
    for k in f:
        if k.endswith('.gim'):
            try:
                g = gim.parse(bytes(f[k])); h = gim.data_hash(g)
            except Exception:
                continue
            idx[h].append((q, k))
            if h not in size_low:
                try:
                    size_low[h] = gim.to_png(g).size
                except Exception:
                    size_low[h] = (0, 0)

# 1. struttura
rows = []
for i_, (root, name) in enumerate(((BASE, 'ULES00600 (pack di base)'), (MOD, f'moduli/{L}'))):
    if i_ == 1 and L == 'it':
        continue
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d)
        if os.path.isdir(p):
            n = sz = 0
            for dp, _, fs in os.walk(p):
                for f in fs:
                    n += 1; sz += os.path.getsize(os.path.join(dp, f))
            sub = ', '.join(sorted(os.listdir(p))[:10]) + (' ...' if len(os.listdir(p)) > 10 else '')
            rows.append((name, d + '/', n, round(sz / 1e6, 1), sub))
        else:
            rows.append((name, d, 1, round(os.path.getsize(p) / 1e6, 2), ''))
with open(os.path.join(out, 'pack_structure.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';'); w.writerow(['radice', 'folder/file', 'file', 'MB', 'contenuto (primi)']); w.writerows(rows)

# 2. texture ui
ini = os.path.join(BASE, 'textures.ini') if L == 'it' else os.path.join(MOD, f'{L}.ini')
mp = {}
for l in open(ini, encoding='utf-8'):
    m = re.match(r'^[0-9a-f]{16}([0-9a-f]{8})\s*=\s*(' + UI + r'/\S+)', l)
    if m:
        mp[m.group(2)] = m.group(1)
ui_rows, fam_count = [], collections.Counter()
root = os.path.join(MOD, UI)
for dp, _, fs in os.walk(root):
    for f in sorted(fs):
        if not f.endswith('.png'):
            continue
        rel = UI + '/' + os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/')
        fam = rel.split('/')[1]
        h = mp.get(rel, '?')
        locs = idx.get(h, [])
        L5 = sorted({language(q, k) for q, k in locs} - {'-'})
        kind = 'NEUTRAL' if (('g' in L5 and 's' in L5) or len(L5) >= 4) else 'SPECIFIC'
        im = Image.open(os.path.join(dp, f))
        src = '; '.join(sorted({q.replace('/PSP_GAME/USRDIR/', '') + ':' + k for q, k in locs})[:3])
        ui_rows.append((rel, h, fam, SCRIPT.get(fam, '?'), size_low.get(h, ('?', '?')), f'{im.width}x{im.height}', kind, ''.join(L5), src))
        fam_count[fam] += 1
with open(os.path.join(out, 'ui_textures.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['file nel pack', 'hash PPSSPP (dati)', 'famiglia', 'script generatore (tools/ui_textures/)', 'original (px)', 'HD (px)', 'neutra/specifica',
                'languages with the same hash', 'origin in the ISO (archive:member)'])
    for r in sorted(ui_rows):
        w.writerow([r[0], r[1], r[2], r[3], f'{r[4][0]}x{r[4][1]}', r[5], r[6], r[7], r[8]])

# 3. regenerated cards
dm = os.path.join(B, 'docs', f'changes_{L}', 'cards.csv')
ids = []
if os.path.exists(dm):
    ids = sorted({int(r[0]) for r in list(csv.reader(open(dm, encoding='utf-8-sig'), delimiter=';'))[1:]})
folder = []
for cid in ids:
    s = os.path.join(MOD, 'cards', f'small_{L}', f'{cid}.png'); lg = os.path.join(MOD, 'cards', f'large_{L}', f'{cid}.png')
    folder.append((cid, os.path.relpath(s, T).replace(os.sep, '/'), os.path.exists(s), os.path.relpath(lg, T).replace(os.sep, '/'), os.path.exists(lg)))
with open(os.path.join(out, 'card_images.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';'); w.writerow(['id carta', 'piccola HD', 'esiste', 'grande HD (nome)', 'esiste']); w.writerows(folder)

# 4. ini lines
cnt = collections.Counter()
for l in open(ini, encoding='utf-8'):
    m = re.match(r'^[0-9a-f]{24}\s*=\s*(\S+)', l)
    if m:
        cnt[m.group(1).split('/')[0] + '/' + (m.group(1).split('/')[1] if '/' in m.group(1) else '')] += 1
with open(os.path.join(out, 'ini_lines.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';'); w.writerow([f'prefisso in {os.path.relpath(ini, T)}', 'righe']); w.writerows(sorted(cnt.items(), key=lambda x: -x[1])[:80])
banner = []
for dp, _, fs in os.walk(os.path.join(MOD, 'intro')):
    for f in fs:
        banner.append(os.path.relpath(os.path.join(dp, f), T).replace(os.sep, '/'))
cards = {d: len(os.listdir(os.path.join(MOD, 'cards', d))) for d in sorted(os.listdir(os.path.join(MOD, 'cards'))) if os.path.isdir(os.path.join(MOD, 'cards', d))} if os.path.isdir(os.path.join(MOD, 'cards')) else {}
summary = dict(language=L, texture_ui=len(ui_rows), per_family=dict(fam_count), neutral=sum(1 for r in ui_rows if r[6] == 'NEUTRAL'), specific=sum(1 for r in ui_rows if r[6] == 'SPECIFIC'),
            rows_ini_ui=len(mp), cards_corrected=len(ids), banner=banner, folders_cards=cards)
json.dump(summary, open(os.path.join(out, 'pack_summary.json'), 'w', encoding='utf-8'), indent=1)
print(summary)
