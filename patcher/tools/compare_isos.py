"""Compares two ISOs file by file (path and content). usage: compare_isos.py A.iso B.iso"""
import hashlib, io, os, sys
import pycdlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'corrections'))
from single_language_iso import all_files


def hashes(p):
    iso = pycdlib.PyCdlib()
    iso.open(p)
    iso.interchange_level = 4
    out = {}
    for f in all_files(iso):
        b = io.BytesIO()
        iso.get_file_from_iso_fp(b, iso_path=f)
        out[f] = hashlib.sha256(b.getvalue()).hexdigest()
    return out


a, b = hashes(sys.argv[1]), hashes(sys.argv[2])
diff = [p for p in sorted(set(a) | set(b)) if a.get(p) != b.get(p)]
print(f'{len(a)} vs {len(b)} files, {len(diff)} differences')
for p in diff[:20]:
    print(' ', p)
sys.exit(1 if diff else 0)
