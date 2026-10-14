"""Composes a ULES00600 pack with the chosen languages: base pack + language modules + localized textures.ini.
usage: compose_pack.py BASE MODULES CARD_DIR OUT LANGUAGE [LANGUAGE ...] [--copy]
  BASE      base ULES00600 pack (cards/small, cards/large, ... textures.ini and _SCEGLI LO STILE DELLE CARTE/*/textures.ini)
  MODULES   folder with the modules (generate_language.py): MODULES/<language>/cards/..., MODULES/<language>/<language>.ini
  CARD_DIR  PSP_GAME/USRDIR/card of the ISO
  OUT       folder of the pack to create
Files are linked (hard links, no extra space) if possible; with --copy (or on another volume) they are copied."""
import os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import module_ini

args = [a for a in sys.argv[1:] if not a.startswith('--')]
copy = '--copy' in sys.argv
base, modules, card_dir, out, codes = args[0], args[1], args[2], args[3], args[4:]


def metti(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        os.remove(dst)
    if not copy:
        try:
            os.link(src, dst)
            return
        except OSError:
            pass
    shutil.copy2(src, dst)


n = 0
for d, _, fs in os.walk(base):
    for f in fs:
        if f.lower() == 'textures.ini' or f == '.DS_Store':
            continue
        p = os.path.join(d, f)
        metti(p, os.path.join(out, os.path.relpath(p, base)))
        n += 1
for c in codes:
    mod = os.path.join(modules, c)
    for d, _, fs in [x for sub in ('cards', 'intro', 'ui_' + c) for x in os.walk(os.path.join(mod, sub))]:
        for f in fs:
            p = os.path.join(d, f)
            metti(p, os.path.join(out, os.path.relpath(p, mod)))
            n += 1
print('file', n)
inis = [('textures.ini', 'textures.ini')]
for v in os.listdir(os.path.join(base, '_SCEGLI LO STILE DELLE CARTE')):
    inis.append((f'_SCEGLI LO STILE DELLE CARTE/{v}/textures.ini',) * 2)
for rel_in, rel_out in inis:
    dst = os.path.join(out, rel_out)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    module_ini.main(card_dir, os.path.join(base, rel_in), dst, modules, [c for c in codes])
