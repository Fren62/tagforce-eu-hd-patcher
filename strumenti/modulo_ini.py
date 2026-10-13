"""Aggiunge a un textures.ini di ULES00600 la localizzazione di una o più lingue: le carte piccole e grandi di quella lingua
puntano a cards/small_<l> e cards/large_<l> (stessa precedenza di gen_ini.py: se gli stessi pixel esistono in più lingue
vince la prima in 'eifgs'), più i frammenti <l>.ini dei moduli (etichette Magia/Trappola).
usage: modulo_ini.py CARD_DIR INI_IN INI_OUT MODULI_DIR LINGUA [LINGUA ...]     (LINGUA = fr de es it ...)
  CARD_DIR   PSP_GAME/USRDIR/card della ISO (cardh_*.cip, cardm_*.cip)
  MODULI_DIR cartella con una sottocartella per lingua; un file mancante lascia l'immagine inglese."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lingue
from tfcards import card_ids, slots, small_blob, large_blob, large_keys, key

ORDINE = 'eifgs'
CARD = re.compile(r'^(0{8})(0000060[67])([0-9a-f]{8})(\s*=\s*)(cards/(small|large)/([^/]+\.png))\s*$', re.I)


def hash_lingue(card_dir):
    """{lettera lingua: {hash: (tipo, ...)}} per le carte piccole e grandi."""
    arch = {(k, l): open(f'{card_dir}/{k}_{l}.cip', 'rb').read() for k in ('cardh', 'cardm') for l in ORDINE}
    ids = card_ids(arch[('cardm', 'e')])
    out = {l: {} for l in ORDINE}
    for l in ORDINE:
        for cid in ids:
            for s in slots(arch[('cardm', l)], cid):
                if s:
                    out[l][key(0, small_blob(arch[('cardm', l)], s))] = 'small'
            for s in slots(arch[('cardh', l)], cid):
                if s:
                    for h in large_keys(large_blob(arch[('cardh', l)], s), stable=False) + large_keys(large_blob(arch[('cardh', l)], s)):
                        out[l][h] = 'large'
    return out


def main(card_dir, ini_in, ini_out, moduli, codici):
    ore = hash_lingue(card_dir)
    lettera = {c: lingue.LINGUE[c][1] for c in codici}
    proprietario = {}
    for l in ORDINE:                      # il primo che ha l'hash lo possiede
        for h in ore[l]:
            proprietario.setdefault(h, l)
    cambi = {c: 0 for c in codici}
    righe = []
    for riga in open(ini_in, encoding='utf-8', errors='ignore').read().split('\n'):
        m = CARD.match(riga.rstrip('\r'))
        if m:
            h = m.group(3).lower()
            for c in codici:
                if proprietario.get(h) == lettera[c] and m.group(6).lower() == ore[lettera[c]].get(h, ''):
                    alt = f'cards/{m.group(6).lower()}_{c}/{m.group(7)}'
                    if os.path.exists(os.path.join(moduli, c, alt)):
                        riga = f'{m.group(1)}{m.group(2)}{h}{m.group(4)}{alt}'
                        cambi[c] += 1
                    break
        righe.append(riga)
    # un frammento sostituisce le righe esistenti con lo stesso hash (es. la striscia dell'etichetta ingrandita con xBRZ)
    chiavi = set()
    for c in codici:
        frm = os.path.join(moduli, c, f'{c}.ini')
        if os.path.exists(frm):
            chiavi |= {m.group(1).lower() for m in re.finditer(r'^([0-9a-fA-F]{24})\s*=', open(frm, encoding='utf-8').read(), re.M)}
    righe = [r for r in righe if not (re.match(r'^[0-9a-fA-F]{24}\s*=', r) and r[:24].lower() in chiavi)]
    testo = '\n'.join(righe)
    if not testo.endswith('\n'):
        testo += '\n'
    gia = set()
    for c in codici:
        frm = os.path.join(moduli, c, f'{c}.ini')
        if os.path.exists(frm):
            for r in open(frm, encoding='utf-8').read().split('\n'):   # la stessa chiave in piu' lingue (es. atlante delle miniature): vince la prima
                k = r[:24].lower() if re.match(r'^[0-9a-fA-F]{24}\s*=', r) else None
                if k and k in gia:
                    continue
                if k:
                    gia.add(k)
                testo += r + '\n' if r else ''
    open(ini_out, 'w', encoding='utf-8', newline='\n').write(testo)
    print('righe carte localizzate:', cambi)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
