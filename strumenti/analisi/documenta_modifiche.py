"""Confronta la ISO originale con la ISO `_definitiva` e scrive, per UNA lingua, l'elenco COMPLETO di ogni modifica fatta dentro la ISO:
carte, dialoghi, frasi dei duelli, stringhe dell'interfaccia, immagini sostituite nei .ehp, piu' l'elenco dei file della ISO toccati.
E' il documento "cosa e' stato cambiato" derivato dai dati reali (non scritto a mano): rilancialo dopo ogni modifica.

uso: python documenta_modifiche.py ISO_ORIGINALE ISO_DEFINITIVA LINGUA OUT_DIR        LINGUA = it|fr|de|es|en
Scrive in OUT_DIR:  carte.csv, dialoghi.csv, frasi_duello.csv, stringhe_ui.csv, immagini_iso.csv, file_toccati.csv, riepilogo.json
(CSV con separatore `;`, UTF-8 con BOM, a capo scritti ⏎ ; apribili con Excel/LibreOffice)."""
import csv, gzip, io, json, os, re, struct, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'strumenti')); sys.path.insert(0, os.path.join(B, 'strumenti', 'correzioni'))
sys.stdout.reconfigure(encoding='utf-8')
import pycdlib
import applica_iso as ai, frasi_duello as fd, dialoghi, lingue, cardprops, gim

orig_p, def_p, L, out = sys.argv[1:5]
LET = dialoghi.LETTERA[L]
COD = {'e': 'eng', 'f': 'fra', 'g': 'ger', 'i': 'ita', 's': 'spa'}[LET]
os.makedirs(out, exist_ok=True)
A, D = pycdlib.PyCdlib(), pycdlib.PyCdlib(); A.open(orig_p); D.open(def_p)


def leggi(iso, p):
    b = io.BytesIO(); iso.get_file_from_iso_fp(b, iso_path=p); return b.getvalue()


def percorsi(iso):
    res = {}
    def cammina(p):
        for ch in iso.list_children(iso_path=p):
            n = ch.file_identifier().decode()
            if n in ('.', '..'):
                continue
            full = p.rstrip('/') + '/' + n
            if ch.is_dir():
                cammina(full)
            else:
                res[full.split(';')[0]] = ch.get_data_length()
    cammina('/')
    return res


def lingua_di(arch, membro):
    """lingua del TESTO: lettera nel membro (strTbl_i.bin, icon06_f.gim, ScrXXXLi.bin) altrimenti nell'archivio"""
    m = re.search(r'_([efgis])(?:\.|\d)', membro) or re.search(r'[A-Za-z0-9]{3}[IL]([efgis])\.bin', membro)
    if m:
        return m.group(1)
    a = os.path.basename(arch)
    m = re.search(r'basic_[a-z]([efgis])\.ehp$', a) or re.search(r'_([efgis])\.ehp$', a)
    if m:
        return m.group(1)
    m = re.search(r'_(eng|fra|ger|ita|spa)\.ehp$', a)
    if m:
        return {'eng': 'e', 'fra': 'f', 'ger': 'g', 'ita': 'i', 'spa': 's'}[m.group(1)]
    return '-'


def tab_ok(d):
    try:
        t = fd.tabella(d)
        return t if t else None
    except Exception:
        return None


pa, pd = percorsi(A), percorsi(D)
toccati = []
for p in sorted(set(pa) | set(pd)):
    if p not in pa or p not in pd:
        toccati.append((p, 'aggiunto' if p in pd else 'rimosso', pa.get(p, 0), pd.get(p, 0))); continue
    if not p.endswith('.ehp'):
        continue
    if pa[p] != pd[p] or leggi(A, p) != leggi(D, p):
        toccati.append((p, 'modificato', pa[p], pd[p]))

