"""Composes the complete document docs/CHANGES_<LANG>.md starting from the CSVs of `document_changes.py` and `document_pack.py`, from the rules
(`corrections/rules_*`, `data/*.json`) and from the choices register. So the numbers and lists are the REAL ones, not hand-written.
usage: python write_changes_document.py LANGUAGE          (it|fr)  -> docs/CHANGES_IT.md / docs/CHANGES_FR.md in the project root
Run first (from the project root):
  python tools/analysis/document_changes.py ISO_ORIG ISO_DEF LANGUAGE docs/changes_<l>
  python tools/analysis/document_pack.py      ISO_ORIG LANGUAGE docs/changes_<l>"""
import collections, csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(B, 'tools', 'corrections')); sys.path.insert(0, os.path.join(B, 'tools'))
sys.stdout.reconfigure(encoding='utf-8')
import importlib
L = sys.argv[1]
ART = "l'" if L in ('it',) else 'il '
NAME = {'it': 'ITALIANO', 'fr': 'FRANCESE', 'de': 'TEDESCO', 'es': 'SPAGNOLO', 'en': 'INGLESE'}[L]
LANG = NAME.lower()
D = os.path.join(B, 'docs', f'changes_{L}')
rel = f'docs/changes_{L}'
rd = lambda n: list(csv.reader(open(os.path.join(D, n), encoding='utf-8-sig'), delimiter=';'))[1:]
js = lambda p: json.load(open(os.path.join(B, p), encoding='utf-8'))
summary = js(f'{rel}/summary.json'); rp = js(f'{rel}/pack_summary.json')
RC = importlib.import_module(f'rules_{L}')
try:
    RS = importlib.import_module(f'string_rules_{L}')
except ImportError:      # language without rules for the interface strings (still to be done)
    class RS:
        STRINGS = []; GLOBALS = []; TABLES = []
touchups = js(f'tools/data/dialogue_touchups_{L}.json'); fra = js(f'tools/data/duel_line_corrections_{L}.json')
tui = [t for t in js('tools/data/ui_texts.json') if (t['file'].split('/')[-1].split('.')[0].endswith(('_i', '_ita')) if L == 'it' else t['file'].split('/')[-1].split('.')[0].endswith(('_f', '_fra')))]
reg = [v for v in js('tools/data/editorial_choices.json')['entries'] if v['language'] == L]
o = []
w = o.append
esc = lambda s: str(s).replace('|', '\\|').replace('\n', '⏎')
esc2 = esc


def tab(head, rows, limit=None):
    w('| ' + ' | '.join(head) + ' |'); w('|' + '---|' * len(head))
    for r in (rows if limit is None else rows[:limit]):
        w('| ' + ' | '.join(esc2(c) for c in r) + ' |')
    if limit is not None and len(rows) > limit:
        w(f'\n(... altre {len(rows) - limit} righe nel CSV)')
    w('')


w(f'# MODIFICHE PER LA VERSIONE POMODORO MISTICO IN {NAME}')
w('')
w(f'Documento **completo** di tutto cio\' che la "Versione Pomodoro Mistico" cambia per {ART}{LANG}: (A) le modifiche **dirette alla ISO**, (B) il **texture pack** '
  f'(com\'e\' fatto, cosa contiene, come si compone), (C) le scelte editoriali, (D) cosa e\' verificato in gioco e cosa no, (E) come rigenerare tutto.')
w('')
w(f'**Questo file e\' generato** da `tools/analysis/write_changes_document.py {L}` a partire dai dati reali: confronto byte per byte tra la ISO originale '
  f'`PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` e la ISO corretta `..._definitiva.iso` (`document_changes.py`) e scansione del pack (`document_pack.py`). '
  f'Gli elenchi riga per riga stanno in `{rel}/*.csv` (separatore `;`, UTF-8 con BOM, a capo come `⏎`): sono la **lista esatta** di ogni cambiamento. Rigenera tutto dopo ogni modifica.')
w('')
w('Per il metodo generale e per le altre lingue: `docs/NEW_LANGUAGE_GUIDE.md`; dettagli tecnici degli script: `TUTORIAL.md`; decisioni: `docs/EDITORIAL_CHOICES.md`; texture neutre/specifiche: `docs/TEXTURE_INVENTORY.md`.')
w('')
w('## Indice')
w('- A. Modifiche alla ISO: A1 panoramica · A2 carte · A3 dialoghi · A4 frasi dei duelli · A5 stringhe dell\'interfaccia · A6 etichetta Magia/Trappola · A7 file toccati e dettagli tecnici · A8 cosa non si puo\' cambiare')
w('- B. Texture pack: B1 provenienza e struttura · B2 immagini delle carte · B3 interfaccia HD (`ui_' + L + '`) · B4 foglio numeri (`card_icon03`) · B5 targa del titolo · B6 textures.ini e composizione · B7 installazione')
w('- C. Scelte editoriali · D. Verifica in gioco · E. Come rigenerare · F. Limiti e punti aperti')
w('')
w('---')
w('')
w('# A. MODIFICHE ALLA ISO')
w('')
w('## A1. Panoramica')
w('')
w('La ISO originale **non viene mai modificata**. `tools/corrections/apply_to_iso.py ISO_ORIG ISO_OUT [lingue]` ne crea una copia in cui alcuni archivi `.ehp` sono riscritti. '
  'Se un archivio cresce (testo piu\' lungo) viene **rimesso in fondo alla ISO** in un nuovo settore e il suo voce nella directory ISO9660 viene riassegnata (`pycdlib`); '
  'la ISO `_definitiva` pesa per questo ~909 MB (l\'originale ~761 MB). **Lanciarlo sempre senza elenco di lingue (o con tutte)**: con una lingua sola sovrascrive le altre.')
w('')
tab(['Cosa', 'Quantita\' (derivata dal confronto ISO)', 'Dove sta il dato', 'File CSV'], [
    ['Carte con testo cambiato (nome e/o descrizione)', f"{summary['cards_unique']} carte ({summary['cards']} campi)", f'`tools/data/card_corrections{"" if L == "it" else "_" + L}.json` da `correzioni/rules_{L}.py`', 'cards.csv'],
    ['Righe di dialogo della storia', f"{summary['dialogues']} righe", f'`tools/data/dialogue_touchups_{L}.json` (+ base)', 'dialogues.csv'],
    ['Frasi dei duellanti nei duelli', f"{summary['sentences_unique']} frasi uniche ({summary['sentences_entries']} voci in tutti gli archivi)", f'`tools/data/duel_line_corrections_{L}.json`', 'duel_lines.csv'],
    ['Stringhe dell\'interfaccia (aiuti, schede, record, tutorial, menu...)', f"{summary['strings_unique']} stringhe uniche ({summary['strings_entries']} voci, {summary['strings_archives']} archivi)", f'`correzioni/string_rules_{L}.py` + `dati/ui_texts.json`', 'ui_strings.csv'],
    ['Immagini sostituite dentro la ISO', f"{summary['images']} (etichetta [CARTA MAGIA/TRAPPOLA] della carta grande)", '`apply_to_iso.py` (copia `card_spell_trap.gim` della lingua)', 'iso_images.csv'],
    ['File della ISO toccati (archivi `.ehp`)', f"{summary['file_touched']}", '-', 'touched_files.csv'],
    ['Altre differenze tecniche (offset ricalcolati)', f"{summary['other']}", '-', 'other.csv']], None)

