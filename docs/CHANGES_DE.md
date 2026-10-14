# MODIFICHE PER LA VERSIONE POMODORO MISTICO IN TEDESCO

Documento **completo** di tutto cio' che la "Versione Pomodoro Mistico" cambia per il tedesco: (A) le modifiche **dirette alla ISO**, (B) il **texture pack** (com'e' fatto, cosa contiene, come si compone), (C) le scelte editoriali, (D) cosa e' verificato in gioco e cosa no, (E) come rigenerare tutto.

**Questo file e' generato** da `tools/analysis/write_changes_document.py de` a partire dai dati reali: confronto byte per byte tra la ISO originale `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` e la ISO corretta `..._definitiva.iso` (`document_changes.py`) e scansione del pack (`document_pack.py`). Gli elenchi riga per riga stanno in `docs/changes_de/*.csv` (separatore `;`, UTF-8 con BOM, a capo come `⏎`): sono la **lista esatta** di ogni cambiamento. Rigenera tutto dopo ogni modifica.

Per il metodo generale e per le altre lingue: `docs/NEW_LANGUAGE_GUIDE.md`; dettagli tecnici degli script: `TUTORIAL.md`; decisioni: `docs/EDITORIAL_CHOICES.md`; texture neutre/specifiche: `docs/TEXTURE_INVENTORY.md`.

## Indice
- A. Modifiche alla ISO: A1 panoramica · A2 carte · A3 dialoghi · A4 frasi dei duelli · A5 stringhe dell'interfaccia · A6 etichetta Magia/Trappola · A7 file toccati e dettagli tecnici · A8 cosa non si puo' cambiare
- B. Texture pack: B1 provenienza e struttura · B2 immagini delle carte · B3 interfaccia HD (`ui_de`) · B4 foglio numeri (`card_icon03`) · B5 targa del titolo · B6 textures.ini e composizione · B7 installazione
- C. Scelte editoriali · D. Verifica in gioco · E. Come rigenerare · F. Limiti e punti aperti

---

# A. MODIFICHE ALLA ISO

## A1. Panoramica

La ISO originale **non viene mai modificata**. `tools/corrections/apply_to_iso.py ISO_ORIG ISO_OUT [lingue]` ne crea una copia in cui alcuni archivi `.ehp` sono riscritti. Se un archivio cresce (testo piu' lungo) viene **rimesso in fondo alla ISO** in un nuovo settore e il suo voce nella directory ISO9660 viene riassegnata (`pycdlib`); la ISO `_definitiva` pesa per questo ~909 MB (l'originale ~761 MB). **Lanciarlo sempre senza elenco di lingue (o con tutte)**: con una lingua sola sovrascrive le altre.

| Cosa | Quantita' (derivata dal confronto ISO) | Dove sta il dato | File CSV |
|---|---|---|---|
| Carte con testo cambiato (nome e/o descrizione) | 258 carte (258 campi) | `tools/data/card_corrections_de.json` da `correzioni/rules_de.py` | cards.csv |
| Righe di dialogo della storia | 1649 righe | `tools/data/dialogue_touchups_de.json` (+ base) | dialogues.csv |
| Frasi dei duellanti nei duelli | 40 frasi uniche (66 voci in tutti gli archivi) | `tools/data/duel_line_corrections_de.json` | duel_lines.csv |
| Stringhe dell'interfaccia (aiuti, schede, record, tutorial, menu...) | 581 stringhe uniche (1426 voci, 55 archivi) | `correzioni/string_rules_de.py` + `dati/ui_texts.json` | ui_strings.csv |
| Immagini sostituite dentro la ISO | 6 (etichetta [CARTA MAGIA/TRAPPOLA] della carta grande) | `apply_to_iso.py` (copia `card_spell_trap.gim` della lingua) | iso_images.csv |
| File della ISO toccati (archivi `.ehp`) | 179 | - | touched_files.csv |
| Altre differenze tecniche (offset ricalcolati) | 254 | - | other.csv |

## A2. Testi delle carte

Archivio: `PSP_GAME/USRDIR/duelsys/cardinfo_fra.ehp` (tabelle `CARD_Name_*`, `CARD_Desc_*`, `CARD_Indx_*`). **258 carte** hanno nome e/o descrizione modificati. Si correggono **solo errori oggettivi** (refusi, accenti, apostrofi, spazi, maiuscole incoerenti, concordanze, plurali fissi, residui di altre lingue); nomi ufficiali e terminologia del gioco non si toccano.

Come: ogni carta e' stata letta (it: 2.479 testi, uno per uno; fr: audit contro database ufficiale + lettura). Regole in `tools/corrections/rules_de.py`: **18 regole globali** (regex applicate a nomi e descrizioni di tutte le carte) e **243 correzioni per carta** (`PER_CARTA`: id, campo, vecchio, nuovo, motivo; il vecchio testo deve esistere esattamente). `generate_card_corrections.py de CARDINFO` (scrive `card_corrections_{L}.json` partendo dai testi originali) produce il json; `apply_to_iso` lo scrive nella ISO; le immagini HD delle carte toccate si rigenerano (sezione B2).

### Regole globali (tutte)
| modello (regex) | sostituzione | motivo |
|---|---|---|
| \baugezeichneten\b | ausgezeichneten | refuso |
| \bausgestatte\b | ausgestattete | refuso |
| \benstanden\b | entstanden | refuso |
| \bsprirituelle\b | spirituelle | refuso |
| \bbeeinflußt\b | beeinflusst | ortografia: ss dopo vocale breve |
| \bAnulliere\b | Annulliere | refuso |
| \bZauberabsorbtion\b | Zauberabsorption | refuso (Absorption) |
| \bSchadensverrechnung\b | Schadensberechnung | terminologia del gioco: altrove "Schadensberechnung" |
| \bKartename\b | Kartenname | refuso |
| auf deiner Spielfeldseite ist, und dein Gegner keine | auf deiner Spielfeldseite ist und dein Gegner keine | virgola superflua (Toon-Karten) |
| dessen DEF niedriger sind als die ATK | dessen DEF niedriger ist als die ATK | concordanza (DEF e' singolare) |
| auf die Hand seines Besitzers zurück gegeben | auf die Hand seines Besitzers zurückgegeben | Zusammenschreibung |
| die Karte auf zu decken | die Karte aufzudecken | Zusammenschreibung |
| in der gleichen Höhe, wie die ursprüngliche ATK des Monsters, zu zufügen | in der gleichen Höhe wie die ursprüngliche ATK des Monsters zuzufügen | Zusammenschreibung e virgole |
| an Stelle 1 beliebigen Fusionsmaterial-Monsterkarte | an Stelle einer beliebigen Fusionsmaterial-Monsterkarte | articolo (come nelle altre carte) |
| \bJedesmal\b | Jedes Mal | ortografia |
| \bjedesmal\b | jedes Mal | ortografia |
| Spezialaktivierung | Spezialbeschwörung | traduzione: Special Summon (EN) non e' un'attivazione |

### Correzioni per carta (tutte)
| id | campo | vecchio | nuovo | motivo |
|---|---|---|---|---|
| 4452 | desc | Schanz | Schwanz | refuso (EN: tail) |
| 4667 | desc | uberprufen | überprüfen | dieresi sostituite da vocali semplici |
| 4667 | desc | nachsten | nächsten | dieresi sostituite da vocali semplici |
| 4667 | desc | Spielzugen | Spielzügen | dieresi sostituite da vocali semplici |
| 4667 | desc | zerstoren | zerstören | dieresi sostituite da vocali semplici |
| 4667 | desc | oder hoher | oder höher | dieresi sostituite da vocali semplici |
| 5575 | name | verrringern | verringern | refuso |
| 5824 | desc | Entfere | Entferne | refuso |
| 5829 | desc | Friehof | Friedhof | refuso |
| 5930 | desc | Verteidigungepsoition | Verteidigungsposition | refuso |
| 6085 | desc | enfernen | entfernen | refuso |
| 6133 | desc | Spielfeld , | Spielfeld, | spazio prima della virgola |
| 6168 | desc | aktiveren | aktivieren | refuso |
| 6368 | desc | enfernt | entfernt | refuso |
| 6542 | desc | Spezialbschwörung | Spezialbeschwörung | refuso |
| 6582 | desc | erhälst | erhältst | refuso |
| 6681 | desc | Enterne | Entferne | refuso |
| 6076 | desc | Fur jede | Für jede | dieresi sostituita da vocale semplice |
| 4017 | desc | Schwert ähnlicher Dornen | schwertähnlicher Dornen | Zusammenschreibung |
| 4035 | desc | rauhesten | rauesten | ortografia (come beeinflusst: ortografia riformata) |
| 4069 | desc | Dieses Karte | Diese Karte | concordanza |
| 4074 | desc | Ein Axt schwingende Ungeheuer-Krieger | Ein Axt schwingender Ungeheuer-Krieger | concordanza |
| 4172 | desc | Jedesmal | Jedes Mal | ortografia |
| 4208 | desc | Es greift an indem | Es greift an, indem | virgola |
| 4235 | desc | Macht anstatt das Leben | Macht, anstatt das Leben | virgola prima dell'infinitiva con anstatt |
| 4238 | desc | Waffe,die | Waffe, die | spazio dopo la virgola |
| 4239 | desc | Unterweltler, des angeblich | Unterweltler, der angeblich | refuso |
| 4258 | desc | Schönheit, zerkratzt sie | Schönheit zerkratzt sie | virgola superflua dopo il complemento iniziale |
| 4292 | desc | erschaffen nur um die Tore | erschaffen nur, um die Tore | virgola prima di um ... zu |
| 4312 | desc | ATK- Wert | ATK-Wert | spazio superfluo |
| 4373 | desc | Life Points, und greifst | Life Points und greifst | virgola superflua (stesso soggetto) |
| 4374 | desc | Erhöht sich die ATK dieser Karte um 100 Punkte für jede Monsterkarte im deinem Friedhof. | Die ATK dieser Karte erhöht sich um 100 Punkte für jede Monsterkarte in deinem Friedhof. | ordine delle parole (EN: Increase) e "im deinem" |
| 4398 | desc | kann per Spezialaktivierung vom Deck | kann als Spezialbeschwörung vom Deck | traduzione (EN: Special Summoned) |
| 4400 | desc | Typ Maschine ist, und den | Typ Maschine ist und den | virgola superflua |
| 4431 | desc | ab um bis zu 2 | ab, um bis zu 2 | virgola prima di um ... zu |
| 4496 | desc | Life Pointsn | Life Points | refuso |
| 4506 | desc | als einer Normalbeschwörung oder Flippbeschwörung | als Normalbeschwörung oder Flippbeschwörung | grammatica |
| 4512 | desc | FusionsDeck | Fusionsdeck | maiuscola (come altrove: Fusionsdeck) |
| 4522 | desc | erhöht sich die ATK und DEF dieser Karte | erhöhen sich ATK und DEF dieser Karte | concordanza (plurale) |
| 4541 | desc | Ein Menschen ähnlicher Mantis | Eine menschenähnliche Mantis | genere e Zusammenschreibung |
| 4574 | desc | Ein Menschen ähnlicher Dinosaurier | Ein menschenähnlicher Dinosaurier | Zusammenschreibung |
| 4576 | desc | Eine getigerter Drache | Ein getigerter Drache | concordanza |
| 4596 | desc | riesigen Rüssel | riesigen Schnabel | traduzione (EN: beak; nome: Schnabelschlange) |
| 4609 | desc | Eine schöner und starker | Ein schöner und starker | concordanza |
| 4622 | desc | „Flipp“-Aktivierung), sind ATK- und DEF-Werte | „Flipp“-Aktivierung) sind die ATK- und DEF-Werte | virgola superflua e articolo |
| 4022 | desc | soviel Schaden wie | so viel Schaden wie | ortografia |
| 4738 | desc | soviel Schaden zuzufügen | so viel Schaden zuzufügen | ortografia |
| 4652 | desc | härter ist als er aussieht | härter ist, als er aussieht | virgola |
| 4654 | desc | durch sein Vorwärtsstürzen | durch ihr Vorwärtsstürzen | concordanza (die Maschine) |
| 4660 | desc | erhöht seinen ATK neben 700 Punkten | erhöht seine ATK um 700 Punkte | traduzione (EN: increases its ATK by 700) |
| 4664 | desc | Wenn ein mit dieser Karte ausgerüstetes Monster angegriffen wird, kannst du seinen ATK-Wert um die Hälfte des ATK-Werts des Angegriffenen erhöhen. | Wenn ein mit dieser Karte ausgerüstetes Monster angreift, kannst du seinen ATK-Wert um die Hälfte des ATK-Werts des angegriffenen Monsters erhöhen. | traduzione (EN: When attacking with a monster equipped with this card) |
| 4687 | desc | Spezialbeschwörung) eine DEF | Spezialbeschwörung), eine DEF | virgola che chiude la relativa |
| 4688 | desc | Spezialbeschwörung) eine ATK | Spezialbeschwörung), eine ATK | virgola che chiude la relativa |
| 4691 | desc | mehr als 2000 Punkte sind | mehr als 2000 Punkte beträgt | concordanza |
| 4692 | desc | auf der Angriffsposition | in Angriffsposition | grammatica |
| 4694 | desc | statt dessen | stattdessen | ortografia |
| 4748 | desc | spezialaktiviert werden | als Spezialbeschwörung beschworen werden | traduzione (EN: Special Summoned) |
| 4750 | desc | maximal einen Zauberzählmarke | maximal eine Zauberzählmarke | genere |
| 4750 | desc | den Zauberzählmarke | die Zauberzählmarke | genere |
| 4755 | desc | aktiviert wird (ohne Spezialaktivierung) | beschworen wird (ohne Spezialbeschwörung) | traduzione (EN: summoned) |
| 4795 | desc | aktiviert wird (einschließlich Spezialaktivierung) | beschworen wird (einschließlich Spezialbeschwörung) | traduzione (EN: Summoned) |
| 4780 | desc | Kampf mit ein Monster der Stufe 7 oder niedriger zerstört. | Kampf mit einem Monster der Stufe 7 oder niedriger zerstört werden. | grammatica |
| 4803 | desc | des Spielzugs in dem diese | des Spielzugs, in dem diese | virgola |
| 4804 | desc | Monster deines Gegner angreift | Monster deines Gegners angreift | refuso |
| 4814 | desc | deines Gegners nachdem du diese Karte aktiviert hast, kann | deines Gegners, nachdem du diese Karte aktiviert hast, kann | virgola |
| 4817 | desc | Diese Monster kann | Dieses Monster kann | concordanza |
| 4830 | desc | keine Monster aktivieren (einschließlich „Flipp“- und Spezialaktivierung) | keine Monster beschwören (einschließlich „Flipp“- und Spezialbeschwörung) | traduzione (EN: summon) |
| 4834 | desc | Am Ende der Battle Phase, gib | Am Ende der Battle Phase gib | virgola |
| 4855 | desc | Wenn Dein Gegner | Wenn dein Gegner | maiuscola |
| 4861 | desc | Normal-, Flipp, oder Spezialbeschwörung | Normal-, Flipp- oder Spezialbeschwörung | trattino e virgola |
| 4861 | desc | das Beschworene Monster | das beschworene Monster | maiuscola |
| 4892 | desc | statt dessen | stattdessen | ortografia |
| 4944 | desc | Permante Zauberkarte | Permanente Zauberkarte | refuso |
| 5030 | desc | beschwöre dieses Karte | beschwöre diese Karte | concordanza |
| 5033 | desc | ATK und DEF dieses Monster zu 1000 | ATK und DEF dieses Monsters zu 1000 | genitivo |
| 5042 | desc | Jedesmal | Jedes Mal | ortografia |
| 5067 | desc | Nach der Schadensberechnung, verringere | Nach der Schadensberechnung verringere | virgola |
| 5113 | desc | Jedesmal | Jedes Mal | ortografia |
| 5197 | desc | Jedesmal | Jedes Mal | ortografia |
| 5164 | desc | jedesmal | jedes Mal | ortografia |
| 5116 | desc | Die Spielsteine | Die Spielmarken | terminologia (Spielmarke) |
| 5129 | desc | Während deiner End Phase, zerstöre | Während deiner End Phase zerstöre | virgola |
| 5142 | desc | dessen DEF niedriger sind als | dessen DEF niedriger ist als | concordanza |
| 5173 | desc | geschickt wird während sie verdeckt liegt, dann wird deinem Gegner 500 Punkte Schaden an seiner LP verursacht. | geschickt wird, während sie verdeckt liegt, dann werden deinem Gegner 500 Punkte Schaden an seinen LP verursacht. | virgola e concordanza |
| 5175 | desc | auf 3000 gesetzt solange | auf 3000 gesetzt, solange | virgola |
| 5177 | desc | wird ein „Jungfernmarke“ getan | wird eine „Jungfernmarke“ getan | genere |
| 5178 | desc | mit einem „Jungfernmarke“ darauf | mit einer „Jungfernmarke“ darauf | genere |
| 5178 | desc | das ausgerüstet Monster | das ausgerüstete Monster | concordanza |
| 5179 | desc | seines Angriffs, eine aufgedeckte | seines Angriffs eine aufgedeckte | virgola superflua |
| 5180 | desc | die ATK des anderen Monster. | die ATK des anderen Monsters. | genitivo |
| 5181 | desc | auf dem Spielfeld deines Feldes | auf der Spielfeldseite deines Gegners | traduzione (EN: opponent's side of the field) |
| 5182 | desc | um 600 erhöht Jedesmal, | um 600 erhöht. Jedes Mal, | punto mancante e ortografia |
| 5182 | desc | bezahlen um am Ende | bezahlen, um am Ende | virgola |
| 5185 | desc | zugefügt wird der die Karte kontrolliert | zugefügt wird, der die Karte kontrolliert | virgola |
| 5189 | desc | Life Points um eine Karte | Life Points, um eine Karte | virgola |
| 5189 | desc | drei Mal benutzt hast, dann erhält | drei Mal benutzt hast, erhält | sintassi |
| 5190 | desc | ab.  Wähle ein 1 Monster | ab. Wähle 1 Monster | doppio spazio e "ein 1" |
| 5202 | desc | gelegt wurden, unter dein Deck | gelegt wurde, unter dein Deck | concordanza |
| 5223 | desc | Nur der „Dunkler Magier“ oder die „Dunkles Magier-Mädchen“ darf | Nur „Dunkler Magier“ oder „Dunkles Magier-Mädchen“ darf | articoli errati davanti ai nomi |
| 5239 | desc | Regelgzwecken | Regelzwecken | refuso |
| 5242 | desc | wenn sich der „Kathedrale der Adligen“ | wenn sich die „Kathedrale der Adligen“ | genere |
| 5260 | desc | im Spielzugs deines Gegners | im Spielzug deines Gegners | caso |
| 5263 | desc | bestimmt, und zerstört die Zauberkarte | bestimmt, und zerstöre die Zauberkarte | modo imperativo (come tutto il testo) |
| 5275 | desc | zurück ihn ihre ursprüngliche | zurück in ihre ursprüngliche | refuso |
| 5286 | desc | mit allen seiner Monster | mit allen seinen Monstern | caso |
| 5290 | desc | jede zerstöre Zauberkarte | jede zerstörte Zauberkarte | refuso |
| 5295 | desc | Beherscher | Beherrscher | refuso |
| 5295 | desc | aus einen Kampf | aus einem Kampf | caso |
| 5299 | desc | Gibt das als Ziel bestimmte Monster | Gib das als Ziel bestimmte Monster | modo imperativo |
| 5313 | desc | genau soviel Stufen haben wie | genauso viele Stufen haben wie | ortografia |
| 5334 | desc | dessen DEF niedriger sind als | dessen DEF niedriger ist als | concordanza |
| 5351 | desc | wähle 2 Karte im Friedhof | wähle 2 Karten im Friedhof | plurale |
| 5384 | desc | beschworen wurde Zusätzlich | beschworen wurde. Zusätzlich | punto mancante |
| 5433 | desc | Standby Phase deines Gegner so | Standby Phase deines Gegners so | genitivo |
| 5453 | desc | wird der ATK dieser Karte | wird die ATK dieser Karte | genere |
| 5452 | desc | dessen DEF niedriger sind als | dessen DEF niedriger ist als | concordanza |
| 5452 | desc | Life Points deines Gegner als | Life Points deines Gegners als | genitivo |
| 5477 | desc | als Tribut an um den Life Points | als Tribut an, um den Life Points | virgola |
| 5479 | desc | Ziehe Karten bis du | Ziehe Karten, bis du | virgola |
| 5482 | desc | in der entsprechenden Spielzug | in dem entsprechenden Spielzug | caso |
| 5499 | desc | bleibt bestehen bis die | bleibt bestehen, bis die | virgola |
| 5531 | desc | Life Points deines Gegner Schaden | Life Points deines Gegners Schaden | genitivo |
| 5530 | desc | Stufe hat wie dein Gegner genannt hat | Stufe hat, wie dein Gegner genannt hat | virgola |
| 5546 | desc | zu sein Deck hinzu | zu seinem Deck hinzu | caso |
| 5546 | desc | von seinem Deck wie er vorher in sein Deck zurück gelegt hat | von seinem Deck, wie er vorher in sein Deck zurückgelegt hat | virgola e Zusammenschreibung |
| 5574 | desc | Diese „Klon-Spielmarken“ hat | Diese „Klon-Spielmarke“ hat | concordanza |
| 5574 | desc | das gleiche Eigenschaft | die gleiche Eigenschaft | genere |
| 5604 | desc | Battle Phase kannst diesen Effekt | Battle Phase kannst du diesen Effekt | pronome mancante |
| 5608 | desc | auf die Hand zurück gegeben | auf die Hand zurückgegeben | Zusammenschreibung |
| 5608 | desc | werden beide gewählte Karten | werden beide gewählten Karten | declinazione |
| 5614 | desc | Karte vergangen sind. | Karte vergangen sind, zu. | verbo separabile mancante (zufügen) |
| 5676 | desc | oben auf sein Deck zurück | oben auf dein Deck zurück | pronome (sein/dein) |
| 5678 | desc | deines Gegners niedriger als die DEF | deines Gegners niedriger ist als die DEF | verbo mancante |
| 5689 | desc | Kampf mit der diese Spielmarke werden | Kampf mit dieser Spielmarke werden | refuso |
| 5689 | desc | wird die diese Spielmarke zerstört | wird diese Spielmarke zerstört | refuso |
| 5699 | desc | Während der Schadensberechnung, erhöhe | Während der Schadensberechnung erhöhe | virgola |
| 5754 | desc | in deiner Hand ist, kannst du sie | in deiner Hand hast, kannst du sie | verbo (EN: if you have) |
| 5755 | desc | Der DEF dieses Monsters | Die DEF dieses Monsters | genere |
| 5784 | desc | soviele Stufen wie | so viele Stufen wie | ortografia |
| 5788 | desc | dieser Karte, gewinnst du | dieser Karte gewinnst du | virgola |
| 5815 | desc | niedriger sind als die DEF dieses Monsters | niedriger ist als die DEF dieses Monsters | concordanza |
| 5817 | desc | indem Du 2 FINSTERNIS Monster in deinem Friedhof aus dem Spiel entfernt. | indem du 2 FINSTERNIS Monster in deinem Friedhof aus dem Spiel entfernst. | persona del verbo e maiuscola |
| 5818 | desc | auf die Hand ihres Besitzers. | auf die Hand ihres Besitzers zurück. | verbo mancante (EN: return) |
| 5824 | desc | als diese Karte aus dem Spiel zu entfernen. | als diese Karte zu zerstören. | traduzione (EN: destroy) |
| 5828 | desc | gegnerischen um Spielzugs 300 Punkte | gegnerischen Spielzugs um 300 Punkte | ordine delle parole |
| 5830 | desc | aus dem Spiel entfernt wird. Falls diese Karte | aus dem Spiel entfernt werden. Falls diese Karte | concordanza |
| 5830 | desc | des nächsten Spielzug deines Gegners | des nächsten Spielzugs deines Gegners | genitivo |
| 5836 | desc | erhöhen dein Gegner 700 Punkte Schaden | erhält dein Gegner 700 Punkte Schaden | verbo (EN: inflict) |
| 5843 | desc | auf Deiner Hand | auf deiner Hand | maiuscola |
| 5844 | desc | keine Zauberkarte in deinem Friedhof befinden | keine Zauberkarte in deinem Friedhof befindet | concordanza |
| 5854 | desc | erhält diese Karte einen Zauberzählmarke | erhält diese Karte eine Zauberzählmarke | genere |
| 5854 | desc | Wenn der 4. Zauberzählmarke | Wenn die 4. Zauberzählmarke | genere |
| 5854 | desc | eine Zauberkarte aktiviert hat, erhält | eine Zauberkarte aktiviert, erhält | concordanza |
| 5854 | desc | Zauberkarte aktiviert hat erhält 3000 | Zauberkarte aktiviert hat, erhält 3000 | virgola |
| 5860 | desc | beschworen werden indem, 1 LICHT | beschworen werden, indem 1 LICHT | virgola |
| 5860 | desc | Zahle 1000 Life Points um alle | Zahle 1000 Life Points, um alle | virgola |
| 5871 | desc | verlor seine Herz | verlor sein Herz | genere |
| 5884 | desc | eines gegnerischen in Verteidigungsposition liegendes Monster angreift | eines gegnerischen, in Verteidigungsposition liegenden Monsters angreift | caso |
| 5895 | desc | auf den Friedhof um alle Karten auf dem Spielfeld, außer dieser Karte, zu auf den Friedhof zu legen. | auf den Friedhof, um alle Karten auf dem Spielfeld, außer dieser Karte, zu zerstören. | traduzione (EN: destroy) e sintassi |
| 5896 | desc | als Tribut an um 1 Zauber- oder Fallenkarte | als Tribut an, um 1 Zauber- oder Fallenkarte | virgola |
| 5897 | desc | Solange „Umi“ offen auf dem Spielfeld befindet | Solange sich „Umi“ offen auf dem Spielfeld befindet | pronome riflessivo mancante |
| 5912 | desc | auf deiner Spielfeldseite um den Life Points | auf deiner Spielfeldseite, um den Life Points | virgola |
| 5922 | desc | offen auf auf dem Spielfeld | offen auf dem Spielfeld | parola doppia |
| 5943 | desc | Würfelergebnis solange die Karte | Würfelergebnis, solange die Karte | virgola |
| 5987 | desc | auf dem Spielfeld werden bis zum Ende dieses Spielzugs zu 0. | auf dem Spielfeld wird bis zum Ende dieses Spielzugs zu 0. | concordanza (DEF singolare) |
| 6001 | desc | nicht Spezialbeschworen werden | nicht spezialbeschworen werden | minuscola |
| 6048 | desc | des ausgerüsteten Monster um 1000 | des ausgerüsteten Monsters um 1000 | genitivo |
| 6066 | desc | deiner normalen Monstern der Stufe | deiner normalen Monster der Stufe | genitivo plurale |
| 6076 | desc | erhöht sich der ATK dieser Karte | erhöht sich die ATK dieser Karte | genere |
| 6097 | desc | diese offene Karten auf den Friedhof | diese offene Karte auf den Friedhof | numero |
| 6133 | desc | auf deiner Spielfeld, dessen | auf deiner Spielfeldseite, dessen | parola troncata (dopo la regola dello spazio) |
| 6158 | desc | Diese Spielmarke können nicht | Diese Spielmarken können nicht | concordanza |
| 6166 | desc | annuliere die Effekt von allen | annuliere die Effekte von allen | plurale |
| 6167 | desc | Falls 5 Zauberzählmarke auf | Falls 5 Zauberzählmarken auf | plurale |
| 6167 | desc | mit 5 Zauberzählmarke auf den Friedhof | mit 5 Zauberzählmarken auf den Friedhof | plurale |
| 6168 | desc | mit einem ATK von 2000 oder weniger | mit einer ATK von 2000 oder weniger | genere |
| 6234 | desc | durch die Welt wandernd um der stärkste | durch die Welt wandernd, um der stärkste | virgola |
| 6234 | desc | Sei vorsichtig ihn nicht zu berühren, oder | Sei vorsichtig, ihn nicht zu berühren, oder | virgola |
| 6244 | desc | In diesem Fall, wird die Grund-ATK | In diesem Fall wird die Grund-ATK | virgola |
| 6249 | desc | in den Friedhof gelegt wird, fügen den Life Points beider Spieler | in den Friedhof gelegt wird, füge den Life Points beider Spieler | modo imperativo |
| 6250 | desc | Zauberzählmarken um ein offenes Monster | Zauberzählmarken, um ein offenes Monster | virgola |
| 6254 | desc | wird, gebe 1 Monster | wird, gib 1 Monster | modo imperativo |
| 6262 | desc | in den Friedhof um 2 Monster | in den Friedhof, um 2 Monster | virgola |
| 6262 | desc | Die Monster die auf diese Weise | Die Monster, die auf diese Weise | virgola |
| 6282 | desc | Spielfeldseite um diese Karte zu aktivieren | Spielfeldseite, um diese Karte zu aktivieren | virgola |
| 6285 | desc | als Tribut an um diese Karte zu aktivieren | als Tribut an, um diese Karte zu aktivieren | virgola |
| 6287 | desc | Spezialbeschwörung wieder auf dein Feld zu bringen. | Spezialbeschwörung wieder auf dein Feld bringen. | sintassi |
| 6287 | desc | wird ihr ATK um 500 Punkte erhöht | wird ihre ATK um 500 Punkte erhöht | genere |
| 6293 | desc | Friedhof ab um 1 Monster vom Typ Zombie | Friedhof ab, um 1 Monster vom Typ Zombie | virgola |
| 6293 | desc | mit einem niedrigeren Stufe | mit einer niedrigeren Stufe | genere |
| 6303 | desc | und nehme sie auf deine Hand | und nimm sie auf deine Hand | modo imperativo |
| 6308 | desc | es sei denn du zahlst | es sei denn, du zahlst | virgola |
| 6320 | desc | Monster vom Typ Fels die vom Spiel entfernten wurden | Monster vom Typ Fels, die aus dem Spiel entfernt wurden | sintassi |
| 6324 | desc | Die Grund-ATK und -DEF dieser Karte wird zur Anzahl | Die Grund-ATK und -DEF dieser Karte werden zur Anzahl | concordanza |
| 6343 | desc | Das Eigenschaft dieser Karte | Die Eigenschaft dieser Karte | genere |
| 6344 | desc | ATK des zerstörten Monster zu | ATK des zerstörten Monsters zu | genitivo |
| 6345 | desc | mit geringeren Grund-ATK als die ATK dieser Karte | mit geringerer Grund-ATK als die ATK dieser Karte | concordanza |
| 6346 | desc | des Spielzuges in dem diese Karte | des Spielzugs, in dem diese Karte | virgola |
| 6354 | desc | Zahle 300 Life Points um die verdeckten | Zahle 300 Life Points, um die verdeckten | virgola |
| 6355 | desc | auf deiner Spielfeldseite um diese Karte zu aktivieren | auf deiner Spielfeldseite, um diese Karte zu aktivieren | virgola |
| 6359 | desc | diese gesetzte Karte zerstört 1000 | diese gesetzte Karte zerstört, 1000 | virgola |
| 6376 | desc | auf den Friedhof um alle Karten, außer dieser Karte, in den Händen | auf den Friedhof, um alle Karten, außer dieser Karte, in den Händen | virgola |
| 6399 | desc | seine ATK niedriger sind als die ATK des Ziels | seine ATK niedriger ist als die ATK des Ziels | concordanza |
| 6400 | desc | in deiner Haupt Phase | in deiner Main Phase | terminologia (Main Phase) |
| 6400 | desc | eines Level 4 Monsters | eines Monsters der Stufe 4 | inglese residuo (Level) |
| 6409 | desc | Effekt 3 mal benutzt | Effekt dreimal benutzt | ortografia |
| 6410 | desc | werden die die folgenden Effekte | werden die folgenden Effekte | parola doppia |
| 6414 | desc | Die ATK von 1 offenen Monster auf dem Spielfeld werden bis zur End Phase | Die ATK von 1 offenen Monster auf dem Spielfeld wird bis zur End Phase | concordanza |
| 6427 | desc | Die Grund-ATK dieser Karte werden zur Anzahl | Die Grund-ATK dieser Karte wird zur Anzahl | concordanza |
| 6438 | desc | Würfel 3 mal | Würfel dreimal | ortografia |
| 6450 | desc | verhindern, das irgendwelche | verhindern, dass irgendwelche | dass/das |
| 6454 | desc | darfst die Effekte von Zauber-, Fallen und Effektmonsterkarten durch das Ablegen einer Karte vom gleichen Typ, unterbrechen | darfst du die Effekte von Zauber-, Fallen- und Effektmonsterkarten durch das Ablegen einer Karte vom gleichen Typ unterbrechen | pronome mancante e punteggiatura |
| 6500 | desc | Schaden zu, jedes Mal wenn du | Schaden zu, jedes Mal, wenn du | virgola |
| 6505 | desc | Spielfeldseite deines Gegner wählen | Spielfeldseite deines Gegners wählen | genitivo |
| 6522 | desc | Keiner der Spieler kann als Fusionsbeschwörungen beschwören. | Keiner der Spieler kann Fusionsbeschwörungen durchführen. | sintassi |
| 6524 | desc | kleiner oder gleich den ATK des ausgerüsteten Monsters sind | kleiner oder gleich der ATK des ausgerüsteten Monsters ist | concordanza |
| 6530 | desc | Schaden zu, jedes Mal wenn ein Spieler | Schaden zu, jedes Mal, wenn ein Spieler | virgola |
| 6541 | desc | ziehe soviele Karten | ziehe so viele Karten | ortografia |
| 6543 | desc | Fallenkarteneffekts der Schaden zufügt | Fallenkarteneffekts, der Schaden zufügt | virgola |
| 6550 | desc | die durch diesen Effekt zerstört wird, erhöht sich der ATK dieser Karte | die durch diesen Effekt aus dem Spiel entfernt wird, erhöht sich die ATK dieser Karte | traduzione (EN: removed from play) e genere |
| 6569 | desc | gleich oder höher als die ATK dieser Karte sind. | gleich oder höher als die ATK dieser Karte ist. | concordanza |
| 6571 | desc | werden die ATK des gewählten Monsters halbiert | wird die ATK des gewählten Monsters halbiert | concordanza |
| 6582 | desc | dessen ATK kleiner oder gleich dem Kampfschaden sind | dessen ATK kleiner oder gleich dem Kampfschaden ist | concordanza |
| 6589 | desc | Monster deines Gegner diese | Monster deines Gegners diese | genitivo |
| 6610 | desc | Wenn diese verdeckt Karte | Wenn diese verdeckte Karte | declinazione |
| 6617 | desc | kann benutzt werde, um | kann benutzt werden, um | refuso |
| 6637 | desc | und das gleiche Eigenschaft wie | und die gleiche Eigenschaft wie | genere |
| 6638 | desc | in der Runde, in der es spezialbeschworen wurde | in der Runde, in der sie spezialbeschworen wurde | concordanza |
| 6639 | desc | Das Eigenschaft dieser Karte | Die Eigenschaft dieser Karte | genere |
| 6639 | desc | Wenn dieser Karte erfolgreich Fusions beschworen werden, dann werden alle | Wenn diese Karte erfolgreich fusionsbeschworen wird, werden alle | grammatica |
| 6639 | desc | mit den gleichen Attributen, steigt der ATK dieser hier um 300 Punkte | mit der gleichen Eigenschaft steigt die ATK dieser Karte um 300 Punkte | grammatica |
| 6642 | desc | verdoppele allen Kampfschaden | verdopple allen Kampfschaden | imperativo (come nelle altre carte) |
| 6654 | desc | Diese Spielmarke können nicht | Diese Spielmarken können nicht | concordanza |
| 6661 | desc | auf deiner Spielfeldseite, nicht zerstört werden | auf deiner Spielfeldseite nicht zerstört werden | virgola superflua |
| 6664 | desc | höher als die ATK dieser Karte sind, kann | höher als die ATK dieser Karte ist, kann | concordanza |
| 6688 | desc | als Normalbeschwörung beschwören ohne ein Monster | als Normalbeschwörung beschwören, ohne ein Monster | virgola |
| 6722 | desc | zerstöre alle die Monster | zerstöre alle Monster | articolo superfluo |
| 6736 | desc | deiner Hand hingefügt wird | deiner Hand hinzugefügt wird | refuso |
| 6758 | desc | seine ATK kleiner sind als die ATK des Angriffsziels | seine ATK kleiner ist als die ATK des Angriffsziels | concordanza |
| 6815 | desc | auf den Friedhof geschickt wird während sie sich in deiner Zauber- & Fallenkartezone befindet | auf den Friedhof geschickt wird, während sie sich in deiner Zauber- & Fallenkartenzone befindet | virgola e refuso |
| 6410 | desc | ●Zauber : die | ●Zauber: die | spazio prima dei due punti |
| 6410 | desc | ●Falle : wähle | ●Falle: wähle | spazio prima dei due punti |
| 6410 | desc | ●Effektmonster : wähle | ●Effektmonster: wähle | spazio prima dei due punti |

### Elenco completo delle carte cambiate
**Confronto completo originale -> nuovo con le parole cambiate evidenziate: `docs/changes_de/cards_diff.md`** (tutte le 258 voci). Dati grezzi: `docs/changes_de/cards.csv`. Prime 40 righe:

| id | nome originale | campo | originale | nuovo |
|---|---|---|---|---|
| 4017 | Schwertdorndrache | desc | Mit einem Körper voller Schwert ähnlicher Dornen wagt nichts und niemand, sich diesem geladenen Monster in den Weg zu stellen. | Mit einem Körper voller schwertähnlicher Dornen wagt nichts und niemand, sich diesem geladenen Monster in den Weg zu stellen. |
| 4022 | Zeitzauberer | desc | Wirf eine Münze und wähle Kopf oder Zahl. Falls du richtig vorausgesagt hast, zerstöre alle Monster auf der Spielfeldseite deines Gegners. Wenn du falsch vorausgesagt hast, zerstöre alle Monster auf deiner Spielfeldseite und deine Life Points erhalten soviel Schaden wie die Hälfte der addierten ATK aller zerstörten Monster beträgt. Du kannst diese Karte nur in deinem Zug aktivieren und nur einmal pro Zug. | Wirf eine Münze und wähle Kopf oder Zahl. Falls du richtig vorausgesagt hast, zerstöre alle Monster auf der Spielfeldseite deines Gegners. Wenn du falsch vorausgesagt hast, zerstöre alle Monster auf deiner Spielfeldseite und deine Life Points erhalten so viel Schaden wie die Hälfte der addierten ATK aller zerstörten Monster beträgt. Du kannst diese Karte nur in deinem Zug aktivieren und nur einmal pro Zug. |
| 4031 | Hornkobold | desc | Ein kleiner Kobold, der in der Dunkelheit lauert und den sein Horn zu einem augezeichneten Gegner macht. | Ein kleiner Kobold, der in der Dunkelheit lauert und den sein Horn zu einem ausgezeichneten Gegner macht. |
| 4035 | Bergkrieger | desc | Ein harter Kämpfer, der sich auch auf dem rauhesten Terrain geschickt bewegen kann. | Ein harter Kämpfer, der sich auch auf dem rauesten Terrain geschickt bewegen kann. |
| 4069 | Harpyien-Schwestern | desc | Dieses Karte kann nicht als Normalbeschwörung beschworen oder gesetzt werden. Diese Karte kann nur durch den Effekt von „Vornehmer Egotist“ als Spezialbeschwörung beschworen werden. | Diese Karte kann nicht als Normalbeschwörung beschworen oder gesetzt werden. Diese Karte kann nur durch den Effekt von „Vornehmer Egotist“ als Spezialbeschwörung beschworen werden. |
| 4074 | Garoozis | desc | Ein Axt schwingende Ungeheuer-Krieger mit dem Kopf eines Drachen. | Ein Axt schwingender Ungeheuer-Krieger mit dem Kopf eines Drachen. |
| 4124 | Helfer im Schatten | desc | Eine niedliche kleine Elfe, die sich im Schatten verbirgt und sprirituelle Unterstützung leistet. | Eine niedliche kleine Elfe, die sich im Schatten verbirgt und spirituelle Unterstützung leistet. |
| 4172 | Mysteriöser Puppenspieler | desc | Jedesmal, wenn du oder dein Gegner ein Monster als Normal- oder Flippbeschwörung beschwören, erhöhe deine Life Points um 500 Punkte. | Jedes Mal, wenn du oder dein Gegner ein Monster als Normal- oder Flippbeschwörung beschwören, erhöhe deine Life Points um 500 Punkte. |
| 4208 | Erzunterweltler Murmeltier der Ruchlosigkeit | desc | Ein Luft-Murmeltier, das ein ruchloses Horn und Flügel hat. Es greift an indem es Eicheln wirft. | Ein Luft-Murmeltier, das ein ruchloses Horn und Flügel hat. Es greift an, indem es Eicheln wirft. |
| 4235 | Sanduhr des Lebens | desc | Diese Kreatur verleiht Macht anstatt das Leben zu verkürzen. | Diese Kreatur verleiht Macht, anstatt das Leben zu verkürzen. |
| 4238 | Madschinn-Gewehr | desc | Eine lebende Waffe,die Projektile spuckt. | Eine lebende Waffe, die Projektile spuckt. |
| 4239 | Dunkler Terrortitan | desc | Ein Unterweltler, des angeblich in der Traumwelt lebt und seine Feinde in ihrem Schlaf angreift. | Ein Unterweltler, der angeblich in der Traumwelt lebt und seine Feinde in ihrem Schlaf angreift. |
| 4258 | Nekogal #1 | desc | Eine weibliche Fee. Im Gegensatz zu ihrer lieblichen Schönheit, zerkratzt sie ihre Feinde. | Eine weibliche Fee. Im Gegensatz zu ihrer lieblichen Schönheit zerkratzt sie ihre Feinde. |
| 4292 | Torwärter | desc | Ein unzerstörbarer Mechanoid, erschaffen nur um die Tore zu bewachen. | Ein unzerstörbarer Mechanoid, erschaffen nur, um die Tore zu bewachen. |
| 4312 | Panzerinsekt mit Laserkanone | desc | Ein mit dieser Karte ausgerüstetes Monster vom Typ Insekt erhöht seinen ATK- Wert um 700 Punkte. | Ein mit dieser Karte ausgerüstetes Monster vom Typ Insekt erhöht seinen ATK-Wert um 700 Punkte. |
| 4373 | Jirai Gumo | desc | Wenn du mit dieser Karte angreifst, musst du eine Münze werfen und dich für Kopf oder Zahl entscheiden. Falls du richtig vorausgesagt hast, greifst du normal an. Wenn du falsch vorausgesagt hast, verlierst du die Hälfte deiner Life Points, und greifst dann an. | Wenn du mit dieser Karte angreifst, musst du eine Münze werfen und dich für Kopf oder Zahl entscheiden. Falls du richtig vorausgesagt hast, greifst du normal an. Wenn du falsch vorausgesagt hast, verlierst du die Hälfte deiner Life Points und greifst dann an. |
| 4374 | Schatten-Leichenfledderer | desc | Erhöht sich die ATK dieser Karte um 100 Punkte für jede Monsterkarte im deinem Friedhof. | Die ATK dieser Karte erhöht sich um 100 Punkte für jede Monsterkarte in deinem Friedhof. |
| 4398 | Metallzoa | desc | Dieses Monster kann per Spezialaktivierung vom Deck auf das Spielfeld gebracht werden, indem die mit einem „Zoa“ ausgestattete „Metallwandler“ als Tribut entrichtet wird. | Dieses Monster kann als Spezialbeschwörung vom Deck auf das Spielfeld gebracht werden, indem die mit einem „Zoa“ ausgestattete „Metallwandler“ als Tribut entrichtet wird. |
| 4400 | Stahlskorpion | desc | Ein Monster, das nicht vom Typ Maschine ist, und den „Stahlskorpion“ angreift, wird in der End Phase des zweiten gegnerischen Zugs nach diesem Angriff zerstört. | Ein Monster, das nicht vom Typ Maschine ist und den „Stahlskorpion“ angreift, wird in der End Phase des zweiten gegnerischen Zugs nach diesem Angriff zerstört. |
| 4420 | Schaufelbrecher | desc | Dieses mit einem Paar Schaufeln ausgestatte Monster zerstört alles, was sich ihm in den Weg stellt. | Dieses mit einem Paar Schaufeln ausgestattete Monster zerstört alles, was sich ihm in den Weg stellt. |
| 4431 | Donnerdrache | desc | Wirf diese Karte aus deiner Hand ab um bis zu 2 „Donnerdrache“-Karten aus deinem Deck deiner Hand hinzuzufügen. Mische dein Deck anschließend. Du kannst diesen Effekt nur während deiner Main Phase benutzen. | Wirf diese Karte aus deiner Hand ab, um bis zu 2 „Donnerdrache“-Karten aus deinem Deck deiner Hand hinzuzufügen. Mische dein Deck anschließend. Du kannst diesen Effekt nur während deiner Main Phase benutzen. |
| 4452 | Wasserschlange | desc | Dieses Monster hypnotisiert einen Gegner mit Hilfe des Balls auf seinem Schanz und zerrt ihn in sein nasses Verderben. | Dieses Monster hypnotisiert einen Gegner mit Hilfe des Balls auf seinem Schwanz und zerrt ihn in sein nasses Verderben. |
| 4496 | Nadelball | desc | FLIPP: Fügt den Life Pointsn deines Gegners einen direkten Schaden von 1000 Punkten auf Kosten von 2000 deiner eigenen Life Points. | FLIPP: Fügt den Life Points deines Gegners einen direkten Schaden von 1000 Punkten auf Kosten von 2000 deiner eigenen Life Points. |
| 4506 | Drachensucher | desc | Wenn diese Karte als einer Normalbeschwörung oder Flippbeschwörung beschworen wurde, zerstöre 1 offenes Monster vom Typ Drache auf dem Spielfeld. | Wenn diese Karte als Normalbeschwörung oder Flippbeschwörung beschworen wurde, zerstöre 1 offenes Monster vom Typ Drache auf dem Spielfeld. |
| 4512 | Sturm-Dogra | desc | Im Tausch gegen 3000 deiner Life Points darfst du ein Monster aus deinem FusionsDeck auf dem Friedhof ablegen. | Im Tausch gegen 3000 deiner Life Points darfst du ein Monster aus deinem Fusionsdeck auf dem Friedhof ablegen. |
| 4522 | Muka Muka | desc | Solange diese Karte offen auf dem Spielfeld liegt, erhöht sich die ATK und DEF dieser Karte um 300 Punkte für jede Karte in der Hand des Spielers, der diese Karte kontrolliert. | Solange diese Karte offen auf dem Spielfeld liegt, erhöhen sich ATK und DEF dieser Karte um 300 Punkte für jede Karte in der Hand des Spielers, der diese Karte kontrolliert. |
| 4541 | Kamakiriman | desc | Ein Menschen ähnlicher Mantis, der über zwei rasiermesserscharfe Sicheln verfügt. | Eine menschenähnliche Mantis, der über zwei rasiermesserscharfe Sicheln verfügt. |
| 4574 | Anthrosaurus | desc | Ein Menschen ähnlicher Dinosaurier mit einem hohen Intelligenzquotienten, dem es an Stärke fehlt. | Ein menschenähnlicher Dinosaurier mit einem hohen Intelligenzquotienten, dem es an Stärke fehlt. |
| 4576 | Trakadon | desc | Eine getigerter Drache, der oft dabei beobachtet wird, wie er mit hoher Geschwindigkeit durch das Ödland rennt. | Ein getigerter Drache, der oft dabei beobachtet wird, wie er mit hoher Geschwindigkeit durch das Ödland rennt. |
| 4596 | Schnabelschlange | desc | Dieses Monster wickelt sich selbst um einen Gegner und stochert mit seinem riesigen Rüssel herum. | Dieses Monster wickelt sich selbst um einen Gegner und stochert mit seinem riesigen Schnabel herum. |
| 4609 | Elfendrache | desc | Eine schöner und starker Elfendrache. | Ein schöner und starker Elfendrache. |
| 4622 | Sanduhr der Tapferkeit | desc | Für 3 Spielzüge (einschließlich der deines Gegners) nach der Aktivierung dieser Karte (einschließlich „Flipp“-Aktivierung), sind ATK- und DEF-Werte dieses Monsters halbiert. Danach werden die ATK- und DEF-Werte für den Rest des Duells verdoppelt. | Für 3 Spielzüge (einschließlich der deines Gegners) nach der Aktivierung dieser Karte (einschließlich „Flipp“-Aktivierung) sind die ATK- und DEF-Werte dieses Monsters halbiert. Danach werden die ATK- und DEF-Werte für den Rest des Duells verdoppelt. |
| 4652 | Grausiger Goo | desc | Ein Schleimmeister, der sicher härter ist als er aussieht. | Ein Schleimmeister, der sicher härter ist, als er aussieht. |
| 4654 | Angriffsmaschine | desc | Diese Maschine, erschaffen, um Angriffe in feindliches Gebiet zu führen, mäht die Feinde durch sein Vorwärtsstürzen einfach nieder. | Diese Maschine, erschaffen, um Angriffe in feindliches Gebiet zu führen, mäht die Feinde durch ihr Vorwärtsstürzen einfach nieder. |
| 4660 | Salamandra | desc | Ein mit dieser Karte ausgerüstetes FEUER-Monster erhöht seinen ATK neben 700 Punkten. | Ein mit dieser Karte ausgerüstetes FEUER-Monster erhöht seine ATK um 700 Punkte. |
| 4664 | Metallwandler | desc | Nach der Aktivierung wird diese Karte verwendet, um ein aufgedecktes Monster auszurüsten. Das mit dieser Karte ausgerüstete Monster erhöht seinen ATK- und DEF-Wert um 300 Punkte. Wenn ein mit dieser Karte ausgerüstetes Monster angegriffen wird, kannst du seinen ATK-Wert um die Hälfte des ATK-Werts des Angegriffenen erhöhen. | Nach der Aktivierung wird diese Karte verwendet, um ein aufgedecktes Monster auszurüsten. Das mit dieser Karte ausgerüstete Monster erhöht seinen ATK- und DEF-Wert um 300 Punkte. Wenn ein mit dieser Karte ausgerüstetes Monster angreift, kannst du seinen ATK-Wert um die Hälfte des ATK-Werts des angegriffenen Monsters erhöhen. |
| 4667 | Vernichtungskarte | desc | Biete 1 FINSTERNIS Monster von deiner Seite des Spielfelds mit einer ATK von 1000 oder weniger als Tribut an. Du und dein Gegner uberprufen alle Monster auf der Spielfeldseite deines Gegners, alle Karten auf der Hand deines Gegners und alle Karten, die dein Gegner in den nachsten 3 Spielzugen zieht, und zerstoren alle Monster mit einer ATK von 1500 oder hoher, die dabei gefunden werden. | Biete 1 FINSTERNIS Monster von deiner Seite des Spielfelds mit einer ATK von 1000 oder weniger als Tribut an. Du und dein Gegner überprüfen alle Monster auf der Spielfeldseite deines Gegners, alle Karten auf der Hand deines Gegners und alle Karten, die dein Gegner in den nächsten 3 Spielzügen zieht, und zerstören alle Monster mit einer ATK von 1500 oder höher, die dabei gefunden werden. |
| 4687 | Haus der Klebestreifen | desc | Wenn ein Monster, das dein Gegner beschwört (mit Ausnahme von Spezialbeschwörung) eine DEF von 500 oder weniger hat, ist es zerstört. | Wenn ein Monster, das dein Gegner beschwört (mit Ausnahme von Spezialbeschwörung), eine DEF von 500 oder weniger hat, ist es zerstört. |
| 4688 | Fressgaboon | desc | Wenn ein Monster, das dein Gegner beschwört (mit Ausnahme von Spezialbeschwörung) eine ATK von 500 oder weniger hat, ist es zerstört. | Wenn ein Monster, das dein Gegner beschwört (mit Ausnahme von Spezialbeschwörung), eine ATK von 500 oder weniger hat, ist es zerstört. |
| 4691 | Säurefallgrube | desc | Wähle 1 verdecktes Monster in Verteidigungsposition. Decke es auf und falls die DEF dieses Monsters 2000 Punkte oder geringer ist, zerstöre das Monster. Falls die DEF mehr als 2000 Punkte sind, lege das Monster in verdeckte Verteidigungsposition zurück. | Wähle 1 verdecktes Monster in Verteidigungsposition. Decke es auf und falls die DEF dieses Monsters 2000 Punkte oder geringer ist, zerstöre das Monster. Falls die DEF mehr als 2000 Punkte beträgt, lege das Monster in verdeckte Verteidigungsposition zurück. |

(... altre 218 righe nel CSV)

## A3. Dialoghi della storia

Archivi: `script/stNN_<scena>_f.ehp`, ogni scena e' una coppia di membri `...If.bin` (offset in caratteri UTF-16) e `...Lf.bin` (stringhe UTF-16LE chiuse da NUL, alcune compresse in gzip). **1649 righe** cambiate (comprese quelle che **ereditano** la correzione perche' hanno lo stesso testo originale e lo stesso giapponese di una riga corretta).

