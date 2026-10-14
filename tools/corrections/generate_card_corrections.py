"""Generates data/card_corrections_<language>.json (fr, de, es, en) from the rules in corrections/rules_<language>.py.
usage: generate_card_corrections.py LANGUAGE CARDINFO.ehp [OUT_JSON]       (also writes comparisons/audit_carte/correzioni_<language>.csv)
The JSON has the form {"<id>": {"name": "...", "desc": "..."}} with the changed fields only, like card_corrections.json (Italian).
Every PER_CARD must find the exact text: if it is not there it stops, so the table does not derive from a wrong reading."""
import csv, importlib.util, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import cardprops

lang, ehp = sys.argv[1:3]
out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, '..', 'data', f'card_corrections{"" if lang == "it" else "_" + lang}.json')
spec = importlib.util.spec_from_file_location('rules', os.path.join(HERE, f'rules_{lang}.py'))
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
IT = lang == 'it'     # Italian: starts from the already corrected texts (card_corrections.json) and merges the result into the same file
cards = cardprops.load(ehp, corrected=IT)
res, rows = {}, []

current = {cid: {'name': c['name'], 'desc': c['desc']} for cid, c in cards.items()}
for cid, field, old, new, reason in R.PER_CARD:
    t = current[cid][field]
    if IT and old not in t and new in t:
        continue      # Italian: already merged into card_corrections.json by a previous run
    if old not in t:
        sys.exit(f'card {cid} {field}: text not found: {old!r}')
    current[cid][field] = t.replace(old, new)
    rows.append((cid, field, old, new, reason + ' [card]'))
for rx, rep, reason in R.GLOBALS:
    p = re.compile(rx)
    n = 0
    for cid in current:
        for field in ('name', 'desc'):
            t, k = p.subn(rep, current[cid][field])
            if k:
                current[cid][field] = t
                n += k
                rows.append((cid, field, p.search(cards[cid][field]).group(0) if p.search(cards[cid][field]) else '', rep, reason + ' [global]'))
    print(f'{n:4d}  {rx[:60]}')
for cid, new in getattr(R, 'NAMES', {}).items():      # official card names (replacement of the whole name, after all the rules)
    if current[cid]['name'] != new:
        rows.append((cid, 'name', current[cid]['name'], new, 'official name [card]'))
        current[cid]['name'] = new
for cid, c in cards.items():
    for field in ('name', 'desc'):
        if current[cid][field] != c[field]:
            res.setdefault(str(cid), {})[field] = current[cid][field]
if IT and os.path.exists(out):
    previous = json.load(open(out, encoding='utf-8'))
    for k, v in res.items():
        previous.setdefault(k, {}).update(v)
    res = previous
json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
csv_path = os.path.join(HERE, '..', '..', 'comparisons', 'audit_carte', f'correzioni_{lang}.csv')
with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['id', 'field', 'before', 'after', 'reason'])
    w.writerows(rows)
try:
    shown = os.path.relpath(out)
except ValueError:      # output on another drive (Windows)
    shown = out
print(lang, 'corrected cards:', len(res), '->', shown)
