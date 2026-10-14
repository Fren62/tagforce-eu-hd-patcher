"""From the CSVs of `document_changes.py` writes the READABLE original -> new comparisons, with the changed words highlighted
(~~removed~~ **added**): cards_diff.md, dialogues_diff.md, duel_lines_diff.md, ui_strings_diff.md in docs/changes_<l>/.
usage: python text_comparisons.py LANGUAGE"""
import csv, difflib, os, re, sys
B = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
L = sys.argv[1]
D = os.path.join(B, 'docs', f'changes_{L}')


def rd(n):
    return list(csv.reader(open(os.path.join(D, n), encoding='utf-8-sig'), delimiter=';'))[1:]


def vis(t):
    t = t.strip() if t.strip() else t
    return t.replace(' ', '␣') if not t.strip(' ␣') else t


def diff_words(a, b):
    ta, tb = re.findall(r'\s+|\w+|[^\w\s]', a), re.findall(r'\s+|\w+|[^\w\s]', b)
    r = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes():
        if op == 'equal':
            r.append(''.join(ta[i1:i2]))
        else:
            if i2 > i1:
                r.append(' ~~' + vis(''.join(ta[i1:i2])) + '~~ ')
            if j2 > j1:
                r.append(' **' + vis(''.join(tb[j1:j2])) + '** ')
    return re.sub(r' {2,}', ' ', ''.join(r))


def write_file(name, title, entries):
    with open(os.path.join(D, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# {title}\n\nOgni voce: testo **originale del gioco**, testo **nuovo** e **differenza** con le parole tolte ~~barrate~~ e quelle aggiunte in **grassetto**. '
                f'Generato da `tools/analysis/text_comparisons.py` dai CSV di `document_changes.py`; {len(entries)} voci. (`⏎` = a capo)\n\n')
        for header, orig, new, extra in entries:
            f.write(f'### {header}\n- Originale: {orig}\n- Nuovo: {new}\n- Differenza: {diff_words(orig, new)}\n')
            for e in extra:
                f.write(f'- {e}\n')
            f.write('\n')
    print(name, len(entries))


write_file('cards_diff.md', f'Carte ({L}): originale -> nuovo', [(f'{c[0]} - {c[1]} ({c[2]})', c[3], c[4], []) for c in rd('cards.csv')])
write_file('dialogues_diff.md', f'Dialoghi ({L}): originale -> nuovo', [(d[0], d[1], d[2], [f'Inglese: {d[3]}'] + ([f'Giapponese: {d[4]}'] if d[4] else [])) for d in rd('dialogues.csv')])
write_file('duel_lines_diff.md', f'Frasi dei duelli ({L}): originale -> nuovo', [(str(n + 1), r[0], r[1], [f'Voci: {r[2]}; archivi: {r[3]}']) for n, r in enumerate(rd('duel_lines.csv'))])
write_file('ui_strings_diff.md', f"Stringhe dell'interfaccia ({L}): originale -> nuovo", [(f'{r[0]} #{r[1]}', r[2], r[3], [f'Archivi: {r[4]}']) for r in rd('ui_strings.csv')])
