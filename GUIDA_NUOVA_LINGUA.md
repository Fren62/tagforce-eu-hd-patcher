# GUIDA - Come adattare il gioco a una lingua europea

Linee guida **generali** (valide per spagnolo, tedesco, inglese o qualunque lingua europea del gioco) ricavate dal lavoro fatto su **italiano** e
**francese**. Gli esempi vengono da quei due casi; niente qui e' specifico di una lingua. Per i dettagli tecnici di ogni script vedi `TUTORIAL.md`
(ricette per famiglia di texture, joypad virtuale, trappole), per lo stato corrente `STATO_LAVORI.md`, per le **scelte editoriali gia' prese**
`REGISTRO_SCELTE.md` (e `strumenti/dati/registro_scelte_editoriali.json`).

**Documenti completi di tutto cio' che e' stato fatto, da prendere come modello:** `MODIFICHE_ITALIANO.md` e `MODIFICHE_FRANCESE.md` (modifiche alla ISO riga per riga, struttura e contenuto del texture pack, scelte, verifiche; elenchi esatti in `documentazione/modifiche_<l>/*.csv`). Si rigenerano con `strumenti/analisi/documenta_modifiche.py`, `confronti_testi.py` (confronti originale->nuovo con parole evidenziate), `documenta_pack.py`, `scrivi_documento_modifiche.py` (anche per es/de: aggiungere la lingua ai dizionari `NOME`/`LING` e creare `regole_<l>`).

Chi parte: leggi questa guida, poi `REGISTRO_SCELTE.md`, poi `TUTORIAL.md` sezioni 2, 3, 7 e 13.

---

## 0. Principi (valgono in ogni fase)

1. **Il riferimento di testo e' l'originale giapponese/inglese del gioco, non l'inventiva.** Si correggono errori oggettivi (refusi, accenti, spazi,
   concordanze, residui di altre lingue, traduzioni palesemente sbagliate o censurate); non si "modernizza" la terminologia.
2. **Ogni controllo fatto per una lingua si estende a tutte le altre** (it, fr, de, es, en): se in italiano trovi una classe di errore, cercala in tutte.
3. **Ogni decisione editoriale va registrata** in `REGISTRO_SCELTE.md` **e** nei dati della lingua, con id, testo originale, testo nuovo, motivo.
   Cosi' un patcher per un'altra lingua applica l'equivalente giusto (esempio: "salsa piccante -> shochu" e' una scelta comune, ogni lingua la scrive a modo suo).
4. **Mai modificare la ISO originale**: `applica_iso.py` scrive una copia (`..._definitiva.iso`).
5. **Non levigare la pixel art** (tasti, frecce, bandiere, cifre piccole) senza conferma dell'utente. Il pixel originale e' preferito.
6. **Leggi a mano tutto il testo**, anche se esistono strumenti: ortografia automatica e confronto con database ufficiali trovano i refusi, non gli errori di senso.
   Per i dump usa sempre testo **senza doppioni** con l'inglese accanto: sono migliaia di righe, ma ripetute poche volte.
7. **Verifica in gioco** (ISO `_definitiva` + pack): un file corretto non basta.
8. Documenta mentre lavori, non alla fine.

## 1. Mappa del lavoro (una lingua = questi 8 blocchi)

| # | Blocco | Dove vive il dato | Come si applica |
|---|---|---|---|
| 1 | Testi delle carte (nomi + descrizioni) | `strumenti/correzioni/regole_<l>.py` -> `dati/correzioni_carte[_<l>].json` | ISO (`cardinfo_<l>.ehp`) **e** immagini HD |
| 2 | Immagini HD delle carte (piccole, grandi, miniature, attributi, etichette) | `PSP/TEXTURES/moduli/<l>/cards` | pack di texture |
| 3 | Dialoghi della storia | `dati/ritocchi_dialoghi_<l>.json` -> `correzioni_dialoghi_<l>.json` | ISO (`script/*.ehp`) |
| 4 | Frasi dei duellanti nei duelli | `dati/correzioni_frasi_duello_<l>.json` | ISO (`duel/*.ehp`) |
| 5 | Stringhe lunghe dell'interfaccia (aiuti, schede dei duellisti, tutorial, record) | `correzioni/regole_stringhe_<l>.py`, `dati/testi_ui.json` | ISO |
| 6 | Interfaccia HD disegnata (scritte in immagine, ~86 texture) | `ui_<l>` nel modulo, script `strumenti/ui_it/*.py` con `TF1_LANG` | pack di texture |
| 7 | Foglio dei numeri del duello (`card_icon03`), targa del titolo | `strumenti/ui_it/icon03_lingue.py`, `titolo_pomodoro.py` | pack di texture |
| 8 | Registro delle scelte + prova in gioco + documentazione | `REGISTRO_SCELTE.md` | - |

