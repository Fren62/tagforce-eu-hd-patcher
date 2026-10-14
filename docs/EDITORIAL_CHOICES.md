# Register of editorial choices

General method for a new language: `docs/NEW_LANGUAGE_GUIDE.md`. This file collects the **decisions taken with the user** that hold for the game (not just for one session), so that the
language-specific patchers apply the right correction of their own language. Every entry says where the data lives, so that the patcher
does not have to derive it again from the code.

Where the corrections live (all read by `tools/corrections/apply_to_iso.py`):

| What | Per-language data | Build |
|---|---|---|
| Dialogues | `tools/data/dialogue_touchups_<l>.json` (`exact`, `parts`) + for Italian the base `dialogue_corrections_it_base.json` | `build_dialogues.py <l>` -> `dialogue_corrections_<l>.json` |
| Long interface strings (help, cards, tutorial) | `tools/corrections/string_rules_<l>.py` | `ui_strings.py` (done: all five languages) |
| Cards | `tools/corrections/rules_<l>.py` | `generate_card_corrections.py` |
| Choices common to all languages (this register) | `tools/data/editorial_choices.json` | documentation/check only: the corrections are already in the data above |

Rule for new choices: write them **both** in the language's data **and** here, with id, original text, corrected text, reason.

## Choices common to all languages

### Syrus + Chumley scene (`st01_t01/Scr003E`, lines #146-#197): sake and maid outfit
Faithful to the Japanese; the European versions had censorship/changes (hot sauce, bikini).
- Chumley's family: **sake distillery**; the gift is **shochu** (not hot sauce). Lines #146, #147 and copies #150, #151.
- Syrus asks Chumley for the drawing of the **Dark Magician Girl (C026) in a maid outfit** (not in a bikini), lines #163, #168, #189, #195.
- Line #191/#197: Syrus hands over a **maid outfit** as a model ("Here, use this ...").
- Italian only: lines #188/#194 "Beh, non sono poi così bravo..." (before "sto sbavando", a translation error).
- No texture has maid/bikini/sake/sauce variants (checked 53 busts, 23 event images, SD sprites, help images).
- Line-by-line and per-language detail: `tools/data/editorial_choices.json` (it, en, fr, de, es). Copies without their own corrected text
  (`inherited: true`) take the correction from the line with the same text and the same Japanese (as `dialogues.py` does).

| Language | Family | Gift | Outfit |
|---|---|---|---|
| it | "La mia famiglia produce sake." | "dello shochu" | "In abito da cameriera!" / "vestita da cameriera!" |
| en | "a sake brewery" | "some shochu" | "Wearing a maid outfit!" / "in a maid outfit!" |
| fr | "une distillerie de saké" | "du shochu" | "En tenue de servante !" / "en tenue de servante !" |
| de | "eine Sake-Brauerei" | "etwas Shochu" | "Im Dienstmädchen-Outfit!" |
| es | "destilería de sake" | "un poco de shochu" | "¡Y va vestida de criada!" / "vestida de criada" |

New languages (or separate patchers): use the same idea (sake distillery, shochu, maid outfit) in their own wording.

### Menu names verified in game
- Italian: main menu `Modalità Storia` (dialogues 1625/7603 quote it that way).
- French: `Mode aventure`.

### Known limit: speaker name
The name in the dialogue box (e.g. "Doyen Sheppard") lives in the executable (encrypted EBOOT): it cannot be modified. It holds for all languages.

