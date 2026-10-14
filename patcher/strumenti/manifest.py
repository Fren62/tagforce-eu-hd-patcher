"""Compone la cartella della Release: manifest.json (moduli texture, patch, dimensioni della ISO per ogni combinazione di
moduli, MD5 accettati) + patch_<l>.tfp + base.zip / <l>.zip (collegati, non copiati).
uso: manifest.py ISO_ORIGINALE CARTELLA_MODULI(texture) CARTELLA_PATCH(patch2_<l>.tfp) CARTELLA_OUT"""
import hashlib, itertools, json, os, shutil, subprocess, sys, zipfile
QUI = os.path.dirname(os.path.abspath(__file__))
iso, moduli, patches, out = sys.argv[1:5]
exe = os.path.join(QUI, '..', 'tfpatch', 'target', 'release', 'tfpatch.exe' if os.name == 'nt' else 'tfpatch')
LINGUE = ['it', 'fr', 'de', 'es', 'en']
os.makedirs(out, exist_ok=True)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 22), b''):
            h.update(c)
    return h.hexdigest()


man = json.load(open(os.path.join(moduli, 'manifest.json'), encoding='utf-8'))
man['patch'], man['iso_sizes'], md5 = {}, {}, set()
for l in LINGUE:
    src = os.path.join(patches, f'patch2_{l}.tfp'); dst = os.path.join(out, f'patch_{l}.tfp')
    shutil.copyfile(src, dst)
    man['patch'][l] = dict(file=f'patch_{l}.tfp', size=os.path.getsize(dst), sha256=sha(dst))
    md5.add(json.loads(zipfile.ZipFile(dst).read('patch.json'))['iso_md5'])
    man['iso_sizes'][l] = {}
    for c, t, s in itertools.product((0, 1), repeat=3):
        opts = [f for f, v in (('--no-cards', not c), ('--no-text', not t), ('--keep-languages', not s)) if v]
        r = subprocess.run([exe, 'iso', '--iso', iso, '--patch', dst, '--dry-run'] + opts, capture_output=True, text=True, check=True)
        man['iso_sizes'][l][f'{c}{t}{s}'] = int(r.stdout.strip())
md5.add('719c99478032a4210ae877832061e9fd')            # dump completo (redump.org)
man['iso_md5'] = sorted(md5)
for nome in ['base.zip'] + [f'{l}.zip' for l in LINGUE]:
    d = os.path.join(out, nome)
    if not os.path.exists(d):
        try:
            os.link(os.path.join(moduli, nome), d)
        except OSError:
            shutil.copyfile(os.path.join(moduli, nome), d)
json.dump(man, open(os.path.join(out, 'manifest.json'), 'w', encoding='utf-8'), indent=1)
print('manifest:', {l: man['iso_sizes'][l]['111'] >> 20 for l in LINGUE}, 'MB (tutti i moduli)')
