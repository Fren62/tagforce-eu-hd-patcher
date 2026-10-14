# Testi disegnati nelle texture francesi: originale del gioco -> HD

Letti **a occhio** (2026-10-11): per ogni texture di `moduli/fr/ui_fr`, originale francese a bassa risoluzione della ISO (ingrandito 4x) accanto al PNG HD. Non c'e' un OCR sul PC: la tabella e' trascritta guardando le immagini. L'HD riscrive le stesse parole dell'originale; le differenze sono in **grassetto**.

| Texture (famiglia / file) | Testo nell'originale francese | Testo nell'HD | Differenza |
|---|---|---|---|
| duel_texts / chain010005 (+ bagliore 010003) | Chaîne | Chaîne | nessuna |
| duel_texts / dilect_atk00001, 00003 | Attaque Directe! | Attaque Directe! | nessuna |
| duel_texts / next_player0001+0002, 0004+0005 | TOUR DU JOUEUR SUIVANT (spezzato "...SUIV" + "ANT"; blu e rosso) | idem | nessuna |
| duel_texts / score-top100011, 100013 | TOUR (blu e rosso) | TOUR | nessuna |
| duel_texts / start_duel10001+10002, 10005 | **DEMARRER** DU + EL (bagliore) | **DÉMARRER** DU + EL | accento aggiunto (l'originale scriveva DEMARRER senza accento) |
| menu_lists / always_bri_fra__story_sys02 | Dimanche, Lundi, Mardi, Mercredi, Jeudi, Vendredi, Samedi · Mai, Juin, Juillet, Août · "jours avant le tournoi" · Matin, Soir | idem | nessuna |
| menu_lists / result_f__menu01 | GAGNÉ · ÉGALITÉ · PERDU | idem | nessuna |
| menu_lists / result_f__menu02 | RÉSULTAT DU DUEL · BONUS DUEL · BONUS NOUVEAU MEILLEUR SCORE · BONUS DÉFI COMPLÉTÉ · RÉSULTAT INTERMÉDIAIRE · RÉSULTAT FINAL | idem | nessuna |
| menu_lists / title_menu_f__m_menu_title01 | MENU PRINCIPAL · SAISIR NOM · LISTE CARTES TÉLÉCHARGÉE · PUZZLE DUEL · OPTIONS · SÉLECTION DE LA LANGUE | idem | nessuna |
| menu_lists / title_menu_f__press_start0003 | APPUYEZ SUR LA TOUCHE START | idem | nessuna |
| menu_lists / title_menu_f__trnsmt02 | LISTE DE GROUPE · FAIRE UN NOUVEAU GROUPE · LISTE D'ENTRÉE · DUEL · **SCAMBIA** · ENVOYER UNE RECETTE · ENVOYER UNE CARTE · ENVOYER UN PUZZLE DUEL · DUEL LIBRE · DUEL NORMAL · TAG DUEL | stesse righe, ma **ÉCHANGE** | residuo italiano dell'originale corretto |
| deck_screens / d_window00008, 00062 | Coffre | Coffre | nessuna |
| deck_screens / d_window00033 | Types de cartes acquis (+ START, ?) | idem | nessuna |
| deck_screens / d_window00051, 00101, rental__window_f0026 | Location | Location | nessuna |
| deck_screens / tab_title | Cartes achetées · Types de cartes ac(quis) (frammento) | idem | nessuna |
| deck_screens / conv_machine__window_f0009 | Convertisseur | Convertisseur | nessuna |
| deck_screens / password__key_f0027 | ENTRÉE | ENTRÉE | nessuna |
| deck_screens / rental__window_f0015 | Labo | Labo | nessuna |
| recipe_screens / limitlist__window_f0002, 0004, 0012 | Limitée · Semi-limitée · Interdite | idem | nessuna |
| recipe_screens / recipe_view_f__recipe010008, 010029, title_menu_f__recipe_sel00033 | Personnage | Personnage | nessuna |
| recipe_screens / recipe_view_f__recipe010015, 010031 | Utilisateur | Utilisateur | nessuna |
| recipe_screens / recipe_view_f__recipe010027 | Téléchargée | Téléchargée | nessuna |
| recipe_screens / title_menu_f__t_window0008, 0026 | **Scambia** | **Échange** | residuo italiano dell'originale corretto |
| vs_screen / jyanken20_f0005, 0007 | DEUXIÈME À JOUER · PREMIER À JOUER | idem | nessuna |
| vs_screen / vs_much1_f0001 | 1er round | 1er round | nessuna |
| vs_screen / vs_much2_f0001, vs_much3_f0001 | **2è** round · **3è** round | **2e** round · **3e** round | forma corretta in francese |
| vs_screen / d_menu01_f | 1er JOUEUR · 2e JOUEUR (x2 colori) · JOUEUR · distintivi 1-4 | idem | nessuna |
| vs_screen / vs_bg01_1_f0005, 0007, 0008, 0012, 0014 | DUEL NORMAL (bagliore) · DUEL · NORMAL · TAG DUEL (bagliore) · TAG | idem | nessuna |
| vs_screen / vs_bg01_2_f0001, f0004 | Mode Un Duel · Mode Match | idem | nessuna (mantenuto come nell'originale) |
| vs_screen / jnk_card01 | GAGNÉ · PERDU · EGALITE | idem | nessuna (EGALITE senza accento, come l'originale) |
| icon_sheets / icon04 | Moi, Lab, NEW, Comp!, ALL, badge 1~4, 5,6, 7~ | idem | nessuna |
| icon_sheets / panel | frammento "hetés" (di "Cartes achetées") | idem | nessuna |
| icon_sheets / s_pack | DP, ÉPUISÉ | idem | nessuna |
| result_letters / duel_win1000{02..14} + silhouette 16 | tessere T U A S G N É + "TU AS GAGNÉ" sfocato | stesse lettere (la É ha l'accento) | nessuna |
| result_letters / duel_lose1000{02..16} | tessere T U A S P E R D (8) | stesse lettere | nessuna |
| result_letters / duel_draw1000{02..12} | tessere E G A L I T (6: nel pareggio **non esiste** la tessera É, quindi "EGALIT" + E finale) | stesse lettere | nessuna |
| tutorial / tuto_duelimg01 | "Ton adversaire a déclaré le duel. Activer l'effet de la carte ?" + bottoni OUI / NON (spazio non separabile prima di `?`) | idem | nessuna |
| tutorial / tuto_duelimg02..06 | 5 cartine (disco del tipo + carta con etichette [CARTE MAGIE]/[CARTE PIÈGE]) | idem | nessuna (nomi e descrizioni da `cardinfo_fra.ehp`; testo minuscolo, non leggibile a questa scala) |

**Controllo completo:** tutte le texture di `ui_fr` sono state confrontate a occhio con l'originale. Limite: le carte minuscole nelle cartine del tutorial non sono leggibili a quella scala.

**Conclusione:** i testi francesi HD coincidono con quelli dell'originale francese **tranne** quattro correzioni: `DEMARRER` -> `DÉMARRER`, `SCAMBIA`/`Scambia` -> `ÉCHANGE`/`Échange` (residuo italiano), `2è/3è round` -> `2e/3e round`.
