# CHANGES OF THE MYSTIC TOMATO VERSION FOR SPANISH

**Complete** document of everything the "Mystic Tomato Version" changes for spanish: (A) the **direct changes to the ISO**, (B) the **texture pack** (how it is made, what it contains, how it is composed), (C) the editorial choices, (D) what has been verified in game and what has not, (E) how to regenerate everything.

**This file is generated** by `tools/analysis/write_changes_document.py es` from the real data: byte-by-byte comparison between the original ISO `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` and the corrected ISO `..._definitiva.iso` (`document_changes.py`) and a scan of the pack (`document_pack.py`). The row-by-row lists are in `docs/changes_es/*.csv` (`;` separator, UTF-8 with BOM, line breaks as `⏎`): they are the **exact list** of every change. Regenerate everything after each modification.

For the general method and for the other languages: `docs/NEW_LANGUAGE_GUIDE.md`; technical details of the scripts: `docs/TUTORIAL.md`; decisions: `docs/EDITORIAL_CHOICES.md`; neutral/specific textures: `docs/TEXTURE_INVENTORY.md`.

## Index
- A. Changes to the ISO: A1 overview · A2 cards · A3 dialogues · A4 duel sentences · A5 interface strings · A6 Spell/Trap label · A7 touched files and technical details · A8 what cannot be changed
- B. Texture pack: B1 origin and structure · B2 card images · B3 HD interface (`ui_es`) · B4 number sheet (`card_icon03`) · B5 title plate · B6 textures.ini and composition · B7 installation
- C. Editorial choices · D. In-game verification · E. How to regenerate · F. Limits and open points

---

# A. CHANGES TO THE ISO

## A1. Overview

The original ISO is **never modified**. `tools/corrections/apply_to_iso.py ISO_ORIG ISO_OUT [languages]` creates a copy in which some `.ehp` archives are rewritten. If an archive grows (longer text) it is **put again at the end of the ISO** in a new sector and its entry in the ISO9660 directory is reassigned (`pycdlib`); for this reason the `_definitiva` ISO weighs ~909 MB (the original ~761 MB). **Always run it without a list of languages (or with all of them)**: with a single language it overwrites the others.

