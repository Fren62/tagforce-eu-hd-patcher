# MODIFICHE PER LA VERSIONE POMODORO MISTICO IN FRANCESE

Documento **completo** di tutto cio' che la "Versione Pomodoro Mistico" cambia per il francese: (A) le modifiche **dirette alla ISO**, (B) il **texture pack** (com'e' fatto, cosa contiene, come si compone), (C) le scelte editoriali, (D) cosa e' verificato in gioco e cosa no, (E) come rigenerare tutto.

**Questo file e' generato** da `tools/analysis/write_changes_document.py fr` a partire dai dati reali: confronto byte per byte tra la ISO originale `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` e la ISO corretta `..._definitiva.iso` (`document_changes.py`) e scansione del pack (`document_pack.py`). Gli elenchi riga per riga stanno in `docs/changes_fr/*.csv` (separatore `;`, UTF-8 con BOM, a capo come `⏎`): sono la **lista esatta** di ogni cambiamento. Rigenera tutto dopo ogni modifica.

Per il metodo generale e per le altre lingue: `docs/NEW_LANGUAGE_GUIDE.md`; dettagli tecnici degli script: `TUTORIAL.md`; decisioni: `docs/EDITORIAL_CHOICES.md`; texture neutre/specifiche: `docs/TEXTURE_INVENTORY.md`.

## Indice
- A. Modifiche alla ISO: A1 panoramica · A2 carte · A3 dialoghi · A4 frasi dei duelli · A5 stringhe dell'interfaccia · A6 etichetta Magia/Trappola · A7 file toccati e dettagli tecnici · A8 cosa non si puo' cambiare
- B. Texture pack: B1 provenienza e struttura · B2 immagini delle carte · B3 interfaccia HD (`ui_fr`) · B4 foglio numeri (`card_icon03`) · B5 targa del titolo · B6 textures.ini e composizione · B7 installazione
- C. Scelte editoriali · D. Verifica in gioco · E. Come rigenerare · F. Limiti e punti aperti

---

# A. MODIFICHE ALLA ISO

## A1. Panoramica

La ISO originale **non viene mai modificata**. `tools/corrections/apply_to_iso.py ISO_ORIG ISO_OUT [lingue]` ne crea una copia in cui alcuni archivi `.ehp` sono riscritti. Se un archivio cresce (testo piu' lungo) viene **rimesso in fondo alla ISO** in un nuovo settore e il suo voce nella directory ISO9660 viene riassegnata (`pycdlib`); la ISO `_definitiva` pesa per questo ~909 MB (l'originale ~761 MB). **Lanciarlo sempre senza elenco di lingue (o con tutte)**: con una lingua sola sovrascrive le altre.

| Cosa | Quantita' (derivata dal confronto ISO) | Dove sta il dato | File CSV |
|---|---|---|---|
| Carte con testo cambiato (nome e/o descrizione) | 266 carte (274 campi) | `tools/data/card_corrections_fr.json` da `correzioni/rules_fr.py` | cards.csv |
| Righe di dialogo della storia | 467 righe | `tools/data/dialogue_touchups_fr.json` (+ base) | dialogues.csv |
| Frasi dei duellanti nei duelli | 51 frasi uniche (93 voci in tutti gli archivi) | `tools/data/duel_line_corrections_fr.json` | duel_lines.csv |
| Stringhe dell'interfaccia (aiuti, schede, record, tutorial, menu...) | 254 stringhe uniche (445 voci, 45 archivi) | `correzioni/string_rules_fr.py` + `dati/ui_texts.json` | ui_strings.csv |
| Immagini sostituite dentro la ISO | 6 (etichetta [CARTA MAGIA/TRAPPOLA] della carta grande) | `apply_to_iso.py` (copia `card_spell_trap.gim` della lingua) | iso_images.csv |
| File della ISO toccati (archivi `.ehp`) | 179 | - | touched_files.csv |
| Altre differenze tecniche (offset ricalcolati) | 254 | - | other.csv |

## A2. Testi delle carte

Archivio: `PSP_GAME/USRDIR/duelsys/cardinfo_fra.ehp` (tabelle `CARD_Name_*`, `CARD_Desc_*`, `CARD_Indx_*`). **266 carte** hanno nome e/o descrizione modificati. Si correggono **solo errori oggettivi** (refusi, accenti, apostrofi, spazi, maiuscole incoerenti, concordanze, plurali fissi, residui di altre lingue); nomi ufficiali e terminologia del gioco non si toccano.

Come: ogni carta e' stata letta (it: 2.479 testi, uno per uno; fr: audit contro database ufficiale + lettura). Regole in `tools/corrections/rules_fr.py`: **47 regole globali** (regex applicate a nomi e descrizioni di tutte le carte) e **214 correzioni per carta** (`PER_CARTA`: id, campo, vecchio, nuovo, motivo; il vecchio testo deve esistere esattamente). `generate_card_corrections.py fr CARDINFO` (scrive `card_corrections_{L}.json` partendo dai testi originali) produce il json; `apply_to_iso` lo scrive nella ISO; le immagini HD delle carte toccate si rigenerano (sezione B2).

