"""Tag Force 1 card database (cardinfo_xxx.ehp): names, descriptions, props (layout from xan1242/TFCardEdit)."""
import struct, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ehp import read
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corrections'))
import card_corrections
import languages


def _str(blob, off):
    end = off
    while blob[end:end + 2] != b'\0\0':
        end += 2
    return blob[off:end].decode('utf-16-le')


def load(path, corrected=True):
    """corrected=True applies the card corrections (data/card_corrections*.json) to the texts of the archive's language"""
    f = read(path)
    table_letter = next(k[-5] for k in f if k.startswith('CARD_Name_'))
    name, desc, indx, intid, prop = (f[f'CARD_Name_{table_letter}.bin'], f[f'CARD_Desc_{table_letter}.bin'], f[f'CARD_Indx_{table_letter}.bin'],
                                     f['CARD_IntID.bin'], f['CARD_Prop.bin'])
    cards = {}
    for off in range(len(intid) // 2):
        idx = struct.unpack_from('<H', intid, off * 2)[0]
        if not idx:
            continue
        name_off, desc_off = struct.unpack_from('<II', indx, idx * 8)
        p1, p2 = struct.unpack_from('<II', prop, idx * 8)
        cards[4000 + off] = dict(name=_str(name, name_off), desc=_str(desc, desc_off), id=p1 & 0x1FFF,
                                 atk=((p1 >> 13) & 0x1FF) * 10, deff=((p1 >> 22) & 0x1FF) * 10,
                                 kind=p2 & 0xF, attr=(p2 >> 4) & 0xF, level=(p2 >> 8) & 0xF,
                                 icon=(p2 >> 12) & 0x7, type=(p2 >> 15) & 0x1F, rarity=(p2 >> 20) & 0xF)
    language = languages.CODE_FROM_FILE.get(os.path.basename(path)[9:12].lower())   # cardinfo_xxx.ehp -> it|fr|de|es|en
    if corrected and language:
        for k, c in cards.items():
            c['name'] = card_corrections.card(k, 'name', c['name'], language)
            c['desc'] = card_corrections.card(k, 'desc', c['desc'], language)
    return cards


if __name__ == '__main__':
    import collections
    c = load(sys.argv[1])
    print(len(c), 'id check', sum(v['id'] == k for k, v in c.items()))
    for field in ('kind', 'icon', 'type', 'attr'):
        g = collections.defaultdict(list)
        for k, v in c.items():
            g[v[field]].append(v['name'])
        print('==', field)
        for val in sorted(g):
            print(f'  {val:2d} n={len(g[val]):4d}', ' | '.join(g[val][:6]))
