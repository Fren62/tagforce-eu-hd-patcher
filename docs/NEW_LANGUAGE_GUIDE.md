# GUIDE - How to adapt the game to a European language

**General** guidelines (valid for Spanish, German, English or any European language of the game) derived from the work done on **Italian** and
**French**. The examples come from those two cases; nothing here is specific to one language. For the technical details of every script see `docs/TUTORIAL.md`
(recipes per texture family, virtual joypad, pitfalls) and for the **editorial choices already taken**
`docs/EDITORIAL_CHOICES.md` (and `tools/data/editorial_choices.json`).

**Complete documents of everything that was done, to be taken as models:** `docs/CHANGES_IT.md` and `docs/CHANGES_FR.md` (changes to the ISO line by line, structure and content of the texture pack, choices, checks; exact lists in `docs/changes_<l>/*.csv`). They are regenerated with `tools/analysis/document_changes.py`, `text_comparisons.py` (original->new comparisons with highlighted words), `document_pack.py`, `write_changes_document.py` (also for es/de: add the language to the `NAME` dictionary and create `rules_<l>`).

Whoever starts: read this guide, then `docs/EDITORIAL_CHOICES.md`, then `docs/TUTORIAL.md` sections 2, 3, 7 and 13.

---

## 0. Principles (valid in every phase)

1. **The text reference is the original Japanese/English of the game, not inventiveness.** Objective errors are corrected (typos, accents, spaces,
   agreement, leftovers from other languages) and, above all, every sentence whose localisation **lost or changed the meaning** of the original is re-adapted and translated again
   from the original language, including censored sentences and sentences that are missing altogether in some languages. The terminology is not "modernized".
2. **Every check done for one language extends to all the others** (it, fr, de, es, en): if you find a class of error in Italian, look for it in all of them.
3. **Every editorial decision is registered** in `docs/EDITORIAL_CHOICES.md` **and** in the language's data, with id, original text, new text, reason.
   This way a patcher for another language applies the right equivalent (example: "hot sauce -> shochu" is a common choice, every language writes it its own way).
4. **Never modify the original ISO**: `apply_to_iso.py` writes a copy (`..._definitiva.iso`).
5. **Do not smooth the pixel art** (keys, arrows, flags, small digits) without the user's confirmation. The original pixel is preferred.
6. **Read all the text by hand**, even if tools exist: automatic spelling and comparison with official databases find typos, not errors of meaning.
   For the dumps always use text **without duplicates** with English next to it: they are thousands of lines, but repeated few times.
7. **Verify in game** (`_definitiva` ISO + pack): a correct file is not enough.
8. Document while you work, not at the end.

## 1. Map of the work (one language = these 8 blocks)

| # | Block | Where the data lives | How it is applied |
|---|---|---|---|
| 1 | Card texts (names + descriptions) | `tools/corrections/rules_<l>.py` -> `tools/data/card_corrections[_<l>].json` | ISO (`cardinfo_<l>.ehp`) **and** HD images |
| 2 | HD card images (small, large, thumbnails, attributes, labels) | `PSP/TEXTURES/modules/<l>/cards` | texture pack |
| 3 | Story dialogues | `tools/data/dialogue_touchups_<l>.json` -> `dialogue_corrections_<l>.json` | ISO (`script/*.ehp`) |
| 4 | Duelist sentences in duels | `tools/data/duel_line_corrections_<l>.json` | ISO (`duel/*.ehp`) |
| 5 | Long interface strings (help, duelist cards, tutorial, records) | `tools/corrections/string_rules_<l>.py`, `tools/data/ui_texts.json` | ISO |
| 6 | Drawn HD interface (lettering in images, ~86 textures) | `ui_<l>` in the module, scripts `tools/ui_textures/*.py` with `TF1_LANG` | texture pack |
| 7 | Duel number sheet (`card_icon03`), title plate | `tools/ui_textures/icon03_languages.py`, `mystic_tomato_title.py` | texture pack |
| 8 | Register of choices + in-game test + documentation | `docs/EDITORIAL_CHOICES.md` | - |

