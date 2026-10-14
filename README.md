# Yu-Gi-Oh! GX Tag Force 1 — European HD & text-fix patcher

[English](README.md) · [Italiano](README.it.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

A free, open-source patcher for **Yu-Gi-Oh! GX Tag Force** (PSP), European version **ULES00600 v1.01**.
Starting from *your own* ISO it produces a copy in the language you choose (**English, French, German, Spanish, Italian**), with the parts you pick:

- **HD textures** for PPSSPP: large and small cards with the text redrawn in your language, interface texts, title banner;
- **text re-adaptation and correction**: wherever the localisation lost or changed the meaning of the original, dialogues, in-duel lines and interface texts are re-adapted and translated again from the original language (including sentences that were missing altogether in some languages), on top of typos, accents, spacing and leftovers from other languages;
- **card text correction**: names and descriptions re-adapted where the translation was wrong or incomplete, plus typos and accents;
- **removal of the other languages**: smaller ISO, the game stays in the chosen language whatever the PSP system language is, and the language selector (first-boot screen and main-menu entry) is removed since it would be pointless.


Texts changed by the patch in each language (counted by comparing the patched ISO with the original; the numbers include every change, from a single wrong letter to a sentence translated again from scratch):

| Language | Cards | Story dialogue lines | Duel lines (unique) | Interface strings (unique) |
|---|---:|---:|---:|---:|
| English | 82 | 402 | 11 | 57 |
| French | 266 | 467 | 51 | 254 |
| German | 258 | 1,649 | 40 | 581 |
| Spanish | 624 | 601 | 55 | 329 |
| Italian | 181 | 2,488 | 33 | 298 |

> **Status: early release.** The patches are verified file by file for every combination of modules, and the five languages were tested in PPSSPP (boot, title screen, demo duels). Story mode, deck editor and shop have not been played through yet. The graphical installer is new: tested on Windows; the Linux build is produced by GitHub Actions and has not been run on a real Linux desktop yet.

## What you need

- Your own **ULES00600 v1.01** (European) ISO. MD5 of the complete dump: `719c99478032a4210ae877832061e9fd` ([redump.org](http://redump.org/)). Copies missing the final 2 KB of zeros are accepted too.
- [PPSSPP](https://www.ppsspp.org/) with **Replace textures** enabled; rendering resolution 4x is recommended.

This repository **does not contain** the game or any data extracted from it: the patches (`.tfp`) hold only binary differences from the original files.

## Graphical installer (recommended)

1. Download from the [Releases](../../releases) page `tfpatch-gui.exe` (Windows) or `tfpatch-gui-linux-x86_64` (Linux; run `chmod +x tfpatch-gui-linux-x86_64` first).
2. Run it. The program opens in your PC language (English if it is not one of the five) and shows the *Mystic Tomato* banner of the **patch language**, which is the same as the program language by default but can be changed separately.
3. The program looks for your ISO and your PPSSPP data folder by itself and only shows the result; if it cannot find one, it asks you to choose it. Keep or untick the modules (all are on by default). Paths, the output ISO location and a new search are under **Advanced options**. The **final ISO size and the size of the texture pack are shown live** and change as you tick or untick modules.
4. Click **Install**. The patch and the texture modules are downloaded from the Releases and verified (SHA-256); your original ISO is never modified.

**Windows warning:** the program is not code-signed, so Windows SmartScreen may say "Windows protected your PC" and some antivirus programs may flag it. Click **More info → Run anyway**. The code is public and the files in the Releases are built from it by GitHub Actions.

Notes on the options:
- Without *Remove the other languages*, the game keeps all five languages and its own language selector; only the patch language gets the corrections and the HD textures.
- *HD textures* creates a separate `textures.zip` in `<PPSSPP data folder>/PSP/TEXTURES/ULES00600/` (the same file works on Android: copy it to the same path on the phone). If that folder already holds another texture pack, move it away first.

## Command line

The command-line tool is not attached to the releases (the graphical installer is what most people need): build it with `cd patcher/tfpatch && cargo build --release` (the program is `target/release/tfpatch`). Patches, downloadable from the release page: `patch_en.tfp`, `patch_fr.tfp`, `patch_de.tfp`, `patch_es.tfp`, `patch_it.tfp`.

```
tfpatch iso --iso ULES00600.iso --patch patch_en.tfp --out ULES00600_en.iso
tfpatch textures --lang en --out textures.zip
```

`tfpatch iso` accepts `--no-cards`, `--no-text` and `--keep-languages` (the three modules above, off) and `--dry-run` (prints the final ISO size in bytes). `tfpatch textures` downloads `base.zip` and the language module, checks their SHA-256 and merges them into one `textures.zip` (pass a folder to `--out` to extract instead; `--source FOLDER` uses files you already downloaded). On Linux type `./tfpatch-linux-x86_64`.

## Known limits

- A save file created in a different language than the patch is not re-aligned to it.
- On Linux the graphical installer needs `libxkbcommon-x11` (X11) or the Wayland libraries, which most desktops already have; otherwise use the command line. The file dialogs use the desktop portal; if they do not open, type the paths under Advanced options.
- Only the PPSSPP emulator is supported (the patch replaces a game module in the ISO and the textures are PPSSPP replacement textures).
- The texture modules are about 1 GB per language plus a 1.4 GB base shared by all languages (the English module is small).

## Reporting problems

Found a typo, a wrong card text or a bug? [Open an issue](../../issues/new/choose): there are forms for text errors and for program problems, and you can write in any of the five languages. Never attach your ISO or any game files.

## How it works

1. `patcher/tools/build_modular_patch.py` builds, for each language, the ISO with only the card corrections, only the text corrections and both, and writes a modular `.tfp` (format 2): a zip with `patch.json` and bsdiff deltas, each tagged with the modules it needs (`cards`, `text`, `strip`).
2. `patcher/tfpatch` (Rust) checks the MD5, selects the deltas of the active modules and writes the ISO in compact form: same header and directories, then only the data still in use. The final size is computed without writing anything, which is how the installer shows it live.
3. With `strip`, `libtitle.prx` is patched (`patcher/tools/remove_language_selector.py`) to remove the language screen and menu entry and to set the fixed language, and the other languages' files point to the chosen language's data.
4. `patcher/tools/build_texture_modules.py` builds `base.zip` and one `<lang>.zip` per language; `patcher/tools/build_manifest.py` completes `manifest.json` (SHA-256, patches, ISO sizes).
5. `verify_modular_patch.py`, `compare_isos.py` and `verify_texture_pack.py` check the results; `build_all_patches.sh LANG...` rebuilds and verifies every combination.

Texts, editorial rules and corrections live in `tools/` (`corrections/`, `data/`). `docs/NEW_LANGUAGE_GUIDE.md`, `docs/EDITORIAL_CHOICES.md` and `docs/CHANGES_<LANG>.md` document the method and the choices (in Italian).

## Building from source

```
cd patcher/tfpatch && cargo build --release
```

This builds both `tfpatch` (command line) and `tfpatch-gui`. On Linux the GUI needs the usual X11/Wayland/OpenGL development packages.

## Credits

- **MikeyMK** — *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* (base of the HD textures, US version).
- **chrisfand** — HD cards.
- Free fonts (OFL): XCharter, Libre Baskerville, Newsreader, Alegreya and others, downloaded by `tools/alt_fonts/download_fonts.sh`.

Unofficial, non-profit fan project, not affiliated with Konami. *Yu-Gi-Oh!* is a trademark of Konami.

## License

The code is released under the [MIT License](LICENSE). The license covers the code only: the game's texts belong to Konami, and the HD textures are based on the work of MikeyMK and chrisfand credited above.