Flusso: lettura riga per riga confrontata con inglese e giapponese -> ritocchi in `tools/data/dialogue_touchups_de.json` (`esatte` e `parti`) -> `build_dialogues.py de` -> `dialogue_corrections_de.json` -> `apply_to_iso.py`. Regole automatiche di impaginazione in `build_dialogues.py`: spazio non separabile prima di `! ? : ;` anche dopo `》` (regola `FR_PUNT`), spazio dopo i segnaposto, "Mode histoire" -> "Mode aventure". Vincoli del box: ~46 caratteri per riga, max 3 righe (un segnaposto vale ~6 caratteri): `apply_to_iso` segnala le righe che potrebbero non starci.

### Ritocchi di rilettura: `esatte` (4) — frase intera originale -> frase nuova
| originale | nuovo |
|---|---|
| Hier, du kannst den hier nehmen! | Hier, nimm dieses Dienstmädchen-Outfit! |
| Warum bist du hier | Warum bist du hier? |
| Tag-Duelle erfordern noch⏎mehr Strategie | Tag-Duelle erfordern noch⏎mehr Strategie. |
| OK!⏎Los geht's | OK!⏎Los geht's! |

### Ritocchi di rilettura: `parti` (331) — sostituzioni di testo applicate a ogni riga (in ordine)
| vecchio | nuovo |
|---|---|
| euchgegeben | euch gegeben |
| anhöhren | anhören |
| das Bestes draus | das Beste draus |
| unan-genehm | unangenehm |
| dann lunger hier nicht herum | dann lungere hier nicht herum |
| mein⏎Deck ins Meer geworden zu haben | mein⏎Deck ins Meer geworfen zu haben |
| Eigentlich brauch man mich | Eigentlich braucht man mich |
| Chazz, wir sind in einem Wohnheim! | Chazz, wir sind jetzt Zimmerkumpel! |
| Außer dem bin ich bei Obelisk | Außerdem bin ich bei Obelisk |
| Was?! Hab gar nicht gehört, wie du⏎gekommen bist, 《C004_2》? | Was?! Du machst mit, 《C004_2》? |
| Das wird den 《C005_4》⏎auch so ergehen! | Dann macht auch der 《C005_4》 mit! |
| Weit du, sie | Weißt du, sie |
| kenne ich kein anderes Mädchen,⏎dass so hart drauf ist, wie sie. | kenne ich kein anderes Mädchen,⏎das so hart drauf ist wie sie. |
| spricht einfach mit mir | sprecht einfach mit mir |
| Ich habe sich geschlagen | Ich habe dich geschlagen |
| Unentscheiden | Unentschieden |
| Ich bin momentan sicher bekannt. | Ich bin ja momentan ziemlich beliebt. |
| alle Meine Duelle | alle meine Duelle |
| Tut mir Leid, dass kann ich | Tut mir Leid, das kann ich |
| Ist es Zeit fürs Abendessen. | Es ist Zeit fürs Abendessen. |
| Von Montags bis Samstags | Von Montag bis Samstag |
| Bringt Sie zum Arzt! | Bringt sie zum Arzt! |
| Schicken Sie vielleicht E-Mails wie diese⏎hier. | Schicken sie dir vielleicht E-Mails wie diese hier. |
| Du hast den Nagel auf den Kopf getroffen. | Das hast du dir doch gerade ausgedacht! |
| Brauchst dich nicht schämen. | Brauchst dich nicht zu schämen. |
| Mir müssen reden. | Wir müssen reden. |
| eine Runde⏎um den See gelaufen | eine Runde⏎um die Insel gelaufen |
| Dein ... Brille?! | Deine ... Brille?! |
| Wie suchen etwas | Wir suchen etwas |
| Da Sandwich des Tages | Das Sandwich des Tages |
| Jetzt bin du dran! | Jetzt bist du dran! |
| Alle denke, ich | Alle denken, ich |
| !„⏎Gepostet | !“⏎Gepostet |
| ?„⏎Gepostet | ?“⏎Gepostet |
| Wir haben jeden Tag unterricht | Wir haben jeden Tag Unterricht |
| Was sind endlich Ferien? | Wann sind endlich Ferien? |
| Haben Sie dir?! | Hast du sie?! |
| Haben Sie die!? | Hast du die!? |
| Haben Sie die?! | Hast du die?! |
| Muss schön sein⏎Du hast | Muss schön sein.⏎Du hast |
| Fertig? „ABC!“ | Fertig? „Guten Appetit!“ |
| Was liegt an',⏎《PLAYER》? | Was liegt an,⏎《PLAYER》? |
| ist och nicht | ist noch nicht |
| als pass auf dich auf | also pass auf dich auf |
| zum Abendbrotszeit | zur Abendbrotzeit |
| Ayers Rock, weiß du? | Ayers Rock, weißt du? |
| im 5:45 aufstehen | um 5:45 aufstehen |
| weil kein Mädchen⏎hier würde wohnen wollen | weil hier kein⏎Mädchen wohnen wollen würde |
| deine Miene so ansehen, | deine Miene so ansehe, |
| ich hab keine DP | Ich hab keine DP |
| Ist du nicht deinen | Isst du nicht deinen |
| wohl, für dich essen | wohl für dich essen |
| das Gleich auftischen | das Gleiche auftischen |
| voll abgelost haben | voll abgeloost haben |
| verlieben!„ | verlieben!“ |
| Ich muss jetzt auf den morgigen Unterricht⏎vorbereiten | Ich muss mich jetzt auf den morgigen Unterricht vorbereiten |
| Leuten wie dich zu befassen | Leuten wie dir zu befassen |
| Sollen in diesem Zimmer⏎wirklich jemand wohnen | Soll in diesem Zimmer⏎wirklich jemand wohnen |
| Schul-abbrecher | Schulabbrecher |
| Ich bin es Leid, dass | Ich bin es leid, dass |
| Ich werden Slifer | Ich werde Slifer |
| und⏎verschiedene Mengen | und⏎verschiedenen Mengen |
| Sandwiche | Sandwiches |
| Wir könnt ihr es wagen | Wie könnt ihr es wagen |
| Dass soll's erst mal | Das soll's erst mal |
| Idol-Trainingskurs„ | Idol-Trainingskurs“ |
| „Cyberengel Benten„ | „Cyberengel Benten“ |
| Warum macht du | Warum machst du |
| Du weiß schon | Du weißt schon |
| Geht's du | Gehst du |
| Erinnerst du sich | Erinnerst du dich |
| Wenn Sie „Cyberengel | Wenn sie „Cyberengel |
| Danke fürs fragen | Danke fürs Fragen |
| duellierst hast | duelliert hast |
| Sorgen⏎machen brauchst | Sorgen zu machen brauchst |
| keine Sorgen machen, aber | keine Sorgen zu machen, aber |
| dir um⏎meinen Bruder Sorgen zu machen | dir Sorgen⏎um meinen Bruder zu machen |
| Also ich wüsste, dass | Also ich weiß, dass |
| so sehr, das niemand | so sehr, dass niemand |
| schon maI⏎getroffen | schon mal⏎getroffen |
| Wenn dur wirklich | Wenn du wirklich |
| Fermentierte Sojanbohnensandwich | Fermentiertes Sojabohnensandwich |
| Phantom Pfeffersandwich | Phantom-Pfeffersandwich |
| Spitzen Salatsandwich | Spitzen-Salatsandwich |
| so ablosen | so verlieren |
| Was ,ein Duell | Was, ein Duell |
| Wir würden und nie | Wir würden uns nie |
| diese Typ⏎ausnutzen | diesen Typ⏎ausnutzen |
| Bandagen⏎lern | Bandagen und lern |
| Lunger hier nicht herum | Lungere hier nicht herum |
| Du kommst du spät | Du kommst zu spät |
| aber denn werden wir | aber dann werden wir |
| Betrachte sie als Belohnung | Betrachte es als Belohnung |
| Du hast sie dir verdient. | Du hast es dir verdient. |
| Willst wissen wer ich bin | Willst du wissen, wer ich bin |
| habe mein bestes geben | habe mein Bestes gegeben |
| mein bestes geben | mein Bestes geben |
| eine menge Duelle | eine Menge Duelle |
| über die Geister bescheid | über die Geister Bescheid |
| nichts besonderes | nichts Besonderes |
| Partners ...? | Partner ...? |
| zurecht finden | zurechtfinden |
| ob ich dein Partner werden! | ob ich dein Partner werde! |
| was besonderes | was Besonderes |
| menge von ihm | Menge von ihm |
| lausiger kleine Dieb | lausiger kleiner Dieb |
| so weiter machst | so weitermachst |
| Das ich das noch verloren | Dass ich das noch verloren |
| halt bescheid | halt Bescheid |
| beim duellieren | beim Duellieren |
| 5000DP | 5000 DP |
| #1 and #2 | #1 und #2 |
| Zeit um Gewichtheben | Zeit zum Gewichtheben |
| nächs-⏎ten | nächsten |
| trotz-⏎dem | trotzdem |
| leicht-⏎sinnig | leichtsinnig |
| tatsäch-⏎lich | tatsächlich |
| Nieder-lage | Niederlage |
| ge-⏎dacht | gedacht |
| Effekt-⏎monstern | Effektmonstern |
| Dinosaurier-⏎skelette | Dinosaurierskelette |
| Ich hoffen du kommst | Ich hoffe, du kommst |
| nur Sandwich,⏎die | nur Sandwiches,⏎die |
| ver-⏎hindern | verhindern |
| Fallen-⏎karten | Fallenkarten |
| be-⏎halten | behalten |
| einge-⏎setzt | eingesetzt |
| Nicht das wir | Nicht, dass wir |
| Nicht das ich | Nicht, dass ich |
| zum duellieren | zum Duellieren |
| Herrin der Windes | Herrin des Windes |
| unser bestes geben | unser Bestes geben |
| Dieses Maschine | Diese Maschine |
| heraus finden | herausfinden |
| dir Regeln zu erklären | euch die Regeln zu erklären |
| Schlüsse⏎für | Schlüssel⏎für |
| dass⏎Tag-Force-Turnier fortzusetzen | das⏎Tag-Force-Turnier fortzusetzen |
| Kein Antwort | Keine Antwort |
| Kartendesigner werden zu können | Kartendesigner zu werden |
| Um wir viele | Um wie viele |
| wie ich sich auch diesem Jungen genommen habe | wie ich es auch bei diesem Jungen getan habe |
| des mächtige Stamms | des mächtigen Stamms |
| Wie siehst mit den Medaillen aus | Wie sieht's mit den Medaillen aus |
| Wir könne doch | Wir können doch |
| Als, dann | Also, dann |
| Duell!l! | Duell! |
| Hätte nie gedacht, ⏎dass geschlagen werde | Hätte nie gedacht, dass⏎ich geschlagen werde |
| Duellgrund-lagen | Duellgrundlagen |
| Duell-⏎grundlagen | Duellgrundlagen |
| Hast du gut gemacht | Das hast du gut gemacht |
| GX-⏎GX-Medaillen | GX-Medaillen |
| GX- Medaillen | GX-Medaillen |
| GX-⏎Medaillen | GX-Medaillen |
| Warum mussten wir ablosen | Warum mussten wir verlieren |
| Bekannt-schaft | Bekanntschaft |
| GX-Medaillen,OK | GX-Medaillen, OK |
| Me-⏎daillen | Medaillen |
| ent-⏎täuscht | enttäuscht |
| Kannst du mit dafür | Kannst du mir dafür |
| Kein Ahnung | Keine Ahnung |
| einfach stärker als. | einfach stärker als du. |
| zu-⏎frieden | zufrieden |
| jeder-zeit | jederzeit |
| zweifels-⏎ohne | zweifelsohne |
| Medaill-⏎en | Medaillen |
| Du hast nicht⏎reichen! | Du hast nicht⏎genug! |
| He ... bist leicht wie Feder, glaube ich. | Hehe ... du bist leicht wie eine Feder, glaube ich. |
| Lass uns das bald später noch mal. | Lass uns das bald noch mal spielen. |
| dieses Karten | diese Karten |
| schon ich dich nicht | schone ich dich nicht |
| etwas scharfe Sauce | etwas Shochu |
| Im Bikini | Im Dienstmädchen-Outfit |
| im Bikini | im Dienstmädchen-Outfit |
| Meinem Vater gehört eine Firma,⏎die scharfe Saucen herstellt. | Meinem Vater gehört eine⏎Sake-Brauerei. |
| Das Büro von Kanzler | Büro des Kanzlers |
| Ich hoffe, die Können bei⏎Duellen ist besser, als⏎die Geschmack bei Freunden. | Ich hoffe, dein Können bei⏎Duellen ist besser als⏎dein Geschmack bei Freunden. |
| für dich zu,⏎arm | für dich zu⏎arm |
| Bastion und ich⏎hatte einfach | Bastion und ich⏎hatten einfach |
| Du musst als ganz unten anfangen | Du musst ganz unten anfangen |
| Mein Kostüm-Duell wird der Hit! | Mein Kostüm-Duell wird ein Reinfall! |
| also gehe ich in Bett. | also gehe ich ins Bett. |
| möchtest, sprecht einfach mit mir. | möchtest, sprich einfach mit mir. |
| wegen einem⏎Tag-Duell hier? | wegen eines⏎Tag-Duells hier? |
| Sprich mit den Anderen. | Sprich mit den anderen. |
| Ich bin ein Mal sitzen geblieben | Ich bin einmal sitzen geblieben |
| Natürlich? Wie sollen die anderen es sonst | Natürlich. Wie sollen die anderen es sonst |
| und sind Sie⏎ein zweiter Crowler! | und Sie sind⏎ein zweiter Crowler! |
| kein Spirit-monster? | kein Spirit-Monster? |
| Gehe zum Schreibtisch, bis über deinem Kopf⏎eine Uhr erscheint. | Gehe zum Bett, bis über deinem Kopf⏎eine Uhr erscheint. |
| Tschüß. | Tschüs. |
| ,⏎Du hast also wieder im Unterricht geschlafen? | ,⏎du hast also wieder im Unterricht geschlafen? |
| Sandwichesn | Sandwiches |
| Schrimps | Shrimps |
| Also haben wir gewartet, bist du kommst. | Also haben wir gewartet, bis du kommst. |
| wo du's sagst,⏎Ich hab gehört | wo du's sagst,⏎ich hab gehört |
| Ich hab gehört, 《C004_3》 ⏎hatte bei seinem Hobby | Ich hab gehört, 《C004_3》 ⏎hatte bei ihrem Hobby |
| Ihr habt Euch | Ihr habt euch |
| Ihr hattet Euch | Ihr hattet euch |
| Koch's Sandwich?! | Kochs Sandwich?! |
| Erinnerst du dich noch an unsere Gespräch? | Erinnerst du dich noch an unser Gespräch? |
| 'Ich liebe dich'?“ | ‚Ich liebe dich‘?“ |
| Du wartest auf  《C003_3》? | Du wartest auf 《C003_3》? |
| “- Action-Figur | “-Action-Figur |
| Man muss das ABC aufsagen,⏎bevor man anfängt, zu essen! | Man muss „Guten Appetit“ sagen,⏎bevor man anfängt zu essen! |
| Oh, ja,⏎Ich hab gehört | Oh, ja,⏎ich hab gehört |
| Oh ...《PLAYER》. | Oh ... 《PLAYER》. |
| heute morgen | heute Morgen |
| dass ich nachsitzen⏎muss, hab ich total den Appetit verloren. | dass ich eine⏎Ehrenrunde drehen muss, hab ich total den Appetit verloren. |
| essen die Abends französisch.⏎Offenbar a la carte. | essen die abends französisch.⏎Offenbar à la carte. |
| Wo ist 《C005_2》 ? | Wo ist 《C005_2》? |
| 》 !?“ | 》!?“ |
| Ich hab' gehört, dass ihr euch heimlich | Ich hab gehört, dass ihr euch heimlich |
| Nun, 《C004_3》⏎hatte bei seinem Hobby | Nun, 《C004_3》⏎hatte bei ihrem Hobby |
| Ich habe gehört, 《C004_3》 hat sein Duell | Ich habe gehört, 《C004_3》 hat ihr Duell |
| dass 《C004_3》 sein Hobby | dass 《C004_3》 ihr Hobby |
| bevor  der Unterricht | bevor der Unterricht |
| Gesellschaft  so hoch | Gesellschaft so hoch |
| Schon wieder 《C005_2》 .⏎ | Schon wieder 《C005_2》.⏎ |
| deiner⏎größer war 《C005_2》. | deiner⏎größer war, 《C005_2》. |
| nach⏎jemand Bestimmten? | nach⏎jemand Bestimmtem? |
| in Obelisk hinein⏎zu kommen | in Obelisk⏎hineinzukommen |
| Platz inne habe | Platz innehabe |
| Wenn du dich weiterhin so sperrst ... | Wenn du weiterhin so geistesabwesend bist ... |
| werden  ...⏎Aber | werden ...⏎Aber |
| Deck interessiert mich eben. | Deck interessiert mich eben nicht. |
| ⏎ „Cyberengel Benten“⏎ist | ⏎„Cyberengel Benten“⏎ist |
| genau so gut wie | genauso gut wie |
| Oder ist 《C006_1》 unverschämt spät? | Oder ist 《C006_1》 in letzter Zeit unscheinbar? |
| kleinen Schüler der⏎Slifer? | kleinen Schüler aus⏎Slifer? |
| Er benutzt keine Schläge in seinen Duellen. | In seinen Duellen hält er sich nicht zurück. |
| 》 , ihr steht euch nahe | 》, ihr steht euch nahe |
| übersteigt  wahrscheinlich | übersteigt wahrscheinlich |
| dich ... ?⏎Hmm... | dich ... ?⏎Hmm ... |
| nachdenken  ... | nachdenken ... |
| Also, ich glaube sie macht sich | Also, ich glaube, sie macht sich |
| Also, ich glaube sie hat sich | Also, ich glaube, sie hat sich |
| Gefühle Anderer | Gefühle anderer |
| 《C004_3》 wollte wirklich mit dir über sein⏎Hobby | 《C004_3》 wollte wirklich mit dir über ihr⏎Hobby |
| 《C004_3》 wollte mit dir über sein Hobby⏎sprechen | 《C004_3》 wollte mit dir über ihr Hobby⏎sprechen |
| 《C004_3》 hat bei seinem Hobby | 《C004_3》 hat bei ihrem Hobby |
| Koch's Sandwich... | Kochs Sandwich... |
| nur⏎５0% meines | nur⏎50% meines |
| nur⏎８0% meines | nur⏎80% meines |
| Warum bringst du mir nicht Pharao? | Warum bringst du mir nicht 《C145_1》? |
| Wo Fruchtsandwiche!? | Wo Fruchtsandwiches!? |
| Oh... Ein neuer Student? | Oh ... Ein neuer Student? |
| Wird sie entweder weg | Iss sie entweder weg |
| „Deck bearbeiten.“ | „Deck bearbeiten“. |
| „Deck-Menü.“ | „Deck-Menü“. |
| Danke für das Duell!⏎Ich mein das ernst! | Danke für die vielen Duelle!⏎Hier, eine kleine Aufmerksamkeit! |
| Ahhh ...  Unentschieden | Ahhh ... Unentschieden |
| dich noch mal wieder sehe! | dich noch mal wiedersehe! |
| Oh, hallo...⏎⏎ | Oh, hallo ...⏎⏎ |
| Sandwichess | Sandwiches |
| Ich mag Shoppen mehr,⏎als meine | Ich mag Shoppen mehr⏎als meine |
| Hoffe sie gefällt dir. | Hoffe, sie gefällt dir. |
| unsere LP ist gleich! | unsere LP sind gleich! |
| Es ist schön dich kennen zu ⏎lernen. | Es ist schön, dich⏎kennenzulernen. |
| ⏎morgens spazieren gehe | ⏎nachts spazieren gehe |
| auf's Meer | aufs Meer |
| über die Beiden? | über die beiden? |
| fair zu geht | fair zugeht |
| Wir werden die Besten sein? | Wir werden die Besten sein! |
| Jederzeit ... | Wie auch immer ... |
| ich ⏎wette du hast davon | ich ⏎wette, du hast davon |
| Ich dachte ich spiele gut. | Ich dachte, ich spiele gut. |
| warum nimmst du nicht mein Rezept. | warum nimmst du nicht mein Rezept? |
| Warum nimmst du nicht diese Karte.⏎ | Warum nimmst du nicht diese Karte?⏎ |
| Alles, klar ... | Alles klar ... |
| viele $M4027,⏎hast, | viele $M4027⏎hast, |
| auseinander liegen | auseinanderliegen |
| Die beste Kämpfe | Die besten Kämpfe |
| hier ist⏎ist eine | hier ist⏎eine |
| jede Menge von⏎diese Karten | jede Menge von⏎diesen Karten |
| Wie geht' denn so? | Wie geht's denn so? |
| weiter bringen! | weiterbringen! |
| Sehr erfreut dich kennen zu ⏎lernen. | Sehr erfreut, dich⏎kennenzulernen. |
| Wetten der ist genauso gut? | Wetten, der ist genauso gut? |
| Ich dachte du hast schon ⏎einen Partner | Ich dachte, du hast schon ⏎einen Partner |
| wie du, lebe ich | wie du lebe ich |
| zusammentun⏎werden | zusammentun,⏎werden |
| unsere Willen und⏎Karten | unseren Willen und⏎Karten |
| für das Duell,⏎gebe ich | für das Duell⏎gebe ich |
| etwas daraus lernen. | etwas daraus lernen? |
| gezeigt⏎wie man Mädels klar macht | gezeigt,⏎wie man Mädels klarmacht |
| Beeil dich mal.⏎Bist du bereit | Beeil dich mal.⏎Bist du bereit? |
| Ein Unentschieden kein Sieg | Ein Unentschieden ist kein Sieg. |
| „Best duelist“ | „Bester Duellant“ |
| Ich höre nicht auf bis mein | Ich höre nicht auf, bis mein |
| nicht wohl gesonnen,“⏎und | nicht wohl gesonnen“,⏎und |
| Das, soll ich essen? | Das soll ich essen? |
| Gut gespielt!  Hahaha! | Gut gespielt! Hahaha! |
| Sehr erfreut dich kennen zu lernen. | Sehr erfreut, dich kennenzulernen. |
| Ich frage mich was du vor... | Ich frage mich, was du vorhast ... |
| einen Obelisk⏎Blue-Partner | einen Obelisk⏎Blau-Partner |
| Aber ich hörte damit kann ⏎man | Aber ich hörte, damit kann ⏎man |
| Hier du kannst eine | Hier, du kannst eine |
| Das erste Mal, das wir uns | Das erste Mal, dass wir uns |
| verloschen, wie eine nasse Kerze | verloschen wie eine nasse Kerze |
| Ich glaube wir sind uns noch nicht begegnet. | Ich glaube, wir sind uns noch nicht begegnet. |
| Ich meine U-Boote fahren Unterwasser, oder? | Ich meine, U-Boote fahren unter Wasser, oder? |
| Hoffe du bist in Ordnung. | Hoffe, du bist in Ordnung. |
| Hoffe du bist kein Gangster. | Hoffe, du bist kein Gangster. |
| behaupten sie hätten | behaupten, sie hätten |
| wer du bist?... Nun | wer du bist? ... Nun |
| komm zu mir wenn du einen Gegner suchst | komm zu mir, wenn du einen Gegner suchst |
| meiner Rezept umgehst | meiner Karte umgehst |
| ein Mädchen bin⏎sollte | ein Mädchen bin,⏎sollte |
| Zeig mir beim Tag Duel⏎was | Zeig mir beim Tag Duel,⏎was |
| antworte „Ja.“ | antworte „Ja“. |
| TRADING CARD⏎GAME.“ | TRADING CARD⏎GAME“. |
| sobald sie das sind | sobald sie da sind |
| 》 -Gruppe | 》-Gruppe |
| „Der Chad“ oder so ähnlich | „Der 《C005_4》“ oder so ähnlich |
| Wie viele Medaillen willst du verwetten! | Wie viele Medaillen willst du verwetten? |
| den 'Wandernden | den ‚Wandernden |
| 》'! | 》‘! |
| treffe ich nicht ... | treffe ich ihn nicht wieder ... |
| ⏎ Dann beim nächsten Mal! | ⏎Dann beim nächsten Mal! |
| Einsatz!⏎dass wir gewinnen,⏎OK? | Einsatz!⏎OK? |
| laden keine⏎Duelleinladungen ab! | lehnen keine⏎Duelleinladungen ab! |
| Hey,  《PLAYER》. ⏎⏎⏎Versuchst | Hey, 《PLAYER》.⏎⏎⏎Versuchst |
| hast du mehr als 90 GX-Medaillen | hast du mindestens 90 GX-Medaillen |
| Du hast nicht mehr als⏎90 GX-Medaillen. | Du hast noch nicht⏎90 GX-Medaillen. |
| Wähl „$C9Duel$C0“ ⏎unter „$C9Talk$C0“. | Wähl „$C9Duell$C0“ ⏎unter „$C9Reden$C0“. |
| „Barett“ bekommen! | „Haarspange“ bekommen! |
| Das Barett ... | Die Haarspange ... |
| Barette sind was für Mädchen. | Haarspangen sind was für Mädchen. |
| Um der Partner eines Grabeshüters, | Um der Partner eines Grabwächters, |
| Duellant von 《M001_1》 | Duellant der 《M001_1》 |
| Duellanten von 《M001_1》 | Duellanten der 《M001_1》 |

