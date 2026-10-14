# Registro delle scelte editoriali

Metodo generale per una nuova lingua: `docs/NEW_LANGUAGE_GUIDE.md`. Questo file raccoglie le **decisioni prese con l'utente** che valgono per il gioco (non solo per una sessione), così che i patcher
specifici per lingua applichino la correzione giusta della propria lingua. Ogni voce dice dove sta il dato, in modo che il patcher
non debba ricavarlo di nuovo dal codice.

Dove vivono le correzioni (tutte lette da `tools/corrections/apply_to_iso.py`):

| Cosa | Dato per lingua | Costruzione |
|---|---|---|
| Dialoghi | `tools/data/dialogue_touchups_<l>.json` (`esatte`, `parti`) + per l'italiano la base `dialogue_corrections_it_base.json` | `build_dialogues.py <l>` -> `dialogue_corrections_<l>.json` |
| Stringhe lunghe dell'interfaccia (aiuti, schede, tutorial) | `tools/corrections/string_rules_<l>.py` | `ui_strings.py` (fatte: fr, it) |
| Carte | `tools/corrections/rules_<l>.py` | `generate_language.py` |
| Scelte comuni a tutte le lingue (questo registro) | `tools/data/editorial_choices.json` | solo docs/controllo: le correzioni sono gia' nei dati sopra |

Regola per le nuove scelte: scriverle **sia** nei dati della lingua **sia** qui, con id, testo originale, testo corretto, motivo.

## Scelte comuni a tutte le lingue

### Scena Syrus + Chumley (`st01_t01/Scr003E`, righe #146-#197): sake e abito da cameriera
Fedele al giapponese; le versioni europee avevano censure/cambi (salsa piccante, bikini).
- Famiglia di Chumley: **distilleria di sake**; il regalo e' **shochu** (non salsa piccante). Righe #146, #147 e copie #150, #151.
- Syrus chiede a Chumley il disegno della **Ragazza Mago Nero (C026) in abito da cameriera** (non in bikini), righe #163, #168, #189, #195.
- Riga #191/#197: Syrus passa un **abito da cameriera** come modello ("Ecco, usa questo ...").
- Solo italiano: righe #188/#194 "Beh, non sono poi così bravo..." (prima "sto sbavando", errore di traduzione).
- Nessuna texture ha varianti cameriera/bikini/sake/salsa (controllati 53 busti, 23 immagini evento, sprite SD, immagini aiuto).
- Dettaglio riga per riga e per lingua: `tools/data/editorial_choices.json` (it, en, fr, de, es). Le copie senza testo corretto proprio
  (`ereditata: true`) prendono la correzione dalla riga con lo stesso testo e lo stesso giapponese (come fa `dialoghi.py`).

| Lingua | Famiglia | Regalo | Abito |
|---|---|---|---|
| it | "La mia famiglia produce sake." | "dello shochu" | "In abito da cameriera!" / "vestita da cameriera!" |
| en | "a sake brewery" | "some shochu" | "Wearing a maid outfit!" / "in a maid outfit!" |
| fr | "une distillerie de saké" | "du shochu" | "En tenue de servante !" / "en tenue de servante !" |
| de | "eine Sake-Brauerei" | "etwas Shochu" | "Im Dienstmädchen-Outfit!" |
| es | "destilería de sake" | "un poco de shochu" | "¡Y va vestida de criada!" / "vestida de criada" |

Nuove lingue (o patcher separati): usare la stessa idea (distilleria di sake, shochu, abito da cameriera) con la propria forma.

