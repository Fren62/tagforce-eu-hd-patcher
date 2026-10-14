"""Corrections to the Spanish interface strings (strTbl*, help_strtbl_*, ddstrtbl, field_strtbl* tables in the ISO's .ehp files): duelist
cards, duel records, help and tutorial of the deck editor and of the duel, items, maps and menus, laboratory, shop, title and options.
Applied by ui_strings.py (also with text longer than the original).
STRINGS: (archive under /PSP_GAME/USRDIR, member, index, [(old, new), ...], reason): every 'old' must appear in the string.
GLOBALS: (regex, replacement or function, reason) applied to all the strings of the TABLES (first the STRINGS, then the GLOBALS, in the order written).
The indexes are those of the table (0-based). The same tables exist identically in the archives of all the regions (always_*_spa, basic_*s).
Hand reading: comparisons/audit_es/ui_strings_es.tsv."""

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

TABLES = [CH, DR, RE, TL, DK, HC, TU, DD, HD, ST, FS, FI, FM, CV, PW, SH, TM, TS, EV] + OM + OG + LE

# --- exact indexes (same indexes in duelrecord and result: the two tables are identical) ---
STRINGS = []
for T in (DR, RE):
    STRINGS += [
        (T[0], T[1], 130, [("en batalla durante", "usando efectos durante")], "the translation of 'using effects' was missing (it said 'en batalla' like the line before)"),
        (T[0], T[1], 179, [("Nivel 4 o superior", "Nivel 4 o inferior")], "English says 'Level 4 or lower'"),
        (T[0], T[1], 124, [("Ganados 100 lanzamientos", "Ganados 10 lanzamientos")], "it, fr, de and en say 10 throws"),
    ]

