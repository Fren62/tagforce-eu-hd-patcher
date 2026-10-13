"""Mostra nome e descrizione di alcune carte in una lingua e in inglese (testo del gioco, senza correzioni).
usage: mostra.py LINGUA ID [ID ...]        (cardinfo estratti in %TEMP%/ci)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import cardprops, lingue

lang, ids = sys.argv[1], [int(x) for x in sys.argv[2:]]
T = os.path.join(os.environ['TEMP'], 'ci')
c = cardprops.load(os.path.join(T, f'cardinfo_{lingue.LINGUE[lang][0]}.ehp'), corretto=False)
e = cardprops.load(os.path.join(T, 'cardinfo_eng.ehp'), corretto=False)
for i in ids:
    print(f'#{i} {c[i]["name"]}  /  {e[i]["name"]}')
    print('  ', c[i]['desc'].replace('\n', ' / '))
    if lang != 'en':
        print('  EN:', e[i]['desc'].replace('\n', ' / '))
