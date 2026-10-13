"""Elenca le texture ridisegnate in ALTRE lingue (ui_<l> di fr/es/de, ui_it del pack di base) che nella lingua scelta hanno un testo proprio
(hash diverso dall'inglese) ma non sono ancora nel modulo della lingua: sono quelle che mancano.

Perche' serve: "stesso hash dell'inglese" va verificato sull'archivio vero della lingua (duel/basic_b<l>.ehp, result_<l>.ehp...), non a occhio:
per il tedesco le tessere di DU GEWINNST / Ketten / NÄCHSTER SPIELER erano state date per inglesi e non lo erano.

uso: python texture_mancanti.py USRDIR LINGUA        LINGUA = fr|de|es
Per ogni texture di riferimento (stessa chiave archivio/membro normalizzata da textures_per_lingua.per_lingua) stampa:
  MANCA        hash della lingua diverso dall'inglese e assente dal modulo -> da ridisegnare
  di tutte le altre categorie stampa solo il conteggio (ok = gia' nel modulo, =ing = neutra)."""
import collections, glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'strumenti')); sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding='utf-8')
from ehp import read
import gim
import textures_per_lingua as T

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
        for c, lett in T.LET.items():
            an, mn = T.per_lingua(rel, lett, T.LET3[c]), T.per_lingua(k, lett, T.LET3[c])
            if an is not None or mn is not None:
                tab.setdefault((an or rel, mn or k), {})[lett] = (h, rel, k)


def ini(files):
    t = {}
    for f in files:
        for r in open(f, encoding='utf8'):
            m = re.match(r'^0*([0-9a-f]{8})\s*=\s*(\S+)', r.strip())
            if m:
                t[m.group(1)] = m.group(2)
    return t


PT = os.path.join(B, 'PSP', 'TEXTURES')
mine = ini([os.path.join(PT, 'moduli', L, L + '.ini')])
refs = {'f': ini([os.path.join(PT, 'moduli', 'fr', 'fr.ini')]), 's': ini([os.path.join(PT, 'moduli', 'es', 'es.ini')]),
        'g': ini([os.path.join(PT, 'moduli', 'de', 'de.ini')]),
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
