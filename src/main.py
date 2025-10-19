import threading

from db.config import redis_client
from logger import logger
from src.parser.parser import TerminalParser

# from telegram.service import TelegramService

if __name__ == '__main__':
    log = logger.new(component='http_parser')

    storage = {
        "tyres": [],
        "notifications": [],
    } # TODO вынести в отдельный класс

    parser_process = threading.Thread(target=TerminalParser(logger=log, storage=storage, redis=redis_client).run)
    # telegram_process = threading.Thread(target=TelegramService(logger=log, storage=storage).run)

    parser_process.start()
    # telegram_process.start()
