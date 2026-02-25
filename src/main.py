import threading

from db.config import redis_client
from logger import logger
from parser.parser import FortochkiParser
from telegram.service import TelegramService

# from telegram.service import TelegramService

if __name__ == '__main__':
    log = logger.new(component='http_parser')

    storage = {
        "tyres": [],
        "notifications": [],
    } # TODO вынести в отдельный класс

    parser_process = threading.Thread(target=FortochkiParser(logger=log, storage=storage, redis=None).run)
    # telegram_process = threading.Thread(target=TelegramService(logger=log, storage=storage).run)

    parser_process.start()
    # telegram_process.start()