| What | Quantity (derived from the ISO comparison) | Where the data lives | CSV file |
|---|---|---|---|
| Cards with changed text (name and/or description) | 624 cards (720 fields) | `tools/data/card_corrections_es.json` from `tools/corrections/rules_es.py` | cards.csv |
| Story dialogue lines | 601 lines | `tools/data/dialogue_touchups_es.json` (+ base) | dialogues.csv |
| Duelist sentences in duels | 55 unique sentences (75 entries in all the archives) | `tools/data/duel_line_corrections_es.json` | duel_lines.csv |
| Interface strings (help, cards, records, tutorial, menus...) | 329 unique strings (1169 entries, 81 archives) | `tools/corrections/string_rules_es.py` + `tools/data/ui_texts.json` | ui_strings.csv |
| Images replaced inside the ISO | 6 ([SPELL CARD/TRAP CARD] label of the large card) | `apply_to_iso.py` (copies the language's `card_spell_trap.gim`) | iso_images.csv |
| ISO files touched (`.ehp` archives) | 179 | - | touched_files.csv |
| Other technical differences (recomputed offsets) | 254 | - | other.csv |

## A2. Card texts

Archive: `PSP_GAME/USRDIR/duelsys/cardinfo_fra.ehp` (tables `CARD_Name_*`, `CARD_Desc_*`, `CARD_Indx_*`). **624 cards** have a modified name and/or description. Only **objective errors** are corrected (typos, accents, apostrophes, spaces, inconsistent capitalization, agreement, fixed plurals, leftovers from other languages); official names and the game's terminology are not touched.

How: every card was read (it: 2,479 texts, one by one; fr: audit against the official database + reading). Rules in `tools/corrections/rules_es.py`: **441 global rules** (regexes applied to the names and descriptions of all the cards) and **201 per-card corrections** (`PER_CARD`: id, field, old, new, reason; the old text must exist exactly). `generate_card_corrections.py es CARDINFO` (writes `card_corrections_{L}.json` starting from the original texts) produces the json; `apply_to_iso` writes it into the ISO; the HD images of the touched cards are regenerated (section B2).

### Global rules (all)
| pattern (regex) | replacement | reason |
|---|---|---|
| \bañadela\b | añádela | imperative with pronoun: missing accent |
| \bAñadela\b | Añádela | imperative with pronoun: missing accent |
| \bañadelas\b | añádelas | imperative with pronoun: missing accent |
| \bAñadelas\b | Añádelas | imperative with pronoun: missing accent |
| \bañadelo\b | añádelo | imperative with pronoun: missing accent |
| \bAñadelo\b | Añádelo | imperative with pronoun: missing accent |
| \bañadelos\b | añádelos | imperative with pronoun: missing accent |
| \bAñadelos\b | Añádelos | imperative with pronoun: missing accent |
| \bbarajalo\b | barájalo | imperative with pronoun: missing accent |
| \bBarajalo\b | Barájalo | imperative with pronoun: missing accent |
| \bbarajalos\b | barájalos | imperative with pronoun: missing accent |
| \bBarajalos\b | Barájalos | imperative with pronoun: missing accent |
| \bcambialo\b | cámbialo | imperative with pronoun: missing accent |
| \bCambialo\b | Cámbialo | imperative with pronoun: missing accent |
| \bcolocalas\b | colócalas | imperative with pronoun: missing accent |
| \bColocalas\b | Colócalas | imperative with pronoun: missing accent |
| \bdesignalo\b | desígnalo | imperative with pronoun: missing accent |
| \bDesignalo\b | Desígnalo | imperative with pronoun: missing accent |
| \bdestruyelo\b | destrúyelo | imperative with pronoun: missing accent |
| \bDestruyelo\b | Destrúyelo | imperative with pronoun: missing accent |
| \bdevuelvela\b | devuélvela | imperative with pronoun: missing accent |
| \bDevuelvela\b | Devuélvela | imperative with pronoun: missing accent |
| \bdevuelvelas\b | devuélvelas | imperative with pronoun: missing accent |
| \bDevuelvelas\b | Devuélvelas | imperative with pronoun: missing accent |
| \bdevuelvelos\b | devuélvelos | imperative with pronoun: missing accent |
| \bDevuelvelos\b | Devuélvelos | imperative with pronoun: missing accent |
| \bequipala\b | equípala | imperative with pronoun: missing accent |
| \bEquipala\b | Equípala | imperative with pronoun: missing accent |
| \bequipalo\b | equípalo | imperative with pronoun: missing accent |
| \bEquipalo\b | Equípalo | imperative with pronoun: missing accent |
| \binvocala\b | invócala | imperative with pronoun: missing accent |
| \bInvocala\b | Invócala | imperative with pronoun: missing accent |
| \binvocalo\b | invócalo | imperative with pronoun: missing accent |
| \bInvocalo\b | Invócalo | imperative with pronoun: missing accent |
| \bmandala\b | mándala | imperative with pronoun: missing accent |
| \bMandala\b | Mándala | imperative with pronoun: missing accent |
| \bmandalas\b | mándalas | imperative with pronoun: missing accent |
| \bMandalas\b | Mándalas | imperative with pronoun: missing accent |
| \bmandalo\b | mándalo | imperative with pronoun: missing accent |
| \bMandalo\b | Mándalo | imperative with pronoun: missing accent |
| \bordenalas\b | ordénalas | imperative with pronoun: missing accent |
| \bOrdenalas\b | Ordénalas | imperative with pronoun: missing accent |
| \bretiralas\b | retíralas | imperative with pronoun: missing accent |
| \bRetiralas\b | Retíralas | imperative with pronoun: missing accent |
| \bretiralo\b | retíralo | imperative with pronoun: missing accent |
| \bRetiralo\b | Retíralo | imperative with pronoun: missing accent |
| \bsaltate\b | sáltate | imperative with pronoun: missing accent |
| \bSaltate\b | Sáltate | imperative with pronoun: missing accent |
| \bSacrifício\b | Sacrificio | Portuguese accent |
| \bdespues\b | después | accent |
| \bdespúes\b | después | typo |
| \bDemónio\b\|\bdemónio\b | demonio | Portuguese accent |
| \bpropietários\b | propietarios | Portuguese accent |
| \bpropietário\b | propietario | Portuguese accent |
| \bInvocacion\b | Invocación | accent |
| \bInvocacón\b | Invocación | typo |
| \bPosicón\b | Posición | typo |
| \bPinguino\b | Pingüino | umlaut |
| \bEspadachin\b | Espadachín | accent |
| \bEspiritu\b | Espíritu | accent |
| \bÓrden\b | Orden | wrong accent |
| \bMágia\b | Magia | wrong accent |
| \bCodícia\b | Codicia | Portuguese accent |
| \bCañon Magico\b | Cañón Mágico | accents |
| \bGuardian Grarl\b | Guardián Grarl | accent |
| \bAngel Guardián\b | Ángel Guardián | accent |
| \bTIRRA\b | TIERRA | typo |
| \bnigún\b | ningún | typo |
| \bNingun\b | Ningún | accent |
| \bningun\b | ningún | accent |
| \bDevuelte\b | Devuelve | typo |
| \bInglige\b\|\binflinge\b | inflige | typo |
| \bselccionado\b\|\bselecionado\b | seleccionado | typo |
| \bamfíbio\b | anfibio | typo |
| \bacrobaticamente\b | acrobáticamente | typo |
| \baerorosol\b | aerosol | typo |
| \bbiotecnologia\b | biotecnología | typo |
| \bcaida\b | caída | typo |
| \bcaidos\b | caídos | typo |
| \bcuetro\b | cuatro | typo |
| \bmáscars\b | máscaras | typo |
| \benmaascarado\b | enmascarado | typo |
| \bexluyendo\b | excluyendo | typo |
| \bcombinandose\b | combinándose | typo |
| \bseparandose\b | separándose | typo |
| \bdefendiendose\b | defendiéndose | typo |
| \bgovernaba\b | gobernaba | typo |
| \bmaritima\b | marítima | typo |
| \bporqie\b | porque | typo |
| \bponne\b | pon | typo |
| \bdia\b | día | typo |
| \benergia\b | energía | typo |
| \bhabia\b | había | typo |
| \bhuída\b | huida | typo |
| \bincreible\b | increíble | typo |
| \bincreiblemente\b | increíblemente | typo |
| \bgrácias\b | gracias | typo |
| \bposeido\b | poseído | typo |
| \bprofuncidades\b | profundidades | typo |
| \bprópio\b | propio | typo |
| \bprópios\b | propios | typo |
| \btecnica\b | técnica | typo |
| \btecnologia\b | tecnología | typo |
| \btodavia\b | todavía | typo |
| \bvctima\b | víctima | typo |
| \bvictima\b | víctima | typo |
| \bmonstuos\b | monstruos | typo |
| \bmonsturo\b | monstruo | typo |
| \bmounstro\b | monstruo | typo |
| \bcañon\b | cañón | typo |
| \bdestruyela\b | destrúyela | imperative with pronoun: missing accent |
| \bDestruyela\b | Destrúyela | imperative with pronoun: missing accent |
| \bfuerzas? de galera\b | fuerza de vendaval | wrong translation (English: gale-force) |
| \bpuede ser invocado mediante\b | puede ser Invocado mediante | inconsistent capitalization (Invocado as in the other cards) |
| \bFé\b | Fe | wrong accent |
| \bel DEF\b | la DEF | gender of DEF (la DEF in the rest of the game) |
| \bEl DEF\b | La DEF | gender of DEF (la DEF in the rest of the game) |
| \bla Deck\b | el Deck | gender of Deck (masculine as in 'tu Deck') |
| \bCerébro\b | Cerebro | wrong accent |
| \bA menos que no pagues\b | A menos que pagues | wrong double negation (English: Unless you pay) |
| de esta carta se convierte en la misma cantidad | de esta carta se convierten en la misma cantidad | agreement (ATK y DEF) |
| \bTu y tu adversario\b | Tú y tu adversario | accent |
| \bTanto tu como\b | Tanto tú como | accent |
| \bPoseida\b | Poseída | accent |
| \bCañon\b | Cañón | accent |
| \bPortacañon\b | Portacañón | accent |
| \bGémins\b | Géminis | typo |
| \bAtaudes\b | Ataúdes | accent |
| \bEspia\b | Espía | accent |
| \bBuho\b | Búho | accent |
| \bInvocaciónes\b | Invocaciones | typo |
| \bhasta el End Phase\b | hasta la End Phase | gender of End Phase (as in the rest of the game) |
| Fusión\.\(no necesitas | Fusión. (no necesitas | missing space |
| \bPeon Vil\b | Peón Vil | accent |
| \bTrio Ojama\b | Trío Ojama | accent |
| \bgana la Match\b | gana el Match | gender of Match |
| \bAmfibio\b | Anfibio | typo |
| \bAmfibia\b | Anfibia | typo |
| \bUna (alma\|hada)\b | Un \1 | 'un' before a stressed a- (RAE) |
| \buna (alma\|hada)\b | un \1 | 'un' before a stressed a- (RAE) |
| "Brazo\ de\ espada\ de\ Dragón" | "Brazo de Espada de Dragón" | quoted card name: official name |
| "Brazo\ de\ espada\ de\ Dragon" | "Brazo de Espada de Dragón" | quoted card name: official name |
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
| "Llamada\ del\ oscuridad" | "Llamada de Oscuridad" | quoted card name: official name |
| "Llamada\ de\ la\ oscuridad" | "Llamada de Oscuridad" | quoted card name: official name |
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
| "Demonio\ Géminis" | "Diablillos Géminis" | quoted card name: official name |
| "Demonio\ Geminis" | "Diablillos Géminis" | quoted card name: official name |
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
| "Ficha\ Tramposa" | "Ficha Difícil" | quoted card name: official name |
| "Ficha\ Tramposas" | "Ficha Difícil" | quoted card name: official name |
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

### Per-card corrections (all)
| id | field | old | new | reason |
|---|---|---|---|---|
| 5666 | desc | se negare. | quedan anulados. | mutilated word |
| 4017 | name | Dragon | Dragón | accent |
| 4089 | desc | monstrus | monstruos | typo |
| 4657 | desc | monstro del adversario ataco | monstruo del adversario ataca | typos |
| 4657 | desc | punots | puntos | typo |
| 4761 | desc | monstruos mas | monstruos más | accent |
| 4808 | desc | Seleccióna | Selecciona | wrong accent |
| 4892 | desc | són destruidas | son destruidas | wrong accent |
| 4948 | desc | numero de cartas | número de cartas | accent |
| 4969 | desc | tengais | tengáis | accent |
| 4976 | desc | calculo | cálculo | accent |
| 5130 | desc | Cámbia | Cambia | wrong accent |
| 5132 | desc | limite | límite | accent |
| 5221 | desc | justícia | justicia | Portuguese accent |
| 5530 | desc | demas cartas | demás cartas | accent |
| 5522 | name | Falcos, o Sábio Alado | Falcos, el Sabio Alado | Portuguese leftover ("o Sábio") |
| 5760 | desc | dstino | destino | typo |
| 5895 | desc | Envia | Envía | accent |
| 6160 | desc | turnsos | turnos | typo |
| 6368 | desc | Destuye | Destruye | typo |
| 6376 | desc | Envie "Umi" no seu Campo para o Cemitério para enviar para o Cemitério todos os cards na mão de ambos os jogadores e no Campo exceto este card. | Envía "Umi" de tu Campo al Cementerio para enviar al Cementerio todas las cartas de la mano de ambos jugadores y del Campo, excepto esta carta. | Portuguese sentence: translated into Spanish following the English text and the game's terminology |
| 6410 | desc | hacersele | hacérsele | accent |
| 6410 | desc | con exito | con éxito | accent |
| 6410 | desc | ●Magica : | ●Mágica: | accent and space before the colon |
| 6537 | desc | montruo | monstruo | typo |
| 4070 | desc | Una rápido y poderoso | Un rápido y poderoso | agreement |
| 4078 | desc | se aplica a | se aplican a | agreement (ATK y DEF) |
| 4088 | desc | con una ataque | con un ataque | agreement |
| 4138 | desc | una sepulcro | un sepulcro | agreement |
| 4148 | desc | y la "Muro de Fuego" | y el "Muro de Fuego" | agreement |
| 4154 | name | controla el oscuridad | controla la oscuridad | agreement |
| 4181 | name | Cerébro | Cerebro | wrong accent |
| 4192 | desc | que invocar refuerzos | que invoca refuerzos | typo |
| 4203 | desc | armas semejante a | armas semejantes a | agreement |
| 4261 | desc | esta escudada | está escudada | accent |
| 4261 | desc | a si misma | a sí misma | accent |
| 4267 | desc | Un perverso guerrero que hipnotiza | Un perverso espejo que hipnotiza | wrong translation (English: mirror) |
| 4286 | desc | el rey esta ausente | el rey está ausente | accent |
| 4303 | desc | todos las señales | todas las señales | agreement |
| 4398 | desc | desde la Deck al campo | desde el Deck al campo | gender of Deck (masculine as in the other cards) |
| 4434 | name | Fé | Fe | wrong accent |
| 4484 | desc | Aumenta en 1000 puntos | aumenta en 1000 puntos | wrong capital letter |
| 4485 | desc | es devuelto a la parte | es devuelta a la parte | agreement |
| 4519 | desc | esta armado | está armado | accent |
| 4521 | desc | Oriental qe lanza | Oriental que lanza | typo |
| 4545 | desc | tiburón zombie | tiburón zombi | spelling consistent with the game's Zombi |
| 4591 | desc | aún así | aun así | accent |
| 4622 | desc | el ATK y el DEF de este monstruo se reduce a la mitad | el ATK y la DEF de este monstruo se reducen a la mitad | agreement |
| 4622 | desc | tanto el ATK como el DEF | tanto el ATK como la DEF | gender of DEF |
| 4637 | desc | la compresión | la comprensión | typo |
| 4655 | desc | oidos | oídos | accent |
| 4660 | desc | equipado con esta tarjeta incrementa su ATK por 700 puntos | equipado con esta carta aumenta su ATK en 700 puntos | terminology (tarjeta -> carta) and preposition |
| 4678 | desc | en el Campo tu adversario | en el Campo de tu adversario | missing preposition |
| 4691 | desc | Posición de DEfensa | Posición de Defensa | wrong capital letter |
| 4693 | desc | Nivel 2 ó inferior | Nivel 2 o inferior | accent |
| 4737 | desc | de esta carta se convierte en la misma | de esta carta se convierten en la misma | agreement |
| 4755 | desc | es Invocación (excluyendo | es Invocada (excluyendo | typo |
| 4761 | desc | en el Campo que tu. | en el Campo que tú. | accent |
| 4786 | desc | Aún cuando | Aun cuando | accent |
| 4789 | desc | monstruos de tipo Demonio | monstruos de Tipo Demonio | inconsistent capitalization |
| 4795 | desc | es Invocación (incluyendo | es Invocada (incluyendo | typo |
| 4805 | desc | cuantos "Fichas de Kuriboh" | cuantas "Fichas de Kuriboh" | agreement |
| 4806 | desc | monstruo del tipo Máquina | monstruo de Tipo Máquina | inconsistent capitalization |
| 4810 | desc | hasta 2 de cartas Tipo Dragón | hasta 2 cartas de Tipo Dragón | grammar |
| 4819 | desc | no son negadas por el efecto | no son negados por el efecto | agreement |
| 4830 | desc | no puedes llamar a ningún monstruo | no puedes Invocar ningún monstruo | wrong translation (English: summon) |
| 4835 | desc | tú eliges cual | tú eliges cuál | accent |
| 4859 | name | Llamada del oscuridad | Llamada de la oscuridad | agreement |
| 4877 | name | Germenes | Gérmenes | accent |
| 4885 | desc | Si un monstruo de tu Campo sea enviado | Si un monstruo de tu Campo fue enviado | verb tense (English: was sent) |
| 4901 | desc | descarta 1 al azar carta | descarta 1 carta al azar | word order |
| 4951 | desc | se convierte del Tipo que has declarado | se convierten en el Tipo que has declarado | agreement |
| 4952 | desc | declarado no puede atacar | declarado no pueden atacar | agreement |
| 4953 | desc | cuando hayan 5 o más | cuando haya 5 o más | agreement (impersonal haber) |
| 4962 | desc | y Colocalas en el Campo | y colócalas en el Campo | wrong capital letter and accent |
| 4983 | desc | monstruo de tipo Dragón | monstruo de Tipo Dragón | inconsistent capitalization |
| 5024 | desc | el ATK y el DEF de todos tus monstruos tipo Planta boca arriba aumenta en | el ATK y la DEF de todos tus monstruos de Tipo Planta boca arriba aumentan en | agreement and capital letter |
| 5027 | desc | los Tipo-Máquina | los monstruos de Tipo Máquina | consistent spelling |
| 5034 | desc | tanto al ATK como al DEF se le añaden | tanto al ATK como a la DEF se les añaden | agreement |
| 5086 | desc | han sido engaños | han sido engañados | typo |
| 5110 | desc | Aumenta en ATK del monstruo | Aumenta el ATK del monstruo | typo |
| 5122 | desc | esta boca arriba | está boca arriba | accent |
| 5177 | desc | Coloca una "Contador de Doncella" | Coloca un "Contador de Doncella" | agreement |
| 5178 | desc | con una "Contador de Doncella" | con un "Contador de Doncella" | agreement |
| 5178 | desc | que ocasiona Damage Step a los Life Points | que ocasiona daño de batalla a los Life Points | wrong translation (English: Battle Damage) |
| 5190 | desc | cada monstruo tipo Bestia | cada monstruo de Tipo Bestia | inconsistent capitalization |
| 5197 | desc | que tu aumentes | que tú aumentes | accent |
| 5212 | desc | que tu controles | que tú controles | accent |
| 5219 | name | EL Secreto | El Secreto | wrong capital letter |
| 5221 | desc | El Espíritu maldito | El espíritu maldito | wrong capital letter |
| 5222 | desc | tu controlas el monstruo | tú controlas el monstruo | accent |
| 5226 | desc | acercarsele | acercársele | accent |
| 5237 | desc | Selecciona lo mismo "Cráneo Convocado" que cualquier monstruo | Selecciona "Cráneo Convocado" o cualquier monstruo | wrong translation (English: either ... or) |
| 5246 | desc | no puede ser negado por ninguna carta | no pueden ser negados por ninguna carta | agreement |
| 5290 | desc | todas las Carta Mágica boca arriba | todas las Cartas Mágicas boca arriba | agreement |
| 5291 | desc | elegir una carta de monstruo de la Mano de tu oponente. Añade esa carta a tu Mano | elegir 1 Carta de Monstruo de la mano de tu oponente. Añade esa carta a tu mano | inconsistent capitalization (mano / Carta de Monstruo) |
| 5299 | desc | esta carta solo cuando | esta carta cuando | repetition of 'solo' |
| 5394 | desc | en el Campos | en el Campo | typo |
| 5406 | desc | y ataca tu monstruo seleccionado | y ataca a tu monstruo seleccionado | missing preposition |
| 5421 | desc | pasa a ser 2400 sólo durante. | pasa a ser 2400 sólo durante ese cálculo de daño. | truncated sentence (English: during that damage calculation only) |
| 5427 | desc | de tu Baraja | de tu Deck | consistent terminology (Deck) |
| 5493 | desc | todas las Carta Mágica y de Trampa | todas las Cartas Mágicas y de Trampa | agreement |
| 5517 | name | Cuidador de Tumba | Cuidador de Tumbas | name consistent with the other cards of the series |
| 5539 | desc | Deck de fusión | Deck de Fusión | inconsistent capitalization |
| 5543 | desc | que infliga daño | que inflija daño | wrong subjunctive |
| 5546 | name | Estratégia | Estrategia | Portuguese accent |
| 5557 | desc | Monstruo de NV 4 | Monstruo de Nivel 4 | abbreviation not used elsewhere |
| 5561 | desc | carta tipo Zombi con un DEF de 1200 | carta de Tipo Zombi con una DEF de 1200 | capital letter/gender |
| 5561 | desc | añadirla a tu Mano | añadirla a tu mano | wrong capital letter |
| 5619 | desc | monstruos que tu. | monstruos que tú. | accent |
| 5619 | desc | selecciona que monstruos son destruidos | selecciona qué monstruos son destruidos | accent |
| 5624 | desc | un monstruo o more. | un/os monstruo/s. | leftover English ('or more') |
| 5645 | name | Paladína | Paladina | wrong accent |
| 5647 | desc | no puede ataque otro monstruo | no puede atacar a otro monstruo | grammar |
| 5656 | desc | en el Campo que la que puedas | en el Campo en la que puedas | preposition |
| 5666 | desc | cuando no hayan otras cartas | cuando no haya otras cartas | agreement (impersonal haber) |
| 5676 | desc | superiores del tu Deck | superiores de tu Deck | typo |
| 5685 | desc | Voltea todos las Cartas | Voltea todas las Cartas | agreement |
| 5689 | desc | la esta Ficha | esta Ficha | typo |
| 5697 | desc | y la mandada al Cementerio | y lo manda al Cementerio | malformed sentence (English: sends it to the Graveyard) |
| 5699 | desc | del turno en la que esta carta realizara una batalla | del turno en el que esta carta realice una batalla | agreement and verb tense |
| 5730 | name | Más Alla | Más Allá | accent |
| 5735 | desc | Todos las monstruos | Todos los monstruos | agreement |
| 5737 | desc | que tu seleccionaste | que tú seleccionaste | accent |
| 5756 | desc | Invocación normal | Invocación Normal | inconsistent capitalization |
| 5757 | desc | como sacrificio | como Sacrificio | inconsistent capitalization |
| 5759 | desc | tenia | tenía | accent |
| 5763 | desc | que controle de tu adversario | que controle tu adversario | extra preposition |
| 5780 | desc | al End Phase del turno | durante la End Phase del turno | preposition/gender |
| 5786 | desc | equipo con esta carta | equipado con esta carta | typo |
| 5829 | desc | como resultado de una batalla y la manda al Cementerio | como resultado de una batalla y lo manda al Cementerio | agreement |
| 5834 | desc | El ATK y la DEF de esta carta se convierte en | El ATK y la DEF de esta carta se convierten en | agreement |
| 5846 | desc | si haya un | si hay un | agreement |
| 5876 | desc | no sera más | no será más | accent |
| 5880 | desc | en vez de ser mandada al Cementerio | en vez de ser mandado al Cementerio | agreement |
| 5952 | name | Sabiduria | Sabiduría | accent |
| 5954 | desc | Cielo"está | Cielo" está | missing space |
| 5976 | desc | de tu Adversario. | de tu adversario. | wrong capital letter |
| 6004 | name | Geminis | Géminis | accent |
| 6005 | desc | cartas en tu Mano, puedes añadir esta carta a tu Mano | cartas en tu mano, puedes añadir esta carta a tu mano | wrong capital letter |
| 6010 | desc | Monstruo de un oponente Ataca | monstruo de un oponente ataca | wrong capital letters |
| 6018 | desc | sabe en que está pensando | sabe en qué está pensando | accent |
| 6019 | desc | sera manchado | será manchado | accent |
| 6025 | desc | Mientras no hayan cartas | Mientras no haya cartas | agreement (impersonal haber) |
| 6059 | name | Energia | Energía | accent |
| 6071 | name | Resurección | Resurrección | typo |
| 6095 | desc | Todavia | Todavía | accent |
| 6129 | name | Factoria | Factoría | accent |
| 6133 | desc | que este escrito | que esté escrito | accent |
| 6148 | desc | Inglige daño a tu adversario igual al número | Inflige daño a tu adversario igual al número | typo (Inglige) |
| 6149 | desc | de tu Mano. Durante | de tu mano. Durante | wrong capital letter |
| 6150 | desc | desde tu Mano descartando otra carta desde tu Mano | desde tu mano descartando otra carta desde tu mano | wrong capital letter |
| 6163 | name | Ficha Bloqueadoras | Ficha Bloqueadora | agreement |
| 6165 | name | Ficha Tramposas | Ficha Tramposa | agreement |
| 6166 | desc | en el tu Campo | en tu Campo | typo |
| 6174 | desc | Dekochi | Dekoichi | wrong name (English: Dekoichi) |
| 6218 | desc | seleccionadas no puede ser activadas | seleccionadas no pueden ser activadas | agreement |
| 6233 | desc | Las Leyendas dicen | Las leyendas dicen | wrong capital letter |
| 6307 | desc | Invocación Especial a una 1 "Fuerza | Invocación Especial a 1 "Fuerza | typo |
| 6383 | desc | a si mismo | a sí mismo | accent |
| 6400 | desc | desde tu Mano puedes | desde tu mano puedes | wrong capital letter |
| 6405 | desc | el ATK y el DEF de todas las otras Cartas de Monstruos en el Campo se reduce a la mitad | el ATK y la DEF de todas las otras Cartas de Monstruo en el Campo se reducen a la mitad | agreement |
| 6410 | desc | desde tu Mano despues | desde tu mano después | wrong capital letter and accent |
| 6410 | desc | ●Trampa : elige | ●Trampa: elige | space before the colon |
| 6410 | desc | ●Monstruo de Efecto : elige | ●Monstruo de Efecto: elige | space before the colon |
| 6419 | desc | de esta carta el final del Damage Step. Si esta carta lucha sin | de esta carta al final del Damage Step. Si esta carta lucha sin | preposition |
| 6419 | desc | destruye esta carta el final del Damage Step | destruye esta carta al final del Damage Step | preposition |
| 6435 | desc | cuando hayan 3 | cuando haya 3 | agreement (impersonal haber) |
| 6454 | desc | desde tu Mano (puede | desde tu mano (puede | wrong capital letter |
| 6487 | desc | Manda 1carta | Manda 1 carta | missing space |
| 6494 | desc | mandado el Cementerio | mandado al Cementerio | preposition |
| 6498 | desc | destruye esta carta el final del Damage Step | destruye esta carta al final del Damage Step | preposition |
| 6517 | desc | activa un Carta Mágica Normal | activa una Carta Mágica Normal | agreement |
| 6537 | desc | infligido a el controlador de monstruo equipado | infligido al controlador del monstruo equipado | grammar |
| 6539 | desc | (si esta boca abajo | (si está boca abajo | accent |
| 6550 | desc | hasta 5 Carta Mágica desde | hasta 5 Cartas Mágicas desde | agreement |
| 6574 | desc | de tu Deck y Colócala en tu Campo | de tu Deck y colócala en tu Campo | wrong capital letter |
| 6598 | desc | todas las Cartas de Magia Continuas | todas las Cartas Mágicas Continuas | consistent terminology |
| 6608 | desc | durante el Standby Phase | durante la Standby Phase | gender of Standby Phase |
| 6636 | desc | a tu Mano o hacerles | a tu mano o hacerles | wrong capital letter |
| 6646 | desc | El ATK y la DEF de esta carta se convierte | El ATK y la DEF de esta carta se convierten | agreement |
| 6647 | desc | El ATK y la DEF de esta carta se convierte | El ATK y la DEF de esta carta se convierten | agreement |
| 6666 | desc | todos las Cartas Mágicas | todas las Cartas Mágicas | agreement |
| 6675 | desc | mediante un Invocación | mediante una Invocación | agreement |
| 6684 | desc | "Ficha de Opción"a tu Campo | "Ficha de Opción" a tu Campo | missing space |
| 6685 | desc | ● Hombre Pila C | ●Hombre Pila C | space after the bullet (as in the other lines) |
| 6617 | desc | sea iguales al Nivel | sea igual al Nivel | agreement |
| 6720 | desc | Invocación de Sacrifico, los monstruos Sacrificadas | Invocación de Sacrificio, los monstruos Sacrificados | typos |
| 6781 | desc | y Colócala en tu Campo | y colócala en tu Campo | wrong capital letter |
| 6815 | desc | en tu Zona de Trampas Mágicas y de Trampa | en tu Zona de Cartas Mágicas y de Trampa | typo |
| 6825 | desc | tu 3ra Standby Phase | tu 3ª Standby Phase | consistent ordinal numeral (2ª, 4º...) |
| 6955 | desc | cuyo DEF es más bajo que el ATK que esta carta | cuya DEF es más baja que el ATK de esta carta | agreement |
| 6957 | desc | mandada el Cementerio | mandada al Cementerio | preposition |
| 6957 | desc | como sacrificio. Cuando | como Sacrificio. Cuando | inconsistent capitalization |
| 4358 | name | Kanan loss Swordmistress | Kanan la Señora de las Espadas | semi-English name; official: Kanan la Señora de las Espadas |
| 4348 | name | el Señora de la Curación | el Señor de la Curación | inconsistent gender (el Señora) |
| 4644 | name | Reina de los permisos de otoño | Reina de las Hojas de Otoño | mistranslation of 'leaves' (no official Spanish name; fr: Reine des Feuilles d'Automne) |
| 5546 | name | Estrategia de Disturbación | Estrategia de Disturbio | 'Disturbación' does not exist; official: Estrategia de Disturbio |
| 6450 | name | Triedad | La Selección | official Spanish name of Triage |
| 5179 | desc | cambiar el blanco de ese ataque | cambiar el objetivo de ese ataque | official terminology: 'objetivo' (target) |
| 5187 | desc | seleccionan los blancos de ataque | seleccionan los objetivos de ataque | official terminology: 'objetivo' (target) |

### Complete list of changed cards
**Complete original -> new comparison with the changed words highlighted: `docs/changes_es/cards_diff.md`** (all 720 entries). Raw data: `docs/changes_es/cards.csv`. First 40 rows:

| id | original name | field | original | new |
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

(... 680 more rows in the CSV)

## A3. Story dialogues

Archives: `script/stNN_<scene>_f.ehp`, every scene is a pair of members `...If.bin` (offsets in UTF-16 characters) and `...Lf.bin` (UTF-16LE strings terminated by NUL, some gzip-compressed). **601 lines** changed (including those that **inherit** the correction because they have the same original text and the same Japanese as a corrected line).

Flow: line-by-line reading compared with English and Japanese -> touch-ups in `tools/data/dialogue_touchups_es.json` (`exact` and `parts`) -> `build_dialogues.py es` -> `dialogue_corrections_es.json` -> `apply_to_iso.py`. Automatic layout rules in `build_dialogues.py`: non-breaking space before `! ? : ;` also after `》` (rule `FR_PUNCT`), space after the placeholders, "Mode histoire" -> "Mode aventure". Box constraints: ~46 characters per line, max 3 lines (a placeholder counts ~6 characters): `apply_to_iso` reports the lines that might not fit.

### Re-reading touch-ups: `exact` (2) — whole original sentence -> new sentence
| original | new |
|---|---|
| ¡Ten, puedes usar éste! | ¡Ten, usa este traje de criada! |
| Qué pasa...⏎¿Estás bien? | ¿Qué pasa...⏎¿Estás bien? |

### Re-reading touch-ups: `parts` (100) — text replacements applied to every line (in order)
| old | new |
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

### Complete list of lines
**Complete original -> new comparison (with English and Japanese): `docs/changes_es/dialogues_diff.md`** (all 601 lines). Raw data: `docs/changes_es/dialogues.csv`. First 30:

| id | original | new | English |
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

(... 571 more rows in the CSV)

## A4. Duelist sentences in duels

Tables `chr_wordstbl_f.bin` and `02chr_wordstbl_...` inside ~72 `duel/cutin_*.ehp` archives (and `zakov*`). The unique sentences are ~1,800: all re-read. **55 sentences changed** (75 entries). Data: `exact` (32) and `parts` (24) in `duel_line_corrections_es.json`. The `*-ptrs.txt` files of the character archives contain absolute offsets: if a table grows they must be recomputed (`remap_pointers`), otherwise the duel crashes.

Comparison with highlighted words: `docs/changes_es/duel_lines_diff.md`.

| original | new | entries | archive examples |
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

## A5. Long and short interface strings

Tables `strTbl*`, `help_strtbl_*`, `ddstrtbl_*`, `field_strtbl*` (format `(n, 12, 12+4n)` + offsets + UTF-16) in 81 archives (the same table is copied into several archives, e.g. `field/always_*_fra.ehp` x6). **329 unique strings changed**. Rules: `tools/corrections/string_rules_es.py` — **6 `STRINGS` entries** (archive, member, 0-based index, [(old, new)], reason), **542 `GLOBALS`** (regex/callable, applied after the STRINGS) on **30 tables** (`TABLES`); plus 0 targeted corrections in `tools/data/ui_texts.json` (in-place writes, text shorter than or equal to the original).

### By member (unique strings changed)
| member | strings |
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

### Global rules (all)
| pattern | replacement | reason |
|---|---|---|
| \bSlifer Red\b | Slifer Rojo | dormitory name as in the dialogues |
| \bRa Yellow\b | Ra Amarillo | dormitory name as in the dialogues |
| \bObelisk Blue\b | Obelisco Azul | dormitory name as in the dialogues |
| \bShadow Rid(?:er\|re)s\b | Jinetes de la Sombra | group name as in the dialogues (and typo Ridres) |
| \bDuelista Shadow\b | Duelista de la Sombra | as 'duelista de sombra' in the dialogues |
| \bArchifiend\b | Archidemonio | name of the card family |
| \bTrio Ojama\b | Trío Ojama | card name, accent |
| Cañon Magico Mega Ton | Cañón Mágico Mega Ton | card name, accents |
| XYZ-Dragón Cañon | XYZ-Dragón Cañón | card name, accent |
| Catapulta Cañon | Catapulta Cañón | card name, accent |
| "Magica de Campo” | "Mágica de Campo" | accent and quotation marks |
| \bMagicas\b | Mágicas | accent |
| \bMagica\b | Mágica | accent |
| Criado de Cráneo | Sirviente de la Calavera | card name |
| \b([Mm])onstruos Cómicos\b | \1onstruos Toon | the cards use Toon |
| \bmonstruos Animados\b | monstruos Toon | the cards use Toon |
| Invocación por Fusión | Invocación de Fusión | term as on the cards |
| Invocación por Ritual | Invocación de Ritual | term as on the cards |
| Invocación por Volteo | Invocación de Volteo | term as on the cards |
| Efecto de Disparado de Múltiple | Efecto de Disparo Múltiple | grammar |
| Efecto de Disparado | Efecto de Disparo | grammar (matches '(Continua, Encendido, Disparo, Volteo)') |
| Trampas de Contraataque | Trampas de Contraefecto | term as on the cards |
| \bBonus Afortunada\b | Bonus Suerte | agreement |
| \bBonus Union\b | Bonus Unión | accent |
| Retirados e a partida | Retirados de la partida | typo |
| Contradores de Magia | Contadores de Magia | typo |
| Número de veces que se invocó monstruos | Número de veces que se invocaron monstruos | agreement |
| Invocación Normal a 10 monstruos durante un duelo\. | Realizadas 10 Invocaciones Normales durante un duelo. | consistency with the neighbouring lines |
| Contraatacadas Magias, Trampas efectos, Ataques e Invocaciones de tu enemigo 10 veces durante un duelo\. | Contraatacados 10 veces Magias, Trampas, efectos, Ataques e Invocaciones de tu oponente durante un duelo. | commas and 'oponente' |
| con un ataque simple y se ganó | con un solo ataque o efecto y se ganó | English says 'single attack or effect' |
| Gana durante el turno de tu oponente\. | Se ganó durante el turno de tu oponente. | verb tense like the neighbouring lines |
| Gana un duelo usando los Efectos de | Se ganó un duelo usando los efectos de | verb tense like the neighbouring lines |
| ^botón ×: siguiente$ | Botón ×: siguiente | capital letter like the next line |
| en el atolladero en que se encuentre | en qué atolladero se encuentre | grammar |
| fusión de cartas de Héroe Elemental | Fusión de cartas de Héroe Elemental | capital letter of the game term |
| gente fuerte, de confiar, | gente fuerte, de confianza, | typo |
| lo hacia desde | lo hacía desde | accent |
| suave de los que su nombre | suave de lo que su nombre | grammar |
| explicar porqué le retuvieron | explicar por qué le retuvieron | por qué |
| porqué le retuvieron | por qué le retuvieron | por qué |
| la cual\.\.\.hace tiempo | la cual... hace tiempo | space |
| atractivas monstruos femeninas | atractivos monstruos femeninos | agreement |
| llamado a "Chica Cibernética" | llamado "Chica Cibernética" | extra preposition |
| como ser humano Y gracias | como ser humano. Y gracias | punctuation |
| en lo  primero que tenga a mano | en lo primero que tenga a mano | space |
| Clama tener seis Decks | Afirma tener seis Decks | 'clamar' is not 'afirmar' |
| nadie que no se Vellian ha usado alguna vez una | nadie que no sea Vellian ha usado jamás una | typo |
| carta principal es Golem de Mecanismo Antiguo", | carta principal es "Golem de Mecanismo Antiguo", | missing quotation marks |
| Nadie sabe que tipo de Deck | Nadie sabe qué tipo de Deck | accent |
| saber que le pasará al hombre | saber qué le pasará al hombre | accent |
| actividades en el campus Pero | actividades en el campus. Pero | punctuation |
| en el campus Pero Alexis | en el campus. Pero Alexis | punctuation |
| para poder matricular y verle | para poder matricularse y verle | grammar |
| también pudiera tener este poder de efecto especial como un espíritu$ | También pudiera tener este poder de efecto especial como un espíritu. | final full stop |
| signo del destino\.\.\n | signo del destino...⏎ | ellipsis dots |
| señal del destino\.\.\n | señal del destino...⏎ | ellipsis dots |
| sella dentro de una carta el alma de perdedor | sella dentro de una carta el alma del perdedor | article |
| tiene como a "Dragón de Oscuridad de Ojos Rojos" como carta principal | tiene a "Dragón de Oscuridad de Ojos Rojos" como carta principal | grammar |
| ^Perfil de Sheppard del Principio$ | Perfil del Rector Sheppard | 'Principal' translated as 'Principio'; Rector as in the dialogues |
| Asaltante Veladora de Tumbas | Asaltante del Cuidador de Tumba | card name |
| ^Sin límite\.$ | Sin límite | extra final full stop |
| mostrarán todas las cartas ¿Aceptas\? | mostrarán todas las cartas. ¿Aceptas? | punctuation |
| es una Carta Limitada, sólo 2 pueden | es una Carta Semi-Limitada, sólo 2 pueden | English says Semi-Limited |
| está in correcta | es incorrecta | typo |
| ^Acerca del Menú Editar Deck\.$ | Acerca del Menú Editar Deck | extra final full stop |
| Acerca de las carta$ | Acerca de las cartas | plural |
| ^Cosas que puedes hacer en "Draw Phase"\.$ | Cosas que puedes hacer en "Draw Phase" | extra final full stop |
| (Día 3: Invocación de Tributo y Fundamentos de Magias y Trampas)\.$ | \1 | extra final full stop |
| Invocación de Tributo | Invocación por Sacrificio | official Spanish term (Invocada por Sacrificio), as in the cards |
| Invocaciones de Tributo | Invocaciones por Sacrificio | official Spanish term, as in the cards |
| ¿Qué es una Deck Receta\? | ¿Qué es una Receta de Deck? | word order |
| ^Trampa Normales$ | Trampas Normales | plural |
| ^Trampa Continuas$ | Trampas Continuas | plural |
| ●Contador Mágico | ●Contadores Mágicos | plural |
| Los Contador Mágico | Los Contadores Mágicos | plural |
| ●Mira bocarriba carta | ●Mirar boca arriba una carta | translation of 'Pick up card' |
| Poner bocarriba carta significa | Mirar boca arriba una carta significa | translation of 'Pick up card' |
| Zone del Deck de Fusión | Zona del Deck de Fusión | typo |
| Flujo el Turno | Flujo del Turno | typo |
| ^colocar \(Invocación Normal\)$ | Colocar (Invocación Normal) | capital letter |
| ●Colocar de Cartas Mágicas y de Cartas de Trampa | ●Colocar Cartas Mágicas y Cartas de Trampa | grammar |
| \(Fase de Final\) | (Fase Final) | as the others |
| Fase  de Batalla | Fase de Batalla | space |
| Deck- tienen que ser 3 | Deck: tienen que ser 3 | punctuation |
| Colocando Etiquetas a tus cartas favoritas o importantes hará | Colocar Etiquetas en tus cartas favoritas o importantes hará | grammar |
| Devuelve una carta que acaba de moverse de otra vez a su posición original\. | Devuelve a su posición original una carta que acaba de moverse. | broken sentence |
| requerimientos\n(Esto es similar a la función) | requerimientos.\n\1 | missing full stop |
| etc\.,en un Deck | etc., en un Deck | space |
| de cual Deck se basa en tipo de concepto | de cuál Deck se basa en qué tipo de concepto | accents |
| botón ×    Mover carta seleccionada Las cartas por lo general | botón ×⏎   Mover carta seleccionada⏎   Las cartas por lo general | missing line breaks (as in English) |
| Cartas de Monstruos de Fusión” | Cartas de Monstruo de Fusión" | agreement |
| Cartas de Monstruos de Fusión\" | Cartas de Monstruo de Fusión" | agreement |
| Carta de Magica llamada | Carta Mágica llamada | grammar |
| Carta de Magia llamada | Carta Mágica llamada | grammar |
| Polimerizacion | Polimerización | accent |
| hacer Invocación de Fusión a este tipo especial de monstruo | hacer una Invocación de Fusión de este tipo especial de monstruo | grammar |
| Mientras carta esté boca arriba | Mientras esta carta esté boca arriba | missing article |
| (?m)^os efectos generalmente | Los efectos generalmente | missing initial letter |
| La misma se usa el mismo orden | Se usa en el mismo orden | grammar |
| as Cartas de Trampa tienen diversos | las Cartas de Trampa tienen diversos | typo |
| una Trampa de Carta | una Carta de Trampa | word order |
| efecto de l Carta de Trampa | efecto de la Carta de Trampa | typo |
| incluso durante el turno de tu oponente\.\nAdemás | incluso durante tu propio turno.⏎Además | English says 'your own turn' |
| "Siete Herramientas del Bandido"\' | "Siete Herramientas del Bandido" | extra apostrophe |
| efecto de negación de la Carta de Trampa "Disruptor Mágico" | efecto de negación de Cartas Mágicas de "Disruptor Mágico" | English says Spell Card-negating |
| Spell Speed 2 Cadenas encadenarse | Spell Speed 2 pueden encadenarse | 'pueden' wrongly replaced by 'Cadenas' |
| no Cadenas encadenarse a cartas | no pueden encadenarse a cartas | 'pueden' wrongly replaced by 'Cadenas' |
| solamente Cadenas encadenarse cartas | solamente pueden encadenarse cartas | 'pueden' wrongly replaced by 'Cadenas' |
| no Cadenas haber encadenamiento | no puede haber encadenamiento | 'puede' wrongly replaced by 'Cadenas' |
| ninguna ora activación | ninguna otra activación | typo |
| Monstruos de Efectos\n | Monstruos de Efecto⏎ | agreement |
| Mágicas de Juego Rápido / Mágicas Normales\nMonstruos de Efecto | Mágicas de Juego Rápido / Trampas Normales⏎Monstruos de Efecto | English says Normal Traps |
| Cartas Prohibidas, Limitadas y Semilimitadas | Cartas Prohibidas, Limitadas y Semi-Limitadas | as in the rest |
| cuando t dicen que robes | cuando te dicen que robes | typo |
| Los efectos no tienen como blanco a carta\(s\) específica\(s\) | Los efectos que no tienen como blanco a carta(s) específica(s) | grammar |
| o efecto que tienen como blanco | o efectos que tienen como blanco | agreement |
| decidir hacia donde moverla | decidir hacia dónde moverla | accent |
| otra vez e botón | otra vez el botón | typo |
| estas cartas  particular han | estas cartas en particular han | missing word |
| Botón × : confirma | Botón ×: confirma | space |
| en una "Matchs" | en una "Match" | wrong plural |
| preguntándote que tipo | preguntándote qué tipo | accent |
| de acuerdo al DEF de cada monstruo | de acuerdo a la DEF de cada monstruo | gender of DEF as on the cards |
| botón △para | botón △ para | space |
| el Deck editando en esos momentos\. | el Deck que estás editando en este momento. | grammar |
| Seleccionando "Búsqueda" después de teclear | Seleccionando "Ejecutar" después de teclear | the button is called Ejecutar (English: Run) |
| o el botó R\. | o el botón R. | typo |
| Descripciónes | Descripciones | typo |
| Parece que has adquirido práctica con unas cuantas cartas\. | Parece que has conseguido unas cuantas cartas. | badly translated ('gotten your hands on') |
| ^Rindes$ | Rendirse | button label |
| eliminadas | retiradas | 'retirar' as in the rest of the game |
| Los Puntos Vida de | Los Puntos de Vida de | missing preposition |
| Tus Puntos Vida han | Tus Puntos de Vida han | missing preposition |
| Te rendiste rendido debido | Te rendiste debido | repetition |
| se reducen 0\. | se reducen a 0. | missing preposition |
| un "Match" está compuesta | un "Match" está compuesto | agreement |
| de toda el Match | de todo el Match | agreement |
| Roba cartas desde aquí y para añadirlas a tu mano\. | Roba cartas desde aquí y añádelas a tu mano. | grammar |
| Esta carta esta excluida | Esta carta está excluida | accent |
| El efecto de esta Magica se aplica | El efecto de esta Carta Mágica se aplica | grammar |
| mediante Piedra Papel Tijeras | mediante Piedra, Papel o Tijeras | punctuation |
| continúas al duelo siguiente | continúas con el duelo siguiente | preposition |
| \(Si no en este momento no quedan | (Si en este momento no quedan | typo |
|  - colocar de una Carta de Trampa o de una Carta Mágica |  - Colocar una Carta de Trampa o una Carta Mágica | grammar |
| Invocar a in monstruo | Invocar a un monstruo | typo |
| a la colocar de una Carta de Monstruo en el campo en Posición de Defensa boca abajo se la llama una "colocar"\. | a colocar una Carta de Monstruo en el campo en Posición de Defensa boca abajo se le llama "Colocar". | broken sentence |
| boca arriba esto se le llama una | boca arriba, a esto se le llama una | grammar |
| La colocar de Cartas Mágicas y de Trampa se diferencia de la colocar de Cartas de Monstruo | Colocar Cartas Mágicas y de Trampa se diferencia de Colocar Cartas de Monstruo | broken sentence |
| de la carta siendo usada,\n | de la carta siendo usada.⏎ | punctuation |
| Casa Paso de la Battle Phase | Cada Paso de la Battle Phase | typo |
| regresarás a la Battle Step | regresarás al Battle Step | gender |
| Posición de Batalla de monstruo que es el blanco | Posición de Batalla del monstruo que es el blanco | article |
| tiene un DEF más bajo | tiene una DEF más baja | gender of DEF as on the cards |
| tiene un DEF más alto | tiene una DEF más alta | gender of DEF as on the cards |
| \n\nif Player C of Team 2 has attacked during his/her Battle Phase.*?in response to the attack\.\n |  | leftover English: the paragraph is already translated right after |
| que tubo su turno justo antes de eso | que tuvo su turno justo antes de eso | typo |
| sera capaz de elegir | será capaz de elegir | accent |
| Asumiendo que el duelo se juega de acuerdo al siguiente,\n(Equipo 1: Jugador A\nEquipo 2: Jugador C\nEquipo 1: Jugador B\nEquipo 2: Jugador D\n)(\n) | Asumiendo que el duelo se juega de acuerdo con el siguiente orden,\n\n\1\2 | incomplete sentence |
| Asumiendo que el duelo se juega de acuerdo al siguiente,\n(Equipo 1: Jugador A\nEquipo 2: Jugador C\nEquipo 1: Jugador B\nEquipo 2: Jugador D)\n?$ | Asumiendo que el duelo se juega de acuerdo con el siguiente orden,⏎⏎\1⏎⏎si el Jugador C del Equipo 2 ha atacado durante su Battle Phase, el jugador que tuvo su turno justo antes de eso, que es el Jugador A del Equipo 1, podrá elegir si quiere o no activar una Carta Mágica de Juego Rápido o una Trampa como respuesta al ataque. | truncated text: the final paragraph was missing (translated from English) |
| ^¡No hay a quién dárselo\.!$ | ¡No hay a quién dárselo! | punctuation |
| ^Trar$ | Comer | English says Eat |
| ^¿Tirar bocadillo\?$ | ¿Comer bocadillo? | English says 'Eat a sandwich?' |
| \$C0 ！ | $C0! | full-width exclamation mark and space |
| ^MIE$ | MIÉ | accent |
| ^SAB$ | SÁB | accent |
| ^¡ %s adquirido!$ | ¡%s adquirido! | space |
| etc\.que no hayan | etc., que no hayan | punctuation |
| La belleza esta en su sabor | La belleza está en su sabor | accent |
| una maestro pastelero | un maestro pastelero | agreement |
| Es divertido mascarlo\. | Es divertido masticarlo. | typo |
| artesanalmente\.\. Sabe | artesanalmente. Sabe | punctuation |
| los cual explica porqué siempre se venden todos | lo cual explica por qué siempre se agotan | typo |
| una hígado de ganso | un hígado de ganso | agreement |
| ^Alójese (\d+)$ | Habitación \1 | the English name is Room |
| ^Academia del duelo$ | Academia de Duelos | as in the rest of the game |
| ^Una tienda$ | Tienda | extra article |
| ^La Oficina de canciller$ | Oficina del Rector | 'Rector' as in the dialogues |
| ^Cliff$ | Acantilado | leftover English |
| ^Dorm abandonado$ | Dormitorio abandonado | English abbreviation |
| ^Último Arena$ | Última Arena | gender |
| No hay cartaseleccionadas | No hay cartas seleccionadas | missing space |
| La contraseña introducida está incorrecta | La contraseña introducida es incorrecta | ser/estar |
| esta carya | esta carta | typo |
| ^Esperando por oponente\.\.\.$ | Esperando al oponente... | grammar |
| Yu-Gi- Oh! | Yu-Gi-Oh! | space |
| ^Derotar Crowler$ | Derrotar a Crowler | typo |
| ^Para princiiantes$ | Para principiantes | typo |
| nuevos dato de juego | nuevos datos de juego | agreement |
| botón □ : Selección | botón □: Selección | space |
| Austes del sonido | Ajustes del sonido | typo |
| Austa el volumen | Ajusta el volumen | typo |
| ^EN$ | ON | 'EN' is not ON (English says ON) |
| ^FUERADE$ | OFF | 'FUERADE' is a typo for OFF |
| ^SIN LIMITE DE TIEMPO$ | SIN LÍMITE DE TIEMPO | accent |
| ^NO LIMITE$ | SIN LÍMITE | correct Spanish |
| Mientras en el modo ad hoc, sostenga el botón SELECT | Mientras estés en modo ad hoc, mantén presionado el botón SELECT | register: the whole game uses the informal tú |
| para desconectar y devolver al menú principal | para desconectar y volver al menú principal | grammar |
| presiona el botón ×\$C0, y confirmar\. | presiona el botón ×$C0, y confirma. | imperative |
| COLECCCIONABLES | COLECCIONABLES | typo |
| ^Escogido entre representante\.$ | Elegido entre los representantes. | grammar |
| ^Interscholastic se baten en duelo\.$ | Duelo interescolar. | leftover English |
| ^Antes de una reunión\.$ | El día antes del torneo Tag Force. | English: the day before the Tag Force meet |
| Ahora le turno a  | Ahora es el turno de  | typo: 'le turno' |
| Ahora le turno\na  | Ahora es el turno⏎de  | typo: 'le turno' |
| ¡Le turno a\n | ¡Es el turno de⏎ | typo: 'le turno' |
| Le turno a  | Es el turno de  | typo: 'le turno' |
| Como te turno\na ti primero, \$0, | Como el primer turno es⏎tuyo, $0, | typo: 'te turno' |
| \$C5Sryus | $C5Syrus | typo |
| \$CALP\$ de su rival | $CALP$C0 de su rival | unclosed color code |
| Zona de Cartas de Monstruos Después, pulsa | Zona de Cartas de Monstruos. Después, pulsa | punctuation |
| tiene una en\nPosición de Ataque | tiene uno en⏎Posición de Ataque | agreement (monstruo) |
| Pero si invocación a un\nmonstruo en vez de\nColocar, | Pero si invocas a un⏎monstruo en vez de⏎colocarlo, | typo: 'invocación' for 'invocas' |
| e invocación a uno\ncon un ATK menor | e invocas a uno⏎con un ATK menor | typo: 'invocación' for 'invocas' |
| \$Cpad analógico\$C0 | $C8pad analógico$C0 | incomplete color code |
| debes realizar una Invocación de u ofrecer uno o más monstruos como Tribute\. | debes realizar una Invocación y ofrecer uno o más monstruos como Sacrificio. | truncated sentence and leftover English |
| ^invocación a 1 monstruo\.$ | Invoca a 1 monstruo. | typo: 'invocación' for 'invoca' |
| ¡\$0!\ninvocación a un monstruo! | ¡$0!⏎¡Invoca a un monstruo! | typo: 'invocación' for 'invoca' |
| Pulsa el botón × para\nabrir el menú de Phase\.\nSelecciona "End Phase" y\nluego pulsa el botón ○\. | Pulsa el botón ○ para⏎abrir el menú de Phase.⏎Selecciona "End Phase" y⏎luego pulsa el botón ×. | swapped buttons (English: ○ opens the menu, × confirms) |
| que Colocar boca abajo, se pondrán | que se coloquen boca abajo se pondrán | grammar |
| Primero hay que Colocar\nboca abajo | Primero hay que colocarlas⏎boca abajo | grammar |
| Colocar tu Carta de Trampa\. | ¡Coloca tu Carta de Trampa! | imperative |
| Antes, \$C5Bastion\$C0 ha preguntado | Antes, $C5Syrus$C0 ha preguntado | English says Syrus |
| %C5Alexis | $C5Alexis | color code |
| aumentan en \$CA200\$\.\.\. | aumentan en $CA200$C0... | unclosed color code |
| disminuyen en \$CA200\$! | disminuyen en $CA200$C0! | unclosed color code |
| ¡Ahora me turno! | ¡Ahora es mi turno! | typo |
| \$C5Alexis'\$C0 | $C5Alexis$C0 | extra apostrophe |
| Cartas de Trampas Normales | Cartas de Trampa Normales | Trampa is invariable |
| #CACarta | $CACarta | color code |
| Zona de de  | Zona de  | doubled word |
| ¡Los monstruo de  | ¡Los monstruos de  | plural |
| "\$C6Umi\$C0" sigue activo, | "$C6Umi$C0" sigue activa, | agreement with Carta Mágica |
| \bel Hechizo(\s)de(\s)(Campo\|Equipo) | la Carta Mágica\1de\2\3 | term as on the cards (and gender) |
| \bEl Hechizo(\s)de(\s)(Campo\|Equipo) | La Carta Mágica\1de\2\3 | term as on the cards (and gender) |
| \bHechizo(\s)de(\s)(Campo\|Equipo) | Carta Mágica\1de\2\3 | term as on the cards |
| (?<=[^\s])(?<!Sí)(?<!No)  +(?=[^\s]) |   | double space |
| \bun refinar búsqueda\b | un filtrado | terminology as in the 'Filtrar' menu |
| Refinar Búsqueda | Filtrar | terminology as in the 'Filtrar' menu |
| "Brazo\ de\ espada\ de\ Dragón" | "Brazo de Espada de Dragón" | quoted card name: official name |
| "Brazo\ de\ espada\ de\ Dragon" | "Brazo de Espada de Dragón" | quoted card name: official name |
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
| "Llamada\ del\ oscuridad" | "Llamada de Oscuridad" | quoted card name: official name |
| "Llamada\ de\ la\ oscuridad" | "Llamada de Oscuridad" | quoted card name: official name |
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
| "Demonio\ Géminis" | "Diablillos Géminis" | quoted card name: official name |
| "Demonio\ Geminis" | "Diablillos Géminis" | quoted card name: official name |
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
| "Ficha\ Tramposa" | "Ficha Difícil" | quoted card name: official name |
| "Ficha\ Tramposas" | "Ficha Difícil" | quoted card name: official name |
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
| \bEfectos de Blanco\b | Efectos con Objetivo | official terminology: objetivo (target) |
| \bblanco\b | objetivo | official terminology: objetivo (target) |
| \bblancos\b | objetivos | official terminology: objetivo (target) |

### STRINGS entries (all): where and why
| archive | member | index | changes | reason |
|---|---|---|---|---|
| database/duelrecord.ehp | strTbl_s.bin | 130 | 1 replacement(s) | the translation of 'using effects' was missing (it said 'en batalla' like the line before) |
| database/duelrecord.ehp | strTbl_s.bin | 179 | 1 replacement(s) | English says 'Level 4 or lower' |
| database/duelrecord.ehp | strTbl_s.bin | 124 | 1 replacement(s) | it, fr, de and en say 10 throws |
| duel/result/result_s.ehp | strTbl.bin | 130 | 1 replacement(s) | the translation of 'using effects' was missing (it said 'en batalla' like the line before) |
| duel/result/result_s.ehp | strTbl.bin | 179 | 1 replacement(s) | English says 'Level 4 or lower' |
| duel/result/result_s.ehp | strTbl.bin | 124 | 1 replacement(s) | it, fr, de and en say 10 throws |

### Targeted corrections `ui_texts.json`
| file | member | index | old | new | reason |
|---|---|---|---|---|---|

### Complete list
**Complete comparison with highlighted words: `docs/changes_es/ui_strings_diff.md`.** Raw data: `docs/changes_es/ui_strings.csv`. First 40:

| member | index | original | new |
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

(... 289 more rows in the CSV)

## A6. [SPELL CARD] / [TRAP CARD] label of the large card in the duel

In all the `duel/basic_<region><language>.ehp` the label was in English (hash `c2268340`): `apply_to_iso.py` replaces it with `card_spell_trap.gim` of `field/always_<language>_<language>.ehp` (hash `9622cd75`).

| archive | member | original hash | new hash |
|---|---|---|---|
| /PSP_GAME/USRDIR/duel/basic_bs.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |
| /PSP_GAME/USRDIR/duel/basic_fs.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |
| /PSP_GAME/USRDIR/duel/basic_gs.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |
| /PSP_GAME/USRDIR/duel/basic_is.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |
| /PSP_GAME/USRDIR/duel/basic_ss.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |
| /PSP_GAME/USRDIR/duel/basic_us.ehp | card_spell_trap.gim | c2268340 | 5e3d2ddd |

## A7. ISO files touched and technical details

179 `.ehp` archives differ from the original (all languages together, because the ISO is a single one; list in `docs/changes_es/touched_files.csv`). The other files (video, audio, `EBOOT.BIN` executable, `PARAM.SFO`) are identical. Non-textual technical differences: `*-ptrs.txt` (absolute member offsets, recomputed when a table changes length), new position of the archives at the end of the ISO.

## A8. What can NOT be changed (game limits)

- The **speaker name** in the dialogue box (e.g. "Preside Sheppard"/"Cancelliere" in Italian, "Doyen Sheppard" in French, "Rector Sheppard" in Spanish) lives in the encrypted EBOOT: it cannot be modified.
- Texts drawn by the game with its own font (dialogues, names, descriptions in the deck, drop-down menus, system keyboard, language selection screen) cannot be replaced by the texture pack: they can only be changed in the ISO.
- The 438 map/background textures are not replaced (the game changes their palette): a limit of MikeyMK's pack, not of our work.

---

# B. TEXTURE PACK

## B1. Origin and structure

Base: **Yu-Gi-Oh! GX Tag Force 1 HD Remastered** by **MikeyMK** (US pack `ULUS10136`) and HD cards by **chrisfand**, adapted to the European ISO `ULES00600`. The project does not redistribute the third-party pack: the patcher gets it from the user. Our work: (1) remap the US pack's **hashes** to the EU ones (`tools/gen_ini.py`), (2) redo the cards and interface lettering in the language, (3) correct the texts, (4) `upscale_extra` for the textures that are not covered.

PPSSPP recognizes a texture by the **hash of its pixels** (xxhash of the data, `gim.data_hash`); every line of `textures.ini` is `0000000000000000<hash8> = path/png`. The PNGs are **4x** the original and redraw exactly the same area. Textures that are identical between languages have the same hash: the replacement holds for all of them (see `docs/TEXTURE_INVENTORY.md`).

### Real structure (from `docs/changes_es/pack_structure.csv`)
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
| moduli/es | cards/ | 5675 | 1024.6 | frame, large_es, small_es, tiny_es |
| moduli/es | es.ini | 1 | 0.01 |  |
| moduli/es | intro/ | 2 | 0.4 | title_screen |
| moduli/es | ui_es/ | 95 | 8.2 | icon_sheets, icon_sheets.ini, result_letters, result_letters.ini, menu_lists, menu_lists.ini, deck_screens, deck_screens.ini, recipe_screens, recipe_screens.ini ... |

Every language except Italian is a **module** (`PSP/TEXTURES/modules/es`) to compose over the base pack with `tools/compose_pack.py BASE MODULES CARD_DIR OUT es [--copy]`: it copies the base and **only** the `cards`, `intro` and `ui_es` folders of the module (hard link or copy), then `module_ini.py` rewrites the `textures.ini`: the localized card lines point to `cards/small_es`/`large_es` and the lines of `es.ini` **replace** those of the base with the same key (hash).

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

Language folders: `frame` (2 files), `large_es` (2833 files), `small_es` (2833 files), `tiny_es` (7 files). Every card has an **HD small** one (name + description + type, regenerated with free OFL fonts: XCharter Bold for names/type/labels, Libre Baskerville for effects, Newsreader Italic for Normals, PT Serif Caption for Spells/Traps, Charis SIL for the missing glyphs) and an **HD large** one (name only on the frame). In addition: the **attribute table** with the words of the language (`cards/frame/icons_attribute_race_<l>.png`, `attributes.py`), the **Spell/Trap label** (`icons_spell_trap_<l>.png`, `label_it.py` / `extract_labels.py` -> `data/label_eu_<code>_128x32.png`) and the deck **thumbnail atlas** (`tiny_<l>`, `tiny_atlas.py` + `tiny_fragment.py`).

When the text of a card changes (section A2) its images must be regenerated: **624 cards** in spanish. List in `docs/changes_es/card_images.csv`. Command: `python tools/generate_language.py fr PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` (without IDs it regenerates all of them: 2,833 + 2,833, ~930 MB).

Typography: non-breaking space before `: ; ! ?` and « » quotation marks.

## B3. HD interface in spanish (`ui_es`)

**87 textures** (`docs/changes_es/ui_textures.csv`: file, PPSSPP hash, family, script, original/HD size, neutral/specific, origin in the ISO). By family: icon_sheets 3, result_letters 22, menu_lists 6, deck_screens 14, recipe_screens 11, vs_screen 14, duel_texts 11, tutorial 6. Of these 0 are neutral (same hash in all languages) and 87 specific. Every family has a script in `tools/ui_textures/<family>.py` (reads `TF1_LANG`): it redraws the lettering texture by texture starting from the low-resolution original of the ISO and from the style of the English pack; same area and same positions (the game crops from fixed rectangles); one font/weight/baseline/shadow per lettering; free fonts (`alt_font.py`).

| family | textures | script | source ISO archive | language texts |
|---|---|---|---|---|
| icon_sheets | 3 | `tools/ui_textures/icon_sheets.py` | deck/all_s.ehp, shop/all_s.ehp, field/always_* | `icon04`, `s_pack` (AGOTADO), `panel` (fragment "rados"); `pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01` have the same hash as English |
| result_letters | 22 | `tools/ui_textures/result_letters.py` | duel/basic_ss.ehp | HAS GANADO (HASGNDO) · HAS PERDIDO (HASPERDIO, 9 tiles) · EMPATE (EMPAT) + silhouette |
| menu_lists | 6 | `tools/ui_textures/menu_lists.py` | title_menu/title_menu_s.ehp, duel/result/result_s.ehp, field/always_bri_<code>.ehp | MENÚ PRINCIPAL · INTRODUCE EL NOMBRE · LISTA DE CARTAS DESCARGADAS · DUELO ACERTIJO · OPCIONES · AJUSTES DEL IDIOMA · AGRUPAR LISTA... · RESULTADO DEL DUELO · PRESIONA EL BOTÓN START · GANAS/EMPATE/PIERDES · Domingo...Sábado · Mayo Julio Junio Agosto · Días / para el torneo / de · AM / PM |
| deck_screens | 14 | `tools/ui_textures/deck_screens.py` | deck/all_s.ehp, labo/*.ehp, shop/all_s.ehp | Tronco ×3, Fusión, Alquiler ×4, Laboratorio, Conversor ×2, "Tipos de carta en posesión", "Cartas compradas" (+ fragment), ACEPTAR |
| recipe_screens | 11 | `tools/ui_textures/recipe_screens.py` | deck/recipe_view_s.ehp, title_menu/title_menu_s.ehp, database/limitlist.ehp | Personaje / Usuario / Recetas descargadas / Recetas de personaje / Recetas de usuario / Limitada / Semi-Limitada / Prohibida / Cambiar |
| vs_screen | 14 | `tools/ui_textures/vs_screen.py` | duel/start/start_e.ehp (members _s), start_all.ehp, start_s.ehp | DUELO / NORMAL / TAG · SEGUNDO EN SALIR / PRIMERO EN SALIR · 1ra/2da/3ra vuelta · Modo Individual / Modo Combate · GANAS/PIERDES/EMPATE · JUGADOR 1 / JUGADOR 2 · JUGADOR |
| duel_texts | 11 | `tools/ui_textures/duel_texts.py` | duel/basic_ss.ehp | Cadena · TURNO DEL SIGUIENTE JUGADOR (the cut between the two textures passes inside a letter, as in the original) · COMENZAR DUELO · Ataque Directo · TURNO and `card_icon03` covered by already existing textures (same hash as Italian / `upscale_extra`) |
| tutorial | 6 | `tools/ui_textures/tutorial.py` | tutorial/tutorial_s.ehp (tuto_duelimg01..06) | Tu oponente ha declarado la batalla. / ¿activar el efecto de la carta? · SÍ/NO · 5 maps; 2-line dialogue but wider box |

Quality rules (valid for every language): regular letters, never deformed one by one; same area as the original; no blur; the text is that of the language's original (only obvious errors are corrected: leftovers from other languages, accents); pixel art is **not** smoothed without confirmation; geometries always measured on the original.

### Drawn texts: original -> HD
Table read by eye, texture by texture: `docs/changes_es/texture_texts_es.md`. Differences from the original: `DEMARRER` -> `DÉMARRER`, `SCAMBIA`/`Scambia` -> `ÉCHANGE`/`Échange`, `2è/3è round` -> `2e/3e round`; everything else rewrites the same words.

### List of every texture
(all 87 rows, from `ui_textures.csv`)

| file in the pack | hash | family | original px | HD px | type | ISO origin |
|---|---|---|---|---|---|---|
| ui_es/icon_sheets/all_s__icon04.png | 57ec7a66 | icon_sheets | 128x128 | 512x512 | SPECIFIC | deck/all_s.ehp:icon04.gim |
| ui_es/icon_sheets/all_s__panel.png | 6c431a2a | icon_sheets | 256x256 | 1024x1024 | SPECIFIC | shop/all_s.ehp:panel.gim |
| ui_es/icon_sheets/all_s__s_pack.png | 7a7314e5 | icon_sheets | 256x256 | 1024x1024 | SPECIFIC | shop/all_s.ehp:s_pack.gim |
| ui_es/result_letters/basic_ss__duel_draw100002.png | ba388fb8 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_draw100002.gim; duel/basic_fs.ehp:duel_draw100002.gim; duel/basic_gs.ehp:duel_draw100002.gim |
| ui_es/result_letters/basic_ss__duel_draw100004.png | 396a68f8 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_draw100004.gim; duel/basic_fs.ehp:duel_draw100004.gim; duel/basic_gs.ehp:duel_draw100004.gim |
| ui_es/result_letters/basic_ss__duel_draw100006.png | 14389066 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_draw100006.gim; duel/basic_fs.ehp:duel_draw100006.gim; duel/basic_gs.ehp:duel_draw100006.gim |
| ui_es/result_letters/basic_ss__duel_draw100008.png | 17a7a350 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_draw100008.gim; duel/basic_fs.ehp:duel_draw100008.gim; duel/basic_gs.ehp:duel_draw100008.gim |
| ui_es/result_letters/basic_ss__duel_draw100010.png | 3d47af74 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_draw100010.gim; duel/basic_fs.ehp:duel_draw100010.gim; duel/basic_gs.ehp:duel_draw100010.gim |
| ui_es/result_letters/basic_ss__duel_lose100002.png | 1cb4482c | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_lose100002.gim; duel/basic_fs.ehp:duel_lose100002.gim; duel/basic_gs.ehp:duel_lose100002.gim |
| ui_es/result_letters/basic_ss__duel_lose100004.png | ecb90266 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_lose100004.gim; duel/basic_fs.ehp:duel_lose100004.gim; duel/basic_gs.ehp:duel_lose100004.gim |
| ui_es/result_letters/basic_ss__duel_lose100006.png | 7d290a32 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_lose100006.gim; duel/basic_fs.ehp:duel_lose100006.gim; duel/basic_gs.ehp:duel_lose100006.gim |
| ui_es/result_letters/basic_ss__duel_lose100008.png | 3733b351 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_lose100008.gim; duel/basic_fs.ehp:duel_lose100008.gim; duel/basic_gs.ehp:duel_lose100008.gim |
| ui_es/result_letters/basic_ss__duel_lose100010.png | ffc4d8e5 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_lose100010.gim; duel/basic_fs.ehp:duel_lose100010.gim; duel/basic_gs.ehp:duel_lose100010.gim |
| ui_es/result_letters/basic_ss__duel_lose100012.png | 302162eb | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_lose100012.gim; duel/basic_fs.ehp:duel_lose100012.gim; duel/basic_gs.ehp:duel_lose100012.gim |
| ui_es/result_letters/basic_ss__duel_lose100014.png | 9aa5d99c | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_lose100014.gim; duel/basic_fs.ehp:duel_lose100014.gim; duel/basic_gs.ehp:duel_lose100014.gim |
| ui_es/result_letters/basic_ss__duel_lose100016.png | 00b99210 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_lose100016.gim; duel/basic_fs.ehp:duel_lose100016.gim; duel/basic_gs.ehp:duel_lose100016.gim |
| ui_es/result_letters/basic_ss__duel_lose100018.png | 09cc5268 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_lose100018.gim; duel/basic_fs.ehp:duel_lose100018.gim; duel/basic_gs.ehp:duel_lose100018.gim |
| ui_es/result_letters/basic_ss__duel_win100002.png | c130b02b | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_win100002.gim; duel/basic_fs.ehp:duel_win100002.gim; duel/basic_gs.ehp:duel_win100002.gim |
| ui_es/result_letters/basic_ss__duel_win100004.png | e40b4f5a | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_win100004.gim; duel/basic_fs.ehp:duel_win100004.gim; duel/basic_gs.ehp:duel_win100004.gim |
| ui_es/result_letters/basic_ss__duel_win100006.png | b602abed | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_win100006.gim; duel/basic_fs.ehp:duel_win100006.gim; duel/basic_gs.ehp:duel_win100006.gim |
| ui_es/result_letters/basic_ss__duel_win100008.png | 5d42a4d6 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_win100008.gim; duel/basic_fs.ehp:duel_win100008.gim; duel/basic_gs.ehp:duel_win100008.gim |
| ui_es/result_letters/basic_ss__duel_win100010.png | 7346cdd7 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_win100010.gim; duel/basic_fs.ehp:duel_win100010.gim; duel/basic_gs.ehp:duel_win100010.gim |
| ui_es/result_letters/basic_ss__duel_win100012.png | 3b9ae395 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_win100012.gim; duel/basic_fs.ehp:duel_win100012.gim; duel/basic_gs.ehp:duel_win100012.gim |
| ui_es/result_letters/basic_ss__duel_win100014.png | 5a1e30a6 | result_letters | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:duel_win100014.gim; duel/basic_fs.ehp:duel_win100014.gim; duel/basic_gs.ehp:duel_win100014.gim |
| ui_es/result_letters/basic_ss__duel_win100016.png | e22c31d5 | result_letters | 64x32 | 256x128 | SPECIFIC | duel/basic_bs.ehp:duel_win100016.gim; duel/basic_fs.ehp:duel_win100016.gim; duel/basic_gs.ehp:duel_win100016.gim |
| ui_es/menu_lists/always_bri_spa__story_sys02.png | 92c0609f | menu_lists | 256x128 | 1024x512 | SPECIFIC | field/always_bri_spa.ehp:story_sys02.gim; field/always_fra_spa.ehp:story_sys02.gim; field/always_ger_spa.ehp:story_sys02.gim |
| ui_es/menu_lists/result_s__menu01.png | 6a156d48 | menu_lists | 256x64 | 1024x256 | SPECIFIC | duel/result/result_s.ehp:menu01.gim |
| ui_es/menu_lists/result_s__menu02.png | ffd0d26a | menu_lists | 256x128 | 1024x512 | SPECIFIC | duel/result/result_s.ehp:menu02.gim |
| ui_es/menu_lists/title_menu_s__m_menu_title01.png | 2589c36d | menu_lists | 256x128 | 1024x512 | SPECIFIC | title_menu/title_menu_s.ehp:m_menu_title01.gim |
| ui_es/menu_lists/title_menu_s__press_start0003.png | 45d9a888 | menu_lists | 256x16 | 1024x64 | SPECIFIC | title_menu/title_menu_s.ehp:press_start0003.gim |
| ui_es/menu_lists/title_menu_s__trnsmt02.png | 87428289 | menu_lists | 256x256 | 1024x1024 | SPECIFIC | title_menu/title_menu_s.ehp:trnsmt02.gim |
| ui_es/deck_screens/all_s__d_window00008.png | 308698d0 | deck_screens | 128x32 | 512x128 | SPECIFIC | deck/all_s.ehp:d_window00008.gim |
| ui_es/deck_screens/all_s__d_window00016.png | 47084696 | deck_screens | 64x32 | 256x128 | SPECIFIC | deck/all_s.ehp:d_window00016.gim |
| ui_es/deck_screens/all_s__d_window00033.png | ac8667a7 | deck_screens | 256x32 | 1024x128 | SPECIFIC | deck/all_s.ehp:d_window00033.gim |
| ui_es/deck_screens/all_s__d_window00051.png | 4b97edef | deck_screens | 64x32 | 256x128 | SPECIFIC | deck/all_s.ehp:d_window00051.gim |
| ui_es/deck_screens/all_s__d_window00062.png | 18b02d40 | deck_screens | 128x32 | 512x128 | SPECIFIC | deck/all_s.ehp:d_window00062.gim; labo/conv_machine.ehp:window_s0016.gim; title_menu/title_menu_s.ehp:t_window0015.gim |
| ui_es/deck_screens/all_s__d_window00101.png | 91eb2bb5 | deck_screens | 64x32 | 256x128 | SPECIFIC | deck/all_s.ehp:d_window00101.gim; labo/rental.ehp:window_s0008.gim |
| ui_es/deck_screens/all_s__tab_title.png | 6fe1264c | deck_screens | 256x32 | 1024x128 | SPECIFIC | shop/all_s.ehp:tab_title.gim |
| ui_es/deck_screens/conv_machine__window_s0009.png | 24cf8aaf | deck_screens | 128x32 | 512x128 | SPECIFIC | labo/conv_machine.ehp:window_s0009.gim; labo/conv_machine.ehp:window_s0026.gim |
| ui_es/deck_screens/conv_machine__window_s0016.png | 18b02d40 | deck_screens | 128x32 | 512x128 | SPECIFIC | deck/all_s.ehp:d_window00062.gim; labo/conv_machine.ehp:window_s0016.gim; title_menu/title_menu_s.ehp:t_window0015.gim |
| ui_es/deck_screens/conv_machine__window_s0026.png | 24cf8aaf | deck_screens | 128x32 | 512x128 | SPECIFIC | labo/conv_machine.ehp:window_s0009.gim; labo/conv_machine.ehp:window_s0026.gim |
| ui_es/deck_screens/password__key_s0027.png | 5d6635f4 | deck_screens | 128x32 | 512x128 | SPECIFIC | labo/password.ehp:key_s0027.gim |
| ui_es/deck_screens/rental__window_s0008.png | 91eb2bb5 | deck_screens | 64x32 | 256x128 | SPECIFIC | deck/all_s.ehp:d_window00101.gim; labo/rental.ehp:window_s0008.gim |
| ui_es/deck_screens/rental__window_s0015.png | fee49520 | deck_screens | 128x32 | 512x128 | SPECIFIC | labo/rental.ehp:window_i0015.gim; labo/rental.ehp:window_s0015.gim |
| ui_es/deck_screens/rental__window_s0026.png | 16a6572b | deck_screens | 64x32 | 256x128 | SPECIFIC | labo/rental.ehp:window_s0026.gim |
| ui_es/recipe_screens/limitlist__window_s0002.png | 7d80a6c6 | recipe_screens | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_s0002.gim |
| ui_es/recipe_screens/limitlist__window_s0004.png | 1d7d2421 | recipe_screens | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_s0004.gim |
| ui_es/recipe_screens/limitlist__window_s0012.png | 8c7ebe78 | recipe_screens | 128x32 | 512x128 | SPECIFIC | database/limitlist.ehp:window_s0012.gim |
| ui_es/recipe_screens/recipe_view_s__recipe010008.png | c5c45bb7 | recipe_screens | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_s.ehp:recipe010008.gim; title_menu/title_menu_s.ehp:recipe_sel00002.gim |
| ui_es/recipe_screens/recipe_view_s__recipe010015.png | b6e6f744 | recipe_screens | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_s.ehp:recipe010015.gim; title_menu/title_menu_s.ehp:recipe_sel00009.gim |
| ui_es/recipe_screens/recipe_view_s__recipe010027.png | 72f7f26a | recipe_screens | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_s.ehp:recipe010027.gim; title_menu/title_menu_s.ehp:recipe_sel00020.gim |
| ui_es/recipe_screens/recipe_view_s__recipe010029.png | 285b971c | recipe_screens | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_s.ehp:recipe010029.gim; title_menu/title_menu_s.ehp:recipe_sel00022.gim |
| ui_es/recipe_screens/recipe_view_s__recipe010031.png | c70a1e0a | recipe_screens | 128x32 | 512x128 | SPECIFIC | deck/recipe_view_s.ehp:recipe010031.gim; title_menu/title_menu_s.ehp:recipe_sel00024.gim |
| ui_es/recipe_screens/title_menu_s__recipe_sel00033.png | 6bb39c40 | recipe_screens | 128x32 | 512x128 | SPECIFIC | title_menu/title_menu_s.ehp:recipe_sel00033.gim |
| ui_es/recipe_screens/title_menu_s__t_window0008.png | 117e2298 | recipe_screens | 64x32 | 256x128 | SPECIFIC | title_menu/title_menu_s.ehp:t_window0008.gim |
| ui_es/recipe_screens/title_menu_s__t_window0026.png | 01673953 | recipe_screens | 64x32 | 256x128 | SPECIFIC | title_menu/title_menu_s.ehp:t_window0026.gim |
| ui_es/vs_screen/start_all__jyanken20_s0005.png | a9897630 | vs_screen | 256x32 | 1024x128 | SPECIFIC | duel/start/start_all.ehp:jyanken20_s0005.gim; duel/start/start_e.ehp:jyanken20_s0005.gim; duel/start/start_f.ehp:jyanken20_s0005.gim |
| ui_es/vs_screen/start_all__jyanken20_s0007.png | 7368d31c | vs_screen | 256x32 | 1024x128 | SPECIFIC | duel/start/start_all.ehp:jyanken20_s0007.gim; duel/start/start_e.ehp:jyanken20_s0007.gim; duel/start/start_f.ehp:jyanken20_s0007.gim |
| ui_es/vs_screen/start_all__vs_much1_s0001.png | ef845abc | vs_screen | 128x16 | 512x64 | SPECIFIC | duel/start/start_all.ehp:vs_much1_s0001.gim; duel/start/start_e.ehp:vs_much1_s0001.gim; duel/start/start_f.ehp:vs_much1_s0001.gim |
| ui_es/vs_screen/start_all__vs_much2_s0001.png | ea46529a | vs_screen | 128x16 | 512x64 | SPECIFIC | duel/start/start_all.ehp:vs_much2_s0001.gim; duel/start/start_e.ehp:vs_much2_s0001.gim; duel/start/start_f.ehp:vs_much2_s0001.gim |
| ui_es/vs_screen/start_all__vs_much3_s0001.png | 386e4f79 | vs_screen | 128x16 | 512x64 | SPECIFIC | duel/start/start_all.ehp:vs_much3_s0001.gim; duel/start/start_e.ehp:vs_much3_s0001.gim; duel/start/start_f.ehp:vs_much3_s0001.gim |
| ui_es/vs_screen/start_e__d_menu01_s.png | a77116f2 | vs_screen | 256x256 | 1024x1024 | SPECIFIC | duel/start/start_e.ehp:d_menu01_s.gim; duel/start/start_f.ehp:d_menu01_s.gim; duel/start/start_g.ehp:d_menu01_s.gim |
| ui_es/vs_screen/start_e__vs_bg01_1_s0005.png | 939ffe1b | vs_screen | 256x32 | 1024x128 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_s0005.gim; duel/start/start_f.ehp:vs_bg01_1_s0005.gim; duel/start/start_g.ehp:vs_bg01_1_s0005.gim |
| ui_es/vs_screen/start_e__vs_bg01_1_s0007.png | 3ab04908 | vs_screen | 256x64 | 1024x256 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_s0007.gim; duel/start/start_f.ehp:vs_bg01_1_s0007.gim; duel/start/start_g.ehp:vs_bg01_1_s0007.gim |
| ui_es/vs_screen/start_e__vs_bg01_1_s0008.png | 41ab9f3e | vs_screen | 256x64 | 1024x256 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_s0008.gim; duel/start/start_f.ehp:vs_bg01_1_s0008.gim; duel/start/start_g.ehp:vs_bg01_1_s0008.gim |
| ui_es/vs_screen/start_e__vs_bg01_1_s0012.png | ed29c0fe | vs_screen | 128x32 | 512x128 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_s0012.gim; duel/start/start_f.ehp:vs_bg01_1_s0012.gim; duel/start/start_g.ehp:vs_bg01_1_s0012.gim |
| ui_es/vs_screen/start_e__vs_bg01_1_s0014.png | 8788a7c8 | vs_screen | 128x64 | 512x256 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_1_s0014.gim; duel/start/start_f.ehp:vs_bg01_1_s0014.gim; duel/start/start_g.ehp:vs_bg01_1_s0014.gim |
| ui_es/vs_screen/start_e__vs_bg01_2_s0001.png | 5796698d | vs_screen | 128x16 | 512x64 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_2_s0001.gim; duel/start/start_f.ehp:vs_bg01_2_s0001.gim; duel/start/start_g.ehp:vs_bg01_2_s0001.gim |
| ui_es/vs_screen/start_e__vs_bg01_2_s0004.png | f081a08d | vs_screen | 128x16 | 512x64 | SPECIFIC | duel/start/start_e.ehp:vs_bg01_2_s0004.gim; duel/start/start_f.ehp:vs_bg01_2_s0004.gim; duel/start/start_g.ehp:vs_bg01_2_s0004.gim |
| ui_es/vs_screen/start_s__jnk_card01.png | a2fc7092 | vs_screen | 512x256 | 2048x1024 | SPECIFIC | duel/start/start_s.ehp:jnk_card01.gim |
| ui_es/duel_texts/basic_ss__chain010003.png | c7fd7035 | duel_texts | 64x32 | 256x128 | SPECIFIC | duel/basic_bs.ehp:chain010003.gim; duel/basic_fs.ehp:chain010003.gim; duel/basic_gs.ehp:chain010003.gim |
| ui_es/duel_texts/basic_ss__chain010005.png | abaeb83c | duel_texts | 128x32 | 512x128 | SPECIFIC | duel/basic_bs.ehp:chain010005.gim; duel/basic_fs.ehp:chain010005.gim; duel/basic_gs.ehp:chain010005.gim |
| ui_es/duel_texts/basic_ss__dilect_atk00001.png | 880d6d24 | duel_texts | 256x32 | 1024x128 | SPECIFIC | duel/basic_bs.ehp:dilect_atk00001.gim; duel/basic_fs.ehp:dilect_atk00001.gim; duel/basic_gs.ehp:dilect_atk00001.gim |
| ui_es/duel_texts/basic_ss__dilect_atk00003.png | d8591359 | duel_texts | 128x32 | 512x128 | SPECIFIC | duel/basic_bs.ehp:dilect_atk00003.gim; duel/basic_fs.ehp:dilect_atk00003.gim; duel/basic_gs.ehp:dilect_atk00003.gim |
| ui_es/duel_texts/basic_ss__next_player0001.png | 9d78973f | duel_texts | 64x32 | 256x128 | SPECIFIC | duel/basic_bs.ehp:next_player0001.gim; duel/basic_fs.ehp:next_player0001.gim; duel/basic_gs.ehp:next_player0001.gim |
| ui_es/duel_texts/basic_ss__next_player0002.png | 1e0eff3f | duel_texts | 256x32 | 1024x128 | SPECIFIC | duel/basic_bs.ehp:next_player0002.gim; duel/basic_fs.ehp:next_player0002.gim; duel/basic_gs.ehp:next_player0002.gim |
| ui_es/duel_texts/basic_ss__next_player0004.png | 6d3897cf | duel_texts | 64x32 | 256x128 | SPECIFIC | duel/basic_bs.ehp:next_player0004.gim; duel/basic_fs.ehp:next_player0004.gim; duel/basic_gs.ehp:next_player0004.gim |
| ui_es/duel_texts/basic_ss__next_player0005.png | 4021e68f | duel_texts | 256x32 | 1024x128 | SPECIFIC | duel/basic_bs.ehp:next_player0005.gim; duel/basic_fs.ehp:next_player0005.gim; duel/basic_gs.ehp:next_player0005.gim |
| ui_es/duel_texts/basic_ss__start_duel10001.png | 692edb74 | duel_texts | 64x64 | 256x256 | SPECIFIC | duel/basic_bs.ehp:start_duel10001.gim; duel/basic_fs.ehp:start_duel10001.gim; duel/basic_gs.ehp:start_duel10001.gim |
| ui_es/duel_texts/basic_ss__start_duel10002.png | 8ea8857e | duel_texts | 256x64 | 1024x256 | SPECIFIC | duel/basic_bs.ehp:start_duel10002.gim; duel/basic_fs.ehp:start_duel10002.gim; duel/basic_gs.ehp:start_duel10002.gim |
| ui_es/duel_texts/basic_ss__start_duel10005.png | 0e4dc413 | duel_texts | 128x32 | 512x128 | SPECIFIC | duel/basic_bs.ehp:start_duel10005.gim; duel/basic_fs.ehp:start_duel10005.gim; duel/basic_gs.ehp:start_duel10005.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg01.png | ab860e12 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_s.ehp:tuto_duelimg01.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg02.png | 18e1d210 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_s.ehp:tuto_duelimg02.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg03.png | e3014dad | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_s.ehp:tuto_duelimg03.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg04.png | d046d2fe | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_s.ehp:tuto_duelimg04.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg05.png | 3536db89 | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_s.ehp:tuto_duelimg05.gim |
| ui_es/tutorial/tutorial_s__tuto_duelimg06.png | d1ec1c4a | tutorial | 256x256 | 1024x1024 | SPECIFIC | tutorial/tutorial_s.ehp:tuto_duelimg06.gim |

### Textures that stay like the original
`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `parts` are pixel-art icon sheets (with NEU/NEW): they stay as they were, covered by the `upscale_extra` enlargement as in the other languages; the text was not changed. The neutral textures come from the base pack. In Spanish `score-top` (TURNO) also has the same hash as Italian and `card_icon03` is in `upscale_extra`.

## B4. The duel number sheet (`card_icon03`)

A single sheet with LP digits, time, keys and multipliers; different hash per language. Recipe chosen by the user (`tools/ui_textures/icon03_languages.py`, rerun with `--apply`):
- rows 0-180 (small digits and signs, orange keys 1/2/3, big digits 0-9 with "LP", small digits 0-9): **from the US pack**, crisp pixel art;
- cells in which the European game differs from the US pack (black check mark, grey ball, empty pill, time word): **original pixels enlarged 4x without smoothing**; time word **TIEMPO**; the orange pill ("Single" in the US pack) stays **empty**;
- rows >= 181 (multipliers x1..x12, icons, cards, arrows): from the Italian sheet already in the pack (`tools/data/card_icon03_base_it.png`);
- the European cells are pasted **only in their band** of rows (otherwise they spoil the top of the big digits).

Files: it -> `ui_it/duel_texts/basic_ii__card_icon03.png` (hash 376925c7); fr -> `upscale_extra/3e5482fd.png`; en ee0c44c3; de ffe309a6; es 859eea2b. Previews in `comparisons/icon03/`.

## B5. Title plate

`python tools/ui_textures/mystic_tomato_title.py es` generates 2 PNGs (`542eff79685c434d`, `705176739829dcf5`, tiles 18 and 19 of the 20-tile 128x64 backdrop `title_menu_i.ehp: main_title00001..00020`) with card 4930 in the language + the "version" wording + the flag, PT Sans Bold font: **"EDICIÓN TOMATE MÍSTICO"**. The plate **is included only for the chosen language** (it lives in `modules/es/intro/title_screen/`); the original base pack has the tiles without a banner. Files in this pack: `moduli/es/intro/title_screen/00000000542eff79685c434d.png`, `moduli/es/intro/title_screen/00000000705176739829dcf5.png`.

## B6. `textures.ini` and composition

`tools/gen_ini.py TOOLS US_INI CARD_DIR OUT_INI i=it +extra_it.ini +ui_it.ini +data/upscale_extra.ini` converts the US `textures.ini` into the EU one: the non-card entries stay (neutral textures = same hashes); the card entries are regenerated from the EU `card/*.cip` archives for the 5 languages (`i=it` remaps `cards/large/X.png` -> `cards/large_it/X.png`); it adds the Spell/Trap label (`extra_it.ini`), the `ui_it` lines and `upscale_extra.ini`. It is also done for the 3 card styles. If the same pixels exist in several languages the first in `e i f g s` wins (for this reason atlas, banner and attribute table are "one per installation").

`ui_es` lines in `es.ini`: 87. Prefix frequency: `docs/changes_es/ini_lines.csv`. Check: every `ui_es/...` line must point to an existing file and there must be no duplicate hashes.

## B7. Installation and settings

PC: copy `ULES00600` into `<PPSSPP>/PSP/TEXTURES/` (Android: `textures.zip` in `.../TEXTURES/ULES00600/`, without extracting it; regenerate the zip with the corrections). Settings: **Replace textures ON**, rendering resolution **4x**, game language = module language (the language is stored in the **save file**). After changing a single PNG it is enough to copy it and restart PPSSPP (cache). To try the texts use the `_definitiva` ISO.

---

# C. EDITORIAL CHOICES

- **Rector Sheppard** (as in the dialogues) in the cards and maps ("Oficina del Rector"); dormitories **Slifer Rojo, Ra Amarillo, Obelisco Azul**; **Jinetes de la Sombra**; "Habitación" instead of "Alójese" (Room).
- Sake/shochu and maid outfit as in the other languages (`st01_t01/Scr003E`), `st02_t01/Scr101E` rotated; "Sirviente de la Calavera", "Toon", "Archidemonio", "Trío Ojama" and name accents as on the cards.
- Options: "EN/FUERADE" -> "ON/OFF"; title messages ("nuevos datos de juego"), tutorial lessons ("le turno" -> "es el turno de", swapped x/o keys, closed color codes), final paragraph of the Tag Duels translated (it was truncated/in English).
- Terms left as in the game: "Invocación por Sacrificio", "Tributar", "Efecto de Blanco", "Tronco" (open questions in `docs/changes_es/open_questions_es.md`).
- Number sheet: digits/LP from the US pack, x1..x12 from the Italian sheet, time word TIEMPO.

### Entries of the choices register for this language (`tools/data/editorial_choices.json`)
| id | original | corrected | inherited | reason |
|---|---|---|---|---|
| st01_t01/Scr003E#146 | Mi padre es el dueño de una⏎empresa de salsa picante. | Mi padre es el dueño de una⏎destilería de sake. | no | sake instead of hot sauce (faithful to the Japanese: Chumley's family makes sake) |
| st01_t01/Scr003E#147 | En la última paga me envió⏎un poco de salsa picante.⏎Te haré un descuento razonable.⏎¿Quieres...? | En la última paga me envió⏎un poco de shochu.⏎Te haré un descuento razonable.⏎¿Quieres...? | no | shochu instead of hot sauce |
| st01_t01/Scr003E#150 | Mi padre es el dueño de una⏎empresa de salsa picante. | Mi padre es el dueño de una⏎destilería de sake. | no | same as 146 |
| st01_t01/Scr003E#151 | En la última paga me envió⏎un poco de salsa picante.⏎Te haré un descuento razonable.⏎¿Quieres...? | En la última paga me envió⏎un poco de shochu.⏎Te haré un descuento razonable.⏎¿Quieres...? | no | same as 147 |
| st01_t01/Scr003E#163 | Vaya... Lo has conseguido.⏎Es 《C026_2》...⏎¡Y lleva un bikini! | Vaya... Lo has conseguido.⏎Es 《C026_2》...⏎¡Y va vestida de criada! | no | maid outfit instead of bikini (Japanese: メイド服) |
| st01_t01/Scr003E#168 | Vaya... Lo has conseguido.⏎Es 《C026_2》...⏎¡Y lleva un bikini! | Vaya... Lo has conseguido.⏎Es 《C026_2》...⏎¡Y va vestida de criada! | no | same as 163 |
| st01_t01/Scr003E#188 | Bueno, supongo que hago⏎mis pinitos... | None | yes | Italian only: "sto sbavando" was a translation error (Japanese: "I am not that good") |
| st01_t01/Scr003E#189 | Oye,⏎¿puedes hacerme un dibujo?⏎¡Dibújame a 《C026_2》 en bikini! | Oye,⏎¿puedes hacerme un dibujo?⏎¡Dibújame a 《C026_2》 vestida de criada! | no | maid outfit instead of bikini |
| st01_t01/Scr003E#191 | ¡Ten, puedes usar éste! | ¡Ten, usa este traje de criada! | no | Syrus hands over a maid outfit as a model (メイド服): with the bikini the joke made no sense |
| st01_t01/Scr003E#194 | Bueno, supongo que hago⏎mis pinitos... | None | yes | same as 188 |
| st01_t01/Scr003E#195 | Oye,⏎¿puedes hacerme un dibujo?⏎¡Dibújame a 《C026_2》 en bikini! | Oye,⏎¿puedes hacerme un dibujo?⏎¡Dibújame a 《C026_2》 vestida de criada! | no | same as 189 |
| st01_t01/Scr003E#197 | ¡Ten, puedes usar éste! | ¡Ten, usa este traje de criada! | no | same as 191 |

Other choices and the re-reading of the duel sentences: `docs/EDITORIAL_CHOICES.md`.

# D. IN-GAME VERIFICATION

- **Seen in game** (`_definitiva` ISO + `es` module, new game in Spanish, 2026-10-12): language selection, title with the "EDICIÓN TOMATE MÍSTICO" plate and "PRESIONA EL BOTÓN START", Juego Nuevo/Continuar, "INTRODUCE EL NOMBRE", save system messages, HD Menú Principal, Lista de Duelistas, deck editor (tabs Deck/Fusión/Side/Tronco, "Tipos de carta en posesión"), Opciones (ON/OFF, help).
- **Not seen** (only read and compared with the original in the comparison sheets): duel (Cadena, Ataque Directo, end of duel, VS, rock-paper-scissors), tutorial and lessons, shop, laboratory, calendar, cards with new text, corrected story dialogues, duel sentences.

# E. HOW TO REGENERATE EVERYTHING

```
# ISO (all languages together)
python tools/corrections/build_dialogues.py es
python tools/corrections/generate_card_corrections.py es CARDINFO_es.ehp          # cards
python tools/corrections/apply_to_iso.py PSP/GAME/ULES00600_..._EUR.iso PSP/GAME/ULES00600_..._EUR_definitiva.iso
# images
python tools/generate_language.py fr PACK CARDINFO US_INI CLEAN_DIR OUT [ID...]
TF1_LANG=es python tools/ui_textures/<family>.py USRDIR PACK_US <module>      # for each of the 8 families (whole!)
python tools/ui_textures/icon03_languages.py --apply ; python tools/ui_textures/mystic_tomato_title.py es
python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules USRDIR/card OUT es --copy
# this document
python tools/analysis/document_changes.py ISO_ORIG ISO_DEF es docs/changes_es
python tools/analysis/document_pack.py ISO_ORIG es docs/changes_es
python tools/analysis/text_comparisons.py es
python tools/analysis/write_changes_document.py es
```
External inputs you need (check that they exist): the original ISO, the extracted USRDIR (`tools/analysis/extract_usrdir.py`), MikeyMK's US pack `ULUS10136` (in a folder outside the project).

# F. LIMITS AND OPEN POINTS

- User questions resolved on 2026-10-12 (broken card names corrected to the official name, Kaiba Corporation, capitalized Duelo, Rector, Sacrificio instead of Tributo): `docs/changes_es/open_questions_es.md`.
- 14 Spanish textures without HD (fragments without text: `recipe_sel`, `t_window0002`, `limitlist window_s0010/20`, `jyanken100005/7`, `recipe010011`, `bg_base_cloud02`) stay like the original.
- Android `textures.zip`: not done; no test on a phone. The texts drawn in the textures are in `docs/changes_es/texture_texts_es.md` (read by eye).
- The speaker name in the dialogue box cannot be modified (encrypted EBOOT).
