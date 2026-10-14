"""textures.ini lines that point the deck thumbnail atlas pages to the language's pages (cards/tiny_<l>/...).
usage: tiny_fragment.py LANGUAGE INI_BASE OUT_FRAGMENT       (INI_BASE = textures.ini of the English/base pack)
The keys (page hashes) are those the base ini assigns to cards/tiny*/<a>_<b>.png; the fragment replaces them
(module_ini.py replaces the lines with the same hash)."""
import re, sys

language, ini, out = sys.argv[1:4]
rows = []
for l in open(ini, encoding='utf-8', errors='ignore'):
    m = re.match(r'^([0-9a-fA-F]{24})\s*=\s*cards/tiny\w+/(\d+_\d+\.png)\s*$', l.rstrip('\r\n'))
    if m:
        rows.append(f'{m.group(1)} = cards/tiny_{language}/{m.group(2)}')
with open(out, 'a', encoding='utf-8', newline='\n') as f:
    f.write(f'# deck thumbnails ({language}): atlas pages rebuilt with the small cards\n' + '\n'.join(rows) + '\n')
print(len(rows), 'lines')
