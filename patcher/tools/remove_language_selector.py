"""Removes the language selection screen from the start-up and the "Language settings" entry from the main menu (gmodule/libtitle.prx),
and fixes the language.

The entry point of libtitle (vaddr 0x34) looks at the "boot mode": 0 and 1 open scene 0x28 (language selection), 2 the title.
Here modes 0 and 1 are diverted to a block that calls SetLanguage(n) (the same import 0x24d1c that the language scene uses
at the end of the selection) and then continues from scene 0 (0x1e0), as the language scene did at the end of the selection (skipping
the initial scenes made the first demo duel crash). The block sits in the space of the old branches (now dead); the `jal`
needs a (PRX) relocation entry: the one of the `jal 0x24d1c` of the language scene (0xb028), now useless, is reused.

Game language indexes (screen order: cursor + 1): 1 en, 2 de, 3 fr, 4 it, 5 es.
usage: remove_language_selector.py ISO LANGUAGE        (modifies the ISO in place: same file length)"""
import struct, sys
import pycdlib

LANGUAGES = dict(en=1, de=2, fr=3, it=4, es=5)
PRX = '/PSP_GAME/USRDIR/gmodule/libtitle.prx'
TEXT = 0x60                  # file offset of the code segment (vaddr 0)
REL = 0x2d2b8                # .rel.text section (8-byte offset, info pairs)
REL_JAL_SCENE = 0x30cc8      # relocation entry of the jal 0x24d1c at 0xb028 (offset 0xb028, type 4)


def patch(b: bytearray, language: str) -> bytearray:
    n = LANGUAGES[language]
    w = lambda o: struct.unpack_from('<I', b, o)[0]

    def put(vaddr, old, new):
        assert w(TEXT + vaddr) == old, f'libtitle differs from the expected one at 0x{vaddr:x}: 0x{w(TEXT + vaddr):x}'
        struct.pack_into('<I', b, TEXT + vaddr, new)

    assert struct.unpack_from('<II', b, REL_JAL_SCENE) == (0xb028, 4), 'relocation entry not found'
    assert w(TEXT + 0xb028) == 0x0c009347                  # jal 0x24d1c (SetLanguage)
    put(0x7c, 0x50620007, 0x50620003)                      # mode 1 -> 0x8c (was 0x9c: language scene)
    put(0x84, 0x50600003, 0x50600001)                      # mode 0 -> 0x8c (was 0x94)
    put(0x8c, 0x10000054, 0x0c009347)                      # jal SetLanguage
    put(0x90, 0x00000000, 0x24040000 | n)                  # (delay slot) a0 = language
    put(0x94, 0x10000052, 0x1000004a)                      # b 0x1e0 -> scene 0 (logo, movie, title), as after the original language selection
    put(0x98, 0xa6020008, 0x00000000)                      # nop
    struct.pack_into('<I', b, REL_JAL_SCENE, 0x8c)         # the relocation now applies to the jal at 0x8c
    # Main menu (init at 0x80c): one entry less = no "Language settings" (it is the last of the list; the counter
    # at +8 of the widget goes from 8 to 7 and the cursor wraps accordingly).
    put(0x8e0, 0x2442ffff, 0x2442fffe)                     # addiu v0, v0, -1  ->  -2
    return b


def main(iso_path, language):
    iso = pycdlib.PyCdlib()
    iso.open(iso_path)
    iso.interchange_level = 4
    rec = iso.get_record(iso_path=PRX)
    ext, size = rec.extent_location(), rec.get_data_length()
    iso.close()
    with open(iso_path, 'r+b') as f:
        f.seek(ext * 2048)
        b = bytearray(f.read(size))
        patch(b, language)
        f.seek(ext * 2048)
        f.write(b)
    print(f'libtitle.prx: language selection removed, fixed language {language} ({LANGUAGES[language]})')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
