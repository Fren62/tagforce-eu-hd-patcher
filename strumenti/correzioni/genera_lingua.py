"""Genera dati/correzioni_carte_<lingua>.json (fr, de, es, en) dalle regole di correzioni/regole_<lingua>.py.
usage: genera_lingua.py LINGUA CARDINFO.ehp [OUT_JSON]       (scrive anche confronti/audit_carte/correzioni_<lingua>.csv)
Il JSON ha la forma {"<id>": {"name": "...", "desc": "..."}} con i soli campi cambiati, come correzioni_carte.json (italiano).
Ogni PER_CARTA deve trovare il testo esatto: se non c'e' si ferma, cosi' la tabella non deriva da una lettura sbagliata."""
import csv, importlib.util, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import cardprops

lang, ehp = sys.argv[1:3]
out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, '..', 'dati', f'correzioni_carte{"" if lang == "it" else "_" + lang}.json')
spec = importlib.util.spec_from_file_location('regole', os.path.join(HERE, f'regole_{lang}.py'))
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
IT = lang == 'it'     # italiano: si parte dai testi gia' corretti (correzioni_carte.json) e si fonde il risultato nello stesso file
cards = cardprops.load(ehp, corretto=IT)
res, rows = {}, []


def cambia(cid, campo, nuovo, motivo, vecchio_frammento=''):
    prima = cards[cid][campo]
    if nuovo != prima:
        res.setdefault(str(cid), {})[campo] = nuovo
        rows.append((cid, campo, prima, nuovo, motivo))


attuale = {cid: {'name': c['name'], 'desc': c['desc']} for cid, c in cards.items()}
for cid, campo, vecchio, nuovo, motivo in R.PER_CARTA:
    t = attuale[cid][campo]
    if IT and vecchio not in t and nuovo in t:
        continue      # italiano: gia' fusa in correzioni_carte.json da un lancio precedente
    if vecchio not in t:
        sys.exit(f'carta {cid} {campo}: testo non trovato: {vecchio!r}')
    attuale[cid][campo] = t.replace(vecchio, nuovo)
    rows.append((cid, campo, vecchio, nuovo, motivo + ' [carta]'))
for rx, rep, motivo in R.GLOBALI:
    p = re.compile(rx)
    n = 0
    for cid in attuale:
        for campo in ('name', 'desc'):
            t, k = p.subn(rep, attuale[cid][campo])
            if k:
                attuale[cid][campo] = t
                n += k
                rows.append((cid, campo, p.search(cards[cid][campo]).group(0) if p.search(cards[cid][campo]) else '', rep, motivo + ' [globale]'))
    print(f'{n:4d}  {rx[:60]}')
for cid, nuovo in getattr(R, 'NOMI', {}).items():      # nomi di carta ufficiali (sostituzione dell'intero nome, dopo tutte le regole)
    if attuale[cid]['name'] != nuovo:
        rows.append((cid, 'name', attuale[cid]['name'], nuovo, 'nome ufficiale [carta]'))
        attuale[cid]['name'] = nuovo
for cid, c in cards.items():
    for campo in ('name', 'desc'):
        if attuale[cid][campo] != c[campo]:
            res.setdefault(str(cid), {})[campo] = attuale[cid][campo]
if IT and os.path.exists(out):
    vecchio = json.load(open(out, encoding='utf-8'))
    for k, v in res.items():
        vecchio.setdefault(k, {}).update(v)
    res = vecchio
json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
csvp = os.path.join(HERE, '..', '..', 'confronti', 'audit_carte', f'correzioni_{lang}.csv')
with open(csvp, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['id', 'campo', 'prima', 'dopo', 'motivo'])
    w.writerows(rows)
print(lang, 'carte corrette:', len(res), '->', os.path.relpath(out))
