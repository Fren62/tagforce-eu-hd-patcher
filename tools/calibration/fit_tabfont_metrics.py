import os, sys, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ui_textures'))
import tabword as T
glyphs = json.load(open(sys.argv[1]))
words = {'Trunk': 'Trunk', 'Fusion': 'Fusion', 'Side': 'Side', 'Deck': 'Deck'}
BASE = 56.0
def cost(size, track, weight=900, verbose=False):
    T.WEIGHT = weight
    tot = 0.0; n = 0; rep = []
    for w, gl in glyphs.items():
        f, xs, _ = T.layout(w, size, track)
        # left-align the first glyph core with the mod's first glyph core
        boxes = []
        for ch, x in zip(w, xs):
            b = f.getbbox(ch, anchor='ls'); boxes.append((x + b[0], x + b[2], b[1], b[3]))
        off = gl[0]['x'] - boxes[0][0] / T.SS
        for g, (l, r, t, b) in zip(gl, boxes):
            gl_, gr_, gt_, gb_ = l / T.SS + off, r / T.SS + off, BASE + t / T.SS, BASE + b / T.SS
            e = [gl_ - g['x'], gr_ - (g['x'] + g['w']), gt_ - g['y'], gb_ - (g['y'] + g['h'])]
            tot += sum(v * v for v in e); n += 4
            if verbose: rep.append((w, g['ch'], [round(v, 1) for v in e]))
    return (tot / n) ** 0.5, rep
best = None
for wt in (800, 900, 1000):
    for size in np.arange(40, 58, 1.0):
        for track in np.arange(-9, 1.5, 0.5):
            c, _ = cost(size, track, wt)
            if best is None or c < best[0]: best = (c, size, track, wt)
print('migliore: rms %.2f px, corpo %.1f, tracking %.1f, peso %d' % best)
c, rep = cost(best[1], best[2], best[3], True)
for r in rep: print(r)
