"""Crea la patch MODULARE di una lingua (formato 2): patch_<l>.tfp.

uso: crea_patch_modulare.py ISO_ORIGINALE LINGUA OUT.tfp [CARTELLA_TEMP]

Ogni voce ha `needs`: i moduli che devono essere attivi perche' si applichi.
  cards  : correzioni ai nomi e alle descrizioni delle carte
  text   : correzioni ai dialoghi, alle frasi dei duelli, alle stringhe dell'interfaccia
  strip  : toglie le altre lingue dalla ISO, fissa la lingua e toglie selettore e voce di menu (libtitle.prx)
Per ogni file si applica la voce con piu' `needs` tutti attivi (le voci "cards+text" servono ai file toccati da entrambi).
Le voci `link` (solo con `strip`) fanno puntare i file delle altre lingue ai dati della lingua scelta.
Il delta e' sempre contro lo stesso file della ISO originale (nessun dato del gioco nel pacchetto)."""
import hashlib, io, json, os, subprocess, sys, zipfile
import bsdiff4
import pycdlib

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.join(QUI, '..', '..')
sys.path.insert(0, os.path.join(RADICE, 'strumenti', 'correzioni'))
sys.path.insert(0, QUI)
from una_lingua_iso import tutti, piano
import salta_lingua


def apri(p):
    iso = pycdlib.PyCdlib(); iso.open(p); iso.interchange_level = 4
    return iso


def leggi(iso, p):
    b = io.BytesIO(); iso.get_file_from_iso_fp(b, iso_path=p); return b.getvalue()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def md5_file(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 22), b''):
            h.update(c)
    return h.hexdigest()


def hash_iso(p):
    iso = apri(p)
    out = {f: sha(leggi(iso, f)) for f in tutti(iso)}
    iso.close()
    return out


def main(orig, lingua, out, tmp=None):
    tmp = tmp or os.path.join(RADICE, 'patcher', 'build', 'mod_tmp')
    os.makedirs(tmp, exist_ok=True)
    isos = {}
    for nome, parti in (('c', 'carte'), ('t', 'testi'), ('ct', 'carte,testi')):
        dst = os.path.join(tmp, f'{lingua}_{nome}.iso'); isos[nome] = dst
        subprocess.run([sys.executable, '-X', 'utf8', os.path.join(RADICE, 'strumenti', 'correzioni', 'applica_iso.py'),
                        orig, dst, lingua, f'--parti={parti}'], check=True, capture_output=True,
                       env={**os.environ, 'PYTHONUTF8': '1'})
    ho = hash_iso(orig)
    h = {k: hash_iso(v) for k, v in isos.items()}
    cambiati = {k: {p for p, x in h[k].items() if ho.get(p) != x} for k in h}
    print({k: len(v) for k, v in cambiati.items()}, 'file cambiati (c, t, ct)')

    iso_o = apri(orig)
    iso_x = {k: apri(v) for k, v in isos.items()}
    voci, blobs = [], []

    def aggiungi(path, needs, sorgente):
        vecchio = leggi(iso_o, path); nuovo = leggi(iso_x[sorgente], path)
        voci.append(dict(op='delta', path=path, src=path, needs=needs, size=len(nuovo), sha256=sha(nuovo)))
        blobs.append(bsdiff4.diff(vecchio, nuovo))

    for p in sorted(cambiati['c']):
        aggiungi(p, ['cards'], 'c')
    for p in sorted(cambiati['t']):
        aggiungi(p, ['text'], 't')
    for p in sorted(cambiati['ct']):
        solo_c, solo_t = p in cambiati['c'], p in cambiati['t']
        if (solo_c and solo_t) or (solo_c and h['ct'][p] != h['c'][p]) or (solo_t and h['ct'][p] != h['t'][p]) or not (solo_c or solo_t):
            aggiungi(p, ['cards', 'text'], 'ct')
    # libtitle: selettore lingua e voce di menu tolti, lingua fissa (solo con strip)
    PRX = '/PSP_GAME/USRDIR/gmodule/libtitle.prx'
    vecchio = leggi(iso_o, PRX)
    nuovo = bytes(salta_lingua.patch(bytearray(vecchio), lingua))
    voci.append(dict(op='delta', path=PRX, src=PRX, needs=['strip'], size=len(nuovo), sha256=sha(nuovo)))
    blobs.append(bsdiff4.diff(vecchio, nuovo))
    # altre lingue: i loro file puntano a quelli della lingua scelta
    for vecchio_p, nuovo_p in piano(tutti(iso_o), lingua):
        voci.append(dict(op='link', path=vecchio_p, target=nuovo_p, needs=['strip']))
    for k in iso_x.values():
        k.close()
    iso_o.close()
    meta = dict(formato=2, lingua=lingua, iso_size=os.path.getsize(orig), iso_md5=md5_file(orig), voci=[])
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        bi = 0
        for v in voci:
            if v['op'] == 'delta':
                v['blob'] = f'blobs/{bi:04d}'; z.writestr(v['blob'], blobs[bi]); bi += 1
            meta['voci'].append(v)
        z.writestr('patch.json', json.dumps(meta, indent=1))
    n = {k: sum(1 for v in voci if v['op'] == 'delta' and v['needs'] == w) for k, w in
         (('cards', ['cards']), ('text', ['text']), ('cards+text', ['cards', 'text']), ('strip', ['strip']))}
    print(f'{lingua}: voci {n}, link {sum(1 for v in voci if v["op"] == "link")} -> {out} ({os.path.getsize(out) >> 10} KB)')
    if not os.environ.get('TFP_KEEP'):      # TFP_KEEP=1 tiene le ISO intermedie (per la verifica)
        for v in isos.values():
            os.remove(v)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
