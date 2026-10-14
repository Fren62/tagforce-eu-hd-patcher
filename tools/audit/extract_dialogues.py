"""Extracts the dialogues (script/stNN_*_<l>.ehp) of all the European languages into comparisons/audit_dialoghi/dialoghi_<l>.tsv:
id (archive/scene#index), language text, English text, Japanese. Line breaks written as ⏎.  usage: extract_dialogues.py ISO OUT_DIR"""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'corrections')); sys.path.insert(0, os.path.join(HERE, '..'))
import pycdlib
import apply_to_iso as ai, dialogues as D
iso_p, out = sys.argv[1:3]; os.makedirs(out, exist_ok=True)
iso = pycdlib.PyCdlib(); iso.open(iso_p)
names = [c.file_identifier().decode().split(';')[0] for c in iso.list_children(iso_path='/PSP_GAME/USRDIR/script')]
get = lambda p: (lambda b: (iso.get_file_from_iso_fp(b, iso_path=p), b.getvalue())[1])(io.BytesIO())
LL = {'i': 'it', 'f': 'fr', 'g': 'de', 's': 'es', 'e': 'en', 'j': 'ja'}
data = {}
for n in sorted(names):
    if not (n.endswith('.ehp') and n[:2] == 'st' and n.rsplit('_', 1)[-1][:-4] in LL):
        continue
    st, l = n[:-4].rsplit('_', 1)
    _, f = ai.open_ehp(get('/PSP_GAME/USRDIR/script/' + n))
    for k in f:
        if k.startswith(('.', '_')) or not k.split('.')[0].endswith('I' + l):
            continue
        sc = k.split('I' + l + '.bin')[0]
        try:
            data[(st, sc, l)] = D.strings(f, sc, l)
        except Exception:
            pass
for l in 'ifgse':
    with open(f'{out}/dialoghi_{LL[l]}.tsv', 'w', encoding='utf-8') as o:
        n = 0
        for (st, sc, ll), v in sorted(data.items()):
            if ll != l:
                continue
            en, ja = data.get((st, sc, 'e'), []), data.get((st, sc, 'j'), [])
            for i, t in enumerate(v):
                t = t.rstrip(D.TRAILING)
                if not t.strip():
                    continue
                g = lambda a: a[i].rstrip(D.TRAILING).replace('\n', '⏎') if i < len(a) else ''
                o.write(f'{st}/{sc}#{i}\t{t.replace(chr(10), "⏎")}\t{g(en)}\t{g(ja)}\n'); n += 1
    print(LL[l], n)
