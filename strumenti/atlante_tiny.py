"""Atlanti delle miniature del deck (cards/tinyMikeyMK/<a>_<b>.png, 2048x2048): ogni pagina e' una griglia 23x17 di celle
88x120 con una carta verticale ciascuna (nella prima pagina la prima cella e' il dorso). Le pagine hanno lo stesso hash in tutte
le lingue, quindi senza questo lavoro il gioco italiano/francese/... mostrerebbe i nomi inglesi. Qui si ricostruisce ogni pagina
con le carte piccole HD della lingua (cards/small_<l>): ogni cella e' la carta piccola ridimensionata.
Le pagine non contengono tutte le carte del loro intervallo: l'associazione cella -> carta si ricava confrontando le immagini
inglesi (analizza) e si salva in dati/atlante_tiny.json.
usage: atlante_tiny.py analizza PACK            associa ogni cella alla sua carta (confronto con cards/small)
       atlante_tiny.py genera LINGUA PACK OUT   scrive OUT/cards/tiny_<lingua>/<pagina>.png   (usa OUT/cards/small_<lingua>)"""
import glob, json, os, re, sys
import numpy as np
from PIL import Image

CW, CH, COLS, ROWS = 88, 120, 23, 17
HERE = os.path.dirname(os.path.abspath(__file__))
JSON = os.path.join(HERE, 'dati', 'atlante_tiny.json')


def ncc(a, b):
    a = a - a.mean(); b = b - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))


def pagine(pack, stile='tinyMikeyMK'):
    out = []
    for f in sorted(glob.glob(os.path.join(pack, 'cards', stile, '*.png'))):
        m = re.match(r'(\d+)_(\d+)\.png$', os.path.basename(f))
        if m:
            out.append((int(m.group(1)), int(m.group(2)), f))
    return out


def ids_esistenti(pack):
    return sorted({int(re.match(r'\d+', f).group()) for f in os.listdir(os.path.join(pack, 'cards', 'small')) if re.fullmatch(r'\d+\.png', f)})


def rect(idx):
    return (idx % COLS) * CW, (idx // COLS) * CH


def analizza(pack):
    tutti = ids_esistenti(pack)
    cache = {}

    def modello(cid):
        if cid not in cache:
            cache[cid] = np.asarray(Image.open(os.path.join(pack, 'cards/small', f'{cid}.png')).convert('RGB').resize((CW, CH), Image.LANCZOS)).astype(np.float32)
        return cache[cid]

    res = {}
    for a, b, f in pagine(pack):
        ids = [i for i in tutti if a <= i <= b]
        atlas = np.asarray(Image.open(f).convert('RGB')).astype(np.float32)
        p, celle, dubbie = 0, [], 0
        for idx in range(COLS * ROWS):
            x0, y0 = rect(idx)
            reg = atlas[y0:y0 + CH, x0:x0 + CW]
            if p >= len(ids):
                celle.append(0); continue
            punteggi = [(ncc(reg, modello(ids[q])), q) for q in range(p, min(p + 8, len(ids)))]
            s, q = next(((s, q) for s, q in punteggi if s > 0.9), (None, None))
            if q is None:
                s, q = max(punteggi)
                if s < 0.6:   # dorso o cella non riconosciuta (es. altra arte): non consuma carte
                    if idx == 0 and a == 4007:
                        celle.append(0); continue
                    q, dubbie = p, dubbie + 1
            celle.append(ids[q])
            p = q + 1
        res[os.path.basename(f)] = celle
        usate = sum(1 for c in celle if c)
        print(os.path.basename(f), 'carte nell\'intervallo', len(ids), 'celle assegnate', usate, 'non riconosciute (assegnate in ordine)', dubbie, flush=True)
    return res


def genera(lingua, pack, out):
    geo = json.load(open(JSON))
    dst = os.path.join(out, 'cards', f'tiny_{lingua}')
    os.makedirs(dst, exist_ok=True)
    for a, b, f in pagine(pack):
        atlas = Image.open(f).convert('RGBA')
        n = 0
        for idx, cid in enumerate(geo[os.path.basename(f)]):
            if not cid:
                continue
            sm = os.path.join(out, 'cards', f'small_{lingua}', f'{cid}.png')
            if not os.path.exists(sm):
                sm = os.path.join(pack, 'cards', f'small_{lingua}', f'{cid}.png')
            if not os.path.exists(sm):
                continue
            atlas.paste(Image.open(sm).convert('RGBA').resize((CW, CH), Image.LANCZOS), rect(idx))
            n += 1
        atlas.save(os.path.join(dst, os.path.basename(f)))
        print(os.path.basename(f), n, 'celle', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'analizza':
        json.dump(analizza(sys.argv[2]), open(JSON, 'w'))
    else:
        genera(sys.argv[2], sys.argv[3], sys.argv[4])
