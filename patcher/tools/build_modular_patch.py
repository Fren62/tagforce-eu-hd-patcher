"""Builds the MODULAR patch of a language (format 2): patch_<l>.tfp.

usage: build_modular_patch.py ORIGINAL_ISO LANGUAGE OUT.tfp [TEMP_DIR]

Every entry has `needs`: the modules that must be active for it to be applied.
  cards  : corrections to the card names and descriptions
  text   : corrections to the dialogues, the duel lines and the interface strings
  strip  : removes the other languages from the ISO, fixes the language and removes the selector and the menu entry (libtitle.prx)
For every file the entry with the most `needs`, all of them active, is applied (the "cards+text" entries are for the files touched by both).
The `link` entries (only with `strip`) make the files of the other languages point to the data of the chosen language.
The delta is always against the same file of the original ISO (no game data in the package)."""
import hashlib, io, json, os, subprocess, sys, zipfile
import bsdiff4
import pycdlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'tools', 'corrections'))
sys.path.insert(0, HERE)
from single_language_iso import all_files, plan
import remove_language_selector


def open_iso(p):
    iso = pycdlib.PyCdlib()
    iso.open(p)
    iso.interchange_level = 4
    return iso


def read_file(iso, p):
    b = io.BytesIO()
    iso.get_file_from_iso_fp(b, iso_path=p)
    return b.getvalue()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def md5_file(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 22), b''):
            h.update(c)
    return h.hexdigest()


def hash_iso(p):
    iso = open_iso(p)
    out = {f: sha(read_file(iso, f)) for f in all_files(iso)}
    iso.close()
    return out


def main(orig, language, out, tmp=None):
    tmp = tmp or os.path.join(ROOT, 'patcher', 'build', 'mod_tmp')
    os.makedirs(tmp, exist_ok=True)
    isos = {}
    for name, parts in (('c', 'cards'), ('t', 'text'), ('ct', 'cards,text')):
        dst = os.path.join(tmp, f'{language}_{name}.iso')
        isos[name] = dst
        subprocess.run([sys.executable, '-X', 'utf8', os.path.join(ROOT, 'tools', 'corrections', 'apply_to_iso.py'),
                        orig, dst, language, f'--parts={parts}'], check=True, capture_output=True,
                       env={**os.environ, 'PYTHONUTF8': '1'})
    ho = hash_iso(orig)
    h = {k: hash_iso(v) for k, v in isos.items()}
    changed = {k: {p for p, x in h[k].items() if ho.get(p) != x} for k in h}
    print({k: len(v) for k, v in changed.items()}, 'changed files (c, t, ct)')

    iso_o = open_iso(orig)
    iso_x = {k: open_iso(v) for k, v in isos.items()}
    entries, blobs = [], []

    def add(path, needs, source):
        old = read_file(iso_o, path)
        new = read_file(iso_x[source], path)
        entries.append(dict(op='delta', path=path, src=path, needs=needs, size=len(new), sha256=sha(new)))
        blobs.append(bsdiff4.diff(old, new))

    for p in sorted(changed['c']):
        add(p, ['cards'], 'c')
    for p in sorted(changed['t']):
        add(p, ['text'], 't')
    for p in sorted(changed['ct']):
        only_c, only_t = p in changed['c'], p in changed['t']
        if (only_c and only_t) or (only_c and h['ct'][p] != h['c'][p]) or (only_t and h['ct'][p] != h['t'][p]) or not (only_c or only_t):
            add(p, ['cards', 'text'], 'ct')
    # libtitle: language selector and menu entry removed, fixed language (only with strip)
    PRX = '/PSP_GAME/USRDIR/gmodule/libtitle.prx'
    old = read_file(iso_o, PRX)
    new = bytes(remove_language_selector.patch(bytearray(old), language))
    entries.append(dict(op='delta', path=PRX, src=PRX, needs=['strip'], size=len(new), sha256=sha(new)))
    blobs.append(bsdiff4.diff(old, new))
    # other languages: their files point to those of the chosen language
    for old_path, new_path in plan(all_files(iso_o), language):
        entries.append(dict(op='link', path=old_path, target=new_path, needs=['strip']))
    for k in iso_x.values():
        k.close()
    iso_o.close()
    meta = dict(format=2, language=language, iso_size=os.path.getsize(orig), iso_md5=md5_file(orig), entries=[])
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        bi = 0
        for v in entries:
            if v['op'] == 'delta':
                v['blob'] = f'blobs/{bi:04d}'
                z.writestr(v['blob'], blobs[bi])
                bi += 1
            meta['entries'].append(v)
        z.writestr('patch.json', json.dumps(meta, indent=1))
    n = {k: sum(1 for v in entries if v['op'] == 'delta' and v['needs'] == w) for k, w in
         (('cards', ['cards']), ('text', ['text']), ('cards+text', ['cards', 'text']), ('strip', ['strip']))}
    print(f'{language}: entries {n}, links {sum(1 for v in entries if v["op"] == "link")} -> {out} ({os.path.getsize(out) >> 10} KB)')
    if not os.environ.get('TFP_KEEP'):      # TFP_KEEP=1 keeps the intermediate ISOs (for the verification)
        for v in isos.values():
            os.remove(v)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
