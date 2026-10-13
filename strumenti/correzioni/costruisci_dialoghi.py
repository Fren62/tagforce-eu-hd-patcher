"""Genera dati/correzioni_dialoghi_<lingua>.json (id -> attuale, proposto) per dialoghi.py a partire da:
  - i dialoghi originali (confronti/audit_dialoghi/dialoghi_<lingua>.tsv, estratti con audit/estrai_dialoghi.py dalla ISO originale)
  - dati/correzioni_dialoghi_<lingua>_base.json (solo it: la revisione completa fatta a mano)
  - dati/ritocchi_dialoghi_<lingua>.json  {"esatte": {riga: nuova}, "parti": [[vecchio, nuovo]]}  (a capo scritti ⏎)
  - regole automatiche: spazi attorno ai segnaposto 《...》 e (solo fr) spazio prima di ! ? : ;
  - la scena st02_t01/Scr101E righe 22-27: nel gioco originale il testo e' ruotato tra le lingue (it ha francese, fr tedesco,
    de inglese, es italiano); si rimette ognuno nella sua lingua.
usage: costruisci_dialoghi.py LINGUA [LINGUA ...]"""
import json, os, re, sys
QUI = os.path.dirname(os.path.abspath(__file__))
DATI = os.path.join(QUI, '..', 'dati')
AUD = os.path.join(QUI, '..', '..', 'confronti', 'audit_dialoghi')
nl = lambda s: s.replace('⏎', '\n')
SPAZIO_PRIMA = re.compile(r"(?<=[A-Za-zÀ-ÿ,;:!?])《")
SPAZIO_DOPO = re.compile(r"》(?=[A-Za-zÀ-ÿ])")
SPAZIO_DOPO_DE = re.compile(r"》(?!s(?![A-Za-zÀ-ÿ]))(?=[A-Za-zÀ-ÿ])")
IT_PUNTINI = re.compile(r"(?<=[A-Za-zà-ÿ])\.\.\.(?=[A-ZÀ-Þ])")      # it: "Um...Questa" -> "Um... Questa"
FR_PUNT = re.compile(r"(?<=[A-Za-zÀ-ÿ》])([!?:;]+)(?=\s|⏎|$)")
# testo corretto delle righe 22-27 di st02_t01/Scr101E; None = si prende dal tsv di un'altra lingua
SCR101 = {
    'es': {22: '¡Yuju! ¡Has jugado bastante bien!⏎¡Buen Duelo!', 23: '¡Creo que mi suerte está cambiando,⏎gracias a ti!',
           24: '¡Tengamos otro duelo!⏎¡Que el espíritu de las cartas te guíe!', 25: '¿Un empate, eh?⏎¡Me debes una revancha!',
           26: '¡Tengamos otro duelo!⏎¡Que el espíritu de las cartas te guíe!', 27: '¡Qué popular soy últimamente!⏎Pero no, gracias.'},
    'it': {26: 'Duelliamo ancora!⏎Che gli spiriti delle carte ti proteggano!'},
}
DA = {'fr': 'it', 'de': 'fr'}      # la lingua il cui testo originale contiene la traduzione giusta


def tsv(l, ja=False):
    r = {}
    for x in open(os.path.join(AUD, f'dialoghi_{l}.tsv'), encoding='utf-8', newline='\n').read().split('\n'):
        p = x.split('\t')
        if len(p) >= 2:
            r[p[0]] = (p[1], p[3] if len(p) > 3 else '') if ja else p[1]
    return r


def costruisci(l):
    orig = tsv(l)
    jp = tsv(l, True)
    base = {}
    f = os.path.join(DATI, f'correzioni_dialoghi_{l}_base.json')
    if os.path.exists(f):
        base = json.load(open(f, encoding='utf-8'))
    rit = {'esatte': {}, 'parti': []}
    f = os.path.join(DATI, f'ritocchi_dialoghi_{l}.json')
    if os.path.exists(f):
        rit = json.load(open(f, encoding='utf-8'))
    esatte = {k: v for k, v in rit.get('esatte', {}).items()}
    parti = [(a, b) for a, b in rit.get('parti', [])]
    regex = [(re.compile(a), b) for a, b in rit.get('regex', [])]      # espressioni regolari, applicate dopo le parti
    uso_p, uso_r = [0] * len(parti), [0] * len(regex)
    speciali = {}
    for n in range(22, 28):
        i = f'st02_t01/Scr101E#{n}'
        if l in SCR101 and n in SCR101[l]:
            speciali[i] = SCR101[l][n]
        elif l in DA and i in orig:
            speciali[i] = tsv(DA[l])[i]
        elif l == 'de' and i in orig:
            speciali[i] = tsv('fr')[i]
    # come fa dialoghi.py: una riga senza correzione propria ma con stesso testo e stesso giapponese di una riga corretta la eredita
    ereditate = {}
    for i, c in base.items():
        if i in jp:
            ereditate.setdefault(jp[i], c['proposto'].replace('\n', '⏎'))
    out = {i: c for i, c in base.items() if i not in orig}      # righe che nel gioco erano vuote
    for i, t in orig.items():
        partenza = base[i]['proposto'].replace('\n', '⏎') if i in base else ereditate.get(jp[i], t)
        n = speciali.get(i, esatte.get(partenza, partenza))
        for k, (a, b) in enumerate(parti):
            if a in n:
                uso_p[k] += 1
                n = n.replace(a, b)
        for k, (a, b) in enumerate(regex):
            n, c = a.subn(b, n)
            uso_r[k] += c
        n = SPAZIO_PRIMA.sub(' 《', n)
        n = (SPAZIO_DOPO_DE if l == 'de' else SPAZIO_DOPO).sub('》 ', n)
        if l == 'fr':
            n = FR_PUNT.sub(r' \1', n)
        if l == 'it':
            n = IT_PUNTINI.sub('... ', n)
        if n != partenza or i in base:
            out[i] = {'attuale': base[i]['attuale'] if i in base else nl(t), 'proposto': nl(n)}
    for k, (a, b) in enumerate(parti):
        if not uso_p[k]:
            print('  AVVISO parte mai applicata:', k, repr(a)[:70])
    for k, (a, b) in enumerate(rit.get('regex', [])):
        if not uso_r[k]:
            print('  AVVISO regex mai applicata:', repr(a)[:70])
    json.dump(out, open(os.path.join(DATI, f'correzioni_dialoghi_{l}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(l, len(out), 'righe corrette (di cui', len(out) - len(base), 'nuove rispetto alla base)')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    for l in sys.argv[1:]:
        costruisci(l)
