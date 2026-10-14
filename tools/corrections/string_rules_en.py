"""Corrections to the English interface strings (strTbl*, help_strtbl_*, ddstrtbl, field_strtbl* tables in the ISO's .ehp files): duelist
cards, duel records, help and tutorial of the deck editor and of the duel, items, maps and menus, laboratory, shop, title and options.
Applied by ui_strings.py (also with text longer than the original).
STRINGS: (archive under /PSP_GAME/USRDIR, member, index, [(old, new), ...], reason): every 'old' must appear in the string.
GLOBALS: (regex, replacement or function, reason) applied to all the strings of the TABLES (first the STRINGS, then the GLOBALS, in the order written).
The indexes are those of the table (0-based). The same tables exist identically in the archives of all the regions (always_*_eng, basic_*e).
Hand reading: comparisons/audit_en/ui_strings_en.tsv."""

CH = ('database/charalist.ehp', 'strTbl_e.bin')
DR = ('database/duelrecord.ehp', 'strTbl_e.bin')
LL = ('database/limitlist.ehp', 'strTbl_e.bin')
RE = ('duel/result/result_e.ehp', 'strTbl.bin')
TL = ('database/tutoriallist.ehp', 'strTbl_e.bin')
DK = ('deck/all_e.ehp', 'strTbl.bin')
HC = ('deck/all_e.ehp', 'help_strtbl_contents.bin')
HL = ('deck/all_e.ehp', 'help_strtbl_label.bin')
TU = ('deck/tutorial.ehp', 'strTbl_e.bin')
DD = ('duel/basic_*e.ehp', 'ddstrtbl_e.bin')
HD = ('duel/basic_*e.ehp', 'help_strtbl_contents_duel_e.bin')
HE = ('duel/basic_*e.ehp', 'help_strtbl_label_e.bin')
ST = ('duel/start/start_e.ehp', 'strTbl_e.bin')
FS = ('field/always_*_eng.ehp', 'field_strtbl.bin')
FI = ('field/always_*_eng.ehp', 'field_strtbl_item.bin')
FM = ('field/always_*_eng.ehp', 'field_strtbl_mapname.bin')
CV = ('labo/conv_machine.ehp', 'strTbl_e.bin')
PW = ('labo/password.ehp', 'strTbl_e.bin')
SH = ('shop/all_e.ehp', 'strTbl_e.bin')

TM = ('title_menu/title_menu_?.ehp', 'title_msg_e.bin')
OM = [('duel/basic_*.ehp', 'option_msg_e.bin'), ('field/always_*_eng.ehp', 'option_msg_e.bin'), ('title_menu/title_menu_?.ehp', 'option_msg_e.bin')]
TS = ('title_menu/title_menu_?.ehp', 'tushin_msg_e.bin')
OG = [('database/cardalbum.ehp', 'ocg_packname_e.bin'), ('deck/all_?.ehp', 'ocg_packname_e.bin'), ('duel/basic_[be]?.ehp', 'ocg_packname_e.bin'),
      ('field/always_[bfgis]??_*.ehp', 'ocg_packname_e.bin')]
EV = ('field/always_*_eng.ehp', 'event_name.bin')
LE = [('tutorial/tutorial_e.ehp', f'0{n}_message_res.bin') for n in (1, 2, 3, 4)]

TABLES = [CH, DR, LL, RE, TL, DK, HC, HL, TU, DD, HD, HE, ST, FS, FI, FM, CV, PW, SH, TM, TS, EV] + OM + LE

