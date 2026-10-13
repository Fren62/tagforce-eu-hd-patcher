# Piano del patcher (2026-10-13)

Decisioni: **un solo patcher**, moduli per lingua scaricati a richiesta (it, fr, de, es, en), moduli texture **completi con la base inclusa** (permesso degli autori dato per acquisito), scritto in **Go** (Windows + Linux), CLI e poi GUI.

## Principio: il Go applica, il Python prepara

Non si riscrive in Go la logica dei testi (`applica_iso.py`, `dialoghi.py`, `frasi_duello.py`, `stringhe_ui.py`, regole per lingua): e' codice di *costruzione*, serve solo a noi, e funziona gia'.
Il Python (in `strumenti/`) genera per ogni lingua un **pacchetto di patch**; il patcher Go lo applica alla ISO dell'utente.

```
BUILD (nostro PC, Python)                      UTENTE (Go, un solo .exe / binario Linux)
ISO originale --applica_iso/dialoghi/...--> ISO definitiva_<l>
   |  confronto file per file                    ISO v1.01 dell'utente
   v                                               | 1. verifica MD5 (719c9947...)
patch_<l>.tfp  = per ogni file cambiato:           | 2. applica patch_<l>.tfp
   delta (bsdiff+zstd) rispetto all'originale      | 3. tiene una sola lingua (hard link ISO9660)
   (nessun dato del gioco ridistribuito)           v
                                               ULES00600_<l>.iso
texture_<l>.zip = base + moduli/<l> (PNG, textures.ini)  --> PSP/TEXTURES/ULES00600/textures.zip
manifest.json = versioni, URL, SHA-256
```

## Componenti Go
1. **iso**: lettore/scrittore ISO9660 minimale *sul posto* (come gia' fa il Python: i file riscritti vanno in fondo alla ISO, si aggiornano LBA e dimensione nei directory record; le altre lingue diventano hard link = stesso LBA). Niente libreria di scrittura ISO necessaria.
2. **delta**: applicazione bsdiff + zstd; verifica SHA-256 del risultato file per file.
3. **fetch**: scarica da GitHub Releases `manifest.json` e i moduli, con ripresa e verifica SHA-256.
4. **texture**: scrive `textures.zip` (o cartella) in `PSP/TEXTURES/ULES00600/`; opzione cartella dati PPSSPP.
5. **cli/gui**: `tfpatch --iso ... --lang it --out ...`; GUI in seguito (finestra con ISO, lingua, cartella PPSSPP).

## Tappe
1. `tools/crea_patch.py`: ISO definitiva_<l> vs originale -> `patch_<l>.tfp`; **test**: patch applicata con un riferimento Python == ISO definitiva (hash identico).
2. Go: `iso` + `delta`, verificato byte per byte contro l'output Python (prima solo `it`).
3. Go: fetch + texture + CLI. Prova end-to-end in PPSSPP per ogni lingua.
4. GUI, build CI (GitHub Actions), release con asset (< 2 GB ciascuno), README, crediti a MikeyMK e chrisfand.

## Rischi
- ISO: i dati non devono cambiare di LBA per i file non toccati (il gioco non usa LBA fissi, ma verificare con PPSSPP).
- Moduli texture ~1 GB: sotto il limite di 2 GB per asset ma lenti da scaricare; valutare zip store + download con ripresa.
- fr/de/es/en non ancora provate in gioco: la tappa 3 le copre.
