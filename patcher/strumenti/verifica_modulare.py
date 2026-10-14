"""Verifica la patch modulare di una lingua: ogni combinazione di moduli deve dare, file per file, la ISO attesa, e la
dimensione stimata (--dry-run) deve coincidere con quella reale.
uso: verifica_modulare.py ISO_ORIGINALE LINGUA PATCH.tfp CARTELLA_TEMP     (la cartella contiene <l>_c.iso, <l>_t.iso, <l>_ct.iso
                                                                           lasciate da crea_patch_modulare.py con TFP_KEEP=1)"""
import os, subprocess, sys
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
from crea_patch_modulare import hash_iso
import salta_lingua

orig, lingua, patch, tmp = sys.argv[1:5]
exe = os.path.join(QUI, '..', 'tfpatch', 'target', 'release', 'tfpatch.exe' if os.name == 'nt' else 'tfpatch')
RADICE = os.path.join(QUI, '..', '..')


def tfpatch(opts, out):
    base = [exe, 'iso', '--iso', orig, '--patch', patch]
    r = subprocess.run(base + opts + ['--dry-run'], capture_output=True, text=True, check=True)
    stima = int(r.stdout.strip())
    subprocess.run(base + opts + ['--out', out], check=True, capture_output=True)
    return stima


def riferimento_strip():
    ref = os.path.join(tmp, f'{lingua}_ref_strip.iso')
    env = {**os.environ, 'PYTHONUTF8': '1'}
    subprocess.run([sys.executable, '-X', 'utf8', os.path.join(RADICE, 'strumenti', 'correzioni', 'una_lingua_iso.py'),
                    os.path.join(tmp, f'{lingua}_ct.iso'), ref, lingua], check=True, capture_output=True, env=env)
    salta_lingua.main(ref, lingua)
    return ref


casi = [  # (opzioni CLI, ISO attesa)
    (['--no-cards', '--no-text', '--keep-languages'], orig),
    (['--no-text', '--keep-languages'], os.path.join(tmp, f'{lingua}_c.iso')),
    (['--no-cards', '--keep-languages'], os.path.join(tmp, f'{lingua}_t.iso')),
    (['--keep-languages'], os.path.join(tmp, f'{lingua}_ct.iso')),
    ([], None),   # tutto: riferimento = ct + una_lingua + salta_lingua
]
ok = True
for opts, atteso in casi:
    out = os.path.join(tmp, f'{lingua}_rust.iso')
    stima = tfpatch(opts, out)
    reale = os.path.getsize(out)
    if atteso is None:
        atteso = riferimento_strip()
    a, b = hash_iso(atteso), hash_iso(out)
    diff = [p for p in sorted(set(a) | set(b)) if a.get(p) != b.get(p)]
    esito = not diff and stima == reale
    ok &= esito
    print(f'{" ".join(opts) or "(tutti i moduli)":45s} file {len(b)}, differenze {len(diff)}, stima {stima} reale {reale} -> {"OK" if esito else "ERRORE"}')
    for p in diff[:5]:
        print('   ', p)
    os.remove(out)
sys.exit(0 if ok else 1)
