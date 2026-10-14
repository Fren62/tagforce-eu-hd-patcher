"""Compares the original ISO with the `_definitiva` ISO and writes, for ONE language, the COMPLETE list of every change made inside the ISO:
cards, dialogues, duel sentences, interface strings, images replaced in the .ehp, plus the list of the ISO files touched.
It is the "what has been changed" document derived from the real data (not hand-written): rerun it after every change.

usage: python document_changes.py ORIGINAL_ISO DEFINITIVE_ISO LANGUAGE OUT_DIR        LANGUAGE = it|fr|de|es|en
Writes in OUT_DIR:  cards.csv, dialogues.csv, duel_lines.csv, ui_strings.csv, iso_images.csv, touched_files.csv, summary.json
(CSV with `;` separator, UTF-8 with BOM, line breaks written as ⏎ ; openable with Excel/LibreOffice)."""
import csv, gzip, io, json, os, re, struct, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'tools')); sys.path.insert(0, os.path.join(B, 'tools', 'corrections'))
sys.stdout.reconfigure(encoding='utf-8')
import pycdlib
import apply_to_iso as ai, duel_lines as fd, dialogues, languages, cardprops, gim

orig_p, def_p, L, out = sys.argv[1:5]
LET = dialogues.LETTER[L]
COD = {'e': 'eng', 'f': 'fra', 'g': 'ger', 'i': 'ita', 's': 'spa'}[LET]
os.makedirs(out, exist_ok=True)
A, D = pycdlib.PyCdlib(), pycdlib.PyCdlib(); A.open(orig_p); D.open(def_p)


def read_file(iso, p):
    b = io.BytesIO(); iso.get_file_from_iso_fp(b, iso_path=p); return b.getvalue()


def paths(iso):
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


def language_di(arch, member):
    """language of the TEXT: letter in the member (strTbl_i.bin, icon06_f.gim, ScrXXXLi.bin) otherwise in the archive"""
    m = re.search(r'_([efgis])(?:\.|\d)', member) or re.search(r'[A-Za-z0-9]{3}[IL]([efgis])\.bin', member)
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
        t = fd.read_table(d)
        return t if t else None
    except Exception:
        return None


pa, pd = paths(A), paths(D)
touched = []
for p in sorted(set(pa) | set(pd)):
    if p not in pa or p not in pd:
        touched.append((p, 'aggiunto' if p in pd else 'rimosso', pa.get(p, 0), pd.get(p, 0))); continue
    if not p.endswith('.ehp'):
        continue
    if pa[p] != pd[p] or read_file(A, p) != read_file(D, p):
        touched.append((p, 'modificato', pa[p], pd[p]))

