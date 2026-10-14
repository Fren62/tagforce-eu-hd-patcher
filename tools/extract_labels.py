"""Extracts from the game the 128x32 strips of the [SPELL CARD]/[TRAP CARD] labels of every language (the
card_spell_trap.gim texture of field/always_<language>_<language>.ehp) into data/label_eu_<code>_128x32.png, and prints the data hash
(key for textures.ini).   usage: extract_labels.py USRDIR [OUT_DIR]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ehp import read
import gim
import languages

usr = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'data')
for code, (f3, _, _) in languages.LANGUAGES.items():
    p = os.path.join(usr, 'field', f'always_{f3}_{f3}.ehp')
    if not os.path.exists(p):
        continue
    g = gim.parse(read(p)['card_spell_trap.gim'])
    gim.to_png(g).save(os.path.join(out, f'label_eu_{f3}_128x32.png'))
    print(code, f3, gim.data_hash(g))