STRINGS = [
    # --- duelist cards (charalist) ---
    (CH[0], CH[1], 13, [('which seems to be cause of', 'which seems to be the cause of'), ('Although they seem a cute and harmless', 'Although they seem cute and harmless')], 'articolo / "a" di troppo'),
    (CH[0], CH[1], 30, [('energy in which he can use', 'energy which he can use')], 'relativa sbagliata'),
    (CH[0], CH[1], 37, [('to see him everyday.', 'to see him every day.')], 'every day (avverbio)'),
    (CH[0], CH[1], 48, [('in her Deck which it is packed with', 'in her Deck, which is packed with')], 'pronome di troppo'),
    (CH[0], CH[1], 52, [("Principle's Sheppard's Profile", "Chancellor Sheppard's Profile")], 'refuso (Principle\'s) e titolo del personaggio come nei dialoghi (Chancellor)'),
    # --- duel records: duelrecord and result have the same table ---
    (DR[0], DR[1], 42, [('opponents cards', "opponent's cards")], 'apostrofo'),
    (RE[0], RE[1], 42, [('opponents cards', "opponent's cards")], 'apostrofo'),
    (LL[0], LL[1], 6, [('in your deck.', 'in your Deck.')], 'maiuscola: Deck'),
    (LL[0], LL[1], 7, [('in your deck.', 'in your Deck.')], 'maiuscola: Deck'),
    (LL[0], LL[1], 8, [('in your deck.', 'in your Deck.')], 'maiuscola: Deck'),
    # --- deck editor help (help_strtbl_contents) ---
    (HC[0], HC[1], 128, [('by "Summon" it.', 'by "Summoning" it.')], 'forma verbale'),
    (HC[0], HC[1], 140, [('can be also be activated', 'can also be activated')], 'parole invertite'),
    (HC[0], HC[1], 162, [('faced-down', 'face-down')], 'refuso'),
    (HC[0], HC[1], 166, [('and viewing its content', 'and view its content'), ('when Pick up a card', 'when you pick up a card')], 'grammatica'),
    # --- deck editor tutorial ---
    (TU[0], TU[1], 4, [('anyway you like', 'any way you like')], 'any way'),
    (TU[0], TU[1], 81, [('of the same name be in it', 'of the same name can be in it')], 'verbo mancante'),
    (TU[0], TU[1], 147, [('functions allow you', 'functions allows you')], 'concordanza (soggetto: Using ... functions)'),
    (TU[0], TU[1], 203, [('more faster and easier', 'faster and easier')], 'comparativo doppio'),
    # --- duel messages (ddstrtbl) and duel help (help_strtbl_contents_duel) ---
    (DD[0], DD[1], 84, [('Your surrendered due to', 'You surrendered due to')], 'refuso'),
    (HD[0], HD[1], 109, [('"Single" are played', '"Single" Duels are played')], 'sostantivo mancante'),
    (HD[0], HD[1], 122, [('by "Summon" it.', 'by "Summoning" it.')], 'forma verbale'),
    (HD[0], HD[1], 134, [('can be also be activated', 'can also be activated')], 'parole invertite'),
    (HD[0], HD[1], 154, [('at anytime between', 'at any time between')], 'any time'),
    (HD[0], HD[1], 160, [('just as you do when Summon.', 'just as you do when Summoning.')], 'forma verbale'),
    (HD[0], HD[1], 163, [('When successfully "Fusion Summon" a Monster Card', 'When you successfully "Fusion Summon" a Monster Card')], 'soggetto mancante'),
    (HD[0], HD[1], 164, [('When successfully "Ritual Summon" a Monster Card', 'When you successfully "Ritual Summon" a Monster Card')], 'soggetto mancante'),
    (HD[0], HD[1], 182, [('faced-down', 'face-down')], 'refuso'),
    (HD[0], HD[1], 186, [('and viewing its content', 'and view its content'), ('when Pick up a card', 'when you pick up a card')], 'grammatica'),
    # --- field menus and messages ---
    (FS[0], FS[1], 14, [('to request duel against', 'to request a duel against')], 'articolo mancante'),
    (FS[0], FS[1], 27, [('！', '!')], 'punto esclamativo a larghezza piena'),
    (FS[0], FS[1], 28, [('！', '!')], 'punto esclamativo a larghezza piena'),
    (FS[0], FS[1], 99, [('You acquired %s !', 'You acquired %s!')], 'spazio prima del !'),
    (FI[0], FI[1], 4, [('Bandanna', 'Bandana')], 'refuso (nei dialoghi: Bandana)'),
    (FI[0], FI[1], 104, [('orange bandanna', 'orange bandana')], 'refuso'),
    (FI[0], FI[1], 161, [('roasted chestnuts, ', 'roasted chestnuts.')], 'virgola al posto del punto'),
    (FI[0], FI[1], 182, [('filled with  an uniquely-dried fish', 'filled with a uniquely-dried fish')], 'doppio spazio, articolo'),
    (FI[0], FI[1], 185, [('lobster chunks', 'lobster chunks.')], 'punto mancante'),
    (FI[0], FI[1], 198, [('what my be inside', 'what may be inside')], 'refuso'),
    # --- title and communications ---
    (TS[0], TS[1], 36, [('entry...Please', 'entry... Please')], 'spazio mancante'),
    (TS[0], TS[1], 46, [('network duel.Please', 'network duel. Please')], 'spazio mancante'),
    (EV[0], EV[1], 10, [('The day before of', 'The day before the')], 'preposizione di troppo'),
] + [(o[0], o[1], 26, [("confirm it's effects", 'confirm its effects')], "its (possessivo)") for o in OM] + [
    # --- tutorial lessons (Crowler) ---
    (LE[0][0], LE[0][1], 59, [('Sryus', 'Syrus'), ('but now  we', 'but now we')], 'nome scritto male, doppio spazio'),
    (LE[0][0], LE[0][1], 109, [('Get em,', "Get 'em,")], 'apostrofo'),
    (LE[0][0], LE[0][1], 138, [('will be take away', 'will be taken away')], 'participio'),
    (LE[1][0], LE[1][1], 17, [('is called "Set" it!', 'is called "Setting" it!')], 'forma verbale'),
    (LE[1][0], LE[1][1], 60, [('is "Summon" and not', 'is "Summoned" and not')], 'forma verbale'),
    (LE[2][0], LE[2][1], 70, [('used for the ritual can', 'used for the Tribute can')], 'termine sbagliato (ritual -> Tribute)'),
    (LE[3][0], LE[3][1], 21, [("your monsters's DEF", "your monsters' DEF")], 'apostrofo del plurale'),
    (LE[3][0], LE[3][1], 74, [("FIRE monsters's ATK", "FIRE monsters' ATK")], 'apostrofo del plurale'),
    (LE[3][0], LE[3][1], 154, [('Tribe$C0"Trap Card', 'Tribe$C0" Trap Card')], 'spazio mancante'),
]
GLOBALS = [
    (r"(\$C0)\$(?= )", r"\1", "\"$\" di troppo dopo il codice colore $C0 (lezioni del tutorial)"),
]