### Elenco completo delle righe
**Confronto completo originale -> nuovo (con inglese e giapponese): `docs/changes_de/dialogues_diff.md`** (tutte le 1649 righe). Dati grezzi: `docs/changes_de/dialogues.csv`. Prime 30:

| id | originale | nuovo | inglese |
|---|---|---|---|
| st01_t01/ImpMapMsg#9 | Das Büro von Kanzler | Büro des Kanzlers | Duel Academy - Chancellor's Office |
| st01_t01/ImpMapMsg#10 | Das Büro von Kanzler | Büro des Kanzlers | Chancellor's Office |
| st01_t01/Iso001E#0 | Ich hoffe, die Können bei⏎Duellen ist besser, als⏎die Geschmack bei Freunden. | Ich hoffe, dein Können bei⏎Duellen ist besser als⏎dein Geschmack bei Freunden. | I hope you duel better⏎than the company you keep. |
| st01_t01/Iso001E#10 | Das ist selbst für dich zu,⏎arm, 《C005_2》! | Das ist selbst für dich zu⏎arm, 《C005_2》! | That's even low for you,⏎《C005_2》! |
| st01_t01/Iso001E#12 | Ich denke, Bastion und ich⏎hatte einfach ähnliche Decks. | Ich denke, Bastion und ich⏎hatten einfach ähnliche Decks. | I guess 《C006_2》 and I just⏎had similar decks. |
| st01_t01/Iso001E#34 | So wie du abgestritten hast, mein⏎Deck ins Meer geworden zu haben. | So wie du abgestritten hast, mein⏎Deck ins Meer geworfen zu haben. | Like you denied throwing⏎my deck into the ocean. |
| st01_t01/Iso003E#16 | Bei 《C001_1》hat sich⏎《C006_2》 geirrt. | Bei 《C001_1》 hat sich⏎《C006_2》 geirrt. | When it came to 《C001_1》,⏎《C006_2》 miscalculated. |
| st01_t01/Iso003E#22 | Du wirst die Duell-Akademie beim⏎Schulduell vertreten! | Du wirst die Duellakademie beim⏎Schulduell vertreten! | You will be Duel Academy's⏎rep at the School Duel! |
| st01_t01/Iso005E#12 | Warum bist du hier | Warum bist du hier? | Why are you here? |
| st01_t01/Iso005E#15 | Mach dem Namen⏎《C005_2》keine Schande. Denn ... | Mach dem Namen⏎《C005_2》 keine Schande. Denn ... | Don't let the 《C005_2》⏎name down. Because... |
| st01_t01/Iso005E#25 | Zuerst, von der Duell-Akademie ... | Zuerst, von der Duellakademie ... | Now first, from⏎Duel Academy... |
| st01_t01/Iso005E#37 | Eigentlich brauch man mich aber⏎gar nicht mehr vorstellen. | Eigentlich braucht man mich aber⏎gar nicht mehr vorstellen. | But then, I don't really⏎need an introduction. |
| st01_t01/Iso005E#56 | Es ist nur ... Eins muss ich 《C005_2》lassen. | Es ist nur ... Eins muss ich 《C005_2》 lassen. | It's just...⏎I gotta give it to 《C005_2》. |
| st01_t01/Iso005E#70 | Du verdienst es nicht, ein ⏎《C005_2》zu sein! | Du verdienst es nicht, ein ⏎《C005_2》 zu sein! | You don't deserve to be a ⏎《C005_2》! |
| st01_t01/Iso005E#95 | Ich gehöre hierher. Die⏎Duell-Akademie ist mein Zuhause. | Ich gehöre hierher. Die⏎Duellakademie ist mein Zuhause. | I belong right here. Duel⏎Academy's my home. |
| st01_t01/Iso005E#101 | Du musst als ganz unten anfangen ... | Du musst ganz unten anfangen ... | So you must start from the⏎bottom... |
| st01_t01/Iso005E#104 | Chazz, wir sind in einem Wohnheim! | Chazz, wir sind jetzt Zimmerkumpel! | 《C005_3》, we're dorm buddies! |
| st01_t01/Iso007E#14 | Komm runter, 《C002_3》.⏎Außer dem bin ich bei Obelisk ... | Komm runter, 《C002_3》.⏎Außerdem bin ich bei Obelisk ... | Chill out, 《C002_3》.⏎Besides, I'm an Obelisk- |
| st01_t01/Iso007E#15 | Was?! Hab gar nicht gehört, wie du⏎gekommen bist, 《C004_2》? | Was?! Du machst mit, 《C004_2》? | What!? Did I hear you're⏎entering, 《C004_2》? |
| st01_t01/Iso007E#16 | Das wird den 《C005_4》⏎auch so ergehen! | Dann macht auch der 《C005_4》 mit! | Then so will the 《C005_4》! |
| st01_t01/Iso007E#40 | Mein Kostüm-Duell wird der Hit! | Mein Kostüm-Duell wird ein Reinfall! | My Costume Duel is gonna⏎be a bust! |
| st01_t01/Iso007E#70 | 《PLAYER》gegen《C026_1》! | 《PLAYER》 gegen 《C026_1》! | It's 《PLAYER》ｖｓ《C026_1》! |
| st01_t01/Iso007E#95 | Sie muss ziemlich gut sein,⏎um 《PLAYER》zu schlagen. | Sie muss ziemlich gut sein,⏎um 《PLAYER》 zu schlagen. | She's a pretty good⏎duelist to beat 《PLAYER》. |
| st01_t01/Iso008E#5 | Weit du, sie könnte⏎näher sein, als du denkst. | Weißt du, sie könnte⏎näher sein, als du denkst. | You know, she may be⏎closer than you think. |
| st01_t01/Iso008E#19 | Morgen ist Unterricht,⏎also gehe ich in Bett. | Morgen ist Unterricht,⏎also gehe ich ins Bett. | There's class tomorrow,⏎so I'm going to bed. |
| st01_t01/Iso008E#27 | kenne ich kein anderes Mädchen,⏎dass so hart drauf ist, wie sie. | kenne ich kein anderes Mädchen,⏎das so hart drauf ist wie sie. | I don't know of another⏎girl as tough as her. |
| st01_t01/Iso008E#30 | Weit du, sie könnte⏎näher sein, als du denkst. | Weißt du, sie könnte⏎näher sein, als du denkst. | You know, she may be⏎closer than you think. |
| st01_t01/Iso010E#1 | Erläuterung anhöhren⏎Sondergelände verlassen⏎Nichts machen | Erläuterung anhören⏎Sondergelände verlassen⏎Nichts machen | Hear explanation.⏎Go out special site.⏎Perform nothing. |
| st01_t01/Iso010E#2 | Das Tag Force-Turnier wird⏎bald beginnen! | Das Tag-Force-Turnier wird⏎bald beginnen! | The Tag Force Tournament⏎will begin soon! |
| st01_t01/Iso010E#7 | Wenn du das Gelände verlassen⏎möchtest, spricht einfach mit mir. | Wenn du das Gelände verlassen⏎möchtest, sprich einfach mit mir. | If you want to leave,⏎simply talk to me. |

(... altre 1619 righe nel CSV)

## A4. Frasi dei duellanti nei duelli

Tabelle `chr_wordstbl_f.bin` e `02chr_wordstbl_...` dentro ~72 archivi `duel/cutin_*.ehp` (e `zakov*`). Le frasi uniche sono ~1.800: tutte rilette. **40 frasi cambiate** (66 voci). Dati: `esatte` (3) e `parti` (38) in `duel_line_corrections_de.json`. I file `*-ptrs.txt` degli archivi dei personaggi contengono offset assoluti: se una tabella cresce vanno ricalcolati (`rimappa_puntatori`), altrimenti il duello va in crash.

Confronto con parole evidenziate: `docs/changes_de/duel_lines_diff.md`.

