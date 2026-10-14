"""Shows the name and description of some cards in a language and in English (game text, without corrections).
usage: show.py LANGUAGE ID [ID ...]        (cardinfo extracted in %TEMP%/ci)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import cardprops, languages

lang, ids = sys.argv[1], [int(x) for x in sys.argv[2:]]
T = os.path.join(os.environ['TEMP'], 'ci')
c = cardprops.load(os.path.join(T, f'cardinfo_{languages.LANGUAGES[lang][0]}.ehp'), corrected=False)
e = cardprops.load(os.path.join(T, 'cardinfo_eng.ehp'), corrected=False)
for i in ids:
    print(f'#{i} {c[i]["name"]}  /  {e[i]["name"]}')
    print('  ', c[i]['desc'].replace('\n', ' / '))
    if lang != 'en':
        print('  EN:', e[i]['desc'].replace('\n', ' / '))
