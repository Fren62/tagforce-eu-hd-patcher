"""Points the card rows of an existing textures.ini at cards/<kind>_<l>/<id>.png when the language's card has the same pixels as English
(same name) but the localized PNG exists in the pack: gen_ini.py/module_ini.py used to leave those on the US PNG (different banner font).
usage: localize_shared_cards.py CARD_DIR PACK_DIR LANGUAGE INI [INI ...]     (rewrites the INI files in place)"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import languages
from module_ini import hash_languages, CARD

card_dir, pack, code = sys.argv[1:4]
letter = languages.LANGUAGES[code][1]
mine = hash_languages(card_dir)[letter]
for ini in sys.argv[4:]:
    rows, n = [], 0
    for row in open(ini, encoding='utf-8', errors='ignore').read().split('\n'):
        m = CARD.match(row.rstrip('\r'))
        if m and m.group(6).lower() == mine.get(m.group(3).lower(), ''):
            alt = f'cards/{m.group(6).lower()}_{code}/{m.group(7)}'
            if os.path.exists(os.path.join(pack, alt)):
                row = f'{m.group(1)}{m.group(2)}{m.group(3).lower()}{m.group(4)}{alt}'
                n += 1
        rows.append(row)
    open(ini, 'w', encoding='utf-8', newline='\n').write('\n'.join(rows))
    print(ini, 'rows now localized:', n)
