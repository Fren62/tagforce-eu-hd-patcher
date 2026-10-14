"""Missing or different accents: words (also capitalized) that without accents coincide with a much more frequent word
that has the accents. usage: accents.py LANGUAGE  -> prints id | word | frequent form | context"""
import collections, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import cardprops, languages

lang = sys.argv[1]
T = os.path.join(os.environ['TEMP'], 'ci')
cards = cardprops.load(os.path.join(T, f'cardinfo_{languages.LANGUAGES[lang][0]}.ehp'), corrected=False)
strip = lambda w: ''.join(c for c in unicodedata.normalize('NFD', w) if unicodedata.category(c) != 'Mn')
tok = lambda t: re.findall(r"[^\W\d_]+", t)
freq = collections.Counter(w.lower() for c in cards.values() for w in tok(c['name'] + ' ' + c['desc']))
forms = collections.defaultdict(list)
for w in freq:
    forms[strip(w)].append(w)
for cid, c in cards.items():
    for field in ('name', 'desc'):
        for m in re.finditer(r"[^\W\d_]+", c[field]):
            w = m.group().lower()
            alt = [g for g in forms[strip(w)] if g != w and freq[g] >= 4 * freq[w] and freq[w] <= 6]
            if alt:
                t = c[field]
                print(cid, field, '|', m.group(), '->', max(alt, key=lambda g: freq[g]), f'({freq[w]}/{freq[max(alt, key=lambda g: freq[g])]})', '|', t[max(0, m.start() - 25):m.end() + 25].replace('\n', ' '))
