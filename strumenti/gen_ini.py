"""Convert a Tag Force 1 USA (ULUS10136) texture pack ini to EU (ULES00600).

usage: gen_ini.py TOOLS_DIR US_INI CARD_DIR OUT_INI [LANG_PNG_DIRS]

Non-card entries are kept as-is (language-neutral textures share hashes).
Card entries are regenerated from the EU card archives for every EU language,
pointing at the PNG the US ini used for the same card id / art slot.
LANG_PNG_DIRS like "i=it" remaps cards/large/X.png -> cards/large_it/X.png for
that language (used for localized card-name PNGs) when that file exists.
"""
import collections, os, re, sys
sys.path.insert(0, sys.argv[1])
from tfcards import card_ids, slots, small_blob, large_blob, large_keys, key

us_ini, card_dir, out_ini = sys.argv[2:5]
extra = [a[1:] for a in sys.argv[5:] if a.startswith('+')]  # +file: extra [hashes] lines to append
lang_dirs = dict(a.split('=') for a in sys.argv[5:] if not a.startswith('+'))   # lettera del gioco -> codice: i=it f=fr g=de s=es
pack_root = os.path.dirname(os.path.abspath(out_ini))
while not os.path.isdir(os.path.join(pack_root, 'cards')) and os.path.dirname(pack_root) != pack_root:
    pack_root = os.path.dirname(pack_root)  # style variants live in a subfolder of the pack
LANGS = 'eifgs'  # english first: used to map alt-art slots to PNGs
CARD = re.compile(r'^0{8}(0000060[67])([0-9a-f]{8})\s*=\s*(cards/(small|large)/(\d+)([^/]*?)\.png)\s*$', re.I)

head, body, card_png = [], [], collections.defaultdict(dict)  # card_png[kind][hash] = png
per_card = collections.defaultdict(list)  # (kind, id) -> ordered unique pngs
names = {}
section = None
for line in open(us_ini, encoding='utf-8', errors='ignore'):
    line = line.rstrip('\r\n')
    if line.startswith('['):
        section = line.strip().lower()
    m = CARD.match(line)
    if m:
        kind, cid, png = m.group(4).lower(), int(m.group(5)), m.group(3)
        card_png[kind][m.group(2).lower()] = png
        if png not in per_card[(kind, cid)]:
            per_card[(kind, cid)].append(png)
        continue
    if re.match(r'^none\s*=', line):  # 'none' keys are not valid in PPSSPP (only warnings)
        continue
    c = re.match(r'^#(\d{4}):\s*(.*)$', line)
    if c:
        names[int(c.group(1))] = c.group(2)
        continue
    if '=' in line and not line.lstrip().startswith('#'):
        k, v = line.split('=', 1)
        line = k + '=' + v.replace('\\', '/')  # windows paths break on macOS/linux
    (head if section in (None, '[options]') else body).append(line)


MODULI = os.environ.get('TF1_MODULI')   # cartella con una sottocartella per lingua (it, fr, ...): moduli non ancora fusi nel pack


def localize(png, lang):
    sub = lang_dirs.get(lang)
    if not sub:
        return png
    alt = re.sub(r'^cards/(large|small)/', rf'cards/\1_{sub}/', png)
    if os.path.exists(os.path.join(pack_root, alt)) or (MODULI and os.path.exists(os.path.join(MODULI, sub, alt))):
        return alt
    return png


archives = {(k, l): open(f'{card_dir}/{k}_{l}.cip', 'rb').read() for k in ('cardh', 'cardm') for l in LANGS}
out, stats = [], collections.Counter()
ids = card_ids(archives[('cardm', 'e')])
for cid in ids:
    block = []
    for kind, arch, keysof in (('small', 'cardm', lambda b: [key(0, b)]), ('large', 'cardh', large_keys)):
        legacy = keysof if kind == 'small' else (lambda b: large_keys(b, stable=False))
        pngs = per_card.get((kind, cid))
        if not pngs:
            continue
        blob = small_blob if kind == 'small' else large_blob
        # map art slot index -> png, via english hashes that match the US ini
        en = [s for s in slots(archives[(arch, 'e')], cid)]
        slot_png = []
        for k, s in enumerate(en):
            hit = next((card_png[kind][h] for h in legacy(blob(archives[(arch, 'e')], s)) if h in card_png[kind]), None)
            if hit:
                stats[kind + '_slot_by_hash'] += 1
            slot_png.append(hit or (pngs[k] if len(pngs) > 1 and k < len(pngs) else pngs[0]))
        mid = '00000606' if kind == 'small' else '00000607'
        for lang in LANGS:
            for k, s in enumerate(slots(archives[(arch, lang)], cid)):
                if s == 0:
                    continue
                for h in keysof(blob(archives[(arch, lang)], s)):
                    block.append(f'00000000{mid}{h} = {localize(slot_png[min(k, len(slot_png) - 1)], lang)}')
                    stats[f'{kind}_{lang}'] += 1
    if block:
        out.append(f'#{cid}: {names.get(cid, "")}')
        seen = {}
        for line in block:  # same pixels in several languages -> keep the first (english) mapping
            seen.setdefault(line.split(' = ')[0], line)
        out += seen.values()

with open(out_ini, 'w', encoding='utf-8', newline='\n') as f:
    for i, line in enumerate(head):
        if line.strip().lower() == '[options]':
            head[i + 1:i + 1] = ['# Tag Force card fix (PPSSPP issue #19714): hash only the 3968 known bytes', 'skipLastDXT1Blocks128x64 = 16']
            break
    f.write('\n'.join(head) + '\n')
    f.write('\n'.join(body) + '\n')
    f.write('#==============================================#\n'
            '#   EU (ULES00600) CARD IMAGES - all 5 languages  #\n'
            '#   generated from the EU card archives          #\n'
            '#==============================================#\n')
    f.write('\n'.join(out) + '\n')
    for e in extra:
        f.write(open(e, encoding='utf-8').read())
print(dict(stats), 'cards', len([l for l in out if l.startswith('#')]))
