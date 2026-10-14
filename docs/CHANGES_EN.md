# MODIFICHE PER LA VERSIONE POMODORO MISTICO IN INGLESE

Documento **completo** di tutto cio' che la "Versione Pomodoro Mistico" cambia per il inglese: (A) le modifiche **dirette alla ISO**, (B) il **texture pack** (com'e' fatto, cosa contiene, come si compone), (C) le scelte editoriali, (D) cosa e' verificato in gioco e cosa no, (E) come rigenerare tutto.

**Questo file e' generato** da `tools/analysis/write_changes_document.py en` a partire dai dati reali: confronto byte per byte tra la ISO originale `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` e la ISO corretta `..._definitiva.iso` (`document_changes.py`) e scansione del pack (`document_pack.py`). Gli elenchi riga per riga stanno in `docs/changes_en/*.csv` (separatore `;`, UTF-8 con BOM, a capo come `⏎`): sono la **lista esatta** di ogni cambiamento. Rigenera tutto dopo ogni modifica.

Per il metodo generale e per le altre lingue: `docs/NEW_LANGUAGE_GUIDE.md`; dettagli tecnici degli script: `TUTORIAL.md`; decisioni: `docs/EDITORIAL_CHOICES.md`; texture neutre/specifiche: `docs/TEXTURE_INVENTORY.md`.

## Indice
- A. Modifiche alla ISO: A1 panoramica · A2 carte · A3 dialoghi · A4 frasi dei duelli · A5 stringhe dell'interfaccia · A6 etichetta Magia/Trappola · A7 file toccati e dettagli tecnici · A8 cosa non si puo' cambiare
- B. Texture pack: B1 provenienza e struttura · B2 immagini delle carte · B3 interfaccia HD (`ui_en`) · B4 foglio numeri (`card_icon03`) · B5 targa del titolo · B6 textures.ini e composizione · B7 installazione
- C. Scelte editoriali · D. Verifica in gioco · E. Come rigenerare · F. Limiti e punti aperti

---

# A. MODIFICHE ALLA ISO

## A1. Panoramica

La ISO originale **non viene mai modificata**. `tools/corrections/apply_to_iso.py ISO_ORIG ISO_OUT [lingue]` ne crea una copia in cui alcuni archivi `.ehp` sono riscritti. Se un archivio cresce (testo piu' lungo) viene **rimesso in fondo alla ISO** in un nuovo settore e il suo voce nella directory ISO9660 viene riassegnata (`pycdlib`); la ISO `_definitiva` pesa per questo ~909 MB (l'originale ~761 MB). **Lanciarlo sempre senza elenco di lingue (o con tutte)**: con una lingua sola sovrascrive le altre.

| Cosa | Quantita' (derivata dal confronto ISO) | Dove sta il dato | File CSV |
|---|---|---|---|
| Carte con testo cambiato (nome e/o descrizione) | 82 carte (83 campi) | `tools/data/card_corrections_en.json` da `correzioni/rules_en.py` | cards.csv |
| Righe di dialogo della storia | 402 righe | `tools/data/dialogue_touchups_en.json` (+ base) | dialogues.csv |
| Frasi dei duellanti nei duelli | 11 frasi uniche (15 voci in tutti gli archivi) | `tools/data/duel_line_corrections_en.json` | duel_lines.csv |
| Stringhe dell'interfaccia (aiuti, schede, record, tutorial, menu...) | 57 stringhe uniche (215 voci, 51 archivi) | `correzioni/string_rules_en.py` + `dati/ui_texts.json` | ui_strings.csv |
| Immagini sostituite dentro la ISO | 0 (etichetta [CARTA MAGIA/TRAPPOLA] della carta grande) | `apply_to_iso.py` (copia `card_spell_trap.gim` della lingua) | iso_images.csv |
| File della ISO toccati (archivi `.ehp`) | 182 | - | touched_files.csv |
| Altre differenze tecniche (offset ricalcolati) | 254 | - | other.csv |

## A2. Testi delle carte

Archivio: `PSP_GAME/USRDIR/duelsys/cardinfo_fra.ehp` (tabelle `CARD_Name_*`, `CARD_Desc_*`, `CARD_Indx_*`). **82 carte** hanno nome e/o descrizione modificati. Si correggono **solo errori oggettivi** (refusi, accenti, apostrofi, spazi, maiuscole incoerenti, concordanze, plurali fissi, residui di altre lingue); nomi ufficiali e terminologia del gioco non si toccano.

Come: ogni carta e' stata letta (inglese: elenco di tutte le carte in confronti/audit_en/carte_en.txt, solo errori oggettivi). Regole in `tools/corrections/rules_en.py`: **26 regole globali** (regex applicate a nomi e descrizioni di tutte le carte) e **42 correzioni per carta** (`PER_CARTA`: id, campo, vecchio, nuovo, motivo; il vecchio testo deve esistere esattamente). `generate_card_corrections.py en CARDINFO` (scrive `card_corrections_{L}.json` partendo dai testi originali) produce il json; `apply_to_iso` lo scrive nella ISO; le immagini HD delle carte toccate si rigenerano (sezione B2).

### Regole globali (tutte)
| modello (regex) | sostituzione | motivo |
|---|---|---|
| \bposible\b | possible | refuso |
| \bfortell\b | foretell | refuso |
| \bmistical\b | mystical | refuso |
| \bmassibe\b | massive | refuso |
| \benourmous\b | enormous | refuso |
| \bTrbute\b | Tribute | refuso |
| \btrbute\b | tribute | refuso |
| (?i)\btrbute | tribute | refuso (qualunque forma) |
| \bfliipped\b | flipped | refuso |
| \bDefence\b | Defense | ortografia incoerente: il gioco usa "Defense" in tutte le altre carte |
| \bDefensive Position\b | Defense Position | terminologia: "Defense Position" nel resto del gioco |
| 　(?=\n) |  | spazio ideografico (giapponese) a fine riga |
| 　 |   | spazio ideografico (giapponese) al posto dello spazio normale |
| \bside the field\b | side of the field | preposizione omessa (carte Toon) |
| \byour must select\b | you must select | refuso (your/you) |
| \bcan Inflict Direct Damage\b | can inflict Direct Damage | maiuscola a meta' frase |
| \bBy tributing\b | By Tributing | "Tribute" ha la maiuscola in tutto il gioco |
| \bbattle damage\b | Battle Damage | "Battle Damage" ha le maiuscole in tutto il gioco |
| \bthis Turn\b | this turn | maiuscola incoerente |
| \bthe Turn\b | the turn | maiuscola incoerente |
| \bthis turns End Phase\b | this turn's End Phase | apostrofo del genitivo |
| \b1card\b | 1 card | spazio mancante |
| \byour opponent's Field\b | your opponent's side of the field | "field" in minuscolo e formula del resto del gioco |
| \byour Field\b | your side of the field | "field" in minuscolo e formula del resto del gioco |
| \bthe Field\b(?! Spell) | the field | "field" in minuscolo (il resto del gioco) |
| \byour Hand\b | your hand | "hand" in minuscolo (il resto del gioco) |

