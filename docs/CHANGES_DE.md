# CHANGES OF THE MYSTIC TOMATO VERSION FOR GERMAN

**Complete** document of everything the "Mystic Tomato Version" changes for german: (A) the **direct changes to the ISO**, (B) the **texture pack** (how it is made, what it contains, how it is composed), (C) the editorial choices, (D) what has been verified in game and what has not, (E) how to regenerate everything.

**This file is generated** by `tools/analysis/write_changes_document.py de` from the real data: byte-by-byte comparison between the original ISO `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` and the corrected ISO `..._definitiva.iso` (`document_changes.py`) and a scan of the pack (`document_pack.py`). The row-by-row lists are in `docs/changes_de/*.csv` (`;` separator, UTF-8 with BOM, line breaks as `⏎`): they are the **exact list** of every change. Regenerate everything after each modification.

For the general method and for the other languages: `docs/NEW_LANGUAGE_GUIDE.md`; technical details of the scripts: `docs/TUTORIAL.md`; decisions: `docs/EDITORIAL_CHOICES.md`; neutral/specific textures: `docs/TEXTURE_INVENTORY.md`.

## Index
- A. Changes to the ISO: A1 overview · A2 cards · A3 dialogues · A4 duel sentences · A5 interface strings · A6 Spell/Trap label · A7 touched files and technical details · A8 what cannot be changed
- B. Texture pack: B1 origin and structure · B2 card images · B3 HD interface (`ui_de`) · B4 number sheet (`card_icon03`) · B5 title plate · B6 textures.ini and composition · B7 installation
- C. Editorial choices · D. In-game verification · E. How to regenerate · F. Limits and open points

---

# A. CHANGES TO THE ISO

## A1. Overview

The original ISO is **never modified**. `tools/corrections/apply_to_iso.py ISO_ORIG ISO_OUT [languages]` creates a copy in which some `.ehp` archives are rewritten. If an archive grows (longer text) it is **put again at the end of the ISO** in a new sector and its entry in the ISO9660 directory is reassigned (`pycdlib`); for this reason the `_definitiva` ISO weighs ~909 MB (the original ~761 MB). **Always run it without a list of languages (or with all of them)**: with a single language it overwrites the others.

