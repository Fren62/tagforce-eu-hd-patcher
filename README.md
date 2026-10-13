# Yu-Gi-Oh! GX Tag Force 1 — European HD & text-fix patcher

*[Leggi in italiano](README.it.md)*

A free, open-source patcher for **Yu-Gi-Oh! GX Tag Force** (PSP), European version **ULES00600 v1.01**.
Starting from *your own* ISO it produces a copy in the language you choose (**English, French, German, Spanish, Italian**) with:

- **corrected texts**: card names and descriptions, dialogues, in-duel lines and interface strings (typos, accents, spacing, leftovers from other languages);
- **HD textures** for PPSSPP: large and small cards with the text redrawn in your language, interface texts, title banner;
- **no language selector**: the language screen at first boot and the "Language Settings" entry of the main menu are removed (the language is fixed), since they would be pointless;
- **a single language in the ISO**: the other languages are dropped, so the ISO is smaller (about 610 MB instead of 835 MB) and the game stays in the chosen language whatever the PSP system language is.

> **Status: early release (v0.1.0).** All five ISO patches are verified file by file. Played in PPSSPP so far: Italian and French (boot, title, main menu). English, German and Spanish still need a full playthrough check. There is no GUI yet, only a command-line tool.

## What you need

- Your own **ULES00600 v1.01** (European) ISO. MD5 of the complete dump: `719c99478032a4210ae877832061e9fd` ([redump.org](http://redump.org/)). Copies missing the final 2 KB of zeros are accepted too.
- [PPSSPP](https://www.ppsspp.org/) with **Replace textures** enabled; rendering resolution 4x is recommended.

This repository **does not contain** the game or any data extracted from it: the patches (`.tfp`) hold only binary differences from the original files.

## How to use (Windows, command line)

Download from the [Releases](../../releases) page: `tfpatch.exe` and the patch for your language (`patch_en.tfp`, `patch_fr.tfp`, `patch_de.tfp`, `patch_es.tfp` or `patch_it.tfp`).

1. Patch the ISO (your original is never modified):

   ```
   tfpatch iso --iso ULES00600.iso --patch patch_en.tfp --out ULES00600_en.iso
   ```

2. Build the HD texture pack. This downloads `base.zip` and your language module from the Releases, checks their SHA-256 and merges them into a single `textures.zip`:

   ```
   tfpatch textures --lang en --out textures.zip
   ```

3. Copy `textures.zip` to `<PPSSPP data folder>/PSP/TEXTURES/ULES00600/textures.zip` (the same path works on Android; do not unzip it). To extract into a folder instead, pass a folder to `--out`. Use `--source FOLDER` to read files you already downloaded.

4. In PPSSPP: Settings → Graphics → enable **Replace textures**, then play `ULES00600_en.iso`.

`--lang` / patch codes: `en`, `fr`, `de`, `es`, `it`.

## Known limits

- A save file created in a different language than the patch is not re-aligned to it.
- Only the PPSSPP emulator is supported (the patch replaces a game module in the ISO and the textures are PPSSPP replacement textures).
- Texture modules are about 1 GB per language (`base.zip` 1.4 GB, shared by all languages; the English module is small).

## How it works

1. `patcher/strumenti/crea_patch.py` compares the original ISO with the final ISO of a language and writes a `.tfp` package (a zip with `patch.json` and bsdiff deltas).
2. `patcher/tfpatch` (Rust) checks the MD5, applies the deltas and rewrites the ISO in compact form: same header and directories, then only the data still in use (the other languages are left out).
3. `patcher/strumenti/salta_lingua.py` patches `libtitle.prx` to remove the language screen and menu entry and to set the fixed language.
4. `patcher/strumenti/crea_moduli.py` builds `base.zip`, one `<lang>.zip` per language and `manifest.json` (SHA-256).
5. `patcher/strumenti/verifica_iso.py` and `verifica_texture.py` check the results; `costruisci_patch.sh LANG...` rebuilds and verifies the whole chain.

Texts, editorial rules and corrections live in `strumenti/` (`correzioni/`, `dati/`). `GUIDA_NUOVA_LINGUA.md`, `REGISTRO_SCELTE.md` and `MODIFICHE_<LANGUAGE>.md` document the method and the choices (in Italian).

## Building from source

```
cd patcher/tfpatch && cargo build --release
```

## Credits

- **MikeyMK** — *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* (base of the HD textures, US version).
- **chrisfand** — HD cards.
- Free fonts (OFL): XCharter, Libre Baskerville, Newsreader, Alegreya and others, downloaded by `strumenti/font_alternativi/scarica_font.sh`.

Unofficial, non-profit fan project, not affiliated with Konami. *Yu-Gi-Oh!* is a trademark of Konami.

## License

The code is released under the [MIT License](LICENSE). The license covers the code only: the game's texts belong to Konami, and the HD textures are based on the work of MikeyMK and chrisfand credited above.
