# Yu-Gi-Oh! GX Tag Force 1 — Patcher europeo (HD + testi corretti)

Patcher gratuito e open source per **Yu-Gi-Oh! GX Tag Force** (PSP) nella versione europea **ULES00600 v1.01**.
Partendo dalla *tua* ISO, produce una copia con la lingua scelta (**italiano, francese, tedesco, spagnolo, inglese**) con:

- **testi corretti**: nomi e descrizioni delle carte, dialoghi, frasi dei duelli, stringhe dell'interfaccia (refusi, accenti, spazi, residui di altre lingue);
- **texture HD** per PPSSPP: carte grandi e piccole con testo ridisegnato nella lingua, scritte dell'interfaccia, banner del titolo;
- **niente selettore lingua**: la schermata di scelta all'avvio e la voce "Parametri lingua" del menu principale sono rimosse (la lingua è fissa), perché sarebbero inutili;
- una sola lingua nella ISO: le voci delle altre lingue puntano ai dati della lingua scelta, quindi il gioco resta in quella lingua qualunque sia la lingua di sistema del PSP.

> **Stato: lavori in corso.** La patch della ISO funziona per tutte e cinque le lingue (verificata file per file); mancano ancora il download dei moduli texture, l'interfaccia grafica e le prove complete in PPSSPP per fr/de/es/en.

## Cosa serve

- La tua ISO **ULES00600 v1.01** (europea). MD5 della ISO completa: `719c99478032a4210ae877832061e9fd` (redump.org). Sono accettate anche le copie senza i 2 KB finali di zeri.
- [PPSSPP](https://www.ppsspp.org/) con "Sostituisci texture" attivo.

Il repository **non contiene** il gioco né dati estratti dal gioco: le patch (`.tfp`) contengono solo differenze binarie rispetto ai file originali.

## Uso (riga di comando)

```
tfpatch --iso ULES00600.iso --patch patch_it.tfp --out ULES00600_it.iso
```

Texture HD (scarica `base.zip` + il modulo della lingua, ne verifica l'SHA-256 e compone `textures.zip`):

```
tfpatch textures --lang it --out PSP/TEXTURES/ULES00600/textures.zip
```

Le patch (`patch_it.tfp`, …) e i moduli texture (`base.zip`, `<lingua>.zip`, `manifest.json`) sono allegati delle [Release](../../releases). Con `--source CARTELLA` si usano file già scaricati.

## Come funziona

1. `patcher/strumenti/crea_patch.py` confronta la ISO originale con la ISO finale di una lingua e scrive un pacchetto `.tfp` (zip con `patch.json` e differenze bsdiff).
2. `patcher/tfpatch` (Rust) controlla l'MD5, copia la ISO, applica le differenze riscrivendo la ISO in forma compatta: stessa intestazione e directory, poi solo i dati ancora usati (le altre lingue restano fuori, circa 610 MB invece di 835).
3. `patcher/strumenti/verifica_iso.py` confronta due ISO file per file; `costruisci_patch.sh LINGUA...` rifà l'intera catena e verifica.

I testi e le regole editoriali stanno in `strumenti/` (`correzioni/`, `dati/`); `GUIDA_NUOVA_LINGUA.md`, `REGISTRO_SCELTE.md` e `MODIFICHE_<LINGUA>.md` documentano metodo e scelte.

## Compilare

```
cd patcher/tfpatch && cargo build --release
```

## Crediti

- **MikeyMK** — *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* (base delle texture HD, versione USA).
- **chrisfand** — carte HD.
- Font liberi (OFL): XCharter, Libre Baskerville, Newsreader, Alegreya e altri in `strumenti/font_alternativi`.

Progetto non ufficiale, senza scopo di lucro, non affiliato a Konami. *Yu-Gi-Oh!* è un marchio di Konami.

## Licenza

Il codice è rilasciato con licenza [MIT](LICENSE). La licenza copre solo il codice: i testi del gioco appartengono a Konami e le texture HD si basano sul lavoro di MikeyMK e chrisfand citato nei crediti; i moduli texture vengono pubblicati solo con il consenso degli autori.
