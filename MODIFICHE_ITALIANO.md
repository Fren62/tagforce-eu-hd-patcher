# MODIFICHE PER LA VERSIONE POMODORO MISTICO IN ITALIANO

Documento **completo** di tutto cio' che la "Versione Pomodoro Mistico" cambia per l'italiano: (A) le modifiche **dirette alla ISO**, (B) il **texture pack** (com'e' fatto, cosa contiene, come si compone), (C) le scelte editoriali, (D) cosa e' verificato in gioco e cosa no, (E) come rigenerare tutto.

**Questo file e' generato** da `strumenti/analisi/scrivi_documento_modifiche.py it` a partire dai dati reali: confronto byte per byte tra la ISO originale `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` e la ISO corretta `..._definitiva.iso` (`documenta_modifiche.py`) e scansione del pack (`documenta_pack.py`). Gli elenchi riga per riga stanno in `documentazione/modifiche_it/*.csv` (separatore `;`, UTF-8 con BOM, a capo come `⏎`): sono la **lista esatta** di ogni cambiamento. Rigenera tutto dopo ogni modifica.

Per il metodo generale e per le altre lingue: `GUIDA_NUOVA_LINGUA.md`; dettagli tecnici degli script: `TUTORIAL.md`; decisioni: `REGISTRO_SCELTE.md`; texture neutre/specifiche: `INVENTARIO_TEXTURE.md`.

## Indice
- A. Modifiche alla ISO: A1 panoramica · A2 carte · A3 dialoghi · A4 frasi dei duelli · A5 stringhe dell'interfaccia · A6 etichetta Magia/Trappola · A7 file toccati e dettagli tecnici · A8 cosa non si puo' cambiare
- B. Texture pack: B1 provenienza e struttura · B2 immagini delle carte · B3 interfaccia HD (`ui_it`) · B4 foglio numeri (`card_icon03`) · B5 targa del titolo · B6 textures.ini e composizione · B7 installazione
- C. Scelte editoriali · D. Verifica in gioco · E. Come rigenerare · F. Limiti e punti aperti

---

# A. MODIFICHE ALLA ISO

## A1. Panoramica

La ISO originale **non viene mai modificata**. `strumenti/correzioni/applica_iso.py ISO_ORIG ISO_OUT [lingue]` ne crea una copia in cui alcuni archivi `.ehp` sono riscritti. Se un archivio cresce (testo piu' lungo) viene **rimesso in fondo alla ISO** in un nuovo settore e il suo voce nella directory ISO9660 viene riassegnata (`pycdlib`); la ISO `_definitiva` pesa per questo ~909 MB (l'originale ~761 MB). **Lanciarlo sempre senza elenco di lingue (o con tutte)**: con una lingua sola sovrascrive le altre.

| Cosa | Quantita' (derivata dal confronto ISO) | Dove sta il dato | File CSV |
|---|---|---|---|
| Carte con testo cambiato (nome e/o descrizione) | 181 carte (182 campi) | `strumenti/dati/correzioni_carte.json` da `correzioni/regole_it.py` | carte.csv |
| Righe di dialogo della storia | 2488 righe | `strumenti/dati/ritocchi_dialoghi_it.json` (+ base) | dialoghi.csv |
| Frasi dei duellanti nei duelli | 33 frasi uniche (70 voci in tutti gli archivi) | `strumenti/dati/correzioni_frasi_duello_it.json` | frasi_duello.csv |
| Stringhe dell'interfaccia (aiuti, schede, record, tutorial, menu...) | 298 stringhe uniche (571 voci, 46 archivi) | `correzioni/regole_stringhe_it.py` + `dati/testi_ui.json` | stringhe_ui.csv |
| Immagini sostituite dentro la ISO | 6 (etichetta [CARTA MAGIA/TRAPPOLA] della carta grande) | `applica_iso.py` (copia `card_spell_trap.gim` della lingua) | immagini_iso.csv |
| File della ISO toccati (archivi `.ehp`) | 142 | - | file_toccati.csv |
| Altre differenze tecniche (offset ricalcolati) | 90 | - | altro.csv |

## A2. Testi delle carte

Archivio: `PSP_GAME/USRDIR/duelsys/cardinfo_ita.ehp` (tabelle `CARD_Name_*`, `CARD_Desc_*`, `CARD_Indx_*`). **181 carte** hanno nome e/o descrizione modificati. Si correggono **solo errori oggettivi** (refusi, accenti, apostrofi, spazi, maiuscole incoerenti, concordanze, plurali fissi, residui di altre lingue); nomi ufficiali e terminologia del gioco non si toccano.

Come: ogni carta e' stata letta (it: 2.479 testi, uno per uno; fr: audit contro database ufficiale + lettura). Regole in `strumenti/correzioni/regole_it.py`: **44 regole globali** (regex applicate a nomi e descrizioni di tutte le carte) e **7 correzioni per carta** (`PER_CARTA`: id, campo, vecchio, nuovo, motivo; il vecchio testo deve esistere esattamente). `genera_lingua.py it CARDINFO` (fonde il risultato nel `correzioni_carte.json` esistente, idempotente) produce il json; `applica_iso` lo scrive nella ISO; le immagini HD delle carte toccate si rigenerano (sezione B2).

### Regole globali (tutte)
| modello (regex) | sostituzione | motivo |
|---|---|---|
| \bLife Point\b | Life Points | plurale di Life Points (altrove sempre Life Points) |
| \bAnnello\b | Anello | refuso |
| \bavvesario\b | avversario | refuso |
| \bin seguita\b | in seguito | refuso |
| \bdopo di chè\b | dopo di che | accento errato |
| \bquesto carta\b | questa carta | concordanza |
| \bUn immagine\b | Un'immagine | apostrofo mancante |
| \bE' composto\b | È composto | accento |
| \bpuo\b | può | accento mancante |
| \bne dichiarare\b | né dichiarare | accento mancante |
| \bMain phase\b | Main Phase | maiuscola incoerente |
| \bdella Damage Step\b | del Damage Step | genere: il Damage Step |
| \b[Tt]ipo-(Demone\|Fata\|Guerriero)\b | Tipo \1 | trattino di troppo |
| \btipo Pyro\b | Tipo Pyro | maiuscola incoerente |
| \bSegna Opzione\b | Segna-Opzione | nome del Segna-Mostro |
| \bTramite Evocazione\b | tramite Evocazione | maiuscola errata |
| \bevocata tramite\b | Evocata tramite | maiuscola incoerente (Evocata) |
| \bX (\d+) punti\b | x \1 punti | moltiplicatore (altrove x) |
| \bX (\d+)\b | x \1 | moltiplicatore (altrove x) |
| \bMagia,Trappola\b | Magia, Trappola | spazio mancante |
| Cimitero,eccetto | Cimitero, eccetto | spazio mancante |
| \bsolo I Mostri\b | solo i Mostri | maiuscola errata |
| \baumenta I tuoi\b | aumenta i tuoi | maiuscola errata |
| \bRimuovi da gioco\b | Rimuovi dal gioco | articolo mancante |
| \bCarte Magie e Trappola\b | Carte Magia e Trappola | Magia e' invariabile |
| Trappola , | Trappola, | spazio prima della virgola |
| Magia : | Magia: | spazio prima dei due punti |
| Trappola : | Trappola: | spazio prima dei due punti |
| Effetto Mostro : | Effetto Mostro: | spazio prima dei due punti |
| \bsi aggiudica il Partita\b | si aggiudica la Partita | genere |
| \bvengono cambiata in\b | vengono cambiati in | concordanza |
| \bquante possibile\b | quante possibili | concordanza |
| \bsi sono 3\b | ci sono 3 | refuso |
| \bdi questa carte\b | di questa carta | refuso |
| \bpuoi scegli\b | puoi scegliere | forma verbale |
| \bcome tributo\b | come Tributo | maiuscola incoerente (Tributo) |
| \binferiore del DEF\b | inferiore al DEF | preposizione |
| \bHa un indole\b | Ha un'indole | apostrofo mancante |
| \bsul tuo terreno\b | sul tuo Terreno | maiuscola incoerente (Terreno) |
| (?<![A-Za-zÀ-ÿ])E' (?=[a-zà-ÿ]) | È  | accento: E' -> È |
| L' (?=[\"A-ZÀ-Þ]) | L' | spazio dopo l'apostrofo |
| " ," | ", " | spazio dopo la virgola |
| \(Mostro,Magia | (Mostro, Magia | spazio dopo la virgola |
| battaglia\.Distruggi | battaglia. Distruggi | spazio dopo il punto |

### Correzioni per carta (tutte)
| id | campo | vecchio | nuovo | motivo |
|---|---|---|---|---|
| 6057 | desc | tutti le Carte | tutte le Carte | concordanza |
| 6173 | desc | E' composto | È composto | accento |
| 6248 | desc | da in Posizione d'Attacco a scoperta in Posizione di Difesa | da Posizione d'Attacco a scoperta in Posizione di Difesa | preposizione di troppo |
| 6659 | desc | viene distrutto in seguito ad una battaglia e mandata al Cimitero | viene distrutto in seguito ad una battaglia e mandato al Cimitero | concordanza |
| 6706 | desc | effetto di "Victory Viper XX3" | effetto di "Victory Viper XX03" | nome della carta |
| 6657 | desc | Magia & Trappola , questa | Magia & Trappola, questa | spazio prima della virgola |
| 6563 | desc | Carte Magie e Trappola non possono | Le Carte Magia e Trappola non possono | articolo e plurale |

### Elenco completo delle carte cambiate
**Confronto completo originale -> nuovo con le parole cambiate evidenziate: `documentazione/modifiche_it/carte_diff.md`** (tutte le 182 voci). Dati grezzi: `documentazione/modifiche_it/carte.csv`. Prime 40 righe:

| id | nome originale | campo | originale | nuovo |
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

(... altre 142 righe nel CSV)

## A3. Dialoghi della storia

Archivi: `script/stNN_<scena>_i.ehp`, ogni scena e' una coppia di membri `...Ii.bin` (offset in caratteri UTF-16) e `...Li.bin` (stringhe UTF-16LE chiuse da NUL, alcune compresse in gzip). **2488 righe** cambiate (comprese quelle che **ereditano** la correzione perche' hanno lo stesso testo originale e lo stesso giapponese di una riga corretta).

Flusso: lettura riga per riga confrontata con inglese e giapponese -> ritocchi in `strumenti/dati/ritocchi_dialoghi_it.json` (`esatte` e `parti`) -> `costruisci_dialoghi.py it` -> `correzioni_dialoghi_it.json` -> `applica_iso.py`. Regole automatiche di impaginazione in `costruisci_dialoghi.py`: spazio dopo i segnaposto `《...》`, tre puntini seguiti da maiuscola (`...Ciao` -> `... Ciao`), base `correzioni_dialoghi_it_base.json` (~1.380 proposte della prima revisione). Vincoli del box: ~46 caratteri per riga, max 3 righe (un segnaposto vale ~6 caratteri): `applica_iso` segnala le righe che potrebbero non starci.

### Ritocchi di rilettura: `esatte` (6) — frase intera originale -> frase nuova
| originale | nuovo |
|---|---|
| Not you too, 《C003_3》. | Anche tu no, 《C003_3》. |
| Huh? E tu chi sei?⏎Oh sei il nuovo arrivato.. | Eh? E tu chi sei?⏎Oh, sei il nuovo arrivato... |
| L'Imperatore 《C007_4》abbia⏎un fratello minore e che si | Si dice che l'Imperatore 《C007_4》⏎abbia un fratello minore e che si |
| E tu che vuoi?⏎Vuoi farti un Duello, Huh?. | E tu che vuoi?⏎Vuoi farti un Duello, eh? |
| Ecco, usa questo! | Ecco, usa questo vestito da cameriera! |
| Oddio, sto sbavando un po'... | Beh, non sono poi così bravo... |

### Ritocchi di rilettura: `parti` (74) — sostituzioni di testo applicate a ogni riga (in ordine)
| vecchio | nuovo |
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

### Elenco completo delle righe
**Confronto completo originale -> nuovo (con inglese e giapponese): `documentazione/modifiche_it/dialoghi_diff.md`** (tutte le 2488 righe). Dati grezzi: `documentazione/modifiche_it/dialoghi.csv`. Prime 30:

| id | originale | nuovo | inglese |
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

(... altre 2458 righe nel CSV)

## A4. Frasi dei duellanti nei duelli

Tabelle `chr_wordstbl_i.bin` e `02chr_wordstbl_...` dentro ~72 archivi `duel/cutin_*.ehp` (e `zakov*`). Le frasi uniche sono ~1.800: tutte rilette. **33 frasi cambiate** (70 voci). Dati: `esatte` (7) e `parti` (27) in `correzioni_frasi_duello_it.json`. I file `*-ptrs.txt` degli archivi dei personaggi contengono offset assoluti: se una tabella cresce vanno ricalcolati (`rimappa_puntatori`), altrimenti il duello va in crash.

Confronto con parole evidenziate: `documentazione/modifiche_it/frasi_duello_diff.md`.

| originale | nuovo | voci | esempi di archivio |
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

## A5. Stringhe lunghe e corte dell'interfaccia

Tabelle `strTbl*`, `help_strtbl_*`, `ddstrtbl_*`, `field_strtbl*` (formato `(n, 12, 12+4n)` + offset + UTF-16) in 46 archivi (la stessa tabella e' copiata in piu' archivi, es. `field/always_*_ita.ehp` x6). **298 stringhe uniche cambiate**. Regole: `strumenti/correzioni/regole_stringhe_it.py` — **159 voci `STRINGHE`** (archivio, membro, indice 0-based, [(vecchio, nuovo)], motivo), **55 `GLOBALI`** (regex/callable, applicate dopo le STRINGHE) su **15 tabelle** (`TABELLE`); piu' 1 correzioni puntuali in `strumenti/dati/testi_ui.json` (scrittura sul posto, testo piu' corto o uguale).

