"""Crea una COPIA della ISO con i testi delle carte corretti (nomi e descrizioni mostrati dal gioco stesso), per ogni lingua
che ha una tabella di correzioni (it: dati/correzioni_carte.json; fr, de, es, en: dati/correzioni_carte_<lingua>.json).
usage: applica_iso.py ISO_ORIGINALE ISO_CORRETTA [LINGUA ...]       (l'originale non viene mai modificato; senza lingue: tutte)
Riscrive duelsys/cardinfo_<lingua>.ehp (CARD_Name_X.bin, CARD_Desc_X.bin, CARD_Indx_X.bin). Richiede: pip install pycdlib."""
import io, os, struct, sys
import pycdlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import applica
import lingue


def ehp_di(lingua):
    return f'/PSP_GAME/USRDIR/duelsys/cardinfo_{lingue.LINGUE[lingua][0]}.ehp'


def parse(d):
    _, total, _, n = struct.unpack_from('<IIII', d, 0)
    ents = []
    for i in range(n):
        no, fo = struct.unpack_from('<II', d, 16 + i * 8)
        e = d.index(b'\0', no)
        ents.append(dict(name=d[no:e].decode(), no=no, szpos=e + 1, fo=fo, size=struct.unpack_from('<I', d, e + 1)[0]))
    return ents


def apri(d):
    ents = parse(d)
    return ents, {e['name']: bytearray(d[e['fo']:e['fo'] + e['size']]) for e in ents}


