"""Elenco delle frasi dei personaggi nei duelli (chr_wordstbl) di una lingua, senza doppioni, con il testo inglese accanto e con le
correzioni gia' applicate (dati/correzioni_frasi_duello_<l>.json). Serve per la rilettura a mano: leggi, annota gli errori e aggiungi
"esatte"/"parti" a quel json, poi rilancia per controllare.
uso: python estrai_frasi_duello.py ISO_ORIGINALE LINGUA OUT.txt        LINGUA = it|fr|de|es|en
Formato: indice <TAB> frase <TAB> inglese   (a capo scritti ⏎)"""
import io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'correzioni')); sys.path.insert(0, os.path.join(HERE, '..'))
import pycdlib
import applica_iso as ai
import frasi_duello as fd
import lingue

iso, lang, out = sys.argv[1:4]
let, en = lingue.LINGUE[lang][1], lingue.LINGUE['en'][1]
c = fd.carica(lang)
esatte, parti = c if c else ({}, [])
I = pycdlib.PyCdlib(); I.open(iso)
visti = {}
for ch in I.list_children(iso_path='/PSP_GAME/USRDIR/duel'):
    nome = ch.file_identifier().decode().split(';')[0]
    if not nome.endswith('.ehp'):
        continue
    b = io.BytesIO(); I.get_file_from_iso_fp(b, iso_path='/PSP_GAME/USRDIR/duel/' + nome)
    try:
        _, f = ai.apri(b.getvalue())
    except Exception:
        continue
    for k in f:
        m = re.match(rf'(02)?chr_wordstbl_{let}\.bin$', k)
        if not m:
            continue
        ke = f'{m.group(1) or ""}chr_wordstbl_{en}.bin'
        if ke not in f:
            continue
        for t, e in zip(fd.tabella(bytes(f[k])), fd.tabella(bytes(f[ke]))):
            u = esatte.get(t, t)
            for a, b2 in parti:
                u = u.replace(a, b2)
            visti.setdefault(u, e)
with open(out, 'w', encoding='utf-8', newline='\n') as o:
    for i, (u, e) in enumerate(sorted(visti.items())):
        o.write(f"{i}\t{u.replace(chr(10), '⏎')}\t{e.replace(chr(10), '⏎')}\n")
print(len(visti), 'frasi uniche ->', out)
