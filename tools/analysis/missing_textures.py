"""Lists the textures redrawn in OTHER languages (ui_<l> of fr/es/de, ui_it of the base pack) that in the chosen language have their own text
(hash different from English) but are not yet in the language's module: those are the ones missing.

Why it is needed: "same hash as English" must be checked on the language's real archive (duel/basic_b<l>.ehp, result_<l>.ehp...), not by eye:
for German the tiles of DU GEWINNST / Ketten / NÄCHSTER SPIELER had been taken for English and were not.

usage: python missing_textures.py USRDIR LANGUAGE        LANGUAGE = fr|de|es
For every reference texture (same normalized archive/member key from textures_per_language.per_language) it prints:
  MANCA        language hash different from English and absent from the module -> to be redrawn
  for all the other categories only the count is printed (ok = already in the module, =ing = neutral)."""
import collections, glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'tools')); sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding='utf-8')
from ehp import read
import gim
import textures_per_language as T

usr, L = sys.argv[1:3]
tab = {}
for p in glob.glob(os.path.join(usr, '**', '*.ehp'), recursive=True):
    rel = os.path.relpath(p, usr).replace(chr(92), '/')
    try:
        a = read(p)
    except Exception:
        continue
    for k, v in a.items():
        if not k.endswith('.gim'):
            continue
        try:
            h = gim.data_hash(gim.parse(v))
        except Exception:
            continue
        for c, letter in T.LET.items():
            an, mn = T.per_language(rel, letter, T.LET3[c]), T.per_language(k, letter, T.LET3[c])
            if an is not None or mn is not None:
                tab.setdefault((an or rel, mn or k), {})[letter] = (h, rel, k)


def ini(files):
    t = {}
    for f in files:
        for r in open(f, encoding='utf8'):
            m = re.match(r'^0*([0-9a-f]{8})\s*=\s*(\S+)', r.strip())
            if m:
                t[m.group(1)] = m.group(2)
    return t


PT = os.path.join(B, 'PSP', 'TEXTURES')
mine = ini([os.path.join(PT, 'modules', L, L + '.ini')])
refs = {'f': ini([os.path.join(PT, 'modules', 'fr', 'fr.ini')]), 's': ini([os.path.join(PT, 'modules', 'es', 'es.ini')]),
        'g': ini([os.path.join(PT, 'modules', 'de', 'de.ini')]),
        'i': ini(glob.glob(os.path.join(PT, 'ULES00600', 'ui_it', '*.ini')))}
me = T.LET[L]
cont = collections.Counter()
for key, d in sorted(tab.items()):
    if me not in d:
        continue
    for ref in 'fsgi':
        if ref != me and ref in d and d[ref][0] in refs[ref] and 'ui_' in refs[ref][d[ref][0]]:
            h, e = d[me][0], d.get('e', (None,))[0]
            cat = '=ing' if h == e else ('ok' if h in mine else 'MANCA')
            cont[cat] += 1
            if cat == 'MANCA':
                print(ref, key, h)
            break
print(dict(cont))
