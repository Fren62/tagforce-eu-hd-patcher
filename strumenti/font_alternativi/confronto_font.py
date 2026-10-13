"""Fogli di confronto per i font liberi: originale inglese HD | mod vecchia | mod nuova (font liberi), per tipo di carta.
Rigenera le carte scelte in una cartella temporanea (non tocca il pack) e scrive i PNG in confronti/font_liberi/.
usage: confronto_font.py ROOT TEMPDIR     (ROOT = cartella del progetto; TEMPDIR contiene ci/ e clean/)"""
import os, re, sys, json, shutil, subprocess, collections
ROOT, TMP = sys.argv[1], sys.argv[2]
T = f'{ROOT}/strumenti'
PACK = f'{ROOT}/PSP/TEXTURES/ULES00600'
OLD = f'{ROOT}/confronti/audit_carte/prima_delle_correzioni'
OUT = f'{ROOT}/confronti/font_liberi'
sys.path.insert(0, T)
from cardprops import load
from PIL import Image, ImageDraw
from banner import extract   # carte grandi: confronto sul banner del nome (320x48)

cards = load(f'{TMP}/ci/cardinfo_ita.ehp')
corr = {int(k) for k in json.load(open(f'{T}/dati/correzioni_carte.json', encoding='utf-8'))}
have = {int(f[:-4]) for f in os.listdir(f'{PACK}/cards/small') if re.fullmatch(r'\d+\.png', f)}
NAMES = {0: 'Normali', 1: 'Effetto', 2: 'Fusione', 3: 'Fusione-Effetto', 4: 'Rituale', 5: 'Rituale-Effetto', 6: 'Toon',
         7: 'Spirito', 8: 'Unione', 9: 'Token'}
groups = collections.defaultdict(list)
for i, c in cards.items():
    if i in have:
        k = c['kind']
        groups[(NAMES[k] if k < 10 else ('Magia' if k == 13 else 'Trappola') + ('-icona' if c['icon'] else '-semplice'))].append(i)


def pick(ids):
    d = lambda i: len(cards[i]['desc'])
    s = {max(ids, key=d), min(ids, key=d), max(ids, key=lambda i: len(cards[i]['name']))}
    s |= {i for i in ids if '●' in cards[i]['desc']} and {sorted(i for i in ids if '●' in cards[i]['desc'])[0]}
    s |= set(sorted(i for i in ids if i in corr)[:2])
    return sorted(s)


sel = {g: pick(v) for g, v in sorted(groups.items())}
ids = sorted({i for v in sel.values() for i in v})
print(len(ids), 'carte:', {g: len(v) for g, v in sel.items()})

# mini pack temporaneo: copia le carte inglesi, rigenera con i font liberi
P = f'{TMP}/prova'
shutil.rmtree(P, ignore_errors=True)
for sub in ('small', 'large'):
    os.makedirs(f'{P}/cards/{sub}')
    for i in ids:
        shutil.copy(f'{PACK}/cards/{sub}/{i}.png', f'{P}/cards/{sub}/{i}.png')
env = dict(os.environ, PYTHONIOENCODING='utf-8')
sh = lambda *a, **k: subprocess.run([sys.executable, *a], check=True, env=k.get('env', env))
ini = f'{PACK}/textures.ini'
sh(f'{T}/small_it.py', T, P, f'{TMP}/ci/cardinfo_ita.ehp', ini, f'{TMP}/clean', *map(str, ids))
sh(f'{T}/gen_large_it.py', T, P, f'{TMP}/ci/cardinfo_ita.ehp', env=dict(env, TF1_IDS=' '.join(map(str, ids))))

# fogli
os.makedirs(OUT, exist_ok=True)


def get(i, kind):
    for p in (f'{OLD}/{kind}_it/{i}.png', f'{PACK}/cards/{kind}_it/{i}.png'):
        if os.path.exists(p):
            return Image.open(p).convert('RGBA')


def sheet(kind, scale):
    for g, v in sel.items():
        cols = [('originale inglese', lambda i: Image.open(f'{PACK}/cards/{kind}/{i}.png').convert('RGBA')),
                ('mod vecchia', lambda i: get(i, kind)),
                ('mod nuova (font liberi)', lambda i: Image.open(f'{P}/cards/{kind}_it/{i}.png').convert('RGBA'))]
        w, h = (320, 48) if kind == 'large' else Image.open(f'{PACK}/cards/{kind}/{v[0]}.png').size
        w, h = int(w * scale), int(h * scale)
        im = Image.new('RGB', (len(cols) * w, 20 + len(v) * (h + 16)), (60, 60, 60))
        d = ImageDraw.Draw(im)
        for c, (title, _) in enumerate(cols):
            d.text((c * w + 5, 4), title, fill=(255, 255, 0))
        for r, i in enumerate(v):
            y = 20 + r * (h + 16)
            d.text((5, y), f'{i} {cards[i]["name"]}{" [corretta]" if i in corr else ""}', fill=(255, 255, 255))
            for c, (_, f) in enumerate(cols):
                a = f(i)
                if kind == 'large':
                    a = extract(a)
                a = a.resize((w, h), Image.LANCZOS)
                bg = Image.new('RGBA', a.size, (60, 60, 60, 255)); bg.alpha_composite(a)
                im.paste(bg.convert('RGB'), (c * w, y + 14))
        im.save(f'{OUT}/{kind}_{g}.png')


sheet('small', 1.0)
sheet('large', 1.5)
print('fogli in', OUT)
