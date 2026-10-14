"""Extract the white letter cores of the mod's HD tab words (Trunk, Fusion, Side, Deck) -> glyph masks with metrics."""
import sys, json
import numpy as np, cv2
from PIL import Image
P = sys.argv[1] + '/ui/deckedit/'
TABS = {'Trunk': ('00000000a33778db85d8f4f8.png', 'Trunk'), 'Fusion': ('0000000065037c929f671d8d.png', 'Fusion'),
        'Side': ('000000006c2037fcdf435532.png', 'Side'), 'Deck': ('00000000f1fc5e4cf83d4357.png', 'Deck')}
out = {}
for name, (f, word) in TABS.items():
    a = np.asarray(Image.open(P + f).convert('RGB')).astype(np.int32)
    H, W = a.shape[:2]
    core = (a.min(-1) > 205)
    core[:8] = False; core[72:] = False
    x_box = {'Trunk': 150, 'Fusion': 146, 'Side': 146, 'Deck': 146}[name]
    mask = core.copy(); mask[:, x_box:] = False; mask[:, :8] = False
    n, lab, st, cen = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    comps = [(st[i, 0], st[i, 1], st[i, 2], st[i, 3], i) for i in range(1, n) if st[i, 4] > 40]
    comps.sort()
    # merge the dot of 'i' (small comp over a taller one)
    merged = []
    for c in comps:
        if merged and c[0] < merged[-1][0] + merged[-1][2] and (c[0] + c[2] > merged[-1][0]) and c[0] <= merged[-1][0] + merged[-1][2] - 0.5 * min(c[2], merged[-1][2]):
            m = merged[-1]; x0 = min(m[0], c[0]); y0 = min(m[1], c[1]); x1 = max(m[0] + m[2], c[0] + c[2]); y1 = max(m[1] + m[3], c[1] + c[3])
            merged[-1] = (x0, y0, x1 - x0, y1 - y0, m[4], c[4]); 
        else:
            merged.append(c)
    print(name, 'letters', len(merged), 'expected', len(word), [(c[0], c[1], c[2], c[3]) for c in merged])
    out[name] = [dict(ch=(word[i] if i < len(word) else '?'), x=int(c[0]), y=int(c[1]), w=int(c[2]), h=int(c[3])) for i, c in enumerate(merged)]
json.dump(out, open(sys.argv[2], 'w'), indent=1)
