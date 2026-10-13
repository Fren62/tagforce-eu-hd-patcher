"""Il progetto non usa font Apple: ogni font macOS richiesto da ImageFont.truetype viene sostituito con un font libero
(OFL) di font_alternativi/static (si crea con scarica_font.sh + crea_istanze.py). Basta fare `import font_alt` all'inizio
dello script. Valgono anche i font variabili di Apple (SF Pro, SF Rounded): le istanze statiche del sostituto vengono scelte
in base al peso richiesto con set_variation_by_axes / set_variation_by_name. L'asse "larghezza" di SF non esiste nei sostituti
e viene ignorato. Gli stili misurati per le carte (apply) valgono per i font liberi."""
import os
from PIL import ImageFont

STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'font_alternativi', 'static')

# (file macOS, indice) -> file libero in static/
MAP = {
    # carte HD
    ('Iowan Old Style.ttc', 4): 'XCharter-Bold.otf',             # nomi, etichetta Magia/Trappola
    ('Iowan Old Style.ttc', 0): 'LibreBaskerville-Regular.ttf',  # descrizioni mostri con effetto
    ('Charter.ttc', 5): 'XCharter-Bold.otf',                     # riga del tipo
    ('Charter.ttc', 3): 'XCharter-Bold.otf',                     # nome carte grandi
    ('Charter.ttc', 0): 'XCharter-Roman.otf',
    ('Charter.ttc', 1): 'XCharter-Italic.otf',
    ('PTSerifCaption.ttc', 0): 'PTSerifCaption-Regular.ttf',     # magie, trappole, tutorial (stesso font)
    ('Athelas.ttc', 1): 'Newsreader-Italic-Regular.ttf',         # mostri Normali
    ('Palatino.ttc', 0): 'LibreBaskerville-Regular.ttf',
    ('Palatino.ttc', 1): 'Lora-Italic-Regular.ttf',
    ('Palatino.ttc', 2): 'LibreBaskerville-Bold.ttf',
    ('Baskerville.ttc', 1): 'LibreBaskerville-Bold.ttf',
    ('Copperplate.ttc', 2): 'CharisSIL-Bold.ttf',
    ('LucidaGrande.ttc', 0): 'CharisSIL-Regular.ttf',            # glifi mancanti
    ('Georgia.ttf', 0): 'Gelasio-Regular.ttf',                   # Gelasio e' compatibile con Georgia
    ('Georgia Italic.ttf', 0): 'Gelasio-Italic-Regular.ttf',
    ('Times New Roman Italic.ttf', 0): 'Tinos-Italic.ttf',
    # interfaccia, scritte del duello, schermata VS, tutorial
    ('Times.ttc', 0): 'Tinos-Regular.ttf',
    ('Times.ttc', 1): 'Tinos-Bold.ttf',
    ('Futura.ttc', 2): 'Jost-Bold.ttf',
    ('Futura.ttc', 3): 'BarlowCondensed-Medium.ttf',             # Futura Condensed
    ('Futura.ttc', 4): 'BarlowCondensed-ExtraBold.ttf',
    ('PTSans.ttc', 7): 'PTSans-Bold.ttf',
    ('Helvetica.ttc', 0): 'Arimo-Regular.ttf',
    ('Arial.ttf', 0): 'Arimo-Regular.ttf',
    ('Arial Bold.ttf', 0): 'Arimo-Bold.ttf',
    ('Arial Black.ttf', 0): 'ArchivoBlack-Regular.ttf',
    ('Comic Sans MS Bold.ttf', 0): 'ComicNeue-Bold.ttf',
    ('ChalkboardSE.ttc', 1): 'Kalam-Regular.ttf',
    ('ChalkboardSE.ttc', 2): 'Kalam-Bold.ttf',
    ('ヒラギノ角ゴシック W8.ttc', 0): 'NotoSansJP-ExtraBold.ttf',
    ('ヒラギノ角ゴシック W9.ttc', 0): 'NotoSansJP-Black.ttf',
    ('ヒラギノ丸ゴ ProN W4.ttc', 0): 'MPLUSRounded1c-Medium.ttf',
    ('Sansation_Bold.ttf', 0): 'Nunito-Bold.ttf',
}
# font variabili Apple -> famiglia libera con istanze statiche NAME-<Peso>.ttf
FAMILY = {'SFNS.ttf': 'Inter', 'SFNSRounded.ttf': 'Nunito', 'SFCompactRounded.ttf': 'Nunito'}
WEIGHTS = {'Regular': 400, 'Medium': 500, 'SemiBold': 600, 'Bold': 700, 'ExtraBold': 800, 'Black': 900}
NAMES = {'thin': 400, 'light': 400, 'regular': 400, 'medium': 500, 'semibold': 600, 'bold': 700, 'heavy': 800,
         'extrabold': 800, 'black': 900}

