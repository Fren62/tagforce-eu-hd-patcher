import json,os,sys,subprocess,shutil,numpy as np,cv2
from PIL import Image
T=os.environ['TEMP']; rows=json.load(open(T+'/unc/list.json'))
os.makedirs(T+'/rgb',exist_ok=True)
for r in rows:
    a=np.array(Image.open(f"{T}/unc/{r['hash']}.png").convert('RGBA'))
    rgb=a[...,:3].copy(); m=(a[...,3]>0).astype(np.uint8)
    # colori dei pixel trasparenti: copiati dai vicini opachi (dilatazione ripetuta), cosi' l'AI non vede nero
    for _ in range(64):
        if m.all(): break
        k=np.ones((3,3),np.uint8); d=cv2.dilate(rgb*m[...,None],k); c=cv2.dilate(m,k)
        sel=(m==0)&(c>0)
        cnt=cv2.filter2D(m.astype(np.float32),-1,k.astype(np.float32)/1,borderType=cv2.BORDER_REPLICATE)
        sm=cv2.filter2D((rgb*m[...,None]).astype(np.float32),-1,np.ones((3,3),np.float32),borderType=cv2.BORDER_REPLICATE)
        avg=(sm/np.maximum(cnt[...,None],1)).astype(np.uint8)
        rgb[sel]=avg[sel]; m=(m|sel).astype(np.uint8)
    Image.fromarray(rgb,'RGB').save(f"{T}/rgb/{r['hash']}.png")
E=T+'/resr/x/realesrgan-ncnn-vulkan.exe'
for out,n in(('ai1','realesr-animevideov3'),('ai2','realesrgan-x4plus-anime')):
    tmp=f"{T}/all/{out}_rgb"; shutil.rmtree(tmp,ignore_errors=True); os.makedirs(tmp)
    subprocess.run([E,'-i',T+'/rgb','-o',tmp,'-n',n,'-s','4','-f','png'],capture_output=True,cwd=T+'/resr/x')
    d=f"{T}/pp/packs/{out}"
    for r in rows:
        a=np.array(Image.open(f"{T}/unc/{r['hash']}.png").convert('RGBA')); h,w=a.shape[:2]
        up=np.array(Image.open(f"{tmp}/{r['hash']}.png").convert('RGB'))
        al=cv2.resize(a[...,3],(w*4,h*4),interpolation=cv2.INTER_LANCZOS4)
        Image.fromarray(np.dstack([up,al]),'RGBA').save(f"{d}/{r['hash']}.png")
    print(out,'ok')
