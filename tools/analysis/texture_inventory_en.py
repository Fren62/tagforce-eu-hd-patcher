"""Inventory of the textures with text of European English (archives *_e / *_eng / basic_?e): for each one says whether the base pack
covers it (and with which file) or it is missing, and whether in that case the same texture has another version in the game (different hash in the other languages).

It is needed to decide what to redraw in `modules/en/ui_en`: MikeyMK's pack is made on the US game; European English almost always has
the same pixels (same hash) and is therefore already covered, but some textures differ (e.g. the duel numbers sheet, the "Single" pill).
Beware of the opposite case: an Italian texture redrawn in `ui_it` whose hash is IDENTICAL to the English one (text not translated
by the game) would make Italian appear in the English game: it is reported as ITA-SU-ING.

usage: python texture_inventory_en.py USRDIR [BASE_INI]
Writes on stdout a table `archive | member | hash | size | outcome | pack file | languages with the same hash`."""
import glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'tools')); sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding='utf-8')
from ehp import read
import gim
import textures_per_language as T

usr = sys.argv[1]
ini_base = sys.argv[2] if len(sys.argv) > 2 else os.path.join(B, 'PSP', 'TEXTURES', 'ULES00600', 'textures.ini')
pack = {}
for r in open(ini_base, encoding='utf-8', errors='ignore'):
    m = re.match(r'^[0-9a-f]{16}([0-9a-f]{8})\s*=\s*(\S+)', r.strip())      # 24-digit key: (8-digit CLUT) + data hash (last 8)
    if m:
        pack.setdefault(m.group(1), m.group(2))
tab = {}
all = {}
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
        markers = {c: T.per_language(k, letter, T.LET3[c]) is not None for c, letter in T.LET.items()}
        for c, letter in T.LET.items():
            an, mn = T.per_language(rel, letter, T.LET3[c]), T.per_language(k, letter, T.LET3[c])
            if an is not None or mn is not None:
                if any(markers.values()) and mn is None:
                    continue      # the member carries the mark of another language (e.g. a start_e archive that also contains the _i variants): it is not of this language
                tab.setdefault((an or rel, mn or k), {})[letter] = (h, rel, k, g)
rows = []
for (a, m), d in sorted(tab.items()):
    if 'e' not in d:
        continue
    h, rel, k, g = d['e']
    equal = ''.join(sorted(l for l, x in d.items() if x[0] == h and l != 'e'))
    different = ''.join(sorted(l for l, x in d.items() if x[0] != h))
    f = pack.get(h)
    if f is None:
        outcome = 'MANCA'
    elif f.startswith('ui_it/') and equal:
        outcome = 'ITA-SU-ING'
    elif f.startswith('upscale_extra/'):
        outcome = 'xBRZ'
    elif f.startswith('ui_'):
        outcome = 'ui_xx'
    else:
        outcome = 'ok'
    try:
        dim = f'{g.width}x{g.height}'
    except Exception:
        dim = '?'
    rows.append((rel, k, h, dim, outcome, f or '-', 'uguale in: ' + (equal or '-') + ' | diversa in: ' + (different or '-')))
for r in rows:
    print(' | '.join(r))
import collections
print('#', dict(collections.Counter(r[4] for r in rows)), len(rows), 'texture inglesi', file=sys.stderr)
