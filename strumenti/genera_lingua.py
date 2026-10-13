"""Costruisce il modulo di UNA lingua (carte piccole e grandi HD, simboli degli attributi, etichette Magia/Trappola, miniature
del deck, frammento di ini).
usage: genera_lingua.py LINGUA PACK CARDINFO_EHP US_INI CLEAN_DIR OUT [ID ...]
  LINGUA        it|fr|de|es|en
  PACK          pack HD inglese di partenza (contiene cards/small, cards/large, cards/tinyMikeyMK, cards/frame/...)
  CARDINFO_EHP  cardinfo_<lingua>.ehp del gioco (PSP_GAME/USRDIR/duelsys)
  US_INI        textures.ini del pack (nomi inglesi #NNNN e chiavi delle pagine/tabelle)
  CLEAN_DIR     cornici pulite (smallclean.py)
  OUT           cartella del modulo: OUT/cards/small_<l>, large_<l>, tiny_<l>, frame/icons_attribute_race_<l>.png,
                frame/icons_spell_trap_<l>.png, OUT/<l>.ini
Senza ID rigenera tutte le carte (con ID: solo quelle, senza atlante). Nessun font Apple: font liberi (font_alt.py).
Nota: la tabella degli attributi, l'etichetta e l'atlante hanno lo stesso hash in tutte le lingue: con piu' moduli installati
vince il primo (vedi modulo_ini.py)."""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lingue

lang, pack, ehp, us_ini, clean, out = sys.argv[1:7]
ids = sys.argv[7:]
f3 = lingue.LINGUE[lang][0]
env = dict(os.environ, TF1_LANG=lang, TF1_EHP=ehp, TF1_OUT=out, PYTHONIOENCODING='utf-8')
py = [sys.executable]
run = lambda *a, **k: subprocess.run(py + list(a), check=True, env=dict(env, **k))
os.makedirs(os.path.join(out, 'cards/frame'), exist_ok=True)
frag = os.path.join(out, f'{lang}.ini')
# conserva le righe ui_<l>/ scritte dagli script ui_it/*.py (altrimenti l'interfaccia HD sparisce dal pack)
_ui = [l for l in open(frag, encoding='utf-8') if f'= ui_{lang}/' in l] if os.path.exists(frag) else []
open(frag, 'w', encoding='utf-8', newline='\n').write(''.join(_ui))


def aggiungi(testo):
    with open(frag, 'a', encoding='utf-8', newline='\n') as f:
        f.write(testo)


def chiave(nome):
    """chiave (24 cifre) che l'ini di base assegna a cards/frame/<nome>.png (anche se punta gia' a una versione localizzata)."""
    for l in open(us_ini, encoding='utf-8', errors='ignore'):
        m = re.match(r'^([0-9a-fA-F]{24})\s*=\s*cards/frame/' + re.escape(nome) + r'(_\w+)?\.png\s*$', l.rstrip('\r\n'))
        if m:
            return m.group(1)


print(f'[{lang}] carte piccole'); run(os.path.join(HERE, 'small_it.py'), HERE, pack, ehp, us_ini, clean, *ids)
print(f'[{lang}] carte grandi'); run(os.path.join(HERE, 'gen_large_it.py'), HERE, pack, ehp, **({'TF1_IDS': ' '.join(ids)} if ids else {}))
if lang != 'en':
    sheet = os.path.join(out, f'cards/frame/icons_attribute_race_{lang}.png')
    print(f'[{lang}] simboli degli attributi')
    run(os.path.join(HERE, 'attributi.py'), 'tabella', lang, pack, sheet, ehp)
    run(os.path.join(HERE, 'attributi.py'), 'carte', sheet, os.path.join(out, f'cards/small_{lang}'), ehp)
    k = chiave('icons_attribute_race')
    if k:
        aggiungi(f'# simboli degli attributi con la scritta in {lang}\n{k} = cards/frame/icons_attribute_race_{lang}.png\n')
strip = os.path.join(HERE, 'dati', f'label_eu_{f3}_128x32.png')
if os.path.exists(strip):
    print(f'[{lang}] etichette Magia/Trappola')
    run(os.path.join(HERE, 'label_it.py'), HERE, os.path.join(pack, 'cards/frame/icons_spell_trap.png'), strip,
        os.path.join(out, f'cards/frame/icons_spell_trap_{lang}.png'))
    aggiungi(f'# etichette [{lingue.etichetta(ehp)}] della carta grande ({lang})\n'
             f'0000000000000000{lingue.ETICHETTA_HASH[lang]} = cards/frame/icons_spell_trap_{lang}.png\n')
if lang != 'en' and not ids:
    print(f'[{lang}] miniature del deck')
    run(os.path.join(HERE, 'atlante_tiny.py'), 'genera', lang, pack, out)
    run(os.path.join(HERE, 'frammento_tiny.py'), lang, us_ini, frag)
print(f'[{lang}] fatto')
