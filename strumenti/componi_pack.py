"""Compone un pack ULES00600 con le lingue scelte: pack base + moduli di lingua + textures.ini localizzati.
usage: componi_pack.py BASE MODULI CARD_DIR OUT LINGUA [LINGUA ...] [--copia]
  BASE      pack ULES00600 di base (cards/small, cards/large, ... textures.ini e _SCEGLI LO STILE DELLE CARTE/*/textures.ini)
  MODULI    cartella con i moduli (genera_lingua.py): MODULI/<lingua>/cards/..., MODULI/<lingua>/<lingua>.ini
  CARD_DIR  PSP_GAME/USRDIR/card della ISO
  OUT       cartella del pack da creare
I file vengono collegati (hard link, nessuno spazio extra) se possibile; con --copia (o su un altro volume) vengono copiati."""
import os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import modulo_ini

args = [a for a in sys.argv[1:] if not a.startswith('--')]
copia = '--copia' in sys.argv
base, moduli, card_dir, out, codici = args[0], args[1], args[2], args[3], args[4:]


def metti(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        os.remove(dst)
    if not copia:
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
for c in codici:
    mod = os.path.join(moduli, c)
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
    modulo_ini.main(card_dir, os.path.join(base, rel_in), dst, moduli, [c for c in codici])
