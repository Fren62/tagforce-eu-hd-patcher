# MODIFICHE PER LA VERSIONE POMODORO MISTICO IN SPAGNOLO

Documento **completo** di tutto cio' che la "Versione Pomodoro Mistico" cambia per il spagnolo: (A) le modifiche **dirette alla ISO**, (B) il **texture pack** (com'e' fatto, cosa contiene, come si compone), (C) le scelte editoriali, (D) cosa e' verificato in gioco e cosa no, (E) come rigenerare tutto.

**Questo file e' generato** da `tools/analysis/write_changes_document.py es` a partire dai dati reali: confronto byte per byte tra la ISO originale `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` e la ISO corretta `..._definitiva.iso` (`document_changes.py`) e scansione del pack (`document_pack.py`). Gli elenchi riga per riga stanno in `docs/changes_es/*.csv` (separatore `;`, UTF-8 con BOM, a capo come `⏎`): sono la **lista esatta** di ogni cambiamento. Rigenera tutto dopo ogni modifica.

Per il metodo generale e per le altre lingue: `docs/NEW_LANGUAGE_GUIDE.md`; dettagli tecnici degli script: `TUTORIAL.md`; decisioni: `docs/EDITORIAL_CHOICES.md`; texture neutre/specifiche: `docs/TEXTURE_INVENTORY.md`.

## Indice
- A. Modifiche alla ISO: A1 panoramica · A2 carte · A3 dialoghi · A4 frasi dei duelli · A5 stringhe dell'interfaccia · A6 etichetta Magia/Trappola · A7 file toccati e dettagli tecnici · A8 cosa non si puo' cambiare
- B. Texture pack: B1 provenienza e struttura · B2 immagini delle carte · B3 interfaccia HD (`ui_es`) · B4 foglio numeri (`card_icon03`) · B5 targa del titolo · B6 textures.ini e composizione · B7 installazione
- C. Scelte editoriali · D. Verifica in gioco · E. Come rigenerare · F. Limiti e punti aperti

---

# A. MODIFICHE ALLA ISO

## A1. Panoramica

La ISO originale **non viene mai modificata**. `tools/corrections/apply_to_iso.py ISO_ORIG ISO_OUT [lingue]` ne crea una copia in cui alcuni archivi `.ehp` sono riscritti. Se un archivio cresce (testo piu' lungo) viene **rimesso in fondo alla ISO** in un nuovo settore e il suo voce nella directory ISO9660 viene riassegnata (`pycdlib`); la ISO `_definitiva` pesa per questo ~909 MB (l'originale ~761 MB). **Lanciarlo sempre senza elenco di lingue (o con tutte)**: con una lingua sola sovrascrive le altre.

| Cosa | Quantita' (derivata dal confronto ISO) | Dove sta il dato | File CSV |
|---|---|---|---|
| Carte con testo cambiato (nome e/o descrizione) | 624 carte (720 campi) | `tools/data/card_corrections_es.json` da `correzioni/rules_es.py` | cards.csv |
| Righe di dialogo della storia | 601 righe | `tools/data/dialogue_touchups_es.json` (+ base) | dialogues.csv |
| Frasi dei duellanti nei duelli | 55 frasi uniche (75 voci in tutti gli archivi) | `tools/data/duel_line_corrections_es.json` | duel_lines.csv |
| Stringhe dell'interfaccia (aiuti, schede, record, tutorial, menu...) | 329 stringhe uniche (1169 voci, 81 archivi) | `correzioni/string_rules_es.py` + `dati/ui_texts.json` | ui_strings.csv |
| Immagini sostituite dentro la ISO | 6 (etichetta [CARTA MAGIA/TRAPPOLA] della carta grande) | `apply_to_iso.py` (copia `card_spell_trap.gim` della lingua) | iso_images.csv |
| File della ISO toccati (archivi `.ehp`) | 179 | - | touched_files.csv |
| Altre differenze tecniche (offset ricalcolati) | 254 | - | other.csv |

## A2. Testi delle carte

Archivio: `PSP_GAME/USRDIR/duelsys/cardinfo_fra.ehp` (tabelle `CARD_Name_*`, `CARD_Desc_*`, `CARD_Indx_*`). **624 carte** hanno nome e/o descrizione modificati. Si correggono **solo errori oggettivi** (refusi, accenti, apostrofi, spazi, maiuscole incoerenti, concordanze, plurali fissi, residui di altre lingue); nomi ufficiali e terminologia del gioco non si toccano.

Come: ogni carta e' stata letta (it: 2.479 testi, uno per uno; fr: audit contro database ufficiale + lettura). Regole in `tools/corrections/rules_es.py`: **441 regole globali** (regex applicate a nomi e descrizioni di tutte le carte) e **201 correzioni per carta** (`PER_CARTA`: id, campo, vecchio, nuovo, motivo; il vecchio testo deve esistere esattamente). `generate_card_corrections.py es CARDINFO` (scrive `card_corrections_{L}.json` partendo dai testi originali) produce il json; `apply_to_iso` lo scrive nella ISO; le immagini HD delle carte toccate si rigenerano (sezione B2).