### Per membro (stringhe uniche cambiate)
| membro | stringhe |
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

### Regole globali (tutte)
| modello | sostituzione | motivo |
|---|---|---|
| (?<=[A-Za-zà-ù.,;!?])  +(?=[A-Za-zÀ-ù]) |   | spazi doppi |
| ’ | ' | apostrofo tipografico -> semplice |
| \bE'(?=[A-Za-zà-ù]) | È  | E' al posto di È |
| \bE'  | È  | E' al posto di È |
| (?m)(?:^\|(?<=[.!?] ))E (?=(?:riuscita\|stato\|sempre\|molto)\b) | È  | E senza accento |
| chè\b | ché | perché, finché, nonché... |
| \bpò\b | po' | un po' |
| \bfà\b | fa | accento |
| \bsà\b | sa | accento |
| \bstà\b | sta | accento |
| \bnè\b | né | accento |
| \bsè\b | sé | accento |
| \bcosi\b | così | accento |
| \bpiu\b | più | accento |
| \bverrano\b | verranno | refuso |
| \bdallla\b | dalla | refuso |
| \bpiù più\b | più | ripetizione |
| \bsanwich\b | sandwich | refuso |
| \bSndwich\b | Sandwich | refuso |
| \bsoya\b | soia | refuso |
| sudentesca | studentesca | refuso |
| choccolato | cioccolato | refuso |
| scimpanzè | scimpanzé | accento |
| \b(?!(?:po\|va\|sta\|fa\|di\|da\|stai\|dai)\b)([A-Za-zÀ-ÿ]+)' (?=[A-Za-zÀ-ÿ]) | \1' | spazio dopo l'apostrofo |
| (?<=[A-Za-zà-ù]) '(?=[A-Za-z]) | ' | spazio prima dell'apostrofo |
| (?<=[a-zà-ù,;] )I (?=[a-zà-ù]) | i  | articolo con la I maiuscola |
| \b([Ii]\|[Dd]ei\|[Nn]ei\|[Aa]i\|[Ss]ui\|[Dd]ai\|[Pp]er i\|[Tt]ra i) Duello\b | \1 Duelli | plurale |
| \bDuello Singoli\b | Duelli Singoli | plurale |
| \b(\d) Duello\b | \1 Duelli | plurale |
| affrontare Duello in cui | affrontare Duelli in cui | plurale |
| \bMostri Fusione\b | Mostri da Fusione | nome del tipo |
| \bMostri Rituale\b | Mostri Rituali | plurale |
| \bGli Mostri\b | I Mostri | articolo |
| (?m)^Magia (Normali\|Continuate\|Equipaggiamento\|Rituale\|Rituali\|Terreno\|da Terreno\|Rapida\|Rapide)(?=\r?$) | (funzione) _magia | elenco dei tipi di Magia |
| (?m)^Trappola (Normali\|Continue)(?=\r?$) | Trappole \1 | elenco dei tipi di Trappola |
| \bsulle carta\b | sulle carte | plurale |
| ●Segna-Monstro | ●Segna-Mostro | nome |
| I Segna dei Mostri | I Segna-Mostro | nome |
| i Segna non | i Segna-Mostro non | nome |
| Un Gettone equivale | Un Segna-Mostro equivale | nome |
| Gettoni Evocati | Segna-Mostro Evocati | nome |
| ●Guarda delle Carte | ●Guardare le Carte | titolo |
| ●Activar | ●Attivazione | refuso |
| \bin terreno\b | in Terreno | maiuscola |
| \bterreno di Duello\b | Terreno di Duello | maiuscola |
| Carta da terreno | Carta da Terreno | maiuscola |
| \bsuo Effetti Scoperta\b | suo Effetto Scoperta | singolare |
| \bl'Effetti Scoperta\b | l'Effetto Scoperta | singolare |
| \bQuesta opzione di permette\b | Questa opzione ti permette | refuso |
| \bcon ad un\b | con un | refuso |
| \b(di\|a\|da\|in) Slifer Red\b | (funzione) f | dormitorio |
| \bSlifer Red\b | Slifer Rosso | nome del dormitorio |
| \b(di\|a\|da\|in) Obelisk Blue\b | (funzione) f | dormitorio |
| \bObelisk Blue\b | Obelisk Blu | nome del dormitorio |
| \bRa Yellow\b | Ra Giallo | nome del dormitorio |