Single entry point for the texts in the ISO: `python tools/corrections/apply_to_iso.py ISO_ORIG ISO_OUT [languages] [--parts=cards,text]`. **Without a list of languages it applies all of them**:
do not run it with a single language towards the final ISO, you would overwrite the others (a mistake already made).

---

## 2. Card texts (block 1)

**What is corrected**: typos (`Annello`->`Anello`), accents (`E'`->`È`, `puo`->`può`), apostrophes and spaces (`L' OSCURITÀ`->`L'OSCURITÀ`, `Magia,Trappola`), capitalization
inconsistent with the rest of the game (`Main phase`->`Main Phase`, `tipo Pyro`->`Tipo Pyro`), agreement (`questo carta`, `vengono cambiata`), fixed plurals of terms
(`Life Point`->`Life Points`), words from other languages, card names badly quoted in other descriptions (`Victory Viper XX3`->`XX03`), and descriptions whose meaning was lost
or changed by the translation (re-adapted from the English/Japanese text). **Not changed**: official names
in the text, terminology chosen by the game (e.g. in French "Carte Piège Continu" is consistent throughout the game: it is left; in Italian "Terreno", "Evocazione tramite Tributo").

**Method (used for it and fr)**
1. Extract the texts (`cardprops.load(cardinfo_<l>.ehp, corrected=False)`), one per line `id <TAB> name <TAB> description`, in blocks of ~90 lines (a tool's output is
   truncated at ~30 KB: more is wasted).
2. **Read everything, in order.** Note every error immediately (id + text): notes go to a file, **not** to memory (a long context is compacted and the notes are lost: it happened).
3. Turn the errors into **rules**: prefer `GLOBALS` (regex `(pattern, replacement, reason)`) when the error is of a class; `PER_CARD` (id, field, old, new, reason)
   for the unique cases. The "old" text of `PER_CARD` must appear **exactly** or the script stops (this is intended: the table does not derive from a wrong reading).
4. After the rules, an **automatic scan** of the error class on all the cards (double spaces, ` ,`, `,A`, `.A`, apostrophe+space, doubled word, `E' `...): it finds what the eye skips.
5. Generate: `python tools/corrections/generate_card_corrections.py LANGUAGE CARDINFO_<l>.ehp` (also writes `comparisons/audit_cards/corrections_<l>.csv`).
   - fr/de/es/en: starts from the **original** texts and writes `tools/data/card_corrections_<l>.json`.
   - it: starts from the **already corrected** texts and **merges** into the existing `tools/data/card_corrections.json` (idempotent: can be rerun).
6. Checks: the `PER_CARD` must not give "text not found"; read the CSV of the changes; **no global rule must touch what you did not want** (look at the printed counts: a rule with 140 matches on a pattern you thought rare is suspect).
7. Regenerate the **images** only of the touched cards (block 2) and rebuild the ISO.

Examples: Italian 116 -> **181** corrected cards (`rules_it.py`, global rules per error class + 7 per card); French 70.
Open questions to ask the user (do not decide alone): bring the card names to the official names of the language, character names (e.g. "Ragazza Mago Nero" / "Maga Nera").

## 3. Card images (block 2)

- Modules: `python tools/generate_language.py LANGUAGE PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]`: without IDs it regenerates everything
  (2,833 small + 2,833 large); with IDs only those, without atlas. Inside: attribute table with the words of the language, Spell/Trap label, deck thumbnail atlas
  (without it the deck shows the **English** names).
- **After every change to the card corrections** regenerate the touched images. For Italian: `sh tools/rebuild_corrections.sh USRDIR PACK_US PACK_MOD PYTHON`
  (181 cards -> 199 small + 199 large images, a few minutes). On Windows the script uses `python -I`: the packages in the *user site* (cv2) are not seen; pass as
  PYTHON a small wrapper that drops `-I` (`exec python "$@"`).
- Then copy the changed PNGs into the pack installed in PPSSPP and **restart PPSSPP** (texture cache). The hashes do not change: `textures.ini` stays the same.
- Typography of the language: French non-breaking space before `: ; ! ?` and « » quotation marks; German „ “; Spanish `¿ ¡`.

