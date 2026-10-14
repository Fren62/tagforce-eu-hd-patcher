# CHANGES OF THE MYSTIC TOMATO VERSION FOR ENGLISH

**Complete** document of everything the "Mystic Tomato Version" changes for english: (A) the **direct changes to the ISO**, (B) the **texture pack** (how it is made, what it contains, how it is composed), (C) the editorial choices, (D) what has been verified in game and what has not, (E) how to regenerate everything.

**This file is generated** by `tools/analysis/write_changes_document.py en` from the real data: byte-by-byte comparison between the original ISO `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` and the corrected ISO `..._definitiva.iso` (`document_changes.py`) and a scan of the pack (`document_pack.py`). The row-by-row lists are in `docs/changes_en/*.csv` (`;` separator, UTF-8 with BOM, line breaks as `⏎`): they are the **exact list** of every change. Regenerate everything after each modification.

For the general method and for the other languages: `docs/NEW_LANGUAGE_GUIDE.md`; technical details of the scripts: `docs/TUTORIAL.md`; decisions: `docs/EDITORIAL_CHOICES.md`; neutral/specific textures: `docs/TEXTURE_INVENTORY.md`.

## Index
- A. Changes to the ISO: A1 overview · A2 cards · A3 dialogues · A4 duel sentences · A5 interface strings · A6 Spell/Trap label · A7 touched files and technical details · A8 what cannot be changed
- B. Texture pack: B1 origin and structure · B2 card images · B3 HD interface (`ui_en`) · B4 number sheet (`card_icon03`) · B5 title plate · B6 textures.ini and composition · B7 installation
- C. Editorial choices · D. In-game verification · E. How to regenerate · F. Limits and open points

---

# A. CHANGES TO THE ISO

## A1. Overview

The original ISO is **never modified**. `tools/corrections/apply_to_iso.py ISO_ORIG ISO_OUT [languages]` creates a copy in which some `.ehp` archives are rewritten. If an archive grows (longer text) it is **put again at the end of the ISO** in a new sector and its entry in the ISO9660 directory is reassigned (`pycdlib`); for this reason the `_definitiva` ISO weighs ~909 MB (the original ~761 MB). **Always run it without a list of languages (or with all of them)**: with a single language it overwrites the others.