| What | Quantity (derived from the ISO comparison) | Where the data lives | CSV file |
|---|---|---|---|
| Cards with changed text (name and/or description) | 258 cards (258 fields) | `tools/data/card_corrections_de.json` from `tools/corrections/rules_de.py` | cards.csv |
| Story dialogue lines | 1649 lines | `tools/data/dialogue_touchups_de.json` (+ base) | dialogues.csv |
| Duelist sentences in duels | 40 unique sentences (66 entries in all the archives) | `tools/data/duel_line_corrections_de.json` | duel_lines.csv |
| Interface strings (help, cards, records, tutorial, menus...) | 581 unique strings (1426 entries, 55 archives) | `tools/corrections/string_rules_de.py` + `tools/data/ui_texts.json` | ui_strings.csv |
| Images replaced inside the ISO | 6 ([SPELL CARD/TRAP CARD] label of the large card) | `apply_to_iso.py` (copies the language's `card_spell_trap.gim`) | iso_images.csv |
| ISO files touched (`.ehp` archives) | 179 | - | touched_files.csv |
| Other technical differences (recomputed offsets) | 254 | - | other.csv |

## A2. Card texts

Archive: `PSP_GAME/USRDIR/duelsys/cardinfo_fra.ehp` (tables `CARD_Name_*`, `CARD_Desc_*`, `CARD_Indx_*`). **258 cards** have a modified name and/or description. Only **objective errors** are corrected (typos, accents, apostrophes, spaces, inconsistent capitalization, agreement, fixed plurals, leftovers from other languages); official names and the game's terminology are not touched.

How: every card was read (it: 2,479 texts, one by one; fr: audit against the official database + reading). Rules in `tools/corrections/rules_de.py`: **18 global rules** (regexes applied to the names and descriptions of all the cards) and **243 per-card corrections** (`PER_CARD`: id, field, old, new, reason; the old text must exist exactly). `generate_card_corrections.py de CARDINFO` (writes `card_corrections_{L}.json` starting from the original texts) produces the json; `apply_to_iso` writes it into the ISO; the HD images of the touched cards are regenerated (section B2).

### Global rules (all)
| pattern (regex) | replacement | reason |
|---|---|---|
| \baugezeichneten\b | ausgezeichneten | typo |
| \bausgestatte\b | ausgestattete | typo |
| \benstanden\b | entstanden | typo |
| \bsprirituelle\b | spirituelle | typo |
| \bbeeinflußt\b | beeinflusst | spelling: ss after a short vowel |
| \bAnulliere\b | Annulliere | typo |
| \bZauberabsorbtion\b | Zauberabsorption | typo (Absorption) |
| \bSchadensverrechnung\b | Schadensberechnung | game terminology: elsewhere "Schadensberechnung" |
| \bKartename\b | Kartenname | typo |
| auf deiner Spielfeldseite ist, und dein Gegner keine | auf deiner Spielfeldseite ist und dein Gegner keine | superfluous comma (Toon-Karten) |
| dessen DEF niedriger sind als die ATK | dessen DEF niedriger ist als die ATK | agreement (DEF is singular) |
| auf die Hand seines Besitzers zurück gegeben | auf die Hand seines Besitzers zurückgegeben | compound written as one word (Zusammenschreibung) |
| die Karte auf zu decken | die Karte aufzudecken | compound written as one word (Zusammenschreibung) |
| in der gleichen Höhe, wie die ursprüngliche ATK des Monsters, zu zufügen | in der gleichen Höhe wie die ursprüngliche ATK des Monsters zuzufügen | compound written as one word and commas |
| an Stelle 1 beliebigen Fusionsmaterial-Monsterkarte | an Stelle einer beliebigen Fusionsmaterial-Monsterkarte | article (as in the other cards) |
| \bJedesmal\b | Jedes Mal | spelling |
| \bjedesmal\b | jedes Mal | spelling |
| Spezialaktivierung | Spezialbeschwörung | translation: Special Summon (EN) is not an activation |

### Per-card corrections (all)
| id | field | old | new | reason |
|---|---|---|---|---|
| 4452 | desc | Schanz | Schwanz | typo (EN: tail) |
| 4667 | desc | uberprufen | überprüfen | umlauts replaced by plain vowels |
| 4667 | desc | nachsten | nächsten | umlauts replaced by plain vowels |
| 4667 | desc | Spielzugen | Spielzügen | umlauts replaced by plain vowels |
| 4667 | desc | zerstoren | zerstören | umlauts replaced by plain vowels |
| 4667 | desc | oder hoher | oder höher | umlauts replaced by plain vowels |
| 5575 | name | verrringern | verringern | typo |
| 5824 | desc | Entfere | Entferne | typo |
| 5829 | desc | Friehof | Friedhof | typo |
| 5930 | desc | Verteidigungepsoition | Verteidigungsposition | typo |
| 6085 | desc | enfernen | entfernen | typo |
| 6133 | desc | Spielfeld , | Spielfeld, | space before the comma |
| 6168 | desc | aktiveren | aktivieren | typo |
| 6368 | desc | enfernt | entfernt | typo |
| 6542 | desc | Spezialbschwörung | Spezialbeschwörung | typo |
| 6582 | desc | erhälst | erhältst | typo |
| 6681 | desc | Enterne | Entferne | typo |
| 6076 | desc | Fur jede | Für jede | umlaut replaced by a plain vowel |
| 4017 | desc | Schwert ähnlicher Dornen | schwertähnlicher Dornen | compound written as one word (Zusammenschreibung) |
| 4035 | desc | rauhesten | rauesten | spelling (as in beeinflusst: reformed spelling) |
| 4069 | desc | Dieses Karte | Diese Karte | agreement |
| 4074 | desc | Ein Axt schwingende Ungeheuer-Krieger | Ein Axt schwingender Ungeheuer-Krieger | agreement |
| 4172 | desc | Jedesmal | Jedes Mal | spelling |
| 4208 | desc | Es greift an indem | Es greift an, indem | comma |
| 4235 | desc | Macht anstatt das Leben | Macht, anstatt das Leben | comma before the infinitive clause with anstatt |
| 4238 | desc | Waffe,die | Waffe, die | space after the comma |
| 4239 | desc | Unterweltler, des angeblich | Unterweltler, der angeblich | typo |
| 4258 | desc | Schönheit, zerkratzt sie | Schönheit zerkratzt sie | superfluous comma after the initial complement |
| 4292 | desc | erschaffen nur um die Tore | erschaffen nur, um die Tore | comma before um ... zu |
| 4312 | desc | ATK- Wert | ATK-Wert | superfluous space |
| 4373 | desc | Life Points, und greifst | Life Points und greifst | superfluous comma (same subject) |
| 4374 | desc | Erhöht sich die ATK dieser Karte um 100 Punkte für jede Monsterkarte im deinem Friedhof. | Die ATK dieser Karte erhöht sich um 100 Punkte für jede Monsterkarte in deinem Friedhof. | word order (EN: Increase) and "im deinem" |
| 4398 | desc | kann per Spezialaktivierung vom Deck | kann als Spezialbeschwörung vom Deck | translation (EN: Special Summoned) |
| 4400 | desc | Typ Maschine ist, und den | Typ Maschine ist und den | superfluous comma |
| 4431 | desc | ab um bis zu 2 | ab, um bis zu 2 | comma before um ... zu |
| 4496 | desc | Life Pointsn | Life Points | typo |
| 4506 | desc | als einer Normalbeschwörung oder Flippbeschwörung | als Normalbeschwörung oder Flippbeschwörung | grammar |
| 4512 | desc | FusionsDeck | Fusionsdeck | capital letter (as elsewhere: Fusionsdeck) |
| 4522 | desc | erhöht sich die ATK und DEF dieser Karte | erhöhen sich ATK und DEF dieser Karte | agreement (plural) |
| 4541 | desc | Ein Menschen ähnlicher Mantis | Eine menschenähnliche Mantis | gender and compound written as one word |
| 4574 | desc | Ein Menschen ähnlicher Dinosaurier | Ein menschenähnlicher Dinosaurier | compound written as one word (Zusammenschreibung) |
| 4576 | desc | Eine getigerter Drache | Ein getigerter Drache | agreement |
| 4596 | desc | riesigen Rüssel | riesigen Schnabel | translation (EN: beak; name: Schnabelschlange) |
| 4609 | desc | Eine schöner und starker | Ein schöner und starker | agreement |
| 4622 | desc | „Flipp“-Aktivierung), sind ATK- und DEF-Werte | „Flipp“-Aktivierung) sind die ATK- und DEF-Werte | superfluous comma and article |
| 4022 | desc | soviel Schaden wie | so viel Schaden wie | spelling |
| 4738 | desc | soviel Schaden zuzufügen | so viel Schaden zuzufügen | spelling |
| 4652 | desc | härter ist als er aussieht | härter ist, als er aussieht | comma |
| 4654 | desc | durch sein Vorwärtsstürzen | durch ihr Vorwärtsstürzen | agreement (die Maschine) |
| 4660 | desc | erhöht seinen ATK neben 700 Punkten | erhöht seine ATK um 700 Punkte | translation (EN: increases its ATK by 700) |
| 4664 | desc | Wenn ein mit dieser Karte ausgerüstetes Monster angegriffen wird, kannst du seinen ATK-Wert um die Hälfte des ATK-Werts des Angegriffenen erhöhen. | Wenn ein mit dieser Karte ausgerüstetes Monster angreift, kannst du seinen ATK-Wert um die Hälfte des ATK-Werts des angegriffenen Monsters erhöhen. | translation (EN: When attacking with a monster equipped with this card) |
| 4687 | desc | Spezialbeschwörung) eine DEF | Spezialbeschwörung), eine DEF | comma closing the relative clause |
| 4688 | desc | Spezialbeschwörung) eine ATK | Spezialbeschwörung), eine ATK | comma closing the relative clause |
| 4691 | desc | mehr als 2000 Punkte sind | mehr als 2000 Punkte beträgt | agreement |
| 4692 | desc | auf der Angriffsposition | in Angriffsposition | grammar |
| 4694 | desc | statt dessen | stattdessen | spelling |
| 4748 | desc | spezialaktiviert werden | als Spezialbeschwörung beschworen werden | translation (EN: Special Summoned) |
| 4750 | desc | maximal einen Zauberzählmarke | maximal eine Zauberzählmarke | gender |
| 4750 | desc | den Zauberzählmarke | die Zauberzählmarke | gender |
| 4755 | desc | aktiviert wird (ohne Spezialaktivierung) | beschworen wird (ohne Spezialbeschwörung) | translation (EN: summoned) |
| 4795 | desc | aktiviert wird (einschließlich Spezialaktivierung) | beschworen wird (einschließlich Spezialbeschwörung) | translation (EN: Summoned) |
| 4780 | desc | Kampf mit ein Monster der Stufe 7 oder niedriger zerstört. | Kampf mit einem Monster der Stufe 7 oder niedriger zerstört werden. | grammar |
| 4803 | desc | des Spielzugs in dem diese | des Spielzugs, in dem diese | comma |
| 4804 | desc | Monster deines Gegner angreift | Monster deines Gegners angreift | typo |
| 4814 | desc | deines Gegners nachdem du diese Karte aktiviert hast, kann | deines Gegners, nachdem du diese Karte aktiviert hast, kann | comma |
| 4817 | desc | Diese Monster kann | Dieses Monster kann | agreement |
| 4830 | desc | keine Monster aktivieren (einschließlich „Flipp“- und Spezialaktivierung) | keine Monster beschwören (einschließlich „Flipp“- und Spezialbeschwörung) | translation (EN: summon) |
| 4834 | desc | Am Ende der Battle Phase, gib | Am Ende der Battle Phase gib | comma |
| 4855 | desc | Wenn Dein Gegner | Wenn dein Gegner | capital letter |
| 4861 | desc | Normal-, Flipp, oder Spezialbeschwörung | Normal-, Flipp- oder Spezialbeschwörung | hyphen and comma |
| 4861 | desc | das Beschworene Monster | das beschworene Monster | capital letter |
| 4892 | desc | statt dessen | stattdessen | spelling |
| 4944 | desc | Permante Zauberkarte | Permanente Zauberkarte | typo |
| 5030 | desc | beschwöre dieses Karte | beschwöre diese Karte | agreement |
| 5033 | desc | ATK und DEF dieses Monster zu 1000 | ATK und DEF dieses Monsters zu 1000 | genitive |
| 5042 | desc | Jedesmal | Jedes Mal | spelling |
| 5067 | desc | Nach der Schadensberechnung, verringere | Nach der Schadensberechnung verringere | comma |
| 5113 | desc | Jedesmal | Jedes Mal | spelling |
| 5197 | desc | Jedesmal | Jedes Mal | spelling |
| 5164 | desc | jedesmal | jedes Mal | spelling |
| 5116 | desc | Die Spielsteine | Die Spielmarken | terminology (Spielmarke) |
| 5129 | desc | Während deiner End Phase, zerstöre | Während deiner End Phase zerstöre | comma |
| 5142 | desc | dessen DEF niedriger sind als | dessen DEF niedriger ist als | agreement |
| 5173 | desc | geschickt wird während sie verdeckt liegt, dann wird deinem Gegner 500 Punkte Schaden an seiner LP verursacht. | geschickt wird, während sie verdeckt liegt, dann werden deinem Gegner 500 Punkte Schaden an seinen LP verursacht. | comma and agreement |
| 5175 | desc | auf 3000 gesetzt solange | auf 3000 gesetzt, solange | comma |
| 5177 | desc | wird ein „Jungfernmarke“ getan | wird eine „Jungfernmarke“ getan | gender |
| 5178 | desc | mit einem „Jungfernmarke“ darauf | mit einer „Jungfernmarke“ darauf | gender |
| 5178 | desc | das ausgerüstet Monster | das ausgerüstete Monster | agreement |
| 5179 | desc | seines Angriffs, eine aufgedeckte | seines Angriffs eine aufgedeckte | superfluous comma |
| 5180 | desc | die ATK des anderen Monster. | die ATK des anderen Monsters. | genitive |
| 5181 | desc | auf dem Spielfeld deines Feldes | auf der Spielfeldseite deines Gegners | translation (EN: opponent's side of the field) |
| 5182 | desc | um 600 erhöht Jedesmal, | um 600 erhöht. Jedes Mal, | missing full stop and spelling |
| 5182 | desc | bezahlen um am Ende | bezahlen, um am Ende | comma |
| 5185 | desc | zugefügt wird der die Karte kontrolliert | zugefügt wird, der die Karte kontrolliert | comma |
| 5189 | desc | Life Points um eine Karte | Life Points, um eine Karte | comma |
| 5189 | desc | drei Mal benutzt hast, dann erhält | drei Mal benutzt hast, erhält | syntax |
| 5190 | desc | ab.  Wähle ein 1 Monster | ab. Wähle 1 Monster | double space and "ein 1" |
| 5202 | desc | gelegt wurden, unter dein Deck | gelegt wurde, unter dein Deck | agreement |
| 5223 | desc | Nur der „Dunkler Magier“ oder die „Dunkles Magier-Mädchen“ darf | Nur „Dunkler Magier“ oder „Dunkles Magier-Mädchen“ darf | wrong articles before the names |
| 5239 | desc | Regelgzwecken | Regelzwecken | typo |
| 5242 | desc | wenn sich der „Kathedrale der Adligen“ | wenn sich die „Kathedrale der Adligen“ | gender |
| 5260 | desc | im Spielzugs deines Gegners | im Spielzug deines Gegners | case |
| 5263 | desc | bestimmt, und zerstört die Zauberkarte | bestimmt, und zerstöre die Zauberkarte | imperative mood (as in the whole text) |
| 5275 | desc | zurück ihn ihre ursprüngliche | zurück in ihre ursprüngliche | typo |
| 5286 | desc | mit allen seiner Monster | mit allen seinen Monstern | case |
| 5290 | desc | jede zerstöre Zauberkarte | jede zerstörte Zauberkarte | typo |
| 5295 | desc | Beherscher | Beherrscher | typo |
| 5295 | desc | aus einen Kampf | aus einem Kampf | case |
| 5299 | desc | Gibt das als Ziel bestimmte Monster | Gib das als Ziel bestimmte Monster | imperative mood |
| 5313 | desc | genau soviel Stufen haben wie | genauso viele Stufen haben wie | spelling |
| 5334 | desc | dessen DEF niedriger sind als | dessen DEF niedriger ist als | agreement |
| 5351 | desc | wähle 2 Karte im Friedhof | wähle 2 Karten im Friedhof | plural |
| 5384 | desc | beschworen wurde Zusätzlich | beschworen wurde. Zusätzlich | missing full stop |
| 5433 | desc | Standby Phase deines Gegner so | Standby Phase deines Gegners so | genitive |
| 5453 | desc | wird der ATK dieser Karte | wird die ATK dieser Karte | gender |
| 5452 | desc | dessen DEF niedriger sind als | dessen DEF niedriger ist als | agreement |
| 5452 | desc | Life Points deines Gegner als | Life Points deines Gegners als | genitive |
| 5477 | desc | als Tribut an um den Life Points | als Tribut an, um den Life Points | comma |
| 5479 | desc | Ziehe Karten bis du | Ziehe Karten, bis du | comma |
| 5482 | desc | in der entsprechenden Spielzug | in dem entsprechenden Spielzug | case |
| 5499 | desc | bleibt bestehen bis die | bleibt bestehen, bis die | comma |
| 5531 | desc | Life Points deines Gegner Schaden | Life Points deines Gegners Schaden | genitive |
| 5530 | desc | Stufe hat wie dein Gegner genannt hat | Stufe hat, wie dein Gegner genannt hat | comma |
| 5546 | desc | zu sein Deck hinzu | zu seinem Deck hinzu | case |
| 5546 | desc | von seinem Deck wie er vorher in sein Deck zurück gelegt hat | von seinem Deck, wie er vorher in sein Deck zurückgelegt hat | comma and compound written as one word |
| 5574 | desc | Diese „Klon-Spielmarken“ hat | Diese „Klon-Spielmarke“ hat | agreement |
| 5574 | desc | das gleiche Eigenschaft | die gleiche Eigenschaft | gender |
| 5604 | desc | Battle Phase kannst diesen Effekt | Battle Phase kannst du diesen Effekt | missing pronoun |
| 5608 | desc | auf die Hand zurück gegeben | auf die Hand zurückgegeben | compound written as one word (Zusammenschreibung) |
| 5608 | desc | werden beide gewählte Karten | werden beide gewählten Karten | declension |
| 5614 | desc | Karte vergangen sind. | Karte vergangen sind, zu. | missing separable verb (zufügen) |
| 5676 | desc | oben auf sein Deck zurück | oben auf dein Deck zurück | pronoun (sein/dein) |
| 5678 | desc | deines Gegners niedriger als die DEF | deines Gegners niedriger ist als die DEF | missing verb |
| 5689 | desc | Kampf mit der diese Spielmarke werden | Kampf mit dieser Spielmarke werden | typo |
| 5689 | desc | wird die diese Spielmarke zerstört | wird diese Spielmarke zerstört | typo |
| 5699 | desc | Während der Schadensberechnung, erhöhe | Während der Schadensberechnung erhöhe | comma |
| 5754 | desc | in deiner Hand ist, kannst du sie | in deiner Hand hast, kannst du sie | verb (EN: if you have) |
| 5755 | desc | Der DEF dieses Monsters | Die DEF dieses Monsters | gender |
| 5784 | desc | soviele Stufen wie | so viele Stufen wie | spelling |
| 5788 | desc | dieser Karte, gewinnst du | dieser Karte gewinnst du | comma |
| 5815 | desc | niedriger sind als die DEF dieses Monsters | niedriger ist als die DEF dieses Monsters | agreement |
| 5817 | desc | indem Du 2 FINSTERNIS Monster in deinem Friedhof aus dem Spiel entfernt. | indem du 2 FINSTERNIS Monster in deinem Friedhof aus dem Spiel entfernst. | verb person and capital letter |
| 5818 | desc | auf die Hand ihres Besitzers. | auf die Hand ihres Besitzers zurück. | missing verb (EN: return) |
| 5824 | desc | als diese Karte aus dem Spiel zu entfernen. | als diese Karte zu zerstören. | translation (EN: destroy) |
| 5828 | desc | gegnerischen um Spielzugs 300 Punkte | gegnerischen Spielzugs um 300 Punkte | word order |
| 5830 | desc | aus dem Spiel entfernt wird. Falls diese Karte | aus dem Spiel entfernt werden. Falls diese Karte | agreement |
| 5830 | desc | des nächsten Spielzug deines Gegners | des nächsten Spielzugs deines Gegners | genitive |
| 5836 | desc | erhöhen dein Gegner 700 Punkte Schaden | erhält dein Gegner 700 Punkte Schaden | verb (EN: inflict) |
| 5843 | desc | auf Deiner Hand | auf deiner Hand | capital letter |
| 5844 | desc | keine Zauberkarte in deinem Friedhof befinden | keine Zauberkarte in deinem Friedhof befindet | agreement |
| 5854 | desc | erhält diese Karte einen Zauberzählmarke | erhält diese Karte eine Zauberzählmarke | gender |
| 5854 | desc | Wenn der 4. Zauberzählmarke | Wenn die 4. Zauberzählmarke | gender |
| 5854 | desc | eine Zauberkarte aktiviert hat, erhält | eine Zauberkarte aktiviert, erhält | agreement |
| 5854 | desc | Zauberkarte aktiviert hat erhält 3000 | Zauberkarte aktiviert hat, erhält 3000 | comma |
| 5860 | desc | beschworen werden indem, 1 LICHT | beschworen werden, indem 1 LICHT | comma |
| 5860 | desc | Zahle 1000 Life Points um alle | Zahle 1000 Life Points, um alle | comma |
| 5871 | desc | verlor seine Herz | verlor sein Herz | gender |
| 5884 | desc | eines gegnerischen in Verteidigungsposition liegendes Monster angreift | eines gegnerischen, in Verteidigungsposition liegenden Monsters angreift | case |
| 5895 | desc | auf den Friedhof um alle Karten auf dem Spielfeld, außer dieser Karte, zu auf den Friedhof zu legen. | auf den Friedhof, um alle Karten auf dem Spielfeld, außer dieser Karte, zu zerstören. | translation (EN: destroy) and syntax |
| 5896 | desc | als Tribut an um 1 Zauber- oder Fallenkarte | als Tribut an, um 1 Zauber- oder Fallenkarte | comma |
| 5897 | desc | Solange „Umi“ offen auf dem Spielfeld befindet | Solange sich „Umi“ offen auf dem Spielfeld befindet | missing reflexive pronoun |
| 5912 | desc | auf deiner Spielfeldseite um den Life Points | auf deiner Spielfeldseite, um den Life Points | comma |
| 5922 | desc | offen auf auf dem Spielfeld | offen auf dem Spielfeld | doubled word |
| 5943 | desc | Würfelergebnis solange die Karte | Würfelergebnis, solange die Karte | comma |
| 5987 | desc | auf dem Spielfeld werden bis zum Ende dieses Spielzugs zu 0. | auf dem Spielfeld wird bis zum Ende dieses Spielzugs zu 0. | agreement (DEF singular) |
| 6001 | desc | nicht Spezialbeschworen werden | nicht spezialbeschworen werden | lowercase |
| 6048 | desc | des ausgerüsteten Monster um 1000 | des ausgerüsteten Monsters um 1000 | genitive |
| 6066 | desc | deiner normalen Monstern der Stufe | deiner normalen Monster der Stufe | genitive plural |
| 6076 | desc | erhöht sich der ATK dieser Karte | erhöht sich die ATK dieser Karte | gender |
| 6097 | desc | diese offene Karten auf den Friedhof | diese offene Karte auf den Friedhof | number |
| 6133 | desc | auf deiner Spielfeld, dessen | auf deiner Spielfeldseite, dessen | truncated word (after the space rule) |
| 6158 | desc | Diese Spielmarke können nicht | Diese Spielmarken können nicht | agreement |
| 6166 | desc | annuliere die Effekt von allen | annuliere die Effekte von allen | plural |
| 6167 | desc | Falls 5 Zauberzählmarke auf | Falls 5 Zauberzählmarken auf | plural |
| 6167 | desc | mit 5 Zauberzählmarke auf den Friedhof | mit 5 Zauberzählmarken auf den Friedhof | plural |
| 6168 | desc | mit einem ATK von 2000 oder weniger | mit einer ATK von 2000 oder weniger | gender |
| 6234 | desc | durch die Welt wandernd um der stärkste | durch die Welt wandernd, um der stärkste | comma |
| 6234 | desc | Sei vorsichtig ihn nicht zu berühren, oder | Sei vorsichtig, ihn nicht zu berühren, oder | comma |
| 6244 | desc | In diesem Fall, wird die Grund-ATK | In diesem Fall wird die Grund-ATK | comma |
| 6249 | desc | in den Friedhof gelegt wird, fügen den Life Points beider Spieler | in den Friedhof gelegt wird, füge den Life Points beider Spieler | imperative mood |
| 6250 | desc | Zauberzählmarken um ein offenes Monster | Zauberzählmarken, um ein offenes Monster | comma |
| 6254 | desc | wird, gebe 1 Monster | wird, gib 1 Monster | imperative mood |
| 6262 | desc | in den Friedhof um 2 Monster | in den Friedhof, um 2 Monster | comma |
| 6262 | desc | Die Monster die auf diese Weise | Die Monster, die auf diese Weise | comma |
| 6282 | desc | Spielfeldseite um diese Karte zu aktivieren | Spielfeldseite, um diese Karte zu aktivieren | comma |
| 6285 | desc | als Tribut an um diese Karte zu aktivieren | als Tribut an, um diese Karte zu aktivieren | comma |
| 6287 | desc | Spezialbeschwörung wieder auf dein Feld zu bringen. | Spezialbeschwörung wieder auf dein Feld bringen. | syntax |
| 6287 | desc | wird ihr ATK um 500 Punkte erhöht | wird ihre ATK um 500 Punkte erhöht | gender |
| 6293 | desc | Friedhof ab um 1 Monster vom Typ Zombie | Friedhof ab, um 1 Monster vom Typ Zombie | comma |
| 6293 | desc | mit einem niedrigeren Stufe | mit einer niedrigeren Stufe | gender |
| 6303 | desc | und nehme sie auf deine Hand | und nimm sie auf deine Hand | imperative mood |
| 6308 | desc | es sei denn du zahlst | es sei denn, du zahlst | comma |
| 6320 | desc | Monster vom Typ Fels die vom Spiel entfernten wurden | Monster vom Typ Fels, die aus dem Spiel entfernt wurden | syntax |
| 6324 | desc | Die Grund-ATK und -DEF dieser Karte wird zur Anzahl | Die Grund-ATK und -DEF dieser Karte werden zur Anzahl | agreement |
| 6343 | desc | Das Eigenschaft dieser Karte | Die Eigenschaft dieser Karte | gender |
| 6344 | desc | ATK des zerstörten Monster zu | ATK des zerstörten Monsters zu | genitive |
| 6345 | desc | mit geringeren Grund-ATK als die ATK dieser Karte | mit geringerer Grund-ATK als die ATK dieser Karte | agreement |
| 6346 | desc | des Spielzuges in dem diese Karte | des Spielzugs, in dem diese Karte | comma |
| 6354 | desc | Zahle 300 Life Points um die verdeckten | Zahle 300 Life Points, um die verdeckten | comma |
| 6355 | desc | auf deiner Spielfeldseite um diese Karte zu aktivieren | auf deiner Spielfeldseite, um diese Karte zu aktivieren | comma |
| 6359 | desc | diese gesetzte Karte zerstört 1000 | diese gesetzte Karte zerstört, 1000 | comma |
| 6376 | desc | auf den Friedhof um alle Karten, außer dieser Karte, in den Händen | auf den Friedhof, um alle Karten, außer dieser Karte, in den Händen | comma |
| 6399 | desc | seine ATK niedriger sind als die ATK des Ziels | seine ATK niedriger ist als die ATK des Ziels | agreement |
| 6400 | desc | in deiner Haupt Phase | in deiner Main Phase | terminology (Main Phase) |
| 6400 | desc | eines Level 4 Monsters | eines Monsters der Stufe 4 | leftover English (Level) |
| 6409 | desc | Effekt 3 mal benutzt | Effekt dreimal benutzt | spelling |
| 6410 | desc | werden die die folgenden Effekte | werden die folgenden Effekte | doubled word |
| 6414 | desc | Die ATK von 1 offenen Monster auf dem Spielfeld werden bis zur End Phase | Die ATK von 1 offenen Monster auf dem Spielfeld wird bis zur End Phase | agreement |
| 6427 | desc | Die Grund-ATK dieser Karte werden zur Anzahl | Die Grund-ATK dieser Karte wird zur Anzahl | agreement |
| 6438 | desc | Würfel 3 mal | Würfel dreimal | spelling |
| 6450 | desc | verhindern, das irgendwelche | verhindern, dass irgendwelche | dass/das |
| 6454 | desc | darfst die Effekte von Zauber-, Fallen und Effektmonsterkarten durch das Ablegen einer Karte vom gleichen Typ, unterbrechen | darfst du die Effekte von Zauber-, Fallen- und Effektmonsterkarten durch das Ablegen einer Karte vom gleichen Typ unterbrechen | missing pronoun and punctuation |
| 6500 | desc | Schaden zu, jedes Mal wenn du | Schaden zu, jedes Mal, wenn du | comma |
| 6505 | desc | Spielfeldseite deines Gegner wählen | Spielfeldseite deines Gegners wählen | genitive |
| 6522 | desc | Keiner der Spieler kann als Fusionsbeschwörungen beschwören. | Keiner der Spieler kann Fusionsbeschwörungen durchführen. | syntax |
| 6524 | desc | kleiner oder gleich den ATK des ausgerüsteten Monsters sind | kleiner oder gleich der ATK des ausgerüsteten Monsters ist | agreement |
| 6530 | desc | Schaden zu, jedes Mal wenn ein Spieler | Schaden zu, jedes Mal, wenn ein Spieler | comma |
| 6541 | desc | ziehe soviele Karten | ziehe so viele Karten | spelling |
| 6543 | desc | Fallenkarteneffekts der Schaden zufügt | Fallenkarteneffekts, der Schaden zufügt | comma |
| 6550 | desc | die durch diesen Effekt zerstört wird, erhöht sich der ATK dieser Karte | die durch diesen Effekt aus dem Spiel entfernt wird, erhöht sich die ATK dieser Karte | translation (EN: removed from play) and gender |
| 6569 | desc | gleich oder höher als die ATK dieser Karte sind. | gleich oder höher als die ATK dieser Karte ist. | agreement |
| 6571 | desc | werden die ATK des gewählten Monsters halbiert | wird die ATK des gewählten Monsters halbiert | agreement |
| 6582 | desc | dessen ATK kleiner oder gleich dem Kampfschaden sind | dessen ATK kleiner oder gleich dem Kampfschaden ist | agreement |
| 6589 | desc | Monster deines Gegner diese | Monster deines Gegners diese | genitive |
| 6610 | desc | Wenn diese verdeckt Karte | Wenn diese verdeckte Karte | declension |
| 6617 | desc | kann benutzt werde, um | kann benutzt werden, um | typo |
| 6637 | desc | und das gleiche Eigenschaft wie | und die gleiche Eigenschaft wie | gender |
| 6638 | desc | in der Runde, in der es spezialbeschworen wurde | in der Runde, in der sie spezialbeschworen wurde | agreement |
| 6639 | desc | Das Eigenschaft dieser Karte | Die Eigenschaft dieser Karte | gender |
| 6639 | desc | Wenn dieser Karte erfolgreich Fusions beschworen werden, dann werden alle | Wenn diese Karte erfolgreich fusionsbeschworen wird, werden alle | grammar |
| 6639 | desc | mit den gleichen Attributen, steigt der ATK dieser hier um 300 Punkte | mit der gleichen Eigenschaft steigt die ATK dieser Karte um 300 Punkte | grammar |
| 6642 | desc | verdoppele allen Kampfschaden | verdopple allen Kampfschaden | imperative (as in the other cards) |
| 6654 | desc | Diese Spielmarke können nicht | Diese Spielmarken können nicht | agreement |
| 6661 | desc | auf deiner Spielfeldseite, nicht zerstört werden | auf deiner Spielfeldseite nicht zerstört werden | superfluous comma |
| 6664 | desc | höher als die ATK dieser Karte sind, kann | höher als die ATK dieser Karte ist, kann | agreement |
| 6688 | desc | als Normalbeschwörung beschwören ohne ein Monster | als Normalbeschwörung beschwören, ohne ein Monster | comma |
| 6722 | desc | zerstöre alle die Monster | zerstöre alle Monster | superfluous article |
| 6736 | desc | deiner Hand hingefügt wird | deiner Hand hinzugefügt wird | typo |
| 6758 | desc | seine ATK kleiner sind als die ATK des Angriffsziels | seine ATK kleiner ist als die ATK des Angriffsziels | agreement |
| 6815 | desc | auf den Friedhof geschickt wird während sie sich in deiner Zauber- & Fallenkartezone befindet | auf den Friedhof geschickt wird, während sie sich in deiner Zauber- & Fallenkartenzone befindet | comma and typo |
| 6410 | desc | ●Zauber : die | ●Zauber: die | space before the colon |
| 6410 | desc | ●Falle : wähle | ●Falle: wähle | space before the colon |
| 6410 | desc | ●Effektmonster : wähle | ●Effektmonster: wähle | space before the colon |

### Complete list of changed cards
**Complete original -> new comparison with the changed words highlighted: `docs/changes_de/cards_diff.md`** (all 258 entries). Raw data: `docs/changes_de/cards.csv`. First 40 rows:

| id | original name | field | original | new |
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

(... 218 more rows in the CSV)

## A3. Story dialogues

Archives: `script/stNN_<scene>_f.ehp`, every scene is a pair of members `...If.bin` (offsets in UTF-16 characters) and `...Lf.bin` (UTF-16LE strings terminated by NUL, some gzip-compressed). **1649 lines** changed (including those that **inherit** the correction because they have the same original text and the same Japanese as a corrected line).

Flow: line-by-line reading compared with English and Japanese -> touch-ups in `tools/data/dialogue_touchups_de.json` (`exact` and `parts`) -> `build_dialogues.py de` -> `dialogue_corrections_de.json` -> `apply_to_iso.py`. Automatic layout rules in `build_dialogues.py`: non-breaking space before `! ? : ;` also after `》` (rule `FR_PUNCT`), space after the placeholders, "Mode histoire" -> "Mode aventure". Box constraints: ~46 characters per line, max 3 lines (a placeholder counts ~6 characters): `apply_to_iso` reports the lines that might not fit.

### Re-reading touch-ups: `exact` (4) — whole original sentence -> new sentence
| original | new |
|---|---|
| Hier, du kannst den hier nehmen! | Hier, nimm dieses Dienstmädchen-Outfit! |
| Warum bist du hier | Warum bist du hier? |
| Tag-Duelle erfordern noch⏎mehr Strategie | Tag-Duelle erfordern noch⏎mehr Strategie. |
| OK!⏎Los geht's | OK!⏎Los geht's! |

### Re-reading touch-ups: `parts` (331) — text replacements applied to every line (in order)
| old | new |
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

### Complete list of lines
**Complete original -> new comparison (with English and Japanese): `docs/changes_de/dialogues_diff.md`** (all 1649 lines). Raw data: `docs/changes_de/dialogues.csv`. First 30:

| id | original | new | English |
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

(... 1619 more rows in the CSV)

## A4. Duelist sentences in duels

Tables `chr_wordstbl_f.bin` and `02chr_wordstbl_...` inside ~72 `duel/cutin_*.ehp` archives (and `zakov*`). The unique sentences are ~1,800: all re-read. **40 sentences changed** (66 entries). Data: `exact` (3) and `parts` (38) in `duel_line_corrections_de.json`. The `*-ptrs.txt` files of the character archives contain absolute offsets: if a table grows they must be recomputed (`remap_pointers`), otherwise the duel crashes.

Comparison with highlighted words: `docs/changes_de/duel_lines_diff.md`.

| original | new | entries | archive examples |
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

## A5. Long and short interface strings

Tables `strTbl*`, `help_strtbl_*`, `ddstrtbl_*`, `field_strtbl*` (format `(n, 12, 12+4n)` + offsets + UTF-16) in 55 archives (the same table is copied into several archives, e.g. `field/always_*_fra.ehp` x6). **581 unique strings changed**. Rules: `tools/corrections/string_rules_de.py` — **491 `STRINGS` entries** (archive, member, 0-based index, [(old, new)], reason), **37 `GLOBALS`** (regex/callable, applied after the STRINGS) on **33 tables** (`TABLES`); plus 0 targeted corrections in `tools/data/ui_texts.json` (in-place writes, text shorter than or equal to the original).

### By member (unique strings changed)
| member | strings |
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

### Global rules (all)
| pattern | replacement | reason |
|---|---|---|
| Seitendeck | Side Deck | a single spelling (Side Deck in the rest of the game) |
| \b([Tt]ut mir) Leid\b | \1 leid | reformed spelling |
| \bspielzug | Spielzug | capital letter |
| \$C0\$(?=[ \n.,!?]) | $C0 | stray $ after the color code |
| Monster-kartenzone | Monsterkartenzone | leftover hyphenation hyphen |
| (Fallen\|Fallenkarten)- (karten\|zone) | \1\2 | space after a hyphenation hyphen |
| Geg-ner | Gegner | leftover hyphenation hyphen |
| Ausrüstungs-zauberkarten | Ausrüstungszauberkarten | leftover hyphenation hyphen |
| Karten-effekte | Karteneffekte | leftover hyphenation hyphen |
| Aktivier-ung | Aktivierung | leftover hyphenation hyphen |
| gleich-zeitig | gleichzeitig | leftover hyphenation hyphen |
| (\$CA[\d.]+)\$(?=[ \n.,!?]) | \1$C0 | incomplete closing color code |
| An-griffsabsicht | Angriffsabsicht | leftover hyphenation hyphen |
| (Angriffs\|Verteidigungs)-position | \1position | leftover hyphenation hyphen |
| gegner-isch | gegnerisch | leftover hyphenation hyphen |
| zer-stört | zerstört | leftover hyphenation hyphen |
| Restscha-den | Restschaden | leftover hyphenation hyphen |
| Angriffspo-sition\|An-griffsposition | Angriffsposition | leftover hyphenation hyphen |
| Ausnahme-fälle | Ausnahmefälle | leftover hyphenation hyphen |
| den-selben | denselben | leftover hyphenation hyphen |
| (?<=[a-zäöüßA-ZÄÖÜ\)“]) um (?=[^.,!?\n\r]{0,70}?\bzu\b) | , um  | comma before the infinitive clause with um ... zu |
| ([.!?“])  (?=[A-ZÄÖÜ]) | \1  | double space after the full stop |
| \bkennen zu lernen\b | kennenzulernen | reformed spelling |
| \bkennen lernen\b | kennenlernen | reformed spelling |
| \bkennen gelernt\b | kennengelernt | reformed spelling |
| Duell Akademie | Duellakademie | single spelling |
| „([^„“"\n\r]{1,60})" | „\1“ | straight closing quotation marks instead of “ |
| Zauber- Und  | Zauber- und  | capital letter |
| Algemeinen | Allgemeinen | typo |
| Vorraussetzung | Voraussetzung | typo |
| Konter-Fall | Konterfall | as in the cards |
| Deck Bearbeitungs | Deck-Bearbeitungs | hyphen |
| ([×△○□])–Taste | \1-Taste | hyphen |
| Story Modus | Story-Modus | hyphen |
| \bSlifer[- ]Red\b | Slifer Rot | leftover English (in the rest of the game: Slifer Rot / Ra Gelb / Obelisk Blau) |
| \bRa[- ]Yellow\b | Ra Gelb | leftover English |
| \bObelisk[- ]Blue\b | Obelisk Blau | leftover English |

### STRINGS entries (all): where and why
| archive | member | index | changes | reason |
|---|---|---|---|---|
| database/charalist.ehp | strTbl_g.bin | 12 | 5 replacement(s) | agreement, spelling |
| database/charalist.ehp | strTbl_g.bin | 13 | 1 replacement(s) | genitive of a name in -s, leftover English |
| database/charalist.ehp | strTbl_g.bin | 14 | 1 replacement(s) | space |
| database/charalist.ehp | strTbl_g.bin | 15 | 1 replacement(s) | case |
| database/charalist.ehp | strTbl_g.bin | 16 | 2 replacement(s) | missing full stop, typo |
| database/charalist.ehp | strTbl_g.bin | 17 | 2 replacement(s) | typo, case |
| database/charalist.ehp | strTbl_g.bin | 18 | 3 replacement(s) | capital letters, wrong verb (EN: He likes to eat vegetables) |
| database/charalist.ehp | strTbl_g.bin | 19 | 1 replacement(s) | typo |
| database/charalist.ehp | strTbl_g.bin | 20 | 3 replacement(s) | case, agreement, missing quotation marks |
| database/charalist.ehp | strTbl_g.bin | 21 | 1 replacement(s) | grammar |
| database/charalist.ehp | strTbl_g.bin | 22 | 2 replacement(s) | genitive of a name in -s |
| database/charalist.ehp | strTbl_g.bin | 24 | 2 replacement(s) | grammar |
| database/charalist.ehp | strTbl_g.bin | 25 | 1 replacement(s) | case |
| database/charalist.ehp | strTbl_g.bin | 28 | 1 replacement(s) | typo |
| database/charalist.ehp | strTbl_g.bin | 29 | 1 replacement(s) | agreement |
| database/charalist.ehp | strTbl_g.bin | 31 | 2 replacement(s) | agreement |
| database/charalist.ehp | strTbl_g.bin | 33 | 1 replacement(s) | name written two ways in the same text |
| database/charalist.ehp | strTbl_g.bin | 35 | 1 replacement(s) | capital letter |
| database/charalist.ehp | strTbl_g.bin | 37 | 2 replacement(s) | typo, grammar (EN: high school level Duel Academy) |
| database/charalist.ehp | strTbl_g.bin | 38 | 1 replacement(s) | doubled word |
| database/charalist.ehp | strTbl_g.bin | 40 | 1 replacement(s) | wrong comma |
| database/charalist.ehp | strTbl_g.bin | 41 | 3 replacement(s) | gender (EN: A card spirit), dass |
| database/charalist.ehp | strTbl_g.bin | 43 | 2 replacement(s) | capital letter, grammar |
| database/charalist.ehp | strTbl_g.bin | 44 | 1 replacement(s) | grammar |
| database/charalist.ehp | strTbl_g.bin | 45 | 1 replacement(s) | typo, article |
| database/charalist.ehp | strTbl_g.bin | 49 | 1 replacement(s) | agreement |
| database/charalist.ehp | strTbl_g.bin | 50 | 1 replacement(s) | term as in the cards (Grabwächters Attentäter) |
| database/charalist.ehp | strTbl_g.bin | 52 | 1 replacement(s) | genitive without apostrophe |
| database/charalist.ehp | strTbl_g.bin | 65 | 1 replacement(s) | as in the card types (permanent) |
| database/charalist.ehp | strTbl_g.bin | 69 | 1 replacement(s) | typo, as in the card types (permanent) |
| database/charalist.ehp | strTbl_g.bin | 70 | 1 replacement(s) | as in the cards (Konterfalle) |
| database/duelrecord.ehp | strTbl_g.bin | 5 | 1 replacement(s) | leftover English |
| duel/result/result_g.ehp | strTbl.bin | 5 | 1 replacement(s) | leftover English |
| database/duelrecord.ehp | strTbl_g.bin | 6 | 1 replacement(s) | leftover English |
| duel/result/result_g.ehp | strTbl.bin | 6 | 1 replacement(s) | leftover English |
| database/duelrecord.ehp | strTbl_g.bin | 9 | 1 replacement(s) | leftover English |
| duel/result/result_g.ehp | strTbl.bin | 9 | 1 replacement(s) | leftover English |
| database/duelrecord.ehp | strTbl_g.bin | 10 | 1 replacement(s) | hyphen |
| duel/result/result_g.ehp | strTbl.bin | 10 | 1 replacement(s) | hyphen |
| database/duelrecord.ehp | strTbl_g.bin | 16 | 1 replacement(s) | capital letter |
| duel/result/result_g.ehp | strTbl.bin | 16 | 1 replacement(s) | capital letter |
| database/duelrecord.ehp | strTbl_g.bin | 17 | 1 replacement(s) | capital letter |
| duel/result/result_g.ehp | strTbl.bin | 17 | 1 replacement(s) | capital letter |
| database/duelrecord.ehp | strTbl_g.bin | 30 | 1 replacement(s) | gender (die ATK), hyphen |
| duel/result/result_g.ehp | strTbl.bin | 30 | 1 replacement(s) | gender (die ATK), hyphen |
| database/duelrecord.ehp | strTbl_g.bin | 32 | 1 replacement(s) | comma |
| duel/result/result_g.ehp | strTbl.bin | 32 | 1 replacement(s) | comma |
| database/duelrecord.ehp | strTbl_g.bin | 34 | 1 replacement(s) | comma |
| duel/result/result_g.ehp | strTbl.bin | 34 | 1 replacement(s) | comma |
| database/duelrecord.ehp | strTbl_g.bin | 35 | 1 replacement(s) | comma |
| duel/result/result_g.ehp | strTbl.bin | 35 | 1 replacement(s) | comma |
| database/duelrecord.ehp | strTbl_g.bin | 36 | 1 replacement(s) | comma |
| duel/result/result_g.ehp | strTbl.bin | 36 | 1 replacement(s) | comma |
| database/duelrecord.ehp | strTbl_g.bin | 37 | 1 replacement(s) | agreement |
| duel/result/result_g.ehp | strTbl.bin | 37 | 1 replacement(s) | agreement |
| database/duelrecord.ehp | strTbl_g.bin | 38 | 1 replacement(s) | agreement |
| duel/result/result_g.ehp | strTbl.bin | 38 | 1 replacement(s) | agreement |
| database/duelrecord.ehp | strTbl_g.bin | 49 | 1 replacement(s) | hyphen |
| duel/result/result_g.ehp | strTbl.bin | 49 | 1 replacement(s) | hyphen |
| database/duelrecord.ehp | strTbl_g.bin | 63 | 1 replacement(s) | hyphen |
| duel/result/result_g.ehp | strTbl.bin | 63 | 1 replacement(s) | hyphen |
| database/duelrecord.ehp | strTbl_g.bin | 64 | 1 replacement(s) | thousands separator as in the other entries |
| duel/result/result_g.ehp | strTbl.bin | 64 | 1 replacement(s) | thousands separator as in the other entries |
| database/duelrecord.ehp | strTbl_g.bin | 67 | 1 replacement(s) | as in the previous entry |
| duel/result/result_g.ehp | strTbl.bin | 67 | 1 replacement(s) | as in the previous entry |
| database/duelrecord.ehp | strTbl_g.bin | 70 | 1 replacement(s) | hyphens (as in Keine-Karten-mehr-Bonus) |
| duel/result/result_g.ehp | strTbl.bin | 70 | 1 replacement(s) | hyphens (as in Keine-Karten-mehr-Bonus) |
| database/duelrecord.ehp | strTbl_g.bin | 71 | 1 replacement(s) | hyphens |
| duel/result/result_g.ehp | strTbl.bin | 71 | 1 replacement(s) | hyphens |
| database/duelrecord.ehp | strTbl_g.bin | 87 | 1 replacement(s) | compound |
| duel/result/result_g.ehp | strTbl.bin | 87 | 1 replacement(s) | compound |
| database/duelrecord.ehp | strTbl_g.bin | 88 | 1 replacement(s) | compound |
| duel/result/result_g.ehp | strTbl.bin | 88 | 1 replacement(s) | compound |
| database/duelrecord.ehp | strTbl_g.bin | 126 | 1 replacement(s) | case, capital letter |
| duel/result/result_g.ehp | strTbl.bin | 126 | 1 replacement(s) | case, capital letter |
| database/duelrecord.ehp | strTbl_g.bin | 127 | 1 replacement(s) | case |
| duel/result/result_g.ehp | strTbl.bin | 127 | 1 replacement(s) | case |
| database/duelrecord.ehp | strTbl_g.bin | 140 | 1 replacement(s) | typos, thousands separator, Toon-Monster as in the cards |
| duel/result/result_g.ehp | strTbl.bin | 140 | 1 replacement(s) | typos, thousands separator, Toon-Monster as in the cards |
| database/duelrecord.ehp | strTbl_g.bin | 151 | 1 replacement(s) | typo |
| duel/result/result_g.ehp | strTbl.bin | 151 | 1 replacement(s) | typo |
| database/duelrecord.ehp | strTbl_g.bin | 152 | 1 replacement(s) | comma |
| duel/result/result_g.ehp | strTbl.bin | 152 | 1 replacement(s) | comma |
| database/duelrecord.ehp | strTbl_g.bin | 153 | 1 replacement(s) | thousands separator |
| duel/result/result_g.ehp | strTbl.bin | 153 | 1 replacement(s) | thousands separator |
| database/duelrecord.ehp | strTbl_g.bin | 154 | 1 replacement(s) | thousands separator |
| duel/result/result_g.ehp | strTbl.bin | 154 | 1 replacement(s) | thousands separator |
| database/duelrecord.ehp | strTbl_g.bin | 163 | 1 replacement(s) | case, capital letter |
| duel/result/result_g.ehp | strTbl.bin | 163 | 1 replacement(s) | case, capital letter |
| database/duelrecord.ehp | strTbl_g.bin | 182 | 1 replacement(s) | wrong translation (JA: 全レベルのモンスターが入った, EN: monsters of every Level) |
| duel/result/result_g.ehp | strTbl.bin | 182 | 1 replacement(s) | wrong translation (JA: 全レベルのモンスターが入った, EN: monsters of every Level) |
| database/duelrecord.ehp | strTbl_g.bin | 213 | 1 replacement(s) | as in the card names |
| duel/result/result_g.ehp | strTbl.bin | 213 | 1 replacement(s) | as in the card names |
| database/duelrecord.ehp | strTbl_g.bin | 215 | 1 replacement(s) | as in the cards |
| duel/result/result_g.ehp | strTbl.bin | 215 | 1 replacement(s) | as in the cards |
| database/duelrecord.ehp | strTbl_g.bin | 224 | 1 replacement(s) | comma |
| duel/result/result_g.ehp | strTbl.bin | 224 | 1 replacement(s) | comma |
| database/duelrecord.ehp | strTbl_g.bin | 225 | 1 replacement(s) | comma |
| duel/result/result_g.ehp | strTbl.bin | 225 | 1 replacement(s) | comma |
| database/duelrecord.ehp | strTbl_g.bin | 226 | 1 replacement(s) | comma |
| duel/result/result_g.ehp | strTbl.bin | 226 | 1 replacement(s) | comma |
| database/duelrecord.ehp | strTbl_g.bin | 229 | 1 replacement(s) | as in the dialogues |
| duel/result/result_g.ehp | strTbl.bin | 229 | 1 replacement(s) | as in the dialogues |
| database/duelrecord.ehp | strTbl_g.bin | 238 | 1 replacement(s) | comma |
| duel/result/result_g.ehp | strTbl.bin | 238 | 1 replacement(s) | comma |
| database/duelrecord.ehp | strTbl_g.bin | 240 | 1 replacement(s) | hyphen |
| duel/result/result_g.ehp | strTbl.bin | 240 | 1 replacement(s) | hyphen |
| database/duelrecord.ehp | strTbl_g.bin | 242 | 1 replacement(s) | German spelling |
| duel/result/result_g.ehp | strTbl.bin | 242 | 1 replacement(s) | German spelling |
| database/duelrecord.ehp | strTbl_g.bin | 244 | 1 replacement(s) | leftover English |
| duel/result/result_g.ehp | strTbl.bin | 244 | 1 replacement(s) | leftover English |
| database/duelrecord.ehp | strTbl_g.bin | 245 | 1 replacement(s) | leftover English |
| duel/result/result_g.ehp | strTbl.bin | 245 | 1 replacement(s) | leftover English |
| database/duelrecord.ehp | strTbl_g.bin | 248 | 1 replacement(s) | leftover English |
| duel/result/result_g.ehp | strTbl.bin | 248 | 1 replacement(s) | leftover English |
| database/duelrecord.ehp | strTbl_g.bin | 249 | 1 replacement(s) | leftover English |
| duel/result/result_g.ehp | strTbl.bin | 249 | 1 replacement(s) | leftover English |
| database/duelrecord.ehp | strTbl_g.bin | 250 | 1 replacement(s) | space |
| duel/result/result_g.ehp | strTbl.bin | 250 | 1 replacement(s) | space |
| database/duelrecord.ehp | strTbl_g.bin | 260 | 1 replacement(s) | missing sentence (EN: The duel will now end.) |
| duel/result/result_g.ehp | strTbl.bin | 260 | 1 replacement(s) | missing sentence (EN: The duel will now end.) |
| database/duelrecord.ehp | strTbl_g.bin | 268 | 1 replacement(s) | term (EN: duel) |
| duel/result/result_g.ehp | strTbl.bin | 268 | 1 replacement(s) | term (EN: duel) |
| database/duelrecord.ehp | strTbl_g.bin | 269 | 1 replacement(s) | German spelling |
| duel/result/result_g.ehp | strTbl.bin | 269 | 1 replacement(s) | German spelling |
| database/limitlist.ehp | strTbl_g.bin | 1 | 1 replacement(s) | lowercase adjectives |
| database/limitlist.ehp | strTbl_g.bin | 2 | 1 replacement(s) | lowercase adjectives |
| database/limitlist.ehp | strTbl_g.bin | 4 | 1 replacement(s) | English abbreviation (Ltd.), menu entry |
| database/tutoriallist.ehp | strTbl_g.bin | 13 | 1 replacement(s) | mixed construction (EN: Changing Battle Positions) |
| deck/all_g.ehp | strTbl.bin | 31 | 1 replacement(s) | hyphen |
| deck/all_g.ehp | strTbl.bin | 41 | 1 replacement(s) | adverb |
| deck/all_g.ehp | strTbl.bin | 83 | 1 replacement(s) | double space |
| deck/all_g.ehp | strTbl.bin | 112 | 1 replacement(s) | compound |
| deck/all_g.ehp | strTbl.bin | 73 | 1 replacement(s) | incomplete (JA: デッキを元の状態に戻す) |
| deck/all_g.ehp | strTbl.bin | 132 | 1 replacement(s) | typo |
| deck/all_g.ehp | strTbl.bin | 134 | 1 replacement(s) | extra word |
| deck/all_g.ehp | strTbl.bin | 172 | 1 replacement(s) | mixed construction (EN: Changing Battle Positions) |
| deck/all_g.ehp | help_strtbl_contents.bin | 4 | 1 replacement(s) | hyphen |
| deck/all_g.ehp | help_strtbl_contents.bin | 23 | 1 replacement(s) | hyphen |
| deck/all_g.ehp | help_strtbl_contents.bin | 29 | 1 replacement(s) | compound |
| deck/all_g.ehp | help_strtbl_contents.bin | 37 | 1 replacement(s) | compound (as Deckrezepte) |
| deck/all_g.ehp | help_strtbl_contents.bin | 41 | 1 replacement(s) | incomplete (JA: デッキを元の状態に戻す) |
| deck/all_g.ehp | help_strtbl_contents.bin | 53 | 1 replacement(s) | construction |
| deck/all_g.ehp | help_strtbl_contents.bin | 70 | 1 replacement(s) | plural |
| deck/all_g.ehp | help_strtbl_contents.bin | 84 | 1 replacement(s) | meaningless (JA: カードをめくる; same entry as 166) |
| deck/all_g.ehp | help_strtbl_contents.bin | 93 | 1 replacement(s) | capital letter, full stop |
| deck/all_g.ehp | help_strtbl_contents.bin | 94 | 1 replacement(s) | capital letter, full stop |
| deck/all_g.ehp | help_strtbl_contents.bin | 97 | 2 replacement(s) | missing pronoun (EN: you will draw), typo, comma |
| deck/all_g.ehp | help_strtbl_contents.bin | 99 | 4 replacement(s) | agreement, case |
| deck/all_g.ehp | help_strtbl_contents.bin | 106 | 1 replacement(s) | hyphen |
| deck/all_g.ehp | help_strtbl_contents.bin | 107 | 1 replacement(s) | plural |
| deck/all_g.ehp | help_strtbl_contents.bin | 109 | 1 replacement(s) | nachdem, missing article |
| deck/all_g.ehp | help_strtbl_contents.bin | 112 | 1 replacement(s) | agreement |
| deck/all_g.ehp | help_strtbl_contents.bin | 123 | 1 replacement(s) | comma, case |
| deck/all_g.ehp | help_strtbl_contents.bin | 126 | 1 replacement(s) | space |
| deck/all_g.ehp | help_strtbl_contents.bin | 129 | 3 replacement(s) | plural, typo, je ... desto |
| deck/all_g.ehp | help_strtbl_contents.bin | 133 | 1 replacement(s) | das/dass |
| deck/all_g.ehp | help_strtbl_contents.bin | 135 | 3 replacement(s) | plural, hyphen, case |
| deck/all_g.ehp | help_strtbl_contents.bin | 136 | 1 replacement(s) | wrong sentence (subject) |
| deck/all_g.ehp | help_strtbl_contents.bin | 137 | 3 replacement(s) | capital letter, extra 'solange' |
| deck/all_g.ehp | help_strtbl_contents.bin | 141 | 2 replacement(s) | article, verb (EN: activated) |
| deck/all_g.ehp | help_strtbl_contents.bin | 142 | 1 replacement(s) | comma |
| deck/all_g.ehp | help_strtbl_contents.bin | 144 | 1 replacement(s) | comma |
| deck/all_g.ehp | help_strtbl_contents.bin | 147 | 1 replacement(s) | missing verb |
| deck/all_g.ehp | help_strtbl_contents.bin | 148 | 1 replacement(s) | nachdem |
| deck/all_g.ehp | help_strtbl_contents.bin | 149 | 2 replacement(s) | missing pronoun, relative |
| deck/all_g.ehp | help_strtbl_contents.bin | 150 | 3 replacement(s) | agreement, case |
| deck/all_g.ehp | help_strtbl_contents.bin | 153 | 1 replacement(s) | nachdem |
| deck/all_g.ehp | help_strtbl_contents.bin | 154 | 1 replacement(s) | comma, full stop |
| deck/all_g.ehp | help_strtbl_contents.bin | 156 | 3 replacement(s) | ungrammatical sentence, typos |
| deck/all_g.ehp | help_strtbl_contents.bin | 157 | 1 replacement(s) | missing verb |
| deck/all_g.ehp | help_strtbl_contents.bin | 158 | 1 replacement(s) | wrong sentence |
| deck/all_g.ehp | help_strtbl_contents.bin | 159 | 1 replacement(s) | typo |
| deck/all_g.ehp | help_strtbl_contents.bin | 161 | 1 replacement(s) | capital letter |
| deck/all_g.ehp | help_strtbl_contents.bin | 162 | 3 replacement(s) | doubled word, case, comma |
| deck/all_g.ehp | help_strtbl_contents.bin | 163 | 2 replacement(s) | typo, construction |
| deck/all_g.ehp | help_strtbl_contents.bin | 165 | 2 replacement(s) | agreement |
| deck/all_g.ehp | help_strtbl_contents.bin | 166 | 1 replacement(s) | plural, hyphen |
| deck/all_g.ehp | help_strtbl_contents.bin | 167 | 1 replacement(s) | typo |
| deck/all_g.ehp | help_strtbl_contents.bin | 171 | 1 replacement(s) | plural |
| deck/all_g.ehp | help_strtbl_contents.bin | 172 | 2 replacement(s) | case, typo |
| deck/all_g.ehp | help_strtbl_contents.bin | 173 | 1 replacement(s) | pronoun |
| deck/tutorial.ehp | strTbl_g.bin | 9 | 1 replacement(s) | comma |
| deck/tutorial.ehp | strTbl_g.bin | 16 | 1 replacement(s) | comma, hyphen |
| deck/tutorial.ehp | strTbl_g.bin | 18 | 1 replacement(s) | ungrammatical sentence |
| deck/tutorial.ehp | strTbl_g.bin | 20 | 1 replacement(s) | comma |
| deck/tutorial.ehp | strTbl_g.bin | 21 | 1 replacement(s) | comma |
| deck/tutorial.ehp | strTbl_g.bin | 26 | 1 replacement(s) | question mark |
| deck/tutorial.ehp | strTbl_g.bin | 27 | 1 replacement(s) | case, verb |
| deck/tutorial.ehp | strTbl_g.bin | 34 | 1 replacement(s) | missing word |
| deck/tutorial.ehp | strTbl_g.bin | 39 | 1 replacement(s) | capital letters |
| deck/tutorial.ehp | strTbl_g.bin | 55 | 1 replacement(s) | plural |
| deck/tutorial.ehp | strTbl_g.bin | 58 | 1 replacement(s) | question mark |
| deck/tutorial.ehp | strTbl_g.bin | 66 | 1 replacement(s) | conjunction |
| deck/tutorial.ehp | strTbl_g.bin | 76 | 1 replacement(s) | typo |
| deck/tutorial.ehp | strTbl_g.bin | 81 | 1 replacement(s) | incomplete sentence |
| deck/tutorial.ehp | strTbl_g.bin | 82 | 1 replacement(s) | capital letters |
| deck/tutorial.ehp | strTbl_g.bin | 87 | 1 replacement(s) | doubled word |
| deck/tutorial.ehp | strTbl_g.bin | 91 | 1 replacement(s) | case |
| deck/tutorial.ehp | strTbl_g.bin | 93 | 1 replacement(s) | gender |
| deck/tutorial.ehp | strTbl_g.bin | 94 | 1 replacement(s) | case |
| deck/tutorial.ehp | strTbl_g.bin | 97 | 1 replacement(s) | incomplete sentence |
| deck/tutorial.ehp | strTbl_g.bin | 98 | 1 replacement(s) | missing word |
| deck/tutorial.ehp | strTbl_g.bin | 60 | 1 replacement(s) | comma / construction |
| deck/tutorial.ehp | strTbl_g.bin | 113 | 1 replacement(s) | gender (die ATK) |
| deck/tutorial.ehp | strTbl_g.bin | 116 | 1 replacement(s) | agreement |
| deck/tutorial.ehp | strTbl_g.bin | 117 | 2 replacement(s) | agreement |
| deck/tutorial.ehp | strTbl_g.bin | 125 | 1 replacement(s) | register |
| deck/tutorial.ehp | strTbl_g.bin | 133 | 1 replacement(s) | plural |
| deck/tutorial.ehp | strTbl_g.bin | 137 | 1 replacement(s) | register |
| deck/tutorial.ehp | strTbl_g.bin | 138 | 1 replacement(s) | comma |
| deck/tutorial.ehp | strTbl_g.bin | 147 | 1 replacement(s) | typo |
| deck/tutorial.ehp | strTbl_g.bin | 150 | 1 replacement(s) | commas |
| deck/tutorial.ehp | strTbl_g.bin | 154 | 1 replacement(s) | comma |
| deck/tutorial.ehp | strTbl_g.bin | 155 | 1 replacement(s) | comma / construction |
| deck/tutorial.ehp | strTbl_g.bin | 156 | 1 replacement(s) | spelling |
| deck/tutorial.ehp | strTbl_g.bin | 157 | 1 replacement(s) | comma |
| deck/tutorial.ehp | strTbl_g.bin | 159 | 1 replacement(s) | commas |
| deck/tutorial.ehp | strTbl_g.bin | 161 | 1 replacement(s) | comma |
| deck/tutorial.ehp | strTbl_g.bin | 163 | 1 replacement(s) | missing pronoun |
| deck/tutorial.ehp | strTbl_g.bin | 165 | 1 replacement(s) | comma |
| deck/tutorial.ehp | strTbl_g.bin | 169 | 1 replacement(s) | comma |
| deck/tutorial.ehp | strTbl_g.bin | 179 | 1 replacement(s) | ungrammatical sentence |
| deck/tutorial.ehp | strTbl_g.bin | 180 | 1 replacement(s) | plural |
| deck/tutorial.ehp | strTbl_g.bin | 186 | 1 replacement(s) | capital letter, comma |
| deck/tutorial.ehp | strTbl_g.bin | 189 | 1 replacement(s) | typo |
| deck/tutorial.ehp | strTbl_g.bin | 190 | 1 replacement(s) | comma, hyphen |
| deck/tutorial.ehp | strTbl_g.bin | 198 | 1 replacement(s) | spelling |
| deck/tutorial.ehp | strTbl_g.bin | 203 | 1 replacement(s) | commas |
| deck/tutorial.ehp | strTbl_g.bin | 209 | 1 replacement(s) | comma |
| deck/tutorial.ehp | strTbl_g.bin | 210 | 1 replacement(s) | wrong menu entry (EN: Run), comma |
| deck/tutorial.ehp | strTbl_g.bin | 215 | 1 replacement(s) | plural |
| deck/tutorial.ehp | strTbl_g.bin | 216 | 1 replacement(s) | grammar |
| deck/tutorial.ehp | strTbl_g.bin | 218 | 1 replacement(s) | doubled word |
| deck/tutorial.ehp | strTbl_g.bin | 220 | 1 replacement(s) | comma |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 23 | 1 replacement(s) | capital letter/hyphen |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 24 | 1 replacement(s) | capital letter/hyphen |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 48 | 1 replacement(s) | grammar (EN: Press the □ button to go back.) |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 60 | 1 replacement(s) | capital letter |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 63 | 1 replacement(s) | cut word |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 66 | 1 replacement(s) | French leftover |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 68 | 1 replacement(s) | plural (LP) |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 75 | 1 replacement(s) | capital letter |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 76 | 1 replacement(s) | comma |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 80 | 1 replacement(s) | agreement (LP plural) |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 87 | 1 replacement(s) | capital letter |
| duel/basic_*g.ehp | ddstrtbl_g.bin | 88 | 1 replacement(s) | comma |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 59 | 1 replacement(s) | spelling |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 66 | 1 replacement(s) | compound |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 115 | 2 replacement(s) | typo, capital letter |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 118 | 1 replacement(s) | comma |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 119 | 3 replacement(s) | preposition, comma, relative |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 120 | 1 replacement(s) | typo |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 136 | 1 replacement(s) | quotation marks and comma |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 150 | 3 replacement(s) | grammar, Duell (EN: loser of the previous Duel) |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 154 | 2 replacement(s) | agreement |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 155 | 1 replacement(s) | comma |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 157 | 1 replacement(s) | das/dass |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 158 | 1 replacement(s) | article, capital letter |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 159 | 3 replacement(s) | typos |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 160 | 1 replacement(s) | grammar |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 161 | 1 replacement(s) | agreement |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 163 | 3 replacement(s) | typo, comma, plural |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 167 | 1 replacement(s) | grammar |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 168 | 3 replacement(s) | commas, missing verb |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 169 | 2 replacement(s) | typo, case |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 171 | 2 replacement(s) | typo, comma, preposition |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 172 | 2 replacement(s) | comma, doubled word |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 173 | 1 replacement(s) | capital letter |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 174 | 1 replacement(s) | grammar |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 175 | 1 replacement(s) | missing closing parenthesis |
| field/always_*_ger.ehp | field_strtbl.bin | 14 | 1 replacement(s) | typo, pronoun |
| field/always_*_ger.ehp | field_strtbl.bin | 21 | 1 replacement(s) | menu entry in lowercase (EN: Give) |
| field/always_*_ger.ehp | field_strtbl.bin | 22 | 1 replacement(s) | menu entry (EN: Eat) |
| field/always_*_ger.ehp | field_strtbl.bin | 47 | 1 replacement(s) | lowercase adjectives |
| field/always_*_ger.ehp | field_strtbl.bin | 64 | 1 replacement(s) | hyphen |
| field/always_*_ger.ehp | field_strtbl.bin | 67 | 1 replacement(s) | leftover English |
| field/always_*_ger.ehp | field_strtbl.bin | 100 | 1 replacement(s) | comma |
| field/always_*_ger.ehp | field_strtbl_item.bin | 70 | 1 replacement(s) | hyphen (as in the dialogues) |
| field/always_*_ger.ehp | field_strtbl_item.bin | 75 | 1 replacement(s) | hyphen (as in the dialogues) |
| field/always_*_ger.ehp | field_strtbl_item.bin | 88 | 1 replacement(s) | typo, agreement (as in the dialogues) |
| field/always_*_ger.ehp | field_strtbl_item.bin | 94 | 1 replacement(s) | genitive without apostrophe (as in the dialogues) |
| field/always_*_ger.ehp | field_strtbl_item.bin | 98 | 1 replacement(s) | linking -s- |
| field/always_*_ger.ehp | field_strtbl_item.bin | 105 | 1 replacement(s) | reformed spelling |
| field/always_*_ger.ehp | field_strtbl_item.bin | 107 | 1 replacement(s) | comma |
| field/always_*_ger.ehp | field_strtbl_item.bin | 156 | 1 replacement(s) | case |
| field/always_*_ger.ehp | field_strtbl_item.bin | 160 | 1 replacement(s) | compound |
| field/always_*_ger.ehp | field_strtbl_item.bin | 164 | 2 replacement(s) | capital letter, full stop |
| field/always_*_ger.ehp | field_strtbl_item.bin | 168 | 1 replacement(s) | case |
| field/always_*_ger.ehp | field_strtbl_item.bin | 169 | 1 replacement(s) | case, sentence |
| field/always_*_ger.ehp | field_strtbl_item.bin | 170 | 2 replacement(s) | case, hyphen |
| field/always_*_ger.ehp | field_strtbl_item.bin | 172 | 1 replacement(s) | typo |
| field/always_*_ger.ehp | field_strtbl_item.bin | 177 | 1 replacement(s) | case, comma |
| field/always_*_ger.ehp | field_strtbl_item.bin | 182 | 1 replacement(s) | case |
| field/always_*_ger.ehp | field_strtbl_item.bin | 189 | 1 replacement(s) | grammar |
| field/always_*_ger.ehp | field_strtbl_item.bin | 193 | 1 replacement(s) | typo, as in the dialogues |
| field/always_*_ger.ehp | field_strtbl_item.bin | 194 | 1 replacement(s) | plural |
| field/always_*_ger.ehp | field_strtbl_item.bin | 200 | 1 replacement(s) | agreement |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 1 | 1 replacement(s) | hyphens |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 19 | 1 replacement(s) | case; without article like the other places (the dialogue says 'Verlasse das 《M006_2》') |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 20 | 1 replacement(s) | missing translation (EN: Library) |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 21 | 1 replacement(s) | missing translation (EN: Roof) |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 25 | 1 replacement(s) | missing translation (EN: Ruins) |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 22 | 1 replacement(s) | leftover English |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 24 | 1 replacement(s) | wrong translation (EN: Abandoned Dorm) |
| field/always_*_ger.ehp | field_strtbl_mapname.bin | 30 | 1 replacement(s) | leftover English (as in the dialogues: Spezial-Finalarena) |
| labo/conv_machine.ehp | strTbl_g.bin | 2 | 1 replacement(s) | capital letter |
| labo/password.ehp | strTbl_g.bin | 1 | 1 replacement(s) | comma |
| labo/password.ehp | strTbl_g.bin | 10 | 1 replacement(s) | compound |
| labo/password.ehp | strTbl_g.bin | 11 | 1 replacement(s) | article |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 4 | 1 replacement(s) | number (EN: Opened File) |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 5 | 1 replacement(s) | typo |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 19 | 1 replacement(s) | capital letter |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 71 | 1 replacement(s) | space before the line break |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 72 | 1 replacement(s) | space before the line break |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 73 | 2 replacement(s) | grammar, comma |
| title_menu/title_menu_?.ehp | title_msg_g.bin | 74 | 1 replacement(s) | typo |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 34 | 1 replacement(s) | grammar |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 36 | 1 replacement(s) | space |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 40 | 1 replacement(s) | grammar |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 41 | 1 replacement(s) | grammar |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 45 | 1 replacement(s) | comma, article |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 46 | 1 replacement(s) | typo, space |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 66 | 1 replacement(s) | article, comma |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 71 | 1 replacement(s) | grammar |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 72 | 1 replacement(s) | typo |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 115 | 1 replacement(s) | case |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 117 | 1 replacement(s) | comma |
| title_menu/title_menu_?.ehp | tushin_msg_g.bin | 121 | 2 replacement(s) | mixed Sie/du, wrong translation (EN: main menu) |
| field/always_*_ger.ehp | event_name.bin | 1 | 1 replacement(s) | grammar |
| field/always_*_ger.ehp | event_name.bin | 2 | 1 replacement(s) | article |
| field/always_*_ger.ehp | event_name.bin | 3 | 1 replacement(s) | article |
| field/always_*_ger.ehp | event_name.bin | 7 | 1 replacement(s) | article |
| field/always_*_ger.ehp | event_name.bin | 4 | 1 replacement(s) | grammar |
| field/always_*_ger.ehp | event_name.bin | 5 | 1 replacement(s) | leftover English |
| field/always_*_ger.ehp | event_name.bin | 11 | 1 replacement(s) | hyphens |
| duel/basic_*.ehp | option_msg_g.bin | 19 | 1 replacement(s) | comma |
| duel/basic_*.ehp | option_msg_g.bin | 24 | 1 replacement(s) | comma |
| duel/basic_*.ehp | option_msg_g.bin | 26 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 1 | 1 replacement(s) | typo |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 9 | 1 replacement(s) | plural |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 19 | 1 replacement(s) | capital letter |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 24 | 1 replacement(s) | capital letter, gender |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 35 | 1 replacement(s) | capital letter, gender |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 37 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 40 | 1 replacement(s) | capital letter, gender |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 45 | 1 replacement(s) | capital letter, gender |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 56 | 1 replacement(s) | space, gender |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 57 | 2 replacement(s) | capital letter, gender, conjugation |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 59 | 2 replacement(s) | typo, gender |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 60 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 61 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 71 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 87 | 2 replacement(s) | space, typo |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 104 | 1 replacement(s) | consistent thousands separator |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 106 | 1 replacement(s) | compound |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 108 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 112 | 1 replacement(s) | punctuation |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 121 | 1 replacement(s) | doubled word |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 128 | 1 replacement(s) | space/comma |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 134 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 135 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 137 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 01_message_res.bin | 140 | 1 replacement(s) | missing word |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 19 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 21 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 15 | 1 replacement(s) | doubled word |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 29 | 1 replacement(s) | genitive |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 35 | 1 replacement(s) | consistent thousands separator |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 39 | 1 replacement(s) | leftover hyphen |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 55 | 1 replacement(s) | typo |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 60 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 61 | 1 replacement(s) | missing article |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 67 | 1 replacement(s) | doubled word |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 69 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 70 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 74 | 1 replacement(s) | space |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 82 | 1 replacement(s) | ellipsis dots |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 87 | 1 replacement(s) | participle |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 88 | 2 replacement(s) | wrong translation, missing negation |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 89 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 92 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 02_message_res.bin | 101 | 4 replacement(s) | wrong translation (EN: Remember), gender, case |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 7 | 1 replacement(s) | hyphen |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 8 | 1 replacement(s) | hyphen, plural |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 10 | 1 replacement(s) | plural |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 23 | 1 replacement(s) | wrong translation (EN: DEF) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 47 | 1 replacement(s) | case |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 42 | 1 replacement(s) | truncated sentence |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 54 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 55 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 56 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 59 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 61 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 69 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 74 | 1 replacement(s) | capital letter |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 76 | 1 replacement(s) | case |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 102 | 1 replacement(s) | wrong translation (EN: set or use) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 103 | 1 replacement(s) | capital letter |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 115 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 121 | 1 replacement(s) | doubled word |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 122 | 1 replacement(s) | grammar, translation (EN: face-down) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 127 | 1 replacement(s) | conjugation |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 131 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 132 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 133 | 2 replacement(s) | swapped buttons (EN: ○ opens, × confirms) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 134 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 137 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 140 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 141 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 144 | 1 replacement(s) | imperative |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 148 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 149 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 150 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 151 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 152 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 153 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 154 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 161 | 1 replacement(s) | number |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 164 | 1 replacement(s) | conjugation |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 169 | 1 replacement(s) | conjugation |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 172 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 176 | 1 replacement(s) | name different from English (EN: Syrus) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 178 | 1 replacement(s) | compound |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 186 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 187 | 3 replacement(s) | gender, hyphenation, truncated sentence |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 188 | 2 replacement(s) | wrong negation (EN: can be used in the following cases) |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 189 | 1 replacement(s) | hyphenation |
| tutorial/tutorial_g.ehp | 03_message_res.bin | 192 | 1 replacement(s) | hyphenation |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 15 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 25 | 1 replacement(s) | wrong color code |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 27 | 1 replacement(s) | hyphenation |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 30 | 1 replacement(s) | typo |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 33 | 2 replacement(s) | gender, grammar |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 35 | 2 replacement(s) | grammar, gender |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 36 | 1 replacement(s) | wrong translation (EN: cut its original ATK in half) |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 37 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 47 | 2 replacement(s) | comma, full stop |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 49 | 1 replacement(s) | comma, compound |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 55 | 1 replacement(s) | number |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 56 | 1 replacement(s) | number |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 60 | 1 replacement(s) | number |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 69 | 1 replacement(s) | wrong color code |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 85 | 1 replacement(s) | number, hyphenation |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 90 | 1 replacement(s) | number |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 92 | 1 replacement(s) | typo |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 109 | 2 replacement(s) | grammar, gender |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 121 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 122 | 1 replacement(s) | inconsistent term (Gegnerrunde) |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 125 | 1 replacement(s) | case |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 128 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 129 | 2 replacement(s) | wrong card name (EN: Shrink), space |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 135 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 151 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 152 | 1 replacement(s) | gender |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 153 | 1 replacement(s) | grammar |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 175 | 2 replacement(s) | space, article |
| tutorial/tutorial_g.ehp | 04_message_res.bin | 179 | 1 replacement(s) | gender |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 38 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 55 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 95 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 104 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 105 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 112 | 4 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 123 | 3 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 127 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 129 | 3 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 130 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 131 | 3 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 135 | 2 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 138 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 141 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 142 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 143 | 2 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 144 | 3 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 145 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 147 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 148 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 176 | 3 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 177 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 178 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 179 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 181 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 182 | 3 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 183 | 2 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 185 | 2 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 186 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 187 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 191 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 192 | 2 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |
| duel/basic_*g.ehp | help_strtbl_contents_duel_g.bin | 193 | 1 replacement(s) | as in deck/all_g.ehp help_strtbl_contents.bin |

### Targeted corrections `ui_texts.json`
| file | member | index | old | new | reason |
|---|---|---|---|---|---|

### Complete list
**Complete comparison with highlighted words: `docs/changes_de/ui_strings_diff.md`.** Raw data: `docs/changes_de/ui_strings.csv`. First 40:

| member | index | original | new |
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

(... 541 more rows in the CSV)

## A6. [SPELL CARD] / [TRAP CARD] label of the large card in the duel

In all the `duel/basic_<region><language>.ehp` the label was in English (hash `c2268340`): `apply_to_iso.py` replaces it with `card_spell_trap.gim` of `field/always_<language>_<language>.ehp` (hash `9622cd75`).

| archive | member | original hash | new hash |
|---|---|---|---|
| /PSP_GAME/USRDIR/duel/basic_bg.ehp | card_spell_trap.gim | c2268340 | be08846c |
| /PSP_GAME/USRDIR/duel/basic_fg.ehp | card_spell_trap.gim | c2268340 | be08846c |
| /PSP_GAME/USRDIR/duel/basic_gg.ehp | card_spell_trap.gim | c2268340 | be08846c |
| /PSP_GAME/USRDIR/duel/basic_ig.ehp | card_spell_trap.gim | c2268340 | be08846c |
| /PSP_GAME/USRDIR/duel/basic_sg.ehp | card_spell_trap.gim | c2268340 | be08846c |
| /PSP_GAME/USRDIR/duel/basic_ug.ehp | card_spell_trap.gim | c2268340 | be08846c |

## A7. ISO files touched and technical details

179 `.ehp` archives differ from the original (all languages together, because the ISO is a single one; list in `docs/changes_de/touched_files.csv`). The other files (video, audio, `EBOOT.BIN` executable, `PARAM.SFO`) are identical. Non-textual technical differences: `*-ptrs.txt` (absolute member offsets, recomputed when a table changes length), new position of the archives at the end of the ISO.

## A8. What can NOT be changed (game limits)

- The **speaker name** in the dialogue box (e.g. "Preside Sheppard"/"Cancelliere" in Italian, "Doyen Sheppard" in French, "Rector Sheppard" in Spanish) lives in the encrypted EBOOT: it cannot be modified.
- Texts drawn by the game with its own font (dialogues, names, descriptions in the deck, drop-down menus, system keyboard, language selection screen) cannot be replaced by the texture pack: they can only be changed in the ISO.
- The 438 map/background textures are not replaced (the game changes their palette): a limit of MikeyMK's pack, not of our work.

---

# B. TEXTURE PACK

## B1. Origin and structure

Base: **Yu-Gi-Oh! GX Tag Force 1 HD Remastered** by **MikeyMK** (US pack `ULUS10136`) and HD cards by **chrisfand**, adapted to the European ISO `ULES00600`. The project does not redistribute the third-party pack: the patcher gets it from the user. Our work: (1) remap the US pack's **hashes** to the EU ones (`tools/gen_ini.py`), (2) redo the cards and interface lettering in the language, (3) correct the texts, (4) `upscale_extra` for the textures that are not covered.

PPSSPP recognizes a texture by the **hash of its pixels** (xxhash of the data, `gim.data_hash`); every line of `textures.ini` is `0000000000000000<hash8> = path/png`. The PNGs are **4x** the original and redraw exactly the same area. Textures that are identical between languages have the same hash: the replacement holds for all of them (see `docs/TEXTURE_INVENTORY.md`).

### Real structure (from `docs/changes_de/pack_structure.csv`)
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
| moduli/de | cards/ | 5675 | 1025.0 | frame, large_de, small_de, tiny_de |
| moduli/de | de.ini | 1 | 0.01 |  |
| moduli/de | intro/ | 2 | 0.4 | title_screen |
| moduli/de | ui_de/ | 106 | 8.2 | fogli_icone, fogli_icone.ini, lettere_esito, lettere_esito.ini, menu_liste, menu_liste.ini, schede_deck, schede_deck.ini, schede_ricette, schede_ricette.ini ... |

Every language except Italian is a **module** (`PSP/TEXTURES/modules/de`) to compose over the base pack with `tools/compose_pack.py BASE MODULES CARD_DIR OUT de [--copy]`: it copies the base and **only** the `cards`, `intro` and `ui_de` folders of the module (hard link or copy), then `module_ini.py` rewrites the `textures.ini`: the localized card lines point to `cards/small_de`/`large_de` and the lines of `de.ini` **replace** those of the base with the same key (hash).

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

Language folders: `frame` (2 files), `large_de` (2833 files), `small_de` (2833 files), `tiny_de` (7 files). Every card has an **HD small** one (name + description + type, regenerated with free OFL fonts: XCharter Bold for names/type/labels, Libre Baskerville for effects, Newsreader Italic for Normals, PT Serif Caption for Spells/Traps, Charis SIL for the missing glyphs) and an **HD large** one (name only on the frame). In addition: the **attribute table** with the words of the language (`cards/frame/icons_attribute_race_<l>.png`, `attributes.py`), the **Spell/Trap label** (`icons_spell_trap_<l>.png`, `label_it.py` / `extract_labels.py` -> `data/label_eu_<code>_128x32.png`) and the deck **thumbnail atlas** (`tiny_<l>`, `tiny_atlas.py` + `tiny_fragment.py`).

When the text of a card changes (section A2) its images must be regenerated: **258 cards** in german. List in `docs/changes_de/card_images.csv`. Command: `python tools/generate_language.py fr PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` (without IDs it regenerates all of them: 2,833 + 2,833, ~930 MB).

Typography: non-breaking space before `: ; ! ?` and « » quotation marks.

## B3. HD interface in german (`ui_de`)

**98 textures** (`docs/changes_de/ui_textures.csv`: file, PPSSPP hash, family, script, original/HD size, neutral/specific, origin in the ISO). By family: fogli_icone 3, lettere_esito 28, menu_liste 6, schede_deck 14, schede_ricette 12, schermata_vs 14, scritte_duello 15, tutorial 6. Of these 0 are neutral (same hash in all languages) and 98 specific. Every family has a script in `tools/ui_textures/<family>.py` (reads `TF1_LANG`): it redraws the lettering texture by texture starting from the low-resolution original of the ISO and from the style of the English pack; same area and same positions (the game crops from fixed rectangles); one font/weight/baseline/shadow per lettering; free fonts (`alt_font.py`).

| family | textures | script | source ISO archive | language texts |
|---|---|---|---|---|
| fogli_icone | 3 | `tools/ui_textures/fogli_icone.py` | ? |  |
| lettere_esito | 28 | `tools/ui_textures/lettere_esito.py` | ? |  |
| menu_liste | 6 | `tools/ui_textures/menu_liste.py` | ? |  |
| schede_deck | 14 | `tools/ui_textures/schede_deck.py` | ? |  |
| schede_ricette | 12 | `tools/ui_textures/schede_ricette.py` | ? |  |
| schermata_vs | 14 | `tools/ui_textures/schermata_vs.py` | ? |  |
| scritte_duello | 15 | `tools/ui_textures/scritte_duello.py` | ? |  |
| tutorial | 6 | `tools/ui_textures/tutorial.py` | tutorial/tutorial_g.ehp (tuto_duelimg01..06) |  |

Quality rules (valid for every language): regular letters, never deformed one by one; same area as the original; no blur; the text is that of the language's original (only obvious errors are corrected: leftovers from other languages, accents); pixel art is **not** smoothed without confirmation; geometries always measured on the original.

### Drawn texts: original -> HD
Table read by eye, texture by texture: `docs/changes_de/texture_texts_de.md`. Differences from the original: `DEMARRER` -> `DÉMARRER`, `SCAMBIA`/`Scambia` -> `ÉCHANGE`/`Échange`, `2è/3è round` -> `2e/3e round`; everything else rewrites the same words.

### List of every texture
(all 98 rows, from `ui_textures.csv`)

| file in the pack | hash | family | original px | HD px | type | ISO origin |
|---|---|---|---|---|---|---|
| ui_de/fogli_icone/all_g__icon04.png | ce4fe497 | fogli_icone | 128x128 | 512x512 | SPECIFIC | deck/all_g.ehp:icon04.gim |
| ui_de/fogli_icone/all_g__panel.png | 68141938 | fogli_icone | 256x256 | 1024x1024 | SPECIFIC | shop/all_g.ehp:panel.gim |
| ui_de/fogli_icone/all_g__s_pack.png | 731df6d4 | fogli_icone | 256x256 | 1024x1024 | SPECIFIC | shop/all_g.ehp:s_pack.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100002.png | b15e254f | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_draw100002.gim; duel/basic_fg.ehp:duel_draw100002.gim; duel/basic_gg.ehp:duel_draw100002.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100004.png | 3dcf0348 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_draw100004.gim; duel/basic_fg.ehp:duel_draw100004.gim; duel/basic_gg.ehp:duel_draw100004.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100006.png | 988d2924 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_draw100006.gim; duel/basic_fg.ehp:duel_draw100006.gim; duel/basic_gg.ehp:duel_draw100006.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100008.png | c27723c2 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_draw100008.gim; duel/basic_fg.ehp:duel_draw100008.gim; duel/basic_gg.ehp:duel_draw100008.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100010.png | d40c8877 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_draw100010.gim; duel/basic_fg.ehp:duel_draw100010.gim; duel/basic_gg.ehp:duel_draw100010.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100012.png | f32aec8b | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_draw100012.gim; duel/basic_fg.ehp:duel_draw100012.gim; duel/basic_gg.ehp:duel_draw100012.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100014.png | 7164c557 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_draw100014.gim; duel/basic_fg.ehp:duel_draw100014.gim; duel/basic_gg.ehp:duel_draw100014.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100016.png | bf811ab0 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_draw100016.gim; duel/basic_fg.ehp:duel_draw100016.gim; duel/basic_gg.ehp:duel_draw100016.gim |
| ui_de/lettere_esito/basic_gg__duel_draw100018.png | fd752d95 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_draw100018.gim; duel/basic_fg.ehp:duel_draw100018.gim; duel/basic_gg.ehp:duel_draw100018.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100002.png | 912fcd45 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_lose100002.gim; duel/basic_fg.ehp:duel_lose100002.gim; duel/basic_gg.ehp:duel_lose100002.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100004.png | 20c32463 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_lose100004.gim; duel/basic_fg.ehp:duel_lose100004.gim; duel/basic_gg.ehp:duel_lose100004.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100006.png | 7e4814ae | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_lose100006.gim; duel/basic_fg.ehp:duel_lose100006.gim; duel/basic_gg.ehp:duel_lose100006.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100008.png | e758002f | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_lose100008.gim; duel/basic_fg.ehp:duel_lose100008.gim; duel/basic_gg.ehp:duel_lose100008.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100010.png | fe18c251 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_lose100010.gim; duel/basic_fg.ehp:duel_lose100010.gim; duel/basic_gg.ehp:duel_lose100010.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100012.png | adde0b1d | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_lose100012.gim; duel/basic_fg.ehp:duel_lose100012.gim; duel/basic_gg.ehp:duel_lose100012.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100014.png | a3ed8c27 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_lose100014.gim; duel/basic_fg.ehp:duel_lose100014.gim; duel/basic_gg.ehp:duel_lose100014.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100016.png | 49b0e354 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_lose100016.gim; duel/basic_fg.ehp:duel_lose100016.gim; duel/basic_gg.ehp:duel_lose100016.gim |
| ui_de/lettere_esito/basic_gg__duel_lose100018.png | 1ee989bc | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_lose100018.gim; duel/basic_fg.ehp:duel_lose100018.gim; duel/basic_gg.ehp:duel_lose100018.gim |
| ui_de/lettere_esito/basic_gg__duel_win100002.png | c8ecef23 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_win100002.gim; duel/basic_fg.ehp:duel_win100002.gim; duel/basic_gg.ehp:duel_win100002.gim |
| ui_de/lettere_esito/basic_gg__duel_win100004.png | 6d2aaacc | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_win100004.gim; duel/basic_fg.ehp:duel_win100004.gim; duel/basic_gg.ehp:duel_win100004.gim |
| ui_de/lettere_esito/basic_gg__duel_win100006.png | 51a3b5f3 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_win100006.gim; duel/basic_fg.ehp:duel_win100006.gim; duel/basic_gg.ehp:duel_win100006.gim |
| ui_de/lettere_esito/basic_gg__duel_win100008.png | 3ee7d405 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_win100008.gim; duel/basic_fg.ehp:duel_win100008.gim; duel/basic_gg.ehp:duel_win100008.gim |
| ui_de/lettere_esito/basic_gg__duel_win100010.png | 595a731a | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_win100010.gim; duel/basic_fg.ehp:duel_win100010.gim; duel/basic_gg.ehp:duel_win100010.gim |
| ui_de/lettere_esito/basic_gg__duel_win100012.png | 2ea9ce79 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_win100012.gim; duel/basic_fg.ehp:duel_win100012.gim; duel/basic_gg.ehp:duel_win100012.gim |
| ui_de/lettere_esito/basic_gg__duel_win100014.png | e6b4a13d | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_win100014.gim; duel/basic_fg.ehp:duel_win100014.gim; duel/basic_gg.ehp:duel_win100014.gim |
| ui_de/lettere_esito/basic_gg__duel_win100016.png | 92a3b4b9 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_win100016.gim; duel/basic_fg.ehp:duel_win100016.gim; duel/basic_gg.ehp:duel_win100016.gim |
| ui_de/lettere_esito/basic_gg__duel_win100018.png | 9b93a537 | lettere_esito | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:duel_win100018.gim; duel/basic_fg.ehp:duel_win100018.gim; duel/basic_gg.ehp:duel_win100018.gim |
| ui_de/lettere_esito/basic_gg__duel_win100020.png | b5401172 | lettere_esito | 64x32 | 256x128 | SPECIFIC | duel/basic_bg.ehp:duel_win100020.gim; duel/basic_fg.ehp:duel_win100020.gim; duel/basic_gg.ehp:duel_win100020.gim |
| ui_de/menu_liste/always_bri_ger__story_sys02.png | bcd751d8 | menu_liste | 256x128 | 1024x512 | SPECIFIC | field/always_bri_ger.ehp:story_sys02.gim; field/always_fra_ger.ehp:story_sys02.gim; field/always_ger_ger.ehp:story_sys02.gim |
| ui_de/menu_liste/result_g__menu01.png | 43526e37 | menu_liste | 256x64 | 1024x256 | SPECIFIC | duel/result/result_g.ehp:menu01.gim |
| ui_de/menu_liste/result_g__menu02.png | 9a4a8236 | menu_liste | 256x128 | 1024x512 | SPECIFIC | duel/result/result_g.ehp:menu02.gim |
| ui_de/menu_liste/title_menu_g__m_menu_title01.png | 90284e3a | menu_liste | 256x128 | 1024x512 | SPECIFIC | title_menu/title_menu_g.ehp:m_menu_title01.gim |
| ui_de/menu_liste/title_menu_g__press_start0003.png | 57081762 | menu_liste | 256x16 | 1024x64 | SPECIFIC | title_menu/title_menu_g.ehp:press_start0003.gim |
| ui_de/menu_liste/title_menu_g__trnsmt02.png | 800ca6a3 | menu_liste | 256x256 | 1024x1024 | SPECIFIC | title_menu/title_menu_g.ehp:trnsmt02.gim |
| ui_de/schede_deck/all_g__d_window00008.png | 410ef331 | schede_deck | 128x32 | 512x128 | SPECIFIC | deck/all_g.ehp:d_window00008.gim |
| ui_de/schede_deck/all_g__d_window00016.png | 34a9652d | schede_deck | 64x32 | 256x128 | SPECIFIC | deck/all_e.ehp:d_window00016.gim; deck/all_f.ehp:d_window00016.gim; deck/all_g.ehp:d_window00016.gim |
| ui_de/schede_deck/all_g__d_window00033.png | 328738aa | schede_deck | 256x32 | 1024x128 | SPECIFIC | deck/all_g.ehp:d_window00033.gim |
| ui_de/schede_deck/all_g__d_window00051.png | 78e0995c | schede_deck | 64x32 | 256x128 | SPECIFIC | deck/all_g.ehp:d_window00051.gim |
| ui_de/schede_deck/all_g__d_window00062.png | 0b841a08 | schede_deck | 128x32 | 512x128 | SPECIFIC | deck/all_g.ehp:d_window00062.gim; labo/conv_machine.ehp:window_g0016.gim; title_menu/title_menu_g.ehp:t_window0015.gim |
| ui_de/schede_deck/all_g__d_window00101.png | dac6a171 | schede_deck | 64x32 | 256x128 | SPECIFIC | deck/all_g.ehp:d_window00101.gim; labo/rental.ehp:window_g0008.gim |
| ui_de/schede_deck/all_g__tab_title.png | c51223fd | schede_deck | 256x32 | 1024x128 | SPECIFIC | shop/all_g.ehp:tab_title.gim |
| ui_de/schede_deck/conv_machine__window_g0009.png | 467c47c3 | schede_deck | 128x32 | 512x128 | SPECIFIC | labo/conv_machine.ehp:window_g0009.gim; labo/conv_machine.ehp:window_g0026.gim |
| ui_de/schede_deck/conv_machine__window_g0016.png | 0b841a08 | schede_deck | 128x32 | 512x128 | SPECIFIC | deck/all_g.ehp:d_window00062.gim; labo/conv_machine.ehp:window_g0016.gim; title_menu/title_menu_g.ehp:t_window0015.gim |
| ui_de/schede_deck/conv_machine__window_g0026.png | 467c47c3 | schede_deck | 128x32 | 512x128 | SPECIFIC | labo/conv_machine.ehp:window_g0009.gim; labo/conv_machine.ehp:window_g0026.gim |
| ui_de/schede_deck/password__key_g0027.png | f2102f5c | schede_deck | 128x32 | 512x128 | SPECIFIC | labo/password.ehp:key_g0027.gim |
| ui_de/schede_deck/rental__window_g0008.png | dac6a171 | schede_deck | 64x32 | 256x128 | SPECIFIC | deck/all_g.ehp:d_window00101.gim; labo/rental.ehp:window_g0008.gim |
| ui_de/schede_deck/rental__window_g0015.png | 55e5724d | schede_deck | 128x32 | 512x128 | SPECIFIC | labo/rental.ehp:window_g0015.gim |
| ui_de/schede_deck/rental__window_g0026.png | 47f0c275 | schede_deck | 64x32 | 256x128 | SPECIFIC | labo/rental.ehp:window_g0026.gim |
| ui_de/schede_ricette/limitlist__window_g0002.png | 3bda99aa | schede_ricette | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_g0002.gim |
| ui_de/schede_ricette/limitlist__window_g0004.png | a6a65331 | schede_ricette | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_g0004.gim |
| ui_de/schede_ricette/limitlist__window_g0012.png | c03e3475 | schede_ricette | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_g0012.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010004.png | 97f5751a | schede_ricette | 256x64 | 1024x256 | SPECIFIC | deck/recipe_view_g.ehp:recipe010004.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010008.png | 1e332ce0 | schede_ricette | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_g.ehp:recipe010008.gim; title_menu/title_menu_g.ehp:recipe_sel00002.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010015.png | 31608bc8 | schede_ricette | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_g.ehp:recipe010015.gim; title_menu/title_menu_g.ehp:recipe_sel00009.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010027.png | 84c2dc4b | schede_ricette | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_g.ehp:recipe010027.gim; title_menu/title_menu_g.ehp:recipe_sel00020.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010029.png | 2aec2bee | schede_ricette | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_g.ehp:recipe010029.gim; title_menu/title_menu_g.ehp:recipe_sel00022.gim |
| ui_de/schede_ricette/recipe_view_g__recipe010031.png | 3582dfbc | schede_ricette | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_g.ehp:recipe010031.gim; title_menu/title_menu_g.ehp:recipe_sel00024.gim |
| ui_de/schede_ricette/title_menu_g__recipe_sel00033.png | f000f198 | schede_ricette | 128x32 | 512x128 | SPECIFIC | title_menu/title_menu_g.ehp:recipe_sel00033.gim |
| ui_de/schede_ricette/title_menu_g__t_window0008.png | 8f980210 | schede_ricette | 64x32 | 256x128 | SPECIFIC | title_menu/title_menu_g.ehp:t_window0008.gim |
| ui_de/schede_ricette/title_menu_g__t_window0026.png | 8fee65d6 | schede_ricette | 64x32 | 256x128 | SPECIFIC | title_menu/title_menu_g.ehp:t_window0026.gim |
| ui_de/schermata_vs/start_all__jyanken20_g0005.png | 2469fc30 | schermata_vs | 256x32 | 1024x128 | SPECIFIC | duel/start/start_all.ehp:jyanken20_g0005.gim; duel/start/start_e.ehp:jyanken20_g0005.gim; duel/start/start_f.ehp:jyanken20_g0005.gim |
| ui_de/schermata_vs/start_all__jyanken20_g0007.png | 8729983a | schermata_vs | 256x32 | 1024x128 | SPECIFIC | duel/start/start_all.ehp:jyanken20_g0007.gim; duel/start/start_e.ehp:jyanken20_g0007.gim; duel/start/start_f.ehp:jyanken20_g0007.gim |
| ui_de/schermata_vs/start_all__vs_much1_g0001.png | 647ec094 | schermata_vs | 128x16 | 512x64 | SPECIFIC | duel/start/start_all.ehp:vs_much1_g0001.gim; duel/start/start_e.ehp:vs_much1_g0001.gim; duel/start/start_f.ehp:vs_much1_g0001.gim |
| ui_de/schermata_vs/start_all__vs_much2_g0001.png | d6e3420a | schermata_vs | 128x16 | 512x64 | SPECIFIC | duel/start/start_all.ehp:vs_much2_g0001.gim; duel/start/start_e.ehp:vs_much2_g0001.gim; duel/start/start_f.ehp:vs_much2_g0001.gim |
| ui_de/schermata_vs/start_all__vs_much3_g0001.png | 0bf3bc02 | schermata_vs | 128x16 | 512x64 | SPECIFIC | duel/start/start_all.ehp:vs_much3_g0001.gim; duel/start/start_e.ehp:vs_much3_g0001.gim; duel/start/start_f.ehp:vs_much3_g0001.gim |
| ui_de/schermata_vs/start_e__d_menu01_g.png | 23d1ae0c | schermata_vs | 256x256 | 1024x1024 | SPECIFIC | duel/start/start_e.ehp:d_menu01_g.gim; duel/start/start_f.ehp:d_menu01_g.gim; duel/start/start_g.ehp:d_menu01_g.gim |
| ui_de/schermata_vs/start_e__vs_bg01_1_g0005.png | 9b2a5a3b | schermata_vs | 256x32 | 1024x128 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_g0005.gim; duel/start/start_f.ehp:vs_bg01_1_g0005.gim; duel/start/start_g.ehp:vs_bg01_1_g0005.gim |
| ui_de/schermata_vs/start_e__vs_bg01_1_g0007.png | cc2fd1b7 | schermata_vs | 256x64 | 1024x256 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_g0007.gim; duel/start/start_f.ehp:vs_bg01_1_g0007.gim; duel/start/start_g.ehp:vs_bg01_1_g0007.gim |
| ui_de/schermata_vs/start_e__vs_bg01_1_g0008.png | e3f4a299 | schermata_vs | 256x64 | 1024x256 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_g0008.gim; duel/start/start_f.ehp:vs_bg01_1_g0008.gim; duel/start/start_g.ehp:vs_bg01_1_g0008.gim |
| ui_de/schermata_vs/start_e__vs_bg01_1_g0012.png | d94ea205 | schermata_vs | 128x32 | 512x128 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_g0012.gim; duel/start/start_f.ehp:vs_bg01_1_g0012.gim; duel/start/start_g.ehp:vs_bg01_1_g0012.gim |
| ui_de/schermata_vs/start_e__vs_bg01_1_g0014.png | 6b884f0c | schermata_vs | 128x64 | 512x256 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_g0014.gim; duel/start/start_f.ehp:vs_bg01_1_g0014.gim; duel/start/start_g.ehp:vs_bg01_1_g0014.gim |
| ui_de/schermata_vs/start_e__vs_bg01_2_g0001.png | 1dd44271 | schermata_vs | 128x16 | 512x64 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_2_g0001.gim; duel/start/start_f.ehp:vs_bg01_2_g0001.gim; duel/start/start_g.ehp:vs_bg01_2_g0001.gim |
| ui_de/schermata_vs/start_e__vs_bg01_2_g0004.png | 38434306 | schermata_vs | 128x16 | 512x64 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_2_g0004.gim; duel/start/start_f.ehp:vs_bg01_2_g0004.gim; duel/start/start_g.ehp:vs_bg01_2_g0004.gim |
| ui_de/schermata_vs/start_g__jnk_card01.png | cc4d76f2 | schermata_vs | 512x256 | 2048x1024 | SPECIFIC | duel/start/start_g.ehp:jnk_card01.gim |
| ui_de/scritte_duello/basic_gg__chain010003.png | d08b0e76 | scritte_duello | 64x32 | 256x128 | SPECIFIC | duel/basic_bg.ehp:chain010003.gim; duel/basic_fg.ehp:chain010003.gim; duel/basic_gg.ehp:chain010003.gim |
| ui_de/scritte_duello/basic_gg__chain010005.png | 63fc2f5c | scritte_duello | 128x32 | 512x128 | SPECIFIC | duel/basic_bg.ehp:chain010005.gim; duel/basic_fg.ehp:chain010005.gim; duel/basic_gg.ehp:chain010005.gim |
| ui_de/scritte_duello/basic_gg__dilect_atk00001.png | 207c290e | scritte_duello | 256x32 | 1024x128 | SPECIFIC | duel/basic_bg.ehp:dilect_atk00001.gim; duel/basic_fg.ehp:dilect_atk00001.gim; duel/basic_gg.ehp:dilect_atk00001.gim |
| ui_de/scritte_duello/basic_gg__dilect_atk00003.png | fd670497 | scritte_duello | 128x32 | 512x128 | SPECIFIC | duel/basic_bg.ehp:dilect_atk00003.gim; duel/basic_fg.ehp:dilect_atk00003.gim; duel/basic_gg.ehp:dilect_atk00003.gim |
| ui_de/scritte_duello/basic_gg__next_player0001.png | 5212b3a9 | scritte_duello | 64x16 | 256x64 | SPECIFIC | duel/basic_bg.ehp:next_player0001.gim; duel/basic_fg.ehp:next_player0001.gim; duel/basic_gg.ehp:next_player0001.gim |
| ui_de/scritte_duello/basic_gg__next_player0002.png | 22c1e7af | scritte_duello | 64x32 | 256x128 | SPECIFIC | duel/basic_bg.ehp:next_player0002.gim; duel/basic_fg.ehp:next_player0002.gim; duel/basic_gg.ehp:next_player0002.gim |
| ui_de/scritte_duello/basic_gg__next_player0003.png | a3399289 | scritte_duello | 256x32 | 1024x128 | SPECIFIC | duel/basic_bg.ehp:next_player0003.gim; duel/basic_fg.ehp:next_player0003.gim; duel/basic_gg.ehp:next_player0003.gim |
| ui_de/scritte_duello/basic_gg__next_player0005.png | 042946dc | scritte_duello | 64x16 | 256x64 | SPECIFIC | duel/basic_bg.ehp:next_player0005.gim; duel/basic_fg.ehp:next_player0005.gim; duel/basic_gg.ehp:next_player0005.gim |
| ui_de/scritte_duello/basic_gg__next_player0006.png | f0dfc85e | scritte_duello | 64x32 | 256x128 | SPECIFIC | duel/basic_bg.ehp:next_player0006.gim; duel/basic_fg.ehp:next_player0006.gim; duel/basic_gg.ehp:next_player0006.gim |
| ui_de/scritte_duello/basic_gg__next_player0007.png | c30370b4 | scritte_duello | 256x32 | 1024x128 | SPECIFIC | duel/basic_bg.ehp:next_player0007.gim; duel/basic_fg.ehp:next_player0007.gim; duel/basic_gg.ehp:next_player0007.gim |
| ui_de/scritte_duello/basic_gg__score-top100011.png | 20d674aa | scritte_duello | 32x32 | 128x128 | SPECIFIC | duel/basic_bg.ehp:score-top100011.gim; duel/basic_fg.ehp:score-top100011.gim; duel/basic_gg.ehp:score-top100011.gim |
| ui_de/scritte_duello/basic_gg__score-top100013.png | aab8884f | scritte_duello | 32x32 | 128x128 | SPECIFIC | duel/basic_bg.ehp:score-top100013.gim; duel/basic_fg.ehp:score-top100013.gim; duel/basic_gg.ehp:score-top100013.gim |
| ui_de/scritte_duello/basic_gg__start_duel10001.png | 13405678 | scritte_duello | 64x64 | 256x256 | SPECIFIC | duel/basic_bg.ehp:start_duel10001.gim; duel/basic_fg.ehp:start_duel10001.gim; duel/basic_gg.ehp:start_duel10001.gim |
| ui_de/scritte_duello/basic_gg__start_duel10002.png | 9bf6803a | scritte_duello | 256x64 | 1024x256 | SPECIFIC | duel/basic_bg.ehp:start_duel10002.gim; duel/basic_fg.ehp:start_duel10002.gim; duel/basic_gg.ehp:start_duel10002.gim |
| ui_de/scritte_duello/basic_gg__start_duel10005.png | ef0dcee9 | scritte_duello | 128x32 | 512x128 | SPECIFIC | duel/basic_bf.ehp:start_duel10005.gim; duel/basic_bg.ehp:start_duel10005.gim; duel/basic_ff.ehp:start_duel10005.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg01.png | 5642fab0 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_g.ehp:tuto_duelimg01.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg02.png | de3b0f96 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_g.ehp:tuto_duelimg02.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg03.png | 78b9eca8 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_g.ehp:tuto_duelimg03.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg04.png | 4119cb51 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_g.ehp:tuto_duelimg04.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg05.png | 7f7bdfb2 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_g.ehp:tuto_duelimg05.gim |
| ui_de/tutorial/tutorial_g__tuto_duelimg06.png | 931db074 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_g.ehp:tuto_duelimg06.gim |

### Textures that stay like the original
`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `parts` are pixel-art icon sheets (with NEU/NEW): they stay as they were, covered by the `upscale_extra` enlargement as in the other languages; the text was not changed. The neutral textures come from the base pack. In Spanish `score-top` (TURNO) also has the same hash as Italian and `card_icon03` is in `upscale_extra`.

## B4. The duel number sheet (`card_icon03`)

A single sheet with LP digits, time, keys and multipliers; different hash per language. Recipe chosen by the user (`tools/ui_textures/icon03_languages.py`, rerun with `--apply`):
- rows 0-180 (small digits and signs, orange keys 1/2/3, big digits 0-9 with "LP", small digits 0-9): **from the US pack**, crisp pixel art;
- cells in which the European game differs from the US pack (black check mark, grey ball, empty pill, time word): **original pixels enlarged 4x without smoothing**; time word **ZEIT**; the orange pill ("Single" in the US pack) stays **empty**;
- rows >= 181 (multipliers x1..x12, icons, cards, arrows): from the Italian sheet already in the pack (`tools/data/card_icon03_base_it.png`);
- the European cells are pasted **only in their band** of rows (otherwise they spoil the top of the big digits).

Files: it -> `ui_it/duel_texts/basic_ii__card_icon03.png` (hash 376925c7); fr -> `upscale_extra/3e5482fd.png`; en ee0c44c3; de ffe309a6; es 859eea2b. Previews in `comparisons/icon03/`.

## B5. Title plate

`python tools/ui_textures/mystic_tomato_title.py de` generates 2 PNGs (`542eff79685c434d`, `705176739829dcf5`, tiles 18 and 19 of the 20-tile 128x64 backdrop `title_menu_i.ehp: main_title00001..00020`) with card 4930 in the language + the "version" wording + the flag, PT Sans Bold font: **"EDITION MYSTISCHE TOMATE"**. The plate **is included only for the chosen language** (it lives in `modules/de/intro/title_screen/`); the original base pack has the tiles without a banner. Files in this pack: `moduli/de/intro/title_screen/00000000542eff79685c434d.png`, `moduli/de/intro/title_screen/00000000705176739829dcf5.png`.

## B6. `textures.ini` and composition

`tools/gen_ini.py TOOLS US_INI CARD_DIR OUT_INI i=it +extra_it.ini +ui_it.ini +data/upscale_extra.ini` converts the US `textures.ini` into the EU one: the non-card entries stay (neutral textures = same hashes); the card entries are regenerated from the EU `card/*.cip` archives for the 5 languages (`i=it` remaps `cards/large/X.png` -> `cards/large_it/X.png`); it adds the Spell/Trap label (`extra_it.ini`), the `ui_it` lines and `upscale_extra.ini`. It is also done for the 3 card styles. If the same pixels exist in several languages the first in `e i f g s` wins (for this reason atlas, banner and attribute table are "one per installation").

`ui_de` lines in `de.ini`: 98. Prefix frequency: `docs/changes_de/ini_lines.csv`. Check: every `ui_de/...` line must point to an existing file and there must be no duplicate hashes.

## B7. Installation and settings

PC: copy `ULES00600` into `<PPSSPP>/PSP/TEXTURES/` (Android: `textures.zip` in `.../TEXTURES/ULES00600/`, without extracting it; regenerate the zip with the corrections). Settings: **Replace textures ON**, rendering resolution **4x**, game language = module language (the language is stored in the **save file**). After changing a single PNG it is enough to copy it and restart PPSSPP (cache). To try the texts use the `_definitiva` ISO.

---

# C. EDITORIAL CHOICES

- **Rector Sheppard** (as in the dialogues) in the cards and maps ("Oficina del Rector"); dormitories **Slifer Rojo, Ra Amarillo, Obelisco Azul**; **Jinetes de la Sombra**; "Habitación" instead of "Alójese" (Room).
- Sake/shochu and maid outfit as in the other languages (`st01_t01/Scr003E`), `st02_t01/Scr101E` rotated; "Sirviente de la Calavera", "Toon", "Archidemonio", "Trío Ojama" and name accents as on the cards.
- Options: "EN/FUERADE" -> "ON/OFF"; title messages ("nuevos datos de juego"), tutorial lessons ("le turno" -> "es el turno de", swapped x/o keys, closed color codes), final paragraph of the Tag Duels translated (it was truncated/in English).
- Terms left as in the game: "Invocación por Sacrificio", "Tributar", "Efecto de Blanco", "Tronco" (open questions in `docs/changes_es/open_questions_es.md`).
- Number sheet: digits/LP from the US pack, x1..x12 from the Italian sheet, time word ZEIT.

### Entries of the choices register for this language (`tools/data/editorial_choices.json`)
| id | original | corrected | inherited | reason |
|---|---|---|---|---|
| st01_t01/Scr003E#146 | Meinem Vater gehört eine Firma,⏎die scharfe Saucen herstellt. | Meinem Vater gehört eine⏎Sake-Brauerei. | no | sake al posto di salsa piccante (fedele al giapponese: la famiglia di Chumley fa sake) |
| st01_t01/Scr003E#147 | Er hat mir zusammen mit dem Taschengeld⏎auch etwas scharfe Sauce geschickt.⏎Ich mach dir einen guten Preis.⏎Interesse? | Er hat mir zusammen mit dem Taschengeld⏎auch etwas Shochu geschickt.⏎Ich mach dir einen guten Preis.⏎Interesse? | no | shochu al posto di salsa piccante |
| st01_t01/Scr003E#150 | Meinem Vater gehört eine Firma,⏎die scharfe Saucen herstellt. | Meinem Vater gehört eine⏎Sake-Brauerei. | no | come 146 |
| st01_t01/Scr003E#151 | Er hat mir zusammen mit dem Taschengeld⏎auch etwas scharfe Sauce geschickt.⏎Ich mach dir einen guten Preis.⏎Interesse? | Er hat mir zusammen mit dem Taschengeld⏎auch etwas Shochu geschickt.⏎Ich mach dir einen guten Preis.⏎Interesse? | no | come 147 |
| st01_t01/Scr003E#163 | Wow. Du hast es geschafft.⏎《C026_2》...⏎Im Bikini! | Wow. Du hast es geschafft.⏎《C026_2》...⏎Im Dienstmädchen-Outfit! | no | abito da cameriera al posto di bikini (giapponese: メイド服) |
| st01_t01/Scr003E#168 | Wow. Du hast es geschafft.⏎《C026_2》...⏎Im Bikini! | Wow. Du hast es geschafft.⏎《C026_2》...⏎Im Dienstmädchen-Outfit! | no | come 163 |
| st01_t01/Scr003E#188 | Tja, ein wenig schon ... | None | yes | solo italiano: "sto sbavando" era un errore di traduzione (giapponese: "non sono poi così bravo") |
| st01_t01/Scr003E#189 | Hey, kannst du was für mich zeichnen?⏎Zeichne mir 《C026_2》 im Bikini! | Hey, kannst du was für mich zeichnen?⏎Zeichne mir 《C026_2》 im Dienstmädchen-Outfit! | no | abito da cameriera al posto di bikini |
| st01_t01/Scr003E#191 | Hier, du kannst den hier nehmen! | Hier, nimm dieses Dienstmädchen-Outfit! | no | Syrus passa un abito da cameriera come modello (メイド服): col bikini la battuta non aveva senso |
| st01_t01/Scr003E#194 | Tja, ein wenig schon ... | None | yes | come 188 |
| st01_t01/Scr003E#195 | Hey, kannst du was für mich zeichnen?⏎Zeichne mir 《C026_2》⏎im Bikini! | Hey, kannst du was für mich zeichnen?⏎Zeichne mir 《C026_2》⏎im Dienstmädchen-Outfit! | no | come 189 |
| st01_t01/Scr003E#197 | Hier, du kannst den hier nehmen! | Hier, nimm dieses Dienstmädchen-Outfit! | no | come 191 |

Other choices and the re-reading of the duel sentences: `docs/EDITORIAL_CHOICES.md`.

# D. IN-GAME VERIFICATION

- **Seen in game** (`_definitiva` ISO + `de` module, new game in German, 2026-10-12): language selection, title with the "MYSTISCHE TOMATE EDITION" plate and Neues Spiel/Fortfahren, "Daten geladen", HD Hauptmenue, Deck menu (Deck bearbeiten / Rezeptanzeige), deck editor (tabs Deck/Fusion/Side/Truhe, "Persoenliches Deck", "Eigene Kartentypen", Hilfe), Rezeptanzeige (Benutzer/Charakter, Fusionsdeck), confirmation "Deckbearbeitung verlassen", calendar ("1. Mai / Montag", "92 Tage bis zum Turnier"), map ("Duellakademie", list of places), office menu (Reden/Duell/Gegenstaende/PDA), dialogues of the chancellor and of Crowler in Klassenzimmer with the corrections (Buero des Kanzlers, Duellakademie, Haupttor...), 2-3-line boxes without cuts.
- **Not seen** (only read and compared with the original in the comparison sheets): Kette, Direktangriff, end of duel, rock-paper-scissors, ZWEITER/ERSTER, 1. Runde, tutorial and lessons, shop (AUSVERKAUFT, "Gekaufte Karten"), laboratory (Labor, Konverter, Miete), PDA, album, Optionen, cards with new text, duel sentences, VS screen.
- **Seen in the title demo duel** (2026-10-12): VS screen ("NORMALES DUELL", "Einzelmodus", "Gegen", badges), duel HUD, duelist sentences in German, card descriptions in German; "Draw Phase" stays English as in the original. Defects reported by the user: dialogue font not HD (system text, cannot be replaced with textures) and PSP save menu in French (PPSSPP system language).

# E. HOW TO REGENERATE EVERYTHING

```
# ISO (all languages together)
python tools/corrections/build_dialogues.py de
python tools/corrections/generate_card_corrections.py de CARDINFO_de.ehp          # cards
python tools/corrections/apply_to_iso.py PSP/GAME/ULES00600_..._EUR.iso PSP/GAME/ULES00600_..._EUR_definitiva.iso
# images
python tools/generate_language.py fr PACK CARDINFO US_INI CLEAN_DIR OUT [ID...]
TF1_LANG=de python tools/ui_textures/<family>.py USRDIR PACK_US <module>      # for each of the 8 families (whole!)
python tools/ui_textures/icon03_languages.py --apply ; python tools/ui_textures/mystic_tomato_title.py de
python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules USRDIR/card OUT de --copy
# this document
python tools/analysis/document_changes.py ISO_ORIG ISO_DEF de docs/changes_de
python tools/analysis/document_pack.py ISO_ORIG de docs/changes_de
python tools/analysis/text_comparisons.py de
python tools/analysis/write_changes_document.py de
```
External inputs you need (check that they exist): the original ISO, the extracted USRDIR (`tools/analysis/extract_usrdir.py`), MikeyMK's US pack `ULUS10136` (in a folder outside the project).

# F. LIMITS AND OPEN POINTS

- German textures added on 2026-10-13 (`result_letters` 28, `duel_texts` 15; before they were taken for equal to English, which was a mistake: see `docs/changes_de/texture_texts_de.md`): compared with the low-resolution original (tile overlay, check sheets), **not yet seen in game**. To check: the centring of the dots of the Ä of NÄCHSTER SPIELER (separate sprite), the width of SPIELZUG in the badge and the silhouette of DU GEWINNST.
- 5 pixel-art icon sheets (`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `parts`) stay enlarged from the pack (open question no. 7 in `open_questions_de.md`; in `pda_pack01` the game has an Italian leftover "NUOVO" next to the "NEU", as in fr/es).
- Android `textures.zip` for German: not done; no test on a phone.
- The speaker name in the dialogue box cannot be modified (encrypted EBOOT).