### Voci STRINGHE (tutte): dove e perche'
| archivio | membro | indice | cambiamenti | motivo |
|---|---|---|---|---|
| database/charalist.ehp | strTbl_i.bin | 12 | 1 sostituzione/i | terza persona |
| database/charalist.ehp | strTbl_i.bin | 13 | 4 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_i.bin | 14 | 3 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_i.bin | 15 | 1 sostituzione/i | refuso |
| database/charalist.ehp | strTbl_i.bin | 17 | 3 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_i.bin | 18 | 3 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_i.bin | 20 | 6 sostituzione/i | refusi e virgolette |
| database/charalist.ehp | strTbl_i.bin | 21 | 1 sostituzione/i | come nei dialoghi: direttore del dormitorio |
| database/charalist.ehp | strTbl_i.bin | 22 | 2 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_i.bin | 23 | 3 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_i.bin | 24 | 2 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_i.bin | 28 | 2 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_i.bin | 29 | 1 sostituzione/i | spazio |
| database/charalist.ehp | strTbl_i.bin | 31 | 1 sostituzione/i | frase confusa |
| database/charalist.ehp | strTbl_i.bin | 34 | 1 sostituzione/i | grammatica |
| database/charalist.ehp | strTbl_i.bin | 37 | 3 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_i.bin | 43 | 2 sostituzione/i | refusi |
| database/charalist.ehp | strTbl_i.bin | 48 | 1 sostituzione/i | accordo |
| database/charalist.ehp | strTbl_i.bin | 49 | 1 sostituzione/i | accento |
| database/charalist.ehp | strTbl_i.bin | 52 | 1 sostituzione/i | Preside con la maiuscola |
| database/duelrecord.ehp | strTbl_i.bin | 26 | 1 sostituzione/i | nome |
| database/duelrecord.ehp | strTbl_i.bin | 35 | 1 sostituzione/i | refuso |
| database/duelrecord.ehp | strTbl_i.bin | 63 | 1 sostituzione/i | refuso |
| database/duelrecord.ehp | strTbl_i.bin | 137 | 1 sostituzione/i | frase confusa |
| database/duelrecord.ehp | strTbl_i.bin | 155 | 1 sostituzione/i | articolo |
| database/duelrecord.ehp | strTbl_i.bin | 159 | 1 sostituzione/i | stile come le altre voci |
| database/duelrecord.ehp | strTbl_i.bin | 160 | 1 sostituzione/i | stile |
| database/duelrecord.ehp | strTbl_i.bin | 161 | 1 sostituzione/i | stile |
| database/duelrecord.ehp | strTbl_i.bin | 162 | 1 sostituzione/i | stile |
| database/duelrecord.ehp | strTbl_i.bin | 163 | 1 sostituzione/i | frase |
| database/duelrecord.ehp | strTbl_i.bin | 164 | 1 sostituzione/i | frase |
| database/duelrecord.ehp | strTbl_i.bin | 182 | 1 sostituzione/i | plurale |
| database/duelrecord.ehp | strTbl_i.bin | 184 | 1 sostituzione/i | frase sbagliata (copia di 182) |
| database/duelrecord.ehp | strTbl_i.bin | 212 | 1 sostituzione/i | refuso |
| database/duelrecord.ehp | strTbl_i.bin | 213 | 1 sostituzione/i | refuso |
| database/duelrecord.ehp | strTbl_i.bin | 248 | 1 sostituzione/i | spazio iniziale |
| duel/result/result_i.ehp | strTbl.bin | 26 | 1 sostituzione/i | nome |
| duel/result/result_i.ehp | strTbl.bin | 35 | 1 sostituzione/i | refuso |
| duel/result/result_i.ehp | strTbl.bin | 63 | 1 sostituzione/i | refuso |
| duel/result/result_i.ehp | strTbl.bin | 137 | 1 sostituzione/i | frase confusa |
| duel/result/result_i.ehp | strTbl.bin | 155 | 1 sostituzione/i | articolo |
| duel/result/result_i.ehp | strTbl.bin | 159 | 1 sostituzione/i | stile come le altre voci |
| duel/result/result_i.ehp | strTbl.bin | 160 | 1 sostituzione/i | stile |
| duel/result/result_i.ehp | strTbl.bin | 161 | 1 sostituzione/i | stile |
| duel/result/result_i.ehp | strTbl.bin | 162 | 1 sostituzione/i | stile |
| duel/result/result_i.ehp | strTbl.bin | 163 | 1 sostituzione/i | frase |
| duel/result/result_i.ehp | strTbl.bin | 164 | 1 sostituzione/i | frase |
| duel/result/result_i.ehp | strTbl.bin | 182 | 1 sostituzione/i | plurale |
| duel/result/result_i.ehp | strTbl.bin | 184 | 1 sostituzione/i | frase sbagliata (copia di 182) |
| duel/result/result_i.ehp | strTbl.bin | 212 | 1 sostituzione/i | refuso |
| duel/result/result_i.ehp | strTbl.bin | 213 | 1 sostituzione/i | refuso |
| duel/result/result_i.ehp | strTbl.bin | 248 | 1 sostituzione/i | spazio iniziale |
| deck/all_i.ehp | strTbl.bin | 51 | 1 sostituzione/i | spazio |
| deck/all_i.ehp | strTbl.bin | 83 | 1 sostituzione/i | refusi |
| deck/all_i.ehp | strTbl.bin | 100 | 1 sostituzione/i | spazio |
| deck/all_i.ehp | strTbl.bin | 101 | 1 sostituzione/i | spazio |
| deck/all_i.ehp | strTbl.bin | 106 | 1 sostituzione/i | spazio |
| deck/all_i.ehp | strTbl.bin | 109 | 1 sostituzione/i | frase |
| deck/all_i.ehp | strTbl.bin | 110 | 1 sostituzione/i | frase |
| deck/all_i.ehp | strTbl.bin | 111 | 1 sostituzione/i | frase |
| deck/all_i.ehp | strTbl.bin | 116 | 1 sostituzione/i | articolo |
| deck/all_i.ehp | strTbl.bin | 126 | 1 sostituzione/i | '$' al posto dell'a capo |
| deck/all_i.ehp | strTbl.bin | 138 | 1 sostituzione/i | frase |
| deck/all_i.ehp | strTbl.bin | 142 | 1 sostituzione/i | italiano |
| deck/all_i.ehp | strTbl.bin | 148 | 1 sostituzione/i | spazio |
| deck/all_i.ehp | strTbl.bin | 152 | 1 sostituzione/i | maiuscola |
| deck/all_i.ehp | strTbl.bin | 154 | 1 sostituzione/i | articolo |
| deck/all_i.ehp | strTbl.bin | 155 | 1 sostituzione/i | spazio |
| deck/all_i.ehp | help_strtbl_label.bin | 1 | 1 sostituzione/i | come l'etichetta del pulsante '?' |
| deck/all_i.ehp | help_strtbl_label.bin | 8 | 1 sostituzione/i | coerenza |
| deck/all_i.ehp | help_strtbl_contents.bin | 81 | 1 sostituzione/i | nome |
| deck/all_i.ehp | help_strtbl_contents.bin | 100 | 1 sostituzione/i | genere |
| deck/all_i.ehp | help_strtbl_contents.bin | 104 | 1 sostituzione/i | termine |
| deck/all_i.ehp | help_strtbl_contents.bin | 105 | 1 sostituzione/i | spazio |
| deck/all_i.ehp | help_strtbl_contents.bin | 106 | 1 sostituzione/i | accordo |
| deck/all_i.ehp | help_strtbl_contents.bin | 107 | 1 sostituzione/i | refuso |
| deck/all_i.ehp | help_strtbl_contents.bin | 118 | 1 sostituzione/i | refuso |
| deck/all_i.ehp | help_strtbl_contents.bin | 129 | 2 sostituzione/i | refusi |
| deck/all_i.ehp | help_strtbl_contents.bin | 157 | 2 sostituzione/i | Activar non e' italiano |
| deck/all_i.ehp | help_strtbl_contents.bin | 164 | 3 sostituzione/i | plurale e genere |
| deck/all_i.ehp | help_strtbl_contents.bin | 175 | 2 sostituzione/i | refusi |
| deck/tutorial.ehp | strTbl_i.bin | 5 | 2 sostituzione/i | genere |
| deck/tutorial.ehp | strTbl_i.bin | 25 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 26 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 27 | 1 sostituzione/i | virgola |
| deck/tutorial.ehp | strTbl_i.bin | 29 | 1 sostituzione/i | articolo |
| deck/tutorial.ehp | strTbl_i.bin | 30 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 34 | 1 sostituzione/i | frase |
| deck/tutorial.ehp | strTbl_i.bin | 36 | 1 sostituzione/i | punteggiatura |
| deck/tutorial.ehp | strTbl_i.bin | 39 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 82 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 46 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 61 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 74 | 1 sostituzione/i | come l'etichetta del pulsante '?' |
| deck/tutorial.ehp | strTbl_i.bin | 79 | 1 sostituzione/i | punteggiatura |
| deck/tutorial.ehp | strTbl_i.bin | 86 | 1 sostituzione/i | frase |
| deck/tutorial.ehp | strTbl_i.bin | 87 | 1 sostituzione/i | spazio |
| deck/tutorial.ehp | strTbl_i.bin | 98 | 1 sostituzione/i | genere |
| deck/tutorial.ehp | strTbl_i.bin | 104 | 1 sostituzione/i | spazio |
| deck/tutorial.ehp | strTbl_i.bin | 113 | 1 sostituzione/i | articolo |
| deck/tutorial.ehp | strTbl_i.bin | 118 | 1 sostituzione/i | nome |
| deck/tutorial.ehp | strTbl_i.bin | 119 | 1 sostituzione/i | punteggiatura |
| deck/tutorial.ehp | strTbl_i.bin | 126 | 1 sostituzione/i | articolo |
| deck/tutorial.ehp | strTbl_i.bin | 128 | 1 sostituzione/i | verbo |
| deck/tutorial.ehp | strTbl_i.bin | 129 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 130 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 133 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 145 | 1 sostituzione/i | termine |
| deck/tutorial.ehp | strTbl_i.bin | 146 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 150 | 1 sostituzione/i | articolo |
| deck/tutorial.ehp | strTbl_i.bin | 153 | 1 sostituzione/i | frase |
| deck/tutorial.ehp | strTbl_i.bin | 154 | 1 sostituzione/i | maiuscola |
| deck/tutorial.ehp | strTbl_i.bin | 166 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 172 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 173 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 175 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 176 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 177 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 179 | 1 sostituzione/i | frase |
| deck/tutorial.ehp | strTbl_i.bin | 189 | 1 sostituzione/i | articolo |
| deck/tutorial.ehp | strTbl_i.bin | 201 | 1 sostituzione/i | accordo |
| deck/tutorial.ehp | strTbl_i.bin | 203 | 1 sostituzione/i | refuso |
| deck/tutorial.ehp | strTbl_i.bin | 205 | 1 sostituzione/i | maiuscola |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 70 | 1 sostituzione/i | punto finale |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 72 | 1 sostituzione/i | termine |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 73 | 1 sostituzione/i | punto finale |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 75 | 1 sostituzione/i | frase |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 81 | 1 sostituzione/i | spazio |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 84 | 1 sostituzione/i | termine |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 87 | 1 sostituzione/i | frase |
| duel/basic_bi.ehp | ddstrtbl_i.bin | 88 | 1 sostituzione/i | frase |
| duel/start/start_i.ehp | strTbl_i.bin | 2 | 1 sostituzione/i | refuso |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 92 | 1 sostituzione/i | nome |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 110 | 1 sostituzione/i | refuso |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 113 | 1 sostituzione/i | genere |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 116 | 1 sostituzione/i | refuso |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 123 | 2 sostituzione/i | refusi |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 154 | 1 sostituzione/i | refuso |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 177 | 2 sostituzione/i | Activar non e' italiano |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 184 | 3 sostituzione/i | plurale e genere |
| duel/basic_bi.ehp | help_strtbl_contents_duel_i.bin | 195 | 2 sostituzione/i | refusi |
| field/always_*_ita.ehp | field_strtbl.bin | 8 | 1 sostituzione/i | come nei dialoghi |
| field/always_*_ita.ehp | field_strtbl.bin | 21 | 1 sostituzione/i | imperativo |
| field/always_*_ita.ehp | field_strtbl.bin | 22 | 1 sostituzione/i | imperativo |
| field/always_*_ita.ehp | field_strtbl.bin | 57 | 1 sostituzione/i | frase |
| field/always_*_ita.ehp | field_strtbl.bin | 58 | 1 sostituzione/i | articolo |
| field/always_*_ita.ehp | field_strtbl.bin | 59 | 1 sostituzione/i | abbreviazione |
| field/always_*_ita.ehp | field_strtbl.bin | 60 | 1 sostituzione/i | termine |
| field/always_*_ita.ehp | field_strtbl.bin | 68 | 1 sostituzione/i | spazio |
| field/always_*_ita.ehp | field_strtbl.bin | 98 | 1 sostituzione/i | refuso |
| field/always_*_ita.ehp | field_strtbl_item.bin | 95 | 1 sostituzione/i | refuso |
| field/always_*_ita.ehp | field_strtbl_item.bin | 60 | 1 sostituzione/i | spazio |
| field/always_*_ita.ehp | field_strtbl_item.bin | 157 | 1 sostituzione/i | termine |
| field/always_*_ita.ehp | field_strtbl_item.bin | 184 | 1 sostituzione/i | refuso |
| field/always_*_ita.ehp | field_strtbl_item.bin | 189 | 1 sostituzione/i | frase |
| field/always_*_ita.ehp | field_strtbl_item.bin | 191 | 1 sostituzione/i | refuso |
| field/always_*_ita.ehp | field_strtbl_item.bin | 193 | 1 sostituzione/i | refuso |
| labo/password.ehp | strTbl_i.bin | 4 | 1 sostituzione/i | refusi |
| labo/password.ehp | strTbl_i.bin | 9 | 1 sostituzione/i | articolo |

