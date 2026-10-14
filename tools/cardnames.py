"""card id -> name from a Tag Force 1 cardinfo_xxx.ehp."""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ehp import read
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corrections'))
import card_corrections
import languages


def names(path):
    language = languages.CODE_FROM_FILE.get(os.path.basename(path)[9:12].lower())
    f = read(path)
    table_letter = next(k[-5] for k in f if k.startswith('CARD_Name_'))
    name, indx, intid = f[f'CARD_Name_{table_letter}.bin'], f[f'CARD_Indx_{table_letter}.bin'], f['CARD_IntID.bin']
    out = {}
    for off in range(len(intid) // 2):
        idx = struct.unpack_from('<H', intid, off * 2)[0]
        if not idx:
            continue
        name_off = struct.unpack_from('<I', indx, idx * 8)[0]
        end = name_off
        while name[end:end + 2] != b'\0\0':
            end += 2
        text = name[name_off:end].decode('utf-16-le')
        out[4000 + off] = card_corrections.card(4000 + off, 'name', text, language) if language else text
    return out


if __name__ == '__main__':
    n = names(sys.argv[1])
    for k in sys.argv[2:]:
        print(k, n.get(int(k)))
    print(len(n))
