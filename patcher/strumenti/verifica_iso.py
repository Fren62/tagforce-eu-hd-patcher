"""Confronta due ISO file per file (percorso e contenuto). uso: verifica_iso.py A.iso B.iso"""
import hashlib, io, os, sys
import pycdlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'strumenti', 'correzioni'))
from una_lingua_iso import tutti


def hashes(p):
    iso = pycdlib.PyCdlib(); iso.open(p); iso.interchange_level = 4
    out = {}
    for f in tutti(iso):
        b = io.BytesIO(); iso.get_file_from_iso_fp(b, iso_path=f)
        out[f] = hashlib.sha256(b.getvalue()).hexdigest()
    return out


a, b = hashes(sys.argv[1]), hashes(sys.argv[2])
diff = [p for p in sorted(set(a) | set(b)) if a.get(p) != b.get(p)]
print(f'{len(a)} vs {len(b)} file, {len(diff)} differenze')
for p in diff[:20]:
    print(' ', p)
sys.exit(1 if diff else 0)