| originale | nuovo | voci | esempi di archivio |
|---|---|---|---|
| Du fordest mich heraus?⏎Den größten Duellanten der Geschichte? | Du forderst mich heraus?⏎Den größten Duellanten der Geschichte? | 1 | cutin_abdos01.ehp |
| Siehe mal, mein Schnellzauber! | Sieh mal, mein Schnellzauber! | 1 | cutin_abdos01.ehp |
| Du wirst die Macht der⏎Alchemie noch kennen lernen! | Du wirst die Macht der⏎Alchemie noch kennenlernen! | 1 | cutin_amunael01.ehp |
| Für die Wiedergeburt braucht man⏎dieFlamme der Auslöschung.⏎Nimm das! | Für die Wiedergeburt braucht man⏎die Flamme der Auslöschung.⏎Nimm das! | 1 | cutin_amunael01.ehp |
| Mein Herz rast ganz schöN! | Mein Herz rast ganz schön! | 1 | cutin_bmgirl01.ehp |
| Abruf!! | Ich gehe mit! | 1 | cutin_boy01.ehp |
| Huh ... | Hä ... | 2 | cutin_boy01.ehp, cutin_rei01.ehp |
| Siehst du?⏎Und ich war nicht mal voll bei der Sache!⏎$Ohne Risiko ist das doch kein Zocken! | Siehst du?⏎Und ich war nicht mal voll bei der Sache!⏎Ohne Risiko ist das doch kein Zocken! | 1 | cutin_boy01.ehp |
| Ich werde nich fallen! | Ich werde nicht fallen! | 1 | cutin_chousaku01.ehp |
| Dieser Schmerze ...⏎Ich liebe ihn. | Dieser Schmerz ...⏎Ich liebe ihn. | 1 | cutin_fubuki_drk01.ehp |
| Australien ist die Heimat der Koalas,⏎undhier ist der größte Koala aller Zeiten!⏎Vorhang auf! | Australien ist die Heimat der Koalas,⏎und hier ist der größte Koala aller Zeiten!⏎Vorhang auf! | 1 | cutin_hayato01.ehp |
| Spüre die Macht des Marsupials! | Spüre die Macht der Beuteltiere! | 1 | cutin_hayato01.ehp |
| Ich brauche deine Kraft, um die drei⏎Heiligen Ungeheuer zu kontrollieren! | Ich brauche deine Kraft, um die drei⏎Heiligen Bestien zu kontrollieren! | 2 | cutin_kagemaru01.ehp, cutin_kagemaru03msg.ehp |
| Nimm die Macht meiner Heiligen Ungeheuer hin!⏎⏎Und ... ⏎Verschwinde! | Nimm die Macht meiner Heiligen Bestien hin!⏎⏎Und ... ⏎Verschwinde! | 3 | cutin_kagemaru01.ehp, cutin_kagemaru03msg.ehp |
| Ja! Endlich!⏎Ich habe meine Jugend wiedergewonnen!⏎⏎Komm schon! Ich nehme dir deine Seel!⏎Dein Innerstes wird mir gehören! | Ja! Endlich!⏎Ich habe meine Jugend wiedergewonnen!⏎⏎Komm schon! Ich nehme dir deine Seele!⏎Dein Innerstes wird mir gehören! | 1 | cutin_kagemaru02_a.ehp |
| Ich werde dich begragen! | Ich werde dich begraben! | 1 | cutin_kagemaru02_a.ehp |
| Meine Macht gleicht der der großen Geister.⏎⏎Trotzdem bin ich immer noch ...⏎⏎Unmöglich ... unmöglich ...$NUNMÖGLICH! | Meine Macht gleicht der der großen Geister.⏎⏎Trotzdem bin ich immer noch ...⏎⏎Unmöglich ... unmöglich ...⏎UNMÖGLICH! | 1 | cutin_kagemaru02_a.ehp |
| Ich aktiviere einen Fallenzauber! | Ich aktiviere eine Falle! | 1 | cutin_kamula01.ehp |
| Jetzt kommt ein Fallenzauber! | Jetzt kommt eine Falle! | 1 | cutin_kamula01.ehp |
| Ich aktiviere einen Konterfalle! | Ich aktiviere eine Konterfalle! | 1 | cutin_kamula01.ehp |
| Jetzt kommt ein Konterfalle! | Jetzt kommt eine Konterfalle! | 1 | cutin_kamula01.ehp |
| Nein!⏎⏎Ich bin eine Vampirlegende⏎Wie konnte ich gegen einen primitiven⏎Menschen verlieren! | Nein!⏎⏎Ich bin eine Vampirlegende!⏎Wie konnte ich gegen einen primitiven⏎Menschen verlieren! | 1 | cutin_kamula01.ehp |
| Mir reichts mit dir!⏎Tschüss, du Loser! | Mir reicht's mit dir!⏎Tschüss, du Loser! | 1 | cutin_kuronosu01.ehp |
| Jippi!!⏎ Öh ...⏎I-ich meine: jawoll! Yo! | Jippi!!⏎Öh ...⏎I-ich meine: jawoll! Yo! | 1 | cutin_rei02.ehp |
| Monster spezialbeschwören ... aus Deck | Monster spezialbeschwören ... aus Deck! | 1 | cutin_sal01.ehp |
| Ich kann nicht garantieren,⏎dass ich verliere! Nicht mehr! | Dass ich verliere, ist nicht garantiert! Nicht mehr! | 1 | cutin_shou01.ehp |
| Das ist das Paradebeispiel⏎für alle Vehicroids.!⏎Los! | Das ist das Paradebeispiel⏎für alle Vehicroids!⏎Los! | 1 | cutin_shou01.ehp |
| Unterschätz das Ding nicht,⏎nur weil es so knuffig ist.!⏎Los! | Unterschätz das Ding nicht,⏎nur weil es so knuffig ist!⏎Los! | 1 | cutin_shou01.ehp |
| Argh ... Du gutt! | Argh ... Du gut! | 1 | cutin_taizan01.ehp |
| Los, König Ojama! ⏎Mach sie alle platt! | Los, Ojama-König! ⏎Mach sie alle platt! | 2 | cutin_thunder01.ehp, cutin_thunder_blk01.ehp |
| Koste den Zorn meines Freundes!⏎Tod und Vernichtung! | Koste den Zorn meines Dämons!⏎Tod und Vernichtung! | 1 | cutin_titan01.ehp |
| Ich setze eine Karten ein. | Ich setze eine Karte ein. | 1 | cutin_tome01.ehp |
| Uhlala!⏎⏎Ich bin das wunderschöne⏎Dunkle-Magier-Mädchen!⏎Ich nehm's gegen dich auf! | Uhlala!⏎⏎Ich bin das wunderschöne⏎Dunkle Magier-Mädchen!⏎Ich nehm's gegen dich auf! | 1 | cutin_tome01.ehp |
| Kombination der Dunklen Skorpione! | Dunkler Skorpion-Gemeinschaftsangriff! | 1 | cutin_zaloog01_a.ehp |
| Ich tu's ! | Ich tu's! | 5 | zakov50.ehp, zakov51.ehp, zakov52.ehp, zakov53.ehp |
| In diesem Augenblich! | In diesem Augenblick! | 6 | zakov65.ehp, zakov66.ehp, zakov67.ehp, zakov68.ehp |
| Ich aktiviere jetzt einen RitualzauberZauber. | Ich aktiviere jetzt einen Ritualzauber. | 5 | zakov70.ehp, zakov71.ehp, zakov72.ehp, zakov73.ehp |
| Tut mir Leid! | Tut mir leid! | 5 | zakov75.ehp, zakov76.ehp, zakov77.ehp, zakov78.ehp |
| Ich setze eine Ausrüstungszauber ein! | Ich setze einen Ausrüstungszauber ein! | 5 | zakov75.ehp, zakov76.ehp, zakov77.ehp, zakov78.ehp |
| Wie unentschieden?⏎Wir wiederholen das Duell! | Wie, unentschieden?⏎Wir wiederholen das Duell! | 1 | zakov82.ehp |

## A5. Stringhe lunghe e corte dell'interfaccia

Tabelle `strTbl*`, `help_strtbl_*`, `ddstrtbl_*`, `field_strtbl*` (formato `(n, 12, 12+4n)` + offset + UTF-16) in 55 archivi (la stessa tabella e' copiata in piu' archivi, es. `field/always_*_fra.ehp` x6). **581 stringhe uniche cambiate**. Regole: `tools/corrections/string_rules_de.py` — **491 voci `STRINGHE`** (archivio, membro, indice 0-based, [(vecchio, nuovo)], motivo), **37 `GLOBALI`** (regex/callable, applicate dopo le STRINGHE) su **33 tabelle** (`TABELLE`); piu' 0 correzioni puntuali in `tools/data/ui_texts.json` (scrittura sul posto, testo piu' corto o uguale).

### Per membro (stringhe uniche cambiate)
| membro | stringhe |
|---|---|
| strTbl_g.bin | 172 |
| help_strtbl_contents_duel_g.bin | 67 |
| help_strtbl_contents.bin | 62 |
| strTbl.bin | 58 |
| 03_message_res.bin | 55 |
| 04_message_res.bin | 33 |
| 02_message_res.bin | 29 |
| 01_message_res.bin | 25 |
| field_strtbl_item.bin | 22 |
| ddstrtbl_g.bin | 12 |
| tushin_msg_g.bin | 12 |
| field_strtbl.bin | 8 |
| field_strtbl_mapname.bin | 8 |
| event_name.bin | 7 |
| title_msg_g.bin | 7 |
| option_msg_g.bin | 4 |

