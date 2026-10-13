"""Correzioni ai testi inglesi delle carte (cardinfo_eng.ehp). Solo errori oggettivi: refusi, ortografia incoerente e sviste
grammaticali evidenti (parole omesse). Non si modernizza il testo: le differenze dal testo ufficiale di oggi che sono solo
riformulazioni (\"Tribute\" al posto di \"offer\", \"banish\", \"Extra Deck\"...) non si toccano.
Lettura completa a mano delle 2.479 carte il 2026-10-13 (note in confronti/audit_en/NOTE_LAVORO.md).
Nomi ufficiali con refuso NON toccati: \"Skull Descovery Knight\" (6001), \"Cemetary Bomb\" (6148), \"Bokoichi the Freightening Car\" (6174).
GLOBALI: (regex, sostituzione, motivo) applicate a nomi e descrizioni di tutte le carte (dopo i PER_CARTA).
PER_CARTA: (id, 'name'|'desc', vecchio, nuovo, motivo); il vecchio testo deve esistere esattamente."""

GLOBALI = [
    (r"\bposible\b", "possible", "refuso"),
    (r"\bfortell\b", "foretell", "refuso"),
    (r"\bmistical\b", "mystical", "refuso"),
    (r"\bmassibe\b", "massive", "refuso"),
    (r"\benourmous\b", "enormous", "refuso"),
    (r"\bTrbute\b", "Tribute", "refuso"),
    (r"\btrbute\b", "tribute", "refuso"),
    (r"(?i)\btrbute", "tribute", "refuso (qualunque forma)"),
    (r"\bfliipped\b", "flipped", "refuso"),
    (r"\bDefence\b", "Defense", "ortografia incoerente: il gioco usa \"Defense\" in tutte le altre carte"),
    (r"\bDefensive Position\b", "Defense Position", "terminologia: \"Defense Position\" nel resto del gioco"),
    # --- rilettura completa (2026-10-13) ---
    (r"　(?=\n)", "", "spazio ideografico (giapponese) a fine riga"),
    (r"　", " ", "spazio ideografico (giapponese) al posto dello spazio normale"),
    (r"\bside the field\b", "side of the field", "preposizione omessa (carte Toon)"),
    (r"\byour must select\b", "you must select", "refuso (your/you)"),
    (r"\bcan Inflict Direct Damage\b", "can inflict Direct Damage", "maiuscola a meta' frase"),
    (r"\bBy tributing\b", "By Tributing", "\"Tribute\" ha la maiuscola in tutto il gioco"),
    (r"\bbattle damage\b", "Battle Damage", "\"Battle Damage\" ha le maiuscole in tutto il gioco"),
    (r"\bthis Turn\b", "this turn", "maiuscola incoerente"),
    (r"\bthe Turn\b", "the turn", "maiuscola incoerente"),
    (r"\bthis turns End Phase\b", "this turn's End Phase", "apostrofo del genitivo"),
    (r"\b1card\b", "1 card", "spazio mancante"),
    (r"\byour opponent's Field\b", "your opponent's side of the field", "\"field\" in minuscolo e formula del resto del gioco"),
    (r"\byour Field\b", "your side of the field", "\"field\" in minuscolo e formula del resto del gioco"),
    (r"\bthe Field\b(?! Spell)", "the field", "\"field\" in minuscolo (il resto del gioco)"),
    (r"\byour Hand\b", "your hand", "\"hand\" in minuscolo (il resto del gioco)"),
]