# ---------------- A2 cards
w('## A2. Testi delle carte')
w('')
w(f'Archivio: `PSP_GAME/USRDIR/duelsys/cardinfo_{"ita" if L == "it" else "fra"}.ehp` (tabelle `CARD_Name_*`, `CARD_Desc_*`, `CARD_Indx_*`). **{summary["cards_unique"]} carte** hanno nome e/o descrizione modificati. '
  'Si correggono **solo errori oggettivi** (refusi, accenti, apostrofi, spazi, maiuscole incoerenti, concordanze, plurali fissi, residui di altre lingue); nomi ufficiali e terminologia del gioco non si toccano.')
w('')
w(f'Come: ogni carta e\' stata letta ({"it: 2.479 testi, uno per uno; fr: audit contro database ufficiale + lettura" if L != "en" else "inglese: elenco di tutte le carte in confronti/audit_en/carte_en.txt, solo errori oggettivi"}). Regole in `tools/corrections/rules_{L}.py`: **{len(RC.GLOBALS)} regole globali** '
  f'(regex applicate a nomi e descrizioni di tutte le carte) e **{len(RC.PER_CARD)} correzioni per carta** (`PER_CARTA`: id, campo, vecchio, nuovo, motivo; il vecchio testo deve esistere esattamente). '
  f'`generate_card_corrections.py {L} CARDINFO` ({"fonde il risultato nel `card_corrections.json` esistente, idempotente" if L == "it" else "scrive `card_corrections_{L}.json` partendo dai testi originali"}) produce il json; `apply_to_iso` lo scrive nella ISO; '
  'le immagini HD delle carte toccate si rigenerano (sezione B2).')
w('')
w('### Regole globali (tutte)')
tab(['modello (regex)', 'sostituzione', 'motivo'], [[g[0], g[1], g[2]] for g in RC.GLOBALS])
w('### Correzioni per carta (tutte)')
tab(['id', 'campo', 'vecchio', 'nuovo', 'motivo'], [list(map(str, p)) for p in RC.PER_CARD])
w(f'### Elenco completo delle carte cambiate\n**Confronto completo originale -> nuovo con le parole cambiate evidenziate: `{rel}/cards_diff.md`** (tutte le {summary["cards"]} voci). Dati grezzi: `{rel}/cards.csv`. Prime 40 righe:')
w('')
tab(['id', 'nome originale', 'campo', 'originale', 'nuovo'], rd('cards.csv'), 40)

# ---------------- A3 dialoghi
w('## A3. Dialoghi della storia')
w('')
w(f'Archivi: `script/stNN_<scena>_{"i" if L == "it" else "f"}.ehp`, ogni scena e\' una coppia di membri `...I{"i" if L == "it" else "f"}.bin` (offset in caratteri UTF-16) e `...L{"i" if L == "it" else "f"}.bin` '
  f'(stringhe UTF-16LE chiuse da NUL, alcune compresse in gzip). **{summary["dialogues"]} righe** cambiate (comprese quelle che **ereditano** la correzione perche\' hanno lo stesso testo originale e lo stesso giapponese di una riga corretta).')
w('')
w('Flusso: lettura riga per riga confrontata con inglese e giapponese -> ritocchi in `tools/data/dialogue_touchups_' + L + '.json` (`esatte` e `parti`) -> `build_dialogues.py ' + L + '` -> `dialogue_corrections_' + L + '.json` -> `apply_to_iso.py`. '
  'Regole automatiche di impaginazione in `build_dialogues.py`: ' + ('spazio dopo i segnaposto `《...》`, tre puntini seguiti da maiuscola (`...Ciao` -> `... Ciao`), base `dialogue_corrections_it_base.json` (~1.380 proposte della prima revisione).' if L == 'it' else 'spazio non separabile prima di `! ? : ;` anche dopo `》` (regola `FR_PUNT`), spazio dopo i segnaposto, "Mode histoire" -> "Mode aventure".') + ' '
  'Vincoli del box: ~46 caratteri per riga, max 3 righe (un segnaposto vale ~6 caratteri): `apply_to_iso` segnala le righe che potrebbero non starci.')
w('')
w(f'### Ritocchi di rilettura: `esatte` ({len(touchups["exact"])}) — frase intera originale -> frase nuova')
tab(['originale', 'nuovo'], [[k, v] for k, v in touchups['exact'].items()])
w(f'### Ritocchi di rilettura: `parti` ({len(touchups["parts"])}) — sostituzioni di testo applicate a ogni riga (in ordine)')
tab(['vecchio', 'nuovo'], [list(p) for p in touchups['parts']])
w(f'### Elenco completo delle righe\n**Confronto completo originale -> nuovo (con inglese e giapponese): `{rel}/dialogues_diff.md`** (tutte le {summary["dialogues"]} righe). Dati grezzi: `{rel}/dialogues.csv`. Prime 30:')
w('')
tab(['id', 'originale', 'nuovo', 'inglese'], [r[:4] for r in rd('dialogues.csv')], 30)

# ---------------- A4 frasi
w('## A4. Frasi dei duellanti nei duelli')
w('')
w(f'Tabelle `chr_wordstbl_{"i" if L == "it" else "f"}.bin` e `02chr_wordstbl_...` dentro ~72 archivi `duel/cutin_*.ehp` (e `zakov*`). Le frasi uniche sono ~{"1.800" if True else ""}: tutte rilette. '
  f'**{summary["sentences_unique"]} frasi cambiate** ({summary["sentences_entries"]} voci). Dati: `esatte` ({len(fra["exact"])}) e `parti` ({len(fra["parts"])}) in `duel_line_corrections_{L}.json`. '
  'I file `*-ptrs.txt` degli archivi dei personaggi contengono offset assoluti: se una tabella cresce vanno ricalcolati (`rimappa_puntatori`), altrimenti il duello va in crash.')
w('')
w(f'Confronto con parole evidenziate: `{rel}/duel_lines_diff.md`.')
w('')
tab(['originale', 'nuovo', 'voci', 'esempi di archivio'], rd('duel_lines.csv'))

# ---------------- A5 stringhe
w('## A5. Stringhe lunghe e corte dell\'interfaccia')
w('')
w(f'Tabelle `strTbl*`, `help_strtbl_*`, `ddstrtbl_*`, `field_strtbl*` (formato `(n, 12, 12+4n)` + offset + UTF-16) in {summary["strings_archives"]} archivi (la stessa tabella e\' copiata in piu\' archivi, es. `field/always_*_{"ita" if L == "it" else "fra"}.ehp` x6). '
  f'**{summary["strings_unique"]} stringhe uniche cambiate**. Regole: `tools/corrections/string_rules_{L}.py` — **{len(RS.STRINGS)} voci `STRINGHE`** (archivio, membro, indice 0-based, [(vecchio, nuovo)], motivo), '
  f'**{len(RS.GLOBALS)} `GLOBALI`** (regex/callable, applicate dopo le STRINGHE) su **{len(RS.TABLES)} tabelle** (`TABELLE`); piu\' {len(tui)} correzioni puntuali in `tools/data/ui_texts.json` (scrittura sul posto, testo piu\' corto o uguale).')
