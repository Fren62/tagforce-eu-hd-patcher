"""Estrae dal gioco le strisce 128x32 delle etichette [CARTA MAGIA]/[CARTA TRAPPOLA] di ogni lingua (la texture
card_spell_trap.gim di field/always_<lingua>_<lingua>.ehp) in dati/label_eu_<codice>_128x32.png, e stampa l'hash dei dati
(chiave per textures.ini).   usage: estrai_etichette.py USRDIR [OUT_DIR]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ehp import read
import gim
import lingue

usr = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'dati')
for code, (f3, _, _) in lingue.LINGUE.items():
    p = os.path.join(usr, 'field', f'always_{f3}_{f3}.ehp')
    if not os.path.exists(p):
        continue
    g = gim.parse(read(p)['card_spell_trap.gim'])
    gim.to_png(g).save(os.path.join(out, f'label_eu_{f3}_128x32.png'))
    print(code, f3, gim.data_hash(g))
