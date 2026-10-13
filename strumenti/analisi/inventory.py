"""Inventory of every GIM texture in the EU ISO vs the installed HD pack.
For each texture used by the ITALIAN game: language-specific (differs from the English variant)? covered by the pack
(PPSSPP data hash present in textures.ini)? is the English counterpart covered (= an HD English reference exists)?
usage: inventory.py USRDIR TEXTURES_INI OUT.json"""
import json, os, re, sys, glob, collections
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, '/Users/admin/Desktop/tmp/TF1_HD_ITA/strumenti')
from ehp import read
import gim

U, ini, out = sys.argv[1:4]
pack = {}
for line in open(ini, encoding='utf-8', errors='replace'):
    m = re.match(r'^([0-9a-fA-F]{24})\s*=\s*(.*)$', line.strip())
    if m:
        pack[m.group(1)[16:].lower()] = m.group(2).strip()

L1 = 'efgijsu'
LANG3 = {'eng': 'e', 'usa': 'u', 'ita': 'i', 'fra': 'f', 'ger': 'g', 'spa': 's', 'jpn': 'j'}


def langkey(rel, member):
    """(group key, language of the menu text, language of the card text) from file + member names."""
    ui = card = None
    a = rel
    m = re.match(r'(.*/always)_([a-z]{3})_([a-z]{3})\.ehp$', a)
    if m:
        card, ui = LANG3.get(m.group(2)), LANG3.get(m.group(3)); a = m.group(1) + '_*_*.ehp'
    m = re.match(r'(.*/basic)_([a-z])([a-z])\.ehp$', a)
    if m:
        card, ui = m.group(2), m.group(3); a = m.group(1) + '_**.ehp'
    m = re.match(r'(.*)_([' + L1 + r'])\.ehp$', a)
    if m and ui is None:
        ui = m.group(2); a = m.group(1) + '_*.ehp'
    b = member
    m = re.match(r'(.*?)_([' + L1 + r'])(\d*\.gim)$', b)
    if m:
        ui = m.group(2); b = m.group(1) + '_*' + m.group(3)   # the member's own language wins over the archive's
    return a + '|' + b, ui, card


rows = []
for path in sorted(glob.glob(U + '/**/*.ehp', recursive=True) + glob.glob(U + '/**/*.gim', recursive=True)):
    rel = os.path.relpath(path, U)
    try:
        members = read(path).items() if path.endswith('.ehp') else [(os.path.basename(path), open(path, 'rb').read())]
    except Exception:
        continue
    for name, data in members:
        if not name.endswith('.gim'):
            continue
        g = gim.parse(data)
        if not g:
            continue
        key, ui, card = langkey(rel, name)
        rows.append(dict(file=rel, member=name, group=key, ui=ui, card=card, fmt=g['fmt'], w=g['w'], h=g['h'],
                         hash=gim.data_hash(g)))

groups = collections.defaultdict(list)
for r in rows:
    groups[r['group']].append(r)


def italian(r):
    """is this variant the one the Italian game loads?"""
    return (r['ui'] in (None, 'i')) and (r['card'] in (None, 'i'))


items = {}
for k, rs in groups.items():
    for r in rs:
        if not italian(r) or r['hash'] is None:
            continue
        en = [x for x in rs if (x['ui'] in (None, 'e', 'u')) and (x['card'] in (None, 'e', 'u'))
              and (x['ui'] or x['card'])]
        lang_specific = any(x['hash'] != r['hash'] for x in rs if x is not r)
        h = r['hash']
        if h in items:
            items[h]['uses'].append(r['file'] + ':' + r['member'])
            continue
        items[h] = dict(hash=h, file=r['file'], member=r['member'], w=r['w'], h=r['h'], fmt=r['fmt'],
                        lang_specific=lang_specific, covered=h in pack, pack_file=pack.get(h),
                        en_hash=[x['hash'] for x in en][:1], en_covered=any(x['hash'] in pack for x in en),
                        en_pack_file=next((pack[x['hash']] for x in en if x['hash'] in pack), None), uses=[r['file'] + ':' + r['member']])
json.dump(list(items.values()), open(out, 'w'), indent=1)
c = collections.Counter((v['lang_specific'], v['covered'], v['en_covered']) for v in items.values())
print('texture uniche usate dal gioco italiano:', len(items))
for (ls, cov, enc), n in sorted(c.items()):
    print(f"  testo per lingua={ls!s:5} coperta dal pack={cov!s:5} inglese coperto={enc!s:5}: {n}")
