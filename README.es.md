# Yu-Gi-Oh! GX Tag Force 1 — Parcheador europeo (HD + textos corregidos)

[English](README.md) · [Italiano](README.it.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

Un parcheador gratuito y de código abierto para **Yu-Gi-Oh! GX Tag Force** (PSP), versión europea **ULES00600 v1.01**.
A partir de *tu propia* ISO, genera una copia en el idioma elegido (**inglés, francés, alemán, español, italiano**) con:

- **textos corregidos**: nombres y descripciones de las cartas, diálogos, frases de los duelos y cadenas de la interfaz (erratas, acentos, espacios, restos de otros idiomas);
- **texturas HD** para PPSSPP: cartas grandes y pequeñas con el texto redibujado en tu idioma, textos de la interfaz, banner del título;
- **sin selector de idioma**: la pantalla de elección del primer arranque y la entrada de selección de idioma del menú principal se eliminan (el idioma es fijo), porque serían inútiles;
- **un solo idioma en la ISO**: se quitan los demás idiomas, así la ISO pesa menos (unos 610 MB en lugar de 835 MB) y el juego se queda en el idioma elegido sea cual sea el idioma del sistema de la PSP.

> **Estado: primera versión (v0.1.0).** Los cinco parches de ISO están verificados archivo por archivo. Probado hasta ahora en PPSSPP: italiano y francés (arranque, título, menú principal). El inglés, el alemán y el español aún deben probarse a fondo. Todavía no hay interfaz gráfica, solo línea de comandos.

## Qué necesitas

- Tu propia ISO **ULES00600 v1.01** (europea). MD5 del volcado completo: `719c99478032a4210ae877832061e9fd` ([redump.org](http://redump.org/)). También se aceptan copias sin los últimos 2 KB de ceros.
- [PPSSPP](https://www.ppsspp.org/) con **Reemplazar texturas** activado; se recomienda resolución de renderizado 4x.

Este repositorio **no contiene** el juego ni datos extraídos de él: los parches (`.tfp`) solo contienen diferencias binarias respecto a los archivos originales.

## Cómo se usa (línea de comandos)

Descarga desde la página de [Releases](../../releases) `tfpatch.exe` (Windows) o `tfpatch-linux-x86_64` (Linux; antes ejecuta `chmod +x tfpatch-linux-x86_64`) y el parche de tu idioma (`patch_es.tfp`, `patch_en.tfp`, `patch_fr.tfp`, `patch_de.tfp` o `patch_it.tfp`).

Los comandos de abajo usan `tfpatch`; en Linux escribe `./tfpatch-linux-x86_64`.

1. Aplica el parche a la ISO (la original nunca se modifica):

   ```
   tfpatch iso --iso ULES00600.iso --patch patch_es.tfp --out ULES00600_es.iso
   ```

2. Crea el pack de texturas HD. Descarga `base.zip` y el módulo de tu idioma desde las Releases, comprueba su SHA-256 y los une en un único `textures.zip`:

   ```
   tfpatch textures --lang es --out textures.zip
   ```

3. Copia `textures.zip` en `<carpeta de datos de PPSSPP>/PSP/TEXTURES/ULES00600/textures.zip` (la misma ruta sirve en Android; no lo descomprimas). Para extraer en una carpeta, pasa una carpeta a `--out`. Con `--source CARPETA` se usan archivos ya descargados.

4. En PPSSPP: Ajustes → Gráficos → activa **Reemplazar texturas** y luego inicia `ULES00600_es.iso`.

Códigos de idioma para `--lang` y para los parches: `es`, `en`, `fr`, `de`, `it`.

## Límites conocidos

- Una partida guardada creada en un idioma distinto al del parche no se reajusta.
- Solo se admite el emulador PPSSPP (el parche sustituye un módulo del juego en la ISO y las texturas son texturas de reemplazo de PPSSPP).
- Los módulos de texturas pesan unos 1 GB por idioma (`base.zip` 1,4 GB, común a todos los idiomas; el módulo en inglés es pequeño).

## Cómo funciona

1. `patcher/strumenti/crea_patch.py` compara la ISO original con la ISO final de un idioma y escribe un paquete `.tfp` (un zip con `patch.json` y diferencias bsdiff).
2. `patcher/tfpatch` (Rust) comprueba el MD5, aplica las diferencias y reescribe la ISO de forma compacta: misma cabecera y mismos directorios, y después solo los datos que siguen en uso (los demás idiomas se quedan fuera).
3. `patcher/strumenti/salta_lingua.py` modifica `libtitle.prx` para quitar la pantalla y la entrada de menú del idioma y fijar el idioma.
4. `patcher/strumenti/crea_moduli.py` crea `base.zip`, un `<idioma>.zip` por idioma y `manifest.json` (SHA-256).
5. `patcher/strumenti/verifica_iso.py` y `verifica_texture.py` comprueban los resultados; `costruisci_patch.sh IDIOMA...` rehace y verifica toda la cadena.

Los textos, las reglas editoriales y las correcciones están en `strumenti/` (`correzioni/`, `dati/`). `GUIDA_NUOVA_LINGUA.md`, `REGISTRO_SCELTE.md` y `MODIFICHE_<IDIOMA>.md` documentan el método y las decisiones (en italiano).

## Compilar desde el código fuente

```
cd patcher/tfpatch && cargo build --release
```

## Créditos

- **MikeyMK** — *Yu-Gi-Oh! GX Tag Force 1 HD Remastered* (base de las texturas HD, versión de EE. UU.).
- **chrisfand** — cartas HD.
- Fuentes libres (OFL): XCharter, Libre Baskerville, Newsreader, Alegreya y otras, descargadas con `strumenti/font_alternativi/scarica_font.sh`.

Proyecto de aficionados no oficial y sin ánimo de lucro, no afiliado a Konami. *Yu-Gi-Oh!* es una marca de Konami.

## Licencia

El código se publica bajo la [licencia MIT](LICENSE). La licencia cubre solo el código: los textos del juego pertenecen a Konami, y las texturas HD se basan en el trabajo de MikeyMK y chrisfand citado arriba.
