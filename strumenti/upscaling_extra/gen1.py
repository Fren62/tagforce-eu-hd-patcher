"""Rigenera singole texture AI con controllo qualita': gen1.py LISTA.json USCITA_DIR
Per ogni hash: RGB (trasparenti riempiti dai vicini) -> Real-ESRGAN animevideov3 x4 -> alpha Lanczos a parte.
Riprova con tile diversi se l'errore rispetto all'originale rimpicciolito e' alto."""
import os, sys, json, shutil, subprocess, numpy as np, cv2
from PIL import Image
T = os.environ['TEMP']; E = T + '/resr/x/realesrgan-ncnn-vulkan.exe'
W = T + '/g1'; os.makedirs(W, exist_ok=True)


def fill_rgb(a):
    rgb = a[..., :3].copy(); m = (a[..., 3] > 0).astype(np.uint8)
    k = np.ones((3, 3), np.float32)
    for _ in range(64):
        if m.all(): break
        cnt = cv2.filter2D(m.astype(np.float32), -1, k, borderType=cv2.BORDER_REPLICATE)
        sm = cv2.filter2D((rgb * m[..., None]).astype(np.float32), -1, k, borderType=cv2.BORDER_REPLICATE)
        sel = (m == 0) & (cnt > 0)
        rgb[sel] = (sm / np.maximum(cnt[..., None], 1)).astype(np.uint8)[sel]; m = (m | sel).astype(np.uint8)
    return rgb


def err(o, u):
    d = np.asarray(Image.fromarray(u).resize((o.shape[1], o.shape[0]), Image.BOX))
    m = (o[..., 3] > 200) & (d[..., 3] > 200)
    if m.sum() < 4: return 0.0
    lab = lambda x: cv2.cvtColor(x[..., :3].astype(np.uint8), cv2.COLOR_RGB2LAB).astype(np.float32)
    return float(np.abs(lab(o) - lab(d)).sum(-1)[m].mean())


def gen(h, tiles=(0, 64, 32, 128)):
    o = np.asarray(Image.open(f'{T}/unc/{h}.png').convert('RGBA')); H, Wd = o.shape[:2]
    src = f'{W}/{h}.png'; Image.fromarray(fill_rgb(o), 'RGB').save(src)
    al = cv2.resize(o[..., 3], (Wd * 4, H * 4), interpolation=cv2.INTER_LANCZOS4)
    best = None
    for t in tiles:
        out = f'{W}/{h}_o.png'
        if os.path.exists(out): os.remove(out)
        subprocess.run([E, '-i', src, '-o', out, '-n', 'realesr-animevideov3', '-s', '4', '-t', str(t), '-j', '1:1:1'],
                       capture_output=True, cwd=T + '/resr/x')
        if not os.path.exists(out): continue
        u = np.dstack([np.asarray(Image.open(out).convert('RGB')), al])
        e = err(o, u)
        if best is None or e < best[0]: best = (e, u)
        if e < 22: break
    return best


if __name__ == '__main__':
    hs = json.load(open(sys.argv[1])); outd = sys.argv[2]; os.makedirs(outd, exist_ok=True); rep = {}
    for h in hs:
        b = gen(h)
        if b: Image.fromarray(b[1], 'RGBA').save(f'{outd}/{h}.png'); rep[h] = round(b[0], 1)
    json.dump(rep, open(outd + '/_err.json', 'w'))
    print(len(rep), 'ok', sum(1 for v in rep.values() if v >= 22), 'ancora alti')
