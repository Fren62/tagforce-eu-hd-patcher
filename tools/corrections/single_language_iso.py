"""Keeps a single language in the Tag Force 1 EU (ULES00600) ISO and reduces its size.

The files of the other languages are not deleted (the game opens them by name according to the PSP system language):
their directory entries become ISO9660 hard links to the data of the chosen language, so the game stays in the
chosen language whatever the system language is, and the unchosen data is no longer written into the ISO.

usage: single_language_iso.py ISO_IN ISO_OUT LANGUAGE        (LANGUAGE = it fr de es en)
Requires pycdlib. All the paths are those of the original ISO; names not listed stay unchanged.
"""
import os, re, sys
import pycdlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
import languages

SUFFIX1 = {'it': 'i', 'fr': 'f', 'de': 'g', 'es': 's', 'en': 'e'}   # one-letter suffix (j = Japanese: always goes to the chosen language)
USR = '/PSP_GAME/USRDIR/'


def all_files(iso):
    out = []

    def walk(p):
        for c in iso.list_children(iso_path=p):
            n = c.file_identifier()
            if n in (b'.', b'..'):
                continue
            n = n.decode()
            if c.is_dir():
                walk(p.rstrip('/') + '/' + n)
            else:
                out.append(p.rstrip('/') + '/' + n)
    walk('/')
    return out


def plan(files, language):
    """[(file to replace, file of the chosen language)] for all the files that depend on the language."""
    l1, l3 = SUFFIX1[language], languages.LANGUAGES[language][0]
    file_set = set(files)
    entries = []
    for f in files:
        d, n = f.rsplit('/', 1)
        if n.startswith('opening_'):   # handled below
            continue
        m = re.match(r'^(.*)_([efgsij])\.(\w+)$', n)          # name_<letter>.ext
        if m and m.group(2) != l1:
            entries.append((f, f'{d}/{m.group(1)}_{l1}.{m.group(3)}'))
            continue
        m = re.match(r'^(cardinfo)_(eng|fra|ger|spa|ita)\.(\w+)$', n)   # cardinfo_<language>.ehp
        if m and m.group(2) != l3:
            entries.append((f, f'{d}/{m.group(1)}_{l3}.{m.group(3)}'))
            continue
        m = re.match(r'^always_(bri|fra|ger|ita|spa|usa)_(eng|fra|ger|spa|ita)\.ehp$', n)   # field/always_<country>_<language>.ehp
        country = 'bri' if language == 'en' else l3          # always_eng_eng does not exist: the European version uses the United Kingdom for English
        if m and (m.group(1), m.group(2)) != (country, l3):
            entries.append((f, f'{d}/always_{country}_{l3}.ehp'))
    # opening movie: opening_f.pmf is French only, opening_a.pmf is for all the others
    a, f_ = USR + 'movie/opening_a.pmf', USR + 'movie/opening_f.pmf'
    if a in file_set and f_ in file_set:
        entries.append((a, f_) if language == 'fr' else (f_, a))
    for old, new in entries:
        assert new in file_set, f'missing {new}'
    return entries


def main(src, dst, language):
    iso = pycdlib.PyCdlib()
    iso.open(src)
    iso.interchange_level = 4   # the ISO names are lowercase and without ';1': pycdlib would otherwise refuse the new hard links
    entries = plan(all_files(iso), language)
    for old, new in entries:
        iso.rm_file(iso_path=old)
        iso.add_hard_link(iso_old_path=new, iso_new_path=old)
    iso.write(dst)
    iso.close()
    print(f'{len(entries)} files relinked; {os.path.getsize(src) >> 20} MB -> {os.path.getsize(dst) >> 20} MB')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
