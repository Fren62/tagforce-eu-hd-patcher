"""Creates a COPY of the ISO with the corrected texts (card names/descriptions, dialogues, in-duel lines, interface strings), for every
language that has correction tables (card tables: data/card_corrections.json for it, data/card_corrections_<language>.json for fr, de, es, en).
usage: apply_to_iso.py ORIGINAL_ISO CORRECTED_ISO [LANGUAGE ...] [--parts=cards,text]
(the original is never modified; without languages: all of them; without --parts: both)
Rewrites duelsys/cardinfo_<language>.ehp (CARD_Name_X.bin, CARD_Desc_X.bin, CARD_Indx_X.bin) and the other archives that contain texts.
Requires: pip install pycdlib."""
import io, os, struct, sys
import pycdlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import card_corrections
import languages


def cardinfo_path(language):
    return f'/PSP_GAME/USRDIR/duelsys/cardinfo_{languages.LANGUAGES[language][0]}.ehp'


def parse_ehp(d):
    _, total, _, n = struct.unpack_from('<IIII', d, 0)
    entries = []
    for i in range(n):
        name_off, file_off = struct.unpack_from('<II', d, 16 + i * 8)
        e = d.index(b'\0', name_off)
        entries.append(dict(name=d[name_off:e].decode(), no=name_off, szpos=e + 1, fo=file_off, size=struct.unpack_from('<I', d, e + 1)[0]))
    return entries


def open_ehp(d):
    entries = parse_ehp(d)
    return entries, {e['name']: bytearray(d[e['fo']:e['fo'] + e['size']]) for e in entries}


