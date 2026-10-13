#!/bin/sh
# Ricostruisce il texture pack HD italiano (ULES00600) a partire dal pack USA di MikeyMK.
#
# uso: rigenera.sh USRDIR PACK_USA USCITA [PYTHON]
#   USRDIR    cartella PSP_GAME/USRDIR estratta dalla ISO europea, video e audio esclusi:
#             7zz x gioco.iso 'PSP_GAME/USRDIR/*' -x'!PSP_GAME/USRDIR/movie/*' -x'!PSP_GAME/USRDIR/snd/*'
#   PACK_USA  cartella ULUS10136 dello zip "Yu-Gi-Oh! GX Tag Force 1 HD Remastered.zip"
#   USCITA    cartella da creare, es. ~/.config/ppsspp/PSP/TEXTURES/ULES00600
#             (accanto alla cartella viene creato anche textures.zip, il pacchetto singolo per Android)
#   PYTHON    python con numpy pillow xxhash opencv-python-headless fonttools (default: python3)
#   Font: liberi (OFL), scaricati al primo uso in strumenti/font_alternativi (serve curl); nessun font Apple (font_alt.py).
set -e
[ "$#" -ge 3 ] && [ "$#" -le 4 ] || { echo "uso: $0 USRDIR PACK_USA USCITA [PYTHON]" >&2; exit 2; }
USR=$1; US=$2; OUT=$3; PY=${4:-python3}
T=$(cd "$(dirname "$0")" && pwd)
[ -d "$T/font_alternativi/static" ] || { echo "font liberi: download e istanze statiche"; sh "$T/font_alternativi/scarica_font.sh" && "$PY" "$T/font_alternativi/crea_istanze.py"; }   # nessun font Apple
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT HUP INT TERM
CARD=$USR/card; ITA=$USR/duelsys/cardinfo_ita.ehp; ENG=$USR/duelsys/cardinfo_eng.ehp

echo "1/8 copia del pack USA"
mkdir -p "$OUT"
rsync -a --exclude textures.ini --exclude '_PICK YOUR CARD STYLE HERE' --exclude desktop.ini "$US/" "$OUT/"

echo "2/8 carte grandi con il nome italiano (cards/large_it)"
"$PY" -I "$T/gen_large_it.py" "$T" "$OUT" "$ITA"

echo "3/8 cornici pulite delle carte piccole"
"$PY" -I "$T/smallclean.py" "$T" "$OUT/cards" "$ENG" "$WORK/smallbg"

echo "4/8 carte piccole con testi italiani (cards/small_it)"
"$PY" -I "$T/small_it.py" "$T" "$OUT" "$ITA" "$US/textures.ini" "$WORK/smallbg"

echo "5/8 etichette [CARTA MAGIA]/[CARTA TRAPPOLA] in HD"
"$PY" -I "$T/label_it.py" "$T" "$US/cards/frame/icons_spell_trap.png" "$T/dati/label_eu_ita_128x32.png" "$OUT/cards/frame/icons_spell_trap_it.png"

echo "6/8 scritte italiane dell'interfaccia in HD (ui_it)"
rm -rf "$OUT/ui_it"
for f in "$T"/ui_it/*.py; do
  case "$(basename "$f")" in common.py|tabword.py) continue ;; esac     # moduli di supporto, non famiglie
  "$PY" -I "$f" "$USR" "$US" "$OUT" > "$WORK/family.log"
  tail -1 "$WORK/family.log"
done
cat "$OUT"/ui_it/*.ini > "$WORK/ui_it.ini"

echo "6b/8 texture non coperte ingrandite 4x con xBRZ (a risoluzione 4x/Auto il 4xBRZ di PPSSPP e' spento)"
rm -rf "$OUT/upscale_extra"
cp -R "$T/dati/upscale_extra" "$OUT/upscale_extra"

echo "7/8 textures.ini per ULES00600 (tutte le 5 lingue, italiano localizzato)"
"$PY" -I "$T/gen_ini.py" "$T" "$US/textures.ini" "$CARD" "$OUT/textures.ini" i=it "+$T/extra_it.ini" "+$WORK/ui_it.ini" "+$T/dati/upscale_extra.ini"
for v in mikeymk official_english official_japanese; do
  mkdir -p "$OUT/_SCEGLI LO STILE DELLE CARTE/$v"
  "$PY" -I "$T/gen_ini.py" "$T" "$US/_PICK YOUR CARD STYLE HERE/$v/textures.ini" "$CARD" \
    "$OUT/_SCEGLI LO STILE DELLE CARTE/$v/textures.ini" i=it "+$T/extra_it.ini" "+$WORK/ui_it.ini" "+$T/dati/upscale_extra.ini" >/dev/null
done
[ -f "$T/../LEGGIMI_PACK.txt" ] && cp "$T/../LEGGIMI_PACK.txt" "$OUT/LEGGIMI.txt"
rm -rf "$WORK"

echo "8/8 pacchetto singolo textures.zip (per PPSSPP su Android: un solo file da copiare)"
if [ "${TF1_SKIP_ZIP:-0}" = 1 ]; then
  echo "textures.zip rimandato (TF1_SKIP_ZIP=1)"
elif command -v zip >/dev/null 2>&1; then
  ZIP=$(cd "$(dirname "$OUT")" && pwd)/textures.zip
  rm -f "$ZIP"
  (cd "$OUT" && zip -0 -r -q -X "$ZIP" . -x '.DS_Store' -x '*/.DS_Store')   # PNG gia' compressi: senza ricompressione
  echo "creato: $ZIP"
else
  echo "zip non trovato: salto il pacchetto singolo"
fi
echo "fatto: $OUT"
