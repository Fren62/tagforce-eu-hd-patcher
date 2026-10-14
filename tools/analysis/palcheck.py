import sys, os, glob, json, collections
import xxhash
N, O, OUT = sys.argv[1:4]
sys.path.insert(0, N + '/tools'); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from ehp import read
import gim
U = N + '/iso/PSP_GAME/USRDIR'
ab = json.load(open(N + '/sheets/ab.json'))
targets = {r['hash'] for r in ab}
by = collections.defaultdict(set); locs = collections.defaultdict(list)
dump = {f[16:24]: f for f in os.listdir(O + '/cleanup/texdump_new') if f.endswith('.png')}
ok = bad = 0; samples = []
for path in glob.glob(U + '/**/*.ehp', recursive=True) + glob.glob(U + '/**/*.gim', recursive=True):
    try: members = read(path).items() if path.endswith('.ehp') else [(os.path.basename(path), open(path, 'rb').read())]
    except Exception: continue
    for name, data in members:
        if not name.endswith('.gim'): continue
        g = gim.parse(data)
        if not g: continue
        h = gim.data_hash(g)
        if h is None: continue
        pal = g['pal_raw'] or b''
        if h in targets:
            by[h].add(pal); locs[h].append(os.path.relpath(path, U) + ':' + name)
        if h in dump and g['pal_raw']:
            c = '%08x' % xxhash.xxh32_intdigest(pal, 0xC0108888)
            if dump[h][8:16] == c: ok += 1
            else:
                bad += 1
                if len(samples) < 6: samples.append((h, dump[h][8:16], c, len(pal), g['pal_fmt']))
coll = {h: len(p) for h, p in by.items() if len(p) > 1}
with open(OUT, 'w') as f:
    f.write(f'bersagli: {len(targets)} | hash dati con palette diverse nel gioco: {len(coll)}\n')
    for h, n in coll.items(): f.write(f'  {h} {n} palette: {locs[h][:5]}\n')
    f.write(f'hash CLUT calcolato = dump: ok {ok} diversi {bad} {samples}\n')
    f.write('FINE\n')
