"""Corregge i dialoghi italiani (script/st0X_t01_i.ehp) con dati/correzioni_dialoghi_it.json (id 'st01_t01/Scr077E#3' -> attuale, proposto).
Ogni scena e' una coppia di file (gz oppure no): ...Ii (offset in caratteri UTF-16) e ...Li (stringhe UTF-16LE, ognuna chiusa da NUL)."""
import gzip, json, os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import applica_iso as ai

def dati(lingua='it'):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dati', f'correzioni_dialoghi_{lingua}.json')
FINE = ' \n\r\t' + chr(0)          # spazi, a capo e NUL finali: restano come nel gioco
LARGHEZZA = 46                      # il gioco non va a capo da solo: nel testo originale le righe arrivano a ~49 caratteri
LETTERA = {'it': 'i', 'fr': 'f', 'de': 'g', 'es': 's', 'en': 'e'}
MAX_RIGHE = 3                       # righe che stanno nel box (nel testo originale: 3 righe in 1.108 stringhe, di piu' in 53)


def larghezza(riga):
    return len(re.sub('《[^》]*》', 'XXXXXX', riga))      # un segnaposto 《...》 occupa circa 6 caratteri (nome del personaggio)


def riadatta(t):
    """va a capo a mano solo se una riga e' piu' larga del box; altrimenti lascia le interruzioni della proposta."""
    if all(larghezza(r) <= LARGHEZZA for r in t.split('\n')):
        return t
    righe, cur = [], ''
    for w in t.replace('\n', ' ').split():
        if cur and larghezza(cur + ' ' + w) > LARGHEZZA:
            righe.append(cur); cur = w
        else:
            cur = cur + ' ' + w if cur else w
    return '\n'.join(righe + [cur])


def _nome(files, sc, tipo, l):
    n = f'{sc}{tipo}{l}.bin'
    return n + '.gz' if n + '.gz' in files else n                                      # alcune scene (ImpMapMsg...) non sono compresse


def _leggi(files, n):
    return gzip.decompress(files[n]) if n.endswith('.gz') else bytes(files[n])


def _metti(files, n, d):
    files[n] = bytearray(gzip.compress(d, 9, mtime=0) if n.endswith('.gz') else d)


def stringhe(files, sc, l):
    i, t = _leggi(files, _nome(files, sc, 'I', l)), _leggi(files, _nome(files, sc, 'L', l))
    o = list(struct.unpack(f'<{len(i) // 4}I', i)) + [len(t) // 2]
    return [t[o[k] * 2:o[k + 1] * 2].decode('utf-16-le') for k in range(len(o) - 1)]


def scrivi(files, sc, l, testi):
    off, pos = [], 0
    for s in testi:
        off.append(pos); pos += len(s)
    _metti(files, _nome(files, sc, 'I', l), struct.pack(f'<{len(off)}I', *off))
    _metti(files, _nome(files, sc, 'L', l), ''.join(testi).encode('utf-16-le'))


def patch(iso_get, avvisi, lingua='it'):
    """iso_get(percorso) -> bytes. Restituisce ({percorso ISO: (originale, nuovo)}, righe riscritte) e riempie `avvisi`."""
    per_scena = {}
    for id_, c in json.load(open(dati(lingua), encoding='utf-8')).items():
        st, rest = id_.split('/'); sc, idx = rest.split('#')
        per_scena.setdefault(st, {}).setdefault(sc, []).append((int(idx), c))
    out, n = {}, 0
    for st, scene in per_scena.items():
        p = f'/PSP_GAME/USRDIR/script/{st}_{LETTERA[lingua]}.ehp'
        d = iso_get(p); ents, files = ai.apri(d)
        _, ja = ai.apri(iso_get(f'/PSP_GAME/USRDIR/script/{st}_j.ehp'))
        # l'audit elenca ogni frase una volta sola: la stessa frase (stesso italiano e stesso giapponese) ripetuta in altre
        # scene o in altri rami della conversazione (es. Scr077E #3 e #9) riceve la stessa correzione
        chiave = {}
        for sc, voci in scene.items():
            tj = stringhe(ja, sc, 'j'); ti = stringhe(files, sc, LETTERA[lingua])
            for idx, c in voci:
                chiave.setdefault((ti[idx].rstrip(FINE), tj[idx].rstrip(FINE)), c)
        nomi = sorted({k.split('I' + LETTERA[lingua] + '.bin')[0] for k in files if ('I' + LETTERA[lingua] + '.bin') in k})
        for sc in nomi:
            try:
                ti, tj = stringhe(files, sc, LETTERA[lingua]), stringhe(ja, sc, 'j')
            except KeyError:
                continue
            if len(ti) != len(tj):
                continue
            gia = {i for i, _ in scene.get(sc, [])}
            for idx, (a, b) in enumerate(zip(ti, tj)):
                c = chiave.get((a.rstrip(FINE), b.rstrip(FINE)))
                if c and idx not in gia:
                    scene.setdefault(sc, []).append((idx, c))
        for sc, voci in scene.items():
            testi = stringhe(files, sc, LETTERA[lingua])
            for idx, c in voci:
                vecchio = testi[idx]; coda = vecchio[len(vecchio.rstrip(FINE)):]
                if vecchio.rstrip(FINE) != c['attuale'].rstrip(FINE):
                    avvisi.append(f'{st}/{sc}#{idx}: testo del gioco diverso dall\'audit, saltata'); continue
                nuovo = riadatta(c['proposto'].rstrip(FINE))
                testi[idx] = nuovo + coda; n += 1
                if nuovo.count('\n') + 1 > MAX_RIGHE and nuovo.count('\n') > vecchio.count('\n'):
                    avvisi.append(f'{st}/{sc}#{idx}: {nuovo.count(chr(10)) + 1} righe, potrebbe non stare nel box')
            scrivi(files, sc, LETTERA[lingua], testi)
        out[p] = (d, ai.chiudi(d, ents, files))
    return out, n
