import os
import sys
from utils import TextBuffer
from pynput import keyboard
from pynput.keyboard import Key
DEBUG = True
text_buffer = TextBuffer()

usernames = sys.argv[1:]

usernames.append(os.environ.get("USERNAME"))

usernames.append("undefined")


def on_press(key):
    global buffer

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
