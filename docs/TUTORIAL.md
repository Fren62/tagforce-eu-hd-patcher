# TUTORIAL - Come portare la "Versione Pomodoro Mistico" a una nuova lingua (spagnolo, tedesco)

Documento per gli agenti che continuano il lavoro. Scritto l'11-10-2026 dopo aver portato il **francese** quasi allo stesso livello dell'italiano.
**Prima leggi `docs/NEW_LANGUAGE_GUIDE.md`** (e, come modelli completi, `docs/CHANGES_IT.md`/`docs/CHANGES_FR.md`) (linee guida generali, valide per qualunque lingua; questo tutorial ne e' l'approfondimento tecnico con l'esempio francese). Leggi **tutto** prima di toccare qualcosa. Per lo stato corrente e la cronologia vedi `STATO_LAVORI.md`; per la descrizione del pack `LEGGIMI.md`.

Indice
1. Cos'e' il progetto e le regole non negoziabili
2. Come funziona tecnicamente (hash, moduli, ISO)
3. Preparare l'ambiente (e ritrovare i file che servono)
4. Mappa delle fasi per una lingua (checklist)
5. Fase 1 - Testi delle carte e moduli carte
6. Fase 2 - Targa del titolo
7. Fase 3 - Interfaccia HD (la parte lunga): metodo e ricetta famiglia per famiglia
8. Fase 4 - Testi dentro la ISO (carte, dialoghi, frasi dei duelli, stringhe dell'interfaccia)
9. Fase 5 - Comporre il pack e installarlo
10. Fase 6 - Prova in gioco (procedura, comandi, schermate da vedere)
11. Cosa e' stato fatto in francese (registro dettagliato)
12. Stato di spagnolo e tedesco e cose specifiche della lingua
13. Trappole, errori gia' fatti e come evitarli
14. Definizione di "fatto" (checklist finale) e come documentare
15. Appendice: file e script, tabella lingue, testi francesi di riferimento

---

## 1. Cos'e' il progetto e le regole non negoziabili

**Obiettivo.** Un patcher gratuito e open source (Windows + Linux) che, dalla ISO europea di *Yu-Gi-Oh! GX Tag Force* (ULES00600 v1.01, unica versione EU), produce il gioco con: testi delle carte corretti, carte e interfaccia in HD, per it, fr, de, es (e correzioni all'inglese). Funziona con PPSSPP standard, anche Android. La mod si chiama **"Versione Pomodoro Mistico"** (il Pomodoro Mistico e' la carta 4930; il titolo mostra una targa col suo nome nella lingua scelta).
La base grafica e' il pack *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* di **MikeyMK** (USA, ULUS10136) e le carte HD di chrisfand, adattati alla versione EU. Il nostro lavoro: mappare tutto sugli hash EU, rifare i testi nelle lingue, correggere i testi.

**Regole decise dall'utente (rispettale, non riaprirle):**
1. **Nessun font Apple.** Solo font liberi (OFL) tramite `tools/alt_font.py` (che sostituisce ogni font macOS con uno libero). Non reintrodurre percorsi `/System/Library/Fonts`.
2. **Ogni controllo/correzione fatta per l'italiano va estesa a tutte le lingue** (fr, de, es, en). L'italiano e' il riferimento di qualita'.
3. **Non levigare mai le texture di pixel art** (tasti PSP, frecce, bandiere, linguette, mani di sasso-carta-forbici...) senza conferma: l'utente le preferisce in pixel originali. Si levigano solo i fix gia' approvati (cifre x1-x12, tabella Spell Speed, simboli attributi, cifre LP/TURNO). Vedi `STATO_LAVORI.md` sez. 2c.
4. **La ISO originale non va mai modificata**: `apply_to_iso.py` scrive una copia. L'originale e' `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso`; quella corretta e' `ULES00600_YuGiOh_GX_TagForce_EUR_definitiva.iso`.
5. **La targa "Versione Pomodoro Mistico" va inclusa solo per la lingua scelta** (vive in `moduli/<lingua>/intro/title_screen/`; il pack di base ha le tessere originali).
6. **Nessuna lingua deve pesare sull'altra**: ogni lingua e' un modulo (`PSP/TEXTURES/modules/<lingua>/`); l'utente scarica solo la sua.
7. **Non ridistribuire il pack di MikeyMK / chrisfand** finche' non rispondono ai messaggi dell'utente (vedi `PERMESSI_AUTORI.md`). Il patcher futuro deve farselo dare dall'utente. Nei test lo si usa solo in locale.
8. **Chiedi conferma prima di scelte di traduzione discutibili**; non "modernizzare" la terminologia delle carte: si correggono solo errori oggettivi (refusi, accenti, spazi, virgolette, residui di altre lingue).
9. Puoi **chiudere/riavviare PPSSPP** quando serve. Per i test apri la finestra sul **secondo monitor** (WindowX=2570 nel ppsspp.ini); nei test in gioco un tasto salta la sigla.
10. Aggiorna **sempre** la documentazione (`STATO_LAVORI.md`, `LEGGIMI.md`, questo file se cambia il metodo) mentre lavori, non alla fine.

---

## 2. Come funziona tecnicamente

### 2.1 Sostituzione texture di PPSSPP
PPSSPP riconosce una texture dall'**hash dei suoi dati** (xxhash dei pixel, piu' la CLUT se paletted). Nel `textures.ini` (sezione `[hashes]`) ogni riga dice quale PNG usare:

```
0000000000000000<hash dati a 8 cifre> = ui_fr/duel_texts/basic_ff__chain010005.png
```
Con indirizzo/CLUT a zero PPSSPP riconosce la texture dal solo hash dei dati (verificato su tutte le texture del gioco senza collisioni; `common.py`). Lo strumento `tools/gim.py` legge i `.gim` e calcola `gim.data_hash(gim.parse(...))`. I PNG sostitutivi devono essere esattamente **4x** la texture originale (es. 128x32 -> 512x128) e ridisegnare **esattamente** la stessa area di contenuto: il gioco compone le parole da pezzi a posizioni fisse (una scritta spezzata in due texture, una lettera per texture, ecc.).

**Conseguenza fondamentale:** se due lingue hanno una texture con gli **stessi pixel** (stesso hash) la sostituzione vale per entrambe. Cosi' molte texture non vanno rifatte: se il francese ha lo stesso hash dell'inglese, la copre gia' il pack inglese di MikeyMK; se ha lo stesso hash dell'italiano, vale la versione `ui_it`.

### 2.2 Pack di base + moduli per lingua
```
PSP/TEXTURES/ULES00600/            pack di base (EU): cards/, characters/, events/, map/, shop/, ui/, ui_it/, upscale_extra/, intro/ ... + textures.ini
PSP/TEXTURES/ULES00600/_CHOOSE YOUR CARD STYLE/{mikeymk,official_english,official_japanese}/textures.ini   3 stili di carte
PSP/TEXTURES/modules/<lingua>/      un modulo per lingua:
    cards/small_<l>, large_<l>, tiny_<l>, frame/icons_attribute_race_<l>.png, frame/icons_spell_trap_<l>.png
    intro/title_screen/*.png       targa del titolo (solo di quella lingua)
    ui_<l>/<famiglia>/*.png        interfaccia HD della lingua (+ ui_<l>/<famiglia>.ini)
    <l>.ini                        frammento di textures.ini del modulo (righe hash = percorso)
```
`tools/compose_pack.py BASE MODULI CARD_DIR OUT LINGUA... [--copia]` copia il base e **solo** le cartelle `cards`, `intro` e `ui_<l>` dei moduli scelti (hard link, o copia con `--copia` o su un altro volume), poi `module_ini.py` riscrive i `textures.ini`: le righe dei carte localizzate puntano a `cards/small_<l>` / `large_<l>`, e le righe del frammento `<l>.ini` **sostituiscono** le righe del base con la stessa chiave (hash).
Nota: la tabella degli attributi, le etichette e l'atlante delle miniature hanno lo **stesso hash in tutte le lingue**: con piu' moduli installati vince il primo (un solo atlante per installazione).

### 2.3 Archivi del gioco e lettere delle lingue
I dati del gioco sono in archivi `.ehp` (leggibili con `tools/ehp.py`: `ehp.read(path)` -> dict nome -> bytes) che contengono `.gim` (texture), tabelle di testo ecc. Ogni lingua ha una **lettera** e un **codice a 3 lettere**:

| Lingua | codice | lettera (file/hash) | `cardinfo_` | tabella |
|---|---|---|---|---|
| italiano | it | **i** | `cardinfo_ita.ehp` | I |
| francese | fr | **f** | `cardinfo_fra.ehp` | F |
| tedesco | de | **g** | `cardinfo_ger.ehp` | G |
| spagnolo | es | **s** | `cardinfo_spa.ehp` | S |
| inglese | en | **e** | `cardinfo_eng.ehp` | E |
(`tools/languages.py`, `LINGUE`). **Attenzione: il tedesco usa la lettera `g` e lo spagnolo `s`**, non `d`/`e`. La lingua si sceglie con la variabile d'ambiente **`TF1_LANG`** (it|fr|de|es|en); in alternativa un argomento `cardinfo_xxx.ehp` o `TF1_EHP`.

Nomi tipici (esempio italiano -> francese -> tedesco -> spagnolo):
- `deck/all_i.ehp` -> `all_f.ehp` -> `all_g.ehp` -> `all_s.ehp`; membri `window_i0009.gim` -> `window_f0009.gim` -> `window_g0009.gim` -> `window_s0009.gim`
- `title_menu/title_menu_i.ehp` (e `_f`, `_g`, `_s`), `duel/result/result_<l>.ehp`, `tutorial/tutorial_<l>.ehp`
- `duel/basic_ii.ehp` (it), `basic_ff.ehp` (fr), `basic_gg.ehp`, `basic_ss.ehp`: **le lettere sono ripetute**. Gli archivi `basic_if`, `basic_ff`, `basic_bf` sono identici in francese (misurato): si usa `basic_<l><l>`. Verificalo con l'hash per de/es (vedi 7.1).
- `duel/start/start_e.ehp` contiene i membri di **tutte** le lingue (`vs_bg01_1_i0007`, `..._f0007`, `..._g0007`, `..._s0007`) e cosi' `start_all.ehp`; `jnk_card01.gim` si prende da `start_<l>.ehp`.
- `field/always_bri_<ita|fra|ger|spa>.ehp` (calendario `story_sys02.gim`), `database/cardalbum.ehp` (membri `icon06_<l>`, `spelltrap_<l>`).
- **La lingua del gioco viene dal salvataggio**: alla prima partenza il gioco mostra la schermata "Language settings" e la scelta e' scritta nel save (vedi 10).

### 2.4 Dove il gioco usa testo disegnato dal gioco e dove no
- Testi in **texture** (immagini) -> si sostituiscono col pack (questo tutorial, fasi 1-3).
- Testi che il **gioco disegna con un suo font** (dialoghi, nomi dei personaggi, descrizioni delle carte nel deck, menu a tendina, tastiera) -> non sostituibili dal texture pack: si correggono **dentro la ISO** (fase 4). Le descrizioni "grandi" mostrate nelle carte HD sono invece immagini (fase 1).

---

## 3. Preparare l'ambiente

### 3.1 Software (Windows, PowerShell + Git Bash)
- Python 3.12 con: `numpy pillow xxhash opencv-python-headless pycdlib pycryptodome requests pyspellchecker` e, per i test in gioco, `vgamepad` (richiede il driver **ViGEmBus**, gia' installato sul PC dell'utente: si disinstalla da Impostazioni > App).
- PPSSPP in `PPSSPPWindows64.exe`, memory stick in `<cartella dati di PPSSPP>\PSP\` (`SYSTEM\ppsspp.ini`, `TEXTURES\`, `SAVEDATA\`). Impostazioni usate: `ReplaceTextures=True`, `InternalResolution=4`, `Language = fr_FR` e `GameLanguage = -1` (auto), finestra sul secondo monitor.
- **Insidia Windows/pip:** `pip` e `python` possono essere interpreti diversi: installa con `python -m pip install ...`. Non usare `python -I` (modalita' isolata) per gli script che importano numpy/cv2 se i pacchetti sono nel *user site*: fallisce con `No module named ...`. Usa `python -P` (non aggiunge la cartella dello script al path) o niente.
- **Insidia heredoc:** in Git Bash, `\u00xx` e `\\` dentro un heredoc a volte arrivano alterati. Per codice con escape Unicode scrivi il file con lo strumento di scrittura, oppure usa `chr(0xa0)`. Mai incollare percorsi Windows con backslash dentro stringhe Python normali senza `r''`.
- Su Git Bash i percorsi sono `/f/...` e `/c/Users/...`; Python li vuole come `F:/...`.

### 3.2 I tre input esterni al repository (**controlla subito che esistano**)
1. **ISO europea** `PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso` (nel progetto).
2. **USRDIR estratta dalla ISO** (senza `movie/` e `snd/`): serve a tutti gli script `ui_it`. Si estrae con `pycdlib`:
   ```
   python tools/analysis/extract_usrdir.py "PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso" USRDIR
   ```
   (656 file, ~340 MB; crea `USRDIR/duel`, `deck`, `shop`, `labo`, `database`, `title_menu`, `tutorial`, `field`, `script`, `duelsys`, `card`...).
3. **Pack USA di MikeyMK** (`ULUS10136`), serve come *riferimento di stile* (e come fonte dei PNG HD dei menu). Non e' nel progetto e puo' sparire dai file temporanei (e' successo!). Scaricalo dal post del forum PPSSPP (thread **29487**, link Mega nel primo post) con lo scaricatore Python (non c'e' megatools):
   ```
   python tools/analysis/mega_dl.py "<idfile>#<chiave>" pack_usa.zip      # idfile#chiave = parte dopo https://mega.nz/file/
   ```
   poi `unzip` -> cartella `ULUS10136`. Lo zip si chiama *"Yu-Gi-Oh! GX Tag Force 1 HD Remastered.zip"* (1,4 GB, 7.849 file).
   Cartella di lavoro usata finora (fuori dal progetto, cancellabile): `_download_pack_usa\` con `estratto\ULUS10136` e `USRDIR`.

Comando tipo per un generatore dell'interfaccia (da cartella di lavoro):
```
TF1_LANG=fr python "<progetto>/tools/ui_textures/<famiglia>.py" USRDIR estratto/ULUS10136 "<progetto>/PSP/TEXTURES/modules/fr"
```

### 3.3 Strumenti di ispezione (in `tools/analysis/`)
- `dump3.py` / `dump4.py` : contact sheet delle texture originali (bassa risoluzione ingrandita) per leggere i testi. Esempio: `python dump4.py fr.png 3 deck/all_f.ehp:d_window00008.gim shop/all_f.ehp:tab_title.gim` (percorsi dentro la USRDIR; **modifica la costante `U`** in testa agli script se la tua USRDIR sta altrove).
- `compare_tiles.py` : affianca originale (nearest 4x) e HD generato.
- `textures_per_language.py USRDIR LINGUA [--solo-diverse]` : elenca per lingua le texture con hash diverso dall'inglese/dall'italiano (euristica sui nomi: **rumorosa**, include anche mappe; serve per stimare il lavoro e non dimenticare archivi).
- `find_pixelated.py`, `validate_pack.py`, `inventory.py` : controlli sul pack.
- Per i test in gioco: `tools/extra_upscaling/pad.py` (joypad virtuale), `rec.py`, `pw.py`, `dlg.py` (vedi 10).

---

## 4. Mappa delle fasi per una lingua (checklist)

| # | Fase | Strumenti | Stato fr | Stato de / es |
|---|---|---|---|---|
| 1 | Testi carte corretti (tabella) + carte piccole/grandi HD + attributi + etichette + miniature | `correzioni/rules_<l>.py`, `generate_language.py`, `attributi.py`, `extract_labels.py`, `tiny_atlas.py` | fatto | **moduli fatti** (`moduli/de`, `moduli/es`: small/large/tiny/frame), correzioni carte de 23, es 125; da ricontrollare in gioco |
| 2 | Targa del titolo | `ui_it/mystic_tomato_title.py LINGUA` | fatto e visto in gioco | tessere presenti nei moduli (DE "MYSTISCHE TOMATE EDITION", ES "EDICIÓN TOMATE MÍSTICO"); **da vedere in gioco** |
| 3 | **Interfaccia HD** (8 famiglie, ~86 texture per lingua) | `ui_it/*.py` con `TF1_LANG` | fatto (86 texture) | **da fare** (non esiste `ui_de`/`ui_es`) |
| 4 | ISO: carte, dialoghi, frasi dei duelli, stringhe UI | `correzioni/apply_to_iso.py` | tabelle fatte | tabelle fatte (dialoghi de 366 righe, es 114; frasi duello de 4+29, es 29+14) ma **non provate in gioco** |
| 5 | Comporre pack e installarlo | `compose_pack.py` | fatto | da fare |
| 6 | Prova in gioco con la ISO `_definitiva` | pad virtuale | parziale (vedi 11) | da fare |
| 7 | Documentazione | `STATO_LAVORI.md`, `LEGGIMI.md` | aggiornata | da aggiornare |

Ordine consigliato per de/es: 6 (vedi cosa gia' c'e'), 3 (il grosso), 4 (verifica), 5, 6, 7. Per ogni fase verifica **in gioco**, non solo nei file.

---

## 5. Fase 1 - Testi delle carte e moduli carte

(Per de/es e' in gran parte gia' fatto: serve per capire cosa c'e' e come rigenerare.)

1. **Dati dal gioco**: `tools/languages.py` legge dalla tabella `DLG_Text_*` di `cardinfo_<l>.ehp` i nomi dei 21 tipi, le forme "/Effetto", le etichette Magia/Trappola (indici 501..559) e le parole degli attributi (531-539).
2. **Correzioni dei testi**: `tools/corrections/rules_<l>.py` contiene `GLOBALI` (regex -> sostituzione) e `PER_CARTA` (id, campo, vecchio, nuovo, motivo). Il vecchio testo deve esistere **esattamente**. `tools/corrections/generate_italian_corrections.py` produce `dati/card_corrections_<l>.json` (it: `card_corrections.json`). `correzioni/applica.py` e' il punto unico usato da `cardprops.load` e `cardnames.names`, cosi' le immagini e la ISO leggono le stesse correzioni.
   **Solo errori oggettivi**: refusi, accenti, spazi, virgolette, residui di portoghese/inglese. Niente modernizzazione della terminologia.
   Carte corrette oggi: it 116, fr 70 (tabella; 56 nella prima passata + 14), de 23 (18+5), es 125 (90+35), en 15.
3. **Audit** (cerca candidati, non corregge): `tools/audit/audit_language.py LINGUA CARDINFO_LINGUA.ehp CARDINFO_ENG.ehp OUT [UFFICIALE_LINGUA.json UFFICIALE_EN.json]` (categorie: mancante, numeri, spazi, virgolette, refuso, inglese, ufficiale). YGOPRODeck copre solo fr, de, it, pt; **per lo spagnolo non c'e' un database ufficiale scaricabile**, quindi niente confronto automatico: servono controlli ortografici (`audit/accenti.py`, `contesto.py`, `mostra.py`) e lettura. I rapporti sono in `confronti/audit_carte/`.
4. **Moduli**: `python tools/generate_language.py LINGUA PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]` -> `OUT/cards/small_<l>`, `large_<l>`, `tiny_<l>`, `frame/icons_attribute_race_<l>.png`, `frame/icons_spell_trap_<l>.png`, `OUT/<l>.ini`. Senza ID rigenera tutte le carte (2.833 piccole + 2.833 grandi, ~930 MB). Con ID solo quelle, senza atlante (usato dopo aver aggiunto correzioni). Dentro ci sono: `attributi.py` (tabella icone con le scritte della lingua e icona sulle 2.830 carte piccole), l'etichetta Magia/Trappola (`extract_labels.py` -> `dati/label_eu_<codice>_128x32.png`), l'atlante delle miniature del deck (`tiny_atlas.py genera LINGUA PACK OUT` + `tiny_fragment.py`: senza di esso il deck mostra i nomi **inglesi** perche' le 7 pagine hanno lo stesso hash in tutte le lingue).
   Tipografia: francese con spazio non separabile prima di `: ; ! ?` e virgolette « »; tedesco „ “ ; (spagnolo: valutare ¿ ¡). Font liberi: XCharter Bold (nomi/tipo/etichette), Libre Baskerville (effetti), Newsreader Italic (Normali), PT Serif Caption (Magie/Trappole), Charis SIL (glifi mancanti).
5. **Dopo ogni modifica alle correzioni** rigenera solo le carte toccate (`generate_language.py ... ID ...`) **e** ricomponi.
6. **Verifica visiva**: fogli di confronto in `confronti/` (per le carte: `carte_grandi_in_gioco`, `descrizioni_carte_piccole`) e in gioco (album/deck).

---

## 6. Fase 2 - Targa del titolo

`python tools/ui_textures/mystic_tomato_title.py LINGUA` rigenera `moduli/<l>/intro/title_screen/` (2 PNG: `*542eff79685c434d*` e `*705176739829dcf5*`, stesso percorso del pack: sovrascrivono le tessere di base) e rimette le tessere originali nel pack di base. `--applica PACK LINGUA` scrive la targa direttamente in un pack (per PPSSPP). Dettagli: il fondale del titolo e' fatto da 20 tessere 128x64 (`title_menu_i.ehp: main_title00001..00020`, ordine inverso); la targa cade nelle tessere 18 e 19.
Testi (carta 4930 nella lingua del gioco + formula "versione" come nei titoli Pokemon di quella lingua + bandiera): it "VERSIONE POMODORO MISTICO", fr "VERSION TOMATE MYSTIQUE", de "MYSTISCHE TOMATE EDITION", es "EDICIÓN TOMATE MÍSTICO", en "MYSTIC TOMATO VERSION". Font PT Sans Bold. **Visto in gioco in francese** (targa rossa, bandiera, "APPUYEZ SUR LA TOUCHE START" HD sotto). Per de/es: da vedere in gioco; se la formula o il nome della carta nella lingua non convince, correggi lo script e rigenera.

---

## 7. Fase 3 - Interfaccia HD (la parte lunga)

### 7.1 Principio
Gli script `tools/ui_textures/<famiglia>.py` ridisegnano le scritte italiane texture per texture (circa 6.500 righe, 8 famiglie), partendo dall'originale a bassa risoluzione del gioco e dallo stile del pack inglese (riferimento di stile: `ui/text/*.png`, ecc.). Dal 2026-10-11 leggono `TF1_LANG` (default `it`: **risultato italiano invariato**, a meno dei font) e per `fr` sono stati adattati. Per de/es si **replica lo stesso adattamento** famiglia per famiglia.

Regole di qualita' (dall'italiano, valgono sempre):
- le lettere sono regolari: un font, un peso, una linea di base, un'ombra costante; **mai** lettere deformate una per una;
- la stessa area/le stesse posizioni dell'originale: il gioco ritaglia da riquadri fissi;
- niente aspetto "da IA", niente sfocature;
- l'originale della lingua e' il riferimento di **testo**: ridisegna le parole che c'erano (corregendo solo errori evidenti, es. residui di altre lingue), non inventare altro.

### 7.2 Procedura generale per UNA famiglia (ripeti 8 volte)
1. **Capisci quali texture cambiano.** Per ogni membro della famiglia (le liste `FILES`, `TABS`, `TEX`, `LISTS`, ... nel sorgente) calcola l'hash nella tua lingua, in inglese e in italiano:
   ```python
   import sys; sys.path.insert(0,'tools/ui_textures'); sys.path.insert(0,'tools')
   import common                      # common.texture(usrdir, 'deck/all_g.ehp', 'd_window00008.gim') -> (immagine PIL, hash)
   ```
   - hash uguale all'**inglese** -> nulla da fare (lo copre il pack MikeyMK);
   - hash uguale all'**italiano** (e diverso dall'inglese) -> vale la texture `ui_it` gia' fatta (era il caso dei pannelli ricette, di `dmenu_recipe`, `parts`, `conv_machine__window_i0022`);
   - altrimenti **da ridisegnare**.
   Lo stesso controllo, esteso a tutto, lo da' `analisi/textures_per_language.py`.
2. **Leggi gli originali.** `dump4.py` con 2-4x di ingrandimento. Annota il testo di ogni riga, le **parole di altre lingue rimaste nel gioco** (bug dell'originale: es. "SCAMBIA" nel francese, "TAUSCHEN" nell'italiano) e gli errori palesi (es. "2è round").
3. **Parametrizza lo script** per la lingua (vedi 7.3): archivio/lettera, stringhe, e **geometrie** che cambiano (le righe di testo, le caselle bianche, le larghezze, il numero di righe).
4. **Genera in una cartella temporanea** (non nel modulo): `TF1_LANG=de python ui_it/<f>.py USRDIR ULUS10136 tmp`.
5. **Confronta con l'originale** (contact sheet originale vs HD): testi corretti, posizione, dimensione, accenti non tagliati e non sulla riga vicina, colori. Il numero "alfa MAE / colore MAE" stampato dagli script e' solo un indizio: le parole diverse dall'italiano danno errori piu' alti anche se vanno bene a occhio.
6. **Installa nel modulo**: stesso comando con `OUT = PSP/TEXTURES/modules/<l>`. `common.Family.finish()` scrive `OUT/ui_<l>/<famiglia>/*.png`, `OUT/ui_<l>/<famiglia>.ini` e **aggiunge/sostituisce** le righe nel frammento `OUT/<l>.ini` (togliendo prima tutte le righe di quella famiglia). **Trappola:** se rilanci una famiglia con soli sotto-gruppi (es. `duel_texts icons`), le righe degli altri gruppi vanno perse dal `<l>.ini`; rilancia sempre la famiglia **intera** (successo con `duel_texts`: bastava rilanciarlo senza gruppi).
7. **Controlla** `<l>.ini`: ogni riga `ui_<l>/...` punta a un file esistente (snippet in 9.2).

### 7.3 Come sono stati parametrizzati gli script (modello da imitare)
Ogni script ha in testa `LANG = os.environ.get('TF1_LANG', 'it')` e una tabella per lingua. Per de/es **aggiungi le chiavi `'de'` e `'es'`** (lettera `'g'`, `'s'`) alle tabelle esistenti e crea i dati di lingua. Cose condivise:
- `common.Family`: `self.lang`, cartella `ui_<l>`, righe `0000000000000000<hash> = ui_<l>/<famiglia>/<id>.png`, merge in `<l>.ini`.
- Il prefisso degli id file e' solo un nome: conta l'hash.

### 7.4 Ricetta per famiglia (con esempio francese)

Legenda: **IT** = come e' fatto per l'italiano; **FR** = adattamento francese; **DE/ES** = cosa fare/attenzione.

#### A. `duel_texts` (13 texture + `card_icon03`) - archivio `duel/basic_<l><l>.ehp`
Texture: `chain010005` (parola "Catena"), `chain010003` (bagliore grigio), `score-top100011/13` (badge "TURNO" blu/rosso), `next_player0002+0001` e `0005+0004` ("TOCCA AL GIOCATORE SUCCESSIVO" spezzata su 2 texture, **il taglio sta in un varco tra due lettere**), `start_duel10002+10001` ("INIZIA IL DUEL|LO", taglio tra le lettere), `start_duel10005` (bagliore), `dilect_atk00001/3` ("Attacco Diretto!" + bagliore), `card_icon03` (foglio di cifre/segni).
- **IT**: parole composte con un unico font (SF Rounded/Chalkboard/Comic -> font liberi via `alt_font`), stile misurato sull'inglese (`ui/text/chain.png`, `nextplayersturn_blue/red.png`, `start.png`, `duel_2.png`, `direct_attack.png`, `turn_blue/red.png`).
- **FR** (tabella `TXT` in testa, con `b`='ff'): chain `Chaîne`; next `TOUR DU JOUEUR SUIVANT` con `next_cut='TOUR DU JOUEUR SUIV'` (cut tra V e A: l'originale taglia li); start `DÉMARRER DUEL`, `start_cut='DÉMARRER DU'`; attack `Attaque Directe!`; turn `TOUR`. I caratteri `rnext/rstart/rturn` (`'TE'`, `'ED'`, `'TUR'`) sono le lettere **che devono esistere nel testo** e servono a misurare l'altezza delle maiuscole (`solve_line`: `ref` deve essere un sottoinsieme del testo; `TOUR` non ha N, per questo `TUR`).
- **`card_icon03`** (`do_icons_fr`): la texture francese differisce da quella italiana solo in 10 pixel (cella 88,38-97,45); si parte dall'**HD italiano gia' corretto** (`PSP/TEXTURES/ULES00600/ui_it/duel_texts/basic_ii__card_icon03.png`: cifre LP/TURNO lisce, righe 104-111 ricostruite, 100-103 e 148-151 svuotate) e si incollano x4 i pixel francesi che differiscono. **Questo e' il trattamento che toglie i trattini sotto gli LP.** Per de/es fai lo stesso: confronta l'originale con l'italiano (`np.abs(a-b).max(-1)>30`) e incolla le celle diverse.
- **DE/ES**: i testi possono essere molto piu' lunghi: leggi l'originale tedesco/spagnolo. Il vincolo e' la larghezza degli slot: il banner "TOCCA AL GIOCATORE" riempie la texture, il solver `place_line` comprime (<=10%), allarga i bordi (`grow`), e restringe il kerning; se non basta riduci la dimensione. Maiuscole accentate (Ä Ö Ü É Ñ): vedi 13.
- Comando: `TF1_LANG=fr python ui_it/duel_texts.py USRDIR ULUS10136 <modulo>` (senza gruppi = tutti: `chain next start attack turn icons`).

#### B. `result_letters` (22 texture) - `duel/basic_<l><l>.ehp`
Una **tessera 64x64 per lettera**, composte dal gioco: win `duel_win1000{02..14}` + silhouette `duel_win100016`, lose `duel_lose1000{02..16}`, draw `duel_draw1000{02..12}`.
- **IT**: "HAI VINTO" (HAIVNTO, 7 tessere + silhouette), "HAI PERSO" (HAIPERSO, 8), "PAREGGIO" (PAREGIO, 7). Lettere Times Bold con gradiente, contorno viola, ombra; lettere I N O S dal contorno inglese; gradienti e colori misurati.
- **FR** (`LETTERS`): win `TUASGNÉ` (7: T U A S G N É) + silhouette 16 "TU AS GAGNÉ"; lose `TUASPERD` (8); draw `EGALIT` (6: l'originale usa E senza accento, **non c'e' una tessera É nel pareggio**). Differenze di codice: `'S'` anche nel set "win" (forma presa da `ui/text/lose/s.png`); `accent_down()` abbassa l'accento di Times sulla É (era piu' alto di quello del gioco e veniva tagliato); parametro **`wide`** (calibrato, solo fr) per le tessere di EGALIT piu' larghe; il test per la silhouette della win cambia (`let.member == 'duel_win100014.gim'` per fr).
- **DE/ES**: conta le tessere reali (`duel_win1000NN` fino a...): il numero e l'ordine delle lettere dipendono dalla lingua e **vanno letti dall'originale** (contact sheet delle tessere), incluse le lettere ripetute (il gioco riusa la stessa tessera). Controlla le lettere accentate.

#### C. `menu_lists` (6 texture) - `title_menu/title_menu_<l>.ehp`, `duel/result/result_<l>.ehp`, `field/always_bri_<ita|fra|ger|spa>.ehp`
Liste di titoli (`m_menu_title01` giallo, `trnsmt02` lista wireless argento, `menu02` risultato duello, `press_start0003`), foglio icone dei risultati (`result_<l>__menu01` con 3 parole), calendario (`story_sys02`).
- **IT**: righe di testo a passo fisso di **21 righe** per riga (`line_rows`), font Futura Bold (-> libero) con peso/corpo fissi (`size`, `bold`), stile e colori misurati sulle immagini inglesi (`en_text`, `en_use`: quale riga inglese serve per i colori), righe condensate (`cond`) dove lo e' anche l'originale.
- **FR** (`FR` dict): testi in 6+11+6+1 righe (vedi appendice). Gotcha:
  1. **`line_rows(L, n=...)`**: le maiuscole accentate (É) toccano la riga sopra e la rilevazione automatica fonde due righe; con `n` noto si usa il passo fisso (si prende **il massimo** tra le altezze di riga pulite, 21).
  2. **Accenti fuori dal riquadro**: l'accento di Futura e' piu' alto di quello originale e finiva sulla riga sopra come puntini (visto in gioco in "SAISIR NOM"). Fix: dopo il fit le righe con maiuscole accentate riducono il corpo fino al **-8%** per entrare (`k_fixed`); se non basta l'accento viene **tagliato** al bordo (`ln.clip`, applicato in `hd_coverage`).
  3. Il campione "orig_text" (`orig_text={4:'SCAMBIA'}`): quando il testo che vuoi scrivere e' diverso da quello che c'e' nella texture originale (residuo italiano), si da' all'algoritmo la parola **originale** per misurare larghezza/spaziatura e si scrive la nuova col `fit_free`.
  4. Etichette `LABELS` del foglio icone: nel francese **non sono condensate** (5-7 lettere): `LABEL_SPEC=FUTURA_BOLD`, `LABEL_SX=(0.95,1.25)`; per l'italiano `FUTURA_COND_XB`, `(0.9,0.9)`.
  5. Calendario: `CAL_SERIF` (giorni/mesi, Times Bold), `CAL_ROUND` (parole crema con contorno marrone), cifre `0123456789月日ー` (Hiragino, uguali in tutte le lingue). Per fr: Dimanche, Lundi, Mardi, Mercredi, Jeudi, Vendredi, Samedi; Mai, Juillet, Juin, Août; "jours" / "avant le tournoi"; Matin / Soir. Le caselle (box) sono le stesse dell'italiano. Per de/es i nomi cambiano (giorni/mesi lunghi: controlla che entrino nei box: `Fitter.fit_set` comprime fino a `sx_min=0.9`, poi riduce il corpo).
- **DE/ES**: testi dei menu **diversi per lunghezza**: le righe di `trnsmt02` e `m_menu_title01` hanno ampiezza fissa (256 px): `LISTE CARTES TÉLÉCHARGÉE` entra a ~0.93, parole tedesche lunghe (es. "Kartenliste heruntergeladen") richiedono compressione/corpo piccolo. Valuta se le stringhe del gioco originale sono gia' abbreviate: **riproduci quelle**.

#### D. `icon_sheets` (3 texture per fr) - `deck/all_<l>.ehp`, `shop/all_<l>.ehp`
Fogli di icone dove cambiano poche parole: `icon04` (partenza dal foglio inglese HD e **solo i pixel che cambiano** in pixel x4, es. "Mia/Moi" e distintivi "A/L"), `s_pack` ("ESAURITE"/"ÉPUISÉ" in PT Sans Bold sul rosso del pack), `panel` (la scritta del tab "prati"/"hetés": **e' un frammento** di una parola che continua in un'altra texture; riproduci il frammento dell'originale, non la parola intera).
- **FR**: costanti `SP_TEXT`/`SP_X` (x0..x1 dell'inchiostro in HD: 45..228), `PANEL_TEXT='hetés'`, `TEXTURES_FR` (solo 3 voci; `pda_pack01`, `ocglist`, `icon06`, `mein_menu00`, `trnsmt01` hanno **lo stesso hash dell'inglese in francese** e non vanno rifatte), `build_icon04_fr` (usa `EN_LOW`, la texture inglese a bassa risoluzione, per trovare i pixel che differiscono; dilata di 1 px; il documento col fulmine `bolt_doc(...)` resta come nell'italiano).
- **DE/ES**: stesso controllo hash: probabilmente solo `icon04`, `s_pack`, `panel` differiscono. Misura x0/x1 della parola con la stampa ASCII (`low[232:246]`) o guardando l'originale a 8x.

#### E. `deck_screens` (10 texture per fr) - `deck/all_<l>.ehp`, `labo/*.ehp`, `shop/all_<l>.ehp`
Linguette dell'editor del deck, del laboratorio, del negozio (Cassa, Affitto, Laboratorio, Convertitore, "Tipi di Carte Posseduti", "Carte Comprate / Tipi di Carte com...", tasto INVIO).
- **FR** (`TEX_FR`): Coffre x2, Location x3, Labo, Convertisseur, "Types de cartes acquis", "Cartes achetées" + "Types de cartes ac" (la seconda e' un **frammento** al bordo della texture), ENTRÉE. `white_box(low)` ricava automaticamente (colonne con >=9 righe bianche) i parametri `box_x0`, `right` che per l'italiano erano scritti a mano; regola: larghezza <20 -> margine 2, altrimenti 1. `key_caption(low)` (ENTRÉE) vettorizza dall'originale: vale per ogni lingua. Stesse parole in francese di "Fusion/Side/Deck" (hash = inglese: lo fa il pack).
- **DE/ES**: elenca quali di queste texture differiscono dall'inglese; scrivi le parole; verifica che la linguetta non vada fuori dal tab (parole lunghe: `tabword.render_tab_word` comprime e riduce il corpo; `TAB_CAP=44`).

#### F. `recipe_screens` (11 texture per fr) - `deck/recipe_view_<l>.ehp`, `title_menu/title_menu_<l>.ehp`, `database/limitlist.ehp`
Linguette: Personnage / Utilisateur / Téléchargée / Limitée / Semi-limitée / Interdite / Échange.
- **FR** (`FR_WORDS` + `TABS_FR`): la **geometria** (`ix`, icona, `tx`, `slot`) e' quella italiana (stessi riquadri); cambiano parola e **limite destro** del testo `tx[1]` misurato sull'originale (script: colonne di pixel bianchi >=230 tra x0 e la casella). Pannelli `recipe_panel`, `dmenu_recipe`, `parts`, `recipe010002/4/6` hanno lo **stesso hash in tutte le lingue**: restano `ui_it`.
- `Scambia` nel francese e' un **residuo italiano** del gioco: scritto `Échange` (come l'italiano ha "Scambio" al posto del tedesco "Tauschen").
- **DE/ES**: stessa cosa; per i limiti usa le parole dell'originale (es. "Eingeschränkt/Halb eingeschränkt/Verboten" sono lunghe: attenzione al limite destro).

#### G. `vs_screen` (14 texture) - `duel/start/start_e.ehp` (membri `_<l>`), `start_all.ehp`, `start_<l>.ehp`
DUEL / NORMAL / TAG (banner grandi in Times Bold con gradiente rosso-giallo), bagliori "DUEL NORMAL" / "TAG DUEL", "Modalita' ..." (due), "n A GIOCARE" (due), "n Duello" (tre: `vs_much1..3`), foglio sasso-carta-forbici (`jnk_card01` con le parole VITTORIA/SCONFITTA/PAREGGIO), foglio giocatori (`d_menu01_<l>` con i 4 distintivi "n° GIOCATORE" e la linguetta GIOCATORE).
- **FR** (`main_fr`, `FILES_FR` derivato da `FILES` sostituendo `_i0`->`_f0`, `start_i`->`start_f`):
  1. **Banner**: `banner_fit(text, low)` cerca corpo, compressione, posizione e base in modo che il riquadro dell'inchiostro (alfa>1/2, contorno e ombra inclusi) coincida con quello dell'originale (6 iterazioni): il gioco **allarga** le parole a riempire la texture, quindi i parametri fissi dell'italiano non vanno bene. Parole fr: `DUEL`, `NORMAL`, `TAG`.
  2. **Bagliori**: per fr si ricavano dall'alfa originale (`glow_from_original`) per entrambi.
  3. **"A giocare"**: `giocare_text(testo, shape, sinistra, destra)`: intera frase con tracking per riempire la larghezza misurata (HD px): `DEUXIÈME À JOUER` (148..876), `PREMIER À JOUER` (180..848).
  4. **Round**: `round_text`: `1er round` (66..446), `2e round` (82..430), `3e round` (90..442) (l'originale ha "2è/3è").
  5. **Modalita'**: `mode_word('Mode Un Duel', ..., base 52, 32..476)` e `('Mode Match', 60..452)`; l'italiano ha base 84 per l'accento della "à"; misura le estensioni del **riempimento** colorato (`np.abs(a-colore).sum<60`).
  6. **jnk**: `JNK.update(size=81, base=1017)` (le lettere francesi sono alte 17 righe contro 11) e parole `GAGNÉ`, `PERDU`, `EGALITE` con `(sinistra, destra)`; si calcola prima la compressione (0.8-1.15) e poi il tracking.
  7. **d_menu01**: `BADGE_TXT=['1er JOUEUR','2e JOUEUR']*2` (Helvetica 42), linguetta `JOUEUR` (`TAB_WORD`) **piu' stretta** di quella inglese: `TAB_DW=-16` (colonne tolte dal corpo e filetto allungato per non spostare il resto), corpo dell'Arial Black adattato (`fit_size`, max 33).
- **DE/ES**: stessa struttura. Probabili differenze: "SPIELMODUS: Einzel/..."; il tedesco ha parole molto lunghe -> compressione maggiore; la linguetta giocatore puo' essere piu' larga (dw>0).

#### H. `tutorial` (6 texture) - `tutorial/tutorial_<l>.ehp` (membri `tuto_duelimg01..06`)
Illustrazione 01: finestra di dialogo (sfondo del duello, riquadro, bottoni OUI/NON, carta piccola, due-tre righe di testo); 02-06: cartina di una carta con disco del tipo (equip, continua, contro, rapida, terreno).
- **FR** (`LANG`, `LL`): `FILE=tutorial/tutorial_f.ehp`, **`TF1_EHP`** impostato prima di importare `small_it` (sennò prende i termini italiani: "[CARTA MAGIA]"), testi `Ton adversaire a déclaré le duel.` / `Activer l'effet de la carte ?` (spazio non separabile prima del `?`), bottoni `OUI`/`NON`, `TEXT_BASE=(27.0, 36.6, 46.1)` (2 righe), **geometria diversa dall'italiano** (misurata sull'originale: riquadro `BOX=(37,10,219,107)`, bottoni `BTN_BLUE_AT=(72.75,48.875)`, `BTN_CREAM_AT=(137,49.125)`, `BTN_LABEL base=60.7`, carta piccola `MINI_AT=(120,75,16,24)`, `FIELD_RECT=(29,2,227,114)`) perche' il dialogo ha una riga in meno. Nome, descrizione e etichetta delle 5 carte arrivano da `cardinfo_fra.ehp` (cid fissi: 4317, 5161, 4863, 5355, 4340); l'atlante etichette si genera con `label_it.py` (lanciato **senza** `-I`).
- **DE/ES**: ricalcola la geometria misurando (script in 7.5); controlla se il dialogo ha 2 o 3 righe e dove stanno i bottoni; ricorda `SI`/`NO` (es: "JA/NEIN", "SÍ/NO").

### 7.5 Snippet di misura usati (adattali)
- Bounding box di un colore in una texture bassa (HD = x4): `m=(a[...,3]>200)&(np.abs(a[...,:3]-col).sum(-1)<tol); ys,xs=np.where(m)`.
- Righe a passo fisso: le righe iniziano a multipli di 21 (menu a lista); controlla con `line_rows`.
- Estensione del testo bianco di una linguetta: `(a[...,:3].min(-1)>=230)&(a[...,3]==255)` tra x0 e la casella.
- Differenze tra due lingue: `np.abs(a-b).max(-1) > 30` poi `cv2.connectedComponentsWithStats` sulla maschera dilatata per ottenere le celle.

### 7.6 Quando una texture ha lo stesso hash ma ancora testo inglese
Le texture identiche all'inglese restano in inglese anche nel gioco originale (es. "NO DATA", "Deck/Fusion Deck/Side Deck", "Standby Phase", "Draw Phase", "Main Phase", "Duel Result"-banner): **non e' un errore del pack**, e' l'originale. Non si sostituiscono senza una decisione dell'utente.

---

## 8. Fase 4 - Testi dentro la ISO

Il testo disegnato dal gioco con il suo font non si cambia col pack. `tools/corrections/apply_to_iso.py ISO_ORIGINALE ISO_CORRETTA [LINGUA ...]` crea una copia con (ogni lingua con una tabella):
1. **Testi carte** (`duelsys/cardinfo_<l>.ehp`: `CARD_Name_X.bin`, `CARD_Desc_X.bin`, `CARD_Indx_X.bin`) da `dati/card_corrections_<l>.json`.
2. **Dialoghi** (`script/stNN_*_<l>.ehp`): `correzioni/dialoghi.py` con `dati/dialogue_corrections_<l>.json` (id `st01_t01/Scr077E#3` -> attuale, proposto). Ogni scena e' una coppia di file (gz o no): `...Ii` (offset in caratteri UTF-16) e `...Li` (stringhe UTF-16LE chiuse da NUL). Vincoli: **larghezza 46 caratteri** per riga (il gioco non va a capo da solo; l'originale arriva a ~49), **max 3 righe** nel box (7 proposte italiane ne hanno di piu': da vedere in gioco), un segnaposto `《...》` vale ~6 caratteri, spazio prima e dopo i segnaposto (regole automatiche in `build_dialogues.py`; fr: spazio prima di `! ? : ;`; de: caso `》s`).
3. **Frasi dei personaggi nei duelli** (`chr_wordstbl_<l>.bin`/`02chr_wordstbl_<l>.bin` dentro `duel/cutin_*.ehp`, `zakov*`): `correzioni/duel_lines.py` con `dati/duel_line_corrections_<l>.json` (`esatte`: frase intera; `parti`: sostituzioni). **Attenzione ai file `*-ptrs.txt`** negli archivi dei personaggi: contengono gli **offset assoluti** dei membri; se una tabella cresce vanno aggiornati (`rimappa_puntatori`) o il duello va in **crash** (`Invalid Memory Access` a 0x20). 237 frasi in 66 archivi per tutte le lingue insieme.
4. **Stringhe dell'interfaccia** (`dati/ui_texts.json`): correzioni puntuali a `strTbl.bin`, `ddstrtbl_<l>.bin`, `help_strtbl_label_<l>.bin`: etichette tagliate dal bordo (it: "Assistenza"->"Aiuto", "Posizionam"->"Posiziona"), stringhe di un'altra lingua nelle tabelle (it "Kartenrand"->"Cornice", fr "Cornice della Carta"->"Cadre de la carte", de "Couleur de cadre"->"Kartenrand", es accento mancante). Per trovare le etichette a rischio: `audit/long_labels.py ISO [rapporto>=1.4] [lunghezza minima 9]`. Candidati segnalati e **da verificare in gioco**: FR "Rechercher", "Aucune restriction", "Étiquette"; DE "Ausführen", "Keine Beschränkung", "Sortieren", "Beschwören", "Schließen"; ES "Invocación".
5. **Etichetta [CARTA MAGIA]/[CARTA TRAPPOLA] della carta grande nel duello**: in tutti i `duel/basic_XY.ehp` c'era l'etichetta inglese (hash c2268340); `apply_to_iso.py` copia `card_spell_trap.gim` di `field/always_<l>_<l>.ehp`. Verificato in gioco **solo per l'italiano**.
6. **Bug del gioco originale**: scena `st02_t01/Scr101E` righe 22-27: il testo e' **ruotato tra le lingue** (it ha francese, fr tedesco, de inglese, es italiano); `build_dialogues.py` rimette ognuno nella sua lingua (lo spagnolo e' stato tradotto da noi).

Flusso per i dialoghi (de/es):
```
python tools/audit/extract_dialogues.py ISO_ORIGINALE confronti/audit_dialoghi        # dialoghi_<l>.tsv (id, testo, inglese, giapponese)
# leggi (a mano, su elenco di righe uniche) e registra i ritocchi in dati/dialogue_touchups_<l>.json  {"esatte":{riga:nuova}, "parti":[[vecchio,nuovo]]}   (a capo scritti ⏎)
python tools/corrections/build_dialogues.py LINGUA                               # -> dati/dialogue_corrections_<l>.json
python tools/corrections/apply_to_iso.py ISO_ORIGINALE ISO_DEFINITIVA                 # tutte le lingue
```
Metodo dell'audit gia' usato: correttore ortografico (`pyspellchecker`) sulle parole rare + controllo delle righe in lingua sbagliata + lettura. **Il francese e' stato letto per intero (righe uniche), tedesco e spagnolo pure; le correzioni sono di `parti` (fr 105 parti, de 180, es 67)**. Per l'italiano la revisione e' stata piu' profonda (1.378 proposte applicate e propagate ai doppioni: 2.176 righe). Obiettivo per fr/de/es: portare la qualita' al livello dell'italiano con una seconda lettura mirata (grammatica, accordi, punteggiatura, terminologia coerente con le carte e coi nomi dei luoghi).
Decisione aperta (da chiedere all'utente): **"Doyen" vs "Chancelier"** in francese. Nel gioco originale il personaggio e' "Doyen Sheppard" (nome del parlante, 15 dialoghi) ma il luogo e' "Le Bureau de chancelier"; due frasi (`l'histoire du Doyen`, `J'accepte, Doyen.`) sono state cambiate in "Chancelier" nei ritocchi: **incoerente** con le altre. Il nome del parlante non e' nei dialoghi ma in un'altra tabella dello stesso archivio. Va deciso un solo termine (il doppiaggio francese ufficiale usa "Doyen"/"directeur" a seconda della fonte: non assumere).

---

## 9. Fase 5 - Comporre il pack e installarlo

### 9.1 Comporre
```
python tools/compose_pack.py PSP/TEXTURES/ULES00600 PSP/TEXTURES/modules <USRDIR>/card <USCITA> fr --copia
```
(con `--copia` perche' PPSSPP sta su `C:` e il progetto su `F:`; senza, hard link). Si possono dare piu' lingue, ma **un solo banner/atlante/tabella attributi vince** (il primo): per test usa **una lingua per volta**.
Il pack composto va in `<cartella dati di PPSSPP>\PSP\TEXTURES\ULES00600`. Il pack italiano gia' installato li' non va perso: **rinomina** (`ULES00600` -> `ULES00600_it_installato`) prima di mettere quello nuovo, e rimettilo a posto a fine prova.
Dopo avere cambiato **un solo PNG**, basta copiarlo nel pack installato (il `textures.ini` non cambia) e **riavviare PPSSPP** (le texture sono in cache).

### 9.2 Controlli automatici
```python
import os,re
M='PSP/TEXTURES/modules/fr'
for l in open(f'{M}/fr.ini',encoding='utf-8'):
    m=re.match(r'^([0-9a-f]{24})\s*=\s*(\S+)',l)
    if m and m.group(2).startswith('ui_fr/') and not os.path.exists(f'{M}/{m.group(2)}'): print('manca',m.group(2))
```
In ogni `textures.ini` composto (anche `_SCEGLI LO STILE.../*/textures.ini`) devono comparire tutte le righe `ui_<l>/`. Ogni hash `ui_<l>` e' gia' presente nel `textures.ini` di base (puntava a `upscale_extra` o all'inglese): il frammento **sostituisce** quella riga, non la duplica (nessun hash duplicato).

### 9.3 Impostazioni PPSSPP consigliate
Sostituisci texture ON; risoluzione di rendering **4x** (e' quella che migliora davvero: a 4x/Auto lo shader 4xBRZ e' spento: per questo le texture non coperte sono ingrandite nel pack in anticipo, `upscale_extra`); lingua di sistema del gioco = quella del modulo. `textures.zip` per Android (2,5 GB) va **rigenerato** con le correzioni e il banner della lingua scelta (non fatto per fr; non provato su telefono).

---

## 10. Fase 6 - Prova in gioco

### 10.1 Preparazione
- Chiudi PPSSPP se aperto. Metti il pack della lingua in `Documents\PPSSPP\PSP\TEXTURES\ULES00600` (vedi 9.1).
- **Salvataggi**: la lingua del gioco e' scritta nel salvataggio. In `Documents\PPSSPP\PSP\SAVEDATA` ci sono: `ULES006000001.OFF` (il salvataggio **italiano** dell'utente, messo da parte dalla sessione precedente), `ULES006000001.FR_PROVA` (quello creato da me nelle prove francesi). **Non rinominare quello di prova col nome originale mentre l'utente gioca in italiano.** Per provare con un salvataggio: rinomina quello della lingua in `ULES006000001`; a fine prova rimettilo (`.XX_PROVA`). Senza salvataggio il gioco mostra la schermata di scelta lingua e, alla conferma del nome, crea un **nuovo** salvataggio ("Un nouveau fichier sera créé sur le Memory Stick" -> OUI): ricordati di spostarlo.
- ISO: per testare **dialoghi e correzioni** usa `ULES00600_YuGiOh_GX_TagForce_EUR_definitiva.iso` (rigenerala con `apply_to_iso.py` se hai cambiato le tabelle); per testare **solo le texture** va bene l'originale (ma non vedrai le correzioni dei testi).
- Avvio: `Start-Process 'PPSSPPWindows64.exe' -ArgumentList '"<ISO>"' -WorkingDirectory 'F:\Games\PPSSPP'`. La finestra va sul secondo monitor (ini).

### 10.2 Joypad virtuale (l'unico modo affidabile per i comandi)
I tasti inviati con `PostMessage`/`keybd_event` **non arrivano**. Si usa il driver ViGEmBus con `vgamepad`:
1. Copia `tools/extra_upscaling/pad.py` in `%TEMP%\vigem\` (i file temporanei **vengono cancellati da altre sessioni**: tieni la copia nel progetto), crea `%TEMP%\vigem\cmd.txt` vuoto e avvia `python -P pad.py` in background.
2. Mandi comandi aggiungendo righe a `cmd.txt`: `btn A [ms]`, `btn START`, `btn UP|DOWN|LEFT|RIGHT|B|X|Y|LB|RB|BACK`, `seq DOWN,DOWN`, `wait 2.5`, `shot nome variante`. Mappa PPSSPP: A = Croce (conferma), B = Cerchio, X = Quadrato, Y = Triangolo, START = Start.
3. Screenshot: `python -P pw.py out.png` (cattura la finestra di PPSSPP anche se coperta, via `PrintWindow`); registrazione a intervalli: `python -P rec.py DIR SECONDI` (salva solo i fotogrammi che cambiano). Poi montaggio dei fotogrammi unici (diff su 160x90) per guardarli a griglia.
4. `tools/extra_upscaling/dlg.py N`: preme A finche' la finestra di dialogo (riquadro crema in basso) sparisce, max N volte; attenzione: premere A **senza** dialogo nell'ufficio apre il menu e "Parler" avvia un nuovo dialogo (si resta in loop).
5. Se il pad non risponde, controlla che `pad.py` giri ancora e che `log.txt` sia aggiornato (il file `vigem` puo' essere stato ripulito: ricopia `pad.py`).

### 10.3 Percorso di prova (con salvataggio esistente)
Intro -> START (piu' volte) -> titolo ("Nouveau jeu" / "Continuer") -> `Continuer` -> "Données chargées." -> OK -> **Menu principale** (`Mode aventure`, `Duel libre`, `Menu Deck`, `Base de données`, `Mode Réseau`, `Options`, `Sauvegarde de données`, `Sélection de la langue`): il cursore **ricorda la voce**; `Duel libre` e' disattivato finche' non si sblocca.
- `Menu Deck` -> `Modification du Deck` (editor del deck) e `Visualisateur de Recettes`.
- `Base de données` -> `Liste des Duellistes`, `Album de cartes`, `Tutorial`, `Classement Duel`, `Liste des Cartes Interdites/Limitées`.
- `Mode aventure`: ufficio del cancelliere (menu `Parler / Duel / Objets / PDA / Vers la carte`, calendario in alto a destra, riquadro del luogo), negozio, laboratorio, tutorial, duelli.
- **Nuovo gioco**: titolo -> `Nouveau jeu`; scelta lingua (frecce + A); filmato; "Entre un nom" (tastiera di sistema: A inserisce i caratteri fino a 8; **START (Terminer)** conferma — dopo aver riavviato `pad.py` se non risponde); "Appuie sur START pour confirmer" -> START -> "Un nouveau fichier..." -> OUI -> salvataggio -> storia: i dialoghi avanzano **solo con A a ogni riga**, B non li salta.
- **Duello dimostrativo**: lasciando il titolo fermo ~1 minuto parte un duello automatico (utile per VS, HUD, TURNO, "TOUR DU JOUEUR SUIVANT", testi del duello).

### 10.4 Schermate da vedere (stato in francese)
| Schermata | Che cosa guardare | fr |
|---|---|---|
| Scelta lingua, nome | testi di sistema (non sostituibili) | visto |
| Titolo | targa, "APPUYEZ SUR LA TOUCHE START" HD, menu | **visto** |
| Menu principale + Base de données + Menu Deck | titoli HD, voci lunghe non tagliate ("Liste des Cartes Interdites/Limitées") | **visto** |
| Editor del deck | linguette (Deck/Fusion/Side/Coffre), "Types de cartes acquis", "Aide" (il "?" tagliato), START | **visto** (lista vuota perche' nuova partita) |
| Finestra Ricette | "Visualisateur de Recettes", "Utilisateur", "Personnage"; "NO DATA" resta inglese (originale) | **visto** |
| Conferma "Terminer la modification du Deck" | OK / ANNULER (testo di sistema) | visto |
| Calendario nell'ufficio | "1 Mai / Lundi", "92 jours avant le tournoi", ora, DP | **visto** |
| Menu dell'ufficio | Parler / Duel / Objets / PDA / Vers la carte (testo di sistema) | visto |
| Schermata VS | DUEL NORMAL, Mode Un Duel, giocatori, Contre | **visto** (demo) |
| Duello: HUD, TOUR n, TOUR DU JOUEUR SUIVANT, descrizioni | | **visto** (demo) |
| Duello: Chaîne, Attaque Directe!, fine duello, schermata "A giocare", sasso-carta-forbici | | **non visto** |
| Tutorial (illustrazioni), negozio (ESAURITE/ÉPUISÉ, tab "Cartes achetées"), laboratorio (Convertisseur, Labo, Location), PDA, album (carte nuove) | | **non visto** |
| Carta grande nel duello con etichetta Magia/Trappola | con ISO `_definitiva` | non visto in fr |
| Dialoghi corretti in storia | con ISO `_definitiva` | non visto in fr |

Nel Tutorial della Base de données e nella Liste des Duellistes la lista era **vuota** (nuova partita): serve avanzare nella storia o usare un salvataggio piu' avanzato dell'utente.

---

## 11. Cosa e' stato fatto in francese (registro dettagliato)

Cronologia (2026-10-10 / 11):

**Gia' prima di questa passata** (vedi `STATO_LAVORI.md` 2b/2c): carte piccole e grandi HD (2.833+2.833), tabella degli attributi e icone sulle carte piccole con parole francesi (`LUMIERE, TENEBRES...`), etichette Magia/Trappola (`label_eu_fra_128x32.png`, hash 6fd4b083), atlante delle miniature (`cards/tiny_fr`, 7 pagine, `fr.ini`), correzioni dei testi delle carte (70), dialoghi (238 righe corrette, letti per intero), frasi dei duelli (19 esatte + 16 parti), `apply_to_iso` su tutte le lingue, targa del titolo.

**Questa passata:**
1. **Recuperato il pack USA** (era sparito): scaricato da Mega (`mega_dl.py`, thread 29487) e **estratta la USRDIR** dalla ISO (`extract_usrdir.py`).
2. **Script parametrizzati per lingua** (`TF1_LANG`): `common.py`, `duel_texts.py`, `result_letters.py`, `menu_lists.py`, `icon_sheets.py`, `deck_screens.py`, `recipe_screens.py`, `vs_screen.py`, `tutorial.py`. `compose_pack.py` copia anche `ui_<l>`.
3. **86 texture francesi** nel modulo `moduli/fr/ui_fr` (86 righe `ui_fr` in `fr.ini`): duel_texts 14 (compresa `card_icon03`), result_letters 22, menu_lists 6, icon_sheets 3, deck_screens 10, recipe_screens 11, vs_screen 14, tutorial 6. Testi francesi in appendice.
4. **Correzioni scoperte dalla prova in gioco**: (a) i trattini sotto gli LP e le cifre TURNO erano la vecchia texture xBRZ di `card_icon03` -> rifatta dall'HD italiano con i 10 pixel francesi; (b) accenti delle maiuscole che uscivano dal riquadro ("SAISIR NOM") -> riduzione fino a -8% + `clip`.
5. **Prove in gioco** (ISO originale e `_definitiva`, `Language = fr_FR`): titolo, menu principale, Base de données, Deck editor, Recettes, calendario, VS, duello dimostrativo, dialoghi dell'ufficio: tutte le texture sostituite risultavano corrette. Il salvataggio di prova e' in `SAVEDATA\ULES006000001.FR_PROVA`; il pack francese di prova in `TEXTURES\ULES00600_fr_prova`.
6. **Scelte di traduzione** (da confermare dall'utente se vuole altro): "ÉCHANGE" al posto di "SCAMBIA"; "2e/3e round" al posto di "2è/3è"; "EGALITE" senza accento (limite del gioco); "Mode Un Duel" mantenuto come nell'originale (si potrebbe preferire "Mode Duel Simple"); "DÉMARRER DUEL" come nell'originale (non "DÉMARRER LE DUEL": troppo lungo per la texture).

**Cosa il francese ha e l'italiano NO** (per non dimenticarlo): niente di sostanziale; l'italiano ha una revisione dei dialoghi e delle carte piu' profonda.
**Cosa l'italiano ha e il francese NO**: revisione profonda dei dialoghi (1.378+ vs 238), audit delle carte contro il database ufficiale con lettura manuale (116 vs 70), verifica in gioco di molte piu' schermate, correzioni alle stringhe corte del gioco (it "Aiuto"...; per fr le etichette lunghe da verificare), tutorial/negozio/laboratorio/PDA non ancora visti in francese, `textures.zip` Android.

---

## 12. Stato di spagnolo e tedesco e cose specifiche

### 12.1 Cosa esiste gia'
| Elemento | de | es |
|---|---|---|
| Modulo carte (`moduli/<l>/cards`) | si (small/large/tiny/frame) | si |
| Targa del titolo | si (nei moduli) | si |
| Correzioni carte | 23 | 125 |
| Correzioni dialoghi (`dati/dialogue_corrections_<l>.json`) | 366 righe (180 parti) | 114 righe (67 parti) |
| Frasi dei duelli | 4 esatte + 29 parti | 29 + 14 |
| `ui_<l>` | **NO** | **NO** |
| Provato in gioco | no | no |
(Contatori letti dai file il 2026-10-11.)

### 12.2 Cose specifiche
- **Tedesco** (lettera `g`, `basic_gg`):
  - Parole molto lunghe: compressione maggiore, corpo piu' piccolo; attenzione a `Fitter.fit_set` (`sx_min`, `size_min`) e ai riquadri fissi delle linguette. Prima di disegnare **leggi cosa dice l'originale tedesco**: spesso e' gia' abbreviato.
  - `ß`, `Ä Ö Ü` **maiuscoli** (come la É francese: toccano la riga sopra): applica le due soluzioni di `menu_lists` (riduzione fino a -8% + `clip`) o `accent_down` per le tessere di lettere.
  - Virgolette „ “, spazi (`《》s` caso `SPAZIO_DOPO_DE`), "Tauschen" gia' tedesco (nell'italiano originale era rimasto tedesco).
  - Residui di altre lingue nelle tabelle (de `ddstrtbl_g` 66 era francese: gia' corretto).
- **Spagnolo** (lettera `s`, `basic_ss`):
  - `¿ ¡ Ñ Á É Í Ó Ú` (accenti sulle maiuscole): stessa attenzione.
  - Nessun database ufficiale scaricabile per l'audit delle carte: servono controlli di accenti/refusi e lettura; le correzioni (125) sono per lo piu' accenti mancanti (la `ddstrtbl_s` 64 "Magicas" -> "Mágicas" gia' in `ui_texts.json`).
  - Scena `st02_t01/Scr101E` rotta nel gioco (testo italiano in es): tradotta da noi, **rileggere**.
- **Entrambi**: ripetere tutti i controlli di `STATO_LAVORI.md` 2c; verificare in gioco le etichette lunghe elencate nella sez. 8, punto 4; verificare che l'atlante `tiny_<l>` sia quello usato (un solo atlante per installazione: il primo modulo).
- Se un archivio ha lo stesso hash dell'inglese per una texture che in italiano era ridisegnata, **non** serve rifarla (controlla sempre con 7.2.1).

---

## 13. Trappole, errori gia' fatti e come evitarli

1. **Perdere il pack USA / USRDIR**: stanno fuori dal progetto e in `%TEMP%`; i file temporanei vengono ripuliti da altre sessioni (successo a pack, a `vigem/pad.py`, a `pp.ps1`). Tieni le copie degli strumenti nel progetto.
2. **`Family.finish()` sostituisce tutte le righe della famiglia** nel `<l>.ini`: rilancia sempre la famiglia intera.
3. **`python -I` e pacchetti nel user site**: `No module named requests/cv2`. Evita `-I` (o installa nel sito di sistema).
4. **Heredoc/escape**: `\u00cc`, `\\u00a0`, percorsi con backslash. Scrivi file con lo strumento di scrittura; usa `chr()`.
5. **La rilevazione automatica delle righe** (`line_rows`) si rompe con le maiuscole accentate (righe fuse): usa `n=` e il passo fisso (max altezza pulita).
6. **Parola di una lingua diversa nella texture originale** (SCAMBIA, TAUSCHEN): trattala come bug del gioco; usa `orig_text`.
7. **Rilanciare un solo gruppo di `duel_texts`** (`icons`) cancella dal `.ini` le righe degli altri gruppi.
8. **Geometria specifica della lingua**: il dialogo del tutorial francese ha 2 righe e il riquadro piu' basso; i banner del VS sono allargati dal gioco a riempire la texture; la linguetta "JOUEUR" e' piu' stretta. Non dare per scontato che i numeri italiani valgano: **misura sempre sull'originale**.
9. **Tessere spezzate**: parole su 2 texture (TOCCA... SUCCE|SSIVO) -> il taglio va in un varco tra lettere (`seam_shift`); le tessere di lettere (result_letters) una per lettera.
10. **L'accento della maiuscola** in Times/Futura e' piu' alto del gioco: abbassalo (`accent_down`) o riduci il corpo + `clip`.
11. **Test con la ISO sbagliata**: l'originale non ha le correzioni di dialoghi/stringhe/etichetta grande; usa `_definitiva` per quelle.
12. **Salvataggio e lingua**: la lingua e' nel save. Non lasciare il save di prova al posto di quello dell'utente (e viceversa).
13. **Nome del joypad/finestra**: `pw.py`/`pad.py` cercano la finestra il cui titolo inizia con `PPSSPP Gold`; se PPSSPP e' una build diversa cambia il filtro.
14. **Non fidarti del solo MAE** (alfa/colore): le parole nuove danno valori alti. Guarda l'immagine.
15. **Non toccare le texture a pixel** (regola 3) e **non usare Real-ESRGAN** (scartato: texture corrotte, palette cambiate a runtime).
16. **Le 438 texture di mappa/sfondi non sono sostituite** (il gioco ne cambia la palette): non e' un difetto del nuovo lavoro.
17. **PPSSPP ricorda il cursore dei menu**: dopo una sottopagina il cursore non e' dove pensi: fai uno screenshot prima di premere A.

---

## 14. Definizione di "fatto" (checklist finale) e documentazione

Una lingua e' "al livello dell'italiano" quando:
- [ ] modulo carte completo, correzioni applicate e **viste in gioco** su una carta con testo nuovo (album/deck e carta grande nel duello);
- [ ] targa del titolo vista in gioco;
- [ ] `ui_<l>`: tutte le famiglie fatte; ogni riga `ui_<l>` in `<l>.ini` punta a un file esistente; le 8 famiglie confrontate con gli originali a occhio;
- [ ] in gioco visti: titolo, menu principale, deck editor, ricette, negozio, laboratorio, calendario, PDA, VS, duello (HUD, Chaîne-equivalente, attacco diretto, fine duello, sasso-carta-forbici), tutorial;
- [ ] ISO `_definitiva` provata: dialoghi (almeno le scene iniziali e un duello), frasi dei duelli, stringhe UI, etichetta Magia/Trappola della carta grande;
- [ ] etichette lunghe verificate (sez. 8, punto 4);
- [ ] `textures.zip` per Android rigenerato con la lingua scelta (o segnalato come da fare);
- [ ] `STATO_LAVORI.md` (sezione della lingua con data, cosa fatto/non fatto/decisioni), `LEGGIMI.md` (riga nella tabella), `TUTORIAL.md` (se il metodo e' cambiato) aggiornati;
- [ ] memoria dell'agente aggiornata (progetto-ui-francese e analoga).

Come documentare: aggiungi in `STATO_LAVORI.md` una sezione "Interfaccia HD in <lingua>" con (1) data, (2) elenco texture per famiglia con i testi scelti, (3) problemi trovati e come risolti, (4) cosa e' stato visto in gioco e cosa no, (5) decisioni aperte per l'utente. Mantieni questo stile: preciso e con i nomi dei file/script.

---

## 15. Appendice

### 15.1 File e script principali (percorsi relativi a `tools/`)
| File | A cosa serve |
|---|---|
| `lingue.py` | dati per lingua letti dal gioco; `TF1_LANG` |
| `ehp.py`, `gim.py` | lettura archivi e texture, hash |
| `alt_font.py`, `font_alternativi/` | font liberi al posto di quelli Apple |
| `generate_language.py`, `attributi.py`, `tiny_atlas.py`, `tiny_fragment.py`, `extract_labels.py` | modulo carte di una lingua |
| `compose_pack.py`, `module_ini.py` | composizione del pack e degli ini |
| `ui_it/*.py` | interfaccia HD (it e, con `TF1_LANG`, fr) |
| `ui_it/common.py` | `Family`, `texture`, `reference`, `check` |
| `ui_it/mystic_tomato_title.py` | targa del titolo |
| `ui_it/pixel_hd.py`, `numeri_hd.py`, `vettoriale.py` | fix approvati sulle sprite a pixel grossi |
| `correzioni/rules_<l>.py`, `generate_italian_corrections.py`, `applica.py`, `apply_to_iso.py`, `dialoghi.py`, `duel_lines.py`, `build_dialogues.py`, `single_language_iso.py` | testi della ISO |
| `dati/*.json` | tabelle di correzioni, `ui_texts.json`, `tiny_atlas.json`, etichette |
| `audit/*.py` | audit di carte, dialoghi, frasi, etichette lunghe |
| `analisi/*.py` | ispezione: `textures_per_language`, `dump3/4`, `compare_tiles`, `extract_usrdir`, `mega_dl`, `find_pixelated`, `validate_pack` |
| `upscaling_extra/pad.py`, `rec.py`, `pw.py`, `dlg.py` | test in gioco |
| `rebuild.sh` | ricostruzione completa del pack italiano |

### 15.2 Testi francesi usati (riferimento per tradurre in de/es)
- **duel_texts**: Chaîne · TOUR (blu/rosso) · TOUR DU JOUEUR SUIVANT · DÉMARRER DUEL · Attaque Directe!
- **result_letters**: TU AS GAGNÉ · TU AS PERDU · EGALITE
- **menu_lists**: MENU PRINCIPAL / SAISIR NOM / LISTE CARTES TÉLÉCHARGÉE / PUZZLE DUEL / OPTIONS / SÉLECTION DE LA LANGUE · LISTE DE GROUPE / FAIRE UN NOUVEAU GROUPE / LISTE D'ENTRÉE / DUEL / ÉCHANGE / ENVOYER UNE RECETTE / ENVOYER UNE CARTE / ENVOYER UN PUZZLE DUEL / DUEL LIBRE / DUEL NORMAL / TAG DUEL · RÉSULTAT DU DUEL / BONUS DUEL / BONUS NOUVEAU MEILLEUR SCORE / BONUS DÉFI COMPLÉTÉ / RÉSULTAT INTERMÉDIAIRE / RÉSULTAT FINAL · APPUYEZ SUR LA TOUCHE START · GAGNÉ / ÉGALITÉ / PERDU · Dimanche Lundi Mardi Mercredi Jeudi Vendredi Samedi · Mai Juillet Juin Août · jours / avant le tournoi · Matin / Soir
- **icon_sheets**: ÉPUISÉ · hetés (frammento di "Cartes achetées")
- **deck_screens**: Coffre · Location · Labo · Convertisseur · Types de cartes acquis · Cartes achetées · Types de cartes ac(quis) · ENTRÉE
- **recipe_screens**: Personnage · Utilisateur · Téléchargée · Limitée · Semi-limitée · Interdite · Échange
- **vs_screen**: DUEL / NORMAL / TAG · DEUXIÈME À JOUER / PREMIER À JOUER · 1er round / 2e round / 3e round · Mode Un Duel / Mode Match · GAGNÉ / PERDU / EGALITE · 1er JOUEUR / 2e JOUEUR · JOUEUR
- **tutorial**: Ton adversaire a déclaré le duel. / Activer l'effet de la carte ? · OUI / NON · carte: Pendentif Noir, Bouclier du Lustre Jaune, ... da `cardinfo_fra.ehp`

### 15.3 Quando lo script non basta
Se una texture ha un layout inedito (cosi' e' stato per il tutorial francese e la linguetta JOUEUR): disegna a partire dall'originale, **misura** le geometrie (bounding box dei colori, estensioni del testo), parametrizza e **verifica con un contact sheet** originale/HD. Non accontentarti di "e' vicino": le texture vengono ritagliate a rettangoli fissi dal gioco.

## Appendice: trappole emerse dall'audit carte francese
- `generate_language.py` conserva le righe `ui_<l>/` di `<l>.ini` (corretto il 2026-10-11; prima le perdeva).
- `python -I` disattiva i pacchetti utente (cv2, numpy): per gli script con cv2 non usarlo.
- Non "correggere" termini ufficiali: in francese "Carte Équipement" e "Deck Fusion" sono corretti.
- `PER_CARTA` si applica prima dei `GLOBALI`: il vecchio testo va cercato nel testo originale.
- **Mojibake nei ritocchi**: dopo ogni modifica a `dialogue_touchups_<l>.json` / `rules_<l>.py` controlla che non ci siano sequenze come `Ã©`, `Ã `, `â€™` (grep `Ã` nei file): una regola con il "vecchio" sporco non si applica mai e una con il "nuovo" sporco scrive caratteri sbagliati nel gioco. Riparo: `s.encode('cp1252').decode('utf-8')` sulle sequenze. Scrivi i file con Write/Edit, non con heredoc dentro `python -c`.

## Appendice: stringhe dell'interfaccia (strTbl, aiuti, schede dei duellisti)
Oltre a carte, dialoghi e frasi dei duelli, la ISO ha **tabelle di stringhe** con formato `(n, 12, 12+4n)` + offset + UTF-16 in membri dei `.ehp` (stesso formato di `chr_wordstbl`; `duel_lines.tabella/scrivi_tabella` leggono e scrivono, round-trip identico). Per una lingua vanno **lette per intero**:
| Archivio (sotto `PSP_GAME/USRDIR`) | Membro (fr) | Contenuto |
|---|---|---|
| `database/charalist.ehp` | `strTbl_<l>.bin` | schede (biografie) dei duellisti |
| `database/duelrecord.ehp`, `duel/result/result_<l>.ehp` | `strTbl_<l>.bin` / `strTbl.bin` | record e obiettivi dei duelli (le due tabelle sono uguali) |
| `database/{cardalbum,limitlist,tutoriallist}.ehp`, `duel/start/start_<l>.ehp`, `shop/all_<l>.ehp`, `labo/{conv_machine,password}.ehp` | `strTbl_<l>.bin` | titoli e messaggi |
| `deck/all_<l>.ehp` | `strTbl.bin`, `help_strtbl_contents.bin`, `help_strtbl_label.bin` | editor del deck e relativo aiuto |
| `deck/tutorial.ehp` | `strTbl_<l>.bin` | tutorial dell'editor del deck |
| `duel/basic_b<l>.ehp` | `ddstrtbl_<l>.bin`, `help_strtbl_contents_duel_<l>.bin` | etichette e aiuto del duello (la ISO europea carica `basic_b<l>`) |
| `field/always_*_<f3>.ehp` | `field_strtbl.bin`, `field_strtbl_item.bin`, `field_strtbl_mapname.bin` | menu dell'ufficio, calendario, oggetti e panini, luoghi |
Procedura: (1) estrai le tabelle (esempio nel progetto: `strtbl.py`-style con `ehp.read` + `duel_lines.tabella` su tutti i `.ehp` della USRDIR e raggruppa per archivio/membro; stampa `indice | testo || inglese`); (2) leggi tutto confrontando con l'inglese (mancano frasi, ci sono residui di altre lingue: es. "Cornice della Carta" nella tabella francese); (3) scrivi `correzioni/string_rules_<l>.py` (vedi quello francese: `STRINGHE`, `GLOBALI`, `TABELLE`; i vecchi testi devono comparire esattamente, a capo reali `\n`, a volte `\r\n`); (4) `apply_to_iso.py` riscrive gli archivi e stampa gli avvisi. Gli indici sono 0-based della tabella. Il nome del parlante (es. "Doyen Sheppard") sta nell'eseguibile e **non e' modificabile**.

## Seconda lettura dei dialoghi (esempio fr)
1. Esporta le righe uniche in un txt e leggile a blocchi.
2. Per ogni errore aggiungi una coppia `(vecchio, nuovo)` a `parti` in `dialogue_touchups_<l>.json` (controlla che il testo esista).
3. `build_dialogues.py <l>`, poi `apply_to_iso.py ISO_ORIG ISO_OUT <l>`: deve stampare 0 avvisi.
4. La punteggiatura francese `! ? : ;` viene distanziata da `FR_PUNT`, anche dopo `》`.
