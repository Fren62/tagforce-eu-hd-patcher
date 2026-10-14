"""Corrections to the English card texts (cardinfo_eng.ehp). Objective errors only: typos, inconsistent spelling and obvious grammar slips (omitted words).
The text is not modernised: differences from today's official text that are mere rewordings
("Tribute" instead of "offer", "banish", "Extra Deck"...) are left alone.
Complete hand reading of the 2,479 cards on 2026-10-13 (notes in comparisons/audit_en/NOTE_LAVORO.md).
Official names with typos NOT touched: "Skull Descovery Knight" (6001), "Cemetary Bomb" (6148), "Bokoichi the Freightening Car" (6174).
GLOBALS: (regex, replacement, reason) applied to the names and descriptions of all the cards.
PER_CARD: (id, 'name'|'desc', old, new, reason); the old text must exist exactly."""

GLOBALS = [
    (r"\bposible\b", "possible", "typo"),
    (r"\bfortell\b", "foretell", "typo"),
    (r"\bmistical\b", "mystical", "typo"),
    (r"\bmassibe\b", "massive", "typo"),
    (r"\benourmous\b", "enormous", "typo"),
    (r"\bTrbute\b", "Tribute", "typo"),
    (r"\btrbute\b", "tribute", "typo"),
    (r"(?i)\btrbute", "tribute", "typo (any form)"),
    (r"\bfliipped\b", "flipped", "typo"),
    (r"\bDefence\b", "Defense", "inconsistent spelling: the game uses \"Defense\" in all the other cards"),
    (r"\bDefensive Position\b", "Defense Position", "terminology: \"Defense Position\" in the rest of the game"),
    # --- complete re-reading (2026-10-13) ---
    (r"　(?=\n)", "", "ideographic space (Japanese) at the end of the line"),
    (r"　", " ", "ideographic space (Japanese) instead of a normal space"),
    (r"\bside the field\b", "side of the field", "omitted preposition (Toon cards)"),
    (r"\byour must select\b", "you must select", "typo (your/you)"),
    (r"\bcan Inflict Direct Damage\b", "can inflict Direct Damage", "capital letter mid-sentence"),
    (r"\bBy tributing\b", "By Tributing", "\"Tribute\" is capitalized throughout the game"),
    (r"\bbattle damage\b", "Battle Damage", "\"Battle Damage\" is capitalized throughout the game"),
    (r"\bthis Turn\b", "this turn", "inconsistent capitalization"),
    (r"\bthe Turn\b", "the turn", "inconsistent capitalization"),
    (r"\bthis turns End Phase\b", "this turn's End Phase", "genitive apostrophe"),
    (r"\b1card\b", "1 card", "missing space"),
    (r"\byour opponent's Field\b", "your opponent's side of the field", "\"field\" in lowercase and wording of the rest of the game"),
    (r"\byour Field\b", "your side of the field", "\"field\" in lowercase and wording of the rest of the game"),
    (r"\bthe Field\b(?! Spell)", "the field", "\"field\" in lowercase (the rest of the game)"),
    (r"\byour Hand\b", "your hand", "\"hand\" in lowercase (the rest of the game)"),
]

