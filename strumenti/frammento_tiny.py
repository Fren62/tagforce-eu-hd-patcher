"""Righe di textures.ini che puntano le pagine dell'atlante delle miniature del deck alle pagine della lingua (cards/tiny_<l>/...).
usage: frammento_tiny.py LINGUA INI_BASE OUT_FRAMMENTO       (INI_BASE = textures.ini del pack inglese/di base)
Le chiavi (hash delle pagine) sono quelle che l'ini di base assegna a cards/tiny*/<a>_<b>.png; il frammento le sostituisce
(modulo_ini.py sostituisce le righe con lo stesso hash)."""
import re, sys

lingua, ini, out = sys.argv[1:4]
righe = []
for l in open(ini, encoding='utf-8', errors='ignore'):
    m = re.match(r'^([0-9a-fA-F]{24})\s*=\s*cards/tiny\w+/(\d+_\d+\.png)\s*$', l.rstrip('\r\n'))
    if m:
        righe.append(f'{m.group(1)} = cards/tiny_{lingua}/{m.group(2)}')
with open(out, 'a', encoding='utf-8', newline='\n') as f:
    f.write(f'# miniature del deck ({lingua}): pagine dell\'atlante ricostruite con le carte piccole\n' + '\n'.join(righe) + '\n')
print(len(righe), 'righe')