carte, dial, frasi, strs, imm = [], [], [], [], []
altri = []
for p, tipo, sa, sd in toccati:
    if not p.endswith('.ehp') or tipo != 'modificato':
        continue
    da, dd = leggi(A, p), leggi(D, p)
    try:
        ea, fa = ai.apri(da); ed, fdz = ai.apri(dd)
    except Exception as e:
        altri.append((p, '', f'archivio non leggibile: {e}')); continue
    nome = os.path.basename(p)
    # carte
    if nome == f'cardinfo_{COD}.ehp':
        ta, tb = '_a.ehp', '_b.ehp'
        pa_, pb_ = os.path.join(out, '_ca.ehp'), os.path.join(out, '_cb.ehp')
        open(pa_, 'wb').write(da); open(pb_, 'wb').write(dd)
        ca, cb = cardprops.load(pa_, corretto=False), cardprops.load(pb_, corretto=False)
        os.remove(pa_); os.remove(pb_)
        for cid in sorted(ca):
            for campo in ('name', 'desc'):
                if ca[cid][campo] != cb[cid][campo]:
                    carte.append((cid, ca[cid]['name'], campo, ca[cid][campo], cb[cid][campo]))
        continue
    # dialoghi: script/stNN_*_<l>.ehp
    if p.startswith('/PSP_GAME/USRDIR/script/') and nome.endswith(f'_{LET}.ehp'):
        st = nome[:-len(f'_{LET}.ehp')]
        try:
            _, fj = ai.apri(leggi(A, p.replace(f'_{LET}.ehp', '_j.ehp')))
            _, fe = ai.apri(leggi(A, p.replace(f'_{LET}.ehp', '_e.ehp')))
        except Exception:
            fj = fe = {}
        scene = sorted({k.split('I' + LET + '.bin')[0] for k in fa if ('I' + LET + '.bin') in k})
        for sc in scene:
            try:
                ta, tb = dialoghi.stringhe(fa, sc, LET), dialoghi.stringhe(fdz, sc, LET)
            except KeyError:
                continue
            try:
                te = dialoghi.stringhe(fe, sc, 'e')
            except Exception:
                te = []
            try:
                tj = dialoghi.stringhe(fj, sc, 'j')
            except Exception:
                tj = []
            for i, (x, y) in enumerate(zip(ta, tb)):
                if x != y:
                    dial.append((f'{st}/{sc}#{i}', x.rstrip(dialoghi.FINE), y.rstrip(dialoghi.FINE),
                                 te[i].rstrip(dialoghi.FINE) if i < len(te) else '', tj[i].rstrip(dialoghi.FINE) if i < len(tj) else ''))
        continue
    for k in sorted(set(fa) | set(fdz)):
        if k in fa and k in fdz and bytes(fa[k]) == bytes(fdz[k]):
            continue
        if k.endswith('-ptrs.txt'):
            altri.append((p, k, 'tecnico: offset assoluti dei membri ricalcolati dopo la riscrittura di una tabella')); continue
        lg = lingua_di(p, k)
        if lg not in (LET,):
            if lg == '-':
                altri.append((p, k, 'membro modificato senza lingua riconoscibile'))
            continue
        if k not in fa or k not in fdz:
            altri.append((p, k, 'membro aggiunto/rimosso')); continue
        if k.endswith('.gim'):
            try:
                ha = gim.data_hash(gim.parse(bytes(fa[k]))); hb = gim.data_hash(gim.parse(bytes(fdz[k])))
            except Exception:
                ha = hb = '?'
            imm.append((p, k, ha, hb)); continue
        if k.endswith('-ptrs.txt'):
            altri.append((p, k, 'tecnico: offset assoluti dei membri ricalcolati dopo la riscrittura di una tabella')); continue
        ta, tb = tab_ok(bytes(fa[k])), tab_ok(bytes(fdz[k]))
        if ta is None or tb is None or len(ta) != len(tb):
            altri.append((p, k, 'binario/tabella non confrontabile (modificato)')); continue
        isf = re.match(r'(02)?chr_wordstbl_', k)
        for i, (x, y) in enumerate(zip(ta, tb)):
            if x != y:
                (frasi if isf else strs).append((p, k, i, x, y))

nl = lambda s: str(s).replace('\r\n', '⏎').replace('\n', '⏎').replace('\r', '⏎')


def csv_w(nome, intest, righe):
    with open(os.path.join(out, nome), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';'); w.writerow(intest)
        for r in righe:
            w.writerow([nl(x) for x in r])


csv_w('carte.csv', ['id', 'nome (originale)', 'campo', 'originale', 'nuovo'], carte)
csv_w('dialoghi.csv', ['id scena#riga', 'originale', 'nuovo', 'inglese', 'giapponese'], dial)
# frasi dei duelli: una riga per frase unica (la stessa frase compare in decine di archivi)
uniche = collections.OrderedDict()
for p, k, i, x, y in frasi:
    e = uniche.setdefault((x, y), [])
    e.append(os.path.basename(p))
csv_w('frasi_duello.csv', ['originale', 'nuovo', 'occorrenze (voci in archivi)', 'esempi di archivio'],
      [(x, y, len(v), ', '.join(sorted(set(v))[:4])) for (x, y), v in uniche.items()])
ug = collections.OrderedDict()
for p, k, i, x, y in strs:
    ug.setdefault((k, i, x, y), []).append(p.replace('/PSP_GAME/USRDIR/', ''))
csv_w('stringhe_ui.csv', ['membro', 'indice (0-based)', 'originale', 'nuovo', 'archivi in cui compare (stessa tabella copiata)'],
      [(k, i, x, y, '; '.join(v)) for (k, i, x, y), v in ug.items()])
csv_w('immagini_iso.csv', ['archivio', 'membro', 'hash originale', 'hash nuovo'], imm)
csv_w('file_toccati.csv', ['percorso nella ISO', 'tipo', 'byte originale', 'byte nuovo'], toccati)
csv_w('altro.csv', ['archivio', 'membro', 'nota'], altri)

riep = dict(lingua=L, carte=len(carte), carte_uniche=len({c[0] for c in carte}), dialoghi=len(dial), frasi_voci=len(frasi), frasi_uniche=len(uniche),
            stringhe_voci=len(strs), stringhe_uniche=len(ug), stringhe_archivi=len({s[0] for s in strs}), immagini=len(imm), file_toccati=len(toccati), altro=len(altri))
json.dump(riep, open(os.path.join(out, 'riepilogo.json'), 'w', encoding='utf-8'), indent=1)
print(riep)
