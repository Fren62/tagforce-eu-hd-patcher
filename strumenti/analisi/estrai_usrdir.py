import pycdlib, os, sys
iso=pycdlib.PyCdlib(); iso.open(sys.argv[1]); out=sys.argv[2]
def walk(p):
    for c in iso.list_children(udf_path=p) if False else iso.list_children(**{k:p}):
        pass
k='iso_path'
n=0
def rec(p):
    global n
    for c in iso.list_children(iso_path=p):
        nm=c.file_identifier().decode()
        if nm in ('.','..'): continue
        full=p.rstrip('/')+'/'+nm
        low=full.lower()
        if c.is_dir():
            if low.startswith('/psp_game/usrdir/movie') or low.startswith('/psp_game/usrdir/snd'): continue
            rec(full)
        elif low.startswith('/psp_game/usrdir'):
            dest=os.path.join(out,*full.split(';')[0].split('/')[3:])
            os.makedirs(os.path.dirname(dest),exist_ok=True)
            iso.get_file_from_iso(dest,iso_path=full); n+=1
rec('/PSP_GAME/USRDIR')
print(n,'file')