w('')
c = collections.Counter((r[0], r[4].count(';') + 1) for r in rd('ui_strings.csv'))
cnt = collections.Counter(r[0] for r in rd('ui_strings.csv'))
w('### Per membro (stringhe uniche cambiate)')
tab(['membro', 'stringhe'], [[k, v] for k, v in cnt.most_common()])
w('### Regole globali (tutte)')
tab(['modello', 'sostituzione', 'motivo'], [[g[0], g[1] if isinstance(g[1], str) else '(funzione) ' + getattr(g[1], '__name__', ''), g[2] if len(g) > 2 else ''] for g in RS.GLOBALS])
w('### Voci STRINGHE (tutte): dove e perche\'')
tab(['archivio', 'membro', 'indice', 'cambiamenti', 'motivo'], [[s[0], s[1], s[2], f'{len(s[3])} sostituzione/i', s[4] if len(s) > 4 else ''] for s in RS.STRINGS])
w('### Correzioni puntuali `ui_texts.json`')
tab(['file', 'membro', 'indice', 'vecchio', 'nuovo', 'motivo'], [[t['file'], t['member'], t['index'], t['old'], t['new'], t.get('reason', '')] for t in tui])
w(f'### Elenco completo\n**Confronto completo con parole evidenziate: `{rel}/ui_strings_diff.md`.** Dati grezzi: `{rel}/ui_strings.csv`. Prime 40:')
w('')
tab(['membro', 'indice', 'originale', 'nuovo'], [r[:4] for r in rd('ui_strings.csv')], 40)

# ---------------- A6/A7/A8
w('## A6. Etichetta [CARTA MAGIA] / [CARTA TRAPPOLA] della carta grande nel duello')
w('')
w('In tutti i `duel/basic_<regione><lingua>.ehp` l\'etichetta era in inglese (hash `c2268340`): `apply_to_iso.py` la sostituisce con `card_spell_trap.gim` di `field/always_<lingua>_<lingua>.ehp` (hash `9622cd75`).')
w('')
tab(['archivio', 'membro', 'hash originale', 'hash nuovo'], rd('iso_images.csv'))
w('## A7. File della ISO toccati e dettagli tecnici')
w('')
w(f'{summary["file_touched"]} archivi `.ehp` risultano diversi dall\'originale (tutte le lingue insieme, perche\' la ISO e\' unica; elenco in `{rel}/touched_files.csv`). Gli altri file (video, audio, eseguibile `EBOOT.BIN`, `PARAM.SFO`) sono identici. '
  'Differenze tecniche non testuali: `*-ptrs.txt` (offset assoluti dei membri, ricalcolati quando una tabella cambia lunghezza), nuova posizione degli archivi in fondo alla ISO.')
w('')
w('## A8. Cosa NON si puo\' cambiare (limiti del gioco)')
w('')
w('- Il **nome del parlante** nella casella del dialogo (es. "Preside Sheppard"/"Cancelliere" in italiano, "Doyen Sheppard" in francese, "Rector Sheppard" in spagnolo) sta nell\'EBOOT cifrato: non modificabile.')
w('- Testi disegnati dal gioco con il suo font (dialoghi, nomi, descrizioni nel deck, menu a tendina, tastiera di sistema, schermata di scelta lingua) non sono sostituibili dal texture pack: si cambiano solo nella ISO.')
w('- Le 438 texture di mappa/sfondi non sono sostituite (il gioco ne cambia la palette): limite del pack di MikeyMK, non del nostro lavoro.')
w('')
w('---')
w('')
w('# B. TEXTURE PACK')
w('')
w('## B1. Provenienza e struttura')
w('')
w('Base: **Yu-Gi-Oh! GX Tag Force 1 HD Remastered** di **MikeyMK** (pack USA `ULUS10136`) e carte HD di **chrisfand**, adattati alla ISO europea `ULES00600`. Il progetto non ridistribuisce il pack di terzi (`PERMESSI_AUTORI.md`): il patcher se lo fa dare dall\'utente. '
  'Il nostro lavoro: (1) rimappare gli **hash** del pack USA su quelli EU (`tools/gen_ini.py`), (2) rifare nella lingua carte e scritte dell\'interfaccia, (3) correggere i testi, (4) `upscale_extra` per le texture non coperte.')
w('')
w('PPSSPP riconosce una texture dall\'**hash dei suoi pixel** (xxhash dei dati, `gim.data_hash`); ogni riga del `textures.ini` e\' `0000000000000000<hash8> = percorso/png`. I PNG sono **4x** l\'originale e ridisegnano esattamente la stessa area. '
  'Texture identiche tra lingue hanno lo stesso hash: la sostituzione vale per tutte (vedi `docs/TEXTURE_INVENTORY.md`).')
w('')
w(f'### Struttura reale (da `{rel}/pack_structure.csv`)')
tab(['radice', 'cartella', 'file', 'MB', 'contenuto'], rd('pack_structure.csv'))
if L == 'it':
    w('Il **pack di base `PSP/TEXTURES/ULES00600` e\' gia\' italiano**: contiene `cards/small_it`, `large_it`, `tiny_it`, `ui_it` (interfaccia italiana) e le tessere italiane del titolo; le altre lingue sono moduli separati in `PSP/TEXTURES/modules/<l>`.')
else:
    w('Ogni lingua tranne l\'italiano e\' un **modulo** (`PSP/TEXTURES/modules/' + L + '`) da comporre sopra il pack di base con `tools/compose_pack.py BASE MODULI CARD_DIR OUT ' + L + ' [--copia]`: copia il base e **solo** le cartelle `cards`, `intro` e `ui_' + L + '` del modulo (hard link o copia), poi `module_ini.py` riscrive i `textures.ini`: le righe delle carte localizzate puntano a `cards/small_' + L + '`/`large_' + L + '` e le righe di `' + L + '.ini` **sostituiscono** quelle del base con la stessa chiave (hash).')