def patch_ehp(d, lingua='it'):
    ents, files = apri(d)
    L = lingue.LINGUE[lingua][2]
    nm, ds, ix, ii = files[f'CARD_Name_{L}.bin'], files[f'CARD_Desc_{L}.bin'], files[f'CARD_Indx_{L}.bin'], files['CARD_IntID.bin']
    tab = applica.tabella(lingua); cambiate = 0

    def leggi(blob, off):
        end = off
        while blob[end:end + 2] != b'\0\0':
            end += 2
        return blob[off:end].decode('utf-16-le')

    cambi = {}                                                    # (campo, indice) -> testo nuovo
    for cid, c in sorted(tab.items()):
        idx = struct.unpack_from('<H', ii, (cid - 4000) * 2)[0]
        if not idx:
            continue
        no, do = struct.unpack_from('<II', ix, idx * 8)
        for campo, blob, off in (('name', nm, no), ('desc', ds, do)):
            if campo in c and leggi(blob, off) != c[campo]:
                cambi[(campo, idx)] = c[campo]
    cambiate = len(cambi)
    # Il gioco ricava la lunghezza di ogni testo dagli offset successivi dell'indice: i blocchi vanno quindi riscritti
    # nello stesso ordine dell'indice (stringhe a 4 byte, offset crescenti, ultima voce = fine del blocco). Accodare
    # i testi nuovi in fondo rompeva l'ordine e mandava il gioco in crash nel Main Deck.
    n = len(ix) // 8
    for campo, blob, pos in (('name', nm, 0), ('desc', ds, 4)):
        offs = [struct.unpack_from('<II', ix, i * 8)[pos // 4] for i in range(n)]
        assert offs == sorted(offs), 'indice originale non ordinato'
        nuovo = bytearray(blob[:offs[0]])
        for i, off in enumerate(offs):
            if off >= len(blob):                                  # voce di chiusura
                new_off = len(nuovo)
            else:
                end = off
                while blob[end:end + 2] != b'\0\0':
                    end += 2
                testo = cambi[(campo, i)].encode('utf-16-le') if (campo, i) in cambi else bytes(blob[off:end])
                new_off = len(nuovo)
                nuovo += testo + b'\0\0'
                nuovo += b'\0' * (-len(nuovo) % 4)
            struct.pack_into('<I', ix, i * 8 + pos, new_off)
        blob[:] = nuovo
        o2 = [struct.unpack_from('<II', ix, i * 8)[pos // 4] for i in range(n)]
        assert o2 == sorted(o2) and o2[-1] == len(blob), 'indice non coerente'
    return chiudi(d, ents, files), cambiate


def chiudi(d, ents, files):
    # ricostruisce l'archivio: stessa tabella, file allineati a 16 byte, dimensioni nuove
    out = bytearray(d[:ents[0]['fo']])
    for e in ents:
        out += b'\0' * (-len(out) % 16)
        struct.pack_into('<I', out, e['no'] + 0 if False else 16 + ents.index(e) * 8 + 4, len(out))   # file_off
        struct.pack_into('<I', out, e['szpos'], len(files[e['name']]))                                # size
        out += files[e['name']]
    out += b'\0' * (-len(out) % 16)
    struct.pack_into('<I', out, 4, len(out))
    return bytes(out)


def stringa(blob, indice):
    n, to, do = struct.unpack_from('<III', blob, 0)
    p = do + struct.unpack_from('<I', blob, to + 4 * indice)[0]
    e = p
    while blob[e:e + 2] != b'\0\0':
        e += 2
    return blob[p:e].decode('utf-16-le')


def posizione_stringa(d, membro, indice):
    """(offset della stringa nel file .ehp, stringa) oppure None se l'archivio non ha quella tabella."""
    ents, files = apri(d)
    e = next((x for x in ents if x['name'] == membro), None)
    if e is None:
        return None
    n, to, do = struct.unpack_from('<III', files[membro], 0)
    return e['fo'] + do + struct.unpack_from('<I', files[membro], to + 4 * indice)[0], stringa(files[membro], indice)


def patch_tabella(d, membro, indice, vecchio, nuovo):
    """cambia una stringa di una tabella (n, offset tabella, offset dati, offset UTF-16...) dentro un .ehp: la nuova stringa
    si aggiunge in fondo ai dati e si aggiorna l'offset; la vecchia resta come spazio morto."""
    ents, files = apri(d)
    if membro not in files:
        return None
    blob = files[membro]
    attuale = stringa(blob, indice)
    if attuale != vecchio:
        return None if attuale == nuovo else False
    n, to, do = struct.unpack_from('<III', blob, 0)
    if len(blob) % 2:
        blob.append(0)
    struct.pack_into('<I', blob, to + 4 * indice, len(blob) - do)
    blob += nuovo.encode('utf-16-le') + b'\0\0'
    return chiudi(d, ents, files)


SECT = 2048


def _record(f, lba, nome):
    """cerca nella directory a `lba` il record `nome` (senza ';1', maiuscole ignorate): (posizione del record, lba, lunghezza, e' directory)"""
    f.seek(lba * SECT); dlen = struct.unpack_from('<I', f.read(SECT), 10)[0]
    f.seek(lba * SECT); buf = f.read(dlen)
    pos = 0
    while pos < len(buf):
        n = buf[pos]
        if n == 0:
            pos = (pos // SECT + 1) * SECT; continue
        idl = buf[pos + 32]; ident = buf[pos + 33:pos + 33 + idl].decode('latin-1').split(';')[0]
        if ident.lower() == nome.lower():
            return lba * SECT + pos, struct.unpack_from('<I', buf, pos + 2)[0], struct.unpack_from('<I', buf, pos + 10)[0], bool(buf[pos + 25] & 2)
        pos += n
    raise FileNotFoundError(nome)


def main(src, dst, lingue_scelte=None):
    import fnmatch, json, shutil
    lingue_scelte = lingue_scelte or [l for l in lingue.LINGUE if applica.tabella(l)]
    iso = pycdlib.PyCdlib(); iso.open(src)
    nuovi = {}
    for l in lingue_scelte:
        b = io.BytesIO(); iso.get_file_from_iso_fp(b, iso_path=ehp_di(l)); d = b.getvalue()
        nuovo, cambiate = patch_ehp(d, l)
        nuovi[ehp_di(l)] = (d, nuovo)
        print(f'{os.path.basename(ehp_di(l))}: {len(d)} -> {len(nuovo)} byte, {cambiate} stringhe riscritte')
    import dialoghi   # dialoghi (script/stNN_*_<l>.ehp), per ogni lingua con dati/correzioni_dialoghi_<lingua>.json
    def prendi(p):
        b = io.BytesIO(); iso.get_file_from_iso_fp(b, iso_path=p); return b.getvalue()
    for l in lingue_scelte:
        if not os.path.exists(dialoghi.dati(l)):
            continue
        avvisi = []
        script, n = dialoghi.patch(prendi, avvisi, l)
        nuovi.update(script)
        print(f'dialoghi {l}: {n} righe riscritte, {len(avvisi)} avvisi'); [print('  ', a) for a in avvisi[:20]]
    import frasi_duello   # battute dei personaggi nei duelli (duel/*.ehp), per ogni lingua con una tabella di correzioni
    avvisi = []
    fd, n = frasi_duello.patch(iso, lingue_scelte, avvisi)
    nuovi.update(fd)
    print(f'frasi duello: {n} frasi riscritte in {len(fd)} archivi, {len(avvisi)} avvisi'); [print('  ', x) for x in avvisi[:20]]
    ui = []   # (percorso nella ISO, vecchio archivio, nuovo archivio) per i testi dell'interfaccia
    ftesti = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dati', 'testi_ui.json')
    if os.path.exists(ftesti):
        tutti = []
        def cammina(p):
            for ch in iso.list_children(iso_path=p):
                n = ch.file_identifier().decode()
                if n in ('.', '..'):
                    continue
                full = p.rstrip('/') + '/' + n
                cammina(full) if ch.is_dir() else tutti.append(full.split(';')[0])
        cammina('/')
        per_file = {}
        for r in json.load(open(ftesti, encoding='utf-8')):
            for p in fnmatch.filter(tutti, r['file']):
                per_file.setdefault(p, []).append(r)
        for p, regole in per_file.items():
            b = io.BytesIO(); iso.get_file_from_iso_fp(b, iso_path=p); d0 = b.getvalue()
            for r in regole:
                pos = posizione_stringa(d0, r['membro'], r['indice'])
                if not pos or pos[1] != r['vecchio']:
                    continue
                nb = r['nuovo'].encode('utf-16-le')
                assert len(nb) <= len(r['vecchio'].encode('utf-16-le')), 'il nuovo testo deve essere piu\' corto o uguale'
                ui.append((p, pos[0], r['vecchio'].encode('utf-16-le'), nb))
        print(f'testi interfaccia: {len(ui)} stringhe da riscrivere sul posto')
    # etichetta [CARTA MAGIA]/[CARTA TRAPPOLA] della carta grande nel duello: ogni basic_<regione><lingua>.ehp ha quella inglese
    # (card_spell_trap.gim, hash c2268340) per qualsiasi lingua; la regione europea e' 'b' (basic_bi = Italia). Si mette quella della
    # lingua (la stessa di field/always_<lingua>_<lingua>.ehp, stesso formato e dimensione) in tutti gli archivi di quella lingua
    for cod, (f3, lett, _) in lingue.LINGUE.items():
        if lingue_scelte and cod not in lingue_scelte or cod == 'en':
            continue
        try:
            pa = f'/PSP_GAME/USRDIR/field/always_{f3}_{f3}.ehp'
            bb = io.BytesIO(); iso.get_file_from_iso_fp(bb, iso_path=pa); fa = apri(bb.getvalue())[1]
        except Exception:
            continue
        nuovo_g = bytes(fa['card_spell_trap.gim'])
        for reg in 'bifgsu':
            pb = f'/PSP_GAME/USRDIR/duel/basic_{reg}{lett}.ehp'
            try:
                bb = io.BytesIO(); iso.get_file_from_iso_fp(bb, iso_path=pb); db = bb.getvalue()
            except Exception:
                continue
            eb, fb = apri(db)
            vecchio = bytes(fb['card_spell_trap.gim'])
            if len(vecchio) == len(nuovo_g) and vecchio != nuovo_g:
                fo = next(x['fo'] for x in eb if x['name'] == 'card_spell_trap.gim')
                ui.append((pb, fo, vecchio, nuovo_g))
    # stringhe dell'interfaccia (aiuti, schede dei personaggi, tutorial...) con testo piu' lungo dell'originale: riscrivono l'archivio;
    # le scritture sul posto che riguardano gli stessi archivi vengono fatte li' dentro (altrimenti finirebbero nella copia vecchia)
    import stringhe_ui
    avvisi = []
    ui_regole = json.load(open(ftesti, encoding='utf-8')) if os.path.exists(ftesti) else []
    su, n = stringhe_ui.patch(iso, lingue_scelte, avvisi, ui_regole)
    assert not set(su) & set(nuovi), 'archivio riscritto due volte'
    nuovi.update(su)
    print(f'stringhe interfaccia: {n} stringhe riscritte in {len(su)} archivi, {len(avvisi)} avvisi'); [print('  ', a) for a in avvisi[:30]]
    ui = [u for u in ui if u[0] not in su]
    # testi dentro l'eseguibile (SYSDIR/BOOT.BIN: nomi dei personaggi nella casella del dialogo): dati/testi_boot.json,
    # sostituzione UTF-16 sul posto (il nuovo testo non puo' essere piu' lungo del vecchio: i puntatori non si spostano)
    fboot = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dati', 'testi_boot.json')
    if os.path.exists(fboot):
        bb = io.BytesIO(); iso.get_file_from_iso_fp(bb, iso_path='/PSP_GAME/SYSDIR/BOOT.BIN'); db = bb.getvalue()
        for r in json.load(open(fboot, encoding='utf-8')):
            if lingue_scelte and r['lingua'] not in lingue_scelte:
                continue
            v, nb = r['vecchio'].encode('utf-16-le'), r['nuovo'].encode('utf-16-le')
            assert len(nb) <= len(v), 'il nuovo testo di BOOT.BIN deve essere piu\' corto o uguale'
            pos, i = [], db.find(v)
            while i >= 0:
                pos.append(i); i = db.find(v, i + 1)
            assert len(pos) == 1, f'BOOT.BIN: {r["vecchio"]!r} trovato {len(pos)} volte'
            ui.append(('/PSP_GAME/SYSDIR/BOOT.BIN', pos[0], v, nb))
    print(f'testi interfaccia + etichette: {len(ui)} scritture sul posto')
    iso.close()
    shutil.copyfile(src, dst)
    with open(dst, 'r+b') as f:
        f.seek(16 * SECT + 156); root = struct.unpack('<I', f.read(34)[2:6])[0]
        lavori = [(p, d, nuovo, p) for p, (d, nuovo) in nuovi.items()]
        for EHP, d, nuovo, l in lavori:
            lba = root
            for part in EHP.strip('/').split('/')[:-1]:
                _, lba, _, isdir = _record(f, lba, part); assert isdir
            recpos, old_lba, old_len, _ = _record(f, lba, EHP.rsplit('/', 1)[1])
            assert old_len == len(d), (old_len, len(d))
            f.seek(0, 2); end = f.tell(); end += -end % SECT; new_lba = end // SECT
            f.seek(end); f.write(nuovo); f.write(bytes(-len(nuovo) % SECT))
            total = f.tell() // SECT
            f.seek(recpos + 2); f.write(struct.pack('<I', new_lba) + struct.pack('>I', new_lba))        # extent (little + big endian)
            f.seek(recpos + 10); f.write(struct.pack('<I', len(nuovo)) + struct.pack('>I', len(nuovo)))  # lunghezza
            f.seek(16 * SECT + 80); f.write(struct.pack('<I', total) + struct.pack('>I', total))         # dimensione volume
            print(l, ': nuovo archivio al settore', new_lba)
    with open(dst, 'r+b') as f:   # testi dell'interfaccia: scritti sul posto, il resto del file e la ISO non cambiano di dimensione
        for p, rel, vecchio, nuovo in ui:
            lba = root
            for part in p.strip('/').split('/')[:-1]:
                _, lba, _, isdir = _record(f, lba, part)
            _, flba, _, _ = _record(f, lba, p.rsplit('/', 1)[1])
            f.seek(flba * SECT + rel)
            assert f.read(len(vecchio)) == vecchio, p
            f.seek(flba * SECT + rel)
            f.write(nuovo + b'\0' * (len(vecchio) - len(nuovo)))
    print('scritto', dst, os.path.getsize(dst), 'byte')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3:] or None)
