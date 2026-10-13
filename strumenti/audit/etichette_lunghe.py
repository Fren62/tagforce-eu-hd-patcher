"""Etichette dell'interfaccia che rischiano di essere tagliate dal bordo di una casella o dello schermo: voci delle tabelle di
stringhe dei pulsanti (deck editor e duello) molto piu' lunghe dell'equivalente inglese. Servono i file estratti dalla ISO:
usage: etichette_lunghe.py ISO [rapporto >= 1.4] [lunghezza minima 9]
Confronta, per ogni lingua, la stessa voce (stesso indice) della tabella inglese; stampa lingua | indice | testo | inglese."""
import io, os, struct, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import pycdlib
from ehp import read

iso_path = sys.argv[1]
ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 1.4
minlen = int(sys.argv[3]) if len(sys.argv) > 3 else 9
MAXEN = int(sys.argv[4]) if len(sys.argv) > 4 else 99   # solo etichette inglesi corte (pulsanti), non didascalie
LING = {'e': 'inglese', 'i': 'italiano', 'f': 'francese', 'g': 'tedesco', 's': 'spagnolo'}


def tabella(d):
    n, to, do = struct.unpack_from('<III', d, 0)
    out = []
    for o in struct.unpack_from(f'<{n}I', d, to):
        p = do + o; e = p
        while e + 1 < len(d) and d[e:e + 2] != b'\0\0':
            e += 2
        out.append(d[p:e].decode('utf-16-le', 'replace'))
    return out


iso = pycdlib.PyCdlib(); iso.open(iso_path)
tmp = os.path.join(tempfile.gettempdir(), 'el.ehp')


def archivio(p):
    b = io.BytesIO(); iso.get_file_from_iso_fp(b, iso_path=p); open(tmp, 'wb').write(b.getvalue()); return read(tmp)


gruppi = {}   # nome gruppo -> {lingua: lista}
for l in LING:
    ar = archivio(f'/PSP_GAME/USRDIR/deck/all_{l}.ehp')
    if 'strTbl.bin' in ar:
        gruppi.setdefault('deck strTbl', {})[l] = tabella(ar['strTbl.bin'])
for l, l3 in (('e', 'e'), ('i', 'i'), ('f', 'f'), ('g', 'g'), ('s', 's')):
    ar = archivio('/PSP_GAME/USRDIR/duel/basic_ea.ehp' if l == 'e' else f'/PSP_GAME/USRDIR/duel/basic_{l3}e.ehp')
    k = f'ddstrtbl_{l}.bin'
    if k in ar:
        gruppi.setdefault('duello ddstrtbl', {})[l] = tabella(ar[k])
for g, per in gruppi.items():
    en = per.get('e')
    if not en:
        continue
    print('==', g, {l: len(v) for l, v in per.items()})
    for l, t in per.items():
        if l == 'e':
            continue
        for i, s in enumerate(t[:len(en)]):
            if len(s) >= minlen and en[i] and len(s) >= ratio * len(en[i]) and len(s) <= 40 and len(en[i]) <= MAXEN:
                print(f'{LING[l]:9s} | {i:3d} | {s[:40]:40s} | {en[i][:30]}')
