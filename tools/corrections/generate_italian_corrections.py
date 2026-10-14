"""Generates data/card_corrections.json: corrections to the Italian texts (name and description) compared with cardinfo_ita.ehp.
usage: generate_italian_corrections.py CARDINFO_ITA.ehp OUT.json [--diff]
The JSON has the form {"<card id>": {"name": "...", "desc": "..."}} with the changed fields only.
Rules: terminology (Campo -> Terreno), typos, grammar, spaces after the apostrophe, missing texts
(compared with the game's English). Every rule is commented with its reason."""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from cardprops import load

POSS = {'tua': 'tuo', 'sua': 'suo', 'loro': 'loro'}
PREP = {'nella': 'sul', 'nel': 'sul', 'sulla': 'sul', 'dalla': 'dal', 'della': 'del', 'alla': 'al'}
FIELD = r'[Cc]ampo(?! magnetico)'    # "campo magnetico" (M-Warrior #2) is another "campo": it must not be touched


def _side(m):
    """'nella tua parte di Campo' -> 'sul tuo Terreno'; 'nella parte di Campo del tuo avversario' -> 'sul Terreno del tuo avversario'"""
    prep, poss = PREP[m.group(1).lower()], m.group(2)
    out = prep + (' ' + POSS[poss] if poss else '') + ' Terreno'
    return out[0].upper() + out[1:] if m.group(1)[0].isupper() else out


def field_to_terreno(t):
    # "in Campo" is always "sul Terreno" in the other 850 cards; "parte di Campo" -> "il tuo Terreno"
    t = re.sub(r'\b(nella|nel|sulla|dalla|della|alla|Nella|Nel|Sulla|Dalla|Della|Alla) (?:(tua|sua|loro) )?(?:parte|lato) (?:di|del) ' + FIELD, _side, t)
    t = re.sub(r'\b(?:nel|Nel) (tuo|suo|loro) lato del ' + FIELD + r'\b', r'sul \1 Terreno', t)   # "nel tuo lato del campo"
    t = re.sub(r'\b(?:in|nel|sul|al) ' + FIELD + r'\b', 'sul Terreno', t)
    t = re.sub(r'\bdal ' + FIELD + r'\b', 'dal Terreno', t)
    t = re.sub(r'\bdel ' + FIELD + r'\b', 'del Terreno', t)
    t = re.sub(r'\b' + FIELD + r'\b', 'Terreno', t)
    return t


# (regex, replacement, reason)
TEXT = [
    (r'"Hydrogeddon"s and ', '"Hydrogeddon" e ', 'untranslated English (Legame - H2O)'),
    (r'\bil questo\b', 'questo', 'article + "questo" (Metal Fiend Token)'),
    (r'\bun Carta\b', 'una Carta', 'masculine article with feminine noun'),
    (r'\bessereusati\b', 'essere usati', 'words stuck together (Trio Ojama)'),
    (r'\bditruggila\b', 'distruggila', 'typo (Bait Doll)'),
    (r'\bun attacc\.', 'un attacco.', 'truncated word (A Hero Emerges)'),
    (r'\bsul Terreo\b', 'sul Terreno', 'typo (Terrorking Archfiend)'),
    (r'\bCarta quipaggiamento\b', 'Carta Equipaggiamento', 'typo (Z-Metal Tank)'),
    (r'\b(Draw|Standby|End|Main|Battle) Phases\b', r'\1 Phase', 'English plural in Italian text'),
    (r"\b(dell|all|nell|sull|dall|quest|quell|un|l|d|sant|bell|anch|nient|buon|tutt|com|gl|nessun|ognun|qualcun|cos|tant|quant|altr)' (?=[A-Za-zÀ-ÿ0-9\"])", r"\1'", "space after the apostrophe"),
]
# quotation marks stuck to a word ("Don Zaloog"e) -> space
QUOTE = [(r'(?<=[A-Za-zÀ-ÿ0-9])"(?=[A-Za-zÀ-ÿ])', None)]

NAMES = {   # card name: typos
    'Fatasma Magico': 'Fantasma Magico',
}

MISSING_DESC = {   # id: full text (the missing parts are translated from the game's English with the terms of the rest of the game)
    5703: 'SCOPRI: Aggiungi 1 carta che includa "Guardiano" nel nome dal tuo Deck alla tua mano. Non puoi aggiungere "Guardiano Celtico", '
          '"Drago Alato #1", "Dragone Alato, Custode della Fortezza #2", "Guardia del Labirinto" o "Guardiano Affidabile".',
    5194: 'Offri 1 mostro sul tuo Terreno come Tributo (escluso questo mostro) durante ogni tua Standby Phase. Se non lo fai, distruggi questa carta. '
          'I mostri usati per un\'Evocazione tramite Tributo, o offerti come Tributo per gli effetti di altre carte, sono esclusi.',
    4029: 'Questa carta scoperta sul Terreno ritorna nella mano del proprietario durante l\'End Phase del tuo turno.',
}


def fix_desc(t):
    t = t.replace('"Hydrogeddon"s and ', '"Hydrogeddon" e ')   # untranslated English (Legame - H2O)
    for pat, rep, _ in TEXT:
        t = re.sub(pat, rep, t)
    t = field_to_terreno(t)
    t = re.sub(r'(?<=[A-Za-zÀ-ÿ0-9])"(?=[A-Za-zÀ-ÿ])', '" ', t)   # stuck quotation marks: "Mondo Toon"sia
    return t


def fix_name(t):
    t = NAMES.get(t, t)
    for pat, rep, reason in TEXT:
        if "space after" in reason:
            t = re.sub(pat, rep, t)
    return t


def build(path):
    cards = load(path)
    out = {}
    for k, c in cards.items():
        new = {}
        d = MISSING_DESC.get(k) or c['desc']
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
    print(len(out), 'corrected cards;', sum('desc' in v for v in out.values()), 'descriptions,', sum('name' in v for v in out.values()), 'names')
    if '--diff' in sys.argv:
        for k, v in sorted(out.items(), key=lambda x: int(x[0])):
            c = cards[int(k)]
            for f in ('name', 'desc'):
                if f in v:
                    print(f'--- {k} {c["name"]} [{f}]')
                    print('  -', c[f].replace('\n', ' / '))
                    print('  +', v[f].replace('\n', ' / '))
