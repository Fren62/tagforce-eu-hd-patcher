# CHANGES OF THE MYSTIC TOMATO VERSION FOR ITALIAN

**Complete** document of everything the "Mystic Tomato Version" changes for italian: (A) the **direct changes to the ISO**, (B) the **texture pack** (how it is made, what it contains, how it is composed), (C) the editorial choices, (D) what has been verified in game and what has not, (E) how to regenerate everything.

**This file is generated** by `tools/analysis/write_changes_document.py it` from the real data: byte-by-byte comparison between the original ISO `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` and the corrected ISO `..._definitiva.iso` (`document_changes.py`) and a scan of the pack (`document_pack.py`). The row-by-row lists are in `docs/changes_it/*.csv` (`;` separator, UTF-8 with BOM, line breaks as `⏎`): they are the **exact list** of every change. Regenerate everything after each modification.

For the general method and for the other languages: `docs/NEW_LANGUAGE_GUIDE.md`; technical details of the scripts: `docs/TUTORIAL.md`; decisions: `docs/EDITORIAL_CHOICES.md`; neutral/specific textures: `docs/TEXTURE_INVENTORY.md`.

## Index
- A. Changes to the ISO: A1 overview · A2 cards · A3 dialogues · A4 duel sentences · A5 interface strings · A6 Spell/Trap label · A7 touched files and technical details · A8 what cannot be changed
- B. Texture pack: B1 origin and structure · B2 card images · B3 HD interface (`ui_it`) · B4 number sheet (`card_icon03`) · B5 title plate · B6 textures.ini and composition · B7 installation
- C. Editorial choices · D. In-game verification · E. How to regenerate · F. Limits and open points

---

# A. CHANGES TO THE ISO

## A1. Overview

The original ISO is **never modified**. `tools/corrections/apply_to_iso.py ISO_ORIG ISO_OUT [languages]` creates a copy in which some `.ehp` archives are rewritten. If an archive grows (longer text) it is **put again at the end of the ISO** in a new sector and its entry in the ISO9660 directory is reassigned (`pycdlib`); for this reason the `_definitiva` ISO weighs ~909 MB (the original ~761 MB). **Always run it without a list of languages (or with all of them)**: with a single language it overwrites the others.

