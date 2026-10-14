#!/bin/bash
# usage: build_all_patches.sh LANGUAGE...   -> patcher/build/mod_tmp/patch2_<l>.tfp, verified combination by combination
export PYTHONUTF8=1
ISO="PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso"; T=patcher/build/mod_tmp
for L in "$@"; do
  TFP_KEEP=1 python -X utf8 patcher/tools/build_modular_patch.py "$ISO" $L $T/patch2_$L.tfp $T 2>&1 | tail -2
  python -X utf8 patcher/tools/verify_modular_patch.py "$ISO" $L $T/patch2_$L.tfp $T 2>&1 | grep -E "OK|ERROR|differences" | sed "s/^/$L: /"
  rm -f $T/${L}_c.iso $T/${L}_t.iso $T/${L}_ct.iso $T/${L}_ref_strip.iso
done
echo DONE
