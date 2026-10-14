# Testi disegnati nelle texture tedesche: originale del gioco -> HD

Letti **a occhio** (2026-10-12): per ogni texture di `moduli/de/ui_de`, l'originale tedesco a bassa risoluzione della ISO (ingrandito 4x) accanto al PNG HD (fogli in `docs/changes_de/fogli/`, generati con `tools/analysis/texture_comparison_sheets.py ISO_ORIGINALE de OUT`). Non c'è un OCR sul PC: la tabella è trascritta guardando le immagini. L'HD riscrive le stesse parole dell'originale; in **grassetto** le differenze.

`scritte_duello` e `lettere_esito`: **fatte il 2026-10-13**. Prima erano date per "uguali all'inglese": errore, il gioco tedesco ha le sue tessere (DU GEWINNST, DU VERLIERST, UNENTSCHIEDEN, Ketten, Direkter Angriff!, NÄCHSTER SPIELER, DUELL BEGINNEN, SPIELZUG; hash diversi da quelli inglesi). Foglio `card_icon03`: parola del tempo ZEIT, cifre dal pack USA. Targa del titolo: MYSTISCHE TOMATE / EDITION.

| Texture (famiglia / file) | Testo nell'originale tedesco | Testo nell'HD | Differenza |
|---|---|---|---|
| lettere_esito / duel_win1000{02..18} | DU GEWINNST: 9 tessere D U G E W I N S T (N e S ripetute dal gioco), giallo | idem, lettere HD nello stile del pack inglese | nessuna |
| lettere_esito / duel_win100020 | sagoma sfocata "DU GEWINNST" (alone dietro la scritta) | idem, ingrandita 4x e levigata | nessuna |
| lettere_esito / duel_lose1000{02..18} | DU VERLIERST: 9 tessere D U V E R L I S T, viola/azzurro | idem | nessuna |
| lettere_esito / duel_draw1000{02..18} | UNENTSCHIEDEN: 9 tessere U N E T S C H I D, rosso | idem | nessuna |
| scritte_duello / chain010005, chain010003 | Ketten (colorato + bagliore grigio) | idem | nessuna |
| scritte_duello / dilect_atk00001, 00003 | Direkter Angriff! (+ bagliore) | idem | nessuna |
| scritte_duello / next_player0003+0002 (blu), 0007+0006 (rosso) | NÄCHSTER SPIELER su 2 texture (il taglio passa dentro la L, come nell'originale) | idem | nessuna |
| scritte_duello / next_player0001, 0005 | i due puntini della Ä (sprite a parte, che il gioco mette sopra la A) | idem, ingranditi 4x e centrati sopra la nostra A | posizione: spostati in orizzontale per seguire la A del nuovo tipo di carattere |
| scritte_duello / start_duel10002+10001, 10005 | DUELL BEGINNEN su 2 texture + bagliore | idem | nessuna |
| scritte_duello / score-top100011, 100013 | SPIELZUG (badge blu e rosso, il numero lo scrive il gioco) | idem | nessuna |
| fogli_icone / all_g__icon04 | foglio di icone: 1~4, 5,6, 7~, ALLE, kom!, NEU, Me in Labor (sillabe), Fusion/Side/Deck | idem (pixel dell'originale ingranditi 4x dove differiscono dall'inglese) | nessuna |
| fogli_icone / all_g__panel | frammento di linguetta "…ypen" (da "Kartentypen") | "ypen" | nessuna (è un frammento, come nell'originale) |
| fogli_icone / all_g__s_pack | AUSVERKAUFT, DP | AUSVERKAUFT, DP | nessuna (parola compressa per entrare nella casella, come l'originale) |
| menu_liste / always_bri_ger__story_sys02 | Sonntag, Montag, Dienstag, Mittwoch, Donnerstag, Freitag, Samstag · Mai, Juni, Juli, August · "Tage / bis zum Turnier" · Vormittag, Nachmittag · "." (data) | idem | nessuna |
| menu_liste / result_g__menu01 | GEWONNEN · UNENTSCHIEDEN · VERLOREN | idem | nessuna |
| menu_liste / result_g__menu02 | DUELLERGEBNIS · DUELLBONUS · NEW HIGH SCORE BONUS · CHALLENGE COMPLETE BONUS · ZWISCHENSTAND · ERGEBNIS | idem | nessuna (le due righe inglesi sono inglesi anche nell'originale tedesco e nelle stringhe del gioco) |
| menu_liste / title_menu_g__m_menu_title01 | HAUPTMENÜ · NAMEN EINGEBEN · HERUNTERLADENE KARTENLISTE · DUELLRÄTSEL · OPTIONEN · SPRACHEINSTELLUNGEN | idem | nessuna |
| menu_liste / title_menu_g__press_start0003 | START-TASTE DRÜCKEN | idem | nessuna |
| menu_liste / title_menu_g__trnsmt02 | GRUPPENLISTE · NEUE GRUPPE ERSTELLEN · EINGANGSLISTE · DUELL · **ÉCHANGE** · REZEPT SENDEN · KARTEN SENDEN · DUELLRÄTSEL SENDEN · FREIES DUELL · NORMALES DUELL · TAG-DUELL | stesse righe, ma **TAUSCHEN** | residuo francese dell'originale corretto (come `tushin_msg`: "Tauschen") |
| schede_deck / d_window00008, 00062, conv_machine__window_g0016 | Truhe | Truhe | nessuna |
| schede_deck / d_window00016 | Fusion | Fusion | nessuna (stessa parola dell'inglese; prima era solo un upscale automatico, ora HD) |
| schede_deck / d_window00033 | Eigene Kartentypen (+ START, ?) | idem | nessuna |
| schede_deck / d_window00051, 00101, rental__window_g0008, g0026 | Miete | Miete | nessuna |
| schede_deck / tab_title | Gekaufte Karten · Gekaufte Kartenty(pen) (frammento al bordo) | idem | nessuna |
| schede_deck / conv_machine__window_g0009, g0026 | Konverter | Konverter | nessuna |
| schede_deck / password__key_g0027 | EINGABE | EINGABE | nessuna |
| schede_deck / rental__window_g0015 | Labor | Labor | nessuna |
| schede_ricette / limitlist__window_g0002, 0004, 0012 | Limitiert · Halblimitiert · Verboten | idem | nessuna |
| schede_ricette / recipe_view_g__recipe010004 | Fusionsdeck | Fusionsdeck | nessuna |
| schede_ricette / recipe_view_g__recipe010008 | Charakter | Charakter | nessuna |
| schede_ricette / recipe_view_g__recipe010015 | Benutzer | Benutzer | nessuna |
| schede_ricette / recipe_view_g__recipe010027 | Heruntergeladene | Heruntergeladene | nessuna |
| schede_ricette / recipe_view_g__recipe010029, title_menu_g__recipe_sel00033 | Charakterrezepte | Charakterrezepte | nessuna |
| schede_ricette / recipe_view_g__recipe010031 | Benutzerrezepte | Benutzerrezepte | nessuna |
| schede_ricette / title_menu_g__t_window0008, 0026 | **Échange** | **Tauschen** | residuo francese dell'originale corretto |
| schermata_vs / jyanken20_g0005, 0007 | ZWEITER · ERSTER | idem | nessuna |
| schermata_vs / vs_much1..3_g0001 | 1. Runde · 2. Runde · 3. Runde | idem | nessuna |
| schermata_vs / vs_bg01_1_g0005, g0012 (bagliori) | NORMALES DUELL · TAG-DUELL | idem | nessuna |
| schermata_vs / vs_bg01_1_g0007, g0008, g0014 | DUELL · NORMALES · TAG- | idem | nessuna |
| schermata_vs / vs_bg01_2_g0001, g0004 | Einzelmodus · Matchmodus | idem | nessuna |
| schermata_vs / jnk_card01 | GEWONNEN · VERLOREN · UNENTSCHIEDEN (sotto i 3+3 tasti) | idem | nessuna |
| schermata_vs / d_menu01_g | SPIELER 1 · SPIELER 2 (4 distintivi) · linguetta SPIELER · distintivi 1-4 | idem | nessuna |
| tutorial / tuto_duelimg01 | "Dein Gegner hat den Kampf eröffnet. / Effekt der Karte aktivieren?" · JA · NEIN | idem | nessuna |
| tutorial / tuto_duelimg02 | carta "Schwarzer Anhänger" (Zauberkarte, equip) | idem, testo della carta dal `cardinfo_ger` corretto | testo della descrizione ora quello corretto delle carte |
| tutorial / tuto_duelimg03 | carta "Gelb-glänzender Schild" (Dauerzauberkarte) | idem | come sopra |
| tutorial / tuto_duelimg04 | carta "Sieben Werkzeuge des Banditen" (Fallenkarte, contro) | idem | come sopra |
| tutorial / tuto_duelimg05 | carta **"Zusammenbruch"** (Schnellzauberkarte) | **"Schrumpfen"** | nome ufficiale della carta (come nel database e nei tutorial: l'originale usava un nome diverso nell'immagine) |
| tutorial / tuto_duelimg06 | carta "Umi" (Spielfeldzauberkarte) | idem | come sopra |

Non rifatte (restano l'upscale del pack, parola diversa dall'inglese di pochi pixel): `pda_pack01`, `icon06_g`, `mein_menu00`, `trnsmt01`, `duelrecord parts_g` ("NEU"/"N" al posto di "NEW"): domanda aperta n. 7 in `open_questions_de.md`.
