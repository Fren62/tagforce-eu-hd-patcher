"""Audit of the card texts of a language (fr, de, es, en, it): reports possible errors, does not correct them.
usage: audit_language.py LANGUAGE CARDINFO_LANGUAGE.ehp CARDINFO_ENG.ehp OUT_DIR [OFFICIAL_LANGUAGE.json OFFICIAL_EN.json]
Checks (all objective and repeatable):
  mancante    description much shorter than the game's English one, or empty
  numeri      the numbers in the text (ATK/DEF, quantities) differ from those of the game's English
  spazi       double spaces, space after the apostrophe or before , . ; punctuation stuck to the following word
  virgolette  odd number of straight quotation marks
  refuso      rare word (<= 2 uses in the game) at distance 1 (2 if long) from a very frequent word (>= 15 uses)
  inglese     common English words left in the text (fr, de, es, it only)
  ufficiale   (with the YGOPRODeck JSONs) text almost identical to the modern official one but with 1-3 different words
Writes OUT_DIR/audit_<language>.csv (id; name; category; note; game text; comparison text)."""
import collections, csv, difflib, json, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from ehp import read
import cardprops

lang, ehp, ehp_en, out = sys.argv[1:5]
official = sys.argv[5:7]


def load_data(path):
    # corrected=False: the audit looks at the game's text, not at the corrections already applied
    return cardprops.load(path, corrected=False)


def passcodes(path):
    f = read(path)
    intid, pas = f['CARD_IntID.bin'], f['CARD_Pass.bin']
    res = {}
    for off in range(len(intid) // 2):
        idx = struct.unpack_from('<H', intid, off * 2)[0]
        if idx:
            res[4000 + off] = struct.unpack_from('<I', pas, idx * 4)[0]
    return res


cards, en = load_data(ehp), load_data(ehp_en)
rows = []


def add(cid, cat, note, text='', conf=''):
    rows.append((cid, cards[cid]['name'], cat, note, text, conf))


norm = lambda t: re.sub(r'\s+', ' ', t.replace('\n', ' ')).strip()
words = lambda t: re.findall(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", t.lower())
nums = lambda t: sorted(re.findall(r'\d+(?:[.,]\d+)*', t.replace('.', '').replace(',', '')))

# 1-3, 5: controlli strutturali
for cid, c in cards.items():
    d, e = norm(c['desc']), norm(en[cid]['desc'])
    if lang != 'en':
        if not d or (len(e) > 60 and len(d) < 0.45 * len(e)):
            add(cid, 'mancante', f'{len(d)} caratteri contro {len(e)} in inglese', d, e)
        if nums(d) != nums(e):
            add(cid, 'numeri', f'numeri {nums(d)} contro {nums(e)} in inglese', d, e)
    if re.search(r'  +|\w\s+[,.;]|[\'’] \w|\b[a-zà-ÿ]{2,}[.,;:][A-Za-zÀ-ÿ]', d):
        m = re.search(r'  +|\w\s+[,.;]|[\'’] \w|\b[a-zà-ÿ]{2,}[.,;:][A-Za-zÀ-ÿ]', d)
        add(cid, 'spazi', f'«{d[max(0, m.start() - 15):m.end() + 15]}»', d)
    if d.count('"') % 2:
        add(cid, 'virgolette', 'numero dispari di virgolette dritte', d)

# 4: possibili refusi (parole rare vicine a parole frequenti)
freq = collections.Counter(w for c in cards.values() for w in words(c['name'] + ' ' + c['desc']))
common = [w for w, n in freq.items() if n >= 15 and len(w) >= 4]
by_len = collections.defaultdict(list)
for w in common:
    by_len[len(w)].append(w)


def dist_max(a, b, k):
    """True if the Levenshtein distance (with transposition) is <= k."""
    if abs(len(a) - len(b)) > k:
        return False
    prev2, prev = None, list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                cur[j] = min(cur[j], prev2[j - 2] + 1)
        prev2, prev = prev, cur
    return prev[-1] <= k


rare = {w for w, n in freq.items() if n <= 2 and len(w) >= 5}
suspects = {}
for w in rare:
    k = 1 if len(w) < 9 else 2
    for L in range(len(w) - k, len(w) + k + 1):
        for g in by_len.get(L, ()):
            if g != w and dist_max(w, g, k) and not (len(w) > len(g) and w.startswith(g)) and not (len(g) > len(w) and g.startswith(w)):
                suspects.setdefault(w, []).append(g)
for cid, c in cards.items():
    for w in dict.fromkeys(words(c['name'] + ' ' + c['desc'])):
        if w in suspects:
            add(cid, 'refuso', f'«{w}» ({freq[w]} uso/i) simile a: ' + ', '.join(sorted(suspects[w], key=lambda g: -freq[g])[:3]), norm(c['desc']))

# parole inglesi rimaste
ENGLISH = {'the', 'this', 'card', 'your', 'opponent', 'monster', 'monsters', 'during', 'when', 'once', 'turn', 'select', 'destroy', 'destroyed',
           'and', 'with', 'from', 'that', 'cards', 'effect', 'field', 'graveyard', 'equipped', 'summon', 'summoned'}
if lang in ('fr', 'de', 'es', 'it'):
    cn = {w for w in ENGLISH}
    for cid, c in cards.items():
        name_en = set(words(en[cid]['name']))
        found = [w for w in dict.fromkeys(words(c['desc'])) if w in cn and w not in name_en]
        if len(found) >= 2 or (found and len(words(c['desc'])) < 12):
            add(cid, 'inglese', 'parole inglesi: ' + ', '.join(found), norm(c['desc']))

# comparison with the modern official text
if official:
    ul = {c['id']: c for c in json.load(open(official[0], encoding='utf-8'))['data']}
    pas = passcodes(ehp)
    for cid, c in cards.items():
        o = ul.get(pas.get(cid))
        if not o:
            continue
        a, b = norm(c['desc']), norm(o.get('desc', ''))
        wa, wb = words(a), words(b)
        sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
        if 0.85 <= sm.ratio() < 1.0 and len(wa) > 4:
            ops = [(t, ' '.join(wa[i1:i2]), ' '.join(wb[j1:j2])) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']
            if 1 <= len(ops) <= 3 and all(len(x[1].split()) <= 3 and len(x[2].split()) <= 3 for x in ops):
                add(cid, 'ufficiale', '; '.join(f'«{x[1]}» -> «{x[2]}»' for x in ops), a, b)

os.makedirs(out, exist_ok=True)
rows.sort(key=lambda r: (r[2], r[0]))
with open(os.path.join(out, f'audit_{lang}.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['id', 'nome', 'categoria', 'nota', 'testo_gioco', 'confronto'])
    w.writerows(rows)
print(lang, collections.Counter(r[2] for r in rows))
