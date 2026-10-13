# Testi disegnati nelle texture spagnole: originale del gioco -> HD

Letti **a occhio** (2026-10-12): per ogni texture di `moduli/es/ui_es`, originale spagnolo a bassa risoluzione della ISO (ingrandito 4x senza sfumare) accanto al PNG HD (`python strumenti/analisi/fogli_confronto_texture.py ISO_ORIGINALE es OUT_DIR`, 6 texture per foglio). Non c'e' un OCR sul PC: la tabella e' trascritta guardando le immagini. Le carte minuscole nelle cartine del tutorial non sono leggibili a quella scala e si danno per buone perche' vengono dai dati delle carte. Le parti sfocate (bagliori) hanno le stesse parole della versione nitida accanto.

Nessuna parola dello spagnolo e' stata cambiata: l'HD riproduce il testo dell'originale (carattere diverso, stessa grafia, stessa posizione). Per i termini dubbi vedi `domande_aperte_es.md`.

| Texture (famiglia / file) | Testo nell'originale spagnolo | Testo nell'HD | Differenza |
|---|---|---|---|
| scritte_duello / chain010005 (+ bagliore 010003) | Cadena | Cadena | nessuna |
| scritte_duello / dilect_atk00001 (+ bagliore 00003) | Ataque Directo | Ataque Directo | nessuna |
| scritte_duello / next_player0001+0002, 0004+0005 | TURNO DEL SIGUIENTE JUGADOR (spezzato "...JUG" + "ADOR"; blu e rosso) | idem | nessuna |
| scritte_duello / score-top | TURNO (blu e rosso) | non rifatta | stesso hash dell'italiano: la base ha gia' la versione HD |
| scritte_duello / start_duel10001+10002 (+ bagliore 10005) | COMENZAR DUELO (spezzato "COMENZAR DUE" + "LO") | idem | nessuna |
| menu_liste / always_bri_spa__story_sys02 | Domingo, Lunes, Martes, Miércoles, Jueves, Viernes, Sábado · Mayo, Junio, Julio, Agosto · "Días" · "para el torneo" · "de" · AM, PM | idem | nessuna |
| menu_liste / result_s__menu01 | GANAS · EMPATE · PIERDES | idem | nessuna |
| menu_liste / result_s__menu02 | RESULTADO DEL DUELO · BONUS DUELO · BONUS NUEVA PUNTUACIÓN ALTA · BONUS DESAFÍO COMPLETO · RESULTADO INTERMEDIO · RESULTADO FINAL | idem | nessuna |
| menu_liste / title_menu_s__m_menu_title01 | MENÚ PRINCIPAL · INTRODUCE EL NOMBRE · LISTA DE CARTAS DESCARGADAS · DUELO ACERTIJO · OPCIONES · AJUSTES DEL IDIOMA | idem | nessuna |
| menu_liste / title_menu_s__press_start0003 | PRESIONA EL BOTÓN START | idem | nessuna |
| menu_liste / title_menu_s__trnsmt02 | AGRUPAR LISTA · FORMAR GRUPO NUEVO · INTRODUCIR LISTA · DUELO · CAMBIAR · ENVIAR RECETA · ENVIAR CARTA · ENVIAR ACERTIJO DUELO · DUELO LIBRE · DUELO NORMAL · DUELO TAG | idem | nessuna |
| schede_deck / d_window00008, 00062, conv_machine window_s0016 | Tronco | Tronco | nessuna |
| schede_deck / d_window00016 | Fusión | Fusión | nessuna |
| schede_deck / d_window00033 | Tipos de carta en posesión (+ START, ?) | idem | nessuna |
| schede_deck / d_window00051, 00101, rental window_s0008, window_s0026 | Alquiler | Alquiler | nessuna |
| schede_deck / tab_title | Cartas compradas · Tipos de carta comp(...) (frammento) | idem | nessuna |
| schede_deck / conv_machine window_s0009, window_s0026 | Conversor | Conversor | nessuna |
| schede_deck / password key_s0027 | ACEPTAR | ACEPTAR | nessuna |
| schede_deck / rental window_s0015 | Laboratorio | Laboratorio | nessuna |
| schede_ricette / limitlist window_s0002, 0004, 0012 | Limitada · Semi-Limitada · Prohibida | idem | nessuna |
| schede_ricette / recipe_view_s recipe010008 | Personaje | Personaje | nessuna |
| schede_ricette / recipe_view_s recipe010015 | Usuario | Usuario | nessuna |
| schede_ricette / recipe_view_s recipe010027 | Recetas descargadas | Recetas descargadas | nessuna |
| schede_ricette / recipe_view_s recipe010029, title_menu_s recipe_sel00033 | Recetas de personaje | Recetas de personaje | nessuna |
| schede_ricette / recipe_view_s recipe010031 | Recetas de usuario | Recetas de usuario | nessuna |
| schede_ricette / title_menu_s t_window0008, 0026 | Cambiar | Cambiar | nessuna |
| schermata_vs / jyanken20_s0005, 0007 | SEGUNDO EN SALIR · PRIMERO EN SALIR | idem | nessuna |
| schermata_vs / vs_much1_s0001, vs_much2_s0001, vs_much3_s0001 | 1ra vuelta · 2da vuelta · 3ra vuelta | idem | nessuna |
| schermata_vs / d_menu01_s | JUGADOR 1 · JUGADOR 2 (x2 colori) · JUGADOR · distintivi 1-4 | idem | nessuna |
| schermata_vs / vs_bg01_1_s0005, 0007, 0008, 0012, 0014 | DUELO NORMAL (bagliore) · DUELO · NORMAL · DUELO TAG (bagliore) · TAG | idem | nessuna |
| schermata_vs / vs_bg01_2_s0001, s0004 | Modo Individual · Modo Combate | idem | nessuna (come nell'originale) |
| schermata_vs / jnk_card01 | GANAS · PIERDES · EMPATE | idem | nessuna |
| fogli_icone / icon04 | Mia, Lab, NEW, Comp!, ALL, badge 1~4, 5,6, 7~ | idem | nessuna (NEW resta in inglese come nell'originale) |
| fogli_icone / panel | frammento "rados" (di "Cartas comprados"/"...rados") | idem | nessuna |
| fogli_icone / s_pack | DP, AGOTADO | idem | nessuna |
| lettere_esito / duel_win1000{02..14} + silhouette 16 | tessere H A S G N D O (lettere di "HAS GANADO", A riusata) (+ "HAS GANADO" sfocato) | stesse lettere | nessuna |
| lettere_esito / duel_lose1000{02..18} | tessere H A S P E R D I O (le lettere di "HAS PERDIDO", D e A riusate) | stesse lettere | nessuna |
| lettere_esito / duel_draw1000{02..10} | tessere E M P A T (per "EMPATE") | stesse lettere | nessuna |
| tutorial / tuto_duelimg01 | Tu oponente ha declarado la batalla. ¿activar el efecto de la carta? · SÍ · NO | idem | nessuna |
| tutorial / tuto_duelimg02..06 | cartine "Colgante Negro", "Efecto del Bosque Angelical" ecc. (illeggibili a questa scala) | idem | nessuna (dai dati delle carte) |

## Texture spagnole senza HD (frammenti senza testo)
`recipe_sel00005/08/16/17/29/30/34`, `t_window0002`, `limitlist window_s0010/20`, `jyanken100005/7`, `recipe010011`, `bg_base_cloud02`: restano come l'originale (la base le ingrandisce con xBRZ).
