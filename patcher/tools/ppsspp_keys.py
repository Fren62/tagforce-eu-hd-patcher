"""usage: ppsspp_keys.py NAME[,NAME...]  (sends keys to PPSSPP via SendInput; Z=cross X=circle SPACE=start, arrows; wN = wait N seconds)"""
import ctypes, sys, time
from ctypes import wintypes
u = ctypes.windll.user32
VK = dict(Z=0x5A, X=0x58, SPACE=0x20, UP=0x26, DOWN=0x28, LEFT=0x25, RIGHT=0x27, ENTER=0x0D, A=0x41, S=0x53)
found = []


def cb(h, _):
    n = u.GetWindowTextLengthW(h)
    if n:
        b = ctypes.create_unicode_buffer(n + 1)
        u.GetWindowTextW(h, b, n + 1)
        if b.value.startswith('PPSSPP Gold') and u.IsWindowVisible(h):
            found.append(h)
    return True


u.EnumWindows(ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(cb), 0)
h = found[0]
fg = u.GetForegroundWindow()
t1 = u.GetWindowThreadProcessId(fg, None)
t2 = ctypes.windll.kernel32.GetCurrentThreadId()
u.AttachThreadInput(t2, t1, True)
u.SetForegroundWindow(h)
u.AttachThreadInput(t2, t1, False)
time.sleep(0.4)
for n in sys.argv[1].split(','):
    if n.startswith('w'):
        time.sleep(float(n[1:]))
        continue
    k = VK[n.upper()]
    u.keybd_event(k, 0, 0, 0)
    time.sleep(0.12)
    u.keybd_event(k, 0, 2, 0)
    time.sleep(0.35)
