"""Accenti mancanti o diversi: parole (anche con iniziale maiuscola) che senza accenti coincidono con una parola molto piu'
frequente che ha gli accenti. usage: accenti.py LINGUA  -> stampa id | parola | forma frequente | contesto"""
import collections, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import cardprops, lingue

lang = sys.argv[1]
T = os.path.join(os.environ['TEMP'], 'ci')
cards = cardprops.load(os.path.join(T, f'cardinfo_{lingue.LINGUE[lang][0]}.ehp'), corretto=False)
strip = lambda w: ''.join(c for c in unicodedata.normalize('NFD', w) if unicodedata.category(c) != 'Mn')
tok = lambda t: re.findall(r"[^\W\d_]+", t)
freq = collections.Counter(w.lower() for c in cards.values() for w in tok(c['name'] + ' ' + c['desc']))
forme = collections.defaultdict(list)
for w in freq:
    forme[strip(w)].append(w)
for cid, c in cards.items():
    for campo in ('name', 'desc'):
        for m in re.finditer(r"[^\W\d_]+", c[campo]):
            w = m.group().lower()
            alt = [g for g in forme[strip(w)] if g != w and freq[g] >= 4 * freq[w] and freq[w] <= 6]
            if alt:
                t = c[campo]
                print(cid, campo, '|', m.group(), '->', max(alt, key=lambda g: freq[g]), f'({freq[w]}/{freq[max(alt, key=lambda g: freq[g])]})', '|', t[max(0, m.start() - 25):m.end() + 25].replace('\n', ' '))
