# Yu-Gi-Oh! GX Tag Force 1 — Patcher europeo (HD + testi corretti)

[English](README.md) · [Italiano](README.it.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

Patcher gratuito e open source per **Yu-Gi-Oh! GX Tag Force** (PSP) nella versione europea **ULES00600 v1.01**.
Partendo dalla *tua* ISO, produce una copia nella lingua scelta (**italiano, francese, tedesco, spagnolo, inglese**), con le parti che scegli:

- **texture HD** per PPSSPP: carte grandi e piccole con testo ridisegnato nella lingua, scritte dell'interfaccia, banner del titolo;
- **correzione di dialoghi e testi**: refusi, accenti, spazi e residui di altre lingue in dialoghi, frasi dei duelli e testi dell'interfaccia;
- **correzione delle carte**: nomi e descrizioni delle carte;
- **rimozione delle altre lingue**: ISO più leggera, il gioco resta nella lingua scelta qualunque sia la lingua di sistema del PSP, e il selettore della lingua (schermata al primo avvio e voce del menu principale) sparisce perché sarebbe inutile.

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

Note sulle opzioni:
- Senza *Rimuovi le altre lingue*, il gioco mantiene tutte e cinque le lingue e il suo selettore; solo la lingua della patch riceve correzioni e texture HD.
- *Texture in HD* crea un `textures.zip` a parte in `<cartella dati di PPSSPP>/PSP/TEXTURES/ULES00600/` (lo stesso file vale su Android: copialo nello stesso percorso sul telefono). Se quella cartella contiene già un altro pacchetto di texture, spostalo prima altrove.

## Riga di comando

Scarica `tfpatch.exe` (Windows) o `tfpatch-linux-x86_64` (Linux; prima `chmod +x`). Patch: `patch_it.tfp`, `patch_fr.tfp`, `patch_de.tfp`, `patch_es.tfp`, `patch_en.tfp`.

```
tfpatch iso --iso ULES00600.iso --patch patch_it.tfp --out ULES00600_it.iso
tfpatch textures --lang it --out textures.zip
```

`tfpatch iso` accetta `--no-cards`, `--no-text` e `--keep-languages` (i tre moduli qui sopra, disattivati) e `--dry-run` (stampa il peso finale della ISO in byte). `tfpatch textures` scarica `base.zip` e il modulo della lingua, ne verifica l'SHA-256 e li compone in un unico `textures.zip` (passa una cartella a `--out` per estrarre; con `--source CARTELLA` si usano file già scaricati). Su Linux scrivi `./tfpatch-linux-x86_64`.

## Limiti noti

- Un salvataggio creato in una lingua diversa da quella della patch non viene riallineato.
- Solo l'emulatore PPSSPP (la patch sostituisce un modulo del gioco nella ISO e le texture sono texture di sostituzione di PPSSPP).
- I moduli texture pesano circa 1 GB per lingua più una base da 1,4 GB comune a tutte le lingue (il modulo inglese è piccolo).

## Come funziona

1. `patcher/strumenti/crea_patch_modulare.py` costruisce, per ogni lingua, la ISO con solo le correzioni alle carte, solo quelle ai testi e entrambe, e scrive un `.tfp` modulare (formato 2): uno zip con `patch.json` e differenze bsdiff, ognuna con i moduli che richiede (`cards`, `text`, `strip`).
2. `patcher/tfpatch` (Rust) controlla l'MD5, sceglie le differenze dei moduli attivi e scrive la ISO in forma compatta: stessa intestazione e directory, poi solo i dati ancora usati. Il peso finale si calcola senza scrivere nulla: è così che l'installer lo mostra in tempo reale.
3. Con `strip`, `libtitle.prx` viene modificato (`patcher/strumenti/salta_lingua.py`) per togliere schermata e voce di menu della lingua e fissare la lingua, e i file delle altre lingue puntano ai dati della lingua scelta.
4. `patcher/strumenti/crea_moduli.py` crea `base.zip` e un `<lingua>.zip` per lingua; `patcher/strumenti/manifest.py` completa `manifest.json` (SHA-256, patch, pesi delle ISO).
5. `verifica_modulare.py`, `verifica_iso.py` e `verifica_texture.py` controllano i risultati; `costruisci_modulari.sh LINGUA...` rifà e verifica ogni combinazione.

I testi, le regole editoriali e le correzioni stanno in `strumenti/` (`correzioni/`, `dati/`); `GUIDA_NUOVA_LINGUA.md`, `REGISTRO_SCELTE.md` e `MODIFICHE_<LINGUA>.md` documentano metodo e scelte.

## Compilare

```
cd patcher/tfpatch && cargo build --release
```

Compila sia `tfpatch` (riga di comando) sia `tfpatch-gui`. Su Linux l'interfaccia grafica richiede i soliti pacchetti di sviluppo X11/Wayland/OpenGL.

## Crediti

- **MikeyMK** — *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* (base delle texture HD, versione USA).
- **chrisfand** — carte HD.
- Font liberi (OFL): XCharter, Libre Baskerville, Newsreader, Alegreya e altri, scaricati da `strumenti/font_alternativi/scarica_font.sh`.

Progetto non ufficiale, senza scopo di lucro, non affiliato a Konami. *Yu-Gi-Oh!* è un marchio di Konami.

## Licenza

Il codice è rilasciato con licenza [MIT](LICENSE). La licenza copre solo il codice: i testi del gioco appartengono a Konami e le texture HD si basano sul lavoro di MikeyMK e chrisfand citato nei crediti.