### Correzioni per carta (tutte)
| id | campo | vecchio | nuovo | motivo |
|---|---|---|---|---|
| 4564 | desc | he is a errand boy | he is an errand boy | articolo |
| 4483 | desc | with saw-like head | with a saw-like head | articolo omesso |
| 4601 | desc | into mirror world | into a mirror world | articolo omesso |
| 4372 | desc | a labyrinth no exit | a labyrinth with no exit | parola omessa |
| 5266 | desc | The number of monster(s) are applied | The number of monster(s) is applied | concordanza |
| 4232 | desc | this monsters grabs | this monster grabs | concordanza (plurale al posto del singolare) |
| 4492 | desc | a wealth of spell written | a wealth of spells written | plurale mancante |
| 4546 | desc | from your deck | from your Deck | maiuscola: "Deck" in tutto il gioco |
| 5062 | desc | "Worm Drake"+"Humanoid Slime" | "Worm Drake" + "Humanoid Slime" | spazi attorno al + come nelle altre fusioni |
| 5096 | desc | your opponents side | your opponent's side | apostrofo del genitivo |
| 5184 | desc | "Don Zaloog"and | "Don Zaloog" and | spazio mancante |
| 5753 | desc | your opponent cannot player cannot activate | your opponent cannot activate | parole doppie (refuso) |
| 6007 | name | Marshmallon glasses | Marshmallon Glasses | nome ufficiale: maiuscola |
| 6302 | desc | from⏎your hand | from your hand | a capo in mezzo alla frase |
| 6639 | desc | When this card are successfully | When this card is successfully | concordanza |
| 6640 | desc | includes "sphinx" in | includes "Sphinx" in | maiuscola (parte di nome) |
| 6684 | desc | Special Summon 1"Option Token" | Special Summon 1 "Option Token" | spazio mancante |
| 6229 | desc | field, tributing 1 monster | field, Tributing 1 monster | "Tribute" ha la maiuscola |
| 6229 | desc | that is level 5 or below | that is Level 5 or below | "Level" ha la maiuscola |
| 5358 | desc | Offer each of your Monsters | Offer each of your monsters | maiuscola incoerente |
| 5367 | desc | While that Monster is | While that monster is | maiuscola incoerente |
| 5451 | desc | all Monsters on | all monsters on | maiuscola incoerente |
| 5493 | desc | your opponent's Monster attacks | your opponent's monster attacks | maiuscola incoerente |
| 5493 | desc | Spell and Trap cards | Spell and Trap Cards | maiuscola incoerente |
| 5497 | desc | Returns 1 Monster on | Returns 1 monster on | maiuscola incoerente |
| 5497 | desc | one Level 4 Monster from | one Level 4 monster from | maiuscola incoerente |
| 5497 | desc | to your Hand | to your hand | maiuscola incoerente |
| 5557 | desc | when a Monster on | when a monster on | maiuscola incoerente |
| 5557 | desc | one Level 4 Monster from | one Level 4 monster from | maiuscola incoerente |
| 5561 | desc | Zombie-type card | Zombie-Type card | "Type" ha la maiuscola |
| 5561 | desc | adding it to your Hand | adding it to your hand | maiuscola incoerente |
| 5743 | desc | face-up Monster on | face-up monster on | maiuscola incoerente |
| 5743 | desc | when a Monster is destroyed | when a monster is destroyed | maiuscola incoerente |
| 6003 | desc | Select 1 Monster in Defense | Select 1 monster in Defense | maiuscola incoerente |
| 6231 | desc | each Monster on | each monster on | maiuscola incoerente |
| 6288 | desc | selecting 1 Monster face-up | selecting 1 monster face-up | maiuscola incoerente |
| 6288 | desc | the selected Monster's ATK | the selected monster's ATK | maiuscola incoerente |
| 6288 | desc | every other Monster face-up | every other monster face-up | maiuscola incoerente |
| 6288 | desc | other Monsters in face-up | other monsters in face-up | maiuscola incoerente |
| 6291 | desc | Zombie-Type Monster with | Zombie-Type monster with | maiuscola incoerente |
| 6291 | desc | The selected Monster will | The selected monster will | maiuscola incoerente |
| 6450 | desc | all Monster cards in | all Monster Cards in | maiuscola incoerente |

### Elenco completo delle carte cambiate
**Confronto completo originale -> nuovo con le parole cambiate evidenziate: `docs/changes_en/cards_diff.md`** (tutte le 83 voci). Dati grezzi: `docs/changes_en/cards.csv`. Prime 40 righe:

| id | nome originale | campo | originale | nuovo |
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

(... altre 43 righe nel CSV)

## A3. Dialoghi della storia

Archivi: `script/stNN_<scena>_f.ehp`, ogni scena e' una coppia di membri `...If.bin` (offset in caratteri UTF-16) e `...Lf.bin` (stringhe UTF-16LE chiuse da NUL, alcune compresse in gzip). **402 righe** cambiate (comprese quelle che **ereditano** la correzione perche' hanno lo stesso testo originale e lo stesso giapponese di una riga corretta).

Flusso: lettura riga per riga confrontata con inglese e giapponese -> ritocchi in `tools/data/dialogue_touchups_en.json` (`esatte` e `parti`) -> `build_dialogues.py en` -> `dialogue_corrections_en.json` -> `apply_to_iso.py`. Regole automatiche di impaginazione in `build_dialogues.py`: spazio non separabile prima di `! ? : ;` anche dopo `》` (regola `FR_PUNT`), spazio dopo i segnaposto, "Mode histoire" -> "Mode aventure". Vincoli del box: ~46 caratteri per riga, max 3 righe (un segnaposto vale ~6 caratteri): `apply_to_iso` segnala le righe che potrebbero non starci.

### Ritocchi di rilettura: `esatte` (2) — frase intera originale -> frase nuova
| originale | nuovo |
|---|---|
| Here, you can use this! | Here, use this maid outfit! |
|  He's Attie now! | He's Attie now! |

### Ritocchi di rilettura: `parti` (79) — sostituzioni di testo applicate a ogni riga (in ordine)
| vecchio | nuovo |
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

