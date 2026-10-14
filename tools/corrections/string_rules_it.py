"""Corrections to the Italian interface strings (strTbl*, help_strtbl_*, ddstrtbl, field_strtbl* tables in the ISO's .ehp files): duelist
cards, duel records, help and tutorial of the deck editor and of the duel, items, maps and menus, laboratory, shop, title and options.
Applied by ui_strings.py (also with text longer than the original).
STRINGS: (archive under /PSP_GAME/USRDIR, member, index, [(old, new), ...], reason): every 'old' must appear in the string.
GLOBALS: (regex, replacement or function, reason) applied to all the strings of the TABLES (first the STRINGS, then the GLOBALS, in the order written).
The indexes are those of the table (0-based). The same tables exist identically in the archives of all the regions (always_*_ita, basic_*i).
Hand reading: comparisons/audit_it/ui_strings_it.tsv. Newlines in the strings are '\n'."""

CH = ('database/charalist.ehp', 'strTbl_i.bin')
DR = ('database/duelrecord.ehp', 'strTbl_i.bin')
RE = ('duel/result/result_i.ehp', 'strTbl.bin')
DK = ('deck/all_i.ehp', 'strTbl.bin')
HC = ('deck/all_i.ehp', 'help_strtbl_contents.bin')
HL = ('deck/all_i.ehp', 'help_strtbl_label.bin')
TU = ('deck/tutorial.ehp', 'strTbl_i.bin')
DD = ('duel/basic_bi.ehp', 'ddstrtbl_i.bin')
HD = ('duel/basic_bi.ehp', 'help_strtbl_contents_duel_i.bin')
ST = ('duel/start/start_i.ehp', 'strTbl_i.bin')
FS = ('field/always_*_ita.ehp', 'field_strtbl.bin')
FI = ('field/always_*_ita.ehp', 'field_strtbl_item.bin')
CV = ('labo/conv_machine.ehp', 'strTbl_i.bin')
PW = ('labo/password.ehp', 'strTbl_i.bin')
SH = ('shop/all_i.ehp', 'strTbl_i.bin')

TABLES = [CH, DR, RE, DK, HC, HL, TU, DD, HD, ST, FS, FI, CV, PW, SH]


def _prep(forms, name):
    """di/a/da/in + dormitory name -> articulated preposition (keeps the initial capital)"""
    def f(m):
        p = m.group(1)
        new = forms[p.lower()] + name
        return new[0].upper() + new[1:] if p[0].isupper() else new
    return f


_SL = {'di': 'dello ', 'a': 'allo ', 'da': 'dallo ', 'in': 'nello '}
_OB = {'di': "dell'", 'a': "all'", 'da': "dall'", 'in': "nell'"}


def _spell(m):
    x = {'Normali': 'Normali', 'Continuate': 'Continue', 'Equipaggiamento': 'Equipaggiamento', 'Rituale': 'Rituali', 'Rituali': 'Rituali',
         'Terreno': 'da Terreno', 'da Terreno': 'da Terreno', 'Rapida': 'Rapide', 'Rapide': 'Rapide'}[m.group(1)]
    return 'Magie ' + x


