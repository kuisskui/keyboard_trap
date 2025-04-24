import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')


class TextBuffer:
    def __init__(self):
        self.usernames = []
        self.buffer = None
        self.init_buffer()

    def send_message(self):
        message = self.usernames[0] + ": " + self.buffer
        payload = {"content": message}
        requests.post(WEBHOOK_URL, data=payload)

    def init_buffer(self):
        self.buffer = ""

    def handle_char(self, character):
        self.buffer += character

    def handle_backspace(self):
        self.buffer = self.buffer[:-1]

    def handle_enter(self):
        self.send_message()
        self.init_buffer()

    def handle_space(self):
        self.buffer += " "

    def handle_esc(self):
        return False
