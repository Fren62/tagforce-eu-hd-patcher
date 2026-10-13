"""Carica le correzioni ai testi delle carte e le applica ai testi letti da cardinfo_xxx.ehp: dati/correzioni_carte.json per l'italiano
(generato da genera_correzioni.py), dati/correzioni_carte_<lingua>.json (fr, de, es, en) per le altre.
Usato da cardprops.load / cardnames.names: tutte le immagini generate (carte HD, carte piccole, nomi) usano i testi corretti.
Per usare i testi originali: variabile d'ambiente TF1_SENZA_CORREZIONI=1."""
import json, os

_DATI = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dati')
_C = {}


def _file(lingua):
    return os.path.join(_DATI, 'correzioni_carte.json' if lingua == 'it' else f'correzioni_carte_{lingua}.json')


def tabella(lingua='it'):
    if lingua not in _C:
        _C[lingua] = {}
        if not os.environ.get('TF1_SENZA_CORREZIONI') and os.path.exists(_file(lingua)):
            _C[lingua] = {int(k): v for k, v in json.load(open(_file(lingua), encoding='utf-8')).items()}
    return _C[lingua]


def carta(card_id, campo, testo, lingua='it'):
    """testo corretto di `campo` ('name' o 'desc') della carta, o `testo` se non ci sono correzioni per quella lingua."""
    return tabella(lingua).get(card_id, {}).get(campo, testo)
