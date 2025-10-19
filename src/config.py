import os

from decouple import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = config('DEBUG', False, cast=bool)
TERMINAL_LOGIN = config('TERMINAL_LOGIN')
TERMINAL_PASSWORD = config('TERMINAL_PASSWORD')

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = config('TELEGRAM_CHAT_ID')


TERMINAL_URL = "https://terminal.yst.ru"

REQUEST_RETRY_TIMEOUT = [1, 2, 4, 8, 16, 32, 64, 128]