w('')
w('### Cartelle del pack di base (uguali per tutte le lingue)')
tab(['cartella', 'contenuto'], [
    ['`cards/small`, `cards/large`', 'carte piccole/grandi HD originali di chrisfand (2.833 carte) con testi inglesi; la lingua sceglie `small_<l>`/`large_<l>` via ini'],
    ['`cards/frame`', 'cornici, tabelle attributo/razza, etichette Magia/Trappola'],
    ['`cards/tinyEN/JP/MikeyMK/tiny_<l>`', 'atlante delle miniature del deck (7 pagine; stesso hash in tutte le lingue: vince un solo atlante per installazione)'],
    ['`characters`', 'ritratti, sprite e 3D dei personaggi HD (MikeyMK)'],
    ['`events`', 'immagini degli eventi (17)'],
    ['`intro`', 'logo, filmato di titolo, nuova partita; `title_screen` contiene le tessere con la targa "Versione Pomodoro Mistico"'],
    ['`map`', 'sfondi della mappa'],
    ['`shop`', 'negozio, pacchetti, stanze'],
    ['`ui`', 'interfaccia HD inglese di MikeyMK (per tutte le lingue con gli stessi hash)'],
    ['`upscale_extra`', 'texture non coperte dal pack, ingrandite 4x con xBRZ (1.192 file, ~56 MB; a risoluzione 4x/Auto lo shader 4xBRZ di PPSSPP e\' spento): include le varianti di `card_icon03` di en/fr/de/es'],
    ['`_CHOOSE YOUR CARD STYLE`', '3 `textures.ini` alternativi (mikeymk, official_english, official_japanese): copiare uno al posto di `textures.ini` per cambiare lo stile delle carte']])

# ---------------- B2 cards
w('## B2. Immagini delle carte')
w('')
cc = rp['folders_cards']
w(f'Cartelle della lingua: {", ".join(f"`{k}` ({v} file)" for k, v in cc.items())}. Ogni carta ha una **piccola HD** (nome + descrizione + tipo, rigenerata con font liberi OFL: XCharter Bold per nomi/tipo/etichette, Libre Baskerville per gli effetti, Newsreader Italic per i Normali, PT Serif Caption per Magie/Trappole, Charis SIL per i glifi mancanti) e una **grande HD** (solo il nome sulla cornice). '
  'In piu\': la **tabella degli attributi** con le parole della lingua (`cards/frame/icons_attribute_race_<l>.png`, `attributes.py`), l\'**etichetta Magia/Trappola** (`icons_spell_trap_<l>.png`, `label_it.py` / `extract_labels.py` -> `dati/label_eu_<codice>_128x32.png`) e l\'**atlante delle miniature** del deck (`tiny_<l>`, `tiny_atlas.py` + `tiny_fragment.py`).')
w('')
w(f'Quando cambia il testo di una carta (sezione A2) vanno rigenerate le sue immagini: **{rp["cards_corrected"]} carte** nel {LANG}. Elenco in `{rel}/card_images.csv`. ' + (
    'Comando: `sh tools/rebuild_corrections.sh USRDIR PACK_US PACK_MOD PYTHON` (carte piccole + grandi); su Windows `python -I` non vede i pacchetti utente: passare un wrapper che scarta `-I`.' if L == 'it' else
    'Comando: `python tools/generate_language.py fr PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` (senza ID rigenera tutte: 2.833 + 2.833, ~930 MB).'))
w('')
w('Tipografia: ' + ('apostrofo tipografico dell\'italiano e virgolette; `Tipo`, `Terreno`, `Evocazione tramite Tributo` come nel gioco.' if L == 'it' else 'spazio non separabile prima di `: ; ! ?` e virgolette « ».'))
w('')

# ---------------- B3 ui
w(f'## B3. Interfaccia HD in {LANG} (`ui_{L}`)')
w('')
w(f'**{rp["texture_ui"]} texture** (`{rel}/ui_textures.csv`: file, hash PPSSPP, famiglia, script, dimensioni originale/HD, neutra/specifica, origine nella ISO). Per famiglia: ' + ', '.join(f'{k} {v}' for k, v in rp['per_family'].items()) + '. '
  f'Di queste {rp["neutral"]} sono neutre (stesso hash in tutte le lingue) e {rp["specific"]} specifiche. '
  'Ogni famiglia ha uno script in `tools/ui_textures/<famiglia>.py` (lettura `TF1_LANG`): ridisegna le scritte texture per texture partendo dall\'originale a bassa risoluzione della ISO e dallo stile del pack inglese; stessa area e stesse posizioni (il gioco ritaglia da rettangoli fissi); un font/peso/linea di base/ombra per scritta; font liberi (`alt_font.py`).')
