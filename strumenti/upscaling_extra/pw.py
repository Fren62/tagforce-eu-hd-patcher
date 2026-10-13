import ctypes, sys
from ctypes import wintypes
from PIL import Image
u=ctypes.windll.user32; g=ctypes.windll.gdi32
u.SetProcessDPIAware()
found=[]
def cb(h,_):
    n=u.GetWindowTextLengthW(h)
    if n:
        b=ctypes.create_unicode_buffer(n+1); u.GetWindowTextW(h,b,n+1)
        if b.value.startswith('PPSSPP Gold') and u.IsWindowVisible(h): found.append(h)
    return True
u.EnumWindows(ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)(cb),0)
h=found[0]; r=wintypes.RECT(); u.GetClientRect(h,ctypes.byref(r)); w,hh=r.right,r.bottom
dc=u.GetDC(h); mdc=g.CreateCompatibleDC(dc); bm=g.CreateCompatibleBitmap(dc,w,hh); g.SelectObject(mdc,bm)
u.PrintWindow(h,mdc,3)
class BI(ctypes.Structure): _fields_=[('s',wintypes.DWORD),('w',wintypes.LONG),('h',wintypes.LONG),('p',wintypes.WORD),('b',wintypes.WORD),('c',wintypes.DWORD),('si',wintypes.DWORD),('x',wintypes.LONG),('y',wintypes.LONG),('u',wintypes.DWORD),('i',wintypes.DWORD)]
bi=BI(40,w,-hh,1,32,0,0,0,0,0,0); buf=ctypes.create_string_buffer(w*hh*4)
g.GetDIBits(mdc,bm,0,hh,buf,ctypes.byref(bi),0)
Image.frombuffer('RGBA',(w,hh),buf,'raw','BGRA',0,1).convert('RGB').save(sys.argv[1]); print(w,hh)
