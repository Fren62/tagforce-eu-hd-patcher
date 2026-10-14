"""Fit the description style (font size, line pitch, first baseline, weight, horizontal scale) on the
English text of the HD pack's small cards, with justified lines like real cards.
usage: fit_desc.py TOOLS CARDS_DIR CLEAN_DIR CARDINFO_ENG KIND FONT_FILE FONT_INDEX
KIND: effect (effect monsters), normal (normal monsters, italic), st (spells/traps)"""
import os, re, sys
sys.path.insert(0, sys.argv[1])
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import small_it as S
from cardprops import load
from smallbg import frame_of

cdir, clean_dir, ehp, kind = sys.argv[2:6]
FONT = (sys.argv[6], int(sys.argv[7]))
cards = load(ehp)
CLEAN = {g: np.asarray(Image.open(os.path.join(clean_dir, f'clean_{g}.png')).convert('RGB')).astype(np.float32)
         for g in ('normal', 'effect', 'fusion', 'ritual', 'spell', 'trap', 'token')}
BOX = {'effect': (19, 199, 237, 231), 'normal': (19, 199, 237, 231), 'st': (19, 192, 237, 240)}[kind]


def pick():
    out = []
    for cid, c in sorted(cards.items()):
        if not os.path.exists(os.path.join(cdir, 'small', f'{cid}.png')):
            continue
        ok = {'effect': c['kind'] == 1, 'normal': c['kind'] == 0, 'st': c['kind'] in (13, 14)}[kind]
        if ok and 60 <= len(c['desc']) <= 150 and '\n' not in c['desc']:
            out.append(cid)
    return out[::max(1, len(out) // 10)][:10]


IDS = pick()


def ink(cid):
    img = np.asarray(Image.open(os.path.join(cdir, 'small', f'{cid}.png')).convert('RGB')).astype(np.float32)
    x0, y0, x1, y1 = BOX
    return np.abs(img - CLEAN[frame_of(cards[cid])]).sum(-1)[y0:y1, x0:x1]


INK = {cid: ink(cid) for cid in IDS}


def render(text, p):
    """justified paragraph -> alpha (0..1) of the BOX region."""
    x0, y0, x1, y1 = BOX
    f = S.font(FONT, p['px'] * S.SS)
    width = (p['x1'] - p['x0']) * S.SS / p['hs']
    lines = S.wrap(text.split(), f, width)
    asc, dsc = f.getmetrics()
    cv = np.zeros((y1 - y0, x1 - x0), np.float32)
    for i, line in enumerate(lines):
        words = line.split()
        last = i == len(lines) - 1
        nat = f.getlength(line)
        gap = f.getlength(' ')
        if not last and len(words) > 1:
            gap += (width - nat) / (len(words) - 1)   # justify
        im = Image.new('L', (int(width + 4 * S.SS), asc + dsc + S.SS), 0)
        dr = ImageDraw.Draw(im)
        x = 0.0
        for w in words:
            dr.text((x, asc), w, font=f, fill=255, anchor='ls')
            x += f.getlength(w) + gap
        if p['emb']:
            im = im.filter(ImageFilter.MaxFilter(p['emb']))
        m = np.asarray(im.resize((max(1, round(im.width / S.SS * p['hs'])), max(1, round(im.height / S.SS))), Image.LANCZOS)).astype(np.float32) / 255
        base = p['base'] + i * p['pitch']
        top = int(round(base - asc / S.SS)) - y0
        left = int(round(p['x0'])) - x0
        ya, yb = max(0, top), min(cv.shape[0], top + m.shape[0])
        xb = min(cv.shape[1], left + m.shape[1])
        if yb > ya:
            cv[ya:yb, left:xb] = np.maximum(cv[ya:yb, left:xb], m[ya - top:yb - top, :xb - left])
    return cv, len(lines)


def corr(a, b):
    a = cv2.GaussianBlur(a, (0, 0), 0.7); b = cv2.GaussianBlur(b, (0, 0), 0.7)
    a = a - a.mean(); b = b - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))


def score(p):
    return sum(corr(INK[cid], render(cards[cid]['desc'], p)[0]) for cid in IDS) / len(IDS)


p = dict(px=6.3, pitch=5.5, base=204.0 if kind != 'st' else 198.0, x0=21.0, x1=236.0, emb=3, hs=1.0)  # pitch measured: 5.5
grid = [('base', np.arange(p['base'] - 2, p['base'] + 2.01, 0.25)), ('px', np.arange(5.0, 8.01, 0.2)),
        ('hs', np.arange(0.84, 1.17, 0.02)), ('emb', [0, 3, 5]),
        ('x0', np.arange(19.5, 23.1, 0.5)), ('x1', np.arange(233.0, 237.1, 0.5))]
if __name__ == '__main__':
  best = score(p)
  print(os.path.basename(FONT[0]), FONT[1], 'campioni', len(IDS), 'iniziale %.4f' % best, flush=True)
  for rnd in range(3):
      for key, vals in grid:
          for v in vals:
              q = dict(p); q[key] = float(v) if key != 'emb' else int(v)
              s = score(q)
              if s > best + 1e-5:
                  best, p = s, q
      print(f'giro {rnd + 1}: correlazione media {best:.4f}', {k: round(v, 3) for k, v in p.items()}, flush=True)
