"""PSP GIM image decoder + PPSSPP texture-replacement data hash (xxh64, seed 0xBACD7814, low 32 bits).
parse(data) -> dict(fmt, order, w, h, pitch_px, pixels(bytes of level 0 as stored), palette(list of RGBA or None), pal_fmt)
to_png(g) -> PIL RGBA image; data_hash(g) -> '%08x' or None when the GE size would read past the image."""
import struct
import numpy as np
import xxhash
from PIL import Image

BPP = {0: 16, 1: 16, 2: 16, 3: 32, 4: 4, 5: 8, 6: 16, 7: 32, 8: 4, 9: 8, 10: 8}


def _chunks(d, off, end):
    while off < end:
        cid, _, size, nxt, dat = struct.unpack_from('<HHIII', d, off)
        yield cid, off, size, nxt, dat
        if cid in (2, 3):                      # root / picture: descend
            yield from _chunks(d, off + dat, off + size)
        off += size if size else end


def _image_header(d, off):
    (hs, ref, fmt, order, w, h, bpp_al, pitch_al, h_al, dims, _, _,
     idx_start, px_start, px_end, plane, lvl_type, lvl_count, frm_type, frm_count) = struct.unpack_from('<12H4I4H', d, off)
    return dict(fmt=fmt, order=order, w=w, h=h, pitch_al=pitch_al or 16, h_al=h_al or 1, px_start=px_start, px_end=px_end,
                idx_start=idx_start, levels=lvl_count, frames=frm_count)


def _colors(raw, fmt):
    if fmt == 3:
        a = np.frombuffer(raw, np.uint8).reshape(-1, 4)
        return a.copy()
    v = np.frombuffer(raw[:len(raw) // 2 * 2], '<u2').astype(np.uint32)
    if fmt == 0:   # 5650
        r, g, b, a = v & 31, v >> 5 & 63, v >> 11 & 31, np.full_like(v, 255)
        return np.stack([r * 255 // 31, g * 255 // 63, b * 255 // 31, a], -1).astype(np.uint8)
    if fmt == 1:   # 5551
        r, g, b, a = v & 31, v >> 5 & 31, v >> 10 & 31, v >> 15
        return np.stack([r * 255 // 31, g * 255 // 31, b * 255 // 31, a * 255], -1).astype(np.uint8)
    r, g, b, a = v & 15, v >> 4 & 15, v >> 8 & 15, v >> 12   # 4444
    return np.stack([r * 17, g * 17, b * 17, a * 17], -1).astype(np.uint8)


def parse(d):
    if d[:4] != b'MIG.':
        return None
    img = pal = None
    for cid, off, size, nxt, dat in _chunks(d, 16, len(d)):
        if cid == 4 and img is None:
            h = _image_header(d, off + dat)
            base = off + dat
            pitch_bytes = -(-h['w'] * BPP[h['fmt']] // 8 // h['pitch_al']) * h['pitch_al']
            if h['fmt'] >= 8:   # DXT: blocks of 4x4
                pitch_bytes = (h['w'] // 4) * (8 if h['fmt'] == 8 else 16)
            rows = h['h'] if h['fmt'] < 8 else h['h'] // 4
            n = pitch_bytes * rows
            h['pixels'] = d[base + h['px_start']:base + h['px_start'] + n]
            h['pitch_px'] = pitch_bytes * 8 // BPP[h['fmt']] if h['fmt'] < 8 else h['w']
            img = h
        elif cid == 5 and pal is None:
            p = _image_header(d, off + dat)
            base = off + dat
            raw = d[base + p['px_start']:base + p['px_end']]
            pal = (_colors(raw, p['fmt']), p['fmt'], raw)
    if img is None:
        return None
    img['palette'], img['pal_fmt'], img['pal_raw'] = (pal if pal else (None, None, None))
    return img


def _unswizzle(raw, pitch_bytes, rows):
    out = bytearray(len(raw))
    bw = pitch_bytes // 16
    src = 0
    for by in range(0, rows, 8):
        for bx in range(bw):
            for y in range(8):
                if by + y >= rows:
                    src += 16
                    continue
                dst = (by + y) * pitch_bytes + bx * 16
                out[dst:dst + 16] = raw[src:src + 16]
                src += 16
    return bytes(out)


def to_png(g):
    fmt, w, h = g['fmt'], g['w'], g['h']
    if fmt >= 8:
        return None
    bpp = BPP[fmt]
    pitch_bytes = g['pitch_px'] * bpp // 8
    raw = g['pixels'].ljust(pitch_bytes * h, b'\0')
    if g['order'] == 1:
        rows = -(-h // 8) * 8
        raw = _unswizzle(raw.ljust(pitch_bytes * rows, b'\0'), pitch_bytes, rows)
    a = np.frombuffer(raw[:pitch_bytes * h], np.uint8).reshape(h, pitch_bytes)
    if fmt == 4:
        idx = np.stack([a & 15, a >> 4], -1).reshape(h, -1)[:, :w]
    elif fmt == 5:
        idx = a[:, :w]
    elif fmt in (6, 7):
        return None
    else:
        px = _colors(a.tobytes(), fmt).reshape(h, -1, 4)[:, :w]
        return Image.fromarray(px, 'RGBA')
    pal = g['palette']
    if pal is None:
        return Image.fromarray((idx * (255 // max(1, idx.max()))).astype(np.uint8), 'L').convert('RGBA')
    idx = np.clip(idx, 0, len(pal) - 1)
    return Image.fromarray(pal[idx], 'RGBA')


def pow2(n):
    p = 1
    while p < n:
        p *= 2
    return p


def data_hash(g):
    """PPSSPP ComputeHash (xxh64, contiguous case bufw <= w): bufw*h pixels of the GE texture (power-of-two w, h)."""
    W, H = pow2(g['w']), pow2(g['h'])
    bufw = g['pitch_px']
    if g['fmt'] >= 8:
        bufw = g['w']
    if bufw > W:   # rows with gaps: PPSSPP hashes each row and combines (result * 11) ^ row
        bpl = BPP[g['fmt']] * W // 8
        stride = BPP[g['fmt']] * bufw // 8
        if (H - 1) * stride + bpl > len(g['pixels']):
            return None
        res = 0
        for y in range(H):
            row = xxhash.xxh64_intdigest(g['pixels'][y * stride:y * stride + bpl], 0xBACD7814) & 0xffffffff
            res = ((res * 11) & 0xffffffff) ^ row
        return '%08x' % res
    size = (BPP[g['fmt']] * (bufw * H + (W - bufw))) // 8
    if size > len(g['pixels']):
        return None          # reads past the stored image (height not a power of two)
    return '%08x' % (xxhash.xxh64_intdigest(g['pixels'][:size], 0xBACD7814) & 0xffffffff)
