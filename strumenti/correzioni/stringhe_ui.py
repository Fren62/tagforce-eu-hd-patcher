"""Corregge le stringhe dell'interfaccia (tabelle strTbl*, help_strtbl_*, ddstrtbl_*, field_strtbl* dentro i .ehp della ISO) anche
quando il testo nuovo e' piu' lungo dell'originale: la tabella viene riscritta per intero e l'archivio finisce in fondo alla ISO
(come per i dialoghi e le battute dei duelli).
Regole per lingua: correzioni/regole_stringhe_<lingua>.py con
  STRINGHE  [(archivio, membro, indice, [(vecchio, nuovo), ...], motivo)]   archivio = percorso sotto /PSP_GAME/USRDIR (anche con * ?)
  GLOBALI   [(regex, sostituzione, motivo)]                                   applicate a tutte le stringhe delle TABELLE
  TABELLE   [(archivio, membro)]                                              tabelle a cui si applicano i GLOBALI
Gli archivi riscritti qui NON ricevono le scritture sul posto di testi_ui.json: le voci di testi_ui.json che li riguardano e
l'etichetta [CARTA MAGIA]/[CARTA TRAPPOLA] dei basic_<regione><lingua>.ehp vengono applicate qui dentro."""
import fnmatch, importlib.util, io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import applica_iso as ai
import frasi_duello as fd
import lingue

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = '/PSP_GAME/USRDIR/'


def regole(lingua):
    f = os.path.join(QUI, f'regole_stringhe_{lingua}.py')
    if not os.path.exists(f):
        return None
    spec = importlib.util.spec_from_file_location(f'regole_stringhe_{lingua}', f)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def tutti_i_percorsi(iso):
    res = []
    def cammina(p):
        for ch in iso.list_children(iso_path=p):
            n = ch.file_identifier().decode()
            if n in ('.', '..'):
                continue
            full = p.rstrip('/') + '/' + n
            cammina(full) if ch.is_dir() else res.append(full.split(';')[0])
    cammina('/')
    return res


def etichetta_gim(iso, percorso, lingue_scelte):
    """nuovo card_spell_trap.gim per un basic_<regione><lingua>.ehp (lo stesso di field/always_<lingua>_<lingua>.ehp), o None"""
    m = re.search(r'/duel/basic_[bifgsu]([a-z])\.ehp$', percorso)
    if not m:
        return None
    for cod, (f3, lett, _) in lingue.LINGUE.items():
        if lett != m.group(1) or cod == 'en' or (lingue_scelte and cod not in lingue_scelte):
            continue
        try:
            bb = io.BytesIO(); iso.get_file_from_iso_fp(bb, iso_path=f'{RADICE}field/always_{f3}_{f3}.ehp')
            return bytes(ai.apri(bb.getvalue())[1]['card_spell_trap.gim'])
        except Exception:
            return None
    return None


def patch(iso, lingue_scelte, avvisi, ui_regole=()):
    """iso: PyCdlib aperto. Restituisce ({percorso ISO: (originale, nuovo)}, stringhe riscritte)."""
    tutti = tutti_i_percorsi(iso)
    per_file = {}      # percorso -> {'str': [(membro, indice, parti, motivo)], 'glob': [(regex, sost)] per membro, 'ui': [...]}
    for l in lingue_scelte:
        R = regole(l)
        if not R:
            continue
        for arc, mem, idx, parti, motivo in R.STRINGHE:
            trovati = fnmatch.filter(tutti, RADICE + arc)
            if not trovati:
                avvisi.append(f'stringhe {l}: archivio non trovato {arc}')
            for p in trovati:
                per_file.setdefault(p, {'str': [], 'glob': {}, 'ui': []})['str'].append((mem, idx, parti, motivo, l))
        for arc, mem in R.TABELLE:
            for p in fnmatch.filter(tutti, RADICE + arc):
                d = per_file.setdefault(p, {'str': [], 'glob': {}, 'ui': []})
                d['glob'].setdefault(mem, []).extend((re.compile(rx), rep) for rx, rep, _ in R.GLOBALI)
    out, n = {}, 0
    for p, ric in sorted(per_file.items()):
        for r in ui_regole:
            if fnmatch.fnmatch(p, r['file']):
                ric['ui'].append(r)
        b = io.BytesIO(); iso.get_file_from_iso_fp(b, iso_path=p); d = b.getvalue()
        ents, files = ai.apri(d)
        tabelle = {}
        def tab(mem):
            if mem not in tabelle:
                tabelle[mem] = fd.tabella(bytes(files[mem])) if mem in files else None
            return tabelle[mem]
        modificati = set()
        for mem, idx, parti, motivo, l in ric['str']:
            t = tab(mem)
            if t is None or idx >= len(t):
                avvisi.append(f'stringhe {l}: {p} {mem} #{idx}: voce non trovata')
                continue
            s = t[idx]
            for vecchio, nuovo in parti:
                if vecchio not in s:
                    avvisi.append(f'stringhe {l}: {p} {mem} #{idx}: testo non trovato {vecchio[:40]!r}')
                    continue
                s = s.replace(vecchio, nuovo)
            if s != t[idx]:
                t[idx] = s; modificati.add(mem); n += 1
        for mem, subs in ric['glob'].items():
            t = tab(mem)
            if t is None:
                avvisi.append(f'stringhe: {p} non ha {mem}')
                continue
            for i, s in enumerate(t):
                u = s
                for rx, rep in subs:
                    u = rx.sub(rep, u)
                if u != s:
                    t[i] = u; modificati.add(mem); n += 1
        for r in ric['ui']:                    # voci di testi_ui.json che il resto del programma scriverebbe sul posto
            t = tab(r['membro'])
            if t is not None and r['indice'] < len(t) and t[r['indice']] == r['vecchio']:
                t[r['indice']] = r['nuovo']; modificati.add(r['membro'])
        for mem in modificati:
            files[mem] = bytearray(fd.scrivi_tabella(tabelle[mem]))
        g = etichetta_gim(iso, p, lingue_scelte)
        if g is not None and 'card_spell_trap.gim' in files and len(files['card_spell_trap.gim']) == len(g) and bytes(files['card_spell_trap.gim']) != g:
            files['card_spell_trap.gim'] = bytearray(g); modificati.add('card_spell_trap.gim')
        if modificati:
            fd.rimappa_puntatori(ents, files)
            out[p] = (d, ai.chiudi(d, ents, files))
    return out, n
