import sys,os,re,glob,json
sys.path.insert(0,'strumenti')
from ehp import read
import gim
U=os.path.expandvars(r'%TEMP%\usr'); out=os.path.expandvars(r'%TEMP%\unc'); os.makedirs(out,exist_ok=True)
pack=set()
for l in open('PSP/TEXTURES/ULES00600/textures.ini',encoding='utf-8',errors='replace'):
    m=re.match(r'^([0-9a-fA-F]{24})\s*=',l.strip())
    if m: pack.add(m.group(1)[16:].lower())
inv={r['hash']:r for r in json.load(open('strumenti/analisi/inventory.json'))}
seen={};rows=[]
for p in sorted(glob.glob(U+'/**/*.ehp',recursive=True)+glob.glob(U+'/**/*.gim',recursive=True)):
    rel=os.path.relpath(p,U).replace(chr(92),'/')
    try: mem=read(p).items() if p.endswith('.ehp') else [(os.path.basename(p),open(p,'rb').read())]
    except Exception: continue
    for n,d in mem:
        if not n.endswith('.gim'): continue
        g=gim.parse(d)
        if not g: continue
        h=gim.data_hash(g)
        if not h or h in pack or h in seen: continue
        im=gim.to_png(g)
        if im is None: continue
        seen[h]=1
        fn=f"{h}.png"; im.save(os.path.join(out,fn))
        rows.append(dict(hash=h,file=rel,member=n,w=g['w'],h=g['h'],lang=inv.get(h,{}).get('lang_specific')))
json.dump(rows,open(os.path.join(out,'list.json'),'w'))
print(len(rows), sum(1 for r in rows if r['lang']))
for r in rows:
    if r['lang']: print(r['file'],r['member'],r['w'],r['h'])