GLOBALS = [
    (r"(?<=[A-Za-zà-ù.,;!?])  +(?=[A-Za-zÀ-ù])", " ", "spazi doppi"),
    (r"’", "'", "apostrofo tipografico -> semplice"),
    (r"\bE'(?=[A-Za-zà-ù])", "È ", "E' al posto di È"),
    (r"\bE' ", "È ", "E' al posto di È"),
    (r"(?m)(?:^|(?<=[.!?] ))E (?=(?:riuscita|stato|sempre|molto)\b)", "È ", "E senza accento"),
    (r"chè\b", "ché", "perché, finché, nonché..."),
    (r"\bpò\b", "po'", "un po'"),
    (r"\bfà\b", "fa", "accento"), (r"\bsà\b", "sa", "accento"), (r"\bstà\b", "sta", "accento"), (r"\bnè\b", "né", "accento"), (r"\bsè\b", "sé", "accento"),
    (r"\bcosi\b", "così", "accento"), (r"\bpiu\b", "più", "accento"),
    (r"\bverrano\b", "verranno", "refuso"), (r"\bdallla\b", "dalla", "refuso"), (r"\bpiù più\b", "più", "ripetizione"),
    (r"\bsanwich\b", "sandwich", "refuso"), (r"\bSndwich\b", "Sandwich", "refuso"), (r"\bsoya\b", "soia", "refuso"), (r"sudentesca", "studentesca", "refuso"),
    (r"choccolato", "cioccolato", "refuso"), (r"scimpanzè", "scimpanzé", "accento"),
    (r"\b(?!(?:po|va|sta|fa|di|da|stai|dai)\b)([A-Za-zÀ-ÿ]+)' (?=[A-Za-zÀ-ÿ])", r"\1'", "spazio dopo l'apostrofo"),
    (r"(?<=[A-Za-zà-ù]) '(?=[A-Za-z])", "'", "spazio prima dell'apostrofo"),
    (r"(?<=[a-zà-ù,;] )I (?=[a-zà-ù])", "i ", "articolo con la I maiuscola"),
    (r"\b([Ii]|[Dd]ei|[Nn]ei|[Aa]i|[Ss]ui|[Dd]ai|[Pp]er i|[Tt]ra i) Duello\b", r"\1 Duelli", "plurale"),
    (r"\bDuello Singoli\b", "Duelli Singoli", "plurale"), (r"\b(\d) Duello\b", r"\1 Duelli", "plurale"),
    (r"affrontare Duello in cui", "affrontare Duelli in cui", "plurale"),
    (r"\bMostri Fusione\b", "Mostri da Fusione", "nome del tipo"), (r"\bMostri Rituale\b", "Mostri Rituali", "plurale"),
    (r"\bGli Mostri\b", "I Mostri", "articolo"),
    (r"(?m)^Magia (Normali|Continuate|Equipaggiamento|Rituale|Rituali|Terreno|da Terreno|Rapida|Rapide)(?=\r?$)", _spell, "elenco dei tipi di Magia"),
    (r"(?m)^Trappola (Normali|Continue)(?=\r?$)", r"Trappole \1", "elenco dei tipi di Trappola"),
    (r"\bsulle carta\b", "sulle carte", "plurale"),
    (r"●Segna-Monstro", "●Segna-Mostro", "nome"), (r"I Segna dei Mostri", "I Segna-Mostro", "nome"), (r"i Segna non", "i Segna-Mostro non", "nome"),
    (r"Un Gettone equivale", "Un Segna-Mostro equivale", "nome"), (r"Gettoni Evocati", "Segna-Mostro Evocati", "nome"),
    (r"●Guarda delle Carte", "●Guardare le Carte", "titolo"),
    (r"●Activar", "●Attivazione", "refuso"),
    (r"\bin terreno\b", "in Terreno", "maiuscola"), (r"\bterreno di Duello\b", "Terreno di Duello", "maiuscola"), (r"Carta da terreno", "Carta da Terreno", "maiuscola"),
    (r"\bsuo Effetti Scoperta\b", "suo Effetto Scoperta", "singolare"), (r"\bl'Effetti Scoperta\b", "l'Effetto Scoperta", "singolare"),
    (r"\bQuesta opzione di permette\b", "Questa opzione ti permette", "refuso"),
    (r"\bcon ad un\b", "con un", "refuso"),
    (r"\b(di|a|da|in) Slifer Red\b", _prep(_SL, 'Slifer Rosso'), "dormitorio"), (r"\bSlifer Red\b", "Slifer Rosso", "nome del dormitorio"),
    (r"\b(di|a|da|in) Obelisk Blue\b", _prep(_OB, 'Obelisk Blu'), "dormitorio"), (r"\bObelisk Blue\b", "Obelisk Blu", "nome del dormitorio"),
    (r"\bRa Yellow\b", "Ra Giallo", "nome del dormitorio"),
]

