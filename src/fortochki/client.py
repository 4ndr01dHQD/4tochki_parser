from logging import Logger

import requests

from config import FORTOCHKI_URL
from fortochki.utils import retry_error_request


class FortochkiApiClient:
    logger: Logger
    URL = FORTOCHKI_URL
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    is_authenticated = False


    def __init__(self, logger: Logger):
        self.logger = logger
        self.__session = requests.Session()
        self.__session.headers.update({'User-Agent': self.USER_AGENT})


    # def auth(self, login: str, password: str) -> dict:
    #     response = self.login(login, password)
    #     data = response.json()
    #
    #     self.is_authenticated = True
    #     self.logger.info("Service has been login.")
    #     return data
    #
    # @retry_error_request
    # def login(self, login: str, password: str) -> Response:
    #     body = {
    #         "username": login,
    #         "password": password,
    #     }
    #     response = self.__session.post(f"{self.URL}/api/Auth/login", json=body)
    #     return response

    def set_token(self, token: str):
        self.__session.headers.update({
            "Cookie":f"ASP.NET_SessionId={token};",
        })
    #
    # @retry_error_request
    # def logout(self):
    #     response = self.__session.post(f"{self.URL}/api/Auth/logout")
    #     self.is_authenticated = False
    #     self.logger.info("Service has been logged out.")
    #     return response

    @retry_error_request
    def get_catalog_page(self, data: dict):
        response = self.__session.get(f"{self.URL}/Product/Tire?kpt=1&fc_pst=1&cmpx=0&ft_w=205&ft_h=60&ft_s=2&ft_p=0&ft_st=0&fc_uaid=41243&fc_wh=1418&fc_wh=232&fc_wh=2184&fc_wh=1222&fc_whg=2&fc_wh=2156&fc_zwid=1418")
        return response
#TODO: ПОЗЖЕ ИСПРАВИТЬ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # def get_image(self, photo_url: str) -> BytesIO:
    #     remote_image = self.__session.get(photo_url)
    #     photo = BytesIO(remote_image.content)
    #     photo.name = 'img.png'
    #
    #     return photo