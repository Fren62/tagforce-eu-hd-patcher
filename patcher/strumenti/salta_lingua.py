"""Toglie la schermata di scelta lingua dall'avvio e la voce "Parametri lingua" dal menu principale (gmodule/libtitle.prx),
imposta la lingua fissa.

Il punto d'ingresso di libtitle (vaddr 0x34) guarda il "modo di avvio": 0 e 1 aprono la scena 0x28 (scelta lingua), 2 il titolo.
Qui i modi 0 e 1 vengono deviati su un blocco che chiama SetLanguage(n) (stesso import 0x24d1c che la scena lingua usa
a fine scelta) e poi continua dalla scena 0 (0x1e0), come faceva la scena lingua a fine scelta (scavalcare le scene iniziali
faceva crashare il primo duello dimostrativo). Il blocco sta nello spazio dei vecchi rami (ora morti); il `jal`
ha bisogno di una voce di rilocazione (PRX): si riusa quella del `jal 0x24d1c` della scena lingua (0xb028), ora inutile.

Indici lingua del gioco (ordine della schermata: cursore + 1): 1 en, 2 de, 3 fr, 4 it, 5 es.
uso: salta_lingua.py ISO LINGUA        (modifica la ISO sul posto: stessa lunghezza del file)"""
import struct, sys
import pycdlib

LINGUE = dict(en=1, de=2, fr=3, it=4, es=5)
PRX = '/PSP_GAME/USRDIR/gmodule/libtitle.prx'
TEXT = 0x60                  # offset file del segmento di codice (vaddr 0)
REL = 0x2d2b8                # sezione .rel.text (coppie offset, info da 8 byte)
REL_JAL_SCENA = 0x30cc8      # voce di rilocazione del jal 0x24d1c a 0xb028 (offset 0xb028, tipo 4)


def patch(b: bytearray, lingua: str) -> bytearray:
    n = LINGUE[lingua]
    w = lambda o: struct.unpack_from('<I', b, o)[0]

    def metti(vaddr, vecchio, nuovo):
        assert w(TEXT + vaddr) == vecchio, f'libtitle diverso da quello atteso a 0x{vaddr:x}: 0x{w(TEXT + vaddr):x}'
        struct.pack_into('<I', b, TEXT + vaddr, nuovo)

    assert struct.unpack_from('<II', b, REL_JAL_SCENA) == (0xb028, 4), 'voce di rilocazione non trovata'
    assert w(TEXT + 0xb028) == 0x0c009347                  # jal 0x24d1c (SetLanguage)
    metti(0x7c, 0x50620007, 0x50620003)                    # modo 1 -> 0x8c (era 0x9c: scena lingua)
    metti(0x84, 0x50600003, 0x50600001)                    # modo 0 -> 0x8c (era 0x94)
    metti(0x8c, 0x10000054, 0x0c009347)                    # jal SetLanguage
    metti(0x90, 0x00000000, 0x24040000 | n)                # (delay slot) a0 = lingua
    metti(0x94, 0x10000052, 0x1000004a)                    # b 0x1e0 -> scena 0 (logo, filmato, titolo), come dopo la scelta lingua originale
    metti(0x98, 0xa6020008, 0x00000000)                    # nop
    struct.pack_into('<I', b, REL_JAL_SCENA, 0x8c)         # la rilocazione ora vale per il jal a 0x8c
    # Menu principale (init a 0x80c): una voce in meno = niente "Parametri lingua" (e' l'ultima della lista; il contatore
    # a +8 del widget passa da 8 a 7 e il cursore gira di conseguenza).
    metti(0x8e0, 0x2442ffff, 0x2442fffe)                   # addiu v0, v0, -1  ->  -2
    return b


def main(iso_path, lingua):
    iso = pycdlib.PyCdlib(); iso.open(iso_path); iso.interchange_level = 4
    rec = iso.get_record(iso_path=PRX)
    ext, size = rec.extent_location(), rec.get_data_length(); iso.close()
    with open(iso_path, 'r+b') as f:
        f.seek(ext * 2048); b = bytearray(f.read(size))
        patch(b, lingua)
        f.seek(ext * 2048); f.write(b)
    print(f'libtitle.prx: scelta lingua rimossa, lingua fissa {lingua} ({LINGUE[lingua]})')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