### Elenco completo delle righe
**Confronto completo originale -> nuovo (con inglese e giapponese): `docs/changes_en/dialogues_diff.md`** (tutte le 402 righe). Dati grezzi: `docs/changes_en/dialogues.csv`. Prime 30:

| id | originale | nuovo | inglese |
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

(... altre 372 righe nel CSV)

## A4. Frasi dei duellanti nei duelli

Tabelle `chr_wordstbl_f.bin` e `02chr_wordstbl_...` dentro ~72 archivi `duel/cutin_*.ehp` (e `zakov*`). Le frasi uniche sono ~1.800: tutte rilette. **11 frasi cambiate** (15 voci). Dati: `esatte` (3) e `parti` (6) in `duel_line_corrections_en.json`. I file `*-ptrs.txt` degli archivi dei personaggi contengono offset assoluti: se una tabella cresce vanno ricalcolati (`rimappa_puntatori`), altrimenti il duello va in crash.

Confronto con parole evidenziate: `docs/changes_en/duel_lines_diff.md`.

| originale | nuovo | voci | esempi di archivio |
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

## A5. Stringhe lunghe e corte dell'interfaccia

Tabelle `strTbl*`, `help_strtbl_*`, `ddstrtbl_*`, `field_strtbl*` (formato `(n, 12, 12+4n)` + offset + UTF-16) in 51 archivi (la stessa tabella e' copiata in piu' archivi, es. `field/always_*_fra.ehp` x6). **57 stringhe uniche cambiate**. Regole: `tools/corrections/string_rules_en.py` — **53 voci `STRINGHE`** (archivio, membro, indice 0-based, [(vecchio, nuovo)], motivo), **1 `GLOBALI`** (regex/callable, applicate dopo le STRINGHE) su **29 tabelle** (`TABELLE`); piu' 0 correzioni puntuali in `tools/data/ui_texts.json` (scrittura sul posto, testo piu' corto o uguale).

### Per membro (stringhe uniche cambiate)
| membro | stringhe |
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

### Regole globali (tutte)
| modello | sostituzione | motivo |
|---|---|---|
| (\$C0)\$(?= ) | \1 | "$" di troppo dopo il codice colore $C0 (lezioni del tutorial) |