GLOBALS = [
    # --- dormitory and group names: the same as in the dialogues and the cards ---
    (r"\bSlifer Red\b", "Slifer Rojo", "dormitory name as in the dialogues"),
    (r"\bRa Yellow\b", "Ra Amarillo", "dormitory name as in the dialogues"),
    (r"\bObelisk Blue\b", "Obelisco Azul", "dormitory name as in the dialogues"),
    (r"\bShadow Rid(?:er|re)s\b", "Jinetes de la Sombra", "group name as in the dialogues (and typo Ridres)"),
    (r"\bDuelista Shadow\b", "Duelista de la Sombra", "as 'duelista de sombra' in the dialogues"),
    (r"\bArchifiend\b", "Archidemonio", "name of the card family"),
    (r"\bTrio Ojama\b", "Trío Ojama", "card name, accent"),
    (r"Cañon Magico Mega Ton", "Cañón Mágico Mega Ton", "card name, accents"),
    (r"XYZ-Dragón Cañon", "XYZ-Dragón Cañón", "card name, accent"),
    (r"Catapulta Cañon", "Catapulta Cañón", "card name, accent"),
    (r'"Magica de Campo”', '"Mágica de Campo"', "accent and quotation marks"),
    (r"\bMagicas\b", "Mágicas", "accent"),
    (r"\bMagica\b", "Mágica", "accent"),
    # --- game terms: as in the cards ---
    (r"Criado de Cráneo", "Sirviente de la Calavera", "card name"),
    (r"\b([Mm])onstruos Cómicos\b", r"\1onstruos Toon", "the cards use Toon"),
    (r"\bmonstruos Animados\b", "monstruos Toon", "the cards use Toon"),
    (r"Invocación por Fusión", "Invocación de Fusión", "term as on the cards"),
    (r"Invocación por Ritual", "Invocación de Ritual", "term as on the cards"),
    (r"Invocación por Volteo", "Invocación de Volteo", "term as on the cards"),
    (r"Efecto de Disparado de Múltiple", "Efecto de Disparo Múltiple", "grammar"),
    (r"Efecto de Disparado", "Efecto de Disparo", "grammar (matches '(Continua, Encendido, Disparo, Volteo)')"),
    (r"Trampas de Contraataque", "Trampas de Contraefecto", "term as on the cards"),
    (r"\bBonus Afortunada\b", "Bonus Suerte", "agreement"),
    (r"\bBonus Union\b", "Bonus Unión", "accent"),
    (r"Retirados e a partida", "Retirados de la partida", "typo"),
    (r"Contradores de Magia", "Contadores de Magia", "typo"),
    (r"Número de veces que se invocó monstruos", "Número de veces que se invocaron monstruos", "agreement"),
    (r"Invocación Normal a 10 monstruos durante un duelo\.", "Realizadas 10 Invocaciones Normales durante un duelo.", "consistency with the neighbouring lines"),
    (r"Contraatacadas Magias, Trampas efectos, Ataques e Invocaciones de tu enemigo 10 veces durante un duelo\.",
     "Contraatacados 10 veces Magias, Trampas, efectos, Ataques e Invocaciones de tu oponente durante un duelo.", "commas and 'oponente'"),
    (r"con un ataque simple y se ganó", "con un solo ataque o efecto y se ganó", "English says 'single attack or effect'"),
    (r"Gana durante el turno de tu oponente\.", "Se ganó durante el turno de tu oponente.", "verb tense like the neighbouring lines"),
    (r"Gana un duelo usando los Efectos de", "Se ganó un duelo usando los efectos de", "verb tense like the neighbouring lines"),
    (r"^botón ×: siguiente$", "Botón ×: siguiente", "capital letter like the next line"),
    # --- duelist cards ---
    (r"en el atolladero en que se encuentre", "en qué atolladero se encuentre", "grammar"),
    (r"fusión de cartas de Héroe Elemental", "Fusión de cartas de Héroe Elemental", "capital letter of the game term"),
    (r"gente fuerte, de confiar,", "gente fuerte, de confianza,", "typo"),
    (r"lo hacia desde", "lo hacía desde", "accent"),
    (r"suave de los que su nombre", "suave de lo que su nombre", "grammar"),
    (r"explicar porqué le retuvieron", "explicar por qué le retuvieron", "por qué"),
    (r"porqué le retuvieron", "por qué le retuvieron", "por qué"),
    (r"la cual\.\.\.hace tiempo", "la cual... hace tiempo", "space"),
    (r"atractivas monstruos femeninas", "atractivos monstruos femeninos", "agreement"),
    (r'llamado a "Chica Cibernética"', 'llamado "Chica Cibernética"', "extra preposition"),
    (r"como ser humano Y gracias", "como ser humano. Y gracias", "punctuation"),
    (r"en lo  primero que tenga a mano", "en lo primero que tenga a mano", "space"),
    (r"Clama tener seis Decks", "Afirma tener seis Decks", "'clamar' is not 'afirmar'"),
    (r"nadie que no se Vellian ha usado alguna vez una", "nadie que no sea Vellian ha usado jamás una", "typo"),
    (r'carta principal es Golem de Mecanismo Antiguo",', 'carta principal es "Golem de Mecanismo Antiguo",', "missing quotation marks"),
    (r"Nadie sabe que tipo de Deck", "Nadie sabe qué tipo de Deck", "accent"),
    (r"saber que le pasará al hombre", "saber qué le pasará al hombre", "accent"),
    (r"actividades en el campus Pero", "actividades en el campus. Pero", "punctuation"),
    (r"en el campus Pero Alexis", "en el campus. Pero Alexis", "punctuation"),
    (r"para poder matricular y verle", "para poder matricularse y verle", "grammar"),
    (r"también pudiera tener este poder de efecto especial como un espíritu$", "También pudiera tener este poder de efecto especial como un espíritu.", "final full stop"),
    (r"signo del destino\.\.\n", "signo del destino...\n", "ellipsis dots"),
    (r"señal del destino\.\.\n", "señal del destino...\n", "ellipsis dots"),
    (r"sella dentro de una carta el alma de perdedor", "sella dentro de una carta el alma del perdedor", "article"),
    (r'tiene como a "Dragón de Oscuridad de Ojos Rojos" como carta principal', 'tiene a "Dragón de Oscuridad de Ojos Rojos" como carta principal', "grammar"),
    (r"^Perfil de Sheppard del Principio$", "Perfil del Rector Sheppard", "'Principal' translated as 'Principio'; Rector as in the dialogues"),
    (r"Asaltante Veladora de Tumbas", "Asaltante del Cuidador de Tumba", "card name"),
    # --- deck editor and tutorial ---
    (r"^Sin límite\.$", "Sin límite", "extra final full stop"),
    (r"mostrarán todas las cartas ¿Aceptas\?", "mostrarán todas las cartas. ¿Aceptas?", "punctuation"),
    (r"es una Carta Limitada, sólo 2 pueden", "es una Carta Semi-Limitada, sólo 2 pueden", "English says Semi-Limited"),
    (r"está in correcta", "es incorrecta", "typo"),
    (r"^Acerca del Menú Editar Deck\.$", "Acerca del Menú Editar Deck", "extra final full stop"),
    (r"Acerca de las carta$", "Acerca de las cartas", "plural"),
    (r'^Cosas que puedes hacer en "Draw Phase"\.$', 'Cosas que puedes hacer en "Draw Phase"', "extra final full stop"),
    (r"(Día 3: Invocación de Tributo y Fundamentos de Magias y Trampas)\.$", r"\1", "extra final full stop"),
    (r"Invocación de Tributo", "Invocación por Sacrificio", "official Spanish term (Invocada por Sacrificio), as in the cards"),
    (r"Invocaciones de Tributo", "Invocaciones por Sacrificio", "official Spanish term, as in the cards"),
    (r"¿Qué es una Deck Receta\?", "¿Qué es una Receta de Deck?", "word order"),
    (r"^Trampa Normales$", "Trampas Normales", "plural"),
    (r"^Trampa Continuas$", "Trampas Continuas", "plural"),
    (r"●Contador Mágico", "●Contadores Mágicos", "plural"),
    (r"Los Contador Mágico", "Los Contadores Mágicos", "plural"),
    (r"●Mira bocarriba carta", "●Mirar boca arriba una carta", "translation of 'Pick up card'"),
    (r"Poner bocarriba carta significa", "Mirar boca arriba una carta significa", "translation of 'Pick up card'"),
    (r"Zone del Deck de Fusión", "Zona del Deck de Fusión", "typo"),
    (r"Flujo el Turno", "Flujo del Turno", "typo"),
    (r"^colocar \(Invocación Normal\)$", "Colocar (Invocación Normal)", "capital letter"),
    (r"●Colocar de Cartas Mágicas y de Cartas de Trampa", "●Colocar Cartas Mágicas y Cartas de Trampa", "grammar"),
    (r"\(Fase de Final\)", "(Fase Final)", "as the others"),
    (r"Fase  de Batalla", "Fase de Batalla", "space"),
    (r"Deck- tienen que ser 3", "Deck: tienen que ser 3", "punctuation"),
    (r"Colocando Etiquetas a tus cartas favoritas o importantes hará", "Colocar Etiquetas en tus cartas favoritas o importantes hará", "grammar"),
    (r"Devuelve una carta que acaba de moverse de otra vez a su posición original\.", "Devuelve a su posición original una carta que acaba de moverse.", "broken sentence"),
    (r"requerimientos\n(Esto es similar a la función)", r"requerimientos.\n\1", "missing full stop"),
    (r"etc\.,en un Deck", "etc., en un Deck", "space"),
    (r"de cual Deck se basa en tipo de concepto", "de cuál Deck se basa en qué tipo de concepto", "accents"),
    (r"botón ×    Mover carta seleccionada Las cartas por lo general", "botón ×\n   Mover carta seleccionada\n   Las cartas por lo general", "missing line breaks (as in English)"),
    (r"Cartas de Monstruos de Fusión”", 'Cartas de Monstruo de Fusión"', "agreement"),
    (r"Cartas de Monstruos de Fusión\"", 'Cartas de Monstruo de Fusión"', "agreement"),
    (r"Carta de Magica llamada", "Carta Mágica llamada", "grammar"),
    (r"Carta de Magia llamada", "Carta Mágica llamada", "grammar"),
    (r"Polimerizacion", "Polimerización", "accent"),
    (r"hacer Invocación de Fusión a este tipo especial de monstruo", "hacer una Invocación de Fusión de este tipo especial de monstruo", "grammar"),
    (r"Mientras carta esté boca arriba", "Mientras esta carta esté boca arriba", "missing article"),
    (r"(?m)^os efectos generalmente", "Los efectos generalmente", "missing initial letter"),
    (r"La misma se usa el mismo orden", "Se usa en el mismo orden", "grammar"),
    (r"as Cartas de Trampa tienen diversos", "las Cartas de Trampa tienen diversos", "typo"),
    (r"una Trampa de Carta", "una Carta de Trampa", "word order"),
    (r"efecto de l Carta de Trampa", "efecto de la Carta de Trampa", "typo"),
    (r"incluso durante el turno de tu oponente\.\nAdemás", "incluso durante tu propio turno.\nAdemás", "English says 'your own turn'"),
    (r'"Siete Herramientas del Bandido"\'', '"Siete Herramientas del Bandido"', "extra apostrophe"),
    (r'efecto de negación de la Carta de Trampa "Disruptor Mágico"', 'efecto de negación de Cartas Mágicas de "Disruptor Mágico"', "English says Spell Card-negating"),
    (r"Spell Speed 2 Cadenas encadenarse", "Spell Speed 2 pueden encadenarse", "'pueden' wrongly replaced by 'Cadenas'"),
    (r"no Cadenas encadenarse a cartas", "no pueden encadenarse a cartas", "'pueden' wrongly replaced by 'Cadenas'"),
    (r"solamente Cadenas encadenarse cartas", "solamente pueden encadenarse cartas", "'pueden' wrongly replaced by 'Cadenas'"),
    (r"no Cadenas haber encadenamiento", "no puede haber encadenamiento", "'puede' wrongly replaced by 'Cadenas'"),
    (r"ninguna ora activación", "ninguna otra activación", "typo"),
    (r"Monstruos de Efectos\n", "Monstruos de Efecto\n", "agreement"),
    (r"Mágicas de Juego Rápido / Mágicas Normales\nMonstruos de Efecto", "Mágicas de Juego Rápido / Trampas Normales\nMonstruos de Efecto", "English says Normal Traps"),
    (r"Cartas Prohibidas, Limitadas y Semilimitadas", "Cartas Prohibidas, Limitadas y Semi-Limitadas", "as in the rest"),
    (r"cuando t dicen que robes", "cuando te dicen que robes", "typo"),
    (r"Los efectos no tienen como blanco a carta\(s\) específica\(s\)", "Los efectos que no tienen como blanco a carta(s) específica(s)", "grammar"),
    (r"o efecto que tienen como blanco", "o efectos que tienen como blanco", "agreement"),
    # tutorial
    (r"decidir hacia donde moverla", "decidir hacia dónde moverla", "accent"),
    (r"otra vez e botón", "otra vez el botón", "typo"),
    (r"estas cartas  particular han", "estas cartas en particular han", "missing word"),
    (r"Botón × : confirma", "Botón ×: confirma", "space"),
    (r'en una "Matchs"', 'en una "Match"', "wrong plural"),
    (r"preguntándote que tipo", "preguntándote qué tipo", "accent"),
    (r"de acuerdo al DEF de cada monstruo", "de acuerdo a la DEF de cada monstruo", "gender of DEF as on the cards"),
    (r"botón △para", "botón △ para", "space"),
    (r"el Deck editando en esos momentos\.", "el Deck que estás editando en este momento.", "grammar"),
    (r'Seleccionando "Búsqueda" después de teclear', 'Seleccionando "Ejecutar" después de teclear', "the button is called Ejecutar (English: Run)"),
    (r"o el botó R\.", "o el botón R.", "typo"),
    (r"Descripciónes", "Descripciones", "typo"),
    (r"Parece que has adquirido práctica con unas cuantas cartas\.", "Parece que has conseguido unas cuantas cartas.", "badly translated ('gotten your hands on')"),
    # --- duel ---
    (r"^Rindes$", "Rendirse", "button label"),
    (r"eliminadas", "retiradas", "'retirar' as in the rest of the game"),
    (r"Los Puntos Vida de", "Los Puntos de Vida de", "missing preposition"),
    (r"Tus Puntos Vida han", "Tus Puntos de Vida han", "missing preposition"),
    (r"Te rendiste rendido debido", "Te rendiste debido", "repetition"),
    (r"se reducen 0\.", "se reducen a 0.", "missing preposition"),
    (r'un "Match" está compuesta', 'un "Match" está compuesto', "agreement"),
    (r"de toda el Match", "de todo el Match", "agreement"),
    (r"Roba cartas desde aquí y para añadirlas a tu mano\.", "Roba cartas desde aquí y añádelas a tu mano.", "grammar"),
    (r"Esta carta esta excluida", "Esta carta está excluida", "accent"),
    (r"El efecto de esta Magica se aplica", "El efecto de esta Carta Mágica se aplica", "grammar"),
    (r"mediante Piedra Papel Tijeras", "mediante Piedra, Papel o Tijeras", "punctuation"),
    (r"continúas al duelo siguiente", "continúas con el duelo siguiente", "preposition"),
    (r"\(Si no en este momento no quedan", "(Si en este momento no quedan", "typo"),
    (r" - colocar de una Carta de Trampa o de una Carta Mágica", " - Colocar una Carta de Trampa o una Carta Mágica", "grammar"),
    (r"Invocar a in monstruo", "Invocar a un monstruo", "typo"),
    (r'a la colocar de una Carta de Monstruo en el campo en Posición de Defensa boca abajo se la llama una "colocar"\.',
     'a colocar una Carta de Monstruo en el campo en Posición de Defensa boca abajo se le llama "Colocar".', "broken sentence"),
    (r"boca arriba esto se le llama una", "boca arriba, a esto se le llama una", "grammar"),
    (r"La colocar de Cartas Mágicas y de Trampa se diferencia de la colocar de Cartas de Monstruo", "Colocar Cartas Mágicas y de Trampa se diferencia de Colocar Cartas de Monstruo", "broken sentence"),
    (r"de la carta siendo usada,\n", "de la carta siendo usada.\n", "punctuation"),
    (r"Casa Paso de la Battle Phase", "Cada Paso de la Battle Phase", "typo"),
    (r"regresarás a la Battle Step", "regresarás al Battle Step", "gender"),
    (r"Posición de Batalla de monstruo que es el blanco", "Posición de Batalla del monstruo que es el blanco", "article"),
    (r"tiene un DEF más bajo", "tiene una DEF más baja", "gender of DEF as on the cards"),
    (r"tiene un DEF más alto", "tiene una DEF más alta", "gender of DEF as on the cards"),
    # final paragraph of the Tag Duel help
    (r"\n\nif Player C of Team 2 has attacked during his/her Battle Phase.*?in response to the attack\.\n", "", "leftover English: the paragraph is already translated right after"),
    (r"que tubo su turno justo antes de eso", "que tuvo su turno justo antes de eso", "typo"),
    (r"sera capaz de elegir", "será capaz de elegir", "accent"),
    (r"Asumiendo que el duelo se juega de acuerdo al siguiente,\n(Equipo 1: Jugador A\nEquipo 2: Jugador C\nEquipo 1: Jugador B\nEquipo 2: Jugador D\n)(\n)",
     r"Asumiendo que el duelo se juega de acuerdo con el siguiente orden,\n\n\1\2", "incomplete sentence"),
    (r"Asumiendo que el duelo se juega de acuerdo al siguiente,\n(Equipo 1: Jugador A\nEquipo 2: Jugador C\nEquipo 1: Jugador B\nEquipo 2: Jugador D)\n?$",
     "Asumiendo que el duelo se juega de acuerdo con el siguiente orden,\n\n\\1\n\n"
     "si el Jugador C del Equipo 2 ha atacado durante su Battle Phase, el jugador que tuvo su turno justo antes de eso, que es el Jugador A del Equipo 1, "
     "podrá elegir si quiere o no activar una Carta Mágica de Juego Rápido o una Trampa como respuesta al ataque.",
     "truncated text: the final paragraph was missing (translated from English)"),
    # --- field, items, maps, laboratory, shop ---
    (r"^¡No hay a quién dárselo\.!$", "¡No hay a quién dárselo!", "punctuation"),
    (r"^Trar$", "Comer", "English says Eat"),
    (r"^¿Tirar bocadillo\?$", "¿Comer bocadillo?", "English says 'Eat a sandwich?'"),
    (r"\$C0 ！", "$C0!", "full-width exclamation mark and space"),
    (r"^MIE$", "MIÉ", "accent"),
    (r"^SAB$", "SÁB", "accent"),
    (r"^¡ %s adquirido!$", "¡%s adquirido!", "space"),
    (r"etc\.que no hayan", "etc., que no hayan", "punctuation"),
    (r"La belleza esta en su sabor", "La belleza está en su sabor", "accent"),
    (r"una maestro pastelero", "un maestro pastelero", "agreement"),
    (r"Es divertido mascarlo\.", "Es divertido masticarlo.", "typo"),
    (r"artesanalmente\.\. Sabe", "artesanalmente. Sabe", "punctuation"),
    (r"los cual explica porqué siempre se venden todos", "lo cual explica por qué siempre se agotan", "typo"),
    (r"una hígado de ganso", "un hígado de ganso", "agreement"),
    (r"^Alójese (\d+)$", r"Habitación \1", "the English name is Room"),
    (r"^Academia del duelo$", "Academia de Duelos", "as in the rest of the game"),
    (r"^Una tienda$", "Tienda", "extra article"),
    (r"^La Oficina de canciller$", "Oficina del Rector", "'Rector' as in the dialogues"),
    (r"^Cliff$", "Acantilado", "leftover English"),
    (r"^Dorm abandonado$", "Dormitorio abandonado", "English abbreviation"),
    (r"^Último Arena$", "Última Arena", "gender"),
    (r"No hay cartaseleccionadas", "No hay cartas seleccionadas", "missing space"),
    (r"La contraseña introducida está incorrecta", "La contraseña introducida es incorrecta", "ser/estar"),
    (r"esta carya", "esta carta", "typo"),
    (r"^Esperando por oponente\.\.\.$", "Esperando al oponente...", "grammar"),
    # --- title messages, options, network, packs, events ---
    (r"Yu-Gi- Oh!", "Yu-Gi-Oh!", "space"),
    (r"^Derotar Crowler$", "Derrotar a Crowler", "typo"),
    (r"^Para princiiantes$", "Para principiantes", "typo"),
    (r"nuevos dato de juego", "nuevos datos de juego", "agreement"),
    (r"botón □ : Selección", "botón □: Selección", "space"),
    (r"Austes del sonido", "Ajustes del sonido", "typo"),
    (r"Austa el volumen", "Ajusta el volumen", "typo"),
    (r"^EN$", "ON", "'EN' is not ON (English says ON)"),
    (r"^FUERADE$", "OFF", "'FUERADE' is a typo for OFF"),
    (r"^SIN LIMITE DE TIEMPO$", "SIN LÍMITE DE TIEMPO", "accent"),
    (r"^NO LIMITE$", "SIN LÍMITE", "correct Spanish"),
    (r"Mientras en el modo ad hoc, sostenga el botón SELECT", "Mientras estés en modo ad hoc, mantén presionado el botón SELECT", "register: the whole game uses the informal tú"),
    (r"para desconectar y devolver al menú principal", "para desconectar y volver al menú principal", "grammar"),
    (r"presiona el botón ×\$C0, y confirmar\.", "presiona el botón ×$C0, y confirma.", "imperative"),
    (r"COLECCCIONABLES", "COLECCIONABLES", "typo"),
    (r"^Escogido entre representante\.$", "Elegido entre los representantes.", "grammar"),
    (r"^Interscholastic se baten en duelo\.$", "Duelo interescolar.", "leftover English"),
    (r"^Antes de una reunión\.$", "El día antes del torneo Tag Force.", "English: the day before the Tag Force meet"),
    # --- tutorial lessons ---
    (r"Ahora le turno a ", "Ahora es el turno de ", "typo: 'le turno'"),
    (r"Ahora le turno\na ", "Ahora es el turno\nde ", "typo: 'le turno'"),
    (r"¡Le turno a\n", "¡Es el turno de\n", "typo: 'le turno'"),
    (r"Le turno a ", "Es el turno de ", "typo: 'le turno'"),
    (r"Como te turno\na ti primero, \$0,", "Como el primer turno es\ntuyo, $0,", "typo: 'te turno'"),
    (r"\$C5Sryus", "$C5Syrus", "typo"),
    (r"\$CALP\$ de su rival", "$CALP$C0 de su rival", "unclosed color code"),
    (r"Zona de Cartas de Monstruos Después, pulsa", "Zona de Cartas de Monstruos. Después, pulsa", "punctuation"),
    (r"tiene una en\nPosición de Ataque", "tiene uno en\nPosición de Ataque", "agreement (monstruo)"),
    (r"Pero si invocación a un\nmonstruo en vez de\nColocar,", "Pero si invocas a un\nmonstruo en vez de\ncolocarlo,", "typo: 'invocación' for 'invocas'"),
    (r"e invocación a uno\ncon un ATK menor", "e invocas a uno\ncon un ATK menor", "typo: 'invocación' for 'invocas'"),
    (r"\$Cpad analógico\$C0", "$C8pad analógico$C0", "incomplete color code"),
    (r"debes realizar una Invocación de u ofrecer uno o más monstruos como Tribute\.", "debes realizar una Invocación y ofrecer uno o más monstruos como Sacrificio.", "truncated sentence and leftover English"),
    (r"^invocación a 1 monstruo\.$", "Invoca a 1 monstruo.", "typo: 'invocación' for 'invoca'"),
    (r"¡\$0!\ninvocación a un monstruo!", "¡$0!\n¡Invoca a un monstruo!", "typo: 'invocación' for 'invoca'"),
    (r'Pulsa el botón × para\nabrir el menú de Phase\.\nSelecciona "End Phase" y\nluego pulsa el botón ○\.',
     'Pulsa el botón ○ para\nabrir el menú de Phase.\nSelecciona "End Phase" y\nluego pulsa el botón ×.', "swapped buttons (English: ○ opens the menu, × confirms)"),
    (r"que Colocar boca abajo, se pondrán", "que se coloquen boca abajo se pondrán", "grammar"),
    (r"Primero hay que Colocar\nboca abajo", "Primero hay que colocarlas\nboca abajo", "grammar"),
    (r"Colocar tu Carta de Trampa\.", "¡Coloca tu Carta de Trampa!", "imperative"),
    (r"Antes, \$C5Bastion\$C0 ha preguntado", "Antes, $C5Syrus$C0 ha preguntado", "English says Syrus"),
    (r"%C5Alexis", "$C5Alexis", "color code"),
    (r"aumentan en \$CA200\$\.\.\.", "aumentan en $CA200$C0...", "unclosed color code"),
    (r"disminuyen en \$CA200\$!", "disminuyen en $CA200$C0!", "unclosed color code"),
    (r"¡Ahora me turno!", "¡Ahora es mi turno!", "typo"),
    (r"\$C5Alexis'\$C0", "$C5Alexis$C0", "extra apostrophe"),
    (r"Cartas de Trampas Normales", "Cartas de Trampa Normales", "Trampa is invariable"),
    (r"#CACarta", "$CACarta", "color code"),
    (r"Zona de de ", "Zona de ", "doubled word"),
    (r"¡Los monstruo de ", "¡Los monstruos de ", "plural"),
    (r'"\$C6Umi\$C0" sigue activo,', '"$C6Umi$C0" sigue activa,', "agreement with Carta Mágica"),
    (r"\bel Hechizo(\s)de(\s)(Campo|Equipo)", r"la Carta Mágica\1de\2\3", "term as on the cards (and gender)"),
    (r"\bEl Hechizo(\s)de(\s)(Campo|Equipo)", r"La Carta Mágica\1de\2\3", "term as on the cards (and gender)"),
    (r"\bHechizo(\s)de(\s)(Campo|Equipo)", r"Carta Mágica\1de\2\3", "term as on the cards"),
    # --- last: double spaces between words (the 'x: Sí  ○: No' lines and the indents after a line break stay) ---
    (r"(?<=[^\s])(?<!Sí)(?<!No)  +(?=[^\s])", " ", "double space"),
    (r"\bun refinar búsqueda\b", "un filtrado", "terminology as in the 'Filtrar' menu"),
    (r"Refinar Búsqueda", "Filtrar", "terminology as in the 'Filtrar' menu"),
]

# --- official card names (tools/data/official_names_es.json, see rules_es.py): the names quoted in quotation marks follow the change ---
import json as _json, os as _os, re as _re
_p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'data', 'official_names_es.json')
for _v in _json.load(open(_p, encoding='utf-8')).values():
    for _old in {_v['old'], _v['old_raw']}:
        GLOBALS.append(('"' + _re.escape(_old) + '"', '"' + _v['new'] + '"', "quoted card name: official name"))

# --- 'blanco' -> 'objetivo': the official Spanish card texts say "selecciona 1 monstruo ... ese objetivo" (target) ---
GLOBALS += [
    (r"\bEfectos de Blanco\b", "Efectos con Objetivo", "official terminology: objetivo (target)"),
    (r"\bblanco\b", "objetivo", "official terminology: objetivo (target)"),
    (r"\bblancos\b", "objetivos", "official terminology: objetivo (target)"),
]

