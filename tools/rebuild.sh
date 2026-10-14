#!/bin/sh
# Rebuilds the Italian HD texture pack (ULES00600) starting from MikeyMK's US pack.
#
# usage: rebuild.sh USRDIR PACK_US OUT [PYTHON]
#   USRDIR    PSP_GAME/USRDIR folder extracted from the European ISO, video and audio excluded:
#             7zz x game.iso 'PSP_GAME/USRDIR/*' -x'!PSP_GAME/USRDIR/movie/*' -x'!PSP_GAME/USRDIR/snd/*'
#   PACK_US   ULUS10136 folder of the "Yu-Gi-Oh! GX Tag Force 1 HD Remastered.zip" archive
#   OUT       folder to create, e.g. ~/.config/ppsspp/PSP/TEXTURES/ULES00600
#             (textures.zip, the single package for Android, is also created next to the folder)
#   PYTHON    python with numpy pillow xxhash opencv-python-headless fonttools (default: python3)
#   Fonts: free (OFL), downloaded on first use into tools/alt_fonts (needs curl); no Apple fonts (alt_font.py).
set -e
[ "$#" -ge 3 ] && [ "$#" -le 4 ] || { echo "usage: $0 USRDIR PACK_US OUT [PYTHON]" >&2; exit 2; }
USR=$1; US=$2; OUT=$3; PY=${4:-python3}
T=$(cd "$(dirname "$0")" && pwd)
[ -d "$T/alt_fonts/static" ] || { echo "free fonts: download and static instances"; sh "$T/alt_fonts/download_fonts.sh" && "$PY" "$T/alt_fonts/create_instances.py"; }   # no Apple fonts
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT HUP INT TERM
CARD=$USR/card; ITA=$USR/duelsys/cardinfo_ita.ehp; ENG=$USR/duelsys/cardinfo_eng.ehp

echo "1/8 copy of the US pack"
mkdir -p "$OUT"
rsync -a --exclude textures.ini --exclude '_PICK YOUR CARD STYLE HERE' --exclude desktop.ini "$US/" "$OUT/"

echo "2/8 large cards with the Italian name (cards/large_it)"
"$PY" -I "$T/gen_large_it.py" "$T" "$OUT" "$ITA"

echo "3/8 clean frames of the small cards"
"$PY" -I "$T/smallclean.py" "$T" "$OUT/cards" "$ENG" "$WORK/smallbg"

echo "4/8 small cards with Italian texts (cards/small_it)"
"$PY" -I "$T/small_it.py" "$T" "$OUT" "$ITA" "$US/textures.ini" "$WORK/smallbg"

echo "5/8 [CARTA MAGIA]/[CARTA TRAPPOLA] labels in HD"
"$PY" -I "$T/label_it.py" "$T" "$US/cards/frame/icons_spell_trap.png" "$T/data/label_eu_ita_128x32.png" "$OUT/cards/frame/icons_spell_trap_it.png"

echo "6/8 Italian interface lettering in HD (ui_it)"
rm -rf "$OUT/ui_it"
for f in "$T"/ui_textures/*.py; do
  case "$(basename "$f")" in common.py|tabword.py) continue ;; esac     # support modules, not families
  "$PY" -I "$f" "$USR" "$US" "$OUT" > "$WORK/family.log"
  tail -1 "$WORK/family.log"
done
cat "$OUT"/ui_it/*.ini > "$WORK/ui_it.ini"

echo "6b/8 uncovered textures enlarged 4x with xBRZ (at 4x/Auto resolution PPSSPP's 4xBRZ is off)"
rm -rf "$OUT/upscale_extra"
cp -R "$T/data/upscale_extra" "$OUT/upscale_extra"

echo "7/8 textures.ini for ULES00600 (all 5 languages, Italian localized)"
"$PY" -I "$T/gen_ini.py" "$T" "$US/textures.ini" "$CARD" "$OUT/textures.ini" i=it "+$T/extra_it.ini" "+$WORK/ui_it.ini" "+$T/data/upscale_extra.ini"
for v in mikeymk official_english official_japanese; do
  mkdir -p "$OUT/_CHOOSE YOUR CARD STYLE/$v"
  "$PY" -I "$T/gen_ini.py" "$T" "$US/_PICK YOUR CARD STYLE HERE/$v/textures.ini" "$CARD" \
    "$OUT/_CHOOSE YOUR CARD STYLE/$v/textures.ini" i=it "+$T/extra_it.ini" "+$WORK/ui_it.ini" "+$T/data/upscale_extra.ini" >/dev/null
done
[ -f "$T/../LEGGIMI_PACK.txt" ] && cp "$T/../LEGGIMI_PACK.txt" "$OUT/LEGGIMI.txt"
rm -rf "$WORK"

echo "8/8 single textures.zip package (for PPSSPP on Android: one file to copy)"
if [ "${TF1_SKIP_ZIP:-0}" = 1 ]; then
  echo "textures.zip postponed (TF1_SKIP_ZIP=1)"
elif command -v zip >/dev/null 2>&1; then
  ZIP=$(cd "$(dirname "$OUT")" && pwd)/textures.zip
  rm -f "$ZIP"
  (cd "$OUT" && zip -0 -r -q -X "$ZIP" . -x '.DS_Store' -x '*/.DS_Store')   # PNGs already compressed: no recompression
  echo "created: $ZIP"
else
  echo "zip not found: skipping the single package"
fi
echo "done: $OUT"