### Regole globali (tutte)
| modello (regex) | sostituzione | motivo |
|---|---|---|
| \benemi\b | ennemi | refuso |
| \binclu\b | inclus | refuso |
| \bmystèrieuse\b | mystérieuse | accento errato |
| \bmétamrophose\b | métamorphose | refuso |
| \bposible\b | possible | refuso (parola inglese sbagliata) |
| \bpossèdez\b | possédez | accento errato |
| \bposséde\b | possède | accento errato |
| \bquatres\b | quatre | accordo errato |
| \bla jete\b | la jette | refuso |
| \bsacrificiant\b | sacrifiant | refuso |
| \bsacrificiée\b | sacrifiée | refuso |
| \bmonstres renés grâce\b | monstres ressuscités grâce | parola mutilata |
| \b(l\|d\|n\|s\|m\|t\|c\|j\|qu\|jusqu\|lorsqu\|puisqu)' (?=\w) | \1' | spazio dopo l'apostrofo ("l' ATK" -> "l'ATK") |
| \bexcépté\b | excepté | accento errato |
| \bEpée\b | Épée | maiuscola senza accento (altrove "Épée") |
| \bElémentaire\b | Élémentaire | maiuscola senza accento (altrove "Élémentaire") |
| \bEquipement\b | Équipement | maiuscola senza accento |
| \bEchangez\b | Échangez | maiuscola senza accento |
| \bEnergie\b | Énergie | maiuscola senza accento |
| \bEtre\b | Être | maiuscola senza accento |
| \bMalediction\b | Malédiction | accento mancante |
| \bAme\b | Âme | maiuscola senza accento (la forma "âme" ha l'accento) |
| \bAmes\b | Âmes | maiuscola senza accento |
| \bGuardien\b | Gardien | refuso |
| \bHâche\b | Hache | accento errato |
| \bCôntrole\b | Contrôle | accento errato |
| \bInfâmie\b | Infamie | accento errato |
| \bÉxécuteur\b | Exécuteur | accento errato |
| \bBeta\b | Bêta | accento mancante (altrove "Bêta") |
| \bAlpha, (Bêta),? et Gamma meld\b | Alpha, \1 et Gamma | parola inglese "meld" rimasta nel testo |
| \bmilles yeux\b | mille yeux | mille e' invariabile |
| \bMilles Yeux\b | Mille Yeux | mille e' invariabile |
| Invoquer Spécialement avec l'effet de | Invoqué par Invocation Spéciale par l'effet de | formula dei Token |
| Ce Jeton ne peuvent pas être sacrifiés | Ce Jeton ne peut pas être sacrifié | accordo |
| [Ii]nvoquée spécialement | Invoquée par Invocation Spéciale | terminologia |
| A (chaque fois\|ce moment) | À  | maiuscola senza accento |
| succés | succès | accento errato |
| ([Ff])aîtes | aites | refuso |
| dégats | dégâts | accento mancante |
| Oeil | Œil | legatura |
| Emissaire | Émissaire | maiuscola senza accento |
| au (dessus\|dessous) | au- | trattino mancante |
| peut-être (?=activ\|utilis\|invoqu\|offert\|jou\|équip) | peut être  | peut-être (forse) usato al posto di peut être |
| Cartes Magies | Cartes Magie | Magie e' invariabile |
| don't | dont | refuso (inglese) |
| 　 |  | spazio ideografico |
| des les Cartes | des Cartes | doppio articolo |

### Correzioni per carta (tutte)
| id | campo | vecchio | nuovo | motivo |
|---|---|---|---|---|
| 4298 | desc | protége | protège | accento |
| 4397 | desc | Métalmorph | Métalmorphe | nome della carta incompleto |
| 4624 | desc | "La Demoiselle Sonique +"La Belle | "La Demoiselle Sonique" + "La Belle | virgolette mancanti |
| 4703 | desc | utilisee | utilisée | accento |
| 5027 | desc | reputé | réputé | accento |
| 5290 | desc | controlées | contrôlées | accento |
| 5758 | desc | lorqsqu'il | lorsqu'il | refuso |
| 5932 | desc | avdersaire | adversaire | refuso |
| 5964 | desc | détruisez-là | détruisez-la | accento errato sul pronome |
| 5996 | desc | Speciale | Spéciale | accento |
| 6052 | desc | controlée | contrôlée | accento |
| 6158 | desc | Terran | Terrain | refuso |
| 6158 | desc | Positon | Position | refuso |
| 6169 | desc | selectionnés | sélectionnés | accento |
| 6288 | desc | seléctionné | sélectionné | accenti |
| 6424 | desc | votore | votre | refuso |
| 6639 | desc | propriètaire | propriétaire | accento errato |
| 6639 | desc | succés | succès | accento errato |
| 6766 | desc | tour,en | tour, en | spazio mancante dopo la virgola |
| 4154 | desc | Ombre tapis | Ombre tapie | concordanza |
| 4027 | name | Éxodia | Exodia | grammatica/refuso |
| 4087 | desc | machoire | mâchoire | grammatica/refuso |
| 4360 | desc | machoire | mâchoire | grammatica/refuso |
| 4062 | desc | ait été équipé | a été équipé | grammatica/refuso |
| 4232 | desc | les attaques avec une piqûre | l'attaque avec une piqûre | grammatica/refuso |
| 4240 | desc | a décapitée | a décapité | grammatica/refuso |
| 4255 | desc | tel de puissant dragon | tel un puissant dragon | grammatica/refuso |
| 4389 | desc | qu'il n'en à l'air | qu'il n'en a l'air | grammatica/refuso |
| 4423 | desc | cette effet | cet effet | grammatica/refuso |
| 4326 | desc | Activée | Activé | grammatica/refuso |
| 4034 | desc | à coup de poings | à coups de poing | grammatica/refuso |
| 4051 | desc | à coup  | à coups  | grammatica/refuso |
| 4465 | desc | à coup  | à coups  | grammatica/refuso |
| 4517 | desc | à coup  | à coups  | grammatica/refuso |
| 4543 | desc | à coup  | à coups  | grammatica/refuso |
| 4469 | desc | envoyé | envoyée | grammatica/refuso |
| 4491 | desc | Ce montre | Ce monstre | grammatica/refuso |
| 4550 | desc | le corp couvert de canon | le corps couvert de canons | grammatica/refuso |
| 4612 | desc | Cette amphibien | Cet amphibien | grammatica/refuso |
| 4610 | desc | ces crocs | ses crocs | grammatica/refuso |
| 4647 | desc | Cette effet | Cet effet | grammatica/refuso |
| 4627 | desc | sports | sorts | grammatica/refuso |
| 4700 | name | Résurrection of Chakra | Résurrection de Chakra | grammatica/refuso |
| 4715 | desc | Résurrection of Chakra | Résurrection de Chakra | grammatica/refuso |
| 4703 | desc | égale | égal | grammatica/refuso |
| 4706 | desc | égale | égal | grammatica/refuso |
| 4660 | name | salamandra | Salamandra | grammatica/refuso |
| 4660 | desc | Un monstre du FEU | Un monstre FEU | grammatica/refuso |
| 4660 | desc | par 700 | de 700 | grammatica/refuso |
| 4750 | desc | d'une Compteur | d'un Compteur | grammatica/refuso |
| 4750 | desc | La Compteur | Le Compteur | grammatica/refuso |
| 4768 | desc | à détruit | a détruit | grammatica/refuso |
| 4788 | desc | lorsque elle | lorsqu'elle | grammatica/refuso |
| 4589 | desc | Battles Phases | Battle Phases | grammatica/refuso |
| 4804 | desc | 1monstre | monstre | grammatica/refuso |
| 4805 | desc | Invoquez par Invocation Spéciale d'autant de | Invoquez par Invocation Spéciale autant de | grammatica/refuso |
| 4870 | name | Epine | Épine | grammatica/refuso |
| 4888 | desc | L'ATK | l'ATK | grammatica/refuso |
| 4950 | desc | la votre | la vôtre | grammatica/refuso |
| 4965 | desc | Respectifs | respectifs | grammatica/refuso |
| 5004 | desc | des pire | des pires | grammatica/refuso |
| 5018 | desc | jusqu'à qu'il | jusqu'à ce qu'il | grammatica/refuso |
| 5086 | desc | dupés sur | dupés par | grammatica/refuso |
| 5175 | desc | posé | posée | grammatica/refuso |
| 5180 | desc | par l'ATK | de l'ATK | grammatica/refuso |
| 5190 | desc | Diminuer | Diminuez | grammatica/refuso |
| 5227 | desc | faites le attaquer | faites-le attaquer | grammatica/refuso |
| 5238 | desc | invocation Spéciale | Invocation Spéciale | grammatica/refuso |
| 5239 | desc | au même règles | aux mêmes règles | grammatica/refuso |
| 5242 | desc | le "Cathédrale | la "Cathédrale | grammatica/refuso |
| 5264 | desc | retiré du jeu | retirés du jeu | grammatica/refuso |
| 5266 | desc | Le nombre de monstre  | Le nombre de monstres  | grammatica/refuso |
| 5275 | desc | incorrecte | incorrect | grammatica/refuso |
| 5275 | desc | soit Activée | est Activée | grammatica/refuso |
| 5278 | desc | d'entres | d'entre | grammatica/refuso |
| 5290 | desc | 500 points de dommage. | 500 points de dommages. | grammatica/refuso |
| 5292 | desc | avoir invoquer | avoir invoqué | grammatica/refuso |
| 5314 | desc | la retire | la retirent | grammatica/refuso |
| 5380 | desc | durant la Draw Phase sa prochaine tour | durant la Draw Phase de son prochain tour | grammatica/refuso |
| 5386 | name | Cœur de L'Eau | Cœur de l'Eau | grammatica/refuso |
| 5410 | desc | se cette | si cette | grammatica/refuso |
| 5433 | desc | avez pioché dû à | avez piochées en raison de | grammatica/refuso |
| 5429 | desc | retournez les | retournez-les | grammatica/refuso |
| 5452 | name | Éxarion | Exarion | grammatica/refuso |
| 5452 | desc | Cette effet | Cet effet | grammatica/refuso |
| 5440 | desc | détruisez-le(s) | détruisez le(s) | grammatica/refuso |
| 5482 | name | Marionnetiste | Marionnettiste | grammatica/refuso |
| 5526 | desc | lorsque elle | lorsqu'elle | grammatica/refuso |
| 5531 | desc | Life points | Life Points | grammatica/refuso |
| 5560 | name | Interdimensionel | Interdimensionnel | grammatica/refuso |
| 5578 | desc | soufferts | souffert | grammatica/refuso |
| 5608 | desc | S' ils | S'ils | grammatica/refuso |
| 5614 | desc | ont passé | se sont écoulées | grammatica/refuso |
| 5619 | desc | le votre | le vôtre | grammatica/refuso |
| 5623 | desc | Libérer | Libérez | grammatica/refuso |
| 5628 | desc | L'ATK | l'ATK | grammatica/refuso |
| 5665 | desc | devient de 200 | devient 200 | grammatica/refuso |
| 5672 | name | Oeil | Œil | grammatica/refuso |
| 5731 | name | Oeil | Œil | grammatica/refuso |
| 5716 | desc | avez sacrifié | avez sacrifiés | grammatica/refuso |
| 5733 | desc | life Points | Life Points | grammatica/refuso |
| 5744 | desc | ne peut pas offert | ne peut pas être offert | grammatica/refuso |
| 5745 | desc | ne peut pas offert | ne peut pas être offert | grammatica/refuso |
| 5746 | desc | ne peut pas offert | ne peut pas être offert | grammatica/refuso |
| 5758 | desc | ne pouvez seulement activer cette carte que | ne pouvez activer cette carte que | grammatica/refuso |
| 5765 | desc | suivants: | suivants : | grammatica/refuso |
| 5788 | desc | Après que 20 tours soient passés | Après que 20 tours se sont écoulés | grammatica/refuso |
| 5856 | desc | son deck | son Deck | grammatica/refuso |
| 5927 | desc | Défausser | Défaussez | grammatica/refuso |
| 5935 | desc | réduits par le nombre | réduits d'un nombre | grammatica/refuso |
| 5943 | desc | sera augmenté par le chiffre | est augmentée du chiffre | grammatica/refuso |
| 5944 | desc | obtenu | obtenue | grammatica/refuso |
| 5945 | desc | envoyer | envoyez | grammatica/refuso |
| 5963 | name | Epines | Épines | grammatica/refuso |
| 5973 | desc | nombre de monstre  | nombre de monstres  | grammatica/refuso |
| 5974 | name | Eclat | Éclat | grammatica/refuso |
| 5980 | desc | faites en | faites-en | grammatica/refuso |
| 6003 | desc | Chosissez | Choisissez | grammatica/refuso |
| 6004 | desc | envoyer | envoyez | grammatica/refuso |
| 6006 | desc | est posée | est posé | grammatica/refuso |
| 6043 | desc | dommage  | dommages  | grammatica/refuso |
| 6051 | name | Economique | Économique | grammatica/refuso |
| 6063 | desc | dans cette ordre: | dans cet ordre : | grammatica/refuso |
| 6063 | desc | envoyez les | envoyez-les | grammatica/refuso |
| 6066 | desc | Invoquez les | Invoquez-les | grammatica/refuso |
| 6067 | desc | La DEF d'origine | la DEF d'origine | grammatica/refuso |
| 6076 | desc | toute les | toutes les | grammatica/refuso |
| 6078 | name | La Dimension | la Dimension | grammatica/refuso |
| 6078 | desc | par cette effet | par cet effet | grammatica/refuso |
| 6079 | desc | retirez les | retirez-les | grammatica/refuso |
| 6087 | desc | faire L'Invocation | faire l'Invocation | grammatica/refuso |
| 6088 | desc | faire L'Invocation | faire l'Invocation | grammatica/refuso |
| 6090 | desc | 3000 ou plus dommages | 3000 points de dommages ou plus | grammatica/refuso |
| 6113 | desc | exceptée | excepté | grammatica/refuso |
| 6126 | desc | Zones Cartes Monstres | Zones Carte Monstre | grammatica/refuso |
| 6150 | desc | invoquée spécialement depuis votre Main | Invoquée par Invocation Spéciale depuis votre main | grammatica/refuso |
| 6158 | desc | invoqués spécialement | Invoqués par Invocation Spéciale | grammatica/refuso |
| 6208 | name | Etincelle | Étincelle | grammatica/refuso |
| 6220 | name | Etudes | Études | grammatica/refuso |
| 6229 | desc | équivalent  | équivalents  | grammatica/refuso |
| 6235 | desc | ne pouvons plus avant ignorer | ne pouvons plus ignorer | grammatica/refuso |
| 6258 | desc | TERRE. de | TERRE de | grammatica/refuso |
| 6288 | desc | augmente  | augmentent  | grammatica/refuso |
| 6308 | desc | Envoyer | Envoyez | grammatica/refuso |
| 6324 | desc | retiré  | retirés  | grammatica/refuso |
| 6408 | desc | et un 1 monstre | et 1 monstre | grammatica/refuso |
| 6450 | desc | toute les | toutes les | grammatica/refuso |
| 6456 | desc | autant de Carte Magie | autant de Cartes Magie | grammatica/refuso |
| 6469 | desc | l' "Ojama Roi" | l'"Ojama Roi" | grammatica/refuso |
| 6474 | desc | reçu  | reçus  | grammatica/refuso |
| 6483 | desc | pour changez | pour changer | grammatica/refuso |
| 6487 | desc | détruite | détruit | grammatica/refuso |
| 6513 | name | Division! | Division ! | grammatica/refuso |
| 6521 | name | Lancement! | Lancement ! | grammatica/refuso |
| 6133 | name | Montée de Niveau! | Montée de Niveau ! | grammatica/refuso |
| 6530 | name | Eradicateur | Éradicateur | grammatica/refuso |
| 6540 | desc | pour détruisez | pour détruire | grammatica/refuso |
| 6541 | desc | à Deck | à votre Deck | grammatica/refuso |
| 6542 | desc | tous les cartes | toutes les cartes | grammatica/refuso |
| 6544 | name | La Fin de Enkindling | La Fin d'Enkindling | grammatica/refuso |
| 6544 | desc | en faites | en fait | grammatica/refuso |
| 6573 | desc | "Rouages Ancients"de | "Rouages Ancients" de | grammatica/refuso |
| 6637 | desc | que  "Vipère | que "Vipère | grammatica/refuso |
| 6645 | desc | retirée | retirées | grammatica/refuso |
| 6653 | desc | Néo-Space! | Néo-Space ! | grammatica/refuso |
| 6684 | desc | suivants: | suivants : | grammatica/refuso |
| 6639 | desc | respectifs | respectif | grammatica/refuso |
| 4398 | desc | sur le terrain par Invocation spéciale du Deck sur en offrant | sur le Terrain par Invocation Spéciale depuis le Deck en offrant | riscrittura di frase errata |
| 4657 | desc | lorsqu'un monstre de votre adversaire. Changez | lorsqu'un monstre de votre adversaire déclare une attaque. Changez | riscrittura di frase errata |
| 5421 | desc | Lorsque cette carte cible pour l'attaquer, un monstre en Position de Défense face verso sur le Terrain de votre adversaire, l'ATK de cette carte devient 2400 durant ce calcul de dommages seulement. | Lorsque cette carte attaque un monstre en Position de Défense face verso sur le Terrain de votre adversaire, l'ATK de cette carte devient 2400 durant ce calcul des dommages seulement. | riscrittura di frase errata |
| 6307 | desc | Envoyer une carte "Soldat Mécano", "Tireur d'Élite Mécano" et "Fantassin Mécano" de chaque depuis votre Terrain au Cimetière. Exécutez une Invocation Spéciale de "Force Mécano" depuis votre Main ou votre Deck. | Envoyez 1 carte "Soldat Mécano", 1 "Tireur d'Élite Mécano" et 1 "Fantassin Mécano" de votre Terrain au Cimetière. Faites l'Invocation Spéciale de "Force Mécano" depuis votre main ou votre Deck. | riscrittura di frase errata |
| 6410 | desc | peut être invoquée spécialement depuis votre Main après avoir annuler les effets d'une carte contrôlée par votre adversaire à l'aide d'une Cartes Contre-Piège. Si cette carte est invoquée spécialement avec succès | peut être Invoquée par Invocation Spéciale depuis votre main après avoir annulé les effets d'une carte contrôlée par votre adversaire à l'aide d'une Carte Contre-Piège. Si cette carte est Invoquée par Invocation Spéciale avec succès | riscrittura di frase errata |
| 6410 | desc | par 1500 | de 1500 | riscrittura di frase errata |
| 6410 | desc | puis invoquez-la spécialement | puis faites-en l'Invocation Spéciale | riscrittura di frase errata |
| 6287 | desc | et envoyé au Cimetière, vous pouvez sacrifier 500 Life Points pour l'invoquer spécialement pendant | et envoyée au Cimetière, vous pouvez payer 500 Life Points pour en faire l'Invocation Spéciale pendant | riscrittura di frase errata |
| 6302 | desc | vous pouvez Invoquer Spécialement de votre Main un monstre | vous pouvez faire l'Invocation Spéciale depuis votre main d'un monstre | riscrittura di frase errata |
| 6380 | desc | pour Invoquer Spécialement cette carte de votre Main ou Cimetière | pour faire l'Invocation Spéciale de cette carte depuis votre main ou votre Cimetière | riscrittura di frase errata |
| 6368 | desc | vous pouvez retiré du jeu | vous pouvez retirer du jeu | riscrittura di frase errata |
| 6368 | desc | un nombre de Carte Magie et Piège égal au nombre de cartes qui vous avez retiré | un nombre de Cartes Magie et Piège égal au nombre de cartes que vous avez retirées | riscrittura di frase errata |
| 6550 | desc | est invoquée normalement ou spécialement avec succès | est Invoquée par Invocation Normale ou Spéciale avec succès | grammatica/refuso |
| 6583 | desc | depuis votre deck | depuis votre Deck | grammatica/refuso |
| 6616 | desc | au "Magicienne Blanche Pikeru" | à "Magicienne Blanche Pikeru" | grammatica/refuso |
| 6636 | desc | Vous pouvez ajouter une carte "Kuriboh" ou "Kuriboh Ailé" à votre Main ou les invoquer spécialement sur votre Terrain depuis votre Deck. | Vous pouvez ajouter 1 carte "Kuriboh" ou "Kuriboh Ailé" de votre Deck à votre main, ou en faire l'Invocation Spéciale sur votre Terrain. | grammatica/refuso |
| 6638 | desc | ne peut pas offert en Sacrifice | ne peut pas être offert en Sacrifice | grammatica/refuso |
| 6638 | desc | a été invoqué spécialement | a été Invoqué par Invocation Spéciale | grammatica/refuso |
| 6648 | desc | peut être invoquée en sacrifiant la carte "Duo Hélios Megistus" posée sur votre Terrain | peut être Invoquée par Invocation Spéciale en sacrifiant "Duo Hélios Megistus" sur votre Terrain | grammatica/refuso |
| 6648 | desc | Cartes Monstre retirée du jeu x 300 | Cartes Monstre retirées du jeu x 300 | grammatica/refuso |
| 6648 | desc | détruite pendant une bataille puis est envoyée au Cimetière, elle est automatiquement invoquée spécialement à la End Phase et son ATK et DEF sont augmentées de 500 points | détruite à l'issue d'un combat et envoyée au Cimetière, elle est Invoquée par Invocation Spéciale durant la End Phase et son ATK et sa DEF augmentent de 500 points | grammatica/refuso |
| 6648 | desc | Si des Cartes Monstre sont sur le Terrain de votre adversaire, cette carte peut attaquer encore une fois. | Si des monstres sont sur le Terrain de votre adversaire, cette carte peut attaquer une fois de plus. | grammatica/refuso |
| 6654 | desc | vous pouvez invoquer spécialement 2 | vous pouvez faire l'Invocation Spéciale de 2 | grammatica/refuso |
| 6654 | desc | il a été invoqué. | il a été Invoqué. | grammatica/refuso |
| 6659 | desc | sur votre terrain qui inclut | sur votre Terrain qui inclut | grammatica/refuso |
| 6659 | desc | (exceptée cette carte) | (excepté cette carte) | grammatica/refuso |
| 6661 | desc | (exceptée cette carte) | (excepté cette carte) | grammatica/refuso |
| 6675 | desc | cette carte: | cette carte : | grammatica/refuso |
| 6685 | desc | Homme-Batterie D:  | Homme-Batterie D :  | grammatica/refuso |
| 6685 | desc | cible cette 1 carte | cible cette carte | grammatica/refuso |
| 6685 | desc | Homme-Batterie C:  | Homme-Batterie C :  | grammatica/refuso |
| 6685 | desc | Homme-Batterie AA:  | Homme-Batterie AA :  | grammatica/refuso |
| 6697 | desc | invocation Spéciale | Invocation Spéciale | grammatica/refuso |
| 6720 | desc | doit être de monstre VENT | doit être un monstre VENT | grammatica/refuso |
| 6736 | desc | l'invocation Spéciale | l'Invocation Spéciale | grammatica/refuso |
| 6759 | desc | nombre de monstres nécessaire | nombre de monstres nécessaires | grammatica/refuso |
| 6761 | desc | Équipement, et équipez-la | Équipement. Équipez-la | grammatica/refuso |
| 6765 | desc | ne peut qu'être Invoquée par Invocation Spéciale depuis | ne peut être Invoquée par Invocation Spéciale que depuis | grammatica/refuso |
| 6766 | desc | ne peut qu'être Invoquée par Invocation Spéciale depuis | ne peut être Invoquée par Invocation Spéciale que depuis | grammatica/refuso |
| 6767 | desc | ne peut qu'être Invoquée par Invocation Spéciale depuis | ne peut être Invoquée par Invocation Spéciale que depuis | grammatica/refuso |
| 6809 | desc | de 2000 points; si | de 2000 points ; si | grammatica/refuso |
| 6815 | desc | Cette carte peut-être considérée | Cette carte peut être considérée | grammatica/refuso |
| 6815 | desc | Invoquez Spécialement cette carte sur votre Terrain | faites l'Invocation Spéciale de cette carte sur votre Terrain | grammatica/refuso |
| 6815 | desc | Invocation Retournement | Invocation Flip | grammatica/refuso |
| 6815 | desc | un nombre de Carte Magie | un nombre de Cartes Magie | grammatica/refuso |
| 6822 | desc | ou soit face verso | soit face verso | grammatica/refuso |
| 6957 | desc | "'Gazelle | "Gazelle | grammatica/refuso |

### Elenco completo delle carte cambiate
**Confronto completo originale -> nuovo con le parole cambiate evidenziate: `docs/changes_fr/cards_diff.md`** (tutte le 274 voci). Dati grezzi: `docs/changes_fr/cards.csv`. Prime 40 righe:

| id | nome originale | campo | originale | nuovo |
|---|---|---|---|---|
| 4022 | Magicien du Temps | desc | Prenez une pièce et jouez à pile ou face. Si vous gagnez, tous les monstres sur le Terrain de votre adversaire sont détruits. Si vous perdez, tous les monstres sur votre Terrain sont détruits et vous recevez des dommages égaux à la moitié des points d'ATK de tous les monstres détruits. Cet effet ne peut-être utilisé qu'une fois par tour, et uniquement durant votre Main Phase. | Prenez une pièce et jouez à pile ou face. Si vous gagnez, tous les monstres sur le Terrain de votre adversaire sont détruits. Si vous perdez, tous les monstres sur votre Terrain sont détruits et vous recevez des dommages égaux à la moitié des points d'ATK de tous les monstres détruits. Cet effet ne peut être utilisé qu'une fois par tour, et uniquement durant votre Main Phase. |
| 4027 | Éxodia l'Interdit | name | Éxodia l'Interdit | Exodia l'Interdit |
| 4034 | Ogre de Pierre Grotto N°1 | desc | Protégé par un solide corps de pierre, ce monstre fracasse les os à coup de poings. | Protégé par un solide corps de pierre, ce monstre fracasse les os à coups de poing. |
| 4051 | Héros Oscillo N°2 | desc | Cette créature électrocute ses adversaires à coup d'éclairs. | Cette créature électrocute ses adversaires à coups d'éclairs. |
| 4062 | Larve de Papillon | desc | Ce monstre ne peut être Invoqué que par Invocation Spéciale en sacrifiant "Petit Papillon" à partir de votre 2ème tour après que "Petit Papillon" ait été équipé de "Cocon d'Évolution". | Ce monstre ne peut être Invoqué que par Invocation Spéciale en sacrifiant "Petit Papillon" à partir de votre 2ème tour après que "Petit Papillon" a été équipé de "Cocon d'Évolution". |
| 4087 | Dragon Rampant N°2 | desc | Ce puissant dragon possède une machoire qui peut presque tout réduire en poussière. | Ce puissant dragon possède une mâchoire qui peut presque tout réduire en poussière. |
| 4089 | Château des Illusions | desc | FLIP: Augmentez de 200 points l'ATK et la DEF de tous les monstres de Type Zombie face recto sur le Terrain. Tant que cette carte reste face recto sur le Terrain, l'ATK et la DEF des monstres de Type Zombie continuent d'augmenter de 200 points supplémentaires durant chacune de vos Standby Phases. Cet effet continuera jusqu'à votre 4ème tour inclu suivant le tour de son activation. | FLIP: Augmentez de 200 points l'ATK et la DEF de tous les monstres de Type Zombie face recto sur le Terrain. Tant que cette carte reste face recto sur le Terrain, l'ATK et la DEF des monstres de Type Zombie continuent d'augmenter de 200 points supplémentaires durant chacune de vos Standby Phases. Cet effet continuera jusqu'à votre 4ème tour inclus suivant le tour de son activation. |
| 4105 | Roi des Fantômes | desc | Tant que "Château des Illusions" reste face recto sur le Terrain, augmentez l'ATK et la DEF de cette carte de 100 points. L'ATK et la DEF de cette carte continuent d'augmenter de 100 points supplémentaires durant chacune de vos Standby Phases. Cet effet continuera jusqu'à votre 4ème tour inclu suivant le tour de son activation. | Tant que "Château des Illusions" reste face recto sur le Terrain, augmentez l'ATK et la DEF de cette carte de 100 points. L'ATK et la DEF de cette carte continuent d'augmenter de 100 points supplémentaires durant chacune de vos Standby Phases. Cet effet continuera jusqu'à votre 4ème tour inclus suivant le tour de son activation. |
| 4154 | L'Ombre qui contrôle les ténèbres | desc | Ombre tapis dans le noir, qui paralyse ses adversaires et les rend inoffensifs. | Ombre tapie dans le noir, qui paralyse ses adversaires et les rend inoffensifs. |
| 4208 | Marmotte Archdémon de L'Infâmie | name | Marmotte Archdémon de L'Infâmie | Marmotte Archdémon de L'Infamie |
| 4232 | Crâne acharné | desc | Rapide et redoutable, ce monstre saisit ses victimes avec ses pinces et les attaques avec une piqûre venimeuse. | Rapide et redoutable, ce monstre saisit ses victimes avec ses pinces et l'attaque avec une piqûre venimeuse. |
| 4240 | La Belle Chasseur de Prime | desc | Une créature vicieuse qui a décapitée plus d'un ennemi. | Une créature vicieuse qui a décapité plus d'un ennemi. |
| 4249 | Elémentaire de l'Eau | name | Elémentaire de l'Eau | Élémentaire de l'Eau |
| 4255 | Omotics Aquatique | desc | Elle manipule l'eau de sa jarre tel de puissant dragon. | Elle manipule l'eau de sa jarre tel un puissant dragon. |
| 4298 | Kappa Psychique | desc | Un monstre amphibien doté de nombreux pouvoirs qui le protége des attaques ennemies. | Un monstre amphibien doté de nombreux pouvoirs qui le protège des attaques ennemies. |
| 4324 | Égotiste Élégant | desc | Vous ne pouvez activer cette carte que lorsqu'il y a 1 ou plusieurs "Dame Harpie" face recto sur le Terrain. Faites l' Invocation Spéciale d'1 "Dame Harpie" ou d'1 "Sœurs de Harpie" depuis votre main ou votre Deck. | Vous ne pouvez activer cette carte que lorsqu'il y a 1 ou plusieurs "Dame Harpie" face recto sur le Terrain. Faites l'Invocation Spéciale d'1 "Dame Harpie" ou d'1 "Sœurs de Harpie" depuis votre main ou votre Deck. |
| 4326 | Stop Défense | desc | Sélectionnez 1 des monstres de votre adversaire et passez-le en Position d'Attaque. Si la carte est face verso, retournez-la face recto. Si la carte a un Effet Flip, celui-ci est immédiatement Activée. | Sélectionnez 1 des monstres de votre adversaire et passez-le en Position d'Attaque. Si la carte est face verso, retournez-la face recto. Si la carte a un Effet Flip, celui-ci est immédiatement Activé. |
| 4360 | Animal en peluche | desc | Il ressemble à une peluche inoffensive mais sa fermeture éclair cache une redoutable machoire. | Il ressemble à une peluche inoffensive mais sa fermeture éclair cache une redoutable mâchoire. |
| 4389 | Dragon Perroquet | desc | Ce dragon de dessin animé est plus dangereux qu'il n'en à l'air. | Ce dragon de dessin animé est plus dangereux qu'il n'en a l'air. |
| 4397 | Zoa | desc | Un monstre dont le plein potentiel est atteint lorsqu'il est habillé avec "Métalmorph". | Un monstre dont le plein potentiel est atteint lorsqu'il est habillé avec "Métalmorphe". |
| 4398 | Métalzoa | desc | Invoquez ce monstre sur le terrain par Invocation spéciale du Deck sur en offrant "Zoa" équipée de "Métalmorphe" en sacrifice. | Invoquez ce monstre sur le Terrain par Invocation Spéciale depuis le Deck en offrant "Zoa" équipée de "Métalmorphe" en sacrifice. |
| 4423 | Jongleur Explosif | desc | Vous ne pouvez Activer cette effet que durant votre Standby Phase. Sélectionnez et détruisez 2 monstres face recto avec une ATK de 1000 points ou moins en sacrifiant cette carte face recto. | Vous ne pouvez Activer cet effet que durant votre Standby Phase. Sélectionnez et détruisez 2 monstres face recto avec une ATK de 1000 points ou moins en sacrifiant cette carte face recto. |
| 4430 | Dragon Céleste | desc | De dangereuses lames se cachent sous les quatres ailes de ce dragon volant. | De dangereuses lames se cachent sous les quatre ailes de ce dragon volant. |
| 4450 | Turu-Purun | desc | Monstre étrange à un œil capable de transpercer son enemi d'un seul coup de lance. | Monstre étrange à un œil capable de transpercer son ennemi d'un seul coup de lance. |
| 4465 | Bête au Fil Tendu | desc | Cette créature attaque à coup d'ondes électromagnétiques. | Cette créature attaque à coups d'ondes électromagnétiques. |
| 4469 | Serpent Électrique | desc | Lorsque cette carte est envoyé directement de votre main au Cimetière par l'effet d'une carte de votre adversaire, piochez 2 cartes de votre Deck. | Lorsque cette carte est envoyée directement de votre main au Cimetière par l'effet d'une carte de votre adversaire, piochez 2 cartes de votre Deck. |
| 4491 | Korogashi | desc | Ce montre forme une énorme boule de fumier pour écraser son adversaire. | Ce monstre forme une énorme boule de fumier pour écraser son adversaire. |
| 4517 | Soldat Haricot | desc | Cette plante guerrière attaque à coup de graines et d'épée. | Cette plante guerrière attaque à coups de graines et d'épée. |
| 4535 | Cérébrus de Flammes | desc | Connu de beaucoup comme "L'Éxécuteur Incandescent", ce monstre est capable de réduire ses ennemis en cendre. | Connu de beaucoup comme "L'Exécuteur Incandescent", ce monstre est capable de réduire ses ennemis en cendre. |
| 4543 | Méga Thunderball | desc | Il roule sur le sol et attaque ses ennemis à coup d'éclairs. | Il roule sur le sol et attaque ses ennemis à coups d'éclairs. |
| 4550 | Canon Dharma | desc | Créature monstrueuse dont le corp couvert de canon ne rate jamais sa cible. | Créature monstrueuse dont le corps couvert de canons ne rate jamais sa cible. |
| 4562 | L'Ame errante | name | L'Ame errante | L'Âme errante |
| 4589 | Bulletin Météo | desc | FLIP: Détruisez toutes les "Épées de Révélation de la Lumière" face recto sur le Terrain de votre adversaire. Si "Épées de Révélation de la Lumière" est détruite, vous pouvez réaliser deux Battles Phases durant ce tour (ou durant votre prochain tour, si l'effet est Activé durant le tour de votre adversaire). | FLIP: Détruisez toutes les "Épées de Révélation de la Lumière" face recto sur le Terrain de votre adversaire. Si "Épées de Révélation de la Lumière" est détruite, vous pouvez réaliser deux Battle Phases durant ce tour (ou durant votre prochain tour, si l'effet est Activé durant le tour de votre adversaire). |
| 4610 | Marmotte obèse de l'Infamie | desc | Souris des champs mal élevée prête à enfoncer ces crocs dans n'importe quoi. | Souris des champs mal élevée prête à enfoncer ses crocs dans n'importe quoi. |
| 4612 | Twin Long Rods N°2 | desc | Cette amphibien utilise ses deux queues comme des fouets. | Cet amphibien utilise ses deux queues comme des fouets. |
| 4624 | Guerrier de la Tradition | desc | "La Demoiselle Sonique +"La Belle Chasseur de Prime" | "La Demoiselle Sonique" + "La Belle Chasseur de Prime" |
| 4627 | Chevalier Succubus | desc | Mage guerrière adepte de la création de sports à vous faire froid dans le dos. | Mage guerrière adepte de la création de sorts à vous faire froid dans le dos. |
| 4637 | Vierge de la Lumière de Lune | desc | Cette sorcière bénie par la lumière lunaire posséde un pouvoir dépassant l'entendement des mortels. | Cette sorcière bénie par la lumière lunaire possède un pouvoir dépassant l'entendement des mortels. |
| 4647 | Usurpatrice du Trône | desc | FLIP: Sélectionnez 1 monstre de votre adversaire et échangez-le avec celui-ci. Cette effet ne peut pas être Activé durant la Battle Phase. | FLIP: Sélectionnez 1 monstre de votre adversaire et échangez-le avec celui-ci. Cet effet ne peut pas être Activé durant la Battle Phase. |
| 4657 | Kunai avec chaîne | desc | Vous pouvez activer 1 ou les 2 effets suivants.⏎●Vous pouvez activer cette carte lorsqu'un monstre de votre adversaire. Changez la position de bataille du monstre attaquant en Position de Défense.⏎●Après activation, cette carte est considérée comme une Carte d'Équipement et augmente l'ATK du monstre équipé de 500 points. Vous pouvez équiper 1 monstre de votre Terrain avec cette carte. | Vous pouvez activer 1 ou les 2 effets suivants.⏎●Vous pouvez activer cette carte lorsqu'un monstre de votre adversaire déclare une attaque. Changez la position de bataille du monstre attaquant en Position de Défense.⏎●Après activation, cette carte est considérée comme une Carte d'Équipement et augmente l'ATK du monstre équipé de 500 points. Vous pouvez équiper 1 monstre de votre Terrain avec cette carte. |

(... altre 234 righe nel CSV)

## A3. Dialoghi della storia

Archivi: `script/stNN_<scena>_f.ehp`, ogni scena e' una coppia di membri `...If.bin` (offset in caratteri UTF-16) e `...Lf.bin` (stringhe UTF-16LE chiuse da NUL, alcune compresse in gzip). **467 righe** cambiate (comprese quelle che **ereditano** la correzione perche' hanno lo stesso testo originale e lo stesso giapponese di una riga corretta).

