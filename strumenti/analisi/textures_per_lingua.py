"""Elenca le texture del gioco che hanno una versione propria per la lingua scelta (cioe' quelle che vanno ridisegnate nell'interfaccia HD).

Per ogni archivio .ehp della USRDIR estratta si leggono le texture GIM e si calcola l'hash dei dati (la chiave che PPSSPP usa in textures.ini).
Gli archivi e i membri si raggruppano togliendo il segno della lingua dal nome (all_i.ehp / all_f.ehp, window_i0009 / window_f0009,
always_bri_ita / always_bri_fra, basic_ii / basic_ff ...). In ogni gruppo si confronta la versione della lingua con quella inglese e quella italiana:
  DIVERSA   hash diverso dall'inglese: la texture contiene testo (o pixel) propri della lingua -> da ridisegnare
  =ING      stesso hash dell'inglese: nessun lavoro (il pack inglese la copre gia')
  =ITA      stesso hash dell'italiano ma diverso dall'inglese: se l'italiano e' stato ridisegnato (esiste in PSP/TEXTURES/ULES00600/ui_it), vale anche per la lingua
Serve per capire QUANTE texture ci sono da fare e in quali archivi, prima di toccare gli script `ui_it/*.py`.

usage: textures_per_lingua.py USRDIR LINGUA [--solo-diverse]        LINGUA = it|fr|de|es|en
Scrive la tabella su stdout: archivio | membro | hash lingua | hash inglese | hash italiano | esito | ridisegnata in ui_it (si/no)

Attenzione: e' un'euristica sui nomi. Controlla sempre a occhio le texture elencate (dump con strumenti/analisi/dump4.py) e ricorda che alcune
lingue condividono lo stesso archivio (basic_if / basic_ff / basic_bf sono identici: si usa basic_<lettera><lettera>)."""
import os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'ui_it'))
from ehp import read
import gim

LET = {'it': 'i', 'fr': 'f', 'de': 'g', 'es': 's', 'en': 'e'}
LET3 = {'it': 'ita', 'fr': 'fra', 'de': 'ger', 'es': 'spa', 'en': 'eng'}


def per_lingua(nome, lettera, tre):
    """nome con il segno della lingua sostituito da '*' (None se il nome non ha il segno di quella lingua)"""
    n = nome
    n2 = re.sub(r'(?<![a-z])' + tre + r'(?![a-z])', '*', n)
    if n2 != n:
        return n2
    n2 = re.sub(r'basic_' + lettera + lettera, 'basic_**', n)
    if n2 != n:
        return n2
    n2 = re.sub(r'(?<=_)' + lettera + r'(?=\.ehp$|\.gim$|\d{4}|\.|_)', '*', n)
    return n2 if n2 != n else None


def main():
    usr, lingua = sys.argv[1:3]
    solo = '--solo-diverse' in sys.argv
    L, T = LET[lingua], LET3[lingua]
    # texture gia' ridisegnate per l'italiano (hash dalla cartella ui_it del pack di base)
    ini = glob.glob(os.path.join(HERE, '..', '..', 'PSP', 'TEXTURES', 'ULES00600', 'ui_it', '*.ini'))
    hash_it = set()
    for f in ini:
        for riga in open(f, encoding='utf-8'):
            m = re.match(r'^0{16}([0-9a-f]{8})\s*=', riga)
            if m:
                hash_it.add(m.group(1))
    tab = {}      # (archivio normalizzato, membro normalizzato) -> {lettera: hash}
    for p in glob.glob(os.path.join(usr, '**', '*.ehp'), recursive=True):
        rel = os.path.relpath(p, usr).replace('\\', '/')
        try:
            a = read(p)
        except Exception:
            continue
        for k, v in a.items():
            if not k.endswith('.gim'):
                continue
            try:
                h = gim.data_hash(gim.parse(v))
            except Exception:
                continue
            for lett, tre in ((x, LET3[c]) for c, x in LET.items()):
                an = per_lingua(rel, lett, tre)
                mn = per_lingua(k, lett, tre)
                if an is None and mn is None:
                    continue
                key = (an or rel, mn or k)
                tab.setdefault(key, {})[lett] = h
    righe = []
    for (a, m), d in sorted(tab.items()):
        if L not in d:
            continue
        e, i = d.get('e'), d.get('i')
        esito = 'DIVERSA' if L != 'e' and d[L] != e else ('=ING' if d[L] == e else '-')
        if esito == 'DIVERSA' and i and d[L] == i and L != 'i':
            esito = '=ITA'
        if solo and esito != 'DIVERSA':
            continue
        righe.append((a, m, d[L], e, i, esito, 'si' if i in hash_it else 'no'))
    for r in righe:
        print(' | '.join(str(x) for x in r))
    print('#', len(righe), 'texture', file=sys.stderr)


if __name__ == '__main__':
    main()
