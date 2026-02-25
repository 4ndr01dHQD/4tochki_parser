import re
import time
from logging import Logger

from config import FORTOCHKI_URL, DEBUG
from telegram.api import TelegramAPI
from telegram.schemas import TyreMessageSchema, TyreMessageType


class TelegramService:

    def __init__(self, logger: Logger, storage: dict):
        self.telegram_api = TelegramAPI()
        self.logger = logger
        self.storage = storage

    def run(self):
        self.logger.info('Starting telegram service')

        try:
            while True:
                if len(self.storage['notifications']):
                    data = self.storage['notifications'].pop()
                    if not DEBUG:
                        self.send_notification_message(data['message'], data['error'])

                if not len(self.storage['tyres']):
                    time.sleep(5)
                    continue

                tyre_message = self.storage['tyres'].pop()
                self.send_message(tyre_message)

        except Exception as err:
            self.logger.error(
                'Unexpected error: {}'.format(err),
                exc_info=True
            )
            self.send_notification_message("⚠️ Terminal parser raise error and has died.", str(err))

    def send_notification_message(self, message: str, error: str):
        text = (f"*{message}*\n"
                f"{error}")
        self.telegram_api.send_message(text)
        self.logger.info(f'Notification message has been sent.')

    def send_message(self, tyre_message: TyreMessageSchema) -> None:

        tyre = tyre_message.data

        text = (f"*{self.escape_markdown_v2(tyre['name'])}*\n"
                f"\n"
                f"*Сезон*: {tyre['season']}\n"
                f"*Размер*: {tyre['width']}/{tyre['height']} r{tyre['diametr']}\n"
                f"*RunFlat*: {'+' if tyre['runFlat'] else '-'}\n"
                f"\n"
                f"\n"
                f"*Цена*: {tyre['price']}\n"
                f"*Сток*: {tyre['rest']}\n"
                f"\n"
                f"[Ссылка]({FORTOCHKI_URL}/app/#/detail/{tyre['productId']}/)" #TODO: исправить!!!!!!!!!!
                )
        if tyre_message.type == TyreMessageType.quantity_changed:
            text = "*Изменение количества ‼*\n\n" + text

        self.telegram_api.send_photo_message(text, tyre_message.image)
        self.logger.info(f'Message has been sent.')

    @staticmethod
    def escape_markdown_v2(text: str) -> str:
        escape_chars = r'_*[]()~`>#+-=|{}.!'
        return re.sub(f'([{re.escape(escape_chars)}])', r'\\', text)