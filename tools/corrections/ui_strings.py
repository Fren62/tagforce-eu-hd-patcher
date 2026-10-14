"""Corrects the interface strings (strTbl*, help_strtbl_*, ddstrtbl_*, field_strtbl* tables inside the ISO's .ehp files) even
when the new text is longer than the original: the whole table is rewritten and the archive ends up at the end of the ISO
(as for the dialogues and the in-duel lines).
Per-language rules: corrections/string_rules_<language>.py with
  STRINGS   [(archive, member, index, [(old, new), ...], reason)]   archive = path under /PSP_GAME/USRDIR (wildcards * ? allowed)
  GLOBALS   [(regex, replacement, reason)]                           applied to all the strings of the TABLES
  TABLES    [(archive, member)]                                      tables the GLOBALS apply to
The archives rewritten here do NOT receive the in-place writes of ui_texts.json: the ui_texts.json entries that concern them and
the [SPELL CARD]/[TRAP CARD] label of basic_<region><language>.ehp are applied in here."""
import fnmatch, importlib.util, io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apply_to_iso as ai
import duel_lines as dl
import languages

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = '/PSP_GAME/USRDIR/'


def load_rules(language):
    f = os.path.join(HERE, f'string_rules_{language}.py')
    if not os.path.exists(f):
        return None
    spec = importlib.util.spec_from_file_location(f'string_rules_{language}', f)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def all_paths(iso):
    res = []

    def walk(p):
        for ch in iso.list_children(iso_path=p):
            n = ch.file_identifier().decode()
            if n in ('.', '..'):
                continue
            full = p.rstrip('/') + '/' + n
            walk(full) if ch.is_dir() else res.append(full.split(';')[0])
    walk('/')
    return res


def spell_trap_label(iso, path, chosen_languages):
    """new card_spell_trap.gim for a basic_<region><language>.ehp (the same as field/always_<language>_<language>.ehp), or None"""
    m = re.search(r'/duel/basic_[bifgsu]([a-z])\.ehp$', path)
    if not m:
        return None
    for code, (f3, letter, _) in languages.LANGUAGES.items():
        if letter != m.group(1) or code == 'en' or (chosen_languages and code not in chosen_languages):
            continue
        try:
            bb = io.BytesIO()
            iso.get_file_from_iso_fp(bb, iso_path=f'{ROOT}field/always_{f3}_{f3}.ehp')
            return bytes(ai.open_ehp(bb.getvalue())[1]['card_spell_trap.gim'])
        except Exception:
            return None
    return None


def patch(iso, chosen_languages, warnings, ui_rules=()):
    """iso: open PyCdlib. Returns ({ISO path: (original, new)}, rewritten strings)."""
    paths = all_paths(iso)
    per_file = {}      # path -> {'str': [(member, index, parts, reason, language)], 'glob': {member: [(regex, replacement)]}, 'ui': [...]}
    for l in chosen_languages:
        R = load_rules(l)
        if not R:
            continue
        for arc, mem, idx, parts, reason in R.STRINGS:
            found = fnmatch.filter(paths, ROOT + arc)
            if not found:
                warnings.append(f'strings {l}: archive not found {arc}')
            for p in found:
                per_file.setdefault(p, {'str': [], 'glob': {}, 'ui': []})['str'].append((mem, idx, parts, reason, l))
        for arc, mem in R.TABLES:
            for p in fnmatch.filter(paths, ROOT + arc):
                d = per_file.setdefault(p, {'str': [], 'glob': {}, 'ui': []})
                d['glob'].setdefault(mem, []).extend((re.compile(rx), rep) for rx, rep, _ in R.GLOBALS)
    out, n = {}, 0
    for p, rec in sorted(per_file.items()):
        for r in ui_rules:
            if fnmatch.fnmatch(p, r['file']):
                rec['ui'].append(r)
        b = io.BytesIO()
        iso.get_file_from_iso_fp(b, iso_path=p)
        d = b.getvalue()
        ents, files = ai.open_ehp(d)
        tables = {}

        def table(mem):
            if mem not in tables:
                tables[mem] = dl.read_table(bytes(files[mem])) if mem in files else None
            return tables[mem]
        modified = set()
        for mem, idx, parts, reason, l in rec['str']:
            t = table(mem)
            if t is None or idx >= len(t):
                warnings.append(f'strings {l}: {p} {mem} #{idx}: entry not found')
                continue
            s = t[idx]
            for old, new in parts:
                if old not in s:
                    warnings.append(f'strings {l}: {p} {mem} #{idx}: text not found {old[:40]!r}')
                    continue
                s = s.replace(old, new)
            if s != t[idx]:
                t[idx] = s
                modified.add(mem)
                n += 1
        for mem, subs in rec['glob'].items():
            t = table(mem)
            if t is None:
                warnings.append(f'strings: {p} has no {mem}')
                continue
            for i, s in enumerate(t):
                u = s
                for rx, rep in subs:
                    u = rx.sub(rep, u)
                if u != s:
                    t[i] = u
                    modified.add(mem)
                    n += 1
        for r in rec['ui']:                    # ui_texts.json entries that the rest of the program would write in place
            t = table(r['member'])
            if t is not None and r['index'] < len(t) and t[r['index']] == r['old']:
                t[r['index']] = r['new']
                modified.add(r['member'])
        for mem in modified:
            files[mem] = bytearray(dl.write_table(tables[mem]))
        g = spell_trap_label(iso, p, chosen_languages)
        if g is not None and 'card_spell_trap.gim' in files and len(files['card_spell_trap.gim']) == len(g) and bytes(files['card_spell_trap.gim']) != g:
            files['card_spell_trap.gim'] = bytearray(g)
            modified.add('card_spell_trap.gim')
        if modified:
            dl.remap_pointers(ents, files)
            out[p] = (d, ai.rebuild_ehp(d, ents, files))
    return out, n
