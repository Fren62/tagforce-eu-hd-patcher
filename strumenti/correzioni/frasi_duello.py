"""Corregge le battute dei personaggi nei duelli (chr_wordstbl_<l>.bin / 02chr_wordstbl_<l>.bin dentro duel/*.ehp) con
dati/correzioni_frasi_duello_<lingua>.json:  {"esatte": {frase: nuova}, "parti": [[vecchio, nuovo], ...]}   (a capo scritti ⏎).
Le "esatte" valgono solo se la frase e' identica; le "parti" sono sostituzioni di testo su ogni frase."""
import json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import applica_iso as ai
import lingue

DATI = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dati')


def carica(lingua):
    f = os.path.join(DATI, f'correzioni_frasi_duello_{lingua}.json')
    if not os.path.exists(f):
        return None
    c = json.load(open(f, encoding='utf-8'))
    nl = lambda s: s.replace('⏎', '\n')
    return {nl(k): nl(v) for k, v in c.get('esatte', {}).items()}, [(nl(a), nl(b)) for a, b in c.get('parti', [])]


def tabella(d):
    n, to, do = struct.unpack_from('<III', d, 0)
    res = []
    for o in struct.unpack_from(f'<{n}I', d, to):
        p = do + o; e = p
        while e + 1 < len(d) and d[e:e + 2] != b'\0\0':
            e += 2
        res.append(d[p:e].decode('utf-16-le'))
    return res


def scrivi_tabella(testi):
    n = len(testi); off, dati = [], b''
    for t in testi:
        off.append(len(dati)); dati += t.encode('utf-16-le') + b'\0\0'
    if testi and testi[-1] == '':      # l'ultima voce vuota punta alla fine dei dati, senza terminatore proprio
        dati = dati[:-2]
    return struct.pack('<III', n, 12, 12 + 4 * n) + struct.pack(f'<{n}I', *off) + dati


def rimappa_puntatori(ents, files):
    """I file *-ptrs.txt dell'archivio contengono gli offset assoluti dei membri: se una tabella cresce e i membri seguenti
    si spostano, vanno aggiornati (altrimenti il gioco carica dati sbagliati e va in crash)."""
    pos = ents[0]['fo']; nuovo = {}
    for e in ents:
        pos += -pos % 16; nuovo[e['fo']] = pos; pos += len(files[e['name']])
    for k in files:
        if k.endswith('-ptrs.txt') and len(files[k]) % 4 == 0:
            v = struct.unpack(f'<{len(files[k]) // 4}I', bytes(files[k]))
            files[k][:] = struct.pack(f'<{len(v)}I', *[nuovo.get(x, x) for x in v])


def patch(iso, lingue_scelte, avvisi):
    """iso: PyCdlib aperto. Restituisce ({percorso ISO: (originale, nuovo)}, frasi riscritte). Ogni archivio e' riscritto una
    volta sola con le correzioni di tutte le lingue scelte."""
    import io
    regole = {}
    for l in lingue_scelte:
        c = carica(l)
        if c:
            regole[l] = (re.compile(rf'(?:02)?chr_wordstbl_{lingue.LINGUE[l][1]}\.bin$'),) + c
    out, n, usate = {}, 0, set()
    for ch in iso.list_children(iso_path='/PSP_GAME/USRDIR/duel'):
        nome = ch.file_identifier().decode().split(';')[0]
        if not nome.endswith('.ehp') or not regole:
            continue
        p = f'/PSP_GAME/USRDIR/duel/{nome}'
        b = io.BytesIO(); iso.get_file_from_iso_fp(b, iso_path=p); d = b.getvalue()
        try:
            ents, files = ai.apri(d)
        except Exception:
            continue
        toccato = False
        for l, (pat, esatte, parti) in regole.items():
            for m in [k for k in files if pat.match(k)]:
                vecchi = tabella(bytes(files[m])); nuovi = []
                for t in vecchi:
                    u = esatte.get(t, t)
                    for a, b2 in parti:
                        u = u.replace(a, b2)
                    if u != t:
                        n += 1; toccato = True; usate.add((l, t))
                    nuovi.append(u)
                if nuovi != vecchi:
                    files[m] = bytearray(scrivi_tabella(nuovi))
        if toccato:
            rimappa_puntatori(ents, files)
            out[p] = (d, ai.chiudi(d, ents, files))
    for l, (pat, esatte, parti) in regole.items():
        for k in esatte:
            if (l, k) not in usate:
                avvisi.append(f'frasi duello {l}: frase esatta mai trovata: {k[:50]!r}')
    return out, n