### Correzioni puntuali `testi_ui.json`
| file | membro | indice | vecchio | nuovo | motivo |
|---|---|---|---|---|---|
| /PSP_GAME/USRDIR/deck/all_i.ehp | strTbl.bin | 107 | Assistenza | Aiuto | etichetta del pulsante '?' del deck editor: "Assistenza" viene tagliata dal bordo dello schermo (si leggeva "Assisten"); in inglese e' "Help" |

### Elenco completo
**Confronto completo con parole evidenziate: `documentazione/modifiche_it/stringhe_ui_diff.md`.** Dati grezzi: `documentazione/modifiche_it/stringhe_ui.csv`. Prime 40:

| membro | indice | originale | nuovo |
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

(... altre 258 righe nel CSV)

## A6. Etichetta [CARTA MAGIA] / [CARTA TRAPPOLA] della carta grande nel duello

In tutti i `duel/basic_<regione><lingua>.ehp` l'etichetta era in inglese (hash `c2268340`): `applica_iso.py` la sostituisce con `card_spell_trap.gim` di `field/always_<lingua>_<lingua>.ehp` (hash `9622cd75`).

| archivio | membro | hash originale | hash nuovo |
|---|---|---|---|
| /PSP_GAME/USRDIR/duel/basic_bi.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |
| /PSP_GAME/USRDIR/duel/basic_fi.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |
| /PSP_GAME/USRDIR/duel/basic_gi.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |
| /PSP_GAME/USRDIR/duel/basic_ii.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |
| /PSP_GAME/USRDIR/duel/basic_si.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |
| /PSP_GAME/USRDIR/duel/basic_ui.ehp | card_spell_trap.gim | c2268340 | 9622cd75 |

## A7. File della ISO toccati e dettagli tecnici

142 archivi `.ehp` risultano diversi dall'originale (tutte le lingue insieme, perche' la ISO e' unica; elenco in `documentazione/modifiche_it/file_toccati.csv`). Gli altri file (video, audio, eseguibile `EBOOT.BIN`, `PARAM.SFO`) sono identici. Differenze tecniche non testuali: `*-ptrs.txt` (offset assoluti dei membri, ricalcolati quando una tabella cambia lunghezza), nuova posizione degli archivi in fondo alla ISO.

## A8. Cosa NON si puo' cambiare (limiti del gioco)

- Il **nome del parlante** nella casella del dialogo (es. "Preside Sheppard"/"Cancelliere" in italiano, "Doyen Sheppard" in francese, "Rector Sheppard" in spagnolo) sta nell'EBOOT cifrato: non modificabile.
- Testi disegnati dal gioco con il suo font (dialoghi, nomi, descrizioni nel deck, menu a tendina, tastiera di sistema, schermata di scelta lingua) non sono sostituibili dal texture pack: si cambiano solo nella ISO.
- Le 438 texture di mappa/sfondi non sono sostituite (il gioco ne cambia la palette): limite del pack di MikeyMK, non del nostro lavoro.

---

# B. TEXTURE PACK

## B1. Provenienza e struttura

Base: **Yu-Gi-Oh! GX Tag Force 1 HD Remastered** di **MikeyMK** (pack USA `ULUS10136`) e carte HD di **chrisfand**, adattati alla ISO europea `ULES00600`. Il progetto non ridistribuisce il pack di terzi (`PERMESSI_AUTORI.md`): il patcher se lo fa dare dall'utente. Il nostro lavoro: (1) rimappare gli **hash** del pack USA su quelli EU (`strumenti/gen_ini.py`), (2) rifare nella lingua carte e scritte dell'interfaccia, (3) correggere i testi, (4) `upscale_extra` per le texture non coperte.

PPSSPP riconosce una texture dall'**hash dei suoi pixel** (xxhash dei dati, `gim.data_hash`); ogni riga del `textures.ini` e' `0000000000000000<hash8> = percorso/png`. I PNG sono **4x** l'originale e ridisegnano esattamente la stessa area. Texture identiche tra lingue hanno lo stesso hash: la sostituzione vale per tutte (vedi `INVENTARIO_TEXTURE.md`).

### Struttura reale (da `documentazione/modifiche_it/pack_struttura.csv`)
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

Il **pack di base `PSP/TEXTURES/ULES00600` e' gia' italiano**: contiene `cards/small_it`, `large_it`, `tiny_it`, `ui_it` (interfaccia italiana) e le tessere italiane del titolo; le altre lingue sono moduli separati in `PSP/TEXTURES/moduli/<l>`.

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

Cartelle della lingua: `frame` (13 file), `large` (2833 file), `large_it` (2833 file), `small` (2833 file), `small_it` (2833 file), `tinyEN` (7 file), `tinyJP` (7 file), `tinyMikeyMK` (7 file), `tiny_it` (7 file). Ogni carta ha una **piccola HD** (nome + descrizione + tipo, rigenerata con font liberi OFL: XCharter Bold per nomi/tipo/etichette, Libre Baskerville per gli effetti, Newsreader Italic per i Normali, PT Serif Caption per Magie/Trappole, Charis SIL per i glifi mancanti) e una **grande HD** (solo il nome sulla cornice). In piu': la **tabella degli attributi** con le parole della lingua (`cards/frame/icons_attribute_race_<l>.png`, `attributi.py`), l'**etichetta Magia/Trappola** (`icons_spell_trap_<l>.png`, `label_it.py` / `estrai_etichette.py` -> `dati/label_eu_<codice>_128x32.png`) e l'**atlante delle miniature** del deck (`tiny_<l>`, `atlante_tiny.py` + `frammento_tiny.py`).

Quando cambia il testo di una carta (sezione A2) vanno rigenerate le sue immagini: **181 carte** nel italiano. Elenco in `documentazione/modifiche_it/carte_immagini.csv`. Comando: `sh strumenti/rigenera_correzioni.sh USRDIR PACK_USA PACK_MOD PYTHON` (carte piccole + grandi); su Windows `python -I` non vede i pacchetti utente: passare un wrapper che scarta `-I`.

Tipografia: apostrofo tipografico dell'italiano e virgolette; `Tipo`, `Terreno`, `Evocazione tramite Tributo` come nel gioco.

## B3. Interfaccia HD in italiano (`ui_it`)

