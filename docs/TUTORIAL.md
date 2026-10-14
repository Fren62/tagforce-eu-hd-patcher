# TUTORIAL - Technical handbook for bringing the "Mystic Tomato Version" to a language

Technical companion of `docs/NEW_LANGUAGE_GUIDE.md` (read that one first: general guidelines valid for any language) and of the complete models
`docs/CHANGES_IT.md` / `docs/CHANGES_FR.md`. This handbook explains how the pipeline works, how to run every script and which traps cost time already.
Per-language status and the editorial decisions live in `docs/EDITORIAL_CHOICES.md` and in the generated `docs/CHANGES_<LANG>.md`.

Index
1. What the project is and the fixed rules
2. How it works technically (hashes, modules, ISO)
3. Preparing the environment
4. Phase 1 - Card texts and card modules
5. Phase 2 - Title plate
6. Phase 3 - HD interface: method and recipe family by family
7. Phase 4 - Texts inside the ISO
8. Phase 5 - Composing the pack and installing it
9. Phase 6 - In-game test
10. Traps and mistakes already made
11. Definition of "done"
12. Appendix: files and scripts, interface string tables

---

## 1. What the project is and the fixed rules

**Goal.** A free, open-source patcher (Windows + Linux) that, from the European ISO of *Yu-Gi-Oh! GX Tag Force* (ULES00600 v1.01, the only EU version), produces the game with: corrected card texts, re-adapted and retranslated dialogues/duel lines/interface texts, cards and interface in HD, for it, fr, de, es (and corrections to English). It works with standard PPSSPP, also on Android. The mod is called **"Mystic Tomato Version"** (the Mystic Tomato is card 4930; the title shows a plate with its name in the chosen language).
The graphic base is the *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* pack by **MikeyMK** (US, ULUS10136) and the HD cards by chrisfand, adapted to the EU version. Our work: map everything onto the EU hashes, redo the texts in the languages, fix the texts.

**Rules decided by the project owner (respect them, do not reopen):**
1. **No Apple fonts.** Only free (OFL) fonts through `tools/alt_font.py` (which replaces every macOS font with a free one). Do not reintroduce `/System/Library/Fonts` paths.
2. **Every check/correction made for Italian extends to all the languages** (fr, de, es, en). Italian is the quality reference.
3. **Never smooth pixel-art textures** (PSP keys, arrows, flags, tabs, rock-paper-scissors hands...) without confirmation: the original pixels are preferred. Only the approved fixes are smoothed (digits x1-x12, Spell Speed table, attribute symbols, LP/TURN digits).
4. **The original ISO is never modified**: `apply_to_iso.py` writes a copy (`ULES00600_..._EUR_definitiva.iso`).
5. **The "Mystic Tomato Version" plate is included only for the chosen language** (it lives in `modules/<language>/intro/title_screen/`; the base pack has the original tiles).
6. **No language must weigh on another**: every language is a module (`PSP/TEXTURES/modules/<language>/`); the user downloads only their own.
7. **The MikeyMK / chrisfand pack is not redistributed**: the patcher gets it from the user. In tests it is used locally only.
8. **Ask before debatable translation choices**; do not "modernize" the terminology: objective errors are fixed and meaning-losing sentences are re-adapted from the original language.
9. Update the documentation **while** you work, not at the end.

---

## 2. How it works technically

### 2.1 PPSSPP texture replacement
PPSSPP recognizes a texture by the **hash of its data** (xxhash of the pixels, plus the CLUT if paletted). In `textures.ini` (section `[hashes]`) every line says which PNG to use:

```
0000000000000000<8-digit data hash> = ui_fr/duel_texts/basic_ff__chain010005.png
```
With address/CLUT at zero PPSSPP recognizes the texture by the data hash alone (verified on all the game textures without collisions; `common.py`). The `tools/gim.py` tool reads the `.gim` files and computes `gim.data_hash(gim.parse(...))`. The replacement PNGs must be exactly **4x** the original texture (e.g. 128x32 -> 512x128) and must redraw **exactly** the same content area: the game composes the words from pieces at fixed positions (a lettering split over two textures, one letter per texture, etc.).

**Fundamental consequence:** if two languages have a texture with the **same pixels** (same hash) the replacement holds for both. So many textures do not need redoing: if French has the same hash as English, MikeyMK's English pack already covers it; if it has the same hash as Italian, the `ui_it` version holds.

### 2.2 Base pack + per-language modules
```
PSP/TEXTURES/ULES00600/            base pack (EU): cards/, characters/, events/, map/, shop/, ui/, ui_it/, upscale_extra/, intro/ ... + textures.ini
PSP/TEXTURES/ULES00600/_CHOOSE YOUR CARD STYLE/{mikeymk,official_english,official_japanese}/textures.ini   3 card styles
PSP/TEXTURES/modules/<language>/    one module per language:
    cards/small_<l>, large_<l>, tiny_<l>, frame/icons_attribute_race_<l>.png, frame/icons_spell_trap_<l>.png
    intro/title_screen/*.png       title plate (only of that language)
    ui_<l>/<family>/*.png          HD interface of the language (+ ui_<l>/<family>.ini)
    <l>.ini                        textures.ini fragment of the module (hash = path lines)
```
`tools/compose_pack.py BASE MODULES CARD_DIR OUT LANGUAGE... [--copy]` copies the base and **only** the `cards`, `intro` and `ui_<l>` folders of the chosen modules (hard link, or copy with `--copy` or on another volume), then `module_ini.py` rewrites the `textures.ini`: the localized card lines point to `cards/small_<l>` / `large_<l>`, and the lines of the `<l>.ini` fragment **replace** the base lines with the same key (hash).
Note: the attribute table, the labels and the thumbnail atlas have the **same hash in all languages**: with several modules installed the first wins (one atlas per installation).

### 2.3 Game archives and language letters
The game data is in `.ehp` archives (readable with `tools/ehp.py`: `ehp.read(path)` -> dict name -> bytes) that contain `.gim` (textures), text tables etc. Every language has a **letter** and a **3-letter code**:

| Language | code | letter (file/hash) | `cardinfo_` | table |
|---|---|---|---|---|
| Italian | it | **i** | `cardinfo_ita.ehp` | I |
| French | fr | **f** | `cardinfo_fra.ehp` | F |
| German | de | **g** | `cardinfo_ger.ehp` | G |
| Spanish | es | **s** | `cardinfo_spa.ehp` | S |
| English | en | **e** | `cardinfo_eng.ehp` | E |

(`tools/languages.py`, `LANGUAGES`). **Beware: German uses the letter `g` and Spanish `s`**, not `d`/`e`. The language is chosen with the environment variable **`TF1_LANG`** (it|fr|de|es|en); alternatively a `cardinfo_xxx.ehp` argument or `TF1_EHP`.

