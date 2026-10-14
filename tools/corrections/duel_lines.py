"""Corrects the characters' lines during duels (chr_wordstbl_<l>.bin / 02chr_wordstbl_<l>.bin inside duel/*.ehp) with
data/duel_line_corrections_<language>.json:  {"exact": {sentence: new}, "parts": [[old, new], ...]}   (line breaks written as ⏎).
"exact" entries apply only if the sentence is identical; "parts" are text substitutions on every sentence."""
import json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_to_iso as ai
import languages

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


def load(language):
    f = os.path.join(DATA, f'duel_line_corrections_{language}.json')
    if not os.path.exists(f):
        return None
    c = json.load(open(f, encoding='utf-8'))
    nl = lambda s: s.replace('⏎', '\n')
    return {nl(k): nl(v) for k, v in c.get('exact', {}).items()}, [(nl(a), nl(b)) for a, b in c.get('parts', [])]


def read_table(d):
    n, table_off, data_off = struct.unpack_from('<III', d, 0)
    res = []
    for o in struct.unpack_from(f'<{n}I', d, table_off):
        p = data_off + o
        e = p
        while e + 1 < len(d) and d[e:e + 2] != b'\0\0':
            e += 2
        res.append(d[p:e].decode('utf-16-le'))
    return res


def write_table(texts):
    n = len(texts)
    offsets, data = [], b''
    for t in texts:
        offsets.append(len(data))
        data += t.encode('utf-16-le') + b'\0\0'
    if texts and texts[-1] == '':      # the empty last entry points to the end of the data, without its own terminator
        data = data[:-2]
    return struct.pack('<III', n, 12, 12 + 4 * n) + struct.pack(f'<{n}I', *offsets) + data


def remap_pointers(ents, files):
    """The archive's *-ptrs.txt files hold the absolute offsets of the members: if a table grows and the following members
    move, they must be updated (otherwise the game loads wrong data and crashes)."""
    pos = ents[0]['fo']
    new_offsets = {}
    for e in ents:
        pos += -pos % 16
        new_offsets[e['fo']] = pos
        pos += len(files[e['name']])
    for k in files:
        if k.endswith('-ptrs.txt') and len(files[k]) % 4 == 0:
            v = struct.unpack(f'<{len(files[k]) // 4}I', bytes(files[k]))
            files[k][:] = struct.pack(f'<{len(v)}I', *[new_offsets.get(x, x) for x in v])


def patch(iso, chosen_languages, warnings):
    """iso: open PyCdlib. Returns ({ISO path: (original, new)}, rewritten sentences). Every archive is rewritten once only,
    with the corrections of all the chosen languages."""
    import io
    rules = {}
    for l in chosen_languages:
        c = load(l)
        if c:
            rules[l] = (re.compile(rf'(?:02)?chr_wordstbl_{languages.LANGUAGES[l][1]}\.bin$'),) + c
    out, n, used = {}, 0, set()
    for ch in iso.list_children(iso_path='/PSP_GAME/USRDIR/duel'):
        name = ch.file_identifier().decode().split(';')[0]
        if not name.endswith('.ehp') or not rules:
            continue
        p = f'/PSP_GAME/USRDIR/duel/{name}'
        b = io.BytesIO()
        iso.get_file_from_iso_fp(b, iso_path=p)
        d = b.getvalue()
        try:
            ents, files = ai.open_ehp(d)
        except Exception:
            continue
        touched = False
        for l, (pat, exact, parts) in rules.items():
            for m in [k for k in files if pat.match(k)]:
                old_texts = read_table(bytes(files[m]))
                new_texts = []
                for t in old_texts:
                    u = exact.get(t, t)
                    for a, b2 in parts:
                        u = u.replace(a, b2)
                    if u != t:
                        n += 1
                        touched = True
                        used.add((l, t))
                    new_texts.append(u)
                if new_texts != old_texts:
                    files[m] = bytearray(write_table(new_texts))
        if touched:
            remap_pointers(ents, files)
            out[p] = (d, ai.rebuild_ehp(d, ents, files))
    for l, (pat, exact, parts) in rules.items():
        for k in exact:
            if (l, k) not in used:
                warnings.append(f'duel lines {l}: exact sentence never found: {k[:50]!r}')
    return out, n
