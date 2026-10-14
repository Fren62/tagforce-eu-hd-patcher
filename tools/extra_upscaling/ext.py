import pycdlib,os,sys
iso=pycdlib.PyCdlib(); iso.open(sys.argv[1])
out=sys.argv[2]; base='/PSP_GAME/USRDIR'
n=tot=0
def walk(d):
    global n,tot
    for c in iso.list_children(iso_path=d):
        name=c.file_identifier().decode()
        if name in('.','..'):continue
        p=d+'/'+name
        if c.is_dir():
            if p.lower().endswith(('/movie','/snd','/card')): continue
            walk(p)
        else:
            nm=name.split(';')[0]
            if nm.lower().endswith(('.ehp','.gim')):
                rel=p[len(base):].split(';')[0]
                dst=out+rel.replace('/',os.sep); os.makedirs(os.path.dirname(dst),exist_ok=True)
                iso.get_file_from_iso(dst,iso_path=p); n+=1; tot+=c.data_length
walk(base); print(n,tot/1e6)
