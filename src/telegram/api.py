from io import BytesIO

import requests

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


class TelegramAPI:
    URL = "https://api.telegram.org"
    BOT_TOKEN = TELEGRAM_TOKEN
    CHAT_ID = TELEGRAM_CHAT_ID

    # TODO handle error Too Many Requests
    def send_photo_message(self, text: str, image: BytesIO) -> dict:
        url = f"{self.URL}/bot{self.BOT_TOKEN}/sendPhoto"

        data = {'chat_id': self.CHAT_ID, 'caption': text, "parse_mode": "Markdown"}
        files = {'photo': image}

        response = requests.post(url=url, data=data, files=files)

        if response.status_code != 200:
            raise Exception(f"Telegram API Error: {response.text}")

        return response.json()

    def send_message(self, text: str) -> dict:
        url = f"{self.URL}/bot{self.BOT_TOKEN}/sendMessage"

        data = {'chat_id': self.CHAT_ID, 'text': text, "parse_mode": "Markdown"}

        response = requests.post(url=url, data=data)

        if response.status_code != 200:
            raise Exception(f"Telegram API Error: {response.text}")

        return response.json()
