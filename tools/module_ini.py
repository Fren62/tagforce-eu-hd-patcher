"""Adds to a ULES00600 textures.ini the localization of one or more languages: the small and large cards of that language
point to cards/small_<l> and cards/large_<l> (same precedence as gen_ini.py: if the same pixels exist in several languages
the first in 'eifgs' wins), plus the modules' <l>.ini fragments (Spell/Trap labels).
usage: module_ini.py CARD_DIR INI_IN INI_OUT MODULES_DIR LANGUAGE [LANGUAGE ...]     (LANGUAGE = fr de es it ...)
  CARD_DIR     PSP_GAME/USRDIR/card of the ISO (cardh_*.cip, cardm_*.cip)
  MODULES_DIR  folder with one subfolder per language; a missing file leaves the English image."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import languages
from tfcards import card_ids, slots, small_blob, large_blob, large_keys, key

ORDER = 'eifgs'
CARD = re.compile(r'^(0{8})(0000060[67])([0-9a-f]{8})(\s*=\s*)(cards/(small|large)/([^/]+\.png))\s*$', re.I)


def hash_languages(card_dir):
    """{language letter: {hash: (type, ...)}} for the small and large cards."""
    arch = {(k, l): open(f'{card_dir}/{k}_{l}.cip', 'rb').read() for k in ('cardh', 'cardm') for l in ORDER}
    ids = card_ids(arch[('cardm', 'e')])
    out = {l: {} for l in ORDER}
    for l in ORDER:
        for cid in ids:
            for s in slots(arch[('cardm', l)], cid):
                if s:
                    out[l][key(0, small_blob(arch[('cardm', l)], s))] = 'small'
            for s in slots(arch[('cardh', l)], cid):
                if s:
                    for h in large_keys(large_blob(arch[('cardh', l)], s), stable=False) + large_keys(large_blob(arch[('cardh', l)], s)):
                        out[l][h] = 'large'
    return out


def main(card_dir, ini_in, ini_out, modules, codes):
    hours = hash_languages(card_dir)
    letter = {c: languages.LANGUAGES[c][1] for c in codes}
    owner = {}
    for l in ORDER:                      # the first one that has the hash owns it
        for h in hours[l]:
            owner.setdefault(h, l)
    changes = {c: 0 for c in codes}
    rows = []
    for row in open(ini_in, encoding='utf-8', errors='ignore').read().split('\n'):
        m = CARD.match(row.rstrip('\r'))
        if m:
            h = m.group(3).lower()
            for c in codes:
                if m.group(6).lower() == hours[letter[c]].get(h, ''):   # also hashes shared with other languages (same name: banner font still differs from the US pack)
                    alt = f'cards/{m.group(6).lower()}_{c}/{m.group(7)}'
                    if os.path.exists(os.path.join(modules, c, alt)):
                        row = f'{m.group(1)}{m.group(2)}{h}{m.group(4)}{alt}'
                        changes[c] += 1
                    break
        rows.append(row)
    # a fragment replaces the existing lines with the same hash (e.g. the label strip enlarged with xBRZ)
    keys = set()
    for c in codes:
        frm = os.path.join(modules, c, f'{c}.ini')
        if os.path.exists(frm):
            keys |= {m.group(1).lower() for m in re.finditer(r'^([0-9a-fA-F]{24})\s*=', open(frm, encoding='utf-8').read(), re.M)}
    rows = [r for r in rows if not (re.match(r'^[0-9a-fA-F]{24}\s*=', r) and r[:24].lower() in keys)]
    text = '\n'.join(rows)
    if not text.endswith('\n'):
        text += '\n'
    already = set()
    for c in codes:
        frm = os.path.join(modules, c, f'{c}.ini')
        if os.path.exists(frm):
            for r in open(frm, encoding='utf-8').read().split('\n'):   # the same key in several languages (e.g. thumbnail atlas): the first wins
                k = r[:24].lower() if re.match(r'^[0-9a-fA-F]{24}\s*=', r) else None
                if k and k in already:
                    continue
                if k:
                    already.add(k)
                text += r + '\n' if r else ''
    open(ini_out, 'w', encoding='utf-8', newline='\n').write(text)
    print('localized card lines:', changes)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
