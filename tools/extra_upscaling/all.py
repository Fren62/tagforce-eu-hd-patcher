import json,os,numpy as np,cv2
from PIL import Image
T=os.environ['TEMP']; rows=json.load(open(T+'/unc/list.json'))
os.makedirs(T+'/all/lan',exist_ok=True)
for r in rows:
    a=np.array(Image.open(f"{T}/unc/{r['hash']}.png").convert('RGBA')); h,w=a.shape[:2]
    f=a.astype(np.float32); al=f[...,3:]/255; pm=np.concatenate([f[...,:3]*al,f[...,3:]],-1)
    up=cv2.resize(pm,(w*4,h*4),interpolation=cv2.INTER_LANCZOS4); up=up+0.7*(up-cv2.GaussianBlur(up,(0,0),1.2))
    A=np.clip(up[...,3:],0,255); rgb=np.clip(up[...,:3]/np.maximum(A/255,1e-3),0,255)
    Image.fromarray(np.clip(np.concatenate([rgb,A],-1)+0.5,0,255).astype(np.uint8),'RGBA').save(f"{T}/all/lan/{r['hash']}.png")
print(len(rows))