### Regole globali (tutte)
| modello | sostituzione | motivo |
|---|---|---|
| Seitendeck | Side Deck | una sola grafia (Side Deck nel resto del gioco) |
| \b([Tt]ut mir) Leid\b | \1 leid | ortografia riformata |
| \bspielzug | Spielzug | maiuscola |
| \$C0\$(?=[ \n.,!?]) | $C0 | $ vagante dopo il codice colore |
| Monster-kartenzone | Monsterkartenzone | trattino di sillabazione rimasto |
| (Fallen\|Fallenkarten)- (karten\|zone) | \1\2 | spazio dopo trattino di sillabazione |
| Geg-ner | Gegner | trattino di sillabazione rimasto |
| Ausrüstungs-zauberkarten | Ausrüstungszauberkarten | trattino di sillabazione rimasto |
| Karten-effekte | Karteneffekte | trattino di sillabazione rimasto |
| Aktivier-ung | Aktivierung | trattino di sillabazione rimasto |
| gleich-zeitig | gleichzeitig | trattino di sillabazione rimasto |
| (\$CA[\d.]+)\$(?=[ \n.,!?]) | \1$C0 | codice colore di chiusura incompleto |
| An-griffsabsicht | Angriffsabsicht | trattino di sillabazione rimasto |
| (Angriffs\|Verteidigungs)-position | \1position | trattino di sillabazione rimasto |
| gegner-isch | gegnerisch | trattino di sillabazione rimasto |
| zer-stört | zerstört | trattino di sillabazione rimasto |
| Restscha-den | Restschaden | trattino di sillabazione rimasto |
| Angriffspo-sition\|An-griffsposition | Angriffsposition | trattino di sillabazione rimasto |
| Ausnahme-fälle | Ausnahmefälle | trattino di sillabazione rimasto |
| den-selben | denselben | trattino di sillabazione rimasto |
| (?<=[a-zäöüßA-ZÄÖÜ\)“]) um (?=[^.,!?\n\r]{0,70}?\bzu\b) | , um  | virgola prima dell'infinitiva con um ... zu |
| ([.!?“])  (?=[A-ZÄÖÜ]) | \1  | doppio spazio dopo il punto |
| \bkennen zu lernen\b | kennenzulernen | ortografia riformata |
| \bkennen lernen\b | kennenlernen | ortografia riformata |
| \bkennen gelernt\b | kennengelernt | ortografia riformata |
| Duell Akademie | Duellakademie | grafia unica |
| „([^„“"\n\r]{1,60})" | „\1“ | virgolette di chiusura dritte al posto di “ |
| Zauber- Und  | Zauber- und  | maiuscola |
| Algemeinen | Allgemeinen | refuso |
| Vorraussetzung | Voraussetzung | refuso |
| Konter-Fall | Konterfall | come nelle carte |
| Deck Bearbeitungs | Deck-Bearbeitungs | trattino |
| ([×△○□])–Taste | \1-Taste | trattino |
| Story Modus | Story-Modus | trattino |
| \bSlifer[- ]Red\b | Slifer Rot | residuo inglese (nel resto del gioco: Slifer Rot / Ra Gelb / Obelisk Blau) |
| \bRa[- ]Yellow\b | Ra Gelb | residuo inglese |
| \bObelisk[- ]Blue\b | Obelisk Blau | residuo inglese |

### Voci STRINGHE (tutte): dove e perche'
| archivio | membro | indice | cambiamenti | motivo |
|---|---|---|---|---|
| database/charalist.ehp | strTbl_g.bin | 12 | 5 sostituzione/i | concordanza, grafia |
| database/charalist.ehp | strTbl_g.bin | 13 | 1 sostituzione/i | genitivo di un nome in -s, residuo inglese |
| database/charalist.ehp | strTbl_g.bin | 14 | 1 sostituzione/i | spazio |
| database/charalist.ehp | strTbl_g.bin | 15 | 1 sostituzione/i | caso |
| database/charalist.ehp | strTbl_g.bin | 16 | 2 sostituzione/i | punto mancante, refuso |
| database/charalist.ehp | strTbl_g.bin | 17 | 2 sostituzione/i | refuso, caso |
| database/charalist.ehp | strTbl_g.bin | 18 | 3 sostituzione/i | maiuscole, verbo sbagliato (EN: He likes to eat vegetables) |
| database/charalist.ehp | strTbl_g.bin | 19 | 1 sostituzione/i | refuso |
| database/charalist.ehp | strTbl_g.bin | 20 | 3 sostituzione/i | caso, concordanza, virgolette mancanti |
| database/charalist.ehp | strTbl_g.bin | 21 | 1 sostituzione/i | grammatica |
| database/charalist.ehp | strTbl_g.bin | 22 | 2 sostituzione/i | genitivo di un nome in -s |
| database/charalist.ehp | strTbl_g.bin | 24 | 2 sostituzione/i | grammatica |
| database/charalist.ehp | strTbl_g.bin | 25 | 1 sostituzione/i | caso |
| database/charalist.ehp | strTbl_g.bin | 28 | 1 sostituzione/i | refuso |
| database/charalist.ehp | strTbl_g.bin | 29 | 1 sostituzione/i | concordanza |
| database/charalist.ehp | strTbl_g.bin | 31 | 2 sostituzione/i | concordanza |
| database/charalist.ehp | strTbl_g.bin | 33 | 1 sostituzione/i | nome scritto in due modi nello stesso testo |
| database/charalist.ehp | strTbl_g.bin | 35 | 1 sostituzione/i | maiuscola |
| database/charalist.ehp | strTbl_g.bin | 37 | 2 sostituzione/i | refuso, grammatica (EN: high school level Duel Academy) |
| database/charalist.ehp | strTbl_g.bin | 38 | 1 sostituzione/i | parola doppia |
| database/charalist.ehp | strTbl_g.bin | 40 | 1 sostituzione/i | virgola sbagliata |
| database/charalist.ehp | strTbl_g.bin | 41 | 3 sostituzione/i | genere (EN: A card spirit), dass |
| database/charalist.ehp | strTbl_g.bin | 43 | 2 sostituzione/i | maiuscola, grammatica |
| database/charalist.ehp | strTbl_g.bin | 44 | 1 sostituzione/i | grammatica |
| database/charalist.ehp | strTbl_g.bin | 45 | 1 sostituzione/i | refuso, articolo |
| database/charalist.ehp | strTbl_g.bin | 49 | 1 sostituzione/i | concordanza |
| database/charalist.ehp | strTbl_g.bin | 50 | 1 sostituzione/i | termine come nelle carte (Grabwächters Attentäter) |
| database/charalist.ehp | strTbl_g.bin | 52 | 1 sostituzione/i | genitivo senza apostrofo |
| database/charalist.ehp | strTbl_g.bin | 65 | 1 sostituzione/i | come nei tipi di carta (permanent) |
| database/charalist.ehp | strTbl_g.bin | 69 | 1 sostituzione/i | refuso, come nei tipi di carta (permanent) |
| database/charalist.ehp | strTbl_g.bin | 70 | 1 sostituzione/i | come nelle carte (Konterfalle) |
| database/duelrecord.ehp | strTbl_g.bin | 5 | 1 sostituzione/i | residuo inglese |
| duel/result/result_g.ehp | strTbl.bin | 5 | 1 sostituzione/i | residuo inglese |
| database/duelrecord.ehp | strTbl_g.bin | 6 | 1 sostituzione/i | residuo inglese |
| duel/result/result_g.ehp | strTbl.bin | 6 | 1 sostituzione/i | residuo inglese |
| database/duelrecord.ehp | strTbl_g.bin | 9 | 1 sostituzione/i | residuo inglese |
| duel/result/result_g.ehp | strTbl.bin | 9 | 1 sostituzione/i | residuo inglese |
| database/duelrecord.ehp | strTbl_g.bin | 10 | 1 sostituzione/i | trattino |
| duel/result/result_g.ehp | strTbl.bin | 10 | 1 sostituzione/i | trattino |
| database/duelrecord.ehp | strTbl_g.bin | 16 | 1 sostituzione/i | maiuscola |
| duel/result/result_g.ehp | strTbl.bin | 16 | 1 sostituzione/i | maiuscola |
| database/duelrecord.ehp | strTbl_g.bin | 17 | 1 sostituzione/i | maiuscola |
| duel/result/result_g.ehp | strTbl.bin | 17 | 1 sostituzione/i | maiuscola |
| database/duelrecord.ehp | strTbl_g.bin | 30 | 1 sostituzione/i | genere (die ATK), trattino |
| duel/result/result_g.ehp | strTbl.bin | 30 | 1 sostituzione/i | genere (die ATK), trattino |
| database/duelrecord.ehp | strTbl_g.bin | 32 | 1 sostituzione/i | virgola |
| duel/result/result_g.ehp | strTbl.bin | 32 | 1 sostituzione/i | virgola |
| database/duelrecord.ehp | strTbl_g.bin | 34 | 1 sostituzione/i | virgola |
| duel/result/result_g.ehp | strTbl.bin | 34 | 1 sostituzione/i | virgola |
| database/duelrecord.ehp | strTbl_g.bin | 35 | 1 sostituzione/i | virgola |
| duel/result/result_g.ehp | strTbl.bin | 35 | 1 sostituzione/i | virgola |
| database/duelrecord.ehp | strTbl_g.bin | 36 | 1 sostituzione/i | virgola |
| duel/result/result_g.ehp | strTbl.bin | 36 | 1 sostituzione/i | virgola |
| database/duelrecord.ehp | strTbl_g.bin | 37 | 1 sostituzione/i | concordanza |
| duel/result/result_g.ehp | strTbl.bin | 37 | 1 sostituzione/i | concordanza |
| database/duelrecord.ehp | strTbl_g.bin | 38 | 1 sostituzione/i | concordanza |
| duel/result/result_g.ehp | strTbl.bin | 38 | 1 sostituzione/i | concordanza |
| database/duelrecord.ehp | strTbl_g.bin | 49 | 1 sostituzione/i | trattino |
| duel/result/result_g.ehp | strTbl.bin | 49 | 1 sostituzione/i | trattino |
| database/duelrecord.ehp | strTbl_g.bin | 63 | 1 sostituzione/i | trattino |
| duel/result/result_g.ehp | strTbl.bin | 63 | 1 sostituzione/i | trattino |
| database/duelrecord.ehp | strTbl_g.bin | 64 | 1 sostituzione/i | punto delle migliaia come nelle altre voci |
| duel/result/result_g.ehp | strTbl.bin | 64 | 1 sostituzione/i | punto delle migliaia come nelle altre voci |
| database/duelrecord.ehp | strTbl_g.bin | 67 | 1 sostituzione/i | come la voce prima |
| duel/result/result_g.ehp | strTbl.bin | 67 | 1 sostituzione/i | come la voce prima |
| database/duelrecord.ehp | strTbl_g.bin | 70 | 1 sostituzione/i | trattini (come Keine-Karten-mehr-Bonus) |
| duel/result/result_g.ehp | strTbl.bin | 70 | 1 sostituzione/i | trattini (come Keine-Karten-mehr-Bonus) |
| database/duelrecord.ehp | strTbl_g.bin | 71 | 1 sostituzione/i | trattini |
| duel/result/result_g.ehp | strTbl.bin | 71 | 1 sostituzione/i | trattini |
| database/duelrecord.ehp | strTbl_g.bin | 87 | 1 sostituzione/i | composto |
| duel/result/result_g.ehp | strTbl.bin | 87 | 1 sostituzione/i | composto |
| database/duelrecord.ehp | strTbl_g.bin | 88 | 1 sostituzione/i | composto |
| duel/result/result_g.ehp | strTbl.bin | 88 | 1 sostituzione/i | composto |
| database/duelrecord.ehp | strTbl_g.bin | 126 | 1 sostituzione/i | caso, maiuscola |
| duel/result/result_g.ehp | strTbl.bin | 126 | 1 sostituzione/i | caso, maiuscola |
| database/duelrecord.ehp | strTbl_g.bin | 127 | 1 sostituzione/i | caso |
| duel/result/result_g.ehp | strTbl.bin | 127 | 1 sostituzione/i | caso |
| database/duelrecord.ehp | strTbl_g.bin | 140 | 1 sostituzione/i | refusi, punto delle migliaia, Toon-Monster come nelle carte |
| duel/result/result_g.ehp | strTbl.bin | 140 | 1 sostituzione/i | refusi, punto delle migliaia, Toon-Monster come nelle carte |
| database/duelrecord.ehp | strTbl_g.bin | 151 | 1 sostituzione/i | refuso |
| duel/result/result_g.ehp | strTbl.bin | 151 | 1 sostituzione/i | refuso |
| database/duelrecord.ehp | strTbl_g.bin | 152 | 1 sostituzione/i | virgola |
| duel/result/result_g.ehp | strTbl.bin | 152 | 1 sostituzione/i | virgola |
| database/duelrecord.ehp | strTbl_g.bin | 153 | 1 sostituzione/i | punto delle migliaia |
| duel/result/result_g.ehp | strTbl.bin | 153 | 1 sostituzione/i | punto delle migliaia |
| database/duelrecord.ehp | strTbl_g.bin | 154 | 1 sostituzione/i | punto delle migliaia |
| duel/result/result_g.ehp | strTbl.bin | 154 | 1 sostituzione/i | punto delle migliaia |
| database/duelrecord.ehp | strTbl_g.bin | 163 | 1 sostituzione/i | caso, maiuscola |
| duel/result/result_g.ehp | strTbl.bin | 163 | 1 sostituzione/i | caso, maiuscola |
| database/duelrecord.ehp | strTbl_g.bin | 182 | 1 sostituzione/i | traduzione sbagliata (JA: 全レベルのモンスターが入った, EN: monsters of every Level) |
| duel/result/result_g.ehp | strTbl.bin | 182 | 1 sostituzione/i | traduzione sbagliata (JA: 全レベルのモンスターが入った, EN: monsters of every Level) |
| database/duelrecord.ehp | strTbl_g.bin | 213 | 1 sostituzione/i | come nei nomi delle carte |
| duel/result/result_g.ehp | strTbl.bin | 213 | 1 sostituzione/i | come nei nomi delle carte |
| database/duelrecord.ehp | strTbl_g.bin | 215 | 1 sostituzione/i | come nelle carte |
| duel/result/result_g.ehp | strTbl.bin | 215 | 1 sostituzione/i | come nelle carte |
| database/duelrecord.ehp | strTbl_g.bin | 224 | 1 sostituzione/i | virgola |
| duel/result/result_g.ehp | strTbl.bin | 224 | 1 sostituzione/i | virgola |
| database/duelrecord.ehp | strTbl_g.bin | 225 | 1 sostituzione/i | virgola |
| duel/result/result_g.ehp | strTbl.bin | 225 | 1 sostituzione/i | virgola |
| database/duelrecord.ehp | strTbl_g.bin | 226 | 1 sostituzione/i | virgola |
| duel/result/result_g.ehp | strTbl.bin | 226 | 1 sostituzione/i | virgola |
| database/duelrecord.ehp | strTbl_g.bin | 229 | 1 sostituzione/i | come nei dialoghi |
| duel/result/result_g.ehp | strTbl.bin | 229 | 1 sostituzione/i | come nei dialoghi |
| database/duelrecord.ehp | strTbl_g.bin | 238 | 1 sostituzione/i | virgola |
| duel/result/result_g.ehp | strTbl.bin | 238 | 1 sostituzione/i | virgola |
| database/duelrecord.ehp | strTbl_g.bin | 240 | 1 sostituzione/i | trattino |
| duel/result/result_g.ehp | strTbl.bin | 240 | 1 sostituzione/i | trattino |
| database/duelrecord.ehp | strTbl_g.bin | 242 | 1 sostituzione/i | ortografia tedesca |
| duel/result/result_g.ehp | strTbl.bin | 242 | 1 sostituzione/i | ortografia tedesca |
| database/duelrecord.ehp | strTbl_g.bin | 244 | 1 sostituzione/i | residuo inglese |
| duel/result/result_g.ehp | strTbl.bin | 244 | 1 sostituzione/i | residuo inglese |
| database/duelrecord.ehp | strTbl_g.bin | 245 | 1 sostituzione/i | residuo inglese |
| duel/result/result_g.ehp | strTbl.bin | 245 | 1 sostituzione/i | residuo inglese |
| database/duelrecord.ehp | strTbl_g.bin | 248 | 1 sostituzione/i | residuo inglese |
| duel/result/result_g.ehp | strTbl.bin | 248 | 1 sostituzione/i | residuo inglese |
| database/duelrecord.ehp | strTbl_g.bin | 249 | 1 sostituzione/i | residuo inglese |
| duel/result/result_g.ehp | strTbl.bin | 249 | 1 sostituzione/i | residuo inglese |
| database/duelrecord.ehp | strTbl_g.bin | 250 | 1 sostituzione/i | spazio |
| duel/result/result_g.ehp | strTbl.bin | 250 | 1 sostituzione/i | spazio |
| database/duelrecord.ehp | strTbl_g.bin | 260 | 1 sostituzione/i | frase mancante (EN: The duel will now end.) |
| duel/result/result_g.ehp | strTbl.bin | 260 | 1 sostituzione/i | frase mancante (EN: The duel will now end.) |
| database/duelrecord.ehp | strTbl_g.bin | 268 | 1 sostituzione/i | termine (EN: duel) |
| duel/result/result_g.ehp | strTbl.bin | 268 | 1 sostituzione/i | termine (EN: duel) |
| database/duelrecord.ehp | strTbl_g.bin | 269 | 1 sostituzione/i | ortografia tedesca |
| duel/result/result_g.ehp | strTbl.bin | 269 | 1 sostituzione/i | ortografia tedesca |
| database/limitlist.ehp | strTbl_g.bin | 1 | 1 sostituzione/i | aggettivi minuscoli |
| database/limitlist.ehp | strTbl_g.bin | 2 | 1 sostituzione/i | aggettivi minuscoli |
| database/limitlist.ehp | strTbl_g.bin | 4 | 1 sostituzione/i | abbreviazione inglese (Ltd.), voce di menu |
| database/tutoriallist.ehp | strTbl_g.bin | 13 | 1 sostituzione/i | costruzione mista (EN: Changing Battle Positions) |
| deck/all_g.ehp | strTbl.bin | 31 | 1 sostituzione/i | trattino |
| deck/all_g.ehp | strTbl.bin | 41 | 1 sostituzione/i | avverbio |
| deck/all_g.ehp | strTbl.bin | 83 | 1 sostituzione/i | doppio spazio |
| deck/all_g.ehp | strTbl.bin | 112 | 1 sostituzione/i | composto |
| deck/all_g.ehp | strTbl.bin | 73 | 1 sostituzione/i | incompleto (JA: デッキを元の状態に戻す) |
| deck/all_g.ehp | strTbl.bin | 132 | 1 sostituzione/i | refuso |
| deck/all_g.ehp | strTbl.bin | 134 | 1 sostituzione/i | parola in piu' |
| deck/all_g.ehp | strTbl.bin | 172 | 1 sostituzione/i | costruzione mista (EN: Changing Battle Positions) |
| deck/all_g.ehp | help_strtbl_contents.bin | 4 | 1 sostituzione/i | trattino |
| deck/all_g.ehp | help_strtbl_contents.bin | 23 | 1 sostituzione/i | trattino |
| deck/all_g.ehp | help_strtbl_contents.bin | 29 | 1 sostituzione/i | composto |
| deck/all_g.ehp | help_strtbl_contents.bin | 37 | 1 sostituzione/i | composto (come Deckrezepte) |
| deck/all_g.ehp | help_strtbl_contents.bin | 41 | 1 sostituzione/i | incompleto (JA: デッキを元の状態に戻す) |
| deck/all_g.ehp | help_strtbl_contents.bin | 53 | 1 sostituzione/i | costruzione |
| deck/all_g.ehp | help_strtbl_contents.bin | 70 | 1 sostituzione/i | plurale |
| deck/all_g.ehp | help_strtbl_contents.bin | 84 | 1 sostituzione/i | senza senso (JA: カードをめくる; stessa voce di 166) |
| deck/all_g.ehp | help_strtbl_contents.bin | 93 | 1 sostituzione/i | maiuscola, punto |
| deck/all_g.ehp | help_strtbl_contents.bin | 94 | 1 sostituzione/i | maiuscola, punto |
| deck/all_g.ehp | help_strtbl_contents.bin | 97 | 2 sostituzione/i | pronome mancante (EN: you will draw), refuso, virgola |
| deck/all_g.ehp | help_strtbl_contents.bin | 99 | 4 sostituzione/i | concordanza, caso |
| deck/all_g.ehp | help_strtbl_contents.bin | 106 | 1 sostituzione/i | trattino |
| deck/all_g.ehp | help_strtbl_contents.bin | 107 | 1 sostituzione/i | plurale |
| deck/all_g.ehp | help_strtbl_contents.bin | 109 | 1 sostituzione/i | nachdem, articolo mancante |
| deck/all_g.ehp | help_strtbl_contents.bin | 112 | 1 sostituzione/i | concordanza |
| deck/all_g.ehp | help_strtbl_contents.bin | 123 | 1 sostituzione/i | virgola, caso |
| deck/all_g.ehp | help_strtbl_contents.bin | 126 | 1 sostituzione/i | spazio |
| deck/all_g.ehp | help_strtbl_contents.bin | 129 | 3 sostituzione/i | plurale, refuso, je ... desto |
| deck/all_g.ehp | help_strtbl_contents.bin | 133 | 1 sostituzione/i | das/dass |
| deck/all_g.ehp | help_strtbl_contents.bin | 135 | 3 sostituzione/i | plurale, trattino, caso |
| deck/all_g.ehp | help_strtbl_contents.bin | 136 | 1 sostituzione/i | frase sbagliata (soggetto) |
| deck/all_g.ehp | help_strtbl_contents.bin | 137 | 3 sostituzione/i | maiuscola, 'solange' di troppo |
| deck/all_g.ehp | help_strtbl_contents.bin | 141 | 2 sostituzione/i | articolo, verbo (EN: activated) |
| deck/all_g.ehp | help_strtbl_contents.bin | 142 | 1 sostituzione/i | virgola |
| deck/all_g.ehp | help_strtbl_contents.bin | 144 | 1 sostituzione/i | virgola |
| deck/all_g.ehp | help_strtbl_contents.bin | 147 | 1 sostituzione/i | verbo mancante |
| deck/all_g.ehp | help_strtbl_contents.bin | 148 | 1 sostituzione/i | nachdem |
| deck/all_g.ehp | help_strtbl_contents.bin | 149 | 2 sostituzione/i | pronome mancante, relativo |
| deck/all_g.ehp | help_strtbl_contents.bin | 150 | 3 sostituzione/i | concordanza, caso |
| deck/all_g.ehp | help_strtbl_contents.bin | 153 | 1 sostituzione/i | nachdem |
| deck/all_g.ehp | help_strtbl_contents.bin | 154 | 1 sostituzione/i | virgola, punto |
| deck/all_g.ehp | help_strtbl_contents.bin | 156 | 3 sostituzione/i | frase non grammaticale, refusi |
| deck/all_g.ehp | help_strtbl_contents.bin | 157 | 1 sostituzione/i | verbo mancante |
| deck/all_g.ehp | help_strtbl_contents.bin | 158 | 1 sostituzione/i | frase sbagliata |
| deck/all_g.ehp | help_strtbl_contents.bin | 159 | 1 sostituzione/i | refuso |
| deck/all_g.ehp | help_strtbl_contents.bin | 161 | 1 sostituzione/i | maiuscola |
| deck/all_g.ehp | help_strtbl_contents.bin | 162 | 3 sostituzione/i | parola doppia, caso, virgola |
| deck/all_g.ehp | help_strtbl_contents.bin | 163 | 2 sostituzione/i | refuso, costruzione |
| deck/all_g.ehp | help_strtbl_contents.bin | 165 | 2 sostituzione/i | concordanza |
| deck/all_g.ehp | help_strtbl_contents.bin | 166 | 1 sostituzione/i | plurale, trattino |
| deck/all_g.ehp | help_strtbl_contents.bin | 167 | 1 sostituzione/i | refuso |
| deck/all_g.ehp | help_strtbl_contents.bin | 171 | 1 sostituzione/i | plurale |
| deck/all_g.ehp | help_strtbl_contents.bin | 172 | 2 sostituzione/i | caso, refuso |
| deck/all_g.ehp | help_strtbl_contents.bin | 173 | 1 sostituzione/i | pronome |
| deck/tutorial.ehp | strTbl_g.bin | 9 | 1 sostituzione/i | virgola |
| deck/tutorial.ehp | strTbl_g.bin | 16 | 1 sostituzione/i | virgola, trattino |
| deck/tutorial.ehp | strTbl_g.bin | 18 | 1 sostituzione/i | frase non grammaticale |
| deck/tutorial.ehp | strTbl_g.bin | 20 | 1 sostituzione/i | virgola |
| deck/tutorial.ehp | strTbl_g.bin | 21 | 1 sostituzione/i | virgola |
| deck/tutorial.ehp | strTbl_g.bin | 26 | 1 sostituzione/i | punto interrogativo |
| deck/tutorial.ehp | strTbl_g.bin | 27 | 1 sostituzione/i | caso, verbo |
| deck/tutorial.ehp | strTbl_g.bin | 34 | 1 sostituzione/i | parola mancante |
| deck/tutorial.ehp | strTbl_g.bin | 39 | 1 sostituzione/i | maiuscole |
| deck/tutorial.ehp | strTbl_g.bin | 55 | 1 sostituzione/i | plurale |
| deck/tutorial.ehp | strTbl_g.bin | 58 | 1 sostituzione/i | punto interrogativo |
| deck/tutorial.ehp | strTbl_g.bin | 66 | 1 sostituzione/i | congiunzione |
| deck/tutorial.ehp | strTbl_g.bin | 76 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_g.bin | 81 | 1 sostituzione/i | frase incompleta |
| deck/tutorial.ehp | strTbl_g.bin | 82 | 1 sostituzione/i | maiuscole |
| deck/tutorial.ehp | strTbl_g.bin | 87 | 1 sostituzione/i | parola doppia |
| deck/tutorial.ehp | strTbl_g.bin | 91 | 1 sostituzione/i | caso |
| deck/tutorial.ehp | strTbl_g.bin | 93 | 1 sostituzione/i | genere |
| deck/tutorial.ehp | strTbl_g.bin | 94 | 1 sostituzione/i | caso |
| deck/tutorial.ehp | strTbl_g.bin | 97 | 1 sostituzione/i | frase incompleta |
| deck/tutorial.ehp | strTbl_g.bin | 98 | 1 sostituzione/i | parola mancante |
| deck/tutorial.ehp | strTbl_g.bin | 60 | 1 sostituzione/i | virgola / costruzione |
| deck/tutorial.ehp | strTbl_g.bin | 113 | 1 sostituzione/i | genere (die ATK) |
| deck/tutorial.ehp | strTbl_g.bin | 116 | 1 sostituzione/i | concordanza |
| deck/tutorial.ehp | strTbl_g.bin | 117 | 2 sostituzione/i | concordanza |
| deck/tutorial.ehp | strTbl_g.bin | 125 | 1 sostituzione/i | registro |
| deck/tutorial.ehp | strTbl_g.bin | 133 | 1 sostituzione/i | plurale |
| deck/tutorial.ehp | strTbl_g.bin | 137 | 1 sostituzione/i | registro |
| deck/tutorial.ehp | strTbl_g.bin | 138 | 1 sostituzione/i | virgola |
| deck/tutorial.ehp | strTbl_g.bin | 147 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_g.bin | 150 | 1 sostituzione/i | virgole |
| deck/tutorial.ehp | strTbl_g.bin | 154 | 1 sostituzione/i | virgola |
| deck/tutorial.ehp | strTbl_g.bin | 155 | 1 sostituzione/i | virgola / costruzione |
| deck/tutorial.ehp | strTbl_g.bin | 156 | 1 sostituzione/i | ortografia |
| deck/tutorial.ehp | strTbl_g.bin | 157 | 1 sostituzione/i | virgola |
| deck/tutorial.ehp | strTbl_g.bin | 159 | 1 sostituzione/i | virgole |
| deck/tutorial.ehp | strTbl_g.bin | 161 | 1 sostituzione/i | virgola |
| deck/tutorial.ehp | strTbl_g.bin | 163 | 1 sostituzione/i | pronome mancante |
| deck/tutorial.ehp | strTbl_g.bin | 165 | 1 sostituzione/i | virgola |
| deck/tutorial.ehp | strTbl_g.bin | 169 | 1 sostituzione/i | virgola |
| deck/tutorial.ehp | strTbl_g.bin | 179 | 1 sostituzione/i | frase non grammaticale |
| deck/tutorial.ehp | strTbl_g.bin | 180 | 1 sostituzione/i | plurale |
| deck/tutorial.ehp | strTbl_g.bin | 186 | 1 sostituzione/i | maiuscola, virgola |
| deck/tutorial.ehp | strTbl_g.bin | 189 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_g.bin | 190 | 1 sostituzione/i | virgola, trattino |
| deck/tutorial.ehp | strTbl_g.bin | 198 | 1 sostituzione/i | ortografia |
| deck/tutorial.ehp | strTbl_g.bin | 203 | 1 sostituzione/i | virgole |
| deck/tutorial.ehp | strTbl_g.bin | 209 | 1 sostituzione/i | virgola |
| deck/tutorial.ehp | strTbl_g.bin | 210 | 1 sostituzione/i | voce di menu sbagliata (EN: Run), virgola |
| deck/tutorial.ehp | strTbl_g.bin | 215 | 1 sostituzione/i | plurale |
| deck/tutorial.ehp | strTbl_g.bin | 216 | 1 sostituzione/i | grammatica |
| deck/tutorial.ehp | strTbl_g.bin | 218 | 1 sostituzione/i | parola doppia |
| deck/tutorial.ehp | strTbl_g.bin | 220 | 1 sostituzione/i | virgola |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 23 | 1 sostituzione/i | maiuscola/trattino |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 24 | 1 sostituzione/i | maiuscola/trattino |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 48 | 1 sostituzione/i | grammatica (EN: Press the □ button to go back.) |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 60 | 1 sostituzione/i | maiuscola |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 63 | 1 sostituzione/i | parola tagliata |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 66 | 1 sostituzione/i | residuo francese |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 68 | 1 sostituzione/i | plurale (LP) |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 75 | 1 sostituzione/i | maiuscola |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 76 | 1 sostituzione/i | virgola |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 80 | 1 sostituzione/i | concordanza (LP plurale) |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 87 | 1 sostituzione/i | maiuscola |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 88 | 1 sostituzione/i | virgola |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 59 | 1 sostituzione/i | ortografia |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 66 | 1 sostituzione/i | composto |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 115 | 2 sostituzione/i | refuso, maiuscola |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 118 | 1 sostituzione/i | virgola |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 119 | 3 sostituzione/i | preposizione, virgola, relativo |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 120 | 1 sostituzione/i | refuso |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 136 | 1 sostituzione/i | virgolette e virgola |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 150 | 3 sostituzione/i | grammatica, Duell (EN: loser of the previous Duel) |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 154 | 2 sostituzione/i | concordanza |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 155 | 1 sostituzione/i | virgola |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 157 | 1 sostituzione/i | das/dass |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 158 | 1 sostituzione/i | articolo, maiuscola |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 159 | 3 sostituzione/i | refusi |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 160 | 1 sostituzione/i | grammatica |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 161 | 1 sostituzione/i | concordanza |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 163 | 3 sostituzione/i | refuso, virgola, plurale |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 167 | 1 sostituzione/i | grammatica |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 168 | 3 sostituzione/i | virgole, verbo mancante |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 169 | 2 sostituzione/i | refuso, caso |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 171 | 2 sostituzione/i | refuso, virgola, preposizione |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 172 | 2 sostituzione/i | virgola, parola doppia |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 173 | 1 sostituzione/i | maiuscola |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 174 | 1 sostituzione/i | grammatica |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 175 | 1 sostituzione/i | parentesi chiusa mancante |
| field/always_*_ger.ehp | field_strtbl.bin | 14 | 1 sostituzione/i | refuso, pronome |
| field/always_*_ger.ehp | field_strtbl.bin | 21 | 1 sostituzione/i | voce di menu in minuscolo (EN: Give) |
| field/always_*_ger.ehp | field_strtbl.bin | 22 | 1 sostituzione/i | voce di menu (EN: Eat) |
| field/always_*_ger.ehp | field_strtbl.bin | 47 | 1 sostituzione/i | aggettivi minuscoli |
| field/always_*_ger.ehp | field_strtbl.bin | 64 | 1 sostituzione/i | trattino |
| field/always_*_ger.ehp | field_strtbl.bin | 67 | 1 sostituzione/i | residuo inglese |
| field/always_*_ger.ehp | field_strtbl.bin | 100 | 1 sostituzione/i | virgola |
| field/always_*_ger.ehp | field_strtbl_item.bin | 70 | 1 sostituzione/i | trattino (come nei dialoghi) |
| field/always_*_ger.ehp | field_strtbl_item.bin | 75 | 1 sostituzione/i | trattino (come nei dialoghi) |
| field/always_*_ger.ehp | field_strtbl_item.bin | 88 | 1 sostituzione/i | refuso, concordanza (come nei dialoghi) |
| field/always_*_ger.ehp | field_strtbl_item.bin | 94 | 1 sostituzione/i | genitivo senza apostrofo (come nei dialoghi) |
| field/always_*_ger.ehp | field_strtbl_item.bin | 98 | 1 sostituzione/i | interfisso -s- |
| field/always_*_ger.ehp | field_strtbl_item.bin | 105 | 1 sostituzione/i | ortografia riformata |
| field/always_*_ger.ehp | field_strtbl_item.bin | 107 | 1 sostituzione/i | virgola |
| field/always_*_ger.ehp | field_strtbl_item.bin | 156 | 1 sostituzione/i | caso |
| field/always_*_ger.ehp | field_strtbl_item.bin | 160 | 1 sostituzione/i | composto |
| field/always_*_ger.ehp | field_strtbl_item.bin | 164 | 2 sostituzione/i | maiuscola, punto |
| field/always_*_ger.ehp | field_strtbl_item.bin | 168 | 1 sostituzione/i | caso |
| field/always_*_ger.ehp | field_strtbl_item.bin | 169 | 1 sostituzione/i | caso, frase |
| field/always_*_ger.ehp | field_strtbl_item.bin | 170 | 2 sostituzione/i | caso, trattino |
| field/always_*_ger.ehp | field_strtbl_item.bin | 172 | 1 sostituzione/i | refuso |
| field/always_*_ger.ehp | field_strtbl_item.bin | 177 | 1 sostituzione/i | caso, virgola |
| field/always_*_ger.ehp | field_strtbl_item.bin | 182 | 1 sostituzione/i | caso |
| field/always_*_ger.ehp | field_strtbl_item.bin | 189 | 1 sostituzione/i | grammatica |
| field/always_*_ger.ehp | field_strtbl_item.bin | 193 | 1 sostituzione/i | refuso, come nei dialoghi |
| field/always_*_ger.ehp | field_strtbl_item.bin | 194 | 1 sostituzione/i | plurale |
| field/always_*_ger.ehp | field_strtbl_item.bin | 200 | 1 sostituzione/i | concordanza |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 1 | 1 sostituzione/i | trattini |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 19 | 1 sostituzione/i | caso; senza articolo come gli altri luoghi (il dialogo dice 'Verlasse das 《M006_2》') |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 20 | 1 sostituzione/i | traduzione mancante (EN: Library) |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 21 | 1 sostituzione/i | traduzione mancante (EN: Roof) |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 25 | 1 sostituzione/i | traduzione mancante (EN: Ruins) |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 22 | 1 sostituzione/i | residuo inglese |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 24 | 1 sostituzione/i | traduzione sbagliata (EN: Abandoned Dorm) |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 30 | 1 sostituzione/i | residuo inglese (come nei dialoghi: Spezial-Finalarena) |
| labo/conv_machine.ehp | strTbl_g.bin | 2 | 1 sostituzione/i | maiuscola |
| labo/password.ehp | strTbl_g.bin | 1 | 1 sostituzione/i | virgola |
| labo/password.ehp | strTbl_g.bin | 10 | 1 sostituzione/i | composto |
| labo/password.ehp | strTbl_g.bin | 11 | 1 sostituzione/i | articolo |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 4 | 1 sostituzione/i | numero (EN: Opened File) |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 5 | 1 sostituzione/i | refuso |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 19 | 1 sostituzione/i | maiuscola |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 71 | 1 sostituzione/i | spazio prima dell'a capo |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 72 | 1 sostituzione/i | spazio prima dell'a capo |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 73 | 2 sostituzione/i | grammatica, virgola |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 74 | 1 sostituzione/i | refuso |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 34 | 1 sostituzione/i | grammatica |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 36 | 1 sostituzione/i | spazio |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 40 | 1 sostituzione/i | grammatica |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 41 | 1 sostituzione/i | grammatica |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 45 | 1 sostituzione/i | virgola, articolo |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 46 | 1 sostituzione/i | refuso, spazio |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 66 | 1 sostituzione/i | articolo, virgola |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 71 | 1 sostituzione/i | grammatica |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 72 | 1 sostituzione/i | refuso |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 115 | 1 sostituzione/i | caso |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 117 | 1 sostituzione/i | virgola |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 121 | 2 sostituzione/i | Sie/du misto, traduzione sbagliata (EN: main menu) |
| field/always_*_ger.ehp | event_name.bin | 1 | 1 sostituzione/i | grammatica |
| field/always_*_ger.ehp | event_name.bin | 2 | 1 sostituzione/i | articolo |
| field/always_*_ger.ehp | event_name.bin | 3 | 1 sostituzione/i | articolo |
| field/always_*_ger.ehp | event_name.bin | 7 | 1 sostituzione/i | articolo |
| field/always_*_ger.ehp | event_name.bin | 4 | 1 sostituzione/i | grammatica |
| field/always_*_ger.ehp | event_name.bin | 5 | 1 sostituzione/i | residuo inglese |
| field/always_*_ger.ehp | event_name.bin | 11 | 1 sostituzione/i | trattini |
| duel/basic_*.ehp | option_msg_g.bin | 19 | 1 sostituzione/i | virgola |
| duel/basic_*.ehp | option_msg_g.bin | 24 | 1 sostituzione/i | virgola |
| duel/basic_*.ehp | option_msg_g.bin | 26 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 1 | 1 sostituzione/i | refuso |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 9 | 1 sostituzione/i | plurale |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 19 | 1 sostituzione/i | maiuscola |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 24 | 1 sostituzione/i | maiuscola, genere |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 35 | 1 sostituzione/i | maiuscola, genere |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 37 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 40 | 1 sostituzione/i | maiuscola, genere |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 45 | 1 sostituzione/i | maiuscola, genere |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 56 | 1 sostituzione/i | spazio, genere |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 57 | 2 sostituzione/i | maiuscola, genere, coniugazione |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 59 | 2 sostituzione/i | refuso, genere |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 60 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 61 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 71 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 87 | 2 sostituzione/i | spazio, refuso |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 104 | 1 sostituzione/i | separatore migliaia coerente |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 106 | 1 sostituzione/i | composto |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 108 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 112 | 1 sostituzione/i | punteggiatura |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 121 | 1 sostituzione/i | parola doppia |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 128 | 1 sostituzione/i | spazio/virgola |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 134 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 135 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 137 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 140 | 1 sostituzione/i | parola mancante |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 19 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 21 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 15 | 1 sostituzione/i | parola doppia |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 29 | 1 sostituzione/i | genitivo |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 35 | 1 sostituzione/i | separatore migliaia coerente |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 39 | 1 sostituzione/i | trattino residuo |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 55 | 1 sostituzione/i | refuso |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 60 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 61 | 1 sostituzione/i | articolo mancante |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 67 | 1 sostituzione/i | parola doppia |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 69 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 70 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 74 | 1 sostituzione/i | spazio |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 82 | 1 sostituzione/i | puntini |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 87 | 1 sostituzione/i | participio |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 88 | 2 sostituzione/i | traduzione sbagliata, negazione mancante |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 89 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 92 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 101 | 4 sostituzione/i | traduzione sbagliata (EN: Remember), genere, caso |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 7 | 1 sostituzione/i | trattino |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 8 | 1 sostituzione/i | trattino, plurale |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 10 | 1 sostituzione/i | plurale |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 23 | 1 sostituzione/i | traduzione sbagliata (EN: DEF) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 47 | 1 sostituzione/i | caso |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 42 | 1 sostituzione/i | frase troncata |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 54 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 55 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 56 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 59 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 61 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 69 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 74 | 1 sostituzione/i | maiuscola |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 76 | 1 sostituzione/i | caso |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 102 | 1 sostituzione/i | traduzione sbagliata (EN: set or use) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 103 | 1 sostituzione/i | maiuscola |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 115 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 121 | 1 sostituzione/i | parola doppia |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 122 | 1 sostituzione/i | grammatica, traduzione (EN: face-down) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 127 | 1 sostituzione/i | coniugazione |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 131 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 132 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 133 | 2 sostituzione/i | tasti scambiati (EN: ○ apre, × conferma) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 134 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 137 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 140 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 141 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 144 | 1 sostituzione/i | imperativo |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 148 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 149 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 150 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 151 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 152 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 153 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 154 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 161 | 1 sostituzione/i | numero |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 164 | 1 sostituzione/i | coniugazione |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 169 | 1 sostituzione/i | coniugazione |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 172 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 176 | 1 sostituzione/i | nome diverso dall'inglese (EN: Syrus) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 178 | 1 sostituzione/i | composto |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 186 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 187 | 3 sostituzione/i | genere, sillabazione, frase troncata |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 188 | 2 sostituzione/i | negazione sbagliata (EN: can be used in the following cases) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 189 | 1 sostituzione/i | sillabazione |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 192 | 1 sostituzione/i | sillabazione |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 15 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 25 | 1 sostituzione/i | codice colore sbagliato |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 27 | 1 sostituzione/i | sillabazione |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 30 | 1 sostituzione/i | refuso |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 33 | 2 sostituzione/i | genere, grammatica |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 35 | 2 sostituzione/i | grammatica, genere |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 36 | 1 sostituzione/i | traduzione sbagliata (EN: cut its original ATK in half) |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 37 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 47 | 2 sostituzione/i | virgola, punto |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 49 | 1 sostituzione/i | virgola, composto |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 55 | 1 sostituzione/i | numero |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 56 | 1 sostituzione/i | numero |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 60 | 1 sostituzione/i | numero |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 69 | 1 sostituzione/i | codice colore sbagliato |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 85 | 1 sostituzione/i | numero, sillabazione |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 90 | 1 sostituzione/i | numero |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 92 | 1 sostituzione/i | refuso |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 109 | 2 sostituzione/i | grammatica, genere |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 121 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 122 | 1 sostituzione/i | termine incoerente (Gegnerrunde) |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 125 | 1 sostituzione/i | caso |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 128 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 129 | 2 sostituzione/i | nome carta sbagliato (EN: Shrink), spazio |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 135 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 151 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 152 | 1 sostituzione/i | genere |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 153 | 1 sostituzione/i | grammatica |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 175 | 2 sostituzione/i | spazio, articolo |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 179 | 1 sostituzione/i | genere |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 38 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 55 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 95 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 104 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 105 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 112 | 4 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 123 | 3 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 127 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 129 | 3 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 130 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 131 | 3 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 135 | 2 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 138 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 141 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 142 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 143 | 2 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 144 | 3 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 145 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 147 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 148 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 176 | 3 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 177 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 178 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 179 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 181 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 182 | 3 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 183 | 2 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 185 | 2 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 186 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 187 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 191 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 192 | 2 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 193 | 1 sostituzione/i | come in deck/all_g.ehp help_strtbl_contents.bin |

### Correzioni puntuali `ui_texts.json`
| file | membro | indice | vecchio | nuovo | motivo |
|---|---|---|---|---|---|

### Elenco completo
**Confronto completo con parole evidenziate: `docs/changes_de/ui_strings_diff.md`.** Dati grezzi: `docs/changes_de/ui_strings.csv`. Prime 40:

| membro | indice | originale | nuovo |
|---|---|---|---|
| strTbl_g.bin | 4 | Slifer-Red | Slifer Rot |
| strTbl_g.bin | 5 | Ra-Yellow | Ra Gelb |
| strTbl_g.bin | 6 | Obelisk-Blue | Obelisk Blau |
| strTbl_g.bin | 12 | Wenn es um Duelle geht, dann ist Jaden die Nummer Eins in Slifer-Red oder anders ausgedrückt, er ist der beste Duellant von allen Schülern des neuen Jahrgangs. Er hat eine natürlich Begabung, wie sie nur ganz wenige haben. ⏎Das Geheimnis seiner Stärke liegt in seiner Hartnäckigkeit. Ganz egal in was für einem Schlamassel er auch steckt, er kommt da immer ohne Probleme wieder raus.⏎⏎Wann immer er nur noch wenig Karten in der Hand hat, ist Bubbleman für ihn da.⏎⏎Er ist bekannt dafür, dass er viele Elementarheld in seinem Deck hat. Diese Elementarheld ähneln den Helden, die er in seiner Kindheit bewundert hat.⏎⏎Er setzt häufig seine Elementarheld in verschiedenen Situationen ein, diese Taktik beherrscht er besonders gut.⏎Dies, in Verbindung mit seinem außergewöhnlichen Glück beim Kartenziehen, erlaubt ihm Gegner schnell zu schlagen, wenn er erstmal in sein Spiel gefunden hat.⏎⏎Was seine Persönlichkeit angeht ist Jaden ein sorgloser und fröhlicher Teenager, der glaubt, dass Spaß das wichtigste bei einem Duell ist. Zuerst konnte er an der strengen Duell Akademie nicht viele Freunde finden, aber durch Duelle bemerkten die anderen seine fröhliche Art und behandelten ihn freundlicher.⏎⏎Seine Gedanken über Mädchen sind ein Mysterium.⏎Manchmal ist ein Mädchen in ihn verknallt, aber er hat selten, wenn überhaupt, irgendein Interesse gezeigt.⏎⏎Was das Essen angeht, so hat er keine besonderen Vorlieben oder Abneigungen. Er isst beinahe alles. | Wenn es um Duelle geht, dann ist Jaden die Nummer Eins in Slifer Rot oder anders ausgedrückt, er ist der beste Duellant von allen Schülern des neuen Jahrgangs. Er hat eine natürliche Begabung, wie sie nur ganz wenige haben. ⏎Das Geheimnis seiner Stärke liegt in seiner Hartnäckigkeit. Ganz egal in was für einem Schlamassel er auch steckt, er kommt da immer ohne Probleme wieder raus.⏎⏎Wann immer er nur noch wenig Karten in der Hand hat, ist Bubbleman für ihn da.⏎⏎Er ist bekannt dafür, dass er viele Elementarhelden in seinem Deck hat. Diese Elementarhelden ähneln den Helden, die er in seiner Kindheit bewundert hat.⏎⏎Er setzt häufig seine Elementarhelden in verschiedenen Situationen ein, diese Taktik beherrscht er besonders gut.⏎Dies, in Verbindung mit seinem außergewöhnlichen Glück beim Kartenziehen, erlaubt ihm Gegner schnell zu schlagen, wenn er erstmal in sein Spiel gefunden hat.⏎⏎Was seine Persönlichkeit angeht ist Jaden ein sorgloser und fröhlicher Teenager, der glaubt, dass Spaß das wichtigste bei einem Duell ist. Zuerst konnte er an der strengen Duellakademie nicht viele Freunde finden, aber durch Duelle bemerkten die anderen seine fröhliche Art und behandelten ihn freundlicher.⏎⏎Seine Gedanken über Mädchen sind ein Mysterium.⏎Manchmal ist ein Mädchen in ihn verknallt, aber er hat selten, wenn überhaupt, irgendein Interesse gezeigt.⏎⏎Was das Essen angeht, so hat er keine besonderen Vorlieben oder Abneigungen. Er isst beinahe alles. |
| strTbl_g.bin | 13 | Syrus bewundert Jaden sehr und sieht zu ihm auf, wie zu einem großen Bruder. Aber er hat auch einen wirklichen älteren Bruder, deshalb hat er für die beiden unterschiedliche Spitznamen.⏎⏎Er respektiert starke und verlässliche Persönlichkeiten, aber er fühlt sich in ihrer Gegenwart immer ein bisschen unterlegen. Er möchte eines Tages so stark wie Jaden sein.⏎⏎Syrus hat nicht viel Selbstvertrauen in seine eigenen Fähigkeiten. Das mag der Grund sein, warum er immer so eine negative Einstellung zu allem hat.⏎Aber auf der anderen Seite kann er auch oft sehr kritisch gegenüber anderen sein.⏎⏎Er hat für gewöhnlich eine negative und halbherzige Einstellung bei seinen Duellen, dies lässt ihn immer glauben, dass er gar nicht gewinnen kann. Aber seit er Jaden getroffen hat, ändert sich seine negative Einstellung langsam zu einer positiveren Einstellung.⏎⏎Syrus liebt alle Arten von Fahrzeugen, deshalb benutzt er in seinem Deck viele verschiedene „Vehicroid“-Karten. „Vehicroids“ sind eine Art Fahrzeug.⏎Er hat einen niedlichen, jungenhaften Charme auf den ersten Blick, aber er ist eigentlich recht stark.⏎⏎Er verliebt sich leicht Hals über Kopf in irgendwelche hübschen Mädchen, aber bis jetzt hat er in seinem Leben noch keine ernsthafte Beziehung gehabt.⏎⏎Syrus Lieblingsessen wird einmal im Monat in der Slifer Red Cafeteria angeboten.⏎Aber er verträgt kein scharfes Essen. | Syrus bewundert Jaden sehr und sieht zu ihm auf, wie zu einem großen Bruder. Aber er hat auch einen wirklichen älteren Bruder, deshalb hat er für die beiden unterschiedliche Spitznamen.⏎⏎Er respektiert starke und verlässliche Persönlichkeiten, aber er fühlt sich in ihrer Gegenwart immer ein bisschen unterlegen. Er möchte eines Tages so stark wie Jaden sein.⏎⏎Syrus hat nicht viel Selbstvertrauen in seine eigenen Fähigkeiten. Das mag der Grund sein, warum er immer so eine negative Einstellung zu allem hat.⏎Aber auf der anderen Seite kann er auch oft sehr kritisch gegenüber anderen sein.⏎⏎Er hat für gewöhnlich eine negative und halbherzige Einstellung bei seinen Duellen, dies lässt ihn immer glauben, dass er gar nicht gewinnen kann. Aber seit er Jaden getroffen hat, ändert sich seine negative Einstellung langsam zu einer positiveren Einstellung.⏎⏎Syrus liebt alle Arten von Fahrzeugen, deshalb benutzt er in seinem Deck viele verschiedene „Vehicroid“-Karten. „Vehicroids“ sind eine Art Fahrzeug.⏎Er hat einen niedlichen, jungenhaften Charme auf den ersten Blick, aber er ist eigentlich recht stark.⏎⏎Er verliebt sich leicht Hals über Kopf in irgendwelche hübschen Mädchen, aber bis jetzt hat er in seinem Leben noch keine ernsthafte Beziehung gehabt.⏎⏎Syrus' Lieblingsessen wird einmal im Monat in der Slifer-Rot-Cafeteria angeboten.⏎Aber er verträgt kein scharfes Essen. |
| strTbl_g.bin | 14 | Chumley ist eigentlich ein ganz gemütlicher Kerl.⏎Er hat eine offene und ehrliche Persönlichkeit.⏎Chumley glaubt, dass es bei einem Duell um mehr gehen sollte als gewinnen und verlieren. Diese Einstellung mag der Grund gewesen sein, dass er das erste Jahr an der strengen Duellakademie wiederholen muss. Er fühlt sich für die Akademie irgendwie ungeeignet.⏎Das bedeutet aber nicht, dass er ein schlechter Duellant ist. Ganz im Gegenteil, er beherrscht die Fähigkeit die Stimme des Geistes des Duells zu hören.⏎⏎Er war auf einem Klassenausflug in Australien und hatte dort einen recht positiven Eindruck von dem Land. Deshalb benutzt er jetzt ein Deck mit vielen Karten, die irgendwie mit Australien zu tun haben.⏎⏎Vielleicht vermisst er seine Mutter, deshalb behält er wohl eine Sammelkarte von einem weiblichen Pop Star, die schon... einmal bessere Zeiten gesehen hat.⏎⏎Chumley hat kein besonderes Lieblingsessen, aber er scheint Fleisch zu vermeiden.⏎⏎Dafür isst er recht oft Fisch. | Chumley ist eigentlich ein ganz gemütlicher Kerl.⏎Er hat eine offene und ehrliche Persönlichkeit.⏎Chumley glaubt, dass es bei einem Duell um mehr gehen sollte als gewinnen und verlieren. Diese Einstellung mag der Grund gewesen sein, dass er das erste Jahr an der strengen Duellakademie wiederholen muss. Er fühlt sich für die Akademie irgendwie ungeeignet.⏎Das bedeutet aber nicht, dass er ein schlechter Duellant ist. Ganz im Gegenteil, er beherrscht die Fähigkeit die Stimme des Geistes des Duells zu hören.⏎⏎Er war auf einem Klassenausflug in Australien und hatte dort einen recht positiven Eindruck von dem Land. Deshalb benutzt er jetzt ein Deck mit vielen Karten, die irgendwie mit Australien zu tun haben.⏎⏎Vielleicht vermisst er seine Mutter, deshalb behält er wohl eine Sammelkarte von einem weiblichen Pop Star, die schon ... einmal bessere Zeiten gesehen hat.⏎⏎Chumley hat kein besonderes Lieblingsessen, aber er scheint Fleisch zu vermeiden.⏎⏎Dafür isst er recht oft Fisch. |
| strTbl_g.bin | 15 | Alexis ist die beste Duellantin unter den Mädchen. Sie ist auch stark genug, um sich gegen die Jungs zu behaupten.⏎Sie ist auch recht ansehnlich. Aus diesem Grund wird sie von einigen auch die „Madonna der Akademie“ genannt.⏎Alexis ist mit Verstand und Schönheit gesegnet und wird aus diesem Grund von den anderen Mädchen beneidet.⏎Sie hat ein mutiges Naturell. Aber aufgrund ihres starken Drangs unbedingt zu siegen, werden ihre Taten und Worte oft als zu schroff empfunden.⏎⏎Sie benutzt ein recht ungewöhnliches Deck, das „Cyber Girl“ genannt wird. Es enthält hauptsächlich attraktive weibliche Monster.⏎Eine von ihnen ist „Cyber-Klingen“, mit einem Effekt, der Alexis schon öfters aus der Klemme gehauen hat, als sie zählen kann.⏎Alexis scheint im Moment noch kein Interesse an den Jungs zu haben.⏎Stattdessen konzentriert sie sich auf ihre „Liebe für das Duell“ und diese Liebe kann man in ihrem Spiel eindeutig sehen.⏎⏎Sie mag besonders süßes und gesundes Essen, aber sie versucht Essen mit starken Geruch zu vermeiden. | Alexis ist die beste Duellantin unter den Mädchen. Sie ist auch stark genug, um sich gegen die Jungs zu behaupten.⏎Sie ist auch recht ansehnlich. Aus diesem Grund wird sie von einigen auch die „Madonna der Akademie“ genannt.⏎Alexis ist mit Verstand und Schönheit gesegnet und wird aus diesem Grund von den anderen Mädchen beneidet.⏎Sie hat ein mutiges Naturell. Aber aufgrund ihres starken Drangs unbedingt zu siegen, werden ihre Taten und Worte oft als zu schroff empfunden.⏎⏎Sie benutzt ein recht ungewöhnliches Deck, das „Cyber Girl“ genannt wird. Es enthält hauptsächlich attraktive weibliche Monster.⏎Eine von ihnen ist „Cyber-Klingen“, mit einem Effekt, der Alexis schon öfters aus der Klemme gehauen hat, als sie zählen kann.⏎Alexis scheint im Moment noch kein Interesse an den Jungs zu haben.⏎Stattdessen konzentriert sie sich auf ihre „Liebe für das Duell“ und diese Liebe kann man in ihrem Spiel eindeutig sehen.⏎⏎Sie mag besonders süßes und gesundes Essen, aber sie versucht Essen mit starkem Geruch zu vermeiden. |
| strTbl_g.bin | 16 | Von Chazz hatte man eigentlich gedacht, dass er die Duellakademie verlassen⏎hätte, weil sein Stolz als Eliteduellant zerstört wurde. Aber er kam mit einem beharrlichen Kampfgeist wieder⏎Er kann schon recht überheblich sein, aber vielleicht liegt es an seiner Erfahrung ganz unten zu sein, dass er nicht mehr so kalt ist wie früher. ⏎Er scheint als Mensch unglaublich gewachsen zu sein. Und deshalb kann er jetzt auch die Stimme des Geistes hören.⏎⏎Er hatte schon viele Decks benutzt, aber jetzt scheint er das „Ojama-Trio“ zu benutzen. ⏎Chazz hatte sich früher mehr auf Kraft verlassen, aber jetzt vetraut er mehr auf Technik.⏎⏎Er respektiert nun die Angehörigen von Slifer-Red ein bisschen mehr, als er es früher getan hat.⏎⏎Chazz liebt es luxuriöses Essen zu essen, aber er mag kein Gemüse. | Von Chazz hatte man eigentlich gedacht, dass er die Duellakademie verlassen⏎hätte, weil sein Stolz als Eliteduellant zerstört wurde. Aber er kam mit einem beharrlichen Kampfgeist wieder.⏎Er kann schon recht überheblich sein, aber vielleicht liegt es an seiner Erfahrung ganz unten zu sein, dass er nicht mehr so kalt ist wie früher. ⏎Er scheint als Mensch unglaublich gewachsen zu sein. Und deshalb kann er jetzt auch die Stimme des Geistes hören.⏎⏎Er hatte schon viele Decks benutzt, aber jetzt scheint er das „Ojama-Trio“ zu benutzen. ⏎Chazz hatte sich früher mehr auf Kraft verlassen, aber jetzt vertraut er mehr auf Technik.⏎⏎Er respektiert nun die Angehörigen von Slifer Rot ein bisschen mehr, als er es früher getan hat.⏎⏎Chazz liebt es luxuriöses Essen zu essen, aber er mag kein Gemüse. |
| strTbl_g.bin | 17 | Ein talentierter Duellant des neuen Jahrgangs im Haus Obelisk-Blue. Einige sind sogar so weit gegangen ihn als Zanes Nachfolger zu bezeichnen.⏎Jüngster der Elitegruppe Princeton, er wird als sehr hochrangiger Dueallant betrachtet. Und auch auf der sozialen Leiter steht er weit oben.⏎Man erwartet, dass er den Titel des Spitzenduellant von seinen beiden älteren Brüdern übernimmt.  Zusammen mit diesen hohen Erwartungen kommt auch eine gehörige Portion Arroganz. Er betrachtet jeden mit einem niedrigeren Stand als unterlegen und er hat eine sehr stolze Einstellung.⏎⏎Er ist sehr konzentriert während eines Duells.⏎Der durchschnittliche Duellant ist seinem aggressiven Stil und seiner Stärke nicht gewachsen.⏎Vielleicht aufgrund seines hohen sozialen Status ist er sehr nett zu Mädchen, vielleicht sogar ein bisschen feministisch.⏎⏎Duellanten von Slifer-Red können bestimmt keine Freundschaft mit ihm ⏎schließen, es sei denn er ändert seine hochnäsige Einstellung. | Ein talentierter Duellant des neuen Jahrgangs im Haus Obelisk Blau. Einige sind sogar so weit gegangen ihn als Zanes Nachfolger zu bezeichnen.⏎Jüngster der Elitegruppe Princeton, er wird als sehr hochrangiger Duellant betrachtet. Und auch auf der sozialen Leiter steht er weit oben.⏎Man erwartet, dass er den Titel des Spitzenduellanten von seinen beiden älteren Brüdern übernimmt. Zusammen mit diesen hohen Erwartungen kommt auch eine gehörige Portion Arroganz. Er betrachtet jeden mit einem niedrigeren Stand als unterlegen und er hat eine sehr stolze Einstellung.⏎⏎Er ist sehr konzentriert während eines Duells.⏎Der durchschnittliche Duellant ist seinem aggressiven Stil und seiner Stärke nicht gewachsen.⏎Vielleicht aufgrund seines hohen sozialen Status ist er sehr nett zu Mädchen, vielleicht sogar ein bisschen feministisch.⏎⏎Duellanten von Slifer Rot können bestimmt keine Freundschaft mit ihm ⏎schließen, es sei denn er ändert seine hochnäsige Einstellung. |
| strTbl_g.bin | 18 | Bastion ist ein brillanter Schüler. Er hatte das beste Ergebnis beim Aufnahmetest der Akademie geschafft.⏎Er war der erste Junge dieses Jahrgangs, der ein Mitglied von Obelisk-Blue wurde.⏎Bastion hat eine sehr ernste Seite, aber er kann auch sehr offenherzig sein. Auch wenn er einen höheren Rang als die Duellanten von Slifer-Red hat, betrachtet er sie nicht als unterlegen.⏎⏎Während seiner Freizeit berechnet Bastion irgendwelche Pläne und schreibt sie dann auf alles, was er gerade finden kann.⏎Deshalb sind die Wände in seinem Raum mit Zahlen und Formeln bedeckt, wie Graffiti. Sogar auf seinen Karten befinden sich mathematische Formeln. Diese seltsame Angewohnheit zeigt sich auch während Duellen. Er berechnet den Spielstil seines Gegners und verwendet seine Ergebnisse um seine Spieltaktik anzupassen.⏎Während Jaden eine natürliche Begabung hat, die ihn zu einem ⏎außergewöhnlichen Duellanten macht, so ist es bei Bastion seine ⏎Hartnäckigkeit und harte Arbeit, die ihn zu was Besonderem macht.⏎⏎Er behauptet sechs verschiedene Decks mit sechs Eigenschaften zu haben und sie entsprechend seinem jeweiligen Gegner einzusetzen. Er sagt, dass jedes dieser Decks perfekt aufgebaut ist.⏎Aber aus irgendeinem Grund kann man ihn selten bei einem Duell sehen.⏎⏎Bastion hat eine menge Potential wenn man seine hohe Intelligenz, seine Persönlichkeit und seine Duellfähigkeiten bedenkt. Aber sein Schwachpunkt ist seine „Abwesenheit“, wegen der er von den anderen die kalte Schulter gezeigt bekommt.⏎⏎Er betont immer kein Interesse an Mädchen zu haben, aber wenn sie ihn um Hilfe bitten, dann reißt er sich ein Bein aus um zu helfen.⏎Bastions Deck besteht aus Karten mit niedlichen, unterwürfig-aussehenden ⏎Mädchen, aber im wirklichen Leben bevorzugt er starke Frauen.⏎⏎Er ist am liebsten Gemüse und scheint sehr Gesundheitsbewusst zu sein.⏎Auf der anderen Seite mag er kein Obst und scheint Süßes nicht zu mögen. | Bastion ist ein brillanter Schüler. Er hatte das beste Ergebnis beim Aufnahmetest der Akademie geschafft.⏎Er war der erste Junge dieses Jahrgangs, der ein Mitglied von Obelisk Blau wurde.⏎Bastion hat eine sehr ernste Seite, aber er kann auch sehr offenherzig sein. Auch wenn er einen höheren Rang als die Duellanten von Slifer Rot hat, betrachtet er sie nicht als unterlegen.⏎⏎Während seiner Freizeit berechnet Bastion irgendwelche Pläne und schreibt sie dann auf alles, was er gerade finden kann.⏎Deshalb sind die Wände in seinem Raum mit Zahlen und Formeln bedeckt, wie Graffiti. Sogar auf seinen Karten befinden sich mathematische Formeln. Diese seltsame Angewohnheit zeigt sich auch während Duellen. Er berechnet den Spielstil seines Gegners und verwendet seine Ergebnisse um seine Spieltaktik anzupassen.⏎Während Jaden eine natürliche Begabung hat, die ihn zu einem ⏎außergewöhnlichen Duellanten macht, so ist es bei Bastion seine ⏎Hartnäckigkeit und harte Arbeit, die ihn zu was Besonderem macht.⏎⏎Er behauptet sechs verschiedene Decks mit sechs Eigenschaften zu haben und sie entsprechend seinem jeweiligen Gegner einzusetzen. Er sagt, dass jedes dieser Decks perfekt aufgebaut ist.⏎Aber aus irgendeinem Grund kann man ihn selten bei einem Duell sehen.⏎⏎Bastion hat eine Menge Potential wenn man seine hohe Intelligenz, seine Persönlichkeit und seine Duellfähigkeiten bedenkt. Aber sein Schwachpunkt ist seine „Abwesenheit“, wegen der er von den anderen die kalte Schulter gezeigt bekommt.⏎⏎Er betont immer kein Interesse an Mädchen zu haben, aber wenn sie ihn um Hilfe bitten, dann reißt er sich ein Bein aus, um zu helfen.⏎Bastions Deck besteht aus Karten mit niedlichen, unterwürfig-aussehenden ⏎Mädchen, aber im wirklichen Leben bevorzugt er starke Frauen.⏎⏎Er isst am liebsten Gemüse und scheint sehr gesundheitsbewusst zu sein.⏎Auf der anderen Seite mag er kein Obst und scheint Süßes nicht zu mögen. |
| strTbl_g.bin | 19 | Zane ist der beste Duellant der Akademie. Er hat sich den Spitznamen „Bester Duellant der Akademie“ für seine unglaublichen Fertigkeiten verdient. ⏎Er ist immer der Beste. Sowohl in der Theorie als auch in der Praxis, ist er wirklich ein Vorbild in der Akademie.⏎Zane ist kein großer Redner, deshalb haben die Leute den Eindruck er sei kalt und leidenschaftslos. Aber jene, die sich die Mühe machen ihn näher kennen zu lernen, sehen vielleicht eine andere Seite von ihm. Wen man ihn näher kennt, dann ist er eine nette und freundliche Person.⏎⏎Zane liebt es „Cyber Drache“-Karten zu verwenden und starke Duelle zu spielen, passend für den Titel „Bester Duellant der Akademie“.⏎Seine Spezialität ist der Einsatz von „Kraftbündnis“ für einen mächtigen einzelnen Angriff.⏎⏎Er glaubt, dass es wichtiger ist sich anzustrengen den Gegner zu respektieren, als zu gewinnen.⏎Zane setzt immer seine gesamte Stärke bei jedem Duell ein und unterschätzt seinen Gegner niemals.⏎Er kommt mit jedem gut klar, der sich als würdiger Gegner bewiesen hat.⏎⏎Seine Erscheinung, Persönlichkeit und Fähigkeiten machen ihn sehr beliebt bei den weiblichen Studenten, eigentlich sogar zu dem beliebtesten Jungen der Schule.⏎Die Mädchen würden sich scharenweise melden, um seine Verabredung zum Abschlussball zu sein (wenn die Akademie denn einen Abschlussball ⏎hätte).⏎⏎Zane mag einfaches Essen. | Zane ist der beste Duellant der Akademie. Er hat sich den Spitznamen „Bester Duellant der Akademie“ für seine unglaublichen Fertigkeiten verdient. ⏎Er ist immer der Beste. Sowohl in der Theorie als auch in der Praxis, ist er wirklich ein Vorbild in der Akademie.⏎Zane ist kein großer Redner, deshalb haben die Leute den Eindruck er sei kalt und leidenschaftslos. Aber jene, die sich die Mühe machen ihn näher kennenzulernen, sehen vielleicht eine andere Seite von ihm. Wenn man ihn näher kennt, dann ist er eine nette und freundliche Person.⏎⏎Zane liebt es „Cyber Drache“-Karten zu verwenden und starke Duelle zu spielen, passend für den Titel „Bester Duellant der Akademie“.⏎Seine Spezialität ist der Einsatz von „Kraftbündnis“ für einen mächtigen einzelnen Angriff.⏎⏎Er glaubt, dass es wichtiger ist sich anzustrengen den Gegner zu respektieren, als zu gewinnen.⏎Zane setzt immer seine gesamte Stärke bei jedem Duell ein und unterschätzt seinen Gegner niemals.⏎Er kommt mit jedem gut klar, der sich als würdiger Gegner bewiesen hat.⏎⏎Seine Erscheinung, Persönlichkeit und Fähigkeiten machen ihn sehr beliebt bei den weiblichen Studenten, eigentlich sogar zu dem beliebtesten Jungen der Schule.⏎Die Mädchen würden sich scharenweise melden, um seine Verabredung zum Abschlussball zu sein (wenn die Akademie denn einen Abschlussball ⏎hätte).⏎⏎Zane mag einfaches Essen. |
| strTbl_g.bin | 20 | Als Professor des Haus der Jungen von Obelisk-Blue, ist Vellian Crowler verantwortlich für die besten Duellanten der Akademie.⏎Er hat eine sehr exzentrisch Art zu sprechen.⏎⏎Vellian ist ein Symbol für die strenge, siegesbesessene Philosophie der Duellakademie. Er behandelt die Schüler mit den besten Noten als seine Lieblinge und ist sehr intolerant gegenüber Schülern, die nicht mithalten können. Er behält Jaden Yuki von Slifer-Red immer im Auge und hat schon mehrere Male versucht ihn aus der Akademie rauswerfen zu lassen.⏎⏎Er trägt einen „Duell Mantel“ wenn er sich duelliert. Anscheinend kann „jeder, der erfolgreich der Akademie beigetreten ist, einen kaufen“, aber niemand ⏎außer Vellian trägt so einen.⏎⏎Er setzt ein Deck mit lauter „Antiker Antrieb“-Karten, „Antiker Antrieb“ ist eine Art von Maschinerie.⏎Seine Hauptkarte ist der Antiker Antriebsgolem“, eine Karte, die so mächtig ist, dass sie auch als der „Regelbrecher“ bekannt ist.⏎⏎Wie seine Erscheinung es einen schon vermuten lässt, ist Vellian ein Liebhaber von Spitzenqualität, dazu gehört auch Essen. | Als Professor des Hauses der Jungen von Obelisk Blau, ist Vellian Crowler verantwortlich für die besten Duellanten der Akademie.⏎Er hat eine sehr exzentrische Art zu sprechen.⏎⏎Vellian ist ein Symbol für die strenge, siegesbesessene Philosophie der Duellakademie. Er behandelt die Schüler mit den besten Noten als seine Lieblinge und ist sehr intolerant gegenüber Schülern, die nicht mithalten können. Er behält Jaden Yuki von Slifer Rot immer im Auge und hat schon mehrere Male versucht ihn aus der Akademie rauswerfen zu lassen.⏎⏎Er trägt einen „Duell Mantel“ wenn er sich duelliert. Anscheinend kann „jeder, der erfolgreich der Akademie beigetreten ist, einen kaufen“, aber niemand ⏎außer Vellian trägt so einen.⏎⏎Er setzt ein Deck mit lauter „Antiker Antrieb“-Karten, „Antiker Antrieb“ ist eine Art von Maschinerie.⏎Seine Hauptkarte ist der „Antiker Antriebsgolem“, eine Karte, die so mächtig ist, dass sie auch als der „Regelbrecher“ bekannt ist.⏎⏎Wie seine Erscheinung es einen schon vermuten lässt, ist Vellian ein Liebhaber von Spitzenqualität, dazu gehört auch Essen. |
| strTbl_g.bin | 21 | Lyman Banner ist ein Professor für Alchemie und steht dem Haus Slifer-Red vor. ⏎⏎Seine entspannte Persönlichkeit und seine zurückhaltende Stimme machen schwierig zu bestimmen, was für eine Person er wirklich ist.⏎⏎Lyman hat selten oder vielleicht sogar nie an einem Duell teilgenommen, weil er sich auf die Alchemie spezialisiert hat, dieser Kunst etwas aus dem Nichts zu erschaffen. Niemand hat eine Idee was für ein Deck er vielleicht benutzen⏎könnte.⏎⏎Auch wenn vieles in seinem Leben von Mysterien verhüllt wird, so ist doch eine Sache für jeden offensichtlich, seine Vorliebe für Katzen.⏎⏎Sogar sein Lieblingsessen ist ein Mysterium. | Lyman Banner ist ein Professor für Alchemie und steht dem Haus Slifer Rot vor. ⏎⏎Seine entspannte Persönlichkeit und seine zurückhaltende Stimme machen es schwierig zu bestimmen, was für eine Person er wirklich ist.⏎⏎Lyman hat selten oder vielleicht sogar nie an einem Duell teilgenommen, weil er sich auf die Alchemie spezialisiert hat, dieser Kunst etwas aus dem Nichts zu erschaffen. Niemand hat eine Idee was für ein Deck er vielleicht benutzen⏎könnte.⏎⏎Auch wenn vieles in seinem Leben von Mysterien verhüllt wird, so ist doch eine Sache für jeden offensichtlich, seine Vorliebe für Katzen.⏎⏎Sogar sein Lieblingsessen ist ein Mysterium. |
| strTbl_g.bin | 22 | Alexis älterer Bruder.⏎Ausgehend von Alexis Persönlichkeit könnte man annehmen, dass er ein strenger und zurückhaltender Junge wäre. Aber nichts könnte weiter von der Wahrheit entfernt sein. Atticus ist eigentlich wirklich lustig, vielleicht sogar schon zu lustig. Das durchschnittliche Mädchen wird von seiner charmanten Persönlichkeit und seinen witzigen Sprüchen überwältigt.⏎⏎Er ist auch ein exzellenter Duellant. Einige behaupten sogar, dass seine ⏎Fähigkeiten es mit denen von Zane aufnehmen können.⏎Anscheinend war er früher ein guter Freund des schweigsamen Zane. Man kann sich das nur schwer vorstellen, wie zwei so gegensätzliche Charaktere miteinander klarkommen.⏎⏎Atticus will immer, dass seine Schwester Alexis mehr wie die anderen Mädchen ist. Darum benimmt er sich ihr gegenüber ganz anders als sonst, um sie zu ⏎überzeugen sich weiblicher zu benehmen. Meistens endet es dann damit, dass sie sauer auf ihn wird. | Alexis' älterer Bruder.⏎Ausgehend von Alexis' Persönlichkeit könnte man annehmen, dass er ein strenger und zurückhaltender Junge wäre. Aber nichts könnte weiter von der Wahrheit entfernt sein. Atticus ist eigentlich wirklich lustig, vielleicht sogar schon zu lustig. Das durchschnittliche Mädchen wird von seiner charmanten Persönlichkeit und seinen witzigen Sprüchen überwältigt.⏎⏎Er ist auch ein exzellenter Duellant. Einige behaupten sogar, dass seine ⏎Fähigkeiten es mit denen von Zane aufnehmen können.⏎Anscheinend war er früher ein guter Freund des schweigsamen Zane. Man kann sich das nur schwer vorstellen, wie zwei so gegensätzliche Charaktere miteinander klarkommen.⏎⏎Atticus will immer, dass seine Schwester Alexis mehr wie die anderen Mädchen ist. Darum benimmt er sich ihr gegenüber ganz anders als sonst, um sie zu ⏎überzeugen sich weiblicher zu benehmen. Meistens endet es dann damit, dass sie sauer auf ihn wird. |
| strTbl_g.bin | 24 | Tania ist ein Mitglied der Schattenreiter, einer Gruppe, die nach den Geisterschlüsseln sucht.⏎Sie ist außerdem noch eine Amazone.⏎⏎Auch wenn die meisten der Schattenreiter recht bösartig sind, so ist Tania doch eine fröhliche und gerechte Persönlichkeit.⏎Die Suche nach einem potentiellen Ehemann ist ihr wichtiger als die Suche nach den Geisterschlüsseln.⏎⏎Da sie ja eine Amazone ist, passt ihr Deck wirklich gut ihr, denn es besteht aus Amazonen-Karten. Sie spezialisiert auf Power-Duelle mit diesen Karten.⏎⏎Jedermann ist interessiert zu erfahren, was aus dem Mann wird, den sie als ihren Bräutigam bestimmt. | Tania ist ein Mitglied der Schattenreiter, einer Gruppe, die nach den Geisterschlüsseln sucht.⏎Sie ist außerdem noch eine Amazone.⏎⏎Auch wenn die meisten der Schattenreiter recht bösartig sind, so ist Tania doch eine fröhliche und gerechte Persönlichkeit.⏎Die Suche nach einem potentiellen Ehemann ist ihr wichtiger als die Suche nach den Geisterschlüsseln.⏎⏎Da sie ja eine Amazone ist, passt ihr Deck wirklich gut zu ihr, denn es besteht aus Amazonen-Karten. Sie spezialisiert sich auf Power-Duelle mit diesen Karten.⏎⏎Jedermann ist interessiert zu erfahren, was aus dem Mann wird, den sie als ihren Bräutigam bestimmt. |
| strTbl_g.bin | 25 | Don Zaloog ist ein Mitglied der Schattenreiter, einer Gruppe, die nach den Geisterschlüsseln sucht.⏎Er ist außerdem der Anführer einer Diebesbande, die sich die „Dunkler Skorpion-Einbrecher“ nennt.⏎Don Zaloog hat sich verkleidet und in die Duellakademie geschlichen. Man sagt, er sei ein klügerer Krimineller, als es den Anschein hat.⏎⏎Während einem Duell besteht sein Deck größtenteils aus „Dunkler Skorpion-Einbrecher“-Karten. Combos von diesen Karten bringen die Hand des Gegners wirklich in Unordnung. | Don Zaloog ist ein Mitglied der Schattenreiter, einer Gruppe, die nach den Geisterschlüsseln sucht.⏎Er ist außerdem der Anführer einer Diebesbande, die sich die „Dunkler Skorpion-Einbrecher“ nennt.⏎Don Zaloog hat sich verkleidet und in die Duellakademie geschlichen. Man sagt, er sei ein klügerer Krimineller, als es den Anschein hat.⏎⏎Während eines Duells besteht sein Deck größtenteils aus „Dunkler Skorpion-Einbrecher“-Karten. Combos von diesen Karten bringen die Hand des Gegners wirklich in Unordnung. |
| strTbl_g.bin | 28 | Selbsternannter „Schattenduellant“.⏎Während eines Schattenspiels, benutzte dieser herzlose Duellant einen Milleniumsgegenstand um seinen Gegner, der verloren hatte, in den Tod zu schicken.⏎⏎Titan lebt von den Schattenspielen. Er nimmt Aufträge an und bekämpft jeden, ⏎für den er angeheuert wurde.⏎Er verlangt drei Monatsgehälter von seinen Kunden, ohne Ausnahme.⏎Weil er ein Schattenduellant ist, besteht sein Deck hauptsächlich aus Karten des Typs Erz-Unterweltler.⏎⏎Er ist sehr professionell und gibt sich niemals eine Blöße. Nicht einmal für den Bruchteil einer Sekunde.⏎Er ist immer in Alarmbereitschaft, sogar beim Hände schütteln. | Selbsternannter „Schattenduellant“.⏎Während eines Schattenspiels, benutzte dieser herzlose Duellant einen Millenniumsgegenstand um seinen Gegner, der verloren hatte, in den Tod zu schicken.⏎⏎Titan lebt von den Schattenspielen. Er nimmt Aufträge an und bekämpft jeden, ⏎für den er angeheuert wurde.⏎Er verlangt drei Monatsgehälter von seinen Kunden, ohne Ausnahme.⏎Weil er ein Schattenduellant ist, besteht sein Deck hauptsächlich aus Karten des Typs Erz-Unterweltler.⏎⏎Er ist sehr professionell und gibt sich niemals eine Blöße. Nicht einmal für den Bruchteil einer Sekunde.⏎Er ist immer in Alarmbereitschaft, sogar beim Hände schütteln. |
| strTbl_g.bin | 29 | Amnael ist die wahre Form von Professor Lyman Banner.⏎Er betrieb alchemistische Forschungen in der Hoffnung Unsterblichkeit zu erreichen.⏎Vielleicht ergaben seine Forschungen, dass dies Geheimnis bei den Heiligen Bestien liegt und plant deswegen ihre Wiederbelebung.⏎⏎Er benutzt ein Alchemiedeck und einen unkonventionellen Duellstil, indem er oft Karten aus dem Spiel entfernt. | Amnael ist die wahre Form von Professor Lyman Banner.⏎Er betrieb alchemistische Forschungen in der Hoffnung Unsterblichkeit zu erreichen.⏎Vielleicht ergaben seine Forschungen, dass dieses Geheimnis bei den Heiligen Bestien liegt und plant deswegen ihre Wiederbelebung.⏎⏎Er benutzt ein Alchemiedeck und einen unkonventionellen Duellstil, indem er oft Karten aus dem Spiel entfernt. |
| strTbl_g.bin | 30 | Kagemaru ist der Vorsitzende der Duellakademie.⏎⏎Er hat die Akademie gegründet um talentierte Duellanten an einem Ort zu sammeln, mit dem Endziel ihre Stärke zum Wiederbeleben der Karten der Heiligen Bestien zu benutzen. Diese Karten sind vor langer Zeit versiegelt worden.⏎Durch die Wiederbelebung der Heiligen Bestien würde eine große Menge Energie freigesetzt, die er benutzen möchte um die ewige Jugend zu erreichen. | Kagemaru ist der Vorsitzende der Duellakademie.⏎⏎Er hat die Akademie gegründet, um talentierte Duellanten an einem Ort zu sammeln, mit dem Endziel ihre Stärke zum Wiederbeleben der Karten der Heiligen Bestien zu benutzen. Diese Karten sind vor langer Zeit versiegelt worden.⏎Durch die Wiederbelebung der Heiligen Bestien würde eine große Menge Energie freigesetzt, die er benutzen möchte, um die ewige Jugend zu erreichen. |
| strTbl_g.bin | 31 | Ein ehemaliger Student von Obelisk-Blue. ⏎Er war exzellent in seinen Studien, aber er hatte ein schwache Ziehtechnik.⏎Diese Schwäche zwang ihn ein zurückgezogenes Leben in den Bergen zu führen.⏎Dort durchlief er ein hartes Trainingsprogramm um seine Ziehtechnik zu perfektionieren.⏎⏎Sein Ziehen hat sich nach dem Training zwar ziemlich verbessert, aber weil er sich auf diesen einen Aspekt konzentriert hat, sind sein anderen Fähigkeiten schwächer geworden. | Ein ehemaliger Student von Obelisk Blau. ⏎Er war exzellent in seinen Studien, aber er hatte eine schwache Ziehtechnik.⏎Diese Schwäche zwang ihn ein zurückgezogenes Leben in den Bergen zu führen.⏎Dort durchlief er ein hartes Trainingsprogramm, um seine Ziehtechnik zu perfektionieren.⏎⏎Sein Ziehen hat sich nach dem Training zwar ziemlich verbessert, aber weil er sich auf diesen einen Aspekt konzentriert hat, sind seine anderen Fähigkeiten schwächer geworden. |
| strTbl_g.bin | 33 | Jasmine ist Fangirl A, ein Fan und Anhänger von Alexis.⏎Sie ist die erste Adresse für Informationen über die Akademie (hauptsächlich Gerüchte) und sie hält Alexis auf dem Laufenden was auf dem Campus gerade abläuft. Aber Alexis scheint nicht besonders an diesen „Informationen“ interessiert zu sein.⏎⏎Jasmin benutzt ein Harpyien-Deck, vielleicht weil sie starke Frauen bewundert. | Jasmine ist Fangirl A, ein Fan und Anhänger von Alexis.⏎Sie ist die erste Adresse für Informationen über die Akademie (hauptsächlich Gerüchte) und sie hält Alexis auf dem Laufenden was auf dem Campus gerade abläuft. Aber Alexis scheint nicht besonders an diesen „Informationen“ interessiert zu sein.⏎⏎Jasmine benutzt ein Harpyien-Deck, vielleicht weil sie starke Frauen bewundert. |
| strTbl_g.bin | 34 | Mindy ist Fangirl B, ein Fan und Anhänger von Alexis.⏎Sie ist sehr damenhaft in ihrer Ausdrucksweise, aber die Dinge, die sie zu sagen hat, sind sehr oft ganz schön boshaft.⏎Sie hat ein klares Interesse daran Jungen zu bewerten und führt sogar ein Buch mit den „Jungenbewertungen“.⏎⏎Mindy benutzt ein Deck voller hübscher Männer, es wird das „Pretty Boy“-Deck genannt. ⏎Sie hat es geschafft nach Obelisk-Blue zu kommen und hat dabei ein Deck benutzt, das zu sehr nach einem Fangirl aussieht. Deshalb glauben die Leute, dass sie als Duellantin recht begabt sein muss. | Mindy ist Fangirl B, ein Fan und Anhänger von Alexis.⏎Sie ist sehr damenhaft in ihrer Ausdrucksweise, aber die Dinge, die sie zu sagen hat, sind sehr oft ganz schön boshaft.⏎Sie hat ein klares Interesse daran Jungen zu bewerten und führt sogar ein Buch mit den „Jungenbewertungen“.⏎⏎Mindy benutzt ein Deck voller hübscher Männer, es wird das „Pretty Boy“-Deck genannt. ⏎Sie hat es geschafft nach Obelisk Blau zu kommen und hat dabei ein Deck benutzt, das zu sehr nach einem Fangirl aussieht. Deshalb glauben die Leute, dass sie als Duellantin recht begabt sein muss. |
| strTbl_g.bin | 35 | Wheeler ist ein experimenteller Schimpanse.⏎Er wurde in der Forschungseinrichtung auf der Insel der Akademie aufgezogen.⏎Er kann zwar kein Golf spielen, aber er ist ein recht passabler Duellant.⏎Außer Affenlaute kann Wheeler sogar richtige Worte sprechen. Aber die Worte kommen nicht aus seinem eigenen Mund, eine Maschine ermöglicht ihm das Sprechen.⏎⏎Er hat eine menge Karten zum Thema Affen in seinem Deck. | Wheeler ist ein experimenteller Schimpanse.⏎Er wurde in der Forschungseinrichtung auf der Insel der Akademie aufgezogen.⏎Er kann zwar kein Golf spielen, aber er ist ein recht passabler Duellant.⏎Außer Affenlaute kann Wheeler sogar richtige Worte sprechen. Aber die Worte kommen nicht aus seinem eigenen Mund, eine Maschine ermöglicht ihm das Sprechen.⏎⏎Er hat eine Menge Karten zum Thema Affen in seinem Deck. |
| strTbl_g.bin | 36 | Ein Junge, der bei Slifer-Red eingeschrieben ist.⏎Er hat einen zierlichen Körperbau, schon fast wie bei einem Mädchen.⏎⏎Er spricht so wie jeder andere Junge auch sprechen würde, aber manchmal ist sein Verhalten doch dem eines Mädchens sehr ähnlich.⏎⏎Und obwohl er ein Junge ist, ist er nie mit den anderen Jungen zusammen im Umkleideraum und duscht immer alleine, genauso wie es ein Mädchen machen würde.⏎⏎Wenn ich es nicht besser wüsste, würde ich sagen, dass dieser Junge eigentlich ein Mädchen ist. | Ein Junge, der bei Slifer Rot eingeschrieben ist.⏎Er hat einen zierlichen Körperbau, schon fast wie bei einem Mädchen.⏎⏎Er spricht so wie jeder andere Junge auch sprechen würde, aber manchmal ist sein Verhalten doch dem eines Mädchens sehr ähnlich.⏎⏎Und obwohl er ein Junge ist, ist er nie mit den anderen Jungen zusammen im Umkleideraum und duscht immer alleine, genauso wie es ein Mädchen machen würde.⏎⏎Wenn ich es nicht besser wüsste, würde ich sagen, dass dieser Junge eigentlich ein Mädchen ist. |
| strTbl_g.bin | 37 | Ein Mädchen, das hinter Zane her ist.⏎Sie hat den Aufnahmetest der Akademie nur deshalb gemacht, damit sie sich an der Akademie einschreiben kann und so Zane jeden Tag sehen kann.⏎Ihre Persönlichkeit lässt sich am besten mit dem Wort „Besessen“ beschreiben. Sie ist definitiv ein eifersüchtiges Mädchen. Sogar so eifersüchtig, dass sie die Kontrolle verliert und alle um sie herum in Verwirrung stürtzt.⏎⏎Ihr Deck spiegelt die Gefühle eines verliebten jungen Mädchens wieder. Sie hofft ihre Gefühle, ihrem Auserwählten, eines Tages durch ein Duell mitteilen zu können.　Ihre Hauptkarte ist „Verliebte Jungfer“. Eigentlich ist es ein Monster, das seine Gegner gefangen nimmt.⏎⏎Und da sie erst in der 5. Klasse ist, kann sie gar nicht auf eine Oberschulen Duellakademie gehen. | Ein Mädchen, das hinter Zane her ist.⏎Sie hat den Aufnahmetest der Akademie nur deshalb gemacht, damit sie sich an der Akademie einschreiben kann und so Zane jeden Tag sehen kann.⏎Ihre Persönlichkeit lässt sich am besten mit dem Wort „Besessen“ beschreiben. Sie ist definitiv ein eifersüchtiges Mädchen. Sogar so eifersüchtig, dass sie die Kontrolle verliert und alle um sie herum in Verwirrung stürzt.⏎⏎Ihr Deck spiegelt die Gefühle eines verliebten jungen Mädchens wieder. Sie hofft ihre Gefühle, ihrem Auserwählten, eines Tages durch ein Duell mitteilen zu können.　Ihre Hauptkarte ist „Verliebte Jungfer“. Eigentlich ist es ein Monster, das seine Gegner gefangen nimmt.⏎⏎Und da sie erst in der 5. Klasse ist, kann sie gar nicht auf eine Duellakademie der Oberstufe gehen. |
| strTbl_g.bin | 38 | Ein Duellant, der gegen Yugi Muto, den legendären Duellkönig, gespielt hat.⏎Er hat ein chinesisches Schriftzeichen auf der Stirn, das „Labyrinth“ bedeutet.⏎⏎Er und sein jüngerer Bruder Dox bilden zusammen ein sehr starkes Tag-Team.⏎Seine Fähigkeiten als individueller Duellant sind unbekannt.⏎⏎Seine Haupttaktik besteht darin, dass er seinen Gegnern einen einen harten Brocken zu verdauen gibt. Die Beschwörung des so genannten „Torwächter“. | Ein Duellant, der gegen Yugi Muto, den legendären Duellkönig, gespielt hat.⏎Er hat ein chinesisches Schriftzeichen auf der Stirn, das „Labyrinth“ bedeutet.⏎⏎Er und sein jüngerer Bruder Dox bilden zusammen ein sehr starkes Tag-Team.⏎Seine Fähigkeiten als individueller Duellant sind unbekannt.⏎⏎Seine Haupttaktik besteht darin, dass er seinen Gegnern einen harten Brocken zu verdauen gibt. Die Beschwörung des so genannten „Torwächter“. |
| strTbl_g.bin | 40 | Ein Kartengeist.⏎Sie ist fröhlich, voller Energie und liebt es Spaß zu haben.⏎Wann immer etwas Lustiges an der Duellakademie vorgeht, versucht sie daran beteiligt zu sein.⏎⏎Sie ist eine sehr talentierte Duellantin und könnte sich auch gegen ein Mädchen aus dem Haus Obelisk-Blue behaupten.⏎Der Geist selber, ist in ihrem Deck enthalten. | Ein Kartengeist.⏎Sie ist fröhlich, voller Energie und liebt es Spaß zu haben.⏎Wann immer etwas Lustiges an der Duellakademie vorgeht, versucht sie daran beteiligt zu sein.⏎⏎Sie ist eine sehr talentierte Duellantin und könnte sich auch gegen ein Mädchen aus dem Haus Obelisk Blau behaupten.⏎Der Geist selbst ist in ihrem Deck enthalten. |
| strTbl_g.bin | 41 | Eine Karte, die augenblicklich versucht wieder eine reale Person zu werden, aber er braucht dafür ein Menschenopfer.⏎⏎Niemand weiß was er plant, für den Fall, das er wiedergeboren wird.⏎⏎Er benutzt sich selber als seine Hauptkarte, eine Karte mit dem Effekt, das die Aktivierung von Fallenkarten negiert werden kann. Er hat diese besondere Spezialeffekt-Kraft vielleicht auch als Geist. | Ein Kartengeist, der im Moment versucht, wieder eine reale Person zu werden, aber er braucht dafür ein Menschenopfer.⏎⏎Niemand weiß was er plant, für den Fall, dass er wiedergeboren wird.⏎⏎Er benutzt sich selber als seine Hauptkarte, eine Karte mit dem Effekt, dass die Aktivierung von Fallenkarten negiert werden kann. Er hat diese besondere Spezialeffekt-Kraft vielleicht auch als Geist. |
| strTbl_g.bin | 43 | Eine Mitarbeiterin der Schule, die im Kartengeschäft der Akademie arbeitet. ⏎Sie hat eine sanfte Persönlichkeit, aber wenn die Studenten sie Siezen, dann starrt sie die Kinder wütend an, weil sie sich dann alt fühlt.⏎⏎Es scheint sie hat seit neustem Interesse an Duellen gefunden. | Eine Mitarbeiterin der Schule, die im Kartengeschäft der Akademie arbeitet. ⏎Sie hat eine sanfte Persönlichkeit, aber wenn die Studenten sie siezen, dann starrt sie die Kinder wütend an, weil sie sich dann alt fühlt.⏎⏎Es scheint, dass sie seit Kurzem Interesse an Duellen gefunden hat. |
| strTbl_g.bin | 44 | Eine Mitarbeiterin der Schule, die im Kartengeschäft der Akademie arbeitet. ⏎Sie ist außerdem das selbsternannte Maskottchen der Akademie. Man kann sie oft bei verschiedenen Anlässen ein Kostüm tragen sehen.⏎⏎Es scheint sie hat seit neustem Interesse an Duellen gefunden. | Eine Mitarbeiterin der Schule, die im Kartengeschäft der Akademie arbeitet. ⏎Sie ist außerdem das selbsternannte Maskottchen der Akademie. Man kann sie oft bei verschiedenen Anlässen ein Kostüm tragen sehen.⏎⏎Es scheint, dass sie seit Kurzem Interesse an Duellen gefunden hat. |
| strTbl_g.bin | 45 | Er ist der älteste Sohn der Princeton Gruppe. Einem riesigen familieneigenen Unternehmen. Ere ist außerdem noch eine Politiker.⏎Die Princeton Gruppe plant die Vorherrschaft in drei Einflussbereichen, der Politik, den Finanzen und dem Duellieren.⏎In seiner Verantwortung liegt der politische Bereich.⏎⏎Er glaubt nicht, dass sein Bruder Chazz das nötige Zeug dazu hat, um die Verantwortung im Bereich Duellieren zu übernehmen. Aus diesem Grund versucht er die Duellakademie selber zu übernehmen, in der Hoffnung, den Ruf der Princeton Gruppe in diesem Bereich zu verbessern.⏎⏎Er benutzt ein hochwertiges Deck. Auch hat er große Summen investiert, um an viele seltene Karten zu kommen. | Er ist der älteste Sohn der Princeton Gruppe. Einem riesigen familieneigenen Unternehmen. Er ist außerdem noch Politiker.⏎Die Princeton Gruppe plant die Vorherrschaft in drei Einflussbereichen, der Politik, den Finanzen und dem Duellieren.⏎In seiner Verantwortung liegt der politische Bereich.⏎⏎Er glaubt nicht, dass sein Bruder Chazz das nötige Zeug dazu hat, um die Verantwortung im Bereich Duellieren zu übernehmen. Aus diesem Grund versucht er die Duellakademie selber zu übernehmen, in der Hoffnung, den Ruf der Princeton Gruppe in diesem Bereich zu verbessern.⏎⏎Er benutzt ein hochwertiges Deck. Auch hat er große Summen investiert, um an viele seltene Karten zu kommen. |
| strTbl_g.bin | 48 | Fonda ist die Vorsteherin des weiblichen Teils des Hauses Obelisk-Blue.⏎Sie ist außerdem noch die Turnlehrerin und Schulschwester an der Duellakademie.⏎Viele männliche Schüler täuschen Verletzungen vor nur um sie einmal zu treffen.⏎⏎Fonda ist eine recht gute Duellantin und genießt manchmal in ihrer Freizeit ein kleines Duell.⏎Sie liebt alles was niedlich ist und das zeigt sich auch in ihrem Deck, das voller niedlicher Karten ist. | Fonda ist die Vorsteherin des weiblichen Teils des Hauses Obelisk Blau.⏎Sie ist außerdem noch die Turnlehrerin und Schulschwester an der Duellakademie.⏎Viele männliche Schüler täuschen Verletzungen vor nur, um sie einmal zu treffen.⏎⏎Fonda ist eine recht gute Duellantin und genießt manchmal in ihrer Freizeit ein kleines Duell.⏎Sie liebt alles was niedlich ist und das zeigt sich auch in ihrem Deck, das voller niedlicher Karten ist. |
| strTbl_g.bin | 49 | Ein wandernder Spieler.⏎Er muss auf gutem Fuß mit der Göttin Fortuna stehen, denn er hat noch nie verloren.⏎Zumindest wird das behauptet, aber in Wirklichkeit behauptet er, er hätte bis jetzt nicht verloren, weil er weiterspielt bis er gewinnt.⏎Nachdem er Gerüchte über die Schattenreiter gehört hat, kam er an die Duellakademie in der Hoffnung trainieren zu können und dann gegen sie zu kämpfen.⏎Er hat auch eine einzigartige Beziehung zu Alexis, vielleicht ein Fingerzeig des Schicksals...⏎⏎Er benutzt ein Spieler-Deck, voller glücksorientierter Karten.⏎Er behauptet es gibt nichts schöneres als alles auf die richtige Zahl bei einem Spiel mit Würfeln oder Münzen zu setzen.⏎⏎Seine wirklicher Name ist Pierre, aber er wird wütend wenn ihn jemand so nennt. | Ein wandernder Spieler.⏎Er muss auf gutem Fuß mit der Göttin Fortuna stehen, denn er hat noch nie verloren.⏎Zumindest wird das behauptet, aber in Wirklichkeit behauptet er, er hätte bis jetzt nicht verloren, weil er weiterspielt bis er gewinnt.⏎Nachdem er Gerüchte über die Schattenreiter gehört hat, kam er an die Duellakademie in der Hoffnung trainieren zu können und dann gegen sie zu kämpfen.⏎Er hat auch eine einzigartige Beziehung zu Alexis, vielleicht ein Fingerzeig des Schicksals...⏎⏎Er benutzt ein Spieler-Deck, voller glücksorientierter Karten.⏎Er behauptet es gibt nichts schöneres als alles auf die richtige Zahl bei einem Spiel mit Würfeln oder Münzen zu setzen.⏎⏎Sein wirklicher Name ist Pierre, aber er wird wütend wenn ihn jemand so nennt. |
| strTbl_g.bin | 50 | Eine Grabhüter-Angreiferin, die den Helden mit einem Schattenspiel begrüßt, wenn er durch die Zeit aus einer antiken Ruine teleportiert.⏎⏎Einige Leute haben Zeitsprünge gemacht und sie ist in einen von ihnen verliebt | Eine Grabwächter-Attentäterin, die den Helden mit einem Schattenspiel begrüßt, wenn er durch die Zeit aus einer antiken Ruine teleportiert.⏎⏎Einige Leute haben Zeitsprünge gemacht und sie ist in einen von ihnen verliebt |
| strTbl_g.bin | 52 | Schulleiter Sheppard’s Beschreibung | Schulleiter Sheppards Beschreibung |
| strTbl_g.bin | 65 | Anhaltenden Zauber aktivieren | Permanenten Zauber aktivieren |
| strTbl_g.bin | 69 | Anhaltende Falle aktiveren | Permanente Falle aktivieren |
| strTbl_g.bin | 70 | Konter-Falle aktivieren | Konterfalle aktivieren |
| strTbl_g.bin | 5 | New High Score Bonus | Neuer Highscore-Bonus |
| strTbl_g.bin | 6 | New Challenge Bonus | Neuer Challenge-Bonus |

(... altre 541 righe nel CSV)

## A6. Etichetta [CARTA MAGIA] / [CARTA TRAPPOLA] della carta grande nel duello

In tutti i `duel/basic_<regione><lingua>.ehp` l'etichetta era in inglese (hash `c2268340`): `apply_to_iso.py` la sostituisce con `card_spell_trap.gim` di `field/always_<lingua>_<lingua>.ehp` (hash `9622cd75`).

| archivio | membro | hash originale | hash nuovo |
|---|---|---|---|
| /PSP_GAME/USRDIR/duel/basic_bg.ehp | card_spell_trap.gim | c2268340 | be08846c |
| /PSP_GAME/USRDIR/duel/basic_fg.ehp | card_spell_trap.gim | c2268340 | be08846c |
| /PSP_GAME/USRDIR/duel/basic_gg.ehp | card_spell_trap.gim | c2268340 | be08846c |
| /PSP_GAME/USRDIR/duel/basic_ig.ehp | card_spell_trap.gim | c2268340 | be08846c |
| /PSP_GAME/USRDIR/duel/basic_sg.ehp | card_spell_trap.gim | c2268340 | be08846c |
| /PSP_GAME/USRDIR/duel/basic_ug.ehp | card_spell_trap.gim | c2268340 | be08846c |

## A7. File della ISO toccati e dettagli tecnici

179 archivi `.ehp` risultano diversi dall'originale (tutte le lingue insieme, perche' la ISO e' unica; elenco in `docs/changes_de/touched_files.csv`). Gli altri file (video, audio, eseguibile `EBOOT.BIN`, `PARAM.SFO`) sono identici. Differenze tecniche non testuali: `*-ptrs.txt` (offset assoluti dei membri, ricalcolati quando una tabella cambia lunghezza), nuova posizione degli archivi in fondo alla ISO.

## A8. Cosa NON si puo' cambiare (limiti del gioco)

- Il **nome del parlante** nella casella del dialogo (es. "Preside Sheppard"/"Cancelliere" in italiano, "Doyen Sheppard" in francese, "Rector Sheppard" in spagnolo) sta nell'EBOOT cifrato: non modificabile.
- Testi disegnati dal gioco con il suo font (dialoghi, nomi, descrizioni nel deck, menu a tendina, tastiera di sistema, schermata di scelta lingua) non sono sostituibili dal texture pack: si cambiano solo nella ISO.
- Le 438 texture di mappa/sfondi non sono sostituite (il gioco ne cambia la palette): limite del pack di MikeyMK, non del nostro lavoro.

---

# B. TEXTURE PACK

## B1. Provenienza e struttura

Base: **Yu-Gi-Oh! GX Tag Force 1 HD Remastered** di **MikeyMK** (pack USA `ULUS10136`) e carte HD di **chrisfand**, adattati alla ISO europea `ULES00600`. Il progetto non ridistribuisce il pack di terzi (`PERMESSI_AUTORI.md`): il patcher se lo fa dare dall'utente. Il nostro lavoro: (1) rimappare gli **hash** del pack USA su quelli EU (`tools/gen_ini.py`), (2) rifare nella lingua carte e scritte dell'interfaccia, (3) correggere i testi, (4) `upscale_extra` per le texture non coperte.

PPSSPP riconosce una texture dall'**hash dei suoi pixel** (xxhash dei dati, `gim.data_hash`); ogni riga del `textures.ini` e' `0000000000000000<hash8> = percorso/png`. I PNG sono **4x** l'originale e ridisegnano esattamente la stessa area. Texture identiche tra lingue hanno lo stesso hash: la sostituzione vale per tutte (vedi `docs/TEXTURE_INVENTORY.md`).

### Struttura reale (da `docs/changes_de/pack_structure.csv`)
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
| moduli/de | cards/ | 5675 | 1025.0 | frame, large_de, small_de, tiny_de |
| moduli/de | de.ini | 1 | 0.01 |  |
| moduli/de | intro/ | 2 | 0.4 | title_screen |
| moduli/de | ui_de/ | 106 | 8.2 | fogli_icone, fogli_icone.ini, lettere_esito, lettere_esito.ini, menu_liste, menu_liste.ini, schede_deck, schede_deck.ini, schede_ricette, schede_ricette.ini ... |

Ogni lingua tranne l'italiano e' un **modulo** (`PSP/TEXTURES/modules/de`) da comporre sopra il pack di base con `tools/compose_pack.py BASE MODULI CARD_DIR OUT de [--copia]`: copia il base e **solo** le cartelle `cards`, `intro` e `ui_de` del modulo (hard link o copia), poi `module_ini.py` riscrive i `textures.ini`: le righe delle carte localizzate puntano a `cards/small_de`/`large_de` e le righe di `de.ini` **sostituiscono** quelle del base con la stessa chiave (hash).

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

Cartelle della lingua: `frame` (2 file), `large_de` (2833 file), `small_de` (2833 file), `tiny_de` (7 file). Ogni carta ha una **piccola HD** (nome + descrizione + tipo, rigenerata con font liberi OFL: XCharter Bold per nomi/tipo/etichette, Libre Baskerville per gli effetti, Newsreader Italic per i Normali, PT Serif Caption per Magie/Trappole, Charis SIL per i glifi mancanti) e una **grande HD** (solo il nome sulla cornice). In piu': la **tabella degli attributi** con le parole della lingua (`cards/frame/icons_attribute_race_<l>.png`, `attributes.py`), l'**etichetta Magia/Trappola** (`icons_spell_trap_<l>.png`, `label_it.py` / `extract_labels.py` -> `dati/label_eu_<codice>_128x32.png`) e l'**atlante delle miniature** del deck (`tiny_<l>`, `tiny_atlas.py` + `tiny_fragment.py`).

Quando cambia il testo di una carta (sezione A2) vanno rigenerate le sue immagini: **258 carte** nel tedesco. Elenco in `docs/changes_de/card_images.csv`. Comando: `python tools/generate_language.py fr PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` (senza ID rigenera tutte: 2.833 + 2.833, ~930 MB).

Tipografia: spazio non separabile prima di `: ; ! ?` e virgolette « ».

## B3. Interfaccia HD in tedesco (`ui_de`)

**98 texture** (`docs/changes_de/ui_textures.csv`: file, hash PPSSPP, famiglia, script, dimensioni originale/HD, neutra/specifica, origine nella ISO). Per famiglia: fogli_icone 3, lettere_esito 28, menu_liste 6, schede_deck 14, schede_ricette 12, schermata_vs 14, scritte_duello 15, tutorial 6. Di queste 0 sono neutre (stesso hash in tutte le lingue) e 98 specifiche. Ogni famiglia ha uno script in `tools/ui_textures/<famiglia>.py` (lettura `TF1_LANG`): ridisegna le scritte texture per texture partendo dall'originale a bassa risoluzione della ISO e dallo stile del pack inglese; stessa area e stesse posizioni (il gioco ritaglia da rettangoli fissi); un font/peso/linea di base/ombra per scritta; font liberi (`alt_font.py`).

| famiglia | texture | script | archivio ISO sorgente | testi della lingua |
|---|---|---|---|---|
| fogli_icone | 3 | `tools/ui_textures/icon_sheets.py` | deck/all_g.ehp, shop/all_g.ehp, field/always_* |  |
| lettere_esito | 28 | `tools/ui_textures/result_letters.py` | duel/basic_gg.ehp | DU GEWINNST (DUGEWINST, 9 tessere) · DU VERLIERST (DUVERLIST, 9 tessere) · UNENTSCHIEDEN (UNETSCHID, 9 tessere; E e N ripetute) + silhouette di DU GEWINNST |
| menu_liste | 6 | `tools/ui_textures/menu_lists.py` | title_menu/title_menu_g.ehp, duel/result/result_g.ehp, field/always_bri_<cod>.ehp |  |
| schede_deck | 14 | `tools/ui_textures/deck_screens.py` | deck/all_g.ehp, labo/*.ehp, shop/all_g.ehp |  |
| schede_ricette | 12 | `tools/ui_textures/recipe_screens.py` | deck/recipe_view_g.ehp, title_menu/title_menu_g.ehp, database/limitlist.ehp |  |
| schermata_vs | 14 | `tools/ui_textures/vs_screen.py` | duel/start/start_e.ehp (membri _g), start_all.ehp, start_g.ehp |  |
| scritte_duello | 15 | `tools/ui_textures/duel_texts.py` | duel/basic_gg.ehp | Ketten · SPIELZUG (blu/rosso) · NÄCHSTER SPIELER (su 2 texture, il taglio passa dentro la L; i puntini della Ä sono una sprite a parte, ingrandita e centrata sopra la A) · DUELL BEGINNEN · Direkter Angriff! · `card_icon03` e' nella cartella `upscale_extra` (B4) |
| tutorial | 6 | `tools/ui_textures/tutorial.py` | tutorial/tutorial_g.ehp (tuto_duelimg01..06) |  |

Regole di qualita' (valgono per ogni lingua): lettere regolari, mai deformate una per una; stessa area dell'originale; niente sfocature; il testo e' quello dell'originale della lingua (si correggono solo errori evidenti: residui di altre lingue, accenti); pixel art **non** levigata senza conferma; geometrie sempre misurate sull'originale.

### Testi disegnati: originale -> HD
Tabella letta a occhio, texture per texture: `docs/changes_de/texture_texts_de.md`. Differenze rispetto all'originale: `DEMARRER` -> `DÉMARRER`, `SCAMBIA`/`Scambia` -> `ÉCHANGE`/`Échange`, `2è/3è round` -> `2e/3e round`; tutto il resto riscrive le stesse parole.

### Elenco di ogni texture
(tutte le 98 righe, da `ui_textures.csv`)

| file nel pack | hash | famiglia | originale px | HD px | tipo | origine ISO |
|---|---|---|---|---|---|---|
| ui_de/fogli_icone/all_g__icon04.png | ce4fe497 | fogli_icone | 128x128 | 512x512 | SPECIFICA | deck/all_g.ehp:icon04.gim |
| ui_de/fogli_icone/all_g__panel.png | 68141938 | fogli_icone | 256x256 | 1024x1024 | SPECIFICA | shop/all_g.ehp:panel.gim |
| ui_de/fogli_icone/all_g__s_pack.png | 731df6d4 | fogli_icone | 256x256 | 1024x1024 | SPECIFICA | shop/all_g.ehp:s_pack.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100002.png | b15e254f | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_draw100002.gim; duel/basic_fg.ehp:duel_draw100002.gim; duel/basic_gg.ehp:duel_draw100002.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100004.png | 3dcf0348 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_draw100004.gim; duel/basic_fg.ehp:duel_draw100004.gim; duel/basic_gg.ehp:duel_draw100004.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100006.png | 988d2924 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_draw100006.gim; duel/basic_fg.ehp:duel_draw100006.gim; duel/basic_gg.ehp:duel_draw100006.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100008.png | c27723c2 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_draw100008.gim; duel/basic_fg.ehp:duel_draw100008.gim; duel/basic_gg.ehp:duel_draw100008.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100010.png | d40c8877 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_draw100010.gim; duel/basic_fg.ehp:duel_draw100010.gim; duel/basic_gg.ehp:duel_draw100010.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100012.png | f32aec8b | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_draw100012.gim; duel/basic_fg.ehp:duel_draw100012.gim; duel/basic_gg.ehp:duel_draw100012.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100014.png | 7164c557 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_draw100014.gim; duel/basic_fg.ehp:duel_draw100014.gim; duel/basic_gg.ehp:duel_draw100014.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100016.png | bf811ab0 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_draw100016.gim; duel/basic_fg.ehp:duel_draw100016.gim; duel/basic_gg.ehp:duel_draw100016.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100018.png | fd752d95 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_draw100018.gim; duel/basic_fg.ehp:duel_draw100018.gim; duel/basic_gg.ehp:duel_draw100018.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100002.png | 912fcd45 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_lose100002.gim; duel/basic_fg.ehp:duel_lose100002.gim; duel/basic_gg.ehp:duel_lose100002.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100004.png | 20c32463 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_lose100004.gim; duel/basic_fg.ehp:duel_lose100004.gim; duel/basic_gg.ehp:duel_lose100004.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100006.png | 7e4814ae | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_lose100006.gim; duel/basic_fg.ehp:duel_lose100006.gim; duel/basic_gg.ehp:duel_lose100006.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100008.png | e758002f | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_lose100008.gim; duel/basic_fg.ehp:duel_lose100008.gim; duel/basic_gg.ehp:duel_lose100008.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100010.png | fe18c251 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_lose100010.gim; duel/basic_fg.ehp:duel_lose100010.gim; duel/basic_gg.ehp:duel_lose100010.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100012.png | adde0b1d | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_lose100012.gim; duel/basic_fg.ehp:duel_lose100012.gim; duel/basic_gg.ehp:duel_lose100012.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100014.png | a3ed8c27 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_lose100014.gim; duel/basic_fg.ehp:duel_lose100014.gim; duel/basic_gg.ehp:duel_lose100014.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100016.png | 49b0e354 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_lose100016.gim; duel/basic_fg.ehp:duel_lose100016.gim; duel/basic_gg.ehp:duel_lose100016.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100018.png | 1ee989bc | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_lose100018.gim; duel/basic_fg.ehp:duel_lose100018.gim; duel/basic_gg.ehp:duel_lose100018.gim |
| ui_de/lettere_esito/basic_gg__duel_win100002.png | c8ecef23 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_win100002.gim; duel/basic_fg.ehp:duel_win100002.gim; duel/basic_gg.ehp:duel_win100002.gim |
| ui_de/lettere_esito/basic_gg__duel_win100004.png | 6d2aaacc | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_win100004.gim; duel/basic_fg.ehp:duel_win100004.gim; duel/basic_gg.ehp:duel_win100004.gim |
| ui_de/lettere_esito/basic_gg__duel_win100006.png | 51a3b5f3 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_win100006.gim; duel/basic_fg.ehp:duel_win100006.gim; duel/basic_gg.ehp:duel_win100006.gim |
| ui_de/lettere_esito/basic_gg__duel_win100008.png | 3ee7d405 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_win100008.gim; duel/basic_fg.ehp:duel_win100008.gim; duel/basic_gg.ehp:duel_win100008.gim |
| ui_de/lettere_esito/basic_gg__duel_win100010.png | 595a731a | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_win100010.gim; duel/basic_fg.ehp:duel_win100010.gim; duel/basic_gg.ehp:duel_win100010.gim |
| ui_de/lettere_esito/basic_gg__duel_win100012.png | 2ea9ce79 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_win100012.gim; duel/basic_fg.ehp:duel_win100012.gim; duel/basic_gg.ehp:duel_win100012.gim |
| ui_de/lettere_esito/basic_gg__duel_win100014.png | e6b4a13d | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_win100014.gim; duel/basic_fg.ehp:duel_win100014.gim; duel/basic_gg.ehp:duel_win100014.gim |
| ui_de/lettere_esito/basic_gg__duel_win100016.png | 92a3b4b9 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_win100016.gim; duel/basic_fg.ehp:duel_win100016.gim; duel/basic_gg.ehp:duel_win100016.gim |
| ui_de/lettere_esito/basic_gg__duel_win100018.png | 9b93a537 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:duel_win100018.gim; duel/basic_fg.ehp:duel_win100018.gim; duel/basic_gg.ehp:duel_win100018.gim |
| ui_de/lettere_esito/basic_gg__duel_win100020.png | b5401172 | lettere_esito | 64x32 | 256x128 | SPECIFICA | duel/basic_bg.ehp:duel_win100020.gim; duel/basic_fg.ehp:duel_win100020.gim; duel/basic_gg.ehp:duel_win100020.gim |
| ui_de/menu_liste/always_bri_ger__story_sys02.png | bcd751d8 | menu_liste | 256x128 | 1024x512 | SPECIFICA | field/always_bri_ger.ehp:story_sys02.gim; field/always_fra_ger.ehp:story_sys02.gim; field/always_ger_ger.ehp:story_sys02.gim |
| ui_de/menu_liste/result_g__menu01.png | 43526e37 | menu_liste | 256x64 | 1024x256 | SPECIFICA | duel/result/result_g.ehp:menu01.gim |
| ui_de/menu_liste/result_g__menu02.png | 9a4a8236 | menu_liste | 256x128 | 1024x512 | SPECIFICA | duel/result/result_g.ehp:menu02.gim |
| ui_de/menu_liste/title_menu_g__m_menu_title01.png | 90284e3a | menu_liste | 256x128 | 1024x512 | SPECIFICA | title_menu/title_menu_g.ehp:m_menu_title01.gim |
| ui_de/menu_liste/title_menu_g__press_start0003.png | 57081762 | menu_liste | 256x16 | 1024x64 | SPECIFICA | title_menu/title_menu_g.ehp:press_start0003.gim |
| ui_de/menu_liste/title_menu_g__trnsmt02.png | 800ca6a3 | menu_liste | 256x256 | 1024x1024 | SPECIFICA | title_menu/title_menu_g.ehp:trnsmt02.gim |
| ui_de/schede_deck/all_g__d_window00008.png | 410ef331 | schede_deck | 128x32 | 512x128 | SPECIFICA | deck/all_g.ehp:d_window00008.gim |
| ui_de/schede_deck/all_g__d_window00016.png | 34a9652d | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_e.ehp:d_window00016.gim; deck/all_f.ehp:d_window00016.gim; deck/all_g.ehp:d_window00016.gim |
| ui_de/schede_deck/all_g__d_window00033.png | 328738aa | schede_deck | 256x32 | 1024x128 | SPECIFICA | deck/all_g.ehp:d_window00033.gim |
| ui_de/schede_deck/all_g__d_window00051.png | 78e0995c | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_g.ehp:d_window00051.gim |
| ui_de/schede_deck/all_g__d_window00062.png | 0b841a08 | schede_deck | 128x32 | 512x128 | SPECIFICA | deck/all_g.ehp:d_window00062.gim; labo/conv_machine.ehp:window_g0016.gim; title_menu/title_menu_g.ehp:t_window0015.gim |
| ui_de/schede_deck/all_g__d_window00101.png | dac6a171 | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_g.ehp:d_window00101.gim; labo/rental.ehp:window_g0008.gim |
| ui_de/schede_deck/all_g__tab_title.png | c51223fd | schede_deck | 256x32 | 1024x128 | SPECIFICA | shop/all_g.ehp:tab_title.gim |
| ui_de/schede_deck/conv_machine__window_g0009.png | 467c47c3 | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/conv_machine.ehp:window_g0009.gim; labo/conv_machine.ehp:window_g0026.gim |
| ui_de/schede_deck/conv_machine__window_g0016.png | 0b841a08 | schede_deck | 128x32 | 512x128 | SPECIFICA | deck/all_g.ehp:d_window00062.gim; labo/conv_machine.ehp:window_g0016.gim; title_menu/title_menu_g.ehp:t_window0015.gim |
| ui_de/schede_deck/conv_machine__window_g0026.png | 467c47c3 | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/conv_machine.ehp:window_g0009.gim; labo/conv_machine.ehp:window_g0026.gim |
| ui_de/schede_deck/password__key_g0027.png | f2102f5c | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/password.ehp:key_g0027.gim |
| ui_de/schede_deck/rental__window_g0008.png | dac6a171 | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_g.ehp:d_window00101.gim; labo/rental.ehp:window_g0008.gim |
| ui_de/schede_deck/rental__window_g0015.png | 55e5724d | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/rental.ehp:window_g0015.gim |
| ui_de/schede_deck/rental__window_g0026.png | 47f0c275 | schede_deck | 64x32 | 256x128 | SPECIFICA | labo/rental.ehp:window_g0026.gim |
| ui_de/schede_ricette/limitlist__window_g0002.png | 3bda99aa | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_g0002.gim |
| ui_de/schede_ricette/limitlist__window_g0004.png | a6a65331 | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_g0004.gim |
| ui_de/schede_ricette/limitlist__window_g0012.png | c03e3475 | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_g0012.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010004.png | 97f5751a | schede_ricette | 256x64 | 1024x256 | SPECIFICA | deck/recipe_view_g.ehp:recipe010004.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010008.png | 1e332ce0 | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_g.ehp:recipe010008.gim; title_menu/title_menu_g.ehp:recipe_sel00002.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010015.png | 31608bc8 | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_g.ehp:recipe010015.gim; title_menu/title_menu_g.ehp:recipe_sel00009.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010027.png | 84c2dc4b | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_g.ehp:recipe010027.gim; title_menu/title_menu_g.ehp:recipe_sel00020.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010029.png | 2aec2bee | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_g.ehp:recipe010029.gim; title_menu/title_menu_g.ehp:recipe_sel00022.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010031.png | 3582dfbc | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_g.ehp:recipe010031.gim; title_menu/title_menu_g.ehp:recipe_sel00024.gim |
| ui_de/schede_ricette/title_menu_g__recipe_sel00033.png | f000f198 | schede_ricette | 128x32 | 512x128 | SPECIFICA | title_menu/title_menu_g.ehp:recipe_sel00033.gim |
| ui_de/schede_ricette/title_menu_g__t_window0008.png | 8f980210 | schede_ricette | 64x32 | 256x128 | SPECIFICA | title_menu/title_menu_g.ehp:t_window0008.gim |
| ui_de/schede_ricette/title_menu_g__t_window0026.png | 8fee65d6 | schede_ricette | 64x32 | 256x128 | SPECIFICA | title_menu/title_menu_g.ehp:t_window0026.gim |
| ui_de/schermata_vs/start_all__jyanken20_g0005.png | 2469fc30 | schermata_vs | 256x32 | 1024x128 | SPECIFICA | duel/start/start_all.ehp:jyanken20_g0005.gim; duel/start/start_e.ehp:jyanken20_g0005.gim; duel/start/start_f.ehp:jyanken20_g0005.gim |
| ui_de/schermata_vs/start_all__jyanken20_g0007.png | 8729983a | schermata_vs | 256x32 | 1024x128 | SPECIFICA | duel/start/start_all.ehp:jyanken20_g0007.gim; duel/start/start_e.ehp:jyanken20_g0007.gim; duel/start/start_f.ehp:jyanken20_g0007.gim |
| ui_de/schermata_vs/start_all__vs_much1_g0001.png | 647ec094 | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much1_g0001.gim; duel/start/start_e.ehp:vs_much1_g0001.gim; duel/start/start_f.ehp:vs_much1_g0001.gim |
| ui_de/schermata_vs/start_all__vs_much2_g0001.png | d6e3420a | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much2_g0001.gim; duel/start/start_e.ehp:vs_much2_g0001.gim; duel/start/start_f.ehp:vs_much2_g0001.gim |
| ui_de/schermata_vs/start_all__vs_much3_g0001.png | 0bf3bc02 | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much3_g0001.gim; duel/start/start_e.ehp:vs_much3_g0001.gim; duel/start/start_f.ehp:vs_much3_g0001.gim |
| ui_de/schermata_vs/start_e__d_menu01_g.png | 23d1ae0c | schermata_vs | 256x256 | 1024x1024 | SPECIFICA | duel/start/start_e.ehp:d_menu01_g.gim; duel/start/start_f.ehp:d_menu01_g.gim; duel/start/start_g.ehp:d_menu01_g.gim |
| ui_de/schermata_vs/start_e__vs_bg01_1_g0005.png | 9b2a5a3b | schermata_vs | 256x32 | 1024x128 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_g0005.gim; duel/start/start_f.ehp:vs_bg01_1_g0005.gim; duel/start/start_g.ehp:vs_bg01_1_g0005.gim |
| ui_de/schermata_vs/start_e__vs_bg01_1_g0007.png | cc2fd1b7 | schermata_vs | 256x64 | 1024x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_g0007.gim; duel/start/start_f.ehp:vs_bg01_1_g0007.gim; duel/start/start_g.ehp:vs_bg01_1_g0007.gim |
| ui_de/schermata_vs/start_e__vs_bg01_1_g0008.png | e3f4a299 | schermata_vs | 256x64 | 1024x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_g0008.gim; duel/start/start_f.ehp:vs_bg01_1_g0008.gim; duel/start/start_g.ehp:vs_bg01_1_g0008.gim |
| ui_de/schermata_vs/start_e__vs_bg01_1_g0012.png | d94ea205 | schermata_vs | 128x32 | 512x128 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_g0012.gim; duel/start/start_f.ehp:vs_bg01_1_g0012.gim; duel/start/start_g.ehp:vs_bg01_1_g0012.gim |
| ui_de/schermata_vs/start_e__vs_bg01_1_g0014.png | 6b884f0c | schermata_vs | 128x64 | 512x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_g0014.gim; duel/start/start_f.ehp:vs_bg01_1_g0014.gim; duel/start/start_g.ehp:vs_bg01_1_g0014.gim |
| ui_de/schermata_vs/start_e__vs_bg01_2_g0001.png | 1dd44271 | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_2_g0001.gim; duel/start/start_f.ehp:vs_bg01_2_g0001.gim; duel/start/start_g.ehp:vs_bg01_2_g0001.gim |
| ui_de/schermata_vs/start_e__vs_bg01_2_g0004.png | 38434306 | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_2_g0004.gim; duel/start/start_f.ehp:vs_bg01_2_g0004.gim; duel/start/start_g.ehp:vs_bg01_2_g0004.gim |
| ui_de/schermata_vs/start_g__jnk_card01.png | cc4d76f2 | schermata_vs | 512x256 | 2048x1024 | SPECIFICA | duel/start/start_g.ehp:jnk_card01.gim |
| ui_de/scritte_duello/basic_gg__chain010003.png | d08b0e76 | scritte_duello | 64x32 | 256x128 | SPECIFICA | duel/basic_bg.ehp:chain010003.gim; duel/basic_fg.ehp:chain010003.gim; duel/basic_gg.ehp:chain010003.gim |
| ui_de/scritte_duello/basic_gg__chain010005.png | 63fc2f5c | scritte_duello | 128x32 | 512x128 | SPECIFICA | duel/basic_bg.ehp:chain010005.gim; duel/basic_fg.ehp:chain010005.gim; duel/basic_gg.ehp:chain010005.gim |
| ui_de/scritte_duello/basic_gg__dilect_atk00001.png | 207c290e | scritte_duello | 256x32 | 1024x128 | SPECIFICA | duel/basic_bg.ehp:dilect_atk00001.gim; duel/basic_fg.ehp:dilect_atk00001.gim; duel/basic_gg.ehp:dilect_atk00001.gim |
| ui_de/scritte_duello/basic_gg__dilect_atk00003.png | fd670497 | scritte_duello | 128x32 | 512x128 | SPECIFICA | duel/basic_bg.ehp:dilect_atk00003.gim; duel/basic_fg.ehp:dilect_atk00003.gim; duel/basic_gg.ehp:dilect_atk00003.gim |
| ui_de/scritte_duello/basic_gg__next_player0001.png | 5212b3a9 | scritte_duello | 64x16 | 256x64 | SPECIFICA | duel/basic_bg.ehp:next_player0001.gim; duel/basic_fg.ehp:next_player0001.gim; duel/basic_gg.ehp:next_player0001.gim |
| ui_de/scritte_duello/basic_gg__next_player0002.png | 22c1e7af | scritte_duello | 64x32 | 256x128 | SPECIFICA | duel/basic_bg.ehp:next_player0002.gim; duel/basic_fg.ehp:next_player0002.gim; duel/basic_gg.ehp:next_player0002.gim |
| ui_de/scritte_duello/basic_gg__next_player0003.png | a3399289 | scritte_duello | 256x32 | 1024x128 | SPECIFICA | duel/basic_bg.ehp:next_player0003.gim; duel/basic_fg.ehp:next_player0003.gim; duel/basic_gg.ehp:next_player0003.gim |
| ui_de/scritte_duello/basic_gg__next_player0005.png | 042946dc | scritte_duello | 64x16 | 256x64 | SPECIFICA | duel/basic_bg.ehp:next_player0005.gim; duel/basic_fg.ehp:next_player0005.gim; duel/basic_gg.ehp:next_player0005.gim |
| ui_de/scritte_duello/basic_gg__next_player0006.png | f0dfc85e | scritte_duello | 64x32 | 256x128 | SPECIFICA | duel/basic_bg.ehp:next_player0006.gim; duel/basic_fg.ehp:next_player0006.gim; duel/basic_gg.ehp:next_player0006.gim |
| ui_de/scritte_duello/basic_gg__next_player0007.png | c30370b4 | scritte_duello | 256x32 | 1024x128 | SPECIFICA | duel/basic_bg.ehp:next_player0007.gim; duel/basic_fg.ehp:next_player0007.gim; duel/basic_gg.ehp:next_player0007.gim |
| ui_de/scritte_duello/basic_gg__score-top100011.png | 20d674aa | scritte_duello | 32x32 | 128x128 | SPECIFICA | duel/basic_bg.ehp:score-top100011.gim; duel/basic_fg.ehp:score-top100011.gim; duel/basic_gg.ehp:score-top100011.gim |
| ui_de/scritte_duello/basic_gg__score-top100013.png | aab8884f | scritte_duello | 32x32 | 128x128 | SPECIFICA | duel/basic_bg.ehp:score-top100013.gim; duel/basic_fg.ehp:score-top100013.gim; duel/basic_gg.ehp:score-top100013.gim |
| ui_de/scritte_duello/basic_gg__start_duel10001.png | 13405678 | scritte_duello | 64x64 | 256x256 | SPECIFICA | duel/basic_bg.ehp:start_duel10001.gim; duel/basic_fg.ehp:start_duel10001.gim; duel/basic_gg.ehp:start_duel10001.gim |
| ui_de/scritte_duello/basic_gg__start_duel10002.png | 9bf6803a | scritte_duello | 256x64 | 1024x256 | SPECIFICA | duel/basic_bg.ehp:start_duel10002.gim; duel/basic_fg.ehp:start_duel10002.gim; duel/basic_gg.ehp:start_duel10002.gim |
| ui_de/scritte_duello/basic_gg__start_duel10005.png | ef0dcee9 | scritte_duello | 128x32 | 512x128 | SPECIFICA | duel/basic_bf.ehp:start_duel10005.gim; duel/basic_bg.ehp:start_duel10005.gim; duel/basic_ff.ehp:start_duel10005.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg01.png | 5642fab0 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_g.ehp:tuto_duelimg01.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg02.png | de3b0f96 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_g.ehp:tuto_duelimg02.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg03.png | 78b9eca8 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_g.ehp:tuto_duelimg03.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg04.png | 4119cb51 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_g.ehp:tuto_duelimg04.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg05.png | 7f7bdfb2 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_g.ehp:tuto_duelimg05.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg06.png | 931db074 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_g.ehp:tuto_duelimg06.gim |

### Texture che restano come l'originale
`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `parts` sono fogli di icone in pixel art (con NEU/NEW): restano com'erano, coperti dall'ingrandimento `upscale_extra` come nelle altre lingue; il testo non e' stato cambiato. Le texture neutre vengono dal pack di base. In spagnolo anche `score-top` (TURNO) ha lo stesso hash dell'italiano e `card_icon03` e' in `upscale_extra`.

## B4. Il foglio dei numeri del duello (`card_icon03`)

Foglio unico con cifre LP, tempo, tasti e moltiplicatori; hash diverso per lingua. Ricetta scelta dall'utente (`tools/ui_textures/icon03_languages.py`, rilanciare con `--apply`):
- righe 0-180 (cifre piccole e segni, tasti arancioni 1/2/3, cifre grandi 0-9 con "LP", cifre piccole 0-9): **dal pack USA**, pixel art netta;
- celle in cui il gioco europeo differisce dal pack USA (spunta nera, palla grigia, pillola vuota, parola del tempo): **pixel originali ingranditi 4x senza sfumare**; parola del tempo **ZEIT**; la pillola arancione ("Single" nel pack USA) resta **vuota**;
- righe >= 181 (moltiplicatori x1..x12, icone, carte, frecce): dal foglio italiano gia' nel pack (`tools/data/card_icon03_base_it.png`);
- le celle europee si incollano **solo nella loro fascia** di righe (altrimenti rovinano la parte alta delle cifre grandi).

File: it -> `ui_it/scritte_duello/basic_ii__card_icon03.png` (hash 376925c7); fr -> `upscale_extra/3e5482fd.png`; en ee0c44c3; de ffe309a6; es 859eea2b. Anteprime in `confronti/icon03/`.

## B5. Targa del titolo

`python tools/ui_textures/mystic_tomato_title.py de` genera 2 PNG (`542eff79685c434d`, `705176739829dcf5`, tessere 18 e 19 del fondale di 20 tessere 128x64 `title_menu_i.ehp: main_title00001..00020`) con la carta 4930 nella lingua + la formula "versione" + la bandiera, font PT Sans Bold: **"EDITION MYSTISCHE TOMATE"**. La targa **va inclusa solo per la lingua scelta** (vive in `moduli/de/intro/title_screen/`); il pack di base originale ha le tessere senza banner. File in questo pack: `moduli/de/intro/title_screen/00000000542eff79685c434d.png`, `moduli/de/intro/title_screen/00000000705176739829dcf5.png`.

## B6. `textures.ini` e composizione

`tools/gen_ini.py TOOLS US_INI CARD_DIR OUT_INI i=it +extra_it.ini +ui_it.ini +dati/upscale_extra.ini` converte il `textures.ini` USA in quello EU: le voci non-carta restano (texture neutre = stessi hash); le voci carta sono rigenerate dagli archivi `card/*.cip` EU per le 5 lingue (`i=it` rimappa `cards/large/X.png` -> `cards/large_it/X.png`); aggiunge l'etichetta Magia/Trappola (`extra_it.ini`), le righe `ui_it` e `upscale_extra.ini`. Si fa anche per i 3 stili carte. Se gli stessi pixel esistono in piu' lingue vince la prima in `e i f g s` (per questo atlante, banner e tabella attributi sono "uno per installazione").

Righe `ui_de` nel `de.ini`: 98. Frequenza dei prefissi: `docs/changes_de/ini_lines.csv`. Controllo: ogni riga `ui_de/...` deve puntare a un file esistente e non devono esserci hash duplicati.

## B7. Installazione e impostazioni

PC: copiare `ULES00600` in `<PPSSPP>/PSP/TEXTURES/` (Android: `textures.zip` in `.../TEXTURES/ULES00600/`, senza estrarlo; rigenerare lo zip con le correzioni). Impostazioni: **Sostituisci texture ON**, risoluzione di rendering **4x**, lingua del gioco = lingua del modulo (la lingua e' scritta nel **salvataggio**). Dopo aver cambiato un solo PNG basta copiarlo e riavviare PPSSPP (cache). Per provare i testi usare la ISO `_definitiva`.

---

# C. SCELTE EDITORIALI

- **Rector Sheppard** (come nei dialoghi) nelle schede e nelle mappe ("Oficina del Rector"); dormitori **Slifer Rojo, Ra Amarillo, Obelisco Azul**; **Jinetes de la Sombra**; "Habitación" al posto di "Alójese" (Room).
- Sake/shochu e abito da cameriera come nelle altre lingue (`st01_t01/Scr003E`), `st02_t01/Scr101E` ruotato; "Sirviente de la Calavera", "Toon", "Archidemonio", "Trío Ojama" e accenti dei nomi come sulle carte.
- Opzioni: "EN/FUERADE" -> "ON/OFF"; messaggi del titolo ("nuevos datos de juego"), lezioni del tutorial ("le turno" -> "es el turno de", tasti x/o scambiati, codici colore chiusi), paragrafo finale dei Duelos Tag tradotto (era troncato/in inglese).
- Termini lasciati come nel gioco: "Invocación por Sacrificio", "Tributar", "Efecto de Blanco", "Tronco" (domande aperte in `docs/changes_es/open_questions_es.md`).
- Foglio numeri: cifre/LP dal pack USA, x1..x12 dal foglio italiano, parola del tempo ZEIT.

### Voci del registro delle scelte per questa lingua (`tools/data/editorial_choices.json`)
| id | originale | corretto | ereditata | motivo |
|---|---|---|---|---|
| st01_t01/Scr003E#146 | Meinem Vater gehört eine Firma,⏎die scharfe Saucen herstellt. | Meinem Vater gehört eine⏎Sake-Brauerei. | no | sake al posto di salsa piccante (fedele al giapponese: la famiglia di Chumley fa sake) |
| st01_t01/Scr003E#147 | Er hat mir zusammen mit dem Taschengeld⏎auch etwas scharfe Sauce geschickt.⏎Ich mach dir einen guten Preis.⏎Interesse? | Er hat mir zusammen mit dem Taschengeld⏎auch etwas Shochu geschickt.⏎Ich mach dir einen guten Preis.⏎Interesse? | no | shochu al posto di salsa piccante |
| st01_t01/Scr003E#150 | Meinem Vater gehört eine Firma,⏎die scharfe Saucen herstellt. | Meinem Vater gehört eine⏎Sake-Brauerei. | no | come 146 |
| st01_t01/Scr003E#151 | Er hat mir zusammen mit dem Taschengeld⏎auch etwas scharfe Sauce geschickt.⏎Ich mach dir einen guten Preis.⏎Interesse? | Er hat mir zusammen mit dem Taschengeld⏎auch etwas Shochu geschickt.⏎Ich mach dir einen guten Preis.⏎Interesse? | no | come 147 |
| st01_t01/Scr003E#163 | Wow. Du hast es geschafft.⏎《C026_2》...⏎Im Bikini! | Wow. Du hast es geschafft.⏎《C026_2》...⏎Im Dienstmädchen-Outfit! | no | abito da cameriera al posto di bikini (giapponese: メイド服) |
| st01_t01/Scr003E#168 | Wow. Du hast es geschafft.⏎《C026_2》...⏎Im Bikini! | Wow. Du hast es geschafft.⏎《C026_2》...⏎Im Dienstmädchen-Outfit! | no | come 163 |
| st01_t01/Scr003E#188 | Tja, ein wenig schon ... | None | si | solo italiano: "sto sbavando" era un errore di traduzione (giapponese: "non sono poi così bravo") |
| st01_t01/Scr003E#189 | Hey, kannst du was für mich zeichnen?⏎Zeichne mir 《C026_2》 im Bikini! | Hey, kannst du was für mich zeichnen?⏎Zeichne mir 《C026_2》 im Dienstmädchen-Outfit! | no | abito da cameriera al posto di bikini |
| st01_t01/Scr003E#191 | Hier, du kannst den hier nehmen! | Hier, nimm dieses Dienstmädchen-Outfit! | no | Syrus passa un abito da cameriera come modello (メイド服): col bikini la battuta non aveva senso |
| st01_t01/Scr003E#194 | Tja, ein wenig schon ... | None | si | come 188 |
| st01_t01/Scr003E#195 | Hey, kannst du was für mich zeichnen?⏎Zeichne mir 《C026_2》⏎im Bikini! | Hey, kannst du was für mich zeichnen?⏎Zeichne mir 《C026_2》⏎im Dienstmädchen-Outfit! | no | come 189 |
| st01_t01/Scr003E#197 | Hier, du kannst den hier nehmen! | Hier, nimm dieses Dienstmädchen-Outfit! | no | come 191 |

Altre scelte e la rilettura delle frasi dei duelli: `docs/EDITORIAL_CHOICES.md`.

# D. VERIFICA IN GIOCO

- **Visti in gioco** (ISO `_definitiva` + modulo `de`, nuovo gioco in tedesco, 2026-10-12): scelta lingua, titolo con targa "MYSTISCHE TOMATE EDITION" e Neues Spiel/Fortfahren, "Daten geladen", Hauptmenue HD, Deck-Menue (Deck bearbeiten / Rezeptanzeige), editor del deck (linguette Deck/Fusion/Side/Truhe, "Persoenliches Deck", "Eigene Kartentypen", Hilfe), Rezeptanzeige (Benutzer/Charakter, Fusionsdeck), conferma "Deckbearbeitung verlassen", calendario ("1. Mai / Montag", "92 Tage bis zum Turnier"), mappa ("Duellakademie", elenco luoghi), menu dell'ufficio (Reden/Duell/Gegenstaende/PDA), dialoghi del cancelliere e di Crowler in Klassenzimmer con le correzioni (Buero des Kanzlers, Duellakademie, Haupttor...), box a 2-3 righe senza tagli.
- **Non visti** (solo letti e confrontati con l'originale nei fogli di confronto): Kette, Direktangriff, fine duello, sasso-carta-forbici, ZWEITER/ERSTER, 1. Runde, tutorial e lezioni, negozio (AUSVERKAUFT, "Gekaufte Karten"), laboratorio (Labor, Konverter, Miete), PDA, album, Optionen, carte con testo nuovo, frasi dei duelli, schermata VS.
- **Visti nel duello dimostrativo del titolo** (2026-10-12): schermata VS ("NORMALES DUELL", "Einzelmodus", "Gegen", distintivi), HUD del duello, frasi dei duellanti in tedesco, descrizioni di carte in tedesco; "Draw Phase" resta inglese come nell'originale. Difetti segnalati dall'utente: font dei dialoghi non HD (testo di sistema, non sostituibile con le texture) e menu di salvataggio PSP in francese (lingua di sistema di PPSSPP).

# E. COME RIGENERARE TUTTO

```
# ISO (tutte le lingue insieme)
python tools/corrections/build_dialogues.py de
python tools/corrections/generate_card_corrections.py de CARDINFO_de.ehp          # carte
python tools/corrections/apply_to_iso.py PSP/GAME/ULES00600_..._EUR.iso PSP/GAME/ULES00600_..._EUR_definitiva.iso
# immagini
python tools/generate_language.py fr PACK CARDINFO US_INI CLEAN_DIR OUT [ID...]
TF1_LANG=de python tools/ui_textures/<famiglia>.py USRDIR PACK_US <modulo>      # per ognuna delle 8 famiglie (intera!)
python tools/ui_textures/icon03_languages.py --apply ; python tools/ui_textures/mystic_tomato_title.py de
python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules USRDIR/card OUT de --copia
# questo documento
python tools/analysis/document_changes.py ISO_ORIG ISO_DEF de docs/changes_de
python tools/analysis/document_pack.py ISO_ORIG de docs/changes_de
python tools/analysis/text_comparisons.py de
python tools/analysis/write_changes_document.py de
```
Input esterni da avere (controlla che esistano): ISO originale, USRDIR estratta (`tools/analysis/extract_usrdir.py`), pack USA di MikeyMK `ULUS10136` (in una cartella fuori dal progetto).

# F. LIMITI E PUNTI APERTI

- Texture tedesche aggiunte il 2026-10-13 (`lettere_esito` 28, `scritte_duello` 15; prima date per uguali all'inglese, ed era un errore: vedi `docs/changes_de/texture_texts_de.md`): confrontate con l'originale a bassa risoluzione (sovrapposizione delle tessere, fogli di controllo), **non ancora viste in gioco**. Da verificare: il centraggio dei puntini della Ä di NÄCHSTER SPIELER (sprite a parte), la larghezza di SPIELZUG nel badge e la sagoma di DU GEWINNST.
- 5 fogli di icone in pixel art (`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `parts`) restano ingranditi dal pack (domanda aperta n. 7 in `open_questions_de.md`; in `pda_pack01` il gioco ha un residuo italiano "NUOVO" accanto ai "NEU", come in fr/es).
- `textures.zip` Android per il tedesco: non fatto; nessuna prova su telefono.
- Il nome del parlante nella casella del dialogo non e' modificabile (EBOOT cifrato).