**105 texture** (`documentazione/modifiche_it/texture_ui.csv`: file, hash PPSSPP, famiglia, script, dimensioni originale/HD, neutra/specifica, origine nella ISO). Per famiglia: fogli_icone 8, lettere_esito 23, menu_liste 6, schede_deck 16, schede_ricette 17, schermata_vs 14, scritte_duello 15, tutorial 6. Di queste 11 sono neutre (stesso hash in tutte le lingue) e 94 specifiche. Ogni famiglia ha uno script in `strumenti/ui_it/<famiglia>.py` (lettura `TF1_LANG`): ridisegna le scritte texture per texture partendo dall'originale a bassa risoluzione della ISO e dallo stile del pack inglese; stessa area e stesse posizioni (il gioco ritaglia da rettangoli fissi); un font/peso/linea di base/ombra per scritta; font liberi (`font_alt.py`).

| famiglia | texture | script | archivio ISO sorgente | testi della lingua |
|---|---|---|---|---|
| fogli_icone | 8 | `strumenti/ui_it/fogli_icone.py` | deck/all_i.ehp, shop/all_i.ehp, field/always_* | fogli di icone: `icon04` (Mia/L e distintivi), `s_pack` (ESAURITE), `panel` (frammento del tab), `icon06` (N), `pda_pack01` (NUOVO), `mein_menu00`, `trnsmt01`, `ocglist` |
| lettere_esito | 23 | `strumenti/ui_it/lettere_esito.py` | duel/basic_ii.ehp | HAI VINTO · HAI PERSO · PAREGGIO: una tessera 64x64 per lettera (lettere ripetute riusano la stessa tessera) + silhouette |
| menu_liste | 6 | `strumenti/ui_it/menu_liste.py` | title_menu/title_menu_i.ehp, duel/result/result_i.ehp, field/always_bri_<cod>.ehp | titoli dei menu (`m_menu_title01`, `trnsmt02`, `menu02`, `press_start0003`), etichette risultato, calendario (giorni, mesi, "giorni al torneo", Mattino/Sera) |
| schede_deck | 16 | `strumenti/ui_it/schede_deck.py` | deck/all_i.ehp, labo/*.ehp, shop/all_i.ehp | linguette Cassa, **Fusion**, Side, Deck, Affitto, Laboratorio, Convertitore, "Tipi di Carte Posseduti", "Carte Comprate", tasto INVIO |
| schede_ricette | 17 | `strumenti/ui_it/schede_ricette.py` | deck/recipe_view_i.ehp, title_menu/title_menu_i.ehp, database/limitlist.ehp | linguette Personaggio / Utente / Scaricata / Limitata / Semi-limitata / Vietata / Scambio e pannelli ricette |
| schermata_vs | 14 | `strumenti/ui_it/schermata_vs.py` | duel/start/start_e.ehp (membri _i), start_all.ehp, start_i.ehp | banner DUEL / NORMAL / TAG, bagliori, "Modalità ...", "n A GIOCARE", "n Duello", foglio sasso-carta-forbici (VITTORIA/SCONFITTA/PAREGGIO), foglio giocatori ("n° GIOCATORE") |
| scritte_duello | 15 | `strumenti/ui_it/scritte_duello.py` | duel/basic_ii.ehp | Catena · TURNO (blu/rosso) · TOCCA AL GIOCATORE SUCCESSIVO (spezzata su 2 texture) · INIZIA IL DUELLO · Attacco Diretto! · foglio numeri `card_icon03` (vedi B4) |
| tutorial | 6 | `strumenti/ui_it/tutorial.py` | tutorial/tutorial_i.ehp (tuto_duelimg01..06) | illustrazione del dialogo di attivazione (testi, bottoni SI/NO, carta piccola) + 5 cartine con disco del tipo |

Regole di qualita' (valgono per ogni lingua): lettere regolari, mai deformate una per una; stessa area dell'originale; niente sfocature; il testo e' quello dell'originale della lingua (si correggono solo errori evidenti: residui di altre lingue, accenti); pixel art **non** levigata senza conferma; geometrie sempre misurate sull'originale.

### Testi disegnati: originale -> HD
Tabella letta a occhio, texture per texture: `documentazione/modifiche_it/testi_texture_it.md`. Differenze rispetto all'originale: `TAUSCHEN`/`Tauschen` -> `SCAMBIO`/`Scambio`, `Fusione` -> `Fusion`; tutto il resto riscrive le stesse parole.

### Elenco di ogni texture
(tutte le 105 righe, da `texture_ui.csv`)

| file nel pack | hash | famiglia | originale px | HD px | tipo | origine ISO |
|---|---|---|---|---|---|---|
| ui_it/fogli_icone/all_i__icon04.png | 0f47adc6 | fogli_icone | 128x128 | 512x512 | SPECIFICA | deck/all_i.ehp:icon04.gim |
| ui_it/fogli_icone/all_i__panel.png | 51288b63 | fogli_icone | 256x256 | 1024x1024 | SPECIFICA | shop/all_i.ehp:panel.gim |
| ui_it/fogli_icone/all_i__s_pack.png | 5f349a93 | fogli_icone | 256x256 | 1024x1024 | SPECIFICA | shop/all_i.ehp:s_pack.gim |
| ui_it/fogli_icone/always_bri_ita__pda_pack01.png | e5169419 | fogli_icone | 512x256 | 2048x1024 | SPECIFICA | field/always_bri_ita.ehp:pda_pack01.gim; field/always_fra_ita.ehp:pda_pack01.gim; field/always_ger_ita.ehp:pda_pack01.gim |
| ui_it/fogli_icone/cardalbum__icon06_i.png | aaef4267 | fogli_icone | 128x128 | 512x512 | SPECIFICA | database/cardalbum.ehp:icon06_i.gim; deck/all_i.ehp:icon06.gim; field/always_bri_ita.ehp:card_icon06.gim |
| ui_it/fogli_icone/cardalbum__ocglist_i.png | 295c8b9c | fogli_icone | 128x64 | 512x256 | NEUTRA | database/cardalbum.ehp:ocglist_e.gim; database/cardalbum.ehp:ocglist_f.gim; database/cardalbum.ehp:ocglist_g.gim |
| ui_it/fogli_icone/title_menu_i__mein_menu00.png | 22692070 | fogli_icone | 128x64 | 512x256 | SPECIFICA | title_menu/title_menu_i.ehp:mein_menu00.gim |
| ui_it/fogli_icone/title_menu_i__trnsmt01.png | bdc35d0d | fogli_icone | 256x128 | 1024x512 | SPECIFICA | title_menu/title_menu_i.ehp:trnsmt01.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100002.png | 60e58b0c | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_draw100002.gim; duel/basic_fi.ehp:duel_draw100002.gim; duel/basic_gi.ehp:duel_draw100002.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100004.png | ce971331 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_draw100004.gim; duel/basic_fi.ehp:duel_draw100004.gim; duel/basic_gi.ehp:duel_draw100004.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100006.png | d2e20c6c | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_draw100006.gim; duel/basic_fi.ehp:duel_draw100006.gim; duel/basic_gi.ehp:duel_draw100006.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100008.png | 1deeba15 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_draw100008.gim; duel/basic_fi.ehp:duel_draw100008.gim; duel/basic_gi.ehp:duel_draw100008.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100010.png | 9a3bba37 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_draw100010.gim; duel/basic_fi.ehp:duel_draw100010.gim; duel/basic_gi.ehp:duel_draw100010.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100012.png | f869c721 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_draw100012.gim; duel/basic_fi.ehp:duel_draw100012.gim; duel/basic_gi.ehp:duel_draw100012.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100014.png | 3d00ca65 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_draw100014.gim; duel/basic_fi.ehp:duel_draw100014.gim; duel/basic_gi.ehp:duel_draw100014.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100002.png | 23e6f72d | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_lose100002.gim; duel/basic_fi.ehp:duel_lose100002.gim; duel/basic_gi.ehp:duel_lose100002.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100004.png | aa67eb3a | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_lose100004.gim; duel/basic_fi.ehp:duel_lose100004.gim; duel/basic_gi.ehp:duel_lose100004.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100006.png | 0b9f2dfd | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_lose100006.gim; duel/basic_fi.ehp:duel_lose100006.gim; duel/basic_gi.ehp:duel_lose100006.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100008.png | 8c1ca0ea | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_lose100008.gim; duel/basic_fi.ehp:duel_lose100008.gim; duel/basic_gi.ehp:duel_lose100008.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100010.png | f7a3a889 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_lose100010.gim; duel/basic_fi.ehp:duel_lose100010.gim; duel/basic_gi.ehp:duel_lose100010.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100012.png | a3668e35 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_lose100012.gim; duel/basic_fi.ehp:duel_lose100012.gim; duel/basic_gi.ehp:duel_lose100012.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100014.png | be8d27c2 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_lose100014.gim; duel/basic_fi.ehp:duel_lose100014.gim; duel/basic_gi.ehp:duel_lose100014.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100016.png | 48fccb29 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_lose100016.gim; duel/basic_fi.ehp:duel_lose100016.gim; duel/basic_gi.ehp:duel_lose100016.gim |
| ui_it/lettere_esito/basic_ii__duel_win100002.png | 00b45490 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_win100002.gim; duel/basic_fi.ehp:duel_win100002.gim; duel/basic_gi.ehp:duel_win100002.gim |
| ui_it/lettere_esito/basic_ii__duel_win100004.png | d38eeaf8 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_win100004.gim; duel/basic_fi.ehp:duel_win100004.gim; duel/basic_gi.ehp:duel_win100004.gim |
| ui_it/lettere_esito/basic_ii__duel_win100006.png | 64e53c06 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_win100006.gim; duel/basic_fi.ehp:duel_win100006.gim; duel/basic_gi.ehp:duel_win100006.gim |
| ui_it/lettere_esito/basic_ii__duel_win100008.png | 6cb385d2 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_win100008.gim; duel/basic_fi.ehp:duel_win100008.gim; duel/basic_gi.ehp:duel_win100008.gim |
| ui_it/lettere_esito/basic_ii__duel_win100010.png | ed0059c9 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_win100010.gim; duel/basic_fi.ehp:duel_win100010.gim; duel/basic_gi.ehp:duel_win100010.gim |
| ui_it/lettere_esito/basic_ii__duel_win100012.png | 8be1d58a | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_win100012.gim; duel/basic_fi.ehp:duel_win100012.gim; duel/basic_gi.ehp:duel_win100012.gim |
| ui_it/lettere_esito/basic_ii__duel_win100014.png | 145d1dd3 | lettere_esito | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:duel_win100014.gim; duel/basic_fi.ehp:duel_win100014.gim; duel/basic_gi.ehp:duel_win100014.gim |
| ui_it/lettere_esito/basic_ii__duel_win100016.png | 736cf75e | lettere_esito | 64x32 | 256x128 | SPECIFICA | duel/basic_bi.ehp:duel_win100016.gim; duel/basic_fi.ehp:duel_win100016.gim; duel/basic_gi.ehp:duel_win100016.gim |
| ui_it/menu_liste/always_bri_ita__story_sys02.png | 5fc07dd2 | menu_liste | 256x128 | 1024x512 | SPECIFICA | field/always_bri_ita.ehp:story_sys02.gim; field/always_fra_ita.ehp:story_sys02.gim; field/always_ger_ita.ehp:story_sys02.gim |
| ui_it/menu_liste/result_i__menu01.png | 23b37425 | menu_liste | 256x64 | 1024x256 | SPECIFICA | duel/result/result_i.ehp:menu01.gim |
| ui_it/menu_liste/result_i__menu02.png | aeddb824 | menu_liste | 256x128 | 1024x512 | SPECIFICA | duel/result/result_i.ehp:menu02.gim |
| ui_it/menu_liste/title_menu_i__m_menu_title01.png | cfe8de2a | menu_liste | 256x128 | 1024x512 | SPECIFICA | title_menu/title_menu_i.ehp:m_menu_title01.gim |
| ui_it/menu_liste/title_menu_i__press_start0003.png | 747668a4 | menu_liste | 256x16 | 1024x64 | SPECIFICA | title_menu/title_menu_i.ehp:press_start0003.gim |
| ui_it/menu_liste/title_menu_i__trnsmt02.png | 7f3a4012 | menu_liste | 256x256 | 1024x1024 | SPECIFICA | title_menu/title_menu_i.ehp:trnsmt02.gim |
| ui_it/schede_deck/all_i__d_window00008.png | e6b24eae | schede_deck | 128x32 | 512x128 | SPECIFICA | deck/all_i.ehp:d_window00008.gim |
| ui_it/schede_deck/all_i__d_window00016.png | 27153d30 | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_i.ehp:d_window00016.gim |
| ui_it/schede_deck/all_i__d_window00024.png | fd0f9c3b | schede_deck | 64x32 | 256x128 | NEUTRA | deck/all_e.ehp:d_window00024.gim; deck/all_f.ehp:d_window00024.gim; deck/all_g.ehp:d_window00024.gim |
| ui_it/schede_deck/all_i__d_window00031.png | b77db24b | schede_deck | 64x32 | 256x128 | NEUTRA | deck/all_e.ehp:d_window00031.gim; deck/all_f.ehp:d_window00031.gim; deck/all_g.ehp:d_window00031.gim |
| ui_it/schede_deck/all_i__d_window00033.png | 339f25bd | schede_deck | 256x32 | 1024x128 | SPECIFICA | deck/all_i.ehp:d_window00033.gim |
| ui_it/schede_deck/all_i__d_window00034.png | 1659d75e | schede_deck | 256x32 | 1024x128 | NEUTRA | deck/all_e.ehp:d_window00034.gim; deck/all_f.ehp:d_window00034.gim; deck/all_g.ehp:d_window00034.gim |
| ui_it/schede_deck/all_i__d_window00051.png | cefa3d7e | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_i.ehp:d_window00051.gim |
| ui_it/schede_deck/all_i__d_window00062.png | f5fd73f9 | schede_deck | 128x32 | 512x128 | SPECIFICA | deck/all_i.ehp:d_window00062.gim; labo/conv_machine.ehp:window_i0016.gim; title_menu/title_menu_i.ehp:t_window0015.gim |
| ui_it/schede_deck/all_i__d_window00101.png | 22ebca63 | schede_deck | 64x32 | 256x128 | SPECIFICA | deck/all_i.ehp:d_window00101.gim; labo/rental.ehp:window_i0008.gim |
| ui_it/schede_deck/all_i__d_window00120.png | 4556da1f | schede_deck | 64x32 | 256x128 | NEUTRA | deck/all_e.ehp:d_window00120.gim; deck/all_f.ehp:d_window00120.gim; deck/all_g.ehp:d_window00120.gim |
| ui_it/schede_deck/all_i__tab_title.png | 6852c8c2 | schede_deck | 256x32 | 1024x128 | SPECIFICA | shop/all_i.ehp:tab_title.gim |
| ui_it/schede_deck/conv_machine__window_i0009.png | 6ca9eba7 | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/conv_machine.ehp:window_i0009.gim; labo/conv_machine.ehp:window_i0026.gim |
| ui_it/schede_deck/conv_machine__window_i0022.png | ada2c664 | schede_deck | 256x32 | 1024x128 | NEUTRA | labo/conv_machine.ehp:window_f0022.gim; labo/conv_machine.ehp:window_g0022.gim; labo/conv_machine.ehp:window_i0022.gim |
| ui_it/schede_deck/password__key_i0027.png | 37603c6b | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/password.ehp:key_i0027.gim |
| ui_it/schede_deck/rental__window_i0015.png | fee49520 | schede_deck | 128x32 | 512x128 | SPECIFICA | labo/rental.ehp:window_i0015.gim; labo/rental.ehp:window_s0015.gim |
| ui_it/schede_deck/rental__window_i0026.png | d4ea2e3a | schede_deck | 64x32 | 256x128 | SPECIFICA | labo/rental.ehp:window_i0026.gim |
| ui_it/schede_ricette/duelrecord__parts_i.png | 4e51e475 | schede_ricette | 128x64 | 512x256 | SPECIFICA | database/duelrecord.ehp:parts_i.gim |
| ui_it/schede_ricette/limitlist__window_i0002.png | 6c94dcad | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_i0002.gim |
| ui_it/schede_ricette/limitlist__window_i0004.png | 9acba8ec | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_i0004.gim |
| ui_it/schede_ricette/limitlist__window_i0012.png | 5c0e1d7a | schede_ricette | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_i0012.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010002.png | 763a4766 | schede_ricette | 256x256 | 1024x1024 | NEUTRA | deck/recipe_view_e.ehp:recipe010002.gim; deck/recipe_view_f.ehp:recipe010002.gim; deck/recipe_view_g.ehp:recipe010002.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010004.png | b2427f09 | schede_ricette | 256x64 | 1024x256 | SPECIFICA | deck/recipe_view_e.ehp:recipe010004.gim; deck/recipe_view_f.ehp:recipe010004.gim; deck/recipe_view_i.ehp:recipe010004.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010006.png | 44c8b170 | schede_ricette | 256x64 | 1024x256 | NEUTRA | deck/recipe_view_e.ehp:recipe010006.gim; deck/recipe_view_f.ehp:recipe010006.gim; deck/recipe_view_g.ehp:recipe010006.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010008.png | 9b52cd0c | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_i.ehp:recipe010008.gim; title_menu/title_menu_i.ehp:recipe_sel00002.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010015.png | 9d53d71b | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_i.ehp:recipe010015.gim; title_menu/title_menu_i.ehp:recipe_sel00009.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010027.png | eb6d8202 | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_i.ehp:recipe010027.gim; title_menu/title_menu_i.ehp:recipe_sel00020.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010029.png | 29e9a88e | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_i.ehp:recipe010029.gim; title_menu/title_menu_i.ehp:recipe_sel00022.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010031.png | 4ceb96c4 | schede_ricette | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_i.ehp:recipe010031.gim; title_menu/title_menu_i.ehp:recipe_sel00024.gim |
| ui_it/schede_ricette/title_menu_i__dmenu_recipe.png | e1ba3fc9 | schede_ricette | 128x32 | 512x128 | NEUTRA | title_menu/title_menu_e.ehp:dmenu_recipe.gim; title_menu/title_menu_f.ehp:dmenu_recipe.gim; title_menu/title_menu_g.ehp:dmenu_recipe.gim |
| ui_it/schede_ricette/title_menu_i__recipe_panel.png | 35c103aa | schede_ricette | 128x128 | 512x512 | NEUTRA | title_menu/title_menu_e.ehp:recipe_panel.gim; title_menu/title_menu_f.ehp:recipe_panel.gim; title_menu/title_menu_g.ehp:recipe_panel.gim |
| ui_it/schede_ricette/title_menu_i__recipe_sel00033.png | 13e83af2 | schede_ricette | 128x32 | 512x128 | SPECIFICA | title_menu/title_menu_i.ehp:recipe_sel00033.gim |
| ui_it/schede_ricette/title_menu_i__t_window0008.png | edf9b615 | schede_ricette | 64x32 | 256x128 | SPECIFICA | title_menu/title_menu_i.ehp:t_window0008.gim |
| ui_it/schede_ricette/title_menu_i__t_window0026.png | 50bfc4e3 | schede_ricette | 64x32 | 256x128 | SPECIFICA | title_menu/title_menu_i.ehp:t_window0026.gim |
| ui_it/schermata_vs/start_all__jyanken20_i0005.png | 84daf8b2 | schermata_vs | 256x32 | 1024x128 | SPECIFICA | duel/start/start_all.ehp:jyanken20_i0005.gim; duel/start/start_e.ehp:jyanken20_i0005.gim; duel/start/start_f.ehp:jyanken20_i0005.gim |
| ui_it/schermata_vs/start_all__jyanken20_i0007.png | f5bbbb53 | schermata_vs | 256x32 | 1024x128 | SPECIFICA | duel/start/start_all.ehp:jyanken20_i0007.gim; duel/start/start_e.ehp:jyanken20_i0007.gim; duel/start/start_f.ehp:jyanken20_i0007.gim |
| ui_it/schermata_vs/start_all__vs_much1_i0001.png | a50e57e6 | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much1_i0001.gim; duel/start/start_e.ehp:vs_much1_i0001.gim; duel/start/start_f.ehp:vs_much1_i0001.gim |
| ui_it/schermata_vs/start_all__vs_much2_i0001.png | 8f118f8a | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much2_i0001.gim; duel/start/start_e.ehp:vs_much2_i0001.gim; duel/start/start_f.ehp:vs_much2_i0001.gim |
| ui_it/schermata_vs/start_all__vs_much3_i0001.png | ae083f33 | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much3_i0001.gim; duel/start/start_e.ehp:vs_much3_i0001.gim; duel/start/start_f.ehp:vs_much3_i0001.gim |
| ui_it/schermata_vs/start_e__d_menu01_i.png | f098096b | schermata_vs | 256x256 | 1024x1024 | SPECIFICA | duel/start/start_e.ehp:d_menu01_i.gim; duel/start/start_f.ehp:d_menu01_i.gim; duel/start/start_g.ehp:d_menu01_i.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0005.png | 50201760 | schermata_vs | 256x32 | 1024x128 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_i0005.gim; duel/start/start_f.ehp:vs_bg01_1_i0005.gim; duel/start/start_g.ehp:vs_bg01_1_i0005.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0007.png | 92f2114b | schermata_vs | 256x64 | 1024x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_i0007.gim; duel/start/start_f.ehp:vs_bg01_1_i0007.gim; duel/start/start_g.ehp:vs_bg01_1_i0007.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0008.png | 5fb4b6dc | schermata_vs | 256x64 | 1024x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_i0008.gim; duel/start/start_f.ehp:vs_bg01_1_i0008.gim; duel/start/start_g.ehp:vs_bg01_1_i0008.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0012.png | 01c81cd4 | schermata_vs | 128x32 | 512x128 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_i0012.gim; duel/start/start_f.ehp:vs_bg01_1_i0012.gim; duel/start/start_g.ehp:vs_bg01_1_i0012.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0014.png | 413ccf1d | schermata_vs | 128x64 | 512x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_i0014.gim; duel/start/start_f.ehp:vs_bg01_1_i0014.gim; duel/start/start_g.ehp:vs_bg01_1_i0014.gim |
| ui_it/schermata_vs/start_e__vs_bg01_2_i0001.png | 005ca7af | schermata_vs | 128x32 | 512x128 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_2_i0001.gim; duel/start/start_f.ehp:vs_bg01_2_i0001.gim; duel/start/start_g.ehp:vs_bg01_2_i0001.gim |
| ui_it/schermata_vs/start_e__vs_bg01_2_i0004.png | 6b0b0fbd | schermata_vs | 128x16 | 512x64 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_2_i0004.gim; duel/start/start_f.ehp:vs_bg01_2_i0004.gim; duel/start/start_g.ehp:vs_bg01_2_i0004.gim |
| ui_it/schermata_vs/start_i__jnk_card01.png | 38e5ae61 | schermata_vs | 512x256 | 2048x1024 | SPECIFICA | duel/start/start_i.ehp:jnk_card01.gim |
| ui_it/scritte_duello/basic_ii__card_icon03.png | 376925c7 | scritte_duello | 128x128 | 512x512 | SPECIFICA | duel/basic_bi.ehp:card_icon03.gim; duel/basic_fi.ehp:card_icon03.gim; duel/basic_gi.ehp:card_icon03.gim |
| ui_it/scritte_duello/basic_ii__card_side.png | dfbaa424 | scritte_duello | 64x32 | 256x128 | NEUTRA | duel/basic_be.ehp:card_side.gim; duel/basic_bf.ehp:card_side.gim; duel/basic_bg.ehp:card_side.gim |
| ui_it/scritte_duello/basic_ii__chain010003.png | 235b1041 | scritte_duello | 64x32 | 256x128 | SPECIFICA | duel/basic_bi.ehp:chain010003.gim; duel/basic_fi.ehp:chain010003.gim; duel/basic_gi.ehp:chain010003.gim |
| ui_it/scritte_duello/basic_ii__chain010005.png | 79b7261f | scritte_duello | 128x32 | 512x128 | SPECIFICA | duel/basic_bi.ehp:chain010005.gim; duel/basic_fi.ehp:chain010005.gim; duel/basic_gi.ehp:chain010005.gim |
| ui_it/scritte_duello/basic_ii__dilect_atk00001.png | ba952e24 | scritte_duello | 256x32 | 1024x128 | SPECIFICA | duel/basic_bi.ehp:dilect_atk00001.gim; duel/basic_fi.ehp:dilect_atk00001.gim; duel/basic_gi.ehp:dilect_atk00001.gim |
| ui_it/scritte_duello/basic_ii__dilect_atk00003.png | 58789f5c | scritte_duello | 128x32 | 512x128 | SPECIFICA | duel/basic_bi.ehp:dilect_atk00003.gim; duel/basic_fi.ehp:dilect_atk00003.gim; duel/basic_gi.ehp:dilect_atk00003.gim |
| ui_it/scritte_duello/basic_ii__next_player0001.png | 8abf9d52 | scritte_duello | 64x32 | 256x128 | SPECIFICA | duel/basic_bi.ehp:next_player0001.gim; duel/basic_fi.ehp:next_player0001.gim; duel/basic_gi.ehp:next_player0001.gim |
| ui_it/scritte_duello/basic_ii__next_player0002.png | 6bc72dfe | scritte_duello | 256x32 | 1024x128 | SPECIFICA | duel/basic_bi.ehp:next_player0002.gim; duel/basic_fi.ehp:next_player0002.gim; duel/basic_gi.ehp:next_player0002.gim |
| ui_it/scritte_duello/basic_ii__next_player0004.png | 8a774ddd | scritte_duello | 64x32 | 256x128 | SPECIFICA | duel/basic_bi.ehp:next_player0004.gim; duel/basic_fi.ehp:next_player0004.gim; duel/basic_gi.ehp:next_player0004.gim |
| ui_it/scritte_duello/basic_ii__next_player0005.png | 83cf47f4 | scritte_duello | 256x32 | 1024x128 | SPECIFICA | duel/basic_bi.ehp:next_player0005.gim; duel/basic_fi.ehp:next_player0005.gim; duel/basic_gi.ehp:next_player0005.gim |
| ui_it/scritte_duello/basic_ii__score-top100011.png | 36655dfa | scritte_duello | 32x32 | 128x128 | SPECIFICA | duel/basic_bi.ehp:score-top100011.gim; duel/basic_bs.ehp:score-top100011.gim; duel/basic_fi.ehp:score-top100011.gim |
| ui_it/scritte_duello/basic_ii__score-top100013.png | 97d1b9a7 | scritte_duello | 32x32 | 128x128 | SPECIFICA | duel/basic_bi.ehp:score-top100013.gim; duel/basic_bs.ehp:score-top100013.gim; duel/basic_fi.ehp:score-top100013.gim |
| ui_it/scritte_duello/basic_ii__start_duel10001.png | faf5cb43 | scritte_duello | 64x64 | 256x256 | SPECIFICA | duel/basic_bi.ehp:start_duel10001.gim; duel/basic_fi.ehp:start_duel10001.gim; duel/basic_gi.ehp:start_duel10001.gim |
| ui_it/scritte_duello/basic_ii__start_duel10002.png | 04bb7f71 | scritte_duello | 256x64 | 1024x256 | SPECIFICA | duel/basic_bi.ehp:start_duel10002.gim; duel/basic_fi.ehp:start_duel10002.gim; duel/basic_gi.ehp:start_duel10002.gim |
| ui_it/scritte_duello/basic_ii__start_duel10005.png | ad550ab4 | scritte_duello | 128x32 | 512x128 | SPECIFICA | duel/basic_bi.ehp:start_duel10005.gim; duel/basic_fi.ehp:start_duel10005.gim; duel/basic_gi.ehp:start_duel10005.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg01.png | 7dd7d0f0 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_i.ehp:tuto_duelimg01.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg02.png | 71437f61 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_i.ehp:tuto_duelimg02.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg03.png | f78156cc | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_i.ehp:tuto_duelimg03.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg04.png | ee87c47c | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_i.ehp:tuto_duelimg04.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg05.png | 866124a4 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_i.ehp:tuto_duelimg05.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg06.png | 030db8b7 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_i.ehp:tuto_duelimg06.gim |

### Texture italiane senza controparte in `ui_fr` (19) e perche'
13 sono neutre (stesso hash in tutte le lingue: pannelli ricette, linguette Side/Deck/Fusion Deck, barre, `card_side`...). 6 hanno wording locale nell'originale (`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `d_window00016`, `duelrecord parts`): l'italiano ha NUOVO / N / Fusion, il francese originale ha NEW / Fusion e ha gia' i suoi HD in `upscale_extra`. La linguetta dell'editor deck dice **Fusion** (non "Fusione"): "Fusion Deck" si chiama cosi' in tutte le lingue.

## B4. Il foglio dei numeri del duello (`card_icon03`)

Foglio unico con cifre LP, tempo, tasti e moltiplicatori; hash diverso per lingua. Ricetta scelta dall'utente (`strumenti/ui_it/icon03_lingue.py`, rilanciare con `--applica`):
- righe 0-180 (cifre piccole e segni, tasti arancioni 1/2/3, cifre grandi 0-9 con "LP", cifre piccole 0-9): **dal pack USA**, pixel art netta;
- celle in cui il gioco europeo differisce dal pack USA (spunta nera, palla grigia, pillola vuota, parola del tempo): **pixel originali ingranditi 4x senza sfumare**; parola del tempo **TEMPO**; la pillola arancione ("Single" nel pack USA) resta **vuota**;
- righe >= 181 (moltiplicatori x1..x12, icone, carte, frecce): dal foglio italiano gia' nel pack (`strumenti/dati/card_icon03_base_it.png`);
- le celle europee si incollano **solo nella loro fascia** di righe (altrimenti rovinano la parte alta delle cifre grandi).

File: it -> `ui_it/scritte_duello/basic_ii__card_icon03.png` (hash 376925c7); fr -> `upscale_extra/3e5482fd.png`; en ee0c44c3; de ffe309a6; es 859eea2b. Anteprime in `confronti/icon03/`.

## B5. Targa del titolo

`python strumenti/ui_it/titolo_pomodoro.py it` genera 2 PNG (`542eff79685c434d`, `705176739829dcf5`, tessere 18 e 19 del fondale di 20 tessere 128x64 `title_menu_i.ehp: main_title00001..00020`) con la carta 4930 nella lingua + la formula "versione" + la bandiera, font PT Sans Bold: **"VERSIONE POMODORO MISTICO"**. La targa **va inclusa solo per la lingua scelta** (vive in `moduli/it/intro/title_screen/`); il pack di base originale ha le tessere senza banner. File in questo pack: `ULES00600/intro/title_screen/00000000542eff79685c434d.png`, `ULES00600/intro/title_screen/00000000705176739829dcf5.png`.

## B6. `textures.ini` e composizione

`strumenti/gen_ini.py TOOLS US_INI CARD_DIR OUT_INI i=it +extra_it.ini +ui_it.ini +dati/upscale_extra.ini` converte il `textures.ini` USA in quello EU: le voci non-carta restano (texture neutre = stessi hash); le voci carta sono rigenerate dagli archivi `card/*.cip` EU per le 5 lingue (`i=it` rimappa `cards/large/X.png` -> `cards/large_it/X.png`); aggiunge l'etichetta Magia/Trappola (`extra_it.ini`), le righe `ui_it` e `upscale_extra.ini`. Si fa anche per i 3 stili carte. Se gli stessi pixel esistono in piu' lingue vince la prima in `e i f g s` (per questo atlante, banner e tabella attributi sono "uno per installazione").

Righe `ui_it` nel `textures.ini`: 105. Frequenza dei prefissi: `documentazione/modifiche_it/ini_righe.csv`. Controllo: ogni riga `ui_it/...` deve puntare a un file esistente e non devono esserci hash duplicati.

## B7. Installazione e impostazioni

PC: copiare `ULES00600` in `<PPSSPP>/PSP/TEXTURES/` (Android: `textures.zip` in `.../TEXTURES/ULES00600/`, senza estrarlo; rigenerare lo zip con le correzioni). Impostazioni: **Sostituisci texture ON**, risoluzione di rendering **4x**, lingua del gioco = lingua del modulo (la lingua e' scritta nel **salvataggio**). Dopo aver cambiato un solo PNG basta copiarlo e riavviare PPSSPP (cache). Per provare i testi usare la ISO `_definitiva`.

---

# C. SCELTE EDITORIALI

- **Preside** (mai "Cancelliere") per Sheppard, compreso "Ufficio del Preside" e "Profilo del Preside Sheppard".
- **Segna-Mostro** (non "Gettoni Mostro") in aiuti, record e carte; `Segna-Opzione`.
- Banner: "direttore dello Slifer Rosso"; dormitori **Slifer Rosso, Ra Giallo, Obelisk Blu**; `Modalità Storia` e' il nome del menu.
- Linguetta **Fusion** (non Fusione). `E'` -> `È`; `Life Point` -> `Life Points`; punteggiatura e apostrofi corretti.
- Scene censurate riportate al giapponese: sake/shochu e abito da cameriera (vedi sotto); "Beh, non sono poi così bravo..." (era "sto sbavando").
- Foglio numeri: cifre/LP dal pack USA, x1..x12 dal foglio italiano, parola del tempo TEMPO.

### Voci del registro delle scelte per questa lingua (`strumenti/dati/registro_scelte_editoriali.json`)
| id | originale | corretto | ereditata | motivo |
|---|---|---|---|---|
| st01_t01/Scr003E#146 | Mio padre possiede un'azienda che⏎produce salsa piccante. | La mia famiglia produce sake. | no | sake al posto di salsa piccante (fedele al giapponese: la famiglia di Chumley fa sake) |
| st01_t01/Scr003E#147 | Mi ha mandato della salsa piccante⏎con la mia ultima paga.⏎Ti farò uno sconto ragionevole.⏎Vuoi... | L'altro giorno mi hanno mandato dello shochu⏎insieme ai soldi da casa, quindi la prossima volta... | no | shochu al posto di salsa piccante |
| st01_t01/Scr003E#150 | Mio padre possiede un'azienda che⏎produce salsa piccante. | None | si | come 146 |
| st01_t01/Scr003E#151 | Mi ha mandato della salsa piccante con la ⏎mia ultima paga.⏎Ti farò uno sconto ragionevole.⏎Vuoi... | L'altro giorno mi hanno mandato dello shochu⏎insieme ai soldi da casa, quindi la prossima volta... | no | come 147 |
| st01_t01/Scr003E#163 | Wow, ce l'hai fatta sul serio.⏎È 《C026_2》...⏎E indossa un bikini! | Wow, ce l'hai fatta sul serio.⏎È 《C026_2》...⏎In abito da cameriera! | no | abito da cameriera al posto di bikini (giapponese: メイド服) |
| st01_t01/Scr003E#168 | Wow, ce l'hai fatta sul serio.⏎È 《C026_2》...⏎E indossa un bikini! | None | si | come 163 |
| st01_t01/Scr003E#188 | Oddio, sto sbavando un po'... | Oddio, non sono un granché... | no | solo italiano: "sto sbavando" era un errore di traduzione (giapponese: "non sono poi così bravo") |
| st01_t01/Scr003E#189 | Ehi, puoi farmi un disegno?⏎Disegnami 《C026_2》 in bikini! | Ehi, puoi farmi un disegno?⏎Disegnami 《C026_2》 vestita da cameriera! | no | abito da cameriera al posto di bikini |
| st01_t01/Scr003E#191 | Ecco, usa questo! | Ecco, usa questo vestito da cameriera! | no | Syrus passa un abito da cameriera come modello (メイド服): col bikini la battuta non aveva senso |
| st01_t01/Scr003E#194 | Oddio, sto sbavando un po'... | None | si | come 188 |
| st01_t01/Scr003E#195 | Ehi, puoi farmi un disegno?⏎Disegnami 《C026_2》 in bikini! | None | si | come 189 |
| st01_t01/Scr003E#197 | Ecco, usa questo! | Ecco, usa questo vestito da cameriera! | no | come 191 |

Altre scelte e la rilettura delle frasi dei duelli: `REGISTRO_SCELTE.md`.

# D. VERIFICA IN GIOCO

- Visto in gioco: interfaccia HD italiana, stringhe lunghe riscritte (aiuti, schede, tutorial), terminologia Preside/Segna-Mostro, carte HD e etichetta Magia/Trappola della carta grande.
- **Non visto** dopo gli ultimi cambi: rilettura carte (65 carte nuove), frasi dei duelli corrette, linguetta "Fusion", 4 avvisi di lunghezza box dei dialoghi (en/es/de #147/#151, de #172).

# E. COME RIGENERARE TUTTO

```
# ISO (tutte le lingue insieme)
python strumenti/correzioni/costruisci_dialoghi.py it
python strumenti/correzioni/genera_lingua.py it CARDINFO_it.ehp          # carte
python strumenti/correzioni/applica_iso.py PSP/GAME/ULES00600_..._EUR.iso PSP/GAME/ULES00600_..._EUR_definitiva.iso
# immagini
sh strumenti/rigenera_correzioni.sh USRDIR PACK_USA PACK_MOD PYTHON
TF1_LANG=it python strumenti/ui_it/<famiglia>.py USRDIR PACK_USA <modulo>      # per ognuna delle 8 famiglie (intera!)
python strumenti/ui_it/icon03_lingue.py --applica ; python strumenti/ui_it/titolo_pomodoro.py it
python strumenti/componi_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/moduli USRDIR/card OUT it --copia
# questo documento
python strumenti/analisi/documenta_modifiche.py ISO_ORIG ISO_DEF it documentazione/modifiche_it
python strumenti/analisi/documenta_pack.py ISO_ORIG it documentazione/modifiche_it
python strumenti/analisi/confronti_testi.py it
python strumenti/analisi/scrivi_documento_modifiche.py it
```
Input esterni da avere (controlla che esistano): ISO originale, USRDIR estratta (`strumenti/analisi/estrai_usrdir.py`), pack USA di MikeyMK `ULUS10136` (in `F:\Progetti\Mods\_download_pack_usa\`, fuori dal progetto).

# F. LIMITI E PUNTI APERTI

- Nomi ufficiali delle carte: da decidere con l'utente. "Ragazza Mago Nero" vs "Maga Nera".
- Le note a mano sulla rilettura delle carte prima di ~riga 1830 sono andate perse; per quel tratto c'e' anche una scansione automatica (refusi, spazi, apostrofi).
- `textures.zip` Android da rigenerare con le correzioni; carte del pack installato da riavviare in PPSSPP (cache).
- Il nome del parlante nella casella del dialogo non e' modificabile (EBOOT cifrato).
