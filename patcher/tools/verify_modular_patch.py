"""Verifies the modular patch of a language: every combination of modules must give, file by file, the expected ISO, and the
estimated size (--dry-run) must match the real one.
usage: verify_modular_patch.py ORIGINAL_ISO LANGUAGE PATCH.tfp TEMP_DIR     (the folder contains <l>_c.iso, <l>_t.iso, <l>_ct.iso
                                                                           left by build_modular_patch.py with TFP_KEEP=1)"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_modular_patch import hash_iso
import remove_language_selector

orig, language, patch, tmp = sys.argv[1:5]
exe = os.path.join(HERE, '..', 'tfpatch', 'target', 'release', 'tfpatch.exe' if os.name == 'nt' else 'tfpatch')
ROOT = os.path.join(HERE, '..', '..')


def tfpatch(opts, out):
    base = [exe, 'iso', '--iso', orig, '--patch', patch]
    r = subprocess.run(base + opts + ['--dry-run'], capture_output=True, text=True, check=True)
    estimate = int(r.stdout.strip())
    subprocess.run(base + opts + ['--out', out], check=True, capture_output=True)
    return estimate


def strip_reference():
    ref = os.path.join(tmp, f'{language}_ref_strip.iso')
    env = {**os.environ, 'PYTHONUTF8': '1'}
    subprocess.run([sys.executable, '-X', 'utf8', os.path.join(ROOT, 'tools', 'corrections', 'single_language_iso.py'),
                    os.path.join(tmp, f'{language}_ct.iso'), ref, language], check=True, capture_output=True, env=env)
    remove_language_selector.main(ref, language)
    return ref


cases = [  # (CLI options, expected ISO)
    (['--no-cards', '--no-text', '--keep-languages'], orig),
    (['--no-text', '--keep-languages'], os.path.join(tmp, f'{language}_c.iso')),
    (['--no-cards', '--keep-languages'], os.path.join(tmp, f'{language}_t.iso')),
    (['--keep-languages'], os.path.join(tmp, f'{language}_ct.iso')),
    ([], None),   # everything: reference = ct + single language + remove_language_selector
]
ok = True
for opts, expected in cases:
    out = os.path.join(tmp, f'{language}_rust.iso')
    estimate = tfpatch(opts, out)
    real = os.path.getsize(out)
    if expected is None:
        expected = strip_reference()
    a, b = hash_iso(expected), hash_iso(out)
    diff = [p for p in sorted(set(a) | set(b)) if a.get(p) != b.get(p)]
    result = not diff and estimate == real
    ok &= result
    print(f'{" ".join(opts) or "(all modules)":45s} files {len(b)}, differences {len(diff)}, estimate {estimate} real {real} -> {"OK" if result else "ERROR"}')
    for p in diff[:5]:
        print('   ', p)
    os.remove(out)
sys.exit(0 if ok else 1)
