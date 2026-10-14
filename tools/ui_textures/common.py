"""Shared helpers for the HD Italian UI textures (tools/ui_textures/<family>.py).

Every family script is run as:   python3 -I <family>.py USRDIR PACK_US OUT
  USRDIR   PSP_GAME/USRDIR of the European ISO (fully extracted, movies/audio not needed)
  PACK_US  ULUS10136 folder of the English HD pack (MikeyMK) - style references only
  OUT      output pack folder (e.g. .../TEXTURES/ULES00600)
and writes OUT/ui_it/<family>/<id>.png plus OUT/ui_it/<family>.ini with lines
  0000000000000000<data hash> = ui_it/<family>/<id>.png
(PPSSPP matches a key with zero address/CLUT on the data hash alone, see TextureReplacer LookupWildcard.)

A replacement must redraw EXACTLY the content of the original Italian texture (the game composes words from
pieces at fixed positions), at 4x its size, in the style of the English HD pack."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from PIL import Image
from ehp import read
import gim

SCALE = 4
_arch = {}


def texture(usrdir, file, member):
    """(PIL RGBA low-res image, PPSSPP data hash) of a GIM inside an EHP archive (or a loose .gim)."""
    p = os.path.join(usrdir, file)
    if p not in _arch:
        _arch.clear()
        _arch[p] = read(p) if p.endswith('.ehp') else {os.path.basename(p): open(p, 'rb').read()}
    g = gim.parse(_arch[p][member])
    return gim.to_png(g), gim.data_hash(g)


def reference(pack_us, rel):
    """English HD reference image from the US pack (RGBA)."""
    return Image.open(os.path.join(pack_us, rel)).convert('RGBA')


class Family:
    def __init__(self, name, argv):
        self.name = name
        self.usrdir, self.pack_us, self.out = argv[1:4]
        self.lang = os.environ.get('TF1_LANG', 'it')
        self.dir = os.path.join(self.out, 'ui_' + self.lang, name)
        os.makedirs(self.dir, exist_ok=True)
        self.lines = []
        self.report = []

    def save(self, tex_id, hd, hash_, low=None):
        """write the HD image, register it; low: original Italian texture for the check."""
        hd = hd.convert('RGBA')
        hd.save(os.path.join(self.dir, f'{tex_id}.png'), optimize=True)
        self.lines.append(f'0000000000000000{hash_} = ui_{self.lang}/{self.name}/{tex_id}.png')
        if low is not None:
            self.report.append((tex_id,) + check(hd, low))

    def finish(self):
        with open(os.path.join(self.dir + '.ini'), 'w') as f:
            f.write(f'# {self.name}: HD UI textures ({self.lang})\n' + '\n'.join(self.lines) + '\n')
        if self.lang != 'it':       # language module: the lines go into the <language>.ini fragment (they replace those of the family)
            ini = os.path.join(self.out, self.lang + '.ini')
            old = open(ini, encoding='utf-8').read().split('\n') if os.path.exists(ini) else []
            old = [r for r in old if f'ui_{self.lang}/{self.name}/' not in r and r.strip()]
            open(ini, 'w', encoding='utf-8').write('\n'.join(old + self.lines) + '\n')
        for r in self.report:
            print('%-40s alfa MAE %.1f  colore MAE %.1f' % r)
        print(self.name, len(self.lines), 'texture')


def check(hd, low):
    """mean abs error (0-255) between the HD image box-downscaled to the original size and the original:
    alpha everywhere, color where the original is visible (alpha > 128)."""
    low = np.asarray(low.convert('RGBA'), np.float32)
    small = np.asarray(hd.convert('RGBA').resize((low.shape[1], low.shape[0]), Image.BOX), np.float32)
    a = np.abs(small[..., 3] - low[..., 3]).mean()
    vis = low[..., 3] > 128
    c = np.abs(small[..., :3] - low[..., :3])[vis].mean() if vis.any() else 0.0
    return float(a), float(c)
