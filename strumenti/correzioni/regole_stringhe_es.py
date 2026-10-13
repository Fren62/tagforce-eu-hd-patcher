"""Correzioni alle stringhe spagnole dell'interfaccia (tabelle strTbl*, help_strtbl_*, ddstrtbl, field_strtbl* nei .ehp della ISO): schede dei
duellisti, record dei duelli, aiuti e tutorial dell'editor del deck e del duello, oggetti e mappe, laboratorio, negozio. Applicate da
stringhe_ui.py (anche con testo piu' lungo dell'originale).
STRINGHE: (archivio sotto /PSP_GAME/USRDIR, membro, indice, [(vecchio, nuovo), ...], motivo): ogni 'vecchio' deve comparire nella stringa.
GLOBALI: (regex, sostituzione, motivo) applicate a tutte le stringhe delle TABELLE (prima le STRINGHE, poi i GLOBALI, nell'ordine scritto).
Gli indici sono quelli della tabella (0-based). Le stesse tabelle esistono identiche negli archivi di tutte le regioni (always_*_spa, basic_*s)."""

CH = ('database/charalist.ehp', 'strTbl_s.bin')
DR = ('database/duelrecord.ehp', 'strTbl_s.bin')
RE = ('duel/result/result_s.ehp', 'strTbl.bin')
TL = ('database/tutoriallist.ehp', 'strTbl_s.bin')
DK = ('deck/all_s.ehp', 'strTbl.bin')
HC = ('deck/all_s.ehp', 'help_strtbl_contents.bin')
TU = ('deck/tutorial.ehp', 'strTbl_s.bin')
DD = ('duel/basic_*s.ehp', 'ddstrtbl_s.bin')
HD = ('duel/basic_*s.ehp', 'help_strtbl_contents_duel_s.bin')
ST = ('duel/start/start_s.ehp', 'strTbl_s.bin')
FS = ('field/always_*_spa.ehp', 'field_strtbl.bin')
FI = ('field/always_*_spa.ehp', 'field_strtbl_item.bin')
FM = ('field/always_*_spa.ehp', 'field_strtbl_mapname.bin')
CV = ('labo/conv_machine.ehp', 'strTbl_s.bin')
PW = ('labo/password.ehp', 'strTbl_s.bin')
SH = ('shop/all_s.ehp', 'strTbl_s.bin')

TM = ('title_menu/title_menu_?.ehp', 'title_msg_s.bin')
OM = [('duel/basic_*.ehp', 'option_msg_s.bin'), ('field/always_*_spa.ehp', 'option_msg_s.bin'), ('title_menu/title_menu_?.ehp', 'option_msg_s.bin')]
TS = ('title_menu/title_menu_?.ehp', 'tushin_msg_s.bin')
OG = [('database/cardalbum.ehp', 'ocg_packname_s.bin'), ('deck/all_?.ehp', 'ocg_packname_s.bin'), ('duel/basic_[bs]?.ehp', 'ocg_packname_s.bin'),
      ('field/always_[bfgis]??_*.ehp', 'ocg_packname_s.bin')]
EV = ('field/always_*_spa.ehp', 'event_name.bin')
LE = [('tutorial/tutorial_s.ehp', f'0{n}_message_res.bin') for n in (1, 2, 3, 4)]

TABELLE = [CH, DR, RE, TL, DK, HC, TU, DD, HD, ST, FS, FI, FM, CV, PW, SH, TM, TS, EV] + OM + OG + LE

# --- indici precisi (stessi indici in duelrecord e result: le due tabelle sono identiche) ---
STRINGHE = []
for T in (DR, RE):
    STRINGHE += [
        (T[0], T[1], 130, [("en batalla durante", "usando efectos durante")], "mancava la traduzione di 'using effects' (diceva 'en batalla' come la riga prima)"),
        (T[0], T[1], 179, [("Nivel 4 o superior", "Nivel 4 o inferior")], "l'inglese dice 'Level 4 or lower'"),
        (T[0], T[1], 124, [("Ganados 100 lanzamientos", "Ganados 10 lanzamientos")], "it, fr, de ed en dicono 10 lanci"),
    ]

