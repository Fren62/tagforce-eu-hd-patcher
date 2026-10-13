import sys
sys.path.insert(0,'F:/Progetti/Mods/Yu-Gi-Oh! Tag Force/Tag Force Versione Pomodoro Mistico/strumenti/ui_it'); sys.path.insert(0,'F:/Progetti/Mods/Yu-Gi-Oh! Tag Force/Tag Force Versione Pomodoro Mistico/strumenti')
import common
from PIL import Image
U='F:/Progetti/Mods/_download_pack_usa/USRDIR'
out=sys.argv[1]; scale=int(sys.argv[2]); pattern=sys.argv[3]   # es. deck/all_{L}.ehp:icon04.gim  (L = i,f,e)
f,m=pattern.split(':')
ims=[]
for L in sys.argv[4].split(','):
    try: im,h=common.texture(U,f.replace('{L}',L).replace('{N}',{'i':'ita','f':'fra','e':'eng'}[L]),m.replace('{L}',L))
    except Exception as e: print('manca',L,e); continue
    print(L,im.size,h)
    b=Image.new('RGBA',im.size,(110,110,110,255)); b.alpha_composite(im.convert('RGBA'))
    ims.append(b.resize((b.width*scale,b.height*scale),Image.NEAREST))
W=sum(i.width+6 for i in ims); H=max(i.height for i in ims)
sh=Image.new('RGB',(W,H),(60,60,60)); x=0
for i in ims: sh.paste(i,(x,0)); x+=i.width+6
sh.save(out)