w('')
FAM_EN = {
    'menu_lists': "`result_e__menu01` (WIN/DRAW/LOSE e icone), `title_menu_e__m_menu_title01` (MAIN MENU · ENTER NAME · DOWNLOADED CARD LIST · DUEL PUZZLE · OPTIONS · LANGUAGE SETTINGS)",
    'icon_sheets': "`icon04` (pixel europei sul foglio USA), `panel` (frammento `ased` della linguetta), `pda_pack01` (colonna NEW)",
    'deck_screens': "linguette Trunk, Rental, Lab, Converter; `Card types in possession`; `Purchased Cards` / `Card Types Purche`; barra dorata; tasto ENTER",
    'recipe_screens': "Character, User, Downloaded Recipes, Character Recipes, User Recipes, Limited, Semi-Limited, Forbidden, Trade",
    'vs_screen': "`2nd round`, `3rd round`, foglio distintivi `1st PLAYER` / `2nd PLAYER` / `PLAYER`",
    'result_letters': "tessere `D R A W` della schermata dei risultati (`result_e`) e del banner (`basic_be`): stesso hash, 4 file",
  'tutorial': "dialogo `Your opponent has declared battle. Activate the effect of a card?` (YES/NO) e 5 carte-esempio con il testo del gioco",
}
FAM = {
    'duel_texts': ('duel/basic_<l><l>.ehp', {'it': 'Catena · TURNO (blu/rosso) · TOCCA AL GIOCATORE SUCCESSIVO (spezzata su 2 texture) · INIZIA IL DUELLO · Attacco Diretto! · foglio numeri `card_icon03` (vedi B4)', 'fr': 'Chaîne · TOUR (blu/rosso) · TOUR DU JOUEUR SUIVANT (taglio dopo SUIV) · DÉMARRER DUEL (taglio dopo DU) · Attaque Directe! · `card_icon03` e\' nella cartella `upscale_extra` (B4)', 'es': 'Cadena · TURNO DEL SIGUIENTE JUGADOR (il taglio tra le due texture passa dentro una lettera, come nell’originale) · COMENZAR DUELO · Ataque Directo · TURNO e `card_icon03` coperti da texture già presenti (stesso hash dell’italiano / `upscale_extra`)', 'de': 'Ketten · SPIELZUG (blu/rosso) · NÄCHSTER SPIELER (su 2 texture, il taglio passa dentro la L; i puntini della Ä sono una sprite a parte, ingrandita e centrata sopra la A) · DUELL BEGINNEN · Direkter Angriff! · `card_icon03` e\' nella cartella `upscale_extra` (B4)'}),
    'result_letters': ('duel/basic_<l><l>.ehp', {'it': 'HAI VINTO · HAI PERSO · PAREGGIO: una tessera 64x64 per lettera (lettere ripetute riusano la stessa tessera) + silhouette', 'fr': 'TU AS GAGNÉ · TU AS PERDU · EGALITE (senza accento: nel pareggio non esiste la tessera É)', 'es': 'HAS GANADO (HASGNDO) · HAS PERDIDO (HASPERDIO, 9 tessere) · EMPATE (EMPAT) + silhouette', 'de': 'DU GEWINNST (DUGEWINST, 9 tessere) · DU VERLIERST (DUVERLIST, 9 tessere) · UNENTSCHIEDEN (UNETSCHID, 9 tessere; E e N ripetute) + silhouette di DU GEWINNST'}),
    'menu_lists': ('title_menu/title_menu_<l>.ehp, duel/result/result_<l>.ehp, field/always_bri_<cod>.ehp', {'it': 'titoli dei menu (`m_menu_title01`, `trnsmt02`, `menu02`, `press_start0003`), etichette risultato, calendario (giorni, mesi, "giorni al torneo", Mattino/Sera)', 'fr': 'MENU PRINCIPAL · SAISIR NOM · LISTE CARTES TÉLÉCHARGÉE · PUZZLE DUEL · OPTIONS · SÉLECTION DE LA LANGUE · LISTE DE GROUPE... · RÉSULTAT DU DUEL · APPUYEZ SUR LA TOUCHE START · GAGNÉ/ÉGALITÉ/PERDU · Dimanche...Samedi · Mai Juillet Juin Août · jours / avant le tournoi · Matin / Soir', 'es': 'MENÚ PRINCIPAL · INTRODUCE EL NOMBRE · LISTA DE CARTAS DESCARGADAS · DUELO ACERTIJO · OPCIONES · AJUSTES DEL IDIOMA · AGRUPAR LISTA... · RESULTADO DEL DUELO · PRESIONA EL BOTÓN START · GANAS/EMPATE/PIERDES · Domingo...Sábado · Mayo Julio Junio Agosto · Días / para el torneo / de · AM / PM'}),
    'icon_sheets': ('deck/all_<l>.ehp, shop/all_<l>.ehp, field/always_*', {'it': 'fogli di icone: `icon04` (Mia/L e distintivi), `s_pack` (ESAURITE), `panel` (frammento del tab), `icon06` (N), `pda_pack01` (NUOVO), `mein_menu00`, `trnsmt01`, `ocglist`', 'fr': '`icon04`, `s_pack` (ÉPUISÉ), `panel` (frammento "hetés"); `pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01` restano con "NEW" come nell\'originale francese', 'es': '`icon04`, `s_pack` (AGOTADO), `panel` (frammento "rados"); `pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01` hanno lo stesso hash dell’inglese'}),
    'deck_screens': ('deck/all_<l>.ehp, labo/*.ehp, shop/all_<l>.ehp', {'it': 'linguette Cassa, **Fusion**, Side, Deck, Affitto, Laboratorio, Convertitore, "Tipi di Carte Posseduti", "Carte Comprate", tasto INVIO', 'fr': 'Coffre ×2, Location ×3, Labo, Convertisseur, "Types de cartes acquis", "Cartes achetées" (+ frammento), ENTRÉE', 'es': 'Tronco ×3, Fusión, Alquiler ×4, Laboratorio, Conversor ×2, "Tipos de carta en posesión", "Cartas compradas" (+ frammento), ACEPTAR'}),
    'recipe_screens': ('deck/recipe_view_<l>.ehp, title_menu/title_menu_<l>.ehp, database/limitlist.ehp', {'it': 'linguette Personaggio / Utente / Scaricata / Limitata / Semi-limitata / Vietata / Scambio e pannelli ricette', 'fr': 'Personnage / Utilisateur / Téléchargée / Limitée / Semi-limitée / Interdite / Échange (nel gioco originale "Scambia" era un residuo italiano)', 'es': 'Personaje / Usuario / Recetas descargadas / Recetas de personaje / Recetas de usuario / Limitada / Semi-Limitada / Prohibida / Cambiar'}),
    'vs_screen': ('duel/start/start_e.ehp (membri _<l>), start_all.ehp, start_<l>.ehp', {'it': 'banner DUEL / NORMAL / TAG, bagliori, "Modalità ...", "n A GIOCARE", "n Duello", foglio sasso-carta-forbici (VITTORIA/SCONFITTA/PAREGGIO), foglio giocatori ("n° GIOCATORE")', 'fr': 'DUEL / NORMAL / TAG · DEUXIÈME À JOUER / PREMIER À JOUER · 1er/2e/3e round · Mode Un Duel / Mode Match · GAGNÉ/PERDU/EGALITE · 1er JOUEUR / 2e JOUEUR · JOUEUR', 'es': 'DUELO / NORMAL / TAG · SEGUNDO EN SALIR / PRIMERO EN SALIR · 1ra/2da/3ra vuelta · Modo Individual / Modo Combate · GANAS/PIERDES/EMPATE · JUGADOR 1 / JUGADOR 2 · JUGADOR'}),
    'tutorial': ('tutorial/tutorial_<l>.ehp (tuto_duelimg01..06)', {'it': 'illustrazione del dialogo di attivazione (testi, bottoni SI/NO, carta piccola) + 5 cartine con disco del tipo', 'fr': '"Ton adversaire a déclaré le duel." / "Activer l\'effetto de la carte ?" · OUI/NON · 5 cartine; geometria diversa (dialogo a 2 righe)', 'es': 'Tu oponente ha declarado la batalla. / ¿activar el efecto de la carta? · SÍ/NO · 5 cartine; dialogo a 2 righe ma riquadro più largo'})}
SCRIPT_OF = {'duel_texts': 'duel_texts', 'result_letters': 'result_letters', 'menu_lists': 'menu_lists', 'icon_sheets': 'icon_sheets',
             'deck_screens': 'deck_screens', 'recipe_screens': 'recipe_screens', 'vs_screen': 'vs_screen', 'tutorial': 'tutorial'}   # pack family -> script
rows = []
for f, n in rp['per_family'].items():
    a, t = FAM.get(f, ('?', {}))
    rows.append([f, n, f'`tools/ui_textures/{SCRIPT_OF.get(f, f)}.py`', a.replace('<l>', {'it': 'i', 'fr': 'f', 'es': 's', 'de': 'g', 'en': 'e'}[L]), t.get(L, FAM_EN.get(f, '') if L == 'en' else '')])