| What | Quantity (derived from the ISO comparison) | Where the data lives | CSV file |
|---|---|---|---|
| Cards with changed text (name and/or description) | 82 cards (83 fields) | `tools/data/card_corrections_en.json` from `tools/corrections/rules_en.py` | cards.csv |
| Story dialogue lines | 402 lines | `tools/data/dialogue_touchups_en.json` (+ base) | dialogues.csv |
| Duelist sentences in duels | 11 unique sentences (15 entries in all the archives) | `tools/data/duel_line_corrections_en.json` | duel_lines.csv |
| Interface strings (help, cards, records, tutorial, menus...) | 57 unique strings (215 entries, 51 archives) | `tools/corrections/string_rules_en.py` + `tools/data/ui_texts.json` | ui_strings.csv |
| Images replaced inside the ISO | 0 ([SPELL CARD/TRAP CARD] label of the large card) | `apply_to_iso.py` (copies the language's `card_spell_trap.gim`) | iso_images.csv |
| ISO files touched (`.ehp` archives) | 182 | - | touched_files.csv |
| Other technical differences (recomputed offsets) | 254 | - | other.csv |

## A2. Card texts

Archive: `PSP_GAME/USRDIR/duelsys/cardinfo_fra.ehp` (tables `CARD_Name_*`, `CARD_Desc_*`, `CARD_Indx_*`). **82 cards** have a modified name and/or description. Only **objective errors** are corrected (typos, accents, apostrophes, spaces, inconsistent capitalization, agreement, fixed plurals, leftovers from other languages); official names and the game's terminology are not touched.

How: every card was read (English: list of all the cards in comparisons/audit_en/cards_en.txt, objective errors only). Rules in `tools/corrections/rules_en.py`: **26 global rules** (regexes applied to the names and descriptions of all the cards) and **42 per-card corrections** (`PER_CARD`: id, field, old, new, reason; the old text must exist exactly). `generate_card_corrections.py en CARDINFO` (writes `card_corrections_{L}.json` starting from the original texts) produces the json; `apply_to_iso` writes it into the ISO; the HD images of the touched cards are regenerated (section B2).

### Global rules (all)
| pattern (regex) | replacement | reason |
|---|---|---|
| \bposible\b | possible | typo |
| \bfortell\b | foretell | typo |
| \bmistical\b | mystical | typo |
| \bmassibe\b | massive | typo |
| \benourmous\b | enormous | typo |
| \bTrbute\b | Tribute | typo |
| \btrbute\b | tribute | typo |
| (?i)\btrbute | tribute | typo (any form) |
| \bfliipped\b | flipped | typo |
| \bDefence\b | Defense | inconsistent spelling: the game uses "Defense" in all the other cards |
| \bDefensive Position\b | Defense Position | terminology: "Defense Position" in the rest of the game |
| 　(?=\n) |  | ideographic space (Japanese) at the end of the line |
| 　 |   | ideographic space (Japanese) instead of a normal space |
| \bside the field\b | side of the field | omitted preposition (Toon cards) |
| \byour must select\b | you must select | typo (your/you) |
| \bcan Inflict Direct Damage\b | can inflict Direct Damage | capital letter mid-sentence |
| \bBy tributing\b | By Tributing | "Tribute" is capitalized throughout the game |
| \bbattle damage\b | Battle Damage | "Battle Damage" is capitalized throughout the game |
| \bthis Turn\b | this turn | inconsistent capitalization |
| \bthe Turn\b | the turn | inconsistent capitalization |
| \bthis turns End Phase\b | this turn's End Phase | genitive apostrophe |
| \b1card\b | 1 card | missing space |
| \byour opponent's Field\b | your opponent's side of the field | "field" in lowercase and wording of the rest of the game |
| \byour Field\b | your side of the field | "field" in lowercase and wording of the rest of the game |
| \bthe Field\b(?! Spell) | the field | "field" in lowercase (the rest of the game) |
| \byour Hand\b | your hand | "hand" in lowercase (the rest of the game) |

### Per-card corrections (all)
| id | field | old | new | reason |
|---|---|---|---|---|
| 4564 | desc | he is a errand boy | he is an errand boy | article |
| 4483 | desc | with saw-like head | with a saw-like head | omitted article |
| 4601 | desc | into mirror world | into a mirror world | omitted article |
| 4372 | desc | a labyrinth no exit | a labyrinth with no exit | omitted word |
| 5266 | desc | The number of monster(s) are applied | The number of monster(s) is applied | agreement |
| 4232 | desc | this monsters grabs | this monster grabs | agreement (plural instead of singular) |
| 4492 | desc | a wealth of spell written | a wealth of spells written | missing plural |
| 4546 | desc | from your deck | from your Deck | capital letter: "Deck" throughout the game |
| 5062 | desc | "Worm Drake"+"Humanoid Slime" | "Worm Drake" + "Humanoid Slime" | spaces around the + as in the other fusions |
| 5096 | desc | your opponents side | your opponent's side | genitive apostrophe |
| 5184 | desc | "Don Zaloog"and | "Don Zaloog" and | missing space |
| 5753 | desc | your opponent cannot player cannot activate | your opponent cannot activate | doubled words (typo) |
| 6007 | name | Marshmallon glasses | Marshmallon Glasses | official name: capital letter |
| 6302 | desc | from⏎your hand | from your hand | line break in the middle of the sentence |
| 6639 | desc | When this card are successfully | When this card is successfully | agreement |
| 6640 | desc | includes "sphinx" in | includes "Sphinx" in | capital letter (part of a name) |
| 6684 | desc | Special Summon 1"Option Token" | Special Summon 1 "Option Token" | missing space |
| 6229 | desc | field, tributing 1 monster | field, Tributing 1 monster | "Tribute" is capitalized |
| 6229 | desc | that is level 5 or below | that is Level 5 or below | "Level" is capitalized |
| 5358 | desc | Offer each of your Monsters | Offer each of your monsters | inconsistent capitalization |
| 5367 | desc | While that Monster is | While that monster is | inconsistent capitalization |
| 5451 | desc | all Monsters on | all monsters on | inconsistent capitalization |
| 5493 | desc | your opponent's Monster attacks | your opponent's monster attacks | inconsistent capitalization |
| 5493 | desc | Spell and Trap cards | Spell and Trap Cards | inconsistent capitalization |
| 5497 | desc | Returns 1 Monster on | Returns 1 monster on | inconsistent capitalization |
| 5497 | desc | one Level 4 Monster from | one Level 4 monster from | inconsistent capitalization |
| 5497 | desc | to your Hand | to your hand | inconsistent capitalization |
| 5557 | desc | when a Monster on | when a monster on | inconsistent capitalization |
| 5557 | desc | one Level 4 Monster from | one Level 4 monster from | inconsistent capitalization |
| 5561 | desc | Zombie-type card | Zombie-Type card | "Type" is capitalized |
| 5561 | desc | adding it to your Hand | adding it to your hand | inconsistent capitalization |
| 5743 | desc | face-up Monster on | face-up monster on | inconsistent capitalization |
| 5743 | desc | when a Monster is destroyed | when a monster is destroyed | inconsistent capitalization |
| 6003 | desc | Select 1 Monster in Defense | Select 1 monster in Defense | inconsistent capitalization |
| 6231 | desc | each Monster on | each monster on | inconsistent capitalization |
| 6288 | desc | selecting 1 Monster face-up | selecting 1 monster face-up | inconsistent capitalization |
| 6288 | desc | the selected Monster's ATK | the selected monster's ATK | inconsistent capitalization |
| 6288 | desc | every other Monster face-up | every other monster face-up | inconsistent capitalization |
| 6288 | desc | other Monsters in face-up | other monsters in face-up | inconsistent capitalization |
| 6291 | desc | Zombie-Type Monster with | Zombie-Type monster with | inconsistent capitalization |
| 6291 | desc | The selected Monster will | The selected monster will | inconsistent capitalization |
| 6450 | desc | all Monster cards in | all Monster Cards in | inconsistent capitalization |

### Complete list of changed cards
**Complete original -> new comparison with the changed words highlighted: `docs/changes_en/cards_diff.md`** (all 83 entries). Raw data: `docs/changes_en/cards.csv`. First 40 rows:

| id | original name | field | original | new |
|---|---|---|---|---|
| 4008 | Mystical Elf | desc | A delicate elf that lacks offense, but has a terrific defense backed by mistical power. | A delicate elf that lacks offense, but has a terrific defense backed by mystical power. |
| 4232 | Skull Stalker | desc | Swift and deadly, this monsters grabs victims with its claws and attacks with a poison stinger. | Swift and deadly, this monster grabs victims with its claws and attacks with a poison stinger. |
| 4317 | Black Pendant | desc | Increase the ATK of a monster equipped with this card by 500 points.　When this card is sent from the field to the Graveyard, inflict 500 points of damage to your opponent's Life Points. | Increase the ATK of a monster equipped with this card by 500 points. When this card is sent from the field to the Graveyard, inflict 500 points of damage to your opponent's Life Points. |
| 4372 | Labyrinth Wall | desc | These walls form a labyrinth no exit for enemies. | These walls form a labyrinth with no exit for enemies. |
| 4483 | Alinsection | desc | A stag beetle with saw-like head and arms. | A stag beetle with a saw-like head and arms. |
| 4492 | Boo Koo | desc | A book-like wizard with a wealth of spell written inside. | A book-like wizard with a wealth of spells written inside. |
| 4546 | Skelengel | desc | FLIP: You can draw 1 card from your deck. | FLIP: You can draw 1 card from your Deck. |
| 4556 | Behegon | desc | With an enourmous maw and massive teeth, this monstrosity is one dangerous and strange serpent from the deep. | With an enormous maw and massive teeth, this monstrosity is one dangerous and strange serpent from the deep. |
| 4564 | Pot the Trick | desc | A not-so-powerful servant, he is a errand boy of a master sorcerer. | A not-so-powerful servant, he is an errand boy of a master sorcerer. |
| 4601 | Fiend Reflection #1 | desc | This monster can draw its enemies into mirror world that renders them helpless. | This monster can draw its enemies into a mirror world that renders them helpless. |
| 4639 | Winged Egg of New Life | desc | Legend has it that this creature can fortell the birth of children. | Legend has it that this creature can foretell the birth of children. |
| 4733 | Manga Ryu-Ran | desc | This card cannot be Normal Summoned or Set. This card can only be Special Summoned while "Toon World" is on your side the field. You can Special Summon this monster from your hand, but Tributes are required for monsters Level 5 or more. This card cannot attack in the turn that it is Summoned. Unless you pay 500 Life Points, this monster cannot attack. When "Toon World" on the field is destroyed, this card is also destroyed. If your opponent doesn't control a Toon Monster, this card can attack your opponent's Life Points directly. If a face-up Toon Monster is on your opponent's side of the field, your must select the Toon Monster as an attack target. | This card cannot be Normal Summoned or Set. This card can only be Special Summoned while "Toon World" is on your side of the field. You can Special Summon this monster from your hand, but Tributes are required for monsters Level 5 or more. This card cannot attack in the turn that it is Summoned. Unless you pay 500 Life Points, this monster cannot attack. When "Toon World" on the field is destroyed, this card is also destroyed. If your opponent doesn't control a Toon Monster, this card can attack your opponent's Life Points directly. If a face-up Toon Monster is on your opponent's side of the field, you must select the Toon Monster as an attack target. |
| 4734 | Toon Mermaid | desc | This card cannot be Normal Summoned or Set. This card can only be Special Summoned while "Toon World" is on your side the field. You can Special Summon this monster from your hand, but Tributes are required for monsters Level 5 or more. This card cannot attack in the turn that it is Summoned. Unless you pay 500 Life Points, this monster cannot attack. When "Toon World" on the field is destroyed, this card is also destroyed. If your opponent doesn't control a Toon Monster, this card can attack your opponent's Life Points directly. If a face-up Toon Monster is on your opponent's side of the field, your must select the Toon Monster as an attack target. | This card cannot be Normal Summoned or Set. This card can only be Special Summoned while "Toon World" is on your side of the field. You can Special Summon this monster from your hand, but Tributes are required for monsters Level 5 or more. This card cannot attack in the turn that it is Summoned. Unless you pay 500 Life Points, this monster cannot attack. When "Toon World" on the field is destroyed, this card is also destroyed. If your opponent doesn't control a Toon Monster, this card can attack your opponent's Life Points directly. If a face-up Toon Monster is on your opponent's side of the field, you must select the Toon Monster as an attack target. |
| 4735 | Toon Summoned Skull | desc | This card cannot be Normal Summoned or Set. This card can only be Special Summoned while "Toon World" is on your side the field. You can Special Summon this monster from your hand, but Tributes are required for monsters Level 5 or more. This card cannot attack in the turn that it is Summoned. Unless you pay 500 Life Points, this monster cannot attack. When "Toon World" on the field is destroyed, this card is also destroyed. If your opponent doesn't control a Toon Monster, this card can attack your opponent's Life Points directly. If a face-up Toon Monster is on your opponent's side of the field, your must select the Toon Monster as an attack target. | This card cannot be Normal Summoned or Set. This card can only be Special Summoned while "Toon World" is on your side of the field. You can Special Summon this monster from your hand, but Tributes are required for monsters Level 5 or more. This card cannot attack in the turn that it is Summoned. Unless you pay 500 Life Points, this monster cannot attack. When "Toon World" on the field is destroyed, this card is also destroyed. If your opponent doesn't control a Toon Monster, this card can attack your opponent's Life Points directly. If a face-up Toon Monster is on your opponent's side of the field, you must select the Toon Monster as an attack target. |
| 4737 | Relinquished | desc | Select 1 monster on your opponent's side of the field and equip it to this card (this effect can only be used once per turn and you can only equip 1 monster at a time to this card). The ATK and DEF of this card become the same amounts as the monster equipped to this card. If this card is destroyed as a result of battle, the equipped monster is destroyed instead, and any battle damage you received from the battle is also inflicted to your opponent's Life Points. | Select 1 monster on your opponent's side of the field and equip it to this card (this effect can only be used once per turn and you can only equip 1 monster at a time to this card). The ATK and DEF of this card become the same amounts as the monster equipped to this card. If this card is destroyed as a result of battle, the equipped monster is destroyed instead, and any Battle Damage you received from the battle is also inflicted to your opponent's Life Points. |
| 4743 | Hyozanryu | desc | A dragon created from a massibe diamond that sparkles with blinding light. | A dragon created from a massive diamond that sparkles with blinding light. |
| 4750 | Hannibal Necromancer | desc | When this card is Summoned successfully, place 1 Spell Counter on it (maximum of 1). Remove the Spell Counter to destroy one face-up Trap Card in the Field. | When this card is Summoned successfully, place 1 Spell Counter on it (maximum of 1). Remove the Spell Counter to destroy one face-up Trap Card in the field. |
| 4773 | Blue-Eyes Toon Dragon | desc | This card cannot be Normal Summoned or Set. This card can only be Special Summoned while "Toon World" is on your side the field. You can Special Summon this monster from your hand, but Tributes are required for monsters Level 5 or more. This card cannot attack in the turn that it is Summoned. Unless you pay 500 Life Points, this monster cannot attack. When "Toon World" on the field is destroyed, this card is also destroyed. If your opponent doesn't control a Toon Monster, this card can attack your opponent's Life Points directly. If a face-up Toon Monster is on your opponent's side of the field, your must select the Toon Monster as an attack target. | This card cannot be Normal Summoned or Set. This card can only be Special Summoned while "Toon World" is on your side of the field. You can Special Summon this monster from your hand, but Tributes are required for monsters Level 5 or more. This card cannot attack in the turn that it is Summoned. Unless you pay 500 Life Points, this monster cannot attack. When "Toon World" on the field is destroyed, this card is also destroyed. If your opponent doesn't control a Toon Monster, this card can attack your opponent's Life Points directly. If a face-up Toon Monster is on your opponent's side of the field, you must select the Toon Monster as an attack target. |
| 4805 | Multiply | desc | Tribute 1 face-up "Kuriboh". Special Summon as many "Kuriboh Tokens" (Fiend-Type/DARK/Level 1/ATK 300/DEF 200) as posible in Defense Position on your side of the field. The tokens cannot be used as a Tribute for a Tribute Summon. | Tribute 1 face-up "Kuriboh". Special Summon as many "Kuriboh Tokens" (Fiend-Type/DARK/Level 1/ATK 300/DEF 200) as possible in Defense Position on your side of the field. The tokens cannot be used as a Tribute for a Tribute Summon. |
| 4922 | Nimble Momonga | desc | When this card is sent to the Graveyard as a result of battle, increase your Life Points by 1000 points. You can also Special Summon up to 2 "Nimble Momonga" cards from your Deck to your side of the field in face-down Defence Position. Then shuffle your Deck. | When this card is sent to the Graveyard as a result of battle, increase your Life Points by 1000 points. You can also Special Summon up to 2 "Nimble Momonga" cards from your Deck to your side of the field in face-down Defense Position. Then shuffle your Deck. |
| 5003 | Alligator's Sword Dragon | desc | "Baby Dragon" + "Alligator's Sword"⏎You can Inflict Direct Damage to your opponent's Life Points with this card if the only Attributes of Monster Cards on your opponent's side of the field are EARTH, WATER, or FIRE. | "Baby Dragon" + "Alligator's Sword"⏎You can inflict Direct Damage to your opponent's Life Points with this card if the only Attributes of Monster Cards on your opponent's side of the field are EARTH, WATER, or FIRE. |
| 5024 | Fairy King Truesdale | desc | As long as this card remains in face-up Defence Position on the field, increase the ATK and DEF of all Plant-Type monsters on your side of the field by 500 points. | As long as this card remains in face-up Defense Position on the field, increase the ATK and DEF of all Plant-Type monsters on your side of the field by 500 points. |
| 5062 | Humanoid Worm Drake | desc | "Worm Drake"+"Humanoid Slime" | "Worm Drake" + "Humanoid Slime" |
| 5096 | Nuvia the Wicked | desc | If this monster is Normal Summoned, destroy this card. If your opponent controls any monster, decrease the ATK of this card by 200 points for each monster on your opponents side of the field. | If this monster is Normal Summoned, destroy this card. If your opponent controls any monster, decrease the ATK of this card by 200 points for each monster on your opponent's side of the field. |
| 5184 | Dark Scorpion - Tragedy of Love | desc | You can only activate this card when there are "Don Zaloog"and "Dark Scorpion - Meanae the Thorn" face-up on your side of the field. Send 1 "Dark Scorpion - Meanae the Thorn" from your side of your field to the Graveyard to destroy all of your opponent's monsters. | You can only activate this card when there are "Don Zaloog" and "Dark Scorpion - Meanae the Thorn" face-up on your side of the field. Send 1 "Dark Scorpion - Meanae the Thorn" from your side of your field to the Graveyard to destroy all of your opponent's monsters. |
| 5189 | Philosopher's Stone - Sabatier | desc | When a "Winged Kuriboh" on your side of the field is destroyed, you can add this card from your Deck to your hand. Pay half of your Life Points to add 1 card from your Deck or Graveyard to your hand. After this card is activated, it is placed into the Deck. Then shuffle the Deck. After you use this effect 3 times, this card takes on the following effect. Select 1 face-up monster on your side of the field and multiply its ATK by the number of monsters on your opponent's side of the field until this turns End Phase. | When a "Winged Kuriboh" on your side of the field is destroyed, you can add this card from your Deck to your hand. Pay half of your Life Points to add 1 card from your Deck or Graveyard to your hand. After this card is activated, it is placed into the Deck. Then shuffle the Deck. After you use this effect 3 times, this card takes on the following effect. Select 1 face-up monster on your side of the field and multiply its ATK by the number of monsters on your opponent's side of the field until this turn's End Phase. |
| 5230 | Dark Sage | desc | This card cannot be Normal Summoned or Set. This card can only be Special Summoned from your hand or your Deck by offering 1 "Dark Magician" on your side of the field as a Trbute when you succeed in the effect of "Time Wizard". At that time, select 1 Spell Card from your Deck, add it to your hand, and then shuffle your Deck. | This card cannot be Normal Summoned or Set. This card can only be Special Summoned from your hand or your Deck by offering 1 "Dark Magician" on your side of the field as a Tribute when you succeed in the effect of "Time Wizard". At that time, select 1 Spell Card from your Deck, add it to your hand, and then shuffle your Deck. |
| 5231 | Cathedral of Nobles | desc | The controller of this card can activate Traps on the turn they are set. Additionally, by sending this card and "Mystical Beast Serket" to the Graveyard when they are on your Field, you may select one Monster Card from your Hand, Deck, or Fusion Deck and Special Summon it. | The controller of this card can activate Traps on the turn they are set. Additionally, by sending this card and "Mystical Beast Serket" to the Graveyard when they are on your side of the field, you may select one Monster Card from your hand, Deck, or Fusion Deck and Special Summon it. |
| 5242 | Mystical Beast Serket | desc | This card is destroyed unless you have "Cathedral of Nobles" on your Field. Each time this card destroys a monster in battle, that monster is removed from play, and this card receives a 500 point ATK bonus. | This card is destroyed unless you have "Cathedral of Nobles" on your side of the field. Each time this card destroys a monster in battle, that monster is removed from play, and this card receives a 500 point ATK bonus. |
| 5266 | Deal of Phantom | desc | Select 1 monster face-up on the field. Increase the selected monster's ATK by 100 points for each monster in your Graveyard during the turn this card is activated. The number of monster(s) are applied when this card is activated. | Select 1 monster face-up on the field. Increase the selected monster's ATK by 100 points for each monster in your Graveyard during the turn this card is activated. The number of monster(s) is applied when this card is activated. |
| 5290 | Enchanted Arrow | desc | Destroys all face-up Spell Cards controlled by your opponent on the Field. For each Spell Card destroyed, your opponent receives 500 damage. | Destroys all face-up Spell Cards controlled by your opponent on the field. For each Spell Card destroyed, your opponent receives 500 damage. |
| 5358 | De-Spell Germ Weapon | desc | Offer each of your Monsters on the Field as a Tribute (except Tokens). For each card offered as a Tribute, your opponent selects a Spell Card from their Deck, sends it to the Graveyard, and afterwards shuffles their Deck. | Offer each of your monsters on the field as a Tribute (except Tokens). For each card offered as a Tribute, your opponent selects a Spell Card from their Deck, sends it to the Graveyard, and afterwards shuffles their Deck. |
| 5367 | Silent Fiend | desc | Special Summons one Normal Monster from your Graveyard in face-up Defense Position. While that Monster is on the Field, it cannot attack. | Special Summons one Normal Monster from your Graveyard in face-up Defense Position. While that monster is on the field, it cannot attack. |
| 5414 | Dark Dust Spirit | desc | This card cannot be Special Summoned. This card returns to the owner's hand during the End Phase of the turn that this card is Normal Summoned or fliipped face-up. If this card is Normal Summoned or flipped face-up, destroy all face-up monsters on the field except this card. | This card cannot be Special Summoned. This card returns to the owner's hand during the End Phase of the turn that this card is Normal Summoned or flipped face-up. If this card is Normal Summoned or flipped face-up, destroy all face-up monsters on the field except this card. |
| 5451 | Gilford the Lightning | desc | When this card is Tribute Summoned with 3 Tributes, all Monsters on your opponent's Field are destroyed. | When this card is Tribute Summoned with 3 Tributes, all monsters on your opponent's side of the field are destroyed. |
| 5483 | Gernia | desc | If this card is face-up on your Field and is destroyed by the effect of an opponent's card and sent to the Graveyard, it will be Special Summoned to your Field on your next Standby Phase. | If this card is face-up on your side of the field and is destroyed by the effect of an opponent's card and sent to the Graveyard, it will be Special Summoned to your side of the field on your next Standby Phase. |
| 5493 | Calamity of the Wicked | desc | Can be activated when your opponent's Monster attacks. Destroys all Spell and Trap cards on the Field. | Can be activated when your opponent's monster attacks. Destroys all Spell and Trap Cards on the field. |
| 5497 | Monster Relief | desc | Can be activated when your opponent attacks during their Battle Step. Returns 1 Monster on your Field to your Hand and Special Summons one Level 4 Monster from your Hand. | Can be activated when your opponent attacks during their Battle Step. Returns 1 monster on your side of the field to your hand and Special Summons one Level 4 monster from your hand. |
| 5501 | Master of Dragon Soldier | desc | "Black Luster Soldier" + "Blue-Eyes Ultimate Dragon"⏎This monster can only be Special Summoned with a Fusion Summon. For each Dragon monster on your Field, not including this one, this card receives a 500 point ATK bonus. | "Black Luster Soldier" + "Blue-Eyes Ultimate Dragon"⏎This monster can only be Special Summoned with a Fusion Summon. For each Dragon monster on your side of the field, not including this one, this card receives a 500 point ATK bonus. |
| 5502 | F.G.D. | desc | This card can only be Special Summoned with a Fusion Summon. This card is Fusion Summoned with 5 Dragon monsters. This card does not take battle damage from EARTH, WATER, FIRE, WIND, or DARK monsters. | This card can only be Special Summoned with a Fusion Summon. This card is Fusion Summoned with 5 Dragon monsters. This card does not take Battle Damage from EARTH, WATER, FIRE, WIND, or DARK monsters. |

(... 43 more rows in the CSV)

## A3. Story dialogues

Archives: `script/stNN_<scene>_f.ehp`, every scene is a pair of members `...If.bin` (offsets in UTF-16 characters) and `...Lf.bin` (UTF-16LE strings terminated by NUL, some gzip-compressed). **402 lines** changed (including those that **inherit** the correction because they have the same original text and the same Japanese as a corrected line).

Flow: line-by-line reading compared with English and Japanese -> touch-ups in `tools/data/dialogue_touchups_en.json` (`exact` and `parts`) -> `build_dialogues.py en` -> `dialogue_corrections_en.json` -> `apply_to_iso.py`. Automatic layout rules in `build_dialogues.py`: non-breaking space before `! ? : ;` also after `》` (rule `FR_PUNCT`), space after the placeholders, "Mode histoire" -> "Mode aventure". Box constraints: ~46 characters per line, max 3 lines (a placeholder counts ~6 characters): `apply_to_iso` reports the lines that might not fit.

### Re-reading touch-ups: `exact` (2) — whole original sentence -> new sentence
| original | new |
|---|---|
| Here, you can use this! | Here, use this maid outfit! |
|  He's Attie now! | He's Attie now! |

### Re-reading touch-ups: `parts` (79) — text replacements applied to every line (in order)
| old | new |
|---|---|
| PhD in deuling | PhD in dueling |
| My father owns a hot sauce⏎company. | My father owns a sake⏎brewery. |
| some hot sauce | some shochu |
| Wearing a bikini! | Wearing a maid outfit! |
| in a bikini! | in a maid outfit! |
| Do you⏎know much we spent?! | Do you⏎know how much we spent?! |
| It was a close,⏎but I can't say I'm happy. | It was close,⏎but I can't say I'm happy. |
| Boy, it does feels good⏎to win a duel! | Boy, it does feel good⏎to win a duel! |
| Show me what your made of! | Show me what you're made of! |
| Argh! You're skill is almost | Argh! Your skill is almost |
| I thought I had you⏎but there, but I lost. | I thought I had you⏎there, but I lost. |
| Tag duel are hard. | Tag duels are hard. |
| I'm important to get⏎experience in tag dueling. | It's important for me to get⏎experience in tag dueling. |
| Did you it easy on me? | Did you go easy on me? |
| it's⏎not like I asked you name! | it's⏎not like I asked your name! |
| You have class everyday⏎from Monday | You have class every day⏎from Monday |
| Even pre-duelist know the⏎answer to this!! | Even a pre-duelist knows the⏎answer to this!! |
| I-I rather have⏎volleyball! | I-I'd rather have⏎volleyball! |
| Okay, how this? | Okay, how's this? |
| You got a 80%. | You got an 80%. |
| Analog Stick . | Analog Stick. |
| I'd say your keeping your⏎eye out | I'd say you're keeping your⏎eye out |
| The foods in! ⏎Anyone | The food's in!⏎Anyone |
| He's said "I'm eating | He said "I'm eating |
| Now that you mention it...⏎⏎I heard | Now that you mention it...⏎I heard |
| The banana from for dinner! | The banana from dinner! |
| Koala's are lishus! | Koalas are lishus! |
| Judging by you expression | Judging by your expression |
| getting' kind of old. | gettin' kind of old. |
| I don't minding eating | I don't mind eating |
| I dreading going to the cafeteria | I was dreading going to the cafeteria |
| It's order made from France. | It's made to order from France. |
| foul stuff⏎everyday like you! | foul stuff⏎every day like you! |
| hard work everyday! | hard work every day! |
| the same thing⏎everyday is getting old. | the same thing⏎every day is getting old. |
| the same thing everyday. | the same thing every day. |
| You're Deck hasn't been calculated | Your Deck hasn't been calculated |
| How can I seal away it's⏎fusion ability? | How can I seal away its⏎fusion ability? |
| pop out at anytime. | pop out at any time. |
| 《PLAYER》、did you finish | 《PLAYER》, did you finish |
| I never thought⏎you to be so into food. | I never thought⏎you'd be so into food. |
| kind⏎of a mysterious in a way? | kind⏎of mysterious in a way? |
| ATK become 8000 | ATK becomes 8000 |
| keep and eye on my | keep an eye on my |
| takes⏎full advantages of your strengths | takes⏎full advantage of your strengths |
| I though about inviting | I thought about inviting |
| A duelist a skilled as you | A duelist as skilled as you |
| Why don't l give you a title of your own? | Why don't I give you a title of your own? |
| He just don't have any⏎interest in you... | He just doesn't have any⏎interest in you... |
| Good-for-nothing's are good for nothing. | Good-for-nothings are good for nothing. |
| wears a red uniform.. | wears a red uniform... |
| I'd be happy to be you're⏎partner! | I'd be happy to be your⏎partner! |
| I though I was doing good. | I thought I was doing good. |
| can duel like rest! | can duel like the rest! |
| not all your⏎cracked up to be! | not all you're⏎cracked up to be! |
| Wonder what your up to... | Wonder what you're up to... |
| I'll do by best! | I'll do my best! |
| I thought we went though⏎this. | I thought we went through⏎this. |
| I like already told you we'd⏎be partners ! | I, like, already told you we'd⏎be partners! |
| it's not like I asked you name! | it's not like I asked your name! |
| But I wonder the scents of a duel are? | But I wonder what the scents of a duel are? |
| number 1post | number 1 post |
| Ah duel? | A duel? |
| Heh heh heh heh.. | Heh heh heh heh... |
| The energy from the duel⏎have revived the Beasts! | The energy from the duel⏎has revived the Beasts! |
| I'm taking your badges! | I'm taking your medals! |
| Gimme your badges! | Gimme your medals! |
| If you don't you have any medals, | If you don't have any medals, |
| We'll let's do this some other time. | Well, let's do this some other time. |
| Let duel then. | Let's duel then. |
| Oh, do I have pay you? | Oh, do I have to pay you? |
| Look's like pay day came | Looks like pay day came |
| You really beat be there! | You really beat me there! |
| It's true that ＊⏎draws as well | It's true that 《PLAYER》⏎draws as well |
| ＊ has always⏎believed in you! | 《PLAYER》 has always⏎believed in you! |
| buying sandwiches⏎is like then, okay? | buying sandwiches⏎is like Zen, okay? |
| ９⏎１０⏎１１⏎１２ | 9⏎10⏎11⏎12 |
| Ｑ⏎Ｐ⏎Ａ⏎Ｃ | Q⏎P⏎A⏎C |
| ｖｓ |  vs  |

### Complete list of lines
**Complete original -> new comparison (with English and Japanese): `docs/changes_en/dialogues_diff.md`** (all 402 lines). Raw data: `docs/changes_en/dialogues.csv`. First 30:

| id | original | new | English |
|---|---|---|---|
| st01_t01/Iso001E#38 | You stole, lied and lost. ⏎You deserve to be demoted! | You stole, lied and lost.⏎You deserve to be demoted! | You stole, lied and lost. ⏎You deserve to be demoted! |
| st01_t01/Iso005E#34 | Scrubs don't have PhDs⏎in dueling!  Got that?! | Scrubs don't have PhDs⏎in dueling! Got that?! | Scrubs don't have PhDs⏎in dueling!  Got that?! |
| st01_t01/Iso005E#49 | Wow.  It's almost like⏎they really... like 《C005_3》. | Wow. It's almost like⏎they really... like 《C005_3》. | Wow.  It's almost like⏎they really... like 《C005_3》. |
| st01_t01/Iso005E#69 | Another chance?! Do you⏎know much we spent?! | Another chance?! Do you⏎know how much we spent?! | Another chance?! Do you⏎know much we spent?! |
| st01_t01/Iso005E#70 | You don't deserve to be a ⏎《C005_2》! | You don't deserve to be a⏎《C005_2》! | You don't deserve to be a ⏎《C005_2》! |
| st01_t01/Iso005E#115 | My new family is already ⏎dysfunctional! | My new family is already⏎dysfunctional! | My new family is already ⏎dysfunctional! |
| st01_t01/Iso007E#42 | Chill, 《C003_3》. ⏎It's just a costume! | Chill, 《C003_3》.⏎It's just a costume! | Chill, 《C003_3》. ⏎It's just a costume! |
| st01_t01/Iso007E#70 | It's 《PLAYER》ｖｓ《C026_1》! | It's 《PLAYER》 vs 《C026_1》! | It's 《PLAYER》ｖｓ《C026_1》! |
| st01_t01/Iso010E#34 | C'mon. ⏎This is a place to duel. | C'mon.⏎This is a place to duel. | C'mon. ⏎This is a place to duel. |
| st01_t01/Iso010E#66 | Huh? A present? I don't ⏎need that, but thanks! | Huh? A present? I don't⏎need that, but thanks! | Huh? A present? I don't ⏎need that, but thanks! |
| st01_t01/Iso010E#102 | I've lost... It was a close,⏎but I can't say I'm happy. | I've lost... It was close,⏎but I can't say I'm happy. | I've lost... It was a close,⏎but I can't say I'm happy. |
| st01_t01/Iso010E#103 | Boy, it does feels good⏎to win a duel! | Boy, it does feel good⏎to win a duel! | Boy, it does feels good⏎to win a duel! |
| st01_t01/Iso010E#172 | Wow, I won! This Deck ⏎isn't so bad after all! | Wow, I won! This Deck⏎isn't so bad after all! | Wow, I won! This Deck ⏎isn't so bad after all! |
| st01_t01/Iso010E#194 | I'm a man! I can't turn my ⏎back when faced with a duel! | I'm a man! I can't turn my⏎back when faced with a duel! | I'm a man! I can't turn my ⏎back when faced with a duel! |
| st01_t01/Iso010E#195 | I'm a man! I admit my ⏎mistakes and move on! | I'm a man! I admit my⏎mistakes and move on! | I'm a man! I admit my ⏎mistakes and move on! |
| st01_t01/Iso010E#196 | I'm a man! I'm a duelist! I ⏎can't let this go to my head! | I'm a man! I'm a duelist! I⏎can't let this go to my head! | I'm a man! I'm a duelist! I ⏎can't let this go to my head! |
| st01_t01/Iso010E#204 | Go ahead, 《PLAYER》.⏎Show me what your made of! | Go ahead, 《PLAYER》.⏎Show me what you're made of! | Go ahead, 《PLAYER》.⏎Show me what your made of! |
| st01_t01/Iso010E#205 | Argh! You're skill is almost⏎inhuman, 《PLAYER》! | Argh! Your skill is almost⏎inhuman, 《PLAYER》! | Argh! You're skill is almost⏎inhuman, 《PLAYER》! |
| st01_t01/Iso010E#216 | Bring it on! I'll give you a ⏎taste of some REAL power! | Bring it on! I'll give you a⏎taste of some REAL power! | Bring it on! I'll give you a ⏎taste of some REAL power! |
| st01_t01/Iso010E#231 | I don't stop until my ⏎opponent surrenders! | I don't stop until my⏎opponent surrenders! | I don't stop until my ⏎opponent surrenders! |
| st01_t01/Iso010E#240 | Perfect timing! I was just ⏎looking for someone to duel. | Perfect timing! I was just⏎looking for someone to duel. | Perfect timing! I was just ⏎looking for someone to duel. |
| st01_t01/Iso010E#241 | Dang! I thought I had you⏎but there, but I lost. | Dang! I thought I had you⏎there, but I lost. | Dang! I thought I had you⏎but there, but I lost. |
| st01_t01/Iso010E#261 | Well, I don't know... Aw, ⏎what the heck. Let's duel! | Well, I don't know... Aw,⏎what the heck. Let's duel! | Well, I don't know... Aw, ⏎what the heck. Let's duel! |
| st01_t01/Iso010E#263 | Yahoo! You played pretty ⏎good though! Nice duel! | Yahoo! You played pretty⏎good though! Nice duel! | Yahoo! You played pretty ⏎good though! Nice duel! |
| st01_t01/Iso010E#270 | Don't worry, I'll finish you ⏎off quick! Let's duel! | Don't worry, I'll finish you⏎off quick! Let's duel! | Don't worry, I'll finish you ⏎off quick! Let's duel! |
| st01_t01/Iso010E#283 | You're really good! I didn't ⏎do bad, but it wasn't enough. | You're really good! I didn't⏎do bad, but it wasn't enough. | You're really good! I didn't ⏎do bad, but it wasn't enough. |
| st01_t01/Iso010E#299 | I've blown you over. Use ⏎your passion and try again! | I've blown you over. Use⏎your passion and try again! | I've blown you over. Use ⏎your passion and try again! |
| st01_t01/Iso010E#302 | Tag duel are hard. I don't⏎know what to do to win. | Tag duels are hard. I don't⏎know what to do to win. | Tag duel are hard. I don't⏎know what to do to win. |
| st01_t01/Iso010E#312 | I'm important to get⏎experience in tag dueling. | It's important for me to get⏎experience in tag dueling. | I'm important to get⏎experience in tag dueling. |
| st01_t01/Iso010E#319 | That was a fun duel. I ⏎made some mistakes, though. | That was a fun duel. I⏎made some mistakes, though. | That was a fun duel. I ⏎made some mistakes, though. |

(... 372 more rows in the CSV)

## A4. Duelist sentences in duels

Tables `chr_wordstbl_f.bin` and `02chr_wordstbl_...` inside ~72 `duel/cutin_*.ehp` archives (and `zakov*`). The unique sentences are ~1,800: all re-read. **11 sentences changed** (15 entries). Data: `exact` (3) and `parts` (6) in `duel_line_corrections_en.json`. The `*-ptrs.txt` files of the character archives contain absolute offsets: if a table grows they must be recomputed (`remap_pointers`), otherwise the duel crashes.

Comparison with highlighted words: `docs/changes_en/duel_lines_diff.md`.

| original | new | entries | archive examples |
|---|---|---|---|
| Here comes a Equip Spell! | Here comes an Equip Spell! | 1 | cutin_aska01.ehp |
| I'm using a Equip Spell! | I'm using an Equip Spell! | 1 | cutin_aska01.ehp |
| See that!⏎And I wasn't even taking it serious!⏎⏎It's not gambling if there was never any risk! | See that!⏎And I wasn't even taking it seriously!⏎⏎It's not gambling if there was never any risk! | 1 | cutin_boy01.ehp |
| N...N...No way...⏎⏎I can't believe it!⏎You're just a a big meanie! | N...N...No way...⏎⏎I can't believe it!⏎You're just a big meanie! | 1 | cutin_junko01.ehp |
| The preparations for my resurrection is complete...⏎⏎All that's left is you. | The preparations for my resurrection are complete...⏎⏎All that's left is you. | 1 | cutin_psychoshocker01.ehp |
| I activate face-down card! | I activate a face-down card! | 1 | cutin_seiko01.ehp |
| Here's face-down card! | Here's a face-down card! | 1 | cutin_seiko01.ehp |
| I'm coming with face-down card! | I'm coming with a face-down card! | 1 | cutin_seiko01.ehp |
| I'm activating a Equip Spell! | I'm activating an Equip Spell! | 5 | zakov60.ehp, zakov61.ehp, zakov62.ehp, zakov63.ehp |
| What you're doing, do you! | What are you doing?! | 1 | zakov82.ehp |
| What's wrong!⏎⏎Are not you annoyed at losing!? | What's wrong!⏎⏎Aren't you annoyed at losing!? | 1 | zakov82.ehp |

## A5. Long and short interface strings

Tables `strTbl*`, `help_strtbl_*`, `ddstrtbl_*`, `field_strtbl*` (format `(n, 12, 12+4n)` + offsets + UTF-16) in 51 archives (the same table is copied into several archives, e.g. `field/always_*_fra.ehp` x6). **57 unique strings changed**. Rules: `tools/corrections/string_rules_en.py` — **53 `STRINGS` entries** (archive, member, 0-based index, [(old, new)], reason), **1 `GLOBALS`** (regex/callable, applied after the STRINGS) on **29 tables** (`TABLES`); plus 0 targeted corrections in `tools/data/ui_texts.json` (in-place writes, text shorter than or equal to the original).

### By member (unique strings changed)
| member | strings |
|---|---|
| strTbl_e.bin | 13 |
| help_strtbl_contents_duel_e.bin | 9 |
| 03_message_res.bin | 7 |
| field_strtbl_item.bin | 6 |
| help_strtbl_contents.bin | 4 |
| field_strtbl.bin | 4 |
| 01_message_res.bin | 3 |
| 04_message_res.bin | 3 |
| tushin_msg_e.bin | 2 |
| 02_message_res.bin | 2 |
| ddstrtbl_e.bin | 1 |
| option_msg_e.bin | 1 |
| strTbl.bin | 1 |
| event_name.bin | 1 |

### Global rules (all)
| pattern | replacement | reason |
|---|---|---|
| (\$C0)\$(?= ) | \1 | extra "$" after the $C0 color code (tutorial lessons) |

### STRINGS entries (all): where and why
| archive | member | index | changes | reason |
|---|---|---|---|---|
| database/charalist.ehp | strTbl_e.bin | 13 | 2 replacement(s) | article / extra "a" |
| database/charalist.ehp | strTbl_e.bin | 30 | 1 replacement(s) | wrong relative clause |
| database/charalist.ehp | strTbl_e.bin | 37 | 1 replacement(s) | every day (adverb) |
| database/charalist.ehp | strTbl_e.bin | 48 | 1 replacement(s) | extra pronoun |
| database/charalist.ehp | strTbl_e.bin | 52 | 1 replacement(s) | typo (Principle's) and character title as in the dialogues (Chancellor) |
| database/duelrecord.ehp | strTbl_e.bin | 42 | 1 replacement(s) | apostrophe |
| duel/result/result_e.ehp | strTbl.bin | 42 | 1 replacement(s) | apostrophe |
| database/limitlist.ehp | strTbl_e.bin | 6 | 1 replacement(s) | capital letter: Deck |
| database/limitlist.ehp | strTbl_e.bin | 7 | 1 replacement(s) | capital letter: Deck |
| database/limitlist.ehp | strTbl_e.bin | 8 | 1 replacement(s) | capital letter: Deck |
| deck/all_e.ehp | help_strtbl_contents.bin | 128 | 1 replacement(s) | verb form |
| deck/all_e.ehp | help_strtbl_contents.bin | 140 | 1 replacement(s) | swapped words |
| deck/all_e.ehp | help_strtbl_contents.bin | 162 | 1 replacement(s) | typo |
| deck/all_e.ehp | help_strtbl_contents.bin | 166 | 2 replacement(s) | grammar |
| deck/tutorial.ehp | strTbl_e.bin | 4 | 1 replacement(s) | any way |
| deck/tutorial.ehp | strTbl_e.bin | 81 | 1 replacement(s) | missing verb |
| deck/tutorial.ehp | strTbl_e.bin | 147 | 1 replacement(s) | agreement (subject: Using ... functions) |
| deck/tutorial.ehp | strTbl_e.bin | 203 | 1 replacement(s) | double comparative |
| duel/basic_*e.ehp | ddstrtbl_e.bin | 84 | 1 replacement(s) | typo |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 109 | 1 replacement(s) | missing noun |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 122 | 1 replacement(s) | verb form |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 134 | 1 replacement(s) | swapped words |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 154 | 1 replacement(s) | any time |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 160 | 1 replacement(s) | verb form |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 163 | 1 replacement(s) | missing subject |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 164 | 1 replacement(s) | missing subject |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 182 | 1 replacement(s) | typo |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 186 | 2 replacement(s) | grammar |
| field/always_*_eng.ehp | field_strtbl.bin | 14 | 1 replacement(s) | missing article |
| field/always_*_eng.ehp | field_strtbl.bin | 27 | 1 replacement(s) | full-width exclamation mark |
| field/always_*_eng.ehp | field_strtbl.bin | 28 | 1 replacement(s) | full-width exclamation mark |
| field/always_*_eng.ehp | field_strtbl.bin | 99 | 1 replacement(s) | space before the ! |
| field/always_*_eng.ehp | field_strtbl_item.bin | 4 | 1 replacement(s) | typo (in the dialogues: Bandana) |
| field/always_*_eng.ehp | field_strtbl_item.bin | 104 | 1 replacement(s) | typo |
| field/always_*_eng.ehp | field_strtbl_item.bin | 161 | 1 replacement(s) | comma instead of full stop |
| field/always_*_eng.ehp | field_strtbl_item.bin | 182 | 1 replacement(s) | double space, article |
| field/always_*_eng.ehp | field_strtbl_item.bin | 185 | 1 replacement(s) | missing full stop |
| field/always_*_eng.ehp | field_strtbl_item.bin | 198 | 1 replacement(s) | typo |
| title_menu/title_menu_?.ehp | tushin_msg_e.bin | 36 | 1 replacement(s) | missing space |
| title_menu/title_menu_?.ehp | tushin_msg_e.bin | 46 | 1 replacement(s) | missing space |
| field/always_*_eng.ehp | event_name.bin | 10 | 1 replacement(s) | extra preposition |
| duel/basic_*.ehp | option_msg_e.bin | 26 | 1 replacement(s) | its (possessive) |
| field/always_*_eng.ehp | option_msg_e.bin | 26 | 1 replacement(s) | its (possessive) |
| title_menu/title_menu_?.ehp | option_msg_e.bin | 26 | 1 replacement(s) | its (possessive) |
| tutorial/tutorial_e.ehp | 01_message_res.bin | 59 | 2 replacement(s) | misspelled name, double space |
| tutorial/tutorial_e.ehp | 01_message_res.bin | 109 | 1 replacement(s) | apostrophe |
| tutorial/tutorial_e.ehp | 01_message_res.bin | 138 | 1 replacement(s) | participle |
| tutorial/tutorial_e.ehp | 02_message_res.bin | 17 | 1 replacement(s) | verb form |
| tutorial/tutorial_e.ehp | 02_message_res.bin | 60 | 1 replacement(s) | verb form |
| tutorial/tutorial_e.ehp | 03_message_res.bin | 70 | 1 replacement(s) | wrong term (ritual -> Tribute) |
| tutorial/tutorial_e.ehp | 04_message_res.bin | 21 | 1 replacement(s) | plural apostrophe |
| tutorial/tutorial_e.ehp | 04_message_res.bin | 74 | 1 replacement(s) | plural apostrophe |
| tutorial/tutorial_e.ehp | 04_message_res.bin | 154 | 1 replacement(s) | missing space |

### Targeted corrections `ui_texts.json`
| file | member | index | old | new | reason |
|---|---|---|---|---|---|

### Complete list
**Complete comparison with highlighted words: `docs/changes_en/ui_strings_diff.md`.** Raw data: `docs/changes_en/ui_strings.csv`. First 40:

| member | index | original | new |
|---|---|---|---|
| strTbl_e.bin | 13 | Syrus admires Jaden a great deal, and looks up to him as an older brother. But he also has a real older brother, so he tends to have different nicknames for each of them.⏎⏎He has respect for, but also feels a little inferior around strong, dependable people. Someday he wants to be as great as Jaden.⏎⏎Syrus doesn't have much confidence in his own abilities, which seems to be cause of his constant negative outlook on life.⏎But on the other hand, he can often be very critical of other people.⏎⏎He used to have a negative, half-hearted approach when playing in duels, always telling himself that he can't win. But since he met Jaden, his negative outlook is gradually changing into a more positive one.⏎⏎Syrus loves all kinds of vehicles, and uses a Deck full of "Vehicroid" cards - "Vehicroid" being a type of vehicle.⏎Although they seem a cute and harmless, they are actually quite strong.⏎⏎He can easily fall head over heels for a pretty girl, but none of his crushes have ever materialized into an actual relationship at this point in his life.⏎⏎Syrus's favorite food is served once a month in the Slifer Red cafeteria.⏎But he can't handle spicy food very well. | Syrus admires Jaden a great deal, and looks up to him as an older brother. But he also has a real older brother, so he tends to have different nicknames for each of them.⏎⏎He has respect for, but also feels a little inferior around strong, dependable people. Someday he wants to be as great as Jaden.⏎⏎Syrus doesn't have much confidence in his own abilities, which seems to be the cause of his constant negative outlook on life.⏎But on the other hand, he can often be very critical of other people.⏎⏎He used to have a negative, half-hearted approach when playing in duels, always telling himself that he can't win. But since he met Jaden, his negative outlook is gradually changing into a more positive one.⏎⏎Syrus loves all kinds of vehicles, and uses a Deck full of "Vehicroid" cards - "Vehicroid" being a type of vehicle.⏎Although they seem cute and harmless, they are actually quite strong.⏎⏎He can easily fall head over heels for a pretty girl, but none of his crushes have ever materialized into an actual relationship at this point in his life.⏎⏎Syrus's favorite food is served once a month in the Slifer Red cafeteria.⏎But he can't handle spicy food very well. |
| strTbl_e.bin | 30 | Kagemaru is the chairman of Duel Academy.⏎⏎He founded the Academy in order to round up talented duelists - ultimately hoping to use their power to resurrect the Sacred Beast Cards, which had been sealed long ago.⏎Bringing the Sacred Beasts back to life will trigger a great deal of energy in which he can use to attain eternal youth. | Kagemaru is the chairman of Duel Academy.⏎⏎He founded the Academy in order to round up talented duelists - ultimately hoping to use their power to resurrect the Sacred Beast Cards, which had been sealed long ago.⏎Bringing the Sacred Beasts back to life will trigger a great deal of energy which he can use to attain eternal youth. |
| strTbl_e.bin | 37 | A girl who chases after Zane.⏎She took the Academy's entrance examination just so she could enroll to see him everyday.⏎Her personality could be described as obsessive. She's definitely the jealous type.⏎So jealous in fact that she'll go overboard and confuse those around her.⏎⏎Her Deck reflects the feelings of a maiden in love. She hopes to someday convey her feelings to that special someone through a duel.⏎Her main card is called "Maiden in Love". It's actually a monster that takes the opponent captive.⏎⏎And since she's only in the 5th grade, she can't get into the high school level Duel Academy. | A girl who chases after Zane.⏎She took the Academy's entrance examination just so she could enroll to see him every day.⏎Her personality could be described as obsessive. She's definitely the jealous type.⏎So jealous in fact that she'll go overboard and confuse those around her.⏎⏎Her Deck reflects the feelings of a maiden in love. She hopes to someday convey her feelings to that special someone through a duel.⏎Her main card is called "Maiden in Love". It's actually a monster that takes the opponent captive.⏎⏎And since she's only in the 5th grade, she can't get into the high school level Duel Academy. |
| strTbl_e.bin | 48 | Fonda is supervisor of the female Obelisk Blue dorm.⏎She is also the gym instructor and school nurse at the Duel Academy.⏎A lot of male students have faked injuries just to meet her.⏎⏎Fonda is actually a pretty good duelist and enjoys an occasional duel on her spare time.⏎She loves anything cute, and this is reflected in her Deck which it is packed with cute cards. | Fonda is supervisor of the female Obelisk Blue dorm.⏎She is also the gym instructor and school nurse at the Duel Academy.⏎A lot of male students have faked injuries just to meet her.⏎⏎Fonda is actually a pretty good duelist and enjoys an occasional duel on her spare time.⏎She loves anything cute, and this is reflected in her Deck, which is packed with cute cards. |
| strTbl_e.bin | 52 | Principle's Sheppard's Profile | Chancellor Sheppard's Profile |
| strTbl_e.bin | 42 | Number of opponents cards removed from Deck | Number of opponent's cards removed from Deck |
| strTbl_e.bin | 6 | You have too many copies of "$CA%s$C0" in your deck. ⏎Edit Deck? | You have too many copies of "$CA%s$C0" in your Deck. ⏎Edit Deck? |
| strTbl_e.bin | 7 | You have too many copies of "$CB%s$C0" in your deck. ⏎Edit Deck? | You have too many copies of "$CB%s$C0" in your Deck. ⏎Edit Deck? |
| strTbl_e.bin | 8 | You have too many copies of "$CC%s$C0" in your deck. ⏎Edit Deck? | You have too many copies of "$CC%s$C0" in your Deck. ⏎Edit Deck? |
| help_strtbl_contents.bin | 128 | A Monster Card⏎can be placed on the field by "Summon" it. Once placed on the field it can be used in battle during the Battle Phase, or its special effects can be activated.⏎Battles held during a Duel are generally Monster Battles using this type of card.⏎A huge amount of Monster Cards exist with a wide variety of Types among them.⏎A Monster Card with high ATK and DEF scores can be very effective in simple battles, but some Monster Cards with low ATK and DEF scores may have unique or powerful effects. Using those effects under the right circumstances is ultimately the key to victory. | A Monster Card⏎can be placed on the field by "Summoning" it. Once placed on the field it can be used in battle during the Battle Phase, or its special effects can be activated.⏎Battles held during a Duel are generally Monster Battles using this type of card.⏎A huge amount of Monster Cards exist with a wide variety of Types among them.⏎A Monster Card with high ATK and DEF scores can be very effective in simple battles, but some Monster Cards with low ATK and DEF scores may have unique or powerful effects. Using those effects under the right circumstances is ultimately the key to victory. |
| help_strtbl_contents.bin | 140 | This is a unique effect.⏎Although effects have a designated timing for activation, this effect can be also be activated during your opponent's turn.⏎⏎[Card Text Example]⏎This effect can also be activated during your opponent's turn. | This is a unique effect.⏎Although effects have a designated timing for activation, this effect can also be activated during your opponent's turn.⏎⏎[Card Text Example]⏎This effect can also be activated during your opponent's turn. |
| help_strtbl_contents.bin | 162 | - The first player cannot attack on the first turn.⏎   (An attack can only be done starting with the second player on the first turn.)⏎⏎- During your own turn, you can use any cards which your teammate has placed on the field.⏎⏎- You can check any card which has been placed faced-down on the field by your teammate.⏎⏎- You can use any Monster Card as a Tribute, Fusion Material, or Ritual Material which your teammate has Summoned to the field.⏎⏎- You can equip an Equip Spell Card to any Monster Card your teammate has Summoned to the field.⏎⏎- During your opponent's turn, the rights of activating effects, such as Quick-Play Spell Cards or Trap Cards go to the player whose turn had just ended.⏎⏎Assuming the Duel is being played according to the following order,⏎⏎Team 1: Player A⏎Team 2: Player C⏎Team 1: Player B⏎Team 2: Player D⏎⏎if Player C of Team 2 has attacked during his/her Battle Phase, the player who had a turn just before that, which is Player A of Team 1, will be able to choose whether or not he/she wants to activate a Quick-Play Spell or Trap in response to the attack. | - The first player cannot attack on the first turn.⏎   (An attack can only be done starting with the second player on the first turn.)⏎⏎- During your own turn, you can use any cards which your teammate has placed on the field.⏎⏎- You can check any card which has been placed face-down on the field by your teammate.⏎⏎- You can use any Monster Card as a Tribute, Fusion Material, or Ritual Material which your teammate has Summoned to the field.⏎⏎- You can equip an Equip Spell Card to any Monster Card your teammate has Summoned to the field.⏎⏎- During your opponent's turn, the rights of activating effects, such as Quick-Play Spell Cards or Trap Cards go to the player whose turn had just ended.⏎⏎Assuming the Duel is being played according to the following order,⏎⏎Team 1: Player A⏎Team 2: Player C⏎Team 1: Player B⏎Team 2: Player D⏎⏎if Player C of Team 2 has attacked during his/her Battle Phase, the player who had a turn just before that, which is Player A of Team 1, will be able to choose whether or not he/she wants to activate a Quick-Play Spell or Trap in response to the attack. |
| help_strtbl_contents.bin | 166 | Pick Up Card basically means to turn a face-down card to face-up position and viewing its content. Flip Effects are not activated when Pick up a card. Generally, after viewing the card's content, it will be returned to its original face-down position on the field. | Pick Up Card basically means to turn a face-down card to face-up position and view its content. Flip Effects are not activated when you pick up a card. Generally, after viewing the card's content, it will be returned to its original face-down position on the field. |
| strTbl_e.bin | 4 | You are able to edit your "Deck" anyway you like. | You are able to edit your "Deck" any way you like. |
| strTbl_e.bin | 81 | You can put "Fusion Monster" cards in your "Fusion Deck" to use during a duel.⏎But you'll have to follow these rules:⏎⏎* No more than 30 cards can be in it.⏎* No more than 3 cards of the same name be in it.⏎* Deck rules for Forbidden, Limited, and ⏎Semi-Limited cards also apply here.⏎* Any Type of card other than "Fusion Monster" cannot be added. | You can put "Fusion Monster" cards in your "Fusion Deck" to use during a duel.⏎But you'll have to follow these rules:⏎⏎* No more than 30 cards can be in it.⏎* No more than 3 cards of the same name can be in it.⏎* Deck rules for Forbidden, Limited, and ⏎Semi-Limited cards also apply here.⏎* Any Type of card other than "Fusion Monster" cannot be added. |
| strTbl_e.bin | 147 | Using the "Sort" and "Narrow Search" functions allow you to quickly find the cards you're looking for. | Using the "Sort" and "Narrow Search" functions allows you to quickly find the cards you're looking for. |
| strTbl_e.bin | 203 | Shortcuts allow you to perform complicated actions without even opening a menu.⏎This means you'll be able to edit your Deck more faster and easier. | Shortcuts allow you to perform complicated actions without even opening a menu.⏎This means you'll be able to edit your Deck faster and easier. |
| ddstrtbl_e.bin | 84 | Your surrendered due to the lock effect of "Yata-Garasu". | You surrendered due to the lock effect of "Yata-Garasu". |
| help_strtbl_contents_duel_e.bin | 109 | Battling with an opponent for victory is called a "Duel".⏎"Single" are played only 1 time, whereas a "Match" consists of 3 Duels.⏎⏎"Single" is only played once to determine victory, while in a "Match", the first to win 2 Duels is the winner of the entire Match. | Battling with an opponent for victory is called a "Duel".⏎"Single" Duels are played only 1 time, whereas a "Match" consists of 3 Duels.⏎⏎"Single" is only played once to determine victory, while in a "Match", the first to win 2 Duels is the winner of the entire Match. |
| help_strtbl_contents_duel_e.bin | 122 | A Monster Card⏎can be placed on the field by "Summon" it. Once placed on the field it can be used in battle during the Battle Phase, or its special effects can be activated.⏎Battles held during a Duel are generally Monster Battles using this type of card.⏎A huge amount of Monster Cards exist with a wide variety of Types among them.⏎A Monster Card with high ATK and DEF scores can be very effective in simple battles, but some Monster Cards with low ATK and DEF scores may have unique or powerful effects. Using those effects under the right circumstances is ultimately the key to victory. | A Monster Card⏎can be placed on the field by "Summoning" it. Once placed on the field it can be used in battle during the Battle Phase, or its special effects can be activated.⏎Battles held during a Duel are generally Monster Battles using this type of card.⏎A huge amount of Monster Cards exist with a wide variety of Types among them.⏎A Monster Card with high ATK and DEF scores can be very effective in simple battles, but some Monster Cards with low ATK and DEF scores may have unique or powerful effects. Using those effects under the right circumstances is ultimately the key to victory. |
| help_strtbl_contents_duel_e.bin | 134 | This is a unique effect.⏎Although effects have a designated timing for activation, this effect can be also be activated during your opponent's turn.⏎⏎[Card Text Example]⏎This effect can also be activated during your opponent's turn. | This is a unique effect.⏎Although effects have a designated timing for activation, this effect can also be activated during your opponent's turn.⏎⏎[Card Text Example]⏎This effect can also be activated during your opponent's turn. |
| help_strtbl_contents_duel_e.bin | 154 | The first phase of a turn is the Draw Phase.⏎The turn player must draw 1 card from the top of his or her Deck.⏎(If there are no cards left to draw from the Deck at this point, the player will lose the Duel.)⏎After drawing a card, the turn player will automatically move on to the Standby Phase. However, Trap Cards or Quick-Play Spell Cards can be activated at anytime between the Draw Phase and Standby Phase. | The first phase of a turn is the Draw Phase.⏎The turn player must draw 1 card from the top of his or her Deck.⏎(If there are no cards left to draw from the Deck at this point, the player will lose the Duel.)⏎After drawing a card, the turn player will automatically move on to the Standby Phase. However, Trap Cards or Quick-Play Spell Cards can be activated at any time between the Draw Phase and Standby Phase. |
| help_strtbl_contents_duel_e.bin | 160 | Similar to a Summon, placing a Monster Card on the field in face-down Defense Position is called a "Set".⏎When Setting a high-level Monster Card (Level 5 or higher), you'll need to offer a Tribute just as you do when Summon.⏎⏎As with a "Normal Summon", this type of Summon can only be done once per turn. | Similar to a Summon, placing a Monster Card on the field in face-down Defense Position is called a "Set".⏎When Setting a high-level Monster Card (Level 5 or higher), you'll need to offer a Tribute just as you do when Summoning.⏎⏎As with a "Normal Summon", this type of Summon can only be done once per turn. |
| help_strtbl_contents_duel_e.bin | 163 | The Summon of a Fusion Monster is called a "Fusion Summon".⏎In order to "Fusion Summon" a card, you'll need the Fusion Material (Monster Card(s)) specified in the card text of the card you wish to Summon, along with the "Polymerization" Spell Card. Both of these need to be either in your Hand or on your side of the Field.⏎(The Fusion Monster itself will be Summoned from the Fusion Deck, so this method cannot be used to Summon any cards from the Graveyard or anywhere other than the Fusion Deck.)⏎When successfully "Fusion Summon" a Monster Card, the Fusion Material used, along with the "Polymerization" Spell Card, will be sent to the Graveyard.⏎⏎This type of Summon is treated the same as a "Special Summon". | The Summon of a Fusion Monster is called a "Fusion Summon".⏎In order to "Fusion Summon" a card, you'll need the Fusion Material (Monster Card(s)) specified in the card text of the card you wish to Summon, along with the "Polymerization" Spell Card. Both of these need to be either in your Hand or on your side of the Field.⏎(The Fusion Monster itself will be Summoned from the Fusion Deck, so this method cannot be used to Summon any cards from the Graveyard or anywhere other than the Fusion Deck.)⏎When you successfully "Fusion Summon" a Monster Card, the Fusion Material used, along with the "Polymerization" Spell Card, will be sent to the Graveyard.⏎⏎This type of Summon is treated the same as a "Special Summon". |
| help_strtbl_contents_duel_e.bin | 164 | The Summon of a Ritual Monster Card is called a "Ritual Summon".⏎In order to perform a Ritual Summon, you must have the Ritual Monster Card you want to Ritual Summon, the Ritual Spell Card specific to that Ritual Monster, and Monster Card(s) to Tribute which are equal to or exceeding the Ritual Monster Card's Level. All of these cards must be in your hand or on your side of the field.⏎When successfully "Ritual Summon" a Monster Card, the Tributed monster(s) and the Ritual Spell Card are sent to the Graveyard.⏎If 1 Monster Card is sufficient for a Tribute, you are unable to choose any more than 1 card to offer.⏎⏎This type of Summon is treated the same as a "Special Summon". | The Summon of a Ritual Monster Card is called a "Ritual Summon".⏎In order to perform a Ritual Summon, you must have the Ritual Monster Card you want to Ritual Summon, the Ritual Spell Card specific to that Ritual Monster, and Monster Card(s) to Tribute which are equal to or exceeding the Ritual Monster Card's Level. All of these cards must be in your hand or on your side of the field.⏎When you successfully "Ritual Summon" a Monster Card, the Tributed monster(s) and the Ritual Spell Card are sent to the Graveyard.⏎If 1 Monster Card is sufficient for a Tribute, you are unable to choose any more than 1 card to offer.⏎⏎This type of Summon is treated the same as a "Special Summon". |
| help_strtbl_contents_duel_e.bin | 182 | - The first player cannot attack on the first turn.⏎   (An attack can only be done starting with the second player on the first turn.)⏎⏎- During your own turn, you can use any cards which your teammate has placed on the field.⏎⏎- You can check any card which has been placed faced-down on the field by your teammate.⏎⏎- You can use any Monster Card as a Tribute, Fusion Material, or Ritual Material which your teammate has Summoned to the field.⏎⏎- You can equip an Equip Spell Card to any Monster Card your teammate has Summoned to the field.⏎⏎- During your opponent's turn, the rights of activating effects, such as Quick-Play Spell Cards or Trap Cards go to the player whose turn had just ended.⏎⏎Assuming the Duel is being played according to the following order,⏎⏎Team 1: Player A⏎Team 2: Player C⏎Team 1: Player B⏎Team 2: Player D⏎⏎if Player C of Team 2 has attacked during his/her Battle Phase, the player who had a turn just before that, which is Player A of Team 1, will be able to choose whether or not he/she wants to activate a Quick-Play Spell or Trap in response to the attack. | - The first player cannot attack on the first turn.⏎   (An attack can only be done starting with the second player on the first turn.)⏎⏎- During your own turn, you can use any cards which your teammate has placed on the field.⏎⏎- You can check any card which has been placed face-down on the field by your teammate.⏎⏎- You can use any Monster Card as a Tribute, Fusion Material, or Ritual Material which your teammate has Summoned to the field.⏎⏎- You can equip an Equip Spell Card to any Monster Card your teammate has Summoned to the field.⏎⏎- During your opponent's turn, the rights of activating effects, such as Quick-Play Spell Cards or Trap Cards go to the player whose turn had just ended.⏎⏎Assuming the Duel is being played according to the following order,⏎⏎Team 1: Player A⏎Team 2: Player C⏎Team 1: Player B⏎Team 2: Player D⏎⏎if Player C of Team 2 has attacked during his/her Battle Phase, the player who had a turn just before that, which is Player A of Team 1, will be able to choose whether or not he/she wants to activate a Quick-Play Spell or Trap in response to the attack. |
| help_strtbl_contents_duel_e.bin | 186 | Pick Up Card basically means to turn a face-down card to face-up position and viewing its content. Flip Effects are not activated when Pick up a card. Generally, after viewing the card's content, it will be returned to its original face-down position on the field. | Pick Up Card basically means to turn a face-down card to face-up position and view its content. Flip Effects are not activated when you pick up a card. Generally, after viewing the card's content, it will be returned to its original face-down position on the field. |
| option_msg_e.bin | 26 | Pause the game when an effect is activated to confirm it's effects. | Pause the game when an effect is activated to confirm its effects. |
| strTbl.bin | 42 | Number of opponents cards removed from Deck | Number of opponent's cards removed from Deck |
| event_name.bin | 10 | The day before of "Tag Force" meet. | The day before the "Tag Force" meet. |
| field_strtbl.bin | 14 | There's no one to request duel against! | There's no one to request a duel against! |
| field_strtbl.bin | 27 | You obtained $C7%s$C0！ | You obtained $C7%s$C0! |
| field_strtbl.bin | 28 | Acquired $C6%s$C0 card！ | Acquired $C6%s$C0 card! |
| field_strtbl.bin | 99 | You acquired %s ! | You acquired %s! |
| field_strtbl_item.bin | 4 | Bandanna | Bandana |
| field_strtbl_item.bin | 104 | This orange bandanna smells nice.⏎It must belong to a girl. | This orange bandana smells nice.⏎It must belong to a girl. |
| field_strtbl_item.bin | 161 | Sandwich filled with sweet, roasted chestnuts, ⏎Its sweet flavor makes it especially popular among the female students. | Sandwich filled with sweet, roasted chestnuts.⏎Its sweet flavor makes it especially popular among the female students. |
| field_strtbl_item.bin | 182 | Sandwich filled with  an uniquely-dried fish. Tastes great, but smells awful. | Sandwich filled with a uniquely-dried fish. Tastes great, but smells awful. |
| field_strtbl_item.bin | 185 | Delicious sandwich filled with lobster chunks⏎One sandwich will fill you up. | Delicious sandwich filled with lobster chunks.⏎One sandwich will fill you up. |
| field_strtbl_item.bin | 198 | A sandwich, but there is no telling what my be inside. | A sandwich, but there is no telling what may be inside. |

(... 17 more rows in the CSV)

## A6. [SPELL CARD] / [TRAP CARD] label of the large card in the duel

In all the `duel/basic_<region><language>.ehp` the label was in English (hash `c2268340`): `apply_to_iso.py` replaces it with `card_spell_trap.gim` of `field/always_<language>_<language>.ehp` (hash `9622cd75`).

| archive | member | original hash | new hash |
|---|---|---|---|

## A7. ISO files touched and technical details

182 `.ehp` archives differ from the original (all languages together, because the ISO is a single one; list in `docs/changes_en/touched_files.csv`). The other files (video, audio, `EBOOT.BIN` executable, `PARAM.SFO`) are identical. Non-textual technical differences: `*-ptrs.txt` (absolute member offsets, recomputed when a table changes length), new position of the archives at the end of the ISO.

## A8. What can NOT be changed (game limits)

- The **speaker name** in the dialogue box (e.g. "Preside Sheppard"/"Cancelliere" in Italian, "Doyen Sheppard" in French, "Rector Sheppard" in Spanish) lives in the encrypted EBOOT: it cannot be modified.
- Texts drawn by the game with its own font (dialogues, names, descriptions in the deck, drop-down menus, system keyboard, language selection screen) cannot be replaced by the texture pack: they can only be changed in the ISO.
- The 438 map/background textures are not replaced (the game changes their palette): a limit of MikeyMK's pack, not of our work.

---

# B. TEXTURE PACK

## B1. Origin and structure

Base: **Yu-Gi-Oh! GX Tag Force 1 HD Remastered** by **MikeyMK** (US pack `ULUS10136`) and HD cards by **chrisfand**, adapted to the European ISO `ULES00600`. The project does not redistribute the third-party pack: the patcher gets it from the user. Our work: (1) remap the US pack's **hashes** to the EU ones (`tools/gen_ini.py`), (2) redo the cards and interface lettering in the language, (3) correct the texts, (4) `upscale_extra` for the textures that are not covered.

PPSSPP recognizes a texture by the **hash of its pixels** (xxhash of the data, `gim.data_hash`); every line of `textures.ini` is `0000000000000000<hash8> = path/png`. The PNGs are **4x** the original and redraw exactly the same area. Textures that are identical between languages have the same hash: the replacement holds for all of them (see `docs/TEXTURE_INVENTORY.md`).

### Real structure (from `docs/changes_en/pack_structure.csv`)
| root | folder | files | MB | content |
|---|---|---|---|---|
| ULES00600 (pack di base) | LEGGIMI.txt | 1 | 0.0 |  |
| ULES00600 (pack di base) | _SCEGLI LO STILE DELLE CARTE/ | 3 | 7.8 | mikeymk, official_english, official_japanese |
| ULES00600 (pack di base) | cards/ | 11373 | 2161.9 | frame, large, large_it, small, small_it, tinyEN, tinyJP, tinyMikeyMK, tiny_it |
| ULES00600 (pack di base) | characters/ | 1468 | 134.3 | 3d, combinations, portraits, sprites |
| ULES00600 (pack di base) | events/ | 17 | 40.5 | academy_festival.png, alexis_rhodes.png, atticus_rhodes_beach.png, bastion_decks.png, bastion_misawa.png, chazz_dueldisk.png, chazz_on_tv.png, chazz_princeton.png, chumley_huffington.png, duel_tower.png ... |
| ULES00600 (pack di base) | intro/ | 60 | 10.9 | konami_logo.png, logo_tagforce, logo_yugioh, new_save, ojama_yellow.png, title_screen, winged_kuriboh.png |
| ULES00600 (pack di base) | map/ | 15 | 21.1 | backgrounds |
| ULES00600 (pack di base) | shop/ | 153 | 69.5 | blue_eyes_jp.png, card_pack_results_ui.png, dorothy, packs, purchase_text_box.png, room_textures, sadie, sandwiches.png, store_purchasing_background.png, store_purchasing_ui.png |
| ULES00600 (pack di base) | textures.ini | 1 | 2.59 |  |
| ULES00600 (pack di base) | ui/ | 331 | 22.3 | cardalbum, deckedit, duels, horizontal_bar_black.png, horizontal_bar_red.png, horizontal_bar_silver.png, horizontal_bar_yellow.png, janken.png, limited.png, loading ... |
| ULES00600 (pack di base) | ui_it/ | 113 | 9.8 | icon_sheets, icon_sheets.ini, result_letters, result_letters.ini, menu_lists, menu_lists.ini, deck_screens, deck_screens.ini, recipe_screens, recipe_screens.ini ... |
| ULES00600 (pack di base) | upscale_extra/ | 1192 | 55.8 | 00085186.png, 00162f3c.png, 003fd929.png, 0047e8d4.png, 00b99210.png, 00c5c424.png, 01673953.png, 01692dff.png, 01f7d8fe.png, 01faa502.png ... |
| moduli/en | cards/ | 174 | 30.7 | frame, large_en, small_en |
| moduli/en | en.ini | 1 | 0.0 |  |
| moduli/en | intro/ | 2 | 0.4 | title_screen |
| moduli/en | ui_en/ | 50 | 3.5 | icon_sheets, icon_sheets.ini, result_letters, result_letters.ini, menu_lists, menu_lists.ini, deck_screens, deck_screens.ini, recipe_screens, recipe_screens.ini ... |

Every language except Italian is a **module** (`PSP/TEXTURES/modules/en`) to compose over the base pack with `tools/compose_pack.py BASE MODULES CARD_DIR OUT en [--copy]`: it copies the base and **only** the `cards`, `intro` and `ui_en` folders of the module (hard link or copy), then `module_ini.py` rewrites the `textures.ini`: the localized card lines point to `cards/small_en`/`large_en` and the lines of `en.ini` **replace** those of the base with the same key (hash).

### Base pack folders (the same for all languages)
| folder | content |
|---|---|
| `cards/small`, `cards/large` | original HD small/large cards by chrisfand (2,833 cards) with English texts; the language picks `small_<l>`/`large_<l>` via the ini |
| `cards/frame` | frames, attribute/race tables, Spell/Trap labels |
| `cards/tinyEN/JP/MikeyMK/tiny_<l>` | deck thumbnail atlas (7 pages; same hash in all languages: only one atlas wins per installation) |
| `characters` | HD portraits, sprites and 3D of the characters (MikeyMK) |
| `events` | event images (17) |
| `intro` | logo, title movie, new game; `title_screen` contains the tiles with the "Mystic Tomato Version" plate |
| `map` | map backgrounds |
| `shop` | shop, packs, rooms |
| `ui` | MikeyMK's English HD interface (for all languages with the same hashes) |
| `upscale_extra` | textures not covered by the pack, enlarged 4x with xBRZ (1,192 files, ~56 MB; at 4x/Auto resolution PPSSPP's 4xBRZ shader is off): includes the `card_icon03` variants of en/fr/de/es |
| `_CHOOSE YOUR CARD STYLE` | 3 alternative `textures.ini` (mikeymk, official_english, official_japanese): copy one in place of `textures.ini` to change the card style |

## B2. Card images

Language folders: `frame` (0 files), `large_en` (87 files), `small_en` (87 files). Every card has an **HD small** one (name + description + type, regenerated with free OFL fonts: XCharter Bold for names/type/labels, Libre Baskerville for effects, Newsreader Italic for Normals, PT Serif Caption for Spells/Traps, Charis SIL for the missing glyphs) and an **HD large** one (name only on the frame). In addition: the **attribute table** with the words of the language (`cards/frame/icons_attribute_race_<l>.png`, `attributes.py`), the **Spell/Trap label** (`icons_spell_trap_<l>.png`, `label_it.py` / `extract_labels.py` -> `data/label_eu_<code>_128x32.png`) and the deck **thumbnail atlas** (`tiny_<l>`, `tiny_atlas.py` + `tiny_fragment.py`).

When the text of a card changes (section A2) its images must be regenerated: **82 cards** in english. List in `docs/changes_en/card_images.csv`. Command: `python tools/generate_language.py fr PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` (without IDs it regenerates all of them: 2,833 + 2,833, ~930 MB).

Typography: non-breaking space before `: ; ! ?` and « » quotation marks.

## B3. HD interface in english (`ui_en`)

**43 textures** (`docs/changes_en/ui_textures.csv`: file, PPSSPP hash, family, script, original/HD size, neutral/specific, origin in the ISO). By family: icon_sheets 3, result_letters 4, menu_lists 2, deck_screens 14, recipe_screens 11, vs_screen 3, tutorial 6. Of these 0 are neutral (same hash in all languages) and 43 specific. Every family has a script in `tools/ui_textures/<family>.py` (reads `TF1_LANG`): it redraws the lettering texture by texture starting from the low-resolution original of the ISO and from the style of the English pack; same area and same positions (the game crops from fixed rectangles); one font/weight/baseline/shadow per lettering; free fonts (`alt_font.py`).

| family | textures | script | source ISO archive | language texts |
|---|---|---|---|---|
| icon_sheets | 3 | `tools/ui_textures/icon_sheets.py` | deck/all_e.ehp, shop/all_e.ehp, field/always_* | `icon04` (European pixels on the US sheet), `panel` (`ased` fragment of the tab), `pda_pack01` (NEW column) |
| result_letters | 4 | `tools/ui_textures/result_letters.py` | duel/basic_ee.ehp | `D R A W` tiles of the results screen (`result_e`) and of the banner (`basic_be`): same hash, 4 files |
| menu_lists | 2 | `tools/ui_textures/menu_lists.py` | title_menu/title_menu_e.ehp, duel/result/result_e.ehp, field/always_bri_<code>.ehp | `result_e__menu01` (WIN/DRAW/LOSE and icons), `title_menu_e__m_menu_title01` (MAIN MENU · ENTER NAME · DOWNLOADED CARD LIST · DUEL PUZZLE · OPTIONS · LANGUAGE SETTINGS) |
| deck_screens | 14 | `tools/ui_textures/deck_screens.py` | deck/all_e.ehp, labo/*.ehp, shop/all_e.ehp | tabs Trunk, Rental, Lab, Converter; `Card types in possession`; `Purchased Cards` / `Card Types Purche`; gold bar; ENTER key |
| recipe_screens | 11 | `tools/ui_textures/recipe_screens.py` | deck/recipe_view_e.ehp, title_menu/title_menu_e.ehp, database/limitlist.ehp | Character, User, Downloaded Recipes, Character Recipes, User Recipes, Limited, Semi-Limited, Forbidden, Trade |
| vs_screen | 3 | `tools/ui_textures/vs_screen.py` | duel/start/start_e.ehp (members _e), start_all.ehp, start_e.ehp | `2nd round`, `3rd round`, badge sheet `1st PLAYER` / `2nd PLAYER` / `PLAYER` |
| tutorial | 6 | `tools/ui_textures/tutorial.py` | tutorial/tutorial_e.ehp (tuto_duelimg01..06) | dialogue `Your opponent has declared battle. Activate the effect of a card?` (YES/NO) and 5 example cards with the game's text |

Quality rules (valid for every language): regular letters, never deformed one by one; same area as the original; no blur; the text is that of the language's original (only obvious errors are corrected: leftovers from other languages, accents); pixel art is **not** smoothed without confirmation; geometries always measured on the original.

### Drawn texts: original -> HD
Table read by eye, texture by texture: `docs/changes_en/texture_texts_en.md`. No word changed: the HD rewrites the same words as the English original (except `DOWNLOADED CARD LIST`, which the US pack has as `DOWNLOAD`).

### List of every texture
(all 43 rows, from `ui_textures.csv`)

| file in the pack | hash | family | original px | HD px | type | ISO origin |
|---|---|---|---|---|---|---|
| ui_en/icon_sheets/all_e__icon04.png | a51fdf03 | icon_sheets | 128x128 | 512x512 | SPECIFIC | deck/all_e.ehp:icon04.gim |
| ui_en/icon_sheets/all_e__panel.png | 4301b477 | icon_sheets | 256x256 | 1024x1024 | SPECIFIC | shop/all_e.ehp:panel.gim |
| ui_en/icon_sheets/always_bri_eng__pda_pack01.png | 180fee24 | icon_sheets | 512x256 | 2048x1024 | SPECIFIC | field/always_bri_eng.ehp:pda_pack01.gim; field/always_bri_fra.ehp:pda_pack01.gim; field/always_bri_spa.ehp:pda_pack01.gim |
| ui_en/result_letters/basic_be__duel_draw100002.png | b4fda5d3 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_be.ehp:duel_draw100002.gim; duel/basic_fe.ehp:duel_draw100002.gim; duel/basic_ge.ehp:duel_draw100002.gim |
| ui_en/result_letters/basic_be__duel_draw100004.png | 2973446a | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_be.ehp:duel_draw100004.gim; duel/basic_fe.ehp:duel_draw100004.gim; duel/basic_ge.ehp:duel_draw100004.gim |
| ui_en/result_letters/basic_be__duel_draw100006.png | 4b73998e | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_be.ehp:duel_draw100006.gim; duel/basic_fe.ehp:duel_draw100006.gim; duel/basic_ge.ehp:duel_draw100006.gim |
| ui_en/result_letters/basic_be__duel_draw100008.png | f720182b | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_be.ehp:duel_draw100008.gim; duel/basic_fe.ehp:duel_draw100008.gim; duel/basic_ge.ehp:duel_draw100008.gim |
| ui_en/menu_lists/result_e__menu01.png | b602d300 | menu_lists | 256x64 | 1024x256 | SPECIFIC | duel/result/result_e.ehp:menu01.gim; duel/result/result_j.ehp:menu01.gim |
| ui_en/menu_lists/title_menu_e__m_menu_title01.png | 1d377d3b | menu_lists | 256x128 | 1024x512 | SPECIFIC | title_menu/title_menu_e.ehp:m_menu_title01.gim |
| ui_en/deck_screens/all_e__d_window00008.png | 92c07948 | deck_screens | 128x32 | 512x128 | SPECIFIC | deck/all_e.ehp:d_window00008.gim |
| ui_en/deck_screens/all_e__d_window00033.png | 4400d119 | deck_screens | 256x32 | 1024x128 | SPECIFIC | deck/all_e.ehp:d_window00033.gim |
| ui_en/deck_screens/all_e__d_window00051.png | b7e9dc1a | deck_screens | 64x32 | 256x128 | SPECIFIC | deck/all_e.ehp:d_window00051.gim |
| ui_en/deck_screens/all_e__d_window00062.png | 61dffec6 | deck_screens | 128x32 | 512x128 | SPECIFIC | deck/all_e.ehp:d_window00062.gim; labo/conv_machine.ehp:window_e0016.gim; title_menu/title_menu_e.ehp:t_window0015.gim |
| ui_en/deck_screens/all_e__d_window00101.png | 082a50da | deck_screens | 64x32 | 256x128 | SPECIFIC | deck/all_e.ehp:d_window00101.gim; labo/rental.ehp:window_e0008.gim |
| ui_en/deck_screens/all_e__tab_title.png | 80de9436 | deck_screens | 256x32 | 1024x128 | SPECIFIC | shop/all_e.ehp:tab_title.gim |
| ui_en/deck_screens/conv_machine__window_e0009.png | 9c07916c | deck_screens | 128x32 | 512x128 | SPECIFIC | labo/conv_machine.ehp:window_e0009.gim; labo/conv_machine.ehp:window_e0026.gim |
| ui_en/deck_screens/conv_machine__window_e0016.png | 61dffec6 | deck_screens | 128x32 | 512x128 | SPECIFIC | deck/all_e.ehp:d_window00062.gim; labo/conv_machine.ehp:window_e0016.gim; title_menu/title_menu_e.ehp:t_window0015.gim |
| ui_en/deck_screens/conv_machine__window_e0022.png | cad9bed1 | deck_screens | 256x32 | 1024x128 | SPECIFIC | labo/conv_machine.ehp:window_e0022.gim; labo/rental.ehp:window_e0021.gim; title_menu/title_menu_e.ehp:t_window0021.gim |
| ui_en/deck_screens/conv_machine__window_e0026.png | 9c07916c | deck_screens | 128x32 | 512x128 | SPECIFIC | labo/conv_machine.ehp:window_e0009.gim; labo/conv_machine.ehp:window_e0026.gim |
| ui_en/deck_screens/password__key_e0027.png | 80e78a95 | deck_screens | 128x32 | 512x128 | SPECIFIC | labo/password.ehp:key_e0027.gim; labo/password.ehp:key_j0027.gim |
| ui_en/deck_screens/rental__window_e0008.png | 082a50da | deck_screens | 64x32 | 256x128 | SPECIFIC | deck/all_e.ehp:d_window00101.gim; labo/rental.ehp:window_e0008.gim |
| ui_en/deck_screens/rental__window_e0015.png | 93c88910 | deck_screens | 128x32 | 512x128 | SPECIFIC | labo/rental.ehp:window_e0015.gim |
| ui_en/deck_screens/rental__window_e0026.png | 4fa2b5e3 | deck_screens | 64x32 | 256x128 | SPECIFIC | labo/rental.ehp:window_e0026.gim |
| ui_en/recipe_screens/limitlist__window_e0002.png | c1e2ff0d | recipe_screens | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_e0002.gim |
| ui_en/recipe_screens/limitlist__window_e0004.png | 6f593093 | recipe_screens | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_e0004.gim |
| ui_en/recipe_screens/limitlist__window_e0012.png | 5e3bc044 | recipe_screens | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_e0012.gim |
| ui_en/recipe_screens/recipe_view_e__recipe010008.png | 72966f8d | recipe_screens | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_e.ehp:recipe010008.gim; title_menu/title_menu_e.ehp:recipe_sel00002.gim |
| ui_en/recipe_screens/recipe_view_e__recipe010015.png | 4efbece8 | recipe_screens | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_e.ehp:recipe010015.gim; title_menu/title_menu_e.ehp:recipe_sel00009.gim |
| ui_en/recipe_screens/recipe_view_e__recipe010027.png | 4d84d0c5 | recipe_screens | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_e.ehp:recipe010027.gim; title_menu/title_menu_e.ehp:recipe_sel00020.gim |
| ui_en/recipe_screens/recipe_view_e__recipe010029.png | e2538eef | recipe_screens | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_e.ehp:recipe010029.gim; title_menu/title_menu_e.ehp:recipe_sel00022.gim |
| ui_en/recipe_screens/recipe_view_e__recipe010031.png | 6ca29a28 | recipe_screens | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_e.ehp:recipe010031.gim; title_menu/title_menu_e.ehp:recipe_sel00024.gim |
| ui_en/recipe_screens/title_menu_e__recipe_sel00033.png | 96fe0ef6 | recipe_screens | 128x32 | 512x128 | SPECIFIC | title_menu/title_menu_e.ehp:recipe_sel00033.gim |
| ui_en/recipe_screens/title_menu_e__t_window0008.png | 05ec86c0 | recipe_screens | 64x32 | 256x128 | SPECIFIC | title_menu/title_menu_e.ehp:t_window0008.gim |
| ui_en/recipe_screens/title_menu_e__t_window0026.png | 45902d92 | recipe_screens | 64x32 | 256x128 | SPECIFIC | title_menu/title_menu_e.ehp:t_window0026.gim |
| ui_en/vs_screen/start_e__d_menu01_e.png | 905aa050 | vs_screen | 256x256 | 1024x1024 | SPECIFIC | duel/start/start_e.ehp:d_menu01_e.gim; duel/start/start_f.ehp:d_menu01_e.gim; duel/start/start_g.ehp:d_menu01_e.gim |
| ui_en/vs_screen/start_e__vs_much2_e0001.png | 7b22a421 | vs_screen | 128x16 | 512x64 | SPECIFIC | duel/start/start_all.ehp:vs_much2_e0001.gim; duel/start/start_e.ehp:vs_much2_e0001.gim; duel/start/start_f.ehp:vs_much2_e0001.gim |
| ui_en/vs_screen/start_e__vs_much3_e0001.png | e71966a5 | vs_screen | 128x16 | 512x64 | SPECIFIC | duel/start/start_all.ehp:vs_much3_e0001.gim; duel/start/start_e.ehp:vs_much3_e0001.gim; duel/start/start_f.ehp:vs_much3_e0001.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg01.png | 5fb78e9f | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_e.ehp:tuto_duelimg01.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg02.png | 0a1af418 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_e.ehp:tuto_duelimg02.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg03.png | 57602964 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_e.ehp:tuto_duelimg03.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg04.png | fa80718b | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_e.ehp:tuto_duelimg04.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg05.png | 7fe0878d | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_e.ehp:tuto_duelimg05.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg06.png | 7bbf6d19 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_e.ehp:tuto_duelimg06.gim |

### English textures that stay as they were
The English textures already covered by the US pack (same hash: 621) come from MikeyMK and are not touched. The textures without text or common to all languages stay **enlarged with xBRZ** (`upscale_extra`) or without a file (14, fragments without text: they look like the original) (the 4 DRAW tiles of the results screen are redrawn in `result_letters`). 17 textures of the Italian pack have the same hash as the English ones (`ITA-ON-ENG`): checked one by one, they have no text. Complete list: `docs/changes_en/texture_inventory_en.txt`.

## B4. The duel number sheet (`card_icon03`)

A single sheet with LP digits, time, keys and multipliers; different hash per language. Recipe chosen by the user (`tools/ui_textures/icon03_languages.py`, rerun with `--apply`):
- rows 0-180 (small digits and signs, orange keys 1/2/3, big digits 0-9 with "LP", small digits 0-9): **from the US pack**, crisp pixel art;
- cells in which the European game differs from the US pack (black check mark, grey ball, empty pill, time word): **original pixels enlarged 4x without smoothing**; time word **TIME**; the orange pill ("Single" in the US pack) stays **empty**;
- rows >= 181 (multipliers x1..x12, icons, cards, arrows): from the Italian sheet already in the pack (`tools/data/card_icon03_base_it.png`);
- the European cells are pasted **only in their band** of rows (otherwise they spoil the top of the big digits).

Files: it -> `ui_it/duel_texts/basic_ii__card_icon03.png` (hash 376925c7); fr -> `upscale_extra/3e5482fd.png`; en ee0c44c3; de ffe309a6; es 859eea2b. Previews in `comparisons/icon03/`.

## B5. Title plate

`python tools/ui_textures/mystic_tomato_title.py en` generates 2 PNGs (`542eff79685c434d`, `705176739829dcf5`, tiles 18 and 19 of the 20-tile 128x64 backdrop `title_menu_i.ehp: main_title00001..00020`) with card 4930 in the language + the "version" wording + the flag, PT Sans Bold font: **"VERSION MYSTIC TOMATO"**. The plate **is included only for the chosen language** (it lives in `modules/en/intro/title_screen/`); the original base pack has the tiles without a banner. Files in this pack: `moduli/en/intro/title_screen/00000000542eff79685c434d.png`, `moduli/en/intro/title_screen/00000000705176739829dcf5.png`.

## B6. `textures.ini` and composition

`tools/gen_ini.py TOOLS US_INI CARD_DIR OUT_INI i=it +extra_it.ini +ui_it.ini +data/upscale_extra.ini` converts the US `textures.ini` into the EU one: the non-card entries stay (neutral textures = same hashes); the card entries are regenerated from the EU `card/*.cip` archives for the 5 languages (`i=it` remaps `cards/large/X.png` -> `cards/large_it/X.png`); it adds the Spell/Trap label (`extra_it.ini`), the `ui_it` lines and `upscale_extra.ini`. It is also done for the 3 card styles. If the same pixels exist in several languages the first in `e i f g s` wins (for this reason atlas, banner and attribute table are "one per installation").

`ui_en` lines in `en.ini`: 43. Prefix frequency: `docs/changes_en/ini_lines.csv`. Check: every `ui_en/...` line must point to an existing file and there must be no duplicate hashes.

## B7. Installation and settings

PC: copy `ULES00600` into `<PPSSPP>/PSP/TEXTURES/` (Android: `textures.zip` in `.../TEXTURES/ULES00600/`, without extracting it; regenerate the zip with the corrections). Settings: **Replace textures ON**, rendering resolution **4x**, game language = module language (the language is stored in the **save file**). After changing a single PNG it is enough to copy it and restart PPSSPP (cache). To try the texts use the `_definitiva` ISO.

---

# C. EDITORIAL CHOICES

- **Only objective errors** of European English: typos (`Sryus`, `Principle's`, `Bandanna`), articles (`a Equip Spell` -> `an Equip Spell`, `face-down card` -> `a face-down card`), apostrophes (`monsters's`, `opponents cards`), agreement, verb forms in the tutorials (`"Summon" it` -> `"Summoning" it`), extra spaces and `$` in the color codes. No stylistic rewriting.
- `Chancellor Sheppard` in the cards, as in the dialogues; `Bandana` as in the dialogues.
- Card terms and texts left as in the game; the 82 corrected cards have their text regenerated in the HD images (`modules/en/cards`).
- The English title plate is `VERSION MYSTIC TOMATO` (confirmed by the user on 2026-10-13).
- Number sheet: digits/LP from the US pack, x1..x12 from the Italian sheet, time word TIME.

### Entries of the choices register for this language (`tools/data/editorial_choices.json`)
| id | original | corrected | inherited | reason |
|---|---|---|---|---|
| st01_t01/Scr003E#146 | My father owns a hot sauce⏎company. | My father owns a sake⏎brewery. | no | sake instead of hot sauce (faithful to the Japanese: Chumley's family makes sake) |
| st01_t01/Scr003E#147 | He sent me some hot sauce with my⏎last allowance.⏎I'll give ya a reasonable discount.⏎Do you wanna... | He sent me some shochu with my⏎last allowance.⏎I'll give ya a reasonable discount.⏎Do you wanna... | no | shochu instead of hot sauce |
| st01_t01/Scr003E#150 | My father owns a hot sauce⏎company. | My father owns a sake⏎brewery. | no | same as 146 |
| st01_t01/Scr003E#151 | He sent me some hot sauce⏎with my last allowance.⏎I'll give ya a reasonable discount.⏎Do you wanna... | He sent me some shochu⏎with my last allowance.⏎I'll give ya a reasonable discount.⏎Do you wanna... | no | same as 147 |
| st01_t01/Scr003E#163 | Wow. You really did it.⏎It's 《C026_2》...⏎Wearing a bikini! | Wow. You really did it.⏎It's 《C026_2》...⏎Wearing a maid outfit! | no | maid outfit instead of bikini (Japanese: メイド服) |
| st01_t01/Scr003E#168 | Wow. You really did it.⏎It's 《C026_2》...⏎Wearing a bikini! | Wow. You really did it.⏎It's 《C026_2》...⏎Wearing a maid outfit! | no | same as 163 |
| st01_t01/Scr003E#188 | Well, I suppose I dabble a little... | None | yes | Italian only: "sto sbavando" was a translation error (Japanese: "I am not that good") |
| st01_t01/Scr003E#189 | Hey, can you draw a picture for me then?⏎Draw me 《C026_2》 in a bikini! | Hey, can you draw a picture for me then?⏎Draw me 《C026_2》 in a maid outfit! | no | maid outfit instead of bikini |
| st01_t01/Scr003E#191 | Here, you can use this! | Here, use this maid outfit! | no | Syrus hands over a maid outfit as a model (メイド服): with the bikini the joke made no sense |
| st01_t01/Scr003E#194 | Well, I suppose I dabble a little... | None | yes | same as 188 |
| st01_t01/Scr003E#195 | Hey, can you draw a picture for me then?⏎Draw me 《C026_2》 in a bikini! | Hey, can you draw a picture for me then?⏎Draw me 《C026_2》 in a maid outfit! | no | same as 189 |
| st01_t01/Scr003E#197 | Here, you can use this! | Here, use this maid outfit! | no | same as 191 |

Other choices and the re-reading of the duel sentences: `docs/EDITORIAL_CHOICES.md`.

# D. IN-GAME VERIFICATION

- **Not seen in game**: the `_definitiva` ISO and the composed English pack have not been tried in PPSSPP yet. Checked only on the data: `apply_to_iso.py` with 0 warnings, every `ui_en` line of `textures.ini` points to an existing file, original/HD comparisons in `docs/changes_en/sheets/` (original 4x next to the HD, re-read by eye).
- To see in game: card with new text, corrected dialogues, editor help, tabs Trunk/Rental/Lab/Converter, `Purchased Cards`, `2nd/3rd round`, `1st/2nd PLAYER` badges, `MAIN MENU` and menu entries, duel tutorial.

# E. HOW TO REGENERATE EVERYTHING

```
# ISO (all languages together)
python tools/corrections/build_dialogues.py en
python tools/corrections/generate_card_corrections.py en CARDINFO_en.ehp          # cards
python tools/corrections/apply_to_iso.py PSP/GAME/ULES00600_..._EUR.iso PSP/GAME/ULES00600_..._EUR_definitiva.iso
# images
python tools/generate_language.py fr PACK CARDINFO US_INI CLEAN_DIR OUT [ID...]
TF1_LANG=en python tools/ui_textures/<family>.py USRDIR PACK_US <module>      # for each of the 8 families (whole!)
python tools/ui_textures/icon03_languages.py --apply ; python tools/ui_textures/mystic_tomato_title.py en
python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules USRDIR/card OUT en --copy
# this document
python tools/analysis/document_changes.py ISO_ORIG ISO_DEF en docs/changes_en
python tools/analysis/document_pack.py ISO_ORIG en docs/changes_en
python tools/analysis/text_comparisons.py en
python tools/analysis/write_changes_document.py en
```
External inputs you need (check that they exist): the original ISO, the extracted USRDIR (`tools/analysis/extract_usrdir.py`), MikeyMK's US pack `ULUS10136` (in a folder outside the project).

# F. LIMITS AND OPEN POINTS

- **User decisions (2026-10-13)**: logo name `VERSION MYSTIC TOMATO` confirmed; DRAW tiles to be redrawn (done); (1) logo name confirmed; (2) `DOWNLOADED CARD LIST` (European) versus `DOWNLOAD` (US text): the European one was chosen, confirmed by the user.
- Android `textures.zip` for English: not done; no test on a phone.
- The texts drawn in the textures are in `docs/changes_en/texture_texts_en.md` (read by eye).
- The speaker name in the dialogue box cannot be modified (encrypted EBOOT).
