"""Checks a composed textures.zip: every file named in the textures.ini files (main and _SCEGLI...) exists in the zip.
usage: verify_texture_pack.py textures.zip"""
import re, sys, zipfile
z = zipfile.ZipFile(sys.argv[1])
names = set(z.namelist())
low = {n.lower() for n in names}
inis = [n for n in names if n.endswith('textures.ini')]
missing = 0
total = 0
for ini in inis:
    for r in z.read(ini).decode('utf-8', 'replace').splitlines():
        m = re.match(r'^\s*[0-9a-fA-F]+\s*=\s*(.+?)\s*$', r)
        if m and not r.lstrip().startswith(('#', ';')):
            total += 1
            if m.group(1) not in names:
                missing += 1
                if missing <= 5:
                    print('missing', ini, m.group(1), '(case only)' if m.group(1).lower() in low else '')
print(f'{len(names)} files, {len(inis)} ini, {total} lines, {missing} missing')
sys.exit(1 if missing else 0)