Flusso: lettura riga per riga confrontata con inglese e giapponese -> ritocchi in `tools/data/dialogue_touchups_fr.json` (`esatte` e `parti`) -> `build_dialogues.py fr` -> `dialogue_corrections_fr.json` -> `apply_to_iso.py`. Regole automatiche di impaginazione in `build_dialogues.py`: spazio non separabile prima di `! ? : ;` anche dopo `》` (regola `FR_PUNT`), spazio dopo i segnaposto, "Mode histoire" -> "Mode aventure". Vincoli del box: ~46 caratteri per riga, max 3 righe (un segnaposto vale ~6 caratteri): `apply_to_iso` segnala le righe che potrebbero non starci.

### Ritocchi di rilettura: `esatte` (16) — frase intera originale -> frase nuova
| originale | nuovo |
|---|---|
| Avec plaisir, Doyen 《C038_4》... | Avec plaisir, Chancelier 《C038_4》... |
| Si le Doyen Sheppard⏎voulait bien que je revienne... | Si le Chancelier Sheppard⏎voulait bien que je revienne... |
| Doyen, que faites-vous là ?!? | Chancelier, que faites-vous là ?!? |
| Doyen, vous connaissez l'alchimie ? | Chancelier, vous connaissez l'alchimie ? |
| À partir d'aujourd'hui, appelez-moi⏎Doyen Crowler ! | À partir d'aujourd'hui, appelez-moi⏎Chancelier Crowler ! |
| Doyen Crowler... | Chancelier Crowler... |
| Doyen Temporaire Crowler. | Chancelier Temporaire Crowler. |
| Doyen Sheppard ! | Chancelier Sheppard ! |
| Je sais, Doyen !⏎Du respect pour son adversaire ! | Je sais, Chancelier !⏎Du respect pour son adversaire ! |
| Ha ha ha !⏎Elle est bonne, Doyen ! | Ha ha ha !⏎Elle est bonne, Chancelier ! |
| Je suis le Doyen《C038_4》. | Je suis le Chancelier《C038_4》. |
| Si tu reçois un e-mail de félicitations de⏎la part du doyen... | Si tu reçois un e-mail de félicitations de⏎la part du chancelier... |
| Ces derniers reçoivent un e-mail de⏎félicitations de la part du doyen. | Ces derniers reçoivent un e-mail de⏎félicitations de la part du chancelier. |
| Tu veux écouter l'histoire⏎du Doyen ? | Tu veux écouter l'histoire⏎du Chancelier ? |
| Le terminal de l'Arène de Duel ne répond plus! | Le terminal de l'Arène ne répond plus ! |
| Hé, que penses-tu de ça ! | Tiens, utilise cette tenue de servante ! |

### Ritocchi di rilettura: `parti` (156) — sostituzioni di testo applicate a ogni riga (in ordine)
| vecchio | nuovo |
|---|---|
| Utilise-là | Utilise-la |
| C'est toi qui veut, alors | C'est toi qui veux, alors |
| préfèrerais avoir volley-ball | préférerais jouer au volley-ball |
| Quel le Duel | Que le Duel |
| Quel Carte Magie reste | Quelle Carte Magie reste |
| Qui sait , Le futur | Qui sait, le futur |
| Ballade-toi un peu | Balade-toi un peu |
| Pain au nouilles | Pain aux nouilles |
| Pain aux ravolis | Pain aux raviolis |
| Pain au durion | Pain au durian |
| Sandwich au truffes | Sandwich aux truffes |
| Je sais comment ce que tu ressens | Je sais ce que tu ressens |
| a cru que volais | a cru que je volais |
| Ça peut semble | Ça peut sembler |
| ça peut semble | ça peut sembler |
| Tu revoies | Tu revois |
| attends que 《C006_2》 voit ça | attends que 《C006_2》 voie ça |
| Huh ? | Hein ? |
| Huh !? | Hein !? |
| tu n'as pas super bien agit | tu n'as pas super bien agi |
| Quoi que. On ne sait | Quoique. On ne sait |
| Hmm... Pas même. | Hmm... Pas mal. |
| règles: limites | règles : limites |
| aujourd' hui | aujourd'hui |
| pâte d'haricot | pâte de haricots |
| aux oeufs | aux œufs |
| à l'oeuf | à l'œuf |
| c' est une promesse | c'est une promesse |
| pas très bien piocher | pas très bien pioché |
| Quelque chose à dû clocher | Quelque chose a dû clocher |
| J'ai suis muté | Je suis muté |
| Réouverture à 2:00 | Réouverture à 14:00 |
| déjà partenaire ! | déjà partenaires ! |
| déjà partenaire, non? | déjà partenaires, non ? |
| déjà partenaire. | déjà partenaires. |
| on est partenaire, hein | on est partenaires, hein |
| tout mes LP | tous mes LP |
| heu-reux | heureux |
| en communs | en commun |
| sur mon coeur | sur mon cœur |
| Je dit des | Je dis des |
| Tu es décidé d'être | Tu es décidé à être |
| prépare toi | prépare-toi |
| préfèrerais | préférerais |
| J'aurais pas du | J'aurais pas dû |
| m'as punis | m'as puni |
| Hein? Un | Hein ? Un |
| nos style à | nos styles à |
| Slifer Rouge ensembles | Slifer Rouge ensemble |
| Non, Je te remercie | Non, je te remercie |
| Qu'est ce que tu en dis | Qu'est-ce que tu en dis |
| me rends plus fort | me rend plus fort |
| Ton habilité | Ton habileté |
| Quoi?! Tu n'as jamais | Quoi ?! Tu n'as jamais |
| aucun doute! | aucun doute ! |
| C'et parti | C'est parti |
| Et bien, tu es un gars | Eh bien, tu es un gars |
| jusqu'a que | jusqu'à ce que |
| Y-a t'il des élèves | Y a-t-il des élèves |
| bien trop d'erreur. | bien trop d'erreurs. |
| J'ai failli oublié | J'ai failli oublier |
| qu'on est partenaire ! | qu'on est partenaires ! |
| Veux- tu | Veux-tu |
| l'ombre du chance | l'ombre d'une chance |
| Si tu m'en juge | Si tu m'en juges |
| me rappeler d'un Slifer | me rappeler un Slifer |
| Je n'ai pas de tête... Hi hi | Je n'ai pas bonne mémoire... Hi hi |
| une bonne fois pour toute. | une bonne fois pour toutes. |
| Qu'est-ce que ce robot ? | Qu'est-ce que c'est que ce robot ? |
| Les phase finale | La phase finale |
| J'accepte, Doyen. | J'accepte, Chancelier. |
| Quel chance d'avoir | Quelle chance d'avoir |
| Pauvre petites poules | Pauvres petites poules |
| amazone.... | amazone... |
| Aidez moi | Aidez-moi |
| Mon frère est moi participons | Mon frère et moi participons |
| cette fille-à. | cette fille-là. |
| tes yeux vacillent | tes yeux vacille |
| Égalité! Minable | Égalité ! Minable |
|   《 |  《 |
| 》   | 》  |
| paquet  ! | paquet ! |
| c'est  ? | c'est ? |
| jetais  pas | jetais pas |
| Je  dois | Je dois |
| alors,  c'est | alors, c'est |
| un  bail | un bail |
| le  directeur | le directeur |
| son  loisir | son loisir |
| Je suis  ⏎ | Je suis⏎ |
| d' 《 | d'《 |
| toi 《PLAYER》 , | toi 《PLAYER》, |
| parait | paraît |
| je pense que qu'il est temps | je pense qu'il est temps |
| Peut-elle faire une bonne duelliste ? | Peut-elle devenir une bonne duelliste ? |
| on se retrouvera Syrus ! | on se retrouvera, Syrus ! |
| Va-y, 《PLAYER》 | Vas-y, 《PLAYER》 |
| Qu'est ce que c'est, Professeur | Qu'est-ce que c'est, Professeur |
| Et il a déjà faux !!! | Et il a déjà tout faux !!! |
| C'est comme un baiser...! | C'est comme un baiser... ! |
| Bon, et bien...! | Bon, eh bien... ! |
| Carte Magie Contigüe | Carte Magie Contiguë |
| choisis "Mode histoire" | choisis "Mode aventure" |
| sélectionnes⏎Mode histoire | sélectionnes⏎Mode aventure |
| Hé bien | Eh bien |
| Um, je n'aime pas vraiment ça | Euh, je n'aime pas vraiment ça |
| te dépêcher ... | te dépêcher... |
| j'ai eu aujourd'hui | j'ai eus aujourd'hui |
| tu me⏎regarde comme ça | tu me⏎regardes comme ça |
| pourraient pas dans un tel taudis | pourraient pas vivre dans un tel taudis |
| Vous n'avez pas passé déjà une année ici | Vous n'avez pas déjà passé une année ici |
| C'est juste, que c'est à toi | C'est juste que c'est à toi |
| mènera nulle pas | mènera nulle part |
| sert ⏎à quelque chose.... | sert ⏎à quelque chose... |
| à Slifer.... | à Slifer... |
| Um, assez de blagues | Euh, assez de blagues |
| à ５0 % | à 50 % |
| à ８0 % | à 80 % |
| Uh-uh. Pas terrible | Hmm. Pas terrible |
| Huh, pas mal | Hé, pas mal |
| Ungh...Pas mal | Ungh... Pas mal |
| Ce corps...ne va pas tenir le coup bien⏎longtemps...Il faut que je me dépêche... | Ce corps... ne va pas tenir le coup bien⏎longtemps... Il faut que je me dépêche... |
| Tu...Tu peux comprendre | Tu... Tu peux comprendre |
| Huh... ? | Hein... ? |
| Um... | Euh... |
| Umm... Eh bien... | Euh... Eh bien... |
| Um, on est déjà partenaires | Euh, on est déjà partenaires |
| n'a pas suffit | n'a pas suffi |
| Je me suis fais⏎avoir | Je me suis fait⏎avoir |
| pas grand chose | pas grand-chose |
| Je me suis fait bien fait avoir | Je me suis bien fait avoir |
| fais moi signe | fais-moi signe |
| appelle moi | appelle-moi |
| Duel ?Duel ? | Duel ? Duel ? |
| Humm, et bien | Humm, eh bien |
| blond(ou la fille ?) | blond (ou la fille ?) |
| Ne m'oublie pas...même si | Ne m'oublie pas... même si |
| J'ai...J'ai gagné | J'ai... J'ai gagné |
| Râ Jaune | Ra Jaune |
| je suis .《C120_1》 | je suis 《C120_1》 |
| 《PLAYER》 ,c'est ça ? | 《PLAYER》, c'est ça ? |
| Comment rendre des cartes⏎Comment pouvoir louer | Comment rendre des cartes ?⏎Comment pouvoir louer |
| compétences⏎des champion. | compétences⏎des champions. |
| Q... Quoi...? | Q... Quoi... ? |
| Oui⏎ Non | Oui⏎Non |
| Um, euh, battons-nous | Hum, euh, battons-nous |
| Uh... | Heu... |
| Um, on peut commencer | Euh, on peut commencer |
| Mon père a une société qui fabrique de la⏎sauce épicée. | Mon père possède une⏎distillerie de saké. |
| Il m'en a envoyé avec | Il m'a envoyé du shochu avec |
| En bikini | En tenue de servante |
| en bikini | en tenue de servante |
| de carillonner comme | de m'interrompre comme |
| que tu t'en⏎débarrasses de quelques- | que tu te⏎sois débarrassé de quelques- |
| te rebattre en⏎Duel contre moi ! | te rebattre en⏎Duel contre moi ? |
| on est ⏎partenaire qu'on | on est ⏎partenaires qu'on |

### Elenco completo delle righe
**Confronto completo originale -> nuovo (con inglese e giapponese): `docs/changes_fr/dialogues_diff.md`** (tutte le 467 righe). Dati grezzi: `docs/changes_fr/dialogues.csv`. Prime 30:

| id | originale | nuovo | inglese |
|---|---|---|---|
| st01_t01/Iso001E#11 | Qu'est-ce qui vous dit que je ne⏎jetais  pas mes cartes, hein ? | Qu'est-ce qui vous dit que je ne⏎jetais pas mes cartes, hein ? | Who says I wasn't throwing⏎away my own cards, huh? |
| st01_t01/Iso001E#32 | Hé...  《C005_2》...⏎Prépare-toi à perdre ! | Hé... 《C005_2》...⏎Prépare-toi à perdre ! | Heh... 《C005_2》...⏎Prepare to lose! |
| st01_t01/Iso003E#3 | Pour Ra Jaune,⏎《C006_2》... 《C006_3》! | Pour Ra Jaune,⏎《C006_2》... 《C006_3》 ! | From Ra Yellow,⏎《C006_3》...《C006_2》! |
| st01_t01/Iso005E#15 | Fais honneur au nom⏎ 《C005_2》, parce que... | Fais honneur au nom⏎《C005_2》, parce que... | Don't let the 《C005_2》⏎name down. Because... |
| st01_t01/Iso005E#22 | Avec plaisir, Doyen 《C038_4》... | Avec plaisir, Chancelier 《C038_4》... | With pleasure,⏎Chancellor 《C038_4》... |
| st01_t01/Iso005E#51 | Tu as déjà battu  《C005_2》,⏎et tu peux le refaire ! | Tu as déjà battu 《C005_2》,⏎et tu peux le refaire ! | You beat 《C005_2》 before,⏎and you'll do it again! |
| st01_t01/Iso005E#60 | Fais honneur au nom⏎ 《C005_2》 ! | Fais honneur au nom⏎《C005_2》 ! | Don't hurt the 《C005_2》⏎name! |
| st01_t01/Iso005E#61 | Quel le Duel commence, 《C001_3》! | Que le Duel commence, 《C001_3》 ! | Here I go, 《C001_3》! |
| st01_t01/Iso005E#63 | C'est parti,  《C005_2》 ! | C'est parti, 《C005_2》 ! | Bring it on, 《C005_2》! |
| st01_t01/Iso005E#88 | 《C005_3》! | 《C005_3》 ! | 《C005_3》! |
| st01_t01/Iso005E#90 | Je n'ai pas le temps pour tes⏎foutaises, 《C005_3》! | Je n'ai pas le temps pour tes⏎foutaises, 《C005_3》 ! | I don't have time for your⏎garbage, 《C005_3》! |
| st01_t01/Iso005E#91 | Viens, 《C032_3》! | Viens, 《C032_3》 ! | Let's go, 《C032_3》! |
| st01_t01/Iso005E#92 | Bien, je pense que qu'il est temps de⏎se dire au revoir ! | Bien, je pense qu'il est temps de⏎se dire au revoir ! | Well, I guess this is⏎goodbye! |
| st01_t01/Iso005E#93 | Écris-nous,⏎《C005_2》! | Écris-nous,⏎《C005_2》 ! | Don't forget to write,⏎《C005_2》! |
| st01_t01/Iso005E#96 | Si le Doyen Sheppard⏎voulait bien que je revienne... | Si le Chancelier Sheppard⏎voulait bien que je revienne... | If Chancellor 《C038_4》⏎will have me back... |
| st01_t01/Iso007E#9 | 《C004_3》!⏎Pile à l'heure ! | 《C004_3》 !⏎Pile à l'heure ! | 《C004_3》!⏎Great timing! |
| st01_t01/Iso007E#67 | Bonne chance,⏎《C026_2》!! | Bonne chance,⏎《C026_2》 !! | Good luck,⏎《C026_2》!! |
| st01_t01/Iso007E#70 | 《PLAYER》 contre 《C026_1》! | 《PLAYER》 contre 《C026_1》 ! | It's 《PLAYER》ｖｓ《C026_1》! |
| st01_t01/Iso007E#83 | Exact,⏎《C026_2》! | Exact,⏎《C026_2》 ! | You go,⏎《C026_2》! |
| st01_t01/Iso007E#92 | Tu es formidable,⏎《C026_2》! | Tu es formidable,⏎《C026_2》 ! | You're awesome,⏎《C026_2》! |
| st01_t01/Iso007E#96 | 《PLAYER》a mordu la poussière,⏎qui est le prochain ? | 《PLAYER》 a mordu la poussière,⏎qui est le prochain ? | 《PLAYER》 is eating dirt,⏎so who's next to face her? |
| st01_t01/Iso007E#111 | Tu es formidable,⏎《C026_2》! | Tu es formidable,⏎《C026_2》 ! | You're awesome,⏎《C026_2》! |
| st01_t01/Iso007E#116 | 《PLAYER》a mordu la poussière,⏎qui est le prochain ? | 《PLAYER》 a mordu la poussière,⏎qui est le prochain ? | 《PLAYER》 is eating dirt,⏎so who's next to face her? |
| st01_t01/Iso007E#130 | ... 《C030_1》... ⏎Peut-elle faire une bonne duelliste ? | ... 《C030_1》... ⏎Peut-elle devenir une bonne duelliste ? | ...《C030_1》... Can she actually⏎be a great duelist? |
| st01_t01/Iso008E#6 | Hein?⏎Arrête un peu, Jad. | Hein ?⏎Arrête un peu, Jad. | Huh?⏎Stop kidding around, Jay. |
| st01_t01/Iso008E#10 | Un jour ou l'autre, on se retrouvera Syrus ! | Un jour ou l'autre, on se retrouvera, Syrus ! | I'm sure one day we'll⏎meet up again, Syrus! |
| st01_t01/Iso008E#12 | Qu'est-ce que c'est, 《C003_3》? | Qu'est-ce que c'est, 《C003_3》 ? | What is it, 《C003_3》? |
| st01_t01/Iso008E#31 | Hein?⏎Arrête un peu, Jad. | Hein ?⏎Arrête un peu, Jad. | Huh?⏎Stop kidding around, Jay. |
| st01_t01/Iso009E#1 | Tu es nouveau, c'est ça.⏎Je suis 《C049_1》! | Tu es nouveau, c'est ça.⏎Je suis 《C049_1》 ! | You're new, aren't you.⏎I'm 《C049_1》! |
| st01_t01/Iso009E#8 | Tu es nouveau, c'est ça.⏎Je suis 《C069_1》! | Tu es nouveau, c'est ça.⏎Je suis 《C069_1》 ! | You're new, aren't you.⏎I'm 《C069_1》! |

