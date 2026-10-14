import os,sys,shutil,subprocess,numpy as np
from PIL import Image
T=os.environ['TEMP'];E=T+'/resr/x/realesrgan-ncnn-vulkan.exe'
def mean(p,s=16): return np.asarray(Image.open(p).convert('L').resize((s,s)),np.float32).mean()
def run(files,n,out):
    s=T+'/ch_in';o=T+'/ch_out'
    for d in(s,o):shutil.rmtree(d,ignore_errors=True);os.makedirs(d)
    for f in files:shutil.copy(f'{T}/rgb/{f}',s)
    subprocess.run([E,'-i',s,'-o',o,'-n',n,'-s','4','-f','png','-j','1:1:1'],capture_output=True,cwd=T+'/resr/x')
    bad=[]
    for f in files:
        p=f'{o}/{f}'
        if os.path.exists(p) and abs(mean(p)-mean(f'{T}/rgb/{f}'))<25: shutil.copy(p,f'{out}/{f}')
        else: bad.append(f)
    return bad
fs=sorted(os.listdir(T+'/rgb'))
for tag,n in(('ai1','realesr-animevideov3'),('ai2','realesrgan-x4plus-anime')):
    out=f'{T}/all/{tag}_rgb';shutil.rmtree(out,ignore_errors=True);os.makedirs(out)
    bad=[]
    for i in range(0,len(fs),150): bad+=run(fs[i:i+150],n,out)
    print(tag,'bad1',len(bad));b2=run(bad,n,out) if bad else [];print(tag,'bad2',len(b2))
    for f in b2:  # last attempt: one at a time
        run([f],n,out)
    print(tag,'tot',len(os.listdir(out)))
