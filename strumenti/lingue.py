"""Dati per lingua dei generatori delle carte HD (it, fr, de, es, en): i testi vengono dal gioco stesso.
La lingua si sceglie con TF1_LANG (it|fr|de|es|en); se manca, la si ricava da un argomento 'cardinfo_xxx.ehp'; default it.
Tipi, forme '/Effetto' ed etichette Magia/Trappola sono nella tabella DLG_Text_* di ogni cardinfo_xxx.ehp (indici 501..559)."""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ehp import read

# codice -> nome del file cardinfo, lettera usata dai nomi dei file/hash del gioco, lettera della tabella
LINGUE = {'it': ('ita', 'i', 'I'), 'fr': ('fra', 'f', 'F'), 'de': ('ger', 'g', 'G'), 'es': ('spa', 's', 'S'), 'en': ('eng', 'e', 'E')}
DA_FILE = {v[0]: k for k, v in LINGUE.items()}
# hash dei dati della striscia 128x32 delle etichette (card_spell_trap.gim di field/always_<lingua>_<lingua>.ehp), vedi estrai_etichette.py
ETICHETTA_HASH = {'it': '9622cd75', 'fr': '6fd4b083', 'de': 'be08846c', 'es': '5e3d2ddd', 'en': 'c2268340'}
PICCOLE = ('de', 'du', 'des', 'la', 'le', 'les', 'en', 'et')      # parole che nei nomi delle etichette restano minuscole (es. "Carta de Trampa")


def corrente():
    l = os.environ.get('TF1_LANG')
    if l:
        return l
    for a in [os.environ.get('TF1_EHP', '')] + sys.argv:
        m = re.search(r'cardinfo_(\w{3})\.ehp$', a)
        if m and m.group(1) in DA_FILE:
            return DA_FILE[m.group(1)]
    return 'it'


def ehp_corrente():
    """percorso del cardinfo_xxx.ehp della lingua corrente: TF1_EHP oppure l'argomento della riga di comando."""
    if os.environ.get('TF1_EHP'):
        return os.environ['TF1_EHP']
    return next((a for a in sys.argv if re.search(r'cardinfo_\w{3}\.ehp$', a)), None)


def dlg(ehp):
    """tabella DLG_Text della lingua dell'archivio: lista di stringhe (indice = indice del gioco)."""
    f = read(ehp)
    L = next(k[-5] for k in f if k.startswith('CARD_Name_'))
    idx, txt = f[f'DLG_Indx_{L}.bin'], f[f'DLG_Text_{L}.bin']
    out = []
    for o in struct.unpack(f'<{len(idx) // 4}I', idx):
        e = o
        while txt[e:e + 2] != b'\0\0' and e < len(txt):
            e += 2
        out.append(txt[o:e].decode('utf-16-le', 'replace'))
    return out


def _titolo(s):
    w = s.lower().split()
    return ' '.join(x if (i and x in PICCOLE) else x[:1].upper() + x[1:] for i, x in enumerate(w))


def termini(ehp):
    """(TIPO {1..21: nome}, KIND {1..9: '/Effetto'...}, parola Magia, parola Trappola) dal gioco."""
    d = dlg(ehp)
    tipo = {i + 1: d[501 + i] for i in range(21)}
    kind = {0: '', **{i + 1: d[551 + i] for i in range(9)}}
    return tipo, kind, _titolo(d[522]), _titolo(d[523])


def etichetta(ehp):
    """parole dell'etichetta Magia / Trappola, per i commenti."""
    t = termini(ehp)
    return f'{t[2]}] / [{t[3]}'


if __name__ == '__main__':
    t, k, s, tr = termini(sys.argv[1])
    print(t, k, s, tr, sep='\n')
