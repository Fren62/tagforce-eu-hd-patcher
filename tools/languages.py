"""Per-language data for the HD card generators (it, fr, de, es, en): the texts come from the game itself.
The language is chosen with TF1_LANG (it|fr|de|es|en); if missing, it is derived from a 'cardinfo_xxx.ehp' argument; default it.
Card types, '/Effect' forms and Spell/Trap labels are in the DLG_Text_* table of every cardinfo_xxx.ehp (indexes 501..559)."""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ehp import read

# code -> cardinfo file name, letter used by the game's file names/hashes, letter of the table
LANGUAGES = {'it': ('ita', 'i', 'I'), 'fr': ('fra', 'f', 'F'), 'de': ('ger', 'g', 'G'), 'es': ('spa', 's', 'S'), 'en': ('eng', 'e', 'E')}
CODE_FROM_FILE = {v[0]: k for k, v in LANGUAGES.items()}
# hash of the data of the 128x32 label strip (card_spell_trap.gim of field/always_<language>_<language>.ehp), see extract_labels.py
LABEL_HASH = {'it': '9622cd75', 'fr': '6fd4b083', 'de': 'be08846c', 'es': '5e3d2ddd', 'en': 'c2268340'}
LOWERCASE_WORDS = ('de', 'du', 'des', 'la', 'le', 'les', 'en', 'et')      # words that stay lowercase in label names (e.g. "Carta de Trampa")


def current():
    """Code of the current language: TF1_LANG, else from a cardinfo_xxx.ehp command-line argument, else 'it'."""
    lang = os.environ.get('TF1_LANG')
    if lang:
        return lang
    for a in [os.environ.get('TF1_EHP', '')] + sys.argv:
        m = re.search(r'cardinfo_(\w{3})\.ehp$', a)
        if m and m.group(1) in CODE_FROM_FILE:
            return CODE_FROM_FILE[m.group(1)]
    return 'it'


def current_ehp():
    """Path of the cardinfo_xxx.ehp of the current language: TF1_EHP or the command-line argument."""
    if os.environ.get('TF1_EHP'):
        return os.environ['TF1_EHP']
    return next((a for a in sys.argv if re.search(r'cardinfo_\w{3}\.ehp$', a)), None)


def dlg(ehp):
    """DLG_Text table of the archive's language: list of strings (index = the game's index)."""
    f = read(ehp)
    table_letter = next(k[-5] for k in f if k.startswith('CARD_Name_'))
    idx, txt = f[f'DLG_Indx_{table_letter}.bin'], f[f'DLG_Text_{table_letter}.bin']
    out = []
    for o in struct.unpack(f'<{len(idx) // 4}I', idx):
        e = o
        while txt[e:e + 2] != b'\0\0' and e < len(txt):
            e += 2
        out.append(txt[o:e].decode('utf-16-le', 'replace'))
    return out


def _title_case(s):
    words = s.lower().split()
    return ' '.join(x if (i and x in LOWERCASE_WORDS) else x[:1].upper() + x[1:] for i, x in enumerate(words))


def terms(ehp):
    """(TYPE {1..21: name}, KIND {1..9: '/Effect'...}, word for Spell, word for Trap) from the game."""
    d = dlg(ehp)
    card_type = {i + 1: d[501 + i] for i in range(21)}
    kind = {0: '', **{i + 1: d[551 + i] for i in range(9)}}
    return card_type, kind, _title_case(d[522]), _title_case(d[523])


def label(ehp):
    """Words of the Spell / Trap label, for comments."""
    t = terms(ehp)
    return f'{t[2]}] / [{t[3]}'


if __name__ == '__main__':
    t, k, s, tr = terms(sys.argv[1])
    print(t, k, s, tr, sep='\n')