### Regole globali (tutte)
| modello (regex) | sostituzione | motivo |
|---|---|---|
| \bañadela\b | añádela | imperativo con pronome: manca l'accento |
| \bAñadela\b | Añádela | imperativo con pronome: manca l'accento |
| \bañadelas\b | añádelas | imperativo con pronome: manca l'accento |
| \bAñadelas\b | Añádelas | imperativo con pronome: manca l'accento |
| \bañadelo\b | añádelo | imperativo con pronome: manca l'accento |
| \bAñadelo\b | Añádelo | imperativo con pronome: manca l'accento |
| \bañadelos\b | añádelos | imperativo con pronome: manca l'accento |
| \bAñadelos\b | Añádelos | imperativo con pronome: manca l'accento |
| \bbarajalo\b | barájalo | imperativo con pronome: manca l'accento |
| \bBarajalo\b | Barájalo | imperativo con pronome: manca l'accento |
| \bbarajalos\b | barájalos | imperativo con pronome: manca l'accento |
| \bBarajalos\b | Barájalos | imperativo con pronome: manca l'accento |
| \bcambialo\b | cámbialo | imperativo con pronome: manca l'accento |
| \bCambialo\b | Cámbialo | imperativo con pronome: manca l'accento |
| \bcolocalas\b | colócalas | imperativo con pronome: manca l'accento |
| \bColocalas\b | Colócalas | imperativo con pronome: manca l'accento |
| \bdesignalo\b | desígnalo | imperativo con pronome: manca l'accento |
| \bDesignalo\b | Desígnalo | imperativo con pronome: manca l'accento |
| \bdestruyelo\b | destrúyelo | imperativo con pronome: manca l'accento |
| \bDestruyelo\b | Destrúyelo | imperativo con pronome: manca l'accento |
| \bdevuelvela\b | devuélvela | imperativo con pronome: manca l'accento |
| \bDevuelvela\b | Devuélvela | imperativo con pronome: manca l'accento |
| \bdevuelvelas\b | devuélvelas | imperativo con pronome: manca l'accento |
| \bDevuelvelas\b | Devuélvelas | imperativo con pronome: manca l'accento |
| \bdevuelvelos\b | devuélvelos | imperativo con pronome: manca l'accento |
| \bDevuelvelos\b | Devuélvelos | imperativo con pronome: manca l'accento |
| \bequipala\b | equípala | imperativo con pronome: manca l'accento |
| \bEquipala\b | Equípala | imperativo con pronome: manca l'accento |
| \bequipalo\b | equípalo | imperativo con pronome: manca l'accento |
| \bEquipalo\b | Equípalo | imperativo con pronome: manca l'accento |
| \binvocala\b | invócala | imperativo con pronome: manca l'accento |
| \bInvocala\b | Invócala | imperativo con pronome: manca l'accento |
| \binvocalo\b | invócalo | imperativo con pronome: manca l'accento |
| \bInvocalo\b | Invócalo | imperativo con pronome: manca l'accento |
| \bmandala\b | mándala | imperativo con pronome: manca l'accento |
| \bMandala\b | Mándala | imperativo con pronome: manca l'accento |
| \bmandalas\b | mándalas | imperativo con pronome: manca l'accento |
| \bMandalas\b | Mándalas | imperativo con pronome: manca l'accento |
| \bmandalo\b | mándalo | imperativo con pronome: manca l'accento |
| \bMandalo\b | Mándalo | imperativo con pronome: manca l'accento |
| \bordenalas\b | ordénalas | imperativo con pronome: manca l'accento |
| \bOrdenalas\b | Ordénalas | imperativo con pronome: manca l'accento |
| \bretiralas\b | retíralas | imperativo con pronome: manca l'accento |
| \bRetiralas\b | Retíralas | imperativo con pronome: manca l'accento |
| \bretiralo\b | retíralo | imperativo con pronome: manca l'accento |
| \bRetiralo\b | Retíralo | imperativo con pronome: manca l'accento |
| \bsaltate\b | sáltate | imperativo con pronome: manca l'accento |
| \bSaltate\b | Sáltate | imperativo con pronome: manca l'accento |
| \bSacrifício\b | Sacrificio | accento portoghese |
| \bdespues\b | después | accento |
| \bdespúes\b | después | refuso |
| \bDemónio\b\|\bdemónio\b | demonio | accento portoghese |
| \bpropietários\b | propietarios | accento portoghese |
| \bpropietário\b | propietario | accento portoghese |
| \bInvocacion\b | Invocación | accento |
| \bInvocacón\b | Invocación | refuso |
| \bPosicón\b | Posición | refuso |
| \bPinguino\b | Pingüino | dieresi |
| \bEspadachin\b | Espadachín | accento |
| \bEspiritu\b | Espíritu | accento |
| \bÓrden\b | Orden | accento errato |
| \bMágia\b | Magia | accento errato |
| \bCodícia\b | Codicia | accento portoghese |
| \bCañon Magico\b | Cañón Mágico | accenti |
| \bGuardian Grarl\b | Guardián Grarl | accento |
| \bAngel Guardián\b | Ángel Guardián | accento |
| \bTIRRA\b | TIERRA | refuso |
| \bnigún\b | ningún | refuso |
| \bNingun\b | Ningún | accento |
| \bningun\b | ningún | accento |
| \bDevuelte\b | Devuelve | refuso |
| \bInglige\b\|\binflinge\b | inflige | refuso |
| \bselccionado\b\|\bselecionado\b | seleccionado | refuso |
| \bamfíbio\b | anfibio | refuso |
| \bacrobaticamente\b | acrobáticamente | refuso |
| \baerorosol\b | aerosol | refuso |
| \bbiotecnologia\b | biotecnología | refuso |
| \bcaida\b | caída | refuso |
| \bcaidos\b | caídos | refuso |
| \bcuetro\b | cuatro | refuso |
| \bmáscars\b | máscaras | refuso |
| \benmaascarado\b | enmascarado | refuso |
| \bexluyendo\b | excluyendo | refuso |
| \bcombinandose\b | combinándose | refuso |
| \bseparandose\b | separándose | refuso |
| \bdefendiendose\b | defendiéndose | refuso |
| \bgovernaba\b | gobernaba | refuso |
| \bmaritima\b | marítima | refuso |
| \bporqie\b | porque | refuso |
| \bponne\b | pon | refuso |
| \bdia\b | día | refuso |
| \benergia\b | energía | refuso |
| \bhabia\b | había | refuso |
| \bhuída\b | huida | refuso |
| \bincreible\b | increíble | refuso |
| \bincreiblemente\b | increíblemente | refuso |
| \bgrácias\b | gracias | refuso |
| \bposeido\b | poseído | refuso |
| \bprofuncidades\b | profundidades | refuso |
| \bprópio\b | propio | refuso |
| \bprópios\b | propios | refuso |
| \btecnica\b | técnica | refuso |
| \btecnologia\b | tecnología | refuso |
| \btodavia\b | todavía | refuso |
| \bvctima\b | víctima | refuso |
| \bvictima\b | víctima | refuso |
| \bmonstuos\b | monstruos | refuso |
| \bmonsturo\b | monstruo | refuso |
| \bmounstro\b | monstruo | refuso |
| \bcañon\b | cañón | refuso |
| \bdestruyela\b | destrúyela | imperativo con pronome: manca l'accento |
| \bDestruyela\b | Destrúyela | imperativo con pronome: manca l'accento |
| \bfuerzas? de galera\b | fuerza de vendaval | traduzione errata (inglese: gale-force) |
| \bpuede ser invocado mediante\b | puede ser Invocado mediante | maiuscola incoerente (Invocado come nelle altre carte) |
| \bFé\b | Fe | accento errato |
| \bel DEF\b | la DEF | genere di DEF (la DEF nel resto del gioco) |
| \bEl DEF\b | La DEF | genere di DEF (la DEF nel resto del gioco) |
| \bla Deck\b | el Deck | genere di Deck (maschile come in 'tu Deck') |
| \bCerébro\b | Cerebro | accento errato |
| \bA menos que no pagues\b | A menos que pagues | doppia negazione errata (inglese: Unless you pay) |
| de esta carta se convierte en la misma cantidad | de esta carta se convierten en la misma cantidad | concordanza (ATK y DEF) |
| \bTu y tu adversario\b | Tú y tu adversario | accento |
| \bTanto tu como\b | Tanto tú como | accento |
| \bPoseida\b | Poseída | accento |
| \bCañon\b | Cañón | accento |
| \bPortacañon\b | Portacañón | accento |
| \bGémins\b | Géminis | refuso |
| \bAtaudes\b | Ataúdes | accento |
| \bEspia\b | Espía | accento |
| \bBuho\b | Búho | accento |
| \bInvocaciónes\b | Invocaciones | refuso |
| \bhasta el End Phase\b | hasta la End Phase | genere di End Phase (come nel resto del gioco) |
| Fusión\.\(no necesitas | Fusión. (no necesitas | spazio mancante |
| \bPeon Vil\b | Peón Vil | accento |
| \bTrio Ojama\b | Trío Ojama | accento |
| \bgana la Match\b | gana el Match | genere di Match |
| \bAmfibio\b | Anfibio | refuso |
| \bAmfibia\b | Anfibia | refuso |
| \bUna (alma\|hada)\b | Un \1 | 'un' davanti ad a- tonica (RAE) |
| \buna (alma\|hada)\b | un \1 | 'un' davanti ad a- tonica (RAE) |
| "Brazo\ de\ espada\ de\ Dragon" | "Brazo de Espada de Dragón" | quoted card name: official name |
| "Brazo\ de\ espada\ de\ Dragón" | "Brazo de Espada de Dragón" | quoted card name: official name |
| "Diablillo\ de\ cuerno" | "Diablillo de Cuerno" | quoted card name: official name |
| "El\ pelo\ de\ serpiente" | "El Pelo de Serpiente" | quoted card name: official name |
| "Insecto\ grande" | "Insecto Grande" | quoted card name: official name |
| "Planta\ devorador\ de\ carne\ humana" | "Planta Come-Hombres" | quoted card name: official name |
| "Incursor\ del\ hacha" | "Incursor del Hacha" | quoted card name: official name |
| "Quimera\ oscura" | "Quimera Oscura" | quoted card name: official name |
| "Guardián\ del\ metal" | "Guardián de Metal" | quoted card name: official name |
| "Guerrero\ de\ lucha" | "Guerrero de Batalla" | quoted card name: official name |
| "Alas\ de\ la\ llama\ perversa" | "Alas de la Llama Perversa" | quoted card name: official name |
| "Espejo\ de\ trabajo\ \-\ Cambiar" | "Espejo de Trabajo - Cambiar" | quoted card name: official name |
| "Cortina\ de\ los\ ones\ oscuros" | "Cortina de los Oscuros" | quoted card name: official name |
| "Tomozaurus" | "Tomozaurio" | quoted card name: official name |
| "Héroe\ de\ oriente" | "Héroe del Este" | quoted card name: official name |
| "Eso\ que\ se\ alimenta\ de\ la\ vida" | "Eso que se Alimenta de la Vida" | quoted card name: official name |
| "Kamionwizard" | "Kamionmago" | quoted card name: official name |
| "Escorpión\ de\ pesadilla" | "Escorpión de Pesadilla" | quoted card name: official name |
| "Partidario\ en\ las\ sombras" | "Partidario en las Sombras" | quoted card name: official name |
| "Herramienta\ antigua" | "Herramienta Antigua" | quoted card name: official name |
| "Ave\ de\ fe" | "Ave de Fe" | quoted card name: official name |
| "La\ mano\ de\ adicto" | "Mano del Demonio" | quoted card name: official name |
| "Zombi\ de\ plata\ de\ ojos\ azules" | "Zombi de Plata Ojizarco" | quoted card name: official name |
| "Necrolancer\ el\ Señor\ del\ Tiempo" | "Necrolancer el Tiempo-Señor" | quoted card name: official name |
| "El\ ladrón\ de\ fantasma\ encantador" | "El Ladrón Fantasma Encantador" | quoted card name: official name |
| "La\ sombra\ que\ controla\ la\ oscuridad" | "La Sombra que Controla la Oscuridad" | quoted card name: official name |
| "La\ sombra\ que\ controla\ el\ oscuridad" | "La Sombra que Controla la Oscuridad" | quoted card name: official name |
| "Segadora\ de\ fuego" | "Segadora de Fuego" | quoted card name: official name |
| "Pote\ antiguo" | "Tarro Antiguo" | quoted card name: official name |
| "Preso\ oscuro" | "Preso Oscuro" | quoted card name: official name |
| "Macis\ de\ tecla" | "Llave de la Maza" | quoted card name: official name |
| "Zombi\ de\ topo\ de\ Mech" | "Zombi Topo Mecánico" | quoted card name: official name |
| "Amante\ feliz" | "Amante Feliz" | quoted card name: official name |
| "Fantasma\ de\ fantasma" | "Espectro Fantasma" | quoted card name: official name |
| "Dragón\ B\.\ Cráneo" | "Dragón de Cráneo Negro" | quoted card name: official name |
| "Acosador\ de\ cráneo" | "Acechador del Cráneo" | quoted card name: official name |
| "Reloj\ de\ arena\ de\ la\ vida" | "Reloj de Arena de la Vida" | quoted card name: official name |
| "Vela\ del\ destino" | "Vela del Destino" | quoted card name: official name |
| "Fairywitch" | "Hadabruja" | quoted card name: official name |
| "Stone\ Armadiller" | "Armadiller de Piedra" | quoted card name: official name |
| "Hechicero\ antiguo" | "Hechicero Antiguo" | quoted card name: official name |
| "Rey\ Niebla" | "Rey Nebuloso" | quoted card name: official name |
| "Légamo\ de\ Cambiar" | "Limo de Cambio" | quoted card name: official name |
| "Armadura\ de\ insecto\ con\ cañón\ de\ rayo\ láser" | "Armadura Insecto con Cañón Láser" | quoted card name: official name |
| "Cyber\ revestimiento" | "Ciber Escudo" | quoted card name: official name |
| "Ojo\ de\ Megasonic" | "Ojo Megasónico" | quoted card name: official name |
| "Guerra\ \-\ león\ excelente" | "Súper León de Guerra" | quoted card name: official name |
| "Zombis\ de\ tres\ patas" | "Zombis de Tres Piernas" | quoted card name: official name |
| "Pingüino\ volando" | "Pingüino Volador" | quoted card name: official name |
| "Revestimiento\ de\ milenio" | "Escudo Milenario" | quoted card name: official name |
| "El\ obsequio\ de\ hada" | "Regalo del Hada" | quoted card name: official name |
| "El\ espejo\ de\ adicto" | "Espejo Demoníaco" | quoted card name: official name |
| "Gusano\ de\ calabozo" | "Gusano del Calabozo" | quoted card name: official name |
| "Monstruo\ más\ dócil" | "Domador de Monstruos" | quoted card name: official name |
| "Dragón\ Definitivo\ de\ Ojos\ Azules" | "Dragón de Ojos Azules Definitivo" | quoted card name: official name |
| "Dragón\ de\ loro" | "Dragón Loro" | quoted card name: official name |
| "Conejo\ oscuro" | "Conejo Oscuro" | quoted card name: official name |
| "Dragón\ mascota\ de\ Arpía" | "Dragón Mascota de Arpía" | quoted card name: official name |
| "Máquina\ de\ péndulo" | "Máquina del Péndulo" | quoted card name: official name |
| "Comilón\ de\ zona" | "Comilón de Zona" | quoted card name: official name |
| "Swordsman\ de\ una\ nación\ extranjera" | "Espadachín de una Tierra Lejana" | quoted card name: official name |
| "Slasher\ de\ sable" | "Asesino de la Espada" | quoted card name: official name |
| "Mech\ \-\ soldado\ gigante" | "Mech - Soldado Gigante" | quoted card name: official name |
| "Spider\ mecánico" | "Araña Karakuri" | quoted card name: official name |
| "Apedree\ D\." | "Dragón de Piedra" | quoted card name: official name |
| "Diosa\ del\ capricho" | "Diosa del Capricho" | quoted card name: official name |
| "Tutor\ del\ mar" | "Centinela del Mar" | quoted card name: official name |
| "Red\ Seasnake\ del\ gigante" | "Serpiente Marina Roja Gigante" | quoted card name: official name |
| "Roca\ de\ barril" | "Roca de Cañón" | quoted card name: official name |
| "Caracol\ de\ perno" | "Caracol del Rayo" | quoted card name: official name |
| "Pingüino\ de\ perno" | "Pingüino de Perno" | quoted card name: official name |
| "Enrojezca\ Sunbird" | "Pájaro Sol Carmesí" | quoted card name: official name |
| "Comilón\ de\ aire" | "Comeaire" | quoted card name: official name |
| "Kamen\ de\ mar" | "Kamen de Mar" | quoted card name: official name |
| "Lirio\ de\ barril" | "Lirio Cañón" | quoted card name: official name |
| "Ball\ de\ aguja" | "Bola de Agujas" | quoted card name: official name |
| "Dogra\ de\ vendaval" | "Gale Dogra" | quoted card name: official name |
| "Peces\ disparatados" | "Peces Disparatados" | quoted card name: official name |
| "Bracchio\ \-\ raidus" | "Bracchio-raidus" | quoted card name: official name |
| "Scizzar\ valiente" | "Scizzar Valiente" | quoted card name: official name |
| "Ave\ de\ tortuga" | "Pájaro Tortuga" | quoted card name: official name |
| "Ave\ monstruosa" | "Ave Monstruosa" | quoted card name: official name |
| "Chico\ Estrela" | "Chico Estrella" | quoted card name: official name |
| "Cazador\ de\ cuello" | "Cazador de Cuello" | quoted card name: official name |
| "Arena\ esotérica" | "Arena Mística" | quoted card name: official name |
| "Frog\ el\ Jam" | "Sapo Viscoso" | quoted card name: official name |
| "Fenomenal\ mamut\ de\ Goldfine" | "Gran Mamut de Goldfine" | quoted card name: official name |
| "Tiburón\ negro\ devorador\ de\ carne\ humana" | "Tiburón Negro Devorador de Carne Humana" | quoted card name: official name |
| "Anthrosaurus" | "Anthrosaurio" | quoted card name: official name |
| "Trakadon" | "Trakodon" | quoted card name: official name |
| "Little\ D" | "D Pequeño" | quoted card name: official name |
| "Macis\ de\ tecla\ \#2" | "Llave de la Maza #2" | quoted card name: official name |
| "Dragón\ de\ hada" | "Dragón Hada" | quoted card name: official name |
| "Reloj\ de\ arena\ del\ valor" | "Reloj de Arena del Coraje" | quoted card name: official name |
| "La\ cosa\ que\ se\ esconde\ en\ el\ barro" | "La Cosa que se Esconde en el Barro" | quoted card name: official name |
| "Amazon\ de\ los\ mares" | "Amazona de los Mares" | quoted card name: official name |
| "Rata\ blindada" | "Rata Blindada" | quoted card name: official name |
| "Lagartija\ de\ noche" | "Lagarto Nocturno" | quoted card name: official name |
| "Bugroth\ anfibio" | "Bugroth Anfibio" | quoted card name: official name |
| "Sustancia\ pegajosa\ horripilante" | "Sustancia Pegajosa Horripilante" | quoted card name: official name |
| "Kunai\ con\ la\ cadena" | "Kunai con Cadena" | quoted card name: official name |
| "Aplaste\ la\ tarjeta" | "Virus Aplastacartas" | quoted card name: official name |
| "Erradicar\ aerosol" | "Aerosol Erradicador" | quoted card name: official name |
| "Erradicar\ aerorosol" | "Aerosol Erradicador" | quoted card name: official name |
| "Bosquejo\ eterno" | "Sequía Eterna" | quoted card name: official name |
| "Castillo\ brillante" | "Palacio Brillante" | quoted card name: official name |
| "Ritual\ de\ guerra\ \-\ león" | "Ritual del León de Guerra" | quoted card name: official name |
| "Ritual\ de\ espejo\ detestable" | "Ritual del Espejo Bestial" | quoted card name: official name |
| "Agujero\-Trampa\ De\ Ácido" | "Agujero Trampa de Ácido" | quoted card name: official name |
| "Ruina\ extendida" | "Ruina Generalizada" | quoted card name: official name |
| "Duende\ travieso\ admirador" | "Abanico Goblin" | quoted card name: official name |
| "Reina\ de\ Cosmo" | "Reina Cosmo" | quoted card name: official name |
| "Dragón\ de\ meteorito" | "Dragón Meteoro" | quoted card name: official name |
| "Dragón\ de\ B\ de\ meteorito" | "Dragón Meteoro Negro" | quoted card name: official name |
| "Firewing\ Pegasus" | "Pegaso Aladefuego" | quoted card name: official name |
| "Ritual\ mágico\ oscuro" | "Ritual de Magia Negra" | quoted card name: official name |
| "Mago\ del\ Caos\ Oscuro" | "Mago del Caos Negro" | quoted card name: official name |
| "Illusionist\ oscuro\ \-\ ojos" | "Ilusionista de Ojos Oscuros" | quoted card name: official name |
| "Círculo\ de\ explosión" | "Esfera Explosiva" | quoted card name: official name |
| "Alpha\ el\ Guerrero\ de\ Imán" | "Alfa el Guerrero Magnético" | quoted card name: official name |
| "Dragón\ de\ metal\ negro\ rojo\ \-\ ojos" | "Dragón de Metal Negro Ojos Rojos" | quoted card name: official name |
| "Aníbal\ el\ Nigromante" | "Hannibal Necromante" | quoted card name: official name |
| "Quimera\ la\ bestia\ mítica\ volando" | "Quimera, la Bestia Voladora Mítica" | quoted card name: official name |
| "Cyber\ Predador" | "Ciber Predador" | quoted card name: official name |
| "Beta\ el\ Guerrero\ de\ Imán" | "Beta el Guerrero Magnético" | quoted card name: official name |
| "Gran\ Escudo\ Guardna" | "Gran Escudo Gardna" | quoted card name: official name |
| "La\ espada\ de\ piel\ de\ caimán" | "Aligátor de la Espada" | quoted card name: official name |
| "Caimán\ cyber\-\ tecnología" | "Aligátor Cibertech" | quoted card name: official name |
| "Gamma\ el\ Guerrero\ de\ Imán" | "Gamma el Guerrero Magnético" | quoted card name: official name |
| "Máquina\ del\ tiempo" | "Máquina del Tiempo" | quoted card name: official name |
| "Multiplique" | "Multiplicar" | quoted card name: official name |
| "Espada\ de\ Fuerza\ Luminosa" | "Espada de la Fuerza de Luz" | quoted card name: official name |
| "Dados\ garbosos" | "Dado Grácil" | quoted card name: official name |
| "Dados\ de\ cráneo" | "Dado de Cráneo" | quoted card name: official name |
| "Cortina\ de\ Magic\ oscura" | "Cortina de Magia Oscura" | quoted card name: official name |
| "Llamada\ de\ la\ tumba" | "Llamada de la Tumba" | quoted card name: official name |
| "Raigeki\ de\ inconformista" | "Anti Raigeki" | quoted card name: official name |
| "Llamada\ de\ la\ oscuridad" | "Llamada de Oscuridad" | quoted card name: official name |
| "Llamada\ del\ oscuridad" | "Llamada de Oscuridad" | quoted card name: official name |
| "Chispa\ Luminosa" | "Chispa Reluciente" | quoted card name: official name |
| "Hermano\ de\ la\ Arpía" | "Explorador del Cielo" | quoted card name: official name |
| "Valkyrion\ el\ Guerrero\ de\ Imán" | "Valkyrion el Guerrero Magno" | quoted card name: official name |
| "El\ dragón\ de\ espada\ de\ piel\ de\ caimán" | "Dragón del Aligátor de la Espada" | quoted card name: official name |
| "Soldado\ Cinético" | "Soldado Cifrado" | quoted card name: official name |
| "Devorador\ de\ Almas" | "Comealma" | quoted card name: official name |
| "Gusano\ Bolsón\ Electromagnético" | "Polilla Electromagnética" | quoted card name: official name |
| "Robodama" | "Robolady" | quoted card name: official name |
| "Soldado\ de\ los\ Artilugios" | "Soldado Mecanismo" | quoted card name: official name |
| "Ficha\ de\ Monstruo\ Insecto" | "Ficha Monstruo Insecto" | quoted card name: official name |
| "Cartas\ infinitas" | "Cartas Infinitas" | quoted card name: official name |
| "Bebé\ de\ la\ Luna\ Roja" | "Bebé Vampiro" | quoted card name: official name |
| "Puerta\ de\ la\ Ilusión" | "Puerta de las Ilusiones" | quoted card name: official name |
| "Tetera\ Alquimia\ \-\ Destilación\ de\ Caos" | "Destilación del Caos" | quoted card name: official name |
| "Piedra\ del\ Filósofo\ \-\ Sabatier" | "Sabatiel - La Piedra Filosofal" | quoted card name: official name |
| "Amanecer\ en\ la\ Roca\ de\ Ayer" | "Amanecer en Ayers Rock" | quoted card name: official name |
| "Amazoness\ Arquera" | "Arquera Amazoness" | quoted card name: official name |
| "Marie\ la\ Caida" | "Señoroscura Marie" | quoted card name: official name |
| "Mamotreto\ de\ Magia\ Negra\ de\ Maga\ Oscura" | "Fórmula Mágica" | quoted card name: official name |
| "Catedral\ de\ Nobles" | "Templo de los Reyes" | quoted card name: official name |
| "Encarnación\ de\ Apofis" | "Encarnación de Apophis" | quoted card name: official name |
| "Entierro\ Tonto" | "Entierro Insensato" | quoted card name: official name |
| "Makiu" | "Makiu, la Niebla Mística" | quoted card name: official name |
| "Serket\ la\ Bestia\ Mística" | "Bestia Mística de Serket" | quoted card name: official name |
| "Caballero\ del\ Viento\ Oscuro\ de\ Gaia" | "Gaia el Caballero Feroz Rápido" | quoted card name: official name |
| "Guardián\ Celta\ Convertido" | "Guardia Celta Convertido" | quoted card name: official name |
| "Garuda\ el\ Espíritu\ del\ viento" | "Garuda el Espíritu del Viento" | quoted card name: official name |
| "Poder\ Almacenado" | "Poder Acumulado" | quoted card name: official name |
| "Muñeca\ Cebo" | "Muñeca Señuelo" | quoted card name: official name |
| "Flecha\ Encantada" | "Flecha Rompedora de Hechizos" | quoted card name: official name |
| "Maestro\ de\ la\ Cadena\ Amazoness" | "Maestra de la Cadena Amazoness" | quoted card name: official name |
| "Vider\ Des" | "Viser Des" | quoted card name: official name |
| "Caballero\ Cráneo\ \#2" | "Caballero del Cráneo #2" | quoted card name: official name |
| "Máquina\ Absorbevida" | "Máquina Absorbe Vidas" | quoted card name: official name |
| "Unidad\ Lanzapiedras" | "Unidad Throwstone" | quoted card name: official name |
| "Un\ Plan\ con\ Estratagema" | "Un plan de finta" | quoted card name: official name |
| "El\ Dragón\ que\ mora\ en\ la\ Cueva" | "El Dragón que Mora en la Cueva" | quoted card name: official name |
| "Super\ Rejuvenecimiento" | "Súper Rejuvenecimiento" | quoted card name: official name |
| "Arma\ Biológica\ De\-Spell" | "Cañón de Virus" | quoted card name: official name |
| "Demonio\ Silente" | "Perdición Silenciosa" | quoted card name: official name |
| "Ficha\ de\ Kuriboh" | "Ficha Kuriboh" | quoted card name: official name |
| "Super\ Robodama" | "Super Robolady" | quoted card name: official name |
| "Escorpión\ de\ 8\ Garras" | "Escorpión de 8 Pinzas" | quoted card name: official name |
| "Ficha\ Malvada" | "Ficha Vil" | quoted card name: official name |
| "Designador\ Negro" | "Designador Oscuro" | quoted card name: official name |
| "Amo\ de\ la\ Marioneta" | "Amo de Títeres" | quoted card name: official name |
| "Hechizo\ de\ Dolor" | "Conjuro de Dolor" | quoted card name: official name |
| "Soldado\ Oculto" | "Soldados Escondidos" | quoted card name: official name |
| "Calamidad\ del\ Malvado" | "Catástrofe Malevolente" | quoted card name: official name |
| "Alivio\ de\ Monstruo" | "Relevar al Monstruo" | quoted card name: official name |
| "Amo\ del\ Dragón\ Soldado" | "Caballero Amo del Dragón" | quoted card name: official name |
| "F\.G\.D\." | "Dragón de Cinco Cabezas" | quoted card name: official name |
| "Soga\ del\ Espíritu" | "Cuerda del Alma" | quoted card name: official name |
| "Zombi\ Duende" | "Goblin Zombi" | quoted card name: official name |
| "Vampiro\ Orchis" | "Orchis Vampírico" | quoted card name: official name |
| "Ordenando\ Libros\ de\ Magia" | "Ordenando el Libro de Magia" | quoted card name: official name |
| "Ordenando\ Libros\ de\ Mágia" | "Ordenando el Libro de Magia" | quoted card name: official name |
| "Libro\ de\ Conjuros\ Oculto" | "Libro de Magia Oculto" | quoted card name: official name |
| "Desarmar" | "Desarmamiento" | quoted card name: official name |
| "Cieno\ con\ Reflejos\ Metálicos" | "Limo Reflectametal" | quoted card name: official name |
| "Excavación\ de\ Piedras\ Mágicas" | "Excavación de la Piedra Mágica" | quoted card name: official name |
| "Ficha\ Demonio\ Metal" | "Ficha Demonio Metálico" | quoted card name: official name |
| "Ladrón\ de\ Almas" | "Toma Almas" | quoted card name: official name |
| "Piedra\ del\ Sabio" | "La Piedra del Sabio" | quoted card name: official name |
| "Archidemonio\ Álfil\ Oscuro" | "Archidemonio Alfil Oscuro" | quoted card name: official name |
| "Semilla\ Primigénia" | "Semilla Primigenia" | quoted card name: official name |
| "D\.\ Victoria" | "Dragón de la Victoria" | quoted card name: official name |
| "Zoma\ Calavera" | "Zoma de Calavera" | quoted card name: official name |
| "Seis\ Máximo" | "Seis como Máximo" | quoted card name: official name |
| "Máquina\ Peligrosa\ TIPO\-6" | "Máquina Peligrosa Tipo 6" | quoted card name: official name |
| "Ejército\ de\ Pira" | "Ejército de Pirañas" | quoted card name: official name |
| "Choque\ de\ Escudo" | "Pulverizar el Escudo" | quoted card name: official name |
| "Demonio\ Geminis" | "Diablillos Géminis" | quoted card name: official name |
| "Demonio\ Géminis" | "Diablillos Géminis" | quoted card name: official name |
| "Regreso\ del\ Zombi" | "Zombi Retornado" | quoted card name: official name |
| "Cadáver\ de\ Yata\-Garasu" | "Legado de Yata-Garatsu" | quoted card name: official name |
| "Invitación\ de\ Espíritu\ Terrestre" | "Invitación de los Espíritus Terrestres" | quoted card name: official name |
| "Lacooda\ de\ 3\ jorobas" | "Lacooda de 3 Jorobas" | quoted card name: official name |
| "Momia\ Regenerativa" | "Momia Regeneradora" | quoted card name: official name |
| "Gandra\ D\.\ Triturador" | "Gandora el Dragón de la Destrucción" | quoted card name: official name |
| "Dragón\ de\ Metal\ Raro" | "Dragón de Metales Preciosos" | quoted card name: official name |
| "Cría\ B\.\ de\ Ojos\ Rojos" | "Cría de Dragón Negro" | quoted card name: official name |
| "El\ Tramposo" | "El Difícil" | quoted card name: official name |
| "Magia\ de\ Tramposo\ 4" | "Conjuro Difícil 4" | quoted card name: official name |
| "Ficha\ Tramposas" | "Ficha Difícil" | quoted card name: official name |
| "Ficha\ Tramposa" | "Ficha Difícil" | quoted card name: official name |
| "Cruz\ del\ Mago" | "Magos, Uníos" | quoted card name: official name |
| "Gran\ Núcleo" | "B.E.S. Núcleo Grande" | quoted card name: official name |
| "Sello\ del\ Dueño" | "Sello del Propietario" | quoted card name: official name |
| "Maldición\ de\ Vampiro" | "Maldición del Vampiro" | quoted card name: official name |
| "Ataque\ Unión" | "Ataque Unido" | quoted card name: official name |
| "Sanguijuela" | "Chupasangre" | quoted card name: official name |
| "Ojo\ Penetrante" | "Ojo Agobiante" | quoted card name: official name |
| "Genesis\ de\ Vampiro" | "Génesis de Vampiro" | quoted card name: official name |
| "Soldados\ Maquinistas" | "Maquinaria Soldado" | quoted card name: official name |
| "Defensor\ Maquinista" | "Maquinaria Defensora" | quoted card name: official name |
| "Francotirador\ Maquinista" | "Maquinaria Francotiradora" | quoted card name: official name |
| "Fuerza\ Maquinista" | "Fuerza de la Maquinaria" | quoted card name: official name |
| "Héroe\ Elemental\ Avian" | "HÉROE Elemental Avian" | quoted card name: official name |
| "Héroe\ Elemental\ Burstinatrix" | "HÉROE Elemental Burstinatrix" | quoted card name: official name |
| "Héroe\ Elemental\ Clayman" | "HÉROE Elemental Clayman" | quoted card name: official name |
| "Héroe\ Elemental\ Sparkman" | "HÉROE Elemental Sparkman" | quoted card name: official name |
| "Héroe\ Elemental\ de\ la\ Llama\ Wingman" | "HÉROE Elemental de la Llama Wingman" | quoted card name: official name |
| "Héroe\ Elemental\ del\ Trueno\ Gigante" | "HÉROE Elemental del Trueno Gigante" | quoted card name: official name |
| "Caballero\ Sagrado\ Ishzark" | "Isaac, Caballero Divino" | quoted card name: official name |
| "Héroe\ Elemental\ Bubbleman" | "HÉROE Elemental Bubbleman" | quoted card name: official name |
| "Ciber\ Dragón\ de\ Dos\ Cabezas" | "Dragón Ciber de Dos Cabezas" | quoted card name: official name |
| "Ciber\ Dragón\ Final" | "Dragón Ciber Final" | quoted card name: official name |
| "Invocación\ de\ Sacerdote" | "Monje Invocador" | quoted card name: official name |
| "Ruta\ Pavorosa\ Oscura" | "La Raizmuerta Malvada" | quoted card name: official name |
| "Vandalgyon\ Gobernante\ Oscuro" | "Van'Dalgyon el Señor de los Dragones Oscuros" | quoted card name: official name |
| "Fuerza\ de\ Ataque\ de\ Elite\ Goblin" | "Fuerza de Ataque de Élite Goblin" | quoted card name: official name |
| "Des\ Rana" | "Des RANA" | quoted card name: official name |
| "Rana\ del\ Robo\ Venenoso" | "RANA del Robo Tóxica" | quoted card name: official name |
| "Caballero\ Bromista\ Alkana" | "Bufón Escolta Arcano" | quoted card name: official name |
| "Asesino\ de\ la\ Guadaña\ Espantosa" | "Cosechador de la Guadaña del Terror" | quoted card name: official name |
| "Héroe\ Elemental\ Shining\ Flare\ Wingman" | "HÉROE Elemental Shining Flare Wingman" | quoted card name: official name |
| "Héroe\ Elemental\ Bladedge" | "HÉROE Elemental Bladedge" | quoted card name: official name |
| "Héroe\ Elemental\ Wildheart" | "HÉROE Elemental Wildheart" | quoted card name: official name |
| "Héroe\ Elemental\ Rampart\ Blaster" | "HÉROE Elemental Rampart Blaster" | quoted card name: official name |
| "Héroe\ Elemental\ Tempest" | "HÉROE Elemental Tempest" | quoted card name: official name |
| "Héroe\ Elemental\ Wiledge" | "HÉROE Elemental Wildedge" | quoted card name: official name |
| "Héroe\ Elemental\ Necroshade" | "HÉROE Elemental Necroshade" | quoted card name: official name |
| "Héroe\ Elemental\ Hombre\ Bola\ Loco" | "HÉROE Elemental Mudballman" | quoted card name: official name |
| "Héroe\ Elemental\ Steam\ Healer" | "HÉROE Elemental Steam Healer" | quoted card name: official name |
| "Dragonauta\ Rancer" | "Draconiano de la Lanza" | quoted card name: official name |
| "Cuerpo\ Neblinoso" | "Cuerpo de Niebla" | quoted card name: official name |
| "Dragonauta\ Hacha" | "Draconiano del Hacha" | quoted card name: official name |
| "D\.\ Cuernos\ Blancos" | "Dragón de Cuerno Blanco" | quoted card name: official name |
| "Héroe\ Elemental\ Neo\-Bubbleman" | "HÉROE Elemental Neo-Bubbleman" | quoted card name: official name |
| "Ciber\ Dragón\ Barrera" | "Dragón Ciber Barrera" | quoted card name: official name |
| "Ciber\ Dragón\ Láser" | "Dragón Ciber Láser" | quoted card name: official name |
| "Ficha\ de\ Mártires\ Fantasma" | "Ficha de Mártir Fantasmal" | quoted card name: official name |
| "Rana\ Arbórea" | "RANA Arbórea" | quoted card name: official name |
| "Rana\ Beelze" | "RANA Beelze" | quoted card name: official name |
| "Deceso,\ Rey\ del\ Apocalipsis" | "Demise, Rey del Armagedón" | quoted card name: official name |
| "Rana\ D\.3\.S\." | "RANA D.3.S." | quoted card name: official name |
| "Ficha\ de\ Peluche" | "Ficha Pelusa" | quoted card name: official name |
| "Héroe\ Elemental\ Erikshieler" | "HÉROE Elemental Electrum" | quoted card name: official name |
| "Héroe\ Elemental\ Wild\ Wingman" | "HÉROE Elemental Wild Wingman" | quoted card name: official name |
| "Héroe\ Elemental\ Necroid\ Shaman" | "HÉROE Elemental Necroid Shaman" | quoted card name: official name |
| "Helios\ Duo\ Megistus" | "Helios Dúo Megistus" | quoted card name: official name |
| "Héroe\ Elemental\ Neos" | "HÉROE Elemental Neos" | quoted card name: official name |
| "Diente\ de\ León\ Presumido" | "Diente de León" | quoted card name: official name |
| "Héroe\ Elemental\ Phoenix\ Enforcer" | "HÉROE Elemental Phoenix Enforcer" | quoted card name: official name |
| "Héroe\ Elemental\ Phoenix\ Enforcer\ Brillante" | "HÉROE Elemental Phoenix Enforcer Brillante" | quoted card name: official name |
| "Héroe\ Elemental\ Mariner" | "HÉROE Elemental Mariner" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Doom\ Lord" | "HÉROE del Destino - Doom Lord" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Captain\ Tenacious" | "HÉROE del Destino - Captain Tenacious" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Diamond\ Dude" | "HÉROE del Destino - Diamond Dude" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Dreadmaster" | "HÉROE del Destino - Dreadmaster" | quoted card name: official name |
| "Flash\ HERO!!" | "Flash Hero!!" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Blade\ Master" | "HÉROE del Destino - Blade Master" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Dasher" | "HÉROE del Destino - Dasher" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Double\ Dude" | "HÉROE del Destino - Double Dude" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Defender" | "HÉROE del Destino - Defender" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Fear\ Monger" | "HÉROE del Destino - Fear Monger" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Dogma" | "HÉROE del Destino - Dogma" | quoted card name: official name |
| "Héroe\ Elemental\ Dark\ Neos" | "HÉROE Elemental Dark Neos" | quoted card name: official name |
| "Héroe\ Elemental\ Aqua\ Neos" | "HÉROE Elemental Aqua Neos" | quoted card name: official name |
| "Héroe\ Elemental\ Flare\ Neos" | "HÉROE Elemental Flare Neos" | quoted card name: official name |
| "Bestia\ Fantasma\ Lagarto\ de\ Roca" | "Bestia Fantasma Rock-Lizard" | quoted card name: official name |

### Correzioni per carta (tutte)
| id | campo | vecchio | nuovo | motivo |
|---|---|---|---|---|
| 5666 | desc | se negare. | quedan anulados. | parola mutilata |
| 4017 | name | Dragon | Dragón | accento |
| 4089 | desc | monstrus | monstruos | refuso |
| 4657 | desc | monstro del adversario ataco | monstruo del adversario ataca | refusi |
| 4657 | desc | punots | puntos | refuso |
| 4761 | desc | monstruos mas | monstruos más | accento |
| 4808 | desc | Seleccióna | Selecciona | accento errato |
| 4892 | desc | són destruidas | son destruidas | accento errato |
| 4948 | desc | numero de cartas | número de cartas | accento |
| 4969 | desc | tengais | tengáis | accento |
| 4976 | desc | calculo | cálculo | accento |
| 5130 | desc | Cámbia | Cambia | accento errato |
| 5132 | desc | limite | límite | accento |
| 5221 | desc | justícia | justicia | accento portoghese |
| 5530 | desc | demas cartas | demás cartas | accento |
| 5522 | name | Falcos, o Sábio Alado | Falcos, el Sabio Alado | residuo di portoghese ("o Sábio") |
| 5760 | desc | dstino | destino | refuso |
| 5895 | desc | Envia | Envía | accento |
| 6160 | desc | turnsos | turnos | refuso |
| 6368 | desc | Destuye | Destruye | refuso |
| 6376 | desc | Envie "Umi" no seu Campo para o Cemitério para enviar para o Cemitério todos os cards na mão de ambos os jogadores e no Campo exceto este card. | Envía "Umi" de tu Campo al Cementerio para enviar al Cementerio todas las cartas de la mano de ambos jugadores y del Campo, excepto esta carta. | frase in portoghese: tradotta in spagnolo seguendo il testo inglese e la terminologia del gioco |
| 6410 | desc | hacersele | hacérsele | accento |
| 6410 | desc | con exito | con éxito | accento |
| 6410 | desc | ●Magica : | ●Mágica: | accento e spazio prima dei due punti |
| 6537 | desc | montruo | monstruo | refuso |
| 4070 | desc | Una rápido y poderoso | Un rápido y poderoso | concordanza |
| 4078 | desc | se aplica a | se aplican a | concordanza (ATK y DEF) |
| 4088 | desc | con una ataque | con un ataque | concordanza |
| 4138 | desc | una sepulcro | un sepulcro | concordanza |
| 4148 | desc | y la "Muro de Fuego" | y el "Muro de Fuego" | concordanza |
| 4154 | name | controla el oscuridad | controla la oscuridad | concordanza |
| 4181 | name | Cerébro | Cerebro | accento errato |
| 4192 | desc | que invocar refuerzos | que invoca refuerzos | refuso |
| 4203 | desc | armas semejante a | armas semejantes a | concordanza |
| 4261 | desc | esta escudada | está escudada | accento |
| 4261 | desc | a si misma | a sí misma | accento |
| 4267 | desc | Un perverso guerrero que hipnotiza | Un perverso espejo que hipnotiza | traduzione errata (inglese: mirror) |
| 4286 | desc | el rey esta ausente | el rey está ausente | accento |
| 4303 | desc | todos las señales | todas las señales | concordanza |
| 4398 | desc | desde la Deck al campo | desde el Deck al campo | genere di Deck (maschile come nelle altre carte) |
| 4434 | name | Fé | Fe | accento errato |
| 4484 | desc | Aumenta en 1000 puntos | aumenta en 1000 puntos | maiuscola errata |
| 4485 | desc | es devuelto a la parte | es devuelta a la parte | concordanza |
| 4519 | desc | esta armado | está armado | accento |
| 4521 | desc | Oriental qe lanza | Oriental que lanza | refuso |
| 4545 | desc | tiburón zombie | tiburón zombi | grafia coerente con Zombi del gioco |
| 4591 | desc | aún así | aun así | accento |
| 4622 | desc | el ATK y el DEF de este monstruo se reduce a la mitad | el ATK y la DEF de este monstruo se reducen a la mitad | concordanza |
| 4622 | desc | tanto el ATK como el DEF | tanto el ATK como la DEF | genere di DEF |
| 4637 | desc | la compresión | la comprensión | refuso |
| 4655 | desc | oidos | oídos | accento |
| 4660 | desc | equipado con esta tarjeta incrementa su ATK por 700 puntos | equipado con esta carta aumenta su ATK en 700 puntos | terminologia (tarjeta -> carta) e preposizione |
| 4678 | desc | en el Campo tu adversario | en el Campo de tu adversario | preposizione mancante |
| 4691 | desc | Posición de DEfensa | Posición de Defensa | maiuscola errata |
| 4693 | desc | Nivel 2 ó inferior | Nivel 2 o inferior | accento |
| 4737 | desc | de esta carta se convierte en la misma | de esta carta se convierten en la misma | concordanza |
| 4755 | desc | es Invocación (excluyendo | es Invocada (excluyendo | refuso |
| 4761 | desc | en el Campo que tu. | en el Campo que tú. | accento |
| 4786 | desc | Aún cuando | Aun cuando | accento |
| 4789 | desc | monstruos de tipo Demonio | monstruos de Tipo Demonio | maiuscola incoerente |
| 4795 | desc | es Invocación (incluyendo | es Invocada (incluyendo | refuso |
| 4805 | desc | cuantos "Fichas de Kuriboh" | cuantas "Fichas de Kuriboh" | concordanza |
| 4806 | desc | monstruo del tipo Máquina | monstruo de Tipo Máquina | maiuscola incoerente |
| 4810 | desc | hasta 2 de cartas Tipo Dragón | hasta 2 cartas de Tipo Dragón | grammatica |
| 4819 | desc | no son negadas por el efecto | no son negados por el efecto | concordanza |
| 4830 | desc | no puedes llamar a ningún monstruo | no puedes Invocar ningún monstruo | traduzione errata (inglese: summon) |
| 4835 | desc | tú eliges cual | tú eliges cuál | accento |
| 4859 | name | Llamada del oscuridad | Llamada de la oscuridad | concordanza |
| 4877 | name | Germenes | Gérmenes | accento |
| 4885 | desc | Si un monstruo de tu Campo sea enviado | Si un monstruo de tu Campo fue enviado | tempo verbale (inglese: was sent) |
| 4901 | desc | descarta 1 al azar carta | descarta 1 carta al azar | ordine delle parole |
| 4951 | desc | se convierte del Tipo que has declarado | se convierten en el Tipo que has declarado | concordanza |
| 4952 | desc | declarado no puede atacar | declarado no pueden atacar | concordanza |
| 4953 | desc | cuando hayan 5 o más | cuando haya 5 o más | concordanza (haber impersonale) |
| 4962 | desc | y Colocalas en el Campo | y colócalas en el Campo | maiuscola errata e accento |
| 4983 | desc | monstruo de tipo Dragón | monstruo de Tipo Dragón | maiuscola incoerente |
| 5024 | desc | el ATK y el DEF de todos tus monstruos tipo Planta boca arriba aumenta en | el ATK y la DEF de todos tus monstruos de Tipo Planta boca arriba aumentan en | concordanza e maiuscola |
| 5027 | desc | los Tipo-Máquina | los monstruos de Tipo Máquina | grafia coerente |
| 5034 | desc | tanto al ATK como al DEF se le añaden | tanto al ATK como a la DEF se les añaden | concordanza |
| 5086 | desc | han sido engaños | han sido engañados | refuso |
| 5110 | desc | Aumenta en ATK del monstruo | Aumenta el ATK del monstruo | refuso |
| 5122 | desc | esta boca arriba | está boca arriba | accento |
| 5177 | desc | Coloca una "Contador de Doncella" | Coloca un "Contador de Doncella" | concordanza |
| 5178 | desc | con una "Contador de Doncella" | con un "Contador de Doncella" | concordanza |
| 5178 | desc | que ocasiona Damage Step a los Life Points | que ocasiona daño de batalla a los Life Points | traduzione errata (inglese: Battle Damage) |
| 5190 | desc | cada monstruo tipo Bestia | cada monstruo de Tipo Bestia | maiuscola incoerente |
| 5197 | desc | que tu aumentes | que tú aumentes | accento |
| 5212 | desc | que tu controles | que tú controles | accento |
| 5219 | name | EL Secreto | El Secreto | maiuscola errata |
| 5221 | desc | El Espíritu maldito | El espíritu maldito | maiuscola errata |
| 5222 | desc | tu controlas el monstruo | tú controlas el monstruo | accento |
| 5226 | desc | acercarsele | acercársele | accento |
| 5237 | desc | Selecciona lo mismo "Cráneo Convocado" que cualquier monstruo | Selecciona "Cráneo Convocado" o cualquier monstruo | traduzione errata (inglese: either ... or) |
| 5246 | desc | no puede ser negado por ninguna carta | no pueden ser negados por ninguna carta | concordanza |
| 5290 | desc | todas las Carta Mágica boca arriba | todas las Cartas Mágicas boca arriba | concordanza |
| 5291 | desc | elegir una carta de monstruo de la Mano de tu oponente. Añade esa carta a tu Mano | elegir 1 Carta de Monstruo de la mano de tu oponente. Añade esa carta a tu mano | maiuscole incoerenti (mano / Carta de Monstruo) |
| 5299 | desc | esta carta solo cuando | esta carta cuando | ripetizione di 'solo' |
| 5394 | desc | en el Campos | en el Campo | refuso |
| 5406 | desc | y ataca tu monstruo seleccionado | y ataca a tu monstruo seleccionado | preposizione mancante |
| 5421 | desc | pasa a ser 2400 sólo durante. | pasa a ser 2400 sólo durante ese cálculo de daño. | frase troncata (inglese: during that damage calculation only) |
| 5427 | desc | de tu Baraja | de tu Deck | terminologia coerente (Deck) |
| 5493 | desc | todas las Carta Mágica y de Trampa | todas las Cartas Mágicas y de Trampa | concordanza |
| 5517 | name | Cuidador de Tumba | Cuidador de Tumbas | nome coerente con le altre carte della serie |
| 5539 | desc | Deck de fusión | Deck de Fusión | maiuscola incoerente |
| 5543 | desc | que infliga daño | que inflija daño | congiuntivo errato |
| 5546 | name | Estratégia | Estrategia | accento portoghese |
| 5557 | desc | Monstruo de NV 4 | Monstruo de Nivel 4 | abbreviazione non usata altrove |
| 5561 | desc | carta tipo Zombi con un DEF de 1200 | carta de Tipo Zombi con una DEF de 1200 | maiuscola/genere |
| 5561 | desc | añadirla a tu Mano | añadirla a tu mano | maiuscola errata |
| 5619 | desc | monstruos que tu. | monstruos que tú. | accento |
| 5619 | desc | selecciona que monstruos son destruidos | selecciona qué monstruos son destruidos | accento |
| 5624 | desc | un monstruo o more. | un/os monstruo/s. | residuo inglese ('or more') |
| 5645 | name | Paladína | Paladina | accento errato |
| 5647 | desc | no puede ataque otro monstruo | no puede atacar a otro monstruo | grammatica |
| 5656 | desc | en el Campo que la que puedas | en el Campo en la que puedas | preposizione |
| 5666 | desc | cuando no hayan otras cartas | cuando no haya otras cartas | concordanza (haber impersonale) |
| 5676 | desc | superiores del tu Deck | superiores de tu Deck | refuso |
| 5685 | desc | Voltea todos las Cartas | Voltea todas las Cartas | concordanza |
| 5689 | desc | la esta Ficha | esta Ficha | refuso |
| 5697 | desc | y la mandada al Cementerio | y lo manda al Cementerio | frase malformata (inglese: sends it to the Graveyard) |
| 5699 | desc | del turno en la que esta carta realizara una batalla | del turno en el que esta carta realice una batalla | concordanza e tempo verbale |
| 5730 | name | Más Alla | Más Allá | accento |
| 5735 | desc | Todos las monstruos | Todos los monstruos | concordanza |
| 5737 | desc | que tu seleccionaste | que tú seleccionaste | accento |
| 5756 | desc | Invocación normal | Invocación Normal | maiuscola incoerente |
| 5757 | desc | como sacrificio | como Sacrificio | maiuscola incoerente |
| 5759 | desc | tenia | tenía | accento |
| 5763 | desc | que controle de tu adversario | que controle tu adversario | preposizione di troppo |
| 5780 | desc | al End Phase del turno | durante la End Phase del turno | preposizione/genere |
| 5786 | desc | equipo con esta carta | equipado con esta carta | refuso |
| 5829 | desc | como resultado de una batalla y la manda al Cementerio | como resultado de una batalla y lo manda al Cementerio | concordanza |
| 5834 | desc | El ATK y la DEF de esta carta se convierte en | El ATK y la DEF de esta carta se convierten en | concordanza |
| 5846 | desc | si haya un | si hay un | concordanza |
| 5876 | desc | no sera más | no será más | accento |
| 5880 | desc | en vez de ser mandada al Cementerio | en vez de ser mandado al Cementerio | concordanza |
| 5952 | name | Sabiduria | Sabiduría | accento |
| 5954 | desc | Cielo"está | Cielo" está | spazio mancante |
| 5976 | desc | de tu Adversario. | de tu adversario. | maiuscola errata |
| 6004 | name | Geminis | Géminis | accento |
| 6005 | desc | cartas en tu Mano, puedes añadir esta carta a tu Mano | cartas en tu mano, puedes añadir esta carta a tu mano | maiuscola errata |
| 6010 | desc | Monstruo de un oponente Ataca | monstruo de un oponente ataca | maiuscole errate |
| 6018 | desc | sabe en que está pensando | sabe en qué está pensando | accento |
| 6019 | desc | sera manchado | será manchado | accento |
| 6025 | desc | Mientras no hayan cartas | Mientras no haya cartas | concordanza (haber impersonale) |
| 6059 | name | Energia | Energía | accento |
| 6071 | name | Resurección | Resurrección | refuso |
| 6095 | desc | Todavia | Todavía | accento |
| 6129 | name | Factoria | Factoría | accento |
| 6133 | desc | que este escrito | que esté escrito | accento |
| 6148 | desc | Inglige daño a tu adversario igual al número | Inflige daño a tu adversario igual al número | refuso (Inglige) |
| 6149 | desc | de tu Mano. Durante | de tu mano. Durante | maiuscola errata |
| 6150 | desc | desde tu Mano descartando otra carta desde tu Mano | desde tu mano descartando otra carta desde tu mano | maiuscola errata |
| 6163 | name | Ficha Bloqueadoras | Ficha Bloqueadora | concordanza |
| 6165 | name | Ficha Tramposas | Ficha Tramposa | concordanza |
| 6166 | desc | en el tu Campo | en tu Campo | refuso |
| 6174 | desc | Dekochi | Dekoichi | nome errato (inglese: Dekoichi) |
| 6218 | desc | seleccionadas no puede ser activadas | seleccionadas no pueden ser activadas | concordanza |
| 6233 | desc | Las Leyendas dicen | Las leyendas dicen | maiuscola errata |
| 6307 | desc | Invocación Especial a una 1 "Fuerza | Invocación Especial a 1 "Fuerza | refuso |
| 6383 | desc | a si mismo | a sí mismo | accento |
| 6400 | desc | desde tu Mano puedes | desde tu mano puedes | maiuscola errata |
| 6405 | desc | el ATK y el DEF de todas las otras Cartas de Monstruos en el Campo se reduce a la mitad | el ATK y la DEF de todas las otras Cartas de Monstruo en el Campo se reducen a la mitad | concordanza |
| 6410 | desc | desde tu Mano despues | desde tu mano después | maiuscola errata e accento |
| 6410 | desc | ●Trampa : elige | ●Trampa: elige | spazio prima dei due punti |
| 6410 | desc | ●Monstruo de Efecto : elige | ●Monstruo de Efecto: elige | spazio prima dei due punti |
| 6419 | desc | de esta carta el final del Damage Step. Si esta carta lucha sin | de esta carta al final del Damage Step. Si esta carta lucha sin | preposizione |
| 6419 | desc | destruye esta carta el final del Damage Step | destruye esta carta al final del Damage Step | preposizione |
| 6435 | desc | cuando hayan 3 | cuando haya 3 | concordanza (haber impersonale) |
| 6454 | desc | desde tu Mano (puede | desde tu mano (puede | maiuscola errata |
| 6487 | desc | Manda 1carta | Manda 1 carta | spazio mancante |
| 6494 | desc | mandado el Cementerio | mandado al Cementerio | preposizione |
| 6498 | desc | destruye esta carta el final del Damage Step | destruye esta carta al final del Damage Step | preposizione |
| 6517 | desc | activa un Carta Mágica Normal | activa una Carta Mágica Normal | concordanza |
| 6537 | desc | infligido a el controlador de monstruo equipado | infligido al controlador del monstruo equipado | grammatica |
| 6539 | desc | (si esta boca abajo | (si está boca abajo | accento |
| 6550 | desc | hasta 5 Carta Mágica desde | hasta 5 Cartas Mágicas desde | concordanza |
| 6574 | desc | de tu Deck y Colócala en tu Campo | de tu Deck y colócala en tu Campo | maiuscola errata |
| 6598 | desc | todas las Cartas de Magia Continuas | todas las Cartas Mágicas Continuas | terminologia coerente |
| 6608 | desc | durante el Standby Phase | durante la Standby Phase | genere di Standby Phase |
| 6636 | desc | a tu Mano o hacerles | a tu mano o hacerles | maiuscola errata |
| 6646 | desc | El ATK y la DEF de esta carta se convierte | El ATK y la DEF de esta carta se convierten | concordanza |
| 6647 | desc | El ATK y la DEF de esta carta se convierte | El ATK y la DEF de esta carta se convierten | concordanza |
| 6666 | desc | todos las Cartas Mágicas | todas las Cartas Mágicas | concordanza |
| 6675 | desc | mediante un Invocación | mediante una Invocación | concordanza |
| 6684 | desc | "Ficha de Opción"a tu Campo | "Ficha de Opción" a tu Campo | spazio mancante |
| 6685 | desc | ● Hombre Pila C | ●Hombre Pila C | spazio dopo il pallino (come le altre righe) |
| 6617 | desc | sea iguales al Nivel | sea igual al Nivel | concordanza |
| 6720 | desc | Invocación de Sacrifico, los monstruos Sacrificadas | Invocación de Sacrificio, los monstruos Sacrificados | refusi |
| 6781 | desc | y Colócala en tu Campo | y colócala en tu Campo | maiuscola errata |
| 6815 | desc | en tu Zona de Trampas Mágicas y de Trampa | en tu Zona de Cartas Mágicas y de Trampa | refuso |
| 6825 | desc | tu 3ra Standby Phase | tu 3ª Standby Phase | numerale ordinale coerente (2ª, 4º...) |
| 6955 | desc | cuyo DEF es más bajo que el ATK que esta carta | cuya DEF es más baja que el ATK de esta carta | concordanza |
| 6957 | desc | mandada el Cementerio | mandada al Cementerio | preposizione |
| 6957 | desc | como sacrificio. Cuando | como Sacrificio. Cuando | maiuscola incoerente |
| 4358 | name | Kanan loss Swordmistress | Kanan la Señora de las Espadas | nome semi-inglese; ufficiale: Kanan la Señora de las Espadas |
| 4348 | name | el Señora de la Curación | el Señor de la Curación | genere incoerente (el Señora) |
| 4644 | name | Reina de los permisos de otoño | Reina de las Hojas de Otoño | mistraduzione di 'leaves' (nessun nome spagnolo ufficiale; fr: Reine des Feuilles d'Automne) |
| 5546 | name | Estrategia de Disturbación | Estrategia de Disturbio | 'Disturbación' non esiste; ufficiale: Estrategia de Disturbio |
| 6450 | name | Triedad | La Selección | nome ufficiale spagnolo di Triage |
| 5179 | desc | cambiar el blanco de ese ataque | cambiar el objetivo de ese ataque | terminologia ufficiale: 'objetivo' (target) |
| 5187 | desc | seleccionan los blancos de ataque | seleccionan los objetivos de ataque | terminologia ufficiale: 'objetivo' (target) |

### Elenco completo delle carte cambiate
**Confronto completo originale -> nuovo con le parole cambiate evidenziate: `docs/changes_es/cards_diff.md`** (tutte le 720 voci). Dati grezzi: `docs/changes_es/cards.csv`. Prime 40 righe:

| id | nome originale | campo | originale | nuovo |
|---|---|---|---|---|
| 4017 | Brazo de espada de Dragon | name | Brazo de espada de Dragon | Brazo de Espada de Dragón |
| 4031 | Diablillo de cuerno | name | Diablillo de cuerno | Diablillo de Cuerno |
| 4036 | Zombi guerrero | desc | "Sirviente de la Calavera" + "Guerrero de lucha" | "Sirviente de la Calavera" + "Guerrero de Batalla" |
| 4042 | El pelo de serpiente | name | El pelo de serpiente | El Pelo de Serpiente |
| 4054 | Sangan | desc | Cuando esta carta se manda del Campo al Cementerio, selecciona 1 monstruo con ATK 1500 o menos de tu Deck, muéstralo a tu adversario y añadelo a tu mano. Luego baraja tu Deck. | Cuando esta carta se manda del Campo al Cementerio, selecciona 1 monstruo con ATK 1500 o menos de tu Deck, muéstralo a tu adversario y añádelo a tu mano. Luego baraja tu Deck. |
| 4055 | Insecto grande | name | Insecto grande | Insecto Grande |
| 4062 | Larva de Moth | desc | Este monstruo no puede ser Invocado mediante una Invocación Normal o Colocado. Esta carta solo puede ser Invocada mediante una Invocación Especial ofreciendo "Petit Moth" como Sacrifício en el 2º de tus turnos despues de que "Petit Moth" haya sido equipado con el "Capullo Evolutivo". | Este monstruo no puede ser Invocado mediante una Invocación Normal o Colocado. Esta carta solo puede ser Invocada mediante una Invocación Especial ofreciendo "Petit Moth" como Sacrificio en el 2º de tus turnos después de que "Petit Moth" haya sido equipado con el "Capullo Evolutivo". |
| 4070 | Hacha del Tigre | desc | Una rápido y poderoso Bestia-Guerrero que porta un hacha. | Un rápido y poderoso Bestia-Guerrero que porta un hacha. |
| 4078 | Capullo Evolutivo | desc | Puedes equipar esta carta de tu mano como una Carta Mágica de Equipo a un "Petit Moth" boca arriba en el Campo. Si está equipada, el ATK y la DEF del "Capullo Evolutivo" se aplica a "Petit Moth". | Puedes equipar esta carta de tu mano como una Carta Mágica de Equipo a un "Petit Moth" boca arriba en el Campo. Si está equipada, el ATK y la DEF del "Capullo Evolutivo" se aplican a "Petit Moth". |
| 4081 | Planta devorador de carne humana | name | Planta devorador de carne humana | Planta Come-Hombres |
| 4084 | Incursor del hacha | name | Incursor del hacha | Incursor del Hacha |
| 4088 | Dragón Negro de Ojos Rojos | desc | Un dragón feroz con una ataque mortal. | Un dragón feroz con un ataque mortal. |
| 4089 | Castillo de las Ilusiones Oscuras | desc | VOLTEO: Aumenta el ATK y la DEF de todos los monstuos de Tipo Zombi en 200 puntos. Mientras esta carta permanezca boca arriba en el Campo, el ATK y la DEF de los monstrus Tipo Zombi continúa aumentando en 200 puntos durante cada una de tus Standby Phases. Este efecto continúa hasta el 4º turno despues de la activación de esta carta. | VOLTEO: Aumenta el ATK y la DEF de todos los monstruos de Tipo Zombi en 200 puntos. Mientras esta carta permanezca boca arriba en el Campo, el ATK y la DEF de los monstruos Tipo Zombi continúa aumentando en 200 puntos durante cada una de tus Standby Phases. Este efecto continúa hasta el 4º turno después de la activación de esta carta. |
| 4090 | Segadora de las Cartas | desc | VOLTEO: Selecciona 1 Carta de Trampa en el Campo y destruyela. Si la carta seleccionada está Colocada, toma y mira la carta. Si es una Carta de Trampa, es destruida. Si es una Carta Mágica, devuelvela a su posición original. | VOLTEO: Selecciona 1 Carta de Trampa en el Campo y destrúyela. Si la carta seleccionada está Colocada, toma y mira la carta. Si es una Carta de Trampa, es destruida. Si es una Carta Mágica, devuélvela a su posición original. |
| 4093 | Quimera oscura | name | Quimera oscura | Quimera Oscura |
| 4094 | Guardián del metal | name | Guardián del metal | Guardián de Metal |
| 4105 | Pumpking el Rey de los Fantasmas | desc | Mientras el "Castillo de las Ilusiones Oscuras" permanezca boca arriba en el Campo, aumenta el ATK y la DEF de esta carta en 100 puntos. Además, el ATK y la DEF de esta carta continúa aumentando en 100 puntos durante cada una de tus Standby Phases. Este efecto continúa hasta el 4º turno despues de la activación de esta carta. | Mientras el "Castillo de las Ilusiones Oscuras" permanezca boca arriba en el Campo, aumenta el ATK y la DEF de esta carta en 100 puntos. Además, el ATK y la DEF de esta carta continúa aumentando en 100 puntos durante cada una de tus Standby Phases. Este efecto continúa hasta el 4º turno después de la activación de esta carta. |
| 4106 | Guerrero de lucha | name | Guerrero de lucha | Guerrero de Batalla |
| 4107 | Alas de la llama perversa | name | Alas de la llama perversa | Alas de la Llama Perversa |
| 4109 | Espejo de trabajo - Cambiar | name | Espejo de trabajo - Cambiar | Espejo de Trabajo - Cambiar |
| 4110 | Cortina de los ones oscuros | name | Cortina de los ones oscuros | Cortina de los Oscuros |
| 4111 | Tomozaurus | name | Tomozaurus | Tomozaurio |
| 4116 | Héroe de oriente | name | Héroe de oriente | Héroe del Este |
| 4118 | Eso que se alimenta de la vida | name | Eso que se alimenta de la vida | Eso que se Alimenta de la Vida |
| 4121 | Kamionwizard | name | Kamionwizard | Kamionmago |
| 4121 | Kamionwizard | desc | "Duende Místico" + "Cortina de los ones oscuros" | "Duende Místico" + "Cortina de los Oscuros" |
| 4122 | Escorpión de pesadilla | name | Escorpión de pesadilla | Escorpión de Pesadilla |
| 4124 | Partidario en las sombras | name | Partidario en las sombras | Partidario en las Sombras |
| 4127 | León Durmiente | desc | Un feroz animal que duerme todo el dia. A veces es mejor dejar que los Leones Durmientes duerman. | Un feroz animal que duerme todo el día. A veces es mejor dejar que los Leones Durmientes duerman. |
| 4130 | Herramienta antigua | name | Herramienta antigua | Herramienta Antigua |
| 4131 | Ave de fe | name | Ave de fe | Ave de Fe |
| 4138 | El Decimotercer Sepulcro | desc | Un zombi que aparece súbitamente desde la parcela nº 13, una sepulcro vacío. | Un zombi que aparece súbitamente desde la parcela nº 13, un sepulcro vacío. |
| 4141 | La mano de adicto | name | La mano de adicto | Mano del Demonio |
| 4145 | Zombi de plata de ojos azules | name | Zombi de plata de ojos azules | Zombi de Plata Ojizarco |
| 4148 | Manipulador de la Llama | desc | Este lanzador de conjuros ataca a sus enemigos con conjuros relacionados con el fuego como el "Mar de Llamas" y la "Muro de Fuego". | Este lanzador de conjuros ataca a sus enemigos con conjuros relacionados con el fuego como el "Mar de Llamas" y el "Muro de Fuego". |
| 4149 | Necrolancer el Señor del Tiempo | name | Necrolancer el Señor del Tiempo | Necrolancer el Tiempo-Señor |
| 4150 | Genio el telespectador del viento | desc | Esta criatura genera vientos con fuerza de galera y tornados que se llevan a sus enemigos. | Esta criatura genera vientos con fuerza de vendaval y tornados que se llevan a sus enemigos. |
| 4151 | El ladrón de fantasma encantador | name | El ladrón de fantasma encantador | El Ladrón Fantasma Encantador |
| 4154 | La sombra que controla el oscuridad | name | La sombra que controla el oscuridad | La Sombra que Controla la Oscuridad |
| 4160 | Segadora de fuego | name | Segadora de fuego | Segadora de Fuego |

(... altre 680 righe nel CSV)

## A3. Dialoghi della storia

Archivi: `script/stNN_<scena>_f.ehp`, ogni scena e' una coppia di membri `...If.bin` (offset in caratteri UTF-16) e `...Lf.bin` (stringhe UTF-16LE chiuse da NUL, alcune compresse in gzip). **601 righe** cambiate (comprese quelle che **ereditano** la correzione perche' hanno lo stesso testo originale e lo stesso giapponese di una riga corretta).

Flusso: lettura riga per riga confrontata con inglese e giapponese -> ritocchi in `tools/data/dialogue_touchups_es.json` (`esatte` e `parti`) -> `build_dialogues.py es` -> `dialogue_corrections_es.json` -> `apply_to_iso.py`. Regole automatiche di impaginazione in `build_dialogues.py`: spazio non separabile prima di `! ? : ;` anche dopo `》` (regola `FR_PUNT`), spazio dopo i segnaposto, "Mode histoire" -> "Mode aventure". Vincoli del box: ~46 caratteri per riga, max 3 righe (un segnaposto vale ~6 caratteri): `apply_to_iso` segnala le righe che potrebbero non starci.

### Ritocchi di rilettura: `esatte` (2) — frase intera originale -> frase nuova
| originale | nuovo |
|---|---|
| ¡Ten, puedes usar éste! | ¡Ten, usa este traje de criada! |
| Qué pasa...⏎¿Estás bien? | ¿Qué pasa...⏎¿Estás bien? |

### Ritocchi di rilettura: `parti` (100) — sostituzioni di testo applicate a ogni riga (in ordine)
| vecchio | nuovo |
|---|---|
| aceparla | aceptarla |
| bcadillo | bocadillo |
| glamouroso | glamuroso |
| *demenzial* | *demencial* |
| Qué el espíritu de carta te guíe. | ¡Que el espíritu de las cartas te guíe! |
| Como niegas haber tirado | Ya que niegas haber tirado |
| ha mordido e polvo | ha mordido el polvo |
| ¿Está pensada para Duelos Tag? | ¿Está pensado para Duelos Tag? |
| Aun queda | Aún queda |
| Contínuos | Continuos |
| Estoy rendido creo que | Estoy rendido, creo que |
| Bueno,,, no sé | Bueno... no sé |
| 5000PD | 5000 PD |
| La sardinas no me | Las sardinas no me |
| Pero a mi me parecen | Pero a mí me parecen |
| Un Disco vació | Un Disco vacío |
| Ya estoy, vamos a robar | Yo daré la señal. Vamos a robar |
| Aún así | Aun así |
| esta carta bien.. | esta carta bien. |
| no he olvidado! | no lo he olvidado! |
| seguro a que has oído de él | seguro que has oído hablar de él |
| So sí, quiero | Oh sí, quiero |
| Mordí el polvo! | ¡Mordí el polvo! |
| derrota Coge | derrota. Coge |
| No tientes que agradecerme | No tienes que agradecerme |
| Regla Apuest va | Regla de Apuestas va |
| Mi destino es ser el apuesto | ¡Mi destino es ser el apuesto |
| Veámos | Veamos |
| te de ideas | te dé ideas |
| contigo!. | contigo! |
| Tu eras quien | Tú eras quien |
| Por qué poco | Por muy poco |
| ¿Quién eras tú? | ¿Quién eres tú? |
| tu poco rango | tu bajo rango |
| ¡Como quiera iba a pedirte | ¡Justo iba a pedirte |
| perdido tan así | perdido así |
| lo que cualquier anciano. | lo que anhela cualquier anciano. |
| ¿Quieres un duelo, ¿huh? | ¿Quieres un duelo, eh? |
| Me quedaré vuestras almas | Llevaré vuestras almas |
| Ando buscado a | Ando buscando a |
| empresa de salsa picante | destilería de sake |
| un poco de salsa picante | un poco de shochu |
| ¡Y lleva un bikini! | ¡Y va vestida de criada! |
| en bikini | vestida de criada |
| Velo della Notte | Velo de la Noche |
| Dante Fiammeggiante | Dante Ardiente |
| Padrone Seydina | Maestro Seydina |
| Imperatore. | Emperador. |
| Truly  Furiosa | Truly Furiosa |
| Alójese | Habitación |
| ¿Quién eres? .. Ah | ¿Quién eres? ... Ah |
| ¡¿Eh?! ¿qué tiene | ¡¿Eh?! ¿Qué tiene |
| edita la Deck | edita el Deck |
| Día deL Duelo | Día del Duelo |
| monos! ⏎Ha sido alucinante! | monos! ⏎¡Ha sido alucinante! |
| He oído que van a añadir⏎canapés | ¡He oído que van a añadir⏎canapés |
| Lo siento, 《C030_1》.⏎El envío | Lo siento, 《C002_3》.⏎El envío |
| 7PM | 7:00 PM |
| ¡Yujuu!! | ¡¡Yujuu!! |
| 《C008_3》》 | 《C008_3》 |
| ¿Me pregunto por dónde⏎ anda 《C005_2》? | Me pregunto por dónde⏎ anda 《C005_2》... |
| nada de,⏎tu severidad | nada de⏎tu severidad |
| un ５0% | un 50% |
| un ８0% | un 80% |
| Slifer Red | Slifer Rojo |
| Ra Yellow | Ra Amarillo |
| Obelisk Blue | Obelisco Azul |
| ¿Huh? | ¿Eh? |
| ¿¡Huh!? | ¿¡Eh!? |
| ¡Hola, 《PLAYER》!. | ¡Hola, 《PLAYER》! |
| ¿huh? | ¿eh? |
| Eres bueno chaval. | Eres bueno, chaval. |
| Espero con ansiedad po⏎ nuestro próximo duelo. | Espero con ansiedad por⏎nuestro próximo duelo. |
| Has mejorado,⏎ 《PLAYER》. | Has mejorado,⏎《PLAYER》. |
| Buen trabajo,⏎ 《PLAYER》. | Buen trabajo,⏎《PLAYER》. |
| ¿Sabes cual es la debilidad | ¿Sabes cuál es la debilidad |
| ¡Cómo alguien como ⏎tú me hizo hecho papilla! | ¡Cómo ha podido alguien como ⏎tú hacerme papilla! |
| Encantado de conocerte. ⏎Lo siento, no me interesa. | Encantado de conocerte. ⏎Lo siento, me distraigo mucho. |
| .¿.. ...? | ¿... ...? |
| ¡Qué alguien me despierte! | ¡Que alguien me despierte! |
| Acabé contigo..⏎ | Acabé contigo...⏎ |
| Creo que esta es primera⏎vez | Creo que esta es la primera⏎vez |
| Trataré de no ser una carga⏎¡Juguemos | Trataré de no ser una carga.⏎¡Juguemos |
| ¡Sabes como detectar | ¡Sabes cómo detectar |
| Hora de los regalos⏎No lo dejes | Hora de los regalos.⏎No lo dejes |
| Eh, 《PLAYER》!⏎¿Cuánto | ¡Eh, 《PLAYER》!⏎¿Cuánto |
| digoo, medallas | digo, medallas |
| Pero necesita tener más⏎confianza en sí mismo.⏎Aun así, a veces se atasca un poco.⏎Aún le queda mucho que⏎aprender como duelista. | Pero necesita más confianza en sí mismo.⏎Aun así, a veces se atasca un poco.⏎Aún le queda mucho que aprender como duelista. |
| En la última paga me envió⏎un poco de shochu.⏎Te haré | En la última paga me envió un poco de shochu.⏎Te haré |
| Hola, 《PLAYER》. ⏎¿Tratas de entrar en⏎Obelisco dando coba ⏎a 《C008_3 | Hola, 《PLAYER》. ¿Tratas de entrar⏎en Obelisco dando coba⏎a 《C008_3 |
| ¡Tengo los músculos a punto!⏎⏎¿Cuántos batidos de proteín...⏎dig | ¡Tengo los músculos a punto!⏎¿Cuántos batidos de proteín... dig |
| duelo | Duelo |
| es mi comida⏎más favorita! | es mi comida⏎favorita! |
| cuestión de,⏎lógica, cálculo | cuestión de⏎lógica, cálculo |
| me⏎hace sentirme relajada | me⏎hace sentir relajada |
| para los duelistas,⏎fracasados, | para los duelistas⏎fracasados, |
| Espero con ansiedad por⏎nuestro próximo Duelo | Espero con ansia⏎nuestro próximo Duelo |
| Perdí,⏎pero esto sólo me hace mejor! | ¡Perdí,⏎pero esto sólo me hace mejor! |
| Vale. ¿Un Duelo normal?⏎¡Estás listo! | Vale. ¿Un Duelo normal?⏎¿Estás listo? |
| No es justo, 《C001_4》!⏎¡Yo | ¡No es justo, 《C001_4》!⏎¡Yo |

### Elenco completo delle righe
**Confronto completo originale -> nuovo (con inglese e giapponese): `docs/changes_es/dialogues_diff.md`** (tutte le 601 righe). Dati grezzi: `docs/changes_es/dialogues.csv`. Prime 30:

| id | originale | nuovo | inglese |
|---|---|---|---|
| st01_t01/ImpChrMsg#23 | Velo della Notte | Velo de la Noche | Nightshroud |
| st01_t01/ImpChrMsg#65 | Dante Fiammeggiante | Dante Ardiente | Blazing Dante |
| st01_t01/ImpChrMsg#68 | Truly  Furiosa | Truly Furiosa | Raging Truly |
| st01_t01/ImpChrMsg#74 | Padrone Seydina | Maestro Seydina | Master Seydina |
| st01_t01/ImpChrMsg#78 | Imperatore. | Emperador. | Emperor. |
| st01_t01/ImpMapMsg#0 | Academia del duelo | Academia del Duelo | Duel Academy |
| st01_t01/ImpMapMsg#7 | Campo del duelo | Campo del Duelo | Duel Academy - Duel Field |
| st01_t01/ImpMapMsg#8 | Campo del duelo | Campo del Duelo | Duel Field |
| st01_t01/ImpMapMsg#15 | Alójese 101 | Habitación 101 | Slifer Red Dorm - Room 101 |
| st01_t01/ImpMapMsg#16 | Alójese 101 | Habitación 101 | Room 101 |
| st01_t01/ImpMapMsg#17 | Alójese 102 | Habitación 102 | Slifer Red Dorm - Room 102 |
| st01_t01/ImpMapMsg#18 | Alójese 102 | Habitación 102 | Room 102 |
| st01_t01/ImpMapMsg#19 | Alójese 103 | Habitación 103 | Slifer Red Dorm - Room 103 |
| st01_t01/ImpMapMsg#20 | Alójese 103 | Habitación 103 | Room 103 |
| st01_t01/ImpMapMsg#21 | Alójese 104 | Habitación 104 | Slifer Red Dorm - Room 104 |
| st01_t01/ImpMapMsg#22 | Alójese 104 | Habitación 104 | Room 104 |
| st01_t01/ImpMapMsg#23 | Alójese 201 | Habitación 201 | Slifer Red Dorm - Room 201 |
| st01_t01/ImpMapMsg#24 | Alójese 201 | Habitación 201 | Room 201 |
| st01_t01/ImpMapMsg#25 | Alójese 202 | Habitación 202 | Slifer Red Dorm - Room 202 |
| st01_t01/ImpMapMsg#26 | Alójese 202 | Habitación 202 | Room 202 |
| st01_t01/ImpMapMsg#27 | Alójese 203 | Habitación 203 | Slifer Red Dorm - Room 203 |
| st01_t01/ImpMapMsg#28 | Alójese 203 | Habitación 203 | Room 203 |
| st01_t01/ImpMapMsg#29 | Alójese 204 | Habitación 204 | Slifer Red Dorm - Room 204 |
| st01_t01/ImpMapMsg#30 | Alójese 204 | Habitación 204 | Room 204 |
| st01_t01/Iso001E#34 | Como niegas haber tirado⏎mi Deck al Océano. | Ya que niegas haber tirado⏎mi Deck al Océano. | Like you denied throwing⏎my deck into the ocean. |
| st01_t01/Iso007E#16 | ¡Entonces también irá《C005_4》! | ¡Entonces también irá 《C005_4》! | Then so will the 《C005_4》! |
| st01_t01/Iso007E#70 | ¡《PLAYER》contra《C026_1》! | ¡《PLAYER》 contra 《C026_1》! | It's 《PLAYER》ｖｓ《C026_1》! |
| st01_t01/Iso007E#116 | 《PLAYER》 ha mordido e polvo,⏎¿quién se quiere medir con ella? | 《PLAYER》 ha mordido el polvo,⏎¿quién se quiere medir con ella? | 《PLAYER》 is eating dirt,⏎so who's next to face her? |
| st01_t01/Iso010E#322 | ¿Quién eres? .. Ah, ya veo.⏎Me llamo 《C116_1》. | ¿Quién eres? ... Ah, ya veo.⏎Me llamo 《C116_1》. | Who are you? ...Oh, I see.⏎The name's 《C116_1》. |
| st01_t01/Iso010E#324 | ¿Cómo es tu Deck?⏎¿Está pensada para Duelos Tag? | ¿Cómo es tu Deck?⏎¿Está pensado para Duelos Tag? | How's your deck?⏎Geared for tag duels? |

(... altre 571 righe nel CSV)

## A4. Frasi dei duellanti nei duelli

Tabelle `chr_wordstbl_f.bin` e `02chr_wordstbl_...` dentro ~72 archivi `duel/cutin_*.ehp` (e `zakov*`). Le frasi uniche sono ~1.800: tutte rilette. **55 frasi cambiate** (75 voci). Dati: `esatte` (32) e `parti` (24) in `duel_line_corrections_es.json`. I file `*-ptrs.txt` degli archivi dei personaggi contengono offset assoluti: se una tabella cresce vanno ricalcolati (`rimappa_puntatori`), altrimenti il duello va in crash.

Confronto con parole evidenziate: `docs/changes_es/duel_lines_diff.md`.

| originale | nuovo | voci | esempi di archivio |
|---|---|---|---|
| ¡Qué estás planeando! | ¿Qué estás planeando? | 1 | cutin_abdos01.ehp |
| ¡Quién te crees que soy! | ¿Quién te crees que soy? | 1 | cutin_abdos01.ehp |
| ¡Cuándo te rendirás! | ¿Cuándo te rendirás? | 1 | cutin_abdos01.ehp |
| Éste es el primer paso de mi ecuación.⏎⏎¡Tetera Alquimia - Destilación de Caos! | Éste es el primer paso de mi ecuación.⏎⏎¡Destilación del Caos! | 1 | cutin_amunael01.ehp |
| ¡Helios Duo Megistus! | ¡Helios Dúo Megistus! | 1 | cutin_amunael01.ehp |
| ¡Qué te parece! | ¿Qué te parece? | 3 | cutin_aska01.ehp, cutin_hayato01.ehp, cutin_rei02.ehp |
| ¡Qué estás haciendo! | ¿Qué estás haciendo? | 1 | cutin_aska01.ehp |
| BIen. Ésa es la mejor forma de hacerlo. | Bien. Ésa es la mejor forma de hacerlo. | 1 | cutin_ayukawa01.ehp |
| ¿…Crees que puedes enfrentarte a mi? | ¿…Crees que puedes enfrentarte a mí? | 1 | cutin_chousaku01.ehp |
| ¡Eek! | ¡Iiih! | 1 | cutin_daitokuji01.ehp |
| ¡Invoco a un monstruo en Posición de Ataque. | ¡Invoco a un monstruo en Posición de Ataque! | 4 | cutin_daitokuji01.ehp, cutin_mokeo01.ehp, cutin_ryo01.ehp, cutin_tome01.ehp |
| ¡Invocaré Fusión de un monstruo! | ¡Haré una Invocación⏎de Fusión de un monstruo! | 2 | cutin_fubuki01.ehp, cutin_junko01.ehp |
| Je…⏎⏎Bueno, ¿qué tal?⏎¿Qué te ha parecido ser⏎el centro de atención! | Je…⏎⏎Bueno, ¿qué tal?⏎¿Qué te ha parecido ser⏎el centro de atención? | 1 | cutin_fubuki01.ehp |
| ¿¡Que!?… | ¿¡Qué!?… | 1 | cutin_fubuki01.ehp |
| ¡Qué pasa!⏎⏎¿Lo único que sabes hacer⏎es gritar? ¡Ja ja ja! | ¿Qué pasa?⏎⏎¿Lo único que sabes hacer⏎es gritar? ¡Ja ja ja! | 1 | cutin_fubuki_drk01.ehp |
| ¡Qué! | ¿Qué? | 1 | cutin_fubuki_drk01.ehp |
| ¿Alguien tiene Bocadillos de Queso? | ¿Alguien tiene bocadillos de queso? | 1 | cutin_hayato01.ehp |
| ¡Qué te ha parecido! | ¿Qué te ha parecido? | 2 | cutin_hayato01.ehp, cutin_shou01.ehp |
| ¡Estaba guardando esto!⏎⏎¡Amanecer en la Roca de Ayers! | ¡Estaba guardando esto!⏎⏎¡Amanecer en Ayers Rock! | 1 | cutin_hayato01.ehp |
| ¡Shhhsh! ¡Eso ha sido cruel! | ¡Caray! ¡Eso ha sido cruel! | 1 | cutin_junko01.ehp |
| ¡Aquí los héroes demuestran lo que valen!⏎¡El Rascacielos de Cartas Mágicas de Campo! | ¡Aquí los héroes demuestran lo que valen!⏎¡La Carta Mágica de Campo Rascacielos! | 2 | cutin_jyudai01.ehp, cutin_player01.ehp |
| ¡Llama Wingman! | ¡Hombre Alado de Llama! | 2 | cutin_jyudai01.ehp, cutin_player01.ehp |
| ¡Rampart Blaster! | ¡Cañón del Baluarte! | 2 | cutin_jyudai01.ehp, cutin_player01.ehp |
| ¡Shining Flare Wingman! | ¡Hombre Alado del Destello Brillante! | 2 | cutin_jyudai01.ehp, cutin_player01.ehp |
| ¡Héroe Elemental Erikshieler! | ¡HÉROE Elemental Electrum! | 2 | cutin_jyudai01.ehp, cutin_player01.ehp |
| ¡En qué estabas pensando! | ¿En qué estabas pensando? | 1 | cutin_kagemaru02_a.ehp |
| ¡Jajajajaja！⏎⏎¡Al derrotarte,⏎me he convertido en…⏎invencible! | ¡Jajajajaja!⏎⏎¡Al derrotarte,⏎me he convertido en…⏎invencible! | 1 | cutin_kagemaru02_a.ehp |
| ¡Contempla mi carta prohibida!⏎⏎¡Ábrete, Puerta de la Ilusión! | ¡Contempla mi carta prohibida!⏎⏎¡Ábrete, Puerta de las Ilusiones! | 1 | cutin_kamula01.ehp |
| ¡Genesis de Vampiro! | ¡Génesis Vampírico! | 1 | cutin_kamula01.ehp |
| ¿Un empate…？⏎Qué mal… | ¿Un empate…?⏎Qué mal… | 1 | cutin_kamula01.ehp |
| ¡Te van a echar el guante! | ¡Te quedarás castigado! | 1 | cutin_kuronosu01.ehp |
| Que… | ¿Qué…? | 2 | cutin_kuronosu01.ehp, cutin_titan01.ehp |
| No tienes ninguna posibilidad de ganar …⏎⏎¡Que empiece la batalla! | No tienes ninguna posibilidad de ganar…⏎⏎¡Que empiece la batalla! | 2 | cutin_meikyu_k01.ehp, cutin_meikyu_m01.ehp |
| No tengo ni idea de qué⏎estás haciendo, ¿y tú? | No tienes ni idea de lo que⏎estás haciendo, ¿verdad? | 1 | cutin_misawa01.ehp |
| Qué te parece. | ¿Qué te parece? | 6 | cutin_mokeo01.ehp, zakov70.ehp, zakov71.ehp, zakov72.ehp |
| ¿¡Cómo es posible!?⏎⏎El corazón ardiente de una doncella⏎es más peligroso que el infierno! | ¿¡Qué te parece!?⏎⏎¡El corazón ardiente de una doncella⏎es más peligroso que el infierno! | 1 | cutin_rei01.ehp |
| Qué debo hacer… | ¿Qué debo hacer…? | 1 | cutin_rei02.ehp |
| ¿¡Que!? | ¿¡Qué!? | 1 | cutin_rei02.ehp |
| Qué te parece esto. | ¿Qué te parece esto? | 1 | cutin_ryo01.ehp |
| ¡Ciber Dragón de Dos Cabezas! | ¡Dragón Ciber de Dos Cabezas! | 1 | cutin_ryo01.ehp |
| ¡Ciber Dragón Final! | ¡Dragón Ciber Final! | 1 | cutin_ryo01.ehp |
| ¡Ciber Dragón Láser! | ¡Dragón Ciber Láser! | 1 | cutin_ryo01.ehp |
| Cómo ha podido ocurrir esto…⏎Yo no cometo errores… | ¿Cómo ha podido ocurrir esto…?⏎Yo no cometo errores… | 1 | cutin_ryo01.ehp |
| ¡Yo bajaré la guardia! | ¡Yo no bajaré la guardia! | 1 | cutin_sala01.ehp |
| ¡Vete, por favor! | ¡Ve con cuidado, por favor! | 1 | cutin_seiko01.ehp |
| ¡Levanta! | ¡Aúpa! | 1 | cutin_seiko01.ehp |
| ¡Éste es el Vehicroid definitivo！⏎¡Adelante! | ¡Éste es el Vehicroid definitivo!⏎¡Adelante! | 1 | cutin_shou01.ehp |
| ¡Mi monstruo hacer Ataque Directo a tú! | ¡Mi monstruo hacer Ataque Directo a ti! | 1 | cutin_taizan01.ehp |
| ¡Sí aún no tienes miedo, lo tendrás! | ¡Si aún no tienes miedo, lo tendrás! | 2 | cutin_thunder01.ehp, cutin_thunder_blk01.ehp |
| ¡Enfrentarte a mi lo peor que podías hacer! | ¡Enfrentarte a mí fue lo peor que podías hacer! | 1 | cutin_titan01.ehp |
| ¡Aplastad y aniquilad! | ¡Aplasta y aniquila! | 1 | cutin_titan01.ehp |
| ¿Quién va ganando?⏎¿Eh?⏎Es mi turno? | ¿Quién va ganando?⏎¿Eh?⏎¿Es mi turno? | 1 | cutin_tome01.ehp |
| Guau guau guau. | Epa, epa, epa. | 1 | cutin_tome01.ehp |
| ¡Equipo!⏎¿Estáis listos! | ¡Equipo!⏎¿Estáis listos? | 1 | cutin_zaloog01_a.ehp |
| Carta Mágica de Juego Rápido activado. | Carta Mágica de Juego Rápido activada. | 1 | zakov81.ehp |

## A5. Stringhe lunghe e corte dell'interfaccia

Tabelle `strTbl*`, `help_strtbl_*`, `ddstrtbl_*`, `field_strtbl*` (formato `(n, 12, 12+4n)` + offset + UTF-16) in 81 archivi (la stessa tabella e' copiata in piu' archivi, es. `field/always_*_fra.ehp` x6). **329 stringhe uniche cambiate**. Regole: `tools/corrections/string_rules_es.py` — **6 voci `STRINGHE`** (archivio, membro, indice 0-based, [(vecchio, nuovo)], motivo), **542 `GLOBALI`** (regex/callable, applicate dopo le STRINGHE) su **30 tabelle** (`TABELLE`); piu' 0 correzioni puntuali in `tools/data/ui_texts.json` (scrittura sul posto, testo piu' corto o uguale).

### Per membro (stringhe uniche cambiate)
| membro | stringhe |
|---|---|
| strTbl_s.bin | 90 |
| help_strtbl_contents_duel_s.bin | 59 |
| help_strtbl_contents.bin | 43 |
| strTbl.bin | 38 |
| 03_message_res.bin | 15 |
| field_strtbl_mapname.bin | 14 |
| 04_message_res.bin | 13 |
| field_strtbl.bin | 8 |
| field_strtbl_item.bin | 8 |
| ddstrtbl_s.bin | 7 |
| tushin_msg_s.bin | 7 |
| 01_message_res.bin | 7 |
| title_msg_s.bin | 6 |
| 02_message_res.bin | 5 |
| option_msg_s.bin | 4 |
| event_name.bin | 3 |
| ocg_packname_s.bin | 2 |

### Regole globali (tutte)
| modello | sostituzione | motivo |
|---|---|---|
| \bSlifer Red\b | Slifer Rojo | nome del dormitorio come nei dialoghi |
| \bRa Yellow\b | Ra Amarillo | nome del dormitorio come nei dialoghi |
| \bObelisk Blue\b | Obelisco Azul | nome del dormitorio come nei dialoghi |
| \bShadow Rid(?:er\|re)s\b | Jinetes de la Sombra | nome del gruppo come nei dialoghi (e refuso Ridres) |
| \bDuelista Shadow\b | Duelista de la Sombra | come 'duelista de sombra' nei dialoghi |
| \bArchifiend\b | Archidemonio | nome della famiglia di carte |
| \bTrio Ojama\b | Trío Ojama | nome della carta, accento |
| Cañon Magico Mega Ton | Cañón Mágico Mega Ton | nome della carta, accenti |
| XYZ-Dragón Cañon | XYZ-Dragón Cañón | nome della carta, accento |
| Catapulta Cañon | Catapulta Cañón | nome della carta, accento |
| "Magica de Campo” | "Mágica de Campo" | accento e virgolette |
| \bMagicas\b | Mágicas | accento |
| \bMagica\b | Mágica | accento |
| Criado de Cráneo | Sirviente de la Calavera | nome della carta |
| \b([Mm])onstruos Cómicos\b | \1onstruos Toon | le carte usano Toon |
| \bmonstruos Animados\b | monstruos Toon | le carte usano Toon |
| Invocación por Fusión | Invocación de Fusión | termine come sulle carte |
| Invocación por Ritual | Invocación de Ritual | termine come sulle carte |
| Invocación por Volteo | Invocación de Volteo | termine come sulle carte |
| Efecto de Disparado de Múltiple | Efecto de Disparo Múltiple | grammatica |
| Efecto de Disparado | Efecto de Disparo | grammatica (coincide con '(Continua, Encendido, Disparo, Volteo)') |
| Trampas de Contraataque | Trampas de Contraefecto | termine come sulle carte |
| \bBonus Afortunada\b | Bonus Suerte | concordanza |
| \bBonus Union\b | Bonus Unión | accento |
| Retirados e a partida | Retirados de la partida | refuso |
| Contradores de Magia | Contadores de Magia | refuso |
| Número de veces que se invocó monstruos | Número de veces que se invocaron monstruos | concordanza |
| Invocación Normal a 10 monstruos durante un duelo\. | Realizadas 10 Invocaciones Normales durante un duelo. | coerenza con le righe vicine |
| Contraatacadas Magias, Trampas efectos, Ataques e Invocaciones de tu enemigo 10 veces durante un duelo\. | Contraatacados 10 veces Magias, Trampas, efectos, Ataques e Invocaciones de tu oponente durante un duelo. | virgole e 'oponente' |
| con un ataque simple y se ganó | con un solo ataque o efecto y se ganó | l'inglese dice 'single attack or effect' |
| Gana durante el turno de tu oponente\. | Se ganó durante el turno de tu oponente. | tempo verbale come le righe vicine |
| Gana un duelo usando los Efectos de | Se ganó un duelo usando los efectos de | tempo verbale come le righe vicine |
| ^botón ×: siguiente$ | Botón ×: siguiente | maiuscola come la riga dopo |
| en el atolladero en que se encuentre | en qué atolladero se encuentre | grammatica |
| fusión de cartas de Héroe Elemental | Fusión de cartas de Héroe Elemental | maiuscola del termine del gioco |
| gente fuerte, de confiar, | gente fuerte, de confianza, | refuso |
| lo hacia desde | lo hacía desde | accento |
| suave de los que su nombre | suave de lo que su nombre | grammatica |
| explicar porqué le retuvieron | explicar por qué le retuvieron | por qué |
| porqué le retuvieron | por qué le retuvieron | por qué |
| la cual\.\.\.hace tiempo | la cual... hace tiempo | spazio |
| atractivas monstruos femeninas | atractivos monstruos femeninos | concordanza |
| llamado a "Chica Cibernética" | llamado "Chica Cibernética" | preposizione di troppo |
| como ser humano Y gracias | como ser humano. Y gracias | punteggiatura |
| en lo  primero que tenga a mano | en lo primero que tenga a mano | spazio |
| Clama tener seis Decks | Afirma tener seis Decks | 'clamar' non e' 'afirmar' |
| nadie que no se Vellian ha usado alguna vez una | nadie que no sea Vellian ha usado jamás una | refuso |
| carta principal es Golem de Mecanismo Antiguo", | carta principal es "Golem de Mecanismo Antiguo", | virgolette mancanti |
| Nadie sabe que tipo de Deck | Nadie sabe qué tipo de Deck | accento |
| saber que le pasará al hombre | saber qué le pasará al hombre | accento |
| actividades en el campus Pero | actividades en el campus. Pero | punteggiatura |
| en el campus Pero Alexis | en el campus. Pero Alexis | punteggiatura |
| para poder matricular y verle | para poder matricularse y verle | grammatica |
| también pudiera tener este poder de efecto especial como un espíritu$ | También pudiera tener este poder de efecto especial como un espíritu. | punto finale |
| signo del destino\.\.\n | signo del destino...⏎ | punti di sospensione |
| señal del destino\.\.\n | señal del destino...⏎ | punti di sospensione |
| sella dentro de una carta el alma de perdedor | sella dentro de una carta el alma del perdedor | articolo |
| tiene como a "Dragón de Oscuridad de Ojos Rojos" como carta principal | tiene a "Dragón de Oscuridad de Ojos Rojos" como carta principal | grammatica |
| ^Perfil de Sheppard del Principio$ | Perfil del Rector Sheppard | 'Principal' tradotto 'Principio'; Rector come nei dialoghi |
| Asaltante Veladora de Tumbas | Asaltante del Cuidador de Tumba | nome della carta |
| ^Sin límite\.$ | Sin límite | punto finale in piu' |
| mostrarán todas las cartas ¿Aceptas\? | mostrarán todas las cartas. ¿Aceptas? | punteggiatura |
| es una Carta Limitada, sólo 2 pueden | es una Carta Semi-Limitada, sólo 2 pueden | l'inglese dice Semi-Limited |
| está in correcta | es incorrecta | refuso |
| ^Acerca del Menú Editar Deck\.$ | Acerca del Menú Editar Deck | punto finale in piu' |
| Acerca de las carta$ | Acerca de las cartas | plurale |
| ^Cosas que puedes hacer en "Draw Phase"\.$ | Cosas que puedes hacer en "Draw Phase" | punto finale in piu' |
| (Día 3: Invocación de Tributo y Fundamentos de Magias y Trampas)\.$ | \1 | punto finale in piu' |
| Invocación de Tributo | Invocación por Sacrificio | termine ufficiale spagnolo (Invocada por Sacrificio), come nelle carte |
| Invocaciones de Tributo | Invocaciones por Sacrificio | termine ufficiale spagnolo, come nelle carte |
| ¿Qué es una Deck Receta\? | ¿Qué es una Receta de Deck? | ordine delle parole |
| ^Trampa Normales$ | Trampas Normales | plurale |
| ^Trampa Continuas$ | Trampas Continuas | plurale |
| ●Contador Mágico | ●Contadores Mágicos | plurale |
| Los Contador Mágico | Los Contadores Mágicos | plurale |
| ●Mira bocarriba carta | ●Mirar boca arriba una carta | traduzione di 'Pick up card' |
| Poner bocarriba carta significa | Mirar boca arriba una carta significa | traduzione di 'Pick up card' |
| Zone del Deck de Fusión | Zona del Deck de Fusión | refuso |
| Flujo el Turno | Flujo del Turno | refuso |
| ^colocar \(Invocación Normal\)$ | Colocar (Invocación Normal) | maiuscola |
| ●Colocar de Cartas Mágicas y de Cartas de Trampa | ●Colocar Cartas Mágicas y Cartas de Trampa | grammatica |
| \(Fase de Final\) | (Fase Final) | come le altre |
| Fase  de Batalla | Fase de Batalla | spazio |
| Deck- tienen que ser 3 | Deck: tienen que ser 3 | punteggiatura |
| Colocando Etiquetas a tus cartas favoritas o importantes hará | Colocar Etiquetas en tus cartas favoritas o importantes hará | grammatica |
| Devuelve una carta que acaba de moverse de otra vez a su posición original\. | Devuelve a su posición original una carta que acaba de moverse. | frase rotta |
| requerimientos\n(Esto es similar a la función) | requerimientos.\n\1 | punto mancante |
| etc\.,en un Deck | etc., en un Deck | spazio |
| de cual Deck se basa en tipo de concepto | de cuál Deck se basa en qué tipo de concepto | accenti |
| botón ×    Mover carta seleccionada Las cartas por lo general | botón ×⏎   Mover carta seleccionada⏎   Las cartas por lo general | a capo mancanti (come l'inglese) |
| Cartas de Monstruos de Fusión” | Cartas de Monstruo de Fusión" | concordanza |
| Cartas de Monstruos de Fusión\" | Cartas de Monstruo de Fusión" | concordanza |
| Carta de Magica llamada | Carta Mágica llamada | grammatica |
| Carta de Magia llamada | Carta Mágica llamada | grammatica |
| Polimerizacion | Polimerización | accento |
| hacer Invocación de Fusión a este tipo especial de monstruo | hacer una Invocación de Fusión de este tipo especial de monstruo | grammatica |
| Mientras carta esté boca arriba | Mientras esta carta esté boca arriba | articolo mancante |
| (?m)^os efectos generalmente | Los efectos generalmente | iniziale mancante |
| La misma se usa el mismo orden | Se usa en el mismo orden | grammatica |
| as Cartas de Trampa tienen diversos | las Cartas de Trampa tienen diversos | refuso |
| una Trampa de Carta | una Carta de Trampa | ordine delle parole |
| efecto de l Carta de Trampa | efecto de la Carta de Trampa | refuso |
| incluso durante el turno de tu oponente\.\nAdemás | incluso durante tu propio turno.⏎Además | l'inglese dice 'your own turn' |
| "Siete Herramientas del Bandido"\' | "Siete Herramientas del Bandido" | apostrofo di troppo |
| efecto de negación de la Carta de Trampa "Disruptor Mágico" | efecto de negación de Cartas Mágicas de "Disruptor Mágico" | l'inglese dice Spell Card-negating |
| Spell Speed 2 Cadenas encadenarse | Spell Speed 2 pueden encadenarse | 'pueden' sostituito per errore da 'Cadenas' |
| no Cadenas encadenarse a cartas | no pueden encadenarse a cartas | 'pueden' sostituito per errore da 'Cadenas' |
| solamente Cadenas encadenarse cartas | solamente pueden encadenarse cartas | 'pueden' sostituito per errore da 'Cadenas' |
| no Cadenas haber encadenamiento | no puede haber encadenamiento | 'puede' sostituito per errore da 'Cadenas' |
| ninguna ora activación | ninguna otra activación | refuso |
| Monstruos de Efectos\n | Monstruos de Efecto⏎ | concordanza |
| Mágicas de Juego Rápido / Mágicas Normales\nMonstruos de Efecto | Mágicas de Juego Rápido / Trampas Normales⏎Monstruos de Efecto | l'inglese dice Normal Traps |
| Cartas Prohibidas, Limitadas y Semilimitadas | Cartas Prohibidas, Limitadas y Semi-Limitadas | come nel resto |
| cuando t dicen que robes | cuando te dicen que robes | refuso |
| Los efectos no tienen como blanco a carta\(s\) específica\(s\) | Los efectos que no tienen como blanco a carta(s) específica(s) | grammatica |
| o efecto que tienen como blanco | o efectos que tienen como blanco | concordanza |
| decidir hacia donde moverla | decidir hacia dónde moverla | accento |
| otra vez e botón | otra vez el botón | refuso |
| estas cartas  particular han | estas cartas en particular han | parola mancante |
| Botón × : confirma | Botón ×: confirma | spazio |
| en una "Matchs" | en una "Match" | plurale errato |
| preguntándote que tipo | preguntándote qué tipo | accento |
| de acuerdo al DEF de cada monstruo | de acuerdo a la DEF de cada monstruo | genere di DEF come sulle carte |
| botón △para | botón △ para | spazio |
| el Deck editando en esos momentos\. | el Deck que estás editando en este momento. | grammatica |
| Seleccionando "Búsqueda" después de teclear | Seleccionando "Ejecutar" después de teclear | il pulsante si chiama Ejecutar (l'inglese: Run) |
| o el botó R\. | o el botón R. | refuso |
| Descripciónes | Descripciones | refuso |
| Parece que has adquirido práctica con unas cuantas cartas\. | Parece que has conseguido unas cuantas cartas. | mal tradotto ('gotten your hands on') |
| ^Rindes$ | Rendirse | etichetta del pulsante |
| eliminadas | retiradas | 'retirar' come nel resto del gioco |
| Los Puntos Vida de | Los Puntos de Vida de | preposizione mancante |
| Tus Puntos Vida han | Tus Puntos de Vida han | preposizione mancante |
| Te rendiste rendido debido | Te rendiste debido | ripetizione |
| se reducen 0\. | se reducen a 0. | preposizione mancante |
| un "Match" está compuesta | un "Match" está compuesto | concordanza |
| de toda el Match | de todo el Match | concordanza |
| Roba cartas desde aquí y para añadirlas a tu mano\. | Roba cartas desde aquí y añádelas a tu mano. | grammatica |
| Esta carta esta excluida | Esta carta está excluida | accento |
| El efecto de esta Magica se aplica | El efecto de esta Carta Mágica se aplica | grammatica |
| mediante Piedra Papel Tijeras | mediante Piedra, Papel o Tijeras | punteggiatura |
| continúas al duelo siguiente | continúas con el duelo siguiente | preposizione |
| \(Si no en este momento no quedan | (Si en este momento no quedan | refuso |
|  - colocar de una Carta de Trampa o de una Carta Mágica |  - Colocar una Carta de Trampa o una Carta Mágica | grammatica |
| Invocar a in monstruo | Invocar a un monstruo | refuso |
| a la colocar de una Carta de Monstruo en el campo en Posición de Defensa boca abajo se la llama una "colocar"\. | a colocar una Carta de Monstruo en el campo en Posición de Defensa boca abajo se le llama "Colocar". | frase rotta |
| boca arriba esto se le llama una | boca arriba, a esto se le llama una | grammatica |
| La colocar de Cartas Mágicas y de Trampa se diferencia de la colocar de Cartas de Monstruo | Colocar Cartas Mágicas y de Trampa se diferencia de Colocar Cartas de Monstruo | frase rotta |
| de la carta siendo usada,\n | de la carta siendo usada.⏎ | punteggiatura |
| Casa Paso de la Battle Phase | Cada Paso de la Battle Phase | refuso |
| regresarás a la Battle Step | regresarás al Battle Step | genere |
| Posición de Batalla de monstruo que es el blanco | Posición de Batalla del monstruo que es el blanco | articolo |
| tiene un DEF más bajo | tiene una DEF más baja | genere di DEF come sulle carte |
| tiene un DEF más alto | tiene una DEF más alta | genere di DEF come sulle carte |
| \n\nif Player C of Team 2 has attacked during his/her Battle Phase.*?in response to the attack\.\n |  | residuo inglese: il paragrafo e' gia' tradotto subito dopo |
| que tubo su turno justo antes de eso | que tuvo su turno justo antes de eso | refuso |
| sera capaz de elegir | será capaz de elegir | accento |
| Asumiendo que el duelo se juega de acuerdo al siguiente,\n(Equipo 1: Jugador A\nEquipo 2: Jugador C\nEquipo 1: Jugador B\nEquipo 2: Jugador D\n)(\n) | Asumiendo que el duelo se juega de acuerdo con el siguiente orden,\n\n\1\2 | frase incompleta |
| Asumiendo que el duelo se juega de acuerdo al siguiente,\n(Equipo 1: Jugador A\nEquipo 2: Jugador C\nEquipo 1: Jugador B\nEquipo 2: Jugador D)\n?$ | Asumiendo que el duelo se juega de acuerdo con el siguiente orden,⏎⏎\1⏎⏎si el Jugador C del Equipo 2 ha atacado durante su Battle Phase, el jugador que tuvo su turno justo antes de eso, que es el Jugador A del Equipo 1, podrá elegir si quiere o no activar una Carta Mágica de Juego Rápido o una Trampa como respuesta al ataque. | testo troncato: mancava il paragrafo finale (tradotto dall'inglese) |
| ^¡No hay a quién dárselo\.!$ | ¡No hay a quién dárselo! | punteggiatura |
| ^Trar$ | Comer | l'inglese dice Eat |
| ^¿Tirar bocadillo\?$ | ¿Comer bocadillo? | l'inglese dice 'Eat a sandwich?' |
| \$C0 ！ | $C0! | punto esclamativo a larghezza piena e spazio |
| ^MIE$ | MIÉ | accento |
| ^SAB$ | SÁB | accento |
| ^¡ %s adquirido!$ | ¡%s adquirido! | spazio |
| etc\.que no hayan | etc., que no hayan | punteggiatura |
| La belleza esta en su sabor | La belleza está en su sabor | accento |
| una maestro pastelero | un maestro pastelero | concordanza |
| Es divertido mascarlo\. | Es divertido masticarlo. | refuso |
| artesanalmente\.\. Sabe | artesanalmente. Sabe | punteggiatura |
| los cual explica porqué siempre se venden todos | lo cual explica por qué siempre se agotan | refuso |
| una hígado de ganso | un hígado de ganso | concordanza |
| ^Alójese (\d+)$ | Habitación \1 | il nome inglese e' Room |
| ^Academia del duelo$ | Academia de Duelos | come nel resto del gioco |
| ^Una tienda$ | Tienda | articolo di troppo |
| ^La Oficina de canciller$ | Oficina del Rector | 'Rector' come nei dialoghi |
| ^Cliff$ | Acantilado | residuo inglese |
| ^Dorm abandonado$ | Dormitorio abandonado | abbreviazione inglese |
| ^Último Arena$ | Última Arena | genere |
| No hay cartaseleccionadas | No hay cartas seleccionadas | spazio mancante |
| La contraseña introducida está incorrecta | La contraseña introducida es incorrecta | ser/estar |
| esta carya | esta carta | refuso |
| ^Esperando por oponente\.\.\.$ | Esperando al oponente... | grammatica |
| Yu-Gi- Oh! | Yu-Gi-Oh! | spazio |
| ^Derotar Crowler$ | Derrotar a Crowler | refuso |
| ^Para princiiantes$ | Para principiantes | refuso |
| nuevos dato de juego | nuevos datos de juego | concordanza |
| botón □ : Selección | botón □: Selección | spazio |
| Austes del sonido | Ajustes del sonido | refuso |
| Austa el volumen | Ajusta el volumen | refuso |
| ^EN$ | ON | 'EN' non e' ON (l'inglese dice ON) |
| ^FUERADE$ | OFF | 'FUERADE' e' un refuso per OFF |
| ^SIN LIMITE DE TIEMPO$ | SIN LÍMITE DE TIEMPO | accento |
| ^NO LIMITE$ | SIN LÍMITE | spagnolo corretto |
| Mientras en el modo ad hoc, sostenga el botón SELECT | Mientras estés en modo ad hoc, mantén presionado el botón SELECT | registro: tutto il gioco da' del tu |
| para desconectar y devolver al menú principal | para desconectar y volver al menú principal | grammatica |
| presiona el botón ×\$C0, y confirmar\. | presiona el botón ×$C0, y confirma. | imperativo |
| COLECCCIONABLES | COLECCIONABLES | refuso |
| ^Escogido entre representante\.$ | Elegido entre los representantes. | grammatica |
| ^Interscholastic se baten en duelo\.$ | Duelo interescolar. | residuo inglese |
| ^Antes de una reunión\.$ | El día antes del torneo Tag Force. | l'inglese: the day before the Tag Force meet |
| Ahora le turno a  | Ahora es el turno de  | refuso: 'le turno' |
| Ahora le turno\na  | Ahora es el turno⏎de  | refuso: 'le turno' |
| ¡Le turno a\n | ¡Es el turno de⏎ | refuso: 'le turno' |
| Le turno a  | Es el turno de  | refuso: 'le turno' |
| Como te turno\na ti primero, \$0, | Como el primer turno es⏎tuyo, $0, | refuso: 'te turno' |
| \$C5Sryus | $C5Syrus | refuso |
| \$CALP\$ de su rival | $CALP$C0 de su rival | codice colore non chiuso |
| Zona de Cartas de Monstruos Después, pulsa | Zona de Cartas de Monstruos. Después, pulsa | punteggiatura |
| tiene una en\nPosición de Ataque | tiene uno en⏎Posición de Ataque | concordanza (monstruo) |
| Pero si invocación a un\nmonstruo en vez de\nColocar, | Pero si invocas a un⏎monstruo en vez de⏎colocarlo, | refuso: 'invocación' per 'invocas' |
| e invocación a uno\ncon un ATK menor | e invocas a uno⏎con un ATK menor | refuso: 'invocación' per 'invocas' |
| \$Cpad analógico\$C0 | $C8pad analógico$C0 | codice colore incompleto |
| debes realizar una Invocación de u ofrecer uno o más monstruos como Tribute\. | debes realizar una Invocación y ofrecer uno o más monstruos como Sacrificio. | frase troncata e residuo inglese |
| ^invocación a 1 monstruo\.$ | Invoca a 1 monstruo. | refuso: 'invocación' per 'invoca' |
| ¡\$0!\ninvocación a un monstruo! | ¡$0!⏎¡Invoca a un monstruo! | refuso: 'invocación' per 'invoca' |
| Pulsa el botón × para\nabrir el menú de Phase\.\nSelecciona "End Phase" y\nluego pulsa el botón ○\. | Pulsa el botón ○ para⏎abrir el menú de Phase.⏎Selecciona "End Phase" y⏎luego pulsa el botón ×. | tasti scambiati (l'inglese: ○ apre il menu, × conferma) |
| que Colocar boca abajo, se pondrán | que se coloquen boca abajo se pondrán | grammatica |
| Primero hay que Colocar\nboca abajo | Primero hay que colocarlas⏎boca abajo | grammatica |
| Colocar tu Carta de Trampa\. | ¡Coloca tu Carta de Trampa! | imperativo |
| Antes, \$C5Bastion\$C0 ha preguntado | Antes, $C5Syrus$C0 ha preguntado | l'inglese dice Syrus |
| %C5Alexis | $C5Alexis | codice colore |
| aumentan en \$CA200\$\.\.\. | aumentan en $CA200$C0... | codice colore non chiuso |
| disminuyen en \$CA200\$! | disminuyen en $CA200$C0! | codice colore non chiuso |
| ¡Ahora me turno! | ¡Ahora es mi turno! | refuso |
| \$C5Alexis'\$C0 | $C5Alexis$C0 | apostrofo di troppo |
| Cartas de Trampas Normales | Cartas de Trampa Normales | Trampa e' invariabile |
| #CACarta | $CACarta | codice colore |
| Zona de de  | Zona de  | parola doppia |
| ¡Los monstruo de  | ¡Los monstruos de  | plurale |
| "\$C6Umi\$C0" sigue activo, | "$C6Umi$C0" sigue activa, | concordanza con Carta Mágica |
| \bel Hechizo(\s)de(\s)(Campo\|Equipo) | la Carta Mágica\1de\2\3 | termine come sulle carte (e genere) |
| \bEl Hechizo(\s)de(\s)(Campo\|Equipo) | La Carta Mágica\1de\2\3 | termine come sulle carte (e genere) |
| \bHechizo(\s)de(\s)(Campo\|Equipo) | Carta Mágica\1de\2\3 | termine come sulle carte |
| (?<=[^\s])(?<!Sí)(?<!No)  +(?=[^\s]) |   | spazio doppio |
| \bun refinar búsqueda\b | un filtrado | terminologia come il menu 'Filtrar' |
| Refinar Búsqueda | Filtrar | terminologia come il menu 'Filtrar' |
| "Brazo\ de\ espada\ de\ Dragon" | "Brazo de Espada de Dragón" | quoted card name: official name |
| "Brazo\ de\ espada\ de\ Dragón" | "Brazo de Espada de Dragón" | quoted card name: official name |
| "Diablillo\ de\ cuerno" | "Diablillo de Cuerno" | quoted card name: official name |
| "El\ pelo\ de\ serpiente" | "El Pelo de Serpiente" | quoted card name: official name |
| "Insecto\ grande" | "Insecto Grande" | quoted card name: official name |
| "Planta\ devorador\ de\ carne\ humana" | "Planta Come-Hombres" | quoted card name: official name |
| "Incursor\ del\ hacha" | "Incursor del Hacha" | quoted card name: official name |
| "Quimera\ oscura" | "Quimera Oscura" | quoted card name: official name |
| "Guardián\ del\ metal" | "Guardián de Metal" | quoted card name: official name |
| "Guerrero\ de\ lucha" | "Guerrero de Batalla" | quoted card name: official name |
| "Alas\ de\ la\ llama\ perversa" | "Alas de la Llama Perversa" | quoted card name: official name |
| "Espejo\ de\ trabajo\ \-\ Cambiar" | "Espejo de Trabajo - Cambiar" | quoted card name: official name |
| "Cortina\ de\ los\ ones\ oscuros" | "Cortina de los Oscuros" | quoted card name: official name |
| "Tomozaurus" | "Tomozaurio" | quoted card name: official name |
| "Héroe\ de\ oriente" | "Héroe del Este" | quoted card name: official name |
| "Eso\ que\ se\ alimenta\ de\ la\ vida" | "Eso que se Alimenta de la Vida" | quoted card name: official name |
| "Kamionwizard" | "Kamionmago" | quoted card name: official name |
| "Escorpión\ de\ pesadilla" | "Escorpión de Pesadilla" | quoted card name: official name |
| "Partidario\ en\ las\ sombras" | "Partidario en las Sombras" | quoted card name: official name |
| "Herramienta\ antigua" | "Herramienta Antigua" | quoted card name: official name |
| "Ave\ de\ fe" | "Ave de Fe" | quoted card name: official name |
| "La\ mano\ de\ adicto" | "Mano del Demonio" | quoted card name: official name |
| "Zombi\ de\ plata\ de\ ojos\ azules" | "Zombi de Plata Ojizarco" | quoted card name: official name |
| "Necrolancer\ el\ Señor\ del\ Tiempo" | "Necrolancer el Tiempo-Señor" | quoted card name: official name |
| "El\ ladrón\ de\ fantasma\ encantador" | "El Ladrón Fantasma Encantador" | quoted card name: official name |
| "La\ sombra\ que\ controla\ la\ oscuridad" | "La Sombra que Controla la Oscuridad" | quoted card name: official name |
| "La\ sombra\ que\ controla\ el\ oscuridad" | "La Sombra que Controla la Oscuridad" | quoted card name: official name |
| "Segadora\ de\ fuego" | "Segadora de Fuego" | quoted card name: official name |
| "Pote\ antiguo" | "Tarro Antiguo" | quoted card name: official name |
| "Preso\ oscuro" | "Preso Oscuro" | quoted card name: official name |
| "Macis\ de\ tecla" | "Llave de la Maza" | quoted card name: official name |
| "Zombi\ de\ topo\ de\ Mech" | "Zombi Topo Mecánico" | quoted card name: official name |
| "Amante\ feliz" | "Amante Feliz" | quoted card name: official name |
| "Fantasma\ de\ fantasma" | "Espectro Fantasma" | quoted card name: official name |
| "Dragón\ B\.\ Cráneo" | "Dragón de Cráneo Negro" | quoted card name: official name |
| "Acosador\ de\ cráneo" | "Acechador del Cráneo" | quoted card name: official name |
| "Reloj\ de\ arena\ de\ la\ vida" | "Reloj de Arena de la Vida" | quoted card name: official name |
| "Vela\ del\ destino" | "Vela del Destino" | quoted card name: official name |
| "Fairywitch" | "Hadabruja" | quoted card name: official name |
| "Stone\ Armadiller" | "Armadiller de Piedra" | quoted card name: official name |
| "Hechicero\ antiguo" | "Hechicero Antiguo" | quoted card name: official name |
| "Rey\ Niebla" | "Rey Nebuloso" | quoted card name: official name |
| "Légamo\ de\ Cambiar" | "Limo de Cambio" | quoted card name: official name |
| "Armadura\ de\ insecto\ con\ cañón\ de\ rayo\ láser" | "Armadura Insecto con Cañón Láser" | quoted card name: official name |
| "Cyber\ revestimiento" | "Ciber Escudo" | quoted card name: official name |
| "Ojo\ de\ Megasonic" | "Ojo Megasónico" | quoted card name: official name |
| "Guerra\ \-\ león\ excelente" | "Súper León de Guerra" | quoted card name: official name |
| "Zombis\ de\ tres\ patas" | "Zombis de Tres Piernas" | quoted card name: official name |
| "Pingüino\ volando" | "Pingüino Volador" | quoted card name: official name |
| "Revestimiento\ de\ milenio" | "Escudo Milenario" | quoted card name: official name |
| "El\ obsequio\ de\ hada" | "Regalo del Hada" | quoted card name: official name |
| "El\ espejo\ de\ adicto" | "Espejo Demoníaco" | quoted card name: official name |
| "Gusano\ de\ calabozo" | "Gusano del Calabozo" | quoted card name: official name |
| "Monstruo\ más\ dócil" | "Domador de Monstruos" | quoted card name: official name |
| "Dragón\ Definitivo\ de\ Ojos\ Azules" | "Dragón de Ojos Azules Definitivo" | quoted card name: official name |
| "Dragón\ de\ loro" | "Dragón Loro" | quoted card name: official name |
| "Conejo\ oscuro" | "Conejo Oscuro" | quoted card name: official name |
| "Dragón\ mascota\ de\ Arpía" | "Dragón Mascota de Arpía" | quoted card name: official name |
| "Máquina\ de\ péndulo" | "Máquina del Péndulo" | quoted card name: official name |
| "Comilón\ de\ zona" | "Comilón de Zona" | quoted card name: official name |
| "Swordsman\ de\ una\ nación\ extranjera" | "Espadachín de una Tierra Lejana" | quoted card name: official name |
| "Slasher\ de\ sable" | "Asesino de la Espada" | quoted card name: official name |
| "Mech\ \-\ soldado\ gigante" | "Mech - Soldado Gigante" | quoted card name: official name |
| "Spider\ mecánico" | "Araña Karakuri" | quoted card name: official name |
| "Apedree\ D\." | "Dragón de Piedra" | quoted card name: official name |
| "Diosa\ del\ capricho" | "Diosa del Capricho" | quoted card name: official name |
| "Tutor\ del\ mar" | "Centinela del Mar" | quoted card name: official name |
| "Red\ Seasnake\ del\ gigante" | "Serpiente Marina Roja Gigante" | quoted card name: official name |
| "Roca\ de\ barril" | "Roca de Cañón" | quoted card name: official name |
| "Caracol\ de\ perno" | "Caracol del Rayo" | quoted card name: official name |
| "Pingüino\ de\ perno" | "Pingüino de Perno" | quoted card name: official name |
| "Enrojezca\ Sunbird" | "Pájaro Sol Carmesí" | quoted card name: official name |
| "Comilón\ de\ aire" | "Comeaire" | quoted card name: official name |
| "Kamen\ de\ mar" | "Kamen de Mar" | quoted card name: official name |
| "Lirio\ de\ barril" | "Lirio Cañón" | quoted card name: official name |
| "Ball\ de\ aguja" | "Bola de Agujas" | quoted card name: official name |
| "Dogra\ de\ vendaval" | "Gale Dogra" | quoted card name: official name |
| "Peces\ disparatados" | "Peces Disparatados" | quoted card name: official name |
| "Bracchio\ \-\ raidus" | "Bracchio-raidus" | quoted card name: official name |
| "Scizzar\ valiente" | "Scizzar Valiente" | quoted card name: official name |
| "Ave\ de\ tortuga" | "Pájaro Tortuga" | quoted card name: official name |
| "Ave\ monstruosa" | "Ave Monstruosa" | quoted card name: official name |
| "Chico\ Estrela" | "Chico Estrella" | quoted card name: official name |
| "Cazador\ de\ cuello" | "Cazador de Cuello" | quoted card name: official name |
| "Arena\ esotérica" | "Arena Mística" | quoted card name: official name |
| "Frog\ el\ Jam" | "Sapo Viscoso" | quoted card name: official name |
| "Fenomenal\ mamut\ de\ Goldfine" | "Gran Mamut de Goldfine" | quoted card name: official name |
| "Tiburón\ negro\ devorador\ de\ carne\ humana" | "Tiburón Negro Devorador de Carne Humana" | quoted card name: official name |
| "Anthrosaurus" | "Anthrosaurio" | quoted card name: official name |
| "Trakadon" | "Trakodon" | quoted card name: official name |
| "Little\ D" | "D Pequeño" | quoted card name: official name |
| "Macis\ de\ tecla\ \#2" | "Llave de la Maza #2" | quoted card name: official name |
| "Dragón\ de\ hada" | "Dragón Hada" | quoted card name: official name |
| "Reloj\ de\ arena\ del\ valor" | "Reloj de Arena del Coraje" | quoted card name: official name |
| "La\ cosa\ que\ se\ esconde\ en\ el\ barro" | "La Cosa que se Esconde en el Barro" | quoted card name: official name |
| "Amazon\ de\ los\ mares" | "Amazona de los Mares" | quoted card name: official name |
| "Rata\ blindada" | "Rata Blindada" | quoted card name: official name |
| "Lagartija\ de\ noche" | "Lagarto Nocturno" | quoted card name: official name |
| "Bugroth\ anfibio" | "Bugroth Anfibio" | quoted card name: official name |
| "Sustancia\ pegajosa\ horripilante" | "Sustancia Pegajosa Horripilante" | quoted card name: official name |
| "Kunai\ con\ la\ cadena" | "Kunai con Cadena" | quoted card name: official name |
| "Aplaste\ la\ tarjeta" | "Virus Aplastacartas" | quoted card name: official name |
| "Erradicar\ aerosol" | "Aerosol Erradicador" | quoted card name: official name |
| "Erradicar\ aerorosol" | "Aerosol Erradicador" | quoted card name: official name |
| "Bosquejo\ eterno" | "Sequía Eterna" | quoted card name: official name |
| "Castillo\ brillante" | "Palacio Brillante" | quoted card name: official name |
| "Ritual\ de\ guerra\ \-\ león" | "Ritual del León de Guerra" | quoted card name: official name |
| "Ritual\ de\ espejo\ detestable" | "Ritual del Espejo Bestial" | quoted card name: official name |
| "Agujero\-Trampa\ De\ Ácido" | "Agujero Trampa de Ácido" | quoted card name: official name |
| "Ruina\ extendida" | "Ruina Generalizada" | quoted card name: official name |
| "Duende\ travieso\ admirador" | "Abanico Goblin" | quoted card name: official name |
| "Reina\ de\ Cosmo" | "Reina Cosmo" | quoted card name: official name |
| "Dragón\ de\ meteorito" | "Dragón Meteoro" | quoted card name: official name |
| "Dragón\ de\ B\ de\ meteorito" | "Dragón Meteoro Negro" | quoted card name: official name |
| "Firewing\ Pegasus" | "Pegaso Aladefuego" | quoted card name: official name |
| "Ritual\ mágico\ oscuro" | "Ritual de Magia Negra" | quoted card name: official name |
| "Mago\ del\ Caos\ Oscuro" | "Mago del Caos Negro" | quoted card name: official name |
| "Illusionist\ oscuro\ \-\ ojos" | "Ilusionista de Ojos Oscuros" | quoted card name: official name |
| "Círculo\ de\ explosión" | "Esfera Explosiva" | quoted card name: official name |
| "Alpha\ el\ Guerrero\ de\ Imán" | "Alfa el Guerrero Magnético" | quoted card name: official name |
| "Dragón\ de\ metal\ negro\ rojo\ \-\ ojos" | "Dragón de Metal Negro Ojos Rojos" | quoted card name: official name |
| "Aníbal\ el\ Nigromante" | "Hannibal Necromante" | quoted card name: official name |
| "Quimera\ la\ bestia\ mítica\ volando" | "Quimera, la Bestia Voladora Mítica" | quoted card name: official name |
| "Cyber\ Predador" | "Ciber Predador" | quoted card name: official name |
| "Beta\ el\ Guerrero\ de\ Imán" | "Beta el Guerrero Magnético" | quoted card name: official name |
| "Gran\ Escudo\ Guardna" | "Gran Escudo Gardna" | quoted card name: official name |
| "La\ espada\ de\ piel\ de\ caimán" | "Aligátor de la Espada" | quoted card name: official name |
| "Caimán\ cyber\-\ tecnología" | "Aligátor Cibertech" | quoted card name: official name |
| "Gamma\ el\ Guerrero\ de\ Imán" | "Gamma el Guerrero Magnético" | quoted card name: official name |
| "Máquina\ del\ tiempo" | "Máquina del Tiempo" | quoted card name: official name |
| "Multiplique" | "Multiplicar" | quoted card name: official name |
| "Espada\ de\ Fuerza\ Luminosa" | "Espada de la Fuerza de Luz" | quoted card name: official name |
| "Dados\ garbosos" | "Dado Grácil" | quoted card name: official name |
| "Dados\ de\ cráneo" | "Dado de Cráneo" | quoted card name: official name |
| "Cortina\ de\ Magic\ oscura" | "Cortina de Magia Oscura" | quoted card name: official name |
| "Llamada\ de\ la\ tumba" | "Llamada de la Tumba" | quoted card name: official name |
| "Raigeki\ de\ inconformista" | "Anti Raigeki" | quoted card name: official name |
| "Llamada\ de\ la\ oscuridad" | "Llamada de Oscuridad" | quoted card name: official name |
| "Llamada\ del\ oscuridad" | "Llamada de Oscuridad" | quoted card name: official name |
| "Chispa\ Luminosa" | "Chispa Reluciente" | quoted card name: official name |
| "Hermano\ de\ la\ Arpía" | "Explorador del Cielo" | quoted card name: official name |
| "Valkyrion\ el\ Guerrero\ de\ Imán" | "Valkyrion el Guerrero Magno" | quoted card name: official name |
| "El\ dragón\ de\ espada\ de\ piel\ de\ caimán" | "Dragón del Aligátor de la Espada" | quoted card name: official name |
| "Soldado\ Cinético" | "Soldado Cifrado" | quoted card name: official name |
| "Devorador\ de\ Almas" | "Comealma" | quoted card name: official name |
| "Gusano\ Bolsón\ Electromagnético" | "Polilla Electromagnética" | quoted card name: official name |
| "Robodama" | "Robolady" | quoted card name: official name |
| "Soldado\ de\ los\ Artilugios" | "Soldado Mecanismo" | quoted card name: official name |
| "Ficha\ de\ Monstruo\ Insecto" | "Ficha Monstruo Insecto" | quoted card name: official name |
| "Cartas\ infinitas" | "Cartas Infinitas" | quoted card name: official name |
| "Bebé\ de\ la\ Luna\ Roja" | "Bebé Vampiro" | quoted card name: official name |
| "Puerta\ de\ la\ Ilusión" | "Puerta de las Ilusiones" | quoted card name: official name |
| "Tetera\ Alquimia\ \-\ Destilación\ de\ Caos" | "Destilación del Caos" | quoted card name: official name |
| "Piedra\ del\ Filósofo\ \-\ Sabatier" | "Sabatiel - La Piedra Filosofal" | quoted card name: official name |
| "Amanecer\ en\ la\ Roca\ de\ Ayer" | "Amanecer en Ayers Rock" | quoted card name: official name |
| "Amazoness\ Arquera" | "Arquera Amazoness" | quoted card name: official name |
| "Marie\ la\ Caida" | "Señoroscura Marie" | quoted card name: official name |
| "Mamotreto\ de\ Magia\ Negra\ de\ Maga\ Oscura" | "Fórmula Mágica" | quoted card name: official name |
| "Catedral\ de\ Nobles" | "Templo de los Reyes" | quoted card name: official name |
| "Encarnación\ de\ Apofis" | "Encarnación de Apophis" | quoted card name: official name |
| "Entierro\ Tonto" | "Entierro Insensato" | quoted card name: official name |
| "Makiu" | "Makiu, la Niebla Mística" | quoted card name: official name |
| "Serket\ la\ Bestia\ Mística" | "Bestia Mística de Serket" | quoted card name: official name |
| "Caballero\ del\ Viento\ Oscuro\ de\ Gaia" | "Gaia el Caballero Feroz Rápido" | quoted card name: official name |
| "Guardián\ Celta\ Convertido" | "Guardia Celta Convertido" | quoted card name: official name |
| "Garuda\ el\ Espíritu\ del\ viento" | "Garuda el Espíritu del Viento" | quoted card name: official name |
| "Poder\ Almacenado" | "Poder Acumulado" | quoted card name: official name |
| "Muñeca\ Cebo" | "Muñeca Señuelo" | quoted card name: official name |
| "Flecha\ Encantada" | "Flecha Rompedora de Hechizos" | quoted card name: official name |
| "Maestro\ de\ la\ Cadena\ Amazoness" | "Maestra de la Cadena Amazoness" | quoted card name: official name |
| "Vider\ Des" | "Viser Des" | quoted card name: official name |
| "Caballero\ Cráneo\ \#2" | "Caballero del Cráneo #2" | quoted card name: official name |
| "Máquina\ Absorbevida" | "Máquina Absorbe Vidas" | quoted card name: official name |
| "Unidad\ Lanzapiedras" | "Unidad Throwstone" | quoted card name: official name |
| "Un\ Plan\ con\ Estratagema" | "Un plan de finta" | quoted card name: official name |
| "El\ Dragón\ que\ mora\ en\ la\ Cueva" | "El Dragón que Mora en la Cueva" | quoted card name: official name |
| "Super\ Rejuvenecimiento" | "Súper Rejuvenecimiento" | quoted card name: official name |
| "Arma\ Biológica\ De\-Spell" | "Cañón de Virus" | quoted card name: official name |
| "Demonio\ Silente" | "Perdición Silenciosa" | quoted card name: official name |
| "Ficha\ de\ Kuriboh" | "Ficha Kuriboh" | quoted card name: official name |
| "Super\ Robodama" | "Super Robolady" | quoted card name: official name |
| "Escorpión\ de\ 8\ Garras" | "Escorpión de 8 Pinzas" | quoted card name: official name |
| "Ficha\ Malvada" | "Ficha Vil" | quoted card name: official name |
| "Designador\ Negro" | "Designador Oscuro" | quoted card name: official name |
| "Amo\ de\ la\ Marioneta" | "Amo de Títeres" | quoted card name: official name |
| "Hechizo\ de\ Dolor" | "Conjuro de Dolor" | quoted card name: official name |
| "Soldado\ Oculto" | "Soldados Escondidos" | quoted card name: official name |
| "Calamidad\ del\ Malvado" | "Catástrofe Malevolente" | quoted card name: official name |
| "Alivio\ de\ Monstruo" | "Relevar al Monstruo" | quoted card name: official name |
| "Amo\ del\ Dragón\ Soldado" | "Caballero Amo del Dragón" | quoted card name: official name |
| "F\.G\.D\." | "Dragón de Cinco Cabezas" | quoted card name: official name |
| "Soga\ del\ Espíritu" | "Cuerda del Alma" | quoted card name: official name |
| "Zombi\ Duende" | "Goblin Zombi" | quoted card name: official name |
| "Vampiro\ Orchis" | "Orchis Vampírico" | quoted card name: official name |
| "Ordenando\ Libros\ de\ Magia" | "Ordenando el Libro de Magia" | quoted card name: official name |
| "Ordenando\ Libros\ de\ Mágia" | "Ordenando el Libro de Magia" | quoted card name: official name |
| "Libro\ de\ Conjuros\ Oculto" | "Libro de Magia Oculto" | quoted card name: official name |
| "Desarmar" | "Desarmamiento" | quoted card name: official name |
| "Cieno\ con\ Reflejos\ Metálicos" | "Limo Reflectametal" | quoted card name: official name |
| "Excavación\ de\ Piedras\ Mágicas" | "Excavación de la Piedra Mágica" | quoted card name: official name |
| "Ficha\ Demonio\ Metal" | "Ficha Demonio Metálico" | quoted card name: official name |
| "Ladrón\ de\ Almas" | "Toma Almas" | quoted card name: official name |
| "Piedra\ del\ Sabio" | "La Piedra del Sabio" | quoted card name: official name |
| "Archidemonio\ Álfil\ Oscuro" | "Archidemonio Alfil Oscuro" | quoted card name: official name |
| "Semilla\ Primigénia" | "Semilla Primigenia" | quoted card name: official name |
| "D\.\ Victoria" | "Dragón de la Victoria" | quoted card name: official name |
| "Zoma\ Calavera" | "Zoma de Calavera" | quoted card name: official name |
| "Seis\ Máximo" | "Seis como Máximo" | quoted card name: official name |
| "Máquina\ Peligrosa\ TIPO\-6" | "Máquina Peligrosa Tipo 6" | quoted card name: official name |
| "Ejército\ de\ Pira" | "Ejército de Pirañas" | quoted card name: official name |
| "Choque\ de\ Escudo" | "Pulverizar el Escudo" | quoted card name: official name |
| "Demonio\ Geminis" | "Diablillos Géminis" | quoted card name: official name |
| "Demonio\ Géminis" | "Diablillos Géminis" | quoted card name: official name |
| "Regreso\ del\ Zombi" | "Zombi Retornado" | quoted card name: official name |
| "Cadáver\ de\ Yata\-Garasu" | "Legado de Yata-Garatsu" | quoted card name: official name |
| "Invitación\ de\ Espíritu\ Terrestre" | "Invitación de los Espíritus Terrestres" | quoted card name: official name |
| "Lacooda\ de\ 3\ jorobas" | "Lacooda de 3 Jorobas" | quoted card name: official name |
| "Momia\ Regenerativa" | "Momia Regeneradora" | quoted card name: official name |
| "Gandra\ D\.\ Triturador" | "Gandora el Dragón de la Destrucción" | quoted card name: official name |
| "Dragón\ de\ Metal\ Raro" | "Dragón de Metales Preciosos" | quoted card name: official name |
| "Cría\ B\.\ de\ Ojos\ Rojos" | "Cría de Dragón Negro" | quoted card name: official name |
| "El\ Tramposo" | "El Difícil" | quoted card name: official name |
| "Magia\ de\ Tramposo\ 4" | "Conjuro Difícil 4" | quoted card name: official name |
| "Ficha\ Tramposas" | "Ficha Difícil" | quoted card name: official name |
| "Ficha\ Tramposa" | "Ficha Difícil" | quoted card name: official name |
| "Cruz\ del\ Mago" | "Magos, Uníos" | quoted card name: official name |
| "Gran\ Núcleo" | "B.E.S. Núcleo Grande" | quoted card name: official name |
| "Sello\ del\ Dueño" | "Sello del Propietario" | quoted card name: official name |
| "Maldición\ de\ Vampiro" | "Maldición del Vampiro" | quoted card name: official name |
| "Ataque\ Unión" | "Ataque Unido" | quoted card name: official name |
| "Sanguijuela" | "Chupasangre" | quoted card name: official name |
| "Ojo\ Penetrante" | "Ojo Agobiante" | quoted card name: official name |
| "Genesis\ de\ Vampiro" | "Génesis de Vampiro" | quoted card name: official name |
| "Soldados\ Maquinistas" | "Maquinaria Soldado" | quoted card name: official name |
| "Defensor\ Maquinista" | "Maquinaria Defensora" | quoted card name: official name |
| "Francotirador\ Maquinista" | "Maquinaria Francotiradora" | quoted card name: official name |
| "Fuerza\ Maquinista" | "Fuerza de la Maquinaria" | quoted card name: official name |
| "Héroe\ Elemental\ Avian" | "HÉROE Elemental Avian" | quoted card name: official name |
| "Héroe\ Elemental\ Burstinatrix" | "HÉROE Elemental Burstinatrix" | quoted card name: official name |
| "Héroe\ Elemental\ Clayman" | "HÉROE Elemental Clayman" | quoted card name: official name |
| "Héroe\ Elemental\ Sparkman" | "HÉROE Elemental Sparkman" | quoted card name: official name |
| "Héroe\ Elemental\ de\ la\ Llama\ Wingman" | "HÉROE Elemental de la Llama Wingman" | quoted card name: official name |
| "Héroe\ Elemental\ del\ Trueno\ Gigante" | "HÉROE Elemental del Trueno Gigante" | quoted card name: official name |
| "Caballero\ Sagrado\ Ishzark" | "Isaac, Caballero Divino" | quoted card name: official name |
| "Héroe\ Elemental\ Bubbleman" | "HÉROE Elemental Bubbleman" | quoted card name: official name |
| "Ciber\ Dragón\ de\ Dos\ Cabezas" | "Dragón Ciber de Dos Cabezas" | quoted card name: official name |
| "Ciber\ Dragón\ Final" | "Dragón Ciber Final" | quoted card name: official name |
| "Invocación\ de\ Sacerdote" | "Monje Invocador" | quoted card name: official name |
| "Ruta\ Pavorosa\ Oscura" | "La Raizmuerta Malvada" | quoted card name: official name |
| "Vandalgyon\ Gobernante\ Oscuro" | "Van'Dalgyon el Señor de los Dragones Oscuros" | quoted card name: official name |
| "Fuerza\ de\ Ataque\ de\ Elite\ Goblin" | "Fuerza de Ataque de Élite Goblin" | quoted card name: official name |
| "Des\ Rana" | "Des RANA" | quoted card name: official name |
| "Rana\ del\ Robo\ Venenoso" | "RANA del Robo Tóxica" | quoted card name: official name |
| "Caballero\ Bromista\ Alkana" | "Bufón Escolta Arcano" | quoted card name: official name |
| "Asesino\ de\ la\ Guadaña\ Espantosa" | "Cosechador de la Guadaña del Terror" | quoted card name: official name |
| "Héroe\ Elemental\ Shining\ Flare\ Wingman" | "HÉROE Elemental Shining Flare Wingman" | quoted card name: official name |
| "Héroe\ Elemental\ Bladedge" | "HÉROE Elemental Bladedge" | quoted card name: official name |
| "Héroe\ Elemental\ Wildheart" | "HÉROE Elemental Wildheart" | quoted card name: official name |
| "Héroe\ Elemental\ Rampart\ Blaster" | "HÉROE Elemental Rampart Blaster" | quoted card name: official name |
| "Héroe\ Elemental\ Tempest" | "HÉROE Elemental Tempest" | quoted card name: official name |
| "Héroe\ Elemental\ Wiledge" | "HÉROE Elemental Wildedge" | quoted card name: official name |
| "Héroe\ Elemental\ Necroshade" | "HÉROE Elemental Necroshade" | quoted card name: official name |
| "Héroe\ Elemental\ Hombre\ Bola\ Loco" | "HÉROE Elemental Mudballman" | quoted card name: official name |
| "Héroe\ Elemental\ Steam\ Healer" | "HÉROE Elemental Steam Healer" | quoted card name: official name |
| "Dragonauta\ Rancer" | "Draconiano de la Lanza" | quoted card name: official name |
| "Cuerpo\ Neblinoso" | "Cuerpo de Niebla" | quoted card name: official name |
| "Dragonauta\ Hacha" | "Draconiano del Hacha" | quoted card name: official name |
| "D\.\ Cuernos\ Blancos" | "Dragón de Cuerno Blanco" | quoted card name: official name |
| "Héroe\ Elemental\ Neo\-Bubbleman" | "HÉROE Elemental Neo-Bubbleman" | quoted card name: official name |
| "Ciber\ Dragón\ Barrera" | "Dragón Ciber Barrera" | quoted card name: official name |
| "Ciber\ Dragón\ Láser" | "Dragón Ciber Láser" | quoted card name: official name |
| "Ficha\ de\ Mártires\ Fantasma" | "Ficha de Mártir Fantasmal" | quoted card name: official name |
| "Rana\ Arbórea" | "RANA Arbórea" | quoted card name: official name |
| "Rana\ Beelze" | "RANA Beelze" | quoted card name: official name |
| "Deceso,\ Rey\ del\ Apocalipsis" | "Demise, Rey del Armagedón" | quoted card name: official name |
| "Rana\ D\.3\.S\." | "RANA D.3.S." | quoted card name: official name |
| "Ficha\ de\ Peluche" | "Ficha Pelusa" | quoted card name: official name |
| "Héroe\ Elemental\ Erikshieler" | "HÉROE Elemental Electrum" | quoted card name: official name |
| "Héroe\ Elemental\ Wild\ Wingman" | "HÉROE Elemental Wild Wingman" | quoted card name: official name |
| "Héroe\ Elemental\ Necroid\ Shaman" | "HÉROE Elemental Necroid Shaman" | quoted card name: official name |
| "Helios\ Duo\ Megistus" | "Helios Dúo Megistus" | quoted card name: official name |
| "Héroe\ Elemental\ Neos" | "HÉROE Elemental Neos" | quoted card name: official name |
| "Diente\ de\ León\ Presumido" | "Diente de León" | quoted card name: official name |
| "Héroe\ Elemental\ Phoenix\ Enforcer" | "HÉROE Elemental Phoenix Enforcer" | quoted card name: official name |
| "Héroe\ Elemental\ Phoenix\ Enforcer\ Brillante" | "HÉROE Elemental Phoenix Enforcer Brillante" | quoted card name: official name |
| "Héroe\ Elemental\ Mariner" | "HÉROE Elemental Mariner" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Doom\ Lord" | "HÉROE del Destino - Doom Lord" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Captain\ Tenacious" | "HÉROE del Destino - Captain Tenacious" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Diamond\ Dude" | "HÉROE del Destino - Diamond Dude" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Dreadmaster" | "HÉROE del Destino - Dreadmaster" | quoted card name: official name |
| "Flash\ HERO!!" | "Flash Hero!!" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Blade\ Master" | "HÉROE del Destino - Blade Master" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Dasher" | "HÉROE del Destino - Dasher" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Double\ Dude" | "HÉROE del Destino - Double Dude" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Defender" | "HÉROE del Destino - Defender" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Fear\ Monger" | "HÉROE del Destino - Fear Monger" | quoted card name: official name |
| "Héroe\ del\ Destino\ \-\ Dogma" | "HÉROE del Destino - Dogma" | quoted card name: official name |
| "Héroe\ Elemental\ Dark\ Neos" | "HÉROE Elemental Dark Neos" | quoted card name: official name |
| "Héroe\ Elemental\ Aqua\ Neos" | "HÉROE Elemental Aqua Neos" | quoted card name: official name |
| "Héroe\ Elemental\ Flare\ Neos" | "HÉROE Elemental Flare Neos" | quoted card name: official name |
| "Bestia\ Fantasma\ Lagarto\ de\ Roca" | "Bestia Fantasma Rock-Lizard" | quoted card name: official name |
| \bEfectos de Blanco\b | Efectos con Objetivo | terminologia ufficiale: objetivo (target) |
| \bblanco\b | objetivo | terminologia ufficiale: objetivo (target) |
| \bblancos\b | objetivos | terminologia ufficiale: objetivo (target) |

### Voci STRINGHE (tutte): dove e perche'
| archivio | membro | indice | cambiamenti | motivo |
|---|---|---|---|---|
| database/duelrecord.ehp | strTbl_s.bin | 130 | 1 sostituzione/i | mancava la traduzione di 'using effects' (diceva 'en batalla' come la riga prima) |
| database/duelrecord.ehp | strTbl_s.bin | 179 | 1 sostituzione/i | l'inglese dice 'Level 4 or lower' |
| database/duelrecord.ehp | strTbl_s.bin | 124 | 1 sostituzione/i | it, fr, de ed en dicono 10 lanci |
| duel/result/result_s.ehp | strTbl.bin | 130 | 1 sostituzione/i | mancava la traduzione di 'using effects' (diceva 'en batalla' come la riga prima) |
| duel/result/result_s.ehp | strTbl.bin | 179 | 1 sostituzione/i | l'inglese dice 'Level 4 or lower' |
| duel/result/result_s.ehp | strTbl.bin | 124 | 1 sostituzione/i | it, fr, de ed en dicono 10 lanci |

### Correzioni puntuali `ui_texts.json`
| file | membro | indice | vecchio | nuovo | motivo |
|---|---|---|---|---|---|

### Elenco completo
**Confronto completo con parole evidenziate: `docs/changes_es/ui_strings_diff.md`.** Dati grezzi: `docs/changes_es/ui_strings.csv`. Prime 40:

| membro | indice | originale | nuovo |
|---|---|---|---|
| ocg_packname_s.bin | 30 | LATAS COLECCCIONABLES 2004 | LATAS COLECCIONABLES 2004 |
| ocg_packname_s.bin | 33 | LATAS COLECCCIONABLES 2005 | LATAS COLECCIONABLES 2005 |
| strTbl_s.bin | 4 | Slifer Red | Slifer Rojo |
| strTbl_s.bin | 5 | Ra Yellow | Ra Amarillo |
| strTbl_s.bin | 6 | Obelisk Blue | Obelisco Azul |
| strTbl_s.bin | 8 | Shadow Riders | Jinetes de la Sombra |
| strTbl_s.bin | 12 | En lo que a duelos se refiere, Jaden es el mejor duelista en Slifer Red, o mejor aún, el mejor duelista entre todos los estudiantes de primer año. Sus dotes naturales son algo con lo que pocos pueden siquiera soñar. El secreto de su fuerza radica en su tenacidad. No importa en el atolladero en que se encuentre, Jaden puede recuperarse con sólo robar una carta.⏎⏎Cada vez que le quedan muy pocas cartas en su mano, ahí está Bubbleman para ayudarle.⏎⏎Se sabe que llena su Deck con muchas cartas de Héroe Elemental, los cuales le recuerdan a los héroes que admiró durante su infancia.⏎⏎Frecuentemente usará fusión de cartas de Héroe Elemental, una táctica en la que es especialmente bueno, en diversas situaciones de duelo.⏎Ese hecho, combinado con su excepcional capacidad para robar, le permite derrotar rápidamente a sus oponentes cuando se encuentra en una racha.⏎⏎En cuanto a su personalidad, Jaden es un adolescente alegre que vive sin preocupaciones, y que piensa que lo más importante de los duelos es divertirse. Al principio no pudo hacer muchos amigos en la estricta Academia de Duelos, pero con los duelos la gente se dio cuenta de su comportamiento sin preocupaciones, y comenzó a hacer más amistad con él.⏎⏎No se sabe lo que piensa de las chicas.⏎En ocasiones una chica puede estar enamorada de él, pero él rara vez, si es que alguna vez lo hace, muestra interés alguno.⏎⏎En lo que se refiere a comida, en realidad no hay nada que le guste o que no le guste. Es feliz comiendo cualquier cosa.⏎ | En lo que a duelos se refiere, Jaden es el mejor duelista en Slifer Rojo, o mejor aún, el mejor duelista entre todos los estudiantes de primer año. Sus dotes naturales son algo con lo que pocos pueden siquiera soñar. El secreto de su fuerza radica en su tenacidad. No importa en qué atolladero se encuentre, Jaden puede recuperarse con sólo robar una carta.⏎⏎Cada vez que le quedan muy pocas cartas en su mano, ahí está Bubbleman para ayudarle.⏎⏎Se sabe que llena su Deck con muchas cartas de Héroe Elemental, los cuales le recuerdan a los héroes que admiró durante su infancia.⏎⏎Frecuentemente usará Fusión de cartas de Héroe Elemental, una táctica en la que es especialmente bueno, en diversas situaciones de duelo.⏎Ese hecho, combinado con su excepcional capacidad para robar, le permite derrotar rápidamente a sus oponentes cuando se encuentra en una racha.⏎⏎En cuanto a su personalidad, Jaden es un adolescente alegre que vive sin preocupaciones, y que piensa que lo más importante de los duelos es divertirse. Al principio no pudo hacer muchos amigos en la estricta Academia de Duelos, pero con los duelos la gente se dio cuenta de su comportamiento sin preocupaciones, y comenzó a hacer más amistad con él.⏎⏎No se sabe lo que piensa de las chicas.⏎En ocasiones una chica puede estar enamorada de él, pero él rara vez, si es que alguna vez lo hace, muestra interés alguno.⏎⏎En lo que se refiere a comida, en realidad no hay nada que le guste o que no le guste. Es feliz comiendo cualquier cosa.⏎ |
| strTbl_s.bin | 13 | Syrus admira mucho a Jaden, y le ve como un hermano mayor. Pero él también tiene un hermano mayor real, y tiende a tener diferentes apodos para cada uno de ellos.⏎⏎Respeta a la gente fuerte, de confiar, pero también se siente un poco inferior entre ella. Quiere ser algún día tan grande como Jaden.⏎⏎Syrus no confía mucho en sus propias habilidades, lo cual parece ser la causa de su constante visión negativa de la vida.⏎Pero por otra parte, con frecuencia puede criticar fuertemente a otras personas.⏎⏎Cuando jugaba duelos lo hacia desde un punto de vista negativo y poco decidido, diciéndose siempre que no podía ganar. Pero desde que conoció a Jaden, su negatividad ha ido cambiando gradualmente hacia un tono más positivo.⏎⏎A Syrus le encanta todo tipo de vehículos, y usa un Deck repleto de cartas Vehicroide (Vehicroide es un tipo de vehículo)⏎A primera vista tiene un encanto atractivo, aniñado, pero en realidad es bastante fuerte.⏎⏎Puede fácilmente perder la cabeza por una chica bonita, pero hasta el momento ninguno de sus enamoramientos se ha materializado en una relación verdadera.⏎⏎La comida favorita de Syrus es servida una vez al mes en la cafetería de Slifer Red.⏎Pero no le cae muy bien la comida muy condimentada.⏎ | Syrus admira mucho a Jaden, y le ve como un hermano mayor. Pero él también tiene un hermano mayor real, y tiende a tener diferentes apodos para cada uno de ellos.⏎⏎Respeta a la gente fuerte, de confianza, pero también se siente un poco inferior entre ella. Quiere ser algún día tan grande como Jaden.⏎⏎Syrus no confía mucho en sus propias habilidades, lo cual parece ser la causa de su constante visión negativa de la vida.⏎Pero por otra parte, con frecuencia puede criticar fuertemente a otras personas.⏎⏎Cuando jugaba duelos lo hacía desde un punto de vista negativo y poco decidido, diciéndose siempre que no podía ganar. Pero desde que conoció a Jaden, su negatividad ha ido cambiando gradualmente hacia un tono más positivo.⏎⏎A Syrus le encanta todo tipo de vehículos, y usa un Deck repleto de cartas Vehicroide (Vehicroide es un tipo de vehículo)⏎A primera vista tiene un encanto atractivo, aniñado, pero en realidad es bastante fuerte.⏎⏎Puede fácilmente perder la cabeza por una chica bonita, pero hasta el momento ninguno de sus enamoramientos se ha materializado en una relación verdadera.⏎⏎La comida favorita de Syrus es servida una vez al mes en la cafetería de Slifer Rojo.⏎Pero no le cae muy bien la comida muy condimentada.⏎ |
| strTbl_s.bin | 14 | Chumley es en realidad mucho más suave de los que su nombre sugiere.⏎Tiene una personalidad simple y pura.⏎Chumley piensa que un duelo debería ser algo más que ganar y perder. Esta filosofía pudiera explicar porqué le retuvieron un año en la rígida Academia de Duelos, sobre la cual siente que no está hecho para ella.⏎Pero esto no significa que sea un mal duelista. Por el contrario, su habilidad le permite escuchar la voz del espíritu del duelo.⏎⏎Fue a Australia con un viaje del colegio y quedó positivamente impresionado por el país. Como resultado, el Deck que usa ahora tiene una cantidad de cartas relacionadas con Australia.⏎⏎Quizá porque extraña a su madre, mantiene una carta de intercambio de una estrella del pop la cual...hace tiempo que vio pasar sus mejores años.⏎⏎Chumley no tiene ninguna comida favorita, pero tiende a evitar las carnes.⏎Por otra parte, come pescado con bastante frecuencia.⏎ | Chumley es en realidad mucho más suave de lo que su nombre sugiere.⏎Tiene una personalidad simple y pura.⏎Chumley piensa que un duelo debería ser algo más que ganar y perder. Esta filosofía pudiera explicar por qué le retuvieron un año en la rígida Academia de Duelos, sobre la cual siente que no está hecho para ella.⏎Pero esto no significa que sea un mal duelista. Por el contrario, su habilidad le permite escuchar la voz del espíritu del duelo.⏎⏎Fue a Australia con un viaje del colegio y quedó positivamente impresionado por el país. Como resultado, el Deck que usa ahora tiene una cantidad de cartas relacionadas con Australia.⏎⏎Quizá porque extraña a su madre, mantiene una carta de intercambio de una estrella del pop la cual... hace tiempo que vio pasar sus mejores años.⏎⏎Chumley no tiene ninguna comida favorita, pero tiende a evitar las carnes.⏎Por otra parte, come pescado con bastante frecuencia.⏎ |
| strTbl_s.bin | 15 | Alexis es la mejor duelista entre las chicas. Es suficientemente fuerte como para también resistir frente a los chicos.⏎En el departamento de belleza, es una chica alucinante a la que algunos llaman la "Madonna de la Academia".⏎Alexis está dotada con inteligencia y belleza, y debido a eso, las otras chicas le envidian.⏎Es valiente por naturaleza. Pero debido a su fuerte deseo de ganar, en ocasiones otros ven cierta aspereza en sus acciones y lenguaje. ⏎⏎Usa un Deck inusual llamado a "Chica Cibernética", formado principalmente por atractivas monstruos femeninas.⏎Una de ellas es "Ciber Patinadora", con un efecto que ha sacado de apuros a Alexis más veces de las que ella puede contar.⏎⏎Alexis todavía no parece interesada en los chicos.⏎En su lugar, ella se jacta de su "amor por el duelo", y este amor puede verse en su juego más que cualquier otra cosa.⏎⏎Le gustan las golosinas y las comidas sanas, pero tiende a mantenerse alejada de comidas que huelen mal. | Alexis es la mejor duelista entre las chicas. Es suficientemente fuerte como para también resistir frente a los chicos.⏎En el departamento de belleza, es una chica alucinante a la que algunos llaman la "Madonna de la Academia".⏎Alexis está dotada con inteligencia y belleza, y debido a eso, las otras chicas le envidian.⏎Es valiente por naturaleza. Pero debido a su fuerte deseo de ganar, en ocasiones otros ven cierta aspereza en sus acciones y lenguaje. ⏎⏎Usa un Deck inusual llamado "Chica Cibernética", formado principalmente por atractivos monstruos femeninos.⏎Una de ellas es "Ciber Patinadora", con un efecto que ha sacado de apuros a Alexis más veces de las que ella puede contar.⏎⏎Alexis todavía no parece interesada en los chicos.⏎En su lugar, ella se jacta de su "amor por el duelo", y este amor puede verse en su juego más que cualquier otra cosa.⏎⏎Le gustan las golosinas y las comidas sanas, pero tiende a mantenerse alejada de comidas que huelen mal. |
| strTbl_s.bin | 16 | Se piensa que Chazz dejó la Academia de Duelos porque su orgullo como duelista de elite quedó hecho añicos. Pero regresó con un espíritu de lucha tenaz.⏎Todavía puede ser autoritario, pero quizás su experiencia en el fondo es la razón por la cual no es tan frío como antes. Parece haber mejorado como ser humano Y gracias a esa mejora, ahora puede escuchar la voz del espíritu.⏎⏎Ha usado muchos Decks, pero ahora principalmente usa el "Trio Ojama".⏎Chazz se concentraba antes en el poder, pero ahora depende más de la técnica.⏎⏎No alberga tanta falta de respeto como antes por aquellos en Slifer Red.⏎⏎A Chazz le gustan los alimentos caros, pero no soporta las verduras. | Se piensa que Chazz dejó la Academia de Duelos porque su orgullo como duelista de elite quedó hecho añicos. Pero regresó con un espíritu de lucha tenaz.⏎Todavía puede ser autoritario, pero quizás su experiencia en el fondo es la razón por la cual no es tan frío como antes. Parece haber mejorado como ser humano. Y gracias a esa mejora, ahora puede escuchar la voz del espíritu.⏎⏎Ha usado muchos Decks, pero ahora principalmente usa el "Trío Ojama".⏎Chazz se concentraba antes en el poder, pero ahora depende más de la técnica.⏎⏎No alberga tanta falta de respeto como antes por aquellos en Slifer Rojo.⏎⏎A Chazz le gustan los alimentos caros, pero no soporta las verduras. |
| strTbl_s.bin | 17 | Un talentoso duelista de primer año del dormitorio Obelisk Blue. Algunos han llegado a llamarle el sucesor de Zane.⏎El más joven del Grupo elite Princeton, es considerado un duelista muy bien situado, y lo mismo en la escala social.⏎Se espera que reciba el título de mejor duelista de parte de sus dos hermanos mayores. Junto con esas grandes expectativas viene una gran arrogancia. Considera que todos tienen un estatus inferior al suyo, y tiene una actitud muy orgullosa.⏎⏎Lo da todo durante un duelo.⏎El duelista promedio no es rival para su estilo agresivo y su fuerza.⏎⏎Quizá a causa de su alto estatus social, es muy considerado con las chicas, hasta un poco feminista.⏎⏎Los duelistas de Slifer Red nunca podrán ser sus amigos a menos que cambie esa actitud presumida.⏎ | Un talentoso duelista de primer año del dormitorio Obelisco Azul. Algunos han llegado a llamarle el sucesor de Zane.⏎El más joven del Grupo elite Princeton, es considerado un duelista muy bien situado, y lo mismo en la escala social.⏎Se espera que reciba el título de mejor duelista de parte de sus dos hermanos mayores. Junto con esas grandes expectativas viene una gran arrogancia. Considera que todos tienen un estatus inferior al suyo, y tiene una actitud muy orgullosa.⏎⏎Lo da todo durante un duelo.⏎El duelista promedio no es rival para su estilo agresivo y su fuerza.⏎⏎Quizá a causa de su alto estatus social, es muy considerado con las chicas, hasta un poco feminista.⏎⏎Los duelistas de Slifer Rojo nunca podrán ser sus amigos a menos que cambie esa actitud presumida.⏎ |
| strTbl_s.bin | 18 | Bastión es un estudiante brillante. Logró la mejor puntuación en el examen de admisión a la Academia.⏎Fue el hombre que más cerca estuvo de convertirse en miembro de Obelisk Blue.⏎Bastión tiene un lado muy serio, pero también puede ser muy generoso. Aunque tiene un rango superior al de los duelistas Slifer Red, no les mira como inferiores.⏎⏎En su tiempo libre, Bastión frecuentemente hace cálculos en su mente, y luego apunta las fórmulas resultantes en lo  primero que tenga a mano.⏎Como resultado, las paredes de su habitación están cubiertas con números y fórmulas, como si fueran pintadas. Hasta las cartas están garabateadas con fórmulas. Este hábito extraño frecuentemente saldrá a relucir durante un duelo. Incluso llegará hasta a calcular el estilo de juego de su oponente, aplicando teorías o cálculos a sus propias tácticas para duelos.⏎Mientras Jaden tiene un don natural que le convierte en un duelista excepcional, la excelencia de Bastión es el resultado de la persistencia y del esfuerzo.⏎⏎Clama tener seis Decks diferentes con seis Atributos, y que los usa dependiendo de su oponente. Dice que cada Deck está perfectamente equilibrado.⏎Pero por alguna razón rara vez se le ve jugando en un duelo.⏎⏎Bastión tiene mucho potencial teniendo en cuenta su gran inteligencia, personalidad y habilidades en los duelos. Pero tiene un punto débil, su "falta de presencia" hace que los otros le vuelvan la espalda.⏎⏎Dice que no le interesan las chicas, pero cuando ellas le piden ayuda hace lo imposible.⏎Bastión añade cartas con chicas guapas con aspecto sumiso a su Deck, pero en la vida real prefiere a las mujeres fuertes.⏎⏎Le gusta comer verduras, y parece coger muy en serio su salud.⏎Por otra parte, no le gustan las frutas, y al parecer odia las golosinas. | Bastión es un estudiante brillante. Logró la mejor puntuación en el examen de admisión a la Academia.⏎Fue el hombre que más cerca estuvo de convertirse en miembro de Obelisco Azul.⏎Bastión tiene un lado muy serio, pero también puede ser muy generoso. Aunque tiene un rango superior al de los duelistas Slifer Rojo, no les mira como inferiores.⏎⏎En su tiempo libre, Bastión frecuentemente hace cálculos en su mente, y luego apunta las fórmulas resultantes en lo primero que tenga a mano.⏎Como resultado, las paredes de su habitación están cubiertas con números y fórmulas, como si fueran pintadas. Hasta las cartas están garabateadas con fórmulas. Este hábito extraño frecuentemente saldrá a relucir durante un duelo. Incluso llegará hasta a calcular el estilo de juego de su oponente, aplicando teorías o cálculos a sus propias tácticas para duelos.⏎Mientras Jaden tiene un don natural que le convierte en un duelista excepcional, la excelencia de Bastión es el resultado de la persistencia y del esfuerzo.⏎⏎Afirma tener seis Decks diferentes con seis Atributos, y que los usa dependiendo de su oponente. Dice que cada Deck está perfectamente equilibrado.⏎Pero por alguna razón rara vez se le ve jugando en un duelo.⏎⏎Bastión tiene mucho potencial teniendo en cuenta su gran inteligencia, personalidad y habilidades en los duelos. Pero tiene un punto débil, su "falta de presencia" hace que los otros le vuelvan la espalda.⏎⏎Dice que no le interesan las chicas, pero cuando ellas le piden ayuda hace lo imposible.⏎Bastión añade cartas con chicas guapas con aspecto sumiso a su Deck, pero en la vida real prefiere a las mujeres fuertes.⏎⏎Le gusta comer verduras, y parece coger muy en serio su salud.⏎Por otra parte, no le gustan las frutas, y al parecer odia las golosinas. |
| strTbl_s.bin | 20 | Como profesor del dormitorio para chicos de Obelisk Blue, Vellian Crowler está a cargo de los mejores duelistas de la Academia.⏎Tiene una forma de hablar muy excéntrica.⏎⏎Vellian simboliza la filosofía rígida y obsesionada con la habilidad de la Academia de Duelos, tratando con favoritismo a los que sacan mejores notas, a la vez que es intolerante con los que no pueden seguir ese ritmo. Ha estado vigilando de cerca a Jaden Yuki, de Slifer Red, y ha estado tramando varias formas de conseguir que lo expulsen de la Academia.⏎⏎En los duelos, usa una "Chaqueta de Duelo". Al parecer "todo el que ingrese con éxito en la academia puede comprar una", pero nadie que no se Vellian ha usado alguna vez una. ⏎⏎Usa un Deck lleno de cartas Mecanismos Antiguos – "Mecanismo Antiguo" es un tipo de maquinaria antigua.⏎Su carta principal es Golem de Mecanismo Antiguo", una carta tan potente que se le conoce como "Rompe Reglas".⏎⏎Como su apariencia hace suponer, Vellian ama las cosas de alta calidad, y la comida está entre ellas. | Como profesor del dormitorio para chicos de Obelisco Azul, Vellian Crowler está a cargo de los mejores duelistas de la Academia.⏎Tiene una forma de hablar muy excéntrica.⏎⏎Vellian simboliza la filosofía rígida y obsesionada con la habilidad de la Academia de Duelos, tratando con favoritismo a los que sacan mejores notas, a la vez que es intolerante con los que no pueden seguir ese ritmo. Ha estado vigilando de cerca a Jaden Yuki, de Slifer Rojo, y ha estado tramando varias formas de conseguir que lo expulsen de la Academia.⏎⏎En los duelos, usa una "Chaqueta de Duelo". Al parecer "todo el que ingrese con éxito en la academia puede comprar una", pero nadie que no sea Vellian ha usado jamás una. ⏎⏎Usa un Deck lleno de cartas Mecanismos Antiguos – "Mecanismo Antiguo" es un tipo de maquinaria antigua.⏎Su carta principal es "Golem de Mecanismo Antiguo", una carta tan potente que se le conoce como "Rompe Reglas".⏎⏎Como su apariencia hace suponer, Vellian ama las cosas de alta calidad, y la comida está entre ellas. |
| strTbl_s.bin | 21 | Lyman Banner es un profesor de alquimia y el jefe del dormitorio Slifer Red. ⏎⏎Su personalidad relajada y su tono de voz tranquilo hace que sea difícil determinar el tipo de persona que realmente es.⏎⏎Lyman raramente, o probablemente nunca, ha participado en un duelo porque se especializa en alquimia, que es el arte de sacar algo de nada. Nadie sabe que tipo de Deck usaría.⏎⏎Aunque mucho de su vida está envuelta en el misterio, para todos es evidente que le encantan los gatos.⏎⏎Hasta su tipo de comida favorita es un misterio.⏎ | Lyman Banner es un profesor de alquimia y el jefe del dormitorio Slifer Rojo. ⏎⏎Su personalidad relajada y su tono de voz tranquilo hace que sea difícil determinar el tipo de persona que realmente es.⏎⏎Lyman raramente, o probablemente nunca, ha participado en un duelo porque se especializa en alquimia, que es el arte de sacar algo de nada. Nadie sabe qué tipo de Deck usaría.⏎⏎Aunque mucho de su vida está envuelta en el misterio, para todos es evidente que le encantan los gatos.⏎⏎Hasta su tipo de comida favorita es un misterio.⏎ |
| strTbl_s.bin | 23 | Camula es miembro de los Shadow Riders – un grupo buscando las Llaves de los Espíritus.⏎También es una vampiresa.⏎⏎El Deck de Camula está formado por cartas Tipo Zombi, como los vampiros. Manipula a los murciélagos con sus ojos rojos para que echen una miradita al Deck de su oponente. De esta forma ella puede ajustar sus tácticas correspondientemente. También se sabe que no tiene reparos en usar Cartas Prohibidas y cuando de tener duelos se trata se traga su orgullo.⏎⏎Disfruta haciendo muñecos de aquellos que pierden con ella en los duelos, y los añade a su colección retorcida. Pero si no le tiene particular cariño a alguien convertido en muñeco, no lo agregará a su colección. Asusta pensar lo que sucede después de eso.⏎ | Camula es miembro de los Jinetes de la Sombra – un grupo buscando las Llaves de los Espíritus.⏎También es una vampiresa.⏎⏎El Deck de Camula está formado por cartas Tipo Zombi, como los vampiros. Manipula a los murciélagos con sus ojos rojos para que echen una miradita al Deck de su oponente. De esta forma ella puede ajustar sus tácticas correspondientemente. También se sabe que no tiene reparos en usar Cartas Prohibidas y cuando de tener duelos se trata se traga su orgullo.⏎⏎Disfruta haciendo muñecos de aquellos que pierden con ella en los duelos, y los añade a su colección retorcida. Pero si no le tiene particular cariño a alguien convertido en muñeco, no lo agregará a su colección. Asusta pensar lo que sucede después de eso.⏎ |
| strTbl_s.bin | 24 | Tania es miembro de los Shadow Riders – un grupo buscando las Llaves de los Espíritus.⏎También es una amazona.⏎⏎Aunque muchos de los Shadow Ridres son muy maliciosos, Tania es alegre y tiene una personalidad imparcial.⏎Para ella tiene más prioridad encontrar un hombre que sea su esposo que buscar las Llaves de los Espíritus.⏎⏎Siendo una amazona, su Deck es muy apropiado, ya que está formado por cartas de Amazonas. Se especializa en duelos potentes cuando usa estas cartas.⏎⏎Todos quieren saber que le pasará al hombre que se convierta en su prometido.⏎ | Tania es miembro de los Jinetes de la Sombra – un grupo buscando las Llaves de los Espíritus.⏎También es una amazona.⏎⏎Aunque muchos de los Jinetes de la Sombra son muy maliciosos, Tania es alegre y tiene una personalidad imparcial.⏎Para ella tiene más prioridad encontrar un hombre que sea su esposo que buscar las Llaves de los Espíritus.⏎⏎Siendo una amazona, su Deck es muy apropiado, ya que está formado por cartas de Amazonas. Se especializa en duelos potentes cuando usa estas cartas.⏎⏎Todos quieren saber qué le pasará al hombre que se convierta en su prometido.⏎ |
| strTbl_s.bin | 25 | Don Zaloog es miembro de los Shadow Riders – un grupo buscando las Llaves de los Espíritus.⏎También es el líder de una banda de ladrones llamada la Banda del Escorpión Oscuro.⏎Don Zaloog se ha disfrazado y se ha metido furtivamente en la Academia de Duelos. La gente dice que es un criminal más listo de lo que aparenta.⏎⏎Durante un duelo, su Deck está formado principalmente por cartas Banda del Escorpión Oscuro. Las combinaciones de esas cartas causarán un verdadero desorden en la mano del oponente. | Don Zaloog es miembro de los Jinetes de la Sombra – un grupo buscando las Llaves de los Espíritus.⏎También es el líder de una banda de ladrones llamada la Banda del Escorpión Oscuro.⏎Don Zaloog se ha disfrazado y se ha metido furtivamente en la Academia de Duelos. La gente dice que es un criminal más listo de lo que aparenta.⏎⏎Durante un duelo, su Deck está formado principalmente por cartas Banda del Escorpión Oscuro. Las combinaciones de esas cartas causarán un verdadero desorden en la mano del oponente. |
| strTbl_s.bin | 26 | Un faraón y duelista experto que no ha perdido un duelo en miles de años.⏎Fue invocado desde su sueño profundo y se convirtió en miembro de los Shadow Riders.⏎Aunque es un faraón, todavía es sólo un niño.⏎Todavía es infantil en muchos aspectos, como su odio irracional a perder.⏎⏎Como ha vivido más de mil años, las cartas que usa son bastante antiguas.⏎ | Un faraón y duelista experto que no ha perdido un duelo en miles de años.⏎Fue invocado desde su sueño profundo y se convirtió en miembro de los Jinetes de la Sombra.⏎Aunque es un faraón, todavía es sólo un niño.⏎Todavía es infantil en muchos aspectos, como su odio irracional a perder.⏎⏎Como ha vivido más de mil años, las cartas que usa son bastante antiguas.⏎ |
| strTbl_s.bin | 27 | Titán Oscuro fue hecho renacer como un verdadero "Duelista Shadow".⏎Es miembro de los Shadow Riders – un grupo buscando las Llaves de los Espíritus.⏎⏎Aunque se ha convertido en un verdadero Duelista Shadow, su apariencia no ha cambiado mucho.⏎Desde el principio se parecía mucho a un Duelista Shadow.⏎⏎Siempre ha usado muchas cartas Archidemonio, pero ahora ellas son más poderosas que nunca.⏎ | Titán Oscuro fue hecho renacer como un verdadero "Duelista de la Sombra".⏎Es miembro de los Jinetes de la Sombra – un grupo buscando las Llaves de los Espíritus.⏎⏎Aunque se ha convertido en un verdadero Duelista de la Sombra, su apariencia no ha cambiado mucho.⏎Desde el principio se parecía mucho a un Duelista de la Sombra.⏎⏎Siempre ha usado muchas cartas Archidemonio, pero ahora ellas son más poderosas que nunca.⏎ |
| strTbl_s.bin | 28 | Se autodenomina el "Duelista Shadow".⏎Durante un juego de las sombras, este duelista sin corazón usará un Objeto del Milenio para enviar a su oponente, que ha perdido, al pozo de la muerte.⏎⏎Titán se gana la vida con juegos de las sombras. Acepta solicitudes y combate contra cualquiera que le hayan contratado para combatir.⏎Exige a cada cliente meses de salario, sin excepciones.⏎Siendo un Duelista Shadow, su Deck está compuesto principalmente por cartas Archifiend.⏎⏎Es muy profesional, y nunca queda en posición vulnerable. Ni siquiera durante una fracción de segundo.⏎Está constantemente alerta, incluso cuando estrecha la mano. | Se autodenomina el "Duelista de la Sombra".⏎Durante un juego de las sombras, este duelista sin corazón usará un Objeto del Milenio para enviar a su oponente, que ha perdido, al pozo de la muerte.⏎⏎Titán se gana la vida con juegos de las sombras. Acepta solicitudes y combate contra cualquiera que le hayan contratado para combatir.⏎Exige a cada cliente meses de salario, sin excepciones.⏎Siendo un Duelista de la Sombra, su Deck está compuesto principalmente por cartas Archidemonio.⏎⏎Es muy profesional, y nunca queda en posición vulnerable. Ni siquiera durante una fracción de segundo.⏎Está constantemente alerta, incluso cuando estrecha la mano. |
| strTbl_s.bin | 31 | Era un estudiante Obelisk Blue.⏎Sobresalió en sus estudios, pero su técnica de robo era débil.⏎Esta debilidad le obligó a vivir una vida solitaria en las montañas.⏎Allí se sometió a un entrenamiento riguroso para perfeccionar sus habilidades para robar.⏎⏎Su robo ha mejorado como resultado del entrenamiento, pero como durante ese tiempo en las montañas se concentró solamente en ese aspecto, han menguado sus otras habilidades como duelista.⏎ | Era un estudiante Obelisco Azul.⏎Sobresalió en sus estudios, pero su técnica de robo era débil.⏎Esta debilidad le obligó a vivir una vida solitaria en las montañas.⏎Allí se sometió a un entrenamiento riguroso para perfeccionar sus habilidades para robar.⏎⏎Su robo ha mejorado como resultado del entrenamiento, pero como durante ese tiempo en las montañas se concentró solamente en ese aspecto, han menguado sus otras habilidades como duelista.⏎ |
| strTbl_s.bin | 33 | Jasmine es Fanática A - una fanática y seguidora de Alexis.⏎Es la chica a la cual recurrir para información sobre la Academia (principalmente cotilleo), y mantiene a Alexis al día sobre los últimos sucesos en el campus Pero Alexis no parece estar muy interesada en esta "información".⏎⏎Jasmine usa un Deck Arpía – quizá debido a su admiración por las mujeres fuertes. | Jasmine es Fanática A - una fanática y seguidora de Alexis.⏎Es la chica a la cual recurrir para información sobre la Academia (principalmente cotilleo), y mantiene a Alexis al día sobre los últimos sucesos en el campus. Pero Alexis no parece estar muy interesada en esta "información".⏎⏎Jasmine usa un Deck Arpía – quizá debido a su admiración por las mujeres fuertes. |
| strTbl_s.bin | 34 | Mindy es Fanática B - una fanática y seguidora de Alexis.⏎Su conducta y manera de hablar son las de una dama, pero con frecuencia lo que tiene que decir es bastante venenoso.⏎Está muy interesada en calificar a los chicos y hasta lleva un diario "Calificación de Chicos".⏎⏎Mindy usa un Deck lleno de jóvenes apuestos, llamado el "Deck de los Bonitos".⏎Pudo entrar en Obelisk Blue usando un Deck que huele a Fanática, por eso la gente normalmente piensa que debe ser una duelista bastante talentosa. | Mindy es Fanática B - una fanática y seguidora de Alexis.⏎Su conducta y manera de hablar son las de una dama, pero con frecuencia lo que tiene que decir es bastante venenoso.⏎Está muy interesada en calificar a los chicos y hasta lleva un diario "Calificación de Chicos".⏎⏎Mindy usa un Deck lleno de jóvenes apuestos, llamado el "Deck de los Bonitos".⏎Pudo entrar en Obelisco Azul usando un Deck que huele a Fanática, por eso la gente normalmente piensa que debe ser una duelista bastante talentosa. |
| strTbl_s.bin | 36 | Un chico matriculado en Slifer Red.⏎⏎Tiene una figura estilizada, más propia de una chica.⏎⏎Habla como debe hablar un chico, pero a veces su amaneramiento es como el de una chica.⏎⏎Aunque es un chico, nunca se le encuentra con otros chicos en el vestuario, y siempre se ducha solo, como lo haría una chica. Si no le conociera, diría que este chico es en realidad una chica.⏎ | Un chico matriculado en Slifer Rojo.⏎⏎Tiene una figura estilizada, más propia de una chica.⏎⏎Habla como debe hablar un chico, pero a veces su amaneramiento es como el de una chica.⏎⏎Aunque es un chico, nunca se le encuentra con otros chicos en el vestuario, y siempre se ducha solo, como lo haría una chica. Si no le conociera, diría que este chico es en realidad una chica.⏎ |
| strTbl_s.bin | 37 | Una chica que persigue a Zane.⏎Hizo el examen de entrada a la Academia sólo para poder matricular y verle todos los días.⏎Su personalidad puede describirse como obsesiva. Definitivamente cae dentro de las celosas.⏎En realidad tan celosa que exagerará y confundirá a los que la rodean.⏎⏎Su Deck refleja los sentimientos de una doncella enamorada. Espera algún día dar a conocer sus sentimientos a esa persona tan especial mediante un duelo.⏎Su carta principal se llama "Doncella Enamorada". En realidad es un monstruo que captura a su oponente.⏎⏎Y como ella es la única en 5to curso, no puede entrar en el nivel de secundaria de la Academia de Duelos. | Una chica que persigue a Zane.⏎Hizo el examen de entrada a la Academia sólo para poder matricularse y verle todos los días.⏎Su personalidad puede describirse como obsesiva. Definitivamente cae dentro de las celosas.⏎En realidad tan celosa que exagerará y confundirá a los que la rodean.⏎⏎Su Deck refleja los sentimientos de una doncella enamorada. Espera algún día dar a conocer sus sentimientos a esa persona tan especial mediante un duelo.⏎Su carta principal se llama "Doncella Enamorada". En realidad es un monstruo que captura a su oponente.⏎⏎Y como ella es la única en 5to curso, no puede entrar en el nivel de secundaria de la Academia de Duelos. |
| strTbl_s.bin | 40 | Un espíritu de carta.⏎Es alegre, energética y le encanta la diversión.⏎Siempre quiere formar parte de cualquier cosa divertida que pase en la Academia de Duelos.⏎⏎Es una duelista con mucho talento, y puede resistir frente a una chica del dormitorio Obelisk Blue.⏎El espíritu en sí mismo está incluido en el Deck que ella usa.⏎ | Un espíritu de carta.⏎Es alegre, energética y le encanta la diversión.⏎Siempre quiere formar parte de cualquier cosa divertida que pase en la Academia de Duelos.⏎⏎Es una duelista con mucho talento, y puede resistir frente a una chica del dormitorio Obelisco Azul.⏎El espíritu en sí mismo está incluido en el Deck que ella usa.⏎ |
| strTbl_s.bin | 48 | Fonda es supervisora en el dormitorio femenino Obelisk Blue.⏎También es la instructora del gimnasio y la enfermera en la Academia de Duelos.⏎Muchos estudiantes han fingido lesiones nada más que para verle.⏎⏎Fonda es en realidad una duelista bastante buena y disfruta de un duelo ocasional en su tiempo libre.⏎Ama todo lo bello, y esto se refleja en su Deck, repleto de cartas bonitas.⏎ | Fonda es supervisora en el dormitorio femenino Obelisco Azul.⏎También es la instructora del gimnasio y la enfermera en la Academia de Duelos.⏎Muchos estudiantes han fingido lesiones nada más que para verle.⏎⏎Fonda es en realidad una duelista bastante buena y disfruta de un duelo ocasional en su tiempo libre.⏎Ama todo lo bello, y esto se refleja en su Deck, repleto de cartas bonitas.⏎ |
| strTbl_s.bin | 49 | Un apostador errante.⏎Debe llevarse bien con la Dama Suerte, ya que no ha perdido ni una vez.⏎Al menos, ese es el rumor, pero en realidad se jacta de que no ha perdido porque se mantiene jugando hasta que gana.⏎Después de oír los rumores sobre los Shadow Riders, vino a la Academia de Duelos esperando entrenar para luchar contra ellos.⏎También tiene una relación especial con Alexis, quizás una señal del destino..⏎⏎Usa un Deck de Apostador lleno de cartas relacionadas con las apuestas.⏎Dice que no hay nada más bello que apostarlo todo a los números correctos en una partida de dados o de monedas.⏎⏎Su nombre verdadero es Pierre, pero se enfada cuando alguien le llama así.⏎ | Un apostador errante.⏎Debe llevarse bien con la Dama Suerte, ya que no ha perdido ni una vez.⏎Al menos, ese es el rumor, pero en realidad se jacta de que no ha perdido porque se mantiene jugando hasta que gana.⏎Después de oír los rumores sobre los Jinetes de la Sombra, vino a la Academia de Duelos esperando entrenar para luchar contra ellos.⏎También tiene una relación especial con Alexis, quizás una señal del destino...⏎⏎Usa un Deck de Apostador lleno de cartas relacionadas con las apuestas.⏎Dice que no hay nada más bello que apostarlo todo a los números correctos en una partida de dados o de monedas.⏎⏎Su nombre verdadero es Pierre, pero se enfada cuando alguien le llama así.⏎ |
| strTbl_s.bin | 50 | Una Asaltante Veladora de Tumbas que saluda al héroe con un juego de las sombras una vez que le transporta en el tiempo desde una ruina antigua.⏎⏎Algunas personas han sido transportadas desde el pasado, y ella está enamorada de una de ellas.⏎ | Una Asaltante del Cuidador de Tumba que saluda al héroe con un juego de las sombras una vez que le transporta en el tiempo desde una ruina antigua.⏎⏎Algunas personas han sido transportadas desde el pasado, y ella está enamorada de una de ellas.⏎ |
| strTbl_s.bin | 51 | Miembro de los Shadow Riders – un grupo buscando las Llaves de los Espíritus.⏎Practica el arte de los "juegos de las sombras", que sella dentro de una carta el alma de perdedor.⏎Se desconoce su verdadera identidad.⏎⏎Usa un Deck Dragón que tiene como a "Dragón de Oscuridad de Ojos Rojos" como carta principal. ⏎Está intentando envolver en llamas al mundo. | Miembro de los Jinetes de la Sombra – un grupo buscando las Llaves de los Espíritus.⏎Practica el arte de los "juegos de las sombras", que sella dentro de una carta el alma del perdedor.⏎Se desconoce su verdadera identidad.⏎⏎Usa un Deck Dragón que tiene a "Dragón de Oscuridad de Ojos Rojos" como carta principal. ⏎Está intentando envolver en llamas al mundo. |
| strTbl_s.bin | 52 | Perfil de Sheppard del Principio | Perfil del Rector Sheppard |
| strTbl_s.bin | 78 | Invocación de Tributo | Invocación por Sacrificio |
| strTbl_s.bin | 25 | Número de Invocaciones de Tributo | Número de Invocaciones por Sacrificio |
| strTbl_s.bin | 36 | Daño directo causado con Monstruos Cómicos | Daño directo causado con Monstruos Toon |
| strTbl_s.bin | 74 | Bonus Invocación de Tributo | Bonus Invocación por Sacrificio |
| strTbl_s.bin | 90 | Bonus Afortunada | Bonus Suerte |
| strTbl_s.bin | 92 | Bonus Union | Bonus Unión |
| strTbl_s.bin | 100 | Bonus Criado de Cráneo | Bonus Sirviente de la Calavera |
| strTbl_s.bin | 104 | Invocado "Dragón Definitivo de Ojos Azules" | Invocado "Dragón de Ojos Azules Definitivo" |

(... altre 289 righe nel CSV)

## A6. Etichetta [CARTA MAGIA] / [CARTA TRAPPOLA] della carta grande nel duello

In tutti i `duel/basic_<regione><lingua>.ehp` l'etichetta era in inglese (hash `c2268340`): `apply_to_iso.py` la sostituisce con `card_spell_trap.gim` di `field/always_<lingua>_<lingua>.ehp` (hash `9622cd75`).

| archivio | membro | hash originale | hash nuovo |
|---|---|---|---|
| /PSP_GAME/USRDIR/duel/basic_bs.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |
| /PSP_GAME/USRDIR/duel/basic_fs.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |
| /PSP_GAME/USRDIR/duel/basic_gs.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |
| /PSP_GAME/USRDIR/duel/basic_is.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |
| /PSP_GAME/USRDIR/duel/basic_ss.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |
| /PSP_GAME/USRDIR/duel/basic_us.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |

## A7. File della ISO toccati e dettagli tecnici

179 archivi `.ehp` risultano diversi dall'originale (tutte le lingue insieme, perche' la ISO e' unica; elenco in `docs/changes_es/touched_files.csv`). Gli altri file (video, audio, eseguibile `EBOOT.BIN`, `PARAM.SFO`) sono identici. Differenze tecniche non testuali: `*-ptrs.txt` (offset assoluti dei membri, ricalcolati quando una tabella cambia lunghezza), nuova posizione degli archivi in fondo alla ISO.

## A8. Cosa NON si puo' cambiare (limiti del gioco)

- Il **nome del parlante** nella casella del dialogo (es. "Preside Sheppard"/"Cancelliere" in italiano, "Doyen Sheppard" in francese, "Rector Sheppard" in spagnolo) sta nell'EBOOT cifrato: non modificabile.
- Testi disegnati dal gioco con il suo font (dialoghi, nomi, descrizioni nel deck, menu a tendina, tastiera di sistema, schermata di scelta lingua) non sono sostituibili dal texture pack: si cambiano solo nella ISO.
- Le 438 texture di mappa/sfondi non sono sostituite (il gioco ne cambia la palette): limite del pack di MikeyMK, non del nostro lavoro.

---

# B. TEXTURE PACK

## B1. Provenienza e struttura

Base: **Yu-Gi-Oh! GX Tag Force 1 HD Remastered** di **MikeyMK** (pack USA `ULUS10136`) e carte HD di **chrisfand**, adattati alla ISO europea `ULES00600`. Il progetto non ridistribuisce il pack di terzi (`PERMESSI_AUTORI.md`): il patcher se lo fa dare dall'utente. Il nostro lavoro: (1) rimappare gli **hash** del pack USA su quelli EU (`tools/gen_ini.py`), (2) rifare nella lingua carte e scritte dell'interfaccia, (3) correggere i testi, (4) `upscale_extra` per le texture non coperte.

PPSSPP riconosce una texture dall'**hash dei suoi pixel** (xxhash dei dati, `gim.data_hash`); ogni riga del `textures.ini` e' `0000000000000000<hash8> = percorso/png`. I PNG sono **4x** l'originale e ridisegnano esattamente la stessa area. Texture identiche tra lingue hanno lo stesso hash: la sostituzione vale per tutte (vedi `docs/TEXTURE_INVENTORY.md`).

### Struttura reale (da `docs/changes_es/pack_structure.csv`)
| radice | cartella | file | MB | contenuto |
|---|---|---|---|---|
| ULES00600 (pack di base) | LEGGIMI.txt | 1 | 0.0 |  |
| ULES00600 (pack di base) | _CHOOSE YOUR CARD STYLE/ | 3 | 7.8 | mikeymk, official_english, official_japanese |
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
| moduli/es | cards/ | 5675 | 1024.6 | frame, large_es, small_es, tiny_es |
| moduli/es | es.ini | 1 | 0.01 |  |
| moduli/es | intro/ | 2 | 0.4 | title_screen |
| moduli/es | ui_es/ | 95 | 8.2 | icon_sheets, icon_sheets.ini, result_letters, result_letters.ini, menu_lists, menu_lists.ini, deck_screens, deck_screens.ini, recipe_screens, recipe_screens.ini ... |

Ogni lingua tranne l'italiano e' un **modulo** (`PSP/TEXTURES/modules/es`) da comporre sopra il pack di base con `tools/compose_pack.py BASE MODULI CARD_DIR OUT es [--copia]`: copia il base e **solo** le cartelle `cards`, `intro` e `ui_es` del modulo (hard link o copia), poi `module_ini.py` riscrive i `textures.ini`: le righe delle carte localizzate puntano a `cards/small_es`/`large_es` e le righe di `es.ini` **sostituiscono** quelle del base con la stessa chiave (hash).

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
| `_CHOOSE YOUR CARD STYLE` | 3 `textures.ini` alternativi (mikeymk, official_english, official_japanese): copiare uno al posto di `textures.ini` per cambiare lo stile delle carte |

## B2. Immagini delle carte

Cartelle della lingua: `frame` (2 file), `large_es` (2833 file), `small_es` (2833 file), `tiny_es` (7 file). Ogni carta ha una **piccola HD** (nome + descrizione + tipo, rigenerata con font liberi OFL: XCharter Bold per nomi/tipo/etichette, Libre Baskerville per gli effetti, Newsreader Italic per i Normali, PT Serif Caption per Magie/Trappole, Charis SIL per i glifi mancanti) e una **grande HD** (solo il nome sulla cornice). In piu': la **tabella degli attributi** con le parole della lingua (`cards/frame/icons_attribute_race_<l>.png`, `attributes.py`), l'**etichetta Magia/Trappola** (`icons_spell_trap_<l>.png`, `label_it.py` / `extract_labels.py` -> `dati/label_eu_<codice>_128x32.png`) e l'**atlante delle miniature** del deck (`tiny_<l>`, `tiny_atlas.py` + `tiny_fragment.py`).

Quando cambia il testo di una carta (sezione A2) vanno rigenerate le sue immagini: **624 carte** nel spagnolo. Elenco in `docs/changes_es/card_images.csv`. Comando: `python tools/generate_language.py fr PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` (senza ID rigenera tutte: 2.833 + 2.833, ~930 MB).

Tipografia: spazio non separabile prima di `: ; ! ?` e virgolette « ».

## B3. Interfaccia HD in spagnolo (`ui_es`)

**87 texture** (`docs/changes_es/ui_textures.csv`: file, hash PPSSPP, famiglia, script, dimensioni originale/HD, neutra/specifica, origine nella ISO). Per famiglia: icon_sheets 3, result_letters 22, menu_lists 6, deck_screens 14, recipe_screens 11, vs_screen 14, duel_texts 11, tutorial 6. Di queste 0 sono neutre (stesso hash in tutte le lingue) e 87 specifiche. Ogni famiglia ha uno script in `tools/ui_textures/<famiglia>.py` (lettura `TF1_LANG`): ridisegna le scritte texture per texture partendo dall'originale a bassa risoluzione della ISO e dallo stile del pack inglese; stessa area e stesse posizioni (il gioco ritaglia da rettangoli fissi); un font/peso/linea di base/ombra per scritta; font liberi (`alt_font.py`).

| famiglia | texture | script | archivio ISO sorgente | testi della lingua |
|---|---|---|---|---|
| icon_sheets | 3 | `tools/ui_textures/icon_sheets.py` | deck/all_s.ehp, shop/all_s.ehp, field/always_* | `icon04`, `s_pack` (AGOTADO), `panel` (frammento "rados"); `pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01` hanno lo stesso hash dell’inglese |
| result_letters | 22 | `tools/ui_textures/result_letters.py` | duel/basic_ss.ehp | HAS GANADO (HASGNDO) · HAS PERDIDO (HASPERDIO, 9 tessere) · EMPATE (EMPAT) + silhouette |
| menu_lists | 6 | `tools/ui_textures/menu_lists.py` | title_menu/title_menu_s.ehp, duel/result/result_s.ehp, field/always_bri_<cod>.ehp | MENÚ PRINCIPAL · INTRODUCE EL NOMBRE · LISTA DE CARTAS DESCARGADAS · DUELO ACERTIJO · OPCIONES · AJUSTES DEL IDIOMA · AGRUPAR LISTA... · RESULTADO DEL DUELO · PRESIONA EL BOTÓN START · GANAS/EMPATE/PIERDES · Domingo...Sábado · Mayo Julio Junio Agosto · Días / para el torneo / de · AM / PM |
| deck_screens | 14 | `tools/ui_textures/deck_screens.py` | deck/all_s.ehp, labo/*.ehp, shop/all_s.ehp | Tronco ×3, Fusión, Alquiler ×4, Laboratorio, Conversor ×2, "Tipos de carta en posesión", "Cartas compradas" (+ frammento), ACEPTAR |
| recipe_screens | 11 | `tools/ui_textures/recipe_screens.py` | deck/recipe_view_s.ehp, title_menu/title_menu_s.ehp, database/limitlist.ehp | Personaje / Usuario / Recetas descargadas / Recetas de personaje / Recetas de usuario / Limitada / Semi-Limitada / Prohibida / Cambiar |
| vs_screen | 14 | `tools/ui_textures/vs_screen.py` | duel/start/start_e.ehp (membri _s), start_all.ehp, start_s.ehp | DUELO / NORMAL / TAG · SEGUNDO EN SALIR / PRIMERO EN SALIR · 1ra/2da/3ra vuelta · Modo Individual / Modo Combate · GANAS/PIERDES/EMPATE · JUGADOR 1 / JUGADOR 2 · JUGADOR |
| duel_texts | 11 | `tools/ui_textures/duel_texts.py` | duel/basic_ss.ehp | Cadena · TURNO DEL SIGUIENTE JUGADOR (il taglio tra le due texture passa dentro una lettera, come nell’originale) · COMENZAR DUELO · Ataque Directo · TURNO e `card_icon03` coperti da texture già presenti (stesso hash dell’italiano / `upscale_extra`) |
| tutorial | 6 | `tools/ui_textures/tutorial.py` | tutorial/tutorial_s.ehp (tuto_duelimg01..06) | Tu oponente ha declarado la batalla. / ¿activar el efecto de la carta? · SÍ/NO · 5 cartine; dialogo a 2 righe ma riquadro più largo |

Regole di qualita' (valgono per ogni lingua): lettere regolari, mai deformate una per una; stessa area dell'originale; niente sfocature; il testo e' quello dell'originale della lingua (si correggono solo errori evidenti: residui di altre lingue, accenti); pixel art **non** levigata senza conferma; geometrie sempre misurate sull'originale.

### Testi disegnati: originale -> HD
Tabella letta a occhio, texture per texture: `docs/changes_es/texture_texts_es.md`. Differenze rispetto all'originale: `DEMARRER` -> `DÉMARRER`, `SCAMBIA`/`Scambia` -> `ÉCHANGE`/`Échange`, `2è/3è round` -> `2e/3e round`; tutto il resto riscrive le stesse parole.

### Elenco di ogni texture
(tutte le 87 righe, da `ui_textures.csv`)

| file nel pack | hash | famiglia | originale px | HD px | tipo | origine ISO |
|---|---|---|---|---|---|---|
| ui_es/icon_sheets/all_s__icon04.png | 57ec7a66 | icon_sheets | 128x128 | 512x512 | SPECIFICA | deck/all_s.ehp:icon04.gim |
| ui_es/icon_sheets/all_s__panel.png | 6c431a2a | icon_sheets | 256x256 | 1024x1024 | SPECIFICA | shop/all_s.ehp:panel.gim |
| ui_es/icon_sheets/all_s__s_pack.png | 7a7314e5 | icon_sheets | 256x256 | 1024x1024 | SPECIFICA | shop/all_s.ehp:s_pack.gim |
| ui_es/result_letters/basic_ss__duel_draw100002.png | ba388fb8 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_draw100002.gim; duel/basic_fs.ehp:duel_draw100002.gim; duel/basic_gs.ehp:duel_draw100002.gim |
| ui_es/result_letters/basic_ss__duel_draw100004.png | 396a68f8 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_draw100004.gim; duel/basic_fs.ehp:duel_draw100004.gim; duel/basic_gs.ehp:duel_draw100004.gim |
| ui_es/result_letters/basic_ss__duel_draw100006.png | 14389066 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_draw100006.gim; duel/basic_fs.ehp:duel_draw100006.gim; duel/basic_gs.ehp:duel_draw100006.gim |
| ui_es/result_letters/basic_ss__duel_draw100008.png | 17a7a350 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_draw100008.gim; duel/basic_fs.ehp:duel_draw100008.gim; duel/basic_gs.ehp:duel_draw100008.gim |
| ui_es/result_letters/basic_ss__duel_draw100010.png | 3d47af74 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_draw100010.gim; duel/basic_fs.ehp:duel_draw100010.gim; duel/basic_gs.ehp:duel_draw100010.gim |
| ui_es/result_letters/basic_ss__duel_lose100002.png | 1cb4482c | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_lose100002.gim; duel/basic_fs.ehp:duel_lose100002.gim; duel/basic_gs.ehp:duel_lose100002.gim |
| ui_es/result_letters/basic_ss__duel_lose100004.png | ecb90266 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_lose100004.gim; duel/basic_fs.ehp:duel_lose100004.gim; duel/basic_gs.ehp:duel_lose100004.gim |
| ui_es/result_letters/basic_ss__duel_lose100006.png | 7d290a32 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_lose100006.gim; duel/basic_fs.ehp:duel_lose100006.gim; duel/basic_gs.ehp:duel_lose100006.gim |
| ui_es/result_letters/basic_ss__duel_lose100008.png | 3733b351 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_lose100008.gim; duel/basic_fs.ehp:duel_lose100008.gim; duel/basic_gs.ehp:duel_lose100008.gim |
| ui_es/result_letters/basic_ss__duel_lose100010.png | ffc4d8e5 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_lose100010.gim; duel/basic_fs.ehp:duel_lose100010.gim; duel/basic_gs.ehp:duel_lose100010.gim |
| ui_es/result_letters/basic_ss__duel_lose100012.png | 302162eb | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_lose100012.gim; duel/basic_fs.ehp:duel_lose100012.gim; duel/basic_gs.ehp:duel_lose100012.gim |
| ui_es/result_letters/basic_ss__duel_lose100014.png | 9aa5d99c | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_lose100014.gim; duel/basic_fs.ehp:duel_lose100014.gim; duel/basic_gs.ehp:duel_lose100014.gim |
| ui_es/result_letters/basic_ss__duel_lose100016.png | 00b99210 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_lose100016.gim; duel/basic_fs.ehp:duel_lose100016.gim; duel/basic_gs.ehp:duel_lose100016.gim |
| ui_es/result_letters/basic_ss__duel_lose100018.png | 09cc5268 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_lose100018.gim; duel/basic_fs.ehp:duel_lose100018.gim; duel/basic_gs.ehp:duel_lose100018.gim |
| ui_es/result_letters/basic_ss__duel_win100002.png | c130b02b | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_win100002.gim; duel/basic_fs.ehp:duel_win100002.gim; duel/basic_gs.ehp:duel_win100002.gim |
| ui_es/result_letters/basic_ss__duel_win100004.png | e40b4f5a | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_win100004.gim; duel/basic_fs.ehp:duel_win100004.gim; duel/basic_gs.ehp:duel_win100004.gim |
| ui_es/result_letters/basic_ss__duel_win100006.png | b602abed | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_win100006.gim; duel/basic_fs.ehp:duel_win100006.gim; duel/basic_gs.ehp:duel_win100006.gim |
| ui_es/result_letters/basic_ss__duel_win100008.png | 5d42a4d6 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_win100008.gim; duel/basic_fs.ehp:duel_win100008.gim; duel/basic_gs.ehp:duel_win100008.gim |
| ui_es/result_letters/basic_ss__duel_win100010.png | 7346cdd7 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_win100010.gim; duel/basic_fs.ehp:duel_win100010.gim; duel/basic_gs.ehp:duel_win100010.gim |
| ui_es/result_letters/basic_ss__duel_win100012.png | 3b9ae395 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_win100012.gim; duel/basic_fs.ehp:duel_win100012.gim; duel/basic_gs.ehp:duel_win100012.gim |
| ui_es/result_letters/basic_ss__duel_win100014.png | 5a1e30a6 | result_letters | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:duel_win100014.gim; duel/basic_fs.ehp:duel_win100014.gim; duel/basic_gs.ehp:duel_win100014.gim |
| ui_es/result_letters/basic_ss__duel_win100016.png | e22c31d5 | result_letters | 64x32 | 256x128 | SPECIFICA | duel/basic_bs.ehp:duel_win100016.gim; duel/basic_fs.ehp:duel_win100016.gim; duel/basic_gs.ehp:duel_win100016.gim |
| ui_es/menu_lists/always_bri_spa__story_sys02.png | 92c0609f | menu_lists | 256x128 | 1024x512 | SPECIFICA | field/always_bri_spa.ehp:story_sys02.gim; field/always_fra_spa.ehp:story_sys02.gim; field/always_ger_spa.ehp:story_sys02.gim |
| ui_es/menu_lists/result_s__menu01.png | 6a156d48 | menu_lists | 256x64 | 1024x256 | SPECIFICA | duel/result/result_s.ehp:menu01.gim |
| ui_es/menu_lists/result_s__menu02.png | ffd0d26a | menu_lists | 256x128 | 1024x512 | SPECIFICA | duel/result/result_s.ehp:menu02.gim |
| ui_es/menu_lists/title_menu_s__m_menu_title01.png | 2589c36d | menu_lists | 256x128 | 1024x512 | SPECIFICA | title_menu/title_menu_s.ehp:m_menu_title01.gim |
| ui_es/menu_lists/title_menu_s__press_start0003.png | 45d9a888 | menu_lists | 256x16 | 1024x64 | SPECIFICA | title_menu/title_menu_s.ehp:press_start0003.gim |
| ui_es/menu_lists/title_menu_s__trnsmt02.png | 87428289 | menu_lists | 256x256 | 1024x1024 | SPECIFICA | title_menu/title_menu_s.ehp:trnsmt02.gim |
| ui_es/deck_screens/all_s__d_window00008.png | 308698d0 | deck_screens | 128x32 | 512x128 | SPECIFICA | deck/all_s.ehp:d_window00008.gim |
| ui_es/deck_screens/all_s__d_window00016.png | 47084696 | deck_screens | 64x32 | 256x128 | SPECIFICA | deck/all_s.ehp:d_window00016.gim |
| ui_es/deck_screens/all_s__d_window00033.png | ac8667a7 | deck_screens | 256x32 | 1024x128 | SPECIFICA | deck/all_s.ehp:d_window00033.gim |
| ui_es/deck_screens/all_s__d_window00051.png | 4b97edef | deck_screens | 64x32 | 256x128 | SPECIFICA | deck/all_s.ehp:d_window00051.gim |
| ui_es/deck_screens/all_s__d_window00062.png | 18b02d40 | deck_screens | 128x32 | 512x128 | SPECIFICA | deck/all_s.ehp:d_window00062.gim; labo/conv_machine.ehp:window_s0016.gim; title_menu/title_menu_s.ehp:t_window0015.gim |
| ui_es/deck_screens/all_s__d_window00101.png | 91eb2bb5 | deck_screens | 64x32 | 256x128 | SPECIFICA | deck/all_s.ehp:d_window00101.gim; labo/rental.ehp:window_s0008.gim |
| ui_es/deck_screens/all_s__tab_title.png | 6fe1264c | deck_screens | 256x32 | 1024x128 | SPECIFICA | shop/all_s.ehp:tab_title.gim |
| ui_es/deck_screens/conv_machine__window_s0009.png | 24cf8aaf | deck_screens | 128x32 | 512x128 | SPECIFICA | labo/conv_machine.ehp:window_s0009.gim; labo/conv_machine.ehp:window_s0026.gim |
| ui_es/deck_screens/conv_machine__window_s0016.png | 18b02d40 | deck_screens | 128x32 | 512x128 | SPECIFICA | deck/all_s.ehp:d_window00062.gim; labo/conv_machine.ehp:window_s0016.gim; title_menu/title_menu_s.ehp:t_window0015.gim |
| ui_es/deck_screens/conv_machine__window_s0026.png | 24cf8aaf | deck_screens | 128x32 | 512x128 | SPECIFICA | labo/conv_machine.ehp:window_s0009.gim; labo/conv_machine.ehp:window_s0026.gim |
| ui_es/deck_screens/password__key_s0027.png | 5d6635f4 | deck_screens | 128x32 | 512x128 | SPECIFICA | labo/password.ehp:key_s0027.gim |
| ui_es/deck_screens/rental__window_s0008.png | 91eb2bb5 | deck_screens | 64x32 | 256x128 | SPECIFICA | deck/all_s.ehp:d_window00101.gim; labo/rental.ehp:window_s0008.gim |
| ui_es/deck_screens/rental__window_s0015.png | fee49520 | deck_screens | 128x32 | 512x128 | SPECIFICA | labo/rental.ehp:window_i0015.gim; labo/rental.ehp:window_s0015.gim |
| ui_es/deck_screens/rental__window_s0026.png | 16a6572b | deck_screens | 64x32 | 256x128 | SPECIFICA | labo/rental.ehp:window_s0026.gim |
| ui_es/recipe_screens/limitlist__window_s0002.png | 7d80a6c6 | recipe_screens | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_s0002.gim |
| ui_es/recipe_screens/limitlist__window_s0004.png | 1d7d2421 | recipe_screens | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_s0004.gim |
| ui_es/recipe_screens/limitlist__window_s0012.png | 8c7ebe78 | recipe_screens | 128x32 | 512x128 | SPECIFICA | database/limitlist.ehp:window_s0012.gim |
| ui_es/recipe_screens/recipe_view_s__recipe010008.png | c5c45bb7 | recipe_screens | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_s.ehp:recipe010008.gim; title_menu/title_menu_s.ehp:recipe_sel00002.gim |
| ui_es/recipe_screens/recipe_view_s__recipe010015.png | b6e6f744 | recipe_screens | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_s.ehp:recipe010015.gim; title_menu/title_menu_s.ehp:recipe_sel00009.gim |
| ui_es/recipe_screens/recipe_view_s__recipe010027.png | 72f7f26a | recipe_screens | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_s.ehp:recipe010027.gim; title_menu/title_menu_s.ehp:recipe_sel00020.gim |
| ui_es/recipe_screens/recipe_view_s__recipe010029.png | 285b971c | recipe_screens | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_s.ehp:recipe010029.gim; title_menu/title_menu_s.ehp:recipe_sel00022.gim |
| ui_es/recipe_screens/recipe_view_s__recipe010031.png | c70a1e0a | recipe_screens | 128x32 | 512x128 | SPECIFICA | deck/recipe_view_s.ehp:recipe010031.gim; title_menu/title_menu_s.ehp:recipe_sel00024.gim |
| ui_es/recipe_screens/title_menu_s__recipe_sel00033.png | 6bb39c40 | recipe_screens | 128x32 | 512x128 | SPECIFICA | title_menu/title_menu_s.ehp:recipe_sel00033.gim |
| ui_es/recipe_screens/title_menu_s__t_window0008.png | 117e2298 | recipe_screens | 64x32 | 256x128 | SPECIFICA | title_menu/title_menu_s.ehp:t_window0008.gim |
| ui_es/recipe_screens/title_menu_s__t_window0026.png | 01673953 | recipe_screens | 64x32 | 256x128 | SPECIFICA | title_menu/title_menu_s.ehp:t_window0026.gim |
| ui_es/vs_screen/start_all__jyanken20_s0005.png | a9897630 | vs_screen | 256x32 | 1024x128 | SPECIFICA | duel/start/start_all.ehp:jyanken20_s0005.gim; duel/start/start_e.ehp:jyanken20_s0005.gim; duel/start/start_f.ehp:jyanken20_s0005.gim |
| ui_es/vs_screen/start_all__jyanken20_s0007.png | 7368d31c | vs_screen | 256x32 | 1024x128 | SPECIFICA | duel/start/start_all.ehp:jyanken20_s0007.gim; duel/start/start_e.ehp:jyanken20_s0007.gim; duel/start/start_f.ehp:jyanken20_s0007.gim |
| ui_es/vs_screen/start_all__vs_much1_s0001.png | ef845abc | vs_screen | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much1_s0001.gim; duel/start/start_e.ehp:vs_much1_s0001.gim; duel/start/start_f.ehp:vs_much1_s0001.gim |
| ui_es/vs_screen/start_all__vs_much2_s0001.png | ea46529a | vs_screen | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much2_s0001.gim; duel/start/start_e.ehp:vs_much2_s0001.gim; duel/start/start_f.ehp:vs_much2_s0001.gim |
| ui_es/vs_screen/start_all__vs_much3_s0001.png | 386e4f79 | vs_screen | 128x16 | 512x64 | SPECIFICA | duel/start/start_all.ehp:vs_much3_s0001.gim; duel/start/start_e.ehp:vs_much3_s0001.gim; duel/start/start_f.ehp:vs_much3_s0001.gim |
| ui_es/vs_screen/start_e__d_menu01_s.png | a77116f2 | vs_screen | 256x256 | 1024x1024 | SPECIFICA | duel/start/start_e.ehp:d_menu01_s.gim; duel/start/start_f.ehp:d_menu01_s.gim; duel/start/start_g.ehp:d_menu01_s.gim |
| ui_es/vs_screen/start_e__vs_bg01_1_s0005.png | 939ffe1b | vs_screen | 256x32 | 1024x128 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_s0005.gim; duel/start/start_f.ehp:vs_bg01_1_s0005.gim; duel/start/start_g.ehp:vs_bg01_1_s0005.gim |
| ui_es/vs_screen/start_e__vs_bg01_1_s0007.png | 3ab04908 | vs_screen | 256x64 | 1024x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_s0007.gim; duel/start/start_f.ehp:vs_bg01_1_s0007.gim; duel/start/start_g.ehp:vs_bg01_1_s0007.gim |
| ui_es/vs_screen/start_e__vs_bg01_1_s0008.png | 41ab9f3e | vs_screen | 256x64 | 1024x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_s0008.gim; duel/start/start_f.ehp:vs_bg01_1_s0008.gim; duel/start/start_g.ehp:vs_bg01_1_s0008.gim |
| ui_es/vs_screen/start_e__vs_bg01_1_s0012.png | ed29c0fe | vs_screen | 128x32 | 512x128 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_s0012.gim; duel/start/start_f.ehp:vs_bg01_1_s0012.gim; duel/start/start_g.ehp:vs_bg01_1_s0012.gim |
| ui_es/vs_screen/start_e__vs_bg01_1_s0014.png | 8788a7c8 | vs_screen | 128x64 | 512x256 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_1_s0014.gim; duel/start/start_f.ehp:vs_bg01_1_s0014.gim; duel/start/start_g.ehp:vs_bg01_1_s0014.gim |
| ui_es/vs_screen/start_e__vs_bg01_2_s0001.png | 5796698d | vs_screen | 128x16 | 512x64 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_2_s0001.gim; duel/start/start_f.ehp:vs_bg01_2_s0001.gim; duel/start/start_g.ehp:vs_bg01_2_s0001.gim |
| ui_es/vs_screen/start_e__vs_bg01_2_s0004.png | f081a08d | vs_screen | 128x16 | 512x64 | SPECIFICA | duel/start/start_e.ehp:vs_bg01_2_s0004.gim; duel/start/start_f.ehp:vs_bg01_2_s0004.gim; duel/start/start_g.ehp:vs_bg01_2_s0004.gim |
| ui_es/vs_screen/start_s__jnk_card01.png | a2fc7092 | vs_screen | 512x256 | 2048x1024 | SPECIFICA | duel/start/start_s.ehp:jnk_card01.gim |
| ui_es/duel_texts/basic_ss__chain010003.png | c7fd7035 | duel_texts | 64x32 | 256x128 | SPECIFICA | duel/basic_bs.ehp:chain010003.gim; duel/basic_fs.ehp:chain010003.gim; duel/basic_gs.ehp:chain010003.gim |
| ui_es/duel_texts/basic_ss__chain010005.png | abaeb83c | duel_texts | 128x32 | 512x128 | SPECIFICA | duel/basic_bs.ehp:chain010005.gim; duel/basic_fs.ehp:chain010005.gim; duel/basic_gs.ehp:chain010005.gim |
| ui_es/duel_texts/basic_ss__dilect_atk00001.png | 880d6d24 | duel_texts | 256x32 | 1024x128 | SPECIFICA | duel/basic_bs.ehp:dilect_atk00001.gim; duel/basic_fs.ehp:dilect_atk00001.gim; duel/basic_gs.ehp:dilect_atk00001.gim |
| ui_es/duel_texts/basic_ss__dilect_atk00003.png | d8591359 | duel_texts | 128x32 | 512x128 | SPECIFICA | duel/basic_bs.ehp:dilect_atk00003.gim; duel/basic_fs.ehp:dilect_atk00003.gim; duel/basic_gs.ehp:dilect_atk00003.gim |
| ui_es/duel_texts/basic_ss__next_player0001.png | 9d78973f | duel_texts | 64x32 | 256x128 | SPECIFICA | duel/basic_bs.ehp:next_player0001.gim; duel/basic_fs.ehp:next_player0001.gim; duel/basic_gs.ehp:next_player0001.gim |
| ui_es/duel_texts/basic_ss__next_player0002.png | 1e0eff3f | duel_texts | 256x32 | 1024x128 | SPECIFICA | duel/basic_bs.ehp:next_player0002.gim; duel/basic_fs.ehp:next_player0002.gim; duel/basic_gs.ehp:next_player0002.gim |
| ui_es/duel_texts/basic_ss__next_player0004.png | 6d3897cf | duel_texts | 64x32 | 256x128 | SPECIFICA | duel/basic_bs.ehp:next_player0004.gim; duel/basic_fs.ehp:next_player0004.gim; duel/basic_gs.ehp:next_player0004.gim |
| ui_es/duel_texts/basic_ss__next_player0005.png | 4021e68f | duel_texts | 256x32 | 1024x128 | SPECIFICA | duel/basic_bs.ehp:next_player0005.gim; duel/basic_fs.ehp:next_player0005.gim; duel/basic_gs.ehp:next_player0005.gim |
| ui_es/duel_texts/basic_ss__start_duel10001.png | 692edb74 | duel_texts | 64x64 | 256x256 | SPECIFICA | duel/basic_bs.ehp:start_duel10001.gim; duel/basic_fs.ehp:start_duel10001.gim; duel/basic_gs.ehp:start_duel10001.gim |
| ui_es/duel_texts/basic_ss__start_duel10002.png | 8ea8857e | duel_texts | 256x64 | 1024x256 | SPECIFICA | duel/basic_bs.ehp:start_duel10002.gim; duel/basic_fs.ehp:start_duel10002.gim; duel/basic_gs.ehp:start_duel10002.gim |
| ui_es/duel_texts/basic_ss__start_duel10005.png | 0e4dc413 | duel_texts | 128x32 | 512x128 | SPECIFICA | duel/basic_bs.ehp:start_duel10005.gim; duel/basic_fs.ehp:start_duel10005.gim; duel/basic_gs.ehp:start_duel10005.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg01.png | ab860e12 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_s.ehp:tuto_duelimg01.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg02.png | 18e1d210 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_s.ehp:tuto_duelimg02.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg03.png | e3014dad | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_s.ehp:tuto_duelimg03.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg04.png | d046d2fe | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_s.ehp:tuto_duelimg04.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg05.png | 3536db89 | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_s.ehp:tuto_duelimg05.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg06.png | d1ec1c4a | tutorial | 256x256 | 1024x1024 | SPECIFICA | tutorial/tutorial_s.ehp:tuto_duelimg06.gim |

### Texture che restano come l'originale
`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `parts` sono fogli di icone in pixel art (con NEU/NEW): restano com'erano, coperti dall'ingrandimento `upscale_extra` come nelle altre lingue; il testo non e' stato cambiato. Le texture neutre vengono dal pack di base. In spagnolo anche `score-top` (TURNO) ha lo stesso hash dell'italiano e `card_icon03` e' in `upscale_extra`.

## B4. Il foglio dei numeri del duello (`card_icon03`)

Foglio unico con cifre LP, tempo, tasti e moltiplicatori; hash diverso per lingua. Ricetta scelta dall'utente (`tools/ui_textures/icon03_languages.py`, rilanciare con `--apply`):
- righe 0-180 (cifre piccole e segni, tasti arancioni 1/2/3, cifre grandi 0-9 con "LP", cifre piccole 0-9): **dal pack USA**, pixel art netta;
- celle in cui il gioco europeo differisce dal pack USA (spunta nera, palla grigia, pillola vuota, parola del tempo): **pixel originali ingranditi 4x senza sfumare**; parola del tempo **TIEMPO**; la pillola arancione ("Single" nel pack USA) resta **vuota**;
- righe >= 181 (moltiplicatori x1..x12, icone, carte, frecce): dal foglio italiano gia' nel pack (`tools/data/card_icon03_base_it.png`);
- le celle europee si incollano **solo nella loro fascia** di righe (altrimenti rovinano la parte alta delle cifre grandi).

File: it -> `ui_it/duel_texts/basic_ii__card_icon03.png` (hash 376925c7); fr -> `upscale_extra/3e5482fd.png`; en ee0c44c3; de ffe309a6; es 859eea2b. Anteprime in `confronti/icon03/`.

## B5. Targa del titolo

`python tools/ui_textures/mystic_tomato_title.py es` genera 2 PNG (`542eff79685c434d`, `705176739829dcf5`, tessere 18 e 19 del fondale di 20 tessere 128x64 `title_menu_i.ehp: main_title00001..00020`) con la carta 4930 nella lingua + la formula "versione" + la bandiera, font PT Sans Bold: **"EDICIÓN TOMATE MÍSTICO"**. La targa **va inclusa solo per la lingua scelta** (vive in `moduli/es/intro/title_screen/`); il pack di base originale ha le tessere senza banner. File in questo pack: `moduli/es/intro/title_screen/00000000542eff79685c434d.png`, `moduli/es/intro/title_screen/00000000705176739829dcf5.png`.

## B6. `textures.ini` e composizione

`tools/gen_ini.py TOOLS US_INI CARD_DIR OUT_INI i=it +extra_it.ini +ui_it.ini +dati/upscale_extra.ini` converte il `textures.ini` USA in quello EU: le voci non-carta restano (texture neutre = stessi hash); le voci carta sono rigenerate dagli archivi `card/*.cip` EU per le 5 lingue (`i=it` rimappa `cards/large/X.png` -> `cards/large_it/X.png`); aggiunge l'etichetta Magia/Trappola (`extra_it.ini`), le righe `ui_it` e `upscale_extra.ini`. Si fa anche per i 3 stili carte. Se gli stessi pixel esistono in piu' lingue vince la prima in `e i f g s` (per questo atlante, banner e tabella attributi sono "uno per installazione").

Righe `ui_es` nel `es.ini`: 87. Frequenza dei prefissi: `docs/changes_es/ini_lines.csv`. Controllo: ogni riga `ui_es/...` deve puntare a un file esistente e non devono esserci hash duplicati.

## B7. Installazione e impostazioni

PC: copiare `ULES00600` in `<PPSSPP>/PSP/TEXTURES/` (Android: `textures.zip` in `.../TEXTURES/ULES00600/`, senza estrarlo; rigenerare lo zip con le correzioni). Impostazioni: **Sostituisci texture ON**, risoluzione di rendering **4x**, lingua del gioco = lingua del modulo (la lingua e' scritta nel **salvataggio**). Dopo aver cambiato un solo PNG basta copiarlo e riavviare PPSSPP (cache). Per provare i testi usare la ISO `_definitiva`.

---

# C. SCELTE EDITORIALI

- **Rector Sheppard** (come nei dialoghi) nelle schede e nelle mappe ("Oficina del Rector"); dormitori **Slifer Rojo, Ra Amarillo, Obelisco Azul**; **Jinetes de la Sombra**; "Habitación" al posto di "Alójese" (Room).
- Sake/shochu e abito da cameriera come nelle altre lingue (`st01_t01/Scr003E`), `st02_t01/Scr101E` ruotato; "Sirviente de la Calavera", "Toon", "Archidemonio", "Trío Ojama" e accenti dei nomi come sulle carte.
- Opzioni: "EN/FUERADE" -> "ON/OFF"; messaggi del titolo ("nuevos datos de juego"), lezioni del tutorial ("le turno" -> "es el turno de", tasti x/o scambiati, codici colore chiusi), paragrafo finale dei Duelos Tag tradotto (era troncato/in inglese).
- Termini lasciati come nel gioco: "Invocación por Sacrificio", "Tributar", "Efecto de Blanco", "Tronco" (domande aperte in `docs/changes_es/open_questions_es.md`).
- Foglio numeri: cifre/LP dal pack USA, x1..x12 dal foglio italiano, parola del tempo TIEMPO.

### Voci del registro delle scelte per questa lingua (`tools/data/editorial_choices.json`)
| id | originale | corretto | ereditata | motivo |
|---|---|---|---|---|
| st01_t01/Scr003E#146 | Mi padre es el dueño de una⏎empresa de salsa picante. | Mi padre es el dueño de una⏎destilería de sake. | no | sake al posto di salsa piccante (fedele al giapponese: la famiglia di Chumley fa sake) |
| st01_t01/Scr003E#147 | En la última paga me envió⏎un poco de salsa picante.⏎Te haré un descuento razonable.⏎¿Quieres...? | En la última paga me envió⏎un poco de shochu.⏎Te haré un descuento razonable.⏎¿Quieres...? | no | shochu al posto di salsa piccante |
| st01_t01/Scr003E#150 | Mi padre es el dueño de una⏎empresa de salsa picante. | Mi padre es el dueño de una⏎destilería de sake. | no | come 146 |
| st01_t01/Scr003E#151 | En la última paga me envió⏎un poco de salsa picante.⏎Te haré un descuento razonable.⏎¿Quieres...? | En la última paga me envió⏎un poco de shochu.⏎Te haré un descuento razonable.⏎¿Quieres...? | no | come 147 |
| st01_t01/Scr003E#163 | Vaya... Lo has conseguido.⏎Es 《C026_2》...⏎¡Y lleva un bikini! | Vaya... Lo has conseguido.⏎Es 《C026_2》...⏎¡Y va vestida de criada! | no | abito da cameriera al posto di bikini (giapponese: メイド服) |
| st01_t01/Scr003E#168 | Vaya... Lo has conseguido.⏎Es 《C026_2》...⏎¡Y lleva un bikini! | Vaya... Lo has conseguido.⏎Es 《C026_2》...⏎¡Y va vestida de criada! | no | come 163 |
| st01_t01/Scr003E#188 | Bueno, supongo que hago⏎mis pinitos... | None | si | solo italiano: "sto sbavando" era un errore di traduzione (giapponese: "non sono poi così bravo") |
| st01_t01/Scr003E#189 | Oye,⏎¿puedes hacerme un dibujo?⏎¡Dibújame a 《C026_2》 en bikini! | Oye,⏎¿puedes hacerme un dibujo?⏎¡Dibújame a 《C026_2》 vestida de criada! | no | abito da cameriera al posto di bikini |
| st01_t01/Scr003E#191 | ¡Ten, puedes usar éste! | ¡Ten, usa este traje de criada! | no | Syrus passa un abito da cameriera come modello (メイド服): col bikini la battuta non aveva senso |
| st01_t01/Scr003E#194 | Bueno, supongo que hago⏎mis pinitos... | None | si | come 188 |
| st01_t01/Scr003E#195 | Oye,⏎¿puedes hacerme un dibujo?⏎¡Dibújame a 《C026_2》 en bikini! | Oye,⏎¿puedes hacerme un dibujo?⏎¡Dibújame a 《C026_2》 vestida de criada! | no | come 189 |
| st01_t01/Scr003E#197 | ¡Ten, puedes usar éste! | ¡Ten, usa este traje de criada! | no | come 191 |

Altre scelte e la rilettura delle frasi dei duelli: `docs/EDITORIAL_CHOICES.md`.

# D. VERIFICA IN GIOCO

- **Visti in gioco** (ISO `_definitiva` + modulo `es`, nuovo gioco in spagnolo, 2026-10-12): scelta lingua, titolo con targa "EDICIÓN TOMATE MÍSTICO" e "PRESIONA EL BOTÓN START", Juego Nuevo/Continuar, "INTRODUCE EL NOMBRE", messaggi di sistema del salvataggio, Menú Principal HD, Lista de Duelistas, editor del deck (linguette Deck/Fusión/Side/Tronco, "Tipos de carta en posesión"), Opciones (ON/OFF, aiuti).
- **Non visti** (solo letti e confrontati con l'originale nei fogli di confronto): duello (Cadena, Ataque Directo, fine duello, VS, sasso-carta-forbici), tutorial e lezioni, negozio, laboratorio, calendario, carte con testo nuovo, dialoghi corretti della storia, frasi dei duelli.

# E. COME RIGENERARE TUTTO

```
# ISO (tutte le lingue insieme)
python tools/corrections/build_dialogues.py es
python tools/corrections/generate_card_corrections.py es CARDINFO_es.ehp          # carte
python tools/corrections/apply_to_iso.py PSP/GAME/ULES00600_..._EUR.iso PSP/GAME/ULES00600_..._EUR_definitiva.iso
# immagini
python tools/generate_language.py fr PACK CARDINFO US_INI CLEAN_DIR OUT [ID...]
TF1_LANG=es python tools/ui_textures/<famiglia>.py USRDIR PACK_US <modulo>      # per ognuna delle 8 famiglie (intera!)
python tools/ui_textures/icon03_languages.py --apply ; python tools/ui_textures/mystic_tomato_title.py es
python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules USRDIR/card OUT es --copia
# questo documento
python tools/analysis/document_changes.py ISO_ORIG ISO_DEF es docs/changes_es
python tools/analysis/document_pack.py ISO_ORIG es docs/changes_es
python tools/analysis/text_comparisons.py es
python tools/analysis/write_changes_document.py es
```
Input esterni da avere (controlla che esistano): ISO originale, USRDIR estratta (`tools/analysis/extract_usrdir.py`), pack USA di MikeyMK `ULUS10136` (in una cartella fuori dal progetto).

# F. LIMITI E PUNTI APERTI

- Domande dell'utente risolte il 2026-10-12 (nomi di carte rotti corretti sul nome ufficiale, Kaiba Corporation, Duelo maiuscolo, Rector, Sacrificio al posto di Tributo): `docs/changes_es/open_questions_es.md`.
- 14 texture spagnole senza HD (frammenti senza testo: `recipe_sel`, `t_window0002`, `limitlist window_s0010/20`, `jyanken100005/7`, `recipe010011`, `bg_base_cloud02`) restano come l'originale.
- `textures.zip` Android: non fatto; nessuna prova su telefono. I testi disegnati nelle texture sono in `docs/changes_es/texture_texts_es.md` (letti a occhio).
- Il nome del parlante nella casella del dialogo non e' modificabile (EBOOT cifrato).