(... altre 437 righe nel CSV)

## A4. Frasi dei duellanti nei duelli

Tabelle `chr_wordstbl_f.bin` e `02chr_wordstbl_...` dentro ~72 archivi `duel/cutin_*.ehp` (e `zakov*`). Le frasi uniche sono ~1.800: tutte rilette. **51 frasi cambiate** (93 voci). Dati: `esatte` (22) e `parti` (22) in `duel_line_corrections_fr.json`. I file `*-ptrs.txt` degli archivi dei personaggi contengono offset assoluti: se una tabella cresce vanno ricalcolati (`rimappa_puntatori`), altrimenti il duello va in crash.

Confronto con parole evidenziate: `docs/changes_fr/duel_lines_diff.md`.

| originale | nuovo | voci | esempi di archivio |
|---|---|---|---|
| Regarde ma Carte magie d'Équipement ! | Regarde ma Carte Magie d'Équipement ! | 1 | cutin_abdos01.ehp |
| Carte Contre-Piège Activée ! | Carte Contre-Piège activée ! | 6 | cutin_abdos01.ehp, cutin_boy01.ehp, cutin_junko01.ehp, cutin_sal01.ehp |
| Rend ton verdict ! | Rends ton verdict ! | 1 | cutin_abdos01.ehp |
| Tris Hélios Megistus | Tris Hélios Megistus ! | 1 | cutin_amunael01.ehp |
| Hiya. | Salut. | 1 | cutin_ayukawa01.ehp |
| Hee hee... ⏎⏎le professeur perd. ⏎⏎Tu es fort. | Hee hee... ⏎⏎Le professeur perd. ⏎⏎Tu es fort. | 1 | cutin_ayukawa01.ehp |
| Royal straight flush ! | Quinte flush royale ! | 1 | cutin_boy01.ehp |
| Huh... | Hein... | 2 | cutin_boy01.ehp, cutin_rei01.ehp |
| Grrr ... | Grrr... | 9 | cutin_boy01.ehp, cutin_fubuki_drk01.ehp, cutin_kagemaru02_a.ehp, cutin_meikyu_k01.ehp |
| Mon dieu... ⏎Je n'ai pas l'habitude de⏎participer à des Duels. | Mon Dieu... ⏎Je n'ai pas l'habitude de⏎participer à des Duels. | 1 | cutin_daitokuji01.ehp |
| Eek ! | Aïe ! | 6 | cutin_daitokuji01.ehp, zakov75.ehp, zakov76.ehp, zakov77.ehp |
| Mon dieu ! | Mon Dieu ! | 3 | cutin_fubuki01.ehp, cutin_kuronosu01.ehp, cutin_momoe01.ehp |
| Mon dieu... ⏎⏎on dirait que ma chance ⏎est⏎en vacances. | Mon Dieu... ⏎⏎on dirait que ma chance ⏎est⏎en vacances. | 1 | cutin_fubuki01.ehp |
| Quelqu'un aurait-il des cheeseburgers ? | Quelqu'un aurait-il des croque-monsieur ? | 1 | cutin_hayato01.ehp |
| J'invoque mon monstre !⏎En position d'attaque ! | J'invoque mon monstre !⏎En Position d'Attaque ! | 1 | cutin_junko01.ehp |
| Huh ? | Hein ? | 6 | cutin_junko01.ehp, cutin_kuronosu01.ehp, cutin_mokeo01.ehp, cutin_ryo01.ehp |
| Sheesh ! C'était brutal ! | Pfff ! C'était brutal ! | 1 | cutin_junko01.ehp |
| Ne soit pas insolent ! | Ne sois pas insolent ! | 3 | cutin_kagemaru01.ehp, cutin_kagemaru03msg.ehp |
| Raviel, Empereur des Phantasmes ! | Raviel, Seigneur des Phantasmes ! | 4 | cutin_kagemaru01.ehp, cutin_kagemaru02_a.ehp, cutin_kagemaru03msg.ehp |
| Cerulean Skyfire ! | Feu Céleste Azur ! | 4 | cutin_kagemaru01.ehp, cutin_kagemaru02_a.ehp, cutin_kagemaru03msg.ehp |
| Shimmering Scraper ! | Racloir Étincelant ! | 4 | cutin_kagemaru01.ehp, cutin_kagemaru02_a.ehp, cutin_kagemaru03msg.ehp |
| Tu es malin. | Tu es mignon. | 1 | cutin_kamula01.ehp |
| Tu n'es pas très gentil. | Tu n'es pas très mignon. | 1 | cutin_kamula01.ehp |
| Vampire Genesis ! | Genèse Vampirique ! | 1 | cutin_kamula01.ehp |
| Mon dieu. ⏎⏎Moi ? Perdre ? ⏎C'est impossible ! | Mon Dieu. ⏎⏎Moi ? Perdre ? ⏎C'est impossible ! | 1 | cutin_kuronosu01.ehp |
| À cet instant là ! | À cet instant-là ! | 2 | cutin_meikyu_k01.ehp, cutin_meikyu_m01.ehp |
| D'abord, détruis-en-une ! | D'abord, détruis-en une ! | 1 | cutin_meikyu_m01.ehp |
| Ma Carte Magie d'Équipement. | Ma Carte Magie d'Équipement ! | 2 | cutin_misawa01.ehp, cutin_tania01.ehp |
| Invocation Rituelle de mon monstre | Invocation Rituelle de mon monstre. | 2 | cutin_mokeo01.ehp, cutin_ryo01.ehp |
| Sors moi de là, vieux. | Sors-moi de là, vieux. | 1 | cutin_mokeo01.ehp |
| Mon dieu, ⏎ce n'est pas plaisant du tout. | Mon Dieu, ⏎ce n'est pas plaisant du tout. | 1 | cutin_momoe01.ehp |
| Ce n'est pas sensé se passer comme ça ! Ahh ! | Ce n'est pas censé se passer comme ça ! Ahh ! | 1 | cutin_psychoshocker01.ehp |
| Tu penses pouvoir arrêter cette attaque ? ⏎Go ! | Tu penses pouvoir arrêter cette attaque ? ⏎Allez ! | 1 | cutin_ryo01.ehp |
| J'invoque l'Assaillant des Protecteurs⏎du Tombeau | J'invoque l'Assaillant des Protecteurs⏎du Tombeau ! | 1 | cutin_sala01.ehp |
| Stealth Slice Strike ! | Coup de Tranchant Furtif ! | 1 | cutin_sala01.ehp |
| Oh mon dieu... | Oh mon Dieu... | 1 | cutin_seiko01.ehp |
| Est-ce que je suis sensée faire ça ? | Est-ce que je suis censée faire ça ? | 1 | cutin_seiko01.ehp |
| C'est le plus puissant des Véhicroids ! ⏎Go ! | C'est le plus puissant des Véhicroids ! ⏎Allez ! | 1 | cutin_shou01.ehp |
| Carte piège ! | Carte Piège ! | 1 | cutin_taizan01.ehp |
| Je offre monstre moi ! | J'offre monstre moi ! | 1 | cutin_taizan01.ehp |
| Juste blessure légère ! | Juste une blessure légère ! | 1 | cutin_taizan01.ehp |
| Donne toi à fond ! Ça ne suffit pas ! | Donne-toi à fond ! Ça ne suffit pas ! | 2 | cutin_thunder01.ehp, cutin_thunder_blk01.ehp |
| Eh ! Ne soit pas insolent ! | Eh ! Ne sois pas insolent ! | 2 | cutin_thunder01.ehp, cutin_thunder_blk01.ehp |
| Une égalité... Humph! ⏎Je vais t'épargner pour cette fois ! | Une égalité... Humph ! ⏎Je vais t'épargner pour cette fois ! | 1 | cutin_thunder01.ehp |
| Je ne perdrai jamais ! ⏎Car je suis le seul et l'unique⏎Chad Princeton ! | Je ne perdrai jamais ! ⏎Car je suis le seul et l'unique⏎Chazz Princeton ! | 1 | cutin_thunder_blk01.ehp |
| Goûtez à la colère de mes démons ! ⏎Annihilation ! | Goûte à la colère de mes démons ! ⏎Annihilation ! | 1 | cutin_titan01.ehp |
| Comment je suis sensée l'utiliser au fait ? | Comment je suis censée l'utiliser au fait ? | 1 | cutin_tome01.ehp |
| Huh ? C'est fini ? ⏎⏎Alors, qui a gagné ? | Hein ? C'est fini ? ⏎⏎Alors, qui a gagné ? | 1 | cutin_tome01.ehp |
| Coalition des Scorpion Noir ! | Coalition des Scorpions Noirs ! | 1 | cutin_zaloog01_a.ehp |
| J'utilise une Carte Piège continu ! | J'utilise une Carte Piège Continu ! | 1 | zakov75.ehp |
| Carte Piège Continue, active. | Carte Piège Continu, active. | 1 | zakov81.ehp |

## A5. Stringhe lunghe e corte dell'interfaccia

Tabelle `strTbl*`, `help_strtbl_*`, `ddstrtbl_*`, `field_strtbl*` (formato `(n, 12, 12+4n)` + offset + UTF-16) in 45 archivi (la stessa tabella e' copiata in piu' archivi, es. `field/always_*_fra.ehp` x6). **254 stringhe uniche cambiate**. Regole: `tools/corrections/string_rules_fr.py` — **139 voci `STRINGHE`** (archivio, membro, indice 0-based, [(vecchio, nuovo)], motivo), **58 `GLOBALI`** (regex/callable, applicate dopo le STRINGHE) su **12 tabelle** (`TABELLE`); piu' 0 correzioni puntuali in `tools/data/ui_texts.json` (scrittura sul posto, testo piu' corto o uguale).

### Per membro (stringhe uniche cambiate)
| membro | stringhe |
|---|---|
| strTbl_f.bin | 85 |
| help_strtbl_contents_duel_f.bin | 63 |
| help_strtbl_contents.bin | 45 |
| field_strtbl_item.bin | 25 |
| strTbl.bin | 23 |
| field_strtbl.bin | 7 |
| ddstrtbl_f.bin | 6 |

### Regole globali (tutte)
| modello | sostituzione | motivo |
|---|---|---|
| \boeuf | œuf | legatura |
| \bboeuf | bœuf | legatura |
| pâte d'haricot | pâte de haricots | grammatica |
| Qu'est ce q | Qu'est-ce q | trattino |
| Éxodia | Exodia | nome della carta |
| \bdurion\b | durian | refuso |
| l\"effet | l'effet | doppio apice al posto dell'apostrofo |
| \bCartes Monstres\b | Cartes Monstre | Monstre e' invariabile |
| \bCartes Pièges\b | Cartes Piège | Piège e' invariabile |
| \bCartes Magies\b | Cartes Magie | Magie e' invariabile |
| \bdes Carte Monstre\b | des Cartes Monstre | plurale |
| \bTypes de Carte Monstre\b | Types de Cartes Monstre | plurale |
| Il existe un monstre spécial appelé Monstres? de Fusion | Il existe un type de monstre spécial appelé Monstre de Fusion | frase |
| \bMonstres Fusion\b | Monstres de Fusion | nome del tipo (come sulle carte) |
| \bMonstre Fusion\b | Monstre de Fusion | nome del tipo (come sulle carte) |
| Les Monstres de Fusion est invoqué | Le Monstre de Fusion est Invoqué | frase |
| \bMonstres Matériel de Fusion\b | Monstres-Matériels de Fusion | termine come sulle carte |
| \bCartes Monstre Matériel de Fusion\b | Monstres-Matériels de Fusion | termine come sulle carte |
| d'une Carte Monstres de Fusion | d'une Carte Monstre de Fusion | plurale |
| \boeil\b | œil | legatura |
| \bMonstres Rituel\b | Monstres Rituels | plurale |
| \bMagie Normal\b | Magie Normale | accordo |
| \bMagie Continu\b | Magie Continue | accordo |
| \bdes carte\b | des cartes | plurale |
| est appelé une\b | est appelée une | accordo |
| conditions d'activations | conditions d'activation | singolare |
| Seule 2  | Seules 2  | accordo |
| sont affichées ci- | sont affichés ci- | accordo |
| ([Ll])es Compteur Magie | \1es Compteurs Magie | plurale |
| d'effet relatifs | d'effets relatifs | plurale |
| étiquett(?=é\|ée\|ées\|és\|er) | étiquet | refuso |
| après que son effet soit activée? | après l'activation de son effet | congiuntivo errato |
| RETOURNEMENT : | FLIP: | come sulle carte |
| le même tour ou elle | le même tour où elle | accento |
| En règle général\b | En règle générale | accordo |
| Certaines cartes nécessite\b | Certaines cartes nécessitent | accordo |
| aurait du être | aurait dû être | accento |
| La résultat | Le résultat | accordo |
| Terrain,  elle | Terrain, elle | doppio spazio |
| à un 1 monstre | à 1 monstre | refuso |
| face verso et retournée | face verso est retournée | refuso |
| en grâce à une | grâce à une | refuso |
| de leur effets | de leurs effets | plurale |
| 1 seul carte | 1 seule carte | accordo |
| nombre d'effet est | nombre d'effets est | plurale |
| réductions due à | réductions dues à | accordo |
| nombre de carte dans | nombre de cartes dans | plurale |
| après voir été | après avoir été | refuso |
| les cartes qui détermine\b | les cartes qui déterminent | accordo |
| le partenaire à placée | le partenaire a placée | refuso |
| Carte Monstre Invoqué par | Carte Monstre Invoquée par | accordo |
| un monstre crée par | un monstre créé par | participio |
| son effet ne pourra pas être activée et être ajouté à la Chaîne | elle ne pourra pas être activée ni ajoutée à la Chaîne | frase |
| les effets cartes de Spell Speed 3 | les effets des cartes de Spell Speed 3 | refuso |
| Magie de Jeu-Rapide | Magie Jeu-Rapide | termine |
| (?<=Speed 3\])\nContre\n | ⏎Contre-Piège⏎ | termine |
| \bDonnez\b | Donner | infinito come le altre voci del menu |
| \bMangez\b | Manger | infinito come le altre voci del menu |

