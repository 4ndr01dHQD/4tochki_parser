import json
import time
from logging import Logger

from redis import Redis

from src.config import TERMINAL_LOGIN, TERMINAL_PASSWORD
from src.terminal.client import TerminalApiClient
from src.terminal.exceptions import UnsuccessfullySeriesOfRequests


class TerminalParser:
    redis: Redis
    # REPOSITORY_CLS = FilterSQLAlchemyModelRepository

    def __init__(self, logger: Logger, storage: dict, redis: Redis):
        self.page = 1
        self.redis = redis
        self.logger = logger
        self.client = TerminalApiClient(self.logger)
        self.storage = storage
        # self.repository = self.REPOSITORY_CLS()

    def run(self):
        self.logger.info('Starting terminal parser')

        try:
            self.auth()
            while True:
                self.logger.info(f'Try to parse page: {str(self.page)}.')

                if not self.is_active_token:
                    self.logger.info(f'Token has been expired. Run reauth.')
                    self.logout()
                    self.auth()
                try:
                    tyres = self.client.get_catalog_page(self.page)
                except UnsuccessfullySeriesOfRequests:
                    time.sleep(60)
                    self.logout()
                    self.auth()
                    continue

                if not len(tyres): #TODO: проверить!!!
                    self.page = 1
                    self.logger.info(f'Restart parser.')
                    continue

                # self.process_tyres(tyres)
                time.sleep(2)
                self.page += 1

        except Exception as err:
            self.logger.error(
                'Unexpected error: {}'.format(err),
                exc_info=True,
                type=type(err)
            )
            self.storage["notifications"].append({
                "message": "⚠️ Terminal parser raise error and has died.",
                "error": err,
            })

    def auth(self):
        cached_token = self.redis.get(f"Token:{TERMINAL_LOGIN}")
        if cached_token:
            self.logger.info('token has been found in redis.')
            token = cached_token.decode("utf-8")
            self.client.set_token(token=token)
        else:
            self.logger.info('cached token has been not found.')
            data = self.client.auth(TERMINAL_LOGIN, TERMINAL_PASSWORD)
            self.redis.set(f"Token:{TERMINAL_LOGIN}", data['accessToken'], ex=60 * 60 * 12)

    @property
    def is_active_token(self):
        return self.redis.exists(f"Token:{TERMINAL_LOGIN}")


    def logout(self):
        if self.client.is_authenticated:
            self.client.logout()
            self.redis.delete(f"Token:{TERMINAL_LOGIN}")