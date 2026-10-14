# Yu-Gi-Oh! GX Tag Force 1 — Patcher europeo (HD + testi corretti)

[English](README.md) · [Italiano](README.it.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

<p align="center"><img src="patcher/tfpatch/assets/banner_it.png" alt="Versione Pomodoro Mistico" width="670"></p>

Patcher gratuito e open source per **Yu-Gi-Oh! GX Tag Force** (PSP) nella versione europea **ULES00600 v1.01**.
Partendo dalla *tua* ISO, produce una copia nella lingua scelta (**italiano, francese, tedesco, spagnolo, inglese**), con le parti che scegli:

- **texture HD** per PPSSPP: carte grandi e piccole con testo ridisegnato nella lingua, scritte dell'interfaccia, banner del titolo;
- **riadattamento e correzione dei testi**: dove la localizzazione aveva perso o cambiato il significato dell'originale, dialoghi, frasi dei duelli e testi dell'interfaccia sono riadattati e tradotti di nuovo dalla lingua originale (comprese frasi del tutto assenti in certe lingue), oltre a refusi, accenti, spazi e residui di altre lingue;
- **correzione dei testi delle carte**: nomi e descrizioni riadattati dove la traduzione era sbagliata o incompleta, più refusi e accenti;
- **rimozione delle altre lingue**: ISO più leggera, il gioco resta nella lingua scelta qualunque sia la lingua di sistema del PSP, e il selettore della lingua (schermata al primo avvio e voce del menu principale) sparisce perché sarebbe inutile.


Testi modificati dalla patch in ciascuna lingua (contati confrontando la ISO patchata con l'originale; i numeri comprendono ogni modifica, da una lettera sbagliata a una frase tradotta di nuovo da zero):

| Lingua | Carte | Righe di dialogo | Frasi dei duelli (uniche) | Stringhe dell'interfaccia (uniche) |
|---|---:|---:|---:|---:|
| Inglese | 82 | 402 | 11 | 57 |
| Francese | 266 | 467 | 51 | 254 |
| Tedesco | 258 | 1,649 | 40 | 581 |
| Spagnolo | 624 | 601 | 55 | 329 |
| Italiano | 181 | 2,488 | 33 | 298 |


Texture HD per lingua. Per francese, tedesco, spagnolo e italiano **ogni singola carta del gioco (tutte e 2.833) è ridisegnata in HD con il testo nella tua lingua, sia nella versione grande sia in quella piccola**, insieme alle pagine delle miniature del deck, alla tabella degli attributi e all'etichetta Magia/Trappola. Anche le texture dell'interfaccia sono ridisegnate in HD:

| Lingua | Carte grandi | Carte piccole | Pagine miniature del deck | Texture dell'interfaccia e delle scene (totale) | di cui ridisegnate da noi |
|---|---:|---:|---:|---:|---:|
| Inglese | 2.833 | 2.833 | – | 3.110 | 50 |
| Francese | 2.833 | 2.833 | 7 | 3.107 | 93 |
| Tedesco | 2.833 | 2.833 | 7 | 3.110 | 106 |
| Spagnolo | 2.833 | 2.833 | 7 | 3.111 | 95 |
| Italiano | 2.833 | 2.833 | 7 | 3.213 | 113 |

Tutte e cinque le lingue hanno tutte le 2.833 carte in HD, grandi e piccole. Per l'inglese vengono dal pack di MikeyMK e chrisfand, e 87 sono rigenerate da noi perché ne abbiamo corretto il testo. «Texture dell'interfaccia e delle scene» conta ogni altra texture HD usata dalla lingua (menu, negozio, mappa, personaggi...: la base condivisa più il modulo della lingua); «di cui ridisegnate da noi» sono quelle disegnate per quella lingua, che per l'inglese sono le 50 che il pack non copre. Le texture identiche in tutte le lingue arrivano dalla base condivisa.

> **Stato: prima versione.** Le patch sono verificate file per file per ogni combinazione di moduli, e le cinque lingue sono state provate in PPSSPP (avvio, titolo, duelli dimostrativi). Modalità storia, editor del deck e negozio non sono ancora stati giocati a fondo. L'installer grafico è nuovo: provato su Windows; la versione Linux è prodotta da GitHub Actions e non è ancora stata eseguita su un vero desktop Linux.

## Cosa serve

- La tua ISO **ULES00600 v1.01** (europea). MD5 della ISO completa: `719c99478032a4210ae877832061e9fd` ([redump.org](http://redump.org/)). Sono accettate anche le copie senza i 2 KB finali di zeri.
- [PPSSPP](https://www.ppsspp.org/) con **Sostituisci texture** attivo; consigliata la risoluzione di rendering 4x.

Il repository **non contiene** il gioco né dati estratti dal gioco: le patch (`.tfp`) contengono solo differenze binarie rispetto ai file originali.

## Installer grafico (consigliato)

1. Dalla pagina [Releases](../../releases) scarica `tfpatch-gui.exe` (Windows) o `tfpatch-gui-linux-x86_64` (Linux; prima `chmod +x tfpatch-gui-linux-x86_64`).
2. Avvialo. Il programma si apre nella lingua del tuo PC (inglese se non è una delle cinque) e mostra il banner *Pomodoro Mistico* della **lingua della patch**, che di default è la stessa del programma ma si può cambiare separatamente.
3. Il programma cerca da solo la tua ISO e la cartella dati di PPSSPP e mostra solo il risultato; se non ne trova una, ti chiede di sceglierla. Lascia o togli la spunta ai moduli (di default sono tutti attivi). Percorsi, posizione della ISO finale e una nuova ricerca sono in **Opzioni avanzate**. Il **peso finale della ISO e quello del pacchetto texture sono mostrati in tempo reale** e cambiano mentre spunti o togli i moduli.
4. Premi **Installa**. La patch e i moduli texture vengono scaricati dalle Release e verificati (SHA-256); la tua ISO originale non viene mai modificata.

**Avviso di Windows:** il programma non è firmato digitalmente, quindi Windows SmartScreen può mostrare "Windows ha protetto il PC" e qualche antivirus può segnalarlo. Clicca **Ulteriori informazioni → Esegui comunque**. Il codice è pubblico e i file delle Release sono compilati da GitHub Actions partendo da esso.

Note sulle opzioni:
- Senza *Rimuovi le altre lingue*, il gioco mantiene tutte e cinque le lingue e il suo selettore; solo la lingua della patch riceve correzioni e texture HD.
- *Texture in HD* crea un `textures.zip` a parte in `<cartella dati di PPSSPP>/PSP/TEXTURES/ULES00600/` (lo stesso file vale su Android: copialo nello stesso percorso sul telefono). Se quella cartella contiene già un altro pacchetto di texture, spostalo prima altrove.

## Riga di comando

Lo strumento da riga di comando non è allegato alle release (alla maggior parte delle persone basta l'installer grafico): compilalo con `cd patcher/tfpatch && cargo build --release` (il programma è `target/release/tfpatch`). Patch, scaricabili dalla pagina della release: `patch_it.tfp`, `patch_fr.tfp`, `patch_de.tfp`, `patch_es.tfp`, `patch_en.tfp`.

```
tfpatch iso --iso ULES00600.iso --patch patch_it.tfp --out ULES00600_it.iso
tfpatch textures --lang it --out textures.zip
```

`tfpatch iso` accetta `--no-cards`, `--no-text` e `--keep-languages` (i tre moduli qui sopra, disattivati) e `--dry-run` (stampa il peso finale della ISO in byte). `tfpatch textures` scarica `base.zip` e il modulo della lingua, ne verifica l'SHA-256 e li compone in un unico `textures.zip` (passa una cartella a `--out` per estrarre; con `--source CARTELLA` si usano file già scaricati). Su Linux scrivi `./tfpatch`.

## Limiti noti

- Un salvataggio creato in una lingua diversa da quella della patch non viene riallineato.
- Su Linux l'installer grafico richiede `libxkbcommon-x11` (X11) o le librerie Wayland, che la maggior parte dei desktop ha già; altrimenti compila e usa la riga di comando. Le finestre di scelta file usano il portale del desktop: se non si aprono, scrivi i percorsi nelle opzioni avanzate.
- Solo l'emulatore PPSSPP (la patch sostituisce un modulo del gioco nella ISO e le texture sono texture di sostituzione di PPSSPP).
- Il download delle texture è di circa 1,4 GB per lingua: una base da 313 MB comune a tutte le lingue (solo le texture che servono a tutte) più un modulo da circa 1 GB con le carte HD e l'interfaccia di quella lingua.

## Segnalare problemi

Hai trovato un refuso, un testo di carta sbagliato o un bug? [Apri una segnalazione](../../issues/new/choose): ci sono moduli per gli errori di testo e per i problemi del programma, e puoi scrivere in una delle cinque lingue. Non allegare mai la tua ISO né file del gioco.

## Come funziona

1. `patcher/tools/build_modular_patch.py` costruisce, per ogni lingua, la ISO con solo le correzioni alle carte, solo quelle ai testi e entrambe, e scrive un `.tfp` modulare (formato 2): uno zip con `patch.json` e differenze bsdiff, ognuna con i moduli che richiede (`cards`, `text`, `strip`).
2. `patcher/tfpatch` (Rust) controlla l'MD5, sceglie le differenze dei moduli attivi e scrive la ISO in forma compatta: stessa intestazione e directory, poi solo i dati ancora usati. Il peso finale si calcola senza scrivere nulla: è così che l'installer lo mostra in tempo reale.
3. Con `strip`, `libtitle.prx` viene modificato (`patcher/tools/remove_language_selector.py`) per togliere schermata e voce di menu della lingua e fissare la lingua, e i file delle altre lingue puntano ai dati della lingua scelta.
4. `patcher/tools/build_texture_modules.py` crea `base.zip` (solo le texture che servono a tutte le lingue) e un `<lingua>.zip` per lingua (le texture usate da quella lingua); `patcher/tools/build_manifest.py` completa `manifest.json` (SHA-256, patch, pesi delle ISO).
5. `verify_modular_patch.py`, `compare_isos.py` e `verify_texture_pack.py` controllano i risultati; `build_all_patches.sh LINGUA...` rifà e verifica ogni combinazione.

I testi, le regole editoriali e le correzioni stanno in `tools/` (`corrections/`, `data/`); `docs/NEW_LANGUAGE_GUIDE.md`, `docs/EDITORIAL_CHOICES.md` e `docs/CHANGES_<LANG>.md` documentano metodo e scelte.

## Compilare

```
cd patcher/tfpatch && cargo build --release
```

Compila sia `tfpatch` (riga di comando) sia `tfpatch-gui`. Su Linux l'interfaccia grafica richiede i soliti pacchetti di sviluppo X11/Wayland/OpenGL.

## Crediti

- **MikeyMK** — *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* (base delle texture HD, versione USA).
- **chrisfand** — carte HD.
- Font liberi (OFL): XCharter, Libre Baskerville, Newsreader, Alegreya e altri, scaricati da `tools/alt_fonts/download_fonts.sh`.

Progetto non ufficiale, senza scopo di lucro, non affiliato a Konami. *Yu-Gi-Oh!* è un marchio di Konami.

## Licenza

Il codice è rilasciato con licenza [MIT](LICENSE). La licenza copre solo il codice: i testi del gioco appartengono a Konami e le texture HD si basano sul lavoro di MikeyMK e chrisfand citato nei crediti.
