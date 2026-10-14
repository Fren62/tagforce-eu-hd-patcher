"""Builds the module of ONE language (HD small and large cards, attribute symbols, Spell/Trap labels, deck
thumbnails, ini fragment).
usage: generate_language.py LANGUAGE PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]
  LANGUAGE      it|fr|de|es|en
  PACK          starting English HD pack (contains cards/small, cards/large, cards/tinyMikeyMK, cards/frame/...)
  CARDINFO_EHP  cardinfo_<language>.ehp of the game (PSP_GAME/USRDIR/duelsys)
  US_INI        textures.ini of the pack (English names #NNNN and keys of the pages/tables)
  CLEAN_DIR     clean frames (smallclean.py)
  OUT           module folder: OUT/cards/small_<l>, large_<l>, tiny_<l>, frame/icons_attribute_race_<l>.png,
                frame/icons_spell_trap_<l>.png, OUT/<l>.ini
Without ID it regenerates all the cards (with ID: only those, without atlas). No Apple fonts: free fonts (alt_font.py).
Note: the attribute table, the label and the atlas have the same hash in all languages: with several modules installed
the first wins (see module_ini.py)."""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import languages

lang, pack, ehp, us_ini, clean, out = sys.argv[1:7]
ids = sys.argv[7:]
f3 = languages.LANGUAGES[lang][0]
env = dict(os.environ, TF1_LANG=lang, TF1_EHP=ehp, TF1_OUT=out, PYTHONIOENCODING='utf-8')
py = [sys.executable]
run = lambda *a, **k: subprocess.run(py + list(a), check=True, env=dict(env, **k))
os.makedirs(os.path.join(out, 'cards/frame'), exist_ok=True)
frag = os.path.join(out, f'{lang}.ini')
# keeps the ui_<l>/ lines written by the ui_textures/*.py scripts (otherwise the HD interface disappears from the pack)
_ui = [l for l in open(frag, encoding='utf-8') if f'= ui_{lang}/' in l] if os.path.exists(frag) else []
open(frag, 'w', encoding='utf-8', newline='\n').write(''.join(_ui))


def aggiungi(text):
    with open(frag, 'a', encoding='utf-8', newline='\n') as f:
        f.write(text)


def key(name):
    """key (24 digits) that the base ini assigns to cards/frame/<name>.png (even if it already points to a localized version)."""
    for l in open(us_ini, encoding='utf-8', errors='ignore'):
        m = re.match(r'^([0-9a-fA-F]{24})\s*=\s*cards/frame/' + re.escape(name) + r'(_\w+)?\.png\s*$', l.rstrip('\r\n'))
        if m:
            return m.group(1)


print(f'[{lang}] small cards'); run(os.path.join(HERE, 'small_it.py'), HERE, pack, ehp, us_ini, clean, *ids)
print(f'[{lang}] large cards'); run(os.path.join(HERE, 'gen_large_it.py'), HERE, pack, ehp, **({'TF1_IDS': ' '.join(ids)} if ids else {}))
if lang != 'en':
    sheet = os.path.join(out, f'cards/frame/icons_attribute_race_{lang}.png')
    print(f'[{lang}] attribute symbols')
    run(os.path.join(HERE, 'attributes.py'), 'table', lang, pack, sheet, ehp)
    run(os.path.join(HERE, 'attributes.py'), 'cards', sheet, os.path.join(out, f'cards/small_{lang}'), ehp)
    k = key('icons_attribute_race')
    if k:
        aggiungi(f'# attribute symbols with the lettering in {lang}\n{k} = cards/frame/icons_attribute_race_{lang}.png\n')
strip = os.path.join(HERE, 'data', f'label_eu_{f3}_128x32.png')
if os.path.exists(strip):
    print(f'[{lang}] Spell/Trap labels')
    run(os.path.join(HERE, 'label_it.py'), HERE, os.path.join(pack, 'cards/frame/icons_spell_trap.png'), strip,
        os.path.join(out, f'cards/frame/icons_spell_trap_{lang}.png'))
    aggiungi(f'# labels [{languages.label(ehp)}] of the large card ({lang})\n'
             f'0000000000000000{languages.LABEL_HASH[lang]} = cards/frame/icons_spell_trap_{lang}.png\n')
if lang != 'en' and not ids:
    print(f'[{lang}] deck thumbnails')
    run(os.path.join(HERE, 'tiny_atlas.py'), 'generate', lang, pack, out)
    run(os.path.join(HERE, 'tiny_fragment.py'), lang, us_ini, frag)
print(f'[{lang}] done')