tab(['famiglia', 'texture', 'script', 'archivio ISO sorgente', 'testi della lingua'], rows)
w('Regole di qualita\' (valgono per ogni lingua): lettere regolari, mai deformate una per una; stessa area dell\'originale; niente sfocature; il testo e\' quello dell\'originale della lingua (si correggono solo errori evidenti: residui di altre lingue, accenti); pixel art **non** levigata senza conferma; geometrie sempre misurate sull\'originale.')
w('')
w('### Testi disegnati: originale -> HD')
w("Tabella letta a occhio, texture per texture: `docs/changes_" + L + "/texture_texts_" + L + ".md`." + (" Differenze rispetto all'originale: `TAUSCHEN`/`Tauschen` -> `SCAMBIO`/`Scambio`, `Fusione` -> `Fusion`; tutto il resto riscrive le stesse parole." if L == 'it' else " Nessuna parola cambiata: l'HD riscrive le stesse parole dell'originale inglese (tranne `DOWNLOADED CARD LIST`, che il pack USA ha come `DOWNLOAD`)." if L == 'en' else " Differenze rispetto all'originale: `DEMARRER` -> `DÉMARRER`, `SCAMBIA`/`Scambia` -> `ÉCHANGE`/`Échange`, `2è/3è round` -> `2e/3e round`; tutto il resto riscrive le stesse parole."))
w('')
w('### Elenco di ogni texture')
w(f'(tutte le {rp["texture_ui"]} righe, da `ui_textures.csv`)')
w('')
tab(['file nel pack', 'hash', 'famiglia', 'originale px', 'HD px', 'tipo', 'origine ISO'], [[r[0], r[1], r[2], r[4], r[5], r[6], r[8]] for r in rd('ui_textures.csv')])
if L == 'it':
    w('### Texture italiane senza controparte in `ui_fr` (19) e perche\'')
    w('13 sono neutre (stesso hash in tutte le lingue: pannelli ricette, linguette Side/Deck/Fusion Deck, barre, `card_side`...). 6 hanno wording locale nell\'originale (`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `d_window00016`, `duelrecord parts`): l\'italiano ha NUOVO / N / Fusion, il francese originale ha NEW / Fusion e ha gia\' i suoi HD in `upscale_extra`. La linguetta dell\'editor deck dice **Fusion** (non "Fusione"): "Fusion Deck" si chiama cosi\' in tutte le lingue.')
elif L == 'en':
    w("### Texture inglesi che restano com'erano")
    w("Le texture inglesi gia' coperte dal pack USA (stesso hash: 621) vengono da MikeyMK e non si toccano. Restano **ingrandite con xBRZ** (`upscale_extra`) o senza file (14, frammenti senza testo: si vedono come l'originale) le texture senza testo o comuni a tutte le lingue (le 4 tessere DRAW della schermata dei risultati sono ridisegnate in `result_letters`). 17 texture del pack italiano hanno lo stesso hash di quelle inglesi (`ITA-SU-ING`): controllate una a una, sono senza testo. Elenco completo: `docs/changes_en/texture_inventory_en.txt`.")
else:
    w('### Texture che restano come l\'originale')
    w('`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `parts` sono fogli di icone in pixel art (con NEU/NEW): restano com\'erano, coperti dall\'ingrandimento `upscale_extra` come nelle altre lingue; il testo non e\' stato cambiato. Le texture neutre vengono dal pack di base. In spagnolo anche `score-top` (TURNO) ha lo stesso hash dell\'italiano e `card_icon03` e\' in `upscale_extra`.')
w('')

# ---------------- B4
w('## B4. Il foglio dei numeri del duello (`card_icon03`)')
w('')
w('Foglio unico con cifre LP, tempo, tasti e moltiplicatori; hash diverso per lingua. Ricetta scelta dall\'utente (`tools/ui_textures/icon03_languages.py`, rilanciare con `--apply`):')
w('- righe 0-180 (cifre piccole e segni, tasti arancioni 1/2/3, cifre grandi 0-9 con "LP", cifre piccole 0-9): **dal pack USA**, pixel art netta;')
w('- celle in cui il gioco europeo differisce dal pack USA (spunta nera, palla grigia, pillola vuota, parola del tempo): **pixel originali ingranditi 4x senza sfumare**; parola del tempo ' + {'it': '**TEMPO**', 'fr': '**TEMPS**', 'de': '**ZEIT**', 'es': '**TIEMPO**', 'en': '**TIME**'}[L] + '; la pillola arancione ("Single" nel pack USA) resta **vuota**;')
w('- righe >= 181 (moltiplicatori x1..x12, icone, carte, frecce): dal foglio italiano gia\' nel pack (`tools/data/card_icon03_base_it.png`);')
w('- le celle europee si incollano **solo nella loro fascia** di righe (altrimenti rovinano la parte alta delle cifre grandi).')
w('')
w('File: it -> `ui_it/duel_texts/basic_ii__card_icon03.png` (hash 376925c7); fr -> `upscale_extra/3e5482fd.png`; en ee0c44c3; de ffe309a6; es 859eea2b. Anteprime in `confronti/icon03/`.')
w('')
# ---------------- B5
w('## B5. Targa del titolo')
w('')
w(f'`python tools/ui_textures/mystic_tomato_title.py {L}` genera 2 PNG (`542eff79685c434d`, `705176739829dcf5`, tessere 18 e 19 del fondale di 20 tessere 128x64 `title_menu_i.ehp: main_title00001..00020`) con la carta 4930 nella lingua + la formula "versione" + la bandiera, font PT Sans Bold: '
  + '**"' + {'it': 'VERSIONE POMODORO MISTICO', 'fr': 'VERSION TOMATE MYSTIQUE', 'de': 'EDITION MYSTISCHE TOMATE', 'es': 'EDICIÓN TOMATE MÍSTICO', 'en': 'VERSION MYSTIC TOMATO'}[L] + '"**' + '. La targa **va inclusa solo per la lingua scelta** (vive in `moduli/' + L + '/intro/title_screen/`); il pack di base originale ha le tessere senza banner. File in questo pack: ' + ', '.join(f'`{b}`' for b in rp['banner'] if 'title_screen' in b and ('542eff' in b or '705176' in b)) + '.')
w('')
# ---------------- B6
w('## B6. `textures.ini` e composizione')
w('')
w('`tools/gen_ini.py TOOLS US_INI CARD_DIR OUT_INI i=it +extra_it.ini +ui_it.ini +dati/upscale_extra.ini` converte il `textures.ini` USA in quello EU: le voci non-carta restano (texture neutre = stessi hash); le voci carta sono rigenerate dagli archivi `card/*.cip` EU per le 5 lingue (`i=it` rimappa `cards/large/X.png` -> `cards/large_it/X.png`); aggiunge l\'etichetta Magia/Trappola (`extra_it.ini`), le righe `ui_it` e `upscale_extra.ini`. Si fa anche per i 3 stili carte. '
  'Se gli stessi pixel esistono in piu\' lingue vince la prima in `e i f g s` (per questo atlante, banner e tabella attributi sono "uno per installazione").')
