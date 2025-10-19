import time
from json import JSONDecodeError
from logging import Logger

import requests
from requests import Response
from urllib3.exceptions import NewConnectionError, MaxRetryError

from src.config import REQUEST_RETRY_TIMEOUT, TERMINAL_URL
from src.terminal.exceptions import InvalidAuthError, UnexpectedResponseError, UnsuccessfullySeriesOfRequests, \
    HTTPError500, UnexpectedStatusError


class TerminalApiClient:
    logger: Logger
    URL = TERMINAL_URL
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    is_authenticated = False
    PAGESIZE = 40


    def __init__(self, logger: Logger):
        self.logger = logger
        self.__session = requests.Session()
        self.__session.headers.update({'User-Agent': self.USER_AGENT})


    def auth(self, login: str, password: str) -> dict:
        for i in REQUEST_RETRY_TIMEOUT:
            response = self.login(login, password)
            if response.status_code != 200:
                self.logger.warning(
                    "Unexpected response by terminal api while logging in.",
                    staus=response.status_code,
                    content=response.content,
                )
                time.sleep(i)
                continue

            data = response.json()

            self.is_authenticated = True
            self.logger.info("Service has been login.")
            return data
        else:
            raise InvalidAuthError()

    def login(self, login: str, password: str) -> Response:
        body = {
            "username": login,
            "password": password,
        }
        response = self.__session.post(f"{self.URL}/api/Auth/login", json=body)
        return response

    def set_token(self, token: str):
        self.__session.headers.update({"Authorization": f"Bearer {token}"})

    def logout(self):
        response = self.__session.post(f"{self.URL}/api/Auth/logout")
        if response.status_code != 200:
            self.logger.error(
                "Unexpected response by terminal api while logout.",
                staus=response.status_code,
                content=response.content,
            )
            raise UnexpectedResponseError("Unexpected response by terminal api while logout.")
        self.is_authenticated = False
        self.logger.info("Service has been logged out.")

    def get_catalog_page(self, page: int) -> dict:
        params = self._make_catalog_page_params(page)
        response = None

        for timeout in REQUEST_RETRY_TIMEOUT:
            try:
                response = self.__session.get(f"{self.URL}/api/product/list", params=params)
                if response.status_code == 200:
                    break
                else:
                    self.logger.error(
                        "Unexpected response by terminal api while getting catalog page.",
                        staus=response.status_code,
                        content=response.content,
                    )
                    time.sleep(timeout)
            except (NewConnectionError, ConnectionError, MaxRetryError):
                time.sleep(timeout)
                continue
            except Exception as e:
                time.sleep(timeout)
                continue

        if not response:
            self.logger.error("An unsuccessful series of requests.")
            raise UnsuccessfullySeriesOfRequests("An unsuccessful series of requests.")

        return self.process_catalog_data(response)

    def process_catalog_data(self, response: Response) -> dict:
        if response.status_code == 200:
            try:
                return response.json()
            except JSONDecodeError:
                self.logger.error(
                    "Unexpected response by mim api while getting catalog page.",
                    staus=response.status_code,
                    content=response.content,
                )
                raise UnexpectedResponseError
        elif response.status_code >= 500:
            self.logger.error(
                "Server return http code 500.",
                staus=response.status_code,
                content=response.content,
            )
            raise HTTPError500
        else:
            self.logger.error(
                "Unexpected status by mim api while getting catalog page.",
                staus=response.status_code,
                content=response.content,
            )
            raise UnexpectedStatusError("Unexpected status by mim api while getting catalog page.")

    def _make_catalog_page_params(self, page: int) -> dict:
        return {
            "sort": "Market",
            "productType": 1,
            "pageSize": self.PAGESIZE,
            "isSet": False,
            "typeOfRests": 1,
            "saleTypes": "",
            "isCargo": False,
            "allOrByCarReplica": False,
            "isEmpty": True,
            "page": page,
            "priceMin": 1000,
            "priceMax": 500000,
        }