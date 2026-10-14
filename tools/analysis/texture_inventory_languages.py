"""For every texture of ui_it (and ui_fr) says whether it is NEUTRAL (same hash in all languages: copied as is for es/de) or
SPECIFIC (different hash per language: to be redone, taking it/fr as reference). Writes docs/TEXTURE_INVENTORY.md.
usage: python texture_inventory_languages.py ORIGINAL_ISO OUT.md"""
import io, os, re, sys, collections
B = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(B, 'tools')); sys.path.insert(0, os.path.join(B, 'tools', 'corrections'))
sys.stdout.reconfigure(encoding='utf-8')
import pycdlib, gim, apply_to_iso as ai
iso, out = sys.argv[1:3]
I = pycdlib.PyCdlib(); I.open(iso)
H, idx = {}, collections.defaultdict(list)
def walk(p):
    for ch in I.list_children(iso_path=p):
        n = ch.file_identifier().decode().split(';')[0]
        if n in ('.', '..'): continue
        q = p.rstrip('/') + '/' + n
        if ch.is_dir(): yield from walk(q)
        elif n.endswith('.ehp'): yield q
for q in walk('/PSP_GAME/USRDIR'):
    b = io.BytesIO(); I.get_file_from_iso_fp(b, iso_path=q)
    try: e, f = ai.open_ehp(b.getvalue())
    except Exception: continue
    for k in f:
        if k.endswith('.gim'):
            try: h = gim.data_hash(gim.parse(bytes(f[k])))
            except Exception: continue
            H[(q, k)] = h; idx[h].append((q, k))
LET = {'e': ('e', 'eng', 'ee'), 'f': ('f', 'fra', 'ff'), 'g': ('g', 'ger', 'gg'), 'i': ('i', 'ita', 'ii'), 's': ('s', 'spa', 'ss')}
def variants(q, k, src):
    """equivalent names in the other languages, replacing the language letter/code src"""
    r = {}
    for L, (a, b3, c) in LET.items():
        sa, sb, sc = LET[src]
        def sub(s):
            s = re.sub(rf'(?<=[_0-9a-z]){sc}(?=\.ehp|__|$)', c, s) if False else s
            s = re.sub(rf'_{sb}(?=\.|_|$)', f'_{b3}', s)
            s = re.sub(rf'_{sa}(?=\.|_|\d|$)', f'_{a}', s)
            s = re.sub(rf'(basic_[bf]?){sa}{sa}\b', rf'\g<1>{a}{a}', s) if False else s
            return s
        r[L] = (sub(q), sub(k))
    return r
def language(q, k):
    """language of a texture's TEXT: letter in the member name (icon06_f.gim, vs_bg01_1_f0005.gim) or, if missing, in the archive
    (all_f.ehp, title_menu_f.ehp, always_bri_fra.ehp, basic_bf.ehp = final letter)"""
    m = re.search(r'_([efgis])(?:\d|\.gim)', k)
    if m: return m.group(1)
    a = os.path.basename(q)
    m = re.search(r'basic_[a-z]([efgis])\.ehp$', a) or re.search(r'_([efgis])\.ehp$', a)
    if m: return m.group(1)
    m = re.search(r'_(eng|fra|ger|ita|spa)\.ehp$', a)
    if m: return {'eng': 'e', 'fra': 'f', 'ger': 'g', 'ita': 'i', 'spa': 's'}[m.group(1)]
    return '-'
rows = collections.defaultdict(list)
for fam in ('ui_it', 'ui_fr'):
    root = os.path.join(B, 'PSP', 'TEXTURES', 'ULES00600' if fam == 'ui_it' else 'modules/fr', fam)
    ini = os.path.join(B, 'PSP', 'TEXTURES', 'ULES00600', 'textures.ini') if fam == 'ui_it' else os.path.join(B, 'PSP', 'TEXTURES', 'modules', 'fr', 'fr.ini')
    mp = {}
    for l in open(ini, encoding='utf-8'):
        m = re.match(r'^[0-9a-f]{16}([0-9a-f]{8})\s*=\s*(' + fam + r'/\S+)', l)
        if m: mp[m.group(2)] = m.group(1)
    for dp, _, fs in os.walk(root):
        for f in sorted(fs):
            if not f.endswith('.png'): continue
            rel = fam + '/' + os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/')
            h = mp.get(rel)
            if not h: rows[fam].append((rel, '?', 'hash not found', '')); continue
            locs = idx.get(h, [])
            L = sorted({language(q, k) for q, k in locs} - {'-'})
            neutral = ('g' in L and 's' in L) or len(L) >= 4 or '-' in {language(q, k) for q, k in locs} and len(L) <= 1 and any(language(q, k) == '-' for q, k in locs)
            kind = 'NEUTRAL' if neutral else 'SPECIFIC'
            rows[fam].append((rel, h, kind, 'languages with the same hash: ' + (''.join(L) or 'none (archive without a language)') + ' - ' + ', '.join(sorted({os.path.basename(q) + ':' + k for q, k in locs})[:2])))
with open(out, 'w', encoding='utf-8', newline='\n') as o:
    o.write('# Inventario texture: neutre / specifiche per lingua\n\nGenerato da `tools/analysis/texture_inventory_languages.py`. **NEUTRA** = lo stesso hash compare in piu\' lingue (de/es incluse): il PNG si copia tale e quale nel modulo della nuova lingua (e di norma e\' gia\' nel pack di base). **SPECIFICA** = l\'originale e\' diverso per lingua: va rifatta con le parole della lingua, prendendo `ui_it`/`ui_fr` come riferimento.\n\n')
    for fam, rs in rows.items():
        c = collections.Counter(r[2] for r in rs)
        o.write(f'## {fam} ({dict(c)})\n\n| file | hash | tipo | dove |\n|---|---|---|---|\n')
        for r in sorted(rs, key=lambda r: (r[2], r[0])): o.write(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} |\n')
        o.write('\n')
print({k: collections.Counter(r[2] for r in v) for k, v in rows.items()})
