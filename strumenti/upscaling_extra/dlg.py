import subprocess,sys,time,os
from PIL import Image
import numpy as np
P=os.path.join(os.environ['TEMP'], 'vigem', 'pw.py'); T=os.path.join(os.environ['TEMP'],'vigem')
def shot(p):
    subprocess.run([sys.executable,'-P',P,p],capture_output=True); return Image.open(p).convert('RGB')
def cmd(c):
    open(T+'/cmd.txt','a').write(c+'\n')
def dialog(im):
    a=np.asarray(im.crop((600,830,1500,960))).astype(int)
    return a.mean()>200 and a.std()<45
if __name__=='__main__':
    for i in range(int(sys.argv[1])):
        im=shot(T+'/cur.png')
        if not dialog(im): print('libero dopo',i); break
        cmd('btn A'); time.sleep(2.5)
