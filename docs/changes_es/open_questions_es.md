# Open questions for the user - Spanish (cards)
- 4358 name "Kanan loss Swordmistress" (English "Kanan the Swordmistress"): broken/semi-English card name. Proposal: "Kanan la Espadachina" (not applied).
- 4348 name "Dian Keto, el Señora de la Curación": inconsistent gender (el/Señora). Proposal: "Dian Keto, el Señor de la Curación" (not applied).
- Names with inconsistent capitalization (e.g. "Espectro de sombra", "Guerrero de montaña", "Zombi guerrero", "El pelo de serpiente"): not touched (game names).
- 4079 "Kairyu - Shin" (spaces around the hyphen; English "Kairyu-Shin"), 4197 "LaLa Li - oon", not touched.
- "sólo"/"solo": mixed use in the game. Not touched.
- 4521 "La Estatua de la Isla Oriental" (English Easter Island = Isla de Pascua): mistranslation of the name, not touched.
- 4644 name "Reina de los permisos de otoño" (English Queen of Autumn Leaves: "leaves" translated as "permits"): mistranslation of the name, proposal "Reina de las Hojas de Otoño" (not applied).
- 5546 name "Estrategia de Disturbación" (English Disturbance Strategy): "Disturbación" does not exist in Spanish; only the accent of Estrategia was fixed. Proposal: "Estrategia de Perturbación".
- 5732 name "Hada del Verano" (English Fairy of the Spring = Hada de la Primavera): mistranslation of the name, not touched.
- 5767/6095 name "Perro Marron Excelente" / "Cráneo Perro Marron" (English Marron, a proper name): left without accent.
- 6684 name "Viper Victory XX03" (English Victory Viper XX03; official Spanish "Victory Viper XX03"): words swapped in the name (it also appears in the text of 6637 "Ficha de Opción"). Not applied.
- 6450 name "Triedad" (English Triage): not touched.

- Dialogue ids 6978/6986/6992: "Kaiba Corporation" (EN: "Umiuma Corporation", a gag of the English edition). Kaiba Corporation left: confirm?
- Dialogues: "duelo/duelos" in lowercase (127 occurrences, in the block 5644-6980) versus capitalized "Duelo" used elsewhere by the game. Not touched: make uniform?

## Resolved on 2026-10-12 (user's answers)
- Broken card names: corrected with the official Spanish name (Yugipedia `es_name`): 4358 "Kanan la Señora de las Espadas", 5546 "Estrategia de Disturbio", 6450 "La Selección". 4348 "Dian Keto, el Señor de la Curación" (gender) and 4644 "Reina de las Hojas de Otoño" (no official Spanish name; like the French "Reine des Feuilles d'Automne"). **Left** because they are official also as they are: "Isla Oriental", "Hada del Verano", "Viper Victory XX03", "Kairyu - Shin", "LaLa Li - oon", "Marron". Another 230 name differences between the game and Yugipedia are different translations of the game, not errors: list in `official_names_diff_es.tsv` (not applied).
- Kaiba Corporation: confirmed (stays as it is).
- "duelo/Duelo": made uniform to **Duelo/Duelos** (capitalized, like the rest of the game: 1,074 versus 263 occurrences) in the dialogues.
- Rector/Canciller: **Rector** (closer to "Preside": head of a school institution).
- Tributo/Sacrificio: the official Spanish texts say "Invocar por Sacrificio" / "Sacrificando": the cards already used it; also corrected "Invocación de Tributo" -> "Invocación por Sacrificio" and "Número de Invocaciones de Tributo" in the UI strings.
- "Efecto de Blanco" = "Targeting Effect" (an effect that targets a card); "blanco" is a literal rendering of "target" (the official text uses "designar"), but it is understandable and consistent throughout the game: left.
- Optional `N`/`NEW` variant: it was a French question (written "NEW" -> "NOUVEAU" in 4 textures). In Spanish `NEW` stays in English as in the original: nothing to do.

## Update (2026-10-12, second answer from the user)
- **All the card names** were aligned with the official Spanish name of Yugipedia, even where the game translated them differently: 294 names (`tools/data/official_names_es.json`, before/after list in `official_names_es.tsv`), plus the quotations in quotation marks in the texts of the other cards (83 cards), in the interface strings (fusion hints) and in the duel sentences. Excluded, because Yugipedia has a typo or the data is missing: 4348 (stays "Señor"), 4193 "recaudación", 6071 "Resurrección", `Amfibio/Amfibia` (stays Anfibio/Anfibia), 4130 "Herramienta Antigua" (Yugipedia writes "Herremienta"), the accent-only differences where Yugipedia removes correct accents (Búho, Cañón, Más Allá, Trío...) and 7 cards without a Spanish name on Yugipedia (they stay as in the game).
- "Official" but strange names, left as Yugipedia gives them: archetypes in capitals (HÉROE Elemental..., RANA ...).
- **"Efecto de Blanco"**: in the official Spanish card texts (Yugipedia `es_text`) the action is "selecciona 1 monstruo..." and the target is "ese objetivo"; Yugipedia translates *Target* as "Objetivo". I did not find an official label for the category "Targeting Effect": I chose **"Efectos con Objetivo"** and replaced "blanco" with "objetivo" in all the explanations (also "objetivo del ataque", "objetivos de ataque" on cards 5179 and 5187). "blanco" stays only in the sense of a hit target/color and of white.
