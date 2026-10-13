"""Exact text-free backgrounds of the HD small cards, one per frame type.
Frames are pixel-identical between cards of a type, so for every pixel we take the value
shared by the cards that have no text there:
  name band : cards whose name (width known from the large card) ends left of the pixel
  desc box  : most frequent value among non-dark pixels (text is dark, parchment is light)
  label     : spell/trap label is on every card -> frame texture copied from the empty left part
Remaining holes are inpainted. usage: smallclean.py TOOLS CARDS_DIR CARDINFO_ENG OUT_DIR"""
import os, re, sys, collections
sys.path.insert(0, sys.argv[1])
import cv2
import numpy as np
from PIL import Image
from banner import extract
from cardprops import load
from smallbg import frame_of
from smallmode import mode_cols

NAME_BAND = (18, 11, 211, 31)
DESC_BOX = (19, 192, 238, 247)
LABEL = (116, 31, 233, 44)
RATIO, MARGIN = 0.70, 6   # small name width ~0.64 x large banner width (p90 0.68)


def large_end(path):
    a = np.asarray(extract(Image.open(path).convert('RGBA')))[..., 3]
    cols = np.where((a > 100).any(0))[0]
    return int(cols.max()) if len(cols) else 0


if __name__ == '__main__':
    cdir, ehp, out = sys.argv[2:5]
    os.makedirs(out, exist_ok=True)
    cards = load(ehp)
    groups = collections.defaultdict(list)
    for f in sorted(os.listdir(os.path.join(cdir, 'small'))):
        m = re.match(r'(\d+)', f)
        if f.endswith('.png') and m and int(m.group(1)) in cards and os.path.exists(os.path.join(cdir, 'large', f)):
            groups[frame_of(cards[int(m.group(1))])].append(f)
    for g, fs in groups.items():
        fs = fs[:600]
        stack = np.stack([np.asarray(Image.open(os.path.join(cdir, 'small', f)).convert('RGB')) for f in fs]).astype(np.int32)
        N = len(fs)
        bg = np.median(stack, 0).astype(np.uint8)
        hole = np.zeros((256, 256), np.uint8)
        # --- name band: median over text-free cards per column
        x0, y0, x1, y1 = NAME_BAND
        ends = np.array([19 + RATIO * max(0, large_end(os.path.join(cdir, 'large', f)) - 12) + MARGIN for f in fs])
        first = None
        for x in range(x0, x1):
            free = ends < x
            if free.sum() >= 3:
                col = stack[free, y0:y1, x]
                packed = (col[..., 0] << 16) | (col[..., 1] << 8) | col[..., 2]
                mv, _ = mode_cols(packed)  # exact: frames are identical, free cards agree
                bg[y0:y1, x] = np.stack([(mv >> 16) & 255, (mv >> 8) & 255, mv & 255], -1)
                first = x if first is None else first
        # leftmost columns are always covered by the first letter: copy the box texture from the right
        period = x1 - first
        for x in range(x0, first):
            bg[y0:y1, x] = bg[y0:y1, first + (x - x0) % period]
        for k in range(4):  # feather the seam
            t = (k + 1) / 5
            src = first + (first - 2 + k - x0) % period
            bg[y0:y1, first - 2 + k] = (t * bg[y0:y1, first - 2 + k] + (1 - t) * bg[y0:y1, src]).astype(np.uint8)
        # --- type line + description: per pixel, exact mode over the cards with NO ink near it
        # (ink found per card: darker than its own morphological closing; frames are identical,
        #  so every text-free card has exactly the same value there)
        x0, y0, x1, y1 = 21, 191, 235, (240 if g in ('spell', 'trap') else 231)
        reg = stack[:, y0:y1, x0:x1]
        free = np.zeros(reg.shape[:3], bool)
        for k in range(N):
            luma = cv2.cvtColor(reg[k].astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.int16)
            close = cv2.morphologyEx(luma, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
            ink = ((close - luma) > 8).astype(np.uint8)
            free[k] = cv2.dilate(ink, np.ones((5, 5), np.uint8)) == 0     # 2 px safety margin around ink
        packed = (reg[..., 0] << 16) | (reg[..., 1] << 8) | reg[..., 2]
        packed = np.where(free, packed, -np.random.default_rng(0).integers(1, 1 << 30, free.shape))  # inked: never wins
        mv, share = mode_cols(packed.reshape(N, -1))
        mv = mv.reshape(y1 - y0, x1 - x0); cnt = (share * N).round().reshape(y1 - y0, x1 - x0)
        nfree = free.sum(0)
        good = (mv >= 0) & (cnt >= 3) & (cnt >= 0.3 * np.maximum(nfree, 1))   # free samples must agree
        sub = np.stack([(mv >> 16) & 255, (mv >> 8) & 255, mv & 255], -1).astype(np.uint8)
        region = bg[y0:y1, x0:x1]
        region[good] = sub[good]
        # pixels covered by text on (almost) every card: copy the parchment texture from the same row
        # further right (or from rows below), corrected by the difference of the row tones
        H = ~good
        rowmed = np.array([np.median(region[r][good[r]], 0) if good[r].sum() > 10 else np.full(3, np.nan) for r in range(y1 - y0)])
        for r in range(len(rowmed)):                       # rows without enough clean pixels: nearest row
            if np.isnan(rowmed[r]).any():
                ok = [k for k in range(len(rowmed)) if not np.isnan(rowmed[k]).any()]
                rowmed[r] = rowmed[min(ok, key=lambda k: abs(k - r))]
        fill = region.astype(np.float32).copy()
        for yy, xx in zip(*np.where(H)):
            cands = [(yy, xx + dx) for dx in range(110, 211, 10)] + [(yy + dy, xx) for dy in range(11, 60, 11)]
            for yd, xd in cands:
                if yd < y1 - y0 - 1 and xd < x1 - x0 - 2 and good[yd, xd]:
                    fill[yy, xx] = region[yd, xd] + (rowmed[yy] - rowmed[yd])
                    break
            else:
                fill[yy, xx] = rowmed[yy]
                hole[y0 + yy, x0 + xx] = 1
        region[:] = np.clip(fill, 0, 255).round().astype(np.uint8)
        hole[y0:y1, x0:x1] = 0   # filled above (no inpainting needed)
        # --- spell/trap label strip: copy frame texture from the empty left side
        if g in ('spell', 'trap'):
            lx0, ly0, lx1, ly1 = LABEL
            ly0, ly1 = 32, 43   # label rows only (row 43+ is the art box border)
            cp = bg.astype(np.float32).copy()
            for x in range(lx0, lx1):  # columns 40..112: plain frame texture, no corners
                cp[ly0 - 1:ly1 + 1, x] = bg[ly0 - 1:ly1 + 1, 40 + (x - lx0) % 72]
            # low-frequency correction so the copy meets the real frame above/below without seams
            top = bg[ly0 - 1, lx0:lx1].astype(np.float32) - cp[ly0 - 1, lx0:lx1]
            bot = bg[ly1, lx0:lx1].astype(np.float32) - cp[ly1, lx0:lx1]
            top = cv2.GaussianBlur(top[None], (0, 0), 6)[0]; bot = cv2.GaussianBlur(bot[None], (0, 0), 6)[0]
            for i, y in enumerate(range(ly0, ly1)):
                t = (i + 1) / (ly1 - ly0 + 1)
                bg[y, lx0:lx1] = np.clip(cp[y, lx0:lx1] + (1 - t) * top + t * bot, 0, 255).astype(np.uint8)
            # feather left/right ends
            for k in range(5):
                t = (k + 1) / 6
                for x in (lx0 + k, lx1 - 1 - k):
                    bg[ly0:ly1, x] = (t * bg[ly0:ly1, x] + (1 - t) * bg[ly0:ly1, x - 1 if x < (lx0 + lx1) // 2 else x + 1]).astype(np.uint8)
        if hole.any():
            bg = cv2.inpaint(bg, hole * 255, 3, cv2.INPAINT_TELEA)
        # pixels identical on most cards are frame (borders, bevels, rules): take them exactly
        packed_all = (stack[..., 0] << 16) | (stack[..., 1] << 8) | stack[..., 2]
        mv, share = mode_cols(packed_all.reshape(N, -1))
        mv = mv.reshape(256, 256); share = share.reshape(256, 256)
        fixed = share >= 0.5
        # never restore text that is merely common (English "[SPELL CARD", the "[" of the type line...)
        text_area = np.zeros((256, 256), bool)
        text_area[11:31, 18:211] = True                     # name
        if g in ('spell', 'trap'):
            text_area[30:45, 100:233] = True                # [SPELL CARD] / [TRAP CARD] label
        else:
            text_area[190:200, 18:236] = True               # [TYPE/KIND] line
        text_area[193:240 if g in ('spell', 'trap') else 230, 20:235] = True   # description (parchment interior)
        fixed &= ~text_area
        bg[fixed] = np.stack([(mv >> 16) & 255, (mv >> 8) & 255, mv & 255], -1).astype(np.uint8)[fixed]
        # description box edge columns: English ink that reached x=20-21 / 234-235 is not frame (mode pixels can keep it)
        ry0, ry1 = (194, 238) if g in ('spell', 'trap') else (199, 230)
        for x in (19, 20, 21, 22, 233, 234, 235, 236):
            col = bg[ry0:ry1, x].astype(np.float32)
            lum = col @ np.array([0.3, 0.59, 0.11], np.float32)
            med = np.median(col, 0)
            dark = lum < np.median(lum) - 12
            col[dark] = med
            bg[ry0:ry1, x] = col.round().astype(np.uint8)
        # QA: no ink-like strokes may remain in the cleaned text areas
        luma = cv2.cvtColor(bg, cv2.COLOR_RGB2GRAY).astype(np.int16)
        resid = (cv2.morphologyEx(luma, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) - luma) > 12
        qa = resid & text_area
        qa[:, 233:] = False; qa[:, :22] = False                    # box borders are not text
        Image.fromarray(bg).save(os.path.join(out, f'clean_{g}.png'))
        print(g, 'QA pixel sospetti nelle zone testo:', int(qa.sum()))
        print(g, N, 'buchi nome', int(hole[11:31, 18:211].sum()), 'buchi descrizione', int(hole[191:240, 21:235].sum()))
