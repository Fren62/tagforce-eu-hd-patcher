"""Virtual joypad for PPSSPP. Reads commands from cmd.txt (one per line):
btn NAME [ms] | wait S | shot NAME VARIANT | seq NAME,NAME,... | quit.  Writes 'done N' in log.txt"""
import os, sys, time, ctypes
from ctypes import wintypes
import vgamepad as vg
from PIL import ImageGrab

T = os.environ['TEMP']; D = T + '/vigem'
CMD, LOG = D + '/cmd.txt', D + '/log.txt'
B = vg.XUSB_BUTTON
M = dict(A=B.XUSB_GAMEPAD_A, B=B.XUSB_GAMEPAD_B, X=B.XUSB_GAMEPAD_X, Y=B.XUSB_GAMEPAD_Y, START=B.XUSB_GAMEPAD_START,
         BACK=B.XUSB_GAMEPAD_BACK, UP=B.XUSB_GAMEPAD_DPAD_UP, DOWN=B.XUSB_GAMEPAD_DPAD_DOWN, LEFT=B.XUSB_GAMEPAD_DPAD_LEFT,
         RIGHT=B.XUSB_GAMEPAD_DPAD_RIGHT, LB=B.XUSB_GAMEPAD_LEFT_SHOULDER, RB=B.XUSB_GAMEPAD_RIGHT_SHOULDER)
pad = vg.VX360Gamepad()
user32 = ctypes.windll.user32


def window_rect():
    found = []
    def cb(h, _):
        n = user32.GetWindowTextLengthW(h)
        if n:
            b = ctypes.create_unicode_buffer(n + 1); user32.GetWindowTextW(h, b, n + 1)
            if b.value.startswith('PPSSPP Gold') and user32.IsWindowVisible(h): found.append(h)
        return True
    user32.EnumWindows(ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(cb), 0)
    if not found: return None
    r = wintypes.RECT(); user32.GetWindowRect(found[0], ctypes.byref(r)); return (r.left, r.top, r.right, r.bottom)


def press(name, ms=120):
    pad.press_button(M[name]); pad.update(); time.sleep(ms / 1000)
    pad.release_button(M[name]); pad.update(); time.sleep(0.25)


def run(line):
    a = line.split()
    if not a: return
    if a[0] == 'btn': press(a[1].upper(), int(a[2]) if len(a) > 2 else 120)
    elif a[0] == 'seq':
        for n in a[1].split(','): press(n.upper())
    elif a[0] == 'wait': time.sleep(float(a[1]))
    elif a[0] == 'shot':
        r = window_rect(); d = f'{T}/shots/{a[2]}'; os.makedirs(d, exist_ok=True)
        if r: ImageGrab.grab(bbox=r, all_screens=True).save(f'{d}/{a[1]}.png')
    elif a[0] == 'quit': sys.exit(0)


open(CMD, 'w').close(); n = 0
while True:
    lines = open(CMD).read().splitlines()
    while n < len(lines):
        run(lines[n]); n += 1; open(LOG, 'w').write(f'done {n}')
    time.sleep(0.2)