PER_CARTA = [
    (4564, 'desc', "he is a errand boy", "he is an errand boy", "articolo"),
    (4483, 'desc', "with saw-like head", "with a saw-like head", "articolo omesso"),
    (4601, 'desc', "into mirror world", "into a mirror world", "articolo omesso"),
    (4372, 'desc', "a labyrinth no exit", "a labyrinth with no exit", "parola omessa"),
    (5266, 'desc', "The number of monster(s) are applied", "The number of monster(s) is applied", "concordanza"),
    # --- rilettura completa (2026-10-13) ---
    (4232, 'desc', "this monsters grabs", "this monster grabs", "concordanza (plurale al posto del singolare)"),
    (4492, 'desc', "a wealth of spell written", "a wealth of spells written", "plurale mancante"),
    (4546, 'desc', "from your deck", "from your Deck", "maiuscola: \"Deck\" in tutto il gioco"),
    (5062, 'desc', "\"Worm Drake\"+\"Humanoid Slime\"", "\"Worm Drake\" + \"Humanoid Slime\"", "spazi attorno al + come nelle altre fusioni"),
    (5096, 'desc', "your opponents side", "your opponent's side", "apostrofo del genitivo"),
    (5184, 'desc', "\"Don Zaloog\"and", "\"Don Zaloog\" and", "spazio mancante"),
    (5753, 'desc', "your opponent cannot player cannot activate", "your opponent cannot activate", "parole doppie (refuso)"),
    (6007, 'name', "Marshmallon glasses", "Marshmallon Glasses", "nome ufficiale: maiuscola"),
    (6302, 'desc', "from\nyour hand", "from your hand", "a capo in mezzo alla frase"),
    (6639, 'desc', "When this card are successfully", "When this card is successfully", "concordanza"),
    (6640, 'desc', "includes \"sphinx\" in", "includes \"Sphinx\" in", "maiuscola (parte di nome)"),
    (6684, 'desc', "Special Summon 1\"Option Token\"", "Special Summon 1 \"Option Token\"", "spazio mancante"),
    (6229, 'desc', "field, tributing 1 monster", "field, Tributing 1 monster", "\"Tribute\" ha la maiuscola"),
    (6229, 'desc', "that is level 5 or below", "that is Level 5 or below", "\"Level\" ha la maiuscola"),
    # maiuscole incoerenti (testo di un altro traduttore: Monster/Hand/Field a meta' frase)
    (5358, 'desc', "Offer each of your Monsters", "Offer each of your monsters", "maiuscola incoerente"),
    (5367, 'desc', "While that Monster is", "While that monster is", "maiuscola incoerente"),
    (5451, 'desc', "all Monsters on", "all monsters on", "maiuscola incoerente"),
    (5493, 'desc', "your opponent's Monster attacks", "your opponent's monster attacks", "maiuscola incoerente"),
    (5493, 'desc', "Spell and Trap cards", "Spell and Trap Cards", "maiuscola incoerente"),
    (5497, 'desc', "Returns 1 Monster on", "Returns 1 monster on", "maiuscola incoerente"),
    (5497, 'desc', "one Level 4 Monster from", "one Level 4 monster from", "maiuscola incoerente"),
    (5497, 'desc', "to your Hand", "to your hand", "maiuscola incoerente"),
    (5557, 'desc', "when a Monster on", "when a monster on", "maiuscola incoerente"),
    (5557, 'desc', "one Level 4 Monster from", "one Level 4 monster from", "maiuscola incoerente"),
    (5561, 'desc', "Zombie-type card", "Zombie-Type card", "\"Type\" ha la maiuscola"),
    (5561, 'desc', "adding it to your Hand", "adding it to your hand", "maiuscola incoerente"),
    (5743, 'desc', "face-up Monster on", "face-up monster on", "maiuscola incoerente"),
    (5743, 'desc', "when a Monster is destroyed", "when a monster is destroyed", "maiuscola incoerente"),
    (6003, 'desc', "Select 1 Monster in Defense", "Select 1 monster in Defense", "maiuscola incoerente"),
    (6231, 'desc', "each Monster on", "each monster on", "maiuscola incoerente"),
    (6288, 'desc', "selecting 1 Monster face-up", "selecting 1 monster face-up", "maiuscola incoerente"),
    (6288, 'desc', "the selected Monster's ATK", "the selected monster's ATK", "maiuscola incoerente"),
    (6288, 'desc', "every other Monster face-up", "every other monster face-up", "maiuscola incoerente"),
    (6288, 'desc', "other Monsters in face-up", "other monsters in face-up", "maiuscola incoerente"),
    (6291, 'desc', "Zombie-Type Monster with", "Zombie-Type monster with", "maiuscola incoerente"),
    (6291, 'desc', "The selected Monster will", "The selected monster will", "maiuscola incoerente"),
    (6450, 'desc', "all Monster cards in", "all Monster Cards in", "maiuscola incoerente"),
]