## Duel sentences (complete re-reading, 2026-10-11)
All the unique sentences were read (it 1,792, fr 1,832) against English. Data: `tools/data/duel_line_corrections_<l>.json`. List for the re-reading: `tools/audit/extract_duel_lines.py`.
- it: missing final full stop in the twin sentences ("Attivo una Magia Continua", "...Magia Terreno", "...Evocazione Rituale", "Sto attivando una Trappola Continua", "È il mio turno"); "duellare non è solo una questione"; "ti rispetterò"; "una l'effetto"; "io SO"; "perché hai perso?"; "Fa' pure!"; "pescare una carta".
- fr: "Tu es mignon." / "Tu n'es pas très mignon." (it was "malin"/"gentil" for *cute*); "Hein ?" instead of "Huh ?"; "Mon Dieu"; "J'offre"; "Juste une blessure légère"; "Position d'Attaque" with capitals; missing "!" in "J'invoque l'Assaillant des Protecteurs du Tombeau".
- Left as they were (intended): "pidgin" sentences of certain characters, sound effects, English move names ("Train Twister"). In French "Carte Piège Continu" is the term consistent across the whole game: it is not changed.
- New languages: same re-reading; correct the equivalent of these classes of error.

Complete list of neutral/specific textures: `docs/TEXTURE_INVENTORY.md`.