### Voci STRINGHE (tutte): dove e perche'
| archivio | membro | indice | cambiamenti | motivo |
|---|---|---|---|---|
| database/charalist.ehp | strTbl_f.bin | 12 | 5 sostituzione/i | refusi e accordi |
| database/charalist.ehp | strTbl_f.bin | 13 | 3 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_f.bin | 14 | 1 sostituzione/i | accordo |
| database/charalist.ehp | strTbl_f.bin | 15 | 6 sostituzione/i | refusi e accordi |
| database/charalist.ehp | strTbl_f.bin | 18 | 4 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_f.bin | 19 | 2 sostituzione/i | accordi |
| database/charalist.ehp | strTbl_f.bin | 20 | 3 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_f.bin | 21 | 2 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_f.bin | 22 | 6 sostituzione/i | refusi, e Atticus/Isidore come nel resto del gioco |
| database/charalist.ehp | strTbl_f.bin | 23 | 3 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_f.bin | 24 | 1 sostituzione/i | trattino |
| database/charalist.ehp | strTbl_f.bin | 25 | 1 sostituzione/i | refuso |
| database/charalist.ehp | strTbl_f.bin | 27 | 2 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_f.bin | 30 | 1 sostituzione/i | participio |
| database/charalist.ehp | strTbl_f.bin | 31 | 2 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_f.bin | 34 | 4 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_f.bin | 35 | 3 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_f.bin | 43 | 1 sostituzione/i | plurale |
| database/charalist.ehp | strTbl_f.bin | 44 | 1 sostituzione/i | plurale |
| database/charalist.ehp | strTbl_f.bin | 51 | 2 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_f.bin | 52 | 1 sostituzione/i | "Profile" e "directeur": come nei dialoghi (Chancelier) |
| database/duelrecord.ehp | strTbl_f.bin | 17 | 1 sostituzione/i | accordo |
| database/duelrecord.ehp | strTbl_f.bin | 80 | 1 sostituzione/i | spazio finale |
| database/duelrecord.ehp | strTbl_f.bin | 82 | 1 sostituzione/i | accento |
| database/duelrecord.ehp | strTbl_f.bin | 94 | 1 sostituzione/i | accordo |
| database/duelrecord.ehp | strTbl_f.bin | 123 | 1 sostituzione/i | frase troncata |
| database/duelrecord.ehp | strTbl_f.bin | 137 | 1 sostituzione/i | refuso |
| database/duelrecord.ehp | strTbl_f.bin | 155 | 1 sostituzione/i | accento |
| database/duelrecord.ehp | strTbl_f.bin | 159 | 1 sostituzione/i | stile come le altre voci |
| database/duelrecord.ehp | strTbl_f.bin | 160 | 1 sostituzione/i | stile |
| database/duelrecord.ehp | strTbl_f.bin | 161 | 1 sostituzione/i | stile |
| database/duelrecord.ehp | strTbl_f.bin | 162 | 1 sostituzione/i | stile |
| database/duelrecord.ehp | strTbl_f.bin | 255 | 1 sostituzione/i | abbreviazione |
| database/duelrecord.ehp | strTbl_f.bin | 256 | 1 sostituzione/i | abbreviazione |
| database/duelrecord.ehp | strTbl_f.bin | 258 | 1 sostituzione/i | accordo |
| duel/result/result_f.ehp | strTbl.bin | 17 | 1 sostituzione/i | accordo |
| duel/result/result_f.ehp | strTbl.bin | 80 | 1 sostituzione/i | spazio finale |
| duel/result/result_f.ehp | strTbl.bin | 82 | 1 sostituzione/i | accento |
| duel/result/result_f.ehp | strTbl.bin | 94 | 1 sostituzione/i | accordo |
| duel/result/result_f.ehp | strTbl.bin | 123 | 1 sostituzione/i | frase troncata |
| duel/result/result_f.ehp | strTbl.bin | 137 | 1 sostituzione/i | refuso |
| duel/result/result_f.ehp | strTbl.bin | 155 | 1 sostituzione/i | accento |
| duel/result/result_f.ehp | strTbl.bin | 159 | 1 sostituzione/i | stile come le altre voci |
| duel/result/result_f.ehp | strTbl.bin | 160 | 1 sostituzione/i | stile |
| duel/result/result_f.ehp | strTbl.bin | 161 | 1 sostituzione/i | stile |
| duel/result/result_f.ehp | strTbl.bin | 162 | 1 sostituzione/i | stile |
| duel/result/result_f.ehp | strTbl.bin | 255 | 1 sostituzione/i | abbreviazione |
| duel/result/result_f.ehp | strTbl.bin | 256 | 1 sostituzione/i | abbreviazione |
| duel/result/result_f.ehp | strTbl.bin | 258 | 1 sostituzione/i | accordo |
| deck/all_f.ehp | strTbl.bin | 37 | 1 sostituzione/i | frase incompleta |
| deck/all_f.ehp | strTbl.bin | 40 | 1 sostituzione/i | accordi |
| deck/all_f.ehp | strTbl.bin | 129 | 1 sostituzione/i | accordo |
| deck/all_f.ehp | strTbl.bin | 138 | 1 sostituzione/i | frase sgrammaticata |
| deck/all_f.ehp | strTbl.bin | 142 | 1 sostituzione/i | congiuntivo |
| deck/all_f.ehp | strTbl.bin | 154 | 2 sostituzione/i | accordo e '$' al posto dell'a capo |
| deck/all_f.ehp | help_strtbl_contents.bin | 8 | 1 sostituzione/i | plurale |
| deck/all_f.ehp | help_strtbl_contents.bin | 13 | 1 sostituzione/i | accordo |
| deck/all_f.ehp | help_strtbl_contents.bin | 16 | 1 sostituzione/i | trattino |
| deck/all_f.ehp | help_strtbl_contents.bin | 99 | 5 sostituzione/i | regole del Deck: manca la regola dei 3 esemplari |
| deck/all_f.ehp | help_strtbl_contents.bin | 102 | 1 sostituzione/i | accordo |
| deck/all_f.ehp | help_strtbl_contents.bin | 103 | 2 sostituzione/i | plurale |
| deck/all_f.ehp | help_strtbl_contents.bin | 104 | 1 sostituzione/i | ripetizione |
| deck/all_f.ehp | help_strtbl_contents.bin | 110 | 1 sostituzione/i | frase incompleta |
| deck/all_f.ehp | help_strtbl_contents.bin | 115 | 1 sostituzione/i | participio |
| deck/all_f.ehp | help_strtbl_contents.bin | 120 | 3 sostituzione/i | refusi |
| deck/all_f.ehp | help_strtbl_contents.bin | 129 | 1 sostituzione/i | frase |
| deck/all_f.ehp | help_strtbl_contents.bin | 130 | 1 sostituzione/i | accordi |
| deck/all_f.ehp | help_strtbl_contents.bin | 138 | 1 sostituzione/i | coerenza |
| deck/all_f.ehp | help_strtbl_contents.bin | 141 | 1 sostituzione/i | accordo |
| deck/all_f.ehp | help_strtbl_contents.bin | 142 | 1 sostituzione/i | accordo |
| deck/all_f.ehp | help_strtbl_contents.bin | 146 | 1 sostituzione/i | refuso |
| deck/all_f.ehp | help_strtbl_contents.bin | 148 | 1 sostituzione/i | refuso |
| deck/all_f.ehp | help_strtbl_contents.bin | 151 | 2 sostituzione/i | accordi |
| deck/all_f.ehp | help_strtbl_contents.bin | 152 | 1 sostituzione/i | plurale |
| deck/all_f.ehp | help_strtbl_contents.bin | 164 | 1 sostituzione/i | plurale |
| deck/all_f.ehp | help_strtbl_contents.bin | 172 | 1 sostituzione/i | frase |
| deck/tutorial.ehp | strTbl_f.bin | 14 | 1 sostituzione/i | nome della scuola |
| deck/tutorial.ehp | strTbl_f.bin | 35 | 2 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_f.bin | 36 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_f.bin | 53 | 1 sostituzione/i | plurale |
| deck/tutorial.ehp | strTbl_f.bin | 79 | 1 sostituzione/i | coerenza |
| deck/tutorial.ehp | strTbl_f.bin | 83 | 1 sostituzione/i | termine |
| deck/tutorial.ehp | strTbl_f.bin | 97 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_f.bin | 92 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_f.bin | 106 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_f.bin | 139 | 1 sostituzione/i | frase incompleta |
| deck/tutorial.ehp | strTbl_f.bin | 146 | 1 sostituzione/i | spazio |
| deck/tutorial.ehp | strTbl_f.bin | 150 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_f.bin | 154 | 1 sostituzione/i | participio |
| deck/tutorial.ehp | strTbl_f.bin | 155 | 1 sostituzione/i | frase |
| deck/tutorial.ehp | strTbl_f.bin | 161 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_f.bin | 163 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_f.bin | 164 | 2 sostituzione/i | refusi |
| deck/tutorial.ehp | strTbl_f.bin | 167 | 2 sostituzione/i | spazi |
| deck/tutorial.ehp | strTbl_f.bin | 169 | 1 sostituzione/i | refusi |
| deck/tutorial.ehp | strTbl_f.bin | 189 | 1 sostituzione/i | frase |
| deck/tutorial.ehp | strTbl_f.bin | 215 | 1 sostituzione/i | refusi |
| duel/basic_bf.ehp | ddstrtbl_f.bin | 70 | 1 sostituzione/i | nome della carta |
| duel/basic_bf.ehp | ddstrtbl_f.bin | 84 | 1 sostituzione/i | refuso |
| duel/basic_bf.ehp | ddstrtbl_f.bin | 88 | 1 sostituzione/i | testo della vittoria al posto di quello della sconfitta |
| duel/basic_bf.ehp | ddstrtbl_f.bin | 66 | 1 sostituzione/i | italiano rimasto nella tabella francese |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 3 | 1 sostituzione/i | plurale |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 15 | 1 sostituzione/i | accordo |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 65 | 1 sostituzione/i | Main Phase 1, non 2 |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 75 | 1 sostituzione/i | invariabili |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 108 | 1 sostituzione/i | frase |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 112 | 5 sostituzione/i | regole del Deck |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 115 | 1 sostituzione/i | accordo |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 117 | 1 sostituzione/i | accordo |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 119 | 3 sostituzione/i | refusi |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 150 | 2 sostituzione/i | refusi |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 152 | 1 sostituzione/i | accordo |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 157 | 2 sostituzione/i | refusi |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 163 | 1 sostituzione/i | accordo |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 165 | 1 sostituzione/i | accordo |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 169 | 1 sostituzione/i | ripetizione |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 170 | 1 sostituzione/i | negazione mancante |
| duel/basic_bf.ehp | help_strtbl_contents_duel_f.bin | 171 | 3 sostituzione/i | termini e refusi |
| field/always_*_fra.ehp | field_strtbl.bin | 35 | 1 sostituzione/i | accento |
| field/always_*_fra.ehp | field_strtbl.bin | 57 | 1 sostituzione/i | accento |
| field/always_*_fra.ehp | field_strtbl.bin | 92 | 1 sostituzione/i | abbreviazione di vendredi |
| field/always_*_fra.ehp | field_strtbl.bin | 100 | 1 sostituzione/i | frase troncata |
| field/always_*_fra.ehp | field_strtbl.bin | 104 | 1 sostituzione/i | refuso |
| field/always_*_fra.ehp | field_strtbl_item.bin | 7 | 1 sostituzione/i | nome come nel resto del gioco |
| field/always_*_fra.ehp | field_strtbl_item.bin | 52 | 1 sostituzione/i | accordo |
| field/always_*_fra.ehp | field_strtbl_item.bin | 89 | 1 sostituzione/i | refuso |
| field/always_*_fra.ehp | field_strtbl_item.bin | 96 | 1 sostituzione/i | accordo |
| field/always_*_fra.ehp | field_strtbl_item.bin | 107 | 1 sostituzione/i | accordo |
| field/always_*_fra.ehp | field_strtbl_item.bin | 156 | 1 sostituzione/i | refuso |
| field/always_*_fra.ehp | field_strtbl_item.bin | 159 | 1 sostituzione/i | plurale |
| field/always_*_fra.ehp | field_strtbl_item.bin | 169 | 2 sostituzione/i | accordo e nome |
| field/always_*_fra.ehp | field_strtbl_item.bin | 172 | 1 sostituzione/i | refuso |
| field/always_*_fra.ehp | field_strtbl_item.bin | 173 | 1 sostituzione/i | accordo |
| field/always_*_fra.ehp | field_strtbl_item.bin | 185 | 1 sostituzione/i | maiuscola |
| field/always_*_fra.ehp | field_strtbl_item.bin | 188 | 1 sostituzione/i | accordo |
| field/always_*_fra.ehp | field_strtbl_item.bin | 194 | 1 sostituzione/i | nome come nei dialoghi |
| field/always_*_fra.ehp | field_strtbl_item.bin | 197 | 1 sostituzione/i | refuso |
| labo/conv_machine.ehp | strTbl_f.bin | 2 | 1 sostituzione/i | accento |
| labo/password.ehp | strTbl_f.bin | 11 | 1 sostituzione/i | verbo mancante |

### Correzioni puntuali `ui_texts.json`
| file | membro | indice | vecchio | nuovo | motivo |
|---|---|---|---|---|---|

### Elenco completo
**Confronto completo con parole evidenziate: `docs/changes_fr/ui_strings_diff.md`.** Dati grezzi: `docs/changes_fr/ui_strings.csv`. Prime 40:

