"""Genera dati/correzioni_carte.json: correzioni ai testi italiani (nome e descrizione) rispetto a cardinfo_ita.ehp.
usage: genera_correzioni.py CARDINFO_ITA.ehp OUT.json [--diff]
Il JSON ha la forma {"<id carta>": {"name": "...", "desc": "..."}} con i soli campi cambiati.
Regole: terminologia (Campo -> Terreno), refusi, grammatica, spazi dopo l'apostrofo, testi mancanti
(rispetto all'inglese del gioco). Ogni regola e' commentata con il motivo."""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from cardprops import load

POSS = {'tua': 'tuo', 'sua': 'suo', 'loro': 'loro'}
PREP = {'nella': 'sul', 'nel': 'sul', 'sulla': 'sul', 'dalla': 'dal', 'della': 'del', 'alla': 'al'}
CAMPO = r'[Cc]ampo(?! magnetico)'    # "campo magnetico" (M-Warrior #2) e' un altro "campo": non va toccato


def _side(m):
    """'nella tua parte di Campo' -> 'sul tuo Terreno'; 'nella parte di Campo del tuo avversario' -> 'sul Terreno del tuo avversario'"""
    prep, poss = PREP[m.group(1).lower()], m.group(2)
    out = prep + (' ' + POSS[poss] if poss else '') + ' Terreno'
    return out[0].upper() + out[1:] if m.group(1)[0].isupper() else out


def campo_terreno(t):
    # "in Campo" e' sempre "sul Terreno" nelle altre 850 carte; "parte di Campo" -> "il tuo Terreno"
    t = re.sub(r'\b(nella|nel|sulla|dalla|della|alla|Nella|Nel|Sulla|Dalla|Della|Alla) (?:(tua|sua|loro) )?(?:parte|lato) (?:di|del) ' + CAMPO, _side, t)
    t = re.sub(r'\b(?:nel|Nel) (tuo|suo|loro) lato del ' + CAMPO + r'\b', r'sul \1 Terreno', t)   # "nel tuo lato del campo"
    t = re.sub(r'\b(?:in|nel|sul|al) ' + CAMPO + r'\b', 'sul Terreno', t)
    t = re.sub(r'\bdal ' + CAMPO + r'\b', 'dal Terreno', t)
    t = re.sub(r'\bdel ' + CAMPO + r'\b', 'del Terreno', t)
    t = re.sub(r'\b' + CAMPO + r'\b', 'Terreno', t)
    return t


# (regex, sostituzione, motivo)
TESTO = [
    (r'"Hydrogeddon"s and ', '"Hydrogeddon" e ', 'inglese non tradotto (Legame - H2O)'),
    (r'\bil questo\b', 'questo', 'articolo + "questo" (Metal Fiend Token)'),
    (r'\bun Carta\b', 'una Carta', 'articolo maschile con nome femminile'),
    (r'\bessereusati\b', 'essere usati', 'parole attaccate (Trio Ojama)'),
    (r'\bditruggila\b', 'distruggila', 'refuso (Bait Doll)'),
    (r'\bun attacc\.', 'un attacco.', 'parola troncata (A Hero Emerges)'),
    (r'\bsul Terreo\b', 'sul Terreno', 'refuso (Terrorking Archfiend)'),
    (r'\bCarta quipaggiamento\b', 'Carta Equipaggiamento', 'refuso (Z-Metal Tank)'),
    (r'\b(Draw|Standby|End|Main|Battle) Phases\b', r'\1 Phase', 'plurale inglese in testo italiano'),
    (r"\b(dell|all|nell|sull|dall|quest|quell|un|l|d|sant|bell|anch|nient|buon|tutt|com|gl|nessun|ognun|qualcun|cos|tant|quant|altr)' (?=[A-Za-zÀ-ÿ0-9\"])", r"\1'", "spazio dopo l'apostrofo"),
]
# virgolette attaccate a una parola ("Don Zaloog"e) -> spazio
QUOTE = [(r'(?<=[A-Za-zÀ-ÿ0-9])"(?=[A-Za-zÀ-ÿ])', None)]

NOMI = {   # nome carta: refusi
    'Fatasma Magico': 'Fantasma Magico',
}

DESC_MANCANTE = {   # id: testo completo (le parti mancanti sono tradotte dall'inglese del gioco con i termini del resto del gioco)
    5703: 'SCOPRI: Aggiungi 1 carta che includa "Guardiano" nel nome dal tuo Deck alla tua mano. Non puoi aggiungere "Guardiano Celtico", '
          '"Drago Alato #1", "Dragone Alato, Custode della Fortezza #2", "Guardia del Labirinto" o "Guardiano Affidabile".',
    5194: 'Offri 1 mostro sul tuo Terreno come Tributo (escluso questo mostro) durante ogni tua Standby Phase. Se non lo fai, distruggi questa carta. '
          'I mostri usati per un\'Evocazione tramite Tributo, o offerti come Tributo per gli effetti di altre carte, sono esclusi.',
    4029: 'Questa carta scoperta sul Terreno ritorna nella mano del proprietario durante l\'End Phase del tuo turno.',
}


def fix_desc(t):
    t = t.replace('"Hydrogeddon"s and ', '"Hydrogeddon" e ')   # inglese non tradotto (Legame - H2O)
    for pat, rep, _ in TESTO:
        t = re.sub(pat, rep, t)
    t = campo_terreno(t)
    t = re.sub(r'(?<=[A-Za-zÀ-ÿ0-9])"(?=[A-Za-zÀ-ÿ])', '" ', t)   # virgolette attaccate: "Mondo Toon"sia
    return t


def fix_name(t):
    t = NOMI.get(t, t)
    for pat, rep, _ in TESTO:
        if "spazio dopo" in _:
            t = re.sub(pat, rep, t)
    return t


def build(path):
    cards = load(path); out = {}
    for k, c in cards.items():
        new = {}
        d = DESC_MANCANTE.get(k) or c['desc']
        d2 = fix_desc(d)
        if d2 != c['desc']:
            new['desc'] = d2
        n2 = fix_name(c['name'])
        if n2 != c['name']:
            new['name'] = n2
        if new:
            out[str(k)] = new
    return cards, out


if __name__ == '__main__':
    cards, out = build(sys.argv[1])
    json.dump(out, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    print(len(out), 'carte corrette;', sum('desc' in v for v in out.values()), 'descrizioni,', sum('name' in v for v in out.values()), 'nomi')
    if '--diff' in sys.argv:
        for k, v in sorted(out.items(), key=lambda x: int(x[0])):
            c = cards[int(k)]
            for f in ('name', 'desc'):
                if f in v:
                    print(f'--- {k} {c["name"]} [{f}]'); print('  -', c[f].replace('\n', ' / ')); print('  +', v[f].replace('\n', ' / '))
