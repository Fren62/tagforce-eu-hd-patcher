"""Ingrandisce 4x con xBRZ (lo stesso algoritmo dello shader 4xBRZ di PPSSPP, che a risoluzione 4x/Auto non e' attivo)
tutte le texture di UNC_DIR (PNG RGBA) e scrive OUT_DIR + OUT.ini.  usage: xbrz_pack.py UNC_DIR XBRZ_DLL OUT_DIR OUT_INI"""
import ctypes, os, sys, numpy as np
from PIL import Image
unc, dll, out, ini = sys.argv[1:5]
d = ctypes.CDLL(dll); os.makedirs(out, exist_ok=True); lines = []
for f in sorted(os.listdir(unc)):
    if not f.endswith('.png'): continue
    h = f[:-4]; a = np.ascontiguousarray(np.asarray(Image.open(f'{unc}/{f}').convert('RGBA')))
    H, W = a.shape[:2]; s = a.view(np.uint32).reshape(H, W); t = np.zeros((H * 4, W * 4), np.uint32)
    d.xbrz_scale_defaults(ctypes.c_size_t(4), s.ctypes.data_as(ctypes.c_void_p), t.ctypes.data_as(ctypes.c_void_p), W, H, 2)
    Image.fromarray(t.view(np.uint8).reshape(H * 4, W * 4, 4), 'RGBA').save(f'{out}/{h}.png', compress_level=6)
    lines.append(f'0000000000000000{h} = upscale_extra/{h}.png')
open(ini, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n'); print(len(lines))
