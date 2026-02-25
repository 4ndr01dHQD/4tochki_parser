import os
import time
from io import BytesIO
from logging import Logger
from typing import List, Dict

from bs4 import BeautifulSoup, Tag
from redis import Redis

from config import FORTOCHKI_TOKEN
from db.filter.repository import FilterSQLAlchemyModelRepository
from parser.model import FilterDomain
from parser.utils import is_price_relevant
from telegram.schemas import TyreMessageType, TyreMessageSchema
from fortochki.client import FortochkiApiClient
from fortochki.exceptions import UnsuccessfullySeriesOfRequests


class FortochkiParser:
    redis: Redis
    repository: FilterSQLAlchemyModelRepository
    PAGESIZE = 40

    def __init__(self, logger: Logger, storage: dict, redis: Redis):
        self.redis = redis
        self.logger = logger
        self.client = FortochkiApiClient(self.logger)
        self.storage = storage
        self.repository = FilterSQLAlchemyModelRepository()

    def run(self):
        self.logger.info('Starting terminal parser')

        try:
            self.auth()
            while True:
                filters = self.get_filters()
                for filter in filters:
                    page_num = 1
                    while True:
                        #                     if not self.is_active_token:
                        #                         self.logger.info(f'Token has been expired. Run reauth.')
                        #                         self.logout()
                        #                         self.auth()
                        tyres = None
                        try:
                            params = self._make_catalog_page_params(page_num, filter)
                            response = self.client.get_catalog_page(params)

                            soup = BeautifulSoup(response.text, 'html.parser')

                            tyres = self.get_tyres(soup)

                        except UnsuccessfullySeriesOfRequests:
                            time.sleep(60)
                            raise UnsuccessfullySeriesOfRequests()
                            # self.logout()
                            # self.auth()
                            # continue

                        if not tyres or not len(tyres):
                            self.logger.warning(
                                f'Tyres for filter not found: {str(filter.id)}: {str(filter.title)}.'
                            )
                            break

                        self.process_tyres(tyres, filter)
                        time.sleep(1)
                        page_num += 1

        except Exception as err:
            self.logger.error(
                'Unexpected error: {}'.format(err),
                exc_info=True,
                type=type(err)
            )
            self.storage["notifications"].append({
                "message": "⚠️ Fortochki parser raise error and has died.",
                "error": err,
            })


    def auth(self):
        token = FORTOCHKI_TOKEN
    #     cached_token = self.redis.get(f"TerminalToken:{TERMINAL_LOGIN}")
    #     if cached_token:
    #         self.logger.info('token has been found in redis.')
    #         token = cached_token.decode("utf-8")
    #     else:
    #         self.logger.info('cached token has been not found.')
    #         data = self.client.auth(TERMINAL_LOGIN, TERMINAL_PASSWORD)
    #         self.redis.set(f"TerminalToken:{TERMINAL_LOGIN}", data['accessToken'], ex=60 * 60 * 6)
    #         token = data['accessToken']
        self.client.set_token(token=token)
    #
    # @property
    # def is_active_token(self):
    #     return self.redis.exists(f"TerminalToken:{TERMINAL_LOGIN}")
    #
    # def logout(self):
    #     if self.client.is_authenticated:
    #         self.client.logout()
    #         self.redis.delete(f"TerminalToken:{TERMINAL_LOGIN}")
    #
    def process_tyres(self, tyres: List[Tag], filter: FilterDomain):
        self.logger.info(f'Process tyres.', length=len(tyres))

        for tyre in tyres:
            price = tyre.select_one("tr td:nth-of-type(6) span").get_text(strip=True)
            if price is not None:
                price = int(price.replace(' ', ''))
                if not is_price_relevant(price, filter):
                    continue

            self.set_tyre(tyre)

    def get_filters(self) -> List[FilterDomain]:
        return self.repository.all()


    def set_tyre(self, tyre: dict) -> None:
        cached_quantity = self.redis.get(f"fortochki:tyre:{tyre['productId']}")

        if cached_quantity is not None and int(cached_quantity) == int(tyre['rest']):
            return

        message_type = TyreMessageType.default if cached_quantity is None or int(cached_quantity) == int(
            tyre['rest']) else TyreMessageType.quantity_changed

        self.storage["tyres"].append(
            TyreMessageSchema(
                data=tyre,  # TODO вынести в pydantic
                image=self.get_image(tyre),
                type=message_type
            )
        )
        self.redis.set(f"fortochki:tyre:{tyre['productId']}", tyre['rest'], ex=60 * 60 * 12)

    # def get_image(self, tyre: dict) -> BytesIO:
    #     image = f"/storage/{tyre['productId']}/md.jpg"
    #     photo_url = f"{IMAGE_URL}{image}"
    #     return self.client.get_image(photo_url)
    #
    def _make_catalog_page_params(self, page: int, filter_obj: FilterDomain) -> dict:

        params = {
            "kpt": "1",
            "fc_pst": "1",
            "cmpx": "0",
            "ft_p": "0",
            "ft_st": "0",
            "fc_uaid": "41243",
            "fc_whg": "2",
            "fc_zwid": "1418",
        }

        if filter_obj.width is not None:
            params['ft_w'] = filter_obj.width

        if filter_obj.height is not None:
            params['ft_h'] = filter_obj.height

        if filter_obj.diametr is not None:
            params['ft_d'] = filter_obj.diametr

        if filter_obj.season is not None:
            params['ft_s'] = filter_obj.season

        if filter_obj.brand is not None:
            params['fc_b'] = filter_obj.brand

        if filter_obj.code is not None:
            params['fc_vc'] = filter_obj.code

        if filter_obj.cae is not None:
            params['fc_c'] = filter_obj.cae

        return params

    def get_tyres(self, soup: BeautifulSoup) -> List    :
        return soup.select('form .table-1 tbody:has(img)')
