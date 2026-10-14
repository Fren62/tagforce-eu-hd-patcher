"""Creates the texture archives for distribution: base.zip (common) + <language>.zip (one per language) + manifest.json.

usage: build_texture_modules.py TEXTURES_DIR CARD_DIR OUT_DIR [LANGUAGE ...]
  TEXTURES_DIR  PSP/TEXTURES (contains ULES00600 = base pack with Italian, and modules/<language>)
  CARD_DIR      PSP_GAME/USRDIR/card of the ISO (module_ini needs it for the card hashes)
Extracted one over the other (first base.zip, then <language>.zip) they give the complete pack of that language: the files of the
language overwrite those of the base and bring the already composed textures.ini. Uncompressed archives (the PNGs already are).
"""
import hashlib, json, os, re, shutil, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'tools'))
import module_ini

LANGUAGES = ['it', 'fr', 'de', 'es', 'en']
ITALIAN = ('cards/large_it', 'cards/small_it', 'cards/tiny_it', 'ui_it')   # in the installed base pack Italian is already inside
STYLE_DIR = '_CHOOSE YOUR CARD STYLE'
# English card art of the base pack: only English uses it (the other languages replace every card with their own
# cards/small_<l> and cards/large_<l>), so it travels in en.zip instead of base.zip
ENGLISH_ONLY = ('cards/small/', 'cards/large/', 'cards/tinyEN/', 'cards/tinyJP/', 'cards/tinyMikeyMK/')


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
    is_english_only = lambda n: n.startswith(ENGLISH_ONLY)
    base = [(n, p) for n, p in everything if n not in inis and not is_italian(n) and n not in it_intro and not is_english_only(n)]
    base_names = {n for n, _ in base}
    per_lang = {}
    for l in languages:
        if l == 'it':
            entries = [(n, p) for n, p in everything if is_italian(n) or n in it_intro]
            entries += [(n, p) for n, p in files(os.path.join(modules, 'it'), 'intro')]
            for rel in inis:     # the base inis hold the lines of every language: keep only those whose file ships
                dst = os.path.join(tmp, l, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(os.path.join(base_dir, rel), dst)
                cut_dead_lines(dst, base_names | {n for n, _ in entries})
                entries.append((rel, dst))
        else:
            mod = os.path.join(modules, l)
            entries = [x for sub in ('cards', 'intro', 'ui_' + l) for x in files(mod, sub)]
            if l == 'en':
                entries += [(n, p) for n, p in everything if is_english_only(n)]
            for rel in inis:
                dst = os.path.join(tmp, l, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                module_ini.main(card_dir, os.path.join(base_dir, rel), dst, modules, [l])
                cut_dead_lines(dst, base_names | {n for n, _ in entries})
                entries.append((rel, dst))
        per_lang[l] = entries
    # base.zip = only the textures that EVERY language needs; a texture needed by some languages goes into those modules;
    # a texture that no language references is dropped (PPSSPP looks textures up by hash, an unreferenced file is dead weight)
    def referenced(entries):
        ref = set()
        for n, p in entries:
            if n.endswith('textures.ini'):
                for r in open(p, encoding='utf-8').read().splitlines():
                    m = re.match(r'^\s*[0-9a-fA-F]+\s*=\s*(.+?)\s*$', r)
                    if m and not r.lstrip().startswith(('#', ';')):
                        ref.add(m.group(1))
        return ref
    refs = {l: referenced(e) for l, e in per_lang.items()}
    common = {n for n in base_names if all(n in refs[l] for l in languages)}
    dropped = [n for n in base_names if not any(n in refs[l] for l in languages)]
    print(f'common to all {len(languages)} languages: {len(common)} files; shared by some: {len(base_names) - len(common) - len(dropped)}; unreferenced (dropped): {len(dropped)}')
    base = [(n, p) for n, p in base if n in common]
    man = dict(format=1, base=write_zip(os.path.join(out, 'base.zip'), base), languages={})
    print('base.zip', man['base']['size'] >> 20, 'MB')
    for l in languages:
        extra = [(n, p) for n, p in everything if n in base_names and n not in common and n in refs[l]]
        # a name present twice goes once only in the language archive
        entries = [e for e in per_lang[l] if not (is_english_only(e[0]) and e[0] not in refs[l])]   # English art nobody points to
        entries = list({n: p for n, p in entries + extra}.items())
        man['languages'][l] = write_zip(os.path.join(out, f'{l}.zip'), entries)
        print(l + '.zip', man['languages'][l]['size'] >> 20, 'MB', len(entries), 'files')
    json.dump(man, open(os.path.join(out, 'manifest.json'), 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:] or LANGUAGES)