w('')
w(f'Righe `ui_{L}` nel `{"textures.ini" if L == "it" else L + ".ini"}`: {rp["rows_ini_ui"]}. Frequenza dei prefissi: `{rel}/ini_lines.csv`. Controllo: ogni riga `ui_{L}/...` deve puntare a un file esistente e non devono esserci hash duplicati.')
w('')
w('## B7. Installazione e impostazioni')
w('')
w('PC: copiare `ULES00600` in `<PPSSPP>/PSP/TEXTURES/` (Android: `textures.zip` in `.../TEXTURES/ULES00600/`, senza estrarlo; rigenerare lo zip con le correzioni). Impostazioni: **Sostituisci texture ON**, risoluzione di rendering **4x**, lingua del gioco = lingua del modulo (la lingua e\' scritta nel **salvataggio**). Dopo aver cambiato un solo PNG basta copiarlo e riavviare PPSSPP (cache). Per provare i testi usare la ISO `_definitiva`.')
w('')
w('---')
w('')
w('# C. SCELTE EDITORIALI')
w('')
if L == 'it':
    w('- **Preside** (mai "Cancelliere") per Sheppard, compreso "Ufficio del Preside" e "Profilo del Preside Sheppard".')
    w('- **Segna-Mostro** (non "Gettoni Mostro") in aiuti, record e carte; `Segna-Opzione`.')
    w('- Banner: "direttore dello Slifer Rosso"; dormitori **Slifer Rosso, Ra Giallo, Obelisk Blu**; `Modalità Storia` e\' il nome del menu.')
    w('- Linguetta **Fusion** (non Fusione). `E\'` -> `È`; `Life Point` -> `Life Points`; punteggiatura e apostrofi corretti.')
    w('- Scene censurate riportate al giapponese: sake/shochu e abito da cameriera (vedi sotto); "Beh, non sono poi così bravo..." (era "sto sbavando").')
else:
    if L == 'fr':
        w('- **Doyen / Chancelier**: dialogo per dialogo, formale -> "Chancelier", informale -> "Doyen"; nelle schede UI "Chancelier Sheppard".')
        w('- Punteggiatura francese `! ? : ;` con spazio (anche dopo `》`); "Mode histoire" -> "Mode aventure" (nome vero del menu).')
        w('- `Échange` al posto di "Scambia" (residuo italiano); "2e/3e round"; "EGALITE" senza accento; "DÉMARRER DUEL".')
        w('- `Piège Continu` e\' il termine coerente di tutto il gioco: non si cambia.')
    elif L == 'en':
        w("- **Solo errori oggettivi** dell'inglese europeo: refusi (`Sryus`, `Principle's`, `Bandanna`), articoli (`a Equip Spell` -> `an Equip Spell`, `face-down card` -> `a face-down card`), apostrofi (`monsters's`, `opponents cards`), concordanze, forme verbali dei tutorial (`\"Summon\" it` -> `\"Summoning\" it`), spazi e `$` di troppo nei codici colore. Nessuna riscrittura di stile.")
        w("- `Chancellor Sheppard` nelle schede, come nei dialoghi; `Bandana` come nei dialoghi.")
        w("- Termini di carte e testi lasciati come nel gioco; le 82 carte corrette hanno il testo rigenerato nelle immagini HD (`moduli/en/cards`).")
        w("- La targa del titolo inglese e' `VERSION MYSTIC TOMATO` (confermato dall'utente il 2026-10-13).")
    else:
        w('- **Rector Sheppard** (come nei dialoghi) nelle schede e nelle mappe ("Oficina del Rector"); dormitori **Slifer Rojo, Ra Amarillo, Obelisco Azul**; **Jinetes de la Sombra**; "Habitación" al posto di "Alójese" (Room).')
        w('- Sake/shochu e abito da cameriera come nelle altre lingue (`st01_t01/Scr003E`), `st02_t01/Scr101E` ruotato; "Sirviente de la Calavera", "Toon", "Archidemonio", "Trío Ojama" e accenti dei nomi come sulle carte.')
        w('- Opzioni: "EN/FUERADE" -> "ON/OFF"; messaggi del titolo ("nuevos datos de juego"), lezioni del tutorial ("le turno" -> "es el turno de", tasti x/o scambiati, codici colore chiusi), paragrafo finale dei Duelos Tag tradotto (era troncato/in inglese).')
        w('- Termini lasciati come nel gioco: "Invocación por Sacrificio", "Tributar", "Efecto de Blanco", "Tronco" (domande aperte in `docs/changes_es/open_questions_es.md`).')
w('- Foglio numeri: cifre/LP dal pack USA, x1..x12 dal foglio italiano, parola del tempo ' + {'it': 'TEMPO', 'fr': 'TEMPS', 'de': 'ZEIT', 'es': 'TIEMPO', 'en': 'TIME'}[L] + '.')
w('')
w('### Voci del registro delle scelte per questa lingua (`tools/data/editorial_choices.json`)')
tab(['id', 'originale', 'corretto', 'ereditata', 'motivo'], [[v['id'], v['original'], v['corrected'], 'si' if v['inherited'] else 'no', v['reason']] for v in reg])
w('Altre scelte e la rilettura delle frasi dei duelli: `docs/EDITORIAL_CHOICES.md`.')
w('')
w('# D. VERIFICA IN GIOCO')
w('')
if L == 'it':
    w('- Visto in gioco: interfaccia HD italiana, stringhe lunghe riscritte (aiuti, schede, tutorial), terminologia Preside/Segna-Mostro, carte HD e etichetta Magia/Trappola della carta grande.')
    w('- **Non visto** dopo gli ultimi cambi: rilettura carte (65 carte nuove), frasi dei duelli corrette, linguetta "Fusion", 4 avvisi di lunghezza box dei dialoghi (en/es/de #147/#151, de #172).')
else:
    if L == 'de':
        w('- **Visti in gioco** (ISO `_definitiva` + modulo `de`, nuovo gioco in tedesco, 2026-10-12): scelta lingua, titolo con targa "MYSTISCHE TOMATE EDITION" e Neues Spiel/Fortfahren, "Daten geladen", Hauptmenue HD, Deck-Menue (Deck bearbeiten / Rezeptanzeige), editor del deck (linguette Deck/Fusion/Side/Truhe, "Persoenliches Deck", "Eigene Kartentypen", Hilfe), Rezeptanzeige (Benutzer/Charakter, Fusionsdeck), conferma "Deckbearbeitung verlassen", calendario ("1. Mai / Montag", "92 Tage bis zum Turnier"), mappa ("Duellakademie", elenco luoghi), menu dell\'ufficio (Reden/Duell/Gegenstaende/PDA), dialoghi del cancelliere e di Crowler in Klassenzimmer con le correzioni (Buero des Kanzlers, Duellakademie, Haupttor...), box a 2-3 righe senza tagli.')
        w('- **Non visti** (solo letti e confrontati con l\'originale nei fogli di confronto): Kette, Direktangriff, fine duello, sasso-carta-forbici, ZWEITER/ERSTER, 1. Runde, tutorial e lezioni, negozio (AUSVERKAUFT, "Gekaufte Karten"), laboratorio (Labor, Konverter, Miete), PDA, album, Optionen, carte con testo nuovo, frasi dei duelli, schermata VS.')
        w('- **Visti nel duello dimostrativo del titolo** (2026-10-12): schermata VS ("NORMALES DUELL", "Einzelmodus", "Gegen", distintivi), HUD del duello, frasi dei duellanti in tedesco, descrizioni di carte in tedesco; "Draw Phase" resta inglese come nell\'originale. Difetti segnalati dall\'utente: font dei dialoghi non HD (testo di sistema, non sostituibile con le texture) e menu di salvataggio PSP in francese (lingua di sistema di PPSSPP).')
    elif L == 'fr':
        w('- Visti in gioco (ISO `_definitiva`): titolo con targa, menu, editor del deck.')
    elif L == 'en':
        w("- **Non visto in gioco**: la ISO `_definitiva` e il pack inglese composto non sono ancora stati provati in PPSSPP. Controllati solo sui dati: `apply_to_iso.py` a 0 avvisi, ogni riga `ui_en` del `textures.ini` punta a un file esistente, confronti originale/HD in `docs/changes_en/sheets/` (originale 4x accanto all'HD, riletti a occhio).")
        w("- Da vedere in gioco: carta con testo nuovo, dialoghi corretti, aiuti dell'editor, linguette Trunk/Rental/Lab/Converter, `Purchased Cards`, `2nd/3rd round`, distintivi `1st/2nd PLAYER`, `MAIN MENU` e voci del menu, tutorial del duello.")
    else:
        w('- **Visti in gioco** (ISO `_definitiva` + modulo `es`, nuovo gioco in spagnolo, 2026-10-12): scelta lingua, titolo con targa "EDICIÓN TOMATE MÍSTICO" e "PRESIONA EL BOTÓN START", Juego Nuevo/Continuar, "INTRODUCE EL NOMBRE", messaggi di sistema del salvataggio, Menú Principal HD, Lista de Duelistas, editor del deck (linguette Deck/Fusión/Side/Tronco, "Tipos de carta en posesión"), Opciones (ON/OFF, aiuti).')
        w('- **Non visti** (solo letti e confrontati con l\'originale nei fogli di confronto): duello (Cadena, Ataque Directo, fine duello, VS, sasso-carta-forbici), tutorial e lezioni, negozio, laboratorio, calendario, carte con testo nuovo, dialoghi corretti della storia, frasi dei duelli.')
