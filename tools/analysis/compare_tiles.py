import sys,glob,os
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, '..', 'ui_textures'))
sys.path.insert(0, os.path.join(_here, '..'))
import common
from PIL import Image
U = os.environ['TF1_USRDIR']   # extracted PSP_GAME/USRDIR folder
arch,d,pat,out=sys.argv[1:5]
fs=sorted(glob.glob(d+'/'+pat))
cols=int(sys.argv[5]) if len(sys.argv)>5 else 6
tiles=[]
for f in fs:
    n=os.path.basename(f)[:-4].split('__',1)[1]
    lo,_=common.texture(U,arch,n+'.gim'); lo=lo.convert('RGBA')
    hd=Image.open(f).convert('RGBA')
    sc=lo.resize(hd.size,Image.NEAREST)
    pair=Image.new('RGBA',(hd.width,hd.height*2),(100,100,100,255)); pair.alpha_composite(sc,(0,0)); pair.alpha_composite(hd,(0,hd.height))
    tiles.append(pair)
w,h=tiles[0].size; k=min(w,300)/w
rows=(len(tiles)+cols-1)//cols
sh=Image.new('RGBA',(cols*w,rows*h),(100,100,100,255))
for i,t in enumerate(tiles): sh.alpha_composite(t,((i%cols)*w,(i//cols)*h))
sh=sh.resize((int(sh.width*350/w),int(sh.height*350/w)))
sh.convert('RGB').save(out); print(sh.size)
