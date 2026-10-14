"""Lists the PNGs of a pack in which at least 90% of the visible 4x4 blocks are constant (nearest enlargement, i.e. still pixelated).
usage: find_pixelated.py PACK_DIR OUT.txt   (columns: fraction, visible blocks, path)"""
import os, sys
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor


def f(p):
    try:
        a = np.asarray(Image.open(p).convert('RGBA')); h, w = a.shape[:2]
        if h % 4 or w % 4 or h < 32 or w < 32:
            return None
        b = a.reshape(h // 4, 4, w // 4, 4, 4)
        c = (b == b[:, :1, :, :1, :]).all(axis=(1, 3, 4))
        vis = a[..., 3].reshape(h // 4, 4, w // 4, 4).max(axis=(1, 3)) > 0
        n = vis.sum()
        return None if n < 50 else ((c & vis).sum() / n, n)
    except Exception:
        return None


def main(root, out):
    fs = [os.path.join(d, x) for d, _, xs in os.walk(root) for x in xs if x.endswith('.png')]
    with ProcessPoolExecutor(8) as ex:
        rs = list(ex.map(f, fs, chunksize=50))
    res = sorted(((r[0], r[1], p) for p, r in zip(fs, rs) if r and r[0] > 0.9), key=lambda t: -t[1])
    with open(out, 'w', encoding='utf-8') as o:
        for fr, n, p in res:
            o.write(f'{fr:.3f}\t{n}\t{p}\n')
    print(len(fs), 'png,', len(res), 'sgranate')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
