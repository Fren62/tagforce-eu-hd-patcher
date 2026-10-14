"""Per-frame-type clean backgrounds (pixel median) of the HD small cards.
usage: smallbg.py TOOLS SMALL_DIR CARDINFO_ENG OUT_DIR"""
import os, re, sys, collections
sys.path.insert(0, sys.argv[1])
import numpy as np
from PIL import Image
from cardprops import load

FRAME = {0: 'normal', 1: 'effect', 6: 'effect', 7: 'effect', 8: 'effect', 2: 'fusion', 3: 'fusion',
         4: 'ritual', 5: 'ritual', 9: 'token', 13: 'spell', 14: 'trap'}


def frame_of(card):
    return FRAME.get(card['kind'], 'effect')


if __name__ == '__main__':
    small, ehp, out = sys.argv[2:5]
    os.makedirs(out, exist_ok=True)
    cards = load(ehp)
    groups = collections.defaultdict(list)
    for f in sorted(os.listdir(small)):
        m = re.match(r'(\d+)\.png$', f)  # base art only for the median
        if m and int(m.group(1)) in cards:
            groups[frame_of(cards[int(m.group(1))])].append(f)
    for g, fs in groups.items():
        fs = fs[::max(1, len(fs) // 160)][:160]
        stack = np.stack([np.asarray(Image.open(os.path.join(small, f)).convert('RGB')) for f in fs])
        med = np.median(stack, 0).astype(np.uint8)
        Image.fromarray(med).save(os.path.join(out, f'bg_{g}.png'))
        print(g, len(fs))