| What | Quantity (derived from the ISO comparison) | Where the data lives | CSV file |
|---|---|---|---|
| Cards with changed text (name and/or description) | 181 cards (182 fields) | `tools/data/card_corrections.json` from `tools/corrections/rules_it.py` | cards.csv |
| Story dialogue lines | 2488 lines | `tools/data/dialogue_touchups_it.json` (+ base) | dialogues.csv |
| Duelist sentences in duels | 33 unique sentences (70 entries in all the archives) | `tools/data/duel_line_corrections_it.json` | duel_lines.csv |
| Interface strings (help, cards, records, tutorial, menus...) | 298 unique strings (571 entries, 46 archives) | `tools/corrections/string_rules_it.py` + `tools/data/ui_texts.json` | ui_strings.csv |
| Images replaced inside the ISO | 6 ([SPELL CARD/TRAP CARD] label of the large card) | `apply_to_iso.py` (copies the language's `card_spell_trap.gim`) | iso_images.csv |
| ISO files touched (`.ehp` archives) | 142 | - | touched_files.csv |
| Other technical differences (recomputed offsets) | 90 | - | other.csv |

## A2. Card texts

Archive: `PSP_GAME/USRDIR/duelsys/cardinfo_ita.ehp` (tables `CARD_Name_*`, `CARD_Desc_*`, `CARD_Indx_*`). **181 cards** have a modified name and/or description. Only **objective errors** are corrected (typos, accents, apostrophes, spaces, inconsistent capitalization, agreement, fixed plurals, leftovers from other languages); official names and the game's terminology are not touched.

How: every card was read (it: 2,479 texts, one by one; fr: audit against the official database + reading). Rules in `tools/corrections/rules_it.py`: **44 global rules** (regexes applied to the names and descriptions of all the cards) and **7 per-card corrections** (`PER_CARD`: id, field, old, new, reason; the old text must exist exactly). `generate_card_corrections.py it CARDINFO` (merges the result into the existing `card_corrections.json`, idempotent) produces the json; `apply_to_iso` writes it into the ISO; the HD images of the touched cards are regenerated (section B2).

### Global rules (all)
| pattern (regex) | replacement | reason |
|---|---|---|
| \bLife Point\b | Life Points | plural of Life Points (elsewhere always Life Points) |
| \bAnnello\b | Anello | typo |
| \bavvesario\b | avversario | typo |
| \bin seguita\b | in seguito | typo |
| \bdopo di chè\b | dopo di che | wrong accent |
| \bquesto carta\b | questa carta | agreement |
| \bUn immagine\b | Un'immagine | missing apostrophe |
| \bE' composto\b | È composto | accent |
| \bpuo\b | può | missing accent |
| \bne dichiarare\b | né dichiarare | missing accent |
| \bMain phase\b | Main Phase | inconsistent capitalization |
| \bdella Damage Step\b | del Damage Step | gender: il Damage Step |
| \b[Tt]ipo-(Demone\|Fata\|Guerriero)\b | Tipo \1 | extra hyphen |
| \btipo Pyro\b | Tipo Pyro | inconsistent capitalization |
| \bSegna Opzione\b | Segna-Opzione | name of the Monster Token |
| \bTramite Evocazione\b | tramite Evocazione | wrong capital letter |
| \bevocata tramite\b | Evocata tramite | inconsistent capitalization (Evocata) |
| \bX (\d+) punti\b | x \1 punti | multiplier (elsewhere x) |
| \bX (\d+)\b | x \1 | multiplier (elsewhere x) |
| \bMagia,Trappola\b | Magia, Trappola | missing space |
| Cimitero,eccetto | Cimitero, eccetto | missing space |
| \bsolo I Mostri\b | solo i Mostri | wrong capital letter |
| \baumenta I tuoi\b | aumenta i tuoi | wrong capital letter |
| \bRimuovi da gioco\b | Rimuovi dal gioco | missing article |
| \bCarte Magie e Trappola\b | Carte Magia e Trappola | Magia is invariable |
| Trappola , | Trappola, | space before the comma |
| Magia : | Magia: | space before the colon |
| Trappola : | Trappola: | space before the colon |
| Effetto Mostro : | Effetto Mostro: | space before the colon |
| \bsi aggiudica il Partita\b | si aggiudica la Partita | gender |
| \bvengono cambiata in\b | vengono cambiati in | agreement |
| \bquante possibile\b | quante possibili | agreement |
| \bsi sono 3\b | ci sono 3 | typo |
| \bdi questa carte\b | di questa carta | typo |
| \bpuoi scegli\b | puoi scegliere | verb form |
| \bcome tributo\b | come Tributo | inconsistent capitalization (Tributo) |
| \binferiore del DEF\b | inferiore al DEF | preposition |
| \bHa un indole\b | Ha un'indole | missing apostrophe |
| \bsul tuo terreno\b | sul tuo Terreno | inconsistent capitalization (Terreno) |
| (?<![A-Za-zÀ-ÿ])E' (?=[a-zà-ÿ]) | È  | accent: E' -> È |
| L' (?=[\"A-ZÀ-Þ]) | L' | space after the apostrophe |
| " ," | ", " | space after the comma |
| \(Mostro,Magia | (Mostro, Magia | space after the comma |
| battaglia\.Distruggi | battaglia. Distruggi | space after the full stop |

### Per-card corrections (all)
| id | field | old | new | reason |
|---|---|---|---|---|
| 6057 | desc | tutti le Carte | tutte le Carte | agreement |
| 6173 | desc | E' composto | È composto | accent |
| 6248 | desc | da in Posizione d'Attacco a scoperta in Posizione di Difesa | da Posizione d'Attacco a scoperta in Posizione di Difesa | extra preposition |
| 6659 | desc | viene distrutto in seguito ad una battaglia e mandata al Cimitero | viene distrutto in seguito ad una battaglia e mandato al Cimitero | agreement |
| 6706 | desc | effetto di "Victory Viper XX3" | effetto di "Victory Viper XX03" | card name |
| 6657 | desc | Magia & Trappola , questa | Magia & Trappola, questa | space before the comma |
| 6563 | desc | Carte Magie e Trappola non possono | Le Carte Magia e Trappola non possono | article and plural |

### Complete list of changed cards
**Complete original -> new comparison with the changed words highlighted: `docs/changes_it/cards_diff.md`** (all 182 entries). Raw data: `docs/changes_it/cards.csv`. First 40 rows:

| id | original name | field | original | new |
|---|---|---|---|---|
| 4029 | Verme Bestiale | desc | Questa carta ritorna nella tua mano alla fine del turno. | Questa carta scoperta sul Terreno ritorna nella mano del proprietario durante l'End Phase del tuo turno. |
| 4167 | Guerriero-M #2 | desc | Guerriero-M #2 è specializzato in attacchi combinati. E' equipaggiato con una resistente armatura rivestita di un campo magnetico. | Guerriero-M #2 è specializzato in attacchi combinati. È equipaggiato con una resistente armatura rivestita di un campo magnetico. |
| 4241 | Wodan l' Abitante della Foresta | name | Wodan l' Abitante della Foresta | Wodan l'Abitante della Foresta |
| 4255 | Trasforma-Acque | desc | E' un essere in grado di trasformare l'acqua che esce da un'anfora in draghi che si scagliano all'attacco. | È un essere in grado di trasformare l'acqua che esce da un'anfora in draghi che si scagliano all'attacco. |
| 4270 | Elfo-Uovo Alato | desc | E' uno spirito racchiuso in un guscio d'uovo che utilizza un enorme paio d'ali per respingere qualunque tipo di proiettile scagliato dai nemici. | È uno spirito racchiuso in un guscio d'uovo che utilizza un enorme paio d'ali per respingere qualunque tipo di proiettile scagliato dai nemici. |
| 4284 | Piccola Falena | desc | E' meglio evitare del tutto questa piccola ma mortale creatura... | È meglio evitare del tutto questa piccola ma mortale creatura... |
| 4392 | Draghetto delle Arpie | desc | I valori ATK e DEF di questa carta aumentano di 300 punti per ogni carta "Lady Arpia" scoperta in Campo. | I valori ATK e DEF di questa carta aumentano di 300 punti per ogni carta "Lady Arpia" scoperta sul Terreno. |
| 4398 | Metalzoa | desc | Questo mostro può essere evocato dal Deck al Campo tramite Evocazione Speciale offrendo come Tributo la carta "Zoa" equipaggiata con "Metalmorph". | Questo mostro può essere evocato dal Deck sul Terreno tramite Evocazione Speciale offrendo come Tributo la carta "Zoa" equipaggiata con "Metalmorph". |
| 4469 | Serpente Elettrico | desc | Quando questa carta viene mandata direttamente dalla tua mano al Cimitero a causa dell' effetto di una carta del tuo avversario, pesca 2 carte dal tuo Deck. | Quando questa carta viene mandata direttamente dalla tua mano al Cimitero a causa dell'effetto di una carta del tuo avversario, pesca 2 carte dal tuo Deck. |
| 4476 | Fatasma Magico | name | Fatasma Magico | Fantasma Magico |
| 4502 | Wilmee | desc | E' un coniglio rabbioso che si fa largo tra gli avversari usando i suoi fenomenali artigli. | È un coniglio rabbioso che si fa largo tra gli avversari usando i suoi fenomenali artigli. |
| 4521 | La Statua dell'Isola dell'Est | desc | Un monumento di pietra dall' Isola dell' Est che lancia raggi laser dalle sue labbra di roccia spaccate. | Un monumento di pietra dall'Isola dell'Est che lancia raggi laser dalle sue labbra di roccia spaccate. |
| 4553 | Griggle | desc | Quando questa carta è scoperta sul Terreno e il suo controllo passa al tuo avversario, aumenta I tuoi Life Points di 3000 punti. Quest'effetto può essere usato una sola volta fino a quando questa carta resta scoperta sul Terreno. | Quando questa carta è scoperta sul Terreno e il suo controllo passa al tuo avversario, aumenta i tuoi Life Points di 3000 punti. Quest'effetto può essere usato una sola volta fino a quando questa carta resta scoperta sul Terreno. |
| 4663 | Megamorph | desc | Se hai meno Life Points del tuo avversario, l' ATK base del mostro equipaggiato con questa carta è raddoppiato. Se, invece, è il tuo avversario a disporre di meno Life Points di te, l' ATK base del mostro equipaggiato con questa carta viene dimezzato. | Se hai meno Life Points del tuo avversario, l'ATK base del mostro equipaggiato con questa carta è raddoppiato. Se, invece, è il tuo avversario a disporre di meno Life Points di te, l'ATK base del mostro equipaggiato con questa carta viene dimezzato. |
| 4668 | Insetticida Sterminatore | desc | Distrugge tutti i mostri di tipo Insetto presenti in Campo. | Distrugge tutti i mostri di tipo Insetto presenti sul Terreno. |
| 4670 | Siccità Eterna | desc | Distrugge tutti i mostri di tipo Pesce presenti in Campo. | Distrugge tutti i mostri di tipo Pesce presenti sul Terreno. |
| 4693 | Ventaglio del Goblin | desc | Fin quando questa carta resta scoperta in Campo, tutti i mostri evocati con Evocazione per Scoperta di Livello 2 o inferiore sono immediatamente distrutti senza che i loro effetti siano attivati. | Fin quando questa carta resta scoperta sul Terreno, tutti i mostri evocati con Evocazione per Scoperta di Livello 2 o inferiore sono immediatamente distrutti senza che i loro effetti siano attivati. |
| 4714 | Regina del Cosmo | desc | E' la regina delle galassie e padrona delle stelle. | È la regina delle galassie e padrona delle stelle. |
| 4733 | Manga Ryu-Ran | desc | Questa carta non può essere evocata a meno che la carta "Mondo Toon"sia sul tuo Terreno. Questa carta non può attaccare nello stesso turno in cui viene evocata. Pagare 500 Life Points ogni volta che attacchi con questo mostro. Quando la carta "Mondo Toon" viene distrutta, anche questa carta viene distrutta. Se il tuo avversario non controlla un Mostro Toon sul Terreno, questo mostro può attaccare direttamente i Life Points del tuo avversario. Se un Mostro Toon è sul Terreno del tuo avversario, questo mostro deve attaccarlo. | Questa carta non può essere evocata a meno che la carta "Mondo Toon" sia sul tuo Terreno. Questa carta non può attaccare nello stesso turno in cui viene evocata. Pagare 500 Life Points ogni volta che attacchi con questo mostro. Quando la carta "Mondo Toon" viene distrutta, anche questa carta viene distrutta. Se il tuo avversario non controlla un Mostro Toon sul Terreno, questo mostro può attaccare direttamente i Life Points del tuo avversario. Se un Mostro Toon è sul Terreno del tuo avversario, questo mostro deve attaccarlo. |
| 4734 | Sirena Toon | desc | Questa carta non può essere evocata a meno che la carta "Mondo Toon"sia sul tuo Terreno. Questa carta non può attaccare nello stesso turno in cui viene evocata. Pagare 500 Life Points ogni volta che attacchi con questo mostro. Quando la carta "Mondo Toon" viene distrutta, anche questa carta viene distrutta. Se il tuo avversario non controlla un Mostro Toon sul Terreno, questo mostro può attaccare direttamente i Life Points del tuo avversario. Se un Mostro Toon è sul Terreno del tuo avversario, questo mostro deve attaccarlo. | Questa carta non può essere evocata a meno che la carta "Mondo Toon" sia sul tuo Terreno. Questa carta non può attaccare nello stesso turno in cui viene evocata. Pagare 500 Life Points ogni volta che attacchi con questo mostro. Quando la carta "Mondo Toon" viene distrutta, anche questa carta viene distrutta. Se il tuo avversario non controlla un Mostro Toon sul Terreno, questo mostro può attaccare direttamente i Life Points del tuo avversario. Se un Mostro Toon è sul Terreno del tuo avversario, questo mostro deve attaccarlo. |
| 4735 | Teschio Evocato Toon | desc | Questa carta non può essere evocata a meno che la carta "Mondo Toon"sia sul tuo Terreno. Questa carta non può attaccare nello stesso turno in cui viene evocata. Pagare 500 Life Points ogni volta che attacchi con questo mostro. Quando la carta "Mondo Toon" viene distrutta, anche questa carta viene distrutta. Se il tuo avversario non controlla un Mostro Toon sul Terreno, questo mostro può attaccare direttamente i Life Points del tuo avversario. Se un Mostro Toon è sul Terreno del tuo avversario, questo mostro deve attaccarlo. | Questa carta non può essere evocata a meno che la carta "Mondo Toon" sia sul tuo Terreno. Questa carta non può attaccare nello stesso turno in cui viene evocata. Pagare 500 Life Points ogni volta che attacchi con questo mostro. Quando la carta "Mondo Toon" viene distrutta, anche questa carta viene distrutta. Se il tuo avversario non controlla un Mostro Toon sul Terreno, questo mostro può attaccare direttamente i Life Points del tuo avversario. Se un Mostro Toon è sul Terreno del tuo avversario, questo mostro deve attaccarlo. |
| 4736 | Illusionista dagli Occhi Scuri | desc | SCOPRI: Fin quando questa carta resta in Campo, 1 mostro designato non può attaccare. | SCOPRI: Fin quando questa carta resta sul Terreno, 1 mostro designato non può attaccare. |
| 4737 | Abbandono | desc | Scegli 1 mostro sul Terreno del tuo avversario. Tratta il mostro selezionato come una Carta Magia Equipaggiamento ed equipaggia l'"Abbandono"con essa. L' "Abbandono" assume ATK e DEF del mostro scelto (a un mostro coperto sono attribuiti ATK e DEF pari a 0). Puoi usare quest'effetto solamente una volta per turno e puoi equipaggiare l' "Abbandono" con 1 solo mostro per volta. Se l' "Abbandono" viene distrutto in seguito ad una battaglia, il mostro usato come equipaggiamento viene distrutto invece dell' "Abbandono" e il danno da combattimento inflitto ai tuoi Life Points viene inflitto anche ai Life Points del tuo avversario. | Scegli 1 mostro sul Terreno del tuo avversario. Tratta il mostro selezionato come una Carta Magia Equipaggiamento ed equipaggia l'"Abbandono" con essa. L'"Abbandono" assume ATK e DEF del mostro scelto (a un mostro coperto sono attribuiti ATK e DEF pari a 0). Puoi usare quest'effetto solamente una volta per turno e puoi equipaggiare l'"Abbandono" con 1 solo mostro per volta. Se l'"Abbandono" viene distrutto in seguito ad una battaglia, il mostro usato come equipaggiamento viene distrutto invece dell'"Abbandono" e il danno da combattimento inflitto ai tuoi Life Points viene inflitto anche ai Life Points del tuo avversario. |
| 4748 | Drago Metallico Occhi Rossi | desc | Questa carta può essere evocata solamente con Evocazione Speciale dal Deck al Campo offrendo come Tributo la carta "Drago Nero Occhi Rossi" equipaggiata con la carta "Metalmorph". Il tuo Deck viene quindi mescolato. | Questa carta può essere evocata solamente con Evocazione Speciale dal Deck sul Terreno offrendo come Tributo la carta "Drago Nero Occhi Rossi" equipaggiata con la carta "Metalmorph". Il tuo Deck viene quindi mescolato. |
| 4769 | Insetto Parassita | desc | SCOPRI: Metti questa carta scoperta nel Deck del tuo avversario e mischialo. Quando il tuo avversario pesca questa carta, essa viene immediatamente evocata tramite un'Evocazione Speciale sul Terreno del tuo avversario, scoperta e in Posizione di Difesa e infligge 1000 punti di danno ai suoi Life Points. Da questo momento, e fino a quando questa carta resta scoperta sul Terreno, tutte i mostri scoperti sul Terreno del tuo avversario sono trattati come mostri di Tipo Insetto. | SCOPRI: Metti questa carta scoperta nel Deck del tuo avversario e mischialo. Quando il tuo avversario pesca questa carta, essa viene immediatamente Evocata tramite un'Evocazione Speciale sul Terreno del tuo avversario, scoperta e in Posizione di Difesa e infligge 1000 punti di danno ai suoi Life Points. Da questo momento, e fino a quando questa carta resta scoperta sul Terreno, tutte i mostri scoperti sul Terreno del tuo avversario sono trattati come mostri di Tipo Insetto. |
| 4773 | Drago Toon Occhi Blu | desc | Questa carta non può essere evocata a meno che la carta "Mondo Toon"sia sul tuo Terreno. Questa carta non può attaccare nello stesso turno in cui viene evocata. Pagare 500 Life Points ogni volta che attacchi con questo mostro. Quando la carta "Mondo Toon" viene distrutta, anche questa carta viene distrutta. Se il tuo avversario non controlla un Mostro Toon sul Terreno, questo mostro può attaccare direttamente i Life Points del tuo avversario. Se un Mostro Toon è sul Terreno del tuo avversario, questo mostro deve attaccarlo. | Questa carta non può essere evocata a meno che la carta "Mondo Toon" sia sul tuo Terreno. Questa carta non può attaccare nello stesso turno in cui viene evocata. Pagare 500 Life Points ogni volta che attacchi con questo mostro. Quando la carta "Mondo Toon" viene distrutta, anche questa carta viene distrutta. Se il tuo avversario non controlla un Mostro Toon sul Terreno, questo mostro può attaccare direttamente i Life Points del tuo avversario. Se un Mostro Toon è sul Terreno del tuo avversario, questo mostro deve attaccarlo. |
| 4787 | Elefante Garnecia | desc | E' così pesante che la terra trema sotto i suoi passi. | È così pesante che la terra trema sotto i suoi passi. |
| 4794 | Macchina del Tempo | desc | Quando 1 mostro viene mandato al Cimitero in seguito all'esito di una battaglia, potrai farlo tornare in Campo nella stessa posizione di battaglia effettuando un'Evocazione Speciale. | Quando 1 mostro viene mandato al Cimitero in seguito all'esito di una battaglia, potrai farlo tornare sul Terreno nella stessa posizione di battaglia effettuando un'Evocazione Speciale. |
| 4836 | Buco Trappola | desc | Quando il tuo avversario evoca un mostro (eccetto le Evocazioni Speciali), se l' ATK di quel mostro evocato è di 1000 o superiore, il mostro viene distrutto. | Quando il tuo avversario evoca un mostro (eccetto le Evocazioni Speciali), se l'ATK di quel mostro evocato è di 1000 o superiore, il mostro viene distrutto. |
| 4859 | Chiamata dell'Oscurità | desc | Tutti i mostri fatti tornare grazie alla carta "Mostro Resuscitato" vengono mandati al Cimitero. Inoltre, la carta "Mostro Resuscitato" non può essere giocata fino a quando questa carta rimane in Campo. | Tutti i mostri fatti tornare grazie alla carta "Mostro Resuscitato" vengono mandati al Cimitero. Inoltre, la carta "Mostro Resuscitato" non può essere giocata fino a quando questa carta rimane sul Terreno. |
| 4916 | Senju dalle 1000 Mani | desc | Quando questa carta viene evocata (escludendo le Evocazioni Speciali), puoi scegli 1 Mostro Rituale dal tuo Deck, mostralo ed aggiungilo alla tua mano. Dopo di che, mischia il tuo Deck. | Quando questa carta viene evocata (escludendo le Evocazioni Speciali), puoi scegliere 1 Mostro Rituale dal tuo Deck, mostralo ed aggiungilo alla tua mano. Dopo di che, mischia il tuo Deck. |
| 4931 | Kotodama | desc | Fino a quando questa carta rimane scoperta sul Terreno, non possono essere contemporaneamente presenti in Campo mostri con lo stesso nome (le carte coperte sono escluse da quest'effetto). Se una carta con lo stesso nome viene evocata in seguito, quella carta viene distrutta (se 2 di queste carte vengono giocate simultaneamente, entrambe le carte vengono distrutte). | Fino a quando questa carta rimane scoperta sul Terreno, non possono essere contemporaneamente presenti sul Terreno mostri con lo stesso nome (le carte coperte sono escluse da quest'effetto). Se una carta con lo stesso nome viene evocata in seguito, quella carta viene distrutta (se 2 di queste carte vengono giocate simultaneamente, entrambe le carte vengono distrutte). |
| 5003 | Drago Spada dell'Alligatore | desc | "Cucciolo di Drago" + "Spada dell'Alligatore"⏎Con questa carta puoi infliggere Danno Diretto ai Life Points del tuo avversario se nel lato di Campo del tuo avversario sono presenti Carte Mostro I cui soli Attributi sono TERRA, ACQUA e FUOCO. | "Cucciolo di Drago" + "Spada dell'Alligatore"⏎Con questa carta puoi infliggere Danno Diretto ai Life Points del tuo avversario se sul Terreno del tuo avversario sono presenti Carte Mostro I cui soli Attributi sono TERRA, ACQUA e FUOCO. |
| 5090 | Abisso Splendente | desc | Questo mostro utilizza sia il potere della Luce che quello dell' Oscurità. | Questo mostro utilizza sia il potere della Luce che quello dell'Oscurità. |
| 5091 | Arcidemone di Gilfer | desc | Quando questa carta viene mandata al Cimitero, può essere trattata come una Carta Magia Equipaggiamento ed essere utilizzata per equipaggiare 1 mostro in Campo. Il valore ATK del mostro equipaggiato con questa carta diminuisce di 500 punti. | Quando questa carta viene mandata al Cimitero, può essere trattata come una Carta Magia Equipaggiamento ed essere utilizzata per equipaggiare 1 mostro sul Terreno. Il valore ATK del mostro equipaggiato con questa carta diminuisce di 500 punti. |
| 5104 | Maschera dell' Antimagia | name | Maschera dell' Antimagia | Maschera dell'Antimagia |
| 5113 | Scatola Fatata | desc | Ogni volta che un mostro sul Terreno del tuo avversario attacca, lancia una moneta e scegli testa o croce. Se indovini, l' ATK del mostro attaccante diventa 0 durante la Battle Phase. Paga 500 Life Points durante ogni tua Standby Phase. Se non lo fai, distruggi questa carta. | Ogni volta che un mostro sul Terreno del tuo avversario attacca, lancia una moneta e scegli testa o croce. Se indovini, l'ATK del mostro attaccante diventa 0 durante la Battle Phase. Paga 500 Life Points durante ogni tua Standby Phase. Se non lo fai, distruggi questa carta. |
| 5171 | Tigre Sventata | desc | Nega l'effetto da Scoperta del Mostro, presente in campo coperto e in posizione Difensiva, attaccato da questa Carta. | Nega l'effetto da Scoperta del Mostro, presente sul Terreno coperto e in posizione Difensiva, attaccato da questa Carta. |
| 5174 | Capovolgere il Tavolo | desc | Puoi usare l'effetto di questa Carta solo se nella tua parte di Campo è presente un Mostro scoperto il cui nome comprenda la parola "sventato/a". Distruggi tutte le Carte presenti nella tua parte di Campo a eccezione di questa. Scegli e distruggi un numero di Carte dell'avversario pari alle tue Carte distrutte con quest'effetto. Non puoi mandare in Campo un Mostro con un'evocazione normale o posizionarne uno nel turno in cui hai usato quest'effetto. | Puoi usare l'effetto di questa Carta solo se sul tuo Terreno è presente un Mostro scoperto il cui nome comprenda la parola "sventato/a". Distruggi tutte le Carte presenti sul tuo Terreno a eccezione di questa. Scegli e distruggi un numero di Carte dell'avversario pari alle tue Carte distrutte con quest'effetto. Non puoi mandare sul Terreno un Mostro con un'evocazione normale o posizionarne uno nel turno in cui hai usato quest'effetto. |
| 5175 | Lithmus, Spadaccino del Destino | desc | Questo Mostro può essere Evocato solo tramite Evocazione Rituale utilizzando la Carta Magia Rituale "Rituale di Lithmus". Questa Carta non viene distrutta in conseguenza di una battaglia e non subisce gli effetti delle Carte Trappola. Fin quando in Campo è presente una Carta Trappola scoperta, i valori ATK e DEF di questa Carta sono pari a 3000. | Questo Mostro può essere Evocato solo tramite Evocazione Rituale utilizzando la Carta Magia Rituale "Rituale di Lithmus". Questa Carta non viene distrutta in conseguenza di una battaglia e non subisce gli effetti delle Carte Trappola. Fin quando sul Terreno è presente una Carta Trappola scoperta, i valori ATK e DEF di questa Carta sono pari a 3000. |

(... 142 more rows in the CSV)

## A3. Story dialogues

Archives: `script/stNN_<scene>_i.ehp`, every scene is a pair of members `...Ii.bin` (offsets in UTF-16 characters) and `...Li.bin` (UTF-16LE strings terminated by NUL, some gzip-compressed). **2488 lines** changed (including those that **inherit** the correction because they have the same original text and the same Japanese as a corrected line).

Flow: line-by-line reading compared with English and Japanese -> touch-ups in `tools/data/dialogue_touchups_it.json` (`exact` and `parts`) -> `build_dialogues.py it` -> `dialogue_corrections_it.json` -> `apply_to_iso.py`. Automatic layout rules in `build_dialogues.py`: space after the `《...》` placeholders, three dots followed by a capital (`...Ciao` -> `... Ciao`), base `dialogue_corrections_it_base.json` (~1,380 proposals of the first review). Box constraints: ~46 characters per line, max 3 lines (a placeholder counts ~6 characters): `apply_to_iso` reports the lines that might not fit.

### Re-reading touch-ups: `exact` (6) — whole original sentence -> new sentence
| original | new |
|---|---|
| Not you too, 《C003_3》. | Anche tu no, 《C003_3》. |
| Huh? E tu chi sei?⏎Oh sei il nuovo arrivato.. | Eh? E tu chi sei?⏎Oh, sei il nuovo arrivato... |
| L'Imperatore 《C007_4》abbia⏎un fratello minore e che si | Si dice che l'Imperatore 《C007_4》⏎abbia un fratello minore e che si |
| E tu che vuoi?⏎Vuoi farti un Duello, Huh?. | E tu che vuoi?⏎Vuoi farti un Duello, eh? |
| Ecco, usa questo! | Ecco, usa questo vestito da cameriera! |
| Oddio, sto sbavando un po'... | Beh, non sono poi così bravo... |

### Re-reading touch-ups: `parts` (74) — text replacements applied to every line (in order)
| old | new |
|---|---|
| inslutarmi | insultarmi |
| Uh. Gran folla. | Uh. Che folla. |
| Huh? | Eh? |
| Um... | Ehm... |
| Um,  | Ehm,  |
| Heh? Perché? | Eh? Perché? |
| Whoa! Tu sei | Oh! Tu sei |
| Wow, Ho vinto | Wow, ho vinto |
| un po’ | un po' |
| Uh...Umm... | Ehm... |
| Umm-mmm! | Mmm-mmm! |
| Umm | Ehm |
| umm | ehm |
| Chancelliere | Cancelliere |
| ’ | ' |
| Eek! | Aah! |
| Ouch! | Ahi! |
| Duel... | Duello... |
| Yaaaaawn | Uaaah |
| Yaaawn | Uaaah |
| Yawn... | Uaaah... |
| Uaaah...   | Uaaah... |
|    |   |
| Yawn! | Uaaah! |
| Whoa, | Oh, |
| finiti a Slifer Rosso | finiti allo Slifer Rosso |
| Ooops! | Ops! |
| Oops | Ops |
|  Sandwich di bistecca... | Sandwich di bistecca... |
| huh? | eh? |
| MI stai sfidando | Mi stai sfidando |
| rossa.. | rossa... |
| Er...  | Ehm...  |
| Ughh.. | Ughh... |
| Hey, | Ehi, |
| di Slifer Rosso | dello Slifer Rosso |
| il mio deck | il mio Deck |
| i panino | i panini |
| Err... | Ehm... |
| er...  | ehm...  |
| Uhm.... | Uhm... |
| chiaccherare | chiacchierare |
| Odia I gatti | Odia i gatti |
| vuoi farti Duello | vuoi farti un Duello |
| Whoaaa!! | Oh!! |
| Whoa! | Oh! |
| Hey! | Ehi! |
| Oh, hey, | Oh, ehi, |
| Sei Attributi Deck Masters | Sei Deck Master degli Attributi |
| Uups | Ops |
| di Ra Giallo | del Ra Giallo |
| Whoopee! | Evviva! |
| Boo hoo! | Buu huu! |
| WoW! | Wow! |
| Duello tag | Tag Duel |
| *sob* | *snif* |
| cosi' in gamba | così in gamba |
| Ooops | Ops |
| interessato in Duelli | interessato ai Duelli |
| Huh...? | Eh...? |
| Huh, | Eh, |
| Huh! | Eh! |
| Okay | Ok |
| Yay | Evviva |
| Yo,  | Ehi,  |
| Yo! | Ehi! |
| Sigh... | Uff... |
| Ahem | Ehm |
| Erm! | Ehm! |
| Whoa...! | Oh...! |
| Yeah! | Sì! |
| diamine... ?! | diamine...?! |
| Cancelliere | Preside |
| cancelliere | preside |

### Complete list of lines
**Complete original -> new comparison (with English and Japanese): `docs/changes_it/dialogues_diff.md`** (all 2488 lines). Raw data: `docs/changes_it/dialogues.csv`. First 30:

| id | original | new | English |
|---|---|---|---|
| st01_t01/ImpChrMsg#23 | Velo Nocturno | Velo Notturno | Nightshroud |
| st01_t01/ImpChrMsg#57 | Giocatore　d'azzardo | Giocatore d'azzardo | Gambler |
| st01_t01/ImpChrMsg#62 | Rock Avalanchadora | Rock Valanga | Avalanching Rock |
| st01_t01/ImpChrMsg#65 | Dante Ardiente | Dante Ardente | Blazing Dante |
| st01_t01/ImpChrMsg#68 | Truly  Furiosa | Truly Furioso | Raging Truly |
| st01_t01/ImpChrMsg#71 | Solo Brown | Brown Solitario | Lonely Brown |
| st01_t01/ImpChrMsg#74 | Amo Seydina | Maestro Seydina | Master Seydina |
| st01_t01/ImpChrMsg#78 | Emperador. | Imperatore | Emperor. |
| st01_t01/ImpMapMsg#1 | Un cancello principale | Accademia del duello - Cancello principale | Duel Academy - Main Gate |
| st01_t01/ImpMapMsg#2 | Un cancello principale | Cancello principale | Main Gate |
| st01_t01/ImpMapMsg#7 | Duello Campo | Accademia del duello - Campo di duello | Duel Academy - Duel Field |
| st01_t01/ImpMapMsg#8 | Duello Campo | Campo di duello | Duel Field |
| st01_t01/ImpMapMsg#9 | L'Ufficio di cancelliere | Accademia del duello - Ufficio del Preside | Duel Academy - Chancellor's Office |
| st01_t01/ImpMapMsg#10 | L'Ufficio di cancelliere | Ufficio del Preside | Chancellor's Office |
| st01_t01/ImpMapMsg#13 | Dormitorio Slifer Rosso | Dormitorio Slifer Rosso - Esterno | Slifer Red Dorm - Outside |
| st01_t01/ImpMapMsg#14 | Dormitorio Slifer Rosso | Esterno | Outside |
| st01_t01/ImpMapMsg#15 | Alloggi 101 | Dormitorio Slifer Rosso - Stanza 101 | Slifer Red Dorm - Room 101 |
| st01_t01/ImpMapMsg#16 | Alloggi 101 | Stanza 101 | Room 101 |
| st01_t01/ImpMapMsg#17 | Alloggi 102 | Dormitorio Slifer Rosso - Stanza 102 | Slifer Red Dorm - Room 102 |
| st01_t01/ImpMapMsg#18 | Alloggi 102 | Stanza 102 | Room 102 |
| st01_t01/ImpMapMsg#19 | Alloggi 103 | Dormitorio Slifer Rosso - Stanza 103 | Slifer Red Dorm - Room 103 |
| st01_t01/ImpMapMsg#20 | Alloggi 103 | Stanza 103 | Room 103 |
| st01_t01/ImpMapMsg#21 | Alloggi 104 | Dormitorio Slifer Rosso - Stanza 104 | Slifer Red Dorm - Room 104 |
| st01_t01/ImpMapMsg#22 | Alloggi 104 | Stanza 104 | Room 104 |
| st01_t01/ImpMapMsg#23 | Alloggi 201 | Dormitorio Slifer Rosso - Stanza 201 | Slifer Red Dorm - Room 201 |
| st01_t01/ImpMapMsg#24 | Alloggi 201 | Stanza 201 | Room 201 |
| st01_t01/ImpMapMsg#25 | Alloggi 202 | Dormitorio Slifer Rosso - Stanza 202 | Slifer Red Dorm - Room 202 |
| st01_t01/ImpMapMsg#26 | Alloggi 202 | Stanza 202 | Room 202 |
| st01_t01/ImpMapMsg#27 | Alloggi 203 | Dormitorio Slifer Rosso - Stanza 203 | Slifer Red Dorm - Room 203 |
| st01_t01/ImpMapMsg#28 | Alloggi 203 | Stanza 203 | Room 203 |

(... 2458 more rows in the CSV)

## A4. Duelist sentences in duels

Tables `chr_wordstbl_i.bin` and `02chr_wordstbl_...` inside ~72 `duel/cutin_*.ehp` archives (and `zakov*`). The unique sentences are ~1,800: all re-read. **33 sentences changed** (70 entries). Data: `exact` (7) and `parts` (27) in `duel_line_corrections_it.json`. The `*-ptrs.txt` files of the character archives contain absolute offsets: if a table grows they must be recomputed (`remap_pointers`), otherwise the duel crashes.

Comparison with highlighted words: `docs/changes_it/duel_lines_diff.md`.

| original | new | entries | archive examples |
|---|---|---|---|
| Una rinascita necessita delle⏎fiamme dell'estizione!⏎Prendi questo! | Una rinascita necessita delle⏎fiamme dell'estinzione!⏎Prendi questo! | 1 | cutin_amunael01.ehp |
| Uff, ho perso.!⏎⏎Ma mi sono divertito!⏎Giochiamo ancora in futuro! | Uff, ho perso!⏎⏎Ma mi sono divertito!⏎Giochiamo ancora in futuro! | 1 | cutin_bmgirl01.ehp |
| Avresti dovuto chiamare qualcuno⏎per ⏎coprirti! | Avresti dovuto chiamare qualcuno⏎per coprirti! | 1 | cutin_boy01.ehp |
| Ora attiverò una l'effetto di un mostro! | Ora attiverò l'effetto di un mostro! | 1 | cutin_fubuki_drk01.ehp |
| Che succedeg!⏎⏎Non sai fare altro⏎che urlare? Ha ha ha! | Che succede!⏎⏎Non sai fare altro⏎che urlare? Ha ha ha! | 1 | cutin_fubuki_drk01.ehp |
| Fatto.⏎⏎In ogni caso, duellare non si è solo a una⏎questione di vittorie o sconfitte. | Fatto.⏎⏎In ogni caso, duellare non è solo una⏎questione di vittorie o sconfitte. | 1 | cutin_hayato01.ehp |
| Sigh...⏎⏎Non riesco a vincere. Mai | Sigh...⏎⏎Non riesco a vincere. Mai. | 1 | cutin_hayato01.ehp |
| Forse se mi sconfiggerai⏎Ti rispetterò un po' di più! | Forse se mi sconfiggerai⏎ti rispetterò un po' di più! | 1 | cutin_junko01.ehp |
| Basta così?⏎⏎Mostra un po' di coraggio la ⏎prossima volta! | Basta così?⏎⏎Mostra un po' di coraggio⏎la prossima volta! | 1 | cutin_junko01.ehp |
| Mwahahahaha!⏎⏎Sconfiggendoti,⏎Io ora sono...⏎invincibile! | Mwahahahaha!⏎⏎Sconfiggendoti,⏎io ora sono...⏎invincibile! | 1 | cutin_kagemaru02_a.ehp |
| Sai finito! | Sei finito! | 1 | cutin_kuronosu01.ehp |
| La tua luce...⏎⏎é finita! | La tua luce...⏎⏎è finita! | 1 | cutin_meikyu_m01.ehp |
| bene bene. | Bene, bene. | 1 | cutin_mokeo01.ehp |
| Vuoi sapere perché mai persot?⏎Perché non me lo dici tu. | Vuoi sapere perché hai perso?⏎Perché non me lo dici tu. | 1 | cutin_ryo01.ehp |
| Oh... Spero di vincere... ⏎⏎No, Io SO che vincerò! | Oh... Spero di vincere... ⏎⏎No, io SO che vincerò! | 1 | cutin_shou01.ehp |
| Hai funzionato?! | Ha funzionato?! | 1 | cutin_shou01.ehp |
| (Non mi tirerò più indietro!) ⏎Go! | (Non mi tirerò più indietro!) ⏎Via! | 1 | cutin_shou01.ehp |
| l'effetto di un mostro! | Effetto di un mostro! | 1 | cutin_taizan01.ehp |
| Metto in ballo il mio orgoglio!⏎⏎La mia Magia Terreno!⏎⏎Attivo una Arena delle Amazzoni! | Metto in ballo il mio orgoglio!⏎⏎La mia Magia Terreno!⏎⏎Attivo l'Arena delle Amazzoni! | 1 | cutin_tania01.ehp |
| Vuoi fare una brutta figura? Fa pure! | Vuoi fare una brutta figura? Fa' pure! | 2 | cutin_thunder01.ehp, cutin_thunder_blk01.ehp |
| Beccati la furia del mio demone⏎!⏎Distruzione! | Beccati la furia del mio demone!⏎Distruzione! | 1 | cutin_titan01.ehp |
| La prima cosa da fare è estrarre una⏎carta,⏎vero? | La prima cosa da fare è pescare una⏎carta,⏎vero? | 1 | cutin_tome01.ehp |
| Userò una carda. | Userò una carta. | 1 | cutin_tome01.ehp |
| I'll do it! | Lo farò io! | 1 | zakov54.ehp |
| È il mio turno | È il mio turno. | 12 | zakov55.ehp, zakov56.ehp, zakov57.ehp, zakov58.ehp |
| Attivo una Magia Continua | Attivo una Magia Continua. | 5 | zakov55.ehp, zakov56.ehp, zakov57.ehp, zakov58.ehp |
| Sto attivando una Trappola Continua | Sto attivando una Trappola Continua. | 5 | zakov55.ehp, zakov56.ehp, zakov57.ehp, zakov58.ehp |
| Attivo la mia Magia Terreno | Attivo la mia Magia Terreno. | 5 | zakov70.ehp, zakov71.ehp, zakov72.ehp, zakov73.ehp |
| Evocherò un mostro per Evocazione Rituale | Evocherò un mostro per Evocazione Rituale. | 5 | zakov70.ehp, zakov71.ehp, zakov72.ehp, zakov73.ehp |
| Attivo una Magia.! | Attivo una Magia! | 6 | zakov75.ehp, zakov76.ehp, zakov77.ehp, zakov78.ehp |
| Posizionerò una Carta! | Posizionerò una carta! | 5 | zakov75.ehp, zakov76.ehp, zakov77.ehp, zakov78.ehp |
| Evocon un mostro per Fusione. | Evoco un mostro per Fusione. | 1 | zakov81.ehp |
| Attivo unan Magia Equipaggiamento! | Attivo una Magia Equipaggiamento! | 1 | zakov82.ehp |

## A5. Long and short interface strings

Tables `strTbl*`, `help_strtbl_*`, `ddstrtbl_*`, `field_strtbl*` (format `(n, 12, 12+4n)` + offsets + UTF-16) in 46 archives (the same table is copied into several archives, e.g. `field/always_*_ita.ehp` x6). **298 unique strings changed**. Rules: `tools/corrections/string_rules_it.py` — **159 `STRINGS` entries** (archive, member, 0-based index, [(old, new)], reason), **55 `GLOBALS`** (regex/callable, applied after the STRINGS) on **15 tables** (`TABLES`); plus 1 targeted corrections in `tools/data/ui_texts.json` (in-place writes, text shorter than or equal to the original).

### By member (unique strings changed)
| member | strings |
|---|---|
| strTbl_i.bin | 124 |
| help_strtbl_contents_duel_i.bin | 49 |
| strTbl.bin | 39 |
| help_strtbl_contents.bin | 35 |
| field_strtbl_item.bin | 25 |
| ddstrtbl_i.bin | 13 |
| field_strtbl.bin | 9 |
| help_strtbl_label.bin | 2 |
| help_strtbl_label_i.bin | 2 |

### Global rules (all)
| pattern | replacement | reason |
|---|---|---|
| (?<=[A-Za-zà-ù.,;!?])  +(?=[A-Za-zÀ-ù]) |   | double spaces |
| ’ | ' | typographic apostrophe -> plain |
| \bE'(?=[A-Za-zà-ù]) | È  | E' instead of È |
| \bE'  | È  | E' instead of È |
| (?m)(?:^\|(?<=[.!?] ))E (?=(?:riuscita\|stato\|sempre\|molto)\b) | È  | E without accent |
| chè\b | ché | perché, finché, nonché... |
| \bpò\b | po' | un po' |
| \bfà\b | fa | accent |
| \bsà\b | sa | accent |
| \bstà\b | sta | accent |
| \bnè\b | né | accent |
| \bsè\b | sé | accent |
| \bcosi\b | così | accent |
| \bpiu\b | più | accent |
| \bverrano\b | verranno | typo |
| \bdallla\b | dalla | typo |
| \bpiù più\b | più | repetition |
| \bsanwich\b | sandwich | typo |
| \bSndwich\b | Sandwich | typo |
| \bsoya\b | soia | typo |
| sudentesca | studentesca | typo |
| choccolato | cioccolato | typo |
| scimpanzè | scimpanzé | accent |
| \b(?!(?:po\|va\|sta\|fa\|di\|da\|stai\|dai)\b)([A-Za-zÀ-ÿ]+)' (?=[A-Za-zÀ-ÿ]) | \1' | space after the apostrophe |
| (?<=[A-Za-zà-ù]) '(?=[A-Za-z]) | ' | space before the apostrophe |
| (?<=[a-zà-ù,;] )I (?=[a-zà-ù]) | i  | article with capital I |
| \b([Ii]\|[Dd]ei\|[Nn]ei\|[Aa]i\|[Ss]ui\|[Dd]ai\|[Pp]er i\|[Tt]ra i) Duello\b | \1 Duelli | plural |
| \bDuello Singoli\b | Duelli Singoli | plural |
| \b(\d) Duello\b | \1 Duelli | plural |
| affrontare Duello in cui | affrontare Duelli in cui | plural |
| \bMostri Fusione\b | Mostri da Fusione | type name |
| \bMostri Rituale\b | Mostri Rituali | plural |
| \bGli Mostri\b | I Mostri | article |
| (?m)^Magia (Normali\|Continuate\|Equipaggiamento\|Rituale\|Rituali\|Terreno\|da Terreno\|Rapida\|Rapide)(?=\r?$) | (function) _spell | list of Spell types |
| (?m)^Trappola (Normali\|Continue)(?=\r?$) | Trappole \1 | list of Trap types |
| \bsulle carta\b | sulle carte | plural |
| ●Segna-Monstro | ●Segna-Mostro | name |
| I Segna dei Mostri | I Segna-Mostro | name |
| i Segna non | i Segna-Mostro non | name |
| Un Gettone equivale | Un Segna-Mostro equivale | name |
| Gettoni Evocati | Segna-Mostro Evocati | name |
| ●Guarda delle Carte | ●Guardare le Carte | title |
| ●Activar | ●Attivazione | typo |
| \bin terreno\b | in Terreno | capital letter |
| \bterreno di Duello\b | Terreno di Duello | capital letter |
| Carta da terreno | Carta da Terreno | capital letter |
| \bsuo Effetti Scoperta\b | suo Effetto Scoperta | singular |
| \bl'Effetti Scoperta\b | l'Effetto Scoperta | singular |
| \bQuesta opzione di permette\b | Questa opzione ti permette | typo |
| \bcon ad un\b | con un | typo |
| \b(di\|a\|da\|in) Slifer Red\b | (function) f | dormitory |
| \bSlifer Red\b | Slifer Rosso | dormitory name |
| \b(di\|a\|da\|in) Obelisk Blue\b | (function) f | dormitory |
| \bObelisk Blue\b | Obelisk Blu | dormitory name |
| \bRa Yellow\b | Ra Giallo | dormitory name |

### STRINGS entries (all): where and why
| archive | member | index | changes | reason |
|---|---|---|---|---|
| database/charalist.ehp | strTbl_i.bin | 12 | 1 replacement(s) | terza persona |
| database/charalist.ehp | strTbl_i.bin | 13 | 4 replacement(s) | refusi |
| database/charalist.ehp | strTbl_i.bin | 14 | 3 replacement(s) | refusi |
| database/charalist.ehp | strTbl_i.bin | 15 | 1 replacement(s) | refuso |
| database/charalist.ehp | strTbl_i.bin | 17 | 3 replacement(s) | refusi |
| database/charalist.ehp | strTbl_i.bin | 18 | 3 replacement(s) | refusi |
| database/charalist.ehp | strTbl_i.bin | 20 | 6 replacement(s) | refusi e virgolette |
| database/charalist.ehp | strTbl_i.bin | 21 | 1 replacement(s) | come nei dialoghi: direttore del dormitorio |
| database/charalist.ehp | strTbl_i.bin | 22 | 2 replacement(s) | refusi |
| database/charalist.ehp | strTbl_i.bin | 23 | 3 replacement(s) | refusi |
| database/charalist.ehp | strTbl_i.bin | 24 | 2 replacement(s) | refusi |
| database/charalist.ehp | strTbl_i.bin | 28 | 2 replacement(s) | refusi |
| database/charalist.ehp | strTbl_i.bin | 29 | 1 replacement(s) | spazio |
| database/charalist.ehp | strTbl_i.bin | 31 | 1 replacement(s) | frase confusa |
| database/charalist.ehp | strTbl_i.bin | 34 | 1 replacement(s) | grammatica |
| database/charalist.ehp | strTbl_i.bin | 37 | 3 replacement(s) | refusi |
| database/charalist.ehp | strTbl_i.bin | 43 | 2 replacement(s) | refusi |
| database/charalist.ehp | strTbl_i.bin | 48 | 1 replacement(s) | accordo |
| database/charalist.ehp | strTbl_i.bin | 49 | 1 replacement(s) | accento |
| database/charalist.ehp | strTbl_i.bin | 52 | 1 replacement(s) | Preside con la maiuscola |
| database/duelrecord.ehp | strTbl_i.bin | 26 | 1 replacement(s) | name |
| database/duelrecord.ehp | strTbl_i.bin | 35 | 1 replacement(s) | typo |
| database/duelrecord.ehp | strTbl_i.bin | 63 | 1 replacement(s) | typo |
| database/duelrecord.ehp | strTbl_i.bin | 137 | 1 replacement(s) | confused sentence |
| database/duelrecord.ehp | strTbl_i.bin | 155 | 1 replacement(s) | article |
| database/duelrecord.ehp | strTbl_i.bin | 159 | 1 replacement(s) | style like the other entries |
| database/duelrecord.ehp | strTbl_i.bin | 160 | 1 replacement(s) | style |
| database/duelrecord.ehp | strTbl_i.bin | 161 | 1 replacement(s) | style |
| database/duelrecord.ehp | strTbl_i.bin | 162 | 1 replacement(s) | style |
| database/duelrecord.ehp | strTbl_i.bin | 163 | 1 replacement(s) | sentence |
| database/duelrecord.ehp | strTbl_i.bin | 164 | 1 replacement(s) | sentence |
| database/duelrecord.ehp | strTbl_i.bin | 182 | 1 replacement(s) | plural |
| database/duelrecord.ehp | strTbl_i.bin | 184 | 1 replacement(s) | wrong sentence (copy of 182) |
| database/duelrecord.ehp | strTbl_i.bin | 212 | 1 replacement(s) | typo |
| database/duelrecord.ehp | strTbl_i.bin | 213 | 1 replacement(s) | typo |
| database/duelrecord.ehp | strTbl_i.bin | 248 | 1 replacement(s) | leading space |
| duel/result/result_i.ehp | strTbl.bin | 26 | 1 replacement(s) | name |
| duel/result/result_i.ehp | strTbl.bin | 35 | 1 replacement(s) | typo |
| duel/result/result_i.ehp | strTbl.bin | 63 | 1 replacement(s) | typo |
| duel/result/result_i.ehp | strTbl.bin | 137 | 1 replacement(s) | confused sentence |
| duel/result/result_i.ehp | strTbl.bin | 155 | 1 replacement(s) | article |
| duel/result/result_i.ehp | strTbl.bin | 159 | 1 replacement(s) | style like the other entries |
| duel/result/result_i.ehp | strTbl.bin | 160 | 1 replacement(s) | style |
| duel/result/result_i.ehp | strTbl.bin | 161 | 1 replacement(s) | style |
| duel/result/result_i.ehp | strTbl.bin | 162 | 1 replacement(s) | style |
| duel/result/result_i.ehp | strTbl.bin | 163 | 1 replacement(s) | sentence |
| duel/result/result_i.ehp | strTbl.bin | 164 | 1 replacement(s) | sentence |
| duel/result/result_i.ehp | strTbl.bin | 182 | 1 replacement(s) | plural |
| duel/result/result_i.ehp | strTbl.bin | 184 | 1 replacement(s) | wrong sentence (copy of 182) |
| duel/result/result_i.ehp | strTbl.bin | 212 | 1 replacement(s) | typo |
| duel/result/result_i.ehp | strTbl.bin | 213 | 1 replacement(s) | typo |
| duel/result/result_i.ehp | strTbl.bin | 248 | 1 replacement(s) | leading space |
| deck/all_i.ehp | strTbl.bin | 51 | 1 replacement(s) | spazio |
| deck/all_i.ehp | strTbl.bin | 83 | 1 replacement(s) | refusi |
| deck/all_i.ehp | strTbl.bin | 100 | 1 replacement(s) | spazio |
| deck/all_i.ehp | strTbl.bin | 101 | 1 replacement(s) | spazio |
| deck/all_i.ehp | strTbl.bin | 106 | 1 replacement(s) | spazio |
| deck/all_i.ehp | strTbl.bin | 109 | 1 replacement(s) | frase |
| deck/all_i.ehp | strTbl.bin | 110 | 1 replacement(s) | frase |
| deck/all_i.ehp | strTbl.bin | 111 | 1 replacement(s) | frase |
| deck/all_i.ehp | strTbl.bin | 116 | 1 replacement(s) | articolo |
| deck/all_i.ehp | strTbl.bin | 126 | 1 replacement(s) | '$' al posto dell'a capo |
| deck/all_i.ehp | strTbl.bin | 138 | 1 replacement(s) | frase |
| deck/all_i.ehp | strTbl.bin | 142 | 1 replacement(s) | italiano |
| deck/all_i.ehp | strTbl.bin | 148 | 1 replacement(s) | spazio |
| deck/all_i.ehp | strTbl.bin | 152 | 1 replacement(s) | maiuscola |
| deck/all_i.ehp | strTbl.bin | 154 | 1 replacement(s) | articolo |
| deck/all_i.ehp | strTbl.bin | 155 | 1 replacement(s) | spazio |
| deck/all_i.ehp | help_strtbl_label.bin | 1 | 1 replacement(s) | come l'etichetta del pulsante '?' |
| deck/all_i.ehp | help_strtbl_label.bin | 8 | 1 replacement(s) | coerenza |
| deck/all_i.ehp | help_strtbl_contents.bin | 81 | 1 replacement(s) | nome |
| deck/all_i.ehp | help_strtbl_contents.bin | 100 | 1 replacement(s) | genere |
| deck/all_i.ehp | help_strtbl_contents.bin | 104 | 1 replacement(s) | termine |
| deck/all_i.ehp | help_strtbl_contents.bin | 105 | 1 replacement(s) | spazio |
| deck/all_i.ehp | help_strtbl_contents.bin | 106 | 1 replacement(s) | accordo |
| deck/all_i.ehp | help_strtbl_contents.bin | 107 | 1 replacement(s) | refuso |
| deck/all_i.ehp | help_strtbl_contents.bin | 118 | 1 replacement(s) | refuso |
| deck/all_i.ehp | help_strtbl_contents.bin | 129 | 2 replacement(s) | refusi |
| deck/all_i.ehp | help_strtbl_contents.bin | 157 | 2 replacement(s) | Activar non e' italiano |
| deck/all_i.ehp | help_strtbl_contents.bin | 164 | 3 replacement(s) | plurale e genere |
| deck/all_i.ehp | help_strtbl_contents.bin | 175 | 2 replacement(s) | refusi |
| deck/tutorial.ehp | strTbl_i.bin | 5 | 2 replacement(s) | genere |
| deck/tutorial.ehp | strTbl_i.bin | 25 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 26 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 27 | 1 replacement(s) | virgola |
| deck/tutorial.ehp | strTbl_i.bin | 29 | 1 replacement(s) | articolo |
| deck/tutorial.ehp | strTbl_i.bin | 30 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 34 | 1 replacement(s) | frase |
| deck/tutorial.ehp | strTbl_i.bin | 36 | 1 replacement(s) | punteggiatura |
| deck/tutorial.ehp | strTbl_i.bin | 39 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 82 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 46 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 61 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 74 | 1 replacement(s) | come l'etichetta del pulsante '?' |
| deck/tutorial.ehp | strTbl_i.bin | 79 | 1 replacement(s) | punteggiatura |
| deck/tutorial.ehp | strTbl_i.bin | 86 | 1 replacement(s) | frase |
| deck/tutorial.ehp | strTbl_i.bin | 87 | 1 replacement(s) | spazio |
| deck/tutorial.ehp | strTbl_i.bin | 98 | 1 replacement(s) | genere |
| deck/tutorial.ehp | strTbl_i.bin | 104 | 1 replacement(s) | spazio |
| deck/tutorial.ehp | strTbl_i.bin | 113 | 1 replacement(s) | articolo |
| deck/tutorial.ehp | strTbl_i.bin | 118 | 1 replacement(s) | nome |
| deck/tutorial.ehp | strTbl_i.bin | 119 | 1 replacement(s) | punteggiatura |
| deck/tutorial.ehp | strTbl_i.bin | 126 | 1 replacement(s) | articolo |
| deck/tutorial.ehp | strTbl_i.bin | 128 | 1 replacement(s) | verbo |
| deck/tutorial.ehp | strTbl_i.bin | 129 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 130 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 133 | 1 replacement(s) | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 145 | 1 replacement(s) | termine |
| deck/tutorial.ehp | strTbl_i.bin | 146 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 150 | 1 replacement(s) | articolo |
| deck/tutorial.ehp | strTbl_i.bin | 153 | 1 replacement(s) | frase |
| deck/tutorial.ehp | strTbl_i.bin | 154 | 1 replacement(s) | maiuscola |
| deck/tutorial.ehp | strTbl_i.bin | 166 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 172 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 173 | 1 replacement(s) | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 175 | 1 replacement(s) | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 176 | 1 replacement(s) | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 177 | 1 replacement(s) | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 179 | 1 replacement(s) | frase |
| deck/tutorial.ehp | strTbl_i.bin | 189 | 1 replacement(s) | articolo |
| deck/tutorial.ehp | strTbl_i.bin | 201 | 1 replacement(s) | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 203 | 1 replacement(s) | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 205 | 1 replacement(s) | maiuscola |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 70 | 1 replacement(s) | punto finale |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 72 | 1 replacement(s) | termine |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 73 | 1 replacement(s) | punto finale |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 75 | 1 replacement(s) | frase |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 81 | 1 replacement(s) | spazio |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 84 | 1 replacement(s) | termine |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 87 | 1 replacement(s) | frase |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 88 | 1 replacement(s) | frase |
| duel/start/start_i.ehp | strTbl_i.bin | 2 | 1 replacement(s) | refuso |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 92 | 1 replacement(s) | nome |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 110 | 1 replacement(s) | refuso |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 113 | 1 replacement(s) | genere |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 116 | 1 replacement(s) | refuso |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 123 | 2 replacement(s) | refusi |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 154 | 1 replacement(s) | refuso |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 177 | 2 replacement(s) | Activar non e' italiano |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 184 | 3 replacement(s) | plurale e genere |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 195 | 2 replacement(s) | refusi |
| field/always_*_ita.ehp | field_strtbl.bin | 8 | 1 replacement(s) | come nei dialoghi |
| field/always_*_ita.ehp | field_strtbl.bin | 21 | 1 replacement(s) | imperativo |
| field/always_*_ita.ehp | field_strtbl.bin | 22 | 1 replacement(s) | imperativo |
| field/always_*_ita.ehp | field_strtbl.bin | 57 | 1 replacement(s) | frase |
| field/always_*_ita.ehp | field_strtbl.bin | 58 | 1 replacement(s) | articolo |
| field/always_*_ita.ehp | field_strtbl.bin | 59 | 1 replacement(s) | abbreviazione |
| field/always_*_ita.ehp | field_strtbl.bin | 60 | 1 replacement(s) | termine |
| field/always_*_ita.ehp | field_strtbl.bin | 68 | 1 replacement(s) | spazio |
| field/always_*_ita.ehp | field_strtbl.bin | 98 | 1 replacement(s) | refuso |
| field/always_*_ita.ehp | field_strtbl_item.bin | 95 | 1 replacement(s) | refuso |
| field/always_*_ita.ehp | field_strtbl_item.bin | 60 | 1 replacement(s) | spazio |
| field/always_*_ita.ehp | field_strtbl_item.bin | 157 | 1 replacement(s) | termine |
| field/always_*_ita.ehp | field_strtbl_item.bin | 184 | 1 replacement(s) | refuso |
| field/always_*_ita.ehp | field_strtbl_item.bin | 189 | 1 replacement(s) | frase |
| field/always_*_ita.ehp | field_strtbl_item.bin | 191 | 1 replacement(s) | refuso |
| field/always_*_ita.ehp | field_strtbl_item.bin | 193 | 1 replacement(s) | refuso |
| labo/password.ehp | strTbl_i.bin | 4 | 1 replacement(s) | refusi |
| labo/password.ehp | strTbl_i.bin | 9 | 1 replacement(s) | articolo |

### Targeted corrections `ui_texts.json`
| file | member | index | old | new | reason |
|---|---|---|---|---|---|
| /PSP_GAME/USRDIR/deck/all_i.ehp | strTbl.bin | 107 | Assistenza | Aiuto | etichetta del pulsante '?' del deck editor: "Assistenza" viene tagliata dal bordo dello schermo (si leggeva "Assisten"); in inglese e' "Help" |

### Complete list
**Complete comparison with highlighted words: `docs/changes_it/ui_strings_diff.md`.** Raw data: `docs/changes_it/ui_strings.csv`. First 40:

| member | index | original | new |
|---|---|---|---|
| strTbl_i.bin | 4 | Slifer Red | Slifer Rosso |
| strTbl_i.bin | 5 | Ra Yellow | Ra Giallo |
| strTbl_i.bin | 6 | Obelisk Blue | Obelisk Blu |
| strTbl_i.bin | 12 | Per quanto riguarda il Duello, Jaden è senza dubbio il duellante più  provetto di Slifer Red, o meglio, è il duellante più provetto tra tutti gli studenti del primo anno. Possiede un talento naturale che pochissimi possono sperare di ottenere in sorte. Il segreto della sua forza risiede nella sua tenacia: in qualsiasi circostanza si trovi, Jaden è sempre in grado di recuperare in una sola mossa.⏎⏎Ogni volta che si trova con pochissime Carte in mano, Bubbleman è sempre pronto ad aiutarlo.⏎⏎E' molto risaputo che il Deck di Jaden è sempre ben fornito di Carte Eroe Elementale, Carte che gli ricordano gli Eroi che tanto ammirava durante la sua infanzia.⏎⏎Spesso, nel corso di un duello, Jaden si è trovato a fondere Carte Eroe Elementale, una tattica in cui è particolarmente versato.⏎Questa caratteristica, insieme alla sua incredibile abilità nell' estrarre Carte, lo rendono in grado di sconfiggere facilmente un avversario, specialmente quando si trova in stato di grazia.⏎⏎Per quanto riguarda la sua personalità, Jaden è un giovane spensierato e scanzonato, che ritiene che il divertimento sia l'aspetto più importante di un Duello. All'inizio, Jaden non aveva molti amici all'interno della rigida Accademia del Duello, ma poi, nel corso dei duelli,  in molti hanno notato  il suo carattere allegro e hanno cominciato a trattarlo più amichevolmente.⏎⏎Che cosa pensi delle ragazze rimene un mistero.⏎Più  di una volta è capitato che una ragazza si sia presa una cotta per lui, ma raramente Jaden ha mostrato un qualche interesse.⏎⏎Per quanto riguarda il cibo, è di gusti molto facili e mangia proprio di tutto. | Per quanto riguarda il Duello, Jaden è senza dubbio il duellante più provetto dello Slifer Rosso, o meglio, è il duellante più provetto tra tutti gli studenti del primo anno. Possiede un talento naturale che pochissimi possono sperare di ottenere in sorte. Il segreto della sua forza risiede nella sua tenacia: in qualsiasi circostanza si trovi, Jaden è sempre in grado di recuperare in una sola mossa.⏎⏎Ogni volta che si trova con pochissime Carte in mano, Bubbleman è sempre pronto ad aiutarlo.⏎⏎È molto risaputo che il Deck di Jaden è sempre ben fornito di Carte Eroe Elementale, Carte che gli ricordano gli Eroi che tanto ammirava durante la sua infanzia.⏎⏎Spesso, nel corso di un duello, Jaden si è trovato a fondere Carte Eroe Elementale, una tattica in cui è particolarmente versato.⏎Questa caratteristica, insieme alla sua incredibile abilità nell'estrarre Carte, lo rendono in grado di sconfiggere facilmente un avversario, specialmente quando si trova in stato di grazia.⏎⏎Per quanto riguarda la sua personalità, Jaden è un giovane spensierato e scanzonato, che ritiene che il divertimento sia l'aspetto più importante di un Duello. All'inizio, Jaden non aveva molti amici all'interno della rigida Accademia del Duello, ma poi, nel corso dei duelli, in molti hanno notato il suo carattere allegro e hanno cominciato a trattarlo più amichevolmente.⏎⏎Che cosa pensa delle ragazze rimane un mistero.⏎Più di una volta è capitato che una ragazza si sia presa una cotta per lui, ma raramente Jaden ha mostrato un qualche interesse.⏎⏎Per quanto riguarda il cibo, è di gusti molto facili e mangia proprio di tutto. |
| strTbl_i.bin | 13 | Syrus è un grande ammiratore di Jaden e lo rispetta come se fosse un fratello maggiore. Ma Syrus ha anche un vero fratello maggiore e spesso conia nuovi e diversi soprannomi per ciascuno dei due.⏎⏎Ha molto rispetto per le persone forti ed affidabili ma allo stesso tempo ne è intimidito. Un giorno spera di poter diventare valente come Jaden.⏎Syrus non ha molta confidenza nelle proprie abilità, cosa che sembra essere la causa principale della sua visione pessimistica delle cose. A volte però è estremamente critico anche nei confronti degli altri.⏎⏎All' inizio, quando si cimentava in un Duello, aveva sempre un' atteggiamento molto negativo, poco entusiasta, sempre convinto di non poter mai vincere .Ma da quando ha incontrato Jaden, il suo atteggiamento sta diventando  lentamente più positivo. Syrus è infatuatuato di ogni tipo di veicolo ed usa un Deck pieno di Carte "Vehicroid" ("Vehicroid" è un tipo di macchina). A primo sguardo, sembra  possedere un fascino giovanile ma in realta è un tipo assai forte. Gli capita spesso di innamorarsi perdutamente di una bella ragazza, ma nessuna delle sue cotte si è fino ad ora trasformata in una vera e propria relazione.⏎⏎Il cibo favorito di Syrus viene servito una volta al mese nella mensa di Slifer Red.⏎⏎Non sopporta il cibo piccante. | Syrus è un grande ammiratore di Jaden e lo rispetta come se fosse un fratello maggiore. Ma Syrus ha anche un vero fratello maggiore e spesso conia nuovi e diversi soprannomi per ciascuno dei due.⏎⏎Ha molto rispetto per le persone forti ed affidabili ma allo stesso tempo ne è intimidito. Un giorno spera di poter diventare valente come Jaden.⏎Syrus non ha molta confidenza nelle proprie abilità, cosa che sembra essere la causa principale della sua visione pessimistica delle cose. A volte però è estremamente critico anche nei confronti degli altri.⏎⏎All'inizio, quando si cimentava in un Duello, aveva sempre un atteggiamento molto negativo, poco entusiasta, sempre convinto di non poter mai vincere. Ma da quando ha incontrato Jaden, il suo atteggiamento sta diventando lentamente più positivo. Syrus è infatuato di ogni tipo di veicolo ed usa un Deck pieno di Carte "Vehicroid" ("Vehicroid" è un tipo di macchina). A primo sguardo, sembra possedere un fascino giovanile ma in realtà è un tipo assai forte. Gli capita spesso di innamorarsi perdutamente di una bella ragazza, ma nessuna delle sue cotte si è fino ad ora trasformata in una vera e propria relazione.⏎⏎Il cibo favorito di Syrus viene servito una volta al mese nella mensa dello Slifer Rosso.⏎⏎Non sopporta il cibo piccante. |
| strTbl_i.bin | 14 | Chumley è in realtà  molto più dolce ti quanto possa far pensare il suo nome.                                                                                                  In quanto a carattere, è una persona semplice e pura.⏎Chumley ritiene che un duello debba essere essere qualcosa di più che il semplice fatto di vincere o perdere. Questa sua convizione ci permette di capire come mai abbia perso un anno nella severa Accademia di Duello - alla quale tra l'altro non si ritiene particolarmente adatto.⏎Ma ciò non vuol dire che non sia portato al Duello. Al contrario, le sue doti di Duellante lo rendono in grado di sentire la voce dello spirito del Duello.⏎⏎Chumley è stato in Australia nel corso di una gita scolastica ed è tornato con un'opinione alquanto positiva di questo paese. Di conseguenza, il Deck che usa in questi giorni contiene un gran numero di Carte legate all'Australia.⏎⏎Forse per il fatto che gli manca molto sua madre, è particolarmente attaccato alla Carta di una pop star che non è  proprio più... giovanissima.⏎⏎Chumley non ha un vero e proprio cibo preferito ma tende ad evitare la carne. Mangia invece spesso pesce. | Chumley è in realtà molto più dolce di quanto possa far pensare il suo nome. In quanto a carattere, è una persona semplice e pura.⏎Chumley ritiene che un duello debba essere qualcosa di più che il semplice fatto di vincere o perdere. Questa sua convinzione ci permette di capire come mai abbia perso un anno nella severa Accademia di Duello - alla quale tra l'altro non si ritiene particolarmente adatto.⏎Ma ciò non vuol dire che non sia portato al Duello. Al contrario, le sue doti di Duellante lo rendono in grado di sentire la voce dello spirito del Duello.⏎⏎Chumley è stato in Australia nel corso di una gita scolastica ed è tornato con un'opinione alquanto positiva di questo paese. Di conseguenza, il Deck che usa in questi giorni contiene un gran numero di Carte legate all'Australia.⏎⏎Forse per il fatto che gli manca molto sua madre, è particolarmente attaccato alla Carta di una pop star che non è proprio più... giovanissima.⏎⏎Chumley non ha un vero e proprio cibo preferito ma tende ad evitare la carne. Mangia invece spesso pesce. |
| strTbl_i.bin | 15 | Alexis è la duellista migliore tra tutte le ragazze. Ed è in grado di farsi valere anche contro I ragazzi.⏎Per quanto riguarda l'aspetto fisico poi, è veramente una bellezza mozzafiato, al punto che in tanti la chiamano la "Madonna dell'Accademia".⏎Alexis è dotata di bellezza e senso dell'umorismo; molte delle ragazze la invidiano per queste sue caratteristiche.⏎E'coraggiosa per natura, ma a causa della sua forte determinazione a vincere, c'è anche chi, in certi casi, trova le sue azioni e le sue parole un pò eccessive.⏎⏎Usa un Deck alquanto particolare, chiamato "Cyber Girl", costituito principalmente di attraenti Mostri femminili.⏎Uno di questi è "Cyber Lama", che possiede un effetto che in più di un' occasione l'ha tolta dai guai.⏎⏎Alexis non sembra ancora interesata ai ragazzi.⏎Spesso, invece, la si sente parlare del suo "amore per il duello",⏎e questo suo amore lo si può vedere più che altro nell' assiduità con cui gioca.⏎⏎Le piace mangiare dolci e cibi sani, ma si tiene alla larga da cibi dall'odore pungente. | Alexis è la duellista migliore tra tutte le ragazze. Ed è in grado di farsi valere anche contro i ragazzi.⏎Per quanto riguarda l'aspetto fisico poi, è veramente una bellezza mozzafiato, al punto che in tanti la chiamano la "Madonna dell'Accademia".⏎Alexis è dotata di bellezza e senso dell'umorismo; molte delle ragazze la invidiano per queste sue caratteristiche.⏎È coraggiosa per natura, ma a causa della sua forte determinazione a vincere, c'è anche chi, in certi casi, trova le sue azioni e le sue parole un po' eccessive.⏎⏎Usa un Deck alquanto particolare, chiamato "Cyber Girl", costituito principalmente di attraenti Mostri femminili.⏎Uno di questi è "Cyber Lama", che possiede un effetto che in più di un'occasione l'ha tolta dai guai.⏎⏎Alexis non sembra ancora interessata ai ragazzi.⏎Spesso, invece, la si sente parlare del suo "amore per il duello",⏎e questo suo amore lo si può vedere più che altro nell'assiduità con cui gioca.⏎⏎Le piace mangiare dolci e cibi sani, ma si tiene alla larga da cibi dall'odore pungente. |
| strTbl_i.bin | 16 | Si pensava che Chazz avesse abbandonato l'Accademia del Duello perchè fosse stato ferito nel suo orgoglio di Duellante provetto. Ma ha poi fatto ritorno, determinato a  vincere come non lo era mai stato.⏎A volte è ancora un pò autoritario, ma non è  più distante come prima, l'essersi trovato per un pò tra gli strati più bassi della società deve avergli fatto bene. Come essere umano sembra essere cresciuto parecchio. E, come conseguenza di questo processo di crescita, è ora in grado di sentire la voce dello spirito.⏎⏎Si è servito di molti Deck diversi ma ultimamente si limita più che altro ad usare il "Trio Ojama".⏎Qualche tempo fa, Chazz era più orientato alla forza bruta, ma ultimamente ha cominciato a riconoscere l'importanza della tecnica.⏎⏎In questi ultimi tempi non nutre più lo stesso disprezzo che in passato nutriva per gli studenti di Slifer Red.⏎⏎A Chazz piacciono i cibi raffinati,⏎ma non sopporta la verdura. | Si pensava che Chazz avesse abbandonato l'Accademia del Duello perché fosse stato ferito nel suo orgoglio di Duellante provetto. Ma ha poi fatto ritorno, determinato a vincere come non lo era mai stato.⏎A volte è ancora un po' autoritario, ma non è più distante come prima, l'essersi trovato per un po' tra gli strati più bassi della società deve avergli fatto bene. Come essere umano sembra essere cresciuto parecchio. E, come conseguenza di questo processo di crescita, è ora in grado di sentire la voce dello spirito.⏎⏎Si è servito di molti Deck diversi ma ultimamente si limita più che altro ad usare il "Trio Ojama".⏎Qualche tempo fa, Chazz era più orientato alla forza bruta, ma ultimamente ha cominciato a riconoscere l'importanza della tecnica.⏎⏎In questi ultimi tempi non nutre più lo stesso disprezzo che in passato nutriva per gli studenti dello Slifer Rosso.⏎⏎A Chazz piacciono i cibi raffinati,⏎ma non sopporta la verdura. |
| strTbl_i.bin | 17 | È uno studente del primo anno, e un Duellante di talento della camerata di Obelisk Blue. C'è già chi non esita a definirlo il successore di Zane.⏎È il più giovane dell'aristocratico Gruppo Princeton, ed è considerato un eccellente Duellante e un personaggio molto in vista.⏎In molti si aspettano che dimostri di essere un Duellante migliore dei suoi due fratelli maggiori, ma tali aspettative hanno fatto nascere in lui una grande superbia. Egli, infatti, considera inferiore chi non appartiene alla sua stessa classe sociale, e ha nei sui confronti un atteggiamento molto arrogante.⏎⏎È sempre concentrato durante i Duelli, e nessun Duellante di medio livello ha alcuna possibilità di spuntarla contro il suo stile aggressivo e pugnace.⏎⏎Forse a causa delle sue nobili origini, è molto cortese nei confronti del gentil sesso e lo si potrebbe quasi considerare una specie di femminista.⏎⏎Non avrà mai molti amici tra i Duellanti di Slifer Red fino a quando non abbandonerà il suo atteggiameneto altezzoso. | È uno studente del primo anno, e un Duellante di talento della camerata dell'Obelisk Blu. C'è già chi non esita a definirlo il successore di Zane.⏎È il più giovane dell'aristocratico Gruppo Princeton, ed è considerato un eccellente Duellante e un personaggio molto in vista.⏎In molti si aspettano che dimostri di essere un Duellante migliore dei suoi due fratelli maggiori, ma tali aspettative hanno fatto nascere in lui una grande superbia. Egli, infatti, considera inferiore chi non appartiene alla sua stessa classe sociale, e ha nei suoi confronti un atteggiamento molto arrogante.⏎⏎È sempre concentrato durante i Duelli, e nessun Duellante di medio livello ha alcuna possibilità di spuntarla contro il suo stile aggressivo e pugnace.⏎⏎Forse a causa delle sue nobili origini, è molto cortese nei confronti del gentil sesso e lo si potrebbe quasi considerare una specie di femminista.⏎⏎Non avrà mai molti amici tra i Duellanti dello Slifer Rosso fino a quando non abbandonerà il suo atteggiamento altezzoso. |
| strTbl_i.bin | 18 | Bastion è uno studente geniale ed ha passato a pieni voti l'esame per entrare all' Accademia.⏎E'stato lo studente maschio che maggiori chance ha avuto di entrare a far parte di Obelisk Blue.⏎Bastion possiede un lato serio ma è anche una persona molto aperta ed estroversa. Sebbene si classifichi sempre ben al di sopra dei Duellanti di Slifer Red, non li considera  assolutamente inferiori a lui.⏎⏎Nel suo tempo libero, Bastion è sempre immerso in calcoli e spesso si interrompe per buttar giù  formule sulla prima superficie che gli capiti di trovare.⏎Di conseguenza le pareti della sua camera sono tapezzate di scritte e di numeri. Persino le sue Carte sono coperte di formule matematiche. Questa sua stravagante abitudine la si può notare anche durante un duello. Arriva addirittura al punto di calcolare in anticipo le mosse dell'avversario, applicando i suoi calcoli matematici al proprio stile di combattimento.⏎Mentre Jaden possiede un talento innato che lo rende un duellante senza pari, la superiorità di Bastion si deve invece alla sua tenacia e persistenza.⏎⏎Si vanta di avere ben sei Deck di sei diversi Attributi, che usa in maniera diversa a seconda del suo avversario. Afferma che i suoi Deck siano perfettamente bilanciati ma per una qualche ragione raramente lo si vede prendere parte ad un Duello.⏎⏎Se si considera la sua intelligenza fuori dalla norma, la sua personalità e le sue abilità di Duellante, Bastion possiede indubbiamente un grande futuro. Il suo unico punto debole è la sua "mancanza di presenze" che spinge molti a guardarlo dall'alto in basso.⏎⏎Bastion si vanta di non essere interessato alle ragazze, ma in realtà, quando gli chiedono aiuto, fà di tutto per accontentarle.                             Bastion fa spesso uso di Carte con ragazze sensibili e sommesse ma nella vita reale preferisce donne dal carattere forte.                             ⏎⏎Gli piace mangiare verdure ed in generale sembra una persona dalle sane abitudini.⏎Daltra parte non gli piace la frutta e si dice che odii i dolci. | Bastion è uno studente geniale ed ha passato a pieni voti l'esame per entrare all'Accademia.⏎È stato lo studente maschio che maggiori chance ha avuto di entrare a far parte dell'Obelisk Blu.⏎Bastion possiede un lato serio ma è anche una persona molto aperta ed estroversa. Sebbene si classifichi sempre ben al di sopra dei Duellanti dello Slifer Rosso, non li considera assolutamente inferiori a lui.⏎⏎Nel suo tempo libero, Bastion è sempre immerso in calcoli e spesso si interrompe per buttar giù formule sulla prima superficie che gli capiti di trovare.⏎Di conseguenza le pareti della sua camera sono tappezzate di scritte e di numeri. Persino le sue Carte sono coperte di formule matematiche. Questa sua stravagante abitudine la si può notare anche durante un duello. Arriva addirittura al punto di calcolare in anticipo le mosse dell'avversario, applicando i suoi calcoli matematici al proprio stile di combattimento.⏎Mentre Jaden possiede un talento innato che lo rende un duellante senza pari, la superiorità di Bastion si deve invece alla sua tenacia e persistenza.⏎⏎Si vanta di avere ben sei Deck di sei diversi Attributi, che usa in maniera diversa a seconda del suo avversario. Afferma che i suoi Deck siano perfettamente bilanciati ma per una qualche ragione raramente lo si vede prendere parte ad un Duello.⏎⏎Se si considera la sua intelligenza fuori dalla norma, la sua personalità e le sue abilità di Duellante, Bastion possiede indubbiamente un grande futuro. Il suo unico punto debole è la sua "mancanza di presenza" che spinge molti a guardarlo dall'alto in basso.⏎⏎Bastion si vanta di non essere interessato alle ragazze, ma in realtà, quando gli chiedono aiuto, fa di tutto per accontentarle. Bastion fa spesso uso di Carte con ragazze sensibili e sommesse ma nella vita reale preferisce donne dal carattere forte.                             ⏎⏎Gli piace mangiare verdure ed in generale sembra una persona dalle sane abitudini.⏎D'altra parte non gli piace la frutta e si dice che odii i dolci. |
| strTbl_i.bin | 20 | In qualità di professore del dormitorio maschile di Obelisk Blue, Vellian Crowler è responsabile dei migliori duellanti dell'Accademia.⏎La sua maniera di parlare è molto particolare.⏎⏎Il carattere di Vellian è tipico della rigida filosofia dell'Accademia: tratta con grande gentilezza coloro che riportano buoni voti ma non ha decisamente pazienza con gli studenti che hanno difficoltà a reggere i ritmi serrati dell'Accademia. Ha il suo occhio puntato su Jaden Yuki di Slifer Red e ha eleborato diversi sotterfugi per farlo espellere dall'Accademia.⏎⏎Quando combatte in Duello porta una speciale Veste da Duello. Apparentemente "chiunque riesca ad entrare all' Accademia può comprarne una", ma ad eccezione di Velliar nessuno le hai mai indossate.⏎⏎Si serve di un Deck ben fornito di Carte "Ingranaggio Antico", un tipo di antiche macchine.⏎La sua Carta principale è il Golem-Ingranaggio Antico", una carta tanto potente da essere conosciuta come la "Infrangi Regole".⏎⏎Come del resto si può intuire dal suo aspetto, Velian è un consumatore di beni di lusso, tra i quali possiamo annoverare anche i raffinatissimi cibi che predilige.. | In qualità di professore del dormitorio maschile dell'Obelisk Blu, Vellian Crowler è responsabile dei migliori duellanti dell'Accademia.⏎La sua maniera di parlare è molto particolare.⏎⏎Il carattere di Vellian è tipico della rigida filosofia dell'Accademia: tratta con grande gentilezza coloro che riportano buoni voti ma non ha decisamente pazienza con gli studenti che hanno difficoltà a reggere i ritmi serrati dell'Accademia. Ha il suo occhio puntato su Jaden Yuki dello Slifer Rosso e ha elaborato diversi sotterfugi per farlo espellere dall'Accademia.⏎⏎Quando combatte in Duello porta una speciale Veste da Duello. Apparentemente "chiunque riesca ad entrare all'Accademia può comprarne una", ma ad eccezione di Vellian nessuno le ha mai indossate.⏎⏎Si serve di un Deck ben fornito di Carte "Ingranaggio Antico", un tipo di antiche macchine.⏎La sua Carta principale è il "Golem-Ingranaggio Antico", una carta tanto potente da essere conosciuta come la "Infrangi Regole".⏎⏎Come del resto si può intuire dal suo aspetto, Vellian è un consumatore di beni di lusso, tra i quali possiamo annoverare anche i raffinatissimi cibi che predilige. |
| strTbl_i.bin | 21 | Lyman Banner è professore di Alchimia nonchè presidente di Slifer Red.⏎⏎La sua personalità affabile ed il tono gentile della sua voce rendono difficile capire di che tipo di persona si tratti realmente.⏎⏎Lyman ha raramente, forse mai, preso parte ad un duello in quanto si occupa di Alchimia, ovvero l'arte di creare qualcosa dal nulla.⏎Nessuno si immagina neanche che tipo di Deck potrebbe mai usare.⏎⏎Sebbene gran parte della sua vita sia avvolta nel mistero, quel che è ovvio a tutti è il suo grande amore per i gatti.⏎⏎Anche il suo cibo preferito rimane un mistero. | Lyman Banner è professore di Alchimia nonché direttore dello Slifer Rosso.⏎⏎La sua personalità affabile ed il tono gentile della sua voce rendono difficile capire di che tipo di persona si tratti realmente.⏎⏎Lyman ha raramente, forse mai, preso parte ad un duello in quanto si occupa di Alchimia, ovvero l'arte di creare qualcosa dal nulla.⏎Nessuno si immagina neanche che tipo di Deck potrebbe mai usare.⏎⏎Sebbene gran parte della sua vita sia avvolta nel mistero, quel che è ovvio a tutti è il suo grande amore per i gatti.⏎⏎Anche il suo cibo preferito rimane un mistero. |
| strTbl_i.bin | 22 | Il fratello maggiore di Alexis.⏎Se pensassimo al carattere di Alexis, sarebbe facile immaginare questo Duellante come una persona severa e priva di senso dell'umorismo. In realtà le cose non stanno proprio così. Atticus è infatti allegro e scanzonato, forse fin troppo.Tutte le ragazze perdono regolarmente la testa per la sua affascinante personalità e per le sue divertenti battute.⏎⏎Atticus è un Duellante provetto: alcuni addiririttura sostengono che sia pari a Zane. Sembra che ci sia stato un tempo in cui i due andavano molto d'accordo, anche se risulta difficile immaginare come due persone dal carattere tanto diverso potessero essere amiche.⏎⏎Atticus vorrebbe che sua sorella Alexis fosse come tutte le altre ragazze, e ha fatto di tutto per farla comportare in maniera più femminile, ma è riuscito solo a farla irritare. | Il fratello maggiore di Alexis.⏎Se pensassimo al carattere di Alexis, sarebbe facile immaginare questo Duellante come una persona severa e priva di senso dell'umorismo. In realtà le cose non stanno proprio così. Atticus è infatti allegro e scanzonato, forse fin troppo. Tutte le ragazze perdono regolarmente la testa per la sua affascinante personalità e per le sue divertenti battute.⏎⏎Atticus è un Duellante provetto: alcuni addirittura sostengono che sia pari a Zane. Sembra che ci sia stato un tempo in cui i due andavano molto d'accordo, anche se risulta difficile immaginare come due persone dal carattere tanto diverso potessero essere amiche.⏎⏎Atticus vorrebbe che sua sorella Alexis fosse come tutte le altre ragazze, e ha fatto di tutto per farla comportare in maniera più femminile, ma è riuscito solo a farla irritare. |
| strTbl_i.bin | 23 | Camula è un membro dei Cavalieri dell' Ombra, un gruppo di persone alla ricerca delle Chiavi dello Spirito.⏎Inoltre è anche una vampiressa.⏎⏎Il Deck di Camula consiste di Carte del Tipo Zombie, come per esempio i vampiri. Camula, con i suoi occhi rossi, è in grado di controllare un esercito di pipistrelli che manda a spiare il Deck dell'avversario, per poi cambiare la sua strategia a seconda delle informazioni ricevute. Inoltre, tutti sanno che non si vergona ad usare Carte Proibite e non possiede un grammo di orgoglio quando si tratta di combattere in Duello.⏎⏎Si diverte a trasformare in bambole tutti coloro che hanno perso in duello contro di lei, e poi li aggiunge alla sua orripilante collezione. Tuttavia, se la persona che è stata trasformata in bambola non le è simpattica, non l'aggiunge nenche alla collezione. Non oso neanche pensare a cosa ne farà! | Camula è un membro dei Cavalieri dell'Ombra, un gruppo di persone alla ricerca delle Chiavi dello Spirito.⏎Inoltre è anche una vampiressa.⏎⏎Il Deck di Camula consiste di Carte del Tipo Zombie, come per esempio i vampiri. Camula, con i suoi occhi rossi, è in grado di controllare un esercito di pipistrelli che manda a spiare il Deck dell'avversario, per poi cambiare la sua strategia a seconda delle informazioni ricevute. Inoltre, tutti sanno che non si vergogna ad usare Carte Proibite e non possiede un grammo di orgoglio quando si tratta di combattere in Duello.⏎⏎Si diverte a trasformare in bambole tutti coloro che hanno perso in duello contro di lei, e poi li aggiunge alla sua orripilante collezione. Tuttavia, se la persona che è stata trasformata in bambola non le è simpatica, non l'aggiunge nemmeno alla collezione. Non oso neanche pensare a cosa ne farà! |
| strTbl_i.bin | 24 | Tania è  un membro deli Cavalieri dell' Ombra, un gruppo di persone alla ricerca delle Chiavi dello Spirito.⏎Inoltre  è anche un Amazzone.⏎⏎Sebbene la maggior parte dei Cavalieri dell'Ombra siano molto maliziosi, Tania è una persona allegra ed equilibrata.⏎Trovare un marito è per lei molto più importante della ricerca delle Chiavi dello Spirito.⏎⏎Trattandosi di un'Amazzone, il suo Deck le si addice molto, visto che è costituito unicamente di Carte Amazzone. Tania è una specialista a combattere in Duello mediante queste Carte.⏎⏎Tutti sono curiosi di sapere che fine farà l'uomo che si sceglierà come marito. | Tania è un membro dei Cavalieri dell'Ombra, un gruppo di persone alla ricerca delle Chiavi dello Spirito.⏎Inoltre è anche un'Amazzone.⏎⏎Sebbene la maggior parte dei Cavalieri dell'Ombra siano molto maliziosi, Tania è una persona allegra ed equilibrata.⏎Trovare un marito è per lei molto più importante della ricerca delle Chiavi dello Spirito.⏎⏎Trattandosi di un'Amazzone, il suo Deck le si addice molto, visto che è costituito unicamente di Carte Amazzone. Tania è una specialista a combattere in Duello mediante queste Carte.⏎⏎Tutti sono curiosi di sapere che fine farà l'uomo che si sceglierà come marito. |
| strTbl_i.bin | 25 | Don Zaloog è anch'egli un membro dei Cavalieri dell' Ombra, un gruppo di persone alla ricerca delle Chiavi dello Spirito.⏎Inoltre  è anche il leader di una banda di predoni conosciuta come la Banda dello Scorpione Oscuro.⏎Don Zaloog spesso si traveste e s'introduce nell'Accademia sotto mentite spoglie.⏎In giro si dice che sia un criminale più furbo di quanto lasci credere.⏎⏎Nel corso di un Duello, il suo Deck è composto principalmente di Carte della Banda dello Scorpione Oscuro. Combinazioni di queste Carte sono in grado di sconvolgere seriamente la mano dell' avversario.     | Don Zaloog è anch'egli un membro dei Cavalieri dell'Ombra, un gruppo di persone alla ricerca delle Chiavi dello Spirito.⏎Inoltre è anche il leader di una banda di predoni conosciuta come la Banda dello Scorpione Oscuro.⏎Don Zaloog spesso si traveste e s'introduce nell'Accademia sotto mentite spoglie.⏎In giro si dice che sia un criminale più furbo di quanto lasci credere.⏎⏎Nel corso di un Duello, il suo Deck è composto principalmente di Carte della Banda dello Scorpione Oscuro. Combinazioni di queste Carte sono in grado di sconvolgere seriamente la mano dell'avversario.     |
| strTbl_i.bin | 26 | Un faraone nonchè duellante esperto che non ha perso un solo Duello in più di mille anni.⏎Si dice che sia stato evocato da un sonno profondo e sia diventato membro dei Cavalieri dell'Ombra.⏎Sebbene sia un faraone, è ancora un bambino, e sotto molti aspetti è ancora molto infantile.⏎Basta pensare per esempio alla sua irrazionale paura di perdere.⏎⏎Essendo in campo da oltre mille anni tende ad usare Carte molto antiche. | Un faraone nonché duellante esperto che non ha perso un solo Duello in più di mille anni.⏎Si dice che sia stato evocato da un sonno profondo e sia diventato membro dei Cavalieri dell'Ombra.⏎Sebbene sia un faraone, è ancora un bambino, e sotto molti aspetti è ancora molto infantile.⏎Basta pensare per esempio alla sua irrazionale paura di perdere.⏎⏎Essendo in campo da oltre mille anni tende ad usare Carte molto antiche. |
| strTbl_i.bin | 27 | Dark Titan è stato riportato in vita come un vero "Duellante Ombra".⏎E' un membro dei Cavalieri dell' Ombra, un gruppo di persone alla ricerca delle Chiavi dello Spirito.⏎⏎Sebbene sia diventato un vero Duellante Ombra, il suo aspetto non è cambiato un granchè,⏎infatti ha sempre avuto l'aria di un Duellante Ombra.⏎⏎Si è  sempre servito molto di Carte Arcinemico anche in passato, ma al momento le ha rese più potenti che mai. | Dark Titan è stato riportato in vita come un vero "Duellante Ombra".⏎È un membro dei Cavalieri dell'Ombra, un gruppo di persone alla ricerca delle Chiavi dello Spirito.⏎⏎Sebbene sia diventato un vero Duellante Ombra, il suo aspetto non è cambiato un granché,⏎infatti ha sempre avuto l'aria di un Duellante Ombra.⏎⏎Si è sempre servito molto di Carte Arcinemico anche in passato, ma al momento le ha rese più potenti che mai. |
| strTbl_i.bin | 28 | Si è autonominato Duellante Ombra.⏎Nel corso di un duello ombra, questo spietato duellante non ha esitato a servirsi di un Millennium Item, per far sprofondare il suo avversaro, che aveva perso, nella fossa della morte.⏎⏎Titan si procura da vivere con i Duelli Ombra. Affronta in duello tutti coloro contro i quali è pagato per combattere.⏎La sua richiesta a chi lo contratta è di tre mesi di salario, senza eccezioni.⏎Essendo un Duellante Ombra, il suo Deck consiste principalmente di Carte Arcinemico.⏎⏎Titan è un grande professionista e non si espone mai, neanche per un secondo.⏎E sempre sul chi vive, anche quando stringe la mano del suo avversario. | Si è autonominato Duellante Ombra.⏎Nel corso di un duello ombra, questo spietato duellante non ha esitato a servirsi di un Millennium Item, per far sprofondare il suo avversario, che aveva perso, nella fossa della morte.⏎⏎Titan si procura da vivere con i Duelli Ombra. Affronta in duello tutti coloro contro i quali è pagato per combattere.⏎La sua richiesta a chi lo ingaggia è di tre mesi di salario, senza eccezioni.⏎Essendo un Duellante Ombra, il suo Deck consiste principalmente di Carte Arcinemico.⏎⏎Titan è un grande professionista e non si espone mai, neanche per un secondo.⏎È sempre sul chi vive, anche quando stringe la mano del suo avversario. |
| strTbl_i.bin | 29 | Amnael è la vera identità del professor Lyman Banner.⏎Nel corso di una ricerca alchemica allo scopo di ottenere l' immortalità, questi ha scoperto che la risposta al problemaè legata alle Bestie Sacre e ha quindi deciso di riportarle in vita.⏎⏎Utilizza un Deck Alchemico; rimuovere spesso carte dal gioco, fà parte del suo eccentrico stile di gioco. | Amnael è la vera identità del professor Lyman Banner.⏎Nel corso di una ricerca alchemica allo scopo di ottenere l'immortalità, questi ha scoperto che la risposta al problema è legata alle Bestie Sacre e ha quindi deciso di riportarle in vita.⏎⏎Utilizza un Deck Alchemico; rimuovere spesso carte dal gioco, fa parte del suo eccentrico stile di gioco. |
| strTbl_i.bin | 30 | Kagemaru è il presidente dell' Accademia del Duello.⏎⏎Ha fondato l'Accademia con lo scopo di riunire tutti Duellanti di più grande talento, sperando di poter un giorno usare i loro poteri per riportare in vita le Bestie Sacre, che sono state  seppellite molti anni fa.⏎Se riportate in vita, le Bestie Sacre faranno scaturire un'enorme quantità di energia di cui Kagemaru si potrà servire per ottenere l'eterna giovinezza. | Kagemaru è il presidente dell'Accademia del Duello.⏎⏎Ha fondato l'Accademia con lo scopo di riunire tutti Duellanti di più grande talento, sperando di poter un giorno usare i loro poteri per riportare in vita le Bestie Sacre, che sono state seppellite molti anni fa.⏎Se riportate in vita, le Bestie Sacre faranno scaturire un'enorme quantità di energia di cui Kagemaru si potrà servire per ottenere l'eterna giovinezza. |
| strTbl_i.bin | 31 | Originariamente, era uno studente di Obelisk Blue.⏎Era bravissimo nei suoi studi, ma la sua tecnica d' estrazione lasciava molto a desiderare.⏎Questa sua debolezza lo indusse  e a vivere una vita da recluso a ritirarsi sulle montagne dove si addestrò  rigorosamente per perfezionare la sua tecnica.⏎⏎Dopo molti anni d' allenamento, durante i quali si è dedicato unicamente a perfezionare la sua estrazione, quel particolare aspetto del suo gioco è molto migliorato, ma a farne le spese sono state tutte le sue altre abilità di Duellante. | Originariamente, era uno studente dell'Obelisk Blu.⏎Era bravissimo nei suoi studi, ma la sua tecnica d'estrazione lasciava molto a desiderare.⏎Questa sua debolezza lo indusse a vivere da recluso, ritirandosi sulle montagne dove si addestrò rigorosamente per perfezionare la sua tecnica.⏎⏎Dopo molti anni d'allenamento, durante i quali si è dedicato unicamente a perfezionare la sua estrazione, quel particolare aspetto del suo gioco è molto migliorato, ma a farne le spese sono state tutte le sue altre abilità di Duellante. |
| strTbl_i.bin | 32 | In tempi precedenti fu un Duellante di grande valore, ma i suoi avversari si perdevano di spirito durante I duelli contro di lui e per questa ragione è stato relegato ad un dormitorio speciale.⏎E' in grado di comunicare con gli spiriti e vuole liberare gli spiriti di altre persone in duello.⏎⏎Il punto forte del suo Deck sono le Carte "Mokey Mokey".⏎E'un tipo che esercita una certa attrazione, quindi fai attenzione a non farti risucchiare in una delle sue trappole. | In tempi precedenti fu un Duellante di grande valore, ma i suoi avversari si perdevano di spirito durante i duelli contro di lui e per questa ragione è stato relegato ad un dormitorio speciale.⏎È in grado di comunicare con gli spiriti e vuole liberare gli spiriti di altre persone in duello.⏎⏎Il punto forte del suo Deck sono le Carte "Mokey Mokey".⏎È un tipo che esercita una certa attrazione, quindi fai attenzione a non farti risucchiare in una delle sue trappole. |
| strTbl_i.bin | 33 | Jasmine è Fangirl A, una seguace e fan assidua di Alexis.⏎Chi vuole fornirsi di informazioni (e pettegolezzi) sull'Accademia si reca da lei.⏎Mantiene Alexis al corrente di ciò che succede  nel Campus, anche se Alexis non sembra particolarmente interessata in queste "informazioni".⏎⏎Jasmine utilizza un Deck Arpia, forse a causa della sua ammirazione per le donne dal carattere forte. | Jasmine è Fangirl A, una seguace e fan assidua di Alexis.⏎Chi vuole fornirsi di informazioni (e pettegolezzi) sull'Accademia si reca da lei.⏎Mantiene Alexis al corrente di ciò che succede nel Campus, anche se Alexis non sembra particolarmente interessata in queste "informazioni".⏎⏎Jasmine utilizza un Deck Arpia, forse a causa della sua ammirazione per le donne dal carattere forte. |
| strTbl_i.bin | 34 | Mindy è Fangirl B, una seguace e fan assidua di Alexis.⏎A giudicare dal suo portamento e maniera di parlare, Mindy sembrerebbe una gran dama, ma le sue parole sono spesso acide e rancorose.⏎Ha un gran interesse nel stilare categorie di ragazzi in base al loro fascino e aggiorna sempre la sua Classifica dei Ragazzi.⏎⏎Mindy usa spesso un Deck pieno di affascinanti ragazzoni, chiamato Deck "Pretty Boy".⏎E riuscita ad entrare in Obelisk Blue usando un Deck con emanazioni di Fangirl, e tutti danno per scontato che sia una Duellante di grande talento. | Mindy è Fangirl B, una seguace e fan assidua di Alexis.⏎A giudicare dal suo portamento e maniera di parlare, Mindy sembrerebbe una gran dama, ma le sue parole sono spesso acide e rancorose.⏎Ha un grande interesse nello stilare categorie di ragazzi in base al loro fascino e aggiorna sempre la sua Classifica dei Ragazzi.⏎⏎Mindy usa spesso un Deck pieno di affascinanti ragazzoni, chiamato Deck "Pretty Boy".⏎È riuscita ad entrare nell'Obelisk Blu usando un Deck con emanazioni di Fangirl, e tutti danno per scontato che sia una Duellante di grande talento. |
| strTbl_i.bin | 35 | Wheeler è uno scimpanzè  usato come cavia per vari esperimenti.⏎E stato allevato in un laboratorio che si trova sull' isola dell'Accademia.⏎Non sa giocare a golf ma non se la cava niente male in Duello.⏎Oltre a emettere suoni gutturali, Wheeler è in grado di usare vere e proprie parole. Ma ciò che gli permette di parlare è una macchina, e quindi le parole non escono realmente dalla sua bocca.⏎⏎Nel suo Deck si trovano molte Carte che hanno a che fare con le scimmie.  | Wheeler è uno scimpanzè usato come cavia per vari esperimenti.⏎È stato allevato in un laboratorio che si trova sull'isola dell'Accademia.⏎Non sa giocare a golf ma non se la cava niente male in Duello.⏎Oltre a emettere suoni gutturali, Wheeler è in grado di usare vere e proprie parole. Ma ciò che gli permette di parlare è una macchina, e quindi le parole non escono realmente dalla sua bocca.⏎⏎Nel suo Deck si trovano molte Carte che hanno a che fare con le scimmie.  |
| strTbl_i.bin | 36 | Un ragazzo iscritto a Slifer Red.⏎⏎Ha una figura esile, simile ad una ragazza.⏎⏎Parla di cose da ragazzi ma a volte I suoi manierismi sono molto simili a quelli di una ragazza.⏎⏎Non lo si vede quasi mai farsi la doccia nello spogliatoio con gli altri ragazzi, e fa sempre la doccia da solo, proprio come una ragazza.⏎⏎Se non sapessi che è un ragazzo lo scambierei per una ragazza. | Un ragazzo iscritto allo Slifer Rosso.⏎⏎Ha una figura esile, simile ad una ragazza.⏎⏎Parla di cose da ragazzi ma a volte i suoi manierismi sono molto simili a quelli di una ragazza.⏎⏎Non lo si vede quasi mai farsi la doccia nello spogliatoio con gli altri ragazzi, e fa sempre la doccia da solo, proprio come una ragazza.⏎⏎Se non sapessi che è un ragazzo lo scambierei per una ragazza. |
| strTbl_i.bin | 37 | Una ragazza che dà la caccia a Zane.⏎Ha sostenuto l'esame per entrare all' Accademia solo per poterlo vedere tutti giorni.⏎La sua personalità  potrebbe essere definita ossessiva, ed è decisamente un tipetto geloso.⏎A dirla proprio tutta, è gelosa al punto da perdere la testa e non riconoscere le persone che le stanno attorno.⏎⏎Il suo Deck riflette lo stato danimo di una fanciulla imnnamorata. Spera di poter un giorno comunicare i suoi sentimenti alla persona amata attraverso un duello.⏎La sua Carta principale si chiama "Fanciulla Innamorata". Si tratta di un mostro che riduce l'avversario in prigionia.⏎⏎Dato che è solo al quinto anno, non può ancora entrare al livello superiore dell' Accademia. | Una ragazza che dà la caccia a Zane.⏎Ha sostenuto l'esame per entrare all'Accademia solo per poterlo vedere tutti i giorni.⏎La sua personalità potrebbe essere definita ossessiva, ed è decisamente un tipetto geloso.⏎A dirla proprio tutta, è gelosa al punto da perdere la testa e non riconoscere le persone che le stanno attorno.⏎⏎Il suo Deck riflette lo stato d'animo di una fanciulla innamorata. Spera di poter un giorno comunicare i suoi sentimenti alla persona amata attraverso un duello.⏎La sua Carta principale si chiama "Fanciulla Innamorata". Si tratta di un mostro che riduce l'avversario in prigionia.⏎⏎Dato che è solo al quinto anno, non può ancora entrare al livello superiore dell'Accademia. |
| strTbl_i.bin | 38 | Un Duellante che si  è spesso cimentato contro Yugi Muto, il leggendario Re del Duello.⏎Ha un carattere cinese iscritto sulla fronte che significa: "Labirinto".⏎⏎Si dà da fare insieme al suo fratello minore, Dox, per dar vita ad una potente squadra tag, ma poco o nulla si sa delle sue doti individuali.⏎⏎La sua strategia consiste nel mettere in difficoltà il suo avversario usando un' evocazione denominata "Guardiano del Cancello". | Un Duellante che si è spesso cimentato contro Yugi Muto, il leggendario Re del Duello.⏎Ha un carattere cinese iscritto sulla fronte che significa: "Labirinto".⏎⏎Si dà da fare insieme al suo fratello minore, Dox, per dar vita ad una potente squadra tag, ma poco o nulla si sa delle sue doti individuali.⏎⏎La sua strategia consiste nel mettere in difficoltà il suo avversario usando un'evocazione denominata "Guardiano del Cancello". |
| strTbl_i.bin | 39 | Un Duellante che si  è spesso cimentato contro Yugi Muto, il leggendario Re del Duello.⏎Ha un carattere cinese iscritto sulla fronte che significa: "Labirinto".⏎⏎Si dà da fare insieme al suo fratello maggiore, Para, per dar vita ad una potente squadra tag, ma poco o nulla si sa delle sue  doti individuali.⏎⏎La sua strategia consiste nel mettere in difficoltà il suo avversario usando un' evocazione denominata "Guardiano del Cancello". | Un Duellante che si è spesso cimentato contro Yugi Muto, il leggendario Re del Duello.⏎Ha un carattere cinese iscritto sulla fronte che significa: "Labirinto".⏎⏎Si dà da fare insieme al suo fratello maggiore, Para, per dar vita ad una potente squadra tag, ma poco o nulla si sa delle sue doti individuali.⏎⏎La sua strategia consiste nel mettere in difficoltà il suo avversario usando un'evocazione denominata "Guardiano del Cancello". |
| strTbl_i.bin | 40 | Uno spirito delle Carte. E' energetica e allegra, e adora divertirsi. Ogni volta che c'è qualche attività  divertente nell' Accademia, cerca sempre di parteciparci.                            Come Duellante ha grande talento e potrebbe tener testa ad una delle ragazze di Obelisk Blue. Lei stessa in quanto spirito fa parte delle Carte che usa. | Uno spirito delle Carte. È energetica e allegra, e adora divertirsi. Ogni volta che c'è qualche attività divertente nell'Accademia, cerca sempre di parteciparci. Come Duellante ha grande talento e potrebbe tener testa ad una delle ragazze dell'Obelisk Blu. Lei stessa in quanto spirito fa parte delle Carte che usa. |
| strTbl_i.bin | 41 | Uno spirito delle Carte che al momento sta cercando di diventare di nuovo una persona reale, ma ha bisogno di un attributo umano per realizzare il suo scopo.⏎⏎Nessuno sà cosa abbia intenzione di fare una volta rinato.⏎⏎Usa sè stesso come Carta principale, una Carta il cui effetto può impedire l' attivazione della Carta Trappola.⏎Anche come spirito, potrebbe avere il potere di questo effetto speciale.  | Uno spirito delle Carte che al momento sta cercando di diventare di nuovo una persona reale, ma ha bisogno di un attributo umano per realizzare il suo scopo.⏎⏎Nessuno sa cosa abbia intenzione di fare una volta rinato.⏎⏎Usa sé stesso come Carta principale, una Carta il cui effetto può impedire l'attivazione della Carta Trappola.⏎Anche come spirito, potrebbe avere il potere di questo effetto speciale.  |
| strTbl_i.bin | 43 | Un membro dello staff dell 'Accademia che lavora nel Negozio delle Carte dell' Accademia.⏎E'molto gentile ma quando gli studenti la chiamano "Signora" per farla sentire vecchia, lli fulmina con' un occhiata velenosa.⏎⏎Recentemente sembra dimostrare un certo interesse per i Duelli. | Un membro dello staff dell'Accademia che lavora nel Negozio delle Carte dell'Accademia.⏎È molto gentile ma quando gli studenti la chiamano "Signora" per farla sentire vecchia, li fulmina con un'occhiata velenosa.⏎⏎Recentemente sembra dimostrare un certo interesse per i Duelli. |
| strTbl_i.bin | 45 | Figlio maggiore del Gruppo Princeton, una gigantesca Multinazionale a gestione familiare. Svolge anche attività di politico.⏎Il Gruppo Princeton ambisce a dominare tre settori diversi: politica, finanza e Duelli. Lui si occupa del settore della politica.⏎⏎Non è convinto che suo  fratello Chazz sia in grado di occuparsi del settore dei Duelli, ed è determinato a impadronirsi dell'Accademia per aumentare l'influenza del Gruppo Princeton in quell'ambito.⏎⏎Si serve di un Deck d'alta classe, ed ha investito un'enorme fortuna in Carte rare. | Figlio maggiore del Gruppo Princeton, una gigantesca Multinazionale a gestione familiare. Svolge anche attività di politico.⏎Il Gruppo Princeton ambisce a dominare tre settori diversi: politica, finanza e Duelli. Lui si occupa del settore della politica.⏎⏎Non è convinto che suo fratello Chazz sia in grado di occuparsi del settore dei Duelli, ed è determinato a impadronirsi dell'Accademia per aumentare l'influenza del Gruppo Princeton in quell'ambito.⏎⏎Si serve di un Deck d'alta classe, ed ha investito un'enorme fortuna in Carte rare. |
| strTbl_i.bin | 46 | È il secondo figlio del Gruppo Princeton, una gigantesca multinazionale a conduzione familiare, ed è anche il presidente della società. Il Gruppo Princeton ambisce a dominare tre settori diversi: politica, finanza e Duelli. Si occupa del settore della finanza.⏎⏎Non è convinto che suo  fratello Chazz sia in grado di occuparsi del settore dei Duelli, ed è determinato a impadronirsi dell'Accademia per aumentare l'influenza del Gruppo Princeton in quell'ambito.⏎⏎Si serve di un Deck d'alta classe, ed ha investito un'enorme fortuna in Carte rare. | È il secondo figlio del Gruppo Princeton, una gigantesca multinazionale a conduzione familiare, ed è anche il presidente della società. Il Gruppo Princeton ambisce a dominare tre settori diversi: politica, finanza e Duelli. Si occupa del settore della finanza.⏎⏎Non è convinto che suo fratello Chazz sia in grado di occuparsi del settore dei Duelli, ed è determinato a impadronirsi dell'Accademia per aumentare l'influenza del Gruppo Princeton in quell'ambito.⏎⏎Si serve di un Deck d'alta classe, ed ha investito un'enorme fortuna in Carte rare. |
| strTbl_i.bin | 48 | Fonda è superintendente del dormitorio femminile Obelisk Blue.⏎E'anche istruttrice di ginnastica ed infermiera dell' Accademia del Duello.⏎Molti studenti maschi si fingono malati solo per riuscire a parlarle.⏎⏎Fonda è una Duellante niente male e nel tempo libero a volte si cimenta in Duelli.⏎E'innamorato di tutto ciò che trova "carino" ed il suo Deck è sempre pieno di Carte "carine". | Fonda è superintendente del dormitorio femminile Obelisk Blu.⏎È anche istruttrice di ginnastica ed infermiera dell'Accademia del Duello.⏎Molti studenti maschi si fingono malati solo per riuscire a parlarle.⏎⏎Fonda è una Duellante niente male e nel tempo libero a volte si cimenta in Duelli.⏎È innamorata di tutto ciò che trova "carino" ed il suo Deck è sempre pieno di Carte "carine". |
| strTbl_i.bin | 49 | Un giocatore d'azzardo itinerante.⏎Deve avere  proprio una bella relazione  con la Dea Bendata, visto che non ha mai perso una volta.⏎O almeno così si dice in giro, anche se in realtà lui sostiene di non avere mai perso perchè continua testardamente a giocare finche non vince.⏎Dopo aver sentito dicerie sul conto dei Cavalieri dell'Ombra, si è presentato all' Accademia del Duello con la speranza di allenarsi per poter un giorno combattere contro di loro.⏎Ha anche una relazione speciale con Alexis, forse un segno del destino...⏎⏎Utilizza un Deck "Gambler" pieno di Carte legate all' azzardo. Sostiene che non vi sia niente di più bello che scommettersi tutto sui numeri giusti.⏎⏎Il suo vero nome è Pierre ma si arrabbia quando qualcuno lo chiama così. | Un giocatore d'azzardo itinerante.⏎Deve avere proprio una bella relazione con la Dea Bendata, visto che non ha mai perso una volta.⏎O almeno così si dice in giro, anche se in realtà lui sostiene di non avere mai perso perché continua testardamente a giocare finché non vince.⏎Dopo aver sentito dicerie sul conto dei Cavalieri dell'Ombra, si è presentato all'Accademia del Duello con la speranza di allenarsi per poter un giorno combattere contro di loro.⏎Ha anche una relazione speciale con Alexis, forse un segno del destino...⏎⏎Utilizza un Deck "Gambler" pieno di Carte legate all'azzardo. Sostiene che non vi sia niente di più bello che scommettersi tutto sui numeri giusti.⏎⏎Il suo vero nome è Pierre ma si arrabbia quando qualcuno lo chiama così. |
| strTbl_i.bin | 51 | Un membro dei Cavalieri dell'Ombra, un gruppo di persone alla ricerca delle Chiavi dello Spirito.⏎Pratica l'arte dei "giochi ombra", nel corso dei quali l'anima del perdente viene sigillata all' interno di una Carta.⏎La sua vera identità è sconosciuta. Il suo è un Deck Drago la cui Carta di punta è "Drago Oscuro Occhi Rossi".⏎Il suo obiettivo è  far scomparire il mondo in un mare di fiamme. | Un membro dei Cavalieri dell'Ombra, un gruppo di persone alla ricerca delle Chiavi dello Spirito.⏎Pratica l'arte dei "giochi ombra", nel corso dei quali l'anima del perdente viene sigillata all'interno di una Carta.⏎La sua vera identità è sconosciuta. Il suo è un Deck Drago la cui Carta di punta è "Drago Oscuro Occhi Rossi".⏎Il suo obiettivo è far scomparire il mondo in un mare di fiamme. |
| strTbl_i.bin | 52 | Profilo del preside Sheppard | Profilo del Preside Sheppard |
| strTbl_i.bin | 79 | Evocazione  Fusione | Evocazione Fusione |

(... 258 more rows in the CSV)

## A6. [SPELL CARD] / [TRAP CARD] label of the large card in the duel

In all the `duel/basic_<region><language>.ehp` the label was in English (hash `c2268340`): `apply_to_iso.py` replaces it with `card_spell_trap.gim` of `field/always_<language>_<language>.ehp` (hash `9622cd75`).

| archive | member | original hash | new hash |
|---|---|---|---|
| /PSP_GAME/USRDIR/duel/basic_bi.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |
| /PSP_GAME/USRDIR/duel/basic_fi.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |
| /PSP_GAME/USRDIR/duel/basic_gi.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |
| /PSP_GAME/USRDIR/duel/basic_ii.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |
| /PSP_GAME/USRDIR/duel/basic_si.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |
| /PSP_GAME/USRDIR/duel/basic_ui.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |

## A7. ISO files touched and technical details

142 `.ehp` archives differ from the original (all languages together, because the ISO is a single one; list in `docs/changes_it/touched_files.csv`). The other files (video, audio, `EBOOT.BIN` executable, `PARAM.SFO`) are identical. Non-textual technical differences: `*-ptrs.txt` (absolute member offsets, recomputed when a table changes length), new position of the archives at the end of the ISO.

## A8. What can NOT be changed (game limits)

- The **speaker name** in the dialogue box (e.g. "Preside Sheppard"/"Cancelliere" in Italian, "Doyen Sheppard" in French, "Rector Sheppard" in Spanish) lives in the encrypted EBOOT: it cannot be modified.
- Texts drawn by the game with its own font (dialogues, names, descriptions in the deck, drop-down menus, system keyboard, language selection screen) cannot be replaced by the texture pack: they can only be changed in the ISO.
- The 438 map/background textures are not replaced (the game changes their palette): a limit of MikeyMK's pack, not of our work.

---

# B. TEXTURE PACK

## B1. Origin and structure

Base: **Yu-Gi-Oh! GX Tag Force 1 HD Remastered** by **MikeyMK** (US pack `ULUS10136`) and HD cards by **chrisfand**, adapted to the European ISO `ULES00600`. The project does not redistribute the third-party pack: the patcher gets it from the user. Our work: (1) remap the US pack's **hashes** to the EU ones (`tools/gen_ini.py`), (2) redo the cards and interface lettering in the language, (3) correct the texts, (4) `upscale_extra` for the textures that are not covered.

PPSSPP recognizes a texture by the **hash of its pixels** (xxhash of the data, `gim.data_hash`); every line of `textures.ini` is `0000000000000000<hash8> = path/png`. The PNGs are **4x** the original and redraw exactly the same area. Textures that are identical between languages have the same hash: the replacement holds for all of them (see `docs/TEXTURE_INVENTORY.md`).

### Real structure (from `docs/changes_it/pack_structure.csv`)
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
| ULES00600 (pack di base) | ui_it/ | 113 | 9.8 | fogli_icone, fogli_icone.ini, lettere_esito, lettere_esito.ini, menu_liste, menu_liste.ini, schede_deck, schede_deck.ini, schede_ricette, schede_ricette.ini ... |
| ULES00600 (pack di base) | upscale_extra/ | 1192 | 55.8 | 00085186.png, 00162f3c.png, 003fd929.png, 0047e8d4.png, 00b99210.png, 00c5c424.png, 01673953.png, 01692dff.png, 01f7d8fe.png, 01faa502.png ... |

The **base pack `PSP/TEXTURES/ULES00600` is already Italian**: it contains `cards/small_it`, `large_it`, `tiny_it`, `ui_it` (Italian interface) and the Italian title tiles; the other languages are separate modules in `PSP/TEXTURES/modules/<l>`.

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

Language folders: `frame` (13 files), `large` (2833 files), `large_it` (2833 files), `small` (2833 files), `small_it` (2833 files), `tinyEN` (7 files), `tinyJP` (7 files), `tinyMikeyMK` (7 files), `tiny_it` (7 files). Every card has an **HD small** one (name + description + type, regenerated with free OFL fonts: XCharter Bold for names/type/labels, Libre Baskerville for effects, Newsreader Italic for Normals, PT Serif Caption for Spells/Traps, Charis SIL for the missing glyphs) and an **HD large** one (name only on the frame). In addition: the **attribute table** with the words of the language (`cards/frame/icons_attribute_race_<l>.png`, `attributes.py`), the **Spell/Trap label** (`icons_spell_trap_<l>.png`, `label_it.py` / `extract_labels.py` -> `data/label_eu_<code>_128x32.png`) and the deck **thumbnail atlas** (`tiny_<l>`, `tiny_atlas.py` + `tiny_fragment.py`).

When the text of a card changes (section A2) its images must be regenerated: **181 cards** in italian. List in `docs/changes_it/card_images.csv`. Command: `sh tools/rebuild_corrections.sh USRDIR PACK_US PACK_MOD PYTHON` (small + large cards); on Windows `python -I` does not see the user packages: pass a wrapper that drops `-I`.

Typography: Italian typographic apostrophe and quotation marks; `Tipo`, `Terreno`, `Evocazione tramite Tributo` as in the game.

## B3. HD interface in italian (`ui_it`)

**105 textures** (`docs/changes_it/ui_textures.csv`: file, PPSSPP hash, family, script, original/HD size, neutral/specific, origin in the ISO). By family: fogli_icone 8, lettere_esito 23, menu_liste 6, schede_deck 16, schede_ricette 17, schermata_vs 14, scritte_duello 15, tutorial 6. Of these 11 are neutral (same hash in all languages) and 94 specific. Every family has a script in `tools/ui_textures/<family>.py` (reads `TF1_LANG`): it redraws the lettering texture by texture starting from the low-resolution original of the ISO and from the style of the English pack; same area and same positions (the game crops from fixed rectangles); one font/weight/baseline/shadow per lettering; free fonts (`alt_font.py`).

| family | textures | script | source ISO archive | language texts |
|---|---|---|---|---|
| fogli_icone | 8 | `tools/ui_textures/fogli_icone.py` | ? |  |
| lettere_esito | 23 | `tools/ui_textures/lettere_esito.py` | ? |  |
| menu_liste | 6 | `tools/ui_textures/menu_liste.py` | ? |  |
| schede_deck | 16 | `tools/ui_textures/schede_deck.py` | ? |  |
| schede_ricette | 17 | `tools/ui_textures/schede_ricette.py` | ? |  |
| schermata_vs | 14 | `tools/ui_textures/schermata_vs.py` | ? |  |
| scritte_duello | 15 | `tools/ui_textures/scritte_duello.py` | ? |  |
| tutorial | 6 | `tools/ui_textures/tutorial.py` | tutorial/tutorial_i.ehp (tuto_duelimg01..06) | illustration of the activation dialogue (texts, YES/NO buttons, small card) + 5 maps with the type disc |

Quality rules (valid for every language): regular letters, never deformed one by one; same area as the original; no blur; the text is that of the language's original (only obvious errors are corrected: leftovers from other languages, accents); pixel art is **not** smoothed without confirmation; geometries always measured on the original.

### Drawn texts: original -> HD
Table read by eye, texture by texture: `docs/changes_it/texture_texts_it.md`. Differences from the original: `TAUSCHEN`/`Tauschen` -> `SCAMBIO`/`Scambio`, `Fusione` -> `Fusion`; everything else rewrites the same words.

### List of every texture
(all 105 rows, from `ui_textures.csv`)

| file in the pack | hash | family | original px | HD px | type | ISO origin |
|---|---|---|---|---|---|---|
| ui_it/fogli_icone/all_i__icon04.png | 0f47adc6 | fogli_icone | 128x128 | 512x512 | SPECIFIC | deck/all_i.ehp:icon04.gim |
| ui_it/fogli_icone/all_i__panel.png | 51288b63 | fogli_icone | 256x256 | 1024x1024 | SPECIFIC | shop/all_i.ehp:panel.gim |
| ui_it/fogli_icone/all_i__s_pack.png | 5f349a93 | fogli_icone | 256x256 | 1024x1024 | SPECIFIC | shop/all_i.ehp:s_pack.gim |
| ui_it/fogli_icone/always_bri_ita__pda_pack01.png | e5169419 | fogli_icone | 512x256 | 2048x1024 | SPECIFIC | field/always_bri_ita.ehp:pda_pack01.gim; field/always_fra_ita.ehp:pda_pack01.gim; field/always_ger_ita.ehp:pda_pack01.gim |
| ui_it/fogli_icone/cardalbum__icon06_i.png | aaef4267 | fogli_icone | 128x128 | 512x512 | SPECIFIC | database/cardalbum.ehp:icon06_i.gim; deck/all_i.ehp:icon06.gim; field/always_bri_ita.ehp:card_icon06.gim |
| ui_it/fogli_icone/cardalbum__ocglist_i.png | 295c8b9c | fogli_icone | 128x64 | 512x256 | NEUTRAL | database/cardalbum.ehp:ocglist_e.gim; database/cardalbum.ehp:ocglist_f.gim; database/cardalbum.ehp:ocglist_g.gim |
| ui_it/fogli_icone/title_menu_i__mein_menu00.png | 22692070 | fogli_icone | 128x64 | 512x256 | SPECIFIC | title_menu/title_menu_i.ehp:mein_menu00.gim |
| ui_it/fogli_icone/title_menu_i__trnsmt01.png | bdc35d0d | fogli_icone | 256x128 | 1024x512 | SPECIFIC | title_menu/title_menu_i.ehp:trnsmt01.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100002.png | 60e58b0c | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_draw100002.gim; duel/basic_fi.ehp:duel_draw100002.gim; duel/basic_gi.ehp:duel_draw100002.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100004.png | ce971331 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_draw100004.gim; duel/basic_fi.ehp:duel_draw100004.gim; duel/basic_gi.ehp:duel_draw100004.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100006.png | d2e20c6c | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_draw100006.gim; duel/basic_fi.ehp:duel_draw100006.gim; duel/basic_gi.ehp:duel_draw100006.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100008.png | 1deeba15 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_draw100008.gim; duel/basic_fi.ehp:duel_draw100008.gim; duel/basic_gi.ehp:duel_draw100008.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100010.png | 9a3bba37 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_draw100010.gim; duel/basic_fi.ehp:duel_draw100010.gim; duel/basic_gi.ehp:duel_draw100010.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100012.png | f869c721 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_draw100012.gim; duel/basic_fi.ehp:duel_draw100012.gim; duel/basic_gi.ehp:duel_draw100012.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100014.png | 3d00ca65 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_draw100014.gim; duel/basic_fi.ehp:duel_draw100014.gim; duel/basic_gi.ehp:duel_draw100014.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100002.png | 23e6f72d | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_lose100002.gim; duel/basic_fi.ehp:duel_lose100002.gim; duel/basic_gi.ehp:duel_lose100002.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100004.png | aa67eb3a | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_lose100004.gim; duel/basic_fi.ehp:duel_lose100004.gim; duel/basic_gi.ehp:duel_lose100004.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100006.png | 0b9f2dfd | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_lose100006.gim; duel/basic_fi.ehp:duel_lose100006.gim; duel/basic_gi.ehp:duel_lose100006.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100008.png | 8c1ca0ea | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_lose100008.gim; duel/basic_fi.ehp:duel_lose100008.gim; duel/basic_gi.ehp:duel_lose100008.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100010.png | f7a3a889 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_lose100010.gim; duel/basic_fi.ehp:duel_lose100010.gim; duel/basic_gi.ehp:duel_lose100010.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100012.png | a3668e35 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_lose100012.gim; duel/basic_fi.ehp:duel_lose100012.gim; duel/basic_gi.ehp:duel_lose100012.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100014.png | be8d27c2 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_lose100014.gim; duel/basic_fi.ehp:duel_lose100014.gim; duel/basic_gi.ehp:duel_lose100014.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100016.png | 48fccb29 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_lose100016.gim; duel/basic_fi.ehp:duel_lose100016.gim; duel/basic_gi.ehp:duel_lose100016.gim |
| ui_it/lettere_esito/basic_ii__duel_win100002.png | 00b45490 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_win100002.gim; duel/basic_fi.ehp:duel_win100002.gim; duel/basic_gi.ehp:duel_win100002.gim |
| ui_it/lettere_esito/basic_ii__duel_win100004.png | d38eeaf8 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_win100004.gim; duel/basic_fi.ehp:duel_win100004.gim; duel/basic_gi.ehp:duel_win100004.gim |
| ui_it/lettere_esito/basic_ii__duel_win100006.png | 64e53c06 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_win100006.gim; duel/basic_fi.ehp:duel_win100006.gim; duel/basic_gi.ehp:duel_win100006.gim |
| ui_it/lettere_esito/basic_ii__duel_win100008.png | 6cb385d2 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_win100008.gim; duel/basic_fi.ehp:duel_win100008.gim; duel/basic_gi.ehp:duel_win100008.gim |
| ui_it/lettere_esito/basic_ii__duel_win100010.png | ed0059c9 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_win100010.gim; duel/basic_fi.ehp:duel_win100010.gim; duel/basic_gi.ehp:duel_win100010.gim |
| ui_it/lettere_esito/basic_ii__duel_win100012.png | 8be1d58a | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_win100012.gim; duel/basic_fi.ehp:duel_win100012.gim; duel/basic_gi.ehp:duel_win100012.gim |
| ui_it/lettere_esito/basic_ii__duel_win100014.png | 145d1dd3 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:duel_win100014.gim; duel/basic_fi.ehp:duel_win100014.gim; duel/basic_gi.ehp:duel_win100014.gim |
| ui_it/lettere_esito/basic_ii__duel_win100016.png | 736cf75e | lettere_esito | 64x32 | 256x128 | SPECIFIC | duel/basic_bi.ehp:duel_win100016.gim; duel/basic_fi.ehp:duel_win100016.gim; duel/basic_gi.ehp:duel_win100016.gim |
| ui_it/menu_liste/always_bri_ita__story_sys02.png | 5fc07dd2 | menu_liste | 256x128 | 1024x512 | SPECIFIC | field/always_bri_ita.ehp:story_sys02.gim; field/always_fra_ita.ehp:story_sys02.gim; field/always_ger_ita.ehp:story_sys02.gim |
| ui_it/menu_liste/result_i__menu01.png | 23b37425 | menu_liste | 256x64 | 1024x256 | SPECIFIC | duel/result/result_i.ehp:menu01.gim |
| ui_it/menu_liste/result_i__menu02.png | aeddb824 | menu_liste | 256x128 | 1024x512 | SPECIFIC | duel/result/result_i.ehp:menu02.gim |
| ui_it/menu_liste/title_menu_i__m_menu_title01.png | cfe8de2a | menu_liste | 256x128 | 1024x512 | SPECIFIC | title_menu/title_menu_i.ehp:m_menu_title01.gim |
| ui_it/menu_liste/title_menu_i__press_start0003.png | 747668a4 | menu_liste | 256x16 | 1024x64 | SPECIFIC | title_menu/title_menu_i.ehp:press_start0003.gim |
| ui_it/menu_liste/title_menu_i__trnsmt02.png | 7f3a4012 | menu_liste | 256x256 | 1024x1024 | SPECIFIC | title_menu/title_menu_i.ehp:trnsmt02.gim |
| ui_it/schede_deck/all_i__d_window00008.png | e6b24eae | schede_deck | 128x32 | 512x128 | SPECIFIC | deck/all_i.ehp:d_window00008.gim |
| ui_it/schede_deck/all_i__d_window00016.png | 27153d30 | schede_deck | 64x32 | 256x128 | SPECIFIC | deck/all_i.ehp:d_window00016.gim |
| ui_it/schede_deck/all_i__d_window00024.png | fd0f9c3b | schede_deck | 64x32 | 256x128 | NEUTRAL | deck/all_e.ehp:d_window00024.gim; deck/all_f.ehp:d_window00024.gim; deck/all_g.ehp:d_window00024.gim |
| ui_it/schede_deck/all_i__d_window00031.png | b77db24b | schede_deck | 64x32 | 256x128 | NEUTRAL | deck/all_e.ehp:d_window00031.gim; deck/all_f.ehp:d_window00031.gim; deck/all_g.ehp:d_window00031.gim |
| ui_it/schede_deck/all_i__d_window00033.png | 339f25bd | schede_deck | 256x32 | 1024x128 | SPECIFIC | deck/all_i.ehp:d_window00033.gim |
| ui_it/schede_deck/all_i__d_window00034.png | 1659d75e | schede_deck | 256x32 | 1024x128 | NEUTRAL | deck/all_e.ehp:d_window00034.gim; deck/all_f.ehp:d_window00034.gim; deck/all_g.ehp:d_window00034.gim |
| ui_it/schede_deck/all_i__d_window00051.png | cefa3d7e | schede_deck | 64x32 | 256x128 | SPECIFIC | deck/all_i.ehp:d_window00051.gim |
| ui_it/schede_deck/all_i__d_window00062.png | f5fd73f9 | schede_deck | 128x32 | 512x128 | SPECIFIC | deck/all_i.ehp:d_window00062.gim; labo/conv_machine.ehp:window_i0016.gim; title_menu/title_menu_i.ehp:t_window0015.gim |
| ui_it/schede_deck/all_i__d_window00101.png | 22ebca63 | schede_deck | 64x32 | 256x128 | SPECIFIC | deck/all_i.ehp:d_window00101.gim; labo/rental.ehp:window_i0008.gim |
| ui_it/schede_deck/all_i__d_window00120.png | 4556da1f | schede_deck | 64x32 | 256x128 | NEUTRAL | deck/all_e.ehp:d_window00120.gim; deck/all_f.ehp:d_window00120.gim; deck/all_g.ehp:d_window00120.gim |
| ui_it/schede_deck/all_i__tab_title.png | 6852c8c2 | schede_deck | 256x32 | 1024x128 | SPECIFIC | shop/all_i.ehp:tab_title.gim |
| ui_it/schede_deck/conv_machine__window_i0009.png | 6ca9eba7 | schede_deck | 128x32 | 512x128 | SPECIFIC | labo/conv_machine.ehp:window_i0009.gim; labo/conv_machine.ehp:window_i0026.gim |
| ui_it/schede_deck/conv_machine__window_i0022.png | ada2c664 | schede_deck | 256x32 | 1024x128 | NEUTRAL | labo/conv_machine.ehp:window_f0022.gim; labo/conv_machine.ehp:window_g0022.gim; labo/conv_machine.ehp:window_i0022.gim |
| ui_it/schede_deck/password__key_i0027.png | 37603c6b | schede_deck | 128x32 | 512x128 | SPECIFIC | labo/password.ehp:key_i0027.gim |
| ui_it/schede_deck/rental__window_i0015.png | fee49520 | schede_deck | 128x32 | 512x128 | SPECIFIC | labo/rental.ehp:window_i0015.gim; labo/rental.ehp:window_s0015.gim |
| ui_it/schede_deck/rental__window_i0026.png | d4ea2e3a | schede_deck | 64x32 | 256x128 | SPECIFIC | labo/rental.ehp:window_i0026.gim |
| ui_it/schede_ricette/duelrecord__parts_i.png | 4e51e475 | schede_ricette | 128x64 | 512x256 | SPECIFIC | database/duelrecord.ehp:parts_i.gim |
| ui_it/schede_ricette/limitlist__window_i0002.png | 6c94dcad | schede_ricette | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_i0002.gim |
| ui_it/schede_ricette/limitlist__window_i0004.png | 9acba8ec | schede_ricette | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_i0004.gim |
| ui_it/schede_ricette/limitlist__window_i0012.png | 5c0e1d7a | schede_ricette | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_i0012.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010002.png | 763a4766 | schede_ricette | 256x256 | 1024x1024 | NEUTRAL | deck/recipe_view_e.ehp:recipe010002.gim; deck/recipe_view_f.ehp:recipe010002.gim; deck/recipe_view_g.ehp:recipe010002.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010004.png | b2427f09 | schede_ricette | 256x64 | 1024x256 | SPECIFIC | deck/recipe_view_e.ehp:recipe010004.gim; deck/recipe_view_f.ehp:recipe010004.gim; deck/recipe_view_i.ehp:recipe010004.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010006.png | 44c8b170 | schede_ricette | 256x64 | 1024x256 | NEUTRAL | deck/recipe_view_e.ehp:recipe010006.gim; deck/recipe_view_f.ehp:recipe010006.gim; deck/recipe_view_g.ehp:recipe010006.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010008.png | 9b52cd0c | schede_ricette | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_i.ehp:recipe010008.gim; title_menu/title_menu_i.ehp:recipe_sel00002.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010015.png | 9d53d71b | schede_ricette | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_i.ehp:recipe010015.gim; title_menu/title_menu_i.ehp:recipe_sel00009.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010027.png | eb6d8202 | schede_ricette | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_i.ehp:recipe010027.gim; title_menu/title_menu_i.ehp:recipe_sel00020.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010029.png | 29e9a88e | schede_ricette | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_i.ehp:recipe010029.gim; title_menu/title_menu_i.ehp:recipe_sel00022.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010031.png | 4ceb96c4 | schede_ricette | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_i.ehp:recipe010031.gim; title_menu/title_menu_i.ehp:recipe_sel00024.gim |
| ui_it/schede_ricette/title_menu_i__dmenu_recipe.png | e1ba3fc9 | schede_ricette | 128x32 | 512x128 | NEUTRAL | title_menu/title_menu_e.ehp:dmenu_recipe.gim; title_menu/title_menu_f.ehp:dmenu_recipe.gim; title_menu/title_menu_g.ehp:dmenu_recipe.gim |
| ui_it/schede_ricette/title_menu_i__recipe_panel.png | 35c103aa | schede_ricette | 128x128 | 512x512 | NEUTRAL | title_menu/title_menu_e.ehp:recipe_panel.gim; title_menu/title_menu_f.ehp:recipe_panel.gim; title_menu/title_menu_g.ehp:recipe_panel.gim |
| ui_it/schede_ricette/title_menu_i__recipe_sel00033.png | 13e83af2 | schede_ricette | 128x32 | 512x128 | SPECIFIC | title_menu/title_menu_i.ehp:recipe_sel00033.gim |
| ui_it/schede_ricette/title_menu_i__t_window0008.png | edf9b615 | schede_ricette | 64x32 | 256x128 | SPECIFIC | title_menu/title_menu_i.ehp:t_window0008.gim |
| ui_it/schede_ricette/title_menu_i__t_window0026.png | 50bfc4e3 | schede_ricette | 64x32 | 256x128 | SPECIFIC | title_menu/title_menu_i.ehp:t_window0026.gim |
| ui_it/schermata_vs/start_all__jyanken20_i0005.png | 84daf8b2 | schermata_vs | 256x32 | 1024x128 | SPECIFIC | duel/start/start_all.ehp:jyanken20_i0005.gim; duel/start/start_e.ehp:jyanken20_i0005.gim; duel/start/start_f.ehp:jyanken20_i0005.gim |
| ui_it/schermata_vs/start_all__jyanken20_i0007.png | f5bbbb53 | schermata_vs | 256x32 | 1024x128 | SPECIFIC | duel/start/start_all.ehp:jyanken20_i0007.gim; duel/start/start_e.ehp:jyanken20_i0007.gim; duel/start/start_f.ehp:jyanken20_i0007.gim |
| ui_it/schermata_vs/start_all__vs_much1_i0001.png | a50e57e6 | schermata_vs | 128x16 | 512x64 | SPECIFIC | duel/start/start_all.ehp:vs_much1_i0001.gim; duel/start/start_e.ehp:vs_much1_i0001.gim; duel/start/start_f.ehp:vs_much1_i0001.gim |
| ui_it/schermata_vs/start_all__vs_much2_i0001.png | 8f118f8a | schermata_vs | 128x16 | 512x64 | SPECIFIC | duel/start/start_all.ehp:vs_much2_i0001.gim; duel/start/start_e.ehp:vs_much2_i0001.gim; duel/start/start_f.ehp:vs_much2_i0001.gim |
| ui_it/schermata_vs/start_all__vs_much3_i0001.png | ae083f33 | schermata_vs | 128x16 | 512x64 | SPECIFIC | duel/start/start_all.ehp:vs_much3_i0001.gim; duel/start/start_e.ehp:vs_much3_i0001.gim; duel/start/start_f.ehp:vs_much3_i0001.gim |
| ui_it/schermata_vs/start_e__d_menu01_i.png | f098096b | schermata_vs | 256x256 | 1024x1024 | SPECIFIC | duel/start/start_e.ehp:d_menu01_i.gim; duel/start/start_f.ehp:d_menu01_i.gim; duel/start/start_g.ehp:d_menu01_i.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0005.png | 50201760 | schermata_vs | 256x32 | 1024x128 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_i0005.gim; duel/start/start_f.ehp:vs_bg01_1_i0005.gim; duel/start/start_g.ehp:vs_bg01_1_i0005.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0007.png | 92f2114b | schermata_vs | 256x64 | 1024x256 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_i0007.gim; duel/start/start_f.ehp:vs_bg01_1_i0007.gim; duel/start/start_g.ehp:vs_bg01_1_i0007.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0008.png | 5fb4b6dc | schermata_vs | 256x64 | 1024x256 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_i0008.gim; duel/start/start_f.ehp:vs_bg01_1_i0008.gim; duel/start/start_g.ehp:vs_bg01_1_i0008.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0012.png | 01c81cd4 | schermata_vs | 128x32 | 512x128 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_i0012.gim; duel/start/start_f.ehp:vs_bg01_1_i0012.gim; duel/start/start_g.ehp:vs_bg01_1_i0012.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0014.png | 413ccf1d | schermata_vs | 128x64 | 512x256 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_i0014.gim; duel/start/start_f.ehp:vs_bg01_1_i0014.gim; duel/start/start_g.ehp:vs_bg01_1_i0014.gim |
| ui_it/schermata_vs/start_e__vs_bg01_2_i0001.png | 005ca7af | schermata_vs | 128x32 | 512x128 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_2_i0001.gim; duel/start/start_f.ehp:vs_bg01_2_i0001.gim; duel/start/start_g.ehp:vs_bg01_2_i0001.gim |
| ui_it/schermata_vs/start_e__vs_bg01_2_i0004.png | 6b0b0fbd | schermata_vs | 128x16 | 512x64 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_2_i0004.gim; duel/start/start_f.ehp:vs_bg01_2_i0004.gim; duel/start/start_g.ehp:vs_bg01_2_i0004.gim |
| ui_it/schermata_vs/start_i__jnk_card01.png | 38e5ae61 | schermata_vs | 512x256 | 2048x1024 | SPECIFIC | duel/start/start_i.ehp:jnk_card01.gim |
| ui_it/scritte_duello/basic_ii__card_icon03.png | 376925c7 | scritte_duello | 128x128 | 512x512 | SPECIFIC | duel/basic_bi.ehp:card_icon03.gim; duel/basic_fi.ehp:card_icon03.gim; duel/basic_gi.ehp:card_icon03.gim |
| ui_it/scritte_duello/basic_ii__card_side.png | dfbaa424 | scritte_duello | 64x32 | 256x128 | NEUTRAL | duel/basic_be.ehp:card_side.gim; duel/basic_bf.ehp:card_side.gim; duel/basic_bg.ehp:card_side.gim |
| ui_it/scritte_duello/basic_ii__chain010003.png | 235b1041 | scritte_duello | 64x32 | 256x128 | SPECIFIC | duel/basic_bi.ehp:chain010003.gim; duel/basic_fi.ehp:chain010003.gim; duel/basic_gi.ehp:chain010003.gim |
| ui_it/scritte_duello/basic_ii__chain010005.png | 79b7261f | scritte_duello | 128x32 | 512x128 | SPECIFIC | duel/basic_bi.ehp:chain010005.gim; duel/basic_fi.ehp:chain010005.gim; duel/basic_gi.ehp:chain010005.gim |
| ui_it/scritte_duello/basic_ii__dilect_atk00001.png | ba952e24 | scritte_duello | 256x32 | 1024x128 | SPECIFIC | duel/basic_bi.ehp:dilect_atk00001.gim; duel/basic_fi.ehp:dilect_atk00001.gim; duel/basic_gi.ehp:dilect_atk00001.gim |
| ui_it/scritte_duello/basic_ii__dilect_atk00003.png | 58789f5c | scritte_duello | 128x32 | 512x128 | SPECIFIC | duel/basic_bi.ehp:dilect_atk00003.gim; duel/basic_fi.ehp:dilect_atk00003.gim; duel/basic_gi.ehp:dilect_atk00003.gim |
| ui_it/scritte_duello/basic_ii__next_player0001.png | 8abf9d52 | scritte_duello | 64x32 | 256x128 | SPECIFIC | duel/basic_bi.ehp:next_player0001.gim; duel/basic_fi.ehp:next_player0001.gim; duel/basic_gi.ehp:next_player0001.gim |
| ui_it/scritte_duello/basic_ii__next_player0002.png | 6bc72dfe | scritte_duello | 256x32 | 1024x128 | SPECIFIC | duel/basic_bi.ehp:next_player0002.gim; duel/basic_fi.ehp:next_player0002.gim; duel/basic_gi.ehp:next_player0002.gim |
| ui_it/scritte_duello/basic_ii__next_player0004.png | 8a774ddd | scritte_duello | 64x32 | 256x128 | SPECIFIC | duel/basic_bi.ehp:next_player0004.gim; duel/basic_fi.ehp:next_player0004.gim; duel/basic_gi.ehp:next_player0004.gim |
| ui_it/scritte_duello/basic_ii__next_player0005.png | 83cf47f4 | scritte_duello | 256x32 | 1024x128 | SPECIFIC | duel/basic_bi.ehp:next_player0005.gim; duel/basic_fi.ehp:next_player0005.gim; duel/basic_gi.ehp:next_player0005.gim |
| ui_it/scritte_duello/basic_ii__score-top100011.png | 36655dfa | scritte_duello | 32x32 | 128x128 | SPECIFIC | duel/basic_bi.ehp:score-top100011.gim; duel/basic_bs.ehp:score-top100011.gim; duel/basic_fi.ehp:score-top100011.gim |
| ui_it/scritte_duello/basic_ii__score-top100013.png | 97d1b9a7 | scritte_duello | 32x32 | 128x128 | SPECIFIC | duel/basic_bi.ehp:score-top100013.gim; duel/basic_bs.ehp:score-top100013.gim; duel/basic_fi.ehp:score-top100013.gim |
| ui_it/scritte_duello/basic_ii__start_duel10001.png | faf5cb43 | scritte_duello | 64x64 | 256x256 | SPECIFIC | duel/basic_bi.ehp:start_duel10001.gim; duel/basic_fi.ehp:start_duel10001.gim; duel/basic_gi.ehp:start_duel10001.gim |
| ui_it/scritte_duello/basic_ii__start_duel10002.png | 04bb7f71 | scritte_duello | 256x64 | 1024x256 | SPECIFIC | duel/basic_bi.ehp:start_duel10002.gim; duel/basic_fi.ehp:start_duel10002.gim; duel/basic_gi.ehp:start_duel10002.gim |
| ui_it/scritte_duello/basic_ii__start_duel10005.png | ad550ab4 | scritte_duello | 128x32 | 512x128 | SPECIFIC | duel/basic_bi.ehp:start_duel10005.gim; duel/basic_fi.ehp:start_duel10005.gim; duel/basic_gi.ehp:start_duel10005.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg01.png | 7dd7d0f0 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_i.ehp:tuto_duelimg01.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg02.png | 71437f61 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_i.ehp:tuto_duelimg02.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg03.png | f78156cc | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_i.ehp:tuto_duelimg03.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg04.png | ee87c47c | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_i.ehp:tuto_duelimg04.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg05.png | 866124a4 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_i.ehp:tuto_duelimg05.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg06.png | 030db8b7 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_i.ehp:tuto_duelimg06.gim |

### Italian textures without a counterpart in `ui_fr` (19) and why
13 are neutral (same hash in all languages: recipe panels, Side/Deck/Fusion Deck tabs, bars, `card_side`...). 6 have local wording in the original (`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `d_window00016`, `duelrecord parts`): Italian has NUOVO / N / Fusion, the original French has NEW / Fusion and already has its HD ones in `upscale_extra`. The deck editor tab says **Fusion** (not "Fusione"): "Fusion Deck" is called that in all languages.

## B4. The duel number sheet (`card_icon03`)

A single sheet with LP digits, time, keys and multipliers; different hash per language. Recipe chosen by the user (`tools/ui_textures/icon03_languages.py`, rerun with `--apply`):
- rows 0-180 (small digits and signs, orange keys 1/2/3, big digits 0-9 with "LP", small digits 0-9): **from the US pack**, crisp pixel art;
- cells in which the European game differs from the US pack (black check mark, grey ball, empty pill, time word): **original pixels enlarged 4x without smoothing**; time word **TEMPO**; the orange pill ("Single" in the US pack) stays **empty**;
- rows >= 181 (multipliers x1..x12, icons, cards, arrows): from the Italian sheet already in the pack (`tools/data/card_icon03_base_it.png`);
- the European cells are pasted **only in their band** of rows (otherwise they spoil the top of the big digits).

Files: it -> `ui_it/duel_texts/basic_ii__card_icon03.png` (hash 376925c7); fr -> `upscale_extra/3e5482fd.png`; en ee0c44c3; de ffe309a6; es 859eea2b. Previews in `comparisons/icon03/`.

## B5. Title plate

`python tools/ui_textures/mystic_tomato_title.py it` generates 2 PNGs (`542eff79685c434d`, `705176739829dcf5`, tiles 18 and 19 of the 20-tile 128x64 backdrop `title_menu_i.ehp: main_title00001..00020`) with card 4930 in the language + the "version" wording + the flag, PT Sans Bold font: **"VERSIONE POMODORO MISTICO"**. The plate **is included only for the chosen language** (it lives in `modules/it/intro/title_screen/`); the original base pack has the tiles without a banner. Files in this pack: `ULES00600/intro/title_screen/00000000542eff79685c434d.png`, `ULES00600/intro/title_screen/00000000705176739829dcf5.png`.

## B6. `textures.ini` and composition

`tools/gen_ini.py TOOLS US_INI CARD_DIR OUT_INI i=it +extra_it.ini +ui_it.ini +data/upscale_extra.ini` converts the US `textures.ini` into the EU one: the non-card entries stay (neutral textures = same hashes); the card entries are regenerated from the EU `card/*.cip` archives for the 5 languages (`i=it` remaps `cards/large/X.png` -> `cards/large_it/X.png`); it adds the Spell/Trap label (`extra_it.ini`), the `ui_it` lines and `upscale_extra.ini`. It is also done for the 3 card styles. If the same pixels exist in several languages the first in `e i f g s` wins (for this reason atlas, banner and attribute table are "one per installation").

`ui_it` lines in `textures.ini`: 105. Prefix frequency: `docs/changes_it/ini_lines.csv`. Check: every `ui_it/...` line must point to an existing file and there must be no duplicate hashes.

## B7. Installation and settings

PC: copy `ULES00600` into `<PPSSPP>/PSP/TEXTURES/` (Android: `textures.zip` in `.../TEXTURES/ULES00600/`, without extracting it; regenerate the zip with the corrections). Settings: **Replace textures ON**, rendering resolution **4x**, game language = module language (the language is stored in the **save file**). After changing a single PNG it is enough to copy it and restart PPSSPP (cache). To try the texts use the `_definitiva` ISO.

---

# C. EDITORIAL CHOICES

- **Preside** (never "Cancelliere") for Sheppard, including "Ufficio del Preside" and "Profilo del Preside Sheppard".
- **Segna-Mostro** (not "Gettoni Mostro") in help, records and cards; `Segna-Opzione`.
- Banner: "direttore dello Slifer Rosso"; dormitories **Slifer Rosso, Ra Giallo, Obelisk Blu**; `Modalità Storia` is the menu name.
- Tab **Fusion** (not Fusione). `E'` -> `È`; `Life Point` -> `Life Points`; punctuation and apostrophes corrected.
- Censored scenes restored to the Japanese: sake/shochu and maid outfit (see below); "Beh, non sono poi così bravo..." (it was "sto sbavando").
- Number sheet: digits/LP from the US pack, x1..x12 from the Italian sheet, time word TEMPO.

### Entries of the choices register for this language (`tools/data/editorial_choices.json`)
| id | original | corrected | inherited | reason |
|---|---|---|---|---|
| st01_t01/Scr003E#146 | Mio padre possiede un'azienda che⏎produce salsa piccante. | La mia famiglia produce sake. | no | sake instead of hot sauce (faithful to the Japanese: Chumley's family makes sake) |
| st01_t01/Scr003E#147 | Mi ha mandato della salsa piccante⏎con la mia ultima paga.⏎Ti farò uno sconto ragionevole.⏎Vuoi... | L'altro giorno mi hanno mandato dello shochu⏎insieme ai soldi da casa, quindi la prossima volta... | no | shochu instead of hot sauce |
| st01_t01/Scr003E#150 | Mio padre possiede un'azienda che⏎produce salsa piccante. | None | yes | same as 146 |
| st01_t01/Scr003E#151 | Mi ha mandato della salsa piccante con la ⏎mia ultima paga.⏎Ti farò uno sconto ragionevole.⏎Vuoi... | L'altro giorno mi hanno mandato dello shochu⏎insieme ai soldi da casa, quindi la prossima volta... | no | same as 147 |
| st01_t01/Scr003E#163 | Wow, ce l'hai fatta sul serio.⏎È 《C026_2》...⏎E indossa un bikini! | Wow, ce l'hai fatta sul serio.⏎È 《C026_2》...⏎In abito da cameriera! | no | maid outfit instead of bikini (Japanese: メイド服) |
| st01_t01/Scr003E#168 | Wow, ce l'hai fatta sul serio.⏎È 《C026_2》...⏎E indossa un bikini! | None | yes | same as 163 |
| st01_t01/Scr003E#188 | Oddio, sto sbavando un po'... | Oddio, non sono un granché... | no | Italian only: "sto sbavando" was a translation error (Japanese: "I am not that good") |
| st01_t01/Scr003E#189 | Ehi, puoi farmi un disegno?⏎Disegnami 《C026_2》 in bikini! | Ehi, puoi farmi un disegno?⏎Disegnami 《C026_2》 vestita da cameriera! | no | maid outfit instead of bikini |
| st01_t01/Scr003E#191 | Ecco, usa questo! | Ecco, usa questo vestito da cameriera! | no | Syrus hands over a maid outfit as a model (メイド服): with the bikini the joke made no sense |
| st01_t01/Scr003E#194 | Oddio, sto sbavando un po'... | None | yes | same as 188 |
| st01_t01/Scr003E#195 | Ehi, puoi farmi un disegno?⏎Disegnami 《C026_2》 in bikini! | None | yes | same as 189 |
| st01_t01/Scr003E#197 | Ecco, usa questo! | Ecco, usa questo vestito da cameriera! | no | same as 191 |

Other choices and the re-reading of the duel sentences: `docs/EDITORIAL_CHOICES.md`.

# D. IN-GAME VERIFICATION

- Seen in game: Italian HD interface, rewritten long strings (help, cards, tutorial), Preside/Segna-Mostro terminology, HD cards and Spell/Trap label of the large card.
- **Not seen** after the latest changes: card re-reading (65 new cards), corrected duel sentences, "Fusion" tab, 4 dialogue box-length warnings (en/es/de #147/#151, de #172).

# E. HOW TO REGENERATE EVERYTHING

```
# ISO (all languages together)
python tools/corrections/build_dialogues.py it
python tools/corrections/generate_card_corrections.py it CARDINFO_it.ehp          # cards
python tools/corrections/apply_to_iso.py PSP/GAME/ULES00600_..._EUR.iso PSP/GAME/ULES00600_..._EUR_definitiva.iso
# images
sh tools/rebuild_corrections.sh USRDIR PACK_US PACK_MOD PYTHON
TF1_LANG=it python tools/ui_textures/<family>.py USRDIR PACK_US <module>      # for each of the 8 families (whole!)
python tools/ui_textures/icon03_languages.py --apply ; python tools/ui_textures/mystic_tomato_title.py it
python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules USRDIR/card OUT it --copy
# this document
python tools/analysis/document_changes.py ISO_ORIG ISO_DEF it docs/changes_it
python tools/analysis/document_pack.py ISO_ORIG it docs/changes_it
python tools/analysis/text_comparisons.py it
python tools/analysis/write_changes_document.py it
```
External inputs you need (check that they exist): the original ISO, the extracted USRDIR (`tools/analysis/extract_usrdir.py`), MikeyMK's US pack `ULUS10136` (in a folder outside the project).

# F. LIMITS AND OPEN POINTS

- Official card names: to be decided with the user. "Ragazza Mago Nero" vs "Maga Nera".
- The hand-written notes on the card re-reading before ~line 1830 were lost; for that stretch there is also an automatic scan (typos, spaces, apostrophes).
- Android `textures.zip` to be regenerated with the corrections; cards of the installed pack to be restarted in PPSSPP (cache).
- The speaker name in the dialogue box cannot be modified (encrypted EBOOT).