cards, dial, sentences, strs, imm = [], [], [], [], []
others = []
for p, type, sa, sd in touched:
    if not p.endswith('.ehp') or type != 'modificato':
        continue
    da, dd = read_file(A, p), read_file(D, p)
    try:
        ea, fa = ai.open_ehp(da); ed, fdz = ai.open_ehp(dd)
    except Exception as e:
        others.append((p, '', f'archivio non leggibile: {e}')); continue
    name = os.path.basename(p)
    # cards
    if name == f'cardinfo_{COD}.ehp':
        ta, tb = '_a.ehp', '_b.ehp'
        pa_, pb_ = os.path.join(out, '_ca.ehp'), os.path.join(out, '_cb.ehp')
        open(pa_, 'wb').write(da); open(pb_, 'wb').write(dd)
        ca, cb = cardprops.load(pa_, corrected=False), cardprops.load(pb_, corrected=False)
        os.remove(pa_); os.remove(pb_)
        for cid in sorted(ca):
            for field in ('name', 'desc'):
                if ca[cid][field] != cb[cid][field]:
                    cards.append((cid, ca[cid]['name'], field, ca[cid][field], cb[cid][field]))
        continue
    # dialoghi: script/stNN_*_<l>.ehp
    if p.startswith('/PSP_GAME/USRDIR/script/') and name.endswith(f'_{LET}.ehp'):
        st = name[:-len(f'_{LET}.ehp')]
        try:
            _, fj = ai.open_ehp(read_file(A, p.replace(f'_{LET}.ehp', '_j.ehp')))
            _, fe = ai.open_ehp(read_file(A, p.replace(f'_{LET}.ehp', '_e.ehp')))
        except Exception:
            fj = fe = {}
        scene = sorted({k.split('I' + LET + '.bin')[0] for k in fa if ('I' + LET + '.bin') in k})
        for sc in scene:
            try:
                ta, tb = dialogues.strings(fa, sc, LET), dialogues.strings(fdz, sc, LET)
            except KeyError:
                continue
            try:
                te = dialogues.strings(fe, sc, 'e')
            except Exception:
                te = []
            try:
                tj = dialogues.strings(fj, sc, 'j')
            except Exception:
                tj = []
            for i, (x, y) in enumerate(zip(ta, tb)):
                if x != y:
                    dial.append((f'{st}/{sc}#{i}', x.rstrip(dialogues.TRAILING), y.rstrip(dialogues.TRAILING),
                                 te[i].rstrip(dialogues.TRAILING) if i < len(te) else '', tj[i].rstrip(dialogues.TRAILING) if i < len(tj) else ''))
        continue
    for k in sorted(set(fa) | set(fdz)):
        if k in fa and k in fdz and bytes(fa[k]) == bytes(fdz[k]):
            continue
        if k.endswith('-ptrs.txt'):
            others.append((p, k, 'tecnico: offset assoluti dei membri ricalcolati dopo la riscrittura di una tabella')); continue
        lg = language_di(p, k)
        if lg not in (LET,):
            if lg == '-':
                others.append((p, k, 'membro modificato senza lingua riconoscibile'))
            continue
        if k not in fa or k not in fdz:
            others.append((p, k, 'membro aggiunto/rimosso')); continue
        if k.endswith('.gim'):
            try:
                ha = gim.data_hash(gim.parse(bytes(fa[k]))); hb = gim.data_hash(gim.parse(bytes(fdz[k])))
            except Exception:
                ha = hb = '?'
            imm.append((p, k, ha, hb)); continue
        if k.endswith('-ptrs.txt'):
            others.append((p, k, 'tecnico: offset assoluti dei membri ricalcolati dopo la riscrittura di una tabella')); continue
        ta, tb = tab_ok(bytes(fa[k])), tab_ok(bytes(fdz[k]))
        if ta is None or tb is None or len(ta) != len(tb):
            others.append((p, k, 'binario/tabella non confrontabile (modificato)')); continue
        isf = re.match(r'(02)?chr_wordstbl_', k)
        for i, (x, y) in enumerate(zip(ta, tb)):
            if x != y:
                (sentences if isf else strs).append((p, k, i, x, y))

nl = lambda s: str(s).replace('\r\n', '⏎').replace('\n', '⏎').replace('\r', '⏎')


def csv_w(name, header, rows):
    with open(os.path.join(out, name), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';'); w.writerow(header)
        for r in rows:
            w.writerow([nl(x) for x in r])


csv_w('cards.csv', ['id', 'nome (originale)', 'campo', 'originale', 'nuovo'], cards)
csv_w('dialogues.csv', ['id scena#riga', 'originale', 'nuovo', 'inglese', 'giapponese'], dial)
# duel sentences: one row per unique sentence (the same sentence appears in dozens of archives)
unique = collections.OrderedDict()
for p, k, i, x, y in sentences:
    e = unique.setdefault((x, y), [])
    e.append(os.path.basename(p))
csv_w('duel_lines.csv', ['originale', 'nuovo', 'occorrenze (voci in archivi)', 'esempi di archivio'],
      [(x, y, len(v), ', '.join(sorted(set(v))[:4])) for (x, y), v in unique.items()])
ug = collections.OrderedDict()
for p, k, i, x, y in strs:
    ug.setdefault((k, i, x, y), []).append(p.replace('/PSP_GAME/USRDIR/', ''))
csv_w('ui_strings.csv', ['membro', 'indice (0-based)', 'originale', 'nuovo', 'archivi in cui compare (stessa tabella copiata)'],
      [(k, i, x, y, '; '.join(v)) for (k, i, x, y), v in ug.items()])
csv_w('iso_images.csv', ['archivio', 'membro', 'hash originale', 'hash nuovo'], imm)
csv_w('touched_files.csv', ['percorso nella ISO', 'tipo', 'byte originale', 'byte nuovo'], touched)
csv_w('other.csv', ['archivio', 'membro', 'nota'], others)

summary = dict(language=L, cards=len(cards), cards_unique=len({c[0] for c in cards}), dialogues=len(dial), sentences_entries=len(sentences), sentences_unique=len(unique),
            strings_entries=len(strs), strings_unique=len(ug), strings_archives=len({s[0] for s in strs}), images=len(imm), file_touched=len(touched), other=len(others))
json.dump(summary, open(os.path.join(out, 'summary.json'), 'w', encoding='utf-8'), indent=1)
print(summary)
