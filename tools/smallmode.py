"""Exact clean backgrounds of the HD small cards: per-pixel MODE over all cards of a frame type
(frames are pixel-identical, text varies). usage: smallmode.py TOOLS SMALL_DIR CARDINFO_ENG OUT_DIR"""
import os, re, sys, collections
sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import Image
from cardprops import load
from smallbg import frame_of

REGIONS = [(18, 10, 211, 31), (112, 31, 234, 44), (18, 191, 238, 247)]  # name, label, desc box (x0,y0,x1,y1)


def mode_cols(col):
    s = np.sort(col, axis=0)
    N, K = s.shape
    change = np.vstack([np.ones((1, K), bool), s[1:] != s[:-1]])
    rid = np.cumsum(change, axis=0) - 1
    counts = np.bincount((rid + np.arange(K)[None, :] * N).ravel(), minlength=N * K).reshape(K, N)
    best = counts.argmax(1)
    first = (rid == best[None, :]).argmax(0)
    return s[first, np.arange(K)], counts.max(1) / N


if __name__ == '__main__':
    small, ehp, out = sys.argv[2:5]
    os.makedirs(out, exist_ok=True)
    cards = load(ehp)
    groups = collections.defaultdict(list)
    for f in sorted(os.listdir(small)):
        m = re.match(r'(\d+)', f)
        if f.endswith('.png') and m and int(m.group(1)) in cards:
            groups[frame_of(cards[int(m.group(1))])].append(f)
    for g, fs in groups.items():
        fs = fs[:500]
        stack = np.stack([np.asarray(Image.open(os.path.join(small, f)).convert('RGB')) for f in fs]).astype(np.int32)
        packed = (stack[..., 0] << 16) | (stack[..., 1] << 8) | stack[..., 2]   # N,256,256
        res = np.median(stack, 0).astype(np.uint8)
        conf = np.ones((256, 256), np.float32)
        for x0, y0, x1, y1 in REGIONS:
            col = packed[:, y0:y1, x0:x1].reshape(len(fs), -1)
            mv, share = mode_cols(col)
            mv = mv.reshape(y1 - y0, x1 - x0)
            res[y0:y1, x0:x1] = np.stack([(mv >> 16) & 255, (mv >> 8) & 255, mv & 255], -1)
            conf[y0:y1, x0:x1] = share.reshape(y1 - y0, x1 - x0)
        Image.fromarray(res).save(os.path.join(out, f'mode_{g}.png'))
        np.save(os.path.join(out, f'conf_{g}.npy'), conf)
        print(g, len(fs), 'min share name %.2f desc %.2f' % (conf[12:30, 18:210].min(), conf[192:246, 19:237].min()))
