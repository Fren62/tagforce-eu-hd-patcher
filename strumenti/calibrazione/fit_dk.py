"""Refine ink darkness (dk), opacity (ink) and weight (edge g) of a fitted description style.
usage: fit_dk.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG FIT.json OUT.json"""
import json, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
from deschar import Bench

cdir, clean_dir, ehp, fin, fout = sys.argv[2:7]
j = json.load(open(fin))
bench = Bench(cdir, clean_dir, ehp, j['kind'], n=16)
st = j['style']; st['font'] = tuple(j['font']); st.setdefault('dk', 1.0)
best = (*bench.evaluate(st), st)
for rnd in range(3):
    for key, vals, sub in (('dk', np.arange(0.4, 1.01, 0.05), None), ('ink', np.arange(0.6, 1.01, 0.05), None), ('g', np.arange(0.3, 1.61, 0.1), 'edge')):
        for v in vals:
            q = json.loads(json.dumps({k: v2 for k, v2 in best[2].items() if k != 'font'})); q['font'] = st['font']
            if sub:
                q[sub][key] = float(v)
            else:
                q[key] = float(v)
            l, r = bench.evaluate(q)
            if r is not None and l < best[0] - 1e-6:
                best = (l, r, q)
l, r, p = best
j.update(loss=l, metrics=r, style={k: v for k, v in p.items() if k != 'font'})
json.dump(j, open(fout, 'w'), indent=1)
print('RISULTATO', j['kind'], j['name'], 'perdita %.2f' % l, 'dk %.2f ink %.2f g %.2f' % (p['dk'], p['ink'], p['edge']['g']), 'scurezza %.3f densita %.3f' % (r['dark'], r['dens']), flush=True)