w('')
w('# E. COME RIGENERARE TUTTO')
w('')
w('```')
w('# ISO (tutte le lingue insieme)')
w('python tools/corrections/build_dialogues.py ' + L)
w('python tools/corrections/generate_card_corrections.py ' + L + ' CARDINFO_' + L + '.ehp          # carte')
w('python tools/corrections/apply_to_iso.py PSP/GAME/ULES00600_..._EUR.iso PSP/GAME/ULES00600_..._EUR_definitiva.iso')
w('# immagini')
w(('sh tools/rebuild_corrections.sh USRDIR PACK_US PACK_MOD PYTHON' if L == 'it' else 'python tools/generate_language.py fr PACK CARDINFO US_INI CLEAN_DIR OUT [ID...]') + '')
w('TF1_LANG=' + L + ' python tools/ui_textures/<famiglia>.py USRDIR PACK_US <modulo>      # per ognuna delle 8 famiglie (intera!)')
w('python tools/ui_textures/icon03_languages.py --apply ; python tools/ui_textures/mystic_tomato_title.py ' + L)
w('python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules USRDIR/card OUT ' + L + ' --copia')
w('# questo documento')
w('python tools/analysis/document_changes.py ISO_ORIG ISO_DEF ' + L + ' docs/changes_' + L)
w('python tools/analysis/document_pack.py ISO_ORIG ' + L + ' docs/changes_' + L)
w('python tools/analysis/text_comparisons.py ' + L)
w('python tools/analysis/write_changes_document.py ' + L)
w('```')
w('Input esterni da avere (controlla che esistano): ISO originale, USRDIR estratta (`tools/analysis/extract_usrdir.py`), pack USA di MikeyMK `ULUS10136` (in una cartella fuori dal progetto).')
w('')
w('# F. LIMITI E PUNTI APERTI')
w('')
if L == 'it':
    w('- Nomi ufficiali delle carte: da decidere con l\'utente. "Ragazza Mago Nero" vs "Maga Nera".')
    w('- Le note a mano sulla rilettura delle carte prima di ~riga 1830 sono andate perse; per quel tratto c\'e\' anche una scansione automatica (refusi, spazi, apostrofi).')
    w('- `textures.zip` Android da rigenerare con le correzioni; carte del pack installato da riavviare in PPSSPP (cache).')
else:
    if L == 'fr':
        w('- Variante opzionale `N`/NOUVEAU al posto di `NEW` nelle 4 texture con wording locale.')
        w('- `textures.zip` Android per il francese: non fatto; nessuna prova su telefono.')
        w('- Etichette lunghe da verificare in gioco: "Rechercher", "Aucune restriction", "Étiquette".')
    elif L == 'de':
        w("- Texture tedesche aggiunte il 2026-10-13 (`result_letters` 28, `duel_texts` 15; prima date per uguali all'inglese, ed era un errore: vedi `docs/changes_de/texture_texts_de.md`): confrontate con l'originale a bassa risoluzione (sovrapposizione delle tessere, fogli di controllo), **non ancora viste in gioco**. Da verificare: il centraggio dei puntini della Ä di NÄCHSTER SPIELER (sprite a parte), la larghezza di SPIELZUG nel badge e la sagoma di DU GEWINNST.")
        w('- 5 fogli di icone in pixel art (`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `parts`) restano ingranditi dal pack (domanda aperta n. 7 in `open_questions_de.md`; in `pda_pack01` il gioco ha un residuo italiano "NUOVO" accanto ai "NEU", come in fr/es).')
        w('- `textures.zip` Android per il tedesco: non fatto; nessuna prova su telefono.')
    elif L == 'en':
        w("- **Decisioni dell'utente (2026-10-13)**: nome del logo `VERSION MYSTIC TOMATO` confermato; tessere DRAW da ridisegnare (fatto); (1) nome del logo confermato; (2) `DOWNLOADED CARD LIST` (europeo) contro `DOWNLOAD` (testo USA): scelto l'europeo, confermato dall'utente.")
        w("- `textures.zip` Android per l'inglese: non fatto; nessuna prova su telefono.")
        w("- I testi disegnati nelle texture sono in `docs/changes_en/texture_texts_en.md` (letti a occhio).")
    else:
        w('- Domande dell\'utente risolte il 2026-10-12 (nomi di carte rotti corretti sul nome ufficiale, Kaiba Corporation, Duelo maiuscolo, Rector, Sacrificio al posto di Tributo): `docs/changes_es/open_questions_es.md`.')
        w('- 14 texture spagnole senza HD (frammenti senza testo: `recipe_sel`, `t_window0002`, `limitlist window_s0010/20`, `jyanken100005/7`, `recipe010011`, `bg_base_cloud02`) restano come l\'originale.')
        w('- `textures.zip` Android: non fatto; nessuna prova su telefono. I testi disegnati nelle texture sono in `docs/changes_es/texture_texts_es.md` (letti a occhio).')
w('- Il nome del parlante nella casella del dialogo non e\' modificabile (EBOOT cifrato).')
open(os.path.join(B, 'docs', f'CHANGES_{L.upper()}.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(o) + '\n')
print(len(o), 'lines ->', f'docs/CHANGES_{L.upper()}.md')