| membro | indice | originale | nuovo |
|---|---|---|---|
| strTbl_f.bin | 12 | Jader est incontestablement le meilleur duelliste parmi le dortoir Slifer Rouge, et il fait surement partie de l'élite des 1ère année. Tous envient son instinct du duel qui lui permet de se sortir des situations les plus désespérées en l'espace d'un tour.⏎⏎Lorsque Jaden se retrouve en difficulté et n'a plus de cartes en main, il peut toujours compter sur Bubbleman.⏎⏎Son Deck laisse une grande part aux Héros Élémentaires, qui ressemblent aux héros de sa jeunesse.⏎⏎Une de ses tactiques préférées consiste à fusionner les cartes des Héros Élémentaires, qui lui permettent, associées à un bonne pioche de cartes, de battre ses adversaires à une vitesse fulgurante.⏎⏎Jaden est un jeune homme de nature insouciante qui considère que le plus important dans un duel est d'abord de s'amuser. Ce comportement lui a empêché de se faire des amis au sein de l'Académie aux règles si strictes, mais il est maintenant une figure appréciée du campus.⏎⏎Bien que jouissant d'un certain succès auprès des filles, ses relations avec elles restent un mystère. Il n'a jamais démontré à leur égard un quelconque intérêt.⏎⏎Il peut manger n'importe quelle type de nourriture et n'a pas vraiment de préférence. | Jaden est incontestablement le meilleur duelliste parmi le dortoir Slifer Rouge, et il fait sûrement partie de l'élite des 1ère année. Tous envient son instinct du duel qui lui permet de se sortir des situations les plus désespérées en l'espace d'un tour.⏎⏎Lorsque Jaden se retrouve en difficulté et n'a plus de cartes en main, il peut toujours compter sur Bubbleman.⏎⏎Son Deck laisse une grande part aux Héros Élémentaires, qui ressemblent aux héros de sa jeunesse.⏎⏎Une de ses tactiques préférées consiste à fusionner les cartes des Héros Élémentaires, qui lui permettent, associées à une bonne pioche de cartes, de battre ses adversaires à une vitesse fulgurante.⏎⏎Jaden est un jeune homme de nature insouciante qui considère que le plus important dans un duel est d'abord de s'amuser. Ce comportement l'a empêché de se faire des amis au sein de l'Académie aux règles si strictes, mais il est maintenant une figure appréciée du campus.⏎⏎Bien que jouissant d'un certain succès auprès des filles, ses relations avec elles restent un mystère. Il n'a jamais démontré à leur égard un quelconque intérêt.⏎⏎Il peut manger n'importe quel type de nourriture et n'a pas vraiment de préférence. |
| strTbl_f.bin | 13 | Syrus a beaucoup d'admiration pour Jaden et le considère comme un grand frère. Mais il a aussi un vrai frère, alors il distingue les deux par différents surnoms.⏎⏎Il a du respect pour les gens à fortes personnalités, mais a tendance à se sentir inférieur. Il aimerait un jour être comme Jaden.⏎⏎Syrus n'a pas trop confiance en ses compétences, ce qui le rend parfois trop pessimiste.⏎Mais il sait aussi être très critique envers les autres.⏎⏎Son pessimisme lui a vallu de combattre en duel sans vraiment se donner à fond, pensant de toute façon perdre. Mais depuis qu'il a rencontré Jaden, il a appris à avoir une attitude plus positive.⏎⏎Syrus aime les véhicules et utilise un deck comprenant beaucoup de cartes "Vehicroid", un type de véhicule vivant.⏎Son air de petit garçon cache en réalité une personne au grand courage.⏎⏎Il est du genre à tomber amoureux d'une jolie fille, mais il n'a jamais vraiment eu d'histoire d'amour avec quelqu'un.⏎⏎Le repas préféré de Syrus est préparé dans la cantine de Slifer Rouge une fois par mois. Cependant, il ne supporte pas la nourriture épicée. | Syrus a beaucoup d'admiration pour Jaden et le considère comme un grand frère. Mais il a aussi un vrai frère, alors il distingue les deux par différents surnoms.⏎⏎Il a du respect pour les gens à fortes personnalités, mais a tendance à se sentir inférieur. Il aimerait un jour être comme Jaden.⏎⏎Syrus n'a pas trop confiance en ses compétences, ce qui le rend parfois trop pessimiste.⏎Mais il sait aussi être très critique envers les autres.⏎⏎Son pessimisme lui a valu de combattre en duel sans vraiment se donner à fond, pensant de toute façon perdre. Mais depuis qu'il a rencontré Jaden, il a appris à avoir une attitude plus positive.⏎⏎Syrus aime les véhicules et utilise un Deck comprenant beaucoup de cartes "Véhicroid", un type de véhicule vivant.⏎Son air de petit garçon cache en réalité une personne au grand courage.⏎⏎Il est du genre à tomber amoureux d'une jolie fille, mais il n'a jamais vraiment eu d'histoire d'amour avec quelqu'un.⏎⏎Le repas préféré de Syrus est préparé dans la cantine de Slifer Rouge une fois par mois. Cependant, il ne supporte pas la nourriture épicée. |
| strTbl_f.bin | 14 | Chumley est bien plus gentil que son nom l'indique.⏎Il possède une personnalité simple et pure.⏎Chumley pense qu'un duel est plus qu'une simple victoire ou défaite. Cette philosophie explique en partie pourquoi il n'a pas réussi à s'adapter à l'enseignement rigoureuse de l'Académie.⏎Toutefois, c'est un excellent duelliste. Ses habiletés lui permettent même d'entendre les esprits des cartes.⏎⏎Il aime l'Australie, après y avoir été en voyage d'école. C'est pourquoi il utilise de nombreuses cartes relatives à ce pays dans son Deck.⏎⏎Pour lui rappeler sa mère, il collectionne des photos d'une pop star qui est... un peu dépassée.⏎⏎Chumley n'a pas de préférence particulière pour la nourriture mais il évite la viande.⏎Il mange souvent du poisson. | Chumley est bien plus gentil que son nom l'indique.⏎Il possède une personnalité simple et pure.⏎Chumley pense qu'un duel est plus qu'une simple victoire ou défaite. Cette philosophie explique en partie pourquoi il n'a pas réussi à s'adapter à l'enseignement rigoureux de l'Académie.⏎Toutefois, c'est un excellent duelliste. Ses habiletés lui permettent même d'entendre les esprits des cartes.⏎⏎Il aime l'Australie, après y avoir été en voyage d'école. C'est pourquoi il utilise de nombreuses cartes relatives à ce pays dans son Deck.⏎⏎Pour lui rappeler sa mère, il collectionne des photos d'une pop star qui est... un peu dépassée.⏎⏎Chumley n'a pas de préférence particulière pour la nourriture mais il évite la viande.⏎Il mange souvent du poisson. |
| strTbl_f.bin | 15 | Alexia est la meilleure duelliste féminine et n'a pas peur d'affronter les garçons. ⏎En plus de ces talents de duelliste, c'est aussi une fille d'une rare beauté. Certains la surnomment d'ailleurs " la Reine de l'Académie". ⏎À la fois belle et intelligente, Alexia rend jalouse les autres filles du campus.⏎⏎Elle est d'une nature courageuse, mais sa ferveur dans les duels lui donne parfois l'impression d'une personne désagréable.⏎⏎Alexia utilise un Deck inhabituel appellé "Cyber Girl", qui consiste de Cartes Monstres représentant de jolies filles.⏎L'une de ces cartes est "Cyber Trancheuse", qui a sortit Alexia du pétrin plus d'une fois.⏎⏎Alexia n'a pas encore l'air de s'intéresser aux garçons. Elle parle plutôt de son "amour pour le duel",⏎qu'elle démontre à chacun de ses combats.⏎⏎Elle aime manger tout ce qui est bon pour la santé, mais ne refuse pas les sucreries de temps en temps.⏎Par contre, elle n'aime pas les nourritures à l'odeur trop forte. | Alexia est la meilleure duelliste féminine et n'a pas peur d'affronter les garçons. ⏎En plus de ses talents de duelliste, c'est aussi une fille d'une rare beauté. Certains la surnomment d'ailleurs "la Reine de l'Académie". ⏎À la fois belle et intelligente, Alexia rend jalouses les autres filles du campus.⏎⏎Elle est d'une nature courageuse, mais sa ferveur dans les duels lui donne parfois l'impression d'une personne désagréable.⏎⏎Alexia utilise un Deck inhabituel appelé "Cyber Girl", composé de Cartes Monstre représentant de jolies filles.⏎L'une de ces cartes est "Cyber Trancheuse", qui a sorti Alexia du pétrin plus d'une fois.⏎⏎Alexia n'a pas encore l'air de s'intéresser aux garçons. Elle parle plutôt de son "amour pour le duel",⏎qu'elle démontre à chacun de ses combats.⏎⏎Elle aime manger tout ce qui est bon pour la santé, mais ne refuse pas les sucreries de temps en temps.⏎Par contre, elle n'aime pas les nourritures à l'odeur trop forte. |
| strTbl_f.bin | 18 | Bastion est un élève brilliant. C'est lui qui a eu la meilleure note au concours d'entrée de l'Académie. C'est le seul garçon qui ait failli réussir à faire parti de l'Obélisque Bleu. Bastion a un côté sérieux, mais il sait aussi être ouvert. Bien qu'il soit supérieur aux duellistes de Slifer Rouge, il ne les considère pas comme ses subordonnés.⏎⏎Pendant son temps libre, Bastion aime réfléchir à des formules mathématiques compliquées et les inscrire sur le premier support qu'il trouve.⏎C'est pour cela que les murs de sa chambre sont couverts de chiffres et de formules. Même les cartes de son Deck sont couvertes de graffitis. Cette vieille habitude refait souvent surface lors de ses duels. Il évalue ainsi le style de jeu de ses adversaires, et applique ses formules mathématiques à sa stratégie.⏎Si Jaden possède un talent naturel qui fait de lui un duelliste exceptionnel, Bastion doit son habilité à son travail et son assiduité.⏎⏎Il prétend avoir six Deck représentant six attributs qu'il utilise en fonction de son adversaire. Il affirme aussi que ces 6 Decks sont parfaitement équilibrés. Pourtant, il ne combat que rarement en duel.⏎⏎La grande intelligence de Bastion fait de lui un adversaire redoutable. ⏎⏎Il a décidé qu'il ne perdrait pas son temps à s'intéresser aux filles, mais lorsqu'elles lui demandent une faveur, il s'empresse d'accomplir leurs souhaits, surtout celles aux jolies regards dociles.⏎⏎Il préfère manger des légumes et semble faire attention à son alimentation.⏎En revanche, il n'aime pas les fruits et les sucreries ne l'intéressent pas. | Bastion est un élève brillant. C'est lui qui a eu la meilleure note au concours d'entrée de l'Académie. C'est le seul garçon qui ait failli réussir à faire partie de l'Obélisque Bleu. Bastion a un côté sérieux, mais il sait aussi être ouvert. Bien qu'il soit supérieur aux duellistes de Slifer Rouge, il ne les considère pas comme ses subordonnés.⏎⏎Pendant son temps libre, Bastion aime réfléchir à des formules mathématiques compliquées et les inscrire sur le premier support qu'il trouve.⏎C'est pour cela que les murs de sa chambre sont couverts de chiffres et de formules. Même les cartes de son Deck sont couvertes de graffitis. Cette vieille habitude refait souvent surface lors de ses duels. Il évalue ainsi le style de jeu de ses adversaires, et applique ses formules mathématiques à sa stratégie.⏎Si Jaden possède un talent naturel qui fait de lui un duelliste exceptionnel, Bastion doit son habileté à son travail et son assiduité.⏎⏎Il prétend avoir six Deck représentant six attributs qu'il utilise en fonction de son adversaire. Il affirme aussi que ces 6 Decks sont parfaitement équilibrés. Pourtant, il ne combat que rarement en duel.⏎⏎La grande intelligence de Bastion fait de lui un adversaire redoutable. ⏎⏎Il a décidé qu'il ne perdrait pas son temps à s'intéresser aux filles, mais lorsqu'elles lui demandent une faveur, il s'empresse d'accomplir leurs souhaits, surtout celles aux jolis regards dociles.⏎⏎Il préfère manger des légumes et semble faire attention à son alimentation.⏎En revanche, il n'aime pas les fruits et les sucreries ne l'intéressent pas. |
| strTbl_f.bin | 19 | Zen est tout simplement le meilleur duelliste de l'Académie. On le surnomme l'"Empereur".⏎Il obtient toujours les meilleures notes de l'école et en est donc le représentant légitime.⏎Zen n'est pas très bavard. C'est pour cela que les gens pensent qu'il est froid et sans émotion, mais ceux qui font l'effort de dépasser cette première impression découvre une personne chaleureuse et bienveillante. ⏎⏎Zen utilise les redoutables cartes "Cyber Dragon". Une de ses spécialités consiste à utiliser l'effet de "Lien de Puissance" pour déclencher une attaque dévastatrice.⏎⏎Pour lui, un duel d'honneur et le respect envers l'adversaire sont plus important que la victoire.⏎Zen ne prend aucun duel à la légère et n'économisera jamais ses forces. Il aura de la considération pour tout duelliste digne de ce nom.⏎⏎Son apparence, sa personnalité et ses compétences de duelliste en font la coqueluche des élèves féminines. Elles sont plus d'une à se disputer ses faveurs.⏎⏎Zen aime la nourriture simple. | Zen est tout simplement le meilleur duelliste de l'Académie. On le surnomme l'"Empereur".⏎Il obtient toujours les meilleures notes de l'école et en est donc le représentant légitime.⏎Zen n'est pas très bavard. C'est pour cela que les gens pensent qu'il est froid et sans émotion, mais ceux qui font l'effort de dépasser cette première impression découvrent une personne chaleureuse et bienveillante. ⏎⏎Zen utilise les redoutables cartes "Cyber Dragon". Une de ses spécialités consiste à utiliser l'effet de "Lien de Puissance" pour déclencher une attaque dévastatrice.⏎⏎Pour lui, un duel d'honneur et le respect envers l'adversaire sont plus importants que la victoire.⏎Zen ne prend aucun duel à la légère et n'économisera jamais ses forces. Il aura de la considération pour tout duelliste digne de ce nom.⏎⏎Son apparence, sa personnalité et ses compétences de duelliste en font la coqueluche des élèves féminines. Elles sont plus d'une à se disputer ses faveurs.⏎⏎Zen aime la nourriture simple. |
| strTbl_f.bin | 20 | En tant que professeur du dortoir des garçons de l'Obélisque Bleu, Vellian Crowler est responsable des meilleurs duellistes de l'Académie.⏎Il a une façon très particulière de s'exprimer.⏎⏎Vellian représente l'esprit de la Duel Académie. C'est à dire une rigidité de l'enseignement et la performance à tout prix. Les meilleurs sont traités en favoris, tandis que les moins doués sont méprisés. Il a observé Jaden Yuki du dortoir Slifer Rouge avec attention et a manigancé de nombreux plans afin de le faire expulser de l'Académie.⏎⏎Il porte une "toge de duel" lorsqu'il se bat. Il paraît que chaque personne de l'Académie peut en obtenir une, mais personne d'autre que Vellian n'en a jamais porté.⏎⏎Il utilise un Deck rempli d"Rouages Ancients", des machines mystérieuses d'une époque perdue. Sa carte principale est le "Golem Rouages Ancients", une carte si puissante qu'on l'appelle la briseuse de règles.⏎⏎Comme son apparence le laisse deviner, Vellian n'aime que les aliments de la plus grande qualité. | En tant que professeur du dortoir des garçons de l'Obélisque Bleu, Vellian Crowler est responsable des meilleurs duellistes de l'Académie.⏎Il a une façon très particulière de s'exprimer.⏎⏎Vellian représente l'esprit de l'Académie de Duel. C'est-à-dire une rigidité de l'enseignement et la performance à tout prix. Les meilleurs sont traités en favoris, tandis que les moins doués sont méprisés. Il a observé Jaden Yuki du dortoir Slifer Rouge avec attention et a manigancé de nombreux plans afin de le faire expulser de l'Académie.⏎⏎Il porte une "toge de duel" lorsqu'il se bat. Il paraît que chaque personne de l'Académie peut en obtenir une, mais personne d'autre que Vellian n'en a jamais porté.⏎⏎Il utilise un Deck rempli de "Rouages Ancients", des machines mystérieuses d'une époque perdue. Sa carte principale est le "Golem Rouages Ancients", une carte si puissante qu'on l'appelle la briseuse de règles.⏎⏎Comme son apparence le laisse deviner, Vellian n'aime que les aliments de la plus grande qualité. |
| strTbl_f.bin | 21 | Lyman Banner est le professeur d'alchimie et est à la tête du dortoir Slifer Rouge.⏎⏎Son comportement décontracté et son discours détendu en font une personne difficile à cerner.⏎⏎Lyman n'a que rarement, ou même jamais participer à un duel car il s'est dédié entièrement à l'alchimie, qui consiste à créer quelque chose à partir de rien. Personne ne sait quel genre de Deck il utilise.⏎⏎Bien qu'il reste un mystère, une chose à son propos est bien connue. Il adore les chats.⏎⏎Quand à son met favori, cela reste aussi une énigme. | Lyman Banner est le professeur d'alchimie et est à la tête du dortoir Slifer Rouge.⏎⏎Son comportement décontracté et son discours détendu en font une personne difficile à cerner.⏎⏎Lyman n'a que rarement, ou même jamais participé à un duel car il s'est dédié entièrement à l'alchimie, qui consiste à créer quelque chose à partir de rien. Personne ne sait quel genre de Deck il utilise.⏎⏎Bien qu'il reste un mystère, une chose à son propos est bien connue. Il adore les chats.⏎⏎Quant à son mets favori, cela reste aussi une énigme. |
| strTbl_f.bin | 22 | C'est le jeune frère d'Alexia, et si l'on s'en réfère à la personnalité de sa soeur, on pourrait croire qu'il s'agit d'un garçon strict et méticuleux. Or, il est joyeux, peut-être même trop. Sa charmante personnalité et ses traits d'humour en font une personne très appréciée des demoiselles.⏎⏎C'est un duelliste hors-pair. Certains affirment même qu'il serait l'égal de Zen.⏎Il a été un bon ami de Zen, un duelliste peu bavard. Curieux que des personnalités apparement opposées puissent s'entendre si bien.⏎⏎Atticus a toujours souhaité que sa soeur ressemble plus aux autre filles, qu'elle soit plus féminine. Elle n'en est que plus irritée. | C'est le grand frère d'Alexia, et si l'on s'en réfère à la personnalité de sa sœur, on pourrait croire qu'il s'agit d'un garçon strict et méticuleux. Or, il est joyeux, peut-être même trop. Sa charmante personnalité et ses traits d'humour en font une personne très appréciée des demoiselles.⏎⏎C'est un duelliste hors pair. Certains affirment même qu'il serait l'égal de Zen.⏎Il a été un bon ami de Zen, un duelliste peu bavard. Curieux que des personnalités apparemment opposées puissent s'entendre si bien.⏎⏎Isidore a toujours souhaité que sa sœur ressemble plus aux autres filles, qu'elle soit plus féminine. Elle n'en est que plus irritée. |
| strTbl_f.bin | 23 | Camula est une membre des Cavaliers de l'Ombre, un groupe à la recherche des clés spirituelles.⏎C'est une vampire.⏎⏎Le Deck de Camula est constitué de Cartes Monstre de type Zombie tels que les vampires.⏎Elle commande des chauve-souris avec ses yeux écarlates pour qu'ils espionnent le Deck de son adversaire. Elle peut ensuite adapter sa tactique en fonction du jeu adverse. Elle combat en duel sans faire preuve de fierté ni même d'honneur, et utilise sans gêne toutes les Cartes Interdites.⏎⏎Elle fabrique des poupées représentant les adversaires qu'elle a battu en duel pour les ajouter à sa collection. Si elle fabrique la poupée d'une personne et qu'elle ne lui plaît pas, elle ne la rajoutera pas à sa collection. On peut redouter le pire quand à ce qu'il en advient. | Camula est une membre des Cavaliers de l'Ombre, un groupe à la recherche des clés spirituelles.⏎C'est une vampire.⏎⏎Le Deck de Camula est constitué de Cartes Monstre de type Zombie tels que les vampires.⏎Elle commande des chauves-souris avec ses yeux écarlates pour qu'ils espionnent le Deck de son adversaire. Elle peut ensuite adapter sa tactique en fonction du jeu adverse. Elle combat en duel sans faire preuve de fierté ni même d'honneur, et utilise sans gêne toutes les Cartes Interdites.⏎⏎Elle fabrique des poupées représentant les adversaires qu'elle a battus en duel pour les ajouter à sa collection. Si elle fabrique la poupée d'une personne et qu'elle ne lui plaît pas, elle ne la rajoutera pas à sa collection. On peut redouter le pire quant à ce qu'il en advient. |
| strTbl_f.bin | 24 | Tania est une membre des Cavaliers de l'Ombre, un groupe à la recherche des clés spirituelles.⏎C'est une amazone.⏎⏎Bien que la plupart des Cavaliers de l'Ombre soient de nature mauvaise, Tania est plutôt joviale et a une personnalité agréable.⏎Elle désire davantage trouver l'homme de sa vie que les clés spirituelles.⏎⏎Il va de soi que son Deck est principalement constitué de cartes amazones. Elle mène ses duels avec force et conviction.⏎⏎Qu'adviendra-t'il de l'homme qu'elle choisira pour compagnon ? Voilà une question que tout le monde se pose. | Tania est une membre des Cavaliers de l'Ombre, un groupe à la recherche des clés spirituelles.⏎C'est une amazone.⏎⏎Bien que la plupart des Cavaliers de l'Ombre soient de nature mauvaise, Tania est plutôt joviale et a une personnalité agréable.⏎Elle désire davantage trouver l'homme de sa vie que les clés spirituelles.⏎⏎Il va de soi que son Deck est principalement constitué de cartes amazones. Elle mène ses duels avec force et conviction.⏎⏎Qu'adviendra-t-il de l'homme qu'elle choisira pour compagnon ? Voilà une question que tout le monde se pose. |
| strTbl_f.bin | 25 | Don Zaloog est un membre des Cavaliers de l'Ombre, un groupe à la recherche des clés spirituelles.⏎C'est aussi le chef d'un gang de voleurs appellé le Scorpion Noir.⏎Don Zaloog s'est déguisé pour s'infiltrer dans la Duel Académie. Il vaut mieux ne pas se fier à son apparence. C'est un habile criminel. | Don Zaloog est un membre des Cavaliers de l'Ombre, un groupe à la recherche des clés spirituelles.⏎C'est aussi le chef d'un gang de voleurs appelé le Scorpion Noir.⏎Don Zaloog s'est déguisé pour s'infiltrer dans la Duel Académie. Il vaut mieux ne pas se fier à son apparence. C'est un habile criminel. |
| strTbl_f.bin | 27 | Le Titan Noir a été ressucité en tant que "Duelliste de l'Ombre". C'est un membre des Cavaliers de l'Ombre, un groupe à la recherche des clés spirituelles.⏎⏎Bien qu'il soit maintenant un Duelliste de l'Ombre, son apparence n'a pas changé.⏎Il avait déjà l'air d'un Duelliste de l'Ombre avant même d'en devenir un.⏎⏎Il utilise depuis longtemps des cartes d'archi-démons, mais elles sont devenus bien plus puissantes maintenant. | Le Titan Noir a été ressuscité en tant que "Duelliste de l'Ombre". C'est un membre des Cavaliers de l'Ombre, un groupe à la recherche des clés spirituelles.⏎⏎Bien qu'il soit maintenant un Duelliste de l'Ombre, son apparence n'a pas changé.⏎Il avait déjà l'air d'un Duelliste de l'Ombre avant même d'en devenir un.⏎⏎Il utilise depuis longtemps des cartes d'archi-démons, mais elles sont devenues bien plus puissantes maintenant. |
| strTbl_f.bin | 30 | Kagemaru est le fondateur de l'Académie.⏎⏎C'est dans l'espoir de ressusciter les cartes des Bêtes Sacrées qu'il a crée l'Académie pour recruter de jeunes talents.⏎S'il peut ramener les Bêtes Sacrées à la vie, il pourra ainsi utiliser l'énergie générée pour obtenir la jeunesse éternelle. | Kagemaru est le fondateur de l'Académie.⏎⏎C'est dans l'espoir de ressusciter les cartes des Bêtes Sacrées qu'il a créé l'Académie pour recruter de jeunes talents.⏎S'il peut ramener les Bêtes Sacrées à la vie, il pourra ainsi utiliser l'énergie générée pour obtenir la jeunesse éternelle. |
| strTbl_f.bin | 31 | C'est un ancien élève de l'Obélisque Bleu.⏎Il était excellent dans ses études, mais sa technique pour piocher les cartes manquait de précision.⏎Cette faiblesse l'a poussé à vivre une vie de reclus dans les montagnes.⏎Il y a suivit un entrainement sévère afin de remédier à cette faiblesse.⏎⏎Ironiquement, sa technique de tirage s'est améliorée mais ayant passé beaucoup de temps dans les montagnes, ses autres compétences ont diminuées. | C'est un ancien élève de l'Obélisque Bleu.⏎Il était excellent dans ses études, mais sa technique pour piocher les cartes manquait de précision.⏎Cette faiblesse l'a poussé à vivre une vie de reclus dans les montagnes.⏎Il y a suivi un entraînement sévère afin de remédier à cette faiblesse.⏎⏎Ironiquement, sa technique de tirage s'est améliorée mais ayant passé beaucoup de temps dans les montagnes, ses autres compétences ont diminué. |
| strTbl_f.bin | 34 | Mindy est la Fangirl B - une fan et disciple d'Alexia.⏎Elle a les manières d'une dame dans son comportement et son language, mais ses propos sont souvent empoisonnés.⏎Elle aime donner des notes aux garçons et à même un fait un classement.⏎⏎Mindy utilise un Deck rempli de beau garçons qui s'appelle le "Deck des beaux gosses".⏎Elle a reussi à rentrer dans le dortoir de l'Obélisque Bleu en utilisant un Deck de Fan girl, donc les gens pensent qu'elle doit être une duelliste de talent. | Mindy est la Fangirl B - une fan et disciple d'Alexia.⏎Elle a les manières d'une dame dans son comportement et son langage, mais ses propos sont souvent empoisonnés.⏎Elle aime donner des notes aux garçons et a même fait un classement.⏎⏎Mindy utilise un Deck rempli de beaux garçons qui s'appelle le "Deck des beaux gosses".⏎Elle a réussi à rentrer dans le dortoir de l'Obélisque Bleu en utilisant un Deck de Fan girl, donc les gens pensent qu'elle doit être une duelliste de talent. |
| strTbl_f.bin | 35 | Wheeler est un chimpanzé de laboratoire.⏎Il a grandit dans un centre de recherche sur l'île de l'Académie. Il ne sait pas jouer au golf, mais c'est un duelliste de qualité.⏎Les autres chimpanzés ne sont pas capable de parler mais Wheeler est équipé d'une machine qui lui permet de communiquer, bien que les mots ne sortent pas de sa bouche.⏎⏎Son Deck est bien évidement constitué de cartes de singe. | Wheeler est un chimpanzé de laboratoire.⏎Il a grandi dans un centre de recherche sur l'île de l'Académie. Il ne sait pas jouer au golf, mais c'est un duelliste de qualité.⏎Les autres chimpanzés ne sont pas capables de parler mais Wheeler est équipé d'une machine qui lui permet de communiquer, bien que les mots ne sortent pas de sa bouche.⏎⏎Son Deck est bien évidemment constitué de cartes de singe. |
| strTbl_f.bin | 41 | C'est une carte spirituelle qui tente de redevenir humaine, mais pour cela elle a besoin de sacrifier une personne.⏎⏎Personne ne connait ses intentions une fois qu'il sera revenu à la vie.⏎⏎Sa carte principale est lui-même. Il peut annuler les effets des Cartes Pièges. Il aurait également d'autres pouvoirs en tant que carte spirituelle. | C'est une carte spirituelle qui tente de redevenir humaine, mais pour cela elle a besoin de sacrifier une personne.⏎⏎Personne ne connait ses intentions une fois qu'il sera revenu à la vie.⏎⏎Sa carte principale est lui-même. Il peut annuler les effets des Cartes Piège. Il aurait également d'autres pouvoirs en tant que carte spirituelle. |
| strTbl_f.bin | 43 | Elle fait partie du personnel de l'Académie et travaille dans le magasin de carte.⏎Elle est gentille, mais se met en colère quand un étudiant l'appelle "madame" car elle ne pense pas être encore si vieille.⏎⏎Elle s'intéresse aux duels depuis quelque temps. | Elle fait partie du personnel de l'Académie et travaille dans le magasin de cartes.⏎Elle est gentille, mais se met en colère quand un étudiant l'appelle "madame" car elle ne pense pas être encore si vieille.⏎⏎Elle s'intéresse aux duels depuis quelque temps. |
| strTbl_f.bin | 44 | Elle fait partie du personnel de l'Académie et travaille dans le magasin de carte.⏎Elle se considère aussi comme la mascotte de l'Académie, et elle porte un déguisement pour les évènements importants.⏎⏎Elle s'intéresse aux duels depuis quelque temps. | Elle fait partie du personnel de l'Académie et travaille dans le magasin de cartes.⏎Elle se considère aussi comme la mascotte de l'Académie, et elle porte un déguisement pour les évènements importants.⏎⏎Elle s'intéresse aux duels depuis quelque temps. |
| strTbl_f.bin | 51 | C'est un membre des Cavaliers de l'Ombre - un groupe à la recherche des clés spirituelles.⏎C'est un pratiquant de l'art des "Duels Obscurs". Le perdant d'un tel duel a son âme prisonnière d'une carte.⏎Sa véritalbe identité est inconnu,⏎⏎Il utilise un Deck de dragon avec comme carte prinicipale "Dragon des Ténèbres aux Yeux Rouges".⏎Il veut faire du monde entier un énorme brasier. | C'est un membre des Cavaliers de l'Ombre - un groupe à la recherche des clés spirituelles.⏎C'est un pratiquant de l'art des "Duels Obscurs". Le perdant d'un tel duel a son âme prisonnière d'une carte.⏎Sa véritable identité est inconnue.⏎⏎Il utilise un Deck de dragon avec comme carte principale "Dragon des Ténèbres aux Yeux Rouges".⏎Il veut faire du monde entier un énorme brasier. |
| strTbl_f.bin | 52 | Profile du directeur Sheppard | Profil du Chancelier Sheppard |
| strTbl_f.bin | 17 | Total des dégâts Directes | Total des dégâts directs |
| strTbl_f.bin | 33 | Nombre de Cartes Pièges activées | Nombre de Cartes Piège activées |
| strTbl_f.bin | 80 | Bonus "Retour dégâts max"  | Bonus "Retour dégâts max" |
| strTbl_f.bin | 82 | Bonus "Dégat en combat" | Bonus "Dégât en combat" |
| strTbl_f.bin | 94 | Bonus "Toute les Zones⏎Carte Monstre utilisées" | Bonus "Toutes les Zones⏎Carte Monstre utilisées" |
| strTbl_f.bin | 123 | Tu as gagné 10 Duels ou plus. | Tu as gagné 10 Duels ou plus contre chaque personnage affrontable. |
| strTbl_f.bin | 137 | Tu as exécuté 10 Invocations Spéciales en Retirant de cartes du jeu depuis le Cimetière pendant le Duel. | Tu as exécuté 10 Invocations Spéciales en retirant des cartes du jeu depuis le Cimetière pendant le Duel. |
| strTbl_f.bin | 155 | Tu as remporté le Duel en obligeant ton adversaire a se défausser de toutes les cartes de son Deck. | Tu as remporté le Duel en obligeant ton adversaire à se défausser de toutes les cartes de son Deck. |
| strTbl_f.bin | 159 | Gagner pendant le tour de votre adversaire. | Tu as gagné pendant le tour de ton adversaire. |
| strTbl_f.bin | 160 | Gagner le Duel en utilisant l'Effet de "Éxodia l'Interdit". | Tu as gagné le Duel en utilisant l'effet de "Exodia l'Interdit". |
| strTbl_f.bin | 161 | Gagner le Duel en utilisant l'Effet de "Tableau de la Destinée". | Tu as gagné le Duel en utilisant l'effet de "Tableau de la Destinée". |
| strTbl_f.bin | 162 | Gagner le Duel en utilisant l'Effet de "Compte à Rebours Final". | Tu as gagné le Duel en utilisant l'effet de "Compte à Rebours Final". |
| strTbl_f.bin | 229 | Tu as obtenu le "Sandwich à l'oeuf d'or". | Tu as obtenu le "Sandwich à l'œuf d'or". |
| strTbl_f.bin | 255 | 2è round | 2e round |
| strTbl_f.bin | 256 | 3è round | 3e round |
| strTbl_f.bin | 258 | Refaire un Duel avec les même paramètres ? | Refaire un Duel avec les mêmes paramètres ? |
| help_strtbl_contents.bin | 8 | À propos des carte | À propos des cartes |
| help_strtbl_contents.bin | 13 | ■ Les titres finissent ici. Les titres sont affichées ci-dessous. ■ | ■ Les titres finissent ici. Les titres sont affichés ci-dessous. ■ |

