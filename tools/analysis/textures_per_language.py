"""Lists the game textures that have their own version for the chosen language (i.e. those to be redrawn in the HD interface).

For every .ehp archive of the extracted USRDIR the GIM textures are read and the data hash is computed (the key PPSSPP uses in textures.ini).
Archives and members are grouped by removing the language mark from the name (all_i.ehp / all_f.ehp, window_i0009 / window_f0009,
always_bri_ita / always_bri_fra, basic_ii / basic_ff ...). In every group the language's version is compared with the English and Italian ones:
  DIVERSA   hash different from English: the texture contains the language's own text (or pixels) -> to be redrawn
  =ING      same hash as English: no work (the English pack already covers it)
  =ITA      same hash as Italian but different from English: if Italian has been redrawn (it exists in PSP/TEXTURES/ULES00600/ui_it), it holds for the language too
It is needed to understand HOW MANY textures there are to do and in which archives, before touching the `ui_textures/*.py` scripts.

usage: textures_per_language.py USRDIR LANGUAGE [--only-different]        LANGUAGE = it|fr|de|es|en
Writes the table on stdout: archive | member | language hash | English hash | Italian hash | outcome | redrawn in ui_it (yes/no)

Warning: it is a heuristic on the names. Always check the listed textures by eye (dump with tools/analysis/dump4.py) and remember that some
languages share the same archive (basic_if / basic_ff / basic_bf are identical: basic_<letter><letter> is used)."""
import os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'ui_textures'))
from ehp import read
import gim

LET = {'it': 'i', 'fr': 'f', 'de': 'g', 'es': 's', 'en': 'e'}
LET3 = {'it': 'ita', 'fr': 'fra', 'de': 'ger', 'es': 'spa', 'en': 'eng'}


def per_language(name, letter, tre):
    """name with the language mark replaced by '*' (None if the name does not have that language's mark)"""
    n = name
    n2 = re.sub(r'(?<![a-z])' + tre + r'(?![a-z])', '*', n)
    if n2 != n:
        return n2
    n2 = re.sub(r'basic_' + letter + letter, 'basic_**', n)
    if n2 != n:
        return n2
    n2 = re.sub(r'(?<=_)' + letter + r'(?=\.ehp$|\.gim$|\d{4}|\.|_)', '*', n)
    return n2 if n2 != n else None


def main():
    usr, language = sys.argv[1:3]
    only = '--only-different' in sys.argv
    L, T = LET[language], LET3[language]
    # textures already redrawn for Italian (hash from the base pack's ui_it folder)
    ini = glob.glob(os.path.join(HERE, '..', '..', 'PSP', 'TEXTURES', 'ULES00600', 'ui_it', '*.ini'))
    hash_it = set()
    for f in ini:
        for row in open(f, encoding='utf-8'):
            m = re.match(r'^0{16}([0-9a-f]{8})\s*=', row)
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
            for letter, tre in ((x, LET3[c]) for c, x in LET.items()):
                an = per_language(rel, letter, tre)
                mn = per_language(k, letter, tre)
                if an is None and mn is None:
                    continue
                key = (an or rel, mn or k)
                tab.setdefault(key, {})[letter] = h
    rows = []
    for (a, m), d in sorted(tab.items()):
        if L not in d:
            continue
        e, i = d.get('e'), d.get('i')
        outcome = 'DIFFERENT' if L != 'e' and d[L] != e else ('=ENG' if d[L] == e else '-')
        if outcome == 'DIFFERENT' and i and d[L] == i and L != 'i':
            outcome = '=ITA'
        if only and outcome != 'DIFFERENT':
            continue
        rows.append((a, m, d[L], e, i, outcome, 'yes' if i in hash_it else 'no'))
    for r in rows:
        print(' | '.join(str(x) for x in r))
    print('#', len(rows), 'texture', file=sys.stderr)


if __name__ == '__main__':
    main()
