"""Tag Force 1 card archive helpers: CIP index, PSP DXT1 decode, PPSSPP hash keys."""
import struct
import numpy as np
import xxhash

SEED = 0xBACD7814


def hdr(d):
    return struct.unpack_from('<9I', d, 0)


def slots(d, cid):
    """sector numbers of all art slots for card id (alt arts follow a list)."""
    h = hdr(d); mn, ott = h[5], h[7]
    sid, _ = struct.unpack_from('<II', d, ott + (cid - mn) * 8)
    if sid & 0x80000000:
        p = sid & 0x7fffffff; out = []
        while True:
            s, _ = struct.unpack_from('<II', d, p); out.append(s & 0x7fffffff); p += 8
            if s & 0x80000000:
                return out
    return [sid]


def card_ids(d):
    h = hdr(d)
    return range(h[5], h[6] + 1)


def key(clut, data):
    return '%08x' % (xxhash.xxh64_intdigest(data, SEED) & 0xffffffff)


def small_blob(d, s):          # cardm: raw 64x64 DXT1, 2048 bytes
    return d[s * 2048:s * 2048 + 2048]


def large_blob(d, s):          # cardh: 128-byte GIM header + 3968 px bytes
    return d[s * 2048:s * 2048 + 4096]


def large_keys(blob, stable=True):
    """PPSSPP keys for a 128x64 DXT1 card: the in-game texture runs 128 bytes past
    the slot (zeros or the next GIM header). With skipLastDXT1Blocks128x64 = 16
    PPSSPP hashes only the 3968 bytes we know -> one stable key (issue #19714)."""
    px = blob[128:]
    legacy = [key(0, px + t) for t in (b'\0' * 128, blob[:128])]
    return ([key(0, px[:3968])] if stable else []) + legacy


def dxt1(data, w, h):
    """decode PSP DXT1 (block = 4 index bytes, then color0, color1)."""
    data = data.ljust(w * h // 2, b'\0')
    out = np.zeros((h, w, 3), np.uint8)
    bw = w // 4
    for bi in range(w * h // 16):
        o = bi * 8
        lines = data[o:o + 4]
        c0, c1 = struct.unpack_from('<HH', data, o + 4)
        def rgb(c): return np.array([(c >> 11 & 31) * 255 // 31, (c >> 5 & 63) * 255 // 63, (c & 31) * 255 // 31], np.int32)
        a, b = rgb(c0), rgb(c1)
        pal = [a, b, (2 * a + b) // 3, (a + 2 * b) // 3] if c0 > c1 else [a, b, (a + b) // 2, np.zeros(3, np.int32)]
        by, bx = divmod(bi, bw)
        for y in range(4):
            for x in range(4):
                out[by * 4 + y, bx * 4 + x] = pal[(lines[y] >> (2 * x)) & 3]
    return out
