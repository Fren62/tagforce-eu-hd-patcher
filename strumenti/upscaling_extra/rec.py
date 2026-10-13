"""Registra i fotogrammi della finestra PPSSPP (anche se coperta) quando cambiano abbastanza; ~ogni 1.5 s."""
import subprocess, time, os, sys
from PIL import Image, ImageChops, ImageStat
out=sys.argv[1]; dur=int(sys.argv[2]); os.makedirs(out,exist_ok=True)
tmp=os.path.join(out,'_t.png'); pw=os.path.join(os.environ['TEMP'], 'vigem', 'pw.py')
prev=None; n=0; t0=time.time()
while time.time()-t0<dur:
    subprocess.run([sys.executable,'-P',pw,tmp],capture_output=True)
    try: im=Image.open(tmp).convert('RGB').resize((480,270))
    except Exception: time.sleep(1.5); continue
    d=999 if prev is None else sum(ImageStat.Stat(ImageChops.difference(im,prev)).mean)
    if d>6:
        Image.open(tmp).convert('RGB').save(os.path.join(out,f'f{n:04d}.jpg'),quality=80); n+=1; prev=im
    time.sleep(1.2)
print('fatto',n)