(... altre 214 righe nel CSV)

## A6. Etichetta [CARTA MAGIA] / [CARTA TRAPPOLA] della carta grande nel duello

In tutti i `duel/basic_<regione><lingua>.ehp` l'etichetta era in inglese (hash `c2268340`): `apply_to_iso.py` la sostituisce con `card_spell_trap.gim` di `field/always_<lingua>_<lingua>.ehp` (hash `9622cd75`).

| archivio | membro | hash originale | hash nuovo |
|---|---|---|---|
| /PSP_GAME/USRDIR/duel/basic_bf.ehp | card_spell_trap.gim | c2268340 | 6fd4b083 |
| /PSP_GAME/USRDIR/duel/basic_ff.ehp | card_spell_trap.gim | c2268340 | 6fd4b083 |
| /PSP_GAME/USRDIR/duel/basic_gf.ehp | card_spell_trap.gim | c2268340 | 6fd4b083 |
| /PSP_GAME/USRDIR/duel/basic_if.ehp | card_spell_trap.gim | c2268340 | 6fd4b083 |
| /PSP_GAME/USRDIR/duel/basic_sf.ehp | card_spell_trap.gim | c2268340 | 6fd4b083 |
| /PSP_GAME/USRDIR/duel/basic_uf.ehp | card_spell_trap.gim | c2268340 | 6fd4b083 |

## A7. File della ISO toccati e dettagli tecnici

179 archivi `.ehp` risultano diversi dall'originale (tutte le lingue insieme, perche' la ISO e' unica; elenco in `docs/changes_fr/touched_files.csv`). Gli altri file (video, audio, eseguibile `EBOOT.BIN`, `PARAM.SFO`) sono identici. Differenze tecniche non testuali: `*-ptrs.txt` (offset assoluti dei membri, ricalcolati quando una tabella cambia lunghezza), nuova posizione degli archivi in fondo alla ISO.

## A8. Cosa NON si puo' cambiare (limiti del gioco)

- Il **nome del parlante** nella casella del dialogo (es. "Preside Sheppard"/"Cancelliere" in italiano, "Doyen Sheppard" in francese, "Rector Sheppard" in spagnolo) sta nell'EBOOT cifrato: non modificabile.
- Testi disegnati dal gioco con il suo font (dialoghi, nomi, descrizioni nel deck, menu a tendina, tastiera di sistema, schermata di scelta lingua) non sono sostituibili dal texture pack: si cambiano solo nella ISO.
- Le 438 texture di mappa/sfondi non sono sostituite (il gioco ne cambia la palette): limite del pack di MikeyMK, non del nostro lavoro.

---

# B. TEXTURE PACK

## B1. Provenienza e struttura

Base: **Yu-Gi-Oh! GX Tag Force 1 HD Remastered** di **MikeyMK** (pack USA `ULUS10136`) e carte HD di **chrisfand**, adattati alla ISO europea `ULES00600`. Il progetto non ridistribuisce il pack di terzi (`PERMESSI_AUTORI.md`): il patcher se lo fa dare dall'utente. Il nostro lavoro: (1) rimappare gli **hash** del pack USA su quelli EU (`tools/gen_ini.py`), (2) rifare nella lingua carte e scritte dell'interfaccia, (3) correggere i testi, (4) `upscale_extra` per le texture non coperte.

PPSSPP riconosce una texture dall'**hash dei suoi pixel** (xxhash dei dati, `gim.data_hash`); ogni riga del `textures.ini` e' `0000000000000000<hash8> = percorso/png`. I PNG sono **4x** l'originale e ridisegnano esattamente la stessa area. Texture identiche tra lingue hanno lo stesso hash: la sostituzione vale per tutte (vedi `docs/TEXTURE_INVENTORY.md`).

### Struttura reale (da `docs/changes_fr/pack_structure.csv`)
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
| moduli/fr | cards/ | 5675 | 1023.9 | frame, large_fr, small_fr, tiny_fr |
| moduli/fr | fr.ini | 1 | 0.01 |  |
| moduli/fr | intro/ | 2 | 0.4 | title_screen |
| moduli/fr | ui_fr/ | 93 | 8.1 | fogli_icone, fogli_icone.ini, lettere_esito, lettere_esito.ini, menu_liste, menu_liste.ini, schede_deck, schede_deck.ini, schede_ricette, schede_ricette.ini ... |

Ogni lingua tranne l'italiano e' un **modulo** (`PSP/TEXTURES/modules/fr`) da comporre sopra il pack di base con `tools/compose_pack.py BASE MODULI CARD_DIR OUT fr [--copia]`: copia il base e **solo** le cartelle `cards`, `intro` e `ui_fr` del modulo (hard link o copia), poi `module_ini.py` riscrive i `textures.ini`: le righe delle carte localizzate puntano a `cards/small_fr`/`large_fr` e le righe di `fr.ini` **sostituiscono** quelle del base con la stessa chiave (hash).

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

Cartelle della lingua: `frame` (2 file), `large_fr` (2833 file), `small_fr` (2833 file), `tiny_fr` (7 file). Ogni carta ha una **piccola HD** (nome + descrizione + tipo, rigenerata con font liberi OFL: XCharter Bold per nomi/tipo/etichette, Libre Baskerville per gli effetti, Newsreader Italic per i Normali, PT Serif Caption per Magie/Trappole, Charis SIL per i glifi mancanti) e una **grande HD** (solo il nome sulla cornice). In piu': la **tabella degli attributi** con le parole della lingua (`cards/frame/icons_attribute_race_<l>.png`, `attributes.py`), l'**etichetta Magia/Trappola** (`icons_spell_trap_<l>.png`, `label_it.py` / `extract_labels.py` -> `dati/label_eu_<codice>_128x32.png`) e l'**atlante delle miniature** del deck (`tiny_<l>`, `tiny_atlas.py` + `tiny_fragment.py`).

Quando cambia il testo di una carta (sezione A2) vanno rigenerate le sue immagini: **266 carte** nel francese. Elenco in `docs/changes_fr/card_images.csv`. Comando: `python tools/generate_language.py fr PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` (senza ID rigenera tutte: 2.833 + 2.833, ~930 MB).

Tipografia: spazio non separabile prima di `: ; ! ?` e virgolette « ».

## B3. Interfaccia HD in francese (`ui_fr`)

**85 texture** (`docs/changes_fr/ui_textures.csv`: file, hash PPSSPP, famiglia, script, dimensioni originale/HD, neutra/specifica, origine nella ISO). Per famiglia: fogli_icone 3, lettere_esito 22, menu_liste 6, schede_deck 10, schede_ricette 11, schermata_vs 14, scritte_duello 13, tutorial 6. Di queste 0 sono neutre (stesso hash in tutte le lingue) e 85 specifiche. Ogni famiglia ha uno script in `tools/ui_textures/<famiglia>.py` (lettura `TF1_LANG`): ridisegna le scritte texture per texture partendo dall'originale a bassa risoluzione della ISO e dallo stile del pack inglese; stessa area e stesse posizioni (il gioco ritaglia da rettangoli fissi); un font/peso/linea di base/ombra per scritta; font liberi (`alt_font.py`).