### Nomi dei menu verificati in gioco
- Italiano: menu principale `Modalità Storia` (i dialoghi 1625/7603 la citano cosi').
- Francese: `Mode aventure`.

### Limite noto: nome del parlante
Il nome nella casella del dialogo (es. "Doyen Sheppard") sta nell'eseguibile (EBOOT cifrato): non modificabile. Vale per tutte le lingue.

## Frasi dei duelli (rilettura completa, 2026-10-11)
Lette tutte le frasi uniche (it 1.792, fr 1.832) contro l'inglese. Dati: `dati/duel_line_corrections_<l>.json`. Elenco per la rilettura: `tools/audit/extract_duel_lines.py`.
- it: punto finale mancante nelle frasi gemelle ("Attivo una Magia Continua", "...Magia Terreno", "...Evocazione Rituale", "Sto attivando una Trappola Continua", "È il mio turno"); "duellare non è solo una questione"; "ti rispetterò"; "una l'effetto"; "io SO"; "perché hai perso?"; "Fa' pure!"; "pescare una carta".
- fr: "Tu es mignon." / "Tu n'es pas très mignon." (era "malin"/"gentil" per *cute*); "Hein ?" al posto di "Huh ?"; "Mon Dieu"; "J'offre"; "Juste une blessure légère"; "Position d'Attaque" con maiuscole; "!" mancante in "J'invoque l'Assaillant des Protecteurs du Tombeau".
- Lasciati com'erano (voluti): frasi in "pidgin" di certi personaggi, versi, nomi di mosse inglesi ("Train Twister"). In francese "Carte Piège Continu" e' il termine coerente di tutto il gioco: non si cambia.
- Nuove lingue: stessa rilettura; correggere l'equivalente di queste classi di errore.

Elenco completo neutre/specifiche: `docs/TEXTURE_INVENTORY.md`.

## Texture "solo italiane" (classificazione, 2026-10-11)
Delle 19 texture in `ui_it` senza controparte in `ui_fr`: **13 sono neutre** (stesso hash in tutte le lingue: pannelli ricette, linguette Side/Deck/Fusion Deck, barre, `card_side`, bandiere...: il modulo di ogni lingua le riceve gia')
e **6 hanno wording locale nell'originale** (`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `d_window00016`, `duelrecord parts`): l'italiano ha `NUOVO`/`N`/`Fusione`, il francese originale ha `NEW`/`Fusion` e ha gia' i suoi HD in `upscale_extra`.
Scelta: il francese **resta come l'originale** (`NEW`). Variante opzionale da proporre all'utente per fr/de/es: `N` come icona iniziale (Nouveau/Neu/Nuevo).

## Italiano
- **Linguetta dell'editor deck: `Fusion`** (non `Fusione`): "Fusion Deck" e' il nome in tutte le lingue (come Side Deck, Deck). Texture `ui_it/schede_deck/all_i__d_window00016.png`, generata da `schede_deck.py`.
- **Sheppard e' sempre "Preside"** (mai "Cancelliere"): dialoghi (`dialogue_touchups_it.json`: `Cancelliere`/`cancelliere` -> `Preside`/`preside`, compreso
  "Ufficio del Preside" e la battuta di Crowler "Preside Crowler... Preside Crowler provvisorio") e interfaccia ("Profilo del Preside Sheppard").
- **I Token si chiamano "Segna-Mostro"** (non "Gettoni"): aiuti dell'editor e del duello, record dei duelli ("Segna-Mostro Evocati"). Nei testi delle carte non compare ne' "Gettone" ne' "Segna".
- Banner: "direttore dello Slifer Rosso" (non "presidente").
- Dormitori ovunque: **Slifer Rosso, Ra Giallo, Obelisk Blu**.
- **Carte**: rilette una per una (2479 testi). Errori oggettivi (Life Point->Points, E'->È, Annello->Anello, concordanze, spazi, maiuscole) in `tools/corrections/rules_it.py`; `generate_language.py it CARDINFO` li fonde in `dati/card_corrections.json` (181 carte). Non cambiati: nomi ufficiali, terminologia del gioco.
- Regole in `dialogue_touchups_it.json` (circa 150 `parti`) e `string_rules_it.py`.

## Francese
- **Doyen / Chancelier** dialogo per dialogo: formale -> "Chancelier", informale -> "Doyen"; nelle schede UI "Chancelier Sheppard".
- Punteggiatura francese `! ? : ;` con spazio (anche dopo `》`): regola `FR_PUNT` in `build_dialogues.py`.
- "Mode histoire" nei dialoghi -> "Mode aventure" (nome vero del menu).

## Tedesco
Vedi sezione "Tedesco: scelte della rilettura" piu' sotto.

## Inglese (europeo, 2026-10-13)
- Solo errori oggettivi (refusi, articoli e concordanze, apostrofi, `Sryus`->`Syrus`, `Principle's`->`Chancellor`, `Bandanna`->`Bandana`): carte 82, dialoghi 402 righe (79 parti, 5 regex, 2 esatte), frasi dei duelli 3 esatte + 6 parti, stringhe UI ~70 (`string_rules_en.py`). Nessuna riscrittura di stile.
- `ocg_packname_e.bin` non esiste nel gioco inglese: tolta la tabella OG.
- Texture: il pack USA (MikeyMK) copre gia' 621 delle 917 texture inglesi (stesso hash). Per le 39 che il pack USA non copre (hash europeo diverso) e che avevano solo xBRZ: ridisegnate in HD con gli script `ui_it` (`TF1_LANG=en`) in `moduli/en/ui_en` (schede_deck 14, schede_ricette 11, tutorial 6, fogli_icone 3, schermata_vs 3, menu_liste 2). Stesse parole dell'originale. Ridisegnate anche le 4 tessere DRAW (`lettere_esito`, richiesta dell'utente 2026-10-13); nome logo `VERSION MYSTIC TOMATO` e `DOWNLOADED CARD LIST` confermati dall'utente. 17 texture ITA-SU-ING controllate: neutre. Elenco in `docs/changes_en/texture_inventory_en.txt`, testi in `texture_texts_en.md`.
- Immagini carte: 82 carte corrette rigenerate in `moduli/en/cards` (small_en/large_en).

## Spagnolo (2026-10-11/12)
Dati: `rules_es.py` (carte, 341 corrette), `dialogue_touchups_es.json` (119 `parti`, 2 `esatte`), `duel_line_corrections_es.json`, `string_rules_es.py`. Elenchi completi in `docs/CHANGES_ES.md`. Domande ancora aperte: `docs/changes_es/open_questions_es.md`.
- **Dormitori e gruppi** come nei dialoghi/carte: **Slifer Rojo, Ra Amarillo, Obelisco Azul** (erano `Slifer Red`, `Ra Yellow`, `Obelisk Blue` in dialoghi e schede), **Jinetes de la Sombra** (`Shadow Riders`), **Duelista de la Sombra**, `Archidemonio`, `Trío Ojama`, `Sirviente de la Calavera`, `Toon` (le carte non usano "Cómico/Animado").
- **Rector Sheppard**: `Oficina del Rector` (mappa), `Perfil del Rector Sheppard` (era "Perfil de Sheppard del Principio"). Nei dialoghi i nomi residui italiani sono stati tradotti (`Velo della Notte`->`Velo de la Noche`, `Dante Fiammeggiante`->`Dante Ardiente`, `Padrone Seydina`->`Maestro Seydina`).
- **Luoghi**: `Alójese 101..204` -> `Habitación 101..204` (inglese: Room), `Cliff` -> `Acantilado`, `Dorm abandonado` -> `Dormitorio abandonado`.
- **Scene comuni**: sake/shochu e abito da cameriera (`st01_t01/Scr003E`) e `st02_t01/Scr101E` come nelle altre lingue; le righe a 4-5 righe dei dialoghi sono state riportate a 3 (`Scr005E#420`, `Scr007E#23`, `Scr063E#6`, `Scr003E#147/#151`).
- **Opzioni**: "EN/FUERADE" -> `ON`/`OFF` (come l'inglese); `Rindes` -> `Rendirse`; `Trar`/`Tirar bocadillo` -> `Comer` (l'inglese dice Eat).
- **Termini dell'editor**: `Refinar Búsqueda` -> `Filtrar` (come il menu); `Efecto de Disparado de Múltiple` -> `Efecto de Disparo Múltiple`; `Contador Mágico` -> `Contadores Mágicos`; `Invocación por Fusión/Ritual/Volteo` -> `Invocación de ...` (come le carte). Lasciati: `Invocación por Sacrificio`, `Tributar`, `Efecto de Blanco`, `Tronco`.
- **Testi mancanti/rotti tradotti dall'inglese**: paragrafo finale degli aiuti dei Duelos Tag (era troncato in `deck/all_s` e in inglese in `basic_bs`); "10 lanzamientos de moneda" (era 100); "usando efectos" (record 130); "Nivel 4 o inferior" (record 179); "Semi-Limitada" (messaggio 135).
- **Lezioni del tutorial** (`tutorial_s.ehp`, 4 file): "le turno" -> "es el turno de", tasti × e ○ scambiati nel passo "End Phase", codici colore chiusi, "Antes, Syrus ha preguntado" (era Bastion), "Hechizo de Campo" -> "Carta Mágica de Campo".
- **Frasi dei duelli**: `¿Cómo ha podido ocurrir esto…?`, `¿Qué…?`, "No tienes ni idea de lo que estás haciendo", "¡Yo no bajaré la guardia!" (mancava il no).
- **Texture**: testi dell'originale riprodotti (nessun cambio di parole): `TURNO DEL SIGUIENTE JUGADOR`, `COMENZAR DUELO`, `Ataque Directo`, `HAS GANADO/HAS PERDIDO/EMPATE`, `1ra/2da/3ra vuelta`, `AM/PM` (al posto di Mattina/Pomeriggio) e `de` nel calendario. `TURNO` ha lo stesso hash dell'italiano.
- **Decisioni dell'utente (2026-10-12)**: `Kaiba Corporation` resta (l'inglese dice Umiuma); "duelo" uniformato a **Duelo/Duelos** nei dialoghi (come il resto del gioco); **Rector** (non Canciller) perche' e' il piu' vicino a "Preside"; **Sacrificio** (non Tributo): `Invocación por Sacrificio`, come nei testi ufficiali spagnoli; `Efecto de Blanco` (= targeting effect) lasciato; `NEW` resta in inglese come nell'originale.
- **Nomi di carte = nome ufficiale spagnolo di Yugipedia (2026-10-12, scelta dell'utente: anche dove il gioco traduceva diversamente)**: 294 nomi in `tools/data/official_names_es.json` (prima/dopo in `docs/changes_es/official_names_es.tsv`), citazioni dei nomi tra virgolette seguono il cambio (carte, stringhe UI, frasi dei duelli). Eccezioni dove Yugipedia ha refusi o manca il dato: `Dian Keto, el Señor`, `recaudación`, `Resurrección`, `Anfibio/Anfibia`, accenti giusti del gioco (Búho, Cañón, Más Allá, Trío), 4130 `Herramienta Antigua`, 4644 `Reina de las Hojas de Otoño` (non ufficiale: come il francese). Archetipi ufficiali in maiuscolo (HÉROE, RANA) lasciati come Yugipedia.
- **`Efecto de Blanco` -> `Efectos con Objetivo`**: i testi ufficiali dicono `selecciona 1 monstruo ... ese objetivo`; Yugipedia traduce Target con `Objetivo`. `blanco` -> `objetivo` in tutte le spiegazioni dell'interfaccia e sulle carte 5179/5187. Non ho trovato un'etichetta ufficiale per la categoria: la scelta e' mia.

## Texture comuni: foglio numeri del duello (`card_icon03`)
Scelta dell'utente: cifre 0-9, LP, tasti e segni piccoli **dal pack USA** (pixel art netta); moltiplicatori ×1…×12 e icone sotto **come nel foglio italiano**; solo la parola del tempo cambia (TEMPO, TEMPS, TIME, ZEIT, TIEMPO). Ricetta e script: `tools/ui_textures/icon03_languages.py` (vedi `STATO_LAVORI.md`). Chi fa il patcher di una nuova lingua deve usare lo stesso foglio e cambiare solo la parola.

## Tedesco: scelte della rilettura (2026-10-12)
Dati: `confronti/audit_de/ritocchi_nuovi.py` (dialoghi), `ritocchi_stringhe.py` (UI), `tools/data/duel_line_corrections_de.json`; elenco in `docs/changes_de/` e domande in `open_questions_de.md`.
- Luoghi senza articolo come negli altri nomi di mappa: "Büro des Kanzlers" (dialogo "Verlasse das 《M006_2》"), "Duellakademie" (fem.: "Duellant der Duellakademie"); mancavano Bibliothek, Dach, Ruinen (mapname 20, 21, 25), "Cliff" -> Klippe, "Verließ Dorm" -> Verlassener Schlafsaal.
- "Spielzug" sempre maiuscolo e maschile ("in diesem Spielzug", "am Zug"); tutorial: tasti ×/○ scambiati corretti, "Fallenkarten können verwendet werden, wenn" (negazione sbagliata), "Einsturz" -> Schrumpfen, "Gegnerrunde" -> "Zug des Gegners", trattini di sillabazione rimasti a metà riga rimossi.
- Menu: "Duel/Talk" nel dialogo -> "Duell/Reden" (come il menu di campo); Barett -> Haarspange.
- Texture: "Tauschen" al posto del residuo francese "ÉCHANGE"; "Fusionsdeck" (recipe010004); linguette Truhe/Miete/Labor/Konverter/Fusion in HD.
- Texture duello (2026-10-13): testi dell'originale riprodotti, nessun cambio di parole: `DU GEWINNST`, `DU VERLIERST`, `UNENTSCHIEDEN`, `Ketten`, `Direkter Angriff!`, `NÄCHSTER SPIELER` (la A resta senza puntini nella texture del banner: sono una sprite a parte), `DUELL BEGINNEN`, `SPIELZUG`.
