# Yu-Gi-Oh! GX Tag Force 1 — Patcher europeo (HD + testi corretti)

*[Read in English](README.md)*

Patcher gratuito e open source per **Yu-Gi-Oh! GX Tag Force** (PSP) nella versione europea **ULES00600 v1.01**.
Partendo dalla *tua* ISO, produce una copia con la lingua scelta (**italiano, francese, tedesco, spagnolo, inglese**) con:

- **testi corretti**: nomi e descrizioni delle carte, dialoghi, frasi dei duelli, stringhe dell'interfaccia (refusi, accenti, spazi, residui di altre lingue);
- **texture HD** per PPSSPP: carte grandi e piccole con testo ridisegnato nella lingua, scritte dell'interfaccia, banner del titolo;
- **niente selettore lingua**: la schermata di scelta all'avvio e la voce "Parametri lingua" del menu principale sono rimosse (la lingua è fissa), perché sarebbero inutili;
- **una sola lingua nella ISO**: le altre lingue vengono tolte, quindi la ISO pesa meno (circa 610 MB invece di 835) e il gioco resta nella lingua scelta qualunque sia la lingua di sistema del PSP.

> **Stato: prima versione (v0.1.0).** Le cinque patch della ISO sono verificate file per file. Giocate in PPSSPP finora: italiano e francese (avvio, titolo, menu principale). Inglese, tedesco e spagnolo vanno ancora provati a fondo. Non c'è ancora una interfaccia grafica, solo la riga di comando.

## Cosa serve

- La tua ISO **ULES00600 v1.01** (europea). MD5 della ISO completa: `719c99478032a4210ae877832061e9fd` ([redump.org](http://redump.org/)). Sono accettate anche le copie senza i 2 KB finali di zeri.
- [PPSSPP](https://www.ppsspp.org/) con **Sostituisci texture** attivo; consigliata la risoluzione di rendering 4x.

Il repository **non contiene** il gioco né dati estratti dal gioco: le patch (`.tfp`) contengono solo differenze binarie rispetto ai file originali.

## Come si usa (Windows, riga di comando)

Dalla pagina [Releases](../../releases) scarica `tfpatch.exe` e la patch della tua lingua (`patch_it.tfp`, `patch_fr.tfp`, `patch_de.tfp`, `patch_es.tfp` o `patch_en.tfp`).

1. Applica la patch alla ISO (l'originale non viene modificato):

   ```
   tfpatch iso --iso ULES00600.iso --patch patch_it.tfp --out ULES00600_it.iso
   ```

2. Crea il pacchetto texture HD. Scarica `base.zip` e il modulo della tua lingua dalle Release, ne verifica l'SHA-256 e li compone in un unico `textures.zip`:

   ```
   tfpatch textures --lang it --out textures.zip
   ```

3. Copia `textures.zip` in `<cartella dati di PPSSPP>/PSP/TEXTURES/ULES00600/textures.zip` (stesso percorso su Android; non estrarlo). Per estrarre in una cartella, passa una cartella a `--out`. Con `--source CARTELLA` si usano file già scaricati.

4. In PPSSPP: Impostazioni → Grafica → attiva **Sostituisci texture**, poi avvia `ULES00600_it.iso`.

Codici lingua per `--lang` e per le patch: `it`, `fr`, `de`, `es`, `en`.

## Limiti noti

- Un salvataggio creato in una lingua diversa da quella della patch non viene riallineato.
- Solo l'emulatore PPSSPP (la patch sostituisce un modulo del gioco nella ISO e le texture sono texture di sostituzione di PPSSPP).
- I moduli texture pesano circa 1 GB per lingua (`base.zip` 1,4 GB, comune a tutte le lingue; il modulo inglese è piccolo).

## Come funziona

1. `patcher/strumenti/crea_patch.py` confronta la ISO originale con la ISO finale di una lingua e scrive un pacchetto `.tfp` (zip con `patch.json` e differenze bsdiff).
2. `patcher/tfpatch` (Rust) controlla l'MD5, applica le differenze e riscrive la ISO in forma compatta: stessa intestazione e directory, poi solo i dati ancora usati (le altre lingue restano fuori).
3. `patcher/strumenti/salta_lingua.py` modifica `libtitle.prx` per togliere schermata e voce di menu della lingua e fissare la lingua.
4. `patcher/strumenti/crea_moduli.py` crea `base.zip`, un `<lingua>.zip` per lingua e `manifest.json` (SHA-256).
5. `patcher/strumenti/verifica_iso.py` e `verifica_texture.py` controllano i risultati; `costruisci_patch.sh LINGUA...` rifà l'intera catena e verifica.

I testi e le regole editoriali stanno in `strumenti/` (`correzioni/`, `dati/`); `GUIDA_NUOVA_LINGUA.md`, `REGISTRO_SCELTE.md` e `MODIFICHE_<LINGUA>.md` documentano metodo e scelte.

## Compilare

```
cd patcher/tfpatch && cargo build --release
```

## Crediti

- **MikeyMK** — *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* (base delle texture HD, versione USA).
- **chrisfand** — carte HD.
- Font liberi (OFL): XCharter, Libre Baskerville, Newsreader, Alegreya e altri, scaricati da `strumenti/font_alternativi/scarica_font.sh`.

Progetto non ufficiale, senza scopo di lucro, non affiliato a Konami. *Yu-Gi-Oh!* è un marchio di Konami.

## Licenza

Il codice è rilasciato con licenza [MIT](LICENSE). La licenza copre solo il codice: i testi del gioco appartengono a Konami e le texture HD si basano sul lavoro di MikeyMK e chrisfand citato nei crediti.
