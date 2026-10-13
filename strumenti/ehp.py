"""Minimal EHP (Tag Force archive) reader: ehp.py FILE OUTDIR"""
import os, struct, sys


def read(path):
    d = open(path, 'rb').read()
    _, _, _, n = struct.unpack_from('<IIII', d, 0)
    out = {}
    for i in range(n):
        no, fo = struct.unpack_from('<II', d, 16 + i * 8)
        name = d[no:d.index(b'\0', no)].decode()
        size = struct.unpack_from('<I', d, d.index(b'\0', no) + 1)[0]
        out[name] = d[fo:fo + size]
    return out


if __name__ == '__main__':
    os.makedirs(sys.argv[2], exist_ok=True)
    for k, v in read(sys.argv[1]).items():
        open(os.path.join(sys.argv[2], k), 'wb').write(v)
        print(k, len(v))
