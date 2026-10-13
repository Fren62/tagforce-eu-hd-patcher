#!/bin/sh
# Rigenera SOLO le immagini delle carte i cui testi sono stati corretti (dati/correzioni_carte.json): carte piccole HD
# (cards/small_it, nome + descrizione) e carte grandi HD (cards/large_it, nome). Gli hash non cambiano: textures.ini resta uguale.
# Font: liberi (OFL), scaricati al primo uso in strumenti/font_alternativi (serve curl; python con fonttools); nessun font Apple.
#
# uso: rigenera_correzioni.sh USRDIR PACK_USA PACK_MOD [PYTHON]
#   USRDIR    cartella PSP_GAME/USRDIR estratta dalla ISO europea (come per rigenera.sh)
#   PACK_USA  cartella ULUS10136 del pack USA
#   PACK_MOD  la cartella ULES00600 gia' costruita (contiene cards/small, cards/large, cards/small_it, cards/large_it)
set -e
[ "$#" -ge 3 ] && [ "$#" -le 4 ] || { echo "uso: $0 USRDIR PACK_USA PACK_MOD [PYTHON]" >&2; exit 2; }
USR=$1; US=$2; OUT=$3; PY=${4:-python3}
T=$(cd "$(dirname "$0")" && pwd)
[ -d "$T/font_alternativi/static" ] || { echo "font liberi: download e istanze statiche"; sh "$T/font_alternativi/scarica_font.sh" && "$PY" "$T/font_alternativi/crea_istanze.py"; }   # nessun font Apple
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT HUP INT TERM
ITA=$USR/duelsys/cardinfo_ita.ehp; ENG=$USR/duelsys/cardinfo_eng.ehp
IDS=$("$PY" -I -c "import json,sys;print(' '.join(sorted(json.load(open(sys.argv[1], encoding='utf-8')))))" "$T/dati/correzioni_carte.json")
echo "carte da rigenerare: $(echo $IDS | wc -w)"
echo "1/3 cornici pulite delle carte piccole"
"$PY" -I "$T/smallclean.py" "$T" "$OUT/cards" "$ENG" "$WORK/smallbg"
echo "2/3 carte piccole (nome + descrizione)"
"$PY" -I "$T/small_it.py" "$T" "$OUT" "$ITA" "$US/textures.ini" "$WORK/smallbg" $IDS
echo "3/3 carte grandi (nome)"
TF1_IDS="$IDS" "$PY" -I "$T/gen_large_it.py" "$T" "$OUT" "$ITA"
echo "fatto: ora rigenera textures.zip (vedi rigenera.sh, passo 8)"
