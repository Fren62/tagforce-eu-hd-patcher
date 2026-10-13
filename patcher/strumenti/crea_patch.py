"""Crea il pacchetto di patch di una lingua (patch_<l>.tfp) confrontando la ISO originale con la ISO finale di quella lingua.

uso: crea_patch.py ISO_ORIGINALE ISO_FINALE LINGUA OUT.tfp
ISO_FINALE = applica_iso.py ORIG X LINGUA  +  una_lingua_iso.py X FINALE LINGUA.

Il .tfp e' uno zip: patch.json + blobs/NNN. Per ogni file della ISO la patch dice cosa fare (per percorso):
  delta  : applicare un bsdiff (formato BSDIFF40) a un file della ISO originale (src) -> nessun dato del gioco nel pacchetto
  new    : contenuto intero (solo file senza controparte)
  link   : la voce di directory punta agli stessi dati di un'altra voce (hard link ISO9660)
Ogni voce ha sha256 e dimensione del risultato. L'ordine delle voci e' quello di applicazione (i link dopo i dati).
"""
import hashlib, json, os, sys, zipfile
import bsdiff4
import pycdlib

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'strumenti', 'correzioni'))
from una_lingua_iso import tutti


def apri(p):
    iso = pycdlib.PyCdlib()
    iso.open(p)
    iso.interchange_level = 4
    return iso


def leggi(iso, p):
    import io
    b = io.BytesIO()
    iso.get_file_from_iso_fp(b, iso_path=p)
    return b.getvalue()


def extent(iso, p):
    return iso.get_record(iso_path=p).extent_location()


def md5_file(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 22), b''):
            h.update(c)
    return h.hexdigest()


def main(orig_p, fin_p, lingua, out):
    o, f = apri(orig_p), apri(fin_p)
    po, pf = set(tutti(o)), tutti(f)
    ho = {}                                                    # percorso -> sha256 originale (calcolato a richiesta)
    cache_o = {}

    def orig(p):
        if p not in cache_o:
            cache_o[p] = leggi(o, p)
        return cache_o[p]

    def sha(b):
        return hashlib.sha256(b).hexdigest()

    gruppi = {}                                                # extent finale -> percorsi
    for p in pf:
        gruppi.setdefault(extent(f, p), []).append(p)
    dati, link = [], []
    for ext, membri in sorted(gruppi.items()):
        membri.sort()
        fin = leggi(f, membri[0])
        h = sha(fin)
        # membri che nella ISO originale hanno gia' questi dati: nulla da fare per loro
        invariati = [p for p in membri if p in po and sha(orig(p)) == h]
        da_fare = [p for p in membri if p not in invariati]
        if not da_fare:
            continue
        if invariati:
            canon, src = invariati[0], None
            for p in da_fare:
                link.append(dict(op='link', path=p, target=canon))
            continue
        # nessuno ha gia' i dati: se ne spedisce uno (delta contro l'originale di dimensione piu' vicina)
        cand = [p for p in membri if p in po]
        canon = min(cand, key=lambda p: (abs(len(orig(p)) - len(fin)), p)) if cand else membri[0]
        voce = dict(op='delta' if cand else 'new', path=canon, size=len(fin), sha256=h)
        if cand:
            voce['src'] = canon
            voce['blob'] = bsdiff4.diff(orig(canon), fin)
        else:
            voce['blob'] = fin
        dati.append(voce)
        for p in membri:
            if p != canon:
                link.append(dict(op='link', path=p, target=canon))
    voci = dati + link
    sz = os.path.getsize(orig_p)
    meta = dict(formato=1, lingua=lingua, iso_size=sz, iso_md5=md5_file(orig_p), voci=[])
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for i, v in enumerate(voci):
            b = v.pop('blob', None)
            if b is not None:
                v['blob'] = f'blobs/{i:04d}'
                z.writestr(v['blob'], b)
            meta['voci'].append(v)
        z.writestr('patch.json', json.dumps(meta, indent=1))
    print(f'{len(dati)} dati, {len(link)} link -> {out} ({os.path.getsize(out) >> 10} KB)')


if __name__ == '__main__':
    main(*sys.argv[1:5])