STRINGS = [
    # --- database/charalist: duelist cards
    (*CH, 12, [("Che cosa pensi delle ragazze rimene un mistero", "Che cosa pensa delle ragazze rimane un mistero")], "terza persona"),
    (*CH, 13, [("infatuatuato", "infatuato"), ("in realta è", "in realtà è"), ("vincere .Ma", "vincere. Ma"), ("un' atteggiamento", "un atteggiamento")], "refusi"),
    (*CH, 14, [("dolce ti quanto", "dolce di quanto"), ("convizione", "convinzione"), ("essere essere", "essere")], "refusi"),
    (*CH, 15, [("interesata", "interessata")], "refuso"),
    (*CH, 17, [("nei sui confronti", "nei suoi confronti"), ("atteggiameneto", "atteggiamento"), ("camerata di Obelisk Blue", "camerata dell'Obelisk Blu")], "refusi"),
    (*CH, 18, [("tapezzate", "tappezzate"), ("Daltra parte", "D'altra parte"), ("mancanza di presenze", "mancanza di presenza")], "refusi"),
    (*CH, 20, [("eleborato", "elaborato"), ("le hai mai indossate", "le ha mai indossate"), ("Velliar", "Vellian"), ("Velian", "Vellian"),
               ("è il Golem-Ingranaggio", "è il \"Golem-Ingranaggio"), ("che predilige..", "che predilige.")], "refusi e virgolette"),
    (*CH, 21, [("nonchè presidente di Slifer Red", "nonché direttore dello Slifer Rosso")], "come nei dialoghi: direttore del dormitorio"),
    (*CH, 22, [("troppo.Tutte", "troppo. Tutte"), ("addiririttura", "addirittura")], "refusi"),
    (*CH, 23, [("si vergona", "si vergogna"), ("simpattica", "simpatica"), ("nenche", "nemmeno")], "refusi"),
    (*CH, 24, [("membro deli Cavalieri", "membro dei Cavalieri"), ("anche un Amazzone", "anche un'Amazzone")], "refusi"),
    (*CH, 28, [("avversaro", "avversario"), ("lo contratta", "lo ingaggia")], "refusi"),
    (*CH, 29, [("problemaè legata", "problema è legata")], "spazio"),
    (*CH, 31, [("lo indusse  e a vivere una vita da recluso a ritirarsi sulle montagne dove si addestrò  rigorosamente",
                "lo indusse a vivere da recluso, ritirandosi sulle montagne dove si addestrò rigorosamente")], "frase confusa"),
    (*CH, 34, [("Ha un gran interesse nel stilare", "Ha un grande interesse nello stilare")], "grammatica"),
    (*CH, 37, [("stato danimo", "stato d'animo"), ("imnnamorata", "innamorata"), ("tutti giorni", "tutti i giorni")], "refusi"),
    (*CH, 43, [("con' un occhiata", "con un'occhiata"), ("lli fulmina", "li fulmina")], "refusi"),
    (*CH, 48, [("E'innamorato di tutto", "È innamorata di tutto")], "accordo"),
    (*CH, 49, [("finche non vince", "finché non vince")], "accento"),
    (*CH, 52, [("Profilo del preside Sheppard", "Profilo del Preside Sheppard")], "Preside con la maiuscola"),
    # --- database/duelrecord and duel/result: duel records and goals (the two tables are identical)
    *[(*T, i, p, m) for T in (DR, RE) for i, p, m in [
        (26, [("Evocazioni Fusione", "Evocazioni per Fusione")], "nome"),
        (35, [("assogettati I Mostri", "assoggettati i Mostri")], "refuso"),
        (63, [("Mentenere", "Mantenere")], "refuso"),
        (137, [("tramite Evocazione Speciale dal Cimitero rimuovendo carte dal gioco carte nel corso di un Duello",
                "tramite Evocazione Speciale rimuovendo dal gioco carte presenti nel Cimitero nel corso di un Duello")], "frase confusa"),
        (155, [("terminare Carte e Duello vinto", "terminare le Carte, e Duello vinto")], "articolo"),
        (159, [("Vinci durante il turno del tuo avversario.", "Hai vinto durante il turno del tuo avversario.")], "stile come le altre voci"),
        (160, [("Vinci un Duello usando Effetti di", "Hai vinto un Duello usando gli effetti di")], "stile"),
        (161, [("Vinci un Duello usando Effetti di", "Hai vinto un Duello usando gli effetti di")], "stile"),
        (162, [("Vinci un Duello usando Effetti di", "Hai vinto un Duello usando gli effetti di")], "stile"),
        (163, [("Hai vinto con una Carta con effetto che ha permesso di vincere il match.", "Hai vinto con una Carta il cui effetto assegna la vittoria.")], "frase"),
        (164, [("Hai vinto con l'effetto costringente \"Yata-Garasu\".", "Hai vinto con il blocco di \"Yata-Garasu\".")], "frase"),
        (182, [("conteneva Mostro di ogni Livello", "conteneva Mostri di ogni Livello")], "plurale"),
        (184, [("Hai vinto con un Deck che conteneva Mostro di ogni Livello .", "Hai vinto con un Deck che non conteneva nessun Mostro con un ATK pari o superiore a 1500.")],
         "frase sbagliata (copia di 182)"),
        (212, [("ad eccezione quelli", "ad eccezione di quelli")], "refuso"),
        (213, [("diquelli", "di quelli")], "refuso"),
        (248, [(" Bonus Nuovo", "Bonus Nuovo")], "spazio iniziale"),
    ]],
    # --- deck/all_i: deck editor
    (*DK, 51, [("5 -6", "5-6")], "spazio"),
    (*DK, 83, [("Se Cambi questo parametro tutti le condizioni", "Se cambi questo parametro tutte le condizioni")], "refusi"),
    (*DK, 100, [("Aggiungi /rimuovi", "Aggiungi/rimuovi")], "spazio"),
    (*DK, 101, [("Cancella /Abbandona", "Cancella/Abbandona")], "spazio"),
    (*DK, 106, [("On /Off", "On/Off")], "spazio"),
    (*DK, 109, [("Un Deck può solo contenere $CA80$C0 o meno Carte.", "Un Deck può contenere solo $CA80$C0 Carte o meno.")], "frase"),
    (*DK, 110, [("Un Side Deck può solo contere $CA15$C0 Carte o meno.", "Un Side Deck può contenere solo $CA15$C0 Carte o meno.")], "frase"),
    (*DK, 111, [("Un Fusion Deck può solo contere $CA30$C0 Carte o meno.", "Un Fusion Deck può contenere solo $CA30$C0 Carte o meno.")], "frase"),
    (*DK, 116, [("Fai scorrere categoria", "Fai scorrere la categoria")], "articolo"),
    (*DK, 126, [("gioco.$Vuoi", "gioco.\nVuoi")], "'$' al posto dell'a capo"),
    (*DK, 138, [("Vuoi confermare %02d \"$CB%s$C0\" Tutorial alla Modifica del Deck?\n(Lo puoi confermare anche all' interno del database.)",
                 "Vuoi vedere il Tutorial %02d \"$CB%s$C0\" sulla Modifica del Deck?\n(Puoi vederlo anche dal database.)")], "frase"),
    (*DK, 142, [("incorretto", "errato")], "italiano"),
    (*DK, 148, [("Menu Selezione Carta .", "Menu Selezione Carta")], "spazio"),
    (*DK, 152, [("la/e Carta/e che hai selezionato sarà/anno", "La/e Carta/e che hai selezionato sarà/anno")], "maiuscola"),
    (*DK, 154, [("abbandonare selezione Carta?", "abbandonare la selezione delle Carte?")], "articolo"),
    (*DK, 155, [("\n OK?", "\nOK?")], "spazio"),
    (*HL, 1, [("Assistenza", "Aiuto")], "come l'etichetta del pulsante '?'"),
    (*HL, 8, [("Chiudi Assistenza", "Chiudi Aiuto")], "coerenza"),
    # --- deck editor help (deck/all_i, help_strtbl_contents)
    (*HC, 81, [("●Segna-Monstro", "●Segna-Mostro")], "nome"),
    (*HC, 100, [("quando giochi una Match", "quando giochi un Match")], "genere"),
    (*HC, 104, [("Elenco dei fogli", "Elenco delle linguette")], "termine"),
    (*HC, 105, [("Menu Modifica del Deck .", "Menu Modifica del Deck.")], "spazio"),
    (*HC, 106, [("della Carta selezionato", "della Carta selezionata")], "accordo"),
    (*HC, 107, [("un'contrassegno", "un contrassegno")], "refuso"),
    (*HC, 118, [("un'contrassegno", "un contrassegno")], "refuso"),
    (*HC, 129, [("Per evocazione in Terreno una Carta", "Per evocare in Terreno una Carta"), ("il suo Attributi", "il suo Attributo")], "refusi"),
    (*HC, 157, [("(Continuato, a Ignizione, Activar, da Scoperta)", "(Continui, ad Ignizione, Innescati, da Scoperta)"),
                ("all’Activar di un’altra", "all’attivazione di un’altra")], "Activar non e' italiano"),
    (*HC, 164, [("Le Segnalino Magia, sono sistemate sopra le Carte", "I Segnalini Magia vengono sistemati sopra le Carte"),
                ("Le Segnalino Magia sono necessarie", "I Segnalini Magia sono necessari"),
                ("non possono essere piazzate sulle Carte", "non possono essere piazzati sulle Carte")], "plurale e genere"),
    (*HC, 175, [("probabilità di pesca la Carta", "probabilità di pescare la Carta"), ("È importante evocazione il giusto equilibrio", "È importante mantenere il giusto equilibrio")], "refusi"),
    # --- deck editor tutorial
    (*TU, 5, [("In questa schermo puoi", "In questa schermata puoi"), ("chiamata schermo di", "chiamata schermata di")], "genere"),
    (*TU, 25, [("verra'spostata", "verrà spostata")], "refuso"),
    (*TU, 26, [("Usa icomandi", "Usa i comandi")], "refuso"),
    (*TU, 27, [("spostare, verrà", "spostare verrà")], "virgola"),
    (*TU, 29, [("la Carte", "le Carte")], "articolo"),
    (*TU, 30, [("Desk", "Deck")], "refuso"),
    (*TU, 34, [("Un Deck può contenere solo dalle 40 alle 80 Carte massimo.", "Un Deck può contenere da 40 a 80 Carte.")], "frase"),
    (*TU, 36, [("avvertimento,", "avvertimento.")], "punteggiatura"),
    (*TU, 39, [("ricordarti di darci", "ricordati di darci")], "refuso"),
    (*TU, 82, [("ricordarti di darci", "ricordati di darci")], "refuso"),
    (*TU, 46, [("e'uno spaccato", "è uno spaccato")], "refuso"),
    (*TU, 61, [("accquistato", "acquistato")], "refuso"),
    (*TU, 74, [("Assistenza:", "Aiuto:")], "come l'etichetta del pulsante '?'"),
    (*TU, 79, [("Duello. .", "Duello.")], "punteggiatura"),
    (*TU, 86, [("La Partita sono tipi di Duelli particolari.", "La Partita è un tipo particolare di Duello.")], "frase"),
    (*TU, 87, [("Partita\" .", "Partita\".")], "spazio"),
    (*TU, 98, [("in un Partita", "in una Partita")], "genere"),
    (*TU, 104, [(" Per visualizzare", "Per visualizzare")], "spazio"),
    (*TU, 113, [("in base al ATK", "in base all'ATK")], "articolo"),
    (*TU, 118, [("Semi/Limitate", "Semi-Limitate")], "nome"),
    (*TU, 119, [("Livello- dalla", "Livello, dalla")], "punteggiatura"),
    (*TU, 126, [("parlarti della \"Filtra\"", "parlarti di \"Filtra\"")], "articolo"),
    (*TU, 128, [("Quando conduci \"Filtra\"", "Quando usi \"Filtra\"")], "verbo"),
    (*TU, 129, [("esattemente", "esattamente")], "refuso"),
    (*TU, 130, [("differanza", "differenza")], "refuso"),
    (*TU, 133, [("Verranno visualizzati una serie di Attributi", "Verrà visualizzata una serie di Attributi")], "accordo"),
    (*TU, 145, [("esibite", "visualizzate")], "termine"),
    (*TU, 146, [("Come ved, i le uniche", "Come vedi, le uniche")], "refuso"),
    (*TU, 150, [("condizioni della Filtra", "condizioni di \"Filtra\"")], "articolo"),
    (*TU, 153, [("puoi solo usare un Deck alla volta, ma puoi salvarne svariati, questi sono chiamati", "puoi usare un solo Deck alla volta, ma puoi salvarne svariati: questi sono chiamati")], "frase"),
    (*TU, 154, [("quando carichi una ricetta", "quando carichi una Ricetta")], "maiuscola"),
    (*TU, 166, [("ti dovrebbero permettono", "ti dovrebbero permettere")], "refuso"),
    (*TU, 172, [("Quetsa", "Questa")], "refuso"),
    (*TU, 173, [("è stata attaccato", "è stato attaccato")], "accordo"),
    (*TU, 175, [("è stato selezionata", "è stata selezionata")], "accordo"),
    (*TU, 176, [("attaccata un Contrassegno", "attaccato un Contrassegno")], "accordo"),
    (*TU, 177, [("attaccata un Contrassegno", "attaccato un Contrassegno")], "accordo"),
    (*TU, 179, [("per un tempo", "per un po'")], "frase"),
    (*TU, 189, [("durante Modifica del Deck", "durante la Modifica del Deck")], "articolo"),
    (*TU, 201, [("verrà rimossa", "verrà rimosso")], "accordo"),
    (*TU, 203, [("sennza", "senza")], "refuso"),
    (*TU, 205, [("Della Schermata", "della Schermata")], "maiuscola"),
    # --- duel: menus and end-of-duel messages
    (*DD, 70, [("\"Exodia il Proibito\"", "\"Exodia il Proibito\".")], "punto finale"),
    (*DD, 72, [("dell'effetto costringente di", "dell'effetto di blocco di")], "termine"),
    (*DD, 73, [("\"Ultimo Turno\"", "\"Ultimo Turno\".")], "punto finale"),
    (*DD, 75, [("Hai vinto con un effetto che ti ha permesso di vincere il match.", "Hai vinto la Partita grazie a un effetto che assegna la vittoria.")], "frase"),
    (*DD, 81, [(" Hai esaurito", "Hai esaurito")], "spazio"),
    (*DD, 84, [("dell' effetto costringente di", "dell'effetto di blocco di")], "termine"),
    (*DD, 87, [("Hai perso a la paritita a causa di un effetto dirompente.", "Hai perso la Partita a causa di un effetto che assegna la vittoria all'avversario.")], "frase"),
    (*DD, 88, [("Hai perso perchè è   scaduto il tempo massimo.", "Hai perso perché il tempo massimo è scaduto.")], "frase"),
    (*ST, 2, [("Scegli I'ordine", "Scegli l'ordine")], "refuso"),
    # --- duel help (help_strtbl_contents_duel)
    (*HD, 92, [("●Segna-Monstro", "●Segna-Mostro")], "nome"),
    (*HD, 110, [("quando deve pesca una", "quando deve pescarne una")], "refuso"),
    (*HD, 113, [("quando giochi una Match", "quando giochi un Match")], "genere"),
    (*HD, 116, [("estratte dal Deck e pesca alla tua Mano", "estratte dal Deck e finiscono nella tua Mano")], "refuso"),
    (*HD, 123, [("Per evocazione in Terreno una Carta", "Per evocare in Terreno una Carta"), ("il suo Attributi", "il suo Attributo")], "refusi"),
    (*HD, 154, [("deve pesca una Carta", "deve pescare una Carta")], "refuso"),
    (*HD, 177, [("(Continuato, a Ignizione, Activar, da Scoperta)", "(Continui, ad Ignizione, Innescati, da Scoperta)"),
                ("all’Activar di un’altra", "all’attivazione di un’altra")], "Activar non e' italiano"),
    (*HD, 184, [("Le Segnalino Magia, sono sistemate sopra le Carte", "I Segnalini Magia vengono sistemati sopra le Carte"),
                ("Le Segnalino Magia sono necessarie", "I Segnalini Magia sono necessari"),
                ("non possono essere piazzate sulle Carte", "non possono essere piazzati sulle Carte")], "plurale e genere"),
    (*HD, 195, [("probabilità di pesca la Carta", "probabilità di pescare la Carta"), ("È importante evocazione il giusto equilibrio", "È importante mantenere il giusto equilibrio")], "refusi"),
    # --- office menu, items, laboratory
    (*FS, 8, [("Manda Avanti Tempo", "Avanza il Tempo")], "come nei dialoghi"),
    (*FS, 21, [("Dia", "Dai")], "imperativo"),
    (*FS, 22, [("Mangi", "Mangia")], "imperativo"),
    (*FS, 57, [("Esamina attività scolastiche, etc, nell'orario.", "Esamina l'orario delle attività scolastiche, ecc.")], "frase"),
    (*FS, 58, [("Visualizza tuo status attuale.", "Visualizza il tuo status attuale.")], "articolo"),
    (*FS, 59, [("etc.", "ecc.")], "abbreviazione"),
    (*FS, 60, [("Cambia parametri suoneria, Duelli, etc.", "Cambia i parametri audio, dei Duelli, ecc.")], "termine"),
    (*FS, 68, [(" Record Duello", "Record Duello")], "spazio"),
    (*FS, 98, [("tasto ×sul tempo", "tasto × sull'orario")], "refuso"),
    (*FI, 95, [("pate' de Foie Gras", "paté di foie gras")], "refuso"),
    (*FI, 60, [(" Sandwich di bistecca", "Sandwich di bistecca")], "spazio"),
    (*FI, 157, [("ripieno di una svizzera preparata", "ripieno di un hamburger preparato")], "termine"),
    (*FI, 184, [("ripieno scampi fritti", "ripieno di scampi fritti")], "refuso"),
    (*FI, 189, [("Un sandwich di gyoza ripieni", "Un sandwich con gyoza ripieni")], "frase"),
    (*FI, 191, [("cinesi E minestra", "cinesi e minestra")], "refuso"),
    (*FI, 193, [("sandwichcol ripieno", "sandwich col ripieno")], "refuso"),
    (*PW, 4, [("E'stata salvatacome Carta a nolo.", "È stata salvata come Carta a noleggio.")], "refusi"),
    (*PW, 9, [("terminare inserimento", "terminare l'inserimento")], "articolo"),
]