### Voci STRINGHE (tutte): dove e perche'
| archivio | membro | indice | cambiamenti | motivo |
|---|---|---|---|---|
| database/charalist.ehp | strTbl_e.bin | 13 | 2 sostituzione/i | articolo / "a" di troppo |
| database/charalist.ehp | strTbl_e.bin | 30 | 1 sostituzione/i | relativa sbagliata |
| database/charalist.ehp | strTbl_e.bin | 37 | 1 sostituzione/i | every day (avverbio) |
| database/charalist.ehp | strTbl_e.bin | 48 | 1 sostituzione/i | pronome di troppo |
| database/charalist.ehp | strTbl_e.bin | 52 | 1 sostituzione/i | refuso (Principle's) e titolo del personaggio come nei dialoghi (Chancellor) |
| database/duelrecord.ehp | strTbl_e.bin | 42 | 1 sostituzione/i | apostrofo |
| duel/result/result_e.ehp | strTbl.bin | 42 | 1 sostituzione/i | apostrofo |
| database/limitlist.ehp | strTbl_e.bin | 6 | 1 sostituzione/i | maiuscola: Deck |
| database/limitlist.ehp | strTbl_e.bin | 7 | 1 sostituzione/i | maiuscola: Deck |
| database/limitlist.ehp | strTbl_e.bin | 8 | 1 sostituzione/i | maiuscola: Deck |
| deck/all_e.ehp | help_strtbl_contents.bin | 128 | 1 sostituzione/i | forma verbale |
| deck/all_e.ehp | help_strtbl_contents.bin | 140 | 1 sostituzione/i | parole invertite |
| deck/all_e.ehp | help_strtbl_contents.bin | 162 | 1 sostituzione/i | refuso |
| deck/all_e.ehp | help_strtbl_contents.bin | 166 | 2 sostituzione/i | grammatica |
| deck/tutorial.ehp | strTbl_e.bin | 4 | 1 sostituzione/i | any way |
| deck/tutorial.ehp | strTbl_e.bin | 81 | 1 sostituzione/i | verbo mancante |
| deck/tutorial.ehp | strTbl_e.bin | 147 | 1 sostituzione/i | concordanza (soggetto: Using ... functions) |
| deck/tutorial.ehp | strTbl_e.bin | 203 | 1 sostituzione/i | comparativo doppio |
| duel/basic_*e.ehp | ddstrtbl_e.bin | 84 | 1 sostituzione/i | refuso |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 109 | 1 sostituzione/i | sostantivo mancante |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 122 | 1 sostituzione/i | forma verbale |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 134 | 1 sostituzione/i | parole invertite |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 154 | 1 sostituzione/i | any time |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 160 | 1 sostituzione/i | forma verbale |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 163 | 1 sostituzione/i | soggetto mancante |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 164 | 1 sostituzione/i | soggetto mancante |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 182 | 1 sostituzione/i | refuso |
| duel/basic_*e.ehp | help_strtbl_contents_duel_e.bin | 186 | 2 sostituzione/i | grammatica |
| field/always_*_eng.ehp | field_strtbl.bin | 14 | 1 sostituzione/i | articolo mancante |
| field/always_*_eng.ehp | field_strtbl.bin | 27 | 1 sostituzione/i | punto esclamativo a larghezza piena |
| field/always_*_eng.ehp | field_strtbl.bin | 28 | 1 sostituzione/i | punto esclamativo a larghezza piena |
| field/always_*_eng.ehp | field_strtbl.bin | 99 | 1 sostituzione/i | spazio prima del ! |
| field/always_*_eng.ehp | field_strtbl_item.bin | 4 | 1 sostituzione/i | refuso (nei dialoghi: Bandana) |
| field/always_*_eng.ehp | field_strtbl_item.bin | 104 | 1 sostituzione/i | refuso |
| field/always_*_eng.ehp | field_strtbl_item.bin | 161 | 1 sostituzione/i | virgola al posto del punto |
| field/always_*_eng.ehp | field_strtbl_item.bin | 182 | 1 sostituzione/i | doppio spazio, articolo |
| field/always_*_eng.ehp | field_strtbl_item.bin | 185 | 1 sostituzione/i | punto mancante |
| field/always_*_eng.ehp | field_strtbl_item.bin | 198 | 1 sostituzione/i | refuso |
| title_menu/title_menu_?.ehp | tushin_msg_e.bin | 36 | 1 sostituzione/i | spazio mancante |
| title_menu/title_menu_?.ehp | tushin_msg_e.bin | 46 | 1 sostituzione/i | spazio mancante |
| field/always_*_eng.ehp | event_name.bin | 10 | 1 sostituzione/i | preposizione di troppo |
| duel/basic_*.ehp | option_msg_e.bin | 26 | 1 sostituzione/i | its (possessivo) |
| field/always_*_eng.ehp | option_msg_e.bin | 26 | 1 sostituzione/i | its (possessivo) |
| title_menu/title_menu_?.ehp | option_msg_e.bin | 26 | 1 sostituzione/i | its (possessivo) |
| tutorial/tutorial_e.ehp | 01_message_res.bin | 59 | 2 sostituzione/i | nome scritto male, doppio spazio |
| tutorial/tutorial_e.ehp | 01_message_res.bin | 109 | 1 sostituzione/i | apostrofo |
| tutorial/tutorial_e.ehp | 01_message_res.bin | 138 | 1 sostituzione/i | participio |
| tutorial/tutorial_e.ehp | 02_message_res.bin | 17 | 1 sostituzione/i | forma verbale |
| tutorial/tutorial_e.ehp | 02_message_res.bin | 60 | 1 sostituzione/i | forma verbale |
| tutorial/tutorial_e.ehp | 03_message_res.bin | 70 | 1 sostituzione/i | termine sbagliato (ritual -> Tribute) |
| tutorial/tutorial_e.ehp | 04_message_res.bin | 21 | 1 sostituzione/i | apostrofo del plurale |
| tutorial/tutorial_e.ehp | 04_message_res.bin | 74 | 1 sostituzione/i | apostrofo del plurale |
| tutorial/tutorial_e.ehp | 04_message_res.bin | 154 | 1 sostituzione/i | spazio mancante |

### Correzioni puntuali `ui_texts.json`
| file | membro | indice | vecchio | nuovo | motivo |
|---|---|---|---|---|---|

### Elenco completo
**Confronto completo con parole evidenziate: `docs/changes_en/ui_strings_diff.md`.** Dati grezzi: `docs/changes_en/ui_strings.csv`. Prime 40:

| membro | indice | originale | nuovo |
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

(... altre 17 righe nel CSV)

## A6. Etichetta [CARTA MAGIA] / [CARTA TRAPPOLA] della carta grande nel duello

In tutti i `duel/basic_<regione><lingua>.ehp` l'etichetta era in inglese (hash `c2268340`): `apply_to_iso.py` la sostituisce con `card_spell_trap.gim` di `field/always_<lingua>_<lingua>.ehp` (hash `9622cd75`).

| archivio | membro | hash originale | hash nuovo |
|---|---|---|---|

## A7. File della ISO toccati e dettagli tecnici

182 archivi `.ehp` risultano diversi dall'originale (tutte le lingue insieme, perche' la ISO e' unica; elenco in `docs/changes_en/touched_files.csv`). Gli altri file (video, audio, eseguibile `EBOOT.BIN`, `PARAM.SFO`) sono identici. Differenze tecniche non testuali: `*-ptrs.txt` (offset assoluti dei membri, ricalcolati quando una tabella cambia lunghezza), nuova posizione degli archivi in fondo alla ISO.

## A8. Cosa NON si puo' cambiare (limiti del gioco)

- Il **nome del parlante** nella casella del dialogo (es. "Preside Sheppard"/"Cancelliere" in italiano, "Doyen Sheppard" in francese, "Rector Sheppard" in spagnolo) sta nell'EBOOT cifrato: non modificabile.
- Testi disegnati dal gioco con il suo font (dialoghi, nomi, descrizioni nel deck, menu a tendina, tastiera di sistema, schermata di scelta lingua) non sono sostituibili dal texture pack: si cambiano solo nella ISO.
- Le 438 texture di mappa/sfondi non sono sostituite (il gioco ne cambia la palette): limite del pack di MikeyMK, non del nostro lavoro.

---

# B. TEXTURE PACK

## B1. Provenienza e struttura

Base: **Yu-Gi-Oh! GX Tag Force 1 HD Remastered** di **MikeyMK** (pack USA `ULUS10136`) e carte HD di **chrisfand**, adattati alla ISO europea `ULES00600`. Il progetto non ridistribuisce il pack di terzi (`PERMESSI_AUTORI.md`): il patcher se lo fa dare dall'utente. Il nostro lavoro: (1) rimappare gli **hash** del pack USA su quelli EU (`tools/gen_ini.py`), (2) rifare nella lingua carte e scritte dell'interfaccia, (3) correggere i testi, (4) `upscale_extra` per le texture non coperte.

PPSSPP riconosce una texture dall'**hash dei suoi pixel** (xxhash dei dati, `gim.data_hash`); ogni riga del `textures.ini` e' `0000000000000000<hash8> = percorso/png`. I PNG sono **4x** l'originale e ridisegnano esattamente la stessa area. Texture identiche tra lingue hanno lo stesso hash: la sostituzione vale per tutte (vedi `docs/TEXTURE_INVENTORY.md`).

### Struttura reale (da `docs/changes_en/pack_structure.csv`)
| radice | cartella | file | MB | contenuto |
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
| ULES00600 (pack di base) | ui_it/ | 113 | 9.8 | fogli_icone, fogli_icone.ini, lettere_esito, lettere_esito.ini, menu_liste, menu_liste.ini, schede_deck, schede_deck.ini, schede_ricette, schede_ricette.ini ... |
| ULES00600 (pack di base) | upscale_extra/ | 1192 | 55.8 | 00085186.png, 00162f3c.png, 003fd929.png, 0047e8d4.png, 00b99210.png, 00c5c424.png, 01673953.png, 01692dff.png, 01f7d8fe.png, 01faa502.png ... |
| moduli/en | cards/ | 174 | 30.7 | frame, large_en, small_en |
| moduli/en | en.ini | 1 | 0.0 |  |
| moduli/en | intro/ | 2 | 0.4 | title_screen |
| moduli/en | ui_en/ | 50 | 3.5 | fogli_icone, fogli_icone.ini, lettere_esito, lettere_esito.ini, menu_liste, menu_liste.ini, schede_deck, schede_deck.ini, schede_ricette, schede_ricette.ini ... |

Ogni lingua tranne l'italiano e' un **modulo** (`PSP/TEXTURES/modules/en`) da comporre sopra il pack di base con `tools/compose_pack.py BASE MODULI CARD_DIR OUT en [--copia]`: copia il base e **solo** le cartelle `cards`, `intro` e `ui_en` del modulo (hard link o copia), poi `module_ini.py` riscrive i `textures.ini`: le righe delle carte localizzate puntano a `cards/small_en`/`large_en` e le righe di `en.ini` **sostituiscono** quelle del base con la stessa chiave (hash).

### Cartelle del pack di base (uguali per tutte le lingue)
| cartella | contenuto |
|---|---|
| `cards/small`, `cards/large` | carte piccole/grandi HD originali di chrisfand (2.833 carte) con testi inglesi; la lingua sceglie `small_<l>`/`large_<l>` via ini |
| `cards/frame` | cornici, tabelle attributo/razza, etichette Magia/Trappola |
| `cards/tinyEN/JP/MikeyMK/tiny_<l>` | atlante delle miniature del deck (7 pagine; stesso hash in tutte le lingue: vince un solo atlante per installazione) |
| `characters` | ritratti, sprite e 3D dei personaggi HD (MikeyMK) |
| `events` | immagini degli eventi (17) |
| `intro` | logo, filmato di titolo, nuova partita; `title_screen` contiene le tessere con la targa "Versione Pomodoro Mistico" |
| `map` | sfondi della mappa |
| `shop` | negozio, pacchetti, stanze |
| `ui` | interfaccia HD inglese di MikeyMK (per tutte le lingue con gli stessi hash) |
| `upscale_extra` | texture non coperte dal pack, ingrandite 4x con xBRZ (1.192 file, ~56 MB; a risoluzione 4x/Auto lo shader 4xBRZ di PPSSPP e' spento): include le varianti di `card_icon03` di en/fr/de/es |
| `_SCEGLI LO STILE DELLE CARTE` | 3 `textures.ini` alternativi (mikeymk, official_english, official_japanese): copiare uno al posto di `textures.ini` per cambiare lo stile delle carte |

## B2. Immagini delle carte

Cartelle della lingua: `frame` (0 file), `large_en` (87 file), `small_en` (87 file). Ogni carta ha una **piccola HD** (nome + descrizione + tipo, rigenerata con font liberi OFL: XCharter Bold per nomi/tipo/etichette, Libre Baskerville per gli effetti, Newsreader Italic per i Normali, PT Serif Caption per Magie/Trappole, Charis SIL per i glifi mancanti) e una **grande HD** (solo il nome sulla cornice). In piu': la **tabella degli attributi** con le parole della lingua (`cards/frame/icons_attribute_race_<l>.png`, `attributes.py`), l'**etichetta Magia/Trappola** (`icons_spell_trap_<l>.png`, `label_it.py` / `extract_labels.py` -> `dati/label_eu_<codice>_128x32.png`) e l'**atlante delle miniature** del deck (`tiny_<l>`, `tiny_atlas.py` + `tiny_fragment.py`).

Quando cambia il testo di una carta (sezione A2) vanno rigenerate le sue immagini: **82 carte** nel inglese. Elenco in `docs/changes_en/card_images.csv`. Comando: `python tools/generate_language.py fr PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` (senza ID rigenera tutte: 2.833 + 2.833, ~930 MB).

Tipografia: spazio non separabile prima di `: ; ! ?` e virgolette « ».

## B3. Interfaccia HD in inglese (`ui_en`)

**43 texture** (`docs/changes_en/ui_textures.csv`: file, hash PPSSPP, famiglia, script, dimensioni originale/HD, neutra/specifica, origine nella ISO). Per famiglia: fogli_icone 3, lettere_esito 4, menu_liste 2, schede_deck 14, schede_ricette 11, schermata_vs 3, tutorial 6. Di queste 0 sono neutre (stesso hash in tutte le lingue) e 43 specifiche. Ogni famiglia ha uno script in `tools/ui_textures/<famiglia>.py` (lettura `TF1_LANG`): ridisegna le scritte texture per texture partendo dall'originale a bassa risoluzione della ISO e dallo stile del pack inglese; stessa area e stesse posizioni (il gioco ritaglia da rettangoli fissi); un font/peso/linea di base/ombra per scritta; font liberi (`alt_font.py`).

| famiglia | texture | script | archivio ISO sorgente | testi della lingua |
|---|---|---|---|---|
| fogli_icone | 3 | `tools/ui_textures/icon_sheets.py` | deck/all_e.ehp, shop/all_e.ehp, field/always_* | `icon04` (pixel europei sul foglio USA), `panel` (frammento `ased` della linguetta), `pda_pack01` (colonna NEW) |
| lettere_esito | 4 | `tools/ui_textures/result_letters.py` | duel/basic_ee.ehp | tessere `D R A W` della schermata dei risultati (`result_e`) e del banner (`basic_be`): stesso hash, 4 file |
| menu_liste | 2 | `tools/ui_textures/menu_lists.py` | title_menu/title_menu_e.ehp, duel/result/result_e.ehp, field/always_bri_<cod>.ehp | `result_e__menu01` (WIN/DRAW/LOSE e icone), `title_menu_e__m_menu_title01` (MAIN MENU · ENTER NAME · DOWNLOADED CARD LIST · DUEL PUZZLE · OPTIONS · LANGUAGE SETTINGS) |
| schede_deck | 14 | `tools/ui_textures/deck_screens.py` | deck/all_e.ehp, labo/*.ehp, shop/all_e.ehp | linguette Trunk, Rental, Lab, Converter; `Card types in possession`; `Purchased Cards` / `Card Types Purche`; barra dorata; tasto ENTER |
| schede_ricette | 11 | `tools/ui_textures/recipe_screens.py` | deck/recipe_view_e.ehp, title_menu/title_menu_e.ehp, database/limitlist.ehp | Character, User, Downloaded Recipes, Character Recipes, User Recipes, Limited, Semi-Limited, Forbidden, Trade |
| schermata_vs | 3 | `tools/ui_textures/vs_screen.py` | duel/start/start_e.ehp (membri _e), start_all.ehp, start_e.ehp | `2nd round`, `3rd round`, foglio distintivi `1st PLAYER` / `2nd PLAYER` / `PLAYER` |
| tutorial | 6 | `tools/ui_textures/tutorial.py` | tutorial/tutorial_e.ehp (tuto_duelimg01..06) | dialogo `Your opponent has declared battle. Activate the effect of a card?` (YES/NO) e 5 carte-esempio con il testo del gioco |

Regole di qualita' (valgono per ogni lingua): lettere regolari, mai deformate una per una; stessa area dell'originale; niente sfocature; il testo e' quello dell'originale della lingua (si correggono solo errori evidenti: residui di altre lingue, accenti); pixel art **non** levigata senza conferma; geometrie sempre misurate sull'originale.

### Testi disegnati: originale -> HD
Tabella letta a occhio, texture per texture: `docs/changes_en/texture_texts_en.md`. Nessuna parola cambiata: l'HD riscrive le stesse parole dell'originale inglese (tranne `DOWNLOADED CARD LIST`, che il pack USA ha come `DOWNLOAD`).

### Elenco di ogni texture
(tutte le 43 righe, da `ui_textures.csv`)

| file nel pack | hash | famiglia | originale px | HD px | tipo | origine ISO |
|---|---|---|---|---|---|---|
| ui_en/fogli_icone/all_e__icon04.png | a51fdf03 | fogli_icone | 128x128 | 512x512 | SPECIFICA | deck/all_e.ehp:icon04.gim |
| ui_en/fogli_icone/all_e__panel.png | 4301b477 | fogli_icone | 256x256 | 1024x1024 | SPECIFICA | shop/all_e.ehp:panel.gim |
| ui_en/fogli_icone/always_bri_eng__pda_pack01.png | 180fee24 | fogli_icone | 512x256 | 2048x1024 | SPECIFICA | field/always_bri_eng.ehp:pda_pack01.gim; field/always_bri_fra.ehp:pda_pack01.gim; field/always_bri_spa.ehp:pda_pack01.gim |
| ui_en/lettere_esito/basic_be__duel_draw100002.png | b4fda5d3 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_be.ehp:duel_draw100002.gim; duel/basic_fe.ehp:duel_draw100002.gim; duel/basic_ge.ehp:duel_draw100002.gim |
| ui_en/lettere_esito/basic_be__duel_draw100004.png | 2973446a | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_be.ehp:duel_draw100004.gim; duel/basic_fe.ehp:duel_draw100004.gim; duel/basic_ge.ehp:duel_draw100004.gim |
| ui_en/lettere_esito/basic_be__duel_draw100006.png | 4b73998e | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_be.ehp:duel_draw100006.gim; duel/basic_fe.ehp:duel_draw100006.gim; duel/basic_ge.ehp:duel_draw100006.gim |
| ui_en/lettere_esito/basic_be__duel_draw100008.png | f720182b | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_be.ehp:duel_draw100008.gim; duel/basic_fe.ehp:duel_draw100008.gim; duel/basic_ge.ehp:duel_draw100008.gim |
| ui_en/menu_liste/result_e__menu01.png | b602d300 | menu_liste | 256x64 | 1024x256 | SPECIFICA | duel/result/result_e.ehp:menu01.gim; duel/result/result_j.ehp:menu01.gim |
| ui_en/menu_liste/title_menu_e__m_menu_title01.png | 1d377d3b | menu_liste | 256x128 | 1024x512 | SPECIFICA | title_menu/title_menu_e.ehp:m_menu_title01.gim |
| ui_en/schede_deck/all_e__d_window00008.png | 92c07948 | schede_deck | 128x32 | 512x128 | SPECIFICA | deck/all_e.ehp:d_window00008.gim |
| ui_en/schede_deck/all_e__d_window00033.png | 4400d119 | schede_deck | 256x32 | 1024x128 | SPECIFICA | deck/all_e.ehp:d_window00033.gim |
| ui_en/schede_deck/all_e__d_window00051.png | b7e9dc1a | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_e.ehp:d_window00051.gim |
| ui_en/schede_deck/all_e__d_window00062.png | 61dffec6 | schede_deck | 128x32 | 512x128 | SPECIFICA | deck/all_e.ehp:d_window00062.gim; labo/conv_machine.ehp:window_e0016.gim; title_menu/title_menu_e.ehp:t_window0015.gim |
| ui_en/schede_deck/all_e__d_window00101.png | 082a50da | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_e.ehp:d_window00101.gim; labo/rental.ehp:window_e0008.gim |
| ui_en/schede_deck/all_e__tab_title.png | 80de9436 | schede_deck | 256x32 | 1024x128 | SPECIFICA | shop/all_e.ehp:tab_title.gim |
| ui_en/schede_deck/conv_machine__window_e0009.png | 9c07916c | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/conv_machine.ehp:window_e0009.gim; labo/conv_machine.ehp:window_e0026.gim |
| ui_en/schede_deck/conv_machine__window_e0016.png | 61dffec6 | schede_deck | 128x32 | 512x128 | SPECIFICA | deck/all_e.ehp:d_window00062.gim; labo/conv_machine.ehp:window_e0016.gim; title_menu/title_menu_e.ehp:t_window0015.gim |
| ui_en/schede_deck/conv_machine__window_e0022.png | cad9bed1 | schede_deck | 256x32 | 1024x128 | SPECIFICA | labo/conv_machine.ehp:window_e0022.gim; labo/rental.ehp:window_e0021.gim; title_menu/title_menu_e.ehp:t_window0021.gim |
| ui_en/schede_deck/conv_machine__window_e0026.png | 9c07916c | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/conv_machine.ehp:window_e0009.gim; labo/conv_machine.ehp:window_e0026.gim |
| ui_en/schede_deck/password__key_e0027.png | 80e78a95 | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/password.ehp:key_e0027.gim; labo/password.ehp:key_j0027.gim |
| ui_en/schede_deck/rental__window_e0008.png | 082a50da | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_e.ehp:d_window00101.gim; labo/rental.ehp:window_e0008.gim |
| ui_en/schede_deck/rental__window_e0015.png | 93c88910 | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/rental.ehp:window_e0015.gim |
| ui_en/schede_deck/rental__window_e0026.png | 4fa2b5e3 | schede_deck | 64x32 | 256x128 | SPECIFICA | labo/rental.ehp:window_e0026.gim |
| ui_en/schede_ricette/limitlist__window_e0002.png | c1e2ff0d | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_e0002.gim |
| ui_en/schede_ricette/limitlist__window_e0004.png | 6f593093 | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_e0004.gim |
| ui_en/schede_ricette/limitlist__window_e0012.png | 5e3bc044 | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_e0012.gim |
| ui_en/schede_ricette/recipe_view_e__recipe010008.png | 72966f8d | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_e.ehp:recipe010008.gim; title_menu/title_menu_e.ehp:recipe_sel00002.gim |
| ui_en/schede_ricette/recipe_view_e__recipe010015.png | 4efbece8 | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_e.ehp:recipe010015.gim; title_menu/title_menu_e.ehp:recipe_sel00009.gim |
| ui_en/schede_ricette/recipe_view_e__recipe010027.png | 4d84d0c5 | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_e.ehp:recipe010027.gim; title_menu/title_menu_e.ehp:recipe_sel00020.gim |
| ui_en/schede_ricette/recipe_view_e__recipe010029.png | e2538eef | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_e.ehp:recipe010029.gim; title_menu/title_menu_e.ehp:recipe_sel00022.gim |
| ui_en/schede_ricette/recipe_view_e__recipe010031.png | 6ca29a28 | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_e.ehp:recipe010031.gim; title_menu/title_menu_e.ehp:recipe_sel00024.gim |
| ui_en/schede_ricette/title_menu_e__recipe_sel00033.png | 96fe0ef6 | schede_ricette | 128x32 | 512x128 | SPECIFICA | title_menu/title_menu_e.ehp:recipe_sel00033.gim |
| ui_en/schede_ricette/title_menu_e__t_window0008.png | 05ec86c0 | schede_ricette | 64x32 | 256x128 | SPECIFICA | title_menu/title_menu_e.ehp:t_window0008.gim |
| ui_en/schede_ricette/title_menu_e__t_window0026.png | 45902d92 | schede_ricette | 64x32 | 256x128 | SPECIFICA | title_menu/title_menu_e.ehp:t_window0026.gim |
| ui_en/schermata_vs/start_e__d_menu01_e.png | 905aa050 | schermata_vs | 256x256 | 1024x1024 | SPECIFICA | duel/start/start_e.ehp:d_menu01_e.gim; duel/start/start_f.ehp:d_menu01_e.gim; duel/start/start_g.ehp:d_menu01_e.gim |
| ui_en/schermata_vs/start_e__vs_much2_e0001.png | 7b22a421 | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much2_e0001.gim; duel/start/start_e.ehp:vs_much2_e0001.gim; duel/start/start_f.ehp:vs_much2_e0001.gim |
| ui_en/schermata_vs/start_e__vs_much3_e0001.png | e71966a5 | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much3_e0001.gim; duel/start/start_e.ehp:vs_much3_e0001.gim; duel/start/start_f.ehp:vs_much3_e0001.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg01.png | 5fb78e9f | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_e.ehp:tuto_duelimg01.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg02.png | 0a1af418 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_e.ehp:tuto_duelimg02.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg03.png | 57602964 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_e.ehp:tuto_duelimg03.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg04.png | fa80718b | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_e.ehp:tuto_duelimg04.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg05.png | 7fe0878d | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_e.ehp:tuto_duelimg05.gim |
| ui_en/tutorial/tutorial_e__tuto_duelimg06.png | 7bbf6d19 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_e.ehp:tuto_duelimg06.gim |

### Texture inglesi che restano com'erano
Le texture inglesi gia' coperte dal pack USA (stesso hash: 621) vengono da MikeyMK e non si toccano. Restano **ingrandite con xBRZ** (`upscale_extra`) o senza file (14, frammenti senza testo: si vedono come l'originale) le texture senza testo o comuni a tutte le lingue (le 4 tessere DRAW della schermata dei risultati sono ridisegnate in `lettere_esito`). 17 texture del pack italiano hanno lo stesso hash di quelle inglesi (`ITA-SU-ING`): controllate una a una, sono senza testo. Elenco completo: `docs/changes_en/texture_inventory_en.txt`.

## B4. Il foglio dei numeri del duello (`card_icon03`)

Foglio unico con cifre LP, tempo, tasti e moltiplicatori; hash diverso per lingua. Ricetta scelta dall'utente (`tools/ui_textures/icon03_languages.py`, rilanciare con `--apply`):
- righe 0-180 (cifre piccole e segni, tasti arancioni 1/2/3, cifre grandi 0-9 con "LP", cifre piccole 0-9): **dal pack USA**, pixel art netta;
- celle in cui il gioco europeo differisce dal pack USA (spunta nera, palla grigia, pillola vuota, parola del tempo): **pixel originali ingranditi 4x senza sfumare**; parola del tempo **TIME**; la pillola arancione ("Single" nel pack USA) resta **vuota**;
- righe >= 181 (moltiplicatori x1..x12, icone, carte, frecce): dal foglio italiano gia' nel pack (`tools/data/card_icon03_base_it.png`);
- le celle europee si incollano **solo nella loro fascia** di righe (altrimenti rovinano la parte alta delle cifre grandi).

File: it -> `ui_it/scritte_duello/basic_ii__card_icon03.png` (hash 376925c7); fr -> `upscale_extra/3e5482fd.png`; en ee0c44c3; de ffe309a6; es 859eea2b. Anteprime in `confronti/icon03/`.

## B5. Targa del titolo

`python tools/ui_textures/mystic_tomato_title.py en` genera 2 PNG (`542eff79685c434d`, `705176739829dcf5`, tessere 18 e 19 del fondale di 20 tessere 128x64 `title_menu_i.ehp: main_title00001..00020`) con la carta 4930 nella lingua + la formula "versione" + la bandiera, font PT Sans Bold: **"VERSION MYSTIC TOMATO"**. La targa **va inclusa solo per la lingua scelta** (vive in `moduli/en/intro/title_screen/`); il pack di base originale ha le tessere senza banner. File in questo pack: `moduli/en/intro/title_screen/00000000542eff79685c434d.png`, `moduli/en/intro/title_screen/00000000705176739829dcf5.png`.

## B6. `textures.ini` e composizione

`tools/gen_ini.py TOOLS US_INI CARD_DIR OUT_INI i=it +extra_it.ini +ui_it.ini +dati/upscale_extra.ini` converte il `textures.ini` USA in quello EU: le voci non-carta restano (texture neutre = stessi hash); le voci carta sono rigenerate dagli archivi `card/*.cip` EU per le 5 lingue (`i=it` rimappa `cards/large/X.png` -> `cards/large_it/X.png`); aggiunge l'etichetta Magia/Trappola (`extra_it.ini`), le righe `ui_it` e `upscale_extra.ini`. Si fa anche per i 3 stili carte. Se gli stessi pixel esistono in piu' lingue vince la prima in `e i f g s` (per questo atlante, banner e tabella attributi sono "uno per installazione").

Righe `ui_en` nel `en.ini`: 43. Frequenza dei prefissi: `docs/changes_en/ini_lines.csv`. Controllo: ogni riga `ui_en/...` deve puntare a un file esistente e non devono esserci hash duplicati.

## B7. Installazione e impostazioni

PC: copiare `ULES00600` in `<PPSSPP>/PSP/TEXTURES/` (Android: `textures.zip` in `.../TEXTURES/ULES00600/`, senza estrarlo; rigenerare lo zip con le correzioni). Impostazioni: **Sostituisci texture ON**, risoluzione di rendering **4x**, lingua del gioco = lingua del modulo (la lingua e' scritta nel **salvataggio**). Dopo aver cambiato un solo PNG basta copiarlo e riavviare PPSSPP (cache). Per provare i testi usare la ISO `_definitiva`.

---

# C. SCELTE EDITORIALI

- **Solo errori oggettivi** dell'inglese europeo: refusi (`Sryus`, `Principle's`, `Bandanna`), articoli (`a Equip Spell` -> `an Equip Spell`, `face-down card` -> `a face-down card`), apostrofi (`monsters's`, `opponents cards`), concordanze, forme verbali dei tutorial (`"Summon" it` -> `"Summoning" it`), spazi e `$` di troppo nei codici colore. Nessuna riscrittura di stile.
- `Chancellor Sheppard` nelle schede, come nei dialoghi; `Bandana` come nei dialoghi.
- Termini di carte e testi lasciati come nel gioco; le 82 carte corrette hanno il testo rigenerato nelle immagini HD (`moduli/en/cards`).
- La targa del titolo inglese e' `VERSION MYSTIC TOMATO` (confermato dall'utente il 2026-10-13).
- Foglio numeri: cifre/LP dal pack USA, x1..x12 dal foglio italiano, parola del tempo TIME.

### Voci del registro delle scelte per questa lingua (`tools/data/editorial_choices.json`)
| id | originale | corretto | ereditata | motivo |
|---|---|---|---|---|
| st01_t01/Scr003E#146 | My father owns a hot sauce⏎company. | My father owns a sake⏎brewery. | no | sake al posto di salsa piccante (fedele al giapponese: la famiglia di Chumley fa sake) |
| st01_t01/Scr003E#147 | He sent me some hot sauce with my⏎last allowance.⏎I'll give ya a reasonable discount.⏎Do you wanna... | He sent me some shochu with my⏎last allowance.⏎I'll give ya a reasonable discount.⏎Do you wanna... | no | shochu al posto di salsa piccante |
| st01_t01/Scr003E#150 | My father owns a hot sauce⏎company. | My father owns a sake⏎brewery. | no | come 146 |
| st01_t01/Scr003E#151 | He sent me some hot sauce⏎with my last allowance.⏎I'll give ya a reasonable discount.⏎Do you wanna... | He sent me some shochu⏎with my last allowance.⏎I'll give ya a reasonable discount.⏎Do you wanna... | no | come 147 |
| st01_t01/Scr003E#163 | Wow. You really did it.⏎It's 《C026_2》...⏎Wearing a bikini! | Wow. You really did it.⏎It's 《C026_2》...⏎Wearing a maid outfit! | no | abito da cameriera al posto di bikini (giapponese: メイド服) |
| st01_t01/Scr003E#168 | Wow. You really did it.⏎It's 《C026_2》...⏎Wearing a bikini! | Wow. You really did it.⏎It's 《C026_2》...⏎Wearing a maid outfit! | no | come 163 |
| st01_t01/Scr003E#188 | Well, I suppose I dabble a little... | None | si | solo italiano: "sto sbavando" era un errore di traduzione (giapponese: "non sono poi così bravo") |
| st01_t01/Scr003E#189 | Hey, can you draw a picture for me then?⏎Draw me 《C026_2》 in a bikini! | Hey, can you draw a picture for me then?⏎Draw me 《C026_2》 in a maid outfit! | no | abito da cameriera al posto di bikini |
| st01_t01/Scr003E#191 | Here, you can use this! | Here, use this maid outfit! | no | Syrus passa un abito da cameriera come modello (メイド服): col bikini la battuta non aveva senso |
| st01_t01/Scr003E#194 | Well, I suppose I dabble a little... | None | si | come 188 |
| st01_t01/Scr003E#195 | Hey, can you draw a picture for me then?⏎Draw me 《C026_2》 in a bikini! | Hey, can you draw a picture for me then?⏎Draw me 《C026_2》 in a maid outfit! | no | come 189 |
| st01_t01/Scr003E#197 | Here, you can use this! | Here, use this maid outfit! | no | come 191 |

Altre scelte e la rilettura delle frasi dei duelli: `docs/EDITORIAL_CHOICES.md`.

# D. VERIFICA IN GIOCO

- **Non visto in gioco**: la ISO `_definitiva` e il pack inglese composto non sono ancora stati provati in PPSSPP. Controllati solo sui dati: `apply_to_iso.py` a 0 avvisi, ogni riga `ui_en` del `textures.ini` punta a un file esistente, confronti originale/HD in `docs/changes_en/sheets/` (originale 4x accanto all'HD, riletti a occhio).
- Da vedere in gioco: carta con testo nuovo, dialoghi corretti, aiuti dell'editor, linguette Trunk/Rental/Lab/Converter, `Purchased Cards`, `2nd/3rd round`, distintivi `1st/2nd PLAYER`, `MAIN MENU` e voci del menu, tutorial del duello.

# E. COME RIGENERARE TUTTO

```
# ISO (tutte le lingue insieme)
python tools/corrections/build_dialogues.py en
python tools/corrections/generate_card_corrections.py en CARDINFO_en.ehp          # carte
python tools/corrections/apply_to_iso.py PSP/GAME/ULES00600_..._EUR.iso PSP/GAME/ULES00600_..._EUR_definitiva.iso
# immagini
python tools/generate_language.py fr PACK CARDINFO US_INI CLEAN_DIR OUT [ID...]
TF1_LANG=en python tools/ui_textures/<famiglia>.py USRDIR PACK_US <modulo>      # per ognuna delle 8 famiglie (intera!)
python tools/ui_textures/icon03_languages.py --apply ; python tools/ui_textures/mystic_tomato_title.py en
python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules USRDIR/card OUT en --copia
# questo documento
python tools/analysis/document_changes.py ISO_ORIG ISO_DEF en docs/changes_en
python tools/analysis/document_pack.py ISO_ORIG en docs/changes_en
python tools/analysis/text_comparisons.py en
python tools/analysis/write_changes_document.py en
```
Input esterni da avere (controlla che esistano): ISO originale, USRDIR estratta (`tools/analysis/extract_usrdir.py`), pack USA di MikeyMK `ULUS10136` (in una cartella fuori dal progetto).

# F. LIMITI E PUNTI APERTI

- **Decisioni dell'utente (2026-10-13)**: nome del logo `VERSION MYSTIC TOMATO` confermato; tessere DRAW da ridisegnare (fatto); (1) nome del logo confermato; (2) `DOWNLOADED CARD LIST` (europeo) contro `DOWNLOAD` (testo USA): scelto l'europeo, confermato dall'utente.
- `textures.zip` Android per l'inglese: non fatto; nessuna prova su telefono.
- I testi disegnati nelle texture sono in `docs/changes_en/texture_texts_en.md` (letti a occhio).
- Il nome del parlante nella casella del dialogo non e' modificabile (EBOOT cifrato).
