"""List of the characters' sentences in the duels (chr_wordstbl) of a language, without duplicates, with the English text beside and with the
corrections already applied (data/duel_line_corrections_<l>.json). It is for the hand reading: read, note the errors and add
"exact"/"parts" to that json, then rerun to check.
usage: python extract_duel_lines.py ORIGINAL_ISO LANGUAGE OUT.txt        LANGUAGE = it|fr|de|es|en
Format: index <TAB> sentence <TAB> English   (line breaks written as ⏎)"""
import io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'corrections')); sys.path.insert(0, os.path.join(HERE, '..'))
import pycdlib
import apply_to_iso as ai
import duel_lines as fd
import languages

iso, lang, out = sys.argv[1:4]
let, en = languages.LANGUAGES[lang][1], languages.LANGUAGES['en'][1]
c = fd.load(lang)
exact, parts = c if c else ({}, [])
I = pycdlib.PyCdlib(); I.open(iso)
seen = {}
for ch in I.list_children(iso_path='/PSP_GAME/USRDIR/duel'):
    name = ch.file_identifier().decode().split(';')[0]
    if not name.endswith('.ehp'):
        continue
    b = io.BytesIO(); I.get_file_from_iso_fp(b, iso_path='/PSP_GAME/USRDIR/duel/' + name)
    try:
        _, f = ai.open_ehp(b.getvalue())
    except Exception:
        continue
    for k in f:
        m = re.match(rf'(02)?chr_wordstbl_{let}\.bin$', k)
        if not m:
            continue
        ke = f'{m.group(1) or ""}chr_wordstbl_{en}.bin'
        if ke not in f:
            continue
        for t, e in zip(fd.read_table(bytes(f[k])), fd.read_table(bytes(f[ke]))):
            u = exact.get(t, t)
            for a, b2 in parts:
                u = u.replace(a, b2)
            seen.setdefault(u, e)
with open(out, 'w', encoding='utf-8', newline='\n') as o:
    for i, (u, e) in enumerate(sorted(seen.items())):
        o.write(f"{i}\t{u.replace(chr(10), '⏎')}\t{e.replace(chr(10), '⏎')}\n")
print(len(seen), 'frasi uniche ->', out)
