"""Shows the context of the 'refuso' reports of an audit: context.py LANGUAGE ID[,ID...] or context.py LANGUAGE all
usage: context.py audit_<language>.csv-dir LANGUAGE [ID ...]"""
import csv, os, re, sys

dir_, lang = sys.argv[1:3]
ids = {int(x) for x in sys.argv[3:]}
for r in csv.DictReader(open(os.path.join(dir_, f'audit_{lang}.csv'), encoding='utf-8-sig'), delimiter=';'):
    if r['categoria'] != 'refuso' or (ids and int(r['id']) not in ids):
        continue
    m = re.match(r'«(.+?)» \((\d+) uso', r['nota'])
    tok = m.group(1)
    t = r['testo_gioco']
    i = t.lower().find(tok)
    print(r['id'], '|', r['nome'][:28], '|', r['nota'].split(') ')[-1][:40], '|', '…' + t[max(0, i - 45):i + len(tok) + 45].replace('\n', ' ') + '…')
