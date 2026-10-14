#!/bin/sh
# Regenerates ONLY the images of the cards whose texts have been corrected (data/card_corrections.json): HD small cards
# (cards/small_it, name + description) and HD large cards (cards/large_it, name). The hashes do not change: textures.ini stays the same.
# Fonts: free (OFL), downloaded on first use into tools/alt_fonts (needs curl; python with fonttools); no Apple fonts.
#
# usage: rebuild_corrections.sh USRDIR PACK_US PACK_MOD [PYTHON]
#   USRDIR    PSP_GAME/USRDIR folder extracted from the European ISO (as for rebuild.sh)
#   PACK_US   ULUS10136 folder of the US pack
#   PACK_MOD  the ULES00600 folder already built (contains cards/small, cards/large, cards/small_it, cards/large_it)
set -e
[ "$#" -ge 3 ] && [ "$#" -le 4 ] || { echo "usage: $0 USRDIR PACK_US PACK_MOD [PYTHON]" >&2; exit 2; }
USR=$1; US=$2; OUT=$3; PY=${4:-python3}
T=$(cd "$(dirname "$0")" && pwd)
[ -d "$T/alt_fonts/static" ] || { echo "free fonts: download and static instances"; sh "$T/alt_fonts/download_fonts.sh" && "$PY" "$T/alt_fonts/create_instances.py"; }   # no Apple fonts
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT HUP INT TERM
ITA=$USR/duelsys/cardinfo_ita.ehp; ENG=$USR/duelsys/cardinfo_eng.ehp
IDS=$("$PY" -I -c "import json,sys;print(' '.join(sorted(json.load(open(sys.argv[1], encoding='utf-8')))))" "$T/data/card_corrections.json")
echo "cards to regenerate: $(echo $IDS | wc -w)"
echo "1/3 clean frames of the small cards"
"$PY" -I "$T/smallclean.py" "$T" "$OUT/cards" "$ENG" "$WORK/smallbg"
echo "2/3 small cards (name + description)"
"$PY" -I "$T/small_it.py" "$T" "$OUT" "$ITA" "$US/textures.ini" "$WORK/smallbg" $IDS
echo "3/3 large cards (name)"
TF1_IDS="$IDS" "$PY" -I "$T/gen_large_it.py" "$T" "$OUT" "$ITA"
echo "done: now regenerate textures.zip (see rebuild.sh, step 8)"
