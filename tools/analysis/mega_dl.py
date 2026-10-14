import sys, json, base64, struct, requests
from Crypto.Cipher import AES
from Crypto.Util import Counter
def b64(s): s=s.replace('-','+').replace('_','/'); return base64.b64decode(s+'='*(-len(s)%4))
fid,key=sys.argv[1].split('#'); out=sys.argv[2]
k=struct.unpack('>8I',b64(key))
aes=[k[0]^k[4],k[1]^k[5],k[2]^k[6],k[3]^k[7]]; iv=(k[4],k[5])
r=requests.post('https://g.api.mega.co.nz/cs',params={'id':0},json=[{'a':'g','g':1,'p':fid}]).json()[0]
if isinstance(r,int): sys.exit('mega error %d'%r)
a=AES.new(struct.pack('>4I',*aes),AES.MODE_CBC,b'\0'*16).decrypt(b64(r['at']))
print(a.rstrip(b'\0'),r['s'],flush=True)
c=AES.new(struct.pack('>4I',*aes),AES.MODE_CTR,counter=Counter.new(64,prefix=struct.pack('>2I',*iv),initial_value=0))
done=0
with requests.get(r['g'],stream=True) as s, open(out,'wb') as f:
    for ch in s.iter_content(1<<20):
        f.write(c.decrypt(ch)); done+=len(ch)
        if done%(100<<20)<(1<<20): print(done>>20,'MB',flush=True)
print('done',done)
