# Inventario texture: neutre / specifiche per lingua

Generato da `strumenti/analisi/inventario_texture_lingue.py`. **NEUTRA** = lo stesso hash compare in piu' lingue (de/es incluse): il PNG si copia tale e quale nel modulo della nuova lingua (e di norma e' gia' nel pack di base). **SPECIFICA** = l'originale e' diverso per lingua: va rifatta con le parole della lingua, prendendo `ui_it`/`ui_fr` come riferimento.

**Come usarlo per una nuova lingua (es, de).**
- **NEUTRA** (11 in `ui_it`): stesso hash in e/f/g/i/s. Nessun lavoro: il PNG vale gia' per tutte le lingue (e' nel pack di base, il modulo non deve rifarlo). Basta guardare che l'immagine non contenga parole di una lingua.
- **SPECIFICA** (94 in `ui_it`, 85 in `ui_fr`): l'originale cambia per lingua. Per la nuova lingua calcola l'hash della *sua* texture (`ui_it/common.texture`): se coincide con quello dell'inglese o con uno gia' coperto, non serve rifarla; altrimenti va ridisegnata con le parole della lingua, usando il PNG `ui_it` e `ui_fr` come riferimento di stile e di geometria (ma **misura sempre sull'originale**).
- Casi limite gia' noti: `recipe010004` e `duel_draw100014` risultano specifiche perche' non compaiono in tutte e 5 le lingue (controlla le tue); le 6 "wording locale" (`NUOVO`/`N`/`Fusion`, `pda_pack01`, `icon06`, `mein_menu00`, `trnsmt01`, `d_window00016`, `parts`) sono specifiche: l'originale di ogni lingua ha gia' il suo HD nel pack.
- Le 8 righe `*.ini` che compaiono come "hash non trovato" non sono texture e sono state escluse.

## ui_it ({'SPECIFICA': 94, 'NEUTRA': 11})

| file | hash | tipo | dove |
|---|---|---|---|
| ui_it/fogli_icone/cardalbum__ocglist_i.png | 295c8b9c | NEUTRA | lingue col stesso hash: efgis - all_e.ehp:ocglist.gim, all_f.ehp:ocglist.gim |
| ui_it/schede_deck/all_i__d_window00024.png | fd0f9c3b | NEUTRA | lingue col stesso hash: efgis - all_e.ehp:d_window00024.gim, all_f.ehp:d_window00024.gim |
| ui_it/schede_deck/all_i__d_window00031.png | b77db24b | NEUTRA | lingue col stesso hash: efgis - all_e.ehp:d_window00031.gim, all_f.ehp:d_window00031.gim |
| ui_it/schede_deck/all_i__d_window00034.png | 1659d75e | NEUTRA | lingue col stesso hash: efgis - all_e.ehp:d_window00034.gim, all_f.ehp:d_window00034.gim |
| ui_it/schede_deck/all_i__d_window00120.png | 4556da1f | NEUTRA | lingue col stesso hash: efgis - all_e.ehp:d_window00120.gim, all_f.ehp:d_window00120.gim |
| ui_it/schede_deck/conv_machine__window_i0022.png | ada2c664 | NEUTRA | lingue col stesso hash: fgis - conv_machine.ehp:window_f0022.gim, conv_machine.ehp:window_g0022.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010002.png | 763a4766 | NEUTRA | lingue col stesso hash: efgis - recipe_view_e.ehp:recipe010002.gim, recipe_view_f.ehp:recipe010002.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010006.png | 44c8b170 | NEUTRA | lingue col stesso hash: efgis - recipe_view_e.ehp:recipe010006.gim, recipe_view_f.ehp:recipe010006.gim |
| ui_it/schede_ricette/title_menu_i__dmenu_recipe.png | e1ba3fc9 | NEUTRA | lingue col stesso hash: efgis - title_menu_e.ehp:dmenu_recipe.gim, title_menu_f.ehp:dmenu_recipe.gim |
| ui_it/schede_ricette/title_menu_i__recipe_panel.png | 35c103aa | NEUTRA | lingue col stesso hash: efgis - title_menu_e.ehp:recipe_panel.gim, title_menu_f.ehp:recipe_panel.gim |
| ui_it/scritte_duello/basic_ii__card_side.png | dfbaa424 | NEUTRA | lingue col stesso hash: efgis - basic_be.ehp:card_side.gim, basic_bf.ehp:card_side.gim |
| ui_it/fogli_icone/all_i__icon04.png | 0f47adc6 | SPECIFICA | lingue col stesso hash: i - all_i.ehp:icon04.gim |
| ui_it/fogli_icone/all_i__panel.png | 51288b63 | SPECIFICA | lingue col stesso hash: i - all_i.ehp:panel.gim |
| ui_it/fogli_icone/all_i__s_pack.png | 5f349a93 | SPECIFICA | lingue col stesso hash: i - all_i.ehp:s_pack.gim |
| ui_it/fogli_icone/always_bri_ita__pda_pack01.png | e5169419 | SPECIFICA | lingue col stesso hash: i - always_bri_ita.ehp:pda_pack01.gim, always_fra_ita.ehp:pda_pack01.gim |
| ui_it/fogli_icone/cardalbum__icon06_i.png | aaef4267 | SPECIFICA | lingue col stesso hash: i - all_i.ehp:icon06.gim, always_bri_ita.ehp:card_icon06.gim |
| ui_it/fogli_icone/title_menu_i__mein_menu00.png | 22692070 | SPECIFICA | lingue col stesso hash: i - title_menu_i.ehp:mein_menu00.gim |
| ui_it/fogli_icone/title_menu_i__trnsmt01.png | bdc35d0d | SPECIFICA | lingue col stesso hash: i - title_menu_i.ehp:trnsmt01.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100002.png | 60e58b0c | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_draw100002.gim, basic_fi.ehp:duel_draw100002.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100004.png | ce971331 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_draw100004.gim, basic_fi.ehp:duel_draw100004.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100006.png | d2e20c6c | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_draw100006.gim, basic_fi.ehp:duel_draw100006.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100008.png | 1deeba15 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_draw100008.gim, basic_fi.ehp:duel_draw100008.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100010.png | 9a3bba37 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_draw100010.gim, basic_fi.ehp:duel_draw100010.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100012.png | f869c721 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_draw100012.gim, basic_fi.ehp:duel_draw100012.gim |
| ui_it/lettere_esito/basic_ii__duel_draw100014.png | 3d00ca65 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_draw100014.gim, basic_fi.ehp:duel_draw100014.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100002.png | 23e6f72d | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_lose100002.gim, basic_fi.ehp:duel_lose100002.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100004.png | aa67eb3a | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_lose100004.gim, basic_fi.ehp:duel_lose100004.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100006.png | 0b9f2dfd | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_lose100006.gim, basic_fi.ehp:duel_lose100006.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100008.png | 8c1ca0ea | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_lose100008.gim, basic_fi.ehp:duel_lose100008.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100010.png | f7a3a889 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_lose100010.gim, basic_fi.ehp:duel_lose100010.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100012.png | a3668e35 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_lose100012.gim, basic_fi.ehp:duel_lose100012.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100014.png | be8d27c2 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_lose100014.gim, basic_fi.ehp:duel_lose100014.gim |
| ui_it/lettere_esito/basic_ii__duel_lose100016.png | 48fccb29 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_lose100016.gim, basic_fi.ehp:duel_lose100016.gim |
| ui_it/lettere_esito/basic_ii__duel_win100002.png | 00b45490 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_win100002.gim, basic_fi.ehp:duel_win100002.gim |
| ui_it/lettere_esito/basic_ii__duel_win100004.png | d38eeaf8 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_win100004.gim, basic_fi.ehp:duel_win100004.gim |
| ui_it/lettere_esito/basic_ii__duel_win100006.png | 64e53c06 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_win100006.gim, basic_fi.ehp:duel_win100006.gim |
| ui_it/lettere_esito/basic_ii__duel_win100008.png | 6cb385d2 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_win100008.gim, basic_fi.ehp:duel_win100008.gim |
| ui_it/lettere_esito/basic_ii__duel_win100010.png | ed0059c9 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_win100010.gim, basic_fi.ehp:duel_win100010.gim |
| ui_it/lettere_esito/basic_ii__duel_win100012.png | 8be1d58a | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_win100012.gim, basic_fi.ehp:duel_win100012.gim |
| ui_it/lettere_esito/basic_ii__duel_win100014.png | 145d1dd3 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_win100014.gim, basic_fi.ehp:duel_win100014.gim |
| ui_it/lettere_esito/basic_ii__duel_win100016.png | 736cf75e | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:duel_win100016.gim, basic_fi.ehp:duel_win100016.gim |
| ui_it/menu_liste/always_bri_ita__story_sys02.png | 5fc07dd2 | SPECIFICA | lingue col stesso hash: i - always_bri_ita.ehp:story_sys02.gim, always_fra_ita.ehp:story_sys02.gim |
| ui_it/menu_liste/result_i__menu01.png | 23b37425 | SPECIFICA | lingue col stesso hash: i - result_i.ehp:menu01.gim |
| ui_it/menu_liste/result_i__menu02.png | aeddb824 | SPECIFICA | lingue col stesso hash: i - result_i.ehp:menu02.gim |
| ui_it/menu_liste/title_menu_i__m_menu_title01.png | cfe8de2a | SPECIFICA | lingue col stesso hash: i - title_menu_i.ehp:m_menu_title01.gim |
| ui_it/menu_liste/title_menu_i__press_start0003.png | 747668a4 | SPECIFICA | lingue col stesso hash: i - title_menu_i.ehp:press_start0003.gim |
| ui_it/menu_liste/title_menu_i__trnsmt02.png | 7f3a4012 | SPECIFICA | lingue col stesso hash: i - title_menu_i.ehp:trnsmt02.gim |
| ui_it/schede_deck/all_i__d_window00008.png | e6b24eae | SPECIFICA | lingue col stesso hash: i - all_i.ehp:d_window00008.gim |
| ui_it/schede_deck/all_i__d_window00016.png | 27153d30 | SPECIFICA | lingue col stesso hash: i - all_i.ehp:d_window00016.gim |
| ui_it/schede_deck/all_i__d_window00033.png | 339f25bd | SPECIFICA | lingue col stesso hash: i - all_i.ehp:d_window00033.gim |
| ui_it/schede_deck/all_i__d_window00051.png | cefa3d7e | SPECIFICA | lingue col stesso hash: i - all_i.ehp:d_window00051.gim |
| ui_it/schede_deck/all_i__d_window00062.png | f5fd73f9 | SPECIFICA | lingue col stesso hash: i - all_i.ehp:d_window00062.gim, conv_machine.ehp:window_i0016.gim |
| ui_it/schede_deck/all_i__d_window00101.png | 22ebca63 | SPECIFICA | lingue col stesso hash: i - all_i.ehp:d_window00101.gim, rental.ehp:window_i0008.gim |
| ui_it/schede_deck/all_i__tab_title.png | 6852c8c2 | SPECIFICA | lingue col stesso hash: i - all_i.ehp:tab_title.gim |
| ui_it/schede_deck/conv_machine__window_i0009.png | 6ca9eba7 | SPECIFICA | lingue col stesso hash: i - conv_machine.ehp:window_i0009.gim, conv_machine.ehp:window_i0026.gim |
| ui_it/schede_deck/password__key_i0027.png | 37603c6b | SPECIFICA | lingue col stesso hash: i - password.ehp:key_i0027.gim |
| ui_it/schede_deck/rental__window_i0015.png | fee49520 | SPECIFICA | lingue col stesso hash: is - rental.ehp:window_i0015.gim, rental.ehp:window_s0015.gim |
| ui_it/schede_deck/rental__window_i0026.png | d4ea2e3a | SPECIFICA | lingue col stesso hash: i - rental.ehp:window_i0026.gim |
| ui_it/schede_ricette/duelrecord__parts_i.png | 4e51e475 | SPECIFICA | lingue col stesso hash: i - duelrecord.ehp:parts_i.gim |
| ui_it/schede_ricette/limitlist__window_i0002.png | 6c94dcad | SPECIFICA | lingue col stesso hash: i - limitlist.ehp:window_i0002.gim |
| ui_it/schede_ricette/limitlist__window_i0004.png | 9acba8ec | SPECIFICA | lingue col stesso hash: i - limitlist.ehp:window_i0004.gim |
| ui_it/schede_ricette/limitlist__window_i0012.png | 5c0e1d7a | SPECIFICA | lingue col stesso hash: i - limitlist.ehp:window_i0012.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010004.png | b2427f09 | SPECIFICA | lingue col stesso hash: efi - recipe_view_e.ehp:recipe010004.gim, recipe_view_f.ehp:recipe010004.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010008.png | 9b52cd0c | SPECIFICA | lingue col stesso hash: i - recipe_view_i.ehp:recipe010008.gim, title_menu_i.ehp:recipe_sel00002.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010015.png | 9d53d71b | SPECIFICA | lingue col stesso hash: i - recipe_view_i.ehp:recipe010015.gim, title_menu_i.ehp:recipe_sel00009.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010027.png | eb6d8202 | SPECIFICA | lingue col stesso hash: i - recipe_view_i.ehp:recipe010027.gim, title_menu_i.ehp:recipe_sel00020.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010029.png | 29e9a88e | SPECIFICA | lingue col stesso hash: i - recipe_view_i.ehp:recipe010029.gim, title_menu_i.ehp:recipe_sel00022.gim |
| ui_it/schede_ricette/recipe_view_i__recipe010031.png | 4ceb96c4 | SPECIFICA | lingue col stesso hash: i - recipe_view_i.ehp:recipe010031.gim, title_menu_i.ehp:recipe_sel00024.gim |
| ui_it/schede_ricette/title_menu_i__recipe_sel00033.png | 13e83af2 | SPECIFICA | lingue col stesso hash: i - title_menu_i.ehp:recipe_sel00033.gim |
| ui_it/schede_ricette/title_menu_i__t_window0008.png | edf9b615 | SPECIFICA | lingue col stesso hash: i - title_menu_i.ehp:t_window0008.gim |
| ui_it/schede_ricette/title_menu_i__t_window0026.png | 50bfc4e3 | SPECIFICA | lingue col stesso hash: i - title_menu_i.ehp:t_window0026.gim |
| ui_it/schermata_vs/start_all__jyanken20_i0005.png | 84daf8b2 | SPECIFICA | lingue col stesso hash: i - start_all.ehp:jyanken20_i0005.gim, start_e.ehp:jyanken20_i0005.gim |
| ui_it/schermata_vs/start_all__jyanken20_i0007.png | f5bbbb53 | SPECIFICA | lingue col stesso hash: i - start_all.ehp:jyanken20_i0007.gim, start_e.ehp:jyanken20_i0007.gim |
| ui_it/schermata_vs/start_all__vs_much1_i0001.png | a50e57e6 | SPECIFICA | lingue col stesso hash: i - start_all.ehp:vs_much1_i0001.gim, start_e.ehp:vs_much1_i0001.gim |
| ui_it/schermata_vs/start_all__vs_much2_i0001.png | 8f118f8a | SPECIFICA | lingue col stesso hash: i - start_all.ehp:vs_much2_i0001.gim, start_e.ehp:vs_much2_i0001.gim |
| ui_it/schermata_vs/start_all__vs_much3_i0001.png | ae083f33 | SPECIFICA | lingue col stesso hash: i - start_all.ehp:vs_much3_i0001.gim, start_e.ehp:vs_much3_i0001.gim |
| ui_it/schermata_vs/start_e__d_menu01_i.png | f098096b | SPECIFICA | lingue col stesso hash: i - start_e.ehp:d_menu01_i.gim, start_f.ehp:d_menu01_i.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0005.png | 50201760 | SPECIFICA | lingue col stesso hash: i - start_e.ehp:vs_bg01_1_i0005.gim, start_f.ehp:vs_bg01_1_i0005.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0007.png | 92f2114b | SPECIFICA | lingue col stesso hash: i - start_e.ehp:vs_bg01_1_i0007.gim, start_f.ehp:vs_bg01_1_i0007.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0008.png | 5fb4b6dc | SPECIFICA | lingue col stesso hash: i - start_e.ehp:vs_bg01_1_i0008.gim, start_f.ehp:vs_bg01_1_i0008.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0012.png | 01c81cd4 | SPECIFICA | lingue col stesso hash: i - start_e.ehp:vs_bg01_1_i0012.gim, start_f.ehp:vs_bg01_1_i0012.gim |
| ui_it/schermata_vs/start_e__vs_bg01_1_i0014.png | 413ccf1d | SPECIFICA | lingue col stesso hash: i - start_e.ehp:vs_bg01_1_i0014.gim, start_f.ehp:vs_bg01_1_i0014.gim |
| ui_it/schermata_vs/start_e__vs_bg01_2_i0001.png | 005ca7af | SPECIFICA | lingue col stesso hash: i - start_e.ehp:vs_bg01_2_i0001.gim, start_f.ehp:vs_bg01_2_i0001.gim |
| ui_it/schermata_vs/start_e__vs_bg01_2_i0004.png | 6b0b0fbd | SPECIFICA | lingue col stesso hash: i - start_e.ehp:vs_bg01_2_i0004.gim, start_f.ehp:vs_bg01_2_i0004.gim |
| ui_it/schermata_vs/start_i__jnk_card01.png | 38e5ae61 | SPECIFICA | lingue col stesso hash: i - start_i.ehp:jnk_card01.gim |
| ui_it/scritte_duello/basic_ii__card_icon03.png | 376925c7 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:card_icon03.gim, basic_fi.ehp:card_icon03.gim |
| ui_it/scritte_duello/basic_ii__chain010003.png | 235b1041 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:chain010003.gim, basic_fi.ehp:chain010003.gim |
| ui_it/scritte_duello/basic_ii__chain010005.png | 79b7261f | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:chain010005.gim, basic_fi.ehp:chain010005.gim |
| ui_it/scritte_duello/basic_ii__dilect_atk00001.png | ba952e24 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:dilect_atk00001.gim, basic_fi.ehp:dilect_atk00001.gim |
| ui_it/scritte_duello/basic_ii__dilect_atk00003.png | 58789f5c | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:dilect_atk00003.gim, basic_fi.ehp:dilect_atk00003.gim |
| ui_it/scritte_duello/basic_ii__next_player0001.png | 8abf9d52 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:next_player0001.gim, basic_fi.ehp:next_player0001.gim |
| ui_it/scritte_duello/basic_ii__next_player0002.png | 6bc72dfe | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:next_player0002.gim, basic_fi.ehp:next_player0002.gim |
| ui_it/scritte_duello/basic_ii__next_player0004.png | 8a774ddd | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:next_player0004.gim, basic_fi.ehp:next_player0004.gim |
| ui_it/scritte_duello/basic_ii__next_player0005.png | 83cf47f4 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:next_player0005.gim, basic_fi.ehp:next_player0005.gim |
| ui_it/scritte_duello/basic_ii__score-top100011.png | 36655dfa | SPECIFICA | lingue col stesso hash: is - basic_bi.ehp:score-top100011.gim, basic_bs.ehp:score-top100011.gim |
| ui_it/scritte_duello/basic_ii__score-top100013.png | 97d1b9a7 | SPECIFICA | lingue col stesso hash: is - basic_bi.ehp:score-top100013.gim, basic_bs.ehp:score-top100013.gim |
| ui_it/scritte_duello/basic_ii__start_duel10001.png | faf5cb43 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:start_duel10001.gim, basic_fi.ehp:start_duel10001.gim |
| ui_it/scritte_duello/basic_ii__start_duel10002.png | 04bb7f71 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:start_duel10002.gim, basic_fi.ehp:start_duel10002.gim |
| ui_it/scritte_duello/basic_ii__start_duel10005.png | ad550ab4 | SPECIFICA | lingue col stesso hash: i - basic_bi.ehp:start_duel10005.gim, basic_fi.ehp:start_duel10005.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg01.png | 7dd7d0f0 | SPECIFICA | lingue col stesso hash: i - tutorial_i.ehp:tuto_duelimg01.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg02.png | 71437f61 | SPECIFICA | lingue col stesso hash: i - tutorial_i.ehp:tuto_duelimg02.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg03.png | f78156cc | SPECIFICA | lingue col stesso hash: i - tutorial_i.ehp:tuto_duelimg03.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg04.png | ee87c47c | SPECIFICA | lingue col stesso hash: i - tutorial_i.ehp:tuto_duelimg04.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg05.png | 866124a4 | SPECIFICA | lingue col stesso hash: i - tutorial_i.ehp:tuto_duelimg05.gim |
| ui_it/tutorial/tutorial_i__tuto_duelimg06.png | 030db8b7 | SPECIFICA | lingue col stesso hash: i - tutorial_i.ehp:tuto_duelimg06.gim |

## ui_fr ({'SPECIFICA': 85})

| file | hash | tipo | dove |
|---|---|---|---|
| ui_fr/fogli_icone/all_f__icon04.png | 98af30ad | SPECIFICA | lingue col stesso hash: f - all_f.ehp:icon04.gim |
| ui_fr/fogli_icone/all_f__panel.png | a07a7109 | SPECIFICA | lingue col stesso hash: f - all_f.ehp:panel.gim |
| ui_fr/fogli_icone/all_f__s_pack.png | 75bfeec6 | SPECIFICA | lingue col stesso hash: f - all_f.ehp:s_pack.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100002.png | d9f0ff03 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_draw100002.gim, basic_ff.ehp:duel_draw100002.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100004.png | 0db73058 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_draw100004.gim, basic_ff.ehp:duel_draw100004.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100006.png | d6fbb9b3 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_draw100006.gim, basic_ff.ehp:duel_draw100006.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100008.png | ec450799 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_draw100008.gim, basic_ff.ehp:duel_draw100008.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100010.png | 15e9ccb0 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_draw100010.gim, basic_ff.ehp:duel_draw100010.gim |
| ui_fr/lettere_esito/basic_ff__duel_draw100012.png | b807cf15 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_draw100012.gim, basic_ff.ehp:duel_draw100012.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100002.png | 0047e8d4 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_lose100002.gim, basic_ff.ehp:duel_lose100002.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100004.png | 80a96d0a | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_lose100004.gim, basic_ff.ehp:duel_lose100004.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100006.png | fde82bc2 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_lose100006.gim, basic_ff.ehp:duel_lose100006.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100008.png | e7309c53 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_lose100008.gim, basic_ff.ehp:duel_lose100008.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100010.png | de35da96 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_lose100010.gim, basic_ff.ehp:duel_lose100010.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100012.png | b810694f | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_lose100012.gim, basic_ff.ehp:duel_lose100012.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100014.png | bcee1236 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_lose100014.gim, basic_ff.ehp:duel_lose100014.gim |
| ui_fr/lettere_esito/basic_ff__duel_lose100016.png | 835c6fa4 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_lose100016.gim, basic_ff.ehp:duel_lose100016.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100002.png | 7c4c0b02 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_win100002.gim, basic_ff.ehp:duel_win100002.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100004.png | 277593da | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_win100004.gim, basic_ff.ehp:duel_win100004.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100006.png | 0b30b8d8 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_win100006.gim, basic_ff.ehp:duel_win100006.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100008.png | 4649bee5 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_win100008.gim, basic_ff.ehp:duel_win100008.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100010.png | bc63bab3 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_win100010.gim, basic_ff.ehp:duel_win100010.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100012.png | 694e26bf | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_win100012.gim, basic_ff.ehp:duel_win100012.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100014.png | a2ac32fb | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_win100014.gim, basic_ff.ehp:duel_win100014.gim |
| ui_fr/lettere_esito/basic_ff__duel_win100016.png | 063d6787 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:duel_win100016.gim, basic_ff.ehp:duel_win100016.gim |
| ui_fr/menu_liste/always_bri_fra__story_sys02.png | 94d129f8 | SPECIFICA | lingue col stesso hash: f - always_bri_fra.ehp:story_sys02.gim, always_fra_fra.ehp:story_sys02.gim |
| ui_fr/menu_liste/result_f__menu01.png | 72607cdb | SPECIFICA | lingue col stesso hash: f - result_f.ehp:menu01.gim |
| ui_fr/menu_liste/result_f__menu02.png | f319c24e | SPECIFICA | lingue col stesso hash: f - result_f.ehp:menu02.gim |
| ui_fr/menu_liste/title_menu_f__m_menu_title01.png | 5d96e868 | SPECIFICA | lingue col stesso hash: f - title_menu_f.ehp:m_menu_title01.gim |
| ui_fr/menu_liste/title_menu_f__press_start0003.png | 773e4c91 | SPECIFICA | lingue col stesso hash: f - title_menu_f.ehp:press_start0003.gim |
| ui_fr/menu_liste/title_menu_f__trnsmt02.png | 13aa38da | SPECIFICA | lingue col stesso hash: f - title_menu_f.ehp:trnsmt02.gim |
| ui_fr/schede_deck/all_f__d_window00008.png | a61d1508 | SPECIFICA | lingue col stesso hash: f - all_f.ehp:d_window00008.gim |
| ui_fr/schede_deck/all_f__d_window00033.png | 4288e72f | SPECIFICA | lingue col stesso hash: f - all_f.ehp:d_window00033.gim |
| ui_fr/schede_deck/all_f__d_window00051.png | b6dda200 | SPECIFICA | lingue col stesso hash: f - all_f.ehp:d_window00051.gim |
| ui_fr/schede_deck/all_f__d_window00062.png | a5f39742 | SPECIFICA | lingue col stesso hash: f - all_f.ehp:d_window00062.gim, conv_machine.ehp:window_f0016.gim |
| ui_fr/schede_deck/all_f__d_window00101.png | 55101663 | SPECIFICA | lingue col stesso hash: f - all_f.ehp:d_window00101.gim, rental.ehp:window_f0008.gim |
| ui_fr/schede_deck/all_f__tab_title.png | 952c742b | SPECIFICA | lingue col stesso hash: f - all_f.ehp:tab_title.gim |
| ui_fr/schede_deck/conv_machine__window_f0009.png | 1d497183 | SPECIFICA | lingue col stesso hash: f - conv_machine.ehp:window_f0009.gim, conv_machine.ehp:window_f0026.gim |
| ui_fr/schede_deck/password__key_f0027.png | 9d980a76 | SPECIFICA | lingue col stesso hash: f - password.ehp:key_f0027.gim |
| ui_fr/schede_deck/rental__window_f0015.png | 784336da | SPECIFICA | lingue col stesso hash: f - rental.ehp:window_f0015.gim |
| ui_fr/schede_deck/rental__window_f0026.png | 19e8234f | SPECIFICA | lingue col stesso hash: f - rental.ehp:window_f0026.gim |
| ui_fr/schede_ricette/limitlist__window_f0002.png | 99e75f0f | SPECIFICA | lingue col stesso hash: f - limitlist.ehp:window_f0002.gim |
| ui_fr/schede_ricette/limitlist__window_f0004.png | 05594cc2 | SPECIFICA | lingue col stesso hash: f - limitlist.ehp:window_f0004.gim |
| ui_fr/schede_ricette/limitlist__window_f0012.png | 2aa7c7b9 | SPECIFICA | lingue col stesso hash: f - limitlist.ehp:window_f0012.gim |
| ui_fr/schede_ricette/recipe_view_f__recipe010008.png | 7195a33d | SPECIFICA | lingue col stesso hash: f - recipe_view_f.ehp:recipe010008.gim, title_menu_f.ehp:recipe_sel00002.gim |
| ui_fr/schede_ricette/recipe_view_f__recipe010015.png | 244adfce | SPECIFICA | lingue col stesso hash: f - recipe_view_f.ehp:recipe010015.gim, title_menu_f.ehp:recipe_sel00009.gim |
| ui_fr/schede_ricette/recipe_view_f__recipe010027.png | 452b2fc3 | SPECIFICA | lingue col stesso hash: f - recipe_view_f.ehp:recipe010027.gim, title_menu_f.ehp:recipe_sel00020.gim |
| ui_fr/schede_ricette/recipe_view_f__recipe010029.png | 6aefce83 | SPECIFICA | lingue col stesso hash: f - recipe_view_f.ehp:recipe010029.gim, title_menu_f.ehp:recipe_sel00022.gim |
| ui_fr/schede_ricette/recipe_view_f__recipe010031.png | 4847fe90 | SPECIFICA | lingue col stesso hash: f - recipe_view_f.ehp:recipe010031.gim, title_menu_f.ehp:recipe_sel00024.gim |
| ui_fr/schede_ricette/title_menu_f__recipe_sel00033.png | a1b7db60 | SPECIFICA | lingue col stesso hash: f - title_menu_f.ehp:recipe_sel00033.gim |
| ui_fr/schede_ricette/title_menu_f__t_window0008.png | 3d9ecfb3 | SPECIFICA | lingue col stesso hash: f - title_menu_f.ehp:t_window0008.gim |
| ui_fr/schede_ricette/title_menu_f__t_window0026.png | 99a306c5 | SPECIFICA | lingue col stesso hash: f - title_menu_f.ehp:t_window0026.gim |
| ui_fr/schermata_vs/start_all__jyanken20_f0005.png | a702e687 | SPECIFICA | lingue col stesso hash: f - start_all.ehp:jyanken20_f0005.gim, start_e.ehp:jyanken20_f0005.gim |
| ui_fr/schermata_vs/start_all__jyanken20_f0007.png | ffb03b77 | SPECIFICA | lingue col stesso hash: f - start_all.ehp:jyanken20_f0007.gim, start_e.ehp:jyanken20_f0007.gim |
| ui_fr/schermata_vs/start_all__vs_much1_f0001.png | f00cc75b | SPECIFICA | lingue col stesso hash: f - start_all.ehp:vs_much1_f0001.gim, start_e.ehp:vs_much1_f0001.gim |
| ui_fr/schermata_vs/start_all__vs_much2_f0001.png | ab4234f3 | SPECIFICA | lingue col stesso hash: f - start_all.ehp:vs_much2_f0001.gim, start_e.ehp:vs_much2_f0001.gim |
| ui_fr/schermata_vs/start_all__vs_much3_f0001.png | 3ee93ceb | SPECIFICA | lingue col stesso hash: f - start_all.ehp:vs_much3_f0001.gim, start_e.ehp:vs_much3_f0001.gim |
| ui_fr/schermata_vs/start_e__d_menu01_f.png | e3cb007e | SPECIFICA | lingue col stesso hash: f - start_e.ehp:d_menu01_f.gim, start_f.ehp:d_menu01_f.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_1_f0005.png | 2938884b | SPECIFICA | lingue col stesso hash: f - start_e.ehp:vs_bg01_1_f0005.gim, start_f.ehp:vs_bg01_1_f0005.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_1_f0007.png | 43aaac68 | SPECIFICA | lingue col stesso hash: f - start_e.ehp:vs_bg01_1_f0007.gim, start_f.ehp:vs_bg01_1_f0007.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_1_f0008.png | 5522ab17 | SPECIFICA | lingue col stesso hash: f - start_e.ehp:vs_bg01_1_f0008.gim, start_f.ehp:vs_bg01_1_f0008.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_1_f0012.png | 4b1c6b9b | SPECIFICA | lingue col stesso hash: f - start_e.ehp:vs_bg01_1_f0012.gim, start_f.ehp:vs_bg01_1_f0012.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_1_f0014.png | 63905ec2 | SPECIFICA | lingue col stesso hash: f - start_e.ehp:vs_bg01_1_f0014.gim, start_f.ehp:vs_bg01_1_f0014.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_2_f0001.png | f22ee1c0 | SPECIFICA | lingue col stesso hash: f - start_e.ehp:vs_bg01_2_f0001.gim, start_f.ehp:vs_bg01_2_f0001.gim |
| ui_fr/schermata_vs/start_e__vs_bg01_2_f0004.png | 9e283fad | SPECIFICA | lingue col stesso hash: f - start_e.ehp:vs_bg01_2_f0004.gim, start_f.ehp:vs_bg01_2_f0004.gim |
| ui_fr/schermata_vs/start_f__jnk_card01.png | cf2b81ef | SPECIFICA | lingue col stesso hash: f - start_f.ehp:jnk_card01.gim |
| ui_fr/scritte_duello/basic_ff__chain010003.png | 9f72a1a4 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:chain010003.gim, basic_ff.ehp:chain010003.gim |
| ui_fr/scritte_duello/basic_ff__chain010005.png | 5a096674 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:chain010005.gim, basic_ff.ehp:chain010005.gim |
| ui_fr/scritte_duello/basic_ff__dilect_atk00001.png | 69b62191 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:dilect_atk00001.gim, basic_ff.ehp:dilect_atk00001.gim |
| ui_fr/scritte_duello/basic_ff__dilect_atk00003.png | 9bcff667 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:dilect_atk00003.gim, basic_ff.ehp:dilect_atk00003.gim |
| ui_fr/scritte_duello/basic_ff__next_player0001.png | 4c3738e7 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:next_player0001.gim, basic_ff.ehp:next_player0001.gim |
| ui_fr/scritte_duello/basic_ff__next_player0002.png | 3ee74e53 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:next_player0002.gim, basic_ff.ehp:next_player0002.gim |
| ui_fr/scritte_duello/basic_ff__next_player0004.png | 84277f2a | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:next_player0004.gim, basic_ff.ehp:next_player0004.gim |
| ui_fr/scritte_duello/basic_ff__next_player0005.png | f0ee3375 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:next_player0005.gim, basic_ff.ehp:next_player0005.gim |
| ui_fr/scritte_duello/basic_ff__score-top100011.png | c1e6c591 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:score-top100011.gim, basic_ff.ehp:score-top100011.gim |
| ui_fr/scritte_duello/basic_ff__score-top100013.png | e0f716eb | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:score-top100013.gim, basic_ff.ehp:score-top100013.gim |
| ui_fr/scritte_duello/basic_ff__start_duel10001.png | 42eb57cb | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:start_duel10001.gim, basic_ff.ehp:start_duel10001.gim |
| ui_fr/scritte_duello/basic_ff__start_duel10002.png | 66a08b34 | SPECIFICA | lingue col stesso hash: f - basic_bf.ehp:start_duel10002.gim, basic_ff.ehp:start_duel10002.gim |
| ui_fr/scritte_duello/basic_ff__start_duel10005.png | ef0dcee9 | SPECIFICA | lingue col stesso hash: fg - basic_bf.ehp:start_duel10005.gim, basic_bg.ehp:start_duel10005.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg01.png | b79d9f2c | SPECIFICA | lingue col stesso hash: f - tutorial_f.ehp:tuto_duelimg01.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg02.png | dab05056 | SPECIFICA | lingue col stesso hash: f - tutorial_f.ehp:tuto_duelimg02.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg03.png | 6ab005ac | SPECIFICA | lingue col stesso hash: f - tutorial_f.ehp:tuto_duelimg03.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg04.png | 9a43109a | SPECIFICA | lingue col stesso hash: f - tutorial_f.ehp:tuto_duelimg04.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg05.png | 4a668513 | SPECIFICA | lingue col stesso hash: f - tutorial_f.ehp:tuto_duelimg05.gim |
| ui_fr/tutorial/tutorial_f__tuto_duelimg06.png | 8ee53835 | SPECIFICA | lingue col stesso hash: f - tutorial_f.ehp:tuto_duelimg06.gim |


## ui_es (2026-10-12)
Spagnolo fatto con gli stessi script `strumenti/ui_it/*.py` (`TF1_LANG=es`): 87 righe in `PSP/TEXTURES/moduli/es/es.ini`. La maggior parte degli hash spagnoli coincide con inglese/italiano o e' gia' in `upscale_extra`. Non coperti (frammenti senza testo): start_s jyanken100005/7, title_menu_s recipe_sel00005/08/16/17/29/30/34 + t_window0002, shop bg_base_cloud02, recipe_view_s recipe010011, limitlist window_s0010/20.