## 4. Story dialogues (block 3)

1. Extract: `python tools/audit/extract_dialogues.py ISO comparisons/audit_dialogues` (unique lines with English and Japanese).
2. Read **line by line comparing with English and Japanese**; the Japanese decides when English and the local language diverge. Note in
   `tools/data/dialogue_touchups_<l>.json`: `exact` {whole original line: new} and `parts` [[old, new]] (line breaks written `⏎`).
3. `python tools/corrections/build_dialogues.py <l>` -> `dialogue_corrections_<l>.json`. Lines without their own correction **inherit** from those with the same original text
   and the same Japanese (propagation to duplicates). The `parts` are applied **after** base and `exact`; the key of an `exact` is the text **before** the parts.
4. Automatic layout rules in `build_dialogues.py`: space after the `《...》` placeholders, French punctuation `! ? : ;`, three dots followed by a capital (`...Ciao` -> `... Ciao`, it only).
5. **Box constraints**: ~46 characters per line (the game does not wrap), maximum 3 lines; `apply_to_iso` warns ("N lines, it may not fit in the box"): check in game
   the reported ones. A placeholder counts ~6 characters.

**What to look for** (classes of error found in Italian, valid for all): English interjections left (`Oh my`), typos, apostrophes, `E'`, accents, time badly written (`7PM`),
inconsistent dormitory names, titles (`Cancelliere`/`Preside`), translations **censored or changed** compared with the Japanese (see below), sentences that lost their meaning or are missing, leftovers from another language.

**Choices common to all languages** (already taken, to be replicated in the new language: details and table in the register):
- scene `st01_t01/Scr003E`: Chumley's family has a **sake distillery**, the gift is **shochu** (not hot sauce); Syrus asks for the drawing of the Dark Magician Girl
  **in a maid outfit** (not a bikini) and hands over a **maid outfit** as a model. Lines #146-#197 apply, copies included (#150, #151);
- scene `st02_t01/Scr101E` lines 22-27: the original text is **rotated between the languages** (a game bug): put each one back in its own language;
- **speaker name** (e.g. "Doyen Sheppard"): it lives in the encrypted EBOOT, **not modifiable** in any language. In Italian the character is "Preside" in all the
  modifiable text; in French "Chancelier"/"Doyen" chosen dialogue by dialogue (formal/informal).

## 5. Duelist sentences (block 4)

These are the lines said during duels (`chr_wordstbl_<l>.bin` / `02chr_wordstbl_<l>.bin` inside ~70 `duel/cutin_*.ehp` archives...): ~34,000 entries but only **~1,800 unique per language**.

1. List to read: `python tools/audit/extract_duel_lines.py ISO LANGUAGE OUT.txt` (sentence with the corrections already applied + English next to it).
2. Read everything (6-7 blocks of ~280 lines). Do not touch what is **intended**: "pidgin" sentences of certain characters (it "Io pescare destino!", fr "Moi pioche, moi victoire !"),
   sound effects (`Screech!`), move names that English leaves in English (`Train Twister`), yawn/pain sounds.
