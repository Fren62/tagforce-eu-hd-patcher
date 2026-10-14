"""Corrects the dialogues (script/stNN_*_<letter>.ehp) with data/dialogue_corrections_<language>.json (id 'st01_t01/Scr077E#3' -> current, proposed).
Every scene is a pair of files (gz or not): ...I<letter> (offsets in UTF-16 characters) and ...L<letter> (UTF-16LE strings, each ended by NUL)."""
import gzip, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_to_iso as ai


def data_path(language='it'):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'dialogue_corrections_{language}.json')


TRAILING = ' \n\r\t' + chr(0)       # trailing spaces, line breaks and NULs: they stay as in the game
WIDTH = 46                          # the game does not wrap by itself: in the original text lines reach ~49 characters
LETTER = {'it': 'i', 'fr': 'f', 'de': 'g', 'es': 's', 'en': 'e'}
MAX_LINES = 3                       # lines that fit in the box (original text: 3 lines in 1,108 strings, more in 53)


def line_width(line):
    return len(re.sub('《[^》]*》', 'XXXXXX', line))      # a 《...》 placeholder takes about 6 characters (character name)


def rewrap(text):
    """Wraps by hand only if a line is wider than the box; otherwise keeps the line breaks of the proposal."""
    if all(line_width(r) <= WIDTH for r in text.split('\n')):
        return text
    lines, cur = [], ''
    for w in text.replace('\n', ' ').split():
        if cur and line_width(cur + ' ' + w) > WIDTH:
            lines.append(cur)
            cur = w
        else:
            cur = cur + ' ' + w if cur else w
    return '\n'.join(lines + [cur])


def _member_name(files, scene, kind, letter):
    n = f'{scene}{kind}{letter}.bin'
    return n + '.gz' if n + '.gz' in files else n                                      # some scenes (ImpMapMsg...) are not compressed


def _read(files, n):
    return gzip.decompress(files[n]) if n.endswith('.gz') else bytes(files[n])


def _put(files, n, d):
    files[n] = bytearray(gzip.compress(d, 9, mtime=0) if n.endswith('.gz') else d)


def strings(files, scene, letter):
    i, t = _read(files, _member_name(files, scene, 'I', letter)), _read(files, _member_name(files, scene, 'L', letter))
    o = list(struct.unpack(f'<{len(i) // 4}I', i)) + [len(t) // 2]
    return [t[o[k] * 2:o[k + 1] * 2].decode('utf-16-le') for k in range(len(o) - 1)]


def write(files, scene, letter, texts):
    offsets, pos = [], 0
    for s in texts:
        offsets.append(pos)
        pos += len(s)
    _put(files, _member_name(files, scene, 'I', letter), struct.pack(f'<{len(offsets)}I', *offsets))
    _put(files, _member_name(files, scene, 'L', letter), ''.join(texts).encode('utf-16-le'))


def patch(iso_get, warnings, language='it'):
    """iso_get(path) -> bytes. Returns ({ISO path: (original, new)}, rewritten lines) and fills `warnings`."""
    per_stage = {}
    for id_, c in json.load(open(data_path(language), encoding='utf-8')).items():
        stage, rest = id_.split('/')
        scene, idx = rest.split('#')
        per_stage.setdefault(stage, {}).setdefault(scene, []).append((int(idx), c))
    out, n = {}, 0
    letter = LETTER[language]
    for stage, scenes in per_stage.items():
        p = f'/PSP_GAME/USRDIR/script/{stage}_{letter}.ehp'
        d = iso_get(p)
        ents, files = ai.open_ehp(d)
        _, ja = ai.open_ehp(iso_get(f'/PSP_GAME/USRDIR/script/{stage}_j.ehp'))
        # the audit lists every sentence once: the same sentence (same text and same Japanese) repeated in other
        # scenes or in other branches of the conversation (e.g. Scr077E #3 and #9) gets the same correction
        by_key = {}
        for scene, items in scenes.items():
            tj = strings(ja, scene, 'j')
            tl = strings(files, scene, letter)
            for idx, c in items:
                by_key.setdefault((tl[idx].rstrip(TRAILING), tj[idx].rstrip(TRAILING)), c)
        scene_names = sorted({k.split('I' + letter + '.bin')[0] for k in files if ('I' + letter + '.bin') in k})
        for scene in scene_names:
            try:
                tl, tj = strings(files, scene, letter), strings(ja, scene, 'j')
            except KeyError:
                continue
            if len(tl) != len(tj):
                continue
            already = {i for i, _ in scenes.get(scene, [])}
            for idx, (a, b) in enumerate(zip(tl, tj)):
                c = by_key.get((a.rstrip(TRAILING), b.rstrip(TRAILING)))
                if c and idx not in already:
                    scenes.setdefault(scene, []).append((idx, c))
        for scene, items in scenes.items():
            texts = strings(files, scene, letter)
            for idx, c in items:
                old = texts[idx]
                tail = old[len(old.rstrip(TRAILING)):]
                if old.rstrip(TRAILING) != c['current'].rstrip(TRAILING):
                    warnings.append(f"{stage}/{scene}#{idx}: game text differs from the audit, skipped")
                    continue
                new = rewrap(c['proposed'].rstrip(TRAILING))
                texts[idx] = new + tail
                n += 1
                if new.count('\n') + 1 > MAX_LINES and new.count('\n') > old.count('\n'):
                    warnings.append(f'{stage}/{scene}#{idx}: {new.count(chr(10)) + 1} lines, it may not fit in the box')
            write(files, scene, letter, texts)
        out[p] = (d, ai.rebuild_ehp(d, ents, files))
    return out, n
