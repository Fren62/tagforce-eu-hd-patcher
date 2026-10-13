"""Inventario delle texture con testo dell'inglese europeo (archivi *_e / *_eng / basic_?e): per ognuna dice se il pack di base
la copre (e con quale file) o se manca, e se in quel caso la stessa texture ha un'altra versione nel gioco (hash diverso nelle altre lingue).

Serve per decidere cosa ridisegnare in `moduli/en/ui_en`: il pack di MikeyMK e' fatto sul gioco USA; l'inglese europeo ha quasi sempre
gli stessi pixel (stesso hash) e quindi e' gia' coperto, ma alcune texture differiscono (es. foglio dei numeri del duello, pillola "Single").
Attenzione al caso opposto: una texture dell'italiano ridisegnata in `ui_it` il cui hash e' IDENTICO a quello inglese (testo non tradotto
dal gioco) farebbe comparire l'italiano nel gioco inglese: viene segnalata come ITA-SU-ING.

usage: python inventario_texture_en.py USRDIR [BASE_INI]
Scrive una tabella `archivio | membro | hash | dimensioni | esito | file del pack | lingue con lo stesso hash` su stdout."""
import glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'strumenti')); sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding='utf-8')
from ehp import read
import gim
import textures_per_lingua as T

usr = sys.argv[1]
ini_base = sys.argv[2] if len(sys.argv) > 2 else os.path.join(B, 'PSP', 'TEXTURES', 'ULES00600', 'textures.ini')
pack = {}
for r in open(ini_base, encoding='utf-8', errors='ignore'):
    m = re.match(r'^[0-9a-f]{16}([0-9a-f]{8})\s*=\s*(\S+)', r.strip())      # chiave a 24 cifre: (CLUT 8 cifre) + hash dei dati (ultime 8)
    if m:
        pack.setdefault(m.group(1), m.group(2))
tab = {}
tutte = {}
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
            g = gim.parse(v)
            h = gim.data_hash(g)
        except Exception:
            continue
        marcatori = {c: T.per_lingua(k, lett, T.LET3[c]) is not None for c, lett in T.LET.items()}
        for c, lett in T.LET.items():
            an, mn = T.per_lingua(rel, lett, T.LET3[c]), T.per_lingua(k, lett, T.LET3[c])
            if an is not None or mn is not None:
                if any(marcatori.values()) and mn is None:
                    continue      # il membro porta il segno di un'altra lingua (es. un archivio start_e che contiene anche le varianti _i): non e' di questa lingua
                tab.setdefault((an or rel, mn or k), {})[lett] = (h, rel, k, g)
righe = []
for (a, m), d in sorted(tab.items()):
    if 'e' not in d:
        continue
    h, rel, k, g = d['e']
    uguali = ''.join(sorted(l for l, x in d.items() if x[0] == h and l != 'e'))
    diverse = ''.join(sorted(l for l, x in d.items() if x[0] != h))
    f = pack.get(h)
    if f is None:
        esito = 'MANCA'
    elif f.startswith('ui_it/') and uguali:
        esito = 'ITA-SU-ING'
    elif f.startswith('upscale_extra/'):
        esito = 'xBRZ'
    elif f.startswith('ui_'):
        esito = 'ui_xx'
    else:
        esito = 'ok'
    try:
        dim = f'{g.width}x{g.height}'
    except Exception:
        dim = '?'
    righe.append((rel, k, h, dim, esito, f or '-', 'uguale in: ' + (uguali or '-') + ' | diversa in: ' + (diverse or '-')))
for r in righe:
    print(' | '.join(r))
import collections
print('#', dict(collections.Counter(r[4] for r in righe)), len(righe), 'texture inglesi', file=sys.stderr)