def patch_ehp(d, language='it'):
    entries, files = open_ehp(d)
    table_letter = languages.LANGUAGES[language][2]
    names, descs, index, int_id = (files[f'CARD_Name_{table_letter}.bin'], files[f'CARD_Desc_{table_letter}.bin'],
                                   files[f'CARD_Indx_{table_letter}.bin'], files['CARD_IntID.bin'])
    corrections = card_corrections.table(language)

    def read_text(blob, off):
        end = off
        while blob[end:end + 2] != b'\0\0':
            end += 2
        return blob[off:end].decode('utf-16-le')

    changes = {}                                                  # (field, index) -> new text
    for cid, c in sorted(corrections.items()):
        idx = struct.unpack_from('<H', int_id, (cid - 4000) * 2)[0]
        if not idx:
            continue
        name_off, desc_off = struct.unpack_from('<II', index, idx * 8)
        for field, blob, off in (('name', names, name_off), ('desc', descs, desc_off)):
            if field in c and read_text(blob, off) != c[field]:
                changes[(field, idx)] = c[field]
    changed = len(changes)
    # The game derives the length of every text from the following offsets of the index: the blocks must therefore be rewritten
    # in the same order as the index (4-byte strings, increasing offsets, last entry = end of the block). Appending the new
    # texts at the end broke the order and made the game crash in the Main Deck.
    n = len(index) // 8
    for field, blob, pos in (('name', names, 0), ('desc', descs, 4)):
        offsets = [struct.unpack_from('<II', index, i * 8)[pos // 4] for i in range(n)]
        assert offsets == sorted(offsets), 'original index not sorted'
        new_blob = bytearray(blob[:offsets[0]])
        for i, off in enumerate(offsets):
            if off >= len(blob):                                  # closing entry
                new_off = len(new_blob)
            else:
                end = off
                while blob[end:end + 2] != b'\0\0':
                    end += 2
                text = changes[(field, i)].encode('utf-16-le') if (field, i) in changes else bytes(blob[off:end])
                new_off = len(new_blob)
                new_blob += text + b'\0\0'
                new_blob += b'\0' * (-len(new_blob) % 4)
            struct.pack_into('<I', index, i * 8 + pos, new_off)
        blob[:] = new_blob
        o2 = [struct.unpack_from('<II', index, i * 8)[pos // 4] for i in range(n)]
        assert o2 == sorted(o2) and o2[-1] == len(blob), 'inconsistent index'
    return rebuild_ehp(d, entries, files), changed


def rebuild_ehp(d, entries, files):
    # rebuilds the archive: same table, files aligned to 16 bytes, new sizes
    out = bytearray(d[:entries[0]['fo']])
    for e in entries:
        out += b'\0' * (-len(out) % 16)
        struct.pack_into('<I', out, 16 + entries.index(e) * 8 + 4, len(out))      # file offset
        struct.pack_into('<I', out, e['szpos'], len(files[e['name']]))             # size
        out += files[e['name']]
    out += b'\0' * (-len(out) % 16)
    struct.pack_into('<I', out, 4, len(out))
    return bytes(out)


def ehp_string(blob, index):
    n, table_off, data_off = struct.unpack_from('<III', blob, 0)
    p = data_off + struct.unpack_from('<I', blob, table_off + 4 * index)[0]
    e = p
    while blob[e:e + 2] != b'\0\0':
        e += 2
    return blob[p:e].decode('utf-16-le')


def string_position(d, member, index):
    """(offset of the string in the .ehp file, string) or None if the archive has no such table."""
    entries, files = open_ehp(d)
    e = next((x for x in entries if x['name'] == member), None)
    if e is None:
        return None
    n, table_off, data_off = struct.unpack_from('<III', files[member], 0)
    return e['fo'] + data_off + struct.unpack_from('<I', files[member], table_off + 4 * index)[0], ehp_string(files[member], index)


def patch_table(d, member, index, old, new):
    """Changes one string of a table (n, table offset, data offset, UTF-16 offsets...) inside an .ehp: the new string is
    appended at the end of the data and the offset is updated; the old one stays as dead space."""
    entries, files = open_ehp(d)
    if member not in files:
        return None
    blob = files[member]
    current = ehp_string(blob, index)
    if current != old:
        return None if current == new else False
    n, table_off, data_off = struct.unpack_from('<III', blob, 0)
    if len(blob) % 2:
        blob.append(0)
    struct.pack_into('<I', blob, table_off + 4 * index, len(blob) - data_off)
    blob += new.encode('utf-16-le') + b'\0\0'
    return rebuild_ehp(d, entries, files)


SECT = 2048


def _find_record(f, lba, name):
    """Looks in the directory at `lba` for the record `name` (without ';1', case-insensitive): (record position, lba, length, is directory)"""
    f.seek(lba * SECT)
    dir_len = struct.unpack_from('<I', f.read(SECT), 10)[0]
    f.seek(lba * SECT)
    buf = f.read(dir_len)
    pos = 0
    while pos < len(buf):
        n = buf[pos]
        if n == 0:
            pos = (pos // SECT + 1) * SECT
            continue
        id_len = buf[pos + 32]
        ident = buf[pos + 33:pos + 33 + id_len].decode('latin-1').split(';')[0]
        if ident.lower() == name.lower():
            return lba * SECT + pos, struct.unpack_from('<I', buf, pos + 2)[0], struct.unpack_from('<I', buf, pos + 10)[0], bool(buf[pos + 25] & 2)
        pos += n
    raise FileNotFoundError(name)


def main(src, dst, chosen_languages=None, parts=('cards', 'text')):
    """parts: 'cards' = card names and descriptions (cardinfo) + Spell/Trap label; 'text' = dialogues, in-duel lines,
    interface strings, texts in BOOT.BIN."""
    import fnmatch, json, shutil
    chosen_languages = chosen_languages or [l for l in languages.LANGUAGES if card_corrections.table(l)]
    iso = pycdlib.PyCdlib()
    iso.open(src)
    new_files = {}
    for lang in (chosen_languages if 'cards' in parts else []):
        b = io.BytesIO()
        iso.get_file_from_iso_fp(b, iso_path=cardinfo_path(lang))
        d = b.getvalue()
        new, changed = patch_ehp(d, lang)
        new_files[cardinfo_path(lang)] = (d, new)
        print(f'{os.path.basename(cardinfo_path(lang))}: {len(d)} -> {len(new)} bytes, {changed} strings rewritten')
    import dialogues   # dialogues (script/stNN_*_<l>.ehp), for every language with data/dialogue_corrections_<language>.json

    def get_file(p):
        b = io.BytesIO()
        iso.get_file_from_iso_fp(b, iso_path=p)
        return b.getvalue()

    for lang in (chosen_languages if 'text' in parts else []):
        if not os.path.exists(dialogues.data_path(lang)):
            continue
        warnings = []
        scripts, n = dialogues.patch(get_file, warnings, lang)
        new_files.update(scripts)
        print(f'dialogues {lang}: {n} lines rewritten, {len(warnings)} warnings')
        for w in warnings[:20]:
            print('  ', w)
    import duel_lines   # lines of the characters during duels (duel/*.ehp), for every language with a correction table
    warnings = []
    fd, n = duel_lines.patch(iso, chosen_languages if 'text' in parts else [], warnings)
    new_files.update(fd)
    print(f'duel lines: {n} lines rewritten in {len(fd)} archives, {len(warnings)} warnings')
    for w in warnings[:20]:
        print('  ', w)
    in_place = []   # (ISO path, offset in the archive, old bytes, new bytes) for the interface texts
    ui_texts_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'ui_texts.json')
    if 'text' in parts and os.path.exists(ui_texts_file):
        all_paths = []

        def walk(p):
            for ch in iso.list_children(iso_path=p):
                n = ch.file_identifier().decode()
                if n in ('.', '..'):
                    continue
                full = p.rstrip('/') + '/' + n
                walk(full) if ch.is_dir() else all_paths.append(full.split(';')[0])

        walk('/')
        per_file = {}
        for r in json.load(open(ui_texts_file, encoding='utf-8')):
            for p in fnmatch.filter(all_paths, r['file']):
                per_file.setdefault(p, []).append(r)
        for p, rules in per_file.items():
            d0 = get_file(p)
            for r in rules:
                pos = string_position(d0, r['member'], r['index'])
                if not pos or pos[1] != r['old']:
                    continue
                nb = r['new'].encode('utf-16-le')
                assert len(nb) <= len(r['old'].encode('utf-16-le')), 'the new text must be shorter than or equal to the old one'
                in_place.append((p, pos[0], r['old'].encode('utf-16-le'), nb))
        print(f'interface texts: {len(in_place)} strings to rewrite in place')
    # [SPELL CARD]/[TRAP CARD] label of the large card in the duel: every basic_<region><language>.ehp has the English one
    # (card_spell_trap.gim, hash c2268340) for any language; the European region is 'b' (basic_bi = Italy). The one of the
    # language is put (the same as field/always_<language>_<language>.ehp, same format and size) in all the archives of that language
    for code, (f3, letter, _) in languages.LANGUAGES.items():
        if 'cards' not in parts or chosen_languages and code not in chosen_languages or code == 'en':
            continue
        try:
            pa = f'/PSP_GAME/USRDIR/field/always_{f3}_{f3}.ehp'
            bb = io.BytesIO()
            iso.get_file_from_iso_fp(bb, iso_path=pa)
            fa = open_ehp(bb.getvalue())[1]
        except Exception:
            continue
        new_gim = bytes(fa['card_spell_trap.gim'])
        for region in 'bifgsu':
            pb = f'/PSP_GAME/USRDIR/duel/basic_{region}{letter}.ehp'
            try:
                bb = io.BytesIO()
                iso.get_file_from_iso_fp(bb, iso_path=pb)
                db = bb.getvalue()
            except Exception:
                continue
            eb, fb = open_ehp(db)
            old_gim = bytes(fb['card_spell_trap.gim'])
            if len(old_gim) == len(new_gim) and old_gim != new_gim:
                fo = next(x['fo'] for x in eb if x['name'] == 'card_spell_trap.gim')
                in_place.append((pb, fo, old_gim, new_gim))
    # interface strings (help, character cards, tutorial...) with text longer than the original: they rewrite the archive;
    # the in-place writes concerning the same archives are done there (otherwise they would end up in the old copy)
    import ui_strings
    warnings = []
    ui_rules = json.load(open(ui_texts_file, encoding='utf-8')) if os.path.exists(ui_texts_file) else []
    rewritten, n = ui_strings.patch(iso, chosen_languages if 'text' in parts else [], warnings, ui_rules if 'text' in parts else [])
    assert not set(rewritten) & set(new_files), 'archive rewritten twice'
    new_files.update(rewritten)
    print(f'interface strings: {n} strings rewritten in {len(rewritten)} archives, {len(warnings)} warnings')
    for w in warnings[:30]:
        print('  ', w)
    in_place = [u for u in in_place if u[0] not in rewritten]
    # texts inside the executable (SYSDIR/BOOT.BIN: character names in the dialogue box): data/boot_texts.json,
    # in-place UTF-16 replacement (the new text cannot be longer than the old one: the pointers do not move)
    boot_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'boot_texts.json')
    if 'text' in parts and os.path.exists(boot_file):
        bb = io.BytesIO()
        iso.get_file_from_iso_fp(bb, iso_path='/PSP_GAME/SYSDIR/BOOT.BIN')
        db = bb.getvalue()
        for r in json.load(open(boot_file, encoding='utf-8')):
            if chosen_languages and r['language'] not in chosen_languages:
                continue
            old, new = r['old'].encode('utf-16-le'), r['new'].encode('utf-16-le')
            assert len(new) <= len(old), 'the new text of BOOT.BIN must be shorter than or equal to the old one'
            positions, i = [], db.find(old)
            while i >= 0:
                positions.append(i)
                i = db.find(old, i + 1)
            assert len(positions) == 1, f'BOOT.BIN: {r["old"]!r} found {len(positions)} times'
            in_place.append(('/PSP_GAME/SYSDIR/BOOT.BIN', positions[0], old, new))
    print(f'interface texts + labels: {len(in_place)} in-place writes')
    iso.close()
    shutil.copyfile(src, dst)
    with open(dst, 'r+b') as f:
        f.seek(16 * SECT + 156)
        root = struct.unpack('<I', f.read(34)[2:6])[0]
        jobs = [(p, d, new, p) for p, (d, new) in new_files.items()]
        for ehp_path, d, new, label in jobs:
            lba = root
            for part in ehp_path.strip('/').split('/')[:-1]:
                _, lba, _, is_dir = _find_record(f, lba, part)
                assert is_dir
            rec_pos, old_lba, old_len, _ = _find_record(f, lba, ehp_path.rsplit('/', 1)[1])
            assert old_len == len(d), (old_len, len(d))
            f.seek(0, 2)
            end = f.tell()
            end += -end % SECT
            new_lba = end // SECT
            f.seek(end)
            f.write(new)
            f.write(bytes(-len(new) % SECT))
            total = f.tell() // SECT
            f.seek(rec_pos + 2)
            f.write(struct.pack('<I', new_lba) + struct.pack('>I', new_lba))        # extent (little + big endian)
            f.seek(rec_pos + 10)
            f.write(struct.pack('<I', len(new)) + struct.pack('>I', len(new)))      # length
            f.seek(16 * SECT + 80)
            f.write(struct.pack('<I', total) + struct.pack('>I', total))            # volume size
            print(label, ': new archive at sector', new_lba)
    with open(dst, 'r+b') as f:   # interface texts: written in place, the rest of the file and the ISO do not change size
        for p, rel, old, new in in_place:
            lba = root
            for part in p.strip('/').split('/')[:-1]:
                _, lba, _, is_dir = _find_record(f, lba, part)
            _, file_lba, _, _ = _find_record(f, lba, p.rsplit('/', 1)[1])
            f.seek(file_lba * SECT + rel)
            assert f.read(len(old)) == old, p
            f.seek(file_lba * SECT + rel)
            f.write(new + b'\0' * (len(old) - len(new)))
    print('written', dst, os.path.getsize(dst), 'bytes')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--parts=')]
    parts = next((a[8:].split(',') for a in sys.argv[1:] if a.startswith('--parts=')), ['cards', 'text'])
    main(args[0], args[1], args[2:] or None, tuple(parts))