3. Errors found (examples): missing final full stop in twin sentences (`Attivo una Magia Continua` + `.`), capital after `⏎` mid-sentence, imperative apostrophe (`Fa pure`->`Fa' pure`),
   duplicated articles (`una l'effetto`), badly built sentences (`non si è solo a una questione`), wrong translation of the meaning (`Tu es malin` for *You're cute* -> `mignon`),
   anglicisms (`Huh ?`->`Hein ?`), capitals (`Mon dieu`->`Mon Dieu`), elisions (`Je offre`->`J'offre`).
4. Add to `tools/data/duel_line_corrections_<l>.json`: `exact` (whole sentence, line breaks as `⏎`) or `parts` (replacement on every sentence). The `exact` entries are for **short** sentences where a `part`
   would also touch longer sentences (e.g. adding a final `.`); check with `apply_to_iso` that it prints **0 warnings** ("exact sentence never found" = wrong key).
5. **Crash**: the `*-ptrs.txt` files in the character archives contain absolute offsets; if a table grows they must be recomputed (`remap_pointers`, already done by `duel_lines.py`),
   otherwise the duel crashes. Do not write sentences with non-UTF-16 parts.

## 6. Long interface strings (block 5)

Tables `strTbl*`, help (`help_strtbl_*`), `ddstrtbl_<l>`, duelist biographies (`charalist`), records and goals (`duelrecord`/`result`), shop, laboratory, office menus.

1. Extract all the tables (same format `(n, 12, 12+4n)` + offsets + UTF-16 as `chr_wordstbl`; `duel_lines.read_table`/`write_table`) and group by archive/member; print `index | text || English`.
2. Read everything. Look for leftovers from other languages, labels that go out of the edge (`audit/long_labels.py`), terminology inconsistent with the cards.
3. Write `tools/corrections/string_rules_<l>.py`: `TABLES` (archives/members), `STRINGS` (per archive/member/0-based index, old->new; the old texts must appear exactly, real line breaks `\n` or `\r\n`),
   `GLOBALS` (regex, string replacement or callable). The `STRINGS` are applied **before** the `GLOBALS`.
4. `apply_to_iso.py` rewrites the archives at the end of the ISO and prints the warnings: they must be 0. Italian 505 strings in 15 archives; with all languages 941 in 25.
5. Consistency of terminology **among the three sources** (cards, dialogues, interface): e.g. in Italian "Segna-Mostro" (never "Gettone") in help, records and cards; "Preside Sheppard" in the card and in the dialogues.

## 7. Interface textures (blocks 6 and 7)

### 7.1 Before redrawing: which textures really have to be done
PPSSPP replaces a texture by the **hash of its pixels**. For every texture of the family, compute the hash in your language, in English and in Italian (`ui_textures/common.texture`, `gim.data_hash`):
- equal to **English** -> it is already covered by the base pack (MikeyMK);
- equal to **Italian** -> the `ui_it` version holds (if it contains text in the wrong language, that is a problem: check the image, not just the hash);
- otherwise **to be redrawn** in `ui_<l>`.

**Complete inventory**: `docs/TEXTURE_INVENTORY.md` (generated by `tools/analysis/texture_inventory_languages.py ISO OUT.md`) lists every texture of `ui_it` and `ui_fr` as NEUTRAL (copy and paste for all languages) or SPECIFIC (to be redone), with the languages that share the hash. Regenerate it if you add textures.

**Classifying the "Italian-only" textures** (work done for French): a texture present only in `ui_it` falls in two cases.
1. *Same hash in all languages* (recipe panels, `Side`/`Deck`/`Fusion Deck` tabs, empty bars, `card_side`, flags): it is neutral, the module of the new language gets it for free. It is enough to look at the image to make sure it contains no Italian words.
2. *Different hash per language*: in the original game the Italian version is written in Italian (`NUOVO`, icon `N`; the deck editor tab says **`Fusion`**, not `Fusione`: "Fusion Deck" is called that in all languages, an Italian error corrected on 2026-10-11), the French one **already has its own hash and its own HD** in `upscale_extra` (with `NEW`, `Fusion`).
   It is not a hole: it is the choice of the original. Redoing those with the local word (e.g. `NOUVEAU`/`N`, `NEU`/`N`, `NUEVO`/`N`) is **optional**: ask the user.

### 7.2 Families and procedure
The 8 families (`duel_texts`, `result_letters`, `menu_lists`, `icon_sheets`, `deck_screens`, `recipe_screens`, `vs_screen`, `tutorial`) and the recipe of each are in `docs/TUTORIAL.md` sec. 7.
Quality rules (from Italian): one font/weight/baseline/shadow per lettering, never letters deformed one by one; same area and same positions as the original (the game crops from fixed
rectangles); the texts are those of the language's original (only obvious errors are corrected); geometries **measured on the original**, never copied from Italian.
Tiles with split words: the cut goes in a gap between two letters. Accented capitals (É Ä Ö Ü Ñ): accent too high -> lower it or reduce the size down to -8% with `clip`.
Always rerun the **whole** family: `Family.finish()` replaces all the lines of the family in `<l>.ini`.

### 7.3 The duel number sheet (`card_icon03`) — recipe chosen by the user
A single sheet with LP, time and multipliers; script `tools/ui_textures/icon03_languages.py` (add the language to `LANGUAGES` and rerun with `--apply`):
- rows 0-180 (small digits, signs, orange keys 1/2/3, big digits 0-9 with "LP", small digits 0-9): **from the US pack**, crisp pixel art;
- the cells in which the European game differs from the US pack (black check mark, grey ball, empty pill, time word): **original game pixels enlarged 4x without smoothing**; the time
  word is the language's (TEMPO, TEMPS, TIME, ZEIT, TIEMPO); the orange pill ("Single" in the US) stays **empty**;
- rows >= 181 (multipliers x1...x12, icons, cards, arrows): from the Italian sheet already in the pack (`tools/data/card_icon03_base_it.png`);
- **beware of the bands**: the European cells are pasted only in their band of rows, otherwise the European pixels spoil the top of the big digits.

### 7.4 Title plate
`python tools/ui_textures/mystic_tomato_title.py LANGUAGE`: name of card 4930 in the language + "version" wording + flag. It lives only in the module of the chosen language.

## 8. Compose, install, test

1. `compose_pack.py` (base + modules) and `module_ini.py`; **one language at a time** for the tests (only one atlas/banner wins). After changing **a single PNG** it is enough to copy it into the installed pack and restart PPSSPP.
2. ISO for the tests: `_definitiva` (texts) + pack (textures). The game language is in the **save file**: use a **copy** of the user's save for the tests and delete it afterwards; never leave the test save in place of the real one.
3. Virtual joypad (`tools/extra_upscaling/pad.py`, `pw.py`, `dlg.py`): see `docs/TUTORIAL.md` sec. 10. Any key skips the opening movie; PPSSPP opens on the second monitor.
4. Screens to see: title, main menu, database, deck editor, recipes, shop, laboratory, calendar, PDA, VS, duel (HUD, Chain, direct attack, end of duel, rock-paper-scissors), tutorial,
   corrected dialogues (with the lines reported by the box check), a card with new text in the album and in the duel.

## 9. Recurring pitfalls (the most expensive)

- **Context that gets compacted**: write notes and rules to a file as you read; a list kept only "in your head" is lost.
- **Heredoc / `python -c`** with accents or backslashes corrupt files: use the write tool. After every change look for mojibake (`Ã`, `â€™`) in the json/py files.
- **Windows**: writes in text mode add `\r`; paths with spaces in quotation marks; `python -I` does not see the *user site*.
- **`apply_to_iso` with a single language** on the final ISO overwrites it: always pass all the languages.
- **A `part` that is too short** (e.g. adding a full stop) also touches the longer sentences that contain it: use `exact`.
- **Key of an `exact` = text before the `parts`**; the `parts` are applied in order.
- **Do not decide alone** official names, terminology or debatable translation choices: list and ask.

## 10. Documenting what changed compared with the original ISO (as for it and fr)

For every language a document `docs/CHANGES_<LANG>.md` must be produced, **generated from the real data**, not hand-written (models: `docs/CHANGES_IT.md`, `docs/CHANGES_FR.md`). To be done **after** building the `_definitiva` ISO and the pack, from the project root, with `L` = `de` or `es`:

```
ISO=PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso
DEF=PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR_definitiva.iso
python tools/analysis/document_changes.py $ISO $DEF L docs/changes_L   # byte-by-byte comparison original/definitive ISO -> CSV
python tools/analysis/text_comparisons.py L                                           # original -> new comparisons with highlighted words (md)
python tools/analysis/document_pack.py $ISO L docs/changes_L            # pack structure, every ui_L texture, regenerated cards, ini
python tools/analysis/write_changes_document.py L                                # composes docs/CHANGES_<LANG>.md
```

What it produces (in `docs/changes_L/`): `cards.csv`, `dialogues.csv`, `duel_lines.csv`, `ui_strings.csv`, `iso_images.csv`, `touched_files.csv`, `other.csv`, `summary.json` (ISO); `cards_diff.md`, `dialogues_diff.md`, `duel_lines_diff.md`, `ui_strings_diff.md` (readable comparisons with ~~removed~~ and **added**); `pack_structure.csv`, `ui_textures.csv`, `card_images.csv`, `ini_lines.csv`, `pack_summary.json` (pack).

Requirements: the language must have `tools/corrections/rules_L.py` (cards), `tools/data/dialogue_touchups_L.json`, `tools/data/duel_line_corrections_L.json`; `string_rules_L.py` and `ui_L` are optional (if missing the section is empty: the scripts do not stop). `write_changes_document.py` already knows it, fr, de, es, en; if a language-specific text is needed (list of the texts drawn in the texture families, editorial choices, state of the in-game tests) add the entry in the `FAM` dictionaries and in the C/D/F sections of the script.

**Part done by eye (not automatic).** The document of the **texts drawn in the textures** (`docs/changes_L/texture_texts_L.md`, models for it and fr) is not generated: there is no OCR on the PC. It is prepared this way: for every texture of `ui_L` the original of the ISO (enlarged 4x without smoothing) is placed next to the HD PNG in a comparison sheet (`python tools/analysis/texture_comparison_sheets.py ORIGINAL_ISO L OUT_DIR`: 6 textures per sheet, original on the left and HD on the right with file name and origin), the sheet is looked at and the text of each one is transcribed into a table, marking in **bold** every difference from the original (leftovers of other languages corrected, accents added, words changed). The letter tiles (`result_letters`) are compared letter by letter; the tiny cards in the tutorial maps are not legible at that scale and are taken as good because they come from the card data.

**When to regenerate**: after every correction of texts or textures; the numbers in the document must always match the ISO and the pack that are delivered. Always add `docs/CHANGES_<LANG>.md` to the files to check in the "done" checklist (sec. 11).

## 11. "Done" checklist for a language

- [ ] cards: all read, `rules_<l>.py`, `card_corrections_<l>.json`, images regenerated, seen in game on a card with new text;
- [ ] dialogues: read in full with English+Japanese, `dialogue_touchups_<l>.json`, box warnings checked in game, sake/maid scenes and `Scr101E` in place;
- [ ] duel sentences: read (1,800 unique), json, `apply_to_iso` with 0 warnings;
- [ ] UI strings: read in full, `string_rules_<l>.py`, 0 warnings;
- [ ] `ui_<l>` of the 8 families + `card_icon03` + plate; "Italian-only" textures classified (7.1);
- [ ] `_definitiva` ISO rebuilt with all the languages; pack composed; in-game test;
- [ ] `docs/CHANGES_<LANG>.md` generated (sec. 10) + `texture_texts_<l>.md` read by eye;
- [ ] `docs/EDITORIAL_CHOICES.md` (+ json), `docs/TUTORIAL.md` if the method changes, agent memory updated;
- [ ] Android `textures.zip` regenerated with the chosen language (or flagged as still to do).

## 12. Concrete examples (what was done, to get oriented)

| Block | Italian | French |
|---|---|---|
| Cards | 181 corrected (every card read; `rules_it.py`) | 70 corrected (`rules_fr.py`) |
| Dialogues | base ~1,380 proposals (2,176 lines with the duplicates) + 6 `exact` + 153 `parts` of re-reading | 16 `exact` + 178 `parts`; Doyen/Chancelier dialogue by dialogue |
| Duel sentences | 7 `exact` + 27 `parts` (all read, 1,792 unique) | 22 `exact` + 22 `parts` (all read, 1,832 unique) |
| UI strings | 505 strings in 15 archives (`string_rules_it.py`) | `string_rules_fr.py` (first language done) |
| Textures | base pack (the Italian texts are in the pack) | 85 + `card_icon03` in the module `modules/fr/ui_fr` |
| Peculiarities | Preside, Segna-Mostro, Slifer Rosso/Ra Giallo/Obelisk Blu, `NUOVO` and `N` as in the original | punctuation `! ? : ;`, `Mode aventure`, `TEMPS` |
