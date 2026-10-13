"""Tag Force 1 card database (cardinfo_xxx.ehp): names, descriptions, props (layout from xan1242/TFCardEdit)."""
import struct, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from ehp import read
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'correzioni'))
import applica
import lingue


def _str(blob, off):
    end = off
    while blob[end:end + 2] != b'\0\0':
        end += 2
    return blob[off:end].decode('utf-16-le')


def load(path, corretto=True):
    """corretto=True applica correzioni_carte.json ai testi italiani (solo per archivi *_ita)"""
    f = read(path)
    L = next(k[-5] for k in f if k.startswith('CARD_Name_'))
    name, desc, indx, intid, prop = (f[f'CARD_Name_{L}.bin'], f[f'CARD_Desc_{L}.bin'], f[f'CARD_Indx_{L}.bin'],
                                     f['CARD_IntID.bin'], f['CARD_Prop.bin'])
    cards = {}
    for off in range(len(intid) // 2):
        idx = struct.unpack_from('<H', intid, off * 2)[0]
        if not idx:
            continue
        no, do = struct.unpack_from('<II', indx, idx * 8)
        p1, p2 = struct.unpack_from('<II', prop, idx * 8)
        cards[4000 + off] = dict(name=_str(name, no), desc=_str(desc, do), id=p1 & 0x1FFF,
                                 atk=((p1 >> 13) & 0x1FF) * 10, deff=((p1 >> 22) & 0x1FF) * 10,
                                 kind=p2 & 0xF, attr=(p2 >> 4) & 0xF, level=(p2 >> 8) & 0xF,
                                 icon=(p2 >> 12) & 0x7, type=(p2 >> 15) & 0x1F, rarity=(p2 >> 20) & 0xF)
    lingua = lingue.DA_FILE.get(os.path.basename(path)[9:12].lower())   # cardinfo_xxx.ehp -> it|fr|de|es|en
    if corretto and lingua:
        for k, c in cards.items():
            c['name'] = applica.carta(k, 'name', c['name'], lingua); c['desc'] = applica.carta(k, 'desc', c['desc'], lingua)
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
