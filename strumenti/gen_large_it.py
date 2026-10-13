"""Write cards/large_<lingua>/*.png (lingua dal cardinfo_xxx.ehp, vedi lingue.py): HD large cards with the name in the banner.
usage: gen_large_it.py TOOLS PACK_DIR CARDINFO_EHP [LIMIT]
TF1_IDS="4476 5104 ..." (variabile d'ambiente): rigenera solo le carte con quegli id."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)))); import font_alt  # noqa: nessun font Apple
import os, re, sys
from multiprocessing import Pool
sys.path.insert(0, sys.argv[1])
from banner import extract, write_back, text_color, make_banner
from cardnames import names
import lingue
LANG = lingue.corrente()
from PIL import Image

pack, ehp = sys.argv[2], sys.argv[3]
src, dst = os.path.join(pack, 'cards/large'), os.path.join(os.environ.get('TF1_OUT', pack), f'cards/large_{LANG}')
NAMES = names(ehp)


def one(fn):
    m = re.match(r'(\d+)', fn)
    if not m or int(m.group(1)) not in NAMES:
        return fn, 'skip'
    im = Image.open(os.path.join(src, fn)).convert('RGBA')
    color = text_color(extract(im))
    if color is None:
        return fn, 'notext'
    write_back(im, make_banner(NAMES[int(m.group(1))], color)).save(os.path.join(dst, fn), optimize=False)
    return fn, 'ok'


if __name__ == '__main__':
    os.makedirs(dst, exist_ok=True)
    only = {int(x) for x in os.environ.get('TF1_IDS', '').split()}
    files = sorted(f for f in os.listdir(src) if f.endswith('.png') and (not only or int(re.match(r'\d+', f).group(0)) in only))[:int(sys.argv[4]) if len(sys.argv) > 4 else None]
    with Pool() as p:
        res = p.map(one, files, chunksize=16)
    from collections import Counter
    print(Counter(r for _, r in res), [f for f, r in res if r != 'ok'][:10])