## "Italian-only" textures (classification, 2026-10-11)
Of the 19 textures in `ui_it` without a counterpart in `ui_fr`: **13 are neutral** (same hash in all languages: recipe panels, Side/Deck/Fusion Deck tabs, bars, `card_side`, flags...: the module of every language already receives them)
and **6 have local wording in the original** (`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `d_window00016`, `duelrecord parts`): Italian has `NUOVO`/`N`/`Fusione`, the original French has `NEW`/`Fusion` and already has its HD ones in `upscale_extra`.
Choice: French **stays like the original** (`NEW`). Optional variant to propose to the user for fr/de/es: `N` as the initial icon (Nouveau/Neu/Nuevo).

## Italian
- **Deck editor tab: `Fusion`** (not `Fusione`): "Fusion Deck" is the name in all languages (like Side Deck, Deck). Texture `ui_it/deck_screens/all_i__d_window00016.png`, generated by `deck_screens.py`.
- **Sheppard is always "Preside"** (never "Cancelliere"): dialogues (`dialogue_touchups_it.json`: `Cancelliere`/`cancelliere` -> `Preside`/`preside`, including
  "Ufficio del Preside" and Crowler's joke "Preside Crowler... Preside Crowler provvisorio") and interface ("Profilo del Preside Sheppard").
- **Tokens are called "Segna-Mostro"** (not "Gettoni"): editor and duel help, duel records ("Segna-Mostro Evocati"). In the card texts neither "Gettone" nor "Segna" appears.
- Banner: "direttore dello Slifer Rosso" (not "presidente").
- Dormitories everywhere: **Slifer Rosso, Ra Giallo, Obelisk Blu**.
- **Cards**: read one by one (2,479 texts). Objective errors (Life Point->Points, E'->È, Annello->Anello, agreement, spaces, capitals) in `tools/corrections/rules_it.py`; `generate_card_corrections.py it CARDINFO` merges them into `tools/data/card_corrections.json` (181 cards). Not changed: official names, the game's terminology.
- Rules in `dialogue_touchups_it.json` (about 150 `parts`) and `string_rules_it.py`.

## French
- **Doyen / Chancelier** dialogue by dialogue: formal -> "Chancelier", informal -> "Doyen"; in the UI cards "Chancelier Sheppard".
- French punctuation `! ? : ;` with a space (also after `》`): rule `FR_PUNCT` in `build_dialogues.py`.
- "Mode histoire" in the dialogues -> "Mode aventure" (real name of the menu).

## German
See the section "German: choices of the re-reading" further below.

## English (European, 2026-10-13)
- Only objective errors (typos, articles and agreement, apostrophes, `Sryus`->`Syrus`, `Principle's`->`Chancellor`, `Bandanna`->`Bandana`): cards 82, dialogues 402 lines (79 parts, 5 regexes, 2 exact), duel sentences 3 exact + 6 parts, UI strings ~70 (`string_rules_en.py`). No stylistic rewriting.
- `ocg_packname_e.bin` does not exist in the English game: the OG table was removed.
- Textures: the US pack (MikeyMK) already covers 621 of the 917 English textures (same hash). The 39 that the US pack does not cover (different European hash) and that only had xBRZ: redrawn in HD with the `ui_textures` scripts (`TF1_LANG=en`) in `modules/en/ui_en` (deck_screens 14, recipe_screens 11, tutorial 6, icon_sheets 3, vs_screen 3, menu_lists 2). Same words as the original. Also redrawn the 4 DRAW tiles (`result_letters`, user's request 2026-10-13); logo name `VERSION MYSTIC TOMATO` and `DOWNLOADED CARD LIST` confirmed by the user. 17 ITA-ON-ENG textures checked: neutral. List in `docs/changes_en/texture_inventory_en.txt`, texts in `texture_texts_en.md`.
- Card images: 82 corrected cards regenerated in `modules/en/cards` (small_en/large_en).

## Spanish (2026-10-11/12)
Data: `rules_es.py` (cards, 341 corrected), `dialogue_touchups_es.json` (119 `parts`, 2 `exact`), `duel_line_corrections_es.json`, `string_rules_es.py`. Complete lists in `docs/CHANGES_ES.md`. Questions still open: `docs/changes_es/open_questions_es.md`.
- **Dormitories and groups** as in the dialogues/cards: **Slifer Rojo, Ra Amarillo, Obelisco Azul** (they were `Slifer Red`, `Ra Yellow`, `Obelisk Blue` in dialogues and cards), **Jinetes de la Sombra** (`Shadow Riders`), **Duelista de la Sombra**, `Archidemonio`, `Trío Ojama`, `Sirviente de la Calavera`, `Toon` (the cards do not use "Cómico/Animado").
- **Rector Sheppard**: `Oficina del Rector` (map), `Perfil del Rector Sheppard` (it was "Perfil de Sheppard del Principio"). In the dialogues the leftover Italian names were translated (`Velo della Notte`->`Velo de la Noche`, `Dante Fiammeggiante`->`Dante Ardiente`, `Padrone Seydina`->`Maestro Seydina`).
- **Places**: `Alójese 101..204` -> `Habitación 101..204` (English: Room), `Cliff` -> `Acantilado`, `Dorm abandonado` -> `Dormitorio abandonado`.
- **Common scenes**: sake/shochu and maid outfit (`st01_t01/Scr003E`) and `st02_t01/Scr101E` as in the other languages; the 4-5-line dialogue lines were brought back to 3 (`Scr005E#420`, `Scr007E#23`, `Scr063E#6`, `Scr003E#147/#151`).
- **Options**: "EN/FUERADE" -> `ON`/`OFF` (as in English); `Rindes` -> `Rendirse`; `Trar`/`Tirar bocadillo` -> `Comer` (English says Eat).
- **Editor terms**: `Refinar Búsqueda` -> `Filtrar` (as the menu); `Efecto de Disparado de Múltiple` -> `Efecto de Disparo Múltiple`; `Contador Mágico` -> `Contadores Mágicos`; `Invocación por Fusión/Ritual/Volteo` -> `Invocación de ...` (as the cards). Left: `Invocación por Sacrificio`, `Tributar`, `Efecto de Blanco`, `Tronco`.
- **Missing/broken texts translated from English**: final paragraph of the Tag Duel help (it was truncated in `deck/all_s` and in English in `basic_bs`); "10 lanzamientos de moneda" (it was 100); "usando efectos" (record 130); "Nivel 4 o inferior" (record 179); "Semi-Limitada" (message 135).
- **Tutorial lessons** (`tutorial_s.ehp`, 4 files): "le turno" -> "es el turno de", swapped × and ○ keys in the "End Phase" step, closed color codes, "Antes, Syrus ha preguntado" (it was Bastion), "Hechizo de Campo" -> "Carta Mágica de Campo".
- **Duel sentences**: `¿Cómo ha podido ocurrir esto…?`, `¿Qué…?`, "No tienes ni idea de lo que estás haciendo", "¡Yo no bajaré la guardia!" (the no was missing).
- **Textures**: texts of the original reproduced (no word changes): `TURNO DEL SIGUIENTE JUGADOR`, `COMENZAR DUELO`, `Ataque Directo`, `HAS GANADO/HAS PERDIDO/EMPATE`, `1ra/2da/3ra vuelta`, `AM/PM` (instead of Morning/Afternoon) and `de` in the calendar. `TURNO` has the same hash as Italian.
- **User decisions (2026-10-12)**: `Kaiba Corporation` stays (English says Umiuma); "duelo" made uniform to **Duelo/Duelos** in the dialogues (as the rest of the game); **Rector** (not Canciller) because it is the closest to "Preside"; **Sacrificio** (not Tributo): `Invocación por Sacrificio`, as in the official Spanish texts; `Efecto de Blanco` (= targeting effect) left; `NEW` stays in English as in the original.
- **Card names = official Spanish name of Yugipedia (2026-10-12, user's choice: even where the game translated differently)**: 294 names in `tools/data/official_names_es.json` (before/after in `docs/changes_es/official_names_es.tsv`), quotations of the names in quotation marks follow the change (cards, UI strings, duel sentences). Exceptions where Yugipedia has typos or the data is missing: `Dian Keto, el Señor`, `recaudación`, `Resurrección`, `Anfibio/Anfibia`, correct accents of the game (Búho, Cañón, Más Allá, Trío), 4130 `Herramienta Antigua`, 4644 `Reina de las Hojas de Otoño` (not official: like the French). Official archetypes in capitals (HÉROE, RANA) left as Yugipedia has them.
- **`Efecto de Blanco` -> `Efectos con Objetivo`**: the official texts say `selecciona 1 monstruo ... ese objetivo`; Yugipedia translates Target as `Objetivo`. `blanco` -> `objetivo` in all the interface explanations and on cards 5179/5187. I did not find an official label for the category: the choice is mine.

## Common textures: duel number sheet (`card_icon03`)
User's choice: digits 0-9, LP, keys and small signs **from the US pack** (crisp pixel art); multipliers ×1…×12 and icons below **as in the Italian sheet**; only the time word changes (TEMPO, TEMPS, TIME, ZEIT, TIEMPO). Recipe and script: `tools/ui_textures/icon03_languages.py`. Whoever makes the patcher of a new language must use the same sheet and change only the word.

## German: choices of the re-reading (2026-10-12)
Data: `comparisons/audit_de/touchups_nuovi.py` (dialogues), `ritocchi_stringhe.py` (UI), `tools/data/duel_line_corrections_de.json`; list in `docs/changes_de/` and questions in `open_questions_de.md`.
- Places without an article like the other map names: "Büro des Kanzlers" (dialogue "Verlasse das 《M006_2》"), "Duellakademie" (fem.: "Duellant der Duellakademie"); Bibliothek, Dach, Ruinen were missing (mapname 20, 21, 25), "Cliff" -> Klippe, "Verließ Dorm" -> Verlassener Schlafsaal.
- "Spielzug" always capitalized and masculine ("in diesem Spielzug", "am Zug"); tutorial: swapped ×/○ keys fixed, "Fallenkarten können verwendet werden, wenn" (wrong negation), "Einsturz" -> Schrumpfen, "Gegnerrunde" -> "Zug des Gegners", hyphenation hyphens left mid-line removed.
- Menu: "Duel/Talk" in the dialogue -> "Duell/Reden" (as the field menu); Barett -> Haarspange.
- Textures: "Tauschen" instead of the French leftover "ÉCHANGE"; "Fusionsdeck" (recipe010004); tabs Truhe/Miete/Labor/Konverter/Fusion in HD.
- Duel textures (2026-10-13): texts of the original reproduced, no word changes: `DU GEWINNST`, `DU VERLIERST`, `UNENTSCHIEDEN`, `Ketten`, `Direkter Angriff!`, `NÄCHSTER SPIELER` (the A stays without dots in the banner texture: they are a separate sprite), `DUELL BEGINNEN`, `SPIELZUG`.
