"""Crea gli archivi texture per la distribuzione: base.zip (comune) + <lingua>.zip (uno per lingua) + manifest.json.

uso: crea_moduli.py TEXTURES_DIR CARD_DIR OUT_DIR [LINGUA ...]
  TEXTURES_DIR  PSP/TEXTURES (contiene ULES00600 = pack di base con l'italiano, e moduli/<lingua>)
  CARD_DIR      PSP_GAME/USRDIR/card della ISO (serve a modulo_ini per gli hash delle carte)
Estratti uno sopra l'altro (prima base.zip, poi <lingua>.zip) danno il pack completo di quella lingua: i file della
lingua sovrascrivono quelli del base e portano i textures.ini gia' composti. Archivi non compressi (i PNG lo sono gia').
"""
import hashlib, json, os, re, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'strumenti'))
import modulo_ini

LINGUE = ['it', 'fr', 'de', 'es', 'en']
ITALIANO = ('cards/large_it', 'cards/small_it', 'cards/tiny_it', 'ui_it')   # nel pack di base installato l'italiano e' gia' dentro


def files(root, sotto=None):
    out = []
    for d, _, fs in os.walk(os.path.join(root, sotto) if sotto else root):
        for f in fs:
            if f != '.DS_Store':
                p = os.path.join(d, f)
                out.append((os.path.relpath(p, root).replace(os.sep, '/'), p))
    return sorted(out)


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 22), b''):
            h.update(c)
    return h.hexdigest()


def taglia_righe_morte(ini, esistenti):
    """Toglie le righe 'hash = file' il cui file non c'e' in questo pack (restano solo quelle dell'italiano, assente)."""
    out = []
    for r in open(ini, encoding='utf-8').read().split(chr(10)):
        m = re.match(r'^\s*[0-9a-fA-F]+\s*=\s*(.+?)\s*$', r)
        if m and not r.lstrip().startswith(('#', ';')) and m.group(1) not in esistenti:
            continue
        out.append(r)
    open(ini, 'w', encoding='utf-8', newline='').write(chr(10).join(out))


def scrivi(zpath, voci):
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_STORED, allowZip64=True) as z:
        for nome, src in voci:
            z.write(src, nome)
    return dict(file=os.path.basename(zpath), size=os.path.getsize(zpath), sha256=sha256(zpath), entries=len(voci))


def main(tex, card_dir, out, lingue):
    base_dir, moduli = os.path.join(tex, 'ULES00600'), os.path.join(tex, 'moduli')
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(dir=out)
    inis = ['textures.ini'] + [f'_SCEGLI LO STILE DELLE CARTE/{v}/textures.ini'
                               for v in sorted(os.listdir(os.path.join(base_dir, '_SCEGLI LO STILE DELLE CARTE')))
                               if os.path.isdir(os.path.join(base_dir, '_SCEGLI LO STILE DELLE CARTE', v))]
    it_intro = {n for n, _ in files(os.path.join(moduli, 'it'), 'intro')}
    is_ita = lambda n: n.startswith(tuple(i + '/' for i in ITALIANO))

    tutti = files(base_dir)
    base = [(n, p) for n, p in tutti if n not in inis and not is_ita(n) and n not in it_intro]
    man = dict(formato=1, base=scrivi(os.path.join(out, 'base.zip'), base), lingue={})
    print('base.zip', man['base']['size'] >> 20, 'MB')
    for l in lingue:
        if l == 'it':
            voci = [(n, p) for n, p in tutti if is_ita(n) or n in it_intro or n in inis]
            voci += [(n, p) for n, p in files(os.path.join(moduli, 'it'), 'intro')]
        else:
            mod = os.path.join(moduli, l)
            voci = [x for sub in ('cards', 'intro', 'ui_' + l) for x in files(mod, sub)]
            for rel in inis:
                dst = os.path.join(tmp, l, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                modulo_ini.main(card_dir, os.path.join(base_dir, rel), dst, moduli, [l])
                taglia_righe_morte(dst, {n for n, _ in base} | {n for n, _ in voci})
                voci.append((rel, dst))
        # un nome presente due volte (base e modulo) va una volta sola nell'archivio della lingua
        voci = list({n: p for n, p in voci}.items())
        man['lingue'][l] = scrivi(os.path.join(out, f'{l}.zip'), voci)
        print(l + '.zip', man['lingue'][l]['size'] >> 20, 'MB', len(voci), 'file')
    json.dump(man, open(os.path.join(out, 'manifest.json'), 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:] or LINGUE)