Typical names (example Italian -> French -> German -> Spanish):
- `deck/all_i.ehp` -> `all_f.ehp` -> `all_g.ehp` -> `all_s.ehp`; members `window_i0009.gim` -> `window_f0009.gim` -> `window_g0009.gim` -> `window_s0009.gim`
- `title_menu/title_menu_i.ehp` (and `_f`, `_g`, `_s`), `duel/result/result_<l>.ehp`, `tutorial/tutorial_<l>.ehp`
- `duel/basic_ii.ehp` (it), `basic_ff.ehp` (fr), `basic_gg.ehp`, `basic_ss.ehp`: **the letters are repeated**. The archives `basic_if`, `basic_ff`, `basic_bf` are identical in French (measured): `basic_<l><l>` is used. Verify it with the hash for de/es.
- `duel/start/start_e.ehp` contains the members of **all** languages (`vs_bg01_1_i0007`, `..._f0007`, `..._g0007`, `..._s0007`) and so does `start_all.ehp`; `jnk_card01.gim` is taken from `start_<l>.ehp`.
- `field/always_bri_<ita|fra|ger|spa>.ehp` (calendar `story_sys02.gim`), `database/cardalbum.ehp` (members `icon06_<l>`, `spelltrap_<l>`).
- **The game language comes from the save file**: on the first start the game shows the "Language settings" screen and the choice is written in the save. (The patcher removes this screen when the other languages are removed.)

### 2.4 Where the game draws text and where it does not
- Texts in **textures** (images) -> replaced with the pack (phases 1-3).
- Texts that the **game draws with its own font** (dialogues, character names, card descriptions in the deck, drop-down menus, keyboard) -> cannot be replaced by the texture pack: they are fixed **inside the ISO** (phase 4). The "large" descriptions shown on the HD cards are images instead (phase 1).

---

## 3. Preparing the environment

### 3.1 Software
- Python 3.12 with: `numpy pillow xxhash opencv-python-headless pycdlib pycryptodome requests pyspellchecker`, `bsdiff4` for the patches and, for in-game tests on Windows, `vgamepad` (needs the **ViGEmBus** driver).
- PPSSPP, memory stick in `<PPSSPP data folder>/PSP/` (`SYSTEM/ppsspp.ini`, `TEXTURES/`, `SAVEDATA/`). Settings used: `ReplaceTextures=True`, `InternalResolution=4`, window on the second monitor if you have one.
- **Windows/pip trap:** `pip` and `python` can be different interpreters: install with `python -m pip install ...`. Do not use `python -I` (isolated mode) for scripts that import numpy/cv2 if the packages are in the *user site*: it fails with `No module named ...`. Use `python -P` or nothing.
- **Heredoc trap:** in Git Bash, `\u00xx` and `\\` inside a heredoc sometimes arrive altered. For code with Unicode escapes write the file with an editor/write tool, or use `chr(0xa0)`. Never paste Windows paths with backslashes into normal Python strings without `r''`.
- In Git Bash the paths are `/f/...` and `/c/Users/...`; Python wants `F:/...`.

### 3.2 The three inputs outside the repository (**check at once that they exist**)
1. **European ISO** `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso`.
2. **USRDIR extracted from the ISO** (without `movie/` and `snd/`): needed by all the `ui_textures` scripts. Extract it with `pycdlib`:
   ```
   python tools/analysis/extract_usrdir.py "PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso" USRDIR
   ```
   (656 files, ~340 MB; creates `USRDIR/duel`, `deck`, `shop`, `labo`, `database`, `title_menu`, `tutorial`, `field`, `script`, `duelsys`, `card`...). Several analysis scripts read its path from the `TF1_USRDIR` environment variable.
3. **MikeyMK's US pack** (`ULUS10136`), needed as a *style reference* (and as the source of the menus' HD PNGs). It is not in the project. Download it from the PPSSPP forum post (thread **29487**, Mega link in the first post) with the Python downloader (there is no megatools):
   ```
   python tools/analysis/mega_dl.py "<fileid>#<key>" pack_us.zip      # fileid#key = the part after https://mega.nz/file/
   ```
   then unzip -> folder `ULUS10136`. The zip is called *"Yu-Gi-Oh! GX Tag Force 1 HD Remastered.zip"* (1.4 GB, 7,849 files).

Typical command for an interface generator:
```
TF1_LANG=fr python "<project>/tools/ui_textures/<family>.py" USRDIR extracted/ULUS10136 "<project>/PSP/TEXTURES/modules/fr"
```

### 3.3 Inspection tools (in `tools/analysis/`)
- `dump3.py` / `dump4.py`: contact sheets of the original textures (low resolution enlarged) to read the texts. Example: `python dump4.py fr.png 3 deck/all_f.ehp:d_window00008.gim shop/all_f.ehp:tab_title.gim` (paths inside the USRDIR; set `TF1_USRDIR`).
- `compare_tiles.py`: places the original (nearest 4x) next to the generated HD.
- `textures_per_language.py USRDIR LANGUAGE [--only-different]`: lists per language the textures with a hash different from English/Italian (heuristic on the names: **noisy**, it also includes maps; it serves to estimate the work and not forget archives).
- `find_pixelated.py`, `validate_pack.py`, `inventory.py`: checks on the pack.
- For in-game tests: `tools/extra_upscaling/pad.py` (virtual joypad), `rec.py`, `pw.py`, `dlg.py` (see sec. 9).

---

## 4. Phase 1 - Card texts and card modules

1. **Data from the game**: `tools/languages.py` reads from the `DLG_Text_*` table of `cardinfo_<l>.ehp` the names of the 21 types, the "/Effect" forms, the Spell/Trap labels (indexes 501..559) and the attribute words (531-539).
2. **Text corrections**: `tools/corrections/rules_<l>.py` contains `GLOBALS` (regex -> replacement) and `PER_CARD` (id, field, old, new, reason). The old text must exist **exactly**. `tools/corrections/generate_card_corrections.py` produces `tools/data/card_corrections_<l>.json` (it: `card_corrections.json`; the Italian base is made by `generate_italian_corrections.py`). `tools/corrections/card_corrections.py` is the single point used by `cardprops.load` and `cardnames.names`, so the images and the ISO read the same corrections.
   Objective errors are corrected and wrong or incomplete translations re-adapted; no modernization of the terminology.
