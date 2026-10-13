# Yu-Gi-Oh! GX Tag Force 1 — Europäischer HD- und Textkorrektur-Patcher

[English](README.md) · [Italiano](README.it.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

Ein kostenloser Open-Source-Patcher für **Yu-Gi-Oh! GX Tag Force** (PSP), europäische Version **ULES00600 v1.01**.
Aus *Ihrer eigenen* ISO erzeugt er eine Kopie in der gewählten Sprache (**Englisch, Französisch, Deutsch, Spanisch, Italienisch**) mit:

- **korrigierten Texten**: Kartennamen und -beschreibungen, Dialoge, Duellsprüche und Oberflächentexte (Tippfehler, Akzente, Leerzeichen, Reste anderer Sprachen);
- **HD-Texturen** für PPSSPP: große und kleine Karten mit neu gezeichnetem Text in Ihrer Sprache, Oberflächentexte, Titelbanner;
- **keine Sprachauswahl mehr**: Der Sprachbildschirm beim ersten Start und der Menüpunkt zur Sprachwahl im Hauptmenü sind entfernt (die Sprache ist fest), da sie überflüssig wären;
- **nur eine Sprache in der ISO**: Die anderen Sprachen werden entfernt, die ISO ist dadurch kleiner (etwa 610 MB statt 835 MB) und das Spiel bleibt in der gewählten Sprache, egal welche Systemsprache die PSP hat.

> **Status: erste Version (v0.1.0).** Alle fünf ISO-Patches sind Datei für Datei geprüft. Bisher in PPSSPP gespielt: Italienisch und Französisch (Start, Titel, Hauptmenü). Englisch, Deutsch und Spanisch müssen noch gründlich getestet werden. Es gibt noch keine grafische Oberfläche, nur die Kommandozeile.

## Was Sie brauchen

- Ihre eigene **ULES00600 v1.01**-ISO (europäisch). MD5 des vollständigen Dumps: `719c99478032a4210ae877832061e9fd` ([redump.org](http://redump.org/)). Kopien ohne die letzten 2 KB Nullen werden ebenfalls akzeptiert.
- [PPSSPP](https://www.ppsspp.org/) mit aktivierter Option **Texturen ersetzen**; Render-Auflösung 4x empfohlen.

Dieses Repository **enthält weder das Spiel noch daraus extrahierte Daten**: Die Patches (`.tfp`) enthalten nur binäre Unterschiede zu den Originaldateien.

## Verwendung (Kommandozeile)

Laden Sie von der Seite [Releases](../../releases) `tfpatch.exe` (Windows) oder `tfpatch-linux-x86_64` (Linux; zuerst `chmod +x tfpatch-linux-x86_64` ausführen) sowie den Patch für Ihre Sprache herunter (`patch_de.tfp`, `patch_en.tfp`, `patch_fr.tfp`, `patch_es.tfp` oder `patch_it.tfp`).

Die folgenden Befehle verwenden `tfpatch`; unter Linux geben Sie stattdessen `./tfpatch-linux-x86_64` ein.

1. ISO patchen (das Original wird nie verändert):

   ```
   tfpatch iso --iso ULES00600.iso --patch patch_de.tfp --out ULES00600_de.iso
   ```

2. HD-Texturpaket erstellen. Das Programm lädt `base.zip` und das Modul Ihrer Sprache von den Releases herunter, prüft deren SHA-256 und fügt sie zu einer einzigen `textures.zip` zusammen:

   ```
   tfpatch textures --lang de --out textures.zip
   ```

3. Kopieren Sie `textures.zip` nach `<PPSSPP-Datenordner>/PSP/TEXTURES/ULES00600/textures.zip` (gleicher Pfad unter Android; nicht entpacken). Um in einen Ordner zu entpacken, geben Sie bei `--out` einen Ordner an. Mit `--source ORDNER` werden bereits heruntergeladene Dateien verwendet.

4. In PPSSPP: Einstellungen → Grafik → **Texturen ersetzen** aktivieren und dann `ULES00600_de.iso` starten.

Sprachcodes für `--lang` und für die Patches: `de`, `en`, `fr`, `es`, `it`.

## Bekannte Einschränkungen

- Ein Spielstand, der in einer anderen Sprache als der des Patches erstellt wurde, wird nicht angepasst.
- Unterstützt wird nur der Emulator PPSSPP (der Patch ersetzt ein Spielmodul in der ISO, und die Texturen sind PPSSPP-Ersatztexturen).
- Die Texturmodule sind etwa 1 GB pro Sprache groß (`base.zip` 1,4 GB, für alle Sprachen gemeinsam; das englische Modul ist klein).

## So funktioniert es

1. `patcher/strumenti/crea_patch.py` vergleicht die Original-ISO mit der fertigen ISO einer Sprache und schreibt ein `.tfp`-Paket (ein Zip mit `patch.json` und bsdiff-Deltas).
2. `patcher/tfpatch` (Rust) prüft die MD5, wendet die Deltas an und schreibt die ISO kompakt neu: gleicher Header und gleiche Verzeichnisse, danach nur die noch benutzten Daten (die anderen Sprachen bleiben draußen).
3. `patcher/strumenti/salta_lingua.py` ändert `libtitle.prx`, um den Sprachbildschirm und den Menüpunkt zu entfernen und die Sprache festzulegen.
4. `patcher/strumenti/crea_moduli.py` erstellt `base.zip`, je Sprache eine `<Sprache>.zip` und `manifest.json` (SHA-256).
5. `patcher/strumenti/verifica_iso.py` und `verifica_texture.py` prüfen die Ergebnisse; `costruisci_patch.sh SPRACHE...` baut und prüft die gesamte Kette neu.

Texte, redaktionelle Regeln und Korrekturen liegen in `strumenti/` (`correzioni/`, `dati/`). `GUIDA_NUOVA_LINGUA.md`, `REGISTRO_SCELTE.md` und `MODIFICHE_<SPRACHE>.md` dokumentieren Methode und Entscheidungen (auf Italienisch).

## Aus dem Quellcode bauen

```
cd patcher/tfpatch && cargo build --release
```

## Danksagungen

- **MikeyMK** — *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* (Grundlage der HD-Texturen, US-Version).
- **chrisfand** — HD-Karten.
- Freie Schriften (OFL): XCharter, Libre Baskerville, Newsreader, Alegreya und weitere, heruntergeladen mit `strumenti/font_alternativi/scarica_font.sh`.

Inoffizielles, nicht kommerzielles Fanprojekt, nicht mit Konami verbunden. *Yu-Gi-Oh!* ist eine Marke von Konami.

## Lizenz

Der Code steht unter der [MIT-Lizenz](LICENSE). Die Lizenz deckt nur den Code ab: Die Spieltexte gehören Konami, und die HD-Texturen beruhen auf der oben genannten Arbeit von MikeyMK und chrisfand.
