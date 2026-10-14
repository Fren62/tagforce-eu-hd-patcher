"""Composes the complete document docs/CHANGES_<LANG>.md starting from the CSVs of `document_changes.py` and `document_pack.py`, from the rules
(`corrections/rules_*`, `data/*.json`) and from the choices register. So the numbers and lists are the REAL ones, not hand-written.
usage: python write_changes_document.py LANGUAGE          (it|fr|de|es|en)  -> docs/CHANGES_IT.md ... in the project root
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
NAME = {'it': 'ITALIAN', 'fr': 'FRENCH', 'de': 'GERMAN', 'es': 'SPANISH', 'en': 'ENGLISH'}[L]
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
        w(f'\n(... {len(rows) - limit} more rows in the CSV)')
    w('')


w(f'# CHANGES OF THE MYSTIC TOMATO VERSION FOR {NAME}')
w('')
w(f'**Complete** document of everything the "Mystic Tomato Version" changes for {LANG}: (A) the **direct changes to the ISO**, (B) the **texture pack** '
  f'(how it is made, what it contains, how it is composed), (C) the editorial choices, (D) what has been verified in game and what has not, (E) how to regenerate everything.')
w('')
w(f'**This file is generated** by `tools/analysis/write_changes_document.py {L}` from the real data: byte-by-byte comparison between the original ISO '
  f'`PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` and the corrected ISO `..._definitiva.iso` (`document_changes.py`) and a scan of the pack (`document_pack.py`). '
  f'The row-by-row lists are in `{rel}/*.csv` (`;` separator, UTF-8 with BOM, line breaks as `⏎`): they are the **exact list** of every change. Regenerate everything after each modification.')
w('')
w('For the general method and for the other languages: `docs/NEW_LANGUAGE_GUIDE.md`; technical details of the scripts: `docs/TUTORIAL.md`; decisions: `docs/EDITORIAL_CHOICES.md`; neutral/specific textures: `docs/TEXTURE_INVENTORY.md`.')
w('')
w('## Index')
w('- A. Changes to the ISO: A1 overview · A2 cards · A3 dialogues · A4 duel sentences · A5 interface strings · A6 Spell/Trap label · A7 touched files and technical details · A8 what cannot be changed')
w('- B. Texture pack: B1 origin and structure · B2 card images · B3 HD interface (`ui_' + L + '`) · B4 number sheet (`card_icon03`) · B5 title plate · B6 textures.ini and composition · B7 installation')
w('- C. Editorial choices · D. In-game verification · E. How to regenerate · F. Limits and open points')
w('')
w('---')
w('')
w('# A. CHANGES TO THE ISO')
w('')
w('## A1. Overview')
w('')
w('The original ISO is **never modified**. `tools/corrections/apply_to_iso.py ISO_ORIG ISO_OUT [languages]` creates a copy in which some `.ehp` archives are rewritten. '
  'If an archive grows (longer text) it is **put again at the end of the ISO** in a new sector and its entry in the ISO9660 directory is reassigned (`pycdlib`); '
  'for this reason the `_definitiva` ISO weighs ~909 MB (the original ~761 MB). **Always run it without a list of languages (or with all of them)**: with a single language it overwrites the others.')
w('')
tab(['What', 'Quantity (derived from the ISO comparison)', 'Where the data lives', 'CSV file'], [
    ['Cards with changed text (name and/or description)', f"{summary['cards_unique']} cards ({summary['cards']} fields)", f'`tools/data/card_corrections{"" if L == "it" else "_" + L}.json` from `tools/corrections/rules_{L}.py`', 'cards.csv'],
    ['Story dialogue lines', f"{summary['dialogues']} lines", f'`tools/data/dialogue_touchups_{L}.json` (+ base)', 'dialogues.csv'],
    ['Duelist sentences in duels', f"{summary['sentences_unique']} unique sentences ({summary['sentences_entries']} entries in all the archives)", f'`tools/data/duel_line_corrections_{L}.json`', 'duel_lines.csv'],
    ['Interface strings (help, cards, records, tutorial, menus...)', f"{summary['strings_unique']} unique strings ({summary['strings_entries']} entries, {summary['strings_archives']} archives)", f'`tools/corrections/string_rules_{L}.py` + `tools/data/ui_texts.json`', 'ui_strings.csv'],
    ['Images replaced inside the ISO', f"{summary['images']} ([SPELL CARD/TRAP CARD] label of the large card)", '`apply_to_iso.py` (copies the language\'s `card_spell_trap.gim`)', 'iso_images.csv'],
    ['ISO files touched (`.ehp` archives)', f"{summary['file_touched']}", '-', 'touched_files.csv'],
    ['Other technical differences (recomputed offsets)', f"{summary['other']}", '-', 'other.csv']], None)

# ---------------- A2 cards
w('## A2. Card texts')
w('')
w(f'Archive: `PSP_GAME/USRDIR/duelsys/cardinfo_{"ita" if L == "it" else "fra"}.ehp` (tables `CARD_Name_*`, `CARD_Desc_*`, `CARD_Indx_*`). **{summary["cards_unique"]} cards** have a modified name and/or description. '
  'Only **objective errors** are corrected (typos, accents, apostrophes, spaces, inconsistent capitalization, agreement, fixed plurals, leftovers from other languages); official names and the game\'s terminology are not touched.')
w('')
w(f'How: every card was read ({"it: 2,479 texts, one by one; fr: audit against the official database + reading" if L != "en" else "English: list of all the cards in comparisons/audit_en/cards_en.txt, objective errors only"}). Rules in `tools/corrections/rules_{L}.py`: **{len(RC.GLOBALS)} global rules** '
  f'(regexes applied to the names and descriptions of all the cards) and **{len(RC.PER_CARD)} per-card corrections** (`PER_CARD`: id, field, old, new, reason; the old text must exist exactly). '
  f'`generate_card_corrections.py {L} CARDINFO` ({"merges the result into the existing `card_corrections.json`, idempotent" if L == "it" else "writes `card_corrections_{L}.json` starting from the original texts"}) produces the json; `apply_to_iso` writes it into the ISO; '
  'the HD images of the touched cards are regenerated (section B2).')
w('')
w('### Global rules (all)')
tab(['pattern (regex)', 'replacement', 'reason'], [[g[0], g[1], g[2]] for g in RC.GLOBALS])
w('### Per-card corrections (all)')
tab(['id', 'field', 'old', 'new', 'reason'], [list(map(str, p)) for p in RC.PER_CARD])
w(f'### Complete list of changed cards\n**Complete original -> new comparison with the changed words highlighted: `{rel}/cards_diff.md`** (all {summary["cards"]} entries). Raw data: `{rel}/cards.csv`. First 40 rows:')
w('')
tab(['id', 'original name', 'field', 'original', 'new'], rd('cards.csv'), 40)

# ---------------- A3 dialogues
w('## A3. Story dialogues')
w('')
w(f'Archives: `script/stNN_<scene>_{"i" if L == "it" else "f"}.ehp`, every scene is a pair of members `...I{"i" if L == "it" else "f"}.bin` (offsets in UTF-16 characters) and `...L{"i" if L == "it" else "f"}.bin` '
  f'(UTF-16LE strings terminated by NUL, some gzip-compressed). **{summary["dialogues"]} lines** changed (including those that **inherit** the correction because they have the same original text and the same Japanese as a corrected line).')
w('')
w('Flow: line-by-line reading compared with English and Japanese -> touch-ups in `tools/data/dialogue_touchups_' + L + '.json` (`exact` and `parts`) -> `build_dialogues.py ' + L + '` -> `dialogue_corrections_' + L + '.json` -> `apply_to_iso.py`. '
  'Automatic layout rules in `build_dialogues.py`: ' + ('space after the `《...》` placeholders, three dots followed by a capital (`...Ciao` -> `... Ciao`), base `dialogue_corrections_it_base.json` (~1,380 proposals of the first review).' if L == 'it' else 'non-breaking space before `! ? : ;` also after `》` (rule `FR_PUNCT`), space after the placeholders, "Mode histoire" -> "Mode aventure".') + ' '
  'Box constraints: ~46 characters per line, max 3 lines (a placeholder counts ~6 characters): `apply_to_iso` reports the lines that might not fit.')
w('')
w(f'### Re-reading touch-ups: `exact` ({len(touchups["exact"])}) — whole original sentence -> new sentence')
tab(['original', 'new'], [[k, v] for k, v in touchups['exact'].items()])
w(f'### Re-reading touch-ups: `parts` ({len(touchups["parts"])}) — text replacements applied to every line (in order)')
tab(['old', 'new'], [list(p) for p in touchups['parts']])
w(f'### Complete list of lines\n**Complete original -> new comparison (with English and Japanese): `{rel}/dialogues_diff.md`** (all {summary["dialogues"]} lines). Raw data: `{rel}/dialogues.csv`. First 30:')
w('')
tab(['id', 'original', 'new', 'English'], [r[:4] for r in rd('dialogues.csv')], 30)

# ---------------- A4 sentences
w('## A4. Duelist sentences in duels')
w('')
w(f'Tables `chr_wordstbl_{"i" if L == "it" else "f"}.bin` and `02chr_wordstbl_...` inside ~72 `duel/cutin_*.ehp` archives (and `zakov*`). The unique sentences are ~1,800: all re-read. '
  f'**{summary["sentences_unique"]} sentences changed** ({summary["sentences_entries"]} entries). Data: `exact` ({len(fra["exact"])}) and `parts` ({len(fra["parts"])}) in `duel_line_corrections_{L}.json`. '
  'The `*-ptrs.txt` files of the character archives contain absolute offsets: if a table grows they must be recomputed (`remap_pointers`), otherwise the duel crashes.')
w('')
w(f'Comparison with highlighted words: `{rel}/duel_lines_diff.md`.')
w('')
tab(['original', 'new', 'entries', 'archive examples'], rd('duel_lines.csv'))

# ---------------- A5 strings
w('## A5. Long and short interface strings')
w('')
w(f'Tables `strTbl*`, `help_strtbl_*`, `ddstrtbl_*`, `field_strtbl*` (format `(n, 12, 12+4n)` + offsets + UTF-16) in {summary["strings_archives"]} archives (the same table is copied into several archives, e.g. `field/always_*_{"ita" if L == "it" else "fra"}.ehp` x6). '
  f'**{summary["strings_unique"]} unique strings changed**. Rules: `tools/corrections/string_rules_{L}.py` — **{len(RS.STRINGS)} `STRINGS` entries** (archive, member, 0-based index, [(old, new)], reason), '
  f'**{len(RS.GLOBALS)} `GLOBALS`** (regex/callable, applied after the STRINGS) on **{len(RS.TABLES)} tables** (`TABLES`); plus {len(tui)} targeted corrections in `tools/data/ui_texts.json` (in-place writes, text shorter than or equal to the original).')
w('')
c = collections.Counter((r[0], r[4].count(';') + 1) for r in rd('ui_strings.csv'))
cnt = collections.Counter(r[0] for r in rd('ui_strings.csv'))
w('### By member (unique strings changed)')
tab(['member', 'strings'], [[k, v] for k, v in cnt.most_common()])
w('### Global rules (all)')
tab(['pattern', 'replacement', 'reason'], [[g[0], g[1] if isinstance(g[1], str) else '(function) ' + getattr(g[1], '__name__', ''), g[2] if len(g) > 2 else ''] for g in RS.GLOBALS])
w('### STRINGS entries (all): where and why')
tab(['archive', 'member', 'index', 'changes', 'reason'], [[s[0], s[1], s[2], f'{len(s[3])} replacement(s)', s[4] if len(s) > 4 else ''] for s in RS.STRINGS])
w('### Targeted corrections `ui_texts.json`')
tab(['file', 'member', 'index', 'old', 'new', 'reason'], [[t['file'], t['member'], t['index'], t['old'], t['new'], t.get('reason', '')] for t in tui])
w(f'### Complete list\n**Complete comparison with highlighted words: `{rel}/ui_strings_diff.md`.** Raw data: `{rel}/ui_strings.csv`. First 40:')
w('')
tab(['member', 'index', 'original', 'new'], [r[:4] for r in rd('ui_strings.csv')], 40)

# ---------------- A6/A7/A8
w('## A6. [SPELL CARD] / [TRAP CARD] label of the large card in the duel')
w('')
w('In all the `duel/basic_<region><language>.ehp` the label was in English (hash `c2268340`): `apply_to_iso.py` replaces it with `card_spell_trap.gim` of `field/always_<language>_<language>.ehp` (hash `9622cd75`).')
w('')
tab(['archive', 'member', 'original hash', 'new hash'], rd('iso_images.csv'))
w('## A7. ISO files touched and technical details')
w('')
w(f'{summary["file_touched"]} `.ehp` archives differ from the original (all languages together, because the ISO is a single one; list in `{rel}/touched_files.csv`). The other files (video, audio, `EBOOT.BIN` executable, `PARAM.SFO`) are identical. '
  'Non-textual technical differences: `*-ptrs.txt` (absolute member offsets, recomputed when a table changes length), new position of the archives at the end of the ISO.')
w('')
w('## A8. What can NOT be changed (game limits)')
w('')
w('- The **speaker name** in the dialogue box (e.g. "Preside Sheppard"/"Cancelliere" in Italian, "Doyen Sheppard" in French, "Rector Sheppard" in Spanish) lives in the encrypted EBOOT: it cannot be modified.')
w('- Texts drawn by the game with its own font (dialogues, names, descriptions in the deck, drop-down menus, system keyboard, language selection screen) cannot be replaced by the texture pack: they can only be changed in the ISO.')
w('- The 438 map/background textures are not replaced (the game changes their palette): a limit of MikeyMK\'s pack, not of our work.')
w('')
w('---')
w('')
w('# B. TEXTURE PACK')
w('')
w('## B1. Origin and structure')
w('')
w('Base: **Yu-Gi-Oh! GX Tag Force 1 HD Remastered** by **MikeyMK** (US pack `ULUS10136`) and HD cards by **chrisfand**, adapted to the European ISO `ULES00600`. The project does not redistribute the third-party pack: the patcher gets it from the user. '
  'Our work: (1) remap the US pack\'s **hashes** to the EU ones (`tools/gen_ini.py`), (2) redo the cards and interface lettering in the language, (3) correct the texts, (4) `upscale_extra` for the textures that are not covered.')
w('')
w('PPSSPP recognizes a texture by the **hash of its pixels** (xxhash of the data, `gim.data_hash`); every line of `textures.ini` is `0000000000000000<hash8> = path/png`. The PNGs are **4x** the original and redraw exactly the same area. '
  'Textures that are identical between languages have the same hash: the replacement holds for all of them (see `docs/TEXTURE_INVENTORY.md`).')
w('')
w(f'### Real structure (from `{rel}/pack_structure.csv`)')
tab(['root', 'folder', 'files', 'MB', 'content'], rd('pack_structure.csv'))
if L == 'it':
    w('The **base pack `PSP/TEXTURES/ULES00600` is already Italian**: it contains `cards/small_it`, `large_it`, `tiny_it`, `ui_it` (Italian interface) and the Italian title tiles; the other languages are separate modules in `PSP/TEXTURES/modules/<l>`.')
else:
    w('Every language except Italian is a **module** (`PSP/TEXTURES/modules/' + L + '`) to compose over the base pack with `tools/compose_pack.py BASE MODULES CARD_DIR OUT ' + L + ' [--copy]`: it copies the base and **only** the `cards`, `intro` and `ui_' + L + '` folders of the module (hard link or copy), then `module_ini.py` rewrites the `textures.ini`: the localized card lines point to `cards/small_' + L + '`/`large_' + L + '` and the lines of `' + L + '.ini` **replace** those of the base with the same key (hash).')
w('')
w('### Base pack folders (the same for all languages)')
tab(['folder', 'content'], [
    ['`cards/small`, `cards/large`', 'original HD small/large cards by chrisfand (2,833 cards) with English texts; the language picks `small_<l>`/`large_<l>` via the ini'],
    ['`cards/frame`', 'frames, attribute/race tables, Spell/Trap labels'],
    ['`cards/tinyEN/JP/MikeyMK/tiny_<l>`', 'deck thumbnail atlas (7 pages; same hash in all languages: only one atlas wins per installation)'],
    ['`characters`', 'HD portraits, sprites and 3D of the characters (MikeyMK)'],
    ['`events`', 'event images (17)'],
    ['`intro`', 'logo, title movie, new game; `title_screen` contains the tiles with the "Mystic Tomato Version" plate'],
    ['`map`', 'map backgrounds'],
    ['`shop`', 'shop, packs, rooms'],
    ['`ui`', 'MikeyMK\'s English HD interface (for all languages with the same hashes)'],
    ['`upscale_extra`', 'textures not covered by the pack, enlarged 4x with xBRZ (1,192 files, ~56 MB; at 4x/Auto resolution PPSSPP\'s 4xBRZ shader is off): includes the `card_icon03` variants of en/fr/de/es'],
    ['`_CHOOSE YOUR CARD STYLE`', '3 alternative `textures.ini` (mikeymk, official_english, official_japanese): copy one in place of `textures.ini` to change the card style']])

# ---------------- B2 cards
w('## B2. Card images')
w('')
cc = rp['folders_cards']
w(f'Language folders: {", ".join(f"`{k}` ({v} files)" for k, v in cc.items())}. Every card has an **HD small** one (name + description + type, regenerated with free OFL fonts: XCharter Bold for names/type/labels, Libre Baskerville for effects, Newsreader Italic for Normals, PT Serif Caption for Spells/Traps, Charis SIL for the missing glyphs) and an **HD large** one (name only on the frame). '
  'In addition: the **attribute table** with the words of the language (`cards/frame/icons_attribute_race_<l>.png`, `attributes.py`), the **Spell/Trap label** (`icons_spell_trap_<l>.png`, `label_it.py` / `extract_labels.py` -> `data/label_eu_<code>_128x32.png`) and the deck **thumbnail atlas** (`tiny_<l>`, `tiny_atlas.py` + `tiny_fragment.py`).')
w('')
w(f'When the text of a card changes (section A2) its images must be regenerated: **{rp["cards_corrected"]} cards** in {LANG}. List in `{rel}/card_images.csv`. ' + (
    'Command: `sh tools/rebuild_corrections.sh USRDIR PACK_US PACK_MOD PYTHON` (small + large cards); on Windows `python -I` does not see the user packages: pass a wrapper that drops `-I`.' if L == 'it' else
    'Command: `python tools/generate_language.py fr PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` (without IDs it regenerates all of them: 2,833 + 2,833, ~930 MB).'))
w('')
w('Typography: ' + ('Italian typographic apostrophe and quotation marks; `Tipo`, `Terreno`, `Evocazione tramite Tributo` as in the game.' if L == 'it' else 'non-breaking space before `: ; ! ?` and « » quotation marks.'))
w('')

# ---------------- B3 ui
w(f'## B3. HD interface in {LANG} (`ui_{L}`)')
w('')
w(f'**{rp["texture_ui"]} textures** (`{rel}/ui_textures.csv`: file, PPSSPP hash, family, script, original/HD size, neutral/specific, origin in the ISO). By family: ' + ', '.join(f'{k} {v}' for k, v in rp['per_family'].items()) + '. '
  f'Of these {rp["neutral"]} are neutral (same hash in all languages) and {rp["specific"]} specific. '
  'Every family has a script in `tools/ui_textures/<family>.py` (reads `TF1_LANG`): it redraws the lettering texture by texture starting from the low-resolution original of the ISO and from the style of the English pack; same area and same positions (the game crops from fixed rectangles); one font/weight/baseline/shadow per lettering; free fonts (`alt_font.py`).')
w('')
FAM_EN = {
    'menu_lists': "`result_e__menu01` (WIN/DRAW/LOSE and icons), `title_menu_e__m_menu_title01` (MAIN MENU · ENTER NAME · DOWNLOADED CARD LIST · DUEL PUZZLE · OPTIONS · LANGUAGE SETTINGS)",
    'icon_sheets': "`icon04` (European pixels on the US sheet), `panel` (`ased` fragment of the tab), `pda_pack01` (NEW column)",
    'deck_screens': "tabs Trunk, Rental, Lab, Converter; `Card types in possession`; `Purchased Cards` / `Card Types Purche`; gold bar; ENTER key",
    'recipe_screens': "Character, User, Downloaded Recipes, Character Recipes, User Recipes, Limited, Semi-Limited, Forbidden, Trade",
    'vs_screen': "`2nd round`, `3rd round`, badge sheet `1st PLAYER` / `2nd PLAYER` / `PLAYER`",
    'result_letters': "`D R A W` tiles of the results screen (`result_e`) and of the banner (`basic_be`): same hash, 4 files",
  'tutorial': "dialogue `Your opponent has declared battle. Activate the effect of a card?` (YES/NO) and 5 example cards with the game's text",
}
FAM = {
    'duel_texts': ('duel/basic_<l><l>.ehp', {'it': 'Catena · TURNO (blue/red) · TOCCA AL GIOCATORE SUCCESSIVO (split over 2 textures) · INIZIA IL DUELLO · Attacco Diretto! · number sheet `card_icon03` (see B4)', 'fr': 'Chaîne · TOUR (blue/red) · TOUR DU JOUEUR SUIVANT (cut after SUIV) · DÉMARRER DUEL (cut after DU) · Attaque Directe! · `card_icon03` is in the `upscale_extra` folder (B4)', 'es': 'Cadena · TURNO DEL SIGUIENTE JUGADOR (the cut between the two textures passes inside a letter, as in the original) · COMENZAR DUELO · Ataque Directo · TURNO and `card_icon03` covered by already existing textures (same hash as Italian / `upscale_extra`)', 'de': 'Ketten · SPIELZUG (blue/red) · NÄCHSTER SPIELER (on 2 textures, the cut passes inside the L; the dots of the Ä are a separate sprite, enlarged and centred over the A) · DUELL BEGINNEN · Direkter Angriff! · `card_icon03` is in the `upscale_extra` folder (B4)'}),
    'result_letters': ('duel/basic_<l><l>.ehp', {'it': 'HAI VINTO · HAI PERSO · PAREGGIO: one 64x64 tile per letter (repeated letters reuse the same tile) + silhouette', 'fr': 'TU AS GAGNÉ · TU AS PERDU · EGALITE (without accent: the draw has no É tile)', 'es': 'HAS GANADO (HASGNDO) · HAS PERDIDO (HASPERDIO, 9 tiles) · EMPATE (EMPAT) + silhouette', 'de': 'DU GEWINNST (DUGEWINST, 9 tiles) · DU VERLIERST (DUVERLIST, 9 tiles) · UNENTSCHIEDEN (UNETSCHID, 9 tiles; E and N repeated) + silhouette of DU GEWINNST'}),
    'menu_lists': ('title_menu/title_menu_<l>.ehp, duel/result/result_<l>.ehp, field/always_bri_<code>.ehp', {'it': 'menu titles (`m_menu_title01`, `trnsmt02`, `menu02`, `press_start0003`), result labels, calendar (days, months, "days to the tournament", Morning/Evening)', 'fr': 'MENU PRINCIPAL · SAISIR NOM · LISTE CARTES TÉLÉCHARGÉE · PUZZLE DUEL · OPTIONS · SÉLECTION DE LA LANGUE · LISTE DE GROUPE... · RÉSULTAT DU DUEL · APPUYEZ SUR LA TOUCHE START · GAGNÉ/ÉGALITÉ/PERDU · Dimanche...Samedi · Mai Juillet Juin Août · jours / avant le tournoi · Matin / Soir', 'es': 'MENÚ PRINCIPAL · INTRODUCE EL NOMBRE · LISTA DE CARTAS DESCARGADAS · DUELO ACERTIJO · OPCIONES · AJUSTES DEL IDIOMA · AGRUPAR LISTA... · RESULTADO DEL DUELO · PRESIONA EL BOTÓN START · GANAS/EMPATE/PIERDES · Domingo...Sábado · Mayo Julio Junio Agosto · Días / para el torneo / de · AM / PM'}),
    'icon_sheets': ('deck/all_<l>.ehp, shop/all_<l>.ehp, field/always_*', {'it': 'icon sheets: `icon04` (Mia/L and badges), `s_pack` (ESAURITE), `panel` (tab fragment), `icon06` (N), `pda_pack01` (NUOVO), `mein_menu00`, `trnsmt01`, `ocglist`', 'fr': '`icon04`, `s_pack` (ÉPUISÉ), `panel` (fragment "hetés"); `pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01` keep "NEW" as in the original French', 'es': '`icon04`, `s_pack` (AGOTADO), `panel` (fragment "rados"); `pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01` have the same hash as English'}),
    'deck_screens': ('deck/all_<l>.ehp, labo/*.ehp, shop/all_<l>.ehp', {'it': 'tabs Cassa, **Fusion**, Side, Deck, Affitto, Laboratorio, Convertitore, "Tipi di Carte Posseduti", "Carte Comprate", INVIO key', 'fr': 'Coffre ×2, Location ×3, Labo, Convertisseur, "Types de cartes acquis", "Cartes achetées" (+ fragment), ENTRÉE', 'es': 'Tronco ×3, Fusión, Alquiler ×4, Laboratorio, Conversor ×2, "Tipos de carta en posesión", "Cartas compradas" (+ fragment), ACEPTAR'}),
    'recipe_screens': ('deck/recipe_view_<l>.ehp, title_menu/title_menu_<l>.ehp, database/limitlist.ehp', {'it': 'tabs Personaggio / Utente / Scaricata / Limitata / Semi-limitata / Vietata / Scambio and recipe panels', 'fr': 'Personnage / Utilisateur / Téléchargée / Limitée / Semi-limitée / Interdite / Échange (in the original game "Scambia" was an Italian leftover)', 'es': 'Personaje / Usuario / Recetas descargadas / Recetas de personaje / Recetas de usuario / Limitada / Semi-Limitada / Prohibida / Cambiar'}),
    'vs_screen': ('duel/start/start_e.ehp (members _<l>), start_all.ehp, start_<l>.ehp', {'it': 'banners DUEL / NORMAL / TAG, glows, "Modalità ...", "n A GIOCARE", "n Duello", rock-paper-scissors sheet (VITTORIA/SCONFITTA/PAREGGIO), player sheet ("n° GIOCATORE")', 'fr': 'DUEL / NORMAL / TAG · DEUXIÈME À JOUER / PREMIER À JOUER · 1er/2e/3e round · Mode Un Duel / Mode Match · GAGNÉ/PERDU/EGALITE · 1er JOUEUR / 2e JOUEUR · JOUEUR', 'es': 'DUELO / NORMAL / TAG · SEGUNDO EN SALIR / PRIMERO EN SALIR · 1ra/2da/3ra vuelta · Modo Individual / Modo Combate · GANAS/PIERDES/EMPATE · JUGADOR 1 / JUGADOR 2 · JUGADOR'}),
    'tutorial': ('tutorial/tutorial_<l>.ehp (tuto_duelimg01..06)', {'it': 'illustration of the activation dialogue (texts, YES/NO buttons, small card) + 5 maps with the type disc', 'fr': '"Ton adversaire a déclaré le duel." / "Activer l\'effet de la carte ?" · OUI/NON · 5 maps; different geometry (2-line dialogue)', 'es': 'Tu oponente ha declarado la batalla. / ¿activar el efecto de la carta? · SÍ/NO · 5 maps; 2-line dialogue but wider box'})}
SCRIPT_OF = {'duel_texts': 'duel_texts', 'result_letters': 'result_letters', 'menu_lists': 'menu_lists', 'icon_sheets': 'icon_sheets',
             'deck_screens': 'deck_screens', 'recipe_screens': 'recipe_screens', 'vs_screen': 'vs_screen', 'tutorial': 'tutorial'}   # pack family -> script
rows = []
for f, n in rp['per_family'].items():
    a, t = FAM.get(f, ('?', {}))
    rows.append([f, n, f'`tools/ui_textures/{SCRIPT_OF.get(f, f)}.py`', a.replace('<l>', {'it': 'i', 'fr': 'f', 'es': 's', 'de': 'g', 'en': 'e'}[L]), t.get(L, FAM_EN.get(f, '') if L == 'en' else '')])
tab(['family', 'textures', 'script', 'source ISO archive', 'language texts'], rows)
w('Quality rules (valid for every language): regular letters, never deformed one by one; same area as the original; no blur; the text is that of the language\'s original (only obvious errors are corrected: leftovers from other languages, accents); pixel art is **not** smoothed without confirmation; geometries always measured on the original.')
w('')
w('### Drawn texts: original -> HD')
w("Table read by eye, texture by texture: `docs/changes_" + L + "/texture_texts_" + L + ".md`." + (" Differences from the original: `TAUSCHEN`/`Tauschen` -> `SCAMBIO`/`Scambio`, `Fusione` -> `Fusion`; everything else rewrites the same words." if L == 'it' else " No word changed: the HD rewrites the same words as the English original (except `DOWNLOADED CARD LIST`, which the US pack has as `DOWNLOAD`)." if L == 'en' else " Differences from the original: `DEMARRER` -> `DÉMARRER`, `SCAMBIA`/`Scambia` -> `ÉCHANGE`/`Échange`, `2è/3è round` -> `2e/3e round`; everything else rewrites the same words."))
w('')
w('### List of every texture')
w(f'(all {rp["texture_ui"]} rows, from `ui_textures.csv`)')
w('')
tab(['file in the pack', 'hash', 'family', 'original px', 'HD px', 'type', 'ISO origin'], [[r[0], r[1], r[2], r[4], r[5], r[6], r[8]] for r in rd('ui_textures.csv')])
if L == 'it':
    w('### Italian textures without a counterpart in `ui_fr` (19) and why')
    w('13 are neutral (same hash in all languages: recipe panels, Side/Deck/Fusion Deck tabs, bars, `card_side`...). 6 have local wording in the original (`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `d_window00016`, `duelrecord parts`): Italian has NUOVO / N / Fusion, the original French has NEW / Fusion and already has its HD ones in `upscale_extra`. The deck editor tab says **Fusion** (not "Fusione"): "Fusion Deck" is called that in all languages.')
elif L == 'en':
    w("### English textures that stay as they were")
    w("The English textures already covered by the US pack (same hash: 621) come from MikeyMK and are not touched. The textures without text or common to all languages stay **enlarged with xBRZ** (`upscale_extra`) or without a file (14, fragments without text: they look like the original) (the 4 DRAW tiles of the results screen are redrawn in `result_letters`). 17 textures of the Italian pack have the same hash as the English ones (`ITA-ON-ENG`): checked one by one, they have no text. Complete list: `docs/changes_en/texture_inventory_en.txt`.")
else:
    w('### Textures that stay like the original')
    w('`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `parts` are pixel-art icon sheets (with NEU/NEW): they stay as they were, covered by the `upscale_extra` enlargement as in the other languages; the text was not changed. The neutral textures come from the base pack. In Spanish `score-top` (TURNO) also has the same hash as Italian and `card_icon03` is in `upscale_extra`.')
w('')

# ---------------- B4
w('## B4. The duel number sheet (`card_icon03`)')
w('')
w('A single sheet with LP digits, time, keys and multipliers; different hash per language. Recipe chosen by the user (`tools/ui_textures/icon03_languages.py`, rerun with `--apply`):')
w('- rows 0-180 (small digits and signs, orange keys 1/2/3, big digits 0-9 with "LP", small digits 0-9): **from the US pack**, crisp pixel art;')
w('- cells in which the European game differs from the US pack (black check mark, grey ball, empty pill, time word): **original pixels enlarged 4x without smoothing**; time word ' + {'it': '**TEMPO**', 'fr': '**TEMPS**', 'de': '**ZEIT**', 'es': '**TIEMPO**', 'en': '**TIME**'}[L] + '; the orange pill ("Single" in the US pack) stays **empty**;')
w('- rows >= 181 (multipliers x1..x12, icons, cards, arrows): from the Italian sheet already in the pack (`tools/data/card_icon03_base_it.png`);')
w('- the European cells are pasted **only in their band** of rows (otherwise they spoil the top of the big digits).')
w('')
w('Files: it -> `ui_it/duel_texts/basic_ii__card_icon03.png` (hash 376925c7); fr -> `upscale_extra/3e5482fd.png`; en ee0c44c3; de ffe309a6; es 859eea2b. Previews in `comparisons/icon03/`.')
w('')
# ---------------- B5
w('## B5. Title plate')
w('')
w(f'`python tools/ui_textures/mystic_tomato_title.py {L}` generates 2 PNGs (`542eff79685c434d`, `705176739829dcf5`, tiles 18 and 19 of the 20-tile 128x64 backdrop `title_menu_i.ehp: main_title00001..00020`) with card 4930 in the language + the "version" wording + the flag, PT Sans Bold font: '
  + '**"' + {'it': 'VERSIONE POMODORO MISTICO', 'fr': 'VERSION TOMATE MYSTIQUE', 'de': 'EDITION MYSTISCHE TOMATE', 'es': 'EDICIÓN TOMATE MÍSTICO', 'en': 'VERSION MYSTIC TOMATO'}[L] + '"**' + '. The plate **is included only for the chosen language** (it lives in `modules/' + L + '/intro/title_screen/`); the original base pack has the tiles without a banner. Files in this pack: ' + ', '.join(f'`{b}`' for b in rp['banner'] if 'title_screen' in b and ('542eff' in b or '705176' in b)) + '.')
w('')
# ---------------- B6
w('## B6. `textures.ini` and composition')
w('')
w('`tools/gen_ini.py TOOLS US_INI CARD_DIR OUT_INI i=it +extra_it.ini +ui_it.ini +data/upscale_extra.ini` converts the US `textures.ini` into the EU one: the non-card entries stay (neutral textures = same hashes); the card entries are regenerated from the EU `card/*.cip` archives for the 5 languages (`i=it` remaps `cards/large/X.png` -> `cards/large_it/X.png`); it adds the Spell/Trap label (`extra_it.ini`), the `ui_it` lines and `upscale_extra.ini`. It is also done for the 3 card styles. '
  'If the same pixels exist in several languages the first in `e i f g s` wins (for this reason atlas, banner and attribute table are "one per installation").')
w('')
w(f'`ui_{L}` lines in `{"textures.ini" if L == "it" else L + ".ini"}`: {rp["rows_ini_ui"]}. Prefix frequency: `{rel}/ini_lines.csv`. Check: every `ui_{L}/...` line must point to an existing file and there must be no duplicate hashes.')
w('')
w('## B7. Installation and settings')
w('')
w('PC: copy `ULES00600` into `<PPSSPP>/PSP/TEXTURES/` (Android: `textures.zip` in `.../TEXTURES/ULES00600/`, without extracting it; regenerate the zip with the corrections). Settings: **Replace textures ON**, rendering resolution **4x**, game language = module language (the language is stored in the **save file**). After changing a single PNG it is enough to copy it and restart PPSSPP (cache). To try the texts use the `_definitiva` ISO.')
w('')
w('---')
w('')
w('# C. EDITORIAL CHOICES')
w('')
if L == 'it':
    w('- **Preside** (never "Cancelliere") for Sheppard, including "Ufficio del Preside" and "Profilo del Preside Sheppard".')
    w('- **Segna-Mostro** (not "Gettoni Mostro") in help, records and cards; `Segna-Opzione`.')
    w('- Banner: "direttore dello Slifer Rosso"; dormitories **Slifer Rosso, Ra Giallo, Obelisk Blu**; `Modalità Storia` is the menu name.')
    w('- Tab **Fusion** (not Fusione). `E\'` -> `È`; `Life Point` -> `Life Points`; punctuation and apostrophes corrected.')
    w('- Censored scenes restored to the Japanese: sake/shochu and maid outfit (see below); "Beh, non sono poi così bravo..." (it was "sto sbavando").')
else:
    if L == 'fr':
        w('- **Doyen / Chancelier**: dialogue by dialogue, formal -> "Chancelier", informal -> "Doyen"; in the UI cards "Chancelier Sheppard".')
        w('- French punctuation `! ? : ;` with a space (also after `》`); "Mode histoire" -> "Mode aventure" (real name of the menu).')
        w('- `Échange` instead of "Scambia" (Italian leftover); "2e/3e round"; "EGALITE" without accent; "DÉMARRER DUEL".')
        w('- `Piège Continu` is the term consistent across the whole game: it is not changed.')
    elif L == 'en':
        w("- **Only objective errors** of European English: typos (`Sryus`, `Principle's`, `Bandanna`), articles (`a Equip Spell` -> `an Equip Spell`, `face-down card` -> `a face-down card`), apostrophes (`monsters's`, `opponents cards`), agreement, verb forms in the tutorials (`\"Summon\" it` -> `\"Summoning\" it`), extra spaces and `$` in the color codes. No stylistic rewriting.")
        w("- `Chancellor Sheppard` in the cards, as in the dialogues; `Bandana` as in the dialogues.")
        w("- Card terms and texts left as in the game; the 82 corrected cards have their text regenerated in the HD images (`modules/en/cards`).")
        w("- The English title plate is `VERSION MYSTIC TOMATO` (confirmed by the user on 2026-10-13).")
    else:
        w('- **Rector Sheppard** (as in the dialogues) in the cards and maps ("Oficina del Rector"); dormitories **Slifer Rojo, Ra Amarillo, Obelisco Azul**; **Jinetes de la Sombra**; "Habitación" instead of "Alójese" (Room).')
        w('- Sake/shochu and maid outfit as in the other languages (`st01_t01/Scr003E`), `st02_t01/Scr101E` rotated; "Sirviente de la Calavera", "Toon", "Archidemonio", "Trío Ojama" and name accents as on the cards.')
        w('- Options: "EN/FUERADE" -> "ON/OFF"; title messages ("nuevos datos de juego"), tutorial lessons ("le turno" -> "es el turno de", swapped x/o keys, closed color codes), final paragraph of the Tag Duels translated (it was truncated/in English).')
        w('- Terms left as in the game: "Invocación por Sacrificio", "Tributar", "Efecto de Blanco", "Tronco" (open questions in `docs/changes_es/open_questions_es.md`).')
w('- Number sheet: digits/LP from the US pack, x1..x12 from the Italian sheet, time word ' + {'it': 'TEMPO', 'fr': 'TEMPS', 'de': 'ZEIT', 'es': 'TIEMPO', 'en': 'TIME'}[L] + '.')
w('')
w('### Entries of the choices register for this language (`tools/data/editorial_choices.json`)')
tab(['id', 'original', 'corrected', 'inherited', 'reason'], [[v['id'], v['original'], v['corrected'], 'yes' if v['inherited'] else 'no', v['reason']] for v in reg])
w('Other choices and the re-reading of the duel sentences: `docs/EDITORIAL_CHOICES.md`.')
w('')
w('# D. IN-GAME VERIFICATION')
w('')
if L == 'it':
    w('- Seen in game: Italian HD interface, rewritten long strings (help, cards, tutorial), Preside/Segna-Mostro terminology, HD cards and Spell/Trap label of the large card.')
    w('- **Not seen** after the latest changes: card re-reading (65 new cards), corrected duel sentences, "Fusion" tab, 4 dialogue box-length warnings (en/es/de #147/#151, de #172).')
else:
    if L == 'de':
        w('- **Seen in game** (`_definitiva` ISO + `de` module, new game in German, 2026-10-12): language selection, title with the "MYSTISCHE TOMATE EDITION" plate and Neues Spiel/Fortfahren, "Daten geladen", HD Hauptmenue, Deck menu (Deck bearbeiten / Rezeptanzeige), deck editor (tabs Deck/Fusion/Side/Truhe, "Persoenliches Deck", "Eigene Kartentypen", Hilfe), Rezeptanzeige (Benutzer/Charakter, Fusionsdeck), confirmation "Deckbearbeitung verlassen", calendar ("1. Mai / Montag", "92 Tage bis zum Turnier"), map ("Duellakademie", list of places), office menu (Reden/Duell/Gegenstaende/PDA), dialogues of the chancellor and of Crowler in Klassenzimmer with the corrections (Buero des Kanzlers, Duellakademie, Haupttor...), 2-3-line boxes without cuts.')
        w('- **Not seen** (only read and compared with the original in the comparison sheets): Kette, Direktangriff, end of duel, rock-paper-scissors, ZWEITER/ERSTER, 1. Runde, tutorial and lessons, shop (AUSVERKAUFT, "Gekaufte Karten"), laboratory (Labor, Konverter, Miete), PDA, album, Optionen, cards with new text, duel sentences, VS screen.')
        w('- **Seen in the title demo duel** (2026-10-12): VS screen ("NORMALES DUELL", "Einzelmodus", "Gegen", badges), duel HUD, duelist sentences in German, card descriptions in German; "Draw Phase" stays English as in the original. Defects reported by the user: dialogue font not HD (system text, cannot be replaced with textures) and PSP save menu in French (PPSSPP system language).')
    elif L == 'fr':
        w('- Seen in game (`_definitiva` ISO): title with plate, menus, deck editor.')
    elif L == 'en':
        w("- **Not seen in game**: the `_definitiva` ISO and the composed English pack have not been tried in PPSSPP yet. Checked only on the data: `apply_to_iso.py` with 0 warnings, every `ui_en` line of `textures.ini` points to an existing file, original/HD comparisons in `docs/changes_en/sheets/` (original 4x next to the HD, re-read by eye).")
        w("- To see in game: card with new text, corrected dialogues, editor help, tabs Trunk/Rental/Lab/Converter, `Purchased Cards`, `2nd/3rd round`, `1st/2nd PLAYER` badges, `MAIN MENU` and menu entries, duel tutorial.")
    else:
        w('- **Seen in game** (`_definitiva` ISO + `es` module, new game in Spanish, 2026-10-12): language selection, title with the "EDICIÓN TOMATE MÍSTICO" plate and "PRESIONA EL BOTÓN START", Juego Nuevo/Continuar, "INTRODUCE EL NOMBRE", save system messages, HD Menú Principal, Lista de Duelistas, deck editor (tabs Deck/Fusión/Side/Tronco, "Tipos de carta en posesión"), Opciones (ON/OFF, help).')
        w('- **Not seen** (only read and compared with the original in the comparison sheets): duel (Cadena, Ataque Directo, end of duel, VS, rock-paper-scissors), tutorial and lessons, shop, laboratory, calendar, cards with new text, corrected story dialogues, duel sentences.')
w('')
w('# E. HOW TO REGENERATE EVERYTHING')
w('')
w('```')
w('# ISO (all languages together)')
w('python tools/corrections/build_dialogues.py ' + L)
w('python tools/corrections/generate_card_corrections.py ' + L + ' CARDINFO_' + L + '.ehp          # cards')
w('python tools/corrections/apply_to_iso.py PSP/GAME/ULES00600_..._EUR.iso PSP/GAME/ULES00600_..._EUR_definitiva.iso')
w('# images')
w(('sh tools/rebuild_corrections.sh USRDIR PACK_US PACK_MOD PYTHON' if L == 'it' else 'python tools/generate_language.py fr PACK CARDINFO US_INI CLEAN_DIR OUT [ID...]') + '')
w('TF1_LANG=' + L + ' python tools/ui_textures/<family>.py USRDIR PACK_US <module>      # for each of the 8 families (whole!)')
w('python tools/ui_textures/icon03_languages.py --apply ; python tools/ui_textures/mystic_tomato_title.py ' + L)
w('python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules USRDIR/card OUT ' + L + ' --copy')
w('# this document')
w('python tools/analysis/document_changes.py ISO_ORIG ISO_DEF ' + L + ' docs/changes_' + L)
w('python tools/analysis/document_pack.py ISO_ORIG ' + L + ' docs/changes_' + L)
w('python tools/analysis/text_comparisons.py ' + L)
w('python tools/analysis/write_changes_document.py ' + L)
w('```')
w('External inputs you need (check that they exist): the original ISO, the extracted USRDIR (`tools/analysis/extract_usrdir.py`), MikeyMK\'s US pack `ULUS10136` (in a folder outside the project).')
w('')
w('# F. LIMITS AND OPEN POINTS')
w('')
if L == 'it':
    w('- Official card names: to be decided with the user. "Ragazza Mago Nero" vs "Maga Nera".')
    w('- The hand-written notes on the card re-reading before ~line 1830 were lost; for that stretch there is also an automatic scan (typos, spaces, apostrophes).')
    w('- Android `textures.zip` to be regenerated with the corrections; cards of the installed pack to be restarted in PPSSPP (cache).')
else:
    if L == 'fr':
        w('- Optional variant `N`/NOUVEAU instead of `NEW` in the 4 textures with local wording.')
        w('- Android `textures.zip` for French: not done; no test on a phone.')
        w('- Long labels to check in game: "Rechercher", "Aucune restriction", "Étiquette".')
    elif L == 'de':
        w("- German textures added on 2026-10-13 (`result_letters` 28, `duel_texts` 15; before they were taken for equal to English, which was a mistake: see `docs/changes_de/texture_texts_de.md`): compared with the low-resolution original (tile overlay, check sheets), **not yet seen in game**. To check: the centring of the dots of the Ä of NÄCHSTER SPIELER (separate sprite), the width of SPIELZUG in the badge and the silhouette of DU GEWINNST.")
        w('- 5 pixel-art icon sheets (`pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `parts`) stay enlarged from the pack (open question no. 7 in `open_questions_de.md`; in `pda_pack01` the game has an Italian leftover "NUOVO" next to the "NEU", as in fr/es).')
        w('- Android `textures.zip` for German: not done; no test on a phone.')
    elif L == 'en':
        w("- **User decisions (2026-10-13)**: logo name `VERSION MYSTIC TOMATO` confirmed; DRAW tiles to be redrawn (done); (1) logo name confirmed; (2) `DOWNLOADED CARD LIST` (European) versus `DOWNLOAD` (US text): the European one was chosen, confirmed by the user.")
        w("- Android `textures.zip` for English: not done; no test on a phone.")
        w("- The texts drawn in the textures are in `docs/changes_en/texture_texts_en.md` (read by eye).")
    else:
        w('- User questions resolved on 2026-10-12 (broken card names corrected to the official name, Kaiba Corporation, capitalized Duelo, Rector, Sacrificio instead of Tributo): `docs/changes_es/open_questions_es.md`.')
        w('- 14 Spanish textures without HD (fragments without text: `recipe_sel`, `t_window0002`, `limitlist window_s0010/20`, `jyanken100005/7`, `recipe010011`, `bg_base_cloud02`) stay like the original.')
        w('- Android `textures.zip`: not done; no test on a phone. The texts drawn in the textures are in `docs/changes_es/texture_texts_es.md` (read by eye).')
w('- The speaker name in the dialogue box cannot be modified (encrypted EBOOT).')
open(os.path.join(B, 'docs', f'CHANGES_{L.upper()}.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(o) + '\n')
print(len(o), 'lines ->', f'docs/CHANGES_{L.upper()}.md')
