#!/bin/bash
# uso: costruisci_patch.sh LINGUA...   (dalla radice del progetto) -> patcher/build/patch_<l>.tfp, verificata con tfpatch + verifica_iso.py
export PYTHONUTF8=1
ORIG="PSP/GAME/ULES00600_YuGiOh_GX_TagForce_EUR.iso"; B=patcher/build
for L in "$@"; do
  python -X utf8 strumenti/correzioni/applica_iso.py "$ORIG" $B/${L}_testi.iso $L > $B/${L}_testi.log 2>&1 || { echo "$L: applica_iso FALLITO"; continue; }
  grep -ci "avviso" $B/${L}_testi.log | sed "s/^/$L: avvisi: /"
  python -X utf8 strumenti/correzioni/una_lingua_iso.py $B/${L}_testi.iso $B/${L}_final.iso $L > $B/${L}_una.log 2>&1 || { echo "$L: una_lingua FALLITO"; continue; }
  python -X utf8 patcher/strumenti/salta_lingua.py $B/${L}_final.iso $L || { echo "$L: salta_lingua FALLITO"; continue; }
  python -X utf8 patcher/strumenti/crea_patch.py "$ORIG" $B/${L}_final.iso $L $B/patch_$L.tfp
  patcher/tfpatch/target/release/tfpatch.exe iso --iso "$ORIG" --patch $B/patch_$L.tfp --out $B/${L}_rust.iso 2>&1 | tail -1
  python -X utf8 patcher/strumenti/verifica_iso.py $B/${L}_final.iso $B/${L}_rust.iso && echo "$L: OK"
  rm -f $B/${L}_testi.iso $B/${L}_final.iso $B/${L}_rust.iso
done
echo FINITO
