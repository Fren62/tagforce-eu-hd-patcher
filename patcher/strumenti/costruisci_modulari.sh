#!/bin/bash
# uso: costruisci_modulari.sh LINGUA...   -> patcher/build/mod_tmp/patch2_<l>.tfp, verificata combinazione per combinazione
export PYTHONUTF8=1
ISO="PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso"; T=patcher/build/mod_tmp
for L in "$@"; do
  TFP_KEEP=1 python -X utf8 patcher/strumenti/crea_patch_modulare.py "$ISO" $L $T/patch2_$L.tfp $T 2>&1 | tail -2
  python -X utf8 patcher/strumenti/verifica_modulare.py "$ISO" $L $T/patch2_$L.tfp $T 2>&1 | grep -E "OK|ERRORE|differenze" | sed "s/^/$L: /"
  rm -f $T/${L}_c.iso $T/${L}_t.iso $T/${L}_ct.iso $T/${L}_ref_strip.iso
done
echo FINITO
