"""Creates the texture archives for distribution: base.zip (common) + <language>.zip (one per language) + manifest.json.

usage: build_texture_modules.py TEXTURES_DIR CARD_DIR OUT_DIR [LANGUAGE ...]
  TEXTURES_DIR  PSP/TEXTURES (contains ULES00600 = base pack with Italian, and modules/<language>)
  CARD_DIR      PSP_GAME/USRDIR/card of the ISO (module_ini needs it for the card hashes)
Extracted one over the other (first base.zip, then <language>.zip) they give the complete pack of that language: the files of the
language overwrite those of the base and bring the already composed textures.ini. Uncompressed archives (the PNGs already are).
"""
import hashlib, json, os, re, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))
import module_ini

LANGUAGES = ['it', 'fr', 'de', 'es', 'en']
ITALIAN = ('cards/large_it', 'cards/small_it', 'cards/tiny_it', 'ui_it')   # in the installed base pack Italian is already inside
STYLE_DIR = '_CHOOSE YOUR CARD STYLE'


def files(root, sub=None):
    out = []
    for d, _, fs in os.walk(os.path.join(root, sub) if sub else root):
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


def cut_dead_lines(ini, existing):
    """Removes the 'hash = file' lines whose file is not in this pack (only those of Italian, which is absent, remain)."""
    out = []
    for r in open(ini, encoding='utf-8').read().split(chr(10)):
        m = re.match(r'^\s*[0-9a-fA-F]+\s*=\s*(.+?)\s*$', r)
        if m and not r.lstrip().startswith(('#', ';')) and m.group(1) not in existing:
            continue
        out.append(r)
    open(ini, 'w', encoding='utf-8', newline='').write(chr(10).join(out))


def write_zip(zpath, entries):
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_STORED, allowZip64=True) as z:
        for name, src in entries:
            z.write(src, name)
    return dict(file=os.path.basename(zpath), size=os.path.getsize(zpath), sha256=sha256(zpath), entries=len(entries))


def main(tex, card_dir, out, languages):
    base_dir, modules = os.path.join(tex, 'ULES00600'), os.path.join(tex, 'modules')
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(dir=out)
    inis = ['textures.ini'] + [f'{STYLE_DIR}/{v}/textures.ini'
                               for v in sorted(os.listdir(os.path.join(base_dir, STYLE_DIR)))
                               if os.path.isdir(os.path.join(base_dir, STYLE_DIR, v))]
    it_intro = {n for n, _ in files(os.path.join(modules, 'it'), 'intro')}
    is_italian = lambda n: n.startswith(tuple(i + '/' for i in ITALIAN))

    everything = files(base_dir)
    base = [(n, p) for n, p in everything if n not in inis and not is_italian(n) and n not in it_intro]
    man = dict(format=1, base=write_zip(os.path.join(out, 'base.zip'), base), languages={})
    print('base.zip', man['base']['size'] >> 20, 'MB')
    for l in languages:
        if l == 'it':
            entries = [(n, p) for n, p in everything if is_italian(n) or n in it_intro or n in inis]
            entries += [(n, p) for n, p in files(os.path.join(modules, 'it'), 'intro')]
        else:
            mod = os.path.join(modules, l)
            entries = [x for sub in ('cards', 'intro', 'ui_' + l) for x in files(mod, sub)]
            for rel in inis:
                dst = os.path.join(tmp, l, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                module_ini.main(card_dir, os.path.join(base_dir, rel), dst, modules, [l])
                cut_dead_lines(dst, {n for n, _ in base} | {n for n, _ in entries})
                entries.append((rel, dst))
        # a name present twice (base and module) goes once only in the language archive
        entries = list({n: p for n, p in entries}.items())
        man['languages'][l] = write_zip(os.path.join(out, f'{l}.zip'), entries)
        print(l + '.zip', man['languages'][l]['size'] >> 20, 'MB', len(entries), 'files')
    json.dump(man, open(os.path.join(out, 'manifest.json'), 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:] or LANGUAGES)