Punto d'ingresso unico per i testi nella ISO: `python strumenti/correzioni/applica_iso.py ISO_ORIG ISO_OUT [lingue]`. **Senza elenco di lingue le applica tutte**:
non lanciarlo con una sola lingua verso la ISO finale, sovrascriveresti le altre (e' un errore gia' fatto).

---

## 2. Testi delle carte (blocco 1)

**Cosa si corregge**: refusi (`Annello`->`Anello`), accenti (`E'`->`È`, `puo`->`può`), apostrofi e spazi (`L' OSCURITÀ`->`L'OSCURITÀ`, `Magia,Trappola`), maiuscole
incoerenti con il resto del gioco (`Main phase`->`Main Phase`, `tipo Pyro`->`Tipo Pyro`), concordanze (`questo carta`, `vengono cambiata`), plurali di termini fissi
(`Life Point`->`Life Points`), parole di altre lingue, nomi di carte citati male in altre descrizioni (`Victory Viper XX3`->`XX03`). **Non si cambiano**: nomi ufficiali
nel testo, terminologia scelta dal gioco (es. in francese "Carte Piège Continu" e' coerente in tutto il gioco: si lascia; in italiano "Terreno", "Evocazione tramite Tributo").

**Metodo (usato per it e fr)**
1. Estrai i testi (`cardprops.load(cardinfo_<l>.ehp, corretto=False)`), uno per riga `id <TAB> nome <TAB> descrizione`, a blocchi di ~90 righe (l'output di uno
   strumento si tronca a ~30 KB: di piu' e' sprecato).
2. **Leggi tutto, in ordine.** Annota subito ogni errore (id + testo): le note vanno su file, **non** a memoria (un contesto lungo si compatta e le note si perdono: e' successo).
3. Trasforma gli errori in **regole**: preferisci `GLOBALI` (regex `(modello, sostituzione, motivo)`) quando l'errore e' di una classe; `PER_CARTA` (id, campo, vecchio, nuovo, motivo)
   per i casi unici. Il "vecchio" di `PER_CARTA` deve comparire **esattamente** o lo script si ferma (e' voluto: la tabella non deriva da una lettura sbagliata).
4. Dopo le regole, **scansione automatica** della classe di errore su tutte le carte (doppi spazi, ` ,`, `,A`, `.A`, apostrofo+spazio, parola doppia, `E' `...): trova quello che l'occhio salta.
5. Genera: `python strumenti/correzioni/genera_lingua.py LINGUA CARDINFO_<l>.ehp` (la versione in `correzioni/`; scrive anche `confronti/audit_carte/correzioni_<l>.csv`).
   - fr/de/es/en: parte dai testi **originali** e scrive `dati/correzioni_carte_<l>.json`.
   - it: parte dai testi **gia' corretti** e **fonde** nel `dati/correzioni_carte.json` esistente (idempotente: rilanciabile).
6. Controlli: i `PER_CARTA` non devono dare "testo non trovato"; leggi il CSV delle modifiche; **nessuna regola globale deve toccare cio' che non volevi** (guarda i conteggi stampati: una regola con 140 corrispondenze su un modello che pensavi raro e' sospetta).
7. Rigenera le **immagini** solo delle carte toccate (blocco 2) e ricostruisci la ISO.

Esempi: italiano 116 -> **181** carte corrette (`regole_it.py`, regole globali per classe di errore + 7 per carta); francese 70.
Domande aperte da fare all'utente (non decidere da soli): portare i nomi delle carte ai nomi ufficiali della lingua, nomi di personaggi (es. "Ragazza Mago Nero" / "Maga Nera").

## 3. Immagini delle carte (blocco 2)

- Moduli: `python strumenti/genera_lingua.py LINGUA PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` (la versione in `strumenti/`): senza ID rigenera tutto
  (2.833 piccole + 2.833 grandi); con ID solo quelle, senza atlante. Dentro: tabella attributi con le parole della lingua, etichetta Magia/Trappola, atlante miniature
  del deck (senza di esso il deck mostra i nomi **inglesi**).
- **Dopo ogni modifica alle correzioni** delle carte rigenera le immagini toccate. Per l'italiano: `sh strumenti/rigenera_correzioni.sh USRDIR PACK_USA PACK_MOD PYTHON`
  (181 carte -> 199 immagini piccole + 199 grandi, pochi minuti). Su Windows lo script usa `python -I`: i pacchetti nel *user site* (cv2) non si vedono; passa come
  PYTHON un piccolo wrapper che scarta `-I` (`exec python "$@"`).
- Poi copia i PNG cambiati nel pack installato in PPSSPP e **riavvia PPSSPP** (cache delle texture). Gli hash non cambiano: `textures.ini` resta uguale.
- Tipografia della lingua: francese spazio non separabile prima di `: ; ! ?` e virgolette « »; tedesco „ “; spagnolo `¿ ¡`.

## 4. Dialoghi della storia (blocco 3)

1. Estrai: `python strumenti/audit/estrai_dialoghi.py ISO confronti/audit_dialoghi` (righe uniche con inglese e giapponese).
2. Leggi **riga per riga confrontando con inglese e giapponese**; il giapponese decide quando inglese e lingua locale divergono. Annota in
   `dati/ritocchi_dialoghi_<l>.json`: `esatte` {riga intera originale: nuova} e `parti` [[vecchio, nuovo]] (a capo scritti `⏎`).
3. `python strumenti/correzioni/costruisci_dialoghi.py <l>` -> `correzioni_dialoghi_<l>.json`. Le righe senza correzione propria **ereditano** da quelle con lo stesso testo originale
   e lo stesso giapponese (propagazione ai doppioni). Le `parti` si applicano **dopo** base ed `esatte`; la chiave di una `esatte` e' il testo **prima** delle parti.
4. Regole automatiche di impaginazione in `costruisci_dialoghi.py`: spazio dopo i segnaposto `《...》`, punteggiatura francese `! ? : ;`, tre puntini seguiti da maiuscola (`...Ciao` -> `... Ciao`, solo it).
5. **Vincoli del box**: ~46 caratteri per riga (il gioco non va a capo), massimo 3 righe; `applica_iso` avvisa ("N righe, potrebbe non stare nel box"): controlla in gioco
   le segnalate. Un segnaposto vale ~6 caratteri.

**Cosa cercare** (classi di errore trovate in italiano, valgono per tutte): interiezioni inglesi lasciate (`Oh my`), refusi, apostrofi, `E'`, accenti, ora scritta male (`7PM`),
nomi dei dormitori incoerenti, titoli (`Cancelliere`/`Preside`), traduzioni **censurate o cambiate** rispetto al giapponese (vedi sotto), residui di un'altra lingua.

**Scelte comuni a tutte le lingue** (gia' prese, da replicare nella nuova lingua: dettagli e tabella nel registro):
- scena `st01_t01/Scr003E`: la famiglia di Chumley ha una **distilleria di sake**, il regalo e' **shochu** (non salsa piccante); Syrus chiede il disegno della Ragazza Mago Nero
  **in abito da cameriera** (non bikini) e passa un **abito da cameriera** come modello. Si applicano righe #146-#197 incluse le copie (#150, #151);
- scena `st02_t01/Scr101E` righe 22-27: il testo originale e' **ruotato tra le lingue** (bug del gioco): rimettere ognuno nella sua lingua;
- **nome del parlante** (es. "Doyen Sheppard"): sta nell'EBOOT cifrato, **non modificabile** in nessuna lingua. In italiano il personaggio e' "Preside" in tutto il testo
  modificabile; in francese "Chancelier"/"Doyen" scelto dialogo per dialogo (formale/informale).

## 5. Frasi dei duellanti (blocco 4)

Sono le battute dette durante i duelli (`chr_wordstbl_<l>.bin` / `02chr_wordstbl_<l>.bin` dentro ~70 archivi `duel/cutin_*.ehp`...): ~34.000 voci ma solo **~1.800 uniche per lingua**.

1. Elenco da leggere: `python strumenti/audit/estrai_frasi_duello.py ISO LINGUA OUT.txt` (frase con le correzioni gia' applicate + inglese accanto).
2. Leggi tutto (6-7 blocchi da ~280 righe). Non toccare cio' che e' **voluto**: frasi in "pidgin" di certi personaggi (it "Io pescare destino!", fr "Moi pioche, moi victoire !"),
   versi (`Screech!`), nomi di mosse che l'inglese lascia in inglese (`Train Twister`), versi di sbadiglio/dolore.
3. Errori trovati (esempi): punto finale mancante in frasi gemelle (`Attivo una Magia Continua` + `.`), maiuscola dopo `⏎` a meta' frase, apostrofo dell'imperativo (`Fa pure`->`Fa' pure`),
   articoli duplicati (`una l'effetto`), frasi mal costruite (`non si è solo a una questione`), traduzione sbagliata del senso (`Tu es malin` per *You're cute* -> `mignon`),
   inglesismi (`Huh ?`->`Hein ?`), maiuscole (`Mon dieu`->`Mon Dieu`), elisioni (`Je offre`->`J'offre`).
4. Aggiungi a `dati/correzioni_frasi_duello_<l>.json`: `esatte` (frase intera, a capo come `⏎`) o `parti` (sostituzione su ogni frase). Le `esatte` sono per le frasi **brevi** dove una `parte`
   toccherebbe anche frasi piu' lunghe (es. aggiungere un `.` finale); verifica con `applica_iso` che stampi **0 avvisi** ("frase esatta mai trovata" = chiave sbagliata).
5. **Crash**: i file `*-ptrs.txt` negli archivi dei personaggi contengono offset assoluti; se una tabella cresce vanno ricalcolati (`rimappa_puntatori`, gia' fatto da `frasi_duello.py`),
   altrimenti il duello va in crash. Non scrivere frasi con parti non-UTF-16.

## 6. Stringhe lunghe dell'interfaccia (blocco 5)

Tabelle `strTbl*`, aiuti (`help_strtbl_*`), `ddstrtbl_<l>`, biografie dei duellisti (`charalist`), record e obiettivi (`duelrecord`/`result`), negozio, laboratorio, menu dell'ufficio.

1. Estrai tutte le tabelle (stesso formato `(n, 12, 12+4n)` + offset + UTF-16 di `chr_wordstbl`; `frasi_duello.tabella`/`scrivi_tabella`) e raggruppa per archivio/membro; stampa `indice | testo || inglese`.
2. Leggi tutto. Cerca residui di altre lingue, etichette che escono dal bordo (`audit/etichette_lunghe.py`), terminologia incoerente con le carte.
3. Scrivi `correzioni/regole_stringhe_<l>.py`: `TABELLE` (archivi/membri), `STRINGHE` (per archivio/membro/indice 0-based, vecchio->nuovo; i vecchi testi devono comparire esattamente, a capo reali `\n` o `\r\n`),
   `GLOBALI` (regex, sostituzione stringa o callable). Le `STRINGHE` si applicano **prima** dei `GLOBALI`.
4. `applica_iso.py` riscrive gli archivi in coda alla ISO e stampa gli avvisi: devono essere 0. Italiano 505 stringhe in 15 archivi; con tutte le lingue 941 in 25.
5. Coerenza di terminologia **tra le tre fonti** (carte, dialoghi, interfaccia): es. in italiano "Segna-Mostro" (mai "Gettone") in aiuti, record e carte; "Preside Sheppard" in scheda e dialoghi.

## 7. Texture dell'interfaccia (blocchi 6 e 7)

### 7.1 Prima di ridisegnare: quali texture sono davvero da fare
PPSSPP sostituisce una texture dall'**hash dei suoi pixel**. Per ogni texture della famiglia, calcola l'hash nella tua lingua, in inglese e in italiano (`ui_it/common.texture`, `gim.data_hash`):
- uguale all'**inglese** -> la copre gia' il pack di base (MikeyMK);
- uguale all'**italiano** -> vale la versione `ui_it` (se contiene testo nella lingua sbagliata, e' un problema: controlla l'immagine, non solo l'hash);
- altrimenti **da ridisegnare** in `ui_<l>`.

**Inventario completo**: `INVENTARIO_TEXTURE.md` (generato da `strumenti/analisi/inventario_texture_lingue.py ISO OUT.md`) elenca ogni texture di `ui_it` e `ui_fr` come NEUTRA (copia e incolla per tutte le lingue) o SPECIFICA (da rifare), con le lingue che condividono l'hash. Rigeneralo se aggiungi texture.

**Classificare le texture "solo italiane"** (lavoro fatto per il francese): una texture presente solo in `ui_it` ricade in due casi.
1. *Stesso hash in tutte le lingue* (pannelli ricette, linguette `Side`/`Deck`/`Fusion Deck`, barre vuote, `card_side`, bandiere): e' neutra, il modulo della nuova lingua la riceve gratis. Basta guardare l'immagine per accertarsi che non contenga parole italiane.
2. *Hash diverso per lingua*: nel gioco originale la versione italiana e' scritta in italiano (`NUOVO`, icona `N`; la linguetta dell'editor deck dice **`Fusion`**, non `Fusione`: "Fusion Deck" si chiama cosi' in tutte le lingue, errore italiano corretto il 2026-10-11), quella francese **gia' ha un suo hash e un suo HD** in `upscale_extra` (con `NEW`, `Fusion`).
   Non e' un buco: e' la scelta dell'originale. Rifare quelle con la parola locale (es. `NOUVEAU`/`N`, `NEU`/`N`, `NUEVO`/`N`) e' **opzionale**: chiedere all'utente.

### 7.2 Famiglie e procedura
Le 8 famiglie (`scritte_duello`, `lettere_esito`, `menu_liste`, `fogli_icone`, `schede_deck`, `schede_ricette`, `schermata_vs`, `tutorial`) e la ricetta di ciascuna sono nel `TUTORIAL.md` sez. 7.
Regole di qualita' (dall'italiano): un solo font/peso/linea di base/ombra per scritta, mai lettere deformate una per una; stessa area e stesse posizioni dell'originale (il gioco ritaglia da
rettangoli fissi); i testi sono quelli dell'originale della lingua (si correggono solo gli errori evidenti); geometrie **misurate sull'originale**, mai copiate dall'italiano.
Tessere con parole spezzate: il taglio va in un varco tra due lettere. Maiuscole accentate (É Ä Ö Ü Ñ): accento troppo alto -> abbassarlo o ridurre il corpo fino a -8% con `clip`.
Rilancia sempre la famiglia **intera**: `Family.finish()` sostituisce tutte le righe della famiglia nel `<l>.ini`.

### 7.3 Il foglio dei numeri del duello (`card_icon03`) — ricetta scelta dall'utente
Un solo foglio con LP, tempo e moltiplicatori; script `strumenti/ui_it/icon03_lingue.py` (aggiungi la lingua a `LINGUE` e rilancia con `--applica`):
- righe 0-180 (cifre piccole, segni, tasti arancioni 1/2/3, cifre grandi 0-9 con "LP", cifre piccole 0-9): **dal pack USA**, pixel art netta;
- le celle in cui il gioco europeo differisce dal pack USA (spunta nera, palla grigia, pillola vuota, parola del tempo): pixel **originali del gioco ingranditi 4x senza sfumare**; la parola
  del tempo e' quella della lingua (TEMPO, TEMPS, TIME, ZEIT, TIEMPO); la pillola arancione ("Single" nell'USA) resta **vuota**;
- righe >= 181 (moltiplicatori x1...x12, icone, carte, frecce): dal foglio italiano gia' nel pack (`strumenti/dati/card_icon03_base_it.png`);
- **attenzione alle fasce**: le celle europee si incollano solo nella loro fascia di righe, altrimenti i pixel europei rovinano la parte alta delle cifre grandi.

### 7.4 Targa del titolo
`python strumenti/ui_it/titolo_pomodoro.py LINGUA`: nome della carta 4930 nella lingua + formula "versione" + bandiera. Vive solo nel modulo della lingua scelta.

## 8. Comporre, installare, provare

1. `componi_pack.py` (base + moduli) e `modulo_ini.py`; **una lingua per volta** per i test (un solo atlante/banner vince). Dopo aver cambiato **un solo PNG** basta copiarlo nel pack installato e riavviare PPSSPP.
2. ISO per i test: `_definitiva` (testi) + pack (texture). La lingua del gioco e' nel **salvataggio**: usa una **copia** del salvataggio dell'utente per le prove e cancellala dopo; non lasciare mai il save di prova al posto di quello vero.
3. Joypad virtuale (`strumenti/upscaling_extra/pad.py`, `pw.py`, `dlg.py`): vedi `TUTORIAL.md` sez. 10. Un tasto qualsiasi salta la sigla; PPSSPP si apre sul secondo monitor.
4. Schermate da vedere: titolo, menu principale, Base dati, editor deck, ricette, negozio, laboratorio, calendario, PDA, VS, duello (HUD, Catena, attacco diretto, fine duello, sasso-carta-forbici), tutorial,
   dialoghi corretti (con le righe segnalate dal box), una carta con testo nuovo nell'album e in duello.

## 9. Trappole ricorrenti (le piu' costose)

- **Contesto che si compatta**: scrivi note e regole su file man mano che leggi; un elenco tenuto solo "in testa" si perde.
- **Heredoc / `python -c`** con accenti o backslash corrompono i file: usa lo strumento di scrittura. Dopo ogni modifica cerca mojibake (`Ã`, `â€™`) nei json/py.
- **Windows**: scritture in modalita' testo aggiungono `\r`; percorsi con spazi tra virgolette; `python -I` non vede il *user site*.
- **`applica_iso` con una sola lingua** sulla ISO finale la sovrascrive: passa sempre tutte le lingue.
- **Una `parte` troppo corta** (es. aggiungere un punto) tocca anche le frasi piu' lunghe che la contengono: usa `esatte`.
- **Chiave di una `esatte` = testo prima delle `parti`**; le `parti` si applicano in ordine.
- **Non decidere da soli** nomi ufficiali, terminologia o scelte discutibili di traduzione: elenca e chiedi.

## 10. Documentare cosa e' cambiato rispetto alla ISO originale (come per it e fr)

Per ogni lingua va prodotto un documento `MODIFICHE_<LINGUA>.md` **generato dai dati reali**, non scritto a mano (modelli: `MODIFICHE_ITALIANO.md`, `MODIFICHE_FRANCESE.md`). Da fare **dopo** aver costruito la ISO `_definitiva` e il pack, dalla radice del progetto, con `L` = `de` o `es`:

```
ISO=PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso
DEF=PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR_definitiva.iso
python strumenti/analisi/documenta_modifiche.py $ISO $DEF L documentazione/modifiche_L   # confronto byte per byte ISO originale/definitiva -> CSV
python strumenti/analisi/confronti_testi.py L                                           # confronti originale -> nuovo con parole evidenziate (md)
python strumenti/analisi/documenta_pack.py $ISO L documentazione/modifiche_L            # struttura del pack, ogni texture ui_L, carte rigenerate, ini
python strumenti/analisi/scrivi_documento_modifiche.py L                                # compone MODIFICHE_<LINGUA>.md
```

Cosa produce (in `documentazione/modifiche_L/`): `carte.csv`, `dialoghi.csv`, `frasi_duello.csv`, `stringhe_ui.csv`, `immagini_iso.csv`, `file_toccati.csv`, `altro.csv`, `riepilogo.json` (ISO); `carte_diff.md`, `dialoghi_diff.md`, `frasi_duello_diff.md`, `stringhe_ui_diff.md` (confronti leggibili con ~~tolto~~ e **aggiunto**); `pack_struttura.csv`, `texture_ui.csv`, `carte_immagini.csv`, `ini_righe.csv`, `riepilogo_pack.json` (pack).

Requisiti: la lingua deve avere `correzioni/regole_L.py` (carte), `dati/ritocchi_dialoghi_L.json`, `dati/correzioni_frasi_duello_L.json`; `regole_stringhe_L.py` e `ui_L` sono opzionali (se mancano la sezione e' vuota: gli script non si fermano). `scrivi_documento_modifiche.py` conosce gia' it, fr, de, es, en; se serve un testo specifico per lingua (elenco dei testi disegnati nelle famiglie di texture, scelte editoriali, stato delle prove in gioco) aggiungi la voce nei dizionari `FAM` e nelle sezioni C/D/F dello script.

**Parte fatta a occhio (non automatica).** Il documento dei **testi disegnati nelle texture** (`documentazione/modifiche_L/testi_texture_L.md`, modelli per it e fr) non si genera: non c'e' un OCR sul PC. Si prepara cosi': per ogni texture di `ui_L` si affianca l'originale della ISO (ingrandito 4x senza sfumare) al PNG HD in un foglio di confronto (`python strumenti/analisi/fogli_confronto_texture.py ISO_ORIGINALE L OUT_DIR`: 6 texture per foglio, originale a sinistra e HD a destra con nome file e origine), si guarda il foglio e si trascrive in tabella il testo di ognuna, segnando in **grassetto** ogni differenza dall'originale (residui di altre lingue corretti, accenti aggiunti, parole cambiate). Le tessere di lettere (`lettere_esito`) si confrontano lettera per lettera; le carte minuscole nelle cartine del tutorial non sono leggibili a quella scala e si danno per buone perche' vengono dai dati delle carte.

**Quando rigenerare**: dopo ogni correzione di testi o texture; i numeri nel documento devono sempre coincidere con la ISO e il pack che si consegnano. Aggiungere sempre `MODIFICHE_<LINGUA>.md` ai file da controllare nella checklist di "fatto" (sez. 11).

## 11. Checklist di "fatto" per una lingua

- [ ] carte: lette tutte, `regole_<l>.py`, `correzioni_carte_<l>.json`, immagini rigenerate, viste in gioco su una carta con testo nuovo;
- [ ] dialoghi: letti per intero con inglese+giapponese, `ritocchi_dialoghi_<l>.json`, avvisi del box controllati in gioco, scene sake/cameriera e `Scr101E` a posto;
- [ ] frasi dei duelli: lette (1.800 uniche), json, `applica_iso` a 0 avvisi;
- [ ] stringhe UI: lette per intero, `regole_stringhe_<l>.py`, 0 avvisi;
- [ ] `ui_<l>` delle 8 famiglie + `card_icon03` + targa; texture "solo italiane" classificate (7.1);
- [ ] ISO `_definitiva` ricostruita con tutte le lingue; pack composto; prova in gioco;
- [ ] `MODIFICHE_<LINGUA>.md` generato (sez. 10) + `testi_texture_<l>.md` letto a occhio;
- [ ] `REGISTRO_SCELTE.md` (+ json), `STATO_LAVORI.md`, `TUTORIAL.md` se il metodo cambia, memoria dell'agente aggiornati;
- [ ] `textures.zip` Android rigenerato con la lingua scelta (o segnalato come da fare).

## 12. Esempi concreti (cosa e' stato fatto, per orientarsi)

| Blocco | Italiano | Francese |
|---|---|---|
| Carte | 181 corrette (letta ogni carta; `regole_it.py`) | 70 corrette (`regole_fr.py`) |
| Dialoghi | base ~1.380 proposte (2.176 righe con i doppioni) + 6 `esatte` + 153 `parti` di rilettura | 16 `esatte` + 178 `parti`; Doyen/Chancelier dialogo per dialogo |
| Frasi duelli | 7 `esatte` + 27 `parti` (letta tutta, 1.792 uniche) | 22 `esatte` + 22 `parti` (letta tutta, 1.832 uniche) |
| Stringhe UI | 505 stringhe in 15 archivi (`regole_stringhe_it.py`) | `regole_stringhe_fr.py` (prima lingua fatta) |
| Texture | pack di base (i testi italiani sono nel pack) | 85 + `card_icon03` nel modulo `moduli/fr/ui_fr` |
| Particolarita' | Preside, Segna-Mostro, Slifer Rosso/Ra Giallo/Obelisk Blu, `NUOVO` e `N` come nell'originale | punteggiatura `! ? : ;`, `Mode aventure`, `TEMPS` |
