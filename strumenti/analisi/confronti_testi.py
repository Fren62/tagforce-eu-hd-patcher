"""Dai CSV di `documenta_modifiche.py` scrive i confronti LEGGIBILI originale -> nuovo, con le parole cambiate evidenziate
(~~tolto~~ **aggiunto**): carte_diff.md, dialoghi_diff.md, frasi_duello_diff.md, stringhe_ui_diff.md in documentazione/modifiche_<l>/.
uso: python confronti_testi.py LINGUA"""
import csv, difflib, os, re, sys
B = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
L = sys.argv[1]
D = os.path.join(B, 'documentazione', f'modifiche_{L}')


def rd(n):
    return list(csv.reader(open(os.path.join(D, n), encoding='utf-8-sig'), delimiter=';'))[1:]


def vis(t):
    t = t.strip() if t.strip() else t
    return t.replace(' ', '␣') if not t.strip(' ␣') else t


def diff_parole(a, b):
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


def scrivi(nome, titolo, voci):
    with open(os.path.join(D, nome), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# {titolo}\n\nOgni voce: testo **originale del gioco**, testo **nuovo** e **differenza** con le parole tolte ~~barrate~~ e quelle aggiunte in **grassetto**. '
                f'Generato da `strumenti/analisi/confronti_testi.py` dai CSV di `documenta_modifiche.py`; {len(voci)} voci. (`⏎` = a capo)\n\n')
        for intest, ori, nuo, extra in voci:
            f.write(f'### {intest}\n- Originale: {ori}\n- Nuovo: {nuo}\n- Differenza: {diff_parole(ori, nuo)}\n')
            for e in extra:
                f.write(f'- {e}\n')
            f.write('\n')
    print(nome, len(voci))


scrivi('carte_diff.md', f'Carte ({L}): originale -> nuovo', [(f'{c[0]} - {c[1]} ({c[2]})', c[3], c[4], []) for c in rd('carte.csv')])
scrivi('dialoghi_diff.md', f'Dialoghi ({L}): originale -> nuovo', [(d[0], d[1], d[2], [f'Inglese: {d[3]}'] + ([f'Giapponese: {d[4]}'] if d[4] else [])) for d in rd('dialoghi.csv')])
scrivi('frasi_duello_diff.md', f'Frasi dei duelli ({L}): originale -> nuovo', [(str(n + 1), r[0], r[1], [f'Voci: {r[2]}; archivi: {r[3]}']) for n, r in enumerate(rd('frasi_duello.csv'))])
scrivi('stringhe_ui_diff.md', f"Stringhe dell'interfaccia ({L}): originale -> nuovo", [(f'{r[0]} #{r[1]}', r[2], r[3], [f'Archivi: {r[4]}']) for r in rd('stringhe_ui.csv')])
