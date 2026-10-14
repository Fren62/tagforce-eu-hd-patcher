"""Creates static/ with static instances (Regular, Medium, SemiBold, Bold, ExtraBold, Black) of the variable fonts in downloaded/.  Requires: pip install fonttools"""
import glob, os, shutil, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
here = os.path.dirname(os.path.abspath(__file__)); os.makedirs(here + '/static', exist_ok=True)
for f in sorted(glob.glob(here + '/downloaded/*.ttf')):
    tt = TTFont(f); base = os.path.basename(f)[:-4]
    if 'fvar' not in tt:
        shutil.copy(f, here + '/static/'); continue
    ax = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in tt['fvar'].axes}
    for name, w in (('Regular', 400), ('Medium', 500), ('SemiBold', 600), ('Bold', 700), ('ExtraBold', 800), ('Black', 900)):
        loc = {'wght': min(max(w, ax['wght'][0]), ax['wght'][2])}
        if 'opsz' in ax: loc['opsz'] = min(max(14, ax['opsz'][0]), ax['opsz'][2])
        if 'wdth' in ax: loc['wdth'] = ax['wdth'][1]
        out = f'{here}/static/{base}-{name}.ttf'
        if not os.path.exists(out):
            instancer.instantiateVariableFont(TTFont(f), loc, inplace=False).save(out)
for f in glob.glob(here + '/xcharter/*.otf'): shutil.copy(f, here + '/static/')