FT = ImageFont.FreeTypeFont
_orig_truetype, _orig_axes, _orig_name, _orig_get = ImageFont.truetype, FT.set_variation_by_axes, FT.set_variation_by_name, FT.get_variation_axes


def _inst(family, weight):
    w = min(WEIGHTS.items(), key=lambda kv: (abs(kv[1] - weight), -kv[1]))[0]   # peso piu' vicino (a parita' il piu' pesante)
    return os.path.join(STATIC, f'{family}-{w}.ttf')


def _reopen(font, weight):
    FT.__init__(font, _inst(font._fa_family, weight), font.size, 0)


def _weight_of_name(name):
    name = name.decode() if isinstance(name, bytes) else name
    return max((v for k, v in NAMES.items() if k in name.lower().replace(' ', '')), default=400)


def _truetype(font=None, size=10, index=0, *a, **k):
    base = os.path.basename(str(font))
    if base in FAMILY:
        f = _orig_truetype(_inst(FAMILY[base], 400), size, 0, *a, **k)
        f._fa_family = FAMILY[base]
        return f
    if (base, index) in MAP:
        return _orig_truetype(os.path.join(STATIC, MAP[(base, index)]), size, 0, *a, **k)
    return _orig_truetype(font, size, index, *a, **k)


def _by_axes(self, axes):
    if hasattr(self, '_fa_family'):
        return _reopen(self, axes[-1])   # SF: l'ultimo asse e' sempre il peso
    return _orig_axes(self, axes)


def _by_name(self, name):
    if hasattr(self, '_fa_family'):
        return _reopen(self, _weight_of_name(name))
    return _orig_name(self, name)


def _get_axes(self):
    if hasattr(self, '_fa_family'):
        return [{'name': b'Weight', 'minimum': 100, 'default': 400, 'maximum': 900}]
    return _orig_get(self)


ImageFont.truetype = _truetype
FT.set_variation_by_axes, FT.set_variation_by_name, FT.get_variation_axes = _by_axes, _by_name, _get_axes


def apply(S):
    """small_it.py: stili misurati per i font liberi, su carte inglesi HD (fit_descfont.py, fit_metrics2.py)."""
    S.DESC['effect'].update(px=4.528, hs=1.39, emb=3, ink=1.0, dk=0.952, pitch=5.42, base=203.95, nmax=6,
                            edge={'g': 1.001, 'sx': 0.519, 'sy': 0.5, 'kx': 1.0, 'hx': 1.291, 'ky': 0.383, 'hy': 1.651})
    S.DESC['normal'].update(px=5.008, hs=1.58, emb=3, ink=0.994, dk=0.894, pitch=5.29, base=204.0, nmax=6,
                            edge={'g': 1.0, 'sx': 0.515, 'sy': 0.452, 'kx': 1.441, 'hx': 0.78, 'ky': 0.223, 'hy': 1.061})
    S.NAME.update(cap=10.2, sc=0.80, emb=0, hs=1.34, base=25.6, x=18.75)
    # prima riga 0,5 px piu' in basso (passo ridotto per restare sopra ATK/DEF): le aste alte dei font liberi la facevano
    # sembrare attaccata al tipo. Riga del tipo ed etichetta: parametri originali (la misura non era affidabile, corr 0,1).