| famiglia | texture | script | archivio ISO sorgente | testi della lingua |
|---|---|---|---|---|
| fogli_icone | 3 | `tools/ui_textures/icon_sheets.py` | deck/all_f.ehp, shop/all_f.ehp, field/always_* | `icon04`, `s_pack` (ÉPUISÉ), `panel` (frammento "hetés"); `pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01` restano con "NEW" come nell'originale francese |
| lettere_esito | 22 | `tools/ui_textures/result_letters.py` | duel/basic_ff.ehp | TU AS GAGNÉ · TU AS PERDU · EGALITE (senza accento: nel pareggio non esiste la tessera É) |
| menu_liste | 6 | `tools/ui_textures/menu_lists.py` | title_menu/title_menu_f.ehp, duel/result/result_f.ehp, field/always_bri_<cod>.ehp | MENU PRINCIPAL · SAISIR NOM · LISTE CARTES TÉLÉCHARGÉE · PUZZLE DUEL · OPTIONS · SÉLECTION DE LA LANGUE · LISTE DE GROUPE... · RÉSULTAT DU DUEL · APPUYEZ SUR LA TOUCHE START · GAGNÉ/ÉGALITÉ/PERDU · Dimanche...Samedi · Mai Juillet Juin Août · jours / avant le tournoi · Matin / Soir |
| schede_deck | 10 | `tools/ui_textures/deck_screens.py` | deck/all_f.ehp, labo/*.ehp, shop/all_f.ehp | Coffre ×2, Location ×3, Labo, Convertisseur, "Types de cartes acquis", "Cartes achetées" (+ frammento), ENTRÉE |
| schede_ricette | 11 | `tools/ui_textures/recipe_screens.py` | deck/recipe_view_f.ehp, title_menu/title_menu_f.ehp, database/limitlist.ehp | Personnage / Utilisateur / Téléchargée / Limitée / Semi-limitée / Interdite / Échange (nel gioco originale "Scambia" era un residuo italiano) |
| schermata_vs | 14 | `tools/ui_textures/vs_screen.py` | duel/start/start_e.ehp (membri _f), start_all.ehp, start_f.ehp | DUEL / NORMAL / TAG · DEUXIÈME À JOUER / PREMIER À JOUER · 1er/2e/3e round · Mode Un Duel / Mode Match · GAGNÉ/PERDU/EGALITE · 1er JOUEUR / 2e JOUEUR · JOUEUR |
| scritte_duello | 13 | `tools/ui_textures/duel_texts.py` | duel/basic_ff.ehp | Chaîne · TOUR (blu/rosso) · TOUR DU JOUEUR SUIVANT (taglio dopo SUIV) · DÉMARRER DUEL (taglio dopo DU) · Attaque Directe! · `card_icon03` e' nella cartella `upscale_extra` (B4) |
| tutorial | 6 | `tools/ui_textures/tutorial.py` | tutorial/tutorial_f.ehp (tuto_duelimg01..06) | "Ton adversaire a déclaré le duel." / "Activer l'effetto de la carte ?" · OUI/NON · 5 cartine; geometria diversa (dialogo a 2 righe) |

Regole di qualita' (valgono per ogni lingua): lettere regolari, mai deformate una per una; stessa area dell'originale; niente sfocature; il testo e' quello dell'originale della lingua (si correggono solo errori evidenti: residui di altre lingue, accenti); pixel art **non** levigata senza conferma; geometrie sempre misurate sull'originale.

### Testi disegnati: originale -> HD
Tabella letta a occhio, texture per texture: `docs/changes_fr/texture_texts_fr.md`. Differenze rispetto all'originale: `DEMARRER` -> `DÉMARRER`, `SCAMBIA`/`Scambia` -> `ÉCHANGE`/`Échange`, `2è/3è round` -> `2e/3e round`; tutto il resto riscrive le stesse parole.

### Elenco di ogni texture
(tutte le 85 righe, da `ui_textures.csv`)

| file nel pack | hash | famiglia | originale px | HD px | tipo | origine ISO |
|---|---|---|---|---|---|---|
| ui_fr/fogli_icone/all_f__icon04.png | 98af30ad | fogli_icone | 128x128 | 512x512 | SPECIFICA | deck/all_f.ehp:icon04.gim |
| ui_fr/fogli_icone/all_f__panel.png | a07a7109 | fogli_icone | 256x256 | 1024x1024 | SPECIFICA | shop/all_f.ehp:panel.gim |
| ui_fr/fogli_icone/all_f__s_pack.png | 75bfeec6 | fogli_icone | 256x256 | 1024x1024 | SPECIFICA | shop/all_f.ehp:s_pack.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100002.png | d9f0ff03 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_draw100002.gim; duel/basic_ff.ehp:duel_draw100002.gim; duel/basic_gf.ehp:duel_draw100002.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100004.png | 0db73058 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_draw100004.gim; duel/basic_ff.ehp:duel_draw100004.gim; duel/basic_gf.ehp:duel_draw100004.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100006.png | d6fbb9b3 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_draw100006.gim; duel/basic_ff.ehp:duel_draw100006.gim; duel/basic_gf.ehp:duel_draw100006.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100008.png | ec450799 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_draw100008.gim; duel/basic_ff.ehp:duel_draw100008.gim; duel/basic_gf.ehp:duel_draw100008.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100010.png | 15e9ccb0 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_draw100010.gim; duel/basic_ff.ehp:duel_draw100010.gim; duel/basic_gf.ehp:duel_draw100010.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100012.png | b807cf15 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_draw100012.gim; duel/basic_ff.ehp:duel_draw100012.gim; duel/basic_gf.ehp:duel_draw100012.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100002.png | 0047e8d4 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_lose100002.gim; duel/basic_ff.ehp:duel_lose100002.gim; duel/basic_gf.ehp:duel_lose100002.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100004.png | 80a96d0a | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_lose100004.gim; duel/basic_ff.ehp:duel_lose100004.gim; duel/basic_gf.ehp:duel_lose100004.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100006.png | fde82bc2 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_lose100006.gim; duel/basic_ff.ehp:duel_lose100006.gim; duel/basic_gf.ehp:duel_lose100006.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100008.png | e7309c53 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_lose100008.gim; duel/basic_ff.ehp:duel_lose100008.gim; duel/basic_gf.ehp:duel_lose100008.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100010.png | de35da96 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_lose100010.gim; duel/basic_ff.ehp:duel_lose100010.gim; duel/basic_gf.ehp:duel_lose100010.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100012.png | b810694f | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_lose100012.gim; duel/basic_ff.ehp:duel_lose100012.gim; duel/basic_gf.ehp:duel_lose100012.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100014.png | bcee1236 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_lose100014.gim; duel/basic_ff.ehp:duel_lose100014.gim; duel/basic_gf.ehp:duel_lose100014.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100016.png | 835c6fa4 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_lose100016.gim; duel/basic_ff.ehp:duel_lose100016.gim; duel/basic_gf.ehp:duel_lose100016.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100002.png | 7c4c0b02 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_win100002.gim; duel/basic_ff.ehp:duel_win100002.gim; duel/basic_gf.ehp:duel_win100002.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100004.png | 277593da | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_win100004.gim; duel/basic_ff.ehp:duel_win100004.gim; duel/basic_gf.ehp:duel_win100004.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100006.png | 0b30b8d8 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_win100006.gim; duel/basic_ff.ehp:duel_win100006.gim; duel/basic_gf.ehp:duel_win100006.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100008.png | 4649bee5 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_win100008.gim; duel/basic_ff.ehp:duel_win100008.gim; duel/basic_gf.ehp:duel_win100008.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100010.png | bc63bab3 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_win100010.gim; duel/basic_ff.ehp:duel_win100010.gim; duel/basic_gf.ehp:duel_win100010.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100012.png | 694e26bf | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_win100012.gim; duel/basic_ff.ehp:duel_win100012.gim; duel/basic_gf.ehp:duel_win100012.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100014.png | a2ac32fb | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:duel_win100014.gim; duel/basic_ff.ehp:duel_win100014.gim; duel/basic_gf.ehp:duel_win100014.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100016.png | 063d6787 | lettere_esito | 64x32 | 256x128 | SPECIFICA | duel/basic_bf.ehp:duel_win100016.gim; duel/basic_ff.ehp:duel_win100016.gim; duel/basic_gf.ehp:duel_win100016.gim |
| ui_fr/menu_liste/always_bri_fra__story_sys02.png | 94d129f8 | menu_liste | 256x128 | 1024x512 | SPECIFICA | field/always_bri_fra.ehp:story_sys02.gim; field/always_fra_fra.ehp:story_sys02.gim; field/always_ger_fra.ehp:story_sys02.gim |
| ui_fr/menu_liste/result_f__menu01.png | 72607cdb | menu_liste | 256x64 | 1024x256 | SPECIFICA | duel/result/result_f.ehp:menu01.gim |
| ui_fr/menu_liste/result_f__menu02.png | f319c24e | menu_liste | 256x128 | 1024x512 | SPECIFICA | duel/result/result_f.ehp:menu02.gim |
| ui_fr/menu_liste/title_menu_f__m_menu_title01.png | 5d96e868 | menu_liste | 256x128 | 1024x512 | SPECIFICA | title_menu/title_menu_f.ehp:m_menu_title01.gim |
| ui_fr/menu_liste/title_menu_f__press_start0003.png | 773e4c91 | menu_liste | 256x16 | 1024x64 | SPECIFICA | title_menu/title_menu_f.ehp:press_start0003.gim |
| ui_fr/menu_liste/title_menu_f__trnsmt02.png | 13aa38da | menu_liste | 256x256 | 1024x1024 | SPECIFICA | title_menu/title_menu_f.ehp:trnsmt02.gim |
| ui_fr/schede_deck/all_f__d_window00008.png | a61d1508 | schede_deck | 128x32 | 512x128 | SPECIFICA | deck/all_f.ehp:d_window00008.gim |
| ui_fr/schede_deck/all_f__d_window00033.png | 4288e72f | schede_deck | 256x32 | 1024x128 | SPECIFICA | deck/all_f.ehp:d_window00033.gim |
| ui_fr/schede_deck/all_f__d_window00051.png | b6dda200 | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_f.ehp:d_window00051.gim |
| ui_fr/schede_deck/all_f__d_window00062.png | a5f39742 | schede_deck | 128x32 | 512x128 | SPECIFICA | deck/all_f.ehp:d_window00062.gim; labo/conv_machine.ehp:window_f0016.gim; title_menu/title_menu_f.ehp:t_window0015.gim |
| ui_fr/schede_deck/all_f__d_window00101.png | 55101663 | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_f.ehp:d_window00101.gim; labo/rental.ehp:window_f0008.gim |
| ui_fr/schede_deck/all_f__tab_title.png | 952c742b | schede_deck | 256x32 | 1024x128 | SPECIFICA | shop/all_f.ehp:tab_title.gim |
| ui_fr/schede_deck/conv_machine__window_f0009.png | 1d497183 | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/conv_machine.ehp:window_f0009.gim; labo/conv_machine.ehp:window_f0026.gim |
| ui_fr/schede_deck/password__key_f0027.png | 9d980a76 | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/password.ehp:key_f0027.gim |
| ui_fr/schede_deck/rental__window_f0015.png | 784336da | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/rental.ehp:window_f0015.gim |
| ui_fr/schede_deck/rental__window_f0026.png | 19e8234f | schede_deck | 64x32 | 256x128 | SPECIFICA | labo/rental.ehp:window_f0026.gim |
| ui_fr/schede_ricette/limitlist__window_f0002.png | 99e75f0f | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_f0002.gim |
| ui_fr/schede_ricette/limitlist__window_f0004.png | 05594cc2 | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_f0004.gim |
| ui_fr/schede_ricette/limitlist__window_f0012.png | 2aa7c7b9 | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_f0012.gim |
| ui_fr/schede_ricette/recipe_view_f__recipe010008.png | 7195a33d | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_f.ehp:recipe010008.gim; title_menu/title_menu_f.ehp:recipe_sel00002.gim |
| ui_fr/schede_ricette/recipe_view_f__recipe010015.png | 244adfce | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_f.ehp:recipe010015.gim; title_menu/title_menu_f.ehp:recipe_sel00009.gim |
| ui_fr/schede_ricette/recipe_view_f__recipe010027.png | 452b2fc3 | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_f.ehp:recipe010027.gim; title_menu/title_menu_f.ehp:recipe_sel00020.gim |
| ui_fr/schede_ricette/recipe_view_f__recipe010029.png | 6aefce83 | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_f.ehp:recipe010029.gim; title_menu/title_menu_f.ehp:recipe_sel00022.gim |
| ui_fr/schede_ricette/recipe_view_f__recipe010031.png | 4847fe90 | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_f.ehp:recipe010031.gim; title_menu/title_menu_f.ehp:recipe_sel00024.gim |
| ui_fr/schede_ricette/title_menu_f__recipe_sel00033.png | a1b7db60 | schede_ricette | 128x32 | 512x128 | SPECIFICA | title_menu/title_menu_f.ehp:recipe_sel00033.gim |
| ui_fr/schede_ricette/title_menu_f__t_window0008.png | 3d9ecfb3 | schede_ricette | 64x32 | 256x128 | SPECIFICA | title_menu/title_menu_f.ehp:t_window0008.gim |
| ui_fr/schede_ricette/title_menu_f__t_window0026.png | 99a306c5 | schede_ricette | 64x32 | 256x128 | SPECIFICA | title_menu/title_menu_f.ehp:t_window0026.gim |
| ui_fr/schermata_vs/start_all__jyanken20_f0005.png | a702e687 | schermata_vs | 256x32 | 1024x128 | SPECIFICA | duel/start/start_all.ehp:jyanken20_f0005.gim; duel/start/start_e.ehp:jyanken20_f0005.gim; duel/start/start_f.ehp:jyanken20_f0005.gim |
| ui_fr/schermata_vs/start_all__jyanken20_f0007.png | ffb03b77 | schermata_vs | 256x32 | 1024x128 | SPECIFICA | duel/start/start_all.ehp:jyanken20_f0007.gim; duel/start/start_e.ehp:jyanken20_f0007.gim; duel/start/start_f.ehp:jyanken20_f0007.gim |
| ui_fr/schermata_vs/start_all__vs_much1_f0001.png | f00cc75b | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much1_f0001.gim; duel/start/start_e.ehp:vs_much1_f0001.gim; duel/start/start_f.ehp:vs_much1_f0001.gim |
| ui_fr/schermata_vs/start_all__vs_much2_f0001.png | ab4234f3 | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much2_f0001.gim; duel/start/start_e.ehp:vs_much2_f0001.gim; duel/start/start_f.ehp:vs_much2_f0001.gim |
| ui_fr/schermata_vs/start_all__vs_much3_f0001.png | 3ee93ceb | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much3_f0001.gim; duel/start/start_e.ehp:vs_much3_f0001.gim; duel/start/start_f.ehp:vs_much3_f0001.gim |
| ui_fr/schermata_vs/start_e__d_menu01_f.png | e3cb007e | schermata_vs | 256x256 | 1024x1024 | SPECIFICA | duel/start/start_e.ehp:d_menu01_f.gim; duel/start/start_f.ehp:d_menu01_f.gim; duel/start/start_g.ehp:d_menu01_f.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_1_f0005.png | 2938884b | schermata_vs | 256x32 | 1024x128 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_f0005.gim; duel/start/start_f.ehp:vs_bg01_1_f0005.gim; duel/start/start_g.ehp:vs_bg01_1_f0005.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_1_f0007.png | 43aaac68 | schermata_vs | 256x64 | 1024x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_f0007.gim; duel/start/start_f.ehp:vs_bg01_1_f0007.gim; duel/start/start_g.ehp:vs_bg01_1_f0007.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_1_f0008.png | 5522ab17 | schermata_vs | 256x64 | 1024x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_f0008.gim; duel/start/start_f.ehp:vs_bg01_1_f0008.gim; duel/start/start_g.ehp:vs_bg01_1_f0008.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_1_f0012.png | 4b1c6b9b | schermata_vs | 128x32 | 512x128 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_f0012.gim; duel/start/start_f.ehp:vs_bg01_1_f0012.gim; duel/start/start_g.ehp:vs_bg01_1_f0012.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_1_f0014.png | 63905ec2 | schermata_vs | 128x64 | 512x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_f0014.gim; duel/start/start_f.ehp:vs_bg01_1_f0014.gim; duel/start/start_g.ehp:vs_bg01_1_f0014.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_2_f0001.png | f22ee1c0 | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_2_f0001.gim; duel/start/start_f.ehp:vs_bg01_2_f0001.gim; duel/start/start_g.ehp:vs_bg01_2_f0001.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_2_f0004.png | 9e283fad | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_2_f0004.gim; duel/start/start_f.ehp:vs_bg01_2_f0004.gim; duel/start/start_g.ehp:vs_bg01_2_f0004.gim |
| ui_fr/schermata_vs/start_f__jnk_card01.png | cf2b81ef | schermata_vs | 512x256 | 2048x1024 | SPECIFICA | duel/start/start_f.ehp:jnk_card01.gim |
| ui_fr/scritte_duello/basic_ff__chain010003.png | 9f72a1a4 | scritte_duello | 64x32 | 256x128 | SPECIFICA | duel/basic_bf.ehp:chain010003.gim; duel/basic_ff.ehp:chain010003.gim; duel/basic_gf.ehp:chain010003.gim |
| ui_fr/scritte_duello/basic_ff__chain010005.png | 5a096674 | scritte_duello | 128x32 | 512x128 | SPECIFICA | duel/basic_bf.ehp:chain010005.gim; duel/basic_ff.ehp:chain010005.gim; duel/basic_gf.ehp:chain010005.gim |
| ui_fr/scritte_duello/basic_ff__dilect_atk00001.png | 69b62191 | scritte_duello | 256x32 | 1024x128 | SPECIFICA | duel/basic_bf.ehp:dilect_atk00001.gim; duel/basic_ff.ehp:dilect_atk00001.gim; duel/basic_gf.ehp:dilect_atk00001.gim |
| ui_fr/scritte_duello/basic_ff__dilect_atk00003.png | 9bcff667 | scritte_duello | 128x32 | 512x128 | SPECIFICA | duel/basic_bf.ehp:dilect_atk00003.gim; duel/basic_ff.ehp:dilect_atk00003.gim; duel/basic_gf.ehp:dilect_atk00003.gim |
| ui_fr/scritte_duello/basic_ff__next_player0001.png | 4c3738e7 | scritte_duello | 64x32 | 256x128 | SPECIFICA | duel/basic_bf.ehp:next_player0001.gim; duel/basic_ff.ehp:next_player0001.gim; duel/basic_gf.ehp:next_player0001.gim |
| ui_fr/scritte_duello/basic_ff__next_player0002.png | 3ee74e53 | scritte_duello | 256x32 | 1024x128 | SPECIFICA | duel/basic_bf.ehp:next_player0002.gim; duel/basic_ff.ehp:next_player0002.gim; duel/basic_gf.ehp:next_player0002.gim |
| ui_fr/scritte_duello/basic_ff__next_player0004.png | 84277f2a | scritte_duello | 64x32 | 256x128 | SPECIFICA | duel/basic_bf.ehp:next_player0004.gim; duel/basic_ff.ehp:next_player0004.gim; duel/basic_gf.ehp:next_player0004.gim |
| ui_fr/scritte_duello/basic_ff__next_player0005.png | f0ee3375 | scritte_duello | 256x32 | 1024x128 | SPECIFICA | duel/basic_bf.ehp:next_player0005.gim; duel/basic_ff.ehp:next_player0005.gim; duel/basic_gf.ehp:next_player0005.gim |
| ui_fr/scritte_duello/basic_ff__score-top100011.png | c1e6c591 | scritte_duello | 32x32 | 128x128 | SPECIFICA | duel/basic_bf.ehp:score-top100011.gim; duel/basic_ff.ehp:score-top100011.gim; duel/basic_gf.ehp:score-top100011.gim |
| ui_fr/scritte_duello/basic_ff__score-top100013.png | e0f716eb | scritte_duello | 32x32 | 128x128 | SPECIFICA | duel/basic_bf.ehp:score-top100013.gim; duel/basic_ff.ehp:score-top100013.gim; duel/basic_gf.ehp:score-top100013.gim |
| ui_fr/scritte_duello/basic_ff__start_duel10001.png | 42eb57cb | scritte_duello | 64x64 | 256x256 | SPECIFICA | duel/basic_bf.ehp:start_duel10001.gim; duel/basic_ff.ehp:start_duel10001.gim; duel/basic_gf.ehp:start_duel10001.gim |
| ui_fr/scritte_duello/basic_ff__start_duel10002.png | 66a08b34 | scritte_duello | 256x64 | 1024x256 | SPECIFICA | duel/basic_bf.ehp:start_duel10002.gim; duel/basic_ff.ehp:start_duel10002.gim; duel/basic_gf.ehp:start_duel10002.gim |
| ui_fr/scritte_duello/basic_ff__start_duel10005.png | ef0dcee9 | scritte_duello | 128x32 | 512x128 | SPECIFICA | duel/basic_bf.ehp:start_duel10005.gim; duel/basic_bg.ehp:start_duel10005.gim; duel/basic_ff.ehp:start_duel10005.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg01.png | b79d9f2c | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_f.ehp:tuto_duelimg01.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg02.png | dab05056 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_f.ehp:tuto_duelimg02.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg03.png | 6ab005ac | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_f.ehp:tuto_duelimg03.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg04.png | 9a43109a | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_f.ehp:tuto_duelimg04.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg05.png | 4a668513 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_f.ehp:tuto_duelimg05.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg06.png | 8ee53835 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_f.ehp:tuto_duelimg06.gim |

### Texture che restano come l'originale
`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `parts` sono fogli di icone in pixel art (con NEU/NEW): restano com'erano, coperti dall'ingrandimento `upscale_extra` come nelle altre lingue; il testo non e' stato cambiato. Le texture neutre vengono dal pack di base. In spagnolo anche `score-top` (TURNO) ha lo stesso hash dell'italiano e `card_icon03` e' in `upscale_extra`.

## B4. Il foglio dei numeri del duello (`card_icon03`)

Foglio unico con cifre LP, tempo, tasti e moltiplicatori; hash diverso per lingua. Ricetta scelta dall'utente (`tools/ui_textures/icon03_languages.py`, rilanciare con `--apply`):
- righe 0-180 (cifre piccole e segni, tasti arancioni 1/2/3, cifre grandi 0-9 con "LP", cifre piccole 0-9): **dal pack USA**, pixel art netta;
- celle in cui il gioco europeo differisce dal pack USA (spunta nera, palla grigia, pillola vuota, parola del tempo): **pixel originali ingranditi 4x senza sfumare**; parola del tempo **TEMPS**; la pillola arancione ("Single" nel pack USA) resta **vuota**;
- righe >= 181 (moltiplicatori x1..x12, icone, carte, frecce): dal foglio italiano gia' nel pack (`tools/data/card_icon03_base_it.png`);
- le celle europee si incollano **solo nella loro fascia** di righe (altrimenti rovinano la parte alta delle cifre grandi).

File: it -> `ui_it/scritte_duello/basic_ii__card_icon03.png` (hash 376925c7); fr -> `upscale_extra/3e5482fd.png`; en ee0c44c3; de ffe309a6; es 859eea2b. Anteprime in `confronti/icon03/`.

## B5. Targa del titolo

`python tools/ui_textures/mystic_tomato_title.py fr` genera 2 PNG (`542eff79685c434d`, `705176739829dcf5`, tessere 18 e 19 del fondale di 20 tessere 128x64 `title_menu_i.ehp: main_title00001..00020`) con la carta 4930 nella lingua + la formula "versione" + la bandiera, font PT Sans Bold: **"VERSION TOMATE MYSTIQUE"**. La targa **va inclusa solo per la lingua scelta** (vive in `moduli/fr/intro/title_screen/`); il pack di base originale ha le tessere senza banner. File in questo pack: `moduli/fr/intro/title_screen/00000000542eff79685c434d.png`, `moduli/fr/intro/title_screen/00000000705176739829dcf5.png`.

## B6. `textures.ini` e composizione

`tools/gen_ini.py TOOLS US_INI CARD_DIR OUT_INI i=it +extra_it.ini +ui_it.ini +dati/upscale_extra.ini` converte il `textures.ini` USA in quello EU: le voci non-carta restano (texture neutre = stessi hash); le voci carta sono rigenerate dagli archivi `card/*.cip` EU per le 5 lingue (`i=it` rimappa `cards/large/X.png` -> `cards/large_it/X.png`); aggiunge l'etichetta Magia/Trappola (`extra_it.ini`), le righe `ui_it` e `upscale_extra.ini`. Si fa anche per i 3 stili carte. Se gli stessi pixel esistono in piu' lingue vince la prima in `e i f g s` (per questo atlante, banner e tabella attributi sono "uno per installazione").

Righe `ui_fr` nel `fr.ini`: 85. Frequenza dei prefissi: `docs/changes_fr/ini_lines.csv`. Controllo: ogni riga `ui_fr/...` deve puntare a un file esistente e non devono esserci hash duplicati.

## B7. Installazione e impostazioni

PC: copiare `ULES00600` in `<PPSSPP>/PSP/TEXTURES/` (Android: `textures.zip` in `.../TEXTURES/ULES00600/`, senza estrarlo; rigenerare lo zip con le correzioni). Impostazioni: **Sostituisci texture ON**, risoluzione di rendering **4x**, lingua del gioco = lingua del modulo (la lingua e' scritta nel **salvataggio**). Dopo aver cambiato un solo PNG basta copiarlo e riavviare PPSSPP (cache). Per provare i testi usare la ISO `_definitiva`.

---

# C. SCELTE EDITORIALI

- **Doyen / Chancelier**: dialogo per dialogo, formale -> "Chancelier", informale -> "Doyen"; nelle schede UI "Chancelier Sheppard".
- Punteggiatura francese `! ? : ;` con spazio (anche dopo `》`); "Mode histoire" -> "Mode aventure" (nome vero del menu).
- `Échange` al posto di "Scambia" (residuo italiano); "2e/3e round"; "EGALITE" senza accento; "DÉMARRER DUEL".
- `Piège Continu` e' il termine coerente di tutto il gioco: non si cambia.
- Foglio numeri: cifre/LP dal pack USA, x1..x12 dal foglio italiano, parola del tempo TEMPS.

### Voci del registro delle scelte per questa lingua (`tools/data/editorial_choices.json`)
| id | originale | corretto | ereditata | motivo |
|---|---|---|---|---|
| st01_t01/Scr003E#146 | Mon père a une société qui fabrique de la⏎sauce épicée. | Mon père possède une⏎distillerie de saké. | no | sake al posto di salsa piccante (fedele al giapponese: la famiglia di Chumley fa sake) |
| st01_t01/Scr003E#147 | Il m'en a envoyé avec ma dernière bourse.⏎Je suis prêt à te faire une réduction.⏎Tu veux... | Il m'a envoyé du shochu avec ma dernière bourse.⏎Je suis prêt à te faire une réduction.⏎Tu veux... | no | shochu al posto di salsa piccante |
| st01_t01/Scr003E#150 | Mon père a une société qui fabrique de la⏎sauce épicée. | Mon père possède une⏎distillerie de saké. | no | come 146 |
| st01_t01/Scr003E#151 | Il m'en a envoyé avec ma dernière bourse.⏎Je suis prêt à te faire une réduction.⏎Tu veux... | Il m'a envoyé du shochu avec ma dernière bourse.⏎Je suis prêt à te faire une réduction.⏎Tu veux... | no | come 147 |
| st01_t01/Scr003E#163 | Ouah. Tu as réussi.⏎C'est la 《C026_2》...⏎En bikini ! | Ouah. Tu as réussi.⏎C'est la 《C026_2》...⏎En tenue de servante ! | no | abito da cameriera al posto di bikini (giapponese: メイド服) |
| st01_t01/Scr003E#168 | Ouah. Tu as réussi.⏎C'est la 《C026_2》...⏎En bikini ! | Ouah. Tu as réussi.⏎C'est la 《C026_2》...⏎En tenue de servante ! | no | come 163 |
| st01_t01/Scr003E#188 | Eh bien, je suppose que oui... | None | si | solo italiano: "sto sbavando" era un errore di traduzione (giapponese: "non sono poi così bravo") |
| st01_t01/Scr003E#189 | Hé, tu peux me dessiner quelque chose, alors ?⏎Comme, par exemple, la 《C026_2》 en bikini ! | Hé, tu peux me dessiner quelque chose, alors ?⏎Comme, par exemple, la 《C026_2》 en tenue de servante ! | no | abito da cameriera al posto di bikini |
| st01_t01/Scr003E#191 | Hé, que penses-tu de ça ! | Tiens, utilise cette tenue de servante ! | no | Syrus passa un abito da cameriera come modello (メイド服): col bikini la battuta non aveva senso |
| st01_t01/Scr003E#194 | Eh bien, je suppose que oui... | None | si | come 188 |
| st01_t01/Scr003E#195 | Hé, tu peux me dessiner quelque chose, alors ?⏎Comme, par exemple, la 《C026_2》 en bikini ! | Hé, tu peux me dessiner quelque chose, alors ?⏎Comme, par exemple, la 《C026_2》 en tenue de servante ! | no | come 189 |
| st01_t01/Scr003E#197 | Hé, que penses-tu de ça ! | Tiens, utilise cette tenue de servante ! | no | come 191 |

Altre scelte e la rilettura delle frasi dei duelli: `docs/EDITORIAL_CHOICES.md`.

# D. VERIFICA IN GIOCO

- Visti in gioco (ISO `_definitiva`): titolo con targa, menu, editor del deck.

# E. COME RIGENERARE TUTTO

```
# ISO (tutte le lingue insieme)
python tools/corrections/build_dialogues.py fr
python tools/corrections/generate_card_corrections.py fr CARDINFO_fr.ehp          # carte
python tools/corrections/apply_to_iso.py PSP/GAME/ULES00600_..._EUR.iso PSP/GAME/ULES00600_..._EUR_definitiva.iso
# immagini
python tools/generate_language.py fr PACK CARDINFO US_INI CLEAN_DIR OUT [ID...]
TF1_LANG=fr python tools/ui_textures/<famiglia>.py USRDIR PACK_US <modulo>      # per ognuna delle 8 famiglie (intera!)
python tools/ui_textures/icon03_languages.py --apply ; python tools/ui_textures/mystic_tomato_title.py fr
python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules USRDIR/card OUT fr --copia
# questo documento
python tools/analysis/document_changes.py ISO_ORIG ISO_DEF fr docs/changes_fr
python tools/analysis/document_pack.py ISO_ORIG fr docs/changes_fr
python tools/analysis/text_comparisons.py fr
python tools/analysis/write_changes_document.py fr
```
Input esterni da avere (controlla che esistano): ISO originale, USRDIR estratta (`tools/analysis/extract_usrdir.py`), pack USA di MikeyMK `ULUS10136` (in una cartella fuori dal progetto).

# F. LIMITI E PUNTI APERTI

- Variante opzionale `N`/NOUVEAU al posto di `NEW` nelle 4 texture con wording locale.
- `textures.zip` Android per il francese: non fatto; nessuna prova su telefono.
- Etichette lunghe da verificare in gioco: "Rechercher", "Aucune restriction", "Étiquette".
- Il nome del parlante nella casella del dialogo non e' modificabile (EBOOT cifrato).
