"""Descrive, per UNA lingua, come e' fatto il texture pack: struttura (cartelle, numero di file, peso), ogni texture dell'interfaccia
(`ui_<l>`: hash, famiglia, script che la genera, archivio e membro della ISO da cui deriva, dimensione, neutra/specifica), le
immagini delle carte rigenerate per le correzioni dei testi, il banner del titolo e gli ini.
uso: python documenta_pack.py ISO_ORIGINALE LINGUA OUT_DIR       (it: il pack di base e' italiano; fr/de/es: PSP/TEXTURES/moduli/<l>)
Scrive: pack_struttura.csv, texture_ui.csv, carte_immagini.csv, ini_righe.csv, riepilogo_pack.json"""
import collections, csv, io, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'strumenti')); sys.path.insert(0, os.path.join(B, 'strumenti', 'correzioni'))
sys.stdout.reconfigure(encoding='utf-8')
import pycdlib, gim, applica_iso as ai
from PIL import Image

iso_p, L, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
T = os.path.join(B, 'PSP', 'TEXTURES')
BASE = os.path.join(T, 'ULES00600')
MOD = BASE if L == 'it' else os.path.join(T, 'moduli', L)
UI = f'ui_{L}'
SCRIPT = {'scritte_duello': 'scritte_duello.py', 'lettere_esito': 'lettere_esito.py', 'menu_liste': 'menu_liste.py', 'fogli_icone': 'fogli_icone.py',
          'schede_deck': 'schede_deck.py', 'schede_ricette': 'schede_ricette.py', 'schermata_vs': 'schermata_vs.py', 'tutorial': 'tutorial.py'}
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


def lingua(q, k):
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
        _, f = ai.apri(b.getvalue())
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
for i_, (root, nome) in enumerate(((BASE, 'ULES00600 (pack di base)'), (MOD, f'moduli/{L}'))):
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
            rows.append((nome, d + '/', n, round(sz / 1e6, 1), sub))
        else:
            rows.append((nome, d, 1, round(os.path.getsize(p) / 1e6, 2), ''))
with open(os.path.join(out, 'pack_struttura.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';'); w.writerow(['radice', 'cartella/file', 'file', 'MB', 'contenuto (primi)']); w.writerows(rows)

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
        L5 = sorted({lingua(q, k) for q, k in locs} - {'-'})
        kind = 'NEUTRA' if (('g' in L5 and 's' in L5) or len(L5) >= 4) else 'SPECIFICA'
        im = Image.open(os.path.join(dp, f))
        src = '; '.join(sorted({q.replace('/PSP_GAME/USRDIR/', '') + ':' + k for q, k in locs})[:3])
        ui_rows.append((rel, h, fam, SCRIPT.get(fam, '?'), size_low.get(h, ('?', '?')), f'{im.width}x{im.height}', kind, ''.join(L5), src))
        fam_count[fam] += 1
with open(os.path.join(out, 'texture_ui.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['file nel pack', 'hash PPSSPP (dati)', 'famiglia', 'script generatore (strumenti/ui_it/)', 'originale (px)', 'HD (px)', 'neutra/specifica',
                'lingue con lo stesso hash', 'origine nella ISO (archivio:membro)'])
    for r in sorted(ui_rows):
        w.writerow([r[0], r[1], r[2], r[3], f'{r[4][0]}x{r[4][1]}', r[5], r[6], r[7], r[8]])

# 3. carte rigenerate
dm = os.path.join(B, 'documentazione', f'modifiche_{L}', 'carte.csv')
ids = []
if os.path.exists(dm):
    ids = sorted({int(r[0]) for r in list(csv.reader(open(dm, encoding='utf-8-sig'), delimiter=';'))[1:]})
cart = []
for cid in ids:
    s = os.path.join(MOD, 'cards', f'small_{L}', f'{cid}.png'); lg = os.path.join(MOD, 'cards', f'large_{L}', f'{cid}.png')
    cart.append((cid, os.path.relpath(s, T).replace(os.sep, '/'), os.path.exists(s), os.path.relpath(lg, T).replace(os.sep, '/'), os.path.exists(lg)))
with open(os.path.join(out, 'carte_immagini.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';'); w.writerow(['id carta', 'piccola HD', 'esiste', 'grande HD (nome)', 'esiste']); w.writerows(cart)

# 4. righe degli ini
cnt = collections.Counter()
for l in open(ini, encoding='utf-8'):
    m = re.match(r'^[0-9a-f]{24}\s*=\s*(\S+)', l)
    if m:
        cnt[m.group(1).split('/')[0] + '/' + (m.group(1).split('/')[1] if '/' in m.group(1) else '')] += 1
with open(os.path.join(out, 'ini_righe.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';'); w.writerow([f'prefisso in {os.path.relpath(ini, T)}', 'righe']); w.writerows(sorted(cnt.items(), key=lambda x: -x[1])[:80])
banner = []
for dp, _, fs in os.walk(os.path.join(MOD, 'intro')):
    for f in fs:
        banner.append(os.path.relpath(os.path.join(dp, f), T).replace(os.sep, '/'))
cards = {d: len(os.listdir(os.path.join(MOD, 'cards', d))) for d in sorted(os.listdir(os.path.join(MOD, 'cards'))) if os.path.isdir(os.path.join(MOD, 'cards', d))} if os.path.isdir(os.path.join(MOD, 'cards')) else {}
riep = dict(lingua=L, texture_ui=len(ui_rows), per_famiglia=dict(fam_count), neutre=sum(1 for r in ui_rows if r[6] == 'NEUTRA'), specifiche=sum(1 for r in ui_rows if r[6] == 'SPECIFICA'),
            righe_ini_ui=len(mp), carte_corrette=len(ids), banner=banner, cartelle_carte=cards)
json.dump(riep, open(os.path.join(out, 'riepilogo_pack.json'), 'w', encoding='utf-8'), indent=1)
print(riep)
