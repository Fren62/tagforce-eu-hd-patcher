# Domande aperte per l'utente - spagnolo (carte)
- 4358 nome "Kanan loss Swordmistress" (inglese "Kanan the Swordmistress"): nome della carta rotto/semi-inglese. Proposta: "Kanan la Espadachina" (non applicato).
- 4348 nome "Dian Keto, el Señora de la Curación": genere incoerente (el/Señora). Proposta: "Dian Keto, el Señor de la Curación" (non applicato).
- Nomi con maiuscole incoerenti (es. "Espectro de sombra", "Guerrero de montaña", "Zombi guerrero", "El pelo de serpiente"): non toccati (nomi del gioco).
- 4079 "Kairyu - Shin" (spazi attorno al trattino; inglese "Kairyu-Shin"), 4197 "LaLa Li - oon", non toccati.
- "sólo"/"solo": uso misto nel gioco. Non toccato.
- 4521 "La Estatua de la Isla Oriental" (inglese Easter Island = Isla de Pascua): mistraduzione del nome, non toccata.
- 4644 nome "Reina de los permisos de otoño" (inglese Queen of Autumn Leaves: "leaves" tradotto come "permessi"): mistraduzione del nome, proposta "Reina de las Hojas de Otoño" (non applicato).
- 5546 nome "Estrategia de Disturbación" (inglese Disturbance Strategy): "Disturbación" non esiste in spagnolo; solo corretto l accento di Estrategia. Proposta: "Estrategia de Perturbación".
- 5732 nome "Hada del Verano" (inglese Fairy of the Spring = Hada de la Primavera): mistraduzione del nome, non toccata.
- 5767/6095 nome "Perro Marron Excelente" / "Cráneo Perro Marron" (inglese Marron, nome proprio): lasciati senza accento.
- 6684 nome "Viper Victory XX03" (inglese Victory Viper XX03; ufficiale spagnolo "Victory Viper XX03"): parole invertite nel nome (compare anche nel testo 6637 "Ficha de Opción"). Non applicato.
- 6450 nome "Triedad" (inglese Triage): non toccato.

- Dialoghi ids 6978/6986/6992: "Kaiba Corporation" (EN: "Umiuma Corporation", gag dell edizione inglese). Lasciato Kaiba Corporation: confermare?
- Dialoghi: "duelo/duelos" in minuscolo (127 occorrenze, nel blocco 5644-6980) contro "Duelo" maiuscolo usato dal gioco altrove. Non toccato: uniformare?

## Risolte il 2026-10-12 (risposte dell'utente)
- Nomi di carte rotti: corretti con il nome ufficiale spagnolo (Yugipedia `es_name`): 4358 "Kanan la Señora de las Espadas", 5546 "Estrategia de Disturbio", 6450 "La Selección". 4348 "Dian Keto, el Señor de la Curación" (genere) e 4644 "Reina de las Hojas de Otoño" (nessun nome ufficiale spagnolo; come il francese "Reine des Feuilles d'Automne"). **Lasciati** perche' ufficiali anche cosi': "Isla Oriental", "Hada del Verano", "Viper Victory XX03", "Kairyu - Shin", "LaLa Li - oon", "Marron". Altre 230 differenze di nome tra il gioco e Yugipedia sono traduzioni diverse del gioco, non errori: elenco in `nomi_ufficiali_diff_es.tsv` (non applicate).
- Kaiba Corporation: confermato (resta cosi').
- "duelo/Duelo": uniformato a **Duelo/Duelos** (maiuscolo, come il resto del gioco: 1.074 contro 263 occorrenze) nei dialoghi.
- Rector/Canciller: **Rector** (piu' vicino a "Preside": capo di un istituto scolastico).
- Tributo/Sacrificio: i testi ufficiali spagnoli dicono "Invocar por Sacrificio" / "Sacrificando": le carte lo usavano gia'; corretti anche "Invocación de Tributo" -> "Invocación por Sacrificio" e "Número de Invocaciones de Tributo" nelle stringhe UI.
- "Efecto de Blanco" = "Targeting Effect" (effetto che sceglie come bersaglio una carta); "blanco" e' una resa letterale di "target" (il testo ufficiale usa "designar"), ma e' comprensibile e coerente in tutto il gioco: lasciato.
- Variante opzionale `N`/`NEW`: era una questione del francese (scritta "NEW" -> "NOUVEAU" in 4 texture). In spagnolo `NEW` resta in inglese come nell'originale: nulla da fare.

## Aggiornamento (2026-10-12, seconda risposta dell'utente)
- **Tutti i nomi di carta** sono stati allineati al nome spagnolo ufficiale di Yugipedia, anche dove il gioco li traduceva diversamente: 294 nomi (`strumenti/dati/nomi_ufficiali_es.json`, elenco prima/dopo in `nomi_ufficiali_es.tsv`), piu' le citazioni tra virgolette nei testi delle altre carte (83 carte), nelle stringhe dell'interfaccia (suggerimenti di fusione) e nelle frasi dei duelli. Esclusi, perche' Yugipedia ha un refuso o manca il dato: 4348 (resta "Señor"), 4193 "recaudación", 6071 "Resurrección", `Amfibio/Amfibia` (resta Anfibio/Anfibia), 4130 "Herramienta Antigua" (Yugipedia scrive "Herremienta"), le differenze di soli accenti dove Yugipedia toglie accenti giusti (Búho, Cañón, Más Allá, Trío...) e 7 carte senza nome spagnolo su Yugipedia (restano come nel gioco).
- Nomi "ufficiali" ma strani, lasciati cosi' come li da' Yugipedia: archetipi in maiuscolo (HÉROE Elemental..., RANA ...).
- **"Efecto de Blanco"**: nei testi ufficiali spagnoli delle carte (Yugipedia `es_text`) l'azione e' "selecciona 1 monstruo..." e il bersaglio e' "ese objetivo"; Yugipedia traduce *Target* con "Objetivo". Non ho trovato un'etichetta ufficiale per la categoria "Targeting Effect": ho scelto **"Efectos con Objetivo"** e ho sostituito "blanco" con "objetivo" in tutte le spiegazioni (anche "objetivo del ataque", "objetivos de ataque" sulle carte 5179 e 5187). "blanco" resta solo nel senso di bersaglio colpito/colore (Cañón de Dharma, Conejo Oscuro, Víbora de llama) e di bianco.
