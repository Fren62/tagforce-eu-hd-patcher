# Texts drawn in the German textures: game original -> HD

Read **by eye** (2026-10-12): for every texture of `modules/de/ui_de`, the low-resolution German original of the ISO (enlarged 4x) next to the HD PNG (sheets in `docs/changes_de/sheets/`, generated with `tools/analysis/texture_comparison_sheets.py ORIGINAL_ISO de OUT`). There is no OCR on the PC: the table is transcribed by looking at the images. The HD rewrites the same words as the original; differences in **bold**.

`duel_texts` e `result_letters`: **done on 2026-10-13**. Before, they were taken as "equal to English": a mistake, the German game has its own tiles (DU GEWINNST, DU VERLIERST, UNENTSCHIEDEN, Ketten, Direkter Angriff!, NÄCHSTER SPIELER, DUELL BEGINNEN, SPIELZUG; hashes different from the English ones). `card_icon03` sheet: time word ZEIT, digits from the US pack. Title plate: MYSTISCHE TOMATE / EDITION.

| Texture (family / file) | Text in the German original | Text in the HD | Difference |
|---|---|---|---|
| result_letters / duel_win1000{02..18} | DU GEWINNST: 9 tiles D U G E W I N S T (N and S repeated by the game), yellow | same, HD letters in the style of the English pack | none |
| result_letters / duel_win100020 | blurred silhouette "DU GEWINNST" (halo behind the lettering) | same, enlarged 4x and smoothed | none |
| result_letters / duel_lose1000{02..18} | DU VERLIERST: 9 tiles D U V E R L I S T, viola/azzurro | same | none |
| result_letters / duel_draw1000{02..18} | UNENTSCHIEDEN: 9 tiles U N E T S C H I D, red | same | none |
| duel_texts / chain010005, chain010003 | Ketten (colored + grey glow) | same | none |
| duel_texts / dilect_atk00001, 00003 | Direkter Angriff! (+ glow) | same | none |
| duel_texts / next_player0003+0002 (blue), 0007+0006 (red) | NÄCHSTER SPIELER over 2 textures (the cut passes inside the L, as in the original) | same | none |
| duel_texts / next_player0001, 0005 | the two dots of the Ä (a separate sprite, which the game puts over the A) | same, enlarged 4x and centred over our A | position: shifted horizontally to follow the A of the new typeface |
| duel_texts / start_duel10002+10001, 10005 | DUELL BEGINNEN over 2 textures + glow | same | none |
| duel_texts / score-top100011, 100013 | SPIELZUG (badge blue and red, the number is written by the game) | same | none |
| icon_sheets / all_g__icon04 | icon sheet: 1~4, 5,6, 7~, ALLE, kom!, NEU, Me in Labor (syllables), Fusion/Side/Deck | same (original pixels enlarged 4x where they differ from English) | none |
| icon_sheets / all_g__panel | tab fragment "…ypen" (from "Kartentypen") | "ypen" | none (it is a fragment, as in the original) |
| icon_sheets / all_g__s_pack | AUSVERKAUFT, DP | AUSVERKAUFT, DP | none (word compressed to fit the box, like the original) |
| menu_lists / always_bri_ger__story_sys02 | Sonntag, Montag, Dienstag, Mittwoch, Donnerstag, Freitag, Samstag · Mai, Juni, Juli, August · "Tage / bis zum Turnier" · Vormittag, Nachmittag · "." (data) | same | none |
| menu_lists / result_g__menu01 | GEWONNEN · UNENTSCHIEDEN · VERLOREN | same | none |
| menu_lists / result_g__menu02 | DUELLERGEBNIS · DUELLBONUS · NEW HIGH SCORE BONUS · CHALLENGE COMPLETE BONUS · ZWISCHENSTAND · ERGEBNIS | same | none (the two English lines are English also in the German original and in the game strings) |
| menu_lists / title_menu_g__m_menu_title01 | HAUPTMENÜ · NAMEN EINGEBEN · HERUNTERLADENE KARTENLISTE · DUELLRÄTSEL · OPTIONEN · SPRACHEINSTELLUNGEN | same | none |
| menu_lists / title_menu_g__press_start0003 | START-TASTE DRÜCKEN | same | none |
| menu_lists / title_menu_g__trnsmt02 | GRUPPENLISTE · NEUE GRUPPE ERSTELLEN · EINGANGSLISTE · DUELL · **ÉCHANGE** · REZEPT SENDEN · KARTEN SENDEN · DUELLRÄTSEL SENDEN · FREIES DUELL · NORMALES DUELL · TAG-DUELL | same lines, but **TAUSCHEN** | French leftover of the original, corrected (come `tushin_msg`: "Tauschen") |
| deck_screens / d_window00008, 00062, conv_machine__window_g0016 | Truhe | Truhe | none |
| deck_screens / d_window00016 | Fusion | Fusion | none (same word as English; before it was just an automatic upscale, now HD) |
| deck_screens / d_window00033 | Eigene Kartentypen (+ START, ?) | same | none |
| deck_screens / d_window00051, 00101, rental__window_g0008, g0026 | Miete | Miete | none |
| deck_screens / tab_title | Gekaufte Karten · Gekaufte Kartenty(pen) (fragment at the edge) | same | none |
| deck_screens / conv_machine__window_g0009, g0026 | Konverter | Konverter | none |
| deck_screens / password__key_g0027 | EINGABE | EINGABE | none |
| deck_screens / rental__window_g0015 | Labor | Labor | none |
| recipe_screens / limitlist__window_g0002, 0004, 0012 | Limitiert · Halblimitiert · Verboten | same | none |
| recipe_screens / recipe_view_g__recipe010004 | Fusionsdeck | Fusionsdeck | none |
| recipe_screens / recipe_view_g__recipe010008 | Charakter | Charakter | none |
| recipe_screens / recipe_view_g__recipe010015 | Benutzer | Benutzer | none |
| recipe_screens / recipe_view_g__recipe010027 | Heruntergeladene | Heruntergeladene | none |
| recipe_screens / recipe_view_g__recipe010029, title_menu_g__recipe_sel00033 | Charakterrezepte | Charakterrezepte | none |
| recipe_screens / recipe_view_g__recipe010031 | Benutzerrezepte | Benutzerrezepte | none |
| recipe_screens / title_menu_g__t_window0008, 0026 | **Échange** | **Tauschen** | French leftover of the original, corrected |
| vs_screen / jyanken20_g0005, 0007 | ZWEITER · ERSTER | same | none |
| vs_screen / vs_much1..3_g0001 | 1. Runde · 2. Runde · 3. Runde | same | none |
| vs_screen / vs_bg01_1_g0005, g0012 (glows) | NORMALES DUELL · TAG-DUELL | same | none |
| vs_screen / vs_bg01_1_g0007, g0008, g0014 | DUELL · NORMALES · TAG- | same | none |
| vs_screen / vs_bg01_2_g0001, g0004 | Einzelmodus · Matchmodus | same | none |
| vs_screen / jnk_card01 | GEWONNEN · VERLOREN · UNENTSCHIEDEN (sotto i 3+3 tasti) | same | none |
| vs_screen / d_menu01_g | SPIELER 1 · SPIELER 2 (4 badges) · linguetta SPIELER · badges 1-4 | same | none |
| tutorial / tuto_duelimg01 | "Dein Gegner hat den Kampf eröffnet. / Effekt der Karte aktivieren?" · JA · NEIN | same | none |
| tutorial / tuto_duelimg02 | card "Schwarzer Anhänger" (Spell Card, equip) | same, card text from the corrected `cardinfo_ger` | the description text is now the corrected one of the cards |
| tutorial / tuto_duelimg03 | card "Gelb-glänzender Schild" (Continuous Spell Card) | same | as above |
| tutorial / tuto_duelimg04 | card "Sieben Werkzeuge des Banditen" (Trap Card, counter) | same | as above |
| tutorial / tuto_duelimg05 | card **"Zusammenbruch"** (Quick-Play Spell Card) | **"Schrumpfen"** | official card name (as in the database and in the tutorials: the original used a different name in the image) |
| tutorial / tuto_duelimg06 | card "Umi" (Field Spell Card) | same | as above |

Not redone (they stay the pack's upscale, word differing from English by a few pixels): `pda_pack01`, `icon06_g`, `mein_menu00`, `trnsmt01`, `duelrecord parts_g` ("NEU"/"N" instead of "NEW"): open question no. 7 in `open_questions_de.md`.
