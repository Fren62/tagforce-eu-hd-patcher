"""Texture dei numeri del gioco (icon03.gim, 128x128): nel pack di MikeyMK (ui/duels/numbers.png, 512x512) le cifre grandi e
le icone sono ridisegnate, ma le righe di simboli, le cifre piccole, "x1 ... x12" (il moltiplicatore di livello nella lista del deck)
sono solo ingrandite a gradini (nearest). Qui quelle fasce sono ricostruite dall'originale a 128 px con un
ingrandimento levigato (bicubico sui colori premoltiplicati + bordo dell'alfa riaffilato), nelle stesse posizioni.
usage: numeri_hd.py ALL_I.ehp PACK_BASE OUT_PNG      (PACK_BASE contiene ui/duels/numbers.png; ALL_I.ehp = USRDIR/deck/all_i.ehp)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
from PIL import Image
from ehp import read
import gim
import cv2

# fasce (y0, y1) nella texture 512x512 che sono solo ingrandite a gradini
FASCE = [(0, 36), (36, 70), (146, 184), (180, 224), (224, 264)]   # le icone a barre/frecce (266-328) restano com'erano: levigate si gonfiano


def liscia(rgba, k=4, lo=0.30, hi=0.62):
    """ingrandimento levigato di un'immagine RGBA a pixel grossi: colori premoltiplicati bicubici, alfa con bordo riaffilato."""
    a = np.asarray(rgba, np.float32) / 255
    pm = a.copy(); pm[..., :3] *= a[..., 3:4]
    big = cv2.resize(pm, (a.shape[1] * k, a.shape[0] * k), interpolation=cv2.INTER_CUBIC)
    al = cv2.GaussianBlur(np.clip(big[..., 3], 0, 1), (0, 0), 0.6)
    t = np.clip((al - lo) / (hi - lo), 0, 1)
    al2 = t * t * (3 - 2 * t)                                        # smoothstep: bordi netti ma senza gradini
    col = np.clip(big[..., :3] / np.maximum(big[..., 3:4], 1e-3), 0, 1)
    return np.dstack([col, al2])


def main(all_i, pack, out):
    low = gim.to_png(gim.parse(read(all_i)['icon03.gim'])).convert('RGBA')
    base = Image.open(os.path.join(pack, 'ui/duels/numbers.png')).convert('RGBA')
    assert low.size == (128, 128) and base.size == (512, 512)
    res = np.asarray(base).astype(np.float32) / 255
    sm = liscia(low)
    # il gioco ritaglia ogni simbolo con un rettangolo preciso: l'inchiostro levigato non deve uscire dall'impronta dell'originale
    # (prima il bordo del "6" saliva di 1-3 px e veniva tagliato piatto): fuori dall'impronta l'alfa e' 0, dentro sfuma in 1,5 px
    fp = (np.asarray(low.resize((512, 512), Image.NEAREST))[..., 3] > 0).astype(np.uint8)
    dist = cv2.distanceTransform(fp, cv2.DIST_L2, 3)
    sm[..., 3] *= np.clip((dist - 0.5) / 1.5, 0, 1)
    # righe "x1...x6" e "x7...x12": il gioco ritaglia ogni simbolo dalla prima riga di inchiostro forte dell'originale (le righe 46 e 57 a
    # bassa risoluzione); l'ingrandimento levigato saliva di una riga sopra e la cima (la coda del 6) veniva tagliata piatta.
    # Si azzera tutto sopra quella riga e si sfuma nei primi 10 px, cosi' la cima resta arrotondata.
    for (y0, y1), top in (((180, 224), 184), ((224, 264), 228)):
        sm[y0:top, :, 3] = 0
        t = np.clip((np.arange(top, top + 10) - top + 1) / 11.0, 0, 1)
        sm[top:top + 10, :, 3] *= (t * t * (3 - 2 * t))[:, None]
    for y0, y1 in FASCE:
        res[y0:y1] = sm[y0:y1]
    Image.fromarray((res * 255).round().astype(np.uint8)).save(out)
    print('scritto', out)


if __name__ == '__main__':
    main(*sys.argv[1:4])