3. **Audit** (looks for candidates, does not correct): `tools/audit/audit_language.py LANGUAGE CARDINFO_LANGUAGE.ehp CARDINFO_ENG.ehp OUT [OFFICIAL_LANGUAGE.json OFFICIAL_EN.json]` (categories: missing, numbers, spaces, quotes, typo, English, official). YGOPRODeck covers only fr, de, it, pt; **for Spanish there is no downloadable official database**, so no automatic comparison: spelling checks (`audit/accents.py`, `context.py`, `show.py`) and reading are needed.
4. **Modules**: `python tools/generate_language.py LANGUAGE PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` -> `OUT/cards/small_<l>`, `large_<l>`, `tiny_<l>`, `frame/icons_attribute_race_<l>.png`, `frame/icons_spell_trap_<l>.png`, `OUT/<l>.ini`. Without IDs it regenerates all the cards (2,833 small + 2,833 large, ~930 MB). With IDs only those, without atlas (used after adding corrections). Inside: `attributes.py` (icon table with the language's lettering and icon on the 2,830 small cards), the Spell/Trap label (`extract_labels.py` -> `data/label_eu_<code>_128x32.png`), the deck thumbnail atlas (`tiny_atlas.py generate LANGUAGE PACK OUT` + `tiny_fragment.py`: without it the deck shows the **English** names because the 7 pages have the same hash in all languages).
   Typography: French with non-breaking space before `: ; ! ?` and « » quotation marks; German „ “; Spanish ¿ ¡. Free fonts: XCharter Bold (names/type/labels), Libre Baskerville (effects), Newsreader Italic (Normals), PT Serif Caption (Spells/Traps), Charis SIL (missing glyphs).
5. **After every change to the corrections** regenerate only the touched cards (`generate_language.py ... ID ...`) **and** recompose.
6. **Visual check**: comparison sheets in `comparisons/` and in game (album/deck).

---

## 5. Phase 2 - Title plate

`python tools/ui_textures/mystic_tomato_title.py LANGUAGE` regenerates `modules/<l>/intro/title_screen/` (2 PNGs: `*542eff79685c434d*` and `*705176739829dcf5*`, same path as the pack: they overwrite the base tiles) and puts the original tiles back in the base pack. `--apply PACK LANGUAGE` writes the plate directly into a pack (for PPSSPP). Details: the title backdrop is made of 20 tiles 128x64 (`title_menu_i.ehp: main_title00001..00020`, reverse order); the plate falls in tiles 18 and 19.
Texts (card 4930 in the game's language + "version" wording as in the Pokemon titles of that language + flag): it "VERSIONE POMODORO MISTICO", fr "VERSION TOMATE MYSTIQUE", de "EDITION MYSTISCHE TOMATE", es "EDICIÓN TOMATE MÍSTICO", en "VERSION MYSTIC TOMATO". Font PT Sans Bold.

---

## 6. Phase 3 - HD interface (the long part)

### 6.1 Principle
The scripts `tools/ui_textures/<family>.py` redraw the lettering texture by texture (about 6,500 lines, 8 families), starting from the low-resolution original of the game and from the style of the English pack (style reference: `ui/text/*.png`, etc.). They read `TF1_LANG` (default `it`) and have language tables for fr, de, es, en.

Quality rules (from Italian, always valid):
- letters are regular: one font, one weight, one baseline, a constant shadow; **never** letters deformed one by one;
- the same area/the same positions as the original: the game crops from fixed boxes;
- no "AI look", no blur;
- the language's original is the **text** reference: redraw the words that were there (correcting only obvious errors, e.g. leftovers from other languages), do not invent anything else.

### 6.2 General procedure for ONE family (repeat 8 times)
1. **Work out which textures change.** For every member of the family (the lists `FILES`, `TABS`, `TEX`, `LISTS`, ... in the source) compute the hash in your language, in English and in Italian:
   ```python
   import sys; sys.path.insert(0,'tools/ui_textures'); sys.path.insert(0,'tools')
   import common                      # common.texture(usrdir, 'deck/all_g.ehp', 'd_window00008.gim') -> (PIL image, hash)
   ```
   - hash equal to **English** -> nothing to do (MikeyMK's pack covers it);
   - hash equal to **Italian** (and different from English) -> the `ui_it` texture already made holds (it was the case of the recipe panels, of `dmenu_recipe`, `parts`, `conv_machine__window_i0022`);
   - otherwise **to be redrawn**.
   The same check, extended to everything, is given by `analysis/textures_per_language.py`.
2. **Read the originals.** `dump4.py` at 2-4x enlargement. Note the text of every line, the **words of other languages left in the game** (original bugs: e.g. "SCAMBIA" in French, "TAUSCHEN" in Italian) and the obvious errors (e.g. "2è round").
3. **Parametrize the script** for the language: archive/letter, strings, and the **geometries** that change (text rows, white boxes, widths, number of lines).
4. **Generate in a temporary folder** (not in the module): `TF1_LANG=de python tools/ui_textures/<f>.py USRDIR ULUS10136 tmp`.
5. **Compare with the original** (contact sheet original vs HD): correct texts, position, size, accents neither cut nor on the neighbouring line, colors. The "alpha MAE / color MAE" figure printed by the scripts is only a hint: words different from Italian give higher errors even if they look fine.
6. **Install in the module**: same command with `OUT = PSP/TEXTURES/modules/<l>`. `common.Family.finish()` writes `OUT/ui_<l>/<family>/*.png`, `OUT/ui_<l>/<family>.ini` and **adds/replaces** the lines in the fragment `OUT/<l>.ini` (first removing all the lines of that family). **Trap:** if you rerun a family with only some sub-groups (e.g. `duel_texts icons`), the lines of the other groups are lost from the `<l>.ini`; always rerun the **whole** family.
7. **Check** `<l>.ini`: every `ui_<l>/...` line points to an existing file (snippet in 8.2).

### 6.3 How the scripts are parametrized (model to imitate)
Every script has at the top `LANG = os.environ.get('TF1_LANG', 'it')` and a per-language table. For a new language **add the keys** (letter `'g'`, `'s'`...) to the existing tables and create the language data. Shared things:
- `common.Family`: `self.lang`, folder `ui_<l>`, lines `0000000000000000<hash> = ui_<l>/<family>/<id>.png`, merge into `<l>.ini`.
- The prefix of the file ids is only a name: the hash is what counts.

### 6.4 Recipe per family (with the French example)

Legend: **IT** = how it is done for Italian; **FR** = French adaptation; **DE/ES** = what to do/watch.

#### A. `duel_texts` (13 textures + `card_icon03`) - archive `duel/basic_<l><l>.ehp`
Textures: `chain010005` (word "Catena"), `chain010003` (grey glow), `score-top100011/13` ("TURNO" badge blue/red), `next_player0002+0001` and `0005+0004` ("TOCCA AL GIOCATORE SUCCESSIVO" split over 2 textures, **the cut sits in a gap between two letters**), `start_duel10002+10001` ("INIZIA IL DUEL|LO", cut between letters), `start_duel10005` (glow), `dilect_atk00001/3` ("Attacco Diretto!" + glow), `card_icon03` (sheet of digits/signs).
- **IT**: words composed with a single font (SF Rounded/Chalkboard/Comic -> free fonts via `alt_font`), style measured on the English one (`ui/text/chain.png`, `nextplayersturn_blue/red.png`, `start.png`, `duel_2.png`, `direct_attack.png`, `turn_blue/red.png`).
- **FR** (table `TXT` at the top, with `b`='ff'): chain `Chaîne`; next `TOUR DU JOUEUR SUIVANT` with `next_cut='TOUR DU JOUEUR SUIV'` (cut between V and A: the original cuts there); start `DÉMARRER DUEL`, `start_cut='DÉMARRER DU'`; attack `Attaque Directe!`; turn `TOUR`. The characters `rnext/rstart/rturn` (`'TE'`, `'ED'`, `'TUR'`) are the letters **that must exist in the text** and serve to measure the capital height (`solve_line`: `ref` must be a subset of the text; `TOUR` has no N, hence `TUR`).
- **`card_icon03`** (`do_icons_fr`): the French texture differs from the Italian one only in 10 pixels (cell 88,38-97,45); start from the **already corrected Italian HD** (`PSP/TEXTURES/ULES00600/ui_it/duel_texts/basic_ii__card_icon03.png`: smooth LP/TURNO digits, rows 104-111 rebuilt, 100-103 and 148-151 emptied) and paste the differing French pixels x4. **This is the treatment that removes the dashes under the LP.** For de/es do the same: compare the original with the Italian (`np.abs(a-b).max(-1)>30`) and paste the differing cells. (The current recipe, chosen by the user, is in `docs/NEW_LANGUAGE_GUIDE.md` 7.3.)
- **DE/ES**: the texts may be much longer: read the German/Spanish original. The constraint is the width of the slots: the "TOCCA AL GIOCATORE" banner fills the texture, the `place_line` solver compresses (<=10%), widens the edges (`grow`), and tightens the kerning; if that is not enough reduce the size. Accented capitals (Ä Ö Ü É Ñ): see sec. 10.
- Command: `TF1_LANG=fr python tools/ui_textures/duel_texts.py USRDIR ULUS10136 <module>` (without groups = all: `chain next start attack turn icons`).

#### B. `result_letters` (22 textures) - `duel/basic_<l><l>.ehp`
One **64x64 tile per letter**, composed by the game: win `duel_win1000{02..14}` + silhouette `duel_win100016`, lose `duel_lose1000{02..16}`, draw `duel_draw1000{02..12}`.
- **IT**: "HAI VINTO" (HAIVNTO, 7 tiles + silhouette), "HAI PERSO" (HAIPERSO, 8), "PAREGGIO" (PAREGIO, 7). Times Bold letters with gradient, purple outline, shadow; letters I N O S from the English outline; gradients and colors measured.
- **FR** (`LETTERS`): win `TUASGNÉ` (7: T U A S G N É) + silhouette 16 "TU AS GAGNÉ"; lose `TUASPERD` (8); draw `EGALIT` (6: the original uses E without accent, **there is no É tile in the draw**). Code differences: `'S'` also in the "win" set (shape taken from `ui/text/lose/s.png`); `accent_down()` lowers Times' accent on the É (it was higher than the game's and got cut); parameter **`wide`** (calibrated, fr only) for the wider EGALIT tiles; the test for the win silhouette changes (`let.member == 'duel_win100014.gim'` for fr).
- **DE/ES**: count the real tiles (`duel_win1000NN` up to...): the number and order of the letters depend on the language and **must be read from the original** (contact sheet of the tiles), including repeated letters (the game reuses the same tile). Check the accented letters.

#### C. `menu_lists` (6 textures) - `title_menu/title_menu_<l>.ehp`, `duel/result/result_<l>.ehp`, `field/always_bri_<ita|fra|ger|spa>.ehp`
Title lists (`m_menu_title01` yellow, `trnsmt02` silver wireless list, `menu02` duel result, `press_start0003`), result icon sheet (`result_<l>__menu01` with 3 words), calendar (`story_sys02`).
- **IT**: text rows at a fixed pitch of **21 rows** per line (`line_rows`), Futura Bold font (-> free) with fixed weight/size (`size`, `bold`), style and colors measured on the English images (`en_text`, `en_use`: which English line serves for the colors), condensed lines (`cond`) where the original is too.
- **FR** (`FR` dict): texts in 6+11+6+1 lines (see appendix). Gotchas:
  1. **`line_rows(L, n=...)`**: accented capitals (É) touch the line above and the automatic detection merges two lines; with `n` known the fixed pitch is used (the **maximum** of the clean line heights, 21).
  2. **Accents outside the box**: Futura's accent is taller than the original and ended up on the line above as dots (seen in game in "SAISIR NOM"). Fix: after the fit the lines with accented capitals reduce the size by up to **-8%** to fit (`k_fixed`); if that is not enough the accent is **cut** at the edge (`ln.clip`, applied in `hd_coverage`).
  3. The sample "orig_text" (`orig_text={4:'SCAMBIA'}`): when the text you want to write differs from the one in the original texture (Italian leftover), the algorithm is given the **original** word to measure width/spacing and the new one is written with `fit_free`.
  4. `LABELS` of the icon sheet: in French they are **not condensed** (5-7 letters): `LABEL_SPEC=FUTURA_BOLD`, `LABEL_SX=(0.95,1.25)`; for Italian `FUTURA_COND_XB`, `(0.9,0.9)`.
  5. Calendar: `CAL_SERIF` (days/months, Times Bold), `CAL_ROUND` (cream words with brown outline), digits `0123456789月日ー` (Hiragino, the same in all languages). For fr: Dimanche, Lundi, Mardi, Mercredi, Jeudi, Vendredi, Samedi; Mai, Juillet, Juin, Août; "jours" / "avant le tournoi"; Matin / Soir. The boxes are the same as Italian. For de/es the names change (long days/months: check they fit the boxes: `Fitter.fit_set` compresses down to `sx_min=0.9`, then reduces the size).
- **DE/ES**: menu texts **different in length**: the lines of `trnsmt02` and `m_menu_title01` have a fixed width (256 px): `LISTE CARTES TÉLÉCHARGÉE` fits at ~0.93, long German words (e.g. "Kartenliste heruntergeladen") need compression/small size. Check whether the original game's strings are already abbreviated: **reproduce those**.

#### D. `icon_sheets` (3 textures for fr) - `deck/all_<l>.ehp`, `shop/all_<l>.ehp`
Icon sheets where few words change: `icon04` (start from the HD English sheet and **only the changing pixels** in x4 pixels, e.g. "Mia/Moi" and "A/L" badges), `s_pack` ("ESAURITE"/"ÉPUISÉ" in PT Sans Bold on the pack's red), `panel` (the tab lettering "prati"/"hetés": **it is a fragment** of a word that continues in another texture; reproduce the fragment of the original, not the whole word).
- **FR**: constants `SP_TEXT`/`SP_X` (x0..x1 of the ink in HD: 45..228), `PANEL_TEXT='hetés'`, `TEXTURES_FR` (only 3 entries; `pda_pack01`, `ocglist`, `icon06`, `mein_menu00`, `trnsmt01` have **the same hash as English in French** and need not be redone), `build_icon04_fr` (uses `EN_LOW`, the low-resolution English texture, to find the differing pixels; dilates by 1 px; the document with the lightning bolt `bolt_doc(...)` stays as in Italian).
- **DE/ES**: same hash check: probably only `icon04`, `s_pack`, `panel` differ. Measure x0/x1 of the word with the ASCII print (`low[232:246]`) or by looking at the original at 8x.

#### E. `deck_screens` (10 textures for fr) - `deck/all_<l>.ehp`, `labo/*.ehp`, `shop/all_<l>.ehp`
Tabs of the deck editor, of the laboratory, of the shop (Cassa, Affitto, Laboratorio, Convertitore, "Tipi di Carte Posseduti", "Carte Comprate / Tipi di Carte com...", INVIO key).
- **FR** (`TEX_FR`): Coffre x2, Location x3, Labo, Convertisseur, "Types de cartes acquis", "Cartes achetées" + "Types de cartes ac" (the second is a **fragment** at the edge of the texture), ENTRÉE. `white_box(low)` derives automatically (columns with >=9 white rows) the parameters `box_x0`, `right` that for Italian were hand-written; rule: width <20 -> margin 2, otherwise 1. `key_caption(low)` (ENTRÉE) vectorizes from the original: valid for every language. Same words in French as "Fusion/Side/Deck" (hash = English: the pack does it).
- **DE/ES**: list which of these textures differ from English; write the words; check that the tab lettering does not go out of the tab (long words: `tabword.render_tab_word` compresses and reduces the size; `TAB_CAP=44`).

#### F. `recipe_screens` (11 textures for fr) - `deck/recipe_view_<l>.ehp`, `title_menu/title_menu_<l>.ehp`, `database/limitlist.ehp`
Tabs: Personnage / Utilisateur / Téléchargée / Limitée / Semi-limitée / Interdite / Échange.
- **FR** (`FR_WORDS` + `TABS_FR`): the **geometry** (`ix`, icon, `tx`, `slot`) is the Italian one (same boxes); the word and the **right limit** of the text `tx[1]` measured on the original change (script: columns of white pixels >=230 between x0 and the box). Panels `recipe_panel`, `dmenu_recipe`, `parts`, `recipe010002/4/6` have the **same hash in all languages**: they stay `ui_it`.
- `Scambia` in French is an **Italian leftover** of the game: written `Échange` (as Italian has "Scambio" instead of the German "Tauschen").
- **DE/ES**: same thing; for the limits use the words of the original (e.g. "Eingeschränkt/Halb eingeschränkt/Verboten" are long: mind the right limit).

#### G. `vs_screen` (14 textures) - `duel/start/start_e.ehp` (members `_<l>`), `start_all.ehp`, `start_<l>.ehp`
DUEL / NORMAL / TAG (big banners in Times Bold with red-yellow gradient), glows "DUEL NORMAL" / "TAG DUEL", "Modalità ..." (two), "n A GIOCARE" (two), "n Duello" (three: `vs_much1..3`), rock-paper-scissors sheet (`jnk_card01` with the words VITTORIA/SCONFITTA/PAREGGIO), player sheet (`d_menu01_<l>` with the 4 badges "n° GIOCATORE" and the GIOCATORE tab).
- **FR** (`main_fr`, `FILES_FR` derived from `FILES` replacing `_i0`->`_f0`, `start_i`->`start_f`):
  1. **Banners**: `banner_fit(text, low)` searches size, compression, position and baseline so that the ink box (alpha>1/2, outline and shadow included) matches that of the original (6 iterations): the game **widens** the words to fill the texture, so the fixed Italian parameters are not right. fr words: `DUEL`, `NORMAL`, `TAG`.
  2. **Glows**: for fr they are derived from the original alpha (`glow_from_original`) for both.
  3. **"To play"**: `play_text(text, shape, left, right)`: whole sentence with tracking to fill the measured width (HD px): `DEUXIÈME À JOUER` (148..876), `PREMIER À JOUER` (180..848).
  4. **Rounds**: `round_text`: `1er round` (66..446), `2e round` (82..430), `3e round` (90..442) (the original has "2è/3è").
  5. **Modes**: `mode_word('Mode Un Duel', ..., base 52, 32..476)` and `('Mode Match', 60..452)`; Italian has base 84 for the accent of "à"; measure the extents of the colored **fill** (`np.abs(a-color).sum<60`).
  6. **jnk**: `JNK.update(size=81, base=1017)` (the French letters are 17 rows tall against 11) and words `GAGNÉ`, `PERDU`, `EGALITE` with `(left, right)`; the compression (0.8-1.15) is computed first and then the tracking.
  7. **d_menu01**: `BADGE_TXT=['1er JOUEUR','2e JOUEUR']*2` (Helvetica 42), `JOUEUR` tab (`TAB_WORD`) **narrower** than the English one: `TAB_DW=-16` (columns removed from the body and fillet lengthened so as not to move the rest), Arial Black size adapted (`fit_size`, max 33).
- **DE/ES**: same structure. Likely differences: "SPIELMODUS: Einzel/..."; German has very long words -> more compression; the player tab may be wider (dw>0).

#### H. `tutorial` (6 textures) - `tutorial/tutorial_<l>.ehp` (members `tuto_duelimg01..06`)
Illustration 01: dialogue window (duel background, box, OUI/NON buttons, small card, two-three lines of text); 02-06: map of a card with the type disc (equip, continuous, counter, quick-play, field).
- **FR** (`LANG`, `LL`): `FILE=tutorial/tutorial_f.ehp`, **`TF1_EHP`** set before importing `small_it` (otherwise it takes the Italian terms: "[CARTA MAGIA]"), texts `Ton adversaire a déclaré le duel.` / `Activer l'effet de la carte ?` (non-breaking space before the `?`), buttons `OUI`/`NON`, `TEXT_BASE=(27.0, 36.6, 46.1)` (2 lines), **geometry different from Italian** (measured on the original: box `BOX=(37,10,219,107)`, buttons `BTN_BLUE_AT=(72.75,48.875)`, `BTN_CREAM_AT=(137,49.125)`, `BTN_LABEL base=60.7`, small card `MINI_AT=(120,75,16,24)`, `FIELD_RECT=(29,2,227,114)`) because the dialogue has one line less. Name, description and label of the 5 cards come from `cardinfo_fra.ehp` (fixed cids: 4317, 5161, 4863, 5355, 4340); the label atlas is generated with `label_it.py` (run **without** `-I`).
- **DE/ES**: recompute the geometry by measuring (snippets in 6.5); check whether the dialogue has 2 or 3 lines and where the buttons sit; remember `YES`/`NO` (e.g. "JA/NEIN", "SÍ/NO").

### 6.5 Measurement snippets used (adapt them)
- Bounding box of a color in a low texture (HD = x4): `m=(a[...,3]>200)&(np.abs(a[...,:3]-col).sum(-1)<tol); ys,xs=np.where(m)`.
- Rows at a fixed pitch: the rows start at multiples of 21 (list menus); check with `line_rows`.
- Extent of the white text of a tab: `(a[...,:3].min(-1)>=230)&(a[...,3]==255)` between x0 and the box.
- Differences between two languages: `np.abs(a-b).max(-1) > 30` then `cv2.connectedComponentsWithStats` on the dilated mask to get the cells.

### 6.6 When a texture has the same hash but still English text
Textures identical to English stay in English also in the original game (e.g. "NO DATA", "Deck/Fusion Deck/Side Deck", "Standby Phase", "Draw Phase", "Main Phase", "Duel Result" banner): **it is not a pack error**, it is the original. They are not replaced without a decision of the project owner.

---

## 7. Phase 4 - Texts inside the ISO

The text drawn by the game with its own font cannot be changed with the pack. `tools/corrections/apply_to_iso.py ORIGINAL_ISO CORRECTED_ISO [LANGUAGE ...] [--parts=cards,text]` creates a copy with (every language that has a table):
1. **Card texts** (`duelsys/cardinfo_<l>.ehp`: `CARD_Name_X.bin`, `CARD_Desc_X.bin`, `CARD_Indx_X.bin`) from `tools/data/card_corrections_<l>.json`.
2. **Dialogues** (`script/stNN_*_<l>.ehp`): `tools/corrections/dialogues.py` with `tools/data/dialogue_corrections_<l>.json` (id `st01_t01/Scr077E#3` -> current, proposed). Every scene is a pair of files (gz or not): `...Ii` (offsets in UTF-16 characters) and `...Li` (UTF-16LE strings terminated by NUL). Constraints: **width 46 characters** per line (the game does not wrap by itself; the original reaches ~49), **max 3 lines** in the box (7 Italian proposals have more: to check in game), a `《...》` placeholder counts ~6 characters, space before and after the placeholders (automatic rules in `build_dialogues.py`; fr: space before `! ? : ;`; de: case `》s`).
3. **Character sentences in duels** (`chr_wordstbl_<l>.bin`/`02chr_wordstbl_<l>.bin` inside `duel/cutin_*.ehp`, `zakov*`): `tools/corrections/duel_lines.py` with `tools/data/duel_line_corrections_<l>.json` (`exact`: whole sentence; `parts`: replacements). **Mind the `*-ptrs.txt` files** in the character archives: they contain the **absolute offsets** of the members; if a table grows they must be updated (`remap_pointers`) or the duel **crashes** (`Invalid Memory Access` at 0x20). 237 sentences in 66 archives for all languages together.
4. **Interface strings** (`tools/data/ui_texts.json`): targeted corrections to `strTbl.bin`, `ddstrtbl_<l>.bin`, `help_strtbl_label_<l>.bin`: labels cut by the edge (it: "Assistenza"->"Aiuto", "Posizionam"->"Posiziona"), strings of another language in the tables (it "Kartenrand"->"Cornice", fr "Cornice della Carta"->"Cadre de la carte", de "Couleur de cadre"->"Kartenrand", es missing accent). To find the labels at risk: `audit/long_labels.py ISO [ratio>=1.4] [minimum length 9]`. Candidates reported and **to be checked in game**: FR "Rechercher", "Aucune restriction", "Étiquette"; DE "Ausführen", "Keine Beschränkung", "Sortieren", "Beschwören", "Schließen"; ES "Invocación". Longer strings go through `tools/corrections/ui_strings.py` + `string_rules_<l>.py`.
5. **[SPELL CARD]/[TRAP CARD] label of the large card in the duel**: in all the `duel/basic_XY.ehp` there was the English label (hash c2268340); `apply_to_iso.py` copies `card_spell_trap.gim` of `field/always_<l>_<l>.ehp`.
6. **Original game bug**: scene `st02_t01/Scr101E` lines 22-27: the text is **rotated between the languages** (it has French, fr German, de English, es Italian); `build_dialogues.py` puts each one back in its own language.

Flow for the dialogues:
```
python tools/audit/extract_dialogues.py ORIGINAL_ISO comparisons/audit_dialogues        # dialogues_<l>.tsv (id, text, English, Japanese)
# read (by hand, on a list of unique lines) and record the touch-ups in tools/data/dialogue_touchups_<l>.json  {"exact":{line:new}, "parts":[[old,new]]}   (line breaks written ⏎)
python tools/corrections/build_dialogues.py LANGUAGE                               # -> tools/data/dialogue_corrections_<l>.json
python tools/corrections/apply_to_iso.py ORIGINAL_ISO DEFINITIVE_ISO                 # all languages
```
Audit method used: spell checker (`pyspellchecker`) on the rare words + check of the lines in the wrong language + reading, with English and Japanese next to every line. Where the localisation lost or changed the meaning, or a sentence is missing, the line is re-adapted from the original language (see `docs/CHANGES_<LANG>.md` for the counts).

---

## 8. Phase 5 - Composing the pack and installing it

### 8.1 Compose
```
python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules <USRDIR>/card <OUT> fr --copy
```
(with `--copy` because PPSSPP lives on `C:` and the project on `F:`; without it, hard links). Several languages can be given, but **a single banner/atlas/attribute table wins** (the first): for tests use **one language at a time**.
The composed pack goes in `<PPSSPP data folder>/PSP/TEXTURES/ULES00600`. An Italian pack already installed there must not be lost: **rename** it before putting the new one, and put it back at the end of the test.
After changing **a single PNG**, it is enough to copy it into the installed pack (the `textures.ini` does not change) and **restart PPSSPP** (textures are cached).

### 8.2 Automatic checks
```python
import os,re
M='PSP/TEXTURES/modules/fr'
for l in open(f'{M}/fr.ini',encoding='utf-8'):
    m=re.match(r'^([0-9a-f]{24})\s*=\s*(\S+)',l)
    if m and m.group(2).startswith('ui_fr/') and not os.path.exists(f'{M}/{m.group(2)}'): print('missing',m.group(2))
```
In every composed `textures.ini` (also `_CHOOSE YOUR CARD STYLE/*/textures.ini`) all the `ui_<l>/` lines must appear. Every `ui_<l>` hash is already present in the base `textures.ini` (it pointed to `upscale_extra` or to English): the fragment **replaces** that line, it does not duplicate it (no duplicate hashes). `patcher/tools/verify_texture_pack.py textures.zip` does the same on a finished zip.

### 8.3 Recommended PPSSPP settings
Replace textures ON; rendering resolution **4x** (it is the one that really improves: at 4x/Auto the 4xBRZ shader is off: for this reason the uncovered textures are enlarged in advance in the pack, `upscale_extra`); game system language = that of the module. The Android `textures.zip` (2.5 GB) must be **regenerated** with the corrections and the banner of the chosen language.

---

## 9. Phase 6 - In-game test

### 9.1 Preparation
- Close PPSSPP if open. Put the language's pack in `PSP/TEXTURES/ULES00600` (see 8.1).
- **Save files**: the game language is written in the save. Never leave a test save in place of a real one. To try with a save: rename the language's one to `ULES006000001`; at the end of the test put it back. Without a save the game shows the language selection screen and, when the name is confirmed, creates a **new** save.
- ISO: to test **dialogues and corrections** use `ULES00600_YuGiOh_GX_TagForce_EUR_definitiva.iso` (regenerate it with `apply_to_iso.py` if you changed the tables); to test **only textures** the original is fine (but you will not see the text corrections).
- Set the path of the ISO in the `TF1_ISO` environment variable for the helper scripts in `tools/extra_upscaling/`.

### 9.2 Virtual joypad (the only reliable way for the controls)
Keys sent with `PostMessage`/`keybd_event` **do not arrive**. The ViGEmBus driver with `vgamepad` is used:
1. Copy `tools/extra_upscaling/pad.py` to a work folder, create an empty `cmd.txt` and start `python -P pad.py` in the background.
2. Send commands by adding lines to `cmd.txt`: `btn A [ms]`, `btn START`, `btn UP|DOWN|LEFT|RIGHT|B|X|Y|LB|RB|BACK`, `seq DOWN,DOWN`, `wait 2.5`, `shot name variant`. PPSSPP map: A = Cross (confirm), B = Circle, X = Square, Y = Triangle, START = Start.
3. Screenshots: `python -P pw.py out.png` (captures the PPSSPP window even if covered, via `PrintWindow`); interval recording: `python -P rec.py DIR SECONDS` (saves only the frames that change). Then a montage of the unique frames (diff on 160x90) to look at them as a grid.
4. `tools/extra_upscaling/dlg.py N`: presses A until the dialogue window (cream box at the bottom) disappears, at most N times; beware: pressing A **without** a dialogue in the office opens the menu and "Talk" starts a new dialogue (you stay in a loop).
5. If the pad does not respond, check that `pad.py` is still running and that `log.txt` is updated.

### 9.3 Test path (with an existing save)
Intro -> START (several times) -> title ("New game" / "Continue") -> `Continue` -> "Data loaded." -> OK -> **Main menu** (Story mode, Free duel, Deck menu, Database, Network mode, Options, Save data, Language selection): the cursor **remembers the entry**; `Free duel` is disabled until unlocked.
- `Deck menu` -> `Deck editing` (deck editor) and `Recipe viewer`.
- `Database` -> `Duelist list`, `Card album`, `Tutorial`, `Duel ranking`, `Forbidden/Limited card list`.
- `Story mode`: chancellor's office (menu `Talk / Duel / Items / PDA / To the map`, calendar at the top right, place box), shop, laboratory, tutorial, duels.
- **New game**: title -> `New game`; language selection (arrows + A); movie; "Enter a name" (system keyboard: A enters the characters up to 8; **START (Done)** confirms — after restarting `pad.py` if it does not respond); "Press START to confirm" -> START -> "A new file will be created" -> YES -> save -> story: the dialogues advance **only with A at every line**, B does not skip them.
- **Demo duel**: leaving the title idle for ~1 minute starts an automatic duel (useful for VS, HUD, TURN, "NEXT PLAYER", duel texts).

### 9.4 Screens to see
Title (plate, "PRESS START" HD, menu); main menu + database + deck menu (HD titles, long entries not cut); deck editor (tabs, "Card types in possession", "Help", START); recipe window; confirmation "Finish deck editing"; calendar in the office; office menu; VS screen; duel (HUD, TURN n, NEXT PLAYER, descriptions, Chain, Direct Attack, end of duel, rock-paper-scissors); tutorial illustrations; shop (SOLD OUT, "Purchased Cards" tab); laboratory (Converter, Lab, Rental); PDA; album (new cards); large card in the duel with the Spell/Trap label; corrected dialogues in the story. In the Tutorial of the database and in the duelist list the list is **empty** with a new game: advance in the story or use a more advanced save.

---

## 10. Traps and mistakes already made

1. **Losing the US pack / USRDIR**: they live outside the project and in temporary folders; temporary files get cleaned by other sessions (it happened to the pack, to `pad.py`, to helper scripts). Keep copies of the tools in the project.
2. **`Family.finish()` replaces all the lines of the family** in the `<l>.ini`: always rerun the whole family.
3. **`python -I` and packages in the user site**: `No module named requests/cv2`. Avoid `-I` (or install into the system site).
4. **Heredoc/escape**: `\u00cc`, `\\u00a0`, paths with backslashes. Write files with a write tool; use `chr()`.
5. **Automatic row detection** (`line_rows`) breaks with accented capitals (merged rows): use `n=` and the fixed pitch (max clean height).
6. **Word of a different language in the original texture** (SCAMBIA, TAUSCHEN): treat it as a game bug; use `orig_text`.
7. **Rerunning a single group of `duel_texts`** (`icons`) deletes the lines of the other groups from the `.ini`.
8. **Language-specific geometry**: the French tutorial dialogue has 2 lines and a lower box; the VS banners are widened by the game to fill the texture; the "JOUEUR" tab is narrower. Do not assume that the Italian numbers hold: **always measure on the original**.
9. **Split tiles**: words over 2 textures (TOCCA... SUCCE|SSIVO) -> the cut goes in a gap between letters (`seam_shift`); letter tiles (result_letters) one per letter.
10. **The capital's accent** in Times/Futura is taller than the game's: lower it (`accent_down`) or reduce the size + `clip`.
11. **Testing with the wrong ISO**: the original does not have the dialogue/string/large-label corrections; use `_definitiva` for those.
12. **Save and language**: the language is in the save. Do not leave the test save in place of the user's.
13. **Name of the joypad/window**: `pw.py`/`pad.py` look for the window whose title starts with `PPSSPP Gold`; if PPSSPP is a different build change the filter.
14. **Do not trust the MAE alone** (alpha/color): new words give high values. Look at the image.
15. **Do not touch pixel textures** (rule 3) and **do not use Real-ESRGAN** (discarded: corrupted textures, palettes changed at runtime).
16. **The 438 map/background textures are not replaced** (the game changes their palette): not a defect of the new work.
17. **PPSSPP remembers the menu cursor**: after a subpage the cursor is not where you think: take a screenshot before pressing A.
18. **`generate_language.py` keeps the `ui_<l>/` lines** of `<l>.ini` (it used to lose them).
19. **Do not "correct" official terms**: in French "Carte Équipement" and "Deck Fusion" are correct.
20. **`PER_CARD` is applied before the `GLOBALS`**: the old text is looked for in the original text.
21. **Mojibake in the touch-ups**: after every change to `dialogue_touchups_<l>.json` / `rules_<l>.py` check that there are no sequences like `Ã©`, `Ã `, `â€™` (grep `Ã` in the files): a rule with a dirty "old" never applies and one with a dirty "new" writes wrong characters in the game. Repair: `s.encode('cp1252').decode('utf-8')` on the sequences. Write the files with a write/edit tool, not with a heredoc inside `python -c`.

---

## 11. Definition of "done"

A language is "at the level of Italian" when:
- [ ] card module complete, corrections applied and **seen in game** on a card with new text (album/deck and large card in the duel);
- [ ] title plate seen in game;
- [ ] `ui_<l>`: all the families done; every `ui_<l>` line in `<l>.ini` points to an existing file; the 8 families compared with the originals by eye;
- [ ] seen in game: title, main menu, deck editor, recipes, shop, laboratory, calendar, PDA, VS, duel (HUD, Chain equivalent, direct attack, end of duel, rock-paper-scissors), tutorial;
- [ ] `_definitiva` ISO tried: dialogues (at least the initial scenes and a duel), duel sentences, UI strings, Spell/Trap label of the large card;
- [ ] long labels checked (sec. 7, point 4);
- [ ] Android `textures.zip` regenerated with the chosen language (or flagged as still to do);
- [ ] `docs/EDITORIAL_CHOICES.md` and the generated `docs/CHANGES_<LANG>.md` updated; this handbook updated if the method changed.

How to document: the generated document `docs/CHANGES_<LANG>.md` carries the numbers; record the hand-made decisions in `docs/EDITORIAL_CHOICES.md` with dates, the texture-by-texture reading in `docs/changes_<l>/texture_texts_<l>.md`, and what was seen in game and what was not.

---

## 12. Appendix

### 12.1 Main files and scripts (paths relative to `tools/`)
| File | What it is for |
|---|---|
| `languages.py` | per-language data read from the game; `TF1_LANG` |
| `ehp.py`, `gim.py` | reading archives and textures, hashes |
| `alt_font.py`, `alt_fonts/` | free fonts instead of the Apple ones |
| `generate_language.py`, `attributes.py`, `tiny_atlas.py`, `tiny_fragment.py`, `extract_labels.py` | card module of a language |
| `compose_pack.py`, `module_ini.py` | composition of the pack and of the inis |
| `ui_textures/*.py` | HD interface (it and, with `TF1_LANG`, the other languages) |
| `ui_textures/common.py` | `Family`, `texture`, `reference`, `check` |
| `ui_textures/mystic_tomato_title.py` | title plate |
| `ui_textures/pixel_hd.py`, `hd_numbers.py`, `vector.py` | approved fixes on chunky-pixel sprites |
| `corrections/rules_<l>.py`, `generate_italian_corrections.py`, `card_corrections.py`, `apply_to_iso.py`, `dialogues.py`, `duel_lines.py`, `ui_strings.py`, `build_dialogues.py`, `single_language_iso.py` | ISO texts |
| `data/*.json` | correction tables, `ui_texts.json`, `tiny_atlas.json`, labels |
| `audit/*.py` | audits of cards, dialogues, sentences, long labels |
| `analysis/*.py` | inspection and documentation: `textures_per_language`, `dump3/4`, `compare_tiles`, `extract_usrdir`, `mega_dl`, `find_pixelated`, `validate_pack`, `document_*`, `write_changes_document` |
| `extra_upscaling/pad.py`, `rec.py`, `pw.py`, `dlg.py` | in-game tests |
| `rebuild.sh`, `rebuild_corrections.sh` | full rebuild of the Italian pack / regeneration of the corrected cards |

### 12.2 French texts used (reference for translating into de/es)
- **duel_texts**: Chaîne · TOUR (blue/red) · TOUR DU JOUEUR SUIVANT · DÉMARRER DUEL · Attaque Directe!
- **result_letters**: TU AS GAGNÉ · TU AS PERDU · EGALITE
- **menu_lists**: MENU PRINCIPAL / SAISIR NOM / LISTE CARTES TÉLÉCHARGÉE / PUZZLE DUEL / OPTIONS / SÉLECTION DE LA LANGUE · LISTE DE GROUPE / FAIRE UN NOUVEAU GROUPE / LISTE D'ENTRÉE / DUEL / ÉCHANGE / ENVOYER UNE RECETTE / ENVOYER UNE CARTE / ENVOYER UN PUZZLE DUEL / DUEL LIBRE / DUEL NORMAL / TAG DUEL · RÉSULTAT DU DUEL / BONUS DUEL / BONUS NOUVEAU MEILLEUR SCORE / BONUS DÉFI COMPLÉTÉ / RÉSULTAT INTERMÉDIAIRE / RÉSULTAT FINAL · APPUYEZ SUR LA TOUCHE START · GAGNÉ / ÉGALITÉ / PERDU · Dimanche Lundi Mardi Mercredi Jeudi Vendredi Samedi · Mai Juillet Juin Août · jours / avant le tournoi · Matin / Soir
- **icon_sheets**: ÉPUISÉ · hetés (fragment of "Cartes achetées")
- **deck_screens**: Coffre · Location · Labo · Convertisseur · Types de cartes acquis · Cartes achetées · Types de cartes ac(quis) · ENTRÉE
- **recipe_screens**: Personnage · Utilisateur · Téléchargée · Limitée · Semi-limitée · Interdite · Échange
- **vs_screen**: DUEL / NORMAL / TAG · DEUXIÈME À JOUER / PREMIER À JOUER · 1er round / 2e round / 3e round · Mode Un Duel / Mode Match · GAGNÉ / PERDU / EGALITE · 1er JOUEUR / 2e JOUEUR · JOUEUR
- **tutorial**: Ton adversaire a déclaré le duel. / Activer l'effet de la carte ? · OUI / NON · cards: Pendentif Noir, Bouclier du Lustre Jaune, ... from `cardinfo_fra.ehp`

### 12.3 When the script is not enough
If a texture has an unprecedented layout (as it was for the French tutorial and the JOUEUR tab): draw starting from the original, **measure** the geometries (bounding boxes of the colors, extents of the text), parametrize and **verify with a contact sheet** original/HD. Do not settle for "it is close": the textures are cropped by the game from fixed rectangles.

### 12.4 Interface strings (strTbl, help, duelist cards)
Besides cards, dialogues and duel sentences, the ISO has **string tables** with format `(n, 12, 12+4n)` + offsets + UTF-16 in members of the `.ehp` files (same format as `chr_wordstbl`; `duel_lines.read_table/write_table` read and write, identical round trip). For a language they must be **read in full**:
| Archive (under `PSP_GAME/USRDIR`) | Member (fr) | Content |
|---|---|---|
| `database/charalist.ehp` | `strTbl_<l>.bin` | duelist cards (biographies) |
| `database/duelrecord.ehp`, `duel/result/result_<l>.ehp` | `strTbl_<l>.bin` / `strTbl.bin` | duel records and goals (the two tables are equal) |
| `database/{cardalbum,limitlist,tutoriallist}.ehp`, `duel/start/start_<l>.ehp`, `shop/all_<l>.ehp`, `labo/{conv_machine,password}.ehp` | `strTbl_<l>.bin` | titles and messages |
| `deck/all_<l>.ehp` | `strTbl.bin`, `help_strtbl_contents.bin`, `help_strtbl_label.bin` | deck editor and its help |
| `deck/tutorial.ehp` | `strTbl_<l>.bin` | deck editor tutorial |
| `duel/basic_b<l>.ehp` | `ddstrtbl_<l>.bin`, `help_strtbl_contents_duel_<l>.bin` | duel labels and help (the European ISO loads `basic_b<l>`) |
| `field/always_*_<f3>.ehp` | `field_strtbl.bin`, `field_strtbl_item.bin`, `field_strtbl_mapname.bin` | office menu, calendar, items and sandwiches, places |

Procedure: (1) extract the tables (use `ehp.read` + `duel_lines.read_table` on all the `.ehp` of the USRDIR and group by archive/member; print `index | text || English`); (2) read everything comparing with English (sentences are missing, there are leftovers from other languages: e.g. "Cornice della Carta" in the French table); (3) write `tools/corrections/string_rules_<l>.py` (see the French one: `STRINGS`, `GLOBALS`, `TABLES`; the old texts must appear exactly, real line breaks `\n`, sometimes `\r\n`); (4) `apply_to_iso.py` rewrites the archives and prints the warnings. The indexes are 0-based in the table. The speaker name (e.g. "Doyen Sheppard") lives in the executable and **cannot be modified**.

### 12.5 Second reading of the dialogues (French example)
1. Export the unique lines to a txt and read them in blocks.
2. For every error add a pair `(old, new)` to `parts` in `dialogue_touchups_<l>.json` (check that the text exists).
3. `build_dialogues.py <l>`, then `apply_to_iso.py ORIGINAL_ISO OUT_ISO <l>`: it must print 0 warnings.
4. French punctuation `! ? : ;` is spaced by `FR_PUNCT`, also after `》`.
