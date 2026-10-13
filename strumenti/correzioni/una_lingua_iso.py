"""Tiene una sola lingua nella ISO di Tag Force 1 EU (ULES00600) e ne riduce la dimensione.

I file delle altre lingue non vengono cancellati (il gioco li apre per nome in base alla lingua di sistema del PSP):
le loro voci di directory diventano hard link ISO9660 ai dati della lingua scelta, quindi il gioco resta nella lingua
scelta qualunque sia la lingua di sistema, e i dati non scelti non vengono piu' scritti nella ISO.

uso: una_lingua_iso.py ISO_IN ISO_OUT LINGUA        (LINGUA = it fr de es en)
Richiede pycdlib. Tutti i percorsi sono quelli dell'ISO originale; i nomi non elencati restano invariati.
"""
import os, re, sys
import pycdlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
import lingue

SUFF1 = {'it': 'i', 'fr': 'f', 'de': 'g', 'es': 's', 'en': 'e'}   # suffisso a una lettera (j = giapponese: va sempre sulla lingua scelta)
USR = '/PSP_GAME/USRDIR/'


def tutti(iso):
    out = []

    def walk(p):
        for c in iso.list_children(iso_path=p):
            n = c.file_identifier()
            if n in (b'.', b'..'):
                continue
            n = n.decode()
            if c.is_dir():
                walk(p.rstrip('/') + '/' + n)
            else:
                out.append(p.rstrip('/') + '/' + n)
    walk('/')
    return out


def piano(files, lingua):
    """[(file da sostituire, file della lingua scelta)] per tutti i file che dipendono dalla lingua."""
    l1, l3 = SUFF1[lingua], lingue.LINGUE[lingua][0]
    insieme = set(files)
    voci = []
    for f in files:
        d, n = f.rsplit('/', 1)
        base = n
        if base.startswith('opening_'):   # gestito sotto
            continue
        m = re.match(r'^(.*)_([efgsij])\.(\w+)$', base)          # nome_<lettera>.ext
        if m and m.group(2) != l1:
            voci.append((f, f'{d}/{m.group(1)}_{l1}.{m.group(3)}'))
            continue
        m = re.match(r'^(cardinfo)_(eng|fra|ger|spa|ita)\.(\w+)$', base)   # cardinfo_<lingua>.ehp
        if m and m.group(2) != l3:
            voci.append((f, f'{d}/{m.group(1)}_{l3}.{m.group(3)}'))
            continue
        m = re.match(r'^always_(bri|fra|ger|ita|spa|usa)_(eng|fra|ger|spa|ita)\.ehp$', base)   # field/always_<paese>_<lingua>.ehp
        paese = 'bri' if lingua == 'en' else l3          # per l'inglese non esiste always_eng_eng: la versione europea usa il Regno Unito
        if m and (m.group(1), m.group(2)) != (paese, l3):
            voci.append((f, f'{d}/always_{paese}_{l3}.ehp'))
    # filmato iniziale: opening_f.pmf e' solo francese, opening_a.pmf e' per tutti gli altri
    a, f_ = USR + 'movie/opening_a.pmf', USR + 'movie/opening_f.pmf'
    if a in insieme and f_ in insieme:
        voci.append((a, f_) if lingua == 'fr' else (f_, a))
    for vecchio, nuovo in voci:
        assert nuovo in insieme, f'manca {nuovo}'
    return voci


def main(src, dst, lingua):
    iso = pycdlib.PyCdlib()
    iso.open(src)
    iso.interchange_level = 4   # i nomi della ISO sono minuscoli e senza ';1': pycdlib altrimenti rifiuta i nuovi hard link
    voci = piano(tutti(iso), lingua)
    for vecchio, nuovo in voci:
        iso.rm_file(iso_path=vecchio)
        iso.add_hard_link(iso_old_path=nuovo, iso_new_path=vecchio)
    iso.write(dst)
    iso.close()
    print(f'{len(voci)} file ricollegati; {os.path.getsize(src) >> 20} MB -> {os.path.getsize(dst) >> 20} MB')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
