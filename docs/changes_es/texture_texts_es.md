# Texts drawn in the Spanish textures: game original -> HD

Read **by eye** (2026-10-12): for every texture of `modules/es/ui_es`, the low-resolution Spanish original of the ISO (enlarged 4x without smoothing) next to the HD PNG (`python tools/analysis/texture_comparison_sheets.py ORIGINAL_ISO es OUT_DIR`, 6 textures per sheet). There is no OCR on the PC: the table is transcribed by looking at the images. The tiny cards in the tutorial maps are not legible at that scale and are taken as good because they come from the card data. The blurred parts (glows) have the same words as the sharp version next to them.

No Spanish word was changed: the HD reproduces the text of the original (different typeface, same spelling, same position). For the doubtful terms see `open_questions_es.md`.

| Texture (family / file) | Text in the Spanish original | Text in the HD | Difference |
|---|---|---|---|
| duel_texts / chain010005 (+ glow 010003) | Cadena | Cadena | none |
| duel_texts / dilect_atk00001 (+ glow 00003) | Ataque Directo | Ataque Directo | none |
| duel_texts / next_player0001+0002, 0004+0005 | TURNO DEL SIGUIENTE JUGADOR (split "...JUG" + "ADOR"; blue and red) | same | none |
| duel_texts / score-top | TURNO (blue and red) | not redone | same hash as Italian: the base already has the HD version |
| duel_texts / start_duel10001+10002 (+ glow 10005) | COMENZAR DUELO (split "COMENZAR DUE" + "LO") | same | none |
| menu_lists / always_bri_spa__story_sys02 | Domingo, Lunes, Martes, Miércoles, Jueves, Viernes, Sábado · Mayo, Junio, Julio, Agosto · "Días" · "para el torneo" · "de" · AM, PM | same | none |
| menu_lists / result_s__menu01 | GANAS · EMPATE · PIERDES | same | none |
| menu_lists / result_s__menu02 | RESULTADO DEL DUELO · BONUS DUELO · BONUS NUEVA PUNTUACIÓN ALTA · BONUS DESAFÍO COMPLETO · RESULTADO INTERMEDIO · RESULTADO FINAL | same | none |
| menu_lists / title_menu_s__m_menu_title01 | MENÚ PRINCIPAL · INTRODUCE EL NOMBRE · LISTA DE CARTAS DESCARGADAS · DUELO ACERTIJO · OPCIONES · AJUSTES DEL IDIOMA | same | none |
| menu_lists / title_menu_s__press_start0003 | PRESIONA EL BOTÓN START | same | none |
| menu_lists / title_menu_s__trnsmt02 | AGRUPAR LISTA · FORMAR GRUPO NUEVO · INTRODUCIR LISTA · DUELO · CAMBIAR · ENVIAR RECETA · ENVIAR CARTA · ENVIAR ACERTIJO DUELO · DUELO LIBRE · DUELO NORMAL · DUELO TAG | same | none |
| deck_screens / d_window00008, 00062, conv_machine window_s0016 | Tronco | Tronco | none |
| deck_screens / d_window00016 | Fusión | Fusión | none |
| deck_screens / d_window00033 | Tipos de carta en posesión (+ START, ?) | same | none |
| deck_screens / d_window00051, 00101, rental window_s0008, window_s0026 | Alquiler | Alquiler | none |
| deck_screens / tab_title | Cartas compradas · Tipos de carta comp(...) (fragment) | same | none |
| deck_screens / conv_machine window_s0009, window_s0026 | Conversor | Conversor | none |
| deck_screens / password key_s0027 | ACEPTAR | ACEPTAR | none |
| deck_screens / rental window_s0015 | Laboratorio | Laboratorio | none |
| recipe_screens / limitlist window_s0002, 0004, 0012 | Limitada · Semi-Limitada · Prohibida | same | none |
| recipe_screens / recipe_view_s recipe010008 | Personaje | Personaje | none |
| recipe_screens / recipe_view_s recipe010015 | Usuario | Usuario | none |
| recipe_screens / recipe_view_s recipe010027 | Recetas descargadas | Recetas descargadas | none |
| recipe_screens / recipe_view_s recipe010029, title_menu_s recipe_sel00033 | Recetas de personaje | Recetas de personaje | none |
| recipe_screens / recipe_view_s recipe010031 | Recetas de usuario | Recetas de usuario | none |
| recipe_screens / title_menu_s t_window0008, 0026 | Cambiar | Cambiar | none |
| vs_screen / jyanken20_s0005, 0007 | SEGUNDO EN SALIR · PRIMERO EN SALIR | same | none |
| vs_screen / vs_much1_s0001, vs_much2_s0001, vs_much3_s0001 | 1ra vuelta · 2da vuelta · 3ra vuelta | same | none |
| vs_screen / d_menu01_s | JUGADOR 1 · JUGADOR 2 (x2 colors) · JUGADOR · badges 1-4 | same | none |
| vs_screen / vs_bg01_1_s0005, 0007, 0008, 0012, 0014 | DUELO NORMAL (glow) · DUELO · NORMAL · DUELO TAG (glow) · TAG | same | none |
| vs_screen / vs_bg01_2_s0001, s0004 | Modo Individual · Modo Combate | same | none (as in the original) |
| vs_screen / jnk_card01 | GANAS · PIERDES · EMPATE | same | none |
| icon_sheets / icon04 | Mia, Lab, NEW, Comp!, ALL, badge 1~4, 5,6, 7~ | same | none (NEW stays in English as in the original) |
| icon_sheets / panel | fragment "rados" (di "Cartas comprados"/"...rados") | same | none |
| icon_sheets / s_pack | DP, AGOTADO | same | none |
| result_letters / duel_win1000{02..14} + silhouette 16 | tiles H A S G N D O (lettere di "HAS GANADO", A riusata) (+ "HAS GANADO" blurred) | same letters | none |
| result_letters / duel_lose1000{02..18} | tiles H A S P E R D I O (the letters of "HAS PERDIDO", D and A reused) | same letters | none |
| result_letters / duel_draw1000{02..10} | tiles E M P A T (for "EMPATE") | same letters | none |
| tutorial / tuto_duelimg01 | Tu oponente ha declarado la batalla. ¿activar el efecto de la carta? · SÍ · NO | same | none |
| tutorial / tuto_duelimg02..06 | maps "Colgante Negro", "Efecto del Bosque Angelical" etc. (illegible at this scale) | same | none (from the card data) |

## Spanish textures without HD (fragments without text)
`recipe_sel00005/08/16/17/29/30/34`, `t_window0002`, `limitlist window_s0010/20`, `jyanken100005/7`, `recipe010011`, `bg_base_cloud02`: they stay like the original (the base enlarges them with xBRZ).