PER_CARD = [
    (4564, 'desc', "he is a errand boy", "he is an errand boy", "article"),
    (4483, 'desc', "with saw-like head", "with a saw-like head", "omitted article"),
    (4601, 'desc', "into mirror world", "into a mirror world", "omitted article"),
    (4372, 'desc', "a labyrinth no exit", "a labyrinth with no exit", "omitted word"),
    (5266, 'desc', "The number of monster(s) are applied", "The number of monster(s) is applied", "agreement"),
    # --- complete re-reading (2026-10-13) ---
    (4232, 'desc', "this monsters grabs", "this monster grabs", "agreement (plural instead of singular)"),
    (4492, 'desc', "a wealth of spell written", "a wealth of spells written", "missing plural"),
    (4546, 'desc', "from your deck", "from your Deck", "capital letter: \"Deck\" throughout the game"),
    (5062, 'desc', "\"Worm Drake\"+\"Humanoid Slime\"", "\"Worm Drake\" + \"Humanoid Slime\"", "spaces around the + as in the other fusions"),
    (5096, 'desc', "your opponents side", "your opponent's side", "genitive apostrophe"),
    (5184, 'desc', "\"Don Zaloog\"and", "\"Don Zaloog\" and", "missing space"),
    (5753, 'desc', "your opponent cannot player cannot activate", "your opponent cannot activate", "doubled words (typo)"),
    (6007, 'name', "Marshmallon glasses", "Marshmallon Glasses", "official name: capital letter"),
    (6302, 'desc', "from\nyour hand", "from your hand", "line break in the middle of the sentence"),
    (6639, 'desc', "When this card are successfully", "When this card is successfully", "agreement"),
    (6640, 'desc', "includes \"sphinx\" in", "includes \"Sphinx\" in", "capital letter (part of a name)"),
    (6684, 'desc', "Special Summon 1\"Option Token\"", "Special Summon 1 \"Option Token\"", "missing space"),
    (6229, 'desc', "field, tributing 1 monster", "field, Tributing 1 monster", "\"Tribute\" is capitalized"),
    (6229, 'desc', "that is level 5 or below", "that is Level 5 or below", "\"Level\" is capitalized"),
    # inconsistent capitalization (text by another translator: Monster/Hand/Field mid-sentence)
    (5358, 'desc', "Offer each of your Monsters", "Offer each of your monsters", "inconsistent capitalization"),
    (5367, 'desc', "While that Monster is", "While that monster is", "inconsistent capitalization"),
    (5451, 'desc', "all Monsters on", "all monsters on", "inconsistent capitalization"),
    (5493, 'desc', "your opponent's Monster attacks", "your opponent's monster attacks", "inconsistent capitalization"),
    (5493, 'desc', "Spell and Trap cards", "Spell and Trap Cards", "inconsistent capitalization"),
    (5497, 'desc', "Returns 1 Monster on", "Returns 1 monster on", "inconsistent capitalization"),
    (5497, 'desc', "one Level 4 Monster from", "one Level 4 monster from", "inconsistent capitalization"),
    (5497, 'desc', "to your Hand", "to your hand", "inconsistent capitalization"),
    (5557, 'desc', "when a Monster on", "when a monster on", "inconsistent capitalization"),
    (5557, 'desc', "one Level 4 Monster from", "one Level 4 monster from", "inconsistent capitalization"),
    (5561, 'desc', "Zombie-type card", "Zombie-Type card", "\"Type\" is capitalized"),
    (5561, 'desc', "adding it to your Hand", "adding it to your hand", "inconsistent capitalization"),
    (5743, 'desc', "face-up Monster on", "face-up monster on", "inconsistent capitalization"),
    (5743, 'desc', "when a Monster is destroyed", "when a monster is destroyed", "inconsistent capitalization"),
    (6003, 'desc', "Select 1 Monster in Defense", "Select 1 monster in Defense", "inconsistent capitalization"),
    (6231, 'desc', "each Monster on", "each monster on", "inconsistent capitalization"),
    (6288, 'desc', "selecting 1 Monster face-up", "selecting 1 monster face-up", "inconsistent capitalization"),
    (6288, 'desc', "the selected Monster's ATK", "the selected monster's ATK", "inconsistent capitalization"),
    (6288, 'desc', "every other Monster face-up", "every other monster face-up", "inconsistent capitalization"),
    (6288, 'desc', "other Monsters in face-up", "other monsters in face-up", "inconsistent capitalization"),
    (6291, 'desc', "Zombie-Type Monster with", "Zombie-Type monster with", "inconsistent capitalization"),
    (6291, 'desc', "The selected Monster will", "The selected monster will", "inconsistent capitalization"),
    (6450, 'desc', "all Monster cards in", "all Monster Cards in", "inconsistent capitalization"),
]
