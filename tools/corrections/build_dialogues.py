"""Generates data/dialogue_corrections_<language>.json (id -> current, proposed) for dialogues.py from:
  - the original dialogues (comparisons/audit_dialoghi/dialoghi_<language>.tsv, extracted with audit/extract_dialogues.py from the original ISO)
  - data/dialogue_corrections_<language>_base.json (it only: the complete hand-made review)
  - data/dialogue_touchups_<language>.json  {"exact": {line: new}, "parts": [[old, new]]}  (line breaks written as ⏎)
  - automatic rules: spaces around the 《...》 placeholders and (fr only) space before ! ? : ;
  - scene st02_t01/Scr101E lines 22-27: in the original game the text is rotated between the languages (it has French,
    fr German, de English, es Italian); each one is put back in its own language.
usage: build_dialogues.py LANGUAGE [LANGUAGE ...]"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
AUDIT = os.path.join(HERE, '..', '..', 'comparisons', 'audit_dialoghi')
nl = lambda s: s.replace('⏎', '\n')
SPACE_BEFORE = re.compile(r"(?<=[A-Za-zÀ-ÿ,;:!?])《")
SPACE_AFTER = re.compile(r"》(?=[A-Za-zÀ-ÿ])")
SPACE_AFTER_DE = re.compile(r"》(?!s(?![A-Za-zÀ-ÿ]))(?=[A-Za-zÀ-ÿ])")
IT_ELLIPSIS = re.compile(r"(?<=[A-Za-zà-ÿ])\.\.\.(?=[A-ZÀ-Þ])")      # it: "Um...Questa" -> "Um... Questa"
FR_PUNCT = re.compile(r"(?<=[A-Za-zÀ-ÿ》])([!?:;]+)(?=\s|⏎|$)")
# correct text of lines 22-27 of st02_t01/Scr101E; a language not listed takes it from the tsv of another language
SCR101 = {
    'es': {22: '¡Yuju! ¡Has jugado bastante bien!⏎¡Buen Duelo!', 23: '¡Creo que mi suerte está cambiando,⏎gracias a ti!',
           24: '¡Tengamos otro duelo!⏎¡Que el espíritu de las cartas te guíe!', 25: '¿Un empate, eh?⏎¡Me debes una revancha!',
           26: '¡Tengamos otro duelo!⏎¡Que el espíritu de las cartas te guíe!', 27: '¡Qué popular soy últimamente!⏎Pero no, gracias.'},
    'it': {26: 'Duelliamo ancora!⏎Che gli spiriti delle carte ti proteggano!'},
}
FROM = {'fr': 'it', 'de': 'fr'}      # the language whose original text contains the right translation


def tsv(l, ja=False):
    r = {}
    for x in open(os.path.join(AUDIT, f'dialoghi_{l}.tsv'), encoding='utf-8', newline='\n').read().split('\n'):
        p = x.split('\t')
        if len(p) >= 2:
            r[p[0]] = (p[1], p[3] if len(p) > 3 else '') if ja else p[1]
    return r


def build(l):
    orig = tsv(l)
    jp = tsv(l, True)
    base = {}
    f = os.path.join(DATA, f'dialogue_corrections_{l}_base.json')
    if os.path.exists(f):
        base = json.load(open(f, encoding='utf-8'))
    touchups = {'exact': {}, 'parts': []}
    f = os.path.join(DATA, f'dialogue_touchups_{l}.json')
    if os.path.exists(f):
        touchups = json.load(open(f, encoding='utf-8'))
    exact = {k: v for k, v in touchups.get('exact', {}).items()}
    parts = [(a, b) for a, b in touchups.get('parts', [])]
    regexes = [(re.compile(a), b) for a, b in touchups.get('regex', [])]      # regular expressions, applied after the parts
    used_parts, used_regexes = [0] * len(parts), [0] * len(regexes)
    special = {}
    for n in range(22, 28):
        i = f'st02_t01/Scr101E#{n}'
        if l in SCR101 and n in SCR101[l]:
            special[i] = SCR101[l][n]
        elif l in FROM and i in orig:
            special[i] = tsv(FROM[l])[i]
        elif l == 'de' and i in orig:
            special[i] = tsv('fr')[i]
    # as dialogues.py does: a line without its own correction but with the same text and the same Japanese as a corrected line inherits it
    inherited = {}
    for i, c in base.items():
        if i in jp:
            inherited.setdefault(jp[i], c['proposed'].replace('\n', '⏎'))
    out = {i: c for i, c in base.items() if i not in orig}      # lines that were empty in the game
    for i, t in orig.items():
        start = base[i]['proposed'].replace('\n', '⏎') if i in base else inherited.get(jp[i], t)
        n = special.get(i, exact.get(start, start))
        for k, (a, b) in enumerate(parts):
            if a in n:
                used_parts[k] += 1
                n = n.replace(a, b)
        for k, (a, b) in enumerate(regexes):
            n, c = a.subn(b, n)
            used_regexes[k] += c
        n = SPACE_BEFORE.sub(' 《', n)
        n = (SPACE_AFTER_DE if l == 'de' else SPACE_AFTER).sub('》 ', n)
        if l == 'fr':
            n = FR_PUNCT.sub(r' \1', n)
        if l == 'it':
            n = IT_ELLIPSIS.sub('... ', n)
        if n != start or i in base:
            out[i] = {'current': base[i]['current'] if i in base else nl(t), 'proposed': nl(n)}
    for k, (a, b) in enumerate(parts):
        if not used_parts[k]:
            print('  WARNING part never applied:', k, repr(a)[:70])
    for k, (a, b) in enumerate(touchups.get('regex', [])):
        if not used_regexes[k]:
            print('  WARNING regex never applied:', repr(a)[:70])
    json.dump(out, open(os.path.join(DATA, f'dialogue_corrections_{l}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(l, len(out), 'corrected lines (of which', len(out) - len(base), 'new compared with the base)')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for l in sys.argv[1:]:
        build(l)
