import sys
sys.path.insert(0,'F:/Progetti/Mods/Yu-Gi-Oh! Tag Force/Tag Force Versione Pomodoro Mistico/strumenti/ui_it'); sys.path.insert(0,'F:/Progetti/Mods/Yu-Gi-Oh! Tag Force/Tag Force Versione Pomodoro Mistico/strumenti')
import common
from PIL import Image
U='F:/Progetti/Mods/_download_pack_usa/USRDIR'
out=sys.argv[1]; sc=int(sys.argv[2]); ims=[]
for a in sys.argv[3:]:
    f,m=a.split(':')
    im,h=common.texture(U,f,m); print(a,im.size)
    b=Image.new('RGBA',im.size,(110,110,110,255)); b.alpha_composite(im.convert('RGBA')); ims.append(b.resize((b.width*sc,b.height*sc),Image.NEAREST))
W=max(i.width for i in ims); H=sum(i.height+6 for i in ims)
sh=Image.new('RGB',(W,H),(60,60,60)); y=0
for i in ims: sh.paste(i,(0,y)); y+=i.height+6
sh.save(out)
