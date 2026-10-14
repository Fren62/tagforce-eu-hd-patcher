# Texts drawn in the French textures: game original -> HD

Read **by eye** (2026-10-11): for every texture of `modules/fr/ui_fr`, the low-resolution French original of the ISO (enlarged 4x) next to the HD PNG. There is no OCR on the PC: the table is transcribed by looking at the images. The HD rewrites the same words as the original; the differences are in **bold**.

| Texture (family / file) | Text in the French original | Text in the HD | Difference |
|---|---|---|---|
| duel_texts / chain010005 (+ glow 010003) | Chaîne | Chaîne | none |
| duel_texts / dilect_atk00001, 00003 | Attaque Directe! | Attaque Directe! | none |
| duel_texts / next_player0001+0002, 0004+0005 | TOUR DU JOUEUR SUIVANT (split "...SUIV" + "ANT"; blue and red) | same | none |
| duel_texts / score-top100011, 100013 | TOUR (blue and red) | TOUR | none |
| duel_texts / start_duel10001+10002, 10005 | **DEMARRER** DU + EL (glow) | **DÉMARRER** DU + EL | accent added (the original wrote DEMARRER without an accent) |
| menu_lists / always_bri_fra__story_sys02 | Dimanche, Lundi, Mardi, Mercredi, Jeudi, Vendredi, Samedi · Mai, Juin, Juillet, Août · "jours avant le tournoi" · Matin, Soir | same | none |
| menu_lists / result_f__menu01 | GAGNÉ · ÉGALITÉ · PERDU | same | none |
| menu_lists / result_f__menu02 | RÉSULTAT DU DUEL · BONUS DUEL · BONUS NOUVEAU MEILLEUR SCORE · BONUS DÉFI COMPLÉTÉ · RÉSULTAT INTERMÉDIAIRE · RÉSULTAT FINAL | same | none |
| menu_lists / title_menu_f__m_menu_title01 | MENU PRINCIPAL · SAISIR NOM · LISTE CARTES TÉLÉCHARGÉE · PUZZLE DUEL · OPTIONS · SÉLECTION DE LA LANGUE | same | none |
| menu_lists / title_menu_f__press_start0003 | APPUYEZ SUR LA TOUCHE START | same | none |
| menu_lists / title_menu_f__trnsmt02 | LISTE DE GROUPE · FAIRE UN NOUVEAU GROUPE · LISTE D'ENTRÉE · DUEL · **SCAMBIA** · ENVOYER UNE RECETTE · ENVOYER UNE CARTE · ENVOYER UN PUZZLE DUEL · DUEL LIBRE · DUEL NORMAL · TAG DUEL | same lines, but **ÉCHANGE** | Italian leftover of the original, corrected |
| deck_screens / d_window00008, 00062 | Coffre | Coffre | none |
| deck_screens / d_window00033 | Types de cartes acquis (+ START, ?) | same | none |
| deck_screens / d_window00051, 00101, rental__window_f0026 | Location | Location | none |
| deck_screens / tab_title | Cartes achetées · Types de cartes ac(quis) (fragment) | same | none |
| deck_screens / conv_machine__window_f0009 | Convertisseur | Convertisseur | none |
| deck_screens / password__key_f0027 | ENTRÉE | ENTRÉE | none |
| deck_screens / rental__window_f0015 | Labo | Labo | none |
| recipe_screens / limitlist__window_f0002, 0004, 0012 | Limitée · Semi-limitée · Interdite | same | none |
| recipe_screens / recipe_view_f__recipe010008, 010029, title_menu_f__recipe_sel00033 | Personnage | Personnage | none |
| recipe_screens / recipe_view_f__recipe010015, 010031 | Utilisateur | Utilisateur | none |
| recipe_screens / recipe_view_f__recipe010027 | Téléchargée | Téléchargée | none |
| recipe_screens / title_menu_f__t_window0008, 0026 | **Scambia** | **Échange** | Italian leftover of the original, corrected |
| vs_screen / jyanken20_f0005, 0007 | DEUXIÈME À JOUER · PREMIER À JOUER | same | none |
| vs_screen / vs_much1_f0001 | 1er round | 1er round | none |
| vs_screen / vs_much2_f0001, vs_much3_f0001 | **2è** round · **3è** round | **2e** round · **3e** round | correct form in French |
| vs_screen / d_menu01_f | 1er JOUEUR · 2e JOUEUR (x2 colors) · JOUEUR · badges 1-4 | same | none |
| vs_screen / vs_bg01_1_f0005, 0007, 0008, 0012, 0014 | DUEL NORMAL (glow) · DUEL · NORMAL · TAG DUEL (glow) · TAG | same | none |
| vs_screen / vs_bg01_2_f0001, f0004 | Mode Un Duel · Mode Match | same | none (kept as in the original) |
| vs_screen / jnk_card01 | GAGNÉ · PERDU · EGALITE | same | none (EGALITE without accent, as in the original) |
| icon_sheets / icon04 | Moi, Lab, NEW, Comp!, ALL, badge 1~4, 5,6, 7~ | same | none |
| icon_sheets / panel | fragment "hetés" (di "Cartes achetées") | same | none |
| icon_sheets / s_pack | DP, ÉPUISÉ | same | none |
| result_letters / duel_win1000{02..14} + silhouette 16 | tiles T U A S G N É + "TU AS GAGNÉ" blurred | same letters (the É has the accent) | none |
| result_letters / duel_lose1000{02..16} | tiles T U A S P E R D (8) | same letters | none |
| result_letters / duel_draw1000{02..12} | tiles E G A L I T (6: in the draw the É tile **does not exist**, so "EGALIT" + final E) | same letters | none |
| tutorial / tuto_duelimg01 | "Ton adversaire a déclaré le duel. Activer l'effet de la carte ?" + buttons OUI / NON (non-breaking space before `?`) | same | none |
| tutorial / tuto_duelimg02..06 | 5 maps (type disc + card with [CARTE MAGIE]/[CARTE PIÈGE] labels) | same | none (names and descriptions from `cardinfo_fra.ehp`; tiny text, not legible at this scale) |

**Complete check:** all the textures of `ui_fr` were compared by eye with the original. Limit: the tiny cards in the tutorial maps are not legible at that scale.

**Conclusion:** the HD French texts match those of the French original **except** for four corrections: `DEMARRER` -> `DÉMARRER`, `SCAMBIA`/`Scambia` -> `ÉCHANGE`/`Échange` (Italian leftover), `2è/3è round` -> `2e/3e round`.
