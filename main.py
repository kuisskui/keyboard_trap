import os
import sys
from utils import TextBuffer, get_bool
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from dotenv import load_dotenv

load_dotenv()

DEBUG = get_bool(os.environ.get('DEBUG'))

usernames = sys.argv[1:]

usernames.append(os.environ.get("USERNAME"))

usernames.append("undefined")

text_buffer = TextBuffer(usernames)


def on_press(key: KeyCode) -> None or bool:
    try:
        text_buffer.handle_char(key.char)

    except AttributeError:
        if key == Key.backspace:
            text_buffer.handle_backspace()
        if key == Key.enter:
            text_buffer.handle_enter()
        if key == Key.space:
            text_buffer.handle_space()
        if DEBUG:
            print(key)
            if key == Key.esc:
                return text_buffer.handle_esc()


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