GLOBALI = [
    # --- nomi dei dormitori e dei gruppi: gli stessi dei dialoghi e delle carte ---
    (r"\bSlifer Red\b", "Slifer Rojo", "nome del dormitorio come nei dialoghi"),
    (r"\bRa Yellow\b", "Ra Amarillo", "nome del dormitorio come nei dialoghi"),
    (r"\bObelisk Blue\b", "Obelisco Azul", "nome del dormitorio come nei dialoghi"),
    (r"\bShadow Rid(?:er|re)s\b", "Jinetes de la Sombra", "nome del gruppo come nei dialoghi (e refuso Ridres)"),
    (r"\bDuelista Shadow\b", "Duelista de la Sombra", "come 'duelista de sombra' nei dialoghi"),
    (r"\bArchifiend\b", "Archidemonio", "nome della famiglia di carte"),
    (r"\bTrio Ojama\b", "Trío Ojama", "nome della carta, accento"),
    (r"Cañon Magico Mega Ton", "Cañón Mágico Mega Ton", "nome della carta, accenti"),
    (r"XYZ-Dragón Cañon", "XYZ-Dragón Cañón", "nome della carta, accento"),
    (r"Catapulta Cañon", "Catapulta Cañón", "nome della carta, accento"),
    (r'"Magica de Campo”', '"Mágica de Campo"', "accento e virgolette"),
    (r"\bMagicas\b", "Mágicas", "accento"),
    (r"\bMagica\b", "Mágica", "accento"),
    # --- termini del gioco: come nelle carte ---
    (r"Criado de Cráneo", "Sirviente de la Calavera", "nome della carta"),
    (r"\b([Mm])onstruos Cómicos\b", r"\1onstruos Toon", "le carte usano Toon"),
    (r"\bmonstruos Animados\b", "monstruos Toon", "le carte usano Toon"),
    (r"Invocación por Fusión", "Invocación de Fusión", "termine come sulle carte"),
    (r"Invocación por Ritual", "Invocación de Ritual", "termine come sulle carte"),
    (r"Invocación por Volteo", "Invocación de Volteo", "termine come sulle carte"),
    (r"Efecto de Disparado de Múltiple", "Efecto de Disparo Múltiple", "grammatica"),
    (r"Efecto de Disparado", "Efecto de Disparo", "grammatica (coincide con '(Continua, Encendido, Disparo, Volteo)')"),
    (r"Trampas de Contraataque", "Trampas de Contraefecto", "termine come sulle carte"),
    (r"\bBonus Afortunada\b", "Bonus Suerte", "concordanza"),
    (r"\bBonus Union\b", "Bonus Unión", "accento"),
    (r"Retirados e a partida", "Retirados de la partida", "refuso"),
    (r"Contradores de Magia", "Contadores de Magia", "refuso"),
    (r"Número de veces que se invocó monstruos", "Número de veces que se invocaron monstruos", "concordanza"),
    (r"Invocación Normal a 10 monstruos durante un duelo\.", "Realizadas 10 Invocaciones Normales durante un duelo.", "coerenza con le righe vicine"),
    (r"Contraatacadas Magias, Trampas efectos, Ataques e Invocaciones de tu enemigo 10 veces durante un duelo\.",
     "Contraatacados 10 veces Magias, Trampas, efectos, Ataques e Invocaciones de tu oponente durante un duelo.", "virgole e 'oponente'"),
    (r"con un ataque simple y se ganó", "con un solo ataque o efecto y se ganó", "l'inglese dice 'single attack or effect'"),
    (r"Gana durante el turno de tu oponente\.", "Se ganó durante el turno de tu oponente.", "tempo verbale come le righe vicine"),
    (r"Gana un duelo usando los Efectos de", "Se ganó un duelo usando los efectos de", "tempo verbale come le righe vicine"),
    (r"^botón ×: siguiente$", "Botón ×: siguiente", "maiuscola come la riga dopo"),
    # --- schede dei duellisti ---
    (r"en el atolladero en que se encuentre", "en qué atolladero se encuentre", "grammatica"),
    (r"fusión de cartas de Héroe Elemental", "Fusión de cartas de Héroe Elemental", "maiuscola del termine del gioco"),
    (r"gente fuerte, de confiar,", "gente fuerte, de confianza,", "refuso"),
    (r"lo hacia desde", "lo hacía desde", "accento"),
    (r"suave de los que su nombre", "suave de lo que su nombre", "grammatica"),
    (r"explicar porqué le retuvieron", "explicar por qué le retuvieron", "por qué"),
    (r"porqué le retuvieron", "por qué le retuvieron", "por qué"),
    (r"la cual\.\.\.hace tiempo", "la cual... hace tiempo", "spazio"),
    (r"atractivas monstruos femeninas", "atractivos monstruos femeninos", "concordanza"),
    (r'llamado a "Chica Cibernética"', 'llamado "Chica Cibernética"', "preposizione di troppo"),
    (r"como ser humano Y gracias", "como ser humano. Y gracias", "punteggiatura"),
    (r"en lo  primero que tenga a mano", "en lo primero que tenga a mano", "spazio"),
    (r"Clama tener seis Decks", "Afirma tener seis Decks", "'clamar' non e' 'afirmar'"),
    (r"nadie que no se Vellian ha usado alguna vez una", "nadie que no sea Vellian ha usado jamás una", "refuso"),
    (r'carta principal es Golem de Mecanismo Antiguo",', 'carta principal es "Golem de Mecanismo Antiguo",', "virgolette mancanti"),
    (r"Nadie sabe que tipo de Deck", "Nadie sabe qué tipo de Deck", "accento"),
    (r"saber que le pasará al hombre", "saber qué le pasará al hombre", "accento"),
    (r"actividades en el campus Pero", "actividades en el campus. Pero", "punteggiatura"),
    (r"en el campus Pero Alexis", "en el campus. Pero Alexis", "punteggiatura"),
    (r"para poder matricular y verle", "para poder matricularse y verle", "grammatica"),
    (r"también pudiera tener este poder de efecto especial como un espíritu$", "También pudiera tener este poder de efecto especial como un espíritu.", "punto finale"),
    (r"signo del destino\.\.\n", "signo del destino...\n", "punti di sospensione"),
    (r"señal del destino\.\.\n", "señal del destino...\n", "punti di sospensione"),
    (r"sella dentro de una carta el alma de perdedor", "sella dentro de una carta el alma del perdedor", "articolo"),
    (r'tiene como a "Dragón de Oscuridad de Ojos Rojos" como carta principal', 'tiene a "Dragón de Oscuridad de Ojos Rojos" como carta principal', "grammatica"),
    (r"^Perfil de Sheppard del Principio$", "Perfil del Rector Sheppard", "'Principal' tradotto 'Principio'; Rector come nei dialoghi"),
    (r"Asaltante Veladora de Tumbas", "Asaltante del Cuidador de Tumba", "nome della carta"),
    # --- editor del deck e tutorial ---
    (r"^Sin límite\.$", "Sin límite", "punto finale in piu'"),
    (r"mostrarán todas las cartas ¿Aceptas\?", "mostrarán todas las cartas. ¿Aceptas?", "punteggiatura"),
    (r"es una Carta Limitada, sólo 2 pueden", "es una Carta Semi-Limitada, sólo 2 pueden", "l'inglese dice Semi-Limited"),
    (r"está in correcta", "es incorrecta", "refuso"),
    (r"^Acerca del Menú Editar Deck\.$", "Acerca del Menú Editar Deck", "punto finale in piu'"),
    (r"Acerca de las carta$", "Acerca de las cartas", "plurale"),
    (r'^Cosas que puedes hacer en "Draw Phase"\.$', 'Cosas que puedes hacer en "Draw Phase"', "punto finale in piu'"),
    (r"(Día 3: Invocación de Tributo y Fundamentos de Magias y Trampas)\.$", r"\1", "punto finale in piu'"),
    (r"Invocación de Tributo", "Invocación por Sacrificio", "termine ufficiale spagnolo (Invocada por Sacrificio), come nelle carte"),
    (r"Invocaciones de Tributo", "Invocaciones por Sacrificio", "termine ufficiale spagnolo, come nelle carte"),
    (r"¿Qué es una Deck Receta\?", "¿Qué es una Receta de Deck?", "ordine delle parole"),
    (r"^Trampa Normales$", "Trampas Normales", "plurale"),
    (r"^Trampa Continuas$", "Trampas Continuas", "plurale"),
    (r"●Contador Mágico", "●Contadores Mágicos", "plurale"),
    (r"Los Contador Mágico", "Los Contadores Mágicos", "plurale"),
    (r"●Mira bocarriba carta", "●Mirar boca arriba una carta", "traduzione di 'Pick up card'"),
    (r"Poner bocarriba carta significa", "Mirar boca arriba una carta significa", "traduzione di 'Pick up card'"),
    (r"Zone del Deck de Fusión", "Zona del Deck de Fusión", "refuso"),
    (r"Flujo el Turno", "Flujo del Turno", "refuso"),
    (r"^colocar \(Invocación Normal\)$", "Colocar (Invocación Normal)", "maiuscola"),
    (r"●Colocar de Cartas Mágicas y de Cartas de Trampa", "●Colocar Cartas Mágicas y Cartas de Trampa", "grammatica"),
    (r"\(Fase de Final\)", "(Fase Final)", "come le altre"),
    (r"Fase  de Batalla", "Fase de Batalla", "spazio"),
    (r"Deck- tienen que ser 3", "Deck: tienen que ser 3", "punteggiatura"),
    (r"Colocando Etiquetas a tus cartas favoritas o importantes hará", "Colocar Etiquetas en tus cartas favoritas o importantes hará", "grammatica"),
    (r"Devuelve una carta que acaba de moverse de otra vez a su posición original\.", "Devuelve a su posición original una carta que acaba de moverse.", "frase rotta"),
    (r"requerimientos\n(Esto es similar a la función)", r"requerimientos.\n\1", "punto mancante"),
    (r"etc\.,en un Deck", "etc., en un Deck", "spazio"),
    (r"de cual Deck se basa en tipo de concepto", "de cuál Deck se basa en qué tipo de concepto", "accenti"),
    (r"botón ×    Mover carta seleccionada Las cartas por lo general", "botón ×\n   Mover carta seleccionada\n   Las cartas por lo general", "a capo mancanti (come l'inglese)"),
    (r"Cartas de Monstruos de Fusión”", 'Cartas de Monstruo de Fusión"', "concordanza"),
    (r"Cartas de Monstruos de Fusión\"", 'Cartas de Monstruo de Fusión"', "concordanza"),
    (r"Carta de Magica llamada", "Carta Mágica llamada", "grammatica"),
    (r"Carta de Magia llamada", "Carta Mágica llamada", "grammatica"),
    (r"Polimerizacion", "Polimerización", "accento"),
    (r"hacer Invocación de Fusión a este tipo especial de monstruo", "hacer una Invocación de Fusión de este tipo especial de monstruo", "grammatica"),
    (r"Mientras carta esté boca arriba", "Mientras esta carta esté boca arriba", "articolo mancante"),
    (r"(?m)^os efectos generalmente", "Los efectos generalmente", "iniziale mancante"),
    (r"La misma se usa el mismo orden", "Se usa en el mismo orden", "grammatica"),
    (r"as Cartas de Trampa tienen diversos", "las Cartas de Trampa tienen diversos", "refuso"),
    (r"una Trampa de Carta", "una Carta de Trampa", "ordine delle parole"),
    (r"efecto de l Carta de Trampa", "efecto de la Carta de Trampa", "refuso"),
    (r"incluso durante el turno de tu oponente\.\nAdemás", "incluso durante tu propio turno.\nAdemás", "l'inglese dice 'your own turn'"),
    (r'"Siete Herramientas del Bandido"\'', '"Siete Herramientas del Bandido"', "apostrofo di troppo"),
    (r'efecto de negación de la Carta de Trampa "Disruptor Mágico"', 'efecto de negación de Cartas Mágicas de "Disruptor Mágico"', "l'inglese dice Spell Card-negating"),
    (r"Spell Speed 2 Cadenas encadenarse", "Spell Speed 2 pueden encadenarse", "'pueden' sostituito per errore da 'Cadenas'"),
    (r"no Cadenas encadenarse a cartas", "no pueden encadenarse a cartas", "'pueden' sostituito per errore da 'Cadenas'"),
    (r"solamente Cadenas encadenarse cartas", "solamente pueden encadenarse cartas", "'pueden' sostituito per errore da 'Cadenas'"),
    (r"no Cadenas haber encadenamiento", "no puede haber encadenamiento", "'puede' sostituito per errore da 'Cadenas'"),
    (r"ninguna ora activación", "ninguna otra activación", "refuso"),
    (r"Monstruos de Efectos\n", "Monstruos de Efecto\n", "concordanza"),
    (r"Mágicas de Juego Rápido / Mágicas Normales\nMonstruos de Efecto", "Mágicas de Juego Rápido / Trampas Normales\nMonstruos de Efecto", "l'inglese dice Normal Traps"),
    (r"Cartas Prohibidas, Limitadas y Semilimitadas", "Cartas Prohibidas, Limitadas y Semi-Limitadas", "come nel resto"),
    (r"cuando t dicen que robes", "cuando te dicen que robes", "refuso"),
    (r"Los efectos no tienen como blanco a carta\(s\) específica\(s\)", "Los efectos que no tienen como blanco a carta(s) específica(s)", "grammatica"),
    (r"o efecto que tienen como blanco", "o efectos que tienen como blanco", "concordanza"),
    # tutorial
    (r"decidir hacia donde moverla", "decidir hacia dónde moverla", "accento"),
    (r"otra vez e botón", "otra vez el botón", "refuso"),
    (r"estas cartas  particular han", "estas cartas en particular han", "parola mancante"),
    (r"Botón × : confirma", "Botón ×: confirma", "spazio"),
    (r'en una "Matchs"', 'en una "Match"', "plurale errato"),
    (r"preguntándote que tipo", "preguntándote qué tipo", "accento"),
    (r"de acuerdo al DEF de cada monstruo", "de acuerdo a la DEF de cada monstruo", "genere di DEF come sulle carte"),
    (r"botón △para", "botón △ para", "spazio"),
    (r"el Deck editando en esos momentos\.", "el Deck que estás editando en este momento.", "grammatica"),
    (r'Seleccionando "Búsqueda" después de teclear', 'Seleccionando "Ejecutar" después de teclear', "il pulsante si chiama Ejecutar (l'inglese: Run)"),
    (r"o el botó R\.", "o el botón R.", "refuso"),
    (r"Descripciónes", "Descripciones", "refuso"),
    (r"Parece que has adquirido práctica con unas cuantas cartas\.", "Parece que has conseguido unas cuantas cartas.", "mal tradotto ('gotten your hands on')"),
    # --- duello ---
    (r"^Rindes$", "Rendirse", "etichetta del pulsante"),
    (r"eliminadas", "retiradas", "'retirar' come nel resto del gioco"),
    (r"Los Puntos Vida de", "Los Puntos de Vida de", "preposizione mancante"),
    (r"Tus Puntos Vida han", "Tus Puntos de Vida han", "preposizione mancante"),
    (r"Te rendiste rendido debido", "Te rendiste debido", "ripetizione"),
    (r"se reducen 0\.", "se reducen a 0.", "preposizione mancante"),
    (r'un "Match" está compuesta', 'un "Match" está compuesto', "concordanza"),
    (r"de toda el Match", "de todo el Match", "concordanza"),
    (r"Roba cartas desde aquí y para añadirlas a tu mano\.", "Roba cartas desde aquí y añádelas a tu mano.", "grammatica"),
    (r"Esta carta esta excluida", "Esta carta está excluida", "accento"),
    (r"El efecto de esta Magica se aplica", "El efecto de esta Carta Mágica se aplica", "grammatica"),
    (r"mediante Piedra Papel Tijeras", "mediante Piedra, Papel o Tijeras", "punteggiatura"),
    (r"continúas al duelo siguiente", "continúas con el duelo siguiente", "preposizione"),
    (r"\(Si no en este momento no quedan", "(Si en este momento no quedan", "refuso"),
    (r" - colocar de una Carta de Trampa o de una Carta Mágica", " - Colocar una Carta de Trampa o una Carta Mágica", "grammatica"),
    (r"Invocar a in monstruo", "Invocar a un monstruo", "refuso"),
    (r'a la colocar de una Carta de Monstruo en el campo en Posición de Defensa boca abajo se la llama una "colocar"\.',
     'a colocar una Carta de Monstruo en el campo en Posición de Defensa boca abajo se le llama "Colocar".', "frase rotta"),
    (r"boca arriba esto se le llama una", "boca arriba, a esto se le llama una", "grammatica"),
    (r"La colocar de Cartas Mágicas y de Trampa se diferencia de la colocar de Cartas de Monstruo", "Colocar Cartas Mágicas y de Trampa se diferencia de Colocar Cartas de Monstruo", "frase rotta"),
    (r"de la carta siendo usada,\n", "de la carta siendo usada.\n", "punteggiatura"),
    (r"Casa Paso de la Battle Phase", "Cada Paso de la Battle Phase", "refuso"),
    (r"regresarás a la Battle Step", "regresarás al Battle Step", "genere"),
    (r"Posición de Batalla de monstruo que es el blanco", "Posición de Batalla del monstruo que es el blanco", "articolo"),
    (r"tiene un DEF más bajo", "tiene una DEF más baja", "genere di DEF come sulle carte"),
    (r"tiene un DEF más alto", "tiene una DEF más alta", "genere di DEF come sulle carte"),
    # paragrafo finale degli aiuti dei Duelos Tag
    (r"\n\nif Player C of Team 2 has attacked during his/her Battle Phase.*?in response to the attack\.\n", "", "residuo inglese: il paragrafo e' gia' tradotto subito dopo"),
    (r"que tubo su turno justo antes de eso", "que tuvo su turno justo antes de eso", "refuso"),
    (r"sera capaz de elegir", "será capaz de elegir", "accento"),
    (r"Asumiendo que el duelo se juega de acuerdo al siguiente,\n(Equipo 1: Jugador A\nEquipo 2: Jugador C\nEquipo 1: Jugador B\nEquipo 2: Jugador D\n)(\n)",
     r"Asumiendo que el duelo se juega de acuerdo con el siguiente orden,\n\n\1\2", "frase incompleta"),
    (r"Asumiendo que el duelo se juega de acuerdo al siguiente,\n(Equipo 1: Jugador A\nEquipo 2: Jugador C\nEquipo 1: Jugador B\nEquipo 2: Jugador D)\n?$",
     "Asumiendo que el duelo se juega de acuerdo con el siguiente orden,\n\n\\1\n\n"
     "si el Jugador C del Equipo 2 ha atacado durante su Battle Phase, el jugador que tuvo su turno justo antes de eso, que es el Jugador A del Equipo 1, "
     "podrá elegir si quiere o no activar una Carta Mágica de Juego Rápido o una Trampa como respuesta al ataque.",
     "testo troncato: mancava il paragrafo finale (tradotto dall'inglese)"),
    # --- campo, oggetti, mappe, laboratorio, negozio ---
    (r"^¡No hay a quién dárselo\.!$", "¡No hay a quién dárselo!", "punteggiatura"),
    (r"^Trar$", "Comer", "l'inglese dice Eat"),
    (r"^¿Tirar bocadillo\?$", "¿Comer bocadillo?", "l'inglese dice 'Eat a sandwich?'"),
    (r"\$C0 ！", "$C0!", "punto esclamativo a larghezza piena e spazio"),
    (r"^MIE$", "MIÉ", "accento"),
    (r"^SAB$", "SÁB", "accento"),
    (r"^¡ %s adquirido!$", "¡%s adquirido!", "spazio"),
    (r"etc\.que no hayan", "etc., que no hayan", "punteggiatura"),
    (r"La belleza esta en su sabor", "La belleza está en su sabor", "accento"),
    (r"una maestro pastelero", "un maestro pastelero", "concordanza"),
    (r"Es divertido mascarlo\.", "Es divertido masticarlo.", "refuso"),
    (r"artesanalmente\.\. Sabe", "artesanalmente. Sabe", "punteggiatura"),
    (r"los cual explica porqué siempre se venden todos", "lo cual explica por qué siempre se agotan", "refuso"),
    (r"una hígado de ganso", "un hígado de ganso", "concordanza"),
    (r"^Alójese (\d+)$", r"Habitación \1", "il nome inglese e' Room"),
    (r"^Academia del duelo$", "Academia de Duelos", "come nel resto del gioco"),
    (r"^Una tienda$", "Tienda", "articolo di troppo"),
    (r"^La Oficina de canciller$", "Oficina del Rector", "'Rector' come nei dialoghi"),
    (r"^Cliff$", "Acantilado", "residuo inglese"),
    (r"^Dorm abandonado$", "Dormitorio abandonado", "abbreviazione inglese"),
    (r"^Último Arena$", "Última Arena", "genere"),
    (r"No hay cartaseleccionadas", "No hay cartas seleccionadas", "spazio mancante"),
    (r"La contraseña introducida está incorrecta", "La contraseña introducida es incorrecta", "ser/estar"),
    (r"esta carya", "esta carta", "refuso"),
    (r"^Esperando por oponente\.\.\.$", "Esperando al oponente...", "grammatica"),
    # --- messaggi del titolo, opzioni, rete, pacchetti, eventi ---
    (r"Yu-Gi- Oh!", "Yu-Gi-Oh!", "spazio"),
    (r"^Derotar Crowler$", "Derrotar a Crowler", "refuso"),
    (r"^Para princiiantes$", "Para principiantes", "refuso"),
    (r"nuevos dato de juego", "nuevos datos de juego", "concordanza"),
    (r"botón □ : Selección", "botón □: Selección", "spazio"),
    (r"Austes del sonido", "Ajustes del sonido", "refuso"),
    (r"Austa el volumen", "Ajusta el volumen", "refuso"),
    (r"^EN$", "ON", "'EN' non e' ON (l'inglese dice ON)"),
    (r"^FUERADE$", "OFF", "'FUERADE' e' un refuso per OFF"),
    (r"^SIN LIMITE DE TIEMPO$", "SIN LÍMITE DE TIEMPO", "accento"),
    (r"^NO LIMITE$", "SIN LÍMITE", "spagnolo corretto"),
    (r"Mientras en el modo ad hoc, sostenga el botón SELECT", "Mientras estés en modo ad hoc, mantén presionado el botón SELECT", "registro: tutto il gioco da' del tu"),
    (r"para desconectar y devolver al menú principal", "para desconectar y volver al menú principal", "grammatica"),
    (r"presiona el botón ×\$C0, y confirmar\.", "presiona el botón ×$C0, y confirma.", "imperativo"),
    (r"COLECCCIONABLES", "COLECCIONABLES", "refuso"),
    (r"^Escogido entre representante\.$", "Elegido entre los representantes.", "grammatica"),
    (r"^Interscholastic se baten en duelo\.$", "Duelo interescolar.", "residuo inglese"),
    (r"^Antes de una reunión\.$", "El día antes del torneo Tag Force.", "l'inglese: the day before the Tag Force meet"),
    # --- lezioni del tutorial ---
    (r"Ahora le turno a ", "Ahora es el turno de ", "refuso: 'le turno'"),
    (r"Ahora le turno\na ", "Ahora es el turno\nde ", "refuso: 'le turno'"),
    (r"¡Le turno a\n", "¡Es el turno de\n", "refuso: 'le turno'"),
    (r"Le turno a ", "Es el turno de ", "refuso: 'le turno'"),
    (r"Como te turno\na ti primero, \$0,", "Como el primer turno es\ntuyo, $0,", "refuso: 'te turno'"),
    (r"\$C5Sryus", "$C5Syrus", "refuso"),
    (r"\$CALP\$ de su rival", "$CALP$C0 de su rival", "codice colore non chiuso"),
    (r"Zona de Cartas de Monstruos Después, pulsa", "Zona de Cartas de Monstruos. Después, pulsa", "punteggiatura"),
    (r"tiene una en\nPosición de Ataque", "tiene uno en\nPosición de Ataque", "concordanza (monstruo)"),
    (r"Pero si invocación a un\nmonstruo en vez de\nColocar,", "Pero si invocas a un\nmonstruo en vez de\ncolocarlo,", "refuso: 'invocación' per 'invocas'"),
    (r"e invocación a uno\ncon un ATK menor", "e invocas a uno\ncon un ATK menor", "refuso: 'invocación' per 'invocas'"),
    (r"\$Cpad analógico\$C0", "$C8pad analógico$C0", "codice colore incompleto"),
    (r"debes realizar una Invocación de u ofrecer uno o más monstruos como Tribute\.", "debes realizar una Invocación y ofrecer uno o más monstruos como Sacrificio.", "frase troncata e residuo inglese"),
    (r"^invocación a 1 monstruo\.$", "Invoca a 1 monstruo.", "refuso: 'invocación' per 'invoca'"),
    (r"¡\$0!\ninvocación a un monstruo!", "¡$0!\n¡Invoca a un monstruo!", "refuso: 'invocación' per 'invoca'"),
    (r'Pulsa el botón × para\nabrir el menú de Phase\.\nSelecciona "End Phase" y\nluego pulsa el botón ○\.',
     'Pulsa el botón ○ para\nabrir el menú de Phase.\nSelecciona "End Phase" y\nluego pulsa el botón ×.', "tasti scambiati (l'inglese: ○ apre il menu, × conferma)"),
    (r"que Colocar boca abajo, se pondrán", "que se coloquen boca abajo se pondrán", "grammatica"),
    (r"Primero hay que Colocar\nboca abajo", "Primero hay que colocarlas\nboca abajo", "grammatica"),
    (r"Colocar tu Carta de Trampa\.", "¡Coloca tu Carta de Trampa!", "imperativo"),
    (r"Antes, \$C5Bastion\$C0 ha preguntado", "Antes, $C5Syrus$C0 ha preguntado", "l'inglese dice Syrus"),
    (r"%C5Alexis", "$C5Alexis", "codice colore"),
    (r"aumentan en \$CA200\$\.\.\.", "aumentan en $CA200$C0...", "codice colore non chiuso"),
    (r"disminuyen en \$CA200\$!", "disminuyen en $CA200$C0!", "codice colore non chiuso"),
    (r"¡Ahora me turno!", "¡Ahora es mi turno!", "refuso"),
    (r"\$C5Alexis'\$C0", "$C5Alexis$C0", "apostrofo di troppo"),
    (r"Cartas de Trampas Normales", "Cartas de Trampa Normales", "Trampa e' invariabile"),
    (r"#CACarta", "$CACarta", "codice colore"),
    (r"Zona de de ", "Zona de ", "parola doppia"),
    (r"¡Los monstruo de ", "¡Los monstruos de ", "plurale"),
    (r'"\$C6Umi\$C0" sigue activo,', '"$C6Umi$C0" sigue activa,', "concordanza con Carta Mágica"),
    (r"\bel Hechizo(\s)de(\s)(Campo|Equipo)", r"la Carta Mágica\1de\2\3", "termine come sulle carte (e genere)"),
    (r"\bEl Hechizo(\s)de(\s)(Campo|Equipo)", r"La Carta Mágica\1de\2\3", "termine come sulle carte (e genere)"),
    (r"\bHechizo(\s)de(\s)(Campo|Equipo)", r"Carta Mágica\1de\2\3", "termine come sulle carte"),
    # --- per ultimo: spazi doppi tra parole (le righe 'x: Sí  ○: No' e le rientranze dopo a capo restano) ---
    (r"(?<=[^\s])(?<!Sí)(?<!No)  +(?=[^\s])", " ", "spazio doppio"),
    (r"\bun refinar búsqueda\b", "un filtrado", "terminologia come il menu 'Filtrar'"),
    (r"Refinar Búsqueda", "Filtrar", "terminologia come il menu 'Filtrar'"),
]

# --- nomi di carta ufficiali (strumenti/dati/nomi_ufficiali_es.json, vedi regole_es.py): i nomi citati tra virgolette seguono il cambio ---
import json as _json, os as _os, re as _re
_p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'dati', 'nomi_ufficiali_es.json')
for _v in _json.load(open(_p, encoding='utf-8')).values():
    for _old in {_v['vecchio'], _v['vecchio_raw']}:
        GLOBALI.append(('"' + _re.escape(_old) + '"', '"' + _v['nuovo'] + '"', "nome di carta citato: nome ufficiale"))

# --- 'blanco' -> 'objetivo': i testi ufficiali spagnoli delle carte dicono "selecciona 1 monstruo ... ese objetivo" (target) ---
GLOBALI += [
    (r"\bEfectos de Blanco\b", "Efectos con Objetivo", "terminologia ufficiale: objetivo (target)"),
    (r"\bblanco\b", "objetivo", "terminologia ufficiale: objetivo (target)"),
    (r"\bblancos\b", "objetivos", "terminologia ufficiale: objetivo (target)"),
]

