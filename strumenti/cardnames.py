"""card id -> name from a Tag Force 1 cardinfo_xxx.ehp."""
import struct, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from ehp import read
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), 'correzioni'))
import applica


def names(path):
    import lingue
    lingua = lingue.DA_FILE.get(__import__('os').path.basename(path)[9:12].lower())
    f = read(path)
    L = next(k[-5] for k in f if k.startswith('CARD_Name_'))
    name, indx, intid = f[f'CARD_Name_{L}.bin'], f[f'CARD_Indx_{L}.bin'], f['CARD_IntID.bin']
    out = {}
    for off in range(len(intid) // 2):
        idx = struct.unpack_from('<H', intid, off * 2)[0]
        if not idx:
            continue
        no = struct.unpack_from('<I', indx, idx * 8)[0]
        end = no
        while name[end:end + 2] != b'\0\0':
            end += 2
        t = name[no:end].decode('utf-16-le')
        out[4000 + off] = applica.carta(4000 + off, 'name', t, lingua) if lingua else t
    return out


if __name__ == '__main__':
    n = names(sys.argv[1])
    for k in sys.argv[2:]:
        print(k, n.get(int(k)))
    print(len(n))
