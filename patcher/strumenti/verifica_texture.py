"""Controlla un textures.zip composto: ogni file citato nei textures.ini (principale e _SCEGLI...) esiste nello zip.
uso: verifica_texture.py textures.zip"""
import re, sys, zipfile
z = zipfile.ZipFile(sys.argv[1]); nomi = set(z.namelist()); low = {n.lower() for n in nomi}
inis = [n for n in nomi if n.endswith('textures.ini')]
mancano = 0; tot = 0
for ini in inis:
    for r in z.read(ini).decode('utf-8', 'replace').splitlines():
        m = re.match(r'^\s*[0-9a-fA-F]+\s*=\s*(.+?)\s*$', r)
        if m and not r.lstrip().startswith(('#', ';')):
            tot += 1
            if m.group(1) not in nomi:
                mancano += 1
                if mancano <= 5: print('manca', ini, m.group(1), '(solo maiuscole)' if m.group(1).lower() in low else '')
print(f'{len(nomi)} file, {len(inis)} ini, {tot} righe, {mancano} mancanti')
sys.exit(1 if mancano else 0)
